# Reference → timed visual specification → verified output

Use when a supplied film, motion reference or tutorial should inform a new visual artifact.
For analysis alone, stop at the requested analysis; a reference is not authorization to render,
upload media, use a paid generator or operate the accounts shown in it.

## Reuse the inspection and direction paths

Reuse existing project analysis and source artifacts, checking that they match the selected media.
When available, the separate `video-analysis` skill supplies adaptive sampling, timestamped evidence
and transcript correlation. Otherwise use available native inspection or local FFmpeg/ffprobe;
do not install another analyzer merely to use this workflow. Follow [art direction](art-direction.md)
for the visual grammar, [the video workflow](video.md) for production and sound, and
[verification](video.md#trace-and-verify-the-complete-deliverable) for export checks. These paths keep their existing responsibilities.

Record source identity/hash when accessible, inspected ranges/frames, timestamp precision and audio
coverage. Increase sampling around important actions and transitions. Separate observed motion,
visible copy, author claims, reconstruction choices and unknowns. A tutorial may intercut different
projects; do not silently join its prompt, generation screen and result into one proven run.
Do not infer hidden prompts, model identity, editable source or production speed from its appearance.

The reusable extraction request is:

> Inspect the supplied reference for the requested outcome. Cite time ranges for narrative beats,
> framing, subject and camera motion, typography, light, material, depth and transitions. Separate
> observations from claims and unknowns, and state inspection/audio limits. Turn the relevant grammar
> into an original timed specification using our subject, copy and available assets. Identify what
> must remain exact, select a supported renderer and carry shot IDs through export review.

## Make one renderer-independent specification

Keep the specification with the project, not the installed skill. Extend an existing storyboard or
scene file instead of creating competing timelines. Markdown is sufficient for a small film; use
structured data when a renderer or repeated revisions consume it. Preserve these meanings:

| Field | Contract |
| --- | --- |
| Brief | Audience, takeaway, output size/aspect, FPS, duration, sound mode and acceptance target |
| Evidence | Source IDs/ranges, inspected artifacts, precision and observation/inference/unknown status |
| Visual world | Original subject/assets, palette, type roles, materials, lighting and continuity anchors; motion tokens (duration scale, easing set, stagger step, overshoot, transition family) saved once per brand or reference and reused across videos |
| Shot identity | Stable shot ID, output in/out on one timebase, explanatory job and reference evidence |
| Space and framing | Foreground/subject/background, screen positions, scale, occlusion, camera/lens intent |
| Start → action → end | First state, separately described subject/environment/camera motion, settled final state |
| Beat timing | Shot-relative beats, holds, transitions and the outgoing continuity handoff |
| Text and sound | Exact copy, typography/layout, caption/cue IDs, sound intent and visual/audio anchors |
| Implementation | Selected renderer, project-local asset IDs/rights, adapter decisions and known compromises |
| Review | Actual output/range, observed mismatch, revision and accepted versus still-unverified checks |

Use output frames or seconds with an explicit FPS; distinguish source time, output time and
shot-relative time. Convert beats to frames for exact rendering, then derive captions and sound
from that same timeline. Use nonoverlapping, end-exclusive shot ranges; declare transition overlap
or intentional gaps. Source excerpts can change order or length without retaining source timestamps
as output timestamps. A generative timing request is a target until measured in the returned clip.

For example, an original eight-second light study at 24fps can have one shot, `orbit`, frames
`[0,192)`: `[0,48)` establish a matte sphere and thin ring; `[48,144)` rotate the ring with the
camera locked; `[144,192)` settle into a clear silhouette and hold. Record ring/sphere positions,
material separation, lighting and the last-frame handoff. This is a timing illustration, not a
recovered reference prompt or a requirement to use eight seconds, spheres or this visual style.

For recurring subjects and locations, use [character and world consistency](character-and-world-consistency.md)
to bind anchor versions and review actual shot-to-shot identity, action and geography.

## Adapt the same shot to the selected renderer

| Need | Reuse and adapter |
| --- | --- |
| Exact diagrams, code or metric cards | Existing project renderer or bundled [storyboard renderer](storyboards.md); map shot duration, copy and supported primitives. Its graph/code/metrics/end schema is narrower than this specification. Do not pass camera/material fields as if it implements them. |
| Designed vector/type or spatial motion | Existing SVG/canvas/motion-code or R3F/Three.js path; convert beats into explicit-time transforms and camera tracks. Discover compatible UI Foundation effects before building equivalents; verify seeking/export support. |
| Authorized generated imagery or footage | Prepare original/authorized anchors and a prompt per shot. Check the actual provider's available inputs, length, aspect, sound and cost before invoking it; use supported controls, not options inferred from a tutorial. |

For a generation handoff, translate a shot into these sections as useful, rather than submitting a
whole montage as one contradictory prompt:

```text
SCENE CONTEXT: original subject, action, visual style and the shot's purpose.
SPACE / APPEARANCE: foreground, subject, background, material, palette and lighting.
START / ANCHORS: first composition and supplied asset IDs with their intended roles.
MOTION / BEATS: subject motion, environment response, camera motion, ordered actions and holds.
END / CONTINUITY: final state and what the next shot must inherit.
SOUND / FINISH: chosen sound mode; exact text or effects to add in the controlled finishing pass.
```

Adapt wording to the provider. An input image can already define appearance; concentrate the motion
prompt on what changes instead of describing a conflicting scene. Use supported start/end frames
or references when helpful, without assuming they guarantee identity or timing. Keep required labels,
logos, data and precisely timed type in a controlled overlay when generation cannot preserve them.
Preserve silence or music-led direction; do not add speech just because a provider supports it.

Retain the spec revision, prompt, input IDs, actual settings, returned clip ID/path and observed result
for each attempt. Review a short representative shot first; revise the specific mismatch within the
authorized attempt/cost limit. If a required capability is unavailable, deliver the prepared spec and
state the blocked handoff. Do not claim a rendered result or silently substitute a different brief.

## Compare the export to the specification

Inspect the same shot IDs at their actual output times, including before/during/after transitions.
Check silhouette, spatial continuity, subject/camera distinction, material/light consistency, readable
text and sound-picture fit. A matching still does not establish matching motion. Measure returned
clip timing before trimming, assembling or aligning cues; propagate timing changes to downstream
shots, captions and audio. Reject identity drift, missing beats and unsupported factual claims.

Carry accepted assets into the existing storyboard/renderer and sound/export workflow. Verify the
actual complete file and editable sources using [video verification](video.md#trace-and-verify-the-complete-deliverable).
Report technical checks, visual review, listening coverage and remaining creative gaps separately.
A prepared prompt, attractive frame or successful encode alone does not complete production.

## Optional provider references

These are implementation references, not required accounts or bundled integrations. Recheck current
capabilities before use; installing this skill does not provision any provider.

- [Google DeepMind prompting guide](https://deepmind.google/models/veo/prompt-guide/): framing,
  camera movement, style, light, action and scene detail.
- [Google Flow creation guide](https://support.google.com/flow/answer/16353334): supported generation
  settings, reference ingredients and start/end-frame inputs.
- [Runway image-to-video prompting](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide):
  distinguish subject, scene and camera motion; let the image supply appearance.
