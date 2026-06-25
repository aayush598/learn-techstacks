# Spinlocks

## Definition
- Thread **busy-waits** (spins) in a tight loop until lock is available
- **Thread does not sleep** — no context switch overhead

## When to Use
| Scenario | Spinlock better | Mutex better |
|----------|----------------|--------------|
| Critical section length | **Very short** (few instructions) | Long (sleep worth overhead) |
| CPU count | **Multi-core** (spinner on different core) | Single-core (spinner wastes CPU) |
| Preemptible kernel | No (bad — spinning task can't yield) | Yes |

## Test-and-Set Spinlock (TSL)
```c
void lock(volatile int *lock) {
    while (__sync_lock_test_and_set(lock, 1));
}
void unlock(volatile int *lock) {
    __sync_lock_release(lock);
}
```
- **Problem**: high contention → cache line bouncing, unfair

## Ticket Spinlock (Fairness)
```c
typedef struct {
    volatile int owner;
    volatile int next;
} ticket_lock;

void lock(ticket_lock *l) {
    int my_ticket = __sync_fetch_and_add(&l->next, 1);
    while (l->owner != my_ticket) ;  // spin
}

void unlock(ticket_lock *l) {
    l->owner++;
}
```
- **FIFO ordering** — solves starvation
- Each thread gets a ticket, waits for its number to be called

## MCS Lock (Scalable)
- List-based queue spinlock
- Each spinner spins on its **local** flag → no cache line contention
- Used in Linux kernel for scalable spinning

## Read-Write Spinlocks
- `pthread_rwlock_t` with read/write variants
- Multiple readers OR single writer
