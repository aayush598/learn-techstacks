# 00 — Smart Order Routing

## Purpose
Choose *how* to send an order (venue, order type, timing) to improve fill
quality while keeping the logic simple, auditable, and self-hosted.

## Routing decisions
1. **Order type**: market vs limit vs limit-with-timeout (CH_03/00).
2. **Timing**: send now vs on the next bar vs when price reaches a level.
3. **Venue** (if multiple venues/brokers): pick the venue with the best price +
   reliability score (for most users: single venue, skip complexity).
4. **Aggressiveness**: cross the spread (taker) vs rest on the book (maker).

## Rule of thumb (intraday)
- **Entries**: prefer limit or limit-with-timeout to pay less.
- **Exits/stops**: prefer market to guarantee the exit.
- Rebalance the trade-off by strategy, not in one place.

## Pseudo-code: route decision
```
def route(intent, market_state):
    if intent.priority == EXIT:        return MARKET
    if intent.is_stop:                 return STOP_MARKET
    if intent.limit_px and near(intent.limit_px, best_ask, tol):
        return LIMIT(timeout=intent.timeout)
    return MARKET   # fallback: don't chase; escalate to strategy if bad fill
```

## Fill quality monitoring
- Compare realized fill vs mid/VWAP at send time → slippage metric per strategy
  (CH_17/02 model vs reality; live report, CH_18/03).

## Rules
- Routing is deterministic and logged (why this type/venue/time).
- Never send both market and limit for the same intent (duplicate risk).
- If routing can't meet the plan's constraints, prefer *not trading*.
