# Principal Driven Domain Design

By [Lex from SigmaStudioz](https://github.com/sigmastudioz). Version **1.4.5**, [MIT](LICENSE).

**Principal-level domain-driven design for AI coding agents.**

Build features that fit the codebase—and trace the connections that make them work.
An engineering baseline for application, API, worker and monorepo changes. Group
code by its owning domain, then by function; keep services and shared modules at the narrowest
useful scope. Reuse an owned engine when real consumers share a cohesive algorithm. Trace modules
through callers, dependencies, consumers and failures, and fix gaps required by the authorized task.

The short entrypoint routes conditional architecture, handoff, gap-tracing, record and verification
rules into focused references. Small fixes stay small; read-only reviews stay read-only.
The baseline does not authorize extra agents, unrelated restructuring or deployment.


## Changes in 1.4.4

Batch handoffs now distinguish source advice, exact-output acceptance and consumer verification;
check copied input roles before dispatch; reconcile all assigned reviews before a limited correction;
and carry changed user requirements, cumulative attempts and stage-specific queue counts forward.
Read-only reviewers may use isolated input packets while write-capable workers retain checkout and
resource ownership boundaries. The optional guard and its schema are unchanged. A sanitized observed
case is included; no fresh native-agent efficacy result is claimed.

## Changes in 1.4.3

Handoffs now cover agent CLIs started from a shell (the guard doesn't see them, so the brief carries every field; sandboxed modes; worktree isolation), labelling cited code as a pattern to copy or a component to reuse, and reporting back up the chain: progress lines, `BLOCKED` questions forwarded to the decision owner, and reviewed results relayed to whoever delegated. One observed case is recorded in the tests folder.

## Changes in 1.4.2

Verification now covers local fakes of external services (fast, deterministic iteration, with one check against the real adapter or contract) and keeping agent instruction files lean by removing rules that newer models make redundant.

## Changes in 1.4.1

Handoff briefs now state the exact command and output behind each library or runtime claim, and briefs written for people carry the same handoff fields in prose.

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

## Changes and validation

Version 1.4.0 preserves the project-record convention and engineering safeguards while splitting
conditional guidance out of the entrypoint. The optional guard recognizes common coding requests
and the supported desktop session tool's offer/proposal/start phases. Starts consume the existing
cumulative budget; proposals carry a validated handoff without consuming a slot. The documented
hook matcher includes this tool. Noncoding prose requests remain outside the handoff contract.
The helper cannot validate host permissions, actual isolated-checkout authority or every possible
wording; those remain coordinator responsibilities.

[Pressure scenarios](skills/domain-driven-design/tests/README.md) link to portable synthetic
inputs in the collection test area and retain historical comparisons. The original DDD baseline already had the skill text in
context, so those records cannot establish causal efficacy. Raw host sessions are not distributed.
Fresh native-agent evaluation was not run for 1.4.0. The historical coding evidence below remains
tied to 1.0.5, and automated guard/package checks do not establish model adherence or marketplace
activation.

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

## Distribution boundary

The runtime skill retains its guidance and functional helpers. Executable synthetic evaluation
fixtures live in the collection’s [test area](https://github.com/sigmastudioz/agent-skills/tree/main/tests/fixtures/domain-driven-design), outside this installable plugin.
Historical scenario summaries retain their original dates and hashes. This packaging change does
not establish Anthropic organization verification or clearance of separate directory findings.
