# MASTER TEMPLATE — Every Section File Must Follow This Exact Structure

> This template guarantees **one-read understanding** at any level (basic → production). Every `.md` section file in every subject folder MUST contain ALL 22 blocks below, in this order. Section files live inside `part/chapter/section-file.md`.

---

## File Name Convention
- Lowercase, hyphen-separated: `section-01-what-is-an-os.md`
- Prefix numbers for ordering: `chapter-01`, `section-01`, `part-01`

## Heading Structure
```
# <Topic Title>

> **TL;DR**: One-sentence summary (what it is + why it matters in one breath).

## 1. Why Does This Exist?            <- motivation / the problem it solves
## 2. How Does It Work?               <- mechanism at a glance
## 3. When Is It Used?                <- production use-cases
## 4. Why Wasn't Another Approach Chosen?  <- alternatives + trade-offs (CRITICAL)
## 5. Intuition                       <- build mental model first, no jargon
## 6. Real-World Analogy              <- everyday-life comparison
## 7. Formal Definition               <- precise, textbook-grade definition
## 8. Example                         <- concrete worked example with numbers/steps
## 9. Internal Working                <- step-by-step internals / data structures / flow
## 10. Time Complexity                <- Big-O analysis (if applicable)
## 11. Advantages                     <- bullet list
## 12. Disadvantages                  <- bullet list (be honest)
## 13. Interview Questions            <- 10-20 Q&A (crisp answers)
## 14. Follow-Up Questions            <- deeper/probing questions (with short answers)
## 15. Coding Example                 <- pseudocode or real code (Java/C/Python)
## 16. Industry Usage                 <- how FAANG/MAANG/production systems use it
## 17. References                     <- real, verifiable sources (books, RFCs, docs, URLs)
## 18. Cheat Sheet                    <- 5-10 quick bullets to memorize
## 19. Quiz                           <- 5-10 MCQs with answers at the end
## 20. Flashcards                     <- 5-8 Q→A pairs for spaced repetition
## 21. Revision                       <- 30-second "read this before interview" recap
## 22. What Interview Questions Come From This Section?  <- question-mapping table
```

---

## Content Rules (MANDATORY)

