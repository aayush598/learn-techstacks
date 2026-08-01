# Top-100 OS Questions and Answers

> **TL;DR**: The 100 highest-frequency OS interview questions, organized by part (01–09), each with a crisp, structured answer and a pointer to the deep section. Drill these until the structure (not just the fact) comes out automatically.

## 1. Why Does This Exist?
Interview questions are the *test* of everything in this series. Recruiters and interviewers reuse a small, high-frequency set: process/thread basics, scheduling, synchronization, deadlocks, memory, virtual memory, filesystems, IPC, Linux internals, and the "type a command" trace. This section collects them so you practice the **delivery**: a correct answer is table stakes — a *structured* answer (state the definition, give the trade-off, name the kernel detail) is what differentiates. Each entry lists the source part/section so you can re-anchor on a weak area.

## 2. How Does It Work?
The bank is organized by part. For each question: the **question**, the **answer** (1–4 lines, structured), and a **deep link** (part/section to review). Practice by: (1) cover the answer column, (2) answer aloud in ~60–90 seconds, (3) compare structure, (4) revisit weak sections.

## 3. The Questions
**Part 01 — OS Fundamentals** (source: part-01)
1. **What does an OS do?** Manages hardware and provides abstractions (processes, memory, files, I/O) with protection, scheduling, and resource accounting. Modern kernels are monolithic (Linux) or microkernel (Mach) hybrids.
2. **What is a system call vs a library call?** Syscall = privileged kernel entry (Part 09 Sec 04); library call = userspace wrapper (glibc `open()` → `syscall`). `strace` shows syscalls, `ltrace` shows libc.
3. **What is a context switch?** Switching CPU state (registers, page tables, kernel stack) between tasks (Part 09 Sec 05); a mode switch (syscall) stays in the same task.
4. **User mode vs kernel mode?** CPU privilege levels (ring 3 vs ring 0): kernel executes privileged instructions, touches hardware; user code is restricted and enters via syscalls/exceptions/interrupts.
5. **What is a kernel?** The core OS component always resident in memory handling syscalls, interrupts, scheduling, memory, and drivers. Monolithic (Linux/BSD) vs microkernel (only IPC+minimal; services in user space).

**Part 02 — Processes and Threads**
6. **Process vs thread?** Process = resource container (address space, fds, creds) + execution unit; thread = a unit of execution sharing the process's resources. Context switch between threads is cheaper (same address space).
7. **Process states?** New, Ready, Running, Waiting/Blocked, Terminated; Linux: TASK_RUNNING, INTERRUPTIBLE, UNINTERRUPTIBLE, STOPPED, ZOMBIE.
8. **What is a zombie / orphan?** Zombie = exited-but-unreaped (needs `wait`); orphan = parent died (reparented to PID 1/subreaper).
9. **What is fork?** System call creating a child via copy-on-write; child returns 0, parent gets child's pid (Part 09 Sec 01).
10. **What is exec?** Replaces the process image (new mm + entry) in place — no new process.
11. **User-level vs kernel-level threads?** User threads (green threads): scheduled in user space, fast, no kernel involvement, but one blocking syscall can block all; kernel threads: scheduled by the OS, preemptible per-thread. Modern Linux threads = kernel threads (clone).
12. **What is a thread pool?** Pre-created idle threads that process tasks from a queue — avoids per-task thread creation overhead; used by web servers, DBs.
13. **What is a stack vs a heap?** Stack: per-thread, LIFO, automatic (locals, call frames), grows down; heap: dynamic allocations via malloc/brk/mmap, grows up (Part 09 Sec 02).
14. **What is a PCB (task_struct)?** The process descriptor holding pid, state, scheduling info, mm, files, signal, creds (Part 09 Sec 01).

