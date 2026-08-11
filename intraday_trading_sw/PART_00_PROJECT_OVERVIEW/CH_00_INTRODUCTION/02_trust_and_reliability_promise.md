# 02 — Trust and Reliability Promise

## Purpose
Define what it means for this software to be *trustworthy*, and the engineering
practices that earn that trust. Trust is the product's real value.

## What users are promised
1. **Honest results**: backtests and live results use the same realistic costs.
   We never inflate performance.
2. **Transparency**: every computation is explainable and auditable (open source,
   readable logs, reproducible runs).
3. **Safety**: risk limits are enforced in code and cannot be bypassed by accident
   or emotion.
4. **No secret sauce claims**: we disclose what models do, what they can't do,
   and their uncertainty.
5. **Determinism**: same inputs produce same outputs, so users can verify us.

## Engineering practices that build trust
- **Reproducibility**: fixed seeds, pinned data versions, recorded environments.
- **Testing**: unit, integration, system, and paper-trading gates (PART_10).
- **Audit trail**: append-only logs of decisions with reasons (PART_09/CH_33).
- **Validation**: walk-forward and out-of-sample testing before any deployment.
- **Fail-safe**: on any anomaly the system halts or goes safe, never acts wild.
- **Security**: secrets never in code; least-privilege access (PART_09/CH_34).

## Trust model diagram (pseudo)
```
Data -> Validation -> Features -> Signal -> Risk gate -> Execution -> Audit log
        (reject bad)  (no leak)   (explain)  (enforce)    (reconcile) (forensic)
Every stage can be inspected and replayed. Nothing is a black box.
```

## Rules
- Never present a backtest without its assumptions (slippage, costs, period).
- Never present a prediction without a probability/confidence and uncertainty.
- Never hide a failure; log it and show it in monitoring.
