# Mutex Implementations & Locking Primitives

## Lock Implementations

| Lock Type | Mechanism | Contention Cost | Best For |
|-----------|-----------|-----------------|----------|
| **Spinlock** | Busy-wait (TAS/CAS) | High (wastes CPU) | Very short critical sections |
| **Ticket Lock** | FIFO order via tickets | Medium | Fairness required |
| **MCS Lock** | Queue-based spinlock | Low (local spinning) | NUMA systems |
| **Futex** | Userspace fast path + kernel sleep | Syscall only on contention | General-purpose |
| **Adaptive Mutex** | Spin N iterations then sleep | Low-medium | Hybrid workloads |

## Atomic Operations
- **TAS** (Test-and-Set): `bool TAS(lock)` → atomically set & return old value
- **CAS** (Compare-and-Swap): `bool CAS(addr, expected, new)` → swap if unchanged
- **LL/SC** (Load-Linked / Store-Conditional): used in ARM, PowerPC

## Futex (Fast Userspace Mutex) — Linux
- Userspace atomic flag (fast path: no syscall)
- On contention: `futex(FUTEX_WAIT)` syscall → thread sleeps
- On unlock: `futex(FUTEX_WAKE)` → wake waiters
- **rt_mutex** variant: priority inheritance for RT tasks
- Used by: **glibc** `pthread_mutex`, **NPTL**

## Adaptive Mutex (Solaris, Java)
- Spin a few hundred cycles first
- If lock still held → sleep (syscall)
- Avoids context switch cost for short-held locks
- Java's `synchronized` uses adaptive spinning since Java 6

## Performance Comparison
| Scenario | Spinlock | Mutex | Futex | RWLock |
|----------|----------|-------|-------|--------|
| No contention | 5ns | 25ns | 5ns | 10ns |
| Low contention | 100ns | 1μs | 200ns | 500ns |
| High contention | *terrible* | 5μs | 3μs | 2μs (reads) |

## When to Use
- **Spinlock:** real-time kernel, < 100 cycle crit section
- **Mutex/Futex:** most user-space, critical sections
- **RWLock:** read-heavy workloads (DB, cache lookups)
- **MCS Lock:** NUMA-aware kernel code
- **Ticket Lock:** when fairness matters (avoid starvation)
