# Chapter: Filesystem Implementations

## What you'll learn
- **Linux filesystems**: ext4 (inodes + extents + journaling), XFS (extent/B-tree, scalability), btrfs (CoW, subvolumes, checksums, RAID).
- **Windows NTFS**: MFT, attributes, sparse files, journaling, ACLs, compression.
- **Journaling & log-structured designs**: why crash consistency is a thing, WAL-style journals, and LFS/CoW alternatives.
- **The Virtual Filesystem (VFS)**: the abstraction layer that lets `ext4`, `ntfs`, `proc`, `sysfs`, NFS, and FUSE all live under one `/`.

## Prerequisites (linked)
- [Chapter 01 Files and Directories](chapter-01-files-and-directories/README.md) — file/dir concepts.
- [Chapter 02 File Allocation and Free Space](chapter-02-file-allocation-and-free-space/README.md) — inodes, extents, allocation.
- [Chapter 03 Disk Management](chapter-03-disk-management/README.md) — the physical substrate.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Linux Filesystems: ext4, XFS, btrfs](section-01-linux-filesystems-ext4-xfs-btrfs.md) | How do real Linux filesystems structure metadata on disk? |
| 02 | [Windows NTFS](section-02-windows-ntfs.md) | How does Windows organize files, attributes, and security? |
| 03 | [Journaling and Log-Structured Filesystems](section-03-journaling-and-log-structured-filesystems.md) | How do filesystems survive crashes without corruption? |
| 04 | [Virtual Filesystem (VFS)](section-04-virtual-file-system-vfs.md) | How does the kernel serve a hundred filesystems behind one API? |

## One-paragraph narrative connecting all sections
Section 01 dives into how Linux actually stores files: ext4's inode table + extents + journal (the default), XFS's B-tree extents and 100+ TB scalability (the enterprise/parallel-FS favorite), and btrfs's copy-on-write trees, subvolumes, and checksums (the modern snapshot machine). Section 02 flips to Windows: NTFS is a different design — a Master File Table holding everything (including data in resident attributes), with its own journaling ($LogFile), ACLs, sparse files, and compression. Section 03 generalizes the "crash consistency" problem both must solve: how a power loss mid-write can corrupt a filesystem, and the three answers — journaling (WAL, order-then-replay), log-structured (append-only, no overwrite), and copy-on-write (btrfs/ZFS) — plus soft updates as the exotic fourth. Section 04 zooms out to the VFS: the kernel object model (`inode`, `dentry`, `file`, `super_block`, `address_space`) with `f_op`/`s_op` operation vectors, which is what makes `ext4`, `proc`, `sysfs`, NFS, and FUSE all feel like one tree. Together: the concrete structures of chapter 02, realized by real filesystems, made crash-safe, and unified by the VFS.

## Common interview trap in this chapter
**Trap:** Confusing "inode" (the on-disk metadata structure) with the VFS `struct inode` (in-memory cache object) — they map but aren't identical. Also: thinking a journal makes writes safe-by-default (only metadata is journaled by default; data=journal is opt-in), and assuming ext4 = journaling = crash-proof (it avoids corruption, not all data loss). And "btrfs is just like ext4" — no: it's CoW with subvolumes/snapshots/checksums, with different trade-offs.

## Checklist before moving on
- [ ] I can describe ext4's inode + extent layout and why extents beat block lists.
- [ ] I can explain XFS's B-tree structures and why it scales to huge files/systems.
- [ ] I can explain btrfs's copy-on-write trees, subvolumes, and checksums.
- [ ] I can describe NTFS's MFT and resident attributes.
- [ ] I can explain the three crash-consistency approaches (journal / LFS / CoW).
- [ ] I can draw the VFS object graph (super_block → inode → dentry → file) and name the operation vectors.
- [ ] I can explain how FUSE and proc/sysfs plug into the VFS.
