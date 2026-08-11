# 01 — Per-Trade Risk Limits

## Purpose
Cap the loss a single trade can inflict, before it happens — the most important
number in the whole system.

## The core rule
Risk per trade ≤ max_risk_pct × equity (e.g., 0.5–1%).
Risk is defined as: stop distance × quantity (the amount you lose if stopped).

## Deriving position size (see also CH_21)
```
risk_amount  = max_risk_pct * equity
stop_dist    = entry_px - stop_px            # in price units (ATR-based, CH_22)
qty          = floor(risk_amount / stop_dist)
```

## Additional per-trade constraints
- **Max position notional**: qty × entry ≤ max_trade_notional_pct × equity.
- **Min stop distance**: never below noise level (≥ 0.5×ATR) — otherwise you're
  donating to the spread.
- **Max leverage**: gross exposure per trade ≤ broker/market limits.
- **Lot size**: round to tradable lot/board lot, never exceed risk_amount.

## Pseudo-code: per-trade gate
```
def per_trade_ok(order, policy, equity):
    risk = abs(order.stop - order.entry) * order.qty
    ok1  = risk <= policy.max_risk_per_trade_pct * equity
    ok2  = order.qty * order.entry <= policy.max_trade_notional_pct * equity
    ok3  = abs(order.stop - order.entry) >= policy.min_stop_atr * order.atr
    return ok1 and ok2 and ok3
```

## Edge cases
- **Gap risk**: a stop can slip; assume worst-case loss = stop_dist × gap_factor.
  If worst-case exceeds a hard cap (e.g., 3× normal), reject or reduce size.
- **Zero/NaN**: if entry/stop invalid → reject order (fail-safe).
- **Illiquid**: if estimated slippage > stop buffer → reject (CH_17/02).

## Rules
- Per-trade risk is computed on *entry* and re-checked on any modify.
- Sizing must never be overridden by strategy confidence alone (confidence may
  scale within the cap, CH_16/02).
- Log the computed risk per order with the order (audit, CH_33).
