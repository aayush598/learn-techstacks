# Design Patterns in Java and Spring Libraries

> **TL;DR**: The GoF patterns are not academic — they are the **actual architecture of the JDK and Spring**: `Comparator` is Strategy, `FilterInputStream` is Decorator, `Runtime` is Singleton, `Iterator` is Iterator, Spring's `BeanFactory` is Factory + Singleton, `@Transactional` is Proxy, `ApplicationContext` is Facade, `@EventListener` is Observer, and `JdbcTemplate` is Template Method — and interviewers test whether you can *recognize* these, not just name the patterns.

## 1. Why Does This Exist?
Interviewers rarely ask "what is the Strategy pattern?" and stop there. The senior-level follow-up is always **"and where does Java/Spring actually use it?"** — because naming a pattern you've never seen in production proves memorization, not understanding. This section exists to build **pattern recognition at the library level**: knowing that `Collections.sort(list, comparator)` *is* Strategy, that every `BufferedReader(new FileReader(...))` *is* Decorator, and that Spring's entire IoC container *is* a composite of Factory + Singleton + Proxy. When you can point at real classes, you prove you can (a) read production code at the shape level, (b) apply patterns correctly in your own designs, and (c) justify framework choices in design reviews. It's the bridge from "I studied patterns" to "I understand how the frameworks I use are built."

It also exists because the *same* pattern appears again and again with different names: learning to see "this is a Proxy" under Spring's `@Transactional`, Hibernate's lazy associations, and Java RMI stubs trains the one skill that transfers across every library you'll ever meet.

