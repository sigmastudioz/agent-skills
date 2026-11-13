export async function cancelOrder(db, payments, orderId) {
  const order = db.orders.get(orderId);
  if (!order) throw new Error(`unknown order ${orderId}`);
  if (order.status !== 'paid') throw new Error(`order ${orderId} is ${order.status}, cannot cancel`);
  db.orders.update(orderId, { status: 'cancelled' });
  const { refundId, status } = await payments.refund(order.paymentId); // provider answers 'pending'
  db.refunds.insert({ refundId, orderId, status, requestedAt: new Date().toISOString() });
  return { orderId, refundId, status };
}
