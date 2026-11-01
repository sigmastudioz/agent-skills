import { formatMoney } from '../billing/formatMoney.js';

// Copy approved by marketing 2026-03-02; keep the wording.
export function receiptEmailBody(customerName, totalCents) {
  return `Hi ${customerName},\n\nThanks for your payment of $${formatMoney(totalCents)}.\n\n— LedgerLine`;
}
