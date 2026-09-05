# S04 — Phase 0: a request that must be split (Large)

**Depth expected:** Large → Phase 0 scope.md, then Phase 1–7 on capability #1 only.
**Exercises:** Phase 0, scope.md shape (slug/responsibility/depends-on/rank/status), stopping after the split.

## Fixture
Reuse the S02 service (copy it).

## Request
> Quiero un sistema de notificaciones: que se manden emails cuando pasan cosas, que el
> usuario configure qué recibe, un historial en la app, y digest semanal.

## Interaction protocol
No waiver. Approve the split with "aprobado, empieza por la primera". Then let it run
capability #1 to completion.
Measure: does it produce `specs/<parent>/scope.md` with **rank** and correct depends-on,
and sibling `specs/<capability>/` dirs — or does it write one giant spec?
