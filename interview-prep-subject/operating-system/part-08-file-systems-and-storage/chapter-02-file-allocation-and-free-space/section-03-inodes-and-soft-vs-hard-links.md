# Inodes and Soft vs Hard Links

> **TL;DR**: The **inode** is the fixed metadata block (mode, link count, owner, size, times, block pointers/extents) that anchors a file's identity; a **hard link** is another directory entry pointing to the *same* inode (link count++), while a **soft/symbolic link** is a tiny separate file holding a pathname — with different semantics for deletion, cross-filesystem use, and dangling.

## 1. Why Does This Exist?
A directory entry is just `name → inode number` (Chapter 01 Sec 02); the inode is where the *real* file lives: all attributes and the map to data blocks. Inodes exist so that metadata is stored once per file, referenced by any number of names — which is precisely what enables hard links. Links exist because files are useful under multiple names: an alias for a frequently-used binary, a versioned name pointing at the latest build, a shortcut across directories. Two link kinds exist because hard links are *limited* (same filesystem, tied to inode identity) while symlinks are *arbitrary* (any path, cross-FS, can dangle) — each answers a different "I want this file under another name" need.

## 2. How Does It Work?
**Inode** (Unix `struct inode`): 
- Fixed-size table entry (ext4: 256 bytes), numbered globally per filesystem.
- Contents: mode/permissions, owner/group, size, atime/mtime/ctime, **link count**, block count, and data pointers (ext4: 4 extents inline → extent tree).
- Directories map names to inode numbers; `stat()` reads inode fields; the inode table lives in each block group.
**Hard link** (`link()`/`ln`): adds a directory entry `newname → inode X` and increments X's link count. No data copy; both names are equal (no "original"); deletion decrements the count.
**Soft link** (`symlink()`/`ln -s`): creates a *new inode* of type symlink whose data is the target path string; the kernel resolves it during path walk. It can point anywhere (cross-FS, nonexistent → dangling); deletion removes only the link.

## 3. When Is It Used?
- **Hard links**: `ln` for deduplication of a file across names; backup/hard-link strategies; `./foo` `../foo` and `.`/`..` are hard links to directories; ctime/link-count inspection.
- **Symlinks**: `/usr/bin/python3 → python3.12`; `/usr/lib/libc.so → libc.so.6`; `~` shortcuts in `/root`→`/home`? (no — `~` is shell); package managers (`update-alternatives`); cross-filesystem shortcuts; `/proc` links; macOS/Windows junctions.
- **Inode metadata**: `stat`, `ls -i`, `df -i` (inode exhaustion), backup tools (rsync inode tracking).

## 4. Why Wasn't Another Approach Chosen?
- **Storing attributes in each directory entry (rejected)**: duplicates metadata, breaks sharing (editing one copy desyncs others) — the inode centralizes.
- **One directory entry per file, always (rejected)**: no aliasing; links were requested by users.
- **Only hard links (rejected)**: can't cross filesystems, can't link to directories safely, can't dangle — insufficient.
- **Only symlinks (rejected)**: cost an extra inode + an extra resolution step per access; hard links are cheaper and safer for same-FS aliasing.
- **Copy the file (rejected)**: wastes space and diverges — links avoid copies.

## 5. Intuition
The inode is the **file's passport**: one document holds all the identity (owner, size, times, where the body lives), and any number of name-tags (directory entries) can be attached to it. A hard link = a second name-tag on the same passport; rip off one tag and the person still exists (link count 2→1). A symlink = a sticky note that says "see `/that/other/person`" — the note itself is a separate little document; if the person leaves, the note stays but points nowhere (dangling).

## 6. Real-World Analogy
A **parking garage** assigns each car a numbered bay (inode). The front desk can issue two different claim tickets for the same bay (hard links) — handing back either ticket gets the same car; both tickets are equivalent. A "parking pass to another garage" (symlink) is a different kind of ticket that simply says "drive to Garage B, bay 12" — it works even if Garage B is a different company (cross-FS), but if the car moves, the pass dangles.

