# Chapter: File Allocation and Free Space

## What you'll learn
- How file data blocks are allocated on disk: **contiguous** (fast but fragmented), **linked** (simple, slow random access), and **indexed** (fast random access, pointer overhead) — and how real filesystems (ext4 extents, FAT's FAT) implement them.
- How **free space** is tracked: bitmaps, free lists, and groups — and what makes each choice fast.
- **Inodes** and the metadata that ties file data together — plus **hard vs soft (symbolic) links** and their semantics.

## Prerequisites (linked)
- [Part 08 Chapter 01 Files and Directories](chapter-01-files-and-directories/README.md) — files, attributes, and directory entries (names → inodes).
- [Part 08 Chapter 03 Disk Management](chapter-03-disk-management/README.md) — disk blocks and seek behavior (why allocation layout matters).

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Contiguous, Linked and Indexed Allocation](section-01-contiguous-linked-and-indexed-allocation.md) | How do files occupy blocks, and what are the space/time trade-offs? |
| 02 | [Free Space Management](section-02-free-space-management.md) | How does the FS know which blocks are available, instantly? |
| 03 | [Inodes and Soft vs Hard Links](section-03-inodes-and-soft-vs-hard-links.md) | What is the metadata that anchors a file, and how do links reference it? |

## One-paragraph narrative connecting all sections
A directory maps a name to an inode (Chapter 01); this chapter says *how the inode's data blocks are laid out*. Section 01 compares the three classic schemes: contiguous (one extent — sequential-fast but fragile and externally-fragmented), linked (blocks chained by pointers — simple, no fragmentation, but O(n) random access), and indexed (an index block of pointers — O(1) random access, but pointer overhead); modern filesystems (ext4 extents, XFS, btrfs) blend these ideas. Section 02 shows how the allocator knows what's free — the free-space bitmap (O(1) locate, compact) vs the free list (fast sequential allocation) — and how group/zone-based designs (ext4 block groups) localize both allocation and its bookkeeping. Section 03 centers everything on the **inode**: the fixed metadata block (mode, links, owner, sizes, block pointers/extents) that `stat` reads and hard links increment; then contrasts hard links (same inode, same FS) with symlinks (path strings, cross-FS, dangling). This completes the "name → metadata → data" chain that Chapter 04's real filesystems implement.

## Common interview trap in this chapter
**Trap:** Claiming ext4 "uses linked allocation" or "uses indexed allocation" — modern ext4/XFS use **extents** (variable-size contiguous runs) plus the multilevel block pointers, which is a hybrid. Also confusing the **FAT (File Allocation Table)** — a separate table of block links, *not* per-file pointers in the file — with pure linked allocation. And: hard links can't cross filesystems; symlinks can — but symlinks cost an extra inode and an extra lookup.

## Checklist before moving on
- [ ] I can simulate contiguous/linked/indexed allocation and state each one's random-access cost.
- [ ] I can explain what extents are and why ext4/XFS use them.
- [ ] I can compare bitmap vs free-list free-space management.
- [ ] I can explain the inode's contents and why `stat` reads it.
- [ ] I can differentiate hard vs symlink behavior (link count, cross-FS, dangling).
