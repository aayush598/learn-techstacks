# 02 — Momentum and Breakout

## Purpose
Design strategies that enter on follow-through once price breaks structure with
conviction, riding the direction of the day.

## When momentum works
- Trending regime (strong ADX), high relative volume, liquid instruments.
- Session phases with directional flow (open/afternoon).
- Breakouts from tight ranges / opening-range / consolidation.

## Core hypothesis
Information is absorbed gradually; once a key level breaks with participation,
the move continues as other participants join (herding, stop runs).

## Strategy template
- **Trigger**: close beyond structure level (range high, opening-range high,
  previous swing) by a buffer (e.g., 0.2–0.5×ATR).
- **Confirmation**: relative volume > threshold (e.g., 1.5–2×) and no opposing
  divergence; ideally order-flow imbalance aligned.
- **Entry**: limit/stop order at breakout level (avoid chasing far beyond).
- **Stop**: below the breakout level / structure (k×ATR).
- **Target**: next structure/volume-profile node, or trail (CH_22).

## Pseudo-code: entry condition
```
if close > level + buffer and rel_vol > conf_vol and adx > adx_min:
    LONG signal (stop = level - stop_atr*atr)
elif close < level - buffer and rel_vol > conf_vol and adx > adx_min:
    SHORT signal
```

## Common failure modes (and defenses)
- **Whipsaws** → require close-beyond (not touch) + volume confirmation.
- **Fake break with no follow-through** → protective stop just inside level;
  re-entry allowed only on reclaim.
- **Late chase** → only enter within X ATR of the level; skip stretched moves.

## Rules
- Breakout signals must be timestamped at the confirming close; never at the
  touch bar (no look-ahead).
- Trend context (higher timeframe) must align with the breakout direction.
- Let winners run with trailing stops — this is where the payoff comes from.
