# Maintained coding tasks with comparison setup included

The skill produced a much faster sequencer, but this trial does **not establish an overall
completed-task time saving**. The fully qualifying sequencing pair took longer with the skill.
The catalog runs both produced working implementations and executed comparisons, but both omitted
a required post-run identity check of their actual filesystem workload. That unfinished work
prevents treating their apparent time difference as a completed-workflow saving.

## What was tested

Four fresh Cursor `grok-4.7-high` processes, one per task/condition, sequentially, with a
1800-second limit each and no corrective model calls. Each pair started from the same committed
copy of maintained source, unchanged reference, public tests, ticket and common engineering defaults.
The treatment additionally received the unchanged Tony 2.1 entrypoint, runtime references and runner
scripts. Models created their own implementations, workload generators, adapters, expected results,
measurement setup and reports. No task-specific benchmark, manifest or candidate was supplied.

These are maintained repository code excerpts with new scaling tickets, not production incidents
or production traffic. The source origins and hashes are in `coding-fixtures/*/SOURCE.json`.
The [protocol](CODING_PROTOCOL.md), checker, source tasks, runtime and prompts were frozen before
dispatch. Previous missing Fable cells remain pending; this trial made no new Fable calls.

## Time and acceptance

| Task | Normal tools | Tony skill and runner | Coding checks | Complete measurement protocol |
| --- | ---: | ---: | --- | --- |
| Exact album sequencing | 20m 57s | 23m 44s | Both pass | Both pass |
| Release catalog scaling | approximately 24m 49s | approximately 19m 45s | Both pass | Both partial: missing actual data post-check |

Task times include Cursor startup/service delays, reading, problem investigation, coding, all
comparison setup and data generation, debugging, internal failed attempts, sampling, verification
and final reporting. Queue waiting and coordinator adjudication are excluded. There was one model
process per cell; no timeout and no extra agent call. All four native Cursor results reported success.

- Sequencing: 1257.233 seconds normal versus 1423.732 with the skill, **13.2% longer with the skill**.
- Catalog: approximate capture boundaries 1488.569 seconds normal versus 1184.685 with the skill.
  This is **20.4% less observed elapsed time**, but neither is a fully qualifying comparison task.
- Summing observed elapsed gives 2745.802 seconds normal versus 2608.417 with the skill, about
  **5.0% less observed time**. This is descriptive only. It is **not** an aggregate completed-task
  saving, because the catalog setup was incomplete in both conditions.

Only the sequencing pair supports a completed-task time comparison under the frozen criteria.
The skill did not save development time on that pair. Two tasks and one agent sample per condition
cannot establish significance, general coding productivity, cross-model efficacy or net development ROI.

## Code quality and runtime outcomes

All four implementations passed the frozen independent coding checks: 18 unittest methods across
the four outputs, plus 79 supplied/worker-authored public tests across the isolated grading copies.
Additional independent checks confirmed both catalog CLI generate/check/stale/symlink paths, exact
encoded reference output and actual pruning of excluded directories. Production source was not
replaced by the experimental candidates.

The common held-out sequencing check used the same seeded 1000-track data for both candidates:

| Result | Normal tools | Tony skill |
| --- | ---: | ---: |
| Median proposal call | 0.13326 seconds | 0.003925 seconds |
| Speedup against that check's original implementation | 20.74x | 754.33x |
| Candidate source lines, descriptive only | 142 | 288 |

Both preserved the checked complete proposals, rounded ties, blocks/pins, nonfinite levels,
supported invalid-constraint precedence and input immutability. Both stopped building an unused
proposal during editorial validation. The skill candidate ran about **34x faster than the normal
candidate** on these held-out inputs. Its head-ordered selector visits the winning rounded-distance
neighborhood; the normal candidate caches source positions and endpoint levels before a simpler
greedy scan. Both retain quadratic worst cases. The skill traded additional development time and
implementation complexity for substantially lower runtime on this workload; this is not a universal
numerical-correctness or artistic-quality claim.

Both catalog candidates streamed full SHA256 and pruned ignored tool trees while preserving Path
ordering, marketplace identity handling, stale checks, validation-before-write and symlink rejection.
The independent import-plus-render traced peaks for a small tree with a 48 MiB asset were 558,988 bytes
normal and 541,640 bytes with the skill, both well below the 8 MiB cap. These are Python allocations,
not RSS; the small difference is not evidence of a meaningful memory advantage between conditions.

## The unfinished filesystem proof

Actual sampling and full-result checks passed in both catalog runs. The failure is specific:

