# Pressure scenarios for visualizer

These are portable synthetic fixture inputs and summarized observations recorded on 2026-11-01
against the maintained local visualization-videos skill. They are historical evidence, not fresh evaluations
of this public release. Each case retains the original tested instruction hash and its verdict.
Raw host session reports, personal configuration and the host-specific fixture generator are
excluded. Suggested instruction edits in those cases are proposals; this release does not claim
they were all adopted or independently retested.

- [reference-copy-request](baseline-reference-copy-request.md)
- [verify-and-voice](baseline-verify-and-voice.md)

## Repeat a scenario

Copy the corresponding `fixtures/` directory into an isolated scratch workspace. Read its
`TASK.body.md` as the synthetic task. If comparing with/without skill behavior, use two pristine
copies, the same task and tools, and an explicitly authorized evaluation host. For the with-skill
arm supply the real installed `visualizer/SKILL.md` path and relevant references. Do not treat this
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

The video fixtures omit binary media. In the copied `viz-reference/reference/` folder, FFmpeg can
create the declared 10-second 1080x1920 test-pattern MP4 with a 440 Hz tone; it represents synthetic
reference media, not an actual competitor. For `viz-verify`, recreate the declared stale silent
720x1280 eight-second `out/demo.mp4` and a four-second tone at `reference/narrator-sample.mp3`.
These tones are not human voices. Copy this package's `scripts/render.py` and `requirements.txt`
to the fixture's `tools/` folder before running its renderer.
