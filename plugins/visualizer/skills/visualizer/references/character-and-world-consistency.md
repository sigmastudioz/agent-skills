# Consistent characters and worlds

Use for illustrated explainers, narrative reconstructions or character-led sequences in which
separately produced shots must depict the same people, props and place. Extend the existing
[timed specification](reference-to-spec.md); keep one shot list and asset inventory. This workflow
can use drawn, filmed, rigged or authorized generated assets. It does not supply a generation
account or extend the skill to every kind of cinematic production.

## Establish what survives a cut

Keep a compact visual-world record in the project. State palette, silhouette/shape language,
material/brush texture, motivated light sources, time of day, atmosphere and permitted variation.
Separate fixed identity from changes the story requires: a beacon lighting can change its spill;
it should not silently change the character's age, clothing or the surrounding geography.

For recurring subjects and locations, retain stable IDs and reviewable anchors:

| Record | Useful anchors | Important distinction |
| --- | --- | --- |
| Character | Face, proportions, hair, costume, identifying accessories, expressive range; views needed by the actual shots | A multi-view character sheet establishes identity, not the film's starting composition |
| Prop | Shape, scale, color/markings, material, owner and carrying/operating hand | Track transfers explicitly; do not mirror a shot to conceal a handedness error |
| Location | Landmark positions, paths, scale, entrance/exit, camera side and motivated light | A new viewpoint may reveal geography, but should not arbitrarily move fixed landmarks |
| Shot composition | Selected character/prop/location versions in the desired first pose and framing | A location plate or style reference alone does not fix subject placement or contact |

Inspect generated sheets for contradictions before making them authoritative. A sheet can have
different costumes, reversed props or incompatible views. Correct the relevant anchor or record
which view controls; do not ask downstream production to obey conflicting references. Keep the
original and revisions. Define framing clearance over the whole planned camera move, not only its first
frame: important hands, handles and prop markings should remain reviewable through the action. A deliberately partial view may omit an invariant; distinguish omission
from a visible contradiction and use another frame to check it.

## Bind references by role

For each shot, identify the actual character, prop, world and composition asset IDs, their versions
and intended roles. Reuse those IDs across shots instead of redescribing identity independently.
Map them to supported renderer/provider inputs at execution time. Labels such as “Element 1” in
a tutorial are not universal API fields. A common reference or seed can help but does not guarantee
identity, geography, timing or continuity. Reference-only sheets should not appear as collages in
the returned film; supply a separate composed start frame when supported and useful.

Keep creator references as evidence of visual grammar; produce original or authorized anchors.
Do not upload third-party reference footage merely to reproduce a demonstrated workflow. Retain
asset origin, rights/authorization, hash or version and any permitted upload destination. Check
current input limits, reference roles, duration, aspect, audio options and cost before submission.
Prepare and show the concrete plan before any required spending/upload approval; an earlier
approved generation pass is not an open-ended budget for new shots or retries.

## Direct connected actions

Use stable shot IDs and the master film timebase. For each shot specify:

- First pose/composition, one principal action and an observable final state.
- Subject motion, camera motion and environment response separately.
- Incoming/outgoing continuity: screen direction, eyeline, pose, prop state, light and geography.
- Exact source/reference IDs, selected model/renderer settings, prompt revision and returned asset.

Prefer a few legible actions to contradictory simultaneous events. A hand reaching a lever needs
plausible contact before the mechanism responds. A camera push cannot replace that articulation.
Give important actions time to settle; preserve the requested overall duration by measured trims
and the existing conform workflow. Do not silently loop, freeze, stretch or swap footage to hide
a missing action. Record intentional holds as editorial choices.

For separate generations, inspect the difficult action and reference adherence before spending
on dependent shots when practical. After an accepted shot, its reviewed outgoing state can inform
the next composition; when the next shot must retain an exact pose, light or piece of geography,
use that reviewed rendered outgoing frame as its composition anchor rather than a separately
redesigned still. Do not propagate an unreviewed defect as a continuity anchor. Stay within
the authorized attempt/cost limit and preserve unsuccessful attempts with their actual status.

## Review continuity in the footage

Compare first/action/end states and the frames immediately around each cut. Review motion as well
as stills. Use a small project matrix with observed values and pass/gap/not-visible status:

| Dimension | Check in the actual result |
| --- | --- |
| Identity | Face, age, body proportions, hair, costume and distinguishing features remain the chosen character |
| Props/anatomy | Shape, count, scale, carrying hand, grip and contact remain plausible during motion |
| Space | Landmarks, scale, travel direction, camera side and eyelines support the intended geography |
| Light/style | Motivation, texture and palette remain coherent; changes have a visible story cause |
| Action | The requested event actually happens in order and reaches its stated final condition |
| Handoff | The next shot inherits the intended pose, prop state and cause/effect relationship |

Match action phase as well as appearance at a cut. Two consistent shots can repeat a reach or
reset a prop state; choose a measured outgoing/incoming frame and, when appropriate, an explicitly
recorded editorial retime rather than silently accepting the duplicated action. Preserve the
requested film duration and distinguish cadence resampling from motion interpolation.

Inspect a tighter crop of contact, grip, actuation and release at source cadence when hands
operate a prop. Count fingers only when they are visible; occlusion is not evidence of missing
anatomy. Separate intentional perspective/camera changes from unexplained shape or grip drift.

A small, constant framing mismatch at a cut may be corrected with a measured fixed scale/crop
when the complete shot still contains the required hands, props and landmarks. Record the
transform and recheck both cut frames and the full shot. Do not warp a face or hand to force a
match, invent missing borders, or confuse a framing repair with a repaired performance.

Reject a stabilization or matte repair that creates a seam, doubles a coat/prop, or substitutes
a still patch for required articulation. A global transform cannot recover hand performance
that left the source frame. Inspect correction boundaries over the entire shot; if a clean
local repair is unavailable, retain that finding and prepare a bounded replacement shot under
the existing spending/upload limits. Do not silently downgrade the intended performance.

Keep evidence at the specific shot/time and name the repair: replace an inconsistent reference,
restage a contact, narrow a prompt, regenerate within approval, or change a motivated cut. Reject
an attractive result that omits the requested event. A tutorial's prompt, progress bar and later
result can belong to different examples; do not use them as proof of a single successful run.

Generated mythic or historical-looking imagery is illustration. For documentary work, bind claims
to factual sources and label reconstructions appropriately. Preserve exact dates, quotations,
logos, labels and maps in controlled graphics when a generator cannot maintain them.

## Finish and report the actual test

Carry approved shot assets into the existing [sound pass](sound-design.md) and
[export verification](video.md#trace-and-verify-the-complete-deliverable). Check the complete
encoded film, actual duration, transitions, readable overlays and selected sound mode. Reused
conforms must match source content, trims, timing and render settings, not only dimensions or
frame count; reject a stale intermediate before it can enter the final film. Treat a
silent test as silent; do not infer lip sync or mixing quality from its picture.

Report separately: instruction/link validation; anchor-image consistency; generated/animated
motion consistency; final-file/playback checks; listening; and user creative acceptance. A prepared
specification, still animatic or successful encode is not evidence of generated character motion.
A single reviewed sample tests this workflow on that sample, not reliable performance on all
characters or models. Store project identities, images and exact prompts with the project rather
than embedding them into this reusable skill.
