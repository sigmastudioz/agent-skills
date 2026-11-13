# Tony skill self-review: comparison runner

This applies the engineering-invention skill to its new tool after the requested Cursor build.
It is a source/behavior review using the skill, not an independent model review or a character claim.

## Does the mechanism remove useful work?

The repeated work is constructing a correctness gate, fresh-process measurement harness, provenance
receipt and qualified decision for each local alternative. The runner supplies that machinery. It
still needs representative cases, exact expected results and inspected implementations. Its own
example demonstrates wiring, not agent productivity. A matched normal-tools trial is a separate gate.

| Capability | Actual application |
| --- | --- |
| System Map | Skill route -> focused reference -> CLI -> manifest -> worker -> qualification -> JSON report |
| Gap Radar | Challenge whether a fast incorrect candidate, tracing overhead, tie or failed child can produce a misleading recommendation |
| Failure Lab | Seven new executable counterexamples fail against the delivered build; original 15 tests pass |
| Impact Trace | Follow module imports, setup cost, scratch paths, report publication and changed/deleted inputs across parent/worker boundaries |
| Repair Loop | Correct the measured mechanism and decision/IO edges, then run regressions and actual fresh comparison fixtures |
| Evidence Memory | Keep original Cursor snapshot, build report, before/after checks and final input identities; retain null/pending efficacy results |

## Supported findings and corrections

| ID | Finding and consequence | Smallest correction and closure |
| --- | --- | --- |
| RUNNER-01 | Ranking times were taken with tracemalloc enabled; tracing can alter costs differently across implementations | Separate untraced timing and traced allocation processes, check outputs in both, stop tracing before result validation; real trace-state regression passes |
| RUNNER-02 | Candidate ties used exact floating equality, so near-tied candidates could produce a false unique winner | Apply the configured tolerance band to candidates as well as baseline; deterministic 1.00/1.02 counterexample now inconclusive |
| RUNNER-03 | Normal sibling helper imports and dataclass module registration were missing | Add the local module directory and register the loaded module; real helper/dataclass CLI case passes |
| RUNNER-04 | Fixed report.json.tmp could overwrite another file; final replace could overwrite a concurrent report | Unique owned temporary file and exclusive link publication, cleaning only that temporary file; neighbor-file and concurrent-writer preservation checks pass |
| RUNNER-05 | Variant/case IDs were used as scratch path pieces, allowing traversal outside scratch | Use stable hashed directory components; traversal-ID test confirms containment |
| RUNNER-06 | A valid result file could mask a subsequent nonzero worker exit | Require successful process exit too; atexit failure is excluded as a crash |
| RUNNER-07 | Deleted input produced an internal error instead of a changed-input rejection report | Convert unreadable/disappeared tracked inputs to changed-input rejection; deletion case now exits 4 with no winner |

Additional adjacent checks cover strict numeric configuration, exclusive publication and owned-process
group cleanup after a leader exits. Interrupts also clean and reap the owned worker. Correctness checks
complete before ranking measurements; source identities are checked after each execution. These remain
bounded engineering claims: the tool is not a sandbox or an attestation of every dependency.

The original 15 tests passed. All seven added counterexamples failed on the original build; after
correction the 22-test gate passed. A tight 0.4-second timeout test was noisy under concurrent calibration;
its timeout was widened to two seconds while its five-second sleeper still must be rejected. This changes
test robustness, not the frozen trial's ten-second candidate limit or twenty-minute agent budget.
Final tests and calibration results are maintained in the collection gap ledger and audit receipt.

## Remaining limits

- Three timing samples and a tolerance band do not establish statistical significance.
- Python traced allocation excludes RSS/native/external process memory. Timing and memory are separate runs.
- Supplied cases do not establish universal correctness. Declared hashes do not discover all dependencies.
- Fresh processes retain normal OS/bytecode caches; this is not a cold-machine guarantee.
- Candidate output is buffered, so inspected side effects and output volume remain relevant.
- POSIX process groups support descendant cleanup; other-platform fallback is narrower and not host-verified.
- Builder elapsed time and later authoring/review costs must not disappear from any ROI claim.
- The mechanism can be useful while still failing to improve an agent's measured task outcome. The user-
  requested efficacy comparison stays separate, with no post-score tuning or forced positive conclusion.
