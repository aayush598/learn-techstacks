# Proxy Pattern

> **TL;DR**: The Proxy pattern provides a **stand-in or surrogate for another object to control access to it** — it exists to defer expensive creation (lazy loading), enforce security, hide remote communication, add caching, or intercept/audit calls, all *without the client knowing it's talking to a stand-in*.

## 1. Why Does This Exist?
Sometimes you cannot (or must not) let the client talk directly to the real object:
- **Cost**: the real object is expensive to create (loading a 2 GB video file, connecting to a remote service, resolving a heavy image) and shouldn't be built until actually used.
- **Security**: the client must pass authorization before the real object's methods run.
- **Remote access**: the real object lives on another machine; the client must not deal with networking, serialization, or stubs.
- **Performance**: the real object's result is stable; caching at a proxy avoids re-computation.
- **Observability**: every call must be logged, counted, or rate-limited without polluting the real object.

Direct access fails on all of these: eager construction wastes resources, security checks would have to be scattered in the real class (violating SRP), remote calls would leak network code into domain logic, and caching/logging would bloat the real class. The Proxy pattern exists to **interpose a stand-in that controls access**, doing the cross-cutting work (lazy init, security, remote marshaling, caching, logging) *around* the real object — while presenting the *same interface*, so the client can't tell the difference.

## 2. How Does It Work?
```
Client ──uses──> Subject (interface)
                    ▲              ▲
                    │ implements   │ implements
              RealSubject     Proxy (holds a RealSubject reference;
                               controls access / defers creation)
```
Participants:
1. **Subject** — the common interface.
2. **RealSubject** — the real, expensive/remote/sensitive object.
3. **Proxy** — implements `Subject`, holds a reference to `RealSubject`, intercepts calls and either delegates or does work first.

```java
interface Image { void display(); }

class RealImage implements Image {              // expensive to construct
    private final String file;
    RealImage(String f) { this.file = f; loadFromDisk(); }   // slow
    private void loadFromDisk() { System.out.println("Loading " + file + " (slow)"); }
    public void display() { System.out.println("Displaying " + file); }
}

class ProxyImage implements Image {             // Proxy: lazy-load
    private RealImage real;                     // created only on first display()
    private final String file;
    ProxyImage(String f) { this.file = f; }
    public void display() {
        if (real == null) real = new RealImage(file);   // defer expensive construction
        real.display();
    }
}
// Client sees only Image:
Image img = new ProxyImage("photo.jpg");
// nothing loaded yet
img.display();   // now the real image is constructed + displayed
```

## 3. When Is It Used?
- **Virtual Proxy (lazy initialization)**: defer construction of heavy objects (images, configs, ML models, big documents) until first use.
- **Protection Proxy**: enforce access control (roles/permissions) before delegating.
- **Remote Proxy (stub)**: a local object representing a remote object; the proxy handles marshaling/network (Java RMI stubs, gRPC clients).
- **Cache Proxy**: cache expensive results (a weather service, DB queries) keyed by arguments.
- **Logging/Auditing Proxy**: record every call, measure latency, count invocations without touching the real class.
- **Smart Reference Proxy**: track references, close/lock resources when unused.
- **In frameworks**: Spring AOP (`@Transactional`, `@Cacheable`), Hibernate lazy-loading proxies, MyBatis mappers.
- **Interviews**: "lazy load a heavy object", "add security/caching/logging without modifying the class" → Proxy.

