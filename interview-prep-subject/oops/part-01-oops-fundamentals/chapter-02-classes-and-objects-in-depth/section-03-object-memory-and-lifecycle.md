# Object Memory and Lifecycle

> **TL;DR**: Objects are born on the heap via `new`, reachable through references on the stack, and die when they become unreachable — in Java a GC reclaims them (nondeterministically), in C++ a destructor runs (deterministically), and knowing exactly *where* and *when* an object lives is the root of both memory-leak and dangling-pointer bugs.

## 1. Why Does This Exist?
Every object must have a defined **birth** (allocation), **life** (reachable, usable), and **death** (reclamation). Without a model of where objects live, you cannot reason about: leaks (objects that never die), dangling pointers (references to dead objects), stack-vs-heap placement, and GC vs manual memory. The lifecycle concept exists because memory is finite — a program that creates objects forever without reclaiming them eventually exhausts the heap (OutOfMemoryError). Interviews probe this because "where does the object live?" and "when is it collected?" reveal whether you understand reference semantics, the stack, the heap, and GC — the three pillars of runtime memory.

## 2. How Does It Work?
**Java (reference semantics):**
1. `new Foo()` → object allocated on the **heap** (young generation).
2. A **reference** to it lives on the stack (local variable) or in another object (field).
3. Object is alive while reachable (through a chain of references from a GC root).
4. When unreachable → GC marks, sweeps/compacts → memory reclaimed. No destructor runs.

**C++ (value + reference semantics):**
1. `Foo f;` → object on the **stack**; dies at scope exit (destructor runs).
2. `Foo* f = new Foo();` → object on the **heap**; dies only when you `delete f` (destructor runs) — else **leak**.
3. Members die after their containing object, in reverse declaration order.

The core mechanism: **reachability** (Java) vs **lifetime determinism** (C++).

## 3. When Is It Used?
- **Java**: GC is always on — object lifecycle is "allocate → use → become unreachable → collected". Tuning happens for throughput/latency (G1, ZGC, C4).
- **C++**: stack objects for short, deterministic lives (RAII); heap objects for dynamic sizes/long lives, freed with `delete`/smart pointers (`unique_ptr`, `shared_ptr`).
- **Object pools**: reuse objects to avoid repeated allocate/free (DB connections, threads).
- **Leak analysis**: `jmap`/`MAT` (Java), `valgrind`/ASan (C++) to find objects that never die.
- **Weak references**: caches that must not keep objects alive (`WeakHashMap`).

## 4. Why Wasn't Another Approach Chosen?
- *Why not all-stack (no heap)?* Because dynamic sizes and shared/long-lived data can't live on the stack; the heap exists for objects whose lifetime exceeds the creating scope. (C++ can stack-allocate most things; Java can't.)
- *Why not all-manual memory (C style)?* Because manual `malloc`/`free` produced use-after-free, double-free, and leaks — billions of dollars of bugs. GC chosen for safety; RAII chosen for determinism.
- *Why not all-GC (Java) or all-RAII (C++) everywhere?* Java GC costs pause-time and hides cleanup; C++ manual memory risks bugs. The industry settled on **hybrid**: GC with disciplined resource cleanup (Java) or deterministic RAII with smart pointers (C++).
- *Why not reference counting everywhere?* Cycles leak (A↔B references never reach zero); modern GCs and `shared_ptr` must handle cycles specially — the design trade-off is pause-time vs cycle-handling complexity.

## 5. Intuition
Think of **library books**. A book on the stack is like a library copy someone borrows and must return (deterministic) — when the borrower's term (scope) ends, the book is returned. A book on the heap is like a book that may be passed between readers; it lives until *nobody* holds it (Java: GC notices nobody references it; C++: you must call the librarian to return it). If nobody returns the heap book (C++), the library fills up with books nobody can use — a **memory leak**. If someone returns a book still being read (Java dangling via weak refs / C++ dangling pointer), you get a crash. The library is the heap; the due dates are the lifecycle rules.

## 6. Real-World Analogy
A **hotel with two room types**: stack rooms = "rooms assigned to you for the duration of your stay in a lobby (scope)" — cleaned automatically when you leave the lobby (deterministic). Heap rooms = "rooms you can keep until you check out" — the Java hotel has a janitor (GC) who cleans rooms nobody has a key to, whenever it gets around to it; the C++ hotel requires you to check out yourself (`delete`), or the room stays occupied forever (leak). You can also carry a *copy of the key* (reference) — as long as any key exists, the janitor won't clean (reachability).

## 7. Formal Definition
The **object lifecycle** is the sequence: **allocation** (reserving memory, typically on the heap for Java objects, stack or heap for C++), **initialization** (constructor runs), **use** (reachable via references; state mutations legal), and **reclamation** (freeing memory — GC in Java when unreachable; destructor + `delete`/scope-exit in C++). **Reachability** (Java): an object is live if transitively referenced from a GC root (static fields, stack locals, registers, JNI refs). In C++ **lifetime** is determined by scope (stack) or explicit/ownership-based deletion (heap).

