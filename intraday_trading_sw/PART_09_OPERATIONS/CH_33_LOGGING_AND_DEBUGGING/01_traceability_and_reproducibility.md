# 01 — Traceability and Reproducibility

## Purpose
Make it possible to answer, for any decision: *what happened, why, with what
data, and can it be replayed?*

## Traceability chain
- Every trade links: strategy/manifest version → model artifact id (CH_16/03) →
  dataset version → features version → signal (reasons) → risk decision → order
  events → fills → P&L.
- IDs flow through every record (correlation id per decision).

## Pseudo-code: decision id
```
decision_id = uuid()                       # one id for the whole chain
signal = {id: decision_id, ...}
order  = {id: decision_id, ...}
fill   = {id: decision_id, ...}
# journal records share decision_id -> reconstruct full story
```

## Reproducibility requirements
- Backtest/training runs record: git commit, data ids, config, seeds, runtime
  (CH_16/01). Rerun with the same record → identical outputs.
- Live decisions replayable: given stored bars + manifests + model, the engine
  produces the same decisions (replay harness in QA, CH_36).

## Incident reconstruction workflow
1. Find decision_id / time window in the journal.
2. Pull the exact data (lineage, CH_00/01) that fed the decision.
3. Replay the decision through the engine (deterministic, CH_28/00).
4. Compare replayed vs actual; document the discrepancy or confirm.

## Rules
- Every artifact (model, dataset, report) is immutable once registered.
- Correlation ids are mandatory on all decision-path records.
- Replay must be runnable with one command (documented in CH_37 tooling).
