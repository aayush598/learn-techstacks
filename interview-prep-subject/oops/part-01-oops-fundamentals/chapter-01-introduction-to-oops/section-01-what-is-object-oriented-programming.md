# What is Object-Oriented Programming?

> **TL;DR**: Object-oriented programming (OOP) is a programming paradigm that models a system as a collection of self-contained "objects" — each bundling data (fields) and behavior (methods) — so that programs mirror real-world entities, hide implementation details, and can be extended safely.

## 1. Why Does This Exist?
OOP exists because the two earlier paradigms — unstructured (goto) and procedural programming — failed to scale as software grew from thousands to millions of lines. In procedural code, data structures (structs) and the functions that operate on them were separate; nothing enforced that `transferMoney()` could only be called on a `BankAccount`, so any function could mutate any record, causing coupling, duplication, and bugs. OOP solves this by *tying data and the operations on that data into one unit (the object)*, giving the programmer three guarantees procedural code never had: (1) data integrity through access control, (2) conceptual modeling that matches the problem domain, and (3) reusable, extendable building blocks. It exists for the same reason modular design exists everywhere — it is a **complexity-management strategy**, not a performance feature.

## 2. How Does It Work?
At its core, OOP works by:
1. Defining **classes** (templates) that declare what data a thing has and what it can do.
2. Creating **objects** (instances) at runtime via `new`; each object gets its own copy of instance fields.
3. Sending **messages** — calls like `account.withdraw(100)` — where the object decides how to respond.
4. Enforcing boundaries with **access modifiers** (`private`, `public`, etc.).
5. Enabling **dynamic dispatch** so the *actual* method run is decided at runtime based on the object's real type.

The mechanism relies on the compiler allocating memory for each instance and a dispatch table (vtable) that lets a call to an overridable method resolve to the right implementation at runtime.

## 3. When Is It Used?
- **Enterprise backends** — Spring (Java), Rails (Ruby), Django (Python) — where business entities (Order, Customer, Invoice) map naturally to classes.
- **GUI frameworks** — every window, button, and event is an object (Swing, Qt, SwiftUI).
- **Games** — each entity (Player, Enemy, Projectile) is an object with state and behavior.
- **Simulation / modeling** — banking, flight booking, inventory systems that mirror real-world entities.
- **Large teams** — where encapsulation and clear interfaces let many developers work on separate modules without stepping on each other.
- It is *not* the right tool for: high-performance numeric kernels, kernel drivers, simple scripts — where procedural/functional styles dominate.

## 4. Why Wasn't Another Approach Chosen?
Alternatives considered and rejected for the core use cases:
- **Pure procedural code** — rejected because global data + free functions cannot enforce invariants; one bug in one module corrupts another. OOP confines damage.
- **Functional programming (FP)** — FP is excellent for concurrency and pure data transformation, but its immutable data + functions model is awkward for systems dominated by mutable, identity-bearing entities (a bank account must change balance, not be re-created). OOP wins for *stateful, identity-heavy* domains; FP wins for *stateless transformation* domains. Modern languages blend both (immutable fields, records, streams).
- **Actor model / message passing only** — too heavyweight for ordinary applications; OOP keeps synchronous method calls.
The real answer: OOP wasn't chosen universally — it won for business software because it maps 1:1 to how domain experts think, reducing the cognitive gap between the requirement and the code.

## 5. Intuition
OOP is "organizing code the way the world is organized." A bakery doesn't have one global table of all flour, sugar, and eggs with free-floating functions; it has cakes (each with its own ingredients and its own `bake()`, `slice()`, `frost()`). If the baker changes how frosting works, only the cake objects need to change. You never worry that frosting flour will affect the bread. That is OOP: **each thing owns its data and its behavior, and the rest of the program only sees the thing's public face.**

