# Section 03: Synchronization in Java and Go

> **TL;DR**: Java centers on shared memory: `synchronized`/monitors, explicit locks, `volatile`, atomics, and the `java.util.concurrent` collection zoo. Go centers on message passing: goroutines + channels, plus mutexes/atomics for the cases that need them. Both encode the Part 04 primitives in language ergonomics — know the mapping.

## 1. Why Does This Exist?
C/pthread primitives are powerful but error-prone (missed unlocks, wrong ordering). Java and Go exist with *structured, safer* concurrency: Java bakes monitors into the language (`synchronized`, `wait/notify`) and provides a battle-tested concurrency library; Go makes concurrency a first-class language feature (goroutines + channels) so shared-memory locking is often unnecessary. Understanding both models — and their primitives' mapping to OS constructs — is essential for real-world systems work.

## 2. How Does It Work?
**Java**:
- `synchronized` method/block = monitor (implicit lock + reentrancy; Part 04 Ch 2 Sec 4).
- `Object.wait()/notify()/notifyAll()` = condition variables (must hold the monitor; while-loop re-check).
- `java.util.concurrent`: `ReentrantLock` (fairness, tryLock), `ReentrantReadWriteLock`, `StampedLock` (seqlock-like), `Semaphore`, `CountDownLatch`, `CyclicBarrier`, `ConcurrentHashMap`, `ArrayBlockingQueue`, `AtomicLong` (CAS), `LongAdder` (striped counters).
- `volatile` = visibility without locking (no atomicity for compound ops).
- Executors/thread pools built on work queues.

**Go**:
- **Goroutines**: lightweight threads (M:N, managed by the Go runtime; stack grows dynamically, ~2KB initial).
- **Channels**: typed communication (`chan T`, buffered/unbuffered) — the CSP model; send/receive synchronize.
- `select` on multiple channels; `sync.Mutex`, `sync.RWMutex`, `sync.WaitGroup`, `sync.Once`, `sync.Atomic`.
- "Do not communicate by sharing memory; instead, share memory by communicating."

## 3. When Is It Used?
- **Java**: enterprise/concurrency-heavy servers; concurrent collections; explicit lock control; fine-grained contention tuning.
- **Go**: network services, microservices, systems tooling — idiomatic pipelines via channels and goroutine-per-request.
- Both: data races are caught by race detectors (Go -race; Java has tools/TSAN analog).

## 4. Why Wasn't Another Approach Chosen?
- **Pure pthreads everywhere**: verbose and bug-prone. Rejected in favor of language structures.
- **Java-only monitors**: explicit lock needs (tryLock, fairness, interruption) pushed `java.util.concurrent` into existence — a library over monitors/atomics.
- **Go channels-only**: some problems need direct state (caches, counters) — mutexes/atomics remain, but channels dominate by design choice (CSP over shared state).
- **Actor model (Erlang/Akka)**: possible but heavier; Go's channels are lighter-weight.
Both chose *pragmatic dual models*: structured locks when needed, plus higher-level concurrency where it fits.

## 5. Intuition
**Java** is like a **shared whiteboard with a designated marker-holder**: everyone syncs by owning the marker (monitor) or using the whiteboard's structured tools (concurrent collections). **Go** is like **workers passing handoffs**: goroutines hand work to each other through pipes (channels) rather than grabbing shared state — you rarely touch the same board, you pass the baton.

## 6. Real-World Analogy
**A kitchen brigade**: Java = one chef holds the pan (lock) and writes to the shared ticket board under a "one chef at the board" rule (monitor), with a shared station toolset (concurrent collections). Go = each station passes dishes through a serving window (channel); a station never reaches into another's prep — it sends the plate (message) and moves on (goroutine per dish).

