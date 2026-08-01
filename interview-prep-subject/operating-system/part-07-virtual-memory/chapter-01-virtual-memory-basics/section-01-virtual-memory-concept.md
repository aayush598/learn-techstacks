# Virtual Memory Concept

> **TL;DR**: Virtual memory decouples a process's logical address space from physical RAM — only the pages actually being used (the **working set**) need to be resident — exploiting locality to run programs far larger than physical memory.

## 1. Why Does This Exist?
Physical RAM is scarce and expensive; programs want more than exists (a 2 GB binary on a 512 MB machine, or thousands of processes each demanding gigabytes). Virtual memory exists to break the assumption from Part 06 that "the whole process must be in RAM." By marking pages non-present and loading them lazily, the OS can (1) run programs larger than RAM, (2) run more processes concurrently (oversubscription), (3) share pages across processes (libc once, not once per process), and (4) only ever pay I/O for pages actually touched. Without VM, a program couldn't start until all of it was resident; with VM, startup touches a few pages.

## 2. How Does It Work?
The process's logical space is *virtual*: each page is either:
- **resident** — mapped to a physical frame (present PTE), or
- **on disk / not yet allocated** — PTE has present=0, with metadata (in a VMA or swap entry) describing where the data lives.

On access to a non-present page, the MMU raises a **page fault**; the kernel's fault handler consults the process's VMAs to decide:
- **Valid access** (address within a VMA): allocate a frame, load the page from disk/swap or zero-fill, set PTE present, retry the instruction.
- **Invalid access** (no VMA, or permission violation): SIGSEGV.

The fault path (Part 07 Sec 02) is the heart of the mechanism; the *concept* here is the policy: which pages are resident, decided by the page-replacement algorithms (Chapter 02).

## 3. When Is It Used?
- **Every modern OS, all the time**: Linux, Windows, macOS, Android, iOS, BSDs.
- **Loading executables**: `execve` maps the binary lazily — a 200 MB binary starts instantly because only the first page is touched.
- **Shared libraries**: libc's text mapped once, resident once, referenced by all processes.
- **Databases**: huge buffer pools, memory-mapped tables, page-sized I/O tuned to VM.
- **Virtualization**: VMs oversubscribe host RAM the same way (ballooning, KSM).
- **JVM/mobile apps**: heap growth, compressed references, and AOT use VM semantics.

## 4. Why Wasn't Another Approach Chosen?
- **No VM (all-resident, Part 06)**: cannot run programs bigger than RAM; sharing requires copying; concurrency limited. Rejected for scale.
- **Overlays (programmer-managed)**: the programmer juggles what's resident — worked for small games in the 80s, unusable at scale; VM automates it.
- **Whole-process swapping (Part 06 Sec 03)**: works but costs O(size) per swap and needs contiguity; VM's per-page granularity is vastly cheaper.
- **Just more RAM**: infinite RAM is the "solution" that cloud vendors sell, but VM remains necessary for oversubscription, sharing, and fast startup — even 1 TB machines still fault-load pages.
- **Software translation without hardware (rejected)**: too slow; VM needs the MMU/TLB foundation.

## 5. Intuition
A college library can't hold all students' textbooks, so it lends pages on demand: you "fault in" the page you need from the repository (disk), and when shelves overflow, some pages are returned to storage. Students (processes) believe they hold every book; the librarian (OS) keeps only the popular ones nearby (working set). Most students re-read the same few chapters (locality), so the system works — but if too many students suddenly need different books, the librarian spends all day running to storage (thrashing, Chapter 03).

## 6. Real-World Analogy
A cookbook app on your phone: the whole book (500 MB) lives on the server (disk), but the app only downloads the recipe pages you actually open (demand paging). The phone's cache (RAM) holds recent recipes; when the cache fills, the least-recently-used recipes are dropped (page replacement). Reading a new recipe costs a network fetch (page fault) — but if you keep hopping between recipes randomly, every action stalls (thrashing).

