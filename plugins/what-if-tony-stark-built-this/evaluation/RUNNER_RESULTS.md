# Comparison runner 2.1: utility trial

The user requested a reusable comparison tool, its build through Cursor, a self-review using the
Tony skill, and a test against models using normal tools. The [frozen protocol](RUNNER_PROTOCOL.md)
defines this trial. Earlier instruction-only findings remain in [1.1](RESULTS.md),
[1.2](TOOLS_RESULTS.md) and [2.0](INVENTION_RESULTS.md); their evidence is unchanged.

## What was supplied

Cursor Auto completed the isolated build in 502.738 seconds, with a working CLI, example, guide
and 15 passing tests. That is builder elapsed time, not the total authoring/review cost or ROI.
The [self-review](RUNNER_SELF_REVIEW.md) found seven failing counterexamples and corrected the
measurement, selection, import, failure and file-publication mechanisms. The pre-dispatch utility
and isolation gate passes 29 tests. This establishes functionality, not agent effectiveness.

The maintained tool runs all supplied exact correctness cases before ranking, then uses separate
fresh untraced timing and traced allocation processes. It applies qualification and tolerance rules,
records source identities and publishes a JSON report without replacing other work. Users still
supply inspected implementations, representative cases and correct expected answers. Python traced
allocation is not RSS; process isolation is not a sandbox; three samples are not significance.

## Matched tasks and treatment

One explicit model, grok-4.7-high; two fresh synthetic tasks; four processes, one attempt per cell,
maximum two active, 1200 seconds each. Fable's earlier unavailable cells stay pending, with no new
Fable call or account/spending change. The fixed Grok setting preserves the previous model choice.

- Lookup: three source variants, first-match compound identity semantics, duplicates/separators/
  zero/absent values, and two measured workloads. A fast candidate is incorrect.
- Decoder: three variants sharing a declared helper, ordered exact decoding, a full-domain cache,
  per-batch cache, short-lived import-plus-call lifecycle and a 512-KiB Python allocation limit.

Both arms get the same committed source, cases/configuration, task, README measurement contract,
shared DDD defaults and standard-library tools. Source inspection alone does not satisfy the task.
The control may construct any equivalent measurement harness. The treatment additionally receives
only the actual runner/worker scripts and 7,165-byte comparison guide. It gets no generic invention
instructions, previous answers, examples, coordinator calibration or scoring material. These are
utility/reporting tasks, not a claim that the tool improves arbitrary algorithm invention.

The actual tool's pre-dispatch calibration selects granite for lookup, excluding copper as incorrect;
it selects violet for decoding, excluding amber for Python allocation. Both baselines remain feasible.
These are source-variant comparisons, not gains caused by supplying the runner to a model. Calibration
stays outside worker checkouts. Runner/guide, fixtures, protocol and checks remain frozen after dispatch.

## Scoring and limits

Automated checks establish unchanged inputs, the expected recommendation and a contained JSON evidence
report. The frozen manual audit separately checks actual source/tool receipts: exactness, three fresh
untraced timing and separate allocation samples per feasible measured case, setup cost, qualification,
selection, provenance and executed measurements. Any equivalent report structure is accepted; no native
runner-schema, heading, prose or novelty bonus is awarded. A correct winner without valid measurement
evidence is not a completed measured recommendation. Process completion is also separate from partial
artifacts passing some checks. Timeouts remain censored and infrastructure errors remain unscored.

Primary observations are accepted measured recommendations and matched process wall times. Tool calls,
authored measurement code and provider counters are descriptive, not quality/cost scores. One-time
build/review effort is separate from per-task times. Shared host/service load and concurrent execution
limit timing conclusions. Three benchmark repetitions do not replicate the agent experiment: there
is one process per task/condition. Two narrow coordinator-authored tasks cannot establish statistical
significance, general productivity/invention gains or an independently designed study. Common host
metadata and hidden service context are not fully observable.

## Status

All four Grok processes completed within their original bounds. Every result passes unchanged-input,
correct-recommendation and evidence-presence checks plus all five frozen manual-audit requirements.
No agent retry or post-score runtime change was made. The original self-review and prior trial results
remain intact.

