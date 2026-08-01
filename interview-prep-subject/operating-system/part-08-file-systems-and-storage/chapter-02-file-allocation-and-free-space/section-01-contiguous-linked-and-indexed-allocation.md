# Contiguous, Linked and Indexed Allocation

> **TL;DR**: File data is allocated as **contiguous** extents (sequential-fast, external-fragmented), **linked** chains (no fragmentation, but O(n) random access), or **indexed** pointer blocks (O(1) random access, pointer overhead) — modern filesystems use **extents** plus multilevel pointers, a hybrid that gets the best of all three.

## 1. Why Does This Exist?
Given fixed-size disk blocks, the FS must decide *which blocks a file owns* and how to find them. Allocation scheme determines three conflicting goals: **sequential access speed** (contiguous = best), **random access speed** (indexed = O(1)), and **space efficiency/no fragmentation** (linked = flexible). Each scheme exists because different workloads weight these differently — and because naive choices collapse under size: a 1 GB file needs thousands of blocks, so the mapping must be compact and scalable. The history (contiguous → linked → indexed → extents) is the story of trading simplicity for scale.

## 2. How Does It Work?
- **Contiguous**: the inode stores `(start block, length)`; blocks `start..start+len−1`. Sequential access = pure streaming; random access O(1) (block = start + n). Problems: finding a contiguous run (external fragmentation, Chapter 06 analogy), growing a file means moving it.
- **Linked**: each block has a next-pointer; the inode stores the first block. Sequential = follow pointers (O(n)); random access = walk n pointers (O(n)); no fragmentation; a broken pointer = file tail lost (FAT solves this by putting links in a separate table — the **FAT**).
- **Indexed**: the inode points to an **index block** of `block size / 4` pointers. Random access = O(1) into the index; sequential = index + blocks. Pointer overhead: 1 block per ~1024 blocks (for 4 KB blocks / 4 B pointers). Large files need multi-level indices (single/double/triple indirect — Unix inode design).
- **Extents (modern)**: instead of N pointers, store variable-length runs `(start, length)` — ext4's `ext4_extent` in a tree; a few extents cover huge files; fragmentation minimized by allocation heuristics.

## 3. When Is It Used?
- **Contiguous**: tapes, some embedded/RTFS, classic OS/360; and *conceptually* every filesystem's data runs are contiguous where possible (that's what extents are).
- **Linked**: FAT/FAT32 (with the FAT as the link table), early Unix `ckd`, simple educational FS.
- **Indexed**: Unix inodes (single/double/triple indirect), NTFS's smaller attribute runs (though NTFS uses extents too), DBMS-managed data.
- **Extents**: ext4, XFS, btrfs, APFS, NTFS's `data runs` — all modern mainstream filesystems.

## 4. Why Wasn't Another Approach Chosen?
- **Contiguous alone**: elegant but kills growth and wastes space via external fragmentation — rejected as a *general* scheme (still the ideal *within* an extent).
- **Linked alone**: no fragmentation but terrible random access and pointer-reliability issues — rejected for performance.
- **Pure indexed**: O(1) random access but 0.4% pointer overhead (fine) — but large-file growth means deep indirect levels; extents reduce the metadata for sequential data.
- **Extents (chosen)**: compact (one entry per run, not per block), locality-friendly, and tree-structured for growth — the industry-standard answer; combines contiguous speed with indexed flexibility.

## 5. Intuition
- **Contiguous** = a shelf of books in one run; reach in, grab any book instantly; but if the shelf is interrupted, you can't fit the whole set.
- **Linked** = a scavenger hunt: each clue points to the next (sequential); finding clue #4000 means following 4000 clues.
- **Indexed** = a filing cabinet with a card drawer (index) listing where every folder is: open the drawer, find the folder's row, walk to it.
- **Extents** = renting *runs* of contiguous shelf space and keeping a small map of "I have shelves 10–24, 40–45, 100–112" — compact and fast.

