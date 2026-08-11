# 04 — Feature Scaling, Selection, and Pipelines

## Purpose
Define how raw features become model-ready data: scaling, handling missing
values, selection, and a single reproducible pipeline.

## Scaling
- **Tree-based models**: scaling unnecessary (splits are threshold-based).
- **Linear/neural models**: standardize (z-score) or robust-scale (median/IQR).
- **Critical**: fit scalers **on training data only**; apply the same transform to
  validation/test. Leaking scaler statistics = look-ahead bias.

## Missing values
- Policy per feature (CH_09/00): forward-fill safe lag features; drop rows with
  too many missing; never impute with future values.
- Models must tolerate NaN (tree splits can route NaN) or use explicit sentinel.

## Feature selection
- **Filter**: drop constants, near-duplicates (correlation > 0.95), high-missing.
- **Wrapper/model-based**: importance from a quick tree model; keep top-K.
- **Domain gate**: keep interpretable, documented features (CH_09/00).
- Beware: intraday features are highly correlated; aggressive dedup helps.

## Pipeline design (single source of truth)
```
fit(X_train):     learn scaler stats, imputation, selection mask
transform(X):     apply learned transform  (stateless after fit)
persist:          save pipeline artifact + feature order
apply_live(bar):  same transform on live feature vector
```
The *same* pipeline object must serve training, backtest, and live (CH_16).

## Pseudo-code: pipeline contract
```
class FeaturePipeline:
    def fit(self, df_train): ...      # computes stats/masks
    def transform(self, df) -> arr: ... # returns ordered matrix
    def save(self, path): ... ; def load(path): ...
```

## Rules
- One pipeline artifact per model version; train/test/live always use it.
- Log feature order with the artifact (models break silently on reorder).
- Re-run selection on data refresh; document what changed and why.
