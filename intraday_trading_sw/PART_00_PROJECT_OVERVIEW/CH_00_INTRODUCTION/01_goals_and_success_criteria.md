# 01 — Goals and Success Criteria

## Purpose
Turn the vague ambition "profitable intraday software" into measurable,
engineering-grade goals.

## Primary goals
1. Build a complete, self-hosted intraday trading system from this resource alone.
2. Make every stage verifiable (data → signal → backtest → live) with numbers.
3. Keep external dependencies minimal so the system is portable and trustworthy.
4. Protect capital first: risk management is a hard, non-negotiable layer.
5. Open source: anyone can inspect, audit, extend, and reuse the system.

## Success criteria (SMART, measurable)
- **Data**: 100% of ingested bars pass validation checks before use.
- **Backtest fidelity**: simulated fills assume realistic slippage + commission
  and can be re-run deterministically (same input → same result).
- **Signal quality**: at least one strategy passes walk-forward validation with
  positive expectancy *before* it may touch paper trading.
- **Risk**: no single trade risks more than a configured maximum (e.g., 0.5–1%
  of capital); enforced by code, not by discipline alone.
- **Reliability**: live engine has ≥ 99.5% scheduled-time uptime during market
  hours across a monitored quarter.
- **Trust**: full audit trail — every signal, order, fill, and risk decision is
  logged and reproducible.

## Metrics that define "good" (definition of done per layer)
| Layer | Definition of done |
|---|---|
| Data | Validation pass rate ≥ 99%; gaps flagged and handled |
| Features | Every feature has a spec, test, and no look-ahead |
| Signals | Deterministic; latency budget met; no NaN leaks |
| Backtest | Slippage/commission modeled; no look-ahead; reproducible |
| Risk | Limits enforced by code; breach = alarm + auto-halt |
| Execution | Order state machine always consistent; reconciliation clean |
| Ops | Health checks green; alerts fire on anomalies |

## Anti-goals (guardrails)
- Chasing ever-higher backtest returns at the cost of realism.
- Adding dependencies when a standard-library solution suffices.
- Going live before paper-trading milestones pass.
