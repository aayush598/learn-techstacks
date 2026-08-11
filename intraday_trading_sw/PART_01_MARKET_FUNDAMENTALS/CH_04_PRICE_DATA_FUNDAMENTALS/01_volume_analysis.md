# 01 — Volume Analysis

## Purpose
Use volume as the confirmation signal: price without volume tells an incomplete
story.

## Core volume concepts
- **Volume confirms price**: up moves on rising volume are stronger than up moves
  on shrinking volume (divergence warning).
- **Climax volume**: extreme spikes often mark short-term exhaustion/reversal.
- **Volume-by-price**: the distribution of volume across price levels reveals
  where big interests sit (support/resistance) — used in volume profile.
- **Relative volume**: current volume vs average volume at same session time
  (accounts for the intraday U-shaped pattern). High relative volume = abnormal
  interest.
- **Volume delta**: buying vs selling volume (from tape aggressor side) → net flow.

## Practical features
- volume / average volume (same session-time bucket) — relative volume
- volume z-score within session
- up-volume vs down-volume (buying/selling pressure)
- volume delta and cumulative volume delta (from tape)
- point-of-control (POC) and high-volume nodes from volume profile

## Pseudo-code: relative volume
```
rel_vol = bar.volume / rolling_mean(session_time_bucket_volume, 20)
# bucket = same time-of-day over last 20 sessions
```

## Rules
- Always pair a price signal with a volume/participation confirmation before entry.
- Flag volume divergences (price new high, volume declining) as weakening.
- Use volume-profile levels for stop/target placement (CH_22).
