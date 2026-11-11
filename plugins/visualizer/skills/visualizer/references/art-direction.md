# Reference-led art direction

Use for studio-quality references, cinematic graphics, character motion, or a richer visual brief.
Extract a design system and motion grammar; preserve the subject's own identity and purpose.
Carry that grammar into the [timed visual specification](reference-to-spec.md) when producing
an artifact: bind shot evidence, spatial staging, motion beats and renderer decisions to one timeline.

## Study the mechanism
- Classify each reference: finished shot, montage, tutorial, recommendation, or interaction demo.
  Inspect nearby frames to distinguish actual animation from cuts between unrelated stills.
- Identify the target animation crop and in/out frames before palette extraction or tracking.
  Exclude tutorial UI and unrelated following shots. If source/output lengths differ, declare and
  label comparison holds or retiming instead of sampling the wrapper as part of the visual world.
- Measure centers, bounds, silhouettes and occlusion at matching times, especially before/during/after
  handoffs. Record crop/resolution or normalized coordinates; correct timing and staging before
  treating every mismatch as a shader problem.
- Record timestamped evidence for silhouette, framing, palette, material, light, camera, and cadence.
  Separate observed content, author claims, implementation hypotheses, and unavailable audio.
- Select a coherent primary visual world. Borrow techniques selectively; do not combine every look.
  Define dominant/accent colors, shape families, surface finish, typography roles, and motion verbs.
- Choose the medium from the visual requirement: illustrated layers, cel animation, actual 3D,
  procedural effects, or authorized generated footage. A richer brief is not always a shader brief.

## Direct the picture
- Make a strong silhouette and focal hierarchy before adding detail. Use purposeful negative space,
  controlled high-chroma accents, and macro/system/detail views rather than one repeated composition.
- Stage foreground, subject, and background with occlusion and value separation. Motivate key/rim
  lights and shadows; use fog or depth falloff for distance, not indiscriminate blur or darkness.
- Design materials as different responses to light: broad matte surfaces, selective glossy edges,
  restrained glass/metal transmission, or graphic ink/cel bands. Global grit is not material richness.
- Compare the footprint and softness of reflected color, not only base hue. Keep luminous cores,
  local spill and surface response distinct; global bloom cannot replace a missing reflection.
  Sample background color away from subject glows, and preserve the reference's actual action
  (for example formation then dispersal, rather than continuous drift).
- Plan camera position, target, lens, and reveal per shot. Move camera or object for a reason;
  carry screen direction, object identity, anchor points, and match shapes across transitions.
- Use anticipation, acceleration, contact, follow-through, secondary motion, and settled holds.
  Smooth does not mean constant motion or one easing curve; expressive stillness can carry a shot.
- Choose cadence deliberately: cinematic/cel timing may use fewer poses; interactive motion may
  benefit from 60fps. Preserve intentional holds and cut rhythm instead of interpolating everything.
- Let typography act: establish a headline, reveal a relation, label evidence, then yield to action.
  Tutorial step labels and captures explain a process; giant text is not a substitute for its visuals.

## Build and judge the right thing
- Use a real scene graph, meshes/layers, camera tracks, and depth-aware effects for spatial reveals.
  A fullscreen video filter cannot supply unseen surfaces, independent parallax, or new camera angles.
- For ink/smoke/ribbon work, preserve flow direction and coherent silhouettes; use restrained
  advection, spline deformation, masks, or particles instead of noisy displacement everywhere.
- For generated scenes, retain a character/style sheet and location/keyframe anchors. Specify motion
  separately from appearance; reject identity, scale, lighting, or geography drift across shots.
- Render an original hero/mechanism/payoff style-frame set and a short motion study before the film.
  Compare at phone and export size; inspect contacts/transitions, not just the most attractive still.
- Review composition, material separation, motion, camera, legibility, and sound-picture fit separately.
  Log the weakest dimension as a creative gap and repair its cause; more effects do not close every gap.

## Look presets
Use a named look as direction, not as bundled assets or a copied artist's style. Translate the
name into decisions the build can verify, then confirm it against the brief and a style frame.

| Look | Material and texture | Cadence | Palette and line | Camera |
| --- | --- | --- | --- | --- |
| Watercolour brush | Wet edges, paper grain, pigment pooling; brush fills (for example a p5 brush library) | Soft holds; slow dissolves | Limited washes; little or no outline | Gentle push-ins |
| Crayon picture book | Waxy strokes, paper tooth, visible hatching | On 2s; small boil | Primary-leaning; thick uneven line | Flat, side-on |
| 16-bit pixel RPG | Integer-scaled pixels, dithered shading, tile grid | Stepped sprite frames; no sub-pixel drift | Restricted palette; 1 px outline | Fixed or tile-snapped pans |
| Mid-century cartoon | Flat shapes, textured fills, limited animation | Held poses; smears on fast moves | Spot colours; geometric line | Lateral pans over flat layers |
| Ukiyo-e print | Woodblock grain, flat gradients (bokashi) | Slow, layered parallax | Indigo, vermilion, ochre; strong keyline | Wide, high horizon |
| Tilt-shift miniature | Shallow focus band, toy saturation | Slightly sped-up motion | Saturated, bright | High angle, looking down |
| Vintage engraving collage | Line-engraved cut-outs, paper shadows | Snappy cut-in and out | Sepia or two-colour | Static or slow drift |
| Worn print or xerox | Toner noise, misregistration, halftone | Jittered holds | One or two inks | Static, with frame jitter |
| Paper or felt craft | Fibres, stitch lines, soft shadows | Stop-motion on 2s | Muted, tactile | Tabletop, shallow depth |

Record the chosen look and its decisions in the timed spec so every shot inherits them.