## 6. Real-World Analogy
A library storing a 30-volume encyclopedia:
- **Contiguous**: all volumes on one consecutive shelf — anyone can read volume 22 instantly, but if the shelf has a gap, the set can't be shelved at all.
- **Linked**: each volume contains a note saying where the next volume is — reading in order is fine, but finding volume 22 means checking 21 notes.
- **Indexed**: a catalog card at the front lists the shelf of every volume — one lookup, one trip.
- **Extents**: the library shelves the set in a few long runs (vols 1–12, 13–22, 23–30) and records just those three runs.

## 7. Formal Definition
- **Contiguous allocation**: a file occupies a single contiguous run of blocks `[start, start+length)`; sequential and direct access are both O(1), but the scheme suffers external fragmentation and requires relocation or over-allocation to grow.
- **Linked allocation**: file blocks form a singly-linked chain via next-pointers (in-block or in a separate table such as the FAT); sequential access is O(n) and direct access is O(n); there is no external fragmentation and blocks may be anywhere.
- **Indexed allocation**: the inode references an index block (or multilevel index) of block pointers; direct access is O(1) (single level) or O(depth), with pointer overhead of `block_size/ptr_size` per level; external fragmentation is absent, and only index-block allocation is limited by contiguity.
- **Extent-based allocation**: files are represented as lists/trees of variable-length extents `(start block, length)`, combining contiguous-speed sequential access with flexible placement.

## 8. Example
File with 5 records (blocks) on a 4 KB-block disk:
- **Contiguous**: inode `(start=100, len=5)`. Read record 3 → block 102, offset 0: O(1). To grow to 8 blocks: need 8 consecutive — if blocks 105-106 used, must relocate the file.
- **Linked**: blocks 100→101→102→103→104, each with `next` pointer. Read record 3 → 100→101→102 (3 pointer hops) O(n). Broken pointer at 103 → tail lost.
- **Indexed**: index block has [100,101,102,103,104]. Read record 3 → index[3]=103 → O(1). Index uses 1 block per 1024 data blocks (4 KB / 4 B).
- **Extent (ext4)**: extent `{start=100, len=5}` in the inode (the `i_block` ext4_extent array). One entry covers the file; sequential access is contiguous-speed; growing appends another extent.

## 9. Internal Working
1. **Allocation**: on file creation/append, the allocator finds free blocks (Chapter 02 Sec 02), updates the inode's representation (start+len, or a chain pointer, or an index entry, or an extent).
2. **Mapping**: `block(offset)` converts a byte offset → disk block number per the scheme; the page cache issues I/O for that block.
3. **Growth**: contiguous → relocate if no space; linked → append block + fix last pointer; indexed → extend index (multi-level if huge); extents → extend the current extent or add one (ext4 prefers extending/merging).
4. **Read path**: VFS → inode mapping → block number → buffer/page cache → disk.
5. **Wear/defrag**: external fragmentation in contiguous/extent schemes is managed by allocation heuristics and offline defrag; linked/indexed avoid it.

## 10. Time Complexity
- Contiguous: direct O(1), sequential O(1) per block.
- Linked: direct O(n) (walk), sequential O(n) total; with FAT table in cache, O(n) still (following links).
- Indexed: single-level O(1); multilevel O(depth) (e.g., 3 levels covers ~1 TB with 4 KB blocks: 10+100+1000 ptrs at 1KB blocks... realistically 256/64K/16M blocks = huge).
- Extent (ext4): direct lookup O(log e) in the extent tree (e extents) — typically 1–2 levels; effectively O(1) for small files.
- Allocation search: contiguous O(n) holes; linked/indexed/extent O(1) from free bitmap.

## 11. Advantages
- **Contiguous**: best sequential throughput, O(1) random, minimal metadata.
- **Linked**: no external fragmentation, simple, blocks anywhere.
- **Indexed**: O(1) random access, no fragmentation, supports sparse files (index entries can be NULL).
- **Extents**: compact metadata, sequential speed + flexible placement, tree-scalable to huge files; sparse-file-friendly.

## 12. Disadvantages
- **Contiguous**: external fragmentation, growth requires relocation, over-allocation wastes space.
- **Linked**: O(n) random access, chain fragility, extra seek per block (pointer locality).
- **Indexed**: pointer overhead (per-block metadata), multilevel depth for huge files, index block can fragment.
- **Extents**: more complex allocator; extent-tree growth for heavily-fragmented files; ext4 extent limit → falls back to indirect blocks for very fragmented files.

