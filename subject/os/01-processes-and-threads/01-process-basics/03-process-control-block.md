# Process Control Block (PCB)

## What is PCB?
- **Kernel data structure** — one per process, stored in kernel memory
- OS can find any PCB via **PID-indexed table** or linked list
- Sole repository of all process metadata; necessary for **context switching**, **scheduling**, **resource mgmt**

## Detailed PCB Fields

| Category | Fields | Purpose |
|----------|--------|---------|
| **Identification** | PID, PPID (parent PID), UID (user) | Unique identity & ownership |
| **State** | current state, status flags | Running, ready, waiting, etc. |
| **CPU Registers** | PC, SP, general-purpose regs, condition codes | Saved/restored on context switch |
| **Scheduling** | priority, queue pointers, scheduling class, CPU burst time | Decides which process runs next |
| **Memory Mgmt** | base & limit registers, page table pointer, segment table | Address translation & protection |
| **Accounting** | CPU time used, real time, child CPU time, account limits | `getrusage()`, billing, resource limits |
| **I/O Status** | list of open file descriptors, I/O devices allocated | File table pointers, device state |
| **Signal Handling** | signal mask, signal dispositions (`SIG_IGN`, `SIG_DFL`, handler fn) | Per-process signal handling |

## PCB & Context Switching (Step-by-Step)

1. **Interrupt/System Call occurs** (e.g., timer, I/O)
2. CPU saves current PC & registers onto **kernel stack**
3. OS calls **scheduler** → picks next process from ready queue
4. **`switch_to()`** called:
   - Save current process registers into **current PCB** (in kernel memory)
   - Load saved registers from **next PCB**
   - Update **page table** / flush TLB
5. Restore PC → start executing next process

**Context switch overhead includes:**
- Saving/restoring ~20–100 registers
- TLB flush + cache misses for new process
- Scheduler dispatch code execution
- Typically **1–100 µs** on modern systems

## PCB Storage & Management

### Data Structures
- **Process Table**: Array/list of all PCBs in system (indexed by PID)
- **Ready Queue**: Linked list of PCBs in READY state
- **Wait Queues**: One per I/O device / event (PCBs in WAITING state)
- **Free List**: Pool of available PCB slots

```
           ┌───────────────────────────────────────────┐
           │            Process Table                   │
           │  ┌─────┬─────┬─────┬─────┬─────┐          │
           │  │PID 0│PID 1│PID 2│ ... │PID N│          │
           │  │ PCB │ PCB │ PCB │     │ PCB │          │
           │  └─────┴─────┴─────┴─────┴─────┘          │
           └───────────────────────────────────────────┘
                        ▲
                        │
           ┌────────────┴────────────┐
           │     ┌──────────┐        │
           │     │ Ready Q  │────────┤
           │     │ (linked  │─→      │
           │     │  list)   │        │
           │     └──────────┘        │
           │  Wait Q (disk) ◄─────── │
           │  Wait Q (keyboard) ◄─── │
           └─────────────────────────┘
```

### Key Design Points
- **PCB size**: Typically **a few KB** (~1–4 KB on Linux). Larger = more context switch overhead
- **Threads**: Each thread has its own TCB (Thread Control Block) — lighter than PCB
- **Linux**: `task_struct` defined in `<linux/sched.h>` — ~2 KB with thousands of fields
- **`clone()` vs `fork()`**: `fork()` creates new PCB; `clone()` (used by pthreads) shares address space

```c
// Key fields in Linux task_struct (simplified)
struct task_struct {
    volatile long state;          // process state
    pid_t pid;                    // process ID
    struct task_struct *parent;   // parent process
    struct list_head children;    // child processes
    struct mm_struct *mm;         // memory descriptor (page table, etc.)
    struct files_struct *files;   // open file descriptors
    const struct sched_class *sched_class;  // scheduling class
    struct thread_struct thread;  // CPU-specific state (registers, SP)
};
```
