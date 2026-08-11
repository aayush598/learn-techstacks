# 03 — Overfitting Defense Checklist

## Purpose
A concrete, auditable checklist that every strategy must pass before it is
allowed near paper trading. Use it as a gate, not a suggestion.

## The checklist
- [ ] Random train/test split was NOT used; splits are time-ordered with purging.
- [ ] Held-out test set exists and was evaluated exactly once.
- [ ] Walk-forward analysis (CH_19/01) passed: median positive, ≥60% windows positive.
- [ ] Costs and slippage modeled pessimistically (CH_17/02); strategy survives 2× costs.
- [ ] No look-ahead: signal→fill at next bar; canary test passes (CH_17/03).
- [ ] Statistical significance: bootstrap CI of expectancy excludes 0 (CH_18/02).
- [ ] Multiple-testing adjusted: the number of tried configs is disclosed and
      the best-of-N inflation is accounted for (CH_19/02).
- [ ] Parameter sensitivity: perturbing params ±20% doesn't collapse performance.
- [ ] No data leakage: scalers/pipelines fit on train only (CH_09/04);
      corporate-action/calendar handled (CH_07/02).
- [ ] Regime coverage: tested across up/down/range and high/low vol (CH_17/03).
- [ ] The strategy's edge is *explainable* in plain language (edge source,
      CH_13/00) — if you can't explain why it works, treat it as luck.
- [ ] Trade count ≥ 30–100 with stable metrics across windows.
- [ ] Report includes every assumption (CH_18/03).

## Red flags (automatic rejection)
- Backtest Sharpe > 3 with daily re-tuning — almost always overfit.
- Metrics improve monotonically as you add conditions — you're curve-fitting.
- Strategy only works on one specific symbol/period.
- Cost sensitivity flips sign — costs game, not edge.
- Any unexplained jump in equity curve around a known event — investigate first.

## Pseudo-code: gate
```
def approve_for_paper(s):
    return all(check(s) for check in OVERFITTING_CHECKS) and not any(red_flag(s))
```

## Rules
- The checklist result is recorded in the strategy's artifact (CH_16/01).
- Paper trading (CH_37) is the next gate; this checklist is the door to it.
