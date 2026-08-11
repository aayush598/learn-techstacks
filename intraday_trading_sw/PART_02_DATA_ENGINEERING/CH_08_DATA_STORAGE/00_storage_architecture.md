# 00 — Storage Architecture

## Purpose
Design a self-hosted, dependency-light storage layer that serves both analytic
workloads (research/backtest) and real-time workloads (live engine).

## Tiered storage design
| Tier | Contents | Access pattern | Tech |
|---|---|---|---|
| Hot (live) | today's bars, ticks, state | append, read recent | memory + local file + SQLite |
| Warm (analytic) | validated bars/features for models | columnar scans | Parquet files (self-written or lib) |
| Cold (archive) | old raw data, audits | rare | compressed files |

## Key principles
- **Append-only** for market data; corrections create new versions (never mutate).
- **Local-first**: everything on local disk / own server; no cloud vendor required.
- **One source of truth** for the live engine: the validated store, not the feed.
- **Atomic writes**: write temp file + rename; a crash never leaves partial files.
- **Bounded hot store**: hot tier rolls into warm on a schedule (EOD job).

## Directory layout (pseudo)
```
data/
  raw/<source>/<symbol>/2024/2024-01-01.csv        # as-received
  store/<interval>/<symbol>/2024.parquet           # validated bars
  features/<interval>/<symbol>/2024.parquet        # engineered features
  state/state.sqlite                               # hot state, checkpoints
  archive/...                                      # compressed cold tier
```

## Hot state (SQLite)
Used for: symbol metadata, ingest checkpoints (CH_06/00), position cache,
order journal, daily stats. Single-writer, WAL mode, small and fast.

## Pseudo-code: atomic write
```
def write_atomic(path, data):
    tmp = path + ".tmp." + pid
    write(tmp, data); flush(); fsync()
    os.rename(tmp, path)      # atomic on same filesystem
```

## Rules
- The store must survive process crashes: WAL/atomic writes + fsync policy.
- Keep raw data separate from cleaned data (audit + reprocessing).
- Storage layout is part of the spec; document it so all modules agree.
