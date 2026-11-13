# Matched instruction-ablation pilot

The user requested the same tasks with and without this skill using Cursor Grok and Fable models.
This is a bounded pilot, not a population-level efficacy or native automatic-discovery claim.

## Frozen design

- Four synthetic tasks: transactional code, a small sorting fix, system invention, and evidence-driven
  replanning. Two models, two conditions, one fresh session per cell: 16 model calls, no corrective reruns.
- Each pair shares the exact task, common engineering defaults, output contract, model identifier,
  read-only/no-tool limits and timeout. Only the explicit target-skill instruction body differs.
- The treatment contains runtime skill instructions, references and packet template; it excludes
  tests, benchmark questions, scoring criteria, previous reviews, results and project evidence.
- The control has no explicit target-skill body. Both run in the same Cursor installation/account.
  Global metadata/settings may remain common context; this estimates the added effect of the supplied
  instructions, not a guaranteed virgin model with no awareness of the installed skill.
- Runs are counterbalanced within model/task pairs and interleaved between models. At most three
  are active. Input hashes, actual process outcome, wall time, raw stream and final response are retained.
- No tools, source writes, shell commands, remote research or additional agents are permitted to the
  evaluated models. All synthetic source/material is inline. Tool calls invalidate a no-tool cell.
  Returned code is a proposed artifact, locally inspected and checked by the coordinator afterward.

## Acceptance and scoring

Freeze the tasks and rubric before dispatch. Hidden behavioral tests exercise the two code tasks;
ordinary source/contract requirements are visible in the task, while test implementations are not.
Run returned code only after inspecting it for unauthorized side effects, in an isolated temporary
directory under the host sandbox. A parse failure, timeout or scope violation remains a failure or
invalid cell; it is not silently retried or discarded. Validity and correctness are separate.

For the two reasoning tasks use the predeclared rubric, scoring each dimension 0 (absent/wrong),
1 (partial) or 2 (concrete and correct). Inspect anonymized outputs before revealing model/condition
mapping. The coordinator authored the tasks and skill, so scoring is condition-masked, not independent
or guaranteed inference-proof. Keep supporting excerpts and critical failures visible.

Report per-task results and matched differences for each model. Do not hide critical correctness or
scope failures inside a mean. Report output size and observed wall time separately; timing includes
service variability/concurrent scheduling and is descriptive, not a reliable efficiency estimate.
Use provider token/cost fields only when supplied and interpretable; otherwise mark unavailable.
One observation per cell cannot establish statistical significance or general reliability.

Do not tune the skill or rubric after seeing these results and call a rerun independent evidence.
Any resulting instruction change needs a new version and fresh tasks for a future evaluation.
Preserve negative and null results. The maintained skill can be useful while this pilot is inconclusive.

## Ownership and retention

The skill plugin owns this protocol, fixtures and evaluator. The collection tracker owns decisions.
An explicit user-requested behavioral audit justifies its evidence bundle. Keep prompts, hashes,
outputs, scores and restoration/interpretation notes with the owning collection; no credentials or
private project material belong in the bundle. Retain until superseded by a reviewed benchmark and
its results have no active consumer, then use the collection's evidence archival convention.
