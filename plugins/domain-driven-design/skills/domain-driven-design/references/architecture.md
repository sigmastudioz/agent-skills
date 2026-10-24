# Architecture guidance

Read the matching sections when the change touches these decisions. Shared authorization,
trace, evidence-retention and verification requirements remain in [SKILL.md](../SKILL.md).

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

### Repository ownership and operational artifacts

Establish actual repository roots, package ownership and release units; adjacent folders and a
common parent checkout do not make independent repositories one monorepo. A task spanning UI,
API and worker repositories must preserve each owner's source, tests, deployment/rollback tools,
source snapshots, patches, build artifacts, receipts and archives in that owning repository.
Do not put API/worker implementation or evidence in a UI repository, or UI implementation or
evidence in an API repository, merely because that is the agent's current working directory.
A verification folder, temporary label or build exclusion does not waive repository ownership.

- Use `.principal-ddd/index.md` as the DDD record map when present; established owner trackers
  and evidence/archive conventions keep their authority. Link related records with
  repository identity, revision and source/artifact checksums rather than duplicating bodies.
- Cross-repository coordination uses an established operations owner or a concise manifest linking
  the owner-local operators and receipts. Do not invent a coordination repository or copy another
  repository's operator to make the release self-contained. Explicitly authorized repository
  consolidations or ownership transfers require the same compatibility and recovery checks as a move.
- Consume another application through its public API or a separately owned, compatible package or
  generated client/schema. Do not import a sibling checkout's private implementation at runtime.
  Existing cross-repository contract tests may read public contracts when that development dependency
  is explicit and available in CI; this does not permit copying another application's internals.
- Classify by responsibility and execution target. UI-owned rendering, server components, session
  proxies and web release tools can legitimately run on a server. They must stay thin where the API
  owns business behavior; a server-only directive does not transfer that behavior to the UI owner.
- Treat source snapshots as inert evidence. Keep them outside runtime, compiler, test-discovery,
  lint and packaging inputs unless a dedicated evidence check explicitly owns them. Prefer an
  existing immutable source/artifact reference when it meets recovery or audit requirements.
  Verify effective inputs and transitive imports: compiler exclusions alone do not block imports,
  and placement outside a source directory alone does not prove exclusion from release artifacts.
- Trace browser imports separately from repository placement. Account for runtime imports,
  re-exports, dynamic loading, aliases and actual build inputs; distinguish erased type imports,
  Node-only tests and UI-owned server entrypoints. Report a misplaced snapshot separately from a
  confirmed browser dependency or shipped artifact; do not infer one from the other.

For existing misplaced operational files, trace all readers/writers, imported helpers, relative
paths, active monitors, release manifests, rollback/restore consumers and concurrent owners before
a move. If migration is authorized, update and verify affected references together, retain exact
content identities and recovery access, and use inert local checks rather than triggering a release.
Keep active or uncertain paths intact until their consumers can migrate safely; record the ownership
gap and next action. An ownership finding or skill update alone does not authorize cleanup,
deployment, deleting recovery evidence, changing risk limits or altering production behavior.
Reuse existing lint/build/import and artifact checks for touched boundaries; enforce both repository
ownership and execution-target isolation rather than hiding misplaced files with exclusions.

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

Record material decisions with real alternatives in the existing ADR, decision log or tracker:
context, choice, tradeoffs, consequences and a revisiting trigger. Create a separate ADR only when
required by the task or repository's maintained architecture documentation. Prefer updating the
owning record and link it from the tracker; do not create parallel verification reports.

