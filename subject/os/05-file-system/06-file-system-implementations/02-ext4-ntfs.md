# File Systems — ext4 & NTFS

## ext4 (Fourth Extended Filesystem)
- **Default Linux FS**; successor of ext3 (which added journaling to ext2)
- **Journaling**: metadata journaling by default; full data journaling optional

### ext4 Key Features
| Feature | Description |
|---------|-------------|
| **Extents** | Replaces block pointers; stores `(start, length)` pairs — less metadata |
| **Delayed allocation** | Allocate on flush, not on write — better contiguous placement |
| **Multi-block allocator** (mballoc) | Allocates multiple blocks in one pass |
| **HTree** | B-tree based directory indexing — O(log n) lookups |
| **Flexible block groups** | Meta-block groups for reduced fragmentation |
| **Fast fsck** | Uninit bitmaps → quick check skips unused inode groups |
| **Volume limit** | 1 EiB (with 4KB blocks) |
| **File size limit** | 16 TiB |
| **Sub-second timestamps** | Nanosecond timestamps |

### ext4 Inode Layout (256 bytes)
- 12 direct extents + extent tree if > 4 extents

## NTFS (New Technology File System)
- **Default Windows FS**; replaced FAT32 from Windows NT 3.1

### NTFS Key Features
| Feature | Description |
|---------|-------------|
| **$MFT** (Master File Table) | Each file = one (or more) MFT records (~1KB each); MFT itself is a file |
| **B+ tree directories** | Balanced tree for fast directory lookups |
| **Journaling** | $LogFile tracks metadata changes for crash recovery |
| **Alternate Data Streams** (ADS) | Multiple data streams per file; `file:stream` syntax |
| **ACLs** | Fine-grained permissions (not just rwx) |
| **Encryption** (EFS) | Per-file encryption with public key cryptography |
| **Compression** | LZ77 per-file compression |
| **Quotas** | Per-user disk space limits |
| **Sparse files** | Efficient storage of files with large zero ranges |
| **Volume limit** | 256 TB (with 64KB clusters) |
| **File size limit** | 16 EB |
| **Hard links** | Yes (POSIX-style) |
| **Junction points** | Directory symbolic links (cross-volume) |

## Comparison Table

| Feature | **ext4** | **NTFS** | **APFS** (macOS) | **ZFS** |
|---------|----------|----------|------------------|---------|
| Journaling | ✅ Metadata | ✅ Metadata | ✅ Metadata | ✅ (Copy-on-write) |
| Max volume | 1 EiB | 256 TB | 8 EB | 256 ZiB |
| Max file | 16 TiB | 16 EB | 8 EB | 16 EB |
| Snapshots | ❌ | ❌ (VSS at volume level) | ✅ | ✅ |
| Checksumming | ❌ (ext4: metadata only) | ❌ | ✅ | ✅ (all data) |
| Compression | ❌ | ✅ | ✅ | ✅ |
| Encryption | ✅ (ext4 encrypt) | ✅ (EFS/BitLocker) | ✅ (native) | ✅ |
| Deduplication | ❌ | ❌ | ❌ | ✅ |
| COW | ❌ | ❌ | ✅ | ✅ |
| Pooling | ❌ | ❌ | ✅ (Fusion) | ✅ |

## Key Interview Questions
- ext4 vs NTFS: which is better? → Depends: ext4 for Linux/embedded, NTFS for Windows compatibility
- What is **$MFT** in NTFS? → Master File Table — a relational database of all files and directories; NTFS's most important structure
- What is **copy-on-write**? → Never overwrite data in place; write to new block, update metadata atomically (APFS, ZFS, Btrfs)
- How does **delayed allocation** help? → OS buffers writes, then allocates the best contiguous space before flushing to disk
- Can Windows read ext4? → Not natively; third-party tools (Ext2Fsd, WSL2) needed
- What are **Alternate Data Streams**? → Hidden data attached to a file (e.g., `file.exe:Zone.Identifier` marks download origin)
