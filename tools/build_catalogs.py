"""Generate native catalogs from one registry; plugin manifests own versions and descriptions."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.parse import urlsplit


# OS metadata files that git ignores and must never be hashed into a release.
JUNK_FILES = {'.DS_Store', 'Thumbs.db', 'desktop.ini'}
# Local tool folders (git-ignored) that never ship: virtualenvs, package and test caches.
JUNK_DIRS = {'.venv', 'venv', 'node_modules', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}


def cursor_identity(author):
    """Cursor's strict author/owner objects accept name and email only."""
    return {key: author[key] for key in ('name', 'email') if key in author}


def terms_url(interface, name):
    """Require an HTTPS terms link before producing an uploadable release inventory."""
    value = interface.get('termsOfServiceURL')
    message = 'Terms of service URL must be a public HTTPS URL: ' + name
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        raise ValueError(message)
    try:
        parsed = urlsplit(value)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError(message)
    except ValueError as error:
        raise ValueError(message) from error
    return value


def validate_listing_text(interface, name):
    """Apply public-submission text limits, which can be stricter than draft uploads."""
    for field, limit in (('displayName', 30), ('shortDescription', 30),
                         ('longDescription', 4000), ('developerName', 80)):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            raise ValueError(f'Listing {field} must contain 1–{limit} characters: {name}')


def antigravity_manifest(manifest, interface, display_name, folder, prompts):
    """Adapt existing metadata; Antigravity discovers the unchanged skills/ tree."""
    for skill in folder.glob('skills/*/SKILL.md'):
        content = skill.read_text(encoding='utf-8')
        body = content.split('\n---\n', 1)[-1] if content.startswith('---\n') else content
        if len(body.encode('utf-8')) > 24000:
            raise ValueError('Antigravity loads only 24,000 skill-body bytes; link conditional detail: '
                             + str(skill))
    logo = interface.get('logo')
    if not isinstance(logo, str) or not logo or Path(logo).is_absolute():
        raise ValueError('Antigravity needs a bundled logo: ' + manifest['name'])
    resolved = (folder / logo).resolve()
    if folder.resolve() not in resolved.parents or not resolved.is_file():
        raise ValueError('Antigravity logo must resolve inside its plugin: ' + manifest['name'])
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or any(
            not isinstance(prompt, str) or not prompt.strip() for prompt in prompts):
        raise ValueError('Antigravity needs one to three starter prompts: ' + manifest['name'])
    return {'$schema': 'https://antigravity.google/schemas/v1/plugin.json',
            **{key: manifest[key] for key in ('name', 'version', 'description', 'author',
                                              'homepage', 'repository', 'license') if key in manifest},
            'displayName': display_name, 'logo': logo, 'suggestedPrompts': prompts,
            'keywords': manifest.get('keywords', [])}


