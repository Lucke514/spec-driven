# Wave B — v3.0.0 audit

Six agents were launched; all six died on a session limit. The mechanical half (regression
verification, seam check, budget measurement, escape-hatch review) was completed directly
instead and is recorded here. The three tester runs (S08 spec-drift, S09 migration,
S10 change-request) and the full red-team pass did NOT run and remain open.

## B8 — regression: did wave A's fixes land? (verified against the current text, not the report)

| Finding | Verdict | Evidence |
|---|---|---|
| A4-F1 — a `new` gate failure must be a gap that blocks exit | **landed** | verification.md:58 "A failure classified `new` is a gap, **whichever gate found it and whether or not any `R#` covers the code it points at**: file a `G#` over it, and it blocks exit exactly like a failed requirement." Exit condition at :106 now reads "**and** the gates show no new or unattributed failures against the recorded baseline, and the docs are accurate" |
| A4-F2 — citation contract + no carry-forward | **landed, and stronger than specified** | verification.md:30 requires "the **test case** and the **assertion** … and the criterion clause each one answers", plus S06's live finding folded in verbatim: "a test that exercises the subject but cannot observe the state the criterion is about — it never renders the component, never reads the row, never inspects the response body — does not encode it, whatever it asserts." Negative control for the Minimum shippable set at :32. Exemplar row rewritten to `R1 \| met \| login.test.ts::"locks after 5 failed attempts" — asserts 429 + lockUntil set, covering both clauses; negative control: passes → fails with the counter stubbed` |
| A3-F2 — "If no one is answering" | **landed** | SKILL.md:21, incl. "Silence is not a waiver: it grants no approval, and no work a stop gates starts on it." |
| A3-F2 — 12 scattered "a standing waiver does not cover" clauses collapsed to one list | **landed** | count across SKILL.md + all six references: **1** (core rule 2 itself), was 12 |
| A5-F1 — three `Base` forms | **landed** | verification.md:15, incl. the shallow-clone guard "A shallow clone must not record a grafted SHA: it makes every later pass diagnose a phantom rebase" and the explicit list of the four downstream rules that are then skipped |
| A4-F3 — two `blocked` verdicts + precedence | **landed** | verification.md:48–49; flaky row carries the right guard — "introduced flakiness is *not met*, never this" |
| A4-F6 — `Change set:` / `Converged:` | **landed** | report format; :93 makes invalidation checkable — "which its `Change set:` SHA makes checkable" |
| A6-F2 — Duplicates read at step 6 | **landed** | verification.md:89, and a declared duplication is not re-filed but stays visible on the `Dead-code sweep:` line |

### Cross-agent seams — all seven contract names resolve
`Evidence per requirement`, `Duplicates`, `Task span`, `Verification report`, `Signal`, `Read at`, `Emitted by` all exist in `assets/` and are cited from `SKILL.md`/`references/`. Nothing dangles.
**The seam tech-A flagged as possibly open is closed**: tech-B added the `C#`/`T#`/`G#` stability lines independently, in all three templates (`spec-template.md:29`, `tasks-template.md:3`, `plan-template.md:42`), and `verification.md:98` carries the `G#`-across-passes half. The two agents converged without coordinating.
Gate table is `| Gate | Command | Where | Baseline |` and Phase 3 says "one gate row per package — gate kind plus package": consistent, package goes in the Gate cell.

## B9 — the budget, measured

### Load per depth (words actually read, unconditional loads only)

| Depth | Words | ≈ tokens | Composition |
|---|---|---|---|
| **Trivial** | **7,801** | ~10.5k | SKILL.md + clean-code |
| **Small** | **17,538** | ~23.7k | + writing-specs, verification, spec-template, doc-template |
| **Standard** | **20,811** | ~28.1k | + team-and-review, plan-template, tasks-template |
| **Large** | 21,025 | ~28.4k | + scope-template |
| conditional | +1,286 / +1,107 | | data-and-delivery / dependencies, only when non-default |

Small improved: A3-F4 measured **19,327** before this pass, now **17,538** — the Discovery and branch-scan relief for Small landed (`SKILL.md:63`, `:106`) and is worth ~1,800 words.
**Trivial is the indictment: 7,801 words to conclude the skill should do nothing.**

### The irreducible core — SKILL.md by section

