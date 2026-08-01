# Crash-Course Revision

> **TL;DR**: A dense, part-by-part rapid-revision deck covering all 9 OS parts in one sitting: the core definitions, the essential formulas/structures, the classic problems, and the highest-yield interview lines — with pointers to deep sections for anything you can't recall instantly.

## 1. Why Does This Exist?
The night before an interview (or between rounds), you need a *single pass* that re-anchors every part: definitions, key structures, classic algorithms, and the trade-off lines. The 22-block sections are deep; this is the **compressed map** — a table you can skim in 20–30 minutes that instantly tells you what you know and what needs a revisit. It exists because breadth matters in OS loops: one weak part (e.g., file systems) can cost a round even if the rest is strong.

## 2. How Does It Work?
The revision is organized part-by-part. For each part: **core facts** (one-liners), **key structures** (the kernel/CS objects), **classic problems/algorithms**, **the trade-off line** (the interview payoff), and **the top 2 questions**. Read top-down; mark anything you can't state in 10 seconds, then re-anchor in the linked section.

## 3. The Revision Deck
**Part 01 — OS Fundamentals**
- Core: OS = resource manager + abstraction layer; kernel = always-resident core; monolithic (Linux) vs microkernel (Mach).
- Key: syscall vs library call; user/kernel mode; context switch vs mode switch.
- Trade-off: monolithic = fast, tight coupling; microkernel = safe, slower IPC.
- Top: "What does an OS do?" "What is a syscall?"

**Part 02 — Processes and Threads**
- Core: process = resource container + execution; thread = execution sharing the container.
- Key: states (Ready/Running/Blocked/Zombie); `task_struct`; fork (COW) / exec / wait; user vs kernel threads.
- Trade-off: process = isolation, costly switch; thread = cheap switch, shared state, single crash kills all.
- Top: "Process vs thread?" "What is fork/exec?"

**Part 03 — CPU Scheduling**
- Core: scheduler picks the next ready task; preemptive vs non-preemptive.
- Key: FCFS (convoy), SJF/SRTF (min avg wait, starvation), RR (fairness), priority (+ aging), multilevel feedback; CFS (vruntime rbtree), sched classes.
- Trade-off: throughput vs latency vs fairness — no free lunch; CFS weights by `nice`.
- Top: "Compare FCFS/SJF/RR." "How does CFS work?"

**Part 04 — Process Synchronization**
- Core: race → critical section → mutual exclusion/progress/bounded waiting.
- Key: mutex (ownership), semaphore (counting, no ownership), spinlock (busy-wait), condition variables, futex (fast path no syscall).
- Problems: bounded buffer (mutex + empty=N + full=0), readers–writers, dining philosophers; atomics/CAS for lock-free.
- Trade-off: mutex = safe ownership, sleeps; spinlock = fast tiny critical sections, burns CPU.
- Top: "Mutex vs semaphore?" "Bounded buffer?"

