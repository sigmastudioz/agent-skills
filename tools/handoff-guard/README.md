# Optional DDD handoff guard

By Lex from SigmaStudioz. MIT, under the repository [LICENSE](../../LICENSE).

This local Python tool is distributed separately from the guidance-only
[DDD marketplace plugin](../../plugins/domain-driven-design/README.md). It checks the
same handoff fields, workspace/baseline identity, explicit agent budget and isolation
declarations as before. The implementation is unchanged by the packaging split.

## Explicit opt-in setup

Use a reviewed checkout of this repository. After the user requests the optional guard,
install the complete DDD skill on that execution host, then copy `guard_handoff.py` from
this directory into that skill's `scripts/` directory. The resulting layout must be:

```text
domain-driven-design/
  SKILL.md
  references/
  scripts/
    guard_handoff.py
```

Inspect and preserve an existing destination before copying; compare and back it up before
an explicitly requested replacement. Existing installations at this layout need no changes.
Do not run this source file directly from `tools/handoff-guard/`: it intentionally trusts only
the `SKILL.md` beside its installed `scripts/` directory, not an arbitrary handoff baseline.
The [host setup guide](../../SETUP.md#optional-claude-handoff-guard) documents the hook matcher
and canonical path. Merge settings deliberately; installing the marketplace skill alone
does not enable hooks or authorize an installer, download or external action.

## Verification and rollback

```sh
python3 -B tools/handoff-guard/test_guard_handoff.py
```

Tests copy the current guidance and this exact guard into temporary installed layouts,
then exercise real hook subprocesses. They do not edit global installations or launch agents.
The collection test entrypoint runs the same regressions.

Rollback of the repository split is the inverse source move from this directory back to
`plugins/domain-driven-design/skills/domain-driven-design/scripts/`, along with the linked
setup/test-loader references. Preserve newer edits before any rollback. Historical public
releases retain their original complete inventories and guard bytes. No installed copy is
removed or rewritten by this split or by rolling back the repository.
