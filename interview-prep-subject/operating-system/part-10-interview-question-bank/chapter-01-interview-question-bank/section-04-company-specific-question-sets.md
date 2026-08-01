# Company-Specific Question Sets

> **TL;DR**: Different loops weight OS topics differently. **Systems-generalist** loops (Google, Amazon, Microsoft, Apple) spread across all parts with design prompts; **Linux/cloud-platform** teams (GCP, AWS, Cloudflare, Stripe infra, kernel-adjacent) weight Linux internals, IPC, and memory; **distributed-systems-leaning** loops (databases, storage) weight file systems, RAID/SSD, scheduling, and IPC at scale. This section maps loop flavor → high-yield topics + practice sets.

## 1. Why Does This Exist?
The Top-100 covers everything, but interview time is finite. A kernel engineer gets Linux-internals questions; a storage-engineer gets filesystem/RAID questions; a generalist gets a mix with design prompts. Tailoring practice to the target loop maximizes the expected value of study hours: the same hours buy the most relevant fluency. This section exists to (a) map company/team flavors to their weighted topics, (b) give a practice set per flavor, and (c) flag which parts deserve extra reps vs a skim.

## 2. How Does It Work?
For each loop flavor: **weighted topics** (which parts/sections matter most), **sample questions**, **the flavor's trap**, and **practice strategy**. Match your target (or, if unsure, train the generalist + your preferred flavor). Weights are relative — the generalist core (processes, sync, deadlock, memory, IPC) is universal; flavors shift the *tails*.

## 3. The Sets
**A. Systems-Generalist (Google, Amazon, Meta, Microsoft, Apple, Uber)**
- Weighted topics: Part 02 (process/thread), Part 03 (scheduling), Part 04 (sync), Part 05 (deadlock), Part 07 (virtual memory), Part 09 (IPC overview + syscalls), Part 10 Sec 02 (design).
- Sample questions: "Process vs thread?" "What is a deadlock / the 4 conditions?" "Design a scheduler." "What is copy-on-write?" "Compare IPC mechanisms."
- Trap: over-specializing into one part — the loop spans breadth + design.
- Strategy: drill Top-100 1–3, 4, 5, 7, 9–IPC; practice 2–3 design prompts (scheduler, filesystem, allocator).

**B. Linux / Cloud-Platform / Kernel-Adjacent (GCP, AWS Compute, Cloudflare, Stripe infra, Kubernetes SIGs, systems SaaS)**
- Weighted topics: Part 09 (Linux internals hard: fork/exec, syscalls, address space, kmalloc/vmalloc, context switch, namespaces/cgroups, /proc), Part 06/07 (memory + page tables), Part 08 (VFS, block layer), Part 04 (kernel sync: spinlock vs mutex, futex).
- Sample questions: "Walk through `fork`→`exec`." "What is a syscall / how are args passed?" "What is the Linux address space layout?" "kmalloc vs vmalloc?" "What is a cgroup and how do you limit CPU?" "What is the page cache?" "What is `strace` and how does it work?"
- Trap: knowing facts but not the *paths* (be ready to trace a syscall end-to-end and debug with `/proc`/`strace`).
- Strategy: Part 09 chapters 01–02 fully; Part 08 Sec 04 (VFS); Part 06/07 deep; run the type-a-command trace + a debugging walkthrough (Section 02 behavioral).

**C. Distributed-Systems / Storage / Databases (MongoDB, Redis, CockroachDB, RocksDB teams, S3/EBS teams, Snowflake)**
- Weighted topics: Part 08 (filesystems: allocation, journaling/CoW/LFS, VFS, RAID, SSD), Part 07 (mmap, page cache, working set), Part 09 (IPC: shm for caches, sockets for distribution), Part 05 (deadlock in distributed locks), Part 10 Sec 02 (design: "design an LSM / a key-value store / a replication log").
- Sample questions: "How does a log-structured filesystem work?" "Journaling vs CoW?" "Design an SSTable/LSM store." "How does `mmap` relate to a database buffer pool?" "What is write amplification?" "RAID 5 vs 10 for a database?" "How would you build IPC between storage nodes?"
- Trap: shallow filesystem depth — know ext4/XFS/btrfs + LFS/CoW well enough to discuss storage engines.
- Strategy: Part 08 all; Part 07 mmap/page-cache; Part 09 Sec 03 (shm) + Sec 05 (sockets); design drills on storage.

