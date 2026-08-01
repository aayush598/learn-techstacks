# Part 09: IPC and Linux Internals

## What this part covers
**Inter-process communication (IPC)** is how processes cooperate and exchange data: pipes/FIFOs, message queues, shared memory, semaphores, sockets, and signals — with POSIX vs System V API variants. **Linux internals** turns the theory into kernel reality: how processes are actually born, scheduled, and torn down; how the kernel address space is laid out (user vs kernel, the `0xc0000000` split, kmalloc/vmalloc, page tables); and how the syscall/`open`→`fd` machinery works inside `fs/`.

## Structure
| Part | Chapter | Sections | Status |
|---|---|---|---|
| 09 | [01 IPC Mechanisms](part-09-ipc-and-linux-internals/chapter-01-ipc-mechanisms/README.md) | 5 | pending |
| 09 | [02 Linux Internals Deep Dive](part-09-ipc-and-linux-internals/chapter-02-linux-internals-deep-dive/README.md) | 5 | pending |

## Prerequisites (linked)
- [Part 02 Processes and Threads](part-02-processes-and-threads/README.md) — processes, context switch, states.
- [Part 04 Process Synchronization](part-04-process-synchronization/README.md) — the synchronization primitives (mutex, semaphore) that IPC builds on.
- [Part 07 Virtual Memory](part-07-virtual-memory/README.md) — virtual address spaces, demand paging, mmap.

## How this part connects to the rest
IPC is the *why* of Part 04's synchronization: once processes share data (shared memory, pipes), they need the mutexes/semaphores to coordinate. The IPC chapter maps each mechanism to its kernel data structure (pipe inode + buffers, `msg_queue`, `shm_file`, semaphore arrays) and its use case (producer–consumer, client–server, streaming). The Linux Internals chapter then shows the concrete kernel code paths: `fork`/`exec`/`exit`, the C standard library's syscall glue and `syscall(2)`, the user/kernel address split and page tables, and the `open`→`fd`→`read`/`write` machinery through the VFS (tie to Part 08). Together they answer the interview's favorite "tell me what actually happens" questions: *"what happens when you fork?", "what happens when you type a command?", "how does a process talk to another?"*

## What you'll be able to do after this part
- Explain all six IPC mechanisms, when to use each, and their kernel structures.
- Compare POSIX vs System V IPC APIs and know which Linux uses.
- Trace `fork`→`exec`→`exit` and describe `CLONE_VM`/`CLONE_THREAD` flags.
- Draw the Linux virtual address space layout (user stack/heap/brk, kernel zone, vsyscall/vdso).
- Explain `mmap`, `kmalloc` vs `vmalloc`, and how page tables map user + kernel memory.
- Walk the `open(2)`→VFS→device-driver path and explain the file-descriptor table, `struct file`, and `fd` inheritance across fork.
- Answer the top "Linux internals" interview questions with kernel-level specifics.

## File map (this part)
- `part-09-ipc-and-linux-internals/README.md` (you are here)
- `chapter-01-ipc-mechanisms/README.md` + `section-01-…md` through `section-05-…md`
- `chapter-02-linux-internals-deep-dive/README.md` + `section-01-…md` through `section-05-…md`

## Completion checklist
- [ ] Part 09 README + 2 chapter READMEs created.
- [ ] 10 section files written (5 IPC + 5 Linux internals).
- [ ] Each section follows the 22-block template with TL;DR, real code, references, complexity, 10–20 Q&A.
- [ ] `find` verification shows the exact planned file list with zero skipped/renamed files.
