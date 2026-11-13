# Tony Stark maintainer evaluations

The evaluation harnesses, frozen synthetic fixtures, protocols and historical results
live in [evaluation/](evaluation/PROTOCOL.md), outside every installable plugin.
Their relocation removes development-only workloads from the marketplace package.
It does not change the skill's comparison runner, examples or engineering guidance.

The harnesses resolve the current runtime from
`plugins/what-if-tony-stark-built-this/skills/what-if-tony-stark-built-this/`.
Run collection regressions from the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_stark*.py'
```

These checks prepare isolated synthetic workspaces and test local contracts; they
do not dispatch models. Live trials require their own explicit authorization and
the relevant frozen protocol. Historical dates, input hashes and results remain
historical; relocating files is not a new efficacy result.

Recovery: move `evaluation/` back to the plugin's former evaluation directory and
revert the runtime-source adapter, test-loader paths and documentation links together.
Preserve newer edits before restoring. Earlier release assets remain available.
