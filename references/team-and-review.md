# Team scale, review & integration

Rules for a feature worked by more than one human or more than one agent. Loaded at Phase 1 (the spec's **Owner**, **Sign-off**, and **Tracking** lines), Phase 3 (the plan's **Integration** line), Phase 5 (task claims and handoff), Phase 7 (integration state), and whenever review feedback arrives. Discover the project's own process by reading the repo — never propose a review, approval, or tracking practice the project does not already have. A solo developer on a repo with no policy answers every line below with its `—` default and loses nothing.

## Discovery — read, never assume

Read these before filling the spec's header and the plan's **Integration** line; name what you found, and record `— none found` where a source is absent:

- [ ] `CODEOWNERS` / `OWNERS` / equivalent — which of the paths this feature touches have named owners.
- [ ] Branch-protection or required-check configuration held in the tree (pipeline config, committed repo settings) — required approvals, required checks, who may merge.
- [ ] `CONTRIBUTING`, a review policy, or a contribution guide — how change sets are proposed, and how large they are expected to be.
- [ ] Pull/merge-request and issue templates — what the team records per change and where.
- [ ] Security, privacy, or operations docs naming a role that must approve their ground.
- [ ] Existing specs, docs, and commit messages — the identifiers they cite show where the team tracks work.

Where the repo shows nothing and the answer matters, ask the user; a guess here is a fabricated approval.

## Sign-off authority

- [ ] **Owner** is accountable for the spec's content. **Sign-off** lists, one line each, the approval-gated items this feature actually raises: spec content; each sensitive-ground `R#`/`E#` (access control, personal or regulated data, secrets, money); a new or version-changed dependency; an irreversible or data-losing data change; a delivery step against a shared, staging, or production environment; accepting a requirement as a documented limitation.
- [ ] Each line names the **role** required, as the repo names it — never a guessed person.
- [ ] `— the session's user holds all of these` is valid and common: record it explicitly, so the artifact says the authority was checked rather than assumed.
- [ ] An item whose named signer is not the person in this session is **not** approved by that person's answer: record `pending sign-off: <role>` on the spec's Status line, name the item, and do not start work gated on it. A standing waiver never covers a pending-sign-off item (core rule 2).
- [ ] The user relaying an absent signer's decision counts as that signer's answer only when the relay says so: record who decided, when, and through whom, as a dated Decisions entry.
- [ ] Clearing a pending sign-off: remove it from the Status line and record the approval as a dated Decisions entry naming the role and the item.

## Integration — how the change set reaches the base branch

- [ ] The plan's **Integration** line states: direct commits, or one or more review-gated change sets; who must approve each (from `CODEOWNERS` and branch protection, mapped to the paths this feature touches); and which checks are required there — they usually overlap the plan's `pipeline-only` gates, so say which.
- [ ] `— direct commits to the base branch, no review policy found` is a valid answer.
- [ ] Where the policy expects several change sets, say which tasks fall in each and in what order; a change set the plan does not describe is not one to invent mid-flight.
- [ ] Pushing, opening, or merging a change set acts on shared ground: it is the user's step unless they say otherwise, exactly like a delivery step. The agent prepares it (branch, commits, a description built from the spec) and hands it over.
- [ ] Phase 7 reports the state on the report's `Integration:` line: `merged` — `git merge-base --is-ancestor HEAD <the branch the plan's Base names>` succeeds — with the required approvals cited; or `pending review (<identifier>)`; or `not opened yet`. Pending never blocks the report; it blocks only the **implemented** status.
- [ ] Record the identifier the review got (number, URL, or whatever the project uses) on a Decisions line, so a later session can find the discussion.
- [ ] Any edit to the change set after a converged Phase 7 pass — review fixes included — makes that pass's report describe a tree that no longer exists: run Phase 7 again before the terminal status.

## Review feedback

Classify every comment before acting on it:

- [ ] **Behavior feedback** — it changes what the system does, accepts, or guarantees (a limit, a default, a removed capability, an error case, an access or data rule). It is a change request whoever relays it: amend `spec.md` first — new or changed `R#`/`E#` plus a Decisions entry naming the reviewer and the review identifier — then `plan.md`/`tasks.md`, then code. Edit the diff first and Phase 7 reports the reviewer's own decision as spec drift.
- [ ] **Plan feedback** — it rejects an approach, a component's placement, a dependency, or a reuse choice: back to Phase 3, amend `plan.md`, re-approve. Not a code edit.
- [ ] **Implementation feedback** — naming, structure, tests, style, anything the spec does not state: ordinary Phase 5 work; a Decisions entry only where it settles something binding beyond this feature.
- [ ] A declined comment is still recorded: a Decisions entry saying what was declined and why, with the review identifier.
- [ ] Feedback arriving after the spec was set **implemented** resets it through the normal amendment path (SKILL.md → Change requests mid-flight).

## Parallel sessions on one feature

- [ ] Two agents on one `tasks.md` collide unless tasks are claimed: **Owner** on the task, set before any code, committed, released to `—` on completion or handback.
- [ ] Before claiming, and where the feature's work spans branches, check the same slug's `tasks.md` on the other active branches (enumerated as in Phase 3's overlap scan) — an unchecked task there may already be held.
- [ ] A claim older than the project's normal task span is stale, not held: ask the user before taking it, and say so in the task's note.
- [ ] Two sessions writing `tasks.md` at once conflict in the one file the workflow trusts: commit claims and completion notes promptly, and re-read `tasks.md` before writing to it.

## Handoff

- [ ] A checked task is evidence only when its work is present in the tree reading it: its **Files** exist and its `Verify:` passes. Confirm this before resuming someone else's feature.
- [ ] Every completion note names where the work landed — the commit(s) carrying it, or `uncommitted, local to <who>`. Uncommitted work is invisible to every other clone, so it is never a handoff state.
- [ ] A checked task whose work is absent here is recovered from the branch or clone that holds it, or reopened (`- [x] Done` → `- [ ] Done`, with a note naming where it was last seen). Never file a `G#` to re-implement a teammate's work before this check has run.
- [ ] Handing a feature over: release every claim, commit or explicitly record every piece of work, and leave each artifact's Status and `Last updated` current.

## Open follow-through

Obligations this workflow creates that outlive the feature — a flag retirement, the cleanup half of a data change, a provider's end-of-support move, a rollout's remaining stages, a pending `SC#`, a requirement deferred out of this change set, the proper version of a deliberate shortcut declared in Phase 5:

- [ ] Each is a dated Decisions entry naming when it lands and who owns it, **and** is filed where the spec's **Tracking** line says the team's open work lives; the identifier it got back goes on that Decisions line.
- [ ] Where the project tracks work in the repo only, the follow-up also stays in `tasks.md` as `- [>] Deferred — YYYY-MM-DD, owner <who>` — a Decisions line alone is a comment no resume will ever surface. A deferred task is closed for this feature's convergence and never counts as unchecked.
- [ ] Resuming work lists an **implemented** feature whose Decisions hold an open follow-up, or whose `tasks.md` holds a `- [>] Deferred` entry, alongside the in-flight features.
- [ ] A follow-up whose named owner has left the team is unowned: report it to the user for reassignment instead of leaving the name in place.
