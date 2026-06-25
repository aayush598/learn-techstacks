# Process Concept

## What is a Process?
- A **process** is a program in execution — an active entity
- Each process has its own **address space** and **resources**
- OS manages processes via the **Process Control Block (PCB)**

## Process Components (Memory Layout)
| Segment | Contents |
|---------|----------|
| **Text** | Executable code (read-only, fixed size) |
| **Data** | Global & static variables (`.data` + `.bss`) |
| **Heap** | Dynamically allocated memory (`malloc`/`free`) |
| **Stack** | Function call frames, local variables, return addresses |

```
┌─────────────────┐  high address
│     Stack       │  grows downward
│  (local vars)   │
├─────────────────┤
│       │         │
│       ▼         │  free memory (gap)
│       ▲         │
│       │         │
├─────────────────┤
│      Heap       │  grows upward
│  (malloc'ed)    │
├─────────────────┤
│  Data (BSS)     │  uninitialized static data
│  Data (Data)    │  initialized static data
├─────────────────┤
│      Text       │  program code (read-only)
└─────────────────┘  low address
```

## Process vs Program
| Program | Process |
|---------|---------|
| Passive entity (file on disk) | Active entity (loaded in memory) |
| Static code + data | Dynamic — has state (PC, registers) |
| Single program → multiple processes | Multiple instances of same program |
| No PCB | Has PCB for OS management |

## Process Control Block (PCB) — Key Fields
- **PID** (unique process identifier)
- **Process State** (ready, running, waiting, etc.)
- **Program Counter** (address of next instruction)
- **CPU Registers** (saved during context switch)
- **Memory Limits** (base & limit registers, page tables)
- **Open File List** (file descriptors)
- **Scheduling Priority** & other accounting info

## Context Switching
- **What**: OS saves state of current process (registers, PC, etc. into PCB) and loads saved state of next process
- **Trigger**: Interrupts, system calls, timer expiry (quantum ends), I/O waiting
- **Overhead**: Pure overhead — CPU does no useful work during switch
  - Includes: saving/loading registers, TLB flush, cache invalidation, kernel scheduler dispatch
  - Typical time: **microseconds** (depends on hardware, OS, TLB size)
- **Key interview point**: Context switch time is wasted; high context switching → **thrashing** (overheads dominate useful work)
