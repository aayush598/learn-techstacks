# File System Structure

## Layered File System Architecture

```
Application
    ↓ (syscall: read, write, open)
Virtual File System (VFS)
    ↓ (generic operations)
Local File System (ext4, NTFS, FAT)
    ↓ (block-level operations)
Buffer Cache / Page Cache
    ↓ (device I/O)
Device Driver
    ↓
Disk Hardware
```

## On-Disk Structures (Unix/Linux)

| Block Type | Content |
|------------|---------|
| **Boot block** | Bootstrap code to load OS |
| **Super block** | Filesystem metadata: block size, total blocks, free blocks, inode count, mount info |
| **Inode blocks** | Array of inodes (file metadata) |
| **Data blocks** | Actual file data |

## Virtual File System (VFS)
- **Abstraction layer** allowing multiple FS types to coexist (`ext4`, `NTFS`, `FAT32`, `NFS`)
- Defines **generic operations** interface (`open`, `read`, `write`, `mmap`, `fsync`)
- Every FS implements these operations via **function pointers**
- Allows seamless **mounting of remote filesystems** (NFS, CIFS)

## Linux VFS Objects (The Four Primitives)

| Object | Represents | Key Fields |
|--------|------------|------------|
| **`super_block`** | Mounted FS | s_blocksize, s_type, s_root (dentry) |
| **`inode`** | File metadata | i_mode, i_uid, i_size, i_blocks, i_atime, i_mtime, i_ctime |
| **`dentry`** | Directory entry (path component) | d_parent, d_name, d_inode |
| **`file`** | Open file descriptor | f_dentry, f_pos, f_op (operations) |

## Inode (Unix) — File Control Block
- Contains: **permissions** (rwx), **owner** (UID/GID), **timestamps**, **size**, **block pointers**
- Does **NOT** contain file name (name lives in directory entry)
- 12 **direct** pointers + 1 **single indirect** + 1 **double indirect** + 1 **triple indirect**
- Inode is fetched from disk to memory when file is first referenced

## Key Interview Questions
- What is the purpose of VFS? → Uniform interface for multiple FS, enables transparent access to network FS
- Why separate dentry and inode? → Dentry caches path lookups; inode holds metadata
- How does a syscall like `read()` traverse the layers? → `sys_read()` → VFS `file->f_op->read()` → FS-specific read → block I/O
