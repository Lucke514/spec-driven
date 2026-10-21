# spec-driven — evaluation harness

Real-usage tests for the `spec-driven` skill. Each run puts a fresh agent in a sandbox
project, hands it `SKILL.md` as its active instructions plus a realistic feature request,
and measures what the agent actually *does* — not what the skill says it should do.

## Layout

```
tests/
├── README.md          # this file
├── RUBRIC.md          # how a run is scored (cost budget first)
├── budget.py          # instruction words per depth path; must pass
├── scenarios/         # one file per test scenario (the user request + setup)
├── runs/              # sandbox projects, one dir per run: runs/<iter>-<scenario>/
└── results/           # one scorecard per run + iterations.md (the improvement log)
```

## Running one

1. Run `python3 tests/budget.py`. If it fails, fix the skill before running anything.
2. Pick a scenario from `scenarios/`.
3. Create `tests/runs/<NN>-<scenario-slug>/` and lay down the scenario's **Fixture**.
4. Give a *fresh* agent: the full text of `SKILL.md` (and let it read `references/`,
   `assets/` on demand), the scenario's **Request**, and the sandbox as its cwd.
5. Score the run against `RUBRIC.md` into `tests/results/<NN>-<scenario-slug>.md`.

The agent must never see `RUBRIC.md` — it measures unprompted behavior.

## What a run is for

Scores are secondary. The primary output is the **friction log**: every place the agent
re-read the skill, guessed, stalled, contradicted itself, or silently skipped a rule.
Those are the defects to fix in the skill.

## Fixing a finding

Every fix has a price, paid on the depth path it touches:

- A fix for a new finding must be paid for by deleting text at least as costly on the same
  depth path. A rule nobody can afford to load is not a fix.
- Edge cases (multi-team, rebases, concurrent sessions) go in on-demand references, never the core.
- `python3 tests/budget.py` must pass after the fix. Raise a budget only with a deletion that
  pays for it.
