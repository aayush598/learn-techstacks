# Generics, Collections and OOP

> **TL;DR**: Generics add compile-time type safety to the object-oriented type system via **type erasure** (the JVM sees raw `Object`), while the Collections Framework is OOP made concrete — a hierarchy of interfaces implemented polymorphically, governed by the `equals`/`hashCode`/`Comparable` contracts.

## 1. Why Does This Exist?
Before generics (Java 1.4), collections held `Object` and every `get()` required a cast: `(String) list.get(0)` — cast failures were **runtime** `ClassCastException`s, and wrong-type insertion was unchecked. Generics move that check to **compile time**: `List<String>` can only hold strings, `get()` returns `String` (no cast), and wrong inserts fail to compile. The "why" is type safety without sacrificing one type system: generic type parameters (`<T>`) give you *polymorphism over types* — the same logic works on any type with the compiler verifying consistency, complementing class/interface polymorphism with **parametric polymorphism**.

## 2. How Does It Work?
At a glance:
- Type parameters `<T>`, `<? extends T>` (upper bound), `<? super T>` (lower bound), and unbounded `<?>`.
- **Erasure**: the compiler replaces type parameters with their leftmost bound (or `Object`) in bytecode; `List<String>` and `List<Integer>` are both `List` at runtime — the JVM has NO idea about type arguments.
- **Collections framework**: `Collection` → `List`/`Set`/`Queue` → `ArrayList`, `LinkedList`, `HashSet`, `TreeSet`, `PriorityQueue`, plus `Map` (`HashMap`, `TreeMap`), `Deque`. Interfaces are implemented polymorphically so algorithms work over any concrete collection.
- Contracts: `equals`/`hashCode` for hash-based structures, `Comparable`/`Comparator` for ordering.

## 3. When Is It Used?
- **Typed collections everywhere** — `List<String>`, `Map<String, Integer>`, `Set<UUID>`.
- **Generic utility classes** — `Collections.sort`, `Arrays.asList`, `Optional<T>`, `Stream<T>`.
- **Type-safe custom containers** — `Result<T>`, `Cache<K, V>`, `Pair<A, B>`.
- **Wildcards in API signatures** — `void copy(List<? super T> dst, List<? extends T> src)` (PECS).
- **Comparators** — `Comparator.comparing(User::getName)` builds typed comparators; `TreeSet`/`PriorityQueue`/`Collections.sort` rely on `Comparable`.

