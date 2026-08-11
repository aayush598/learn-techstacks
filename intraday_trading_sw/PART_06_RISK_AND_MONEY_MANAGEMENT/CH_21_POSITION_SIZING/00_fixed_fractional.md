# 00 — Fixed Fractional Sizing

## Purpose
Size every trade so the dollar risk is a constant fraction of equity — the
safe, baseline money-management method.

## Formula
```
risk_amount = equity × f            # f = 0.005..0.01 typical
qty         = floor(risk_amount / stop_distance)     # stop_distance in price units
```
Stop_distance comes from the stop rule (CH_22), typically k×ATR.

## Why it works
- Constant risk per trade → drawdowns are survivable and compounding is smooth.
- Automatically scales down after losses and up after gains (risk-based).

## Pseudo-code
```
def size_fixed_fractional(equity, stop_dist, f):
    if stop_dist <= 0: return 0
    risk = equity * f
    return floor(risk / stop_dist)   # then apply lot-size rounding (CH_20/01)
```

## Choosing f (risk fraction)
- f = 0.5–1% for moderate; 0.25% for conservative. Based on your max drawdown
  tolerance: a realistic max drawdown ≈ 10–20× f.
- Calibrate from backtest drawdowns (CH_18/01): f should keep worst-case DD
  within a tolerable band.

## Interaction with other gates
- The result still must pass per-trade notional and leverage caps (CH_20/01).
- Sizing happens inside the risk layer — the strategy never sets qty directly;
  it proposes a plan, risk computes qty.

## Rules
- qty = 0 → no trade (risk engine won't fabricate minimum sizes).
- Round down, never up (protect the risk budget).
- f is per-strategy-configurable but bounded by the global policy maximum.
