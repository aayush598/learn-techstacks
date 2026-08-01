# Segmentation In Depth

> **TL;DR**: Segmentation gives each region of a program (code, data, stack) its own variable-size segment with independent base, limit, and permissions, addressing as `(segment, offset)` — a programmer-friendly model that paging lacks, but one that suffers external fragmentation because segments vary in size.

## 1. Why Does This Exist?
Paging treats all memory as uniform 4 KB units — but a program isn't a flat blob: it has code (read-only, executable), data (grows), and a stack (grows downward), each with different needs and protection. Segmentation exists to model this reality: give each logical unit its own region with its own base, limit, and access rights, so that (1) the compiler/programmer can think in "segments" matching their code, (2) each segment grows independently, (3) sharing is by *meaningful unit* (share all of libc's code segment, not an arbitrary page range), and (4) protection is expressed naturally ("code is read/execute, stack is read/write"). It was the dominant idea on classic machines (Burroughs, Multics, Intel 8086/x86-32) precisely because it matches how humans organize programs.

## 2. How Does It Work?
A logical address is split into **segment number S** and **offset d**:
- The **segment table** (array indexed by S) holds per-segment entries: **base** (physical start), **limit** (size), and **permissions** (read/write/execute).
- Translation: `if d < limit[S]: physical = base[S] + d; else → fault`.
- Each process has its own segment table (pointer in a control register); the OS loads/switches it per context switch.
- Segments are variable-size; a process can have a handful (code, data, stack, extra) rather than millions of pages.

## 3. When Is It Used?
- **Legacy & embedded**: Intel 8086/80286 real/protected mode, early x86-32 protected mode; many microcontrollers' MPUs define "regions" semantically similar to segments.
- **Modern relics**: x86-64 keeps CS/DS/SS (flat base-0), FS/GS for TLS and kernel percpu; Windows uses FS for TEB (thread environment block).
- **Multics/classic**: the textbook realization with ring-based protection (rings 0–7).
- **OS-internal "segments"**: modern Linux splits each process into VMAs (virtual memory areas) — semantically segments — and *implements* them with paging. The concept lives on in software.

