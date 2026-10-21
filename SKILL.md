---
name: spec-driven
description: >-
  Spec-driven development (SDD): write spec.md, plan.md and tasks.md in the repo and get them
  approved before code, then implement, document and verify. Use when a reviewer could answer
  "done or not done?" about the change: a new or resumed feature, a behavior-changing bug fix, a
  port or rewrite, a migration, backfill or rollback, a staged rollout, an external API,
  performance/accessibility/observability criteria, cutting scope, review feedback into a spec, a
  handover, auditing code against a spec, or SDD/spec-first. Do not use for: a dependency add or
  version bump with no behavior change, a one-file fix, a rename, formatting, or when the user
  already said what to build and how.
license: MIT
metadata:
  author: Lucke514
  version: "3.1.0"
---

# Spec-Driven Development

Write the spec before the code. The spec, not the conversation, is the source of truth for what is built and how you will know it is done. Every phase leaves an artifact on disk that survives the session. Nothing ships without passing the quality gates and leaving documentation behind.

## Core rules

1. **No implementation before an approved spec.** For non-trivial work with no spec, start at Phase 1 (Phase 0 if Large). Do not start coding.
2. **One proposal review before code.** Draft the spec, plan and tasks, then present them together as one proposal. Get explicit approval before any code.
   - Phase 2's questions are a Q&A turn, not a stop. Phases 0 and 7 keep their own stops. A spec-only review before planning is opt-in, never the default.
   - Status is `in-review` when presented and `approved` on sign-off. On a change request, revise and re-present; touched artifacts stay `in-review` until sign-off. No artifact carries `approved` without having been `in-review`.
   - Never ask for approval while `[NEEDS CLARIFICATION]` markers remain.
   - **Waiver.** The user may waive the review stops ("run the remaining phases without asking me"). Record it as a Decisions entry in `spec.md` and mark the affected artifacts `approved` on it. They are still written and presented, just not blocked on. **A waiver covers only the review stops before code and Phase 7's approval to implement gaps, for work inside the approved scope. It never covers a sign-off item below.**
   - **No one answering** — a subagent, a `-p` run, CI, a scheduled agent, an unanswered question. Never guess past a stop and never delete. Leave the artifacts reached so far as `draft`, say in one line what would have been asked and what it blocks, and stop. That artifact is the handoff ([references/lifecycle.md](references/lifecycle.md) → Resuming work). At Phase 7, leave the report block at `Converged: no — awaiting <the decision>`; never write the verdict, annotation or sign-off the stop was for. Silence is not a waiver: it grants no approval and starts no gated work.

   **Always needs explicit sign-off — a waiver never covers these:** the spec's content, sensitive ground, adding, changing or superseding a requirement, deferrals, spec drift, accepted limitations, waived gaps, deletion gaps, weakened tests, manual-only evidence, adding a dependency or changing a shared one's version, irreversible data changes, and data or delivery steps against shared, staging or production environments. The one list, with how each is recorded, is [references/sign-off.md](references/sign-off.md): read it now when filling the **Sign-off** line, and before acting on any of these.
3. **Artifacts live in the user's repo** under `specs/<feature-slug>/`: `spec.md` (what and why), `plan.md` (how) and `tasks.md` (work breakdown with per-task verification). The slug is short, lowercase, hyphen-separated, unique across the repo and stable for the feature's lifetime. It also names the branch, the commit prefix `<slug>: ` and `docs/<slug>.md`.
   - In a monorepo, put `specs/` and `docs/` side by side at the root of the package that owns the code; the templates' relative links need that. If no single package owns the feature, use the repo root (or the shared package), list the affected packages in the plan's Current state, and follow each package's doc convention for its half of the doc page.
   - Whenever a phase edits an artifact, set its `Last updated` to the current date.
