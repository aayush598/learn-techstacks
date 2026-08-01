# Preemptive vs Non-Preemptive Scheduling

> **TL;DR**: In non-preemptive scheduling a running process keeps the CPU until it blocks or finishes; in preemptive scheduling the OS can forcibly take the CPU away (usually via a timer interrupt) — preemption is what makes interactive time-sharing possible, and the choice drives everything from fairness to real-time guarantees.

## 1. Why Does This Exist?
If the CPU can only be released *voluntarily*, one long-running process can freeze every other process for arbitrarily long — that's non-preemptive scheduling. The distinction exists because interactive and real-time systems need a guarantee: *no process can hog the CPU forever*. Preemption adds the mechanism (timer interrupt → scheduler may switch) that lets the OS reclaim the CPU on a schedule. The two modes exist as a design axis: non-preemption is simpler and lower-overhead but offers no response-time bounds; preemption enables responsiveness, fairness, and deadlines at the cost of complexity (and the need for synchronization — see Part 04).

## 2. How Does It Work?
- **Non-preemptive**: a task runs until it (a) blocks (I/O, lock, sleep), (b) terminates, or (c) yields. The scheduler only gets to choose a *new* task when the current one gives up the CPU. No timer-driven switching.
- **Preemptive**: a timer interrupt fires (e.g., every tick); the kernel may call `schedule()` and switch to another task even if the current one is mid-computation. Preemption also happens when a higher-priority task becomes ready (scheduler preempts the running task) — "preemption by wakeup."
- Linux: both coexist — CFS/EEVDF is preemptive (tick + wakeup preemption); `SCHED_FIFO` tasks are preempted only by higher-priority FIFO tasks; the RT and fair classes interact via the core scheduling layer.

## 3. When Is It Used?
- **Preemptive**: all general-purpose OSes (Linux CFS/EEVDF, Windows NT, macOS) — required for interactive response and fairness.
- **Non-preemptive**: some simple RTOS/embedded loop schedulers, early batch systems, kernels that run non-preemptible critical sections (though these are *regions*, not whole scheduling).
- **Hybrid within Linux**: `CONFIG_PREEMPT`/`PREEMPT_RT` control kernel preemption; user tasks are always preemptible; RT tasks use static priorities with preemption by higher RT tasks.

## 4. Why Wasn't Another Approach Chosen?
- **Pure non-preemptive**: simple, no timer needed, low overhead, deterministic per-task execution — but an uncooperative process starves everyone; rejected for general use (kept in tiny cooperative RTOS/embedded loops).
- **Pure preemptive (preempt everything always)**: best responsiveness but kernel critical sections become races (need locks), overhead per tick, and determinism suffers. Rejected; preemption is scoped (user tasks preemptible; kernel sections either non-preemptible or fine-grained PREEMPT_RT).
- **Cooperative (yield-based) with enforced yields**: needs all programs to be well-behaved; a buggy program never yields → hang. Rejected for robustness.
- **No preemption in kernel, only user (2.6 legacy)**: compromised — drivers hog CPU on SMP; PREEMPT_RT went further.
The chosen design: **preemptive user-level scheduling + controlled preemption in the kernel** — responsive and safe.

