# Functional Programming vs OOP in Java

> **TL;DR**: Java 8+ added lambdas, streams, and method references on top of its OOP core — functional style (declarative pipelines, immutability, higher-order functions) coexists with OOP because every lambda is secretly an object implementing a `@FunctionalInterface`, and streams are just objects whose methods take those function objects.

## 1. Why Does This Exist?
Classic OOP Java (pre-8) was verbose: sorting a list by a field required either a named `Comparator` class or an anonymous inner class — dozens of lines to express "sort by price." Passing behavior around required *objects* because Java's type system is object-centric. Java 8's real motivation: **express behavior as a value**. Lambdas (`(a, b) -> a.price - b.price`) and streams let you chain `filter`/`map`/`reduce` into declarative pipelines. This exists because (1) verbosity hurt productivity, (2) parallel execution is hard to express with imperative loops, (3) functional idioms (immutability, pure functions) are inherently safer to parallelize — and the designers chose to fit these into OOP rather than bolt on a separate type system.

## 2. How Does It Work?
At a glance:
- **Lambda**: an anonymous *function value* `(params) -> body`, compiled to an instance of a functional interface (exactly one abstract method): `Comparator`, `Runnable`, `Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`.
- **Method reference**: `ClassName::method`, `instance::method`, `Type::new` — shorthand for a lambda that just calls a method.
- **`java.util.stream.Stream<T>`**: a lazy, possibly-parallel pipeline of intermediate ops (`filter`, `map`, `flatMap`, `distinct`, `sorted`, `limit`) terminated by a terminal op (`collect`, `reduce`, `forEach`, `count`, `toList`).
- **Optional<T>**: a container for a possibly-absent value; FP-flavored null handling.
- OOP keeps owning the *domain objects and state*; FP provides the *data-processing glue*.

## 3. When Is It Used?
- **Transformation pipelines** — `list.stream().filter(...).map(...).collect(toList())`.
- **Comparators** — `Comparator.comparing(User::getName).thenComparing(User::getAge)`.
- **Collection utilities** — grouping (`groupingBy`), partitioning, summing with `Collectors`.
- **Event/callback handling** — `CompletableFuture.thenApplyAsync(...)`, `Executor.execute(() -> ...)`.
- **Default methods** on interfaces (`List.sort`, `Map.computeIfAbsent`) — interfaces gained behavior, blurring the class/interface boundary.
- **Parallel data processing** — `parallelStream()` for CPU-bound, side-effect-free workloads.

## 4. Why Wasn't Another Approach Chosen?
Alternatives:
- **Anonymous inner classes**: Java 5-7's only way to pass behavior — verbose boilerplate (the "interface ceremony") that obscured intent. Lambdas are *syntax* that lowers to the same object instantiation, so Java added sugar, not a new paradigm.
- **Scala/Kotlin-style functions as first-class citizens**: JVM lambdas are not truly first-class functions; they are *functional-interface instances* — but this preserves binary compatibility and fits the OOP type system. Java deliberately avoided adding a function type (like `Function` with built-in operators) beyond the standard `java.util.function` package.
- **Full FP (immutable-everywhere)**: Java keeps mutable OOP classes as the norm; FP is a *style layer*. Rejected alternatives like records/strict immutability-by-default would have broken backward compatibility.
- **Purely procedural top-level functions**: rejected — Java remains class-based; every function must live in a class or interface context, which is exactly why method references and functional interfaces exist.

## 5. Intuition
Think of OOP as **building a toolbox of workers** (objects, each with skills = methods). FP is **arranging a conveyor belt** (the stream pipeline): you dump parts in one end (`source`), pass them through stations (`filter`, `map`, `sort`), and collect finished products at the end (`collect`). Each station is described as a small *instruction card* (a lambda) rather than a full worker object. The trick that makes both coexist in Java: **an instruction card is itself a worker** — a lambda is just an object implementing a one-method interface, so the conveyor belt (stream) can pass it around like any other object. OOP supplies the stations and parts; FP supplies how the line is configured.

