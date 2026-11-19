# Operations and release lifecycle

Read this when a change touches process startup or shutdown, deployment, release branches,
supervisors, scheduled automation, alerting or manual production operations. These rules carry the
same authority as [SKILL.md](../SKILL.md). They do not authorize deploying, restarting, changing
production settings or bypassing an owner's approval.

## Process lifecycle

- **Boot.** One owner runs schema DDL, indexes and migrations. Serving and read-only processes bind
  to an existing schema; they do not create collections or tables at startup. A dependency the
  process does not serve must not be able to stop it booting. Cold and headless entrypoints get
  their own smoke check on a fresh install.
- **Shutdown.** Stop accepting new work first, then drain in-flight work with a deadline shorter
  than the supervisor's kill timeout. Bound and log each shutdown step, make a second overlapping
  stop a no-op, and test with a real server and a request in flight.
- **Reboot.** Deployment acceptance includes surviving a host reboot: the supervisor is enabled at
  boot and its process list is saved. Record any service that needs a manual unlock.
- **Crash leftovers.** Cleanup in `finally` or exit handlers does not run after a hard crash. Reap
  orphaned children and temporary directories at startup, and tie child processes to the parent's
  lifetime.
- **Reload semantics.** Confirm what a supervisor reload re-resolves. A reload can keep serving the
  previous release directory behind a symlink; verify the running revision after every deploy.
  Fingerprint static assets so caches cannot serve an old build.

## Release flow

- Read the served revision on each host before calling a change live; release numbers are build
  numbers of whichever pipeline ran last, and several pipelines can run at once.
- Land every out-of-band hotfix in the release branch before the next pipeline runs, or the next
  release overwrites it. A pipeline that is red and therefore not deploying is an incident.
- Build release artifacts and run release gates from a clean export of exactly what is staged,
  without local configuration, and record its fingerprint.
- Test a published package from each consumer's real import style: root and deep imports, each
  module-resolution mode, side-effect registration and cold start. Keep `exports` and
  `typesVersions` (or the equivalent) in sync with a test.
- After a manifest or version bump, refresh the lockfile with the repository's documented command
  and check it for collateral removals before committing.

## Manual operations

Manual operations run the same guards the automated path runs. Before a hand restart, configuration
change or data repair, run the guard or preflight the pipeline would have run; approval of a
setting change is not approval to skip the guard. Never chain a commit or push after a merge in one
shell command; stop and inspect conflicts. Prefer read-only probes, resolve every collection,
database and field name from the schema, and treat a zero result as unverified until the probe has
found a known-present item.

## Enabling automation and alerts

- Enable automation that acts on many records behind an allowlist or canary first. Compare dry-run
  counts against expectations, then widen in steps; record each step and its rollback.
- Verify that each alert reaches a receiver and that a fail-safe timeout or freeze raises its own
  alarm. An alert with no configured destination pages nobody.
- When the same incident recurs, stop symptom repair from the second occurrence: count recurrences
  in the owning ledger and make prevention of the mechanism the blocking next action.
