# Engineering invention trial: frozen before model dispatch

Version 2.0.0 targets a better mechanism when the current approach cannot meet a consequential
constraint. This is a new task family; old general-coding results remain historical and are not
relabelled. Comparing across versions cannot isolate the effect of this rewrite. Within this trial,
the added selected guidance is the planned difference.

## Matched conditions and authority

Two fresh repositories: Maintenance Window Planner and Pulse Telemetry Analyzer. Both have correct
small-input behavior and three passing public checks. Their expansion-based baseline cannot support
the documented target scale. No prior relay/importer code or prompts are reused as tasks. Success
requires exact outputs through the public API and actual CLI at scale; a faster inner loop or a new
presentation alone cannot establish it. Different algorithms are permitted; novelty is not scored.
The coordinator authored the skill and tasks, so this is not an independent study.

Models: `grok-4.7-high` and `claude-fable-5-2-high`, same explicit settings as before. Eight fresh
processes: two tasks x two models x two conditions, one attempt per cell, maximum three active,
1200 seconds each. No corrective reruns, reviewers or additional agents. Both arms get independent
writable clones of the same committed synthetic task base, identical ticket, contracts, tools,
relevant shared DDD defaults and completion request. Condition order is counterbalanced. All input
identities are frozen in the manifest before dispatch. A timeout stays a timeout.

Control: no additional Stark guidance. Treatment: the actual 2.0 SKILL.md plus the one relevant
references/invention-methods.md, concatenated byte-for-byte with two newlines. These constitute the
selected invention guidance. No other references, templates, scoring criteria, prior results, hidden
checks or coordinator witness solutions enter worker checkouts. Workers must not load global skills.
Host metadata/settings may remain common and service-side context is not completely observable.

Use Cursor tools, sandbox enabled and safe-tool auto-review, without permission-bypass flags.
Workers own package code and added tests in their isolated checkout; original expectations,
contracts, common instructions and guidance are readonly. Standard-library local execution and
read-only Git are allowed. Own generated scratch data and own tool-output files are allowed;
external task inputs, network, dependency installs, background jobs, broad process kills, extra
agents, commits, publication and deployment are not. Supply the actual ownership/handoff contract.

## Acceptance and measurements

Inspect candidate source and executable additions before executing them. In fresh grading copies,
restore original public tests and run the frozen held-out checker. It has 13 distinct methods per
task. Do not reward headings, brainstorming quantity or character voice. Report separately:

- Public preservation and held-out behavior, including exact small randomized oracle comparisons,
  finite/empty/invalid inputs, large integers, target-scale behavior and actual CLI output.
- Scale feasibility: the documented large inputs complete within a five-second per-case guard;
  Pulse also has an eight-MiB traced allocation guard on a four-million-sample encoded workload.
  The guards are local feasibility gates, not universal throughput benchmarks. No resource claim
  follows just from a small correctness test. The input expansion helpers keep their original limits.
- Process completion within 1200 seconds, even if a partial frozen artifact passes code checks.
- Scope/tampering/leakage observations; critical issues cannot count as accepted solutions.
- Actual tool starts, guide reads, wall time and raw provider usage, descriptive only. Timed-out
  elapsed time is censored; missing usage remains missing. Do not infer monetary cost.

Before dispatch, calibrate original public success and target-scale failure, and confirm that a
coordinator-owned witness outside worker inputs can satisfy every held-out check. The witness proves
feasibility, not independence. The Windows oracle is checked against brute force on small random
inputs; Pulse uses an independently expanded small-data oracle and known large identities. Record
checker and witness hashes. Do not tailor the runtime guide or revise acceptance after scores arrive.
One sample per cell cannot establish significance or a general invention advantage. Strong controls
may still solve every task; preserve ties and failures rather than increasing difficulty after seeing
which condition wins. Mechanism observations remain descriptive, not a post-hoc bonus score.

## Evidence and retention

The plugin owns fixtures, runner profile and checker; existing tool-trial modules own dispatch,
snapshots, grading and audit. The collection's existing gap ledger records source traces, accepted
outcomes and links a durable evidence archive for this user-requested behavioral audit. Retain exact
prompts, sources/guide/protocol/checker hashes, final code/diffs, grade receipts, process outcomes,
tool-call receipts and provider counters. Exclude raw service thinking and credentials. Verify ZIP
integrity, member hashes and restoration into a new empty directory. Keep the old evidence intact.
Retain until a reviewed replacement supersedes the trial and no active consumer needs its originals.
