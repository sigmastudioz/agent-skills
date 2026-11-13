# What If Tony Stark Built This 1.1.0: matched pilot

Recorded November 12, 2026. Result: **seven tied task/model comparisons and one small rubric gain**.
This pilot does not establish a general engineering-quality advantage from the skill.

## What changed in the skill

The runtime now explicitly exposes System Map, Gap Radar, Failure Lab, Impact Trace, Repair Loop
and Evidence Memory. Capabilities are selected by the uncertainty blocking the task. A reproducible
experiment-packet template and adaptive-decision reference connect failed assumptions to retracted
conclusions and a revised next action. Small fixes can use a short route.

## Actual comparison

Four synthetic tasks were completed by each model with and without the explicit skill instructions:
16 fresh Cursor CLI calls, one attempt per cell. Models were `grok-4.7-high` and
`claude-fable-5-2-high`. All 16 returned parseable artifacts within the fixed 600-second limit.
All exited successfully, with zero recorded tool calls and no scored critical failures.

| Model | Task | Without skill | With skill |
| --- | --- | --- | --- |
| Fable 5.2 | Tenant-scoped inventory reservation | 18/18 checks | 18/18 checks |
| Fable 5.2 | Stable sorting fix | 6/6 checks | 6/6 checks |
| Fable 5.2 | Offline synchronization invention | 9/10 rubric | 9/10 rubric |
| Fable 5.2 | Replanning after rejected cache hypothesis | 10/10 rubric | 10/10 rubric |
| Grok 4.7 | Tenant-scoped inventory reservation | 18/18 checks | 18/18 checks |
| Grok 4.7 | Stable sorting fix | 6/6 checks | 6/6 checks |
| Grok 4.7 | Offline synchronization invention | 8/10 rubric | 9/10 rubric |
| Grok 4.7 | Replanning after rejected cache hypothesis | 9/10 rubric | 9/10 rubric |

All eight returned code artifacts were inspected before local execution. They passed 96 behavioral
test-case executions in total: 48/48 in each condition. These are repeated checks on eight artifacts,
not 96 independent model trials. Inventory checks cover normalization, invalid inputs, atomic
rejection, tenant/separator isolation, replay/conflict, release-once and detached receipts. Sorting
checks cover direction, missing-last, stability, zero/negative/fractional scores and non-mutation.

The sole rubric gain was Grok supplying a meaningful smaller system-design comparator in its
invention answer. Without the skill, its "comparator" described version/value comparison inside
the design. With the skill, it compared keyed-field reconciliation against a simpler whole-field
approach. This is a one-point qualitative difference from one pair, not proof of a repeatable gain.

All four invention answers received partial experiment credit: they supplied useful finite
scenarios and rejecting observations, but no complete runnable fixture/command/cleanup recipe.
The tasks were proposal-only, so no model-side experiment execution was expected. The replanning
answers from both Grok conditions also omitted parts of the held-worker/failure/duplicate/reorder
test sequence. Fable's replanning answers covered those cases in both conditions.

## Observed effort and format

Means below are across four tasks per model/condition. Wall time includes service variation,
shared-host/cache effects and concurrent scheduling; it is descriptive, not a reliable efficiency
estimate or pricing claim.

| Model | Mean wall seconds, without -> with | Mean reply characters, without -> with |
| --- | --- | --- |
| Fable 5.2 | 90.0 -> 101.4 | 3,729.0 -> 3,676.8 |
| Grok 4.7 | 253.1 -> 275.1 | 3,832.0 -> 5,726.2 |

Treatment prompts supplied all runtime references inline and were 43,882 UTF-8 bytes larger per
cell (mean total prompt 4,943.2 -> 48,825.2 bytes). This does not measure production lazy-reference
loading. Grok's treatment replies included substantial duplicated structured content in addition to
the requested analysis; that content is counted in reply size, not rewarded as extra quality.

Fable met the requested answer-field word limits in all eight runs. Grok met them in three of four
runs per condition: its treatment inventory rationale had 151 whitespace-separated words against
150; its control replanning analysis had 746 against 700. These format observations remain separate
from the predeclared correctness/rubric scores. Provider token/cache counters are retained verbatim;
their cross-provider accounting was not normalized and no monetary cost was calculated.

## Method and limits

- The [protocol](PROTOCOL.md), [tasks](tasks.json) and [rubric](rubric.json) were fixed before dispatch.
  The runtime, task and rubric hashes were rechecked unchanged while runs were active.
- Each pair shared task, model, common engineering defaults, output contract and no-tool limits.
  Only explicit target-skill runtime guidance differed. Tests, scoring criteria, prior reviews and
  results were excluded from model input. A shared baseline's relevant rules were supplied inline;
  no ancillary baseline documents were uploaded.
- Independent sessions were counterbalanced/interleaved with at most three active. No model call
  was retried, repaired or given feedback. Returned code was tested by the coordinator afterward.
- Reasoning was scored against five 0/1/2 dimensions with supporting excerpts. Model/condition
  labels were withheld during scoring, and scores were sealed before revealing the mapping.
  The coordinator authored the skill and rubric; scoring is not independent or inference-proof.
- This is one-shot instruction ablation on one Cursor host/account. Common global metadata/settings
  may remain. It is not a guaranteed virgin-system-prompt comparison, automatic-discovery test,
  autonomous tool-use trial, production workload or statistical significance result.
- Detailed task prompts and capable models create a strong baseline; the two coding tasks had a
  correctness ceiling in both conditions. One observation per cell cannot establish general effects.

## Decision

Keep the six capabilities and the new runtime resources available for appropriate tasks. This pilot
supports proportional use: it found no coding-correctness gain, one small invention-score gain,
and higher observed mean response time for both models. It does not justify mandatory use on routine
fixes or a claim that adding more instructions improves quality.

The next empirical question, if requested, is whether selectively supplied task-relevant guidance
improves outcomes on fresh, harder tasks without the full inline-context overhead. Do not tune on
these tasks and call a rerun independent evidence. Runtime version 1.1.0 was not changed after seeing
the results.

## Provenance and verification

Sealed score-file SHA-256:
`01a9881df064efe0fe72469e0c696774ef63276b8600d1ed5ab95582729c3e52`.
The collection's owning gap record links the durable evidence bundle, input/source hashes, final
responses, code checks and dimension-level scores. Service thinking payloads are excluded from the
delivery bundle; audit receipts retain stream hashes and event counts. Raw local service streams
remain temporary material rather than runtime dependencies.

All 198 repository regression tests passed with native Blender access. These regressions establish
package/helper behavior, separately from the model comparison above. Final package/catalog/link
checks and local discovery aliases are recorded in the owning collection trace. No publication,
deployment or remote-host installation was performed.
