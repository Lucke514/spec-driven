# S10 — Change request from a code reviewer, mid-implementation

**Depth expected:** Standard, interrupted
**Exercises:** "Change requests mid-flight" — reviewer feedback must land in `spec.md` first,
what counts as behavior feedback vs. ordinary Phase 5 work, invalidated tasks, re-approval.

## Fixture
The S01 app with an in-flight feature:
- `specs/bulk-actions/` complete (spec/plan/tasks), Status `approved`, T1–T3 done, T4–T6 open.

## Request (two turns)
1. > Sigue con lo de bulk actions.
2. (after it starts T4) > El reviewer dice dos cosas: que el botón debería llamarse
   "Aplicar" en vez de "Ejecutar", y que las acciones masivas tienen que pedir confirmación
   cuando afectan más de 20 filas. Es el PR #418, lo revisó [a teammate].

## Interaction protocol
No waiver. Measure the *split*: the rename is ordinary Phase 5 work; the confirmation
threshold is a new `R#` that must enter through `spec.md` with a Decisions entry naming the
reviewer and PR #418 — and it must check whether T1–T3 are invalidated before continuing.
