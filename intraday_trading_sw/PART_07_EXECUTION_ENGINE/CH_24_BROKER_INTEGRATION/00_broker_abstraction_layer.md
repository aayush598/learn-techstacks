# 00 — Broker Abstraction Layer

## Purpose
Isolate ALL broker-specific code behind one interface so the core system is
broker-agnostic, testable with a simulator, and resilient to broker changes.

## Interface contract (what the core needs)
```
class Broker:
    # market data
    subscribe(symbols) -> stream of quote/trade events
    request_history(symbol, interval, start, end)
    # orders
    place(order) -> broker_order_id
    cancel(broker_order_id)
    modify(broker_order_id, price|qty|stop)
    # state
    get_orders(filter) -> list[Order]
    get_positions() -> list[Position]
    get_balance() -> Balance
    # lifecycle
    connect(); disconnect(); is_connected()
```

## The core NEVER sees broker specifics
- No broker SDK types leak out; adapters return canonical objects
  (schema in CH_07/00).
- No broker credentials anywhere except the adapter config (CH_34).
- Order ids: internal id ↔ broker id mapping in the OMS (CH_25).

## Adapter structure
```
adapters/
  base.py        # abstract Broker + canonical types
  simulator.py   # paper trading broker (CH_37) — always exists
  broker_x.py    # one concrete implementation per broker
```
The `simulator` is not a nicety — it is the primary test surface and the paper
trading venue; every feature must work against it first.

## Pseudo-code: adapter selection
```
def load_broker(config):
    return ADAPTERS[config.broker_type](config)   # simulator | broker_x
```

## Rules
- One interface, many adapters; the OMS (CH_25) only talks to the interface.
- Every broker call is wrapped with retries/timeouts (CH_05/02 pattern) and
  logged with the full payload (audit, CH_33).
- Add a new broker = write one adapter + tests, zero core changes.