## 7. Formal Definition
- **Java monitor**: `synchronized` on a method/block acquires the object's monitor; reentrant; `wait` releases + sleeps; `notify/notifyAll` wake; must be inside synchronized; predicate re-check in while-loop (Mesa).
- **Java volatile**: guarantees visibility/ordering (happens-before) but not atomicity for RMW — use atomics for counters.
- **Java atomics**: `AtomicReference/AtomicLong` = CAS; `LongAdder` = striped counters for extreme read/write.
- **Go goroutine**: a function running concurrently on an M:N scheduler; stack grows; cheap to spawn (thousands).
- **Go channel**: `ch <- v` (send, blocks until received if unbuffered/full), `v := <-ch` (receive, blocks if empty); unbuffered = rendezvous; buffered = bounded queue.
- **Go select**: choose among ready channel ops — like a multi-way wait.

## 8. Example
**Java**: 
```java
synchronized void inc() { count++; }              // monitor
AtomicLong a = new AtomicLong(0); a.incrementAndGet(); // CAS
ConcurrentHashMap<String,Long> map = new ConcurrentHashMap<>();
```
**Go**:
```go
func worker(id int, jobs <-chan int, wg *sync.WaitGroup) {
    for j := range jobs { fmt.Println(id, j) }   // receive until closed
    wg.Done()
}
jobs := make(chan int, 10)                        // bounded buffer
for i := 0; i < 3; i++ { go worker(i, jobs, &wg) }
for i := 0; i < 10; i++ { jobs <- i }             // sends
close(jobs); wg.Wait()
```
The Go version coordinates via the channel; the Java version would use a BlockingQueue + thread pool.

## 9. Internal Working
**Java**:
- synchronized → monitorenter/monitorexit bytecodes; biased → lightweight (CAS) → heavyweight (futex monitor) lock escalation.
- ReentrantLock → AbstractQueuedSynchronizer (AQS): CLH-style wait queue + CAS state.
- Atomics → `Unsafe.compareAndSwapInt` / VarHandle (CAS).
- ConcurrentHashMap → striped locks + CAS + volatile.

**Go**:
- Goroutine scheduler (GMP): M (OS threads) × P (processors) × G (goroutines); work stealing; runtime parks goroutines on futex/mutex internally when blocked.
- Channels → internal hchan: ring buffer + wait queues (sendq/recvq); unbuffered = direct handoff; runtime uses futex/mutex to park.
- sync.Mutex → futex-based (like glibc) with spin briefly then park.
- Go race detector (TSAN-based) instruments loads/stores.

## 10. Time Complexity
- Java synchronized uncontended: ~O(1) CAS (ns). Heavily contended: futex (~µs) via heavyweight monitor.
- Go channel op: O(1) — with atomic fast path; blocking = park (futex).
- Go goroutine creation: ~O(1), ~100s of ns — far cheaper than OS threads.
- ConcurrentHashMap ops: O(1) amortized (striped).
- select: O(n channels).

## 11. Advantages
- **Java**: mature, expressive concurrency library; explicit control (fairness, timeouts, interruption); race detection; huge ecosystem.
- **Go**: cheap goroutines (scale to 100k+), idiomatic channels (clear ownership), race detector built in, no deep lock hierarchies in idiomatic code.

## 12. Disadvantages
- **Java**: verbose; synchronized granularity coarse; monitor misuse (notify vs notifyAll, missed predicate checks) still possible; heavyweight monitor on contention.
- **Go**: channels can mask deadlocks (silent blocking); mutex misuse still possible; no built-in monitors (CVs via channels only); channel allocation overhead vs plain locks for counters.

