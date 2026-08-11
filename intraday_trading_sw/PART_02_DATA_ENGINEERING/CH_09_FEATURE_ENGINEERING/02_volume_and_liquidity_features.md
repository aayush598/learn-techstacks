# 02 — Volume and Liquidity Features

## Purpose
Define the features that tell the model *whether* a move is supported by
participation (the difference between real moves and noise).

## Core features
- **relative_volume** = volume_t / mean(volume at same session-time bucket, 20d)
- **volume_z** = (volume_t − mean)/std over rolling window (per session shape)
- **volume_delta** = buyer_volume − seller_volume (needs aggressor side)
- **cum_volume_delta** = running sum within session
- **trade_count** and **avg_trade_size**
- **large_print_count** = trades above k×avg size in window
- **spread_bp** = (ask−bid)/mid × 10000 (if quotes available)
- **book_imbalance_N** = (bidSize−askSize)/(bidSize+askSize) at depth N (CH_03/02)
- **vpin (volume-synchronized pressure)**: signed volume over rolling volume bars

## Session-shape awareness
Volume has a U-shape across the day. Bucketing by session-time (CH_02/02)
removes that bias before normalization.

## Pseudo-code: session-time bucket mean
```
def rel_volume(bar, hist_by_bucket):
    key = bucket(bar.session_minute)              # e.g., every 5 min
    avg = hist_by_bucket[key].rolling_mean(20)
    return bar.volume / max(avg, 1)
```

## Usage guidance
- Combine with price features: `price_up & rel_volume_high` = strong push;
  `price_up & rel_volume_low` = weak/false break.
- Volume delta is directionally informative; use sign and magnitude.

## Rules
- Volume features are computed per-session-time bucket, never flat across the day.
- If aggressor side is unavailable, do not fabricate; omit delta features.
- Handle zero/NaN when a symbol has no trading in a bucket (explicit policy).
