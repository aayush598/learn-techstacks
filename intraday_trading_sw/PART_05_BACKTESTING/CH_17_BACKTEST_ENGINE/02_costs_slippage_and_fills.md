# 02 — Costs, Slippage, and Fills

## Purpose
Model the real frictions of trading; unrealistic cost assumptions are the #1
reason backtests lie.

## Cost components (all must be modeled)
- **Commission/fees**: per order or per share/contract (broker schedule).
- **Taxes/stamp duty** (jurisdiction-specific; CH_39).
- **Spread**: crossing the bid-ask (CH_03/00).
- **Slippage**: fill vs reference price (liquidity-dependent).
- **Market impact**: your own order's effect (larger size, CH_26/02).
- **Financing/rollover** if positions held past close (avoid for intraday).

## Fill model tiers
1. **Conservative fixed**: fill = reference ± (spread_half + slip_tick). Simple.
2. **Liquidity-aware**: slippage scales with order size relative to recent volume
   (e.g., % of avg bar volume).
3. **Book-modeled**: use recorded L2 book to simulate walking the book (only with
   tick/L2 data, CH_06/03).

## Pseudo-code: conservative fill
```
def fill_price(side, ref, model):
    slip = model.spread_bp/2 + model.slip_bp(vol_ratio)   # bp on ref
    return ref * (1 + side*slip/1e4)   # buy fills higher, sell lower
```

## Cost sanity test
A strategy that makes money with zero costs must be re-checked with
**pessimistic** costs (e.g., 2× baseline). If it dies, it's a costs-game, not an edge.

## Parameter defaults (starting point, tune to broker)
- spread: use instrument's typical half-spread in bp.
- slippage: minimum 0.5–1 bp; higher for illiquid/volatile.
- commission: per broker schedule; include minimums per order.

## Rules
- Cost model is a single module shared by both backtest engines AND the paper
  trader (CH_37) — same assumptions everywhere.
- Report backtests with and without costs (transparency, CH_18/00).
- Slippage is asymmetric: exits (stops) slip more than entries.
