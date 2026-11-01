import test from 'node:test';
import assert from 'node:assert/strict';
import { buildStatement } from '../src/statements/generate.js';

test('statement totals and csv header', () => {
  const st = buildStatement({ id: 'c1' }, [{ date: '2026-10-03', description: 'Plan', cents: 123450 }], '2026-10');
  assert.equal(st.totalCents, 123450);
  assert.equal(st.csv.split('\n')[0], 'date,description,amount');
  assert.equal(st.csv.split('\n')[1], '2026-10-03,Plan,1234.50');
});
