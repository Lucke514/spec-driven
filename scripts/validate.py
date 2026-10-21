#!/usr/bin/env python3
"""Deterministic checks for spec-driven artifacts.

Usage:
  python3 validate.py specs/<slug>           # spec.md, plus plan.md / tasks.md if present
  python3 validate.py specs/<slug>/spec.md   # a collapsed Small spec (one file with "## Tasks")

Prints one line per finding, "file:line: error|warning: message".
Exit status: 0 when no errors, 1 on any error, 2 on a usage error.

Checks:
  - header block: a valid Status and a YYYY-MM-DD "Last updated" line
  - no "[NEEDS CLARIFICATION" marker once Status is not draft
  - R#/E#/SC#/C#/T#/G# ids unique within their file
  - every live R#/E# (not superseded, deferred or an accepted limitation)
    is named by a component's Implements (Standard) and by a task's Implements
  - no Implements, Component, coverage or evidence line names an id that does not exist
  - every component not cut is covered by a task; every component implements something
  - task anchors: "## T#" / "## G#" headings, exactly one box line in a known
    state, exactly one **Owner** line and one **Notes** line
  - Standard: Success criteria holds at least one SC#; every spec: a Minimum shippable line
"""
import argparse
import datetime
import os
import re
import sys

SPEC_STATUSES = {"draft", "in-review", "approved", "implemented", "superseded", "abandoned"}
TASKS_STATUSES = {"draft", "in-review", "approved", "abandoned"}

RE_H2 = re.compile(r"^##\s+(.*?)\s*$")
RE_DEF_SPEC = re.compile(r"^\s*-\s+\*\*((?:R|E|SC)\d+)\*\*")
RE_DEF_C = re.compile(r"^###\s+(C\d+)\b")
RE_TASK_HEAD = re.compile(r"^(#{1,6})\s+([TG]\d+)\b")
RE_SPEC_REF = re.compile(r"\b((?:R|E|SC)\d+)\b")
RE_REQ = re.compile(r"^[RE]\d+$")
RE_C_REF = re.compile(r"\b(C\d+)\b")
RE_IMPLEMENTS = re.compile(r"\*\*Implements\*\*:\s*([^·]*)")
RE_COMPONENT = re.compile(r"\*\*Component\*\*:\s*([^·]*)")
RE_BOX = re.compile(r"^-\s*\[.\]")
RE_KNOWN_BOX = re.compile(
    r"^- \[[ x]\] Done\s*$"
    r"|^- \[~\] Waived — \d{4}-\d{2}-\d{2}\b"
    r"|^- \[>\] Deferred — \d{4}-\d{2}-\d{2}\b"
    r"|^- \[!\] Blocked — \d{4}-\d{2}-\d{2}\b"
)
RE_NOT_LIVE = re.compile(r"—\s*(superseded|deferred|accepted limitation)\b", re.I)
RE_CUT = re.compile(r"—\s*cut\b", re.I)


class Report:
    def __init__(self):
        self.items = []

    def error(self, path, line, msg):
        self.items.append((path, line, "error", msg))

    def warning(self, path, line, msg):
        self.items.append((path, line, "warning", msg))

    def errors(self):
        return sum(1 for i in self.items if i[2] == "error")


def load(path):
    """Read a file; blank HTML comments and fenced code so line numbers stay true."""
    with open(path, encoding="utf-8") as f:
        raw = f.read().split("\n")
    lines, in_comment, in_fence = [], False, False
    for line in raw:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            lines.append("")
            continue
        if in_fence:
            lines.append("")
            continue
        out = ""
        rest = line
        while rest:
            if in_comment:
                end = rest.find("-->")
                if end < 0:
                    rest = ""
                else:
                    rest, in_comment = rest[end + 3:], False
            else:
                start = rest.find("<!--")
                if start < 0:
                    out, rest = out + rest, ""
                else:
                    out, rest, in_comment = out + rest[:start], rest[start + 4:], True
        lines.append(out)
    return lines


