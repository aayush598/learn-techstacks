# Windows NTFS

> **TL;DR**: NTFS is Windows' journaling filesystem built around the **Master File Table (MFT)** — a file that stores every file, directory, and stream as a record with **attributes**. Everything (data, ACLs, timestamps, even small files' contents) lives in attribute streams; journaling, compression, sparse files, and quotas are native.

## 1. Why Does This Exist?
FAT32 couldn't scale (4 GB max file, no permissions, no journaling, no recovery) — NTFS (introduced with Windows NT 3.1, 1993) replaced it with a journaling, metadata-rich, secure filesystem: variable-size attributes, ACLs, compression, encryption (EFS), sparse files, quotas, hard links, and 16 EB limits. It had to serve Windows' enterprise ambitions (multiuser, secure, crash-tolerant) from the start. It remains the Windows system/primary filesystem (reFS is the newer sibling for storage spaces).

## 2. How Does It Work?
- **MFT (Master File Table)**: a special file (`$MFT`) containing fixed-size (usually 1 KB) **file records**, one per file/directory. Each record holds **attributes** (an attribute stream list):
  - `$STANDARD_INFORMATION` (timestamps, flags), `$FILE_NAME` (name + parent ref), `$SECURITY_DESCRIPTOR` (ACL), `$DATA` (file content — *resident* if small, else runs/extents), `$INDEX_ROOT`/`$INDEX_ALLOCATION` (directory B-tree), `$BITMAP`, `$ATTRIBUTE_LIST` (overflow), `$OBJECT_ID`, `$EA`/`$EA_INFORMATION`.
