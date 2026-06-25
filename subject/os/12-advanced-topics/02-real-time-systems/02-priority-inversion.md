# Priority Inversion & Inheritance

## Priority Inversion
**Definition:** High-priority task blocked by a low-priority task holding a lock, while a medium-priority task preempts the low-priority task.

### Classic Scenario (3 Tasks)
1. **L** (low priority) acquires lock `L_mutex`
2. **H** (high priority) preempts L, needs `L_mutex` → **blocks**
3. **M** (medium priority) preempts L (since L has low priority)
4. **Result:** H is blocked by M, even though M has nothing to do with the lock

```
Priority
  High H  : ----BLOCKED-------------------------------
  Med  M  :        -----running----
  Low  L  : --running-[holds lock]--------running---
              ↑T1    ↑T2       ↑T3    ↑T4
```

- **Unbounded duration:** H could wait indefinitely (depends on M's execution)
- This violates RT guarantee — H must meet deadline

## Real Example: Mars Pathfinder (1997)
- VxWorks RTOS, priority inheritance not enabled by default
- High-priority bus manager task blocked by low-priority meteorological task
- Medium-priority communications task preempted low-priority → watchdog reset
- **Fix:** enable priority inheritance → problem solved (reset in software)

## Priority Inheritance Protocol (PIP)
- When **low-priority** task holds a lock needed by **high-priority** task:
  - Low-priority task **inherits** high priority temporarily
  - This prevents medium-priority tasks from preempting
- Once lock released → priority returns to normal

```c
// pip inheritance happens automatically on lock contention
pthread_mutexattr_t attr;
pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
pthread_mutex_init(&mutex, &attr);
```

### Properties
- **No deadlock avoidance** (only solves inversion)
- **Chained blocking:** multiple locks can cascade inheritance
- **Implementation complexity:** priority management on lock/unlock

## Priority Ceiling Protocol (PCP)
- Each resource has a **ceiling priority** (max priority of any task that might lock it)
- Task can only lock if its priority > current ceiling of all locked resources
- **Prevents deadlocks** (no circular wait possible)
- **Avoids chained blocking** (lock only granted if safe)
- More complex than PIP

## Linux: rt_mutex (FUTEX_LOCK_PI)
- Linux implements **priority inheritance** for real-time mutexes
- `pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT)`
- Uses **futex** (fast userspace mutex) with PI extension
- `FUTEX_LOCK_PI` / `FUTEX_UNLOCK_PI` syscalls handle inheritance
- Used by: PREEMPT_RT kernel, real-time threads

## Comparison

| Protocol | Prevents Inversion | Prevents Deadlock | Overhead |
|----------|-------------------|-------------------|----------|
| **None** | ❌ | ❌ | None |
| **PIP** | ✅ (bounded) | ❌ | Low |
| **PCP** | ✅ (bounded) | ✅ | Medium |

## Interview Tips
- *"Priority inversion: high-priority task waits for low-priority to release lock, while medium runs"*
- *"Priority inheritance: low inherits high temporarily (solves unbounded inversion)"*
- *"Mars Pathfinder: classic bug — fixed by enabling PIP"*
- *"Linux rt_mutex implements priority inheritance via FUTEX_LOCK_PI"*