## 13. Interview Questions
1. **Q: How does Java do mutual exclusion?** A: `synchronized` (monitor — implicit lock), `ReentrantLock`/`ReentrantReadWriteLock` (explicit), atomics for counters; all built on the primitives from Part 04.
2. **Q: What does `synchronized` guarantee?** A: Mutual exclusion + happens-before (visibility): code inside the block is ordered and visible after lock release.
3. **Q: What's `volatile` vs `synchronized`?** A: `volatile` gives visibility/ordering only (no atomicity for RMW); `synchronized` gives full ME. Use volatile for flags, atomics for counters, monitors for compound state.
4. **Q (TRICKY): When is `volatile` enough?** A: For a single read/write flag (e.g., `running = false`) where no compound operation is needed — visibility without locking.
5. **Q: What are goroutines?** A: Lightweight concurrency in Go (M:N — many goroutines multiplexed on few OS threads); cheap stack, ~100ns spawn.
6. **Q: How do channels relate to bounded buffers?** A: `make(chan T, N)` is a bounded buffer; unbuffered (N=0) is a rendezvous — sends block until a receive is ready, exactly the producer-consumer pattern.
7. **Q: What's `select`?** A: Waits on multiple channel operations — the Go way to multiplex concurrent communication (like a multi-channel `poll`).
8. **Q (PRODUCTION): Why might a Go program deadlock with channels?** A: A blocking send/receive with no matching partner on the other side (and no select/default) parks forever; the runtime detects some and panics, but silent waits hide logic bugs.
9. **Q: How does Go implement sync.Mutex?** A: Spin briefly (bounded, ~4ns spins) then park via the runtime's futex-based machinery — same fast-path/sleep structure as glibc.
10. **Q: What is the race detector?** A: A runtime instrumentation (TSAN-like) that reports data races on shared memory access — `go test -race`; Java has similar tooling.
11. **Q: Java: how does ConcurrentHashMap achieve concurrency?** A: Striped locks (bins) + CAS + volatile reads — reads are mostly lock-free; writes lock only their bin.
12. **Q (TRICKY): Channel vs mutex in Go — when each?** A: Channels for ownership transfer/coordination (data flows between goroutines); mutex for protecting shared mutable state (counters, caches). Idiom: "share memory by communicating" — but measure; a mutex for a counter is fine.

## 14. Follow-Up Questions
1. **Q: What is AQS in Java?** A: AbstractQueuedSynchronizer — the CLH-based queue + CAS state machine under ReentrantLock/Semaphore/CountDownLatch.
2. **Q: What's the difference between Java's `Object.wait` and `Condition.await`?** A: `Condition` from ReentrantLock allows multiple distinct conditions per lock (vs one per object) and interruption/fairness.
3. **Q: What's LongAdder and why?** A: A striped counter that reduces contention (cells per thread) with O(1) snapshot — better than AtomicLong under heavy write contention.
4. **Q: How does Go's GMP scheduler scale?** A: M OS threads, P logical processors (GOMAXPROCS), G goroutines with a run queue; work stealing balances load — thousands of goroutines per P.
5. **Q: How do you translate a producer-consumer in Java vs Go?** A: Java: BlockingQueue + thread pool; Go: buffered channel + goroutines — semantically identical, different ergonomics.

## 15. Coding Example
```java
// Java: monitor + explicit lock + atomic
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

class Counter {
    private final ReentrantLock lock = new ReentrantLock(true); // fair
    private long value;
    void inc() { lock.lock(); try { value++; } finally { lock.unlock(); } }
    long get() { lock.lock(); try { return value; } finally { lock.unlock(); } }
}
AtomicLong atomic = new AtomicLong();
atomic.incrementAndGet();
```
```go
// Go: goroutines + channel (bounded producer-consumer)
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	jobs := make(chan int, 3)   // bounded buffer, capacity 3
	for i := 0; i < 2; i++ {
		wg.Add(1)
		go func(id int) {       // goroutine (consumer)
			defer wg.Done()
			for j := range jobs {
				fmt.Printf("worker %d got %d\n", id, j)
			}
		}(i)
	}
	for j := 0; j < 5; j++ { jobs <- j }  // producer (sends)
	close(jobs)
	wg.Wait()
}
```

## 16. Industry Usage
- **Java**: Apache/Spring services, Kafka, Hadoop, Elasticsearch — heavy concurrent-collection usage.
- **Go**: Docker, Kubernetes, Terraform, Prometheus — goroutine-per-request, channels for pipelines.
- Both dominate cloud infrastructure; race detection and structured concurrency are table stakes.

