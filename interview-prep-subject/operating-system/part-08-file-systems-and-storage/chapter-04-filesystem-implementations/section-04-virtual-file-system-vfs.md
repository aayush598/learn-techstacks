# Virtual Filesystem (VFS)

> **TL;DR**: The VFS is the kernel's abstraction layer that lets `ext4`, `XFS`, `btrfs`, `NTFS`-via-`ntfs3`, `proc`, `sysfs`, `tmpfs`, NFS, and FUSE all live under one `/`. It defines the object model — `super_block`, `inode`, `dentry`, `file`, `address_space` — with operation-vector tables (`f_op`, `i_op`, `d_op`, `s_op`) that each filesystem implements.

## 1. Why Does This Exist?
Users, programs, and syscalls shouldn't care which filesystem backs a file: `open("/home/u/file")` should work whether `/` is ext4 and `/home` is btrfs and `/proc` is virtual. Filesystems are complex and varied (on-disk vs virtual vs network). The VFS is the "Dependency Inversion" point: system calls talk to *one* interface, and every filesystem implements that interface — so a new FS (or a FUSE-backed one, or NFS) plugs in without touching the syscall layer or the page cache. It also centralizes the things all FSs share: dentry cache, inode cache, page cache (buffered I/O), path resolution, and permission checks.

## 2. How Does It Work?
Core objects:
- **`super_block`** (`struct super_block`): one per mounted filesystem — carries `s_op` (super operations: `alloc_inode`, `sync_fs`, `write_inode`, `statfs`, `put_super`), `s_mount`, block device, etc. Lives in the superblock list.
- **`inode`** (`struct inode`): in-memory representation of a file *object* (metadata: mode, uid, size, timestamps, i_ino, i_nlink) — distinct from on-disk inode; cached in the inode cache, keyed by (fs, ino). Carries `i_op` (inode ops: `lookup`, `create`, `unlink`, `mkdir`, `getattr`, `setattr`, `setxattr`), `i_fop` (file ops for this inode type), `i_mapping` (address_space).
- **`dentry`** (`struct dentry`): directory entry — the (parent, name)→inode mapping; cached in the **dcache**; a dentry has a `d_op` (dentry ops: `d_revalidate`, `d_delete`, `d_hash`). Path lookup walks dentries.
- **`file`** (`struct file`): an open file description — `f_path` (dentry+mnt), `f_pos` (file offset), `f_flags` (O_RDONLY...), `f_op` (file ops: `read`, `write`, `read_iter`, `write_iter`, `open`, `release`, `mmap`, `fsync`, `llseek`), `f_mapping`. Created on `open`, shared by dup/fork.
- **`address_space`** (`struct address_space`): ties the file to the **page cache** — `readpage`, `writepage`, `writepages`, `a_ops`, holds radix-tree of cached pages; the bridge between VFS I/O and the actual FS.
- **`file_system_type`**: registry (`fs_types`) of known filesystems (ext4, btrfs, proc...), each with `mount` (parses opts, reads superblock).

