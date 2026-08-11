# 03 — Outlier Detection

## Purpose
Find and handle extreme data points that are errors (bad prints) versus real
market events (news spikes) — the two must never be treated the same.

## Two classes of outliers
- **Errors**: bad prints, decimal shifts, stale/duplicate ticks, feed glitches.
  → Correct or reject.
- **Real events**: flash spikes, halt/limit moves, gap on news. → Preserve, but
  tag and handle carefully (stops may fill at bad prices; features must be robust).

## Detection methods
- **Absolute bounds**: price outside [min,max] for the instrument (exchange rules).
- **Rolling z-score**: |z| > threshold vs rolling mean/std of returns.
- **Hampel filter**: median-based, robust to the outliers themselves.
- **Tick price jump**: single tick moves > K×ATR within a bar with no volume
  support → likely error.
- **Zero/negative**: price ≤ 0, absurd volume, inverted bid>ask.

## Handling policy
| Class | Action |
|---|---|
| Obvious error | reject at validation (CH_07/01) |
| Suspicious | quarantine + manual review |
| Real extreme | keep, tag `event=True`, use robust statistics |

## Robust feature note
Prefer median/quantile-based statistics and winsorized scaling so one extreme
bar cannot distort indicators and model inputs (CH_09).

## Pseudo-code: Hampel outlier
```
def hampel(values, window, n_sigma):
    median = rolling_median(values, window)
    mad    = rolling_median(|values - median|)   # scaled
    return [x if |x - m| <= n_sigma*mad_scale else m for x,m in zip(...)]
```

## Rules
- Never silently delete outliers; log them and record the action.
- Tag preserved extreme bars so backtests can report their effect.
- Outlier handling is data-layer logic, before feature engineering.
