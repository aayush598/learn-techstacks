# 03 — Time and Session Features

## Purpose
Encode the calendar and clock context that makes intraday patterns predictable.

## Core features
- **session_phase** (categorical: OPEN/MORNING/MIDDAY/AFTERNOON/CLOSE) — CH_02/02
- **minutes_since_open** (float)
- **minutes_to_close** (float)
- **day_of_week** (1–5)
- **time_bucket** (e.g., minute-of-session normalized 0–1)
- **is_pre_news_flag** (minutes since known scheduled events — with calendar, CH_12)
- **bar_index_in_session** (sequential count)

## Why time features matter
- Volatility, volume, and drift all vary by time-of-day (U-shape, open/close).
- Session phase directly gates which strategy logic may run (CH_02/02).
- Minutes-to-close matters for exits (time stops, no overnight).

## Encoding approach
- Categorical → one-hot or ordinal with documented mapping.
- Cyclical time (minute-of-session) → keep as ordinal minutes; do NOT fold into
  radians unless a model needs it (keep it interpretable).
- Normalize by session length (different markets have different session lengths).

## Pseudo-code
```
f.minutes_since_open = bar.t - session.open_time
f.minutes_to_close   = session.close_time - bar.t
f.session_phase      = classify_phase(f.minutes_since_open)   # CH_02/02
f.day_of_week        = bar.t.weekday()
```

## Rules
- Derive from the bar timestamp and the session calendar only — no live clock
  dependency in features (deterministic per bar).
- Time features are mandatory for any intraday model (context).
- Never let a session-aware feature leak across the session boundary.
