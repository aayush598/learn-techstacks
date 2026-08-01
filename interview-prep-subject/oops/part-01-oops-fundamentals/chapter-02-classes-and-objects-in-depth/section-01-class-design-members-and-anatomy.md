# Class Design, Members, and Anatomy

> **TL;DR**: A Java class is a blueprint made of six kinds of members — fields, methods, constructors, initializers, nested types, and static members — each declared for a specific reason; designing them deliberately (what's private, what's a method vs a field, what's static) is the entire art of class design.

## 1. Why Does This Exist?
A class exists to be the *unit of design*, and its anatomy — the members you choose and how you expose them — determines the class's usability, safety, and extensibility. Poorly designed classes (public fields, no constructors, everything static) silently degrade into procedural code and break encapsulation. Understanding the anatomy answers interview questions like "what can a class contain?", "why use a constructor over a static factory?", and "when should a member be static?" — and in production it is how you design APIs others will depend on. The anatomy is not trivia: each member type exists to solve a specific lifecycle/visibility/reuse problem.

## 2. How Does It Work?
A class declaration `class Foo { ... }` can contain, in any order:
1. **Fields** (instance + static): state. `private int count;` `static final int MAX = 100;`
2. **Methods** (instance + static): behavior. `public void increment() { count++; }`
3. **Constructors**: initialization. `Foo(int initial) { ... }` — always same name as class, no return type.
4. **Initializers**: `{ ... }` instance block, `static { ... }` class block — run during construction/class-loading.
5. **Nested types**: inner classes, static nested classes, local/anonymous classes.
6. **Modifiers** on all of the above: `public/private/protected`, `static`, `final`, `abstract`, `synchronized`.

The compiler organizes fields into the object layout and methods into the class's method tables; the runtime uses constructors/initializers to set up a valid object before you ever use it.

## 3. When Is It Used?
- **Fields**: every object that holds data. Instance fields for per-object data; static fields for class-wide constants/shared config.
- **Methods**: every operation on the object; public methods form the API, private ones are implementation details.
- **Constructors**: mandatory setup (validate inputs, set defaults, acquire resources).
- **Static factories** (`valueOf`, `of`, `getInstance`): when construction needs naming, caching, or subtype choice.
- **Nested classes**: helper classes scoped to the outer class; `Builder` inner classes; callbacks.
- **Initializers**: rare — default values, `static` config loading (e.g., reading a properties file once per class).

## 4. Why Wasn't Another Approach Chosen?
- *Fields vs all-private-with-getters*: fields are for trivial state; exposed directly only when there's no invariant to protect. Every *other* approach (public fields) was rejected because it breaks invariants — getters/setters chosen when behavior needed guarding.
- *Constructors vs a plain `new` with field assignment*: field-by-field assignment can produce *partially built* objects (invalid states visible to other threads/callers); constructors chosen because they make "object is valid immediately" a language guarantee.
- *Constructors vs static factory methods*: factories give naming, caching, and subtype flexibility, but constructors are simpler and familiar; Effective Java says prefer factories but constructors remain for simple cases — both are standard, and the choice is a design judgment.
- *Instance methods vs static methods*: static chosen when the method doesn't depend on instance state (utilities) — because an instance method that ignores `this` misleads readers and blocks stateless reuse.
- *Nested vs top-level classes*: nested chosen for tight coupling/access to private state; top-level for independent reuse.

## 5. Intuition
A class is a **job description** for an object: "you will have these attributes (fields), you will be set up like this (constructor), you will do these things (methods), and the public ones are what others may ask of you." A well-written job description lists *responsibilities* (public methods), keeps internal details private (private fields), and includes how the employee is onboarded (constructor). Like a job description, a class should state its role clearly and not mix unrelated duties (the Single Responsibility Principle in miniature).

## 6. Real-World Analogy
A **bank vault box** — fields are the contents (private); the methods are the approved operations (deposit/withdraw via a teller); the constructor is the opening process (verify ID, sign forms); static members are the bank's shared policies (all boxes share the same security rules). Nobody reaches into the box directly; they interact through the sanctioned procedures. The class defines "what a box is" and "how you may use it"; the anatomy is the box's paperwork.

## 7. Formal Definition
A **class** is a user-defined type whose declaration may contain six kinds of members: **fields** (instance and static data members), **methods** (instance and static function members), **constructors** (special methods named after the class that initialize new instances), **instance/static initializer blocks** (executed at construction and class-loading, respectively), **nested types** (member classes/interfaces/enums declared inside the class), and (in Java) **enum constants** for `enum` types. Each member may carry access and other modifiers that govern visibility, sharing, and overridability.

## 8. Example
```java
public class Order {
    // 1) STATIC FIELDS (class-wide)
    private static final int MAX_ITEMS = 50;

    // 2) INSTANCE FIELDS (per-object state)
    private final String orderId;
    private int itemCount;
    private boolean shipped;

    // 3) CONSTRUCTOR (initialization guarantee)
    public Order(String orderId) {
        if (orderId == null || orderId.isBlank()) throw new IllegalArgumentException("orderId required");
        this.orderId = orderId;
        this.itemCount = 0;
        this.shipped = false;
    }

    // 4) INSTANCE METHODS (behavior)
    public void addItem() {
        if (itemCount >= MAX_ITEMS) throw new IllegalStateException("max items reached");
        itemCount++;
    }
    public void ship() { shipped = true; }
    public boolean isShipped() { return shipped; }

    // 5) STATIC METHOD (behavior independent of instance)
    public static String format(String orderId, int items) {
        return orderId + ":" + items;
    }

    // 6) NESTED TYPE (helper scoped to Order)
    public static class Builder {
        private String id = "UNASSIGNED";
        public Builder withId(String id) { this.id = id; return this; }
        public Order build() { return new Order(id); }
    }
}
```
Members at work: static field shared by all orders; instance fields per order; constructor validates before state exists publicly; instance methods mutate state safely; static method usable without an instance; nested `Builder` gives fluent construction.

## 9. Internal Working
1. **Compilation**: javac parses members; fields become fixed offsets in the object layout; methods become entries in the class file's method table; static fields become entries in the class-level "static" storage (metaspace).
2. **Class loading**: the JVM loads `Order.class`, initializes static fields and runs `static {}` initializers once, in declaration order (only on first active use).
3. **Instantiation**: `new Order("A1")` → allocate object → run field initializers and instance `{}` blocks in source order → run constructor body → object is fully valid.
4. **Dispatch**: instance methods are bound to `this`; static methods are invoked without an instance and can't access instance fields (compiler enforces).
5. **Access control**: private members are visible only within the class; the bytecode verifier rejects other classes' access.
Each member type maps to a precise runtime step — that's why the anatomy matters beyond style.

## 10. Time Complexity
- Field access: O(1) (offset from `this`).
- Method call: O(1) (direct or vtable).
- Static field access: O(1) (fixed class-level slot).
- Constructor: O(1) + cost of field initializers and constructor body (often O(fields)).
- Class loading/static-init: O(class size) once, amortized.
- Nested class instantiation: same as outer (O(1) + init).

## 11. Advantages
- **Single place for state + behavior** — cohesion, one-stop modification.
- **Encapsulation** — private members stay private; API surface is explicit.
- **Reuse** — static members shared; nested types co-located with their owner.
- **Safety** — constructors make invalid objects impossible (when written well).
- **Clarity** — the class doc + public signature *is* the contract.

## 12. Disadvantages
- **Boilerplate** — getters/setters/constructors (mitigated by records, Lombok).
- **Large class risk** — too many members violates SRP (class grows unreadable).
- **Static state is global state** — static mutable fields are a hidden coupling point.
- **Nested classes increase cognitive load** — anon/local classes can obscure flow.
- **Initializer order pitfalls** — relying on field initializer order can bite during refactors.

## 13. Interview Questions
1. **Q: What members can a Java class contain?** A: Fields (instance/static), methods (instance/static), constructors, instance/static initializer blocks, nested types (inner classes, static nested classes, local/anonymous), and enum constants (in enums).
2. **Q: Why are fields typically private and accessed via methods?** A: So the class controls all state changes — invariants (e.g., `itemCount <= MAX_ITEMS`) are enforced at every mutation; direct public access lets callers break them.
3. **Q: Constructor vs static factory method — when each?** A: Constructor for simple guaranteed-valid construction; static factory when you need naming (`of`, `from`), caching (`valueOf` reuses instances), or choosing a subtype. Effective Java prefers factories when both fit.
4. **Q: TRICKY — What's the difference between a field initializer, an instance initializer block, and a constructor?** A: A field initializer (`private int x = 5;`) runs at construction in source order; an instance `{}` block also runs at construction in source order; the constructor runs *last*, after all initializers. Order matters when one depends on another.
5. **Q: When does a `static {}` block run?** A: Once, when the class is first actively used (class initialization) — not per instance and not necessarily at load time; it's where class-wide setup (loading config) belongs.
6. **Q: PRACTICAL — Should `MAX_ITEMS` be static final, and why?** A: Yes — it's the same for every `Order`, never changes, and is compile-time constant; `static final` makes it a constant expression inlined by javac.
7. **Q: Why can a constructor have no return type?** A: Because `new` *always* returns the constructed object; a return type would be meaningless/ambiguous. Constructors aren't called like methods — they're invoked by `new`.
8. **Q: SCENARIO — Design a `Config` class that loads a properties file once.** A: `static` fields + a `static {}` block (or `static final Config INSTANCE`); instance methods read the loaded values; constructor made `private` to force single instance.
9. **Q: When should a method be `static`?** A: When it doesn't use any instance state — pure computation on parameters (`Order.format(...)`); making it static signals "no instance needed" and prevents accidental coupling to `this`.
10. **Q: TRICKY — Can a static method access an instance field?** A: No — there's no `this` to access it through; the compiler rejects it. It can only access instance state via a passed-in reference.
11. **Q: What is a nested class and why nest it?** A: A class declared inside another; nest when it's a detail of the outer class (Builder, iterators, listeners) that needs access to private members — keeps the namespace and coupling explicit.
12. **Q: PRODUCTION — Why does `Optional.of(x)` reject null but `Optional.ofNullable(x)` allow it?** A: Because `of` is a *named* static factory with a documented contract (fail fast on null) while `ofNullable` tolerates null — an example of factories letting the API express two semantics cleanly.
13. **Q: What's the difference between a class and a record in Java?** A: A record is a *restricted* class: immutable state, auto `equals`/`hashCode`/`toString`, and a canonical constructor — the "data carrier" anatomy; classes keep full flexibility (mutable state, behavior, inheritance).
14. **Q: SCENARIO — A class has 20 public methods and 5 fields. What's the smell?** A: Likely SRP violation — too many responsibilities; consider splitting into collaborating classes (extract behavior into a strategy/handler). High method count with few fields often indicates behavior doesn't belong to the data.
15. **Q: Can a class be `final` and still have constructors?** A: Yes — `final` only bans subclassing; constructors still run for instances of the final class itself.

## 14. Follow-Up Questions
1. **Q: What happens if a field initializer reads a field declared later?** A: It sees the default value (0/null/false) — order of initialization is source order; relying on it is a smell (fix by reordering or constructor assignment).
2. **Q: Why are anonymous classes limited?** A: They can't have constructors (only instance initializers), can't be abstract, and capture effectively-final locals — they're sugar for one-shot implementations.
3. **Q: When should a nested class be static vs inner?** A: Static nested when it doesn't need the outer instance (Builder — no outer needed); inner (non-static) when it must reference `this` of the outer (listeners adapters). Inner classes hold a hidden reference, preventing the outer from being GC'd — a leak source.
4. **Q: What's the difference between `synchronized` on a static vs instance method?** A: They lock different objects — the `Class` object vs the instance — so they don't serialize against each other; a classic concurrency misunderstanding.

## 15. Coding Example
```java
public class Service {
    private static final long START = System.currentTimeMillis();   // static init at class load
    private final String name;
    private int requests;

    {                                   // instance initializer: runs before constructor
        this.requests = 0;              // default anyway — illustration only
    }
    static {                            // class initializer: once per class
        System.out.println("Service class initialized");
    }

    public Service(String name) { this.name = name; }

    public void handle() {
        requests++;
        System.out.printf("[%s] requests=%d uptimeMs=%d%n", name, requests, uptimeMs());
    }
    private static long uptimeMs() { return System.currentTimeMillis() - START; }

    public static void main(String[] args) {
        Service a = new Service("alpha");   // static init happened once already
        Service b = new Service("beta");
        a.handle();                          // alpha requests=1
        b.handle();                          // beta  requests=1  (independent instance state)
        System.out.println(Service.uptimeMs());   // static call, no instance needed
    }
}
```
```cpp
// C++ class anatomy: fields, constructor, member functions (incl. static), destructor
class Service {
    static inline long start_ = 0;      // C++17 inline static, one per class
    std::string name_;
    int requests_ = 0;
public:
    explicit Service(std::string name) : name_(std::move(name)) {}
    void handle() { ++requests_; }
    static void init() { start_ = /* ... */; }
};
```
```python
class Service:
    start = None                      # class variable (shared)

    def __init__(self, name: str):    # constructor
        self.name = name
        self.requests = 0             # instance variable

    def handle(self) -> None:
        self.requests += 1
        print(self.name, self.requests)
```

## 16. Industry Usage
- **Java standard library**: `Collections` is all static utility methods (procedural-by-design — stateless); `String` is a final class with instance state; `Optional` shows the static-factory API (`of`/`ofNullable`/`empty`) used in virtually every modern codebase.
- **Spring**: `@Configuration` classes + `@Bean` methods are class members used by DI; record DTOs (Java 17+) now dominate data anatomy in production microservices.
- **Guava**: `ImmutableList.of(...)` — static factories everywhere; the class anatomy includes builders (`ImmutableList.Builder`).
- **Android/Kotlin**: `companion object` replaces Java's static members; data classes replace records — same anatomy, different syntax.
- **Effective Java discipline**: most production Java style guides (Google Java Style, Amazon internal) encode "fields private, expose behavior, prefer factories for complex construction."

## 17. References
- Joshua Bloch, *Effective Java* — Items 1 (static factories), 2 (Builder), 4 (non-instantiability), 15–17 (fields and access).
- Java Language Specification, Ch. 8, §8.1–8.6 (Class body, fields, methods, initializers): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- Oracle Java Tutorials, "Declaring Member Variables" / "Defining Methods": https://docs.oracle.com/javase/tutorial/java/javaOO/index.html
- Robert C. Martin, *Clean Code* — object anatomy and cohesion.

## 18. Cheat Sheet
- Six member kinds: fields, methods, constructors, initializers, nested types (+ enum constants).
- Init order: field init & `{}` blocks in source order → constructor body.
- `static {}` runs once per class on first active use.
- Static method ↔ no `this`; can't touch instance state.
- Instance field = per object; static field = per class.
- Fields private; public API = methods only (unless trivial immutable constant).
- Constructor can't have return type; can't be static/final/abstract.

## 19. Quiz
1. Which is NOT a class member? a) field b) constructor c) `main` d) nested class → **c** (`main` is a method, but as *the* `main` it's not a member category; strictly it's a static method — trick: it IS a member. The intended answer is that all are members; use judgment — the tested distinction is that a constructor and nested class are members, and any method is a member.)
2. Instance initializer blocks run: a) once per class load b) before the constructor on each `new` c) after `main` d) never → **b**
3. A static method can access: a) instance fields directly b) only static members c) `this` d) nothing → **b**
4. Constructor return type: a) `void` b) the class type c) none d) `Object` → **c**
5. `static final int MAX = 50;` is: a) instance state b) a compile-time constant shared by all instances c) mutable d) a method → **b**
6. True or False: A nested class can be `static`. → **True** (static nested class)

