# Linux Filesystems: ext4, XFS, btrfs

> **TL;DR**: ext4 is the default (inodes + extents + journaling); XFS scales to huge files with B-tree extents; btrfs is copy-on-write with subvolumes, snapshots, and checksums. They differ in allocation strategy, metadata structure, and crash-safety design, all under the same VFS.

## 1. Why Does This Exist?
A filesystem has to solve: *where* do file bytes live (allocation), *how* do I find them fast (metadata: inode/directory), *how* do I survive crashes (journaling/CoW), and *how* do I scale (huge files, huge volumes, many files). ext2/ext3 answered the basics; ext4 added extents and better allocation; XFS was built for large, parallel filesystems; btrfs brought the ZFS-style "copy-on-write, snapshots, checksums" model to mainline Linux. Different workloads (small files vs huge files, enterprise vs desktop, snapshot-heavy) need different structures — that's why Linux ships many and the VFS lets them coexist.

## 2. How Does It Work?
**ext4** (default since RHEL 6 / Ubuntu 9.10):
- On-disk layout: boot block, superblock (duplicated), group descriptors, **block groups** (each with its own inode table + block bitmap + inode bitmap), data blocks.
- **Inodes**: fixed-size (256 bytes) records holding mode, owner, timestamps, size, block counts, and **15 block pointers** → 12 direct, 1 indirect, 1 double, 1 triple. Plus **extents** (since ext4): instead of 12 direct pointers, the first 4 slots can be a small extent tree: `[start, len]` pairs that map contiguous ranges (a 128 MB contiguous file fits in one extent entry).
- **Extents**: `struct ext4_extent { ee_block, ee_len, ee_start_hi, ee_start_lo }` — 12 bytes per extent; an inode's `i_block` area holds up to 4 extents inline, else an extent index tree (B-tree-like).
- **Journaling**: default `data=ordered` — data written to file first, then metadata+pointers journaled; `data=journal` journals everything; `data=writeback` fastest, least safe.
- Allocation: **multiblock allocation**, delayed allocation (`delalloc`), **flex_bg** (multiple block groups per flex group for locality), online defrag, orphan inode tracking.
- Delayed allocation: `write()` just marks page dirty; actual blocks allocated at `writeback` time → better contiguous layout (extents) but risk of ENOSPC surprise at flush.

**XFS**:
- **B-tree** index for every metadata structure: inode B-trees, extent B-trees, free-space B-trees (bno, cnt), reverse-mapping (rmap, optional), and the **AG (allocation group)** structure — 8+ groups, each independently allocatable → parallelism.
- **Extent-based** allocation from the start; designed for large files/systems (up to 8 EB theoretical, 16 TB files classic; practical large volumes).
- **Delayed allocation** (from day one), preallocation, and **dynamic inodes** — inodes allocated on demand (no fixed inode table).
- Journaling via log (`xfs_log`), with metadata checkpointing; **no data journaling** (data via delalloc + ordered).
- `xfs_growfs` online grow, online defrag/repair (`xfs_scrub`).

**btrfs**:
- **Copy-on-write (CoW)**: every write allocates new blocks; old blocks stay until no longer referenced → **snapshots** for free (a snapshot is a new root referencing old blocks).
- On-disk: **B-trees** (extent trees, inode trees, checksum trees, free-space) in **subvolumes** — subvolumes are independent filesystem roots mountable/nestable.
- **Checksums** (crc32c, xxhash, sha256) on every block, checked on read → detects bit-rot.
- **Data checksums + RAID** (btrfs raid1/raid5/raid6/raid10 with scrub).
- **Compression** (lzo/zstd/zlib) inline, transparent.
- Auto-defrag, **balance/rebalance**, logical volume management built-in (no LVM needed), COW disabled for database files (`nodatacow`).

