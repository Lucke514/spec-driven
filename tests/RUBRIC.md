# Scoring rubric

Score what the agent **did**, from its transcript and the files on disk — never what it claimed.
Check the cost budget first. Then score the 12 dimensions, 0–5 each, out of 60.

## Cost budget (pass/fail, checked first)

A run over any limit for its depth **fails, whatever its score**. Record the three numbers and
the verdict at the top of the scorecard. `python3 tests/budget.py` must pass before any run.

| Depth | Instruction words loaded before the first presented artifact | Tool calls to the first presented artifact | Review round-trips before code |
|---|---|---|---|
| Trivial | 4,200 (whole run; no artifact) | 15 (to the first edit) | 0 |
| Small | 7,500 | 25 | 1 |
| Standard | 10,700 | 40 | 1 |
| Large | Standard's, per capability | Standard's, per capability | Phase 0 + 1 per capability |

- **Words loaded** — sum the files and sections the agent actually read, counted like `wc -w`.
  Re-reading a file counts again. `tests/budget.py` prints the floor for the default path.
- **Tool calls** — every tool call from the request to the first artifact presented to the user.
- **Round-trips** — turns where the agent stops for approval before code. Phase 2's one batch
  of questions is not a review; a stop a sign-off item forces (`references/sign-off.md`) is not
  counted either.

## Dimensions

| # | Dimension | 0 | 5 |
|---|---|---|---|
| D1 | **Depth call** | Wrong class, or none stated | Correct class, stated in one line before starting |
| D2 | **Phase discipline** | Jumped to code, or skipped phases the depth requires | Every required phase ran, in order, with its artifact on disk |
| D3 | **Artifact fidelity** | Ignored templates / missing header block | Templates followed; Status, Owner, Sign-off, Tracking, Last updated all filled from evidence |
| D4 | **Testable requirements** | Vague prose ("fast", "nice UX") | Every `R#` answerable yes/no; `E#` cover real edges; Minimum shippable present |
| D5 | **Traceability** | IDs missing or unlinked | `R#`/`E#` → `C#` → `T#` chain complete and consistent in both directions |
| D6 | **Gate discovery** | Invented commands, or none | Real commands read from the repo, baselined on the untouched tree, `Base` + `Integration` recorded |
| D7 | **Code quality** | Dead code, debug leftovers, magic values, duplication | Clean diff; conventions match the fixture; gates actually executed |
| D8 | **Review stops** | Chained phases without stopping (absent a waiver) | Stopped where required; waiver, if any, recorded as a Decisions entry |
| D9 | **Documentation** | None, or invented behavior | `docs/<slug>.md` accurate against the code; entry points updated |
| D10 | **Verification** | No Phase 7, or verdicts asserted without evidence | Every `R#`/`E#` gets a verdict citing real code + a passing test; report block appended |
| D11 | **Scope fidelity** | Built beyond the spec, or silently less | Diff covered by the spec; shortcuts and cuts declared as Decisions entries |
| D12 | **Ceremony to value** | Artifact lines and process commits dwarf the shipped diff (a 120-line spec and 9 commits for 3 lines) | Artifact lines and process-only commits per line of shipped diff in proportion to the depth; nothing written that no later phase reads |

## Friction log (the real output)

For every dimension scoring ≤3, record:

- **Where** — the exact SKILL.md rule or reference section involved.
- **What went wrong** — misread, unread, contradictory, or unactionable.
- **Why** — the property of the text that caused it (buried in a long sentence, no example,
  conflicts with another rule, requires info the agent cannot get, etc.).
- **Fix shape** — the smallest change to the skill that would prevent it.
