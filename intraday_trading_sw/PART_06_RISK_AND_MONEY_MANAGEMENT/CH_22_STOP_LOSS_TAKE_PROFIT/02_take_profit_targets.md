# 02 — Take-Profit Targets

## Purpose
Define where a trade's thesis is complete, converting paper profit into cash
before the market takes it back.

## Target methods
1. **Risk-reward multiple (R-multiple)**: target = entry ∓ R×stop_dist
   (e.g., R=2). Simple; pairs with the strategy's payoff design.
2. **Structure target**: next resistance/support, volume-profile node, previous
   swing, opening-range opposite side (CH_11/01, CH_10/04).
3. **VWAP / fair-value**: mean reversion targets the anchor (CH_13/01).
4. **Volatility-expansion target**: entry ∓ k×ATR projected from the breakout
   level.
5. **Trail to target**: if no fixed target, trail (CH_22/01) and let the market
   define the exit.

## Pseudo-code: R-multiple target
```
target = entry + side * R * stop_dist     # R from manifest (CH_13/00)
```

## Partial takes (optional, configurable)
- Take 50% at R=1 (bank it), trail the rest — reduces regret variance.
- Must be modeled in backtest exactly as configured (CH_17/03).

## Interaction with stops
- Target and stop are both fixed at entry (trade plan, CH_14/02).
- Asymmetry: if R<1, win rate must be high; if R>2, win rate will be lower —
  the payoff/win-rate trade-off (CH_18/00).

## Rules
- Targets are set at entry, recorded, and only changed by a written invalidation
  rule (never "let it run" impulse).
- A target at a structure level is preferred over a round number.
- Verify target achievability in backtest with realistic fills (CH_17/02).
