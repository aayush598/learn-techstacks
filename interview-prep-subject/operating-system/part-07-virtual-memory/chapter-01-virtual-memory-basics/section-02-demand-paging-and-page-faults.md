# Demand Paging and Page Faults

> **TL;DR**: **Demand paging** loads a page into RAM only on first reference; a **page fault** is the hardware→kernel trap that makes that possible — the fault handler validates the address against VMAs, brings the page in (zero-fill, file, or swap), installs the PTE, and resumes the faulting instruction.

## 1. Why Does This Exist?
Loading every page of a program at startup wastes memory and time: most pages are never touched (rare error paths, unused libraries, sparse arrays). Demand paging exists to postpone I/O until it's strictly needed — each page is materialized on its first reference. This makes programs start in milliseconds regardless of size, keeps RAM devoted to *used* pages, and turns "load the whole process" (Part 06) into "load the working set" (Part 07). The page fault is the enabling mechanism: without a hardware trap on non-present pages, the OS couldn't know when to load what.

## 2. How Does It Work?
A page is "logically present" but "physically absent" when its PTE has `present=0` yet a VMA covers it. On access:
1. MMU walk finds present=0 (or a permission mismatch) → raises **#PF** with the faulting address (CR2 on x86) and an error code.
2. CPU traps to kernel → `do_page_fault` → `find_vma` validates the address.
3. Three outcomes:
   - **No VMA** → invalid → SIGSEGV.
   - **Permission violation** → SIGSEGV (or a *special* case: COW/guard pages, Part 07 Sec 03).
   - **Valid, not present** → allocate a frame, populate it from: **zero page** (anonymous fresh), **file** (file-backed via the page cache), or **swap** (evicted anonymous page), then `set_pte` present and retry.
4. Return from exception → the instruction re-executes → TLB walk now hits the present PTE.

## 3. When Is It Used?
- **Every process start**: `execve` maps the binary with not-present PTEs; only touched pages fault in (code pages, data, stack).
- **Every `mmap`ed file**: pages fault in on read; dirty pages write back on eviction (`mmap` I/O).
- **Heap growth**: `malloc`/`brk` extends the heap VMA; pages are zero-filled on first touch (lazy commit).
- **Stack growth**: guard-page faults grow the stack downward on demand.
- **Anonymous memory**: `calloc` (which is `mmap(MAP_ANONYMOUS)`) — pages are shared zero-frames until written.

## 4. Why Wasn't Another Approach Chosen?
- **Eager loading (prepaging)**: at startup, load everything. Wasteful (rare paths) but deterministic; used in some real-time/predictive systems where you *know* the working set in advance (and in database prefetching).
- **Software-only paging (no MMU)**: impossible without a trap on absent pages.
- **Whole-process demand (swapping, Part 06 Sec 03)**: coarser; a single fault loads *everything* (huge I/O); per-page demand is fine-grained and cheap.
- **Zero-fill shared pages**: Linux shares one read-only zero page across all fresh anonymous mappings until first write (COW) — a demand-paging optimization.
- **Readahead (chosen as a *complement*)**: the kernel also prefetches neighboring pages (`readahead`/`fault-around`) to amortize faults on sequential access — demand paging alone would pay per-page latency on streaming.

## 5. Intuition
You rent an apartment where every item of furniture is ordered online on the day you first need it. The catalog (VMA) says the item exists and where it is; the order form (PTE) says "not delivered yet." First time you sit down (touch), you get a delivery notice (page fault); the system fetches it (I/O) and installs it (PTE present); next time you sit, it's there. For a 200-item house, you pay delivery only for the ~30 items you actually use — demand paging.

## 6. Real-World Analogy
A streaming platform buffers only what you watch: opening a movie doesn't download all episodes (eager), nor the whole library (swapping); the player requests each segment on demand (demand paging), and the buffer size limits what's resident (frames). If you skip around, each skip is a new fetch (fault). A prefetching player reads ahead (readahead) so watching straight through is smooth.

## 7. Formal Definition
**Demand paging** is a virtual-memory policy in which a page is brought into physical memory only when a reference to it causes a page fault; pages are marked not-present in their PTEs until that moment. A **page fault** is an exception raised by the MMU on an access to a not-present page or on a permission violation; the operating system's fault handler either resolves the fault (by allocating and loading a frame, or by applying copy-on-write/guard-page semantics) or terminates the process with SIGSEGV if the access is invalid. The average time to access memory under demand paging is `EAT = (1 − p)·t_mem + p·t_fault`, where p is the fault rate.

