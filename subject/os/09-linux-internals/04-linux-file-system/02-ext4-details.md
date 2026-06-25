# ext4 Filesystem

## Overview
- Default filesystem on most Linux distributions
- Backward-compatible with **ext2/ext3**
- Supports: volumes up to 1 EB, files up to 16 TB
- **Journaling**: ensures consistency after crash

## Extents
- Replaces indirect block mapping (ext2/ext3)
- **Extent**: contiguous block range `(start_block, length)`
- Single extent can map up to 128 MB (4KB blocks)
- ext4 inode has 4 extents in-line; more stored in extent tree
- Reduces metadata, improves large-file performance

## Delayed Allocation
- **Delay block allocation** until data is flushed to disk
- When `write()` called: data goes to page cache, blocks not allocated yet
- Blocks allocated when **writeback** occurs (or fsync)
- Better contiguous allocation (extents are larger)

## Journaling
- Records metadata (and optionally data) changes in **journal**
- After crash: replay journal to restore consistency
- Located in:
  - `.journal` file (regular extents)
  - Separate journal device (external journal)

| Journal Mode | Metadata | Data | Safety | Performance |
|-------------|----------|------|--------|-------------|
| **journal** | Yes | Yes | Best | Slowest |
| **ordered** (default) | Yes | Yes (written first) | Good | Moderate |
| **writeback** | Yes | No | Weak (data corruption possible) | Fastest |

## Key Features
- **Multi-block allocator** (mballoc): allocates multiple blocks at once
- **Lazy initialization**: inode tables initialized in background (fast mkfs)
- **Extents** (reduces fragmentation)
- **Flexible block groups**: block groups flexibly combined
- **Uninit_BG**: keeps block group bitmap uninitialized (fast fsck)
- **Online defragmentation**: `e4defrag` tool
- **Timestamps**: nanosecond precision, birth time (crtime)
