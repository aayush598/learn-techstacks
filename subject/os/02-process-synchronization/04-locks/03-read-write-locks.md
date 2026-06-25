# Read-Write Locks

## Concept
- **Multiple readers** can hold the lock simultaneously
- **Writers** require exclusive access (no readers, no other writers)
- Improves concurrency for read-heavy workloads

## Implementation (Mutex + Condition Variables)
```c
pthread_mutex_t rw_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t rw_cond = PTHREAD_COND_INITIALIZER;
int readers = 0;
int writers = 0;
int write_waiting = 0;  // for writer priority

void read_lock() {
    pthread_mutex_lock(&rw_mutex);
    while (writers > 0 || write_waiting > 0)
        pthread_cond_wait(&rw_cond, &rw_mutex);
    readers++;
    pthread_mutex_unlock(&rw_mutex);
}

void read_unlock() {
    pthread_mutex_lock(&rw_mutex);
    readers--;
    if (readers == 0)
        pthread_cond_broadcast(&rw_cond);
    pthread_mutex_unlock(&rw_mutex);
}

void write_lock() {
    pthread_mutex_lock(&rw_mutex);
    write_waiting++;
    while (readers > 0 || writers > 0)
        pthread_cond_wait(&rw_cond, &rw_mutex);
    write_waiting--;
    writers = 1;
    pthread_mutex_unlock(&rw_mutex);
}

void write_unlock() {
    pthread_mutex_lock(&rw_mutex);
    writers = 0;
    pthread_cond_broadcast(&rw_cond);
    pthread_mutex_unlock(&rw_mutex);
}
```

## Reader Priority vs Writer Priority
| Scheme | Readers | Writers |
|--------|---------|---------|
| **Reader-priority** | Can starve writers | Never starve if no new readers |
| **Writer-priority** | May starve | Never starve (queue ahead of new readers) |
| **Fair** (e.g., ticket) | FIFO order | FIFO order |

## In Practice
- Linux: `rwlock_t` (spinlock variant), `pthread_rwlock_t`
- Java: `ReadWriteLock`, `ReentrantReadWriteLock`
- C++: `std::shared_mutex` (C++17), `std::shared_lock` and `std::unique_lock`

## Beyond Locks
- **Lock-free**: No locks at all; uses CAS + retry (e.g., lock-free stack, queue)
- **Wait-free**: Every thread completes in finite steps regardless of others (harder)
- RCU (Read-Copy-Update): lock-free reads, synchronized updates — used in Linux kernel
