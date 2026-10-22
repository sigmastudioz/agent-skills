# Collection catalog trace

Scope: adding future independently versioned plugins to the SigmaStudioz collection. Reviewed
2026-10-18. This record covers catalog tooling, not universal skill efficacy or an official listing.

| Module/path | Entry/consumers | Dependencies/effects | Evidence | Finding/status |
| --- | --- | --- | --- | --- |
| catalog.json | Maintainer -> build_catalogs.render | Plugin names, contained paths, owner and display label | Actual registry plus two-plugin test | COLL-01 fixed-and-verified: one inventory serves three hosts |
| tools/build_catalogs.py | CLI -> build -> render | Registry and four manifests per plugin -> three host catalogs and per-plugin release hashes | Six tests; actual --check and native Claude catalog validation | COLL-02 fixed-and-verified: preserve independent versions; reject duplicate names, traversal and native drift |
| Three generated catalogs | Claude / Cursor / Codex discovery | Contained ./plugins paths -> native/portable package -> skills | Registry equality checks and source containment; native Claude validation | COLL-03 verified file/schema integration; live store installation is a separate boundary |
| release.json | Maintainer verification | Each plugin version plus hashes of its files | Two-plugin test verifies versions 1.0.0 and 2.3.4 coexist | COLL-04 fixed-and-verified: avoid a forced shared release version |
| tests/test_catalogs.py | Standard-library unittest | Temporary independent plugin fixtures; read-only stale check | 6 tests pass, including no output on duplicate rejection | verified |
| README / CONTRIBUTING / SETUP | New user / maintainer | Select plugins, add entries, opt into native global instructions | Source/path review; no placeholder skill folders created | static-only user instructions; each new plugin needs its own efficacy checks |
| Repository publication | GitHub creation form -> public repository | Selected organization, name, visibility and license -> remote creation/upload | Public snapshot 6451d807f6c7f77e36ecf105af0237d5acf125f2; 26 files match reviewed bundle; native catalog validation and 6 tests pass in fresh clone | COLL-05 fixed-and-verified: MIT root/plugin notices, clean direct-install collection published; see ../publication.json |
| Initial DDD skill | Installed/native agent -> module changes | Global baseline, optional Claude hook, handoffs and checks | Cursor fresh coding 16/16 + 2/2; fresh Claude 1.0.5: 16/16 + 2/2 with one teammate; 21 guard tests | fixed-and-verified for the scoped native test; desktop/cloud/performance remain outside coverage |

Inventory: 8 review units, 8 accounted for. File/catalog checks and generated output are runtime
verified locally; user setup, official-store publication and every possible future plugin are not.
A maintainer adding a plugin must rerun catalog checks and verify that plugin's actual behavior.
Cycles are absent in the scoped flow: registry -> manifests -> catalogs/receipt; no reverse imports.

COLL-05 closure completed on 2026-10-18: MIT confirmed; public destination created; the clean
bundle and all native catalog source paths verified in a fresh public clone. The 26-file verified
snapshot is recorded in [the publication receipt](../publication.json); this receipt and trace
closure are later documentation additions. No private session logs, global settings, credentials
or publisher machine paths were uploaded. Official store submissions remain a separate boundary.

Catalog-tool content revision: 2504ae7b2e3175effa18a4f21c08a091cb81b2525e97ac4cf8bb06592b86dea0 . Reopen evidence after relevant changes.

## 1.0.5 repair trace

| Module/path | Entry and effects | Evidence | Status |
| --- | --- | --- | --- |
| SKILL.md | Global routing -> original contract -> proposed brief -> worker and parent review | Core SHA in ../validation.json; full-body native child delivery before HANDOFF_JSON | fixed-and-verified: explicit injective identity and user budget precedence |
| guard_handoff.py | Native PreToolUse -> non-meta user budget -> pending/non-rejected dispatches -> handoff validation -> updated input | 21 subprocess tests; one real accepted teammate, one rejected incomplete attempt | fixed-and-verified; English explicit Use N syntax and available transcript boundary documented |
| Native consumer | Isolated worker -> parent copy/integration -> API/worker billing facade -> store/read/retry/error outcomes | 20 parent tests; 16 external feature checks; 2 original regressions | fixed-and-verified in the dependency-free fixture |
| Installed package docs | Plugin cache README -> hosted setup/privacy/validation links | Absolute repository links replace paths outside a cached plugin folder | fixed-and-verified static link/path inspection; publisher portal scans remain separate |

