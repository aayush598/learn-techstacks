# Partitioning and Swapping

> **TL;DR**: **Partitioning** splits RAM into (fixed or dynamic) regions for processes; **swapping** moves entire processes between RAM and a swap disk to free memory for new arrivals — the ancestor of virtual memory, but O(size) I/O per swap makes it a last resort on modern systems.

## 1. Why Does This Exist?
Without partitioning, either one process owns all RAM (no multiprogramming) or allocation is ad-hoc. Partitioning exists to give the OS a *predictable* way to divide RAM so that multiple processes can reside simultaneously and be scheduled. Swapping exists to answer the follow-on problem: "the next process needs RAM, but the current set of processes won't fit." Moving a whole process to disk frees a complete contiguous region immediately, letting the OS run more processes than fit in RAM — the direct precursor of virtual memory (Part 07). Swapping also serves robustness: a process can be rolled out when it blocks on I/O, and its memory reused.

## 2. How Does It Work?
**Partitioning:**
- **Fixed (static) partitions**: memory divided at boot into N partitions of fixed sizes (e.g., 4×64 KB, 3×128 KB). A queue per partition; a process goes to the smallest partition that fits it. Allocation is O(1), but internal fragmentation is unavoidable.
- **Dynamic (variable) partitions**: no fixed sizes; holes are created/split as processes arrive/depart (Chapter 02 Sec 01's free-list). No internal fragmentation but external fragmentation appears.

**Swapping:**
1. OS selects a victim process (idle/blocked/longest-suspended).
2. Writes its whole image to a swap region on disk (swap file/partition).
3. Marks its memory free; reassigns the region.
4. When the swapped-out process becomes runnable, **swap-in**: read the whole image back (only when enough contiguous RAM exists).
5. Its base/limit (or page tables) are restored; it resumes where it left off.
A process's **swap-in/swap-out time is proportional to its size** — the crucial scaling problem.

## 3. When Is It Used?
- **Early Unix (V6/V7)**: the "swapping" approach as the only way to multiplex small RAM; large programs were swapped out wholesale.
- **Modern Linux**: `swap` still exists (`/swapfile`, `zram`) but the unit is the *page*, not the process — demand paging + swap of pages (Part 07), not whole-process roll-out.
- **RTOS / small embedded**: partitioned heaps; `heap_5` merges static buffers at link time.
- **Windows**: the paging file (`pagefile.sys`) — again page-granular, not process-granular.
- **Process suspend/resume tools**: e.g., laptop *hibernation* (write RAM to disk, restore on boot) is whole-memory swapping; checkpoint/restore (CRIU) is process swapping at a finer granularity.

## 4. Why Wasn't Another Approach Chosen?
- **Fixed partitions vs dynamic**: fixed is O(1) and dead-simple but wastes RAM (internal) and guesses sizes poorly; dynamic wastes via external fragmentation. Modern general-purpose OSes choose *neither* — they page.
- **Swapping whole processes vs paging**: swapping has two fatal flaws: (1) cost scales with *process size* (a 2 GB process costs 2 GB of I/O per swap); (2) it needs a *contiguous* free region to swap back in. Paging (Part 07) swaps only the pages actually touched, and any frames work, so it scales. Thus modern OSes keep swap *pages*, not processes.
- **Not swapping (run until memory exhausted)**: OOM-kill or system failure. Swapping is preferable when temporary.
- **Demand paging**: the chosen successor — lazily loads only referenced pages and evicts only some pages — same purpose (oversubscribe RAM) at ~0 cost when memory pressure is low.

## 5. Intuition
RAM is a hotel with limited rooms. Partitioning = the hotel manager decides in advance how many rooms of each type (studio, suite) exist. Swapping = when the hotel is full, the manager tells a sleeping guest "move your stuff to the storage locker down the street" so a new guest can check in, then moves them back when a room frees up. Moving luggage costs time proportional to how much stuff you have (O(size)); and if there's no room in the hotel when they return, they wait outside (contiguity requirement).

## 6. Real-World Analogy
An office with fixed cubicle sizes (fixed partitions) — you get a cubicle bigger than you need (internal waste) or too small (can't fit). Swapping is like seasonal warehouse overflow: when the office fills, move a whole team's desks to an external warehouse; when they need to work, truck everything back. Trucking cost = volume of desks moved (O(size)), and the move back requires a free floor (contiguous space).

## 7. Formal Definition
**Partitioning** is a memory-management scheme that divides physical memory into regions (partitions) of fixed or variable size to which processes are bound; fixed partitioning allocates a partition of size ≥ process size (inducing internal fragmentation), while variable partitioning allocates exact-size holes (inducing external fragmentation). **Swapping** is the transfer of an entire process image between main memory and backing store (swap device) so that a process may be temporarily absent from memory; swap-out frees its region and swap-in restores it when scheduled, with cost proportional to process size.

## 8. Example
RAM 1 MB, fixed partitions: 256 KB × 4.
- Processes: P1=150 KB → partition A (256 KB, 106 KB internal waste); P2=300 KB → cannot fit any single partition → wait/swap.
- If 4 processes each ~200 KB: each wastes ~56 KB → 224 KB total wasted (internal).

Dynamic example with swapping: RAM 512 KB. P1=200 KB @0, P2=150 KB @200, P3=100 KB @350. Free = 62 KB.
- P4 arrives needing 180 KB → no hole. **Swap out P2** (150 KB): write 150 KB to disk, now free = 212 KB contiguous at [200,512). P4 placed at [200,380).
- P2 becomes runnable → **swap in**: needs 150 KB contiguous. Free is [380,512) = 132 KB → too small → P2 must wait (double-swap hazard) or another process must be swapped.

Swap time: at 100 MB/s disk, swapping a 100 MB process costs ~1 s each way (2 s round trip) — vs a few ms for page-level swap of a touched working set.

## 9. Internal Working
1. **Partition init**: at boot, carve RAM into partitions (fixed) or an empty free-list (dynamic).
2. **Admission**: on process creation, find smallest fitting partition (fixed) or a fitting hole (dynamic, per first/best/worst).
3. **Scheduling tie-in**: a process that blocks on I/O is a swap-out candidate (freeing RAM for a CPU-bound process) — the classic *scheduler + swapper* design (e.g., the "medium-term scheduler").
4. **Swap-out**: suspend process → flush its TLB/state → copy image to swap → free region → update free-list.
5. **Swap-in**: when the process is unblocked and scheduled, check for contiguous space ≥ size; if none, choose to (a) wait, (b) swap out another process, or (c) compact.
6. **Restore**: reload image, restore base/limit, resume.
7. Modern page-swapping replaces steps 4–5 with per-page demand loading (Part 07 Ch 01).

## 10. Time Complexity
- Fixed-partition allocate: **O(1)** (index into partition queue).
- Dynamic-partition allocate: O(n) (free-list scan).
- Swap-out/in: **O(size of process)** — linear in process size, dominated by disk bandwidth; e.g., 100 MB at 500 MB/s ≈ 200 ms each way.
- Context-switch overhead is unaffected (swapping happens at scheduler boundaries, not per instruction).
- Page-level swap (modern): O(#pages touched) ≈ O(working set), usually ≪ O(size).

## 11. Advantages
- Fixed partitions: O(1) allocation, deterministic, trivial.
- Swapping: allows running *more* processes than RAM fits; simple to implement on top of contiguous allocation; good for processes that are idle/blocked for long stretches (roll them out, roll in busy ones).
- No page tables needed (contiguous translation).
- Great for **real-time**: predictable layout, no page faults.

## 12. Disadvantages
- Fixed partitions: internal fragmentation; poor fit for mixed workloads.
- Dynamic partitions: external fragmentation → needs compaction.
- Swapping: **O(size) I/O** per swap; **contiguous-space requirement** on swap-in can cause deadlock-like waits (double-swapping); disk wear; long latency spikes.
- Whole-process swap cannot share pages between processes (libc loaded per process in RAM).
- Not scalable: swapping a 64-bit process's 8 GB address space is absurd → modern systems swap pages instead.
- Hibernation uses swap but needs enough swap space ≥ RAM size.

## 13. Interview Questions
1. **Q: Fixed vs dynamic partitioning — trade-offs?** A: Fixed: O(1) allocation, but internal fragmentation and bad size guessing. Dynamic: exact sizes, no internal waste, but external fragmentation requiring compaction or swapping.
2. **Q: What is swapping?** A: Moving a whole process image between main memory and a backing store so the OS can oversubscribe RAM; swap-out frees a region, swap-in restores it when runnable.
3. **Q: Why did page-swapping replace whole-process swapping?** A: Whole-process swap costs O(size) — a 8 GB process means 8 GB of I/O per swap — and requires a contiguous region to swap back into. Page-level swap costs O(working set) and any frames work. Demand paging keeps RAM oversubscription with negligible idle cost.
4. **Q: What is the "double swap" / thrashing risk? (Tricky)** A: If more processes are ready than fit in RAM, the OS may swap out a process that's immediately needed, forcing another swap-out — time is wasted moving processes in/out with no work done. This is the process-level ancestor of *thrashing* (Part 07 Ch 03).
5. **Q: When is swapping actually beneficial in production?** A: Hibernation (whole-RAM swap), checkpointing long-running jobs to survive restarts, and rolling out long-idle processes to free memory for bursty ones — where the swap is rare and amortized over long idle time.
6. **Q: How does the OS pick a victim to swap out?** A: Prefer processes that are (a) blocked/idle, (b) small (cheaper to move), (c) have been out of the running set longest; never swap kernel threads or pinned/real-time processes.
7. **Q: Why does swap-in need contiguous space?** A: Under contiguous allocation, the process must be restored as one image at one base; if no single hole fits, it waits — hence the requirement (and why paging removes it).
8. **Q: How do modern Linux systems "swap" today? (Production)** A: They swap *pages* via demand paging (`do_swap_page`), use `zswap`/`zram` (compressed in-RAM swap) to trade CPU for I/O, and only under memory pressure. `sysctl vm.swappiness` tunes how eagerly anonymous pages are swapped.
9. **Q: What's the relationship between partitioning and security?** A: Partitions + base/limit give coarse isolation (a partition can't read another). Fine-grained sharing needs paging. ARINC 653 partitions on avionics enforce space isolation this way.
10. **Q: Can fixed partitioning lead to a "wait forever" condition?** A: Yes — if no partition of sufficient size ever frees (partition sizes badly chosen), small processes starve or large ones wait indefinitely; dynamic partitioning avoids the size mismatch but adds external fragmentation.
11. **Q: What happens to a swapped-out process's timers/sockets?** A: Kernel state (PCB, file descriptors, timers) stays in RAM; only the *address-space image* moves to disk, so the process "freezes" — sockets may time out if the swap is too long.
12. **Q: Why is swapping unsuitable for real-time systems?** A: Swap-in latency is unbounded (depends on disk + contiguity) — real-time deadlines can't tolerate multi-second pauses. RTOSes pin all processes in RAM (or use fixed partitions).
13. **Q: Swapping vs virtual memory — one sentence each.** A: Swapping moves *entire processes* between RAM and disk; virtual memory (Part 07) moves *individual pages* on demand, giving the same oversubscription with far lower cost and no contiguity requirement.

## 14. Follow-Up Questions
1. **Q: What's a "roll in/roll out" policy?** A: Rolling out a blocked process and rolling in a ready one when the CPU has nothing else — a classic swapping-driven scheduling heuristic (medium-term scheduling).
2. **Q: How does hibernation relate to swapping?** A: Hibernation writes the entire RAM image to the swap file/partition and, on resume, restores it — whole-memory swapping with a single swap-in.
3. **Q: What's zram vs zswap?** A: `zram` creates a compressed block device in RAM used *as* the swap device (good for low-RAM devices); `zswap` compresses pages and stores them in RAM *before* writing to disk swap, deferring real I/O.
4. **Q: Why would a swap partition be preferred over a swap file?** A: Swap files on certain filesystems need `swapon` support and can fragment/contend with filesystem I/O; a dedicated partition avoids filesystem overhead and is simpler for the kernel (`swap_info` subsystem).

## 15. Coding Example
```c
// Simulate whole-process swapping: pick victim, free its region, swap back in
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define RAM_SIZE 512

typedef struct { char name; unsigned base, size; int in_ram; } Proc;

// backing store keyed by name -> image copy in "disk" (heap array)
static char *disk[26];

void swap_out(Proc *p) {
    disk[p->name - 'A'] = malloc(p->size);      // write image to "disk"
    printf("%c: swap-out %u KB @%u\n", p->name, p->size, p->base);
    p->in_ram = 0; p->base = 0;
}

int swap_in(Proc *p, Proc *others, int n) {
    // find a contiguous free region by scanning from 0 upward (first-fit)
    unsigned cursor = 0;
    for (int i = 0; i < n; i++) {
        if (others[i].in_ram && others[i].base >= cursor) {
            if (others[i].base - cursor >= p->size) break;
            cursor = others[i].base + others[i].size;
        }
    }
    if (RAM_SIZE - cursor < p->size) { printf("%c: swap-in blocked\n", p->name); return -1; }
    p->base = cursor; p->in_ram = 1;
    free(disk[p->name - 'A']);
    printf("%c: swap-in @%u\n", p->name, p->base);
    return 0;
}

int main(void) {
    Proc p1 = {'A',0,200,1}, p2 = {'B',200,150,1}, p3 = {'C',350,100,1};
    Proc *all[] = { &p1, &p2, &p3 };
    swap_out(&p2);
    // place a 180 KB process in the freed 212 KB region
    Proc p4 = {'D',200,180,1};
    swap_in(&p2, (Proc[]){p1,p3,p4}, 3);        // may or may not fit now
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/swapfile.c`, `mm/swap.c`, `zswap`, `zram`, `swappiness`; hibernation via `echo disk > /sys/power/state`.
- **Windows**: `pagefile.sys` (page-granular swap); hibernation file `hiberfil.sys`.
- **macOS**: dynamic `swapfile0..n`, compressed memory (Apple's `vm_compressor`).
- **Real-time**: ARINC 653 partitioning; RTEMS fixed partitions; QNX provides both fixed and dynamic for embedded partitions.
- **CRIU (Checkpoint/Restore In Userspace)**: dumps a process's full image to disk (process-level swap) for live migration and container checkpointing.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.2 "Contiguous Allocation", 8.2.3 "Swapping".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.2 "Memory Management: Swapping".
- Linux source: `mm/swapfile.c`, `mm/swap_state.c`, `include/linux/swap.h`.
- Linux docs: `Documentation/admin-guide/sysctl/vm.rst` (swappiness), `Documentation/admin-guide/blockdev/zram.rst`.
- ARINC 653 / RTCA DO-178C partitioning standards.

## 18. Cheat Sheet
- Fixed partitions → O(1), internal fragmentation.
- Dynamic partitions → exact fit, external fragmentation.
- Swapping = whole-process RAM↔disk; cost O(size); needs contiguous region.
- Swap-in blocked ⇒ double-swap/thrashing risk.
- Page-level swap (modern) costs O(working set), any frames.
- zram/zswap = compressed RAM-backed swap; swappiness tunes aggressiveness.
- Hibernation = whole-RAM swap-out.
- Virtual memory supersedes swapping for oversubscription.

## 19. Quiz
1. Fixed partitioning causes:
   a) external fragmentation b) internal fragmentation c) thrashing d) both a & b → **b**