## 6. Real-World Analogy
A **restaurant kitchen** is OOP in action. The Waiter is an object with state (table number, orders) and behavior (`takeOrder()`, `deliverFood()`). The Chef has private state (recipes) and a public method (`cook(order)`) — you never touch his knife drawer directly (encapsulation). The Menu is a template that produces many Dish objects. The manager can replace the "Italian Chef" with an "Indian Chef" who also implements the `cook()` method, and the waiter never notices — that's polymorphism through inheritance. Procedural programming is the equivalent of everyone grabbing ingredients from one shared pantry with no rules: faster for one cook, chaotic for a kitchen team.

## 7. Formal Definition
**Object-oriented programming (OOP)** is a programming paradigm based on the concept of *objects*, which are instances of *classes*. A class is a user-defined data type that encapsulates data (attributes/fields) and the operations on that data (methods) into a single unit. OOP is characterized by the four pillars: **encapsulation** (bundling + hiding data), **abstraction** (exposing only essential interfaces), **inheritance** (deriving new classes from existing ones), and **polymorphism** (one interface, multiple implementations, resolved at compile time or runtime).

## 8. Example
Consider modeling a `BankAccount`:
- Procedural approach: a struct `{double balance;}` plus functions `withdraw(balance, amt)` that every caller must remember to call. Nothing stops a buggy caller from writing `balance = -1000;` directly.
- OOP approach:

```java
public class BankAccount {
    private double balance;              // state, hidden
    public BankAccount(double initial) { // constructor
        if (initial < 0) throw new IllegalArgumentException();
        this.balance = initial;
    }
    public void withdraw(double amount) {
        if (amount > balance) throw new InsufficientFundsException();
        balance -= amount;               // behavior bundled with data
    }
    public double getBalance() { return balance; }
}
```
Now `withdraw()` is the *only* way money leaves the account, and the invariant "balance >= 0" is guaranteed. That single refactor is the entire motivation for OOP.

## 9. Internal Working
1. The compiler parses the class declaration and lays out a **layout plan**: each instance field gets an offset; each method gets an entry in the class's method table.
2. On `new BankAccount(1000)`, the runtime allocates memory for one object's instance fields (on the JVM heap, typically ~8 bytes header + field sizes), then runs the constructor to set initial values and establish invariants.
3. The object reference (a pointer) is stored in a local variable (on the stack).
4. A call `account.withdraw(100)` compiles to a dispatch: the runtime reads the object's type tag (via the vtable in C++/Java), finds `withdraw`, and invokes it *with the object itself as an implicit `this` parameter*.
5. Because `balance` is `private`, the bytecode verifier rejects any attempt by another class to access `account.balance` directly — protection is enforced even before runtime.

## 10. Time Complexity
- Object creation: O(1) amortized (bump-the-pointer allocation in JVM; C++ `new` uses malloc, typically O(1) for small sizes).
- Field access: O(1) — a fixed offset from the object base pointer.
- Method call (non-virtual): O(1) — direct address at compile time.
- Method call (virtual/dynamic): O(1) — single vtable indirection (constant time, independent of class hierarchy depth).
- Garbage collection of dead objects: amortized O(1) per object in modern collectors (generational GC), though full GC pauses exist.
- **Key interview point**: OOP adds *constant* overhead per operation; the paradigm's cost is design complexity, not asymptotics.

## 11. Advantages
- **Modularity and reusability**: classes are self-contained units that can be reused across projects.
- **Encapsulation/security**: data is protected from accidental or malicious modification.
- **Maintainability**: changes are localized to a class; the rest of the system is unaffected.
- **Modeling clarity**: code mirrors the problem domain, easing communication with non-programmers (domain experts).
- **Extensibility**: inheritance and polymorphism let you add new behavior without rewriting existing code.
- **Team-scale development**: clear interfaces let many engineers work in parallel.

