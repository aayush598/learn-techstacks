# Immutability and the `final` Keyword

> **TL;DR**: `final` in Java is a *reference-level* restriction — it stops you from reassigning a variable or overriding a method, but it does NOT make an object immutable; a truly immutable class requires `final` class + `final` fields + no mutable state leaks, and it buys you thread-safety and hashability for free.

## 1. Why Does This Exist?
Mutable shared state is the root of most concurrency bugs: two threads reading/writing the same object race, and caches break when keys change after insertion. Immutability removes an entire category of bugs — once published, an immutable object can never be observed in a partially-constructed or mutated state, so it is inherently thread-safe and can be cached, shared, and hashed without synchronization. `final` exists in the language to *enforce* the reference-level half of that contract, and the JLS §17.5 ("Final Field Semantics") even gives `final` fields special memory-model guarantees so immutable objects are safe to publish without locks.

## 2. How Does It Work?
At a glance:
- `final` **variable**: assigned at most once (initializer or constructor); reassignment is a compile error.
- `final` **field**: assigned in the declaration or constructor; JLS §17.5 guarantees other threads see it properly initialized *after* the constructor completes (safe publication via the final-field freezE).
- `final` **method**: cannot be overridden in a subclass.
- `final` **class**: cannot be subclassed at all.
- Immutability is a *class-level* design property: all fields `final` + all fields hold only immutable types (or are defensively copied) + no mutator methods + class can't be subclassed (final class or private constructor).

## 3. When Is It Used?
- **Value objects** — `String`, `Integer`, `BigDecimal`, `LocalDate`, `Optional`, records — all immutable; used as map keys, cache keys, cache values.
- **Config/DTO objects** in microservices — a parsed config is immutable so no thread can corrupt it.
- **Functional programming** — stream operations and `Comparator`s treat data as immutable pipelines.
- **Constants** — `public static final int MAX_RETRIES = 3` (compile-time constants).
- **Safe publication** — publishing an immutable object to another thread (via `Executor`, event queue) needs no `synchronized`/`volatile` because of §17.5.

## 4. Why Wasn't Another Approach Chosen?
Alternatives:
- **Mutable + synchronization**: `synchronized`/`Lock` everywhere is slow, error-prone, and doesn't compose. Immutability composes (immutable fields of immutable types stay immutable).
- **`const` (C++)**: Java's `final` is a per-reference const, but unlike C++ `const`, `final` on a reference still lets you mutate the referenced *object* (`final List x; x.add(1)` compiles). Java deliberately chose this because deep-const is not expressible in its type system — the language gives you the *discipline* (immutable-class patterns) instead.
- **Defensive copying everywhere**: immutable objects avoid copying on read (no need to return clones because the receiver can't mutate); copying only happens at *construction boundaries*.
- **Records (Java 16+)**: the language now provides shallow immutability syntactically — `record Point(int x, int y)` gives `final` fields, `equals`/`hashCode`/`toString`, and a canonical constructor, proving the platform has moved *toward* immutability as the default.

## 5. Intuition
`final` is a **"Do Not Touch the Handle"** sticker on a specific door handle: it says "you cannot *re-point* this variable," but the room behind the handle is still fully open — a `final ArrayList` can still have elements added. Immutability is the opposite promise: it's a *sealed room* — no door at all. You must make every field `final` (you can't re-point) AND ensure the objects they point to are themselves sealed (or copy them at the door), AND prevent subclassing (or a subclass could add mutable state and break the promise). Only then can you tell other threads "this object is frozen forever — use it without locks."

## 6. Real-World Analogy
A **printing plate** in a newspaper: once cast, it can't be edited — every copy is identical, so thousands of presses can read it simultaneously without any lock. Contrast with a **whiteboard**: anyone can write, so people must coordinate (locks) to avoid overwriting each other. The `final` keyword is like a *signature* on a contract — "this clause can't be changed by a subclass," but the signatories still can't modify the *contents* of the paper they referenced.

## 7. Formal Definition
- **Final variable**: "A final variable may only be assigned once" (JLS §4.12.4); a blank final field must be assigned in every constructor.
- **Final field semantics** (JLS §17.5): "When a constructor completes, the final fields are guaranteed to have the values written by the constructor *as seen by any thread* that obtains a reference to the object after construction completes" — this is the safe-publication guarantee.
- **Immutable class**: a class whose instances cannot be modified after construction: all fields are `final` and reference only immutable values (or are copied on entry/exit), no mutator methods, no subclassable API (final class or private constructor + factory), and no leakage of mutable internals.
- **Record** (JLS §8.10): a class whose members are declared by the record header; fields are private `final`, accessor names match components, and `equals`/`hashCode`/`toString` are derived.

