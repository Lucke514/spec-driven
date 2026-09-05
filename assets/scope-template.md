<!-- Row Status enum: pending | in-progress | done | deferred | abandoned -->

# Scope: [Parent feature name]

> Last updated: [YYYY-MM-DD]

[1–3 sentences: the request this split covers, and the date the user approved the split.]

| Slug | Responsibility | Depends-on | Rank | Status |
|---|---|---|---|---|
| notification-events | Deliver a notification by email when a tracked action happens | — | 1 | done |
| notification-preferences | Let a user choose, per notification type, whether they receive it by email | notification-events | 2 | in-progress |
| notification-digest | Roll up a user's notifications from the past 7 days into one weekly email | notification-events, notification-preferences | 3 | deferred — 2026-08-26, owner @maya |

[One row per capability, each shippable and valuable on its own. **Rank** is the order the user approved, by value delivered — the tiebreak when several capabilities are unblocked at once. A `deferred` row carries its date and owner and stays visible for a later session; `abandoned` is a capability that is not coming back. Each capability gets its own sibling `specs/<capability-slug>/`, runs Phases 1–7, and updates its Status here as it lands. Adding, removing, or moving behavior between capabilities is a change to this table, approved first (SKILL.md → Phase 0).]
