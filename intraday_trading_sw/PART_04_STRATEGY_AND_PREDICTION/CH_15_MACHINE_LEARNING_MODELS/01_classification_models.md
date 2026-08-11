# 01 — Classification Models

## Purpose
Design models that predict the *direction class* (up/down/flat) or *trade
quality* (profitable/not) within a horizon.

## Targets (defined in CH_16/00)
- Direction: `up` if future return over h bars > +cost_threshold, `down` if < −t.
- Trade quality: `good` if a fixed R-rule would have made money.

## Model options (start simple)
1. **Logistic regression**: interpretable, stable, good baseline.
2. **Decision trees** (then boosted, CH_15/03): handle nonlinearity, missing values.
3. **Small neural nets**: only after baselines; need care + more data.
4. **k-NN / SVM**: rarely the right intraday choice; mostly for benchmarking.

## Training considerations
- **Class imbalance**: up/down may be near-balanced; flat target often rare —
  use weighted loss / class weights, evaluate with precision/recall, not accuracy.
- **Feature scale**: logistic needs scaling (CH_09/04); trees don't.
- **Regularization**: always — L1/L2 for linear, depth/min-samples for trees.
- **Probabilities must be calibrated** (CH_16/02) before they feed risk.

## Pseudo-code: logistic pipeline
```
pipe = FeaturePipeline(); pipe.fit(X_train)        # CH_09/04
model = LogisticRegression(C=reg, class_weight=w)
model.fit(pipe.transform(X_train), y_train)
# eval on time-ordered validation only (CH_19)
p = model.predict_proba(pipe.transform(X_val))
```

## Evaluation focus
- **Calibration**: Brier score, reliability diagram — do not trust raw sigmoid.
- **Ranking quality**: AUC, and — more important — the *profitability of the top
  decile* (the trades you'd actually take).
- **Cost awareness**: a prediction is only useful if edge > costs (CH_18).

## Rules
- Baseline must beat: constant predictor, and the rule strategy it augments.
- Never choose a model on validation metrics alone; validate the *strategy*
  around it via backtest (CH_16/02).
- Report per-class metrics; accuracy hides most of the story.
