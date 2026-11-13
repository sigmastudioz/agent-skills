# Retention and ranking patterns

Each pattern lists what it is, the signals it may use, a first construction, the guardrail and
the check. Sources are public creator breakdowns of large apps (language-learning, short video,
dating, consumer apps); treat their specifics as claims.

## 1. Daily return likelihood (language-learning apps)

- **What:** one number per user per day: the chance they open the product tomorrow.
- **Signals:** today's activity, days active in the last 7/28, how they opened the app
  (notification, widget, icon), unfinished items, recent first win.
- **First construction:** a transparent score (weighted recency and frequency) before any model;
  calibrate against next-day returns in history.
- **Use:** decides whether to send a nudge and which rescue action to offer; never shown as a
  judgement to the user.
- **Check:** calibration (predicted vs actual return by bucket) and holdout lift in next-day
  return.

## 2. Habit-timed nudges

- **What:** send the one daily reminder at the hour the user usually engages.
- **Signals:** the user's own past session start times in this product only.
- **Guardrail:** opt-in, quiet hours, one a day, easy off; never infer place or routine from
  networks, location or other apps.
- **Check:** open rate and opt-out rate versus fixed-time reminders.

## 3. Rescue action

- **What:** when return likelihood drops, offer the smallest useful win (a 5-minute workout, one
  episode to finish, a single lesson), not a streak warning.
- **Check:** completion of the offered action and the following day's return.

## 4. Per-item ranking (short-video feeds)

- **What:** before showing items, score each for this user (predicted finish, save, skip) and
  rank by it; mix in a share of fresh items so the feed doesn't narrow.
- **First construction:** content-based similarity to items the user finished, plus popularity
  among similar users; explain each suggestion.
- **Guardrail:** cap repeated categories, keep a diversity share, never rank by outrage or
  compulsive-use signals.
- **Check:** offline replay on history (did the top-k contain what they finished?), then a live
  holdout on completion.

## 5. Results-based asset choice (dating apps' photo selection)

- **What:** pick the lead photo, thumbnail or cover by measured response (click-through,
  add-to-cart, completion), not by guess.
- **Guardrail:** propose changes as drafts for the owner; never alter a person's own photos;
  enough traffic per variant before deciding.
- **Check:** a fair split test or a before/after with a stated window.

## 6. Upgrade timing

- **What:** show a paid offer right after a completed win, when value is felt.
- **Guardrail:** never at first launch, mid-task or by blocking progress; clear price and
  cancellation; no countdown pressure.
- **Check:** conversion together with refund and cancellation rates.

## 7. Speed to first win (from small-team app breakdowns)

- **What:** the time from install to the first meaningful success; front-load it in onboarding.
- **Check:** median time to first win and day-2 return, before and after.

## 8. Promise, quiz, plan, then price (onboarding to paywall)

- **What:** one promise and one button; a short quiz where every answer visibly shapes the plan;
  show the plan built from those answers before any price; then a paywall that shows exactly when
  money is taken (today: full plan; day 5: reminder; day 7: billing) with a "remind me before it
  ends" switch on by default.
- **Guardrail:** the quiz must change the plan for real; the price and billing day are on the same
  screen as the button; cancelling is as easy as starting.
- **Check:** quiz completion, trial start, trial-to-paid and refund/cancellation rates.

## 9. One number, a replay of real sessions, and a small test loop

- **What:** pick one number specific to the product (round length, time to first win, matches per
  user), add structured logging (OpenTelemetry) and session replays (consented, masked inputs),
  then repeat: propose the change most likely to move the number, test it on half of users, keep
  the winner.
- **Guardrail:** replays mask text fields and payment/health data and respect opt-out; one change
  at a time; trust signals (opt-outs, complaints, refunds) are guard metrics, not afterthoughts.
- **Check:** the number itself, with a stated test window and minimum sample.

## 10. Ask for a review after a win, without gating

- **What:** request the platform's native review prompt right after a completed win, not at launch
  or after a loss. A separate, clearly labelled "send feedback" option may sit beside it.
- **Guardrail:** never pre-select five stars, never route only happy users to the store and unhappy
  ones to a private form (review gating breaks App Store and Google Play rules), never reward ratings.
- **Check:** rating volume and average, and feedback-form volume, before and after.

## Avoid list: patterns seen in public app teardowns

These were shown in creator teardowns of top-grossing games and apps (claims with code excerpts;
treat details as unverified). Each one optimises revenue against the user. Do not build them, and
flag them in reviews:

- **Difficulty set by the user's ad value or spend**, not their skill: easing a run until the
  user's average length and then forcing a loss when a high-value ad is ready ("boost then kill",
  a scripted unwinnable turn), followed by a revive-for-an-ad offer.
- **Hidden harder copies of levels** (fewer moves, pieces chosen not to match) served to some
  users to push purchases; difficulty tuned so that a near-win sells the continue.
- **Quietly inflating results** (adding to a high score after a paid or ad revive) to bring people
  back.
- **Per-person pricing from a spend label** (a cheap first offer only for non-payers, then higher
  prices forever after the first purchase) and shop prices rewritten per user by remote rules.
- **Profiling by loading invisible ads** at sign-up to estimate a user's ad value.
- **Loss threats on exit** ("everything you are about to lose") to stop someone leaving.
- **Sending several purchase events to ad networks for one sale** to game ad optimisation.
- **Review gating** (pre-selected five stars; low ratings kept private).

Fair counterparts: dynamic difficulty that only helps a struggling player and is the same for
payers and non-payers; one public price list; a revive that is optional and does not change the
odds of the next turn; accurate conversion events.
