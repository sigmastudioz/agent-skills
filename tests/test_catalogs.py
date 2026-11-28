"""Exercise adding real plugin entries and reject unsafe/stale distributions."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('catalogs', Path(__file__).resolve().parents[1] / 'tools/build_catalogs.py')
catalogs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalogs)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.registry = {'name': 'example', 'displayName': 'Example Skills', 'description': 'Example',
                         'publisher': {'name': 'Example author'}, 'plugins': []}
        self.add_plugin('first', '1.0.0')

    def add_plugin(self, name, version):
        directory = self.root / 'plugins' / name
        directory.mkdir(parents=True)
        terms = 'https://example.com/terms'
        interface = {'termsOfServiceURL': terms, 'displayName': name, 'shortDescription': name,
                     'longDescription': name, 'developerName': 'Example author',
                     'logo': './assets/icon.svg', 'defaultPrompt': ['Help with this skill']}
        manifest = {'name': name, 'version': version, 'description': name, 'author': {'name': 'Example author'},
                    'extensions': {'com.openai': {'interface': interface}}}
        (directory / 'plugin.json').write_text(json.dumps(manifest))
        (directory / 'assets').mkdir()
        (directory / 'assets/icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        for host in ('claude', 'cursor', 'codex'):
            path = directory / f'.{host}-plugin/plugin.json'
            native = dict(manifest)
            if host == 'codex':
                native['interface'] = interface
            path.parent.mkdir(); path.write_text(json.dumps(native))
        self.registry['plugins'].append({'name': name, 'path': './plugins/' + name})
        self.save()

    def save(self):
        (self.root / 'catalog.json').write_text(json.dumps(self.registry))

    def test_add_second_plugin_reaches_all_hosts_without_rewriting_versions(self):
        self.add_plugin('second', '2.3.4')
        catalogs.build(self.root)
        for path, data in catalogs.render(self.root).items():
            if path == 'release.json':
                self.assertEqual(data['plugins']['first']['version'], '1.0.0')
                self.assertEqual(data['plugins']['second']['version'], '2.3.4')
                continue
            actual = json.loads((self.root / path).read_text())
            if '/.antigravity-plugin/' in path:
                self.assertEqual(actual['suggestedPrompts'], ['Help with this skill'])
                continue
            self.assertEqual([p['name'] for p in actual['plugins']], ['first', 'second'])
        self.assertEqual(json.loads((self.root / 'plugins/first/plugin.json').read_text())['version'], '1.0.0')
        self.assertEqual(json.loads((self.root / 'plugins/second/plugin.json').read_text())['version'], '2.3.4')

    def test_local_tool_folders_are_skipped_even_with_symlinks(self):
        venv = self.root / 'plugins/first/scripts/.venv/bin'
        venv.mkdir(parents=True)
        (venv / 'python').symlink_to('/usr/bin/python3')
        (self.root / 'plugins/first/scripts/.pytest_cache').mkdir()
        (self.root / 'plugins/first/scripts/.pytest_cache/v').write_text('x')
        (self.root / 'plugins/first/scripts/tool.py').write_text('print(1)')
        self.save()
        files = catalogs.render(self.root)['release.json']['plugins']['first']['files']
        self.assertIn('scripts/tool.py', files)
        self.assertFalse([f for f in files if '.venv' in f or '.pytest_cache' in f])

    def test_os_metadata_files_are_not_released(self):
        (self.root / 'plugins/first/.DS_Store').write_bytes(b'junk')
        (self.root / 'plugins/first/README.md').write_text('readme')
        self.save()
        files = catalogs.render(self.root)['release.json']['plugins']['first']['files']
        self.assertIn('README.md', files)
        self.assertNotIn('.DS_Store', files)

    def test_check_is_read_only_and_detects_changed_description(self):
        catalogs.build(self.root)
        path = self.root / 'plugins/first/plugin.json'
        data = json.loads(path.read_text()); data['description'] = 'Changed'; path.write_text(json.dumps(data))
        before = (self.root / '.claude-plugin/marketplace.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'regeneration'):
            catalogs.build(self.root, check=True)
        self.assertEqual((self.root / '.claude-plugin/marketplace.json').read_bytes(), before)

    def test_duplicate_identity_rejected_before_output(self):
        self.registry['plugins'].append(dict(self.registry['plugins'][0])); self.save()
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            catalogs.build(self.root)
        self.assertFalse((self.root / '.claude-plugin').exists())

    def test_claude_only_identity_preserves_other_hosts_and_distribution(self):
        self.registry['plugins'][0]['claudeName'] = 'example-first'
        self.save()
        path = self.root / 'plugins/first/.claude-plugin/plugin.json'
        data = json.loads(path.read_text()); data['name'] = 'example-first'
        path.write_text(json.dumps(data))
        outputs = catalogs.render(self.root)
        self.assertEqual(outputs['.claude-plugin/marketplace.json']['plugins'][0]['name'], 'example-first')
        self.assertEqual(outputs['.cursor-plugin/marketplace.json']['plugins'][0]['name'], 'first')
        self.assertIn('first', outputs['release.json']['plugins'])
        self.assertEqual(outputs['plugins/first/.antigravity-plugin/plugin.json']['name'], 'first')

    def test_duplicate_claude_identity_rejected(self):
        self.add_plugin('second', '1.0.0')
        self.registry['plugins'][1]['claudeName'] = 'first'; self.save()
        with self.assertRaisesRegex(ValueError, 'duplicate Claude'):
            catalogs.render(self.root)

    def test_missing_and_escaping_logo_rejected_before_writes(self):
        path = self.root / 'plugins/first/plugin.json'
        data = json.loads(path.read_text())
        for logo in ('./assets/missing.svg', '../../../outside.svg', '/outside.svg'):
            with self.subTest(logo=logo):
                data['extensions']['com.openai']['interface']['logo'] = logo
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'logo'):
                    catalogs.build(self.root)
                self.assertFalse((self.root / 'release.json').exists())

    def test_antigravity_truncated_skill_rejected_before_writes(self):
        skill = self.root / 'plugins/first/skills/first/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('---\nname: first\ndescription: Test\n---\n' + 'x' * 24001)
        with self.assertRaisesRegex(ValueError, '24,000'):
            catalogs.build(self.root)
        self.assertFalse((self.root / 'release.json').exists())

    def test_traversal_rejected(self):
        self.registry['plugins'][0]['path'] = './../outside'; self.save()
        with self.assertRaisesRegex(ValueError, 'inside'):
            catalogs.build(self.root)

    def test_mismatched_manifest_name_rejected(self):
        path = self.root / 'plugins/first/plugin.json'
        data = json.loads(path.read_text()); data['name'] = 'other'; path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'inconsistent'):
            catalogs.build(self.root)

    def test_native_version_drift_rejected(self):
        path = self.root / 'plugins/first/.claude-plugin/plugin.json'
        data = json.loads(path.read_text()); data['version'] = '9.0.0'; path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Compatibility'):
            catalogs.build(self.root)

    def test_cursor_identity_omits_url_without_changing_other_hosts(self):
        author = {'name': 'Example author', 'url': 'https://example.com'}
        self.registry['publisher'] = author
        self.save()
        for relative in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            path = self.root / 'plugins/first' / relative
            data = json.loads(path.read_text()); data['author'] = author
            path.write_text(json.dumps(data))
        outputs = catalogs.render(self.root)
        self.assertEqual(outputs['.cursor-plugin/marketplace.json']['owner'], {'name': 'Example author'})
        self.assertEqual(outputs['.claude-plugin/marketplace.json']['owner'], author)

    def test_cursor_author_name_drift_still_rejected(self):
        path = self.root / 'plugins/first/.cursor-plugin/plugin.json'
        data = json.loads(path.read_text()); data['author']['name'] = 'Different author'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Compatibility'):
            catalogs.build(self.root)

    def test_missing_terms_rejected_before_catalog_writes(self):
        for relative in ('plugin.json', '.codex-plugin/plugin.json'):
            with self.subTest(relative=relative):
                path = self.root / 'plugins/first' / relative
                original = path.read_text()
                data = json.loads(original)
                interface = (data['extensions']['com.openai']['interface']
                             if relative == 'plugin.json' else data['interface'])
                del interface['termsOfServiceURL']
                path.write_text(json.dumps(data))
                try:
                    with self.assertRaisesRegex(ValueError, 'Terms of service'):
                        catalogs.build(self.root)
                    self.assertFalse((self.root / 'release.json').exists())
                finally:
                    path.write_text(original)

    def test_invalid_terms_urls_rejected(self):
        path = self.root / 'plugins/first/plugin.json'
        data = json.loads(path.read_text())
        for value in ('', None, 42, 'http://example.com/terms', 'javascript:alert(1)',
                      'https:///terms', 'https://user:secret@example.com/terms',
                      'https://example.com/terms with spaces'):
            with self.subTest(value=value):
                data['extensions']['com.openai']['interface']['termsOfServiceURL'] = value
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'Terms of service'):
                    catalogs.render(self.root)

    def test_terms_match_native_fallback(self):
        path = self.root / 'plugins/first/.codex-plugin/plugin.json'
        data = json.loads(path.read_text())
        data['interface']['termsOfServiceURL'] = 'https://example.com/different-terms'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Terms of service'):
            catalogs.render(self.root)

    def test_listing_text_submission_limits_rejected(self):
        path = self.root / 'plugins/first/plugin.json'
        original = path.read_text()
        for field, limit in (('displayName', 30), ('shortDescription', 30),
                             ('longDescription', 4000), ('developerName', 80)):
            with self.subTest(field=field):
                data = json.loads(original)
                data['extensions']['com.openai']['interface'][field] = 'x' * (limit + 1)
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'Listing ' + field):
                    catalogs.render(self.root)

    def test_required_listing_text_rejected(self):
        path = self.root / 'plugins/first/.codex-plugin/plugin.json'
        original = path.read_text()
        for value in ('', None, 42):
            with self.subTest(value=value):
                data = json.loads(original)
                data['interface']['shortDescription'] = value
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'Listing shortDescription'):
                    catalogs.render(self.root)

    def test_fallback_listing_copy_drift_rejected(self):
        path = self.root / 'plugins/first/.codex-plugin/plugin.json'
        original = path.read_text()
        for field in ('longDescription', 'category'):
            with self.subTest(field=field):
                data = json.loads(original)
                data['interface'][field] = 'Different skill'
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'Listing ' + field):
                    catalogs.render(self.root)


if __name__ == '__main__':
    unittest.main()
