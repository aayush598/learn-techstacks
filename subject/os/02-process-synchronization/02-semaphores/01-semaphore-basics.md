# Semaphore Basics

## Definition
- Integer `S` accessed only via two atomic operations:
  - **`wait(S)`** (P): `while (S <= 0) ; // busy wait; S--;`
  - **`signal(S)`** (V): `S++;`

## Types
| Type | Value Range | Purpose |
|------|-------------|---------|
| **Binary** | 0 or 1 | Mutual exclusion (like mutex) |
| **Counting** | 0..N | Resource management (N instances) |

## Busy-Wait (Spinlock) Implementation
```c
void wait(S) {
    while (S <= 0);  // TestAndSet in real hardware
    S--;
}
void signal(S) {
    S++;
}
```

## Blocking (No Busy-Wait) Implementation
```c
typedef struct {
    int value;
    struct process *list;  // waiting queue
} semaphore;

void wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        add current process to S->list;
        block();  // yield CPU, process goes to sleep
    }
}

void signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        remove process P from S->list;
        wakeup(P);  // move to ready queue
    }
}
```
- **S->value < 0** → magnitude = number of processes blocked

## POSIX Semaphore APIs
```c
#include <semaphore.h>

sem_t sem;
sem_init(&sem, 0, 1);    // pshared=0 (thread), initial=1
sem_wait(&sem);           // P operation
sem_post(&sem);           // V operation
sem_destroy(&sem);
```

## Advantages
- Works for **N processes** (not limited to 2 like Peterson)
- **No busy waiting** in blocking variant
- Can solve arbitrary synchronization patterns
