# Counterexamples and experiments

Choose experiments that can change a decision. Start from a supported promise and its failure
condition, not a universal checklist or an urge to build a simulator.

## Plan a discriminating check

Before executing, state the claim, competing explanation/design, counterexample, inputs and initial
state, observable expected result, baseline, environment, resource bound and cleanup. Set thresholds
before observing results, using the actual requirement. A proposed budget is not permission to spend.
For ambiguous debugging, prefer a check where leading explanations predict different observations.
Record actual commands/steps and results afterward; keep planned and performed work distinguishable.

Pick relevant stressors from the actual path:

| Boundary | Useful counterexample |
| --- | --- |
| Async state | An older success arrives after cancellation, refund or deletion |
| Delivery | A message is duplicated, reordered, delayed or processed after restart |
| Partial work | An effect commits before acknowledgment, or one write succeeds before another fails |
| Authority | A legitimate user requests another tenant's object; a client supplies a forged authority field |
| Dependency | A response is valid in shape but stale, incomplete, rate-limited or timed out |
| Concurrency | Two supported writers observe the same old state and both attempt an effect |
| Migration | Old rows, old clients and new writers coexist during interruption or rollback |
| Performance | Representative skew, payload sizes, cold/warm caches or contention change the bottleneck |
| Cadence | Work crosses the next anchored schedule, a retry overlaps, or a calendar boundary occurs |
| AI/tool loop | A plausible wrong answer, untrusted retrieved instruction, malformed tool input or tool failure |
| Device/control | Sensor delay or loss, actuator acknowledgment loss, restart or bounded simulator divergence |

Preserve declared timing, authority and business semantics; a test must not "fix" an inconvenient
contract by weakening it. Make adversarial data synthetic and isolated. Inspect commands for real
endpoints and side effects before executing an existing harness; its test name is not containment.

## Explore futures without inventing observations

Use the cheapest adequate method: source contradiction, tabletop state sequence, existing test,
fake adapter, deterministic replay, isolated integration, then authorized target-environment check.
Advance only when stronger evidence is needed and permitted. Missing live access can leave a useful
bounded result. Do not silently treat a fake as a real-adapter check.

When comparing futures, change named variables and expose shared assumptions. Separate schedule
exploration from stochastic samples; a seed makes a sample reproducible, not exhaustive. Use
controlled interleavings/barriers for races where possible instead of hoping sleeps trigger them.
Capture the minimal sequence/input that falsifies the claim, then narrow it to the responsible edge.
Disprove the candidate with alternative valid paths and baseline behavior before recording a defect.

For performance/cost, use equivalent workload and conditions, verify correctness, and report actual
units, repetitions, distribution and known variability. A synthetic speedup proves only that case;
estimates and extrapolations stay labeled. No invented p95, savings, scale or uptime claims.

For a consequential repair/design comparison, hold acceptance criteria and workloads constant.
Avoid selecting a winner that only improved a proxy while the terminal user outcome regressed.
Keep failed candidates and why they failed; stop exploring when further alternatives cannot change
the scoped decision enough to justify their cost.

## Completion and cleanup

Respect existing bounds. If none exist, select a small local reversible check when sufficient;
ask only for a missing limit or permission that actually blocks the needed experiment. Do not infer
authority for production fault injection, hardware actuation, disruptive load, deployment or spending.
An unchanged blocker is a reason to preserve the missing proof and move to independent work.

Restore isolated state, stop owned temporary processes and remove test credentials/artifacts according
to project rules. Do not delete a shared resource or another writer's evidence. Retain only evidence
with an actual consumer/retention need. Report the method, result, what it disproved or supported,
remaining uncertainty and the next check. Never label a tabletop exercise a performed simulation.
