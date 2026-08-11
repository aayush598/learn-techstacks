# 00 — Welcome and Scope

## Purpose
Define what this resource is, what it builds, and what it deliberately does NOT
cover, so that anyone starting from this directory has the same mental model.

## Scope — what the software will do
- Ingest market data (historic and real-time) for intraday instruments.
- Clean, validate, store, and manage that data locally (self-hosted).
- Compute technical indicators, patterns, and engineered features.
- Generate trading signals using rule-based logic and machine-learning models.
- Predict favorable intraday outcomes with calibrated probabilities.
- Backtest strategies honestly and report performance.
- Enforce risk limits and position sizing before any execution.
- Execute orders through a broker abstraction layer (paper or live).
- Run a live platform: engine loop, dashboard, alerts, monitoring, logging.

## Out of scope (deliberately)
- A promise of profits. No system can guarantee earnings.
- Financial or investment advice.
- High-frequency/low-latency HFT-grade market making.
- Multi-currency global coverage in the MVP (one market first, then extend).
- Closed-source, proprietary, or paid SaaS features.

## Non-goals
- Predicting exact future prices (impossible). We predict *probabilistic* direction
  and favorable conditions only.
- Replacing the trader's judgment. The software is a decision-support tool.

## Reference
- `../CH_01_SYSTEM_ANATOMY/00_anatomy_of_an_intraday_trading_system.md`
- `PART_13/CH_44/00_mvp_definition.md`
