# Free Space Management

> **TL;DR**: The FS tracks unused blocks with a **free-space bitmap** (O(1) locate + compact) or a **free list** (fast sequential allocation, coalescing needed) — with group/zone designs (ext4 block groups) localizing both allocation and its bookkeeping.

## 1. Why Does This Exist?
Every block allocation must answer "which blocks are free?" instantly. Without free-space metadata, the FS would scan the entire disk to place a file — unusable. Free-space management exists to make allocation (and release) cheap and to preserve locality (adjacent free blocks → contiguous extents → fast I/O). It also influences reliability: the bitmap is one of the first structures a crash can corrupt (hence journaling, Chapter 04 Sec 03). The design choice — bitmap vs list vs grouped — is really about the shape of the free space being tracked and how allocation requests arrive.

## 2. How Does It Work?
- **Free-space bitmap**: one bit per block (1 = free); the bitmap itself is N/8 bytes for N blocks (e.g., a 1 TB disk with 4 KB blocks = 2⁵²... 1 TB / 4 KB = 268M bits = 32 MB bitmap). Finding a free block = scan for a 1 bit (hardware `bsf`/`ffs` makes this fast); release = clear the bit.
- **Free list (linked)**: free blocks chained via a `next` pointer stored inside each free block (the disk is its own index). Allocation pops the head — O(1); but no contiguity info without coalescing scans, and updates are not atomic (crash risks).
- **Grouping/counting**: the free list groups blocks by counting runs (like extents); a "counted free list" stores `(start, count)` entries — fewer entries, better locality, and fast contiguous allocation.
- **Group/zone designs**: ext4 divides the disk into block groups, each with its own bitmap — allocation stays local (metadata + data in the same group), reducing seeks and scaling the bitmap.

## 3. When Is It Used?
- **Bitmaps**: ext4/XFS/btrfs block group bitmaps; NTFS $Bitmap; virtually all modern filesystems (bitmaps are the standard).
- **Free lists**: FAT-style systems historically, educational FS, some log-structured filesystems (which track free extents differently).
- **Counted/grouped**: ext4's buddy-like per-group free counts; XFS AG freespace B-trees.
- **SSD context**: TRIM uses a bitmap-like model (logical block state); overprovisioning sets aside hidden free blocks (Part 08 Ch 03 Sec 03).

