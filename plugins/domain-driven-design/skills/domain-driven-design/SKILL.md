---
name: domain-driven-design
description: Automatic principal-level engineering baseline for production-code tasks in applications, APIs, workers, and monorepos. Apply during implementation, fixes, refactoring, and architecture review without requiring a skill name or trigger phrase. Group by domain then function, using scoped services, shared modules, and reusable engines. Trace created modules and changed paths for integration gaps, bugs, and required behavior; preserve explicit agent handoffs. Apply small fixes locally without triggering a repository restructure. Excludes prose-only work and generated or vendor edits.
---

# Principal Driven Domain Design
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Make business ownership obvious from paths, names, contracts, and dependencies.
Optimize for correct behavior, readable change, measured performance, and economical evolution.
Apply this skill to the requested change; it is not authorization to redesign the project.

## Automatic execution
Apply this baseline before planning or editing production code; do not wait for a skill invocation,
trigger phrase, or an architecture request. Carry out authorized implementation, reuse, gap fixes,
verification, and handoffs as part of the coding task, rather than merely suggesting them.
For review-only or planning-only tasks, apply the same reasoning without editing code. Keep work
proportional to scope and risk; automatic use does not authorize unrelated changes or delegation.

## Agent portability and handoffs

These are tool-neutral instructions for agents that can read Markdown and inspect a project.
Use available search, build, test, and runtime tools; no particular vendor, plugin, or CLI is required.
Honor the host's instruction hierarchy, permissions, and explicit task scope. This skill does not
enable disabled capabilities or grant permission to deploy, publish, or perform destructive changes.

When delegation is already authorized, pass the skill's accessible path or relevant instructions,
owned files/modules, acceptance conditions, and trace obligations in the assignment. Do not assume
a child agent inherits the parent's conversation, loaded skills, or global instruction files.
Require evidence and unresolved edges back from each worker; reconcile traces across worker boundaries.
Delegate verified invariants; label proposed algorithms as assumptions and challenge contradictions.
If the child cannot read the skill, supply its relevant contents within the allowed context.
Do not spawn agents merely because this section describes handoffs.
Before adopting another workflow, record any explicit user-authorized teammate limit and roles.
Every new exploration, implementation and review agent consumes that budget; resuming an existing
agent does not allocate a new slot. Follow-up reviews stay in the coordinator when the budget is
exhausted. An absent numeric cap is not permission to delegate, and optional workflow skills cannot
expand the user's limit.
Treat task briefs and pseudocode as proposals: independently check their algorithms against the
original contract. Correct a flawed plan instead of preserving it as an implementation requirement.

### Handoff contract
Every authorized agent assignment or resumable handoff must identify:

| Field | Required context |
| --- | --- |
| Goal and limits | User outcome, acceptance checks, authorized actions, exclusions |
| Location | Accessible workspace root, actual branch/worktree or revision, relevant instruction/skill paths |
| Ownership | Exact files/modules the agent owns; other active owners and shared interface dependencies |
| Architecture | Domain owner, public entrypoints/contracts, important caller and consumer paths |
| Current state | Implemented versus pending work, local edits, decisions and why, known failures |
| Evidence | Commands and results, trace-ledger path/IDs, verified revision, unavailable environments |
| Next action | Concrete next step, blockers, required inputs, and expected return format |

Hosts may enforce this contract with [the delegation guard](scripts/guard_handoff.py).
The optional Claude guard supplies this baseline path and checks explicit numeric agent limits in the
native user turns (`Use N teammates/agents/workers` and common polite forms). Quoted, fenced or
negated examples cannot increase the cap. The first explicit cap starts a budget; repeating or
changing it retains usage within that budget. Only an explicit native instruction such as
`Start a new delegation budget: use N agents` resets it.
Malformed records do not erase a previously parsed cap. Missing history and natural-language
restrictions outside this limited parser remain the coordinator's responsibility. The runtime
must validate resumed agent identities. This local guard covers recognized coding workspaces;
an unrecognized workspace does not waive this baseline or grant delegation permission. It does
not establish remote accessibility or prove the semantic correctness of a handoff.
The child must read the accessible baseline and relevant linked guidance before acting. The hook
adds a compact reminder rather than embedding the entire skill on every call; if the child cannot
access the skill, supply the relevant contents as required above. Repeated hook processing must
not duplicate that reminder or bypass validation and budget checks.
When that guard is installed, prefix the assignment with `HANDOFF_JSON=` and a JSON object containing
`goal`, `limits`, `workspace`, `revision`, `owns`, `interfaces`, `state`, `evidence`, `next`, `return`,
`trace`, `checks`, and `baseline`. `return` must be an object with nonempty `paths`, `contracts`,
`checks`, `gaps`, and `remaining` instructions. `trace` names paths and failure cases to follow;
`checks` names checks to run or why unavailable. `baseline` is this skill's accessible path. This applies
to exploration and review assignments too. A rejected assignment must be corrected before retrying.
Handoff fields must contain meaningful nonblank text or nonempty structured context; workspace and
baseline paths must be text. When `workspace` differs from the launch checkout, add an `isolation`
object with `confirmed: true`, the matching absolute `workspace`, and a nonblank `reason`. The
coordinator must verify that checkout and its authority; an isolation keyword in prose is not
confirmation. These declarations do not authorize a new workspace, branch, or external action.

