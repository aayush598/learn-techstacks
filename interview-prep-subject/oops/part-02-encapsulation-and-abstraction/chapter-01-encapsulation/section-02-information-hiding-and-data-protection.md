# Information Hiding and Data Protection

> **TL;DR**: Information hiding (Parnas, 1972) is the principle that a module should hide the design decisions most likely to change behind a stable interface — encapsulation is the language mechanism that implements it, and data protection is its payoff in invariants, security, and evolution safety.

## 1. Why Does This Exist?
Information hiding exists because **change is the constant**: the storage format of a price, the algorithm of a sort, the collection behind a cache — all are details that will *change* during a system's life. If those details leak into other modules, every change ripples across the codebase ("shotgun surgery"): one schema change breaks twenty callers. Parnas proved in 1972 that decomposing a system into modules that hide *one changeable design decision each* makes changes local and cheap. Data protection is the security/robustness half: without hiding, invariants (never negative, never null, never > MAX) can be violated by any caller, and sensitive data can be read by anyone. Together they answer the interview favorite: "Why do we hide data, and what exactly do we hide?"

## 2. How Does It Work?
1. Identify the **design decisions most likely to change** (representation, algorithm, I/O format, policy).
2. Hide each behind a **stable interface** — expose only what callers need (methods), keep the rest private.
3. Enforce with language mechanisms: `private`/package-private (Java), `_`/`__` (Python), opaque structs (C), modules (Java 9 `module-info`).
4. **Protect data** three ways: validation at every write (reject bad values), immutable state (no writes at all), and safe reads (copies/unmodifiable views so callers can't mutate what they read).

The mechanism is "interface stable, implementation free": the callers' contract is fixed; everything else is a private implementation detail you can swap.

## 3. When Is It Used?
- **Representation hiding**: `BigDecimal` inside a money class, `HashMap` inside a cache, `byte[]` inside a hashing utility — callers never see the storage.
- **Algorithm hiding**: sort orders, search strategies, compression — callers call `sort()`; the algorithm is private.
- **I/O / transport hiding**: JDBC drivers hide the wire protocol; HTTP clients hide sockets.
- **Data protection**: passwords/keys stored private; balances validated; caches unmodifiable.
- **Evolvable libraries**: the JDK hides ArrayList's array growth policy so it can change in new JDKs.
- **Modules/packages**: Java 9 modules hide whole packages (`module-info`), extending hiding to deployment units.

## 4. Why Wasn't Another Approach Chosen?
- *Why not "global data + conventions"?* Because conventions don't scale: one forgetful caller breaks the invariant and the bug is far from its cause. Hiding chosen because the *compiler* enforces, not the README.
- *Why not make everything public and let the community "be careful"?* Public internals become de-facto API: you can never change them (the "internal API trap" — JDK suffered this pre-Java 9, forcing `sun.*` hacks). Hiding chosen to keep the freedom to change.
- *Why not hide nothing but provide thorough docs?* Docs describe *current* behavior; hiding enforces the *contract* and gives future freedom. Both are used; hiding is the load-bearing one.
- *Why not just copy on every access (protect by copying)?* Copies protect against mutation but cost O(n) and don't enforce invariants on writes; the chosen design is validation at write + safe reads + immutability where feasible — a mix that protects without copying everything.

## 5. Intuition
Think of a **house**: information hiding says "the electrical wiring, plumbing, and foundation are decisions you, the builder, will change; so hide them behind walls." The *interface* is the light switch, the tap, the front door. When you rewire the house, you only touch the walls, not every room's furniture. Data protection says "the wall also stops people from touching the live wire" — the same wall that gives you freedom to change also gives you safety from misuse.

## 6. Real-World Analogy
A **restaurant kitchen vs the dining room**. The menu is the stable interface (what you can ask for); the kitchen — its ingredients, recipes, equipment — is the hidden implementation. The chef can switch suppliers, change the recipe, even swap the oven, and diners are unaffected (information hiding: the change is contained). And diners can't walk into the kitchen and alter the ingredients (data protection: the kitchen is off-limits, so the food's quality — the invariant — is preserved). The menu that never changes, the kitchen that freely changes: that's the whole principle.