## 7. Formal Definition
**Virtual memory** is a memory-management technique that gives each process the abstraction of a contiguous, arbitrarily large address space, backed by a combination of physical frames and secondary storage. The mapping between logical (virtual) pages and physical frames is defined by page tables; pages not in RAM are marked not-present and are brought in on demand (**demand paging**) when referenced. The set of pages currently needed by a process is its **working set**; effective VM relies on the principle of **locality** — programs cluster references in space and time — and on a **page-replacement algorithm** to choose eviction victims when memory is exhausted.

## 8. Example
A 32-bit process with a 4 MB binary on a machine with 64 MB RAM:
- `execve` maps the file: code VMA (4 MB), data VMA, stack VMA — *no frames allocated*; PTEs not-present.
- Main touches code page 0 → fault → allocate frame, read 4 KB from disk → PTE present. Startup touches maybe 20–50 pages out of 1024 → ~100–200 KB read.
- The process *thinks* it has 4 GB (its address space); it actually consumes ~a few MB resident.
- Two more copies of the same binary run: both processes' page tables point at the *same* code frames (shared read-only) → total resident for 3 processes ≈ 1 process's code + per-process data.

Without VM: the whole 4 MB binary must load before start; with 2 more processes, each loads its own copy → 12 MB; with VM → ~5 MB and instant start.

## 9. Internal Working
1. **Setup**: process's `mm_struct` holds a linked list / maple-tree of VMAs (`struct vm_area_struct`), each with range + flags (READ/WRITE/EXEC, file-backed vs anonymous, MAP_SHARED vs MAP_PRIVATE).
2. **Access**: a load touches page P; TLB miss; hardware walk; PTE present=0 → #PF.
3. **Dispatch**: CPU saves state, traps to `do_page_fault` (arch-specific) with the faulting address (CR2 on x86) and error code.
4. **Decide**: `find_vma` looks up the VMA covering the address:
   - none → SIGSEGV (invalid).
   - permission mismatch → SIGSEGV (or copy-on-write path).
   - valid but not present → **demand paging**.