**Part 05 — Deadlocks**
- Core: 4 conditions — mutual exclusion, hold-and-wait, no preemption, circular wait.
- Key: prevention (break one), avoidance (Banker's algorithm), detection (wait-for graph) + recovery.
- Trade-off: prevention = restrictive/simple; avoidance = needs known max claims; detection = runtime cost.
- Top: "Name the 4 conditions." "Banker's algorithm?"

**Part 06 — Memory Management**
- Core: MMU translates logical→physical; contiguous allocation fragments.
- Key: paging (pages, page tables, PTE flags), segmentation (variable-size, segment tables), paging+segmentation.
- Trade-off: internal vs external fragmentation; pages = simple + no external frag; segments = logical but external frag.
- Top: "Logical vs physical address?" "Internal vs external fragmentation?"

**Part 07 — Virtual Memory**
- Core: virtual space > physical; demand paging; page faults.
- Key: TLB (cache of PTE), page replacement (FIFO/OPT/LRU/Clock), Belady's anomaly, working set, thrashing, COW, mmap.
- Trade-off: OPT optimal but unimplementable; LRU good but approximated (Clock); FIFO simple but Belady-prone.
- Top: "Page replacement algorithms?" "What is thrashing?"

**Part 08 — File Systems**
- Core: files, directories, inodes, allocation, crash safety, RAID, SSDs.
- Key: inode vs name; hard vs soft links; contiguous/linked/indexed allocation; extents; journaling/CoW/LFS; VFS (super_block/inode/dentry/file/address_space); RAID 0/1/5/6/10; TRIM/wear leveling; NTFS MFT.
- Trade-off: contiguous = fast/simple but fragments; journal = safe/fast recovery but write overhead; CoW = snapshots/checksums but write amplification.
- Top: "Hard vs soft links?" "What is the VFS?" "RAID levels?"

**Part 09 — IPC and Linux Internals**
- Core: pipes/MQ/shm/semaphores/sockets/signals; namespaces/cgroups; syscall mechanism; address space.
- Key: pipe (byte stream), MQ (priority), shm (zero-copy, no sync), semaphore (sync), socket (full-duplex/network), signal (async event); `fork`/`exec`/`exit`/`wait`; `syscall`+`sys_call_table`+vdso; PAGE_OFFSET direct map, kmalloc vs vmalloc; `/proc`.
- Trade-off: shm fastest but sync is on you; sockets general but heavier; syscall ~100 ns, vdso ~10 ns.
- Top: "IPC comparison?" "What happens when you type a command?"

**Part 10 — This bank**
- Core: 4-step answer (definition → trade-off → example → kernel detail); design loop (requirements → components → trade-offs → scenario); STAR behaviorals.
- Trade-off: recall vs reasoning — the reasoning is graded.

## 4. Why Wasn't Another Approach Chosen?
- **Reading the full series again (rejected for pre-interview)**: depth is right for learning, wrong for the night before — the crash deck compresses to 20–30 min.
- **Only question lists (rejected)**: without the *lines* (trade-off phrasing, kernel structures), answers stay shallow.
- **Only code (rejected)**: interviews are verbal; the deck emphasizes speakable one-liners.
- **Flashcard app only (rejected)**: a curated linear deck is faster to self-diagnose than a random-shuffle app for last-minute anchoring.

## 5. Intuition
**A pilot's pre-flight checklist**: you don't re-read the manual before each flight — you run a checklist that touches every system (engines, hydraulics, avionics). This deck is the OS pre-flight: a rapid pass over every subsystem, where "check" means you can state the core fact, structure, algorithm, and trade-off line in 10 seconds.

## 6. Real-World Analogy
**A fire drill checklist**: alarms (processes), exits (scheduling), assembly points (synchronization), no bottlenecks (deadlocks), floor plans (memory), evacuation (virtual memory), storage lockers (filesystems), communications (IPC), command center (Linux internals). You walk the checklist; anything you can't recall instantly, you practice — that's the drill.

## 7. Formal Definition
A rapid-revision deck = a per-part table of {core facts, key structures, classic algorithms, trade-off lines, top questions} drawn from the series' 22-block sections, designed to be re-anchored in ≤30 minutes with a self-diagnosis pass (10-second recall per cell). It complements — not replaces — deep study; cells you can't recall in 10 seconds are marked for revisit in the linked sections.

## 8. Example
Self-test "page replacement":
- State in 10 s: FIFO (oldest out; Belady's anomaly possible), OPT (min faults, needs future — benchmark only), LRU (least-recently-used; hardware cost high), Clock (second-chance LRU approximation, a single pointer around a ring).
- Trade-off line: "OPT is the lower bound but unimplementable; LRU is the target, and Clock approximates it cheaply; FIFO is simplest but can regress with more frames."
- If this took >10 s → reopen Part 07 Sec 02/03 for the worked examples (the 236/331-cylinder disk-scheduling-style traces).

## 9. Internal Working
1. Scan the deck top-to-bottom (20–30 min).
2. For each cell, self-test: can I state it in 10 seconds with the trade-off line?
3. Mark misses; reopen the linked sections' "Cheat Sheet" + "Revision" blocks (they're the same compressed view, deeper).
4. Re-drill only the marked cells; then run Section 01's Top-100 spot checks on those parts.

## 10. Time Complexity
- First pass: ~25–30 min (9 parts × ~3 min).
- Self-test: ~1 min per part.
- Re-drill misses: ~10 min.
- Total: ~45 min for a full re-anchor — the night-before budget.

## 11. Advantages
- **Breadth insurance**: no part left weak for the loop.
- **Trade-off lines**: ready-to-speak phrasing for the "why" follow-ups.
- **Self-diagnosing**: 10-second recall is a clear pass/fail signal.
- **Portable**: skimmable in a waiting room or between rounds.

## 12. Disadvantages
- **Depth trade**: compressed cells can't carry a deep discussion — must be ready to expand (linked sections).
- **Staleness**: the deck must reflect the actual series; verify against the sections when in doubt.
- **Not a substitute**: for the strong parts, the deck is a summary; for weak parts, it's a pointer, not the lesson.

## 13. Interview Questions
1. **Q: How do you use the crash course?** A: Skim part-by-part, self-test each cell in 10 seconds, mark misses, reopen the linked sections' cheat-sheet/revision blocks, then re-drill — about 45 minutes total.
2. **Q: What's the fastest way to re-anchor scheduling?** A: Recall FCFS/SJF/RR/priority/multilevel + CFS's vruntime rbtree + sched classes, then the trade-off line ("fairness vs latency — CFS weights by nice") — Part 03 + Part 09 Sec 01.
3. **Q: How do you re-anchor file systems fast?** A: Recall inode vs name, hard/soft links, allocation schemes, extents, journal/CoW/LFS, VFS objects, RAID levels, then the lines ("RAID ≠ backup", "journal = safe recovery, write overhead") — Part 08.
4. **Q: What's the single most important page-replacement line?** A: "OPT is the unattainable lower bound; LRU is the target approximated by Clock; FIFO can suffer Belady's anomaly." — Part 07 Sec 02/03.
5. **Q: How do you re-anchor IPC in 60 seconds?** A: Pipe = byte stream; MQ = structured/priority; shm = zero-copy but no sync; semaphore = sync; socket = full-duplex/network; signal = async event; then the table (shm fastest, sockets most general) — Part 09 Sec 01–06.
6. **Q: What's the deadlock re-anchor?** A: Four conditions + three strategies: prevention (break a condition), avoidance (Banker's), detection/recovery (wait-for graph) — Part 05.
7. **Q: What's the memory re-anchor?** A: Logical vs physical, MMU, paging (PTE, no external frag) vs segmentation (logical units, external frag), internal vs external fragmentation — Part 06.
8. **Q: What's the virtual-memory re-anchor?** A: Demand paging + page faults; TLB; replacement (FIFO/OPT/LRU/Clock); working set vs thrashing; COW; mmap — Part 07.
9. **Q: What's the sync re-anchor?** A: Race → critical section → 3 requirements; mutex vs semaphore vs spinlock; bounded buffer; futex fast path — Part 04 + Part 09 Sec 04.
10. **Q: What's the Linux internals re-anchor?** A: fork/exec/exit/wait; syscall mechanism + vdso; address space (PAGE_OFFSET direct map, kmalloc vs vmalloc); namespaces + cgroups; /proc; the type-a-command trace — Part 09.
11. **Q: What's the process/thread re-anchor?** A: Process = container + execution; thread = shared execution; COW fork; states; zombie/orphan; user vs kernel threads — Part 02 + Part 09 Sec 01.
12. **Q: What's the OS-fundamentals re-anchor?** A: OS = manager + abstractions; kernel; user/kernel mode; syscall vs lib call; context vs mode switch — Part 01.