## 2. How Does It Work?
Recognition works by **mapping each pattern's participants onto a real API**:
1. Identify the *interface* (the pattern's `Strategy`/`Component`/`Subject`).
2. Identify the *concrete implementation(s)* (ConcreteStrategy / ConcreteComponent / Observer).
3. Identify the *context/aggregate* (the object that delegates / holds the reference).
4. Confirm the *intent* (interface change? behavior add? access control? notification?) — not just the shape.

Example — `Comparator`:
- Strategy interface = `Comparator<T>`.
- Concrete strategies = any comparator you write (`(a,b) -> a.age - b.age`).
- Context = `Collections.sort(list, c)` / `TreeMap(comparator)`.
- Intent = vary the *sorting algorithm's comparison* without changing the sort routine → **Strategy**. ✓

Example — `@Transactional` (Spring):
- Real subject = your bean's method (the transactional work).
- Proxy = the JDK-dynamic/CGLIB proxy Spring wraps around the bean.
- Interception = begin/commit/rollback around the method call.
- Intent = *control* what happens around the real call (transaction boundary) while presenting the same interface → **Proxy** (with AOP "around" advice), *not* Decorator (which adds a responsibility to the object's own behavior, not an external control seam).

## 3. When Is It Used?
- **In design interviews** when asked "which pattern is this?" or "how would you implement X in Spring?".
- **In code reviews** when recognizing a framework's internal shape helps you predict behavior (why self-invocation bypasses `@Transactional`; why `Observable` was deprecated).
- **When extending frameworks**: knowing `JdbcTemplate` is Template Method tells you *which methods to override* (`doInConnection` callback) and which to leave alone (the fixed skeleton).
- **When troubleshooting**: recognizing the Proxy behind `@Transactional` explains proxy-only failure modes; recognizing the Decorator chain in I/O explains buffering/encoding layering.
- **When designing**: you cite the library precedent as evidence your chosen pattern is idiomatic ("Spring does exactly this with X").

## 4. Why Wasn't Another Approach Chosen?
- **Learning patterns from diagrams only**: rejected because the interview (and production reality) is recognition — diagrams don't tell you that `JdbcTemplate` is a Template Method or that `CompletableFuture.thenApply` is an Observer-ish callback. Library mapping is the *evidence* layer.
- **Listing patterns alphabetically**: rejected as non-usable — this section is organized by *library* (JDK first, Spring second), mirroring how interviewers probe ("JDK examples?" then "Spring examples?").
- **Relying on Spring's own docs to name patterns**: rejected — Spring rarely labels its classes "Strategy" or "Proxy"; you must infer intent from the structure (which is exactly the skill being trained).
- **A separate "case study" appendix**: rejected — recognition is a *per-pattern* habit, so this section maps pattern-by-pattern, reinforcing each one where it appears.

## 5. Intuition
Think of the JDK and Spring as **pattern museums** — every wing is curated around a pattern, even though the plaques aren't labeled. `java.io` is the *Decorator wing* (streams layering streams). The collections framework is the *Iterator + Strategy + Factory wing* (every collection returns an iterator; sorts take comparators; `Collection.of`/factories create). Spring's `ApplicationContext` is the *Facade + Factory + Singleton wing* (one door over creation, wiring, events). The skill is **reading the architecture the way an architect reads a building** — you see the structural choices ("this was built as a Decorator chain") even though no blueprints are posted.

## 6. Real-World Analogy
A **city map annotated with landmarks**. The GoF catalog is the legend (🔺 factory, 🏛️ facade, 📡 observer). This section is the *annotated map of the city you work in*: "this building (Spring) is a facade over its interior; this tower (Java I/O) is a stack of decorators; this exchange (BeanFactory) is a factory + singleton registry." When someone asks "where do you actually see a Decorator?" you don't describe the concept — you *point at the building*. Recognition is knowing the landmarks; the map is the library.

## 7. Formal Definition
**Pattern recognition** is the inverse of pattern application: given a concrete system, identify the GoF patterns instantiated in it by (a) finding the interface–implementation relationships, (b) verifying the *intent* matches the pattern's defined problem (not merely its structure), and (c) naming the participants in the real code. A library usage is *canonical* when the pattern's intent (creation / composition / communication) is genuinely served by the design — e.g., `Comparator` serving `Collections.sort` is Strategy by intent; a random wrapper class that merely looks like a Decorator but adds no behavior is not one.

## 8. Example
**Pattern-by-pattern recognition table for the JDK:**

| Pattern | JDK example | Participants in real code |
|---|---|---|
| **Strategy** | `Collections.sort(list, comparator)` | Strategy=`Comparator`; ConcreteStrategy=your comparator; Context=`Collections.sort` |
| **Decorator** | `new BufferedReader(new FileReader(f))` | Component=`Reader`; Decorator=`BufferedReader`/`FilterReader`; ConcreteComponent=`FileReader` |
| **Adapter** | `InputStreamReader` (byte→char), `Arrays.asList` | Target=`Reader`; Adaptee=`InputStream` |
| **Iterator** | `Iterator`/`Iterable`, for-each | Aggregate=`Collection`; Iterator=`ArrayList.Itr` |
| **Singleton** | `Runtime.getRuntime()` | private ctor + static accessor |
| **Factory Method** | `Collection.iterator()`, `Calendar.getInstance()` | Creator=`Collection`; Product=`Iterator` |
| **Observer** | `Observable`/`Observer` (deprecated), `PropertyChangeSupport` | Subject=`Observable`; Observer=`Observer` |
| **Command** | `Runnable`/`Callable`/`Supplier`, `ExecutorService` | Command=`Runnable`; Invoker=`Executor`; Receiver=your task |
| **Template Method** | `AbstractList`, `Thread.run()`, servlet `service()` | Base=`AbstractList`; steps=`get`/`size` abstract |
| **Memento** | `UndoManager`+`StateEditable` | Originator=editor; Caretaker=`UndoManager` |
| **Prototype** | `Object.clone()`/`Cloneable` (discouraged) | Prototype=the cloneable object |

## 9. Internal Working
**How the JDK "runs" these patterns:**
1. **`Collections.sort(list, comparator)`**: the sort algorithm is fixed (TimSort/MergeSort); the *comparison* is the varied step — the comparator is called inside the sort loop (the context) → Strategy, executed per comparison (O(1) callbacks, O(n log n) total).
2. **`new BufferedReader(new FileReader(f))`**: `BufferedReader` (a `FilterReader` subclass — abstract Decorator) holds the wrapped reader; every `read()` buffers from the inner stream → Decorator chain, executed per read.
3. **`for (X x : coll)`**: compiled to `Iterator` creation + `hasNext`/`next` calls → Iterator, per element.
4. **`Runtime.getRuntime()`**: a static holder returning the one process-wide runtime → Singleton, O(1) per call.

**How Spring "runs" them:**
1. **BeanFactory/ApplicationContext** = **Factory + Singleton**: `getBean("name")` looks up the singleton registry (a `ConcurrentHashMap`) or creates a prototype → Abstract-Factory-style creation + registry.
2. **`@Transactional`/`@Cacheable`** = **Proxy**: Spring wraps the bean in a JDK-dynamic or CGLIB proxy; the proxy's `InvocationHandler`/method interceptor begins the transaction, delegates, commits/rolls back → Proxy + AOP "around" advice.
3. **`ApplicationContext`** = **Facade**: one object exposes bean access, events (`publishEvent`), resources, environment, and lifecycle over the whole container.
4. **`@EventListener`** = **Observer**: `ApplicationEventPublisher` notifies registered listeners (type-dispatched, sync by default).
5. **`JdbcTemplate`/`RestTemplate`** = **Template Method**: the skeleton (open/execute/map/close) is fixed; `doInConnection(StatementCallback)` is the overridable step.
6. **`HandlerAdapter`** = **Adapter**: `DispatcherServlet` uniformly executes any controller shape via an adapter.
7. **`ProxyFactoryBean`/`FactoryBean<T>`** = **Factory**: objects that produce other objects behind a factory interface.

## 10. Time Complexity
- **Recognition itself**: O(1) once you know the library — the real value is *cognitive*, not computational.
- **Underlying library behavior** (what matters to interviews):
  - `Collections.sort` + comparator: O(n log n) comparisons (Strategy adds O(1)/comparison).
  - Decorator I/O: O(1) per call per layer (O(L) for L layers).
  - Singleton `getRuntime()`: O(1).
  - Iterator: O(1) per step, O(N) per traversal.
  - Spring Proxy: O(1) interceptor dispatch per proxied call (plus AOP advice cost).
  - `@EventListener`: O(N) listeners per event (Observer fan-out).
  - `getBean`: O(1) registry lookup (singleton) or O(construction) (prototype).
- **Design cost**: using these patterns in your code adds the same O(1) indirection noted in Section 01/10 — no algorithmic change, only structural overhead.

## 11. Advantages
- **Pattern recognition = production fluency**: you can read frameworks, extend them correctly, and troubleshoot their internals.
- **Evidence-backed interview answers**: "which pattern is this?" becomes a confident, specific answer.
- **Correct framework use**: knowing `JdbcTemplate` is Template Method tells you which methods to override; knowing `@Transactional` is Proxy explains self-invocation pitfalls.
- **Design justification**: you cite library precedent ("Spring does exactly this") as evidence your chosen pattern is idiomatic.
- **Faster onboarding**: the "pattern museum" lens makes new frameworks feel familiar — you're recognizing shapes, not memorizing APIs.
- **Cross-language transfer**: the same patterns appear in .NET, JS frameworks, Python libs — recognition transfers.

## 12. Disadvantages
- **Over-generalization risk**: seeing patterns where the intent doesn't match (calling a random wrapper a Decorator when it's just a utility) — a false pattern (Section 01/13 Q11).
- **Library-vs-pattern confusion**: Spring's "singleton" is registry-based, not the GoF singleton — calling Spring beans "the Singleton pattern" without nuance is a classic interview error.
- **Evolution makes maps stale**: `Observable` deprecated, `Cloneable` discouraged — the "museum" changes; recognition must track deprecations.
- **Recognition ≠ application**: knowing Spring's patterns doesn't mean you can design well — it's necessary but not sufficient (Section 02 covers selection).
- **Potential for name-dropping**: reciting "that's a Proxy" without explaining the intent and consequences is as bad as not knowing.

## 13. Interview Questions
1. **Q: Which GoF pattern is `Collections.sort(list, comparator)`?** A: Strategy — `Comparator` is the Strategy interface, your comparator the ConcreteStrategy, and the sort routine the context that applies the comparison strategy. It varies the comparison without changing the sorting algorithm.
2. **Q: Which pattern is `new BufferedReader(new FileReader(f))`?** A: Decorator — `Reader` is the Component, `FileReader` the ConcreteComponent, `FilterReader`/`BufferedReader` the abstract/concrete decorators adding buffering. `FilterInputStream`/`FilterReader` are the JDK's abstract Decorator classes.
3. **Q: Is Spring's `@Transactional` a Proxy or a Decorator? (Tricky)** A: **Proxy** — Spring wraps the bean in a JDK-dynamic/CGLIB proxy that *controls the transaction boundary around* the real method call (begin/commit/rollback), presenting the same interface. It's not a Decorator because it doesn't *add a responsibility to the object's behavior*; it *intercepts and manages access/lifecycle* around the call — the Proxy intent (and AOP "around" advice). The shapes overlap; the intent differs.
4. **Q: Which pattern is `Runtime.getRuntime()`?** A: Singleton — private constructor + static accessor returning the one process-wide `Runtime`. (Note: it's lazy-ish via the static holder mechanism the JVM uses.)
5. **Q: Which pattern is Spring's `ApplicationContext`?** A: Facade (and Factory) — it exposes a unified interface over bean creation, wiring, event publishing, resource loading, and environment; `getBean` is the Abstract-Factory-style creation. One door over the whole container.
6. **Q: Is Spring's bean "singleton scope" the GoF Singleton pattern? (Tricky)** A: No — it implements *singleton semantics* via a container registry (`ConcurrentHashMap` per bean name), not the GoF pattern (no private constructor; the container owns creation). This is the DI-preferred form: the *container* enforces single-ness, not the class. Saying this precisely is the senior answer.
7. **Q: Which pattern is Spring's `@EventListener` / `ApplicationEventPublisher`?** A: Observer — publishers broadcast events to registered listeners (`@EventListener`-annotated methods), type-dispatched, synchronous by default. It's Observer with framework-managed registration.
8. **Q: Which pattern is `JdbcTemplate`?** A: Template Method — the skeleton (open → execute SQL → map results → handle exceptions → close) is fixed; the `doInConnection(StatementCallback)` callback is the overridable step subclasses/clients provide.
9. **Q: Which pattern is `Iterator` in the JDK?** A: Iterator — every collection returns an iterator via the Factory Method `iterator()`; enhanced for-each compiles to `hasNext()`/`next()`. The JDK's collections framework is *both* Iterator and Factory Method.
10. **Q: Which pattern does `Runnable`/`Callable` represent?** A: Command — a request (a task) encapsulated as an object, submitted to an `ExecutorService` (the Invoker/queue) and executed by a worker (the Receiver context). `submit(runnable)` queues commands.
11. **Q: Which pattern is `Arrays.asList(...)` / `Collections.unmodifiableList(...)`?** A: Adapter-ish (asList: array → List interface conversion) and a structural wrapper (unmodifiableList: exposes a restricted view). `asList` is the classic Adapter — it adapts the array's interface to `List` without copying.
12. **Q: Where does Spring use the Factory pattern?** A: `BeanFactory`/`ApplicationContext.getBean()` (Abstract-Factory-style creation), `FactoryBean<T>` (a factory object producing beans), `@Bean` methods (factory methods), `ProxyFactoryBean` (factory producing proxies). Spring's IoC container *is* a factory at its core.
13. **Q: Where does Spring use the Adapter pattern?** A: `HandlerAdapter` — `DispatcherServlet` uniformly executes heterogeneous controllers (`@Controller`, `Controller`, `HttpRequestHandler`, `HandlerFunction`) by adapting each to a uniform `handle()` call. Also `MethodInvokingFactoryBean`-style adapters.
14. **Q: Which pattern is `java.util.Observable` and why was it deprecated? (Production)** A: Observer — but deprecated because it's a *class* (forces `extends`), uses a synchronized `Vector`, has a clunky API, and can't carry rich event payloads. Modern replacement: custom subject + `CopyOnWriteArrayList`, or Spring `@EventListener`, or reactive streams.
15. **Q: Which pattern is Hibernate's lazy-loading?** A: Proxy (virtual proxy) — associations load as proxies that fetch the real entity on first access. Accessing the proxy outside the session throws `LazyInitializationException`. Same intent as the GoF virtual proxy.
16. **Q: Which patterns are combined in Spring's IoC container? (Scenario)** A: **Factory** (creates beans) + **Singleton** (registry per bean name) + **Proxy** (AOP on proxied beans) + **Facade** (`ApplicationContext`'s unified API) + **Observer** (event publishing). Naming the composition (not just one pattern) is the senior answer.
17. **Q: Which pattern is `CompletableFuture`?** A: Observer-ish — `thenApply`/`whenComplete` register callbacks (Observers) that fire when the future completes; plus Command-ish (`supplyAsync(runnable)` submits a task). It's an observer-callback API over asynchronous completion.
18. **Q: Which pattern is Swing's `EventListenerList` + `addActionListener`?** A: Observer — the component is the Subject, listeners are Observers, and `EventListenerList` is the thread-safe typed listener registry. Swing's whole event model is Observer.
19. **Q: Which pattern is `javax.servlet.http.HttpServlet.service()`?** A: Template Method — `service()` dispatches to `doGet`/`doPost`/`doPut` (hooks); subclasses override only the HTTP-method steps while the request-handling skeleton stays fixed.
20. **Q: How would you *prove* in an interview that you recognize patterns in a framework you haven't studied? (Scenario)** A: Take one class, run the triage: identify its interface(s), its concrete implementations, the object that delegates/owns, and the *intent* (compat / augmentation / access control / notification / creation). Then verify with the library's docs and name participants in real code. The method (interface → implementers → intent) transfers to any framework.

## 14. Follow-Up Questions
1. **Q: Is `StringBuilder` a Builder pattern?** A: Yes — a *fluent* builder that accumulates mutable state and produces an immutable `String` via `toString()`; it's the JDK's canonical fluent builder (along with `Locale.Builder`, `HttpClient.Builder`).
2. **Q: Is `Map.of()` / `List.of()` a Factory?** A: Yes — static factory methods (Effective Java item 1): a *convention* (a static method returning an instance), related to but not identical with the Factory Method *pattern* (an overridable instance method used by creator logic).
3. **Q: Which patterns does the JDK use to make `for-each` work?** A: Factory Method (each collection's `iterator()`) + Iterator (the returned cursor). The enhanced for is *syntax* that compiles to the pattern.
4. **Q: Does Spring ever use Decorator?** A: Yes, occasionally — e.g., `CompositePropertySource` (a composite), `WebClient` builder layering, and framework response/request wrappers (`ContentCachingResponseWrapper` is decorator-flavored over the servlet response). But Spring's *headline* patterns are Factory/Singleton/Proxy/Facade/Template; naming Decorator where it genuinely appears (e.g., in servlet wrappers) shows precision.
5. **Q: How do you map a pattern to a framework class *without* the docs?** A: Read the class's dependencies and methods: does it take an interface and delegate (Strategy/Template)? Does it wrap another object of the same interface and add behavior (Decorator)? Does it own a list of callbacks (Observer)? Does it create things (Factory)? Does it expose one API over many subsystems (Facade)? The *structure* plus the *method signatures* reveal the intent — that's the recognition skill.

## 15. Coding Example
```java
// Recognizing patterns by reading — a "museum tour" in code
import java.util.*;
import java.io.*;
import java.util.concurrent.*;

public class PatternMuseum {
    public static void main(String[] args) throws Exception {
        // 1. STRATEGY — Comparator in Collections.sort
        List<String> names = new ArrayList<>(List.of("bob", "alice", "carol"));
        Collections.sort(names, (a, b) -> b.compareTo(a));      // strategy: reverse compare
        System.out.println(names);                              // [carol, bob, alice]

        // 2. DECORATOR — BufferedReader over FileReader over (no-op) over StringReader
        BufferedReader br = new BufferedReader(new StringReader("hello\nworld"));
        System.out.println(br.readLine());                      // hello  (buffered read)
        br.close();

        // 3. ITERATOR + FACTORY METHOD — for-each compiles to iterator()
        for (String s : names) System.out.print(s.charAt(0));   // cba

        // 4. COMMAND — Runnable submitted to an executor
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<?> f = pool.submit(() -> System.out.println("task ran"));   // Runnable = Command
        pool.shutdown();

        // 5. SINGLETON — Runtime.getRuntime()
        System.out.println(Runtime.getRuntime().availableProcessors());     // one instance

        // 6. ADAPTER — Arrays.asList (array → List)
        String[] arr = {"x", "y"};
        List<String> list = Arrays.asList(arr);                 // adapted view
        System.out.println(list);

        // 7. TEMPLATE METHOD — AbstractList requires only get() and size()
        List<String> tiny = new AbstractList<>() {
            private final String[] data = {"a", "b"};
            public String get(int i) { return data[i]; }        // the abstract step
            public int size() { return data.length; }           // the abstract step
        };
        System.out.println(tiny);                               // [a, b] — everything else from AbstractList
    }
}
```
```java
// Simulating Spring's proxy for @Transactional (the Proxy pattern in miniature)
import java.lang.reflect.*;

interface PaymentService { void pay(double amt); }

class RealPaymentService implements PaymentService {
    public void pay(double amt) { System.out.println("Real: charging $" + amt); }
}

public class TransactionalProxy {
    public static void main(String[] args) {
        PaymentService real = new RealPaymentService();
        // JDK dynamic proxy = Spring's proxy mechanism (like @Transactional)
        PaymentService proxied = (PaymentService) Proxy.newProxyInstance(
                TransactionalProxy.class.getClassLoader(),
                new Class<?>[]{PaymentService.class},
                (proxy, method, margs) -> {
                    System.out.println("[BEGIN TX]");
                    try { Object r = method.invoke(real, margs); System.out.println("[COMMIT]"); return r; }
                    catch (Throwable t) { System.out.println("[ROLLBACK]"); throw t; }
                });
        proxied.pay(100.0);
        // [BEGIN TX] / Real: charging $100.0 / [COMMIT]
    }
}
```
```python
# Recognizing patterns in Python libs
import functools

# Strategy: sorted() takes a key function
data = ["bb", "a", "ccc"]
print(sorted(data, key=len))            # ['a', 'bb', 'ccc']  — key IS a strategy

# Decorator: functools.lru_cache wraps a function
@functools.lru_cache(maxsize=None)       # python decorator (function-level Decorator pattern)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print(fib(20))

# Observer: asyncio callbacks / add_done_callback
import asyncio
async def main():
    fut = asyncio.get_event_loop().create_future()
    fut.add_done_callback(lambda f: print("observer fired:", f.result()))
    fut.set_result(42)
asyncio.run(main())
```
```cpp
// C++ recognition: STL as a pattern museum
#include <iostream>
#include <vector>
#include <algorithm>
#include <thread>

// Strategy: std::sort with a comparator (a strategy via function)
int main() {
    std::vector<int> v{3, 1, 2};
    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });  // strategy
    // Iterator: begin()/end() are iterators; range-for uses them
    for (int x : v) std::cout << x << " ";                               // 3 2 1
    std::cout << "\n";
    // Command: std::thread takes a callable (a command)
    std::thread t([]{ std::cout << "task\n"; });
    t.join();
}
```

## 16. Industry Usage
- **Every Java production service** uses these patterns daily via the JDK (Iterator in every for-each, Strategy in every comparator, Decorator in every buffered stream, Command in every executor, Singleton in `Runtime`).
- **Every Spring application** is built on Factory+Singleton (beans), Proxy (`@Transactional`/`@Cacheable`/`@Secured`), Facade (`ApplicationContext`), Observer (`@EventListener`), Template Method (`JdbcTemplate`/`RestTemplate`), Adapter (`HandlerAdapter`), Command (transaction templates, task scheduling).
- **Hibernate**: virtual Proxy for lazy loading; Template Method in `Session`/`Transaction`; Factory in `SessionFactory`/`EntityManagerFactory`.
- **Non-Java ecosystems prove transferability**: .NET's `IComparer` (Strategy), `Stream` wrappers (Decorator); Python's `functools`/`contextlib` (decorators/observers); Go's `sort.Interface` (Strategy+Template); JS's `EventTarget`/`Promise` (Observer/Command-ish).
- **Interviews**: "which pattern is X?" (JDK/Spring recognition) is among the most common senior OOP questions — expect `Comparator`, `BufferedReader`, `@Transactional`, `Runtime`, `ApplicationContext`, `Observable`, `JdbcTemplate`, `iterator()`, and `Runnable` as the classic probes.

## 17. References
- **Oracle Java Docs**: `java.util.Collections.sort`, `java.io.FilterInputStream`/`FilterReader`, `java.lang.Runtime`, `java.util.Iterator`/`Iterable`, `java.util.Observable`, `java.util.concurrent.Runnable`/`ExecutorService`, `java.lang.reflect.Proxy` — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Reference**: "The IoC Container" (BeanFactory, scopes, FactoryBean), "AOP" (proxying mechanisms), "Events" (`ApplicationEventPublisher`/`@EventListener`), "Data Access" (`JdbcTemplate`), "Web MVC" (`HandlerAdapter`) — https://docs.spring.io/spring-framework/reference/
- **Hibernate ORM Docs**: lazy loading / proxy mechanism — https://hibernate.org/orm/documentation/
- **Joshua Bloch, *Effective Java* (3rd ed.), Items 1, 3, 13, 18**: static factories, singletons (enum), clone critique, composition over inheritance — the JDK-behind-the-JDK commentary.
- **Gamma et al., *Design Patterns*** — the canonical intents this chapter maps onto libraries.
- **refactoring.guru — "Design Patterns in Java"** — library mapping pages.
- **Baeldung — "Design Patterns in the Spring Framework"** — pattern-by-pattern Spring tour.

## 18. Cheat Sheet
- **Recognition method**: interface → implementations → delegator → *intent* (never just shape).
- JDK map: `Comparator`=Strategy, `FilterInputStream`/`BufferedReader`=Decorator, `Iterator`=Iterator, `Runtime`=Singleton, `iterator()`=Factory Method, `Observable`=Observer (deprecated), `Runnable`/`Executor`=Command, `AbstractList`/`Thread.run`=Template Method, `Arrays.asList`/`InputStreamReader`=Adapter, `StringBuilder`/`HttpClient.Builder`=Builder, `clone()`=Prototype (discouraged).
- Spring map: `BeanFactory`/`getBean`=Factory, beans (default scope)=Singleton (registry-based), `@Transactional`/`@Cacheable`=Proxy (AOP), `ApplicationContext`=Facade+Factory, `@EventListener`=Observer, `JdbcTemplate`/`RestTemplate`=Template Method, `HandlerAdapter`=Adapter, `FactoryBean<T>`=Factory.
- Spring's bean singleton is **container-enforced**, not the GoF private-constructor singleton.
- `@Transactional` = **Proxy** (access/control seam), not Decorator (behavior augmentation).
- Hibernate lazy loading = virtual **Proxy**.
- Know *why* `Observable` and `Cloneable` were deprecated (recognition must track evolution).
- The same patterns appear in .NET/Python/JS/Go — recognition transfers across ecosystems.
- In interviews, pair every pattern you name with one JDK + one Spring example.

## 19. Quiz
1. `Collections.sort(list, comparator)` is: a) Decorator b) Strategy c) Adapter d) Singleton → **b**
2. `BufferedReader(new FileReader(f))` is: a) Adapter b) Decorator c) Facade d) Iterator → **b**
3. Spring's `@Transactional` is implemented via: a) Decorator b) Proxy (AOP) c) Adapter d) Builder → **b**
4. `Runtime.getRuntime()` is: a) Factory Method b) Singleton c) Prototype d) Strategy → **b**
5. Spring bean default scope = singleton is: a) the GoF singleton b) container-enforced singleton semantics (not GoF) c) a prototype d) an enum → **b**
6. Spring's `ApplicationContext` is primarily a: a) Decorator b) Facade+Factory c) Iterator d) Memento → **b**
7. `JdbcTemplate`'s `doInConnection` callback makes it: a) Strategy b) Template Method c) Observer d) Proxy → **b**
8. Spring's `@EventListener` is: a) Command b) Observer c) Memento d) Flyweight → **b**
9. `Runnable` submitted to an `ExecutorService` is: a) Observer b) Command c) Strategy d) Builder → **b**
10. Which is a virtual proxy in production? a) `Runtime` b) Hibernate lazy-loading associations c) `Comparator` d) `Observable` → **b**