## 8. Example
Build `Money` — an immutable money class:
```java
public final class Money {
    private final long cents;      // primitive: inherently immutable
    public Money(long cents) { this.cents = cents; }
    public long cents() { return cents; }
    public Money plus(Money o) { return new Money(this.cents + o.cents); } // returns NEW, never mutates
}
```
Now the contrast — the classic *broken* "immutable" class:
```java
public final class BadMoney {
    private final long cents;
    private final List<String> tags = new ArrayList<>(); // final REFERENCE, mutable OBJECT
    public void addTag(String t) { tags.add(t); }         // mutates through the final field!
}
```
The fix — defensive copy:
```java
public final class GoodMoney {
    private final long cents;
    private final List<String> tags;
    public GoodMoney(long cents, List<String> tags) {
        this.cents = cents;
        this.tags = List.copyOf(tags);   // copy on entry; now unmodifiable
    }
    public List<String> tags() { return tags; }  // List.copyOf result is unmodifiable, safe to expose
}
```
Trace `final` field safe publication: Thread A builds `Money m = new Money(500)` then hands `m` to Thread B via an `Executor`. Because `cents` is `final`, Thread B is guaranteed to read `500` (no staleness). If `cents` were non-final, B could observe `0` without a memory barrier.

## 9. Internal Working
1. Compiler enforces: a `final` variable is assigned at most once (definite assignment check); a blank final field is assigned in every constructor path.
2. JVM bytecode: `final` fields have no special opcode, but classfile flags mark them; the JIT can constant-fold `static final` primitives/Strings (compile-time constants are inlined into using classes).
3. **Freeze semantics**: the JVM inserts a write barrier (store with release semantics) at the end of constructors of objects with `final` fields so the final-field values are visible after the constructor's freeze point.
4. `static final` fields are initialized once at class-load/clinit; safe publication via the class-initialization barrier (`clinit`).
5. `records` generate `private final` fields + accessor + `equals`/`hashCode`/`toString` at compile time.
6. Subclassing blocked by `final class` → JIT can devirtualize calls (no v-table dispatch) → faster.
7. Immutable objects in caches: identity is irrelevant, value-equality is stable → safe to reuse the same instance (e.g., `Integer.valueOf` caching).

## 10. Time Complexity
- Read access to `final` fields: same as normal field read — O(1); often faster than non-final because the JIT can hoist/inline constants.
- Safe publication via final fields: no runtime locking cost at access time (one-time construction barrier).
- Defensive copying (e.g., `List.copyOf`) costs O(n) per construction but eliminates per-read copies — a one-time cost for unlimited lock-free reads.
- `String` immutability enables `String.substring`/interning optimizations that would be impossible on mutable strings.

## 11. Advantages
- Inherently thread-safe: no synchronization needed for sharing.
- Safe to use as `Map`/`Set` keys and in caches (hash never changes).
- Failure-atomicity: an operation that throws never leaves a half-mutated object.
- Composable: immutable objects of immutable types stay immutable.
- Easier reasoning/debugging: no "who changed this?" hunts.
- JIT-friendly: final methods/classes allow devirtualization; final fields allow constant folding.

## 12. Disadvantages
- Copy-on-write can be expensive for large objects or frequent small changes (each change allocates a new object → GC pressure).
- Deep immutability is not enforceable by the type system — a mutable collection hidden in an immutable shell breaks the promise (must remember defensive copies).
- Functional styles with many small immutable updates can be slow (though records + value-based classes mitigate this).
- Constructing a graph of immutable objects that reference each other (mutual references) is awkward because each must be built in one shot.

