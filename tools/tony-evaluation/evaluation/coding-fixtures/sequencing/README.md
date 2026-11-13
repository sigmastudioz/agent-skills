# Exact album sequencing scaling ticket

`music/sequence.py` is an exact copy of maintained record-label code. Its public consumers
are the technical sequence proposal and editorial-order validation workflows.
`reference/original.py` is the unchanged before implementation, not a suggested algorithm.
`SOURCE.json` records provenance. Work here is an isolated candidate, not a deployment.

Speed up `propose_sequence` for long track collections and make `validate_album_order` avoid
computing unused technical proposals. Keep both signatures, the complete returned proposal,
error types/messages on supported invalid inputs and the deterministic greedy ordering exactly
compatible. Preserve two-decimal rounded jump comparisons, source-order tie breaking, unavailable
or nonfinite level handling, ordered kept blocks, pinned endpoints, validation order and input
immutability. This is exact optimization, not a new artistic scoring method. Keep domain rules
with this module; no dependencies, approximation, persistent caches or concurrency.

The candidate must be at least 3x faster than the before implementation in the coordinator's
untraced repeated-call check on 1000 deterministic finite-level tracks, with the entire proposal
equal. Editorial-order validation must preserve error precedence and stop generating a greedy
proposal just to validate an externally authored order. Do not special-case the benchmark size.
Add regression tests, inspect callers and document remaining complexity and unknowns.

Own `music/` and new tests, experiment setup/adapters, generated data and evidence. Supplied
tests, README, reference, SOURCE and instructions are readonly. Run supplied tests and add
meaningful regressions including invalid inputs and rounded ties.

## Comparison you must set up

No alternate implementation, workload generator, benchmark adapter, expected-result data or
experiment manifest is supplied. Inspect, implement, and create the comparison inputs yourself.
Use the unchanged reference as the before implementation. Create at least two deterministic
workloads of at least 300 tracks each: one unconstrained proposal and one with ordered blocks
and pinned endpoints. Exercise both public entrypoints in correctness checks. The measured
proposal must include the real function and verify the entire result against the reference.
Generate tracks before timing; include source-module import plus one proposal call in timing.

For each implementation/workload collect at least three fresh-process, untraced timing samples
and three separate fresh-process Python allocation samples beginning before source-module
import and ending after the call. Check outputs in all samples. Keep per-sample data,
environment, commands, exclusions and source/input SHA256 identities before/after. Hash adapters,
generators, declared dependencies and workload data too. Timing with tracemalloc active is not
an untraced timing sample. State that traced allocation is not RSS and samples are not statistical
proof. Use additional regression tests for nonfinite values that a strict JSON adapter cannot encode.

Write `decision.json` with `implemented` (boolean), `reason` (text), `evidence_path` (contained
machine-readable JSON report path), and `limitations` (list). The report schema is your choice.
Explain correctness and whether the candidate should be adopted. A rejected candidate is an
honest result but does not fulfill the optimization ticket. Keep comparison setup, reruns,
debugging and verification inside this session's 1800-second budget.