5. **Allocate**: `handle_mm_fault` → `alloc_zeroed_user_highpage` or read from `address_space` (`filemap_fault` for mmap'd files; `swapin_readahead` for swapped pages).
6. **Install**: `set_pte` marks present with proper bits; flush TLB entry (optional; not cached yet).
7. **Resume**: return from exception → retry the faulting instruction; now the TLB walks the present PTE.

## 10. Time Complexity
- Demand-load a fresh page: **O(1)** frames + **O(I/O)** — ~0.1–1 µs for a cached/dirty page, ~100 µs–1 ms for SSD/disk I/O; a *page fault ≈ 10⁵–10⁶ cycles* vs ~1 cycle TLB hit (5+ orders of magnitude).
- Fault handling overhead (no I/O): ~1–10 µs (walk, alloc, install, retry).
- Accessing N distinct fresh pages: O(N × fault cost).
- `execve` mapping: O(#segments), not O(#pages) — lazy.
- Sharing: O(1) PTE updates to point multiple processes at one frame.

## 11. Advantages
- Programs can be **larger than physical RAM**.
- **Oversubscription**: more processes than fit in RAM (working sets overlap).
- **Sharing**: files/libraries/COW pages shared via page tables.
- **Fast startup** and low memory for binaries (`execve` is lazy).
- **Protection** integrated: each VMA's permissions enforced by PTEs.
- Memory-efficient: pages touched ≤ pages needed (working set), not total footprint.

## 12. Disadvantages
- **Page-fault latency**: unpredictable stalls (µs–ms) — bad for real-time.
- **Overhead**: TLB/table walks, fault handling, kernel complexity.
- **Thrashing** risk (Chapter 03): if the working set exceeds RAM, the system spends all time faulting.
- **Memory overhead** of VMAs, page tables, swap metadata.
- **Predictability loss** for embedded/safety-critical (must pin/lock pages).
- Swap device management (space, wear on SSDs).

## 13. Interview Questions
1. **Q: What is virtual memory?** A: An abstraction giving each process a large logical address space backed by only the resident subset of pages; missing pages are loaded on demand (demand paging), with page-replacement choosing eviction victims.
2. **Q: Why does virtual memory work at all?** A: **Locality** — programs reference a small fraction of their pages in short windows (spatial + temporal), so a small resident working set suffices.
3. **Q: What is the difference between virtual memory and swap?** A: VM is the abstraction (paged address space); swap is one implementation of *evicting* pages to secondary storage. Not all evictions go to swap (file-backed pages go back to their file; anonymous pages to swap).
4. **Q: Can a process run with zero resident pages?** A: Not meaningfully — it must fault in pages to execute; but VM lets almost all pages be absent at any moment, which is why 100+ processes can share RAM.
5. **Q: What happens when you `exec` a huge binary? (Scenario)** A: The kernel maps its segments into VMAs with PTEs not-present; only pages actually touched fault in. A 2 GB binary starts in ~100 ms because maybe 10 MB gets read.
6. **Q: How much slower is a page fault than a TLB hit? (Production)** A: ~1 cycle vs ~1 µs (fresh) to ~1 ms (disk) — 10⁵–10⁶×. The gap is why page-replacement quality and hit ratios matter enormously.
7. **Q: What is oversubscription?** A: The OS admits more resident pages than physical RAM (working sets overlap); guaranteed only when total *working sets* ≤ RAM, else thrashing.
8. **Q: How are two processes sharing one library different from two copies?** A: Both page tables point to the same frames (read-only) — zero extra RAM for the second process's code; "copy" would double it.
9. **Q: What's the role of VMAs in the fault path?** A: `find_vma` decides if the faulting address is legal and with what semantics (file-backed/anon, shared/private); no VMA → SIGSEGV.
10. **Q: Is a page fault always bad?** A: No — demand faults are the *mechanism*; only excessive faulting (thrashing) or faults on invalid addresses (SIGSEGV) are problems.
11. **Q: What is the working set?** A: The set of pages a process referenced in the recent past (e.g., the last Δ time units); a useful estimate of resident needs (Chapter 03).
12. **Q: Why is the page table not "virtual memory" by itself?** A: Page tables are the *translation* mechanism (Part 06); VM is the *policy* of lazily populating them and evicting — different layers.

## 14. Follow-Up Questions
1. **Q: What happens to a process's VMAs at `fork`?** A: The child inherits a *copy* of the VMA list and page tables (COW) — cheap, not a memory copy (Part 07 Sec 03).
2. **Q: What is a "sparse" file and how does VM handle it?** A: A file with unwritten holes; `mmap` maps it lazily so holes fault as zero-filled pages without allocating disk blocks.
3. **Q: How do huge pages change VM?** A: Fewer, larger PTEs (2 MB/1 GB) — cheaper walks, fewer TLB misses, but coarser granularity for eviction/sharing.
4. **Q: How does the OOM killer relate to VM?** A: When the kernel can't reclaim enough (no evictable pages), it selects a victim process (by score) and kills it to free frames — the last line of defense for oversubscription failure.

## 15. Coding Example
```c
// Simulate demand paging: pages "on disk" loaded lazily, tracked by present bit
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define NPAGES 16
typedef struct { uint8_t present; uint8_t data[64]; } Page;
static Page *disk[NPAGES];      // backing store
static Page *ram[NPAGES];       // resident frames

void ensure_page(unsigned p) {
    if (ram[p]) return;
    if (!disk[p]) { disk[p] = calloc(1, sizeof(Page)); memset(disk[p]->data, p, 64); }
    ram[p] = disk[p];           // demand load: copy/swap into a frame
    disk[p] = NULL;
    printf("page %u demand-loaded\n", p);
}

uint8_t vload(unsigned p, unsigned off) {
    ensure_page(p);
    return ram[p]->data[off];
}

int main(void) {
    printf("read page 3 byte 10 = %u\n", vload(3, 10));   // loads page 3
    printf("read page 3 byte 10 = %u\n", vload(3, 10));   // cached, no fault
    printf("read page 9 byte 0 = %u\n", vload(9, 0));     // loads page 9
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/memory.c` (`handle_mm_fault`), `mm/filemap.c` (`filemap_fault`), `mm/mmap.c` (VMAs), `mm/swapfile.c`; `Documentation/admin-guide/mm/`.
- **Windows**: NT virtual memory manager — page faults, working sets, mapped files (`CreateFileMapping`/`MapViewOfFile`).
- **macOS**: XNU VM, `vm_map`, compressed memory instead of swap.
- **Databases**: Postgres/MySQL tune `shared_buffers` vs page cache; memory-mapped tables (SQLite, RocksDB-like engines).
- **Languages**: Go/JVM heaps assume VM; JITs use guard pages; Rust's `mmap` in allocators (jemalloc/mimalloc).
- **Virtualization**: KVM/KSM merges duplicate pages across VMs (VM-aware sharing).

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9 "Virtual Memory".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.6–3.7 "Virtual Memory".
- Denning, P. "The Locality Principle" (CACM 2005) — the theoretical basis.
- Linux source: `mm/memory.c`, `mm/mmap.c`, `mm/filemap.c`, `Documentation/admin-guide/mm/*`.
- `man 2 mmap`, `man 5 proc` (`/proc/<pid>/smaps` shows resident vs virtual).

## 18. Cheat Sheet
- VM = logical space ≫ RAM; only working set resident.
- Works because of locality (spatial + temporal).
- Present=0 PTE → #PF → `do_page_fault` → valid? load or SIGSEGV.
- Demand paging = lazy load on first touch.
- execve/mmap are lazy — startup is cheap.
- Sharing via page tables (one frame, many PTEs).
- Fault ≈ 10⁵–10⁶ cycles vs ~1 cycle TLB hit.
- Thrashing = working sets > RAM; eviction algorithms decide victims.
- Swap is one eviction target (for anonymous pages), not "VM".

## 19. Quiz
1. Virtual memory works because of:
   a) bigger disks b) locality c) faster CPUs d) caching in L2 → **b**
