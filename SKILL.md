---
name: spec-driven
description: Spec-driven development (SDD) workflow for software features. Guides work through phases — specify, clarify, plan, tasks, implement, document, verify — producing spec.md, plan.md, and tasks.md before code, enforcing clean-code gates, stored-data changes (migration, backfill), delivery (config, flags, rollout, kill switch), dependencies (license, pinning, contracts), scope cuts, and team integration (review, sign-off). Use when the change is worth a written requirement — a reviewer could answer "done or not done?" about it: starting a new feature, resuming or continuing an in-flight feature, a bug fix that changes behavior, porting or rewriting an existing module, a schema migration, backfill, rollback, a staged rollout, integrating an external API, defining performance, accessibility, or observability criteria, cutting scope for a deadline, taking code-review feedback into a spec, a feature handover, or when the user mentions SDD, spec-first, or writing a spec before coding. Also use to audit existing code against an existing spec (Phase 7 → Audit mode). Do not use for: a single dependency add or version bump with no behavior change, a one-file fix, a rename, formatting, or when the user has already said what to build and how.
license: MIT
metadata:
  author: Lucke514
  version: "3.1.0"
---

# Spec-Driven Development

Write the spec before the code. The spec — not the conversation — is the source of truth for what is being built, why, and how you will know it is done. Code is the output generated *against* the spec, every phase produces an artifact on disk that survives the session, and nothing ships without passing the quality gates and leaving documentation behind.

## Core rules

1. **No implementation before an approved spec.** If the user asks to build something non-trivial and no spec exists, start at Phase 1 (Phase 0 if the request is Large) — do not start coding.
2. **Stop for human review between phases.** Present each artifact (spec, plan, tasks) and get explicit approval before moving on — never chain spec → plan → tasks → code in one uninterrupted run. Set its Status as the phase table says: `in-review` when you present it, `approved` once the user signs off; on a change request, revise and re-present — it stays `in-review` until sign-off. No artifact carries `approved` without having existed as `in-review` first: the stop leaves a trace, or it did not happen. The spec's review stop is Phase 2's exit, so Phases 1–2 are one unit: never ask for approval while `[NEEDS CLARIFICATION]` markers remain.

   The user may waive the review stops ("run the remaining phases without asking me"): record the waiver as a Decisions entry in `spec.md` and mark the affected artifacts `approved` on that standing instruction — every artifact is still written and presented, just not blocked on. **A waiver covers exactly two things: the phase review stops, and Phase 7's approval to implement gaps, for work inside the approved scope.** It never covers a row of the table below — those approve what the feature promises, destroys, or ships, not the pace of the workflow.

   **If no one is answering.** In a non-interactive session (a subagent, a `-p` run, a CI job, a scheduled agent), or when a question simply goes unanswered, never guess past a stop and never delete: write the phase's artifact, leave its Status `draft`, say in one line what would have been asked and what it blocks, and stop with the artifact on disk. That artifact is the handoff — Resuming work picks it up. At Phase 7 the artifacts are already `approved`, so the report block is where the stop lands instead: leave the pass `Converged: no — awaiting <the decision>` and never write the verdict, annotation, or sign-off the stop was for. Silence is not a waiver: it grants no approval, and no work a stop gates starts on it.

   **Always needs explicit sign-off — a waiver never covers these.** This table is the one list: the spec's **Sign-off** line carries one line per row this feature actually raises — including a row raised mid-flight — and nothing else.

   | Item | Rule lives in | Recorded as |
   |---|---|---|
   | The spec's own content | Phase 2 — Clarify | Status set `approved` on that role's answer; a relayed answer also gets a dated Decisions entry |
   | A sensitive-ground `R#`/`E#` (auth, personal or regulated data, secrets, money) | [references/writing-specs.md](references/writing-specs.md) → Sensitive ground | a dated Decisions entry, plus the row it adds to the **Sign-off** line |
   | Adding or changing an `R#`/`E#`/`SC#` | Change requests mid-flight | the new or changed id, plus a dated Decisions entry |
   | Annotating an `R#`/`E#` **superseded** | Change requests mid-flight | `— superseded by …` on the requirement, plus a dated Decisions entry |
   | Deferring a requirement out of this change set | [references/writing-specs.md](references/writing-specs.md) → Minimum shippable & deferral | `— deferred (Decisions YYYY-MM-DD, owner <who>)` on it, that entry, and the open-follow-through filing |
   | Resolving spec drift | [references/verification.md](references/verification.md) → Handling gaps | the spec amendment with its dated Decisions entry, or the `G#` task that fixes the code |
   | Accepting a requirement as a documented limitation | [references/verification.md](references/verification.md) → Convergence loop | `— accepted limitation (Decisions YYYY-MM-DD, accepted by <who>)` on the requirement, plus that Decisions entry |
   | Closing a Phase 7 gap as **waived** — the user declines the fix | [references/verification.md](references/verification.md) → Convergence loop | `- [~] Waived — YYYY-MM-DD, why` on that `G#`, a dated Decisions entry, and the report's `Waived:` line |
   | Implementing a Phase 7 deletion gap | [references/verification.md](references/verification.md) → step 6 | the user's confirmation on that `G#` and the report's `Dead-code sweep:` line |
   | Removing, disabling, or weakening a pre-existing test (unless an `R#` specifies it) | [references/verification.md](references/verification.md) → step 4 | the report's `Tests removed:` line, naming the test and the approval |
   | Accepting a manual verification as a requirement's only evidence | [references/verification.md](references/verification.md) → step 2 | a dated Decisions entry in `spec.md`, cited on the Phase 7 report |
   | Adding a third-party dependency, or changing the version of one other code shares | [references/dependencies.md](references/dependencies.md) | the plan's **Dependencies** line, approved with the plan |
   | Executing a data change the plan records as irreversible or data-losing | [references/data-and-delivery.md](references/data-and-delivery.md) → Stored-data checklist | a dated Decisions entry per change, naming what makes recovery possible |
   | Running any data-change command — reversible ones included — against a shared, staging, or production datastore | [references/data-and-delivery.md](references/data-and-delivery.md) → **Target** / **Who executes it** | the user's go-ahead per command and target, with the result on the report's `Data & delivery:` line |
   | Executing a delivery step (deploy, stage promotion, flag or config change) against a shared, staging, or production environment | [references/data-and-delivery.md](references/data-and-delivery.md) → Delivery checklist | the user's go-ahead per step and environment, with the result on the report's `Data & delivery:` line |

   An item whose **Sign-off** line names a signer other than the person in this session is not approved by that person's answer — read [references/team-and-review.md](references/team-and-review.md) → Sign-off authority now and follow it.