## 4. Why Wasn't Another Approach Chosen?
- **Construct the real object eagerly**: simplest, but wastes resources (an image never displayed still loads), breaks responsiveness (slow startup), and can fail at startup for a resource that's never used. Rejected when construction is expensive and usage is uncertain.
- **Put lazy/security/caching logic directly in `RealSubject`**: rejected — violates SRP (the real object now does loading + auth + caching), can't be reused across subjects, and couples the domain object to infrastructure (remote calls, security).
- **Modify the client to check before calling**: rejected — scatters cross-cutting logic across every call site (a bug factory) and leaks knowledge of the real object's cost into clients.
- **A Decorator**: superficially similar (both wrap and delegate), but Decorator *adds behavior* around the same interface for *augmentation*; Proxy *controls access* to the real subject for *management* (lazy, security, remote). The intent differs even though the shapes overlap.
- **An Adapter**: rejected — adapter changes the interface for compatibility; proxy keeps the same interface.
- **A static utility / service that clients call**: rejected — clients must know about the indirection; the proxy's whole value is *transparency* (client sees `Subject` and doesn't care which implementation it is).
- **Hand-written vs dynamic proxies**: hand-written proxies are type-safe and explicit; *dynamic proxies* (`java.lang.reflect.Proxy`, CGLIB, JDK dynamic proxies, Spring AOP) generate the stand-in at run time — chosen when you have many subjects or want framework-managed cross-cutting behavior.

## 5. Intuition
A proxy is a **personal assistant / security guard** for a VIP. You never speak to the VIP (expensive, protected, remote) directly — you speak to the assistant (the proxy). The assistant decides: is the request allowed (protection)? Should the VIP even be woken up yet (lazy init)? Should I answer from memory to save the VIP time (caching)? The VIP does the actual work, but the assistant *controls access* to it — and from the outside, the assistant and the VIP seem like the same person (same interface).

## 6. Real-World Analogy
A **ticket agent vs the performer backstage**. Fans (clients) buy tickets from the agent (proxy); they never talk to the performer directly. The agent controls *when* the performer appears (lazy — only on show night), checks who's allowed backstage (protection), sells cached showtimes (caching), and handles the remote booking system (remote proxy). To the fan, the agent "is" the show's front door — same "interface" as dealing with the venue, but all the messy control logic happens at the agent.

## 7. Formal Definition
> **Proxy**: Provide a **surrogate or placeholder** for another object to **control access** to it. (GoF, p. 207)
>
> Participants: **Subject** (common interface), **RealSubject** (the real object), **Proxy** (maintains a reference to RealSubject, implements Subject, and controls access — creation, security, remote, caching, logging). Varieties: **virtual proxy** (lazy creation), **protection proxy** (access control), **remote proxy** (local stand-in for remote object), **cache proxy**, **smart reference proxy** (tracking).

## 8. Example
A **cache proxy** for an expensive weather API:
```java
interface WeatherService { Weather get(String city); }

class RealWeatherService implements WeatherService {   // calls a remote API — slow
    public Weather get(String city) {
        System.out.println("Calling remote weather API for " + city);
        return new Weather(city, 72);                   // simulated latency
    }
}

class CachedWeatherService implements WeatherService {  // Proxy with caching
    private final Map<String, Weather> cache = new ConcurrentHashMap<>();
    private final WeatherService real;
    CachedWeatherService(WeatherService r) { this.real = r; }
    public Weather get(String city) {
        return cache.computeIfAbsent(city, real::get);  // hit: O(1), miss: real call
    }
}
// Client unchanged:
WeatherService svc = new CachedWeatherService(new RealWeatherService());
svc.get("Bengaluru");   // calls remote
svc.get("Bengaluru");   // cache hit — no remote call
```
- The client sees `WeatherService`; the cache proxy intercepts, serves hits locally, and only the first request reaches the remote service. Adding caching didn't touch `RealWeatherService` or any client.

## 9. Internal Working
1. The client holds a reference typed to `Subject`, but the injected object is a `Proxy`.
2. On `subject.method(args)`:
   a. **Dynamic dispatch** lands on the Proxy's method.
   b. The proxy performs its *interception* in one of several modes:
      - **Lazy**: `if (real == null) real = new RealSubject(...)` then delegate.
      - **Protection**: check permissions (`checkAccess(user, "method")`); deny → throw, allow → delegate.
      - **Remote**: serialize args, send over network, deserialize result, return.
      - **Cache**: hash the args; hit → return cached; miss → delegate + store.
      - **Audit**: log start, delegate, log end/latency.
   c. The proxy delegates to `real.method(args)` (the real work) or handles it entirely (cache hit).