**D. Embedded / Real-Time / Safety-Critical (ARM, NVIDIA, automotive, robotics, RTOS roles)**
- Weighted topics: Part 03 (real-time scheduling: rate-monotonic, EDF, priority), Part 04 (sync: semaphores, priority inversion), Part 05 (deadlock in resource-constrained), Part 06 (MMU-less / partitioning), Part 09 (interrupts, context switch cost).
- Sample questions: "What is rate-monotonic scheduling?" "What is priority inversion and how do you solve it (priority inheritance/ceiling)?" "Semaphores vs mutexes in an RTOS?" "What is the context-switch cost and how do you minimize it?"
- Trap: desktop-Linux assumptions — RTOS priorities, deterministic latency, no virtual memory assumptions.
- Strategy: Part 03 RT sections + priority inversion (Part 04), resource ordering (Part 05), memory partitioning.

**E. Any loop, universal core**
- Weighted topics: Part 02 (processes/threads), Part 04 (sync), Part 05 (deadlock), Part 07 (virtual memory basics), Part 09 (IPC comparison) — always drilled.
- Sample questions: "Process vs thread?" "Mutex vs semaphore?" "4 deadlock conditions?" "Demand paging / page fault?" "Compare IPC."
- Strategy: these five are non-negotiable for every flavor.

## 4. Why Wasn't Another Approach Chosen?
- **Company-specific question leaks (rejected)**: interview questions aren't public-reproducible lists, and memorizing "what Google asked" ages out; the *flavor weighting* is stable and honest.
- **Everything-equally (rejected)**: finite study time — weighting by loop flavor raises the expected value.
- **One-size design prep (rejected)**: design prompts differ by domain (scheduler vs filesystem vs storage engine) — flavor-matched design drills beat a generic one.
- **Skipping the universal core (rejected)**: every flavor still asks the core five topics; flavor prep complements, never replaces, them.

## 5. Intuition
**A scout pre-hiking a trail**: you don't pack for all terrain equally — you match your pack to the trail (loop flavor): switchbacks need light gear (generalist = breadth), rocky scrambles need boots (Linux = internals), river crossings need waders (storage = filesystems). The core gear (boots, water) is universal — that's the core-five topics — and the flavor determines the extra gear.

## 6. Real-World Analogy
**A job posting's JD**: read the JD like a syllabus. A posting that says "deep Linux kernel experience" is the Linux flavor; "distributed storage" is the storage flavor; a general SWE role is the generalist. The company set is just mapping the JD keywords back to parts: kernel/process/syscall → Part 09, filesystem/storage/SSD → Part 08, scheduler/RT → Part 03.

## 7. Formal Definition
Company-specific prep = mapping a role/loop's emphasis onto the series' parts, producing a **weighted drill plan**: (1) universal core (parts 02, 04, 05, 07-basics, 09-IPC) always mastered; (2) flavor-weighted extensions (Linux internals for platform roles; filesystems/storage for DB roles; RT for embedded); (3) flavor-matched design prompts; (4) flavor-specific traps (tracing end-to-end, priority inversion, write amplification). The mapping is by *emphasis*, not by claims about any company's live question set.

