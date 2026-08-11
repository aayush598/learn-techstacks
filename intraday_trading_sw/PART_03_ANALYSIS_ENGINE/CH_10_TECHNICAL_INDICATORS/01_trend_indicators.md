# 01 — Trend Indicators

## Purpose
Quantify the direction and strength of a trend; the "context" layer that
determines whether momentum or mean-reversion strategies are appropriate.

## Trend indicator set
- **SMA / EMA family**: baseline; crossovers of fast/slow define trend shifts.
- **ADX** (Average Directional Index): trend *strength* (not direction).
  ADX > threshold ⇒ trending regime; below ⇒ range regime.
- **+DI / −DI**: direction of up/down pressure; crossovers give direction.
- **Moving-average ribbon / alignment**: all MAs aligned up = strong uptrend.
- **Linear regression slope**: statistical trend over a window.
- **Higher-timeframe trend**: e.g., 15m close vs 15m SMA(20) as the session trend
  filter (context for 1m triggers, CH_04/02).

## Regime classification (important for strategy gating)
```
regime = TRENDING_UP / TRENDING_DOWN / RANGE
decision = if ADX strong and +DI > -DI: TRENDING_UP
           elif ADX strong and -DI > +DI: TRENDING_DOWN
           else: RANGE
```

## Pseudo-code: ADX core
```
for bar in window:
    +DM = up_move if (h-h_prev) > (l_prev-l) and (h-h_prev) > 0 else 0
    -DM = down_move if (l_prev-l) > (h-h_prev) and (l_prev-l) > 0 else 0
    TR  = max(h-l, |h-c_prev|, |l-c_prev|)
    smooth (Wilder) +DM, -DM, TR
    +DI = 100*sm(+DM)/sm(TR); -DI = 100*sm(-DM)/sm(TR)
    DX  = 100*|+DI - -DI| / (+DI + -DI)
ADX = Wilder_smooth(DX, n)
```

## Usage guidance
- Trends are slow: use trend indicators as *filters*, not entry triggers.
- Never trade against the session trend without a reason (gap, extreme).
- Exit signals also respect trend: in an uptrend, exits are weaker (let winners run).

## Rules
- Always pair a trend measure with a regime label for strategy gating (CH_14).
- Document lookback; trends on 1m are noisy — prefer 15m+ for context.
- Test ADX/DI on trending vs ranging synthetic series (CH_36).
