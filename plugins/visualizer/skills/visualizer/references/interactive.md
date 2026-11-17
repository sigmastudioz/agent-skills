# Interactive explanations and simulations

## Start with a question and observable consequence
Give the viewer an immediately legible initial state. Choose controls that reveal relationships:
change a scenario, inspect an entity, adjust a meaningful parameter, compare outcomes, or step
through a process. A decorative animation with unrelated sliders is not an interactive explanation.
Show units, current values, valid ranges, assumptions and the consequence of each action.
Offer sensible defaults and a reset that restores all affected state, including time and selection.

Keep explanatory copy short and adjacent to its referent. Put an important variable where its
effect appears. Use stable spatial anchors and small multiples when they clarify comparisons.
Do not distort the model to make every control produce a dramatic result.

## State and deterministic behavior
- Own canonical state in one place; derive computed values rather than copying them into widgets.
- Validate programmatic inputs as well as visible controls. Handle NaN, infinity, zero denominators,
  empty sets, bounds and invalid parameter combinations with meaningful states.
- Give selections stable IDs; reconcile them when filtering/removing records. Explain no matches.
- Distinguish loading, empty, stale, unavailable and error. Preserve context on recoverable failures.
- Async requests need cancellation or stale-result protection. A slower earlier response must not
  overwrite the latest scenario. Retries must not duplicate effects.
- Record seeds and scenario parameters for stochastic models. Pause/seek/replay must be reproducible.
- For numerical simulation, state equations, units, assumptions and integration method. Use bounded
  fixed simulation steps or a suitable solver, not display frame count as physical time.
- Cap catch-up work after a suspended tab. Treat invalid or unstable solver states explicitly;
  inspect conservation/monotonicity/analytic limits where the modeled system requires them.
- An illustrative simulation is not a validated forecast. Avoid unsupported real-world precision.

## Input, accessibility and responsive layout
Use labeled native controls when practical. Support keyboard focus, arrows/step buttons, touch and
pointer as appropriate; avoid hover-only information and color-only distinctions. Keep focus visible.
Provide a readable text/table summary for meaningful canvas/WebGL information. Controls need names,
current values and instructions; announce important state changes without narrating every frame.
Tooltips must stay on screen and be dismissible; avoid covering the selected evidence.

Measure text, labels and hit targets at the actual laptop/phone size. Reflow related controls with
the visualization instead of shrinking a desktop composition until it is unreadable. Verify long
labels, localization/number formatting when relevant, zoom and high pixel density.
Honor reduced motion with a static/stepwise equivalent. Essential meaning must survive animation
being disabled. Pause moving content; never autoplay sound without user input.

## Render and operate efficiently
Separate model updates from draws. Redraw on state/size changes; stop animation work when paused,
hidden, unmounted or no longer visible unless a documented calculation must continue.
Bound pixel ratio, node counts, particle counts, history, subscriptions and concurrency. Profile a
representative target device/workload before claiming a frame rate or selecting a worker/GPU path.
Use spatial indexing, level of detail, aggregation or virtualization only where actual scale needs it.
Keep important marks/labels readable when aggregating; expose the resulting loss of detail.
Dispose listeners, timers, observers, workers, audio nodes, GPU resources and temporary URLs.

## Export and offline behavior
A shareable interactive artifact needs its actual sources and dependencies, not only a screenshot.
State whether it needs a local server, network access, API credentials or a supported browser.
Pin dependencies and retain licenses; bundle locally for offline delivery when allowed.
Ensure failed network imports have a useful fallback or visible error. Do not embed secrets in HTML.
For an export, capture the selected scenario, units, filters, time and attribution. Preserve the
current view or clearly offer a reset/export-all option. Verify the exported artifact independently.

Test every meaningful control through model and visual consequence: initial state, parameter
extremes, keyboard interaction, reset, rapid changes, empty/error cases, resize and cleanup.
Add numeric invariants and meaningful regression cases where calculation or integration is at risk.
Do not substitute a static screenshot test for behavioral verification.

