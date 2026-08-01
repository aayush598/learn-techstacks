# Chapter: Thrashing and Advanced Virtual Memory

## What you'll learn
- **Thrashing**: the runaway condition where total working sets exceed RAM, so the system spends almost all its time on page faults — and its cure, the **working-set model**.
- **Advanced modern VM**: how Linux actually implements all of Part 07 — `kswapd`, the OOM killer, transparent huge pages, KSM, zswap/zram, memory compression, and tuning knobs.

## Prerequisites (linked)
- [Part 07 Chapter 01 Virtual Memory Basics](chapter-01-virtual-memory-basics/README.md) — demand paging, faults, working set.
- [Part 07 Chapter 02 Page Replacement Algorithms](chapter-02-page-replacement-algorithms/README.md) — replacement + frame allocation (thrashing is the allocation failure).

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Thrashing and Working Set Model](section-01-thrashing-and-working-set-model.md) | Why does a system collapse under memory pressure, and how do you detect and stop it? |
| 02 | [Advanced Virtual Memory in Modern OS](section-02-advanced-virtual-memory-in-modern-os.md) | How do Linux/Windows/macOS actually run VM in production? |

## One-paragraph narrative connecting all sections
Replacement algorithms and frame allocation (Chapter 02) assume memory pressure is manageable. When it isn't — the sum of all processes' working sets exceeds physical RAM — the system enters **thrashing**: every fault triggers an eviction that causes another fault, and CPU utilization collapses. Section 01 explains the phenomenon, the working-set model that measures each process's true need, and the two cures: suspend/swap a process or grow memory (and the modern "locality" tools that estimate working sets cheaply). Section 02 zooms out to production reality: Linux's `kswapd` background reclaim, the OOM killer as the last resort, THP/hugetlbfs, KSM dedup, zswap/zram compression, `madvise`/`mincore` hints, and the sysctls engineers tune — turning the textbook machinery into the systems you actually operate and interview about.

## Common interview trap in this chapter
**Trap:** Equating "high memory usage" with thrashing. Thrashing is specifically the *fault-dominant* state (CPU utilization *drops* while page-in/page-out dominates); you diagnose it via fault counters, not via `free`'s used bytes. Another: proposing "just buy more RAM" as the only fix — interviewers want the working-set/suspend/limit answer. And: "swap = slow, so disable it" — production systems use zswap/compression precisely to make swap survivable.

## Checklist before moving on
- [ ] I can define thrashing and explain why CPU utilization collapses.
- [ ] I can compute a working set from a reference string + window Δ.
- [ ] I can describe both thrashing cures (suspend/swap vs add frames).
- [ ] I can explain kswapd vs direct reclaim, and the OOM killer's role.
- [ ] I can discuss THP, KSM, zswap, swappiness, and when each is used.
