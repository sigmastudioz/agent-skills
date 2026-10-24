# Publication plan

Publisher: **Lex from SigmaStudioz**. Catalog: `sigmastudioz`. Plugins: `domain-driven-design`, `visualizer`, `video-analysis`, `engineering-spikes`.
Publisher profile: https://github.com/sigmastudioz.
Public repository: https://github.com/sigmastudioz/agent-skills.
MIT was selected by the publisher on 2026-10-18; root and plugin LICENSE files carry the notice
Copyright (c) 2026 Lex from SigmaStudioz.

## Repository release

The collection contains the Principal Driven Domain Design 1.3.0 release (`domain-driven-design`) and supports independently versioned
future plugins. Regenerate catalogs with `python3 tools/build_catalogs.py`, verify with `--check`,
and run `python3 -m unittest discover -s tests` before publishing changes. Include each plugin's
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
