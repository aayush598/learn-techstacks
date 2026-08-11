# 03 — Arbitrage and Spread Trading

## Purpose
Trade relative value between related instruments (futures vs spot, correlated
pairs, index constituents) where the *spread* — not direction — is the signal.

## Families
1. **Cross-sectional / pairs**: two cointegrated instruments; trade the spread
   when it deviates, expect convergence.
2. **Futures vs spot (basis)**: convergence at expiry; calendar spreads between
   expiry months.
3. **Index vs constituents (stat arb, optional)**: index movement vs a basket —
   requires multiple legs; advanced.
4. **ETF/ETN dislocations**: NAV vs price mismatches.

## Data prerequisites
- Simultaneous, aligned bars for ALL legs (same timestamps, no asynchronicity).
- Cointegration/ratio modeling requires careful stationarity testing (CH_18/CH_19).

## Strategy template (pairs)
- **Spread** = log(pA) − β·log(pB) (β estimated on a rolling window).
- **Entry**: spread z-score < −k (buy spread) or > +k (sell spread).
- **Exit**: z-score returns to ~0; **Stop**: z beyond k_stop or ratio regime break.

## Pseudo-code: z-score entry
```
spread = log(pA) - beta*log(pB)
z = (spread - mean(spread, w)) / std(spread, w)
if z < -k and stationary(pair):  BUY spread   # long A short B
elif z > +k and stationary(pair): SELL spread
```

## Risks
- **Non-convergence**: the relationship can break structurally — stop is mandatory.
- **Execution risk**: legs must be filled together; use leg-level market orders
  and re-quote logic.
- **Costs**: double commissions/slippage eat thin spreads; only trade where
  expected z-reversion ≫ costs.
- **Liquidity mismatch**: one leg illiquid = silent killer.

## Rules
- Re-estimate and re-test cointegration on a rolling basis; never assume it holds.
- Pairs/spread strategies need *aligned* data pipelines (CH_06).
- Backtest costs as double-sided; if the edge disappears with costs, reject it.