**Part 03 — CPU Scheduling**
15. **What is scheduling and why?** Deciding which ready task runs next to achieve fairness, low latency, high throughput, and bounded starvation.
16. **Preemptive vs non-preemptive?** Preemptive: scheduler can interrupt a running task (time slice, higher-priority arrival); non-preemptive: task runs until it blocks/yields.
17. **FCFS?** First-come-first-served: simple, convoy effect (a long job holds CPU).
18. **SJF / SRTF?** Shortest-job-first (non-preemptive) / shortest-remaining-time-first (preemptive): minimal average waiting time, but starvation and requires future knowledge.
19. **Round robin?** Time-sliced FCFS: fairness, but poor for CPU-bound vs I/O-bound mix without priority.
20. **Priority scheduling?** Higher-priority runs first; needs aging to prevent starvation; can combine with RR per level.
21. **Multilevel queue / feedback?** Multiple queues by process type (system/interactive/batch); feedback moves tasks between queues based on behavior — the classic adaptive scheme.
22. **What is the convoy effect?** A long first job delays all shorter jobs behind it (FCFS).
23. **What is starvation and aging?** A task never getting CPU; aging = increase priority over time to guarantee progress.
24. **What is the Linux CFS scheduler?** Fair scheduler using a red-black tree keyed by vruntime; leftmost runs; `nice` maps to weights (Part 09 Sec 01).
25. **What are sched classes?** SCHED_DEADLINE > RT (FIFO/RR) > CFS (fair) > IDLE.
26. **What is the difference between I/O-bound and CPU-bound?** I/O-bound bursts short, blocks often (latency-sensitive → high priority); CPU-bound computes long (throughput → RR).
27. **What is a quantum/time slice and why tune it?** The CPU time unit per run; too small → overhead, too big → poor responsiveness.

**Part 04 — Process Synchronization**
28. **What is a race condition?** Outcome depends on interleaving of concurrent accesses to shared state; fix with atomicity/locks.
29. **What is the critical section problem?** Ensuring mutual exclusion + progress + bounded waiting for code touching shared state.
30. **What are the three requirements?** Mutual exclusion (one at a time), progress (someone who wants in eventually gets in), bounded waiting (no infinite postponement).
31. **What is a mutex?** A lock with ownership (the holder unlocks); binary; protects critical sections.
32. **What is a semaphore?** A counting synchronization primitive (wait decrements/blocks at 0, signal increments) with no ownership (Part 09 Sec 04).
33. **What is the difference between a mutex and a binary semaphore?** Ownership: mutex can only be unlocked by its holder; semaphore can be signaled by any process — misuse allows double-signal bugs.
34. **What is a spinlock?** A busy-waiting lock (test-and-set/atomic) — fine for very short critical sections on multicore; wastes CPU under contention.
35. **What is a condition variable?** A wait/signal primitive paired with a mutex to wait for a predicate (producer-consumer slot).
36. **What is the producer–consumer (bounded buffer) problem?** Producer adds to a fixed buffer, consumer removes; solved with mutex + two counting semaphores (or CVs) — full/empty slots.
37. **What is the readers–writers problem?** Multiple readers OR one writer; solutions prioritize readers (starvation of writers) or writers.
38. **What is the dining philosophers problem?** N philosophers sharing N forks; must avoid deadlock + starvation (asymmetric pickup, one-at-a-time, or resource hierarchy).
39. **What are atomics / lock-free programming?** Operations that complete without interleaving (C++ `std::atomic`, CAS); used to avoid locks; need memory-ordering care.
40. **What is the compare-and-swap (CAS)?** An atomic primitive: if `*p == old`, set `*p = new`; basis of lock-free data structures.
41. **What is a futex?** Fast user-space mutex: atomic in user space, kernel syscall only on contention (Part 09 Sec 04).
42. **What is the difference between `mutex` and `spinlock` in the kernel?** Mutex sleeps (can block, uses scheduler), spinlock busy-waits (for tiny critical sections, interrupt-disabled contexts).

