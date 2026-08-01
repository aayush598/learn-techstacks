# Address Space and Kernel Memory Layout

> **TL;DR**: On x86-64, a process sees a 48-bit virtual space: the **user half** (code/data/heap via `brk`, mmap region, stack at `0x7ffffffff000`) and the **kernel half** (`PAGE_OFFSET` direct map of RAM, `vmalloc` region, `vmemmap`, fixmap, `kasan`). The kernel maps all physical memory + a vmalloc area; `kmalloc` gives physically contiguous memory, `vmalloc` gives virtually contiguous (physically scattered). Page tables (4 levels on x86-64) translate both halves.

## 1. Why Does This Exist?
The kernel and every process share one virtual address space architecture, but need different guarantees. User processes need a large, protected, demand-paged space (Part 07). The kernel needs (a) to reach any physical page cheaply (a direct mapping), (b) large virtually-contiguous buffers that physical memory can't provide (vmalloc), (c) a stable region for per-CPU data and fixups (fixmap), and (d) bookkeeping memory per physical page (vmemmap). Understanding the layout explains a huge set of interview answers: why user pointers get validated, why the kernel half is above the user half, why `kmalloc` is limited, and how the 4-level page table works in practice.

## 2. How Does It Work?
**x86-64 user space** (per process `mm`, mapped via `mm_struct`):
- `0x0000000000400000` (typical PIE base): text/code, then data/bss.
- Heap: grows up via `brk`/`sbrk` (the program break) for small allocations (malloc arenas).
- `mmap` region: grows *down* from `0x7ffffffff000`-ish — `malloc` for big chunks, shared libs (`MAP_PRIVATE`), `shm_open`, `mmap` files.
- Stack: at the top, grows down; `ulimit -s` sets max; guard page.
- `0x00007fffffffe000` = highest user address (`TASK_SIZE_MAX`), `0xffff800000000000` = kernel half start.
- Also: `vsyscall` (0xffffffffff600000) and `[vdso]` — the fast syscall helpers mapped into user space.

**Kernel half** (x86-64, 4-level paging, `-4G`? no — 64-bit split at `PAGE_OFFSET`):
- `PAGE_OFFSET` = `0xffff888000000000` (CONFIG default): **direct map** — maps all physical RAM linearly (`virt = phys + PAGE_OFFSET`); used for `kmalloc` and general kernel pointers.
- `VMALLOC_START`–`VMALLOC_END`: vmalloc region (scattered physical pages, contiguous virtual).
- `VMEMMAP_START`: `vmemmap` — one `struct page` per physical page.
- Fixmap, CPU entry area, `kasan` shadow, modules area, `cpu_entry_area`.
- Kernel text/data are mapped at `0xffffffff80000000` (high kernel mapping, `_text`/`_stext`).

**Page tables (4-level x86-64)**: `pgd → pud → pmd → pte` (each level 512 entries, 4 KB pages; 5-level `p4d` on newer configs). The kernel has one init page table set (`swapper_pg_dir`) shared by all processes (via the top-level entries) — so every process's page tables include the kernel half for free. TLBs are flushed with `switch_mm` (mitigated by PCID/ASIDs).

**kmalloc vs vmalloc**:
- `kmalloc` (slab/slub): physically contiguous, in the direct map — fast, cache-friendly, used for kernel objects; limited to contiguous physical spans (size limits; `GFP_*` flags).
- `vmalloc`: virtually contiguous, physically scattered (per-page allocations) — for large buffers, sparse mappings; requires page-table updates per area (slower), no SLAB caching.
- Also: `kvmalloc` (try kmalloc, fall back vmalloc), `get_free_pages` (page allocator), `alloc_pages`, `kmem_cache` (SLUB).

## 3. When Is It Used?
- **User**: every program's memory (stack/heap/mmap); shared libs; shared memory (Part 09 Sec 03); mmap'd files.
- **Kernel**: `kmalloc` for the vast majority of kernel objects (task_struct, inode, sk_buff...); `vmalloc` for module text, some drivers, big buffers (`vmalloc(16MB)` for staging), `vmemmap`/direct map for everything else.
- **Debugging/inspection**: `/proc/self/maps` (user layout), `/proc/kallsyms`, `cat /proc/meminfo` (direct/vmalloc/kernel stacks), `pagemap`; `perf`/`crash` for kernel addresses.