| Section | Words | Resident at every moment? |
|---|---|---|
| frontmatter + intro | 264 | yes |
| Core rules | 1,151 | yes |
| Adaptive depth | 671 | yes |
| Workflow overview table | 225 | yes |
| Templates list | 27 | yes |
| **resident subtotal** | **2,338** | |
| Phase 0 | 187 | only at Large |
| Phase 1 | 454 | one phase |
| Phase 2 | 103 | one phase |
| Phase 3 | 727 | one phase |
| Phase 4 | 178 | one phase |
| Phase 5 | 745 | one phase |
| Phase 6 | 241 | one phase |
| Phase 7 | 343 | one phase |
| Change requests mid-flight | 477 | event-driven |
| Resuming work | 1,202 | session start on an existing feature only |
| **non-resident subtotal** | **4,657 (66%)** | |

**Verdict: this is a packaging failure, not a content problem.** Two-thirds of the always-loaded
file is needed at exactly one moment. The workflow is strictly ordered, which makes this unusually
tractable — a phase's content can live in `references/phase-N.md` loaded at phase entry, the way
`verification.md` already is for Phase 7 (which is why Phase 7's own section is the *smallest*
of the eight at 343 words: it was already converted, in iteration 1).

**Proposal — the same conversion, applied to the other seven phases:**
- `SKILL.md` = frontmatter + core rules + depth table + phase/status table + a one-line router per phase ≈ **2,500 w** (from 7,072, −65%)
- `references/phase-1-specify.md` … `phase-6-document.md`, loaded at phase entry
- `references/resuming.md` (1,202 w) — loaded only when the trigger is a resume
- `references/change-requests.md` (477 w) — loaded on the event

Effect: **Trivial 7,801 → ~3,200. Small ~17,538 → ~13,000** (Phases 0/3/4 and Resuming never load).
The activation decision itself is made against 2,500 words instead of 7,072.
Cost: one mechanical split, plus rewriting every intra-SKILL.md cross-reference as a file reference.
Risk: more files to keep consistent — the failure mode iterations 1–2 already demonstrated. It is
worth doing only with the recurrence rule enforced, which v3.0.0 now states.

## B10 — escape hatches: guarded, with one gap

| Hatch | Guarded? |
|---|---|
| `unattributed` | **yes** — "blocks exit until they accept it" |
| `blocked (pre-existing)` | **yes** — requires step 4 to have actually attributed the cause outside the change set |
| `blocked (flaky)` | **yes** — "introduced flakiness is *not met*, never this" |
| `provisional` baseline | **yes** — recorded as provisional in the plan |
| **`Base: — no resolvable history`** | **NO** — see below |