**Part 05 — Deadlocks**
43. **What is a deadlock?** A set of processes each holding a resource and waiting for another's, none can proceed.
44. **Four necessary conditions?** Mutual exclusion, hold-and-wait, no preemption, circular wait.
45. **How to prevent?** Break one condition: no hold-and-wait (acquire all at once), allow preemption, impose resource ordering (no circular wait).
46. **How to avoid?** Banker's algorithm (check safe states before granting) — needs known max claims.
47. **How to detect/recover?** Wait-for graph detection + cycle detection; recovery by process/resource preemption or killing.
48. **What is the Banker's algorithm?** Resource allocation avoiding unsafe states: only grant if the system remains safe (some sequence can finish).
49. **What is the difference between deadlock and starvation?** Deadlock = circular wait, no progress by anyone; starvation = a process never gets a resource (not necessarily circular).
50. **What is livelock?** Processes keep executing but make no progress (e.g., mutual retry loops) — like two people stepping around each other forever.
51. **How do databases avoid deadlock?** Lock ordering, timeouts, and deadlock detection (rollback of a victim transaction).

**Part 06 — Memory Management**
52. **Logical vs physical address?** Logical = as seen by the program (virtual); physical = actual RAM location; the MMU translates.
53. **What is the MMU?** Hardware translating logical→physical addresses via page tables/TLB.
54. **Contiguous allocation & its problem?** Partitioning memory into fixed/variable contiguous regions; suffers external fragmentation.
55. **What is fragmentation?** Internal = wasted space inside an allocation (rounded to block size); external = free gaps too small to use.
56. **What is compaction?** Moving allocated blocks together to consolidate free space (requires relocation; costly).
57. **What is paging?** Fixed-size pages (4 KB) mapped via page tables; no external fragmentation; internal fragmentation ≤ page size.
58. **What is a page table entry?** Contains page frame number + flags (valid, RW, user, dirty, accessed, NX) (Part 06/07).
59. **What is segmentation?** Variable-size segments (code/data/stack) by logical units; external fragmentation; segment tables.
60. **Paging + segmentation together?** Segments mapped to pages — Intel x86 style (Part 06 Sec 04).

**Part 07 — Virtual Memory**
61. **What is virtual memory?** Logical space larger than physical; demand paging brings pages in on fault; process isolation + shared memory + efficient code loading.
62. **What is demand paging?** Only load pages actually accessed; invalid pages cause page faults that load them.
63. **What is a page fault?** Access to a non-resident page → trap → OS loads/allocates → resume.
64. **What is copy-on-write?** Pages shared read-only until written, then duplicated (fork, `MAP_PRIVATE`).
65. **What is TLB and why does it matter?** Translation Lookaside Buffer — cache of page-table entries; a miss walks page tables (slow); TLB shootdown on flush (Part 06 Sec 02).
66. **Page replacement: FIFO, OPT, LRU, Clock?** FIFO = oldest in; OPT = future (unimplementable, benchmark); LRU = least-recently-used (approximated); Clock = second-chance approximation of LRU.
67. **What is Belady's anomaly?** FIFO can *increase* faults with more frames; OPT/LRU don't.
68. **What is thrashing?** Working set exceeds physical memory → constant faults, near-zero CPU use; controlled by working-set policy / locality.
69. **What is the working set model?** The pages a process currently needs (recently used); maintain WS > sum of working sets to avoid thrashing.
70. **What is the difference between `mmap` and `read`?** mmap maps file pages into the address space (page-cache-backed, zero-copy); read copies through the page cache (Part 09 Sec 03).
71. **What is the swap?** The backing store for evicted anonymous pages; `vm.swappiness` tunes eagerness.
72. **How does Linux find the victim page?** Page cache LRU lists (active/inactive), `vmscan`; anon vs file balancing.

