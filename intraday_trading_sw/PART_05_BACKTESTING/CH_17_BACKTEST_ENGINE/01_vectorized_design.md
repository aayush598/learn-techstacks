# 01 — Vectorized Backtest Design

## Purpose
Provide a fast, array-based backtester for quick screening of many parameter
combinations — always cross-checked against the event-driven engine.

## When to use
- Screening hundreds of strategies/parameter sets (CH_19/02).
- Indicator/signal sanity checks before investing in a full engine run.

## How it works
- Precompute signal arrays (vectorized over all bars).
- Simulate entries/exits via vectorized position transitions where possible.
- Apply flat assumptions (e.g., fills at next-bar open, fixed slippage) — the
  same conventions as the event-driven engine.

## Simplifications (must be documented)
- No intra-bar stop paths, no partial fills, no concurrent-order queue logic
  unless modeled explicitly.
- Because of these, vectorized results are a *screen*, not a verdict.

## Pseudo-code: vectorized skeleton
```
signals = strategy.signal_array(features)     # long/short/flat per bar
exec_px = next_open(signals)                  # shift: signal at t -> fill t+1
pnl = vectorize_fills(exec_px, signals, costs)
```

## Cross-validation with event-driven
- Rule: any strategy that passes vectorized screening MUST be re-run through the
  event-driven engine (CH_17/00) before acceptance.
- Discrepancies above a tolerance → investigate (usually timing/cost modeling).

## Pseudo-code: cross-check
```
v = vectorized_backtest(s)
e = event_backtest(s)
if |v.net_pnl - e.net_pnl| / max(|e.net_pnl|,1) > tol:
    flag_inconsistency(s)
```

## Rules
- Label every backtest result with its engine type (vectorized/event-driven).
- Never quote vectorized numbers as final performance.
- Keep both engines sharing the same cost model (CH_17/02) — one source of truth.
