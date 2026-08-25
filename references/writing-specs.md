# Writing good specs

Detailed guidance for Phase 1 (Specify). Load this when drafting or reviewing a `spec.md`.

## The testability rule

Every requirement must let a reviewer answer **"done or not done?"** with a plain yes/no. If judging it needs taste, context, or a meeting, it is not a requirement yet.

Rewrite vague qualities as observable behavior:

| Vague | Testable |
|---|---|
| "Search should be fast" | "Search returns results in < 300ms p95 for a 10k-item catalog" |
| "Handle errors gracefully" | "On network failure, the pending change is kept locally and a retry banner is shown; no data is lost" |
| "Secure login" | "After 5 failed attempts within 10 minutes, the account requires email verification to continue" |
| "Support large files" | "Uploads up to 500MB complete without loading the whole file into memory" |
| "Intuitive UI" | "A first-time user completes checkout without leaving the flow; every action reachable in ≤ 2 clicks from cart" |

Technique: ask "how would I demo this?" and "what test would fail if it broke?" — the answers are the criteria.

**Measured criteria** — a requirement stating a number (latency, memory, payload size, query count) is an `R#` only when a command can measure it in *this* environment **under the conditions the number actually means** (its data scale, concurrency, and environment — a benchmark on seeded toy data does not measure a production p95); Phase 3 records that command next to the plan's quality gates and Phase 7 cites its output as the requirement's evidence. Where nothing here can measure it, it is not a requirement: state it as an `SC#` naming its measurement method and the environment it is measured in, and keep as `R#` the part that is checkable without measurement ("results are ranked by relevance", not "in < 300ms"). The `< 300ms p95` row above is a requirement in a project that can run that measurement, and an `SC#` in one that cannot.

## What belongs in a spec — and what doesn't

**In**: behavior, constraints, edge cases, error semantics, non-goals, success criteria.

**Out**: technology choices, file names, architecture, library picks, data schemas beyond what behavior demands. All of that is Phase 3 (`plan.md`). A spec that says "use Redis" has leaked *how* into *what* — unless Redis itself is genuinely a requirement (e.g. mandated by the platform), in which case record it under Decisions with the rationale.

## Surfaces & their criteria

Name every surface the feature exposes, then cover its row with `R#`/`E#` or say in Non-goals that it is out of scope. Classify the surface, never the framework — "an HTTP contract plus a background job" is the statement; which library serves it is Phase 3's business. A feature with several surfaces carries criteria from each row.

| Surface | The spec covers — or names as a non-goal |
|---|---|
| UI / visual | interaction states (loading, empty, error), what is shown when there is no data or the action fails, keyboard and assistive-technology-relevant behavior |
| API / contract | inputs, outputs, error semantics and result codes, compatibility with existing consumers, how the change is versioned |
| CLI | exit codes, what goes to standard output vs error, flags and their defaults |
| Background job / scheduled work | idempotency on re-run, retry and give-up behavior, how a failure becomes visible to a human |
| Data pipeline | input contract and bad-record handling, re-run and backfill semantics, guarantees on the output |
| Library / package | public-surface compatibility, deprecation of whatever it replaces |

## Operational criteria

A feature that faces users or runs in production carries these too — an internal library or a pure refactor states in one line that it does not. Cover each item with `R#`/`E#` or say in Non-goals that it is out of scope; discover what this project already commits to by reading the repo (checker config, CI jobs, scripts, stated policy) and never assume a standard it has not adopted. Whatever you cannot answer becomes a `[NEEDS CLARIFICATION]`.

