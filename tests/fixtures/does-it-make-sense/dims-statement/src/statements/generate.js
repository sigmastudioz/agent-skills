export function buildStatement(customer, rows, period) {
  const lines = rows.map((r) => ({ ...r, amount: (r.cents / 100).toFixed(2) }));
  const totalCents = rows.reduce((s, r) => s + r.cents, 0);
  const csv = ['date,description,amount', ...lines.map((l) => `${l.date},${l.description},${l.amount}`)].join('\n');
  return { customerId: customer.id, period, lines, totalCents, csv };
}
