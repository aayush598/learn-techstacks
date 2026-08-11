# 03 — Volatility Indicators

## Purpose
Measure expected price variability to size positions, set stops, and filter
conditions (most intraday strategies only work in a certain volatility band).

## Volatility indicator set
- **ATR(n)** — average true range (Wilder). Basis for stop distance and sizing.
- **Realized vol** — std of log returns over window, annualized or per-bar scale.
- **Bollinger bandwidth** = (upper−lower)/mid — normalized range.
- **Historical vol percentile** — current vol vs its own distribution.
- **Intraday range ratio** = (day high − low)/open.
- **Gap size** (open vs previous close) — start-of-session risk.

## Why volatility matters intraday
- Stops sized in ATR adapt to the instrument's own noise (CH_22).
- Position size = risk budget ÷ (ATR × stop multiplier) (CH_21) — same risk per
  trade across symbols with different vol.
- Volatility clustering: measure today's vol relative to recent days to choose
  whether a strategy is allowed at all.

## Pseudo-code: ATR (Wilder)
```
tr = max(h-l, |h-c_prev|, |l-c_prev|)
atr = wilder_smooth(tr, n)   # seed = SMA of first n
```

## Pseudo-code: vol percentile
```
realized = rolling_std(log_returns, w=30)   # per bar
perc = rank(realized_t, hist_of_realized_last_250_bars)
```

## Usage guidance
- Always express stop and target distances in ATR units, not fixed ticks.
- If realized vol is extreme (top/bottom percentile), often tighten or skip trading
  (regime filter, CH_13/CH_14).
- Report vol percentile as a feature to models (CH_09) — very predictive intraday.

## Rules
- Compute ATR per symbol, per timeframe; never reuse across granularity.
- Stops below ATR×k get hit by noise; set k from backtest evidence, not guess.
