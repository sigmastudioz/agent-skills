# Privacy policy and data handling

Last updated: November 28, 2026. Publisher: Lex from SigmaStudioz.

This policy covers the twelve plugins currently distributed in this repository:
Principal Driven Domain Design (domain-driven-design), SigmaStudioz Visualizer (visualizer),
SigmaStudioz Video Analysis (video-analysis), Engineering Spikes (engineering-spikes),
UI Foundation Reuse (ui-foundation-reuse), Does It Make Sense? (does-it-make-sense),
What If Tony Stark Built This (what-if-tony-stark-built-this), Returncraft (app-retention),
Delegating to Agents (delegating-to-agents), Senior Digital Skills Class (senior-digital-skills),
Slipstream (slipstream) and Follow-Through (follow-through).

## Shared behavior and user control

These plugins provide instructions and optional local Python/Node.js helpers. There is no publisher-hosted
backend, account system or telemetry endpoint. Shipped helpers do not send media or project data to
the publisher. The Video Analysis sampler invokes existing local FFmpeg/ffprobe; it does not install
dependencies or download speech models. No hooks automatically register these media helpers.

The host agent may use local or external rendering, transcription or generation tools authorized
by the user. Those providers may process supplied content under their own terms/settings. Selecting
a skill does not authorize uploading private media, publishing an analysis or creating paid jobs.
Keep private reference media, transcripts and extracted evidence out of public export packages.

Engineering Spikes has no executable helper, publisher service or required external connector.
During a user-requested investigation, the host agent may read supplied tickets, findings and
permitted repository files, then create local stakeholder and technical documents, evidence
records or isolated experiment artifacts. These can contain personal or confidential information.
Local retention and deletion remain under the user's control; the publisher receives and retains
none of these artifacts through a publisher service.

Optional research and experiments use only tools and destinations authorized by the user. A host
browser or research provider may process search queries or other content deliberately supplied
to it; the applicable provider depends on the user's tools and account settings. No external
research provider, experiment service or Confluence connection is required by this package.
Review the chosen provider's privacy policy before sharing restricted evidence. Invoking the
skill does not authorize uploading private files, spending money, or publishing pages or attachments.

The coding agent reads project files and uses the tools permitted by its host. The optional
handoff helper reads the host-provided session transcript locally to check explicit teammate
limits, reads the installed baseline, and returns handoff instructions to the local agent runtime.
It does not upload transcript contents to the publisher. The agent provider may process project
context and prompts according to the user's account settings and that provider's terms.

The skill asks agents to keep credentials and private payloads out of handoff notes. Users remain
in control of host permissions and which repositories the agent can access. Installing the plugin
does not silently install global rules or enable the optional helper; see [setup](SETUP.md).

