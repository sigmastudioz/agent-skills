export function describeOrder(db, orderId) {
  const order = db.orders.get(orderId);
  if (!order) return `order ${orderId}: not found`;
  return `order ${orderId}: ${order.status} | refund: ${order.refund_status ?? 'none'}`;
}
