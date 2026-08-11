# 01 — Walk-Forward Analysis

## Purpose
Simulate the realistic deployment cycle: retrain periodically, trade the next
window, roll forward. This is the most honest evaluation of a strategy.

## Walk-forward procedure
```
for each window (train_len, test_len) rolling forward:
    fit features/model on window.train
    run strategy on window.test ONLY (no re-fitting mid-test)
    record test-window metrics
combine all test-window metrics = the walk-forward result
```

## Design parameters
- **Window length**: e.g., train 3 months, test 1 month; or daily-expanding.
- **Re-fit cadence**: match how the live system retrains (CH_16/03).
- **Buffer/purge** between train and test (CH_19/00) for label horizons.

## What walk-forward gives you
- A performance distribution across time, not one number.
- Stability metrics: % of windows with positive expectancy, median/CI of Sharpe.
- Early warning: strategy works only in one regime → show regime breakdown.

## Pseudo-code: walk-forward runner
```
results = []
for (train, test) in windows(data):
    pipe.fit(train); model.fit(pipe.transform(train.X), train.y)
    pnl = run_strategy_on(test)          # event-driven engine (CH_17/00)
    results.append(metrics(pnl, test))
final = aggregate(results)               # median, CI, %positive-windows
```

## Acceptance rule (example)
- ≥ 60% of test windows positive after costs, median expectancy > 0, and no
  window worse than −X× the risk limit.

## Rules
- Walk-forward is the *gate* for going to paper trading (CH_37).
- Results must be re-computed when train/test periods are extended.
- Report per-window metrics in the strategy report (CH_18/03).
