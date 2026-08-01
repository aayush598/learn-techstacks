# Builder Pattern

> **TL;DR**: The Builder pattern separates the **construction of a complex object from its representation** — you configure an object step-by-step (optional parts, validation, immutability) via a fluent builder instead of a giant constructor — and it exists because telescoping constructors, `null` args, and unvalidated intermediate states make object construction a bug factory.

## 1. Why Does This Exist?
Consider a class with 8 fields, 4 of which are optional:
```java
new Pizza(12, true, false, true, "pepperoni", null, "pan", false)
```
This is the **telescoping constructor anti-pattern**: 2⁸ constructor overloads, callers passing positional `null`s that are easy to swap, and no readability ("what was arg 5?"). Even worse, a complex object may have an **invalid intermediate state** — you can't write a constructor that validates the final object if callers assemble it piecemeal, and you can't make the object immutable if it's built in mutable stages.

The Builder pattern exists to solve three problems simultaneously:
1. **Readability**: each attribute is named (`pizza.size(12).cheese(true)`), eliminating positional-arg errors.
2. **Flexibility**: optional parameters are omitted, not passed as `null`.
3. **Safety**: the final `build()` can validate the complete object *and* produce an **immutable** instance (all fields `final`), because the builder holds the mutable intermediate state.

It exists precisely where "an object with many optional/combinable parts" would otherwise explode into unmaintainable constructors.

## 2. How Does It Work?
The pattern has four participants:
1. **Product** — the complex object being built (e.g., `Pizza`), typically immutable, with a *private constructor* taking the builder.
2. **Builder** — the abstract interface declaring build steps (`setSize`, `setCheese`, ...) and `build()`.
3. **ConcreteBuilder** — implements steps, accumulates configuration, performs validation in `build()`.
4. **Director** (optional) — orchestrates a standard sequence of steps; skipped in the fluent/static version.

The *fluent* variant (most common in Java — `StringBuilder`, Lombok `@Builder`, Spring's `UriComponentsBuilder`) is a static nested class:
```java
public class Pizza {
    private final int size;        // final → immutable
    private final boolean cheese;
    private Pizza(Builder b) { this.size = b.size; this.cheese = b.cheese; }
    public static class Builder {
        private int size; private boolean cheese;
        public Builder(int size) { this.size = size; }          // required field
        public Builder cheese(boolean c) { this.cheese = c; return this; }  // each step returns this
        public Pizza build() {
            if (size < 10) throw new IllegalStateException("size too small");
            return new Pizza(this);
        }
    }
}
// usage
Pizza p = new Pizza.Builder(12).cheese(true).build();
```
Each setter mutates the *builder* and returns `this` (the "fluent" part); `build()` validates and produces the immutable product.

## 3. When Is It Used?
- **Objects with many optional parameters** (4+): config objects, HTTP request builders, notification payloads.
- **Immutable objects needing flexible construction**: immutability requires all fields set in the constructor, but a huge constructor is unreadable — the builder bridges both.
- **Validated composite construction**: when `build()` must validate cross-field invariants (e.g., "if size < 10 then no topping", "start date < end date").
- **Different representations of the same construction process**: the GoF Director+Builder variant lets the *same* build steps produce XML, JSON, or a Java object (one Director, many ConcreteBuilders).
- **Fluent DSLs**: `StringBuilder`, `Stream.Builder`, Mockito's `when(...)`, JUnit's `assertThat` builders, Lombok `@Builder`, Jackson `ObjectMapper` config builders.
- **In interviews**: "constructor with too many parameters" → immediately Builder.

## 4. Why Wasn't Another Approach Chosen?
- **Telescoping constructors**: rejected — combinatorial overload explosion, positional-arg bugs, unreadable calls, and no validation of a complete object.
- **A big constructor with all-null defaults (JavaBeans style: default constructor + setters)**: rejected because it allows *invalid intermediate states* (a `Pizza` with `size=0`), breaks immutability (setters), and lets callers forget required fields (no compile-time guarantee). This is the classic "setter-based" alternative and the reason Builder exists.
- **Static factory methods (`Pizza.of(12, true, ...)`)**: fine for a few params, but has the same positional-arg readability problem at scale and no fluent chaining.
- **Multiple overloaded factory methods per combination**: rejected — combinatorial explosion (each combo needs a named method).
- **Passing a config POJO/map**: rejected — no type safety, no validation hooks, strings-as-keys bugs.
- **A plain parameter object (e.g., `PizzaOptions`)**: a reasonable middle ground — but it still needs validation and can't guarantee immutability as cleanly; Builder adds fluent ergonomics and per-step constraint enforcement.
- **Lombok `@Builder` / Kotlin default args / Python kwargs**: these are *language-level* replacements that reduce boilerplate; the pattern is still worth knowing for interviews and for libraries that can't use codegen. (Part 08 covers language idioms.)

## 5. Intuition
A **custom car configurator**: you don't tell a factory "car with 8 mystery options in one sentence". Instead you walk through a *builder* — engine, color, seats, sunroof — each step optional, each choice named, and at the end the dealership *validates* the whole config and hands you the finished car (immutable — you can't change it after delivery). The configurator sheet is the builder; the finished car is the product. Compare with calling "give me a car: true, false, 5, red, false" — the configurator is why Builders exist.

