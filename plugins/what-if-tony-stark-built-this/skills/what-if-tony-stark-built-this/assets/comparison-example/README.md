# Comparison example

Extreme-margin Manifest v1 experiment used by the skill comparison runner.

```bash
python3 ../../scripts/compare_designs.py experiment.json --output /tmp/stark-example-report.json
```

`base` sleeps briefly; `candidate` returns the same answer without that cost. This
demonstrates runner wiring only; it is not evidence of product efficacy.
