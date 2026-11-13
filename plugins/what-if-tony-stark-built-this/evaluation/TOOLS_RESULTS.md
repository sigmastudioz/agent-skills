# Tool-enabled coding trial: diagnosis and evidence

Version 1.2.0, November 12, 2026. This report preserves the first pilot rather than replacing its
negative/null results. The [frozen trial protocol](TOOLS_PROTOCOL.md) defines the comparison.

## Why the first pilot barely helped

Several limits are directly supported by its artifacts:

- Both coding tasks reached full correctness in both conditions, leaving no correctness headroom.
- Inline task prompts already supplied extensive case lists, so the models had little need to discover
  requirements through callers, persisted state or consumers.
- Tools were forbidden. The skill's advice to build a reproducer, inspect a repository, change code
  and retrace a real consumer could not be exercised by the evaluated agent.
- Every reference was supplied inline, adding 43,882 prompt bytes. That imposed context overhead
  without adding a corresponding observed coding-quality gain.

Those facts establish experiment limitations. They do not isolate which factor caused the small
effect: task, tool access and guidance size were not independently varied. A further plausible
explanation is redundant advice: the control agents already perform many of these engineering steps.
The new trial's tool traces let us inspect that explanation directly.

## What was improved before the new trial

The skill entry point was reduced from 178 to 89 lines. System Map, Gap Radar, Failure Lab,
Impact Trace, Repair Loop and Evidence Memory remain its six capabilities, selected by need.
Runtime guidance now routes coding to one 560-word, 3,776-byte reference. Other references load
only for a named uncertainty; existing applicable specialist guidance should not be repeated.

The selected [coding loop](../skills/what-if-tony-stark-built-this/references/coding-loop.md) emphasizes
actions: follow an actual consumer, identify a broken contract, reproduce it on the unchanged code,
repair its authoritative owner, and check the final path/recovery. It asks for runnable evidence
instead of substituting a report or proposed test for authorized execution. The guide was frozen
before dispatch and contains no fixture-specific symbol names, hidden test cases or prior answers.

The selected resource is about 91% smaller than the old full-inline addition. That is a guidance-byte
comparison, not a claim of an equivalent total-token, runtime or cost reduction.

## Matched coding work

Two fresh standard-library Python repositories each contain several modules, SQLite persistence,
a supported CLI, documented contracts and passing public tests:

- **Local Relay:** durable delivery, competing claims, lease ownership/replacement, transport failure,
  replay and legacy provider identities. Three public tests; 15 held-out behavioral checks.
- **Restartable CSV Import:** batch interruption/process death, logical CSV rows, content identity,
  tenant isolation, immutable records and durable CLI status. Two public tests; 18 held-out checks.

Each model/condition starts from an independent writable clone of the same task's committed base.
The ticket, source, public contracts, tools, common engineering defaults and 1,200-second limit match.
The control gets no additional Stark guidance. The treatment gets only the coding-loop file,
copied byte-for-byte. Hidden tests, other skill references, templates and historical results remain
outside the worker checkout. Models are `grok-4.7-high` and `claude-fable-5-2-high`, retaining the
previous pilot's model settings. Eight fresh processes, maximum three active; no model reruns or
feedback after scoring. Shared starting fixtures, selected guide, contracts and held-out checks
stayed frozen; worker code changes are the outputs being measured.

Both conditions retain the user's standing engineering defaults, including relevant DDD principles.
This measures marginal added Stark guidance over that setup, not a blank agent without instructions.
Cursor global metadata/settings may also remain common. Explicit outside reads and tool actions
are audited; hidden service context is not fully observable.

## Grading and interpretation

Final package snapshots are inspected before local execution. The coordinator grades them in fresh
directories with the original public tests restored, then runs the frozen held-out checker. Worker
test rewrites cannot redefine acceptance. Behavioral counts use distinct test methods, not the number
of failed subtests. Process completion, behavior, scope observations and tool activity are separate.

The checker exercises actual SQLite behavior, controlled concurrency, injected failures, a child
process exiting mid-batch, reopened stores and the public CLI. It does not establish a real remote
provider guarantee, power-loss durability, production workload behavior or universal correctness.

The coordinator authored the skill and tasks. Code checks are objective against frozen expectations,
but the study is not independently designed. One process per task/model/condition cannot establish
statistical significance or broad efficacy. Tool latency and provider counters are descriptive under
shared services and concurrent execution; no monetary cost is inferred.

The first reviewed controls already added regressions, exercised the CLI and checked new tests
against their base revision. This supports the redundancy explanation on these tasks. It does not
show that the guide is unnecessary for every model, user or less-specified project.