**Part 08 — File Systems**
73. **What is a file system?** Structure + metadata + allocation + access control for persistent data on storage.
74. **Inode vs file name?** Inode = file metadata + block pointers; directory = name→inode mapping. Hard link = another name for the same inode; soft link = a path reference.
75. **Hard vs soft links?** Hard: same inode (same data), can't cross filesystems/dirs, no links to dirs; soft: separate inode containing a path, can cross, breaks if target moves.
76. **Contiguous / linked / indexed allocation?** Contiguous = fast sequential but external fragmentation; linked = no fragmentation but random access slow; indexed = index block per file (FAT vs inode designs).
77. **What is an extent?** `[start, len]` mapping a contiguous run — ext4/XFS use extents instead of block lists (Part 08 Sec 04-01).
78. **Free space management?** Bitmaps (ext4), B-trees (XFS), block lists.
79. **What is a journal?** A write-ahead log for crash-consistent metadata (JBD2, NTFS $LogFile); replay on mount (Part 08 Sec 04-03).
80. **What is copy-on-write FS (btrfs/ZFS)?** Never overwrite; flip root pointer; snapshots free + checksums.
81. **What is the VFS?** The kernel filesystem abstraction: super_block/inode/dentry/file/address_space + op vectors (Part 08 Sec 04-04).
82. **What is RAID 0/1/5/10?** Striping / mirroring / distributed parity (1 failure) / mirrored stripes (Part 08 Sec 03-02); RAID ≠ backup.
83. **What is TRIM and wear leveling?** TRIM: tell the SSD dead LBAs (less GC); wear leveling: spread erases evenly (Part 08 Sec 03-03).
84. **What is NTFS's MFT?** Master File Table — one record per file/dir with attributes (Part 08 Sec 04-02).

**Part 09 — IPC and Linux Internals**
85. **What is a pipe?** Unidirectional kernel-buffered byte stream; `pipe(2)` → two fds (read/write); FIFO = named pipe.
86. **Message queues: POSIX vs System V?** POSIX `mq_open/send/receive` (priority); System V `msgget/msgsnd/msgrcv` (key-based, type selection).
87. **Why is shared memory fastest?** Zero copies, zero syscalls after `mmap` — same physical pages; but no synchronization (Part 09 Sec 03).
88. **IPC semaphores vs mutex?** Semaphores: counting, no ownership, cross-process; mutex: ownership, binary.
89. **Unix domain sockets?** AF_UNIX: path-addressed, full-duplex, local; `socketpair` = bidirectional channel for related processes.
90. **Signals: what are they?** Async events interrupting a process; SIGKILL/SIGSTOP uncatchable; handlers must be async-signal-safe.
91. **What is a namespace?** Isolated view of a global (PID/net/mnt/UTS/IPC/user/cgroup); the container's isolation.
92. **What is a cgroup?** Hierarchical resource limits (CPU/memory/I/O) — the container's budget (Part 09 Sec 05).
93. **What is `fork` + `exec` + `exit` + `wait`?** Creation (COW), image replacement, termination (zombie), reaping (Part 09 Sec 01).
94. **What is the syscall mechanism?** `syscall` instr, `%rax` number, sys_call_table dispatch, `sysret`; vdso skips traps (Part 09 Sec 04).
95. **What is kmalloc vs vmalloc?** Phys-contiguous (direct map, fast) vs virtually-contiguous (scattered, large).
96. **What is the address space layout?** User: text/data/heap/mmap/stack; kernel: direct map (PAGE_OFFSET), vmalloc, vmemmap (Part 09 Sec 02).
97. **What is the page cache?** The `address_space`-backed cache of file pages — buffered I/O, readahead, write coalescing.
98. **What is `strace`?** ptrace-based syscall tracing (TIF_SYSCALL_TRACE) — shows number/args/result per syscall.
99. **What happens when you type a command?** Shell fork → COW; exec → ELF loader maps segments, `_start` → main; syscalls (openat/read/write); exit → zombie → wait (Part 09 Sec 05).
100. **What is the difference between a process and a thread in Linux?** Both are `task_struct`s; threads share mm/files/signal via `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD`.

## 4. Why Wasn't Another Approach Chosen?
- **Only definitions (rejected)**: definitions without the trade-off ("why", "when") fail the follow-up; every answer above includes the decision context.
- **Only deep code (rejected)**: too much for an interview answer; the deep sections are linked for when the interviewer pushes.
- **Only trivia (rejected)**: the bank is curated by frequency — the questions actually asked in OS loops, not a textbook dump.

