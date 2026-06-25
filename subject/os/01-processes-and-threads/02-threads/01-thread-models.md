# Thread Models

## Thread Definition
- A **thread** is the **basic unit of CPU utilization** — the smallest sequence of programmed instructions the OS scheduler can manage
- A process can have **1+ threads** sharing the same address space
- **Process** = resource container (address space, files); **Thread** = execution entity

## Thread Components

### Per-Thread (private) — stored in **Thread Control Block (TCB)**
| Component | Purpose |
|-----------|---------|
| **TID** | Thread identifier |
| **Program Counter** | Next instruction to execute |
| **Register Set** | Saved CPU registers |
| **Stack** | Function calls, local variables |

### Shared by Threads of Same Process
- **Code section** (text)
- **Data section** (global/static variables)
- **Heap** (dynamically allocated memory)
- **Open file descriptors**
- **Signal handlers**
- **Current working directory**

```
┌─────────────────────────────────────┐
│           Process                   │
│  ┌────────┐  ┌────────┐  ┌────────┐│
│  │ Thread │  │ Thread │  │ Thread ││
│  │   1    │  │   2    │  │   3    ││
│  │ ────── │  │ ────── │  │ ────── ││
│  │  TID   │  │  TID   │  │  TID   ││
│  │  PC    │  │  PC    │  │  PC    ││
│  │  Regs  │  │  Regs  │  │  Regs  ││
│  │  Stack │  │  Stack │  │  Stack ││
│  └────────┘  └────────┘  └────────┘│
│  ┌─────────────────────────────┐    │
│  │  Shared: Code, Data, Heap,  │    │
│  │  Files, Signals             │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## Benefits of Multithreading
| Benefit | Explanation |
|---------|-------------|
| **Responsiveness** | One thread blocks, others continue (e.g., UI stays responsive during network call) |
| **Resource Sharing** | Threads share memory by default — no need for IPC |
| **Economy** | Creating a thread is cheaper than a process (no new address space) |
| **Scalability** | Threads can run on different CPUs/cores in parallel |

## User-Level vs Kernel-Level Threads

| Aspect | User-Level Threads (ULT) | Kernel-Level Threads (KLT) |
|--------|-------------------------|---------------------------|
| **Managed by** | Thread library (pthreads in user space) | OS kernel |
| **Kernel aware?** | No — kernel sees single process | Yes — kernel schedules each thread |
| **Creation speed** | Very fast (no syscall) | Slower (syscall overhead) |
| **Context switch** | User space — very fast | Kernel space — slower (mode switch) |
| **Parallelism** | ❌ Cannot run on multiple CPUs (one process = one scheduling unit) | ✅ Multiple threads can run on different cores |
| **Blocking** | One thread blocks → entire process blocks | Only that thread blocks |
| **Examples** | Early Java threads, GNU Pth | Linux NPTL, Windows threads |

### Key Insight
- ULT is **lightweight** but cannot exploit multi-core parallelism
- KLT is **heavier** but fully leverages multi-core CPUs
- Modern OS (Linux, Windows, macOS) use **kernel-level threads** via NPTL (Native POSIX Thread Library)
