# Principal Driven Domain Design

By [Lex from SigmaStudioz](https://github.com/sigmastudioz). Version **1.2.0**, [MIT](LICENSE).

**Principal-level domain-driven design for AI coding agents.**

Build features that fit the codebase—and trace the connections that make them work.
An engineering baseline for application, API, worker and monorepo changes. Group
code by its owning domain, then by function; keep services and shared modules at the narrowest
useful scope. Reuse an owned engine when real consumers share a cohesive algorithm. Trace modules
through callers, dependencies, consumers and failures, and fix gaps required by the authorized task.

The instruction file has **405 lines**; the complete skill folder has **1348 lines**, including
the architecture reference, metadata, optional Python helper and its regression tests. Small fixes stay small; read-only reviews stay read-only.
The baseline does not authorize extra agents, unrelated restructuring or deployment.

## What it helps agents do

- Put code with the domain that owns it, then group services and shared modules by function.
- Reuse cohesive engines across real consumers without creating a catch-all framework.
- Follow callers, dependencies, consumers and failure paths to find and repair required gaps.
- Give authorized teammates explicit ownership, contracts and evidence for integration.

- Check consumer, contract, registration, cadence, compatibility and staged-snapshot edges.
- Disprove candidate findings against earlier revisions and real callers before reporting them.

## Setup and handoffs

Install this plugin from the SigmaStudioz catalog. For global automatic use without trigger words,
follow the one-time [native setup](https://github.com/sigmastudioz/agent-skills/blob/main/SETUP.md).
Marketplace discovery alone does not install global instructions or enable lifecycle hooks.

Pass an accessible baseline, workspace/revision, ownership, contracts, current state, evidence,
trace obligations, checks and expected return format to already-authorized teammates. Verify the
integrated result. Task briefs and pseudocode are proposals, not proof of algorithm correctness.
User teammate limits override optional workflow steps, including extra review agents.

The optional Claude helper validates handoff structure and adds a compact reminder to read the
installed baseline and relevant linked guidance. It recognizes more coding workspaces, rejects
malformed inputs, and preserves cumulative explicit agent budgets across repeated limits. Only an
explicit new-budget instruction resets usage. Quoted or negated examples cannot expand a limit;
resuming an existing worker does not allocate another slot. A different workspace needs explicit
isolation confirmation. Missing history, unrecognized wording, actual isolation authority and
semantic correctness remain the coordinator's responsibility. Requires Python 3.

## Validation

Version 1.2.0 publishes the final user-maintained source: tracker-first evidence retention and safe
archival, corrected cadence and verification rules, repository ownership and conditional architecture guidance, and clearer
handoff safeguards. The packaged guard has **51 subprocess regression tests**. The UI metadata is
unchanged. No fresh native-agent efficacy run was performed for 1.2.0; the native coding evidence
below belongs to 1.0.5 and its earlier full-baseline guard. Package tests do not establish model
adherence or marketplace activation. The earlier 567/666-line 1.1.0 and 597-line receipts remain
historical; this release's complete skill folder contains 1348 lines.

Fresh Claude Code 1.0.5 test: **16/16 external feature checks and 2/2 original regressions pass**,
with exactly one implementation teammate. The parent integrated the isolated worktree result,
ran 20 local tests, reviewed authority paths itself and fixed a forged-tenant field bug.
Compound identity uses a JSON tuple instead of a separator, including NUL.

The test used normal global configuration with the optional handoff helper and an ordinary prompt
that did not name the skill. The actual worker received the complete baseline before the assignment.
Historical guard tests: 21; installer tests: 14. See the
[validation receipt](https://github.com/sigmastudioz/agent-skills/blob/main/docs/validation.json).
Earlier failed Claude runs remain recorded. The earlier passing Cursor CLI evidence is tied to
its original baseline; no new Cursor desktop or 1.0.5 coding result is implied.

Production performance, durable payment concurrency and remote/cloud adherence are outside this
small fixture. Local installation does not establish universal behavior across models or hosts.

## Example

An ordinary request such as “Add invoice refunds to the API and retry worker” should make the
agent inspect the billing domain, reuse a shared billing service, wire both consumers, and trace
retry, authorization and persistence paths. Automatic application requires the native setup above.

## Data and support

No publisher-hosted service, telemetry or automatic usage upload is included. The optional helper
reads the host-provided transcript locally; the agent provider handles prompts according to user
settings. See [data handling](https://github.com/sigmastudioz/agent-skills/blob/main/PRIVACY.md).
Support: [GitHub Issues](https://github.com/sigmastudioz/agent-skills/issues). Do not post secrets,
private code or raw session logs. The MIT copyright notice credits Lex from SigmaStudioz.
