"""Verify distributed runtime integrity and safe app-local staging contracts."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest

SKILL=Path(__file__).resolve().parents[1]/'plugins/ui-foundation-reuse/skills/ui-foundation-reuse'
NODE=shutil.which('node')

class RuntimeBundleTests(unittest.TestCase):
    def test_archive_integrity_and_exports_are_self_contained(self):
        meta=json.loads((SKILL/'assets/bundle.json').read_text())
        archive=SKILL/'assets'/meta['archive']
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),meta['sha256'])
        with tarfile.open(archive) as package:
            files={m.name:m for m in package.getmembers()}
            self.assertEqual(len(files),meta['fileCount'])
            self.assertTrue(all(m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts for m in files.values()))
            manifest=json.load(package.extractfile('package/package.json'))
            self.assertEqual((manifest['name'],manifest['version']),(meta['package'],meta['version']))
            def targets(value):
                if isinstance(value,str):yield value
                elif isinstance(value,dict):
                    for child in value.values():yield from targets(child)
            for target in targets(manifest['exports']):
                self.assertIn('package/'+target.removeprefix('./'),files,target)
            self.assertTrue(any(p.startswith('package/src/') for p in files))
            self.assertIn('package/LICENSE',files)

    @unittest.skipUnless(NODE,'Node is required for staging behavior')
    def test_staging_is_idempotent_and_preserves_app_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            app=Path(tmp); manifest=app/'package.json'; manifest.write_text('{"name":"isolated-test","private":true}\n')
            before=manifest.read_bytes()
            for _ in range(2):
                r=subprocess.run([NODE,str(SKILL/'scripts/stage-runtime.mjs'),str(app)],capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stderr)
                info=json.loads(r.stdout)
                staged=app/info['archive']
                self.assertEqual(hashlib.sha256(staged.read_bytes()).hexdigest(),info['sha256'])
            self.assertEqual(manifest.read_bytes(),before)
            self.assertFalse((app/'node_modules').exists())
            self.assertFalse((app/'package-lock.json').exists())

    @unittest.skipUnless(NODE,'Node is required for staging behavior')
    def test_conflicting_archive_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            app=Path(tmp); (app/'package.json').write_text('{}'); target=app/'vendor/ui-foundation/ui-foundation.tgz'
            target.parent.mkdir(parents=True);target.write_bytes(b'keep existing pinned runtime')
            r=subprocess.run([NODE,str(SKILL/'scripts/stage-runtime.mjs'),str(app)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertEqual(target.read_bytes(),b'keep existing pinned runtime')

    @unittest.skipUnless(NODE,'Node is required for staging behavior')
    def test_symlinked_vendor_does_not_write_outside_app(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);app=root/'app';outside=root/'outside';app.mkdir();outside.mkdir()
            (app/'package.json').write_text('{}');(app/'vendor').symlink_to(outside,target_is_directory=True)
            r=subprocess.run([NODE,str(SKILL/'scripts/stage-runtime.mjs'),str(app)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertEqual(list(outside.iterdir()),[])

if __name__=='__main__':unittest.main()
