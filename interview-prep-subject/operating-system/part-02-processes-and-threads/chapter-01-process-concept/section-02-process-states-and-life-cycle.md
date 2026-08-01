# Process States and Life Cycle

> **TL;DR**: A process is never "just running" — it travels through a life cycle of states (new, ready, running, waiting, terminated, plus suspended variants), and the OS's job is to move it correctly between states while allocating the CPU and memory; the state diagram is the map of all those transitions.

## 1. Why Does This Exist?
A process can't be executing all the time: only one process per CPU core actually runs, others wait for the CPU, for I/O, for memory, or for termination. The OS needs a *formal model* of these conditions so it can: (1) schedule correctly (only READY processes can be chosen), (2) block processes waiting on I/O without wasting CPU, (3) support suspension when memory is tight, and (4) manage exit/reaping. The state model exists to make resource management *a graph of transitions* rather than ad-hoc bookkeeping — it's the OS's decision map.

## 2. How Does It Work?
The classic **5-state model**:
- **new**: being created (PCB allocated, not yet admitted).
- **ready**: in the ready queue, waiting for CPU.
- **running**: actually executing on a CPU core.
- **waiting/blocked**: waiting for an event (I/O, lock, signal).
- **terminated**: finished; PCB retained until reaped (zombie).

Transitions (with triggers):
- new→ready: **admitted** by the long-term scheduler.
- ready→running: **dispatched** by the short-term scheduler.
- running→ready: **preempted** (timer interrupt) or yields.
- running→waiting: **blocks** on I/O or a lock.
- waiting→ready: **event completes** (I/O done, lock granted).
- running→terminated: **exit**.
The **7-state model** adds **suspended/ready (swapped out)** and **suspended/blocked** when memory pressure moves processes to disk (swap) — used by virtual-memory managers.

## 3. When Is It Used?
- **Scheduler decision**: the short-term scheduler always picks from the ready queue; never from waiting.
- **I/O wait**: a process calling `read()` from a socket moves to waiting; the completion (interrupt → softirq → wakeup) moves it back to ready.
- **Memory pressure**: swapping moves ready/blocked processes to suspended states (Linux kswapd).
- **Debugging**: `ps` state letters (R, S, D, T, Z) are live states; `top` shows them.
- **Process supervision**: systemd watches states (running, failed) — a coarse process-state model.

## 4. Why Wasn't Another Approach Chosen?
- **Two states only (running / not)**: too coarse — can't distinguish "waiting for CPU" from "waiting for I/O", so the scheduler couldn't avoid waking idle processes; rejected.
- **States inferred from code (no explicit state)**: fragile and untestable; explicit states make transitions auditable and bugs visible.
- **No swap/suspend states**: on machines with more processes than RAM, we'd have to kill or fail rather than suspend to disk; 7-state model adds suspend for graceful memory overcommit.
- **One queue for everything (ready + blocked together)**: scheduler would scan blocked processes pointlessly; separate queues per state (ready queue, wait queues per event) make wakeup and dispatch O(1)-ish.
The chosen approach — explicit states + per-state queues — is the standard in Linux (runnable queue + wait queues keyed by event) and every RTOS.

## 5. Intuition
Think of a **cafeteria line**: customers arrive (new), stand in the line (ready), get served at the counter (running), wait for their food to cook (waiting/blocked), then their food arrives and they rejoin the line (waiting→ready), eat, and leave (terminated). The manager (OS) only puts *line-standers* (ready) at the counter, never people still waiting for their order — that would waste the counter. If the café is overcrowded, some customers wait outside (suspended).

## 6. Real-World Analogy
An **airport gate**: passengers check in (new), sit in the boarding lounge (ready), board when called (running), wait for their bags after landing (blocked), rejoin the flow, and depart the terminal (terminated). If the terminal is overcrowded, flights are held on the tarmac (suspend). The gate agent (scheduler) only boards passengers who are in the lounge and "ready" — never ones still waiting on their baggage carousel.

## 7. Formal Definition
The **process state** is the current condition of a process as tracked by the OS, from a standard set: **new**, **ready** (admitted, awaiting CPU), **running** (executing), **waiting/blocked** (awaiting an event), **terminated** (exited, awaiting reap); the **suspended** variants add "moved out of main memory." Transitions between states are triggered by admission, dispatch, preemption, blocking, event completion, exit, and swap-in/swap-out. On Linux, states in `task_struct.state` include `TASK_RUNNING` (R), `TASK_INTERRUPTIBLE` (S), `TASK_UNINTERRUPTIBLE` (D), `TASK_STOPPED` (T), `TASK_TRACED` (t), `EXIT_ZOMBIE` (Z), `EXIT_DEAD` (X).