## 3. When Is It Used?
- **ext4**: default root/home for most distros; general-purpose.
- **XFS**: RHEL/CentOS/Fedora default since RHEL 7; parallel FS on large storage (up to hundreds of TB); workloads with big files (media, HPC).
- **btrfs**: Fedora/openSUSE default (subvolumes for snapshots/rollback), NAS appliances, snapshot-happy setups; ZFS-alternative for Linux.

## 4. Why Wasn't Another Approach Chosen?
- **ext3 (superseded)**: block-pointer inodes → huge files need huge indirect trees; no extents, no delalloc → fragmentation; slow fsck on large volumes (full-tree scan).
- **ReiserFS**: innovative B-tree, but fragile + stagnant; ext4 won the "next default" contest.
- **JFS/HPFS**: niche, low adoption on Linux.
- **ZFS**: licensed (CDDL) — couldn't be mainline Linux; btrfs became the in-tree answer (both are CoW+B-tree+checksums).
- **Classic linked-list blocks (FAT-like)**: too slow for random access; rejected by all modern designs.
- **XFS vs ext4 for default**: XFS won in RHEL 7 for scalability; ext4 won in Debian/Ubuntu for maturity/simplicity.

## 5. Intuition
**A library with a card catalog**: ext4 = fixed catalog cards (inodes) in fixed drawers (block groups), where a book's contents list is a chain of "next page" entries (block pointers) with shortcuts for long contiguous runs (extents). XFS = the catalog is split into many separate rooms (AGs), each self-contained with its own B-tree indexes, so many librarians can work at once. btrfs = every edit to the catalog is a *new page* (CoW), so the library always has the old catalog page intact — snapshots are just "keep the old page" — and every page has a checksum so nobody can silently alter a book.

## 6. Real-World Analogy
**A writer's notes**: ext4 keeps a master list per chapter (inode) with links to each page; long straight passages get compressed into "pages 40–120" (extents). XFS organizes by chapter into separate boxes (AGs), each with its own index cards — parallel editing works. btrfs never edits an existing page — every change writes a fresh copy (CoW), which means you can always "undo" to the previous snapshot, and every page is fingerprint-checked (checksum) so tampering/bit-rot is caught.

## 7. Formal Definition
**ext4**: block-group layout; 256-byte inodes; 12 direct + indirect/double/triple pointers **or** extent trees (`ee_block/ee_len/ee_start`); `journaling` (JBD2) with `data=ordered/writeback/journal`; delayed + multiblock allocation; flex_bg; 16 TB–1 EB (64-bit feature) max; extents in a B-tree for large files.
**XFS**: allocation groups (AG) each with bno/cnt B-trees + inode B-trees + extent B-trees; delayed allocation; 64-bit block numbers; up to 8 EB; log = circular transaction log with checkpointing; no data journal.
**btrfs**: COW B-tree ("btree" over blocks); subvolumes (independent roots); extent/dir/checksum/root trees; checksums (crc32c/xxhash/sha256) on data+metadata; snapshots (copy-on-write of the root node); RAID via the FS; compression; balance.

## 8. Example
- **ext4**, file of 200 KB contiguous on a 4 KB-block FS = 50 blocks → one extent `[start=0x1000, len=50]` in the inode (fits in the inline 4 extent slots). Same file scattered → extent tree, maybe 8 extents. **Compare**: ext3 would store 50 pointers + indirect blocks.
- **XFS**, a 10 TB media file: one extent record covers huge contiguous runs; AG-level B-trees find free space quickly; `xfs_growfs` grows a mounted FS.
- **btrfs**, `snapshot` of `/home` every hour: each snapshot = a new root pointing at the same blocks; after editing one file, only that file's blocks + tree nodes are new; `btrfs balance` rebalances; `btrfs scrub` verifies checksums and repairs from RAID1 mirror; a corrupted sector on one disk is transparently replaced from the mirror.

