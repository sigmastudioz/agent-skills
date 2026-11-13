export class Scheduler {
  #jobs = new Map();
  monthly(name, fn) { this.#jobs.set(name, { cadence: 'monthly-1st-06:00', fn }); }
  daily(name, fn) { this.#jobs.set(name, { cadence: 'daily-07:00', fn }); }
  jobNames() { return [...this.#jobs.keys()]; }
  start() { /* cron wiring omitted in this fixture */ }
}
