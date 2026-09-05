# Clean code

Standards for Phase 5 (Implement) and the final sweep in Phase 7 (Verify). These are pass/fail, not style preferences: a task whose diff violates them is **not done**, even if its tests pass. Sweep every diff before marking a task done and record the result on the task's completion note, in the shape the tasks template pins: `Clean-code: <n> hits — <what> | none · close calls: <each one, and which way it went> | none`. Both halves are always written — a `none` recorded, never a field left blank, so "none" and "none recorded" never look the same.

## Gates — mechanical

Answerable by grep, the AST, or the compiler, over the diff alone. A hit is a hit.

- [ ] No commented-out code. Version control is the archive; delete it.
- [ ] No debug output (`console.log`, `print`, `dbg!`, dumps) outside real logging.
- [ ] No dead code: unused functions, variables, imports, parameters, exports, dependencies added "just in case".
- [ ] No orphan artifacts: scratch files, `.bak`/`.old` copies, empty modules, fixtures nothing reads.
- [ ] No `TODO`/`FIXME`/`HACK` without a task ID (`T#`/`G#`), an issue reference, or the dated Decisions entry that declares a deliberate shortcut — `TODO(Decisions 2026-05-06)`, written as Declared shortcuts below requires. An anonymous TODO is a decision nobody made; a declared one carries a date, a trade, and an owner.
- [ ] No stubbed error handling: empty `catch` blocks, swallowed errors, `except: pass`. Handle it, propagate it, or let it crash loudly — silently continuing is the one wrong option.
- [ ] No hardcoded secrets, URLs, paths, or environment assumptions that belong in configuration.
- [ ] No hardcoded user-facing text, and no locale-dependent formatting of money, dates, numbers, or sorting, where the project already has a mechanism for them — find it before writing the string (the plan's **Reuses** line names it). Where the project has none, a literal is correct and inventing a framework is not.

## Judgment calls — same weight, no automated check

Each states its threshold. Where a call is close, name it and say which way you went on the note's `close calls:` sub-field — three close calls all resolved *no* must not produce the same note as a diff that raised none.

- [ ] No copy-paste duplication. **Threshold**: the repeated block encodes a decision (a branch, a formula, a validation rule, an ownership check) — or, encoding none, spans more than ~5 lines — and that is the second occurrence to extract. Read the decision test first: it is the broader clause, and a short block that repeats a decision is duplication at two lines. Two similar-looking lines are not duplication; a duplicated algorithm is.
- [ ] No magic values: unexplained numbers or strings get a named constant when the name adds meaning (`MAX_RETRIES = 3`, not `THREE = 3`).
- [ ] No reinvented wheels: the diff must not reimplement behavior the codebase already provides — check the plan's **Reuses** and **Duplicates** lines and the shared/core/util areas before writing a helper; if the existing one almost fits, extend it (within its responsibility) instead of forking a copy.
- [ ] No speculative generality: abstractions, options, layers, or generics with exactly one current use and a hypothetical future one. Build for today's spec; the future has its own spec. **Extracting logic so an acceptance criterion becomes testable is a current use** — but that licenses the *extraction* and nothing around it: the interface, the options, the type parameters, the injection point, the registry it is registered in each still need a second current caller of their own. A `Verify:` step is that caller for the extracted unit only. Phase 5 mandates a test for everything, so a rule that read the test as a second use for whatever surrounds it would make this gate unfileable.
- [ ] Functions do one thing at one level of abstraction. **Threshold**: a name that needs "and" to stay accurate, or a body mixing two levels (policy and I/O, parsing and dispatch), splits.
- [ ] Guard clauses over nesting: return early; don't pyramid.
- [ ] Nothing misleading: names, comments, and doc comments must match what the code actually does *after* your change, not before.

## Declared shortcuts

Where a task ships code that meets its `R#` but knowingly does not do what the plan's component describes — a narrower correctness, a duplication left in place, a step skipped for time — the spec is not wrong and the gates will not catch it, so the record is the only thing that will: add a dated Decisions entry naming what was traded, the proper version, and who owns it; cite it in the task's completion note; let Phase 7 report it on its `Shortcuts declared:` line. An owner and a date make it an open follow-through — read [team-and-review.md](team-and-review.md) → Open follow-through and file it where the spec's **Tracking** line points.

## Boundaries

- **Boy-scout rule, bounded**: leave the lines you touch cleaner, but don't refactor beyond the task's scope. Wider cleanups become new tasks proposed to the user, never smuggled into an unrelated diff. Improving a project-wide convention is a spec/plan discussion, not a drive-by.
- **Diff-clean is not feature-clean**: these per-task checks can't see code orphaned *across* tasks — something used when written whose last caller a later task removed. Phase 7 runs a reachability sweep over the whole change set and deletes what nothing reaches; don't assume passing every per-task gate means no dead code shipped.
- **Tests are code**: every rule above applies to test files. Duplicated setup becomes a helper; a test nobody can read verifies nothing.
- **When a gate conflicts with the spec** (e.g. cleanliness suggests an API change the spec forbids), the spec wins — raise it as spec feedback instead of quietly deviating.