## 6. Real-World Analogy
A **restaurant ordering a custom burger**. The waiter (builder) takes *named* steps — bun, patty, cheese, toppings — with the option to skip each ("no onions" = simply not selected, not "null onions"). The kitchen can't start cooking until the order is complete and validated ("wait, you can't have a burger with no patty"). The finished burger (product) is exactly as ordered and can't be modified after it leaves the kitchen. A "constructor-style" order would be one line: "burger(white, beef, true, false, lettuce, null, ...)" — unreadable and error-prone.

## 7. Formal Definition
> **Builder**: Separate the construction of a complex object from its representation, so that the same construction process can create different representations. (GoF, p. 97)

Participants per GoF: **Director** (constructs the object using the Builder interface), **Builder** (abstract interface for creating parts), **ConcreteBuilder** (implements Builder and assembles the parts, tracks the representation), **Product** (the complex object built). In the widely used *fluent/static* variant, the Director is omitted and the ConcreteBuilder is a nested static class that returns `this` from each step and exposes a validating `build()`.

## 8. Example
Building an immutable `HttpRequest`:
```java
public final class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;   // immutable copy
    private final String body;

    private HttpRequest(Builder b) {
        this.url = b.url; this.method = b.method;
        this.headers = Map.copyOf(b.headers); this.body = b.body;
    }
    public static class Builder {
        private final String url;                 // required
        private String method = "GET";
        private final Map<String, String> headers = new HashMap<>();
        private String body;
        public Builder(String url) { this.url = url; }
        public Builder method(String m) { this.method = m; return this; }
        public Builder header(String k, String v) { headers.put(k, v); return this; }
        public Builder body(String b) { this.body = b; return this; }
        public HttpRequest build() {
            if (!url.startsWith("http")) throw new IllegalArgumentException("bad url: " + url);
            if (!List.of("GET", "POST", "PUT", "DELETE").contains(method))
                throw new IllegalStateException("unsupported method: " + method);
            return new HttpRequest(this);
        }
    }
}
// Usage — readable, validated, immutable:
HttpRequest req = new HttpRequest.Builder("https://api.example.com")
        .method("POST")
        .header("Content-Type", "application/json")
        .body("{\"k\":\"v\"}")
        .build();
```
- Stepwise config, required field enforced by the Builder's constructor, optional fields chained, cross-field validation in `build()`, and an immutable `HttpRequest` (all fields `final`, headers copied defensively).

