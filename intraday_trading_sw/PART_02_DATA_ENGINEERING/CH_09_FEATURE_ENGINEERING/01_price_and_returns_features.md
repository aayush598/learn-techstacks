# 01 — Price and Returns Features

## Purpose
Define the price-derived features that describe level, change, and distribution —
the raw material for indicators and models.

## Core features (with specs)
- **log_return_1m** = ln(close_t / close_{t-1})
- **log_return_n** = ln(close_t / close_{t-n}) for n in {3,5,10,15,30,60}
- **close_above_sma_n** = close_t − sma_n(close) (deviation, not boolean)
- **rolling_std_return** = std(log_returns, window)  → volatility feature
- **high_low_range** = (high − low)/close
- **open_to_close** = (close − open)/open
- **gap_from_open** (relative to session open for first bars)
- **drawdown_from_day_high** = (close − day_high)/day_high

## Derived families
- **Momentum**: differences of returns over multiple horizons (concise).
- **Mean reversion signal**: z-score of price vs rolling mean.
- **Extreme returns**: indicator flags for |return| > k·σ (tagged, not dropped).

## Pseudo-code: rolling returns
```
def features_for_close(series, horizons):
    out = {}
    for n in horizons:
        out[f"ret_{n}"] = log(series[t]/series[t-n])   # shift by n
        out[f"z_{n}"]   = zscore(series[t-n+1:t+1])     # recent window
    return out
```

## Usage guidance
- Models work better with **log returns** (additive, more stable scale).
- Include **multiple horizons**: short for entry, long for context.
- Interactions (e.g., return × volume-z) are usually feature-engineered, not
  left to the model.

## Rules
- Returns must be computed on adjusted prices (CH_07/02).
- Every return feature must be shifted so it contains no future info.
- Test that `ret_n` at t equals exactly `ln(close_t/close_{t-n})` (QA, CH_36).
