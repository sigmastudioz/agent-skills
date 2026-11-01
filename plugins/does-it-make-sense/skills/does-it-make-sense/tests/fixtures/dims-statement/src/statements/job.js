import { buildStatement } from './generate.js';

export function registerStatementJob(scheduler, { customers, ledger, mailer, now = () => new Date() }) {
  scheduler.monthly('statements', async () => {
    const d = now();
    const period = `${d.getUTCFullYear()}-${String(d.getUTCMonth()).padStart(2, '0')}`; // previous month
    for (const c of await customers.active()) {
      const statement = buildStatement(c, await ledger.rowsFor(c.id, period), period);
      await mailer.send({
        to: c.email,
        subject: `Your ${period} statement`,
        text: `Hi ${c.name}, your statement for ${period} is attached. Total: ${(statement.totalCents / 100).toFixed(2)}.`,
      });
    }
  });
}
