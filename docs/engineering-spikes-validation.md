# Engineering Spikes: design and validation

Version 1.0.0, by Lex from SigmaStudioz. Reviewed 2026-10-22.

The starting rule required separate stakeholder and technical documents, conditional workflows
and Confluence-ready formatting. The human chose a full spike lifecycle. This expansion makes
the investigation and decision contract explicit while preserving those audience requirements.

## Gap trace against the starting standard

| ID | Missing or ambiguous detail | Resolution / owning resource | Closure evidence |
| --- | --- | --- | --- |
| SP-01 | When to activate; plan versus execute | SKILL scope and four operating modes | Document mode cannot silently launch experiments; ordinary feature work is excluded |
| SP-02 | What uncertainty the spike resolves | SKILL framing; technical decision frame | Question, scope, owner, constraints and observable disproof recorded before investigation |
| SP-03 | Timebox and stopping | SKILL stop and decide | Stop at criteria, resource bound or unchanged blocker; proposed budgets are not approvals |
| SP-04 | What constitutes a finding | SKILL evidence ledger; technical template | Provenance, method, observation and limits; synthetic/static proof remains bounded |
| SP-05 | Comparable alternatives | SKILL options; both templates | Real alternatives and viable baseline; no fabricated option quota or averaging away hard failures |
| SP-06 | Expected versus actual behavior | SKILL gap trace; technical template | Requirement -> option -> evidence -> consequence; check baseline before calling a gap a defect |
| SP-07 | Inconclusive or blocked outcome | SKILL closure; both templates | Four supported outcomes; lifecycle state and recommendation approval are separate |
| SP-08 | Audience separation and consistency | Two distinct templates; SKILL audience checks | Shared ID/status/date/companion; plain-language summary agrees with engineering evidence |
| SP-09 | Meaning of Confluence-ready | references/confluence.md | Rendered basic HTML copying; raw Markdown import and actual paste success are not assumed |
| SP-10 | Diagram portability | SKILL delivery; Confluence reference | Useful flows only; caption and text fallback; Mermaid source is not a rendered image |
| SP-11 | Adoption and ownership | SKILL handoff; technical template | Follow-ups have owner or unassigned, dependencies and acceptance; prototype is not production |
| SP-12 | Permissions and disclosure | SKILL modes/evidence; README | No inferred publication, spending or access rights; restricted material stays appropriately scoped |
| SP-13 | Independent distribution | Registry and four manifests | Stable engineering-spikes ID/version; three generated host catalogs and exact release inventory |

## Review scenarios

These are authored instruction walkthroughs, not independent model runs. They establish design
coverage and expose wording problems; they do not prove every agent will follow the instructions.

| Scenario | Required handling / inspected instruction |
| --- | --- |
| Plan only, access missing | Proposed checks stay proposed; record blocker and do independent planning; modes/framing |
| Preferred option misses its threshold | Preserve negative evidence, compare baseline and recommend rejection or further investigation; evidence/options/closure |
| Timebox ends with incomplete evidence | Stop, state unknowns, preserve partial work and specify a bounded next step; stop and decide |
| Simple source lookup | Still produce two concise audience documents; skip decorative workflows; framing/delivery |
| Retry flow has partial failure | Trace consumer/state/error edges; useful technical diagram needs a caption and textual fallback; gap trace/delivery |
| Stakeholder summary overstates prototype | Reconcile both documents; no production guarantee or invented approval; audience/verification |
| Existing implementation already meets requirement | Disprove gap against baseline and record why; do not fabricate a defect; gap trace |
| Private investigation | Permission depends on access classification, not technical versus stakeholder label; evidence |
| Source changes on resume | Reopen affected claims and retain provenance; resume/evidence |

Templates were narrowed to two-column identity tables after review found that six-column
metadata impaired copying/readability. Experiment details use per-experiment sections when wide.
All template guidance must be replaced before delivery; templates themselves are intentional guides.

## Verification boundaries

Repository checks cover manifest/catalog wiring, release file hashes, resource links and existing
regressions. A synthetic two-document example is used for local rendering review. The example is
explicitly fabricated test input, not evidence of a real product experiment. No fresh native-agent
efficacy run or actual Confluence paste test is claimed. Directory scans, approvals and installation
are separate external checks. No existing plugin instruction or version is changed by this addition.

Primary editor references, checked 2026-10-22:
[Markdown shortcuts](https://support.atlassian.com/confluence-cloud/docs/available-markdown-commands/),
[legacy markup limits](https://support.atlassian.com/confluence-cloud/docs/insert-confluence-wiki-markup/),
[tables](https://support.atlassian.com/confluence-cloud/docs/simplify-data-with-tables/).

## Local acceptance results

- Skill-creator quick validation passed; UI YAML parses and local resource links resolve.
- All 40 existing repository tests passed; generated catalogs and release hashes verify.
- Claude native plugin/catalog validation passed with the existing nonblocking icon and
  documentationUrl notes. Both official Cursor schemas cached from the earlier source validation
  passed against the new plugin and updated catalog.
- All three existing plugin versions and file-hash inventories match the main baseline exactly.
- Two synthetic HTML documents were visually reviewed locally, including evidence/gap tables
  and matching conclusions. Actual Confluence paste and fresh native-agent efficacy remain unverified.
- The standalone plugin ZIP contains all 13 plugin files, each byte-identical to the source.