class Part:
    """A file, or a line range of one (the two halves of a collapsed Small spec)."""

    def __init__(self, path, lines, start=0, end=None):
        self.path, self.lines = path, lines
        self.start, self.end = start, len(lines) if end is None else end

    def rows(self, start=None, end=None):
        for i in range(self.start if start is None else start, self.end if end is None else end):
            yield i + 1, self.lines[i]

    def sections(self):
        """Level-2 sections as (title, first line index, end index)."""
        heads = [(i, m.group(1)) for i in range(self.start, self.end)
                 for m in [RE_H2.match(self.lines[i])] if m]
        return [(t, i, heads[k + 1][0] if k + 1 < len(heads) else self.end)
                for k, (i, t) in enumerate(heads)]

    def section(self, name):
        for title, s, e in self.sections():
            if title.lower().startswith(name.lower()):
                return s, e
        return None


def check_header(part, statuses, rep):
    """Validate the "> Status:" / "> Last updated:" block; return the status word."""
    status = None
    found_status = found_date = False
    for n, line in part.rows():
        m = re.match(r"^>\s*Status:\s*(.*)$", line)
        if m and not found_status:
            found_status = True
            value = m.group(1).strip()
            if value.startswith("pending sign-off"):
                status = "pending sign-off"
            else:
                word = re.match(r"[a-z-]*", value).group(0)
                if word in statuses:
                    status = word
                else:
                    rep.error(part.path, n, "Status '%s' is not one of: %s, pending sign-off: <role>"
                              % (value, " | ".join(sorted(statuses))))
        m = re.match(r"^>\s*Last updated:\s*(.*)$", line)
        if m and not found_date:
            found_date = True
            value = m.group(1).strip()
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                rep.error(part.path, n, "Last updated '%s' is not a YYYY-MM-DD date" % value)
    if not found_status:
        rep.error(part.path, part.start + 1, "header block has no '> Status:' line")
    if not found_date:
        rep.error(part.path, part.start + 1, "header block has no '> Last updated:' line")
    return status


def check_markers(part, status, rep):
    if status in (None, "draft"):
        return
    for n, line in part.rows():
        if "[NEEDS CLARIFICATION" in line:
            rep.error(part.path, n, "[NEEDS CLARIFICATION] marker left while Status is %s" % status)


def collect(part, pattern, rep, group=1):
    """Map each id the pattern defines to its first line; report duplicates."""
    found = {}
    for n, line in part.rows():
        m = pattern.match(line)
        if not m:
            continue
        ident = m.group(group)
        if ident in found:
            rep.error(part.path, n, "duplicate id %s (first defined at line %d)" % (ident, found[ident][0]))
        else:
            found[ident] = (n, line)
    return found


def check_refs(part, n, text, known, rep, what):
    for ident in RE_SPEC_REF.findall(text):
        if ident not in known:
            rep.error(part.path, n, "%s names %s, which the spec does not define" % (what, ident))


def table_rows(part, span):
    """Data rows of the first Markdown table in a section: (line number, cells)."""
    rows = []
    for n, line in part.rows(*span):
        s = line.strip()
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip().strip("`") for c in s.strip("|").split("|")]
        rows.append((n, cells))
    return [r for r in rows[1:] if not re.match(r"^:?-+:?$", r[1][0] or "-")]


def check_spec(part, small, rep):
    defs = collect(part, RE_DEF_SPEC, rep)
    live = [i for i, (n, line) in defs.items() if RE_REQ.match(i) and not RE_NOT_LIVE.search(line)]
    scen = part.section("Users & scenarios")
    if scen:
        for n, line in part.rows(*scen):
            check_refs(part, n, line, defs, rep, "coverage line")
    ms = [(n, line) for n, line in part.rows() if "**Minimum shippable**" in line]
    if not ms:
        rep.error(part.path, part.start + 1, "no '**Minimum shippable**:' line in Requirements")
    for n, line in ms:
        value = line.split("**Minimum shippable**", 1)[1].lstrip(":* ").strip()
        if not value:
            rep.error(part.path, n, "Minimum shippable line is empty")
        check_refs(part, n, value, defs, rep, "Minimum shippable")
    if not small:
        sc = part.section("Success criteria")
        if not sc:
            rep.error(part.path, part.start + 1, "no '## Success criteria' section (required at Standard)")
        elif not any(RE_DEF_SPEC.match(l) and l.strip().startswith("- **SC") for _, l in part.rows(*sc)):
            rep.error(part.path, sc[0] + 1, "Success criteria holds no SC# (required at Standard)")
    return defs, live


