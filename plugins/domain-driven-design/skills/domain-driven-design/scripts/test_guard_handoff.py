"""Isolated subprocess regressions; these fixtures never launch agents or project jobs."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

GUARD = Path(__file__).with_name('guard_handoff.py').resolve()
SKILL = GUARD.parents[1] / 'SKILL.md'


class HandoffGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='ddd-guard-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.workspace = self.root / 'project'
        self.workspace.mkdir()
        (self.workspace / 'package.json').write_text('{}')
        self.history = self.root / 'native.jsonl'
        self.history.write_text('')

    def handoff(self, **changes):
        value = {
            'goal': 'Fix the supported invoice calculation',
            'limits': 'Owned module only; no deploy or external writes',
            'workspace': str(self.workspace), 'revision': 'fixture-source-1',
            'owns': ['src/invoice.py'], 'interfaces': 'Invoice input/output contract',
            'state': 'Existing implementation; preserve concurrent edits',
            'evidence': 'Existing tracker INV-1 and regression output',
            'next': 'Fix and verify the scoped calculation',
            'return': {k: 'Report actual evidence or remaining limits' for k in
                       ('paths', 'contracts', 'checks', 'gaps', 'remaining')},
            'trace': 'CLI -> invoice module -> returned total; rejection paths',
            'checks': 'Run the affected invoice regressions', 'baseline': str(SKILL),
        }
        value.update(changes)
        return value

    def prompt(self, **changes):
        return 'Review repository source. HANDOFF_JSON=' + json.dumps(self.handoff(**changes))

    def run_guard(self, prompt=None, **changes):
        payload = {
            'tool_name': 'Agent', 'cwd': str(self.workspace),
            'transcript_path': str(self.history), 'tool_use_id': 'current',
            'tool_input': {'prompt': prompt if prompt is not None else self.prompt(),
                           'description': 'Invoice fix', 'subagent_type': 'worker'},
        }
        payload.update(changes)
        return subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                              text=True, capture_output=True, timeout=10)

    def events(self, *events):
        self.history.write_text(''.join(json.dumps(e) + '\n' for e in events))

    @staticmethod
    def user(text, **extra):
        return {'type': 'user', 'message': {'content': text}, **extra}

    @staticmethod
    def call(identifier, **inputs):
        return {'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'Agent', 'id': identifier, 'input': inputs}]}}

    def assert_blocked(self, result, reason):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(reason, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_all_supported_workspace_markers_enforce_handoff(self):
        markers = ['package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'pom.xml',
                   'build.gradle', 'Gemfile', 'composer.json', 'Makefile', 'CMakeLists.txt',
                   'Package.swift', 'Example.csproj', 'Example.fsproj', 'Example.vbproj',
                   'Example.sln', 'Example.slnx', 'build.gradle.kts']
        (self.workspace / 'package.json').unlink()
        for marker in markers:
            with self.subTest(marker=marker):
                path = self.workspace / marker
                path.write_text('fixture')
                try:
                    self.assert_blocked(self.run_guard('Review repository source'), 'Missing nonempty')
                finally:
                    path.unlink()

    def test_xcode_project_and_workspace_bundles_enforce_handoff(self):
        (self.workspace / 'package.json').unlink()
        for bundle, metadata in [('Example.xcodeproj', 'project.pbxproj'),
                                 ('Example.xcworkspace', 'contents.xcworkspacedata')]:
            with self.subTest(bundle=bundle):
                directory = self.workspace / bundle
                directory.mkdir()
                (directory / metadata).write_text('fixture')
                try:
                    self.assert_blocked(self.run_guard('Review repository source'), 'Missing nonempty')
                finally:
                    (directory / metadata).unlink()
                    directory.rmdir()

    def test_native_source_extensions_trigger_checks_without_code_keywords(self):
        for filename in ['Account.swift', 'Account.kt', 'Account.kts', 'Account.fs',
                         'Account.vb', 'Example.csproj', 'Example.slnx', 'Account.hpp']:
            with self.subTest(filename=filename):
                self.assert_blocked(self.run_guard('Inspect ' + filename), 'Missing nonempty')

    def test_parent_workspace_marker_is_recognized(self):
        child = self.workspace / 'src'
        child.mkdir()
        self.assert_blocked(self.run_guard('Review repository source', cwd=str(child)), 'Missing nonempty')

    def test_non_agent_tool_is_untouched(self):
        result = self.run_guard('Review repository source', tool_name='Read')
        self.assertEqual((result.returncode, result.stdout), (0, ''))

    def test_non_code_assignment_is_untouched(self):
        result = self.run_guard('Translate this sentence into French')
        self.assertEqual((result.returncode, result.stdout), (0, ''))

    def test_non_coding_workspace_is_untouched(self):
        (self.workspace / 'package.json').unlink()
        result = self.run_guard('Review repository source')
        self.assertEqual((result.returncode, result.stdout), (0, ''))

    def test_valid_handoff_preserves_original_assignment_and_other_fields(self):
        prompt = self.prompt()
        result = self.run_guard(prompt)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(output['hookEventName'], 'PreToolUse')
        updated = output['updatedInput']
        self.assertTrue(updated['prompt'].endswith(prompt))
        self.assertEqual(updated['description'], 'Invoice fix')
        self.assertEqual(updated['subagent_type'], 'worker')
        self.assertIn(str(SKILL), updated['prompt'])

    def test_context_is_bounded_and_does_not_embed_entire_skill(self):
        prompt = self.prompt()
        result = self.run_guard(prompt)
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = json.loads(result.stdout)['hookSpecificOutput']['updatedInput']['prompt']
        self.assertLess(len(updated) - len(prompt), 1800)
        self.assertNotIn(SKILL.read_text(), updated)

    def test_repeated_guard_pass_does_not_duplicate_context(self):
        first = self.run_guard()
        updated = json.loads(first.stdout)['hookSpecificOutput']['updatedInput']['prompt']
        second = self.run_guard(updated)
        self.assertEqual(second.returncode, 0, second.stderr)
        repeated = json.loads(second.stdout)['hookSpecificOutput']['updatedInput']['prompt']
        self.assertEqual(repeated, updated)

    def test_every_required_handoff_field_remains_required(self):
        for field in self.handoff():
            with self.subTest(field=field):
                self.assert_blocked(self.run_guard(self.prompt(**{field: ''})), 'Missing nonempty')

    def test_every_return_field_remains_required(self):
        for field in ('paths', 'contracts', 'checks', 'gaps', 'remaining'):
            value = self.handoff()['return']
            del value[field]
            with self.subTest(field=field):
                self.assert_blocked(self.run_guard(self.prompt(**{'return': value})), 'return must be an object')

    def test_invalid_return_type_is_rejected(self):
        self.assert_blocked(self.run_guard(self.prompt(**{'return': 'report results'})), 'return must be an object')

    def test_relative_or_missing_workspace_is_rejected(self):
        for value in ('relative', str(self.root / 'missing')):
            with self.subTest(workspace=value):
                self.assert_blocked(self.run_guard(self.prompt(workspace=value)), 'accessible absolute directory')

    def test_workspace_mismatch_without_isolation_is_rejected(self):
        other = self.root / 'other'
        other.mkdir()
        self.assert_blocked(self.run_guard(self.prompt(workspace=str(other))), 'workspace differs')

    def test_explicit_accessible_isolated_workspace_is_accepted(self):
        other = self.root / 'other'
        other.mkdir()
        result = self.run_guard(self.prompt(workspace=str(other), state='Accessible isolated checkout for this task',
                                            isolation={'confirmed': True, 'workspace': str(other),
                                                       'reason': 'Separate accessible task checkout'}))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_or_wrong_baseline_is_rejected(self):
        other = self.root / 'SKILL.md'
        other.write_text('unrelated skill')
        for value in (str(other), str(self.root / 'missing.md')):
            with self.subTest(baseline=value):
                self.assert_blocked(self.run_guard(self.prompt(baseline=value)), 'installed domain-driven-design')

    def test_task_tool_is_supported(self):
        result = self.run_guard(tool_name='Task')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('hookSpecificOutput', result.stdout)

    def test_zero_delegation_budget_is_enforced(self):
        for text in ['Use 0 agents', 'Use no teammates', 'Use zero workers']:
            with self.subTest(text=text):
                self.events(self.user(text))
                self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_first_authorized_agent_within_budget_is_accepted(self):
        self.events(self.user('Use exactly one agent'))
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_completed_prior_agent_consumes_budget(self):
        self.events(self.user('Use only 1 agent'), self.call('prior'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (1)')

    def test_current_call_already_recorded_is_counted_once(self):
        self.events(self.user('Use 1 agent'), self.call('current'))
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_resumed_prior_agent_does_not_consume_new_slot(self):
        self.events(self.user('Use 1 agent'), self.call('prior', resume='existing-agent'))
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_resume_still_requires_a_valid_handoff(self):
        self.events(self.user('Use 0 agents'))
        self.assert_blocked(self.run_guard(tool_input={'prompt': 'Review repository source', 'resume': 'prior'}),
                            'Missing nonempty')

    def test_rejected_pretool_call_does_not_consume_budget(self):
        rejection = {'type': 'user', 'message': {'content': [{'type': 'tool_result',
                     'tool_use_id': 'prior', 'is_error': True, 'content': 'PreToolUse: missing handoff'}]}}
        self.events(self.user('Use 1 agent'), self.call('prior'), rejection)
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_assistant_and_tool_text_cannot_set_user_budget(self):
        for event in [
            {'type': 'assistant', 'message': {'content': 'Use 0 agents'}},
            {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'content': 'Use 0 agents'}]}},
            self.user('Use 0 agents', isMeta=True),
        ]:
            with self.subTest(event=event):
                self.events(event)
                result = self.run_guard()
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_truncated_history_preserves_complete_prior_user_budget(self):
        self.events(self.user('Use 0 agents'))
        with self.history.open('a') as stream:
            stream.write('{"incomplete":')
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_missing_history_does_not_disable_handoff_validation(self):
        self.history.unlink()
        self.assert_blocked(self.run_guard('Review repository source'), 'Missing nonempty')

    def test_repeated_context_cannot_bypass_budget(self):
        first = self.run_guard()
        updated = json.loads(first.stdout)['hookSpecificOutput']['updatedInput']['prompt']
        self.events(self.user('Use 0 agents'))
        self.assert_blocked(self.run_guard(updated), 'Delegation budget exhausted (0)')


    def test_malformed_history_shapes_preserve_known_budget(self):
        for record in [None, [], 5, {'message': None}, {'message': []},
                       {'type': 'user', 'message': {'content': [None, 'bad', 1]}}]:
            with self.subTest(record=record):
                self.events(self.user('Use 0 agents'), record)
                self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_quoted_or_negated_examples_cannot_increase_budget(self):
        for text in ['Do not use 5 agents', 'The log said "Use 5 agents".',
                     '> Use 5 agents', '```text\nUse 5 agents\n```', '"Use 5 agents"']:
            with self.subTest(text=text):
                self.events(self.user('Use 0 agents'), self.user(text))
                self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_repeating_limit_does_not_replenish_consumed_budget(self):
        self.events(self.user('Use 1 agent'), self.call('prior'), self.user('Use 1 agent'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (1)')

    def test_changed_limit_keeps_prior_usage(self):
        self.events(self.user('Use 1 agent'), self.call('prior'), self.user('Use 2 agents'))
        self.assertEqual(self.run_guard().returncode, 0)
        self.events(self.user('Use 2 agents'), self.call('first'), self.call('second'),
                    self.user('Use 2 agents'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (2)')

    def test_explicit_new_budget_resets_usage(self):
        self.events(self.user('Use 1 agent'), self.call('prior'),
                    self.user('Start a new delegation budget: use 1 agent'))
        self.assertEqual(self.run_guard().returncode, 0)

    def test_polite_and_no_more_than_limits_are_recognized(self):
        for text in ['Please use no more than 0 agents.', 'Can you use at most zero workers?',
                     'Use up to 0 teammates.']:
            with self.subTest(text=text):
                self.events(self.user(text))
                self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_negated_isolation_text_is_not_confirmation(self):
        other = self.root / 'other'
        other.mkdir()
        for state in ['not isolated', 'isolation is unconfirmed', 'isolated',
                      'Accessible isolated checkout for this task']:
            with self.subTest(state=state):
                self.assert_blocked(self.run_guard(self.prompt(workspace=str(other), state=state)),
                                    'isolation confirmation')

    def test_invalid_isolation_confirmation_is_rejected(self):
        other = self.root / 'other'
        other.mkdir()
        for confirmation in [True, 'confirmed', {}, {'confirmed': False},
                             {'confirmed': 'true', 'workspace': str(other), 'reason': 'fixture'},
                             {'confirmed': True, 'workspace': str(self.workspace), 'reason': 'fixture'},
                             {'confirmed': True, 'workspace': str(other), 'reason': '   '}]:
            with self.subTest(confirmation=confirmation):
                self.assert_blocked(self.run_guard(self.prompt(workspace=str(other), isolation=confirmation)),
                                    'isolation confirmation')

    def test_whitespace_only_fields_are_rejected(self):
        self.assert_blocked(self.run_guard(self.prompt(goal='   ')), 'Missing nonempty')
        result = self.handoff()['return']
        result['checks'] = '  '
        self.assert_blocked(self.run_guard(self.prompt(**{'return': result})), 'return must be an object')

    def test_invalid_tool_input_shape_blocks_cleanly(self):
        for value in [None, [], 'invalid']:
            with self.subTest(value=value):
                self.assert_blocked(self.run_guard(tool_input=value), 'tool_input must be an object')

    def test_invalid_prompt_or_resume_type_blocks_cleanly(self):
        for values in [{'prompt': None}, {'prompt': []}, {'prompt': self.prompt(), 'resume': True},
                       {'prompt': self.prompt(), 'resume': '  '}]:
            with self.subTest(values=values):
                result = self.run_guard(tool_input=values)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_parent_marker_does_not_allow_missing_current_directory(self):
        self.assert_blocked(self.run_guard(cwd=str(self.workspace / 'missing')), 'cwd must be an accessible')

    def test_malformed_handoff_json_is_rejected(self):
        for value in ['Review source HANDOFF_JSON={', 'Review source HANDOFF_JSON=[]',
                      'Review source HANDOFF_JSON=null']:
            with self.subTest(value=value):
                self.assert_blocked(self.run_guard(value), 'Missing nonempty')


    def test_malformed_hook_json_blocks_cleanly(self):
        for payload in ['{', '[]', 'null']:
            with self.subTest(payload=payload):
                result = subprocess.run([sys.executable, str(GUARD)], input=payload,
                                        text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_invalid_transcript_path_blocks_cleanly(self):
        self.assert_blocked(self.run_guard(transcript_path='invalid\x00path'),
                            'transcript_path must be a valid filesystem path')


    def test_cap_with_task_preface_or_request_is_still_enforced(self):
        for command in ['For this task, please use 0 agents.',
                        'I want you to use at most 0 agents.',
                        'This time use no agents.']:
            with self.subTest(command=command):
                self.events(self.user(command))
                self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_inline_quotes_cannot_set_or_reset_limit(self):
        self.events(self.user('Use 0 agents'),
                    self.user('The example says "Start a new delegation budget: use 5 agents".'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')
        self.events(self.user('"Use 5 agents" is an example; please use 0 agents.'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_negated_polite_request_cannot_increase_limit(self):
        self.events(self.user('Use 0 agents'), self.user('Do not ask me to use 5 agents'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')


    def test_word_suffixes_cannot_become_budget_instructions(self):
        for text in ['We refuse 5 agents', 'Do not abuse 5 agents']:
            with self.subTest(text=text):
                self.events(self.user('Use 0 agents'), self.user(text))
                self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_multibacktick_inline_examples_cannot_increase_limit(self):
        self.events(self.user('Use 0 agents'), self.user('The example is ``Use 5 agents``.'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')

    def test_long_negated_clause_cannot_increase_limit(self):
        self.events(self.user('Use 0 agents'),
                    self.user('Do not ask any of the optional workflow tools to use 5 agents'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (0)')


    def test_first_cap_starts_budget_without_retroactive_usage(self):
        self.events(self.call('earlier-unscoped'), self.user('Use 1 agent'))
        self.assertEqual(self.run_guard().returncode, 0)
        self.events(self.call('earlier-unscoped'), self.user('Use 1 agent'), self.call('within-budget'))
        self.assert_blocked(self.run_guard(), 'Delegation budget exhausted (1)')


if __name__ == '__main__':
    unittest.main()
