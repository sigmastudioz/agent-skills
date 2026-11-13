#!/usr/bin/env python3
"""Read-only automated portion of the runner-utility trial; measurement protocol is audited separately."""
from pathlib import Path
import argparse
import hashlib
import json

HERE=Path(__file__).resolve().parent
EXPECTED={'lookup':'granite','codec':'violet'}


def check(task,candidate):
    candidate=candidate.resolve();fixture=HERE/'runner-fixtures'/task
    changed=[]
    for source in fixture.rglob('*'):
        if not source.is_file() or '__pycache__' in source.parts or source.suffix=='.pyc':continue
        target=candidate/source.relative_to(fixture)
        if not target.is_file() or target.is_symlink() or hashlib.sha256(target.read_bytes()).digest()!=hashlib.sha256(source.read_bytes()).digest():changed.append(str(source.relative_to(fixture)))
    errors=[];decision={};evidence=None
    try:
        decision=json.loads((candidate/'decision.json').read_text())
        if not isinstance(decision,dict):raise ValueError('decision must be an object')
        if not isinstance(decision.get('reason'),str) or not decision['reason'].strip():errors.append('missing reason')
        path=decision.get('evidence_path')
        if not isinstance(path,str):raise ValueError('evidence_path must be text')
        evidence=(candidate/path).resolve()
        if candidate not in evidence.parents or evidence.is_symlink():raise ValueError('evidence must be contained')
        parsed=json.loads(evidence.read_text())
        if not isinstance(parsed,(dict,list)) or not parsed:raise ValueError('empty measurement evidence')
    except (OSError,ValueError,TypeError) as error:errors.append(str(error))
    correct=decision.get('winner')==EXPECTED[task]
    return dict(task=task,decision_correct=correct,inputs_unchanged=not changed,changed_inputs=changed,
                evidence_json_present=evidence is not None and not errors,errors=errors,
                automated_checks_passed=correct and not changed and not errors,
                manual_measurement_audit_required=True,
                note='Winner and JSON presence alone do not prove executed measurements. Apply the frozen measurement rubric to actual tool receipts and measurement source.')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--task',choices=EXPECTED,required=True);parser.add_argument('--candidate',type=Path,required=True);args=parser.parse_args()
    report=check(args.task,args.candidate);print(json.dumps(report,indent=2));return int(not report['automated_checks_passed'])


if __name__=='__main__':raise SystemExit(main())
