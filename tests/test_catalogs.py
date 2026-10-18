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
        manifest = {'name': name, 'version': version, 'description': name, 'author': {'name': 'Example author'}}
        (directory / 'plugin.json').write_text(json.dumps(manifest))
        for host in ('claude', 'cursor', 'codex'):
            path = directory / f'.{host}-plugin/plugin.json'
            path.parent.mkdir(); path.write_text(json.dumps(manifest))
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
            self.assertEqual([p['name'] for p in actual['plugins']], ['first', 'second'])
        self.assertEqual(json.loads((self.root / 'plugins/first/plugin.json').read_text())['version'], '1.0.0')
        self.assertEqual(json.loads((self.root / 'plugins/second/plugin.json').read_text())['version'], '2.3.4')

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


if __name__ == '__main__':
    unittest.main()