### B10-F1 (medium-high) — the `— no resolvable history` hatch has an entry condition but requires no evidence that it holds
It disables four rules at once (the rebase test, the base-tree control, the change-set inventory,
the integration check). Its entry condition — "no VCS, no commits yet, or a shallow history that
resolves no merge base" — is mechanically checkable (`git rev-parse --is-shallow-repository`,
`git rev-parse HEAD`), but **nothing requires the agent to cite the check**, and it is the cheapest
path through Phase 7 in the whole skill.
**Fix:** require the check's output on the **Base** line — `— no resolvable history (git rev-parse
--is-shallow-repository → true)` — the same citation discipline A4-F2 just imposed on evidence.

## Still open (session limit)
S08 spec-drift, S09 migration/backfill, S10 change-request-midflight, and the full adversarial
red-team pass. The three scenarios are the only ones never run against any version.

---

# B10 — red team (full pass, v3.0.0)

**Correction to the partial audit above:** I scored `blocked (pre-existing)` and `blocked (flaky)`
"guarded — requires step 4 to have actually attributed the cause". B10 shows the attribution
requires only that the agent **type** it: step 4's base-tree control leaves no artifact anywhere in
the report format. Both verdicts are assertion-gated, not evidence-gated.

## Five-attack verification
| # | Attack | Status |
|---|---|---|
| 1 | Exit green with a red gate | **partially closed** — *red* is closed; *not-run* is not. A non-test gate that errors and prints no violations satisfies "no new failures" literally; only the test gate has the executed-count guard (`:61`) |
| 2 | Cite a test that doesn't exercise the requirement | **partially closed** — correct diagnosis, but the compliance signal is still the agent's own prose; no runner output required on the citation path |
| 3 | Carry a verdict forward | **partially closed** — the literal form is banned (`:31`), but five *sanctioned* non-re-verifying labels now exist and one is self-authorable |
| 4 | Waiver swallows a table row | **partially closed** — see F3 |
| 5 | Delete live code as a deletion gap | **closed** — four independent layers |

## F1 (critical) — every gate verdict rests on two numbers no rule requires the agent to have produced
`verification.md:10` (baseline) and `:56` (base-tree control) both demand a *run*; neither demands an
*artifact*. Contrast the line directly above: **Base** requires `git rev-parse HEAD` — a SHA cannot be
produced without running the command. A baseline can: it is a free-text cell **whose first offered
example in `plan-template.md:26` is the word `clean`**.
Trace: Phase 3 under time pressure → agent writes `Baseline: clean` in all four rows, copying the
template. Phase 7 step 4 → attribution costs a stash plus a second full suite run and **leaves no line
anywhere in the report format**, so it is skipped and the agent writes the sentence the exemplar models.
Output: `Gates: pytest ✅ 82/84 (2 pre-existing failures, unchanged) · Converged: yes` — where
"unchanged" compares a Phase 7 count against a *word*, and `pre-existing` may be a fabrication.
**Self-report inventory — four unverifiable gates remain:** the Phase 3 baseline, step 4's base-tree
control, `Clean-code: none`, and step 7's "examples run as written". The strongest gate in the whole
skill is the negative control, because it is the only one that requires **observed failure output**.
**Drop order under context pressure:** (1) step 4's base-tree control — most expensive act in Phase 7,
*zero* artifact; (2) the Phase 3 baseline; (3) per-pass re-running of evidence; (4) the overlap scan's
branch reads; (5) step 7's examples.
**Fix:** apply A4-F2's own discipline to the gate half — the **Baseline** cell carries observed output
or counts, never an adjective; a mandatory `Attribution:` report line names the base-tree command run
and its result per failure; change the template's first example away from `clean`.

## F2 (critical) — the honest path is priced above the dishonest one, by the skill's own exception structure
`R4 — focus returns to the trigger after the dialog closes`, jsdom-only project.
*Honest route* (`:34`, manual verification): interrupt the user — and this is a row a standing waiver
**never** covers, so even "run the rest without asking me" gets stopped — plus a dated Decisions entry
plus exact commands and observed output. Three artifacts, one blocked stop.
*Cheap route:* cite `dialog.test.tsx::"closes on Escape"` — renders, fires Escape, asserts unmount.
One sentence, zero stops, satisfies the citation contract's **shape** exactly. `:30`'s own prose says
this does not encode the criterion — but that judgment is made by the same agent that wants to finish,
and nothing downstream can disagree. This is the S06 class, and it survived two passes there because a
second pass re-running the same reasoning reaches the same conclusion.
**Fix:** make the routes cost the same — require the runner's own line for the cited case (`1 passed`
for that node id), the citation contract's missing half.

## F3 (high) — Phase 7's carve-out lists 4 of the 13 excluded rows, and it is the copy read at the point of use
`SKILL.md:19` says "That is the whole exclusion; no rule elsewhere repeats it." **The claim is false in
its own file:** `:179` repeats it lossily as "(a deletion, spec drift, a deferral, an accepted
limitation)", omitting nine rows — six of them plausible gap resolutions, including test removal.
Trace: a waived session files `G3 — remove obsolete legacy_auth_test.py::test_old_flow`; test removal
is not in the four-item list, so the waiver covers it; `:19`'s uniqueness claim actively discourages
going back to check. The agent deletes the test and the gate goes green — the exact act `:61` names as
the canonical cheat ("Deleting or weakening a failing test is never how a gate passes").
**Fix:** delete the parenthetical, point at the table unenumerated, and delete the false uniqueness claim.

## F4 (high) — `— accepted limitation` is the only sign-off row with no approver in its recorded form, and it confers permanent immunity
Siblings carry a trace: `deferred` requires `owner <who>`; deletion requires the user's confirmation;
test removal requires "naming the test **and the approval**". Accepted limitation requires **a date**.
And `:106` grants it immunity: "later passes report its recorded verdict and never re-file a gap for it".
Trace: Phase 7 pass 3, unevidenceable `R6`, user silent. `SKILL.md:21`'s silence rule ("leave its Status
`draft`") is **incoherent at Phase 7**, where artifacts are `approved`. With no defined behavior and a host
prompt saying finish, the agent writes the annotation itself. Output is byte-identical to the exemplar.
The user agreed to nothing, and no future pass reopens it — the carry-forward `:31` bans, re-entering
under a label `:31` doesn't cover. `waived` launders the same way and **is not in core rule 2's table at all**.
**Fix:** `— accepted limitation (Decisions YYYY-MM-DD, accepted by <who>)`; define silence at Phase 7 as
`Converged: no — awaiting <the decision>`; add `waived` to the table.

## F5 (high) — the canonical report exemplar converges with a gate that never ran
`:65` — "report the gate `pending` and **do not exit the convergence loop on it**". `:120` — `Converged: yes`.
`:130` — "coverage ⏳ pending — no run for this change set yet". The `Waived:` line lists two items,
neither of them the coverage gate. **The exemplar demonstrates the exact exit the rule forbids.**
Exemplars are copied; prose fifteen lines up in another subsection is not.
Second residual: a *non-test* gate that errors out (mypy crashing on a new dep, lint exiting 2 with no
findings) produces zero failures and satisfies "no new failures" — only the test gate has `:61`'s guard.
**Fix:** set the exemplar to `Converged: no — coverage gate pending (step 9)`; extend `:61` to all gates.

## F6 (high) — Audit mode inherits the procedure but not the artifacts its guards attach to
Three structural mismatches: (a) it invokes step 2 and step 3's verdict table but **not step 4** — yet two
of that table's verdicts are defined entirely by step 4; (b) it builds the inventory "over the paths those
requirements name", while `writing-specs.md:37` **forbids requirements from naming paths**; (c) the
scope-of-analysis disclosure is scoped to "every deletion gap", and audit mode files none.
Trace: a failing `test_retry_schedule.py` → `blocked (pre-existing)` reads as *definitionally* correct in
an audit (every cause is outside any change set by construction) → a genuinely broken retry schedule is
filed as "not our problem". Meanwhile the agent guesses the path set itself, misses a dotted-path Celery
entry and a signal handler, and reports two live production entry points as dead — with no scope line.
**Fix:** audit mode needs its own verdict vocabulary (forbid both `blocked` verdicts where step 4 didn't
run), a user-confirmed path set, the scope line on any unreached finding, and a required output shape.

## F7 (medium-high) — every v3.0.0 judgment threshold resolves toward "no finding", and one dissolves the rule above it
- **Speculative generality is now unfileable.** `clean-code.md:25` (added for S03-T4) says a `Verify:` step
  is a second caller and "this rule never wins over a requirement's evidence" — and Phase 5 mandates a test
  for everything. So `SKILL.md:160`'s "current second use" is satisfied **by construction** for anything the
  agent writes. A `RetryStrategy` interface with one implementation and a test is defensibly not-a-hit.
  *This is a regression introduced by wave A.*
- **The close-call disclosure is invisible in its own format:** `:21` asks which way a close call went;
  the format at `:3` is `Clean-code: none`. Three close calls resolved "no" produce a byte-identical note to none.
- **The duplication threshold is read one clause deep:** ">~5 lines, **or** encodes a decision" — the second
  clause is far broader, so an agent wanting a clean sweep reads the leading quantified clause and stops. The `~` makes 6 arguable.
- **The plan-omission size test has a ~50:1 cost ratio across an agent-judged boundary**, and the word doing
  the work is "plainly".
- **The magnitude flag reports the agent's own number:** the agent authored the **Files** line, so a nine-file
  task can be written naming three and the flag never fires.

## B10 verdict
Most dangerous remaining path: **F1 × F2** — a report reading `Converged: yes · Gates: ✅ · every R# met`,
produced by an agent that typed its baseline instead of measuring it, never ran the base-tree control, and
cited tests that touch the subject without observing the criterion. All three steps are *stated* correctly
and *evidenced* by nothing but the agent's prose. The report is byte-indistinguishable from a true one, and
it is the artifact the user reads **instead of** the code. v3.0.0 hardened the evidence half and left the
gate half on assertion — **the failure moved one column left.**
**Ship?** Not as a workflow claiming Phase 7 gates anything. Ship the specification-and-documentation half —
that is sound — with the verification claim downgraded until: (1) baseline and base-tree control cite command
output; (2) the exemplar stops modelling `Converged: yes` over an unrun gate; (3) `:179`'s four-item
enumeration is deleted.

