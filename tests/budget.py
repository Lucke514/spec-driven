#!/usr/bin/env python3
"""Instruction-cost budget for the spec-driven skill.

Counts the words an agent must load on each depth's default path before it
presents its first artifact, and fails if any path is over its budget.

Usage: python3 tests/budget.py [--root DIR]
Exit status: 0 all paths within budget, 1 a path is over or a section is missing.

The mapping below is derived from SKILL.md's load triggers on the default
no-team path (Team signals finds nothing; Data changes, Delivery and
Dependencies keep their defaults). When SKILL.md changes what a phase loads
before the first presented artifact, update PATHS in the same change.
Words are counted like `wc -w`: whitespace-separated tokens.
"""

import argparse
import os
import re
import sys

# (file, section heading or None for the whole file)
TRIVIAL = [
    ("SKILL.md", None),
    ("references/clean-code.md", None),  # core rule 6: the Trivial self-review
]

PHASE_1 = [
    ("SKILL.md", None),
    ("references/writing-specs.md", None),  # Phase 1: "Read ... now"
    ("references/sign-off.md", None),  # Phase 1: Sign-off rows
    ("references/team-and-review.md", "Team signals"),  # Phase 1, every depth
    ("assets/spec-template.md", None),
]

PATHS = {
    "Trivial (whole run)": TRIVIAL,
    "Small (to the spec)": PHASE_1,
    "Standard (to the proposal)": PHASE_1 + [
        ("references/verification.md", "Recording gates"),  # Phase 3 gates
        ("references/team-and-review.md", "Integration"),  # Phase 3 Integration
        ("assets/plan-template.md", None),
        ("assets/tasks-template.md", None),
    ],
}

# Measured at 3.2.0 and set about 10% above. Raise one only by deleting
# text at least as costly on the same path (tests/README.md).
BUDGET = {
    "Trivial (whole run)": 4200,
    "Small (to the spec)": 7500,
    "Standard (to the proposal)": 10700,
}

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def words(text):
    return len(text.split())


def section(text, name):
    """Return the section whose heading starts with `name`, up to the next
    heading of the same or a higher level; None if absent."""
    lines = text.splitlines()
    start, level = None, None
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m:
            continue
        if start is None:
            if m.group(2).strip().startswith(name):
                start, level = i, len(m.group(1))
        elif len(m.group(1)) <= level:
            return "\n".join(lines[start:i])
    return None if start is None else "\n".join(lines[start:])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument("--root", default=default_root, help="skill directory")
    args = parser.parse_args()

    failed = False
    rows = []
    for depth, parts in PATHS.items():
        total = 0
        for path, name in parts:
            with open(os.path.join(args.root, path), encoding="utf-8") as fh:
                text = fh.read()
            if name is not None:
                text = section(text, name)
                if text is None:
                    print("error: %s has no section '%s'" % (path, name))
                    failed = True
                    continue
            total += words(text)
        limit = BUDGET[depth]
        ok = total <= limit
        failed = failed or not ok
        rows.append((depth, total, limit, "pass" if ok else "FAIL"))

    print("%-28s %8s %8s  %s" % ("Path", "Words", "Budget", "Result"))
    for depth, total, limit, result in rows:
        print("%-28s %8d %8d  %s" % (depth, total, limit, result))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