## 7. Formal Definition
**Information hiding** (Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules," 1972): a system should be decomposed into modules such that each module conceals a single design decision that is most likely to change; the module's interface is the only externally visible part, so the decision can be changed by modifying only that module. **Data protection** is the application of information hiding to mutable state: restricting who can read or write fields (access control), validating every write to preserve invariants, and providing mutation-safe reads (copies/unmodifiable views), with immutability as the strongest form.

## 8. Example
A `Cache` that hides its storage and algorithm:
```java
public final class Cache<K, V> {
    private final Map<K, V> storage;          // hidden: LinkedHashMap (LRU), could become ConcurrentHashMap
    private final int capacity;

    public Cache(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity <= 0");
        this.capacity = capacity;
        this.storage = new LinkedHashMap<>() {   // hidden implementation detail
            @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > capacity;        // hidden eviction policy
            }
        };
    }
    public V get(K key) {
        V v = storage.get(key);                 // hidden: could add TTL, logging, metrics here
        return v;
    }
    public void put(K key, V value) {
        if (value == null) throw new NullPointerException("value");
        storage.put(key, value);                // hidden: write-through, async write, etc.
    }
    public int size() { return storage.size(); }
    // NOTE: no accessor exposes `storage` itself
}
```
The caller sees `get`/`put`/`size` — a stable contract. The storage type, eviction policy, null rules, and any future TTL are private decisions the maintainer can change without breaking a single caller. That's information hiding + data protection in production shape.

## 9. Internal Working
1. **Design time**: the module's public API is chosen to be *stable* (what callers need); the private members are everything else (fields, helpers, constants).
2. **Compile time**: `private` fields reject external bytecode; `package-private` shields within a package; module files hide packages.
3. **Write path**: `put()` validates (null check, capacity), enforces policy (eviction), then mutates the hidden `storage`. External code physically cannot reach `storage` — it can only call `put`.
4. **Read path**: `get()` returns values; for collections, the getter returns unmodifiable views or copies — so reading cannot become writing.
5. **Change path**: the maintainer edits only `Cache.java` — replace `LinkedHashMap` with a `ConcurrentHashMap`, add TTL — recompile, ship; callers' source doesn't change.
6. **Audit path**: because all mutation goes through `put`, you can add logging/metrics in one place.

## 10. Time Complexity
- Hiding itself: zero runtime cost (compile/verify time).
- Validated writes: O(1) + validation.
- Unmodifiable view read: O(1) (wrapper).
- Defensive copy read: O(n) for a collection of n — the explicit cost you trade for safety.
- Immutability: O(1) after construction (no mutation paths at all).
- Hidden eviction (LinkedHashMap LRU): O(1) per put amortized.

## 11. Advantages
- **Change localization**: swap representation/algorithm without touching callers (the biggest maintenance win).
- **Invariant protection**: writes go through validated gates; bad states are impossible.
- **Security**: sensitive data isn't reachable by arbitrary code.
- **Small API surface**: fewer methods to learn, document, test, and break.
- **Independent testing/ownership**: a module can be developed and tested in isolation.
- **Fits SOLID**: SRP (one change reason), OCP (extend without modifying), DIP (depend on the hidden abstraction).

## 12. Disadvantages
- **Extra indirection**: hidden state sometimes forces accessor calls (usually inlined).
- **Over-hiding**: hiding trivial, stable details (a getter for a pair of constants) adds ceremony without benefit.
- **Hides bad design**: a clean interface can conceal a tangled implementation (you fix the interface, not the problem).
- **Access friction**: internal teams sometimes need package-private/reflection to do legitimate work — a sign the hiding granularity is wrong.
- **Testing**: internal states that matter for testing (cache hit counts) become hard to inspect without test hooks or reflection.

## 13. Interview Questions
1. **Q: What is information hiding?** A: Parnas's principle: each module hides the design decisions most likely to change behind a stable interface, so a change touches only that module. Encapsulation is the language mechanism that implements it.
2. **Q: What's the difference between encapsulation and information hiding?** A: Encapsulation is the *mechanism* (bundle data + methods, restrict access); information hiding is the *principle* (hide changeable design decisions). Encapsulation serves information hiding; a class can encapsulate without effectively hiding the right things.
3. **Q: TRICKY — What exactly should you hide?** A: Design decisions likely to change: storage representation, algorithm, I/O format, policy rules, physical resources (sockets, files). You should *expose* stable contracts: what the module does, not how.
4. **Q: Give an example where hiding paid off.** A: JDBC: the interface (`Connection`, `PreparedStatement`) is stable, but drivers (MySQL, Postgres, Oracle) each hide different wire protocols — you can swap databases by changing a driver, not your code.
5. **Q: PRACTICAL — How do you protect a private `Map` from being mutated via its getter?** A: Return `Collections.unmodifiableMap(map)` (O(1) view — mutation throws) or a shallow copy. Never return the map itself. Do the same for lists/sets.
6. **Q: SCENARIO — Your `User` class must expose `email` but prevent it ever becoming null/invalid.** A: Private field + validated setter (`if (!email.contains("@")) throw`) + constructor that runs the same validation; no way to set it outside the class. Read via getter (String is immutable — safe).
7. **Q: TRICKY — Is a private field with a trivial getter/setter "information hiding"?** A: Mechanically yes (access control), but it hides *nothing of value* — it's a public field in disguise. Good information hiding conceals *changeable decisions*, not just any data.
8. **Q: How does immutability relate to data protection?** A: It's the strongest form: no mutation methods at all, so no validation is ever bypassed and reads are always safe. `String`, `BigDecimal`, `LocalDate`, and records are the canonical examples.
9. **Q: PRODUCTION — Why did Java introduce modules (Java 9)?** A: To extend hiding to whole packages — `module-info` exports only chosen packages, so internal `sun.*` packages can no longer be imported. It's information hiding at deployment scale.
10. **Q: What is the "internal API trap"?** A: When internal details get used by outsiders, they become de-facto public API and can never change — the reason to hide internals *before* they're exposed (see `sun.misc.Unsafe` history).
11. **Q: SCENARIO — A payment library must keep its signing algorithm secret-ish and its balance integrity solid.** A: Algorithm in `private` methods/classes; balance `private final` (or validated); public surface = `sign(bytes)` and `verify(bytes, sig)`; raw key material never exposed; secrets never logged or serialized.
12. **Q: When is hiding the *wrong* choice?** A: When the "hidden" detail is actually the product (an open algorithm), when callers legitimately need the detail (plugin points), or when over-hiding creates unmaintainable indirection. Hide what changes, not what is.
13. **Q: PRACTICAL — What does `Collections.unmodifiableList` cost vs a copy?** A: The view is O(1) and reflects later changes (both good and bad — it's a *view*); the copy is O(n) and independent. Choose view for brevity/safety, copy when the caller outlives the source or must be isolated.
14. **Q: TRICKY — Can reflection defeat information hiding?** A: Yes — `setAccessible(true)` reads/writes private members; frameworks (Spring, Hibernate) do this deliberately. That's why constructor injection (no reflection on fields) is preferred: it respects hiding by design.
15. **Q: PRODUCTION — How do you evolve a library without breaking clients?** A: Keep the public interface stable; hide everything else; add capabilities via new methods/overloads (never change signatures); deprecate before removing. Hiding is what *allows* this evolution.

## 14. Follow-Up Questions
1. **Q: What is the difference between a "stable interface" and a "contract"?** A: Same idea, different emphasis: an interface is the *shape* (method signatures); a contract adds *semantics* (preconditions/postconditions, invariants) — design-by-contract (Meyer) says the interface promises behavior, not just signature.
2. **Q: How does Parnas's decomposition criterion apply to SOLID?** A: SRP ≈ one changeable decision per module (Parnas); OCP ≈ extend via the stable interface without modifying it; both are direct descendants of information hiding.
3. **Q: What is "white-box vs black-box" reuse?** A: White-box = subclasses see/use parent internals (information leaks); black-box = composition via public API (hiding preserved). Prefer black-box — it's the composition-over-inheritance argument.
4. **Q: Can hiding be too strict in a monorepo?** A: Yes — within one team, excessive package-private/private forces duplicate logic or reflection; hide at *package/module* boundaries and relax inside the team, keeping the external API strict.

## 15. Coding Example
A fully-protected, information-hiding `Temperature`:
```java
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;

public final class Temperature {
    private final double celsius;            // hidden representation
    private final List<Double> history = new ArrayList<>();

    private Temperature(double celsius) { this.celsius = celsius; }   // private ctor: controlled creation

    public static Temperature ofCelsius(double c) {
        if (c < -273.15) throw new IllegalArgumentException("below absolute zero");
        Temperature t = new Temperature(c);
        t.history.add(c);
        return t;
    }
    public double inCelsius() { return celsius; }       // stable contract
    public double inFahrenheit() { return celsius * 9.0 / 5.0 + 32; }
    public List<Double> getHistory() { return Collections.unmodifiableList(history); }  // safe read

    public static void main(String[] args) {
        Temperature t = Temperature.ofCelsius(25);
        System.out.println(t.inFahrenheit());          // 77.0
        try { t.getHistory().add(999); } catch (UnsupportedOperationException e) {
            System.out.println("history protected");   // protected!
        }
    }
}
```
Representation (`celsius`), construction policy (private ctor + factory), and history storage are hidden; the contract (`ofCelsius`, `inCelsius`, `inFahrenheit`) is stable. Changing `celsius` to `kelvin` internally would not affect callers at all.

## 16. Industry Usage
- **JDK**: every class hides its internals (`HashMap` buckets, `String`'s `byte[]`); Java 9 modules hide whole packages.
- **JDBC drivers**: stable `java.sql` interface, hidden wire protocols — swapping Postgres↔MySQL is a driver swap.
- **Spring**: `@Repository`/`@Service` hide data access; interfaces stable, implementations private.
- **Guava's ImmutableList**: immutable + unmodifiable views — data protection as a product.
- **Linux kernel**: opaque structs + accessor functions; `struct file` internals are deliberately hidden from drivers.
- **Microservice boundaries**: REST/GraphQL contracts are "stable interfaces"; the service's internals (DB schema, caching) are hidden — information hiding scaled to systems.

## 17. References
- David L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules," *Communications of the ACM*, 1972.
- Joshua Bloch, *Effective Java* — Items 15–17, and Item 10–12 (equals/toString discipline = contract).
- Bertrand Meyer, *Object-Oriented Software Construction* — design by contract.
- Joel Spolsky, "The Law of Leaky Abstractions," 2002.
- Oracle, "The Java Module System" (Java 9): https://docs.oracle.com/javase/9/core/java-se-9-module-system.htm
- Java Tutorials, "Encapsulation / Access Control": https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html

## 18. Cheat Sheet
- Information hiding = hide changeable design decisions behind a stable interface (Parnas, 1972).
- Encapsulation = the mechanism; information hiding = the principle.
- Hide: representation, algorithm, I/O format, policy, resources. Expose: stable contract.
- Protect writes: validated setters. Protect reads: unmodifiable views / copies.
- Strongest protection: immutability.
- Public internals = permanent API (the trap).
- Modules (Java 9) hide whole packages.
- Constructor injection respects hiding; field-injection reflection bypasses it.

## 19. Quiz
1. Information hiding was formalized by: a) Bloch b) Parnas c) Gamma d) Meyer → **b**
2. Which should you hide? a) public contract b) storage representation c) method names d) class name → **b**
3. Safest getter for a `List` field: a) return it b) unmodifiable view c) make it public d) return null → **b**
4. Strongest form of data protection: a) getters b) private setters c) immutability d) documentation → **c**
5. Java 9 modules hide: a) fields b) methods c) whole packages d) memory → **c**
6. True or False: Trivial getters/setters are the essence of information hiding. → **False** (they're a mechanism, often hiding nothing)

## 20. Flashcards
- **Q: Who coined information hiding?** → **A:** David Parnas, 1972.
- **Q: What to hide vs expose?** → **A:** Hide changeable decisions (representation/algorithm/I-O); expose the stable contract.
- **Q: Encapsulation vs information hiding?** → **A:** Mechanism vs principle.
- **Q: How to protect a returned list?** → **A:** Unmodifiable view or defensive copy; never the internal object.
- **Q: Strongest data protection?** → **A:** Immutability.
- **Q: Java 9 modules do what?** → **A:** Export/hide whole packages via `module-info`.

## 21. Revision
Information hiding (Parnas) is the principle: each module conceals the design decisions most likely to change behind a stable interface; encapsulation is the mechanism implementing it. Protect data by validated writes, safe reads (unmodifiable views/copies), and immutability as the ceiling. Leaking internals turns them into permanent API (the trap), so hide by default, expose deliberately. First-30-seconds answer: "Encapsulation hides state; information hiding hides changeable design decisions; both keep the interface stable and the internals safe."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is information hiding?" | Interview Q1 / Formal Definition |
| "Encapsulation vs information hiding?" | Interview Q2 |
| "What should be hidden?" | Interview Q3 |
| "How to protect a Map/list getter?" | Interview Q5 / Section 15 |
| "Does immutability protect data?" | Interview Q8 |
| "Why Java modules?" | Interview Q9 |
| "Can reflection defeat hiding?" | Interview Q14 |
| "How to evolve a library safely?" | Interview Q15 |