---

# S08 — spec-drift audit (first real run against v3.0.0) — 52/60

**Verdict accuracy: 9/9 exact** — R1 met, R2 met, **R3 spec drift**, R4 met, **R5 not met**, R6 met,
E1 met, **E2 not met**, E3 met. Best accuracy of any run so far.

**v3.0.0 held, empirically:**
- **The citation contract did real work** — it caught R3: a test that passes and genuinely exercises
  `rankResults` but never encodes relevance semantics. This is exactly the S06 failure mode (a passing
  test whose scope is narrower than the requirement), caught by the rule written in response to it.
- **"Never carry a verdict forward"** was exercised for real across two full passes, with fresh
  re-derivation each time — the "unchanged from pass 1" hole is closed in practice, not just on paper.
- **Gate-failure-is-a-gap** fired correctly on a new lint warning, via a real base-tree worktree check.
- **The report format** was complete across every labelled line in both passes.
- **Report-don't-fix** held with zero exceptions: no code was touched until every gap was filed and approved.

### S08-T1 (high — a rule actually skipped) — the claim commit was dropped when implementing gaps
Phase 5's "claim it and commit that claim before writing code — **one commit, always**" was skipped
outright for G4/G5: code and claim landed in one commit. The rule is **buried mid-paragraph** among
overlap-scan and staleness content, so in a solo session it reads as ceremony. (Iteration 2 made this
commit mandatory precisely to remove the judgment call; it is still being dropped because of where it sits.)

