# Beat maps and word timing

By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Read this when cuts, reveals or captions must land on music or on spoken words. It extends the
[sound-design pass](sound-design.md) and the measured-audio rules in [media in 3D](media-in-3d.md);
it does not replace them. The standing rule still holds: no beat grid without measured or
actually heard audio. A guessed BPM is an assumption and must be labelled as one.

## Beat map

1. Choose the actual track revision (hash it). Measure onsets and downbeats with the tools
   available on the host (an audio-analysis library, or an FFmpeg-based envelope as in
   [media in 3D](media-in-3d.md)). Do not copy a BPM from a caption or a reference video.
2. Record `bpm`, first-downbeat `offset` in seconds, time signature if known, a confidence value
   and the method in `beatmap.json` next to the scene source, on the master timeline.
3. Snap hard cuts and hero reveals to downbeats. Put minor accents (type pops, small transforms)
   on off-beats or subdivisions. Leave some beats unmarked: not every beat needs an event.
4. When the track's tempo drifts, store measured beat times instead of a constant grid.
5. Review at normal speed with sound. Report drift in frames; under one frame is the target.

## Word timing

The workflow already emits scene-level captions (one cue per scene, see
[storyboards](storyboards.md)). Word timing is the finer layer for word-highlight captions and
per-word reveals.

1. Start from approved narration text. Align it to the recorded or synthesised audio with an
   available forced-alignment or word-timestamp transcription tool. If no tool is available, say
   so and keep scene-level captions.
2. Store `words.json` (word, start, end, scene ID) on the same master clock as the beat map.
3. Derive caption chips, per-word highlights and per-word type reveals from that file. Do not
   hand-tune word times independently in two places.
4. Check a sample of words against the waveform or by listening; transcription timestamps can
   be late on plosives and early on soft onsets.

## Verification

Carry the beat map and word file into the export trace. Spot-check at least the first cut, the
hero reveal and the last cut against the decoded audio. Report which checks were listening and
which were structural.
