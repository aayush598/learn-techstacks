# Lock-Free & Wait-Free Data Structures

## Progress Guarantees

| Level | Definition | Example |
|-------|-----------|---------|
| **Obstruction-Free** | Thread makes progress only if no contention | Single CAS loop |
| **Lock-Free** | At least **one** thread makes progress system-wide | Treiber stack, MS queue |
| **Wait-Free** | **Every** thread makes progress in finite steps | RCU readers, LLSC objects |
| **Wait-Free Bounded** | Each operation completes in O(1) known steps | Restricted to simple ops |

## CAS-Based Structures

### Treiber Stack (Lock-Free Stack)
- **Push:** CAS on top pointer (retry on ABA)
- **Pop:** CAS top → top.next (retry if changed)
- **Problem:** ABA issue when top is modified A→B→A

### Michael-Scott (MS) Queue
- Lock-free FIFO queue with head/tail pointers
- **Enqueue:** CAS tail.next then CAS tail
- **Dequeue:** CAS head → head.next (remove sentinel node)
- Widely used in **Java** `ConcurrentLinkedQueue`

## ABA Problem
- Thread reads `top = A` (A's next = X)
- Thread 2 pops A, pushes new A (address reused!)
- Thread 1's CAS succeeds incorrectly (A == A, but structure changed)
- **Solutions:**
  - **Tagged pointer:** store counter with pointer (double-wide CAS)
  - **Hazard pointers:** track in-use pointers to prevent reuse
  - **RCU:** defer reclamation until no readers

## RCU (Read-Copy-Update) — Linux Kernel
- **Readers:** no locks, no memory barriers (extremely fast)
- **Writers:** copy data → update atomic pointer → wait for grace period → free old
- **Grace period:** all pre-existing readers finish
- Used in Linux (routing tables, VFS dentries)
- **Read overhead:** essentially 0 (just pointer dereference)

## Hazard Pointers
- Each thread stores pointers it's accessing in a thread-local list
- Writer checks hazard list before freeing
- Lock-free reclamation without GC
- Used in C++ `boost.lockfree`

## Memory Reclamation Summary
| Technique | Overhead | Scalability | Complexity |
|-----------|----------|-------------|------------|
| **Epoch-Based (EBR)** | Low | Good | Medium |
| **Hazard Pointers** | Medium | Fair | High |
| **RCU** | Very low (reads) | Excellent | Low (kernel) |

## Interview Tip
- *"Lock-free guarantees system-wide progress — at least one thread moves forward"*
- Know ABA + tagged pointers cold
- RCU is Linux's secret weapon for read-mostly workloads
