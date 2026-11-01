# Gap finding and module tracing

Read this when tracing created or changed modules, running a gap audit, recording findings in the
gap ledger, or creating or archiving evidence. These rules carry the same authority as
[SKILL.md](../SKILL.md); the records convention is in [project-records.md](project-records.md).

## 11. Find gaps and trace every module

Gap finding compares intended behavior with implemented, connected, and observable behavior.
Gap tracing follows the actual paths that establish where a missing step, defect, or inconsistency
starts and which consumers it affects. A file existing or compiling does not establish a working path.

Run a complete connected-path trace for every module created. For changed modules, retrace affected
paths and adjacent contracts. For an explicit full-project gap audit, inventory every first-party
module and its entrypoints, including workers, scheduled tasks, event handlers, and internal tools.
Track inventory coverage; do not sample a few modules and describe the result as a full audit.

Define a module as a cohesive public capability, package, engine, or registered runtime handler;
trace its implementing files too. Inventory orphaned exports and unregistered handlers explicitly.
Use a visited set of modules and edges to terminate cycles. Record forbidden or harmful dependency
cycles as findings; a legitimate runtime loop is not automatically a defect.
Bound traversal by named workflows and repository/host scope, not an arbitrary number of hops.
At external boundaries, inspect the local adapter and published contract; record unavailable remote
internals as a coverage boundary. Generated/vendor internals need no edits, but their integration
contracts still need checking. Do not equate excluded internals with verified behavior.

### Edge checks

A change set is a set of pieces, and every piece edge is a contract with a mechanical test. A
misfit is an edge with no mate, or two mates that disagree about one fact. Test every edge the
change touches; each failure below is a defect class, not a style preference. These are
file-independent: any can fail while per-file review and build gates stay green. Apply the
relevant edge checks; use static, contract or runtime proof appropriate to the edge instead of
creating a new test for every row. Record why an edge is inapplicable or remains unverified.

| Edge | What must mate | Test |
| --- | --- | --- |
| Consumer | New module to a real supported caller or executable entrypoint | Trace imports, registered commands, handlers or documented tool invocation outside the module and its tests; a standalone CLI need not have a production importer |
| Contract | New field or event to a consumer that selects it, and the reverse | Search each added field in the consuming codebase, then search the consumer's request for fields the producer does not declare |
| Mount | New component to a page or parent that renders it | Search the name outside its own file and tests |
| Registration | Handler/model to its registry or loader, shipped runtime file to the actual build and deployment mechanism | Check the registries and artifact mechanisms used by this project; do not assume every project deploys a tar archive |
| Cadence | Trigger policy, completion, overlap ownership and retries | Preserve fixed wall-clock/calendar anchors and intentional fixed-rate cadence. For completion-relative loops, schedule from completion; verify bounded retries and overlap/catch-up policy without changing declared timing |
| Discriminator | One consistent meaning across every relevant decision and persistence site | Trace each handler, validator, serializer and reader; multiple decision sites can be legitimate, but variant meaning, exhaustive handling and missing-field semantics must agree |
| Default | An absent argument to one meaning | Absence must not mean one lane on one side of a call and no lane at all on the other |
| Back-compat | A changed persisted key or field shape to the rows written before the change | Read one pre-change row through the new code path; a new variant should take a new shape and leave the old one resolvable, and the datastore's treatment of a missing field must land those rows on the legacy branch |
| Snapshot | Reviewed content to the revision or artifact actually being claimed | When Git staging is relevant, compare index and worktree including derived files; otherwise identify the actual files/artifacts by content hash and mark staging inapplicable |
| Concurrent writer | A path to exactly one writer for the duration of the change | Establish what else writes each touched path — an automated appender, a scheduled job, another agent — before editing or staging it wholesale; a path with another live writer is staged by hunk or left alone, never swept in |
| Headroom | The change to every chokepoint file it must pass through | Remaining budget against the cap, and whether a baseline or ratchet exempts that file |

Identify whether a task uses a fixed wall-clock/calendar schedule, fixed-rate polling or a
completion-relative loop before assessing cadence. Preserve timezone, market/calendar anchors,
leases and overlap ownership, bounded catch-up and missed-run behavior. Test long-running work,
failures and clock/calendar boundaries where relevant; a retry must follow its declared bounded
backoff policy without silently moving the next scheduled anchor or weakening risk/freshness rules.

