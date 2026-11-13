---
name: domain-driven-design
description: Use when an agent plans, implements, fixes, refactors, reviews or delegates production code in applications, APIs, workers or monorepos, including architecture reviews and gap audits. Applies automatically on every such task without a trigger phrase. Not for prose-only work or edits to generated or vendor code.
---

# Principal Driven Domain Design
Regression tests: recorded baseline and with-skill pressure scenarios live in [tests/](tests/README.md).
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
Do not spawn agents merely because this section describes handoffs. An absent numeric cap is not
permission to delegate, and optional workflow skills cannot expand the user's limit. Do not assume
a child agent inherits the parent's conversation, loaded skills, or global instruction files; if the
child cannot read the skill, supply its relevant contents within the allowed context.

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

The marketplace skill contains guidance only. An optional handoff guard can be installed
separately by the host owner; do not download, install or enable it merely to use this skill.
When that guard is already installed, prefix the assignment with
`HANDOFF_JSON=` and a JSON object containing `goal`, `limits`, `workspace`, `revision`, `owns`,
`interfaces`, `state`, `evidence`, `next`, `return`, `trace`, `checks`, and `baseline`. `return` must
be an object with nonempty `paths`, `contracts`, `checks`, `gaps`, and `remaining` instructions.
`baseline` is this skill's accessible path. This applies to exploration and review assignments too,
and to sessions started through the desktop app's session tool, which the guard also intercepts.

Before delegating, resuming a handoff, or coordinating concurrent agents, read
[handoffs](references/handoffs.md) in full: delegation budgets and how the guard parses them, guard
behaviour, `isolation` declarations, shell-started workers, pattern-versus-component examples,
reporting back up the chain, concurrent work and file ownership, interruption and resume,
and installation discovery. For multi-stage batches, it also covers frozen input roles, stage-specific
acceptance, review disagreements, changing instructions and queue reconciliation. Those rules apply
with the same authority as this file.

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

## Find gaps, keep records, verify

Run a complete connected-path trace for every module created; for changed modules, retrace affected
paths and adjacent contracts. A file existing or compiling does not establish a working path, and an
edge not tested is an unverified path, not a passed one. When tracing created or changed modules, or
running any gap audit, read [gap tracing](references/gap-tracing.md) for the edge checks, the
recurring traps and the trace procedure, and follow them in full.

Record findings in the project's existing tracker or owning gap ledger; for a full audit or a
substantial change without a record, use one compact `.principal-ddd/gap-trace.md` discovered through
`.principal-ddd/index.md`. Classify each finding as bug, integration gap, required feature gap,
improvement opportunity or unverified path, and disprove candidates before recording them. Before
recording findings or resuming from a ledger, read
[gap ledger and continuity](references/gap-tracing.md#gap-ledger-and-continuity).

Create separate evidence files only when needed for deployment, rollback, an actual audit or an
active monitor; routine check results belong in the existing tracker. Before creating evidence
artifacts or archiving superseded evidence, read
[evidence retention and archival](references/gap-tracing.md#evidence-retention-and-archival).

Acceptance evidence must apply to the final relevant content and execution environment; reuse never
waives mandatory checks or turns partial or stale evidence into a pass. Before finishing substantial
work, reusing earlier check results or reporting completion, read
[verification](references/verification.md) and work through its completion checklist.
