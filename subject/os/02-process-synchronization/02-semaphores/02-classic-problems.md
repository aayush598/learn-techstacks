# Classic Synchronization Problems

## Bounded Buffer (Producer-Consumer)
```c
sem_t mutex = 1;  // mutual exclusion for buffer
sem_t empty = N;  // count of empty slots
sem_t full = 0;   // count of full slots

// Producer:
do {
    produce(item);
    wait(&empty);
    wait(&mutex);
    buffer[in] = item;  in = (in + 1) % N;
    signal(&mutex);
    signal(&full);
} while (TRUE);

// Consumer:
do {
    wait(&full);
    wait(&mutex);
    item = buffer[out];  out = (out + 1) % N;
    signal(&mutex);
    signal(&empty);
    consume(item);
} while (TRUE);
```
- **Order matters**: always wait on counting semaphore *before* mutex (prevents deadlock)

## Readers-Writers Problem

### 1st Variation (Reader Priority)
```c
sem_t rw_mutex = 1;  // writers' lock
sem_t mutex = 1;     // protect read_count
int read_count = 0;

// Writer:
wait(&rw_mutex);  // write;  signal(&rw_mutex);

// Reader:
wait(&mutex);  read_count++;
if (read_count == 1) wait(&rw_mutex);
signal(&mutex);  // read  wait(&mutex);  read_count--;
if (read_count == 0) signal(&rw_mutex);
signal(&mutex);
```
- **Writer starvation**: readers can keep arriving and block writers indefinitely

### 2nd Variation (Writer Priority)
- Use additional semaphore to queue readers when a writer is waiting
- No starvation for writers, but readers may starve

## Dining Philosophers

### Problem
- 5 philosophers, 5 chopsticks, need 2 to eat
- Deadlock-prone: each picks left, waits for right → circular wait

### Deadlock-Free Solutions
```c
// Option 1: Pick up both or none (mutex around pickup)
sem_t chopstick[5] = {1};
sem_t mutex = 1;

void pickup(int i) {
    wait(&mutex);
    wait(&chopstick[i]);
    wait(&chopstick[(i+1)%5]);
    signal(&mutex);
}

// Option 2: Odd/Even pattern
// Odd philosophers: pick left then right
// Even philosophers: pick right then left
// Breaks circular wait
```

## Sleeping Barber
- **Barber**: waits on barber chair semaphore; if queue empty, sleeps
- **Customer**: if chairs full, leaves; else waits on queue semaphore, wakes barber
- Uses 3 semaphores: `customers`, `barbers`, `mutex`
