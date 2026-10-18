# SigmaStudioz Video Analysis

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version1.0.0.

Analyze supplied videos and audio through timestamped frames, adaptive inspection, transcripts and explicit evidence/coverage limits. By Lex from SigmaStudioz.

## Watch the demo

https://github.com/user-attachments/assets/63d7d3cb-c85c-4cb8-910d-664a97a7ab8f

A 32-second film by **Lex from SigmaStudioz**: turn a source clip into timestamped
evidence, connect observations to actual frames, and make coverage limits clear.
Three.js shader animation and an original stereo score present the workflow in 1080p60.

[Download MP4](../../assets/video-analysis-demo.mp4?raw=true) ·
[Captions: SRT](../../assets/video-analysis-demo.srt) / [VTT](../../assets/video-analysis-demo.vtt) ·
[Poster](../../assets/video-analysis-demo-poster.png) ·
[Editable sources for both demos](../../assets/visual-skills-demo-source.zip?raw=true)

The film shows six actual timestamped frames from our original six-second synthetic clip.
The released sampler returned eleven frames within a twelve-frame budget. Sparse samples
do not establish exhaustive viewing or audio understanding. This is an authored demonstration,
not a fresh agent session. Captions are timed scene summaries; there is no voiceover.
[Reproduce the preview and inspect export checks](../../assets/README.md#visualizer-and-video-analysis-films).

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
