# 03 — Symbol Universe and Watchlist Selection

## Purpose
Define, score, and maintain the tradable universe — deciding *which* symbols
the system watches and trades. A curated universe improves signal quality,
data cost control, and execution reliability (CH_05/01).

## Selection criteria (score each symbol)
- **Liquidity**: average dollar volume and spread over recent sessions — the
  primary filter (CH_02/00).
- **Volatility**: enough intraday range to trade, not so much that slippage and
  risk overwhelm the edge (CH_20/01).
- **Correlation**: avoid a watchlist of highly-correlated names — diversification
  across groups (CH_20/02).
- **Data availability**: reliable, clean feed and history (CH_05, CH_07).
- **Broker support**: order types and margin the broker supports (CH_24/00).
- **Event proximity**: earnings, economic data, roll windows — an event-aware
  calendar (CH_02/03) flags names to pause or de-risk.

## Scoring approach
```
score = w1*liquidity_rank + w2*volatility_rank - w3*correlation_penalty
        + w4*data_quality_rank + w5*bidask_health
tier_1: top N   -> actively traded
tier_2: next N  -> standby/watch
tier_3: others  -> research only (CH_13/02 paper)
```

## Steps to maintain
1. Score from recent realized data (volume, spread, range) — recompute
   periodically (e.g., weekly or monthly).
2. Publish the universe as a versioned artifact (CH_08) the rest of the system
   reads (features, backtests, live).
3. Review drift: demote symbols whose liquidity/quality degraded; promote
   candidates that improved.

## Rules
- **Survivorship bias** (CH_15/00, CH_19): score candidates from *realized*
  data available at the time; a universe chosen from today's winners bakes in
  look-ahead. Backtest on the universe as it was, not as it is.
- Never trade a symbol whose data/broker support isn't verified (CH_05/02).
- Pause symbols in event windows unless the strategy explicitly handles them.
- Universe changes are reviewed and versioned, not silently applied to
  backtests.