## 13. Interview Questions
1. **Q: Compare contiguous, linked, and indexed allocation.** A: Contiguous: O(1) both, but external fragmentation + no growth. Linked: flexible/no fragmentation, O(n) random. Indexed: O(1) random, no fragmentation, pointer overhead + multilevel depth.
2. **Q: What is external fragmentation in a filesystem context?** A: Free space split into runs too small for a new file/contiguous requirement — the same concept as memory (Part 06) applied to disk blocks; extent schemes minimize it with allocation heuristics.
3. **Q: What is the FAT and how does it differ from per-file linked pointers?** A: The File Allocation Table is a *separate* table (per-FS) storing the next-block link for every block; files reference entries in it. It's linked allocation with the pointers centralized — recovering from a broken chain is easier, and random access is still O(n) through the FAT.
4. **Q: Why does indexed allocation support sparse files?** A: Index entries can be NULL (holes) — a 1 TB sparse file with a few GB of data uses index space, not data blocks (Chapter 01 Sec 03's sparse files).
5. **Q: What are extents and why do ext4/XFS use them?** A: Variable-length `(start, len)` runs of contiguous blocks. One extent covers many blocks → tiny metadata, sequential speed, tree-based growth; the modern answer to "how to store a huge file compactly."
6. **Q: How does random access work with linked allocation? (Tricky)** A: It doesn't — you walk the chain from block 0: O(n). That's why FAT/linked schemes are terrible for databases, which need O(1) offsets (indexed/extents).
7. **Q: What's the pointer overhead of single-level indexed allocation?** A: `block_size / pointer_size` blocks indexed per index block: 4 KB / 4 B = 1024 data blocks per index block — ~0.1% overhead, trivial; the *depth* is the issue for huge files.
8. **Q: How does ext4 grow a file beyond 15 extents?** A: The inode holds 4 extents inline; beyond that, a tree of extents (index blocks) grows — still compact vs per-block pointers.
9. **Q: Why can't you just use contiguous allocation with defragmentation? (Scenario)** A: Growth relocation is O(file) and disruptive; online defrag is expensive; and disks fill unpredictably — extents give most of the speed without the fragility.
10. **Q: Which scheme do tapes use?** A: Contiguous by nature — sequential media can't seek; files are laid out one after another (a tape is a pure contiguous stream).
11. **Q: How does NTFS store data?** A: "Data runs" — essentially extents (start VCN, length) recorded as run lists in the MFT; sparse runs and compression supported.
12. **Q: What's the trade-off between sequential I/O and fragmentation?** A: Contiguous/extents maximize sequential bandwidth (fewer seeks); fragmented files suffer per-extent seeks — SSDs (Part 08 Ch 03 Sec 03) make this moot, which is why TRIM/overprovisioning matter there.

## 14. Follow-Up Questions
1. **Q: What is "block group" allocation locality?** A: ext4 groups blocks into block groups; inodes and data blocks are placed in the same group to reduce seek distance — an allocation locality optimization.
2. **Q: What is "delayed allocation" in ext4?** A: Deferring block allocation until writeback lets the FS allocate contiguous blocks for the whole dirty region — fighting fragmentation at the source.
3. **Q: What is "preallocation" (fallocate)?** A: Reserving contiguous blocks up front for a growing file — improves contiguity and guarantees space (used by databases/video).
4. **Q: What is the multilevel indexed limit in classic Unix?** A: 12 direct + single/double/triple indirect pointers cover ~16 TB with 4 KB blocks — the design extents replaced for compactness.

## 15. Coding Example
```c
// Simulate the three allocation schemes' mapping costs
#include <stdio.h>

// linked: return block index after n hops (O(n))
int linked_map(int *chain, int first, int n) {
    int b = first;
    for (int i = 0; i < n && b != -1; i++) b = chain[b];
    return b;
}

// indexed: O(1) via index array
int indexed_map(int *index, int n) { return index[n]; }

// contiguous: O(1) arithmetic
int contig_map(int start, int n) { return start + n; }

int main(void) {
    // linked chain: block0->2->5->9->13
    int chain[16] = {2, -1, 5, -1, -1, 9, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1};
    printf("linked record 3 -> block %d (4 hops)\n", linked_map(chain, 0, 3));

    int index[] = {0, 2, 5, 9, 13};
    printf("indexed record 3 -> block %d (O(1))\n", indexed_map(index, 3));
    printf("contiguous (start=100) record 3 -> block %d (O(1))\n", contig_map(100, 3));
    return 0;
}
```

## 16. Industry Usage
- **ext4**: extents (`fs/ext4/extents.c`), delayed allocation, block groups, fallocate.
- **XFS**: B+-tree extents; AG (allocation groups); best at huge files/parallel I/O.
- **btrfs**: extent trees, COW extents.
- **NTFS**: MFT data runs (extents), sparse + compressed.
- **FAT/FAT32**: FAT table (linked allocation), still used for USB/microSD compatibility.
- **APFS**: extent-based with snapshots.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 11.4 "Allocation Methods".
- Tanenbaum, *Modern Operating Systems*, Ch. 4.3.
- Linux source: `fs/ext4/extents.c`, `fs/xfs/xfs_bmap.c`.
- ext4 docs: `Documentation/filesystems/ext4/` (extents, delayed allocation).
- `man 2 fallocate`, `man 8 e2fsck`, `man 8 fsck.ext4`.

## 18. Cheat Sheet
- Contiguous: O(1)+O(1), external fragmentation, no growth.
- Linked: no fragmentation, O(n) random (FAT = centralized links).
- Indexed: O(1) random, sparse files OK, pointer overhead + depth.
- Extents: (start,len) runs; compact; tree for huge files — ext4/XFS/btrfs/NTFS.
- ext4: 4 inline extents → extent tree; delayed allocation for locality.
- Sparse files need index/extent NULL entries.
- Tapes = contiguous; databases need indexed/extent.
- fallocate = preallocation for contiguity.
- Random access cost: contiguous O(1), linked O(n), indexed O(1).

## 19. Quiz
1. Linked allocation random access is:
   a) O(1) b) O(n) c) O(log n) d) impossible → **b**