## 8. Example
32-bit, 4 KB pages. Process maps a file-backed VMA at 0x1000–0x2000 (4 pages). Initially all PTEs not-present.

- `LOAD [0x1234]` → page 0x1 → fault (CR2=0x1234).
  - `find_vma`: 0x1234 ∈ [0x1000, 0x2000), flags READ|WRITE, file-backed → valid.
  - Allocate frame F1; read 4 KB from the file offset 0x1000−0x1000=0 (file position = VA − VMA start + file offset).
  - PTE[0x1] = (F1, present, rw, file).
  - Return; retry → load succeeds.
- `STORE [0x1ABC]` → page 0x1 already present → no fault, PTE dirty bit set by hardware.
- `LOAD [0x9000]` → no VMA covers → SIGSEGV.

Fault cost: hardware trap (~1–2 µs) + kernel work (~1–5 µs) + disk read (50 µs SSD / 300 µs HDD). If fault rate p=10⁻⁴, EAT = (0.9999)·100ns + 10⁻⁴·100µs ≈ 110 ns — only 10% overhead. At p=10⁻², EAT ≈ 1 µs+ (10×). Fault rate is everything.

## 9. Internal Working
1. **Walk**: TLB miss → 4-level walk → PTE present=0 → #PF, error code encodes r/w, user, reserved, present.
2. **Trap**: CPU saves the instruction context; on x86 the faulting address is in CR2.
3. **Dispatch**: `do_page_fault` (arch) → checks address against `mm` (kernel vs user half, vs `vmalloc` region).
4. **VMA lookup**: `find_vma(mm, addr)` — address in any VMA?
5. **Special paths** (before generic load): `do_wp_page` (COW), `do_anonymous_page` (zero-fill), `do_swap_page` (swap-in), `do_fault`/`filemap_fault` (file).
6. **Frame allocation**: `alloc_page` → maybe reclaim a victim (Chapter 02 algorithms) → eviction: write dirty anon page to swap, dirty file page to disk, else drop.
7. **Populate**: copy from zero page, `readpage` from the file's `address_space` (page cache lookup first), or swap-in.
8. **Install & finish**: `set_pte`, update stats, possibly prefetch neighbors (`fault-around`), return to user mode, retry the faulting instruction.

## 10. Time Complexity
- Fault without I/O (fresh anon page): O(1) kernel work, ~1–5 µs.
- Fault with disk I/O: O(1) + **O(I/O)** — ~50 µs (SSD) to ~10 ms (spinning disk); page fault ≈ 10⁵–10⁶ cycles.
- EAT formula: `(1−p)·mem + p·fault`; linear in p.
- Reading a file sequentially with readahead: ~one I/O per 64+ pages (amortized), not one per page.
- `madvise(MADV_SEQUENTIAL)`/`MADV_RANDOM` let apps bias readahead for accuracy.

## 11. Advantages
- **Lazy I/O**: only used pages cost; startup O(working set) not O(size).
- **Memory efficiency**: resident ∝ working set, not footprint.
- Enables **oversubscription** and **sharing** (multiple processes share file pages).
- Simplifies programming: no overlay management.
- Faults are hook points: COW, guard pages, KSM dedup, swap-in all ride the same path.

## 12. Disadvantages
- **Fault latency**: unpredictable stalls (bad for real-time); disk faults are brutal.
- **Overhead**: trap, walk, VMA lookup, frame reclaim.
- **Complexity**: every eviction must handle clean/dirty/file/swap/anonymous cases.
- **Readahead guessing**: prefetching can waste bandwidth.
- **Thrashing** (Chapter 03): high fault rates collapse throughput.
- Kernel must be careful with `PTE` races on SMP (page-table locks).

