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
