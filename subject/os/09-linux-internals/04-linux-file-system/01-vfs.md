# Virtual File System (VFS)

## Purpose
- **Abstract layer** unifying different filesystem types
- Allows `open()`, `read()`, `write()` to work on ext4, NFS, tmpfs identically
- Similar to object-oriented design: each FS provides operations

## Four Core VFS Objects

| Object | Purpose | Kernel struct |
|--------|---------|---------------|
| **super_block** | Mounted filesystem info | `struct super_block` |
| **inode** | File metadata (no name) | `struct inode` |
| **dentry** | Directory entry (links name → inode) | `struct dentry` |
| **file** | Open file descriptor (associated with process) | `struct file` |

## super_block
- Created when filesystem mounted
- Contains: device info, block size, operations, mount point
- `s_root`: dentry of root directory
- `s_op`: filesystem-specific operations (`alloc_inode`, `destroy_inode`, `write_super`)

## inode
- **Metadata**: size, permissions, timestamps, block pointers
- **Does NOT** contain filename (that's dentry)
- Each inode has unique **inode number** within filesystem
- `i_op`: inode operations (`create`, `lookup`, `link`, `unlink`, `mkdir`, `rmdir`)
- `i_fop`: file operations (see below)

## dentry
- Maps **path component** to inode: `"/usr" → inode_of_usr`
- Forms directory hierarchy tree
- Three states: **used** (in use), **negative** (name exists but no inode), **unused**
- Not stored on disk (memory-only construct)

## file
- Represents an **open file** (one inode can have many file objects)
- `f_pos`: current read/write position
- `f_op`: file operations (`read`, `write`, `mmap`, `llseek`)
- Created by `open()`, destroyed by `close()`

## Dentry & Inode Caches
- **dentry cache** (dcache): caches directory entries → fast path resolution
- **inode cache**: caches recently accessed inodes
- Both reduce disk I/O significantly
- Memory pressure → caches shrink (reclaimable)

## File Operations
```c
struct file_operations {
    loff_t (*llseek)(...);
    ssize_t (*read)(...);
    ssize_t (*write)(...);
    int (*mmap)(...);
    int (*open)(...);
    int (*release)(...);
};
```

## Registered Filesystems
- View with `cat /proc/filesystems`
- Common: ext4, XFS, btrfs, tmpfs, proc, sysfs, nfs, overlay
