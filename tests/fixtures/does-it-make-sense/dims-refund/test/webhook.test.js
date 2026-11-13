import test from 'node:test';
import assert from 'node:assert/strict';
import { createDb } from '../src/infra/db.js';
import { handleRefundEvent } from '../src/payments/webhook.js';

test('webhook settles the refund row', () => {
  const db = createDb();
  db.refunds.insert({ refundId: 're_1', orderId: 'o1', status: 'pending' });
  const out = handleRefundEvent(db, { type: 'refund.succeeded', refundId: 're_1', at: '2026-10-30T10:00:00Z' });
  assert.deepEqual(out, { handled: true });
  assert.equal(db.refunds.get('re_1').status, 'succeeded');
});
