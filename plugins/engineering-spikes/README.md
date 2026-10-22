# Engineering Spikes

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version 1.0.0.

Turn engineering uncertainty into a bounded investigation, an evidence-backed recommendation,
and two separate documents: one for stakeholders and one for engineers. Covers the full spike
lifecycle: planning, research, experiments, gap tracing, decisions, handoff and documentation.

## Install

```sh
npx skills add sigmastudioz/agent-skills --skill engineering-spikes
```

For Claude Code, register this repository and select the independent plugin:

```sh
claude plugin marketplace add sigmastudioz/agent-skills
claude plugin install engineering-spikes@sigmastudioz
```

Claude, Cursor and Codex manifests are included. Native marketplace review is separate from
repository availability. Relevant requests can select the skill through normal host discovery;
this does not install a global rule or guarantee selection on every host/model.

## What the skill delivers

| Stage | Result |
| --- | --- |
| Frame | Decision question, scope, timebox, constraints and observable exit criteria |
| Compare | Real options evaluated against the same criteria, with hard failures visible |
| Investigate | Bounded experiments and source research; proposed work kept distinct from actual runs |
| Trace | Questions connected to evidence, findings, gaps and decision consequences |
| Close | Proceed, reject, further investigation or no decision, with confidence and follow-up owners |
| Communicate | Separate Non-Technical and Technical Docs with matching conclusions and limitations |

The stakeholder document explains what and why without code or engineering jargon. The
technical document explains how, including architecture, APIs, data models, code, dependencies,
failure paths and trade-offs when relevant. Both remain useful when the spike is blocked or
inconclusive. A recommendation never stands in for the decision maker's approval.

## Confluence delivery

Default output is two separate basic HTML documents: open each in a browser, then copy its
rendered content into the intended Confluence page. Editable Markdown companions can be included.
Raw Markdown and Mermaid are not assumed to become native Confluence formatting automatically.
Workflow diagrams are conditional, with captions and textual fallbacks; trivial spikes omit them.
Actual paste results depend on the editor and must be verified separately from a local preview.

No Confluence account, MCP service, paid API or helper dependency is required. Publishing pages,
uploading attachments and external experiments require an authorized destination and scope.

## Example requests

1. “Plan a one-day spike to decide whether our existing export flow can support larger reports.
   Define disproof criteria, compare realistic options and prepare both audience documents.”
2. “Run the approved local feasibility experiment. Trace the actual callers, storage and failure
   paths, record the evidence, and stop at the agreed timebox.”
3. “Write up these supplied findings. The preferred option missed its target. Produce separate
   stakeholder and engineering documents without inventing a successful outcome or new test run.”
4. “Resume this blocked spike using the updated source. Reopen affected claims and identify
   what evidence is still needed before we can decide.”

## Resources and verification

- [Skill instructions](skills/engineering-spikes/SKILL.md)
- [Stakeholder template](skills/engineering-spikes/assets/non-technical.template.md)
- [Engineering template](skills/engineering-spikes/assets/technical.template.md)
- [Confluence delivery notes](skills/engineering-spikes/references/confluence.md)
- [Design gaps and validation scope](https://github.com/sigmastudioz/agent-skills/blob/main/docs/engineering-spikes-validation.md)
- [Privacy](https://github.com/sigmastudioz/agent-skills/blob/main/PRIVACY.md)

This package contains instructions and templates, with no executable helper, installer or publisher
backend. Documents and experiment artifacts may contain user-controlled confidential material;
audience and access classification are separate. Packaging checks and authored scenario reviews
do not establish fresh native-agent efficacy, Confluence paste fidelity or marketplace approval.
Report issues without private evidence or credentials.
