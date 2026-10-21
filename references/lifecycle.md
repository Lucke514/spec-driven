# Change requests & resuming

Rules for a feature whose target changes after approval, and for picking a feature up in a new session. Load Change requests mid-flight when new or different behavior is asked for after the proposal is approved. Load Resuming work when a session starts on an existing feature.

## Change requests mid-flight

New or different behavior asked for after approval enters through the spec, not the code. That holds whether it comes from the user, or from a code reviewer or any third party whose feedback the user relays. The one-line test: if the diff you are about to write isn't covered by the current spec, stop and amend the spec first.

- **Order.** Amend `spec.md` first: the new or changed `R#`/`E#`, plus a Decisions entry recording what changed and why. Then update `plan.md` and `tasks.md` if the change touches them. Then implement.
- **Review feedback.** Behavior feedback from a code review is a change request like any other, whoever relays it. It lands in `spec.md` first, never straight in the diff; otherwise Phase 7 reports the reviewer's own decision as spec drift. Read [team-and-review.md](team-and-review.md) → Review feedback now and classify each comment before acting on it.
- **Large split.** If the change adds a capability, removes one, or moves behavior between capabilities, update `specs/<parent-slug>/scope.md` first, with the user's approval: the capability row, its depends-on and its status. Then amend the affected capability's `spec.md` as usual.
- A clarification that changes no requirement needs only a Decisions entry.
- If the change invalidates completed tasks, list them and get approval before redoing them.
- **Status reset.** Every artifact the amendment touches goes to `in-review` and stays there until sign-off, whatever Status it held. That includes `plan.md` and `tasks.md`: one left `approved` while its content is under revision claims a stop that did not happen. An **implemented** spec and its plan reset the same way. They return to `approved` on the user's sign-off, and to `implemented` once the new `R#`/`E#` pass Phase 7.
- **Wholesale replacement.** If the change replaces the feature's behavior wholesale, write a new spec and mark the old one **superseded** instead of reopening it.
- **Partial replacement of another feature.** If it replaces part of what *another* feature's spec still claims, amend that spec in the same approval: a Decisions entry, plus `— superseded by specs/<successor-slug>/spec.md` on each affected `R#`/`E#`. Supersede the whole artifact only when nothing in it stays live. The annotation is records-only. It does not reset an **implemented** Status; only adding or changing a live `R#`/`E#` does. Phase 7 reports each annotated requirement as **superseded** rather than re-verifying it.
- **Cancellation, at any phase.** Set the artifacts' Status to **abandoned** with a Decisions entry saying why. Never delete the directory.
  - Propose reverting whatever change set already landed, built the same way as the step-6 inventory in [verification.md](verification.md), unless the user explicitly keeps parts. Record what was kept or reverted in that entry.
  - Mark any existing `docs/<slug>.md` **deprecated**.
  - Every reverted task's `- [x] Done` goes back to `- [ ] Done`, with a note naming the revert. Task state must never claim code the tree no longer has.
  - For a capability of a Large split, set its `scope.md` row to **abandoned**. In the same approval, resolve every capability that depends on it: re-point, absorb, or abandon it too.

## Resuming work

### Which feature

- **None named:** resume the one matching the current branch or the most recent `<slug>: ` commits.
- **Named loosely** ("carry on with the bulk actions thing"): if exactly one open-work spec matches, resume it directly and say which. List the others only when the match is not unique.
- **Otherwise:** read only the header block of each `specs/*/spec.md`, list the open work, and ask which one. Open work is:
  - a Status of `draft`, `in-review` or `approved`;
  - an **implemented** spec whose Status line records a rollout still in progress;
  - an **implemented** spec whose Decisions hold an open dated follow-up of any kind ([team-and-review.md](team-and-review.md) → Open follow-through);
  - an **implemented** spec whose `tasks.md` holds a `- [>] Deferred` or `- [!] Blocked` entry.
- Skip `implemented` with none of those, `superseded` and `abandoned`. A directory holding `scope.md` and no `spec.md` is a Large parent: see Large split below.

### Which task

Read the chosen feature's artifacts in order. If `specs/<slug>/` is absent here, the missing-artifact check below rules the branch case out first.

Then take the first unchecked task no one else holds: **Owner** is `—` ([implement.md](implement.md) → Claiming a task). `- [~] Waived` is closed. `- [>] Deferred` is not due until its date. `- [!] Blocked` waits on the user, not on you.

Name the task to the user before claiming it: state the task and what it will change. That turn is their chance to redirect; proceeding after it is not silence. A feature-level "continue" is not that naming.

### Checks, in order

One dependency: the drift check may order a diagnostic pass that needs a missing artifact. Then recover the artifact under the missing-artifact check **first**. Or run the pass in reduced form and say in the report which gates and which **Base** it could not read.

