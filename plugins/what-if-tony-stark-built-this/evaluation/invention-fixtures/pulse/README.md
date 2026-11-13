# Pulse Telemetry Analyzer

Telemetry recipes encode sample blocks, concatenation, and repetition. Our analyzer and report CLI
work on small recipes but expand the entire stream. Make exact analysis and the report work when a
small recipe denotes trillions of samples. Work and storage must depend on the encoded recipe and
integer sizes, not on the expanded stream length. No sampling, approximation or new dependency.
Raising the preview expansion budget does not solve the product requirement.

## Contracts

A program is exactly one of:
- `{"values":[3,-2,5]}`: a block of integers (not booleans), including an empty block;
- `{"concat":[PROGRAM,...]}`: ordered concatenation, including an empty list;
- `{"repeat":COUNT,"body":PROGRAM}`: COUNT copies, COUNT a nonnegative integer, not bool.

Nesting depth is at most 64 and input is a JSON tree. Invalid programs raise ValueError, including
an invalid body of a zero repetition. Counts up to 10**12 per repeat are normal; nested repeats can
represent still larger streams. Negative and arbitrary-precision sample values are valid.

`pulse.engine.analyze(program)` returns these exact fields:
`count`, `sum`, `first`, `last`, `minimum`, `maximum`, `drawdown`, `rise`.
Drawdown is `max(0, sample[i]-sample[j])` for `i <= j` in chronological order.
Rise is the largest number of samples in a contiguous strictly increasing run. A single sample
has rise 1; equality breaks a rise. Empty streams have count/sum/drawdown/rise 0 and the other four
fields None. Do not change the program or trade integer exactness for floating point.

`pulse.report.build(program)` returns `{"metrics":analyze(program),"preview":[...]}` where preview
is the first at most eight samples in order. Both metrics and preview must work at the target scale,
including empty repeated bodies. Run `python3 -m pulse.cli recipe.json` to print this report as JSON.
Keep existing public module names and interfaces. `pulse.recipe.expand(program, limit=10000)` is a
bounded preview/reference helper whose limit remains enforced; it is not the production scale API.

Run checks with `python3 -m unittest discover -s tests -v`. Add useful regressions and demonstrate
why the new mechanism removes expansion while preserving chronological semantics. Check the actual
report/CLI consumer. No deployment is requested.
