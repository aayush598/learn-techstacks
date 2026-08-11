# 02 — Microstructure Patterns

## Purpose
Use order-flow and book dynamics (not just price shape) to spot transient
imbalances and exhaustion.

## Patterns to detect
- **Order-book imbalance spikes**: large sustained bid imbalance → short-term
  upward pressure; reversal candidates when price stalls despite imbalance.
- **Absorption**: heavy size on one side repeatedly consumed without price
  movement — big player holding price → breakout or exhaustion pending.
- **Iceberg detection**: repeated refill at same price/size — hidden large order.
- **Aggressive-flow exhaustion**: rising buyer-initiated volume but price making
  no progress → tiring; reversal risk.
- **Sweep-and-recover**: price wicks through a level (stop sweep) then snaps
  back — classic shakeout; useful for entry timing.
- **Spoofing-like patterns**: large limit orders that repeatedly cancel before
  being reached (must be flagged, not traded blindly).

## Feature events (typed, timestamped)
`FLOW_IMBALANCE`, `ABSORPTION`, `SWEEP_RECOVER`, `EXHAUSTION`, `ICEBERG`.

## Pseudo-code: absorption detector
```
def detect_absorption(book_window):
    # size consumed at best bid over window vs price change
    consumed = sum(deltas(book_window, best_bid))
    moved    = |price(now) - price(start)|
    return consumed > k * typical_flow and moved < tol_atr
```

## Why they matter
- These patterns precede moves *before* price shape shows it — they lead, candles lag.
- Best used as *alert/context* alongside price patterns, or as features to models.

## Data requirements
- Needs L2 book and/or tape with aggressor side (CH_03/02, CH_06/03).
- If unavailable: degrade to flow proxies (volume delta on bars).

## Rules
- Flag manipulative patterns (spoof-like) as risk warnings, never trade them.
- Validate detectors on replayed sessions (CH_37); measure false-positive rates.
- Always record the exact data used (depth, threshold) with each event.
