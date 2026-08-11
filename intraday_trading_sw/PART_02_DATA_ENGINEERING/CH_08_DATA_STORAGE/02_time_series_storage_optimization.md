# 02 — Time Series Storage Optimization

## Purpose
Make time-series reads/writes fast and disk-efficient for intraday granularity
(1m bars of many symbols over years).

## Optimization techniques
1. **Partition by symbol → year → month**: scans touch only relevant files.
2. **Sorted timestamps** within files: enable binary-search range reads and
   delta encoding for timestamps (big savings).
3. **Delta-of-delta timestamps + varint** for the ts column (common for
   time-series compression).
4. **Out-of-order tolerant ingest**: keep a small unsorted buffer, flush sorted
   batches; readers tolerate per-file sort.
5. **Column pruning at read time**: only load requested columns.
6. **File-level stats**: min/max ts per file to skip files outside a query range.
7. **Chunked/streaming reads** for long ranges — never load whole years into RAM.

## Pseudo-code: range read
```
def read_range(symbol, interval, start, end):
    files = select_files(symbol, interval, overlapping(start,end))
    for f in files:
        rows = f.read_range(start, end)     # via stats + binary search
        yield rows
```

## Write amplification control
- Batch appends (e.g., flush every N bars or T seconds) into sorted row groups.
- Compaction job merges small row groups into larger ones in the background.

## Sizing guidance (typical)
- 1m bars: ~365 days × ~375 bars/day × 100 symbols ≈ 13.7M rows/year.
- With columnar compression: easily within a few GB for years of history —
  fits comfortably on a normal server disk.

## Rules
- Keep timestamps sorted per row group (query correctness + compression).
- Always keep file-level stats current after compaction.
- Measure read latency for the longest backtests; tune chunking accordingly.
