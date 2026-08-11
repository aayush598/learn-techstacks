# 00 — Market and Limit Orders

## Purpose
Master the two fundamental order types the execution engine will use, including
their cost, speed, and fill certainty.

## Market order
- Executes immediately at the best available price; walks the book as needed.
- Pros: guaranteed fill (in liquid markets); Cons: pays the spread, uncertain
  price, market impact on large size.
- **Use when**: speed matters more than price (stops, exits that must happen).

## Limit order
- Executes only at the limit price or better.
- Pros: control over price, can earn the spread as a maker; Cons: may not fill.
- **Use when**: patience exists, or you want to be the passive liquidity.

## Order book basics
- **Bid** = highest price a buyer will pay; **Ask** = lowest price a seller will take.
- **Best Bid/Offer (BBO)**: the top of book; **mid** = (bid+ask)/2.
- **Spread** = ask − bid. Crossing the spread costs you the spread.
- **Slippage** = difference between expected fill price and actual fill price.

## Design decisions for the OMS
- Store order type, side, quantity, price (if any), limit/stop price, time.
- Model worst-case fill = ask (for buys) / bid (for sells) in backtests (CH_17).
- Provide a configurable "order style" per strategy: market, limit, or limit-with-timeout.

## Pseudo-code: choosing execution style
```
def execute(intent):
    if intent.style == MARKET:
        return broker.market_order(side, qty)
    elif intent.style == LIMIT:
        lmt = quote(limit_price_for(intent))
        return broker.limit_order(side, qty, lmt)
    elif intent.style == LIMIT_TIMEOUT:
        place limit; wait t_secs
        if not filled: cancel -> market (or abandon per strategy)
```

## Rules
- Never assume fills at the last traded price; model BBO + slippage.
- For exits, prefer market orders; for entries, limit orders where possible.
