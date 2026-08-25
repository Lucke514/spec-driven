# [Feature name]

> Spec history: [../specs/<slug>/](../specs/<slug>/)
> Status: active  <!-- active | deprecated -->
> Last updated: [YYYY-MM-DD]

## What it does

[2–4 sentences for someone who has never seen this feature: what it does and when to reach for it. No implementation details.]

## Usage

[The shortest realistic example that works. Runnable as written — verified, not imagined.]

```[lang]
[example]
```

[One or two more examples only if they show genuinely different usage, e.g. error handling or an advanced option.]

## Interface

[The public surface: functions/endpoints/commands with signatures, inputs, outputs, and error behavior. Document what callers rely on — skip internals.]

### `[name(params)]`

- **Input**: [params and their constraints]
- **Returns**: [shape of the result]
- **Errors**: [what fails, how it surfaces]

## Behavior notes

[Edge cases and limits a user would otherwise learn the hard way — drawn from the spec's edge-case section.]

- [Note]

## Operating

[Only for a feature that ships behind a switch, carries an operational signal, or calls an external service at runtime — remove this section otherwise. Written for someone who reaches this page under pressure.]

- **Switch**: [the flag or config value that controls the feature, where it is set per environment, and the exact way to turn the feature off.]
- **Signal**: [what shows the feature working or broken, and where it is read.]
- **External services**: [each third-party service this feature calls at runtime, the provider API or protocol version this integration targets and where that version is set, and where the provider's status or incidents are read — omit this line when the feature calls none.]
- **When it fires**: [what to do first — the check to make, the switch to flip, who to reach.]

## Related

- [Links to adjacent docs, ADRs, or external references — or remove this section.]