def check_coverage_table(part, span, spec_ids, live, rep, name, components=None):
    rows = table_rows(part, span)
    seen = set()
    for n, cells in rows:
        ident = cells[0]
        if not RE_SPEC_REF.fullmatch(ident or ""):
            continue
        seen.add(ident)
        if ident not in spec_ids:
            rep.error(part.path, n, "%s row names %s, which the spec does not define" % (name, ident))
        rest = " ".join(cells[1:])
        if len(cells) < 2 or any(not c for c in cells[1:]):
            rep.error(part.path, n, "%s row for %s has an empty cell" % (name, ident))
        if components is not None:
            for c in RE_C_REF.findall(rest):
                if c not in components:
                    rep.error(part.path, n, "%s row names %s, which the plan does not define" % (name, c))
    for ident in live:
        if ident not in seen:
            rep.error(part.path, span[0] + 1, "%s has no row for %s" % (name, ident))


def check_evidence(part, spec_ids, live, rep):
    head = next((n - 1 for n, l in part.rows() if re.match(r"^#{2,3}\s+Evidence per requirement", l)), None)
    span = None if head is None else (head, part.end)
    if span:
        check_coverage_table(part, span, spec_ids, live, rep, "Evidence per requirement")
    else:
        rep.warning(part.path, part.start + 1, "no '## Evidence per requirement' table")


def check_plan(part, spec_ids, live, rep):
    comps = collect(part, RE_DEF_C, rep)
    heads = sorted((n - 1, c) for c, (n, _) in comps.items())
    implemented, active = set(), set()
    for k, (i, c) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else part.end
        for title, s, e in part.sections():
            if s > i:
                end = min(end, s)
                break
        body = "\n".join(part.lines[i:end])
        if RE_CUT.search(body):
            continue
        active.add(c)
        ids = []
        for n, line in part.rows(i, end):
            m = RE_IMPLEMENTS.search(line)
            if m:
                check_refs(part, n, m.group(1), spec_ids, rep, "%s Implements" % c)
                ids += [x for x in RE_SPEC_REF.findall(m.group(1)) if RE_REQ.match(x)]
        if not ids:
            rep.error(part.path, i + 1, "%s implements no R#/E# from the spec; cut it" % c)
        implemented.update(ids)
    for ident in live:
        if ident not in implemented:
            rep.error(part.path, part.start + 1, "%s is not named by any component's Implements" % ident)
    span = part.section("Requirement coverage")
    if span:
        check_coverage_table(part, span, spec_ids, live, rep, "Requirement coverage", comps)
    else:
        rep.error(part.path, part.start + 1, "no '## Requirement coverage' table")
    check_evidence(part, spec_ids, live, rep)
    return comps, active


