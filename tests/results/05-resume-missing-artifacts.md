# Scorecard — 05-resume-missing-artifacts

- **Scenario**: [scenarios/05-resume-missing-artifacts.md](../scenarios/05-resume-missing-artifacts.md) — resuming an in-flight feature with a deleted `plan.md`, a falsely-checked task with absent work, a stale claim, and real drift (Standard depth, pre-existing)
- **Iteration**: 5
- **Date**: 2026-08-26
- **Model**: Claude Sonnet 5 (`claude-sonnet-5`)
- **Skill version**: `metadata.version: "2.2.0"` (SKILL.md, as read at test time). Note: the skill
  repo's working tree was under active, concurrent modification by another session while this
  test ran (`git diff` on `SKILL.md`/`references/*`/`assets/*`/`CHANGELOG.md` showed uncommitted
  changes from `2.0.0` → `2.2.0` appear mid-session, not caused by this run). This scorecard
  reflects the `2.2.0` text as read; none of those files were touched by this run.
- **Run**: [tests/runs/05-resume-missing-artifacts/](../runs/05-resume-missing-artifacts/) —
  see `specs/task-comments/{spec,plan,tasks}.md`, `docs/task-comments.md`, branch `main`
  (slug-prefixed commits, no dedicated feature branch — the fixture's other convention)

**Fixture construction (disclosed):** built by copying `tests/runs/02-express-crud-api/`
(`tasks-crud` branch renamed `main`, all prior commit dates rewritten to a coherent June 2026
timeline so they chronologically precede this feature), then staging a real git history for
`task-comments`: two `task-comments:`-prefixed commits (T1 done with its file present; T2
falsely checked done by "Jordan Lee" 2026-07-27 with neither of its files ever committed
anywhere), then three later non-prefixed commits by other authors — two touching code this
feature reuses (`src/middleware/validate.ts`, `src/app.ts`) and one deleting `plan.md`
outright. Dates: `spec.md`/`tasks.md` `Last updated: 2026-08-06` (20 days before eval date
2026-08-26); T2's `Owner` claim dated `2026-07-27` (30 days before). All fixture-construction
commits and all resume/implementation commits are real, dated commits in the nested repo
(never the outer skill repo).

## Scores

| # | Dimension | Score /5 | Justification |
|---|---|---|---|
| D1 | Depth call | 2 | The pre-existing artifacts are unambiguously Standard depth (separate `plan.md`, a `Component` field on every task) and I read and used that correctly throughout — but I never stated the depth as a one-line declaration anywhere in the resume flow, the way SKILL.md → Adaptive depth requires "before starting" a fresh feature. Resuming work never restates or re-confirms the operative depth, and nothing in Resuming work told me to say it — so it just never got said. |
| D2 | Phase discipline | 3 | The 5 resume checks ran in the scenario's exact required order (see table below), and Phase 5→6→7 followed correctly after. Docked for two real ordering problems, one caused by the skill text and one by me: (a) the drift check's own mandate — "run Phase 7 first" — could not literally run first, because Phase 7 needs `plan.md` (Quality gates, Base line) and `plan.md` was still missing at that point; the five bullets read as a fixed sequence but two of them have a real data dependency the text never flags. (b) I cleared T2's stale `Owner` field during the work-present check, before the stale-claim step or the user's confirmation — jumping two steps ahead. I caught and reverted this myself, but a less careful run would have silently skipped "ask the user before taking it." |
| D3 | Artifact fidelity | 4 | Templates followed throughout; Status/Owner/Sign-off/Tracking/Last updated all filled and kept current across every edit. Docked for a real, if self-caught, miss: adding **E4** (a sensitive-ground authentication edge case) at Phase 7 without updating the spec's **Sign-off** line to add an "authentication (E4)" row — the exact pattern `tasks-crud`'s own spec already established in this same repo. I only noticed and fixed it while writing this scorecard, well after the commit that added E4. |
| D4 | Testable requirements | 5 | Every `R#`/`E#` (including the Phase-7-discovered E4) is a yes/no Given/When/Then; `Minimum shippable` names R1, R2, R4 as the load-bearing set and correctly excludes R3 (deletion) as valuable-but-not-essential. |
| D5 | Traceability | 4 | Final state has a complete, bidirectional `R#`/`E#` → `C#` → `T#` chain, including E4 threaded through `plan.md`'s coverage table and both T3/T4's `Implements` lines. Docked because this was not the state after T3/T4 were first marked done — E4 didn't exist yet at that point (spec.md never had it until Phase 7's code-to-spec sweep found `requireAuth` wired with no requirement describing its negative case), so the chain was silently incomplete for several commits before Phase 7 caught it. |
| D6 | Gate discovery | 4 | Real commands recovered from the restored `plan.md`, correctly re-validated against the untouched tree at resume (gates still clean, baseline unchanged) rather than trusted blindly. Docked: `verification.md`'s rebase-detection check (`git merge-base HEAD <Base branch>` vs the recorded Base SHA) is written for a feature with its own dedicated branch; this fixture uses Phase 5's other sanctioned convention (slug-prefixed commits directly on the shared branch), where `HEAD` and `<Base branch>` are the same ref and the check is structurally degenerate. Nothing in the skill flags that this specific check doesn't generalize to the convention the skill itself offers as an alternative. |
| D7 | Code quality | 4 | Clean diff matching the fixture's conventions (mirrors `tasks-crud`'s factory/repository shape exactly); every gate actually executed at every task; the `catchAsync` duplication was correctly avoided by extraction (a live second-use case, not speculative) instead of copy-pasted. Docked for a real bug I introduced and initially missed: two tests in `test/comments.test.ts` were tagged with the wrong edge-case ID (`(E1)` on a datastore-failure test that is actually `E2`; `(E2)` on a test that isn't a defined edge case at all). This should have been caught at T3's own self-review (Phase 5: "self-review the diff against the junk-code checklist") but wasn't — it surfaced only during the later Phase 7 sweep. `clean-code.md`'s checklist has no item asking whether a test's cited `R#`/`E#` tag is actually correct, so nothing during the mandated self-review was actually pointed at this class of mistake. |
| D8 | Review stops | 4 | Stopped for real approval-shaped moments throughout (plan.md's post-recovery re-presentation, T2's stale-claim takeover, the sensitive-ground E4 addition) with no waiver in effect, matching the "no waiver" protocol. Docked for a judgment call I'm not confident the skill actually license: mid-T3 I found `plan.md`'s C3 component under-specified a needed repository function (`getTask`) and treated it as a small bookkeeping amendment (a quick confirmation, then continued) rather than the full stop-and-return-to-Phase-3 cycle Phase 5's rule literally describes for "the plan is wrong" ("a standing waiver does not cover this"). The rule doesn't scale its own ceremony to the size of the defect — a missing one-line helper function and a wrong architecture get the identical instruction — so an agent has to invent its own proportionality threshold, and mine may have been too lax. |
| D9 | Documentation | 5 | `docs/task-comments.md` accurate against the code; its runnable example was actually executed (`201` with the real response body) before being pasted in; the raw-HTTP example is clearly marked illustrative; README's Structure section updated for the new `src/lib/` and the extended `src/routes/`/`src/db/` entries; absent `CHANGELOG.md` correctly left uninvented. |
| D10 | Verification | 5 | Two real Phase 7 passes: a diagnostic pass on resume (correctly filed zero `G#`s since every `not met` verdict was already covered by an unchecked task, per `verification.md` → Handling gaps) and a full convergence pass with every `R#`/`E#` (through E4) verified against real code and a passing test, gates re-run and diffed against the restored baseline, a real dead-code-sweep inventory built from the slug-prefixed commit set (correctly excluding the three drift commits), and the terminal status correctly left `approved` rather than `implemented` because Integration is `not opened yet` — matching the exact precedent `tasks-crud`'s own report set in this repo. |
| D11 | Scope fidelity | 5 | The diff is exactly the spec's `R#`/`E#` (through the two legitimate Phase-5/7 discoveries, both declared as dated Decisions entries) plus nothing else; the drift commits' unrelated changes (`x-powered-by`, array-rejection) were reviewed for compatibility but correctly never absorbed into this feature's own change set or commits. |
| D12 | Cost | 4 | No re-reading of `SKILL.md` itself (read once). `team-and-review.md` and `verification.md` were read essentially in full, but both loads were genuinely trigger-justified by this specific scenario (Resuming work's own text names both as required reading for a drifted resume) rather than a blanket upfront batch — `writing-specs.md`, `clean-code.md`, `data-and-delivery.md`, and `dependencies.md` were never opened at all, since nothing in this run needed them. Docked one point because this run's tester and agent roles share one session and context window (the same structural confound run 01/02 flagged), so "no gratuitous re-reads" is not fully separable from "the tester already had this material in context for other reasons." |

**Total: 49/60**

## Resume checks: what actually ran

| # | Check | Ran? | Order | What it cost |
|---|---|---|---|---|
| 1 | Work-present check | Ran | 1st (correct) | `git log --all` over both of T2's Files paths (empty everywhere) plus the overlap scan (`billing-export`, unrelated) — cheap, conclusive. Cost: I also cleared T2's `Owner` field here, prematurely — see D2, self-corrected before committing forward. |
| 2 | Drift check | Ran | 2nd (correct) | `git log --since=<Last updated> -- <path>` per path inferred from the surviving `tasks.md` (plan.md's own coverage table wasn't available yet). Found 3 non-prefixed commits. Correctly triggered "run Phase 7 first," but that pass could not actually execute yet — see D2's bootstrapping finding. |
| 3 | Artifact cross-check | Ran | 3rd (correct) | Bidirectional `R#`/`E#` ↔ task `Implements` check on the two surviving artifacts (clean); `spec.md`/`tasks.md`'s own last-touching commit confirmed exactly at their `Last updated` date and slug-prefixed (no unprocessed hand-edit). `plan.md`'s coverage table deferred to the next bullet, per that bullet's own carve-out. |
| 4 | Missing-artifact recovery (`plan.md`) | Ran | 4th (correct) | Ruled out the branch case (only `billing-export`, unrelated) in one command; found `plan.md` added in `48ff9b9` and deleted whole by `35a59cd` with no edits between, so a byte-for-byte `git show` restore was possible (not the lossy regenerate path). Re-presented for confirmation before treating it as approved again — the rule's exact wording ("get the regenerated artifact re-approved... run Phase 7 immediately") reads as scoped to the regenerate branch, so applying it to a restore anyway was a judgment call, not a clearly mandated one. |
| 5 | Stale-claim handling (T2) | Ran | 5th (correct) — but its *execution* (clearing/re-claiming Owner) happened twice: once prematurely during step 1 (reverted), once correctly here, after confirming `plan.md`'s Base line held no different task span and asking the user before taking a >7-day-old claim | Cheap once sequenced correctly: one text check (no span override in `plan.md`), one confirmation, one commit. |

## Friction log

### 1. Where: SKILL.md → Adaptive depth ("State the chosen depth in one line before starting") vs. → Resuming work (no mention of depth at all)

- **What went wrong**: Resuming an existing Standard-depth feature, I never stated the depth anywhere — there is no equivalent instruction in Resuming work telling an agent to confirm or restate it, unlike Phase 1's explicit "before starting" requirement for new work.
- **Why**: "Before starting" reads naturally as "before Phase 1," and Resuming work is a different entry point that the Adaptive depth section doesn't visibly cover. An agent following Resuming work literally has no textual prompt to ever say the depth out loud.
- **Fix shape**: Add one line to Resuming work: "state the resumed feature's depth (read from its existing artifacts) in the same one-line form Phase 1 uses, before triaging it."

### 2. Where: SKILL.md → Resuming work — drift check ("if anything else is newer, run Phase 7 first as a diagnostic pass") vs. → Missing or unrecoverable artifacts (restoring `plan.md`)

- **What went wrong**: The drift check told me to run Phase 7 "first" (before Phase 5 resumes), but Phase 7 needs `plan.md` (its Quality gates table, its Base line) to run at all, and `plan.md` was exactly the artifact missing. The five Resuming-work bullets read like a fixed checklist in order, but two of them have a real dependency the text never states: the diagnostic Phase 7 pass the drift check demands cannot execute until the missing-artifact bullet — three positions later in the same list — has already restored the file it needs.
- **Why**: Each bullet is written as if it resolves independently; nothing says "step 5's prerequisite may be step 2's output," so an agent following the list top-to-bottom hits a wall exactly where I did — forced to read ahead and reorder mid-flight rather than following a rule that already told it to.
- **Fix shape**: Add a note to the drift check bullet: "if a diagnostic Phase 7 pass is triggered and an artifact it needs is itself missing, restore or regenerate that artifact (next bullet) first, then run the pass."

### 3. Where: my own execution — `references/team-and-review.md` → Handoff (reopening a checked task) vs. → Parallel sessions ("ask the user before taking" a stale claim)

- **What went wrong**: While reopening T2 (work-present check), I also cleared its stale `Owner` field in the same edit — before asking the user, and before the stale-claim step the scenario measures separately. I caught this and reverted the `Owner` clear before committing, leaving the checkbox reopened but the claim untouched until the dedicated stale-claim step ran later.
- **Why**: Handoff's reopen instruction (`- [x] Done` → `- [ ] Done`, with a note) and Phase 5/Parallel-sessions' claim-release instruction touch the same task at the same moment, and nothing states that they are two separate actions with a required gap between them (ask, then act) — a natural reading bundles them into one "fix the task" edit.
- **Fix shape**: Add a clause to Handoff's reopen instruction: "reopening a task does not by itself resolve its `Owner` field — a stale or held claim is still governed by Phase 5's claim rule and is asked about separately."

### 4. Where: SKILL.md core rule 2's table, row "A sensitive-ground `R#`/`E#`" → "Recorded as: the approval as a dated Decisions entry in `spec.md`"

- **What went wrong**: I added E4 (an authentication edge case) with a proper dated Decisions entry, exactly as that row says — but never updated the spec's own **Sign-off** header line to add an "authentication (E4)" row, even though this exact repo's sibling feature (`tasks-crud`'s spec) already establishes that convention for the same table row (its Sign-off line reads "access control (R5, R6, E3) — the session's user holds all of these"). I only caught the omission while writing this scorecard.
- **Why**: The table's "Recorded as" column names only the Decisions entry, not the Sign-off-line update — the Sign-off-line convention is only discoverable by finding and reading a sibling feature's spec, not from the rule text itself.
- **Fix shape**: Extend the "Recorded as" cell for that row: "a dated Decisions entry in `spec.md`, and a matching row on the spec's Sign-off line naming the `R#`/`E#` it covers."

### 5. Where: `references/verification.md` step 4's rebase-detection check (`git merge-base HEAD <Base branch>` against the recorded Base SHA) vs. SKILL.md Phase 5's slug-prefix-on-shared-branch convention

- **What went wrong**: This fixture's feature has no dedicated branch — its commits carry the `task-comments:` prefix directly on the shared branch, exactly as Phase 5 permits ("or its commits are slug-prefixed"). Under that convention, `HEAD` and the Base branch are the same ref, so `git merge-base HEAD <Base branch>` trivially returns `HEAD` itself and can never usefully detect a rebase — the check is structurally degenerate for the exact alternative the skill itself sanctions.
- **Why**: The rebase-detection check is written assuming a feature-owns-a-branch topology; the skill offers a second topology (shared branch, prefixed commits) without ever revisiting whether every downstream check written for the first topology still means anything under the second.
- **Fix shape**: Add a line to `verification.md`'s rebase-detection check: "on a shared branch with slug-prefixed commits, this check is not meaningful (`HEAD` and Base are the same ref) — rely on the artifact cross-check's own hand-edit detection instead."

### 6. Where: `references/clean-code.md`'s checklist (Phase 5's mandated pre-done self-review) — has no item for requirement-ID tag accuracy

- **What went wrong**: T3 shipped with two tests tagged with the wrong edge-case ID (`(E1)` on what is actually an `E2` case; `(E2)` on a test that maps to no edge case in the spec at all). This survived T3's own mandated self-review and was only caught later, incidentally, while assembling Phase 7's verdict table.
- **Why**: `clean-code.md`'s checklist covers dead code, debug leftovers, duplication, and similar hygiene items, but nothing on it asks "does every test's cited `R#`/`E#` actually match the spec" — a wrong tag is invisible to every check the self-review is told to run, even though it directly undermines traceability (D5) and the Phase 7 report's own evidence citations.
- **Fix shape**: Add one line to `clean-code.md`'s checklist: "every test naming an `R#`/`E#` in its title actually matches that requirement's or edge case's definition in the current spec."

### 7. Where: SKILL.md Phase 5 ("If implementation reveals the spec or plan is wrong, stop... a standing waiver does not cover this")

- **What went wrong**: T3 revealed `plan.md`'s C3 component never named the single-task lookup (`getTask`) its own described task-ownership check actually needs. I treated this as a small bookkeeping fix (add the function, amend the plan's Reuses line, get a one-line confirmation) rather than the full stop-and-return-to-Phase-3 cycle the rule literally describes for "the plan is wrong."
- **Why**: The rule gives one instruction regardless of the defect's size — a plan missing a two-line helper function and a plan built on the wrong architecture are treated identically ("stop... amend the artifact with the user"). Nothing distinguishes a proportional response, so an agent has to decide on its own how much ceremony a given plan gap deserves, with no textual anchor for where that line sits.
- **Fix shape**: Add a proportionality clause: "a plan gap that adds a small, same-pattern helper without changing a component's `Implements`, architecture, or Reuses target may be confirmed in one line and folded into the current task's note; a gap that changes what a component does or where it lives is the full stop this rule describes."

### 8. Where: SKILL.md → Resuming work — Missing or unrecoverable artifacts ("restore it from git history; if it is unrecoverable, regenerate it..., leave every regenerated task unchecked, ... get the regenerated artifact re-approved, then run Phase 7 immediately as a diagnostic pass")

- **What went wrong**: `plan.md` was cleanly recoverable from git history (added once, deleted whole, no edits between). I chose to still re-present it for the user's confirmation and treated the drift check's already-independent Phase 7 trigger as covering the "run Phase 7" clause here too — but the sentence's clauses ("leave every regenerated task unchecked," "get the regenerated artifact re-approved") read grammatically as describing the *regenerate* branch specifically, not the *restore* branch that actually applied.
- **Why**: The bullet's single sentence covers two very different recovery qualities (an exact restore vs. a lossy re-derivation) without a clear boundary for which of its trailing clauses apply to which branch — an agent doing a clean restore has to guess whether the re-approval and diagnostic-pass steps are required or merely good practice.
- **Fix shape**: Split the sentence: "...restore it from git history — re-present it for the user's acknowledgment given the time it was missing, but treat its content as already approved. If it is unrecoverable, regenerate it from the surviving artifacts, leave every regenerated task unchecked, record the reconstruction as a Decisions entry, get the regenerated artifact re-approved, then run Phase 7 immediately as a diagnostic pass."

### 9. Where: my own execution — D1 (depth), see friction #1 for the skill-side root cause

- **What went wrong**: Never stated depth at any point in the resume flow, even informally.
- **Why / Fix shape**: See friction #1 — this is the same gap, logged here only to confirm it's reflected in D1's score, not a second independent finding.