3. **Artifacts live in the user's repo**, under `specs/<feature-slug>/` (slug: short, lowercase, hyphen-separated, unique across the repo, stable for the feature's lifetime — it also names the branch, the commit prefix `<slug>: `, and `docs/<slug>.md`):
   ```
   specs/
   └── user-authentication/
       ├── spec.md      # what & why — requirements, acceptance criteria
       ├── plan.md      # how — architecture, components, risks
       └── tasks.md     # work breakdown with per-task verification
   ```
   In a monorepo, place `specs/` and `docs/` at the root of the package that owns the code — not the repo root — keeping them siblings so the templates' relative links resolve. If no single package owns the feature, put them at the repo root (or the shared/platform package), list the affected packages in the plan's Current state, and follow each package's own documentation convention for its half of the doc page. Whenever a phase edits an artifact — checkboxes, completion notes, amendments, Status changes, appended reports — set that artifact's `Last updated` to the current date.
4. **Requirements must be testable.** Every requirement in the spec is written so that a reviewer can answer "done or not done?" with a yes/no. Rewrite vague asks ("fast", "user-friendly", "secure") as measurable criteria.
5. **When the spec and the code disagree, the spec wins** — either fix the code, or change the spec explicitly with the user's approval. Never let them drift silently.
6. **No junk code — ever.** A task is not done while its diff contains dead code, debug leftovers, or duplication. The full checklist is in [references/clean-code.md](references/clean-code.md) — requirements, not suggestions; load it when you first self-review a diff (Phase 5, or a Trivial change).
7. **A feature is not done until it is documented.** Phase 6 produces documentation inside the repo; verification checks it like any other requirement. That doc page is a spec deliverable the user asked for by starting this workflow, not proactive documentation — where the host agent you run inside forbids creating `.md` files unbidden, say so in one line and use the README/doc-comment form the Small row already allows.

## Adaptive depth

Scale the ceremony to the work. Classify before starting:

