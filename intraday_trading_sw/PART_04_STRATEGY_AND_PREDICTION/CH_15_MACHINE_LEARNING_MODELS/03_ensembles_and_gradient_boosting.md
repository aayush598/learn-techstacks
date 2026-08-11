# 03 — Ensembles and Gradient Boosting

## Purpose
Use ensemble methods — the practical workhorses of intraday tabular ML — with
guardrails against their main failure mode: overfitting.

## Why ensembles win on tabular features
- Bagging (Random Forest): reduces variance, robust to outliers/noise.
- Boosting (GBM): reduces bias, captures interactions; needs regularization.
- Blend/stack: combine a linear baseline + a tree model — often the best
  robustness/performance balance.

## Guardrails (mandatory)
- **Strong regularization**: depth ≤ 5, min_samples_leaf decent size,
  subsample/colsample < 1, low learning rate + early stopping.
- **Early stopping on validation** (time-ordered, CH_19) — never on the training loss.
- **Fixed seed** + limited hyperparameter space (a few dozen configs max).
- **Compare to baseline** (logistic / rule strategy): boosters that don't beat
  the baseline by a meaningful margin are not deployed.

## Pseudo-code: GBM training
```
model = GBM(
    learning_rate=0.02, max_depth=4, min_samples_leaf=50,
    subsample=0.8, colsample=0.8, n_estimators=2000)
model.fit(X_train, y_train, eval_set=(X_val, y_val),
          early_stopping_rounds=100, verbose=False)
```

## Ensemble/pool design
- Keep multiple candidate models per strategy; a **model pool** with versioned
  artifacts (CH_16/03) lets you A/B and roll back safely.
- Blend by averaging calibrated probabilities, not raw logits.

## Pseudo-code: simple blend
```
p_blend = 0.5*logreg.predict_proba(X) + 0.5*gbm.predict_proba(X)
```

## Rules
- Hyperparameter search is done on training data with early stopping on
  validation; final selection on a *held-out* out-of-time window (CH_19).
- Log every model's params, features, and validation metrics (CH_16).
- If an ensemble overfits the validation window, it will betray you live — see CH_19.