## 6. Real-World Analogy
A **restaurant order line**: classic OOP is each *chef* (object) who "knows how to cook pasta" (method). Functional style is a *ticket* with instructions: "Take order #42, filter out vegetarian-unfriendly items, map each to a course, collect to a bill." The ticket isn't a chef — it's a *description of behavior* (a lambda). The kitchen manages workers as objects, but the flow of dishes is orchestrated by declarative tickets. And the best part: because each ticket only *describes* work, the manager can run two identical ticket lines in parallel (parallelStream) without the chefs tripping over each other — as long as no ticket mutates shared state.

## 7. Formal Definition
- **Lambda expression** (JLS §15.27): an anonymous function: `(formal parameters) -> expression|block`. Its type is the *target type*, which must be a **functional interface**.
- **Functional interface** (JLS §9.8): an interface with exactly one abstract method (excluding `Object` methods and default/static methods), e.g., `@FunctionalInterface Predicate<T> boolean test(T)`, `Function<T,R> R apply(T)`, `Consumer<T> accept(T)`, `Supplier<T> T get()`, `Comparator<T> int compare(T,T)`.
- **Stream** (java.util.stream): "A sequence of elements supporting sequential and parallel aggregate operations." Intermediate ops are lazy; terminal ops are eager and close the pipeline; streams are single-use.
- **Effectively final** (JLS §4.12.4): a variable that is never reassigned — the only local variables a lambda can capture (because lambda instances are objects capturing variables by value at the point of the closure).
- **Optional<T>** (java.util): a value-based container that may be empty; methods `map`, `flatMap`, `orElse`, `orElseGet`, `orElseThrow`.

## 8. Example
Compare imperative vs functional for "find the total price of products in category BOOKS priced over 100, sorted by name":
```java
// Imperative OOP style
long total = 0;
List<Product> matches = new ArrayList<>();
for (Product p : products) {
    if (p.category() == Category.BOOKS && p.priceCents() > 100) matches.add(p);
}
matches.sort((a, b) -> a.name().compareTo(b.name()));   // lambdas even here
for (Product p : matches) total += p.priceCents();
```
```java
// Functional stream style
long total = products.stream()
    .filter(p -> p.category() == Category.BOOKS && p.priceCents() > 100)
    .sorted(Comparator.comparing(Product::name))
    .mapToLong(Product::priceCents)
    .sum();
```
Both produce the same result. The stream version: (1) `stream()` opens the pipeline; (2) `filter` keeps only BOOKS > 100 — lazy, nothing computed yet; (3) `sorted` with a method-reference comparator; (4) `mapToLong` projects prices; (5) `sum()` is terminal — it pulls elements through the stations one at a time.

Step trace for a 3-element list: filter → sorted → mapToLong → sum executes lazily in a single pass; the pipeline is an *object graph*, each op an object with a reference to the next.

## 9. Internal Working
1. **Compile**: `invokedynamic` (bootstrap method `LambdaMetafactory`) — the JVM *dynamically* generates a class implementing the functional interface. First call triggers metafactory; subsequent calls reuse the generated implementation. No anonymous-class classfile is emitted (unlike Java 7).
2. **Capturing**: lambdas capture *effectively final* locals by value (stored as constructor fields of the generated class); non-capturing lambdas (no locals) are compiled to a singleton and reused — no allocation per call.
3. **Streams**: `filter`/`map`/etc. return *new* reference pipeline objects (`ReferencePipeline`), forming a linked list; `sum`/`collect` pull via `Spliterator` (a splittable iterator enabling parallel fork).
4. **Parallel**: `parallelStream()` wraps the pipeline in `ForkJoinPool.commonPool()`: the `Spliterator` splits the source into chunks, each reduced independently, results merged — only safe when operations are stateless and non-interfering.
5. **`Optional`** is a small final class; `map` returns `Optional` of result, `empty()`/`of(value)` factories.

