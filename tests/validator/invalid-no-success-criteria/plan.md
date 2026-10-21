<!-- Status enum: draft | in-review | approved | implemented | superseded | abandoned -->

# Plan: Bulk archive

> Spec: [spec.md](./spec.md)
> Status: approved
> Last updated: 2026-10-01

## Approach

Add a batch endpoint and a selection toolbar.

## Components

### C1 — Batch endpoint

- **Implements**: R2, E1
- **Where**: `src/api/notes.py`
- **Depends on**: —

### C2 — Selection toolbar

- **Implements**: R1
- **Where**: `src/ui/toolbar.tsx`
- **Depends on**: C1

### C3 — Old export button — cut (Decisions 2026-10-01)

- **Implements**: R3

## Evidence per requirement

| R#/E# | Evidence | Exists today? |
|---|---|---|
| R1 | `tests/toolbar.test.tsx::archives_selected` | no — written by T2 |
| R2 | `bench/archive.py` | no — written by T1 |
| E1 | `tests/api_test.py::test_reject_keeps_notes` | no — written by T1 |

## Requirement coverage

| Requirement | Covered by |
|---|---|
| R1 | C2 |
| R2 | C1 |
| E1 | C1 |
