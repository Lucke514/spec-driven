# spec-driven — evaluation harness

Real-usage tests for the `spec-driven` skill. Each run puts a fresh agent in a sandbox
project, hands it `SKILL.md` as its active instructions plus a realistic feature request,
and measures what the agent actually *does* — not what the skill says it should do.

## Layout

```
tests/
├── README.md          # this file
├── RUBRIC.md          # how a run is scored
├── scenarios/         # one file per test scenario (the user request + setup)
├── runs/              # sandbox projects, one dir per run: runs/<iter>-<scenario>/
└── results/           # one scorecard per run + iterations.md (the improvement log)
```

## Running one

1. Pick a scenario from `scenarios/`.
2. Create `tests/runs/<NN>-<scenario-slug>/` and lay down the scenario's **Fixture**.
3. Give a *fresh* agent: the full text of `SKILL.md` (and let it read `references/`,
   `assets/` on demand), the scenario's **Request**, and the sandbox as its cwd.
4. Score the run against `RUBRIC.md` into `tests/results/<NN>-<scenario-slug>.md`.

The agent must never see `RUBRIC.md` — it measures unprompted behavior.

## What a run is for

Scores are secondary. The primary output is the **friction log**: every place the agent
re-read the skill, guessed, stalled, contradicted itself, or silently skipped a rule.
Those are the defects to fix in the skill.
