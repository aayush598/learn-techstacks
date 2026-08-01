# Chapter: Page Replacement Algorithms

## What you'll learn
- **Page replacement fundamentals**: why the OS must evict pages when frames run out, and the evaluative metrics (fault rate, Belady's anomaly).
- **FIFO and Optimal**: the simplest algorithm and the provably-optimal oracle — and why Optimal is unreachable.
- **LRU and its approximations**: true LRU vs how real systems fake it (aging).
- **Clock and LFU**: the classic second-chance algorithm and frequency-based replacement — the practical and production choices.
- **Frame allocation**: how many frames each process gets (equal/proportional), and how allocation interacts with the algorithms.

## Prerequisites (linked)
- [Part 07 Chapter 01 Virtual Memory Basics](chapter-01-virtual-memory-basics/README.md) — demand paging and page faults (what replacement is *for*).
- [Part 06 Chapter 03 Paging](part-06-memory-management/chapter-03-paging/README.md) — frames, PTEs, accessed/dirty bits.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Page Replacement Fundamentals](section-01-page-replacement-fundamentals.md) | What problem does replacement solve, and how do we judge an algorithm? |
| 02 | [FIFO and Optimal Replacement](section-02-fifo-and-optimal-replacement.md) | The simplest and the theoretically-perfect algorithms. |
| 03 | [LRU and Approximations](section-03-lru-and-approximations.md) | Why LRU is the reference standard and how systems approximate it. |
| 04 | [Clock and LFU Replacement](section-04-clock-and-lfu-replacement.md) | The practical Clock algorithm and frequency-based LFU. |
| 05 | [Frame Allocation Strategies](section-05-frame-allocation-strategies.md) | How frames are divided among processes and the thrashing boundary. |

## One-paragraph narrative connecting all sections
When demand paging fills all frames, the next fault forces a choice: evict one page to make room. Section 01 frames the problem (the "fault rate" metric, the notion of optimality, and why eviction must consider future use). Section 02 covers the two anchors: FIFO (O(1), but suffers Belady's anomaly — more frames can mean more faults) and Optimal (provably minimal faults, impossible to implement — the theoretical yardstick). Section 03 introduces LRU, which approximates Optimal via recency but is too expensive to implement exactly at scale. Section 04 delivers the production answer: the **Clock algorithm** (LRU-ish with a hardware reference bit, O(1)) and LFU (frequency-based), which real OSes (Linux's variants, Windows, macOS) actually use. Section 05 ties allocation to correctness: how many frames per process (equal/proportional/minimum) determines whether the system thrash-boundaries hold — the bridge to Chapter 03 (thrashing).

## Common interview trap in this chapter
**Trap:** Assuming "more frames is always better." Belady's anomaly shows FIFO can get *worse* with more frames (LRU and stack algorithms never do — a key interview distinguisher). Also, students answer "LRU" as if it were cheap — real systems use Clock/aging approximations because exact LRU needs per-access timestamp updates. And "Optimal" is not a candidate for production; it's the theoretical lower bound used to evaluate others.

## Checklist before moving on
- [ ] I can simulate FIFO, Optimal, LRU, and Clock by hand on a reference string.
- [ ] I can explain Belady's anomaly and which algorithms avoid it (stack property).
- [ ] I can explain how the hardware reference bit makes Clock practical.
- [ ] I can compute the fault count for a given string and frame count.
- [ ] I can explain equal vs proportional allocation and the minimum-frames argument.
