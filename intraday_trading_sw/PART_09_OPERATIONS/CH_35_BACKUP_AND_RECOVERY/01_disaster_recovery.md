# 01 — Disaster Recovery

## Purpose
Define what the system does when something big breaks — machine loss, disk
failure, data corruption, broker outage — and how to come back safely.

## Disaster classes and responses
1. **Process crash** → auto-restart + journal replay (CH_28/02, CH_31/02).
2. **Machine loss** → rebuild from setup automation (CH_31/00) + restore backup
   (CH_35/00) + reconcile with broker (CH_25/02) before trading.
3. **Disk failure/data corruption** → detect (validation/checksums, CH_07),
   restore from daily snapshot; mark affected period and re-derive.
4. **Broker/exchange outage** → pause trading (halt new entries, keep/flatten
   per policy), monitor, resume after reconciliation. Never trade blind.
5. **Network partition** → auto-reconnect + gap backfill (CH_06/02); safety
   orders (stops) remain at broker.

## Recovery procedure (machine loss example)
```
1. provision new host per CH_31/00 (doctor passes)
2. install repo at pinned version (CH_12/CH_41)
3. restore latest verified backup (CH_35/00)
4. reconcile with broker (authoritative state, CH_25/02)
5. run replay on last session's decisions (sanity, CH_33/01)
6. enter pre-market flow; enable trading only after health checks green (CH_32/01)
```

## Pseudo-code: recovery gate
```
def enable_trading_after_recovery():
    assert doctor_ok()
    assert restored_data_verified()
    assert reconciliation_clean()
    assert health_checks_green()
    log("recovery_complete")
    resume()
```

## Rules
- Recovery goal: **correct** first, fast second. A wrong resume is worse than a
  late one.
- Every recovery is a logged incident with a written review (CH_32/02).
- Run a recovery drill quarterly (planned downtime) to keep the playbook honest.