## 17. References
- Java Language Spec: synchronized, volatile, wait/notify; Javadoc `java.util.concurrent`.
- Go spec: goroutines, channels, select; `sync` package docs.
- *Effective Java* (Bloch), *The Go Programming Language* (Donovan & Kernighan).
- Herlihy & Shavit (for the underlying primitives).
- Go scheduler papers: "Analysis of the Go runtime scheduler."

## 18. Cheat Sheet
- Java: synchronized = monitor; wait/notify = CVs; volatile = visibility; atomics = CAS; concurrent collections = striped locks.
- Go: goroutine = lightweight M:N thread; channel = typed pipe (bounded/unbuffered); select = multi-channel wait; sync.Mutex/RWMutex/WaitGroup/Once/Atomic.
- Unbuffered channel = rendezvous (both block).
- Buffered channel N = bounded buffer (backpressure).
- Race detectors: go test -race; Java tooling.
- Synchronized → biased→lightweight→heavyweight escalation.
- Go GMP: M × P × G with work stealing.
- Idiom Go: channels for ownership transfer; mutex for shared state.

## 19. Quiz
1. synchronized = a) semaphore b) monitor c) channel d) spin → **b**
2. volatile gives: a) atomicity b) visibility c) exclusion d) counting → **b**
3. Go unbuffered channel = a) queue b) rendezvous c) pool d) lock → **b**
4. Goroutines are: a) OS threads b) lightweight M:N c) processes d) fibers-only → **b**
5. select waits on: a) mutex b) channels c) files d) CPU → **b**
6. ConcurrentHashMap uses: a) one lock b) striped locks+volatile c) semaphores d) spin → **b**
7. LongAdder reduces: a) memory b) contention c) threads d) latency → **b**
8. Java wait must be in: a) static b) synchronized c) try d) loop → **b**
9. Go sync.Mutex implementation: a) spin forever b) spin-then-park c) only spin d) only sleep → **b**
10. Idiomatic Go for ownership transfer: a) mutex b) channel c) atomic d) volatile → **b**

## 20. Flashcards
- **Q: Java synchronized?** → **A:** Monitor (implicit lock).
- **Q: volatile?** → **A:** Visibility only, no atomicity.
- **Q: Goroutine?** → **A:** Lightweight M:N thread.
- **Q: Unbuffered channel?** → **A:** Rendezvous.
- **Q: Buffered channel?** → **A:** Bounded buffer.
- **Q: select?** → **A:** Multi-channel wait.
- **Q: Race detector?** → **A:** TSAN-based instrumentation.
- **Q: Go idiom?** → **A:** Channels for transfer; mutex for state.

## 21. Revision
Java and Go encode Part 04's primitives with different philosophies. Java: monitors (synchronized + wait/notify), explicit locks (ReentrantLock with fairness/tryLock), volatile for visibility, CAS-based atomics, and striped concurrent collections — shared-memory first. Go: goroutines (cheap M:N threads), channels (typed pipes; unbuffered = rendezvous, buffered = bounded buffer), select for multiplexing, and mutexes/atomics for state — message-passing first, with race detectors in both. Knowing the mapping (monitor→synchronized, CV→wait/notify/channel, bounded buffer→BlockingQueue/channel) is the interview win.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Java mutual exclusion?" | 13 Q1 / 2 How Does It Work |
| "What does synchronized guarantee?" | 13 Q2 / 7 Formal Definition |
| "volatile vs synchronized?" | 13 Q3 / 7 Formal Definition |
| "When is volatile enough?" | 13 Q4 / 8 Example |
| "What are goroutines?" | 13 Q5 / 7 Formal Definition |
| "Channels as bounded buffers?" | 13 Q6 / 6 Real-World Analogy |
| "What's select?" | 13 Q7 / 2 How Does It Work |
| "Go channel deadlock?" | 13 Q8 / 12 Disadvantages |
| "How does Go mutex work?" | 13 Q9 / 9 Internal Working |
| "Channel vs mutex in Go?" | 13 Q12 / 4 Why Wasn't Another Approach Chosen |