## 5. Intuition
Preemption is like a **basketball ref with a shot clock**. Non-preemptive: a team can hold the ball forever (a process runs until it's done — everyone else waits). Preemptive: the shot clock (timer interrupt) forces a change every N seconds — no stall, everyone gets a chance. The ref (kernel) also stops play if a star gets open (higher-priority task waking up).

## 6. Real-World Analogy
A **shared meeting room**: non-preemptive = whoever books the room first keeps it until they leave (block/finish); someone else's urgent meeting waits indefinitely. Preemptive = the facility manager (OS) sets a 1-hour timer (quantum) — when it rings, the room is reassigned to the next reservation (timer interrupt → context switch). If an emergency (high-priority task) needs it immediately, the manager preempts mid-meeting (wakeup preemption).

## 7. Formal Definition
- **Non-preemptive scheduling**: a running process retains the CPU until it blocks (I/O/lock), exits, or explicitly yields; the scheduler never forcibly removes it.
- **Preemptive scheduling**: the OS may interrupt a running process at any time (via a timer interrupt or a higher-priority task becoming ready) and reschedule the CPU; requires a dispatcher that can save/restore context mid-execution.
- **Dispatching vs preemption**: dispatching = switching to a chosen task; preemption = the *interrupt-driven decision* to forcibly switch.

## 8. Example
Jobs: A (burst 10, priority low), B (burst 2, arrives t=3), quantum 2.
- **Non-preemptive (FCFS, A first)**: A runs t=0-10 to completion; B waits until t=10, runs 10-12. B's response time = 10 (bad for interactivity).
- **Preemptive (RR, q=2)**: A runs 0-2,2-4 (B arrives at 3, joins queue), then B runs 4-6 → B's response = 1 (t=3 arrival, first CPU at 4). A finishes later. Preemption *costs* A time but *saves* B's interactivity — the whole point.

## 9. Internal Working
1. **Timer**: the local APIC/timer raises an interrupt every tick (or the scheduler uses hrtimers); kernel's `tick_handle_periodic` → scheduler tick → `scheduler_tick()`.
2. **scheduler_tick**: updates the current task's vruntime (EEVDF), checks if its time slice is exhausted or a higher-priority task should preempt; if so, `resched_curr()` sets TIF_NEED_RESCHED.
3. **Preemption point**: on return from interrupt (or at a preemption point in kernel), `__schedule()` runs if `need_resched` — a context switch occurs.
4. **Wakeup preemption**: `try_to_wake_up` → if the woken task has higher effective priority and preemption is enabled, it preempts the current task (for CFS: compares vruntime/delay; for RT: static priority).
5. **Non-preemptible regions**: while holding `spinlock`/in interrupt context, `preempt_count` blocks preemption; `PREEMPT_RT` makes most kernel regions preemptible with priority-inheritance locks.

## 10. Time Complexity
- Preemption check per tick: O(1) (`need_resched` flag).
- Pick-next after preemption: O(1) amortized (EEVDF leftmost), O(log n) worst.
- Context switch per preemption: O(1) + microarchitectural cost.
- Overhead of ticking: proportional to tick rate (NO_HZ reduces idle ticking).
- Non-preemptive path: zero timer cost (no forced switches).

## 11. Advantages
**Preemptive**: guaranteed response bounds (no starvation by a hog); fairness via time slicing; supports priorities & real-time; makes the system interactive.
**Non-preemptive**: simpler (no timer, no races from forced switches); lower overhead; deterministic per-task completion; simpler synchronization (no mid-critical-section preemption in user code).

## 12. Disadvantages
**Preemptive**: overhead (ticks + switches); races on shared data (must use locks — Part 04); harder determinism; priority inversion / convoy effects possible (mitigated by inheritance).
**Non-preemptive**: a long-running task freezes the system; no response guarantees; unfair; unsuitable for interactive/RT.

## 13. Interview Questions
1. **Q: What's the difference between preemptive and non-preemptive scheduling?** A: Non-preemptive: a running task keeps the CPU until it blocks, exits, or yields. Preemptive: the OS (timer interrupt or higher-priority wakeup) can forcibly switch tasks at any time.
2. **Q: Why is preemption necessary for interactive systems?** A: Without it, one compute-heavy process could hold the CPU indefinitely — everyone else's response time is unbounded. A timer-driven preemption bounds how long anyone can monopolize the CPU.
3. **Q (TRICKY): Is FCFS always non-preemptive?** A: FCFS is *defined* non-preemptively (first-come, first-served, run-to-completion). But a "preemptive FCFS" variant exists conceptually in RR-with-infinite-quantum... no — FCFS run-to-completion IS non-preemptive; preemption requires a timer, which FCFS lacks.
4. **Q: What mechanism does preemption require that non-preemption doesn't?** A: A timer interrupt (to forcibly switch) plus a dispatcher able to save/restore mid-execution (context switch) and a `need_resched` decision path.
5. **Q: Is SJF preemptive or non-preemptive?** A: Both exist: non-preemptive SJF (run to completion, then pick shortest) and preemptive SJF = **SRTF** (shortest remaining time first — preempt when a shorter job arrives).
6. **Q (SCENARIO): A high-priority task arrives while a low-priority task runs. When does it run?** A: Under preemptive scheduling, immediately (or at the next preemption point); under non-preemptive, only when the current task blocks/exits. Preemption by wakeup is what makes priorities meaningful.
7. **Q: What is the "convoy effect"?** A: In non-preemptive FCFS, one long CPU-bound job arriving first delays many short jobs behind it — poor TAT. Preemption (RR/SRTF) breaks the convoy.
8. **Q: Why must kernel code sometimes be non-preemptible?** A: To protect critical sections — if a task is preempted while holding a spinlock, another CPU spinning on that lock stalls (or worse, deadlock). Preemption is disabled inside those regions (`preempt_count`); PREEMPT_RT shrinks them with sleepable locks.
9. **Q: How does the timer interrupt trigger preemption in Linux?** A: `scheduler_tick()` updates vruntime, and if the task exceeded its slice (or a higher-priority task is pending), it sets `TIF_NEED_RESCHED`; on return from interrupt, `schedule()` runs — a context switch.
10. **Q: What is preemption in RTOS terms?** A: Fixed-priority preemptive: the highest-priority ready task always runs; a higher-priority task preempts immediately (FreeRTOS `configUSE_PREEMPTION`). Contrast with cooperative (task must yield).
11. **Q (PRODUCTION): You set a process to `SCHED_FIFO` but it's still preempted. Why?** A: `SCHED_FIFO` is preempted by *higher-priority* RT tasks and by the deadline class; also by hardware interrupts/NMIs. It is NOT preempted by CFS (fair) tasks — but the RT class itself has priority ordering.
12. **Q: What is the difference between "preempted" and "blocked"?** A: Preempted = forcibly switched out while still runnable (timer/wakeup); blocked = waiting for an event (I/O/lock), not runnable. Preempted tasks stay on the runqueue; blocked tasks leave it.
13. **Q: What are preemption points?** A: Places in kernel code where preemption is explicitly allowed (`cond_resched()`, syscall exit, interrupt return) — used to bound latency without disabling preemption globally.
14. **Q: Why does a non-preemptive design make synchronization easier?** A: Without forced switches, a task can't be interrupted mid-critical-section by another task on the same CPU — user-level critical sections need no locks in uniprocessor non-preemptive kernels (though SMP still needs them).
15. **Q (TRICKY): Can a non-preemptive OS still do timesharing?** A: Not meaningfully — timesharing requires forced time-slicing (preemption). A "cooperative multitasking" OS (old Mac OS) is non-preemptive: apps must yield; a stuck app freezes everything.

## 14. Follow-Up Questions
1. **Q: What is `TIF_NEED_RESCHED`?** A: A per-task flag set when the scheduler wants to switch; checked at preemption points (interrupt return, syscall return) — the Linux preemption mechanism.
2. **Q: What is the difference between tick preemption and wakeup preemption?** A: Tick: time-slice expiry via timer. Wakeup: a newly-ready higher-priority task preempts immediately (`try_to_wake_up` → `check_preempt_curr`). Both set need_resched.
3. **Q: What is PREEMPT_RT?** A: A kernel config making nearly the whole kernel preemptible (spinlocks → rtmutexes with priority inheritance), bounding kernel latency — the difference between "soft" and near-hard real-time on Linux.
4. **Q: What is `preempt_count`?** A: A per-task counter; non-zero disables preemption (inside locks, interrupt context); preemptible code checks it. Replaced conceptually by `preempt_disable()`/`preempt_enable()`.
5. **Q: How do RT and CFS coexist in the Linux core scheduler?** A: The core scheduler picks the highest *class* first (stop > dl > rt > fair > idle); within a class its own policy; RT tasks preempt fair tasks; balance via `push/pull`.

## 15. Coding Example
```c
/* FreeRTOS: preemptive vs cooperative scheduling knob */
#include "FreeRTOS.h"
#include "task.h"

/* configUSE_PREEMPTION (FreeRTOSConfig.h):
   1  = preemptive: higher-priority task preempts immediately (default)
   0  = cooperative: tasks must call taskYIELD() to switch            */

void vLow(void *p) {
    for (;;) {
        /* without preemption, this loop would starve others */
        taskYIELD();   /* cooperative: explicitly yield to higher tasks */
    }
}

void vHigh(void *p) {
    for (;;) { /* high priority: with preemption it runs immediately */ }
}

int main(void) {
    xTaskCreate(vHigh, "hi", 128, NULL, 3, NULL);
    xTaskCreate(vLow,  "lo", 128, NULL, 1, NULL);
    vTaskStartScheduler();   /* highest-priority-ready always runs */
    return 0;
}
```
```bash
# Watch preemption behavior on Linux
chrt -f -p 50 $$                        # set SCHED_FIFO priority 50
cat /proc/$$/sched | grep policy
# A FIFO task still yields to RT interrupts and higher RT prios
```

## 16. Industry Usage
- **Linux**: `kernel/sched/core.c` (`scheduler_tick`, `schedule`, `try_to_wake_up`), `kernel/sched/rt.c`, `kernel/sched/deadline.c`, `CONFIG_PREEMPT_RT` for real-time. Every cloud/desktop workload.
- **Windows NT**: preemptive with priority boost; dispatcher preempts lower-priority threads.
- **FreeRTOS/QNX**: fixed-priority preemptive (default); cooperative optional.
- **Embedded**: many MCU systems still run non-preemptive cooperative loops where determinism + simplicity beat responsiveness.
- **Real-time**: PREEMPT_RT, SCHED_DEADLINE (preemptive EDF) for industrial/robotics.
- **Interview angle**: preemption vs non-preemption is the entry question to priority, RR, and real-time scheduling — expect it early in any scheduling discussion.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 6.1-6.2 (Preemption, scheduling).
- Tanenbaum, *Modern OS*, Ch. 2.4 (Scheduling).
- Linux source: `kernel/sched/core.c`, `kernel/sched/rt.c`, `kernel/sched/fair.c`.
- Linux docs: `sched-design-CFS`, PREEMPT_RT wiki.
- FreeRTOS docs: "Scheduling" (configUSE_PREEMPTION).
- man: `chrt(1)`, `sched(7)`.

## 18. Cheat Sheet
- Non-preemptive: run until block/exit/yield. Preemptive: timer/wakeup can force a switch.
- Preemption needs: timer interrupt + dispatcher + need_resched.
- SJF (non-preemptive) vs SRTF (preemptive SJF).
- Convoy effect: one long job delays many — broken by preemption.
- Linux: TIF_NEED_RESCHED + scheduler_tick + try_to_wake_up.
- Kernel critical sections disable preemption (preempt_count); PREEMPT_RT shrinks them.
- SCHED_FIFO: preempted by higher RT prios and interrupts, not by CFS.
- Cooperative multitasking = non-preemptive (old Mac OS).
- Preempted (still runnable) vs blocked (waiting) are different.
- FreeRTOS configUSE_PREEMPTION selects the mode.

## 19. Quiz
1. Non-preemptive means the CPU is released: a) on timer b) only voluntarily c) by higher priority d) never → **b**
2. Preemption requires: a) a yield call b) a timer interrupt c) a process exit d) a reboot → **b**
3. SRTF is: a) non-preemptive SJF b) preemptive SJF c) RR d) FCFS → **b**
4. The convoy effect comes from: a) preemption b) FCFS non-preemptive c) priority d) quantum → **b**
5. `TIF_NEED_RESCHED` triggers schedule at: a) boot b) preemption points c) fork d) exec → **b**
6. Kernel critical sections disable: a) IRQs only b) preemption c) interrupts always d) memory → **b**
7. SCHED_FIFO is preempted by: a) CFS tasks b) higher RT prios c) nothing d) idle → **b**
8. A preempted task is: a) blocked b) still runnable c) zombie d) stopped → **b**
9. Cooperative multitasking is: a) preemptive b) non-preemptive c) both d) RT only → **b**
10. PREEMPT_RT makes: a) user tasks non-preemptible b) the kernel mostly preemptible c) RT slower d) IRQ disabled → **b**

