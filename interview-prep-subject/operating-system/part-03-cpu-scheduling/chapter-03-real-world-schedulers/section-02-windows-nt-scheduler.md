# Section 02: Windows NT Scheduler

> **TL;DR**: Windows schedules 32 priority levels (0-31) with a preemptive, quantum-based dispatcher. Priorities come from a priority class × thread base priority; interactive threads get dynamic boosts, then decay back — a priority-plus-boost hybrid (MLFQ spirit) running a ready bitmap that finds the highest-priority thread in O(1).

## 1. Why Does This Exist?
Windows needed a scheduler that gives *interactive responsiveness* (the desktop) while supporting foreground/background and real-time-ish classes. The NT dispatcher exists to express importance (priority classes), adapt to interactivity (dynamic boosts), bound CPU hogs (quantum), and run efficiently (O(1) ready-bitmap). Its design goal mirrors MLFQ's: interactive threads respond instantly; background work fills idle.

## 2. How Does It Work?
- **32 levels**: 0 = zero page thread (System Idle-ish), 1-15 = variable (dynamic) priority, 16-31 = real-time (fixed).
- **Priority class** (process-level): IDLE, BELOW_NORMAL, NORMAL, ABOVE_NORMAL, HIGH, REALTIME.
- **Base priority** (thread): 1-15 added to class base → thread's starting priority.
- **Dispatcher**: ready queues (32); a bitmap finds the highest non-empty queue → dispatch head (FIFO within a level); quantum (default ~2 system quanta, ~10-30ms) expiry → demote to end of queue, or to next lower priority on repeated expiry.
- **Dynamic boosts**: waiting on I/O, keyboard/mouse, window message, etc. → +1-6 boost for the blocked thread; when it wakes, it runs at boosted priority for one quantum then decays back to base. Foreground process gets +2 boost.
- **Balance Set Manager**: periodic scan boosts "starving" low-priority runnable threads to keep progress.
- **Starvation/inversion protection**: waiting threads get boosted (fixes inversion — see Part 04), and the scan fixes starvation.

## 3. When Is It Used?
- Default scheduler on Windows desktop and server.
- Priorities for background (IDLE class) vs interactive (NORMAL class with foreground boost) vs real-time (REALTIME class for drivers/timers).
- Adjust via Task Manager (process base priority), `SetPriorityClass`, `SetThreadPriority`.

## 4. Why Wasn't Another Approach Chosen?
- **Pure priority (static)**: starves low-priority and inverts. Rejected.
- **MLFQ literal**: Windows approximates MLFQ with *boosts* instead of multi-queue demotion — boosts are cheaper and adequate.
- **CFS-style fair share**: NT chose importance (priority) over strict share; the desktop wants "the interactive process wins" not "equal share."
- **EDF**: no deadlines in NT semantics.
The chosen design: **priority + dynamic boost + quantum decay + O(1) bitmap** — simple, responsive, and tunable per class.

## 5. Intuition
**An airport that always serves the "urgent" traveler next**: each passenger has a rank (class + base). When a passenger gets blocked (I/O, waiting for a gate — like a thread waiting for I/O), they get a *temporary VIP sticker* (boost) so they're served immediately when ready — the desk gives them the next agent. After serving, the sticker fades (decay) back to their real rank. A forever-urgent crowd (realtime class) always goes first.

## 6. Real-World Analogy
**A hospital ER triage with 32 acuity levels**: triage ranks patients (priority). A patient who was waiting for test results (I/O wait) gets a temporary "fast-track" boost when results arrive, so the nurse sees them promptly; after care, the boost decays. The FASTER scan (Balance Set Manager) periodically re-checks everyone who waited long (starvation) and bumps them. Level 31 (REALTIME) is always first — even ahead of most everything.

## 7. Formal Definition
- Priority P = class_base + base_priority, clamped 0-31.
  - IDLE class base 4, NORMAL 8, HIGH 13, REALTIME 24 (bases vary by process class).
- Quantum: default ~2 quanta (quantum = clock interval, ~15.6ms typical) → ~30ms; varies by edition and foreground/background.
- Ready queues: `KiDispatcherReadyListHead[32]` + `KiReadySummary` bitmap; pick = highest set bit, head of queue (FIFO per level).
- Boost: on I/O completion, mouse/keyboard, etc.; boosted priority lasts one quantum (or boost-only quanta), then decays to base.
- Real-time priorities (16-31) never get dynamic boosts; a real-time thread can preempt anything.

## 8. Example
A GUI app thread: NORMAL class (base 8) + thread base 0 → priority 8. User clicks (keyboard event): waiting on input gets +2-6 boost → runs at ~14 for one quantum, handles the click instantly, then decays to 8. A background renderer at priority 6 loses to it. A REALTIME thread at 20 preempts both. Balance Set Manager: if the priority-1 background thread hasn't run for ~1s, bump to ~15 briefly → progress guaranteed.