| Task | Normal standard-library tools | Supplied runner | Observed elapsed reduction |
| --- | --- | --- | --- |
| Decoder | Accepted; 724.832 s | Accepted; 337.938 s | 386.894 s (53.4%) |
| Lookup | Accepted; 746.451 s | Accepted; 137.799 s | 608.652 s (81.5%) |

These are model-process completion times, including reasoning, tool work, validation and final reply.
They are not the runtime of the chosen source variant. Both conditions select violet for decoding and
granite for lookup, reject the same invalid/over-cap alternatives, and deliver valid measurements.
There is no observed recommendation-correctness advantage. In these two prepared tasks, supplying
the runner reduced elapsed time while retaining the required evidence quality.

The sum of per-cell times is 1471.283 s for controls versus 475.737 s for treatments, a difference of
995.546 s (16.6 minutes). This sum is not the campaign's wall time: processes overlap. It excludes
one-time tool construction, review, workload/oracle design and adaptation costs. It is not a net ROI
or a forecast of future savings. The initial Cursor build alone took 502.738 s; all later authoring
and review effort was not measured as a separate clean cost.

## What accounts for the observed work

Controls built persistent custom harnesses: measure_decoder.py (39,453 bytes) and measure_lookup.py
(44,991 bytes). They implemented fresh subprocesses, strict output checks, timing/allocation separation,
qualification, hashes and report verification. The decoder control's first full measurement attempt
failed at report publication; it corrected its own writer and reran. The lookup control refined and
reran its harness/report too. These were internal task iterations, not new agent trials; their elapsed
cost and failed/debug executions remain visible in the original tool receipts.

Treatments reused the two supplied scripts and wrote only decision/evidence files on disk. They also
wrote postcheck and diagnostic shell snippets; reuse is not zero effort. Decoder treatment used 33
tool starts versus control 28; lookup used 26 versus control 40. Tool count alone does not explain
completion time and is not a productivity score. Native and custom harnesses both performed the actual
measurement contract. The observed reuse/debugging difference supports the intended mechanism, but
one sample per pair does not isolate every service, timing or reasoning factor.

## Audit details

All original cases, candidate source, dependencies, README/AGENTS instructions and supplied utilities
remain unchanged. All four HEAD revisions equal the original bases. Snapshots contain no symlinks.
All observed explicit edit/read paths are contained in their assigned checkout; own generated scratch
and Python cache cleanup affected only worker-created paths. No global skill, evaluator, network,
new dependency, extra agent or account change was observed. Each treatment read the focused guide
once and every control read it zero times. Hidden service context remains an observation boundary.

Manual audits independently recompute sample counts, medians, allocation peaks, source identities,
qualification and winner direction. Controls may use their own JSON schema. The decoder control's 48
raw worker records and lookup control's 36 raw samples support equivalent accepted recommendations;
custom source and actual command receipts establish fresh-process execution. The lookup control uses
a direct source compiler and a disclosed one-nanosecond numeric tie allowance; neither changes the
actual case outcome. The lookup treatment has an inverted ratio phrase in its final prose, while its
authoritative decision JSON and numeric table state the correct direction. This report uses the correct
numbers; no prose bonus or new acceptance rule was added.

All 237 repository tests pass in 146.806 seconds with native Blender access. The runtime and trial
code stayed unchanged after dispatch. Source-only evaluator/audit infrastructure and final docs/catalog
checks are distinct from proving an agent benefit.

## Interpretation boundary

This is the first recorded positive time observation for the skill's executable asset on its intended
prepared-comparison task. It does not show higher model intelligence, better generated algorithms,
general coding speed, significance, production performance or effects on other models. Manifests,
expected answers and representative workloads were already prepared; their creation and real-codebase
adapter effort are excluded. Controls used normal standard-library tools in fresh isolated sessions;
they did not carry an existing custom harness across tasks. A user with a reusable benchmark system
could have a smaller or absent advantage. Concurrent host/service load, unobservable common metadata
and two coordinator-authored tasks limit causal/general claims.

The [self-review record](RUNNER_SELF_REVIEW.md) explains what was fixed before freezing this trial.
The collection ledger links the restore-verified audit archive, including original Cursor build,
review failures/fixes, exact supplied assets/prompts, all outcomes and tool receipts. Raw service
thinking and private account/billing payloads are excluded. Fable's older blocked cells remain pending;
no new Fable experiment was run. No additional model calls or post-score tuning follow from this result.
