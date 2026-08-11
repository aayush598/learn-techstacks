# 03 — Reporting Dashboards

## Purpose
Produce transparent, reproducible performance reports that any reader — including
a skeptic — can audit.

## Report contents (required sections)
1. **Header**: strategy id/version, engine type (CH_17), data ids, cost model,
   period covered, date generated, git/artifact version.
2. **Equity curve** (chart) + per-session P&L histogram.
3. **Core metrics table** (CH_18/00) — with and without costs.
4. **Risk-adjusted table** (CH_18/01): Sharpe, Sortino, Calmar, VaR, CVaR, skew.
5. **Trade statistics**: win rate, payoff, expectancy, profit factor, holding
   time distribution, worst trade, average slippage.
6. **Drawdown analysis**: max DD, time-to-recover, DD by month/session phase.
7. **Significance section** (CH_18/02): CIs, permutation p, multiple-testing
   adjustment, out-of-time replication.
8. **Regime breakdown**: performance in trending vs range vs high/low vol.
9. **Assumptions list**: every fidelity/cost assumption (CH_17/02, CH_17/03).
10. **Known limitations & next steps**.

## Output formats (self-hosted)
- HTML report (self-contained, viewable offline) generated from JSON data.
- CSV/JSON exports for further analysis.
- Deterministic: same inputs → identical report bytes.

## Pseudo-code: report generator
```
data = evaluate(strategy, engine, datasets, costs)
report = {
  header: make_header(strategy, engine, datasets),
  metrics: core_metrics(data), risk: risk_metrics(data),
  significance: significance_tests(data),
  regime: regime_breakdown(data),
  assumptions: collect_assumptions(engine),
}
render_html(report, out_path)
```

## Live reporting
- The same report generator runs nightly on live results (CH_32) — live vs
  paper vs backtest side by side (drift detection, CH_16/03).

## Rules
- Reports are versioned artifacts, stored with the strategy (reproducibility).
- Every number in the report must trace to a defined formula (CH_18/00–01).
- A report is not honest unless it shows the costs and the failed periods too.