## 12. Disadvantages
- **Performance overhead**: object indirection hurts cache locality; virtual dispatch prevents some inlining (mitigated by JIT devirtualization).
- **Memory footprint**: headers, vtables, and per-object metadata.
- **Complexity**: deep inheritance hierarchies become hard to reason about; the "gratuitous OOP" anti-pattern (over-abstraction) is real.
- **Steep learning curve**: concepts like dynamic dispatch are unintuitive to beginners.
- **Not always the right paradigm**: FP or procedural styles are better for pure data pipelines and high-perf numerics.
- **Testing friction**: object graphs are harder to mock than pure functions.

## 13. Interview Questions
1. **Q: What is object-oriented programming in one sentence?** A: A programming paradigm that models software as a collection of objects — each bundling data and behavior — to enable encapsulation, abstraction, inheritance, and polymorphism for modular, maintainable systems.
2. **Q: What are the four pillars of OOP?** A: Encapsulation (bundling + hiding data), Abstraction (exposing only the contract), Inheritance (IS-A reuse), and Polymorphism (one interface, multiple implementations). Many add Association/Aggregation/Composition as relationship pillars.
3. **Q: Which languages pioneered OOP?** A: Simula 67 (first OOP language, by Dahl & Nygaard, introduced classes) and Smalltalk (made OOP popular, pioneered "everything is an object"). C++ and Java made it mainstream.
4. **Q: Is Java 100% object-oriented?** A: No — it has primitives (`int`, `boolean`), `static` methods, and `String` immutability, all non-object constructs. Smalltalk is the classic "pure" OO language.
5. **Q: Can you do OOP in C?** A: Yes, manually — simulate classes with structs + function pointers and simulate `this` by passing a pointer (as the Linux kernel's `file_operations` struct does). This proves OOP is a discipline, not a language feature.
6. **Q: TRICKY — "OOP is slower than procedural, so why use it?"** A: For correctness and maintainability at scale; the constant-time overhead per call (see Section 10) is negligible relative to the cost of debugging a corrupted global state. Also, JITs often devirtualize and inline, closing the gap.
7. **Q: PRACTICAL — When would you NOT use OOP?** A: High-frequency numeric kernels (use C/vectorization), pure data transformation pipelines (FP), small scripts, and code where the domain has no natural identity-bearing entities.
8. **Q: PRODUCTION — How does OOP help a 200-engineer team ship in parallel?** A: Encapsulation gives each team a private sandbox; public interfaces become contracts; a change inside a class is invisible to others; inheritance + polymorphism let teams extend shared frameworks without modifying them.
9. **Q: SCENARIO — Your company has a giant class hierarchy that keeps breaking; what do you do?** A: Favor composition over inheritance, prefer interfaces over deep class trees, extract shared logic into collaborators, and apply SOLID (especially LSP) to catch is-a violations.
10. **Q: What is the difference between a paradigm and a design pattern?** A: A paradigm (OOP, FP) is a fundamental style of structuring programs; a pattern (Singleton, Strategy) is a reusable solution to a recurring design problem *within* a paradigm.
11. **Q: Is OOP a science or an engineering practice?** A: It is an engineering practice informed by experience (and by data on bug rates and maintenance costs); there is no formal proof that OOP reduces bugs — the evidence is empirical.
12. **Q: TRICKY — Your interviewer says "OOP is just glorified structs with function pointers." Respond.** A: Partly true in mechanism (see Q5), but wrong in effect — OOP adds *enforced* visibility, dynamic dispatch, inheritance, and a mental model, which change how reliably large systems can be built.
13. **Q: PRACTICAL — Design a `User` class: what fields, methods, and access levels?** A: `private` fields (`id`, `name`, `email`), a constructor validating input, `public` getters, and domain methods like `changeEmail(String)` that enforce policy — never expose fields directly.
14. **Q: What problem did OOP solve that structured programming couldn't?** A: Structured programming fixed control flow (gotos); OOP fixed *data organization* — the coupling between data and the code that must respect its invariants.
15. **Q: SCENARIO — A teammate writes everything as static utility classes. Critique.** A: It's procedural code in Java clothing; it defeats encapsulation, blocks polymorphic extension, and hard-codes dependencies, making it untestable without refactoring to injected collaborators.
16. **Q: What role do messages/`this` play in OOP?** A: `object.method(args)` is a message; the runtime passes the receiver as an implicit `this` argument, which is how the method accesses *that object's* state.

## 14. Follow-Up Questions
1. **Q: How is OOP different from object-based programming?** A: Object-based (e.g., JavaScript before ES6, early Visual Basic) uses objects and encapsulation but has *no inheritance or polymorphism*; OOP requires all four pillars.
2. **Q: Does OOP improve performance?** A: No — it slightly hurts it (indirection); it improves *development productivity and maintainability*, which is why business software uses it.
3. **Q: Why is OOP dominant in enterprise but rare in systems programming?** A: Enterprise values evolvability over performance; systems programming values control over abstraction. C++ is the middle ground (OOP only where it pays).
4. **Q: What are mixins and traits?** A: Reusable units of behavior shared across classes without single-inheritance constraints (Java interfaces with default methods, C++ CRTP, Scala traits, Ruby modules) — a hybrid of inheritance and composition.
5. **Q: Can FP and OOP coexist?** A: Yes — modern Java uses records, streams, and lambdas inside OO classes; domain *entities* stay objects while *transformations* become pure functions.

## 15. Coding Example
Same program — procedural (C) vs object-oriented (Java):

```c
// PROCEDURAL (C) — data and behavior separated
typedef struct { double balance; } Account;
void withdraw(Account* a, double amt) { a->balance -= amt; } // caller must pass a
// Danger: nothing stops:  a.balance = -1000;
```
```java
// OOP (Java) — data and behavior bundled, state protected
public class BankAccount {
    private double balance;                       // hidden state
    public BankAccount(double initial) {          // constructor enforces invariant
        if (initial < 0) throw new IllegalArgumentException("initial < 0");
        this.balance = initial;
    }
    public void withdraw(double amount) {
        if (amount <= 0)  throw new IllegalArgumentException("amount <= 0");
        if (amount > balance) throw new IllegalStateException("insufficient funds");
        balance -= amount;
    }
    public double getBalance() { return balance; }
    public static void main(String[] args) {
        BankAccount acc = new BankAccount(500);
        acc.withdraw(150);
        System.out.println(acc.getBalance());     // 350.0
    }
}
```
```python
# OOP (Python) — same idea, dynamic typing
class BankAccount:
    def __init__(self, initial: float):
        if initial < 0: raise ValueError("initial < 0")
        self.__balance = initial                 # name-mangled private state
    def withdraw(self, amount: float) -> None:
        if amount > self.__balance: raise ValueError("insufficient funds")
        self.__balance -= amount
    @property
    def balance(self) -> float:
        return self.__balance
```

## 16. Industry Usage
- **Java/Spring** — every business entity is a class; Spring beans are objects with injected dependencies; the framework itself is built on reflection + proxies (dynamic dispatch at runtime).
- **Amazon's internal Java services** — domain models map to `BankAccount`-style classes; Lambdas (serverless) still use POJOs for events.
- **Google** — Go supports OOP through interfaces + struct methods (no inheritance); Java/C++ used in Android and Ads.
- **Linux kernel** — C-style OOP: `struct file_operations` with function pointers is a manual vtable; the VFS (virtual filesystem) is a textbook example of polymorphism without language support.
- **Games (Unity/C#)** — every `MonoBehaviour` is an object with lifecycle hooks; component-based composition has largely replaced deep inheritance.
- **Trading systems (C++)** — low-latency OOP where virtual calls are banned on hot paths (manual function pointers and static polymorphism).

## 17. References
- Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software* (the "Gang of Four" book) — the OOP design vocabulary.
- Joshua Bloch, *Effective Java* — Java-specific OOP best practices.
- Bertrand Meyer, *Object-Oriented Software Construction* — the theory of Eiffel and design-by-contract.
- Grady Booch, *Object-Oriented Analysis and Design* — the canonical modeling text.
- Simula 67: Dahl & Nygaard, "SIMULA — an ALGOL-based simulation language".
- GeeksForGeeks, "Introduction of Object Oriented Programming": https://www.geeksforgeeks.org/introduction-of-object-oriented-programming/
- Java Language Specification, Ch. 8 (Classes): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html

## 18. Cheat Sheet
- OOP = objects (data + behavior) + 4 pillars: Encapsulation, Abstraction, Inheritance, Polymorphism.
- Created by Simula 67; popularized by Smalltalk; made mainstream by C++/Java.
- Object = runtime instance with its own memory; Class = compile-time template.
- Benefit = maintainability/reuse at scale; Cost = small constant-time overhead + design complexity.
- Not all OOP languages are pure: Java has primitives and static methods.
- One sentence answer: "OOP bundles data and behavior into objects to manage complexity via the four pillars."

## 19. Quiz
1. Which language is generally considered the *first* OOP language? a) Java b) Simula 67 c) Smalltalk d) C++ → **b**
2. Which pillar is "hide implementation details, expose only what's needed"? a) Polymorphism b) Inheritance c) Abstraction d) Encapsulation → **c** (encapsulation hides details too; abstraction is the *exposure of the contract* — the pairing matters)
3. A class is best described as: a) a living entity in memory b) a blueprint for objects c) a function pointer table d) a package → **b**
4. Which is NOT a benefit of OOP? a) improved worst-case runtime asymptotics b) modularity c) data protection d) reuse → **a** (OOP is about maintainability, not asymptotic speedup)
5. Java is NOT purely OOP because: a) it has `int`, `boolean` primitives b) it lacks classes c) it has no polymorphism d) it has no GC → **a**
6. True or False: In OOP, `object.method()` is a message sent to the object. → **True**