## 13. Interview Questions
1. **Q: Does `final` make an object immutable?** A: No — it prevents reassignment of the reference, not mutation of the referenced object; immutability is a design property requiring final fields + immutable contents + no mutators + no subclassing.
2. **Q: What does `final` guarantee for thread-safety?** A: JLS §17.5: final fields are visible with their constructor-assigned values after construction completes (safe publication) without a lock.
3. **Q: What is a blank final field?** A: A final field without an initializer that must be assigned in every constructor.
4. **Q: Can a `final` reference be used to call mutating methods?** A: Yes — `final StringBuilder sb` allows `sb.append(...)`; finalness is about the variable, not the object.
5. **Q: What is the difference between `final`, `finally`, and `finalize()`?** A: `final` = modifier; `finally` = exception-handler block that always runs; `finalize()` = deprecated legacy GC hook.
6. **Q: How do you make a class truly immutable?** A: final class, private final fields, immutable field types or defensive copies on entry, no setters, no leaking mutable internals, and prefer returning new instances from "update" methods.
7. **Q: Why is `String` immutable?** A: Security (classloader paths, URLs), thread-safety, caching/interning, and performance of `hashCode` (computed once) and substring.
8. **Q: What is the difference between a `record` and a regular class?** A: A record is a class with an implicit final class, private final fields, canonical constructor, and auto-generated `equals`/`hashCode`/`toString` — shallow immutability with less boilerplate.
9. **Q: How does immutability help with caching?** A: Immutable keys never change hash, so cache lookups never break; immutable values can be shared without defensive copies.
10. **Q: What is a defensive copy and when is it needed?** A: Copying a mutable object on the way in (constructor) or out (getter) so the class's own state can't be changed by callers.
11. **Q: Can an immutable class contain a `Date` or `ArrayList`?** A: Only if copied and the copies are unmodifiable; otherwise the object is mutable-in-disguise.
12. **Q: What is `Collections.unmodifiableList` vs a truly immutable list?** A: `unmodifiableList` is a read-only *view* over a mutable backing list (still changeable behind the scenes); `List.of`/`List.copyOf` (Java 9+) are genuinely unmodifiable.
13. **Q: Why might the JIT inline a `static final` constant?** A: Compile-time constants are folded into bytecode at compile time (inlining), so reads cost nothing — but that also means changing the constant requires recompiling users.
14. **Q: What is "failure atomicity" and how does immutability provide it?** A: If a method throws mid-operation, the object is unchanged because there's nothing to change; state is only ever replaced wholesale.
15. **Q: When is immutability a bad idea?** A: High-frequency mutation of large objects (copy cost + GC pressure); complex mutually-referencing graphs; or when you need true object identity/identity semantics.
16. **Q: What's the difference between a final variable and a constant?** A: A `static final` primitive/String is a compile-time constant; a `final` instance field is not compile-time constant (per-instance value).
17. **Q: Can a final field be set in a static block?** A: Yes for `static final` fields (blank static finals assigned in static initializer).
18. **Q: Does a record's component accessor return a copy?** A: No — it returns the field directly; if the component is mutable, the record is only *shallowly* immutable (must defensively copy at construction).

## 14. Follow-Up Questions
1. **Q: What exactly does §17.5 freeze guarantee?** A: After the constructor returns, any thread that reads the reference sees the constructor-written values of final fields; writes to non-final fields have no such guarantee (may be stale).
2. **Q: Why can a `HashMap` key still be looked up if you mutate it?** A: If a mutable key changes its `hashCode`, the bucket is wrong → lookup fails. That's why immutable keys are required for correct maps.
3. **Q: What is an "unmodifiable view" and why is it dangerous?** A: `Collections.unmodifiableList(list)` wraps the *original* list; if some other code holds the original and mutates it, the view changes too — a common source of subtle bugs.
4. **Q: How do value-based classes (e.g., `Optional`, `LocalDate`) relate to immutability?** A: They are final, immutable, and compare by value; the JVM is allowed to replace instances to deduplicate them (identity semantics are unspecified).
5. **Q: What's the cost of defensive copies in a hot path?** A: O(n) per construction plus allocation; mitigate by using immutable collections (`List.of`), primitive components, or by not exposing internals at all.
6. **Q: Can you make an immutable class that lazily caches a derived value?** A: Yes — a `final transient` or a `volatile` cached field (e.g., `String.hashCode`), computed once and reused; it keeps logical immutability because the derived value never changes.
7. **Q: Why does the JLS give `final` fields special treatment but not regular fields?** A: Because final fields can't be reassigned after construction, the JVM can prove they're "frozen," enabling the safe-publication guarantee; non-final fields have no such proof.

