"""Claude PreToolUse guard: require explicit handoffs in coding workspaces."""
import json
import re
from pathlib import Path
import sys

data = json.load(sys.stdin)
if data.get('tool_name') not in {'Task', 'Agent'}:
    raise SystemExit(0)
cwd = Path(data.get('cwd', '.'))
markers = ('package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'pom.xml',
           'build.gradle', 'Gemfile', 'composer.json', 'Makefile', 'CMakeLists.txt')
roots = (cwd, *cwd.parents)
if not any((root / marker).is_file() for root in roots for marker in markers):
    raise SystemExit(0)
# Read only native user turns and tool records; never treat skill/tool text as authorization.
limit, calls, rejected = None, [], set()
try:
    for line in Path(data['transcript_path']).read_text().splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue  # Native transcript may end with an incomplete streaming record.
        message = event.get('message', {})
        content = message.get('content', [])
        text = content if isinstance(content, str) else ' '.join(b.get('text', '') for b in content if b.get('type') == 'text')
        if event.get('type') == 'user' and not event.get('isMeta'):
            words = dict(zip('no zero one two three four five six seven eight nine ten'.split(), [0, *range(11)]))
            found = re.search(r'\buse\s+(?:(?:exactly|only|at most|up to)\s+)?(\d+|' + '|'.join(words) + r')\s+(?:teammates?|subagents?|agents?|workers?)\b', text, re.I)
            if found:
                value = found[1].lower()
                limit, calls, rejected = int(value) if value.isdigit() else words[value], [], set()
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get('type') == 'tool_use' and block.get('name') in {'Task', 'Agent'} and not block.get('input', {}).get('resume'):
                if block['id'] not in calls:
                    calls.append(block['id'])
            if block.get('type') == 'tool_result' and block.get('is_error') and 'PreToolUse:' in str(block.get('content')):
                rejected.add(block.get('tool_use_id'))
except (KeyError, OSError, ValueError):
    limit = None  # Missing native history cannot establish a budget; normal handoff checks remain.
if limit is not None and not data.get('tool_input', {}).get('resume'):
    current = data.get('tool_use_id')
    calls = [call for call in calls if call not in rejected]
    if current and current not in calls:
        calls.append(current)
    if (calls.index(current) if current in calls else len(calls)) >= limit:
        print(f'Delegation budget exhausted ({limit}). User limits override optional workflows. '
              'Complete further reviews and integration in the coordinator; do not retry with another role.', file=sys.stderr)
        raise SystemExit(2)
prompt = str(data.get('tool_input', {}).get('prompt', ''))
if not re.search(r'\b(code|codebase|repo|repository|checkout|implement|refactor|debug|test|api|worker|module|service|function|architecture|source)\b|\.(m?js|tsx?|jsx|py|rs|go|java|cs|cpp)\b', prompt, re.I):
    raise SystemExit(0)
required = ('goal', 'limits', 'workspace', 'revision', 'owns', 'interfaces',
            'state', 'evidence', 'next', 'return', 'trace', 'checks', 'baseline')
handoff = {}
try:
    start = prompt.index('HANDOFF_JSON=') + len('HANDOFF_JSON=')
    handoff, _ = json.JSONDecoder().raw_decode(prompt[start:].lstrip())
except (ValueError, json.JSONDecodeError):
    pass
if not isinstance(handoff, dict):
    handoff = {}
missing = [key for key in required if not handoff.get(key)]
problem = 'Missing nonempty handoff fields: ' + ', '.join(missing) if missing else ''
if not problem:
    result = handoff['return']
    if not isinstance(result, dict) or any(not result.get(k) for k in ('paths', 'contracts', 'checks', 'gaps', 'remaining')):
        problem = 'return must be an object with nonempty paths, contracts, checks, gaps, remaining instructions'
if not problem:
    workspace = Path(str(handoff['workspace'])).expanduser()
    if not workspace.is_absolute() or not workspace.is_dir():
        problem = 'workspace must be an accessible absolute directory'
    elif workspace.resolve() != cwd.resolve():
        problem = 'workspace differs from this checkout; confirm an accessible isolated checkout in state'
        if 'isolated' in str(handoff['state']).lower():
            problem = ''
if not problem:
    baseline = Path(str(handoff['baseline'])).expanduser()
    expected = Path(__file__).resolve().parents[1] / 'SKILL.md'
    if not baseline.is_file() or baseline.resolve() != expected:
        problem = 'baseline must point to the installed domain-driven-design SKILL.md'
if problem:
    baseline = Path(__file__).resolve().parents[1] / 'SKILL.md'
    print('Delegation preflight: ' + problem + '. Prefix the prompt with HANDOFF_JSON= followed '
          'by an object with ' + ', '.join(required) + '. Read ' + str(baseline) + ' for the '
          'handoff contract. Include trace and checks fields; return is an object with paths, contracts, checks, gaps, remaining instructions. State ownership, current revision, executed checks, trace obligations, '
          'and return evidence explicitly; then retry. No user approval is needed for this correction.',
          file=sys.stderr)
    raise SystemExit(2)
note = 'User scope and teammate limits override optional workflow steps. Task briefs and pseudocode are proposals; verify them against original contracts, including injective compound identities.\nRead and apply ' + str(baseline) + ' before acting; its contents follow:\n' + baseline.read_text() + '\nPreserve task scope and others\' edits. Verify proposed algorithms against original README/contracts; challenge unsupported assumptions. Trace callers, dependencies, consumers and failure paths. Return changed paths, contracts, executed checks/results, gap IDs/status and remaining actions, including unavailable checks.'
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'updatedInput': {**data['tool_input'], 'prompt': note + '\nTask assignment follows:\n' + prompt}}}))
