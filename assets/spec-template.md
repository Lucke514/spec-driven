# Spec: [Feature name]

> Status: draft  <!-- draft | in-review | approved | implemented | superseded | abandoned -->
> Owner: [who is accountable for this spec's content]
> Sign-off: [one line per approval-gated item this feature raises — spec content, sensitive-ground R#/E#, a new or version-changed dependency, an irreversible data change, a delivery step against a shared, staging, or production environment, accepting a requirement as a documented limitation — each naming the role that must approve it, read from the repo (CODEOWNERS, review policy, security/ops docs). `— the session's user holds all of these` is valid and common. An item whose signer is not in the session is recorded on the Status line as `pending sign-off: <role>` until that role answers, and no waiver covers it.]
> Tracking: [the team's work item for this feature — id or link — as discovered by reading the repo (issue and pull-request templates, the contribution policy, identifiers cited in existing docs and commits); or `— this project tracks work in the repo only`.]
> Last updated: [YYYY-MM-DD]

## Objective

[1–3 sentences: what this feature does and why it is worth building. If you cannot state the "why", stop and ask.]

## Users & scenarios

[Who uses this and in what situation. One short paragraph or bullet per scenario.]

- **[Scenario name]**: As a [user], when [situation], I want [capability] so that [outcome].
- **Surfaces**: [which of UI / API or contract / CLI / background job / data pipeline / library this feature exposes — each one brings its own class of acceptance criteria into Requirements, or an explicit Non-goal.]
- **Operational criteria**: [for a feature that faces users or runs in production — expected load and volume; the accessibility standard and level this project already commits to; user-visible text and locale-dependent formatting; the signal that shows the feature working or broken and where a human sees it; behavior when a dependency is slow or unavailable; where the feature writes in more than one place, what a failure between those writes leaves behind and what makes it consistent again. Each covered by a Requirement or Edge case, or an explicit Non-goal.]

## Requirements

[Each requirement is testable: a reviewer can answer "done or not done?" with yes/no. Use stable IDs — tasks and verification will reference them. A requirement another feature has replaced is never deleted: keep it and append `— superseded by specs/<slug>/spec.md`. A requirement verification could not make met and the user accepted as a documented limitation is annotated in place the same way: `— accepted limitation (Decisions YYYY-MM-DD)`. A requirement cut from *this* change set by an explicit decision — shipped later, not given up — is annotated in place too: `— deferred (Decisions YYYY-MM-DD, owner <who>)`. Never delete it, never move it to Non-goals, and never record it as an accepted limitation: those say the feature deliberately does not do this, while a deferral says it is not in this change set yet.]

- **R1** — [Requirement stated as an observable behavior.]
  - Given [precondition], when [action], then [observable result].
- **R2** — ...

**Minimum shippable**: [R1, R2, E1 — the smallest set that still delivers the Objective. The rest are worth building, but the feature is not pointless without them. A cut under deadline defers from outside this set; cutting into it cancels the feature instead of trimming it.]

## Non-goals

[What this feature deliberately does NOT do. Prevents scope creep and drift.]

- [Non-goal 1]

## Edge cases & error behavior

[What happens on bad input, empty states, concurrency, limits. Each entry is testable and carries a stable ID — plan and verification reference them like requirements. If the feature touches authentication or authorization, personal or regulated data, secrets, or money, it carries explicit entries here or in Requirements for access control, traceability, data handling, and — where it creates a new store of personal data — how that data is deleted and exported when its subject is — or Non-goals says in writing that it does not.]

- **E1** — When [edge condition], the system [expected behavior].
- **E2** — ...

## Decisions

[Choices made during clarification, with rationale. Append-only. A follow-up this feature defers — a flag retirement, the cleanup half of a data change, a provider move, a rollout's last stage, a requirement deferred out of this change set, the proper version of a deliberate shortcut — is dated, names its owner, and carries the identifier it got from the Tracking target; where the project tracks work in the repo only, it is also left in tasks.md as a `- [>] Deferred` entry, so a later session still sees it.]

- [YYYY-MM-DD] [Decision] — because [rationale].

## Open questions

[Unresolved items. Must be empty before the spec is approved.]

- [NEEDS CLARIFICATION: question]

## Success criteria

[How we know the feature works in the real world, beyond tests passing: metrics, manual checks, rollout conditions. Each entry carries a stable ID — verification walks and reports them by ID. Each criterion names the signal it reads (metric, log, dashboard, report); a criterion that can only be observed after rollout also names the environment it is measured in, and how. Where this feature must produce that signal, emitting it is planned work, not an assumption.]

- **SC1** — [Criterion, stated so it can be checked or measured.]
- **SC2** — ...
