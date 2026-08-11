# 00 — Candlestick Patterns

## Purpose
Recognize single- and multi-bar price shapes that signal short-term reversal or
continuation, encoded as explicit rules (not fuzzy visual judgments).

## Pattern library (start set, each with rules)
- **Doji**: |open−close| ≤ small_frac × (high−low). Signifies indecision;
  meaningful only at key levels (trend extreme, POC).
- **Hammer / Shooting star**: long lower/upper wick, small body. Reversal *context*
  (after down/up move) matters more than shape.
- **Engulfing**: body of bar t engulfs body of t−1, opposite color.
- **Harami**: small body inside previous body.
- **Three soldiers / three crows**: three consecutive same-direction bodies.
- **Momentum bars**: body ≥ k×ATR, used for breakout confirmation.

## Detection framework
Pattern detector = (shape rules) AND (context rules). Store both parts explicitly.
- Shape: exact inequalities on o/h/l/c relative to ATR.
- Context: where in the session, trend regime, volatility percentile, key levels.

## Pseudo-code: engulfing
```
def detect(bar_prev, bar):
    up_engulf = bar.close > bar.open and bar_prev.close < bar_prev.open \
                and bar.close >= bar_prev.open and bar.open <= bar_prev.close
    context = regime == DOWNTREND and near_support(bar.close)
    return (up_engulf and context)
```

## Key-level interaction
Patterns are only worth acting on near: session open/high/low, day VWAP,
volume-profile POC/nodes, prior swing points. Far from levels they are noise.

## Usage guidance
- Patterns are *candidate signals* that feed the strategy layer (CH_14); the
  strategy still applies its own filters and risk rules.
- Never trade a pattern without volume/participation confirmation.

## Rules
- Every pattern has a precise spec + unit tests on crafted bars (CH_36).
- Report pattern + confidence + level distance, not a bare boolean.
- A single pattern rarely carries edge; combinations + context do.
