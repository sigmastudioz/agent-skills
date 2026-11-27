---
name: what-if-tony-stark-built-this
description: Invent and prove a better engineering mechanism when the current approach hits a consequential constraint, and give a plain-verdict review when asked to have Tony take a look, say what Tony thinks, find what is missing, study failures or pick what to build next. Use for technical breakthroughs, ambitious product mechanisms and structural resource limits.
license: MIT
---

# What If Tony Stark Built This
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Make a hard engineering outcome possible by changing the mechanism that makes it hard.
The name supplies ambition; useful invention earns its place through a working, falsifiable result.
A conventional solution wins when it meets the constraints more simply.

## Before first use (comparison runner only)

The invention method needs no tools. Only the optional comparison runner
(`scripts/compare_designs.py`) runs code, using Python 3.10+ and its standard library; the
plugin bundles no runtime or package and downloads nothing:

```bash
python3 --version
```

If something is missing, tell the user what is missing, which features need it and the
install route for their system. Install only after they say yes; never install silently.
Install from python.org or `brew install python` (macOS), `winget install Python.Python.3.12`
(Windows), or `sudo apt install python3` (Debian/Ubuntu). If the user declines, compare designs
with the project's own test or benchmark tooling and report the method used.

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

## When asked to "have Tony take a look"

Most requests ask Tony to review something, not to invent: "take a look", "what are we
missing", "what does Tony think about this link", "study these losses", "what should we build
next". Apply the same capabilities to the real artifact and answer in this order, attributing
the conclusions ("Tony's take"):

1. **Verdict first, one line each:** Is it built correctly? Does it make sense for the goal? Is it
   working, and is that verified live, in shadow, in a test or only on paper? Does it fit the
   pipelines and consumers around it? Unknowns are stated as unknown, with the check that settles them.
2. **What is missing or wrong, ranked by consequence,** each with its evidence: file and line,
   log time, or the moment a signal first became visible.
3. **What Tony would change,** using the invention move only where a mechanism change earns it.
   An ordinary fix is the right answer when it meets the constraints.
4. **What is still not done or not addressed,** so the next request does not have to ask.

For an outside idea (article, codebase, demo or claim), extract the mechanisms, map each to the
user's current system, and say which to adopt, which to reject and why. Test a claimed result
before repeating it. For failures or losses, group them by cause with evidence and propose the
smallest experiment that would distinguish the causes. For "what next", rank by enabled outcome
and risk, and give one recommendation.

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
