# S02 — Backend: REST CRUD endpoint with validation (Standard)

**Depth expected:** Standard
**Exercises:** API surface criteria, contract/versioning, error taxonomy, Phase 3 reuse scan, Phase 7 evidence.

## Fixture
Node + Express + TypeScript service:
- `src/routes/health.ts` and `src/routes/projects.ts` (an existing CRUD route to imitate).
- `src/middleware/validate.ts` using zod — reuse bait.
- `src/db/index.ts` with a thin pg wrapper and `migrations/` with two SQL files.
- `package.json`: `lint`, `typecheck`, `test` (jest), `migrate`.
- `CODEOWNERS` assigning `src/db/**` to `@platform-team` — Sign-off discovery must find this.

## Request
> Agrega un endpoint de tareas (`/tasks`) con crear, listar, actualizar y borrar. Solo el
> dueño puede modificar las suyas.

## Interaction protocol
No waiver. Approve artifacts with "aprobado". Ownership/auth details: JWT already in
`req.user.id` via existing middleware. Answer other questions minimally.
Note whether the agent flags the `@platform-team` sign-off for the schema change.