## 4. Why Wasn't Another Approach Chosen?
- **Bitmap (chosen standard)**: O(1) locate via bit ops, compact (1/32768 of disk for 4 KB blocks: 32 MB/TB), easy to snapshot/journal; slight drawback: allocation is a scan (fast with `ffs`) and the bitmap itself needs writing.
- **Free list**: O(1) head allocation, but no contiguity/locality, non-atomic updates, and fragmented allocation — rejected for general use.
- **Counting (chosen hybrid)**: `(start,count)` runs in memory (ext4's per-group `free_clusters` buddy) — combines list compactness with contiguous allocation.
- **Tree-based (XFS, btrfs)**: B-trees of free extents — O(log n) with good locality and scalability to huge disks; the high-end choice.
- **Nothing (mark blocks at format time, never reuse)**: impossible at scale.

## 5. Intuition
A parking garage with numbered spots and a **dashboard of LED lights** (bitmap): one light per spot, green = empty. Finding a spot = glance at the board (scan bits); parking = flip the light. A **free list** is like a chain of "this spot is empty — the next empty one is #427" notes left in the spots themselves. Grouped designs are like floor-by-floor boards (block groups) so you can check just one floor instead of the whole building.

## 6. Real-World Analogy
A hotel's **room availability board**: a grid of rooms with vacant/occupied markers (bitmap). Housekeeping updates it instantly; finding a free room is reading the board. The counted-list variant is the front-desk's "wings with contiguous vacancies" list — great for when a big group (contiguous allocation) checks in at once.

## 7. Formal Definition
**Free-space management** is the subsystem that records which disk blocks are unallocated. In a **bitmap** (or bit vector), block i's availability is bit i (1 = free); allocation locates a free bit (O(1) with bit-scan instructions, O(n) worst-case scan) and release clears it. In a **free list**, free blocks are linked together via pointers stored within them; allocation and release are O(1) but lose locality information. A **counting** variant stores `(start block, count)` runs (or B-tree of extents) for compactness and contiguous allocation. Grouped designs (ext4 block groups) maintain per-group bitmaps and counts to keep allocation local and scalable.

## 8. Example
Disk with 16 blocks; bitmap = `1110011110111011` (bits 0..15; 1=free).
- Free blocks: 0,1,2,5,6,7,8,10,11,14,15 (11 free).
- Allocate one block: scan for first 1-bit → block 0 → set bit 0 → `0110011110111011`.
- Allocate a contiguous run of 3: find 3 consecutive 1-bits → blocks 5,6,7 → `0110000110111011`.
- Release block 3: `1110000110111011`.
- Counted list representation of the same: `(0,3),(5,4),(10,2),(14,2)` — 4 entries vs 16 bits: allocation of a run = find an entry with count ≥ request.

ext4 scale: 1 TB, 4 KB blocks, 256 MB... 1 TB / 4 KB = 268,435,456 blocks → 32 MB bitmap (0.003%), split into block-group bitmaps (typically 8 MB groups of 128 MB → 32 KB bitmap each, stored inline in the group).

## 9. Internal Working
1. **Bitmap read**: the group's bitmap block is read into memory (cached); per-group `free_count` tracks availability without scanning.
2. **Allocate**: `mb_find_free_blocks` (ext4 mballoc) — scan bitmap for run ≥ request; prefer locality (same group as inode / previous allocation); use the buddy allocator for power-of-two sizes.
3. **Update**: flip bits, decrement group count, update the buddy structures; the bitmap block is a *metadata block* → journaled (ext4) so a crash won't double-allocate.
4. **Release**: on unlink/truncate, `mb_free_blocks` — flip bits, coalesce with neighbors in the buddy.
5. **Persistence**: bitmap blocks are read/written through the page cache and journal; fsck reconstructs them from inodes if corrupted.
6. **TRIM (SSD)**: the FS informs the device of freed logical blocks (fstrim/discard) so the SSD can erase/overprovision — free-space *propagation* to the device.

## 10. Time Complexity
- Bitmap locate: O(1) with `bsf`/word-scan; worst-case O(bits/word) = O(n/64).
- Bitmap update: O(1).
- Free list pop: O(1); coalescing: O(neighbors).
- Counted/B-tree (XFS `xfs_allocbt`): O(log n).
- ext4 buddy: O(log group) for power-of-two; O(n) worst for irregular runs.
- Group locality: O(1) per group lookup.

## 11. Advantages
- **Bitmap**: compact (0.003% overhead), O(1) locate/update, trivial to journal and fsck.
- **Free list**: minimal metadata, O(1) allocation (head).
- **Counted/grouped**: contiguous-run allocation without scanning; per-group locality (fewer seeks); buddy allocator for speed.
- **B-tree (XFS/btrfs)**: scalable to huge disks, ordered by address → contiguous allocation trivial.
- Bitmap + journal = crash-safe double-allocation prevention.

## 12. Disadvantages
- **Bitmap**: needs a scan for runs (mitigated by buddy/group counts); bitmap blocks are hot metadata (cache pressure, write amplification).
- **Free list**: no locality info, non-atomic (crash → lost free space), fragmented allocation.
- **Counted/B-tree**: more complex, more memory for the index, recovery complexity.
- All schemes: must stay consistent with inodes — corruption = lost/overlapped space (fsck's job).
- TRIM/discard requires the FS and SSD to agree on freed ranges.

## 13. Interview Questions
1. **Q: What is a free-space bitmap?** A: One bit per disk block (1=free); allocation scans for a 1-bit, release clears it. Compact and fast (O(1) with bit-scan).
2. **Q: How much space does a bitmap take?** A: 1 bit per block = disk_size / (block_size × 8) — a 1 TB disk with 4 KB blocks needs ~32 MB (0.003%).
3. **Q: What is a free list and its drawback?** A: Free blocks linked by next-pointers stored inside them; O(1) pop, but no locality/contiguity info, non-atomic updates, and no coalescing without scans.
4. **Q: What's a counted free list?** A: Stores `(start, count)` runs instead of single blocks — compact and enables contiguous-run allocation; the precursor of extent-based free structures.
5. **Q: Why does ext4 use block groups? (Tricky)** A: Each group has its own bitmap + inode table — allocation stays local (inode + data blocks in one group = fewer seeks), the bitmap scales, and group-level free counts make "any free block?" O(1) per group.
6. **Q: How does the FS avoid allocating the same block twice? (Production)** A: Bitmap + journaling: the bitmap update is a journaled metadata transaction, so a crash replays or rolls back — no double-allocation. fsck repairs inconsistencies.
7. **Q: What's the difference between bitmap and buddy allocator?** A: The bitmap is the source of truth; the buddy is an in-memory power-of-two index over it for fast contiguous allocation (ext4's mballoc uses both).
8. **Q: What is TRIM/discard and why does it matter for SSDs?** A: The FS tells the SSD which logical blocks are free so the device can erase/consolidate them — without TRIM, SSDs stall on garbage collection (Part 08 Ch 03 Sec 03).
9. **Q: What happens if a free list is corrupted?** A: Blocks leak or get double-allocated — fsck reconstructs free space by scanning inodes; bitmaps are more robust because each bit is self-describing.
10. **Q: How does allocation preserve locality?** A: Allocate from the same block group as the inode, extend the current extent, and use the buddy for aligned runs — keeping sequential files contiguous.
11. **Q: Why is the free-space metadata "hot"?** A: Every allocation/release touches it; on busy filesystems the bitmap blocks are cache-pinned and journaled — a write-amplification source on SSDs.
12. **Q: How do XFS/btrfs scale free-space tracking?** A: B-trees of free extents ordered by address — O(log n) lookups, naturally support contiguous allocation, and scale to petabytes (better than a flat bitmap).

## 14. Follow-Up Questions
1. **Q: How does ext4's mballoc work?** A: Multi-block allocator: scans the group bitmap with buddy structures, keeps per-CPU locality caches (`mb_group_locality`) for fast repeated allocation.
2. **Q: What's the relationship between free-space management and filesystem check (fsck)?** A: fsck rebuilds free space by walking inodes and reconstructing which blocks are used — detecting bitmap/inode mismatches.
3. **Q: What is "discard" mode vs fstrim?** A: Continuous discard passes TRIM on every free; `fstrim` batches it periodically (SSD-friendly, avoids churn on busy systems).
4. **Q: How does a log-structured FS track free space?** A: LFS treats the disk as a log; free space is found by segment cleaning (garbage collection) — free-space management becomes segment-level (Chapter 04 Sec 03).

## 15. Coding Example
```c
// Free-space bitmap: allocate a run of n blocks, free a block
#include <stdio.h>
#include <string.h>

#define NBLOCKS 64
unsigned long long bitmap = 0xFFFF;   // first 16 blocks free

int alloc_run(int n, int *start) {
    int run = 0;
    for (int i = 0; i < NBLOCKS; i++) {
        if (bitmap & (1ULL << i)) run++;
        else run = 0;
        if (run == n) {
            *start = i - n + 1;
            for (int j = *start; j <= i; j++) bitmap &= ~(1ULL << j);
            return 0;
        }
    }
    return -1;   // no contiguous run
}

void free_block(int i) { bitmap |= (1ULL << i); }

int main(void) {
    int s;
    if (alloc_run(3, &s) == 0) printf("allocated run of 3 at block %d\n", s); // 0
    printf("bitmap now: 0x%llx\n", bitmap);
    free_block(s);
    printf("after free: 0x%llx\n", bitmap);
    return 0;
}
```

## 16. Industry Usage
- **ext4**: per-block-group bitmaps + mballoc (buddy), `Documentation/filesystems/ext4/group-descr.rst`.
- **XFS**: AG freespace B-trees (`xfs_allocbt`).
- **btrfs**: extent trees + free-space cache.
- **NTFS**: `$Bitmap` file.
- **FAT**: a variant — the FAT itself encodes both allocation *and* free (0x0000 = free) — elegant single structure.
- **SSDs**: TRIM/`fstrim`, overprovisioning, NVMe deallocate — free-space propagation to the device.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 11.5 "Free-Space Management".
- Tanenbaum, *Modern Operating Systems*, Ch. 4.3.3.
- Linux source: `fs/ext4/mballoc.c`, `fs/xfs/xfs_alloc.c`, `Documentation/filesystems/ext4/`.
- `man 8 fstrim`, `man 8 e2fsck`.

## 18. Cheat Sheet
- Bitmap: 1 bit/block; 1 TB/4 KB → 32 MB (0.003%).
- Free list: next-pointers in free blocks; O(1) but no locality.
- Counted list: (start,count) runs — contiguous allocation.
- ext4: per-group bitmaps + mballoc buddy + locality caches.
- XFS/btrfs: B-tree of free extents — O(log n), petabyte-scale.
- Journaling makes bitmap updates crash-safe (no double-alloc).
- TRIM/fstrim tells SSDs which blocks are free.
- fsck rebuilds free space from inodes if corrupted.
- FAT uses 0x0000 entry = free (allocation + free in one table).

## 19. Quiz
1. A free-space bitmap uses:
   a) 1 byte/block b) 1 bit/block c) 1 pointer/block d) nothing → **b**