## 4. Why Wasn't Another Approach Chosen?
- **Flat mapping of all memory (too risky)**: user needs isolation — hence the split at PAGE_OFFSET.
- **Kernel entirely in low memory (historical, 32-bit)**: on 32-bit, the 3G/1G split constrained kernel address space to 1 GB — 64-bit solved it with a huge kernel half.
- **All allocations vmalloc (rejected)**: page-table per area + TLB pressure would kill performance — hence direct map + kmalloc for hot paths.
- **All allocations kmalloc (rejected)**: physically contiguous memory isn't available for large sizes — hence vmalloc for big/scattered needs.
- **`KASLR` (chosen)**: randomize kernel text/module base for security — but the layout structure remains fixed; `kptr_restrict` hides addresses.
- **5-level paging (CONFIG_X86_5LEVEL)**: optional for >48-bit machines; default is 4-level for compatibility.

## 5. Intuition
**A building with two wings**: the user half is the public wing (each tenant gets their own rooms: code, data, heap, stack); the kernel half is the staff-only wing, present in every tenant's floor plan but inaccessible. The direct map is the "master key" — a single linear walk from `PAGE_OFFSET` lets the kernel reach any physical room without a fancy map. `kmalloc` = contiguous rooms on one floor (fast, but limited by floor layout); `vmalloc` = a virtual hallway that connects rooms scattered across floors (big, but slower to build).

## 6. Real-World Analogy
**A library with a general catalog**: each reader (process) gets their own study carrel layout (user space). The librarians (kernel) have a *master floor plan* (direct map) so they can walk any shelf without consulting a map. For big projects (vmalloc) they can reserve a corridor that hops across different rooms. The catalog itself (page tables) is a 4-level index: Wing → Floor → Room → Shelf (PGD → PUD → PMD → PTE), with the top level shared by everyone so all librarians see the same staff area.

## 7. Formal Definition
On x86-64 with 4-level paging: user space `[0x0, 0x00007ffffffff000]` (TASK_SIZE_MAX), kernel space `[0xffff800000000000, 0xffffffffffffffff]`. Key kernel regions: `PAGE_OFFSET` (direct map of all physical RAM, `virt_to_phys(x) = x - PAGE_OFFSET`), `VMALLOC_START/END` (vmalloc area), `VMEMMAP_START` (`struct page` array, `vmemmap`), fixmap (permanent fixed mappings), `cpu_entry_area` (per-CPU entry/trampoline), `__START_KERNEL_map` (kernel text/data high mapping). Virtual→physical translation: walk `pgd` (index by bits 39–47) → `pud` (30–38) → `pmd` (21–29) → `pte` (12–20) → frame (bits 0–11 flags). `kmalloc` = slab/slub-backed physically-contiguous allocation from the direct map; `vmalloc` = non-contiguous physical pages under one virtual range (area in `vmlist`/`vmap_area_tree`). `malloc` in user space uses `brk` (small) + `mmap` (large) via glibc arenas.

## 8. Example
Layout of a running program (`/proc/self/maps`):
```
00400000-00401000 r-xp  /bin/cat            (text)
00600000-00601000 r--p  /bin/cat            (rodata/reloc)
00601000-00602000 rw-p  /bin/cat            (data/bss)
7f8b8d2ba000-7f8b8d3d0000 r-xp  /lib/x86_64-linux-gnu/libc.so.6
7f8b8d3d0000-7f8b8d5d1000 ---p  (guard)
7f8b8d5d1000-7f8b8d5d4000 rw-p  (libc data)
7fff283c0000-7fff283e1000 rw-p  [stack]     (grows down from 0x7fff...)
7fff283ff000-7fff28400000 r-xp  [vdso]      (fast syscall helper)
ffffffffff600000-ffffffffff601000 r-xp  [vsyscall]
```
Kernel side (`/proc/kallsyms` prefixes): kernel text at `ffffffff81000000`, direct map entries `ffff8880...`, vmalloc `ffffc900...`, vmemmap `ffffea00...` — illustrating the four regions.

`kmalloc` vs `vmalloc` example:
- `struct task_struct *tsk = kmalloc(sizeof(struct task_struct), GFP_KERNEL);` — one physically contiguous object, direct-map backed, SLUB-cached.
- `void *buf = vmalloc(16 * 1024 * 1024);` — 16 MB virtually contiguous, pages allocated individually; page tables set up for the range; freed with `vfree`.

