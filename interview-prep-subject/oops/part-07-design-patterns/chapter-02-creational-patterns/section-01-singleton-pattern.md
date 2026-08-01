# Singleton Pattern

> **TL;DR**: The Singleton pattern guarantees a class has **exactly one instance** and provides a **global point of access** to it — it exists for truly single resources (config, connection pools, logging) where multiple instances would corrupt state or waste resources, and it must be implemented thread-safely (double-checked locking, holder class, or enum).

## 1. Why Does This Exist?
Some resources are conceptually **one-of-a-kind**: an application's global configuration, a logging facility, a database connection pool, a thread pool, a device controller (a printer), or a window manager. If you allow arbitrary `new Config()` calls, you get multiple, divergent copies of a "single" reality — two configs, two connection pools — each consuming resources and each capable of holding *different* values for the same logical setting. The Singleton pattern exists to enforce the invariant **"at most one instance exists, and everyone can reach it"** from inside the class itself, so the single-ness cannot be violated by any caller, however careless.

It also exists for **coordination**: when multiple modules must share *one* object (one logging file, one cache, one counter), a single shared instance is the coordination mechanism. Without Singleton, engineers reach for a static class — but static methods carry hidden global state and cannot be swapped/tested; the Singleton keeps the object *an object* (inheritance, interfaces, lazy init, substitution possible) while enforcing uniqueness.

## 2. How Does It Work?
The mechanism has three parts:
1. **Private constructor** — nobody outside can call `new Singleton()`.
2. **A static field** to hold the single instance.
3. **A static `getInstance()` accessor** that creates the instance on first call (lazy) or eagerly, and returns the same instance every time.

Because the constructor is private, all creation funnels through `getInstance()`, which can enforce "create once, return forever". Thread-safety is added at the creation step (the only place two threads could race to create two instances). There are four production-grade Java implementations, each with different thread-safety/simplicity trade-offs:

| Implementation | Lazy? | Thread-safe? | Notes |
|---|---|---|---|
| Eager `static final` | No | Yes (class-loading) | Simplest; instance created even if unused |
| Synchronized method | Yes | Yes | `synchronized` on every call — costly |
| Double-checked locking | Yes | Yes (needs `volatile`) | Fast reads after init; subtle but correct with `volatile` |
| Static inner holder class | Yes | Yes (class-loading) | Best of lazy + no explicit sync |
| Enum singleton | Lazy-ish (on first use) | Yes | Best: serialization-safe, reflection-proof (Effective Java) |

## 3. When Is It Used?
- **Configuration/registry**: a single `Config` or service registry shared app-wide.
- **Resource pooling**: one connection pool, one thread pool, one cache — where a second instance would duplicate scarce resources.
- **Logging**: a single logger writing to one sink.
- **Hardware/OS access**: one controller for a device that physically has one instance (printer spool, display, keyboard).
- **Caching**: a single cache so every module reads the same cached value.
- **Framework internals**: Spring's beans are singletons *by default* (`scope="singleton"`) — the container guarantees one instance per bean name (implemented via its own registry, not the GoF pattern, but same intent).
- **Counter/sequence**: a global unique-ID generator (though `AtomicLong` + static is simpler here).

## 4. Why Wasn't Another Approach Chosen?
- **Static class (all static methods)**: rejected for most cases because static state is *global mutable state* that can't be interface-substituted, is hard to unit-test (can't mock), and encourages tight coupling. Singleton keeps an *object* you can pass around and mock.
- **A global variable / `public static final` field**: rejected because it doesn't guarantee *lazy* creation and — critically — doesn't prevent anyone from making *another* instance via the constructor. Singleton seals the constructor.
- **Passing a shared instance through constructors (dependency injection)**: the modern alternative — you *construct* the single instance once (in composition root) and inject it everywhere. Singleton is chosen when the DI container is absent, when the object is a truly infrastructure-level facility, or when frameworks (Spring) do the single-ing for you. DI is *preferred* when testability matters most.
- **Double instance protection via factories**: a factory can return a shared instance — that's fine, but the Singleton *embeds* the single-ness in the class itself; the factory approach requires the caller to cooperate. Singleton is stronger (enforced).
- **Thread-local instance**: for "one per thread" resources — that's a *different* requirement (ThreadLocal), not a singleton.

