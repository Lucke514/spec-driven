# Scorecard — 01-react-data-table

- **Scenario**: [scenarios/01-react-data-table.md](../scenarios/01-react-data-table.md) — sortable/filterable admin user table (Standard depth)
- **Iteration**: 1
- **Date**: 2026-08-26
- **Model**: Claude Sonnet 5 (`claude-sonnet-5`)
- **Run**: [tests/runs/01-react-data-table/](../runs/01-react-data-table/) — see `specs/admin-user-table/{spec,plan,tasks}.md`, `docs/admin-user-table.md`, branch `admin-user-table`

**Fixture deviation (disclosed per the task brief):** the fixture cannot run real `eslint`/`tsc`/`vitest`/`prettier` (no `npm install`, no network). `package.json` keeps the real script names but each one shells out to a small hand-rolled Node script (`scripts/lint.js`, `scripts/typecheck.js`, `scripts/format-check.js`) or `node --test`, documented as such in the fixture's own `package.json` and `README.md`. Components are plain `.jsx`, not TypeScript. This changes what "gate discovery" found (a genuinely minimal toolchain) but not whether the agent followed the discovery *process* correctly — it did.

## Scores

| # | Dimension | Score /5 | Justification |
|---|---|---|---|
| D1 | Depth call | 4 | Correct class (Standard) chosen and recorded in `spec.md` Decisions before any other artifact existed — but the "state it in one line before starting" step (SKILL.md → Adaptive depth) was folded into the spec draft itself rather than delivered as a distinct statement the user could react to before Phase 1 output existed. |
| D2 | Phase discipline | 5 | Phases 1→2→3→4→5→6→7 ran in order, Phase 0 correctly skipped (not Large), every phase's artifact landed on disk before the next began, no chaining without approval. |
| D3 | Artifact fidelity | 5 | All three templates followed exactly; Status/Owner/Sign-off/Tracking/Last updated filled from real repo evidence (absence of CODEOWNERS, `git log`, branch scan), not assumed. |
| D4 | Testable requirements | 4 | Every `R#`/`E#` is a yes/no Given/When/Then, `Minimum shippable` is present, edges are real (E1–E5). Docked because the first *approved* draft of R6 silently under-covered writing-specs.md's own 4-item accessibility checklist (missing contrast) — caught only during Phase 5 implementation, after two review gates had already passed it. |
| D5 | Traceability | 5 | Full `R#`/`E#` → `C#` → `T#` chain, checked in both directions; no orphan component, no task naming a requirement the spec lacks. |
| D6 | Gate discovery | 5 | Real commands read from `package.json`; baseline captured on the untouched tree (1 pre-existing lint warning, 1 pre-existing skipped test, clean typecheck/format); Base (`main`@SHA) and Integration recorded and later re-confirmed with `git merge-base` at Phase 7. |
| D7 | Code quality | 5 | Clean diff matching the fixture's existing conventions (JSDoc style, 2-space, single quotes); all four gates plus the new benchmark script actually executed and passed; zero hits on the Phase 7 clean-code sweep. |
| D8 | Review stops | 4 | Stopped at every required gate (spec, plan, tasks, the R6 re-approval) with no waiver and no chaining. Docked because the "manual verification accepted as a requirement's evidence" sign-off (core rule 2) has no specified place to be recorded — unlike a data-change or dependency sign-off, which SKILL.md names a specific artifact line for — forcing improvisation each time it was needed (three times: T3, T3-contrast, Phase 7 consolidated). |
| D9 | Documentation | 4 | `docs/admin-user-table.md` accurate against the code; the four `src/lib/` interface examples were actually executed and matched; README/CHANGELOG updated; Operating section correctly omitted per its own conditional. Docked because "every example runs as written" (references/verification.md step 7) has no exception for a project with no way to execute JSX, unlike the parallel R#/E# manual-verification exception — the `<UsersTable />` snippets could only be checked statically. |
| D10 | Verification | 5 | Full Phase 7 procedure run for real: every `R#`/`E#` got a verdict with real evidence (code path + passing test, or a disclosed manual trace with recorded sign-off); gates re-run and diffed against baseline; dead-code sweep with a real inventory (`git diff <Base>...HEAD`); integration state checked via `git merge-base`; `SC1` walked; report appended in the reference's exact format. |
| D11 | Scope fidelity | 5 | Diff is exactly the spec's `R#`/`E#`, nothing more; Non-goals held (no pagination/export/edit); the one shortcut found (E4 reachable only via manual trace) was declared as a dated Decisions entry, not shipped silently. |
| D12 | Cost | 3 | No thrashing or re-reading `SKILL.md` — read once, quoted correctly throughout. But all 6 references were read upfront in one batch rather than "when first needed" as the skill itself instructs, and the Phase 5 task-claim/release ceremony (a commit to claim, a separate commit to complete — for every one of 6 tasks) doubled the commit count in a run with exactly one agent and one branch, i.e. zero collision risk to protect against. |

