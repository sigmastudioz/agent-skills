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
Before adopting another workflow, record the user-authorized teammate count and roles. Every
exploration, implementation and review agent consumes that budget; follow-up reviews stay in the
coordinator when it is exhausted. Optional workflow skills cannot expand the user's limit.
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
The optional Claude guard supplies this baseline and checks explicit numeric agent limits in the
native user turns (`Use N teammates/agents/workers`); missing history leaves enforcement to the
coordinator. It does not grant tools or guarantee semantic correctness.
When that guard is installed, prefix the assignment with `HANDOFF_JSON=` and a JSON object containing
`goal`, `limits`, `workspace`, `revision`, `owns`, `interfaces`, `state`, `evidence`, `next`, `return`,
`trace`, `checks`, and `baseline`. `return` must be an object with nonempty `paths`, `contracts`,
`checks`, `gaps`, and `remaining` instructions. `trace` names paths and failure cases to follow;
`checks` names checks to run or why unavailable. `baseline` is this skill's accessible path. This applies
to exploration and review assignments too. A rejected assignment must be corrected before retrying.

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

Inspect applicable repository instructions, manifests, package exports, entrypoints, existing
domain modules, migrations, tests, and relevant runtime evidence. Search for equivalent behavior
and existing shared packages before creating files. Use the repository's language and tooling.

Trace one relevant workflow from user or event input through authorization, service, domain
rules, persistence, downstream effects, and returned or displayed state. Include error paths.
Identify real consumers and writers; a directory name alone does not establish ownership.

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

## 2. Define the domain boundaries

A bounded context owns a coherent business vocabulary, rules, and model. A feature, table,
screen, framework layer, deployment, or team name is not automatically a bounded context.
Use business capability names such as `billing`, `scheduling`, `playback`, or `execution`.

- Separate contexts when the same term has different meanings, invariants, lifecycles, or owners.
- Keep entities together when their invariant must be enforced in one atomic operation.
- Avoid oversized aggregates: distinguish true atomic invariants from cross-context workflows that
  need explicit consistency, orchestration, or compensation instead of a shared transaction.
- Distinguish core business differentiation from supporting and commodity capabilities.
- Invest modeling effort where complexity or business value warrants it; keep simple CRUD simple.
- Record upstream/downstream ownership and translation at important context boundaries.
- Consume another context through its public API, port, or contract; do not import its internals.
- Translate external/provider models at the boundary rather than leaking them into business rules.
- Prefer a modular monolith until independent deployment, scaling, failure isolation, or ownership
  justifies a service split. A monorepo does not imply microservices.

If a change spans domains, identify the orchestrating use case and each domain's responsibility.
Put orchestration with the workflow's owner, not in a global helper or UI component.

## 3. Structure by domain, then function

Choose the owning scope first, then the functional category. Within that scope:

| Category | Responsibility |
| --- | --- |
| `model/` | Entities, value objects, invariants, policies, domain events |
| `services/` | Named application use cases and orchestration |
| `ports/` | Interfaces for persistence, clocks, identity, queues, providers |
| `adapters/` | Concrete database, transport, provider, or platform implementations |
| `contracts/` | Public DTOs, event schemas, validation, compatibility contracts |
| `components/`, `hooks/` | Domain UI and UI behavior when that domain owns a frontend |
| `shared/` | Reusable code for consumers within that scope |
| `tests/` or colocated tests | Behavior and boundary verification using repository conventions |

Service implementations belong in `services/` at their owning layer. When a domain service is
needed for a rule spanning entities, place it in `model/services/`; orchestration stays in the
domain's main `services/`. Provider services can live in `adapters/services/` when useful.

For one app, use `src/domains/<domain>/{model,services,ports,adapters,contracts,shared}` as
needed, a public entrypoint, thin framework routes and a composition root. Put domain-neutral
primitives under `src/shared/`. Create only directories containing real code.

Monorepo example; respect existing package conventions and explicit exports:

```text
apps/
  web/                           # App composition and presentation
  api/                           # Thin transport entrypoints
  worker/                        # Job registration and composition
packages/
  billing/                       # Owned workspace package
    package.json                 # Public exports and runtime compatibility
    src/
      services/                  # Use cases shared by API/worker
      shared/                    # Billing-local reuse
      index.ts                   # Explicit public facade
  shared/
    contracts/                   # Domain-neutral workspace package
    ui/                          # Compatible frontend consumers
```

Register real packages in the workspace; paths alone do not make them importable.
In polyglot workspaces, expose compatible libraries or generated clients from canonical schemas;
do not attempt to import code across incompatible runtimes.