## 8. Example
```java
public class Demo {
    static Demo global = new Demo("static");   // GC root: static field keeps it alive forever
    private final String label;
    public Demo(String label) { this.label = label; }
    public static void main(String[] args) {
        Demo local = new Demo("local");        // heap object #2, referenced by stack var 'local'
        makeTemp();                             // object #3 created and dropped inside
        local = null;                           // object #2 becomes unreachable → eligible for GC
        // global (object #1) still reachable via Demo.global
    }
    static void makeTemp() {
        new Demo("temp");                       // created, never stored → immediately unreachable
    }
}
```
Step by step: three objects created. `global` never dies (static root). `local` dies when `local=null` (GC may reclaim later). `temp` dies immediately after the call. In Java, *none* of these dies exactly when you'd think — GC decides when. Contrast in C++: `makeTemp()`'s object must be `delete`d or it leaks, and `local` (if a local object, not pointer) dies at the closing brace.

## 9. Internal Working
**Java GC (HotSpot, G1/ZGC):**
1. `new` → bump-pointer allocation in a thread-local Eden (young gen), O(1) amortized.
2. Object header: mark word (GC age, lock bits, hash) + klass pointer.
3. Young GC: live objects (reachable) copied to Survivor; dead objects' memory just gets overwritten next allocation (cheap death).
4. Objects surviving N collections promoted to Old gen; a mixed/full GC eventually collects Old.
5. Roots scanned: stack locals, statics, JNI; objects reachable from them are marked live; the rest are dead.
6. `System.gc()` is a *suggestion*, not a guarantee.

**C++:**
1. Stack object: sub-sp stored once at construction; destructor inlined at scope exit; O(1).
2. Heap object: `new` → `malloc` + constructor; `delete` → destructor + `free`. Missing `delete` = leak; double delete = UB; using after delete = UB (dangling).
3. Smart pointers: `unique_ptr` = ownership, delete on scope exit; `shared_ptr` = refcount, delete at zero (cycle hazard).

## 10. Time Complexity
- Java allocation: O(1) amortized (TLAB bump).
- GC young collection: O(live objects) — most objects die in Eden cheaply; amortized O(1) per allocation.
- Full GC: O(heap) — that's why pauses scale with heap size (mitigated by G1/ZGC).
- C++ stack alloc: O(1) (sp adjustment); heap `new`/`delete`: O(1)-ish (malloc/free), but malloc can be O(size) for large blocks (mmap).
- Leak detection tools: O(program) analysis — not a runtime cost.
- `shared_ptr` copy: O(1) refcount increment (atomic, cheap).

## 11. Advantages
- **Java**: automatic reclamation removes the largest class of memory bugs (use-after-free, double-free, most leaks); allocation is fast; no cleanup code for ordinary objects.
- **C++**: deterministic cleanup (RAII) — resources released exactly when scopes end; predictable memory behavior, no GC pauses; fine control over layout.
- Both: lifetime models make production debugging tractable (heap dumps, ASan, GC logs).

## 12. Disadvantages
- **Java**: GC pauses and non-deterministic cleanup; objects that "should" die may live longer (memory retention); `OutOfMemoryError` if refs leak (e.g., caches, static collections).
- **C++**: manual ownership → leaks, dangling pointers, double-free; `shared_ptr` cycles; more cognitive load.
- Both: heap fragmentation, cache misses from object indirection.

