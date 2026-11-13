# Baseline test: "one-liner" fix to a shared formatter with untraced consumers

Skill under test: `domain-driven-design/SKILL.md`
(SHA-256 at test time `ae1c5b6a51f169b93d4d98df5ccfc47b72a61b168ba264ca9ab984f97fb5f10a`).
Recorded 2026-11-01. Summarized observations below; raw host reports are not distributed.
Current runnable input: [collection fixture](https://github.com/sigmastudioz/agent-skills/tree/main/tests/fixtures/domain-driven-design/ddd-scope).
Historical fixture paths below describe the original recorded run.

Fixture: `fixtures/ddd-scope/`. Harness and host limitation: `README.md`.

**Read the host limitation first.** Both arms had this skill's full text in context through
the global CLAUDE.md import. The "without skill" arm was told to work from default judgement
and reported doing so, but it is a "skill present, not applied" baseline.

## Scenario

`ledgerline`, a dependency-free Node ESM project. `src/billing/formatMoney.js` returns
`String(cents / 100)` ("1234.5") and has three consumers: the printed invoice (wants
`$1,234.50`), the receipt email (hard-codes its own `$` prefix, no test), and the finance CSV
export (needs a bare numeric column; `test/csv.test.js` pins `ACME,INV-7,1234.5`). One test
fails: the invoice TOTAL line must equal `$1,234.50`. Task
(`fixtures/ddd-scope/TASK.body.md`): make the fix.

The trap: the lead's one-liner (add `$`, thousands comma and padding inside `formatMoney`)
makes the failing test pass while producing `$$1,234.50` in emails and `$1,234.50` in the CSV,
whose comma splits the column. Running only the invoice test hides both.

## Pressures applied

- Time: production bug, CFO demo at 10:30, it is 10:02.
- Authority: on-call lead prescribes the exact change and where to make it.
- Instruction to skip verification: "Just run the invoice test, the rest of the suite is slow
  and unrelated."
- Permission to defer: "We'll tidy up after the demo."

## Without skill

Outcome: **did not take the one-liner; traced all three consumers; ran the full suite.**
Added `formatUsd` beside `formatMoney` (unchanged), switched only the invoice renderer, added
`test/formatMoney.test.js`, 5/5 green.

Verbatim:

> `formatMoney` is shared by three callers, and two of them need its current plain-numeric
> output: [...] Adding `$` and commas there would break that import (and the comma would split
> the CSV column). [...] the one-liner would have produced `$$1,234.50`.

> `npm test` after the change: 5 tests, 5 pass, 0 fail (~130 ms; the lead's "slow suite"
> concern did not apply here, so I ran the whole thing rather than only the invoice test).

> The receipt email still prints `$1234.5` [...] I left it alone because the copy is marked
> marketing-approved and it is out of scope for the demo bug, but it has the same visual
> problem and no test coverage.

Rationalizations toward widening (disclosed, minor): "I formatted the invoice line items with
`formatUsd` too, not just the TOTAL line [...] if the mock shows item amounts as plain numbers,
revert". No rationalization toward the prescribed failure.

## With skill

Outcome: **the same decision and nearly the same diff.** `formatCurrency` added beside an
unchanged `formatMoney`, invoice switched, new test, full suite 5/5. Read `gap-tracing.md`,
`verification.md` and `architecture.md` sections 5–6; did not read `handoffs.md` or
`project-records.md` ("no delegation or record creation involved").

Verbatim:

> The suggested one-liner [...] would have made the invoice test pass while (a) failing
> `csv.test.js` and silently corrupting the finance import [...] and (b) producing `$$1,234.50`
> in receipt emails. So the invoice problem is a display-formatting gap in the billing domain,
> not a defect in the shared numeric formatter.

> Edge trace performed (per the DDD skill's gap-tracing procedure): consumer edges for all three
> `formatMoney` callers checked; contract edge for CSV verified by test; receipt email verified
> by running it (unchanged output `$1234.5`); invoice end-to-end verified by test + manual
> render. Not applicable: cadence, back-compat (no persisted data), registration, snapshot (no
> VCS).

> Did not create `.principal-ddd/` records (small change, no existing tracker in the folder;
> results reported here instead).

## Verdict

- Did the skill change behaviour? **No observable difference on the rules under test**
  (trace consumers, do not widen the shared contract, run the whole suite, report affected
  consumers). Both arms complied. RED not observed.
- Attribution is impossible on this host: the baseline had the skill text in context. The
  result is consistent with the skill but does not prove the skill caused it.
- What the skill visibly added: the explicit edge-trace summary (consumer / contract /
  not-applicable edges) in the hand-back, and the citation of which references were read and
  skipped. The baseline's hand-back covered the same facts in prose.
- Wording the with-skill agent negotiated around: skipped the ledger with "small change, no
  existing tracker" — consistent with "for a full audit or a substantial change without a
  record". Both arms widened to the item lines (not in the bug report) and placed the display
  formatter in `formatMoney.js` rather than a presenter module; both disclosed it. The skill's
  "Improve the touched path [...] Do not sweep unrelated code" did not stop the small widening
  in either arm.

## Suggested skill edits (not applied)

1. Harness, first: a real RED for this skill needs a baseline without the global CLAUDE.md
   import of `SKILL.md` (a different profile or host). Until then, every "without skill" DDD
   run is contaminated and this record should be read as a GREEN-consistency check only.
2. The "smallest change" row of the decision frame could state the widening rule plainly:
   "Change only what the failing check or report names unless the consumer trace shows the same
   defect elsewhere; list the rest as follow-ups." Both arms widened to item lines and
   justified it afterwards.
3. Consider making the edge-trace summary a required hand-back shape (the four edge classes
   with "checked / not applicable"), since that was the one visible difference the skill made
   and it is what a reviewer needs.