## 20. Flashcards
- **Q: Six kinds of class members?** → **A:** Fields, methods, constructors, initializers, nested types (+ enum constants).
- **Q: Order of initialization?** → **A:** Field initializers + `{}` blocks in source order, then constructor body.
- **Q: When does `static {}` run?** → **A:** Once, on first active use of the class.
- **Q: Can a static method access instance fields?** → **A:** No — no `this`.
- **Q: Constructor vs static factory?** → **A:** Factory gives naming/caching/subtypes; constructor is simple and language-guaranteed.
- **Q: Why private fields + public methods?** → **A:** The class controls all state changes → invariants stay intact.

## 21. Revision
A class's anatomy is fields (instance per-object / static per-class), methods (instance / static), constructors (name = class, no return type, run last after initializers in source order), initializers (`{}` per-new, `static {}` once per class load), and nested types. Static members have no `this` and can't touch instance state; `static final` fields are shared compile-time constants. Good design: private fields, public methods as the API, constructors or static factories to guarantee valid state. First-30-seconds answers: "constructors guarantee initialization; static means class-level; order is initializers then constructor."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What can a Java class contain?" | Formal Definition / Section 13 |
| "Init order of fields vs constructor?" | Interview Q4 / Internal Working |
| "When does static block run?" | Interview Q5 |
| "Constructor vs static factory?" | Interview Q3 / Section 16 |
| "Why private fields?" | Interview Q2 |
| "Can static method access instance field?" | Interview Q10 |
| "Why no return type on constructor?" | Interview Q7 |
| "Record vs class anatomy?" | Interview Q13 / Section 16 |
