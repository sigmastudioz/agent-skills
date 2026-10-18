# Visual skill validation and scope

By Lex from SigmaStudioz. Candidates: **Visualizer1.0.0** and **Video Analysis1.0.0**.
Both are original MIT packages. Visualizer combines interactive visuals and video generation in
one skill; Video Analysis is separate and can supply an evidence brief to it. Neither requires
the other to be installed. Existing Principal Driven Domain Design1.0.7 is unchanged.

## What is implemented

Visualizer routes to interactive, data, video/sound, rendering/shader and verification references.
It defines a shared model/time contract for interactive and film consumers, purpose-driven art
direction, accessible controls, truthful data, original/licensed sound, delivery checks and gap traces.
There is no automatic renderer install, telemetry, paid job, skill-to-skill dependency or global
configuration rewrite. Available project/host tools determine supported render and export paths.

Video Analysis evolves the local frame-plus-transcription workflow with capability detection,
actual presentation timestamps, stream/orientation handling, adaptive evidence coverage and honest
audio/transcript limits. Its optional standard-library Python sampler calls installed local
FFmpeg/ffprobe; it has no shell-eval wrapper, global installer, model download or cloud fallback.
The older local self-installing script is not redistributed. Whisper remains an optional tool.

## Evidence categories

Package/schema checks, media-helper runtime tests and fresh-agent selection/efficacy are different
claims. The first two can be tested locally. No fresh Claude/Cursor/Codex agent-selection test has
yet been run for these new skills; no universal automatic-activation claim is made.
The earlier DDD coding-test results do not transfer to these packages.

The published DDD film/preview informed the visualization guidance: Three.js material processing,
controls/fallback, original synchronized sound and a verified video export. Those historical checks
are not relabeled as tests of the new unified skill or a native 3D scene generator.

## Sampler runtime checks

Run `python3 -B -m unittest discover -s tests -p test_video_analysis.py -v` with FFmpeg/ffprobe.
Fixtures are synthetic; none contain private user videos, transcripts or third-party reference art.
Cases cover source preservation/hash, bounded sample counts, actual PTS, window offsets, nonzero
stream start, variable-rate timestamps, rotated display, audio-only, default/explicit video tracks,
corrupt input, existing output, invalid ranges/streams and missing decoder with atomic cleanup.

A VFR fixture exposed misleading container duration shorter than its presentation timeline.
The helper now scans packet timing separately before selecting the default range; reported and
packet durations are both retained. A rotation fixture initially lacked a display matrix; it was
corrected to carry actual90-degree metadata before testing autorotation. Packet scanning is not
a full-decode claim. Sparse samples still require explicit ending/detail inspection.

## Connected-path trace

| ID | Path and consumer | Evidence/status | Remaining boundary |
| --- | --- | --- | --- |
| VIS-01 | Request → mode routing → relevant reference → artifact contract | Static review; all local references linked | Fresh host selection untested |
| VIS-02 | Data/model → interaction/view → snapshot/timeline → film adapter | Explicit shared-contract guidance; static-only for new skill | Artifact quality needs actual task execution |
| VIS-03 | References → original art/sound → render/export → public player | Historical demo pipeline and inline-player check; guidance reviewed | Not a new 3D/runtime efficacy test |
| VA-01 | CLI → source hash/probe → stream/time choice → decoded frames → inventory | Synthetic runtime tests | Native host perception/transcription not exercised |
| VA-02 | Packet timeline → sampling → source-relative timestamps → evidence citations | VFR/nonzero-origin/window regression tests | Sparse coverage; full media semantics not inferred |
| VA-03 | Invalid input/tool/decode/output → failure → cleanup | Runtime failure-path tests | External model/provider failures outside helper |
| PUB-01 | catalog registry → native manifests → three catalogs → package hashes | Generator drift checks and catalog tests | Native marketplace review is separate |

## Reproduce package checks

```sh
python3 tools/build_catalogs.py
python3 tools/build_catalogs.py --check
python3 -B -m unittest discover -s tests
claude plugin validate .
```

Run the host's skill frontmatter validator on each skill directory. Verify the current official
Cursor plugin/catalog schemas and retained Codex/Claude manifest conventions before submission.
Keep any validator warnings, dependency failures and skipped checks in the task's release receipt.
Package line budgets and linked references are mechanical checks, not semantic efficacy scores.

## Publication and marketplace state

Direct repository packaging is distinct from Claude, Cursor, Codex or Antigravity approval.
Use separate application/scan records for each new plugin, original icons, visible Lex attribution,
accurate descriptions and relevant keywords. Do not reuse DDD approval, support cases or listing IDs.
No new marketplace approval, fresh-host activation, platform-wide performance or ranking is claimed.