2. A present=0 PTE causes:
   a) TLB hit b) page fault c) SIGSEGV always d) deadlock → **b**
3. Which is NOT true of demand paging?
   a) pages load on first touch b) startup is fast c) whole process must be resident d) faults are normal → **c**
4. Sharing libc across processes means:
   a) copying it per process b) shared frames via page tables c) static linking d) it's impossible → **b**
5. A page fault that hits disk costs about:
   a) 10 cycles b) 1000 cycles c) 10⁵–10⁶ cycles d) 10 cycles → **c**
6. The OOM killer runs when:
   a) disk full b) can't reclaim enough frames c) TLB full d) too many VMAs → **b**

## 20. Flashcards
- **Q: What is virtual memory?** → **A:** Logical address space backed by only resident pages; demand-loaded, evicted by algorithms.
- **Q: Why does VM work?** → **A:** Locality — working sets are tiny fractions of address spaces.
- **Q: What triggers a page fault?** → **A:** Present=0 PTE or permission violation during translation.
- **Q: What does the kernel check first in a fault?** → **A:** Whether the address is inside a VMA (valid) and permissions match.
- **Q: Why is `exec` cheap?** → **A:** Lazy mapping — only touched pages fault in.
- **Q: What is the working set?** → **A:** The pages a process recently referenced — what it needs resident.

## 21. Revision
Virtual memory replaces "all-resident" with "resident-on-demand": the process's huge logical space is served by page tables whose PTEs are often not-present; touching a missing page raises a fault, the kernel validates it against VMAs, loads the page from file/swap or zero-fills it, and resumes. Locality makes this efficient — working sets are small — and page tables enable sharing (libc once) and oversubscription. Faults cost ~10⁵–10⁶ cycles, so replacement quality matters; when working sets exceed RAM, the system thrashes. This concept powers everything in the rest of Part 07 and is the most-asked VM interview topic.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is virtual memory and why does it work?" | 1 Why / 13 Q1-2 |
| "What is demand paging?" | 2 How / 9 Internal |
| "Is a page fault always an error?" | 13 Q10 / 2 How |
| "Why is exec fast for huge binaries?" | 13 Q5 / 8 Example |
| "What's the difference between VM and swap?" | 13 Q3 / 18 Cheat Sheet |
| "What is oversubscription / OOM?" | 13 Q7 / 14 Q4 |
