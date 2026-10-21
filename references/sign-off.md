# Sign-off

The items that always need explicit sign-off (SKILL.md core rule 2). **A waiver never covers them**: they approve what the feature promises, destroys or ships, not the pace of the workflow. Load this file when filling the spec's **Sign-off** line (Phase 1), and before acting on any item below at any phase.

This table is the one list. The spec's **Sign-off** line carries one line per row this feature raises, mid-flight ones included, and nothing else.

| Item | Rule lives in | Recorded as |
|---|---|---|
| The spec's own content | SKILL.md → Phase 4 (the proposal) | `approved` on that role's answer; a relayed answer also gets a dated Decisions entry |
| A sensitive-ground `R#`/`E#` (auth, personal or regulated data, secrets, money) | [writing-specs.md](writing-specs.md) → Sensitive ground | a dated Decisions entry, plus its row on the **Sign-off** line |
| Adding or changing an `R#`/`E#`/`SC#` | [lifecycle.md](lifecycle.md) → Change requests mid-flight | the new or changed id, plus a dated Decisions entry |
| Annotating an `R#`/`E#` **superseded** | the same | `— superseded by …` on it, plus a dated Decisions entry |
| Deferring a requirement out of this change set | `writing-specs.md` → Minimum shippable & deferral | `— deferred (Decisions YYYY-MM-DD, owner <who>)` on it, that entry, and the open follow-through filing |
| Resolving spec drift | [verification.md](verification.md) → Handling gaps | the spec amendment with its dated Decisions entry, or the `G#` that fixes the code |
| Accepting a requirement as a documented limitation | `verification.md` → Convergence loop | `— accepted limitation (Decisions YYYY-MM-DD, accepted by <who>)` on it, plus that entry |
| Closing a Phase 7 gap as **waived** (the user declines the fix) | `verification.md` → Convergence loop | `- [~] Waived — YYYY-MM-DD, why` on the `G#`, a dated Decisions entry, the report's `Waived:` line |
| Implementing a Phase 7 deletion gap | `verification.md` → step 6 | the user's confirmation on the `G#`, the report's `Dead-code sweep:` line |
| Removing, disabling or weakening a pre-existing test (unless an `R#` specifies it) | `verification.md` → step 4 | the report's `Tests removed:` line, naming the test and the approval |
| Accepting a manual check as a requirement's only evidence | `verification.md` → step 2 | a dated Decisions entry, cited on the Phase 7 report |
| Adding a third-party dependency, or changing the version of one other code shares | [dependencies.md](dependencies.md) | the plan's **Dependencies** line, approved with the plan |
| Executing a data change the plan records as irreversible or data-losing | [data-and-delivery.md](data-and-delivery.md) → Stored-data checklist | a dated Decisions entry per change, naming what makes recovery possible |
| Running any data-change command, reversible ones included, against a shared, staging or production datastore | `data-and-delivery.md` → **Target** / **Who executes it** | the user's go-ahead per command and target; the result on the report's `Data & delivery:` line |
| Executing a delivery step (deploy, stage promotion, flag or config change) against a shared, staging or production environment | `data-and-delivery.md` → Delivery checklist | the user's go-ahead per step and environment; the result on the report's `Data & delivery:` line |

A **Sign-off** line naming a signer other than the person in this session is not approved by that person's answer. Read [team-and-review.md](team-and-review.md) → Sign-off authority now and follow it.
