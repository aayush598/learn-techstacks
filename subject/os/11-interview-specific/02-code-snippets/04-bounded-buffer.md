# Bounded Buffer (Monitor / Condition Variables)

## Monitor with Condition Variables (Hoare-style)

```c
#include <pthread.h>

#define N 10
int buf[N];
int in = 0, out = 0, count = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;
pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;

void put(int x) {
    pthread_mutex_lock(&mutex);
    while (count == N)                        // while, not if (spurious wakeup)
        pthread_cond_wait(&not_full, &mutex); // releases mutex, reacquires on wake
    buf[in] = x;
    in = (in + 1) % N;
    count++;
    pthread_cond_signal(&not_empty);          // wake a consumer
    pthread_mutex_unlock(&mutex);
}

int get() {
    pthread_mutex_lock(&mutex);
    while (count == 0)
        pthread_cond_wait(&not_empty, &mutex);
    int x = buf[out];
    out = (out + 1) % N;
    count--;
    pthread_cond_signal(&not_full);           // wake a producer
    pthread_mutex_unlock(&mutex);
    return x;
}
```

## Monitor vs Semaphore

| Aspect | Monitor | Semaphore |
|--------|---------|-----------|
| **Structure** | Object with methods + condition variables | Integer + P/V operations |
| **Scope** | Internal (structured concurrency) | Global (can be used anywhere) |
| **Mutex** | Built-in (only one thread in monitor) | Separate mutex needed |
| **State** | Encapsulated | Exposed counter |
| **Error-prone** | Less (structured, less scattered P/V) | More (easy to forget P or V) |
| **Condition** | `wait()` + `signal()` (condition-based) | P/V on resource count |

## Spurious Wakeup
- `pthread_cond_wait()` can return even if condition not signaled (POSIX allows it)
- **Always use `while` loop** (not `if`) to re-check condition
- Java's `wait()` also has spurious wakeups

## Signal Semantics
| Model | Signal behavior |
|-------|----------------|
| **Mesa** (POSIX, Java) | Signaled thread placed on ready queue; may not run immediately |
| **Hoare** (theoretical) | Signaler immediately yields to signaled thread (atomic handoff) |

- POSIX is **Mesa-style**: must re-check condition (while loop)
- Hoare: if condition changes, the thread gets scheduled later

## Key Points
- `while` loop for condition: handles spurious wakeup + Mesa semantics
- `pthread_cond_signal` wakes **one** thread; `pthread_cond_broadcast` wakes **all**
- Should pair `wait(not_full)` with `signal(not_full)` and vice versa
- **Monitor = mutex + condition variables** (structured approach)

## Interview Tip
- *"Monitors are structured concurrency — mutex + condition variables in one package"*
- *"Always use while, not if, for condition checks after wait() — spurious wakeup"*
- *"Mesa semantics: signaled thread doesn't run immediately — must recheck condition"*