## 15. Coding Example
```java
import java.util.*;

// A fully immutable class (production shape)
public final class Product {
    private final String id;                     // immutable type
    private final long priceCents;               // primitive
    private final List<String> tags;             // MUST be defensively copied
    private final Map<String, String> attrs;     // mutable inside -> copy

    public Product(String id, long priceCents, List<String> tags, Map<String, String> attrs) {
        this.id = id;
        this.priceCents = priceCents;
        this.tags = List.copyOf(tags);                       // copy on entry (unmodifiable)
        this.attrs = Collections.unmodifiableMap(new HashMap<>(attrs)); // copy + wrap
    }

    public List<String> tags() { return tags; }              // already unmodifiable: safe to expose
    public Map<String, String> attrs() { return attrs; }     // safe: wrapped, no backing ref escapes

    public Product withPrice(long newCents) {                // "update" returns a NEW instance
        return new Product(id, newCents, tags, attrs);
    }

    @Override public String toString() {
        return "Product{" + id + ", " + priceCents + ", " + tags + "}";
    }
}
```
```java
// Where immutable wins: concurrent cache reads with zero locks
import java.util.concurrent.ConcurrentHashMap;

public final class Cache {
    private static final ConcurrentHashMap<String, Product> STORE = new ConcurrentHashMap<>();
    static void init() { STORE.put("p1", new Product("p1", 500, List.of("a"), Map.of())); }
    static Product get(String id) { return STORE.get(id); }  // caller can never corrupt the Product
}
```
```java
// final keyword semantics demo
public class FinalDemo {
    private final int x = 5;            // assigned at declaration
    private final int y;                // blank final
    private final List<String> list = new ArrayList<>(); // final reference, mutable object

    public FinalDemo(int y) { this.y = y; }  // blank final MUST be assigned here

    void demo() {
        // this.list = new ArrayList<>();   // COMPILE ERROR: can't reassign final
        this.list.add("ok");                // LEGAL: mutating the object behind the final ref
    }
    // void method(final int p) { p++; }    // COMPILE ERROR: can't reassign final param
}
```
```java
// record = language-supported shallow immutability (Java 16+)
public record Point(int x, int y) { }
// gives: private final int x, y;  Point(int,int) ctor;  x() y() accessors; equals/hashCode/toString
```

## 16. Industry Usage
- **JDK core**: `String`, `Integer`, `BigDecimal`, `Optional`, `LocalDate` are immutable; `String` immutability underpins string pooling and the security model (classpaths, URLs).
- **Guava** ships `ImmutableList/Set/Map` with proper copy-on-write; Google-style guides mandate immutable DTOs in many services.
- **Spring/Jackson** deserialize into immutable DTOs via constructor binding (`@JsonCreator`), so configuration objects are frozen after load.
- **Event-driven systems** (Kafka consumers, domain events) model events as immutable value objects so they can be replayed and shared across threads safely.
- **CQRS/EventSourcing** treat every state transition as a new immutable event — the entire architecture leans on immutability for correctness.
- **Functional frameworks** (Vavr, Arrow) and Kotlin's `data class` + `val` push the same discipline; Java records (16+) make it idiomatic.

## 17. References
- Oracle, *The Java Language Specification*, §4.12.4 "final Variables", §8.3.1.2 "final Fields", §17.5 "final Field Semantics", §8.10 "Records".
- Joshua Bloch, *Effective Java (3rd ed.)*, Item 17 "Minimize mutability" — the canonical recipe.
- Brian Goetz et al., *Java Concurrency in Practice*, ch. 3 "Sharing Objects" (safe publication, §3.5.3 "Safe Publication Idioms").
- Oracle docs, "Objects, Classes, and Interfaces — final" (docs.oracle.com/javase/tutorial/java/IandI/final.html).
- JEP 395: Records (OpenJDK).
- Baeldung, "Immutable Objects in Java" and "Guide to the final Keyword in Java".

## 18. Cheat Sheet
- `final` variable = assign once; `final` field = assign in ctor; `final` method = no override; `final` class = no subclass.
- Immutable class = final class + final fields + immutable contents (or copies) + no mutators + no internal leakage.
- JLS §17.5: final fields are safe to publish without locks (freeze after constructor).
- Records give shallow immutability automatically (16+).
- `List.of`/`copyOf` are truly unmodifiable; `Collections.unmodifiableList` is a mutable-backed view.
- Defensive copies go on the way IN (constructor) and out (getters).
- Immutability ⇒ thread-safe, safe keys, cache-friendly, failure-atomic.
- Cost: extra allocations on update (copy-on-write).
- `static final` primitives/Strings are compile-time constants (inlined).
- "Update" methods return a new object, never mutate.