def check_tasks(part, spec_ids, live, comps, active, rep):
    for n, line in part.rows():
        m = RE_TASK_HEAD.match(line)
        if m and len(m.group(1)) != 2:
            rep.error(part.path, n, "task heading %s must be level '##', not '%s'" % (m.group(2), m.group(1)))
    collect(part, re.compile(r"^##\s+([TG]\d+)\b"), rep)
    named, covered = set(), set()
    for title, s, e in part.sections():
        m = re.match(r"([TG]\d+)\b", title)
        if not m:
            continue
        tid, boxes, owners, notes = m.group(1), [], 0, 0
        for n, line in part.rows(s + 1, e):
            if RE_TASK_HEAD.match(line):
                break
            if RE_BOX.match(line):
                boxes.append((n, line))
            owners += bool(re.match(r"^\s*-\s+\*\*Owner\*\*:", line))
            notes += bool(re.match(r"^\s*-\s+\*\*Notes\*\*:", line))
            im = RE_IMPLEMENTS.search(line)
            if im:
                check_refs(part, n, im.group(1), spec_ids, rep, "%s Implements" % tid)
                named.update(RE_SPEC_REF.findall(im.group(1)))
            cm = RE_COMPONENT.search(line)
            if cm and comps is not None:
                for c in RE_C_REF.findall(cm.group(1)):
                    covered.add(c)
                    if c not in comps:
                        rep.error(part.path, n, "%s Component names %s, which the plan does not define" % (tid, c))
        if len(boxes) != 1:
            rep.error(part.path, s + 1, "%s has %d box lines; exactly one is required" % (tid, len(boxes)))
        for n, line in boxes:
            if not RE_KNOWN_BOX.match(line.rstrip()):
                rep.error(part.path, n, "%s box line is not a known state: %s" % (tid, line.strip()))
        if owners != 1:
            rep.error(part.path, s + 1, "%s has %d **Owner** lines; exactly one is required" % (tid, owners))
        if notes != 1:
            rep.error(part.path, s + 1, "%s has %d **Notes** lines; exactly one is required" % (tid, notes))
    for ident in live:
        if ident not in named:
            rep.error(part.path, part.start + 1, "%s is not named by any task's Implements" % ident)
    for c in sorted(active):
        if c not in covered:
            rep.error(part.path, part.start + 1, "component %s is not covered by any task" % c)


def validate(target, rep):
    if os.path.isdir(target):
        folder, spec_path = target, os.path.join(target, "spec.md")
    else:
        folder, spec_path = os.path.dirname(target) or ".", target
    if not os.path.isfile(spec_path):
        print("validate.py: no spec.md at %s" % spec_path, file=sys.stderr)
        return False
    lines = load(spec_path)
    split = next((i for i, l in enumerate(lines) if re.match(r"^##\s+Tasks\s*$", l)), None)
    small = split is not None
    spec = Part(spec_path, lines, 0, split)
    status = check_header(spec, SPEC_STATUSES, rep)
    check_markers(Part(spec_path, lines), status, rep)
    spec_ids, live = check_spec(spec, small, rep)
    if small:
        tasks = Part(spec_path, lines, split)
        check_evidence(tasks, spec_ids, live, rep)
        check_tasks(tasks, spec_ids, live, None, set(), rep)
        return True
    plan_path, tasks_path = os.path.join(folder, "plan.md"), os.path.join(folder, "tasks.md")
    comps, active = None, set()
    if os.path.isfile(plan_path):
        plan = Part(plan_path, load(plan_path))
        check_markers(plan, check_header(plan, SPEC_STATUSES, rep), rep)
        comps, active = check_plan(plan, spec_ids, live, rep)
    if os.path.isfile(tasks_path):
        tasks = Part(tasks_path, load(tasks_path))
        check_markers(tasks, check_header(tasks, TASKS_STATUSES, rep), rep)
        check_tasks(tasks, spec_ids, live, comps, active, rep)
    if status in ("in-review", "approved", "pending sign-off"):
        for p in (plan_path, tasks_path):
            if not os.path.isfile(p):
                rep.warning(spec_path, 1, "spec is %s but %s is missing" % (status, os.path.basename(p)))
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", nargs="+", help="specs/<slug> directory, or a collapsed Small spec.md")
    args = parser.parse_args(argv)
    rep, ok = Report(), True
    for target in args.target:
        ok = validate(target, rep) and ok
    for path, line, level, msg in sorted(rep.items, key=lambda i: (i[0], i[1])):
        print("%s:%d: %s: %s" % (path, line, level, msg))
    if not ok:
        return 2
    return 1 if rep.errors() else 0


if __name__ == "__main__":
    sys.exit(main())
