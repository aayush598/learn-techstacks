# Contiguous Memory Allocation

## Fixed Partition (Multiprogramming with Fixed Tasks - MFT)

- Main memory divided into **fixed-size** partitions
- Each partition holds one process
- **Internal fragmentation:** space wasted inside allocated block (process smaller than partition)
- Example: 8 MB partition with 5 MB process → **3 MB internal fragmentation**
- Limitations: degree of multiprogramming fixed by partition count

## Dynamic Partition (Multiprogramming with Variable Tasks - MVT)

- Partitions created **dynamically** to match process size
- No internal fragmentation within allocated blocks
- **External fragmentation:** free holes between allocated blocks, total free space may be enough but not contiguous
- Example: 50 MB free but split as 20 MB + 20 MB + 10 MB holes, need 35 MB → can't satisfy

## Allocation Strategies

| Strategy | Description | Performance |
|---|---|---|
| **First-fit** | Scan from start, allocate first hole big enough | Fastest, simple |
| **Best-fit** | Allocate smallest hole that fits | Minimizes wasted space, slow (must sort/search all) |
| **Worst-fit** | Allocate largest hole | Leaves large holes available, often worst performer |

### Trade-offs

- **First-fit:** generally best in practice, O(n) search, low overhead
- **Best-fit:** produces tiny leftover holes (leads to more external fragmentation)
- **Worst-fit:** leaves medium holes, counterintuitively may run out faster

## Fragmentation

| Type | Definition | Cause |
|---|---|---|
| **External fragmentation** | Free memory split into small non-contiguous holes | Variable-size allocation, process termination |
| **Internal fragmentation** | Wasted space inside allocated block | Fixed-size partitions |

**50-percent rule:** For first-fit, roughly 1/3 of memory is lost to external fragmentation (statistical average)

## Compaction

- **Relocate** processes to merge free holes into one large block
- All addresses within process must be **relocatable** (dynamic binding)
- Requires **relocation registers** in MMU
- Cost: CPU time to copy process data, process ineligible during move
- Only possible if processes can be dynamically relocated
- Used in early systems; modern OS uses paging instead

## Quick Comparison

```
Fixed:  |  P1 (4M)  |  P2 (8M)  |  P3 (6M)  |  2M internal waste
        |<- 8M part ->|<- 8M part ->|<- 8M part ->|

Dynamic:|  P1 (4M)  |  free 8M  |  P2 (5M)  |  free 2M  |  P3 (3M)  |
```
