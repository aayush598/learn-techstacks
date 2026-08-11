# 01 — Risk-Adjusted Metrics

## Purpose
Measure return *per unit of risk* — the only fair way to compare strategies of
different volatility.

## Metrics (define exactly)
- **Sharpe ratio** = mean(period_returns)/std(period_returns) × sqrt(annualization).
  For intraday: use the natural period (per-trade or per-session), report it.
- **Sortino ratio** = mean return / downside deviation (only negative returns).
  Better than Sharpe when upside variance shouldn't be penalized.
- **Calmar ratio** = annualized return / |max drawdown|.
- **Ulcer index / average drawdown**: how long/deep the pain is.
- **Skew & kurtosis** of returns: negative skew = tail risk (bad for you).
- **Value at Risk (VaR, 1-day, 95/99%)** and **Expected Shortfall** (CVaR):
  how bad is a bad day really.
- **Hit rate of daily P&L**: days above/below zero.

## Pseudo-code: Sharpe (per-session)
```
rets = session_returns  # net of costs
sharpe = mean(rets)/std(rets) * sqrt(sessions_per_year)
```

## Interpretation rules
- Sharpe < 0 after costs → reject.
- High Sharpe from few trades is not evidence (statistical significance, CH_18/02).
- Compare strategies on Sortino and Calmar as well — they penalize the risks
  that actually hurt traders.

## VaR/CVaR computation
```
sorted_rets = sort(session_returns)
var95   = percentile(sorted_rets, 5)          # 5% worst case
cvar95  = mean(sorted_rets[: <= var95])       # average of worst 5%
```

## Rules
- Always annualize with an explicit, documented convention.
- Report Sharpe with its trade/session count and period (context, not just a number).
- Include tail metrics; positive average with negative skew can still ruin you.
