# Changelog

All notable changes to the `spec-driven` skill.

## 3.1.0

Wave B audit: the red-team pass plus the three scenarios never run before (spec drift, data migration, mid-flight change request). v3.0.0 hardened the evidence half of Phase 7 and left the gate half on assertion; this release evidences the gate half, gives a real data migration a door into Phase 7, and stops the exemplar modelling the exit its own rule forbids.

**The gate half now cites command output, not adjectives**

- **The Baseline cell carries what the command printed** — enumerated failures or the counts it reported — never an adjective. `clean` is a claim; `84 selected, 0 failed` is a reading, and a cell holding neither was not measured, which voids every verdict that would compare against it.
- **`Attribution:` is a mandatory report line.** Every failure names the base-tree command actually run and what it printed. No `blocked (pre-existing)` and no `blocked (flaky)` verdict exists without it — the two verdicts wave A introduced were satisfiable by typing the attribution, since step 4's control left no artifact anywhere in the report format.
- **`Base: — no resolvable history` cites its check** (`git rev-parse --is-shallow-repository → true`), the same discipline: it is the cheapest path through Phase 7 and it disables four rules at once.
- **A citation quotes the runner's own line for the cited case** (`1 passed` for that node id). The honest path and the cheap one now cost the same: mis-citing a test no longer satisfies the contract's shape.
- **The negative control's escape is falsifiable** — "cannot be stubbed" must name the compile-time construct that makes it impossible — and it has a path where the only evidence is an approved manual check: the same trace, run with the behavior reverted.

**A migration has a sanctioned door into Phase 7**

- **A fourth task state, `- [!] Blocked — YYYY-MM-DD, <what the user must do>`**, for work that is required, in scope, and executable only by the user. Exempt from Phase 7's entry condition the way a `pipeline-only` gate is exempt from a local baseline; still open work for Resuming work's triage; and it qualifies the terminal status the way an unfinished rollout stage does.
- **A verdict that fits it**: **blocked (execution pending)** — implementation complete and evidenced against an approved stand-in, the real run pending. `partially met` ("missing edge case, missing test") described something else and told reviewers the code was unfinished.
- **The Stored-data Target checklist answers "no rehearsal environment exists at all"** — the fourth form, stated rather than assumed away — and the Delivery checklist reads in the register of a one-time data change instead of requiring a flag-gated translation.

**Sign-off, silence, and the waiver carve-out**

- **`— accepted limitation` carries a signer** (`Decisions YYYY-MM-DD, accepted by <who>`), like `deferred`'s owner. It was the only sign-off row with no approver in its recorded form, and it confers permanent immunity from re-filing.
- **Silence at Phase 7 is defined**: the report block reads `Converged: no — awaiting <the decision>`. The old rule ("leave its Status `draft`") is incoherent where every artifact is already `approved`.
- **`waived` joined core rule 2's table**, as did running any data-change command — reversible ones included — against a shared, staging, or production datastore.
- **Phase 7's four-item parenthetical is deleted** and points at the table unenumerated; so is the false claim that no rule elsewhere repeats the carve-out, which its own file disproved.

**Exemplars stop teaching the wrong exit**

- **The canonical report reads `Converged: no — coverage gate pending (step 9)`.** It converged over an unrun gate, fifteen lines below the rule forbidding exactly that — and exemplars are what get copied.
- **The executed-count guard covers every gate, not just the test gate**: a command that errored, crashed, or collected nothing is not a passed gate whatever its failure count.

**Audit mode**

- Neither `blocked` verdict is available (step 4 never runs, so every cause is outside a change set by construction); the path set is proposed and **user-confirmed** before the inventory is built, since a spec names behavior and never paths; the scope-of-analysis line attaches to any `unreached` finding; and the mode has a required output shape with `Scope of analysis:` and `Not run:`.

**Judgment thresholds that all resolved toward "no finding"**

- **Extraction-for-testability is capped**: it licenses the extraction, not the interface, the options, the generics, or the injection point around it. Wave A's version, against a Phase 5 that mandates a test for everything, made speculative generality unfileable.
- **The duplication threshold is read decision-first**, the broader clause before the line count.
- **`Clean-code:` carries a `close calls:` sub-field**, so "none" and "none recorded" stop looking identical.

**Findings from the three new runs**

