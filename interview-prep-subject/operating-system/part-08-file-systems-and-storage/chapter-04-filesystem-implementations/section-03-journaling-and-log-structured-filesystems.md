# Journaling and Log-Structured Filesystems

> **TL;DR**: Crashes mid-write can corrupt metadata. **Journaling** (ext3/4 JBD2, NTFS $LogFile, XFS log) solves it with a write-ahead log: record the change, apply it, then commit — replay/undo at mount. **Log-structured filesystems** (LFS) make the whole disk a log (append-only, out-of-place), and **copy-on-write** filesystems (btrfs/ZFS) get crash safety from never overwriting — three answers to the same problem.

## 1. Why Does This Exist?
A filesystem has many interdependent structures: inode (file metadata) + directory (name→inode) + bitmap (free space). If the machine loses power between "allocate a block," "write the inode," and "update the directory," the on-disk state can be *inconsistent* — an inode pointing at a block the bitmap says is free, or a directory entry pointing at a deleted inode. A crash is not a clean transaction boundary; it can happen after any sub-step. Journaling, log-structured design, and copy-on-write each guarantee that after any crash the filesystem is either the old state or the new state — never a torn hybrid — so that recovery is fast and loss is bounded. Without them, you'd need a full `fsck` (scan the whole disk) to find and fix inconsistencies.

## 2. How Does It Work?
**Journaling (WAL — write-ahead log)**:
1. Start transaction: log the *intent* — write a descriptor + the metadata blocks to the journal.
2. **Commit**: force the journal to disk (commit record). *Now* the change is durable.
3. **Checkpoint/applying**: copy the metadata to their real locations (inode, bitmap, directory).
4. On crash: mount reads the journal — transactions with commit records are **redone** (applied), incomplete ones are **undone** (discarded). Fast, bounded recovery.
- **Data vs metadata**: journal only metadata by default (ext4 `data=ordered`: data first, then metadata commit — so data is on disk before the commit). Full data journaling (`data=journal`) journals data too — slower, max safety.
- **Circular log**: journal is a ring buffer, reused after checkpointing.

**Log-structured filesystem (LFS)**:
- Treat the disk as a **circular log**: all writes (data + metadata) are appended sequentially to the log head. No in-place update ever.
- The inode map (a small, cached table) translates file→inode location in the log.
- Old versions of blocks become garbage; **cleaner** (garbage collector) compacts the log periodically.
- Reads are as fast as any (with caching), writes are sequential → great for flash; random-write HDD workloads benefit (log writes are sequential).
- Recovery: replay from the last checkpoint.

**Copy-on-write (CoW)**:
- Never overwrite live blocks — write new blocks, update parent pointers (inode→extent tree→data), atomically flip the *root* pointer to the new tree.
- Crash can only leave the old tree or the new tree intact — because old blocks are never touched. Recovery = mount the last committed root.
- btrfs/ZFS: transaction groups (ZFS txg), `fsync` commits the root.

## 3. When Is It Used?
- **Journaling**: ext3/ext4 (JBD2), XFS log, NTFS `$LogFile`, FAT's replacement on modern systems, Apple APFS journaling (CoW + journaling combined).
- **Log-structured**: original LFS (Rosenblum & Ousterhout, 1991); flash SSDs *internally* (FTL is log-structured); LogFS (Linux); modern descendants influence journaling FS design (flash-friendly allocation).
- **CoW**: ZFS, btrfs, APFS (mixed), WAFL (NetApp), filesystem snapshots.
- **Trade**: journaling for mature simplicity; CoW for snapshots + checksums; LFS for pure sequential-write workloads.

