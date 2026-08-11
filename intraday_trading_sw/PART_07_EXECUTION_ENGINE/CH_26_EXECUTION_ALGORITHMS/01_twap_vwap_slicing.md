# 01 — TWAP and VWAP Slicing

## Purpose
Slice large orders into small pieces over time to reduce market impact and
average into better prices (needed for larger intraday orders).

## TWAP (Time-Weighted Average Price)
- Split total qty into N equal child orders over a horizon T (one per interval).
- No price target — just time. Simple and predictable.

## Pseudo-code: TWAP scheduler
```
def twap_schedule(total, horizon, interval):
    n = horizon/interval
    piece = floor(total/n)
    for k in 1..n:
        schedule_emit_at(start + k*interval, piece)
```

## VWAP (Volume-Weighted Average Price)
- Split qty in proportion to expected volume profile per interval:
```
piece_k = total * expected_volume(k) / sum(expected_volume over horizon)
```
- Expected volume = session-time-bucket averages (CH_09/02).

## Execution with limits
- Each child order: limit at the *current* benchmark price (twap/vwap mid), or
  marketable limit slightly inside.
- Unfilled children: re-quote at next interval (no protection gaps).

## Pseudo-code: child re-quote
```
for interval:
    child = next_piece()
    lmt = twap_mid_or_marketable(child)
    oid = oms.submit(LIMIT, child, lmt)
    if not filled by next interval: cancel + re-quote (or market for last piece)
```

## Rules
- Slicing is optional complexity: only use when order size ≫ typical bar volume
  (impact threshold, CH_26/02).
- The last piece is often sent as market to guarantee completion before close.
- Backtest must model slicing faithfully (CH_17/03) if you use it live.