1. **Every sentence answers a question**: Why does this exist? / How does it work? / When is it used? / Why wasn't another approach chosen? / What interview questions come from it?
2. **Intuition FIRST**: explain the "aha" before any formula. A reader must understand *why* before *what*.
3. **Analogy for every concept**: always give a real-world analogy (restaurant, library, highway, courier, etc.).
4. **Numbers and steps**: every example must be concrete (walk through it step-by-step with actual values).
5. **Interview depth**: include easy → medium → hard questions. Include **tricky, practical, production-grade, scenario-based** questions. Assume the interviewer is at FAANG/MAANG level.
6. **No fluff**: no filler sentences. Dense, high-signal, skimmable with headers.
7. **Consistency**: same 22 blocks, same order, in every file. Do NOT skip blocks.
8. **Accuracy**: correctness over volume. Every claim must be true to real systems (Linux kernel, TCP/IP, Postgres, JVM, etc.).
9. **Code blocks** where relevant with language tags (```java, ```c, ```python, ```sql, ```pseudocode).
10. **Part/Chapter READMEs**: each `part-XX` and each `chapter-XX` folder should contain a `README.md` that lists its contents and connects the concepts.

## Folder Hierarchy (recursive)
```
interview-prep-subject/
└── <subject>/
    └── part-XX-<part-name>/
        ├── README.md
        └── chapter-XX-<chapter-name>/
            ├── README.md
            └── section-XX-<section-name>.md   (ONE TOPIC PER FILE, full template)
```

---

## Chapter README Format
```
# Chapter: <name>
## What you'll learn
## Prerequisites (linked)
## Sections (linked table)
## One-paragraph narrative connecting all sections
## Common interview trap in this chapter
## Checklist before moving on
```

## Part README Format
```
# Part: <name>
## What this part covers
## Chapter map (table: chapter → sections → key skills)
## Study order
## Interview importance (0-5 stars) + which companies emphasize it
## How the parts connect (roadmap)
```

---

## Example of a fully filled section file (reference — this is the STANDARD):

`# Process Control Block`

> **TL;DR**: A PCB is a kernel data structure that stores everything the OS needs to manage one process (state, registers, memory, priority) — it's the process's "identity card."

## 1. Why Does This Exist?
Without a PCB, the OS would have nowhere to store a process's saved registers and memory info, so it could never pause and resume a process (context switching would be impossible). It exists because a process is a *dynamic, changing* entity that must be suspended and resumed.

## 2. How Does It Work?
Every process has exactly one PCB, created at process creation and freed at termination. On every context switch, the OS saves the outgoing process's state into its PCB and loads the incoming process's state from its PCB.

## 3. When Is It Used?
- On `fork()`/`exec()` in Linux
- On every timer interrupt (scheduler tick)
- On I/O waits, signals, process exit
- In debugging (`ps`, `/proc/<pid>/` on Linux reads PCB data)

## 4. Why Wasn't Another Approach Chosen?
Alternative: store process state inline in the process's own memory. Rejected because the process is suspended and may not be resident/mapped — the OS needs *its own* protected structure. Alternative: one global table (older Unix). Rejected for cache locality and scalability — per-process PCB + per-CPU runqueues scale better.

## 5. Intuition
Think of a passenger who keeps getting on and off a train. The station master's clipboard (PCB) records exactly where each passenger is, their seat, destination, and ticket — so they can be resumed perfectly when the next train arrives. The process is the passenger; the CPU is the train; the clipboard is the PCB.

## 6. Real-World Analogy
A bookmarks/locker analogy: a PCB is like a "save game" slot in a video game — it stores the full state so the game can be paused and resumed exactly where it left off.

## 7. Formal Definition
A process control block (PCB), also called task control block (TCB), is a kernel-maintained data structure that contains the complete context of a process: process ID, process state, program counter, CPU registers, CPU-scheduling information, memory-management information, accounting information, and I/O status information.

## 8. Example
PID 2345 in `fork()`: parent creates child → kernel allocates a fresh PCB → copies parent's fields, sets child's state to READY, links PCB into the ready queue → returns PID 2345 to parent and 0 to child.

## 9. Internal Working
1. Process created → kernel calls `alloc_pid()` + `dup_task_struct()` → PCB memory allocated from kernel heap.
2. PCB fields initialized (state=NEW/READY, PC=entry, registers copied, memory struct, files struct).
3. PCB linked into a global process list (`list_head` in `task_struct`) + the appropriate scheduler queue.
4. Timer tick / syscall → `schedule()` runs → `context_switch()` saves `regs` into old PCB, loads from new PCB, updates `CR3`/page table pointer, flushes TLB.
5. `exit()` → PCB freed, parent notified via `wait()`, zombie PCB kept until reaped.

## 10. Time Complexity
- Create: O(1) amortized (slab cache for `task_struct`).
- Context switch: O(1) — fixed number of register save/loads (no per-size scan).
- Scheduler lookup: O(1) with O(1) scheduler; O(n) naive scan of ready queue.
- Memory: a few KB per process (`task_struct` ≈ 2 KB on x86-64 Linux).

## 11. Advantages
- Enables preemptive multitasking, context switching, isolation of process state, and priority scheduling.
- Decouples process execution from physical CPU: a process can migrate CPUs.

## 12. Disadvantages
- Overhead: PCB allocate/free + context-switch cost (register saves, TLB flush, cache miss).
- Fixed-size fields can waste memory; huge structs hurt cache locality.

## 13. Interview Questions
1. **Q: What is a PCB and what does it store?** A: ... (full answer required)
... [10-20 questions]

## 14. Follow-Up Questions
1. **Q: Why is a context switch expensive?** A: ...

## 15. Coding Example
```c
// Simulating a minimal PCB in C
struct pcb { int pid; int state; int pc; int regs[32]; ... };
```

## 16. Industry Usage
Linux: `struct task_struct` in `include/linux/sched.h`; Windows: `KPROCESS`/`ETHREAD`; XNU: `proc`/`uthread`. Every RTOS (FreeRTOS TCB) and every microkernel uses it.

## 17. References
- Silberschatz, Operating System Concepts, Ch. 3 (Processes)
- Linux source: `kernel/fork.c`, `arch/x86/kernel/process_64.c`
- Tanenbaum, Modern Operating Systems, Ch. 2

## 18. Cheat Sheet
- PCB = the process's identity card / save-game slot
- Created on fork, freed on exit, zombie keeps PCB until reaped
- Contents: PID, state, PC, registers, memory info, scheduler info, I/O info

## 19. Quiz
1. Which is NOT stored in PCB? a) PC b) heap data c) registers d) PID → **b** ...
(answers listed at the end)

## 20. Flashcards
- **Q: What is a PCB?** → **A:** Kernel data structure storing one process's full context.

## 21. Revision
One-paragraph rapid recap: everything in 4-5 lines.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What happens during fork()?" | Internal Working / Example |
| "Why is context switch expensive?" | Internal Working / Time Complexity |
```

---

**REMINDER TO GENERATORS**: Follow this template EXACTLY for every single section file. Do not shorten. Do not reorder. Production-grade depth.