| Depth | Test | Artifacts | Phases run | Docs form |
|---|---|---|---|---|
| **Trivial** | Nothing observable changes for a user of the code and there is nothing a requirement could be written about — typo, rename, comment, formatting, version bump. If you could state the change as an `R#` with a Given/When/Then, it is at least Small. The test runs over the request **as a whole**: one clause in it that is at least Small makes the whole request at least Small — never split one request into clauses of different depths | none — no spec, no plan, no tasks, but the change is still gated (below) | none | — |
| **Small** | One capability, < ~1 day | one collapsed `spec.md`: header block (Status, Owner, Sign-off, Tracking, Last updated), Objective, **Users & scenarios** with its coverage lines, Requirements, Non-goals (one line is fine), Edge cases, Decisions, then `## Tasks` in the tasks format without the **Component** field (tasks cite `R#`/`E#` directly); no Success criteria. Recorded next to those tasks: the gate commands with their baselines, the **Measurements**, **Base**, **Integration** and **Task span** lines, the branch set the overlap scan covered, the **Evidence per requirement** table, and the **Data changes** / **Delivery** / **Dependencies** lines. **Owner**, **Sign-off**, and **Tracking** default to `— the session's user holds all of these` and `— this project tracks work in the repo only` without running Discovery — run Discovery only where a `CODEOWNERS` entry covers a path this change touches. The overlap scan at Small is `ls specs/` in this tree; branch enumeration is Standard and above | 1, 2, 5, 6, 7 — plus Phase 3's tooling discovery, its minimal-setup proposal included; 0, 3, 4 skipped | a README or doc-comment update may replace the doc page |
| **Standard** | One feature, multiple components. Decomposing into independently testable pieces is normal and is not a reason to split — a piece worthless on its own (a restore with nothing to restore from) belongs to this feature | `spec.md`, `plan.md`, `tasks.md` | 1–7 | `docs/<slug>.md` |
| **Large** | Bundles capabilities that are each shippable and valuable on their own, not merely testable on their own | `specs/<parent-slug>/scope.md`, then a full set per capability | 0 first, then 1–7 per capability | one page per capability |

**A Trivial change is still gated.** Run the project's existing quality gates once before changing anything and treat only new failures against that run as blocking — there is no plan to record a baseline in — then self-review the diff against the junk-code checklist (core rule 6). A gate that cannot execute at all — missing service, dependency, or config; a run that collects nothing — is not a passed gate: say so explicitly, and if the change's correctness depends on it, treat the work as Small.

At Small, wherever the workflow or a reference says `plan.md` or `tasks.md`, use the matching part of the collapsed `spec.md` — gates, **Base**, **Integration**, and tasks next to `## Tasks`, verification gaps and reports appended there too. Baselines and **Base** are measured exactly as Phase 3 says. Phases 1–2 still close first: resolve every `[NEEDS CLARIFICATION]` and get the spec half approved before drafting the gates-and-tasks half of the same file.

- State the chosen depth in one line before starting — for Trivial, that line ("treating this as Trivial — no spec") is the user's chance to object. When unsure, ask which depth the user wants instead — one sentence, not a questionnaire.
- Where the session does not start at Phase 1, state the entry mode in that same one line instead — `Phase-7-only`, `Resuming work` (naming the feature), or `Audit mode` — so the user can redirect before any artifact is read.
- If work at any depth reveals a larger scope than classified, stop and re-classify upward — read [references/writing-specs.md](references/writing-specs.md) → Depth now and follow it.
- If the user directs a lighter depth than the size suggests, or the artifacts show the work has outgrown the size its depth states, read that same section now — neither is a re-classification.

## Workflow

| Phase | Output artifact | Status after | Stop? |
|---|---|---|---|
| **0 — Scope check** *(Large only)* | `specs/<parent-slug>/scope.md` | rows `pending` | **yes** — the split and its order |
| **1 — Specify** | `specs/<slug>/spec.md` | `draft` → `in-review` | no — Phases 1–2 are one unit |
| **2 — Clarify** | the same `spec.md`, no markers left | `approved` on sign-off (`pending sign-off: <role>` where a named signer is absent) | **yes** |
| **3 — Plan** | `specs/<slug>/plan.md` | `draft` → `in-review` → `approved` | **yes** |
| **4 — Tasks** | `specs/<slug>/tasks.md` | `draft` → `in-review` → `approved` | **yes** |
| **5 — Implement** | code; checked boxes and completion notes in `tasks.md` | artifacts stay `approved` | no |
| **6 — Document** | `docs/<slug>.md`, README/CHANGELOG/doc comments | artifacts stay `approved` | no |
| **7 — Verify** | verdict table, `G#` gap tasks and a dated report block in `tasks.md` | `implemented` on `spec.md` and `plan.md` once merged and converged; `tasks.md` stays `approved` | **yes** — the gap tasks |

`draft` is the state of an artifact that has been produced but not yet presented — what an interrupted session leaves on disk. Resuming work triages it like any other in-flight state. `superseded` and `abandoned` are set by the rules in Change requests mid-flight.

### Phase 0 — Scope check *(only for Large — stop for approval)*

If the request bundles multiple capabilities that could each ship and deliver value on their own, map them before writing anything:

- List each capability with a stable slug, a one-line responsibility, and its dependencies on the others.
- Propose the split and an order. Get approval.
- Write the approved split to `specs/<parent-slug>/scope.md` from `assets/scope-template.md`, one row per capability, following the row semantics it states. A row is `done` on the same bar Phase 7 sets **implemented** on: merged and converged, not merely converged.
- Then run Phases 1–7 per capability in dependency order.

