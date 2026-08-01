# Prototype and Object Pool Patterns

> **TL;DR**: The **Prototype** pattern creates new objects by *cloning an existing instance* (a prototype) instead of calling constructors, and the **Object Pool** pattern *reuses* a set of pre-created, expensive objects instead of constructing and destroying them per request — both exist to sidestep expensive or unwieldy construction, and both trade memory/complexity for latency.

## 1. Why Does This Exist?
Object creation isn't always cheap or convenient:
- **Prototype** exists when `new` is *undesirable*: constructing an object may be expensive (loading a large config, resolving a graph of dependencies, initializing native resources) or awkward (a deeply nested composite where reconstruction requires repeating every sub-step). When you already *have* an instance with the exact configuration you need, **cloning it** is dramatically cheaper and guarantees an identical baseline. Prototype also solves *generic* creation: a framework that must create "objects like this one" without knowing their concrete class can call `clone()` on a prototype it was handed — no reflection, no factory per type.
- **Object Pool** exists when objects are *expensive to create but cheap to reset* and *frequently needed* — e.g., database connections, TCP sockets, thread-pool workers, large buffers, ECS game entities. Constructing a new connection per request costs a handshake (TCP + TLS + auth); destroying it afterwards wastes that cost. A pool keeps a fixed set of live objects, hands them out on request, and recycles them, so steady-state latency drops by orders of magnitude.

Both patterns are responses to one root fact: **construction cost is not free**, and for some resource types it dominates the request path. Prototype amortizes *configuration*; Object Pool amortizes *allocation + initialization*.

## 2. How Does It Work?
**Prototype**:
1. Define a `Cloneable`/`copy()` interface on the product (`abstract Prototype { Prototype clone(); }`).
2. Each concrete class implements `clone()` — either **shallow** (share references) or **deep** (copy the object graph).
3. The client keeps a *prototype instance* and produces new objects via `prototype.clone()`, never via `new Concrete()`.
4. The prototype can be a *registry*: a map of key → prototype, so clients clone by name ("document:report" → clone) without any concrete type knowledge.

```
Prototype ── clone(): Prototype (abstract)
   ▲
ConcreteA.clone() → new ConcreteA(this-copy)     ConcreteB.clone() → new ConcreteB(this-copy)
   Client: Object x = registry.get("A").clone();   // no concrete class named
```