## 9. Internal Working
1. Client instantiates the `Builder` (usually with a required-field constructor or static `builder()`).
2. Client calls a sequence of fluent setters; each mutates the builder's internal (mutable) fields and returns `this` for chaining.
3. At any point, the *product* does not exist yet — only builder state (this is what makes intermediate invalid states *possible but contained*; the builder never emits a half-built product).
4. Client calls `build()`:
   - validates invariants (required fields present, cross-field rules, ranges);
   - copies mutable collections defensively (so later builder reuse can't mutate the product);
   - invokes the product's private constructor passing `this`;
   - the product copies the builder's fields into `final` fields → immutable, safe publication (see Part 08: `final` field semantics).
5. Optionally the builder can be reused with `.reset()` (GoF Director-style) — though for immutable products each `build()` usually produces a fresh product.

The pattern "works internally" because it moves the *mutability problem* to the builder (short-lived, throwaway) while keeping the product immutable and validating a complete object before it's born.

## 10. Time Complexity
- **Each build step**: O(1) (a field write + reference return).
- **`build()`**: O(P) where P = number of configured parts (plus O(C) to defensively copy collections of size C). Validation is O(1)-O(P) per check.
- **Overall**: constructing an N-part object is O(N) — the same order as a constructor, but with the added O(N) *copies* only where collections are defensively copied. Builder adds a constant factor (method-call overhead per step) — negligible vs the correctness it buys.
- **Memory**: O(N) transient builder state, freed after `build()`.

## 11. Advantages
- **Readability**: named, fluent configuration eliminates positional-arg errors — `new Pizza.Builder(12).cheese(true)` vs `new Pizza(12, true, ...)`.
- **Immutability**: product fields are `final`; the builder holds mutable state, so the product is thread-safe after construction (safe publication).
- **Optionality without `null`**: omitted steps simply don't set a field; no `null`-arg ambiguity.
- **Validation of the whole**: `build()` can enforce cross-field invariants before the object exists.
- **Consistency across representations (GoF variant)**: same steps → different representations (XML/JSON/object) via different ConcreteBuilders.
- **Testability**: build objects easily in tests; fluent DSLs make test code read like assertions.

## 12. Disadvantages
- **Boilerplate**: a full nested Builder is verbose (a class + a nested class); mitigated by Lombok `@Builder`, Kotlin named/default args, or IDE codegen.
- **Not always justified**: for 2-3 required fields and no options, a plain constructor is clearer — Builder is over-engineering (YAGNI).
- **Forgotten steps compile silently**: an omitted optional field is silently defaulted (not a compile error) — validation in `build()` is your only guard.
- **Not a replacement for validation of *behavior***: it validates structure, not semantics.
- **Over-fluency**: chains that enforce *compulsory* step ordering require a state machine (the "Staged Builder" variant) — complexity not needed for most cases.

## 13. Interview Questions
1. **Q: What problem does the Builder pattern solve?** A: Readable, safe construction of objects with many optional/combinable parts, without telescoping constructors or `null` args, while enabling validation and immutability of the final product.
2. **Q: How does Builder differ from a factory?** A: A factory answers *which concrete class* to create, in one step; a Builder answers *how a complex object is assembled*, in many steps, with optional parts and validation. They're complementary (a factory can return a builder).
3. **Q: Why is the JavaBeans setter approach (default constructor + setters) considered bad here?** A: Because it allows invalid intermediate states (a half-set object is visible to other threads), breaks immutability, and provides no compile-time guarantee that required fields were set. Builder keeps the object unbuilt until `build()`.
4. **Q: What is a telescoping constructor anti-pattern?** A: Constructors with overloads for every parameter combination (`Pizza(12)`, `Pizza(12, true)`, `Pizza(12, true, false)`...) — combinatorial explosion, unreadable positional args, and fragile calls. Builder replaces the whole explosion with one fluent API.
5. **Q: Why should the Product be immutable?** A: Because the builder has already handled all mutability; the finished product should be safe to share across threads (safe publication via `final` fields). Immutability also prevents callers from corrupting the validated object after build.
6. **Q: What is the GoF Director, and when do you use it? (Tricky)** A: The Director orchestrates a *fixed sequence* of builder steps — e.g., "build a standard veggie pizza" always calls size→cheese→topping in order. Use it when there are standard construction recipes; skip it in the fluent variant where the client is the director.
7. **Q: How do you make a Builder enforce a *required* step? (Production)** A: Make the required field a constructor parameter of the builder (`new Builder(url)`), or use the "staged builder" where the type changes per step (`WithUrl → WithMethod → Buildable`). The first is standard; the second is a compile-time-checked fluent DSL.
8. **Q: Builder vs Prototype — when each?** A: Builder: many configurable steps from scratch. Prototype: copying an existing instance when construction is expensive and you want a variant. "Same shape, different values" → Prototype; "many optional parts" → Builder.
9. **Q: Where does the JDK use Builder?** A: `StringBuilder`/`StringBuffer`, `Stream.Builder`, `Locale.Builder`, `java.lang.ProcessBuilder`, `Calendar.Builder`, `UriComponentsBuilder` (Spring), Jackson's `ObjectMapper` builders, and `HttpClient.Builder`. 
10. **Q: How does Lombok's `@Builder` relate to the pattern?** A: It's *code generation* of the fluent builder — same shape, zero boilerplate: `@Builder` generates the nested `Builder` class, `build()`, and the private all-args constructor. It's the pattern automated, not a different pattern.
11. **Q: Can Builder help with validation? Give an example of cross-field validation.** A: Yes — in `build()`, e.g., "if `endDate` is before `startDate` throw", "if `size < 10` no toppings allowed". A constructor can validate too, but Builder lets the *client* assemble choices first and validates the *whole* configuration at once, which is the only point where cross-field rules are checkable.
12. **Q: Why does `build()` defensively copy collections? (Tricky)** A: Because the builder's `List`/`Map` is mutable and possibly reusable; if the product stored the *same* reference, later builder mutation would change the supposedly-immutable product. `Map.copyOf`/`List.copyOf` gives the product an unmodifiable snapshot.
13. **Q: When should you NOT use a Builder? (Production)** A: For 1-3 fields with no options (plain constructor/record), for objects created in hot loops where the extra indirection matters (rare), and when a value object could just be a Java record (records give immutable positional construction for small objects). Builder shines at 4+ optional parts.
14. **Q: How does the fluent style work internally — what does each method return?** A: Each fluent step mutates the builder and returns `this` (the builder itself), enabling chaining. The final `build()` returns the *product*, changing the chain's terminal type — that's the "fluent interface" trick.
15. **Q: Builder vs Java records for value objects? (Scenario)** A: Records give immutable, positional construction (`new Point(1,2)`) — ideal for small, fixed-arity values. Records are *insufficient* when you need (a) many optional fields, (b) fluent/readable configuration, or (c) validation beyond the canonical constructor — that's Builder's territory. Senior answer: records replace *some* builder use, not all.
16. **Q: How do you make the builder reusable? (Tricky)** A: Add `reset()` (GoF-style) to clear state after `build()`, or keep one builder per product. For immutable products, reuse is usually unnecessary; per-build builders are simpler and thread-confined.
17. **Q: Thread-safety of Builder?** A: A builder is *not* thread-safe by design (mutable state, chaining) — builders are per-thread/creation-local. The *product* is thread-safe (immutable). Do not share a builder across threads unless you synchronize or use thread-local builders.
18. **Q: Can Builder produce multiple representations from one build process? (GoF intent)** A: Yes — that's the GoF Director+Builder purpose: same steps (Director) executed by different ConcreteBuilders produce different representations (an XML document vs a JSON document). This is used in serialization libraries (e.g., a document builder per format).
19. **Q: Name the exact call sequence a client makes and what each call does.** A: `new Builder(url)` → sets required fields + creates mutable state; `.method("POST")` → mutates builder, returns `this`; `.header(k,v)` → mutates map, returns `this`; `.build()` → validates → defensively copies → calls private product constructor → returns immutable product.
20. **Q: How would you test a Builder? (Production)** A: Test (1) each optional step sets the right field, (2) `build()` validation rejects invalid combos (assert `build()` throws), (3) the product is immutable (mutating the builder's source list after build doesn't affect the product), (4) default values for omitted steps, (5) fluent chaining returns a builder (not a product).

## 14. Follow-Up Questions
1. **Q: What is a "staged" or "type-safe" builder?** A: A builder where each step returns a *different builder type*, so the compiler forbids skipping required steps or calling steps out of order: `WithUrl → WithMethod → Buildable` (e.g., `new ReqBuilder().url(u).method(m).build()` only compiles if both steps ran). Trade-off: more types, but compile-time ordering guarantees.
2. **Q: How does Builder interact with immutability and safe publication?** A: `final` fields + a fully-constructed product → the product is safely published to other threads without synchronization (JMM: final-field freeze semantics, Part 08). The builder's mutable state never escapes.
3. **Q: Builder vs "parameter object"?** A: A parameter object (a `PizzaOptions` passed to a constructor) is a lighter alternative: it groups args but doesn't add validation or fluent ergonomics by itself. Builder ≈ parameter object + fluent DSL + validation + immutability wiring.
4. **Q: How does Kotlin's default arguments / named arguments change the picture?** A: Named + default args make most fluent-builder needs moot in Kotlin (readable, optional, immutable data classes). In Java (no named args), Builder remains the standard idiom. This is a great "language-aware design" point for interviews.
5. **Q: What is the relationship between Builder and Composite?** A: Builders often build *trees* (a Composite product) — e.g., building an HTML document, a parse tree, or a config tree. The Director walks the structure while ConcreteBuilders emit different representations. Classic use: a compiler's AST builder.

## 15. Coding Example
```java
// Full fluent Builder for an immutable Notification (Java)
import java.util.*;

public final class Notification {
    private final String channel;                      // email | sms | push
    private final String title;
    private final String body;
    private final Set<String> tags;                    // immutable set
    private final int priority;

    private Notification(Builder b) {
        this.channel = b.channel;
        this.title = b.title;
        this.body = b.body;
        this.tags = Set.copyOf(b.tags);
        this.priority = b.priority;
    }
    public static class Builder {
        private final String channel;                  // required
        private String title = "";
        private String body = "";
        private final Set<String> tags = new HashSet<>();
        private int priority = 5;

        public Builder(String channel) { this.channel = channel; }

        public Builder title(String t) { this.title = t; return this; }
        public Builder body(String b) { this.body = b; return this; }
        public Builder tag(String t) { tags.add(t); return this; }
        public Builder priority(int p) { this.priority = p; return this; }

        public Notification build() {
            if (!Set.of("email", "sms", "push").contains(channel))
                throw new IllegalArgumentException("invalid channel: " + channel);
            if (priority < 1 || priority > 10)
                throw new IllegalStateException("priority out of range: " + priority);
            return new Notification(this);
        }
    }
    // getters...
}
// Usage
Notification n = new Notification.Builder("email")
        .title("Deploy complete")
        .body("v1.2.3 shipped to prod")
        .tag("deploy").tag("prod")
        .priority(9)
        .build();
```
```python
# Python Builder (dataclasses make it lighter, but pattern is clear)
from dataclasses import dataclass, field, fields

@dataclass(frozen=True)
class Notification:                     # frozen → immutable
    channel: str
    title: str = ""
    body: str = ""
    tags: frozenset = frozenset()
    priority: int = 5

class NotificationBuilder:
    def __init__(self, channel: str):
        self._channel = channel
        self._title, self._body, self._tags, self._priority = "", "", set(), 5
    def title(self, t: str): self._title = t; return self
    def body(self, b: str): self._body = b; return self
    def tag(self, t: str): self._tags.add(t); return self
    def priority(self, p: int): self._priority = p; return self
    def build(self) -> Notification:
        if self._priority < 1 or self._priority > 10:
            raise ValueError("priority out of range")
        return Notification(self._channel, self._title, self._body,
                            frozenset(self._tags), self._priority)

n = NotificationBuilder("email").title("Deploy").body("done").tag("deploy").build()
```
```cpp
// C++ fluent builder (return by reference for chaining)
#include <string>
#include <iostream>

class Notification {
    std::string channel_, title_, body_;
    int priority_;
    Notification(const std::string& c, const std::string& t,
                 const std::string& b, int p)
        : channel_(c), title_(t), body_(b), priority_(p) {}
public:
    class Builder {
        std::string channel_, title_, body_;
        int priority_ = 5;
    public:
        explicit Builder(const std::string& c) : channel_(c) {}
        Builder& title(const std::string& t) { title_ = t; return *this; }
        Builder& body(const std::string& b) { body_ = b; return *this; }
        Builder& priority(int p) { priority_ = p; return *this; }
        Notification build() const { return Notification(channel_, title_, body_, priority_); }
    };
    friend class Builder;
    void describe() const { std::cout << channel_ << " " << priority_ << "\n"; }
};

// Usage
Notification n = Notification::Builder("email").title("Hi").priority(9).build();
```

## 16. Industry Usage
- **JDK**: `StringBuilder` (the canonical fluent builder), `Stream.Builder`, `Locale.Builder`, `ProcessBuilder`, `Calendar.Builder`, `HttpClient.Builder`, `java.lang.invoke.MethodType`/`MethodHandle` builders.
- **Spring**: `UriComponentsBuilder`, `RestTemplate`/`WebClient` builders (`WebClient.builder()`), `AuthenticationManagerBuilder`, `HttpSecurity`'s fluent DSL (a *staged/type-safe* builder).
- **Jackson/Gson**: `ObjectMapper.builder()`, `JsonWriter` fluent APIs; **Apache HttpClient**: `RequestConfig.Builder`.
- **Protocol buffers / FlatBuffers**: generated builders (`Message.Builder`) are builders *by language design* — construction of immutable messages via stepwise, validated builders.
- **Lombok `@Builder`**: codegen of the pattern across countless Java services — the pattern is embedded in the ecosystem's daily tooling.
- **Kotlin**: named/default args replace most builders; **Python**: dataclasses + `frozen=True` make the pattern lighter; still taught and used in frameworks.
- **Interviews**: expect "build an immutable config/request with a builder", "builder vs factory", "why not setters?", "how do you validate in a builder?", and LLD scenarios (design a REST client / URL builder).

## 17. References
- **Gamma et al., *Design Patterns* — "Builder" (p. 97)**: canonical definition, Director/Builder/ConcreteBuilder/Product participants.
- **Joshua Bloch, *Effective Java* (3rd ed.), Item 2**: "Consider a builder when faced with many constructor parameters" — the modern fluent-builder standard.
- **Oracle Docs: `StringBuilder`, `Locale.Builder`, `ProcessBuilder`, `HttpClient.Builder`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Docs: `UriComponentsBuilder`, `WebClient.Builder`** — https://docs.spring.io/spring-framework/reference/
- **Project Lombok — `@Builder`** — https://projectlombok.org/features/Builder
- **refactoring.guru — "Builder"** — modern diagrams and Java/C++/Python examples.
- **Baeldung — "Builder Pattern in Java"** — tutorial with validation and reuse patterns.

## 18. Cheat Sheet
- Builder = **separate construction from representation**; fluent steps + `build()`.
- Solves: **telescoping constructors**, positional `null` args, invalid intermediate states, non-immutable products.
- Participants: Product (immutable, private ctor), Builder (steps + `build()`), optional Director (fixed recipe).
- Each fluent step returns `this`; `build()` validates + defensively copies + constructs product.
- Never use setters to build an immutable object — Builder is the safe path.
- Java examples: `StringBuilder`, `Locale.Builder`, `HttpClient.Builder`, Lombok `@Builder`, Spring `UriComponentsBuilder`.
- Builder vs Factory: Factory = *which* type, one step; Builder = *how* to assemble, many steps.
- Not thread-safe as a builder; the *product* is (immutable, safe publication via `final`).
- Use when 4+ optional params; for small fixed objects use a record/constructor.
- Staged builders enforce step order at compile time (type per step).

## 19. Quiz
1. The Builder pattern separates: a) interface from implementation b) construction from representation c) creation from access d) state from behavior → **b**
2. The main problem Builder solves is: a) slow construction b) many-parameter / telescoping constructors c) memory leaks d) serialization → **b**
3. Which is a JavaBeans anti-pattern the Builder avoids? a) constructor injection b) default ctor + setters (invalid intermediate state) c) immutable fields d) static factory → **b**
4. Each fluent builder step returns: a) the product b) the builder (`this`) c) void d) a new builder class → **b**
5. What should `build()` do before returning the product? a) nothing b) validate + defensively copy + construct c) log d) clone → **b**
6. Which is a JDK Builder? a) `Collections.sort` b) `Locale.Builder` c) `Iterator` d) `Comparator` → **b**
7. Builder differs from Factory because: a) factory is fluent b) factory picks the type, builder assembles parts c) builder is faster d) they're identical → **b**
8. Why is the product often immutable? a) performance b) safe publication + caller can't corrupt validated object c) Java requires it d) testing → **b**
9. Lombok `@Builder` is: a) a different pattern b) codegen of the fluent builder c) a factory d) a singleton → **b**
10. When is Builder over-engineering? a) 6 optional params b) 2 fixed params, no options c) fluent DSLs d) validation needed → **b**