## 5. Intuition
**A sparring partner**: you don't learn to box by reading the manual — you run rounds. Each question is one round: you state the move (answer), the opponent throws the follow-up (trade-off), you counter (kernel detail). The 100 questions are the opponent's most common punches; drilling them makes the defense automatic.

## 6. Real-World Analogy
**A bar exam's "most tested" list**: the bar-prep course doesn't teach every statute — it ranks the highest-yield topics and drills them. This bank is that ranking for OS interviews: the topics with the highest probability of appearing, with the exact shape of the expected answer.

## 7. Formal Definition
The bank is a curated mapping `{question → (structured answer, source part)}` covering: process/thread model (Part 02, 09), scheduling (Part 03, 09), synchronization (Part 04, 09), deadlock (Part 05), memory management (Part 06), virtual memory (Part 07), file systems (Part 08), IPC (Part 09), and Linux internals (Part 09). Effective practice: 90–120 second spoken answers, graded on *structure* (definition → trade-off → example/kernel detail), with weak areas re-anchored in the linked deep sections.

## 8. Example
Weak spot drill — "What is the difference between a mutex and a semaphore?"
1. **Definition**: mutex = ownership lock (binary, holder unlocks); semaphore = counting counter with wait/signal (no ownership).
2. **Trade-off**: semaphores express "N available" and work cross-process; no ownership means a double-signal bug is possible; mutexes catch misuse.
3. **Example**: bounded buffer uses a mutex + two counting semaphores (empty=N, full=0).
4. **Kernel detail**: on Linux, both are futex-backed in the uncontended fast path (Part 09 Sec 04).
Do this for every question in the bank.

## 9. Internal Working
1. Identify the weak topic (e.g., scheduling).
2. Open the source part's sections (Part 03 + Part 09 Sec 01) and re-read the "Formal Definition" and "Interview Questions" blocks.
3. Practice the bank's question aloud with the 4-step structure (definition → trade-off → example → kernel detail).
4. Repeat until the structure is automatic; then move to the system-design and company-specific sections.

## 10. Time Complexity
- Per-question drill: ~2 minutes spoken.
- Full bank first pass: ~3.5 hours (100 × 2 min) — split into daily sets.
- Re-drill of weak topics: ~30 min/day.
- Total to interview-ready: ~1–2 weeks at 1 hr/day.

## 11. Advantages
- **Frequency-weighted**: the questions actually asked.
- **Structured answers**: definition → trade-off → example → kernel detail — interview-ready delivery.
- **Self-diagnosing**: linked source sections turn every miss into a study target.
- **Portable**: the same structure works for verbal or written rounds.

## 12. Disadvantages
- **Answer recall ≠ interview success**: must add the framework (Section 02) and behavioral polish.
- **Frequencies vary by role**: a kernel team vs a generalist loop weights topics differently (Section 04 addresses this).
- **Stale risk**: interviewers increasingly ask open-ended "design a…" variants — covered in Section 02.

## 13. Interview Questions
1. **Q: How do you practice for an OS loop?** A: Drill the Top-100 with a 4-step spoken answer (definition → trade-off → example → kernel detail), self-diagnose weak topics, re-anchor in the deep sections, then practice design prompts (Section 02).
2. **Q: What's the most common OS question?** A: Process vs thread, and "what happens when you type a command" — both appear in most OS-flavored loops; know them cold.
3. **Q: What separates a good answer from a great one?** A: The trade-off and a concrete example/kernel detail. "A mutex is a lock" is weak; "a mutex has ownership (only the holder unlocks), unlike a semaphore which counts N resources and can be signaled by anyone — in the bounded-buffer I use a mutex plus two counting semaphores" is strong.
4. **Q: How do you handle a question you don't know?** A: Say what you do know, structure it (definition/analogy), and reason from first principles — the interviewer grades the thinking, not the recall.

## 14. Follow-Up Questions
1. **Q: Why does the interviewer ask "why" after "what"?** A: To test depth — the trade-off and the "when would you choose X" reasoning is the actual signal.
2. **Q: Should I memorize Linux kernel line numbers?** A: No — but naming the actual kernel structs/paths (task_struct, CFS vruntime, sys_call_table, PAGE_OFFSET) strongly signals real depth.

