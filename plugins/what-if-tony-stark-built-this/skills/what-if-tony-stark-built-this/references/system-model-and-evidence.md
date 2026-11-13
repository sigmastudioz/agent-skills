# System model and evidence

Use an existing architecture map or tracker when adequate. For a small task, a few linked sentences
are enough. For complex work, keep the following logical records together in the owning task/ledger;
they are not a mandate for new files or a graph database. If no record exists or record writes are
outside scope, deliver the compact record in the response as not persisted. A later invocation needs
that response or another supplied record; do not imply memory that the host has not retained.

## Model the promise and the mechanism

Give important claims stable IDs. Connect each claim to the accepted requirement, actual entry,
owner, state transitions, effects, terminal consumer, failure/recovery branches and closure check.
Trace significant components backward to the promise or constraint they serve. Unexplained purpose
is a candidate for investigation, not permission to delete compatibility or recovery code.

For a new concept, show proposed components and interactions explicitly as proposed. Record which
assumptions need a prototype or user evidence. Do not fabricate existing paths for an unbuilt idea.

An optional compact representation:

| Claim / requirement | Entry -> owner -> state/effects -> terminal consumer | Evidence IDs / limits | Status / next check |
| --- | --- | --- | --- |
| C1: accepted export becomes a usable download | Actual symbols, contracts and artifact path | Existing evidence with source identity | Observed, static-only, contradicted or unknown; specific next check |

Treat edges as contracts. Check real caller reachability, producer/consumer payload agreement in
both directions, registration/build inclusion, absent values/defaults, persisted compatibility,
authorization, cadence where applicable and concurrent ownership. Trace indirect/asynchronous
consumers. Follow a changed rule through every relevant reader and writer, including cleanup.
Use a visited set for cycles; inspect harmful dependency cycles without treating all runtime loops
as defects. Bound traversal by the named workflow and actual repository/host scope.

At external boundaries, inspect the local adapter and available published contract. Name unknown
remote internals. Dynamic dispatch and generated registries need their actual wiring inspected;
an import search alone cannot establish absence. A supported standalone command is a real entrypoint.

## Keep causal predictions honest

Distinguish observed causality, a connection supported by source, and a hypothesized consequence.
For impact, follow a failure to reachable consumers and identify conditions that enable propagation.
Track authority, timing, idempotency and recovery across the path. A broad dependency fan-out is not
proof that every consumer fails; local fallback or reconciliation may stop the consequence.

For example, "storage is unavailable -> export request succeeds -> queued job retries -> UI reports
complete" is a hypothesis until the worker and UI behavior support those links. A delayed result,
a lost result and a misleading success state are distinct findings with different repairs.

## Evidence with identity and limits

For each consequential evidence item retain:

- Claim/finding ID, actual source path/symbol or artifact, revision/content hash and environment.
- Method, inputs, configuration, relevant dependency versions and actual observation/result.
- Evidence class: source inspection, tabletop prediction, mock/contract test, isolated execution,
  real-adapter check or target-environment observation.
- Coverage boundary, missing conditions, freshness assumptions and the check that would close it.

Do not convert a prediction to an experiment result or static reachability to runtime success.
Use observed/not observed/contradicted/unknown or equivalent explanatory states, not an unsupported
confidence percentage. One strong failure cannot be averaged away by unrelated passing checks.

Before recording a finding, search for alternative supported paths, documented tradeoffs and real
callers. Compare baseline behavior before attributing the defect to a change. Preserve disproved
candidates with the decisive evidence, and classify latent hazards separately from reachable defects.
Each surviving finding needs impact, owner or owner-unassigned, the smallest action and closure check.

## Recheck and continuity

On resume, compare claim inputs: code, schemas, configuration, dependencies, generated artifacts,
runtime registration and environment. Reopen the claims whose supporting assumptions changed,
plus dependent claims; use the model to bound the affected set. Check negative dependencies too:
a new caller or route can invalidate an earlier "unreachable" conclusion. Unknown impact means
unverified evidence until resolved, not permission to reuse it as a pass.

Retain prior evidence as historical with its original identity; a new date does not refresh a run.
Do not rerun unaffected checks without a requirement or concrete reason. Keep project evidence in
its existing owning record and respect privacy/retention; no secrets or raw private payloads belong
in the reusable skill. Rechecking happens when invoked; this package installs no watcher.

Report inventoried versus traced modules and resolved versus unknown edges separately from runtime
checks. A full static trace may still have runtime unknowns. Never claim a whole-system audit from
sampled paths or equate an excluded boundary with a verified one.
