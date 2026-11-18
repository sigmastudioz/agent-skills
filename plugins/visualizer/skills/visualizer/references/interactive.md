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
there; hovering a room lights it in both views. Checked 2026-11-17 with React 19.3, Three.js 0.186,
React Three Fiber 9.8 and ui-foundation 0.13.2 in headless Chromium at 1280×720, 900×700, 390×844
and 667×375, with reduced motion and with WebGL blocked; treat other versions as unverified. Two
fresh agents, each given only the recipe at that time and a different four-room layout, built
versions that passed an independent checker.

**One layout, validated.** Rooms, doors, furniture and poses live in one JSON layout, in metres:
- A room or piece of furniture is `{ x, z, w, d }`, where `x, z` is the corner with the smallest
  x and z. Furniture also has a height `h`. Each room has an `entry` pose `{ x, z, yaw }` for its
  "Go to" button; the layout has a `start` pose. Do not aim at the room centre: furniture often stands there.
- A door is `{ x, z, width }`, centred on a wall line. It must lie on exactly one wall line, inside a
  stretch still solid after earlier doors are cut (so doors cannot overlap), with no crossing or
  touching wall inside its opening (a T or corner junction), and it must join two rooms: probe a
  few centimetres either side of it and require a different room on each side.
- A pose is standable when it is inside a room and the player's circle touches no wall or furniture.
  A point on a shared wall line or in a doorway belongs to whichever room the walker was last in,
  so the status does not flicker.

Build the plan in a pure function. Round coordinates to millimetres first, so `0.1 + 0.2` and `0.3`
key the same wall line. Every room edge becomes a span on its line, spans on one line merge so
shared walls appear once, and door widths are cut out. Reject the layout with a named reason when a
value is not finite, a size is not positive, rooms overlap, furniture is not inside one room, a door
breaks the rules above, a room cannot be reached from the start through doors, or a pose is not
standable. The 3D walls, the SVG plan lines and collision all read the output, so the views cannot
drift. A wall is one segment left after door cuts. Test the model on its own: the fixture's wall
count and total wall length (merged line lengths minus door widths), no two walls overlapping on a
line, and one invalid layout per rejection reason.

**Plan units are world units.** Give the SVG `viewBox` the layout's bounds in metres and map world
x → plan x, world z → plan y (both grow the same way). Placing the marker then needs no screen
maths: write `translate(x z) rotate(-yaw°)` on the marker group with `setAttribute`, with no React
state. Resizing, CSS scaling and letterboxing are handled by the SVG itself.

**The player controller owns the walk and the plan sync, not the 3D frame loop.** Send every change
of pose (a walking step, a drag, a click on the plan, "Go to", reset) through one `commit(pose)`
that stores the pose, writes the marker transform, updates the room status when the room changes,
and requests a 3D frame. Step the walk in the controller's own `requestAnimationFrame` loop, which
runs only while a key or button is held. The 3D view only reads the pose. A canvas host stops
rendering when it is offscreen or the tab is hidden (ui-foundation `Scene` sets
`frameloop="never"`), and without WebGL there is no frame loop at all. Anything driven from
`useFrame` (the marker, the status or the walk itself) stops exactly when a phone user has scrolled
to the plan and presses the walk buttons.

**Click to teleport by inverting the SVG's own matrix.** This stays right after any resize:

```ts
// Read the point from pointerdown/pointerup: a click event's clientX/Y are rounded to whole pixels,
// about 3 cm on a desktop-sized plan.
const m = svg.getScreenCTM()                        // null when not rendered
const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m!.inverse())
teleport(p.x, p.y)                                  // plan y is world z
```

Refuse a target outside every room or on furniture, and say why in the status line. Pull an
accepted point inside its room by the player radius plus half a wall, so the viewer never lands in a
wall. Refuse it if the pulled point touches furniture. Keep the heading on teleport.