## 9. Internal Working
1. VFS routes `open/read/write` → `ext4_file_operations` / `xfs_` / `btrfs_`.
2. `write()` (ext4): marks page cache dirty (delayed alloc); at flush, `ext4_mb_new_blocks` allocates extents, `ext4_ext_map_blocks` maps, JBD2 journal records the metadata changes.
3. Crash consistency (ext4): journal descriptor + metadata blocks written to log; commit record forces to disk; on mount, replay journal → metadata consistent (data=ordered ensures data hits disk before commit).
4. XFS: transactions (`xfs_trans_*`) → log record → checkpoint to B-trees; `xfs_log_force` on sync.
5. btrfs: write → COW: allocate new block, write data, update checksum tree, update extent tree, update inode tree → write new root node; commit transaction (tree roots) → block group free space updated.
6. Readahead / allocation decisions done by each FS's `->get_block`/`->writepages`; all coordinated by the VFS `address_space` (Section 04).

## 10. Time Complexity
- ext4 inode lookup: O(1) in group (inode table index) → + extent tree O(log e) for extents (e = extents).
- ext3 pointer chain: O(blocks) for indirect — that's why ext4 extents matter (direct map for contiguous).
- XFS metadata: O(log n) B-tree ops; AG parallelism scales with cores/disks.
- btrfs: O(log n) B-tree updates per COW write; snapshot = O(1) (new root) + O(tree height) on subsequent writes; checksum verify O(size).
- fsck: ext3/4 fast in practice (per-group bitmaps); XFS `xfs_repair` parallel per-AG; btrfs scrub streams checksums.

## 11. Advantages
- **ext4**: stable, simple, ubiquitous; fast for typical workloads; extents cut fragmentation; journaling.
- **XFS**: scales to enormous files/volumes; parallel AG allocation; online grow; strong on big sequential workloads.
- **btrfs**: snapshots (cheap, instant), checksums catch bit-rot, RAID+scrub, compression, subvolumes, no LVM needed.
- **VFS layer**: all coexist, mount everywhere, `mount -o` per-FS options.

## 12. Disadvantages
- **ext4**: max file size / volume smaller than XFS; no checksums (silent bit-rot undetected); fsck needs unmount (except online defrag).
- **XFS**: no metadata/data checksums (rmap needed for robust repair); data journaling absent; small-file heavy dirs less optimal than ext4 in some cases; historically slow to shrink.
- **btrfs**: CoW + snapshots can fragment / surprise ENOSPC (old snapshots hold blocks); performance overhead of CoW+checksums on some workloads; had historical bugs (though now very stable); RAID5/6 historically risky (now improved); complex.
- **All**: delalloc means `write()` success ≠ durable until `fsync` — application must know sync semantics.

## 13. Interview Questions
1. **Q: ext4 vs ext3?** A: extents (replace block-pointer chains), delayed allocation, multiblock allocation, flex_bg, larger limits (1 EB vs 16 TB), online defrag — same on-disk family, better layout + performance.
2. **Q: What is an extent?** A: `[start block, length]` — one record for a contiguous run; a 50-block contiguous file is *one* extent instead of 50 pointers. Enables large contiguous allocation and fast lookup.
3. **Q: ext4 journaling modes?** A: `data=ordered` (default: data written before metadata commit — consistency without double-write), `data=journal` (everything journaled — safest, slowest), `data=writeback` (metadata only, ordering loose — fastest, less safe).
4. **Q: XFS vs ext4?** A: XFS = AG-based B-tree structures, extent-only, dynamic inodes, better for huge files/volumes + parallel workloads; ext4 = block-group inodes, simpler, better for small files / maturity. RHEL picked XFS; Debian picked ext4.
5. **Q: What is copy-on-write (CoW)?** A: Writes allocate *new* blocks instead of overwriting — old blocks preserved → snapshots free, no overwrite-corruption (crash-safe), checksums stay valid; btrfs/ZFS model.
6. **Q: What are btrfs subvolumes and snapshots?** A: A subvolume = independent root (mountable, nestable); a snapshot = a new root referencing the same blocks (O(1)); after writes only changed blocks are new — rollback = mount the old root.
7. **Q: Why checksums in btrfs but not ext4/XFS?** A: Detect silent corruption (bit-rot, failing drives) on *read* and repair from RAID mirrors/parity (scrub). ext4/xfs assume hardware correctness — mostly true but unsafe for long-term archives.
8. **Q: What is delayed allocation?** A: `write()` only marks pages dirty; real block allocation happens at flush → better contiguous layout (bigger extents), fewer seeks — but a late ENOSPC possible and `fsync` cost is real.
9. **Q: What are block groups / allocation groups?** A: ext4 splits the volume into block groups each with own inode table + bitmaps (locality); XFS splits into AGs each independently allocatable (parallelism + partial-failure isolation).
10. **Q: Why does btrfs sometimes "run out of space" with free space showing?** A: CoW + snapshots + fragmentation: free space exists but as scattered blocks, or old snapshot versions pin blocks — the classic btrfs surprise; solved by balance/defrag and careful snapshot policy.
11. **Q: XFS data vs metadata journaling?** A: XFS journals *metadata* only (transactions) with delayed allocation for data; crash gives consistent metadata, data may be stale but not corrupt — similar to ext4 data=writeback.
12. **Q: How do these all work under the VFS?** A: Each provides `->sops/->iops/->fops/->dops`; the VFS is the common `struct inode/dentry/file/super_block` machinery (Section 04), so `open("file")` is FS-agnostic.