### Placement rules
1. One consumer and domain-specific meaning: keep it in that domain.
2. Several consumers inside one domain: use that domain's `services/` or `shared/`.
3. Several compatible apps need reusable domain code: put it in a workspace domain package;
   privileged server behavior remains server-side behind an authorized API or client contract.
4. Several domains need the same domain-neutral primitive: use scoped `shared/` code.
5. Consumers need different business meanings: keep separate models and translate explicitly.
6. Cross-domain workflow: use an owning application service and public domain contracts.
7. Routes, screens, controllers, and jobs: delegate rules to services; keep transport concerns local.

Never copy a capability into multiple apps just to make imports convenient. Never make an app
the library for another app. Move reusable ownership downward to a package both can depend on.
Keep required framework directories; route them into the domain structure rather than fighting
the framework. Respect language-standard packaging and valid existing architecture.

## 4. Enforce dependency direction

```text
entrypoints -> public application services -> model + ports
adapters -> ports + model
bootstrap -> services + adapters             # Wires concrete implementations
domain packages -> domain-neutral shared packages
```

- The model does not depend on HTTP, UI frameworks, databases, queues, or provider SDKs.
- Services orchestrate use cases through explicit dependencies; adapters implement ports.
- Shared packages do not import apps or domain internals. Avoid circular dependencies.
- Cross-domain calls use public contracts; avoid synchronous call cycles and chatty chains.
- Export intentional entrypoints. Block deep imports with existing package, lint, or build tools.
- Split browser-safe contracts from server-only implementations and privileged dependencies.
- Keep privileged SDKs, database clients, secrets, and filesystem code out of client dependency graphs.
- Provider SDKs may run in a client only when designed for it, with public credentials and an
  explicit security model; privileged server SDKs never belong in a client bundle.
- Keep platform-specific UI separate when web and native have different rendering requirements.
- Use explicit runtime exports and type-only imports where supported. Avoid broad barrel exports
  that hide cycles, inflate bundles, or expose private APIs.

Enforce boundaries mechanically with existing tools when the change introduces or repairs a
boundary. Do not introduce a new architecture toolchain for an isolated low-impact edit.

## 5. Model behavior and contracts precisely

- Use the domain's vocabulary consistently in code, contracts, tests, and user-facing states.
- Name modules by responsibility and operations by intent: `issueInvoice`, `reserveSlot`.
- Avoid vague `Manager`, `Helper`, `Common`, `misc`, and giant catch-all `utils` modules.
- Give entities stable identity; use value objects for validated concepts without independent identity.
- Make invalid states unrepresentable when practical; use explicit state transitions and typed results.
- Define aggregate boundaries around transactional invariants; reference other aggregates by identity.
- Keep rules in the model or its owning service, not duplicated across controllers, jobs, and screens.
- Distinguish business failures from transport/provider failures and preserve useful error context.
- Validate untrusted input at boundaries; enforce invariants again at the authoritative write path.
- Use explicit precision, currency, units, timezone, and effective dates where the domain requires them.
- Inject nondeterministic dependencies such as time, randomness, and external I/O when verification
  or correctness requires control. Do not add interfaces with no useful variation or boundary.
- Treat IDs, authorization context, and tenant scope as explicit inputs at trust boundaries.
- Keep public contracts small and version-compatible; consumers should not depend on ORM entities.
- Design queries for consumer needs without granting consumers ownership of another domain's writes.

## 6. Reuse without erasing ownership

Search existing code and call sites before introducing a helper, service, schema, or package.
Extract a shared implementation when consumers share the same rule, lifecycle, and semantics.
Migrate all affected callers and remove the replaced implementation within the authorized scope.
Reuse the repository's libraries and dependencies before introducing new ones.

Do not deduplicate merely similar syntax across contexts with different meanings. Independent
domain models are legitimate; an abstraction that couples unrelated business rules is not reuse.
Document intentional duplication when its rationale would otherwise be unclear.

Share canonical schemas and generate compatible clients/types where supported; do not maintain
hand-copied payload definitions. Share stable primitives rather than a giant universal domain model.
Prefer composition, explicit inputs/outputs, and cohesive modules over inheritance and flag-driven
mega-services. Introduce abstractions at demonstrated seams, not hypothetical future variations.

### Cluster cohesive behavior into a reusable engine

Look for a reusable engine when multiple workflows or apps repeat a cohesive algorithm, ruleset,
state machine, scheduling process, reconciliation process, or execution pipeline. An engine owns
that reusable behavior behind a small contract; it is more than a folder of miscellaneous helpers.
Use an engine when consolidating shared knowledge reduces drift and makes change or verification
materially simpler. Reuse or extend an existing engine before introducing another.

