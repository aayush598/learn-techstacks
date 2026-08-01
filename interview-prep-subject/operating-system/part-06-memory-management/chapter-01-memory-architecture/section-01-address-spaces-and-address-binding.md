# Address Spaces and Address Binding

> **TL;DR**: Every process gets its own private **address space** (a fake range of addresses starting at 0) and its binding to real RAM happens at one of three times — compile, load, or run time — with run-time binding (via hardware translation) being the only scheme modern OSes trust.

## 1. Why Does This Exist?
If processes referenced physical RAM directly (e.g., "my data lives at 0x100000"), then:
- Two processes could never both be in memory (they'd collide on addresses).
- A program compiled for one machine layout would break on another.
- No isolation — process A could read/overwrite process B's data, so one bug kills the whole system.

An **address space** exists to decouple what a program *thinks* its addresses are from where they *physically* are. This buys three things simultaneously: **protection** (process A cannot touch process B's memory), **relocation** (any process can run at any physical base, or be moved while running), and **portability** (a binary's addresses don't depend on the machine's memory layout). This single abstraction — plus virtual memory in Part 07 — is what makes modern multitasking OSes possible at all.

## 2. How Does It Work?
A process's address space is defined by the set of addresses it can legally generate: typically `0 .. MAX`, where MAX is 2³²−1 (4 GB, 32-bit) or 2⁶⁴−1 (64-bit). The program uses these *logical* addresses; the OS/MMU maps a *subset* of them to actual physical frames. The point in the toolchain where this mapping gets pinned down is called **binding**:

| Binding time | What happens | When it runs | Still relocatable? |
|---|---|---|---|
| **Compile time** | Compiler emits absolute physical addresses; binary can only run at that exact address | `gcc`, linker | No |
| **Load time** | Compiler emits *relative* (relocatable) addresses; loader patches them with a base offset at load | `ld.so` / loader | Only if fully reloaded |
| **Run time** | Addresses stay logical; CPU+MMU translate every access using a base/limit or page table | Every instruction, via MMU | Yes, freely |

Modern OSes (Linux, Windows, macOS, all Unixes) use **run-time binding** for user processes: the binary is compiled position-independent (`-fPIC` / PIE), and the OS is free to place it anywhere, move it, and swap it out without re-patching.

## 3. When Is It Used?
- **Compile-time binding**: embedded systems, microcontrollers, kernel code that must live at a fixed address (e.g., the x86 reset vector at 0xFFFF0), boot loaders, `-fno-pic` firmware.
- **Load-time binding**: classic UNIX before MMUs, MS-DOS `.EXE` relocation tables, bootloader→kernel handoff.
- **Run-time binding**: every modern desktop/mobile/server OS for all user processes; this is what enables ASLR (Address Space Layout Randomization), shared libraries mapped at different bases per process, and `fork()` + exec with copy-on-write.

## 4. Why Wasn't Another Approach Chosen?
- **One process at a time (monoprogamming)**: simplest — no binding needed — but the CPU sits idle during every I/O. Rejected for throughput.
- **Overlay programming**: the *programmer* manually divides the program into segments that get swapped into a fixed window; binds at compile time. Rejected: error-prone, kills productivity (this is what killed memory as a "programmer-managed" resource).
- **Static partition + compile-time binding**: simple but wastes memory (processes rarely fit perfectly) and forbids growth.
- **Base+limit (load-time)**: cheap and simple, but requires contiguous physical memory and cannot move a running process without halting and repatching.
- **Run-time binding + MMU translation**: more complex hardware, but it is the only approach giving free relocation, fine-grained protection, and later virtual memory. This is why it won everywhere.

## 5. Intuition
Imagine every program is a book written with page numbers starting at "Page 1". If libraries stored books by "the number printed inside", two books would clash. Instead, the library assigns a *shelf position* — book A starts at shelf 100, book B at shelf 200 — and any page number *inside* the book means "shelf + printed page − 1". The program is the book; the *printed page numbers* are logical addresses; the *shelf offset* is the base register; and the librarian converting "Page 5 → Shelf 104" on every lookup is the MMU. The book never needs re-printing when it's moved — the librarian just updates the offset.

## 6. Real-World Analogy
A hotel with room numbers 100–199 on every floor (each floor reuses "100–199"). The front desk (MMU) knows that "Room 105" printed on a guest's key card means *Floor 2, Room 105* for one guest and *Floor 7, Room 105* for another. Guests (processes) each believe they have rooms 100–199; the desk keeps a mapping per guest. If a guest changes floors, only the desk's mapping changes — the key card is untouched.

## 7. Formal Definition
An **address space** is the set of logical (virtual) addresses a process may generate, plus the mapping defined by the system from those addresses to physical addresses. **Address binding** is the process of associating a program instruction's data/instruction references with physical memory locations; it occurs at compile time, load time, or run time depending on the binding scheme. Under **run-time binding**, logical addresses remain in the program and hardware translates them to physical addresses at execution, so the mapping can change at any time without program modification.

## 8. Example
Take a 32-bit binary compiled with `-fPIC`. Say the instruction `LOAD R1, 0x4000` exists at logical 0x1000.

- **Compile-time binding**: if the OS pinned the process at physical 0x0, no translation is needed — 0x1000→0x1000, 0x4000→0x4000. Fragile: any other resident process breaks it.
- **Load-time binding**: the loader places the process at physical base 0x8000, adds 0x8000 to every address: instruction at 0x9000, loads from physical 0xC000. If the process must move, every reference is re-patched.
- **Run-time binding**: process placed at physical base 0x8000; MMU base register = 0x8000, limit = 0x8000+size. Instruction `LOAD R1,0x4000` at logical 0x1000 is fetched → MMU adds 0x8000 → fetches from physical 0x9000 → MMU translates data address 0x4000→0xC000. Moving the process to 0x5000 requires only updating the base register; the binary never changes.

## 9. Internal Working
1. **Compile/link**: compiler produces relocatable object code with *symbolic* addresses; linker assigns them logical addresses within the program's virtual layout (e.g., `.text` at 0x400000, `.data` next). PIE makes these offsets, not absolutes.
2. **Load**: `execve()` creates the process; the kernel maps file segments into the address space at chosen bases (respecting ASLR). No physical pages are touched yet under demand paging (Part 07).
3. **Run**: for each memory reference, the CPU hands the logical address to the MMU.
4. **Translate**: MMU consults base/limit or page-table base register (CR3 on x86); adds base (or walks the table), checks bounds, and emits a physical address onto the memory bus.
5. **Protect**: if the logical address exceeds the limit (or no page-table entry exists), the MMU raises a **segmentation fault / page fault** exception, transferring control to the kernel, which terminates or faults in the page.
6. **Relocate**: when the OS moves or swaps a process, it updates only the MMU registers/page tables; the process's logical image is untouched.

## 10. Time Complexity
- Logical→physical translation with base/limit: **O(1)** — one add + one compare.
- With paging + TLB: **O(1)** average (TLB hit), **O(L)** per miss, where L = levels of page table (4 on x86-64), then O(1) caching.
- Load-time re-binding a process of size N: **O(N)** (must patch every relocatable reference) — the fundamental reason run-time binding scales.
- Memory overhead of a 4-level page table per process: O(1) root table + O(4) top levels, page tables allocated on demand — asymptotically O(used VA) rather than O(full VA range).

## 11. Advantages
- **Isolation**: a process cannot address another's memory (no shared-address accidents).
- **Relocation for free**: process can be moved/swapped without re-patching.
- **Portability**: one binary runs regardless of physical layout; enables ASLR for security.
- **Paves the way for virtual memory** (Part 07): demand paging, mmap, copy-on-write all build on run-time binding.
- Sparse address use: the process *may* reference 2⁶⁴ addresses without reserving RAM for them.

## 12. Disadvantages
- Run-time binding requires MMU hardware (absent on the cheapest microcontrollers).
- Translation adds latency per access — must be mitigated by TLBs and caches.
- Address-space metadata (page tables) costs memory and complexity.
- Base/limit-style protection only checks *range*, not fine-grained permissions (r/w/x per page) — for that you need page tables.

## 13. Interview Questions
1. **Q: What is an address space and why does every process have one?** A: The set of logical addresses a process can generate (0..2^n−1), kept separate per process so programs can't corrupt each other, can be relocated freely, and don't need to know the physical layout. It exists to provide isolation, protection, and portability.
2. **Q: Name the three binding times and which one modern OSes use.** A: Compile time (absolute addresses baked in, used in firmware/embedded), load time (loader patches relative addresses; used by classic UNIX and MS-DOS), run time (MMU translates every access; used by Linux/Windows/macOS for all user code).
3. **Q: Why can't you just bake physical addresses into a compiled binary?** A: Two processes would collide if loaded together, the binary breaks if memory layout differs, and you lose ASLR and demand paging. Only usable for single-purpose embedded/firmware code at fixed addresses.
4. **Q: What's the difference between a logical, a physical, and a relative address?** A: Logical/virtual = what the program emits; physical = actual RAM location on the bus; relative = offset from a base (used at load time, becomes logical or physical after adding the base).
5. **Q: How does the OS change a running process's physical location? (Tricky)** A: It updates the MMU's base register / page tables for that process, flushes the TLB, and resumes; the process's logical image never changes — that's the whole point of run-time binding.
6. **Q: What is ASLR and how does it relate to address binding?** A: Address Space Layout Randomization randomizes the base of the stack, heap, libraries, and executable at load time (using run-time binding) so attackers can't predict where code lives; defeats return-oriented programming and ret2libc attacks.
7. **Q: When would you still use compile-time binding in production?** A: Firmware, boot ROMs, kernel entry at a fixed physical address (x86 reset vector), real-time microcontrollers, and safety-critical systems where a known physical layout is required for deterministic behavior.
8. **Q: What's the downside of load-time binding that run-time binding eliminates?** A: Load-time binding makes relocation O(N) (patch every reference) and can't move a process while it runs; run-time binding makes relocation O(1) hardware-register updates but needs an MMU.
9. **Q: A process refers to address 0x1000. Which address does the memory bus see, and who changed it? (Scenario)** A: The bus sees whatever the MMU emits after adding the base (say 0x8000 → 0x9000). The MMU changed it using the process's base register; the CPU and process are oblivious.
10. **Q: Can a 64-bit process address 2⁶⁴ bytes of physical RAM? (Production)** A: No — 2⁶⁴ is the *virtual* address space. Physical RAM is bounded by hardware (e.g., 48-bit or 52-bit physical address on x86-64 with PAE/LARGE). The OS maps a subset of virtual addresses to physical frames; the rest are unmapped (page faults).
11. **Q: What happens if a process references an address outside its range?** A: With base/limit, the MMU raises a trap (segmentation fault); with paging, the walk finds no PTE and faults — the kernel typically sends SIGSEGV. The process is prevented from ever touching foreign memory.
12. **Q: Why are shared libraries mapped at different virtual bases in each process? (Tricky)** A: Because each process's address space is independent, the loader can place libc at a random base per process (ASLR) even though the physical pages are shared (same physical frame mapped into many spaces) — this strengthens security without losing sharing.

## 14. Follow-Up Questions
1. **Q: How does run-time binding make `fork()` cheap?** A: The child's page tables can initially point at the same physical frames (copy-on-write), so no copying of code happens — only table cloning. Binding at run time means the two processes can later diverge without re-binding.
2. **Q: What does "position-independent code" (PIC/PIE) mean?** A: Code whose addresses are relative to its own base, so it can be loaded anywhere without patching; required for shared libraries and ASLR.
3. **Q: How do kernel addresses differ from user addresses in binding?** A: The kernel is typically mapped into the *top* of every process's virtual address space (e.g., above 0xFFFF800000000000 on x86-64 Linux) with a fixed high-half mapping, while user space is the low half.
4. **Q: What is a "swizzle" pointer vs a bound pointer?** A: Swizzling is converting on-disk/persistent pointers at load time (like load-time binding); bound pointers carry provenance for protection — an advanced memory-safety technique.
5. **Q: Does TLB invalidation matter when relocating a process?** A: Yes — after changing page tables/base you must `invlpg`/flush TLB entries or stale translations persist (use `munmap`, `mprotect`, ASLR-aware loads all flush).

## 15. Coding Example
```c
// Minimal simulation of run-time binding with a base/limit "MMU"
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    unsigned base;          // physical start of the process
    unsigned limit;         // size of the process in bytes
} MMU;

// Returns physical address, or -1 if out of range (segfault)
int translate(MMU *mmu, unsigned logical) {
    if (logical >= mmu->limit) {
        printf("FAULT: logical 0x%x outside limit 0x%x\n", logical, mmu->limit);
        return -1;                       // kernel would raise SIGSEGV here
    }
    return (int)(mmu->base + logical);   // O(1) add + compare
}

int main(void) {
    MMU mmu = { .base = 0x8000, .limit = 0x2000 };
    printf("ld 0x1000 -> phys 0x%x\n", translate(&mmu, 0x1000)); // 0x9000
    translate(&mmu, 0x3000);                                      // FAULT
    mmu.base = 0x5000;  // process relocated while running!
    printf("ld 0x1000 -> phys 0x%x\n", translate(&mmu, 0x1000)); // 0x6000
    return 0;
}
```

## 16. Industry Usage
- **Linux**: PIE executables by default (`gcc -pie -fPIE`); ASLR enabled via `randomize_va_space`; `struct mm_struct` holds `start_code`, `start_data`, `brk`, and the memory map; relocation done by `mmap` during `execve` (`fs/exec.c`). The kernel itself is compiled `-fno-pie` and loaded at a fixed high address.
- **Windows**: PIE-equivalent is ASLR on every PE (DYNAMICBASE); loader rebases DLLs at run time; `NtMapViewOfSection` places images.
- **macOS/XNU**: ASLR on all apps; hardened runtime with `-Wl,-pie`.
- **Android/iOS**: ASLR + PIE mandatory for all apps since Android 5 / iOS 7.
- **Embedded**: FreeRTOS/RTOS tasks use base+size descriptors; some safety systems (AUTOSAR) still use fixed link addresses.

## 17. References
- Silberschatz, Galvin & Gagne, *Operating System Concepts (10th ed.)*, Ch. 8 "Main Memory".
- Tanenbaum & Bos, *Modern Operating Systems (4th ed.)*, Ch. 3 "Memory Management".
- Linux kernel docs: `Documentation/admin-guide/kernel-parameters.rst` (ASLR), `Documentation/arch/x86/x86_64/mm.rst`.
- Linux source: `fs/exec.c`, `arch/x86/mm/mmap.c`, `include/linux/mm_types.h`.
- `man 7 aslr`, `man 5 elf` (program headers → `PT_LOAD` for mapping segments).

## 18. Cheat Sheet
- Address space = the set of logical addresses a process may touch; starts at 0.
- Binding times: compile (absolute, embedded), load (patching, classic Unix), run (MMU, modern).
- Run-time binding ⇒ free relocation, isolation, ASLR, and virtual memory.
- Logical address = what the program emits; physical = what hits the bus; MMU converts.
- Base+limit = add base, check limit — O(1) per access, but requires contiguous RAM.
- PIE/PIC = position-independent code required for ASLR and shared libraries.
- Out-of-range access ⇒ MMU trap ⇒ SIGSEGV.
- Translation cost is why we need TLBs and CPU caches.

## 19. Quiz
1. A program that can only run at one physical address uses ___ binding.
   a) run-time b) load-time c) compile-time d) none → **c**
