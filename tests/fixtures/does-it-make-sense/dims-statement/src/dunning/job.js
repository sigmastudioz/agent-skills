export function registerDunningJob(scheduler, { customers, mailer }) {
  scheduler.daily('dunning', async () => {
    for (const c of await customers.active()) {
      if (c.overdueCents > 0) await mailer.send({ to: c.email, subject: 'Payment overdue', text: 'Please pay.' });
    }
  });
}