## 7. Formal Definition
An **inode** (index node) is the filesystem's metadata record for a file: it contains the mode (type + permissions), owner/group identifiers, file size, access/modification/status-change timestamps, link count, block count, and the mapping from logical file blocks to physical blocks (pointers or extents). It is created at file creation and freed when its link count reaches zero and no processes hold it open. A **hard link** is an additional directory entry that references an existing inode, incrementing its link count; all hard links are equal names for the same file. A **symbolic link** is a distinct file (inode) whose content is a pathname; path resolution follows it (with loop limits), it may reference files on other filesystems, and it may dangle if the target is absent.

## 8. Example
`ln /data/report.pdf /data/report-backup.pdf`:
- Both names → inode 100. Inode 100's link count: 1 → 2. No data copy.
- `stat`: same size, same mtime, same inode (`ls -i` shows 100 for both).
- `rm /data/report.pdf`: entry removed, link count 2 → 1, data still accessible via report-backup.pdf.
- `rm /data/report-backup.pdf`: count 1 → 0 → inode 100 + data blocks freed.

`ln -s /data/report.pdf /tmp/latest.pdf`:
- Creates a *new* inode (say 200) of type symlink with data = `/data/report.pdf`.
- `ls -l`: `latest.pdf -> /data/report.pdf`. `stat` follows → inode 100; `lstat` → inode 200.
- `rm /data/report.pdf`: inode 100 freed; `/tmp/latest.pdf` now **dangles** (opening → ENOENT).

