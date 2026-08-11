# 02 — Market Phases and Sessions

## Purpose
Recognize that an intraday session has distinct phases with different behavior;
strategies must be aware of the clock, not just the price.

## Typical intraday session phases (equities/derivatives, local time)
1. **Opening auction + first minutes**: highest volume, widest ranges, most
   volatility and noise. Reversals common (opening range breakout/mean reversion).
2. **Morning trend (usually 30–90 min after open)**: directional flows as
   overnight news is digested.
3. **Midday lull**: lower volume, ranges, choppiness; many strategies go quiet.
4. **Afternoon drift**: renewed movement ahead of close.
5. **Close auction / last minutes**: closing imbalance, settlement, profit-taking.

## Session-aware strategy implications
- **Opening range** (first N-minute high/low) is a common intraday anchor.
- Avoid entering long-right-after-open on the first spike unless designed for it.
- Midday often rewards range/mean-reversion; open/close often reward breakout.
- Volatility clustering: use ATR to size and place stops relative to current phase.

## Data model for sessions
Store per bar: session id (PRE/OPEN/MORNING/MIDDAY/AFTERNOON/CLOSE), minutes
since open, time bucket. These become features (CH_09).

## Pseudo-code: phase classifier
```
mins = bar.time_minutes_since_open
if mins < 0:            phase = PRE
elif mins <= 15:        phase = OPEN
elif mins <= 90:        phase = MORNING
elif mins <= 210:       phase = MIDDAY
elif mins <= 330:       phase = AFTERNOON
else:                   phase = CLOSE
```

## Rules
- Never ignore the clock: time features are as important as price features.
- Compute and store session phase for every bar at ingestion.
- A strategy should define which phases it trades and reject signals elsewhere.