2. The FAT stores:
   a) file contents b) next-block links for every block c) permissions d) inodes → **b**
3. Extents represent files as:
   a) one block pointer each b) (start, len) runs c) hash chains d) FIFO → **b**
4. Sparse files work with:
   a) contiguous b) linked c) indexed/extents (NULL holes) d) none → **c**
5. Contiguous allocation's main problem:
   a) pointer overhead b) external fragmentation/growth c) O(n) d) TLB → **b**
6. ext4 growth beyond inline extents uses:
   a) a linked list b) an extent tree c) the FAT d) tapes → **b**

## 20. Flashcards
- **Q: Contiguous allocation?** → **A:** One run (start,len); O(1) both; external fragmentation.
- **Q: Linked allocation?** → **A:** Blocks chained by pointers (or FAT); no fragmentation, O(n) random.
- **Q: Indexed allocation?** → **A:** Index block of pointers; O(1) random; multilevel for huge files.
- **Q: What are extents?** → **A:** Variable (start, len) runs; compact; used by ext4/XFS/btrfs/NTFS.
- **Q: Why sparse files need NULL index entries?** → **A:** Holes map to no blocks.
- **Q: Which media are contiguous by nature?** → **A:** Tapes (sequential-only).

## 21. Revision
File allocation choices trade off sequential speed, random access, and fragmentation. Contiguous runs (O(1) both, external fragmentation, no growth) → linked chains/FAT (no fragmentation, O(n) random) → indexed blocks (O(1) random, sparse support, pointer depth) → extents (variable (start,len) runs in a tree — compact, sequential-fast, scalable) which is what ext4, XFS, btrfs, and NTFS use. Modern systems couple extents with delayed allocation and preallocation for locality. Know each scheme's asymptotic costs and why extents won.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Compare the three allocation methods." | 2 How / 13 Q1 |
| "What is the FAT?" | 13 Q3 / 8 Example |
| "Why support sparse files?" | 13 Q4 / 12 Advantages |
| "What are extents and why?" | 13 Q5 / 4 Alternative |
| "How does random access differ?" | 13 Q6 / 10 Time |
| "How does ext4 grow files?" | 13 Q8 / 9 Internal |
