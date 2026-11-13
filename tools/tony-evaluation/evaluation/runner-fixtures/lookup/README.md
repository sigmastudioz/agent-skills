# Select a lookup mechanism

We need a measured choice for a batch lookup API. Each row has a string tenant, string key and integer
value; each query is a [tenant, key] pair. Return the first matching row's value, or null if absent.
Order, case, separators and zero values matter. The supplied variants are alternative implementations;
choose a correct feasible one for these representative synthetic workloads. Do not change their code.
The memory cap is eight MiB of measured Python allocations including module setup and call.

## Deliverable and measurement contract

Choose among the supplied implementations; keep all inputs, variant source and dependencies unchanged.
Write decision.json with winner (variant ID or null), reason, and evidence_path (a local JSON report).
Keep your measurement code or supplied-tool source identity available alongside that evidence.
Use the supplied experiment.json as authoritative inputs, exact expected outputs and configuration.
A correct recommendation requires actual measurements, not just source inspection or an estimated win.

Validate exact structural JSON outputs (including types) on every case before ranking. Each marked
measurement case needs three fresh-process untraced timing samples and three separate fresh-process
allocation samples per eligible variant, no hidden warmups. Measure module initialization plus one
call; record call-only and subprocess wall time separately. Timing used for ranking must run without
tracemalloc; tracing changes execution cost. In separate allocation samples start Python tracing
before importing the variant and stop after the call; this is not RSS. Input JSON parsing
and interpreter startup can be excluded from setup-plus-call but state those exclusions. Every timed
sample must still return the exact expected output. Failed, timed-out, incorrect or over-memory-budget
variants cannot win. Rank by sum of measured-case median setup-plus-call seconds; constrain the maximum
measured Python traced peak to memory_limit_bytes. Keep a feasible baseline within tie_fraction of the
best; otherwise an unresolved candidate tie has no unique winner. Do not infer significance from three
samples or omit preprocessing costs. Candidate startup/prints must not corrupt your evidence.

Report raw samples, aggregates, qualification/exclusion reasons, decision and SHA256 identities of the
experiment, candidate source, declared dependencies and measurement implementation. Check identities
before/after measurement. A changed-input experiment is invalid. Refuse to overwrite unrelated work.
Standard-library Python tools are available. No dependency installation, network, account changes or
extra agent is needed or authorized. Supplied code is local synthetic code; no production side effects.
