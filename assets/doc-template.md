<!-- Status enum: active | deprecated -->

# [Feature name]

> Spec history: [../specs/<slug>/](../specs/<slug>/)
> Status: active
> Last updated: [YYYY-MM-DD]

## What it does

[2–4 sentences for someone who has never seen this feature: what it does, when to reach for it. No implementation details.]

## Usage

[The shortest realistic example that works. Runnable as written — verified, not imagined.]

```[lang]
[example]
```

[More only where they show genuinely different usage — error handling, an advanced option.]

## Interface

[The public surface: functions/endpoints/commands. What callers rely on — skip internals.]

### `[name(params)]`

- **Input**: [params and their constraints]
- **Returns**: [shape of the result]
- **Errors**: [what fails, how it surfaces]

## Behavior notes

[Edge cases and limits a user would otherwise learn the hard way — from the spec's edge cases.]

- [Note]

## Operating

[Carried where the plan's **Delivery** is not `— ships with the normal release`, the spec carries an operational-signal `R#`/`E#`, or the plan's **Dependencies** line records an external service the feature calls at runtime — removed otherwise.]

- **Switch**: [the flag or config value controlling the feature, where it is set per environment, and the exact way to turn it off.]
- **Signal**: [what shows the feature working or broken, and where it is read.]
- **External services**: [each third-party service called at runtime, the provider API or protocol version this integration targets and where it is set, and where the provider's status is read — omit when the feature calls none.]
- **When it fires**: [what to do first — the check to make, the switch to flip, who to reach.]
