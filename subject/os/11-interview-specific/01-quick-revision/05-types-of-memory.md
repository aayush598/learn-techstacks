# Types of Memory (Memory Hierarchy)

## The Memory Hierarchy
```
         CPU Register          ~1ns     ~500B
              ↓
            L1 Cache           ~1ns     ~32KB
              ↓
            L2 Cache           ~4ns     ~256KB
              ↓
            L3 Cache           ~10ns    ~8-16MB
              ↓
          Main RAM             ~100ns   ~8-512GB
              ↓
         SSD (NVMe)            ~10μs    ~256GB-2TB
              ↓
         HDD (Disk)            ~10ms    ~1-10TB
```

## Latency Numbers (Approximate)

| Memory Type | Technology | Latency | Size | Cost/GB |
|-------------|------------|---------|------|---------|
| **Register** | Flip-flops | ~0.3–1ns | ~256–1KB | $$$$$ |
| **L1 Cache** | SRAM (static) | ~1ns | 32–64KB | ~$1000 |
| **L2 Cache** | SRAM | ~4ns | 256KB–1MB | ~$500 |
| **L3 Cache** | SRAM | ~10ns | 8–32MB | ~$100 |
| **Main Memory** | DRAM (dynamic) | ~100ns | 4–512GB | ~$10 |
| **SSD** | NAND Flash | ~10μs (10,000ns) | 256GB–2TB | ~$0.10 |
| **HDD** | Magnetic disk | ~10ms (10,000,000ns) | 1–10TB | ~$0.02 |

## Key Concepts
- **Locality of Reference:**
  - **Temporal:** recently accessed data likely accessed again (keep in cache)
  - **Spatial:** nearby data likely accessed soon (cache lines: 64B)
- **Cache Line:** smallest unit of data transfer between cache and RAM (typically 64B)
- **Cache Miss:** L1 → L2 → L3 → RAM → disk (each level ~10× slower)
- **Virtual Memory:** extends "memory" to disk via paging (swap)

## DRAM vs SRAM
| Property | SRAM | DRAM |
|----------|------|------|
| **Speed** | Fast (~1–5ns) | Slower (~50–100ns) |
| **Density** | Low (6 transistors/bit) | High (1 capacitor + 1 transistor) |
| **Power** | Higher leakage | Lower (needs refresh) |
| **Use** | Cache (L1/L2/L3) | Main memory (RAM) |

## Caching Levels (Why it matters)
- L1 hit: ~1ns | L3 hit: ~10ns | RAM hit: ~100ns
- Main memory **miss** → disk I/O → **~10 million ns penalty**
- **Cache-friendly code:** sequential access (spatial locality), reuse data (temporal)

## Interview Tip
- *"L1 cache reference is 100× faster than main memory, a million times faster than disk"*
- Know the **latency numbers table** (registers ~1ns → HDD ~10ms = 10^7 difference)
- *"Cache misses are the silent performance killer"*
