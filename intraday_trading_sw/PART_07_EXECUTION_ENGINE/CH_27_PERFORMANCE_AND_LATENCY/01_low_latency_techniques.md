# 01 — Low-Latency Techniques

## Purpose
Achieve predictable low latency through sound engineering — without exotic
hardware or micro-optimization theatre.

## Techniques (ranked by value)
1. **Precompute and cache**: indicators/features computed incrementally on new
   bars, never recomputed from scratch (CH_10/00, CH_09).
2. **Avoid I/O on hot paths**: no disk writes or blocking network in decide();
   order logs are async/batched (CH_33).
3. **Minimize allocations**: reuse buffers, avoid creating objects per bar.
4. **Efficient data structures**: ring buffers, arrays; binary search for ranges.
5. **Single-threaded hot loop** with event queues (no locks on the hot path).
6. **Batched flushes**: storage writes are buffered and flushed periodically
   (CH_08), not per bar.
7. **Sort stable events**; never block on network in the signal path.
8. **Profile-driven**: only optimize what benchmarks (CH_38/00) show is hot.

## Anti-patterns to avoid
- Re-parsing/JSON-decoding per bar unnecessarily.
- Synchronous DB calls in the signal path.
- Logging at high volume on the hot thread (async logging).
- Copying large history arrays per update.

## Pseudo-code: incremental feature update
```
state = IndicatorState(symbol)          # persists between bars
def on_bar(bar):
    t0 = now_ms()
    state.update(bar)                   # O(1) per bar
    feats = state.current()             # no re-scan of history
    ...
```

## Rules
- Optimize the *measured* hot path only (CH_38/00).
- Latency is checked continuously; keep p95 well under budget (CH_27/00).
- Readability and correctness outrank micro-optimization — except where the
  budget says otherwise.