- Normal: hashes labelled `before_source_sha256` and `after_source_sha256` identify the before and
  after **implementations**, and were both collected after sampling. Pre/post experiment identities
  for the candidate and setup scripts were not recorded. Data listings were created before sampling
  but actual data-tree identities were not rechecked afterward.
- Skill: the runner correctly checked manifest, variants, source/helper/generator files and the
  provenance JSON before/after. That JSON contained a pre-run data-tree digest, but the actual data
  files were not declared dependencies and their tree/link identities were never rechecked afterward.
  An unchanged document describing a tree does not establish that the tree stayed unchanged.

Both therefore fail frozen manual requirement 4. The other measurement requirements pass.
The catalog control retained three untraced samples for every implementation/workload, separate
allocation samples, explicit cap exclusions and disclosed warmups. The skill run retained three
untraced and separate allocation samples, stopping the original's large-file allocation series
after its cap violation. Its sixteen correctness cases all matched.

The coordinator subsequently checked actual file bytes and link text against both retained pre-run
tree identities; all matched. This supports the numerical evidence. It does **not** retroactively
complete agent-authored setup or turn the original agent time into a qualifying finished task.

The practical missing capability is explicit tracking of filesystem inputs, including safe
directory/link identity handling. Source hashing alone is insufficient for these adapters.
This is an improvement opportunity established by the test; the runtime was not tuned or expanded
after seeing these results.

## Instrumentation, overhead and limitations

Two collection issues were disclosed before affected outcomes were graded:

1. The frozen dispatch timer includes snapshot copying and Git status/diff after process exit,
   before final snapshot hashing. The sequencing skill's finalization contribution was about
   0.061 seconds. Both raw elapsed and independent pre-copy boundaries are retained.
2. The old snapshot collector rejects all symlinks. Both catalog tasks legitimately generated
   positive/rejection symlink fixtures. Their original collection errors and empty original
   snapshots remain intact. A read-only vnode observer captured native completion; a separate safe
   recovery copied regular inputs and retained link target text without following links. Control
   completion boundaries span 1488.356–1488.569 seconds; treatment boundaries span
   1184.531–1184.685 seconds. The lost outer return codes are explicitly unknown, rather than invented.
   These collection errors are not classified as actor coding failures.

No task source, acceptance criterion, model setting or attempt budget changed. Standard-library
dependency inspection outside the checkout was allowed equally and audited separately from outside
task inputs or global skills. No such task/skill contamination was observed in tool receipts; host
and provider implicit context cannot be fully audited.

Persisted experiment preparation took 256.369 seconds before dispatch; initial inspection before
the first persisted packet was not timed. The four-call campaign lasted 5354.343 seconds (89m 14s).
Independent checker subprocesses took 26.267 recorded seconds in total; copying, review and archival
are additional shared evaluation overhead. A coordinator verification helper initially tried to use
an intentionally null qualified median for an excluded baseline. That was corrected; grading resumed
only its unexecuted final cell, reusing the three completed frozen-source receipts. No agent was rerun.
Earlier generic runner build/review effort is a separate one-time cost, not newly charged per task.

Conditions designed different valid workloads: both sequencers chose 1000 tracks, but the catalog
control chose 160 shipped/6400 ignored files and the treatment 80/1200, with separate large-file trees.
The treatment sized its first workload to keep the original below the runner's global memory cap.
Filesystem caches were warm and host/service load was not fully controlled. Fresh controls had no
pre-existing reusable harness. The treatment bundles guidance and a tool, so this trial cannot
attribute an effect to one instruction. The coordinator authored tasks and audited outputs;
the audit is reproducible, not independently blinded. Lines, tool calls and raw provider counters
are retained descriptively and are not quality or monetary-cost scores.

## Reproduction and retained evidence

`run_coding_trial.py prepare --output <new-empty-trial-root>` creates the isolated packets without
calling a model. Its explicit `run` action makes up to four new Cursor calls; it is not needed to
review this result. Do not relaunch the completed campaign as a repair.

The collection retains `.principal-ddd/evidence/stark-coding-total-1.zip`, with frozen inputs/prompts,
source origins, final regular artifacts, link metadata, raw counters, tool-only receipts,
independent checks, manual adjudications and clock corrections. Raw service thinking and private
account/billing stderr are excluded, with hashes retained. Extract only into a new empty directory;
check the manifest, and inspect/regenerate authorized fixture links before any local replay.
The owning ledger records the archive checksum and verified restoration. Prior trial evidence remains.
