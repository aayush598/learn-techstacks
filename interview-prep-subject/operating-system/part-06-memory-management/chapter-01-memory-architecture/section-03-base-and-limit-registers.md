# Base and Limit Registers

> **TL;DR**: The **base and limit registers** are the simplest memory-protection hardware: the OS loads a process's start address and size into two registers, and the MMU rejects (faults) any access outside `[base, base+limit)` — cheap and fast, but requires contiguous physical memory and was superseded by paging.

## 1. Why Does This Exist?
In the earliest multiprogramming systems, the OS needed a way to keep process A from reading/writing process B's memory *without* an expensive software check on every instruction. Base and limit registers exist as the minimal hardware answer: a process can only ever legally touch memory in one contiguous window, defined by two registers. Because the check is done in hardware on *every* memory access, protection is both complete and free (one add + one compare). It's the historical bridge from "one process owns all RAM" to "many processes share RAM safely."

## 2. How Does It Work?
The OS assigns each process a contiguous region of physical memory `[base, base+size)`. It stores `base` in the **base register** and `size` (or base+size) in the **limit register**. These are privileged registers — only the kernel can load them, and it does so on every context switch. On each memory access:
1. CPU produces a logical address.
2. The MMU compares: if `logical ≥ limit`, raise a trap (protection fault) → kernel kills the process (SIGSEGV).
3. Otherwise, physical address = `base + logical`.

The mapping is therefore a *single translation rule per process*, identical for all addresses — a pure offset.

## 3. When Is It Used?
- **Classic UNIX (V6/V7), early MS-DOS extenders**: the standard protection scheme for real-time and first-generation Unix before hardware paging was cheap.
- **Microcontrollers without an MMU**: ARM Cortex-M parts (STM32) often use MPU (Memory Protection Unit) with base/limit-like regions to isolate tasks in bare-metal or FreeRTOS/Tock.
- **Real-time and safety-critical systems** (AUTOSAR, DO-178C): deterministic, predictable protection without page-fault handling complexity.
- **As a teaching device**: every OS textbook introduces it because it makes the concept of logical→physical + hardware protection concrete before paging.
- **Some hypervisor/TEE primitives**: e.g., initial memory-region checks before paging is enabled.

## 4. Why Wasn't Another Approach Chosen?
- **No protection at all**: obviously unsafe — rejected.
- **Software address checking (in compiler-generated code)**: every load preceded by compare → 2-3× slowdown and impossible for hand-written asm. Rejected for speed.
- **Two base/limit pairs (code + data)**: slightly better, but still one big contiguous block each — doesn't fix fragmentation.
- **Segmentation with many segments (Intel 8086)**: more flexible but 64 KB segments with 20-bit addresses were awkward; later combined with paging (Part 06 Ch. 04).
- **Paging (the real successor)**: fixed-size pages eliminate *external* fragmentation, allow non-contiguous placement, and enable virtual memory. The base/limit idea survives *inside* paging (each page maps a 4 KB "region"), but a single contiguous window was too restrictive — that's why paging replaced it on all general-purpose CPUs.
- **Memory protection keys (PKU)**: faster than full paging for *region isolation* but needs paging underneath; base/limit can't offer page-level permissions or sharing.

## 5. Intuition
The base register is the "seat number of the first row" and the limit is "how many rows your section has." You're told your seats are rows 20–30. Every seat you try to sit in, the usher checks "is it in your rows?" and refuses otherwise. Your ticket doesn't know the stadium's full layout — the usher (MMU) maps "my row 3" to "actual row 22."

## 6. Real-World Analogy
A prepaid phone plan with a data cap: the plan says "you get 10 GB starting from the day you activate" (base) and "up to 10 GB total" (limit). Every byte you use, the provider checks "still within the 10 GB?" and cuts you off at the cap. Move to a new phone/number? The carrier just changes your start date and cap — your usage pattern (logical addresses) stays the same.

