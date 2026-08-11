# 00 — Anatomy of an Intraday Trading System

## Purpose
Give a complete map of the pieces that make up the software, how they relate,
and where each piece is documented in this resource.

## The six subsystems
1. **Data Subsystem** (PART_02)
   Acquires, cleans, stores, and serves market data (historic + real-time).
2. **Analysis Subsystem** (PART_03)
   Computes indicators, patterns, features, and market context.
3. **Strategy & Prediction Subsystem** (PART_04)
   Turns analysis into signals and probabilistic predictions.
4. **Backtest Subsystem** (PART_05)
   Evaluates strategies honestly before they are allowed to act.
5. **Risk Subsystem** (PART_06)
   Enforces limits on position size, loss, exposure, and behavior.
6. **Execution & Live Subsystem** (PART_07, PART_08)
   Places orders, manages the order lifecycle, runs the live engine, UI, alerts.

## Supporting subsystems (cross-cutting)
- Operations & monitoring (PART_09)
- Quality & testing (PART_10)
- Governance, compliance & ethics (PART_11)
- Open-source & community (PART_12)

## Component diagram (pseudo)
```
                     ┌────────────────────────────────────────────┐
  Exchanges/Brokers  │   LIVE PLATFORM (PART_08)                  │
  (feeds, orders)    │   Engine Loop ── Orchestrator ── Risk Gate │
        │            └───────┬────────────────┬──────────────────┘
        │ feeds              │                │ signals
        ▼                    ▼                ▼
  ┌──────────────────────────────────────────────────────────┐
  │  DATA (PART_02)        ANALYSIS (PART_03)    STRATEGY     │
  │  ingest → clean →      indicators →          rule/ML      │
  │  store → serve         features → context    → signal     │
  └──────────────────────────────────────────────────────────┘
        ▲                                      │
        │         BACKTEST (PART_05)           ▼
        └──── validate strategies ◄───  RISK (PART_06)
                                          enforce limits
```

## Minimal module list (build order)
1. `ingest` — pull data from sources (CH_05, CH_06)
2. `clean` — validate and normalize (CH_07)
3. `store` — local, self-hosted storage (CH_08)
4. `features` — engineering (CH_09)
5. `indicators` — computations (CH_10)
6. `signals` — rules + models (CH_14, CH_15)
7. `backtest` — evaluation (CH_17, CH_18, CH_19)
8. `risk` — limits and sizing (CH_20–CH_23)
9. `oms` — order management (CH_25)
10. `broker` — abstraction layer (CH_24)
11. `live` — engine loop (CH_28)
12. `ui` / `alerts` — interface (CH_29, CH_30)

## Rule
One subsystem per concern. Never let execution logic live inside data code or
vice versa. This keeps the system auditable and testable.
