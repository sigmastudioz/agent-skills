# Bundled handoff contract

A versioned adaptation of the Principal Driven Domain Design 1.4.5 handoff rules,
by Lex from SigmaStudioz, distributed under this plugin's MIT license. This file is
part of the installed skill. It supplies the handoff contract without fetching instructions
from a website or requiring another plugin to be installed.

## Authorization and limits

Delegate only when the user or applicable host instructions already authorize it. An absent
numeric cap does not authorize extra agents. Count each new exploration, implementation
and review agent against the cumulative authorized budget; resuming an existing agent does
not allocate a new slot. Changing stages or repeating a cap does not reset usage. Preserve
explicit roles, concurrency limits and retry budgets. This guidance cannot enable disabled
tools, grant permissions or authorize publishing, deployment or destructive actions.

Honor the host's instruction hierarchy. Do not assume a child inherits the conversation,
loaded skills or local instruction files. Provide accessible baseline paths and relevant
contents when the receiving actor cannot read them. A brief is a proposal; check its
algorithms against the original contract rather than treating flawed pseudocode as authority.

## Handoff contract

Every authorized agent assignment, resumable handoff or brief another person acts on includes:

| Field | Required context |
| --- | --- |
| Goal and limits | User outcome, acceptance checks, authorized actions and exclusions |
| Location | Accessible workspace, actual branch/worktree or revision, instruction and baseline paths |
| Ownership | Exact owned files/modules, other active owners and shared interfaces |
| Architecture | Domain owner, public entrypoints, contracts, callers and consumers |
| Current state | Implemented and pending work, local edits, decisions, failing checks and their cause |
| Evidence | Exact commands/options and results, checked content identity, trace records and unavailable environments |
| Next action | Concrete next step, blockers, required inputs and expected return format |

When an existing host handoff guard requires it, prefix the assignment with `HANDOFF_JSON=`
and an object with `goal`, `limits`, `workspace`, `revision`, `owns`, `interfaces`, `state`,
`evidence`, `next`, `return`, `trace`, `checks` and `baseline`. `return` is an object with
nonempty `paths`, `contracts`, `checks`, `gaps` and `remaining` instructions. All fields carry
meaningful context; `workspace` and `baseline` are accessible paths on the receiving host.
If the workspace differs from the launch checkout, verify its authority and include the
host's required isolation declaration: `confirmed: true`, matching absolute `workspace`
and a nonblank `reason`. A declaration alone grants no authority. Correct a rejected brief
before retrying. This package supplies no guard or executable helper.

## Examples: pattern or component

For each cited code example, label it a pattern to copy or a component to reuse and state
the invariant it must preserve. A path alone does not establish an authorized write model.
For each runtime or library claim, provide the actual command, options and observed output;
source inspection, a recommendation and a completed runtime check establish different things.

## Shell workers and isolation

A host guard on agent/session tools may not intercept a CLI started from a shell. Enforce
the same brief and authorization contract there. Keep the authoritative brief, progress log,
job state and accepted report outside the worker's writable scope; supply a readable input
copy and named return channel. If write-capable workers would share uncommitted work, use
an authorized isolated worktree from a committed base containing the inputs. A read-only
review may use an isolated input packet. Share only the data/tools that actor is authorized
to use. Never put credentials or private runtime payloads in handoff notes. If dependency
folders are linked, forbid installs. Prefer sandboxed modes; run-everything flags require
explicit user approval and may still be refused by the host.

## Reporting back up the chain

Require progress per named milestone, `BLOCKED | question` for decisions the actor cannot
make, a final report and `DONE`. Use the host's event/monitor facility when available.
Forward each blocked question promptly to its decision owner. Review the final diff and
run the relevant checks before relaying results to the user and whoever delegated the task.
Separate the worker's claims from your checks and identify unresolved paths.

## Batches, concurrent ownership and resuming

Keep stable item identities, pinned input revisions, assigned actors, stages, holds and
cumulative attempts in the existing task queue. Before launch, verify actual input roles,
reference identities, permitted actions and expected output. Freeze launched input packets.
A prepared packet is not a running actor. Count running, completed, failed and pending work
from item identities, not report rows. Keep reviewed, accepted, persisted and consumer-verified
states separate. A timeout or unopened input is unresolved, not a pass.

Collect all assigned reviews before spending a limited correction and reconcile concrete
findings against original evidence. Disagreement needs checking, not majority voting. Recover
an existing valid report from formatting/path-label mismatches when its inputs are verified.
When the user's requirements change, record the controlling revision and mark affected work
superseded or pending before integration; preserve unaffected work and earlier failures.

Agree public contracts and exactly owned files before concurrent writes. Tell workers they
are not alone and must preserve others' edits. Reconcile isolated changes before claiming
integration, including adjacent consumers and failure paths. After interruption, save the
handoff in the existing owning record with timestamp/content identity; on resume inspect the
checkout and current diff, and revalidate stale assumptions. Local installation establishes
nothing about remote/cloud discovery; confirm paths and configuration on every actual host.

## Maintainer provenance

Derived from the DDD 1.4.5 entrypoint contract and handoffs reference at collection commit
`583d79b65807e30b0f6f133a249446ab3aba6b89`. Source reference SHA-256:
`f50902af7c9c5613d0cd579328959b776e416fd201db5f3f2d6a01f714bcb1b6`.
Refresh this bundled contract deliberately in a versioned release when its maintained source
changes. Source attribution is provenance, not an instruction to download remote rules.
