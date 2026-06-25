# File Allocation Methods

## Contiguous Allocation
- File occupies **contiguous disk blocks**
- Directory entry: `[name, start_block, length]`
- **Pros**: excellent sequential + direct access (just `start + N`)
- **Cons**: **external fragmentation**, hard to grow file (need to relocate if no space)
- Used in: **FAT** volumes (root directory), DVD/ISO images

## Linked Allocation
- Each data block contains **pointer to next block** (last = `-1`)
- Directory: `[name, start_block, end_block]`
- **Pros**: no external fragmentation, easy to grow
- **Cons**: **sequential only** (must traverse from start), pointer storage overhead, reliability (one broken link loses rest)
- **Variation**: **FAT** (File Allocation Table) — linked list stored in a separate table in memory

## FAT (File Allocation Table)
- Each entry in FAT corresponds to a disk block
- FAT entry = next block number (or EOF, or bad)
- Root directory stored in data region (FAT32)
- **FAT cached in memory** at mount time → random access possible (table in RAM)
- Used in: MS-DOS, Windows (FAT32), USB drives, SD cards

## Indexed Allocation
- **Index block** contains array of pointers to data blocks
- Directory: `[name, index_block_number]`
- **Pros**: supports **direct access**, no external fragmentation
- **Cons**: index block overhead, max file size limited by index block size (small files waste index block)

## Multi-Level Indexed (Unix Inode)
```
Inode: [12 direct | single indirect | double indirect | triple indirect]
```
- **12 direct** pointers → first 48KB (4KB blocks)
- **Single indirect** → 1024 pointers → 4MB
- **Double indirect** → 1024×1024 pointers → 4GB
- **Triple indirect** → 1024³ pointers → 4TB
- Efficient for small files (direct pointers), scales for large files

## Extent-Based (ext4, modern FS)
- **Extent**: contiguous block range `(start_block, length)`
- Inode stores extents instead of individual block pointers
- Single extent can describe thousands of contiguous blocks
- **Drastically reduces metadata** for large sequential files
- ext4: extent tree (HTree) when more than 4 extents needed

## Comparison Table

| Method | Sequential Access | Direct Access | Fragmentation | Max File Size |
|--------|-------------------|---------------|---------------|---------------|
| **Contiguous** | ✅ Excellent | ✅ Excellent | External | Unlimited |
| **Linked** | ✅ Good | ❌ Poor | None | Unlimited |
| **FAT** | ✅ Good | ✅ Good (FAT in RAM) | External | 2TB (FAT32) |
| **Indexed** | ✅ Good | ✅ Good | None | Limited by index |
| **Unix inode** | ✅ Good | ✅ Good | Minimal | Very large |
| **Extent** | ✅ Excellent | ✅ Excellent | Minimal | Very large |

## Key Interview Questions
- Why does Unix use 12 direct pointers? → Most files are < 48KB; avoids indirect block overhead
- What is **block size** impact? → 4KB vs 1KB: larger blocks waste space but reduce pointer overhead
- How does ext4 allocate contiguous blocks? → **Multi-block allocator** (mballoc) allocates multiple blocks at once
