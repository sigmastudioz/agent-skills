# What If Tony Stark Built This

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version 2.1.0.

Engineering invention for a consequential constraint: challenge the inherited approach, find a
better mechanism, and prove a working slice. The name supplies ambition; a useful breakthrough
must earn its place through exact behavior, real constraints and a connected consumer.

## When to use it

Use it when the existing approach makes the desired outcome too expensive, fragile or impractical,
when an ambitious product idea needs a credible mechanism, or when you explicitly want a different
engineering approach. It asks what work can disappear, which representation changes the problem,
and whether information or authority already present elsewhere can supply the answer.

Routine coding, straightforward fixes and ordinary reviews stay with the existing engineering
workflow. Explicit invocation on simple work can conclude that a conventional solution is best.
The skill does not manufacture novelty or require a new platform, service or extra agent.

## Six supporting capabilities

| Capability | What it contributes to invention |
| --- | --- |
| System Map | Locate the limiting work and the consumer that actually needs its result |
| Gap Radar | Expose the assumption separating the outcome from the present mechanism |
| Failure Lab | Reject an attractive idea with the smallest decisive experiment |
| Impact Trace | Account for correctness, costs and complexity moved elsewhere |
| Repair Loop | Connect the surviving mechanism to usable behavior |
| Evidence Memory | Retain attempted mechanisms, failed assumptions and input-bound proof |

These are tools selected by need, not six required stages or documents. The implementation goal
is an early working slice. Further investigation should answer a decision that can change it.

## Invocation and installation

Once installed, ask naturally or explicitly invoke the portable identifier:

```text
Use $what-if-tony-stark-built-this to rethink the mechanism behind this resource bottleneck.
Use $what-if-tony-stark-built-this to invent a credible first slice of this product idea. Propose only.
Use $what-if-tony-stark-built-this to build and test a better approach within these constraints.
```

The display name remains **What If Tony Stark Built This**. Normal host discovery is enabled, with
narrowed relevance in version 2. Host selection behavior is not guaranteed by package validation.
After this addition is published at the selected repository revision:

```sh
npx skills add sigmastudioz/agent-skills --skill what-if-tony-stark-built-this
```

For Claude Code at a published revision:

```text
/plugin install what-if-tony-stark-built-this --marketplace sigmastudioz/agent-skills
```

Claude, Cursor and Codex manifests are included; host catalogs live at the collection root. Local
availability is separate from publication, marketplace approval and remote installation.

## Scope and resources

Load the short [entrypoint](skills/what-if-tony-stark-built-this/SKILL.md) and relevant
[invention methods](skills/what-if-tony-stark-built-this/references/invention-methods.md).
Other references load only for a consequential uncertainty: [experiments](skills/what-if-tony-stark-built-this/references/counterexamples-and-experiments.md),
[assumption changes](skills/what-if-tony-stark-built-this/references/adaptive-decisions.md),
[evidence](skills/what-if-tony-stark-built-this/references/system-model-and-evidence.md),
[adoption/recovery](skills/what-if-tony-stark-built-this/references/repair-and-delivery.md), and
[workflow composition](skills/what-if-tony-stark-built-this/references/tech-entry-points.md).
The old [coding support link](skills/what-if-tony-stark-built-this/references/coding-loop.md) is retained
as an adoption note. It is no longer a default general coding workflow.

Proposal/review requests retain their read/write/execute limits. Novelty grants no extra authority,
deployment, spending or delegation. Existing project tools and specialists are optional. No required
paid dependency, account integration, persistent graph service, background watcher or telemetry is
introduced. Project learning belongs in the owning project record; memory and monitoring depend on
the host. The name does not request character roleplay or imply fictional capabilities.

## Working comparison tool

Version 2.1 adds a local [comparison runner](skills/what-if-tony-stark-built-this/references/comparison-runner.md):

```sh
python3 plugins/what-if-tony-stark-built-this/skills/what-if-tony-stark-built-this/scripts/compare_designs.py experiment.json --output report.json
```

It validates exact outputs before ranking, uses fresh processes, measures untraced import/setup-plus-call
latency separately from Python allocation, applies memory limits and conservative tie rules, and records
source identities and failure reasons. Reports are published without overwriting existing work. A
[runnable example](skills/what-if-tony-stark-built-this/assets/comparison-example/README.md) is included.
Python 3.10+ is required for this optional tool; it has no third-party dependency or model/API call.
Execute inspected authorized local code only. Process isolation is for measurement, not a security
sandbox; Python allocations are not RSS and the result covers supplied cases on the recorded host.
The tool leaves candidate generation and case/workload design to the user or existing workflow.

The [self-review](evaluation/RUNNER_SELF_REVIEW.md) records actual counterexamples and fixes after the
Cursor build. A new matched trial tests whether supplying the tool helps versus normal standard-library
tools; local variant speedup by itself is not evidence that the skill helps an agent.

## Evidence and evaluation

The first two trials found little added general-coding value, including guided Grok timeouts.
Those results motivated the narrower purpose; they remain historical evidence:

- [1.1 no-tool pilot](evaluation/RESULTS.md)
- [1.2 tools-enabled coding comparison](evaluation/TOOLS_RESULTS.md)
- [2.0 frozen engineering-invention protocol](evaluation/INVENTION_PROTOCOL.md)
- [2.0 engineering-invention trial record](evaluation/INVENTION_RESULTS.md)
- [Runner utility trial protocol](evaluation/RUNNER_PROTOCOL.md)
- [Runner utility trial results](evaluation/RUNNER_RESULTS.md)
- [Coding tasks with setup included: frozen protocol](evaluation/CODING_PROTOCOL.md)
- [Coding tasks with setup included: results and limits](evaluation/CODING_RESULTS.md)
- [Portable authored behavioral cases](skills/what-if-tony-stark-built-this/tests/README.md)

The optional standard-library Python evaluation tools live outside the runtime skill. Live trials
require Git and an authenticated Cursor `agent` CLI with the selected models; ordinary skill use
requires neither. The invention trial supplies only the new entrypoint and invention-methods file.
Hidden checks, previous outputs and all other skill resources stay outside worker checkouts.
Package and catalog validation proves wiring, not model efficacy. Synthetic task success does not
establish production behavior, universal invention ability or compatibility with every host.
The maintained-code trial includes model-authored workload and comparison setup in task time.
It found a faster sequencer with longer development time and incomplete filesystem provenance in
both catalog comparisons; it does not establish an overall completed-task time saving.
Collection acceptance and retained evidence are linked from `.principal-ddd/gap-trace.md` outside this
standalone plugin. No trial result is replaced by a newer version's claims.