## 13. Interview Questions
1. **Q: What is demand paging?** A: The policy of loading a page only on first reference; PTEs are not-present until touched, at which point a fault brings the page in.
2. **Q: What exactly is a page fault?** A: An MMU exception on access to a not-present page (or permission violation); the kernel either resolves it (load/copy) or SIGSEGVs if invalid.
3. **Q: Walk me through a page fault end-to-end.** A: TLB miss → walk → present=0 → #PF → trap → `do_page_fault` → `find_vma` → allocate frame → populate (zero/file/swap) → `set_pte` → retry instruction.
4. **Q: How does the kernel tell a valid fault from an invalid one?** A: `find_vma`: address inside a VMA with matching permissions = valid (demand/COW); outside any VMA or permission mismatch = invalid → SIGSEGV.
5. **Q: Where does the faulting address come from?** A: The CPU records it — CR2 on x86 — and passes it in the error code (plus r/w/user bits) to the handler.
6. **Q: What is the EAT formula?** A: `EAT = (1−p)·access + p·fault_time`. At p=10⁻⁴ over a 100 ns access and 100 µs fault, EAT ≈ 110 ns (10% overhead); p must stay tiny.
7. **Q: What is a minor vs major page fault? (Tricky)** A: Minor = no I/O (page already in RAM/swap cache; just link it); major = requires disk I/O. `time`/`ps` report `minflt`/`majflt` — many minors at startup are normal.
8. **Q: What is readahead and why is it needed?** A: Sequential access would fault per page; the kernel prefetches following pages (fault-around, `page_cache_ra`) to amortize I/O — a demand-paging complement for locality.
9. **Q: How does `calloc` avoid immediate memory allocation?** A: `mmap` anonymous → all PTEs point to a shared zero page; first write faults and copy-on-write materializes a real frame — so a 1 GB `calloc` costs no RAM until written.
10. **Q: Can a page fault occur in kernel mode?** A: Yes — e.g., on `copy_to_user` into a swapped-out user page, or kernel data (vmalloc). The kernel handles it with a fault context (`FAULT_FLAG_KERNEL`); user faults block, kernel paths differ.
11. **Q: What happens if the process is killed during a fault? (Production)** A: The handler must not re-fault or deadlock: Linux uses `FAULT_FLAG_RETRY_NOWAIT`, per-VMA locks, and checks `mmap_lock` state; a SIGSEGV during fault aborts cleanly.
12. **Q: How is a swap-in fault different from a fresh-page fault?** A: Fresh anonymous → zero-fill; swap-in → the page's data is in swap, so the handler reads it from swap (`do_swap_page`) into a new frame and unlinks the swap entry.
13. **Q: How does COW interact with the fault path?** A: A write to a page mapped read-only (fork's COW) is a *protection* fault; `do_wp_page` copies the page, marks both writable, and returns without I/O.
14. **Q: What is the cost if an app faults every access?** A: EAT → fault_time; throughput collapses (thrashing). The fix is replacement quality + memory limits + `madvise` hints (Chapter 02/03).

## 14. Follow-Up Questions
1. **Q: What is `FAULT_FLAG_RETRY_NOWAIT` for?** A: Lets the kernel retry page-table operations under contention without sleeping — prevents deadlock in the fault path.
2. **Q: What's the difference between the page cache and page tables?** A: The page cache holds *file* pages keyed by (inode, offset); page tables map *virtual* → *physical*. A file page can be referenced by many processes' tables simultaneously.
3. **Q: What is `filemap_fault` doing?** A: Looking up the file page in the page cache (via `address_space`), reading it if absent, installing it in the process's PTE — the mmap read path.
4. **Q: How do JITs (V8) use faults?** A: Guard pages and W^X toggles generate deliberate faults for trap-based bounds-checking (e.g., "guard page" memory isolation).

## 15. Coding Example
```c
// Demonstrate lazy zero-filled pages via mmap + count faults using /proc/self/stat
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

static unsigned long read_faults(void) {
    FILE *f = fopen("/proc/self/stat", "r");
    unsigned long maj = 0, min = 0; char s[128]; long ignore;
    if (!f) return 0;
    // fields 9 and 10 of /proc/pid/stat are minor and major faults
    int n = fscanf(f, "%ld %s %c", &ignore, s, (char[1]){0});
    (void)n;
    // simpler: use getrusage
    fclose(f);
    struct rusage ru;
    getrusage(RUSAGE_SELF, &ru);
    min = ru.ru_minflt; maj = ru.ru_majflt;
    printf("minor faults=%lu major faults=%lu\n", min, maj);
    return min;
}

int main(void) {
    size_t n = 256 * 1024 * 1024;                 // 256 MB
    uint8_t *p = mmap(NULL, n, PROT_READ|PROT_WRITE,
                      MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); return 1; }
    printf("after mmap  : "); read_faults();      // ~0 extra faults
    p[0] = 1; p[4096] = 2; p[4095] = 3;           // touch 3 pages
    printf("after touch : "); read_faults();      // ~3 minor faults
    munmap(p, n);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/memory.c` (`handle_mm_fault`, `do_wp_page`, `do_anonymous_page`, `do_swap_page`, `do_fault`), `mm/filemap.c` (`filemap_fault`, readahead), `mm/mmap.c`.
- **Windows**: NT fault handler `MmAccessFault`, working-set manager, mapped sections.
- **macOS/XNU**: `vm_fault`, `vm_pageout`.
- **Databases**: Postgres `shared_buffers` + OS page cache interplay; Oracle leverages double buffering with `DB_BLOCK_SIZE` aligned to page size.
- **Runtimes**: Go's allocator uses mmap; JVM uses `-XX:+UseTransparentHugePages`; JITs use guard pages.
- **Virtualization**: KVM page faults into guest memory; ballooning reclaims frames.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.2 "Demand Paging".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.6.
- Linux source: `mm/memory.c`, `mm/filemap.c`, `arch/x86/mm/fault.c`.
- `man 2 mmap`, `man 2 madvise`, `man 5 proc`.
- Bonwick & Adams, "Magazines and Vmem" — allocation design (related).

## 18. Cheat Sheet
- Demand paging = load on first touch; PTEs not-present until needed.
- #PF: TLB miss → walk → present=0 → trap → handler.
- Valid fault? `find_vma` says yes (VMA + permissions) → load; else SIGSEGV.
- CR2 (x86) holds the faulting address; error code has r/w/user bits.
- Fresh anon → zero-fill; file → page cache; swap → swap-in.
- Minor fault = no I/O; major fault = disk I/O.
- EAT = (1−p)·mem + p·fault; keep p tiny.
- Readahead prefetches neighbors for sequential access.
- COW and guard pages ride the fault path deliberately.

## 19. Quiz
1. Demand paging loads a page:
   a) at exec b) on first reference c) at compile d) never → **b**
