# Linux Memory Management

## Virtual Memory
- **Page tables**: 4-level on x86_64 (PGD → P4D → PUD → PMD → PTE)
- Each process has own **page table** (CR3 register on context switch)
- **TLB** (Translation Lookaside Buffer): caches recent page translations
- Huge pages: 2MB (HugeTLB) or 1GB pages — reduce TLB misses

## Physical Memory Allocation

### Buddy System
- Allocates physical pages in **power-of-2** blocks (4KB, 8KB, ..., 4MB)
- Free blocks organized in **lists per order** (0 to 10, MAX_ORDER)
- **Buddy**: pair of blocks of same order that can be merged
- `alloc_pages()`, `free_pages()`
- Fragmentation: **external** (reduced by buddy merging), **internal** (within blocks)

### Slab Allocator
- For **small kernel objects** (task_struct, inode, dentry)
- **Cache**: per-object-type pool of pre-allocated objects
- Slab = one or more contiguous pages divided into objects
- Types: SLAB (original), **SLUB** (default, simpler), SLOB (embedded)

## OOM Killer
- Triggered when kernel **exhausts all memory**
- Selects "best" victim using **badness score**:
  - Sum of RSS + swap + page table pages
  - Root processes adjusted (lower score)
  - Process with highest badness killed
- `echo f > /proc/sysrq-trigger` (manual OOM trigger)
- `/proc/sys/vm/overcommit_memory`: controls overcommit policy

## /proc/meminfo
| Field | Meaning |
|-------|---------|
| **MemTotal** | Total physical RAM |
| **MemFree** | Completely unused RAM |
| **Buffers** | Block device buffers |
| **Cached** | Page cache (files mapped) |
| **SwapTotal** | Total swap space |
| **SwapFree** | Unused swap |
| **Dirty** | Memory waiting to be written to disk |
| **Mapped** | Memory-mapped files (mmap) |

## Swap
- **Swap space**: disk extension of RAM (partition or file)
- **Swapping**: entire process (old Unix) vs **paging**: pages (Linux)
- Swap out: evicts inactive pages to disk
- Swap in: page fault brings page back
- `swapoff -a` disables swap (moves pages back to RAM)
