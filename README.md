# spec-driven

An [Agent Skill](https://agentskills.io) for **spec-driven development (SDD)**: the agent writes and gets approval on a spec, a plan, and a task breakdown — as files in your repo — before writing any code, then verifies the finished code against the spec.

## Workflow

```
specify → clarify → plan → tasks → implement → document → verify
```

The planning phases produce artifacts under `specs/<feature-slug>/` in your project:

| Artifact | Contents |
|---|---|
| `spec.md` | What & why — testable requirements (R#), edge cases (E#), non-goals, decisions, success criteria (SC#) |
| `plan.md` | How — components (C#) mapped to requirements, build order, risks |
| `tasks.md` | Single-session tasks (T#) with acceptance criteria and a verify command |

The agent stops for your review after each planning artifact (spec, plan, tasks) and before implementing any gaps verification finds, and requirements, edge cases, components, and tasks are cross-referenced by ID so the final verification pass is mechanical: every requirement and edge case gets a verdict (met / partially met / not met / spec drift / superseded / deferred).

Two things ship with every feature, enforced as pass/fail gates:

- **Clean code** — no dead code, debug leftovers, commented-out blocks, duplication, or magic values survive a task; the project's lint/format/type/test commands are recorded in the plan and must show no new failures against their recorded baseline before any task is marked done.
- **Documentation in the repo** — a `docs/<feature>.md` page plus README/CHANGELOG updates, verified against actual behavior like any other requirement.

Depth adapts to the work — trivial changes skip SDD entirely; small features collapse to a single file; large requests are split into one spec per capability.

## Install

From [skills.sh](https://skills.sh):

```bash
npx skills add Lucke514/spec-driven
```

Or manually — clone into your agent's skills directory:

```bash
git clone https://github.com/Lucke514/spec-driven ~/.claude/skills/spec-driven
```

## Usage

Just ask for a feature and mention the workflow ("let's do this spec-first"), or invoke it directly:

```
/spec-driven add user authentication with email + password
```

## Layout

```
SKILL.md                     # the workflow and its rules
assets/                      # templates: spec, plan, tasks, feature docs
references/                  # deep guidance: writing specs, clean code, verification
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
