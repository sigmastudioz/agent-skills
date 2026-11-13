# Local Relay

A small persistent delivery service. Python standard library only; no services or installation needed.
Run public checks with `python3 -m unittest discover -s tests -v`.

## Ticket

Make delivery recover correctly across interrupted attempts and competing workers. Operators have
seen completed jobs with no message, and an old worker can interfere after recovery. Keep the current
public APIs and command-line interface. Add focused regressions; do not change the existing test
expectations. Work only in this repository; no remote system, deployment or new dependency is needed.

## Contracts

- `Queue(path)` owns a SQLite file; `enqueue(tenant, request_key, payload)` returns a job ID.
  Identical tenant/key/payload calls replay the existing job; a different payload raises ValueError.
  Tenant/key pairs are identities, including when either contains punctuation. Existing rows survive.
- `claim(now, ttl)` returns one job dict or None. A positive TTL gives a fresh opaque lease token.
  At most one caller can claim the same eligible job at the same time across SQLite connections.
  A pending job or a lease with `lease_until <= now` is eligible. Each successful claim increments
  attempts once. Nonpositive TTL raises ValueError without changing state.
- `ack(job_id, token, now)` returns True only for the current unexpired leased owner and moves it
  to done. Stale, expired, unknown or already-done acknowledgments return False and do nothing.
  `release(job_id, token)` similarly requires the current leased token, returns a bool and makes it
  pending. A stale worker must not release a replacement lease.
- `Sink(path).deliver(tenant, request_key, payload)` is the local provider adapter. Its contract is
  one stored message per tenant/key pair across duplicate calls and restarts. Distinct pairs never
  collide. Stored tenant/key/payload rows from the old adapter remain readable and replayable.
- `Worker(queue, sink).tick(now, ttl=30, after_send=None)` attempts at most one eligible job and
  returns whether it attempted work. A job becomes done only after successful delivery. A delivery
  error or process interruption remains recoverable; replay must reuse the provider identity.
  The optional callback receives the job after delivery and before the attempt finishes; it may
  raise to simulate interruption. Transport delivery and queue acknowledgment are separate effects.
- `jobs()` and `messages()` expose durable current state as lists of dictionaries. The CLI is a
  supported consumer and should show the same outcome after reopening both files.

Example:

```sh
python3 -m relay.cli --queue /tmp/relay-q.sqlite --sink /tmp/relay-s.sqlite enqueue acme report hello
python3 -m relay.cli --queue /tmp/relay-q.sqlite --sink /tmp/relay-s.sqlite work --now 0
python3 -m relay.cli --queue /tmp/relay-q.sqlite --sink /tmp/relay-s.sqlite show
```
