import test from 'node:test';
import assert from 'node:assert/strict';
import { invoicesToCsv } from '../src/reports/csvExport.js';

test('csv export keeps a plain numeric amount column', () => {
  const csv = invoicesToCsv([{ customer: 'ACME', id: 'INV-7', totalCents: 123450 }]);
  assert.equal(csv.split('\n')[1], 'ACME,INV-7,1234.5');
});
