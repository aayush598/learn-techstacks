# 00 — Market Participants and Liquidity

## Purpose
Understand who trades, why, and how that shapes price behavior. Strategies must
fit the market's structure, not fight it.

## Participant classes (intraday focus)
- **Market makers / liquidity providers**: quote both sides, earn spread; smooth
  price, profit from volume.
- **Retail day traders**: momentum, breakout, mean reversion; small size, high
  turnover; often the "herd" whose flows create moves and reversals.
- **Institutional / algo desks**: TWAP/VWAP execution, portfolio rebalancing,
  program trades; create large, slow, directional pressure.
- **Hedgers / arbitrageurs**: keep prices in line across venues and derivatives.
- **High-frequency traders**: front-run/scan and add liquidity in microseconds.

## What each participant means for us
- Liquidity is not constant: it clusters near round numbers, opening/closing,
  and news. Thin markets → slippage and false signals.
- Momentum strategies ride the imbalance between informed flow and passive flow.
- Mean-reversion works in ranging, liquid markets; dies in strong trends.

## Liquidity measures
- **Spread**: ask − bid. Tighter = better execution.
- **Depth**: size available at best bid/ask (order book).
- **Volume / turnover**: trades per unit time.
- **Market impact**: how much your own order moves price.
- **Resilience**: how fast price recovers from a large print.

## Steps to build participant/liquidity awareness into the software
1. Record bid/ask spread and depth per bar (if available) (CH_06, CH_03).
2. Compute a liquidity score per symbol/time (features in CH_09).
3. Only trade symbols and sessions where liquidity score passes a threshold.
4. Model impact in the execution layer (CH_26).

## Rules
- Never trade illiquid instruments with a large order and a tight stop.
- Prefer liquid, high-turnover instruments for intraday strategies.
- Rank watchlist by average daily volume and average spread, not by buzz.
