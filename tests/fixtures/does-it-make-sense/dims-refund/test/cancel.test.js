import test from 'node:test';
import assert from 'node:assert/strict';
import { createDb } from '../src/infra/db.js';
import { cancelOrder } from '../src/orders/cancel.js';

test('cancel marks the order cancelled and requests a refund', async () => {
  const db = createDb();
  const payments = { async refund() { return { refundId: 're_1', status: 'pending' }; } };
  const result = await cancelOrder(db, payments, 'o1');
  assert.equal(db.orders.get('o1').status, 'cancelled');
  assert.deepEqual(result, { orderId: 'o1', refundId: 're_1', status: 'pending' });
  assert.equal(db.refunds.byOrder('o1')[0].status, 'pending');
});