Before extracting, inspect real consumers and establish:

- The common invariant or algorithm and which domain owns its meaning.
- The stable input, output, errors, state transitions, and supported extension points.
- Which differences are configuration, which are explicit policies, and which require separate models.
- The runtime, precision, ordering, performance, and compatibility requirements of each consumer.

Keep domain-specific engines inside their owning domain, for example
`domains/billing/engines/reconciliation/`. If multiple apps need it, make that domain module a
workspace package or expose the engine through an existing domain package's public exports.
Use `packages/shared/engines/<capability>/` only for genuinely domain-neutral behavior.
Keep orchestration services in `services/`, including within an engine when it owns services;
keep engine-local reusable primitives in `shared/`. Create only necessary internal categories.

Prefer a deterministic core with injected ports for storage, time, queues, providers, or devices.
Keep transport and platform adapters outside the core. Expose a small, intention-revealing API;
prevent consumers from depending on engine internals. Use explicit policies for real supported
variation instead of growing flags, global state, special-case app names, or hidden callbacks.

Migrate actual callers to the engine and remove superseded implementations. Verify the shared
invariants once at the core and each consumer's contract and integration separately. Run the gap
trace across every caller, adapter, state transition, and downstream effect affected by extraction.
Record ownership and compatibility obligations when the engine becomes a shared dependency.

Do not force unrelated rules into one engine because their code looks similar. Do not create a
generic engine framework for one simple use case. Engine extraction is a task within the authorized
scope; propose a wider consolidation separately when it would require unrelated product changes.

## 7. Design data ownership and reliable workflows

- Identify the system of record, authorized writer, transaction boundary, and consistency model.
- Other domains read through supported APIs or owned projections; avoid cross-domain table writes.
- Separate source facts from derived views. Specify freshness and reconciliation where they matter.
- Protect concurrent updates with suitable constraints, transactions, version checks, or atomic writes.
- For retried commands, define idempotency scope, durable uniqueness, payload consistency, and result reuse.
- Encode compound string identities with `JSON.stringify([tenantId, requestId])` or nested keyed
  maps; use an equivalent injective encoding in other runtimes. Changing a separator to NUL still
  collides for unrestricted IDs. Verify distinct tuples stay distinct; do not invent character bans
  absent from the public contract. Apply the same encoding consistently across writers and retries.
- For external effects, use provider idempotency where available and persist recoverable operation state.
- When committed state must publish an event reliably, consider a transactional outbox or equivalent.
- Assume messages can repeat or arrive out of order unless a stronger guarantee is established.
- Define retry bounds, backoff, timeouts, poison-message handling, and recovery for asynchronous paths.
- Do not claim exactly-once effects from an acknowledgement or a process-local deduplication set.
- Model long workflows with explicit states and compensations where atomic transactions cannot apply.
- Version persisted events and public schemas; account for older consumers and replay behavior.

Use these techniques when the workflow needs them; do not add a queue, event bus, CQRS, saga,
or event sourcing merely to appear scalable. CQRS can be separate functions over one database.

Recurring project concerns to recognize when relevant:

| Workload | Engineering consequence |
| --- | --- |
| Billing and ledgers | Exact monetary arithmetic, immutable audit evidence, reconciliation, idempotent posting |
| Trading and execution | Explicit live/simulated modes, risk limits, stale-data checks, replayable decisions |
| Broadcast and playback | Resource ownership, lifecycle cleanup, bounded buffering, timing and device failures |
| Multi-app workflows | Stable contracts, per-consumer permissions, compatible releases, explicit handoff state |
| Agent orchestration | Durable job identity, cancellation, bounded concurrency, recoverable ownership |

These are prompts to inspect actual requirements, not assumptions about every project.

## 8. Make performance and scale evidence-driven

Define relevant budgets from requirements or measured baselines: latency distribution, throughput,
memory, startup, bundle size, query count, freshness, or infrastructure cost. State missing data.

- Examine algorithmic complexity, N+1 queries, overfetching, repeated serialization, and repeated work.
- Bound queries and collections with pagination, selective reads, indexes justified by access patterns,
  batching, and sensible limits. Check execution plans for consequential database changes.
- Bound concurrency, queues, buffers, retries, and resource lifetimes; use cancellation and backpressure.
- Cache only with an ownership, tenant isolation, freshness, invalidation, and failure policy.
- Keep blocking CPU work off latency-sensitive event loops; isolate it only when measured need warrants it.
- Profile hot paths before adding memoization, parallelism, infrastructure, or distributed services.
- Check shared-package imports for runtime compatibility, tree shaking, and bundle consequences.
- Identify the next bottleneck and operational trigger before proposing independent scaling.
- Match availability, recovery time, and acceptable data loss to actual requirements. Analyze
  capacity and failure domains before claiming horizontal scaling or high availability.