## 8. Example
Target: **"Linux Platform Engineer, cloud infrastructure"** (flavor B).
- Drill plan: Part 09 chapters 01–02 (fork/exec/syscalls/address space/context switch/namespaces-cgroups) — the majority of prep; Part 08 Sec 04 (VFS); Part 06/07 (page tables, kmalloc/vmalloc, TLB); Part 04 kernel sync.
- Design prompts: "Design the process isolation for a multi-tenant container host" (namespaces + cgroups + seccomp), "Design a debugger for a hung process" (D-state, /proc, strace, perf).
- Trap to practice: being asked to *trace* rather than recite — drill "what happens when you type `ls`" and "what does `open` do" end-to-end.
Target: **"Senior Software Engineer, storage"** (flavor C).
- Drill plan: Part 08 all (allocation, journal/CoW/LFS, VFS, RAID, SSD); Part 07 (mmap, page cache); Part 09 shm.
- Design prompts: "Design an LSM-based key-value store" (memtable → SSTables → compaction → write amplification — directly built from LFS/CoW ideas), "Design a log-structured file system".
- Trap: discuss write amplification + journaling vs CoW trade-offs fluently.

## 9. Internal Working
1. Read the JD/posting; keyword-map to parts (kernel/syscall → 09; storage/SSD → 08; scheduler/real-time → 03; distributed → 07+09-IPC).
2. Pick the flavor set (A–D) + the universal core.
3. Build a weekly plan: core drill daily (30 min), flavor parts deep (60 min), design prompt 2×/week.
4. Do one "mock trace" per week (walk the type-a-command path for platform; walk an LSM write path for storage).
5. Review with Section 03's crash deck weekly; reweight if a round reveals a gap.

## 10. Time Complexity
- Core (parts 02, 04, 05, 07-basics, 09-IPC): ~1 hr/day for 1–2 weeks.
- Flavor A generalist: add design drills — ~30 min/day.
- Flavor B Linux: add Part 09 internals deep study — ~1.5–2 hrs/day.
- Flavor C storage: add Part 08 deep — ~1.5 hrs/day + design.
- Flavor D RT: add RT scheduling + priority inversion — ~1 hr/day.
- Total to loop-ready: 2–4 weeks depending on flavor depth.

## 11. Advantages
- **Focused study**: hours go to the topics the target loop actually weights.
- **Design alignment**: flavor-matched prompts (scheduler vs LSM vs isolation) train the right "design a…" shape.
- **Trap awareness**: knowing the flavor's likely trap (tracing, write amplification, priority inversion) prevents the common miss.
- **Universal core stays strong**: no flavor skips the essential five topics.

## 12. Disadvantages
- **Emphasis is heuristic**: actual questions vary by interviewer; the flavor map is a guide, not a guarantee.
- **Over-fitting risk**: a generalist who trains only Linux internals gets caught on a sync question; keep the core.
- **JD ambiguity**: vague postings make flavor selection uncertain — when unsure, train generalist + strongest adjacent flavor.