**Total: 54/60**

## Friction log

### 1. Where: SKILL.md Phase 2 ("If the user says 'you decide', record the decision *and its rationale* in the spec's Decisions section") vs. references/writing-specs.md → Clarification questions ("Record every answer in the Decisions section — including 'user said you decide' plus what you decided and why")

- **What went wrong**: SKILL.md's own Phase 2 bullet only requires a Decisions entry for "you decide" answers. Its reference file states the broader rule that *every* clarification answer goes to Decisions, including ones the user answered directly (row count, WCAG level, viewport width). Followed as literally as either document to spec.md would produce a materially different (shorter vs. fuller) Decisions section.
- **Why**: The core file states a narrower rule than the reference it points to for "detailed guidance," with no cross-reference flagging the broader scope. An agent that reads only SKILL.md (the reference is optional, loaded "on demand") would under-record; one that loads the reference gets a contradiction to resolve, not an elaboration.
- **Fix shape**: Make SKILL.md's Phase 2 bullet match the reference verbatim ("record every answer"), or have the reference explicitly say it's expanding, not restating, the core rule.

### 2. Where: SKILL.md Phase 1 bullet 4 / references/writing-specs.md → Operational criteria (Accessibility: "the standard and level this project already commits to... plus keyboard reach, focus behavior on navigation, contrast, and how errors are announced")

- **What went wrong**: R6 was drafted, presented, and approved twice (spec approval, then again unchanged at plan approval) naming only "WCAG 2.1 AA" with Given/When/Then covering keyboard + focus + `aria-sort` — missing the checklist's own "contrast" item. It was caught only during Phase 5's manual accessibility check, forcing a mid-implementation spec amendment and a second approval round.
- **Why**: The four accessibility sub-items live as one clause in a paragraph inside a reference file, not as a checklist the agent is forced to walk item-by-item before Phase 2's exit criteria ("zero markers left"). Nothing in Phase 1/2 requires enumerating the sub-items against the requirement text before presenting it, so a requirement can look complete (it cites the standard) while covering only part of what the standard implies.
- **Fix shape**: Turn writing-specs.md's accessibility line into an explicit checkbox list (like the "Operational criteria" bullets already are) so a requirement citing an accessibility standard visibly needs one acceptance line per item, not one line for the standard's name.

### 3. Where: SKILL.md core rule 2 ("accepting a manual verification as a requirement's only evidence always need[s] explicit sign-off") and references/verification.md step 2 (same exception)

