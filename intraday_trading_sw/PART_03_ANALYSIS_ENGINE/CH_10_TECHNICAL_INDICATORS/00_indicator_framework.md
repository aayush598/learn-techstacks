# 00 — Indicator Framework

## Purpose
Define a uniform, testable, dependency-light framework in which all technical
indicators are implemented, so results are consistent across backtest and live.

## Framework contract
- Input: a series of bars/values (ordered, timestamps aligned).
- Output: a series aligned to the same index (or per required convention).
- Every indicator exposes: warmup length, params, and a spec reference.
- Indicators are **stateless functions on arrays** for backtest use, plus
  **incremental variants** for live use (see below).

## Two computation modes
1. **Batch**: compute over a full series (backtest/training).
   `sma(close, 20) -> array`
2. **Incremental**: update on each new bar (live).
   `ema_state.update(close) -> value` with persistent state.

The incremental implementation must produce *identical* results to the batch
one for the same inputs (test this — QA gate, CH_36).

## Common formulas (canonical, avoid ambiguity)
- SMA(n) = mean of last n closes.
- EMA(n): `ema = α·close + (1−α)·ema_prev`, α = 2/(n+1); seed with SMA(n).
- RSI(n) = 100 − 100/(1 + RS), RS = avgGain/avgLoss (Wilder smoothing).
- ATR(n) = Wilder-smoothed true range; TR = max(h−l, |h−c_prev|, |l−c_prev|).
- MACD = ema12 − ema26; signal = ema9(MACD); hist = MACD − signal.
- Bollinger: mid = SMA(n); band = ±k·std(n).
- VWAP (day) = Σ(typical·vol)/Σ(vol), typical=(h+l+c)/3.

## Pseudo-code: batch EMA
```
def ema(x, n):
    alpha = 2/(n+1)
    out = [None]*len(x)
    seed = mean(x[:n])
    for i in range(len(x)):
        out[i] = seed if i==0 else alpha*x[i] + (1-alpha)*out[i-1]
    return out   # warmup = n
```

## Rules
- Every indicator has a numeric identity test against a hand-computed example (CH_36).
- NaN handling: warmup values are NaN, never 0 (zero poisons averages).
- Never compute indicators on unadjusted prices for models (CH_07/02).
- The indicator layer never knows about strategy or risk — it is pure math.
