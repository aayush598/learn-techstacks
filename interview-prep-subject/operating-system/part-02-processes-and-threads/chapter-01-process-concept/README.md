# Chapter: Process Concept

## What you'll learn
- The precise definition of a process as a program in execution, and how it differs from a program (the file) and a thread (the execution unit).
- The process life cycle: new → ready → running → waiting → terminated, and when each transition happens (with the classic 7-state model including suspend states).
- The Process Control Block (PCB) — the kernel's per-process data structure — field by field.
- The real kernel structures behind it: Linux `task_struct`, `mm_struct`, `files_struct`, and `cred`.

## Prerequisites (linked)
- [Part 01 Ch-02 (Kernel Architecture)](../../part-01-os-fundamentals/chapter-02-kernel-architecture/README.md) — user/kernel mode, syscalls.
- [Part 01 Ch-03 (Linux Architecture)](../../part-01-os-fundamentals/chapter-03-linux-architecture/README.md) — /proc, task_struct context.
- Feeds into [Ch-02 (Creation & Termination)](../chapter-02-process-creation-and-termination/README.md) and [Ch-03 (Threads)](../chapter-03-threads/README.md).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — What is a Process](section-01-what-is-a-process.md) | Program vs process; the 4 segments; the process's address space |
| [Section 02 — Process States and Life Cycle](section-02-process-states-and-life-cycle.md) | 5-state + 7-state models; transition triggers |
| [Section 03 — Process Control Block (PCB)](section-03-process-control-block-pcb.md) | Every field the kernel keeps per process; Linux task_struct |
| [Section 04 — Process vs Program vs Thread](section-04-process-vs-program-vs-thread.md) | The three-way distinction that opens most interviews |

## One-paragraph narrative connecting all sections
A process is a program *in execution* — the dynamic entity with its own address space, PC, and state (Section 01). That dynamic nature means the OS must track it through a life cycle of states (ready, running, waiting...) as it competes for the CPU (Section 02). All the bookkeeping — registers, state, memory, files, priority — lives in one per-process kernel structure, the PCB (Section 03). Once you hold process, program, and thread straight — a process is an *execution instance with resources*, a thread is *an execution stream within it* — you can answer the opening questions of any OS interview (Section 04).

## Common interview trap in this chapter
Calling a **thread a lightweight process** without explaining *what's shared*. The real differentiator: threads share the address space and file table (context switch = registers + stack pointer), while processes don't (context switch = page tables + TLB flush + fd table). Also: `fork()` on Linux doesn't actually copy the whole address space — it uses **copy-on-write**; saying "fork copies all memory" is the single most common process-concepts mistake.

## Checklist before moving on
- [ ] I can define a process in one sentence and name its 4 memory segments.
- [ ] I can draw the 5-state diagram and name a trigger for every transition.
- [ ] I can list all PCB/task_struct fields from memory.
- [ ] I can explain the exact process vs program vs thread difference with an example.
- [ ] I can explain copy-on-write and why it makes fork cheap.
- [ ] I know what `/proc/<pid>/` exposes and can name 3 files under it.