## 20. Flashcards
- **Q: `Collections.sort(list, comparator)` pattern?** → **A:** Strategy (Comparator = Strategy interface).
- **Q: `BufferedReader(new FileReader)` pattern?** → **A:** Decorator (FilterReader = abstract Decorator).
- **Q: `@Transactional` pattern?** → **A:** Proxy (AOP around-advice; NOT Decorator).
- **Q: `Runtime.getRuntime()` pattern?** → **A:** Singleton.
- **Q: Spring bean default scope?** → **A:** Container-enforced singleton (registry), not the GoF pattern.
- **Q: `ApplicationContext` pattern?** → **A:** Facade + Factory.
- **Q: `@EventListener` pattern?** → **A:** Observer.
- **Q: `JdbcTemplate` / `Thread.run()` pattern?** → **A:** Template Method.

## 21. Revision
The JDK and Spring are **pattern museums**, and interviews test recognition. JDK: `Comparator` in `Collections.sort` = **Strategy**; `BufferedReader`/`FilterInputStream` = **Decorator**; `Iterator`/for-each = **Iterator** + **Factory Method** (`iterator()`); `Runtime.getRuntime()` = **Singleton**; `Runnable`/`ExecutorService` = **Command**; `AbstractList`/`Thread.run()` = **Template Method**; `Arrays.asList`/`InputStreamReader` = **Adapter**; `Observable` = **Observer** (deprecated — know why); `StringBuilder`/`HttpClient.Builder` = **Builder**; `clone()` = **Prototype** (discouraged). Spring: `BeanFactory`/`getBean` = **Factory**; default bean scope = **container-enforced singleton** (NOT the GoF pattern — the container enforces it); `@Transactional`/`@Cacheable` = **Proxy** (AOP — and *not* Decorator: it controls the call, it doesn't add object behavior); `ApplicationContext` = **Facade + Factory**; `@EventListener` = **Observer**; `JdbcTemplate`/`RestTemplate` = **Template Method**; `HandlerAdapter` = **Adapter**; `FactoryBean<T>` = **Factory**. Hibernate lazy loading = virtual **Proxy**. Recognition method: interface → implementations → delegator → **intent**. Pair every pattern you name with one JDK + one Spring example.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Which pattern is `Collections.sort(list, comparator)`?" | 8 Example / 13 Q1 |
| "Which pattern is `BufferedReader(...)`?" | 8 Example / 13 Q2 |
| "Is `@Transactional` a Proxy or Decorator?" | 13 Q3 / 18 Cheat Sheet |
| "Is Spring bean singleton the GoF pattern?" | 13 Q6 / 18 Cheat Sheet |
| "Which patterns are in `ApplicationContext`?" | 13 Q5 / 13 Q16 |
| "Where does Spring use Factory / Adapter / Observer / Template?" | 13 Q8 / 13 Q9 / 13 Q12 / 13 Q13 |
| "Why was `Observable` deprecated?" | 13 Q14 / 18 Cheat Sheet |
| "Which pattern is Hibernate lazy loading?" | 13 Q15 / 16 Industry Usage |
| "How to recognize patterns without docs?" | 13 Q20 / 14 Q5 |
| "Which pattern is `Runnable` / `service()`?" | 13 Q10 / 13 Q19 |