Use actual paths on the receiving agent's host; include the necessary content when paths differ or
are inaccessible. Give commands their working directory and required non-secret configuration names.
Never place credentials or private runtime payloads in handoff notes. A branch name alone is not
proof that a child sees uncommitted work; establish whether the checkout is shared or isolated.

For concurrent work, agree public contracts and file ownership before overlapping changes. Tell
agents they are not alone: preserve others' edits and coordinate shared files through the assigned
owner. Rebase or reconcile isolated changes before claiming integration; do not silently discard work.
On return, report changed paths, public-contract changes, checks with outcomes, gap IDs/status, and
remaining actions. The coordinator reconciles the trace ledger and verifies cross-agent seams and
affected consumers; several passing worker checks do not establish a working integrated workflow.

For interruption or context loss, save the handoff in the existing task/trace record with a timestamp
and content revision, then link that record. On resume, inspect the checkout and current diff before
acting; revalidate stale assumptions. Do not create a second source of task truth.

Local installation does not imply cloud, remote-host, or unrelated agent installation. Establish
discovery on each execution host; use a host-native global instruction to route relevant work here.
If discovery or file access is unavailable, report that limit instead of claiming global enforcement.

## Principal engineering contract
- Start with business capabilities, invariants, user workflows, and operational constraints.
- Prefer high cohesion within domains and low coupling between them.
- Put domain-specific code with its owner; group code by function inside that boundary.
- Give each business rule and authoritative write model one clear owner.
- Reuse existing implementations before adding another; avoid duplicate business knowledge.
- Choose the smallest architecture that meets demonstrated needs and supports likely change.
- Separate observations, assumptions, decisions, and evidence. Do not invent requirements or benchmarks.
- Preserve working public behavior during structural changes unless behavior change is requested.
- Improve the touched path and its necessary dependencies. Do not sweep unrelated code into the task.

## 1. Establish context before editing

For project continuity, check `.principal-ddd/index.md` when present, then read the linked owning
tracker and relevant trace. Use the [project records convention](references/project-records.md)
when creating or migrating DDD records. Do not scaffold empty folders or replace an existing tracker.

Inspect applicable repository instructions, manifests, package exports, entrypoints, existing
domain modules, migrations, tests, and relevant runtime evidence. Search for equivalent behavior
and existing shared packages before creating files. Use the repository's language and tooling.

Trace one relevant workflow from user or event input through authorization, service, domain
rules, persistence, downstream effects, and returned or displayed state. Include error paths.
Identify real consumers and writers; a directory name alone does not establish ownership.
Map actual repository roots and owning release units before creating or copying files. Keep each
repository's implementation, deployment/rollback tooling and evidence with that owner, including
verification folders; a multi-repository task does not merge their ownership. Apply the repository
ownership rules in [architecture guidance](references/architecture.md#repository-ownership-and-operational-artifacts)
when work crosses repositories or captures source/artifact evidence.

For substantial architecture work, establish a compact decision frame:

| Question | Required answer |
| --- | --- |
| Business outcome | Which user workflow or invariant changes? |
| Ownership | Which bounded context owns the meaning and authoritative writes? |
| Consumers | Which apps, jobs, modules, or external systems need the capability? |
| Constraints | Compatibility, data volume, latency, tenancy, availability, cost, deployment? |
| Current evidence | Relevant paths, contracts, failures, timings, or query behavior? |
| Smallest change | What can be reused, and what boundary actually needs changing? |
| Completion | Observable acceptance conditions and appropriate verification? |

Ask only when an unresolved business decision blocks correct work; otherwise state assumptions.

## Architecture guidance when relevant

Keep domain ownership explicit; place services and shared behavior at the narrowest useful scope,
reuse existing capabilities, and preserve public contracts, persistence, authorization and tenant
boundaries. Keep privileged code out of clients and respect framework/package conventions. Apply
small fixes locally rather than restructuring the repository. Do not add engines, queues or other
frameworks without demonstrated need. Retain risk limits and established operational policies.

For changes touching the following decisions, read the matching sections of
[architecture guidance](references/architecture.md) before editing. Load only applicable sections;
small local fixes do not require every architectural example in context.

| Decision | Reference section |
| --- | --- |
| Domain ownership and boundary placement | [2. Boundaries](references/architecture.md#2-define-the-domain-boundaries) |
| Modules, services, workspace packages and framework integration | [3. Structure](references/architecture.md#3-structure-by-domain-then-function) |
| Imports, exports and client/server boundaries | [4. Dependencies](references/architecture.md#4-enforce-dependency-direction) |
| Business rules, value precision, schemas and public contracts | [5. Modeling](references/architecture.md#5-model-behavior-and-contracts-precisely) |
| Shared behavior and reusable engines | [6. Reuse](references/architecture.md#6-reuse-without-erasing-ownership) |
| Persistence, idempotency and asynchronous workflows | [7. Data ownership](references/architecture.md#7-design-data-ownership-and-reliable-workflows) |
| Measured performance, resource budgets and scaling | [8. Performance](references/architecture.md#8-make-performance-and-scale-evidence-driven) |
| Authorization, tenant isolation and operational recovery | [9. Security](references/architecture.md#9-preserve-security-and-operability-at-boundaries) |
| Refactoring, compatibility and migrations | [10. Safe evolution](references/architecture.md#10-evolve-existing-projects-safely) |

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
