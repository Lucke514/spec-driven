# Spec: Rename save button

> Status: in-review
> Owner: — the session's user
> Sign-off: — the session's user holds all of these
> Tracking: — this project tracks work in the repo only
> Last updated: 2026-10-01

## Objective

Rename "Submit" to "Save" so the label matches what the button does.

## Users & scenarios

- **Surfaces**: UI
- **Sensitive ground**: none touched

## Requirements

- **R1** — The form's primary button reads "Save".

**Minimum shippable**: R1

## Non-goals

- Restyling the button.

## Edge cases & error behavior

- **E1** — When the form is disabled, the button still reads "Save".

## Decisions

- 2026-10-01 Label text "Save" — because the product copy guide uses it.

## Tasks

| Gate | Command | Where | Baseline |
|---|---|---|---|
| Tests | `npm test` | `here` | `0 failed, 12 passed` |

**Base**: `main` @ `abc1234`

## T1 — Relabel the button

- [ ] Done
- **Owner**: —
- **Implements**: R1, E1
- **Verify**: `npm test form`
- **Notes**: —

### T2 — Document the feature

- [ ] Done
- **Owner**: —
- **Implements**: all (documentation)
- **Notes**: —
