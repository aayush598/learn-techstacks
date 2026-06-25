# Page Replacement Algorithms: Comparison Summary

| Algorithm | Pros | Cons | Belady's Anomaly? | Stack Property? | Performance |
|---|---|---|---|---|---|
| **FIFO** | Simplest implementation, lowest overhead | Can cause Belady's anomaly, poor performance | **Yes** | **No** | Worst (baseline) |
| **OPT (MIN)** | Lowest possible page faults (theoretical optimum) | Needs future knowledge, **not implementable** | **No** | **Yes** | Best (theoretical) |
| **LRU** | Near-optimal in practice, avoids Belady's | Expensive per-access overhead, needs hardware support | **No** | **Yes** | Near-optimal |
| **Clock (Second-Chance)** | Low overhead, approximates LRU well | Less accurate than true LRU under some workloads | **No** | **No** (approx) | Good |
| **Enhanced Clock** | Considers dirty pages (avoids writes) | Slightly more complex than basic Clock | **No** | **No** (approx) | Good–Very Good |
| **NFU + Aging** | Very close to LRU, low per-interrupt cost | Needs timer interrupt, counter size limits history | **No** | **No** (approx) | Near-LRU |
| **LFU** | Works for long-running hot pages | Stale count problem (pages never evicted) | **No** | **No** | Poor (without decay) |

## Key Takeaways for Interviews

- **OPT** = theoretical lower bound (benchmark only)
- **LRU** = best practical algorithm, but too expensive
- **Clock** = practical approximation used in most OS (Linux, BSD, Windows)
- **FIFO** = only algorithm with Belady's anomaly (a classic trap question)
- **Stack property** ⇒ can't have Belady's anomaly (OPT, LRU have it; FIFO doesn't)

## Performance Ranking (Typical)

```
OPT ≥ LRU ≥ Aging ≈ Enhanced Clock > Clock > FIFO
(Best)                                        (Worst)
```

## Implementation in Real OS

| OS | Algorithm |
|---|---|
| Linux | Clock-like (PG_active + PG_referenced) + LRU lists (active/inactive) |
| Windows | Clock-based with FIT (frequency-based) |
| BSD/macOS | Enhanced Clock (reference + modify) |
