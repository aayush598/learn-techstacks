# 02 — Process Management and Autostart

## Purpose
Keep every service running: start on boot, restart on failure, no zombie
processes, clean shutdowns.

## Process manager
- **systemd units** (default): start ordering, restart policies, log capture,
  and status checks out of the box.
- Fallback: a small supervised launcher script (no external dependency) with the
  same behavior: respawn, backoff, log.

## Unit design (per service)
- `Restart=on-failure`, `RestartSec` with backoff (e.g., 1s→30s).
- Start ordering: `db` → `ingest` → `engine`/`oms` → `ui` → `monitor`.
- `ExecStop` = graceful shutdown signal (CH_28/02).
- Resource limits: `MemoryMax`, `LimitNOFILE`; watchdog `WatchdogSec` for the
  engine (heartbeat, CH_32/01).

## Pseudo-code: watchdog heartbeat
```
engine loop:
    watchdog.reset()        # every bar / N seconds
# process manager kills+restarts if watchdog not reset in time
```

## Autostart + scheduling
- Service starts at boot (before market open), stops cleanly after close
  (EOD routine, CH_28/02).
- Nightly jobs (backfill, retraining, backups CH_35) via systemd timers or cron.

## Rules
- A crashed service must never start a *second* trading instance (single-writer
  lock: a lock file / DB claim on the journal, CH_28/01).
- Every restart is logged with reason (journal entry, CH_33).
- Restart loops are alerting-worthy (CH_32/02) — three failures = human attention.