## 9. Internal Working
1. **User layout**: `exec` sets up `mm_struct` from ELF PT_LOAD; `brk` adjusts `mm->brk` (program break); `mmap` inserts a `vm_area_struct` (VMA) into `mm->mmap` rbtree; page faults (`handle_mm_fault`) allocate pages and fill page tables (`do_anonymous_page` for heap/stack, `filemap_fault` for file maps, `do_wp_page` for COW).
2. **Kernel layout**: on boot, `init_mem_mapping` builds the direct map (large pages 2 MB/1 GB) from `PAGE_OFFSET`; `vmalloc_init` reserves `VMALLOC_START..END`; `vmemmap_init` maps the struct-page array; `setup_arch` sets fixmap/cpu_entry_area; `KASLR` randomizes `_text`/modules.
3. **Translation**: `virt_to_phys`/`phys_to_virt` for direct map; `walk_page_range`/`follow_page` for arbitrary; TLB misses walk 4 levels via `mmu_gather`/`p*_alloc`; `switch_mm` switches CR3 + (with PCID) avoids full flushes.
4. **Allocators**: page allocator (`alloc_pages` buddy) → `kmem_cache` (SLUB) → `kmalloc`; `vmalloc` calls `alloc_page` per chunk + `vmap_page_range` to build the area.
5. **Per-process view**: each task's `pgd` top-level entries copied from `swapper_pg_dir` → the kernel half is mapped identically in every process (only the user half differs) — kernel code runs in the same page table space as the interrupted task.

## 10. Time Complexity
- Direct-map access: O(1) arithmetic (`phys = virt - PAGE_OFFSET`).
- Page-table walk: O(levels) = O(4) per miss (TLB hit: O(1)).
- `kmalloc`: O(1) from slab (fast); page allocator O(1) per page (buddy).
- `vmalloc`: O(n) page-table setup per area (n = pages), plus vmap tree lookup O(log areas) — slower than kmalloc, which is why it's not the default.
- `brk`/`mmap`: O(log n) VMA tree op; fault: O(1) per page + page-table entries.
- `switch_mm`: O(1) CR3 write (+ PCID flush optimization).

## 11. Advantages
- **Direct map**: O(1) phys↔virt; hot kernel paths never touch page tables for RAM access.
- **vmalloc**: large/scattered buffers without physical contiguity; sparse mappings possible.
- **Split space**: user isolation + kernel presence in every process's tables (no page-table switch on syscall).
- **vmemmap**: O(1) page-struct lookup for any physical page (buddy/refcount).
- **Huge pages**: direct map uses 2 MB/1 GB → fewer TLB entries, fast kernel memory access.
- **KASLR/kptr_restrict**: security hardening of the kernel half.

## 12. Disadvantages
- **Kernel-space security**: a user bug can't reach kernel, but kernel bugs (use-after-free) have no user-space protection — hence KASAN/slab hardening.
- **kmalloc limits**: physical contiguity caps sizes (a few MB per allocation reliably) — big allocations must use vmalloc.
- **vmalloc cost**: page-table updates + TLB pressure for large areas; not cache-friendly (scattered).
- **Address-space split complexity**: `virt_to_phys` only valid for direct-map addresses; pointer provenance bugs (e.g., `virt_to_phys(vmalloc_addr)`) are classic.
- **Wasted space**: mapping the kernel half in every process's page tables costs page-table memory (mitigated by shared top levels).
- **32-bit legacy**: 3G/1G split constrained the kernel; 64-bit removed the pain but multiplied page-table depth.

