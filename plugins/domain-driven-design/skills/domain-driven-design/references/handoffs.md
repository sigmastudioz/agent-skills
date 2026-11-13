# Agent handoffs and delegation

Read this in full before delegating, resuming a handoff, or coordinating concurrent agents. These
rules carry the same authority as [SKILL.md](../SKILL.md), which keeps the handoff-contract table
and the `HANDOFF_JSON=` field list for quick reference.

## Agent portability and handoffs

These are tool-neutral instructions for agents that can read Markdown and inspect a project.
Use available search, build, test, and runtime tools; no particular vendor, plugin, or CLI is required.
Honor the host's instruction hierarchy, permissions, and explicit task scope. This skill does not
enable disabled capabilities or grant permission to deploy, publish, or perform destructive changes.

When delegation is already authorized, pass the skill's accessible path or relevant instructions,
owned files/modules, acceptance conditions, and trace obligations in the assignment. Do not assume
a child agent inherits the parent's conversation, loaded skills, or global instruction files.
Require evidence and unresolved edges back from each worker; reconcile traces across worker boundaries.
Delegate verified invariants; label proposed algorithms as assumptions and challenge contradictions.
For each claim about library or runtime behaviour in the brief, state the exact command and options
that produced the evidence and its output, so a reviewer can see what was and was not tested.
If the child cannot read the skill, supply its relevant contents within the allowed context.
Do not spawn agents merely because this section describes handoffs.
Before adopting another workflow, record any explicit user-authorized teammate limit and roles.
Every new exploration, implementation and review agent consumes that budget; resuming an existing
agent does not allocate a new slot. Follow-up reviews stay in the coordinator when the budget is
exhausted. An absent numeric cap is not permission to delegate, and optional workflow skills cannot
expand the user's limit.
Treat task briefs and pseudocode as proposals: independently check their algorithms against the
original contract. Correct a flawed plan instead of preserving it as an implementation requirement.

