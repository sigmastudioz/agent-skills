# Pressure scenarios for domain-driven-design

These are historical scenario summaries and observations recorded on 2026-11-01
against the maintained local domain-driven-design skill. They are historical evidence, not fresh evaluations
of this public release. Each case retains the original tested instruction hash and its verdict.
Raw host session reports, personal configuration and the host-specific fixture generator are
excluded. Suggested instruction edits in those cases are proposals; this release does not claim
they were all adopted or independently retested.

- [delegation-brief](baseline-delegation-brief.md)
- [quick-fix-shared-formatter](baseline-quick-fix-shared-formatter.md)
- [observed-cli-delegation](observed-cli-delegation.md) (observed in a real session, 2026-11-12)
- [batch-review coordination](observed-batch-review-coordination.md) (observed in a real session, 2026-11-12)

## Repeat a scenario

The executable fixtures live in the collection’s [test area](https://github.com/sigmastudioz/agent-skills/tree/main/tests/fixtures/domain-driven-design),
outside the installable plugin. Copy the corresponding fixture into an isolated scratch workspace. Read its
`TASK.body.md` as the synthetic task. If comparing with/without skill behavior, use two pristine
copies, the same task and tools, and an explicitly authorized evaluation host. For the with-skill
arm supply the real installed `domain-driven-design/SKILL.md` path and relevant references. Do not treat this
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

The recorded cases below retain their original fixture paths and instruction hashes.
Their historical paths refer to the recorded run; use the collection test area for a new run.
