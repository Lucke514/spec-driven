<!-- Status enum: draft | in-review | approved | implemented | superseded | abandoned -->

# Plan: [Feature name]

> Spec: [spec.md](./spec.md)
> Status: draft
> Last updated: [YYYY-MM-DD]

## Approach

[2–5 sentences: the technical strategy, and what it was chosen over.]

## Current state

[What exists today that this builds on or changes: modules, conventions, constraints found by reading the codebase. Real paths.]

- **Architecture**: [how this repo organizes code — layers / feature folders / modules — and where each kind of thing lives; or "no coherent pattern — following the local convention of `path/`". Components respect this.]
- `path/to/module` — [role, what changes]

## Quality gates

[Gate, Command, Where: discovered in Phase 3; every task passes all of them. Baseline: observed output or counts, filled at Phase 5's start. Fill every cell — `Where`, a gate with no tooling, the read-only command form — per `references/verification.md` → Recording gates.]

| Gate | Command | Where | Baseline |
|---|---|---|---|
| Tests | `[e.g. pytest, go test ./...]` | `here` | `[e.g. 2 pre-existing failures in legacy/*, 387 skipped, flaky: LedgerLockIT; or: 0 failed, 1284 passed, 387 skipped]` |
| Lint | `[e.g. ruff check ., cargo clippy -- -D warnings]` | `here` | `[e.g. 8317 pre-existing warnings, compared per file and rule; or: 0 warnings over 412 files]` |
| Format | `[e.g. gofmt -l ., cargo fmt --check]` | `here` | `[e.g. 0 files listed; or: 3 unformatted]` |
| Types | `[e.g. go build ./..., mypy]` | `here` | `[e.g. 0 errors in 218 files; or: 41 pre-existing]` |
| [Other] | `[e.g. accessibility scan, dependency audit, size budget — one row per additional check the project runs]` | `[here / pipeline-only]` | `[e.g. 3 pre-existing violations; or: 0 findings]` |

**Base**: `[base branch]` @ `[SHA at Phase 5's start]` — the branch this feature starts from (one that still resolves later, never a bare SHA or `HEAD`) and the commit the baselines were measured on. [Same reference.]

**Integration**: `[direct commits to the base branch, no review policy found | one review-gated change set | N change sets, in order]` — how this change set reaches the branch named in **Base**, who approves it, and which required checks overlap the `pipeline-only` gates. [`references/team-and-review.md` → Discovery.]

**Task span**: `— a task is claimed for at most 7 days` — [replace only where this project's tasks legitimately run longer: a claim older than the span is stale, not held (SKILL.md → Phase 5).]

**Measurements**: `[command]` → `[value at Phase 5's start, or "new behavior — no current value"]` @ `[conditions: environment, data scale, concurrency, run count]` — one row per requirement stating a number; omit when none does. [Same reference.]

## Components

[Each component maps to ≥1 spec `R#`/`E#`; one implementing nothing from the spec is cut. `C#` ids are stable for this plan's lifetime — never renumbered, never reused after deletion; a cut component keeps its number and gets `— cut (Decisions YYYY-MM-DD)`.]

### C1 — [Component name]

- **Implements**: R1, R3, E1
- **Where**: [files/modules to create or change, where the Architecture line says they live; state the reason if it deviates]
- **What**: [what it does; key interfaces or data shapes]
- **Reuses**: [existing code this extends or calls — real paths/symbols; or `— searched <areas/terms>, nothing found`.]
- **Duplicates**: [`— none`, or — where the search found a near-miss this component repeats anyway — the module whose behavior it repeats and why extending or extracting it is not the answer. Non-empty, it is approved with the plan and reaches Phase 7's sweep pre-declared.]
- **Depends on**: [other components, or `—`]

### C2 — ...

## Build order

[Dependency-ordered. Independent groups that can proceed in parallel are the groups the tasks carry as `[P]`.]

1. C1
2. C2, C3 (parallel)
3. ...

## Evidence per requirement

[One row per spec `R#` and `E#` — filled in Phase 3, read directly by Phase 7's walk. Resolve a blank cell before presenting the plan (same reference → Evidence per requirement).]

| R#/E# | Evidence (test path / measurement command / stand-in / manual check) | Exists today? |
|---|---|---|
| R1 | `test/module_test.py::test_named_case` | no — written by T3 |
| E1 | `[the stand-in it runs against, per **Dependencies**]` | yes |

## Data changes, delivery & dependencies

[One line each. The defaults below are common; anything else is one line per checklist item of `references/data-and-delivery.md` / `references/dependencies.md` — uncomment the matching block and fill it in.]

- **Data changes**: — none
<!-- when not — none: one line each, per change (data-and-delivery.md → Stored data)
- **Mechanism**:
- **Target**: [disposable local | ephemeral CI | restorable copy | none exists — say so, and what that blocks]
- **Reversal**:
- **Existing rows**:
- **Required data**:
- **Compatibility during rollout**:
- **Volume**:
- **Data integrity**:
- **Data lifecycle**:
-->

- **Delivery**: — ships with the normal release
<!-- when not — ships with the normal release: one line each (data-and-delivery.md → Delivery)
- **How it reaches users**: [pipeline and environments; or a one-time run, and when]
- **Who executes it**:
- **Rollout stages**:
- **Configuration**:
- **How it is turned off**: [flag, config, or revert; or the change's reversal]
- **Flag retirement**:
- **Where the checks are measured**:
-->

- **Dependencies**: — none
<!-- when not — none: one row per dependency — name · new | version a.b → x.y | retired · exact pinned version · the R#/E# that needs it — plus that file's checklist answers
-->

## Risks

| Risk | Mitigation |
|---|---|
| [What could go wrong] | [How the plan handles it] |

## Requirement coverage

[Sanity check — every spec `R#`/`E#` appears here; Phase 7 checks it for accuracy.]

| Requirement | Covered by |
|---|---|
| R1 | C1 |
| R2 | ... |
| E1 | C2 |
