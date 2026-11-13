import test from 'node:test';
import assert from 'node:assert/strict';
import { renderInvoiceLines } from '../src/billing/invoice.js';

test('invoice total matches the approved mock', () => {
  const lines = renderInvoiceLines({ items: [{ description: 'Baltic corridor plan', cents: 123450 }] });
  assert.equal(lines.at(-1), `${'TOTAL'.padEnd(28)} $1,234.50`);
});
