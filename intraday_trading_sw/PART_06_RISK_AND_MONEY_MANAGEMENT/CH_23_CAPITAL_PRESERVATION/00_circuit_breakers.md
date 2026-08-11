# 00 — Circuit Breakers

## Purpose
Automatically stop the entire system when abnormal conditions threaten capital —
before a human can even react.

## Breaker types
1. **Equity drawdown breaker**: equity falls X% from peak (e.g., 5%).
2. **Daily loss breaker**: daily P&L ≤ −Y% of equity (e.g., 2%).
3. **Exposure breaker**: gross/net exposure exceeds hard caps (CH_20/02).
4. **Execution-health breaker**: order rejections/failures spike, feed lag too
   high, OMS desync (CH_25/02) → halt new trading.
5. **Data breaker**: data gap/validation alarms high (CH_07) → halt strategies
   that depend on the affected data.
6. **Event breaker**: exchange-wide halt, circuit breaker at the market level.

## Breaker behavior
- Trigger → log + alert (CH_30) + **flatten all positions** (market orders) +
  disable new entries for the session (or until human re-arms).
- Breakers are latching: they do not self-reset mid-session without review.

## Pseudo-code: breaker monitor
```
def check_breakers(state, health, policy):
    alarms = []
    if state.dd_from_peak >= policy.breaker_dd:      alarms.append("DD_BREAKER")
    if state.daily_loss_pct <= -policy.daily_loss:   alarms.append("DAILY_LOSS")
    if not health.feed_ok():                         alarms.append("FEED_DOWN")
    if health.order_reject_rate > policy.reject_rate: alarms.append("OMS_DESYNC")
    if alarms:
        flatten_all(MARKET, reasons=alarms)
        halt_new_entries(reason=alarms)
        alert_paginate(alarms)
```

## Pseudo-code: flatten
```
def flatten_all(side_filter=None):
    for pos in open_positions:
        if not side_filter or pos.side in side_filter:
            market_order(opposite(pos.qty), reason="circuit_breaker")
```

## Rules
- Breakers are configurable but *enabled by default* in live mode (CH_20/00).
- Every breaker event is a top-severity incident with full audit (CH_33, CH_32).
- Test breakers in dry-run/papaper mode before enabling in live (CH_37).
