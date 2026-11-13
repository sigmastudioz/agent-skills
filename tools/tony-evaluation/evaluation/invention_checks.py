#!/usr/bin/env python3
"""Frozen behavioral/resource acceptance for the two engineering-invention tasks."""
from pathlib import Path
import argparse
import copy
import importlib
import json
import math
import random
import signal
import subprocess
import sys
import tempfile
import tracemalloc
import unittest


def brute_metrics(values):
    if not values:
        return dict(count=0, sum=0, first=None, last=None, minimum=None, maximum=None, drawdown=0, rise=0)
    return dict(count=len(values), sum=sum(values), first=values[0], last=values[-1], minimum=min(values),
                maximum=max(values), drawdown=max([0]+[x-y for i,x in enumerate(values) for y in values[i:]]),
                rise=max(j-i for i in range(len(values)) for j in range(i+1,len(values)+1)
                         if all(values[k]<values[k+1] for k in range(i,j-1))))


def bounded_expand(node):
    if 'values' in node:
        return node['values'][:]
    if 'concat' in node:
        return [v for child in node['concat'] for v in bounded_expand(child)]
    return bounded_expand(node['body'])*node['repeat']


def modular_oracle(a,b,lower,upper):
    # Enumerate the bounded possible start displacements, not recurrences.
    best=None
    g=math.gcd(a.period,b.period)
    step_a,step_b=b.period//g,a.period//g
    stride=a.period*step_a
    ceil=lambda x,y:-((-x)//y)
    for displacement in range(1-b.duration,a.duration):
        c=b.start-a.start-displacement
        if c%g: continue
        i=(c//g*pow(a.period//g,-1,b.period//g))%(b.period//g) if b.period//g>1 else 0
        j=(a.start+i*a.period+displacement-b.start)//b.period
        begin=max(a.start+i*a.period,b.start+j*b.period)
        end=min(a.start+i*a.period+a.duration,b.start+j*b.period+b.duration)
        k=max(ceil(-i,step_a),ceil(-j,step_b),ceil(lower+1-end,stride))
        kmax=min((a.count-1-i)//step_a,(b.count-1-j)//step_b,(upper-1-begin)//stride)
        if k<=kmax:
            at=max(lower,begin+k*stride)
            best=at if best is None else min(best,at)
    return best


class BoundedCase(unittest.TestCase):
    def setUp(self):
        self.previous=signal.signal(signal.SIGALRM,self.expired)
        signal.setitimer(signal.ITIMER_REAL,5)

    def expired(self,*args):
        raise AssertionError('five-second case resource bound exceeded')

    def tearDown(self):
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,self.previous)
        if tracemalloc.is_tracing():tracemalloc.stop()


class WindowsChecks(BoundedCase):
    def series(self,*args):return self.model.Series(*args)
    def check(self,a,b,lo,hi,expected):self.assertEqual(self.engine.first_overlap(a,b,lo,hi),expected)

    def test_random_small_exact_oracle(self):
        rng=random.Random(73931)
        for _ in range(300):
            def series():
                period=rng.randint(1,19)
                return self.series(rng.randint(-40,40),period,rng.randint(1,min(10,period)),rng.randint(0,15))
            a,b=series(),series();lo=rng.randint(-50,80);hi=lo+rng.randint(1,100)
            points_a={t for i in range(a.count) for t in range(a.start+i*a.period,a.start+i*a.period+a.duration)}
            points_b={t for i in range(b.count) for t in range(b.start+i*b.period,b.start+i*b.period+b.duration)}
            expected=min((t for t in points_a&points_b if lo<=t<hi),default=None)
            self.check(a,b,lo,hi,expected)
            self.assertEqual(modular_oracle(a,b,lo,hi),expected)

    def test_trillion_no_collision_residue(self):
        self.check(self.series(0,100,1,10**12),self.series(1,100,1,10**12),0,10**14,None)

    def test_late_point_collision(self):
        p,q=1000003,1000033
        at=p*pow(p,-1,q)
        self.check(self.series(0,p,1,10**12),self.series(1,q,1,10**12),0,10**18,at)

    def test_finite_end_excludes_mathematical_collision(self):
        p,q=1000003,1000033;at=p*pow(p,-1,q)
        self.check(self.series(0,p,1,at//p),self.series(1,q,1,10**12),0,10**18,None)

    def test_wide_windows_huge_exact(self):
        a,b=self.series(-10**20,1000003,63,10**12),self.series(-10**20+123,1000033,64,10**12)
        lo=-10**20+10**15;hi=lo+10**12
        self.check(a,b,lo,hi,modular_oracle(a,b,lo,hi))

    def test_query_clips_inside_existing_overlap(self):
        self.check(self.series(-100,10,8,10**12),self.series(-99,10,7,10**12),10**11+3,10**11+4,10**11+3)

    def test_touching_large_series_has_no_overlap(self):
        self.check(self.series(0,128,64,10**12),self.series(64,128,64,10**12),0,10**15,None)

    def test_large_integer_translation(self):
        shift=10**40
        self.check(self.series(shift,10,4,10**12),self.series(shift+3,10,2,10**12),shift+10**10,shift+10**10+10,shift+10**10+3)

    def test_zero_count_short_circuits(self):
        self.check(self.series(0,1,1,0),self.series(0,1,1,10**12),0,10**12,None)

    def test_validation_unchanged(self):
        for args in [(0,0,1,3),(0,2,3,3),(0,100,65,3),(0,1,1,-1),(True,1,1,3)]:
            with self.assertRaises(ValueError):self.series(*args)
        for lo,hi in [(1,1),(2,1),(False,2)]:
            with self.assertRaises(ValueError):self.engine.first_overlap(self.series(0,1,1,3),self.series(0,1,1,3),lo,hi)

    def test_plan_pairs_order_and_no_mutation(self):
        request={'lower':0,'upper':10**14,'schedules':[dict(id=k,start=s,period=128,duration=2,count=10**12) for k,s in [('z',0),('b',1),('a',0)]]}
        before=copy.deepcopy(request)
        self.assertEqual(self.planner.plan(request),{'conflicts':[{'left':'a','right':'z','at':0},{'left':'a','right':'b','at':1},{'left':'b','right':'z','at':1}]})
        self.assertEqual(request,before)
        request['schedules'][1]['id']='z'
        with self.assertRaises(ValueError):self.planner.plan(request)

    def test_preview_limit_remains_bounded(self):
        with self.assertRaises(ValueError):list(self.series(0,1,1,100).occurrences(0,100,limit=3))

    def test_real_cli_large(self):
        request={'lower':0,'upper':10**15,'schedules':[dict(id='a',start=0,period=128,duration=64,count=10**12),dict(id='b',start=64,period=128,duration=64,count=10**12)]}
        self.assertEqual(self.cli_json('windows.cli',request),{'conflicts':[]})


class PulseChecks(BoundedCase):
    def test_small_random_exact_oracle(self):
        rng=random.Random(17271)
        def node(depth=0):
            if depth==3 or rng.random()<0.45:return {'values':[rng.randint(-9,9) for _ in range(rng.randrange(5))]}
            if rng.random()<0.5:return {'concat':[node(depth+1) for _ in range(rng.randrange(3))]}
            return {'repeat':rng.randrange(4),'body':node(depth+1)}
        for _ in range(180):
            program=node();values=bounded_expand(program)
            self.assertEqual(self.engine.analyze(program),brute_metrics(values))
            self.assertEqual(self.report.build(program),{'metrics':brute_metrics(values),'preview':values[:8]})

    def test_trillion_repeated_block(self):
        n=10**12;program={'repeat':n,'body':{'values':[3,-2,5]}}
        self.assertEqual(self.engine.analyze(program),dict(count=3*n,sum=6*n,first=3,last=5,minimum=-2,maximum=5,drawdown=7,rise=2))

    def test_nested_repetition_large(self):
        n=10**12;program={'repeat':n,'body':{'repeat':n,'body':{'values':[1,2,0,-3]}}}
        self.assertEqual(self.engine.analyze(program),dict(count=4*n*n,sum=0,first=1,last=-3,minimum=-3,maximum=2,drawdown=5,rise=3))

    def test_empty_repeat_does_not_loop(self):
        program={'concat':[{'repeat':10**12,'body':{'concat':[]}},{'values':[9]}]}
        self.assertEqual(self.report.build(program),{'metrics':brute_metrics([9]),'preview':[9]})

    def test_cross_boundary_rise(self):
        program={'concat':[{'values':[9,-2,-1]},{'values':[]},{'values':[0,1,2,-4]}]}
        self.assertEqual(self.engine.analyze(program),brute_metrics([9,-2,-1,0,1,2,-4]))

    def test_cross_boundary_drawdown_order(self):
        for values in [[10,3,7,-2],[-2,3,7,10],[5,5,5],[-8,-12,-7]]:
            self.assertEqual(self.engine.analyze({'concat':[{'values':values[:2]},{'values':values[2:]}]}),brute_metrics(values))

    def test_zero_repeat_still_validates(self):
        for program in [{'repeat':0,'body':{'values':[True]}},{'repeat':True,'body':{'values':[]}},{'concat':[{'values':[1.5]}]},{'values':[], 'extra':0}]:
            with self.assertRaises(ValueError):self.engine.analyze(program)

    def test_arbitrary_integer_exactness(self):
        big=10**60;n=10**12
        program={'repeat':n,'body':{'values':[big,-big]}}
        self.assertEqual(self.engine.analyze(program),dict(count=2*n,sum=0,first=big,last=-big,minimum=-big,maximum=big,drawdown=2*big,rise=2))

    def test_no_input_mutation(self):
        program={'repeat':4,'body':{'values':[1,2,3]}};before=copy.deepcopy(program)
        self.report.build(program);self.assertEqual(program,before)

    def test_preview_bounded_on_huge_nonempty(self):
        program={'repeat':10**12,'body':{'values':[3,-2,5]}}
        report=self.report.build(program)
        self.assertEqual(report['preview'],[3,-2,5,3,-2,5,3,-2])
        self.assertEqual(report['metrics']['count'],3*10**12)

    def test_peak_allocations_follow_recipe_not_stream(self):
        program={'repeat':1000000,'body':{'values':[4,-1,7,2]}}
        tracemalloc.start()
        result=self.engine.analyze(program)
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        self.assertEqual(result['count'],4000000)
        self.assertLess(peak,8*1024*1024,'encoded-input workload exceeded 8 MiB traced allocation gate')

    def test_expand_reference_limit_preserved(self):
        with self.assertRaises(ValueError):list(self.recipe.expand({'values':[1,2,3]},limit=2))

    def test_real_cli_huge_with_empty_prefix(self):
        program={'concat':[{'repeat':10**12,'body':{'values':[]}},{'repeat':10**12,'body':{'values':[1,2]}}]}
        result=self.cli_json('pulse.cli',program)
        self.assertEqual(result['preview'],[1,2,1,2,1,2,1,2])
        self.assertEqual(result['metrics'],dict(count=2*10**12,sum=3*10**12,first=1,last=2,minimum=1,maximum=2,drawdown=1,rise=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--task',choices=['windows','pulse'],required=True);parser.add_argument('--candidate',type=Path,required=True);args=parser.parse_args()
    candidate=args.candidate.resolve();sys.path.insert(0,str(candidate))
    cls=WindowsChecks if args.task=='windows' else PulseChecks
    package='windows' if args.task=='windows' else 'pulse'
    for name in (['model','engine','planner'] if package=='windows' else ['recipe','engine','report']):
        setattr(cls,name,importlib.import_module(package+'.'+name))
    def cli_json(self,module,payload):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'request.json';path.write_text(json.dumps(payload))
            completed=subprocess.run([sys.executable,'-m',module,str(path)],cwd=candidate,capture_output=True,text=True,timeout=4)
            self.assertEqual(completed.returncode,0,completed.stderr)
            return json.loads(completed.stdout)
    cls.cli_json=cli_json
    import io
    stream=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromTestCase(cls);result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    failed={str(t).split()[0] for t,_ in result.failures+result.errors}
    print(json.dumps({'task':args.task,'checks':result.testsRun,'passed':result.wasSuccessful(),'passed_checks':result.testsRun-len(failed),'failed_checks':sorted(failed),'failures':len(result.failures),'errors':len(result.errors),'summary':stream.getvalue()},indent=2))
    return int(not result.wasSuccessful())


if __name__=='__main__':sys.exit(main())