def render(root):
    root = Path(root).resolve()
    registry = json.loads((root / 'catalog.json').read_text())
    native, claude, codex, seen, claude_names, releases, adapters = [], [], [], set(), set(), {}, {}
    for entry in registry['plugins']:
        name, relative = entry['name'], entry['path']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name in seen:
            raise ValueError('Invalid or duplicate plugin name: ' + name)
        seen.add(name)
        if not relative.startswith('./') or '..' in Path(relative).parts:
            raise ValueError('Plugin path must stay inside the repository: ' + relative)
        manifest_path = (root / relative / 'plugin.json').resolve()
        if root not in manifest_path.parents:
            raise ValueError('Plugin resolves outside the repository: ' + relative)
        manifest = json.loads(manifest_path.read_text())
        if manifest['name'] != name or not manifest.get('version') or not manifest.get('description'):
            raise ValueError('Plugin identity/version/description missing or inconsistent: ' + name)
        interface = manifest.get('extensions', {}).get('com.openai', {}).get('interface', {})
        terms = terms_url(interface, name)
        validate_listing_text(interface, name)
        claude_name = entry.get('claudeName', name)
        if (not isinstance(claude_name, str) or len(claude_name) > 64
                or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', claude_name)
                or claude_name in claude_names):
            raise ValueError('Invalid or duplicate Claude plugin name: ' + str(claude_name))
        claude_names.add(claude_name)
        display_name = name
        for host in ('claude', 'cursor', 'codex'):
            compatibility_path = (manifest_path.parent / f'.{host}-plugin/plugin.json').resolve()
            if root not in compatibility_path.parents:
                raise ValueError('Compatibility manifest resolves outside the repository')
            compatibility = json.loads(compatibility_path.read_text())
            if host == 'codex' and terms_url(compatibility.get('interface', {}), name) != terms:
                raise ValueError('Terms of service URL differs in Codex fallback: ' + name)
            if host == 'codex':
                validate_listing_text(compatibility['interface'], name)
                for field in ('displayName', 'shortDescription', 'longDescription', 'developerName', 'category'):
                    if compatibility['interface'].get(field) != interface.get(field):
                        raise ValueError(f'Listing {field} differs in Codex fallback: {name}')
            expected_author = manifest.get('author', {})
            if host == 'cursor':
                expected_author = cursor_identity(expected_author)
            expected_name = claude_name if host == 'claude' else name
            if (compatibility.get('name') != expected_name
                    or compatibility.get('version') != manifest.get('version')
                    or compatibility.get('author') != expected_author):
                raise ValueError('Compatibility identity/version/author differs: ' + host + '/' + name)
            if host == 'claude':
                display_name = compatibility.get('displayName', name)
        adapter_path = (Path(relative) / '.antigravity-plugin/plugin.json').as_posix()
        adapter = antigravity_manifest(manifest, interface, display_name, manifest_path.parent,
                                      entry.get('antigravityPrompts', interface.get('defaultPrompt', [])))
        adapters[adapter_path] = adapter
        claude.append({'name': claude_name, 'source': relative, 'description': manifest['description']})
        native.append({'name': name, 'source': relative, 'description': manifest['description']})
        codex.append({'name': name, 'source': {'source': 'local', 'path': relative},
                      'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                      'category': entry.get('category', 'Productivity')})
        files = {}
        for path in sorted(manifest_path.parent.rglob('*')):
            if JUNK_DIRS.intersection(path.relative_to(manifest_path.parent).parts):
                continue
            if path.is_symlink():
                raise ValueError('Distribution must be self-contained: ' + str(path))
            if (path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc'
                    and path.name not in JUNK_FILES):
                files[path.relative_to(manifest_path.parent).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        files['.antigravity-plugin/plugin.json'] = hashlib.sha256(
            (json.dumps(adapter, indent=2) + '\n').encode()).hexdigest()
        files = dict(sorted(files.items()))
        releases[name] = {'version': manifest['version'], 'files': files}
    return {
        **adapters,
        '.claude-plugin/marketplace.json': {'name': registry['name'], 'owner': registry['publisher'],
            'description': registry['description'], 'plugins': claude},
        '.cursor-plugin/marketplace.json': {'name': registry['name'], 'owner': cursor_identity(registry['publisher']),
            'metadata': {'description': registry['description']}, 'plugins': native},
        '.agents/plugins/marketplace.json': {'name': registry['name'],
            'interface': {'displayName': registry['displayName']}, 'plugins': codex},
        'release.json': {'catalog': registry['name'], 'plugins': releases},
    }


def build(root, check=False):
    root = Path(root).resolve()
    outputs = render(root)  # Validate every plugin before modifying any catalog.
    stale = []
    for relative, data in outputs.items():
        path = root / relative
        encoded = json.dumps(data, indent=2) + '\n'
        if not path.exists() or path.read_text() != encoded:
            stale.append(relative)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(encoded)
    if check and stale:
        raise ValueError('Catalogs need regeneration: ' + ', '.join(stale))
    return len(outputs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        count = build(Path(__file__).resolve().parents[1], args.check)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print(f'{count} catalog/release files ' + ('verified.' if args.check else 'generated.'))
