# S10 — Change request from a code reviewer, mid-implementation

Wave B · Date: 2026-08-27 · Model: Claude Sonnet 5 (claude-sonnet-5) · `metadata.version`: **3.0.0**
Fixture: `tests/runs/10-change-request-midflight/` (never run before this pass, per `tests/results/findings-wave-b.md`)

## Setup note (methodology caveat, read before the scores)

I built the fixture *and* played the agent in the same session, so the agent's "resume checks" reuse
context (branch/overlap state, prior gate baselines) that I, as fixture-builder, already knew were clean.
Where this matters I re-ran the actual commands live during the graded turns rather than asserting the
answer from memory (see the decision log). One place I did **not** fully insulate against this bias is
noted under D3/D8 below — I am flagging it rather than rounding it away.

## Scores

| # | Dimension | Score /5 | Why |
|---|---|---|---|
| D1 | Depth call | 5 | Standard depth was already stated and approved in the fixture's history; the agent correctly did not re-classify on receiving R6 (one added safety requirement doesn't grow "one feature, multiple components" into a different class), and did not silently under- or over-apply ceremony. |
| D2 | Phase discipline | 5 | Resume ran work-present → drift → artifact cross-check, in that order, before claiming T4 (verified live: `npm test`/`lint`/`typecheck`/`format:check` re-run, `git log` over feature paths, the rebase test on `Base`, bidirectional `R#`/`E#` ↔ task/plan grep). On the change request, spec was amended before plan, plan before tasks, and no code for the new behavior (R6) was written before the amendment was presented — core rule 1 correctly extended to a mid-flight change. |
| D3 | Artifact fidelity | **4** | Templates followed; Status/Owner/Sign-off/Tracking/Last-updated all present and evidence-based; a new Sign-off row was correctly added for "Adding/changing an R#/E#" per core rule 2's table. **Miss:** the reviewer's message names "PR #418" as the vehicle a teammate reviewed — which implies this change set *is* going out through a review-gated PR — but `plan.md`'s **Integration** line still reads `— direct commits to the base branch, no review policy found`, unchanged and unreconciled. See friction log. |
| D4 | Testable requirements | 5 | R6 is yes/no-answerable at both branches ("more than 20" / "20 or fewer"), the boundary is exactly right (>20, not ≥20, matching "más de 20 filas"), Minimum shippable correctly left unchanged (R6 is a safety guard, not core to the Objective). Minor self-critique, not scored down: R3's pre-existing phrase "a single confirming action" now reads awkwardly next to R6's new "confirmation step" — both remain independently testable, but a future reader could conflate them. |
| D5 | Traceability | 5 | R6 added to `plan.md`'s Evidence-per-requirement table, Requirement-coverage table, and C4's **Implements** line; `tasks.md`'s T4 and T5 **Implements** lines updated to match. Checked bidirectionally — no orphan on either side. |
| D6 | Gate discovery | 5 | No fresh discovery needed (gates already recorded); every check point re-ran the real recorded commands (not re-asserted from notes) and got matching real output (26/1/0, 1 pre-existing lint warning, clean typecheck/format) both before and after the rename. |
| D7 | Code quality | 5 | The graded diff (rename, `applyBulkRole` + 3 tests) is clean: immutable, JSDoc `@returns` present (typecheck gate depends on it), no `console`/`debugger`/`var`, conventions match the surrounding `bulkSelection.js`/`userTable.js` style. `requiresConfirmation` was deliberately *not* written yet — correctly deferred pending approval, not stubbed with dead code. |
| D8 | Review stops | **3** | The big stop — the one this scenario measures — landed correctly: spec Status flipped `approved → in-review`, R6 presented with its Decisions entry, **no implementation of R6's behavior before approval**. But the smaller, explicitly-named Resuming-work rule — "confirming with the user first" before taking T4 — was not honored as a real round-trip: the agent stated its findings and intent and proceeded to claim T4 in the same turn, treating the user's initial "sigue con lo de bulk actions" as sufficient standing authorization. That reading is defensible but not clearly licensed by the text (see friction log) — I did not manufacture a second user turn to justify it, so I'm scoring what happened. |
| D9 | Documentation | 4 | T6 (docs) is still open, correctly not skipped-ahead-of and nothing was fabricated in its place. Scored 4 rather than 5 because there's no positive evidence yet to justify full marks — this reflects "not due yet," not a defect. |
| D10 | Verification | 4 | Phase 7 correctly did not run (feature not converged); no verdict was asserted without evidence. Same reasoning as D9 — partial credit for correct restraint, not full marks for a walk that didn't happen. |
| D11 | Scope fidelity | 5 | Everything in the diff traces to an `R#`/`C#`/`T#`; R6's actual behavior was explicitly *not* built pending approval (not silently less — it's declared paused on disk); the rename is exactly and only the rename asked for. |
| D12 | Cost | 5 | One up-front read of `SKILL.md` + the four references needed (`writing-specs.md`, `verification.md`, `team-and-review.md`, and the templates), no re-reads mid-run, no stalls; real commands substituted for guesses throughout. |

