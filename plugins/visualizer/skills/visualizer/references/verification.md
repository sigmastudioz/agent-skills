# Connected-path gap trace and acceptance

## Inventory before claiming coverage
List created/changed capabilities, owning paths, public contracts, consumers, asset dependencies,
configuration and runtime registration. Include control handlers, async loaders, animation loops,
worker/GPU adapters, exports and cleanup. Search for existing equivalent behavior before adding it.
For a small fix, trace the touched path and adjacent contracts; don't audit unrelated projects.
For an explicitly full audit, inventory every first-party module and account for each edge.

Follow entry/input → validation → model/calculation → visual mapping → layout → renderer → visible
state. Trace controls back through model changes; trace exports through snapshot/timeline, encoder,
captions, audio, final artifact and public links. Check indirect consumers and lifecycle disposal.
Use a visited set for cycles and record them; external internals are a coverage boundary.

Trace alternatives appropriate to the artifact: invalid/empty/missing input, nonfinite values,
loading/error/stale state, rapid updates, cancellation, paused seek, reset/replay, resize, import
failure, GPU/context loss, missing font/media, failed encode and interrupted publication.
For a repair, retrace the consumer and observable result; fixing the producer alone is insufficient.

## Ledger and decisions
Use the task's existing evidence location, not the global skill. Record source revision/hash,
path/contract, entry/consumer, dependencies/effects, command/result, finding, impact and next action.
Use stable IDs and statuses: verified, static-only, gap-found, fixed-and-verified, blocked or
not-applicable. Classify bugs, integration gaps, required feature gaps, improvements and unverified
paths separately. Fix confirmed in-scope bugs and required gaps; do not invent extra product scope.
Report inventoried/traced modules and checked/unresolved edges separately from runtime checks.

## Meaningful acceptance tests
| Mode | Required evidence when applicable |
| --- | --- |
| Data | Known-input calculations, units/scale/denominator correctness, missing/outlier behavior |
| Diagram | Valid endpoints/direction, label readability, reachable selection and reset |
| Simulation | Stable seed, analytic/invariant cases, numerical bounds, time-step behavior |
| Interaction | Every control's actual consequence, keyboard/touch, rapid changes, reset, empty/error |
| GPU | Shader compilation, resize, context loss/recovery, reduced motion, fallback and cleanup |
| Video | Full decode, timing/frame count, representative shots/transitions, captions and audio |
| Shared output | Same selected model state/seed/time across interactive and film adapters |
| Distribution | Self-contained sources, dependency/license inventory, paths and actual public playback |

Use existing tools and tests. Add regression tests for substantive calculations or lifecycle bugs,
not assertions that merely mirror source wording or folder names. A screenshot is visual evidence,
not proof of all state transitions. A successful skill/catalog validator is packaging evidence,
not proof that a fresh model chose the skill or produced a good artifact.

Measure realistic data size, device, resolution and operating state when reporting performance.
Frame pacing, responsiveness, memory and export time are different metrics. Describe the tested
budget and limits; do not turn one desktop result into a universal 60fps or scale claim.
Inspect representative frames at viewing size and export size, with sound if available. Record
audio measurements separately from listening and accessibility checks; don't infer unheard speech.

## Deliver and hand off
Provide the actual artifact, editable sources, scenario/timeline, assets/rights, reproduction
commands, dependency versions and relevant evidence. Preserve useful errors and partial results;
report unavailable tools or unfinished exports without substituting an unrelated screenshot.
Name exact files, revision, model/adapter contracts, covered paths, unresolved gaps and next action.
Do not include private inputs, session logs, credentials or machine-specific secrets in public ZIPs.
Installation and implicit-invocation metadata do not configure every remote host. Verify discovery
and behavior on each claimed runtime; keep failed and untested cases visible.
