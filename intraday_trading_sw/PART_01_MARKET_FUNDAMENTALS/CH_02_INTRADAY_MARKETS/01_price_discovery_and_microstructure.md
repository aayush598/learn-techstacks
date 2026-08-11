# 01 — Price Discovery and Market Microstructure

## Purpose
Explain how prices actually form at the micro level, so the signal engine can
interpret price action correctly instead of treating price as a pure random walk.

## Price discovery basics
- Price is the point where supply and demand clear. It is continuously
  re-discovered as new information arrives.
- Trades occur at the limit prices that buyers/sellers have resting on the book;
  a market order "walks the book" and moves price through levels.
- The *sequence* of trades (the "tape") carries information: aggressive buys vs
  sells (whether the taker crossed the spread), size, and timing.

## Key microstructure concepts
- **Taker vs maker**: taker crosses the spread (pays liquidity), maker rests on
  the book (earns spread). Aggressive taker flow = directional pressure.
- **Order book imbalance**: if bid size ≫ ask size, short-term upward pressure.
- **Volume clustering**: size printed at levels creates support/resistance.
- **Price improvement / fair value**: short-term price oscillates around an
  unobservable fair value; microstructure features help estimate it.
- **Autocorrelation at short horizons**: intraday returns show weak negative
  autocorrelation (bid-ask bounce) and transient momentum around news.

## What this means for predictions
- Short-term moves are driven by order flow, not just indicator crossovers.
- Simple tick-rule and book-imbalance features are powerful (CH_09/CH_10).
- Bid-ask bounce creates noise in returns; use mid-price for signal math.

## Steps to model microstructure
1. If tick data available, compute: trade direction (tick rule), signed volume,
   spread, book imbalance per interval (CH_06, CH_09).
2. Use mid-price for return calculations to remove bounce noise.
3. Feed microstructure features into strategy/ML layers (CH_15).

## Pseudo-code: tick rule for trade direction
```
for trade t:
    if t.price > last_trade_price: direction = +1   # buyer-initiated
    elif t.price < last_trade_price: direction = -1 # seller-initiated
    else: direction = last_direction                # tick rule carry
    signed_volume[t] = direction * t.volume
```

## Rules
- Compute signals on mid-price; assume worst-case fills for execution math.
- Track order-flow features; they often beat price-only indicators intraday.
