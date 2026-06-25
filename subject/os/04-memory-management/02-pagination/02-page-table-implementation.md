# Page Table Implementation

## Page Table in Main Memory

- **PTBR (Page Table Base Register):** points to process's page table in memory
- **PTLR (Page Table Length Register):** indicates page table size for bounds checking
- Problem: every memory access requires **two actual memory accesses**
  - (1) Fetch page table entry
  - (2) Access data/instruction

## TLB (Translation Lookaside Buffer)

- Small, fast **associative cache** inside MMU
- Stores recent page# → frame# mappings
- On address translation:
  - Check TLB first (hardware parallel search)
  - **TLB hit:** get frame# immediately (one memory access)
  - **TLB miss:** walk page table in memory, update TLB (two memory accesses)

## Effective Memory Access Time (EAT)

```
EAT = hit_ratio × (TLB_time + mem_time) 
     + (1 - hit_ratio) × (TLB_time + 2 × mem_time)
```

Simplified (TLB_time negligible vs mem_time, but included for accuracy):

```
EAT = hit_ratio × TLB_time 
     + (1 - hit_ratio) × (TLB_time + 2 × mem_time)
     + mem_time
```

### Example Calculation

| Parameter | Value |
|---|---|
| TLB hit ratio | 99% |
| TLB access time | 2 ns |
| Memory access time | 100 ns |

```
EAT = 0.99 × (2 + 100) + 0.01 × (2 + 200)
    = 0.99 × 102 + 0.01 × 202
    = 100.98 + 2.02
    = 103.0 ns
```

Without TLB: **200 ns** (2 memory accesses). With TLB: **103 ns**. Near-ideal.

## TLB and Context Switch

- TLB entries are **per-process** (same virtual page# maps to different frame#)
- On context switch:
  - **Flush TLB** (invalidate all entries) — simple but costly
  - **ASID (Address Space ID):** tag each TLB entry with process ID
    - No flush needed; hardware matches ASID
    - Used in modern CPUs (x86-64 PCID, ARM ASID)

## TLB Reach

- **TLB reach** = number of entries × page size
- Example: 64 TLB entries × 4 KB pages = **256 KB reach**
- For workloads > 256 KB → TLB misses increase
- Solution: **huge pages** (2 MB) increase TLB reach to 128 MB (64 entries × 2 MB)
