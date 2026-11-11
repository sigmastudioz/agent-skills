# Montage, kinetic type and layered compositing

Read for rapid mixed-media edits, shape matches, portals, presenter-integrated type or editorial
collage. Use the existing [timed specification](reference-to-spec.md) and [sound workflow](sound-design.md).
This is production guidance, not a claim that bundled diagram primitives implement these effects.

## Choose the owner by the output

An authored montage or animated collage belongs in the video workflow, with separately produced
clips treated as assets. A cinematic appearance alone does not require a whole Blender scene.
Editing supplied presenter footage, speech captions and social packaging can use the separately
available Social Media Curator; hand off bespoke motion shots with asset IDs, source/output ranges,
alpha conventions, typography and audio anchors. Actual rigged subjects, changing perspective or
DCC-rendered films can use the separately available 3D Animator. Do not add 3D for a crop or flat
collage translation. Missing companions do not authorize installation.

## Resolve the edit before polishing assets

Inspect dense edits more frequently than their shortest meaningful insert and inspect important
transitions before/during/after. Large frame differences may be flashes, inversions or movement.
Keep inspected reference cuts distinct from semantic beat groups and proposed output cuts; use
decoded timestamps. Do not infer a beat grid without hearing audio. Preserve a calmer treatment
when required by the brief or audience rather than universalizing a rapid reference's pacing.

Prove scale changes, composition anchors and the payoff in a placeholder edit. Record each asset's
entry/action/exit state. Align shape matches by screen-space center, radius, silhouette and movement
direction. Similar colors alone do not make a convincing match.

## Specify motion and layers

Extend the shot with asset/layer IDs, masks, z-order, alpha/premultiplication convention, transforms,
subject motion, camera motion, effect envelopes and overlap. Layers use the same master timeline.
Check actual renderer support before committing; a new instruction does not supply a new engine.

| Mechanism | Production decision | Review target |
| --- | --- | --- |
| Iris/object portal | Track the opening, reveal the next scene inside its matte, then push until it fills the frame | Edges and continuity across the handoff |
| Forward travel | Separate near/far particles and occluders; use changing perspective or a suitable motion clip | Depth survives motion; a wallpaper zoom is not equivalent |
| Growth/reaching gesture | Use actual source motion, temporal mattes, animation or a rig when the pose changes | First/action/end poses; global zoom cannot supply articulation |
| Light climax | Separate core, rays, spill and exposure; attach light to its visible cause | Subject readable before climax; correct growth and decay |
| Type behind a moving person | Original footage, temporal matte, rear type, foreground subject and intentional front-type exceptions | Hair/finger edges, placement and readable phrase holds |
| Paper collage | Cutouts, texture, edges, shadows and independent pieces governed by one anchor frame | Consistent edge/shadow scale, motivated motion and exact copy |

Distinguish speech subtitles from authored display type. Preserve exact copy and anchors in a
controlled overlay; reveal by meaning, select emphasis deliberately and allow a readable hold.
A font or tracking option does not establish a helper's temporal segmentation capability.

## Prove the difficult passage

Make a short motion study of the hardest transition before producing every asset. Compare actual
source/output times, silhouette, scale, pose, occlusion, glow area and entry/exit states; then
review normal-speed motion and encoded sound. A matching still or valid encode does not prove
articulation, moving mattes or synchronization. Keep technical, creative and listening checks
separate. Private reference media, creator identities, exact durations and recipes stay in projects.

## Real human motion and frame-accurate handoff

Choose the source medium for the requested result. Photorealistic hand motion needs suitable
filmed/generated footage or a reviewed anatomical rig with skin, joints, nails and lighting.
A photograph with a global transform, a puppet warp or a capsule outline is a different treatment.
Inspect fingers, thumb placement, joint bends and contact at first/action/end poses and between
them; reject changing finger counts, fused contours and slipping light attachment. Keep any flare
separate until the anatomy reads, or review it both with and without the flare.

A moving presenter requires actual changing poses and a matte that changes with them. An original
synthetic presenter is valid when appropriate to the brief; preserve its identity and keep exact
words in controlled typography. Do not infer speech or lip sync from a silent performance. For a
controlled green-screen source, key every decoded frame and inspect hair, fingers, green spill,
face color and type occlusion over both light and dark backgrounds. Keying is not arbitrary-background
person segmentation. Green spill may survive on fully opaque hair pixels, so an alpha-edge-only
despill can leave a colored rim; review and correct contaminated foreground color as well. Keep
source cadence distinct from export cadence: ordinary resampling can repeat/drop frames and is
not optical-flow interpolation. Footage with green clothing, mixed backgrounds or unstable lighting needs
another reviewed matte method. The separately available Social Media Curator's
`references/presenter-and-collage.md` documents its local frame-preparation helper when installed.

Bind source ranges, frame rate and alpha convention to the master timeline. For a browser/canvas
renderer, await the chosen frame's decode at each explicit seek before drawing, including random
and backward seeks; a playback clock or an asynchronously replaced image can encode stale frames.
Update silhouette mattes from that same frame. Fail on missing/incomplete source frames instead of
falling back to a still cutout. Bound the frame cache rather than preloading an entire high-resolution
sequence. Preserve the requested film duration and soundtrack; a short inserted shot does not require
stretching or looping the whole film. Record any intentional still holds as editorial choices.

Verify temporal asset preparation, source quality, actual compositing, encoded playback and user
acceptance separately. A synthetic green-screen shape test can prove mechanics but cannot validate
human anatomy, hair edges, identity or performance. Prepared prompts and a cost quote do not prove
that a motion source exists; obtain any required spending/upload approval before that step.


## Commercial and speech-led motion handoff

For bespoke motion shots in a product spot or speech-led montage, retain the existing timed spec.
Add the shot's job (problem, reveal, demonstrated benefit or payoff), exact display copy, source
ranges, panel/crop anchors, matte owner and sound onset. Keep product claims bound to evidence;
a visual treatment does not prove a feature. Separate authored display type from speech subtitles.
Match cuts need corresponding screen-space shape/size/direction. Blur needs an anchor, peak and
sharp recovery; a flash or whoosh is not a substitute for a motivated cut. Review the difficult
transition before committing the whole sequence, with a lower-stimulation variant when appropriate.

The separately available Social Media Curator owns footage selection, commercial treatment,
speech-led editing and packaging; its commercial-and-montage and delivery references provide
those handoffs when installed. Return asset IDs, source/output times, cadence, alpha convention,
exact copy and audio anchors for the final edit. Do not claim a new bundled recipe or NLE/model
integration merely because a reference describes it. Use the existing supported rendering path.
Verify the final encoded file against an explicit delivery contract and inspect picture/sound;
a fixed bitrate or Full-range switch is not a universal quality upgrade. Keep private creator
identities, media and exact reference recipes with the project.
