# 00 — Performance Budget

## Purpose
Define explicit timing budgets for each pipeline stage so the system meets its
intraday decision deadlines — and can prove it.

## Reference budgets (1m strategy, moderate hardware)
| Stage | Budget |
|---|---|
| Feed → validated bar | ≤ 250 ms |
| Features + indicators (incremental) | ≤ 20 ms / symbol |
| Strategy decide() | ≤ 10 ms |
| Risk gate | ≤ 5 ms |
| OMS place (adapter round-trip) | ≤ 250 ms |
| End-to-end bar→order decision | ≤ 500 ms |
Roughly 10× headroom vs typical needs — latency is predictable, not tight.

## Why budgets matter
- Strategy logic must never be the bottleneck: a missed bar = missed signal
  = silent strategy degradation (drift, CH_16/03).
- Slippage grows with reaction time; keep the gap between bar close and order
  send small and *measured*.

## Instrumentation
- Wrap each stage with timing; record p50/p95/max per minute into metrics
  (CH_32/00).
- Alert if a stage exceeds its budget repeatedly (CH_32/02).

## Pseudo-code: timed stage
```
def timed(stage, fn):
    t0 = now_ms(); r = fn(); dt = now_ms()-t0
    metrics.observe(stage, dt); budget_check(stage, dt)
    return r
```

## Rules
- Budgets are per-stage, measured end-to-end (queue + compute + send).
- A stage over budget twice in a row → alert; trading for affected symbols pauses.
- Re-validate budgets on every major code change (CH_38 benchmarks).
