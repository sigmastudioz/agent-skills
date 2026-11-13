# Maintenance Window Planner

Operators need the first conflict for every pair of recurring maintenance windows in a requested
integer-time range. The small-input implementation is correct, but long-lived schedules exhaust
its expansion budget. Make the same public planner and CLI work for counts up to 10**12 without
enumerating occurrences. Use Python's standard library; approximate answers are not acceptable.
The encoded request remains small (at most 12 schedules). A local expansion-limit increase, more
workers or replacing exactness with sampling does not meet the goal.

## Contracts

`windows.model.Series(start, period, duration, count)` describes half-open windows
`[start + i*period, start + i*period + duration)` for integer indices `0 <= i < count`.
Start can be negative. Period is positive; `1 <= duration <= min(64, period)`; count is nonnegative.
Fields and query bounds must be integers (booleans are not accepted). Invalid inputs raise ValueError.
Python integer exactness is required. There is no infinite recurrence or wall-clock/timezone behavior.

`windows.engine.first_overlap(a, b, lower, upper)` returns the earliest integer tick in the intersection
of both series and `[lower, upper)`, or None. Touching endpoints do not overlap; `lower >= upper`
is invalid. `windows.planner.plan(request)` accepts `{"lower":0,"upper":100,"schedules":[
{"id":"a","start":0,"period":10,"duration":2,"count":10},
{"id":"b","start":1,"period":15,"duration":1,"count":5}]}` and returns
`{"conflicts":[{"left":"a","right":"b","at":1}]}`. IDs are unique nonempty strings.
Each unordered pair appears at most once, left/right are lexicographically ordered IDs, and rows
sort by `(at, left, right)`. An empty schedule list is valid. Do not mutate the request.

Run `python3 -m windows.cli request.json` to print that JSON result. Existing module names and public
interfaces remain supported. `Series.occurrences` is a bounded small-data preview utility, not a way
to increase the planner's supported scale. Preserve its limit behavior.

Run public checks with `python3 -m unittest discover -s tests -v`. Add appropriate checks and provide
a working implementation, evidence for exactness, and an explanation of what work no longer grows
with recurrence count. Check the real CLI as part of delivery. No deployment is requested.
