# Copy-on-Write and Memory-Mapped Files

> **TL;DR**: **Copy-on-write (COW)** makes `fork()` O(page tables) instead of O(memory) by sharing frames read-only and copying only on first write; **memory-mapped files** (`mmap`) make file I/O lazy and page-cache-backed, unifying files and memory.

## 1. Why Does This Exist?
- **COW exists** because `fork()` copying the entire parent address space was brutal (a 2 GB process forks in seconds of pure copy; then most children immediately `exec`, discarding it). COW shares all frames read-only and copies a page only when either process writes it — so `fork` is nearly free, `exec` discards shared pages without ever copying, and memory usage stays proportional to *differences*, not totals.
- **`mmap` exists** because `read()`/`write()` force userspace↔kernel copies and eager scheduling; mapping a file into the address space lets the page cache serve bytes lazily (demand paging, Part 07 Sec 02), eliminates the copy for reads, enables shared writable files between processes, and is exactly how the loader runs executables and shared libraries.

## 2. How Does It Work?
**COW (`fork`):**
1. Kernel clones the parent's `mm_struct` + page tables for the child.
2. All user frames are *shared*: PTEs marked read-only (RW cleared) in both, with `_PAGE_COW` tracking.
3. Either process writes → #PF (protection violation) → `do_wp_page`: if `page_count > 1` (shared), allocate a new frame, copy the data, install a private RW PTE; if only one owner, just set RW.
**`mmap`:**
1. `mmap(file, ...)` → kernel inserts a file-backed VMA and fills PTEs as **not-present** (or "restartable" for `MAP_POPULATE`).
2. On read → fault → `filemap_fault`: page cache lookup; miss → `readpage` from disk → insert into page cache + PTE.
3. Writes go straight to the page (dirty bit set); the kernel writes back to the file on eviction/`msync`/`writeback` (`MAP_SHARED`), or keeps a private copy for `MAP_PRIVATE`.

