# 02 — Shutdown, Recovery, Restart

## Purpose
Make shutdown and restart first-class, safe operations — the system must never
crash into a state where positions are unprotected.

## Shutdown types
1. **Planned (end of day / operator)**: flatten any positions (CH_23/01),
   cancel open orders, persist final state, run EOD reconciliation, disconnect.
2. **Graceful (signal SIGTERM)**: stop taking new decisions, flush journals,
   keep protective stops in place (broker-side), checkpoint, exit cleanly.
3. **Crash (any failure)**: journal is durable (journal-first, CH_28/01);
   broker-side protective orders remain valid; recovery on restart.

## Graceful shutdown pseudo-code
```
def shutdown(reason):
    risk.halt_new_entries(reason)
    cancel_non_protective_orders()
    flatten_open_positions(MARKET, reason)     # or rely on broker stops per policy
    journal.flush(); checkpoint()
    reconcile_full()                            # CH_25/02
    log("shutdown_complete", reason)
    disconnect()
```

## Recovery sequence (pseudo)
```
startup():
    load_config(); open journal
    reconcile_full()                            # broker truth (CH_25/02)
    rebuild_ephemeral_states(from stored bars)
    validate_daily_limits_state()
    if clean: enter pre-market routine
    else: alert(); require human review to enable trading
```

## Restart cadence
- Normal: daily restart before market open (pick up calendar, config, model
  updates from the registry, CH_16/03).
- Unexpected: auto-restart by the process manager (CH_31/02) with the recovery
  sequence above.

## Rules
- Protective stops stay at the broker through restarts (defense in depth, CH_03/01).
- If flattening fails during shutdown, log + alert immediately; never pretend.
- Recovery must pass reconciliation before any new order (CH_25/02).
