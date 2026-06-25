# Direct Memory Access (DMA)

## Problem DMA Solves
- **PIO** (Programmed I/O): CPU moves each byte between device and memory
- For large transfers (disk, network, GPU): PIO **wastes CPU** that could be doing useful work
- **DMA**: device transfers data directly to/from memory, CPU is free

## How DMA Works
1. CPU programs **DMA controller** with: **source address**, **destination address**, **byte count**
2. CPU issues "start transfer" command to device
3. DMA controller manages data movement on the **bus**
4. DMA controller sends **interrupt** when transfer completes
5. CPU handles interrupt (knows data is ready)

```
CPU → DMA Controller (setup: src, dest, count)
        ↓
Device ↔ Memory (via DMA, CPU free to compute)
        ↓
DMA → CPU (interrupt: transfer complete)
```

## DMA Modes

| Mode | Description | Impact |
|------|-------------|--------|
| **Burst mode** | DMA transfer happens in one burst; CPU suspended for entire transfer | Blocks CPU, fast transfer |
| **Cycle stealing** | DMA steals one bus cycle at a time, interleaved with CPU | Minimal CPU slowdown |
| **Transparent mode** | DMA uses bus only when CPU not using it | No CPU slowdown, slower transfer |

## Scatter-Gather DMA
- Transfer data to/from **multiple discontiguous memory buffers** in one operation
- DMA controller reads a **descriptor list** (linked list of `{address, length}` entries)
- Eliminates need for **data copying** (no "bounce buffer")
- Used in: **high-performance NICs**, **NVMe drives**, **GPU transfers**

## DMA vs PIO

| Aspect | PIO | DMA |
|--------|-----|-----|
| **CPU usage** | 100% during transfer | Setup only (then free) |
| **Transfer rate** | Limited by CPU speed | Limited by bus/device speed |
| **Complexity** | Simple | Complex (DMA engine, cache coherency) |
| **Best for** | Small transfers (< ~1KB) | Large transfers (> ~1KB) |
| **Example** | Early ATA (PIO mode) | NVMe, SATA (DMA mode) |

## DMA Considerations
- **Cache coherency**: DMA writes memory directly; CPU cache may have **stale data**
  - Solutions: **cache flushing** (before DMA read), **coherent DMA** (uncached memory), **IOMMU**
- **Bus mastering**: modern devices have integrated DMA engine (bus master)
- **IOMMU** (I/O Memory Management Unit): translates device virtual addresses to physical; provides **protection** and **isolation** (used in virtualization)
- **Bounce buffers**: on 32-bit systems, DMA buffer must be in low memory (< 4GB) for legacy devices; data copied via **bounce buffer**

## Key Interview Questions
- Why use DMA for disk, but PIO for keyboard? → Disk transfers are large (4KB+); keyboard is 1 byte at a time — DMA setup overhead not worth it
- What is **cache coherency** problem with DMA? → DMA writes memory, but CPU cache holds old copy → data inconsistency
- How does scatter-gather DMA improve performance? → Avoids copying scattered buffers into one contiguous buffer
- What is **IOMMU**? → Like MMU for devices; maps device DMA addresses to physical memory; provides isolation in VMs
- What is **DDIO**? → Intel Data Direct I/O; DMA transfers directly to/from CPU cache (L3), bypassing main memory
