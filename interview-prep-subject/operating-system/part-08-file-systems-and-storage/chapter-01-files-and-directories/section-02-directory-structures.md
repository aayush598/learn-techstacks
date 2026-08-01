# Directory Structures

> **TL;DR**: A directory is itself a special file whose entries map **names → inode numbers**; organization evolved from a single flat list to **two-level** (per-user), **tree** (hierarchical paths), and **acyclic-graph** (hard links + symlinks) structures — with the tree being what every modern OS uses.

## 1. Why Does This Exist?
A flat namespace ("all files in one list") breaks down as file counts grow: name collisions across users, no grouping, slow lookups. Directories exist to give the namespace *structure* — a hierarchy that lets users organize files, avoid collisions, share subtrees, and resolve names incrementally. They also answer "where do I look for a file?" — the directory is the *naming* mechanism, separate from the *storage* mechanism (inodes/data blocks, Chapter 02). Every pathname resolution is a sequence of directory lookups, so directory design directly affects performance and features (links, mount points).

## 2. How Does It Work?
A directory is a file whose data is a sequence of entries: `(name → inode number, type, length)`. Lookup = linear scan or hash of a name → inode → follow it.
- **Single-level**: one directory for everything (early micros, DOS `\`).
- **Two-level**: a directory per user; lookup is `(user, name)`.
- **Tree**: nested directories → absolute paths (`/a/b/c`); relative paths from cwd; efficient grouping; this is the standard.
- **Acyclic graph (tree + links)**: hard links (two names → same inode, link count) and symbolic links (a special file containing a path) allow sharing subtrees without cycles in the hard-link sense.
- **General graph (rejected)**: cycles — modern FS prohibit hard links to directories (except via mount bind or special cases) to keep `find`/gc and `rm` sane.

## 3. When Is It Used?
- **Every Unix/Linux/Windows/macOS install**: tree with `/`, `C:\`, etc.; per-user home trees.
- **Links**: `ln` (hard), `ln -s` (symbolic); `~`, `.`, `..`, relative paths; symlinks used by package managers (`/usr/bin/node` → versioned path), runtime libs (`libc.so → libc.so.6`).
- **Mount points**: directories are the attach points for filesystems (VFS, Chapter 04 Sec 04).
- **Pseudo-dirs**: `/proc/<pid>`, `/sys` — directories exposing kernel state.

## 4. Why Wasn't Another Approach Chosen?
- **Single-level**: too collision-prone, no grouping — fine for 10 files, useless at scale. Rejected.
- **Two-level**: per-user separation but no sub-organization — a compromise before trees. Superseded.
- **Tree**: hierarchical names, arbitrary depth — chosen everywhere; path length and lookup are the cost (mitigated by dcache).
- **Acyclic graph**: needed for sharing/aliasing → links; but hard-link cycles are impossible for dirs (kernel enforces), and symlinks introduce dangling targets (a feature).
- **Database-like object stores**: S3 flat key space with `/` in keys is *semantically* a tree emulated by convention — cloud object stores show the trade-off (flat = scalable, hierarchical = convenient).

## 5. Intuition
A directory is a **card catalog**: each card maps a book title to a call number (inode). The library doesn't store the catalog only as one giant box — it organizes by floors and aisles (tree of directories) so "find the book on operating systems" means walking aisle by aisle. The card itself is lightweight (name→number); the *book* (data blocks) lives elsewhere. Links are like two catalog cards pointing to the same physical book.

## 6. Real-World Analogy
A **company's org chart**: the CEO directory contains the CTO directory, which contains the "platform" directory, which contains "docs". `aayush/reports/q3.md` is "go to aayush's office, look in the reports folder, pull the q3 binder." A hard link = two departments' charts pointing at the same physical binder (two names, one binder). A symlink = a sticky note on the wall reading "see the binder in aayush's office" — the note itself is a tiny file with a path.

## 7. Formal Definition
A **directory** is a special file containing a set of entries, each mapping a component name to an inode (or file identifier) plus type and length information. Directory structures range from a **single-level** table to **two-level** (per-user) and **tree-structured** directories (hierarchical, with absolute and relative pathname resolution). **Acyclic-graph** structures extend the tree by allowing sharing via **hard links** (multiple directory entries referencing the same inode; the inode's link count tracks references) and **symbolic links** (a small file whose contents are a pathname, resolved by the OS at lookup, which may dangle). General cyclic graphs are typically prohibited to preserve well-defined traversal and deletion semantics.

## 8. Example
A tree directory:
```
/ (root)
├── home/aayush/
│   ├── docs/ (dir)
│   │   └── resume.pdf → inode 5823
│   └── scripts/
└── usr/lib/
    ├── libc.so.6 → inode 9144
    └── libc.so → SYMLINK to "libc.so.6"
```
- Resolve `/home/aayush/docs/resume.pdf`: read `/`'s entries → `home` → inode; read home → `aayush` → inode; read aayush → `docs`; read docs → `resume.pdf → 5823`. Five directory reads (dcache makes them O(1) after warmup).
- Hard link: `ln docs/resume.pdf docs/cv.pdf` → inode 5823 link count 2; both names work; deleting one leaves the other.
- Symlink: `ln -s /usr/lib/libc.so.6 /tmp/mylib` → a file whose data is the string `/usr/lib/libc.so.6`; opening `/tmp/mylib` follows it (unless `open(O_NOFOLLOW)`).
- `..` in each dir points to the parent inode — relative navigation.

## 9. Internal Working
1. **Path walk** (`fs/namei.c`): start at the root inode (absolute) or cwd (relative); for each component, read the current directory's data (or hash lookup), match the name, get the child inode.
2. **Permission check**: `x` (execute) on each directory along the path — that's what "execute" means for directories.
3. **dcache**: `dentry` cache maps (parent inode, name) → dentry/inode — most lookups never touch disk.
4. **Links**: hard link = add an entry + bump inode link count (no data copy). Symlink = create a small file containing the target path; resolution re-walks it (loop-guarded: `ELOOP`).
5. **Delete**: remove entry, decrement link count; free when 0 (Chapter 01 Sec 01).
6. **Hashed directories**: ext4 uses htree (indexed) for large dirs — O(1) lookup instead of linear.

## 10. Time Complexity
- Linear directory lookup: O(n) entries.
- Hashed/htree directory (ext4): O(1) average.
- Path resolution: O(path length × per-component lookup); dcache makes it O(1) amortized per component.
- Hard link creation: O(1) (entry + link count).
- Symlink resolution: O(target path length) + loop detection O(1) counter.
- Tree search (e.g., `find`): O(total entries).

## 11. Advantages
- **Hierarchy** = organization, collision-freedom, and per-user/per-project separation.
- **Relative/absolute paths** + cwd make names convenient.
- **Hard links**: share a file without copying (link count semantics).
- **Symlinks**: flexible aliasing, cross-filesystem, versioned targets.
- Directory-as-file means **uniform operations** (open/read) apply; permissions per component.
- htree/hash makes large directories fast.

## 12. Disadvantages
- **Deep paths** cost lookups (mitigated by dcache).
- **Links complicate semantics**: symlink loops (ELOOP), dangling links, hard-link count bugs, permissions ambiguity (`chown` on a symlink vs target).
- **Hard links can't cross filesystems** (inode numbers differ); only symlinks can.
- **Acyclic-graph** shares can confuse backup/GC tools (double-counting).
- General-graph cycles are impossible for dirs → limits some sharing models (bind mounts work around this).

## 13. Interview Questions
1. **Q: What is a directory, really?** A: A special file whose data is a list of `name → inode` entries (plus type/length) — it's naming metadata, not file content.
2. **Q: Name the directory structures and their trade-offs.** A: Single-level (flat, collisions), two-level (per-user, no sub-org), tree (hierarchical, standard), acyclic graph (tree + links for sharing), general graph (cycles — disallowed for dirs).
3. **Q: How does `ln` differ from `ln -s`?** A: `ln` = hard link: another directory entry for the same inode (link count++), no copy, must be on the same FS. `ln -s` = symlink: a separate tiny file containing a path; cross-FS allowed; can dangle.
4. **Q: Why can't hard links cross filesystems? (Tricky)** A: A hard link is a second name for a specific inode; inode numbers are only meaningful within one filesystem — there's no way to point a directory entry in FS-A at an inode in FS-B.
5. **Q: What is a dangling symlink and why is it a feature?** A: A symlink whose target doesn't exist — legal, letting you point at files that may appear later (or be moved); tools detect it with `readlink`/`-L` checks.
6. **Q: What does 'x' (execute) permission mean for a directory?** A: Permission to traverse it (use it as a path component). To read names you need 'r'; to list+stat you need both 'r' and 'x'; to create/delete entries, 'w'+'x'.
7. **Q: How do `find` and `rm` deal with symlink loops?** A: `find` uses `-H/-L/-P` and tracks visited inodes/devices to avoid infinite loops; the kernel limits symlink chains with `MAXSYMLINKS`/`ELOOP`; `rm` doesn't follow symlinks by default.
8. **Q: What happens when you `mv` a directory that's someone's cwd?** A: It still works — processes hold inode references; absolute paths from the new location change but the inode is the same (this is why tools use `openat`/relative fds).
9. **Q: How does the kernel resolve `/usr/bin/python3`?** A: Walk root → usr → bin (dirs), reading each directory's entries (dcache-cached), then read the `python3` entry → inode → check permissions → open. If `python3` is a symlink, it re-resolves the target path.
10. **Q: What is a mount point?** A: A directory where a second filesystem is attached; the VFS switches resolution to the mounted FS's root at that directory (the old directory contents are hidden until unmount).
11. **Q: Why do modern filesystems hash large directories?** A: A linear directory makes lookup O(n) — thousands of files = slow. ext4's htree uses a balanced tree of hashed names → O(1) average lookup at scale.
12. **Q: What is the '.' and '..' semantic?** A: '.' = the directory itself, '..' = its parent — both are real entries (hard links to dirs) in many FS; the kernel resolves them during path walk.

## 14. Follow-Up Questions
1. **Q: What's the difference between absolute, relative, and canonical paths?** A: Absolute = from root (`/a`); relative = from cwd (`../a`); canonical = fully resolved, no `..`/symlinks (`realpath`).
2. **Q: How does the dcache speed directory operations?** A: Dentry cache maps (parent, name) → inode, so repeated path components never touch disk — massive for hot paths.
3. **Q: What is an `openat`/`*at` syscall for?** A: Resolves relative to a given directory FD — safe against cwd races (TOCTOU) and per-thread cwd emulation.
4. **Q: What is a bind mount?** A: Mounting the same tree at another location — effectively a directory hard link across the namespace (the modern answer to sharing subtrees without cycles).

## 15. Coding Example
```c
// Demonstrate directory iteration, hard links, and symlinks
#include <stdio.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>

int main(void) {
    mkdir("/tmp/dirdemo", 0755);

    // hard link: two names, one inode
    FILE *f = fopen("/tmp/dirdemo/a.txt", "w"); fclose(f);
    link("/tmp/dirdemo/a.txt", "/tmp/dirdemo/b.txt");      // link count -> 2
    // symlink
    symlink("/tmp/dirdemo/a.txt", "/tmp/dirdemo/c-link");

    struct stat st;
    stat("/tmp/dirdemo/a.txt", &st);
    printf("a.txt links=%ld\n", (long)st.st_nlink);         // 2
    lstat("/tmp/dirdemo/c-link", &st);
    printf("c-link is a symlink? %s\n",
           S_ISLNK(st.st_mode) ? "yes" : "no");

    // iterate the directory
    DIR *d = opendir("/tmp/dirdemo");
    struct dirent *e;
    while ((e = readdir(d)))
        printf("entry: %s\n", e->d_name);
    closedir(d);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: VFS `fs/namei.c` (path walk), `fs/dcache.c` (dcache), `fs/ext4/namei.c` (htree), `fs/proc` (pseudo-directories), mount table in `fs/namespace.c`.
- **Windows**: NTFS B-tree directory indexes; `C:\Users\...` trees; junctions/symlinks (`mklink`).
- **macOS/APFS**: B-tree directories, `Firmlinks`.
- **Object stores**: S3/GCS use a flat key space with `/` convention — directories are an app-level fiction (a lesson in the flat-vs-tree trade-off at scale).

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 11.3 "Directory Structure".
- Tanenbaum, *Modern Operating Systems*, Ch. 4.1.4-4.1.5.
- Linux source: `fs/namei.c`, `fs/dcache.c`, `fs/ext4/namei.c`.
- `man 2 link`, `man 2 symlink`, `man 3 opendir`, `man 7 path_resolution`.

## 18. Cheat Sheet
- Directory = file of `name → inode` entries.
- Structures: single → two-level → tree (standard) → acyclic graph (+links).
- Hard link: same inode, link count++; same-FS only.
- Symlink: tiny file holding a path; cross-FS; can dangle.
- Dirs need 'x' to traverse, 'r' to list, 'w' to modify entries.
- dcache caches dentries — path lookups are O(1) amortized.
- htree (ext4) = hashed balanced tree for large dirs.
- '..' and '.' are real entries; cycles prohibited.
- Mount points attach filesystems at directories.
- object stores: flat keys with '/' convention.

## 19. Quiz
1. A directory stores:
   a) file contents b) name→inode entries c) disk blocks d) permissions → **b**
