# 02 — Momentum Indicators

## Purpose
Measure the *speed* of price change to time entries and detect divergences.

## Momentum indicator set
- **ROC / RSI / Stochastic**:
  - ROC(n) = (close_t − close_{t−n})/close_{t−n} × 100
  - RSI(n) = 100 − 100/(1+RS) (Wilder smoothing) — CH_10/00
  - Stoch %K = (close − LLn)/(HHn − LLn) × 100, %D = SMA3(%K)
- **MACD**: momentum of moving averages + histogram (crossing zero/signal).
- **Rate of change acceleration**: change of ROC (momentum of momentum).
- **Candlestick momentum**: consecutive up/down bars, body dominance.

## Divergence detection (price vs momentum)
- **Bullish divergence**: price makes lower low, RSI makes higher low →
  possible upward reversal. **Bearish divergence**: mirror.
- Implement with pivot detection on both series; only flag on *confirmed* pivots.

## Pseudo-code: RSI
```
def rsi(close, n=14):
    delta = diff(close); gain = max(delta,0); loss = max(-delta,0)
    avg_gain = wilder_smooth(gain, n); avg_loss = wilder_smooth(loss, n)
    rs = avg_gain / max(avg_loss, eps)
    return 100 - 100/(1+rs)
```

## Pseudo-code: divergence check
```
lows_p = pivots(close, lookback)   # local minima with k bars either side
lows_r = values_at(RSI, lows_p)
if len(lows_p) >= 2:
    if close[lows_p[-1]] < close[lows_p[-2]] and \
       RSI[lows_r[-1]] > RSI[lows_r[-2]]:
        return BULLISH_DIVERGENCE
```

## Usage guidance
- Momentum confirms entry timing; overbought/oversold alone are weak signals.
- Momentum *exhaustion* (huge RSI extreme + volume climax) often marks reversal.
- Use divergences as alerts, not standalone entries — they fail in strong trends.

## Rules
- Report RSI/Stoch as features with their window; never hardcode interpretation
  in the math layer — interpretation lives in strategy (CH_14).
- Momentum is mean-reverting at extremes but trending in the middle — respect regime.
