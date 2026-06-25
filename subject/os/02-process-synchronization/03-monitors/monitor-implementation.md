# Monitors

## Definition
- **High-level concurrency construct** (Hoare, 1974)
- Collection of procedures + shared variables + condition variables
- **Only one thread** can be active in the monitor at any time (automatic mutual exclusion)

## Condition Variables
```c
// Inside a monitor:
condition x, y;

x.wait();   // suspend calling thread, release monitor lock
x.signal(); // wake one waiting thread (if any)
```
- Always called from within the monitor

## Mesa vs Hoare Semantics
| Aspect | Hoare | Mesa |
|--------|-------|------|
| Signal behavior | Signal thread blocks, waiter runs immediately | Signal thread continues, waiter moves to ready queue |
| Condition guarantee | Condition **definitely** true when waiter resumes | Condition **may be false** — must re-check with `while` |
| Usage | Proof-oriented, harder to implement | Practical (Java, pthreads), **most widely used** |

```c
// Mesa-style: always re-check condition
while (count == 0) x.wait();
// consume

// Hoare-style: condition guaranteed (no while needed)
if (count == 0) x.wait();
// consume
```

## Monitor Implementation with Semaphores
```c
sem_t mutex = 1;     // monitor entry
sem_t next = 0;      // for signaler to sleep
int next_count = 0;

// Each condition variable:
sem_t x_sem = 0;
int x_count = 0;

x.wait():
    x_count++;
    if (next_count > 0) signal(&next);
    else signal(&mutex);
    wait(&x_sem);
    x_count--;

x.signal():
    if (x_count > 0) {
        next_count++;
        signal(&x_sem);
        wait(&next);
        next_count--;
    }
```

## In Practice
- **Java `synchronized`**: every object has a monitor; `wait()`, `notify()`, `notifyAll()` (Mesa semantics)
- **Java `ReentrantLock`**: `Condition` objects with `await()`, `signal()`
- **pthreads**: `pthread_mutex_t` + `pthread_cond_t`