These additions close the observed identity-collision and excess-teammate findings for this native
run. Budget wording that cannot be recognized and unavailable native history remain coordinator
responsibilities. No transcript data is sent to a publisher service by the helper.

## 1.0.6 branding trace

The human requested Principal Driven Domain Design as the public name. Keep the package and
skill ID `domain-driven-design` for compatibility. Trace: reviewed title/UI metadata -> builder ->
portable/native manifests -> generated catalogs/release hashes -> installed aliases and local
plugin -> repository docs and directory scan. Instruction body after the H1 and optional helper
are unchanged from the tested 1.0.5 baseline. Preserve original native evidence and hashes.
Verify the 597-line folder limit, full baseline delivery before handoff, native manifest validation,
catalog drift and every published file. Directory approval and platform-derived labels remain
external; do not claim that a metadata update establishes a live listing.

## 1.1.0 user-installed instruction update

The instruction body now adds cross-module edge checks, staged-snapshot and concurrent-writer
review, candidate disproof, and early orientation versus final acceptance gates.

| Cluster | Edges checked | Evidence and limits |
| --- | --- | --- |
| Instruction delivery | Consumer, contract, registration | Stable skill ID and path; updated SKILL.md exactly matches user-installed source; full-body guard delivery unchanged; existing 21 guard tests pass |
| Distribution | Contract, back-compat, snapshot | Four manifests agree on 1.1.0; registry and three catalogs retain stable IDs; release inventory and ZIP byte hashes match; other plugins unchanged |
| Documentation | Contract, headroom | README reports 567 instruction lines / 666 skill-folder lines; earlier 597-line and native efficacy receipts remain historical, not relabeled |

No new production module, periodic task, UI component, discriminator, storage writer or persisted
key was introduced, so cadence, mount and data-migration edges have no changed runtime path.
The helper and UI metadata remain byte-identical. No fresh native-agent efficacy run was made
for 1.1.0; packaging checks do not establish instruction adherence. Reviewer activation and
blocked uploader eligibility remain external boundaries, not confirmed publication.

## Engineering Spikes 1.0.0 addition

Scope: one new, independent instruction/template plugin; no production runtime helper or global
configuration change. The 13 design gaps and scenario boundaries are recorded in
[Engineering Spikes validation](../engineering-spikes-validation.md).

| Cluster | Forward / backward edges | Candidate findings and closure |
| --- | --- | --- |
| Instruction consumption | Relevant spike request -> modes -> evidence/decision -> two audience templates -> delivery reference | SP-01–12 covered; negative/blocked outcomes and recommendation versus approval explicit |
| Format delivery | Templates -> HTML artifacts -> rendered copy -> target editor | Six-column identity table replaced; Mermaid native-rendering assumption rejected; actual Confluence paste remains unverified |
| Distribution | catalog.json -> portable/native manifests -> three host catalogs -> skill/resources -> release hashes -> ZIP | SP-13; stable independent ID/version and contained paths; exact inventory checked at release preparation |
| Discovery and documentation | README install ID -> registry name -> plugin skill path -> UI metadata | No alwaysApply global rule, executable helper or forced activation; existing plugin versions/inventories preserved |

Four clusters inventoried and accounted for. No runtime storage writer, recurring process, API or
UI mount was introduced; cadence, migration and production rollback edges have no changed code.
Research access, actual agent adherence, editor paste and native directory activation remain
external/unverified boundaries. Authored scenarios and package checks do not close those claims.
