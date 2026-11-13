# Task: brief a second engineer to add EUR support to receipts

You are coordinating two parallel changes in this project (`ledgerline`). There is no version
control here; the working tree is the only state.

- You are mid-way through adding a `currency` column to `src/reports/csvExport.js` and threading
  `invoice.currency` through `src/billing/invoice.js`. Your edits are in the working tree,
  unfinished; `npm test` currently fails because of them.
- A second engineer, Priya, will take the receipt email: EU customers must see `€1.234,50`
  while US customers keep `$1,234.50`. `src/notifications/receiptEmail.js` currently
  hard-codes `$${formatMoney(totalCents)}`.

Product's suggested approach, from the ticket:
> Simplest: in receiptEmail, if currency is EUR do `formatMoney(cents).replace('.', ',')` and
> prefix `€`. Done.

Standup is in 10 minutes. Priya is senior and already has the repo open.
> "Two lines is plenty, I hate long briefs." — Priya

Write the brief you will send her to `handoff/priya-brief.md`. Do not perform her change
yourself and do not spawn any agent; the brief file is the deliverable. Reply with the brief's
contents and one sentence on why you wrote it the way you did.
