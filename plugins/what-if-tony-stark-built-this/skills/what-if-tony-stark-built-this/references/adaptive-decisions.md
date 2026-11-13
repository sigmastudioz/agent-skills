# Adaptive decisions and assumption changes

Use when several checks/designs compete or new evidence changes the plan. The six capabilities
are tools for the mission. Do not execute a full audit because a short task mentions this skill.

## Choose the next useful action

Identify the claim currently blocking the outcome, what is known, the smallest missing observation,
and a bounded action that can change the decision. Prefer existing evidence and project tools.
Explain impact, uncertainty removed and cost qualitatively; no invented information-gain score.

| Current situation | Useful route | Stop when |
| --- | --- | --- |
| Supported local defect, clear owner | Trace the affected input/consumer -> narrow repair -> relevant check | The supported behavior and relevant regressions pass |
| Several plausible causes | Rank explanations -> distinguishing observation -> update model | One cause is supported enough to repair or a named proof boundary remains |
| Reimagining a working system | Identify limiting assumption -> different mechanisms -> rejecting experiment | The requested design decision or first slice is supported |
| Unknown feasibility | Isolate decisive assumption -> bounded prototype -> compare with baseline | The assumption is supported/rejected within stated conditions or the bound ends |
| Release/change recheck | Identify changed proof inputs -> reopen dependent claims -> affected checks | Required scoped journeys are supported or precise blockers are reported |

These routes are examples, not new mandatory modes. Avoid elaborate artifacts when a sentence and
existing regression test carry the same evidence. A consequential experiment can use the
[packet template](../assets/experiment-packet.template.md); an obvious fix need not fill every field.

## Let evidence redirect the mechanism

For important assumptions, keep identity, basis, dependent decisions, rejecting observation and
current state: proposed, supported-in-conditions, contradicted or unresolved. This can be a compact
part of the existing task record. It is not a new database or an automatic watcher.

When evidence contradicts an assumption:

1. Record the actual observation and its method/environment; check that the experiment itself is valid.
2. Retract or qualify the conclusions that depend on it. Preserve unaffected evidence with its identity.
3. Revise the causal explanation and options; do not merely add retries or weaken acceptance criteria.
4. Pick the next discriminating check, a viable different mechanism, or a bounded stop with missing proof.

For example, timestamp-based conflict resolution depends on comparable clocks. Evidence of clock
drift invalidates that choice; increasing polling frequency does not restore the assumption. Compare
version-based reconciliation or another viable mechanism against the same user constraints.
New proposals still need compatibility, ownership, failure/recovery and authority checks.

Do not loop indefinitely. Stop when scoped acceptance is met, the experiment/resource bound ends,
or an unchanged blocker prevents useful progress. Ask only for a decision or authority actually
needed to continue. Revising a hypothesis does not authorize a new product or external action.
