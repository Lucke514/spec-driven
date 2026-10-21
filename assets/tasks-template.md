<!--
Anchors — every resume rule parses this file. Keep these exact shapes.
- Tasks and gap tasks are both `##`: `## T1`, `## G1`. Ids are stable — never renumbered, never reused after deletion; `G#` numbering continues across passes.
- Report blocks are `### Verification report — <slug> — <YYYY-MM-DD> — pass <n>`, strictly one level below `## Verification reports`; `<n>` counts from 1 across the feature's passes.
- Exactly one `**Notes**` line per task: overwrite the `—` placeholder, never add a second.
- Box states: `- [ ] Done` open · `- [x] Done` complete · `- [~] Waived — YYYY-MM-DD, why` (declined) · `- [>] Deferred — YYYY-MM-DD, owner <who>` (ships later; closed for this feature's verification, never counted unchecked) · `- [!] Blocked — YYYY-MM-DD, <what the user must do>` (required and in scope, executable only by the user; open, not closed).
- `**Owner**` names who or which branch is executing the task, since YYYY-MM-DD; `—` means unclaimed. Set when the task starts (a separate claim commit only when the work spans branches or agents: `references/implement.md` → Claiming a task), released on completion or handback, stale past the plan's **Task span**. Keep the line bare — no trailing comment for a rule to misread.
- `[P]` on a task heading = runs in parallel with the `[P]` tasks it is contiguous with; the first task without `[P]` ends the group.
- Status enum: draft | in-review | approved | abandoned.
-->

# Tasks: [Feature name]

> Spec: [spec.md](./spec.md) · Plan: [plan.md](./plan.md)
> Status: draft
> Last updated: [YYYY-MM-DD]

[One task = one focused session. Done means: **Verify** passes, the plan's gates pass with no new failures against their baselines, and the diff is clean per the junk-code checklist. A data change, a dependency change, a delivery step and the kill-switch exercise are each their own task (`references/data-and-delivery.md`, `references/dependencies.md`); the documentation task is always present.]

## T1 — [Task name]

- [ ] Done
- **Owner**: —
- **Component**: C1 · **Implements**: R1
- **Files**: [e.g. `src/module.py`, `tests/test_module.py`]
- **Do**: [Concrete change to make.]
- **Acceptance**: [Observable result that must hold.]
- **Verify**: `[the evidence for its Implements ids: test, measurement command, stand-in, or approved manual check — e.g. pytest tests/test_module.py]`
- **Notes**: — [overwrite on completion: what landed, where (the commit(s) carrying it, or `uncommitted, local to <who>`), the Decisions date of any shortcut taken, and `Clean-code: <n> hits — <what> | none · close calls: <each one, and which way it went> | none` — `none` recorded, never left unwritten]

## T2 [P] — [Task name]

- [ ] Done
- **Owner**: —
- **Component**: C2 · **Implements**: R2, E1
- **Files**: ...
- **Do**: ...
- **Acceptance**: ...
- **Verify**: ...
- **Notes**: —

## T[N] — Document the feature

- [ ] Done
- **Owner**: —
- **Component**: — · **Implements**: all (documentation)
- **Files**: `docs/<slug>.md` (+ README/CHANGELOG if the project keeps them)
- **Do**: Write `docs/<slug>.md` from the doc template; update README/CHANGELOG where kept; add doc comments on public interfaces.
- **Acceptance**: Docs describe actual behavior; every example runs as written.
- **Verify**: run each documented example
- **Notes**: —

---

## Gaps found in verification

[Appended by Phase 7 as `## G1`, `## G2`, … — same fields as a task, same `##` level, below this line. The section ends at `## Verification reports`.]

---

## Verification reports

[Appended by Phase 7 — one block per pass, newest last, never overwritten. Contents: `references/verification.md`.]

### Verification report — [slug] — [YYYY-MM-DD] — pass [n]