## 10. Time Complexity
- Stream pipeline: same asymptotic cost as the equivalent loop (each op is O(n) per element); but **constant factors** differ — boxing (primitive streams `IntStream` avoid it), spliterator overhead, and one object allocation per op.
- `parallelStream()`: O(n/p) with p ≈ cores *for CPU-bound, independent operations*; **not** a speedup for tiny data, I/O-bound, or shared-state operations (amortized overhead + merge cost).
- Lambda invocation: same cost as an interface method call (virtual dispatch); non-capturing lambdas are a *static singleton* — effectively free.
- `Collectors.groupingBy`/`toMap`: O(n) with hash-based grouping.

## 11. Advantages
- **Expressiveness**: intent is declared, not spelled out (`filter` says *what*, loop says *how*).
- **Parallelism**: correct pipelines are trivially parallelizable (`parallelStream`) — the hard part (splitting, merging) is hidden.
- **Laziness**: intermediate ops don't run until the terminal op, enabling short-circuit (`findFirst`, `anyMatch`) and fusion (single pass).
- **Purity encouragement**: FP style discourages mutable shared state, reducing races and bugs.
- **Less boilerplate**: method references and lambdas shrink anonymous-class noise.

## 12. Disadvantages
- **Abstraction cost**: debugging streams is harder (no obvious variable to inspect); stack traces show synthetic methods.
- **Boxing overhead**: object streams box primitives; must use `IntStream`/`LongStream`/`DoubleStream` for hot paths.
- **Not a cure-all for state**: streams over mutable shared state or with side-effectful lambdas reintroduce races and defeat laziness.
- **Parallelism isn't free**: parallel streams on small data or with blocking ops are *slower* than sequential.
- **Learning curve**: `flatMap`, `reduce`, `Collectors` idioms confuse beginners; overuse hurts readability for teams that think imperatively.
- **Effectively-final capture**: you can't mutate a local counter inside a lambda (must use `int[]`/`AtomicInteger` hacks) — surprising to newcomers.