- **Work-present check** — run it before anything else. Confirm each checked task's work is actually in *this* tree: its **Files** exist and its `Verify:` passes.
  - A checked task whose work is absent here was never handed over. Recover it from the branch or clone the task's note names, or reopen it (`- [x] Done` → `- [ ] Done`, with a note saying where it was last seen).
  - Reopening never releases the claim. **Owner** is cleared only by its owner or by the user's answer: two actions, with the ask in between.
  - Never trust the checkbox alone. Never file a `G#` to re-implement a teammate's work before this check has run.
  - A claim naming this session's own branch or user, on an unchecked task with no completion note, is a crashed claim, not a held one. Re-run that task's `Verify:` and check its **Files**, then continue it or reopen it. Never wait out its 7 days.
- **Drift check** — did code change *outside* this feature since the artifacts were written? Compare each artifact's `Last updated` against `git log` for the paths the feature touches.
  - Discount the feature's own work: commits on its branch, commits carrying the slug prefix, and the working tree its last completed task left behind. They are never drift.
  - If anything else is newer, run Phase 7 as a diagnostic pass.
  - Dates also mislead after a rebase or a merge from the base branch. Run the rebase test on the plan's **Base** line, in the form that line's topology takes ([verification.md](verification.md) → Recording gates). Where it fires, treat the code as changed regardless of dates and run that pass. Its step 4 refreshes the stale baseline.
- **Artifact cross-check** — run `scripts/validate.py`. An error about a missing or unknown id is a mismatch; fix any other error in place.
  - Then check each artifact against its own history. The workflow's own edits are legitimate in an `approved`/`implemented` artifact: checkboxes, completion notes, amendments, Status changes, appended reports and `Last updated` bumps. They are committed on the feature's branch, under its `<slug>: ` prefix, or still uncommitted from its last completed task.
  - A mismatch is an edit outside that set. Either a commit touching the artifact, newer than its `Last updated` line, and neither on the feature's branch nor `<slug>: `-prefixed. Check with `git log -1 --format=%as -- <artifact>`: the author date, which a rebase preserves where committer dates do not. Or an uncommitted change (`git diff -- <artifact>`) rewriting an `R#`/`E#`, its criteria, or the plan's components.
  - A mismatch means the artifact was hand-edited. Treat it as an unprocessed change request and run Change requests mid-flight first.
  - An artifact the depth never produces (no `plan.md` at Small) is never a mismatch. One the depth should have produced but that is absent is the next check's case.
- **Missing or unrecoverable artifacts** — rule out the branch case first. If a branch named `<slug>`, or another active branch (run the overlap scan), holds `specs/<slug>/`, nothing was lost. Switch to that branch to resume it, or ask the user. Never restore copies into the current branch.
  - Otherwise, an artifact the lifecycle already produced may be missing or unreadable. It was produced if its upstream artifact is `approved` or `implemented`, or a downstream artifact references it. Restore it from git history.
  - If it is unrecoverable, regenerate it from the surviving artifacts (`tasks.md` from the plan's components). Leave every regenerated task unchecked. Record the reconstruction as a Decisions entry in `spec.md` and get it re-approved.
  - Then run Phase 7 immediately as a diagnostic pass. Its **met** verdicts, not memory of earlier sessions, decide which regenerated tasks are already done.
- **Stopped at an earlier phase** — resume at that phase's exit; never re-specify from scratch. A spec with no plan resumes at Phase 2, or Phase 3 once no markers remain. A later `draft` or `in-review` artifact is completed and presented as the proposal. An approved plan with unfilled Baseline cells resumes at [implement.md](implement.md) → Baselines first.
- **Every task closed, Status still `approved`** — read the `Verification reports` section of `tasks.md` (Small: the end of the collapsed `spec.md`'s `## Tasks` section). Phase 7 never converged if there is no report block, if its `Converged:` line reads `no`, or if the last pass still lists open gaps or verdicts other than **met**, **superseded**, **deferred**, **blocked** or an accepted limitation. Run it then. An in-progress block names the step it stopped at; restart there. Never set **implemented** without a converged report block on record.

### Special cases

- **Large split** — read `specs/<parent-slug>/scope.md` first. Pick the next capability whose dependencies are `done`.
  - Where several qualify, take the one the approved **rank** names first and report that choice; never pick silently. A different order is a re-rank of those rows, with the user's approval.
  - A `deferred` row is not a candidate until its date. Report it alongside the in-flight rows, so a cut capability stays visible.
  - If none qualifies, report the blocking rows instead of stopping. An `abandoned` dependency is a scope decision (re-point, absorb, or abandon the dependent), never a permanent block.
- **Abandoned** — skip it unless the user explicitly reopens it. Reopening sets `spec.md`, `plan.md` and `tasks.md` back to `in-review`, and the normal lifecycle re-applies. After re-approval, run Phase 7 immediately as a diagnostic pass. Its **met** verdicts, not checkboxes left behind before the cancellation, decide which tasks are still done and where Phase 5 restarts.