3. The result returns to the client — the client never knows a proxy was involved (**transparency**).

**Concurrency concern**: lazy proxies are *not thread-safe by default* — two threads can both see `real == null` and both construct. Fixes: `synchronized`, double-checked locking with `volatile` (see Singleton, Section 01 of chapter 02), or let the framework do it (Spring/Hibernate generate thread-safe-enough proxies with locking).

## 10. Time Complexity
- **Proxy call overhead**: O(1) — one extra dispatch + the proxy's check. A virtual proxy's first call adds O(construction) once, then O(1) per call.
- **Cache proxy**: O(1) amortized per call (hash lookup); worst-case miss O(real call cost). Hits convert an expensive O(C) operation into O(1).
- **Remote proxy**: adds O(network latency + serialization) per call — the real cost of remote indirection.
- **Lazy creation**: the construction cost is *deferred*, not reduced — worst-case first-call latency = construction cost.
- **Memory**: O(1) for the proxy; O(cache-size) if it caches.

## 11. Advantages
- **Lazy initialization**: expensive objects built only on first use — faster startup, lower resource usage.
- **Access control without touching the real class**: security checks live in the proxy (SRP preserved).
- **Remote transparency**: clients use a local object; networking is hidden (RMI, gRPC stubs).
- **Caching**: repeated expensive results served in O(1); no client changes.
- **Observability**: logging, metrics, and rate limiting can be added uniformly.
- **Transparency**: the client's code is identical whether it holds the real object or a proxy — enabling framework-level injection (Spring, Hibernate).

## 12. Disadvantages
- **Indirection/extra layer**: one more object and call hop; debugging stack traces gain proxy frames.
- **Lazy-init thread-safety trap**: naive lazy proxies are not thread-safe; naive fixes add lock overhead.
- **Identity/equality breaks**: `proxy.equals(real)` fails; `instanceof` against `RealSubject` fails.
- **Exceptions can mask the real problem**: remote proxies wrap network errors in `RemoteException`/`InvocationTargetException` — you lose the original stack unless `initCause` is used.
- **Fragility in AOP/dynamic-proxy land**: proxies generated by frameworks can behave subtly differently (no `this` interception for self-calls, final methods not proxyable) — production gotchas.
- **Proxy can become a hidden coupling**: if overused (proxy per class everywhere), the codebase hides real behavior behind many thin stand-ins.

