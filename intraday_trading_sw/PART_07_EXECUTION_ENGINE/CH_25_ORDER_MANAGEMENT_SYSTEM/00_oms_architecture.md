# 00 — OMS Architecture

## Purpose
Design the Order Management System: the single owner of the order lifecycle,
guaranteeing no lost, duplicate, or mis-stated orders.

## Responsibilities
- Accept approved orders from the engine (CH_28).
- Assign internal ids; maintain the internal↔broker id map.
- Drive the order state machine (CH_25/01).
- Persist every transition to the execution journal (append-only).
- Reconcile with the broker on ambiguity/disconnect (CH_25/02).
- Provide an ordered query API for UI, risk, and reports.

## OMS as the only order gateway
- No module (strategy, UI, research) talks to the broker directly — only the OMS.
- The UI's manual orders and the strategy's orders both go through the same
  risk gate + OMS (CH_23/02).

## Pseudo-code: OMS submit path
```
def submit(order, source):
    assert risk_gate.approve(order)          # already enforced upstream
    oid = internal_id(order, source)
    journal.append(PENDING, order)           # persist before send
    broker_id = adapter.place(order)          # CH_24/02
    journal.append(SENT, {oid, broker_id})
    register(oid, broker_id)
    return oid
```

## Concurrency model
- Single OMS thread/actor; order events queued. No two threads mutate an order.
- Timeouts and callbacks funnel into one event queue (avoid races).

## Pseudo-code: OMS event loop
```
while True:
    ev = order_events.get()          # ack, fill, reject, timeout
    transition(state_machine, ev)    # CH_25/01
    journal.append(ev)
    notify_subscribers(ev)           # UI, risk, positions
```

## Rules
- Journal-first: persist state before acting on it (crash safety, CH_35).
- OMS is idempotent: retries keyed by internal id never double-execute.
- Every order query goes through the OMS (single consistent view).
