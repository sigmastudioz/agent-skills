# Experiment packet

Use for a consequential experiment or reproducible handoff. Replace these field instructions with
actual content. Omit irrelevant fields with a reason; a small local check can remain a few lines.
Keep the packet in the owning task record or existing experiment artifact, not a parallel tracker.

## Proposed experiment

| Field | Supply |
| --- | --- |
| Identity and question | Stable experiment/claim IDs and the decision this check can change |
| Assumption and alternatives | Current explanation/mechanism, basis and viable comparator |
| Input identity | Actual fixture/data path and revision/hash, initial state, configuration and dependencies |
| Environment and authority | Where it runs, permitted actions, isolation and external boundaries |
| Resource and stop bounds | Time/workload/retry/cost limits relevant to this check; unchanged-blocker stop |
| Reproduction | Exact commands or steps with working directory and required non-secret configuration names |
| Supporting observation | Observable outcome required to support the claim within these conditions |
| Rejecting observation | Result that would reject the claim or force redesign |
| Dependent decisions | Conclusions to reopen if the assumption fails |
| Cleanup and retention | Owned temporary state/process cleanup and evidence consumer/lifetime |

## Actual execution

Complete only after execution. Otherwise mark this section not run.

Record actual source/input/environment identities, command/steps, observation time, measured results,
errors, evidence class and coverage limits. Link existing durable output where sufficient; do not
invent logs, token usage, performance values or production observations. State cleanup actually done.

## Decision update

State supported-in-conditions, contradicted or unresolved; explain why. Identify changed assumptions,
dependent conclusions retracted/reopened, chosen repair/design or next discriminating check, owner
and closure/stop condition. A negative result can be a successful experiment.
