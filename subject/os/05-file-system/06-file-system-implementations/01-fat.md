# File System — FAT (File Allocation Table)

## Overview
- **FAT12/16/32**: Microsoft's legacy FS family
- Simple, **widely compatible** (all OSes, cameras, game consoles, USB drives)
- No journaling, no permissions (beyond basic), no encryption

## On-Disk Layout (FAT32)
```
[Reserved Sectors | FAT #1 | FAT #2 (copy) | Root Directory | Data Region]
```
- **Reserved sectors**: boot sector (BPB — BIOS Parameter Block), FS info
- **FAT tables**: two copies (FAT #1 + backup); 32-bit entries each
- **Root directory**: special location in FAT32 (not fixed size like FAT16)
- **Data region**: clusters storing file/directory contents

## Key Concepts
- **Cluster**: basic allocation unit (1, 2, 4, 8, 16, 32 sectors); power of 2
- FAT entry per cluster: value = next cluster, **`EOF`** (0x0FFFFFFF), **`BAD`** (0x0FFFFFF7), or **`FREE`** (0x00000000)
- Files are **linked lists of clusters** via FAT table
- FAT cached in RAM → semi-random access possible

## FAT32 Limitations

| Feature | FAT32 Limit | Why It Matters |
|---------|-------------|----------------|
| **Max volume** | 2TB (32-bit entries limit) | Can't format larger drives as FAT32 |
| **Max file size** | 4GB (32-bit size field) | Can't store 4K movies |
| **Max files** | ~268M (cluster count) | Plenty for most uses |
| **Max filename** | 8.3 + VFAT (255 chars) | VFAT extension in directory entries |
| **Fragmentation** | Severe | No defragmentation avoidance |
| **Permissions** | ❌ None | No file security |
| **Journaling** | ❌ None | Corruption on power loss |
| **Compression** | ❌ None | |
| **Encryption** | ❌ None | |

## exFAT (FAT64)
- Microsoft's modern replacement for flash storage
- **Max file size**: 16EB; **Max volume**: 128PB
- No journaling (simple, fast for flash)
- Supports larger cluster sizes (up to 32MB)
- Used in: SDXC cards (>32GB), USB drives

## Key Interview Questions
- Why does FAT have two copies of the FAT table? → Redundancy; if first FAT sector dies, backup exists
- How does deletion work? → Mark FAT entry as `FREE`; data remains on disk until overwritten
- Why 4GB max file on FAT32? → 32-bit file size field in directory entry → 2³² bytes = 4GB
- How does **fragmentation** happen in FAT? → Non-contiguous cluster chain; frequent writes/deletes scatter free clusters
