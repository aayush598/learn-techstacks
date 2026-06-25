# Hierarchical (Multilevel) Page Tables

## Problem

- 32-bit address, 4 KB pages → 2^20 = **1M pages** per process
- Each PTE = 4 bytes → page table = **4 MB** contiguous per process
- Contiguous 4 MB allocation is wasteful and hard to satisfy
- Most page table entries are **invalid** (sparse address space)

## Two-Level Paging

- **Page the page table itself**: outer page table points to inner page tables
- Inner page tables are allocated only for **valid regions**

### 32-bit Example: 4 KB pages, 4-byte PTEs

```
Address: [ outer page (10 bits) | inner page (10 bits) | offset (12 bits) ]
```

- 10 bits → 2^10 = 1024 entries in outer table
- Outer PTE → points to a 4 KB inner page table (1024 entries × 4 bytes)
- Inner PTE → frame number
- Only outer table + active inner tables need memory

**Before:** 4 MB contiguous (1M entries)
**After:** 4 KB (outer) + n × 4 KB (inner) where n = number of active regions

## Address Translation Steps

1. Extract outer page# (p1) from logical address
2. Index outer page table → get inner page table base
3. Extract inner page# (p2) → index inner page table → get frame#
4. Combine frame# + offset → physical address

**Memory accesses per translation:** 3 (outer PT + inner PT + data)

## Three-Level and Four-Level Paging

- 64-bit address space is **enormous** (2^64 bytes)
- Even with 4 KB pages → 2^52 pages → absurd
- More levels reduce each table size

### x86-64 4-Level Paging

```
[ PML4 (9) | Directory Ptr (9) | Directory (9) | Table (9) | Offset (12) ]
```

| Level | Name | Bits |
|---|---|---|
| L4 | PML4 | 9 (512 entries) |
| L3 | Page Directory Pointer | 9 (512 entries) |
| L2 | Page Directory | 9 (512 entries) |
| L1 | Page Table | 9 (512 entries) |
| Offset | — | 12 |

- Each table is exactly **one page** (4096 bytes / 8 bytes per entry = 512 entries)
- 48-bit virtual address (sign-extended to 64), leaving 16 bits unused
- **5-level paging** (57-bit) introduced for even larger systems

## Trade-offs

| Pros | Cons |
|---|---|
| Saves memory (sparse PTs) | More memory accesses per translation |
| Scales to 64-bit | TLB miss is more expensive |
| No contiguous PT requirement | Slightly more complex hardware |

## TLB Miss Handling

- Hardware **page table walker** traverses levels automatically
- x86 does hardware TLB miss handling (no OS intervention for regular pages)
- OS only handles **page faults** (invalid entries)
