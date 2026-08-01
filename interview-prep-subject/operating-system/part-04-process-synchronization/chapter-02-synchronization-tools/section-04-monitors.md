# Section 04: Monitors

> **TL;DR**: A monitor bundles shared data + its synchronization into one object: all methods are protected by an implicit lock, and condition variables handle waiting. Language-level monitors (Java `synchronized`/`wait`/`notify`, C# `lock`) move mutual exclusion out of the programmer's hands and into the structure of the code.

## 1. Why Does This Exist?
Mutexes/semaphores leave synchronization as *discipline*: a programmer must remember to lock around every access — one missed lock = race. A monitor exists to make mutual exclusion *structural*: the compiler/runtime guarantees that only one thread executes any monitor method at a time. It was invented by Hoare and Brinch Hansen as the language-level answer, and it's the foundation of Java/C# synchronized code, and it makes correctness much easier to reason about.

## 2. How Does It Work?
- A monitor = data + procedures, with an implicit mutex guarding all procedures.
- Only one thread may be inside the monitor at a time (ME is automatic).
- To wait for a state change, the thread uses a **condition variable** inside the monitor: `wait` releases the monitor lock and sleeps; `signal`/`notify` wakes a waiter (re-checking predicate under Mesa semantics).
- Compiler inserts lock/unlock around every public method (Java `synchronized` methods; `synchronized(block)` for finer scope).

## 3. When Is It Used?
- Language-level shared-state protection: Java `synchronized`, C# `lock`, Python `with lock`, C++ `std::lock_guard`.
- Implementing classic problems (bounded buffer, readers-writers, philosophers) with clean, structured code.
- Whenever the "one method call at a time" model fits the object (queues, caches, counters, registries).
- Pattern: monitor objects in OOP design.

## 4. Why Wasn't Another Approach Chosen?
- **Bare mutex discipline**: easy to forget locks — the exact failure monitors prevent. Rejected for language ergonomics (still available for finer control).
- **Semaphores**: no structure — any thread can signal; misuse-prone. Rejected as the default API.
- **Global lock**: too coarse (kills concurrency); monitors scope to the object. 
- **Message passing**: an alternative model (Erlang, Go channels) but awkward for shared-mutable-state OOP.
Monitors chosen because they *bake correctness into the type system*: you can't access the protected data without going through the lock.

## 5. Intuition
**A bank teller with one desk and a queue**: the teller's desk is the monitor — only one customer (thread) can be at the desk at a time (implicit lock). If a customer needs the manager (a condition), they step aside (wait) and someone else uses the desk; when the manager arrives (signal), the waiting customer comes back and *checks again* if the manager is still there (re-check predicate). You never have to remember to "lock the desk" — the structure does it.

## 6. Real-World Analogy
**A public bathroom with a lockable door that auto-locks**: you enter (acquire implicit lock), only one person inside at a time. If you need a towel refilled (condition), you wait outside the door, and the attendant (another thread) brings it and notifies you (signal); you re-enter and check if towels are there (re-check). No sign-up sheet, no "please remember to lock" — the door does it structurally, like a monitor.

## 7. Formal Definition
- **Monitor**: an ADT whose:
  - state is private;
  - operations are mutual-exclusion-protected (implicit lock; at most one thread inside);
  - waiting is done via internal condition variables: `wait(cv)` atomically releases the monitor and sleeps; `signal(cv)` wakes a waiter (Mesa semantics in Java/C#: re-check predicate).
- **Java**: `synchronized` method = monitor; every object has a monitor + one implicit condition (via `wait()`/`notify()`/`notifyAll()`); `synchronized` reentrant.
- **C#**: `lock` statement on an object (Monitor.Enter/Exit), same model.
- **Reentrancy**: the same thread may re-enter (lock count), avoiding self-deadlock.
- **Signal-and-continue** (Mesa) vs **signal-and-wait** (Hoare): Java/C# are Mesa.

## 8. Example
**Bounded buffer as a monitor** (Java):
```java
class BoundedBuffer<E> {
    private final Queue<E> q = new ArrayDeque<>();
    private final int cap;
    synchronized void put(E e) {
        while (q.size() == cap) { try { wait(); } catch (...) {} }
        q.add(e); notifyAll();
    }
    synchronized E take() {
        while (q.isEmpty()) { try { wait(); } catch (...) {} }
        E e = q.remove(); notifyAll(); return e;
    }
}
```
- Methods are implicitly locked (only one put/take at a time).
- `wait()` drops the lock while sleeping.
- `while` re-checks; `notifyAll()` wakes all (safe).
- No explicit mutex anywhere — the structure guarantees exclusion.

## 9. Internal Working
1. Compiler/runtime adds lock on method entry, unlock on exit (Java: monitorenter/monitorexit bytecodes; biased → lightweight → heavyweight lock path).
2. `wait()`: enqueues the thread on the object's wait set and *releases the monitor lock* (atomically), then blocks (parked via futex).
3. `notify()`/`notifyAll()`: moves one/all waiters to the entry set; they re-contend for the lock and resume (re-checking the while predicate).
4. Reentrancy counter: nested synchronized re-entry increments a count; exit decrements.
5. Heavyweight path (Java): monitors map to OS mutex + condition — futex-based.

## 10. Time Complexity
- Uncontended method call: O(1) atomic lock/unlock (fast path).
- wait/notify: O(1) futex ops + scheduling.
- Contention: queueing + handoff O(1) per waiter.
- notifyAll: O(waiters) wakeups.

## 11. Advantages
- **Correctness by construction** — ME is automatic; no missing locks.
- Clean composition with condition variables (no external mutex bookkeeping).
- Reentrant — no self-deadlock on nested calls.
- Readable, high-level, matches OOP structure.
- Portability across languages (same model everywhere).

## 12. Disadvantages
- **Coarse granularity**: one lock per object serializes all methods — may need fine-grained locks inside.
- **Signal-and-continue** subtlety: predicate must be re-checked (while loops).
- Notify vs notifyAll tradeoff (missed wakeup vs thundering herd).
- Waiting threads hold no progress info; no priority/fairness control.
- Hard to express some patterns (multiple locks, try-lock, reader-writer) without dropping to lower primitives.

## 13. Interview Questions
1. **Q: What is a monitor?** A: A language construct bundling data + methods where all methods are protected by an implicit mutex; waiting via internal condition variables. Mutual exclusion is automatic.
2. **Q: How is a monitor different from a mutex?** A: A mutex is a *tool* you apply around code; a monitor is a *structure* where ME is enforced by the type/compiler — you can't forget to lock.
3. **Q: Java synchronized method = ?** A: A monitor method — implicit lock on the object; wait/notify/notifyAll as the condition mechanism.
4. **Q: What happens when wait() is called inside a synchronized method?** A: The thread releases the monitor lock and sleeps; another thread can enter; on notify, the waiter re-acquires the lock and resumes (re-checking the predicate).
5. **Q (TRICKY): Why re-check the predicate after wait() returns?** A: Mesa semantics (signal-and-continue) + spurious wakeups: the condition may be false again when you wake — hence `while`, not `if`.
6. **Q: notify() vs notifyAll()?** A: notify wakes one waiter (lost-wakeup risk if wrong waiter/condition); notifyAll wakes all (safe, but thundering herd). Default to notifyAll when conditions are shared.
7. **Q: What does "reentrant" mean for a monitor?** A: The same thread can re-enter synchronized methods (recursion/nested calls) — the lock has an owner + count, avoiding self-deadlock.
8. **Q (PRODUCTION): All methods synchronized on one object → bottleneck. Fix?** A: Fine-grained locking: split monitors, use read-write locks for read-mostly, use concurrent collections (e.g., ConcurrentHashMap) — the monitor granularity is the contention source.
9. **Q: What are the semantics of Java's wait/notify vs POSIX CVs?** A: Same Mesa model; Java uses one implicit CV per object (wait/notify/notifyAll) while pthreads lets you create multiple CVs per mutex.
10. **Q: Can a monitor solve the producer-consumer problem?** A: Yes — the bounded-buffer monitor (put/take with while-wait and notifyAll) is the canonical solution; the buffer state + CVs live inside the monitor.
11. **Q: What's the downside of signal-and-continue (Mesa)?** A: The signaler keeps running and the woken thread only gets a *hint* — it must re-check the predicate; lost-wakeup requires notifyAll or careful predicate design.
12. **Q (TRICKY): Two synchronized methods on the same object, called from the same thread. Deadlock?** A: No — monitors are reentrant: the same owner can re-enter, the count just increments. Deadlock only if *different* threads hold *different* locks in opposite order.

## 14. Follow-Up Questions
1. **Q: What's the difference between a monitor and a semaphore?** A: Monitor = structural ME + CVs (wait on state); semaphore = free-standing counter (wait on count, no structure). Monitors are safer; semaphores are more flexible.
2. **Q: What is a "bounded buffer monitor" exactly?** A: An object with cap-sized buffer, put/take methods (synchronized), and two conditions (full/empty) implemented via wait/notify.
3. **Q: How does Go differ from monitors?** A: Go channels = message passing (CSP), a different model; Go mutexes still exist for shared state, but channels are preferred for goroutine communication.
4. **Q: What is the "signal-and-continue vs signal-and-wait" tradeoff?** A: Continue (Mesa) is simpler (no lock handoff); wait (Hoare) has guaranteed predicate but complex semantics — all mainstream languages chose Mesa.
5. **Q: How do C# lock and Java synchronized differ?** A: Nearly identical semantics; C# also offers Monitor.Enter/Exit and async-friendly SemaphoreSlim.

## 15. Coding Example
```java
// Java monitor: bounded buffer (producer-consumer) — no explicit locks
public class BoundedBuffer<E> {
    private final java.util.ArrayDeque<E> q = new java.util.ArrayDeque<>();
    private final int cap;

    public BoundedBuffer(int cap) { this.cap = cap; }

    public synchronized void put(E e) throws InterruptedException {
        while (q.size() == cap) wait();        // full: wait, release lock
        q.add(e);
        notifyAll();                            // wake consumers
    }

    public synchronized E take() throws InterruptedException {
        while (q.isEmpty()) wait();             // empty: wait, release lock
        E e = q.remove();
        notifyAll();                            // wake producers
        return e;
    }
}
```
```csharp
// C# equivalent with lock
public sealed class BoundedBuffer<T> {
    private readonly Queue<T> q = new();
    private readonly int cap;
    private readonly object gate = new();
    public void Put(T item) {
        lock (gate) {
            while (q.Count == cap) Monitor.Wait(gate);
            q.Enqueue(item);
            Monitor.PulseAll(gate);
        }
    }
}
```

## 16. Industry Usage
- **Java**: synchronized everywhere — collections (Vector, Hashtable legacy; ConcurrentHashMap uses internal striping), Executors, servlets (synchronized handlers).
- **C#**: lock/Monitor in .NET.
- **Python**: threading.Lock + Condition (monitor-ish).
- **C++**: std::mutex + std::condition_variable used to build monitor-style classes.
- **Databases**: pessimistic row locking is monitor-like; MVCC is the lock-free alternative.

## 17. References
- Hoare, "Monitors: An Operating System Structuring Concept" (CACM 1974).
- Brinch Hansen, "Operating System Principles" (1973) — monitors.
- Silberschatz, *OS Concepts*, 7.7 (Monitors).
- Java Language Spec: synchronized, Object.wait/notify.
- C# spec: lock/Monitor.

## 18. Cheat Sheet
- Monitor = data + methods with implicit lock; one thread inside at a time.
- wait() releases lock + sleeps; notify/notifyAll wake.
- Reentrant: same owner can re-enter (count).
- Mesa semantics: re-check predicate in while loop.
- notify = one waiter; notifyAll = all (safer).
- Java: synchronized / wait / notify / notifyAll.
- C#: lock / Monitor.Wait / Pulse / PulseAll.
- Bounded buffer monitor: put/take + while-wait + notifyAll.
- Coarse granularity → contention → fine-grained alternatives.
- No self-deadlock (reentrant), but cross-object lock ordering still matters.

## 19. Quiz
1. Monitor guarantees: a) atomic methods b) one thread inside c) fairness d) speed → **b**
2. wait() inside monitor: a) keeps lock b) releases + sleeps c) spins d) signals → **b**
3. Java implicit condition: a) one per object b) one per class c) many d) none → **a**
4. Reentrancy: a) other thread re-enters b) same owner re-enters c) no re-entry d) all → **b**
5. Mesa means: a) guaranteed b) re-check predicate c) no wake d) Hoare → **b**
6. notifyAll wakes: a) one b) all c) none d) two → **b**
7. Producer-consumer monitor uses: a) explicit locks b) while-wait + notifyAll c) semaphores d) spin → **b**
8. Coarse monitor causes: a) races b) contention c) deadlock d) priority → **b**
9. Self-deadlock in reentrant monitor: a) yes b) no c) always d) only nested → **b**
10. Java monitor bytecodes: a) enter/exit b) monitorenter/monitorexit c) lock/unlock d) get/put → **b**