## 4. Why Wasn't Another Approach Chosen?
- **Sync writes everywhere (rejected)**: force every metadata write to disk immediately — correct but 10–100× slower (each write = a physical seek + flush).
- **Full fsck after crash (rejected)**: works but scans the entire volume — minutes to hours on big disks.
- **Hardware battery-backed write cache (a band-aid)**: controllers with BBU hide ordering, but that's hardware, not filesystem.
- **Journaling (chosen for ext3/4, NTFS)**: cheap (small log), bounded recovery, well understood.
- **CoW (chosen for btrfs/ZFS)**: crash safety *for free* + snapshots + checksums; cost: every update writes more blocks (amplification), fragmentation.
- **LFS (mostly not chosen as user FS)**: cleaner complexity, read performance, and mixed workloads hurt; but its *idea* lives in SSDs' FTLs and in CoW designs.

## 5. Intuition
**A chef's prep list (journaling)**: before touching the dish, the chef writes the change on a sticky note (journal), sets it on the counter (commit), then makes the change. If power goes out mid-step, the sous-chef reads the notes: completed notes = redo, torn notes = start over — everything is consistent and recovery is fast.

**A banker's ledger append (LFS)**: every transaction is appended to the end of the ledger — never edit an old page. Old entries that are superseded are garbage; an accountant (cleaner) periodically rewrites the ledger, dropping dead entries.

**A version-controlled repo (CoW)**: every edit creates a new version of the file; the repo just points its HEAD to the new version. A crash leaves HEAD pointing at the last committed version — you never get a half-edited file because edits never touch existing versions.

## 6. Real-World Analogy
- **Journaling**: a recipe card system where you write the intended change on a card, place it on the "to do" pile, then update the actual card; on restart you replay the to-do pile.
- **LFS**: a ship's logbook that only grows — you never rewrite history; when the book fills, a fresh volume starts and the old one is archived (but a "cleaner" rewrites compact volumes).
- **CoW**: photo editing where "save" always creates a new layer rather than painting over the original — the file is always an atomic swap of layers; you can roll back to any previous save (snapshot).

## 7. Formal Definition
**Journaling (write-ahead log)**: A circular log where a metadata update is recorded as a transaction `{descriptor, blocks, commit}`. A transaction is *durable* once its commit record is flushed; recovery replays (redo) committed transactions and rolls back incomplete ones (undo via prior state). Ext4 JBD2 modes: `ordered` (data flushed before metadata commit), `journal` (data in journal), `writeback` (no ordering). Cost: one small sequential log write per transaction — much cheaper than sync-writing scattered metadata.
**LFS**: The disk is an append-only log; each write appends data + an inode block; an **inode map** (partial on disk, cached in RAM) maps file → current inode block; garbage is reclaimed by a **cleaner** that reads fragmented log regions, extracts live blocks, and appends them compactly; checkpoints delimit recoverable state.
**CoW**: All updates allocate fresh blocks and rewire parent pointers; the filesystem root (or tree root) is updated **atomically** (single sector) at commit; a crash before commit leaves the previous root → previous consistent state; snapshots = previously committed roots retained.

## 8. Example
Crash scenario — creating file `f`, writing 4 KB, deleting:
- **ext4 (ordered)**: (1) data blocks written to their final place; (2) JBD2 transaction logs inode update + bitmap update + directory entry; (3) commit record; (4) apply metadata. Crash before (2): old state (no file) — clean. Crash between (2) and (4): replay applies metadata → file exists with correct data. Crash during apply: redo completes the apply.
- **NTFS**: `$LogFile` record for the same; undo of an incomplete `$LogFile` transaction at mount.
- **LFS**: write appends data segment + inode update; inode map updated; crash before checkpoint → replay from last checkpoint (lost tail of writes, no corruption).
- **btrfs**: write allocates new blocks for data + new inode tree nodes + new root; single atomic root-pointer swap commits; crash before swap → old root (file absent); after swap → file present; snapshot = keep the old root.