## 20. Flashcards
- **Q: What is OOP?** → **A:** A paradigm modeling software as objects that bundle data and behavior, built on encapsulation, abstraction, inheritance, and polymorphism.
- **Q: Name the four pillars.** → **A:** Encapsulation, Abstraction, Inheritance, Polymorphism.
- **Q: First OOP languages?** → **A:** Simula 67 (origin), Smalltalk (popularized), C++/Java (mainstream).
- **Q: Why does OOP exist?** → **A:** To manage complexity at scale — procedural code couldn't keep data and its invariants safe.
- **Q: Cost of OOP?** → **A:** Constant-time overhead per indirection/call; design complexity when overused.
- **Q: Is OOP faster than procedural?** → **A:** No — it's slower per-op but cheaper to maintain; JITs often close the gap.

## 21. Revision
OOP exists because procedural code couples data with operations only *conventionally*, so invariants break as systems grow. It models the world as objects — bundles of data (fields) and behavior (methods) defined by classes — and rests on four pillars: encapsulation (bundle + hide), abstraction (expose the contract), inheritance (IS-A reuse), and polymorphism (one interface, many implementations). Born in Simula 67 and popularized by Smalltalk, it became mainstream through C++ and Java. It costs a constant-time overhead per object operation and some design complexity, and it is the wrong tool for numeric kernels and pure data pipelines — but for stateful, identity-bearing business domains it is the dominant choice. First-30-seconds answers: class = blueprint, object = instance; and know the four pillars with one example each.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is OOP? Define it in one sentence." | Formal Definition / Why Does This Exist |
| "What are the four pillars?" | Four Pillars / Formal Definition |
| "Why was OOP invented? What did it solve?" | Why Does This Exist / Section 1 |
| "Class vs object?" | Example / Objects and Classes |
| "Is Java pure OOP? Why not?" | Interview Q4 |
| "When should I NOT use OOP?" | When Is It Used / Q7 |
| "OOP vs FP — how do you decide?" | Why Wasn't Another Approach Chosen |
| "How does OOP enable 200-engineer teams?" | Industry Usage / Q8 |
