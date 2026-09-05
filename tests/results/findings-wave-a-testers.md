# Wave A — tester findings (real runs against v2.2.0)

## S03 — trivial-vs-small boundary — 49/60

**Depth call passed, but only by inference.** The whole request was correctly classified **Small** (not Trivial, not split into two artifacts of different depths) — the scenario's core test. But nothing in SKILL.md states whether "the change" in the Trivial-escape test ("if you could state the change as an `R#` with a Given/When/Then, it is at least Small") means **the whole request or each clause inside it**. Correct behavior required elimination-by-inference, not a stated rule.

**Proportionality — the headline number.** For a 3-line functional diff requested in one sentence: **9 commits (4 of them pure ceremony — the mandatory claim-then-release commits), a 120-line spec artifact, 4 full gate-suite runs = 16 command executions.**

**Abandonment point:** right after the first artifact was presented — a full collapsed spec with header block, R1/R2, non-goals, edge cases, decisions, a 3-task breakdown with gate/Base/Integration/overlap-scan bookkeeping, plus a clarifying question about test tooling — **before any code changed**, for what was pitched as a trivial text-and-disable tweak.

### S03-T1 (high) — the depth-boundary rule is under-specified for mixed-depth requests
Phase 0's split logic only fires at Large. Nothing tells an agent that a sub-Large request bundling a Trivial-shaped clause and a Small-shaped clause must be classified **as one unit at its deepest clause**.
**Fix:** state it in the depth table's Trivial row — the test applies to the request as a whole; one clause that is at least Small makes the request at least Small.

### S03-T2 (high) — Phase 5's junk-code self-review has no forcing function
"Before marking a task done, pass the gates: run the task's verification step **and** every quality gate recorded in the plan …, then self-review the diff against the junk-code checklist" is one compound sentence. **The gates have a concrete artifact (the Quality gates table) forcing evidence; the self-review has none.** All three tasks in this run were marked done after gates alone; `clean-code.md` was not opened until Phase 7's mandatory sweep forced it retroactively — i.e. exactly the "delivered post-writing" timing A7 flagged.
**Fix:** give the self-review an artifact — a per-task `Clean-code: <n> hits / none` line in the completion note, so an unrun sweep is a blank field rather than an unobservable omission.

### S03-T3 (medium-high) — Small's artifact list has no home for the Surfaces / Operational-criteria analysis
Phase 1 requires walking those checklists at **every** depth, but Small's enumerated section list (header, Objective, Requirements, Non-goals, Edge cases, Decisions, Tasks) drops "Users & scenarios" entirely, leaving nowhere canonical to put that analysis. Pairs with A7-F1: the walk already has no verification, and at Small it has no slot either.

### S03-T4 (medium-high) — genuine unflagged rule conflict: "tests are the executable form of the spec" vs. "no speculative generality"
Phase 5's "Write or update tests that encode the task's acceptance criteria — tests are the executable form of the spec" collides with core rule 6 / `clean-code.md`'s "New abstractions need a current — not hypothetical — second use" **exactly when** a component's only untestable part is JSX wiring but its logic could be extracted to a testable pure function purely to dodge that gap. **No tie-breaker exists; two equally defensible runs produce different diffs from the identical spec.**
**Fix:** state which wins — extracting to make a criterion testable is a current use, not speculative generality.

### S03-T5 (medium) — ordering ambiguity inside the collapsed Small draft
Small folds "Phase 3's tooling discovery" into the same draft as Phases 1–2, but nothing sequences it against "never ask for approval while `[NEEDS CLARIFICATION]` markers remain". This run drafted the full gates/tasks content **before** resolving its one marker — which the text neither licenses nor forbids.

### Iteration-2 changes: did they hold?
- Small header block naming **Sign-off** + **Tracking** — **held**.
- Sign-off table's **Recorded as** column — **held**.
- Mandatory claim commit — **held exactly as intended**; a deliberate design choice, and the single largest ceremony cost at this depth (4 of 9 commits).
- Per-requirement evidence check in Phase 3 — **held, and did real work**: it caught the JSX-untestability gap *before* code was written.
- Phase 7 coverage-table reconciliation — **not applicable**: Small has no `plan.md` and no coverage table.

---

## S04 — Large split / Phase 0 — 51/60

### S04-T1 (high) — Phase 3/4 review stops have no checkable precondition, unlike Phase 1→2
`plan.md` and `tasks.md` were written **straight to `Status: approved`** — neither file exists at any commit in `in-review`. Phase 1→2 has a hard guard ("never ask for approval while `[NEEDS CLARIFICATION]` markers remain"); Phases 3 and 4 just say "Stop and get approval", with **nothing an agent can fail to satisfy**. The stop is unobservable after the fact, so the skill's central claim (human review between phases) leaves no trace.
**Fix:** give Phases 3/4 the same shape of guard — the artifact must exist in `in-review` before it can carry `approved`.

