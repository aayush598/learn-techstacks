# 01 — Data Flow and Pipeline

## Purpose
Describe the end-to-end journey of information: from exchange feed to final
executed order and audit log. Every system component connects through this flow.

## Main pipeline (historic / offline)
```
Raw OHLCV download -> Raw files (.csv/.parquet)
        -> validate (CH_07)
        -> adjust (splits/dividends)
        -> store (columnar, partitioned)
        -> feature engine (CH_09)
        -> dataset for training/backtest (PART_05)
```

## Main pipeline (real-time / live)
```
Exchange/broker WebSocket feed
        -> tick buffer (dedupe, reorder)
        -> bar aggregation (1m/3m/5m…)  (CH_04, CH_06)
        -> validation & quality gate
        -> append to store (append-only)
        -> feature updates (incremental)
        -> indicator/pattern update
        -> signal generation (PART_04)
        -> RISK GATE (limits, sizing)   (PART_06)
        -> order request -> OMS -> broker -> fills
        -> reconciliation -> audit log
```

## Key design decisions
- **Decouple acquisition from consumption**: live pipeline writes to a local
  store; strategy reads from that store. Strategy never talks to the feed directly.
- **One source of truth**: the validated store is the only data any other module reads.
- **Append-only with versioning**: never mutate history in place; write new versions.
- **Bounded buffers**: live pipeline must never grow memory unboundedly; use ring buffers.

## Pseudo-code: pipeline supervisor
```
loop:
    bar = feed.next_bar()                    # from tick aggregator
    if not validate(bar):                    # CH_07 checks
        log_warn(reject, bar); continue
    store.append(bar)                        # append-only
    feats = feature_engine.update(bar)       # incremental
    sig = strategy.evaluate(feats)           # PART_04
    if sig is None: continue
    if not risk_gate.approve(sig):           # PART_06
        log_risk_reject(sig); continue
    oms.submit(order_from(sig))              # PART_07/08
    audit_log.record(sig, order, time)
```

## Data lineage
- Every stored artifact records: source, capture time, validation result,
  version, and the processing step that produced it. This makes results
  reproducible and debuggable.

## Rules
- A bar is consumed exactly once in the live path (idempotent consumers).
- Any failure in a stage must not silently drop data — log + buffer or halt.