- The **claim commit** has its own line in Phase 5; buried mid-paragraph among overlap-scan content, it was being dropped outright.
- **The entry mode is stated in one line** — Phase-7-only, Resuming work, or Audit mode — the way depth is for new work.
- **Review feedback reconciles Integration** against an incoming review identifier before filing its Decisions entry.
- **"Confirming with the user first" has a shape**: name the task and what it changes; that turn is the redirect; a feature-level "continue" is not the naming.
- **The Status reset is stated generally** — every artifact a change request amends stays `in-review` until sign-off, whatever Status it held — not only for the `implemented` case.
- **A stop is written down for information arriving mid-task**, not only for self-discovered errors.
- **A loose reference matching exactly one open-work spec resumes it directly.**

**Budget**

SKILL.md is 7,071 words, one under v3.0.0's 7,072: every addition above was paid for by deleting a restatement of a reference the same phase already loads. Phase 1's opening three acts moved to `writing-specs.md` → Starting the spec, the declared-shortcut rule to `clean-code.md` → Declared shortcuts, and the monorepo gate-row rule to `verification.md` → Recording gates.

## 3.0.0

Wave A review: five advisors and four real runs. The workflow now declines itself cheaply, survives a session with nobody answering, and converges on evidence rather than on citations.

**Activation (breaking)**