Order work by cost and yield: inspect existing gate results first and run cheap affected checks
when evidence is missing or uncertain. Full suites are not automatically cheap. Honor repository
requirements for gate scope and timing. Cluster changed files by business vocabulary; trace the
cluster with the most new domain nouns end to end, then cross-boundary contracts. Check the
snapshot edge last, because staged/working-tree divergence can invalidate earlier conclusions.
A coherent working tree establishes nothing about the commit that ships.

Record which edges were tested for which cluster, and carry that into the gap ledger below. An edge
not tested is an unverified path, not a passed one: "fit checked" is not a claim, whereas "consumer,
contract, and registration edges tested on these four clusters; cadence untested because no periodic
task changed" is. Account for edges the same way this section accounts for modules, and state which
of them no available evidence could close.

Report a fit finding as: the edge that failed, the exact sites on both sides of it as path and line,
what ships if nobody fixes it, the smallest fix, and a severity where blocking means something
breaks on the next commit or deployment and latent means no caller reaches it yet. Open with the
cluster map rather than a file list, and close with the checks actually run and their results,
naming separately what was not verified.

Recurring traps in fit review:

| Trap | Instead |
| --- | --- |
| A file list, or notes filed per file | Clusters, and the edges between them |
| Treating green gates as proof of fit | Gates establish files; fit lives between them, and every edge above can fail with all gates green |
| Checking a contract edge in one direction | A field the producer added and a field the consumer selects are two separate tests |
| Calling a cadence outlier the defect | Identify the declared schedule first; test anchor drift, unintended overlap, catch-up and retry behavior against that policy rather than forcing completion-relative timing |
| Calling a near-duplicate a reuse violation | Compare inputs, consumers, and trust boundaries first: offline untrusted input and live authoritative reads are different contexts |
| Reviewing the working tree and calling the change reviewed | Review what the next commit contains |
| Relieving a chokepoint by raising its cap | Extract a cohesive group, keep registration and call order identical, and give the extracted module its own test |

### Trace procedure
1. **Inventory:** List created/changed modules, their owner, public exports, runtime registration,
   callers, dependencies, configuration, and affected consumers. Include migrations and code generation.
   When Git staging is relevant, record staged-versus-working-tree state; otherwise record the
   applicable content identity. Check any actual line/complexity caps, including exemptions,
   without inventing a universal file-size limit.
2. **Trace backward:** Find how real UI actions, routes, jobs, commands, or events reach each module.
   Check package exports, imports, dependency wiring, routing, subscriptions, and feature gates.
3. **Trace forward:** Follow branches through services, rules, ports, adapters, writes, emitted events,
   queues, projections, caches, notifications, and returned/displayed state to the terminal outcome.
   Continue across app and domain boundaries through their public contracts.
4. **Trace alternatives:** Follow rejection, invalid state, empty state, timeout, cancellation, retry,
   duplicate delivery, partial success, concurrent update, authorization, and tenant paths as applicable.
   Check creation, updates, deletion, restart, replay, and cleanup where those lifecycles exist.
5. **Check adjacent behavior:** Inspect producers and consumers of changed contracts, schema readers
   and writers, cache invalidation, UI state handling, permissions, and operational recovery. A repaired
   producer can still leave its consumer broken. Follow indirect callers and asynchronous consumers.
6. **Compare intent:** Check acceptance criteria, established contracts, domain invariants, repository
   docs, and tests against the trace. Identify missing implementation, wiring, or required behavior.
7. **Resolve and retrace:** When implementation is authorized, fix confirmed bugs and required
   behavior, then retrace the repaired path and affected consumers. For review-only work, report
   findings and proposed fixes without mutating code. Stop when scoped acceptance is met or a
   concrete external blocker prevents further proof; do not widen the audit to unrelated work.

Use source search, call sites, imports/exports, route and handler registries, dependency injection,
schema references, tests, and available runtime evidence. Static reachability is not runtime proof.
Dynamic dispatch, reflection, plugins, generated code, and external consumers may need additional
registry, contract, or runtime evidence. Mark an unresolved edge as unverified; do not assume it works.

### Gap ledger and continuity
Use the project's existing tracker or owning gap ledger as the default record for work of any size.
Update the existing task entry with a concise outcome, checks and results, reviewed revision/hash,
open gaps and next action. Where the repository requires both a status tracker and a technical
ledger, link them and keep each fact in its owning record rather than duplicating reports. For a
small change without an existing tracker or a durable handoff need, report results in the final
response. For a full audit or substantial change without an existing record, use one compact
`.principal-ddd/gap-trace.md`, discovered through `.principal-ddd/index.md`. Keep established trackers
authoritative and link them; do not fork their status into a second ledger. Follow the linked
project-records convention before moving existing data. Do not create a new report or dated
verification folder per run, or put project-specific state into this global skill.

