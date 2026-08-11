# 00 — Risk-First Design

## Purpose
Make the risk layer the most heavily engineered part of the system: every
signal passes through it, and it can stop everything.

## Principles
1. **Risk is enforced in code, not by discipline**: limits are hard gates; the
   engine cannot bypass them.
2. **Fail-safe**: on any anomaly or uncertainty, the default action is to *halt*
   or *flatten*, never to trade more.
3. **Risk is independent**: the risk layer knows nothing about strategy details;
   it only enforces policy.
4. **Layers of defense**: software risk gates + broker-side protective orders
   + daily limits + human escalation (defense in depth).

## Architecture
```
Signal -> RISK GATE -> order
            |-- per-trade limits (CH_20/01)
            |-- portfolio limits (CH_20/02)
            |-- event/calendar gates (CH_12/02)
            |-- circuit breakers (CH_23)
            `-- audit log of every decision
```

## Pseudo-code: risk gate (single choke point)
```
def approve(order, state, policy):
    checks = [
      per_trade_ok(order, policy),      # size, stop distance
      portfolio_ok(order, state, policy), # exposure, correlation
      daily_ok(state, policy),          # daily loss/win limits
      breaker_ok(state, policy),        # no circuit breaker tripped
      event_ok(order, calendar),        # no high-impact event window
    ]
    if all(checks): return APPROVE
    log_risk_reject(order, reasons); return REJECT
```

## Risk policy file (single source of truth)
```
risk_policy.yaml:
  capital: 100000
  max_risk_per_trade_pct: 0.5      # % of equity risked per trade
  max_daily_loss_pct: 2.0          # halt trading for the day
  max_open_positions: 10
  max_gross_exposure_pct: 60
  max_corr_concentration: 0.35
  breakers: { enabled: true, dd_pct: 5.0 }
  events: { pause_minutes: 15, importance_min: HIGH }
```

## Rules
- The risk layer is read-only about policy (loaded from config, never hardcoded).
- Every rejection is logged with reasons (CH_33) — the risk journal.
- Risk gates run on the live engine thread — no async ambiguity at decision time.
