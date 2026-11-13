#!/usr/bin/env python3
"""Matched comparison-runner utility trial, using the existing isolated dispatch engine."""
from pathlib import Path
import argparse
import importlib.util

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('stark_runner_dispatch',HERE/'run_tools.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
RUNTIME=engine.shared.PLUGIN_ROOT/'skills/what-if-tony-stark-built-this'
TICKETS={
    'lookup':'Make a measured implementation recommendation for the supplied lookup API, following the README measurement contract. Preserve all supplied inputs/code. Deliver decision.json and executed measurement evidence.',
    'codec':'Make a measured implementation recommendation for the bounded-memory decoder, following the README measurement contract. Preserve all supplied inputs/code. Deliver decision.json and executed measurement evidence.',
}
COMMON='''Work only in this isolated synthetic repository. Read AGENTS.md and README.md. Compare the
supplied variants using the supplied cases and limits, and produce the requested decision/evidence.
Do not change or remove any supplied code, README, experiment, common instructions or supplied tools.
Own only new measurement scripts, new reports and an optional short note. Preserve other writers by
staying in your own checkout. Python standard-library tools and read-only Git are available.
No global skills/plugins, external task inputs, network, installs, additional dependencies, extra
agents, account/spending changes, commits, publication or deployment. Own generated temporary data
and this run's own tool-output files are permitted. No background jobs or broad process kills; only
clean up known owned child processes. Stop within 1200 seconds. Emit brief MILESTONE compare/verify
updates and a final stdout summary of paths, actual commands/results and remaining proof, ending DONE.
Source inspection or a proposed experiment alone is insufficient: execute the comparison.
'''


def profile():
    assets=[dict(source=path,target='.stark-tools/'+str(path.relative_to(RUNTIME/'scripts'))) for path in sorted((RUNTIME/'scripts').rglob('*.py')) if '__pycache__' not in path.parts]
    return dict(name='comparison-runner-utility-v1',model_count=1,maximum_active=2,tickets=TICKETS,
                fixtures=HERE/'runner-fixtures',guides=[RUNTIME/'references/comparison-runner.md'],assets=assets,
                checker=HERE/'runner_trial_checks.py',protocol=HERE/'RUNNER_PROTOCOL.md',common=COMMON,
                guidance_file='.stark-comparison-guidance.md',
                asset_instruction='Use the provided local copy at .stark-tools/compare_designs.py; the reference installation path is different from this isolated fixture.',
                owns='Only new measurement scripts/reports/decision.json and optional note; supplied source, cases, README, instructions and tools are readonly',
                checks='Execute README comparison contract, preserve all supplied inputs, write decision.json and machine-readable evidence, verify actual outputs and report source identities',
                state='Fresh committed comparison task with alternative source/cases; no previous model outputs, expected recommendation, coordinator calibration or hidden grading supplied.')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--model',default='grok-4.7-high');parser.add_argument('--workers',type=int,default=2);args=parser.parse_args()
    if args.action=='prepare':engine.prepare(args.output.resolve(),[args.model],profile())
    else:engine.run(args.output.resolve(),args.workers)


if __name__=='__main__':main()