## 4. Why Wasn't Another Approach Chosen?
Alternatives:
- **Raw types / `Object` casts (pre-1.5)**: no compile-time safety; rejected.
- **Template reification (C++ templates)**: C++ instantiates a *separate class per type* at compile time (no runtime, no casting), but code bloat, no runtime type info, and slow compiles. Java chose **erasure** so generic and non-generic code share one classfile, binary compatibility is preserved, and `List<String>` and `List<Integer>` are one class — at the cost of no `new T()`, no `T[]`, no `instanceof T`.
- **Reified generics (C#)**: C# keeps type arguments at runtime (via type descriptors), enabling `typeof(T)` — but requires runtime support the JVM/classfile format (designed for erasure) lacks. Java's design is a deliberate trade-off for backward compatibility.
- **Separate collection types per element type**: absurd combinatorics — one hierarchy with generics is the OOP-consistent answer.

## 5. Intuition
Think of generics as **labeled crates**: `List<String>` is a crate labeled "strings only." The *label* (type argument) lives only at the warehouse's check-in desk (compile time). Once the crate is in transit (the running JVM), the label is gone — the crate is just "a List," and the workers (the JVM) only know to fetch `Object`s and hand them to you; the compiler already verified you'll never put a `Integer` in a strings-crate. The Collections framework is the **shelf system**: an interface is the "shelf slot" (`List`), and each concrete class (`ArrayList`, `LinkedList`) is a differently-built shelf that fits the same slot — so a conveyor belt (an algorithm like `sort`) works with any shelf that claims to be a `List`.

## 6. Real-World Analogy
A **valet parking lot with assigned slots**: the valet ticket says "red car slot" (`List<String>`). The attendant who parks (compiler) makes sure only red cars go in that slot. The *garage itself* (JVM) has no idea what color a car is — it just holds cars (`Object`). If you somehow got a ticket for a green car in a red slot, the compiler catches it at check-in. For collections: the parking lot has a *standard gate* (interface `List`) that all garages implement; whether it's an open-air lot (`ArrayList`) or a multi-story ramp structure (`LinkedList`), the same gate procedures (methods) work on both, and you can swap garages without changing your routine (polymorphism).

## 7. Formal Definition
- **Generic type**: "A class or interface is generic if it declares one or more type variables" (JLS §8.1.2). `class Box<T> {}`.
- **Type erasure**: "Type variables are erased when generic types are compiled: they are replaced by the type variable's leftmost bound or `Object`" (JLS §4.6). Bridge methods are generated to preserve overriding when erasure changes signatures.
- **Wildcards**: `? extends T` (covariant read-only source), `? super T` (contravariant write-capable sink), `?` (unknown). PECS: **Producer Extends, Consumer Super**.
- **Contracts**: `equals` defines logical equality; `hashCode` (equal objects ⇒ equal hashes) governs hash buckets; `Comparable<T>.compareTo` defines natural ordering (consistent with equals is required for `TreeSet`/`TreeMap` correctness).
- **Collections framework**: interfaces (`Collection`, `List`, `Set`, `Queue`, `Deque`, `Map`) + concrete implementations + algorithms (`Collections`, `Arrays`) — the canonical application of OOP (interface inheritance + polymorphism) at JDK scale.

## 8. Example
Trace `List<String>`:
```java
List<String> words = new ArrayList<>();
words.add("java");                      // ok
// words.add(42);                       // COMPILE ERROR: int not String
String w = words.get(0);                // no cast needed
```
What the compiler produces (erasure): `words.add` becomes `((List) words).add("java")`; `String w = (String) ((List) words).get(0)` — the compiler inserts the cast. At runtime, `words.getClass()` is `ArrayList.class`; there is no `List<String>.class` — `List<String>` and `List<Integer>` are the **same** class.

Example of the erasure trap (the interview classic):
```java
public class Container {
    public static void main(String[] args) {
        List<String> a = new ArrayList<>();
        List<Integer> b = new ArrayList<>();
        System.out.println(a.getClass() == b.getClass());   // true — both ArrayList.class
        // a.add(1);  // compile error — but this WORKS at runtime via reflection:
        ((List) a).add(1);                                  // reflection erases checks entirely
        Object o = ((List) a).get(0);                       // it's an Integer now!
    }
}
```

Example — PECS in action:
```java
public static <T> void copy(List<? super T> dst, List<? extends T> src) {
    for (T item : src) dst.add(item);   // read from extends (producer), write to super (consumer)
}
```

## 9. Internal Working
1. **Compile**: type-checking against declared bounds; erasure replaces `T` with leftmost bound; the compiler inserts casts at usage sites and **bridge methods** where erasure would break overriding (e.g., `Comparable<String>`).
2. **Bytecode**: generic types appear as `Ljava/util/List;` with no signature info in most places (a `Signature` attribute may exist for reflection but the JVM does not enforce it).
3. **Runtime**: `getClass()`/`instanceof`/casts are all raw; the only enforcement is the implicit cast inserted by the compiler, which throws `ClassCastException` if the erased contents violate expectations (e.g., the reflection trick above).
4. **Collections internals**:
   - `HashMap` buckets = `Node<K,V>[]`; `hashCode` → bucket, `equals` → resolve collisions.
   - `TreeSet`/`TreeMap` use `compareTo` (natural order) for a red-black tree; `HashSet` uses equals+hashCode.
   - `PriorityQueue` = binary heap using `Comparable`/`Comparator`.
5. **`equals`/`hashCode` contract**: equal objects MUST have equal hashes; breaking it means objects land in wrong buckets → lookups fail silently.

## 10. Time Complexity
- `ArrayList.get` O(1); `add` amortized O(1); `contains`/`indexOf` O(n); `add(i, v)`/`remove` O(n).
- `LinkedList.get(i)` O(n); `add/remove` at ends O(1).
- `HashMap` get/put O(1) average (O(n) worst on heavy collision); `TreeMap` O(log n); `HashSet` O(1) average.
- `PriorityQueue` add/remove O(log n).
- `Collections.sort` (TimSort) O(n log n).
- Erasure adds zero runtime cost for normal generics (casts are free modulo `checkcast`).

## 11. Advantages
- Compile-time type safety: no accidental `ClassCastException` from collections.
- No explicit casts in client code (less noise, fewer errors).
- Generic algorithms/utilities reusable across all types (parametric polymorphism).
- Wildcards express read-only vs write-only intent precisely (PECS).
- Collections + contracts give consistent OOP design: interfaces define behavior, implementations supply performance/behavior trade-offs, and swapping implementations doesn't change callers (Open/Closed Principle at framework scale).

## 12. Disadvantages
- Erasure means no runtime type info: `new T()`, `new T[]`, `instanceof T`, and `Class<T>` literals are illegal — need `Class<T>` + reflection hacks.
- `List<String>` and `List<Integer>` are indistinguishable at runtime → generic information is lost to reflection.
- Raw types remain for compatibility (unchecked warnings), which quietly bypass safety.
- Wildcards complicate signatures; PECS is a memorization point and a source of `capture of ?` errors.
- Arrays and generics don't mix (`new List<String>[10]` is illegal) — a recurring interview gotcha.

## 13. Interview Questions
1. **Q: What is type erasure?** A: The compiler replaces type parameters with their bounds (or `Object`) at compile time; the JVM sees only raw types, so `List<String>` and `List<Integer>` are the same `List` at runtime.
2. **Q: Why can't you do `new T()` in a generic method?** A: Because `T` is erased to its bound; there's no class information at runtime to instantiate. Pass `Class<T>` and use reflection if you must.
3. **Q: What is a wildcard and why use it?** A: `?` denotes an unknown type; `? extends T` / `? super T` bound it. They let methods accept collections of *subtypes* (covariance) or write into collections of *supertypes* (contravariance), which plain `T` can't express.
4. **Q: What is PECS?** A: Producer Extends, Consumer Super: if a method *reads* from a collection (producer), use `? extends T`; if it *writes* (consumer), use `? super T`.
5. **Q: Can you put an `Integer` into a `List<String>`?** A: Not via typed code (compile error), but via reflection/raw types yes — erasure means the runtime has no check; you'd get `ClassCastException` when the implicit cast at `get` fails.
6. **Q: Why does overriding `equals` force overriding `hashCode`?** A: The contract: equal objects must have equal hashes. `HashMap` buckets by `hashCode`, so unequal hashes for equal objects make `contains`/`get` fail even though `equals` says they're equal.
7. **Q: What's the `equals`/`hashCode` contract and its failure mode?** A: Contract: reflexivity, symmetry, transitivity, consistency, and equal-objects⇒equal-hash. Failure: objects equal by `equals` land in different buckets → lookups silently return null.
8. **Q: `ArrayList` vs `LinkedList`?** A: `ArrayList` = dynamic array: O(1) get, O(n) middle insert, cache-friendly, compact. `LinkedList` = doubly linked: O(n) get, O(1) end insert/remove, larger per-node overhead; rarely preferred.
9. **Q: How does `HashMap` work internally?** A: Array of `Node` buckets; key's `hashCode` → bucket index; `equals` resolves collisions (chain, then tree when a bucket > 8 and array > 64); resize at 0.75 load factor, rehash into a doubled array.
10. **Q: What is `ConcurrentHashMap` vs `HashMap`?** A: `HashMap` is not thread-safe; `ConcurrentHashMap` (Java 8+) uses CAS on bins + synchronized on bin heads for high concurrency, with no global lock (no null keys/values).
11. **Q: `Comparable` vs `Comparator`?** A: `Comparable<T>` = natural ordering inside the class (`compareTo`, e.g., `Integer`, `String`); `Comparator<T>` = external ordering object passed to `sort`/`TreeSet`, enabling multiple orderings without touching the class.
12. **Q: Why can't you create a generic array `new T[]`?** A: Arrays are *reified* (runtime-checked) but generics are *erased*; `new T[]` would create an array whose element type is unknown at runtime, breaking array store checks. Use `ArrayList<T>` instead.
13. **Q: What is an unbounded wildcard `List<?>` and what can you add?** A: A list of *some* unknown type; you can't add anything except `null` (type unknown) but can read as `Object` — often used for read-only parameters.
14. **Q: What are bridge methods?** A: Synthetic methods the compiler generates when erasure would change a signature, preserving polymorphism for overriding (e.g., `Comparable.compareTo(Object)` bridging to `compareTo(String)`).
15. **Q: What is the difference between `Set`, `List`, and `Queue`?** A: `List` = ordered, allows duplicates, index access; `Set` = no duplicates (equality-based), `HashSet` unordered / `TreeSet` sorted / `LinkedHashSet` insertion-ordered; `Queue`/`Deque` = ordering discipline (FIFO/priority/LIFO).
16. **Q: What is `TreeSet`'s ordering requirement?** A: Elements must be `Comparable` or you must supply a `Comparator`; and `compareTo` should be consistent with `equals` or the set behaves oddly (may exclude objects equal by equals).
17. **Q: What are the consequences of a mutable `hashCode` key in a map?** A: The key's bucket becomes wrong after mutation → the entry is "lost" to lookups; only the old bucket holds it. Use immutable keys.
18. **Q: What is `ClassCastException` and where does it actually come from in generic code?** A: The compiler-inserted `checkcast` at usage sites (e.g., `get()`); erasure means the JVM checks the *cast*, not the add — the check happens when you read with a typed variable.

## 14. Follow-Up Questions
1. **Q: What is the `capture of ?` error?** A: `List<?>` has a *fresh type variable* per use; passing `? extends T` to a method expecting `? super U` fails because the compiler can't prove the capture relationship — resolve by widening to `?`/`Object` or a generic method `<T>`.
2. **Q: How does `Collections.sort` know how to sort a `List<String>`?** A: It requires `T extends Comparable<? super T>` — the bounded type parameter — and uses the element's natural ordering via a generic `sort(List<T>)`.
3. **Q: Why is `HashMap`'s worst case O(n)?** A: If many keys hash to the same bucket and are unequal, the bucket becomes a long chain (linked list); Java 8 converts chains > 8 to red-black trees when the table is ≥ 64 bins, improving worst case to O(log n).
4. **Q: What's the `hashCode`-generation rule for a class?** A: Use a stable subset of significant fields: `result = 31 * result + field.hashCode()` — 31 chosen as an odd prime for good distribution (Effective Java Item 11).
5. **Q: Why does `equals` also need type checks (`instanceof`) and a `null` check?** A: To be symmetric: `a.equals(b)` must equal `b.equals(a)`; `getClass`-based or `instanceof`-based checks both preserve the contract, but `instanceof` is the recommended approach for non-final hierarchies (with caveats).

## 15. Coding Example
```java
import java.util.*;
import java.util.stream.*;

public class GenericsCollectionsDemo {
    // Generic container: parametric polymorphism
    static class Result<T> {
        private final T value;
        private final boolean ok;
        private Result(T value, boolean ok) { this.value = value; this.ok = ok; }
        static <T> Result<T> success(T v) { return new Result<>(v, true); }
        static <T> Result<T> failure() { return new Result<>(null, false); }
        boolean ok() { return ok; }
        T value() { return value; }   // compiler inserts a cast to T on callers
    }

    // PECS: Producer Extends, Consumer Super
    static <T> void copyInto(List<? super T> dst, List<? extends T> src) {
        for (T item : src) dst.add(item);
    }

    // equals/hashCode/Comparable done right
    static final class Product implements Comparable<Product> {
        private final String id;
        private final long priceCents;
        Product(String id, long priceCents) { this.id = id; this.priceCents = priceCents; }

        @Override public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Product p)) return false;      // pattern matching instanceof
            return id.equals(p.id) && priceCents == p.priceCents;
        }
        @Override public int hashCode() {
            return Objects.hash(id, priceCents);
        }
        @Override public int compareTo(Product o) {           // natural ordering
            return Long.compare(this.priceCents, o.priceCents);
        }
        @Override public String toString() { return id + "@" + priceCents; }
    }

    public static void main(String[] args) {
        Map<String, Product> byId = new HashMap<>();          // keyed by immutable String
        byId.put("p1", new Product("p1", 500));

        List<Product> products = List.of(new Product("p2", 200), new Product("p1", 500));
        // typed stream pipeline: FP over OOP types
        long total = products.stream().filter(p -> p.priceCents > 100)
                                      .mapToLong(Product::priceCents)
                                      .sum();

        TreeSet<Product> byPrice = new TreeSet<>(products);   // uses compareTo
        // multiple orderings with Comparator without touching the class:
        products.stream().sorted(Comparator.comparing(Product::toString)).forEach(System.out::println);

        // PECS demo
        List<Object> dst = new ArrayList<>();
        List<String> src = List.of("a", "b");
        copyInto(dst, src);                                   // dst accepts Object (super of String)
        System.out.println(dst);
    }
}
```

## 16. Industry Usage
- **Every Spring/JPA/Spring Data repository** uses generic `CrudRepository<T, ID>` and `Page<T>` — the framework is a textbook of bounded generics and wildcards.
- **Guava** (`ImmutableList`, `Multimap`, `Table`), Vavr, and Apache Commons use generics heavily; `Collectors`/`Stream<T>` are JDK staples in every service.
- **Kafka/Spark/Pulsar** typed APIs (`Producer<K,V>`, `KStream<String, Row>`) rely on generic contracts.
- **Microservice DTO mapping** (MapStruct, Jackson) generates type-safe mappers parameterized by source/target types.
- **Effective Java** is the canonical style guide at JVM-heavy companies; type-safe heterogenous containers (`Class<T>` keys) are an advanced pattern interviewers love.

## 17. References
- Oracle, *The Java Language Specification*, §4.5 "Parameterized Types", §4.6 "Type Erasure", §8.1.2 "Generic Classes and Interfaces".
- Oracle tutorial, "Generics" (docs.oracle.com/javase/tutorial/java/generics/) and "The Collections Framework".
- Joshua Bloch, *Effective Java (3rd ed.)*, Items 26-33 (generics), 11-12 (equals/hashCode), 14 (Comparable), 57-68 (collections).
- Maurice Naftalin & Philip Wadler, *Java Generics and Collections*.
- Angelika Langer, *Java Generics FAQ* (angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html) — the definitive reference.
- Brian Goetz, *Java Concurrency in Practice*, ch. 5 (thread-safe collections).

## 18. Cheat Sheet
- Erasure: `T` → leftmost bound/`Object`; `List<String>` ≡ `List<Integer>` at runtime; compiler inserts casts + bridge methods.
- No `new T()`, no `new T[]`, no `instanceof T`; arrays + generics don't mix.
- PECS: `? extends T` = producer (read), `? super T` = consumer (write), `?` = unknown (read-only).
- Collections: `List` ordered/dupes/idx; `Set` unique (Hash/Tree/Linked); `Map` key-value; `Queue`/`Deque` discipline.
- Complexity: `ArrayList.get` O(1); `HashMap` O(1) avg; `TreeMap`/`PriorityQueue` O(log n); `sort` O(n log n).
- `equals`+`hashCode`: equal ⇒ equal hash; break it → `HashMap` lookups fail.
- `Comparable` = natural order inside class; `Comparator` = external order; `TreeSet` needs one.
- `HashMap`: buckets by hashCode, equals resolves collisions, 0.75 load factor, bin→tree at 8.
- `ConcurrentHashMap`: no global lock, CAS + per-bin locks.
- Mutable keys in maps = silent "lost" entries — use immutable keys.

## 19. Quiz
1. `List<String>` and `List<Integer>` at runtime are: a) Different classes b) The same raw `List` c) Compile error d) Arrays → **b**
2. Which is legal in a generic class `class Box<T>`? a) `new T()` b) `new T[5]` c) `T t = null;` d) `t instanceof T` → **c**
3. PECS means: a) Producers are Super b) Producer Extends, Consumer Super c) Everything extends d) Consumers are Extends → **b**
4. What can you safely do with `List<?>`? a) `add("x")` b) `add(null)` c) `add(42)` d) `add(list.get(0))` → **b** (null is the only addable element; reading yields `Object`)
5. Equal objects with unequal hashes in a `HashMap` cause: a) Slower only b) Lookups to miss c) Compile error d) Nothing → **b**
6. `ArrayList` vs `LinkedList` — which has O(1) `get(i)`? a) ArrayList b) LinkedList c) Both d) Neither → **a**
7. `HashMap` get average time: a) O(1) b) O(log n) c) O(n) d) O(n²) → **a**
8. Which expresses "read-only source of T-subtypes"? a) `List<? super T>` b) `List<? extends T>` c) `List<T>` d) `List<Object>` → **b**
9. `TreeSet` requires elements to be: a) `Serializable` b) `Comparable` or have a `Comparator` c) `Cloneable` d) `final` → **b**
10. Where does the `ClassCastException` come from in generic code? a) `add()` b) The compiler-inserted cast at `get()` c) GC d) `hashCode` → **b**

