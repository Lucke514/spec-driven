<!-- Status enum: draft | in-review | approved | implemented | superseded | abandoned -->

# Spec: [Feature name]

> Status: draft
> Owner: [who is accountable for this spec's content]
> Sign-off: [one row per item this feature raises from core rule 2's table (SKILL.md → Core rules) — that table is the list — each naming the role that approves it, read from the repo. **Every non-empty Sensitive ground item below carries a row here.** `— the session's user holds all of these` is valid and common; an absent signer is `pending sign-off: <role>` on the Status line, which no waiver covers.]
> Tracking: [the team's work item for this feature — id or link — discovered by reading the repo; or `— this project tracks work in the repo only`.]
> Last updated: [YYYY-MM-DD]

## Objective

[1–3 sentences: what this feature does and why it is worth building. If you cannot state the "why", ask.]

## Users & scenarios

[Who uses this and in what situation. Coverage lines: `references/writing-specs.md` → Surfaces / Operational criteria / Sensitive ground. List only what applies.]

- **[Scenario name]**: As a [user], when [situation], I want [capability] so that [outcome].
- **Surfaces**: [UI | API or contract | CLI | background job | data pipeline | library — each one exposed, with its criteria in Requirements or a Non-goal.]
- **Operational criteria**: [only the items that apply, each with its `R#`/`E#`/`SC#` — e.g. `Load & volume: R4 · Degradation: E2` — or `n/a — <reason>`. Not required at Small.]
  - Accessibility (UI surface only): [the standard and level this project commits to, or `non-goal`] — Keyboard reach: [R#] · Focus behavior: [R#] · Contrast: [R#] · Error announcement: [E#]
- **Sensitive ground**: [`none touched` — or, when it touches auth, personal or regulated data, secrets or money, all five items, each `R#`/`E#` or `non-goal`, each filled item with its **Sign-off** row above:]
  - Access control: [R#] · Traceability: [R#] · Data handling: [E#] · Data lifecycle: [non-goal] · Repeat-request correctness: [R#]

## Requirements

[Each requirement is testable: a reviewer answers "done or not done?" with yes/no. Ids are stable — never renumbered, never reused. A requirement is never deleted and never moved to Non-goals; it is annotated in place: `— superseded by specs/<slug>/spec.md` · `— accepted limitation (Decisions YYYY-MM-DD)` · `— deferred (Decisions YYYY-MM-DD, owner <who>)`.]

- **R1** — [subject] [verb] [observable object].
  - Given [precondition], when [action], then [observable result].
- **R2** — ...

**Minimum shippable**: [R1, R2, E1 — the smallest set that still delivers the Objective.]

## Non-goals

[What this feature deliberately does NOT do.]

- [Non-goal 1]

## Edge cases & error behavior

[Bad input, empty states, concurrency, limits. Each entry is testable and carries a stable id, referenced like a requirement.]

- **E1** — When [edge condition], the system [expected behavior].
- **E2** — ...

## Decisions

[Append-only. A follow-up this feature defers — a flag retirement, a data change's cleanup half, a provider move, a rollout's last stage, a deferred requirement, a shortcut's proper version — names its owner and date and carries the identifier it got from **Tracking**; where work is tracked in the repo only, it is also a `- [>] Deferred` entry in `tasks.md`.]

- [YYYY-MM-DD] [Decision] — because [rationale].

## Open questions

[Must be empty before the spec is approved.]

- [NEEDS CLARIFICATION: question]

## Success criteria

[How we know the feature works in the real world, beyond tests passing. Ids are stable — verification walks and reports them by id. An empty section at Standard or above is a `[NEEDS CLARIFICATION]`, not a valid state; Small carries none.]

- **SC1** — [criterion, checkable or measurable] · **Signal**: [metric | log | dashboard | report] · **Read at**: [where a human reads it, plus the environment when it is only observable after rollout] · **Emitted by**: [the `C#`/`T#` that emits the signal, or `already exists`]
- **SC2** — ...
