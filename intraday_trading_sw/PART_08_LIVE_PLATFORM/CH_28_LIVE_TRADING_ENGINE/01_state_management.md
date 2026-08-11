# 01 — State Management

## Purpose
Define how the engine's state is structured, persisted, and protected — so a
crash or restart never corrupts trading decisions.

## State groups
1. **Persistent state** (SQLite, CH_08/03): positions, orders journal, daily
   limits state, equity curve, checkpoints, strategy state.
2. **Ephemeral state**: indicator/feature incremental states per symbol
   (rebuildable from stored bars — treat as disposable).
3. **Configuration**: manifests, risk policy, model registry pointers — loaded
   at startup, versioned.

## Design rules
- **Stateless strategies**: strategies decide from ctx (CH_14/03); the engine
  owns all mutable state. This makes decisions testable and replayable.
- **Journal-first**: mutate the journal (append) before updating in-memory
  caches (CH_25/00) — crash replay rebuilds truth.
- **Checkpoints**: persist daily-limit counters and positions at bar granularity
  when they change (cheap, batched) so recovery is near-immediate.

## Pseudo-code: state update discipline
```
def apply(order_event):
    journal.append(order_event)          # durable first
    cache.apply(order_event)             # in-memory mirror (fast path)
    if bar_boundary: checkpoint()        # periodic durable snapshot
```

## Recovery (CH_35 tie-in)
- Restart = load journal + checkpoints → reconcile with broker (CH_25/02) →
  rebuild ephemeral state from stored bars → resume.
- Never resume trading from in-memory-only state.

## Rules
- State schema is versioned; migrations run at startup (CH_08/03).
- The UI reads state through the engine's query API (no direct DB writes).
- Two engine instances must never share the same journal (single writer).
