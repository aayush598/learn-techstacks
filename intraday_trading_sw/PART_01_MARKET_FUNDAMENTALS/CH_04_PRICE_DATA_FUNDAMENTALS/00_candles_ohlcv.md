# 00 — Candles and OHLCV

## Purpose
Standardize the fundamental unit of price data — the OHLCV bar — so every module
agrees on its meaning, timestamps, and edge cases.

## Definition
A bar aggregates a time interval: **O**pen, **H**igh, **L**ow, **C**lose, **V**olume
(and optionally: trade count, VWAP, bid/ask range). It compresses tick noise into
a decision-relevant summary.

## Bar construction rules (critical)
- **Timestamp convention**: use the bar's *start* time (e.g., 09:31–09:32 bar is
  stamped 09:31) and state it explicitly everywhere.
- **Open** = first traded price of interval; **Close** = last traded price.
- **High** = max, **Low** = min of all trades (and sometimes quotes) in interval.
- **Volume** = sum of traded volume in interval (native units).
- **Period alignment**: bars must align to the exchange session; do NOT create
  bars across the session boundary (no bar spanning close→open).

## Edge cases
- Empty interval (no trades): decide policy — emit bar with open=high=low=close=last,
  volume=0, or skip. Document and keep consistent (affects indicators!).
- Session start/end partial bars: allow partial first/last bar, never merge days.
- Timezone: store UTC; convert to local session time at display/feature time.

## Pseudo-code: tick → bar aggregator
```
def on_tick(tick, bar_window):
    if tick.t < bar_start: return None        # drop late/stale ticks
    if tick.t >= bar_start + bar_window:
        emit(open, high, low, close, volume)  # finalize bar
        bar_start = floor_to_window(tick.t)
        open = close = tick.price; high = low = tick.price; volume = tick.size
    else:
        high = max(high, tick.price); low = min(low, tick.price)
        close = tick.price; volume += tick.size
```

## Rules
- One timezone, one timestamp convention, documented and enforced by tests.
- Use start-of-interval timestamps consistently in storage and features.
- Handle empty intervals explicitly; never feed NaN bars into indicators.
