# 02 — Graduated Live Scale-Up

## Purpose
Move from paper to real money in small, reversible steps so any live-only
surprise costs little.

## Scale-up ladder (each step needs the prior one green)
| Step | Scope | Evidence needed |
|---|---|---|
| 1 | Live broker connected; **no auto-trading** | reconciliation clean, data flows, ops green |
| 2 | Auto-trading with **micro size** (e.g., 1 lot / min notional) | ≥ 2 weeks, no anomalies, slippage within model |
| 3 | Normal size for **1–2 strategies, few symbols** | ≥ 4 weeks, metrics match paper, drawdown OK |
| 4 | Full strategy set, all symbols, configured limits | ≥ 8 weeks + review sign-off |
| 5 | Full production | standing review cadence (CH_32) |

## Gate conditions per step
- Paper/dry-run green (CH_37/01).
- Overfitting checklist passed (CH_19/03).
- Reconciliation clean every session (CH_25/02).
- No breaker trips of unexplained cause (CH_23/00).
- Human reviewer signs off (audit, CH_34/02).

## Rollback (reversibility)
- Any step can step back to the previous level in minutes (config, not code).
- Live-only issues → record, fix, re-run dry-run (CH_37/01), then re-climb.

## Pseudo-code: step config
```
live_mode:
  step: 2
  max_notional_per_trade: 5000        # micro-size
  enabled_strategies: ["breakout_15m"]
  rollback_alert_thresholds: {...}    # auto-step-down on breach
```

## Rules
- The ladder is enforced by config + gates; skipping steps is not allowed.
- Live metrics are compared to paper expectations continuously (CH_16/03 drift).
- First real month is considered a validation period, not production.
