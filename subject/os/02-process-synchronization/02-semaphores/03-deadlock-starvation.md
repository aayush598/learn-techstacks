# Deadlock & Starvation with Semaphores

## Deadlock with Semaphores
**Example**: Two processes, two semaphores `S = 1`, `Q = 1`
```
P0: wait(S); wait(Q); ... signal(Q); signal(S);
P1: wait(Q); wait(S); ... signal(S); signal(Q);
```
- If P0 executes `wait(S)` and P1 executes `wait(Q)` simultaneously → each waits for the other → **deadlock**

## Starvation (Indefinite Blocking)
- A process waits indefinitely to enter its critical section
- **vs Deadlock**: in starvation, other processes *do* make progress; the starved process is simply never scheduled
- Example: Reader-Writers with reader priority → writer starves

| | Deadlock | Starvation |
|---|---|---|
| Progress | No process progresses | Other processes progress |
| Resolution | Requires external intervention | OS scheduling policy can help |
| Resource state | All held resources blocked | Resources actively used by others |

## Priority Inversion
- **Problem**: Low-priority task holds lock → medium-priority tasks preempt it → high-priority task blocks on the lock → high priority indirectly waits for medium
- **Mars Pathfinder (1997)**: Periodic "information bus" task (high) blocked by low-priority weather task → system reset
- **Root cause**: low-priority task preempted by medium-priority tasks while holding a lock needed by high-priority

## Priority Inheritance Protocol
- When high-priority task blocks on a lock held by low-priority task: low-priority **inherits** the high priority temporarily
- Low-priority executes at inherited priority, cannot be preempted by medium
- After releasing lock, priority returns to original
- Supported by: **pthreads** (`PTHREAD_PRIO_INHERIT`), **RTOS** (VxWorks, FreeRTOS)
