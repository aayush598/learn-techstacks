# 01 — Realtime Stream Ingestion

## Purpose
Design the always-on ingestion path that turns a live feed into validated,
stored bars with bounded memory and graceful degradation.

## Ingestion pipeline stages
1. **Connection layer**: WebSocket client (CH_05/02) → raw message queue.
2. **Normalizer**: convert source messages → canonical tick/quote/bar records.
3. **Deduplicator**: drop duplicates (exchange re-sends, reconnect replays).
4. **Orderer**: handle out-of-order timestamps (bounded reorder buffer).
5. **Bar aggregator**: ticks → 1m bars (CH_04/00); higher TF derived later.
6. **Validator**: quality gate (CH_07) — reject bad bars, log, count.
7. **Writer**: append-only write to store (batched, fsync policy).
8. **Fan-out**: publish validated bars to in-process subscribers (features, engine).

## Bounded memory design
- Use fixed-capacity ring buffers at each stage; slow consumers must not grow queues.
- Policy: if a stage falls behind, drop *raw* data first and backfill later from
  REST (never drop already-validated bars without a record).

## Pseudo-code: orchestrator
```
while running:
    msg = raw_queue.get(timeout)
    rec = normalize(msg)
    if not dedupe(rec): continue
    bar = aggregator.push(rec)
    if bar is None: continue
    if not validate(bar): metrics.gaps++; continue
    store.append(bar)
    fan_out.publish(bar)      # non-blocking
    metrics.ingested += 1
```

## Rules
- Separate the ingestion process from strategy/execution processes; a data spike
  must never stall order handling.
- Record ingestion lag (feed timestamp vs now) as a monitored metric (CH_32).
- Backfill missed intervals automatically after any reconnect.
