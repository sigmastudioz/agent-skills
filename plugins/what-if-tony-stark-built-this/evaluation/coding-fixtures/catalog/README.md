# Release catalog scaling ticket

`tools/build_catalogs.py` is an exact copy of a maintained release catalog builder.
Its real consumers are the three agent marketplaces and release integrity checks.
`reference/original.py` is the unchanged before implementation, not a suggested fix.
`SOURCE.json` records its provenance. Work here is an isolated candidate, not a deployment.

Make release hashing use bounded Python memory for large shipped files, and avoid
walking entire excluded tool/cache subtrees. Keep `render(root)`, `build(root, check=False)`
and the script CLI compatible. Output dictionaries, deterministic ordering, full SHA256
content identities, native host author handling, stale-check behavior and validation-before-write
must remain equivalent. Continue rejecting distribution symlinks outside ignored tool folders,
including symlink directories. Ignored tool-folder symlinks remain allowed. A same-size changed
file must change its digest; metadata alone cannot stand in for content. Do not add a persistent
cache, dependencies or concurrency. Preserve errors on malformed/inconsistent registries.

Delivered implementation must hash a 48 MiB shipped asset while keeping peak Python traced
allocation below 8 MiB for a small plugin tree. This cap includes importing the candidate and
one render call; it excludes input JSON parsing and result encoding. This is tracemalloc,
not process RSS. The before implementation may fail that cap; report its failure honestly.

Own `tools/` and new tests, experiment setup/adapters, generated data and evidence. Supplied
tests, README, reference, SOURCE and instructions are readonly. Run the supplied tests, add
meaningful regressions and verify the CLI/build/check consumers, including failure paths.

## Comparison you must set up

No alternate implementation, workload generator, benchmark adapter, expected-result data or
experiment manifest is supplied. Inspect the source, implement the change, and create all of
those comparison inputs yourself. Use the unchanged reference as the before implementation.
Build at least two deterministic workloads: (1) a many-small-files tree with deeply nested ignored
tool data and (2) a tree with the 48 MiB shipped asset. Include meaningful correctness/failure
cases separately. Both workloads must exercise the real `render` entrypoint. Prepare files before
the measured call, include source-module import plus one render call in timing, and verify the
entire returned result against the unchanged reference, not just counts or selected hashes.

For each implementation/workload collect at least three fresh-process, untraced timing samples
and three separate fresh-process Python allocation samples beginning before source-module
import and ending after the call. An allocation-excluded implementation can stop allocation
sampling after its first cap violation. Check outputs in all samples. Keep per-sample data,
environment, commands, exclusions and source/input SHA256 identities before/after. Hash adapters,
generators, declared dependencies and the generated data identity too. A timing instrumented
with tracemalloc is not a valid untraced timing sample. State filesystem/cache limitations.

Write `decision.json` with `implemented` (boolean), `reason` (text), `evidence_path` (contained
machine-readable JSON report path), and `limitations` (list). The report schema is your choice.
Explain correctness, resource qualification and whether the candidate should be adopted;
a rejected candidate is an honest result but does not fulfill the optimization ticket.
Keep comparison setup, reruns, debugging and verification inside this session's 1800-second budget.
