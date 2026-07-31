# Operating Systems Concepts for Infosys SP DSE Interview

## Table of Contents
1. [Process vs Thread](#process-vs-thread)
2. [Process States](#process-states)
3. [CPU Scheduling Algorithms](#cpu-scheduling-algorithms)
4. [Deadlock](#deadlock)
5. [Synchronization](#synchronization)
6. [Memory Management](#memory-management)
7. [Virtual Memory](#virtual-memory)
8. [Page Replacement Algorithms](#page-replacement-algorithms)
9. [Common Interview Questions](#common-interview-questions)

---

## Process vs Thread

| Feature | Process | Thread |
|---------|---------|--------|
| Definition | Program in execution | Lightweight process |
| Memory | Separate address space | Shared address space |
| Creation | Heavyweight (slow) | Lightweight (fast) |
| Communication | IPC (pipes, sockets, shared memory) | Direct (shared variables) |
| Context Switch | Expensive | Cheaper |
| Crash Impact | Isolated (other processes safe) | Can crash entire process |
| Examples | Chrome browser, VS Code | Tabs in Chrome, threads in VS Code |

```
Process with multiple threads:
┌─────────────────────────────────┐
│         Process (Chrome)        │
│  ┌─────────┐  ┌─────────┐     │
│  │ Thread 1 │  │ Thread 2 │     │
│  │ (Tab 1)  │  │ (Tab 2)  │     │
│  └─────────┘  └─────────┘     │
│       │              │         │
│       ▼              ▼         │
│  ┌─────────────────────┐      │
│  │   Shared Memory      │      │
│  │ - Code section       │      │
│  │ - Data section       │      │
│  │ - Open files         │      │
│  └─────────────────────┘      │
└─────────────────────────────────┘
```

---

## Process States

```
            ┌──────────┐
            │  New     │
            └────┬─────┘
                 │ admit
                 ▼
            ┌──────────┐
      ┌─────│ Ready    │◄────┐
      │     └────┬─────┘     │
      │          │ schedule  │
      │          ▼           │
      │     ┌──────────┐    │
      │     │ Running  │    │
      │     └────┬─────┘    │
      │          │          │
      │     ┌────┴────┐    │
      │     ▼         ▼    │
┌─────┴────┐   ┌──────────┐│
│Waiting/  │   │ Terminated││
│Blocked   │   └──────────┘│
└────┬─────┘               │
     │ I/O complete        │
     └─────────────────────┘
```

| State | Description |
|-------|-------------|
| **New** | Process is being created |
| **Ready** | Waiting to be assigned to CPU |
| **Running** | Instructions being executed |
| **Waiting/Blocked** | Waiting for I/O or event |
| **Terminated** | Finished execution |

---

## CPU Scheduling Algorithms

### 1. FCFS (First Come First Serve)
Non-preemptive. Simplest algorithm.

```
Processes: P1(24), P2(3), P3(3)
Arrival order: P1, P2, P3

Gantt Chart:
|---P1---|--P2--|--P3--|
0       24     27     30

Waiting time:
P1: 0
P2: 24
P3: 27

Average Waiting Time = (0 + 24 + 27) / 3 = 17
```

### 2. SJF (Shortest Job First)
Non-preemptive. Optimal for average waiting time.

```
Processes: P1(6), P2(8), P3(7), P4(3)
Arrival time: 0 for all

Gantt Chart (sorted by burst time):
|---P4--|---P1---|----P3----|------P2------|
0      3        9          16             24

Waiting time:
P4: 0
P1: 3
P3: 9
P2: 16

Average Waiting Time = (0 + 3 + 9 + 16) / 4 = 7
```

### 3. SRTF (Shortest Remaining Time First)
Preemptive version of SJF.

```
Processes:
P1: Arrival=0, Burst=8
P2: Arrival=1, Burst=4
P3: Arrival=2, Burst=9
P4: Arrival=3, Burst=5

Gantt Chart:
|---P1---|--P2--|---P4---|----P1----|--------P3--------|
0       1      5        9         13                  22

At time 1: P2 arrives (4 < 7 remaining), preempt P1
At time 5: P2 done, P4 arrives (5 < 4 remaining of P1)
At time 9: P4 done, P1 resumes
```

### 4. Round Robin
Preemptive with time quantum.

```
Processes: P1(10), P2(4), P3(7), P4(3)
Time Quantum = 3

Gantt Chart:
|P1|P2|P3|P4|P1|P2|P3|P4|P1|P3|
0  3  6  9 12 15 18 21 24 27 30

Wait times:
P1: (0) + (15-3) + (27-18) = 0 + 12 + 9 = 21
P2: (1) + (18-6) = 1 + 12 = 13
P3: (2) + (12-9) + (24-21) = 2 + 3 + 3 = 8
P4: (3) + (15-12) = 3 + 3 = 6

Average = (21 + 13 + 8 + 6) / 4 = 12
```

### 5. Priority Scheduling
Higher priority process executes first.

```
Processes:
P1: Burst=10, Priority=3
P2: Burst=1, Priority=1 (highest)
P3: Burst=2, Priority=4
P4: Burst=1, Priority=5 (lowest)
P5: Burst=5, Priority=2

Gantt Chart (lower number = higher priority):
|--P2--|---P5---|----P1----|---P3--|--P4--|
0      1        6          16      18     19

Wait times:
P2: 0
P5: 1
P1: 6
P3: 16
P4: 18

Average = (0 + 1 + 6 + 16 + 18) / 5 = 8.2
```

### Comparison Table

| Algorithm | Preemptive | Starvation | Optimal Avg Wait | Use Case |
|-----------|-----------|------------|------------------|----------|
| FCFS | No | No | No | Batch systems |
| SJF | No | Yes | Yes (for non-preemptive) | Short jobs |
| SRTF | Yes | Yes | Yes (for preemptive) | Mixed workloads |
| Round Robin | Yes | No | No | Time-sharing |
| Priority | Either | Yes | No | Real-time systems |

---

## Deadlock

### Four Conditions (all must hold)

```
1. Mutual Exclusion: Resource can't be shared
2. Hold and Wait: Process holds resource, waits for another
3. No Preemption: Resources can't be forcibly taken
4. Circular Wait: Chain of processes waiting for each other

Example:
P1 holds R1, waits for R2
P2 holds R2, waits for R1
→ Circular wait → Deadlock
```

### Deadlock Prevention
Break one of the four conditions.

```python
# Prevention: Resource ordering (break circular wait)
# Assign numbers to resources, processes must request in order

def process_1():
    lock(resource_1)  # Lower number first
    lock(resource_2)
    # ... work ...
    unlock(resource_2)
    unlock(resource_1)

def process_2():
    lock(resource_1)  # Same order
    lock(resource_2)
    # ... work ...
    unlock(resource_2)
    lock(resource_1)
```

### Deadlock Avoidance
Banker's algorithm (see below).

### Deadlock Detection
Allow deadlocks, detect them, and recover.

```python
# Detection: Wait-for graph
# If cycle exists → deadlock

# Recovery methods:
# 1. Terminate one process
# 2. Preempt resources
```

---

## Banker's Algorithm

```python
def bankers_algorithm(available, maximum, allocation):
    """
    Available: Available resources of each type
    Maximum: Maximum demand of each process
    Allocation: Resources currently allocated

    Returns: Safe sequence or None if unsafe
    """
    n = len(maximum)          # Number of processes
    m = len(available)        # Number of resource types

    # Calculate Need matrix
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    work = available[:]
    finish = [False] * n
    safe_sequence = []

    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i]:
                # Check if process can be satisfied
                if all(need[i][j] <= work[j] for j in range(m)):
                    # Process can finish, release its resources
                    for j in range(m):
                        work[j] += allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            return None  # Deadlock state

    return safe_sequence


# Example
available = [3, 3, 2]  # Available resources

maximum = [
    [7, 5, 3],  # P0 max need
    [3, 2, 2],  # P1 max need
    [9, 0, 2],  # P2 max need
    [2, 2, 2],  # P3 max need
    [4, 3, 3],  # P4 max need
]

allocation = [
    [0, 1, 0],  # P0 currently has
    [2, 0, 0],  # P1 currently has
    [3, 0, 2],  # P2 currently has
    [2, 1, 1],  # P3 currently has
    [0, 0, 2],  # P4 currently has
]

result = bankers_algorithm(available, maximum, allocation)
if result:
    print(f"Safe sequence: {result}")
    # Output: Safe sequence: [1, 3, 4, 0, 2]
else:
    print("Unsafe state - potential deadlock")
```

### Step-by-step Execution

```
Initial: Work = [3, 3, 2], Finish = [F, F, F, F, F]

Step 1: P1 can run (Need [1,2,2] ≤ Work [3,3,2])
  Work = [3+2, 3+0, 2+0] = [5, 3, 2]
  Finish = [F, T, F, F, F]

Step 2: P3 can run (Need [0,1,1] ≤ Work [5,3,2])
  Work = [5+2, 3+1, 2+1] = [7, 4, 3]
  Finish = [F, T, F, T, F]

Step 3: P4 can run (Need [4,3,3] ≤ Work [7,4,3])
  Work = [7+0, 4+0, 3+2] = [7, 4, 5]
  Finish = [F, T, F, T, T]

Step 4: P0 can run (Need [7,4,3] ≤ Work [7,4,5])
  Work = [7+0, 4+1, 5+0] = [7, 5, 5]
  Finish = [T, T, F, T, T]

Step 5: P2 can run (Need [6,0,0] ≤ Work [7,5,5])
  Work = [7+3, 5+0, 5+2] = [10, 5, 7]
  Finish = [T, T, T, T, T]

Safe sequence: P1 → P3 → P4 → P0 → P2
```

---

## Synchronization

### Mutex (Mutual Exclusion)
Binary lock - only one thread can hold it at a time.

```python
import threading

class Mutex:
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

counter = 0
mutex = Mutex()

def increment():
    global counter
    mutex.acquire()
    try:
        counter += 1  # Critical section
    finally:
        mutex.release()

# With context manager (preferred)
def increment_safe():
    global counter
    with mutex.lock:
        counter += 1
```

### Semaphore
Can allow multiple threads (counting semaphore).

```python
import threading
import time

class Semaphore:
    def __init__(self, count):
        self.count = count
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def acquire(self):
        with self.condition:
            while self.count <= 0:
                self.condition.wait()
            self.count -= 1

    def release(self):
        with self.condition:
            self.count += 1
            self.condition.notify()

# Example: Database connection pool
class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = Semaphore(max_connections)
        self.connections = []

    def get_connection(self):
        self.semaphore.acquire()
        # Create or reuse connection
        conn = f"Connection-{len(self.connections)}"
        self.connections.append(conn)
        return conn

    def release_connection(self, conn):
        self.connections.remove(conn)
        self.semaphore.release()

# Allow 3 concurrent connections
pool = ConnectionPool(3)
```

### Monitor
Higher-level synchronization construct.

```python
import threading

class BoundedBuffer:
    """Monitor for producer-consumer problem"""
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.size:
                print("Buffer full, waiting...")
                self.not_full.wait()
            self.buffer.append(item)
            print(f"Produced: {item}")
            self.not_empty.notify()

    def consume(self):
        with self.not_empty:
            while len(self.buffer) == 0:
                print("Buffer empty, waiting...")
                self.not_empty.wait()
            item = self.buffer.pop(0)
            print(f"Consumed: {item}")
            self.not_full.notify()
            return item
```

---

## Memory Management

### Contiguous Allocation
Each process gets a single contiguous block.

```
Memory Layout:
┌─────────────────┐ High Address
│   Kernel        │
├─────────────────┤
│   Free Space    │
├─────────────────┤
│   Process 2     │
├─────────────────┤
│   Free Space    │
├─────────────────┤
│   Process 1     │
├─────────────────┤
│   Free Space    │
└─────────────────┘ Low Address

Problem: External fragmentation
```

### Paging
Divide memory into fixed-size blocks.

```
Logical Address → Physical Address

Page Table:
┌───────┬──────────┐
│ Page  │ Frame    │
├───────┼──────────┤
│   0   │    5     │
│   1   │    2     │
│   2   │    8     │
└───────┴──────────┘

Example: Page size = 4KB
Logical address 8196 = Page 2, offset 4
Physical address = Frame 8 × 4KB + 4 = 32772

Advantages:
- No external fragmentation
- Easy to share pages
- Virtual memory support

Disadvantages:
- Internal fragmentation (last page)
- Page table overhead
```

### Segmentation
Variable-size blocks based on logical divisions.

```
Segment Table:
┌─────────┬──────────┬────────┐
│ Segment │ Base     │ Limit  │
├─────────┼──────────┼────────┤
│ Code    │ 14000    │ 4000   │
│ Data    │ 10000    │ 2500   │
│ Stack   │ 8000     │ 3000   │
└─────────┴──────────┴────────┘

Logical address: (segment_number, offset)
Check: offset < limit, then physical = base + offset

Advantages:
- Logical division (code, data, stack)
- No internal fragmentation
- Better protection

Disadvantages:
- External fragmentation
- Complex memory allocation
```

### Paging vs Segmentation

| Feature | Paging | Segmentation |
|---------|--------|--------------|
| Block size | Fixed | Variable |
| Fragmentation | Internal | External |
| User awareness | Transparent | Visible |
| Logical division | No | Yes |
| Protection | Per page | Per segment |

---

## Virtual Memory

```
Physical Memory + Disk Space = Virtual Memory

Process sees:
┌─────────────────┐
│ Virtual Address  │
│    Space         │
├─────────────────┤
│   Process A     │
├─────────────────┤
│   Process B     │
└─────────────────┘

Actual in RAM:
┌─────────────────┐
│ Part of A       │
├─────────────────┤
│ Part of B       │
└─────────────────┘

Rest on disk (swap space):
┌─────────────────┐
│ Part of A       │
├─────────────────┤
│ Part of B       │
└─────────────────┘
```

### Demand Paging
Pages loaded only when needed.

```
Page Fault → Load page from disk → Resume instruction

Page Fault Handling:
1. Check if address is valid
2. Find free frame (or evict one)
3. Read page from disk to frame
4. Update page table
5. Restart instruction
```

### Thrashing
When system spends more time paging than executing.

```
Symptoms:
- High page fault rate
- Low CPU utilization
- Constant disk I/O

Causes:
- Too many processes
- Too little RAM
- Poor locality of reference

Solutions:
- Increase RAM
- Reduce number of processes
- Improve algorithm locality
- Working Set Model
```

---

## Page Replacement Algorithms

### FIFO (First In First Out)
Replace the oldest page.

```
Reference string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3
Frame size: 3

Step | Page | Frames    | Fault?
-----|------|-----------|-------
  1  |  7   | [7]       | Yes
  2  |  0   | [7,0]     | Yes
  3  |  1   | [7,0,1]   | Yes
  4  |  2   | [2,0,1]   | Yes (replace 7)
  5  |  0   | [2,0,1]   | No
  6  |  3   | [2,3,1]   | Yes (replace 0)
  7  |  0   | [2,3,0]   | Yes (replace 1)
  8  |  4   | [4,3,0]   | Yes (replace 2)
  9  |  2   | [4,2,0]   | Yes (replace 3)
 10  |  3   | [4,2,3]   | Yes (replace 0)

Total faults: 9
Belady's anomaly: More frames can cause more faults!
```

### LRU (Least Recently Used)
Replace the page not used for longest time.

```
Reference string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3
Frame size: 3

Step | Page | Frames    | Fault? | LRU order (oldest→newest)
-----|------|-----------|--------|--------------------------
  1  |  7   | [7]       | Yes    | [7]
  2  |  0   | [7,0]     | Yes    | [7,0]
  3  |  1   | [7,0,1]   | Yes    | [7,0,1]
  4  |  2   | [2,0,1]   | Yes    | [7,0,1] → [0,1,2]
  5  |  0   | [2,0,1]   | No     | [0,1,2]
  6  |  3   | [2,0,3]   | Yes    | [1,2,0] → [2,0,3]
  7  |  0   | [2,0,3]   | No     | [2,0,3]
  8  |  4   | [2,0,4]   | Yes    | [2,0,3] → [0,3,4] → [0,4,2]
  9  |  2   | [2,0,4]   | No     | [0,4,2]
 10  |  3   | [3,0,4]   | Yes    | [4,2,0] → [2,0,3] → [0,3,4]

Total faults: 7
No Belady's anomaly!
```

### Optimal (Belady's Algorithm)
Replace page that won't be used for longest time in future.

```
Reference string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3
Frame size: 3

Step | Page | Frames    | Fault? | Future use
-----|------|-----------|--------|-----------
  1  |  7   | [7]       | Yes    | Never used again
  2  |  0   | [7,0]     | Yes    | Used at 4,6
  3  |  1   | [7,0,1]   | Yes    | Never used again
  4  |  2   | [2,0,1]   | Yes    | 7 used never, 1 never, 2 at 8
  5  |  0   | [2,0,1]   | No     |
  6  |  3   | [2,0,3]   | Yes    | 1 never, 2 at 8, 3 at 9
  7  |  0   | [2,0,3]   | No     |
  8  |  4   | [2,0,4]   | Yes    | 2 at 8 (just used), 0 at 6 (done), 4 never
  9  |  2   | [2,0,4]   | No     |
 10  |  3   | [2,0,3]   | Yes    | 2 never, 0 never, 4 never

Total faults: 6
Optimal but impossible to implement (needs future knowledge)
```

### Algorithm Comparison

| Algorithm | Faults (example) | Belady's | Implementation |
|-----------|-----------------|----------|----------------|
| FIFO | 9 | Yes | Simple queue |
| LRU | 7 | No | Stack/counter |
| Optimal | 6 | No | Impossible (future) |
| Clock (LRU approx) | ~7 | No | Circular + reference bit |

---

## Common Interview Questions

### Q1: What is context switching?
**Answer:** Saving the state of the current process and loading the saved state for the next process. Overhead includes saving registers, updating memory maps, and flushing CPU cache.

### Q2: Difference between process and thread?
**Answer:** Process has its own memory space; thread shares memory with other threads in the same process. Process creation is heavyweight; thread creation is lightweight. Process communication requires IPC; threads communicate via shared memory.

### Q3: What is a race condition?
**Answer:** When multiple threads access shared data concurrently and the result depends on timing. Example: Two threads incrementing `counter++` simultaneously may lose updates.

```python
# Race condition
counter = 0
def unsafe_increment():
    global counter
    counter += 1  # Not atomic: read, increment, write

# Fix with lock
lock = threading.Lock()
def safe_increment():
    global counter
    with lock:
        counter += 1
```

### Q4: What is starvation?
**Answer:** A process waits indefinitely because other processes are always given priority. Example: In priority scheduling, low-priority processes may never execute if high-priority processes keep arriving.

### Q5: What is the difference between internal and external fragmentation?
**Answer:**
- **Internal:** Space inside allocated block is wasted (paging with partial last page)
- **External:** Free memory is broken into small blocks (segmentation)

### Q6: What is a page fault?
**Answer:** When a program accesses a page not currently in physical memory. OS must fetch it from disk (swap space), update page table, and restart the instruction.

### Q7: What is thrashing and how to prevent it?
**Answer:** When page fault rate is very high, causing excessive paging. Caused by too many processes or too little RAM. Prevent by: increasing RAM, reducing processes, using Working Set Model.

### Q8: Explain the dining philosophers problem.
**Answer:** 5 philosophers sit around a table, each needs 2 forks to eat. With 5 forks, deadlock can occur if all pick up left fork simultaneously. Solutions: resource ordering, allow at most 4 philosophers to sit, use a coordinator.

```python
# Solution: Resource ordering
def philosopher(left_fork, right_fork):
    while True:
        think()
        # Always pick up lower-numbered fork first
        first = min(left_fork, right_fork)
        second = max(left_fork, right_fork)
        pick_up(first)
        pick_up(second)
        eat()
        put_down(second)
        put_down(first)
```

### Q9: What is a semaphore? Difference from mutex?
**Answer:**
- **Mutex:** Binary lock (0 or 1), only holder can release
- **Semaphore:** Counter-based, any thread can signal (release)
- **Binary semaphore** ≈ mutex, but semaphore can be signaled by any thread

### Q10: What is virtual memory?
**Answer:** Technique that gives processes illusion of large contiguous memory by using disk as extension of RAM. Uses demand paging to load pages only when needed, enabling multitasking with limited physical memory.

---

## Real-World Analogies for Quick Recall

```
╔══════════════════════════════════════════════════════════════════════╗
║                    OS CONCEPT → REAL WORLD                         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Process = A running program (like a running app on your phone)    ║
║  Thread  = A worker inside that program (a tab in Chrome)          ║
║                                                                    ║
║  CPU Scheduling = A manager deciding who works next                ║
║  FCFS         = Queue at a shop (first come, first served)         ║
║  SJF          = Let the quickest task go first                     ║
║  Round Robin  = Kids taking turns on a swing                       ║
║  Priority     = VIP queue at airport                               ║
║                                                                    ║
║  Deadlock     = Two people in a hallway, both refusing to move     ║
║  Starvation   = A nice person always letting others go first       ║
║                                                                    ║
║  Paging       = Library with numbered shelves (fixed-size slots)   ║
║  Segmentation = Warehouse with variable-size storage rooms         ║
║  Virtual Memory = Using disk as extra RAM (like cloud storage)     ║
║                                                                    ║
║  Mutex        = A bathroom key (only one person at a time)         ║
║  Semaphore    = A parking lot counter (shows remaining spots)      ║
║  Monitor      = A bank teller (handles one customer at a time)     ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Deep Dive: Process Scheduling Visual Walkthrough

### FCFS - Convoy Effect Problem

```
Scenario: Short jobs stuck behind a long job

Processes: P1(100ms), P2(1ms), P3(1ms)

Bad Order:
|--------P1--------|--P2--|--P3--|
0                 100    101    102

Waiting times: P1=0, P2=100, P3=101
Average = (0+100+101)/3 = 67ms  ← TERRIBLE!

If we did SJF first:
|--P2--|--P3--|--------P1--------|
0      1      2                 102

Waiting times: P2=0, P3=1, P1=2
Average = (0+1+2)/3 = 1ms  ← MUCH BETTER!
```

### Round Robin - Time Quantum Effect

```
Time Quantum too large  → Behaves like FCFS
Time Quantum too small  → Too much context switching overhead
Time Quantum just right → Good response time

Example: P1=10, P2=4, P3=7, Quantum=3

Round 1: [P1] [P2] [P3]     → Each gets 3ms
Round 2: [P1] [P2] [P3]     → P2 finishes, others continue
Round 3: [P1] [P3]           → P3 finishes
Round 4: [P1]                → P1 finishes

Timeline:
0  3  6  9  12 15 18 21 24 27 30
|--|--|--|--|--|--|--|--|--|--|
P1 P2 P3 P1 P2 P3 P1 P3    P1
```

---

## Memory Management Deep Dive

### Virtual Address Translation (Step-by-Step)

```
Given: Page size = 4KB (2^12 = 4096 bytes)
Logical address = 8196 (decimal)

Step 1: Convert to binary
8196 = 0010000000000100

Step 2: Split into Page Number + Offset
┌──────────┬────────────┐
│  Page #  │   Offset   │
│ (20 bits)│ (12 bits)  │
├──────────┼────────────┤
│  0010    │ 000000000100│
└──────────┴────────────┘
Page = 2 (binary 0010)
Offset = 4 (binary 100)

Step 3: Look up Page Table
Page 2 → Frame 8

Step 4: Calculate Physical Address
Physical = Frame × PageSize + Offset
Physical = 8 × 4096 + 4
Physical = 32768 + 4 = 32772

┌─────────────────────────────────────────┐
│     VIRTUAL ADDRESS TRANSLATION         │
│                                         │
│  Logical: [Page 2 | Offset 4]          │
│              │                          │
│              ▼ (Page Table Lookup)      │
│  Page Table: [2 → 8]                   │
│              │                          │
│              ▼                          │
│  Physical: [Frame 8 | Offset 4]        │
│            = 32772                      │
└─────────────────────────────────────────┘
```

### Page Table with Multiple Levels

```
Single-level page table (32-bit address, 4KB pages):
- Would need 2^20 entries = 1 million entries!
- Each entry 4 bytes → 4MB just for page table!

Solution: Multi-level page table

Two-level page table (x86):
┌──────────┬──────────┬────────────┐
│ Page Dir │  Page #  │   Offset   │
│ (10 bits)│ (10 bits)│ (12 bits)  │
└──────────┴──────────┴────────────┘

        Page Directory
        ┌─────────┐
        │ Entry 0 │──→ Page Table 0 ──→ Frames 0-1023
        │ Entry 1 │──→ Page Table 1 ──→ Frames 1024-2047
        │ Entry 2 │──→ (not allocated)
        │  ...    │
        │Entry 1023│
        └─────────┘

Only allocates page tables that are actually used!
```

---

## Synchronization Deep Dive

### Producer-Consumer Problem (Visual)

```
┌─────────────────────────────────────────────────────┐
│                  BOUNDED BUFFER                     │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐                │
│  │ 1 │ 2 │ 3 │ 4 │   │   │   │   │  ← Buffer     │
│  └───┴───┴───┴───┴───┴───┴───┴───┘                │
│    ↑                         ↑                      │
│    │                         │                      │
│ Producer                 Consumer                   │
│ (adds items)          (removes items)               │
│                                                     │
│ Rules:                                              │
│ 1. Producer waits if buffer is FULL                 │
│ 2. Consumer waits if buffer is EMPTY                │
│ 3. Only one thread accesses buffer at a time        │
└─────────────────────────────────────────────────────┘

Synchronization needed:
- Mutex: Protect buffer access
- Semaphore (empty): Count of empty slots
- Semaphore (full): Count of full slots

Producer:                    Consumer:
wait(empty)                  wait(full)
lock(buffer)                 lock(buffer)
  add item                     remove item
unlock(buffer)               unlock(buffer)
signal(full)                 signal(empty)
```

### Readers-Writers Problem

```
Database Access Pattern:

Readers (multiple can read simultaneously):
  ┌─────┐  ┌─────┐  ┌─────┐
  │ R1  │  │ R2  │  │ R3  │  ← All can read at same time
  └──┬──┘  └──┬──┘  └──┬──┘
     │        │        │
     ▼        ▼        ▼
  ┌─────────────────────┐
  │     DATABASE        │
  └─────────────────────┘
     ▲        ▲        ▲
     │        │        │
  ┌──┴──┐  ┌──┴──┐
  │ W1  │  │ W2  │  ← Only ONE writer at a time
  └─────┘  └─────┘    AND no readers during write

Rules:
1. Multiple readers can read simultaneously
2. Only one writer at a time
3. No readers while writing
```

---

## Context Switching Deep Dive

```
What happens during a context switch:

Step 1: Timer interrupt occurs (process used its time slice)
Step 2: CPU saves current process state:
  ┌──────────────────────────────────┐
  │ SAVED STATE (PCB - Process Ctrl Block) │
  ├──────────────────────────────────┤
  │ • Program Counter (where to resume)     │
  │ • CPU Registers (all values)            │
  │ • Memory Management info (page tables)  │
  │ • I/O status info                       │
  │ • Scheduling info (priority, etc.)      │
  │ • Accounting info (CPU time used)       │
  └──────────────────────────────────┘
Step 3: OS scheduler picks next process
Step 4: CPU loads new process state
Step 5: New process resumes execution

Cost of Context Switch:
- Direct cost: Save/restore registers (~1-100 μs)
- Indirect cost: Cache pollution, TLB flush
- Too many switches → wasted CPU time
```

---

## Additional Interview Questions

### Q11: Explain the Producer-Consumer problem and its solutions.
**Answer:** One thread produces data, another consumes. Bounded buffer shared between them. Solutions:
1. **Semaphore-based:** Use two semaphores (empty count, full count) + mutex
2. **Monitor-based:** Use condition variables (not_full, not_empty)
3. **Lock-free:** Use ring buffer with atomic operations

```python
# Visual: How semaphores coordinate producer-consumer
#
# Buffer capacity = 5
# Initially: empty=5, full=0, mutex=1
#
# Producer adds item:
#   wait(empty)  → empty becomes 4 (decrement)
#   lock(mutex)  → exclusive access
#   add to buffer
#   unlock(mutex)
#   signal(full) → full becomes 1 (increment)
#
# Consumer removes item:
#   wait(full)   → full becomes 0 (decrement)
#   lock(mutex)  → exclusive access
#   remove from buffer
#   unlock(mutex)
#   signal(empty)→ empty becomes 5 (increment)
```

### Q12: What is a race condition? How do you prevent it?
**Answer:** Race condition occurs when multiple threads access shared data concurrently and the result depends on execution order.

```
Example: Two threads incrementing counter (initially 0)

Thread A:          Thread B:          Counter:
read counter (0)                       0
                   read counter (0)   0
increment to 1                         0
                   increment to 1     0
write counter (1)                      1
                   write counter (1)  1

Expected: 2, Actual: 1 ← DATA RACE!

Prevention: Use synchronization (mutex, semaphore, lock)
```

### Q13: What is the difference between a process and a program?
**Answer:**
- **Program:** Static code stored on disk (like a recipe book)
- **Process:** Program in execution (like cooking from the recipe)
- One program can have multiple processes (open Chrome twice)
- Each process has its own memory space and PID

### Q14: Explain the dining philosophers problem.
**Answer:** Classic synchronization problem illustrating deadlock.

```
        Philosopher 0
           /    \
     Fork0      Fork1
        /          \
Philosopher 4    Philosopher 1
    |                |
  Fork4          Fork2
    \              /
Philosopher 3  Philosopher 2
           \    /
          Fork3

Each philosopher needs 2 forks to eat.
If all pick up left fork simultaneously → DEADLOCK!

Solutions:
1. Allow at most 4 philosophers to sit
2. Always pick up lower-numbered fork first
3. Use a coordinator (waiter) to arbitrate
4. Use chopsticks (resources) with timeout
```

### Q15: What is priority inversion and how to solve it?
**Answer:** High-priority process waits for low-priority process holding a needed resource, while medium-priority processes preempt the low-priority one.

```
Priority Inversion Scenario:
High Priority:    [--------WAITING--------]
Medium Priority:       [---RUNNING---]
Low Priority:     [--RUN--][---PREEMPTED---][RUN--]
                   ↑ has resource      ↑ can't run to release

Solution: Priority Inheritance Protocol
- Temporarily boost low-priority process to high priority
- It releases resource quickly
- Then priority is restored
```

---

## Quick Reference Cheat Sheet

| Topic | Key Points |
|-------|-----------|
| Process | Separate address space, heavyweight |
| Thread | Shared memory, lightweight |
| FCFS | Non-preemptive, simple, convoy effect |
| SJF | Optimal avg wait, may starve long jobs |
| Round Robin | Preemptive, time quantum, fair |
| Deadlock | 4 conditions: mutual exclusion, hold-wait, no preemption, circular wait |
| Banker's Algorithm | Deadlock avoidance, checks safe state |
| Mutex | Binary lock, one holder |
| Semaphore | Counter-based, any can signal |
| Paging | Fixed-size blocks, no external fragmentation |
| Segmentation | Variable-size, logical divisions |
| Virtual Memory | Disk extension of RAM |
| FIFO | Simple, Belady's anomaly |
| LRU | Good performance, no Belady's |
| Optimal | Best possible, impossible to implement |
| Context Switch | Save/restore process state, overhead cost |
| Race Condition | Concurrent access to shared data, use locks |
| Priority Inversion | High waits for low, solved by priority inheritance |

---

## Quick Memory: Page Replacement Comparison

```
Algorithm    │ Concept                  │ Analogy
─────────────┼──────────────────────────┼──────────────────────
FIFO         │ Replace oldest page      │ Delete oldest file
LRU          │ Replace least used       │ Delete forgotten file
Optimal      │ Replace farthest future  │ Perfect but impossible
Clock        │ Approximate LRU          │ Round-robin with check bit

For interview, remember:
- FIFO is simple but has Belady's anomaly
- LRU is practical and good performance
- Optimal is theoretical benchmark
- Clock is what real systems use (approximation of LRU)
```

---

## Key Formulas to Remember

```
1. CPU Utilization = (Busy Time / Total Time) × 100%

2. Throughput = Number of processes completed / Time unit

3. Turnaround Time = Completion Time - Arrival Time

4. Waiting Time = Turnaround Time - Burst Time

5. Response Time = First Response Time - Arrival Time

6. Page Fault Rate = (Page Faults / Total Accesses) × 100%

7. Effective Access Time = (1-p)×memory_access + p×page_fault_time
   where p = page fault rate

8. Number of Frames = (Process Size / Page Size)

9. Page Table Size = Number of Pages × Entry Size

10. Internal Fragmentation = (Page Size / 2) on average
```