## 13. Interview Questions
1. **Q: Describe the Linux virtual address space on x86-64.** A: User half `0x0–0x7ffffffff000` (code, data, heap/brk, mmap, stack, vdso/vsyscall); kernel half `0xffff800000000000+` (direct map at PAGE_OFFSET, vmalloc, vmemmap, fixmap, kernel text). The kernel half is mapped in every process's page tables.
2. **Q: What is the direct map (PAGE_OFFSET)?** A: A linear virtual mapping of all physical RAM: `virt = phys + PAGE_OFFSET`, O(1) translation. The kernel's default way to access memory (kmalloc memory, page cache).
3. **Q: kmalloc vs vmalloc?** A: `kmalloc` = physically contiguous (direct map, SLUB-cached, fast, smallish); `vmalloc` = virtually contiguous over scattered physical pages (slower, page-table setup, for large buffers). `kvmalloc` picks either.
4. **Q: Why is the kernel above user space?** A: The top of the address space is reserved for the kernel (split at PAGE_OFFSET/TASK_SIZE_MAX); on x86-64 that's the top ~half. Keeps user code out and lets the kernel map all RAM + its own structures without interfering with user addresses.
5. **Q: How does the kernel access user memory?** A: `copy_from_user`/`copy_to_user` (and `get_user`/`put_user`) — validated, fault-tolerant copies across the boundary (they can sleep / handle faults).
6. **Q: What are the four page-table levels?** A: PGD → PUD → PMD → PTE (48-bit VA: 39–47, 30–38, 21–29, 12–20 index bits), each 512 entries; 5-level (p4d) optional. TLB caches results; `switch_mm`/CR3 switches per process.
7. **Q: What is vmemmap?** A: The array of `struct page` objects (one per physical page) mapped at VMEMMAP_START — the kernel's per-physical-page bookkeeping (refcount, flags, lru) accessed by `pfn_to_page`/`page_to_pfn`.
8. **Q: What is the difference between the heap (brk) and mmap allocations?** A: `brk`/`sbrk` extends the program break (contiguous small allocations — glibc uses it for small chunks); `mmap` allocates regions mapped individually (large chunks, shared libs, files). malloc mixes both via arenas.
9. **Q: What is KASLR?** A: Kernel Address Space Layout Randomization — randomizes the base of kernel text/modules at boot so attackers can't rely on fixed addresses; `kptr_restrict` hides kernel addresses from unprivileged users.
10. **Q: Why can't the kernel use vmalloc for everything?** A: vmalloc requires per-area page-table updates and scattered pages — slower + more TLB pressure; the direct map + kmalloc is the fast path. vmalloc is for large/irregular needs.
11. **Q: What does `/proc/self/maps` show?** A: Each mapped region (VMA): address range, permissions, file/anon, offset — the user-space half of the layout in action (text/data/rodata/heap/stack/libs/vdso).
12. **Q: What is the vsyscall/vdso?** A: Fixed (vsyscall) and dynamic (vdso) kernel-to-user pages containing fast syscall helpers (e.g., `gettimeofday`, `clock_gettime`) so common calls never trap into the kernel (Part 09 Sec 04).

## 14. Follow-Up Questions
1. **Q: What is the guard page?** A: An unmapped page below the stack/heap to catch overflow — touching it faults (SIGSEGV) instead of silently corrupting memory.
2. **Q: What is KASAN?** A: KernelAddressSanitizer — a shadow region (in the kernel address space) that detects use-after-free/out-of-bounds in kernel memory; maps validity via a parallel shadow map.
3. **Q: What is `mmap` MIN/MAX and ASLR?** A: `mmap_rnd_bits` randomizes the mmap/stack bases (user-space ASLR); `vm.mmap_min_addr` protects the zero page.
4. **Q: What is the difference between 32-bit and 64-bit layout?** A: 32-bit: 3G/1G split (user 0–3G, kernel 3–4G, no vmalloc room historically). 64-bit: huge kernel half, 4–5 level paging, virtually unlimited user space.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

