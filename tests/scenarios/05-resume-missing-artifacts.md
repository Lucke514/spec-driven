# S05 — Resuming work with a broken artifact set

**Depth expected:** n/a — resume path
**Exercises:** Resuming work, work-present check, missing-artifact recovery, artifact cross-check.

## Fixture
The S02 service, plus a half-finished feature:
- `specs/task-comments/spec.md` — Status `approved`, 4 requirements, `Last updated` 20 days ago.
- `specs/task-comments/tasks.md` — T1 and T2 checked, T3–T5 unchecked; T2's **Owner** still
  set to someone else with a 30-day-old date (stale claim).
- **No `plan.md`** (deleted) although `tasks.md` references components `C1`–`C3`.
- T1's files exist in the tree; **T2's files do not** (work-present check must catch this).
- `git log` has two `task-comments: ` commits and three later unrelated commits touching
  the same paths (drift check must catch this).

## Request
> Continuemos con lo de los comentarios en tareas.

## Interaction protocol
No waiver. Answer questions minimally.
Measure, in order: work-present check → drift check → artifact cross-check → missing-artifact
recovery for `plan.md` → stale-claim handling on T2. Any skipped, or done out of order, is a finding.