2. Which binding is used by Linux for user-space processes?
   a) compile-time b) load-time c) run-time d) virtual → **c**
3. The MMU converts a ___ address into a ___ address.
   a) physical, logical b) logical, physical c) virtual, logical d) none → **b**
4. What does the limit register do?
   a) bounds the heap b) checks logical addresses are within the process range c) caches translations d) selects the CPU → **b**
5. Relocating a process is O(1) when using:
   a) load-time binding b) compile-time binding c) run-time binding d) overlays → **c**
6. ASLR is possible only because of ___.
   a) compile-time binding b) run-time binding c) load-time binding d) overlays → **b**

## 20. Flashcards
- **Q: Why does each process get its own address space?** → **A:** Isolation + relocation + portability; processes can't corrupt each other and can be placed anywhere.
- **Q: Name the 3 binding times.** → **A:** Compile time (embedded), load time (classic Unix/classic DOS), run time (all modern OSes, via MMU).
- **Q: What does the MMU do per memory access?** → **A:** Adds base / walks page tables, checks bounds, emits physical address; raises trap on violation.
- **Q: Why does run-time binding make relocation O(1)?** → **A:** Only the MMU base register / page tables change; the program image never changes.
- **Q: What happens on an out-of-range address?** → **A:** MMU raises a fault; kernel sends SIGSEGV (or loads the page in demand paging).
- **Q: Why do modern binaries need PIE?** → **A:** ASLR; code with absolute addresses can't be randomized at load.

## 21. Revision
Processes must not know physical RAM locations: they use a logical address space (0..MAX). Binding — when logical references are resolved to physical — happens at compile, load, or run time; modern OSes pick **run-time** binding so a process can be relocated, isolated, and later support virtual memory. Per memory access the MMU adds a base and checks a limit (or walks page tables), emitting the physical address; an out-of-range access traps and becomes SIGSEGV. This decoupling is why Linux/Windows can run thousands of processes safely in limited RAM and is the prerequisite for everything in the rest of this part.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is an address space and why is it needed?" | 1 Why / 7 Formal Definition |
| "Explain compile vs load vs run-time binding." | 2 How It Works / 8 Example |
| "Why is ASLR possible on modern OSes?" | 4 Alternative / 13 Q6 |
| "How does the MMU translate a logical address?" | 2 How / 9 Internal Working |
| "What happens on an out-of-bounds access?" | 9 Internal Working / 13 Q11 |
| "Why can't two processes share physical addresses?" | 1 Why Does This Exist |
| "How is a running process relocated?" | 8 Example / 13 Q5 |