## 14. Follow-Up Questions
1. **Q: What is a flex_bg?** A: ext4 groups several block groups into one "flex group" sharing bitmaps — reduces metadata seeks for small-file workloads.
2. **Q: What is an orphan inode?** A: An inode whose last link was removed while open; ext4 tracks orphans so the journal can clean up on recovery.
3. **Q: What is `xfs_scrub`?** A: Online verification (checks metadata structure + integrity, cross-checks with rmap); repairs from redundancy.
4. **Q: btrfs `nodatacow`?** A: Per-file or per-dir CoW disable — for database files where CoW causes fragmentation and surprising writes; trade snapshot-ability for layout stability.

## 15. Coding Example
```c
// ext4: an extent in the inode (struct ext4_extent layout, abbreviated)
#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint32_t ee_block;   // first logical block of the extent
    uint16_t ee_len;     // number of blocks covered
    uint16_t ee_start_hi;
    uint32_t ee_start_lo; // physical start block
} ext4_extent;

// map a logical block within a file to a physical block via an extent list
uint64_t extent_lookup(ext4_extent *exts, int n, uint32_t lblock) {
    for (int i = 0; i < n; i++) {
        if (lblock >= exts[i].ee_block &&
            lblock < exts[i].ee_block + exts[i].ee_len)
            return ((uint64_t)exts[i].ee_start_hi << 32 | exts[i].ee_start_lo)
                   + (lblock - exts[i].ee_block);
    }
    return (uint64_t)-1;  // hole / not found
}

int main(void) {
    // file with two extents: [0,100] and [120,40] (100 KB file + a 40-block run)
    ext4_extent exts[2] = {
        { .ee_block = 0,   .ee_len = 100, .ee_start_lo = 0x1000 },
        { .ee_block = 120, .ee_len = 40,  .ee_start_lo = 0x5000 },
    };
    printf("lblock 10  -> phys %llu\n",
           (unsigned long long)extent_lookup(exts, 2, 10));   // 0x100A
    printf("lblock 130 -> phys %llu\n",
           (unsigned long long)extent_lookup(exts, 2, 130));  // 0x500A
    return 0;
}
```

## 16. Industry Usage
- **ext4**: Ubuntu/Debian/Android root, most desktop/server default; Raspberry Pi OS.
- **XFS**: RHEL/CentOS/Fedora default; AWS EBS with XFS recommended for certain workloads; Ceph/Gluster backends; big media/HPC stores.
- **btrfs**: Fedora/openSUSE default (snapshot rollback via snapper), Synology/QNAP NAS, Docker overlay layers (storage drivers on btrfs), ZFS-alternative deployments.
- **Android**: F2FS (flash-friendly) on userdata; ext4 still common.

