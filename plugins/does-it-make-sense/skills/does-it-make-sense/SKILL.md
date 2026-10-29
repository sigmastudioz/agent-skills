---
name: does-it-make-sense
description: Assess an existing build against its intended end goal. Explain actual behavior, trace user outcomes through implementation and downstream results, identify evidence-backed gaps, and recommend concrete refinements within the agreed scope. Use for post-build sense checks, outcome reviews, and requests to understand whether what was built solves the original problem. Excludes ordinary implementation, isolated code review, and checks concerned only with passing an already defined test gate.
---

# Does It Make Sense?
By Lex from SigmaStudioz.

Determine whether the intended user can achieve the intended result with the actual build.
Explain what exists, why it exists, where the evidence supports the goal, and what smallest
refinements would close demonstrated gaps. A build passing its tests can still leave the user's
job unfinished; an unfamiliar design can also be correct. Neither appearance establishes a verdict.

## Scope and authority

Default to assessment and recommendations. A request to think, review, trace or analyze does not
authorize product edits. When the user also authorizes refinement or fixes, implement only the
confirmed in-scope corrections, follow applicable engineering instructions, and retrace the affected
journey. Assessment does not authorize deployment, publication, new account access or external
messages. Do not add agents or tools merely to run this skill.

Use available project tools and existing review evidence. No particular framework, planning system,
knowledge graph or other skill is required. Reuse applicable architecture, UX, security or test
findings rather than repeating their audits. Scale depth to the requested feature and its risk.

## Establish the goal before judging the build

Read the original request, accepted decisions, relevant project instructions and current task record.
Establish the intended user, problem, observable end result, included workflows, non-goals and
material constraints. Identify the actual build/revision and environment under review, including
relevant uncommitted changes. Do not assume repository HEAD represents the running deployment.

Distinguish explicit requirements, accepted decisions, inferred goals and preferences. Trace changed
requirements to the latest authorized decision; do not treat an obsolete plan as the current contract.
If goals conflict, expose the conflict. Ask only when an unresolved choice materially changes the
judgment; continue independent inspection while that choice remains unresolved.

Check whether acceptance criteria represent the stated end goal. If all criteria can pass while the
user's job remains incomplete, explain the mismatch with a concrete scenario. An implied capability
is required only when its absence prevents the agreed outcome. A proposed broader outcome or new
product direction remains a decision for the user, not an automatic addition to the scope.

## Reconstruct what actually exists

Start from real user actions, commands, jobs or events. Inspect their actual entry points, relevant
implementation and configuration, state transitions, dependencies, downstream consumers and final
visible or usable results. Use running behavior when available and authorized. Documentation, test
names and prior completion claims are leads to verify, not proof of the current behavior.

Explain the build in plain language: what the user can do, what the system does, what it produces,
and what still requires manual intervention. Distinguish implemented, reachable, enabled, exercised
and deployed behavior. A component's existence or static reachability does not prove runtime success.

Bound the inventory to significant components and journeys needed for this goal. Follow a dependency
outside the feature when its behavior affects the outcome; do not expand into auditing that entire
subsystem. Mark inaccessible services and unknown consumers as evidence limits.

## Trace in both directions

For each important journey, connect:

**Original problem → intended outcome → required capability → actual entry point and implementation
→ state changes and downstream effects → observable result → evidence → gap or supported success.**

Trace backward from significant components to the outcome or constraint they serve. Flag unexplained
purpose, duplicate behavior or disproportionate complexity as candidates for investigation. A missing
explanation is not sufficient evidence that a component should be removed. Compatibility, recovery
and operational constraints may justify it.

Follow relevant alternatives: rejection, empty or invalid state, missing permission, cancellation,
timeout, retry, duplicate delivery, partial success and recovery. Select cases according to the
actual workflow; do not manufacture a universal checklist. Continue past an intermediate success
response to the terminal result: persisted state, completed work, delivered output, and whether the
user can understand or confirm the result. For asynchronous work, inspect the consumer and final
status rather than treating an accepted or queued response as completion.

Keep a compact trace table or equivalent narrative:

| Goal / journey | Actual path and terminal result | Evidence and limits | Outcome coverage / gap |
| --- | --- | --- | --- |

