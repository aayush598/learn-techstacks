# Hashed & Inverted Page Tables

## Hashed Page Table

- Used for **address spaces > 32 bits**
- Virtual page number is hashed into a **hash table**
- Each bucket contains a linked list of entries (collision chain)
- Each entry: `(virtual_page#, frame#, next_ptr)`

### Lookup

1. Hash virtual page# → hash table index
2. Walk chain comparing virtual page#
3. Match found → use frame# for translation

### Pros & Cons

| Pros | Cons |
|---|---|
| Smaller than full page table | Collision chains can degrade performance |
| Handles sparse address spaces well | Hash function adds latency |
| Used in SPARC, PowerPC | TLB miss penalty includes walk + hash |

## Inverted Page Table

- **One entry per physical frame** (not per virtual page)
- System-wide table (not per-process)
- Entry: `(process_id, page#)` — who owns this frame
- Dramatically reduces memory: 4 GB RAM, 4 KB frames → 1M entries → ~8 MB total

### Lookup

- Search entire table for `(PID, page#)` → index is frame#
- Linear search is **too slow** → must use hash table to index into inverted PT
- **Hashed inverted page table:** hash `(PID, page#)` → index into inverted PT

| Aspect | Regular Page Table | Inverted Page Table |
|---|---|---|
| **Entries** | Per virtual page | Per physical frame |
| **Memory** | Large (4 MB per process) | Small (8 MB total) |
| **Search** | Indexed (O(1)) | Hashed (O(1) avg) |
| **Shared memory** | Multiple entries | Single entry, multiple PIDs |
| **Used in** | x86, ARM | PowerPC, UltraSPARC, PA-RISC |

### Drawback

- **Shared memory** is hard to represent (one physical frame accessed by multiple processes)
- Requires PID in TLB entries (ASID)
- Eliminated in x86-64; modern systems use **radix tree page tables** (Linux: 4-level)

## Comparison Summary

```
Full page table:      [page# → frame#]  per process, O(1), large memory
Inverted page table:  [PID + page# → frame#]  one global, small memory, needs hash
Hierarchical:         [p1 → p2 → frame#]  per process, O(levels), sparse-friendly
Hashed:               [hash(page#) → frame#]  per process, O(1) avg, good for >32-bit
```
