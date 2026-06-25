# User Thread vs Kernel Thread

## Comparison Table

| Property | User Thread | Kernel Thread |
|----------|-------------|---------------|
| **Managed by** | Thread library (pthreads, green threads) | OS kernel |
| **Creation speed** | Very fast (no syscall) | Slower (syscall needed) |
| **Context switch** | User-space only (fast) | Kernel trap (slower) |
| **Blocking I/O** | Blocked thread blocks **all** threads in process (M:1) | Only that thread blocks |
| **Multi-core** | Cannot utilize (M:1) — only 1 thread runs at a time | Yes, all threads can run in parallel |
| **System calls** | None needed for sync | Required for synchronization |
| **OS visibility** | Kernel sees only 1 process | Kernel sees all threads (schedules each) |
| **Example** | POSIX Pthreads (user-level), goroutines (before Go 1.2), Python threads (GIL) | Linux `clone()` with CLONE_THREAD, Windows threads |

## Threading Models

| Model | Description | User : Kernel | Pros | Cons |
|-------|-------------|---------------|------|------|
| **Many-to-One** (M:1) | All user threads map to 1 kernel thread | Many : 1 | Fast context switch | No multicore, one blocking blocks all |
| **One-to-One** (1:1) | Each user thread maps to 1 kernel thread | 1 : 1 | Full parallelism, blocking works | Slower creation, context switch |
| **Many-to-Many** (M:N) | User threads multiplex across kernel threads | Many : Many | Balanced | Complex to implement |

## Implementation Details
- **User threads:** scheduler in user space (setjmp/longjmp, or makecontext/swapcontext)
- **Kernel threads:** `clone()` system call with flags (CLONE_VM, CLONE_THREAD, etc.)
- Linux: `pthread_create` → `clone()` → kernel thread (1:1 model)

## Go Goroutines (Special Case)
- **Before Go 1.2:** M:N user threading
- **Now:** M:N with own scheduler (GMP model: Goroutine → Machine → Processor)
- Goroutine stack: starts at 2KB (vs ~1MB for kernel thread)
- Millions of goroutines feasible; kernel threads limited (~10k)

## Performance Numbers
- User thread context switch: **~0.1–0.5μs**
- Kernel thread context switch: **~1–5μs** (involves syscall)
- Creating: user thread ~1μs | kernel thread ~10–50μs

## Interview Tip
- *"Linux uses 1:1 threading — each pthread maps to a kernel thread via clone()"*
- *"Go rejected 1:1 for M:N to support millions of goroutines"*
- Know that **Python's GIL** effectively gives M:1 behavior (only one thread runs Python bytecode)