## 9. Internal Working
1. **Create**: `create()` allocates a fresh inode from the group's inode table, initializes mode/owner/times, link count 1.
2. **Hard link**: `link()` → allocate a directory entry (name, inode#), bump link count; journaled so the count matches entries (crash-safe).
3. **Symlink**: `symlink()` → allocate inode (type `S_IFLNK`), write the path string as its data (fast path: inline in the inode for short links).
4. **Resolution**: path walk checks `S_ISLNK`; if symlink, read the path, re-walk (loop limit → `ELOOP`; `O_NOFOLLOW` skips).
5. **Delete**: `unlink()` removes the entry, decrements count; if 0 and no open handles → free inode + blocks (ext4: also free extents, update bitmap).
6. **stat vs lstat**: stat resolves the chain to the target inode; lstat reads the link's own inode.
7. **inode exhaustion**: a filesystem full of tiny files runs out of inode-table slots before space (`df -i`).

## 10. Time Complexity
- Hard link create: O(1) (dir entry + count).
- Symlink create: O(1) (small file).
- Path resolution per component: O(1) dcache; symlink adds O(target path length).
- `stat`: O(1) (read inode).
- Delete: O(1) (entry + count decrement); freeing large files O(#extents).
- Hard-linked-tree dedup (e.g., `rdfind`): O(n log n) hashing.

## 11. Advantages
- **Inode**: single metadata record — no duplication, atomic stat, easy fsck.
- **Hard links**: zero-copy aliasing, same-FS dedup, deletion-safe (other links survive), cheap.
- **Symlinks**: arbitrary targets (cross-FS, cross-machine via NFS), versioned/reconfigurable names, dangling allowed (pointers to not-yet-existing files), no link-count bookkeeping.
- Both integrate with the directory name-resolution machinery.

## 12. Disadvantages
- **Hard links**: same-FS only; can't link directories (loop/gc hazard); link count must stay consistent (crash → count/entries mismatch); ambiguous "which is the original" (none).
- **Symlinks**: extra inode + extra path resolution per access; dangling targets cause ENOENT surprises; symlink loops possible (ELOOP); permission confusion (chown on a symlink is often a no-op on the link itself).
- **Inodes**: fixed table size → inode exhaustion; per-FS numbers not globally unique (hard links across FS impossible).

## 13. Interview Questions
1. **Q: What is an inode?** A: The FS metadata record: mode/type, permissions, owner, size, times, link count, and block/extent pointers — the "identity card" of a file, referenced by directory entries.
2. **Q: What's the difference between a hard and a soft link?** A: Hard = another directory entry for the same inode (link count++, same FS, no copy, equal names). Soft = a new symlink file holding a target path (cross-FS, can dangle).
3. **Q: Why can't hard links cross filesystems?** A: Inodes are numbered per-filesystem; a directory entry in FS-A can't reference an inode in FS-B — there's no global inode namespace.
4. **Q: What happens to data when you delete a hard link?** A: Only that name disappears; link count decrements; data lives until count reaches 0 (and no open handles).
5. **Q: What is a dangling symlink?** A: A symlink whose target doesn't exist — legal (unlike hard links); opening it → ENOENT; `readlink` still works.
6. **Q: Why can't you hard-link directories? (Tricky)** A: Cycles would break traversal (`find`), deletion, and reference counting; POSIX forbids it (only root via special FS features); `.` and `..` are the exceptions.
7. **Q: What does `stat` vs `lstat` tell you about a symlink?** A: `stat` follows to the target's inode; `lstat` reports the link's own inode (type symlink, size = path length).
8. **Q: What is inode exhaustion?** A: Running out of inode-table slots (filesystem full of tiny files) — `df -i` shows it; the fix is `mkfs -N more-inodes` or a different FS — the disk still has free blocks.
9. **Q: How do backup tools exploit hard links?** A: They detect hard-linked files (same inode) and back up the data once, recording multiple names — saving space (and `rsync -H` preserves them).
10. **Q: When is a symlink preferable to a hard link? (Production)** A: Cross-filesystem references, versioned tooling (`python3 → python3.12`), reconfigurable system paths, and anything that must keep working when targets are swapped.
11. **Q: What's `link count` in `ls -l`?** A: The number of hard links to the inode (directories: 2 + subdirectory count, because of `.` and `..`).
12. **Q: Why is a symlink "cheap" but not free?** A: It consumes an inode and an extra lookup per access; for hot paths (libc), the kernel caches the resolution (dcache) so the cost amortizes.
13. **Q: What does `O_NOFOLLOW` do?** A: Makes `open` fail with ELOOP if the final component is a symlink — security hardening against symlink-race (TOCTOU) attacks on setuid programs and /tmp.
14. **Q: How do containers use links?** A: Overlay filesystems and container images use symlinks and hard-link-like semantics for whiteouts/merging; `update-alternatives` manages symlinked toolchains.

## 14. Follow-Up Questions
1. **Q: How do you find all hard links to a file?** A: `find / -inum <inode>` (same inode number, same FS) or `ls -li`; tools like `stat` show link count.
2. **Q: What is a "whiteout" in overlayfs?** A: A symlink-like marker (chardev 0/0) telling the overlay that a lower-layer file is deleted — links reused for filesystem semantics.
3. **Q: How does ext4 recover from a link-count mismatch?** A: fsck recomputes counts from directory entries during a check pass — a classic journaling/fsck duty.
4. **Q: What's the difference between `~` (shell) and a symlink?** A: `~` is shell expansion of `$HOME`, not a filesystem object; symlinks are actual filesystem objects resolved by the kernel.

## 15. Coding Example
```c
// Demonstrate hard links vs symlinks: link counts, stat/lstat, dangling
#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

int main(void) {
    const char *base = "/tmp/inodedemo";
    mkdir(base, 0755);
    const char *orig = "/tmp/inodedemo/file.txt";
    const char *hard = "/tmp/inodedemo/hard.txt";
    const char *soft = "/tmp/inodedemo/soft.txt";

    FILE *f = fopen(orig, "w"); fputs("data", f); fclose(f);
    link(orig, hard);                 // hard link
    symlink(orig, soft);              // symlink

    struct stat a, b, c;
    stat(orig, &a); stat(hard, &b); lstat(soft, &c);
    printf("orig inode=%ld links=%ld\n", (long)a.st_ino, (long)a.st_nlink);
    printf("hard inode=%ld links=%ld\n", (long)b.st_ino, (long)b.st_nlink);
    printf("symlink inode=%ld type=link? %s size=%ld\n",
           (long)c.st_ino, S_ISLNK(c.st_mode) ? "yes" : "no", (long)c.st_size);

    unlink(orig);                     // hard link survives, symlink dangles
    struct stat d;
    int ok = stat(hard, &d);          // hard still valid
    int bad = stat(soft, &d);         // dangling -> ENOENT
    printf("after unlink: hard ok=%d, symlink errno? ok=%d\n", ok == 0, bad == 0);
    return 0;
}
```

## 16. Industry Usage
- **ext4/XFS/btrfs**: `struct ext4_inode`, inode tables per group, extent trees; `df -i`.
- **NTFS**: MFT records play the inode role; hard links = `POSIX` hard links; junctions/symlinks for paths.
- **APFS**: inodes + firmlinks (a filesystem-level symlink).
- **Tools**: `ln`, `ln -s`, `stat`, `ls -i`, `find -inum`, `rsync -H`, `tar --hard-dereference`.
- **Packaging**: Debian `update-alternatives`, npm's `.bin` symlink farm, `libc.so → libc.so.6`.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 11.1.1 (file attributes) and Ch. 11.6 (implementation: inode).
- Tanenbaum, *Modern Operating Systems*, Ch. 4.3.2.
- Linux source: `fs/ext4/inode.c`, `include/linux/fs.h` (`struct inode`), `fs/namei.c` (symlink resolution).
- `man 2 link`, `man 2 symlink`, `man 2 stat`, `man 7 symlink`.

## 18. Cheat Sheet
- Inode = mode, owner, size, times, link count, block pointers/extents.
- Hard link: new dir entry → same inode; count++; same-FS only.
- Symlink: new inode whose data is a path; cross-FS; can dangle.
- stat follows symlinks; lstat reads the link.
- Delete frees data when count=0 and no open handles.
- Dirs: link count = 2 + subdirs (`.` and `..`).
- Inode exhaustion: `df -i` — full of tiny files.
- O_NOFOLLOW guards against symlink-race attacks.
- `.` and `..` are hard links to directories (the only dir hard links).

## 19. Quiz
1. The inode stores:
   a) the file name b) metadata + block pointers c) directory entries d) the FAT → **b**
