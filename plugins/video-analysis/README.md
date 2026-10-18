# SigmaStudioz Video Analysis

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version1.0.0.

Analyze supplied videos and audio through timestamped frames, adaptive inspection, transcripts and explicit evidence/coverage limits. By Lex from SigmaStudioz.

## Install

```sh
npx skills add sigmastudioz/agent-skills --skill video-analysis
```

Or register this repository as a Claude marketplace and select `video-analysis@sigmastudioz`.
The package includes Claude, Cursor and Codex manifests. Native directories require separate
review; repository availability does not mean this plugin is approved by any marketplace.
Normal skill discovery is enabled for relevant requests; installation does not rewrite global
settings or guarantee selection on every model, desktop or remote host.

## Capability and limits

This is an original, portable evolution of our local frames-plus-transcription workflow.
It supports native media understanding when available, or local FFmpeg sampling with recorded
presentation timestamps. It separates visible evidence, audible content, transcript hypotheses
and interpretation; sparse sampling is never advertised as exhaustive viewing.

The optional Python3.10+ sampler requires existing ffprobe/FFmpeg. It has no auto-installer,
model download, cloud fallback or transcription dependency. Whisper is optional; external
transcription and large model downloads need an appropriate user-authorized destination/budget.
See the skill references for commands, timing conventions and audio-only/partial-evidence cases.

## Example requests

No test account or paid API is required. Supply a short clip you own or may analyze, and a host
with native media input or local Python/FFmpeg. The following are reproducible review scenarios;
we have tested the sampler independently, not new-agent selection or every analysis outcome.

1. “Analyze my attached clip. Summarize the visible events with timestamps, report which ranges
   you inspected, and distinguish observations from interpretation.”
2. “Study the transition from 2 to 5 seconds in this clip. Inspect before/during/after frames,
   describe the motion and hierarchy, and propose an original reconstruction without copying assets.”
3. “Compare the spoken explanation with on-screen captions in this clip. Use audio only if you
   can actually inspect it; flag uncertain transcription, missing audio and any contradictions.”

## Evidence and support

See [the skill](skills/video-analysis/SKILL.md), [collection validation](../../docs/visual-skills-validation.md)
and [Privacy](../../PRIVACY.md). Packaging checks are distinct from fresh-agent efficacy.
Report issues without private media, credentials or transcripts. No universal performance or
automatic activation claim is made.
