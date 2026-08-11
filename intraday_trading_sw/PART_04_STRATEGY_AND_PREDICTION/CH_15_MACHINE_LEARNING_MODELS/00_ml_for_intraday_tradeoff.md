# 00 — ML for Intraday: Trade-offs

## Purpose
Decide honestly *whether* to use ML and how, given intraday's unique pitfalls
(noise, non-stationarity, tiny edge).

## When ML adds value vs when it hurts
| Situation | Verdict |
|---|---|
| Rule strategy already works; ML might tune the edge | Try ML *after* a baseline exists |
| No baseline, hoping ML "finds" edge | No — find an edge first |
| Predict direction vs just filtering | Often better as a *filter* than a trader |
| Very noisy 1m targets | Prefer longer horizons / smoothed targets |
| Tiny dataset | No — ML will overfit |

## Honest expectations
- Intraday returns are near-random; realistic ML edges are small (e.g.,
  51–55% accuracy, or modest return-per-trade improvement).
- A model that looks great in-sample is usually overfit (CH_19).
- ML's real win intraday: **better risk/exit decisions and position sizing**
  (predict volatility, trade quality) rather than pure direction.

## Key intraday-specific concerns
- **Non-stationarity**: market behavior drifts daily; models must be refreshed
  and monitored for drift (CH_16/03).
- **Label noise**: labels built on future returns are noisy; choose robust targets
  (CH_16/00).
- **Survivorship/selection**: model trained on today's watchlist may not apply
  tomorrow — retrain and re-validate on new symbols.
- **Temporal leakage**: random CV is forbidden; only time-ordered validation
  (CH_19).

## Model-tier architecture (dependency isolation)
```
features (CH_09) -> pipeline (CH_09/04) -> model (CH_15) -> calibrator -> signal
model interface: fit(X,y,meta) | predict_proba(X) | save/load | importance()
```
Any ML library lives *only* behind this interface; swappable.

## Pseudo-code: model interface
```
class Model:
    def fit(self, X_train, y_train, w=None): ...
    def predict_proba(self, X) -> np.array   # P(up), P(down)
    def predict(self, X) -> labels
    def save(self, path); def load(path)
    def feature_importance(self) -> dict
```

## Rules
- Never deploy ML without: time-ordered validation, calibrated probabilities,
  drift monitoring, and a rule-based fallback.
- The output is a *probability* that flows into risk, never a raw bet size.
