# Objects and Classes

> **TL;DR**: A class is a compile-time blueprint that declares what data and behavior a thing has; an object is a runtime instance of that class with its own memory and its own copy of instance state — "class = cookie cutter, object = cookie."

## 1. Why Does This Exist?
The class/object distinction exists because code is *static text* while running programs are *dynamic state*. If you declared one `BankAccount` in your source, you would still need a way to represent ten thousand distinct accounts, each with a different balance, all sharing the *same* withdrawal logic. The class provides the shared definition (one copy of code); the object provides the per-account memory (ten thousand copies of `balance`). Without classes you'd duplicate code for every entity; without objects you'd have no place to store per-instance data. The pair is the fundamental OOP unit — everything else (pillars, relationships, SOLID) is built on understanding these two.

## 2. How Does It Work?
1. You write a `class` (a template): declare fields (`private double balance`), methods (`withdraw()`), a constructor.
2. The compiler records the layout: every field gets an offset in the object; every non-static method gets an implicit `this` parameter.
3. At runtime, `new BankAccount(500)` allocates a chunk of memory for the object's fields, initializes them via the constructor, and returns a *reference* to that memory.
4. All instances share the class's method code but have **independent field memory**.
5. Static members belong to the *class* (one copy), instance members belong to each *object*.

The relationship is one-to-many: one class → N objects, and `class.class` (the `Class` object / `.class` literal) represents the class itself at runtime (reflection).

