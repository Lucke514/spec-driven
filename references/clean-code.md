# Clean code & quality gates

Detailed standards for Phase 5 (Implement) and the final sweep in Phase 7 (Verify). These are pass/fail gates, not style preferences: a task whose diff violates them is **not done**, even if its tests pass.

## The junk-code checklist

Sweep every diff for these before marking a task done. Each item is checkable by reading the diff alone.

**Leftovers**
- [ ] No commented-out code. Version control is the archive; delete it.
- [ ] No debug output (`console.log`, `print`, `dbg!`, dumps) outside real logging.
- [ ] No dead code: unused functions, variables, imports, parameters, exports, dependencies added "just in case".
- [ ] No orphan artifacts: scratch files, `.bak`/`.old` copies, empty modules, fixtures nothing reads.

**Placeholders**
- [ ] No `TODO`/`FIXME`/`HACK` without a task ID (`T#`/`G#`), an issue reference, or the dated Decisions entry that declares a deliberate shortcut — `TODO(Decisions 2026-05-06)`, written where SKILL.md → Phase 5 requires that entry. An anonymous TODO is a decision nobody made; a declared one carries a date, a trade, and an owner.
- [ ] No stubbed error handling: empty `catch` blocks, swallowed errors, `except: pass`. Handle it, propagate it, or let it crash loudly — silently continuing is the one wrong option.
- [ ] No hardcoded secrets, URLs, paths, or environment assumptions that belong in configuration.
- [ ] No hardcoded user-facing text, and no locale-dependent formatting of money, dates, numbers, or sorting, where the project already has a mechanism for them — find it before writing the string (the plan's **Reuses** line names it). Where the project has none, a literal is correct and inventing a framework is not.

**Structure**
- [ ] No copy-paste duplication. Second occurrence of a non-trivial block → extract it. (Two similar-looking lines are fine; a duplicated algorithm is not.)
- [ ] No magic values: unexplained numbers or strings get a named constant when the name adds meaning (`MAX_RETRIES = 3`, not `THREE = 3`).
- [ ] No reinvented wheels: the diff must not reimplement behavior the codebase already provides — check the plan's **Reuses** lines and the shared/core/util areas before writing a helper; if the existing one almost fits, extend it (within its responsibility) instead of forking a copy.
- [ ] No speculative generality: abstractions, options, layers, or generics with exactly one current use and a hypothetical future one. Build for today's spec; the future has its own spec.
- [ ] Functions do one thing at one level of abstraction. If honestly naming it needs "and", split it.
- [ ] Guard clauses over nesting: return early; don't pyramid.

**Names & comments**
- [ ] Names say what things are: full words, no cryptic abbreviations, no `data2`/`newHelper`/`tmp` surviving past the draft.
- [ ] Comments explain *why*, never *what* the code already says. A comment paraphrasing the next line is noise; a comment explaining a non-obvious constraint is gold.
- [ ] Nothing misleading: names, comments, and doc comments must match what the code actually does *after* your change, not before.

**Consistency**
- [ ] The change reads like the surrounding codebase — same naming style, error-handling pattern, file layout, test conventions. Improving a project-wide convention is a spec/plan discussion, not a drive-by.
- [ ] Comment density matches the file's; don't carpet-bomb a sparse file with narration.

## Quality gates (mechanical)

Discovered in Phase 3 and recorded in `plan.md` → Quality gates, together with their **baseline**: run each gate once on the untouched tree before Phase 5 starts and record its pre-existing failures — plus the test gate's skipped count — there. A gate that does not reproduce its own result is nondeterministic; a failure absent from the baseline counts as new only after attribution ([verification.md](verification.md) step 4). Run all gates before marking any task done. A gate **passes** when it introduces no *new* failures relative to that baseline — pre-existing failures stay in the baseline, are reported in Phase 7, and never block a task.

1. **Tests** — the task's `Verify:` command plus the recorded test-gate command (narrow it to the touched areas only when the full suite is too slow to run per task); zero new failures against the recorded baseline.
2. **Linter** — zero new warnings; where the tooling supports it, scope the recorded command to the files you touched rather than diffing a repo-wide backlog. Never silence a rule inline to get past it; if a rule is genuinely wrong for this case, that's a Decision to record, with the user's approval.
3. **Formatter** — run it on the files you touched; commit no formatting noise in unrelated lines, and don't reformat untouched files to satisfy a repo-wide check.
4. **Type checker** — zero new errors; no `any`/casts/`# type: ignore` escapes added to dodge one.
5. **Every other recorded gate** — the accessibility, security/dependency, size or performance-budget, or contract check the plan records because the project already runs it: run it the same way, zero new failures against its recorded baseline.

Gates with no tooling were settled in Phase 3: either a minimal-setup task exists, or the user's recorded refusal routes those tasks to approved manual checks ([verification.md](verification.md) step 2).

## Boundaries

- **Boy-scout rule, bounded**: leave the lines you touch cleaner, but don't refactor beyond the task's scope. Wider cleanups become new tasks proposed to the user, never smuggled into an unrelated diff.
- **Diff-clean is not feature-clean**: these per-task checks can't see code orphaned *across* tasks — something used when written whose last caller a later task removed. Phase 7 runs a reachability sweep over the whole change set and deletes what nothing reaches; don't assume passing every per-task gate means no dead code shipped.
- **Tests are code**: every rule above applies to test files. Duplicated setup becomes a helper; a test nobody can read verifies nothing.
- **When a gate conflicts with the spec** (e.g. cleanliness suggests an API change the spec forbids), the spec wins — raise it as spec feedback instead of quietly deviating.
