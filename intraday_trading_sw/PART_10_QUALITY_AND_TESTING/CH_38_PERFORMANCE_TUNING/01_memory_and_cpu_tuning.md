# 01 — Memory and CPU Tuning

## Purpose
Keep the live system within predictable memory and CPU budgets during long,
data-heavy sessions.

## Memory design (bounded from the start)
- Ring buffers everywhere in the hot path (CH_06/01) — bounded by construction.
- Hot store kept in RAM with a hard cap; older data streams from disk
  (CH_08/00 tiering).
- No unbounded caches; every cache has a size limit and eviction policy.
- Track per-process RSS; alert on growth trend (CH_32/00), not just spikes.

## CPU tuning
- Prefer the incremental computations (CH_27/01) — no per-bar full recomputes.
- Batch flushes for storage/logs (CH_08, CH_33) to avoid per-bar syscalls.
- If CPU-bound: profile (CH_38/00) → optimize hot functions → only then add
  parallel workers (be careful with shared state, CH_25/00 single-writer rule).
- Backtest/training jobs are separate, low-priority processes (CH_31/01) so they
  never starve live work.

## Pseudo-code: cache policy
```
class BoundedCache:
    def __init__(cap): self.cap = cap
    def get(k): ...
    def put(k,v):
        if len >= cap: evict_oldest()          # bounded memory guaranteed
        store(k,v)
```

## Rules
- Memory growth over a session is a bug: monitor and alert (CH_32).
- Never tune CPU by increasing polling or recomputation — restructure first.
- Load tests: simulate 2× the max expected symbols/bars to verify budgets
  (CH_36/02).
