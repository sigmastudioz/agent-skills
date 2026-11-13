import { formatMoney } from './formatMoney.js';

// Presentation for the printed invoice (US customers only, for now).
function formatUsd(cents) {
  const [whole, frac] = formatMoney(cents).split('.');
  return `$${whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}.${frac}`;
}

export function renderInvoiceLines(invoice) {
  // WIP (coordinator): currency column — `invoice.currency` is not yet threaded through.
  const lines = invoice.items.map((it) => `${it.description.padEnd(28)} ${formatUsd(it.cents)}`);
  const total = invoice.items.reduce((sum, it) => sum + it.cents, 0);
  lines.push(`${'TOTAL'.padEnd(28)} ${formatUsd(total)}`);
  return lines;
}
