// Provider webhook: refund.succeeded / refund.failed, delivered asynchronously (minutes to days).
export function handleRefundEvent(db, event) {
  const refund = db.refunds.get(event.refundId);
  if (!refund) return { handled: false, reason: 'unknown refund' };
  db.refunds.update(event.refundId, { status: event.type === 'refund.succeeded' ? 'succeeded' : 'failed', settledAt: event.at });
  return { handled: true };
}
