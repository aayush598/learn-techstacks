# Producer-Consumer (Bounded Buffer) with Semaphores

## Problem
- **Producer** generates data, **Consumer** processes it
- **Bounded buffer** shared between them (fixed size)
- Must not overfill (producer waits) or consume empty (consumer waits)

## Semaphore Solution (Classic)

```c
#include <pthread.h>
#include <semaphore.h>

#define BUFFER_SIZE 10
int buffer[BUFFER_SIZE];
int in = 0, out = 0;

sem_t empty;  // counts empty slots (initialized to BUFFER_SIZE)
sem_t full;   // counts filled slots (initialized to 0)
sem_t mutex;  // protects buffer indices (initialized to 1)

void *producer(void *arg) {
    int item;
    while (1) {
        item = produce_item();
        sem_wait(&empty);     // wait for empty slot (P)
        sem_wait(&mutex);     // enter critical section
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;
        sem_post(&mutex);     // exit critical section
        sem_post(&full);      // signal filled slot (V)
    }
}

void *consumer(void *arg) {
    int item;
    while (1) {
        sem_wait(&full);      // wait for filled slot
        sem_wait(&mutex);     // enter critical section
        item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        sem_post(&mutex);     // exit critical section
        sem_post(&empty);     // signal empty slot
        consume_item(item);
    }
}
```

## Semaphore as Resource Counter
- **P (proberen / wait):** if value > 0, decrement and continue; else block
- **V (verhogen / signal):** increment value; if blocked threads, wake one

## Key Points
- `empty` = buffer slots available (start = BUFFER_SIZE)
- `full` = items available (start = 0)
- `mutex` = binary semaphore (acts as mutex for buffer indices)
- Order: wait(empty) **before** wait(mutex) — avoid deadlock
- **Problem:** if consumer waits(mutex) first then waits(full), and buffer empty → **deadlock**

## Variants
- **Multiple producers/consumers:** works with same semaphores (general)
- **Condition variable version:** use `pthread_cond_wait` / `pthread_cond_signal`
- **Lock-free ring buffer:** single producer + single consumer (no sync needed)
  - Works when only one each: just update `in` and `out` atomically

## Interview Tips
- *"Semaphores count resources; mutexes protect critical sections"*
- *"Always wait for resource semaphore before mutex"*
- *"For single producer + single consumer, lock-free ring buffer is faster"*