## Recipe: explainer controls for a 3D subject
For a spatial explanation that someone presents or studies: a section through the object, named
camera shots, a rewind to the current beat, and notes pinned to parts. These sit on top of
pause, seek, replay, step and keyboard support above. Checked 2026-11-13 on a small vane-pump scene
with React 18, Three.js 0.160 and React Three Fiber 8 in headless Chromium, with and without
reduced motion; treat other versions as unverified.

**One clock.** Keep scene seconds in one place and make every moving part a pure function of it
(`poseAt(seconds)`). Controls only change the clock or a view setting, so seeking to the same time
always draws the same picture, in any order.

**Beats and rewind.** List beats as `{ id, start, title }`. "Next" and "previous" jump to beat
starts. "Rewind to beat" follows the media-player rule: go to the start of the current beat, or to
the beat before when pressed within about 0.6 s of that start. Do nothing at the last beat rather
than wrapping. Show "Beat 2 of 3: title · time" in a status line.

```ts
function rewindTarget(t: number, beats: { start: number }[], grace = 0.6) {
  let i = 0
  beats.forEach((b, n) => { if (t >= b.start) i = n })
  return t - beats[i].start <= grace && i > 0 ? beats[i - 1].start : beats[i].start
}
```

**Cutaway.** Turn on `renderer.localClippingEnabled`, keep one `THREE.Plane`, and pass it in
`clippingPlanes` only to the materials of the shell being opened, with `side: DoubleSide`. Parts
inside stay whole. Toggle by passing an empty array. A clipped shell is hollow at the cut: add a
cap only if the wall thickness matters to the explanation. State it on the button with
`aria-pressed`.

**Camera shots.** Name each shot `{ key, name, position, target }` and bind the keys 1–9. Ease toward
the shot with a frame-rate independent factor, `1 - Math.exp(-6 * delta)`, applied to both
position and look-at target. Under reduced motion use a factor of 1: a cut. Show the active shot on
its button.

**Notes pinned to parts.** Each note has an anchor, text and a time window. Keep the labels as DOM
elements over the canvas and, once per frame, project the anchor to pixels and write a transform
on the element (no React state per frame). Three rules found while checking this:
- The anchor of a moving part must be a function of scene seconds; a fixed point soon labels empty space.
- Hide a note whose part is hidden, for example inside a closed casing, and say so in the text list.
- Hide a note whose anchor leaves the view or goes behind the camera.

Give the same notes as an ordered text list for the current moment, so the meaning does not
depend on the overlay. A "Notes" toggle hides the overlay only.

**Hotkeys.** One `keydown` listener on the window. Ignore the event when a modifier is held or the
target is an input, textarea, select or editable element; let Space on a focused button press that
button. Give every hotkey a visible button with the key in its label and `aria-keyshortcuts`.
Suggested set: Space play/pause, `[` and `]` previous/next beat, B rewind to beat, C cutaway,
A notes, 1–9 shots, R reset. Reset restores time, shot, cutaway and notes.

Verify before delivery: next/previous land exactly on beat starts; rewind obeys the grace rule;
the same seek twice gives the same pose; play advances time and pause holds it; the cutaway
changes the picture and reveals the inside notes; each shot key brings the camera to its named
position, at once under reduced motion; a moving part's note stays within 2 px of it; typing
`abc 123 []` in a text field changes nothing; reset restores everything. All of these passed in
the check above. Captured canvas pixels omit DOM notes: for a film, composite them or draw the
text in the scene, as the React Three Fiber reference says.

## Recipe: live floor-plan map beside a walkable 3D space
For a walkthrough of a home, venue or site: a first-person 3D view with the 2D plan beside it,
showing where the viewer stands and which way they face, live. Clicking the plan moves the viewer
there; hovering a room lights it in both views. Checked 2026-11-17 on a three-room plan with
React 19.3, Three.js 0.186, React Three Fiber 9.8 and ui-foundation 0.13.2 in headless Chromium,
at 1280×720, 900×700 and 390×844 and with reduced motion; treat other versions as unverified.