**Object Pool**:
1. Pre-create (lazy-fill or eager) a bounded set of objects at startup.
2. `acquire()`: if an idle object exists, remove it from the idle list and hand it out; else block, wait, create (up to a max), or throw.
3. The caller uses the object.
4. `release()`: reset the object to a clean state and return it to the pool.
5. Concurrency: `ConcurrentLinkedQueue`/`ArrayBlockingQueue` + `Semaphore` (or `commons-pool2`'s `GenericObjectPool`) manage acquire/release atomically.

```
Pool [ o1, o2, o3 ]   acquire() → remove o2, hand to Thread A
                     Thread A finishes → release(o2) → reset o2 → put back
```

## 3. When Is It Used?
- **Prototype**: document/image templates (duplicate a "report" prototype); game entities (spawn enemies by cloning a template); complex object graphs where reconstruction repeats expensive steps; generic frameworks that must copy objects without knowing concrete types (a `copyOf` utility over `Cloneable`); caches of configured objects.
- **Object Pool**: database connection pools (HikariCP, C3P0, commons-dbcp); thread pools (`Executors.newFixedThreadPool` is a *thread* pool); HTTP/socket connection pools (Apache HttpClient, OkHttp); large buffer pools (Netty's `ByteBuf` pool); object pools in game engines (bullet pools — reuse projectiles); expensive client objects in microservices.
- **In interviews**: "copying expensive objects" → Prototype; "frequently-created expensive resources" → Object Pool; "object explosion in a game loop" → both.

## 4. Why Wasn't Another Approach Chosen?
**For Prototype:**
- **Plain construction (`new` + configure)**: simplest, but repeats expensive setup and can't clone generic types without knowing concrete classes. Chosen when objects are cheap; rejected when configuration/construction is the cost.
- **Factory Method**: factory returns `new` objects — no copy; rejected when the *state* (not the type) is what should be preserved. Factory says "make a fresh one of this type"; Prototype says "make a copy of *this* one."
- **Serialization round-trip** (serialize + deserialize to clone): works for deep copies but is slow (reflection, I/O) and fragile (transient fields, serialVersionUID). Chosen only when deep-copy semantics are critical and clone() is unwieldy.
- **Copy constructors**: a constructor taking a source instance is a *manual* deep copy — it's the language-level cousin of Prototype; but it requires the caller to know the concrete type and can't be invoked through an interface (`new X(other)` names `X`). Prototype's `clone()` is the polymorphic form (call through `Prototype`).
- **Structural sharing / copy-on-write**: an alternative that *avoids* copying by sharing immutable parts — chosen when most of the graph is immutable and only leaves change (persistent data structures). More complex; rejected when you genuinely need independent copies.

**For Object Pool:**
- **Construct per request, discard after**: simplest, but pays construction+teardown cost per request — the exact thing pools avoid; rejected for high-frequency, high-cost resources.
- **Caching (create and keep one long-lived instance)**: a single cached connection is *shared mutable state* — threads can't use it concurrently. A pool is the concurrency-safe middle ground (many reusable instances, handed out exclusively).
- **Thread-local objects**: avoids pooling *and* locking — each thread owns one instance; works when the resource is per-thread by nature (e.g., a reusable buffer in a worker thread). Rejected for *shared* resources (connections must be used by different threads over time).
- **Lazy creation without pooling (just `new` on demand)**: still pays construction cost each time; pools trade memory (keep-alive) for that cost.
- **Just-in-time / async creation**: for very low-frequency or long-lived resources, construction cost is negligible and a pool's memory is wasted — so pools are rejected when creation is rare.

## 5. Intuition
**Prototype**: a **master key** or a **cookie-cutter**. You don't re-negotiate the cookie recipe every time you need a cookie — you stamp out copies of the *same* shape from the one mold. If you need a "report" with all its standard sections, formatting, and headers, you clone the *template report* you already have; cloning is stamping, reconstructing is re-baking from scratch.

**Object Pool**: a **valet parking lot** vs **building a new car per customer**. Paying for a brand-new car each time someone needs to drive is absurd — you keep a *fleet* of ready cars and hand one out on demand, then take it back, wipe the GPS history (reset), and hand it to the next driver. The fleet is the pool; the reset is `release()`. Database connections are exactly these "cars" — expensive to manufacture (TLS handshake), cheap to reuse.

## 6. Real-World Analogy
- **Prototype**: a **printer template for wedding invitations**. Once you've designed the invitation once (expensive: fonts, layout, names), you don't re-design each copy — you print duplicates from the master. In software, the "master" is the prototype instance; printing is `clone()`; a registry of templates (invite types) lets you clone by name without knowing the designer (concrete class).
- **Object Pool**: a **public swimming pool** (fittingly). The pool pre-heats a fixed amount of water (the pooled resource). Swimmers (threads) enter/leave the water (acquire/release); no one is expected to boil their own private water per swim. If everyone had to heat private water (construct a connection) each swim, the morning rush would be a disaster.

## 7. Formal Definition
> **Prototype**: Specify the kinds of objects to create using a **prototypical instance**, and create new objects by **copying this prototype**. (GoF, p. 117)
>
> **Object Pool** (not in the original GoF catalog; a later creational pattern): A pool maintains a collection of initialized objects that are **acquired, used, and released** instead of constructed and destroyed; the pool manages the lifecycle so clients reuse expensive resources. (Documented in POSA; e.g., Java's `commons-pool2` `GenericObjectPool`.)

## 8. Example
**Prototype** — cloning a `Report` template:
```java
abstract class Report implements Cloneable {
    abstract String type();
    public Report copy() { return (Report) clone(); }   // shallow clone via Cloneable
}
class FinancialReport extends Report {
    private final String templateName;
    FinancialReport(String name) { this.templateName = name; }
    String type() { return "FINANCIAL"; }
    public FinancialReport copy() { return (FinancialReport) super.clone(); }
}
// registry of prototypes
Map<String, Report> registry = Map.of("annual", new FinancialReport("annual-v2"));
Report r = registry.get("annual").copy();     // O(1) copy — no reconstruction
```
- A copy is created by *stamping* the existing instance — no re-loading of template data, no re-resolving of config. (Note: `super.clone()` is shallow; deep-copy graphs need manual deep cloning or serialization.)

**Object Pool** — a bounded connection pool:
```java
class ConnectionPool {
    private final ArrayBlockingQueue<Connection> idle;
    private final Semaphore permits;             // bounds total outstanding
    ConnectionPool(int max) {
        idle = new ArrayBlockingQueue<>(max);
        permits = new Semaphore(max);
        for (int i = 0; i < max; i++) idle.offer(new Connection("conn-" + i));
    }
    Connection acquire() throws InterruptedException {
        permits.acquire();                        // block if all in use
        Connection c = idle.poll();
        return (c != null) ? c : new Connection("extra");   // lazy growth up to... guarded
    }
    void release(Connection c) {
        c.reset();                                // clean state before reuse
        idle.offer(c);                            // return to pool
        permits.release();
    }
}
```

## 9. Internal Working
**Prototype internal flow:**
1. Client selects a prototype (direct reference or via a registry keyed by name).
2. Client calls `prototype.copy()` — **dynamic dispatch** resolves to the concrete class's clone.
3. JVM allocates a new object and copies the instance fields (shallow). For deep copies, the concrete `copy()` recursively clones referenced objects (or uses serialization/manual traversal).
4. The returned object is a *new, independent instance* with the prototype's baseline state — callers can mutate it without affecting the prototype (if the copy is deep enough; shallow copies share mutable references — the classic shallow-vs-deep trap).
5. The prototype remains pristine, ready to spawn the next copy.

**Object Pool internal flow:**
1. **Bootstrap**: pool pre-creates (lazy or eager) up to `maxIdle` objects; a `Semaphore`/counter tracks the outstanding budget.
2. **Acquire**: take a permit (block if exhausted), pop an idle object (create one if the pool allows growth below `maxTotal`).
3. **Use**: caller works with the exclusively-held object.
4. **Release**: caller returns it; pool *resets* it to a clean state (the crucial step — a connection with a stale transaction/state is a correctness bug), then pushes it back to idle and releases the permit.
5. **Destroy/reap**: a maintenance thread (e.g., HikariCP's housekeeper) removes idle objects older than `idleTimeout`, keeping the pool fresh and bounded.

Concurrency correctness comes from the queue + semaphore + the "reset before reuse" contract. Leaks (unreleased connections) eventually exhaust the pool — hence "connection leak" bugs and `close()` semantics in practice.

## 10. Time Complexity
- **Prototype `copy()`**: O(S) where S = size of the object graph (shallow = O(1) fields copy; deep = O(G) graph size). Compare to reconstruction O(C) where C includes expensive setup — Prototype wins when C ≫ G. A registry lookup is O(1).
- **Object Pool `acquire()`/`release()`**: O(1) amortized (queue pop/push + semaphore). The *real* win: steady-state creation cost drops from O(construction) per request to O(1) reuse — construction happens only at bootstrap/refill. Worst case (pool exhausted, must wait): blocking, latency-bound by the semaphore.
- **Memory**: the pool holds up to `maxTotal` objects alive — O(maxTotal × size). Prototype holds the prototype(s) alive: O(prototypes).
- **Amortization rule of thumb**: pool if creation cost > (reset cost + reuse cost) and request rate is high; otherwise pooling wastes memory.

## 11. Advantages
**Prototype:**
- Fast creation by copying — avoids expensive construction/setup.
- Generic, type-agnostic creation through the `Prototype` interface (clone via interface, not `new Concrete`).
- Cleaner alternative to reconstruction for complex graphs.
- Hides the concrete class from the caller (a registry of prototypes).
**Object Pool:**
- Massive latency win for expensive, high-frequency resources (connections, buffers, threads).
- Bounds resource usage (`maxTotal`) — prevents uncontrolled object explosion.
- Reuse reduces GC pressure (fewer allocations) and OS-level handshake costs.
- Settable idle/validation policies for production tuning.

## 12. Disadvantages
**Prototype:**
- **Shallow-vs-deep copy trap**: `clone()` is shallow by default; deep copies are manual and error-prone (nested mutable refs leak shared state).
- `Cloneable` is a *marker* interface — the JVM's `clone()` is a low-level field copy; misuse (calling `clone()` on non-`Cloneable`) throws `CloneNotSupportedException` at runtime.
- Copying objects with non-cloneable internals (file handles, sockets, native resources) is meaningless or dangerous — those should be *constructed*, not cloned.
- Circular references break naive deep-copy implementations.
**Object Pool:**
- **Reset correctness**: every resource must be reliably reset before reuse; a missed reset leaks state between users (a serious data-leak bug).
- **Leaks**: clients that forget `release()` silently exhaust the pool — "connection leak" is a classic production incident.
- **Stale resources**: idle objects can die (server closes an idle connection); pools need validation/eviction — added complexity.
- **Memory overhead**: pooled objects are held alive even when unused (`maxIdle` memory).
- **Fragility**: blocking `acquire()` under load creates latency spikes; tuning (size, timeout, eviction) is non-trivial.
- Not in the original GoF catalog — no canonical shape, so implementations vary (a maintenance/consistency concern).

## 13. Interview Questions
1. **Q: What is the Prototype pattern?** A: Create new objects by *copying an existing prototype instance* (`clone()`) instead of constructing them, so that expensive construction/configuration is done once and copied many times, and clients can create "objects like this one" without knowing the concrete class.
2. **Q: What problem does Object Pool solve?** A: High-frequency need for resources that are expensive to construct (DB connections, sockets, threads, buffers) — it pre-creates a bounded set, hands them out exclusively (acquire), and recycles them (release) so steady-state construction cost drops to O(1).
3. **Q: Prototype vs Factory Method?** A: Factory Method constructs a *fresh* object of a chosen concrete type (one step, names the type via subclass). Prototype *copies* an existing object's *state* (type + configuration) and works through the interface — the emphasis is state preservation, not type selection.
4. **Q: Shallow copy vs deep copy — explain the danger.** A: A shallow copy shares references to nested mutable objects; mutating a nested object through the copy also mutates the prototype (shared state bug). A deep copy clones the whole graph (independent). `Object.clone()` is shallow; deep copying is manual — the #1 Prototype footgun.
5. **Q: Why is `Cloneable` considered a flawed API? (Tricky)** A: `Cloneable` is an *empty marker* with no `clone()` declared on it — `clone()` is on `Object`, throws `CloneNotSupportedException` unless the class opts in, and its behavior (shallow field copy) bypasses constructors, so subclasses can silently break cloning. Effective Java item 13 recommends a *copy constructor or static copy factory* instead of `Cloneable`.
6. **Q: How would you implement a deep copy in Java?** A: Options: (1) manual recursion over the object graph; (2) serialization round-trip (implements `Serializable` → serialize to bytes → deserialize) — slow but automatic; (3) copy constructors on each class; (4) libraries (Apache Commons `SerializationUtils.clone`, Jackson `convertValue`). Choose manual/copy-constructors when performance matters; serialization when correctness-by-simplicity wins.
7. **Q: When would you use Object Pool over just creating objects? (Production)** A: When creation is *expensive* (network handshake, TLS, large buffers) AND the object is *frequently needed* AND it can be *reset* for reuse. If creation is cheap or rare, pooling wastes memory and adds complexity. Database connections and HTTP keep-alive connections are the canonical examples.
8. **Q: What is the connection-leak bug and how do pools make it worse?** A: A leak = the client fails to `release()`/`close()` a pooled resource. The pool silently runs out of permits, and acquire() blocks or fails — turning a slow bug into an outage. Production mitigations: try-with-resources, lease timeouts (force-reclaim after X minutes), and leak-detection (HikariCP `leakDetectionThreshold`).
9. **Q: How do you reset a pooled object correctly? (Tricky)** A: Before returning to the pool: roll back any transaction, clear buffers/streams, reset timeouts, close nested resources, and validate the object is still usable (e.g., `isValid()` / ping). Reset must be *idempotent* and *fast* — it runs on every release, so it can't be a heavyweight operation.
10. **Q: What happens when the pool is exhausted?** A: Depends on policy: block until a permit frees (bounded wait — most pools), create beyond max up to `maxTotal` (overflow, still bounded), return an error/timeout, or throw. Good pools distinguish `maxIdle` (idle-held) from `maxTotal` (all-time outstanding) and let you set acquire timeouts.
11. **Q: Prototype registry — what is it and why?** A: A map of key → prototype instance so clients clone "by name" (`registry.get("annual-report").copy()`) without naming concrete classes. It combines Prototype's copy semantics with Factory-like lookup; useful for document/image template systems.
12. **Q: Which JDK/framework classes use Object Pool?** A: `ThreadPoolExecutor` (thread pool — threads are pooled workers), `commons-pool2`'s `GenericObjectPool` (generic pooling), HikariCP/C3P0/dbcp (connection pools), Netty `ByteBufPool`, Apache HttpClient `PoolingHttpClientConnectionManager`, Go's `sync.Pool`.
13. **Q: Is Object Pool a GoF pattern? (Tricky)** A: No — it's not among the 23 GoF patterns. It was cataloged later (e.g., Pattern-Oriented Software Architecture / concurrent-object-pool literature; JDK `Executors` and commons-pool2 codify it). Saying this precisely shows catalog fluency.
14. **Q: Prototype + Object Pool together? (Scenario)** A: A game spawns 1000 bullet objects: the pool holds e.g. 50 bullet *prototypes*? No — the pool holds *pre-created bullets* and `acquire()` returns one (pool); if each needs a config baseline, the pool *stamps* bullets from a prototype first (prototype). Both reduce cost: prototype avoids config-cost, pool avoids allocation/GC-cost. Common in ECS/game engines (object pools with prototype templates).
15. **Q: What does "lazy growth" in a pool mean?** A: Start with a small `minIdle`, create more on demand up to `maxTotal`, and let the evictor shrink back — avoids pre-paying for a large fleet while bounding peak usage. Contrast with eager pools that pre-create everything at bootstrap.
16. **Q: How do you handle pool eviction / stale objects? (Production)** A: A background housekeeper periodically tests idle objects (a `SELECT 1` for DB connections, TCP ping) and discards failures; enforces `idleTimeout`/`maxLifetime`. HikariCP's default `maxLifetime` (30 min) avoids stale-server-side connections.
17. **Q: Prototype for immutable objects — good or bad?** A: Mostly unnecessary — immutable objects can be safely *shared* rather than copied (no one can mutate a shared instance). Cloning immutable objects wastes memory; the JVM's string/cached-instance sharing already does "copying" via references. Prototype shines for *mutable* configured objects.
18. **Q: Copy constructor vs clone() — which is better? (Tricky)** A: Effective Java prefers *copy constructors* (`public Foo(Foo other)`) and *copy factories* (`Foo.copyOf(other)`) because they're safe with inheritance and final fields, and don't depend on the `Cloneable` marker. `clone()` is the pattern's language mechanism but is widely considered an API mistake; many teams implement the *pattern* with copy constructors.
19. **Q: When is Prototype faster than construction? Give numbers.** A: If a config load costs 500 ms (parsing, network) but copying an in-memory graph costs 5 ms, cloning is ~100× faster. The pattern pays the 500 ms once at prototype creation and stamps copies thereafter. This is the "cost ∝ construction vs copy" argument.
20. **Q: Design a spawner for a game with heavy enemy objects. (Scenario)** A: Keep an `EnemyRegistry` of enemy prototypes (per type); for a large wave, an `EnemyPool` pre-creates bullets/enemies and `acquire()` returns a reset instance; new types = register a prototype. Prototype handles configuration + type-agnostic creation; pool handles allocation/GC pressure. State the reset contract and bounded `maxTotal`.

## 14. Follow-Up Questions
1. **Q: What is a circular-reference deep copy?** A: A graph where A→B and B→A; a naive recursive deep copy infinitely recurses. Fix: track an identity map (original → copy) so a node already copied is returned from the map (topological memoization).
2. **Q: Why is `Object.clone()` shallow and how does that cause bugs with `final` fields?** A: `clone()` copies field values; for a `final` reference field it copies the reference (shared). Also, you can't set a *new* value of a `final` field in a normal constructor path after clone — another reason copy constructors are preferred.
3. **Q: What's the difference between `maxIdle`, `minIdle`, and `maxTotal` in commons-pool2?** A: `maxIdle` = how many idle objects the pool keeps around; `minIdle` = how many it maintains even when idle; `maxTotal` = the hard cap on all objects (borrowed + idle) at once. Tuning them is the pool-sizing interview question.
4. **Q: How does GC interact with pooling?** A: Pooled objects are *referenced by the pool*, so they're never GC'd while pooled (that's the memory cost). The win is fewer allocations on the hot path (less GC pressure) — you trade heap retention for allocation rate.
5. **Q: When is a pool actively harmful?** A: When the pooled resource is cheap to create (object explosion is a myth), when it can't be safely reset, when demand is sparse (pool idles and leaks memory), or when the "reset" is more expensive than construction. Also harmful when it becomes a hidden shared-mutable-state bug vector.

## 15. Coding Example
```java
// Prototype: type-agnostic cloning via interface + registry
interface Document extends Cloneable {
    Document copy();
    String describe();
}
class Report implements Document {
    private String title;
    Report(String t) { this.title = t; }
    public Document copy() {
        try { return (Document) super.clone(); } catch (CloneNotSupportedException e) { throw new AssertionError(e); }
    }
    public String describe() { return "Report(" + title + ")"; }
}
// Client — knows only Document:
Document proto = new Report("Annual");
Document d2 = proto.copy();          // no concrete class named
System.out.println(d2.describe());   // Report(Annual)
```
```java
// Object Pool: generic, bounded, thread-safe (skeleton)
import java.util.concurrent.*;

class Expensive { public void reset() { } }

class GenericPool<T> {
    private final BlockingQueue<T> idle = new LinkedBlockingQueue<>();
    private final Semaphore permits;
    private final Supplier<T> factory;
    private final Consumer<T> reseter;
    GenericPool(int max, Supplier<T> f, Consumer<T> r) { permits = new Semaphore(max); factory = f; reseter = r; }
    public T acquire() throws InterruptedException {
        permits.acquire();
        T t = idle.poll();
        return t != null ? t : factory.get();
    }
    public void release(T t) { reseter.accept(t); idle.offer(t); permits.release(); }
}
// Usage
GenericPool<Expensive> pool = new GenericPool<>(10, Expensive::new, Expensive::reset);
Expensive e = pool.acquire();
try { /* use e */ } finally { pool.release(e); }   // never leak
```
```python
# Python Object Pool
from queue import Queue
from threading import Semaphore

class Connection:
    def __init__(self, name): self.name = name; self.open = True
    def reset(self): pass

class ConnectionPool:
    def __init__(self, size: int):
        self._idle: Queue = Queue()
        self._permits = Semaphore(size)
        for i in range(size): self._idle.put(Connection(f"conn-{i}"))
    def acquire(self):
        self._permits.acquire()
        conn = self._idle.get()
        return conn
    def release(self, conn: Connection):
        conn.reset()
        self._idle.put(conn)
        self._permits.release()
```
```cpp
// C++ Prototype via clone idiom
#include <memory>
#include <string>
#include <iostream>

struct Document {
    virtual ~Document() = default;
    virtual std::unique_ptr<Document> copy() const = 0;   // the "clone" 
    virtual std::string describe() const = 0;
};
struct Report : Document {
    std::string title;
    explicit Report(std::string t) : title(std::move(t)) {}
    std::unique_ptr<Document> copy() const override { return std::make_unique<Report>(*this); }
    std::string describe() const override { return "Report(" + title + ")"; }
};
// Client: generic copy through interface
void duplicate(const Document& d) { auto copy = d.copy(); std::cout << copy->describe() << "\n"; }
// int main() { Report r("Annual"); duplicate(r); }
```

## 16. Industry Usage
- **Prototype**: Java `Object.clone()` / `Cloneable` (though discouraged); Guava's `Copyable`; game engines (Unity prefabs — a prefab IS a prototype you instantiate); document systems (design templates); `String`'s copy-on-write in some runtimes; JavaScript's `Object.create(proto)` (the language's native prototype mechanism); config-template systems (clone a base config, override one field).
- **Object Pool**: HikariCP (the default Spring Boot connection pool), Apache DBCP/C3P0, commons-pool2, Netty `ByteBuf` pool, Apache HttpClient pooling manager, `ThreadPoolExecutor` (thread pool), Go's `sync.Pool`, PostgreSQL connection pools (pgbouncer is a *proxy* pool), Redis/Memcached client pools.
- **Cloud/backend**: connection pools are mandatory in every service with a database — HikariCP tuning (maximumPoolSize, idleTimeout, leakDetectionThreshold) is a standard production question.
- **Interviews**: "copy expensive objects" → Prototype (with the deep/shallow trap), "frequent expensive connections" → Object Pool (with leak/reset/eviction traps). Both appear in LLD rounds for caches, spawners, and resource-manager designs.

## 17. References
- **Gamma et al., *Design Patterns* — "Prototype" (p. 117)**: canonical prototype definition, shallow vs deep copy discussion, prototype manager.
- **Joshua Bloch, *Effective Java* (3rd ed.), Item 13**: "Override clone judiciously" — the critique of `Cloneable` and recommendation of copy constructors/factories.
- **Buschmann et al., *Pattern-Oriented Software Architecture, Volume 1* (POSA)** — the "Object Pool" family of resource-management patterns (later catalog, not GoF).
- **Oracle Docs: `Object.clone()`, `Cloneable`, `java.util.concurrent` (Semaphore, BlockingQueue)** — https://docs.oracle.com/javase/8/docs/api/
- **Apache Commons Pool 2 (`GenericObjectPool`) docs** — https://commons.apache.org/proper/commons-pool/
- **HikariCP GitHub/wiki: pool sizing, leak detection, maxLifetime** — https://github.com/brettwooldridge/HikariCP
- **refactoring.guru — "Prototype"** — modern diagrams and examples.
- **Baeldung — "Object Pool Pattern in Java"** — tutorial using commons-pool2.

## 18. Cheat Sheet
- **Prototype**: clone an existing instance instead of `new` — avoid expensive construction; generic type-agnostic creation via a `copy()` interface.
- **Object Pool** (NOT GoF): reuse a bounded set of expensive resources; `acquire()` → use → `release()` (reset first).
- Shallow copy shares mutable refs (bug source); deep copy is manual or serialization-based; `Cloneable`+`clone()` is flawed — prefer copy constructors/factories.
- Pool correctness: **reset on release**, never leak (finally/try-with-resources), validate + evict stale idle objects.
- Pool exhaustion → block / overflow / timeout depending on policy; distinguish `maxIdle` vs `maxTotal`.
- Use a pool when: creation expensive + frequent + resettable. Otherwise memory waste.
- Registry + prototype = clone by key without concrete classes.
- Examples: HikariCP (pool), ThreadPoolExecutor (pool), Unity prefabs / `Object.create` (prototype), Netty ByteBuf (pool).
- Prototype fast when construction ≫ copy; pool fast because steady-state is O(1) reuse.
- Watch: circular refs (identity map), immutable objects (share, don't clone), final fields in clone.

## 19. Quiz
1. Prototype creates objects by: a) calling constructors b) copying a prototype c) factory d) reflection → **b**
2. `Object.clone()` performs a: a) deep copy b) shallow copy c) serialized copy d) no copy → **b**
3. Which is the main Prototype footgun? a) speed b) shallow copies sharing mutable state c) memory d) serialization → **b**
4. Effective Java recommends ___ over `clone()`. a) reflection b) copy constructors/copy factories c) serialization d) setters → **b**
5. Object Pool is: a) a GoF pattern b) a later resource-management pattern c) an anti-pattern d) a JDK class → **b**
6. What MUST happen before a pooled object is reused? a) clone it b) reset it c) log it d) serialize it → **b**
7. "Connection leak" means: a) too many connections b) clients fail to release, exhausting the pool c) network error d) memory leak → **b**
8. Which class is an object-pool implementation? a) `StringBuilder` b) `ThreadPoolExecutor` c) `HashMap` d) `Cloneable` → **b**
9. When is pooling harmful? a) cheap-to-create resources b) high-frequency DB connections c) expensive TCP connections d) big buffers → **a**
10. A prototype registry lets you: a) construct by name b) clone by key without concrete classes c) pool objects d) serialize → **b**

