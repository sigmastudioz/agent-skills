"""Repository-wide checks: every relative link and heading anchor resolves, and each plugin states one version."""
import json
import re
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
# In a checkout the demo media exists; a source archive (git archive, GitHub ZIP) omits it (.gitattributes).
ARCHIVED_MEDIA = any((REPO / 'assets').glob('*.mp4'))


def prose_lines(path):
    """Lines outside fenced code blocks, with inline code removed."""
    fenced = False
    for number, line in enumerate(path.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
        if line.lstrip().startswith('```'):
            fenced = not fenced
        elif not fenced:
            yield number, re.sub(r'`[^`]*`', '', line), line


def anchors(path):
    """GitHub heading anchors of a Markdown file, including the -1, -2 suffixes of repeated headings."""
    found, seen = set(), {}
    for _, _, line in prose_lines(path):
        heading = re.match(r'#{1,6}\s+(.*?)\s*#*$', line)
        if heading:
            text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', heading.group(1))
            slug = re.sub(r'[^\w\- ]', '', re.sub(r'[`*_]', '', text).strip().lower()).replace(' ', '-')
            count = seen.get(slug, 0); seen[slug] = count + 1
            found.add(slug if not count else f'{slug}-{count}')
        found.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', line))
    return found


class Links(unittest.TestCase):
    def test_relative_links_and_anchors_resolve_everywhere(self):
        broken = []
        for page in sorted(REPO.rglob('*.md')):
            if any(part in ('node_modules', '.git', '__pycache__') for part in page.parts):
                continue
            for number, text, _ in prose_lines(page):
                for target in LINK.findall(text):
                    if re.match(r'[a-z][a-z0-9+.-]*:', target):
                        continue
                    if target.endswith('?raw=true') and not ARCHIVED_MEDIA:
                        continue
                    path, _, fragment = target.partition('#')
                    path = path.split('?')[0]
                    resolved = page if not path else page.parent / path
                    where = f'{page.relative_to(REPO)}:{number} -> {target}'
                    if not resolved.exists():
                        broken.append(where + ' (missing)')
                    elif fragment and resolved.suffix == '.md' and fragment not in anchors(resolved):
                        broken.append(where + ' (no such heading)')
        self.assertEqual(broken, [])

    def test_anchor_slugs_follow_github(self):
        with tempfile.TemporaryDirectory() as folder:
            sample = Path(folder) / 'sample.md'
            sample.write_text('# Optional browser renderer: hyperframes\n## 3. Route\n## 3. Route\n```\n# not a heading\n```\n')
            self.assertEqual(anchors(sample), {'optional-browser-renderer-hyperframes', '3-route', '3-route-1'})


class Versions(unittest.TestCase):
    def test_each_plugin_states_one_version(self):
        table = (REPO / 'README.md').read_text(encoding='utf-8')
        wrong = []
        for entry in json.loads((REPO / 'catalog.json').read_text())['plugins']:
            folder = REPO / entry['path']
            name = entry['name']
            version = json.loads((folder / 'plugin.json').read_text())['version']
            for host in ('claude', 'cursor', 'codex'):
                other = json.loads((folder / f'.{host}-plugin/plugin.json').read_text())['version']
                if other != version:
                    wrong.append(f'{name}: .{host}-plugin says {other}, plugin.json says {version}')
            byline = re.search(r'version\s*(\d+\.\d+\.\d+)', '\n'.join((folder / 'README.md').read_text(encoding='utf-8').splitlines()[:6]))
            if byline and byline.group(1) != version:
                wrong.append(f'{name}: README byline says {byline.group(1)}, plugin.json says {version}')
            row = re.search(rf'\(plugins/{re.escape(name)}/README\.md\)[^\n]*\|\s*(\d+\.\d+\.\d+)\s*\|', table)
            if not row:
                wrong.append(f'{name}: no row with a version in the root README table')
            elif row.group(1) != version:
                wrong.append(f'{name}: root README table says {row.group(1)}, plugin.json says {version}')
        self.assertEqual(wrong, [])


if __name__ == '__main__':
    unittest.main()