**One layout, two drawings.** Describe rooms (axis-aligned rectangles in metres), doors (a centre
point and width on a wall line) and furniture in one JSON layout. A pure function turns it into
walls: every room edge becomes a span on its wall line, spans on the same line are merged so shared
walls appear once, and door widths are cut out. The 3D walls, the SVG plan lines and collision all
read that output, so the two views cannot drift. Check that the plan draws exactly as many wall
lines as the model has walls.

**Plan units are world units.** Give the SVG `viewBox` the layout's bounds in metres and map world
x → plan x, world z → plan y (both grow the same way). Then each frame needs no screen maths: write
`translate(x z) rotate(-yaw°)` on the marker group with `setAttribute`, from inside the frame loop,
with no React state. Resizing, CSS scaling and letterboxing are handled by the SVG itself.

**Click to teleport by inverting the SVG's own matrix.** This stays right after any resize:

```ts
const m = svg.getScreenCTM()                        // null when not rendered
const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m!.inverse())
teleport(p.x, p.y)                                  // plan y is world z
```

Refuse a target outside every room or on furniture and say why in the status line. Pull an
accepted point inside its room by the player radius plus half a wall, so the viewer never lands in
a wall. Keep the heading on teleport.

**Heading and view cone.** With Three's default camera, yaw 0 faces −z, so forward is
`(-sin yaw, -cos yaw)` and the plan arrow (drawn pointing up) rotates by `-yaw`. The cone's width
is the horizontal field of view, `2·atan(tan(fov/2) · aspect)`, which changes with the canvas
shape: redraw the cone when `camera.aspect` changes, not only on mount.

**Walking.** Move one axis at a time and undo an axis that would hit a wall or furniture
rectangle (walls widened by their thickness), so the viewer slides along walls. Cap the frame step
(about 50 ms) so a hidden tab does not jump the viewer through a wall on return. Update the
"In Kitchen" status only when the room changes, through an `aria-live="polite"` line.

**Host.** ui-foundation's `/three` `Scene` hosts the canvas and stops rendering offscreen or in a
hidden tab. With reduced motion it renders on demand, which would freeze a walk the user is
driving: store `invalidate` from `useThree` and call it from every key, drag and button handler,
and keep calling it inside the frame loop while a key or button is held. In the check above,
removing those calls made the walk under reduced motion stop moving. `World` is not suitable
here: it adds orbit controls and its own lighting and ground.

**Controls and access.**
- Look by dragging with pointer capture (mouse, pen and touch) and `touch-action: none` on the
  canvas. Do not use pointer lock: it hides the pointer and traps it, and fails in many embeds.
- Make the 3D view a focusable region with the keys in its accessible name: W/S or ↑/↓ walk,
  A/D or ←/→ turn, Q/E sidestep. Listen for keys on that region only, so typing elsewhere does
  not walk, and clear held keys on blur.
- Give hold-to-move buttons (pointer down/up/cancel and Enter/Space) for touch and switch users,
  and a "Go to <room>" button per room as the keyboard way to teleport. Hover is an extra for a
  mouse; the buttons and the status line carry the same information.
- A first-person view is still hard for screen-reader users and can cause motion sickness: the
  plan, the room buttons and the status line must be enough on their own, and turning stays a
  steady rate with no camera bob.

For furniture with options and prices, use ui-foundation's `/product-config`. This recipe gives
the doorway full-height openings and no ceiling; add lintels and a ceiling as scene detail.

Verify before delivery: the marker's transform equals the player within 0.01 m and 0.05° after
walking, turning, teleporting and resizing; a click on the plan moves the player to the world
point under that pixel and the marker is drawn within 1 px of it, at desktop, tablet and stacked
phone widths; the 3D camera sits at the player's position and yaw; the view cone matches the
canvas aspect after each resize; walking into a wall for 3 s keeps the viewer inside the room; a
click on furniture is refused; hovering a room lights it in the plan and the 3D floor; a "Go to"
button works from the keyboard; keys pressed with focus elsewhere do nothing; and walking still
works with reduced motion. All of these passed in the check above.