Record enough evidence for another agent to resume:

| Module/path | Entry and consumer | Dependencies and effects | Evidence | Gap and impact | Resolution/status |
| --- | --- | --- | --- | --- | --- |

For each path, record the source revision or date, actual file/symbol references, checks performed,
and status: `verified`, `static-only`, `gap-found`, `fixed-and-verified`, `blocked`, or `not-applicable`.
Give findings stable IDs, severity, affected consumers, reproduction or evidence, owner/next action,
and a closure check. Tie verification to the reviewed content revision or hash; a date alone cannot
establish that evidence remains current. Keep module inventory and edge/path evidence linked.
Record why a path is inapplicable. Preserve unresolved items and reopen stale evidence after relevant
code or contract changes. On resuming work, read this ledger and revalidate affected assumptions.

Classify findings before acting:

- **Bug:** Existing behavior violates a supported contract or invariant; give the failing path and impact.
- **Integration gap:** Implementation exists but registration, data flow, exports, or a consumer is missing.
- **Required feature gap:** The authorized workflow cannot complete because necessary behavior is absent.
- **Improvement opportunity:** Useful additional capability without evidence that current scope requires it.
- **Unverified path:** Evidence or an environment is unavailable; name the exact missing verification.

Disprove each candidate before recording it. Compare the pre-change revision of the same path: a
defect that predates the change is a pre-existing condition, not this change's. Locate real call
sites: a hazard no caller reaches is an unverified path or a latent risk, not a bug, and the record
must say why it is unreachable. Establish whether an asymmetry is principled before calling it an
inconsistency - two sibling contracts may differ legitimately when one must represent an empty
population and the other is only constructed from a non-empty one. Record which candidates were
disproved and on what evidence; a report of survivors alone cannot be audited and invites the next
reviewer to re-investigate settled questions.

Prioritize by user impact, data correctness, security, and blast radius. Fix bugs and required gaps
within the task's authority; capture unrelated findings and optional features as proposed follow-ups.
Do not invent requirements from personal preference or silently turn a module trace into a new product.
Do not claim universal absence of gaps: report covered paths, concrete evidence, and remaining limits.
Report inventoried versus traced modules and checked versus unresolved edges separately from runtime
checks. Before claiming a full audit, account for every inventoried module and discovered in-scope
edge, including explicit exclusions and blockers. A full inventory with static-only paths is a full
static trace, not complete runtime verification. Stop retrying an unchanged blocker; preserve the
specific evidence and recovery action instead of repeating the same unsuccessful check.

### Evidence retention and archival

Create separate evidence files only when needed for deployment, rollback, an actual audit, or an
active monitor. Link to existing CI results, native receipts or durable logs when they satisfy the
need; do not duplicate them. Routine tests, builds and checks belong as concise results in the
existing tracker, not new log dumps, screenshots or JSON snapshots. Do not relabel routine work as
an audit to justify extra files. This policy concerns evidence artifacts, not source code, tests
or maintained product/design documentation required by the task. Do not relabel raw verification
output as design documentation to evade the retention rules.
Record the purpose, consumer and retention/archival trigger for a necessary evidence bundle in its
owning tracker; create a manifest only when the bundle needs one. Keep evidence in the repository
that owns the code or release it proves. An allowed evidence purpose does not permit storing a
sibling repository's source, patches, operators or release artifacts in the current repository.
Use cross-repository links and immutable identities for combined acceptance; follow the repository
ownership and migration rules above before relocating existing active evidence.

As part of finishing authorized work, archive superseded or bulky evidence from that task once it
is stable and no active consumer needs its original location. Reuse the repository's archive tools
and conventions; do not start an unrelated repository-wide cleanup or a new archival framework.
Before moving files, trace scripts, manifests, deployment/rollback paths, monitor prompts/state,
dynamic filename readers, links and concurrent writers. Preserve live or pinned paths; change owned
references only when their consumers can be verified. Leave uncertain or actively written files in
place and record the remaining scope without blocking independent cleanup.

Keep current decisions, unresolved findings, source/artifact identities and active handoffs easy to
find in the existing tracker. Preserve required audit originals, protocols, failure evidence and
recovery records, either in place when consumed or in the archive when safe. Use lossless archives
with original relative paths, checksums and restoration instructions. Verify archive contents and a
restore before removing originals; restoration must not overwrite newer work. Preserve access
restrictions and verify affected consumers without triggering jobs or deployments. Summarize the
archive location and checks in the existing tracker. Archiving does not close gaps, turn failed
checks into passes, or establish deployment or production success.
