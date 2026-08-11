# 01 — Realtime Charts

## Purpose
Render live candles, indicators, and structure levels — self-hosted, with no
external charting service.

## Rendering approach (dependency-minimized)
- **Server**: generate chart *data* (bars, indicator series, level lines) as
  compact JSON from the engine snapshot.
- **Client**: a small canvas/SVG renderer (hand-written or a tiny library)
  draws: candlesticks, indicator overlays, volume bars, level lines, POC,
  VWAP, and marked signal entries/exits.
- **Streaming**: send delta updates (new bar, updated indicator) over the live
  channel; full redraw on session start / timeframe change.

## Chart requirements
- Timeframes: match the engine's (1m/5m/15m/…) with multi-timeframe overlays
  (context vs trigger, CH_04/02).
- Structure overlays: opening range, swing levels, volume-profile POC (CH_11).
- Signal markers: entries (arrow), stops/targets (lines), exits (dot) from the
  journal — so decisions are visible against the market.

## Pseudo-code: client render loop
```
on_data(payload):
    if payload.type == BAR_UPDATE: draw_bar(payload.bar)
    elif payload.type == LEVELS:   draw_levels(payload.levels)
    elif payload.type == MARK:     draw_signal_marker(payload.signal)
```

## Rules
- Charts are read-only views of engine truth — never a place to trade.
- Indicator series on the chart must use the same incremental engine math
  (CH_10/00) — no client-side recomputation drift.
- Streaming updates must be idempotent (re-send safe on reconnect).
