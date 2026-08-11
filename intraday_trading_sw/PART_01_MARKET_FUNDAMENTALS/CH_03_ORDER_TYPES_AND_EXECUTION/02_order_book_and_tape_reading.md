# 02 — Order Book and Tape Reading

## Purpose
Turn the raw order book and trade tape into actionable microstructure features
and signals.

## The order book (L2)
- Levels: price → size (bid side and ask side).
- **Depth**: cumulative size at/beyond best levels.
- **Imbalance** = (bid_size − ask_size) / (bid_size + ask_size) at chosen depth.
- **Wall detection**: abnormally large size at a level → likely support/resistance.
- **Queue position**: with price-time priority, a resting order's position matters.

## The tape (trades)
- Every print: price, volume, timestamp, aggressor side (if known).
- **VWAP tracking**: compare traded price to day VWAP to judge fair value.
- **Large prints** (block trades) can indicate institutional activity.
- **Print frequency & avg size** signal retail vs institutional participation.

## Practical features (used in CH_09)
- spread (bp), mid-price, bid/ask size ratio, depth imbalance at levels 1–5,
  count of level changes per second, net signed volume per minute, trade size
  distribution, number of large prints.

## Pseudo-code: imbalance feature
```
def book_imbalance(bid_sizes, ask_sizes, depth=5):
    b = sum(bid_sizes[:depth]); a = sum(ask_sizes[:depth])
    return (b - a) / (b + a)      # +1 strong bid pressure, -1 ask pressure
```

## Rules for using L2/tape data
- The exchange/broker must actually supply L2 + tape; check feed spec first (CH_05).
- If unavailable, gracefully degrade to OHLCV-only features (never crash).
- Store raw book snapshots for replay/audit, not only derived features.

## Integration step
1. Feed → normalizer → per-second snapshots → aggregate to bars (CH_06).
2. Extract book/tape features in the feature engine (CH_09).
