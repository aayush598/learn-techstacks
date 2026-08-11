# 01 — Mean Reversion

## Purpose
Design strategies that fade short-term extremes, betting price returns to an
intraday fair value.

## When mean reversion works
- Ranging regime (low ADX), liquid instruments, normal volatility.
- Price stretched far from VWAP/rolling mean with no volume confirmation.
- Session phases with range behavior (midday) rather than trend (open).

## Core hypothesis
At short horizons, price overshoots fair value due to order-flow imbalance and
market-maker positioning; the overshoot tends to revert (weak negative
autocorrelation, CH_01/02).

## Strategy template
- **Fair value**: session VWAP or rolling mean (e.g., 10–30 bar EMA).
- **Entry**: price deviates > k×ATR (or z > z_thresh) from fair value AND
  volume doesn't confirm the push AND regime is RANGE.
- **Target**: return to fair value (or VWAP).
- **Stop**: beyond deviation + buffer (structure/ATR-based, CH_22).

## Pseudo-code: entry condition
```
dev = (price - fair) / atr
if regime == RANGE and dev > +k and rel_vol < 1.5:
    SHORT signal
elif regime == RANGE and dev < -k and rel_vol < 1.5:
    LONG signal
```

## Common failure modes (and defenses)
- **Fading a strong trend** → require regime == RANGE (ADX filter).
- **Catching a falling knife** → wait for stabilization (first counter-bar),
  don't enter on the extreme bar itself.
- **News-driven moves** → event gate blocks (CH_12/02).

## Rules
- Mean reversion requires a fair-value anchor; never fade "because RSI high".
- Time-stop exits are essential (reversion may take longer than expected).
- Paper-trade at least a full market cycle before trusting (CH_37).
