# S08 — Verification against pre-existing, drifted code

**Depth expected:** n/a — Phase 7 only ("verify existing code against its spec")
**Exercises:** Phase 7 verdicts, spec drift, deletion gaps, superseded, the report block format.

## Fixture
The S01 app with a **completed** feature whose code drifted:
- `specs/user-search/spec.md` — Status `approved`, R1–R6, E1–E3, SC1–SC2.
- `specs/user-search/plan.md` with C1–C4 and recorded gates.
- `specs/user-search/tasks.md` — all tasks checked, **no verification report block**.
- The code: R3 implemented differently than specified (drift), R5 not implemented at all,
  E2 unhandled, plus `src/lib/searchCache.ts` that nothing imports (deletion gap), and a
  debug `console.log` left in `src/features/search/useSearch.ts`.

## Request
> Verifica que la búsqueda de usuarios cumpla con su spec.

## Interaction protocol
No waiver. Measure verdict accuracy per id (expected: R3 spec drift, R5 not met,
E2 not met, rest met), the deletion gap on `searchCache.ts`, the junk-code catch, whether
gaps are appended as `G#` tasks with approval requested, and whether the report block
matches `references/verification.md`'s format.
