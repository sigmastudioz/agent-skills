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
