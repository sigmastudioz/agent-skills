# Tool-enabled coding trial: no Stark guidance versus relevant guidance

## Diagnosis of the first pilot

Observed limits: both coding tasks reached full correctness in both arms; the ticket prompts already
enumerated most of the important cases; no tools were permitted; all runtime references were supplied
inline, adding 43,882 bytes per prompt. The first pilot therefore could not measure whether the skill
improves repository exploration, counterexample construction, iterative repair or consumer verification.
These are plausible explanations, not an identified causal decomposition. This new trial changes
task difficulty, tool access and guidance size together; historical score differences cannot isolate
which change matters. The within-trial comparison estimates the added selected guidance only.

## Frozen comparison

Two fresh synthetic multi-module Python repositories, two explicit models (`grok-4.7-high` and
`claude-fable-5-2-high`), two conditions: eight fresh model processes, one per cell, maximum three
active. No corrective reruns or additional agents. Each call has the same fixed 1,200-second limit.
The source fixtures, ticket/contracts, public tests and hidden checker are fixed before dispatch.
Task order and within-pair condition order are counterbalanced. This remains one observation per cell.

Each run gets an independent writable Git checkout cloned from that task's committed synthetic base.
Both arms share the identical base revision, ticket, common engineering defaults, tool policy and
output request. The baseline gets no explicit Stark guidance. The treatment gets only the maintained
`references/coding-loop.md`, with its exact source hash recorded; no complete skill body, invention
references, templates, historical results or evaluator files are supplied. Selection is fixed for
both coding tasks, not tailored to a hidden failing case. Global metadata/settings may remain common
on the Cursor host; this is not a guarantee of a pristine model with no installed-skill metadata.

Models may inspect/edit their own package and add local tests, execute Python standard-library checks
and use read-only Git inspection. No outside-workspace file reads, dependency installs, network
research, extra agents, commits, deployment or publication are authorized. Existing test expectations
and the README contracts are authoritative. The synthetic benchmark roots contain no credentials,
production data or remote service endpoints. Cursor is run with sandboxing and automatic review of
safe tool calls, without run-everything/permission-bypass flags. A tool permission/infrastructure
failure is reported separately from implementation correctness.

## What is scored

Primary outcome: the final implementation passes all original public tests and hidden task checks,
with no critical scope/test-tampering/leakage issue. Secondary: number of distinct behavioral checks
passed, actual tool activity, added regression artifacts and base-fail/patch-pass proof when present.
The checker uses distinct test methods, so failing subtests do not double-count a single case.

Hidden tests stay outside every worker checkout. The coordinator snapshots the final package into
a separate grading directory and uses frozen public tests and the hidden checker, never worker-edited
expectations. Inspect patches for off-task effects before local execution under the host sandbox.
The relay suite checks 15 cases; the importer suite checks 18. Contracts in fixture READMEs define
their expected behavior; hidden tests add no secret product requirements. Failures, timeouts and
partial work stay visible. A partial implementation is not silently discarded or retried.

Retain exact base/source/guidance hashes, prompts, streamed event audit, final file snapshots/diffs,
actual check results, process outcomes, wall times and raw provider usage counters. Count provider
tool starts where identifiable; do not confuse paired started/completed events with two calls.
Audit explicit paths/commands for outside reads, global target-skill loading or hidden-check leakage;
record any uncertainty. Extra service-side metadata may be outside the visible trace.

Report per-model/task matched outcomes and critical failures separately. Code tests are objective
against the frozen checker; the coordinator is still the task/skill author, not an independent judge.
Wall time/counters are descriptive under shared service and concurrent execution. No significance,
pricing, universal efficacy or production-readiness claim follows from eight synthetic runs.

Do not modify the runtime guide, task source, checker or acceptance thresholds after dispatch and
claim a rerun independent. Retain the old pilot and negative/null outcomes. Any change inspired by
this trial requires a new version and fresh tasks for later evidence.

## Ownership and retention

The skill plugin owns the synthetic fixtures, maintained checker and trial runner. The collection
gap record owns decisions and links the evidence bundle. This explicit user-requested behavioral
audit justifies retained prompts, snapshots, results and event receipts. Raw service thinking
payloads are not delivered. Preserve evidence until superseded by a reviewed trial with no active
consumer needing the original; then use the collection's existing archival convention.