- **What went wrong**: Both places require an explicit sign-off every time the manual-verification exception is used as a requirement's evidence, but neither says *where* that sign-off is recorded. Contrast with the data-change and dependency sign-offs, which SKILL.md and their reference files explicitly route to "a dated Decisions entry in spec.md." Here, nothing says whether it's a Decisions entry, a tasks.md note, or just a citation on the Phase 7 report — so three separate instances (T3's R4/R6 check, the contrast addendum, the Phase 7 consolidated sign-off) each needed an improvised recording convention.
- **Why**: The rule specifies *that* sign-off is required and *what it covers* (a standing waiver doesn't), but not *where it lives* — an omission other sign-off types in the same document don't have.
- **Fix shape**: Add one clause to core rule 2 or verification.md step 2: "record it as a dated Decisions entry in spec.md, cited on the Phase 7 report," matching the pattern already used for data-change and dependency sign-offs.

### 4. Where: SKILL.md Phase 5, task-claim mechanic ("claim it by setting Owner to who ... plus today's date, and commit that claim before writing code. Release it ... on completion")

- **What went wrong**: Executed literally, this doubled the commit count for a single-agent, single-branch run (a claim commit and a completion commit for every one of the 6 tasks — 12 commits with zero informational content beyond "still just me"). references/team-and-review.md explicitly gives the Owner/Sign-off/Tracking defaults a "a solo developer on a repo with no policy ... loses nothing" escape hatch; Phase 5's claim/release mechanic, which exists to prevent exactly the collision team-and-review.md is scoping around, has no equivalent.
- **Why**: The rule is written for the general (possibly multi-agent, possibly multi-branch) case and never narrows for the common single-session case the way its sibling reference does elsewhere in the same document.
- **Fix shape**: Let the claim/release commit be skipped (Owner can still be set in the same commit as the task's own work) when Phase 3's overlap scan found no other active branch/session for this slug — i.e., extend team-and-review.md's existing solo-case default to Phase 5's claim mechanic.

### 5. Where: references/verification.md step 7 ("its examples run as written [...] verified, not imagined") vs. step 2's manual-verification exception (which exists precisely for "the project has no [runnable tool] ... in this environment")

- **What went wrong**: Two of the doc page's usage examples are JSX (`<UsersTable />`, `<UsersTable rowCount={50} />`) in a project with no way to execute JSX (the same constraint step 2 already has an exception for, for requirement verification). Step 7 has no equivalent exception, so those two examples could only be checked statically (import path, prop name) rather than run — a gap the report had to disclose without any textual permission to do so.
- **Why**: The two rules address the identical underlying limitation (no JSX execution in this environment) but only one of them anticipates it; the doc-verification rule was seemingly written assuming code examples are always executable if the described behavior is.
- **Fix shape**: Extend step 2's manual-verification exception (or add a one-line pointer) to cover doc-example verification in step 7, so a disclosed static check is the documented fallback instead of an improvised one.

### 6. Where: SKILL.md → Adaptive depth ("State the chosen depth in one line before starting")

- **What went wrong**: The depth classification was correct and was recorded in `spec.md`'s Decisions section, but it was never delivered as a standalone statement preceding Phase 1's output — it arrived bundled inside the first artifact itself, after the fact rather than before it.
- **Why**: The rule names *what* must be said but not *when relative to what other output* — "before starting" is satisfied technically (before the spec is approved) even by embedding it in the spec draft itself, which defeats the rule's own stated purpose ("the user's chance to object" before work is sunk into an artifact).
- **Fix shape**: Add "as a message on its own, before creating or editing any artifact" to close the gap between "technically first" and "actually first."

### 7. Where: SKILL.md Phase 3, Measurements line ("the value the untouched tree shows today ... and the conditions that value was measured under") and references/writing-specs.md's measured-criteria rule ("under the conditions the number actually means")

- **What went wrong**: The user's performance bar was "p95 < 150ms on a mid-range laptop." Nothing in the skill gives an agent a way to determine whether its own execution environment qualifies as that hardware class, and the rule's own remedy (move it to an `SC#` if conditions can't be reproduced) would have thrown away a genuinely measurable, valuable requirement over an unanswerable hardware-tier question. The only way through was to quietly reword the requirement's own condition clause to name the actual (unverified-tier) machine instead of asserting equivalence to "mid-range."
- **Why**: The rule is rigorous about the *comparison* (measured value vs. threshold, under stated conditions) but silent on what an agent should do when the condition itself (a colloquial hardware-class description) is unfalsifiable from inside the environment doing the measuring.
- **Fix shape**: Add a line: when the stated condition names a hardware/environment class the agent cannot verify, record the actual environment honestly and flag the gap as a Decisions entry rather than blocking or silently asserting equivalence — i.e. give this specific, probably-common case its own named escape hatch instead of leaving it to the general "can't reproduce → SC#" fallback, which would sacrifice a requirement that was in fact measurable.

## Timing / cost notes

- `SKILL.md` was read once, in full, at the start of the run and never re-read — every subsequent citation was a direct quote from that single read, with no confusion requiring a return trip.
- All six references (`writing-specs.md`, `clean-code.md`, `verification.md`, `team-and-review.md`, `data-and-delivery.md`, `dependencies.md`) and all four `assets/*-template.md` files were read once each, up front, in one batch before Phase 1 — this is *heavier* than the skill's own "load it when you first need it" guidance calls for (a real single-pass agent would more likely load `writing-specs.md` at Phase 1, `clean-code.md` at Phase 5, `verification.md` at Phase 7, etc.), so this run's time-to-first-artifact is not a clean measurement of the skill's natural pacing.
- No thrashing, stalls, or contradicted-and-redone work inside a single phase. The one real backtrack (R6's contrast gap, friction #2) was a clean, single-pass amendment, not a spiral.
- Heaviest point in the run: reconciling `writing-specs.md`'s accessibility checklist, `verification.md`'s manual-verification exception, and `clean-code.md`'s dead-code-sweep/speculative-generality checks *simultaneously* for the R4/R6/E4 cluster — three reference files' rules all bearing on one implementation decision (the `rowCount` prop and its one-caller reachability) at once. Everything else (gate discovery, task execution, Phase 7's mechanical steps) moved in a straight line.