## 13. Interview Questions
1. **Q: How do you tailor OS prep to a loop?** A: Map the JD/role to a flavor: generalist (breadth + design), Linux/platform (internals, syscalls, namespaces/cgroups), storage/DB (filesystems, RAID, SSD, mmap), embedded/RT (RT scheduling, priority inversion) — then weight the core-five topics plus the flavor's deep parts and design prompts.
2. **Q: What's the universal core every loop asks?** A: Process vs thread (Part 02), mutex vs semaphore + bounded buffer (Part 04), deadlock conditions (Part 05), demand paging/page fault (Part 07), IPC comparison (Part 09 Sec 06) — drill these first, always.
3. **Q: What does a Linux/platform loop emphasize?** A: Part 09 internals (fork/exec trace, syscall mechanism, address space, kmalloc/vmalloc, context switch, namespaces/cgroups, /proc) + VFS (Part 08 Sec 04) + kernel sync (spinlock vs mutex, futex) — and the type-a-command trace.
4. **Q: What does a storage/DB loop emphasize?** A: Part 08 (allocation, journaling vs CoW vs LFS, VFS, RAID, SSD/TRIM), Part 07 (mmap, page cache, working set), shm + sockets (Part 09) — and design prompts like "design an LSM store".
5. **Q: What does an embedded/RT loop emphasize?** A: Part 03 real-time scheduling (rate-monotonic, EDF), priority inversion + priority inheritance/ceiling (Part 04), deterministic context-switch cost, resource-constrained memory — not desktop-Linux assumptions.
6. **Q: How do you prep design prompts per flavor?** A: Generalist: scheduler, filesystem, allocator, IPC. Linux: container isolation, process manager, debugger-for-hung-process. Storage: LSM store, log-structured file system, buffer pool. RT: hard-real-time scheduler.
7. **Q: How much time for flavor prep?** A: Core 1 hr/day + flavor depth 1–2 hrs/day for 2–4 weeks; reweight weekly using the crash deck (Section 03) and mock traces.
8. **Q: What's the biggest flavor trap for platform loops?** A: Reciting facts without tracing — be ready to walk "type a command" and `open`→VFS→block end-to-end with `/proc`/`strace` diagnostics.
9. **Q: What's the biggest flavor trap for storage loops?** A: Shallow filesystem depth — know ext4/XFS/btrfs, LFS/CoW, journaling, write amplification, RAID trade-offs enough to discuss storage engines.
10. **Q: What's the biggest flavor trap for RT loops?** A: Applying general-purpose scheduling ideas — RT asks for determinism: rate-monotonic schedulability, priority inversion solutions, bounded blocking.
11. **Q: What if the posting is generic?** A: Train the generalist core + design, then add one flavor you'd most likely hit (usually the team's domain); the core carries any loop.
12. **Q: How do you self-assess flavor readiness?** A: Do a "mock trace" per week (platform: type-a-command; storage: an LSM write path; RT: a priority-inversion scenario) and time your Top-100 answers on the weighted parts (Section 01).

## 14. Follow-Up Questions
1. **Q: What is the LSM (log-structured merge-tree) connection to OS?** A: It's a storage-engine pattern (memtable → SSTables → compaction) that borrows from log-structured filesystems — the "sequential writes + background compaction" idea from Part 08 Sec 04-03/03-03; knowing both is the storage-flavor differentiator.
2. **Q: How does `mmap` relate to a database buffer pool?** A: A buffer pool is essentially a managed page cache; `mmap` defers to the OS page cache (with fault costs), while databases often implement their own for control — the Part 07 mmap/page-cache trade-off in practice.
3. **Q: What is priority inheritance?** A: A low-priority task holding a lock boosts to the priority of the highest-priority waiter — fixing priority inversion (the Mars Pathfinder bug); the RT-flavor must-know (Part 04).

## 15. Coding Example
```c
// Flavor practice: implement the storage-flavor "write path" analog —
// a tiny LSM-like append + in-memory index (design drill made concrete).
#include <stdio.h>
#include <string.h>

#define N 8
typedef struct { char key[8]; int val; } rec_t;

int main(void) {
    rec_t memtable[N]; int n = 0;
    // append writes (like an LSM memtable)
    const char *keys[] = {"a", "b", "c", "d"};
    for (int i = 0; i < 4 && n < N; i++) {
        strcpy(memtable[n].key, keys[i]);
        memtable[n].val = i;
        n++;
    }
    // "compaction": scan in key order
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (strcmp(memtable[j].key, memtable[i].key) < 0) {
                rec_t t = memtable[i]; memtable[i] = memtable[j]; memtable[j] = t;
            }
    for (int i = 0; i < n; i++)
        printf("key=%s val=%d\n", memtable[i].key, memtable[i].val);
    return 0;
}
```
The point: storage-flavor prep means being able to *code* the concepts (append logs, compaction, sorted runs) not just describe them.

