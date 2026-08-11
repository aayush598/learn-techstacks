# 01 — Stop and Bracket Orders

## Purpose
Learn the protective and bracket order structures that enforce risk limits at
the broker level (in addition to software-level risk gates).

## Stop order (stop-loss)
- Becomes a market (or limit) order when price touches the stop level.
- Buy-stop triggers above current price; sell-stop triggers below.
- Purpose: cap loss. Note: a sell-stop can fill *worse* than the stop price
  (slippage/gap), especially in fast markets.

## Stop-limit
- Stop becomes a *limit* order after trigger: caps slippage but may not fill.
- Trade-off: fill certainty vs price control.

## Bracket orders
- **Entry** + **profit target (limit)** + **stop loss** placed as one unit.
- Rules: when one leg fills, the other legs are canceled; the bracket protects
  the position automatically even if software fails.
- Intraday variant: add a **time stop** (exit by time regardless of P&L).

## Design decisions
- Always attach a protective stop at the broker when going live (defense in depth).
- Compute stop/target prices from risk module (PART_06) *before* entry.
- On cancel/replace of legs, keep the protection continuous (no unprotected gap).

## Pseudo-code: place bracket
```
entry = risk.bracket_plan(symbol, side, qty)   # CH_22
main = broker.place(side, qty, entry.limit or market)
if main.filled:
    sl = broker.place(sell_stop(qty, entry.stop_price))      # protective
    tp = broker.place(sell_limit(qty, entry.target_price))   # profit
    bracket = {entry: main, stop: sl, target: tp}
    link_cancel_rule(bracket)   # OCO: if one fills, cancel others
```

## Rules
- Never leave a live position without a protective stop (software or broker).
- A stop is protection, not a prediction; it may slip in gaps.
- Time stops keep intraday risk bounded — no overnight surprises.