## 4. Why Wasn't Another Approach Chosen?
- **Pure paging (chosen instead)**: uniform pages solve fragmentation and simplify hardware but lose program structure, natural sharing-by-whole-unit, and per-segment growth. Modern systems pick paging *and* emulate segments in software (VMAs).
- **Pure segmentation (rejected)**: variable segment sizes → external fragmentation (Chapter 02's problem returns); segment tables + compaction are complex; and per-segment protection requires *many* table entries.
- **Base/limit (rejected)**: one window per process — no structural granularity at all.
- **Combined segmentation + paging (Intel x86-32)**: keeps both — but the two-stage translation (segment → linear → page) is slow and complex; x86-64 dropped the segment stage for speed.
- **Overlays (rejected)**: manual segment swapping by the programmer — the worst of all worlds.

## 5. Intuition
A program is a building with distinct rooms: the lobby (code), storage (data), and an elevator that grows upward/downward (stack). Paging treats it as a brick wall where every brick is the same. Segmentation treats it as rooms with their own doors (bases), capacities (limits), and access rules ("staff only" for the code room). To reach room "Data, shelf 5," you find the Data room's door and walk 5 shelves in — that's `(segment, offset)`.

## 6. Real-World Analogy
A storage warehouse organized by numbered aisles (segments): Aisle 1 = inventory, Aisle 2 = returns, Aisle 3 = shipping. Each aisle has a marked length (limit) and rules (only authorized staff in Aisle 1). To fetch something you say "Aisle 2, slot 41" — the floor plan tells you where Aisle 2 starts (base) and its length; if slot 41 exceeds the aisle's length, the request is rejected (fault). Shipping (processes) can expand an aisle by renting adjacent space — but the warehouse is contiguous, so expanding one aisle may require moving another (external fragmentation).

## 7. Formal Definition
Segmentation is a memory-management scheme in which each process's logical address space is divided into a set of independent, variable-size regions called **segments**, each with its own base address, limit (size), and access-permission attributes, referenced by a **segment number** and **offset**. A **segment table** maps segment numbers to `(base, limit, permissions)`; translation is `physical = base + offset` subject to `offset < limit`. Because segments are variable-size, free memory must be managed with variable-size holes, leading to external fragmentation.

## 8. Example
Process P's segment table:
| Segment | Base (physical) | Limit | Permissions |
|---|---|---|---|
| 0 (code) | 0x1000 | 0x800 | read/exec |
| 1 (data) | 0x9000 | 0x400 | read/write |
| 2 (stack) | 0xE000 | 0x200 | read/write |

Accesses:
- `LOAD (1, 0x123)` → 0x123 < 0x400 ✓ → physical = 0x9000 + 0x123 = 0x9123. OK.
- `STORE (1, 0x123)` → allowed (rw). OK.
- `LOAD (0, 0x10)` → OK → 0x1010, but `STORE (0, 0x10)` → code is read/exec → **protection fault**.
- `LOAD (2, 0x250)` → 0x250 ≥ 0x200 → **limit fault** → SIGSEGV.

The stack segment can grow by enlarging its limit (if adjacent space is free) — growing *one* segment doesn't disturb code or data. Under paging, growing the stack means mapping more pages — also fine, but the *semantic grouping* is invisible to the allocator.

## 9. Internal Working
1. **Context**: process's segment-table base register (e.g., x86 LDTR/GDTR for system segments) is set at switch.
2. **Access**: CPU produces `(S, d)`.
3. **Lookup**: fetch segment-table entry `seg[S]` (base, limit, perms).
4. **Check**: `d < limit`; access type (read/write/exec) matches perms; supervisor vs user.
5. **Translate**: `physical = base + d` → memory bus.
6. **Fault**: on limit or permission violation → #GP (general-protection) / segmentation fault; the OS terminates or (rarely) handles it.
7. **Growth**: OS grows a segment by finding a larger hole, copying the segment, updating the table — the contiguous-allocation dance returns.

## 10. Time Complexity
- Translation (hit, no paging): **O(1)** — base+limit from a register-cached entry.
- Segment-table lookup: O(1) index into array.
- External-fragmentation management: same as Chapter 02 — O(n) free-list, O(total memory) compaction.
- Segment growth: O(segment size) copy if relocation required.
- Segmentation + paging (x86-32): segment stage O(1) + page walk O(3) — two extra steps vs pure paging.

## 11. Advantages
- **Structural**: code/data/stack share the *programmer's* mental model.
- **Independent growth** and per-segment protection (rwx per segment).
- **Natural sharing**: share a whole segment (all of libc's code) by pointing two segment tables at the same base.
- **No internal fragmentation** (unlike fixed partitions / paging's last page) — segments are exact.
- Clear **modularity** for linkers/loaders (each library a segment).

## 12. Disadvantages
- **External fragmentation**: variable sizes → holes; needs compaction.
- **Compaction is costly/risky** and needs run-time binding.
- Two-stage hardware complexity if combined with paging (x86-32).
- Requires the compiler/hardware to generate `(segment, offset)` addresses — burdens the toolchain.
- No demand paging for free (segments are swapped wholesale unless combined with paging).
- Modern CPU vendors (x86-64, ARM64) dropped it from the canonical path — segments became a compatibility footnote.

## 13. Interview Questions
1. **Q: What is segmentation and how does addressing work?** A: Dividing a process's space into variable-size segments (code, data, stack) each with base+limit+permissions; addresses are `(segment, offset)`, translated as `base + offset` with a limit check.
2. **Q: What does the segment table contain per segment?** A: Base, limit, and permission bits (read/write/execute, user/supervisor); indexed by segment number.
3. **Q: What happens on `STORE` to a read-only code segment?** A: Permission check fails → protection fault (#GP) → the process gets SIGSEGV unless the OS handles it (e.g., copy-on-write schemes historically).
4. **Q: Why does pure segmentation suffer external fragmentation? (Tricky)** A: Segments are variable-size, so free memory becomes holes that may not fit new/relocated segments — the Chapter 02 dynamic-allocation problem, requiring compaction or swapping.
5. **Q: How is sharing done in segmentation?** A: Two processes' segment tables point to the same physical base for a segment (e.g., the shared code of libc), with identical limits and read/exec permissions.
6. **Q: What's the difference between a segmentation fault and the segmentation scheme?** A: "Segmentation fault/SIGSEGV" is a generic name for memory-protection errors — modern OSes throw it from *paging* (bad page/permission), not from actual segment tables.
7. **Q: How does a stack grow under segmentation?** A: The OS increases the stack segment's limit (and maybe relocates it to a larger hole); paging instead maps new pages — but segmentation keeps the "stack" concept intact for protection.
8. **Q: Why did x86-64 remove user segmentation?** A: Simplicity + speed: one flat 64-bit space with paging covers everything; keeping two-stage translation (segment→linear→page) adds latency and complexity with no benefit for modern workloads.
9. **Q: What survives of segmentation on x86-64?** A: CS/DS/SS are flattened (base 0, full limit); FS/GS are repurposed — FS points at TLS/thread-local storage in user mode, GS at the kernel's percpu area. These are software conveniences, not the old protected segments.
10. **Q: When is segmentation actually better than paging? (Scenario)** A: When protection/sharing is by *logical unit* and segment count is small (embedded MPU regions, TEEs, legacy 16-bit apps). For general-purpose servers, paging's uniformity wins.
11. **Q: How does segmentation interact with demand paging?** A: Pure segmentation pages/segments are swapped wholesale (expensive); combined segmentation+paging (x86-32) pages only *used* portions of segments — the origin of modern VM for large segments.
12. **Q: What is the relationship between segments and the Linux VMA?** A: A VMA is a modern software "segment": a contiguous range of virtual addresses with uniform permissions (text/data/stack/anon/mmap) — emulated with paging. `struct vm_area_struct` in Linux is literally a segment table entry extended.
13. **Q: How many segments did classic Multics/System/360 support and why?** A: Multics had segments with ring-based protection (rings 0–7) and paging inside segments; IBM System/360 supported many segments — proving the concept worked but with heavy hardware complexity.
14. **Q: Is external fragmentation worse with segmentation or contiguous allocation?** A: Same fundamental issue (variable sizes); segmentation adds *internal* freedom (segments can be any size) but external fragmentation is the binding constraint in both.

## 14. Follow-Up Questions
1. **Q: How did x86-32 combine segments and paging?** A: Logical `(segment, offset)` → linear address (segment base + offset) → then paging's linear→physical translation. Two independent mechanisms stacked.
2. **Q: What's a "far pointer" in segmentation?** A: A pointer carrying both segment selector and offset (16:16 on 8086); near pointers used the current segment. The overhead and bugs of far pointers helped kill the scheme.
3. **Q: Why do modern OSes still set up GDT/LDT segments?** A: The CPU requires *some* descriptor tables for ring transitions and TLS/percpu; Linux keeps a minimal GDT and a null LDT for legacy support.
4. **Q: How does a JIT compile code if segmentation is gone?** A: It uses paging + `mprotect` to toggle W^X on pages — segments aren't needed; the "code segment" is just a VMA marked PROT_EXEC.

## 15. Coding Example
```c
// Simulate a segment table with base/limit/permission checks
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct { uint32_t base, limit; uint8_t rw, exec; } Segment;

static Segment table[4] = {
    { 0x1000, 0x800, 0, 1 },  // 0: code   (read/exec)
    { 0x9000, 0x400, 1, 0 },  // 1: data   (read/write)
    { 0xE000, 0x200, 1, 0 },  // 2: stack  (read/write)
};

int access(uint32_t seg, uint32_t off, bool is_write, uint32_t *phys) {
    if (seg >= 4) return -3;                       // bad segment
    Segment *s = &table[seg];
    if (off >= s->limit) return -1;                // limit fault
    if (is_write && !s->rw)  return -2;            // protection fault
    *phys = s->base + off;
    return 0;
}

int main(void) {
    uint32_t phys;
    printf("data[0x123]  -> %d (phys 0x%x)\n", access(1, 0x123, 0, &phys), phys); // ok
    printf("stack[0x250] -> %d (limit)\n", access(2, 0x250, 1, &phys));           // -1
    printf("code[0x10] write -> %d (prot)\n", access(0, 0x10, 1, &phys));         // -2
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `struct vm_area_struct` (software segments), `mm/mmap.c`; FS/GS segment use in `arch/x86/kernel/process.c` (percpu), `arch/x86/include/asm/segment.h`.
- **Windows**: FS points to TEB (thread environment block); x64 paging is flat.
- **ARM64**: no hardware segments; MPU regions on Cortex-M for safety domains (Zephyr, FreeRTOS+MPU, RT-Thread).
- **TEEs/TrustZone**: memory regions defined with base/limit semantics for secure domains.
- **Legacy**: DOS-era memory models; OS/2 and early Windows 16-bit segment managers.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.3 "Segmentation".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.5 "Segmentation".
- Intel SDM Vol. 3A, Ch. 3 "Protected-Mode Memory Management" (segments), Ch. 4 (paging).
- Linux source: `include/linux/mm_types.h` (`vm_area_struct`), `arch/x86/include/asm/segment.h`.
- Dennis & Van Horn (Multics), "Programming Semantics for Multiprogrammed Computations".

## 18. Cheat Sheet
- Address = `(segment, offset)`; physical = base + offset; check offset < limit.
- Segment table: base + limit + permissions per segment.
- Segments match program structure (code/data/stack) — paging doesn't.
- Pure segmentation → external fragmentation (variable sizes).
- x86-32 combined segments + paging (two-stage translation).
- x86-64 dropped user segments; FS/GS survive for TLS/percpu.
- "Segmentation fault" ≠ the scheme — it's a generic memory-protection error.
- Modern "segments" = Linux VMAs implemented on paging.

## 19. Quiz
1. A segment address is:
   a) (page, offset) b) (segment, offset) c) (frame, offset) d) linear only → **b**
2. Which operation faults on a read-only code segment?
   a) fetch b) load c) store d) jump → **c**
3. Pure segmentation's main problem:
   a) internal fragmentation b) external fragmentation c) TLB misses d) page faults → **b**
4. On x86-64, user-mode segmentation is:
   a) the primary scheme b) removed/flattened c) used for all memory d) mandatory → **b**
5. Linux emulates segments using:
   a) GDT b) VMAs c) page tables only d) LDT → **b**
6. FS register on Linux x86-64 typically holds:
   a) code base b) TLS pointer c) page table d) stack size → **b**

## 20. Flashcards
- **Q: What is segmentation?** → **A:** Variable-size regions (code/data/stack) with base+limit+permissions; addresses `(segment, offset)`.
- **Q: Why did pure segmentation fail?** → **A:** External fragmentation from variable sizes.
- **Q: What was x86-32's design?** → **A:** Segment → linear, then paging linear → physical (two stages).
- **Q: What survives on x86-64?** → **A:** Flat CS/DS/SS; FS (TLS) and GS (percpu) reused.
- **Q: What's a Linux VMA?** → **A:** A software segment: contiguous VA range with uniform permissions, on top of paging.
- **Q: "Segmentation fault" means?** → **A:** A memory-protection error (usually from paging), not the segmentation scheme.

## 21. Revision
Segmentation splits a process into variable-size logical segments (code, data, stack), addressed as `(segment, offset)`, with a segment table giving base, limit, and permissions per segment — natural for protection, sharing, and growth. Its fatal flaw: variable sizes → external fragmentation, needing compaction. Intel's x86-32 stacked segments on paging (two-stage translation), but x86-64 flattened segments (CS/DS/SS base-0) and left paging as the sole mechanism, keeping only FS/GS for TLS/percpu. Modern Linux "segments" are VMAs — contiguous permission-homogeneous ranges emulated on paging. Know this arc for interviews: segmentation = programmer-friendly, allocator-hostile; paging won.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is segmentation?" | 2 How / 7 Formal |
| "Why did it fail?" | 4 Alternative / 13 Q4 |
| "What's a segmentation fault really?" | 13 Q6 / 18 Cheat Sheet |
| "What survived on x86-64?" | 13 Q9 / 8 Example |
| "How do Linux VMAs relate to segments?" | 13 Q12 / 16 Industry |
| "How did x86-32 combine both?" | 14 Q1 / 4 Alternative |