## 20. Flashcards
- **Q: Builder intent?** → **A:** Separate construction of a complex object from its representation; stepwise, fluent, validated.
- **Q: Problem it solves?** → **A:** Telescoping constructors, positional null args, invalid intermediate states, immutability loss.
- **Q: What does each fluent step return?** → **A:** The builder itself (`this`), enabling chaining.
- **Q: What does `build()` do?** → **A:** Validate invariants, defensively copy collections, invoke the private product constructor.
- **Q: Builder vs Factory?** → **A:** Factory = which type (one step); Builder = how to assemble (many optional steps).
- **Q: Why product immutable?** → **A:** Builder holds mutability; immutable product = thread-safe, safe publication via `final`.
- **Q: JDK examples?** → **A:** `StringBuilder`, `Locale.Builder`, `HttpClient.Builder`, `ProcessBuilder`, `Stream.Builder`.
- **Q: JavaBeans alternative and its flaw?** → **A:** Default ctor + setters — invalid intermediate states and no immutability.

## 21. Revision
Builder separates **construction from representation**: a fluent builder accumulates named, optional, stepwise configuration and `build()` produces a validated, **immutable** product. It exists because telescoping constructors, positional `null` args, and setter-based (JavaBeans) construction are unreadable, allow invalid intermediate states, and break immutability. Mechanics: each step mutates the builder and returns `this`; `build()` validates cross-field rules, defensively copies collections, and calls the product's private constructor (fields `final` → safe publication). Use it for objects with 4+ optional parts; skip it for small fixed objects (use a record/constructor). JDK/JVM examples: `StringBuilder`, `Locale.Builder`, `HttpClient.Builder`, Spring `UriComponentsBuilder`, Lombok `@Builder`, Protocol Buffers. Distinguish from Factory (which-type, one step) and Prototype (clone vs configure). Not thread-safe as a builder — per-thread; the product is thread-safe. When asked "why not setters?" — the answer is invalid intermediate states + immutability + no required-field guarantee.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What problem does Builder solve?" | 1 Why / 13 Q1 |
| "Why is JavaBeans/setter construction bad?" | 4 Alternatives / 13 Q3 |
| "Builder vs Factory?" | 13 Q2 / 14 Q2 |
| "What does `build()` do internally?" | 9 Internal Working / 13 Q11 / 13 Q19 |
| "Why should the product be immutable?" | 13 Q5 / 14 Q2 |
| "Where does the JDK/Spring use builders?" | 13 Q9 / 16 Industry Usage |
| "How does Lombok `@Builder` work?" | 13 Q10 |
| "Staged / type-safe builders?" | 14 Q1 / 16 Industry Usage |
| "When should you NOT use a builder?" | 13 Q13 / 14 Q3 |
| "How to enforce a required step?" | 13 Q7 |
