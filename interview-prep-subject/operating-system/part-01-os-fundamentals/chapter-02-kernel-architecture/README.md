# Chapter: Kernel Architecture

## What you'll learn
- Why the CPU has privilege levels and what user vs kernel mode really means (ring model, `CPL`, `RPL`, syscall instructions).
- The three kernel design families — monolithic, microkernel, hybrid — and the real-world trade-offs that made Linux/Windows/macOS choose what they chose.
- The complete system-call path: from `syscall` instruction to `sys_call_table` to handler and back.
- The difference between interrupts, traps, and exceptions, and how the IDT dispatches them.
- The full boot sequence from power-on (UEFI/firmware) through kernel init to the first user-space process.

## Prerequisites (linked)
- [Part 01 Chapter 01 (What is an OS)](../chapter-01-what-is-an-operating-system/README.md) — vocabulary: processes, services, syscalls.
- Follow-up parts build on this: [Part 02 (Processes & Threads)](../../part-02-processes-and-threads/README.md) uses fork/exec syscalls; [Part 04 (Synchronization)](../../part-04-process-synchronization/README.md) uses futexes (a syscall).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Kernel vs User Mode and Privilege Levels](section-01-kernel-vs-user-mode-and-privilege-levels.md) | Rings, mode bits, and why isolation exists |
| [Section 02 — Monolithic vs Microkernel vs Hybrid](section-02-monolithic-vs-microkernel-vs-hybrid-kernel.md) | Kernel design families and the performance/isolation trade-off |
| [Section 03 — System Calls in Depth](section-03-system-calls-in-depth.md) | The full syscall path with x86-64 mechanics |
| [Section 04 — Interrupts, Traps, and Exceptions](section-04-interrupts-traps-and-exceptions.md) | Event handling: IDT, ISRs, top/bottom halves |
| [Section 05 — Booting Process](section-05-booting-process.md) | Power-on → firmware → bootloader → kernel → init |

## One-paragraph narrative connecting all sections
The kernel's whole job is to control hardware safely, which requires the CPU to distinguish privileged code from everything else — that's the user/kernel mode split enforced by ring levels (Section 01). How the privileged core is organized is a design choice: put everything in one big address space (monolithic), isolate everything into services (microkernel), or blend them (hybrid); Linux, Windows NT, and macOS chose different points on that spectrum for performance-versus-reliability reasons (Section 02). Once the design exists, the only doorway from user code into the privileged world is the system call — a precisely orchestrated trap through the syscall table (Section 03). Events arriving from outside (device I/O) or from software faults (divide-by-zero, page faults) enter through the same protected door via the IDT and are classified as interrupts, traps, or exceptions (Section 04). Finally, the entire machine must come to life from a cold start — firmware, bootloader, kernel init, and the first process — which is Section 05. Together these five give you "the kernel, end to end."

## Common interview trap in this chapter
Candidates think syscalls and interrupts are the same. They are not: syscalls are *synchronous, initiated by the user process*; interrupts are *asynchronous, initiated by hardware*. Also, a common error is claiming Linux "has no microkernel anywhere" — modern Linux has kernel modules, KVM, and microkernel-inspired isolation, and macOS/iOS XNU is genuinely hybrid (Mach + BSD). Be precise.

## Checklist before moving on
- [ ] I can draw the ring model and explain what each ring does in x86.
- [ ] I can name which syscall instruction x86-64 vs ARM64 uses (`syscall` vs `svc`).
- [ ] I can compare monolithic vs microkernel vs hybrid with real OS examples and the IPC-vs-isolation trade-off.
- [ ] I can trace a syscall from user `read()` to the kernel handler and back.
- [ ] I can classify an event as interrupt/trap/fault/abort with an example of each.
- [ ] I can explain top-half vs bottom-half (softirq/tasklet) interrupt processing.
- [ ] I can recite the boot chain: UEFI → GRUB → kernel → systemd (PID 1).
- [ ] I know where Linux kernel code lives for each concept (arch/x86/entry, kernel/irq, init/main.c).