### Phase 1 — Specify

Produce `specs/<slug>/spec.md` from `assets/spec-template.md`. Read [references/writing-specs.md](references/writing-specs.md) now — it governs every bullet below.

- Work `writing-specs.md` → Starting the spec first: say what you understood before anything else, read any requirements document the repo already holds, and test the slug against surviving evidence.
- Fill the header's **Owner**, **Sign-off**, and **Tracking** lines from the repo, never from assumption: read [references/team-and-review.md](references/team-and-review.md) → Discovery now and work its checklist.
- Capture **what** and **why** — never *how* — and state the non-goals explicitly.
- Turn every requirement into acceptance criteria, and close the Requirements section with a **Minimum shippable** line.
- Name the surfaces the feature exposes, the sensitive ground it touches, and — where the feature faces users or runs in production — its operational criteria. Walk the row or checklist each one brings in `writing-specs.md`, and cover every item with an `R#`/`E#` or an explicit non-goal, recorded item by item on the spec's coverage lines so a blank is visible. Anything you cannot answer becomes a `[NEEDS CLARIFICATION]`.
- Define measurable **success criteria** with stable `SC#` ids — real-world checks beyond tests passing, in the template's `**Signal**` / `**Read at**` / `**Emitted by**` shape; where this feature must produce that signal, emitting it becomes a plan component and a task, never an assumption. The collapsed Small spec omits them; at Standard and above an empty section is a `[NEEDS CLARIFICATION]`, never a valid state.
- Mark anything you had to assume with `[NEEDS CLARIFICATION: question]` inline.

### Phase 2 — Clarify *(stop for approval)*

Before planning, resolve every `[NEEDS CLARIFICATION]` marker:

- Ask the open questions, batched, most-consequential first, each offering a default ("X or Y? I'd default to X because…") — that gets faster, better answers than an open question.
- Fold the answers back into `spec.md` and delete the markers.
- Record **every** answer in the spec's Decisions section — including, where the user said "you decide", the decision *and its rationale*.

Exit criteria: zero markers left, and the spec approved by everyone its **Sign-off** line names (core rule 2).

### Phase 3 — Plan *(stop for approval)*

Produce `specs/<slug>/plan.md` from `assets/plan-template.md`. Read the actual codebase first — the plan must reference real files, real modules, and the project's existing conventions, not a greenfield fantasy.

- **Other features in flight** — run the overlap scan ([references/team-and-review.md](references/team-and-review.md) → Overlap scan, read it now) to find the specs whose plan claims files or symbols this plan touches, and record its result in the plan's Current state. Surface any overlap to the user before asking for approval.
- **Quality gates and evidence** — discover the project's quality tooling (linter, formatter, type checker, test runner, plus any other check it already runs in CI or its scripts — accessibility, security or dependency scan, size or performance budget, contract/schema check), then read [references/verification.md](references/verification.md) → Recording gates now and follow it — it governs the Quality gates table and its baselines, the **Base** and **Measurements** lines, and the **Evidence per requirement** walk. Every recorded gate is a mandatory check for every task.
- Record how this change set reaches its base branch as the plan's **Integration** line, next to **Base**: read [references/team-and-review.md](references/team-and-review.md) → Integration now and follow its checklist.
- Map the architecture before proposing components: how the repo organizes code (layers, feature folders, modules, hexagonal — whatever the tree actually shows) and where each kind of thing lives; record it in the plan's Current state. Where no coherent pattern exists, say so there and follow the dominant local convention of the area being touched — never introduce a new architecture as a side effect of a feature; proposing one is its own spec.
- Search for reusable code before planning any new code — search by behavior, not name: grep the domain terms, read the shared/core/util areas, check what similar features call. Each component's **Reuses** line names what it extends or calls; where the search found a near-miss this component will repeat instead of extending, its **Duplicates** line names that module and why extraction is not the answer — a non-empty **Duplicates** is a Phase 3 item the approver sees, not a Phase 7 surprise. New code is the fallback, not the default: prefer extending an existing module, within its responsibility, over a parallel one. Reuse-first covers third parties too: read the manifest before reaching outside, and extend a declared dependency that nearly fits like internal code.
- Identify components to build/change, dependency order between them, risks with mitigations, and what can proceed in parallel. Place every component where the mapped architecture says that kind of thing lives; one that breaks the pattern needs a stated reason in the plan.
- Record three lines in the plan — each is a question with a default answer:
  - **Data changes** — does any component alter the shape of stored data (new or removed field, changed type, changed meaning, rename) or the values of data already stored? Default `— none`.
  - **Delivery** — does the feature need anything beyond the project's normal release to reach users (a flag, a new config value or secret, a job/schedule registration, an ordered rollout, a manual step)? Default `— ships with the normal release`.
  - **Dependencies** — does the feature add a third-party dependency, change the version of one already present, retire one, or call an external service at runtime? Default `— none`.

  If any answer is not its default, read the matching reference now, before writing that line, and follow its checklist: [references/data-and-delivery.md](references/data-and-delivery.md) for the first two, [references/dependencies.md](references/dependencies.md) for the third. A dependency change is never a task's side effect, and a version change no `R#`/`E#` here needs is its own spec discussion, like a new architecture.