**Heading and view cone.** With Three's default camera, yaw 0 faces −z, so forward is
`(-sin yaw, -cos yaw)` and the plan arrow (drawn pointing up) rotates by `-yaw`. Put a dot centred
on the origin in the marker group: its bounding-box centre is the viewer's position, which tests
measure (the arrow and cone make the group's box lopsided). The cone, about 1.6 m long, has the
horizontal field of view, `2·atan(tan(fov/2) · aspect)`, which changes with the canvas shape:
redraw it when `camera.aspect` changes, not only on mount.

**Walking.** These defaults gave a comfortable walk: speed 2.2 m/s, turn 1.8 rad/s, player radius
0.25 m, eye height 1.6 m, vertical field of view 70°, yaw and pitch from a drag at 0.004 rad per pixel,
clamped to ±1.1 rad. Collide against walls as rectangles extending half the wall thickness each
side of the centre line, and against furniture rectangles. Move one axis at a time and undo an axis
that would hit, so the viewer slides along walls. Split a long frame into sub-steps of at most
50 ms, so no single step can cross a wall, and cap the total catch-up at about 0.25 s for a tab
returning from the background. Clamping the whole frame to 50 ms instead makes a slow device walk
at half speed. Show the room in an `aria-live="polite"` status line ("In Kitchen."), updated only
when the room changes; put a refusal reason or "Moved to …" after it on the same line.

**Host and failure.** ui-foundation's `/three` `Scene` hosts the canvas and stops rendering
offscreen or in a hidden tab. With reduced motion it renders only on demand, which would freeze a
walk the user is driving. Store `invalidate` from `useThree` and call it from `commit`, so every
step of the controller's loop requests a frame. Without that, the view stopped following the walk
under reduced motion. Do not use `World` here: it adds
orbit controls, lighting and a ground of its own. `Scene` renders a wrapper `div`: give it an explicit
size (for example `position: absolute; inset: 0` inside the view). Wrap `Scene` in an error boundary that shows
a short message in place of the view. A blocked or lost WebGL context throws to that boundary, and
`Scene`'s `fallback` covers only a failed import. Because `commit` owns the plan, the plan, "Go to"
buttons and status keep working without WebGL. Only the view cone, which needs the camera, is lost.
If the package cannot be installed (an offline sandbox), follow the `ui-foundation-reuse` skill's
staging steps. Aliasing its subpaths to an extracted copy also works in Vite, with these settings:
- `resolve.dedupe` for React, Three.js and React Three Fiber, so only one copy of each loads.
- `server.fs.allow` for the extracted folder and the real path of a symlinked `node_modules`.
- A `cacheDir` you can write, when `node_modules` is read-only.
- `optimizeDeps.include` for `three`, `@react-three/fiber` and the JSX runtime, so the lazily
  loaded renderer does not trigger a reload.

**Controls and access.**
- Look by dragging with pointer capture. Set `touch-action: pan-y` on the canvas: a horizontal touch
  drag turns, and a vertical swipe still scrolls the page. Pitch follows a mouse or pen drag only. Do
  not use pointer lock: it hides and traps the pointer, and fails in many embeds.
- Make the 3D view a focusable region with the keys in its accessible name: W/S or ↑/↓ walk,
  A/D or ←/→ turn, Q/E sidestep. Listen on that region, not the window, so held movement keys never
  fire while someone types elsewhere. This differs from the explainer recipe's window hotkeys, which
  are single presses. Call `preventDefault` on the movement keys, or the arrows scroll the page.
- After a click on the plan, move focus back to the 3D view (`focus({ preventScroll: true })`), so
  the walk keys work at once. Clicking the plan otherwise leaves focus on the page body, and the keys
  silently do nothing. Leave focus on the "Go to" buttons, which keyboard users reach with Tab.
- A key-up always releases its key, whatever modifiers are down. When a key goes down with Cmd, Ctrl
  or Alt, drop every held key: macOS sends no key-up for keys released while Cmd is held, so the
  walk would carry on. Clear held keys when the region or the window loses focus.
- Keep keyboard holds and on-screen button holds in separate state. Pressing a button moves focus off
  the region, and its blur handler must not cancel the button's own hold.
- Offer hold-to-move buttons (pointer down/up/cancel, Enter/Space), a "Go to <room>" button per room
  using its entry pose, and a Reset that restores the start pose, pitch, held input, hover and status.
  Hover is a mouse extra; the buttons and the status line carry the same information.
- On a narrow screen, stack the plan under the view and size the view row so the two cannot overlap
  in landscape, for example `grid-template-rows: max(180px, 55vh) auto` with no fixed minimum height
  on the view.
- A first-person view is still hard for screen-reader users and can cause motion sickness: the
  plan, the room buttons and the status line must be enough on their own. Keep turning at a steady
  rate with no camera bob.

For furniture with options and prices, use ui-foundation's `/product-config`. This recipe models
interior doors only and gives doorways full-height openings with no ceiling; add lintels, a ceiling
and outside doors as scene detail.

Verify before delivery:
- The model tests above pass.
- The marker's transform equals the player within 0.01 m and 0.05° after walking, turning,
  teleporting, "Go to", reset and resizing.
- A click on the plan moves the player to the world point under that pixel, and the marker is drawn
  within 1 px of it, at desktop, tablet and stacked phone widths. The 3D camera sits at the player's
  position and yaw, and the view cone matches the canvas aspect after each resize.
- Walking into a wall for 3 s keeps the player at least radius plus half a wall (0.31 m here) from
  the wall's centre line. A click on furniture is refused.
- After a click on the plan, W walks straight away.
- "Go to" works for a room whose centre is under furniture, and works from the keyboard. Keys pressed
  with focus elsewhere do nothing. Holding W, pressing Cmd, then releasing both leaves the player still.
- With the 3D view scrolled offscreen on a phone, "Go to" and a click on the plan still move the
  marker and the status. With WebGL blocked, the message replaces the view and the plan and "Go to"
  still work.
- Walking still works with reduced motion. At 667×375 the view does not overlap the plan.

**From a floor-plan image.** A marketing plan (PNG or PDF) can be traced into this layout by hand
or by an agent reading the image; checked 2026-11-17 on four real apartment plans. Take the scale
from the printed room sizes: compute pixels per metre from two or three rooms and expect them to
agree within about 5% (labels are often depth × width, not width × depth). Put the origin at the
inside of one corner and convert every edge to metres, rounded to 5 cm. Model each space as a
rectangle: split an L-shaped living area or a hall into rectangles joined by a wide opening (a door
as wide as the shared wall minus about 20 cm). Leave closets, laundry niches and columns as voids or
solid furniture, and leave out the front door, which joins no room. Let the validator find the
mistakes; in the check, every rejection was a real tracing error (a start pose inside the sofa,
rooms overlapping by 7 cm, an opening touching a T junction). Trace furniture from the drawn
symbols. A plan with a mezzanine or stairs needs a level per floor, which this model does not have:
trace the lower level and say what was left out.

How to test it: block WebGL by launching Chromium with `--disable-webgl --disable-3d-apis` (or by
making `getContext` return `null` for WebGL), and expect R3F to log the context error. To push the
view offscreen at phone size, insert a tall spacer above the panel in the test. Keep the view cone out of the marker group, or check the marker's dot rather than the group's
bounding box, whose centre moves with the cone. Give the page an
icon (`<link rel="icon" href="data:,">`) so a missing favicon is not reported as a console error.
Also check that a hold-to-walk button still walks with the view offscreen and with WebGL blocked.

In the check above, every one of these passed. Run against the first version of this recipe, the
offscreen, WebGL-blocked, stuck-key, "Go to"-under-furniture and landscape checks each failed.

To turn the grey rooms into a lit, furnished interior (windows, surfaces, furniture, light and
post-processing from the same layout), continue with [finishing a walkable interior](interior-finish.md).
