# 02 — Backfill and Gap Filling

## Purpose
Repair missing data caused by disconnects, feed outages, or source gaps, so the
store is continuous and strategies never act on holes.

## When backfill is needed
- Reconnect after a WebSocket drop (missed interval since last confirmed bar).
- Source provided data with gaps (delisted hours, feed maintenance).
- Historic job finished but a range failed partway.

## Backfill procedure
1. Detect gap: expected next bar timestamp vs actual (CH_07 gap detector).
2. Determine fill source: prefer the same source; else the catalog backup (CH_05).
3. Fetch missing window via REST (chunked, with rate limit).
4. Validate fetched bars with the standard suite.
5. Merge into store *as a corrected version*, preserving original raw (lineage).
6. If a gap cannot be filled, mark the window `has_gap=True` and propagate this
   flag to any feature/backtest consumer — never fabricate bars.

## Pseudo-code: gap detector
```
expected = last_bar.ts + bar_period
if next_bar.ts > expected + tolerance:
    gap = (expected, next_bar.ts - bar_period)
    schedule_backfill(symbol, gap)
```

## Data fabrication policy
- **Allowed**: interpolation only for display/plotting, clearly labeled.
- **Forbidden**: fabricated bars entering backtests or model training.
  Gaps must be represented by explicit flags so backtests skip honestly.

## Rules
- Backfill is offline-safe: run immediately on reconnect, not on the live thread.
- Never silently splice sources without lineage tags (CH_05).
- Monitor gap counts per symbol per day (CH_32) as a data-health KPI.
