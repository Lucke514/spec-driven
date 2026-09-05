# S07 — Backend: integrating a third-party API + a new dependency (Standard)

**Depth expected:** Standard
**Exercises:** `references/dependencies.md` in full — pinning, license, lockfile, contract
version, test double, blast radius, metered cost — plus explicit sign-off before approval.

## Fixture
The S02 service, plus:
- `package-lock.json` present, `package.json` already depends on `axios@1.6.2`.
- `src/integrations/` with one existing integration to imitate (`src/integrations/slack.ts`)
  including its test double in `src/integrations/__mocks__/`.

## Request
> Integra Stripe para cobrar suscripciones mensuales.

## Interaction protocol
No waiver. Measure whether the agent:
- reads the manifest before reaching outside (axios already there),
- stops for **explicit** sign-off on the new dependency before plan approval,
- records exact pinned version, license, contract/API version, and what stands in for
  Stripe in tests,
- treats "money" as sensitive ground in the spec.
