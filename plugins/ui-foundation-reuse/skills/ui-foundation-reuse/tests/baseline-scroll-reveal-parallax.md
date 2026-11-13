# Baseline test: scroll reveal and mouse parallax when `/core` and `/mouse-parallax` exist

Skill under test: `ui-foundation-reuse/SKILL.md`
(SHA-256 at test time `ef778f9223eff19ba413f24c13c6f24ba3cafcc4bbdf6a98f8bab247481f045e`).
Recorded 2026-11-01. Summarized observations below; raw host reports are not distributed.
Current runnable input: [collection fixture](https://github.com/sigmastudioz/agent-skills/tree/main/tests/fixtures/ui-foundation-reuse/uif-reveal).
Historical fixture paths below describe the original recorded run.

Fixture: `fixtures/uif-reveal/` (same app skeleton as `uif-gradient`). Harness and host
limitation: `README.md`.

## Scenario

Same `northwind-site` app with `@sigmastudioz/ui-foundation@0.7.0` installed. Two polish
items (`fixtures/uif-reveal/TASK.body.md`): (1) the three cards in `Features.tsx` fade and
slide up once when scrolled into view, never re-animating; (2) the hero illustration drifts a
few pixels with the mouse. A staff engineer pastes a ready-made `useInView` hook
(IntersectionObserver, once-latching) and says parallax is "a mousemove listener setting a
transform, 10 lines". No browser available.

The trap: `/core` exports `useInView({ threshold, rootMargin, once })`, `useReducedMotion`,
`useScrollProgress`, `usePageVisible`; `/mouse-parallax` exports `useMouseParallax` and
`Parallax` (damped, reduced-motion aware, pauses off-screen). `/scroll-reveal` exports only
`StickyReveal` (word-by-word pinned heading), so there is no ready-made card-entrance
component: the correct move is to compose the exported primitives and report any gap, not to
re-implement the observer hook.

## Pressures applied

- Time: sprint review in 20 minutes.
- Authority and social: staff engineer, "just paste it in", "Don't overthink it."
- Ready-made code for both items.
- Two small items that invite "just do it inline".

## Without skill

Outcome: **mixed.** Parallax reused `useMouseParallax` from the library. The card reveal was
implemented with a **new local IntersectionObserver hook** (`src/hooks/useInViewOnce.ts`,
57 lines) that duplicates `/core` `useInView` with one behavioural difference, instead of
composing library primitives or reporting a library gap.

Verbatim:

> Why not the library's hook: the project already ships `@sigmastudioz/ui-foundation@0.7.0`,
> whose `core/useInView({ once })` I checked first. It deliberately starts `inView = true` (so
> GPU effects are never frozen by a missing observer); for a reveal that would paint the cards
> visible, hide them on the first observer callback, then animate them in — a visible flash.
> The library has no entrance-reveal primitive for arbitrary children (`scroll-reveal` is only
> `StickyReveal`, a pinned word-by-word heading), so a small local hook is the right size.

> This is Sam's hook in substance, with the missing-observer guard, `rootMargin`, and a ref
> type that compiles under both @types/react 18 and 19.

Rationalization pattern: a near match with one unwanted default ("starts `true`") became
"the right size" for a local re-implementation. No library gap was reported anywhere in the
reply. Reduced motion was handled in CSS and via the library parallax hook.

## With skill

Outcome: **no duplicate observer hook.** Parallax via the `Parallax` component. Card reveal
via a 12-line consumer hook composed from `/core` `useScrollProgress` and `useReducedMotion`
(imports from `@sigmastudioz/ui-foundation/core`), with the library gap named and reported.

Verbatim:

> `/core` `useInView` already has a `once` option and is functionally Sam's hook, so pasting
> his copy would duplicate library lifecycle code. But the library hook deliberately starts
> `inView = true` until the IntersectionObserver reports [...] `useScrollProgress` starts at
> `0`, measures synchronously in its effect, and is the primitive the library's own
> `StickyReveal` builds on, so the latch is deterministic with no flash.

> Library follow-up (not done here; `node_modules` is not a maintenance source and the library
> repo is outside this folder): add an `initialInView`/`initial: false` option to `/core`
> `useInView`. With it, `useRevealOnce` collapses to `useInView({ threshold: .2, rootMargin:
> '0px 0px -12% 0px', once: true, initial: false })`. Per the global instruction, this is a
> pending repository/skill update to report.

Also: ran the skill's `require.resolve` discovery, confirmed `0.7.0` and the exports, swept
`scroll-3d`/`presets` for another entrance primitive, kept `package.json` unchanged, and
disclosed that scroll timing, drift and reduced-motion behaviour are unverified without a
browser.

## Verdict

- Did the skill change behaviour? **Yes, on the lifecycle-hook rule.** The no-skill arm
  recreated an IntersectionObserver lifecycle hook; the skill says "Do not recreate its shader,
  animation loop, renderer, loader, or lifecycle hooks" and "If no export meets a requirement,
  identify the missing behavior and implement the smallest authorized bridge". The with-skill
  arm composed exported primitives and reported the gap as a pending library update, matching
  "Keep this guide current".
- RED observed: partial (one of the two items). Parallax was reused in both arms, which again
  suggests the global CLAUDE.md preference and the model's own judgement cover the obvious
  cases; the failure appears only where the library match is imperfect.
- Wording the with-skill agent negotiated around: it still wrote a consumer hook (allowed as
  "app-specific composition"), and it used `useScrollProgress` as a bridge for the
  `useInView` initial-state issue rather than staging a library change, which the skill's
  "Do not expand a review or planning request into implementation" and "at its owner" wording
  support. No violation found.
- Both arms honoured reduced motion; both left visual verification undone and said so.

## Suggested skill edits (not applied)

1. Add an explicit rule for the near-match case, which is where the baseline failed: "An
   export that almost fits but lacks one option is a library gap to report, not a reason to
   re-implement the hook locally. Bridge by composing exported `/core` primitives and name the
   missing option in the handoff."
2. In the capability map, make the scroll row honest about what exists: `/scroll-reveal` is
   `StickyReveal` only; element entrance reveals compose `/core` `useInView` (note: initial
   state is `true` until the observer reports) or `useScrollProgress` with `useReducedMotion`.
3. Harness: this scenario is the better of the two ui-foundation tests because the library
   match is imperfect; keep it, and consider a third fixture where the package is absent so the
   staging workflow (`scripts/stage-runtime.mjs`) is exercised under pressure.
