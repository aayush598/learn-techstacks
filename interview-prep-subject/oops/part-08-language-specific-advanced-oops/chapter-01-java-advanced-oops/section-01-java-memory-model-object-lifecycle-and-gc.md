# Java Memory Model, Object Lifecycle & Garbage Collection

> **TL;DR**: A Java object lives on the heap, is referenced through stack/metaspace roots, and is reclaimed by an automatic garbage collector (GC) that frees you from manual `free()` — but only if you understand object reachability, generations, and the cost of allocation.

## 1. Why Does This Exist?
C and C++ make the programmer responsible for memory: `malloc`/`new` hands out blocks and `free`/`delete` must return them exactly once. Bugs are catastrophic and invisible: use-after-free (silent corruption), double-free (crash), leaks (OOM). Java exists partly to eliminate this entire class of bugs. The JVM adds an automatic memory manager (the GC) so that the object lifecycle is: allocate → use → become unreachable → reclaimed. The "why" of the Java memory model is **safety + productivity**: no dangling pointers, no manual ownership, deterministic-enough allocation cost, and a well-defined story for multithreaded visibility (the Java Memory Model, JSR-133).

## 2. How Does It Work?
At a glance, three runtime areas matter:
- **Stack** — one per thread, holds primitive values and *references* to objects, plus each frame's local variables and operand stack.
- **Heap** — shared by all threads, holds the *objects themselves* (all `new` targets).
- **Metaspace** (Java 8+, replaced PermGen) — holds class metadata: the class object, method bytecode, constant pools, and v-table-like dispatch info.

The object itself has a **header** (mark word + klass pointer), then instance fields, then optional padding. The GC decides death by **reachability**: an object is live iff reachable from the GC roots (local variables on thread stacks, static fields, `Thread` references, JNI references, class loaders). Unreachable objects are garbage.

## 3. When Is It Used?
- On **every `new`** — allocation is a bump-the-pointer on the young generation (extremely cheap, ~10ns, cheaper than `malloc` on many workloads).
- On **every allocation threshold crossing** — a young-GC (minor GC) runs when the young generation fills.
- On **promotion** — objects that survive multiple young GCs are tenured (moved) to the old generation.
- On **old-gen exhaustion** — a full GC (major GC) runs, usually with a stop-the-world pause.
- On **`System.gc()`** — a *hint* only; the JVM may ignore it (it triggers Full GC when `-XX:+ExplicitGCInvokesConcurrent` is set, or nothing under G1/ZGC).

