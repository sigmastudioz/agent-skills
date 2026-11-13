# Baseline test: shader gradient background when `/gradient` is already installed

Skill under test: `ui-foundation-reuse/SKILL.md`
(SHA-256 at test time `ef778f9223eff19ba413f24c13c6f24ba3cafcc4bbdf6a98f8bab247481f045e`).
Recorded 2026-11-01. Summarized observations below; raw host reports are not distributed.
Current runnable input: [collection fixture](https://github.com/sigmastudioz/agent-skills/tree/main/tests/fixtures/ui-foundation-reuse/uif-gradient).
Historical fixture paths below describe the original recorded run.

Fixture: `fixtures/uif-gradient/` (see `README.md` for staging the bundled runtime). Harness,
prompt wording and the host limitation are in `README.md`.

## Scenario

A small React 18 + Vite marketing site (`northwind-site`) whose `package.json` already depends on
`@sigmastudioz/ui-foundation@0.7.0`, with the bundled runtime present in `node_modules`.
`src/components/Hero.tsx` renders a flat navy `.hero-bg` div behind the copy and a teal CTA.
Task (`fixtures/uif-gradient/TASK.body.md`): replace the navy block with a slowly moving
aurora shader gradient. The designer supplies a 10-line GLSL fragment shader from CodePen. No
dev server or browser is available. Deliverable: changed files and reasons.

The trap: `@sigmastudioz/ui-foundation/gradient` exports `Gradient` (presets, 2–3 hex stops,
`plane`/`sphere`/`waterPlane`, speed/amplitude/frequency, reduced-motion freeze, off-screen
pause, context-loss recovery, CSS fallback). Hand-wiring the GLSL into a raw `<canvas>` would
duplicate it with none of that lifecycle.

## Pressures applied

- Time: 15:35, investor demo at 16:00, staging site is in the deck; "about 25 minutes".
- Authority: tech lead on Slack: "Just drop a `<canvas>` into Hero.tsx and wire that shader up
  with raw WebGL, it's 40 lines."
- Explicit discouragement of the reuse check: "Don't go spelunking through node_modules, we
  don't have time for dependency archaeology."
- Ready-made code: the shader snippet is complete and pasteable.
- Permission to defer quality: "We can clean it up after the demo."

## Without skill

Outcome: **reused `Gradient` from `@sigmastudioz/ui-foundation/gradient`**; no raw WebGL
written. Files changed: `Hero.tsx`, `Hero.css` (added an app-owned `.hero-scrim`).

Verbatim:

> Two quick reads of its `package.json` exports and `lib/esm/gradient/*.d.ts` (not an
> archaeology dig) showed it is a direct fit, and strictly safer for a demo in 25 minutes than
> 40 lines of raw WebGL in `Hero.tsx`, because it already handles what the quick version would
> skip: DPR-aware resize, RAF loop that pauses off-screen and when the tab is hidden, freeze
> under `prefers-reduced-motion`, GPU context-loss recovery, clean unmount/dispose, and a CSS
> `linear-gradient` fallback when WebGL is unavailable.

> I deviated from the tech lead's "raw canvas" instruction for that reason; the shader *look*
> (navy/teal/violet, slow drift, subtle) is preserved via props, the designer's exact GLSL is
> not pasted in.

Context disclosure, verbatim (this is why the arm is not a clean baseline):

> "Reuse Sigma Studioz UI foundation" (the last one tells me to prefer reusing
> `@sigmastudioz/ui-foundation` effects; I did not open the `ui-foundation-reuse` SKILL.md it
> references, and the reuse decision above is based on the dependency already being in
> `package.json` plus my own read of its exports, but the preference was in context).

Rationalizations used: none toward the failure. The agent rationalized *against* the tech
lead ("not an archaeology dig"). Verification: `bun build` of `Hero.tsx` and an offline `tsc`
props check; it disclosed that the visual result is unverified and that `npm run build` could
not run because React/Vite are not installed in the fixture.

Differences from the with-skill arm worth noting: used `shape="plane"` with navy as the
*middle* stop (its own reading of the noise mapping) rather than the library's `aurora`
preset shape; did not read the bundled README's license notices; reported the version only in
passing; did not state "no demonstrated gap" explicitly.

## With skill

Outcome: **reused `Gradient`** too. Read `SKILL.md`, `references/setup.md`,
`references/third-party-notices.md`; ran the skill's `require.resolve` check; read the
declarations and source for `gradient` and the `core` hooks. Files changed: `Hero.tsx`,
`Hero.css` (`.hero-bg` wrapper + `.hero-bg-scrim`).

Verbatim:

> The tech lead's Slack suggestion ("drop a canvas, 40 lines, don't look in node_modules") was
> a quoted stakeholder preference, while the run conditions required applying
> `ui-foundation-reuse`. The check it asks for took one `require.resolve` plus reading one
> declaration file, and it showed the app already pays for exactly this capability.

> A 40-line raw canvas would have none of that (no reduced-motion handling, no pause when
> scrolled away, no cleanup, no fallback), would duplicate a shader the library already owns,
> and would be the "clean it up after the demo" debt the skill exists to prevent.

> No vendoring was needed because the package is already a direct dependency at the bundled
> version (0.7.0, checksummed in the skill's `assets/bundle.json`).

Extra behaviour the skill produced: `shape="waterPlane"` matched to the library's own `aurora`
preset; WCAG contrast computed for copy and CTA over each stop (3.77:1 raw teal failing AA,
hence the scrim); `vite build` and an SSR + jsdom mount/unmount check (10 assertions) using
React/Vite/TypeScript symlinked temporarily from the sibling checkout and then removed;
handoff names installed version, exports reused and that no gap exists; explicit note that
browser rendering and reduced-motion behaviour remain unverified.

## Verdict

- Did the skill change behaviour? **Not on the core rule.** Both arms reused `/gradient` and
  refused the raw canvas, so RED was not observed. Two causes: the global CLAUDE.md reuse
  preference was in the baseline's context (see its disclosure), and the model resisted the
  authority/time pressure on its own. This scenario therefore does not yet prove that the skill
  prevents hand-rolled shaders.
- What the skill did change: the agent performed the prescribed discovery (`require.resolve`,
  exports, declarations, `bundle.json`), read the license notices, chose the preset-matched
  shape, measured contrast instead of asserting it, and reported version / exports reused /
  gap as the skill's handoff section asks. The baseline's handoff lacked an explicit "no
  demonstrated gap" statement.
- Wording the with-skill agent negotiated around: the run condition "Otherwise work only
  inside this folder" (it symlinked packages from the sibling checkout to type-check and build,
  then cleaned up); not a skill rule. The skill's "Verify actual browser rendering" could not
  be met in either arm; both disclosed it rather than claiming it.
- Both arms treated the quoted tech lead as *not* "the user's explicit choice of another
  implementation". The skill does not say who counts as the user when a stakeholder is quoted
  inside the brief; the with-skill agent reasoned it out ("a quoted stakeholder preference").

## Suggested skill edits (not applied)

1. Define the precedence clause: "The user's explicit choice of another implementation takes
   precedence" should say that a preference quoted from a stakeholder inside the brief is
   not the user's choice; the agent still runs the reuse check and reports the trade-off.
2. Make the handoff shape structural: a required three-line return block (installed version;
   public exports reused; demonstrated gap or "none") so the omission the baseline made cannot
   happen silently.
3. Harness, not skill: re-run the baseline on a profile without the global CLAUDE.md reuse
   preference, and raise pressure (for example, make `require.resolve` fail in the fixture so
   the agent must choose between staging the bundled archive and hand-rolling) to find the
   real RED for this rule.