## 9. Internal Working
1. **ext4**: `ext4_journal_start` → reserve journal space → modify buffer_heads (metadata) → `jbd2_journal_stop` → `jbd2_journal_commit_transaction` (log descriptor + blocks, barrier/commit). On mount: `jbd2_journal_recover` replays.
2. **NTFS**: `$LogFile` — transactions with `LogClient` (redo) + `LogClientUndo` records; `ntfsck`/mount replays.
3. **LFS (theoretical)**: write segment = batch of sequential appends; segment summary + inode blocks; cleaner triggers at threshold; checkpoints (a superblock region) written periodically.
4. **btrfs**: transaction: COW the affected tree paths → write new root node → `btrfs_commit_transaction` (writes superblock with new root pointer) → done. `fsync` flushes the current transaction.
5. **ZFS**: transaction groups (`txg`) — all writes accumulate, committed together; `zfs sync` forces; CoW + checksums + RAID built in.

## 10. Time Complexity
- Journal commit: O(log size) or O(1) amortized — a few sector writes, batched across the transaction.
- Checkpointing (ext4): O(metadata changed); can lag behind.
- Recovery replay: O(journal length) — milliseconds, vs O(volume) full fsck.
- LFS write: O(1) append (sequential); cleaner: O(log region size) — but total write amplification grows with fragmentation.
- CoW commit: O(tree height) pointer updates + O(changed blocks) — the commit itself is O(1) (root swap).
- Write amplification: journal ≈ small constant; LFS grows with old-age garbage; CoW ≈ 2× for single block updates (data + tree path).

## 11. Advantages
- **Journaling**: mature, fast recovery, minimal write overhead (metadata only by default); works on existing designs (ext2→ext3 upgrade).
- **LFS**: perfect sequential write patterns (SSD-friendly), crash-safe (append only), no in-place corruption; historical importance (FTL/SSD design).
- **CoW**: crash safety *without* a journal (no replay), free snapshots, checksums can be verified (btrfs/ZFS), no torn writes by construction.
- **All**: bounded, fast recovery vs full fsck; bounded data loss window (committed-but-unsynced data).

## 12. Disadvantages
- **Journaling**: doesn't protect *data* by default (ordered protects pointers, not file bytes); journal is extra write overhead; replay needed at mount; journal itself can corrupt (rare, or no journaling of the journal).
- **LFS**: cleaner complexity + cost (write amplification), read performance with poor locality, mixed random workloads poor, implementation difficulty — why it never became a mainstream user FS.
- **CoW**: write amplification (every update rewrites tree path), fragmentation, needs background defrag (btrfs balance), higher memory for tree metadata; snapshots retain old data → surprise space usage.
- **All**: guarantee is metadata consistency, not "no data loss" — a power cut after successful `write()` but before `fsync()` can lose data by design (POSIX).

## 13. Interview Questions
1. **Q: Why do filesystems need journaling?** A: Crash mid-multi-structure-update (inode+bitmap+dir) can leave inconsistent state; journaling logs the change *before* applying (WAL) so recovery is fast and the FS is always old-or-new consistent.
2. **Q: What is the write-ahead log?** A: Record the intended change durably (commit) *before* modifying real structures; on recovery redo committed / undo partial transactions — the same idea as database WAL.
3. **Q: ext4 data=ordered vs data=journal?** A: `ordered`: data written first, metadata committed after → pointers never point to unwritten data, no double write; `journal`: data itself journaled → max safety, ~2× write cost.
4. **Q: What's the difference between journaling and a log-structured FS?** A: Journal = a *small* WAL + in-place metadata application; LFS = the *whole disk* is the log, all writes append, cleaner reclaims garbage — different mechanisms, same "no torn state" goal.
5. **Q: How does CoW achieve crash safety?** A: Never overwrite live blocks — write new blocks + new tree path, atomically flip the root pointer; crash leaves old or new root, never a mix (btrfs/ZFS model).
6. **Q: What is a checkpoint?** A: In journaling, applying logged metadata to real locations (and freeing log space); in LFS, the point from which recovery replays; in ZFS, the committed txg.
7. **Q: Why was full fsck not enough?** A: It works but scans the entire volume — slow (hours on big disks); journaling bounds recovery to the log length (milliseconds) and keeps the FS always mountable-consistent.
8. **Q: What does LFS mean for flash?** A: Append-only writes match NAND's erase-before-write; SSDs' FTLs *are* internal log-structured translators (Section 08-03-03) — LFS ideas live on inside flash.
9. **Q: Journal vs snapshot?** A: Journal = crash consistency mechanism (redo/undo log); snapshot = point-in-time image (CoW keeps old roots). ext4 has no snapshots; btrfs/ZFS have both (CoW + transaction log for fsync).
10. **Q: What is the fsync guarantee?** A: `fsync`/`fdatasync` flushes data + metadata (and forces journal commit) so after crash the file's contents are durable — but a plain `write()` returning before `fsync` is *not* durable (POSIX).
11. **Q: What is write amplification in CoW?** A: Each block update also rewrites tree nodes (inode, extent, checksum) — a 4 KB write can touch several 4 KB tree blocks; btrfs/ZFS accept this for snapshots + checksums.
12. **Q: What is the "cleaner" in LFS?** A: Garbage collector: reads log segments, copies live blocks to a new compact segment, erases the old → reclaims space and keeps writes sequential.

