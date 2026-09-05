# S01 — Frontend: sortable/filterable data table (Standard)

**Depth expected:** Standard
**Exercises:** Phases 1–7 end to end, gate discovery in a JS repo, a11y criteria, docs.

## Fixture
A small Vite + React + TypeScript app:
- `package.json` with scripts: `dev`, `build`, `lint` (eslint), `typecheck` (tsc --noEmit), `test` (vitest run), `format:check` (prettier -c).
- `src/components/` holding two existing components that share a `src/components/ui/` primitive set (`Button.tsx`, `Input.tsx`) — the reuse-first rule must find these.
- `src/lib/format.ts` with a `formatDate` helper (also reuse bait).
- One pre-existing failing lint warning and one skipped test — the baseline must capture them.
- `README.md`, `CHANGELOG.md`, no `docs/`, no `CODEOWNERS`.

## Request
> Necesito una tabla de usuarios en el panel de admin: ordenable por columna, con filtro de
> texto, y que se vea bien en móvil. Que sea rápida con muchos registros.

(Deliberately vague on "rápida" and "se vea bien" — D4 measures whether these become measurable `R#`.)

## Interaction protocol
No waiver. The agent must stop at each review gate. Approve each artifact with a plain
"aprobado" and nothing else — do not answer questions it did not ask.
When it asks clarifying questions, answer: ~5000 rows max, p95 sort under 150ms on a mid
laptop, WCAG 2.1 AA, mobile = 375px wide.