## 9. Internal Working
1. Thread blocks on a wait (I/O, object): priority boosted (boost value per wait type), inserted into ready list at boosted level.
2. Dispatcher picks highest non-empty level (bitmap find-first-set) → runs FIFO head.
3. Quantum expires: if thread used its boost quantum → decay to base and re-insert; if base and still > 0 quantum → move to end of same level; if "quantum rolled over" multiple times → demote one level (down to floor 1).
4. Foreground process: threads get +2 boost (configurable) → foreground responsiveness.
5. Balance Set Manager (every ~1s): scans for runnable threads stuck at low priority > threshold time → temporarily boost to 15 and run a couple quanta → prevents starvation.
6. Interrupts/DPCs: dispatch-level interrupts preempt; DPC queue runs after — scheduling is not simply highest-ready-thread when interrupt context is involved.

## 10. Time Complexity
- Find-highest-priority: O(1) — 32-bit bitmap `BitScanForward` on `KiReadySummary`.
- Enqueue/dequeue: O(1) per level FIFO.
- Quantum/boost bookkeeping: O(1) per event.
- Balance Set Manager scan: O(runnable threads) periodically (~1s) — the only O(n) part.

## 11. Advantages
- **Responsive**: boosts make interactive/foreground work snappy.
- **Expressive**: 32 levels + classes cover everything from background to real-time.
- **O(1) dispatch** — cheap even at high thread counts.
- **Robust**: boosts + balance scan prevent both inversion and starvation in practice.
- **Simple model** to reason about (priority + boost + quantum).

## 12. Disadvantages
- **Real-time class is dangerous**: a 31 thread (or a misbehaving driver thread) can starve everything below it.
- **Quantum-based** — energy/throughput tradeoff; background processes run at reduced quantum.
- **Boost heuristics** are tuned by Microsoft, not clean math (vs CFS's provable share).
- **FIFO within level** → a CPU hog can hold a priority level.
- Priorities are *global heuristic*, not workload-aware; no deadline support.

## 13. Interview Questions
1. **Q: Describe Windows scheduling.** A: 32 levels; class base + thread base priority; preemptive; quantum with dynamic boosts for interactive threads; O(1) ready bitmap.
2. **Q: What are the three priority ranges?** A: 0 = zero page thread; 1-15 = variable (dynamic, boostable); 16-31 = real-time (fixed, never boosted).
3. **Q: What is the priority class?** A: Process-level policy (IDLE → REALTIME) setting the base; thread base priority (1-15) is added to it.
4. **Q (TRICKY): Why does a thread get boosted on I/O completion?** A: It was waiting for the I/O; boosting it makes the completed work (e.g., a response) run immediately → better responsiveness; it decays after one quantum.
5. **Q: How does Windows prevent starvation?** A: Balance Set Manager periodically boosts long-waiting low-priority runnable threads so they progress.
6. **Q: How does Windows handle priority inversion?** A: Waiter-based boosts — when a high-priority thread waits on a lock held by a lower-priority thread, the owner is boosted to the waiter's priority (plus the balance manager). Similar to Linux's priority inheritance.
7. **Q: What's the quantum and how is it used?** A: Default ~2 clock intervals (≈10-30ms); expiry → requeue; repeated expiry → demote one level (until floor 1). Foreground processes get a longer quantum (configurable).
8. **Q (PRODUCTION): A REALTIME-priority thread starves the GUI. Why and fix?** A: REALTIME (16-31) never decays and preempts everything; the fix is to not use REALTIME for non-critical work — use HIGH class or set explicit base priorities.
9. **Q: What's the difference between real-time and variable priority?** A: Variable (1-15) gets boosts and decay; real-time (16-31) is fixed — it preempts variable threads and is never adjusted (except no boost).
10. **Q: How is the ready queue implemented?** A: 32 FIFO lists + a 32-bit ready bitmap; find highest priority via bit scan → O(1) dispatch.
11. **Q: Why is a boost limited to one quantum?** A: To prevent a repeatedly-woken thread from permanently living at high priority — the boost is transient, then it decays to base, keeping fairness.
12. **Q (TRICKY): Can the zero-page thread (priority 0) run during normal operation?** A: Only when nothing else is ready (it's the lowest) — it zeroes free pages at idle; effectively the Windows "idle" thread.

## 14. Follow-Up Questions
1. **Q: How do foreground vs background processes differ?** A: Foreground gets a base priority boost (+2) and a longer quantum; background processes can be at reduced priority (and in some editions reduced quantum).
2. **Q: What is the dispatcher lock?** A: A spinlock serializing access to the ready queues (KiDispatcherLock); since Vista most scheduling is per-CPU with a global lock used for cross-CPU decisions.
3. **Q: What's the relation to MLFQ?** A: NT's boost-on-wait + decay approximates MLFQ's adaptive priority without explicit multi-queues — "priority with feedback."
4. **Q: How does Windows do CPU affinity?** A: Process/thread affinity masks; the dispatcher tries to keep a thread on its last CPU (soft affinity) for cache warmth.
5. **Q: What about Hyper-Threading/SMT?** A: NT is aware of SMT siblings; it spreads load and avoids scheduling latency-critical threads on the same core as each other.

## 15. Coding Example
```c
/* Windows: setting priorities (kernel-mode example semantics) */
#include <windows.h>

void set_thread_priorities(void) {
    /* process-level class */
    SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS);

    /* thread-level base priority (class base + delta) */
    SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_ABOVE_NORMAL);

    /* real-time class + highest delta → level ~31 */
    HANDLE rt = CreateThread(NULL, 0, NULL, NULL, 0, NULL);
    SetThreadPriority(rt, THREAD_PRIORITY_TIME_CRITICAL); /* 15 + class base */
    /* THREAD_PRIORITY_TIME_CRITICAL = base 15 → with REALTIME class ≈ 31 */
}
```
```powershell
# Inspect priorities on a live Windows system
Get-Process | Select-Object Name, BasePriority
Get-Process -Id <pid> | Select-Object PriorityClass
```

## 16. Industry Usage
- **All Windows** — desktop and server — through the NT dispatcher.
- **Game streaming/foreground apps**: foreground boost + input boosts keep the UX smooth.
- **Servers**: NORMAL/HIGH classes for critical services; REALTIME for driver/timer threads (rarely user-mode).
- **Audio**: REALTIME-class threads for glitch-free buffers (though typical audio stacks use boost-on-I/O).
- **Windows Internals** is the canonical reference — interviewer favorite for "how does Windows schedule?"

## 17. References
- Russinovich, Solomon, Ionescu, *Windows Internals*, 7th ed., ch. 5 (Processes, Threads, Scheduling).
- Microsoft docs: `SetPriorityClass`, `SetThreadPriority`, scheduling (learn.microsoft.com).
- Windows Internals blog series (Alex Ionescu, David Solomon).

## 18. Cheat Sheet
- 32 levels: 0 zero-page; 1-15 variable; 16-31 real-time.
- Priority = class base + thread base (clamped).
- Classes: IDLE→REALTIME (4/8/13/24 bases).
- Quantum ~2 intervals (~10-30ms); expiry → requeue/demote.
- Boost on I/O/input waits (+2-6); decays after 1 quantum; foreground +2.
- Balance Set Manager (~1s) fixes starvation.
- Waiter boosts fix inversion.
- Ready bitmap → O(1) highest-priority pick.
- REALTIME is never boosted — dangerous if overused.

## 19. Quiz
1. Windows priority levels: a) 140 b) 32 c) 99 d) 256 → **b**
2. Variable range: a) 0-31 b) 1-15 c) 16-31 d) 0-7 → **b**
3. Boost happens on: a) CPU expiry b) I/O completion c) boot d) fork → **b**
4. Boost duration: a) forever b) one quantum c) 1s d) until demote → **b**
5. Balance Set Manager prevents: a) inversion b) starvation c) fragmentation d) boosting → **b**
6. Ready pick cost: a) O(n) b) O(1) c) O(log n) d) O(32) → **b**
7. REALTIME threads: a) boosted b) never boosted c) decay d) idle → **b**
8. Foreground process gets: a) -2 b) +2 boost c) none d) RT → **b**
9. Priority = class base + ? a) quantum b) thread base c) boost d) affinity → **b**
10. Inversion fix: a) balance scan b) waiter boost c) quantum d) priority class → **b**

