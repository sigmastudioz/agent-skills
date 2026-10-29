# Sound-design pass

Read for a film with audio, after a rough picture edit and before final export. Start
the cue sheet during storyboarding; resolve it against the actual render. Honor a
silent brief. Success is clearer meaning, emphasis or rhythm, not more effects.

## Establish what needs sound

Inspect existing audio and available narration, music and SFX stems. Record what must
stay, the picture revision, duration, time origin and actual frame rate/time base.
Identify a small, coherent palette that fits the subject and materials. Preserve
approved music and voices; do not clone a reference presenter.

For each important event, decide whether sound explains contact, movement, a state
change, tension or resolution. Record intentional silence too. Do not sound every
cut, character, cursor move or detected motion. Detection and beat grids propose
candidates; inspect the picture before accepting them. Repeated effects should not
compete with reading, narration or the main payoff. Silence is a valid final choice.

## Keep an editable cue sheet

Use the project's existing timeline/cue format rather than introducing a second
timeline. Keep enough fields to reproduce and review each decision:

| Field | Meaning |
| --- | --- |
| Identity | Stable cue and scene/event IDs; source picture revision/hash |
| Intent | Visual cause, explanatory purpose, priority and sound family, or reason for silence |
| Picture target | Event time or frame plus its time base; use presentation timestamps for variable-frame-rate input |
| Placement | Audible onset, peak or end anchor; intentional lead/lag; resolved file-start time and duration |
| Asset | Local file/hash, original recording or generated recipe/seed/tool revision; source and rights record |
| Treatment | Trim, stretch/pitch if used, gain in dB, fades, pan and bus/ducking choice |
| Review | Measured offset from the intended anchor, listening status, accepted choice or unresolved issue |

A contact can align to an audible attack, a whoosh to the movement's apex, and a
riser's end to the reveal. The file boundary is not necessarily its audible anchor.
Allow motivated anticipation and trailing decay instead of forcing every sound's
start onto a cut. Compute placement after trimming/stretching:

`file start = picture event + intentional offset - processed asset anchor`

For example, an event at 2.000 s with a 0.320 s whoosh peak starts that file at
1.680 s when no offset is intended. Retain audio sample precision; do not promise
subframe visual accuracy beyond the picture's resolution. Handle pre-roll and final
tails explicitly; do not silently truncate a negative start or cut off a decay.

After picture or narration changes, re-resolve cues, captions and ducking against
that revision. Compare imported/resolved cue times with the source; a tool's JSON
schema is an adapter contract, not permission to overwrite hand-edited decisions.

## Choose and clear assets

Prefer suitable approved/local assets first. Search externally when useful; generate
only when it fits the brief and closes a real gap. Recorded foley and synthesized
effects are both options, with truthful labels. If neither fits, leave the event
quiet and report the omission. Read [verified tool options](sound-tools.md) when
choosing Openverse, Real SFX or Earshot; none is a required dependency.

For each external asset retain title/creator, original item page, download URL,
license/version/link, required credit, access date, local hash and any modifications.
Check the original item's terms for the intended commercial use, adaptation and
redistribution. Search filters and a tool's software license do not clear the audio.
Unclear rights mean omit/replace that asset, not invent a license. Keep credits with
the deliverable; include source media only where its terms permit redistribution.
For generated sounds record the recipe, seed, version and any input recording's
rights. Synthesis or fitting does not erase obligations on source material.

## Mix without damaging the original

Work into new outputs. Keep narration, music, ambience and effects separate where
available; preserve the approved base. Check for effects already baked into it to
avoid doubling. Prefer a clean stem/re-render when replacing effects. Do not assume
that arbitrary SFX can be removed cleanly from a combined voice/music track; retain
the original and report the limitation when stems are unavailable.

Set a hierarchy: speech first when the explanation relies on narration, then the
important accents, with music/ambience supporting them. Adjust gain, duration,
frequency balance and fades; automate or duck music/effects under speech where
needed. Do not apply a music-led tool's “duck original under effects” option as if it
protected speech. Use the actual speech stem/regions where available. Avoid pumping,
harsh repeated transients, excessive bass, masked words and phase-cancelling stereo.
Use restrained panning and inspect the mono fold-down. A quiet film need not grow a
music bed, and an approved music-led film need not gain narration.

Measure integrated loudness, true peak and relevant dynamics on the final decoded
export, using a suitable meter such as FFmpeg's loudness filters or an available
verified measurement tool. Choose and state a target for the actual destination;
do not impose a universal LUFS value or call a sample-peak reading true peak. Check
the encoded result again after gain, limiting or codec changes. Match sample rates,
duration and start offsets during muxing; verify start/middle/end sync and tails.

## Review against the goal and finish

Render a representative section covering speech, a fast event and the payoff before
a long export. Compare the added-effects version with the same approved base without
them, keeping voice/music levels comparable. Include silence or an alternative cue
when a choice is uncertain. Check whether each addition clarifies the action, adds
useful emphasis or improves rhythm; remove distracting additions rather than filling
holes to satisfy an event-density score.

Inspect cue anchors against nearby frames and the processed audio envelope. Listen
to the full final export when a listening-capable tool or reviewer is available,
including transitions, dense passages, speech and the ending. Check mono and a small
speaker/phone preview where available. Correct only evidenced failures, then recheck
the affected passage and final export. Stop when the brief and checks are met; do
not expand the video or keep adding layers to chase a score.

Separate file/decode checks, timing/loudness measurements, model-assisted descriptions
and actual listening. ASR, waveforms and a “passed” critique do not establish taste,
emotional fit, intelligible pronunciation or a human listening review. If listening
is unavailable, identify timestamped moments and specific questions for the reviewer;
keep creative approval and unreviewed audio explicit.

Deliver the playable video, editable cue sheet, rights/credits manifest, reproduction
command and separate SFX WAV/stems when relevant. Trace cue → asset/recipe → processed
anchor → mix → muxed export and disclose missing tools, skipped cues, unclear rights
or unchecked playback. A failed search or tool must not be presented as successful
sound design. Preserve project media and notes outside the installed skill.