## 20. Flashcards
- **Q: Non-preemptive?** → **A:** Task runs until block/exit/yield.
- **Q: Preemptive?** → **A:** Timer/wakeup can force a switch.
- **Q: What makes preemption possible?** → **A:** Timer interrupt + dispatcher + need_resched.
- **Q: SRTF?** → **A:** Preemptive SJF (shortest remaining time).
- **Q: Convoy effect?** → **A:** Long job first delays many short; preemption breaks it.
- **Q: TIF_NEED_RESCHED?** → **A:** Flag checked at preemption points.
- **Q: Why disable preemption in critical sections?** → **A:** Protect locks/shared kernel state.
- **Q: Preempted vs blocked?** → **A:** Runnable-but-switched vs waiting on event.
- **Q: SCHED_FIFO preemption?** → **A:** By higher RT prios/interrupts only.
- **Q: Cooperative multitasking?** → **A:** Non-preemptive (yield-based).

## 21. Revision
Preemptive scheduling lets the OS (via timer interrupt or higher-priority wakeup) forcibly switch tasks — giving response bounds, fairness, and priorities; non-preemptive runs tasks to block/exit/yield, which is simpler but allows starvation. SJF is non-preemptive, SRTF is its preemptive version. Linux uses TIF_NEED_RESCHED + scheduler_tick + wakeup preemption; kernel critical sections temporarily disable preemption (PREEMPT_RT minimizes these). Preempted (runnable) ≠ blocked (waiting). This distinction underlies RR, priority, and all of Part 04's synchronization.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Preemptive vs non-preemptive?" | 7 Formal Definition / 2 How It Works |
| "Why is preemption needed for interactive?" | 13 Q2 / 3 When Is It Used |
| "What does preemption require?" | 13 Q4 / 9 Internal Working |
| "Is SJF preemptive?" | 13 Q5 / 8 Example |
| "When does a high-priority task run?" | 13 Q6 / 5 Intuition |
| "What is the convoy effect?" | 13 Q7 / 12 Disadvantages |
| "Why disable preemption in the kernel?" | 13 Q8 / 9 Internal Working |
| "How does the timer preempt in Linux?" | 13 Q9 / 9 Internal Working |
| "Why is my SCHED_FIFO task preempted?" | 13 Q11 / 12 Disadvantages |
| "Preempted vs blocked?" | 13 Q12 / 8 Example |