## 20. Flashcards
- **Q: Levels?** → **A:** 32 (0 zero-page, 1-15 variable, 16-31 RT).
- **Q: Boost on?** → **A:** I/O/input wait completion; decays after 1 quantum.
- **Q: Starvation fix?** → **A:** Balance Set Manager.
- **Q: Inversion fix?** → **A:** Waiter-based priority boost.
- **Q: Ready pick?** → **A:** O(1) bitmap.
- **Q: REALTIME?** → **A:** Fixed 16-31, never boosted.
- **Q: Foreground?** → **A:** +2 base boost.
- **Q: Quantum?** → **A:** ~2 intervals (~10-30ms).

## 21. Revision
Windows dispatches threads across 32 priority levels = process class base + thread base priority. Variable levels (1-15) get dynamic boosts when their I/O/input completes (decaying after a quantum) — an MLFQ-like adaptive feedback — plus a foreground boost, while real-time levels (16-31) are fixed and preempt everything. Starvation is handled by the Balance Set Manager and inversion by waiter boosts. Ready queues are 32 FIFOs + a bitmap → O(1) dispatch.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe Windows scheduling" | 13 Q1 / 2 How It Works |
| "Three priority ranges?" | 13 Q2 / 7 Formal Definition |
| "What is priority class?" | 13 Q3 / 7 Formal Definition |
| "Why boost on I/O?" | 13 Q4 / 5 Intuition |
| "Starvation prevention?" | 13 Q5 / 9 Internal Working |
| "Inversion handling?" | 13 Q6 / 9 Internal Working |
| "Quantum usage?" | 13 Q7 / 2 How It Works |
| "REALTIME thread starving GUI?" | 13 Q8 / 12 Disadvantages |
| "Ready queue impl?" | 13 Q10 / 10 Time Complexity |
| "Why boost limited to one quantum?" | 13 Q11 / 12 Disadvantages |
