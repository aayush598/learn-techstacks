# 00 — Backup Strategy

## Purpose
Protect data, state, and configuration so nothing critical is ever lost — with
recovery that actually works.

## What to back up (in priority order)
1. **Order/risk journal** and **audit log** (append-only, CH_25, CH_34/02).
2. **State DB** (positions, daily limits, checkpoints) (CH_28/01).
3. **Validated market data** (store/features) (CH_08) — re-downloadable but
   expensive; back up the raw as-fetched too.
4. **Configuration + manifests + model artifacts** (CH_16) — cheap, versioned
   in the repo anyway.
5. **Logs** (CH_33) for forensics.

## Backup cadence
- Continuous: journal/audit (WAL files copied or per-batch).
- Intraday: state DB checkpoints hourly.
- Daily: full data + state + config snapshot after close.
- Weekly: cold archive to a second location.

## Pseudo-code: daily backup job
```
def daily_backup():
    snapshot = tar(data_dir, state.db, config, models)
    write_atomic(snapshot, backup_dir/daily/)         # local
    copy_encrypted(snapshot, backup_dir/offsite/)     # second location (CH_35/01)
    verify(snapshot)                                  # hash + spot-read
```

## Verification (restore drills)
- Backup is only real if it restores. Monthly: restore to a scratch dir and run
  `doctor` (CH_31/00) + a replay (CH_33/01) on the restored data.
- Log verification results; a failing drill is a CRITICAL alert (CH_30).

## Rules
- Backups are encrypted at rest (CH_34/00 policy) when they contain secrets.
- Retention: daily ≥ 30 days, weekly ≥ 6 months, monthly ≥ 2 years (journal/
  audit kept longer per compliance, CH_39).
- Test restore — untested backups don't count.
