# 01 — Training Pipeline

## Purpose
Define a reproducible, auditable pipeline that turns stored data into versioned
model artifacts.

## Pipeline stages
1. **Data version selection**: choose dataset (symbols, period, features version,
   target version) — resolved to exact artifact ids.
2. **Split** (time-ordered, CH_19/00): train / validation (early stopping,
   tuning) / held-out test (final, once).
3. **Feature pipeline fit** (CH_09/04): scaler/imputation/selection on train only.
4. **Model training** (CH_15) with fixed seed and logged hyperparameters.
5. **Calibration** (CH_16/02) on validation.
6. **Evaluation** (CH_18, CH_19): metrics + strategy backtest around the model.
7. **Artifact packaging**: model + feature pipeline + manifest (version, data ids,
   params, metrics, model card) → single artifact file.
8. **Register** in the model registry (SQLite table).

## Pseudo-code: pipeline runner
```
def train(job):
    ds   = load_dataset(job.dataset_id)
    tr, va, te = time_split(ds, job)           # CH_19/00
    pipe = FeaturePipeline(); pipe.fit(tr.features)
    model = build(job.model_type, job.params)
    model.fit(pipe.transform(tr.X), tr.y, eval=va)
    calibrator.fit(model.proba(va.X), va.y)
    metrics = evaluate(model, pipe, te)        # CH_18
    art = package(model, pipe, calibrator, job, metrics)
    registry.register(art)
    return art.id
```

## Reproducibility requirements
- Record: code version, data ids, feature/target versions, seeds, hyperparams,
  runtime environment, start/end times, host.
- A training run must be repeatable from this record (determinism tests, CH_36).

## Job configuration (YAML)
```
train_job:
  dataset: ds_v7
  model: gbm
  params: { lr: 0.02, depth: 4, ... }
  seed: 42
  split: { train_end: 2025-12-31, val_end: 2026-04-30, test_end: 2026-07-31 }
```

## Rules
- The test (held-out) set is touched exactly once per model.
- Every artifact stores its own manifest; no artifact is deployed without one.
- Data drift / refresh (CH_16/03) re-triggers this pipeline automatically.
