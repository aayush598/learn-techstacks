# 00 — Feature Catalog Overview

## Purpose
Define a standard, versioned catalog of features used by indicators, strategies,
and ML models — each with a spec, unit, and no-look-ahead guarantee.

## Feature groups
1. **Price & returns** — levels, log-returns, moving averages, deviations.
2. **Volume & liquidity** — relative volume, volume delta, book imbalance, spread.
3. **Time & session** — phase, minutes since open, day-of-week, time bucket.
4. **Volatility** — realized vol, ATR ratio, gaps (usually in indicator layer).
5. **Microstructure** — tick-rule signed flow, trade size stats (CH_03/02).

## Feature record spec (per feature)
```
name, group, formula/spec, inputs, output dtype, lookback, missing policy,
canonical unit, usage notes, tested?(QA reference)
```

## No-look-ahead guarantee (critical)
A feature at time t may use **only** data available at t (inclusive of the bar
that has just closed at t, if declared). This is enforced by the feature engine:
- Rolling/expanding windows use strictly past observations.
- Any future-reference feature is forbidden (test catches it, CH_17/CH_36).

## Pseudo-code: feature engine contract
```
def compute_features(bars) -> FeatureFrame:
    for bar in bars:
        f[bar.t] = { feature: compute_spec(feature, history_up_to(bar.t)) }
```

## Versioning
- Each catalog version freezes feature definitions.
- Datasets are tagged with `features_version`; models/backtests reference it
  explicitly (reproducibility, CH_16/CH_19).

## Rules
- No feature enters a model or strategy without a catalog entry + tests.
- Missing values: explicit policy per feature (forward-fill only when safe,
  otherwise NaN with model handling — never invent values).
- All features must be computable incrementally for live use (CH_28).