2. After `ln a b`, the link count is:
   a) 1 b) 2 c) 3 d) 0 → **b**
3. Symlinks can:
   a) cross filesystems b) dangle c) be loops-limited d) all → **d**
4. `stat` on a symlink reports:
   a) the link itself b) the target's inode c) nothing d) ENOENT → **b**
5. Data is freed when:
   a) any unlink b) link count=0 and no open handles c) close d) fsync → **b**
6. A symlink's content is:
   a) data blocks b) a pathname string c) an inode number d) a bitmap → **b**

## 20. Flashcards
- **Q: What is an inode?** → **A:** Metadata record (mode, owner, size, times, links, block/extent pointers).
- **Q: Hard vs symlink?** → **A:** Hard = same inode, count++ (same FS); sym = path-file (cross-FS, dangling OK).
- **Q: When is data freed?** → **A:** Link count 0 AND no open file handles.
- **Q: stat vs lstat on a symlink?** → **A:** stat follows; lstat reads the link's own inode.
- **Q: Why no hard-linked dirs?** → **A:** Cycles break traversal/gc; only `.` and `..` exist.
- **Q: What is inode exhaustion?** → **A:** Full of tiny files → inode table exhausted (`df -i`).

## 21. Revision
The inode is the file's metadata record — mode, owner, size, times, link count, and block/extent pointers — anchored by directory entries that map names to inode numbers. Hard links add another entry to the same inode (count++, same-FS only, zero-copy, equal names, deletion-safe). Symlinks are separate tiny files containing target paths — cross-FS, dangling allowed, but cost an inode and a resolution step. `stat` follows symlinks, `lstat` doesn't; data is freed at link count 0 with no open handles; inode tables can exhaust on filesystems full of tiny files. These semantics underpin `ln`, backup dedup, packaging tools, and container filesystems.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is an inode?" | 2 How / 13 Q1 |
| "Hard vs soft links?" | 13 Q2 / 8 Example |
| "Why can't hard links cross FS?" | 13 Q3 / 12 Disadvantages |
| "What's a dangling symlink?" | 13 Q5 / 8 Example |
| "Why no hard-linked directories?" | 13 Q6 / 4 Alternative |
| "What is inode exhaustion?" | 13 Q8 / 16 Industry |
| "stat vs lstat?" | 13 Q7 / 9 Internal |
