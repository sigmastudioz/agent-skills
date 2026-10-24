"""Run the packaged guard regressions through the repository test entrypoint."""
from pathlib import Path
import importlib.util
import unittest

script = (Path(__file__).resolve().parents[1] / 'plugins/domain-driven-design'
          / 'skills/domain-driven-design/scripts/test_guard_handoff.py')
spec = importlib.util.spec_from_file_location('packaged_handoff_guard_tests', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
HandoffGuardTests = module.HandoffGuardTests

if __name__ == '__main__':
    unittest.main()