## 13. Interview Questions
1. **Q: What is a lambda in Java?** A: An anonymous function value that is an instance of a functional interface (an interface with exactly one abstract method); compiled via `invokedynamic`/`LambdaMetafactory`.
2. **Q: What is a functional interface?** A: An interface with exactly one abstract method; can be annotated `@FunctionalInterface` (enforced); `Predicate`, `Function`, `Consumer`, `Supplier`, `Comparator`, `Runnable`.
3. **Q: What's the difference between intermediate and terminal stream operations?** A: Intermediate ops (`filter`, `map`, `sorted`, `limit`) are lazy and return a new stream; terminal ops (`collect`, `sum`, `forEach`, `count`) are eager, trigger execution, and close the stream (single-use).
4. **Q: What does "lazy" mean for streams?** A: Nothing computes until a terminal op; elements flow one-at-a-time through the chain, enabling short-circuiting (`findFirst`, `anyMatch`) and avoiding full intermediate collections.
5. **Q: When is `parallelStream()` faster?** A: For CPU-bound, side-effect-free, independent operations on large data (tens of thousands+ elements) with >1 core; it splits work via `Spliterator` into the common `ForkJoinPool`.
6. **Q: What are the risks of `parallelStream()`?** A: Shared mutable state causes races; I/O or blocking in lambdas stalls the pool; small data loses to merge/scheduling overhead; using the common pool can starve other tasks.
7. **Q: Can a lambda modify a local variable?** A: No — it can only capture *effectively final* variables (never reassigned). Workarounds: mutable holder (`AtomicInteger`, array) — but that's usually a smell.
8. **Q: Method reference vs lambda?** A: A method reference is sugar for a lambda that delegates to a named method: `Product::priceCents` ≡ `p -> p.priceCents()`; `Type::new` ≡ constructor call.
9. **Q: How is a lambda compiled?** A: `invokedynamic` + `LambdaMetafactory` generates the functional-interface class at runtime; non-capturing lambdas are singletons (no per-call allocation).
10. **Q: `Optional` — why and when?** A: Expresses "maybe absent" in the type system, forcing callers to handle absence (`orElse`, `orElseThrow`, `ifPresent`); use it for *return* types that may be empty, not for fields or parameters.
11. **Q: How do you handle checked exceptions in streams?** A: Lambda bodies can't throw checked exceptions; wrap in a helper that translates to `RuntimeException`, or use sneaky-throw (`throwException`), or use a custom collector.
12. **Q: What is `flatMap`?** A: Maps each element to a *stream* and flattens them: `List<List<String>>` → `List<String>`; used for nested collections and for one-to-many expansions.
13. **Q: What is `reduce`?** A: A terminal op that folds the stream to one value using an accumulator: `reduce(0, Integer::sum)`; `map`+`reduce` is the canonical parallelizable pattern.
14. **Q: What are `Collectors.groupingBy`/`partitioningBy`?** A: `groupingBy(classifier)` → `Map<K, List<V>>`; `partitioningBy(pred)` → `Map<Boolean, List<V>>` (two partitions).
15. **Q: Is FP a replacement for OOP in Java?** A: No — Java's functional features live *inside* the OOP type system (lambdas are objects of functional interfaces); domain modeling stays OOP, data processing often becomes functional.
16. **Q: What is a `Spliterator`?** A: A splittable iterator that lets a parallel stream fork the source into chunks; `StreamSupport.stream(spliterator, parallel)`.
17. **Q: What is the difference between `map` and `flatMap`?** A: `map` one-to-one (function returns a value); `flatMap` one-to-many (function returns a `Stream` that gets flattened).
18. **Q: How do primitive streams differ?** A: `IntStream`/`LongStream`/`DoubleStream` avoid boxing and have primitive ops (`sum`, `average`, `range`, `rangeClosed`); `mapToInt` converts.

## 14. Follow-Up Questions
1. **Q: What is stream fusion / short-circuiting?** A: Lazy pipelines chain ops into a single pass; ops like `limit`, `findFirst`, `anyMatch`, `takeWhile` can stop pulling early — O(1) instead of O(n) when the answer appears early.
2. **Q: Why is `forEach` discouraged for transformation?** A: It's a terminal op with side effects — it defeats the pure-pipeline model; prefer `map`/`collect`/`toList` and use `forEach` only for genuine side effects (logging, sinks).
3. **Q: How does `invokedynamic` make lambdas cheap?** A: The metafactory generates the impl class once and caches it; non-capturing lambdas become static singletons — zero per-call allocation, comparable to a direct call.
4. **Q: What's the "effective final" rule really about?** A: Lambda instances outlive the enclosing scope, so captured locals are copied into the object at creation — copying a value that might change later would be inconsistent, hence the compiler forbids reassignment.
5. **Q: Can you reuse a stream?** A: No — streams are single-use; a second terminal op throws `IllegalStateException: stream has already been operated upon or closed`.
6. **Q: What's the downside of the common `ForkJoinPool`?** A: A blocking `parallelStream` lambda occupies a common-pool thread; long-running blocking work can exhaust it and degrade *all* parallel streams in the JVM. Configure a dedicated pool for heavy work.