### S08-T2 (medium-high) — the negative control has no path when the only evidence is an approved manual check
Its escape covers "a compile-time or type-level criterion" only. When a requirement's sole evidence is
an approved manual trace, **there is no assertion to invert at all** (hit on R6). Extended by analogy.

### S08-T3 (medium) — whether a gate's baseline tracks warnings, not just exit code, is stated only for the test gate
`:61`'s guard names the test gate's skipped/executed counts. A lint-only warning with no clean-code
analogue would slip through. (Same root as B10-F5's second residual.)

### S08-T4 (medium) — the report heading has no room for two passes on the same day
`### Verification report — <slug> — YYYY-MM-DD` forced an improvised `(pass 2)` suffix, deviating from
the template's "keep these exact shapes" instruction. B10-F1 wants a pass counter; this is where it goes.

### S08-T5 (medium) — no rule requires stating the entry mode before starting
Adaptive depth requires stating the depth in one line for new work. There is no equivalent for
"Phase-7-only / Resuming work / Audit mode" — a transparency gap on exactly the entry path this run used.

---

# S09 — schema migration + backfill (2M rows) — 53/60 (highest of all ten runs)

### S09-F1 (SEVERE — headline) — a real data migration has NO rule-sanctioned door into Phase 7
T4 ("run the migration + backfill in production") is **required** (inside Minimum shippable), **in scope**,
and cannot honestly become `Done` (no production access), `Waived` (nothing was declined), or `Deferred`
(deferral means "not in this change set", and R2/SC2 are). Phase 7's entry condition is literally "when
every task is done, waived, or deferred" — so **the feature has no sanctioned entry into Phase 7 at all.**
This is the *normal shape* of a real data migration, not an edge case. It is S07-T3 still open in v3.0.0,
sharper: the only way a report was produced at all was by borrowing "Diagnostic passes" from
`verification.md`, whose stated triggers are resume-only — an explicit guess, not a sanctioned path.

### S09-F2 (moderate) — no verdict fits "implementation complete and tested against a stand-in, real execution pending"
R1/R2's code is written, reviewed, and covered by passing tests plus a real negative control — done by any
normal measure. But their only sanctioned evidence (the production run's observed output) does not exist.
`partially met`'s definition ("missing edge case, missing test…") **does not describe this at all**. Used as
least-wrong and flagged; an unflagged use would tell a reviewer the code is unfinished when it is not.

### S09-F3/F4 (moderate) — the claim-commit and the draft→in-review→approved discipline leave no artifact trace *by design*
Both are process invariants whose only witness is git history at the moment they happen; **the final artifact
looks identical whether the stop genuinely occurred or was skipped.** This run skipped both (caught on
self-review) and nothing in the artifacts would have caught it externally. Independent confirmation of
S04-T1, and the same class as B10-F1: the skill's process guarantees are unfalsifiable after the fact.

### S09-F5 (moderate) — the Stored-data **Target** checklist has no answer for "no rehearsal environment exists at all"
Its three named forms (disposable local / ephemeral CI / restorable copy) all assume *some* safe environment
exists to rehearse the forward→reversal→forward cycle Phase 5 requires. Resolved by analogy to a different
section's "cannot execute at all" rule; the Target bullet itself gives no instruction.

### S09-F6 (minor) — core rule 2's table calls itself "the one list" but has no row for the Target / Who-executes-it stop-and-ask
Running a data-change command against production is unambiguously a stop-and-ask per `data-and-delivery.md`,
but the table names only "irreversible/data-losing execution" and "a delivery step" — the agent had to infer
that a schema migration counts as "delivery" to map it onto a Sign-off row at all.

### The 16 data/delivery slots — verdict on tech-B's work
**All 16 exercised, none left `— none` or unanswerable.** Roughly half drove real decisions: **Target,
Reversal, Existing rows, Volume, Data integrity, Who executes it, Rollout stages, Where checks are measured** —
each surfaced a genuine finding (no rehearsal environment, forward-only migrations, the measured-criteria
SC-split, avoiding invented monitoring). The other half (**Required data, Data lifecycle, Configuration,
Flag retirement**, and partly **How it is turned off**) were fast, correct, low-drama answers — not wasted,
since each forced a real check against the repo, but not where the value came from.
Two slots (**How it reaches users**, **How it is turned off**) needed conceptual translation: the Delivery
checklist's vocabulary is visibly tuned for flag-gated app rollouts rather than a one-time data change.

---

# S10 — reviewer change request mid-flight — 55/60 (highest of all ten runs)

### The split — handled correctly, both halves
**Rename ("Ejecutar" → "Aplicar"):** correctly classified as ordinary Phase 5 implementation feedback
(after confirming no `R#`/`E#` names the literal label), applied directly with no spec touch, gates re-run clean.
**Confirmation threshold (>20 rows):** correctly classified as behavior feedback and routed as a change
request — new **R6** into `spec.md` first (dated Decisions entry naming the reviewer and PR #418, plus a new
Sign-off row), then `plan.md` (C4's Implements, the Evidence and coverage tables, an Approach addendum), then
`tasks.md` (T4/T5 scope extended) — **in that order**, spec Status `approved → in-review` and left there, with
no R6 behavior implemented pending sign-off.
**The invalidation check ran and is on record:** T1/T2 unaffected (R6 gates only the apply action), T3's
shipped code unaffected (the gate lives entirely in T4's unshipped remainder) — reasoned from actual component
boundaries rather than asserted.

### S10-T1 (high) — the **Integration** line is never reconciled against an incoming PR number
The user's message names "PR #418" as what the teammate reviewed, strongly implying this change set goes out
through a review-gated PR — but `plan.md`'s **Integration** line still read `— direct commits to the base
branch, no review policy found`, and was never reconciled or flagged. The two checklists that each mention
"the identifier" describe **different things** (a review comment's origin vs. the change set's own merge path)
and never cross-reference each other.
**Fix:** in Review feedback — "If the review identifier names a change set the plan's **Integration** line does
not record, reconcile Integration now — update it or flag the mismatch — before filing the Decisions entry."

### S10-T2 (high) — "confirming with the user first" before claiming a task has no defined shape
Resuming work says "take the first unchecked task no one else holds… confirming with the user first". The
agent stated its findings and claimed T4 in the same turn, treating "sigue con lo de bulk actions" as standing
authorization. Nothing disambiguates whether a feature-level "continue" already counts — and Phase 5 itself is
`Stop? no` in the workflow table, so this resume-specific courtesy sits inconsistently on a phase that
otherwise never stops.
**Fix:** drop the clause, or make it explicit — state the task, give one turn to redirect, and proceeding after
that turn is not silence.

### S10-T3 (medium-high) — the Status reset rule covers only the `implemented` case
"Amending an **implemented** spec resets it (and `plan.md`) to `in-review`" vs. core rule 2's general "revise
and re-present — it stays `in-review` until sign-off". Here the spec was `approved`, not `implemented`:
`spec.md` correctly flipped to `in-review`, but **`plan.md`'s Status was left `approved`** because no rule
covers that case.
**Fix:** state the general case once — any artifact whose content a change request amends stays `in-review`
until sign-off, regardless of prior Status.

### S10-T4 (medium) — "write the stop down before asking" is scoped to self-discovered errors
Its trigger — "If implementation **reveals** the spec or plan is wrong" — is narrower than its evident purpose.
Applying it to an externally-triggered pause (reviewer feedback arriving mid-task) required inference.
**Fix:** "If implementation must pause — because it reveals a problem, **or because new information arrives
mid-task** — write the stop down before acting on it."

### S10-T5 (medium) — resume routing has no case for a loose but unambiguous reference
"sigue con lo de bulk actions" is neither "named none" nor an exact slug. Resolving it meant reading both
specs' headers — and discovering `admin-user-table` also technically qualifies as open work via an open dated
follow-up — before concluding the phrase disambiguates.
**Fix:** a third clause — a loose reference matching exactly one open-work spec resumes it directly, without
listing the rest.
