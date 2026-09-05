# Scoring rubric

Each dimension scores 0–5. A run's total is out of 60.
Score what the agent **did**, from its transcript and the files on disk — never what it claimed.

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
| D12 | **Cost** | Thrashed: re-read the skill repeatedly, long stalls, huge preamble | Read what it needed once; time-to-first-artifact short |

## Friction log (the real output)

For every dimension scoring ≤3, record:

- **Where** — the exact SKILL.md rule or reference section involved.
- **What went wrong** — misread, unread, contradictory, or unactionable.
- **Why** — the property of the text that caused it (buried in a long sentence, no example,
  conflicts with another rule, requires info the agent cannot get, etc.).
- **Fix shape** — the smallest change to the skill that would prevent it.
