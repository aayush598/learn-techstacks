# Hardware Synchronization

## TestAndSet (TAS) — Atomic Instruction
```c
// Atomically: read old value, set to TRUE, return old
boolean TestAndSet(boolean *lock) {
    boolean old = *lock;
    *lock = TRUE;
    return old;
}

// Mutual exclusion using TAS
do {
    while (TestAndSet(&lock));  // acquire — spin
    // critical section
    lock = FALSE;               // release
    // remainder section
} while (TRUE);
```
- **Problem**: violates bounded waiting, may starve

## TAS with Bounded Waiting
```c
// Each process has a waiting[i] flag
waiting[i] = TRUE;
key = TRUE;
while (waiting[i] && key)
    key = TestAndSet(&lock);
waiting[i] = FALSE;
// critical section
// select next process j waiting to enter
j = (i + 1) % n;
while (j != i && !waiting[j]) j = (j + 1) % n;
if (j == i) lock = FALSE;
else waiting[j] = FALSE;
```

## Swap Instruction
```c
// Atomically swap values
void Swap(boolean *a, boolean *b) {
    boolean temp = *a;
    *a = *b;
    *b = temp;
}

do {
    key = TRUE;
    while (key == TRUE) Swap(&lock, &key);
    // critical section
    lock = FALSE;
} while (TRUE);
```

## Memory Barrier / Fence
- Prevents CPU/compiler from **reordering** instructions across the barrier
- `asm volatile("mfence" ::: "memory")` on x86
- `__sync_synchronize()` (GCC built-in)

## Compare-and-Swap (CAS)
```c
// Atomically: if *ptr == expected, set *ptr = new and return true
bool CAS(int *ptr, int expected, int new) {
    if (*ptr != expected) return false;
    *ptr = new;
    return true;
}
// Lock-free counter:
do {
    old = *counter;
} while (!CAS(counter, old, old + 1));
```
- **ABA problem**: pointer changes from A→B→A, CAS succeeds incorrectly
- Fix: **double-wide CAS** (DCAS) or tagged pointers

## Atomic Variables
- Java: `AtomicInteger`, `AtomicReference`
- C11: `atomic_int`, `atomic_compare_exchange_strong`
- C++: `std::atomic<T>`