## 3. When Is It Used?
- **Every OOP program** — classes are the fundamental organizing unit (Java, C++, C#, Python).
- **Domain modeling**: `Order`, `Product`, `User` classes with objects per row of data.
- **Framework development**: Spring beans are instances; Spring scans *classes* (via reflection) to create objects.
- **Factory/Prototype patterns**: where you decide "which class to instantiate" at runtime.
- **Data classes**: Java records, C++ structs, Python dataclasses — all are classes with an emphasis on state.
- **Whenever you need "many similar things that behave the same but hold different data."**

## 4. Why Wasn't Another Approach Chosen?
- *Why not only classes (no objects)?* Because then all state would be shared/static — every account would share one balance. That defeats the purpose; you need per-instance memory.
- *Why not only objects (no classes)?* This is the prototype-based approach (JavaScript before ES6, Self). Objects are cloned from a prototype object instead of instantiated from a template. It's flexible but loses compile-time type checking and shared-type guarantees. Classes were chosen for statically-typed languages because they give *type safety, predictable layout, and compiler checks*.
- *Why not functions + closures for state?* Closures capture state too (Python/JS), but without named types, inheritance, or visibility rules, so they can't express the full OOP model. Classes chosen for modeling, closures kept as an implementation detail (Python/JS methods are closures over instances).

## 5. Intuition
A class is a **blueprint for a house** — it says there will be a living room, a bedroom, a bathroom (fields), and that you can open/close doors (methods). A blueprint builds no house; it describes all houses. An object is **one physical house** built from that blueprint — it has its own actual living room with its own furniture. Ten houses built from one blueprint share the *design* but not the *contents*. That is exactly "one class, many objects, independent state."

## 6. Real-World Analogy
A **cookie cutter and cookies**. The class is the cutter (a fixed, reusable shape); objects are the cookies (many identical-shaped cookies, each its own physical thing). You can't eat a cookie cutter, and you can't use a cookie as a template. Similarly, you can't run a class (no memory/behavior instance), and you can't make objects without the class. In Java, `Cookie.class` (reflection) is like the cutter's documentation — metadata about the shape, not a cookie.

## 7. Formal Definition
A **class** is a user-defined reference data type that defines a set of instance fields (state), methods (behavior), and constructors (initialization) — a template for objects. An **object** is an instance of a class: a runtime entity with identity (its memory address/reference), state (its field values), and behavior (methods invokable on it). In Java, an object is created with `new ClassName(...)`; the reference is stored in a variable, and the object itself resides on the heap. The class's code (methods) is shared by all instances.

## 8. Example
```java
public class Car {
    private final String model;
    private int speedKmh;

    public Car(String model, int speedKmh) {
        this.model = model;
        this.speedKmh = speedKmh;
    }
    public void accelerate(int delta) { speedKmh += delta; }
    public int getSpeedKmh() { return speedKmh; }
}

Car a = new Car("Tesla", 0);    // object 1: model="Tesla", speed=0
Car b = new Car("BMW", 60);     // object 2: model="BMW", speed=60
```
- `a` and `b` are *two distinct objects*: changing `a.speedKmh` (via `a.accelerate(20)`) does NOT affect `b`.
- They share the single compiled copy of `accelerate()` code.
- `Car.class` is the class-level metadata; `a.getClass()` returns the same `Class<Car>` for both.

## 9. Internal Working
1. **Compile time**: javac reads the class, assigns each instance field an offset (`model` at 0, `speedKmh` at 4 for a 32-bit int, after the header), and compiles `accelerate` to code that takes a `this` reference.
2. **Load time**: the JVM loads `Car.class`, creates a `Class<Car>` object in the heap (method area/metaspace holds method code), verifies bytecode.
3. **Instantiation**: `new Car("Tesla",0)` → JVM allocates object memory in Eden (young gen) — object header (mark word + klass pointer, ~12–16 bytes in HotSpot, aligned) + field space (`model` reference 4–8 bytes + `speedKmh` 4 bytes) → constructor runs, writing values.
4. **Reference semantics**: the local variable `a` holds a reference (pointer) to the heap object; assignment `Car c = a;` copies the *reference*, not the object (two variables, one object).
5. **Method call**: `a.accelerate(20)` pushes `this=a` and the arg; the JIT-compiled code reads `speedKmh` at `this+offset` and stores back.
6. **Death**: when no references point at the object, the GC reclaims it (for `Car`, automatically; `finalize` is deprecated and should not be relied upon).

## 10. Time Complexity
- `new` allocation: O(1) amortized (bump-the-pointer in Eden, thread-local allocation buffers/TLABs).
- Field read/write: O(1) — fixed offset from object base.
- Instance method call: O(1) — direct or vtable dispatch.
- Object death: amortized O(1) (GC marking, generational collection); not to be confused with destructor cost (C++ non-trivial destructors add O(fields) or more).
- Class loading: O(1) once, amortized over instances.

## 11. Advantages
- **Reusability**: one class definition serves unlimited objects.
- **Type safety**: the class is a type; the compiler rejects wrong usage.
- **Memory efficiency of code**: method code stored once, shared by all instances.
- **Modeling**: class = noun (type), object = specific thing (instance) — matches how humans think.
- **Static type checking** at compile time and **runtime polymorphism** via objects.

## 12. Disadvantages
- **Per-object overhead**: object header + reference indirection; thousands of tiny objects hurt cache locality.
- **Boilerplate**: getters/setters/constructors (mitigated by records/lombok/dataclasses).
- **Runtime creation cost** vs stack-allocated plain data (in Java, all objects are heap).
- **Class-as-type rigidity**: you cannot easily create "a class with one extra field" without inheritance or composition.
- **Identity vs value confusion**: two objects with equal state are not `==`-equal unless you override `equals` (the classic bug).

## 13. Interview Questions
1. **Q: Difference between a class and an object?** A: A class is a template/type declaring fields, methods, constructors; an object is a runtime instance with its own allocated memory and state. Class = blueprint, object = building.
2. **Q: How many objects does `String s = new String("hi");` create?** A: Two: the `String` object on the heap and the string literal `"hi"` in the constant pool (interned); plus the reference `s`. `"hi"` and the `String` are distinct objects (though `equals` is true).
3. **Q: TRICKY — `Car a = new Car("Tesla",0); Car b = new Car("Tesla",0);` — is `a == b`? Is `a.equals(b)`?** A: `a == b` is false (references differ). `a.equals(b)` is false unless `Car` overrides `equals` to compare state. Default `Object.equals` uses `==`. This is the identity-vs-equality trap.
4. **Q: Can a class exist without any object?** A: Yes — the class (and its static members) exist as metadata in metaspace once loaded; you can call static methods and use reflection without any instance.
5. **Q: Can an object exist without a class?** A: No in class-based OOP. In prototype-based JS you can clone objects without an explicit class (ES5), but Java/C++/C# require a class.
6. **Q: PRACTICAL — Where does the object live and where does the reference live in Java?** A: The object lives on the heap (always); the reference lives on the stack (local variable) or inside another object (field). Primitives in local variables live on the stack.
7. **Q: What happens on `Car c2 = a;`?** A: Only the reference is copied; both `a` and `c2` point to the same single object. Mutating through `c2` is visible through `a`. This is call-by-value-of-reference (Java is pass-by-value, always).
8. **Q: TRICKY — Is Java pass-by-value or pass-by-reference?** A: Pass-by-value, always. For objects, the *value passed is the reference* (pointer value). Mutating the object works; reassigning the local parameter does not affect the caller's variable.
9. **Q: SCENARIO — Design an `Address` class. Should it be a class or a record, and why?** A: A record (`record Address(String street, String city, String zip)`) — it's an immutable value with structural equality; use a class only if you need mutable state or behavior beyond the accessors.
10. **Q: Why do objects need a header in memory?** A: The JVM stores metadata — mark word (GC/age/hashcode bits) and klass pointer (type identity for dispatch, instanceof, casting) — enabling GC, locking, and polymorphism. C++ objects of a polymorphic class carry a vptr instead.
11. **Q: What's the difference between `new Car()` and declaring `Car c;`?** A: `new Car()` allocates and constructs an object; `Car c;` only declares a reference variable (initially `null` in Java, garbage value in C++ local unless initialized). No object exists until `new`.
12. **Q: PRACTICAL — Why prefer a single class with N objects over N copies of the code?** A: Because method code is shared (stored once), state is separated per object, and a bug fix in the class fixes all objects. Duplicated code would create divergence.
13. **Q: SCENARIO — A teammate defines one class per customer because "each has different fields." What's the problem?** A: It violates reuse and type design: you'd need a class per combination of fields. Better: one `Customer` class with nullable/optional fields or an `attributes` map; use inheritance only for genuine is-a variants (e.g., `PremiumCustomer`).
14. **Q: What is the `Class` object?** A: At load time, the JVM creates a `java.lang.Class<T>` instance representing each class — used for reflection (`getClass()`, `.class`), the basis of frameworks like Spring (bean scanning, DI) and Hibernate (entity mapping).
15. **Q: How many copies of a static field exist?** A: Exactly one per class (in metaspace), shared by all instances and reachable without any instance. Contrast: instance fields have one copy per object.
16. **Q: TRICKY — Can a class have no fields? What's the point?** A: Yes — a marker/tagging class (e.g., `Serializable` implemented as an interface, or a tag class), or a pure behavior class (strategy objects). The point is *type identity*, not state.

## 14. Follow-Up Questions
1. **Q: What is object identity in Java?** A: An object's identity is its heap address (reference); it's constant for the object's life and what `==` compares. Two objects always have distinct identities even with equal state.
2. **Q: What does the `equals`/`hashCode` contract have to do with classes?** A: If you override `equals` to compare state, you must override `hashCode` so equal objects hash equally — otherwise HashMap/Set break (two equal keys land in different buckets).
3. **Q: What's the difference between a class and a type?** A: A class is a runtime construct with code + metadata; a type is a compile-time concept. In Java every class is a type (and interfaces too), and you can have a type (interface) without a class.
4. **Q: What are `static` nested classes vs inner classes?** A: A static nested class is just a namespace-scoped class (like a top-level class); an inner (non-static) class has an implicit reference to the enclosing instance and cannot exist without it.

## 15. Coding Example
```java
public class Wallet {
    private final String owner;
    private int cash;

    public Wallet(String owner, int cash) {
        this.owner = owner;          // 'this' disambiguates field from parameter
        this.cash = cash;
    }
    public void add(int amount) { if (amount > 0) cash += amount; }
    public void spend(int amount) {
        if (amount > cash) throw new IllegalStateException("insufficient funds");
        cash -= amount;
    }
    public int getCash() { return cash; }

    public static void main(String[] args) {
        Wallet alice = new Wallet("Alice", 100);  // object #1
        Wallet bob   = new Wallet("Bob", 50);     // object #2
        alice.add(20);
        bob.spend(10);
        System.out.println(alice.getCash());      // 120  (independent of bob)
        System.out.println(bob.getCash());        // 40
        Wallet alias = alice;                      // copies the REFERENCE only
        alias.spend(100);                          // affects alice too
        System.out.println(alice.getCash());      // 20
    }
}
```
```cpp
// C++ — same concept with value semantics available
class Wallet {
    std::string owner_;
    int cash_;
public:
    Wallet(std::string owner, int cash) : owner_(std::move(owner)), cash_(cash) {}
    void add(int amount) { if (amount > 0) cash_ += amount; }
    int cash() const { return cash_; }
};
// Wallet a("Alice",100); Wallet b = a;  // b is a COPY (value semantics), unlike Java
```
```python
class Wallet:
    def __init__(self, owner: str, cash: int):
        self.owner = owner          # every instance gets its own namespace
        self.cash = cash
    def add(self, amount: int) -> None:
        if amount > 0: self.cash += amount
alice = Wallet("Alice", 100)        # object 1
bob   = Wallet("Bob", 50)           # object 2
```

## 16. Industry Usage
- **Spring Framework**: beans are objects; `@Configuration` classes are scanned at startup; DI instantiates classes and wires objects — the entire framework is "classes → objects" at scale.
- **Hibernate/JPA**: entity *classes* map to tables; *objects* map to rows. One `User.class` → N `User` objects, each a DB row.
- **Jackson/Gson**: serializes objects to JSON and back using the class definition as the schema; per-object state is the payload.
- **Java records** (Java 16+) adopted precisely because many classes are just state buckets — production code increasingly uses records for DTOs and classes for behavior.
- **Object pools** (connection pools, thread pools) reuse objects — the class defines the reusable unit; the pool manages object lifecycle.

## 17. References
- Joshua Bloch, *Effective Java* — Items on creating/destroying objects, `equals`/`hashCode`.
- Java Language Specification, Ch. 8 (Classes), Ch. 12 (Execution): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- Oracle Java Tutorials, "Classes and Objects": https://docs.oracle.com/javase/tutorial/java/javaOO/
- Bjarne Stroustrup, *The C++ Programming Language* — classes and object model.
- Python docs, "Classes": https://docs.python.org/3/tutorial/classes.html
- GeeksForGeeks, "Classes and Objects in Java": https://www.geeksforgeeks.org/classes-objects-java/

## 18. Cheat Sheet
- Class = template/type (compile-time, shared code); Object = instance (runtime, own memory).
- One class → N objects; objects share method code, not state.
- Objects live on the heap; references live on the stack/fields; Java is pass-by-value (of reference).
- `==` compares references; `.equals()` compares state (when overridden).
- `new` = allocate + construct; GC reclaims when unreachable.
- Static = one per class; instance = one per object.
- `.class` / `getClass()` gives runtime class metadata (reflection).

## 19. Quiz
1. An object is: a) a template b) an instance of a class with own memory c) a method d) a package → **b**
2. `String s1 = new String("a"); String s2 = new String("a");` — `s1 == s2` is: a) true b) false c) compile error d) null → **b**
3. Java object lives on: a) stack b) heap c) metaspace d) registers → **b**
4. Static fields have: a) one copy per object b) one copy per class c) none d) per-thread → **b**
5. Class is to Object as: a) recipe is to dish b) dish is to recipe c) meal is to menu d) chef is to waiter → **a**
6. True or False: `Car c = new Car();` declares an object named `c`. → **False** — it declares a *reference* to an object.