### S04-T2 (high) — Phase 7's gap-discovery and gap-approval are one section apart, and nothing interrupts the walk
Mid-walk on E2 the agent noticed a real undertested claim, **wrote the missing test and confirmed it passed** — before reporting any verdict or asking approval, i.e. exactly the report-first → file `G#` → approve → implement sequence `Handling gaps` requires. The instruction to stop lives a full section after the point where the agent's attention is already on the fix.
**Fix:** one sentence in step 2 — "a gap noticed mid-walk is reported, not fixed on the spot."

### S04-T3 (medium-high) — Phase 0 has no `scope-template.md`
Every other phase has one, explicitly linked (spec/plan/tasks/doc). `scope.md`'s shape had to be reverse-engineered from one paragraph of prose, with **no worked example of a `deferred` row** and nothing saying what belongs above the table.
**Observed output:** a `Last updated` line + one context sentence + a 5-column table (`Slug | Responsibility | Depends-on | Rank | Status`) — no header block, since Phase 0 names only `Last updated` for this artifact.

### S04-T4 (medium) — `scope.md`'s `done` vs. `spec.md`'s `implemented` is never reconciled
Phase 7 is explicit that `implemented` requires actual merge into **Base**, not just convergence. Phase 0 never says whether a capability's `done` carries the same bar. The agent inferred yes from "as it lands" — inference, not a stated rule.

### S04-T5 (medium) — adding an `SC#` mid-Phase-3 has no home in core rule 2's sign-off table
Discovering that nodemailer could not be evidenced offline led (per `verification.md`) to moving half of R1/R2 into a **new SC2 on an already-`approved` spec**. The table claims to be "the one list" for approval-gated edits and has a row for `R#`/`E#` changes — **none for `SC#`**. The agent proceeded by analogy; the skill never licenses it. (Compounds A7-F7: Phase 3 discoveries routinely demand spec-level edits after the spec closed.)

### Phase 0 specifics
**Rank** was a plain 1–4 sequence that in this run **exactly matched what dependencies alone already forced** — its actual purpose (breaking a tie when two capabilities are simultaneously unblocked) was never exercised, because the scenario stopped after capability #1 landed, right at the point where two capabilities become unblocked at once.
**Dependency order** was honored but enforced **only by discipline in reading the table** — nothing mechanical stops a future session from jumping ahead.

---

## S05 — resuming work with a broken artifact set — 49/60

**Resume checks — what actually ran:** all five ran, in the correct order. Work-present (cheap, `git log --all`) → drift (found 3 non-prefixed commits, correctly triggered Phase 7 — which then could not run, see T1) → artifact cross-check (bidirectional, clean) → missing-artifact recovery for `plan.md` (clean git-history restore) → stale-claim handling on T2 (cheap once sequenced right, but **accidentally front-run at step 1** and redone).

### S05-T1 (high) — the drift check and missing-artifact recovery are circular, and nothing says so
The drift check's remedy is "run Phase 7 first as a diagnostic pass". Here one of the newer commits **had deleted `plan.md`** — and Phase 7 needs `plan.md` (Quality gates, **Base** line) to run at all. The five Resuming-work bullets read as a fixed top-to-bottom checklist, but **step 2's remedy depends on step 4's output, three positions later.**
**Fix:** state the dependency — recover missing artifacts before running the diagnostic pass the drift check orders, or say the pass runs in a reduced form when `plan.md` is absent.

### S05-T2 (high) — reopening a checked task and releasing its stale claim get bundled by a natural reading, but must not be
Handoff says reopen `- [x] Done` → `- [ ] Done` on absent work; a separate rule says **ask the user** before taking over a >7-day-old claim. The agent did both in one edit — **clearing `Owner` before asking** — and had to catch and revert it. Nothing states these are two actions with a required gap between them.
**Fix:** one clause — reopening a task never releases its claim; the claim is released only by its owner or by the user's answer.

### S05-T3 (medium-high) — the sensitive-ground row never says to update the **Sign-off** line
Core rule 2's table records a sensitive-ground `R#`/`E#` as "a dated Decisions entry in `spec.md`" and is **silent on also adding a Sign-off-line row** — even though the sibling feature in the same fixture had already established that convention. The agent added E4 (authentication) with a proper Decisions entry and missed the Sign-off line for several commits, catching it only while writing the scorecard. (Directly compounds A7-F1 and A6's finding that the walk has no verification.)

