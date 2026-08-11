# 00 — Target and Label Engineering

## Purpose
Define prediction targets precisely. The target determines everything the model
learns; a bad target makes a good model useless.

## Target types
1. **Direction over horizon h**: `up` if ret(t+1..t+h) > +θ, `down` if < −θ, else `flat`.
   - θ = cost threshold (commission + slippage + spread) so "up" means *profitable
     after costs*, not just positive.
2. **Trade-quality label**: for a candidate entry (t) with a fixed rule plan
   (stop/target), did the plan finish profitable? Labels = simulated outcome.
3. **Volatility target**: realized vol over next h bars (CH_15/02).

## Labeling rules (no look-ahead)
- Labels use data **strictly after** the feature time t.
- Horizon h and threshold θ are part of the dataset manifest (reproducibility).
- Skip/ignore labels that cross the session close (no overnight carry) unless
  the strategy explicitly allows it.

## Pseudo-code: direction label
```
def label(bar_t, future_bars, h, cost):
    ret = close[t+h]/close[t] - 1
    if   ret >  cost: return UP
    elif ret < -cost: return DOWN
    else:             return FLAT
```

## Class design choices
- **3-class (up/flat/down)** vs 2-class (drop flat): drop-flat models can bias
  probability mass; keep 3-class and handle imbalance (CH_15/01).
- Choose h to match the strategy's holding period (1m signals ⇒ h=1..5 bars).

## Robustness
- Compute labels on **adjusted** prices (CH_07/02) and exclude corporate-action
  days from target windows.
- Verify label distribution per period (drift in market regime shows up here).

## Rules
- Target definition is versioned and logged with every dataset.
- Never train direction models with targets that ignore trading costs.
- Document the h and θ in the model card (CH_16/03).
