# 03 — Post-Session Review and Trading Journal

## Purpose
Turn every session's results into improvements: a structured end-of-day review
and a trading journal that connects decisions, emotions, and outcomes — closing
the loop from live results back to research (CH_00/03, CH_23/02).

## What to capture per session (auto + manual)
- **Plan vs actual**: intended strategy/symbols/risk vs what executed.
- **Execution quality**: slippage, partial fills, rejections, latency (CH_27/02).
- **Missed setups**: signals that fired but weren't taken — and why.
- **Risk discipline**: did any trade violate sizing/stops/limits (CH_21, CH_22)?
- **Decision log**: for discretionary overrides — what, why, context.
- **Session notes**: market regime, news, state (focused/fatigued).

## Review workflow (end of day)
1. Auto-generate a session report (metrics from CH_18/03 + execution logs).
2. Compare actual vs plan; flag deviations for the human.
3. Journal: fill notes, tag mistakes by category (process, execution, sizing,
   psychology).
4. Weekly review: group tags, count repeated mistakes, pick 1-2 process fixes.

## Pseudo-code: deviation report
```
def review(plan, actual):
    for (strat, symbol) in plan.trades:
        a = actual.trades.get((strat, symbol))
        if not a: yield MISSED
        elif a.slippage > threshold(a.symbol): yield EXECUTION_ISSUE
        elif a.risk_violation(a): yield RISK_VIOLATION
    yield summary_metrics(actual)
```

## Rules
- Review daily while memory is fresh; act weekly.
- Tag mistakes as **process** (fixable in code/config) vs **judgment**
  (fixable in discipline); a repeatable judgment mistake becomes a rule or an
  automated guard (CH_23/02).
- The journal is confidential, honest, and never used to blame — it feeds
  learning (CH_40/00).
- Log everything automatically; never rely on memory (CH_33/00).
