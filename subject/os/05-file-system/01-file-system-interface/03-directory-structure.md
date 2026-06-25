# Directory Structure

## Types of Directory Structures

| Structure | Description | Pros | Cons |
|-----------|-------------|------|------|
| **Single-level** | One directory for all files | Simple | Name collision, no grouping |
| **Two-level** | Per-user directory (UFD + MFD) | Isolated users, no collisions | No sub-grouping |
| **Tree-structured** | Hierarchical directories | Flexible, natural organization | Cannot share files easily |
| **Acyclic-graph** | Tree + links/shared subdirectories | Share files via multiple paths | Must manage cycles (garbage collection) |
| **General graph** | Cycles allowed | Max flexibility | Need cycle detection |

## Current Directory & Paths
- **Current directory** (`pwd`): per-process attribute, avoids full paths
- **Absolute path**: from root `/` (e.g., `/home/user/file.txt`)
- **Relative path**: from current directory (e.g., `docs/file.txt`)
- **`.`** = current dir; **`..`** = parent dir

## Directory Operations
- `Create` directory entry, `Delete` (must be empty unless `rm -rf`), `List` contents
- `Rename` (may move between directories), `Link` (hard/symlink), `Unlink` (remove entry)
- `Mount`: attach filesystem to a mount point directory

## Hard Links vs Symbolic Links

| Feature | **Hard Link** | **Symbolic Link** (Soft) |
|---------|---------------|--------------------------|
| Points to | Inode (same inode number) | Pathname (string) |
| Survives target deletion | ✅ Yes | ❌ No (dangling) |
| Across filesystems | ❌ No | ✅ Yes |
| Directories | ❌ No (except `.` and `..`) | ✅ Yes |
| Size of link | Same size as original | Path string length |
| `ls -l` shows | Link count increments | `file -> target` |

- **Reference count**: number of hard links; inode deleted only when count reaches 0
- **Dangling symlink**: target deleted, symlink still exists but points to nothing

## Mounting
- `mount -t ext4 /dev/sda1 /mnt` → attaches device to directory tree
- Mount table: maps mount points → superblock → device
- **`/etc/fstab`**: automatic mounts on boot

## Key Interview Questions
- Why no hard links for directories? → Prevents cycles in filesystem graph
- What happens when you `unlink` a file? → Decrements link count; data blocks freed if count = 0
- How does `mount` work internally? → VFS creates mount entry, replaces directory inode with root inode of mounted FS