## 15. Coding Example
```c
// Drill template: every answer can be coded as (definition, tradeoff, example)
#include <stdio.h>
#include <string.h>

typedef struct { const char *def; const char *trade; const char *ex; } qa_t;

void answer(const char *q, qa_t a) {
    printf("Q: %s\n  1. Definition: %s\n  2. Trade-off: %s\n  3. Example: %s\n",
           q, a.def, a.trade, a.ex);
}

int main(void) {
    answer("mutex vs semaphore", (qa_t){
        "mutex = ownership lock (binary); semaphore = counting counter (wait/signal, no ownership)",
        "semaphores count N resources and work cross-process; no ownership risks double-signal; mutexes catch misuse",
        "bounded buffer: mutex + empty=N + full=0"});
    answer("page fault", (qa_t){
        "access to a non-resident page traps to the kernel",
        "demand paging trades fault latency for memory efficiency",
        "a lazy mmap'd page faults once, then stays resident"});
    return 0;
}
```

## 16. Industry Usage
- **Interview prep**: FAANG and systems-company loops (Google/Meta/Amazon/Apple/Microsoft, Stripe, Cloudflare, MongoDB) reuse this question set in OS/Systems rounds.
- **Study groups / mock interviews**: structured self-drill and peer grading.
- **Role-specific prep**: kernel/embedded/platform teams weight the Linux internals + memory + sync questions higher (Section 04).

## 17. References
- Silberschatz, *Operating System Concepts* (the canonical answers source).
- Tanenbaum, *Modern Operating Systems*.
- Love, *Linux Kernel Development* (Linux-specific depth).
- This series: parts 01–09 (each question links to its deep section).
- `man` pages and Linux kernel docs for the internals questions.

## 18. Cheat Sheet
- 4-step answer: definition → trade-off → example → kernel detail.
- Highest-frequency: process/thread, type-a-command, deadlock conditions, page replacement, IPC comparison.
- Always name the kernel detail (task_struct, CFS vruntime, futex, PAGE_OFFSET, sys_call_table).
- Trade-offs are the signal — never answer with a definition alone.
- Drill aloud, 90–120 s, daily sets.

## 19. Quiz
1. The strongest answer format is? a) definition only b) definition → trade-off → example → kernel detail c) code only d) analogy → **b**
2. Which question appears in most OS loops? a) define DRAM b) type-a-command c) RAID 7 d) TLB size → **b**
3. A good follow-up test is? a) "what" b) "why / when" c) trivia d) yes/no → **b**
4. Kernel depth is shown by? a) line numbers b) structs/paths c) version numbers d) lore → **b**

## 20. Flashcards
- **Q: Answer structure?** → **A:** Definition → trade-off → example → kernel detail.
- **Q: Most common question?** → **A:** Process vs thread; type-a-command trace.
- **Q: What's graded?** → **A:** The reasoning and trade-off, not recall.
- **Q: How to handle unknown?** → **A:** Structure + first-principles reasoning.
- **Q: Deep link on miss?** → **A:** Re-read the source part's Formal Definition + Interview Questions blocks.

## 21. Revision
The Top-100 is the drill set for the entire OS series: 10 questions per part, each with a structured answer (definition → trade-off → example → kernel detail) and a deep link. Drill aloud in 90–120 s chunks, self-diagnose, re-anchor weak topics in the source sections, then layer on the design frameworks (Section 02) and company-specific weighting (Section 04). The bank is the sparring partner; the deep sections are the coach — and both are needed for a strong OS loop.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you practice for an OS loop?" | 13 Q1 / 2 How |
| "What's the most common OS question?" | 13 Q2 / 3 The Questions |
| "What separates good from great?" | 13 Q3 / 8 Example |
| "How do you handle an unknown question?" | 13 Q4 / 5 Intuition |
| "Why does the interviewer ask why?" | 14 Q1 / 4 Why not |
| "Should I memorize kernel details?" | 14 Q2 / 18 Cheat Sheet |