## 16. Industry Usage
- **Interview prep for systems roles** at FAANG, cloud providers, databases, and infrastructure companies — flavor mapping is standard coaching practice.
- **Team interviews / take-homes**: the same weighting applies to LLD/HLD rounds (design a scheduler/storage engine).
- **Mock interviews**: coaches match mock questions to the target loop's flavor.

## 17. References
- This series: the flavor sets map directly to parts 01–10 (weighted sections listed per set).
- Posting/JD keyword analysis (the standard prep method).
- Silberschatz/Tanenbaum/Love for depth within weighted parts.
- LSM/STAR references for storage/behavioral design drills.

## 18. Cheat Sheet
- Universal core: processes/threads, sync, deadlock, virtual memory basics, IPC comparison.
- Generalist (A): breadth + design (scheduler/filesystem/allocator/IPC).
- Linux/platform (B): Part 09 internals + VFS + kernel sync; trace end-to-end.
- Storage/DB (C): Part 08 + mmap/page cache + shm; design LSM/log-FS.
- Embedded/RT (D): RT scheduling, priority inversion/inheritance, determinism.
- Trap lines: "trace, don't recite" (B), "write amplification + journal vs CoW" (C), "priority inversion" (D).
- Prep: core 1 hr/day + flavor 1–2 hrs/day, 2–4 weeks.

## 19. Quiz
1. Universal core topics include? a) RAID b) sync + deadlock c) RT c) SELinux → **b**
2. Linux/platform loop weights? a) Part 09 internals b) music theory c) RAID 7 d) none → **a**
3. Storage loop's trap? a) tracing b) shallow FS depth c) RT d) nothing → **b**
4. RT loop must know? a) priority inversion b) LSM c) TRIM d) RAID → **a**
5. Design prompt for storage? a) scheduler b) LSM store c) container d) allocator → **b**
6. Generic posting strategy? a) only flavor b) core + design + one flavor c) skip core d) random → **b**

## 20. Flashcards
- **Q: Universal core?** → **A:** Processes, sync, deadlock, vmem basics, IPC.
- **Q: Platform flavor?** → **A:** Part 09 internals + VFS; trace end-to-end.
- **Q: Storage flavor?** → **A:** Part 08 + mmap/page cache; LSM design.
- **Q: RT flavor?** → **A:** Rate-monotonic, priority inversion/inheritance.
- **Q: Prep structure?** → **A:** Core 1 hr + flavor 1–2 hrs/day.
- **Q: Best self-assessment?** → **A:** Weekly mock trace (type-a-command / LSM write path).

## 21. Revision
Company-specific prep is a weighting exercise: map the role/JD to a loop flavor — systems-generalist (breadth + design), Linux/platform (internals, syscalls, namespaces/cgroups, VFS), storage/DB (filesystems, RAID/SSD, mmap, LSM design), or embedded/RT (rate-monotonic, priority inversion) — and always anchor on the universal core (processes, sync, deadlock, virtual memory basics, IPC). Each flavor has a trap to pre-empt (trace-don't-recite, shallow-FS-depth, write-amplification fluency, RT determinism). Practice 2–4 weeks with a core-daily + flavor-depth plan, weekly mock traces, and the Section 03 crash deck for reweighting. The flavor map is a guide, not a guarantee — but it reliably concentrates study where the loop concentrates its questions.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you tailor OS prep to a loop?" | 13 Q1 / 2 How |
| "What's the universal core?" | 13 Q2 / 3 The Sets (E) |
| "What does a Linux/platform loop emphasize?" | 13 Q3 / 3 The Sets (B) |
| "What does a storage/DB loop emphasize?" | 13 Q4 / 3 The Sets (C) |
| "What does an embedded/RT loop emphasize?" | 13 Q5 / 3 The Sets (D) |
| "How do you prep design prompts per flavor?" | 13 Q6 / 8 Example |
| "Biggest flavor traps?" | 13 Q8–10 / 3 The Sets |
| "How do you self-assess readiness?" | 13 Q12 / 9 Internal |