## 4. Why Wasn't Another Approach Chosen?
Alternatives to automatic GC:
- **Manual memory management (C/C++)**: gives control but produces leaks/use-after-free; rejected for Java's safety goals.
- **Reference counting (Python, early C++ smart pointers)**: simple, but needs cycle detection (extra collector) and has per-assignment atomic overhead; JVM chose reachability tracing instead because cycles are collected *naturally*.
- **Region-based / arena allocation (Rust's ownership, C++ arenas)**: gives determinism and zero pause but demands the *programmer* enforce lifetimes at compile time — incompatible with Java's "everything is a reference" ergonomics.
- **Bohem GC-style conservative scanning**: scanning registers/stack imprecisely; the JVM uses *precise* (exact) object maps from JIT-compiled code, so it never misidentifies a random bit pattern as a pointer.

## 5. Intuition
Think of the heap as a **warehouse** and your program as workers who add boxes (objects). The GC is a **janitor** who only throws away boxes that nobody can reach. The janitor never tracks every box continuously; instead, every so often it draws a line from every *entrance* (the stack — what a worker is holding) and keeps anything the entrances lead to. Boxes not on any chain from an entrance are garbage. Because young boxes are usually trash quickly (short-lived temporaries), the janitor separates the warehouse into a small "recent drop-off zone" (young gen) and a big "long-term storage" (old gen), sweeping the drop-off zone far more often.

## 6. Real-World Analogy
A **restaurant's ingredient fridge**: the *stack* is the chef's cutting board (what's being worked on right now, per cook). The *heap* is the fridge (shared storage). The *GC* is the stock clerk: every night he marks every item reachable from the chef's current order tickets; anything else is expired and thrown out. A chef never has to remember to throw things away — the clerk does it for all chefs. Some items (a shared secret sauce recipe) are kept forever because the head chef's board (a static root) always references them.

## 7. Formal Definition
The Java Virtual Machine Specification (JVM Spec, JSR-924) defines a runtime data area model: per-thread *PC register*, *JVM stack* (frames of local variables + operand stack), *native method stacks*, and the shared *heap* plus *method area* (implemented in modern HotSpot as Metaspace). Object memory layout: an object header (mark word storing hash, lock state, GC age; klass pointer to type metadata), instance data, and alignment padding. Garbage collection is the automatic process of identifying objects no longer reachable from the GC root set and reclaiming their memory, governed by the *Java Language Specification* §17.4 *Java Memory Model* for visibility/ordering guarantees.

## 8. Example
Trace one object, `new Counter()`:
1. `main()` starts; JVM creates the `main` thread stack with a frame for `main`.
2. Bytecode `new Counter` → JVM reserves 16 bytes (8 header + 8 for `int` field) in the young gen via bump-the-pointer.
3. `dup` + `invokespecial <init>` → constructor runs, header's klass pointer set, mark word zeroed.
4. `astore_1` stores the *reference* (a 4/8-byte heap address or compressed oop) in `main`'s local slot 1.
5. `main` calls `run()` which does `new Counter()` again; the second object is referenced only by `run`'s local slot.
6. `run()` returns → its frame is popped → the second object's only reference disappears → it is now unreachable.
7. Young gen fills → young GC: root scan finds `counter1` (reachable), does NOT find `counter2` → `counter2` is copied/compacted or simply marked dead → its 16 bytes reclaimed; `counter1` survives, age incremented.
8. After N survive-cycles, `counter1` promotes to old gen.

## 9. Internal Working
1. **Allocation**: TLAB (Thread-Local Allocation Buffer) — each thread gets a private slice of Eden; `new` is just bump-pointer + `store` (no lock). Overflow → allocates a new TLAB from Eden.
2. **Young GC (minor)**: when Eden fills. Root scan from stacks, statics, JNI, registers. Live objects in Eden + one survivor space are copied to the other survivor space (copying collector, mark phase: objects marked through object graph). Age counter increments; survivors above threshold (default 15, via `-XX:MaxTenuringThreshold`) promote to old gen.
3. **Promotion + old GC (major/full)**: old gen fills → mark-sweep-compact (or G1 mixed collections). Mark live set, then sweep dead, then optionally compact to kill fragmentation.
4. **Pause times**: young GCs are ~ms (small regions); full GCs are stop-the-world and can be seconds on huge heaps. Modern collectors (G1 default since Java 9, ZGC/Shenandoah) shrink pauses by doing most work concurrently with application threads.
5. **Finalization**: `finalize()` is deprecated (Java 9) and effectively removed (Java 18) — it ran after death but before reclamation, caused resurrection bugs and long pauses. `Cleaner`/`Cleanable` (Java 9+) or try-with-resources is the replacement.

## 10. Time Complexity
- Allocation (TLAB bump): **O(1)** — one pointer increment + store, cheaper than `malloc`.
- Young GC (copying): **O(live objects)** — proportional to survivors, not total heap; dead objects cost ~nothing (just skipped).
- Full GC mark-sweep: **O(heap size)** for marking, plus sweep; compaction adds O(n) moves.
- Finalizer execution (legacy): O(1) per object but runs on a dedicated thread — introduces unbounded, hard-to-predict latency.
- Memory overhead per object: 12–16 byte header (compressed oops make references 4 bytes on heaps < 32 GB).

## 11. Advantages
- No manual memory management → no use-after-free, double-free, or leaks as a class of bug.
- Compaction fights fragmentation, unlike naive `malloc`/`free`.
- Young-gen copy makes short-lived allocations cheaper than `malloc`.
- Precise, concurrent collectors (G1/ZGC) keep p99 pauses bounded (ZGC targets < 1 ms).
- Language-level reachability gives a clear contract for when resources can be released.

## 12. Disadvantages
- Stop-the-world pauses (though shrinking) are unpredictable for real-time/ultra-low-latency systems.
- GC adds CPU/bandwidth overhead; tuning flags (`-Xmx`, `-XX:NewRatio`, GC choice) is a specialist skill.
- No deterministic destruction: you cannot say "this object's native resource is freed *now*" the way RAII does in C++.
- Heaps over 32 GB disable compressed oops, increasing memory footprint.
- Unreachable-but-resource-holding objects can exhaust native resources (file descriptors) while Java heap looks fine.

## 13. Interview Questions
1. **Q: Where do objects live in Java?** A: On the heap; references live on thread stacks (locals) or in static/instance fields; class metadata lives in Metaspace.
2. **Q: What are GC roots?** A: Live thread stacks (local variables, operand stack), static fields of loaded classes, JNI references, and (historically) the current PC's registers — the only places a live object can be first reached from.
3. **Q: What is a minor GC vs a full GC?** A: Minor collects the young gen only (copying, cheap, frequent). Major/full collects the whole heap including old gen (mark-sweep, expensive, stop-the-world).
4. **Q: How does an object "die"?** A: It doesn't have an explicit death; it becomes unreachable from roots and the next GC reclaims it.
5. **Q: Why is allocation in Java considered cheap?** A: Bump-the-pointer on a TLAB is O(1) and lock-free; because many objects die young, the young GC reclaims them nearly for free without compaction work.
6. **Q: What is the difference between PermGen and Metaspace?** A: PermGen (pre-Java 8) was a fixed-size heap area for class metadata; Metaspace uses native memory that grows as needed, removing the "OutOfMemoryError: PermGen space" class.
7. **Q: What does `System.gc()` do?** A: It only *suggests* a GC; HotSpot may ignore it or run a full GC depending on flags; you should never rely on it.
8. **Q: What is the object header and why does it exist?** A: The header stores the mark word (identity hash, lock state for biased/thin locks, GC age) and a klass pointer to class metadata; it's what lets the GC and the synchronized machinery tag any object.
9. **Q: What is a stop-the-world event?** A: A phase where application threads are paused so the collector can scan roots safely; young GCs are short, full GCs are long.
10. **Q: Why is `finalize()` deprecated?** A: It runs at an arbitrary time after death, can resurrect objects (resetting reachability), introduces long pause, and hides resource leaks; use try-with-resources or `Cleaner`.
11. **Q: What is the default GC in modern Java?** A: G1 (Garbage-First) since Java 9; ZGC and Shenandoah are low-pause alternatives for large heaps.
12. **Q: Can you force an object to be collected?** A: No direct API; null out references and let reachability do the work; `WeakReference` lets you observe collection via the `ReferenceQueue`.
13. **Q: What's the difference between `StrongReference`, `SoftReference`, and `WeakReference`?** A: Strong = never collected while reachable; Soft = collected only when memory is low; Weak = collected whenever it's no longer strongly reachable.
14. **Q: How do you find a memory leak in a Java app?** A: Heap dump + analyzer (Eclipse MAT/JProfiler), diff heap snapshots, look for growing caches/static collections/`ClassLoader` retention (classloader leak).
15. **Q: What is the Java Memory Model?** A: JLS §17.4 — the happens-before rules that define when one thread's write is visible to another; it's about visibility/ordering, not about GC.
16. **Q: What is a TLAB?** A: Thread-Local Allocation Buffer — a per-thread Eden slice making allocation lock-free.
17. **Q: When does promotion happen?** A: When an object survives enough young GCs (age ≥ tenuring threshold) or the survivor space is full; it moves to old gen.
18. **Q: Why does the JVM have generational GC?** A: The weak generational hypothesis: most objects die young, so collecting the young gen frequently and the old gen rarely is cheap and effective.

## 14. Follow-Up Questions
1. **Q: What is the "weak generational hypothesis"?** A: Empirically, ~95%+ of objects die young; designing the heap in generations lets the collector spend most effort on the small, quickly-emptying young gen.
2. **Q: Why does G1 divide the heap into regions?** A: To do incremental, predictable collections — it reclaims the regions with the most garbage first ("Garbage-First"), keeping pause times bounded while still collecting the whole heap over time.
3. **Q: What's the difference between stop-the-world, concurrent, and parallel GC?** A: STW pauses all app threads; concurrent collectors (G1/ZGC) do marking while app threads run; parallel GC uses many GC threads *during* STW to shorten it.
4. **Q: How does ZGC achieve <1ms pauses?** A: Colored pointers + load barriers allow concurrent compaction, and relocation happens in tiny chunks so no phase requires stopping all threads for long.
5. **Q: Can a reference still exist but the object be garbage?** A: No — a live reference *is* a root; an object with any strong reference is reachable. But a reference can be "stale" in a collection (e.g., a `List` holding references to dead-anyway objects is a leak if the list lives forever).
6. **Q: How does the JVM know exactly which bits on the stack are pointers?** A: JIT-compiled code maintains precise safepoint metadata (stack maps / oop maps) that tell the GC exactly which slots are references — this is why HotSpot is a *precise* collector, unlike conservative collectors.
7. **Q: What's an "escape" and how does escape analysis help?** A: If the JIT proves an object never leaves a method (doesn't escape), it can allocate it on the stack or eliminate it entirely (scalar replacement) — removing GC pressure.

## 15. Coding Example
```java
public class ObjectLifecycleDemo {
    static int counter = 0;                      // static field: a GC root (keeps referencing objects alive)

    static class Counter {                       // a normal object: 16-byte header + int field
        int value;
        Counter(int v) { this.value = v; }
    }

    static void run() {
        Counter local = new Counter(1);          // local: rooted on this thread's stack
        for (int i = 0; i < 100; i++) {
            Counter tmp = new Counter(i);        // tmp escapes after each iteration -> young-gen garbage
        }
        local.value++;                           // still alive here
    }                                            // "local" dies when run() returns (frame popped)

    public static void main(String[] args) {
        Counter[] cache = new Counter[1_000_000]; // array on heap, rooted by "cache" (main frame)
        for (int i = 0; i < cache.length; i++) cache[i] = new Counter(i);
        run();
        System.gc();                             // hint, never rely on it in production
        System.out.println(cache[0].value);      // cache keeps the whole array reachable
        System.gc();                             // NOT a guarantee the array is collected - it isn't, cache is live
    }
}
```

```java
// Weak reference demo: observe collection
import java.lang.ref.WeakReference;

public class WeakRefDemo {
    public static void main(String[] args) {
        Counter c = new Counter(42);
        WeakReference<Counter> weak = new WeakReference<>(c);
        c = null;                                 // strong ref gone
        System.gc();
        System.out.println(weak.get());           // null after the GC ran (usually)
    }
}
```

## 16. Industry Usage
- **Every JVM production system** relies on the memory model: Tomcat/Spring apps, Apache Kafka (JVM), Elasticsearch, Hadoop/Spark JVM tasks, Netflix/Zillow/Scalable apps — all tuned with flags like `-Xmx`, `-XX:+UseG1GC`.
- **Low-latency fintech** uses ZGC/Shenandoah or off-heap memory (Netty `PooledByteBufAllocator` manages off-heap buffers precisely to dodge GC).
- **Spark/Storm** tune young-gen ratios to reduce GC stalls in streaming workloads; Databricks/JVM data engines cite GC pause as a top performance lever.
- **Profile tools** (YourKit, async-profiler, Java Flight Recorder) expose allocation rates and GC pauses — JFR is free in OpenJDK and expected knowledge at JVM shops.
- AWS/Google Cloud JVM-based services use container-aware GC flags (`-XX:MaxRAMPercentage`) so the JVM sizes its heap to the container limit.

## 17. References
- Oracle, *The Java Virtual Machine Specification (Java SE 17)*, ch. 2 "The Structure of the Java Virtual Machine".
- James Gosling et al., *The Java Language Specification*, §17.4 "Memory Model".
- Oracle, *HotSpot Virtual Machine Garbage Collection Tuning Guide* (docs.oracle.com/javase/gc/tuning).
- Oracle, *JEP 366: Deprecate the Finalization Mechanism*; *JEP 421: Deprecate `finalize()` for Removal*.
- Gil Tene, *Understanding Java Garbage Collection* (Azul, talks/white-papers).
- Baeldung, *Guide to Java Garbage Collection* (baeldung.com).
- `docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/ref/package-summary.html`

## 18. Cheat Sheet
- Objects → heap; references → stack/fields; class metadata → Metaspace.
- GC roots: thread stacks, statics, JNI, class loaders. Reachability decides life.
- Young gen = Eden + 2 survivors (copying); old gen = long-lived (mark-sweep-compact).
- Allocation is O(1) bump-the-pointer on a TLAB.
- `System.gc()` = hint. `finalize()` = deprecated. Use try-with-resources / `Cleaner`.
- G1 is default since Java 9; ZGC/Shenandoah for <1 ms pauses.
- Weak vs Soft vs Strong references = survival pressure.
- Compressed oops (default for heaps < 32 GB) make references 4 bytes.
- Precise GC uses safepoint oop maps, so no misread pointers.
- JFR / heap dumps are the standard tools for leak diagnosis.

## 19. Quiz
1. Where does the *object* (not the reference) live? a) Stack b) Heap c) Metaspace d) Native memory → **b**
2. Which is NOT a GC root? a) A local variable b) A static field c) An object field of a reachable object d) A JNI global reference → **c** (object fields are reached *through* roots; they are not themselves roots)
3. The default GC since Java 9 is: a) Parallel b) CMS c) G1 d) ZGC → **c**
4. `System.gc()` is best described as: a) Guaranteed full GC b) A hint c) An error d) A compile-time directive → **b**
5. An object becomes garbage when: a) `finalize()` runs b) The program ends c) It is no longer reachable from roots d) The heap is full → **c**
6. What does the mark word in the object header contain? a) Instance fields b) hashCode/lock/GC age c) The class name d) A pointer to the array length → **b**
7. A minor GC collects: a) Only the old gen b) Only the young gen c) The whole heap d) Metaspace → **b**
8. Which guarantee does the Java Memory Model NOT provide by default? a) `volatile` visibility b) Happens-before across synchronized blocks c) That two threads see writes instantly without synchronization d) Final field semantics → **c**
9. Promotion moves an object from: a) Old gen to young gen b) Young gen to old gen c) Heap to stack d) Metaspace to heap → **b**
10. Which is the correct replacement for `finalize()`? a) `clone()` b) try-with-resources / `Cleaner` c) `Object.finalize2()` d) `WeakReference` → **b**