Readable code and explicit ownership come first unless measurements establish a necessary tradeoff.
Record actual before/after evidence for performance claims; do not equate fewer lines with faster code.

## 9. Preserve security and operability at boundaries

Enforce authorization and tenant isolation on the server at every relevant entrypoint, including
workers and internal APIs. UI visibility is not authorization. Validate file, URL, and provider input
where it crosses a trust boundary. Scope credentials and redact sensitive operational data.

Propagate correlation, causation, job, or trace identifiers across asynchronous and service boundaries.
Record meaningful domain outcomes, failures, retries, and durations using existing observability.
Make partial failures visible and recoverable; do not silently substitute success, empty data, or stale
state unless that behavior is explicitly part of the contract. Clean up streams and subscriptions.

For consequential changes, identify failure containment, rollback, and recovery behavior. Design
operational evidence around the workflow so an operator can distinguish pending, failed, and complete.

## 10. Evolve existing projects safely

Do not rename or move the whole repository to match an example. Prefer a vertical slice:

1. Capture the relevant behavior and consumers; add a regression test when behavior is at risk.
2. Establish the target boundary and public contract at the narrowest responsible scope.
3. Move or extract the implementation and update imports, exports, tests, and workspace wiring.
4. Preserve compatibility through a temporary facade only when consumers need staged migration.
5. Give compatibility code an owner and removal condition; avoid indefinite parallel implementations.
6. Verify affected consumers and remove obsolete paths after migration is proven.

Use expand/migrate/contract for incompatible schema or contract changes. Account for old and new
deployments coexisting, backfills, rollback limits, and reconciliation. Do not hide behavior changes
inside structural edits. Inspect concurrent changes and preserve work outside your responsibility.

Record an ADR for material decisions with real alternatives: context, choice, tradeoffs, consequences,
and a revisiting trigger. Prefer a short repository-native note over mandatory document scaffolding.

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
Use a visited set of modules and edges to terminate cycles while recording the cycle as a finding.
Bound traversal by named workflows and repository/host scope, not an arbitrary number of hops.
At external boundaries, inspect the local adapter and published contract; record unavailable remote
internals as a coverage boundary. Generated/vendor internals need no edits, but their integration
contracts still need checking. Do not equate excluded internals with verified behavior.

### Trace procedure
1. **Inventory:** List created/changed modules, their owner, public exports, runtime registration,
   callers, dependencies, configuration, and affected consumers. Include migrations and code generation.
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
7. **Resolve and retrace:** Fix confirmed bugs and missing behavior needed for the authorized outcome.
   Follow the repaired path again and verify affected consumers. Repeat until no new blocking gap
   appears in the scoped connected paths, or an explicit external blocker prevents further proof.

Use source search, call sites, imports/exports, route and handler registries, dependency injection,
schema references, tests, and available runtime evidence. Static reachability is not runtime proof.
Dynamic dispatch, reflection, plugins, generated code, and external consumers may need additional
registry, contract, or runtime evidence. Mark an unresolved edge as unverified; do not assume it works.

### Gap ledger and continuity
For a small change, keep a compact ledger in working notes and report relevant results. For a full
audit or substantial multi-module change, persist it in the repository's existing planning/audit
location; if none exists, use `docs/architecture/gap-trace.md`. Update the existing record instead of
creating competing reports. Do not put project-specific state into this global skill.

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

Prioritize by user impact, data correctness, security, and blast radius. Fix bugs and required gaps
within the task's authority; capture unrelated findings and optional features as proposed follow-ups.
Do not invent requirements from personal preference or silently turn a module trace into a new product.
Do not claim universal absence of gaps: report covered paths, concrete evidence, and remaining limits.
Report inventoried versus traced modules and checked versus unresolved edges separately from runtime
checks. Before claiming a full audit, account for every inventoried module and discovered in-scope
edge, including explicit exclusions and blockers. A full inventory with static-only paths is a full
static trace, not complete runtime verification. Stop retrying an unchanged blocker; preserve the
specific evidence and recovery action instead of repeating the same unsuccessful check.

## 12. Verify and finish

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

Report the resulting structure, important decisions and tradeoffs, checks performed, and remaining
limitations. For architecture reviews, give actionable findings with paths, impact, and the smallest
fix; do not manufacture findings or perform a redesign unless requested. Stop when the scoped
acceptance conditions are met. Do not promise that architecture alone guarantees performance or scale.