2. A faulting address that matches no VMA produces:
   a) demand load b) SIGSEGV c) COW d) swap-in → **b**
3. A "major" page fault means:
   a) no I/O b) I/O to disk c) permission error d) kernel bug → **b**
4. `calloc(1 GB)` initially costs:
   a) 1 GB RAM b) zero frames (shared zero page) c) 1 GB swap d) a SIGSEGV → **b**
5. EAT with p=10⁻⁴, 100 ns mem, 100 µs fault:
   a) 100 ns b) 110 ns c) 1 µs d) 100 µs → **b**
6. Readahead helps:
   a) random access b) sequential access c) swap d) TLB misses → **b**

## 20. Flashcards
- **Q: What is demand paging?** → **A:** Load each page only on first reference; PTE starts not-present.
- **Q: What does the fault handler do first?** → **A:** `find_vma` — is the address in a legal, permission-matching VMA?
- **Q: Fresh anonymous page → ?** → **A:** Shared zero page / zero-fill (no I/O).
- **Q: File-backed page → ?** → **A:** Page cache lookup + `readpage` (filemap_fault).
- **Q: Evicted anonymous page → ?** → **A:** Swap-in via `do_swap_page`.
- **Q: Minor vs major fault?** → **A:** No I/O (page already cached) vs disk I/O.
- **Q: EAT formula?** → **A:** (1−p)·access + p·fault_time.

## 21. Revision
Demand paging means PTEs start not-present and load pages on first touch. The page fault is the mechanism: MMU raises #PF (CR2 = address), the kernel validates against VMAs (`find_vma`), then loads from the zero page (fresh anon), page cache (file), or swap (evicted anon), installs the PTE, and retries. Fault rate p drives the EAT formula; minor faults (cached) are cheap, major faults (disk) are ~10⁵–10⁶ cycles. Readahead prefetches for sequential access, COW and guard pages deliberately abuse the fault path, and excessive faulting becomes thrashing (Chapter 03).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is demand paging?" | 2 How / 13 Q1 |
| "Walk me through a page fault." | 9 Internal / 13 Q3 |
| "Valid vs invalid fault?" | 13 Q4 / 9 Internal |
| "What is EAT and how does p affect it?" | 8 Example / 13 Q6 |
| "Minor vs major faults?" | 13 Q7 / 18 Cheat Sheet |
| "How does calloc avoid allocating?" | 13 Q9 / 8 Example |
| "How is swap-in different?" | 13 Q12 / 2 How |