## 20. Flashcards
- **Q: What is type erasure?** → **A:** Compiler replaces `T` with its bound at compile time; runtime sees raw types only.
- **Q: What can't you do with erased `T`?** → **A:** `new T()`, `new T[]`, `instanceof T`; pass `Class<T>` instead.
- **Q: What is PECS?** → **A:** Producer Extends (read), Consumer Super (write).
- **Q: What breaks when `equals`/`hashCode` disagree?** → **A:** Hash-based lookups miss (equal objects in different buckets).
- **Q: `Comparable` vs `Comparator`?** → **A:** Natural order inside class vs external ordering object.
- **Q: How does `HashMap` work?** → **A:** hash → bucket, equals resolves collisions, load factor 0.75, chains→trees.
- **Q: Why no generic arrays?** → **A:** Arrays are runtime-checked (reified); generics are erased — incompatible.
- **Q: What are bridge methods?** → **A:** Synthetic methods preserving overriding after erasure.
- **Q: When do you use `? super T`?** → **A:** When writing into a collection of T-or-supertype.

## 21. Revision
Generics = compile-time type safety via erasure: `T` is replaced by its bound, casts are inserted by the compiler, and the JVM sees only raw types — so `new T()` is illegal and `List<String>` ≡ `List<Integer>` at runtime. Wildcards express variance: `? extends T` reads (producer), `? super T` writes (consumer), PECS. Collections = interface hierarchy implemented polymorphically: `ArrayList` O(1) get / `LinkedList` O(n) get, `HashMap` O(1) via hash→bucket with equals collisions (bin→tree at 8, load 0.75), `TreeSet` O(log n) via Comparable/Comparator, `PriorityQueue` O(log n). The `equals`+`hashCode` contract (equal ⇒ equal hash) governs correctness of hash-based structures; mutable keys break maps. `Comparable` = natural order, `Comparator` = external order. Bridge methods and implicit `checkcast` explain why `ClassCastException` appears at `get` even though `add` compiled. Expect the erasure-reflection trick and PECS in interviews.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is type erasure?" | 2 / 7 / 8 Example |
| "Why can't you `new T()`?" | 12 Disadvantages / 13 Interview |
| "What are wildcards and PECS?" | 4 Alternatives / 8 Example / 13 Interview |
| "How does `HashMap` work internally?" | 9 Internal Working / 13 Interview |
| "Why override `equals` and `hashCode` together?" | 7 Formal Definition / 13 Interview |
| "`ArrayList` vs `LinkedList`?" | 10 Time Complexity / 13 Interview |
| "`Comparable` vs `Comparator`?" | 13 Interview / 15 Coding |
| "Why don't arrays and generics mix?" | 12 Disadvantages / 13 Interview |
| "Where does `ClassCastException` come from?" | 8 Example / 13 Interview |
| "What are bridge methods?" | 9 Internal Working / 13 Interview |
