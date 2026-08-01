# Part: File Systems and Storage

> **TL;DR**: File systems give durable, named, structured storage on top of raw disks — this part covers files & directories, allocation and free-space management, disk structure/scheduling, RAID, and how Linux (ext4/XFS/btrfs), Windows (NTFS), and the VFS layer actually implement it all.

## What this part covers
Part 08 explains the storage stack from the file abstraction down to the spinning/SSD disk: how files and directories are represented and accessed, how block allocation and free-space management work (contiguous/linked/indexed, inodes, hard vs soft links), how disks are organized and scheduled (FCFS/SSTF/SCAN/C-SCAN/LOOK), how RAID levels trade off performance/reliability, how modern SSDs change the calculus, and the real implementations (ext4, XFS, btrfs, NTFS, journaling, log-structured, and the Linux VFS layer).

## Chapter map (chapter → sections → key skills)

| Chapter | Sections | Key skills you'll gain |
|---|---|---|
| **Chapter 01: Files & Directories** | file concept/attributes/operations; directory structures; file access methods | Design file attributes; compare single/two/multi-level + tree directory structures; explain sequential vs direct vs indexed access |
| **Chapter 02: File Allocation & Free Space** | contiguous/linked/indexed allocation; free-space management; inodes & links | Allocate files with each scheme (external fragmentation, pointer overhead); manage free lists/bitmaps; explain inodes and hard vs symlink behavior |
| **Chapter 03: Disk Management** | disk structure & scheduling; RAID levels; SSDs & hybrid | Compute seek/rotational latency; trace FCFS/SSTF/SCAN/C-SCAN/LOOK; design RAID 0-6/10; explain SSD wear leveling & TRIM |
| **Chapter 04: FS Implementations** | ext4/XFS/btrfs; NTFS; journaling & log-structured; VFS | Describe ext4 extents + journaling, XFS vs btrfs features, NTFS MFT, journaling vs LFS, and the VFS dispatch model |

## Study order
1. **Chapter 01** — the file abstraction (what the OS exposes to apps).
2. **Chapter 02** — how files occupy and reclaim disk space (the allocator's view).
3. **Chapter 03** — the disk hardware + scheduling + RAID (the physical layer).
4. **Chapter 04** — real filesystems and the VFS that unifies them (the production layer).

## Interview importance
★★★★★ — file systems and storage are top-5 OS interview topics, especially for storage/infra roles (Amazon S3/EBS, AWS, NetApp, Pure Storage, Nvidia, database teams). Every systems round asks about RAID levels, disk scheduling, inodes vs links, journaling, and "how does `read()` actually work."

## How the parts connect (roadmap)
- **Part 06/07 (Memory)** — page cache and mmap glue memory to files; buffer/page cache is where file I/O actually lands.
- **Part 09 (Linux Internals)** — syscalls like `open/read/write/stat`, file descriptors, and the VFS `file_operations` dispatch.
- **Part 04 (Synchronization)** — RAID and FS operations need locking (superblock, inode locks); journaling is a concurrency/crash story.
