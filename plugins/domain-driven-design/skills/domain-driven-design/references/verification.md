# Verification and completion

Read this before finishing substantial work, reusing earlier check results, or reporting
completion. These rules carry the same authority as [SKILL.md](../SKILL.md).

## 12. Verify and finish

Acceptance evidence must apply to the final relevant content and execution environment. Reuse an
earlier passing check when its scope covers the change and its source, configuration, dependency
inputs and relevant environment still match. Rerun affected checks after relevant changes, failures
or unresolved concerns, and honor any repository/CI/release rule requiring a fresh or broader gate.
Do not repeat passing checks solely because work reached its final step or another agent ran them.
Record the checked revision/hash, command, result and reuse boundary in the existing tracker.
Freshness-sensitive runtime evidence needs its required observation window; unchanged code cannot
renew an old production observation. Reuse never waives mandatory checks or turns partial,
interrupted, unavailable or stale evidence into a pass.

Choose verification proportional to the changed behavior and risk:

- Domain tests establish important invariants, state transitions, and boundary cases.
- Integration tests establish persistence, constraints, authorization, and relevant external adapters.
- Local fakes of external services give fast, deterministic feedback while iterating; keep at least one
  check against the real adapter or its published contract before claiming the integration works.
- Contract tests or compatibility checks establish cross-domain and cross-app payload behavior.
- A focused end-to-end check establishes the affected user or job workflow, including failure handling.
- Existing lint, type, build, workspace, or dependency checks establish changed package boundaries.
- Performance checks establish only the performance claims actually made.

For monorepo package changes, verify the package and affected consumers; do not stop at a library's
unit tests when browser, mobile, server, or worker imports may break differently. Use available
affected-project tooling. Report unavailable environments and unverified paths without claiming success.

Avoid tests that only mirror implementation or check folder names. Do not add a broad testing system
for a trivial move when existing compiler/build checks adequately establish the change.
Challenge assumptions with adversarial contract cases: compound-key separator characters, forged
authority fields, retries after later state changes, and cross-consumer behavior where applicable.

Before completing substantial work, confirm:

- Paths and names reveal domain ownership and functional responsibility.
- Business rules have one authoritative owner and exposed contracts have clear consumers.
- Services and shared modules live at the narrowest scope that serves their real consumers.
- No new circular dependencies, forbidden imports, app-to-app imports, or client/server leaks exist.
- No duplicate implementation, unused abstraction, empty scaffold, or abandoned compatibility path remains.
- Relevant consistency, failure recovery, resource usage, and authorization behavior are verified.
- The implementation meets the agreed acceptance conditions without unrelated restructuring.
- Every created module has a connected-path trace; touched paths and adjacent consumers are accounted for.
- Confirmed gaps are fixed and retraced, or explicitly recorded with their impact and blocking evidence.
- Existing tracking records are updated; separate evidence has an operational purpose, and eligible
  task evidence is archived with verified restoration while active dependencies remain intact.

Report the resulting structure, important decisions and tradeoffs, checks performed, and remaining
limitations. For architecture reviews, give actionable findings with paths, impact, and the smallest
fix; do not manufacture findings or perform a redesign unless requested. Stop when the scoped
acceptance conditions are met. Do not promise that architecture alone guarantees performance or scale.

Keep agent instruction files lean. When a repeated agent mistake earns a rule, record the failure it
prevents; when newer models or tooling make a rule redundant, confirm the failure no longer occurs,
then remove it rather than letting rules accumulate.

