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