## 20. Flashcards
- **Q: Monitor?** → **A:** Data+methods, implicit lock, one thread inside.
- **Q: wait()?** → **A:** Release lock + sleep; re-acquire on wake.
- **Q: Reentrant?** → **A:** Same owner re-enters (count).
- **Q: Mesa?** → **A:** Signal = hint; re-check predicate.
- **Q: notify vs notifyAll?** → **A:** One vs all (notifyAll safer).
- **Q: Java?** → **A:** synchronized + wait/notify/notifyAll.
- **Q: C#?** → **A:** lock + Monitor.Wait/Pulse.
- **Q: Granularity issue?** → **A:** One object lock = contention.

## 21. Revision
Monitors make mutual exclusion structural: data + methods where the compiler/runtime enforces one-thread-at-a-time, with condition variables (wait/notify) for state waiting. Java synchronized/wait/notify and C# lock/Monitor are the practical forms. Key subtleties: Mesa semantics (re-check predicates in while loops), reentrancy (same owner re-enters), and notify vs notifyAll. Monitors compose cleanly (bounded-buffer) but serialize on one object lock — fine-grained/read-write alternatives address contention.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a monitor?" | 13 Q1 / 7 Formal Definition |
| "Monitor vs mutex?" | 13 Q2 / 4 Why Wasn't Another Approach Chosen |
| "Java synchronized = ?" | 13 Q3 / 7 Formal Definition |
| "What happens on wait()?" | 13 Q4 / 9 Internal Working |
| "Why re-check predicate?" | 13 Q5 / 8 Example |
| "notify vs notifyAll?" | 13 Q6 / 7 Formal Definition |
| "Reentrant meaning?" | 13 Q7 / 7 Formal Definition |
| "Synchronized bottleneck fix?" | 13 Q8 / 12 Disadvantages |
| "Can a monitor solve producer-consumer?" | 13 Q10 / 8 Example |
| "Mesa downside?" | 13 Q11 / 12 Disadvantages |
