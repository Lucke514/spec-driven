# Tasks: [Feature name]

> Spec: [spec.md](./spec.md) · Plan: [plan.md](./plan.md)
> Status: draft  <!-- draft | in-review | approved | abandoned -->
> Last updated: [YYYY-MM-DD]

<!--
Conventions:
- One task = one focused session.
- [P] = can run in parallel with the [P] tasks it is contiguous with; the first task without [P] ends the group.
- Every task carries acceptance criteria and a concrete verification step — a command, or where the project has no test runner and the user declined adding one, a manual check the user approved.
- Done means: Verify command passes, the plan's quality gates pass with no new
  failures against their recorded baseline (lint, format, types, tests, and every other gate the plan records), and the diff is clean per the spec-driven skill's junk-code checklist.
- Include a documentation task (docs/<slug>.md, plus README/CHANGELOG if the project keeps them).
- A change to stored data (schema, shape, or values already stored) is its own task, ordered before the tasks that depend on it; its Verify names the datastore it runs against — a disposable or restorable one, never a shared, staging, or production store — and runs the change forward, then its reversal with rows present, then forward again, or cites the user's sign-off where the plan records it as irreversible. Its Acceptance is the check that proves the data survived (counts, a checksum, or an invariant query), not that the command exited.
- A feature flag introduced by this feature is retired by a task here or by a dated follow-up recorded in the spec's Decisions — never left unowned.
- A third-party dependency this feature adds, upgrades, or retires is its own task, ordered before the tasks that import it; its Files name the manifest, the lockfile, and any vendored path, and its Acceptance is the exact version resolved and pinned in the lockfile (for a removal: no remaining importers), not that the command exited. A dependency the plan does not record — and that the user did not sign off on — is never added as a side effect of another task.
- A delivery step (deploy, promotion between rollout stages, flag change, config change) names the environment it acts on; a step acting on a shared, staging, or production environment is handed to the user to run, never executed here on a standing instruction. A new config value or secret reaches its environments before the task that ships the code reading it.
- Where the feature has a kill switch, a task exercises it: turn the feature on, turn it off, confirm the pre-feature behavior returns, and note what work done under the on path survives the flip (compensation, reconciliation, or "nothing to undo").
- A task in progress is claimed, not merely unchecked: **Owner** names who (or which branch) is executing it and since when; `—` means unclaimed. Claim before writing code, commit the claim, release it to `—` on completion or handback. A claim older than the project's normal task span is stale, not held — ask before taking it.
- On completion: check the box, release **Owner** to `—`, and add a one-line note (what landed, anything surprising, and the date of the Decisions entry for any deliberate shortcut taken) that names where the work landed — the commit(s) carrying it, or `uncommitted, local to <who>` — so the record is readable from someone else's clone. Uncommitted work is not a handoff state.
- A task the user declines to do — an ordinary `T#` as much as a gap `G#` — is closed as waived, not left open: replace `- [ ] Done` with `- [~] Waived — YYYY-MM-DD, why`.
- A follow-up this feature creates but does not ship (a flag retirement, the cleanup half of a data change, a provider move, a requirement deferred out of this change set, the proper version of a deliberate shortcut) is, where the project tracks work only in the repo, left here as `- [>] Deferred — YYYY-MM-DD, owner <who>`: it is closed for this feature's verification, never counts as unchecked, and is what a later resume sees.
-->

## T1 — [Task name]

- [ ] Done
- **Owner**: —  <!-- who or which branch is executing it, since YYYY-MM-DD; `—` when unclaimed -->
- **Component**: C1 · **Implements**: R1
- **Files**: [e.g. `src/module.py`, `tests/test_module.py`]
- **Do**: [Concrete change to make.]
- **Acceptance**: [Observable result that must hold.]
- **Verify**: `[command to run, e.g. pytest tests/test_module.py]`
- **Notes**: —

## T2 [P] — [Task name]

- [ ] Done
- **Owner**: —
- **Component**: C2 · **Implements**: R2, E1
- **Files**: ...
- **Do**: ...
- **Acceptance**: ...
- **Verify**: ...
- **Notes**: —

## T[N] — Document the feature

- [ ] Done
- **Owner**: —
- **Component**: — · **Implements**: all (documentation)
- **Files**: `docs/<slug>.md` (+ README/CHANGELOG if the project keeps them)
- **Do**: Write docs/<slug>.md from the spec-driven skill's doc template; update README and CHANGELOG if applicable; add doc comments on public interfaces.
- **Acceptance**: Docs describe actual behavior; every example runs as written.
- **Verify**: run each documented example
- **Notes**: —

---

## Gaps found in verification

[Appended by Phase 7 — same task format, prefixed G1, G2, ...]

---

## Verification reports

[Appended by Phase 7 — one dated report block per pass, newest last. Never overwrite an earlier pass.]