## 15. Coding Example
```java
import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class FpVsOopDemo {
    record Product(String name, Category cat, long priceCents) {}
    enum Category { BOOKS, TOYS, FOOD }

    public static void main(String[] args) {
        List<Product> products = List.of(
            new Product("Craft", Category.BOOKS, 1500),
            new Product("Moby",  Category.BOOKS, 900),
            new Product("Lego",  Category.TOYS,  5000),
            new Product("Bread", Category.FOOD,  300)
        );

        // Declarative pipeline
        long total = products.stream()
            .filter(p -> p.cat() == Category.BOOKS)       // Predicate<Product>
            .filter(p -> p.priceCents() > 1000)
            .mapToLong(Product::priceCents)               // method reference (long)
            .sum();

        // Grouping + counting: Collector (functional interface too)
        Map<Category, Long> byCat = products.stream()
            .collect(Collectors.groupingBy(Product::cat, Collectors.counting()));

        // Optional: handle absence without NPE
        Optional<Product> cheapest = products.stream().min(Comparator.comparing(Product::priceCents));
        Product fallback = cheapest.orElseThrow(() -> new NoSuchElementException("no products"));

        // Custom functional interface: FP inside OOP
        @FunctionalInterface
        interface Discount { long apply(Product p); }       // exactly one abstract method
        Discount halfOff = p -> p.priceCents() / 2;         // lambda is a Discount object
        long discounted = products.stream().mapToLong(halfOff::apply).sum();

        System.out.println(total + " " + byCat + " " + fallback + " " + discounted);

        // Parallel: only safe if pure (no shared mutable state)
        long parTotal = products.parallelStream()
            .filter(p -> p.cat() == Category.BOOKS)
            .mapToLong(Product::priceCents)
            .sum();
        System.out.println(parTotal);
    }
}
```
```java
// The "stream has already been operated upon" trap
Stream<String> s = List.of("a").stream();
s.count();
// s.count();  // IllegalStateException: stream already operated upon
```

## 16. Industry Usage
- **Spring's functional routing** (`RouterFunction`/`route()`) and `Stream`-based `@Query` projections — functional style at framework boundaries.
- **Apache Spark's Java API** is *literally* `JavaRDD<String>.map/filter/reduce` — distributed stream pipelines; the "map/reduce" paradigm is the industry standard for data engineering.
- **Kafka Streams** exposes `KStream<K,V>.filter/map/groupBy` DSL — production stream processing in a functional/OOP hybrid.
- **CompletableFuture** (`thenApplyAsync`, `thenCompose`) chains async behavior functionally; widely used in JVM microservices.
- **Fluent APIs** (Java Streams, Guava `FluentIterable`, jOOQ, AssertJ) are the dominant modern API style — they're OOP objects arranged with functional chains.
- **Project Reactor / RxJava** (reactive streams) build on functional interfaces for backpressure-driven pipelines at Netflix, LinkedIn, and other large-scale JVM shops.

## 17. References
- Oracle, *The Java Language Specification*, §15.27 "Lambda Expressions", §9.8 "Functional Interfaces", §4.12.4 "Effectively final".
- Oracle, *java.util.stream* and *java.util.function* package docs (docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/stream/package-summary.html).
- JEP 126 (Lambda expressions) / JEP 107 (bulk data operations for Collections).
- Raoul-Gabriel Urma, Mario Fusco, Alan Mycroft, *Java 8 in Action*.
- Venkat Subramaniam, *Functional Programming in Java*.
- Oracle tutorial, "Aggregate Operations / Parallelism" (docs.oracle.com/javase/tutorial/collections/streams/).

## 18. Cheat Sheet
- Lambda = instance of a functional interface (1 abstract method): `(a,b) -> ...`; compiled via `invokedynamic`.
- Core functional interfaces: `Predicate`(test), `Function`(apply), `Consumer`(accept), `Supplier`(get), `Comparator`(compare).
- Stream lifecycle: source → intermediate (lazy) → terminal (eager, single-use).
- Intermediate: filter/map/flatMap/distinct/sorted/limit/peek. Terminal: collect/toList/sum/reduce/count/forEach/anyMatch/findFirst.
- `mapToInt/Long/Double` avoid boxing; `IntStream.range` etc.
- `flatMap` = one-to-many + flatten; `reduce` = fold to one value.
- `Optional`: orElse/orElseGet/orElseThrow/map/ifPresent; return-type only, not fields.
- Captured locals must be *effectively final*.
- `parallelStream()` only for pure, CPU-bound, independent, large data.
- Streams are single-use; `forEach` = side effects (avoid for transforms).

