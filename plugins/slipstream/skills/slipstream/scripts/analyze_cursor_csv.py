#!/usr/bin/env python3
"""Cursor keeps no real token usage locally (its tokenCount fields are zero). Export usage
from your Cursor account's usage page as CSV, then: python3 analyze_cursor_csv.py usage.csv
Column names are matched loosely (input / cache read / cache write / output / total / model / date)."""
import csv, sys
from collections import defaultdict


def col(h, *keys, exclude=()):
    for i, name in enumerate(h):
        n = name.lower()
        if all(k in n for k in keys) and not any(x in n for x in exclude):
            return i
    return None


def num(v):
    try:
        return float(str(v).replace(",", "").strip() or 0)
    except ValueError:
        return 0.0


rows = list(csv.reader(open(sys.argv[1], newline="", encoding="utf-8-sig")))
h, data = rows[0], rows[1:]
# Per Cursor's export (export-usage-events-csv?strategy=tokens) the input columns are disjoint:
# "Input (w/o Cache Write)" = plain input, "Input (w/ Cache Write)" = cache-write tokens.
ci = {"input": col(h, "input", "w/o") if col(h, "input", "w/o") is not None else col(h, "input", exclude=("cache",)),
      "cache_write": col(h, "input", "w/ cache") if col(h, "input", "w/ cache") is not None else col(h, "cache", "write"),
      "cache_read": col(h, "cache", "read"), "output": col(h, "output"), "total": col(h, "total"),
      "model": col(h, "model"), "date": col(h, "date")}
tot, by_model, days = defaultdict(float), defaultdict(float), set()
for r in data:
    for k in ("input", "cache_read", "cache_write", "output", "total"):
        if ci[k] is not None and ci[k] < len(r):
            tot[k] += num(r[ci[k]])
    if ci["model"] is not None:
        by_model[r[ci["model"]]] += num(r[ci["total"]]) if ci["total"] is not None else 0
    if ci["date"] is not None:
        days.add(r[ci["date"]][:10])
inp = tot["input"] + tot["cache_read"] + tot["cache_write"]
print(f"requests: {len(data)} over {len(days)} days; columns used: { {k: h[v] for k, v in ci.items() if v is not None} }")
print(f"input-side tokens: {inp:,.0f} (cache read {tot['cache_read']:,.0f}); output: {tot['output']:,.0f}; "
      f"input per output: {inp / max(tot['output'], 1):,.0f}:1")
print(f"avg input per request: {inp / max(len(data), 1):,.0f}  <- this is the per-call context; shrink it")
for m, v in sorted(by_model.items(), key=lambda x: -x[1])[:6]:
    print(f"  {m}: {v:,.0f} tokens")
