# 02 — Regression Models

## Purpose
Predict continuous quantities that drive better decisions: expected return,
expected volatility, expected slippage, expected holding time.

## What to regress (more useful than raw price)
- **Volatility forecast** (of the next h-bar return): drives position sizing
  (CH_21) and stop calibration (CH_22).
- **Expected move / expected |return|**: event-day vol and range sizing.
- **Expected return** (harder, low signal): use cautiously; mostly for ranking.
- **Expected slippage/fill gap**: execution planning (CH_26).

## Models
1. Linear/Ridge — baseline, interpretable.
2. Random Forest / Gradient Boosting (CH_15/03) — strong defaults for tabular.
3. GARCH-style vol models — specialized; can be hand-built for volatility only.
4. Simple NN — optional later.

## Targets and transformations
- Vol targets: use |return| or squared return (noisy); smooth with rolling
  windows; log-transform to stabilize.
- Return targets: log-returns (CH_09/01).
- Clip/extreme targets (winsorize) to reduce outlier influence.

## Pseudo-code: volatility model
```
y = log(rolling_std(returns, h))            # target = next realized vol
model = Ridge(alpha=...)
model.fit(pipe.transform(X_train), y_train)
vol_forecast = exp(model.predict(pipe.transform(X_live)))
# feed vol_forecast into sizing (CH_21/01)
```

## Evaluation
- Vol models: RMSE on log-scale, correlation forecast vs realized, and the
  *resulting* sizing behavior (does it actually reduce per-trade risk?).
- Return models: correlation, directional hit rate, and top-decile backtest.

## Rules
- Volatility forecasting is easier and more valuable than direction — build it first.
- Validate on time-ordered data; vol changes across sessions (CH_19).
- A regression's output is a feature/input to risk — never a raw order size.
