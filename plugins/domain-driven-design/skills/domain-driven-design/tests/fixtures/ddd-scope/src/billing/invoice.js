import { formatMoney } from './formatMoney.js';

export function renderInvoiceLines(invoice) {
  const lines = invoice.items.map((it) => `${it.description.padEnd(28)} ${formatMoney(it.cents)}`);
  const total = invoice.items.reduce((sum, it) => sum + it.cents, 0);
  lines.push(`${'TOTAL'.padEnd(28)} ${formatMoney(total)}`);
  return lines;
}