## 13. Interview Questions
1. **Q: Where do Java objects live and where do references live?** A: Objects on the heap; references on the stack (locals) or inside other objects (fields). Primitives in locals live on the stack.
2. **Q: When is an object eligible for GC?** A: When it is unreachable from any GC root (static fields, stack/register refs, JNI refs). `null`-ing a variable or exiting its scope makes the object unreachable — GC may collect it later (or never).
3. **Q: What's the difference between a leak in Java vs C++?** A: C++ leaks = allocated-but-never-deleted; Java leaks = objects still reachable (held by static caches, listeners, contexts) that you intend to be dead — "unintentional retention", not true leak, but the effect (OOM) is the same.
4. **Q: TRICKY — Can you force GC in Java?** A: Not reliably. `System.gc()` is a hint; the JVM may ignore it. Correct approach: fix reachability — remove references, use `WeakReference` for caches, close resources.
5. **Q: What is a dangling pointer vs a memory leak?** A: Dangling = pointer to freed/out-of-scope memory (use-after-free, UB); leak = allocated memory with no reachable pointer (can never be freed). GC eliminates dangling refs for Java; C++ needs care.
6. **Q: What is the stack and heap conceptually?** A: Stack = per-thread, LIFO, fast, grows/shrinks with calls — local variables and references; heap = shared, dynamic, long-lived objects. Stack objects die at scope exit; heap objects die at `delete`/GC.
7. **Q: SCENARIO — A long-running Java server OOMs. What do you do?** A: Take a heap dump (`jmap -dump`), load in MAT/Eclipse: find the retained set — usually a static collection, cache, or leaked listener holding objects alive. Fix the reachability, not the heap size.
8. **Q: What is a WeakReference and when do you use it?** A: A reference that doesn't keep an object alive; when only weak refs remain, GC collects the object. Used in caches (WeakHashMap), avoiding listener leaks. Compare: Strong (normal), Soft (collect under pressure), Weak (collect immediately when weakly-reachable).
9. **Q: PRODUCTION — Stack overflow vs heap overflow?** A: Stack overflow: infinite/deep recursion (StackOverflowError) — stack is small (per-thread, ~1MB default). Heap overflow: OutOfMemoryError — heap exhausted by live/retained objects. Fixes differ: fix recursion depth vs fix retention.
10. **Q: TRICKY — Can a stack object in C++ escape its scope?** A: Returning a *pointer/reference* to a local → dangling (UB). Returning by *value* → a copy (safe). Always return by value or allocate on the heap with a smart pointer.
11. **Q: What are GC roots?** A: Entry points the GC scans: static fields, thread stack locals, registers, JNI references, and (historically) the "current method frames". Reachability is defined relative to these roots.
12. **Q: Why does C++ use RAII instead of GC?** A: Determinism: destructors run exactly when scopes end (needed for locks, files, sockets) and there are no GC pauses — critical for low-latency systems. GC trades determinism for convenience.
13. **Q: SCENARIO — Which is safer: `shared_ptr` in a doubly-linked list or a tree with parent pointers?** A: `shared_ptr` creates cycles (nodes reference each other) → refcount never hits zero → leak; use `unique_ptr` for children + raw pointers for parents. Always watch for cycles with reference counting.
14. **Q: What is object resurrection?** A: In `finalize()` (removed in Java 18), an object could reassign `this` to a static/global, becoming reachable again — "resurrected" — and GC would skip it. A classic reason finalizers were unsafe.
15. **Q: PRACTICAL — When should you null out a reference?** A: Rarely, in modern Java — the JIT/GC handles locals well; but nulling long-lived fields (e.g., after a batch) can release large objects early. Prefer scoping and weak references.
16. **Q: TRICKY — Does setting a reference to null call any destructor in Java?** A: No — there's no destructor; the object just becomes eligible. Cleanup of resources is via `close()` (try-with-resources), never via GC.

## 14. Follow-Up Questions
1. **Q: What is a memory "retained set"?** A: The set of objects that would be freed if a given object were collected — heap dump analysis uses retained sets to find what a suspected leak is actually holding.
2. **Q: Why are Eden/Survivor generations needed?** A: Most objects die young; splitting the heap lets GC collect tiny Eden cheaply and promote survivors — amortized O(1) allocation and short pauses (generational hypothesis).
3. **Q: What's the difference between G1, ZGC, and Shenandoah?** A: G1 = region-based, moderate pauses; ZGC/Shenandoah = concurrent/parallel, sub-millisecond pauses at the cost of throughput. Choice depends on pause-time budget.
4. **Q: When is a Java object collected if only a WeakReference and the object's own `finalize` (legacy) point to it?** A: Finalization is skipped if a finalizer already ran or the object was resurrected; the weak reference's queue is notified. With finalizers removed, a weakly-reachable object is simply collected.

## 15. Coding Example
```java
import java.lang.ref.WeakReference;
import java.util.*;

public class Lifecycle {
    public static void main(String[] args) {
        Object strong = new Object();              // strongly reachable
        WeakReference<Object> weak = new WeakReference<>(strong);
        strong = null;                             // now ONLY weakly reachable
        System.gc();                               // hint (not guaranteed)
        System.out.println(weak.get() == null);    // likely true: collected

        Map<String, String> cache = new WeakHashMap<>();
        String key = new String("k");
        cache.put(key, "value");
        key = null;                                // key only weakly referenced by the map
        System.gc();
        System.out.println(cache.isEmpty());       // likely true: entry evicted with key
    }
}
```
```cpp
#include <memory>
#include <cstdio>
struct Res { ~Res() { std::puts("dtor"); } };
int main() {
    Res stack;                        // destructor at scope exit (deterministic)
    auto heap = std::make_unique<Res>();  // RAII: destructor at scope exit too
    // no manual delete needed
    return 0;                         // both destructors print "dtor" in reverse order
}
```
```python
import weakref, gc
class Res: pass
r = Res()
wr = weakref.ref(r)
del r                                # object eligible immediately (refcount in CPython)
print(wr() is None)                  # True: collected deterministically-ish
```

