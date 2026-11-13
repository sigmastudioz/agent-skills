#!/usr/bin/env python3
"""Fresh maintained-code tasks; all implementation and comparison setup is timed."""
from pathlib import Path
import argparse
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('stark_coding_dispatch', HERE / 'run_tools.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
RUNTIME = HERE.parent / 'skills/what-if-tony-stark-built-this'
TICKETS = {
    'catalog': 'Implement the release catalog scaling ticket in README.md, create your own comparison inputs and adapters, execute the before/after comparison and verify the connected consumers.',
    'sequencing': 'Implement the exact album sequencing scaling ticket in README.md, create your own comparison inputs and adapters, execute the before/after comparison and verify both public entrypoints.',
}
COMMON = '''Work only in this isolated copy of maintained code. Read AGENTS.md and README.md.
Implement the coding ticket and design, set up and execute its comparison from scratch.
The entire 1800-second session budget includes reading, task inspection, workload/adapter/manifest
setup, coding, debugging, all benchmark attempts and verification. No prepared comparison is supplied.
Own only the code directories authorized in README, new tests and new experiment/data/report files.
Supplied tests, reference, README, SOURCE, engineering instructions and skill tools are readonly.
Python standard-library tools and read-only Git are available; use bounded foreground commands.
No outside task inputs/global skills/plugins, network, installs, extra dependencies, extra agents,
background jobs, broad process kills, commits, publication, deployment or account/spending changes.
Own generated scratch data and this session's generated tool output are permitted. Clean up only
your known owned files/processes. You are not alone: independent workers and the coordinator are
active; preserve others' work by staying in this checkout. No AI attribution in code comments.
Give brief MILESTONE inspect/implement/setup/compare/verify updates and finish with a concise stdout
report of changed paths, contracts, actual checks, remaining gaps, then DONE. Do the coding and
execute the comparison; a proposal or a claimed speedup without evidence is insufficient.
'''


def profile():
    files = [RUNTIME / 'SKILL.md', *sorted((RUNTIME / 'references').glob('*.md')),
             *sorted((RUNTIME / 'scripts').glob('*.py'))]
    assets = [dict(source=p, target='.stark-skill/' + str(p.relative_to(RUNTIME))) for p in files]
    return dict(name='maintained-coding-total-time-v1', model_count=1, maximum_active=1,
                timeout_seconds=1800, tickets=TICKETS, fixtures=HERE / 'coding-fixtures',
                guides=[RUNTIME / 'SKILL.md'], assets=assets,
                checker=HERE / 'coding_trial_checks.py', protocol=HERE / 'CODING_PROTOCOL.md',
                common=COMMON, guidance_file='.stark-coding-guidance.md',
                asset_instruction='The maintained runtime is available at .stark-skill/SKILL.md with working relative references and scripts. Read only needed runtime resources there; do not follow the maintainer evaluation pointer. No task-specific manifest, adapter, case or expected output is provided.',
                owns='Only README-authorized active code directories, new regression tests, experiment generators/adapters/data/reports and decision.json; all supplied tests/reference/README/SOURCE/instructions/tools are readonly',
                checks='Run supplied tests, add relevant regressions, satisfy README coding/resource contracts and execute before/after measurement with your own setup and provenance; report actual evidence and limits',
                state='Fresh committed copy of maintained production code and unchanged reference. Original public checks pass; requested optimization not implemented. No candidate, benchmark setup, workload data, expected output, hidden checker, prior output or coordinator calibration supplied.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--model', default='grok-4.7-high')
    args = parser.parse_args()
    if args.action == 'prepare':
        engine.prepare(args.output.resolve(), [args.model], profile())
    else:
        engine.run(args.output.resolve(), 1)


if __name__ == '__main__':
    main()
