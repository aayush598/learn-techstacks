# Chapter: Context Switching

## What you'll learn
- Exactly what a context switch does: saving one task's register/stack state and loading another's, plus the address-space switch (CR3/TLB) between processes.
- Why context switches are expensive in practice — TLB/cache cold misses, syscall crossings, kernel entry/exit — and how modern CPUs and kernels mitigate them (PCID, KPTI trade-offs, runqueue locality).
- The difference between a mode switch, a thread switch, and a process switch.
- Production techniques to reduce switching cost: CPU affinity, cooperative batching, `sched_yield` misuse, and why too many threads hurt.

## Prerequisites (linked)
- [Ch-01 Process Concept](../chapter-01-process-concept/README.md) — PCB, task_struct.
- [Ch-03 Threads](../chapter-03-threads/README.md) — why thread switches are cheaper (shared mm).
- [Part 01 Ch-02 Kernel Architecture](../../part-01-os-fundamentals/chapter-02-kernel-architecture/README.md) — kernel mode, interrupts, syscalls.
- Feeds into [Part 03 (CPU Scheduling)](../../part-03-cpu-scheduling/README.md) — the scheduler *decides*, the context switch *executes*.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Context Switch Internals](section-01-context-switch-internals.md) | The save/restore mechanics, switch_mm/switch_to, and thread vs process switch |
| [Section 02 — Context Switch Cost and Mitigation](section-02-context-switch-cost-and-mitigation.md) | The real costs (TLB/cache) and the engineering that reduces them |

## One-paragraph narrative connecting all sections
A context switch is the act that makes multitasking real: the kernel saves the running task's registers and kernel stack, picks the next task, and restores it (Section 01). For processes the switch also changes the address space — reloading CR3 and paying TLB/cache misses, which is why process switches are measurably more expensive than thread switches (Section 02). Understanding the mechanics (Section 01) and the costs (Section 02) lets you answer both "what happens during a switch" and "why is my system slow from switching" — the two directions interviews probe.

## Common interview trap in this chapter
Conflating **mode switch** (user→kernel for a syscall, same process) with **context switch** (saving one task, restoring another). A syscall does a mode switch; a context switch also involves changing the running task. Also: claiming modern context switches "flush the TLB every time" — PCID and ASID make that false; the *cost* is more nuanced (partial TLB retention + cache coldness).

## Checklist before moving on
- [ ] I can describe the register/kernel-stack save-restore sequence of a context switch.
- [ ] I can explain why thread switches skip `switch_mm` and process switches don't.
- [ ] I can quantify context-switch cost (~1-5µs threads, 2-10µs+ processes) and name the dominant factors (TLB/cache).
- [ ] I can distinguish mode switch vs context switch.
- [ ] I can list at least 3 mitigations (CPU affinity, PCID/ASID, runqueue locality, batching, thread-per-core).
- [ ] I know where the Linux code lives (`switch_to`, `switch_mm`, `context_switch` in kernel/sched/core.c).
