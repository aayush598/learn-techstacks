# 02 — Validation and Backtesting Loop

## Purpose
Close the loop between model metrics and *actual strategy outcomes*: a model is
only useful if the strategy built on it makes money after costs out-of-sample.

## The two evaluation tiers
1. **Model metrics** (CH_18): calibration, AUC, Brier, per-class metrics.
2. **Strategy-level backtest** (CH_17): feed model probabilities into the full
   strategy (with risk, costs, execution) and measure outcome.

Tier 2 is decisive. A "good" model can still lose money once costs/risk are in.

## Loop process (pseudo)
```
model = train(...)                 # CH_16/01
proba = model.predict_proba(...)   # on test window only
strategy = Strategy(manifest, proba_gate=model)   # probabilities drive entries/sizing
report = backtest(strategy, test_window, realistic_costs)
if report.sharpe < min_sharpe or report.net_pnl <= 0:
    reject(model); try_again_with(changes)
else:
    register(artifact, report)
```

## Probabilities → decisions mapping
- Threshold θ_p on P(up): below θ_p no trade (avoids marginal calls).
- Confidence bands: trade only in the top X% by predicted probability (top-decile).
- Size scales with confidence, capped by risk limits (CH_21).

## Pseudo-code: probability gate
```
p = model.proba(features_at(t))
if p > entry_threshold and strategy_rules_ok(ctx):
    qty = size_for(confidence=p, risk_budget=...)   # CH_21
```

## Rules
- Never deploy a model on the strength of model metrics alone.
- Every model evaluation ends with the full backtest of the surrounding strategy.
- Keep rejected models in the registry with reasons (learning, not shame).