## 7. Formal Definition
Base and limit registers are two CPU control registers used for address translation and protection in contiguous memory allocation. The **base register** holds the smallest legal physical address of a process; the **limit register** holds the size (or largest legal address). An address is valid iff `logical < limit`; the physical address is computed as `physical = base + logical`. They are privileged, reloaded on every context switch, and protect the OS itself (which lives outside the window) from the process and vice versa.

## 8. Example
Two processes and 64 KB of RAM (0x00000–0xFFFFF is 1 MB in this example's units; use KB for simplicity):
- Process A: placed at 0x00000, size 0x2000 (8 KB) → base=0x0000, limit=0x2000.
- Process B: placed at 0x20000, size 0x3000 (12 KB) → base=0x20000, limit=0x3000.

Context switch to B, then B executes `LOAD R1, 0x1000`:
- 0x1000 < 0x3000 ✓ → physical = 0x20000 + 0x1000 = 0x21000. OK.
- B executes `LOAD R1, 0x3500`: 0x3500 ≥ 0x3000 ✗ → MMU trap → kernel sends SIGSEGV. B's 0x3500 would have landed at 0x23500 — inside C's memory if C lived there — but the hardware prevented it.

Now suppose A needs to grow by 4 KB. If the region above A is occupied, A cannot grow in place → must be swapped/moved (external fragmentation, Part 06 Ch. 02).

## 9. Internal Working
1. Kernel scheduler picks process P.
2. Kernel (privileged) loads P's base and limit into the MMU registers (on x86-64-class CPUs, this concept lives in the paging layer instead; base/limit survives on MPU-class parts).
3. For the process's lifetime, every address is checked against the limit and offset by the base — no kernel involvement on the hot path.
4. On an invalid access, the MMU raises a *protection fault*; the CPU traps to the kernel's fault handler, which checks whether the faulting address is a legal future access (no — base/limit can't be extended on the fly without relocation) and terminates the process.
5. On context switch out, the registers are saved with the rest of the context (in the PCB) and overwritten by the next process's values.

## 10. Time Complexity
- Per-access translation + check: **O(1)** — one add + one compare, fully in hardware.
- Context switch register reload: **O(1)**.
- Process placement (finding a free window): O(n) over free-list entries (first/best/worst fit).
- **Relocation is O(1)** (change base register) but **swap-in/out is O(size)** because the whole contiguous block must move.
- External fragmentation management (compaction) is O(total-memory) to relocate everything.

## 11. Advantages
- Extremely simple and cheap — no page tables, no multi-level walks, no TLB (translation is trivial).
- Protection is complete and hardware-enforced on every access.
- Deterministic: no page-fault handling paths; predictable worst-case latency (great for RTOS).
- Relocation (move a process) is a single register write when there's a free window.
- Small memory overhead: just two registers.

## 12. Disadvantages
- Requires **contiguous physical memory** per process → **external fragmentation**; free RAM is chopped into useless holes.
- A process **cannot grow** beyond its limit without relocation (copy to a bigger window).
- No **sharing** — two processes can't share one library (except by loading it inside each window, wasting memory).
- No fine-grained permissions (no r/w/x per region, no NX).
- Coarse granularity: protection is a single window, not per-page; a bug anywhere in the process can address the whole window.
- No support for virtual memory, demand paging, or sparse address spaces.

