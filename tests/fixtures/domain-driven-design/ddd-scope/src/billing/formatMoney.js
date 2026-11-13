// Shared numeric money formatter. Integer cents in, decimal string out.
export function formatMoney(cents) {
  if (!Number.isInteger(cents)) throw new TypeError('cents must be an integer');
  return String(cents / 100);
}