- **`description` rewritten.** It gained a size gate ("worth a written requirement — a reviewer could answer 'done or not done?' about it") and an explicit exclusion list (a lone dependency add or version bump, a one-file fix, a rename, formatting, or a request that already says what to build and how). It gained the triggers that fired nothing: **resuming an in-flight feature**, **a bug fix that changes behavior**, **porting or rewriting a module**. It lost `asks to plan before implementing` (which collided with the host's own planning mode), `adding or upgrading a dependency` (now an exclusion), and two of the three scope-cut phrasings, all of which only ever arrive after the skill is loaded.
- **Phase 7 → Audit mode** implements what the description promised: with a `spec.md` but no `plan.md`/`tasks.md`, walk the requirements for evidence, build the inventory from git over the paths they name, report the verdict table — file no `G#`, append no report, set no Status.

**Nobody is answering**

- **Core rule 2 gained "If no one is answering."** A non-interactive session (subagent, `-p`, CI, scheduled agent) or an unanswered question writes the artifact, leaves it `draft`, states in one line what would have been asked, and stops. Silence grants no approval.
- **The waiver's scope is stated once**, in core rule 2: it covers the phase review stops and Phase 7's gap approval, and never a row of the sign-off table. The twelve scattered "a standing waiver does not cover it" clauses across the references are deleted — the table is the one list.
- **Phase 5's "the spec is wrong" stop is written down before it is asked** — a dated Decisions entry or the task's **Notes** — so a session that ends unanswered leaves the stop on disk.

**Convergence can no longer exit green with the gates red**

- **A gate failure classified `new` is a gap** (`verification.md` step 4) and blocks exit, whether or not any `R#` covers the code it points at. The convergence loop's exit test now names the gates and the docs.
- **The citation contract** (step 2): Evidence names the **test case** and the **assertion** that encodes the criterion, and the clause each answers — never a bare file path. A test that exercises the subject but cannot observe the state the criterion is about does not encode it. `unchanged from pass 1` is void: every pass re-cites and re-runs. Requirements in the **Minimum shippable** set carry a negative control — the cited assertion must be shown to fail with the behavior stubbed out.
- **Two new verdicts**, `blocked (pre-existing)` and `blocked (flaky)`, plus a precedence line: spec drift outranks *partially met*; a failure attributed outside the change set is never *not met*.
- **A stand-in is tied or accepted in Phase 3**, not capped at Phase 7: an approved untied stand-in on the plan's **Dependencies** line *is* evidence.
- **A gap noticed mid-walk is reported, not fixed on the spot.**

**The report block is a record, not a summary**

- **Written as you go**: opened at step 1 with `Change set: <SHA>` and `Converged: no — in progress (step N)`, appended row by row, closed at step 9. A pass that runs out of context leaves its verdicts on disk and resumes at the step the block names. A change set too large for one pass is verified in slices, one block each, converging on the union.
- **Every labelled line is always present**; write `none` where there is nothing to report. A new `Coverage:` line reports the spec's surfaces, sensitive-ground and accessibility walks, so a skipped item is visible.

**Degraded environments**

- **`Base` has three forms**, and the plan says which: a dedicated feature branch (merge-base test), slug-prefixed commits on a shared branch (ancestor test — the merge-base test can never fire there), and `— no resolvable history` for no VCS, no commits, or a shallow clone, which retires the phantom-rebase diagnosis a grafted SHA produced. Every rule reading **Base** is then skipped and says so.
- **The base-tree control has an escape**: where the tree cannot be reverted, or another session's uncommitted work is present, skip it and report the failure `unattributed` — never `git stash` a tree you did not author. Baselines measured beside someone else's uncommitted work are recorded `provisional`.
- **A crashed claim is not a held one**: an **Owner** naming this session's own branch or user, on an unchecked task with no completion note, is re-run and continued — never waited out for 7 days.
- **Configuration and infrastructure** got a surfaces row, an evidence exception, and a step-6 reachability exemption, so a declarative feature can converge instead of being filed for deletion.
- **A repo that already holds a requirements document** (RFC, PRD, design doc, the ticket **Tracking** points at) is read first and the `R#`/`E#` derived from it — the spec restates it and never re-decides it.

**Proportionality**

- **Small skips Discovery**: **Owner**/**Sign-off**/**Tracking** take their documented defaults unless a `CODEOWNERS` entry covers a touched path, and the overlap scan is `ls specs/` — branch enumeration starts at Standard.
- **Phase 1 presents the Objective and the open questions first**, before the slug test and Discovery.
- **The Trivial test runs over the request as a whole**: one clause that is at least Small makes the whole request at least Small.
- **A plan omission that changes no component boundary** is amended in place on a one-line confirmation, instead of triggering the same full re-planning cycle as a wrong architecture.

**Recurrence rule adopted** — no sentence in `SKILL.md` restates content from a reference the same phase loads unconditionally. Deleted under it, with nothing put in their place: Phase 7's restatement of `verification.md`'s procedure and Phase 3's empty gate table (~540 w); `team-and-review.md` → Handoff and Parallel sessions (330 w, their one unique line moved into Phase 5); `clean-code.md` → Quality gates, a third copy that contradicted step 4's baseline (307 w); the open-follow-through paragraph copied at four sites (~200 w); the two "Does this apply?" sections (174 w); `writing-specs.md` → Anti-patterns, three Clarification bullets and the Technique line (~220 w); and three rationale passages in `verification.md`.

**Also**

- `clean-code.md` split into **Gates — mechanical** (grep/AST-answerable) and **Judgment calls**, each with a stated threshold; four unfalsifiable items deleted. Phase 5 records the sweep as `Clean-code: <n> hits / none` on the task's completion note, so an unrun sweep is a blank field.
- **Extracting logic so a criterion becomes testable is a current use**, not speculative generality — the tie-break two runs decided differently.
- **No artifact carries `approved` without having existed as `in-review`** — Phases 3 and 4 gained the guard Phase 1→2 always had.
- `SC#` joins the `R#`/`E#` row of the sign-off table; a sensitive-ground approval also adds its **Sign-off** line row; reopening a task never releases its claim; a `scope.md` row is `done` on the same bar Phase 7 sets **implemented**; `G#` numbering continues across passes; monorepos record one gate row per package; components carry a **Duplicates** line beside **Reuses**; missing artifacts are recovered before the drift check's diagnostic pass runs.

## 2.2.0

Consistency pass over the 2.1.0 restructure: every rule that existed in two places now exists in one, and the contradictions a real run surfaced are decided.

**One list per rule**

- **The Sign-off list lives only in core rule 2's table.** The six-item enumerations in `references/team-and-review.md` → Sign-off authority and in `assets/spec-template.md` are gone; both now read "one line per row of core rule 2's table that this feature actually raises". Two rows were added to the table so nothing was lost in the merge: *the spec's own content* and *a sensitive-ground `R#`/`E#`*.
- **The table gained a "Recorded as" column** and lost the blanket "each is recorded as a dated Decisions entry": a deletion gap is recorded on the report's `Dead-code sweep:` line, a test removal on `Tests removed:`, a dependency on the plan's **Dependencies** line. The test row now carries step 4's exception — *unless an `R#` specifies the removal*.
- **`assets/plan-template.md` stopped restating the gate rules.** The baseline-run, read-only-command, `pipeline-only`, and missing-tooling blocks — and the **Measurements** line's demote-the-requirement rule, which contradicted `references/verification.md` — are one-line pointers to `verification.md` → Recording gates. Templates carry fields, not rules.

**Contradictions decided**

- **The Small depth row** now names the full header block (Status, Owner, **Sign-off**, **Tracking**, Last updated) and the full recorded-next-to-tasks set (adding the **Measurements** line and the overlap scan's branch set) — the two lines Phase 2's exit and Phase 5's shortcut rule read were missing from a row that reads as exhaustive.
- **A `pipeline-only` gate with no run keeps the convergence loop open** (`verification.md` step 4); a pending *integration* state does not. Phase 7's "the same shape as a pipeline-only gate" analogy is gone.
- **The claim commit is always its own commit.** 2.1.0's exemption asked the overlap scan a question it cannot answer — it enumerates branches, never sessions — so it is removed from `SKILL.md`, `team-and-review.md`, and `assets/tasks-template.md`.
- **The waiver's gap carve-out widened** from deletions alone to any gap whose resolution appears in core rule 2's table: a deletion, spec drift, a deferral, an accepted limitation.
- **The overlap scan's "run once per session" rule** now states its one exception: Phase 5 re-reads the other branches' `tasks.md` at each claim, because a claim can land after the scan ran.

**New rules**

- **`verification.md` step 2 reconciles the plan's Requirement coverage table** — where a requirement's evidence, or a gap's fix, sits in a component the table does not attribute it to, the row and the component's **Implements** line are amended. The table was previously checked for presence and never for accuracy.
- **CODEOWNERS routing is stated once**, in `team-and-review.md` → Discovery: ownership of a *path* the change touches → the plan's **Integration** line; ownership tied to a *gated item* → the spec's **Sign-off** line. Cross-linked from Sign-off authority, Integration, and the spec template.
- **Enforcement that does not live in the tree** (native branch protection, org policy) is recorded as claimed-not-confirmed or asked about — never reported as *required* from a `CODEOWNERS` entry alone.
- **Phase 3 now asks what will evidence each requirement**, not only what gates the tasks: `verification.md` → Recording gates gained an *Evidence per requirement* item, so the missing-tooling rule fires in Phase 3 instead of surfacing at Phase 7.
- **Open follow-through has a fallback** when the user names neither owner nor date: the spec's **Owner** and the next release or review point, recorded as defaults — or `unowned — revisit at <trigger>`.

## 2.1.0

Restructure of `SKILL.md` for context economy and progressive disclosure. No rule was removed: every rule moved out of `SKILL.md` landed in a named section of a reference file, and kept a trigger in `SKILL.md` saying when to load it.

**`SKILL.md`**

- **Core rule 2** cut to the review-stop rule itself, followed by a two-column table — *Always needs explicit sign-off — a waiver never covers these* — with one row per approval-gated item and the file its rule lives in. The `pending sign-off: <role>` procedure is now one line pointing at `references/team-and-review.md` → Sign-off authority.
- **Adaptive depth** replaced by a `Depth | Test | Artifacts | Phases run | Docs form` table plus three imperative lines. Trivial now reads "no spec, no plan, no tasks — but the change is still gated", with the gate rule immediately after the table. Re-classification, cost overrun, and a user-directed lighter depth moved to `references/writing-specs.md` → Depth.
- **New phase table** at the top of `## Workflow` — `Phase | Input | Output artifact | Status after | Stop?` — including `draft` as the state of a produced-but-unpresented artifact. Phase headings that are review stops now say so.
- **Phase 3's quality-gate rule** reduced to a fillable gate table (`Gate | Command (must be read-only) | Where it runs | Baseline`), the **Base** line's two fields, and one sentence. The baseline run, flaky failures, the rebase test, `pipeline-only` rows, compiled-language type gates, missing tooling, a gate that cannot execute, and the measurement commands moved to `references/verification.md` → Recording gates.
- **The cross-branch overlap scan** moved to `references/team-and-review.md` → Overlap scan, now a single bounded command (`--sort=-committerdate --count=15`, the ~90-day cut applied to the printed date). All call sites now read "run the overlap scan".
- **Inlined tables of contents deleted** at reference link sites — each link now carries its trigger condition and an imperative "read it now". The Data changes / Delivery / Dependencies bullet is three questions with their default answers, then one load instruction.
- **Rules that asked for undiscoverable facts made checkable**: Phase 4 presents the task count and flags any task naming more than 3 files or more than one component as large; a task claim dated more than 7 days ago is stale unless the plan records a different span; cost overrun is read from the artifacts.
- **Resuming work** triages `draft` artifacts alongside `in-review` and `approved`, and re-presents them rather than re-specifying.
- **Phase 2** now records *every* clarification answer in Decisions, matching `references/writing-specs.md`.
- **Phase 5** skips the separate claim commit where the overlap scan found no other active branch or session for the slug.

**References**

- `references/verification.md` — new `## Recording gates` section (Phase 3's gate rules); step 2's manual-verification sign-off is recorded as a dated Decisions entry and cited on the report; step 7's doc-example check gained step 2's non-executable exception.
- `references/team-and-review.md` — new `## Overlap scan` section; the claim-commit and stale-claim rules updated to match `SKILL.md`.
- `references/writing-specs.md` — new `## Depth` section; the Operational criteria accessibility item is now an explicit sub-checklist (keyboard reach, focus behavior, contrast, error announcement) that a requirement citing a standard must cover before it can be presented.
- `assets/tasks-template.md` — claim conventions updated to match.

