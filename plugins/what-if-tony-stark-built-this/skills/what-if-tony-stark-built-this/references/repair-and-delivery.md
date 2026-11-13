# Repair, instrumentation and delivery

Use this when implementation is authorized. Planning/review work can recommend these actions
without making changes. A completion claim must cover the result the user actually needs.

## Compare mechanisms before multiplying infrastructure

For a consequential gap, identify the existing capability or smallest repair first. Compare a
different mechanism when it could materially improve the result or resolve a critical unknown.
Evaluate all viable candidates against the same hard constraints and closure checks:

- Correctness and observable user outcome, including failure and recovery.
- Existing owners, public contracts, real consumers and relevant trust boundaries.
- Compatibility, migration needs, operational burden and reversibility.
- Measured resource behavior when relevant; estimates with their basis otherwise.
- Decisive unknown and the smallest experiment that could reject the candidate.

For example, duplicate processing might be addressed by an existing authoritative uniqueness
constraint, an idempotent state transition, or a new coordination mechanism. Inspect actual ownership
and guarantees before choosing. A new queue or distributed lock is not inherently more ambitious
or better. Do not prototype multiple solutions for an obvious local correction.

Use isolated branches/directories or the repository's existing experiment facility for candidates;
do not overwrite concurrent work. Each prototype has a decision question and cleanup/disposition.
A winning prototype needs product-code integration and verification before it is the delivered feature.
Do not ship abandoned alternatives, unused abstractions or new framework layers without consumers.

## Build through the boundary

Implement the chosen design as an end-to-end slice. Trace real input -> authorization -> owned
rules -> persistence/effects -> actual consumer -> usable outcome, and the relevant alternatives.
Keep domain rules in their existing owner and reuse public APIs. Preserve established behavior
outside the authorized change. Update registrations, exports, generated artifacts, migrations,
configuration and consumer handling where the slice requires them.

If the mission needs a larger capability than authorized, finish independent in-scope work and
present the concrete decision and its tradeoffs. Do not silently redefine success to avoid a gap.
An optional invention remains optional even if it is technically attractive.

## Create instruments only for a real question

When a claim cannot be observed, identify what signal would distinguish success, delay and failure.
Prefer existing telemetry, authoritative state and reconciliation before introducing a new signal.
An added probe needs an owner, consumer, collection point, meaning, runtime cost, sensitive-data
handling and appropriate lifetime. Avoid raw payload logging and unbounded metric cardinality.
Do not add a monitoring service or dashboard merely to display the skill's process.

Verify the signal follows the effect being claimed. "Queued" cannot stand in for "delivered";
"handler returned" cannot stand in for "persisted". Test the signal during relevant partial failure.
Instrumentation that reports success incorrectly creates another contract defect.

## Close with proof at the right level

Use the existing compiler/lint/build gates and focused tests appropriate to changed contracts.
Challenge the repaired case and relevant regressions, then exercise the terminal journey when
available. For a package/shared engine, check actual consuming imports and behavior, not only its
unit tests. A fake adapter needs a real-adapter or published-contract check before claiming that
integration works. Record unavailable environments precisely.

Review the actual final content and artifact; do not substitute HEAD for uncommitted source or a
running deployment. For a next-commit review, account for index/worktree differences and generated
files. Record finding closure only after the required proof; "implemented, verification blocked"
is a valid state. Retain unresolved impact, owner, recovery action and exact missing evidence.

For ideation, deliver mechanism, tradeoffs and the experiment-ready first slice. For review, deliver
supported findings or a bounded no-findings judgment. For implementation, deliver the working path
and checks. Mission-control visuals and ambitious proposals do not replace those outputs.
