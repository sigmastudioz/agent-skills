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
   Smooth the energy over about 10 ms and set an energy floor, or decaying kicks and clicks in
   near-silence register as extra beats (a first pass read 732 BPM on a 120 BPM track).
2. Record `bpm`, first-downbeat `offset` in seconds, time signature if known, a confidence value
   and the method in `beatmap.json` next to the scene source, on the master timeline.
3. Snap hard cuts and hero reveals to downbeats, quantised to the nearest frame (evaluate each
   frame at its centre), not the next frame. Put minor accents (type pops, small transforms)
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

## Frozen-subject beat build

A still or near-still hero carries a music piece when everything around it moves on the measured
beat map. Seen in a reviewed audiovisual opening (one figure in one pose, 120 BPM). Tested
2026-11-18 on a 15 s code-rendered demo: all 8 hard cuts within 0.15 frame of the measured beats.
Cut-ownership index: `video-editor` signature-moves #57; layer/subdivision recipe stays here.

1. Freeze the subject; give each layer around it its own subdivision from `beatmap.json`:
   geometry or density changes on eighths (show the rebuild as glowing wireframe), surface or
   material swaps only on hard cuts, light pulses on each beat (for example travelling down
   cables into the subject). Decide whether a pulse *arrives* on the beat or *leaves* on it, and
   write it down.
2. Escalate by subdivision rather than by speed: frame shake on quarters, then eighths, then
   sixteenths into the drop.
3. Let the camera do the travelling: skim along the surface (up an arm, neck to jaw, down the
   spine), then one pull-back on the drop that reveals the subject's place in the wider scene. On
   a flat 2D subject the skim reads as a pan; add depth or parallax.
4. Never repeat a title entrance: assign one transform per hit (slice, stretch, flip, shatter,
   melt, colour split) from a list, so the sequence varies by design. Make the list at least as
   long as the number of hits; add transforms rather than repeat one.
5. Place cuts backward from the beat grid (start from the drop and the downbeats, then fill),
   then verify as below.

## Hit / gap motif gate

On producer teasers: live picture on hits; one reused abstract motif on every silence hole (about
1.8 s when regular). Irregular gaps weaken the brand more than trough inserts alone. Cut timing
and brightest-on-hit placement stay with `video-editor` (see signature-moves #3); campaign
packaging with `record-label`. Motif design stays here.
*Evidence:* hanzbeats Dd_IJtjgOZf vs DdyXRbsAEyS. **Shown.**

## Verification

Carry the beat map and word file into the export trace. Spot-check at least the first cut, the
hero reveal and the last cut against the decoded audio. Report which checks were listening and
which were structural.

A check of picture against the cue sheet cannot detect shifted audio: also measure the
soundtrack's placement in the file, with a control shifted by FFmpeg `adelay` (an `-itsoffset`
control on a copied video stream under-shifted in testing).
