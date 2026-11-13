# Comparison runner utility: frozen matched trial

## Intervention and scope

The user requested a working runner built through Cursor, a self-review using the Tony skill, and
an empirical comparison with normal model tools. Cursor Auto built a standalone standard-library
Manifest v1 runner, docs, example and 15 passing tests in 502.738 seconds. Self-review then produced
seven failing counterexamples and fixes, including untraced timing separate from allocation passes,
tolerance-based candidate ties, helper imports, exclusive report publication and failure handling.
The maintained runtime is frozen only after that review and appropriate checks. Builder elapsed time
is a separate one-time cost; per-task savings do not include all authoring/review costs or prove ROI.

This trial tests the reusable runner and focused usage reference, not a large instruction bundle or
an agent's ability to invent a new algorithm. The supplied variants already exist. Both conditions
have the same decision, correctness, resource and evidence requirements in their README. The control
may create any standard-library measurement code; it is not denied subprocess, time or tracemalloc.
The treatment additionally receives the actual maintained runner/worker scripts and comparison guide,
copied byte-for-byte into its isolated checkout. No other skill text, templates, examples, prior
results, coordinator calibration or grading material is supplied. Common relevant DDD defaults remain.

## Fresh tasks and matched execution

- Lookup API: first-match composite identity with separators, duplicates, zero and absent values;
  two representative measured workloads. One candidate is fast but incorrect.
- Decoder: exact ordered results from the shared declared helper; import/setup plus one batch is the
  actual job lifecycle. A full-domain cache must account for setup cost and Python allocation, while
  a per-batch cache is an alternative. These are synthetic comparison tasks, not a broad coding suite.

Explicit model: grok-4.7-high, same setting as previous trials. Fable's earlier blocked cells remain
pending; no new Fable call or account/spend change is made. Four fresh Grok processes, two tasks x
control/treatment, one attempt each, max two active, 1200 seconds per process. Independent clones
share their task's committed base, ticket, cases, source, memory/time/tie settings and output contract.
Condition order is counterbalanced. No corrective model reruns or acceptance changes after dispatch.
Cursor sandboxing and safe-tool auto-review are enabled, with no permission bypass.

Only new measurement scripts/reports/decision.json and an optional note are worker-owned. Supplied
source, cases, contracts, instructions and utility files are readonly. Standard-library tools,
read-only Git and own generated scratch/tool output are permitted. No outside inputs/global skills,
network, installs, extra agents, background jobs, broad process kills, commits or publication.

## Acceptance and audit rubric

Automated checks read decision.json, preserve supplied source/case identities, verify the expected
recommendation and require a contained parseable evidence report. These alone do not establish an
executed comparison. Inspect source, reports and actual tool receipts against this frozen rubric:

1. Every supplied case is checked with exact structural JSON semantics; incorrect variants cannot win.
2. Each feasible variant has three fresh untraced setup-plus-call timing samples per measured case,
   with call-only and subprocess wall time retained, plus three separate fresh Python allocation
   samples starting before module import and ending after the call. Timed outputs remain checked.
   An already excluded variant can stop early. No hidden warmups or cross-trial module state.
3. Qualification applies the configured measured Python allocation cap and timeout/crash/incorrectness
   failures; selection applies sum of case median setup-plus-call seconds and baseline/tie rules.
4. Experiment, variants, declared dependencies and measurement implementation have matching source
   SHA256 identities before/after; observed changes invalidate the experiment. Environment and
   exclusions are stated. Native runner or independently written equivalent evidence is acceptable.
5. Measurement code and actual successful tool execution support the reported samples. No fabricated
   run, revised expectation, unauthorized source edit or unsupported performance claim qualifies.

Record each rubric result with a source/report/tool-receipt reference and unresolved limits. Keep
correct recommendation, full protocol completion and model-process completion separate. A wrong
winner, missing evidence or a timeout cannot become a completed task by reporting only partial work.
The coordinator authored the runner specification/tasks and audits results; this is not independent
or inference-proof scoring. No prose/heading, runner-report-schema or novelty bonus is awarded.

## Time and results

Primary usefulness observations: accepted measured recommendation and process completion time within
each pair. Report wall time, timeouts as censored, actual tool starts, added measurement code and raw
provider counters descriptively. Lines/calls are not a quality or cost score. Do not convert counters
to money or equate the supplied candidate's speedup with a treatment benefit. Keep one-time build/
review effort separate from per-task time. Shared host/service load and concurrent execution can
change times; three local timing samples do not replicate an agent trial. One sample per cell and
two narrow synthetic tasks cannot establish significance or general productivity/invention gains.

Before dispatch, run the actual utility on both tasks to establish feasible recommendations and clear
margins. Keep calibration outside worker inputs. Freeze guide/scripts, fixtures, protocol and rubric
identities before model work. Preserve ties, failures, missing evidence and infrastructure errors.
Do not change the runner in response to trial results and call a repeat independent.

## Evidence and retention

The plugin owns runner runtime, profile, fixtures and checks. Existing run_tools owns dispatch,
isolation, attempt/deadline bounds and immutable snapshots. The existing collection gap ledger owns
self-review findings, source traces and accepted outcomes. Retain a durable audit bundle for this
user-requested evaluation: exact sources/prompts, final artifacts, grades/adjudications, tool-only
receipts, process/counter outcomes and hashes. Exclude service thinking and private account/billing
payloads. Verify member hashes and fresh-directory restoration. Keep prior evidence intact. Retain
until superseded by reviewed evidence and no active consumer needs the original. No publication.
