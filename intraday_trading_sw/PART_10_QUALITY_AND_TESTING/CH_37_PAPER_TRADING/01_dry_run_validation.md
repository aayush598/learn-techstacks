# 01 — Dry-Run Validation

## Purpose
Compare paper-trading behavior against backtest expectations to catch any gap
between simulated and real live behavior before deployment.

## What dry-run must confirm
1. **Decision parity**: paper engine produces the same signals as the backtest
   engine for the same data (replay harness, CH_33/01).
2. **Fill realism**: paper fills within the cost-model tolerance of backtest
   assumptions (CH_17/02).
3. **Risk enforcement**: limits, breakers, halts behave as coded (CH_20–CH_23).
4. **Operations**: monitoring, alerts, dashboards, reconciliation all function
   (CH_32, CH_29).
5. **Latency**: stage budgets met (CH_27/00) — paper uses the live pipeline.

## Dry-run protocol
```
run_paper(weeks >= 4):
    daily:
        compare signals(paper) vs signals(backtest replay)   # parity %
        compare fills vs cost model tolerance
        record metrics; flag anomalies
    weekly: report drift, incidents, rejected signals review
exit criteria: N consecutive sessions with parity >= threshold,
               zero unexplained risk bypasses, alerts accurate
```

## Pseudo-code: parity check
```
def parity_day():
    sig_paper  = paper.journal.signals(day)
    sig_replay = replay(day).signals
    return fraction(sig_paper == sig_replay)
```

## Rules
- Dry-run counts as evidence in the acceptance gates (CH_36/02).
- Any unexplained mismatch between paper and backtest is a bug — fix before live.
- Dry-run results are stored like any report (CH_18/03), versioned.