- Every requirement and edge case (`R#`, `E#`) in the spec must map to at least one component in the plan. If something in the plan implements nothing from the spec, cut it.
- Stop and get approval.

### Phase 4 — Tasks *(stop for approval)*

Produce `specs/<slug>/tasks.md` from `assets/tasks-template.md`.

- Each task is completable in one focused session, names the files it touches, and carries its own acceptance criteria and a concrete verification step (a command to run, a test that must pass — or, where the project has no runnable test runner and the user declined the setup proposed in Phase 3, a manual check the user approved).
- Order by dependency; mark tasks that can run in parallel with `[P]`, whose contiguity semantics the tasks template states — the plan's Build order names no parallel groups of its own.
- Every plan component must be covered by at least one task.
- Include the documentation task (Phase 6's work).
- Stop and get approval. Present the magnitude with the list, in one line: the task count, every task that names more than 3 files or more than one component flagged as large, and the size the chosen depth states — so the approver can object to the commitment before approving it instead of after.

### Phase 5 — Implement

Execute `tasks.md` in order:

- If the repo uses git, do the feature's work on a branch named for the slug — or prefix its commits with `<slug>: ` — so Phase 7 can reconstruct the change set later. Before the first commit, confirm the plan's **Base** line: the branch point where the feature has its own branch, the tip of the shared branch at that moment where its commits are slug-prefixed. Commit as tasks land where the user allows commits; uncommitted work stays in the tree for Phase 7 to see, but it is invisible to every other session and clone and so is never a handoff state: before handing the feature over or leaving it, commit it or record it in the task's note as `uncommitted, local to <who>`.
- One task at a time, and only a task nobody else holds: before starting, confirm its **Owner** is `—` here and — where the feature's work spans branches — in the same slug's `tasks.md` on the other active branches (run the overlap scan — [references/team-and-review.md](references/team-and-review.md)); then claim it by setting **Owner** to who (or which branch) is executing it plus today's date. Re-read `tasks.md` before writing to it; two sessions writing it at once conflict in the one file the workflow trusts. Release the claim (**Owner** back to `—`) on completion or handback. A claim dated more than 7 days ago is stale, not held, unless the plan records a different **Task span** — ask the user before taking it. Load only the spec/plan sections relevant to the current task.
- **Commit the claim before writing a line of code — one commit, always**, whatever the scan found: a second session in this same clone is invisible to it, and that commit is the only artifact showing the task was held before it was worked.
- Write or update tests that encode the task's acceptance criteria — tests are the executable form of the spec. Where the project has no runnable test runner and the user declined the setup proposed in Phase 3, the task's `Verify:` is instead the user-approved manual check Phase 4 recorded, cited with its observed output ([references/verification.md](references/verification.md) step 2).
- Write code that reads like the surrounding codebase: same conventions, naming, structure.
- Before marking a task done, pass the gates: run the task's verification step **and** every quality gate recorded in the plan with no new failures against its baseline, then self-review the diff against the junk-code checklist in [references/clean-code.md](references/clean-code.md) — read it now if this is the session's first self-review. The sweep leaves a record on the completion note in the shape that file states, so an unrun sweep is a blank field rather than an invisible omission.
- Update the task's checkbox and add a one-line completion note in `tasks.md` as you go.
- **A task only the user can execute** — a data change or delivery step against a shared, staging, or production environment, anything gated on access this session does not have — is `- [!] Blocked — YYYY-MM-DD, <what the user must do>`: not `Done`, not `Waived` (nothing was declined), not `Deferred` (it *is* in this change set). It is exempt from Phase 7's entry condition the way a `pipeline-only` gate is exempt from a local baseline, and its requirements take the **blocked (execution pending)** verdict ([references/verification.md](references/verification.md) step 3) — but it stays **open**: file it as open follow-through with an owner and a date, and it blocks the terminal status below.
- If implementation must pause — because it reveals the spec or plan is wrong, or because new information arrives mid-task (review feedback, a changed constraint, an answer that moves the target) — **stop**, and write the stop down before acting on it: a dated Decisions entry (or the task's **Notes**) naming what looks wrong and what is blocked, so a session that ends unanswered leaves the stop on disk the way `pending sign-off: <role>` does. Then size it. A plan omission that changes no component boundary — a helper the plan's `C#` never named, a file that plainly belongs to an existing component — is amended in place on the user's one-line confirmation and noted on that component. Anything that moves behavior between components, changes the architecture, or changes what the spec promises goes back to the affected phase and is amended with the user there. Do not improvise around the spec either way.
- **A deliberate shortcut is declared, never silent** — the rule and its record are in [references/clean-code.md](references/clean-code.md) → Declared shortcuts, which this phase already loads.

### Phase 6 — Document

Documentation lives in the repo and ships with the feature:

- Produce `docs/<slug>.md` from `assets/doc-template.md`: what the feature does, how to use it, its public API/interface, and a link back to `specs/<slug>/` for the full history. The template's **Operating** section is filled — and only filled — where the plan's **Delivery** is not `— ships with the normal release`, the spec carries an operational-signal `R#`/`E#`, or the plan's **Dependencies** line records an external service the feature calls at runtime; remove it otherwise.
- Update the project's existing entry points: README (if the feature is user-facing), CHANGELOG (if the project keeps one), and doc comments on the public interfaces the feature exposes.
- Follow the project's existing documentation conventions if it has any (`docs/` layout, docstring style, ADRs); create the `docs/` folder only if nothing exists yet. Where a Decisions entry binds beyond this feature — an architecture pattern, a shared dependency, a cross-cutting convention, a targeted contract version — and the project keeps its own decision record (`docs/adr/`, `decisions/`, an RFC folder, discovered by reading the repo), write that entry there too in the project's format and link it both ways with the spec's Decisions line; where the project keeps none, say so in one line and never start the practice uninvited.
- Documentation describes behavior as specified — if writing it exposes a mismatch with the code, that is spec drift: handle it in Phase 7, don't paper over it.

### Phase 7 — Verify *(stop for approval)*

When every task is done, waived, deferred, or blocked on the user's own execution, run a convergence pass — read [references/verification.md](references/verification.md) now and follow its procedure end to end. Two things live here rather than there:

- **The waiver carve-out.** Gaps are reported, then approved, then implemented via Phase 5. A standing waiver recorded under core rule 2 covers that approval — gaps are still reported, just not blocked on — except any gap whose resolution appears in a row of core rule 2's table, which needs the explicit sign-off that table requires. Read the table, row by row, against the gap you are about to implement; do not work from a remembered list of it.
- **The terminal status.** Once the change set is merged into the branch the plan's **Base** names, set `spec.md` and `plan.md` to **implemented** — which means merged and verified *in the repo*, never that the feature is live: where the plan's **Delivery** records rollout stages the feature has not finished, state that on the spec's Status line (`implemented — rollout in progress, stage <the one it is at>`) with a dated owner for the final stage, the way an introduced flag carries a retirement owner, and reduce it to plain **implemented** when the last stage completes. A standing `- [!] Blocked` task qualifies it the same way — `implemented — T4 blocked, <what the user must run>, owner <who>` — and reduces to plain **implemented** once that run lands and a pass re-verifies the requirements it evidences. `tasks.md` stays `approved` — its checkboxes, completion notes, and appended reports are its completion record (at Small the collapsed `spec.md` takes the spec's status and its `## Tasks` section is that record). A later feature replacing this one marks the old spec and plan **superseded** (linking to the successor) and the doc page **deprecated** — never delete the history.

**Audit mode** — a `spec.md` with shipped code but no `tasks.md` and no `plan.md` (the user asks whether existing code matches its spec): re-read the spec, walk its `R#`/`E#` for evidence as step 2 says, and report the verdict table with what it would take to close each gap. There is no change set here, so:

- **The path set is proposed and user-confirmed before the inventory is built** — a spec names behavior, never paths — listing the registries and config sources read with it.
- **Neither `blocked` verdict is available**: step 4 never runs, so every cause is outside a change set by construction, and a genuinely broken feature would file as not-our-problem. A failing check is *not met* or *partially met*.
- **Every `unreached` finding carries step 6's scope-of-analysis line**, which here attaches to findings, not to the deletion gaps this mode never files.
- **Output**: the verdict table, then `Scope of analysis:` (the confirmed path set plus what else was read) and `Not run:` (the gates, baselines, controls, and sweeps this mode skips). File no `G#`, append no report block, set no Status — the output is the report to the user, and turning it into work is a normal entry at Phase 1 or Phase 3.

## Change requests mid-flight

When new or different behavior is asked for after the spec is approved — by the user, or by a code reviewer or any third party whose feedback the user relays — the change enters through the spec, not the code:

- Amend `spec.md` first (new/changed `R#`/`E#`, a Decisions entry recording what changed and why), then update `plan.md` and `tasks.md` if the change touches them, then implement.
- Behavior feedback from a code review is a change request like any other, whoever relays it: it lands in `spec.md` first — never straight in the diff, or Phase 7 reports the reviewer's own decision as spec drift. Read [references/team-and-review.md](references/team-and-review.md) → Review feedback now and classify each comment before acting on it.
- For a Large split, if the change adds a capability, removes one, or moves behavior between capabilities, update `specs/<parent-slug>/scope.md` first (add or adjust the capability row, its depends-on, and its status) with the user's approval — then amend the affected capability's `spec.md` as usual.
- A clarification that changes no requirement → just a Decisions entry.
- If the change invalidates completed tasks, list which ones and get approval before redoing them.
- **Every artifact the amendment touches goes to `in-review` and stays there until sign-off, whatever Status it held** — `plan.md` and `tasks.md` as much as the spec: one left `approved` while its content is under revision claims a stop that did not happen. An **implemented** spec (and its `plan.md`) resets the same way and re-walks the normal lifecycle — `approved` on the user's sign-off, `implemented` again once the new `R#`/`E#` pass Phase 7. If the change replaces the feature's behavior wholesale, write a new spec and mark the old one **superseded** instead of reopening it. If it replaces only part of what *another* feature's spec still claims, amend that spec in the same approval — a Decisions entry plus `— superseded by specs/<successor-slug>/spec.md` on each affected `R#`/`E#`; supersede the whole artifact only when nothing in it stays live. That annotation is records-only: it does not reset an **implemented** Status — only adding or changing a live `R#`/`E#` does — and Phase 7 reports each annotated requirement as **superseded** rather than re-verifying it.
- **If the user cancels the feature at any phase**: set its artifacts' Status to **abandoned** with a Decisions entry saying why — never delete the directory. Then propose reverting whatever change set already landed (built the same way as the step-6 inventory in [references/verification.md](references/verification.md)) unless the user explicitly keeps parts; record what was kept or reverted in that entry, and mark any existing `docs/<slug>.md` **deprecated**. Every reverted task's `- [x] Done` goes back to `- [ ] Done` with a note naming the revert, so task state never claims code the tree no longer has. If the feature is a capability of a Large split, set its `scope.md` row to **abandoned** and, in the same approval, resolve every capability that depends on it — re-point, absorb, or abandon it too.

The one-line test: if the diff you are about to write isn't covered by the current spec, stop and amend the spec first.

## Resuming work

When picking up an existing feature: if the user named none, resume the one matching the current branch or the most recent `<slug>: ` commits; if they named it loosely ("carry on with the bulk actions thing") and exactly one open-work spec matches that reference, resume that one directly and say which — list the rest only where the match is not unique; otherwise read only the header block of each `specs/*/spec.md` and list the features whose Status is `draft`, `in-review`, or `approved`, plus any **implemented** one whose Status line records a rollout still in progress, whose Decisions hold an open dated follow-up of any kind [references/team-and-review.md](references/team-and-review.md) → Open follow-through lists, or whose `tasks.md` holds a `- [>] Deferred` or `- [!] Blocked` entry — those are open work — then ask which one. Skip `implemented` with none of those, `superseded`, and `abandoned`; a directory holding `scope.md` and no `spec.md` is a Large parent, see that bullet. Read the chosen feature's artifacts in order — if `specs/<slug>/` is absent here, the missing-artifact bullet below rules the branch case out first. Then take the first unchecked task no one else holds (**Owner** is `—` — Phase 5's claim rule; `- [~] Waived` is closed, `- [>] Deferred` is not due until its date, and `- [!] Blocked` waits on the user, not on you), naming it to the user before claiming it: state the task and what it will change, and that turn is their chance to redirect — proceeding after it is not silence, and a feature-level "continue" is not that naming.

