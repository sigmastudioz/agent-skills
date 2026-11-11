"""Expose the distributed media-in-3D adapter tests through the collection test gate."""
from pathlib import Path
import importlib.util
import sys
import unittest

scripts = Path(__file__).resolve().parents[1] / 'plugins/visualizer/skills/visualizer/scripts'
try:
    import numpy  # noqa: F401  (optional adapter dependencies)
    import PIL  # noqa: F401
except ImportError:
    raise unittest.SkipTest('numpy/Pillow not installed; see requirements-media-3d.txt')
# Register the adapter under its import name without putting scripts/ on sys.path,
# which would shadow same-named test modules in this folder.
_adapter = importlib.util.spec_from_file_location('media_in_3d', scripts / 'media_in_3d.py')
sys.modules['media_in_3d'] = importlib.util.module_from_spec(_adapter)
_adapter.loader.exec_module(sys.modules['media_in_3d'])
spec = importlib.util.spec_from_file_location('packaged_media_in_3d_tests', scripts / 'test_media_in_3d.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for _name in dir(module):
    _obj = getattr(module, _name)
    if isinstance(_obj, type) and issubclass(_obj, unittest.TestCase) and _obj is not unittest.TestCase:
        globals()[_name] = _obj
