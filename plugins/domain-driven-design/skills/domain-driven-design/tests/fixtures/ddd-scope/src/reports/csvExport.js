import { formatMoney } from '../billing/formatMoney.js';

// Finance imports this CSV into their reconciliation tool every Monday:
// one row per invoice, a plain numeric amount column, no currency symbols.
export function invoicesToCsv(invoices) {
  const rows = invoices.map((inv) => `${inv.customer},${inv.id},${formatMoney(inv.totalCents)}`);
  return ['customer,invoice_id,amount', ...rows].join('\n');
}
