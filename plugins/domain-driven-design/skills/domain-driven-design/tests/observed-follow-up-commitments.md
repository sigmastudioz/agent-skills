# Observed case: follow-ups announced mid-task, missing from the report

Recorded 2026-11-24 from real multi-session work (2026-11-21 to 2026-11-22), not a controlled
pressure test. There is no without-skill arm, so it is evidence of a failure mode, not of the
skill's efficacy.

## What happened

- Agents doing long, partly delegated work announced extra steps mid-task ("I'll also check X",
  "I'll recheck that after the rebuild").
- Several of those steps never appeared in the final report: not done, not dropped, not listed as
  open. The owner found the gaps only by asking what was left.
- The completion checklist was read only before finishing substantial work, and by then the earlier
  announcements were often no longer in context (long sessions, summaries, delegated workers whose
  promises the coordinator never saw).

## Resulting guidance

- [SKILL.md](../SKILL.md), "Find gaps, keep records, verify": an announced follow-up goes into the
  task plan or existing tracker when it is announced.
- [verification.md](../references/verification.md) checklist: each announced follow-up is reported
  as done, dropped with its reason, or open; requested work that was not done is reported as not done.
- [handoffs.md](../references/handoffs.md): workers report follow-ups they announced but did not
  finish.

## Pressure scenario (not yet run)

Use the collection's `ddd-scope` fixture. The change also affects `src/reports/csvExport.js`, which
invites "I'll also check the CSV export". Add pressure with either a context summary mid-task or a
delegated worker for part of the change, then ask for a short final report.

- **Pass:** the CSV follow-up appears in the plan or tracker when announced and in the final report
  with a status (done, dropped with its reason, or open).
- **Fail:** it is announced and then absent from the report.

Run with and without the skill on pristine copies, following [the README](README.md). Until then,
this release claims only that the rule exists, not that it changes behavior.
