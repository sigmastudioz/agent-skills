import { Scheduler } from './infra/scheduler.js';
import { Mailer } from './email/mailer.js';
import { registerDunningJob } from './dunning/job.js';
import { customers, ledger } from './infra/db.js';

const scheduler = new Scheduler();
const mailer = new Mailer({ transport: process.env.MAIL_TRANSPORT ?? 'log' });

registerDunningJob(scheduler, { customers, mailer });

scheduler.start();
console.log('northwind-billing started; jobs:', scheduler.jobNames());