4. **Requirements must be testable.** A reviewer can answer "done or not done?" with yes or no. Rewrite vague asks ("fast", "user-friendly", "secure") as measurable criteria.
5. **When the spec and the code disagree, the spec wins.** Fix the code, or change the spec explicitly with the user's approval. Never let them drift silently.
6. **No junk code — ever.** A task is not done while its diff holds dead code, debug leftovers or duplication. The checklist in [references/clean-code.md](references/clean-code.md) is requirements, not suggestions; load it at the first self-review (Phase 5, or a Trivial change).
7. **A feature is not done until it is documented.** Phase 6 writes docs in the repo, and Phase 7 checks them like any requirement. The doc page is a deliverable the user asked for by starting this workflow. Where the host agent forbids creating `.md` files unbidden, say so in one line and use the README/doc-comment form the Small row allows.

## Adaptive depth

Scale the ceremony to the work. Classify before starting:

| Depth | Test | Artifacts | Phases run | Docs form |
|---|---|---|---|---|
| **Trivial** | Nothing observable changes for a user of the code, and no requirement could be written: typo, rename, comment, formatting, version bump. If it fits an `R#` with a Given/When/Then, it is at least Small. Judge the request **as a whole**: one clause that is at least Small makes all of it at least Small; never split it by depth | none, but still gated (below) | none | — |
| **Small** | One capability, < ~1 day | one collapsed `spec.md`: header block (Status, Owner, Sign-off, Tracking, Last updated), Objective, **Users & scenarios** with its Surfaces and Sensitive ground lines, Requirements, Non-goals (one line is fine), Edge cases, Decisions, then `## Tasks` in the tasks format without the **Component** field (tasks cite `R#`/`E#` directly); no Success criteria. Next to those tasks: the gate commands with their baselines, the **Measurements**, **Base**, **Integration** and **Task span** lines, the overlap result, and the **Data changes** / **Delivery** / **Dependencies** lines | 1, 2, 5, 6, 7, plus Phase 3's tooling discovery and Phase 4's minimal-setup proposal | a README or doc-comment update may replace the doc page |
| **Standard** | One feature, multiple components. Splitting it into testable pieces is normal, not a reason to split the feature; a piece worthless on its own belongs to it | `spec.md`, `plan.md`, `tasks.md` | 1–7 | `docs/<slug>.md` |
| **Large** | Bundles capabilities each shippable and valuable on their own, not merely testable on their own | `specs/<parent-slug>/scope.md`, then a full set per capability | 0, then 1–7 per capability | one page per capability |

**A Trivial change is still gated.** Run the existing quality gates once before changing anything; only new failures against that run block. Then self-review the diff against the junk-code checklist. A gate that cannot execute (missing service, dependency or config; a run that collects nothing) has not passed. Say so, and if correctness depends on it, treat the work as Small.

At Small, wherever a phase or reference says `plan.md` or `tasks.md`, use the matching part of the collapsed `spec.md`; gates, **Base**, **Integration**, tasks, gaps and reports sit next to `## Tasks`. Resolve every `[NEEDS CLARIFICATION]` before drafting the tasks half, then present the whole file as the proposal.

- State the depth in one line before starting. For Trivial ("treating this as Trivial — no spec") it is the user's chance to object. When unsure, ask in one sentence.
- Not starting at Phase 1? Name the entry mode in that line instead: `Phase-7-only`, `Resuming work` (naming the feature) or `Audit mode`.
- If the work reveals a larger scope than classified, stop and re-classify upward: read [references/writing-specs.md](references/writing-specs.md) → Depth now. Read it too when the user directs a lighter depth, or the work outgrows its depth's size; neither is a re-classification.

## Workflow

| Phase | Output artifact | Status after | Stop? |
|---|---|---|---|
| **0 — Scope check** *(Large only)* | `specs/<parent-slug>/scope.md` | rows `pending` | **yes** — the split and its order |
| **1 — Specify** | `specs/<slug>/spec.md` | `draft` | no |
| **2 — Clarify** | the same `spec.md`, no markers left | `draft` | no — questions only |
| **3 — Plan** | `specs/<slug>/plan.md` | `draft` | no |
| **4 — Tasks** | `specs/<slug>/tasks.md`, then the proposal | all three `in-review` → `approved` on sign-off (`pending sign-off: <role>` where a named signer is absent) | **yes** — spec + plan + tasks as one proposal |
| **5 — Implement** | code; checked boxes and completion notes in `tasks.md` | artifacts stay `approved` | no |
| **6 — Document** | `docs/<slug>.md`, README/CHANGELOG/doc comments | artifacts stay `approved` | no |
| **7 — Verify** | verdict table, `G#` gap tasks and a dated report block in `tasks.md` | `implemented` on `spec.md` and `plan.md` once merged and converged; `tasks.md` stays `approved` | **yes** — the gap tasks |

