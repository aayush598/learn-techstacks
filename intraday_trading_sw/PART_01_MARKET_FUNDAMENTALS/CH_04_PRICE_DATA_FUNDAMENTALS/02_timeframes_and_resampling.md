# 02 — Timeframes and Resampling

## Purpose
Define how the software supports multiple timeframes and builds higher-timeframe
bars from lower-timeframe bars consistently.

## Supported timeframe model
- Base storage granularity: finest reliable data you can get (1m bars or ticks).
- Derived timeframes: 3m, 5m, 10m, 15m, 30m, 60m, day.
- Higher timeframes are **derived** from base bars, never separately ingested
  (single source of truth; guarantees consistency).

## Resampling rules
- Group base bars by aligned period boundaries of the target timeframe.
- **OHLCV aggregation**: open = first open; high = max high; low = min low;
  close = last close; volume = sum volume; count = sum counts.
- Never mix sessions: stop aggregation at session boundaries.
- Only resample from validated bars; apply same empty-interval policy.

## Multi-timeframe strategy pattern
- **Higher timeframe = context** (trend, regime): e.g., 15m trend filter.
- **Lower timeframe = trigger** (precise entry/exit): e.g., 1m momentum.
- A trade only fires when context and trigger agree.

## Pseudo-code: resample
```
def resample(base_bars, target):
    out = []
    group = []
    for bar in base_bars:
        if same_period(group, bar, target) and same_session(group, bar):
            group.append(bar)
        else:
            if group: out.append(aggregate(group))
            group = [bar]
    if group: out.append(aggregate(group))
    return out
```

## Rules
- Derive higher timeframes from validated base bars only.
- A strategy must declare which timeframe it reads as context vs trigger.
- Cache derived timeframes; invalidate only on new base data.
