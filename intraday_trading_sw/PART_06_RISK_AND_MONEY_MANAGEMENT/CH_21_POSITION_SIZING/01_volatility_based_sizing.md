# 01 — Volatility-Based Sizing

## Purpose
Normalize risk across instruments by sizing to a target amount of *volatility*,
so a 2% ATR stock and a 0.5% ATR stock risk the same amount.

## Formula (ATR-based)
```
qty = risk_amount / (stop_atr_mult × ATR)
```
where ATR = current ATR (per timeframe), stop_atr_mult = stops in ATR units
(CH_22/00). Equivalently: fixed-fractional with stop_distance = mult×ATR.

## Volatility targeting (portfolio level)
- Target portfolio risk = σ_target (e.g., daily vol budget).
- Scale total exposure so expected daily vol ≈ target:
```
scale = σ_target / σ_forecast
```
where σ_forecast comes from the vol model (CH_15/02) or realized vol.

## Pseudo-code: ATR sizing
```
def size_by_atr(equity, f, atr, stop_mult):
    risk = equity * f
    stop_dist = stop_mult * atr
    if stop_dist <= 0: return 0
    return floor(risk / stop_dist)
```

## Regime adjustments
- In high-vol regimes, ATR grows → size shrinks automatically (good).
- Optional floor/ceiling: don't let size swing more than X% between sessions
  without reason (avoid overtrading after one quiet day).

## Rules
- Use the *same* ATR and timeframe the stop rule uses (consistency, CH_22).
- Volatility targeting caps the *portfolio*, not just single trades (CH_20/02).
- Document ATR period and the sizing formula per strategy manifest (CH_13/00).