- **Resident vs non-resident**: small attributes (including small files' data, a few hundred bytes) live *inside* the MFT record → no separate allocation. Large data = non-resident runs (extents) pointed by `$DATA` mapping pairs (VCN→LCN runs).
- **Directories**: B-trees of file name records (`$FILE_NAME` entries with name + file reference) → fast lookups, sorted.
- **Journaling**: `$LogFile` ($NTFS log) — a WAL of metadata transactions (NTFS uses write-ahead logging with redo/undo records). It keeps **file system** metadata consistent after crash (data may need NTFS scan for consistency in some cases; the log is often "the safety net").
- **Streams (ADS)**: every file is a set of named streams; `$DATA` unnamed is the default. `Zone.Identifier` (mark-of-the-web), `:stream` data.
- **Compression**: LZNT1 for files/sparse; attribute-level, on $DATA.
- **Sparse files**: `$DATA` with allocated/unallocated runs; hole reads return zeros.
- **Quotas, hard links, junctions, EFS** (per-file encryption), **USN journal** (change tracking for search/backup), **$UpCase**, **$BadClus** (bad cluster map), **$Bitmap** (allocation bitmap), **$Volume** info.

## 3. When Is It Used?
- Windows system drive (`C:`), all modern Windows since NT.
- **reFS** for Storage Spaces / Hyper-V VHDs (larger, checksummed, but not a general C: filesystem).
- macOS/Linux read NTFS via `ntfs-3g` (FUSE) / kernel `ntfs3` driver (Paragon) — Linux gained native NTFS read/write via `ntfs3` in kernel 5.15.
- exFAT for removable media (FAT-family, no MFT; NTFS is journaling+ACLs, exFAT is simple flash-friendly).

## 4. Why Wasn't Another Approach Chosen?
- **FAT32**: no journal, 4 GB files, no ACLs, no recovery — rejected for the OS drive long ago.
- **HPFS (OS/2)**: B-tree directories but no journaling or ACL model NT needed.
- **A Unix ext-style design**: Windows wanted a *single central table* (MFT) with extensible attributes rather than fixed inodes — more flexible (streams, ADS) at the cost of MFT fragmentation.
- **Journaling via external LVM (Linux)**: NTFS baked the WAL in from day one (`$LogFile`).
- **reFS (not chosen as default)**: checksummed, resiliant (mirror/parity) but intentionally lacks features needed for C: (boot, ADS broadly, EFS) — NTFS remains the system FS.

## 5. Intuition
**A master filing cabinet with index cards**: The MFT is a giant set of index cards (records), one per file, and each card has labeled pockets (attributes): name, timestamps, permissions, and a slot for the file's *contents itself* if small (resident data). Directories are not separate structures — they're just more cards whose contents point at other cards (B-tree name lists). If a file's data is too big for its card, the card points to a chain of storage runs elsewhere. The `$LogFile` is the pencil-erasure journal: before changing any card, the change is written to a log so a power loss can't leave a half-erased card.

## 6. Real-World Analogy
**A legal docket system**: each file is a case folder (MFT record) with labeled tabs (attributes): "filed date" (timestamps), "parties" (ACL/security), "documents" (data stream). Small case folders hold the documents in the folder itself (resident); huge ones reference external storage boxes (runs). The docket index (directory B-tree) is alphabetical cross-references. The court's **docket journal** (journal) is where every change is recorded *before* it's made, so if power dies mid-update the court can reconstruct exactly what was and wasn't done.

## 7. Formal Definition
NTFS organizes the volume around the **$MFT**, an array of 1 KB (default) file records. A record = a sequence of attributes, each `[type, name, size, value|mapping]`; `$DATA` non-resident attributes are stored as **mapping pairs** (run lists) `(VCN offset, length → LCN)` — an extent scheme. Directories are B-trees whose leaves are `$FILE_NAME` index entries (name + file reference + timestamps). The **$LogFile** is a circular write-ahead journal of transactions with redo/undo; **$Bitmap** tracks free clusters; **$BadClus** marks bad sectors; **$Quota** enforces quotas; every data/metadata block has a logical cluster number (LCN) mapping via VCN. ACLs live in `$SECURITY_DESCRIPTOR` and are deduplicated in `$Secure`. NTFS metadata is stored as hidden system files (`$MFT`, `$MFTMirr`, `$LogFile`, ...) at the volume start.

## 8. Example
A 100-byte text file "hello.txt":
- MFT record for `hello.txt` (record #42): `$STANDARD_INFORMATION` (created/modified/accessed, DOS time), `$FILE_NAME` (parent ref → directory record, name "hello.txt"), `$SECURITY_DESCRIPTOR` (ACL: User: Full control), `$DATA` = the 100 bytes **resident** (fits in the record, no extra allocation — this is why NTFS tiny files are efficient).
- A 10 MB binary: `$DATA` non-resident → mapping pairs: `run1 (VCN0, len 0x800 clusters → LCN 0x12345)`, `run2 (...)`. Reads resolve VCN→LCN via the run list.
- Directory `\home\user`: its MFT record's `$INDEX_ROOT` (small dir) or `$INDEX_ALLOCATION` (B-tree runs) lists `hello.txt` entries; lookups binary-search the B-tree.
- After a crash: mount replays `$LogFile` — any transaction not committed is undone; committed-but-not-applied is redone → metadata consistent.

## 9. Internal Working
1. VFS/NTFS driver (kernel `ntfs3` or FUSE `ntfs-3g`) translates path → walk directories via B-tree index → find file reference (MFT record #).
2. Read: parse record attributes → `$DATA` resident (copy) or run list → map VCN→LCN → read clusters.
3. Write: allocate clusters (update `$Bitmap`), extend `$DATA` run list, update record; all metadata changes go through `$LogFile` transaction (WAL): log redo/undo → apply → commit.
4. Flush/`FlushFileBuffers`/`fsync`: force log + metadata + data to disk.
5. Recovery after crash: `ntfsck`-style log replay; `$BadClus` updated if bad sectors found.
6. Compression: compress $DATA (LZNT1) per block; decompress on read, transparently.

## 10. Time Complexity
- File lookup: O(log n) directory B-tree (n = entries).
- Read/write: O(r) for run list traversal (r = number of extents) + O(blocks) transfer; resident reads O(1) (in-record copy).
- MFT record access: O(1) (record index → file record offset).
- Log commit: O(1) batch (WAL commit record), amortized.
- Compression: O(size) compress/decompress (LZNT1), with caching.
- Allocation: `$Bitmap` O(1) per cluster run via bitmap scan.

## 11. Advantages
- **MFT-centric**: everything is attributes/streams — flexible (ADS), metadata-rich, extensible.
- **Resident data**: tiny files cost almost nothing (no allocation).
- **Journaling** (`$LogFile`): fast, consistent crash recovery.
- **B-tree directories**: scale to millions of entries.
- **Native**: ACLs, compression, sparse files, EFS, quotas, USN journal, hard links, junctions.
- **Robustness**: `$BadClus` maps bad sectors; `chkdsk` can repair; `$MFTMirr` mirrors critical MFT records.

## 12. Disadvantages
- **MFT fragmentation**: heavily-fragmented MFT degrades performance (Defrag needed); MFT growth is dynamic.
- **No per-block checksums** (unlike btrfs/ZFS): silent bit-rot undetected (NTFS relies on hardware ECC).
- **Journal only guarantees metadata consistency**; data in cache can be lost on sudden power loss (mitigated by `FlushFileBuffers`, `writeback`).
- **Complexity**: ADS/streams confuse users (Zone.Identifier), hard to implement (that's why ntfs-3g took years).
- **Windows-only** (though ntfs3 driver brings read/write to Linux); exFAT needed for flash.
- **Overhead**: MFT records + attributes per file vs simpler designs; high overhead on small volumes.

## 13. Interview Questions
1. **Q: What is the MFT?** A: The Master File Table — a special file of 1 KB records, one per file/directory; each record is a set of attributes (metadata, ACL, data). Everything in NTFS is a record in the MFT.
2. **Q: What is a resident attribute?** A: An attribute stored *inside* the MFT record (fits in 1 KB) — small files' data is resident → no separate allocation, very fast tiny-file access.
3. **Q: What are ADS (alternate data streams)?** A: Named streams on a file, e.g., `Zone.Identifier` (mark-of-the-web); NTFS stores each stream as a separate `$DATA` attribute — data + metadata both extendable.
4. **Q: How does NTFS do crash recovery?** A. `$LogFile`: a write-ahead journal (redo/undo) — metadata changes are logged before application, replayed/rolled back at mount → consistent metadata after power loss.
5. **Q: NTFS directories?** A: B-tree index records (`$INDEX_ROOT` inline, `$INDEX_ALLOCATION` on-disk runs) of `$FILE_NAME` entries — logarithmic lookups, sorted, scale to millions.
6. **Q: How are large files stored?** A: Non-resident `$DATA` as mapping pairs (run list): `(VCN → LCN, length)` — NTFS's extent scheme; reads resolve via the run list.
7. **Q: NTFS vs FAT32?** A: FAT32: 4 GB max file, no ACLs, no journal, no recovery, no sparse/compression; NTFS: 16 EB, ACLs, journaling, compression, EFS, quotas — the modern Windows FS.
8. **Q: What's the role of `$Bitmap`?** A: The allocation bitmap — free/used cluster tracking, used at allocation time; analogous to ext4's block bitmap.
9. **Q: What is a sparse file?** A: A file with holes — unallocated runs in `$DATA` read as zeros; used for huge logical sizes (VM images, `sparsebundle`).
10. **Q: Does NTFS have checksums?** A: Not for data blocks (unlike btrfs/ZFS) — only some metadata has fixups; silent bit-rot is detected via hardware ECC + chkdsk, not on-read verification.
11. **Q: How does Linux access NTFS?** A: Kernel `ntfs3` driver (Paragon, since 5.15) for read/write, or FUSE `ntfs-3g`; NTFS was reverse-engineered (spec now documented) — notoriously complex.
12. **Q: What is the USN journal?** A: The Update Sequence Number journal — a change-log of file modifications (used by search indexing, backup, antivirus); distinct from `$LogFile`.

## 14. Follow-Up Questions
1. **Q: What is reFS?** A: Resilient File System — checksums + auto-correction, mirror/parity via Storage Spaces, 1 PB+ volumes; not a boot/system FS (no ADS broad support) — NTFS stays for C:.
2. **Q: What is `chkdsk`?** A: Windows's fsck — checks MFT/bitmap consistency, fixes from `$LogFile` + `$BadClus`; `chkdsk /f` on mount if dirty bit set.
3. **Q: What is `$MFTMirr`?** A: A mirrored copy of the first (critical) MFT records — protects against MFT corruption.
4. **Q: NTFS vs exFAT?** A: exFAT is FAT's modern flash-friendly variant (no MFT, no journaling, no ACLs, 16 EB files) for removable media; NTFS is the full-featured system FS.

## 15. Coding Example
```c
// Run-list mapping (simplified NTFS $DATA non-resident): VCN -> LCN
#include <stdint.h>
#include <stdio.h>

typedef struct { int64_t vcn; uint64_t len; int64_t lcn; } run;

// read a cluster: resolve logical VCN via the run list
int64_t vcn_to_lcn(const run *runs, int n, int64_t vcn) {
    int64_t cur = 0;
    for (int i = 0; i < n; i++) {
        if (vcn < cur + (int64_t)runs[i].len)
            return runs[i].lcn + (vcn - cur);   // within this run
        cur += runs[i].len;
    }
    return -1; // hole / unallocated
}

int main(void) {
    // file of 1000 clusters stored in three runs
    run runs[] = {
        { .vcn = 0, .len = 200, .lcn = 0x1000 },
        { .vcn = 200, .len = 500, .lcn = 0x9000 },
        { .vcn = 700, .len = 300, .lcn = 0x3000 },
    };
    printf("VCN 50  -> LCN 0x%llX\n",
           (unsigned long long)vcn_to_lcn(runs, 3, 50));    // 0x1032
    printf("VCN 800 -> LCN 0x%llX\n",
           (unsigned long long)vcn_to_lcn(runs, 3, 800));   // 0x3064
    return 0;
}
```

## 16. Industry Usage
- **Windows**: system drive C:, every modern Windows install; boot, apps, user data.
- **Storage Spaces / Hyper-V**: reFS for VHDX pools, NTFS still the app FS.
- **Cross-platform**: Linux/macOS via `ntfs3` (kernel) and `ntfs-3g` (FUSE); NTFS-formatted external drives.
- **Enterprise**: Windows servers (AD, file shares with ACLs, DFS), databases on NTFS (though SSD-era sees reFS for checksums).

## 17. References
- Microsoft NTFS documentation: "NTFS overview" (learn.microsoft.com); MS-NTFS spec (the on-disk format).
- Silberschatz, *Operating System Concepts*, Ch. 11.8 "Windows file systems" (NTFS overview).
- Tanenbaum, *Modern Operating Systems*, Ch. 4.5 "Example file systems" (Windows).
- `man ntfs-3g`, `ntfsfix`; Linux kernel `fs/ntfs3/`.
- Russinovich, *Windows Internals*, Part 2 (Storage/File Systems chapter).

## 18. Cheat Sheet
- MFT = array of 1 KB records, one per file/dir; everything is attributes.
- Resident attribute = data inside the MFT record (small files).
- Non-resident $DATA = run list (VCN→LCN mapping pairs = extents).
- Directories = B-tree of $FILE_NAME entries.
- $LogFile = write-ahead journal (redo/undo) → crash-consistent metadata.
- ADS = named streams; Zone.Identifier etc.
- Sparse = unallocated runs read as zeros.
- No data checksums (vs btrfs/ZFS); reFS adds them.
- Linux: ntfs3 kernel driver / ntfs-3g FUSE.

## 19. Quiz
1. NTFS's central structure? a) superblock b) MFT c) inode table d) block group → **b**
2. A resident attribute? a) on another disk b) inside MFT record c) encrypted d) sparse → **b**
3. NTFS journal is? a) $Bitmap b) $LogFile c) $MFT d) $UpCase → **b**
4. Directories in NTFS? a) linked list b) B-tree c) hash table d) array → **b**
5. Large file data stored as? a) run list b) resident c) bitmap d) ADS → **a**
6. Silent bit-rot detection? a) yes, checksums b) no data checksums c) always d) via MFT → **b**

