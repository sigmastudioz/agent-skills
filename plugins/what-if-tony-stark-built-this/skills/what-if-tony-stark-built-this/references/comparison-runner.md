# Comparison runner (Manifest v1)

Portable standard-library CLI that compares authorized local design variants under a
fixed acceptance workload. It is a measurement tool for Failure Lab experiments, not an
agent service, general benchmark framework, or security sandbox.

## When to use

Use this runner when two or more inspected local implementations should be compared on
the same correctness cases and at least one measured case. Prefer it over narrative
claims about speed. Do not claim statistical significance from medians or `tie_fraction`.

## Public entry

```bash
python3 plugins/what-if-tony-stark-built-this/skills/what-if-tony-stark-built-this/scripts/compare_designs.py \
  path/to/experiment.json \
  --output path/to/report.json
```

Paths inside the manifest are relative to the manifest's directory. The output path must
not already exist; the runner refuses to overwrite reports or inputs.

Runnable extreme-margin example:

```bash
python3 .../scripts/compare_designs.py \
  .../assets/comparison-example/experiment.json \
  --output /tmp/stark-compare-example-report.json
```

## Manifest v1

```json
{
  "version": 1,
  "baseline": "base",
  "variants": [
    {"id": "base", "path": "base.py", "function": "run"},
    {"id": "candidate", "path": "candidate.py", "function": "run"}
  ],
  "cases": [
    {"id": "small", "input": {}, "expected": {}, "measure": false},
    {"id": "workload", "input": {}, "expected": {}, "measure": true}
  ],
  "dependencies": [],
  "repeats": 3,
  "timeout_seconds": 10,
  "memory_limit_bytes": null,
  "tie_fraction": 0.05
}
```

Rules:

- Every variant function takes one JSON-compatible argument and returns one JSON-compatible result.
- Correctness uses exact structural JSON equality (bool is not int; nonfinite values rejected).
- All cases are acceptance checks, including measured cases. At least one `measure: true` case is required.
- Baseline, variant, and case ids must be unique. Variant and dependency paths must be contained regular files.
- `repeats` is a bounded positive integer; `timeout_seconds` is finite positive; `memory_limit_bytes` is null or a positive integer; `tie_fraction` is finite in `[0, 1)`.
- No shell-command manifests, third-party dependencies, downloads, or automatic model calls.

## Execution model

1. Validate configuration before any variant runs.
2. Record SHA256 identities of the manifest, each variant source, declared dependencies, and runner/worker sources.
3. For each variant and case, run a fresh correctness subprocess.
4. After all correctness cases pass, each measured case gets `repeats` fresh untraced timing subprocesses and `repeats` separate traced allocation subprocesses. Every trial still checks correctness; an excluded variant can stop early.
5. Rank only untraced module-import/setup-plus-call timings; report call-only time separately. Separate allocation trials measure tracemalloc peak across import and call, ending before result validation/serialization (Python traced allocation, not RSS). Tracing does not perturb the ranked timings.
6. Re-check input identities during and after execution. A changed-input experiment is rejected.
7. Continue collecting failure detail across variants unless input identity changes. Candidate stdout/stderr are captured as tails and never parsed as the machine report.

Excluded from measured intervals: parent input parsing, interpreter startup outside the worker, worker protocol JSON encode/decode, and parent orchestration. `subprocess_wall_seconds` retains worker-reported wall time after worker startup; `parent_wait_seconds` retains parent-observed launch/wait time. Neither is the ranking metric. Variant sibling imports are supported; manifest dependencies are declared provenance, not automatic package/dependency discovery.

Default aggregate metric: `sum_median_setup_plus_call_seconds` over measured cases, constrained by maximum measured Python traced peak against `memory_limit_bytes` when set.

## Decision rule

Among correct feasible variants, select the lowest aggregate time. Preserve a feasible baseline if it is within `tie_fraction` of the best (`baseline <= best * (1 + tie_fraction)`, or both zero). If the baseline is outside that band and multiple candidates fall within that best-time tolerance band, the outcome is `inconclusive` with no unique winner. If no variant is feasible, there is no winner. Failing or over-budget variants are never recommended. Speedup versus baseline is omitted when the baseline is invalid. Medians and tolerance are not statistical significance.

## Report schema (summary)

Top-level fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Report schema version (`1`) |
| `status` | `completed` or `rejected_changed_input` |
| `manifest` | Echo of key experiment settings |
| `environment` | Python/platform plus measurement notes |
| `limits` | Timeout, memory cap, repeats, tie fraction, metric names |
| `identities` | SHA256 provenance of inputs and runner (not a tamper-proof guarantee) |
| `variants` | Per-variant feasibility, case trials, aggregates, exclusion reasons |
| `decision` | `winner_id`, `outcome`, `reason`, aggregates, optional `speedup_vs_baseline` |

Decision `outcome` values: `baseline_preserved`, `candidate_selected`, `inconclusive`, `no_feasible_variant`, `rejected_changed_input`.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Experiment completed; report written (winner may be null) |
| `1` | CLI usage error |
| `2` | Manifest/validation error before a completed experiment report |
| `3` | Refused to overwrite an existing report path |
| `4` | Inputs changed during execution; rejection report written when possible |
| `5` | Internal runner failure |

Ordinary candidate incorrectness, timeouts, crashes, or memory-cap failures still produce exit `0` with a structured report describing exclusions.

`measured_trials` contain untraced timings; `allocation_trials` contain the separate traced samples. Memory qualification uses measured-case allocation peaks. All correctness cases run before timing; incorrect candidates are excluded without ranking. Temporary scratch names do not use caller-controlled IDs, and reports are published exclusively without replacing another writer's file.

## Safety and limits

Subprocess isolation is not a security sandbox. Execute only authorized inspected local code. Source hashes are provenance and change detection, not dependency discovery or integrity attestation. This tool does not demonstrate product efficacy by itself; it only reports the scoped comparison.

Python 3.10+ is required. POSIX supports cleanup of owned worker process groups; other platforms use the worker-process fallback and do not establish descendant cleanup. A report covers declared files and supplied cases on the recorded environment, including normal filesystem/bytecode caches. It is not a cold-machine benchmark or a complete dependency attestation. Candidate output is buffered; inspect side effects/output volume before execution. Configured repeat/timeout bounds are 1–10000 and up to 86400 seconds; use small values appropriate to the authorized experiment.
