import test from 'node:test';
import assert from 'node:assert/strict';
import { registerStatementJob } from '../src/statements/job.js';
import { Scheduler } from '../src/infra/scheduler.js';
import { Mailer } from '../src/email/mailer.js';

test('statement job emails every active customer once a month', async () => {
  const scheduler = new Scheduler();
  const mailer = new Mailer({ transport: 'none' });
  const customers = { async active() { return [{ id: 'c1', name: 'ACME', email: 'ap@acme.example' }]; } };
  const ledger = { async rowsFor() { return [{ date: '2026-10-03', description: 'Plan', cents: 123450 }]; } };
  registerStatementJob(scheduler, { customers, ledger, mailer, now: () => new Date('2026-11-01T06:00:00Z') });
  assert.deepEqual(scheduler.jobNames(), ['statements']);
  // run the registered job body directly
  const job = Object.getOwnPropertySymbols(scheduler).length ? null : null; // scheduler internals are private
  void job;
  // exercise through a second scheduler stub that captures the fn
  const captured = {};
  registerStatementJob({ monthly(name, fn) { captured[name] = fn; } }, { customers, ledger, mailer, now: () => new Date('2026-11-01T06:00:00Z') });
  await captured.statements();
  assert.equal(mailer.sent.length, 1);
  assert.equal(mailer.sent[0].to, 'ap@acme.example');
  assert.match(mailer.sent[0].subject, /2026-10 statement/);
});