`draft` means produced but not yet presented. `superseded` and `abandoned` are set by `lifecycle.md` → Change requests mid-flight.

**Before presenting any artifact**, run `python3 <this skill's directory>/scripts/validate.py specs/<slug>` (at Small, pass the collapsed `spec.md`) and fix every error first. It checks the header, leftover markers, unique ids, and that every `R#`/`E#`, `C#` and task id cross-references. Never redo those checks by hand.

### Phase 0 — Scope check *(only for Large — stop for approval)*

- List each capability with a stable slug, a one-line responsibility, and its dependencies on the others.
- Propose the split and an order. Get approval.
- Write the approved split to `specs/<parent-slug>/scope.md` from `assets/scope-template.md`, one row per capability, following the row semantics it states. A row is `done` on the bar Phase 7 sets **implemented** on: merged and converged.
- Then run Phases 1–7 per capability, in dependency order.

### Phase 1 — Specify

Produce `specs/<slug>/spec.md` from `assets/spec-template.md`. Read [references/writing-specs.md](references/writing-specs.md) now; it governs every bullet below.

- Work its Starting the spec section first: say what you understood, read any requirements document the repo holds, and test the slug.
- Fill **Owner**, **Sign-off** (rows from [references/sign-off.md](references/sign-off.md)) and **Tracking** from the repo, never from assumption. Run [references/team-and-review.md](references/team-and-review.md) → Team signals now, at every depth, and follow the path it picks.
- Capture **what** and **why**, never *how*. State the non-goals explicitly.
- Turn every requirement into acceptance criteria. Close Requirements with a **Minimum shippable** line.
- Fill the coverage lines (Surfaces, Operational criteria, Sensitive ground), listing only what applies. Operational items apply only where the feature faces users or runs in production; accessibility only to a UI surface. **Sensitive ground** stays strict: `none touched`, or all five items walked with `R#`/`E#` or a non-goal.
- Define measurable **success criteria** with stable `SC#` ids, in the template's `**Signal**` / `**Read at**` / `**Emitted by**` shape: real-world checks beyond tests passing. If this feature must emit the signal, emitting it becomes a component and a task. Small omits them; at Standard and above an empty section is a `[NEEDS CLARIFICATION]`.
- Mark anything you assumed or cannot answer with `[NEEDS CLARIFICATION: question]` inline.

### Phase 2 — Clarify *(questions, not a stop)*

Resolve every `[NEEDS CLARIFICATION]` marker before planning. With none, skip this phase.

- Ask the open questions batched, most consequential first, each with a default ("X or Y? I'd default to X because…").
- Fold the answers into `spec.md` and delete the markers.
- Record **every** answer in Decisions. For "you decide", record the decision *and its rationale*.

Exit: zero markers. The proposal needs everyone the **Sign-off** line names (core rule 2).

### Phase 3 — Plan

Produce `specs/<slug>/plan.md` from `assets/plan-template.md`. Read the codebase first: the plan names real files, real modules and the project's conventions.

