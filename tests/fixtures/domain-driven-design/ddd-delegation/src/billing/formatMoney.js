// Shared numeric money formatter. Integer cents in, fixed two-decimal string out.
export function formatMoney(cents) {
  if (!Number.isInteger(cents)) throw new TypeError('cents must be an integer');
  return (cents / 100).toFixed(2);
}
