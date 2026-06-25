# Working Set Model

## Concept

- **Working set:** set of pages a process is currently using
- Defined by a **window Δ** (a fixed number of page references)
- WSS_i = **working set size** of process i (number of unique pages referenced in last Δ)

### Example

```
Δ = 10 (window of last 10 page references)

References: ... 2 6 1 5 7 7 7 1 4 3 4 4 2 1 6 7 8 3 1 4 ...
                                      ^--- current Δ ---^
Working set = {1, 2, 3, 4, 6, 7}  (unique pages in window)
WSS = 6
```

## Working Set Size (WSS)

- WSS varies per process and over time
- Changes with **locality shifts**
- If Δ is too small: may not capture full locality
- If Δ is too large: may overlap multiple localities
- Typical Δ = 10,000–100,000 references

## Total Demand Frames

```
D = Σ WSS_i   (sum over all processes)
```

- **D = total frames needed** to avoid thrashing
- If `D > m` (total available frames) → thrashing
- OS must suspend/swap out some processes

## Working Set Model Prevents Thrashing

1. OS monitors each process's WSS (approximated via reference bits)
2. If `D > m`:
   - Suspend one or more processes (swap out)
   - Bring total demand within available frames
3. Advantage: **proactive** rather than reactive (vs. PFF)

## Implementation

- Approximate WSS by checking **reference bits** every clock interrupt
- Scan page table, update working set info
- Pages not referenced in the last Δ scans are **not in working set**
- Overhead: periodic scan of page tables

## Page Fault Frequency (PFF) Approach

- Alternative to explicit working set tracking
- Set **upper and lower thresholds** for page fault rate

```
Page fault rate
    ↑
  Upper threshold → allocate more frames (increase WSS)
    ↓
  Lower threshold → reclaim frames (decrease WSS)
    ↓
```

- Each process adjusts its frame allocation dynamically
- System-wide: monitor sum of allocated frames vs available memory

## Working Set vs PFF

| Aspect | Working Set | PFF |
|---|---|---|
| **Mechanism** | Track referenced pages | Monitor fault rate |
| **Implementation** | Periodic reference bit scan | Count page faults per time |
| **Proactive?** | Yes (predicts need) | Reactive |
| **Overhead** | Periodic scans | Fault counters |
| **Used in** | Research/early UNIX | Modern OS (Linux) |

## Linux Working Set Approximation

- **PG_active + PG_referenced** flags
- Pages move between **active** and **inactive** lists
- Active list ≈ working set
- **kswapd** reclaims pages from inactive list
- Pages faulted back are reactivated
