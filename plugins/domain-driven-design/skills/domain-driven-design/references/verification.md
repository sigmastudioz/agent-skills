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

## Claims and their authoritative targets

Before reporting a state, name where that state is held and read it there. A proxy can be a useful
hint; it is not evidence of the claim.

| Claim | Proxy that has misled | Authoritative readback |
| --- | --- | --- |
| Deployed or live | Commit in the release branch, higher release number, pipeline exit 0 | The code or revision the running process serves on each host |
| Saved, written, published | Exit status, acknowledgement, model or tool narration | The stored file hash or mtime, the provider's record, the saved remote state |
| Installed or ready | Folder exists, process started | The files actually loaded, a smoke call against the installed artifact |
| Absent, zero, never happened | A probe returning empty | The same probe finding a known-present item, with names resolved from the schema |
| Check passed | Exit 0 of a pipeline, a chained shell, a tool that prints failures | The check's own status and parsed output |
| Status in a tracker | The last ledger mention | Current runtime, deploy and Git state |

After packaging or deploying, smoke-test the installed or deployed artifact through its real entry
and keep a named rollback copy; unit and build gates do not establish that it starts. Validate the
operations a shipped client actually sends against the deployed schema, not workspace source.

### Checks that can fail

A check counts as evidence only after it has been seen to fail on the defect it claims to catch.
Show each new regression test failing before the fix. For a new gate, feed it one known-bad input
or mutation. A gate that cannot resolve its input (a missing base revision, an empty file set, an
excluded path) must fail, not skip. Identify what aliases, mocks and exclusions remove (styles,
GPU, native modules, type-checking of test files) and keep one check on the real path for that
class. Do not downgrade a blocking gate to a warning without an owner and a removal condition, and
do not raise timeouts or budgets against a failure nobody has reproduced.

### Isolate verification from the user's live data

Tests, probes and harnesses run against isolated home, data, configuration and environment roots;
pin that isolation with a guard test. A fixture that defaults to the user's real documents or
ledger can overwrite them. Run every harness that is written and check its result before relying
on it. Experiments against a running user application (a desktop host, an editor, a live store)
use an allowlist of verified operations; ask the user to save first and do not repeat a crash to
confirm it.

## Completion checklist

Before completing substantial work, confirm:

- Paths and names reveal domain ownership and functional responsibility.
- Business rules have one authoritative owner and exposed contracts have clear consumers.
- Services and shared modules live at the narrowest scope that serves their real consumers.
- No new circular dependencies, forbidden imports, app-to-app imports, or client/server leaks exist.
- No duplicate implementation, unused abstraction, empty scaffold, or abandoned compatibility path remains.
- Relevant consistency, failure recovery, resource usage, and authorization behavior are verified.
- Every reported state was read back from its authoritative target, and every new gate was seen to fail.
- Each follow-up announced during the task is in the plan or tracker and is reported as done,
  dropped with its reason, or open. Requested work that was not done is reported as not done.
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

