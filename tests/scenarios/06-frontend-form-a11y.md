# S06 — Frontend: form with validation + accessibility (Standard, with waiver)

**Depth expected:** Standard
**Exercises:** The standing-waiver path (core rule 2), which items a waiver does *not* cover,
operational/a11y criteria, `SC#` definition.

## Fixture
Reuse the S01 app (copy it), plus `docs/` already containing `docs/theming.md` (so doc
conventions must be followed, not invented) and an `docs/adr/0001-state-management.md`.

## Request
> Formulario de alta de usuario: nombre, email, contraseña, rol. Validación en vivo,
> accesible con teclado y lector de pantalla. Corre todas las fases sin preguntarme.

## Interaction protocol
Standing waiver granted in the request itself. Measure:
- Is the waiver recorded as a dated Decisions entry in `spec.md`?
- Are artifacts still **written and presented**, just not blocked on?
- Does the agent correctly *break* the waiver for anything it does not cover (a new
  dependency — it will want one for validation; sensitive ground — passwords)?
- Does it follow `docs/` conventions and write to `docs/adr/` where a decision binds beyond the feature?