## 5. Intuition
A singleton is **the single public water fountain in a building**. The architect doesn't install a fountain in every office — there is exactly one, everyone knows where it is (the global access point), and building a second fountain is physically impossible because there's no plumbing for it (the private constructor). Everyone drinks from the *same* source, so there's one place to maintain, one filter to change (one config to update), and no risk of two fountains showing different water temperatures.

The deeper intuition: **enforce the invariant at the class boundary, not by discipline.** Instead of *asking* everyone to share one instance (a convention that someone will break), the class *makes it impossible* to have two. That's the OO principle of *encapsulating an invariant*.

## 6. Real-World Analogy
A **country's central bank**. There is exactly one central bank (monetary authority), it is globally known (everyone can reach it), it's created lazily only when the country forms (or eagerly at boot), and creating a second "central bank" would be catastrophic (two currencies, two interest rates). All banks (modules) must go through the central bank for monetary operations — the global access point. Now imagine a buggy implementation where two "central banks" could exist: that's exactly the failure the pattern prevents.

## 7. Formal Definition
> The Singleton pattern ensures a class has **only one instance**, and provides a **global point of access** to it. It is implemented by (1) making the constructor private, (2) providing a static method that returns the instance, and (3) ensuring the instance is created exactly once, thread-safely, either eagerly or on first use.

— Gang of Four, *Design Patterns*, p. 127.

A consequence per GoF: the Singleton class itself is both the *factory* (it creates its own instance) and the *owner* (it holds it in a static field). This conflation is precisely what makes Singleton criticized in modern practice (see Disadvantages).

