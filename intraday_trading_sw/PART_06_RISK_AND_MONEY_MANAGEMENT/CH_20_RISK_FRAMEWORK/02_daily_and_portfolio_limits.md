# 02 — Daily and Portfolio Limits

## Purpose
Cap aggregate risk across all open positions and across the trading day, so
correlated losses or a bad day can't compound into a catastrophe.

## Portfolio (cross-position) limits
- **Max open positions**: cap simultaneous trades.
- **Max gross exposure**: Σ(qty×price) / equity ≤ limit.
- **Max net exposure**: Σ(sign×qty×price) / equity ≤ limit (long/short balance).
- **Correlation concentration**: total risk in correlated instruments ≤ limit
  (e.g., one sector/theme; CH_13/04).
- **Concentration per symbol**: max % of capital in any single instrument.

## Daily limits (behavioral circuit breakers)
- **Max daily loss** (e.g., 2% of equity): hit → flatten all, halt for the day.
- **Max daily wins / profit target** (optional): lock in gains, stop overtrading.
- **Max trade count per day**: limits overtrading and fee bleed.
- **Max consecutive losses** (e.g., 5): pause and review (pattern, not just bad luck).

## Pseudo-code: portfolio gate
```
def portfolio_ok(order, state, policy):
    new = state.exposure + order.notional
    ok1 = len(state.positions) + 1 <= policy.max_open_positions
    ok2 = new.gross <= policy.max_gross_exposure_pct * equity
    ok3 = new.net  <= policy.max_net_exposure_pct  * equity
    ok4 = correlation_ok(order, state.positions, policy.max_corr_concentration)
    ok5 = per_symbol_notional_ok(order, state, policy)
    return all([ok1, ok2, ok3, ok4, ok5])
```

## Pseudo-code: daily gate
```
def daily_ok(state, policy):
    if state.daily_pnl_pct <= -policy.max_daily_loss_pct:  return HALT("daily_loss")
    if state.trade_count >= policy.max_trades_per_day:     return HALT("max_trades")
    if state.consecutive_losses >= policy.max_consec_loss: return HALT("streak")
    return OK
```

## Recovery handling
- After a daily halt, the next day starts fresh with the same limits — no
  "revenge" allowance.
- When a limit is hit, the engine flattens with market orders and disables new
  entries until the next session (CH_23).

## Rules
- Limits are config (risk_policy.yaml, CH_20/00) — reviewed, never edited live.
- Portfolio checks run before every new order; daily checks run on every bar.
- Violations that still get through (any system failure) become top-priority
  incidents (CH_32).
