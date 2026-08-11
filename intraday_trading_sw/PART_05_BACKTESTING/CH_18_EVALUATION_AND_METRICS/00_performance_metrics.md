# 00 — Performance Metrics

## Purpose
Define a standard set of performance metrics with exact formulas, so every
backtest and live report speaks the same language.

## Core metrics (define exactly)
- **Total return** = (end_equity / start_equity) − 1.
- **Net P&L** = realized+unrealized − all costs.
- **Trade count** and **round trips**.
- **Win rate** = winning trades / total trades (count-based).
- **Payoff ratio** = avg win / avg loss (magnitude-based).
- **Expectancy** = win_rate×avg_win − (1−win_rate)×avg_loss (per trade, after costs).
- **Profit factor** = gross profit / gross loss.
- **Max drawdown** = max peak-to-trough decline in equity (absolute and %).
- **Average holding time** (bars), **turnover** (volume traded / equity).

## Reporting conventions
- Report per strategy, per period, **with and without costs**.
- Metrics computed on the full backtest AND per rolling window (stability view).
- Per-session summary: best/worst day, distribution of daily P&L.

## Pseudo-code: expectancy
```
def expectancy(trades):
    w = [t.pnl for t in trades if t.pnl > 0]
    l = [t.pnl for t in trades if t.pnl <= 0]
    return mean(w)*len(w)/len(trades) - |mean(l)|*len(l)/len(trades)
```

## Which number to trust
- Expectancy and profit factor (they include magnitude).
- Max drawdown (survivability).
- Nothing else matters if costs make expectancy ≤ 0.

## Rules
- Win rate alone is meaningless (a 90% win rate can lose money).
- Report all metrics; cherry-picking undermines trust (CH_00/02).
- Metrics module is shared by backtest and live reporting (CH_18/03).
