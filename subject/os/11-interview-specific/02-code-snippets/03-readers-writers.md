# Readers-Writers Problem

## Problem
- Shared resource (database, file): **readers** only read, **writers** read+write
- Multiple readers can read simultaneously (safe)
- Writers need **exclusive access** (no readers, no other writer)

## Reader-Priority Solution

```c
#include <pthread.h>
#include <semaphore.h>

sem_t rw_mutex = 1;  // controls access to resource (binary)
sem_t mutex = 1;     // protects read_count
int read_count = 0;

void *reader(void *arg) {
    while (1) {
        sem_wait(&mutex);
        read_count++;
        if (read_count == 1)
            sem_wait(&rw_mutex);   // first reader locks writers out
        sem_post(&mutex);

        // Critical section: multiple readers can be here simultaneously
        read_resource();

        sem_wait(&mutex);
        read_count--;
        if (read_count == 0)
            sem_post(&rw_mutex);   // last reader unlocks writers
        sem_post(&mutex);
    }
}

void *writer(void *arg) {
    while (1) {
        sem_wait(&rw_mutex);       // wait for exclusive access
        write_resource();          // Critical section: only one writer
        sem_post(&rw_mutex);
    }
}
```

## Writer-Priority Solution

```c
sem_t rw_mutex = 1, read_mutex = 1, write_mutex = 1, queue = 1;
int read_count = 0, write_count = 0;

void *reader(void *arg) {
    sem_wait(&queue);            // queue for fairness (writers first)
    sem_wait(&read_mutex);
    read_count++;
    if (read_count == 1) sem_wait(&rw_mutex);
    sem_post(&read_mutex);
    sem_post(&queue);            // let next in queue proceed
    read_resource();
    sem_wait(&read_mutex);
    read_count--;
    if (read_count == 0) sem_post(&rw_mutex);
    sem_post(&read_mutex);
}

void *writer(void *arg) {
    sem_wait(&write_mutex);
    write_count++;
    if (write_count == 1) sem_wait(&queue);  // writers block new readers
    sem_post(&write_mutex);

    sem_wait(&rw_mutex);
    write_resource();
    sem_post(&rw_mutex);

    sem_wait(&write_mutex);
    write_count--;
    if (write_count == 0) sem_post(&queue);  // allow readers again
    sem_post(&write_mutex);
}
```

## Variants

| Variant | Behavior | Problem |
|---------|----------|---------|
| **Reader-Priority** | Readers never wait for writers | **Writer starvation** |
| **Writer-Priority** | Writers jump ahead of readers | **Reader starvation** |
| **Fair (queue)** | FIFO ordering (both wait equally) | Slightly less concurrent |

## Use Cases
- **Databases:** read-heavy workloads → reader-priority good
- **File systems:** writers important → writer-priority or fair
- **Linux kernel:** `RCU` (lock-free readers) is used for read-mostly paths

## Interview Tip
- *"Reader-priority can starve writers; writer-priority can starve readers"*
- *"Most practical systems use fair queue or RCU instead"*
- *"First reader locks the resource; last reader unlocks"*
