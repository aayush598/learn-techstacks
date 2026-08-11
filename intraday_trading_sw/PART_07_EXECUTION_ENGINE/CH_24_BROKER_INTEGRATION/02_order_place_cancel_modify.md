# 02 — Order Place, Cancel, Modify

## Purpose
Define the exact, retry-safe semantics for placing, canceling, and modifying
orders — including what the system must *never* do on ambiguity.

## Place
1. Build order from the approved plan (risk gate already passed, CH_20).
2. Assign internal order id; log intent BEFORE sending.
3. Send via adapter; capture broker id on success.
4. If the response is lost (timeout) — **do not assume**; query order status
   (reconciliation, CH_25/02).

## Cancel
- Send cancel; confirm cancellation by status change (`CANCELLED`), not by the
  cancel-response alone.
- On ambiguity (no status within timeout): query; escalate if unresolved
  (could be a ghost order).
- Cancel-replace only when the new order is ready (no gap in protection).

## Modify
- Preferred: cancel + place (atomic-ish) for intraday simplicity.
- Alternative: native modify if the broker supports it and reports status atomically.
- Re-run the risk gate on the modified values (new qty/stop) (CH_20/01).

## Pseudo-code: place with timeout handling
```
def safe_place(order):
    oid = internal_id(); log_intent(oid, order)
    try:
        bid = broker.place(order)
        return map_ids(oid, bid)
    except Timeout:
        status = broker.query(order=order)     # reconcile
        return interpret(status)               # filled | live | unknown→alert
    except Rejected(e):
        log_rejection(e); risk.notify(); return REJECTED
```

## Rules
- Log every order event (intent/send/ack/status) with internal+broker ids (CH_33).
- A lost response must trigger reconciliation, never a blind resend (duplicates).
- Idempotency: the OMS tracks "last sent snapshot" so retries don't double-execute.