## 14. Follow-Up Questions
1. **Q: How is this different from the Top-100?** A: The Top-100 is *questions* (delivery practice); the crash course is *facts + lines* (recall anchoring). Use both: deck first, then drill the questions.
2. **Q: What if a part feels truly weak?** A: Don't re-read the whole part the night before — read its "Cheat Sheet", "Revision", and "Flashcards" blocks (the compressed versions), then do 3–5 of its interview questions aloud.

## 15. Coding Example
```c
// The crash course as a flashcard self-test: state each line in 10s.
#include <stdio.h>

typedef struct { const char *part; const char *line; } card_t;

int main(void) {
    card_t cards[] = {
        {"scheduling", "FCFS convoy; SJF min wait; RR fair; CFS vruntime rbtree"},
        {"sync",       "mutex ownership; semaphore counting; futex fast path"},
        {"deadlock",   "4 conditions; prevent/avoid(Banker)/detect-recover"},
        {"memory",     "paging no external frag; segmentation external frag"},
        {"vmmem",      "OPT lower bound; LRU target; Clock approximation"},
        {"fs",         "inode vs name; journal safe; RAID != backup"},
        {"ipc",        "pipe stream; MQ priority; shm fast no sync; socket general"},
        {"linux",      "fork COW; syscall table; PAGE_OFFSET; ns+cgroups"},
    };
    for (int i = 0; i < 8; i++)
        printf("PART %-11s -> %s\n", cards[i].part, cards[i].line);
    return 0;
}
```

