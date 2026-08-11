# 00 — Profiling and Benchmarks

## Purpose
Measure performance objectively so optimizations are driven by evidence, and
regressions are caught before they matter.

## Benchmark types
1. **Unit benchmarks**: indicator/feature batch vs incremental throughput
   (bars/sec); decide() latency; risk gate latency.
2. **Pipeline benchmarks**: end-to-end bar→decision time (CH_27/00 budget).
3. **Backtest benchmarks**: days of data processed per second (vectorized vs
   event-driven, CH_17).
4. **Storage benchmarks**: write throughput, range-read latency, compression
   ratio (CH_08).

## Methodology
- Same machine, warm caches, N repeats; report median/p95/max.
- Fixed dataset fixtures (versioned) so results are comparable over time.
- Profiling: find the top-5 hot spots first; optimize only those (CH_27/01).

## Pseudo-code: benchmark harness
```
def bench(name, fn, n=1000):
    warmup(fn); times = [fn() for _ in range(n)]
    report(name, p50(times), p95(times), max(times))
```

## Budget enforcement
- Benchmarks run in CI (CH_12/CH_41): a change that pushes p95 over budget
  fails the pipeline (CH_27/00).

## Rules
- Optimize measured hot paths only (CH_27/01) — everything else stays readable.
- Store benchmark results historically (a small table) to spot drift.
- Benchmark and profile on the *target hardware class* (CH_27/02), not just dev.
