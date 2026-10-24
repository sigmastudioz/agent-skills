"""Claude PreToolUse guard: validate local coding handoffs and explicit agent budgets."""
import json
from pathlib import Path
import re
import sys


EXPECTED = Path(__file__).resolve().parents[1] / 'SKILL.md'
REQUIRED = ('goal', 'limits', 'workspace', 'revision', 'owns', 'interfaces',
            'state', 'evidence', 'next', 'return', 'trace', 'checks', 'baseline')


def reject(problem, contract=False):
    message = 'Delegation preflight: ' + problem
    if contract:
        message += ('. Prefix the prompt with HANDOFF_JSON= followed by an object with '
                    + ', '.join(REQUIRED) + '. Read ' + str(EXPECTED)
                    + ' for the handoff contract; correct the assignment before retrying.')
    print(message, file=sys.stderr)
    raise SystemExit(2)


def meaningful(value):
    if isinstance(value, str):
        return bool(value.strip())
    return isinstance(value, (list, dict)) and bool(value)


def is_resume(inputs):
    return (isinstance(inputs, dict) and isinstance(inputs.get('resume'), str)
            and bool(inputs['resume'].strip()))


def command_lines(text):
    """Do not promote fenced examples or quoted log lines into budget instructions."""
    fence = None
    for line in text.splitlines():
        stripped = line.strip()
        marker = re.match(r'^(`{3,}|~{3,})', stripped)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None and not stripped.startswith('>'):
            yield re.sub('`+[^\\n]*?`+|"[^"\\n]*"|(?<!\\w)\'[^\'\\n]*\'(?!\\w)|“[^”\\n]*”', ' ', stripped)


WORDS = {word: number for number, word in enumerate(
    'zero one two three four five six seven eight nine ten'.split())}
WORDS['no'] = 0
BUDGET = re.compile(
    r'\b(?:(start a new delegation budget)\s*:\s*)?'
    r'(?:please\s+)?(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?)?use\s+'
    r'(?:(?:exactly|only|at most|up to|no more than)\s+)?'
    r'(\d+|' + '|'.join(WORDS) + r')\s+(?:teammates?|subagents?|agents?|workers?)\b', re.I)