## 13. Interview Questions
1. **Q: What are base and limit registers and what do they protect against?** A: Two privileged registers defining a process's contiguous legal memory window `[base, base+limit)`; the MMU rejects any access outside it, protecting other processes and the OS from a buggy/malicious process.
2. **Q: When is an address valid under base/limit?** A: When `logical < limit`; the physical address is then `base + logical`. Access ≥ limit → protection fault.
3. **Q: Why did paging replace base/limit?** A: Base/limit needs contiguous RAM (external fragmentation), forbids growth, allows no sharing or per-page permissions, and can't support virtual memory. Paging keeps hardware protection but with fixed 4 KB units that can be scattered anywhere.
4. **Q: How is the OS itself protected from a process? (Tricky)** A: The OS lives outside every process's window (above `base+limit` for the user process; the OS's own window is separate), and the limit check makes any user access to kernel memory fault.
5. **Q: What must the kernel do on a context switch?** A: Save the outgoing process's base/limit in its PCB and load the incoming process's values — otherwise the new process inherits the wrong window.
6. **Q: Can a process running under base/limit be moved while it runs? (Scenario)** A: Not without stopping it: relocation requires changing the base register, which the kernel does during a context switch — so the process is moved *between* runs, never mid-instruction.
7. **Q: Where do base/limit-style ideas survive in modern CPUs?** A: In MPU-equipped microcontrollers (ARM Cortex-M), TEEs, and conceptually as the offset+size in each page-table entry — and in LAM/SDI-style region checks; plus every region-based memory-safe scheme (e.g., checked segment bounds).
8. **Q: What is external fragmentation in the base/limit world?** A: As processes terminate, free memory becomes scattered holes; a new process with size S may find no *single contiguous* hole ≥ S even though total free memory ≥ S. Requires compaction or swapping.
9. **Q: Why is swap cost O(size) here but not under paging?** A: With base/limit you must move the entire contiguous image on swap in/out. With paging you move only the pages actually needed (demand paging, Part 07) — much cheaper for large processes.
10. **Q: How does the OS choose which hole to place a process in? (Production)** A: First-fit (fastest, leaves large tail holes), best-fit (smallest adequate hole — but slow and creates tiny fragments), worst-fit (largest hole — but destroys big windows). First-fit with a free-list is the common choice.
11. **Q: What happens if a process tries to grow beyond its limit?** A: The allocation fails; the OS must either terminate, swap out to relocate into a larger hole, or — with base/limit alone — you simply cannot grow in place. This is a core reason for demand paging.
12. **Q: Is base/limit "virtual memory"?** A: No — the entire process must be resident; there's no demand loading, no paging, no oversubscription. It's *relocation + protection* only, the precursor to VM.
13. **Q: What's the difference between an MPU and an MMU? (Tricky)** A: An MPU only *checks* permissions against configured regions (no translation); an MMU *translates* and checks. MPU = base/limit generalized to many regions; MMU = paging. Cortex-M uses MPUs; Cortex-A uses MMUs.
14. **Q: If base/limit is so limited, why do we still teach it?** A: It isolates the essential idea — hardware-enforced address-range protection — with minimal complexity, and its failure modes (fragmentation, no sharing) motivate everything that follows: paging, segmentation, and virtual memory.

## 14. Follow-Up Questions
1. **Q: Can base and limit be used for the kernel's own memory?** A: Historically yes (kernel in its own window); modern kernels are paged like users. The kernel's window was placed outside user windows so user processes couldn't reach it.
2. **Q: What is the relationship between the base+limit check and a page-table walk?** A: A page table is "base/limit per 4 KB chunk" — every page entry effectively says "this page maps to frame X with these permissions." Paging generalizes the window to thousands of tiny windows.
3. **Q: How do JITs/WebAssembly deal with the no-fine-granularity problem?** A: They use guard pages and sandboxing (linear memory + bounds checks), effectively re-implementing base/limit *in software* inside paged address spaces.

## 15. Coding Example
```c
// Simulate base/limit protection with a context-switch reload
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct { uint32_t base, limit; } Region;

static Region current;

void set_region(Region r) { current = r; }         // kernel-only, context switch

bool translate(Region *r, uint32_t logical, uint32_t *phys) {
    if (logical >= r->limit) return false;          // hardware compare -> fault
    *phys = r->base + logical;                      // hardware add
    return true;
}

int main(void) {
    Region A = { .base = 0x00000, .limit = 0x2000 };
    Region B = { .base = 0x20000, .limit = 0x3000 };
    set_region(A);                                  // run A
    uint32_t phys;
    printf("A[0x1000] -> %s\n",
           translate(&current, 0x1000, &phys) ? "0x01000 (ok)" : "fault");
    set_region(B);                                  // context switch to B
    printf("B[0x1000] -> %s\n",
           translate(&current, 0x1000, &phys) ? "0x21000 (ok)" : "fault");
    printf("B[0x3500] -> %s\n",
           translate(&current, 0x3500, &phys) ? "mapped" : "FAULT (SIGSEGV)");
    return 0;
}
```

