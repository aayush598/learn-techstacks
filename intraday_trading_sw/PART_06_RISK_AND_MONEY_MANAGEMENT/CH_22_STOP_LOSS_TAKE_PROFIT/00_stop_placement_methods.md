# 00 — Stop Placement Methods

## Purpose
Place stops at levels that respect market structure and volatility — not round
numbers or gut feel — so losses are bounded without being noise-bait.

## Stop placement methods
1. **ATR-based**: stop = entry ∓ k×ATR (k typically 1.0–2.0). Adapts to
   volatility; k chosen from backtest evidence (CH_19/02).
2. **Structure-based**: stop beyond the nearest swing point / level that
   invalidates the thesis (CH_11/01) — a "if this breaks, I'm wrong" price.
3. **Volume-profile based**: stop beyond POC / high-volume node that should hold
   (CH_10/04).
4. **VWAP-based**: for mean reversion, stop beyond the deviation that defines
   failure.
5. **Broker/exchange rules**: respect minimum tick/price rules and margin.

## Placement algorithm
```
candidate = entry ∓ k×ATR
structure = structure_stop(side, swing_points)     # nearest invalidation level
stop = the_wider_of(candidate, structure)  + buffer  # conservative
# widen slightly beyond the level, not exactly at it (avoids stop hunting)
```

## Pseudo-code
```
def compute_stop(entry, side, atr, k, structure_level):
    vol_stop  = entry - side*k*atr
    struct    = structure_level - side*buffer
    return max(vol_stop, struct) if side==LONG else min(vol_stop, struct)
```

## Sizing interaction
- Stop distance feeds position sizing (CH_21). Wider stop → smaller qty →
  same risk. Never widen the stop *and* keep the size.

## Rules
- Stops are computed at entry time and recorded in the trade plan (CH_14/02).
- Never place a stop inside the spread / inside noise (< 0.5×ATR).
- Re-verify stop distance when modifying an order (risk re-check, CH_20/01).