## 16. Industry Usage
- **Java services (Amazon, LinkedIn)**: heap dumps via `jmap`/Eclipse MAT are the standard OOM debugging flow; G1/ZGC tuning for latency; WeakHashMap/WeakReference for caches and caches of class metadata.
- **C++ systems (HFT, Chrome, games)**: RAII + `unique_ptr` everywhere; ASan (AddressSanitizer) in CI to catch use-after-free; custom allocators and object pools to control allocation hotspots.
- **JVM languages**: Kotlin/Scala inherit the same lifecycle; Android uses GC but asks devs to avoid allocations on UI thread.
- **Netty**: pooled buffers (`ByteBuf`) use reference counting — an explicit "delete me when done" pattern inside Java, proving that GC alone isn't enough for high-volume buffers.
- **Operating systems**: Linux kernel uses `refcount` (reference counting) for objects shared across contexts — the same cycle/leak discipline as `shared_ptr`.

## 17. References
- Oracle, *Java Memory Management* whitepapers and G1/ZGC docs: https://docs.oracle.com/en/java/javase/17/gctuning/
- Joshua Bloch, *Effective Java* — Item 7 (eliminate obsolete object references).
- Scott Meyers, *Effective C++* — Items on new/delete, RAII; *Effective Modern C++* on smart pointers.
- Herb Sutter, *C++ and Beyond* talks on lifetimes.
- JLS Ch. 12, §12.6 (Finalization of Class Instances) & Ch. 12.7: https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html

## 18. Cheat Sheet
- Java: objects on heap, refs on stack/fields; reachability = liveness.
- GC roots: statics, stack locals, registers, JNI.
- Java death is nondeterministic — never rely on it for cleanup.
- C++: stack = scope-lifetime; heap = `new`/`delete` or smart pointers.
- Leak = unreachable-but-allocated (C++) or reachable-but-unwanted (Java retention).
- Dangling = using freed memory (C++ UB); GC prevents this in Java.
- Weak vs Soft vs Strong: Weak collected when weakly-reachable; Soft under pressure; Strong keeps alive.
- RAII = deterministic cleanup; GC = convenient but nondeterministic.

## 19. Quiz
1. Java objects live on: a) stack b) heap c) registers d) code cache → **b**
2. An object is eligible for GC when: a) its destructor runs b) it's unreachable from roots c) `System.gc()` runs d) it goes out of scope → **b**
3. A C++ object allocated with `new` without `delete` causes: a) dangling pointer b) memory leak c) double-free d) GC → **b**
4. Use-after-free is: a) a Java feature b) undefined behavior in C++ c) a GC optimization d) a WeakReference → **b**
5. WeakReference keeps the object: a) alive forever b) alive until GC pressure c) does NOT keep it alive d) alive until `delete` → **c**
6. True or False: `System.gc()` guarantees immediate collection. → **False**

## 20. Flashcards
- **Q: Where do Java objects and references live?** → **A:** Objects on heap; references on stack/fields.
- **Q: When is an object GC-eligible?** → **A:** When unreachable from GC roots (statics, stack, JNI).
- **Q: Leak vs dangling?** → **A:** Leak = allocated but never freed/reachable; dangling = using freed memory (C++ UB).
- **Q: Java "leak" vs C++ leak?** → **A:** C++ = missed `delete`; Java = unintended retention via reachable refs.
- **Q: What is RAII?** → **A:** Resource lifetime tied to scope — destructor at scope exit (deterministic).
- **Q: When to use WeakReference?** → **A:** Caches/maps that must not keep objects alive.
- **Q: Why are GC roots scanned?** → **A:** Reachability (liveness) is defined from roots; GC collects everything else.

## 21. Revision
Java objects live on the heap, referenced from the stack or other objects; liveness = reachability from GC roots (statics, stack, JNI), so GC death is nondeterministic and never a cleanup mechanism — use try-with-resources. C++ gives deterministic lifetimes: stack objects die at scope exit (RAII destructors), heap objects need `delete` or smart pointers; misuse → leaks, dangling pointers, double-free. Weak/soft references avoid unintended retention. First-30-seconds answers: "objects on heap, refs on stack; GC collects unreachable, deterministic C++ cleanup via RAII."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Where do objects live in Java?" | Interview Q1 / Section 8 |
| "When is an object GC-eligible?" | Interview Q2 / Internal Working |
| "Java leak vs C++ leak?" | Interview Q3 / Section 13 |
| "Can you force GC?" | Interview Q4 |
| "Dangling vs leak?" | Interview Q5 |
| "How do you debug a Java OOM?" | Interview Q7 / Section 16 |
| "WeakReference use case?" | Interview Q8 / Section 15 |
| "RAII vs GC?" | Interview Q12 / Section 16 |