## 20. Flashcards
- **Q: MFT?** → **A:** Master File Table: one 1 KB record per file/dir, attributes inside.
- **Q: Resident data?** → **A:** Small files' data inside the MFT record.
- **Q: $LogFile?** → **A:** Write-ahead journal for crash-consistent metadata.
- **Q: NTFS dirs?** → **A:** B-tree of name records.
- **Q: Run list?** → **A:** VCN→LCN extent mapping for non-resident data.
- **Q: reFS vs NTFS?** → **A:** reFS = checksummed resilient; NTFS = the system FS.

## 21. Revision
NTFS organizes the whole volume as a **Master File Table** of 1 KB records, where every file and directory is a set of **attributes** — including resident `$DATA` (tiny files live inside their record) and non-resident run lists (extents) for large files. Directories are B-trees of name entries; `$Bitmap` tracks allocation; `$BadClus` maps bad sectors; ACLs live in `$SECURITY_DESCRIPTOR`. Crash safety comes from `$LogFile`, a write-ahead redo/undo journal replayed at mount. Windows' niche features — ADS streams (`Zone.Identifier`), compression, sparse files, EFS, quotas, USN journal — all emerge from the attribute model. It has no data checksums (reFS adds them), and Linux reads/writes it via `ntfs3`/`ntfs-3g`. Contrast with Section 01's Linux trio: same problems (metadata, allocation, crash safety), different anatomy.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the MFT?" | 13 Q1 / 2 How |
| "What is a resident attribute?" | 13 Q2 / 8 Example |
| "What are ADS streams?" | 13 Q3 / 2 How |
| "How does NTFS recover from crashes?" | 13 Q4 / 9 Internal |
| "How are large files stored?" | 13 Q6 / 8 Example |
| "NTFS vs FAT32?" | 13 Q7 / 4 Why not |
| "Does NTFS have checksums?" | 13 Q10 / 12 Disadvantages |
| "How does Linux read NTFS?" | 13 Q11 / 16 Industry |
