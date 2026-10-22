---
name: engineering-spikes
description: Plan and run timeboxed engineering spikes, trace questions to evidence and decisions, and produce separate stakeholder and engineering documents ready for Confluence. Use for feasibility research, technical discovery, proofs of concept, or spike write-ups. Excludes ordinary feature delivery, general essays, and financial price spikes.
---

# Engineering Spikes
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Reduce a specific uncertainty enough to support a decision. A spike is complete when its
questions have evidence-backed answers or a bounded explanation of what remains unknown.
Producing code, reading sources, or reaching a preferred answer does not establish feasibility.

## Scope and operating modes

Apply automatically to relevant spike work. Do not copy `alwaysApply: true` into unrelated
host settings or run this process for every coding task. Use the user's requested mode:

- **Plan:** frame questions, evidence needs and experiments; do not report proposed work as run.
- **Investigate:** execute authorized research/experiments and maintain both audience documents.
- **Document:** synthesize supplied findings without silently launching new experiments.
- **Resume:** read the prior documents and evidence; reopen claims affected by changed sources.

Use available host tools. No MCP server, paid service, renderer, or particular agent is required.
Research permission does not authorize production changes, purchases, new account access,
Confluence publication, or accepting terms. Keep prototypes isolated and reversible. Respect the
user's experiment budget, data permissions and teammate limit; this skill does not add agents.

## 1. Frame the spike

Inspect the ticket, existing decisions, relevant code/contracts and supplied evidence before
inventing a solution. Establish the following in the technical document; summarize their business
meaning in the stakeholder document:

| Frame | Capture |
| --- | --- |
| Identity | Stable spike ID, title, owner, decision maker, date and related ticket |
| Question | The decision this spike supports and the uncertainty preventing it |
| Scope | Included workflows, explicit non-goals and affected audiences/systems |
| Constraints | Timebox, cost/resource limits, access, compatibility and relevant quality needs |
| Exit criteria | Observable evidence needed to answer each question, including disproof |
| Status | Planned, running, blocked, complete or cancelled; separate from the decision outcome |

Ask only for missing facts that block safe execution or the decision itself. Otherwise identify
proposed assumptions and proceed with independent work. An unspecified timebox is a proposal,
not an approved extension or spending limit. Scale the investigation to the uncertainty.

Create two distinct documents from the start, even for a plan or inconclusive result. Use
`<spike-id>-non-technical` and `<spike-id>-technical` filenames, or two named Confluence pages.
Give each the same spike ID, status, update date and a link to its companion. Never combine
them into one document, even when the request arrives as one ticket.

## 2. Compare realistic options

Consider the current approach or doing nothing where viable, plus plausible alternatives.
Do not manufacture options to meet a count. Compare against the same decision criteria.
Separate hard constraints from preferences; do not hide a hard failure inside an average score.

Record cost, delivery effort, operational burden, user impact and reversibility when relevant.
Label estimates with their basis and uncertainty. Explain why an option is rejected or deferred.
An architecture, API or data-model section may be inapplicable; say why instead of inventing one.

## 3. Investigate and preserve evidence

Prioritize the cheapest experiment or source that could overturn the preferred option.
Use authoritative documentation for external contracts and inspect real local callers, producers,
consumers and failure paths for repository claims. Record unavailable remote internals as a limit.

Before an experiment, record the hypothesis, method, baseline/comparator, acceptance threshold,
environment, inputs, resource bound and expected artifacts. Distinguish a proposed check from a
completed check. Record actual commands or steps, results, failures and cleanup afterward.
Do not infer a production guarantee from a small synthetic proof of concept or static review.

Use stable question, evidence and gap IDs, such as Q1, E1 and G1. In the technical document keep:

| Evidence | Source/revision and date | Method and conditions | Observation | Limits |
| --- | --- | --- | --- | --- |
| E1 | Actual URL, file/line, commit or supplied artifact | What was inspected or run | Supported fact | Missing coverage or uncertainty |

Keep observations, interpretations, assumptions and recommendations distinguishable. Conflicting
sources require an explicit resolution or unresolved contradiction. Negative results are findings.
Do not invent missing logs, performance numbers, interviews, approvals, prices or experiment runs.
Link reproducible artifacts without copying secrets, personal data or restricted project material
into broadly shared documents. Separate audience from access classification; engineers do not
automatically have permission to see every attachment.

