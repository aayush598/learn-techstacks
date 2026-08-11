# 03 — Simulation Fidelity

## Purpose
Ensure the backtest simulates the real trading environment faithfully; the
difference between simulation and reality is where money is lost.

## Fidelity dimensions
1. **Timing**: signal→execution latency modeled (next-bar open + reaction delay).
2. **Stops**: intra-bar stop fills use the *triggered* price with slippage, not
   the bar close (be conservative).
3. **Gaps**: stops fill at the gap price (worse), not the stop price.
4. **Partial fills / rejections**: rare but modeled for realism (config flag).
5. **Limit fills**: a limit fill is assumed when the bar trades through the
   limit — but conservative: require a cross by a buffer or use midpoint bias.
6. **Calendar**: holidays, half-days, corporate-action dates excluded/adjusted.
7. **Session close**: force-flatten rules at close (no overnight).
8. **Regime coverage**: the backtest period must include up/down/range and
   high/low volatility months (CH_19/00).

## Fidelity checks (test suite)
- **No look-ahead test**: a strategy that "predicts" with future data must
  produce flat results in the test (synthetic canary).
- **Cost sensitivity**: results must be stable (not flip sign) for small cost
  changes.
- **Replay determinism**: rerun gives byte-identical output (fixed seeds).

## Pseudo-code: intra-bar stop fill
```
if stop_order and bar.low <= stop_price <= bar.high:
    fill = stop_price * (1 + side*slip_bp/1e4)   # worse than stop
    if gap: fill = bar.open (worse)              # overnight/session gap
```

## Fidelity budget (what to spend effort on)
1. Costs/slippage — highest impact.  2. Timing/look-ahead — correctness.
3. Gaps and stop paths.  4. Calendar and close handling.  5. Everything else.

## Rules
- Default to *conservative* when uncertain; optimism is the enemy.
- Every assumption is a documented parameter, reviewed in QA (CH_36).
- Backtest reports list every fidelity assumption (CH_18/03) — trust demands it.
