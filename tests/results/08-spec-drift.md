# S08 — Verification against pre-existing, drifted code

**Wave**: B (new — never run against any version before this)
**Date**: 2026-08-27
**Model**: Claude (Sonnet 5), acting as both the coding agent and the scripted user
**Skill version under test**: `metadata.version: "3.0.0"` (SKILL.md frontmatter)
**Fixture**: `tests/runs/08-spec-drift/` — a minimal offline React-shaped app (Node v22, `node --test`, hand-rolled lint/typecheck/format stand-ins mirroring `tests/runs/01-react-data-table/`'s pattern) with a completed-but-drifted `specs/user-search/` feature: R3 implemented as plain alphabetical sort instead of the spec's relevance ranking (drift), R5 (debounce) entirely unimplemented, E2 (search-failure handling) entirely unimplemented, `src/lib/searchCache.js` built but never imported (deletion gap), and a debug `console.log` left in `src/features/search/useSearch.js` that also leaks matched users' name/email (a Sensitive-ground Data-handling violation, not just a clean-code hit). Two git commits: a pre-feature scaffold (`e2d0983`) and the drifted feature (`8b0ac7f`), so `git diff <base>...HEAD` is meaningful for the dead-code sweep.

**Request**: "Verifica que la búsqueda de usuarios cumpla con su spec." No waiver granted at any point.

## Scores

| # | Dimension | Score /5 | Justification |
|---|---|---|---|
| D1 | Depth call | **3** | Correctly determined this is Resuming-Work → Phase 7 (not Audit mode, not a fresh depth classification) through its actions (checked Audit mode's two negative conditions, ran the ordered Resuming-Work checks) — but never stated this as one explicit line to the user before starting substantive work, the way Adaptive Depth requires for new work. SKILL.md has no analogous "state your entry mode" instruction for the Resuming-Work path, so this is as much a text gap as an execution one. |
| D2 | Phase discipline | **3** | Resuming-Work's ordered checks and the full Phase 7 procedure ran correctly, in order, gaps reported before any fix — but Phase 5's explicit claim rule ("claim it by setting **Owner**... and commit that claim before writing code — one commit, always") was skipped outright when implementing G4/G5: code changes and the claim were folded into a single commit instead of two. A real, confirmed skipped rule, not an interpretation call. |
| D3 | Artifact fidelity | **5** | Every artifact touched (spec.md, plan.md, tasks.md) got its `Last updated` bumped from real edits; Decisions entries dated and rationaled; plan.md's cut component correctly annotated `— cut (Decisions 2026-08-27)` per the plan template's own convention. |
| D4 | Testable requirements | **4** | Not meaningfully exercised — this is a Phase-7-only scenario, no Phase 1 ran. The inherited spec's R#/E# were all yes/no-answerable and this testability is exactly what let the pass reach precise verdicts, but the dimension itself is largely inherited rather than produced by the agent under test. |
| D5 | Traceability | **5** | Actively verified, not assumed: caught that `plan.md`'s Evidence-per-requirement and Requirement-coverage tables falsely attributed R5 to a component (`searchCache.js`) that was never wired in, rather than trusting the plan's claims at face value. |
| D6 | Gate discovery | **5** | Real, empirical verification via a `git worktree` on the recorded Base SHA (not fabricated): confirmed the lint warning is genuinely new (0 warnings on the untouched tree) and separately discovered the recorded "Types: clean" baseline doesn't literally reproduce at that SHA (crashes — no `src/` exists yet there), reported as a non-blocking technicality rather than ignored or over-escalated. |
| D7 | Code quality | **5** | Both the dead code (`searchCache.js`) and the debug leftover were caught by real mechanical sweeps (fresh `grep`/reachability tracing) run at Phase-7 time, not recalled from having planted them. |
| D8 | Review stops | **5** | Every required stop actually happened and was answered by the scripted user: manual-verification-as-evidence sign-off, the R3 spec-drift decision point, the deletion-gap decision, and approval before implementing G4/G5. No waiver existed or was assumed. |
| D9 | Documentation | **3** | Process was correct (staleness identified, gapped as G6, not silently fixed or ignored) — but graded on disk state, not intent: `docs/user-search.md` remains genuinely inaccurate (claims relevance ranking, a debounce, and error-handling that don't exist) at the end of the run, since the user deferred G6 along with G1–G3. |
| D10 | Verification | **4** | Rigorous and empirically grounded: every verdict cites real code, tests were actually executed (not assumed), negative controls for R1/R4 were run by physically stubbing and restoring code, E2's unhandled rejection was reproduced live. Docked one point because the negative-control rule has no defined behavior for a Minimum-shippable requirement (R6) whose *only* evidence is an approved manual trace — its escape hatch text is scoped to "a compile-time or type-level criterion," not to "no assertion exists at all," so the agent had to extend it by analogy rather than follow explicit instruction. |
| D11 | Scope fidelity | **5** | No code touched until gaps were filed and approved; the later G4/G5 implementation stayed exactly within what was explicitly approved (nothing from G1/G2/G3/G6 was touched). Both required Decisions/report citations (deletion-gap user confirmation, G# task recording the spec-drift resolution) were present per core rule 2's table. |
| D12 | Cost | **5** | The scored run (from fixture-finalization onward) was direct: oriented once, walked the spec once per pass, no repeated re-reads of SKILL.md, no stalls. (Two rounds of fixture-construction rework happened *before* the scored run began — see Decision log note — and are not counted here.) |

**Total: 52/60**

## Friction log

### F1 — D1: no stated entry-mode line for Resuming-Work/Phase-7-only entry
- **Where**: SKILL.md → Adaptive depth: *"State the chosen depth in one line before starting... When unsure, ask which depth the user wants instead."* This instruction is scoped to the Adaptive Depth table (new work being classified Trivial/Small/Standard/Large).
- **What went wrong**: When entering via Resuming Work → Phase 7 (existing, completed feature; no new depth to classify), there is no equivalent instruction to state the entry mode/plan in one line before starting. The agent correctly determined internally that Audit mode did not apply and that Phase 7 was the right procedure, but never surfaced that determination to the user up front — it only became visible retroactively through the report.
- **Why**: The "state before starting" rule lives entirely inside the Adaptive Depth section, which textually only covers the new-feature path. Resuming Work has no analogous bullet.
- **Fix shape**: Add one sentence to Resuming Work's opening paragraph: "State which case applies (resume in-flight work / diagnostic pass / Audit mode) and why, in one line, before running its checks — the same transparency Adaptive Depth requires for new work."

### F2 — D2: Phase 5's claim-commit rule is buried and was skipped
- **Where**: SKILL.md → Phase 5 — Implement, second bullet: *"...then claim it by setting **Owner** to who (or which branch) is executing it plus today's date, and commit that claim before writing code — one commit, always, whatever the scan found..."*
- **What went wrong**: When implementing G4 (delete `searchCache.js`) and G5 (remove the `console.log`), the agent went straight from user approval to writing the code changes and committing them together, with no separate claim-commit beforehand. A real, unambiguous rule was skipped, not misread.
- **Why**: The claim-commit instruction sits mid-paragraph, sandwiched between the overlap-scan cross-reference and the staleness/7-day rule, in a bullet whose primary visible topic is "confirm nobody else holds this task" — not "always commit the claim as its own commit." In a single-session, single-branch, no-team context, the "claim" ritual reads as procedural overhead for a concern (concurrent claims) that visibly doesn't apply, making it easy to silently drop even though the rule states "one commit, always" with no solo-session exception.
- **Fix shape**: Give the claim-commit its own sentence or sub-bullet, separate from the overlap-scan/staleness content, and state explicitly that it applies even in a solo, single-branch session (the rule already says "always," but nothing calls out that "always" includes the seemingly-unnecessary solo case).

### F3 — D10: negative-control rule has no defined behavior for manual-trace-only evidence
- **Where**: references/verification.md → Procedure, step 2, "Negative control for the Minimum shippable set": *"...show the cited assertion actually fails when the behavior is stubbed out or reverted... Cite the observed failure; where the stub cannot be produced (a compile-time or type-level criterion), say so in one line on the report."*
- **What went wrong**: R6 is inside this fixture's Minimum-shippable set (`R1, R4, R6`) and its *only* evidence is an approved manual code trace (no JSX-render tool exists in the project) — there is no assertion at all to invert. The rule's one stated escape hatch ("a compile-time or type-level criterion") does not describe this case. The agent extended the hatch by analogy ("no negative control possible on manual-only evidence — noted") rather than following an explicit instruction, because none exists.
- **Why**: The rule was written with an automated-test model in mind and only anticipated one specific reason a stub can't be produced. It doesn't account for its own sibling exception (the manual-verification exception two paragraphs above in the same file) ever landing on a Minimum-shippable requirement.
- **Fix shape**: Extend the escape-hatch sentence: "...where the stub cannot be produced (a compile-time or type-level criterion, **or the requirement's only evidence is an approved manual trace with no assertion to invert**), say so in one line on the report."

### F4 — D6/D10: ambiguous whether a *new warning* (not just a new error) counts as a gate failure
- **Where**: references/verification.md → Procedure, step 4: *"Gates are judged as no new failures, not absolute zero"* combined with Recording gates' *"Compare a baseline recorded as a count... per file and per rule."* Neither sentence states outright whether a lint/type gate's tracked "count" includes warnings, or only the exit-code-determining errors — the one place the text is explicit about counts (skipped/executed/passing) is scoped to the test gate only.
- **What went wrong**: The fixture's lint stand-in exits 0 regardless of warnings (only errors fail it), so the new `console.log` warning left the gate's exit code unchanged from baseline. The agent had to infer — from `tests/runs/01-react-data-table`'s own precedent of recording a "1 pre-existing warning" baseline, not from an explicit SKILL/reference rule — that a newly-appeared warning should be classified `new` and gapped, not waved through because the exit code matched baseline.
- **Why**: Low practical risk here specifically because step 5's mechanical clean-code sweep ("No debug output... outside real logging") catches the same `console.log` unconditionally regardless of this ambiguity — the two rules overlap and one is unambiguous. But a lint rule with no clean-code-checklist analogue (a style or complexity warning, say) would have no such safety net.
- **Fix shape**: Add one clause to Recording Gates' baseline definition: "...a gate's tracked baseline is its full reported output — warnings and any other severity the tool reports, not only what the tool's own exit code treats as failing."

### F5 — D3/D10: report-block heading has no provision for same-day multiple passes
- **Where**: assets/tasks-template.md anchors comment: *"Report blocks are `### Verification report — <slug> — <YYYY-MM-DD>`, strictly one level below `## Verification reports`. Keep these exact shapes."* / references/verification.md → Convergence loop: *"count the passes on the report blocks, which is what makes 'two' checkable."*
- **What went wrong**: Pass 1 and pass 2 of this run happened on the same calendar date (`2026-08-27`). The literal template heading gives both blocks an identical title. The agent improvised a `(pass 2)` suffix to keep them distinguishable — a deviation from the "keep these exact shapes" instruction that anchors elsewhere in the file rely on.
- **Why**: The heading format's only variable is the date, which is too coarse a key when convergence genuinely takes multiple passes within one working session (a realistic, even common case for a small gap-fix like this one).
- **Fix shape**: Extend the heading shape to include an explicit pass ordinal always, not just when needed: `### Verification report — <slug> — <YYYY-MM-DD> — pass <n>` — cheap, and removes the same-day collision entirely rather than leaving it to be improvised inconsistently across agents/runs.

## Verdict-accuracy table

| Id | Expected | Actual verdict produced | Match |
|---|---|---|---|
| R1 | met | met (test citation + negative control + signed-off manual trace for the UI-trigger clause) | ✅ |
| R2 | met | met (signed-off manual trace; no automated test possible) | ✅ |
| R3 | spec drift | spec drift (empirically demonstrated: alphabetical vs. relevance order diverge on a constructed case; cited test does not encode the relevance clause) | ✅ |
| R4 | met | met (test citation + negative control + signed-off manual trace for the UI-clearing clause) | ✅ |
| R5 | not met | not met (no debounce mechanism exists; plan's cited cache-based evidence doesn't exist either) | ✅ |
| R6 | met | met (signed-off manual trace; no automated test/negative-control possible — flagged as its own finding, F3) | ✅ |
| E1 | met | met (test citation) | ✅ |
| E2 | not met | not met (empirically reproduced unhandled rejection; cited test doesn't encode the criterion) | ✅ |
| E3 | met | met (test citation) | ✅ |

All nine verdicts match the scenario's expected answer key exactly.

## Additional findings beyond the scenario's stated drifts

- **`searchCache.js` deletion gap**: caught cleanly, correctly not auto-deleted (user's explicit confirmation obtained and cited both in the gap task and the report's Dead-code sweep line, per core rule 2's table).
- **Junk-code catch**: caught (`console.log` at `useSearch.js:30`), and correctly recognized as a *double* hit — both a mechanical clean-code violation **and** a direct contradiction of the spec's own Sensitive-ground Data-handling non-goal (the log line prints matched users' name and email). Neither the scenario description nor the fixture's design notes called out this second angle explicitly; it fell out of actually cross-referencing the spec's coverage lines during the walk rather than only running the clean-code checklist mechanically.
- **Stale documentation**: `docs/user-search.md` describes the spec's *intended* behavior (relevance ranking, debounce, error handling) as already shipped. This is not one of the scenario's four named drifts but is a direct, correctly-caught consequence of Phase 7 step 7 ("documentation describes behavior as specified... that is spec drift, don't paper over it") — filed as G6.
- **Plan-bookkeeping falsification**: `plan.md`'s Evidence-per-requirement table asserted specific, checkable claims for R5 ("the 300ms debounce timer in `useSearch.js`") and E2 ("try/catch... surfaced as the inline error message") that are simply false — neither exists in the named files. The agent did not accept these at face value; it re-derived every verdict from the actual code, exactly as the citation contract requires.

## v3.0.0 changes: did they hold?

- **Citation contract (test case + assertion + criterion clause; never carry a verdict forward)**: **held, and did real work.** It was the citation contract specifically — not just "reading the code" — that caught R3: `test/search.test.js::"rankResults orders results by name"` genuinely passes and genuinely exercises `rankResults`, but never asserts anything about relevance-to-query, so per the contract it "does not encode" R3. A verification pass that only checked "is there a passing test named plausibly" would have rubber-stamped this as met. The "never carry forward" half was exercised for real across two passes: pass 2 re-ran every gate and every negative control from scratch (including for R1/R2/R4/R6/E1/E3, which hadn't changed) rather than copying pass 1's verdicts, and the two report blocks are genuinely distinct, re-derived documents. One real gap found in the same mechanism: the negative-control sub-rule doesn't cover manual-trace-only evidence inside the Minimum-shippable set (F3).
- **Gate-failure-is-a-gap**: **held.** The `console.log`'s lint warning was correctly classified `new` (via a real base-tree control through a `git worktree`, not assumed) and filed as a gap (G5) that blocked exit — exactly A4-F1's fix. The one wrinkle (F4) is that recognizing it as a *gate* failure at all, separately from the always-fires clean-code sweep, required inferring that a tool's warning output counts toward its baseline even when its exit code doesn't change.
- **New report block (`Change set:` / `Converged:` first, append-as-you-go)**: **held, format-complete.** Both blocks opened with `Change set:`/`Converged:` first; every labelled line the exemplar requires was present (writing `none` where empty) across both passes; the block was opened at step 1 and closed at step 9 as instructed. The one deviation found (F5) is structural, not a content omission: the template's heading has no room for a same-day second pass, so `(pass 2)` was improvised.
- **Report-don't-fix ("a gap noticed mid-walk is reported, not fixed on the spot")**: **held completely.** No code was touched during the entire walk (steps 1–9) despite finding four real, fixable defects; every one was filed as a `G#`, presented, and only G4/G5 were implemented after separate, explicit approval — and even then, in a distinct Phase-5 step after the report closed, not folded into the verification pass itself.

## Decision log

Real friction is captured as F1–F5 above. The remaining logged actions produced no friction — the applicable rule was read, was unambiguous, and was followed as written:

- Determined Audit mode's entry condition (spec.md + shipped code, **no** plan.md/tasks.md) was unambiguously false here (both exist) — no ambiguity to report, per the scenario's own prompt to check.
- Ran Resuming Work's ordered checks (Work-present, Drift/rebase test, Artifact cross-check, Missing-artifacts, Stopped-at-earlier-phase, Every-task-closed-still-approved) in the stated order; the last one correctly triggered Phase 7 as a genuine (non-diagnostic) pass since no `T#`/`G#` was unchecked going in.
- Recognized the manual-verification-as-evidence sign-off requirement (core rule 2's table) for R1/R2/R4/R6's UI-wiring portions and stopped for it, batching the ask across all four rather than four separate stops — a reasonable judgment call the text neither requires nor forbids.
- Correctly applied Handling gaps' spec-drift decision point (put the choice to the user rather than deciding unilaterally) and the deletion-gap "never automatic" rule (asked before deleting `searchCache.js`).
- Correctly applied the SC# walk's "pending only on its value" distinction between SC1 (signal path exists in the change set) and SC2 (reads an external, not-yet-observable signal).
- Correctly reported `Integration: direct commits — no review policy`, matching the exact phrasing the reference gives for that exact topology.

**Note on fixture construction** (before the scored run began, not counted in D1–D12 above): building the fixture surfaced two of its own bugs, both fixed before Step 2 started. First, a `select()`/`useEffect` interaction meant selecting a result would silently reopen the results list moments later (`setQuery` inside `select()` re-triggered the `[query]`-keyed search effect) — this would have made R6 genuinely broken and contaminated the "rest met" control group, so a `suppressNextSearch` guard was added. Second, `SearchBox` was never mounted by anything, which would have made the *entire* feature chain unreached (not just `searchCache.js`) under the dead-code sweep — a `src/pages/AdminDashboard.jsx` entry point (mirroring `01-react-data-table`'s own `src/pages/` convention) was added to fix this. Both were caught and corrected by re-reading the fixture adversarially before the scored run, exactly as the scored run later re-read the feature adversarially — but neither is scored against the skill, since neither happened during Step 2.

Scorecard: `tests/results/08-spec-drift.md`