## 4. Trace gaps to the decision

For each in-scope question, trace requirement -> option -> source/experiment -> finding ->
decision consequence. For a technical path, follow its actual entrypoint through dependencies,
state changes and downstream outcomes, including the relevant rejection or partial-failure case.
Test a proposed gap against existing contracts and the pre-spike baseline before calling it a bug.

| Gap | Expected outcome | Observed evidence | Impact on decision | Owner / next action / closure check |
| --- | --- | --- | --- | --- |
| G1 | Requirement or exit criterion | Evidence ID, contradiction or explicitly missing proof | Blocking, conditional or non-blocking, with reason | A bounded way to resolve or accept the uncertainty |

Distinguish a defect, missing integration, required feature, optional improvement and unverified
path. Missing access is not a failed product. A speculative risk is not a reproduced defect.
Resolve investigation gaps within the authorized scope; implementation outside the spike becomes
a named follow-up. Do not silently expand a discovery task into a production rewrite.

## 5. Stop and decide

Stop when exit criteria are met, the timebox/resource limit is reached, or an unchanged blocker
prevents useful progress. Preserve partial evidence; do not retry indefinitely or extend the budget
without authorization. Report elapsed effort only when measured; label estimates and proposals.

Use a supported outcome: **proceed**, **reject**, **further investigation**, or **no decision**.
State what the evidence supports, confidence and its basis, unresolved conditions, and a trigger
for revisiting. A recommendation is not the decision maker's approval. A blocked or cancelled
spike can still have a useful conclusion; do not label incomplete experiments complete.

Specify follow-up tasks with owners (or owner unassigned), dependencies, acceptance checks and
priority. Distinguish spike/prototype artifacts to retain, dispose of or harden before production.
Include rollback/recovery and operational work when the proposed adoption needs them.

## 6. Produce the two audience documents

Use [the stakeholder template](assets/non-technical.template.md) and
[the engineering template](assets/technical.template.md) as coverage guides. Adapt length and
omit genuinely irrelevant detail with a reason; replace all guidance before delivery.

**Non-Technical Doc:** plain-language summary, problem, scope, options, recommendation or
inconclusive outcome, evidence in business terms, risks, impact, next steps and decision needed.
Explain unavoidable product terms; omit code, API signatures, stack traces and engineering jargon.
It must stand alone without requiring stakeholders to read the technical companion.

**Technical Doc:** questions/criteria, current versus proposed design, architecture, APIs, data
models and snippets where relevant; method, evidence, results, trade-offs, dependencies, gap
trace, failure cases, constraints and adoption/handoff work. Label illustrative code and distinguish
tested prototype behavior from proposed implementation. It must support engineering review.

Both documents must agree on status, options, recommendation, confidence, risks, impact and
unresolved conditions. Translate the same evidence for each audience; do not dilute uncertainty
or claim a decision in the summary that the technical findings do not establish.

## 7. Deliver for Confluence and verify

Read [Confluence delivery](references/confluence.md) when producing the final artifacts.
Default to two separate basic HTML documents for rendered copying into Confluence, with editable
Markdown companions when useful or requested. A format variant is the same audience document,
not permission to merge the audience outputs. If files are unavailable, provide two separately
named rendered documents and explain any formatting limitations.

Use workflow diagrams only when they clarify a decision, interaction or failure path. Prefer
technical diagrams in the engineering document; a stakeholder diagram uses plain business labels.
Include a caption and textual fallback. Mermaid source alone is not a portable rendered diagram.
Skip diagrams for trivial investigations; do not add decorative workflows to fill a template.

Before delivery, check the question-to-evidence-to-decision trace, both audiences' consistency,
source links, table readability, code/diagram rendering and unresolved findings. A formatting check
does not verify technical claims. Report local rendering separately from an actual Confluence
paste test. Publishing pages or attachments requires the user's authorized destination and scope.

Finish with both document links, the supported outcome, remaining decision/blockers, and precisely
what was verified. Keep draft/review/approved publication state distinct from spike completion.
