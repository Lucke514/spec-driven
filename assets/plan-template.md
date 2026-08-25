# Plan: [Feature name]

> Spec: [spec.md](./spec.md)
> Status: draft  <!-- draft | in-review | approved | implemented | superseded | abandoned -->
> Last updated: [YYYY-MM-DD]

## Approach

[2–5 sentences: the overall technical strategy and why this approach over the obvious alternatives.]

## Current state

[What exists today that this builds on or changes: relevant modules, conventions, constraints found by reading the codebase. Reference real paths.]

- **Architecture**: [how this repo organizes code — layers / feature folders / modules / etc. — and where each kind of thing lives; or "no coherent pattern — following the local convention of `path/`". Components below must respect this.]
- `path/to/module` — [role, what changes]

## Quality gates

[Discovered from the project's tooling in Phase 3. Every task must pass all of these before it is marked done, along with the spec-driven skill's junk-code checklist.]

| Gate | Command | Where | Baseline |
|---|---|---|---|
| Tests | `[e.g. pytest, go test ./..., mix test]` | `here` | `[e.g. clean; or: 2 pre-existing failures in legacy/*, 387 skipped, flaky: LedgerLockIT]` |
| Lint | `[e.g. ruff check ., go vet ./..., cargo clippy -- -D warnings]` | `here` | `[e.g. clean, or: 8317 pre-existing warnings (count; compared per file and rule)]` |
| Format | `[e.g. gofmt -l ., cargo fmt --check, mix format --check-formatted]` | `here` | `[e.g. clean]` |
| Types | `[e.g. go build ./..., mypy, mix dialyzer]` | `here` | `[e.g. clean]` |
| [Other] | `[e.g. accessibility scan, dependency audit, size or performance budget, contract check — one row per additional check the project already runs]` | `[here / pipeline-only]` | `[e.g. clean; or: 3 pre-existing violations in legacy/*]` |

**Base**: `[base branch]` @ `[SHA]` — the branch this feature starts from and the commit the baselines above were measured on, recorded in Phase 3 with them and confirmed at the start of Phase 5, before the feature's first commit: the branch point when the feature has its own branch, the tip of the shared branch at that moment when its commits are slug-prefixed. Name a branch that still resolves later (`main`, `release/2.4`), never a bare SHA or `HEAD` — verification tests `git merge-base HEAD <that branch>` against the SHA above to detect a rebase or a merged-in base. Verification builds the feature's change set from the SHA.

**Integration**: `[direct commits to the base branch, no review policy found | one review-gated change set | N change sets, in order]` — how this change set reaches the branch named in **Base**, read from the project's own policy (CODEOWNERS, branch-protection or required-check configuration, the contribution/review policy, a pull-request template): who must approve it, and which checks are required there (name the ones that overlap the `pipeline-only` gates above). Pushing, opening, or merging is the user's step, like a delivery step. Verification checks the resulting state before the spec reaches **implemented**: merged into that branch with the required approvals on record, or reported as `pending review` with its identifier.

**Measurements**: `[command that measures it]` → `[value on the untouched tree, or "new behavior — no current value"]` @ `[conditions: environment, data scale, concurrency, run count]` — one row per requirement stating a number (latency, memory, payload size, query count, throughput). Verification re-runs the command and cites its value **against these conditions**; a value measured under conditions the requirement does not describe is partially met, never met. If the conditions the requirement actually means cannot be reproduced here, it is not a requirement: move it to a success criterion naming its environment and measurement method. Omit this line when no requirement states a number.

[Record each baseline by running the command once on the untouched tree before implementation starts — its failures (enumerated, or a total when the backlog is too large to list), the test gate's skipped count, and any check that fails only on some runs, marked `flaky`. A gate passes when it adds no NEW failures to its baseline; pre-existing failures are reported in verification and may become their own fix task — they never block this feature. A command that could not execute at all — missing service, dependency, or config — has no baseline: get it runnable, or record the user's refusal in the spec's Decisions. Never record a failure-to-run in the Baseline column. Measure on a tree holding none of this feature's work — if a diff already exists, stash it first; its failures are the feature's, never baseline. Every command recorded above must be read-only — it reports, it never rewrites the tree: record a writing tool's check form (`cargo fmt --check`, `mix format --check-formatted`, `black --check`), never its default; a formatter gate that always exits 0 is not a gate.]

[**Where** is `here` for a gate that runs in this environment, and `pipeline-only` for a check the project enforces automatically on every change but whose credentials or infrastructure live only in its pipeline. A pipeline-only gate has no local baseline — record `—` — and verification evidences it from that pipeline's run on this change set, cited by run and result; it is a recorded gate, never missing tooling, and never covered by the manual-verification exception.]

[A gate is missing only when nothing in the project can perform its check — in statically typed compiled languages the build command is the type gate; where the language compiles without type-checking (Elixir, Erlang, Clojure) the build is no type gate, so record the project's configured analyzer instead. If a gate is genuinely missing, say so and propose a task to add a minimal setup.]

## Components

[Each component maps to ≥1 spec requirement or edge case. If a component implements nothing from the spec, cut it.]

### C1 — [Component name]

- **Implements**: R1, R3, E1
- **Where**: [files/modules to create or change — placed where the Architecture line above says this kind of thing lives; state the reason if it deviates]
- **What**: [what it does, key interfaces or data shapes]
- **Reuses**: [existing code this extends or calls — real paths/symbols; or "searched <areas/terms>, nothing fits because <reason>". New code is the fallback, not the default.]
- **Depends on**: [other components, or "—"]

### C2 — ...

## Build order

[Dependency-ordered sequence. Mark independent groups that can proceed in parallel.]

1. C1
2. C2, C3 (parallel)
3. ...

## Data changes, delivery & dependencies

[One line each. The defaults below are valid and common; anything else follows the spec-driven skill's data-and-delivery checklists — for data: mechanism, target datastore, reversal (and what makes recovery possible where it is irreversible), existing rows, required/seed data, compatibility during rollout, volume, the integrity check that proves the data survived, and how a new store of personal data joins the project's erasure/export path; for delivery: how it reaches users, who executes each step and against which environment (a step acting on a shared, staging, or production environment is a stop-and-ask, never run by the agent), the stages of an ordered rollout with each stage's scope, observation window, signal, condition to advance and condition to roll back, each new config value or secret — how it reaches every environment, required or defaulted, and the behavior when it is absent — how the feature is turned off and the task that exercises that off path, who retires an introduced flag, and the environment plus the signal (metric, log, dashboard, report) each rollout success criterion is read from; for dependencies: how each one enters (manifest plus committed lockfile, vendored copy, private mirror) at an exact pinned version, its license and compatibility with this repo's, its maintenance and open advisories, its weight and install-time behavior, the cost and limits of a metered service, the provider contract version the integration targets and what stands in for it in tests, the other callers a version change affects and what covers them, and who removes a dependency this feature retires. Adding a dependency, or changing the version of one other code shares, is approved by the user before this plan is — never a side effect of a task.]

- **Data changes**: — none
- **Delivery**: — ships with the normal release
- **Dependencies**: — none  <!-- otherwise one row per dependency: name · new | version a.b → x.y | retired · exact pinned version · the R#/E# that needs it -->

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| [What could go wrong] | low/med/high | [How the plan handles it] |

## Verification strategy

[How the work will be checked as it lands: test approach per component, commands to run, any manual checkpoints.]

- [Component/area]: [how it is verified]

## Requirement coverage

[Sanity check — every spec requirement and edge case appears here.]

| Requirement | Covered by |
|---|---|
| R1 | C1 |
| R2 | ... |
| E1 | C2 |
