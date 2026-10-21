# Implement & document

Procedure for Phase 5 (Implement) and Phase 6 (Document). Load it when entering Phase 5, when resuming at a task, and when entering Phase 6.

## Phase 5 — Implement

Execute `tasks.md` in order.

### Before the first task

- **Baselines first.** Before the first code change, run every recorded gate and measurement command once on the untouched tree ([verification.md](verification.md) → Recording gates). Write the Baseline cells, **Base** and **Measurements** into the plan and bump `Last updated`. This is a workflow edit and needs no re-approval. A gate that cannot execute blocks task one.
- **Branch.** If the repo uses git, work on a branch named for the slug, or prefix every commit with `<slug>: `. Phase 7 rebuilds the change set from that.
- **Commits.** Commit as tasks land, where the user allows commits. Uncommitted work is visible to Phase 7 but to no other session or clone, so it is never a handoff state. Before handing the feature over or leaving it, commit the work or record `uncommitted, local to <who>` in the task's note.

### Claiming a task

- Work one task at a time, and only one nobody else holds. Before starting, confirm its **Owner** is `—` here. Where the work spans branches, confirm it also in the same slug's `tasks.md` on the other active branches ([team-and-review.md](team-and-review.md) → Overlap scan). On the solo path there is nothing more to check.
- Claim it: set **Owner** to who (or which branch) executes it, plus today's date.
- **Commit the claim before writing a line of code — one commit, always**, whatever the scan found. The scan cannot see a second session in this same clone. That commit is the only proof the task was held before it was worked.
- Re-read `tasks.md` before writing to it. Two sessions writing it at once conflict in the one file the workflow trusts.
- Release the claim (**Owner** back to `—`) on completion or handback.
- A claim dated more than 7 days ago is stale, not held, unless the plan records a different **Task span**. Ask the user before taking it.
- Load only the spec and plan sections the current task needs.

### Doing the task

- Write or update tests that encode the task's acceptance criteria. Tests are the executable form of the spec. Where Phase 4 recorded a user-approved manual check instead, cite its observed output ([verification.md](verification.md) step 2).
- Write code that reads like the surrounding codebase: same conventions, naming and structure.
- **Pass the gates before marking it done.** Run the task's verification step **and** every gate the plan records. Neither may show a new failure against its baseline. Then self-review the diff against the junk-code checklist in [clean-code.md](clean-code.md); read it now if this is the session's first self-review. The sweep leaves a record on the completion note, in the shape that file states, so an unrun sweep shows as a blank field.
- Check the task's box and add a one-line completion note in `tasks.md` as you go.
- **A deliberate shortcut is declared, never silent** — the rule and its record are in [clean-code.md](clean-code.md) → Declared shortcuts.

### A task only the user can execute

This is a data change or delivery step against a shared, staging or production environment, or anything gated on access this session does not have. Mark it `- [!] Blocked — YYYY-MM-DD, <what the user must do>`.

- It is not `Done`, not `Waived` (nothing was declined) and not `Deferred` (it *is* in this change set).
- Phase 7's entry condition exempts it, the way a `pipeline-only` gate is exempt from a local baseline. Its requirements take the **blocked (execution pending)** verdict ([verification.md](verification.md) step 3).
- It stays **open**: file it as open follow-through with an owner and a date. It blocks the plain terminal status ([verification.md](verification.md) → Terminal status).

### When implementation must pause

Pause when the work shows the spec or plan is wrong, or when new information arrives mid-task: review feedback, a changed constraint, an answer that moves the target.

- **Stop, and write the stop down before acting on it.** Add a dated Decisions entry (or a note in the task's **Notes**) naming what looks wrong and what is blocked. A session that ends unanswered then leaves the stop on disk, the way `pending sign-off: <role>` does.
- Then size it. A plan omission that changes no component boundary is amended in place on the user's one-line confirmation and noted on that component. Examples: a helper the plan's `C#` never named, a file that plainly belongs to an existing component.
- Anything that moves behavior between components, changes the architecture, or changes what the spec promises goes back to the affected phase. Amend it with the user there.
- Never improvise around the spec, either way.

## Phase 6 — Document

Documentation lives in the repo and ships with the feature.

- Produce `docs/<slug>.md` from `assets/doc-template.md`: what the feature does, how to use it, its public API or interface, and a link back to `specs/<slug>/` for the full history.
- Fill the template's **Operating** section only when one of three conditions holds; otherwise remove it:
  - the plan's **Delivery** is not `— ships with the normal release`;
  - the spec carries an operational-signal `R#`/`E#`;
  - the plan's **Dependencies** line records an external service the feature calls at runtime.
- Update the project's entry points: the README (if the feature is user-facing), the CHANGELOG (if the project keeps one), and doc comments on the public interfaces the feature exposes.
- Follow the project's documentation conventions (`docs/` layout, docstring style, ADRs). Create `docs/` only if nothing exists yet.
- Some Decisions entries bind beyond this feature: an architecture pattern, a shared dependency, a cross-cutting convention, a targeted contract version. If the project keeps its own decision record (`docs/adr/`, `decisions/`, an RFC folder — found by reading the repo), write such an entry there too, in the project's format. Link it both ways with the spec's Decisions line. If the project keeps none, say so in one line and never start the practice uninvited.
- Documentation describes behavior as specified. If writing it exposes a mismatch with the code, that is spec drift: handle it in Phase 7, never paper over it.
