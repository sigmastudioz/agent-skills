# Marketplace map and update workflow

Last reconciled: **November 28, 2026**. This opening section is the current destination map.
Older dated sections below are historical, including their old plugin counts and release scopes.
The approved public set is the **twelve entries in [catalog.json](catalog.json)**.

## Destinations and coverage

| Destination | Current recorded coverage | Update route |
| --- | --- | --- |
| [GitHub](https://github.com/sigmastudioz/agent-skills) | Twelve public source plugins with versioned releases. | Review scoped source; publish complete ZIPs for new versions; verify inventories and downloaded assets. Preserve old releases. |
| [Claude submissions](https://claude.ai/directory/manage) | Eight earlier submitted identities plus Senior Digital Skills submitted November28; Delegating has one saved draft. Slipstream and Follow-Through are blocked at initial validation. DDD, Sense and Engineering have live older listings. | Reuse the same repository/folder submission. Read the candidate hash, findings and exact revision covered by a pending publish request before updating it. |
| [OpenAI / Codex](https://platform.openai.com/plugins) | Twelve existing uploaded drafts; the observed remaining intake gate is skills-only submissions. | Upload a complete corrected ZIP to the same draft and read its checks. Source commits do not update uploaded ZIPs. Never duplicate an existing draft or sent support report. |
| [skills.sh](https://www.skills.sh/sigmastudioz/agent-skills) | All twelve canonical pages have been observed, including Slipstream and Follow-Through after the November28 refresh. | Read canonical pages first; use one official isolated-project refresh only for a demonstrated gap. Page content does not establish full distributed-file equality. |
| [AgenticSkills](https://agenticskills.io/skills/visualizer) | Visualizer accepted. Tony, Returncraft, Delegating, Senior, Video, Slipstream and Follow-Through have sent-once intakes awaiting selective review. DDD, UI, Engineering and Sense retain earlier declines. | Preserve each prior intake and decision. The provider says accepted Visualizer follows the repository and needs no routine version email. A declined entry needs new review evidence; GitHub updates alone are not acceptance. |
| [Cursor](https://cursor.com/marketplace/publish) | One received publisher application for namespace `sigmastudioz` and this collection; native public listing is unverified. November28 on-site publisher search found no result. | Preserve the existing application. A reappearing form does not mean the application was lost. Do not confuse private/team installation with public approval. |
| [Google Antigravity](https://antigravity.google/docs/build-plugins/) | Earlier interest submissions preserved; twelve native manifests now validate. Public partner acceptance remains unverified. | The official partner route is the [same existing intake](https://forms.gle/2EX5RFYPoJe1UgxR9). Validate complete packages, follow any existing provider case, and avoid duplicate interest forms. |

## Stable identities and overlap

Returncraft retains `app-retention`. Claude alone uses `sigmastudioz-slipstream` for the new
Slipstream package because an existing connector owns the bare name; the skill, source folder
and other hosts remain `slipstream`. Tony is separate from DDD, not nested under it.
See the [README skill table](README.md#available-plugins) and catalog for the exact approved set.
Other local additions remain held back unless the publisher explicitly adds them to the scope.

DDD owns implementation structure, reuse and connected-path checks. Tony owns mechanism invention;
Engineering Spikes owns bounded uncertainty tests; Delegating owns agent handoffs. Those four can
collaborate without becoming one skill. Sense reviews whether a build reaches the intended outcome.
Visualizer creates visual explanations/films; UI Foundation supplies reusable effect/runtime code;
Video Analysis examines supplied footage. Returncraft owns product retention/ranking. Senior Digital
Skills owns older-adult teaching. Slipstream reduces context overhead; Follow-Through keeps tasks visible.

## Continuity before any update or monitor

- Read this map, the current catalog and the publisher's latest private handoff/receipt tracker.
  Exact submission IDs, case links, revision hashes, sent-once actions and observation times belong
  in that private tracker. Do not publish private correspondence, account details or local paths.
- Distinguish source published, ZIP uploaded, scan passed, review requested and publicly live.
  Read each claimed state from the service that owns it. Preserve prior times and evidence.
- Keep full functionality and existing native identities. Anthropic's Verified-organization gate
  is not fixed by disguising or silently removing scripts or the offline UI archive. Domain proof
  and a Verified request were completed November28; the human decision remains pending.
- Prepare accurate new-submission disclosures. Obtain action-time approval for publisher agreements
  or new sensitive access; never tick an inaccurate code-execution or data-handling declaration.
- Reconcile every meaningful result into the existing receipt once. Do not repeat a completed send,
  application, scan request or release simply because another task or recurring monitor runs.

## Native package checks

`tools/build_catalogs.py` generates three catalogs, twelve Antigravity manifests and full plugin
hashes. It checks identity/version consistency, terms links, contained icons, starter prompts and
Antigravity's actual24,000-byte skill-body limit. Keep complete conditional guidance in linked
references and retain real local tools. Claude privacy/terms/support links point to the existing
shared privacy policy, MIT usage terms and issue tracker.

Follow [CONTRIBUTING.md](CONTRIBUTING.md) for checks. Successful packaging or loader validation is
not native reviewer approval, automatic skill activation or evidence that all hosted snapshots match.

---

# Historical publication records

# Remaining Claude review items — November 13

Preserve full runtime packages, existing native identities and the UI runtime archive.
The current four blocked submissions require Anthropic Verified-organization eligibility
for bundled code. Do not disguise code or remove working features to claim clearance.

Tony2.1.1 moves its maintainer evaluation suite outside the installable plugin to
`tools/tony-evaluation/evaluation/`. Its real comparison scripts and example implementations
remain included byte-identically. Existing test consumers and provenance paths are adapted;
fixture bytes and historical result identities are preserved. Publish only this patch;
all eight other plugin inventories, including concurrent Visualizer1.4.7, are retained.
The fixture-inspection finding may clear only after a new native scan. The code-type gate
remains a distinct external blocker. No account, declaration, webhook or Publish change.

---

# Publication plan

## OpenAI upload metadata — November 28

Every plugin's root `plugin.json` must include
`extensions.com.openai.interface.termsOfServiceURL`. Keep the same URL in
`.codex-plugin/plugin.json` under `interface.termsOfServiceURL` for consumers of that fallback.
The current MIT-licensed collection uses its existing published usage terms:
`https://github.com/sigmastudioz/agent-skills/blob/main/LICENSE`.
This adds a listing link; it does not replace licenses or third-party notices with new terms.
If a future plugin has different terms, use its actual public terms page.

The catalog/release builder rejects missing, non-HTTPS or mismatched terms links before writing
outputs. Run `python3 tools/build_catalogs.py --check` before preparing upload ZIPs; package the
complete plugin folder, including both manifests. Terms-link validation is separate from OpenAI's
skills-only intake restriction and does not establish marketplace approval. Existing uploaded
drafts need their own corrected ZIP reupload; repository changes do not update them automatically.

## OpenAI listing readiness — November 28

Public-submission limits can be stricter than draft uploads: display names and subtitles are
limited to 30 characters, long descriptions to 4000, and publisher names to 80. The catalog
builder enforces these limits in both OpenAI and Codex listing interfaces and rejects core
listing-text/category drift between them. Use neutral listing language; keep necessary technical
compatibility details and platform-specific instructions inside the skill rather than using
other AI product names as listing copy. See the [official field reference](https://developers.openai.com/plugins/deploy/submission#listing-metadata).

All twelve already-public plugins were checked for these fields, the four HTTPS destinations,
contained square icon files and starter-prompt limits. Nine subtitles were shortened. DDD,
Delegating to Agents, Slipstream and Follow-Through listing copy no longer names other AI
platforms; Engineering Spikes' listing uses a neutral knowledge-base description. Returncraft's
Codex fallback now describes retention rather than the unrelated outcome-review skill, and
Delegating's fallback reflects its current versioned handoff contract. Full skill functionality,
identities, versions, licenses and historical evidence remain unchanged. Local checks establish
metadata readiness, not provider approval or an exception to the skills-only intake restriction.

## DDD guidance-only package — November 13

DDD1.4.6 contains the full baseline and local references, with no executable guard or tests.
The optional guard remains byte-identical in tools/handoff-guard and is installed separately
only when the host owner requests it. No automatic fetch, installer or hook ships in the
plugin. Preserve the current nine public identities, all eight other plugin inventories
(including concurrent Visualizer1.4.6 from8d2beee), existing installed/global guards and historical releases.
This fixes the submitted package's file-type boundary; only a remote scan/reviewer can
establish directory clearance or activation. Use the existing DDD submission identity.

---

## Credential-boundary patch — November 13

Update only Visualizer to 1.4.4 and UI Foundation Reuse to 1.2.3 on the nine-plugin
public base b661947. Keep all seven other inventories and all held-back additions unchanged.
Visualizer's three local tool entrypoints share an environment constructed without caller
values; sound no longer reads its former OS/temp/locale allowlist. Both Claude manifests
explicitly declare an empty MCP server map. UI's runtime archive/source/API are unchanged.
The provider's manifest warnings did not correspond to an actual declared MCP credential;
new source and local validation do not prove their removal by the directory scanner.
Preserve functional scripts, local runtime archive and cross-host manifests. No new native
identity, legal declaration, account verification, auto-publish or webhook change is involved.

---

Publisher: **Lex from SigmaStudioz**. Catalog: `sigmastudioz`. Plugins: `domain-driven-design`, `visualizer`, `video-analysis`, `engineering-spikes`, `ui-foundation-reuse`, `does-it-make-sense`, `what-if-tony-stark-built-this`.
Publisher profile: https://github.com/sigmastudioz.
Public repository: https://github.com/sigmastudioz/agent-skills.
MIT was selected by the publisher on 2026-10-18; root and plugin LICENSE files carry the notice
Copyright (c) 2026 Lex from SigmaStudioz.

## Repository release

The collection contains seven independently versioned plugins. The latest release scope is recorded below;
older sections preserve historical publication context. Regenerate catalogs with `python3 tools/build_catalogs.py`, verify with `--check`,
and run `python3 -m unittest discover -s tests` before publishing changes. Install the pre-push
hook once per clone (`ln -s ../../tools/hooks/pre-push .git/hooks/pre-push`): it refuses a push
while a generated catalog is stale or regenerated but not committed. Include each plugin's
license in its own folder so cached distributions preserve the notice.

Only the clean distribution is published. Private session logs, global settings, authentication
material, backups and publisher machine paths are excluded. Fresh Claude Code with the optional guard now passes 16/16 feature checks and 2/2 original
regressions using one teammate. Earlier failures and the earlier Cursor baseline remain recorded.
Do not promote universal adherence or untested desktop/cloud/performance results from these observations.

Repository availability lets people install directly. A listing in a platform's official public
directory is a separate application/review process; uploading files to GitHub does not create one.

| Platform | Distribution / public listing |
| --- | --- |
| Claude Code | Users register the public repository as a marketplace. For broader directory discovery, submit through Anthropic's developer portal; official-marketplace listing is a different partner route. |
| Cursor | Submit the Git repository at cursor.com/marketplace/publish; Cursor reviews public listings. Team marketplace import is a separate team feature. |
| ChatGPT / Codex | Submit the plugin ZIP through the OpenAI plugin portal, resolve automated findings, submit for review, and publish after approval. Select the verified developer identity that should appear publicly. |

Each plugin has an original icon and visible Lex from SigmaStudioz attribution. New Visualizer
and Video Analysis1.0.0 applications need their own review records; do not reuse the DDD submission
ID, imply approval, or accept new publisher agreements without action-time approval. Preserve the
existing DDD review/support correspondence; no duplicate applications or messages.

Engineering Spikes1.0.0 is a separate instruction skill for timeboxed investigation and paired
Confluence-oriented documents. Its repository release is separate from official marketplace review.
No Confluence account, terms acceptance or external publication is implied by installation.

## Visualizer 1.10.0 and Video Analysis 1.1.0 — November 20

Visualizer 1.10.0 adds music-teaser and collage motion (hit/gap motif gate, collage and lyric-UI
cadence, persistent title or rig-over-final stack, mixed-media collage, wordmark to type-only)
from a 50-post public creator study; it also carries the unreleased 1.5.0 to 1.9.0 changes, which
had no GitHub release of their own. Video Analysis 1.1.0 adds region/band cut scoring. Held local
plugins are outside this release's files, catalogs and history. Publish one complete plugin ZIP
per version (`git archive` of the plugin folder, which applies the export-ignore rules) on tags
`visualizer-v1.10.0` and `video-analysis-v1.1.0`; preserve earlier tags and assets. GitHub
availability does not establish native directory review or a refreshed index snapshot.

## Visualizer 1.11.0 and Delegating to Agents 1.1.0 — November 25

Visualizer 1.11.0 adds round-21 references (art direction, data, montage and compositing, motion
vocabulary, shaders, sound design with a local open-licence narration voice). Delegating to Agents
1.1.0 adds checking work with a second agent. Held local plugins are outside this release's files,
catalogs and history. Publish one complete plugin ZIP per version (`git archive` of the plugin
folder) on tags `visualizer-v1.11.0` and `delegating-to-agents-v1.1.0`; preserve earlier tags and
assets. GitHub availability does not establish native directory review or a refreshed index snapshot.

## License comparison — checked 2026-10-17

**Recommendation: MIT** for this instruction/script skill when the goal is straightforward reuse
and adoption. Both choices allow commercial reuse. MIT requires the copyright/license notice to
remain with copies or substantial portions. It does not require a visible app UI credit or prevent
someone from selling a derivative. Keep the author prominently in manifests, byline and README too.

Apache 2.0 adds an explicit contributor patent license, notices for changed files, and retention of
relevant source attribution / NOTICE content. It is a reasonable alternative if those terms are a
priority. Neither license forces derivative source code to be published. Do not add a custom
mandatory UI-credit clause and continue calling the result unmodified MIT.

| Primary source checked | Observed license |
| --- | --- |
| [Vercel agent-skills README](https://github.com/vercel-labs/agent-skills#license) | MIT |
| [Superpowers LICENSE](https://github.com/obra/superpowers/blob/main/LICENSE) | MIT |
| [OpenAI skill-creator LICENSE.txt](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/LICENSE.txt) | Apache-2.0 for that specific skill |
| [Anthropic skill-creator LICENSE.txt](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/LICENSE.txt) | Apache-2.0 for that specific skill |

These are examples, not a claim that every skill in either catalog uses the same license.
The publisher selected MIT. The comparison above explains that decision; it does not change the
terms of the unmodified MIT license text included with this collection and its initial plugin.

Primary references: [MIT text](https://opensource.org/license/mit),
[Apache 2.0 text](https://www.apache.org/licenses/LICENSE-2.0),
[Claude distribution](https://code.claude.com/docs/en/plugins/publish),
[Cursor publishing](https://cursor.com/docs/plugins),
[OpenAI submission and publisher identity](https://developers.openai.com/plugins/deploy/submission).

## UI Foundation Reuse and Visualizer update

UI Foundation Reuse1.0.0 includes runtime0.5.0 plus its original TypeScript source,
compiled modules, type declarations and notices. Bundled head/brain geometry retains
CC BY attribution; the implementation's MIT license does not replace those notices.
Visualizer1.2.0 preserves its stable plugin/skill identity and demo assets, adding the
latest local video workflow, renderer and optional reuse-companion routing.
Update its existing draft and existing directory identities; do not create a second
Visualizer or rename it to visualization-videos. UI Foundation Reuse is a distinct
new plugin; check for an existing entry before creating any native submission.
No new legal declarations are accepted by repository publication.

## Local skill sync and outcome-review addition

UI Foundation Reuse1.1.0 packages maintained runtime 0.7.0 and matching effect/scene/native
guidance. Visualizer1.2.1 adds reviewed-feedback learning guidance while retaining its
existing identity, renderer, interactive routes and historical demos. Does It Make Sense?1.0.0
is a separate instruction-only outcome-review plugin, registered once in the collection.
No new native submission, legal acceptance or provider approval is performed by this sync.
Use existing provider identities for updates; the new plugin has no native review receipt.

## Maintained skill sync — November 1

Publish independently versioned DDD 1.4.0, Visualizer 1.3.1, UI Foundation Reuse 1.1.1 and
Does It Make Sense? 1.0.1 from one reviewed collection revision. Keep Engineering Spikes and
Video Analysis unchanged. This sync adds no new catalog entries or marketplace submissions.
Only reusable synthetic fixtures and summarized test cases are public; raw host sessions,
personal paths/configuration and the original host-specific generator remain private.
Existing native publication requests are not repeated. GitHub release availability does not
establish native review approval or a refreshed skills.sh backing snapshot.


## Maintained skill sync — November 11

Update only the six previously published identities: DDD 1.4.1, Visualizer 1.4.0,
Video Analysis 1.0.1, UI Foundation Reuse 1.2.0 and Does It Make Sense? 1.0.2;
Engineering Spikes stays 1.0.0 with its existing inventory unchanged. UI Foundation Reuse
bundles runtime 0.11.0, source, declarations and license notices. Visualizer includes the
reference-to-timed-spec workflow, motion vocabulary, optional renderer guidance and the
media-in-3D adapter. New plugin additions are outside this release.

Use the existing directory identities and supported update paths. Publication on GitHub
does not prove provider review approval, native activation or a current index snapshot.
Retain prior sent-once requests and actual observation times. AgenticSkills' accepted
Visualizer listing follows the repository; its provider requested no version-update emails.

## Tony Stark and maintained-skill release — November 12

The authorized collection contains exactly seven identities: the six previously published
plugins plus What If Tony Stark Built This 2.0.0. DDD 1.4.4 adds multi-stage batch handoff
and review-evidence guidance. Visualizer 1.4.3 combines the looping-asset and mechanism-rate
guidance with isolated sound-tool environments and anonymous audio-decoding boundaries.
UI Foundation Reuse 1.2.1 preserves its public critique-loop guidance and runtime 0.11.0.
Video Analysis 1.0.1, Does It Make Sense? 1.0.2 and Engineering Spikes 1.0.0 are retained.
Other local additions are excluded from this release's files, catalogs and commit history.

Publish complete plugin ZIPs for the new or unreleased versions. Preserve earlier tags and
release assets. GitHub availability establishes neither a fresh skills.sh snapshot nor
native marketplace approval. Tony Stark has no native directory submission identity in
this task; no new legal declarations, account changes or support messages are implied.

## Slipstream addition — November 27

Slipstream 1.0.0 is a new, separately versioned plugin: local token-usage measurement, a
usage-based skill listing with an installed-skills catalog and prompt-time hints, a context meter,
a polling guard and a Cursor usage-CSV parser. Configuration changes are dry-run by default, and
its hook scripts are registered only by `lean_setup.py --apply` (not declared as plugin lifecycle
hooks). Published evidence is ratios and methods only; raw logs and personal evidence stay local.
It has no native review receipt. A Cursor publisher application for this repository and an OpenAI
ZIP submission were prepared from the merged main ZIP; their outcomes are recorded only once observed.
The Claude directory route needs the Verified-organization allowance noted above for bundled code.

## Prerequisite pattern — November 27

Collection rule: plugins ship their own tools, never a runtime, dependency tree or binary, and
check prerequisites with the user first. Visualizer 1.11.1, Video Analysis 1.1.1, UI Foundation
Reuse 1.6.1, What If Tony Stark Built This 2.1.2 and Delegating to Agents 1.1.1 gain a "Before
first use" section: check what is installed, explain what is missing and which features need it,
install only with the user's yes (Python packages into a project virtual environment), and state
what still works if they decline. `tests/test_prerequisites.py` enforces this for every plugin that
ships code or calls an outside tool and rejects bundled runtimes. This is a reliability and
transparency rule; it does not change the Claude directory's code-type review gate.

## Tony 2.2.0 — learned from real use, November 27

What If Tony Stark Built This 2.2.0 adds a verdict-first review mode. A local review of human-driven
skill use across Claude Code, Codex and Cursor found that most Tony requests ask for a review
("take a look", "what are we missing", an opinion on a link) rather than an invention, and that
several follow-ups were needed to get a plain verdict. The new section answers in order: verdict
(built correctly, makes sense, working and how verified, fits surrounding pipelines), ranked gaps
with evidence, what to change, and what remains. Session content stayed local; only the general
pattern is published. Other plugins had too little skill-specific evidence to change.

## Slipstream 1.1.0 — November 27

Long sessions now get a concrete way out, chosen by the app the session runs in. Past ~100K of
growth, at the next task boundary, the agent writes the handoff and, in the Claude desktop app,
offers a one-click fresh-session card carrying it; in the terminal it gives the `/clear` step.
Nothing starts without the user. Fixed: after a compaction the meter stayed silent until the session passed its old peak; it
now nudges again once the context regrows. New `scripts/handoff_report.py` measures follow-through. Baseline
on the 1.0.x nudge (one day, 10 nudged sessions): 7 wrote a handoff and 4 offered a session, yet
they kept going for 1,142 calls re-sending 457M tokens. Tests cover each app route and the report.

## Slipstream 1.0.2 — November 27

The skill hint also ignores other sessions' hand-backs ("Another Claude session sent a message",
`<agent-message>` blocks) and carried-over summaries, for every match rule. Observed live in the
first hours after install: 20 of 23 hints were one unrelated skill, triggered by subagent
hand-backs and continuation summaries. Replaying those 22 real prompts through 1.0.2 leaves 3
hints, all on words the user typed. Regression test added; verified to fail on 1.0.1.

## Slipstream 1.0.1 — November 27

The prompt-time skill hint ignores app-generated notices (session events, system reminders, task and
CI notifications) and matches only what the user typed. Observed live: a session notice containing
"rollout" triggered an unrelated skill hint twice. Regression test added; verified to fail on 1.0.0.