Flow: `open("/home/u/f")` → `path_openat` → walk `/` (root dentry) → `home` (lookup via root inode's i_op) → ... → `f` → alloc dentry+inode (via `s_op->alloc_inode` + `i_op->lookup`) → build `struct file` with `f_op` = the FS's file ops → return fd. `read(fd,...)` → `fdget` → `f_op->read_iter` (or generic via page cache) → `address_space` ops → FS block I/O.

Also: **mount** builds a `mount`/`vfsmount` attaching a super_block under a dentry; **FUSE** presents a userspace daemon as a filesystem (the kernel does VFS → FUSE → /dev/fuse → daemon → real FS); **proc/sysfs** are in-memory FSs whose `i_op`/`f_op` generate data on the fly.

## 3. When Is It Used?
- Every `open/read/write/stat/mmap` on Linux routes through the VFS.
- Mounted ext4/XFS/btrfs/ntfs3/NFS/CIFS/FUSE/tmpfs/proc/sysfs/devtmpfs — all under one `/`.
- Page cache: buffered reads/writes go through `address_space` regardless of FS.
- Containers use bind mounts, overlayfs (itself a VFS filesystem), and proc per-pid namespaces.
- `mount(2)`/`umount(2)` manipulate the VFS mount tree.

## 4. Why Wasn't Another Approach Chosen?
- **Per-syscall dispatch via filesystem ID (rejected)**: would leak FS specifics into the syscall layer and break pluggability.
- **Wrapping the whole disk device (rejected)**: doesn't handle virtual/network FSs.
- **One "generic filesystem" (rejected)**: on-disk format compatibility (ext4 vs ntfs vs zfs) and FS diversity require multiple implementations.
- **VFS object model (chosen)**: clean interface + shared caches (dcache, inode cache, page cache) + operation-vector polymorphism (like C++ vtables) — exactly what made Linux able to absorb FUSE, NFS, proc, and 50+ FSs without redesigning syscalls.

## 5. Intuition
**A universal power socket**: the syscall layer is the plug — a file descriptor — and the VFS is the socket standard. Whether the appliance behind the wall is a toaster (ext4), a laser (XFS), or a hologram (proc/FUSE), the plug fits the same socket, and the socket routes to the right appliance. The operation vectors are the "interface contract" each appliance agrees to (read = pull the lever; the lever may do different things inside each appliance).

## 6. Real-World Analogy
**A restaurant kitchen**: system calls are the waiters (they only know table numbers = fds). The VFS is the pass-through counter where every dish (filesystem) has the same order slips (`open`, `read`, `write`, `fsync`) even though the kitchens are wildly different (a grill = ext4, a sous-vide = btrfs, a smoke-and-mirrors kitchen = FUSE). `super_block` = the restaurant's license (one per kitchen), `inode` = the recipe card for a dish, `dentry` = the menu line pointing at the recipe, `file` = a specific order (with its position in the meal), `address_space` = the pantry cache shared by all kitchens.

## 7. Formal Definition
The VFS (Linux `fs/`) is the in-kernel framework of filesystem-independent data types and interfaces. Key structures:
- `struct super_block` — per-mounted-FS state, `->s_op` = `{alloc_inode, destroy_inode, write_inode, drop_inode, sync_fs, statfs, remount_fs}`.
- `struct inode` — in-core file metadata with `->i_op` (inode ops) and `->i_fop` (default file ops) and `->i_mapping` (`address_space`).
- `struct dentry` — path component mapping, `->d_name`, `->d_parent`, `->d_op`, `->d_inode`; held in the **dcache** (LRU).
- `struct file` — open instance, `->f_op` `= {open, release, llseek, read_iter, write_iter, mmap, fsync, flush, splice_read, iterate}` and `->f_mapping`.
- `struct address_space` — page-cache interface `->a_ops = {readpage, readpages, writepage, writepages, write_begin, write_end, invalidatepage, releasepage, direct_IO}`.
- `struct file_system_type` — mount factory + registry.
Operations dispatch through function pointers (polymorphism); path resolution (`namei.c`) is FS-agnostic and uses `->lookup`/`->d_revalidate`. All FS implementations (real, virtual, network) conform to this interface.

## 8. Example
`open("/proc/version")` (virtual) vs `open("/etc/hosts")` (ext4):
- Both go through `do_sys_open` → `path_openat` → `link_path_walk` → `namei`.
- `/` → root super_block (ext4 on `/`); `/etc` dentry lookup hits dcache; `hosts` lookup → ext4 `i_op->lookup` → reads the directory → inode.
- `/proc/version` → at `/proc`, the mount point redirects to proc's super_block; `version` → proc `i_op->lookup` = `proc_lookup` → creates a dynamic inode whose `i_fop->read_iter` *generates* the kernel version string on read.
- `read()` on `/proc/version`: proc's `f_op->read_iter` fills a buffer from a function (no disk I/O). `read()` on `/etc/hosts`: generic `file_read_iter` → page cache → `a_ops->readpage` → ext4 `ext4_readpage` → submit_bio.

This is why "everything is a file" works: `proc`, `sysfs`, `devfs`, `sockets` (via `sockfs`), and FUSE all implement the same interface.

## 9. Internal Working
1. `do_sys_open` → `getname` (copy path) → `path_openat` → `walk_component` loops: for each component, `d_lookup` (dcache) or `inode->i_op->lookup` → `d_splice_alias` → next.
2. Final: `do_dentry_open` → `inode->i_fop->open` (FS hook) → build `struct file` → `fd_install` → return fd.
3. `read`: `vfs_read` → `f_op->read_iter` (ext4 uses `generic_file_read_iter` via page cache; proc uses custom) → page cache → `mapping->a_ops->readpage` → `submit_bio` → FS/block layer.
4. `write`: `f_op->write_iter` → `generic_perform_write` → `a_ops->write_begin/write_end` (page cache dirty) → `writepages` at flush → FS allocation + block I/O.
5. `mount`: `sys_mount` → `fs_type->mount` (e.g., `ext4_fs_type.mount = ext4_mount`) → read superblock → `sget` → attach `vfsmount`.
6. Caches: dcache + inode cache (`inode_hashtable`) + page cache (`mapping` radix/`xarray`) accelerate lookups and I/O across all FSs.

## 10. Time Complexity
- Path lookup: O(path components) dcache hits O(1) each; miss → `->lookup` + disk read per component (worst O(n · disk)).
- dcache/inode lookup: O(1) hash (dentry cache hit) — the whole point of caching.
- `read_iter`: O(n) data transfer, page-cache backed (O(1) per page hit).
- Mount: O(1) per super_block registration + FS-specific setup.
- dispatch overhead: one indirect function call per op — negligible vs actual I/O.

## 11. Advantages
- **Pluggability**: ext4/btrfs/proc/sysfs/NFS/FUSE behind one API; adding a FS = implementing the ops.
- **Shared infrastructure**: dcache, inode cache, page cache, generic read/write, namei, permission checks — written once, all FSs benefit.
- **"Everything is a file"**: virtual and pseudo filesystems give a uniform control interface (proc/sysfs).
- **FUSE**: filesystems in userspace without kernel code.
- **Consistency**: syscall API stable across FSs; mount semantics uniform.

## 12. Disadvantages
- **Indirection overhead**: function-pointer dispatch + extra object layers vs a tight FS-specific path (minor in practice).
- **Caching complexity**: cache invalidation (dcache/inode/page) correctness bugs are notoriously hard.
- **One-size-fits-all I/O model**: the page-cache/generic-read path isn't optimal for every FS (e.g., direct I/O, O_DSYNC, large sequential — FSs must opt out with `direct_IO`/own ops).
- **Security/sandboxing**: pseudo filesystems (proc/sysfs) are a large attack surface; FUSE trusts userspace daemons.
- **Locking**: global inode/dcache locks are historical bottlenecks (mitigated: per-inode locks, RCU path walk).

## 13. Interview Questions
1. **Q: What is the VFS?** A: The kernel's filesystem abstraction: a common object model (`super_block`, `inode`, `dentry`, `file`, `address_space`) + operation vectors so syscalls work uniformly across all filesystems — real, virtual, and network.
2. **Q: Name the core VFS objects and their roles.** A: `super_block` (one per mounted FS, `s_op`), `inode` (file metadata, `i_op`/`i_fop`), `dentry` (name→inode, dcache), `file` (open instance, `f_op`, offset), `address_space` (page cache binding, `a_ops`).
3. **Q: inode vs dentry vs file?** A: `inode` = the file object (metadata) shared by all links; `dentry` = the *name* mapping (one per directory entry/path component); `file` = one *open* instance (position, flags). Multiple dentries and files can reference one inode.
4. **Q: What is the dcache?** A: The dentry cache — recently-resolved path components, making repeated `open()`s O(1) without disk directory reads; invalidation happens on unlink/rename.
5. **Q: What is the `address_space`?** A: The per-inode interface to the page cache: `a_ops` (`readpage`, `writepage`, `write_begin`...) — the glue between VFS I/O and the filesystem's block storage, used by all buffered I/O.
6. **Q: How does the VFS support proc/sysfs/FUSE?** A: They're filesystems too: they register a `file_system_type` and implement `i_op`/`f_op` whose methods *generate* data in memory (proc) or forward to a userspace daemon (FUSE) — no disk behind them.
7. **Q: What happens in `open("/a/b")`?** A: `do_sys_open` → path walk: dcache lookup per component, else `inode->i_op->lookup` → build dentry/inode → `f_op->open` → `struct file` → fd. One pass, cached afterward.
8. **Q: What is `f_op`?** A: The file operation vector — the method table (`open`, `read_iter`, `write_iter`, `llseek`, `mmap`, `fsync`, `release`) that makes a `struct file` work; each FS provides its own.
9. **Q: How do syscalls and VFS relate to a specific FS?** A: `sys_read` → `vfs_read` → `f_op->read_iter` → FS-specific implementation (generic page-cache read for ext4, custom for proc). The syscall never knows the FS.
10. **Q: What is a superblock in VFS?** A: Per-mounted-filesystem state (device, size, ops `s_op`, root inode); `sget`/`alloc_super` creates one at mount; all FSs derive from the VFS `super_block` struct.
11. **Q: What is FUSE exactly?** A: A VFS filesystem whose ops forward requests over `/dev/fuse` to a userspace daemon — letting you write a filesystem in userspace (sshfs, ntfs-3g, rclone mount) without kernel code.
12. **Q: How is the VFS used for mount points?** A: `sys_mount` calls the FS's `mount` op → creates `super_block` + root `dentry` + a `vfsmount` attached to the mount-point dentry in the mount tree; path walk follows mounts.

## 14. Follow-Up Questions
1. **Q: What is overlayfs?** A: A VFS-level union filesystem (lower + upper) used by containers and image layers — pure VFS (no new on-disk format), just composition of existing FSs.
2. **Q: What is direct I/O vs buffered?** A: `O_DIRECT` bypasses the page cache (`direct_IO` a_op) — for DBs; VFS still routes it, just with no caching layer.
3. **Q: What is RCU path walking?** A: Lock-free dentry lookup in `namei.c` (read-copy-update) — concurrent path resolution without big locks.
4. **Q: How do filesystems implement `mmap`?** A: `f_op->mmap` → the VFS maps the file into a process via the address_space (`filemap_map_pages`) — page faults call `readpage` from the FS.

## 15. Coding Example
```c
// Illustration of the VFS op-dispatch idea (greatly simplified)
#include <stdio.h>
#include <string.h>

typedef struct file file_t;
typedef int (*read_fn)(file_t *, char *, size_t);
typedef int (*write_fn)(file_t *, const char *, size_t);

typedef struct file_ops { read_fn read; write_fn write; } file_ops_t;

struct file { const file_ops_t *ops; void *priv; };

// ext4-like implementation: read from "disk" (a buffer here)
static int ext4_read(file_t *f, char *buf, size_t n) {
    const char *data = "ext4 disk contents";
    size_t m = strlen(data) < n ? strlen(data) : n;
    memcpy(buf, data, m);
    return (int)m;
}

// proc-like implementation: generate the data on the fly
static int proc_read(file_t *f, char *buf, size_t n) {
    const char *data = "Linux version 6.x (proc-generated)";
    size_t m = strlen(data) < n ? strlen(data) : n;
    memcpy(buf, data, m);
    return (int)m;
}

static const file_ops_t ext4_ops = { ext4_read, 0 };
static const file_ops_t proc_ops = { proc_read, 0 };

// THE SYSCALL: doesn't know which FS it's talking to
static ssize_t vfs_read(file_t *f, char *buf, size_t n) {
    if (f->ops && f->ops->read) return f->ops->read(f, buf, n);
    return -1;
}

int main(void) {
    file_t f1 = { .ops = &ext4_ops }, f2 = { .ops = &proc_ops };
    char buf[64];
    vfs_read(&f1, buf, sizeof buf); printf("ext4: %s\n", buf);
    vfs_read(&f2, buf, sizeof buf); printf("proc: %s\n", buf);
    return 0;
}
```

## 16. Industry Usage
- **Linux kernel** `fs/`: `namei.c`, `super.c`, `inode.c`, `dentry.c`, `file_table.c`, `buffer.c`, `read_write.c`, `open.c`, `fs_context.c`.
- **Real FSs under VFS**: ext4, XFS, btrfs, ntfs3, exfat, tmpfs, ramfs, proc, sysfs, cgroup, overlayfs, squashfs, NFS, CIFS, FUSE, sockfs (sockets), epoll (via `eventpoll`).
- **FUSE**: sshfs, ntfs-3g, rclone, gocryptfs, Docker/containerd storage drivers.
- **Databases**: PostgreSQL uses `O_DIRECT`/posix_fadvise through the VFS; `pg_test_fsync` measures VFS flush behavior.

## 17. References
- Love, *Linux Kernel Development*, Ch. 12 "The Virtual Filesystem".
- Silberschatz, *Operating System Concepts*, Ch. 12 "File-System Implementation" (VFS), Ch. 11.
- Tanenbaum, *Modern Operating Systems*, Ch. 4.3 "File system implementation" (VFS in Linux).
- Linux kernel docs: `Documentation/filesystems/vfs.rst` (the canonical VFS doc).
- `man 2 open`, `man 2 read`, `man 2 mount`, `man 2 mmap`.

## 18. Cheat Sheet
- VFS objects: super_block (mount), inode (file), dentry (name), file (open), address_space (page cache).
- Op vectors: `s_op`, `i_op`, `i_fop`/`f_op`, `d_op`, `a_ops`.
- Dispatch = function pointers (polymorphism).
- dcache = dentry cache (path walk O(1) hits).
- Page cache shared via address_space (buffered I/O).
- proc/sysfs = generated in memory; FUSE = userspace daemon.
- `open` → path walk → lookup → build file → fd.
- "Everything is a file" lives in the VFS.

## 19. Quiz
1. One per mounted filesystem? a) inode b) super_block c) dentry d) file → **b**
2. Maps name→inode? a) file b) dentry c) address_space d) fd → **b**
3. Page cache interface? a) s_op b) i_op c) a_ops d) d_op → **c**
4. Proc files are generated by? a) disk b) i_op/f_op functions c) RAM d) cache → **b**
5. FUSE runs filesystems? a) in kernel b) in userspace c) in BIOS d) in VM → **b**
6. Path walk uses which cache? a) page b) dcache c) TLB d) superblock → **b**