2. The standard modern directory structure is:
   a) single-level b) tree c) two-level d) graph → **b**
3. A hard link:
   a) copies data b) adds an entry for the same inode c) needs a path d) crosses FS → **b**
4. Hard links can't cross filesystems because:
   a) policy b) inode numbers are FS-local c) too slow d) permissions → **b**
5. To traverse a directory you need:
   a) r b) w c) x d) rwx → **c**
6. ext4's large-directory optimization is:
   a) linear scan b) htree (hashed tree) c) B-tree only d) none → **b**

## 20. Flashcards
- **Q: What is a directory?** → **A:** A special file mapping names → inodes.
- **Q: Hard vs sym link?** → **A:** Hard = extra name for the same inode (same FS); sym = path-containing file (cross-FS, dangling OK).
- **Q: Why can't hard links cross FS?** → **A:** Inode numbers are only meaningful within one filesystem.
- **Q: What does 'x' on a dir mean?** → **A:** Permission to traverse it.
- **Q: What's the dcache?** → **A:** Dentry cache making path lookups O(1) amortized.
- **Q: How do large dirs stay fast?** → **A:** Hashed balanced trees (ext4 htree).

## 21. Revision
Directories are files whose entries map names to inodes. Structure evolved from flat single-level (collisions) through two-level (per-user) to the tree every modern OS uses, extended by links into an acyclic graph: hard links are extra names for the same inode (link count, same-FS only), while symlinks are tiny path-files (cross-FS, dangling). Path resolution walks components (dcache-cached, O(1) amortized), dirs need 'x' to traverse, and large dirs use hashed trees. Mount points attach filesystems at directories, and object stores emulate directories as flat keys — the endpoint of the flat-vs-tree trade-off.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a directory?" | 2 How / 7 Formal |
| "Directory structure designs?" | 8 Example / 13 Q2 |
| "Hard vs symlink?" | 13 Q3 / 8 Example |
| "Why no cross-FS hard links?" | 13 Q4 / 12 Disadvantages |
| "What does x mean on dirs?" | 13 Q6 / 9 Internal |
| "How does the kernel resolve a path?" | 13 Q9 / 9 Internal |
| "How do large directories stay fast?" | 13 Q11 / 16 Industry |
