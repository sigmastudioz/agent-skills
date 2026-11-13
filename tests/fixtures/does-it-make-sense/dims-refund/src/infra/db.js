// Minimal in-memory store standing in for Postgres in this fixture.
export function createDb() {
  const orders = new Map([['o1', { id: 'o1', status: 'paid', paymentId: 'pay_1', refund_status: null }]]);
  const refunds = new Map();
  return {
    orders: {
      get: (id) => orders.get(id),
      update: (id, patch) => orders.set(id, { ...orders.get(id), ...patch }),
      list: () => [...orders.values()],
    },
    refunds: {
      insert: (row) => refunds.set(row.refundId, row),
      update: (refundId, patch) => refunds.set(refundId, { ...refunds.get(refundId), ...patch }),
      byOrder: (orderId) => [...refunds.values()].filter((r) => r.orderId === orderId),
      get: (refundId) => refunds.get(refundId),
    },
  };
}
