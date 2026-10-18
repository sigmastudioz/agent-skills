# Principal Domain-Driven Design

By [Lex from SigmaStudioz](https://github.com/sigmastudioz). Plugin version 1.0.4.

A principal-level engineering baseline for application/API/worker/monorepo changes. Group code by
its owning domain, then by function; keep services and shared modules at the narrowest useful scope.
Reuse an owned engine when actual consumers share a cohesive algorithm. Trace created modules and
changed paths through callers, dependencies, consumers and relevant failures; fix authorized gaps.

The instruction file is 535 lines; its complete skill folder is **598 lines** with metadata and
its optional native Claude delegation helper. Small fixes stay small. Read-only reviews stay
read-only. The baseline does not authorize extra agents, unrelated restructuring or deployment.

## Installation and automatic use

After registering the collection catalog, install only this plugin:

```sh
claude plugin install domain-driven-design@sigmastudioz --scope user
```

For Codex and Cursor instructions, see the [collection README](../../README.md).
For ordinary coding tasks to apply the baseline without trigger words, follow the one-time
user-approved [global setup](../../SETUP.md). Native discovery alone does not force every runtime
to apply every rule. Hosts that disable user instructions and remote/cloud agents need separate setup.

## Handoffs

Pass the accessible baseline, workspace/revision, ownership, contracts, current state, evidence,
trace obligations, checks and expected return format. Do not assume a worker inherits context.
The optional Claude hook checks structured handoff presence and includes the complete baseline
in the worker's actual assignment. It preserves other tool arguments and native permission decisions.
It does not prove the handoff's truth or the worker's adherence; verify the integrated result.

## Validation status

Fresh Cursor Agent CLI: 16/16 external feature checks and 2/2 original regressions pass. The agent
loaded the skill automatically, delegated one bounded task, integrated the result and ran checks.
Fresh Claude Code confirmation completed: 15/16 external feature checks and 2/2 original
regressions pass. The missing case is a compound-identity collision caused by joining unrestricted
IDs with a NUL delimiter. Four actual teammates ran despite the request for one. The handoff guard
rejected incomplete assignments and accepted corrected ones, but does not enforce agent budgets
or semantic correctness. Automatic baseline loading/delivery works; full adherence is unvalidated.

Earlier iterations exposed incomplete handoffs, excess delegated roles and compound-identity
collisions; those failures are retained in the maintainer's experiment evidence. Do not claim that
all initial attempts passed. Cursor desktop UI, cloud agents, production concurrency and performance
were not established by the small dependency-free billing fixture.

A sanitized [validation receipt](../../docs/validation.json) records counts and evidence hashes.

The current publication remains a preview, licensed under [MIT](LICENSE).
See [publication details](../../PUBLISHING.md). Publisher identity in
an official directory also depends on the platform's verification, not only local author metadata.

The public repository is https://github.com/sigmastudioz/agent-skills.
This plugin is the first collection entry. Future plugins can own their own versions and skills.