## 16. Industry Usage
- **Classic Unix**: V6/V7 used base+limit-style relocation registers in the PDP-11 MMU (8 segment pairs — an early "many base/limit regions" design).
- **Microcontrollers**: ARM Cortex-M MPU supports 8–16 programmable regions (base + size + permissions) used by Zephyr, FreeRTOS+MPU, Tock, and safety-certified bare-metal.
- **TEEs**: ARM TrustZone and Intel SGX define memory regions the CPU enforces with base/limit-style semantics before paging/hardware-enforced isolation.
- **Hypervisors**: initial low-memory layout uses region checks before enabling paging.
- **Education + legacy**: still the textbook exemplar for memory protection.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.1.1 "Address Binding", 8.1.2 "Logical vs Physical", Figure 8.2 (base/limit).
- Tanenbaum, *Modern Operating Systems (4th ed.)*, Ch. 3.1 "No Memory Abstraction", 3.2 "Address Spaces".
- Dennis & Van Horn, *Programming Semantics for Multiprogrammed Computations* (1966) — the early model of memory protection.
- ARM Cortex-M3 Devices Generic User Guide: "Memory Protection Unit".
- Zephyr RTOS docs: "Memory Protection".

## 18. Cheat Sheet
- Valid address iff `logical < limit`; physical = `base + logical`.
- Two privileged registers; OS loads them on every context switch.
- Protection fault on out-of-range → kernel kills process.
- Requires contiguous memory → external fragmentation.
- Can't grow in place; no sharing; no per-page permissions; no VM.
- O(1) per access; O(1) relocate; O(size) swap.
- MPU = many base/limit regions; MMU = paging; Cortex-M vs Cortex-A.
- The "one window per process" idea → paging = thousands of tiny windows.

## 19. Quiz
1. A base/limit access is legal iff:
   a) base ≤ logical b) logical < limit c) base+logical < limit d) logical > base → **b**
2. Who loads the base/limit registers?
   a) the process b) the kernel, on context switch c) the MMU d) the compiler → **b**
3. An out-of-range access causes:
   a) TLB miss b) a protection fault/SIGSEGV c) swap-out d) a cache flush → **b**
4. Base/limit causes which problem?
   a) internal fragmentation b) external fragmentation c) deadlock d) thrashing → **b**
5. Why did paging replace base/limit?
   a) paging is simpler b) paging removes external fragmentation and adds VM c) paging is slower d) paging needs no hardware → **b**
6. An MPU is to an MMU as:
   a) check is to translate b) translate is to check c) cache is to memory d) none → **a**

## 20. Flashcards
- **Q: What is the validity condition under base/limit?** → **A:** logical < limit; physical = base + logical.
- **Q: When are the registers loaded?** → **A:** On every context switch, by the kernel (privileged).
- **Q: Main drawback of base/limit?** → **A:** External fragmentation — contiguous memory required, no growth, no sharing.
- **Q: What replaced it?** → **A:** Paging — thousands of tiny per-page base/limit windows.
- **Q: Where does the idea survive?** → **A:** ARM Cortex-M MPUs, TEEs, and per-page PFN+permissions in page tables.

## 21. Revision
Base/limit registers give each process one contiguous legal window: the MMU adds the base and checks the limit on every access, trapping to the kernel (SIGSEGV) on violation — O(1), fully hardware-enforced, and privileged. The OS reloads them per context switch. Because the window must be contiguous, free memory fragments (external fragmentation), processes can't grow or share, and there's no per-page permission or virtual memory — which is exactly why general-purpose CPUs moved to paging, where every 4 KB page is effectively its own tiny base/limit window with its own permissions.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are base and limit registers?" | 2 How / 7 Formal |
| "When is an address valid?" | 8 Example / 13 Q2 |
| "Why did paging replace base/limit?" | 4 Alternative / 13 Q3 |
| "What is external fragmentation?" | 8 Example / 13 Q8 |
| "How does context switching interact with base/limit?" | 9 Internal Working / 13 Q5 |
| "What's an MPU vs an MMU?" | 13 Q13 / 16 Industry Usage |