## 8. Example
A process does: `read()` on a slow disk then a busy computation.
```
state history (from start):
  new            -> ready -> running -> waiting (read syscall)
  I/O completes  -> ready (wakeup by softirq)
                -> running (scheduler dispatch) -> running (compute)
  program ends   -> terminated (zombie) -> reaped by parent wait()
```
Now with `ps`:
```
$ sleep 30 & ps -o pid,stat,comm -p $!
  4567 S    sleep         # S = sleeping (TASK_INTERRUPTIBLE)
$ kill -STOP $!; ps -o pid,stat,comm -p $!
  4567 T    sleep         # T = stopped (SIGSTOP)
```
The state column directly reflects the model.

## 9. Internal Working
1. **new**: `fork()`/`clone()` allocates `task_struct` (slab cache), sets `state = TASK_RUNNING` (Linux conflates new+ready; "new" exists in theory), enqueues to runqueue. The **long-term scheduler** (admission) roughly corresponds to cgroup/CPU limits in modern Linux (not a distinct scheduler).
2. **ready**: on the runqueue (EEVDF rbtree). State `TASK_RUNNING` even when not running.
3. **running**: `schedule()` picks it; `context_switch()` runs it; accounting via `vruntime`.
4. **waiting**: syscall blocks → task dequeued from runqueue, `state = TASK_INTERRUPTIBLE` (or `TASK_UNINTERRUPTIBLE` for fs/wait-for-disk), enqueued on the event's **wait queue** (`wait_event`/`add_wait_queue`).
5. **Event completion**: interrupt/softirq calls `wake_up()` → task moved from wait queue to runqueue, `state = TASK_RUNNING` (runnable).
6. **terminated**: `do_exit()` sets `EXIT_ZOMBIE`, signals parent (`SIGCHLD`); memory/files freed; PCB remains until `wait()` → `EXIT_DEAD` → `task_struct` released.
7. **suspend**: `kswapd`/memory pressure swaps out pages (`TASK_UNINTERRUPTIBLE` during swap I/O or full swap); resume via swap-in.

## 10. Time Complexity
- Enqueue/dequeue ready: O(log n) (rbtree) / O(1) amortized (EEVDF cached).
- Wakeup from wait queue: O(1) per task woken.
- Dispatch (ready→running): O(1) + context-switch cost.
- Block (running→waiting): O(1) + scheduling.
- Zombie reaping: O(1) per child.
- Swap in/out: O(pages swapped) — I/O bound.

## 11. Advantages
- **Correct scheduling**: only READY tasks are ever dispatched — no wasted wakeups.
- **Efficient I/O**: blocked tasks use zero CPU; completion wakes exactly the right task via wait queues.
- **Memory flexibility**: suspension lets systems overcommit and survive RAM pressure.
- **Debuggability**: `ps`/`top`/`/proc` states make problems (zombie piles, D-state) visible.
- **Foundation for RTOS**: deterministic state transitions enable worst-case analysis.

## 12. Disadvantages
- **Overhead**: state transitions + queue ops add per-event cost.
- **D-state blind spot**: uninterruptible sleep can't be killed — the state hides a stuck driver/fs.
- **Zombie accumulation**: unreaped terminated processes leak PCB slots and PIDs.
- **Suspend costs**: swapping causes latency spikes; overcommit can trigger the OOM killer.
- **Model simplifications**: Linux conflates states (new=ready); tracing "life cycle" is more subtle than the 5-state picture.