## 20. Flashcards
- **Q: Where do Java objects live?** → **A:** On the heap; references live on stacks/fields; metadata in Metaspace.
- **Q: What decides if an object is garbage?** → **A:** Reachability from GC roots (thread stacks, statics, JNI, classloaders).
- **Q: Why are there generations in the JVM heap?** → **A:** Most objects die young; collecting the small young gen often is cheap.
- **Q: What is a TLAB?** → **A:** Per-thread Eden buffer making `new` a lock-free O(1) bump.
- **Q: Is `System.gc()` guaranteed to collect?** → **A:** No, it's only a hint.
- **Q: Why was `finalize()` deprecated?** → **A:** Nondeterministic, resurrects objects, hides leaks; use try-with-resources.
- **Q: What's the default GC since Java 9?** → **A:** G1.
- **Q: What does the Java Memory Model govern?** → **A:** Visibility/ordering of writes across threads (happens-before), not GC.

## 21. Revision
A Java object is an 8+ byte heap block; references to it live on the thread stack (locals) or in fields/statics. The JVM reclaims unreachable objects automatically: the young gen (Eden + survivors) is collected frequently by cheap copying; survivors age and promote to the old gen, which is mark-sweep-compacted rarely. G1 is the default collector; ZGC/Shenandoah trim pause times. `System.gc()` is a hint, `finalize()` is deprecated (use try-with-resources/`Cleaner`). Roots = stacks, statics, JNI, classloaders; a precisely-known oop map lets the collector identify references exactly. Allocation is O(1) via TLAB bump-the-pointer. The Java Memory Model (JLS §17.4) separately governs cross-thread visibility via happens-before — it has nothing to do with GC. Before any JVM interview: be able to trace one object from `new` through allocation, use, unreachability, and reclamation.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Where are objects stored in Java?" | 8 Example / 9 Internal Working |
| "How does garbage collection work in the JVM?" | 9 Internal Working / 10 Time Complexity |
| "What are GC roots?" | 7 Formal Definition / 9 Internal Working |
| "Why is Java allocation cheap?" | 9 Internal Working / 10 Time Complexity |
| "What's the difference between minor and full GC?" | 9 Internal Working |
| "What happened to PermGen / `finalize()`?" | 8 Example / 9 Internal Working |
| "What is the Java Memory Model?" | 7 Formal Definition |
| "How do you diagnose a memory leak?" | 13 Interview Questions |
| "What is escape analysis?" | 14 Follow-Up Questions |
| "Which GC should you pick for a low-latency service?" | 12 Disadvantages / 16 Industry Usage |
