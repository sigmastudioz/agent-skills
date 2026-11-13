---
name: what-if-tony-stark-built-this
description: Invent and prove a better engineering mechanism when the current approach hits a consequential constraint. Use for technical breakthroughs, ambitious product mechanisms, architecture alternatives, and performance or resource limits that call for rethinking the approach. Also use when explicitly asked what if Tony Stark built this. Routine fixes and ordinary implementation use the existing engineering workflow; excludes character trivia and roleplay.
license: MIT
---

# What If Tony Stark Built This
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Make a hard engineering outcome possible by changing the mechanism that makes it hard.
The name supplies ambition; useful invention earns its place through a working, falsifiable result.
A conventional solution wins when it meets the constraints more simply.

## The invention move

Express the user outcome without today's component names. Separate hard requirements from the
inherited approach. Locate the assumption responsible for the expensive, impossible or fragile work.
Ask what could remove that work, change its representation, or answer the question elsewhere using
information the system already possesses. Read [invention methods](references/invention-methods.md)
for this search and proof; do not load the rest of the library by default.

Choose a materially different mechanism only when you can explain what it eliminates or enables.
For authorized builds, implement the smallest executable version of the decisive mechanism early.
Let its result decide whether to integrate, revise or reject it. Once the constraint is understood,
more inventory or reproductions should answer a new decision; otherwise move to implementation.
If the resource budget is tight, prioritize a working vertical slice over a broad investigation.

## Six capabilities behind the invention

| Capability | Contribution |
| --- | --- |
| System Map | Find where the limiting work originates and which consumer needs its result |
| Gap Radar | Expose the assumption separating the desired outcome from the existing mechanism |
| Failure Lab | Run the smallest experiment that could reject the proposed leap |
| Impact Trace | Account for costs, correctness and complexity moved across a boundary |
| Repair Loop | Turn the surviving mechanism into a connected, usable implementation |
| Evidence Memory | Preserve what was tried, what failed and which inputs support the conclusion |

Select these as needed. They are not six phases, reports, or a brainstorming quota.
Existing engineering skills own ordinary implementation, ownership and verification discipline;
do not repeat their checklists or build a second workflow around them.

## Scope and delivery

Keep the user's hard constraints, authority boundaries and public behavior outside the requested
change. Novelty never justifies approximation, hidden extra work, invalidation debt or unsupported
infrastructure. Proposal/review requests stay within their read/write/execute scope. Invocation adds
no deployment, spending, account, destructive-action or delegation authority.

When an invention crosses a consequential boundary, load only the needed supporting reference:
[experiments](references/counterexamples-and-experiments.md),
[changed assumptions](references/adaptive-decisions.md),
[system evidence](references/system-model-and-evidence.md), or
[adoption and recovery](references/repair-and-delivery.md).
[Tech entry points](references/tech-entry-points.md) explain composition with existing workflows.

When comparing two or more inspected local implementations on the same acceptance
workload, use the Manifest v1 [comparison runner](references/comparison-runner.md)
(`scripts/compare_designs.py`) and keep its report with the experiment evidence. Do not
treat medians or a winner label as statistical proof or product efficacy.

Lead the result with the enabled outcome, the assumption changed and the mechanism. Give actual
checks against the constraints, the connected consumer and the remaining limits. Keep speculative
ideas separate from executed work. A shorter implementation, an ordinary method, or a rejected idea
can be the right result; do not manufacture breakthroughs or claim efficacy from a plausible design.
Use the existing project record for reusable evidence; optional substantial experiments can use the
[packet](assets/experiment-packet.template.md). Do not imply persistent memory or monitoring.

Maintainers only: [evaluation requests and scoring criteria](tests/README.md).
Do not load these criteria during ordinary skill use or as an agent under evaluation.
