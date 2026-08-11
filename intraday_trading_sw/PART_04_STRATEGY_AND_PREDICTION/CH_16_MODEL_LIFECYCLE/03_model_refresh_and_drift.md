# 03 — Model Refresh and Drift

## Purpose
Keep deployed models relevant as markets change, with automated detection,
scheduled retraining, and safe rollback.

## Types of drift to monitor
- **Feature drift**: distribution of inputs changes (e.g., volatility regime shift).
- **Prediction drift**: model's output distribution changes (P(up) always 0.6 = broken).
- **Target/label drift**: actual outcomes no longer match model assumptions.
- **Performance drift**: live metrics (calibration, hit rate, P&L) degrade vs baseline.

## Monitoring implementation
- Stream live features/predictions to monitoring (CH_32).
- Daily job compares last N days vs reference distribution (KS/PSI tests) and
  reports to alerting.

## Refresh strategy
- **Scheduled retraining**: e.g., weekly with a sliding window (data versions).
- **Event-triggered**: on drift alarm, structural change (symbol list, expiry),
  or large regime shift.
- **Rolling window**: always train on the most recent period (e.g., 6–12 months),
  validating on the most recent portion.

## Pseudo-code: drift check
```
psi = psi_score(live_pred_dist, reference_dist)
if psi > psi_threshold:
    alarm("prediction_drift", psi)
    trigger_retrain(job)
```

## Deployment & rollback
- Models are versioned artifacts (CH_16/01); deploy = switch registry pointer.
- **Shadow mode** first: run new model alongside current, compare outcomes on
  paper (CH_37), no orders.
- Keep the previous artifact; automatic rollback on performance alarm.

## Model card (required per artifact)
```
model_id, version, trained_at, data_ids, feature/target versions, hyperparams,
metrics, calibration report, drift status, deployment status, owner
```

## Rules
- Every live model has a model card and a rollback target.
- Drift alarms page a human (CH_30) — models do not silently self-deploy.
- Retraining must pass the same gates as the original (CH_16/02).