## 14. Follow-Up Questions
1. **Q: What is a barrier in ext4?** A: `barrier=1` forces disk cache flush ordering so the commit record isn't reordered ahead of the journal data (needed on write-back disk caches; dangerous if disabled).
2. **Q: What is APFS's approach?** A: CoW + journaling + snapshots (Apple) — hybrid: CoW tree with a journal for crash consistency of some structures.
3. **Q: What is the write hole in RAID + journaling?** A: Parity updates can be torn across a crash; ZFS/CoW avoids it because parity is also CoW'd — a nice tie to Section 08-03-02.
4. **Q: What is LogFS / F2FS?** A: Flash-adapted LFS descendants: F2FS (Android) uses append-only logs + checkpoint, designed for NAND.

## 15. Coding Example
```c
// Sketch of a write-ahead journal (crash-consistent append of a tx)
#include <stdio.h>
#include <stdint.h>
#include <string.h>

typedef struct { uint32_t seq; uint8_t op; uint32_t block; uint8_t data[16]; } tx_t;

// append a transaction to the log, force it, then apply to "disk"
void journal_and_apply(FILE *journal, uint32_t *disk, tx_t *tx, int count) {
    // 1. WRITE-AHEAD: log the transaction durably
    fwrite(tx, sizeof(tx_t), count, journal);
    fflush(journal);                    // commit (force to disk)
    // 2. apply to the real metadata structures
    for (int i = 0; i < count; i++) {
        memcpy((char*)disk + tx[i].block * 16, tx[i].data, 16);
    }
    // 3. free log space (checkpoint) — omitted for brevity
}

// on recovery: replay committed tx, ignore torn tail (seq gaps)
void recover(FILE *journal, uint32_t *disk) {
    tx_t t; uint32_t last = 0;
    while (fread(&t, sizeof(tx_t), 1, journal) == 1) {
        if (t.seq == last + 1) {        // contiguous, committed
            memcpy((char*)disk + t.block * 16, t.data, 16);
            last = t.seq;
        } else break;                   // torn write → stop
    }
    printf("recovered through seq %u\n", last);
}

int main(void) {
    uint32_t disk[4] = {0};
    FILE *j = tmpfile();
    tx_t tx[1] = {{.seq = 1, .op = 1, .block = 0, .data = {1,2,3}}};
    journal_and_apply(j, disk, tx, 1);
    rewind(j);
    recover(j, disk);
    fclose(j);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: ext4/JBD2 (default), XFS log, `reiserfs` (historic); `Documentation/filesystems/`.
- **Windows**: NTFS `$LogFile`; reFS (CoW + checksums).
- **Apple**: APFS (CoW + journaling + snapshots).
- **NAS/enterprise**: ZFS (CoW + txg), btrfs, NetApp WAFL (CoW + NVRAM log), Ceph (metadata journal in BlueStore/WAL).
- **Databases** (the same idea): PostgreSQL WAL, MySQL InnoDB redo log — "write-ahead logging" is a universal crash-consistency technique.

## 17. References
- Rosenblum & Ousterhout (1991), "The Design and Implementation of a Log-Structured File System" (LFS paper).
- Silberschatz, *Operating System Concepts*, Ch. 11.6 "Log-Structured File Systems", Ch. 12.5 (journaling).
- Tanenbaum, *Modern Operating Systems*, Ch. 4.3 "File system implementation" (journaling/log-structured).
- Linux `fs/jbd2/` (journaling), `Documentation/filesystems/`.
- ZFS `txg.c` (transaction groups), btrfs `transaction.c`.

## 18. Cheat Sheet
- Problem: crash mid-update = torn metadata (inode+bitmap+dir).
- Journal (WAL): log → commit → apply; replay at mount; fast.
- ext4 modes: ordered (default) / journal / writeback.
- LFS: whole disk is a log; append-only; cleaner reclaims; inode map.
- CoW: never overwrite; flip root atomically; crash-safe; snapshots.
- ZFS txg / btrfs transaction: batch + commit root.
- fsync = durable; plain write() is not.
- Write amplification: CoW/LFS > journal.
- Same idea in DBs: PostgreSQL WAL, InnoDB redo.

## 19. Quiz
1. Journaling's core idea? a) checksums b) WAL c) mirroring d) caching → **b**
2. ext4 default data mode? a) journal b) writeback c) ordered d) none → **c**
3. Recovery with a journal is? a) O(volume) b) O(log length) c) O(1) d) O(files) → **b**
4. LFS writes are? a) in-place b) append-only c) mirrored d) compressed → **b**
5. CoW commits by? a) log replay b) root pointer swap c) fsck d) bitmap → **b**
6. fsync guarantees? a) write() returned b) data durable c) cache warm d) snapshot → **b**

## 20. Flashcards
- **Q: Why journal?** → **A:** Crash consistency; log-then-apply; fast replay.
- **Q: data=ordered?** → **A:** Data first, metadata commit after — pointers safe.
- **Q: LFS?** → **A:** Whole disk is an append-only log; cleaner compacts.
- **Q: CoW crash safety?** → **A:** Flip root atomically; never overwrite.
- **Q: Checkpoint?** → **A:** Apply log / recover-from point / committed txg.
- **Q: fsync?** → **A:** Makes write durable; plain write() isn't.

## 21. Revision
All three approaches solve the same crash-consistency problem — a power loss can tear a multi-structure metadata update. **Journaling** (ext4 JBD2, NTFS $LogFile, XFS) uses a small write-ahead log: log the change, commit, then apply; recovery replays committed and discards torn transactions in milliseconds. **Log-structured** (LFS) makes the disk itself an append-only log — no in-place writes, a cleaner reclaims garbage — ideal for flash (and literally what SSD FTLs do internally). **Copy-on-write** (btrfs/ZFS/APFS) never overwrites live blocks, atomically flipping the root pointer at commit, giving crash safety *and* free snapshots and checksums — at the cost of write amplification. The universal takeaway (also true for databases): order writes so that a commit marker is the single durable point of consistency, and recovery is O(log) not O(volume).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why do filesystems need journaling?" | 1 Why / 13 Q1 |
| "What is WAL?" | 13 Q2 / 2 How |
| "data=ordered vs data=journal?" | 13 Q3 / 8 Example |
| "Journal vs LFS?" | 13 Q4 / 2 How |
| "How does CoW give crash safety?" | 13 Q5 / 7 Formal |
| "Why was fsck not enough?" | 13 Q7 / 4 Why not |
| "What is write amplification?" | 13 Q11 / 12 Disadvantages |
| "What is the cleaner?" | 13 Q12 / 2 How |
