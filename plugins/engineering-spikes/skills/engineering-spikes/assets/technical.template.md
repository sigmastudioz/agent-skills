# Spike title — Technical Doc

| Field | Value |
| --- | --- |
| Spike | Shared ID |
| Status / updated | Actual lifecycle state / date |
| Owner / decision maker | Named people or unassigned |
| Non-technical companion | Link |

## Decision frame

Record the decision, uncertainty, scope/non-goals, constraints, agreed timebox/resource bound,
current source revision and environment. Separate proposed assumptions from approved constraints.

| Question | Hypothesis | Exit criterion / disproof | Evidence needed |
| --- | --- | --- | --- |
| Q1 | Falsifiable expectation | Observable threshold | Source or bounded experiment |

## Current and proposed behavior

Trace the current entrypoint, dependencies, authoritative state and downstream consumers.
Describe proposed architecture, API contracts, data models and code only where relevant.
Identify affected authorization, compatibility, error/retry and operational paths. Explain omissions.
Label illustrative snippets and prototype limitations; do not imply proposed code is deployed.

## Options and trade-offs

| Option | Criteria met / failed / unknown | Dependencies | Effort / cost basis | Trade-off |
| --- | --- | --- | --- | --- |
| Real alternative | Hard constraints remain visible | Systems, access or prerequisites | Measurement or uncertain estimate | Why considered or rejected |

## Investigation and experiments

For each experiment record its ID, question, reproducible method/inputs/baseline, threshold defined
before execution, resource bound, and execution state (proposed, run, blocked or stopped).
Use a short per-experiment section when a table would become too wide.

Record actual commands/steps, results, negative findings, cleanup and artifact locations.
State dataset/workload coverage, synthetic inputs and any missing environment.

## Evidence ledger

| Evidence | Source / revision / date | Method and conditions | Observation | Coverage limit |
| --- | --- | --- | --- | --- |
| E1 | URL, supplied artifact or file/line at revision | Actual inspection or run | Supported fact | What this cannot establish |

Separate observation, interpretation and assumption. Reconcile contradictions explicitly.

## Requirement and gap trace

| Question / requirement | Option | Evidence | Finding / gap | Decision consequence |
| --- | --- | --- | --- | --- |
| Q1 / contract | Considered option | E1 or missing proof | Verified result or G1 | Supports, rejects or leaves unknown |

| Gap | Expected versus observed | Type / impact | Owner and next action | Closure check |
| --- | --- | --- | --- | --- |
| G1 | Cite the requirement and evidence | Defect, integration, feature, improvement or unverified | Assigned or unassigned | Specific proof needed |

Record disproved candidates and why; distinguish pre-existing behavior from a prototype regression.

## Outcome and confidence

State proceed, reject, further investigation or no decision; recommendation versus actual approval;
confidence and basis; unmet criteria, residual risks and the trigger for reopening the spike.

## Implementation and handoff

| Follow-up | Owner | Dependency / priority | Acceptance check |
| --- | --- | --- | --- |
| Specific production or investigation task | Named owner or unassigned | Actual prerequisite | Observable success |

Record prototype retention/disposal, production hardening, migration/rollback and operational work
where relevant. Include relevant security, privacy, performance and accessibility limitations.

## Verification and delivery

List checks actually run, failures/unavailable checks and the content revision they cover.
Link the stakeholder companion. Add diagrams only when useful, with captions and text fallbacks.
Record local rendering and target Confluence paste verification separately; replace all template guidance.
