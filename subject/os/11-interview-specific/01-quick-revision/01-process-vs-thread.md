# Process vs Thread

| Property | Process | Thread |
|----------|---------|--------|
| **Weight** | Heavyweight | Lightweight |
| **Address Space** | Separate (isolated) | Shared (same address space) |
| **Context Switch** | Slow (TLB flush, page table switch) | Fast (registers + stack only) |
| **Creation** | fork() — expensive (COW) | pthread_create() — cheap |
| **IPC** | Pipes, sockets, shared memory, signals | Direct shared memory |
| **Failure** | One crash → other processes unaffected | One thread crash → whole process dies |
| **Protection** | OS protects address spaces | No protection between threads (same process) |
| **Data** | Owns code, data, heap, stack | Owns only stack + registers |
| **Identifier** | PID (Process ID) | TID (Thread ID) |
| **OS Unit** | PCB (Process Control Block) | TCB (Thread Control Block) |

## Memory Layout

```
Process:
  [Code][Data][Heap  ←  →  Stack]   ← isolated

Threads within Process:
  [Code][Data][Heap  ← T1 Stack][T2 Stack][T3 Stack]   ← shared code/data/heap
```

## Context Switch Cost
- **Process switch:** save/load registers + TLB flush + page table switch → ~5–10μs
- **Thread switch:** save/load registers only → ~1–2μs
- Same-process threads share page tables (no TLB flush needed)

## When to Use
- **Process:** strong isolation needed; separate programs; security-sensitive
- **Thread:** shared data access; low-latency communication; parallel computation

## System Limits
- Linux max PIDs: `cat /proc/sys/kernel/pid_max` (default 32768)
- Linux max threads: `cat /proc/sys/kernel/threads-max` (typically ~100k+)
- Thread creation ~1–10μs | Process creation ~50–200μs

## Interview Tip
- *"Threads share address space — no IPC needed, but no protection either"*
- Know **COW (Copy-on-Write)** for fork(): pages shared until modified