## 20. Flashcards
- **Q: Class vs object?** → **A:** Class = blueprint/type, shared code; Object = instance with own allocated state.
- **Q: Where do objects and references live in Java?** → **A:** Objects on heap, references on stack or in fields.
- **Q: `==` vs `.equals()`?** → **A:** `==` compares references/identity; `.equals()` compares state if overridden.
- **Q: Is Java pass-by-value or by-reference?** → **A:** Pass-by-value; for objects the value passed is the reference.
- **Q: What's the `Class` object?** → **A:** Runtime metadata instance for a class, basis of reflection.
- **Q: Number of static copies?** → **A:** One per class; instance fields are one per object.

## 21. Revision
Classes are compile-time templates (type, shared code); objects are runtime instances with independent memory allocated by `new` on the heap, reached through references on the stack. All instances share method code but not state; static members are class-level. In Java, `==` compares reference identity, `.equals()` compares state (when overridden); Java is strictly pass-by-value, passing reference values for objects. The JVM adds a per-object header (mark word + klass pointer) enabling GC, locking, and dispatch. Master these micro-facts — they generate the first three minutes of every OOP interview.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Class vs object?" | Example / Formal Definition |
| "How many objects does `new String` create?" | Interview Q2 |
| "`==` vs `equals`?" | Interview Q3 / Flashcard |
| "Where do objects live in Java?" | Interview Q6 / Internal Working |
| "Is Java pass-by-value?" | Interview Q8 |
| "What's the `Class` object for?" | Interview Q14 / Industry Usage |
| "Why does an object need a header?" | Interview Q10 / Internal Working |
| "Static vs instance members?" | Interview Q15 |
