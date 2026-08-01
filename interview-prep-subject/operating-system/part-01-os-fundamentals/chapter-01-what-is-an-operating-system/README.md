# Chapter: What is an Operating System

## What you'll learn
- The precise definition of an OS and the 5 jobs every OS does (resource allocation, process management, memory management, file/device management, security).
- The evolution of OS types and why each one exists (batch → multiprogramming → time-sharing → real-time → mobile/embedded).
- How an OS presents services to users (command interpreter, GUI, system calls) and to itself (kernel components).
- The difference between "the OS" (kernel) and "an operating system" (kernel + system utilities + application software).

## Prerequisites (linked)
- None strictly, but a high-level grasp of what hardware does (CPU executes instructions, RAM stores them, disks store data) from any CS101 course helps.
- Follow-up parts assume this chapter: [Part 02 (Processes & Threads)](../../part-02-processes-and-threads/README.md), [Part 03 (CPU Scheduling)](../../part-03-cpu-scheduling/README.md).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Role, Goals, and Functions of OS](section-01-role-goals-and-functions-of-os.md) | What the OS is *for*: allocator of scarce resources + virtualizer of hardware |
| [Section 02 — Types of Operating Systems](section-02-types-of-operating-systems.md) | Batch, multiprogrammed, time-sharing, RTOS, distributed, embedded |
| [Section 03 — OS Services and Components](section-03-os-services-and-components.md) | Services the OS provides and the components that provide them |

## One-paragraph narrative connecting all sections
An OS exists because raw hardware is unusable by humans and dangerous to share: it must allocate the CPU, memory, and devices among competing programs (Section 01). The design goal changed over time — batch systems optimized throughput, time-sharing systems optimized interactivity, RTOS systems optimize predictability — which is why so many *types* of OS exist (Section 02). Regardless of type, every OS exposes the same skeleton of services (UI, program execution, file/device management, protection, communication), which are implemented by internal components and reached by user programs through system calls (Section 03). Everything later — processes, threads, scheduling, sync, deadlocks — is a refinement of these three ideas.

## Common interview trap in this chapter
Candidates call the **shell (bash) or the GUI "the OS"**. They are not the kernel; they are user-space programs the kernel hosts. When an interviewer says "the OS," they almost always mean the kernel plus privileged system services. Saying "Linux is the kernel, GNU/Linux is the distribution" is a free differentiation point — use it.

## Checklist before moving on
- [ ] I can define OS in one sentence and name its 5 jobs.
- [ ] I can explain why multiprogramming (not just batch) was necessary.
- [ ] I can give a real example of a hard-real-time OS (FreeRTOS in a car airbag) vs soft real-time (video streaming).
- [ ] I can draw the layered OS diagram and point at each layer.
- [ ] I can distinguish kernel, system programs, and application programs.
- [ ] I know at least 5 real OS examples across types (Linux, Windows, macOS/XNU, FreeRTOS, QNX, z/OS).