- [ ] **Load & volume** — the traffic, data size, and concurrency the feature must hold, and what it does past that point.
- [ ] **Accessibility** — for user-facing surfaces: the standard and level this project already commits to (found in its checker config, CI job, or stated policy), plus keyboard reach, focus behavior on navigation, contrast, and how errors are announced.
- [ ] **Text & locale** — user-visible text and locale-dependent formatting (money, dates, numbers, sorting), where the project has a mechanism for them; where it has none, say so.
- [ ] **Operational signal** — what shows this feature working or broken: what it emits, where a human sees it, and what makes someone look. (The Background job row's failure-visibility question, asked of every surface.)
- [ ] **Degradation** — what the feature does when a dependency it calls is slow or unavailable.
- [ ] **Partial failure** — where the feature's operation writes in more than one place (two stores, a store plus an external call, a store plus a queue or file): what is left behind when it fails between them, and what makes it consistent again (one transaction, retry, compensating action, reconciliation job). An `R#`/`E#` or an explicit Non-goal — never unstated.

An item stating a number follows the measured-criteria rule above: an `R#` only when a command here can measure it under the conditions the number actually means — otherwise an `SC#` naming its measurement method and environment.

## Sensitive ground

When the feature touches authentication or authorization, personal or regulated data, secrets and credentials, or money, the spec carries explicit `R#`/`E#` for each item below — or Non-goals states in writing that it does not:

- **Access control** — who may do this, and what happens when someone who may not tries.
- **Traceability** — what record the action leaves (who did what, when) and where that record is visible.
- **Data handling** — what is stored, what appears in outputs, errors, and logs, what is deliberately not logged, and how long it is kept.
- **Data lifecycle** — when the feature creates a new store of personal or regulated data: how that data is deleted and exported when its subject is, naming the project's existing erasure, export, or retention path as discovered by reading the repo. An explicit "the project has none" is a valid answer and belongs in Non-goals.
- **Correctness under repetition** — for anything moving money, credits, or entitlements: what happens when the same request arrives twice.

Whatever you cannot answer becomes a `[NEEDS CLARIFICATION]` and goes in Phase 2's first batch — these questions change the shape of the plan, so they are asked first.

## Replacement & port features

For a behavior-preserving change — porting a module to another library, runtime, or framework; rewriting an implementation; swapping a dependency — "what, never how" does not license an empty spec: the requirements are the behavior that exists today.

- Derive `R#`/`E#` by reading the current code and its tests, and cite what you read (real paths) under Decisions so a reviewer can check the derivation.
- Record the mandated target technology under Decisions with its rationale — the same escape hatch as any platform-mandated choice. It is a constraint, not a requirement.
- State what is allowed to change (performance, internal structure) and what is not (public surface, stored-data shape); the second list belongs in Non-goals.
- Add an `E#` or a first task that characterization-tests the current behavior *before* the switch, so Phase 7 has evidence of equivalence rather than evidence that new code passes new tests.

## Anti-patterns

- **The wishlist** — requirements with no acceptance criteria attached. Every `R#` carries at least one Given/When/Then or checkable statement.
- **The tutorial** — spec written as implementation steps ("first create the table, then add the endpoint"). Steps are tasks, not requirements.
- **Silent assumptions** — you picked a behavior for an unspecified case and wrote it as if the user asked for it. Mark it `[NEEDS CLARIFICATION]` or put it in Decisions; never smuggle it in.
- **Happy-path-only** — no edge cases section, or one that just says "handle errors". Empty states, bad input, concurrency, and limits are where features actually fail.
- **Unbounded scope** — no Non-goals section. If you can't name what the feature *doesn't* do, the scope isn't understood yet.
- **Untestable success** — success criteria like "users are happy". Tie success to something checkable: a metric, a manual script, a rollout gate.

## Sizing requirements

- One requirement = one observable capability. If an `R#` needs the word "and" to describe two independent behaviors, split it.
- 3–12 requirements is the normal range for a Standard feature. Above that, revisit Phase 0 — it may be several features.

## Minimum shippable & deferral

The Requirements section ends with a **Minimum shippable** line — the smallest set of `R#`/`E#` that still delivers the Objective. It exists so the deadline question ("what do we drop?") has an answer written before it is asked.

- [ ] Test each requirement: *if this `R#` were absent, would the Objective still be delivered?* Yes → outside the minimum set. No → inside it.
- [ ] Dependency order is not value order: the plan's Build order says what must come first, never what is worth most. Never derive one from the other.
- [ ] The line is spec content: settled at Phase 2 with everything else, and changed only through the amendment path, like any `R#`.
- [ ] It is also the scope-creep test — a requirement added during clarification that lands outside the minimum set is stated as such, not carried as if it were load-bearing.

Cutting scope under a deadline reads that line first and defers from **outside** it:

- [ ] Annotate the requirement in place — `— deferred (Decisions YYYY-MM-DD, owner <who>)` — and never delete it, move it to Non-goals, or record it as an accepted limitation: those say the feature deliberately does not do this; a deferral says *not in this change set*.
- [ ] Record the dated decision in Decisions — what was cut, why, and when it is expected — and route it through the Open follow-through path in [team-and-review.md](team-and-review.md): owner, date, and the identifier from the spec's **Tracking** target, or a `- [>] Deferred` entry in `tasks.md` where the project tracks work in the repo only. That is what makes a later session surface it again.
- [ ] Deferral is the user's decision and always needs explicit sign-off (SKILL.md core rule 2) — an agent never cuts a requirement to save itself work.
- [ ] Cutting *into* the minimum set is not a cut: it cancels the feature (SKILL.md → Change requests mid-flight) or re-specifies it. Say that plainly instead of shipping a hollow version.
- [ ] Close the tasks that would have implemented it as `- [~] Waived` or `- [>] Deferred`, and let Phase 7 give the requirement the **deferred** verdict ([verification.md](verification.md) step 3) — not *not met*, which reads as a verification failure nobody chose.
- [ ] When the deferral comes due the requirement is already written: record a dated Decisions entry taking it back into scope, remove the `— deferred` annotation, plan and schedule its tasks (an **implemented** spec reopens to `in-review` like any amendment), and let Phase 7 verify it **met**.

## Clarification questions (Phase 2)

- Batch them; don't drip one question per message.
- Order by consequence: ask first what would change the shape of the plan.
- Offer a default: "X or Y? I'd default to X because…" gets faster, better answers than open questions.
- Record every answer in the Decisions section — including "user said you decide" plus what you decided and why.
