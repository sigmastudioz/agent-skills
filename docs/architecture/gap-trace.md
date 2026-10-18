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