Cite real file/symbol references, artifacts, commands or observations. Tie evidence to the reviewed
revision/environment and actual observation time. Reuse matching evidence; do not relabel old runtime
observations as fresh. Distinguish observed behavior, static inference and unresolved assumptions.
Report traced and excluded journeys; do not claim a whole-product audit from a sampled feature path.

## Challenge and classify candidate gaps

Try to disprove each candidate before reporting it. Look for existing behavior, alternative entry
points, documented tradeoffs and legitimate differences between consumers. Check whether the issue
predates the reviewed change before attributing it. Challenge the agent's own earlier implementation
and plans against the original goal, using the same evidence standard as anyone else's work.

Classify surviving findings:

- **Defect:** demonstrated behavior violates an agreed requirement or invariant.
- **Integration gap:** capability exists but a real entry point, connection or consumer is missing.
- **Required capability gap:** the agreed end goal cannot be reached because necessary behavior is absent.
- **Goal/criteria mismatch:** the stated acceptance or design assumptions do not adequately establish the
  intended outcome; identify which decision needs clarification.
- **Refinement opportunity:** an evidenced friction, complexity or weakness can be reduced within the
  existing outcome, without inventing a new requirement.
- **Unverified path:** evidence or access is insufficient; state the exact missing proof.

Missing access is not product failure. Speculation is not a reproduced defect. Passing component
tests does not prove a complete journey. Evidence that a flow works does not prove real-world
adoption or effectiveness without appropriate user/operational evidence. Separate those conclusions.

## Recommend concrete, bounded refinements

Every recommendation must identify the affected goal/journey, supporting evidence, user impact,
smallest sufficient change, responsible layer or owner, and an observable closure check. Describe
what the user will be able to do or confirm afterward. Note material tradeoffs or dependencies;
label effort estimates and their basis rather than inventing precision.

Prioritize outcome-blocking corrections first, followed by relevant refinements. Separate actions
needed for the agreed goal from optional additions or changes requiring a new product decision.
Do not turn every uncertainty into a new feature or an improvement list into an implementation mandate.
Prefer reuse, simplification or removing a proven unnecessary step when those meet the goal; a larger
redesign needs evidence that a smaller change cannot work.

For example, if the goal is operator recovery of a failed broadcast and retry already works but its
final result is invisible, recommend surfacing authoritative recovery state and verifying it against
the broadcast outcome. Additional dashboard charts need their own justification. If recovery state
already appears elsewhere in the normal journey, disprove or narrow the candidate instead.

A useful refinement entry is:

**Finding → goal impact → evidence → proposed change and owner → expected behavior → closure check
→ priority and scope status.**

It is valid to recommend no change. Stop suggesting refinements once the agreed outcome is adequately
supported and remaining ideas are optional. If implementation is authorized, close a finding only
after checking the repaired journey and affected consumers; record anything still blocked.

## Deliver a supported judgment

Adapt the length to the build. Give the reader:

1. **What exists:** a plain-language explanation of actual capability and material limitations.
2. **Goal assessment:** achieved, partially achieved, not achieved, or insufficient evidence, with
   reasons tied to covered journeys. Use a per-goal verdict when outcomes differ; do not hide a
   critical missing capability inside an average score.
3. **Trace:** the important connections from goal to terminal result, evidence and coverage limits.
4. **Findings and refinements:** prioritized concrete actions, with required corrections separated
   from optional improvements and unresolved product decisions.
5. **Stop/next action:** leave as is, perform bounded refinements, obtain specific proof, or resolve
   a named goal decision. State what was inspected/run and what remains unverified.

A functioning journey can have an achieved verdict with optional friction improvements. A known
missing essential capability supports not achieved or partially achieved, even if other paths lack
proof. Use insufficient evidence when a goal's judgment itself cannot be established; do not obscure
known failures with uncertainty about unrelated paths.

Use the project's existing owning task/gap record for durable findings and evidence. Keep stable
finding IDs and closure checks when follow-up work needs continuity. For a small assessment, the
response can be sufficient. Do not create duplicate status ledgers, routine evidence folders or
project-specific state inside this reusable skill. Preserve unresolved findings and revalidate
claims affected by later changes. End when the scoped judgment and justified next actions are clear.