### Handoff contract
The contract table (the fields every authorized agent assignment or resumable handoff must
identify) lives in [SKILL.md](../SKILL.md#agent-portability-and-handoffs); it is not repeated here.
The fields apply to every handoff someone else will act on. If the deliverable is a brief for a
person (a Markdown file, ticket or message), carry the same fields in prose: workspace and revision
(file hashes when there is no version control), owned files, current state including failing checks
and their cause, acceptance checks with their commands, and the return format. The `HANDOFF_JSON=`
prefix below applies only to agent and session tools.

Hosts may enforce this contract with a separately installed delegation guard. This guidance-only
skill contains no executable guard and does not download or enable one. The written handoff
contract applies whether or not a guard is installed.
The optional Claude guard supplies this baseline path and checks explicit numeric agent limits in the
native user turns (`Use N teammates/agents/workers` and common polite forms). Quoted, fenced or
negated examples cannot increase the cap. The first explicit cap starts a budget; repeating or
changing it retains usage within that budget. Only an explicit native instruction such as
`Start a new delegation budget: use N agents` resets it.
Malformed records do not erase a previously parsed cap. Missing history and natural-language
restrictions outside this limited parser remain the coordinator's responsibility. The runtime
must validate resumed agent identities. This local guard covers recognized coding workspaces;
an unrecognized workspace does not waive this baseline or grant delegation permission. It does
not establish remote accessibility or prove the semantic correctness of a handoff.
The guard intercepts Claude Code's `Task` and `Agent` subagent tools and the Claude desktop
session tool (`mcp__ccd_session__start_session`), so the hook matcher must name all three. For
the session tool, an offer card (title only) passes untouched because nothing runs; a proposal
with a brief is validated but not counted against the budget until the user starts it; a
`user_asked` start or a `proposal_id` start counts against the budget. A brief is checked when it
reads as coding work: implementation, repository, build, bug, feature, deploy, component, page or
API language, or a source-file extension. Prose-only assignments pass; that keyword gate is a
heuristic, so the coordinator still owns the contract for an assignment it does not catch.
The child must read the accessible baseline and relevant linked guidance before acting. The hook
adds a compact reminder rather than embedding the entire skill on every call; if the child cannot
access the skill, supply the relevant contents as required above. Repeated hook processing must
not duplicate that reminder or bypass validation and budget checks.
When that guard is installed, prefix the assignment with `HANDOFF_JSON=` and a JSON object with the
field list given in [SKILL.md](../SKILL.md#agent-portability-and-handoffs). `trace` names paths and
failure cases to follow; `checks` names checks to run or why unavailable. A rejected assignment must
be corrected before retrying.
Handoff fields must contain meaningful nonblank text or nonempty structured context; workspace and
baseline paths must be text. When `workspace` differs from the launch checkout, add an `isolation`
object with `confirmed: true`, the matching absolute `workspace`, and a nonblank `reason`. The
coordinator must verify that checkout and its authority; an isolation keyword in prose is not
confirmation. These declarations do not authorize a new workspace, branch, or external action.

### Examples: pattern or component

When a brief cites existing code as an example, say whether it is a pattern to copy or a component
to reuse, and state the invariant the worker must not break. Workers tend to reuse whatever is
named. Observed: a brief that cited an account-keyed rate-limit collection as "the pattern" for an
anonymous counter led the worker to write hashed anonymous IDs into that collection's `userId`
field, breaking the rule that anonymous identifiers never enter account-keyed records.

### Workers started from a shell

The guard sees only the agent and session tools above. An agent CLI launched through a shell
command (for example `cursor-agent -p`, `codex exec`, `claude --print`) is not intercepted, so the
coordinator enforces the contract. Keep the authoritative brief, job state and accepted report
outside the worker's writable scope; supply an accessible input copy and a named return channel.
When a write-capable worker would share another owner's uncommitted checkout, use a worktree cut
from a committed base that contains its authorized inputs. A read-only review can instead use an
isolated input packet without a checkout or commit. Include only the data and tools authorized for
that actor; a publisher's credentials or private runtime payloads do not belong in a review packet.
If dependency folders are linked from the main checkout, forbid installs. Prefer the CLI's
sandboxed mode; run-everything flags need the user's approval and may be refused by the host.

### Multi-stage batches and changing instructions

For delegated batch work, use the existing queue to carry each item's stable identity, input
revision, assigned actor, stage, holds and cumulative attempt budget. Keep the concurrency limit
separate from the total delegation and retry budgets; opening another batch, changing a variant or
resuming a worker does not reset them. Feed the next eligible item to an available authorized actor
when requested, without adding agents or passing over unresolved holds merely to keep slots busy.
Report actual running, completed, failed and pending work; a prepared packet is not a running agent.

Before launch, compare the actual brief and supplied inputs with that item: identity, revision,
reference roles, permitted actions and expected output. Copied task names or example references
can silently carry the previous item's requirements. Distinguish authoritative product/data or
identity references from examples whose styling or implementation may change. Freeze the launched
packet; never change it while a worker is reviewing it and attribute the result to the new inputs.

Name what a review's PASS establishes. Source sufficiency, output acceptance, persistence,
consumer-visible verification and replacement cleanup are different gates; use the stages the task
actually needs. Give every externally mutable resource an explicit writer; independent reviewers
need no write access. A worker recommendation cannot release a later gate outside its authority.
Verify the final exact artifact and its consumer before retiring the superseded version when that
ordering is required. For converted inputs, record source and supplied identities and the relevant
equivalence check; a changed container hash alone proves neither corruption nor pixel equivalence.

Before spending a limited correction, collect all assigned independent reviews and reconcile their
concrete findings against original evidence. A timeout or unopened input is unresolved, not PASS.
Review disagreement requires checking the claim, not a majority vote; estimates across unlike
examples are not measurements. Recover an existing complete report from a formatting or path-label
mismatch when the supplied input set is verified; do not rerun paid work solely to reformat it or
normalize missing evidence into acceptance.

When user feedback changes the brief during a job, record the new controlling revision and mark
affected outputs superseded or pending before they can be integrated or published. Preserve useful
unaffected work and prior failure evidence. Rebind the next assignment to the changed requirements
and recheck affected final-artifact gates. Carry cumulative attempts forward; a specifically
requested additional change is a scoped exception only to the extent actually authorized, not a
reset of unrelated limits or holds.

Reconcile accepted reports into the queue by item and revision, preserving earlier holds and
unresolved work. Count units from the pinned input/output manifest and inspected-item identities,
not report-row count: one row may describe several inputs and one output may serve several items.
Keep reviewed, accepted, persisted and consumer-verified totals distinct; partial coverage does not
establish whole-task completion. Observed examples and their limits are recorded in
[batch-review coordination](../tests/observed-batch-review-coordination.md).

### Reporting back up the chain

Reporting travels the whole chain: worker to coordinator, coordinator to the user, and coordinator
to whoever delegated the task to it. In the brief, require a progress line per named milestone,
a `BLOCKED` line for decisions the worker cannot make, a final report file and a `DONE` marker.
Watch the progress file with the host's event or monitor facility rather than repeated sleeps.
Forward each `BLOCKED` question promptly to the party that owns the decision, as one question.
Relay results upward only after reviewing the diff and re-running checks; report the worker's
claims and your verification separately, including what remains unverified.

### Paths and concurrency

Use actual paths on the receiving agent's host; include the necessary content when paths differ or
are inaccessible. Give commands their working directory and required non-secret configuration names.
Never place credentials or private runtime payloads in handoff notes. A branch name alone is not
proof that a child sees uncommitted work; establish whether the checkout is shared or isolated.

For concurrent work, agree public contracts and file ownership before overlapping changes. Tell
agents they are not alone: preserve others' edits and coordinate shared files through the assigned
owner. Rebase or reconcile isolated changes before claiming integration; do not silently discard work.
On return, report changed paths, public-contract changes, checks with outcomes, gap IDs/status, and
remaining actions. The coordinator reconciles the trace ledger and verifies cross-agent seams and
affected consumers; several passing worker checks do not establish a working integrated workflow.

For interruption or context loss, save the handoff in the existing task/trace record with a timestamp
and content revision, then link that record. On resume, inspect the checkout and current diff before
acting; revalidate stale assumptions. Do not create a second source of task truth.

Local installation does not imply cloud, remote-host, or unrelated agent installation. Establish
discovery on each execution host; use a host-native global instruction to route relevant work here.
If discovery or file access is unavailable, report that limit instead of claiming global enforcement.