## 8. Example
A **global application config**:
```java
public class AppConfig {
    private static AppConfig instance;
    private final String dbUrl;
    private AppConfig(String dbUrl) { this.dbUrl = dbUrl; }        // private!
    public static synchronized AppConfig getInstance() {           // lazy + thread-safe
        if (instance == null) instance = new AppConfig("jdbc:mysql://prod:3306/app");
        return instance;
    }
    public String dbUrl() { return dbUrl; }
}
```
- **Call 1** (`Thread A` and `Thread B` simultaneously): with the `synchronized` method, only one thread enters; it creates the instance; the second waits, then sees `instance != null` and returns the same object. Exactly one `AppConfig` exists.
- **Call 2..N** (any thread): returns the same instance in O(1) — but note the `synchronized` costs a lock acquisition every call (that's why double-checked locking exists).

## 9. Internal Working (with Thread-Safety Analysis)
**The naive version is broken** — this is the #1 interview trap:
```java
public static AppConfig getInstance() {          // NOT thread-safe!
    if (instance == null)                        // T1 and T2 both pass this check
        instance = new AppConfig(...);           // → two instances created
    return instance;
}
```
Two threads can both see `instance == null` and both construct — yielding two instances and a torn publication.

**Fix 1 — synchronized method**: serialize the whole check-and-create. Cost: every subsequent call pays lock overhead.
**Fix 2 — double-checked locking (DCL)**:
```java
private static volatile AppConfig instance;      // volatile is mandatory!
public static AppConfig getInstance() {
    if (instance == null) {                      // fast path (no lock) — the "double check"
        synchronized (AppConfig.class) {
            if (instance == null)                // re-check inside lock
                instance = new AppConfig("..."); 
        }
    }
    return instance;
}
```
Why `volatile` is mandatory: `new AppConfig(...)` is not atomic — the JVM may (a) allocate memory, (b) invoke constructor, (c) assign the reference. Without `volatile`, the JMM allows *reordering* (c) before (b), so another thread may see a *partially-constructed* object (non-null reference, uninitialized fields). `volatile` gives the happens-before guarantee that the write to `instance` publishes a fully-constructed object to all readers. (Part 08 covers the JMM.)
**Fix 3 — inner-class holder (idiomatic, zero explicit locking)**:
```java
public class AppConfig {
    private AppConfig() {}
    private static class Holder { static final AppConfig INSTANCE = new AppConfig(); }
    public static AppConfig getInstance() { return Holder.INSTANCE; }
}
```
`Holder` is not loaded until `getInstance()` is first called (class-loading is lazy), and the JVM guarantees class initialization is thread-safe (only one thread initializes the class). Lazy + safe + fast.
**Fix 4 — enum (Effective Java recommendation)**:
```java
public enum AppConfig { INSTANCE;
    private final String dbUrl = "jdbc:mysql://prod:3306/app";
    public String dbUrl() { return dbUrl; }
}
```
The JVM guarantees each enum constant exists exactly once; it's automatically serialization-safe (reflection cannot create a second instance via the private constructor), and reading/writing enum fields is safe after class init. Downside: eager-ish (created at class load) and no superclass.

**Object lifecycle**: the single instance lives for the JVM's lifetime (or until class unloading in an app server — which is why Spring beans are singletons per-`ClassLoader`/container, not JVM-global).

## 10. Time Complexity
- **Eager / holder / enum `getInstance()`**: O(1) amortized; after class initialization it's a single field read.
- **Synchronized method `getInstance()`**: O(1) but with lock-acquisition cost on *every* call (a real hot-path tax; avoid for high-frequency access).
- **Double-checked locking `getInstance()`**: O(1) average — one volatile read on the hot path; the lock is taken only on the first call(s).
- **Memory**: one object, plus a `volatile` static reference (cache-line effects negligible at this scale).
- **Note**: singleton *does not* make application operations faster — it only avoids duplicate construction cost. If the singleton is expensive to build and rarely used, prefer lazy (holder/enum) so the cost is paid only on first use.

## 11. Advantages
- **Enforced uniqueness**: the invariant "one instance" is guaranteed by the class itself — callers can't violate it.
- **Global, convenient access**: any code can reach the instance without threading references through every constructor.
- **Lazy initialization**: with holder/enum implementations, the (possibly expensive) object is created only on first use.
- **Object benefits over static**: can implement interfaces, be extended (with care), be passed as an argument, and be mocked in tests (though mocking a private-constructor class needs frameworks).
- **Thread-safe by construction** (with the correct implementation): no torn reads, no duplicate instances.
- **Framework-friendly**: Spring's default bean scope *is* singleton — the pattern aligns with container conventions.

## 12. Disadvantages
- **Global mutable state**: the singleton is a hidden dependency; any code can read/write it, making behavior non-local and hard to reason about — the same sin as global variables.
- **Testability**: a private constructor + static accessor resists mocking and makes unit tests order-dependent (state leaks across tests).
- **Hidden coupling**: callers depend on the singleton class directly (`AppConfig.getInstance()`), violating Dependency Inversion; it's a *service locator*, which is widely considered an anti-pattern when overused.
- **Not extensible**: the GoF's own escape hatch (subclass the singleton) is clunky; with a private constructor you cannot subclass cleanly.
- **No lazy guarantee in enum form**: enum constants are initialized at class-load; for very heavy objects that may be wasteful.
- **Lifecycle/leaks in app servers**: JVM-global singletons can leak across application redeploys (classloader leaks) — a real production bug in web containers.
- **Concurrency pitfalls**: the naive implementation is broken; correct ones are subtle (the `volatile` requirement is non-obvious).

## 13. Interview Questions
1. **Q: What is the Singleton pattern and what problem does it solve?** A: It guarantees a class has exactly one instance and provides a global access point, by making the constructor private and funneling creation through a static method. It solves "one-of-a-kind resource" problems (config, pools, logging) where multiple instances would be wasteful or inconsistent.
2. **Q: Write a thread-safe lazy Singleton.** A: Three correct answers: (1) synchronized method; (2) double-checked locking with `volatile`; (3) static inner holder class. The *canonical* safe+lazy+fast one is the holder: `private static class Holder { static final X INSTANCE = new X(); }` — lazy because the class isn't loaded until first call, thread-safe because class initialization is JVM-guaranteed atomic.
3. **Q: Why must the field be `volatile` in double-checked locking?** A: Because object construction can be reordered — a thread could see a non-null reference to a partially-constructed object (memory allocated, constructor not finished). `volatile` adds the happens-before edge: the write that publishes the reference is ordered after the constructor completes, so readers see a fully-built instance.
4. **Q: What's the difference between eager and lazy initialization, and when is each right?** A: Eager (static final field) creates the instance at class-load: simpler and always safe, but pays the cost even if unused. Lazy (holder/enum/dcl) creates on first use: right when the singleton is expensive and possibly unused (rarely-used config loader). Rule: default to lazy via holder if cost matters, eager if it's cheap.
5. **Q: How does the enum singleton compare to the class singleton?** A: The enum (`enum AppConfig { INSTANCE }`) is simpler, automatically serialization-safe, and reflection-proof (can't call a second private constructor). Drawbacks: can't extend a class, eager-ish initialization, less familiar to teams. Effective Java (item 3) says the enum is the *best* way to write a singleton in Java.
6. **Q: Can a Singleton be serialized and still remain single? (Tricky)** A: Not by default — deserialization creates a *second* instance unless you implement `readResolve()` to return the existing instance. The enum singleton handles this automatically; the class singleton must add `private Object readResolve() { return INSTANCE; }`.
7. **Q: Can reflection break a Singleton?** A: Yes — `setAccessible(true)` on the private constructor allows `new AppConfig()`. Fixes: throw an exception in the constructor if `instance != null`, or use the enum (reflection can't create enum instances).
8. **Q: Is Singleton a good idea for shared mutable state like a counter? (Production)** A: A singleton *is* shared mutable state — use it only if the single-ness is semantically required. For a counter, `AtomicLong` + static, or DI of an injected instance, is simpler and more testable. Interviewers want you to say "singleton for true single-resource; avoid for generic shared state."
9. **Q: What is the "double" in double-checked locking?** A: Two null-checks: the first (outside the lock) avoids paying lock cost after initialization; the second (inside the lock) ensures only one thread constructs when racing. Both are needed for lazy init.
10. **Q: What's the difference between Singleton and a static class?** A: A static class has only static members and cannot be a subtype/instance; a singleton is a *real object* — it can implement interfaces, be passed around, hold instance state, be mocked, and be lazily created. Static classes are simpler but couple everything to a global name.
11. **Q: Why is Singleton considered an anti-pattern by some?** A: Because it introduces hidden global state, couples callers to the concrete class (violating DIP), and hurts testability. Modern guidance: prefer *dependency injection* of a single instance created at the composition root; reserve the GoF singleton for infrastructure facilities or when no container exists.
12. **Q: How does Spring implement singletons? Is it the GoF pattern? (Scenario)** A: Spring's `ApplicationContext` maintains a bean registry (a `ConcurrentHashMap` of name→bean); beans default to `scope="singleton"` meaning one shared instance per bean name per container. That's the *singleton semantics* implemented by a registry/factory — Spring owns creation (not the class), so it's "singleton by container", which is actually the DI-preferred design.
13. **Q: Two threads call `getInstance()` simultaneously with a naive impl. What exactly happens? (Tricky)** A: Both read `instance == null`, both construct, and you get two objects; one reference is overwritten. Worse, the other thread may have a torn/partially-constructed object without `volatile`. This is why the check-and-create must be atomic (lock + volatile publication).
14. **Q: When would you choose a *lazy* singleton over eager in a web application? (Production)** A: When the singleton wraps an expensive, rarely-used resource (e.g., a legacy integration client) that you don't want to instantiate during cold start; lazy defers the cost. Also when the singleton is only used on certain code paths. Eager is fine for cheap, always-used singletons (loggers, small configs).
15. **Q: Can you subclass a Singleton?** A: The GoF book describes singleton subclasses (registry of singletons keyed by name) — but with a private constructor, subclassing is impossible; you'd need a protected constructor and a registry. In practice, don't subclass; use composition or DI instead.
16. **Q: `getInstance()` — is it a static method that blocks all singleton users?** A: Only with the `synchronized`-method implementation. With double-checked locking or the holder, the hot path is lock-free (a volatile read). This is the standard performance discussion: "don't synchronize the accessor in a hot path."
17. **Q: What's a *singleton with parameters*? (Tricky)** A: A singleton whose `getInstance(args)` takes config — but then two different arg sets would "want" two instances, which breaks single-ness. Correct approaches: use a *setter-based* config applied after creation, or a *factory* that builds one instance from config, or ThreadLocal/context-based config. This edge case is a known Singleton smell.
18. **Q: How do you test a Singleton? (Production)** A: Prefer DI so you inject a mock instance. If you must use the GoF singleton, add a package-private/`@VisibleForTesting` static setter (`setInstanceForTesting`), reset it in `@Before`/`@After`, or use Mockito's static mocking (inline mock maker) — and always clean up global state between tests to avoid cross-test leakage.
19. **Q: Name real-world singletons in the JDK and frameworks.** A: `java.lang.Runtime.getRuntime()`, `System.out`/`System.err` (infrastructure), `Desktop.getDesktop()`; Guava `MoreExecutors`; Spring beans default scope; `java.util.logging.LogManager`; each `ClassLoader`'s bootstrap singletons. This demonstrates you know *infrastructure* singletons vs *domain* singletons.
20. **Q: "Design a system where the same settings must be visible everywhere." Would you use Singleton? Walk through the decision. (Scenario)** A: Identify the tension (shared, single source of truth) → candidate Singleton (simple, guaranteed) vs DI single instance (testable, no hidden coupling) vs static holder. In a Spring app, choose DI (a `@ConfigurationProperties` bean injected everywhere — the container makes it a singleton). In a small non-framework app, a holder-based singleton is pragmatic. The answer demonstrates pattern *maturity*: you know Singleton is a tool, not a reflex.

## 14. Follow-Up Questions
1. **Q: What does "double-checked locking was broken until Java 1.5" mean?** A: Before the JMM was redefined in Java 5 (JSR-133), the happens-before semantics for `volatile` didn't guarantee publication of a fully-constructed object; DCL was subtly broken. After 1.5, `volatile` semantics make DCL correct. Knowing this shows historical depth.
2. **Q: What is a "torn" or "partially constructed" object?** A: A reference to an object whose memory is allocated but whose fields are not yet fully initialized (due to instruction reordering under the old JMM or without proper synchronization). Readers observe default field values (0/null). `volatile` + lock prevent this.
3. **Q: Why do web containers cause singleton leakage?** A: A JVM-global singleton holds references to classes loaded by an application's `ClassLoader`; on redeploy, the classloader can't be GC'd (the singleton keeps referencing its classes), causing permgen/metaspace leaks and `ClassNotFoundException` on subsequent deploys. Containers scope beans per-context for this reason.
4. **Q: `INSTANCE` in the enum — what's its access semantics under concurrency?** A: Enum constants are initialized during class initialization, which the JVM serializes (a class is initialized only once, under lock); after that, reads of `INSTANCE` are safe. So the enum needs no `volatile`.
5. **Q: Is `getInstance()` the same as a "Service Locator"?** A: Related: a Service Locator is a singleton-like registry that locates services by name — and it's considered an anti-pattern because it hides dependencies. The GoF singleton is simpler (one object, not a registry). Interviewers sometimes conflate them; differentiate precisely.

## 15. Coding Example
```java
// Production-grade Singleton: static inner holder (lazy + thread-safe + lock-free hot path)
public final class CacheManager {
    private final Map<String, Object> cache = new ConcurrentHashMap<>();
    private CacheManager() {}

    private static final class Holder {
        static final CacheManager INSTANCE = new CacheManager();
    }

    public static CacheManager getInstance() { return Holder.INSTANCE; }

    public Object get(String key) { return cache.get(key); }
    public void put(String key, Object value) { cache.put(key, value); }
}
```
```java
// Enum singleton (Effective Java item 3) — serialization-safe, reflection-safe
public enum Config {
    INSTANCE;
    private final Properties props = new Properties();
    public void load(String path) throws IOException {
        try (var in = Files.newInputStream(Paths.get(path))) { props.load(in); }
    }
    public String get(String key) { return props.getProperty(key); }
}
```
```python
# Python idiomatic singleton: module-level instance (a module is imported once)
# singleton.py
class CacheManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, "cache"):
            self.cache = {}
# Use directly: from singleton import CacheManager  -> same object everywhere
```
```cpp
// C++11 magic statics: thread-safe local static (C++11 and later)
class CacheManager {
    std::unordered_map<std::string, std::string> cache_;
    CacheManager() = default;
public:
    CacheManager(const CacheManager&) = delete;
    CacheManager& operator=(const CacheManager&) = delete;
    static CacheManager& getInstance() {
        static CacheManager instance;   // C++11: initialized exactly once, thread-safely
        return instance;
    }
};
```

## 16. Industry Usage
- **Java standard library**: `Runtime.getRuntime()`, `Desktop.getDesktop()` (platform integration points), `java.util.logging.LogManager`, `SecurityManager` (historical).
- **Spring**: every bean is a singleton by default; `ApplicationContext` itself is a singleton-ish registry; the pattern intent is implemented by the container so that your domain classes stay *testable* (DI instead of GoF singleton).
- **Android**: `Application` instance, system services via `context.getSystemService()` (a service-locator-ish singleton registry).
- **Logging**: Log4j2's `Logger` via `LoggerContext` (a per-classloader registry); SLF4J's `LoggerFactory`.
- **Databases/pools**: HikariCP `DataSource` (one pool per data source), Redis clients (one shared connection pool per client).
- **Caches**: Ehcache/Guava `CacheBuilder` managers, keyed caches per-application.
- **Game engines (Unity/Unreal)**: `GameManager`, `EventManager` as singletons for global systems.
- **Interviews**: singleton is a *guaranteed* question — expect "write a thread-safe singleton", "why is your version safe?", "enum vs holder", "is singleton an anti-pattern?", and "how would you test it?".

## 17. References
- **Gamma et al., *Design Patterns*, 1994 — "Singleton" (p. 127)**: the canonical definition and subclass registry discussion.
- **Joshua Bloch, *Effective Java* (3rd ed.), Item 3**: "Enforce the singleton property with a private constructor or an enum type" — the enum recommendation.
- **Bill Pugh, "The Double-Checked Locking is Broken" Declaration (1996) / Java JSR-133 (Java 5 JMM)**: why DCL requires `volatile` and the pre-1.5 breakage.
- **Brian Goetz, *Java Concurrency in Practice*, Ch. 3**: safe publication, `volatile`, happens-before.
- **Oracle Docs: `volatile`, `synchronized`, JMM** — https://docs.oracle.com/javase/specs/jls/se17/html/jls-17.html
- **Martin Fowler, "Service Locator" / "Inversion of Control Containers and the Dependency Injection pattern" (2004)**: the DI-vs-ServiceLocator critique of singletons.
- **Wikipedia: "Singleton pattern" / "Double-checked locking"** — history of DCL breakage.
- **refactoring.guru — "Singleton"**: modern treatment and when to avoid.

## 18. Cheat Sheet
- Singleton = private constructor + static field + static `getInstance()` → *one instance, global access*.
- **Naive `getInstance()` is NOT thread-safe** — two threads → two instances.
- Safe + lazy + fast: **static inner holder** (`Holder.INSTANCE`) — class-loading is JVM-guaranteed atomic.
- Double-checked locking **requires `volatile`** on the field (safe publication of the fully-constructed object).
- **Enum singleton** (Effective Java): serialization-safe, reflection-proof, simplest — but eager-ish.
- Serialization breaks single-ness unless `readResolve()` returns the instance (enum does this automatically).
- Reflection can break single-ness via `setAccessible(true)` (enum is immune).
- Singleton ≠ static class: singleton is an *object* (interfaces, mocking, lazy init); static class is a name.
- Modern guidance: **prefer DI** of a single instance; GoF singleton for infrastructure/no-container scenarios.
- "Is singleton an anti-pattern?" → "It's abused; it's correct for true one-of-a-kind resources."

## 19. Quiz
1. Which is required for a Singleton? a) public constructor b) private constructor c) final class d) volatile field → **b**
2. The naive lazy singleton is broken because: a) it's slow b) two threads can both pass the null-check and construct c) it uses too much memory d) constructors can't be private → **b**
3. In double-checked locking, the field MUST be: a) static b) volatile c) final d) synchronized → **b**
4. Why does DCL need `volatile`? a) to speed up reads b) to prevent two locks c) to publish the fully-constructed object (prevent reordering) d) to make it immutable → **c**
5. Which singleton impl is serialization-safe out of the box? a) eager static final b) holder class c) enum d) synchronized method → **c**
6. Which is the best (Effective Java) way to write a singleton? a) eager field b) synchronized method c) double-checked locking d) enum → **d**
7. A deserialized singleton is: a) the same instance b) a second instance (unless `readResolve()`) c) null d) a ClassCastException → **b**
8. Spring's default bean scope is: a) prototype b) request c) singleton d) session → **c**
9. Which is a legitimate reason to use a singleton? a) sharing a config with many modules b) global mutable counter c) making a class "special" d) avoiding DI setup → **a**
10. What does `static` class lack that singleton has? a) methods b) fields c) instance semantics (interface impl, mocking, lazy init) d) encapsulation → **c**

