# 02 — Database and I/O Tuning

## Purpose
Make the storage layer (CH_08) fast enough for live appends and analytic scans
without exotic hardware.

## Write path (live)
- Batch bar writes (flush every N bars / T seconds) into sorted row groups
  (CH_08/02); avoid per-bar fsync.
- SQLite (state/journal, CH_08/03): WAL mode, batched transactions,
  `busy_timeout`, single writer — no per-event commits on the hot path.
- Journal-first persistence (CH_25/00) uses the same batching, with a guarantee
  that order-critical records are flushed before ack.

## Read path (analytic)
- Column pruning + file-level stats to skip irrelevant files (CH_08/01–02).
- Range reads with binary search; stream, don't load everything.
- Keep indexes on hot queries (symbol+ts) minimal (CH_08/03).

## I/O tuning specifics
- SSD recommended (CH_27/02); direct I/O where the runtime allows.
- Compression: columnar defaults; measure read-vs-size trade-off per dataset.
- No I/O on the decision hot path except the required journal-first flush
  (async/queued, CH_33/00).

## Pseudo-code: batched flush
```
def flush_batch():
    with db.transaction(): insert(batch)
    write_row_group(bars_batch)                 # columnar append
    metrics.flush_duration.observe(...)
```

## Rules
- Validate latency with load tests (CH_38/01) — 2× expected volume must hold
  the write budget (CH_27/00).
- A slow storage layer must alert before it degrades live decisions (CH_32).
- Tune with measurements (CH_38/00); never guess at storage bottlenecks.
