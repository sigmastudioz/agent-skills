#!/usr/bin/env python3
"""Prepare/run fresh engineering-invention cells using the owned tool trial engine."""
from pathlib import Path
import argparse
import importlib.util

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('stark_tools_engine',HERE/'run_tools.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
RUNTIME=engine.shared.PLUGIN_ROOT/'skills/what-if-tony-stark-built-this'
TICKETS={
    'windows':'Make Maintenance Window Planner exact and usable for long-lived recurring schedules at the README scale. Preserve the public planner/CLI and add relevant checks. Deliver a working implementation with evidence for the mechanism and its limits.',
    'pulse':'Make Pulse Telemetry Analyzer and its report CLI handle the README scale exactly without expanding the sample stream. Preserve public contracts and add relevant checks. Deliver a working implementation with evidence for the mechanism and its limits.',
}
COMMON='''Work only in this isolated synthetic repository. Read AGENTS.md and README.md, implement
the ticket and run appropriate local checks. Preserve public APIs and existing test expectations.
Own the package, added regression tests and an optional short local note. README contracts and
supplied guidance are read-only. Git inspection and standard-library local test commands are allowed.
No external inputs/global skills/plugins, network, installs, new dependencies, extra agents, commits,
publishing or deployment. Generated scratch data may use temporary directories; outside file reads
are allowed only for this run's own generated tool output, not additional instructions or task inputs.
No background jobs or broad process kills; use bounded commands and clean up only known owned PIDs.
Other workers/coordinator are active: preserve their work by staying in your independent checkout.
Stop within 1200 seconds. Give brief MILESTONE inspect/implement/verify updates, then a final stdout
summary of changed paths, mechanism, actual commands/results and remaining proof, ending DONE.
Do the coding in the checkout, not as a proposed patch in the final response.
'''


def profile():
    return dict(name='engineering-invention-v2',tickets=TICKETS,fixtures=HERE/'invention-fixtures',
                guides=[RUNTIME/'SKILL.md',RUNTIME/'references/invention-methods.md'],
                checker=HERE/'invention_checks.py',protocol=HERE/'INVENTION_PROTOCOL.md',
                guidance_file='.stark-invention-guidance.md',common=COMMON,
                state='Committed synthetic base; three original public checks per task pass on small inputs; target scale not supported. No proposed algorithm, hidden checker or prior results supplied.')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--models',nargs=2);parser.add_argument('--workers',type=int,default=3);args=parser.parse_args()
    if args.action=='prepare':
        if not args.models:parser.error('prepare requires two explicit models')
        engine.prepare(args.output.resolve(),args.models,profile())
    else:engine.run(args.output.resolve(),args.workers)


if __name__=='__main__':main()
