# Observed case: delegating to an agent CLI from a shell

Recorded 2026-11-12 from a real coordination session, not a controlled pressure test. There is no
without-skill arm, so it is evidence of a failure mode, not of the skill's efficacy.

## Setup

A coordinator delegated a backend-plus-app feature to `cursor-agent -p` in a git worktree cut from
a committed base, because the main checkout held the owner's uncommitted work. Dependency folders
were symlinked from the main checkout. The brief carried every handoff field, a progress-log
format with named milestones, a `BLOCKED` convention and a report file outside the worktree.

## What happened

- The host refused `cursor-agent --force` as an unsafe agent; `--sandbox enabled` without
  `--force` ran.
- Progress lines arrived as events through a file monitor, so each milestone was relayed to the
  user without sleeps.
- The brief named an account-keyed rate-limit collection as "the pattern" to reuse. The worker
  reused the collection itself, writing a hash of the anonymous install ID into its `userId`
  field, and noted "so we do not add a second collection". The plan's invariant (anonymous IDs
  never enter account-keyed records) was in the plan but not restated next to the example.
- The delegation guard did not see the CLI launch; the contract held only because the coordinator
  wrote it into the brief.
- The user asked for reports to reach the delegating agent as well as the user.

## Resulting guidance

[handoffs.md](../references/handoffs.md): "Examples: pattern or component", "Workers started from
a shell" and "Reporting back up the chain".