## 13. Interview Questions
1. **Q: List the process states.** A: New, ready, running, waiting/blocked, terminated — plus suspended variants (7-state model). On Linux: R, S, D, T, Z.
2. **Q: What transitions are possible?** A: new→ready (admit), ready→running (dispatch), running→ready (preempt/yield), running→waiting (block), waiting→ready (event), running→terminated (exit); swap: ready↔suspend-ready, waiting↔suspend-waiting.
3. **Q (TRICKY): Can a process go from waiting directly to running?** A: No — it must first become *ready* (event completion enqueues it on the runqueue); only the scheduler dispatches it to running. Missing this is a classic slip.
4. **Q: What is the difference between ready and running?** A: Ready = in the runqueue, eligible for CPU; running = actually executing on a core. Only one (per core) can be running; many can be ready.
5. **Q: What is a zombie process?** A: A terminated process whose parent hasn't `wait()`ed — the PCB (and PID) is retained; it's not running, uses no CPU/memory beyond the PCB, but must be reaped. Fix: fix the parent or `init` will adopt+reap.
6. **Q (PRODUCTION): You see 500 zombie processes. What does it mean?** A: Some parent isn't calling `wait()` (bug) or a process is stuck. Zombies themselves are harmless (tiny PCB) but signal a lifecycle bug; check `ppid` — if the parent died, systemd reaps them.
7. **Q: What is an orphan process?** A: A process whose parent died before it; on Unix it's adopted by PID 1 (systemd), which reaps it — so orphans don't become permanent zombies.
8. **Q: What is a stopped vs a sleeping process?** A: Stopped (T) = suspended by a signal (`SIGSTOP`/`SIGTSTP`), resumed by `SIGCONT`; sleeping (S/D) = waiting on an event (I/O, lock). Stop is parent/signal-driven; sleep is event-driven.
9. **Q (TRICKY): What does `TASK_UNINTERRUPTIBLE` (D) mean and why is it dangerous?** A: The task waits on I/O that can't be interrupted (NFS, disk, some drivers); it ignores signals, so `kill -9` won't work — it can hang the shutdown. Linux fixed many (e.g., NFS "inode barrier") cases with `TASK_KILLABLE`.
10. **Q: What is the role of the long-term scheduler (admission)?** A: Historically it decided how many jobs enter the ready pool (batch); in modern Linux it's effectively cgroup/CPU limits and the number of runnable tasks; the short-term scheduler (dispatcher) makes per-tick choices.
11. **Q: What is the medium-term scheduler?** A: Swap in/out — moves suspended processes between memory and disk under memory pressure. In Linux, kswapd + direct reclaim approximate it.
12. **Q (SCENARIO): A process is perpetually in R but barely progresses. Why?** A: Possibly a CPU hog holding a lock while runnable, or it's runnable but starved by higher-priority tasks; check with `perf`/`top`. R-state with high CPU time can also be a busy-wait bug.
13. **Q: How does Linux represent states in the kernel?** A: `task_struct.state` bitmask: `TASK_RUNNING`, `TASK_INTERRUPTIBLE`, `TASK_UNINTERRUPTIBLE`, `TASK_STOPPED`, `TASK_TRACED`, `EXIT_ZOMBIE`, `EXIT_DEAD`; `ps` maps them to R/S/D/T/t/Z/X.
14. **Q: Why does a process wake but not run immediately?** A: Wakeup moves it to ready (runqueue); the scheduler may dispatch it later (priority, load balance, CPU affinity) — event completion ≠ dispatch.
15. **Q (PRODUCTION): What is `wait_event_interruptible` vs `wait_event` in drivers?** A: The former allows signal interruption (task wakes with EINTR on signal); the latter makes the task uninterruptible. Choosing the wrong one causes unrecoverable waits — directly the D-state problem above.

