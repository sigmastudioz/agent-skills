---
name: app-retention
description: Design fair retention and ranking for a product from its own data - a daily return-likelihood estimate, nudges timed to the user's real habits, a rescue action when return looks unlikely, per-item ranking of feeds and suggestions, choosing assets (photos, thumbnails) by measured results, and timing upgrade offers after a win. Use when building or reviewing onboarding, notifications, streaks, recommendations, home rows, feeds, paywalls or "keep users coming back" features in an app, game, store or assistant. Privacy-first and no dark patterns; every mechanic is a hypothesis to measure.
license: MIT
---

# Returncraft
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Help people come back because the product is useful to them, not because it nags or tricks them.
Large consumer apps publicly described (and widely "reverse-engineered") use a few repeatable
patterns. This skill turns them into small, honest, measurable features. Read the
[patterns](references/patterns.md) for constructions, signals and checks.

## Rules

1. **Own data only.** Use signals the product already collects for its own purpose (sessions,
   completions, follows, purchases). No third-party trackers, no Wi-Fi, location or device
   fingerprinting, no data brokers. Prefer on-device computation where it is enough.
2. **Opt-in and controllable.** Every nudge and personalised ranking can be switched off;
   respect quiet hours; at most one proactive nudge a day unless the user chose more.
3. **No dark patterns.** No fake urgency or scarcity, guilt copy, streak-loss threats, hidden
   costs, confirm-shaming or pay-to-skip pressure. Offers appear after a real win, never at
   first launch or mid-task.
4. **Explainable.** Start with a transparent rule or simple model; show users why an item is
   suggested ("because you finished 4 similar sessions").
5. **Measure, don't assume.** Each mechanic is a hypothesis: define the metric (next-day
   return, completion, time to first win), compare against a holdout or an earlier period,
   and keep it only if it helps users without harming trust signals (opt-outs, uninstalls,
   complaints).
6. **No revenue-tuned odds or prices.** Do not change difficulty, odds, rewards or prices per user
   from their ad value or spend, hide harder variants, or gate reviews; the
   [avoid list](references/patterns.md#avoid-list-patterns-seen-in-public-app-teardowns) names them.
7. **Honest claims.** Viral breakdowns of other apps are leads, not facts; don't copy their
   numbers into product promises.

## Workflow

1. Map the product's real loop: entry → first win → repeat value → return trigger.
2. Find where users drop (onboarding steps, day-2 return, unfinished items) from existing data.
3. Pick the smallest pattern that addresses that drop ([patterns](references/patterns.md)).
4. Build it behind a flag with tests on fixtures; add the off switch and copy review.
5. Measure on a holdout; record the result next to the decision.
6. Review the screens and copy with an independent critique where the host has one.

## Hand off

For free ways to get found (store keywords, localisation, problem pages, AI-answer listings, instant links, bundles), see [distribution levers](references/distribution-levers.md). Feature code belongs to the product repository. Store-wide image or catalog changes are drafts
for the owner's approval. For research on which content formats travel, use the social
post-research workflow if installed; this skill covers in-product mechanics.