## 20. Flashcards
- **Q: What is the VFS?** → **A:** FS abstraction: super_block/inode/dentry/file/address_space + op vectors.
- **Q: super_block?** → **A:** One per mounted FS, `s_op`.
- **Q: dentry vs inode?** → **A:** name mapping vs file metadata.
- **Q: address_space?** → **A:** Page cache binding, `a_ops`.
- **Q: proc/sysfs/FUSE?** → **A:** In-memory generated / userspace-daemon filesystems.
- **Q: open() flow?** → **A:** path walk → dcache/lookup → file + fd.

## 21. Revision
The VFS is Linux's answer to "many filesystems, one API": a small object model — `super_block` (per mount), `inode` (file metadata), `dentry` (name→inode, cached in the dcache), `file` (open instance), and `address_space` (page-cache binding) — plus operation-vector tables (`s_op`, `i_op`, `f_op`, `d_op`, `a_ops`) that each FS implements via function pointers. Syscalls (`open`, `read`, `write`, `mmap`, `mount`) go through generic VFS code that dispatches to FS methods, so ext4, XFS, btrfs, ntfs3, proc, sysfs, NFS, and FUSE all live under one `/` and share caches (dcache, inode, page). This is also why "everything is a file" works and why new filesystems (FUSE daemons, overlayfs, new on-disk formats) join without kernel syscall changes. It's the capstone that makes Sections 01–03 of this chapter fit together.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the VFS?" | 1 Why / 13 Q1 |
| "Name the core objects and roles." | 13 Q2 / 2 How |
| "inode vs dentry vs file?" | 13 Q3 / 7 Formal |
| "What is the dcache?" | 13 Q4 / 9 Internal |
| "What is the address_space?" | 13 Q5 / 7 Formal |
| "How do proc/sysfs/FUSE work?" | 13 Q6 / 8 Example |
| "What happens in open()?" | 13 Q7 / 8 Example |
| "What is FUSE?" | 13 Q11 / 16 Industry |
