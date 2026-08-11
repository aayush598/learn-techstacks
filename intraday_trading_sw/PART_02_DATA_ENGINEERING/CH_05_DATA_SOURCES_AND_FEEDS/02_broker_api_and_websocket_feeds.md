# 02 — Broker API and WebSocket Feeds

## Purpose
Design the connection to the broker/exchange for both market data and order
execution, with a clean interface and robust connection handling.

## Two channel types
- **REST (request/response)**: historic backfill, snapshot quotes, order placement,
  account queries. Simple, but polling adds latency.
- **WebSocket (push)**: continuous streaming of quotes/trades/order updates.
  Required for live signals; lower latency, one persistent connection.

## Required capabilities (interface contract)
- Subscribe to symbols → receive trades, quotes, and (if available) L2 book.
- Request historic bars for backfill (same instrument/timeframe/granularity).
- Place/cancel/modify orders; receive order status and fill callbacks.
- Query positions, balances, and day P&L.

## Connection management (critical)
1. **Heartbeat/ping**: send pings; detect dead connections.
2. **Auto-reconnect with backoff**: exponential (1s, 2s, 4s… cap 60s).
3. **Resubscribe on reconnect**: re-request all subscriptions.
4. **Gap handling**: on reconnect, backfill any missed interval from REST before
   resuming live consumption.
5. **Order state safety**: on disconnect, do NOT assume orders failed — query
   broker for authoritative state (reconciliation, CH_25).

## Pseudo-code: resilient WebSocket client
```
on_open():  resubscribe(all_subscriptions); restart heartbeat
on_message(m):
    if heartbeat: reply pong
    else: normalize -> push to pipeline
on_close(err):
    backoff = min(backoff*2, 60s)
    schedule reconnect(backoff)
    request_missed_since(last_ts)   # backfill gap via REST
```

## Rules
- Treat the broker feed as external and unreliable: buffer, validate, reconnect.
- Never block the data pipeline on broker network calls (separate threads/queues).
- Keep all broker-specific code inside the adapter (CH_24); nothing else sees it.
