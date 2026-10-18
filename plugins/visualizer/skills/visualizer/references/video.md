# Visualization video, motion and sound

## Story and timeline
Write timed beats with picture, copy, evidence, motion, sound and explanatory purpose. A useful
arc is hook → context → mechanism → tension → repair/reveal → proof → next action; shorten it when
appropriate. Give each shot one dominant action and enough settled time for important labels.
An animated replay must be labeled as such. Never fabricate live terminals, test results or demos.

Use stable scene/event IDs and one clock for picture, captions and sound. Define frame rate,
duration, boundary behavior and frame count. Calculate state from absolute time for seek/export;
avoid accumulating animation deltas that make paused seeks or out-of-order frames incorrect.
For interactive-to-film conversion, record the scenario, seed and meaningful control events.
Hide unused UI only in the film adapter; retain the same model and evidence.

Animate the mechanism: assemble, connect, travel, interrupt, repair, hand off and resolve. Preserve
object identity, screen direction and spatial anchors across shots. Use anticipation, contact,
follow-through, secondary motion and holds; smooth motion is not constant motion.
Use motivated wipes, match movement or a reveal led by the subject. Do not transition every shot
with unrelated effects. Check first/last frames and contact points, not just attractive stills.

Recompose portrait/landscape layouts instead of cropping away labels or attribution. Measure
font metrics, safe areas and wrapping; inspect phone-sized playback and full export resolution.
More effects cannot repair weak hierarchy, excessive copy or a confusing causal sequence.

## Sound with material and causality
Build a cue sheet: event ID, time, visual cause, sound family, duration, level and stereo position.
Use a coherent score, tactile foreground effects, subtle environment and optional authorized
narration. A repeating tone is a scratch track, not a rich finished mix.
Use variation and silence: friction for motion, soft contact for connection, tension for a break,
and resolution for recovery. Label synthetic effects accurately; do not call them recorded foley.
Pan with restrained screen direction; keep essential meaning understandable in mono and picture.
Duck music for speech or meaningful interruptions. Measure the final encoded loudness/true peak
against the destination's requirements and listen for clipping, harshness, masking and repetitive
hits. Report actual measurements separately from listening review.
Use original/licensed/authorized audio. Never clone a reference presenter without permission.
Without narration, on-screen labels/captions must still explain the film. Distinguish scene-summary
captions from speech transcripts. Preserve timing, language and a clearly identified translation.

Preview controls may include play/pause, replay, seek, chapters, mute and volume. Actual control
feedback starts after user input and honors mute. Baked event cues do not make an MP4 interactive.
Preserve time and playback/mute state when changing aspect ratio or effects. Seek after metadata
is ready; verify paused seeking and end/replay behavior. Release temporary audio/video resources.

## Encode and deliver
Reuse the project's renderer. For new code, own storyboard/model, layout, assets, renderer and
encoder separately at the smallest useful scope. Stream frames and bound buffers; use argument
arrays for subprocesses. Detect render/encoder failures and incomplete frames. Preserve the prior
output until a staged export passes validation; avoid overwriting source or evidence files.
Render at explicit frame times. A 60fps container with duplicated 30fps poses does not establish
smoother source motion; deliberate cel holds are valid when chosen and documented.
Use a compatible codec/container and color pipeline for the destination. Keep high-quality master
and delivery derivatives distinct. Copy encoded audio when appropriate to avoid unnecessary loss.

Decode the complete export, then verify dimensions, duration, FPS, frame count, audio, captions,
orientation, safe areas and representative transitions. Inspect rich textures after compression.
Retain reproduction commands, dependency versions, asset licenses and editable scene/timeline data.

## Inline playback and public delivery
Check the actual destination renderer: a Markdown image linking to an MP4 is a poster link.
On GitHub, upload an authorized MP4 through the Markdown attachment control, use its returned
stable attachment URL, and preview the resulting player before committing. Verify current file
limits and codecs; use a smaller delivery derivative when needed, preserving the full download.
Do not store expiring signed CDN URLs in source. Verify the public page without relying on the
publisher's session: player controls, media readiness, duration and actual time advancement.
Keep captions, source downloads and a fallback link. Record upload versus commit versus live
verification separately; stop/recover when another user controls the browser. Social launch drafts
remain unsent until authorized. A public repository is not a marketplace approval.