The checks below run in order, with one dependency: where the drift check orders a diagnostic pass and an artifact that pass needs is missing, recover it under the missing-artifact bullet **first**, or run the pass in reduced form and say in the report which gates and which **Base** it could not read.

- **Work-present check** — before anything else, confirm each checked task's work is actually in *this* tree: its **Files** exist and its `Verify:` passes. A checked task whose work is absent here was never handed over — recover it from the branch or clone the task's note names, or reopen it (`- [x] Done` → `- [ ] Done`, with a note saying where it was last seen). Reopening never releases the claim: **Owner** is cleared only by its owner or by the user's answer, two actions with the ask in between. Never trust the checkbox alone, and never file a `G#` to re-implement a teammate's work before this check has run. A claim whose **Owner** names this session's own branch or user, on an unchecked task with no completion note, is a crashed claim, not a held one: re-run that task's `Verify:`, check its **Files**, then continue it or reopen it — never wait out its 7 days.
- **Drift check** — to tell whether code changed *outside* this feature since the artifacts were written, compare each artifact's `Last updated` date against `git log` for the paths the feature touches, discounting the feature's own work — commits on its branch, commits carrying the slug prefix, and the working tree its last completed task left behind are never drift; if anything else is newer, run Phase 7 as a diagnostic pass. Dates also mislead after a rebase or a merge from the base branch: run the rebase test on the plan's **Base** line, in the form that line's topology takes ([references/verification.md](references/verification.md) → Recording gates) — where it fires, treat the code as changed regardless of dates and run that pass, whose step 4 refreshes the stale baseline.
- **Artifact cross-check** — every spec `R#`/`E#` carries at least one task (for Small, in the collapsed `spec.md`'s `## Tasks` section) and, at Standard and Large, a row in the plan's Requirement coverage table; in reverse, no coverage row and no task's `Implements` may name an `R#`/`E#` the spec no longer has. Then check each artifact against its own history, discounting the workflow's own edits — checkboxes, completion notes, amendments, Status changes, appended reports, and `Last updated` bumps are legitimate in an `approved`/`implemented` artifact, committed on the feature's branch, under its `<slug>: ` prefix, or still uncommitted from its last completed task. What counts is an edit outside that set: a commit touching the artifact newer than its `Last updated` line (`git log -1 --format=%as -- <artifact>` — author date, which a rebase preserves where committer dates do not) and neither on the feature's branch nor `<slug>: `-prefixed, or an uncommitted change (`git diff -- <artifact>`) rewriting an `R#`/`E#`, its criteria, or the plan's components. Any such mismatch means the artifact was hand-edited — treat it as an unprocessed change request and run Change requests mid-flight first. An artifact the depth never produces (no `plan.md` at Small) is never a mismatch; one the depth should have produced but that is absent is the next bullet's case.
- **Missing or unrecoverable artifacts** — rule out the branch case first: if a branch named `<slug>` or another active branch (run the overlap scan) holds `specs/<slug>/`, nothing was lost — switch to that branch to resume it, or ask the user, and never restore copies into the current branch. Otherwise, if an artifact the lifecycle already produced (its upstream artifact is `approved` or `implemented`, or a downstream artifact references it) is missing or unreadable, restore it from git history; if it is unrecoverable, regenerate it from the surviving artifacts (`tasks.md` from the plan's components), leave every regenerated task unchecked, record the reconstruction as a Decisions entry in `spec.md`, get it re-approved, then run Phase 7 immediately as a diagnostic pass — its **met** verdicts, not memory of earlier sessions, decide which regenerated tasks are already done.
- **Stopped at an earlier phase** — a feature whose artifacts simply stop at an earlier phase resumes at that phase's exit: a `draft` artifact is presented for approval as its phase says, an `in-review` one re-presented — neither is lost, neither is re-specified from scratch.
- **Every task closed, Status still `approved`** — read the `Verification reports` section of `tasks.md` (for Small, the end of the collapsed `spec.md`'s `## Tasks` section). No report block, one whose `Converged:` line reads `no`, or a last pass still listing open gaps or verdicts other than **met**/**superseded**/**deferred**/**blocked**/an accepted limitation, means Phase 7 never converged — run it (an in-progress block names the step it stopped at; restart there), and never set **implemented** without a converged report block on record.
- **Large split** — read `specs/<parent-slug>/scope.md` first and pick the next capability whose dependencies are `done`; where several qualify, take the one the approved **rank** names first and report that choice rather than picking silently — a different order is a re-rank of those rows, with the user's approval. A `deferred` row is not a candidate until its date, and is reported alongside the in-flight rows so a cut capability stays visible. If none qualifies, report the blocking rows instead of stopping — an `abandoned` dependency is a scope decision (re-point, absorb, or abandon the dependent), never a permanent block.
- **Abandoned** — skip `abandoned` features unless the user explicitly reopens them; reopening sets `spec.md`, `plan.md`, and `tasks.md` back to `in-review` and the normal lifecycle re-applies. After re-approval, run Phase 7 immediately as a diagnostic pass — its **met** verdicts, not checkboxes left behind before the cancellation, decide which tasks are still done and where Phase 5 restarts.

## Templates

- [assets/spec-template.md](assets/spec-template.md) — specification
- [assets/plan-template.md](assets/plan-template.md) — implementation plan
- [assets/tasks-template.md](assets/tasks-template.md) — task breakdown
- [assets/scope-template.md](assets/scope-template.md) — Large-split capability map (Phase 0)
- [assets/doc-template.md](assets/doc-template.md) — feature documentation
