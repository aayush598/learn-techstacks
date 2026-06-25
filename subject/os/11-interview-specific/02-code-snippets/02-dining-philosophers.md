# Dining Philosophers

## Problem
- 5 philosophers, 5 chopsticks, circular table
- Each philosopher: **think** or **eat** (needs 2 chopsticks)
- Goal: prevent deadlock (all hold left, wait for right)

## Deadlock-Free Solution (Odd/Even — Break Circular Wait)

```c
#include <pthread.h>
#include <semaphore.h>

#define N 5
sem_t chopstick[N];

void *philosopher(void *arg) {
    int i = *(int *)arg;
    while (1) {
        think();
        if (i % 2 == 0) {          // even: pick left then right
            sem_wait(&chopstick[i]);
            sem_wait(&chopstick[(i + 1) % N]);
        } else {                     // odd: pick right then left
            sem_wait(&chopstick[(i + 1) % N]);
            sem_wait(&chopstick[i]);
        }
        eat();
        sem_post(&chopstick[i]);
        sem_post(&chopstick[(i + 1) % N]);
    }
}
```

## Alternative Solutions

### Resource Hierarchy
- Always pick **lower-numbered chopstick first**
- Deadlock-free: circular wait broken (monotonic ordering)
```c
int left = i, right = (i + 1) % N;
if (left > right) { int tmp = left; left = right; right = tmp; }
sem_wait(&chopstick[left]);
sem_wait(&chopstick[right]);
```

### Maximum 4 Philosophers
- Allow at most 4 to sit at table → one always has both chopsticks
- Counting semaphore `room = 4`

### Monitor Solution (And-request)
- Request both or none atomically
```c
void pickup(int i) {
    state[i] = HUNGRY;
    test(i);
    if (state[i] != EATING) self[i].wait();
}
void test(int i) {
    if (state[i]==HUNGRY && state[(i+4)%N]!=EATING && state[(i+1)%N]!=EATING) {
        state[i] = EATING;
        self[i].signal();
    }
}
```

## Key Points
- **Deadlock requires all 4 Coffman conditions** — break any one
- Odd/even: breaks **circular wait** (not all can hold left simultaneously)
- Resource hierarchy: breaks **circular wait** (monotonic ordering)
- Max 4: reduces resources so **hold & wait** can't deadlock

## Interview Tips
- *"Dining philosophers is the classic deadlock example — break circular wait"*
- *"Odd/even and resource hierarchy are the two most common solutions"*
- *"Monitor solution with state array and condition variables is most general"*
