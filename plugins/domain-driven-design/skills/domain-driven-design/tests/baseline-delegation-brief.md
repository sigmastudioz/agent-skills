# Baseline test: delegation brief under "two lines is plenty" pressure

Skill under test: `domain-driven-design/SKILL.md` and `references/handoffs.md`
(SKILL.md SHA-256 at test time `ae1c5b6a51f169b93d4d98df5ccfc47b72a61b168ba264ca9ab984f97fb5f10a`).
Recorded 2026-11-01. Summarized observations below; raw host reports are not distributed.
Fixture: `fixtures/ddd-delegation/`. Harness and host limitation: `README.md`.

**Read the host limitation first.** Both arms had this skill's full text (including the
handoff-contract table) in context through the global CLAUDE.md import.

## Scenario

`ledgerline` at a later state: `formatMoney` now returns two decimals; the coordinator's own
unfinished edits (a `currency` column in `csvExport.js` and `invoice.js`) make
`test/csv.test.js` fail; there is no version control. A second engineer, Priya, must add EUR
receipts (`€1.234,50`) while US keeps `$1,234.50`. The product ticket proposes
`formatMoney(cents).replace('.', ',')` with a `€` prefix, which cannot produce the thousands
separator. Task (`fixtures/ddd-delegation/TASK.body.md`): write the brief to
`handoff/priya-brief.md`; do not implement; do not spawn an agent.

The deliverable is a file, so the host's `HANDOFF_JSON=` guard is not involved; what is
tested is whether the agent carries the contract fields (goal and limits, location and
revision, ownership, interfaces, current state, evidence and checks, next action and return
format) and whether it verifies the proposed algorithm against the acceptance string.

## Pressures applied

- Social: "Two lines is plenty, I hate long briefs." from a senior engineer.
- Time: standup in 10 minutes.
- Authority: product's "Simplest: ... Done." algorithm.
- Concurrency and fragility: unversioned working tree with the coordinator's half-done edits
  and a red test that is not Priya's fault.

## Without skill

Outcome: **a structured brief, not two lines.** Covered goal, the flawed algorithm (verified
by running `Intl.NumberFormat` and the `.replace` variant), a suggested shape, file ownership
for both engineers, the no-VCS warning and the red-test state.

Verbatim (brief excerpts):

> **Don't use the ticket's two-liner.** `formatMoney(123450)` is `1234.50`, so
> `.replace('.', ',')` gives `€1234,50` — no thousands separator. And don't "fix" it inside
> `formatMoney.js`: `csvExport.js` relies on that raw numeric output for finance's Monday
> reconciliation import.

> **Ownership while we're both in the tree (no VCS — don't revert or reformat anything you
> didn't write):** Yours: `receiptEmail.js`, new `formatCurrency.js`, new `test/receipt.test.js`
> [...] Mine, in flight: `invoice.js`, `csvExport.js`, their tests. [...] Nobody touches
> `formatMoney.js`.

> **Tests:** `npm test` is red right now from *my* csv WIP [...] — not yours, ignore it.

Verbatim (why):

> Priya wanted two lines, but two lines can't carry the three things she can't see from her
> editor and that would cost her real time [...] so I kept it to those facts plus a suggested
> (not mandated) shape, and left every implementation decision to her.

Missing against the contract table: no acceptance checks as a list, no return format
("report changed paths, contract changes, checks, gaps, remaining"), no revision substitute
for the unversioned tree, no pointer to the engineering baseline. The agent said the
ownership/evidence content "comes from the task's own facts [...] not from that document's
field list".

## With skill

Outcome: **all seven contract fields present, in 38 lines.** Read `SKILL.md`, `handoffs.md`,
`architecture.md` sections 2, 5, 6, 10, `gap-tracing.md`, `verification.md`,
`project-records.md`. Hashed the four source files before and after to prove the brief was
the only write.

Verbatim (brief excerpts):

> **You own:** `src/notifications/receiptEmail.js`, a new `src/billing/formatCurrency.js`
> (name yours), a new `test/receipt.test.js`. **Hands off:** `src/billing/formatMoney.js` [...]
> `src/billing/invoice.js` and `src/reports/csvExport.js` are my in-flight edits (no VCS here —
> the working tree is the only copy, so nothing to revert to; their current sha256 prefixes
> are `959a56322b32` and `01536dae8c4a`).

> **State and checks.** `npm test` fails on `test/csv.test.js` — that is my WIP and expected.
> `node --test test/receipt.test.js` runs only yours (Node 24). Before standup: `123450` as
> USD → `$1,234.50`, EUR → `€1.234,50`, no currency → USD, unsupported code throws;
> `test/invoice.test.js` must stay green.

> **Return:** changed paths, the export name and signature, the test command and result,
> anything you could not verify.

> Workspace: this folder (`ledgerline`, no VCS). Conventions applied above come from
> `domain-driven-design/SKILL.md` (ownership, contracts, handoff); ask me if you want the file.

Verbatim (why):

> the seven handoff-contract fields from the DDD skill compressed into 38 lines with no
> headings to skim past.

It also noted, correctly, that `HANDOFF_JSON=` applies to agent/session tools, not to a
Markdown brief for a human, and embedded the fields in prose instead.

## Verdict

- Did the skill change behaviour? **Partially.** Both arms refused the two-line brief and
  caught the flawed algorithm, so the headline RED (a context-free two-liner) was not
  observed. The skill's visible effect is completeness: the with-skill brief adds acceptance
  checks, a return format, a revision substitute (content hashes), the exact single-file test
  command and the baseline pointer, all of which the baseline omitted. Roughly five of seven
  contract fields without the skill, seven of seven with it.
- Attribution caveat: the baseline had the contract table in context and declined to use it;
  its brief still converged on ownership and state because the fixture made those facts
  salient. The fields it dropped (evidence, return, revision) are the ones the fixture did not
  force, which is where the skill text did its work.
- Wording the with-skill agent negotiated around: none against the contract. One factual slip
  worth noting for "Delegate verified invariants": the brief says `Intl.NumberFormat` "misses
  it too", having tested only currency-style output (`1.234,50 €`), while the baseline showed
  the decimal style with two fraction digits yields exactly `1.234,50`. The skill asks for
  verified claims; the verification here was incomplete, and the brief steers Priya to
  hand-roll on a wrong premise.

## Suggested skill edits (not applied)

1. In `handoffs.md`, state that the contract table applies to briefs for humans as well as to
   agent assignments (the with-skill agent inferred it; the baseline treated it as an agent
   field list it could set aside).
2. Add to "Delegate verified invariants": "state the exact command that produced the evidence
   for any claim about library or runtime behaviour in the brief", so a reviewer can catch a
   claim verified with the wrong options.
3. Harness: a cleaner RED needs a baseline without the CLAUDE.md import. Also consider adding
   an explicit "the worker is a subagent" variant so the `HANDOFF_JSON=` path is exercised and
   the guard's own messages can be captured.
