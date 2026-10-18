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
| Repository publication | GitHub creation form -> public repository | Selected organization, name, visibility and license -> remote creation/upload | Publisher approved MIT; public repository created; root/plugin licenses match | COLL-05 publication verification recorded in repository publication receipt |
| Initial DDD skill | Installed/native agent -> module changes | Global baseline, optional Claude hook, handoffs and checks | Cursor fresh coding 16/16 + 2/2; completed Claude 15/16 + 2/2 with four teammates | gap-found: Claude tuple-collision and agent-count adherence remain open; preview disclosed |

Inventory: 8 review units, 8 accounted for. File/catalog checks and generated output are runtime
verified locally; user setup, official-store publication and every possible future plugin are not.
A maintainer adding a plugin must rerun catalog checks and verify that plugin's actual behavior.
Cycles are absent in the scoped flow: registry -> manifests -> catalogs/receipt; no reverse imports.

Closure check for COLL-05: confirm the license, create the public destination, publish only the clean
bundle, verify the repository files and native catalog source paths remotely, and record the result.
Do not upload private session logs, global settings, credential material or publisher workspace paths.

Catalog-tool content revision: 2504ae7b2e3175effa18a4f21c08a091cb81b2525e97ac4cf8bb06592b86dea0 . Reopen evidence after relevant changes.
