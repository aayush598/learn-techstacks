# 04 — Reinforcement Learning: Introduction

## Purpose
Explain when RL is (rarely) worth it for intraday, and how to keep it honest if
used. Default recommendation: start with rule-based + supervised ML instead.

## What RL would do
Learn a policy π(state) → action (enter/exit/size) by maximizing cumulative
reward in a simulated market environment.

## Why intraday RL is hard (honest risks)
- **Non-stationary environment**: the "true" transition dynamics shift daily.
- **Reward misspecification**: naive reward (P&L) leads to dangerous behavior
  (overtrading, maximizing variance).
- **Cost blindness**: RL explores orders; costs must be in the reward or it will
  churn.
- **Sample inefficiency & overfitting**: agents memorize the training tape.
- **Hard to audit**: a policy is a black box; compliance demands explainability.

## If pursued (guardrail framework)
1. **Environment = the backtester** (CH_17) with realistic costs/slippage.
2. **State** = the same feature vector used elsewhere (CH_09), not raw prices.
3. **Reward** = risk-adjusted: e.g., P&L − λ·|turnover| − κ·drawdown_penalty.
4. **Validation**: train on years A–B, test strictly on later period C (CH_19).
5. **Comparison gate**: the RL policy must beat the supervised/rule baseline
   out-of-sample *after costs* or it is rejected.
6. **Action constraints**: embed risk limits in the action space (max size,
   no-hold-through-close) so the agent cannot learn to violate them.

## Pseudo-code: environment reward
```
def reward(step):
    pnl    = position_pnl(step)
    churn  = |orders_executed(step)| * cost_per_order
    return pnl - lam*churn - kappa*max(0, -cum_pnl)
```

## Verdict
- Build rule + supervised ML first; RL is a research add-on behind the same
  strategy interface, gated by the comparison rule above.

## Rules
- Never run an RL agent live without a hard risk layer between it and orders.
- RL results are presented with full environment assumptions (CH_17/03).
