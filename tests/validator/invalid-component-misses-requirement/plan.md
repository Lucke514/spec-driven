<!-- Status enum: draft | in-review | approved | implemented | superseded | abandoned -->

# Plan: Bulk archive

> Spec: [spec.md](./spec.md)
> Status: approved
> Last updated: 2026-10-01

## Approach

Add a batch endpoint and a selection toolbar.

## Components

### C1 — Batch endpoint

- **Implements**: R2
- **Where**: `src/api/notes.py`
- **Depends on**: —

### C2 — Selection toolbar

- **Implements**: R1
- **Where**: `src/ui/toolbar.tsx`
- **Depends on**: C1

### C3 — Old export button — cut (Decisions 2026-10-01)

- **Implements**: R3