## 14. Follow-Up Questions
1. **Q: What's the difference between a wait queue and the ready queue?** A: Wait queues are per-event lists of blocked tasks; the ready queue (runqueue) holds runnable tasks. Event completion moves tasks between them.
2. **Q: What is `TASK_KILLABLE`?** A: A compromise: interruptible by *fatal* signals only — recoverable waits without unbounded D-states (used by NFS).
3. **Q: What triggers a transition from running to ready?** A: Timer tick (preemption), yielding (`sched_yield`), or a higher-priority task becoming ready (with preemption enabled).
4. **Q: Can a running task block without giving up the CPU in a cooperative OS?** A: In a *non-preemptive/cooperative* system, only explicit yield/blocking transitions occur; preemption requires a timer interrupt. RTOSes differ by design.
5. **Q: How does `top` derive %CPU from states?** A: It samples `/proc/<pid>/stat` (utime+stime deltas) — R/S don't directly give %CPU; accounting is per jiffy.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();
    if (pid == 0) {
        /* child: block on stdin read (goes to sleeping state) */
        char c;
        read(0, &c, 1);
        _exit(0);
    }
    /* parent: watch the child's state */
    char path[64], buf[128];
    snprintf(path, sizeof path, "/proc/%d/status", pid);
    for (int i = 0; i < 5; i++) {
        FILE *f = fopen(path, "r");
        while (fgets(buf, sizeof buf, f))
            if (strncmp(buf, "State:", 6) == 0) printf("iteration %d: %s", i, buf);
        fclose(f);
        sleep(1);
    }
    kill(pid, SIGKILL);   /* or write to its stdin */
    wait(NULL);
    return 0;
}
```
```bash
# Watch states live
watch -n0.5 'ps -eo pid,stat,comm,args | grep -E "sleep|ls"'
# Create a zombie on purpose
bash -c 'sleep 1 & exec sleep 10'
ps -eo pid,ppid,stat,comm | grep sleep   # the 1s-sleep shows as Z
```

## 16. Industry Usage
- **Linux**: `kernel/sched/core.c` (`schedule`, runqueue), `kernel/wait.c` (wait queues), `kernel/exit.c` (`do_exit`), `kernel/signal.c`. Every production host's process states are read by `ps`/`top`/`sar`/`perf`.
- **Windows NT**: state machine in `KPROCESS` (running, ready, standby, waiting, transition, terminated) — a richer variant of the same model.
- **FreeRTOS**: `eRunning`, `eReady`, `eBlocked`, `eSuspended`, `eDeleted` — the same states on a small scale.
- **Production ops**: SREs triage "D-state pileups" (bad mounts), "zombie floods" (buggy parent), and "R-state CPU burn" — all vocabulary from this model.
- **RTOS/certification**: state transition tables are part of safety analysis (QNX, seL4).

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.1-3.2 (Process Concept, Process Scheduling/States).
- Tanenbaum, *Modern OS*, Ch. 2.1 (Processes).
- Linux man: `ps(1)`, `proc(5)` (State field).
- Linux source: `include/linux/sched.h` (task state), `kernel/sched/core.c`, `kernel/exit.c`, `kernel/wait.c`, `include/linux/wait.h`.
- FreeRTOS docs — task states.

## 18. Cheat Sheet
- 5 states: new, ready, running, waiting, terminated (+ suspended).
- Transitions: admit, dispatch, preempt/yield, block, event-complete, exit, swap.
- waiting → ready → running (never waiting → running directly).
- Linux states: R, S, D, T/t, Z, X.
- D = uninterruptible I/O sleep; not killable; TASK_KILLABLE fixes some.
- Zombie = terminated, unreaped (PCB kept); orphan = parent died (adopted by init).
- Runqueue = ready tasks; wait queues = per-event blocked tasks.
- Medium-term scheduler = swap; long-term = admission (≈ cgroup limits now).
- Event completion wakes (→ready); scheduler dispatches (→running).

## 19. Quiz
1. Only which state can the scheduler dispatch? a) waiting b) ready c) new d) terminated → **b**
2. running→waiting happens on: a) timer tick b) block on I/O c) fork d) exit → **b**
3. A task in D-state: a) runs b) ignores signals, waits on I/O c) is reaped d) is stopped → **b**
4. A zombie is: a) running b) terminated & unreaped c) stopped d) orphaned → **b**
5. Orphans get adopted by: a) parent b) PID 1 (init/systemd) c) kernel thread d) nobody → **b**
6. T (stopped) is caused by: a) I/O b) SIGSTOP c) OOM d) exec → **b**
7. Which transition is impossible? a) ready→running b) waiting→ready c) waiting→running d) running→ready → **c**
8. `TASK_UNINTERRUPTIBLE` vs `TASK_INTERRUPTIBLE` differ in: a) CPU usage b) signal response c) memory d) priority → **b**
9. The medium-term scheduler: a) picks CPU b) swaps processes c) forks d) reaps → **b**
10. `ps` shows R for: a) running b) runnable/ready c) restarted d) rejected → **b**

## 20. Flashcards
- **Q: 5 process states?** → **A:** New, ready, running, waiting, terminated.
- **Q: Can waiting → running happen?** → **A:** No — always through ready.
- **Q: Zombie?** → **A:** Terminated, PCB kept until parent wait().
- **Q: Orphan?** → **A:** Parent died; adopted by PID 1.
- **Q: D-state?** → **A:** Uninterruptible kernel I/O wait, unkillable.
- **Q: What does the scheduler dispatch?** → **A:** Only ready tasks.
- **Q: Wait queue vs runqueue?** → **A:** Blocked (per-event) vs runnable tasks.
- **Q: Linux state letters?** → **A:** R, S, D, T/t, Z, X.

## 21. Revision
Processes move through new→ready→running→waiting→terminated (plus suspend), each transition with a specific trigger: admit, dispatch, preempt, block, event-complete, exit. The scheduler only dispatches READY tasks; event completion only moves tasks waiting→ready. Linux encodes states in `task_struct.state` (R/S/D/T/Z/X). Zombies are unreaped terminated processes; orphans are adopted by PID 1. D-state is unkillable kernel I/O wait. Suspended states exist for swapping. This diagram answers most "what happens when a process waits / wakes / exits" questions.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "List process states & transitions" | 7 Formal Definition / 2 How It Works |
| "Can waiting → running directly?" | 13 Q3 / 5 Intuition |
| "What is a zombie/orphan?" | 13 Q5-7 / 8 Example |
| "What is D-state?" | 13 Q9 / 12 Disadvantages |
| "Stopped vs sleeping?" | 13 Q8 / 2 How It Works |
| "Long/short/medium-term schedulers?" | 13 Q10-11 / 14 Follow-Up |
| "500 zombies in production?" | 13 Q6 / 16 Industry Usage |
| "How are states represented in Linux?" | 13 Q13 / 9 Internal Working |
| "Why does wake ≠ run immediately?" | 13 Q14 / 10 Time Complexity |
| "wait_event_interruptible vs wait_event?" | 13 Q15 / 14 Follow-Up Q1 |
