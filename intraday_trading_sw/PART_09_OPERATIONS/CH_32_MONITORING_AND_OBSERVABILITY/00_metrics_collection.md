# 00 — Metrics Collection

## Purpose
Collect the numbers that tell you the system is healthy, on time, and behaving
as expected — self-hosted, low-overhead.

## Metric groups (with examples)
1. **Data health**: bars ingested/min, gap count, validation rejections,
   feed lag (ms), backfill runs (CH_06, CH_07).
2. **Pipeline timing**: per-stage p50/p95/max (ingest, features, decide, risk,
   OMS round-trip) (CH_27/00).
3. **Signal/strategy**: signals/min per strategy, entry/exit counts, signal→order
   conversions, strategy health flags (CH_14).
4. **Risk**: positions, exposure (gross/net), risk used vs limits, breaker
   status, daily loss used % (CH_20, CH_23).
5. **Execution**: orders/min, reject rate, slippage realized, reconciliation
   diffs, pending orders (CH_24, CH_25).
6. **Model**: prediction drift PSI, feature drift, hit rate rolling, last
   retrain time (CH_16/03).
7. **System**: CPU, RAM, disk, process restarts, NTP offset (CH_31).

## Storage & query (self-hosted)
- Simple: append-only metrics log + periodic rollups in SQLite (CH_08/03).
- Keep raw minute-level metrics for 30–90 days; daily rollups forever.
- Query API for dashboards (CH_29) and alerting (CH_30/00).

## Pseudo-code: metric observation
```
def observe(name, value, tags):
    buffer.append((name, value, tags, now()))
    if len(buffer) >= flush_n or now() - last_flush > flush_s:
        db.append(batch(buffer)); buffer.clear()
```

## Rules
- Metrics must not perturb the hot path: async/batched writes (CH_27/01).
- Every metric has a documented meaning and unit (metrics catalog).
- Never alert on a metric you don't understand — catalog first.