## 13. Interview Questions
1. **Q: What is the Proxy pattern?** A: A structural pattern providing a surrogate/placeholder that *controls access* to another object — lazy creation, security, remote calls, caching, or logging — while conforming to the same interface so the client is unaware.
2. **Q: What problem does it solve?** A: Direct access to the real object is expensive (construction), dangerous (no access control), remote (network), slow (repeated calls), or unobservable — and none of that logic belongs in the real class. The proxy intercepts around it.
3. **Q: Name the proxy varieties.** A: Virtual (lazy creation), Protection (access control), Remote (local stand-in for remote object — RMI/gRPC stubs), Cache (memoize results), Smart Reference (track usage / release resources).
4. **Q: Proxy vs Decorator?** A: Both wrap and delegate with the same interface. Decorator *adds behavior* (augmentation — stacking responsibilities); Proxy *controls access* (management — lazy/security/remote/caching). Decorator is "make it do more"; Proxy is "control how it's reached".
5. **Q: Proxy vs Adapter?** A: Adapter *changes the interface* for compatibility (a translator); Proxy *keeps the same interface* and controls access. Proxy ≠ interface conversion.
6. **Q: How does a lazy proxy handle thread safety? (Tricky)** A: Naively, two threads both see `real == null` and construct twice. Correct: synchronize the check-and-create, or use double-checked locking with `volatile`, or rely on the framework (Spring/Hibernate). This mirrors the Singleton DCL discussion.
7. **Q: How does Spring AOP implement the Proxy pattern? (Production)** A: When a bean has AOP advice (`@Transactional`, `@Cacheable`), Spring creates a proxy bean (JDK dynamic proxy if the bean implements interfaces, else CGLIB) that intercepts method calls, applies the advice (transaction begin/commit/rollback, cache check), and delegates to the real bean.
8. **Q: Why can't Spring's proxy intercept *self-invocations*? (Tricky)** A: Because the proxy wraps the bean at the boundary — an internal call `this.methodB()` inside the bean never passes through the proxy. Hence `@Transactional` on a method called from within the same class doesn't apply. Fix: self-injection or `AopContext.currentProxy()`. This is a famous Spring production trap.
9. **Q: How does Hibernate use proxies?** A: Lazy-loading proxies: a `@ManyToOne`/`@OneToOne` association is loaded as a proxy that fetches the real entity on first access (first `getXxx()` call) — avoiding eager loading of the whole graph. Accessing the proxy outside a session throws `LazyInitializationException`.
10. **Q: What's the difference between JDK dynamic proxy and CGLIB proxy? (Production)** A: JDK dynamic proxy (`java.lang.reflect.Proxy`) requires the target to implement at least one interface and intercepts via `InvocationHandler`. CGLIB generates a *subclass* at run time, so it works without interfaces but can't proxy `final` classes/methods. Spring defaults: interface → JDK proxy; class → CGLIB.
11. **Q: When would you use a protection proxy in a real system?** A: When a sensitive service (admin operations, user-data endpoints) must check authorization without scattering permission checks in the business class — the proxy checks the current user's roles before delegating, keeping the real class clean.
12. **Q: What does a remote proxy hide from the client?** A: Networking, marshaling/serialization, connection management, and failures (wrapped as remote exceptions). The client calls a local object; the proxy sends bytes over the wire. Java RMI stubs and gRPC client stubs are remote proxies.
13. **Q: How does a cache proxy decide cache validity?** A: Key = method + arguments; TTL, eviction (LRU), and invalidation rules; stale-data tolerance determines policy. The proxy must know when to refresh (e.g., weather service: 10-min TTL). Cache proxies are the heart of many services.
14. **Q: What are the pitfalls of proxies?** A: Thread-safety (lazy init), identity/equality loss, `instanceof` failures, hidden exceptions (wrapped remote/reflection exceptions), self-invocation not intercepted, `final` methods not proxyable, and overuse (indirection everywhere).
15. **Q: Proxy vs Facade?** A: Proxy keeps the same interface to *one* object and controls access; Facade offers a *new simpler interface* to a *whole subsystem*. Proxy = same door, guarded; Facade = new, simpler door.
16. **Q: How is a proxy different from a simple wrapper/helper?** A: A proxy is *transparent* (implements the same Subject interface, so it's interchangeable) and *controls access*; a helper is a separate utility the client calls deliberately. Transparency + interface conformance is what makes something a proxy.
17. **Q: Design a lazy-loading heavy document system. (Scenario)** A: `Document` (Subject) with `open()`/`render()`; `HeavyDocument` (RealSubject) loads a 500 MB file in the constructor; `DocumentProxy` defers construction until `render()` is first called (with double-checked locking). Unopened documents cost nothing; the client never changes.
18. **Q: When should you use a *dynamic* proxy over a hand-written one? (Production)** A: When many classes need the same cross-cutting behavior (logging, transaction, security across a whole service layer) — one `InvocationHandler` serves any interface. Hand-written proxies are better when you want explicit, type-safe, debuggable control over a few classes.
19. **Q: How does the proxy interact with the client's equality checks? (Tricky)** A: `proxy.equals(real)` returns false (different objects), and hash-based containers break if a proxy and real object are mixed. Frameworks handle this by generating `equals/hashCode` that delegate to the target (e.g., Hibernate proxies), but hand-written proxies must be careful.
20. **Q: Proxy + Decorator — can they combine? (Scenario)** A: Yes — a chain: `AuditingProxy(new CachedProxy(new RealService()))` — access control/logging outside, caching inside. Both conform to the same interface, so proxies and decorators compose; the outermost layer defines what the client sees.

## 14. Follow-Up Questions
1. **Q: What is `LazyInitializationException` in Hibernate?** A: Accessing a lazy-loaded proxy after the `Session` is closed throws it, because the proxy has no session to fetch from. It's the classic proxy lifetime bug — solve by keeping the session open, `@Transactional`, or eager `JOIN FETCH`.
2. **Q: How does `java.lang.reflect.Proxy.newProxyInstance` work?** A: It generates (at run time) a class implementing the given interfaces, whose methods route to an `InvocationHandler.invoke(proxy, method, args)`. The generated class IS the proxy — dynamic proxies are just proxies built on demand.
3. **Q: What's the difference between a "virtual proxy" and "lazy initialization"?** A: They're the same idea: virtual proxy is the *pattern name* for lazily creating the real subject on first access. "Lazy initialization" is the general technique; the virtual proxy is its object-oriented, transparent form.
4. **Q: Can a proxy add *new* methods the subject lacks?** A: Not through the shared interface — the client can only call Subject methods. Hand-written proxies can expose extra public methods (e.g., `evictCache()`), but that breaks strict transparency; dynamic proxies can't add interface methods at all. Keep proxies transparent: same interface.
5. **Q: How does the Remote Proxy differ from a Facade to a service?** A: A remote proxy *stands in for one remote object* keeping its interface (RPC stub). A service facade (API gateway) *simplifies access to many services* with a new interface. Same "distributed" flavor, different scope: one object vs many services.

## 15. Coding Example
```java
// Full virtual (lazy) + logging proxy over a document service
interface Document { String render(); }

class HeavyDocument implements Document {          // RealSubject — expensive
    private final String name;
    HeavyDocument(String name) {
        this.name = name;
        System.out.println("[LOAD] " + name + " (heavy: reading 500MB)");   // slow op
    }
    public String render() { return "contents of " + name; }
}

class DocumentProxy implements Document {          // Virtual proxy, lazy + thread-safe
    private volatile HeavyDocument real;           // volatile: safe publication
    private final String name;
    DocumentProxy(String name) { this.name = name; }
    public String render() {
        HeavyDocument local = real;
        if (local == null) {                       // fast path
            synchronized (this) {                  // lock only on miss
                local = real;
                if (local == null) {
                    local = new HeavyDocument(name);   // expensive construction here
                    real = local;
                }
            }
        }
        return local.render();
    }
}

class LoggingProxy implements Document {           // Another proxy (auditing)
    private final Document inner;
    LoggingProxy(Document d) { this.inner = d; }
    public String render() {
        long start = System.nanoTime();
        String result = inner.render();
        System.out.println("[AUDIT] render took " + (System.nanoTime() - start) / 1_000_000 + " ms");
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        Document doc = new LoggingProxy(new DocumentProxy("annual-report.pdf"));
        // Nothing heavy yet:
        doc.render();   // loads + renders + audit log
        doc.render();   // cache-free but no re-load (real already created)
    }
}
```
```python
# Python proxy via __getattr__ delegation
class RealImage:
    def __init__(self, file: str):
        self.file = file
        print(f"[LOAD] {file}")        # expensive
    def display(self) -> None:
        print(f"Displaying {self.file}")

class ProxyImage:
    def __init__(self, file: str):
        self.file, self._real = file, None
    def display(self) -> None:
        if self._real is None:
            self._real = RealImage(self.file)      # lazy
        self._real.display()

img = ProxyImage("photo.jpg")
img.display()      # loads now
img.display()      # already loaded
```
```cpp
// C++ virtual proxy
#include <iostream>
#include <memory>
#include <string>

struct Document { virtual ~Document() = default; virtual std::string render() = 0; };
class HeavyDocument : public Document {
    std::string name_;
public:
    explicit HeavyDocument(std::string n) : name_(std::move(n)) { std::cout << "[LOAD] " << name_ << "\n"; }
    std::string render() override { return "contents of " + name_; }
};
class DocumentProxy : public Document {
    std::shared_ptr<HeavyDocument> real_;   // null until first use
    std::string name_;
public:
    explicit DocumentProxy(std::string n) : name_(std::move(n)) {}
    std::string render() override {
        if (!real_) real_ = std::make_shared<HeavyDocument>(name_);   // lazy
        return real_->render();
    }
};
// int main(){ Document* d = new DocumentProxy("x.pdf"); std::cout << d->render() << "\n"; }
```

## 16. Industry Usage
- **Spring AOP**: `@Transactional`, `@Cacheable`, `@Secured` — implemented via JDK dynamic or CGLIB proxies; the single most common proxy usage in Java production.
- **Hibernate/JPA**: lazy-loading proxies for associations; proxies over entities returned from `getReference()`.
- **Java RMI / CORBA / gRPC**: remote stubs (proxies) marshaling calls across processes — the original remote-proxy use case from the GoF book.
- **java.lang.reflect.Proxy**: JDK dynamic proxies powering frameworks (Spring, MyBatis, Retrofit).
- **Caching layers**: Spring `@Cacheable`, Guava `Cache` wrappers, Redis cache-aside proxies.
- **Networking/security**: reverse proxies (nginx), service mesh sidecars (Envoy — control access to services), API gateways with auth.
- **ORM/microservice lazy loading**: JPA `@ManyToOne(fetch = LAZY)`.
- **Interviews**: "lazy load a heavy object", "add security without modifying the class", "how does `@Transactional` work?", "Hibernate lazy loading", "JDK vs CGLIB proxy" — all classic.

## 17. References
- **Gamma et al., *Design Patterns* — "Proxy" (p. 207)**: canonical definition, virtual/protection/remote variants.
- **Oracle Docs: `java.lang.reflect.Proxy`, `InvocationHandler`, Java RMI** — https://docs.oracle.com/javase/8/docs/api/java/lang/reflect/Proxy.html
- **Spring Framework Reference: AOP — "Proxying Mechanisms" (JDK vs CGLIB), `@Transactional` self-invocation** — https://docs.spring.io/spring-framework/reference/core/aop/
- **Hibernate Docs: lazy loading, `LazyInitializationException`** — https://hibernate.org/orm/documentation/
- **Joshua Bloch, *Effective Java* (3rd ed.), Item 18**: composition/wrapper classes — the proxy/wrapper family context.
- **refactoring.guru — "Proxy"** — modern diagrams and Java/C++/Python examples.
- **Baeldung — "Proxy Pattern in Java" and "Spring AOP vs AspectJ"** — practical tutorials.

## 18. Cheat Sheet
- Proxy = **surrogate controlling access** to the real object; same interface → transparent.
- Varieties: **Virtual** (lazy), **Protection** (auth), **Remote** (stub/marshaling), **Cache** (memoize), **Smart reference** (tracking).
- **Proxy vs Decorator**: decorator *adds behavior*; proxy *controls access*. (Both same interface.)
- **Proxy vs Adapter**: adapter *changes interface*; proxy keeps it.
- **Proxy vs Facade**: facade simplifies a subsystem; proxy guards one object.
- Lazy proxies need **double-checked locking with `volatile`** (same trap as Singleton).
- Spring AOP = JDK dynamic proxy (interface) or CGLIB (subclass); **self-invocation is not intercepted**.
- Hibernate lazy proxies → `LazyInitializationException` when used outside a session.
- Proxies break **identity/equality** (`proxy.equals(real)` false) and `instanceof` on the real class.
- Framework examples: `@Transactional`, `@Cacheable`, RMI/gRPC stubs, `java.lang.reflect.Proxy`.

## 19. Quiz
1. Proxy's intent: a) add behavior b) control access to another object c) change interface d) simplify subsystem → **b**
2. Which proxy defers construction? a) protection b) virtual c) remote d) cache → **b**
3. A gRPC client stub is a: a) virtual proxy b) remote proxy c) cache proxy d) adapter → **b**
4. Proxy vs Decorator: a) decorator controls access b) proxy controls access, decorator adds behavior c) both add behavior d) both change interface → **b**
5. Proxy vs Adapter: a) adapter keeps interface b) proxy keeps interface, adapter changes it c) both keep d) neither → **b**
6. Spring creates which proxy for a bean implementing an interface? a) CGLIB b) JDK dynamic proxy c) hand-written d) no proxy → **b**
7. Why does `this.methodB()` inside a proxied bean bypass `@Transactional` on B? a) Java syntax b) the internal call never passes the proxy c) CGLIB can't d) config issue → **b**
8. The lazy-init proxy must use ___ to be thread-safe. a) nothing b) double-checked locking with volatile c) an enum d) serialization → **b**
9. Hibernate throws ___ when a lazy proxy is accessed outside a session. a) NullPointerException b) LazyInitializationException c) SQLException d) ClassCastException → **b**
10. `proxy.equals(real)` returns: a) true always b) false (identity lost through wrapping) c) depends on hash d) exception → **b**

