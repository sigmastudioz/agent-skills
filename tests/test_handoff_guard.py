from pathlib import Path
import json,subprocess,sys,tempfile,unittest
SCRIPT=Path(__file__).resolve().parents[1]/'plugins/domain-driven-design/skills/domain-driven-design/scripts/guard_handoff.py'
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.cwd=Path(self.temp.name)
  (self.cwd/'package.json').write_text('{}')
 def run_guard(self,prompt,tool='Agent',cwd=None,events=None,use_id='current',resume=None):
  data={'tool_name':tool,'cwd':str(cwd or self.cwd),'tool_input':{'prompt':prompt,'description':'bounded task'},'tool_use_id':use_id}
  if resume:data['tool_input']['resume']=resume
  if events is not None:
   transcript=self.cwd/'native.jsonl';transcript.write_text('\n'.join(json.dumps(e) for e in events));data['transcript_path']=str(transcript)
  return subprocess.run([sys.executable,str(SCRIPT)],input=json.dumps(data),capture_output=True,text=True)
 def payload(self):
  return {'goal':'Implement refunds','limits':'One worker; no commits or installs','workspace':str(self.cwd),'revision':'working-tree, no edits yet','owns':['packages/billing/src/services/refund.mjs'],'interfaces':'API and worker use billing facade','state':'Shared checkout; parent owns integration','evidence':'node --test: existing tests pass; trace README API -> billing -> store','next':'Implement and trace error paths','return':{k:'Report '+k for k in ['paths','contracts','checks','gaps','remaining']},'trace':'API -> billing -> store -> worker retry; failure cases','checks':'node --test','baseline':str(SCRIPT.parents[1]/'SKILL.md')}
 def test_rejects_missing_handoff(self):self.assertEqual(self.run_guard('Explore the repo').returncode,2)
 def test_accepts_complete_handoff(self):
  result=self.run_guard('HANDOFF_JSON='+json.dumps(self.payload()));self.assertEqual(result.returncode,0)
  hook=json.loads(result.stdout)['hookSpecificOutput'];self.assertEqual(hook['hookEventName'],'PreToolUse')
  self.assertNotIn('permissionDecision',hook);self.assertEqual(hook['updatedInput']['description'],'bounded task')
  prompt=hook['updatedInput']['prompt'];self.assertIn('Read and apply '+str(SCRIPT.parents[1]/'SKILL.md'),prompt);self.assertIn('gap IDs/status',prompt)
  self.assertIn((SCRIPT.parents[1]/'SKILL.md').read_text(),prompt)
 def test_rejects_inaccessible_workspace(self):
  d=self.payload();d['workspace']='/does-not-exist';self.assertEqual(self.run_guard('HANDOFF_JSON='+json.dumps(d)).returncode,2)
 def test_rejects_wrong_baseline(self):
  d=self.payload();d['baseline']=str(self.cwd/'package.json');self.assertEqual(self.run_guard('HANDOFF_JSON='+json.dumps(d)).returncode,2)
 def test_rejects_thin_return(self):
  d=self.payload();d['return']='Done';self.assertEqual(self.run_guard('HANDOFF_JSON='+json.dumps(d)).returncode,2)
 def test_rejects_missing_trace(self):
  d=self.payload();del d['trace'];self.assertEqual(self.run_guard('HANDOFF_JSON='+json.dumps(d)).returncode,2)
 def test_read_tools_unaffected(self):self.assertEqual(self.run_guard('',tool='Read').returncode,0)
 def test_prose_assignment_in_coding_workspace_unaffected(self):self.assertEqual(self.run_guard('Write a poem about summer').returncode,0)
 def test_noncoding_workspace_unaffected(self):
  (self.cwd/'package.json').unlink();self.assertEqual(self.run_guard('Write a poem').returncode,0)
 def user(self,text,meta=False):return {'type':'user','isMeta':meta,'message':{'content':text}}
 def call(self,id):return {'type':'assistant','message':{'content':[{'type':'tool_use','name':'Agent','id':id,'input':{'prompt':'review source'}}]}}
 def result(self,id,error=False):return {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':id,'is_error':error,'content':'PreToolUse:Agent hook error' if error else 'agentId: native-worker'}]}}
 def complete(self,**kw):return self.run_guard('HANDOFF_JSON='+json.dumps(self.payload()),**kw)
 def test_first_pending_dispatch_allowed(self):self.assertEqual(self.complete(events=[self.user('Use one teammate for implementation.'),self.call('current')]).returncode,0)
 def test_extra_review_dispatch_blocked(self):
  r=self.complete(events=[self.user('Use one teammate for implementation.'),self.call('first'),self.result('first'),self.call('current')])
  self.assertEqual(r.returncode,2);self.assertIn('budget exhausted (1)',r.stderr)
 def test_numeric_limit_and_zero(self):
  self.assertEqual(self.complete(events=[self.user('Use at most 0 agents.')]).returncode,2)
  self.assertEqual(self.complete(events=[self.user('Use only two subagents.'),self.call('first'),self.result('first')]).returncode,0)
 def test_rejected_handoff_does_not_consume_budget(self):
  self.assertEqual(self.complete(events=[self.user('Use one teammate.'),self.call('rejected'),self.result('rejected',True)]).returncode,0)
 def test_skill_text_cannot_expand_user_budget(self):
  events=[self.user('Use one teammate.'),self.call('first'),self.result('first'),self.user('Use 8 agents.',True)]
  self.assertEqual(self.complete(events=events).returncode,2)
 def test_later_explicit_user_budget_starts_new_interval(self):
  events=[self.user('Use one teammate.'),self.call('first'),self.result('first'),self.user('Use one teammate for this next task.')]
  self.assertEqual(self.complete(events=events).returncode,0)
 def test_parallel_pending_calls_reserve_in_transcript_order(self):
  events=[self.user('Use one teammate.'),self.call('a'),self.call('b')]
  self.assertEqual(self.complete(events=events,use_id='a').returncode,0)
  self.assertEqual(self.complete(events=events,use_id='b').returncode,2)
 def test_resume_existing_worker_is_not_new_dispatch(self):
  events=[self.user('Use one teammate.'),self.call('first'),self.result('first')]
  self.assertEqual(self.complete(events=events,resume='native-worker').returncode,0)
 def test_prose_agent_still_counts_under_explicit_user_budget(self):
  events=[self.user('Use one teammate.'),self.call('first'),self.result('first')]
  self.assertEqual(self.run_guard('Write a poem',events=events).returncode,2)
 def test_no_explicit_limit_preserves_normal_handoff_flow(self):
  self.assertEqual(self.complete(events=[self.user('Implement a feature.'),self.call('first'),self.result('first')]).returncode,0)
 def test_user_text_blocks_are_recognized(self):
  message={'type':'user','message':{'content':[{'type':'text','text':'Use zero workers.'}]}}
  self.assertEqual(self.complete(events=[message]).returncode,2)
 def test_worker_receives_baseline_before_proposed_task(self):
  r=self.complete();p=json.loads(r.stdout)['hookSpecificOutput']['updatedInput']['prompt']
  self.assertLess(p.index('# Principal Domain-Driven Design'),p.index('HANDOFF_JSON='))
if __name__=='__main__':unittest.main(verbosity=2)
