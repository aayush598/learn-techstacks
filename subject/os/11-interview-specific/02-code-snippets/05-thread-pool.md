# Thread Pool

## Concept
- Pre-create a pool of threads; reuse them for many tasks
- Avoids thread creation/destruction overhead (expensive syscalls)
- Limits resource usage (max threads prevents thrashing)

## Conceptual Implementation

```c
#include <pthread.h>
#include <semaphore.h>

typedef struct {
    void (*function)(void *);
    void *arg;
} task_t;

typedef struct {
    task_t *queue;       // task queue (circular buffer)
    int head, tail, size, count;
    pthread_t *workers;  // worker thread handles
    int num_workers;
    sem_t tasks;         // count of pending tasks
    pthread_mutex_t lock;
    int shutdown;
} thread_pool_t;

void *worker(void *arg) {
    thread_pool_t *pool = (thread_pool_t *)arg;
    while (1) {
        sem_wait(&pool->tasks);             // block until task available
        pthread_mutex_lock(&pool->lock);
        if (pool->shutdown) break;          // time to die
        task_t task = pool->queue[pool->head];
        pool->head = (pool->head + 1) % pool->size;
        pool->count--;
        pthread_mutex_unlock(&pool->lock);
        task.function(task.arg);            // execute
    }
    pthread_mutex_unlock(&pool->lock);
    return NULL;
}

void pool_submit(thread_pool_t *pool, void (*func)(void *), void *arg) {
    pthread_mutex_lock(&pool->lock);
    // queue full? wait / resize / block
    pool->queue[pool->tail].function = func;
    pool->queue[pool->tail].arg = arg;
    pool->tail = (pool->tail + 1) % pool->size;
    pool->count++;
    pthread_mutex_unlock(&pool->lock);
    sem_post(&pool->tasks);                 // wake a worker
}
```

## Thread Pool Configurations

| Aspect | Fixed Pool | Dynamic Pool | Work-Stealing |
|--------|-----------|-------------|---------------|
| **Threads** | Fixed N (e.g., 4) | Grows/shrinks as needed (min, max, keepalive) | Each thread has own deque |
| **Queue** | Single shared queue | Shared + possibly per-thread | Per-thread deques |
| **Stealing** | No | No | Idle threads steal from others |
| **Best for** | Predictable load | Variable load | Recursive divide-and-conquer (ForkJoin) |

## Language Examples
- **Java:** `ExecutorService` (`newFixedThreadPool`, `newCachedThreadPool`, `newWorkStealingPool`)
- **Python:** `concurrent.futures.ThreadPoolExecutor` (uses `os.cpu_count()` default)
- **C++:** `std::async` (implementation-defined, often thread pool)
- **Go:** goroutines are **not** a thread pool — M:N scheduling (goroutine ≠ thread)

## Performance Benefits
- Thread creation: ~10–50μs → pool avoids this per-task (saves 10–50μs per task)
- Memory: threads have ~1MB stack → 1000 threads = 1GB; pool limits threads
- Context switch: fewer threads → less thrashing

## ForkJoinPool (Java 7+)
- **Work-stealing:** idle threads steal from busy threads' deque
- **Divide-and-conquer:** `ForkJoinTask` forks subtasks, joins results
- `RecursiveAction` (void) / `RecursiveTask` (return value)
- **Parallel stream** uses ForkJoinPool.commonPool()

## Optimal Pool Size
- **CPU-bound:** `N_threads = N_cores` (or N_cores + 1 for I/O waits)
- **I/O-bound:** `N_threads = N_cores * (1 + wait_time / compute_time)`
  - E.g., 80% I/O wait → N_threads = N_cores × 5

## Interview Tips
- *"Thread pools reuse threads — avoids creation cost and limits resource usage"*
- *"CPU-bound: N_threads ≈ N_cores; I/O-bound: more threads (hide I/O latency)"*
- *"Java's ForkJoinPool uses work-stealing for divide-and-conquer parallelism"*