## 20. Flashcards
- **Q: Proxy intent?** → **A:** Provide a surrogate that controls access to the real object (lazy, security, remote, cache) with the same interface.
- **Q: Proxy varieties?** → **A:** Virtual (lazy), Protection (auth), Remote (stub), Cache, Smart reference.
- **Q: Proxy vs Decorator?** → **A:** Decorator adds behavior; Proxy controls access. Both keep the interface.
- **Q: Proxy vs Adapter?** → **A:** Proxy keeps the interface; Adapter changes it.
- **Q: Lazy proxy thread-safety?** → **A:** Double-checked locking with `volatile`.
- **Q: Spring AOP proxy types?** → **A:** JDK dynamic proxy (interface) / CGLIB (subclass); self-invocations bypass the proxy.
- **Q: Hibernate lazy proxy outside a session?** → **A:** `LazyInitializationException`.
- **Q: What breaks with proxies?** → **A:** Identity/equality and `instanceof` against the real class.

## 21. Revision
Proxy is a **surrogate that controls access** to a real object through the *same* interface — transparent to the client. Varieties: virtual (lazy creation — defer expensive construction until first use), protection (enforce authorization), remote (local stub over network — RMI/gRPC), cache (memoize repeated results), smart reference (tracking). It exists because eager construction wastes resources, and security/caching/logging/network logic doesn't belong in the real class (SRP). Discriminate: Decorator *adds behavior* (same interface); Adapter *changes interface*; Facade *simplifies a subsystem*. Correctness: lazy proxies need double-checked locking with `volatile`; proxies break `equals`/`instanceof`; remote proxies hide errors. Production: Spring AOP (`@Transactional`/`@Cacheable` — JDK dynamic vs CGLIB; **self-invocations bypass the proxy** — the famous trap), Hibernate lazy-loading proxies (`LazyInitializationException` outside a session), RMI/gRPC stubs, `java.lang.reflect.Proxy`. Interview hook: "lazy load / add security / how does `@Transactional` work?" → Proxy.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Proxy pattern / its varieties?" | 2 How / 13 Q1 / 13 Q3 |
| "Proxy vs Decorator / Adapter / Facade?" | 13 Q4–Q5 / 13 Q15 |
| "How does lazy-init thread safety work?" | 13 Q6 / 14 Q3 / 15 Coding |
| "How does Spring AOP implement proxies?" | 13 Q7 / 16 Industry Usage |
| "Why is self-invocation not intercepted?" | 13 Q8 / 18 Cheat Sheet |
| "Hibernate lazy loading / LazyInitializationException?" | 13 Q9 / 14 Q1 |
| "JDK dynamic proxy vs CGLIB?" | 13 Q10 / 16 Industry Usage |
| "When to use a protection proxy?" | 13 Q11 |
| "Design a lazy-loading document system (scenario)." | 13 Q17 / 15 Coding |
| "What are proxy pitfalls?" | 13 Q14 / 13 Q19 |