## 20. Flashcards
- **Q: What problem does Singleton solve?** → **A:** Guarantees exactly one instance of a class + a global access point, for one-of-a-kind resources (config, pools).
- **Q: Three correct thread-safe implementations?** → **A:** synchronized method; double-checked locking with `volatile`; static inner holder; (plus enum).
- **Q: Why `volatile` in DCL?** → **A:** Safe publication — prevents readers seeing a partially-constructed object (constructor reordering).
- **Q: Why is the naive lazy singleton broken?** → **A:** Two threads can both pass `instance == null` and create two instances.
- **Q: Best singleton in Java?** → **A:** Enum — serialization-safe, reflection-proof, simplest (Effective Java item 3).
- **Q: How to keep a serialized singleton single?** → **A:** Implement `readResolve()` returning the existing instance.
- **Q: Singleton vs static class?** → **A:** Singleton is an object (interfaces, mocking, lazy); static class is a global name.
- **Q: Why is singleton criticized?** → **A:** Hidden global state, hidden coupling (DIP violation), poor testability — prefer DI.

## 21. Revision
Singleton enforces **exactly one instance + global access** via a private constructor and a static accessor — the right tool for one-of-a-kind infrastructure (config, pools, loggers), not a reflex for shared state. The naive lazy version is *broken under concurrency*; production options are the **synchronized method** (safe, slow), **double-checked locking with `volatile`** (safe, fast, subtle — `volatile` publishes the fully-constructed object), the **static inner holder** (safe, lazy, no explicit locking — the sweet spot), and the **enum** (Effective Java's recommendation: serialization-safe, reflection-proof). Watch serialization (`readResolve`) and reflection (enum immune). Criticism: hidden global state and coupling — so prefer **DI of a single instance** (what Spring does: beans are singletons per container). In interviews: write a thread-safe singleton, explain `volatile`, compare enum vs holder, and argue *when not to use it*.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Write a thread-safe singleton." | 9 Internal Working / 15 Coding Example |
| "Why is naive lazy init broken?" | 9 Internal Working / 13 Q2 |
| "Why `volatile` in double-checked locking?" | 9 Internal Working / 13 Q3 / 14 Q1 |
| "Enum vs holder vs DCL?" | 9 Internal Working / 13 Q5 |
| "Can serialization/reflection break it?" | 13 Q6 / 13 Q7 |
| "Is singleton an anti-pattern?" | 12 Disadvantages / 13 Q11 |
| "How does Spring implement singletons?" | 13 Q12 / 16 Industry Usage |
| "When would you avoid a singleton?" | 13 Q8 / 13 Q20 |
| "Singleton with parameters?" | 13 Q17 |
| "How do you test a singleton?" | 13 Q18 |
