"""Expose the distributed renderer regressions through the collection test gate."""
from pathlib import Path
import importlib.util

script = (Path(__file__).resolve().parents[1] / 'plugins/visualizer'
          / 'skills/visualizer/scripts/test_render.py')
spec = importlib.util.spec_from_file_location('packaged_renderer_tests', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ValidateTests = module.ValidateTests
SizeRuleTests = module.SizeRuleTests
CommandLineTests = module.CommandLineTests
