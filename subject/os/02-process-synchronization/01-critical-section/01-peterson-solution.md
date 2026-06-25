# Peterson's Solution

## Race Condition
- Multiple processes access shared data concurrently; **final value depends on execution order**
- Example: `counter++` compiled to `LOAD R1, counter; INC R1; STORE counter` — interleaved increments lose updates

## Critical Section Problem
```
do {
    entry section      // request permission
    critical section   // access shared resource
    exit section       // release resource
    remainder section  // non-critical work
} while (TRUE);
```

### 3 Requirements
| Requirement | Meaning |
|-------------|---------|
| **Mutual Exclusion** | Only one process in CS at a time |
| **Progress** | If no process in CS, only processes outside RS can decide who enters next |
| **Bounded Waiting** | Bound on number of times others can enter after a process requests entry |

## Peterson's Algorithm (2 Processes)
```c
int turn;              // whose turn to enter
bool flag[2] = {FALSE, FALSE};  // ready to enter

// Process Pi
do {
    flag[i] = TRUE;
    turn = j;          // defer to other process
    while (flag[j] && turn == j);  // wait
    // critical section
    flag[i] = FALSE;
    // remainder section
} while (TRUE);
```

## Correctness Proof
- **Mutual Exclusion**: P₀ enters CS only when `flag[1] == FALSE` or `turn == 0`. Both cannot be true simultaneously.
- **Progress**: If P₁ not ready, `flag[1]` is FALSE → P₀ enters immediately. If both ready, `turn` decides — one enters.
- **Bounded Waiting**: P₀ waits at most one CS entry by P₁ (P₁ sets `turn = 0` before entering).

## Limitations
- Only works for **2 processes**
- **Assumes sequential memory consistency** — on modern CPUs with reordering, may need memory barriers (`atomic_thread_fence`)
- Modern equivalent: `std::atomic` with `memory_order_seq_cst`
