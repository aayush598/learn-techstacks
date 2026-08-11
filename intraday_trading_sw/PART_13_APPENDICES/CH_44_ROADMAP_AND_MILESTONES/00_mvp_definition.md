# 00 — MVP Definition

## Purpose
Define the smallest system that is genuinely useful and safe: a complete
research→paper-trading platform. (Live trading is a later milestone.)

## MVP scope (what to build first)
- Data: one market, a curated liquid symbol set, 1m bars, historic + real-time
  from one source class (CH_05, CH_06), validated and stored (CH_07, CH_08).
- Analysis: core indicators + features (CH_09, CH_10), session awareness (CH_02).
- Strategy: 1–3 rule-based strategies from the taxonomy (CH_13), defined in the
  signal language (CH_14).
- Backtest: event-driven engine with costs (CH_17), metrics + reports
  (CH_18), overfitting gate (CH_19).
- Risk: per-trade/daily/portfolio limits + breakers (CH_20–CH_23) — non-negotiable.
- Execution: OMS + simulator broker (CH_24, CH_25) for paper trading only.
- Platform: engine loop (CH_28), dashboard (CH_29), logging (CH_33).
- Ops: process management (CH_31), health/alert basics (CH_32), secrets
  (CH_34), backup (CH_35).
- QA: test pyramid (CH_36) + paper trading protocol (CH_37).

## Explicitly NOT in MVP
- Live broker orders, ML models, L2/tape strategies, multi-market, UI polish.

## MVP exit criteria
```
- data validation pass >= 99%
- indicators tested (batch == incremental)
- 1+ strategy passes overfitting checklist (CH_19/03)
- paper trading runs N sessions without anomalies (CH_37/01)
- all acceptance gates green (CH_36/02)
```

## Pseudo-code: MVP check
```
def is_mvp_done():
    return (paper_ok() and strategy_gated() and risk_enforced()
            and ops_healthy() and docs_complete())
```

## Rules
- No live money in the MVP — live is a post-MVP milestone (CH_37/02).
- Simplicity is a feature: fewer moving parts = fewer failure points (CH_00/02).
