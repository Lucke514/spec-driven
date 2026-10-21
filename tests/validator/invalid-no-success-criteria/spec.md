<!-- Status enum: draft | in-review | approved | implemented | superseded | abandoned -->

# Spec: Bulk archive

> Status: approved
> Owner: — the session's user
> Sign-off: — the session's user holds all of these
> Tracking: — this project tracks work in the repo only
> Last updated: 2026-10-01

## Objective

Let a user archive many notes at once, because archiving one by one is slow.

## Users & scenarios

- **Archive a batch**: As a user, when my list is cluttered, I want to archive selected notes so that the list stays short.
- **Surfaces**: UI
- **Operational criteria**: Load & volume: R2 · Degradation: E1
  - Accessibility (UI surface only): WCAG 2.2 AA — Keyboard reach: R1 · Focus behavior: R1 · Contrast: R1 · Error announcement: E1
- **Sensitive ground**: none touched

## Requirements

- **R1** — The list archives every selected note.
  - Given three selected notes, when the user presses Archive, then all three leave the list.
- **R2** — Archiving 500 notes completes in under 2 seconds.
  - Given 500 selected notes, when the user presses Archive, then the list updates within 2 s.
- **R3** — The list exports archived notes as CSV — deferred (Decisions 2026-10-01, owner lucas)

**Minimum shippable**: R1, E1

## Non-goals

- Restoring archived notes.

## Edge cases & error behavior

- **E1** — When the server rejects the batch, the list keeps every note and shows the error.

## Decisions

- 2026-10-01 CSV export deferred — because no user asked for it yet.

## Open questions

## Success criteria

