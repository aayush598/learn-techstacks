# Memory Fragmentation

## External Fragmentation
- **Definition:** free memory broken into small, non-contiguous holes
- **Cause:** variable-size partitions, segmentation, allocation/deallocation patterns
- **Result:** total free memory is sufficient, but no single contiguous block fits a request
- **Example:** 100MB free (four 25MB chunks), request 50MB → **fails**
- **Solution:** **compaction** — rearrange memory to consolidate holes (expensive, O(n))

## Internal Fragmentation
- **Definition:** allocated memory larger than requested
- **Cause:** fixed-size partitions, paging (last page not fully used)
- **Result:** wasted space **within** allocated block
- **Example:** 4KB page size, request 5KB → allocates 2 pages (8KB), 3KB **internal fragmentation**
- **Solution:** use smaller page size (but increases page table size)

## Comparison

| Aspect | External Fragmentation | Internal Fragmentation |
|--------|----------------------|----------------------|
| **Location** | Outside allocated blocks (between them) | Inside allocated blocks |
| **Caused by** | Variable-size allocation / deallocation | Fixed-size allocation (last unit partial) |
| **Memory scheme** | Segmentation, dynamic partitioning | Paging, fixed partitioning |
| **Example** | 3×10KB holes but 30KB request fails | 16KB request → 8KB page → 2 pages → waste |
| **Mitigation** | Compaction, coalescing, slab allocator | Smaller page size, kmalloc (Linux kernel) |

## Compaction
- Move processes in memory to consolidate free space
- **Costly:** requires updating all address references
- Only possible if relocation is **dynamic** (base + limit registers)
- Used in: **segmentation with compaction**, Java GC (compact phase)

## Paging and Fragmentation
- **Paging eliminates external fragmentation** (all pages are same size)
- **But has internal fragmentation** (partial last page)
- **Page size trade-off:**
  - Small pages (4KB): less internal fragmentation, larger page tables
  - Large pages (2MB/1GB): less page table overhead, more internal fragmentation
  - Huge Pages (Linux): `hugeadm`, `hugetlbfs` — 2MB or 1GB pages

## Linux Slab Allocator
- Solves both fragmentations for kernel objects
- Object caches: pre-allocate fixed-size objects (e.g., `task_struct` cache)
- Reduces **external fragmentation** — objects same size
- Reduces **internal fragmentation** — exact-fit allocation
- `slabtop` to view slab usage

## Interview Tips
- *"Paging eliminates external fragmentation but introduces internal fragmentation"*
- *"Compaction is expensive — like defragmenting a disk while it's running"*
- *"Slab allocator pre-allocates kernel object caches to avoid both"*
