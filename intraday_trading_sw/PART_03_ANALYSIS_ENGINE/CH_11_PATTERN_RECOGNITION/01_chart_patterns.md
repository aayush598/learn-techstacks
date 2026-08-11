# 01 — Chart Patterns

## Purpose
Detect swing-based formations (trend lines, ranges, breakouts) using pivot
points, so the software "sees" the structure traders talk about.

## Primitive: swing points (pivots)
- **Pivot high**: bar whose high > k bars on each side. **Pivot low**: mirror.
- k is timeframe-scaled (e.g., 3–5 bars on 1m, more on higher TFs).
- Track as a sequence; structures are built from consecutive pivots.

## Structure library
- **Trend line**: connect successive pivot highs (down) / lows (up); breakout of
  the line = regime change candidate.
- **Support/Resistance**: horizontal levels from pivots that were touched ≥ N
  times; price near them + reaction = tradable zone.
- **Range**: bounded by a resistance and a support; strategies choose mean
  reversion at bounds or breakout on close beyond.
- **Opening-range breakout**: high/low of the first N minutes (e.g., 15m) act as
  intraday trigger levels.
- **Flag/pennant**: sharp move then tight consolidation — continuation pattern;
  trade the breakout with the initial move's direction.

## Detection steps
1. Compute pivots with a fixed k (configurable per timeframe).
2. Cluster pivot levels into zones (tolerance = e.g., 0.2×ATR).
3. Classify zones: support, resistance, or both (range).
4. Detect breakouts: close beyond zone ± tolerance with volume confirmation.
5. Emit structure events (zone touched, breakout, rejection) as typed events.

## Pseudo-code: breakout detector
```
for bar:
    if regime == RANGE and close > resistance + tol and rel_volume > 1.5:
        emit(Event.BREAKOUT_UP, level=resistance, conf=...)   # continuation
    if regime == TRENDING_UP and close < support - tol:
        emit(Event.BREAK_DOWN, ...)   # regime change candidate
```

## Usage guidance
- Breakouts need **confirmation** (close beyond, volume, follow-through), not a
  single touch — whipsaw protection.
- False breaks are common; define a stop-back-inside-zone rule (CH_22).

## Rules
- Pivot k must be documented per timeframe and tested for stability.
- Structures are events with timestamps — the backtest must see them *as of* their
  bar, never retroactively (no look-ahead, CH_17).
