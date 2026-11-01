import { formatMoney } from '../billing/formatMoney.js';

// Finance imports this CSV into their reconciliation tool every Monday:
// one row per invoice, a plain numeric amount column, no currency symbols.
// WIP (coordinator): adding a `currency` column; header done, rows not yet.
export function invoicesToCsv(invoices) {
  const rows = invoices.map((inv) => `${inv.customer},${inv.id},${formatMoney(inv.totalCents)}`);
  return ['customer,invoice_id,amount,currency', ...rows].join('\n');
}
