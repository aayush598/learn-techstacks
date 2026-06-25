# Caching in I/O

## What is a Cache?
- **Cache**: smaller, faster memory that stores **copies** of frequently accessed data from slower storage
- Goal: reduce average access time (exploit **temporal** and **spatial locality**)
- Cache hit: 1-10μs (RAM); Cache miss: 5-10ms (disk) → **1000× difference**

## Write Policies

| Policy | Write to Cache | Write to Disk | Performance | Safety |
|--------|---------------|---------------|-------------|--------|
| **Write-through** | ✅ Immediately | ✅ Immediately | Slow writes | ✅ Safe (data never lost) |
| **Write-back** | ✅ Immediately | ❌ On eviction / periodic flush | Fast writes | ⚠️ Data loss if crash before flush |
| **Write-around** | ❌ Bypass cache | ✅ Direct to disk | Good for large sequential writes | ✅ Safe |

- **Write-back** is most common for page cache (Linux: `pdflush`/`writeback` flusher threads)
- **Write-through** used for critical metadata (e.g., NTFS log)
- **Write-around** used for large streaming writes (avoid cache pollution)

## Cache Replacement Policies

| Policy | Description | Pros | Cons |
|--------|-------------|------|------|
| **LRU** (Least Recently Used) | Evict oldest used item | Good temporal locality | Doesn't consider frequency |
| **LFU** (Least Frequently Used) | Evict least frequently used | Good for hot data | Starvation of new items |
| **FIFO** | First in, first out | Simple | Ignores access patterns |
| **Clock** (Second Chance) | Approximate LRU with circular list + reference bit | Efficient, no hardware support | Approximation |
| **ARC** (Adaptive Replacement Cache) | Adaptive between recency and frequency | Best overall (ZFS) | Complex |

## Linux Page Cache Architecture
- **Unified page cache**: caches both file data and block device data
- Pages: 4KB each; tracked by **radix tree** (now XArray) per address_space
- `struct address_space`: connects inode ↔ page cache ↔ block device
- Dirty pages: tracked and periodically flushed by **writeback threads** (`/sys/vm/dirty_ratio`)
- Clean pages: evicted under memory pressure via **kswapd** / **direct reclaim**

## Caching at Different Levels

| Level | Cache | Typical Size | Access Time |
|-------|-------|-------------|-------------|
| **CPU** | L1/L2/L3 | 32KB-32MB | 1-20ns |
| **OS** | Page cache | MBs-GBs | 1-10μs (if in RAM) |
| **Disk** | Disk controller RAM | MBs (16-256MB) | < 1ms |
| **RAID** | RAID controller NVRAM | GBs | < 1ms |
| **NAS** | NAS appliance cache | GBs-TBs | < 1ms |

## Key Interview Questions
- Why unified page cache? → Avoids double caching (file data in buffer cache + page cache); simpler, more memory efficient
- What is **dirty page**? → Page modified in memory, not yet written to disk
- How does Linux know when to flush? → `dirty_expire_centisecs` (age limit) + `dirty_background_ratio` (memory pressure) + `sync()`/`fsync()`
- What is **cache thrashing**? → Working set > cache size; constant eviction/reload → performance collapses
- **Buffer cache** vs **Page cache**? → Both eliminated in Linux 2.4+; unified page cache handles both file and block I/O
- How does **O_DIRECT** work? → Bypasses page cache; data transferred directly to user buffer (databases use this)