Support is through [GitHub Issues](https://github.com/sigmastudioz/agent-skills/issues). Issues are
public; do not include credentials, private source, personal records or raw agent session logs.
This notice describes these plugins' behavior; it does not replace the host provider's policies.

UI Foundation Reuse reads its local runtime metadata/archive and a selected app manifest,
then copies a checksum-verified archive into that app's vendor directory. It does not
download code, install dependencies, send data or modify package manifests. A separately
authorized package-manager install can access its configured registries for external peers.
Visualizer's optional local renderer reads user-controlled scene/font files and invokes
local FFmpeg to write video, captions and posters; no publisher service receives them.

Visualizer's optional sound bridge sends the selected search terms and source/license
filters to Openverse, then downloads a chosen asset from its source host. Those services
receive the network request under their own policies. The bridge does not upload local
media, project files or narration. It stores result metadata, the rights-review note,
asset hashes, cue plans, runtime paths and mix reports locally in the selected project.
Earshot bank rendering and Real SFX mixing run in a separately configured local runtime;
the bridge disables optional model fetching and does not register an MCP server. Installing
the skill does not install that runtime or authorize new uploads, accounts or paid calls.

Does It Make Sense? provides instructions for reviewing a user-authorized build and its
goal/evidence records. It has no executable helper, publisher backend or required external
connector. Assessment may read confidential project context and produce local findings;
keep them in the owning project. Implementation, external messages and uploads require
the corresponding user authorization. Host/provider data handling remains applicable.

Slipstream reads local agent logs (Claude Code session transcripts and Codex rollouts under the
user's home directory) to compute token totals, skill usage and prompt-to-skill pairs, and reads
local skill and plugin folders to build a catalog. Results stay in `~/.claude/skill-library/`;
nothing is sent anywhere. Its hooks are not registered on install: `lean_setup.py --apply` adds
them to the user's settings only when run, after a dry run, and `--undo` removes them. The prompt
hint reads only the current prompt and the local catalog. The Cursor helper parses a CSV the user
exported from their own Cursor account. No publisher service, account or network access is used.

## What If Tony Stark Built This

The guidance can use project requirements, source code, test cases and experiment results that
the user authorizes the host agent to access. Its optional Python comparison runner reads a
local experiment manifest, selected implementation modules and JSON input cases. It starts
local Python processes and writes measurement/error reports in the selected output location.
The runner does not contain a publisher upload endpoint. Selected implementation code runs
with the local process's access, can itself read files or use the network, and is not sandboxed.
Inspect that code and its inputs before execution; do not put credentials or private payloads
in reports intended for sharing. Experiment files remain under the user's storage controls.

## Returncraft (app-retention)

This is guidance for designing retention, ranking and experiments in a user's own product.
It may use authorized product requirements and aggregate or de-identified usage evidence.
The package does not include an analytics collector, tracking SDK, advertising service,
notification sender or publisher database. Feature code and any data collection implemented
in the consuming product are owned by that product and subject to its own privacy policy.
The guidance calls for data the product already collects for its own purposes, user controls
and no third-party tracking, fingerprinting or data-broker input. Avoid sharing identifiable
customer records with a host or external tool unless the user has authority to do so.

## Senior Digital Skills Class

This guidance helps prepare lesson plans, practice materials, budgets, funding research and
learning-outcome summaries. It has no executable helper, learner account system or publisher
collection service. Use dummy information for sensitive exercises and anonymous outcome checks
where possible. Do not record learner passwords, verification codes, payment details, government
identifiers, health records or private messages in prompts or teaching materials. Learners keep
control of their own devices and accounts. Authorized web research is handled by the chosen host
or research provider, not by a publisher-hosted service.

## Delegating to Agents

This guidance helps prepare task briefs, progress notes, handoff contracts and reports using
user-authorized project context. It does not launch a worker, register hooks or send a brief on
its own. A host or worker service selected by the user may receive the context deliberately
included in an authorized assignment, under that service's policies. Keep credentials and
unnecessary private context out of briefs and use project-owned storage for resulting records.

## Follow-Through

The local Python tool reads and writes task titles, completion criteria, status, next steps and
evidence in a JSON task tree. The default store is under ~/.follow-through/; the user can select
a different path. Optional owner-configured hooks read the tree and local session identifiers
and print reminders to the host. The tool does not make network requests or send task records
to the publisher. A host agent can still process a reminder or task content under the host's own
privacy settings. Task files can contain confidential project information; choose titles and
evidence accordingly and control access to the storage location.

## Storage, deletion and privacy questions

There is no publisher-operated storage or retention period for local task, media, experiment or
project files produced by these packages. Files remain until the user or their own software
changes or deletes them; local tools do not provide automatic deletion of all outputs or host
history. Users can inspect, edit or remove their local files. Backups, host conversation history,
external-provider retention and any consuming application's data require that owner's controls.
Removing a plugin does not necessarily remove its previously created files or configured hooks.

For privacy questions contact ojo@sigmastudioz.com. Public GitHub issues are also available for
non-sensitive support. Information deliberately sent in a support email or public issue is
received through the email or GitHub service to respond to the request; do not send credentials,
private source, raw session logs or learner/customer records. Do not use a public issue for a
private deletion request. These support channels have their own provider retention controls.
