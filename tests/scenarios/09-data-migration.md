# S09 — Backend: schema migration + backfill (Standard)

**Depth expected:** Standard
**Exercises:** `references/data-and-delivery.md` — migration, backfill, reversibility,
irreversible-change sign-off, the check that proves data survived, rollout/kill switch.

## Fixture
The S02 service. `migrations/` uses plain numbered SQL, applied by `npm run migrate`.
A `tasks` table already has `status TEXT`. Seed data exists in `seeds/dev.sql`.

## Request
> Hay que separar `status` en `status` + `archived_at`, y migrar los registros que hoy
> tienen status='archived'. En producción hay ~2M filas.

## Interaction protocol
No waiver. Measure whether the agent:
- records **Data changes** with the target datastore and the check that proves survival,
- classifies the change as reversible or not, and demands sign-off if irreversible,
- plans the backfill for 2M rows (batching, resumability) rather than one UPDATE,
- plans the read/write cutover ordering (expand → migrate → contract),
- records **Delivery** (flag/rollout/kill switch) instead of `— ships with the normal release`.