// Prints the user-space layout of THIS process.
int main(void) {
    static int data;                    // in .data (BSS section)
    int *heap = malloc(1 << 20);        // brk/mmap-allocated
    void *map = mmap(NULL, 1 << 20, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    char env[] = "env";

    printf("text   : %p (main)\n", (void *)main);
    printf("data   : %p\n", (void *)&data);
    printf("heap   : %p (malloc)\n", (void *)heap);
    printf("mmap   : %p (anon)\n", map);
    printf("stack  : %p (this var)\n", (void *)&env);
    printf("libc   : %p (printf)\n", (void *)&printf);
    printf("brk    : %p\n", (void *)sbrk(0));

    munmap(map, 1 << 20);
    free(heap);
    return 0;
}
```
Run it: text (0x55...) < data < heap (0x55...) < mmap (0x7f...) < stack (0x7ff...) — the classic increasing-address ordering (heap near text, mmap/stack high).

## 16. Industry Usage
- **Kernel**: `arch/x86/mm/init.c` (direct map), `mm/vmalloc.c`, `mm/slub.c` (kmalloc), `mm/sparse.c` (vmemmap), `arch/x86/include/asm/page_64_types.h` (PAGE_OFFSET), `mm/kasan/`.
- **Runtime**: glibc malloc (brk + mmap arenas), JVM/Go (mmap), ASLR config (`kernel.randomize_va_space`).
- **Diagnostics**: `/proc/self/maps`, `/proc/self/smaps`, `/proc/meminfo`, `crash`, `gdb` (`xinfo`).
- **Security**: KASLR, `kptr_restrict`, SELinux/AppArmor (memory layout), heap hardening.

## 17. References
- Love, *Linux Kernel Development*, Ch. 11 "Memory Management" (kmalloc/vmalloc, address spaces).
- Silberschatz, *Operating System Concepts*, Ch. 9 (virtual memory), Linux chapter.
- Tanenbaum, *Modern Operating Systems*, Ch. 3 (memory management) and Linux sections.
- Kernel docs: `Documentation/admin-guide/mm/`, `Documentation/vm/`, `Documentation/x86/x86_64/mm.rst` (the canonical layout).
- `man 5 proc` (`/proc/self/maps`), `man 2 brk`, `man 2 mmap`.

## 18. Cheat Sheet
- User half: text → data/bss → heap(brk) → mmap → stack → vdso/vsyscall.
- Kernel half: direct map (PAGE_OFFSET) → vmalloc → vmemmap → fixmap → text.
- Direct map: `virt = phys + PAGE_OFFSET`, O(1).
- kmalloc = phys-contiguous (direct map, SLUB); vmalloc = virt-contiguous (scattered).
- Page tables: PGD→PUD→PMD→PTE (4 levels, 4 KB pages; 5-level opt).
- Kernel half mapped in every process's page tables.
- `copy_from_user`/`to_user` cross the boundary safely.
- KASLR + kptr_restrict harden the kernel half.

## 19. Quiz
1. User space ends at? a) 0x7ffffffff000 b) 0xffffffff c) 4G d) 0xffff8000 → **a**
2. Direct map formula? a) virt=phys+PAGE_OFFSET b) phys=virt+2G c) both d) neither → **a**
3. kmalloc gives? a) virt-contiguous b) phys-contiguous c) random d) shared → **b**
4. vmalloc is for? a) hot objects b) large/scattered buffers c) DMA d) stack → **b**
5. Page-table levels? a) 2 b) 3 c) 4 d) 5 optional → **c** (4 on x86-64 default)
6. `/proc/self/maps` shows? a) kernel b) VMAs c) devices d) tasks → **b**

## 20. Flashcards
- **Q: User space layout?** → **A:** text, data, heap(brk), mmap, stack, vdso.
- **Q: Direct map?** → **A:** PAGE_OFFSET linear map of all RAM.
- **Q: kmalloc vs vmalloc?** → **A:** Phys-contig (fast) vs virt-contig (scattered).
- **Q: Page-table levels?** → **A:** PGD→PUD→PMD→PTE.
- **Q: Kernel half in every process?** → **A:** Yes — top-level pgd shared.
- **Q: brk vs mmap?** → **A:** Small contiguous heap vs per-region mappings.

## 21. Revision
Linux's x86-64 address space splits at the top: the user half (`text/data/heap/brk → mmap → stack`, ending ~0x7ffffffff000) and the kernel half (direct map at PAGE_OFFSET giving O(1) phys↔virt, vmalloc for large scattered buffers, vmemmap for `struct page`, fixmap, and randomized kernel text). Page tables are 4 levels (PGD→PUD→PMD→PTE), with the kernel half mapped identically in every process — so syscalls don't switch page tables. `kmalloc` (SLUB, physically contiguous, fast) vs `vmalloc` (virtually contiguous, scattered, for big buffers) is the classic differentiator. User↔kernel crossings use `copy_from_user`/`copy_to_user`, and KASLR/kptr_restrict harden the layout. This is the memory-stage on which the syscall machinery (Section 04) and I/O paths (Section 03) run.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe the x86-64 address layout." | 13 Q1 / 2 How |
| "What is the direct map?" | 13 Q2 / 2 How |
| "kmalloc vs vmalloc?" | 13 Q3 / 7 Formal |
| "Why is the kernel above user space?" | 13 Q4 / 4 Why not |
| "How does the kernel access user memory?" | 13 Q5 / 9 Internal |
| "What are the page-table levels?" | 13 Q6 / 7 Formal |
| "What is vmemmap?" | 13 Q7 / 2 How |
| "What does /proc/self/maps show?" | 13 Q11 / 8 Example |
