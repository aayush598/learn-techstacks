# Free-Space Management

## Bit Vector (Bitmap)
- **n bits** for n blocks; `1` = free, `0` = allocated
- **Pros**: simple, efficient for finding contiguous free blocks
- **Cons**: must keep in memory (or cached) for performance
- Finding first free block: scan for `1`; CPU has bit-scan instructions (`BSF`)
- Used in: **ext4**, **NTFS**, most modern FS
- Must be **kept in sync** with on-disk version

## Linked List (Free List)
- First free block points to next free block
- **Free block pointer** stored in super block
- **Pros**: only needs pointer to first free block in memory
- **Cons**: **poor fragmentation** (no contiguous allocation), traversal is slow
- Not commonly used as primary method

## Grouping (Modified Linked List)
- Store **addresses of n free blocks** in the first free block
- First n-1 blocks are actually free; last block points to next group
- **Pros**: faster free block traversal, easy to allocate multiple free blocks
- **Hybrid of linked list + bitmap benefits**

## Counting
- Track **(block number, count)** for runs of contiguous free blocks
- **Extent-based**: maintain list of free extents
- **Pros**: efficient when free space is contiguous
- **Cons**: list can grow large if filesystem is fragmented
- Used in: **ext4** (combined with bitmap)

## SSD-Specific: TRIM/Discard
- **Problem**: SSD must erase entire block before writing (write amplification)
- **TRIM command**: OS tells SSD which blocks are no longer in use
- **Discard**: Linux `fstrim` issues TRIM for all free blocks
- Without TRIM: SSD unaware of free blocks → garbage collection overhead
- **`-o discard`** mount option: TRIM on every file deletion (performance impact)

## Performance Trade-offs

| Method | Memory | Allocation Speed | Contiguous Alloc | Used In |
|--------|--------|------------------|------------------|---------|
| **Bitmap** | High (n bits) | Fast (scan) | ✅ Good | ext4, NTFS |
| **Linked list** | Low (1 ptr) | Slow (traverse) | ❌ Poor | Old Unix |
| **Grouping** | Low (1 ptr) | Moderate | ❌ Poor | Some Unix |
| **Counting** | Moderate | Fast | ✅ Excellent | ext4 |

## Key Interview Questions
- How does `free` command show free space? → Filesystem reports via `statfs()` syscall
- What happens when free space is fragmented? → New files get striped across disk; performance degrades
- **TRIM** on HDD vs SSD? → HDD doesn't need TRIM (overwrite in place); SSD must erase before write
- How does ext4 allocate blocks? → **Buddy allocator** on block groups; tries to allocate in same group as inode