## 19. Quiz
1. `final` on a field guarantees: a) The object is immutable b) The reference can't be reassigned c) Thread visibility of all data d) No subclassing → **b**
2. Which makes an object safe to publish to another thread without locks? a) `synchronized` methods b) final fields per §17.5 c) Making fields public d) `static` fields → **b**
3. A "blank final" field must be: a) Set to null b) Assigned in every constructor c) Declared `static` d) Marked `volatile` → **b**
4. Which is truly unmodifiable? a) `Collections.unmodifiableList(b)`) `List.of(a,b,c)` c) `new ArrayList<>(...)` d) A plain array → **b**
5. A class with `private final List<String> tags` — can callers modify the tags? a) No, final blocks it b) Yes, through the list's mutator methods if a reference escapes c) Only via reflection d) Only in the constructor → **b**
6. What does `String` being immutable enable? a) String pooling b) Cached hashCode c) Thread-safety d) All of the above → **d**
7. A record (Java 16+) is: a) Deeply immutable automatically b) Shallowly immutable with auto equals/hashCode c) Mutable by default d) A synonym for `final class` → **b**
8. When is immutability a poor fit? a) Frequent small mutations of large objects b) Cache keys c) Value DTOs d) Configuration objects → **a**
9. `public static final int X = 5;` — what's true? a) X is computed at runtime b) X is a compile-time constant, inlined into users c) X is stored on the heap d) X can be changed via setter → **b**
10. Why are immutable keys required for `HashMap`? a) hashCode must not change while in the map b) equals must be fast c) Keys need final fields d) They must be Comparable → **a**

## 20. Flashcards
- **Q: Does `final` make an object immutable?** → **A:** No, only the reference; immutable design needs final class+fields+copies+no mutators.
- **Q: What does §17.5 guarantee?** → **A:** Final fields are visible with constructor values after construction (safe publication).
- **Q: What's the immutable-class recipe?** → **A:** final class, private final fields, copy mutable inputs, no setters, return new objects.
- **Q: `List.of` vs `unmodifiableList`?** → **A:** Truly unmodifiable vs read-only view of a mutable backing list.
- **Q: What's a defensive copy?** → **A:** Copying mutable data on entry/exit so internals can't be mutated.
- **Q: Why is String immutable?** → **A:** Security, thread-safety, caching/interning, fast hashCode.
- **Q: What is a record?** → **A:** A final class with private final fields + auto equals/hashCode/toString (shallow immutability).
- **Q: When avoid immutability?** → **A:** Hot, frequently-updated large objects (copy + GC cost).

## 21. Revision
`final` controls references and override-ability, not object contents: a final variable is assigned once, a blank final field in every constructor, a final method can't be overridden, a final class can't be subclassed. Immutability is a class-level discipline: final class, private final fields, immutable or defensively-copied contents, no setters, "update" methods return new instances. Per JLS §17.5, final fields give lock-free safe publication after construction — the reason immutable objects are inherently thread-safe and great as map keys/cache values. Records (16+) encode shallow immutability. Watch the trap: `Collections.unmodifiableList` is a mutable-backed view; use `List.of`. Cost of the pattern: extra allocation on every update (copy-on-write). Be ready to build an immutable class and to explain exactly why each step (final, copies, no leak, final class) exists.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you make a class immutable in Java?" | 2 How It Works / 8 Example / 15 Coding |
| "What does `final` actually guarantee?" | 2 How It Works / 7 Formal Definition |
| "What is safe publication?" | 7 Formal Definition / 14 Follow-Up |
| "Why is String immutable?" | 13 Interview Questions |
| "What's a defensive copy and when do you need it?" | 8 Example / 13 Interview Questions |
| "What's the difference between `final`, `finally`, `finalize`?" | 13 Interview Questions |
| "What are records and how do they help?" | 4 Alternatives / 7 Formal Definition / 15 Coding |
| "Why are immutable objects thread-safe?" | 1 Why Exists / 11 Advantages |
| "When should you NOT use immutability?" | 12 Disadvantages / 13 Interview Questions |
| "What's wrong with `Collections.unmodifiableList`?" | 13 / 14 Follow-Up Questions |