## 3. When Is It Used?
- **COW**: every `fork()` on Linux (it's mandatory); also `madvise(MADV_DONTNEED)`/KSM dedup; hypervisor memory dedup; and (in concept) every "snapshot" system (ZFS, btrfs snapshots, Postgres MVCC) that shares read-only pages and copies on write.
- **mmap**: loading executables/libraries (`execve`); `malloc`/`calloc` (anonymous); shared memory (Part 09 Sec 04); databases (SQLite, LMDB, Postgres's `mmap` paths); search/ML index loading (mmap a huge index and let OS page it); JVMs and language runtimes.

## 4. Why Wasn't Another Approach Chosen?
- **Full copy on fork (rejected)**: O(address space); wasteful given exec; `vfork` was the old hack (share everything, no protection — dangerous); COW is the safe refinement.
- **Shared everything (no COW)**: what would processes do — both writing the same memory? Chaos. COW gives private-writable semantics cheaply.
- **read()/write() for files (still used)**: copies data through the page cache; fine for streaming but wasteful for random access and sharing. mmap wins for shared/existing pages.
- **Mmap for everything (rejected)**: latency (fault-based) and page-granularity I/O are poor for small/streaming transfers; `read`/`write` + sendfile remain for I/O-heavy paths.
- **Direct disk address mapping (no page cache)**: no sharing/caching; only for specific devices (O_DIRECT).

## 5. Intuition
**COW**: A library photocopies one master textbook and says "borrow it; if you underline a page, we'll print your own copy of just that page." Reading costs nothing; personalizing costs one page. That's fork+COW.

**mmap**: A warehouse (disk) lets you keep an index card (VMA) promising "we have box 42." You don't take the box until you need it; when you do, it's brought to the loading dock (page cache) and you read directly from the dock instead of copying it into your own box first.

## 6. Real-World Analogy
- **COW = a legal document** you and a co-signer both reference. Neither of you may alter the original; the moment one of you wants changes, the notary prints a private copy with the edits — only that one page is re-printed.
- **mmap = a museum audiobook**: the museum streams each exhibit's narration when you approach (on demand), caching the last few narrations; you never "download" the whole museum.

## 7. Formal Definition
**Copy-on-write** is a memory-sharing optimization in which multiple processes (or pages) share the same physical frames with read-only PTEs; a write to a shared page triggers a page fault that clones the frame and makes the writer's PTE read/write, so the cost of copying is deferred to (and bounded by) actual modifications. **Memory-mapped I/O (`mmap`)** is a system call that places a file's contents (or anonymous memory) into a process's virtual address space; pages are loaded lazily through the page cache, and modifications are either written back to the file (MAP_SHARED) or confined to the process (MAP_PRIVATE). Both exploit the demand-paging fault path.

## 8. Example
**COW:** Parent P has a 1 GB anonymous mapping, all pages resident.
- `fork()` → child C inherits page tables; every PTE cleared RW, `_PAGE_COW` set; frames shared. Cost: table clone (~µs) + `pte` changes. Resident frames unchanged: 1 GB total (shared).
- C writes byte at page 42 → #PF → `do_wp_page` → copy 4 KB page 42 into a new frame → C's PTE[42] = RW private. Now resident = 1 GB + 4 KB.
- If C instead `exec("ls")`, the shared 1 GB is simply dropped (refcounts) — never copied. That's why `fork` + `exec` is the standard launch pattern.

**mmap:** File `data.bin` (64 MB).
- `fd = open; ptr = mmap(ptr, 64MB, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);`
- Read `ptr[0x1000]` → fault → page cache reads 4 KB from offset 0x1000 → resident 4 KB.
- Write `ptr[0x1000] = 7` → dirty. Later, `msync`/writeback → file updated.
- Second process `mmap`s the same file → its PTEs point at the *same* page-cache frames — shared state with no userspace coordination.

## 9. Internal Working
**COW path (`do_wp_page`):**
1. Write fault on RW=0 PTE → `handle_pte_fault` sees `pte_dirty`/`_PAGE_COW`.
2. Check `page_count(page)`:
   - 1 → the page is exclusively owned → just set RW, done (fast).
   - >1 → shared → `alloc_page` new frame, copy 4 KB, `page_add_new_anon_rmap`, install new PTE (RW), decrement old page's refcount, flush TLB entry.
3. Return → retry write instruction.
**mmap path (`filemap_fault`):**
1. Fault on file-backed PTE → look up `(inode, offset)` in the page cache (`radix_tree`/`xa_tree`).
2. Hit → map the existing page, install PTE (RW as per VMA).
3. Miss → `read_folio` → submit I/O (readahead may issue 64 KB) → page in cache → install PTE.
4. Eviction: clean file page → drop; dirty file page → `writeback` to disk; MAP_PRIVATE dirty → stays as anonymous copy.
5. `msync(MS_SYNC)` forces writeback; `munmap` flushes TLB and decrements refs.

## 10. Time Complexity
- `fork` with COW: **O(page tables)** (walk+clone+mark RW=0), not O(memory). For a 1 GB process ≈ thousands of PTE writes (~1–5 ms) vs O(GB) copy (seconds).
- First write to a shared page: O(1) copy (4 KB) + fault overhead (~µs).
- mmap read of a fresh page: O(1) page cache op + **O(I/O)**; readahead amortizes.
- mmap random access: O(1) per page after first fault (no syscall per byte — the win over read()).
- COW fork + exec: O(page tables) then O(drop) — typically microseconds total for launch.

## 11. Advantages
- **COW**: fork is cheap, exec-friendly, memory ∝ differences; enables checkpointing/snapshot tooling (madvise, CRIU, ZFS-style snapshots).
- **mmap**: zero-copy reads (page cache shared), lazy I/O, random-access friendly (no syscall per byte), cross-process shared files, clean model for huge files (sparse, partial).
- Both integrate with the existing fault/TLB machinery — no new abstractions.
- `MAP_PRIVATE` gives "copy of file on write" semantics for config/overlay use.
- Loader uses mmap so libraries share physical pages across processes.

## 12. Disadvantages
- **COW**: read-only PTEs add fault overhead on first writes; a write-heavy fork (parent+child both modifying) pays copy cost anyway; page-table clone still O(tables).
- **mmap**: page-granular I/O is poor for small random writes; fault latency; page cache double-buffers with userspace buffers; `MAP_SHARED` writes are only visible after writeback unless `msync`; memory-mapping huge files can exhaust address space; SIGBUS on truncated files.
- Both add kernel complexity and subtle SMP races.
- COW + fork in threaded/multithreaded apps can be slower than `posix_spawn`/`vfork`+exec (clone).

## 13. Interview Questions
1. **Q: What is copy-on-write?** A: Sharing frames read-only after `fork`; a write faults and clones the page, so copy cost is paid only for modified pages.
2. **Q: Why does `fork()` + `exec()` work so well with COW?** A: fork clones tables (cheap); exec discards the shared pages (never copied) — a 2 GB process can fork+exec in microseconds of actual copying.
3. **Q: What exactly happens on the first write after fork?** A: Write to RW=0 PTE → protection fault → `do_wp_page`: if the page is shared (`page_count>1`), copy it, install a private RW PTE; else just set RW.
4. **Q: How does the kernel know a page is shared? (Tricky)** A: `page_count(page) > 1` (refcount includes all mappings + page cache). If 1, no copy needed; if >1, clone.
5. **Q: What is the difference between MAP_SHARED and MAP_PRIVATE?** A: SHARED: writes go to the page cache and writeback to the file — visible to other mappers. PRIVATE: copy-on-write — writes never touch the file (fresh copy per process).
6. **Q: How does `mmap` read a file?** A: Fault on the file-backed VMA → `filemap_fault` → page cache lookup → `readpage` on miss → PTE installed; reads then bypass syscalls (direct memory access).
7. **Q: When would you choose `read()` over `mmap`? (Production)** A: Small/streaming I/O (mmap faults + page granularity hurt), or when you need explicit control over buffering; mmap wins for random access, sharing, and large files.
8. **Q: What happens if a mapped file is truncated while mapped?** A: Accessing the truncated region faults with **SIGBUS** (the VMA says the range exists but the file doesn't back it) — a classic mmap pitfall.
9. **Q: How is `calloc`/`malloc` implemented with mmap?** A: `mmap(MAP_ANONYMOUS)` creates a VMA backed by the shared zero page; first write COW-faults to a real frame — so `calloc(1GB)` costs ~nothing until used.
10. **Q: What does `msync` do?** A: Flushes dirty pages of a MAP_SHARED mapping to the file synchronously (`MS_SYNC`), asynchronously (`MS_ASYNC`), or invalidates (`MS_INVALIDATE`); without it, writeback is lazy.
11. **Q: Can COW be used outside fork? (Scenario)** A: Yes — `madvise(MADV_DONTNEED)`, KSM (merging identical anonymous pages), hypervisor dedup, and filesystems' snapshot/overlay designs reuse it; even `mmap` MAP_PRIVATE uses COW per page.
12. **Q: What's the memory accounting gotcha with COW?** A: "Resident" RSS after fork counts the *shared* frames once for the group; per-process PSS splits shared pages proportionally — tools use RSS vs PSS/Swap vs USS to reason about it.
13. **Q: Why does `mmap` make shared libraries cheap?** A: The loader maps libc's text once into the page cache; every process's PTEs point at the same frames → one physical copy for N processes.
14. **Q: What's the downside of mmap for a database? (Production)** A: Page-cache double-buffering, no control over writeback timing (unless msync/fsync), crash-consistency issues → many DBs (Postgres) prefer their own buffered I/O; embedded DBs (SQLite/LMDB) embrace mmap.

## 14. Follow-Up Questions
1. **Q: What is `madvise` and when is it useful?** A: Hints to the kernel: `MADV_RANDOM` (no readahead), `MADV_SEQUENTIAL`, `MADV_DONTNEED` (drop pages), `MADV_FREE` (lazy free) — improves fault behavior for specific access patterns.
2. **Q: What is the Linux "page cache" vs "buffer cache"?** A: Same thing on modern Linux — the page cache (`address_space`) backs file pages; the old "buffer cache" merged into it.
3. **Q: How does KSM work?** A: The kernel scans for identical anonymous pages and merges them via COW — the same mechanism, used for VM dedup (cloud savings).
4. **Q: How do ZFS/btrfs "snapshots" relate to COW?** A: Snapshots share unchanged blocks read-only; on write, the filesystem copies the block (COW) — the same principle at the block level.

## 15. Coding Example
```c
// Demonstrate MAP_SHARED vs MAP_PRIVATE + msync; and COW via fork
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
    // --- mmap: shared file-backed mapping ---
    int fd = open("/tmp/mapdemo.bin", O_RDWR|O_CREAT, 0644);
    ftruncate(fd, 4096);
    char *shared = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    strcpy(shared, "hello shared file");
    msync(shared, 4096, MS_SYNC);   // now durable
    munmap(shared, 4096);

    // --- MAP_PRIVATE: writes don't reach the file ---
    char *priv = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE, fd, 0);
    strcpy(priv, "private change");
    munmap(priv, 4096);
    // /tmp/mapdemo.bin still contains "hello shared file"

    // --- COW: fork, write in child ---
    char *mem = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);
    strcpy(mem, "original");
    pid_t pid = fork();
    if (pid == 0) { strcpy(mem, "child wrote"); _exit(0); }  // COW copy (MAP_SHARED still shared)
    wait(NULL);
    printf("parent sees: %s\n", mem);   // "child wrote" for MAP_SHARED
    munmap(mem, 4096); close(fd);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `kernel/fork.c` (COW setup), `mm/memory.c` (`do_wp_page`), `mm/filemap.c` (`filemap_fault`), `mm/ksm.c`, `mm/madvise.c`; loader `fs/binfmt_elf.c` uses mmap.
- **Windows**: `MapViewOfFile`/`CreateFileMapping` (mmap equivalent); fork-less but COW via `NtMapViewOfSection` for section sharing.
- **macOS**: `mmap` + `vm_copy`; XNU fault handler.
- **Databases**: SQLite `mmap` mode; LMDB (memory-mapped B-tree); Postgres uses `read`/`write` + `posix_fadvise`; RocksDB mmap for indexes.
- **Big data**: Spark/DuckDB memory-map parquet/Arrow files for zero-copy column reads; search engines (Elasticsearch) mmap indices.
- **Runtimes**: JVM uses mmap for class files + THP; Go `syscall.Mmap`; JITs use mprotect guard pages.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.3 "Copy-on-Write", Ch. 9.6 "Memory-Mapped Files".
- Linux source: `mm/memory.c`, `mm/filemap.c`, `mm/ksm.c`, `fs/binfmt_elf.c`.
- `man 2 mmap`, `man 2 msync`, `man 2 madvise`, `man 2 fork`.
- Gorman, *Understanding the Linux Virtual Memory Manager*.
- The "Hacking Linux mmap" series, linux-mm.org.

## 18. Cheat Sheet
- COW: fork shares frames read-only; write → fault → clone → RW.
- `page_count==1` ⇒ no copy (just set RW); `>1` ⇒ clone.
- fork+exec: tables cloned, pages dropped — nearly free.
- mmap: file pages served from page cache; lazy (fault) I/O.
- MAP_SHARED: writes→file (need msync); MAP_PRIVATE: COW, file untouched.
- mmap reads: no syscalls per byte — the big win.
- Truncated mmap file → SIGBUS on touch.
- calloc = anon mmap + zero page + COW on first write.
- Page cache keyed by (inode, offset); PTEs point to its pages.
- RSS counts shared frames per-group; PSS splits proportionally.

## 19. Quiz
1. After fork, parent and child share frames with:
   a) RW PTEs b) read-only PTEs c) present=0 d) separate copies → **b**
2. On first write to a shared page:
   a) SIGSEGV b) COW clones the page c) nothing d) swap-in → **b**
3. MAP_SHARED writes eventually reach the file via:
   a) never b) writeback/msync c) copy d) TLB flush → **b**
4. `calloc(1 GB)` initially maps:
   a) 1 GB frames b) the shared zero page c) swap d) SIGBUS → **b**
5. Truncating a mapped file causes:
   a) SIGSEGV b) SIGBUS c) ENOSPC d) nothing → **b**
6. mmap random reads avoid per-byte:
   a) page faults b) syscalls c) cache misses d) writes → **b**

## 20. Flashcards
- **Q: What is COW?** → **A:** Share read-only; clone a page on first write via fault.
- **Q: Why is fork cheap?** → **A:** Clones page tables, not memory; exec drops the shared pages.
- **Q: MAP_SHARED vs MAP_PRIVATE?** → **A:** Shared→file-backed writes; private→COW, file untouched.
- **Q: How does mmap read a file?** → **A:** Fault → page cache (`filemap_fault`) → no syscalls after.
- **Q: What raises SIGBUS on a mapped file?** → **A:** Accessing beyond a truncated file's actual size.
- **Q: What does msync do?** → **A:** Forces writeback of dirty MAP_SHARED pages to disk.
- **Q: How is calloc lazy?** → **A:** Anon mmap + shared zero page; COW materializes on write.

## 21. Revision
COW lets `fork()` share the parent's frames read-only and clone a page only on first write (`do_wp_page`, gated by `page_count`), making fork+exec nearly free and memory proportional to *differences*. `mmap` maps files/anonymous memory into the address space, serving pages lazily through the page cache (`filemap_fault`) — no syscall per byte for reads, MAP_SHARED gives cross-process file sharing, MAP_PRIVATE gives per-page COW. `calloc` is anon-mmap on the shared zero page; truncated files SIGBUS; `msync` forces writeback. Together these are the load-bearing abstractions behind loading, malloc, shared memory, snapshots, and databases.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How does fork use COW?" | 2 How / 9 Internal |
| "What happens on first write after fork?" | 9 Internal / 13 Q3 |
| "How does the kernel detect sharing?" | 13 Q4 / 9 Internal |
| "MAP_SHARED vs MAP_PRIVATE?" | 13 Q5 / 2 How |
| "Why mmap over read()?" | 13 Q7 / 4 Alternative |
| "What causes SIGBUS?" | 13 Q8 / 12 Disadvantages |
| "Why is calloc cheap?" | 13 Q9 / 8 Example |