2. Swapping cost is proportional to:
   a) number of processes b) process size c) page count d) TLB size → **b**
3. Modern Linux swaps:
   a) whole processes b) individual pages c) partitions d) nothing → **b**
4. A process can't be swapped back in because:
   a) no contiguous hole b) disk full c) TLB full d) scheduler busy → **a**
5. `zram` provides:
   a) faster CPU b) compressed RAM-backed swap device c) disk cache d) page tables → **b**
6. Hibernation is an example of:
   a) page swap b) whole-memory swap c) fixed partition d) compaction → **b**

## 20. Flashcards
- **Q: Fixed vs dynamic partitions?** → **A:** Fixed = pre-sized (O(1), internal frag); dynamic = exact holes (external frag).
- **Q: What is swapping?** → **A:** Moving entire processes RAM↔disk; O(size) I/O; needs contiguity.
- **Q: Why page-swap instead of process-swap?** → **A:** Cost O(working set) vs O(size); no contiguity requirement.
- **Q: What's the double-swap hazard?** → **A:** Swapping a process in/out repeatedly because RAM pressure is too high — wasted I/O.
- **Q: What do zswap/zram do?** → **A:** Compress swapped pages in RAM to avoid disk I/O.
- **Q: When is swapping still used?** → **A:** Hibernation, CRIU checkpoint, rolling out idle processes.

## 21. Revision
Partitioning divides RAM into fixed (O(1), internal waste) or dynamic (exact fit, external waste) regions. Swapping moves whole processes to a backing store when RAM is short, trading O(size) I/O for RAM; swap-in needs a contiguous hole, so under pressure you get double-swap thrashing — the process-level ancestor of VM thrashing. Modern OSes abandoned process-swap: they swap *pages* (Part 07), costing only the working set, plus compression (zram/zswap). Fixed-partition and swap ideas survive in RTOSes, ARINC 653, hibernation, and checkpoint/restore tools.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Fixed vs dynamic partitioning?" | 2 How / 13 Q1 |
| "What is swapping and when is it used?" | 2 How / 13 Q2 |
| "Why did page swapping replace process swapping?" | 4 Alternative / 13 Q3 |
| "What's the double-swap/thrashing risk?" | 13 Q4 / 9 Internal |
| "How does modern Linux swap?" | 13 Q8 / 16 Industry |
| "Why can't you swap a real-time process?" | 13 Q12 |