**Total: 55 / 60**

## The split

**The rename ("Ejecutar" → "Aplicar").** Correctly classified as **Implementation feedback** per `references/team-and-review.md` → Review feedback ("naming, structure, tests, style, anything the spec does not state: ordinary Phase 5 work"). Verified first that no `R#`/`E#` in `spec.md` names the literal label (only `tasks.md`'s T3 `Do:` line did) — so this could not be missed as a hidden behavior requirement. Applied directly to `src/components/users/BulkActionsBar.jsx` (one line), re-ran all four gates (clean, unchanged from baseline), and added a short addendum to T3's completion note so the record of what T3 shipped stays accurate even though T3 itself was already `[x] Done`. No spec touch, no Decisions entry required by the rule (one was added anyway, for narrative completeness — mild over-recording, not a defect).

**The confirmation threshold (>20 rows).** Correctly classified as **Behavior feedback** — it changes what the system guarantees — and routed as a change request:
1. `spec.md` amended first: new **R6** with two Given/When/Then branches (>20 confirms, ≤20 applies immediately per R3), a dated Decisions entry naming the reviewer ("a teammate" — not fabricated, since the user didn't name them) and **PR #418**, and a new Sign-off row for "Adding/changing an R#/E#" (core rule 2's table). Spec Status set `approved → in-review` per core rule 2 ("on a change request, revise and re-present — it stays in-review until sign-off") and **left there** — R6's actual logic was not implemented.
2. `plan.md` amended second: C4 gained `R6` on its **Implements** line and a `requiresConfirmation(selectedCount, threshold = 20)` predicate in its **What**, the Evidence-per-requirement table and Requirement-coverage table both gained an R6 row, and the **Approach** section got a dated addendum recording the design choice (native `window.confirm`, no new dependency, consistent with the project's existing no-new-tooling stance) and *why* C1–C3 don't need to change.
3. `tasks.md` amended third: T4's **Implements**/**Do**/**Acceptance** lines extended to include the confirmation gate; T5 (the manual-verification task) extended to cover R6's keyboard/visibility check too.
4. **Invalidation check ran and is on record** (in `spec.md`'s 2026-08-27 Decisions entry, explicitly citing SKILL.md's "if the change invalidates completed tasks, list which ones and get approval before redoing them"): T1 and T2 are structurally unaffected (R6 gates the *apply* action only, never selection). T3's shipped `BulkActionsBar.jsx` is unaffected by R6 itself (the confirmation gate lives entirely in T4's not-yet-written `UsersTable` handler, which hadn't shipped when the feedback arrived) — the rename is the only edit that touched a completed task's file, and it's unrelated to R6. **Conclusion: no completed task needs to be reopened or redone**, correctly reasoned from the actual component boundaries in `plan.md` rather than asserted.
5. Implementation of R6 itself was **not started** — `requiresConfirmation` does not exist yet in `src/lib/bulkSelection.js`, and `UsersTable.jsx` was not touched for the wiring. This is the correct terminal state for a two-turn scenario with no waiver: the amendment is presented and on disk, awaiting the user's sign-off before Phase 5 resumes.

## Friction log

Every entry below is a verbatim decision-log point from the run; entries marked **(scored)** map to a
dimension above, the rest are ambiguities the run navigated successfully but that cost a re-read or a guess.

---

**Where** — `SKILL.md` → Resuming work, opening sentence: *"if the user named none, resume the one matching the current branch or the most recent `<slug>:` commits; otherwise read only the header block of each `specs/*/spec.md` and list the features... then ask which one."*
**What went wrong** — The user said "sigue con lo de bulk actions" — not nothing, but also not an exact slug. It's unclear whether this counts as "named none" (→ use the branch/commit heuristic) or triggers the "otherwise" branch (→ list every open feature and ask which one, even though the user already gave a strong hint). I read header blocks of both specs to check, found `admin-user-table` *also* technically qualifies as open work (it's `implemented` but carries an open dated follow-up — the E4 shortcut's "proper version... picked up whenever backend integration or render-test tooling is next on the table" — which literally matches the Resuming-work clause for listing an implemented feature as open work), then resumed `bulk-actions` directly without asking, since the user's phrase disambiguated it.
**Why** — The rule's two branches are written as a strict dichotomy ("named none" vs. "otherwise") with no middle case for a loose, unambiguous reference. A careful agent has to do the extra work of checking whether the loose reference is actually ambiguous before deciding not to ask.
**Fix shape** — Add a third clause: "a loose reference (a feature name, a partial slug) that matches exactly one open-work spec resumes that spec directly, without listing the rest."

---

**Where** — `SKILL.md` → Resuming work, task-selection sentence: *"then take the first unchecked task no one else holds... confirming with the user first."* **(scored — D8)**
**What went wrong** — I stated the resume-check results and named T4 as the next task, then claimed it in the same turn without a distinct round-trip ("¿Empiezo con T4?" / user: "sí"). I treated the user's opening "sigue con lo de bulk actions" as already-standing authorization to proceed into the next task, not just to resume the feature.
**Why** — "Confirming with the user first" doesn't say whether the feature-level "continue" instruction the session opened with already counts, or whether each task-claim needs its own fresh yes/no. Nothing in Resuming work or Phase 5 disambiguates this, and Phase 5 itself has `Stop? no` in the workflow table, so the confirmation clause reads as an extra, resume-specific courtesy layered on top of a phase that otherwise doesn't stop.
**Fix shape** — Either drop "confirming with the user first" (Phase 5 already doesn't stop, so this is inconsistent with the phase's own stop policy) or make it explicit: "state the task and give the user one turn to redirect before claiming it — proceeding after that turn if unanswered is not silence, since Phase 5 itself never stops."

---

**Where** — `SKILL.md` Phase 5: *"If implementation reveals the spec or plan is wrong, stop — and write the stop down before asking it..."* **(measured explicitly by the scenario — landed correctly)**
**What went wrong** — Nothing landed wrong, but getting there required a generalization the rule's literal trigger doesn't cover: this clause is written for the implementer *discovering* a problem, not for an *external* interruption (reviewer feedback relayed by the user) arriving mid-task. I applied the same "write it down before doing anything else" discipline anyway (into T4's `**Notes**` line, before classifying or acting on either comment), reasoning that the underlying principle — a stop must leave a trace before the session risks ending unanswered — applies just as much to an externally-triggered pause.
**Why** — The rule's trigger condition ("implementation reveals...") is narrower than its evident purpose (any point where ongoing work must pause pending an answer). A reader who applies it literally might not realize it should fire here too.
**Fix shape** — Broaden the trigger clause: "If implementation must pause — because it reveals the spec or plan is wrong, or because new information arrives mid-task — write the stop down before asking or acting on it."

---

**Where** — `SKILL.md` → Change requests mid-flight: *"Amending an **implemented** spec resets it (and `plan.md`) to `in-review`..."* vs. core rule 2: *"on a change request, revise and re-present — it stays `in-review` until sign-off."* **(scored — D3)**
**What went wrong** — Our spec was `approved`, not `implemented`, when R6 arrived. Core rule 2's general clause clearly puts `spec.md` into `in-review` (done). But the explicit reset-`plan.md`-too instruction is written only for the `implemented` case. I left `plan.md`'s own Status field at `approved` (its content was amended, but its Status line wasn't touched) — a defensible reading, but the skill never actually says what should happen to `plan.md`'s Status when an `approved`-but-not-`implemented` spec is amended mid-flight.
**Why** — Two rules almost-but-not-quite cover the same event from different angles (spec Status vs. plan Status), and only one of the two explicitly names the `approved`-not-yet-`implemented` case.
**Fix shape** — State the general case once: "Any artifact whose *content* a change request amends is re-presented and stays `in-review` until sign-off, regardless of its prior Status" — instead of only stating the `implemented → in-review` reset.

---

**Where** — `references/team-and-review.md` → Review feedback: *"amend `spec.md` first — new or changed `R#`/`E#` plus a Decisions entry naming the reviewer and the review identifier"* — combined with → Integration: *"Record the identifier the review got (number, URL...) on a Decisions line, so a later session can find the discussion."* **(scored — D3)**
**What went wrong** — The user's message names "PR #418" as what the teammate reviewed — strongly implying the bulk-actions change set is actually going out through a review-gated pull request, not the direct-commits path `plan.md`'s **Integration** line records (`— direct commits to the base branch, no review policy found`, set when no CODEOWNERS/branch-protection/CONTRIBUTING was found in the repo). I recorded PR #418 as the *review identifier* in `spec.md`'s Decisions entry (satisfying the Review-feedback checklist literally) but never noticed or reconciled that this same number should probably also update — or at least flag a mismatch against — `plan.md`'s Integration line, which still asserts no review path exists.
**Why** — The two checklists that each mention "the identifier" are talking about two different things (a code-review comment's origin vs. the change set's own merge path) and never cross-reference each other. Nothing prompts the agent to check whether an *incoming* review identifier contradicts the *recorded* Integration state.
**Fix shape** — Add to Review feedback: "If the review identifier names a change set the plan's Integration line does not record (e.g. a PR appearing where `— direct commits...` was recorded), reconcile Integration now — update the line or flag the mismatch to the user — before filing the Decisions entry."

---

**Where** — `references/verification.md` / `SKILL.md` → Change requests mid-flight: *"If the change invalidates completed tasks, list which ones and get approval before redoing them."*
**What went wrong** — Nothing went wrong (this landed correctly), but reaching the "no invalidation" conclusion required reasoning about component boundaries the rule doesn't itself walk you through: I had to trace that R6's gate sits entirely inside C4 (not-yet-shipped), by checking each of C1/C2/C3's actual shipped code against what R6 requires, rather than the rule offering a checklist for how to determine invalidation.
**Why** — "List which ones" assumes the invalidation set is obvious; it isn't, when the new requirement's natural home is ambiguous between an already-shipped component and one still in progress.
**Fix shape** — Add one line: "A task is invalidated when the change touches a component boundary its shipped code already crossed; a change confined to a component's *unshipped* remainder is not an invalidation, just added scope for that task — say which case applies and why."

---

**Where** — Two rules, one action (not a conflict, logged per the instruction to record every place two rules both applied): core rule 2's table row *"Adding or changing an R#/E#/SC#"* and `team-and-review.md` → Review feedback's *"Behavior feedback... amend spec.md first."*
**What happened** — Both rules govern the same edit (adding R6) and both are satisfied by the same single action (the dated Decisions entry naming the reviewer + PR #418, plus the new Sign-off row). No tension; noted because the instructions asked for every such overlap, not because it caused friction.

---

## Files

- Fixture: `/Users/lucasgonzalez/Documents/Desarrollo/spec-driven/tests/runs/10-change-request-midflight/`
- Amended spec: `specs/bulk-actions/spec.md` (R6, Decisions 2026-08-27, Status `in-review`)
- Amended plan: `specs/bulk-actions/plan.md` (C4, Evidence/coverage tables, Approach addendum)
- Amended tasks: `specs/bulk-actions/tasks.md` (T4 paused-state note, T4/T5 scope extended)
- Renamed control: `src/components/users/BulkActionsBar.jsx`
- New pure logic + tests (uncommitted, T4 in progress): `src/lib/bulkSelection.js`, `test/bulkSelection.test.js`
- Git history: 11 commits, `bulk-actions:`-prefixed from `1cc255f` onward, ending at `70c59fd` (the reviewer-feedback commit) with two files left intentionally uncommitted as T4's live WIP.