## 20. Flashcards
- **Q: Prototype intent?** → **A:** Create objects by cloning a prototype instead of constructing them (avoid expensive config; generic type-agnostic copy).
- **Q: Object Pool intent?** → **A:** Reuse a bounded set of expensive, resettable objects via acquire()/release() to amortize construction cost.
- **Q: Shallow vs deep copy?** → **A:** Shallow shares nested mutable refs (bug); deep copies the whole graph (independent).
- **Q: Best clone approach in Java?** → **A:** Copy constructors / copy factories (Effective Java item 13); `Cloneable.clone()` is flawed.
- **Q: Correct pool release?** → **A:** Reset the object, return it to the pool, release the permit; use try-with-resources/finally to avoid leaks.
- **Q: Is Object Pool in GoF?** → **A:** No — later catalog (POSA / commons-pool2); not one of the 23.
- **Q: When to use a pool?** → **A:** Expensive creation + high frequency + safe reset; otherwise pooling wastes memory.
- **Q: Real-world pools?** → **A:** HikariCP, ThreadPoolExecutor, Netty ByteBuf pool, Apache HttpClient pool, Go sync.Pool.

## 21. Revision
**Prototype** clones an existing instance via a `copy()`/`clone()` method — sidestepping expensive construction and enabling generic creation through an interface (a registry lets clients clone "by key" without concrete classes). Footguns: `Object.clone()` is *shallow* (shared mutable state), `Cloneable` is a flawed marker API, deep copies need manual recursion/serialization, circular references need an identity map, and immutable objects should be *shared*, not cloned. **Object Pool** (not GoF — a later resource-management pattern) pre-creates a bounded set of expensive objects; `acquire()` hands out an exclusive instance, `release()` resets it and returns it; a semaphore/queue bounds and serializes access. Correctness demands: **reset before reuse**, guaranteed release (try-with-resources — connection leaks exhaust the pool), and eviction of stale idle objects (HikariCP's `maxLifetime`, `leakDetectionThreshold`). Use a pool when creation is expensive + frequent + the object is resettable; otherwise it wastes memory. Real systems: HikariCP, `ThreadPoolExecutor`, Netty `ByteBuf`, Apache HttpClient, Go `sync.Pool`; prototypes: Unity prefabs, JavaScript `Object.create`, config/template systems.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Prototype pattern?" | 2 How / 7 Formal Definition |
| "Shallow vs deep copy — dangers?" | 9 Internal Working / 13 Q4 / 14 Q1 |
| "Why is `Cloneable.clone()` flawed?" | 13 Q5 / 14 Q2 / 17 References |
| "Copy constructor vs clone?" | 13 Q18 / 14 Q2 |
| "What is Object Pool and when to use it?" | 13 Q2 / 13 Q7 |
| "How do you prevent connection leaks?" | 13 Q8 / 13 Q9 |
| "How do you reset a pooled object?" | 13 Q9 / 18 Cheat Sheet |
| "Is Object Pool a GoF pattern?" | 13 Q13 |
| "Pool sizing: maxIdle vs maxTotal?" | 14 Q3 / 13 Q10 |
| "Prototype + Pool in a game spawner?" | 13 Q14 / 13 Q20 |
