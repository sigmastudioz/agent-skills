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

## Evidence and support

See [the skill](skills/video-analysis/SKILL.md), [collection validation](../../docs/visual-skills-validation.md)
and [data handling](../../PRIVACY.md). Packaging checks are distinct from fresh-agent efficacy.
Report issues without private media, credentials or transcripts. No universal performance or
automatic activation claim is made.