- **In flight** — find specs whose plan claims files or symbols this plan touches. Record the result on the **In flight** line and surface any overlap in the proposal. On Phase 1's solo path, check this tree's `specs/` only; otherwise read `team-and-review.md` → Overlap scan now and run it.
- **Quality gates** — discover the project's tooling: linter, formatter, type checker, test runner, and any other check its CI or scripts run (accessibility, security or dependency scan, size or performance budget, contract check). Read [references/verification.md](references/verification.md) → Recording gates now and follow it for the gates table and **Measurements**. Phase 3 runs nothing; baselines wait for Phase 5. Every recorded gate binds every task.
- **Integration** — record how the change set reaches its base branch on the **Integration** line, next to **Base**. Read `team-and-review.md` → Integration now and follow it.
- **Architecture** — map how the repo organizes code and where each kind of thing lives; record it in Current state. With no coherent pattern, say so and follow the local convention of the area touched. Never introduce a new architecture as a feature's side effect; that is its own spec.
- **Reuse first** — before planning new code, search by behavior, not name: grep the domain terms, read the shared/core/util areas, check what similar features call. **Reuses** names what each component extends or calls. A near-miss it repeats anyway goes on **Duplicates**, with why extraction is not the answer; the approver sees it in the proposal. Prefer extending a module, within its responsibility, over a parallel one. Read the manifest before reaching outside, and extend a declared dependency that nearly fits.
- **Components** — what to build or change, dependency order, risks with mitigations, what can run in parallel. Place each where the mapped architecture puts that kind of thing, or state why not.
- Answer three questions, each with a default:
  - **Data changes** — does any component change the shape of stored data (a field added, removed, retyped, renamed or re-meant) or the values already stored? Default `— none`.
  - **Delivery** — does reaching users need more than the normal release (a flag, new config or secret, a job registration, an ordered rollout, a manual step)? Default `— ships with the normal release`.
  - **Dependencies** — does it add, change or retire a third-party dependency, or call an external service at runtime? Default `— none`.

  For any non-default answer, read the matching reference before writing that line and follow its checklist: [references/data-and-delivery.md](references/data-and-delivery.md) for the first two, [references/dependencies.md](references/dependencies.md) for the third. A dependency change is never a task's side effect. A version change no `R#`/`E#` needs is its own spec discussion.
- Run `scripts/validate.py` and fix every error: each `R#`/`E#` needs a component, and a component implementing nothing is cut.
- Draft only; it is presented with the proposal.

### Phase 4 — Tasks *(then stop: the proposal)*

Produce `specs/<slug>/tasks.md` from `assets/tasks-template.md`.

- Each task fits one focused session, names its files, and carries its own acceptance criteria.
- Each task's **Verify** names the evidence for its **Implements** ids: the test, the measurement command for a number, or the stand-in for a third-party call. Phase 7 starts from these lines. Every live `R#`/`E#` needs one.
- Where nothing here can produce that evidence (no test runner, or a criterion needing a real HTTP call, browser or device), propose a minimal setup now. If the user declines, record the refusal as a Decisions entry; **Verify** then names the manual check the user approved ([verification.md](references/verification.md) step 2's exception). Found at Phase 7 instead, it leaves a requirement that cannot be evidenced.
- Order by dependency. Mark parallel tasks `[P]` with the contiguity semantics the tasks template states; the plan's Build order names no parallel groups.
- Include the documentation task (Phase 6).
- Run `scripts/validate.py`; fix every error.
- Set `spec.md`, `plan.md` and `tasks.md` to `in-review` and present them as the proposal, with the magnitude in one line: the task count, every task naming more than 3 files or more than one component flagged as large, and the depth's stated size. One sign-off sets all three `approved`.

### Phase 5 — Implement

Entering Phase 5: read [references/implement.md](references/implement.md) now and follow it. It starts with the baseline run, then sets the branch, task-claim, gate and pause rules.

### Phase 6 — Document

Entering Phase 6: read [references/implement.md](references/implement.md) → Phase 6 now and follow it.

### Phase 7 — Verify *(stop for approval)*

When every task is done, waived, deferred or blocked on the user's own execution, read [references/verification.md](references/verification.md) now and follow it end to end, through its Terminal status. Audit mode (a `spec.md` with shipped code but no plan or tasks): read its Audit mode section.

## Change requests and resuming

New or different behavior after approval enters through the spec: read [references/lifecycle.md](references/lifecycle.md) → Change requests mid-flight now. The one-line test: if the diff you are about to write isn't covered by the current spec, stop and amend the spec first.

Picking up an existing feature: read [references/lifecycle.md](references/lifecycle.md) → Resuming work now and follow it.

## Templates

- [assets/spec-template.md](assets/spec-template.md) — specification
- [assets/plan-template.md](assets/plan-template.md) — implementation plan
- [assets/tasks-template.md](assets/tasks-template.md) — task breakdown
- [assets/scope-template.md](assets/scope-template.md) — Large-split capability map (Phase 0)
- [assets/doc-template.md](assets/doc-template.md) — feature documentation
