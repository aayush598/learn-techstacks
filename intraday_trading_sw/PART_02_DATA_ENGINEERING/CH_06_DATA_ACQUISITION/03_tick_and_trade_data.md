# 03 — Tick and Trade Data

## Purpose
Handle finest-granularity data: individual trades and quotes. Used for
microstructure features, exact fill simulation, and high-fidelity replay.

## Tick data model
- **Trade tick**: ts (ns precision), price, size, aggressor side (if known), trade id.
- **Quote tick**: ts, bid, bid_size, ask, ask_size, level (top or depth).
- Store in time order; keep raw source fields for audit.

## Processing concerns
- **Volume**: ticks can be enormous. Compress: store raw for a limited lookback +
  daily aggregates, and derive features incrementally.
- **Ordering**: timestamps from different sources may interleave; sort by a stable
  key (exchange seq id first, then ts).
- **Bid-ask bounce**: mid-price (bid+ask)/2 is the clean signal; trades flip
  between bid and ask.
- **Aggressor side**: usually inferred by tick rule when not provided (CH_03/02).

## Tick → bar (already covered) and tick → features
- Keep a rolling window of recent trades for: signed volume (tick rule),
  trade size distribution, print frequency, VWAP, book imbalance.

## Pseudo-code: rolling signed-volume counter
```
window = deque(maxlen=per_minute_capacity)
def on_trade(t):
    direction = tick_rule(t)            # +1 buyer, -1 seller
    window.append(direction * t.size)
    net_flow = sum(window)
```

## Storage strategy (tiered)
| Tier | Content | Storage |
|---|---|---|
| Hot | today's ticks (live trading) | memory + local file |
| Warm | last N days ticks | compressed columnar |
| Cold | old ticks (research) | compressed archives |
Never store ticks for every symbol forever by default; curate the hot list.

## Rules
- Ticks are used to build features, not for direct signal decisions (too noisy).
- Compress aggressively; validate and dedupe on arrival.
- A tick gap detector (sequence number discontinuity) must trigger backfill (CH_06).
