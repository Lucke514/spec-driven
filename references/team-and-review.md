# Team scale, review & integration

Rules for a feature worked by more than one human or more than one agent. Loaded at Phase 1 (Team signals, then Discovery where a signal fires), Phase 3 (overlap scan, **Integration** line), Phase 5 (task claims, open follow-through), Phase 7 (integration state), and whenever review feedback arrives. Discover the project's own process by reading the repo — never propose a review, approval, or tracking practice the project does not already have. A solo developer on a repo with no policy answers every line below with its `—` default and loses nothing.

## Team signals — check first

Run once per session at Phase 1, and reuse the result:

1. **Team files** — `CODEOWNERS`/`OWNERS`, `CONTRIBUTING`, or pull/merge-request or issue templates: `find . -maxdepth 3 -not -path '*/node_modules/*' \( -iname CODEOWNERS -o -iname OWNERS -o -iname 'CONTRIBUTING*' -o -iname '*request_template*' -o -iname ISSUE_TEMPLATE \)`.
2. **Other branches** — the overlap scan's step 2 command below returns a row from the last ~90 days.

**Neither fires** — the solo path: skip Discovery and the overlap scan's branch steps. **Owner**, **Sign-off**, and **Tracking** take `— the session's user holds all of these` and `— this project tracks work in the repo only`. The overlap result is `— single branch, no team signals`. Core rule 2 is unchanged: every item it gates still gets the user's explicit sign-off.

**A signal fires** — run only what it calls for. A team file → Discovery. A recent unmerged branch → the full overlap scan. The user saying others work on this, or a signal appearing later, triggers both.

## Discovery — read, never assume

Where Team signals calls for it, read these before filling the spec's header and the plan's **Integration** line; name what you found, and record `— none found` where a source is absent:

- [ ] `CODEOWNERS` / `OWNERS` / equivalent — which of the paths this feature touches have named owners.
- [ ] Branch-protection or required-check configuration held in the tree (pipeline config, committed repo settings) — required approvals, required checks, who may merge. Most hosts keep this outside the tree, so `— none found` proves nothing. Never call an approval or check *required* from a `CODEOWNERS` entry alone: record `— claimed by CODEOWNERS, enforcement not confirmable from the tree`, or ask the user and record their answer.
- [ ] `CONTRIBUTING`, a review policy, or a contribution guide — how change sets are proposed, and how large they are expected to be.
- [ ] Pull/merge-request and issue templates — what the team records per change and where.
- [ ] Security, privacy, or operations docs naming a role that must approve their ground.
- [ ] Existing specs, docs, and commit messages — the identifiers they cite show where the team tracks work.

Where the repo shows nothing and the answer matters, ask the user; a guess here is a fabricated approval.

**Routing what an owner owns** — ownership of a **path** this change touches goes on the plan's **Integration** line (who approves the change set). Ownership tied to one of the gated **items** in [sign-off.md](sign-off.md) goes on the spec's **Sign-off** line (who approves the decision), even where no path of that owner is touched. Both, when both are true.

## Overlap scan

The bounded enumeration of what else is in flight outside this working tree, used by the slug test, Phases 3, 5 and 7, and [lifecycle.md](lifecycle.md) → Resuming work. On the solo path (Team signals above) it is step 1 only, recorded as `— single branch, no team signals`. Run it once per session and reuse the result — with one exception: Phase 5's per-task claim check exists for freshness. Reuse the branch set there, but re-read the other branches' `tasks.md` (step 3) at each claim, because a claim can land after the scan ran.

1. **This tree** — every `specs/*/` in the repo; in a monorepo, each package's `specs/`, not just this one's.
2. **The other active branches**, bounded and newest first — those holding commits not yet merged here:

   ```
   git for-each-ref --sort=-committerdate --count=15 \
     --format='%(committerdate:short) %(refname:short)' \
     --no-merged HEAD refs/heads refs/remotes
   ```

   Keep the rows whose printed date falls within the last ~90 days — compare that date, never the branch name, and stop at the first row older than the cut. `--count=15` is the bound: if 15 rows survive the date filter, more branches may qualify — list the 15, tell the user the scan is bounded to the 15 most recent, and record that bound with the branch set.
3. **Read what they hold** — `git ls-tree -r --name-only <branch> | grep -E '(^|/)specs/'` for each surviving branch, then `git show <branch>:<path>` to read the artifacts it lists.
4. **Where branches cannot be enumerated at all**, ask the user which other features are in flight.
5. **Record the result** — the branch set scanned, or the user's answer, or the bound the scan hit — on the plan's **In flight** line (at Small, next to the tasks in the collapsed `spec.md`). An empty scan means "none", never "not visible".

## Sign-off authority

- [ ] **Owner** is accountable for the spec's content. **Sign-off** carries one line per row of [sign-off.md](sign-off.md)'s table that this feature actually raises — that table is the list, and this file keeps no second copy of it.
- [ ] Each line names the **role** required, as the repo names it — never a guessed person.
- [ ] `— the session's user holds all of these` is valid and common: record it explicitly, so the artifact says the authority was checked rather than assumed.
- [ ] An item whose named signer is not the person in this session is **not** approved by that person's answer: record `pending sign-off: <role>` on the spec's Status line, name the item, and do not start work gated on it.
- [ ] The user relaying an absent signer's decision counts as that signer's answer only when the relay says so: record who decided, when, and through whom, as a dated Decisions entry.
- [ ] Clearing a pending sign-off: remove it from the Status line and record the approval as a dated Decisions entry naming the role and the item.

## Integration — how the change set reaches the base branch

- [ ] The plan's **Integration** line states: direct commits, or one or more review-gated change sets; who must approve each (from `CODEOWNERS` and branch protection, mapped to the paths this feature touches, routed and confirmed as Discovery says); and which checks are required there — they usually overlap the plan's `pipeline-only` gates, so say which.
- [ ] `— direct commits to the base branch, no review policy found` is a valid answer.
- [ ] Where the policy expects several change sets, say which tasks fall in each and in what order; a change set the plan does not describe is not one to invent mid-flight.
- [ ] Pushing, opening, or merging a change set acts on shared ground: it is the user's step unless they say otherwise, exactly like a delivery step. The agent prepares it (branch, commits, a description built from the spec) and hands it over.
- [ ] Phase 7 reports the state on the report's `Integration:` line: `merged` — `git merge-base --is-ancestor HEAD <the branch the plan's Base names>` succeeds — with the required approvals cited; or `pending review (<identifier>)`; or `not opened yet`. Pending never blocks the report; it blocks only the **implemented** status.
- [ ] Record the identifier the review got (number, URL, or whatever the project uses) on a Decisions line, so a later session can find the discussion.
- [ ] Any edit to the change set after a converged Phase 7 pass — review fixes included — makes that pass's report describe a tree that no longer exists: run Phase 7 again before the terminal status.

## Review feedback

Classify every comment before acting on it:

- [ ] **Reconcile Integration against the review's identifier first.** Where the feedback names a change set (a PR or MR number, a review URL) that the plan's **Integration** line does not record — it still reads `— direct commits to the base branch`, or names a different change set — reconcile that line now: update it, or flag the mismatch to the user, before filing any Decisions entry.
- [ ] **Behavior feedback** — it changes what the system does, accepts, or guarantees (a limit, a default, a removed capability, an error case, an access or data rule). It is a change request whoever relays it: amend `spec.md` first — new or changed `R#`/`E#` plus a Decisions entry naming the reviewer and the review identifier — then `plan.md`/`tasks.md`, then code. Edit the diff first and Phase 7 reports the reviewer's own decision as spec drift.
- [ ] **Plan feedback** — it rejects an approach, a component's placement, a dependency, or a reuse choice: back to Phase 3, amend `plan.md`, re-approve. Not a code edit.
- [ ] **Implementation feedback** — naming, structure, tests, style, anything the spec does not state: ordinary Phase 5 work; a Decisions entry only where it settles something binding beyond this feature.
- [ ] A declined comment is still recorded: a Decisions entry saying what was declined and why, with the review identifier.
- [ ] Feedback arriving after the spec was set **implemented** resets it through the normal amendment path ([lifecycle.md](lifecycle.md) → Change requests mid-flight).

## Open follow-through

Obligations this workflow creates that outlive the feature — a flag retirement, the cleanup half of a data change, a provider's end-of-support move, a rollout's remaining stages, a pending `SC#`, a requirement deferred out of this change set, the proper version of a deliberate shortcut declared in Phase 5:

- [ ] Each is a dated Decisions entry naming when it lands and who owns it, **and** is filed where the spec's **Tracking** line says the team's open work lives; the identifier it got back goes on that Decisions line.
- [ ] **When the user names neither** ("later, don't touch it now"), the owner defaults to the spec's **Owner** and the date to the project's next release or review point, both recorded as defaults (`owner <who> (default — spec Owner), YYYY-MM-DD (default — next release)`). Where the project has no such point, record `unowned — revisit at <trigger>` naming the event that brings it back (the flag's first production use, the provider's end-of-support date, the next change to this area). An unowned entry is reported to the user for an owner the next time Resuming work surfaces it.
- [ ] Where the project tracks work in the repo only, the follow-up also stays in `tasks.md` as `- [>] Deferred — YYYY-MM-DD, owner <who>` — a Decisions line alone is a comment no resume will ever surface. A deferred task is closed for this feature's convergence and never counts as unchecked.
- [ ] Resuming work lists an **implemented** feature whose Decisions hold an open follow-up, or whose `tasks.md` holds a `- [>] Deferred` entry, alongside the in-flight features.
- [ ] A follow-up whose named owner has left the team is unowned: report it to the user for reassignment instead of leaving the name in place.
