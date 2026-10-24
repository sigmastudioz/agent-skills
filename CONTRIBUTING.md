# Adding another skill or plugin

The repository is a collection. The current domain-driven-design plugin is the first entry, not a
limit on the number of skills. Installers select the plugins they need.

1. Decide ownership: use a separate plugin when the capability should be installed/versioned alone;
   group related skills only when they form a cohesive workflow. Avoid one oversized universal skill.
2. Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` with required skill metadata and only
   real supporting resources. Give the skill a precise description for natural task selection.
3. Add portable `plugin.json` and the three native compatibility manifests. Keep name, version and
   author consistent. Give this plugin its own semantic version and truthful documentation/status.
4. Add one entry to root `catalog.json`, using `./plugins/<plugin-name>` as the path. Catalog metadata
   comes from that plugin's manifest; the generator does not rewrite its version or implementation.
5. Generate and check all host catalogs, run the tests, and validate the actual skill behavior:

```sh
python3 tools/build_catalogs.py
python3 tools/build_catalogs.py --check
python3 -B tests/test_catalogs.py
claude plugin validate .
```

6. Document setup, runtime/permission requirements, affected consumers and platform limits. When a
   coding skill delegates work, include accessible context, ownership, checks and return evidence.
7. Review changes before release. A repository commit can change one plugin while others keep their
   existing versions. A root release tag is a collection snapshot, not a forced shared plugin version.

The initial DDD release targeted an under-600-line folder; later user-approved releases include
linked references and guard regressions. Report actual instruction and folder sizes for each release
and honor applicable host limits. Do not turn global instructions into project-specific task state. Avoid copying the same behavior across several skills; link or
share owned resources when their semantics really match.

Catalog generation traces registry -> plugin manifests -> three contained host sources -> skill
folders. The tests exercise adding a second plugin, preserving independent versions, read-only
staleness detection, duplicate identities, path traversal and native manifest drift. Validate every
new plugin's actual runtime behavior separately; passing catalog tests is not an efficacy result.

This collection and its first plugin use MIT. Include a LICENSE file in every plugin distribution
and preserve its copyright notice. Record any explicit per-plugin license exception clearly.