2. A 1 TB disk, 4 KB blocks → bitmap ≈
   a) 4 MB b) 32 MB c) 256 MB d) 1 GB → **b**
3. A free list's main drawback:
   a) memory cost b) no locality/contiguity info c) slow updates d) journaling → **b**
4. ext4 allocates with:
   a) free list only b) mballoc (bitmap + buddy + locality) c) FAT d) tape → **b**
5. XFS tracks free space with:
   a) bitmaps b) B-trees of extents c) free lists d) FAT → **b**
6. TRIM tells:
   a) the FS b) the SSD which blocks are free c) the CPU d) the network → **b**

## 20. Flashcards
- **Q: Free-space bitmap?** → **A:** 1 bit per block; locate free via bit scan; ~0.003% overhead.
- **Q: Free list?** → **A:** Free blocks linked by in-block pointers; O(1) but no locality.
- **Q: Counted free list?** → **A:** (start,count) runs for contiguous allocation.
- **Q: Why block groups?** → **A:** Local allocation (inode+data near), scalable bitmaps.
- **Q: How do XFS/btrfs scale?** → **A:** B-trees of free extents, O(log n).
- **Q: What's TRIM?** → **A:** FS → SSD free-block notification for wear/GC.

## 21. Revision
Free-space management tracks unallocated blocks so allocation is fast. The bitmap (1 bit/block, ~0.003% overhead, O(1) locate) is the standard, organized per-block-group for locality and scale (ext4 mballoc adds a buddy allocator); XFS/btrfs use B-trees of free extents for petabyte scale. Free lists are O(1) but locality-blind and fragile. Journaling makes bitmap updates crash-safe, fsck rebuilds them after corruption, and TRIM propagates freed blocks to SSDs. The design goal everywhere: find blocks fast *and* keep them contiguous for I/O locality.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a free-space bitmap?" | 2 How / 13 Q1-2 |
| "What is a free list and its drawback?" | 13 Q3 / 12 Disadvantages |
| "Why does ext4 use block groups?" | 13 Q5 / 3 When |
| "How do you avoid double-allocation?" | 13 Q6 / 9 Internal |
| "What is TRIM and why does it matter?" | 13 Q8 / 16 Industry |
| "How do XFS/btrfs scale free-space?" | 13 Q12 / 4 Alternative |
