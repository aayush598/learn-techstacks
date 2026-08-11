# 00 — Split and Validation Strategies

## Purpose
Define how to partition data so validation results reflect out-of-sample
performance — the heart of honest evaluation.

## Time-ordered splits (mandatory)
- **Random split is FORBIDDEN** for time-series/market data (leaks across time).
- Structure: `Train | Validation | Held-out Test` strictly chronological.
  - Train: fit everything (scalers, models, features).
  - Validation: early stopping, calibration, parameter tuning (repeatedly).
  - Test: evaluated exactly once, after all choices are frozen.

## Split conventions
- **Purged gaps**: when labels span h future bars, drop a buffer of h bars between
  train and validation (prevents label leakage across the split).
- **Embedding**: keep per-symbol continuity; never split mid-session in a way
  that leaks session features.
- **Calendar-aware**: train/val/test may skip holiday disruptions.

## Pseudo-code: purged split
```
def time_split(df, train_end, val_end, h):
    train = df[df.t <= train_end - h]
    val   = df[(df.t > train_end) & (df.t <= val_end - h)]
    test  = df[df.t > val_end]
    return train, val, test
```

## Coverage requirement
- Validation + test windows must contain up/down/range regimes and high/low
  volatility periods (CH_17/03) — otherwise results are period-lucky.

## Rules
- The test set is touched exactly once (per model family). Multiple peeks = overfit.
- Document the exact split boundaries in every dataset artifact (CH_16/01).
- When adding features/models later, re-do the split process cleanly.
