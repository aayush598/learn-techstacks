# Basic Pagination

## Core Concept

- **Physical memory** divided into equal-sized blocks called **frames**
- **Logical memory** divided into same-sized blocks called **pages**
- Each process's pages map to any available frame (non-contiguous)
- Eliminates external fragmentation entirely

## Address Translation

- CPU generates **logical address**: `(page_number, offset)`
- **Page table** maps page_number → frame_number
- **Physical address**: `(frame_number, offset)` — same offset, just swapped page# with frame#

```
Logical address: [ page# (p bits) | offset (d bits) ]
                        |
                        v  Page table lookup
                        |
Physical address: [ frame# | offset ]
```

### Example: 32-bit address, 4 KB page size

- Page size = 2^12 = 4096 bytes → **12-bit offset**
- Remaining 20 bits → **page number** (2^20 = 1M pages)
- `0x12345678` → page# = 0x12345, offset = 0x678

## Page Size Considerations

| Factor | Small Pages | Large Pages |
|---|---|---|
| Internal fragmentation | Less | More (last page) |
| Page table size | Larger | Smaller |
| I/O overhead | More transfers | Fewer transfers |
| TLB coverage | Less | More |

- **4 KB** is ubiquitous (x86, ARM default)
- Modern trend: **2 MB** (huge pages) for database/VMs to improve TLB reach

## Fragmentation

- **No external fragmentation:** any page fits any frame
- **Internal fragmentation:** only in last page of process (avg = half page size)
- Example: process 72 KB, page 4 KB → 18 pages → last page has 4 KB - (72 - 17×4) = 4 - 4 = 0? Actually 72/4 = 18 exactly, no waste. If 73 KB → 18 full pages + 1 KB in last page → 3 KB wasted

## Key Details

- **Frame size** = **Page size** (hardware defined, typically 4 KB)
- **Page offset** = `log2(page_size)` bits
- **Page number bits** = `address_bits - offset_bits`
- MMU performs translation on **every memory access**
- Each process has its own **page table**
- Context switch: change page table register (PTBR)
