"""Run the separately distributed records budget regressions through the collection gate."""
from pathlib import Path
import importlib.util
import unittest

script = Path(__file__).resolve().parents[1] / 'tools/records-budget/test_check_records.py'
spec = importlib.util.spec_from_file_location('packaged_records_budget_tests', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
RecordsBudgetTests = module.RecordsBudgetTests

if __name__ == '__main__':
    unittest.main()
