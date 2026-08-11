# 02 — System and Acceptance Tests

## Purpose
Prove the whole system works together as a product, and that it meets the
defined success criteria (CH_00/01) — before any live deployment.

## System tests (end-to-end on replayed data)
- Full session replay (real recorded day): engine consumes bars exactly as live,
  produces the same decisions (CH_33/01 replay harness).
- Broker outage scenario: reconnect + backfill + reconciliation resume
  (CH_06, CH_25).
- Feed gap scenario: gap detection, halt for affected symbols, backfill
  (CH_06/02).
- Breaker scenario: force a daily-loss breach → flatten + halt + alert
  (CH_23/00, CH_30).
- Crash/restart scenario: kill engine mid-session → journal replay → reconcile →
  resume correctly (CH_28/02).
- Cost realism: live-ish fills vs model within tolerance (CH_17/02).

## Acceptance gates (definition of done per milestone)
- Data milestone: validation pass rate ≥ 99% (CH_07).
- Signal milestone: deterministic, no NaN leaks, latency under budget (CH_27/00).
- Strategy milestone: overfitting checklist passed (CH_19/03).
- Paper milestone: N sessions paper trading, correlation with expected behavior
  (CH_37).
- Live milestone: graduated scale-up plan executed (CH_37/02).

## Pseudo-code: acceptance run
```
def acceptance_suite():
    for scenario in SYSTEM_SCENARIOS: run(scenario)          # assert invariants
    gates = [data_gate, signal_gate, strategy_gate, paper_gate]
    return all(g.passed for g in gates)
```

## Rules
- Acceptance runs on staging (CH_31/00) against the simulator/paper broker.
- A failed acceptance gate blocks the next milestone — no exceptions.
- Scenarios are kept as versioned fixtures with the repo (reproducibility).
