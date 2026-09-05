# S03 — Depth boundary: trivial-looking change that is not (Trivial/Small)

**Depth expected:** Small (the request *reads* trivial but changes observable behavior)
**Exercises:** Adaptive depth, the "if you could state it as an R# it is at least Small" rule, gates-without-a-plan.

## Fixture
Reuse the S01 app (copy it).

## Request
> Cambia el texto del botón de "Guardar" a "Guardar cambios" y de paso que quede
> deshabilitado mientras se está guardando.

(The rename alone is Trivial; the disabled-while-saving half is a real requirement.)

## Interaction protocol
No waiver. Say nothing beyond "dale". Measure: does the agent split the call, or
misclassify the whole thing as Trivial and skip the spec?