## 17. References
- Kernel docs: `Documentation/filesystems/ext4/`, `xfs.rst`, `btrfs.rst`.
- Silberschatz, *Operating System Concepts*, Ch. 11.7 (examples), Ch. 12 (Linux filesystems).
- Tanenbaum, *Modern Operating Systems*, Ch. 4 (file systems).
- `man mkfs.ext4`, `man mkfs.xfs`, `man mkfs.btrfs`, `man mount`.
- Love, *Linux Kernel Development*, Ch. "The Virtual Filesystem" + ext3/4 overview.
- btrfs wiki (`btrfs.wiki.kernel.org`) for design docs.

## 18. Cheat Sheet
- ext4: block groups, 256B inodes, extents (12B each), JBD2 journal (ordered default), delalloc.
- Extent = [start, len]; 50 contiguous blocks = 1 extent.
- XFS: AGs + B-trees (bno/cnt/inode/extent), extent-only, dynamic inodes, huge volumes.
- btrfs: COW B-trees, subvolumes, snapshots (O(1)), checksums, RAID+scrub, compression.
- delalloc: write → dirty page → allocate at flush.
- fsck: ext4 per-group; xfs_repair per-AG; btrfs scrub online.
- All behind VFS `fops/iops/sops` (Section 04).

## 19. Quiz
1. ext4's big change vs ext3? a) journaling b) extents + delalloc c) checksums d) RAID → **b**
2. An extent stores? a) one pointer b) [start,len] run c) inode number d) checksum → **b**
3. ext4 default journal mode? a) writeback b) journal c) ordered d) none → **c**
4. XFS is structured around? a) block groups b) allocation groups c) subvolumes d) pages → **b**
5. btrfs snapshots work because of? a) journaling b) copy-on-write c) extents d) RAID → **b**
6. Which detects silent bit-rot? a) ext4 b) XFS c) btrfs checksums d) delalloc → **c**

## 20. Flashcards
- **Q: ext4 vs ext3?** → **A:** Extents + delalloc + multiblock + larger.
- **Q: What's an extent?** → **A:** [start block, length] run mapping.
- **Q: ext4 journal modes?** → **A:** ordered / journal / writeback.
- **Q: XFS core?** → **A:** AGs + B-trees; extent-only; huge scale.
- **Q: btrfs CoW?** → **A:** Writes to new blocks → snapshots, crash-safety.
- **Q: Why checksums?** → **A:** Detect bit-rot; repair via scrub/RAID.

## 21. Revision
Linux ships three structurally different filesystems. ext4 (default on Debian/Ubuntu/Android): block groups with inode tables and bitmaps, inodes with extent trees replacing pointer chains, JBD2 journaling (ordered default), and delayed allocation for contiguous layout — fast and battle-tested but no checksums and modest size limits. XFS (default on RHEL/Fedora): allocation groups each with independent B-trees (free space, inodes, extents), extent-only layout, dynamic inodes — built for huge files and parallel I/O. btrfs (Fedora/openSUSE, NAS): copy-on-write B-trees with subvolumes, cheap snapshots, per-block checksums with scrub repair, built-in RAID and compression — the modern "crash-safe + verifiable" design. The interview signals: extents explain ext4's performance, AGs explain XFS's scale, and CoW+checksums explain btrfs's safety — and all three plug into the VFS of Section 04.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "ext4 vs ext3?" | 13 Q1 / 2 How |
| "What is an extent?" | 13 Q2 / 7 Formal |
| "ext4 journaling modes?" | 13 Q3 / 2 How |
| "XFS vs ext4?" | 13 Q4 / 3 When |
| "What is copy-on-write?" | 13 Q5 / 2 How |
| "btrfs subvolumes/snapshots?" | 13 Q6 / 8 Example |
| "Why checksums?" | 13 Q7 / 12 Disadvantages |
| "What is delayed allocation?" | 13 Q8 / 9 Internal |
