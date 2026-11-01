# Pressure scenarios for does-it-make-sense

These are portable synthetic fixture inputs and summarized observations recorded on 2026-11-01
against the maintained local does-it-make-sense skill. They are historical evidence, not fresh evaluations
of this public release. Each case retains the original tested instruction hash and its verdict.
Raw host session reports, personal configuration and the host-specific fixture generator are
excluded. Suggested instruction edits in those cases are proposals; this release does not claim
they were all adopted or independently retested.

- [green-tests-unfinished-job](baseline-green-tests-unfinished-job.md)
- [refund-scope-authority](baseline-refund-scope-authority.md)

## Repeat a scenario

Copy the corresponding `fixtures/` directory into an isolated scratch workspace. Read its
`TASK.body.md` as the synthetic task. If comparing with/without skill behavior, use two pristine
copies, the same task and tools, and an explicitly authorized evaluation host. For the with-skill
arm supply the real installed `does-it-make-sense/SKILL.md` path and relevant references. Do not treat this
README as permission to spawn agents, install dependencies, download models or publish anything.
Ask each run to disclose instructions already in context and report changed files, checks and limits.
The fixtures intentionally contain failing tests or missing workflow connections; they are not
release-gate failures to fix in the template.

## Evidence limits

The original host imported DDD instructions and a UI reuse preference through global instructions.
Its DDD without-skill arm was therefore contaminated; UI baselines also had the reuse preference.
A baseline that already passes is not evidence that a skill prevented a failure. Use a clean
profile for causal comparisons and report partial results without turning them into efficacy claims.
Public Visualizer retains interactive/data/3D modes beyond the local video-only skill tested here.