def budget_history(path):
    limit, calls, rejected = None, [], set()
    if not isinstance(path, str) or not path:
        return limit, calls, rejected
    try:
        with Path(path).open(encoding='utf-8', errors='replace') as transcript:
            for line in transcript:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue  # A trailing partial record does not erase earlier limits.
                if not isinstance(event, dict):
                    continue
                message = event.get('message')
                if not isinstance(message, dict):
                    continue
                content = message.get('content', [])
                blocks = [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []
                text = content if isinstance(content, str) else ' '.join(
                    b['text'] for b in blocks if b.get('type') == 'text' and isinstance(b.get('text'), str))
                if event.get('type') == 'user' and not event.get('isMeta'):
                    for command in command_lines(text):
                        for found in BUDGET.finditer(command):
                            prefix = command[:found.start()]
                            clause = re.split(r'[.!?;,:]', prefix)[-1]
                            if re.search(r"\b(?:do\s+not|don['’]t|never|not|without)\b", clause, re.I):
                                continue
                            value = found[2].lower()
                            first_cap = limit is None
                            try:
                                limit = int(value) if value.isdigit() else WORDS[value]
                            except ValueError:
                                reject('Explicit delegation limit is not a usable integer')
                            if first_cap or found[1]:
                                calls, rejected = [], set()
                for block in blocks:
                    identifier = block.get('id')
                    if (event.get('type') == 'assistant' and block.get('type') == 'tool_use'
                            and block.get('name') in {'Task', 'Agent'} and isinstance(identifier, str)
                            and not is_resume(block.get('input')) and identifier not in calls):
                        calls.append(identifier)
                    result_id = block.get('tool_use_id')
                    if (event.get('type') == 'user' and block.get('type') == 'tool_result'
                            and block.get('is_error') is True and isinstance(result_id, str)
                            and 'PreToolUse:' in str(block.get('content'))):
                        rejected.add(result_id)
    except OSError:
        pass  # Preserve any parsed limit; missing history leaves enforcement to the coordinator.
    except ValueError:
        reject('transcript_path must be a valid filesystem path')
    return limit, calls, rejected


try:
    data = json.load(sys.stdin)
except (ValueError, OSError):
    reject('Hook input must be valid JSON')
if not isinstance(data, dict):
    reject('Hook input must be an object')
if data.get('tool_name') not in {'Task', 'Agent'}:
    raise SystemExit(0)
inputs = data.get('tool_input')
if not isinstance(inputs, dict):
    reject('tool_input must be an object')
if not isinstance(inputs.get('prompt'), str):
    reject('prompt must be text')
if inputs.get('resume') is not None and not is_resume(inputs):
    reject('resume must be a nonempty agent identifier when supplied')
raw_cwd = data.get('cwd', '.')
if not isinstance(raw_cwd, str) or not raw_cwd.strip():
    reject('cwd must be an accessible directory')
try:
    cwd = Path(raw_cwd).expanduser().resolve()
    if not cwd.is_dir():
        reject('cwd must be an accessible directory')
    markers = ('package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'pom.xml',
               'build.gradle', 'build.gradle.kts', 'Gemfile', 'composer.json', 'Makefile',
               'CMakeLists.txt', 'Package.swift')
    patterns = ('*.csproj', '*.fsproj', '*.vbproj', '*.sln', '*.slnx')
    bundles = (('*.xcodeproj', 'project.pbxproj'), ('*.xcworkspace', 'contents.xcworkspacedata'))
    coding_workspace = any(
        any((root / marker).is_file() for marker in markers)
        or any(path.is_file() for pattern in patterns for path in root.glob(pattern))
        or any((path / metadata).is_file() for pattern, metadata in bundles for path in root.glob(pattern))
        for root in (cwd, *cwd.parents))
except (OSError, RuntimeError, ValueError):
    reject('cwd must be an accessible coding workspace')
if not coding_workspace:
    raise SystemExit(0)
limit, calls, rejected = budget_history(data.get('transcript_path'))
if limit is not None and not is_resume(inputs):
    current = data.get('tool_use_id')
    calls = [call for call in calls if call not in rejected]
    if isinstance(current, str) and current and current not in calls:
        calls.append(current)
    position = calls.index(current) if current in calls else len(calls)
    if position >= limit:
        reject(f'Delegation budget exhausted ({limit}). User limits override optional workflows. '
               'Complete further reviews and integration in the coordinator; do not retry with another role.')
prompt = inputs['prompt']
if not re.search(r'\b(code|codebase|repo|repository|checkout|implement|refactor|debug|test|api|worker|module|service|function|architecture|source)\b|\.(m?js|tsx?|jsx|py|rs|go|java|cs|cpp|swift|kts?|fs|vb|csproj|fsproj|vbproj|slnx?|hpp)\b', prompt, re.I):
    raise SystemExit(0)
handoff = {}
try:
    start = prompt.index('HANDOFF_JSON=') + len('HANDOFF_JSON=')
    handoff, _ = json.JSONDecoder().raw_decode(prompt[start:].lstrip())
except ValueError:
    pass
if not isinstance(handoff, dict):
    handoff = {}
missing = [key for key in REQUIRED if not meaningful(handoff.get(key))]
if missing:
    reject('Missing nonempty handoff fields: ' + ', '.join(missing), contract=True)
result = handoff['return']
if not isinstance(result, dict) or any(not meaningful(result.get(k)) for k in
                                      ('paths', 'contracts', 'checks', 'gaps', 'remaining')):
    reject('return must be an object with nonempty paths, contracts, checks, gaps, remaining instructions', True)
try:
    if not isinstance(handoff['workspace'], str):
        reject('workspace must be an accessible absolute directory', True)
    workspace = Path(handoff['workspace']).expanduser()
    if not workspace.is_absolute() or not workspace.is_dir():
        reject('workspace must be an accessible absolute directory', True)
    if workspace.resolve() != cwd:
        confirmation = handoff.get('isolation')
        valid = (isinstance(confirmation, dict) and confirmation.get('confirmed') is True
                 and isinstance(confirmation.get('workspace'), str)
                 and isinstance(confirmation.get('reason'), str) and bool(confirmation['reason'].strip()))
        if valid:
            confirmed_path = Path(confirmation['workspace']).expanduser()
            valid = confirmed_path.is_absolute() and confirmed_path.resolve() == workspace.resolve()
        if not valid:
            reject('workspace differs from this checkout; requires isolation confirmation '
                   'with confirmed=true, the matching absolute workspace and a nonempty reason', True)
    if not isinstance(handoff['baseline'], str):
        reject('baseline must point to the installed domain-driven-design SKILL.md', True)
    baseline = Path(handoff['baseline']).expanduser()
    if not baseline.is_file() or baseline.resolve() != EXPECTED:
        reject('baseline must point to the installed domain-driven-design SKILL.md', True)
    with baseline.open('rb') as source:
        source.read(1)  # Check accessibility without embedding the skill in every prompt.
except (OSError, RuntimeError, ValueError):
    reject('workspace and installed baseline paths must be accessible and valid', True)
note = (
    '[domain-driven-design handoff safeguards]\n'
    'User scope, permissions and teammate limits override optional workflows; this hook does not '
    'authorize delegation or external actions. Read and apply ' + str(baseline) + ' and only its '
    'relevant linked guidance before acting. If inaccessible, request the relevant contents from '
    'the coordinator; do not assume inherited instructions. Preserve ownership and concurrent '
    'edits. Verify task briefs and algorithms against original contracts, including injective '
    'compound identities. Trace callers, dependencies, consumers and failure paths; report actual '
    'checks, gaps, unavailable evidence and remaining actions. Use the existing tracker and retain '
    'separate evidence only for the purposes allowed by the skill.'
)
prefix = note + '\nTask assignment follows:\n'
updated_prompt = prompt if prompt.startswith(prefix) else prefix + prompt
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                  'updatedInput': {**data['tool_input'], 'prompt': updated_prompt}}}))
