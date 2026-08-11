# 02 — Reconciliation and Failover

## Purpose
Keep OMS truth aligned with broker truth through disconnects, lost responses,
and process restarts — and fail over without losing protection.

## Reconciliation triggers
- On startup (before any new order).
- After any fill/reject event (spot check positions, CH_24/03).
- After reconnect / auth refresh (CH_24/01).
- Periodic (e.g., every N minutes during market hours).
- At EOD (full: orders + positions + balances).

## Procedure (pseudo)
```
def reconcile_full():
    broker_orders = broker.get_orders()
    broker_pos    = broker.get_positions()
    oms_orders    = journal.live_orders()
    for each oms order:  find broker counterpart by (symbol,side,qty,ts)
        missing -> query by internal_id_map; if gone: adopt broker state
        extra in broker -> adopt (may be manual/ghost): alert + record
    compare positions (CH_24/03); adopt broker as authoritative
    log reconciliation report; alert on any forced adoption
```

## Ghost order handling
- A broker order we no longer track → query by id map; if unresolvable,
  alert + treat as unknown risk (reduce/halt that symbol until resolved).

## Failover design
- Single OMS is simplest and safest for MVP; the failover = restart with
  journal replay: reload state from the journal, reconcile, resume.
- If running a primary/backup pair: only one OMS is active (no split-brain);
  backup takes over after health-check timeout, then reconciles before trading.

## Pseudo-code: startup recovery
```
startup():
    load_journal()
    reconcile_full()            # re-sync with broker truth
    if reconciliation_clean: resume_trading()
    else: alert(); risk.halt_new_entries(pending_review)
```

## Rules
- Broker is authoritative; the journal is our memory of intent.
- Reconciliation differences are never silently ignored — each is logged + alerted.
- Never start trading after restart without a clean reconciliation.
