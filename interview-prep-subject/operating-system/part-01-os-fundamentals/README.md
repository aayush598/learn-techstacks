# Part: OS Fundamentals

## What this part covers
Everything you need to answer the **first 30 seconds of any OS interview**: what an operating system actually is, why it exists, the layers it is built from (hardware → kernel → system libraries → utilities), how the kernel enforces security via privilege levels, and the mechanisms (system calls, interrupts, traps) through which user code talks to the kernel. This part ends with a deep dive into the Linux architecture as the concrete production-grade reference implementation you will be judged against at FAANG/MAANG.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 What is an Operating System | role/goals/functions, types of OS, OS services & components | Define the OS, explain its 5 roles, distinguish batch/time-sharing/RTOS/embedded, map services to system calls |
| ch-02 Kernel Architecture | user vs kernel mode, monolithic vs micro vs hybrid, system calls, interrupts/traps/exceptions, booting | Explain privilege rings, the syscall path, IDT/ISR flow, BIOS/UEFI boot sequence |
| ch-03 Linux Architecture | architecture overview, utility programs vs kernel | Draw the Linux block diagram, classify user-space tools, explain kernel modules & `vsyscall` |

## Study order
1. **ch-01** first — it gives the vocabulary (process, memory, device, file, security) used everywhere else.
2. **ch-02** — the kernel is the heart; understand modes, syscalls, and interrupts before anything else.
3. **ch-03** last — Linux ties it together and gives you real paths (`kernel/sys.c`, `/proc`) to cite in interviews.
Read every section in numbered order within a chapter; each section assumes the previous one.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐ (3/5)** — high-frequency as *warm-up* questions, but only 1-3 questions come from here in most interviews.
- **Emphasized by**: system-programming-heavy teams (Databricks, NVIDIA, Docker/Kubernetes orgs, Apple kernel team, Amazon L4->L5 system design screen); **Linux-only shops** (Red Hat, Canonical, most infra roles) rate this part 4-5 stars.
- Typical asked: "What happens when you type `ls`?" (syscall walkthrough), "user mode vs kernel mode", "monolithic vs microkernel", "how does booting work".

## How the parts connect (roadmap)
- Part 01 is the **foundation**: it introduces processes, memory, files, and CPU as concepts.
- **Part 02 (Processes & Threads)** builds directly on the syscall + kernel-mode foundation: `fork()`/`exec()`, the PCB, context switching are exactly the "mechanisms" Part 01 names.
- **Part 03 (CPU Scheduling)** answers the question "who gets the CPU and for how long" that Part 01 only gestured at with the scheduler concept.
- **Part 04 (Synchronization)** and **Part 05 (Deadlocks)** add concurrency correctness — the failure modes of the multitasking Part 01 enables.
- After finishing Part 05, you will have covered ~60% of a standard OS core course, missing only Memory Management and I/O/Storage (a future Part 06-10).