### S05-T4 (medium-high) — the rebase-detection check is structurally degenerate under the skill's own alternative topology
`verification.md` checks `git merge-base HEAD <Base branch>` against a recorded SHA to detect a rebase. Under Phase 5's **sanctioned** "slug-prefixed commits on a shared branch" convention (used here — no dedicated feature branch), **`HEAD` *is* the Base branch**, so the check can never fire. The skill offers two topologies and the detection only works for one. (Pairs with A5-F1: the other topology's failure mode is the shallow-clone false positive.)

### S05-T5 (medium) — "stop if the plan is wrong" does not scale to the size of the defect
Discovering that the plan's C3 component never named a needed one-line helper (`getTask`) technically triggers "**stop** — go back to Phase 3 … a standing waiver does not cover this" — **the same instruction a wrong architecture triggers**. The agent folded it into a one-line confirmation instead of a full re-planning cycle: a judgment call the text gives no anchor for.
**Fix:** distinguish a plan omission that changes no component boundary (amend in place, note it) from one that changes the architecture (back to Phase 3).

---

## S06 — standing waiver + a11y form — 49/60

### Waiver behavior — seven gated items came up
- **Correctly NOT covered** (agent stopped): spec-content approval (4 clarification questions), the sensitive-ground Password sign-off (R14), and the manual-verification-as-evidence sign-off (JSX-tooling decline) — all three recorded as separate dated Decisions entries.
- **Correctly covered by the waiver:** Phase 7 gap implementation (G1, G2 without a separate stop, per the table's carve-out). Separately, the agent **correctly refused to push/merge to `main`** on the waiver's authority, leaving `Integration: not opened yet`, Status `approved`.
- **Never triggered:** a new dependency — reuse-first plus the fixture's zero-dependency convention plus no-npm-install made hand-rolling validators the obviously correct call. A finding about the scenario/fixture pairing, not the skill.
- **Wrongly swallowed:** discovering mid-implementation that `Button.jsx` needed a `type` prop (its hardcoded `type="button"` would have silently blocked form submission) is exactly the case Phase 5 names as never covered ("implementation reveals the plan is wrong … **stop**"). **The plan was quietly amended and work continued without the required re-approval stop.**

### S06-T1 (HIGHEST VALUE — empirical confirmation of A4-F2) — a passing test hides a real bug when its scope is narrower than the requirement
E3 was reported **met on two consecutive Phase 7 passes**, solely on `test/userForm.test.js`'s pure-function coverage — **which never renders `UserForm` and cannot see its `success` state.** The rendered component had a real bug: a stale success banner surviving a failed resubmission. It surfaced only on a third, adversarial re-read.
This is A4-F2's "evidence is checked for existence and execution, never for sufficiency" caught in the act, with a concrete escaped defect rather than a hypothetical.
**Fix:** step 2 must require confirming the cited test's **scope reaches every clause of the requirement** — not merely that some test exists, executed and passed.

### S06-T2 (high) — Phase 5's "the plan is wrong, stop" rule has no size threshold
Independently found by S05-T5 as well. Discovering `Button.jsx` needed a small additive prop technically triggers "the plan is wrong … a standing waiver does not cover this"; the agent read it as a trivial refinement and continued. **The rule prescribes the same remedy — full stop, re-approval — for a one-file omission as for a wrong architecture.**
**Fix:** give it a size test in the shape of Phase 4's magnitude line — a gap confined to *how* an approved component is built (no new `R#`/`E#`, no changed **Implements**, no new component) is recorded and continued; anything else stops.

### S06-T3 (medium-high) — the Measurement/Evidence bullets don't separate a numeric sub-criterion from a rendering-dependent cluster
R12 (contrast) was lumped in with the genuinely rendering-dependent R6–R11/R13/R14/E4 under the manual-verification exception at Phase 3 — when it is **pure color math needing no rendering at all**. Caught only at Phase 7, via a real rerunnable script that could have existed from the start.
**Fix:** prompt, per numeric criterion inside an accessibility cluster, whether it is separately computable.

### S06-T4 (medium) — `Last updated` has no guard against becoming a changelog
When the plan was amended mid-implementation the date line was rewritten with a parenthetical rationale instead of staying a bare date. Every rule that parses it (`git log -1 --format=%as` comparisons, the drift check) expects a date.
**Fix:** state that only the date belongs there.

### S06-T5 (medium — a CONFIRMED IMPROVEMENT, recorded deliberately)
Core rule 2's sign-off table, used purely as a **lookup**, now works cleanly: all three never-waived items this feature raised were recorded exactly per the **Recorded as** column with no synthesis needed. This is a genuine improvement over runs 01/02, whose difficulty was with the table's *routing* questions (CODEOWNERS ambiguity), not its lookup.

---

## S07 — Stripe integration / dependencies.md deep test — 52/60

### S07-T1 (high) — Cost & limits is scoped to "Adding a new dependency", but the need for it is independent of that
This feature's correct, reuse-first-driven decision was **not to add a new dependency at all** (axios already does the HTTP work). Under that path nothing points at **Cost & limits** — even though the actual need for it (Stripe is metered, rate-limited, credentialed) has nothing to do with whether a new library enters. The checklist **conflates "a new npm package enters" with "a metered/credentialed external service gets called."**
**Fix:** move Cost & limits out from under "Adding a new dependency" into its own item, or cross-reference it under "Calling an external service at runtime", keyed to *the service is metered / rate-limited / credentialed* rather than to *a new dependency was added*.

### S07-T2 (high) — Phase 1 fills the **Sign-off** line before three of its rows are discoverable
Phase 1 fills **Sign-off** before Phase 3 exists, but three of core rule 2's rows — a new dependency, a data change, a delivery step — are **only discoverable during Phase 3**. The agent's first draft speculatively pre-listed a hedged dependency row, then self-corrected on re-reading. **Nothing instructs coming back to amend the Sign-off line once Phase 3 raises a new row** — the agent inferred it. (Same root as S05-T3, from the opposite direction.)
**Fix:** one line on Phase 3's Dependencies / Data changes / Delivery bullets — "if this raises a core-rule-2 row not already on the spec's **Sign-off** line, add it there now and bump `Last updated`."

### S07-T3 (high — structural, found by no one else) — the task vocabulary has no state for "required, in-scope, but only the user can execute it"
Phase 7's entry condition is "every task is done, waived, or deferred". But the real `npm install stripe` (needs network) and setting three production secrets (needs a real environment) **can never become `Done`**, are not declined (`Waived`), and are not cut from scope (`Deferred` means "not in this change set yet" — these very much are). This is exactly the situation the skill's own dependency and delivery rules **repeatedly create**, since both insist such steps are the user's own.
**Fix:** a fourth checkbox state — `- [!] Blocked — <what the user must do>` — exempted from the done/waived/deferred gate the way a `pipeline-only` gate is exempted from needing a local baseline.

### S07-T4 (medium-high) — nothing anticipates the install tool itself being unrunnable
"never a manifest edit without the lockfile update the project's own tooling produces" assumes the tooling can run. Nothing covers an environment where **npm itself needs network and can never run in-session** — as opposed to a gate that is merely missing. The agent had to invent the answer by analogy to the delivery-step stop-and-ask pattern.
**Fix:** "where the project's install tool needs network or credentials this environment lacks, name the exact command and hand it to the user as their own step — **never fabricate the lockfile entry it would have produced**."

### S07-T5 (medium — real, and disclosed as partly environmental) — "Tests are code" collides with directory-based test discovery
Extracting duplicated test helpers (`signToken`/`fakeRes`) into a shared `test/helpers.ts` — the textbook clean-code fix — made `node --test`'s directory-based discovery report the helper module as a **spurious, always-green phantom test**. The agent reverted to small, disclosed duplication.
**Fix:** caveat on "Tests are code" — a shared test helper is still subject to the project's own test-discovery rules; for a runner that treats every file under `test/` as a test, place shared helpers outside that directory or accept small, disclosed duplication.

### Dependency checklist — item by item, offline
| Item | Answerable offline? | What was written |
|---|---|---|
| Intake | Yes | Found `axios` + the `slack.ts` pattern; presented as an explicit A/B choice; reason recorded |
| How it enters | **No** | Manifest/lockfile untouched; target version recorded as unverified; the real `npm install` handed to the user as its own task |
| License | Partial | MIT stated from general knowledge, **not network-verified**; the repo's own private/unpublished status fully checked |
| Maintenance | **No** | Explicitly recorded as unobtainable offline; filed as a Risk |
| Weight & install-time behavior | **No** | Recorded as unknown until a real install; expectation stated and flagged unconfirmed |
| Cost & limits | Yes | Reasoned fully despite no new library (see T1 on where this lives structurally) |
| Contract version | Yes | Stripe API `2023-10-16` set explicitly; correctly found no forced end-of-support date |
| Stood in for by | Yes | Hand-written fake, explicitly disclosed; **correctly capped affected requirements at partially met** — i.e. A4-F4's predicted cost was paid in a real run |
| Failure behavior | Yes | E3/E5/E6/E7 mapped to real code + (after a Phase 7 fix) real tests |
| Blast radius / Why now / Removal owner | N/A | Correctly stated N/A |
