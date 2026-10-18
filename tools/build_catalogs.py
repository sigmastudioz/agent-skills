"""Generate native catalogs from one registry; plugin manifests own versions and descriptions."""
from pathlib import Path
import argparse
import hashlib
import json
import re


def render(root):
    root = Path(root).resolve()
    registry = json.loads((root / 'catalog.json').read_text())
    native, codex, seen, releases = [], [], set(), {}
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
        for host in ('claude', 'cursor', 'codex'):
            compatibility_path = (manifest_path.parent / f'.{host}-plugin/plugin.json').resolve()
            if root not in compatibility_path.parents:
                raise ValueError('Compatibility manifest resolves outside the repository')
            compatibility = json.loads(compatibility_path.read_text())
            if any(compatibility.get(key) != manifest.get(key) for key in ('name', 'version', 'author')):
                raise ValueError('Compatibility identity/version/author differs: ' + host + '/' + name)
        native.append({'name': name, 'source': relative, 'description': manifest['description']})
        codex.append({'name': name, 'source': {'source': 'local', 'path': relative},
                      'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                      'category': entry.get('category', 'Productivity')})
        files = {}
        for path in sorted(manifest_path.parent.rglob('*')):
            if path.is_symlink():
                raise ValueError('Distribution must be self-contained: ' + str(path))
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                files[path.relative_to(manifest_path.parent).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        releases[name] = {'version': manifest['version'], 'files': files}
    return {
        '.claude-plugin/marketplace.json': {'name': registry['name'], 'owner': registry['publisher'],
            'description': registry['description'], 'plugins': native},
        '.cursor-plugin/marketplace.json': {'name': registry['name'], 'owner': registry['publisher'],
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