## 19. Quiz
1. A lambda's runtime type is: a) A new function type b) An instance of a functional interface c) `Object` d) A closure class → **b**
2. Which is a functional interface? a) `List` b) `Predicate<T>` c) `HashMap` d) `String` → **b**
3. Which is a terminal operation? a) `filter` b) `map` c) `collect` d) `sorted` → **c**
4. Streams are: a) Reusable b) Single-use c) Always parallel d) Mutable → **b**
5. When is `parallelStream()` a win? a) Tiny lists b) CPU-bound independent large data c) I/O-bound work d) Never → **b**
6. Can a lambda modify a captured local? a) Yes b) Only if `volatile` c) Only if effectively final d) No — capture is restricted to effectively-final vars → **d**
7. Non-capturing lambdas compile to: a) Anonymous classes b) A cached singleton instance c) A method handle only d) Nothing → **b**
8. `flatMap` differs from `map` because it: a) Skips nulls b) Returns a stream that is flattened c) Runs in parallel d) Sorts → **b**
9. Which avoids primitive boxing? a) `Stream<Integer>` b) `IntStream` c) `List<Integer>` d) `Stream<Long>` → **b**
10. `Optional` should primarily be used: a) As a field b) As a return type c) As a parameter d) For collections → **b**

## 20. Flashcards
- **Q: What is a lambda's runtime type?** → **A:** An instance of the target functional interface (exactly one abstract method).
- **Q: Intermediate vs terminal ops?** → **A:** Intermediate = lazy, returns stream; terminal = eager, closes stream.
- **Q: When parallelize?** → **A:** Pure, CPU-bound, independent ops, large data, >1 core.
- **Q: What can lambdas capture?** → **A:** Only effectively-final locals (never reassigned).
- **Q: How are lambdas compiled?** → **A:** invokedynamic + LambdaMetafactory; non-capturing = cached singleton.
- **Q: `map` vs `flatMap`?** → **A:** map one-to-one; flatMap one-to-many + flatten.
- **Q: Can you reuse a stream?** → **A:** No — single-use, second terminal op throws.
- **Q: Where should `Optional` be used?** → **A:** Return types that may be absent, not fields/params.

## 21. Revision
Java's FP features live inside OOP: every lambda is an object implementing a functional interface (1 abstract method) — `Predicate`, `Function`, `Consumer`, `Supplier`, `Comparator` — compiled via `invokedynamic` (non-capturing lambdas are cached singletons). Streams are lazy pipelines: source → intermediate ops (`filter`, `map`, `flatMap`, `sorted`, `limit`) → one eager terminal op (`collect`, `sum`, `reduce`, `count`, `toList`), single-use. Captured locals must be effectively final. Use primitive streams (`IntStream`, `mapToLong`) to avoid boxing. `parallelStream()` splits work via `Spliterator` into the common ForkJoinPool — only for pure, CPU-bound, independent, large workloads; shared mutable state breaks it. OOP models the domain (records, classes); streams transform it. Expect: "lambda vs anonymous class", "lazy vs eager", "when to parallelize", and the "stream already operated" trap.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a lambda and how is it compiled?" | 2 / 9 Internal Working / 13 Interview |
| "What is a functional interface?" | 7 Formal Definition / 13 Interview |
| "Intermediate vs terminal operations?" | 2 / 13 Interview |
| "What does lazy mean for streams?" | 8 Example / 13 Interview |
| "When is `parallelStream()` faster?" | 10 Time Complexity / 13 Interview |
| "Why can't a lambda mutate a local?" | 7 / 13 Interview / 14 Follow-Up |
| "How do you handle checked exceptions in streams?" | 13 Interview |
| "What is `flatMap` / `reduce` / `Collectors`?" | 13 Interview / 15 Coding |
| "FP vs OOP in Java?" | 4 Alternatives / 13 Interview |
| "What's the trap with reusable streams?" | 14 Follow-Up / 15 Coding |