## 16. Industry Usage
- **Pre-interview cramming**: the standard night-before practice for OS loops.
- **Between-round refreshers**: a 10-minute skim before a second OS round.
- **Peer coaching**: use the cells as a quick oral quiz list.
- **Syllabus maps**: instructors/TAs compress a course into the same per-topic deck format.

## 17. References
- This series: parts 01–09 (the deck's source); the "Cheat Sheet", "Revision", and "Flashcards" blocks of each section are the same compressed view.
- Silberschatz / Tanenbaum / Love for any cell needing expansion.

## 18. Cheat Sheet
- Deck = per-part {core facts, key structures, algorithms, trade-off lines, top 2 questions}.
- Self-test: 10-second recall per cell; mark misses.
- Re-anchor misses in the linked sections' Cheat Sheet/Revision/Flashcards.
- Key lines: "RAID ≠ backup", "shm needs sync", "OPT unimplementable, LRU target, Clock approximates", "journal = safe recovery / write overhead", "mutex ownership vs semaphore counting", "process = container, thread = shared execution".
- Total re-anchor ≈ 45 min.

## 19. Quiz
1. The crash course is for? a) learning b) rapid re-anchoring c) code d) docs → **b**
2. Per-cell self-test time? a) 1 min b) 10 s c) 5 s d) 30 s → **b**
3. Weak part → reopen? a) whole part b) Cheat Sheet/Revision blocks c) code d) nothing → **b**
4. Key sync line? a) mutex ownership vs semaphore counting b) shm fast c) CFS rbtree d) RAID → **a**
5. Page replacement line? a) OPT optimal b) FIFO best c) LRU target, Clock approximates d) random → **c**
6. Re-anchor time budget? a) 5 min b) 45 min c) 4 h d) 2 h → **b**

## 20. Flashcards
- **Q: Crash course purpose?** → **A:** 45-minute full re-anchor of all 9 parts.
- **Q: Self-test?** → **A:** 10-second recall per cell, mark misses.
- **Q: Fix a miss?** → **A:** Reopen the section's Cheat Sheet/Revision/Flashcards.
- **Q: Key lines?** → **A:** shm needs sync; RAID ≠ backup; mutex vs semaphore; OPT/LRU/Clock.
- **Q: After the deck?** → **A:** Drill Section 01's Top-100 on weak parts.

## 21. Revision
The crash course compresses all 9 parts into a skimmable deck: core facts, key structures, classic algorithms, and trade-off lines, self-tested at 10 seconds per cell. Misses reopen the linked sections' compressed blocks (Cheat Sheet/Revision/Flashcards), and the whole pass costs ~45 minutes. Use it the night before, between rounds, or as a peer-quiz list — then back it with the Top-100 drill (Section 01) for delivery.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you use the crash course?" | 13 Q1 / 2 How |
| "Fastest way to re-anchor scheduling?" | 13 Q2 / 3 The Deck |
| "File systems re-anchor?" | 13 Q3 / 3 The Deck |
| "Page-replacement line?" | 13 Q4 / 8 Example |
| "IPC re-anchor in 60s?" | 13 Q5 / 3 The Deck |
| "Memory/virtual-memory re-anchor?" | 13 Q7–8 / 3 The Deck |
