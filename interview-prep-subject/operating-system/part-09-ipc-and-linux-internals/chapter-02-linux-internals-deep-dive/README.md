# Chapter: Linux Internals Deep Dive

## What you'll learn
- **Process lifecycle in Linux**: `fork`→`exec`→`exit` — the `task_struct`, `CLONE_*` flags (`CLONE_THREAD`, `CLONE_VM`, `CLONE_FILES`), copy-on-write fork, zombies/orphans, and how the scheduler actually runs them.
- **Address space and kernel memory layout**: the Linux virtual memory map (user: stack/heap/`brk`/mmap; kernel: direct map, vmalloc, vmemmap, fixmap), `kmalloc` vs `vmalloc`, page tables in practice, and the `0xc0000000`/`0xffff888000000000` splits.
- **I/O syscalls and file-descriptor internals**: `open`→fd→`struct file`→`file_operations`→VFS→block/device layer, `read`/`write` buffering (page cache), `mmap`, and how `fd` tables are shared across fork.
- **Syscall mechanism and userspace glue**: what `syscall(2)` does — `int 0x80` vs `syscall` (vsyscall/vdso), `syscall_table`, argument passing, `strace`/`perf` visibility, and the glibc `SYSCALL_WRAPPER` path.
- **Deep-dive concepts and interview synthesis**: namespaces/cgroups, `/proc` and `sysfs`, context switch internals, `perf`/`strace`, and the big "what happens when…" answers.

## Prerequisites (linked)
- [Part 02 Processes and Threads](part-02-processes-and-threads/README.md) — what a process is, states, context switch, threads.
- [Part 03 CPU Scheduling](part-03-cpu-scheduling/README.md) — the scheduler this chapter's `task_struct` feeds.
- [Part 07 Virtual Memory](part-07-virtual-memory/README.md) — paging, page tables, TLB, mmap.
- [Part 08 File Systems](part-08-file-systems-and-storage/README.md) — the VFS/block layer this chapter's I/O path hits.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Process Lifecycle and Scheduling Practice](section-01-process-lifecycle-and-scheduling-practice.md) | What happens in `fork`/`exec`/`exit`, and how does the CFS run them? |
| 02 | [Address Space and Kernel Memory Layout](section-02-address-space-and-kernel-memory-layout.md) | How is user + kernel virtual memory arranged on x86-64? |
| 03 | [I/O Syscalls and File Descriptor Internals](section-03-io-syscalls-and-fd-internals.md) | What's behind `open`→`fd`, `read`/`write`, and `mmap`? |
| 04 | [Syscall Mechanism and Userspace Glue](section-04-syscall-mechanism-and-userspace-glue.md) | How does a C function call become a kernel syscall? |
| 05 | [Linux Internals: Concepts and Interview Synthesis](section-05-linux-internals-concepts-and-interview-questions.md) | Namespaces, cgroups, `/proc`, context switch, and "what happens when you type a command?" |

## One-paragraph narrative connecting all sections
This chapter turns Part 02/03/07/08's theory into kernel reality. Section 01 follows a process through `fork` (copy-on-write page tables + shared `task_struct` fields), `exec` (fresh mm + program loading), and `exit` (zombie → reaped by `wait`), then shows how the Completely Fair Scheduler (`CFS`, red-black tree of `sched_entity`s, `vruntime`) picks which `task_struct` runs next. Section 02 maps the address space those tasks live in: the user layout (code/data/heap/`brk`/mmap/stack, `0x00400000`→`0x7fff...`) and the kernel half (`PAGE_OFFSET`/direct map, `vmalloc` region, `vmemmap`, fixmap, `kasan`), with `kmalloc` vs `vmalloc` and two-level page tables. Section 03 walks the I/O path: `open` allocates an fd → `struct file` → VFS `f_op` (Part 08) → page cache → block layer → device, and explains fd sharing across `fork`/`dup`/`dup2`. Section 04 shows the boundary crossing: `syscall`/`int 0x80`, the syscall table, argument registers, `strace`, and the vdso/vsyscall fast paths that skip the trap entirely. Section 05 ties it together: namespaces/cgroups (containers), `/proc` and `sysfs` as the observable kernel, context-switch anatomy, and the classic "what actually happens when you type a command" answer — the interview capstone.

## Common interview trap in this chapter
**Trap:** Saying `fork` *copies* the process (it's copy-on-write — pages are shared until a write); saying user space "is above kernel space in memory" without noting the split is at the top of the 48-bit space on x86-64 (`0xffff800000000000`); confusing fd tables (shared across `fork`), open file descriptions (`struct file`, shared across `dup`), and inodes; and thinking `kmalloc` vs `vmalloc` is about size only (it's about *contiguity in physical vs virtual address space*). Also: "type a command" questions reward the full trace — shell → fork/exec → loader → `_start` → main → syscalls — not a one-liner.

## Checklist before moving on
- [ ] I can trace `fork`→`exec`→`exit` with COW and `CLONE_*` flags.
- [ ] I can draw the x86-64 user + kernel address layout and explain `kmalloc` vs `vmalloc`.
- [ ] I can walk `open`→fd→`struct file`→VFS→block I/O and explain fd sharing.
- [ ] I can explain the syscall mechanism (`syscall`/`int 0x80`, table, args, vdso, `strace`).
- [ ] I can explain namespaces, cgroups, `/proc`, context switch, and "what happens when you type a command".
- [ ] Each section meets the 22-block template with real kernel references and 10–20 Q&A.