## Observed results

Every original public suite passed. The table reports held-out checks on the frozen code, followed
by whether the agent actually completed within the fixed 20-minute limit. A timeout is not a completed
solution even when the code passes. No deadline was extended and no cell was retried.

| Model | Task | No added skill | Relevant guide only |
| --- | --- | --- | --- |
| Fable 5.2 high | Relay | 15/15; completed, 363.7 s | 15/15; completed, 387.4 s |
| Fable 5.2 high | Importer | 18/18; completed, 374.9 s | 18/18; completed, 392.8 s |
| Grok 4.7 high | Relay | 15/15; completed, 1177.8 s | 4/15; timeout at 1200 s |
| Grok 4.7 high | Importer | 18/18; completed, 1184.3 s | 18/18; timeout at 1200 s |

All four controls completed and passed acceptance. Two of four guided runs completed and passed;
three of four guided frozen implementations passed. Guided Grok Relay changed no application source:
it reproduced failures and added regressions but reached the bound before repair. Its 4/15 matches
the initial broken implementation. Guided Grok Importer produced correct code and ran local checks,
but never returned a final completion before the bound. These are distinct failure outcomes.

Fable's mean completion time was 369.3 s without versus 390.1 s with guidance, approximately 5.6%
longer in this sample. Grok's guided timeouts are censored; do not average them as completion times.
The two Grok controls also used nearly the whole budget. Shared service latency and one sample per
cell prevent attributing these time differences solely to the guidance.

| Model/task | Control tool starts | Guided tool starts | Guided file reads |
| --- | ---: | ---: | ---: |
| Fable Relay | 19 | 24 | 1 |
| Fable Importer | 22 | 23 | 1 |
| Grok Relay | 31 | 23 | 1 |
| Grok Importer | 33 | 34 | 1 |

Tool starts describe activity, not useful work or cost. Raw provider counters are retained separately;
usage is absent for timed-out calls, and provider fields are not normalized or converted to money.

## What the traces change about the diagnosis

The control runs independently added recovery regressions, repaired authoritative state and exercised
real CLI/persistence paths. Some also replayed new tests against the base source. The guide therefore
repeats capabilities these models already demonstrate under the common task and engineering defaults.
This is stronger evidence for redundancy in this setting than the first no-tool pilot provided.

The guided Grok Relay run made several exploratory probes, wrote a substantial failing regression
suite, inspected its failure output and then hit the bound without repairing application code.
That is an observed investigation-before-implementation bottleneck. The guide emphasizes reproducing
the broken contract, so process overhead is a plausible contributor, but a single run cannot prove
that this instruction caused the timeout. The selected guide's smaller context did not establish a
correctness or completion advantage. The trial supplies no evidence for marketing the six capabilities
as a general performance improvement over a strong coding baseline.

The implemented 1.2 changes improve focus and reduce supplied instruction bytes; efficacy remains a
separate, unproven claim. The evaluated runtime is retained unchanged after dispatch. Adding fixture-
specific rules now and replaying these same tasks would be tuning, not independent confirmation.
A future revision should test a narrower, distinctive intervention on unseen work with repetitions,
rather than adding more universal workflow requirements to chase these scores. This report does not
claim that future revision or those additional runs were performed.

## Scope review and evidence

All eight final source snapshots and shell commands were inspected before grading. Original public
test files, README contracts, common AGENTS instructions and selected guidance remained unchanged.
Every treatment read the guidance file once; controls did not read it. No explicit reads of global
Stark instructions, historical results or the hidden checker were observed. All worker Git revisions
remained at their initial base; snapshots contain no symlinks.

Grok Relay's guided run read a Cursor-generated file outside its checkout twice. The preceding shell
receipt identifies that exact file as its own failing unittest output. This departs from the protocol's
literal no-outside-read wording, but supplies no new task input or hidden-test leakage; the run
already fails both behavior and completion acceptance. Grok Importer's guided run used both an explicit PID kill and a broad
`pkill -f "batch_size=0"` cleanup after a hanging probe. The probe later stopped, but the broad pattern
was not proven limited to its owned process. No collateral failure was established. This remains an
operational containment uncertainty, independent of its passing code and timeout.

The durable audit bundle is linked from the collection's existing gap ledger. It retains exact
fixtures, guide, prompts, frozen checker/protocol, final code and diffs, local grade receipts, provider
counters, tool-call receipts and raw-stream hashes. Service thinking payloads and credentials are
excluded. A manifest and fresh-directory restoration check establish archive integrity; they do not
turn a failed or timed-out run into a pass. The earlier pilot and its archive remain intact.
