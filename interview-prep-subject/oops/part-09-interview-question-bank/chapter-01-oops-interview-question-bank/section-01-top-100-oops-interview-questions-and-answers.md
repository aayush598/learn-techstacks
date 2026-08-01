# Top 100 OOPs Interview Questions and Answers

> **TL;DR**: The complete OOPs question bank — 100 questions ordered easy → medium → hard across every part of this resource, each with a 30-second model answer, a follow-up probe, and the source section to revisit if your answer feels thin.

## 1. Why Does This Exist?
Interviewers recycle a well-known set of OOPs questions because they reveal depth in seconds: one follow-up ("why is that important?") separates memorized answers from understanding. This bank exists to (1) cover every concept in Parts 01-08 as a *question*, (2) give a crisp, correct 30-second answer you can say out loud, and (3) map each question to its theory section so you can deepen any weak spot. Practicing with this list converts passive reading into the active recall that interviews actually test.

## 2. How Does It Work?
Questions are grouped by the parts they draw from, and ordered easy → hard. Each entry has: **Q**, a **30-second answer** (what to say), and a **Follow-up** (the probe to expect, with the reasoning). Use the checkboxes to track. In an interview, never recite the answer word-for-word — say it, then *apply* it to a small example; interviewers reward an example far more than a definition.

## 3. When Is It Used?
- **Practice mode** (weeks before): go section by section, answer aloud, then read the model answer.
- **Mock mode** (week before): random questions, timed 45 seconds each, with follow-ups.
- **Weak-spot hunting**: mark anything you can't answer in 30 seconds and re-read that source part.
- **Final review**: skim Section 05 (crash course) after this bank.

## 4. Why Wasn't Another Approach Chosen?
Memorizing only *answers* fails because interviewers vary wording and add follow-ups. Memorizing only *theory* fails because you can't produce answers fast enough. This bank is the bridge: full coverage (so no surprise), compressed answers (so they're sayable), and source references (so depth is one click away). Flashcards (Section 20 of each theory file) are the spaced-repetition companion; this list is the exam-mode drill.

## 5. Intuition
Think of this as a **flight of stairs**: the first questions (what is a class?) are the ground floor — anyone can answer. The middle (abstract vs interface, diamond problem) is mid-flight — you need real understanding. The top (design a cache, memory model, v-tables) is the penthouse — reserved for candidates who can apply concepts. Interviewers climb the stairs with you: they start easy, and how high you get is your score.

## 6. Real-World Analogy
A **sommelier's tasting**: the interviewer hands you 100 wines (questions) over your career; most are familiar labels, some are rare vintages. Tasting blind (no notes) you must recognize the grape (the concept), name the region (the context), and suggest a pairing (an example). This bank is your "tasting notes" — knowing the labels cold means you never fumble the pour.

## 7. Formal Definition
An interview question bank is a structured set of prompt-answer pairs that (a) covers the full knowledge domain (classes, objects, pillars, relationships, SOLID, patterns, language internals), (b) ranks items by cognitive difficulty (recall → comprehension → application → design), and (c) includes follow-up probes that test for conceptual transfer rather than rote recall.

## 8. Example
**Q: "What is the difference between an abstract class and an interface?"**
Answer (30s): "An abstract class can have instance state, constructors, and concrete methods; a class can extend only one. An interface (Java 8+) declares abstract methods and can have default/static methods, but (pre-9) no instance fields and a class can implement many. Use an abstract class for a shared *base implementation*; use an interface for a *capability contract*."
Follow-up: "When would you pick one over the other?" → "When multiple classes share behavior + state → abstract class; when unrelated classes must share a contract or you need multiple inheritance → interface."
Source: Part 02, section-02-abstract-classes-vs-interfaces.

## 9. Internal Working
To *use* this bank effectively: 1) Attempt the answer aloud before reading it. 2) Compare with the model answer — note the *structure* (define → contrast → when-to-use → example). 3) Answer the follow-up; if you can't, the concept is weak — re-read the mapped section. 4) Re-test the weak ones after 24h and 7d (spaced repetition). 5) Build a "final 10" list — your personal most-likely-to-be-asked — and drill those daily.

## 10. Time Complexity
- Answering each question: target ≤ 30 seconds (recall) — 100 questions ≈ 1 hour of drilling.
- Full pass: ~50-75 minutes if you answer first and verify.
- Mock mode (random 20 + follow-ups): ~20 minutes per mock.

## 11. Advantages
- Full coverage: every concept from Parts 01-08 appears as a question.
- Answers are sized to say aloud (not essay-length).
- Every answer maps to a source section for deep-dive.
- Ordered by difficulty → measurable progress.
- Follow-ups train the exact probing style of real interviewers.

## 12. Disadvantages
- Static: real interviews invent scenario-based variants — you must *apply*, not memorize.
- Language-specific answers (Java-heavy) may need adaptation for C++/Python interviews.
- No substitute for coding practice (Section 02) and LLD (Section 03).
- Volume can feel overwhelming; prioritize the "high-frequency" flags and your target company's heatmap (Section 04).

## 13. Interview Questions

### Part 01 — OOPs Fundamentals (Q1-Q15)
1. **What is Object-Oriented Programming?** A: A paradigm that models a system as *objects* — bundles of state (fields) and behavior (methods) — communicating via messages, contrasted with procedural code that operates on passive data structures.
2. **What is a class vs an object?** A: A class is the blueprint (type) defining fields/methods; an object is a runtime *instance* with its own state. `class Dog {}` + `new Dog()` = object. Follow-up: "How many objects from one class?" → unlimited, each with independent state.
3. **What are the four pillars of OOP?** A: Encapsulation (bundle + hide state), Abstraction (expose essentials, hide implementation), Inheritance (derive classes from bases), Polymorphism (one interface, many forms). Follow-up: "Which pillar does `private` serve?" → encapsulation.
4. **What is the difference between procedural and OOP?** A: Procedural = functions + data separated, data flows through functions; OOP = data + the functions that operate on it are bound into objects, enabling reuse via inheritance and behavior swaps via polymorphism.
5. **What is state vs behavior vs identity?** A: State = values of fields; behavior = methods; identity = which instance it is (reference/address). Two equal objects still have distinct identity.
6. **What is the difference between `==` and `equals` (Java)?** A: `==` compares references (identity); `equals` compares logical content (overridable). Default `Object.equals` is identity, so override for value equality.
7. **What is a constructor and why can't it be virtual/static?** A: It initializes a new object; can't be virtual because no object exists yet to dispatch through; can't be static in the sense of producing an existing instance (Java has no static ctor, C++/C# do).
8. **What is a copy constructor / clone?** A: Creates a new object as a copy of another (deep vs shallow). In Java it's `clone()` (shallow by default) — prefer copy constructors/factories; C++ has real copy ctors (see Part 08).
9. **What is the purpose of a `main` method?** A: The JVM/OS entry point that starts a program; in Java: `public static void main(String[] args)` — `public` (JVM calls it from outside), `static` (no instance yet), `void` (JVM ignores return).
10. **What is garbage collection in one line?** A: Automatic reclamation of objects no longer reachable from GC roots, freeing programmers from manual `free` (see Part 08 section 01).
11. **What is method overloading?** A: Same method name, different parameter lists in the *same* class — resolved at *compile time* (static polymorphism). Return type alone is not enough.
12. **What is method overriding?** A: Subclass redefines a base method with the same signature — resolved at *runtime* (dynamic dispatch via v-table in C++ / JVM invokevirtual in Java).
13. **Overloading vs overriding?** A: Overloading = compile-time, same class, different params; overriding = runtime, subclass, same signature, requires inheritance; overriding uses `@Override`, cannot reduce visibility (Java).
14. **What is a `static` member?** A: Belongs to the *class*, not instances; one copy shared by all; accessed via class name; can't access instance members from a static context.
15. **What is the `this` keyword?** A: A reference to the current instance, used to disambiguate field vs parameter and to chain constructors (`this(...)`).

### Part 02 — Encapsulation & Abstraction (Q16-Q25)
16. **What is encapsulation?** A: Bundling data + methods and *hiding* internal state behind access control (private fields, public methods), so state changes only through the class's contract.
17. **Why hide data (information hiding)?** A: Prevents inconsistent state, allows implementation to change without breaking callers, and enforces invariants (e.g., no negative balance).
18. **What is abstraction?** A: Exposing *what* an object does (its contract) while hiding *how* (implementation) — via abstract classes and interfaces.
19. **Encapsulation vs abstraction?** A: Encapsulation = hiding *state* (data protection); abstraction = hiding *implementation* (behavior contract). Encapsulation is the *how*; abstraction is the *what*.
20. **Abstract class vs interface (Java)?** A: Abstract class: state, ctors, concrete methods, single inheritance. Interface: contract of abstract methods + default/static methods, multiple implementation; prefer interface for contracts, abstract class for shared base implementation.
21. **Can an interface have fields?** A: Only `public static final` constants (Java ≤8); Java 9+ added private methods; instance fields remain disallowed — implement with abstract classes.
22. **Can an abstract class be instantiated?** A: No — `new AbstractX()` is a compile error; only concrete subclasses that implement all abstract methods can be instantiated.
23. **What are getters/setters and when are they wrong?** A: Controlled access to private fields (validation, lazy init). Wrong when they expose internals pointlessly (no logic) — prefer behavior methods that keep state valid.
24. **What is the default access modifier in Java?** A: Package-private — visible within the same package only.
25. **Why is `String` effectively the most common immutable class?** A: Final class, final char[] (now byte[]), no mutators — gives thread-safety, pooling, cached hash.

### Part 03 — Inheritance (Q26-Q38)
26. **What is inheritance?** A: A class derives from a base, reusing state/methods and enabling substitution (IS-A). Java: single inheritance of classes, multiple of interfaces.
27. **Types of inheritance?** A: Single, multilevel (A→B→C), hierarchical (one base many derived), multiple (a class inherits from many — Java via interfaces, C++ directly), hybrid = multiple + hierarchical (diamond).
28. **What is the diamond problem?** A: `class D(A, B)` where A and B both extend Base — which `Base` method wins? Java classes: resolved by the *leftmost/compile-time* linear order (and interfaces have rules); C++: ambiguous, must disambiguate; Python: C3 MRO (Part 08).
29. **Composition vs inheritance?** A: Inheritance = IS-A (rigid, couples to base implementation, breaks with fragile-base-class); composition = HAS-A (delegates behavior, flexible, favors interfaces). Prefer composition unless a true IS-A with behavior reuse exists.
30. **What is the `super` keyword?** A: Refers to the parent — `super.method()`, `super()` for base ctor; in Python it's cooperative MRO-next (Part 08).
31. **Can a subclass access private members of its parent?** A: No — private is not inherited; use protected (or package-private) for subclass access.
32. **What is `protected` vs `default` vs `public`?** A: protected = package + subclasses; default = package only; public = everywhere. (Also `private` = class only.)
33. **Can you override a `static` method?** A: No — static methods are *hidden* (not overridden); calling via subclass name resolves statically to the compile-time type. `@Override` on static is a compile error.
34. **Can you override a `private` method?** A: No — private methods aren't inherited, so a same-named method in the subclass is a *new* method (not an override).
35. **What is the fragile base class problem?** A: Changes to a base class silently change derived behavior — inheritance couples subclasses to base implementation; mitigated by final, interfaces, composition.
36. **What does `final` on a class/method do?** A: Final class = cannot be subclassed (e.g., `String`); final method = cannot be overridden.
37. **Can you prevent inheritance?** A: Java: `final` class; C++: non-virtual dtor/private ctor; Python: `__new__`/metaclass tricks — but prefer composition.
38. **What is Liskov Substitution (one-liner)?** A: Subtypes must be substitutable for their base without breaking correctness — derived classes must honor the base's contract.

### Part 04 — Polymorphism (Q39-Q48)
39. **What is polymorphism?** A: One interface, many implementations: the same call behaves differently based on the actual (dynamic) object type.
40. **Compile-time vs runtime polymorphism?** A: Compile-time = overloading/operator overloading (decided at compile time); runtime = overriding/virtual dispatch (decided at runtime via v-table/JVM dispatch).
41. **How does overriding actually work in Java?** A: `invokevirtual` on a method — the JVM looks up the method in the object's class (its v-table equivalent), so `Shape.draw` called on a `Circle` runs `Circle.draw`.
42. **Can overriding change the return type?** A: Yes for *covariant* return types (subtype of the base's return) — Java allows it; C++ does too.
43. **Can overriding reduce visibility?** A: No — a subclass can't reduce access (must be same or more visible); increasing visibility is allowed.
44. **What is method hiding vs overriding?** A: Static methods are hidden (compile-time, based on static type); instance methods are overridden (runtime, based on dynamic type).
45. **What is operator overloading?** A: Defining operator behavior for user types (`+`, `==`); Java doesn't support it (except `+` for String), C++ and Python do (dunders).
46. **What is duck typing?** A: "If it quacks, treat it as a duck" — an object's *behavior* (methods present) determines usability, not its declared type; Python's default.
47. **Virtual functions in C++?** A: A method declared `virtual` is dispatched through the v-table by dynamic type; non-virtual calls bind to the static type.
48. **What is `@Override` for?** A: A compile-time check that the method truly overrides a base method — catching signature typos early.

### Part 05 — Object Relationships (Q49-Q56)
49. **Association vs aggregation vs composition?** A: Association = general "uses" link; aggregation = HAS-A with independent lifetimes (library → books); composition = HAS-A with owned lifetimes (house → rooms die with the house).
50. **What is a dependency?** A: The weakest relationship — a class *uses* another temporarily (a parameter or local), no field holding it.
51. **Why prefer composition over inheritance?** A: Composition is flexible (swap behavior via delegation), respects encapsulation, avoids fragile-base and deep coupling; inheritance exposes base internals and is rigid.
52. **What is delegation?** A: An object forwards a request to a contained object — the classic way composition implements behavior reuse.
53. **How do you model a UML "has-a" relationship?** A: A diamond + multiplicity (1..*, 0..1): filled diamond = composition, hollow = aggregation.
54. **What is a one-to-many relationship?** A: One object references many (e.g., a `Department` has many `Employee`s); modeled with a collection field.
55. **What is the difference between IS-A and HAS-A?** A: IS-A = inheritance (a Dog is a Animal); HAS-A = composition/aggregation (a Car has an Engine). Use HAS-A unless IS-A is genuine and stable.
56. **When is inheritance actually justified?** A: A true IS-A with shared behavior, no fragile-base risk, and substitutability (LSP) — e.g., domain taxonomies, framework base classes, template-method patterns.

### Part 06 — SOLID (Q57-Q66)
57. **What are the SOLID principles?** A: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
58. **SRP in one line?** A: A class should have one reason to change — one responsibility (e.g., separate persistence from business logic).
59. **OCP in one line?** A: Open for extension, closed for modification — add behavior via subclassing/strategies/interfaces, not by editing working code.
60. **LSP violation example?** A: A `Square` subclassing `Rectangle` breaks `setWidth`/`setHeight` behavior (a square can't have different width/height) — classic LSP violation; prefer composition.
61. **ISP in one line?** A: Clients shouldn't depend on methods they don't use — split fat interfaces into focused ones.
62. **DIP in one line?** A: Depend on abstractions (interfaces), not concretions; high-level modules shouldn't depend on low-level modules — invert with interfaces.
63. **Why is DIP important in practice?** A: It enables dependency injection (Spring), swapping implementations (DB → cache), and testability (mock interfaces).
64. **What does SRP imply for a "God object"?** A: God objects (doing everything) violate SRP → split into focused classes with single responsibilities.
65. **How do SOLID principles relate to design patterns?** A: Patterns are the *solutions*; SOLID are the *rules* — e.g., Strategy = OCP + DIP; Observer = OCP; Builder = SRP for construction.
66. **Can SOLID be over-applied?** A: Yes — over-abstraction adds indirection and complexity for small codebases; apply pragmatically.

### Part 07 — Design Patterns (Q67-Q78)
67. **What are design patterns?** A: Reusable solutions to recurring design problems — named, documented solutions from the GoF book, categorized as creational/structural/behavioral.
68. **Singleton — when and how (thread-safe)?** A: One instance globally (config, connection pool); use an enum or a holder class (lazy, thread-safe via JVM class init) or double-checked locking with `volatile`.
69. **Why is Singleton often called an anti-pattern?** A: Hides dependencies, breaks testability (global state), violates SRP; prefer DI + a single scoped instance.
70. **Factory vs Abstract Factory?** A: Factory Method = one factory method creating one product; Abstract Factory = an interface for families of related products (e.g., UI widgets per OS).
71. **Builder — when?** A: When construction has many optional parameters or is multi-step; Java example: `StringBuilder`, `Lombok @Builder`, `java.time` builders; improves immutability + readability.
72. **Adapter vs Facade?** A: Adapter makes an *existing* interface usable by a client expecting a *different* interface (conversion); Facade provides a *simplified* interface to a complex subsystem.
73. **Proxy vs Decorator?** A: Proxy controls *access* to the target (lazy, remote, security — same interface); Decorator adds *behavior* dynamically (wraps with extra responsibility). Both wrap, but intent differs.
74. **Strategy vs State?** A: Strategy: client *selects* an interchangeable algorithm at runtime (e.g., sorting, payment). State: the object's *internal state* changes behavior automatically as state changes (finite state machine).
75. **Observer — when?** A: When many objects must react to a subject's changes (event listeners, pub/sub, MVC) — subject notifies observers; Java: `Observable`/`EventListener`, Spring events.
76. **Command — when?** A: Encapsulate an action as an object — for undo/redo, queuing, transactional operations (e.g., editor undo stack).
77. **Which patterns are used in Spring?** A: Singleton (beans default), Factory/FactoryBean, Proxy (AOP), Template Method (`JdbcTemplate`), Observer (event listeners), Dependency Injection (DIP), Strategy, Decorator (annotations-as-wrappers).
78. **What is the difference between a pattern and a principle?** A: A principle is a rule of design (SOLID); a pattern is a *reusable recipe* that applies principles to a concrete recurring problem.

### Part 08 — Language Internals (Q79-Q90)
79. **Where do Java objects live?** A: Heap; references on stacks/fields; class metadata in Metaspace; GC reclaims unreachable objects (young-gen copying, old-gen mark-sweep).
80. **What is type erasure?** A: Generic type params replaced by bounds at compile time; `List<String>` and `List<Integer>` are the same runtime `List`; can't `new T()`, `instanceof T`.
81. **What is PECS?** A: Producer Extends, Consumer Super — `? extends T` for reading, `? super T` for writing collections.
82. **How do you make a class immutable?** A: Final class + final fields + no mutators + defensive copies + no leaking mutable internals (Effective Java Item 17); JLS §17.5 gives lock-free safe publication.
83. **What is the Java Memory Model?** A: JLS §17.4 happens-before rules governing cross-thread visibility/ordering — volatile, synchronized, final-field semantics.
84. **Checked vs unchecked exceptions in Java?** A: Checked must be caught/declared (compiler); unchecked = `RuntimeException`/`Error`. Modern practice: prefer unchecked for most cases.
85. **What is a virtual function in C++?** A: A method dispatched via the v-table by dynamic type; cost = one indirect load; requires virtual dtor when deleting via base.
86. **What is RTTI / `dynamic_cast`?** A: Runtime type info (typeid, type_info in v-table); `dynamic_cast` safely downcasts → nullptr/bad_cast on failure; needs a polymorphic type.
87. **Rule of Three / Five (C++)?** A: If a class needs a custom destructor, it needs copy ctor + copy assignment (Three); C++11 adds move ctor + move assignment (Five); `std::move` enables moves.
88. **`unique_ptr` vs `shared_ptr`?** A: unique = sole ownership, move-only, zero overhead; shared = atomic refcount, copies share ownership, last owner frees; weak_ptr breaks cycles.
89. **What is the Python MRO / `super()`?** A: C3 linearization determines lookup order (`D(A,B)` → D,A,B,Base); `super()` cooperatively calls the next class in the MRO so `__init__`s run once each.
90. **Why does defining `__eq__` break hashing in Python?** A: `__hash__` is set to None → objects unhashable; restore `__hash__` explicitly (equal objects must hash equally).

### Scenario-Based & Design (Q91-Q100)
91. **Design a parking lot (LLD) — key classes?** A: `ParkingLot`, `Floor`, `ParkingSpot` (types), `Vehicle` (abstract: Car/Motorcycle/Truck), `Ticket`, `Payment`, `ParkingDisplay`. Strategy per spot-type, Observer for display updates (see Part 09 section 03 for the full design).
92. **How would you model a chess game?** A: `ChessBoard` (8x8 `Square`s), abstract `Piece` with `canMove(from,to)` + concrete `Pawn`/`Rook`/…, `Game` (state machine), `Player`, `Move`, `MoveValidator` (Strategy). Polymorphism handles "which piece" logic.
93. **Design an LRU cache.** A: `HashMap<K,Node>` + doubly-linked list: get/put O(1); on access move node to head; evict tail when full (see Section 02 solution).
94. **How would you make a class both thread-safe and efficient?** A: Immutability first (Part 08), else synchronized/ConcurrentHashMap/atomics; avoid locking hot read paths; use copy-on-write where reads dominate.
95. **"Your colleague stored `java.util.Date` in a `HashMap` key — why does the lookup fail?"** A: Date is mutable; changing the key changes hashCode → the entry is stranded in the old bucket; use immutable keys.
96. **How do you handle failures in a long chain of operations?** A: Command + undo stack, or try-with-resources / transactional boundaries; design for compensation (saga-style) at scale.
97. **Design a vending machine.** A: `VendingMachine` state machine (Idle/Ready/Dispensing/OutOfStock), `Product`, `Money`, `Inventory`; State pattern for transitions; commands for operations (see Section 02).
98. **What patterns would you use for a notification system?** A: Observer (subscribers to events), Strategy (different channels: email/SMS/push), Factory (create notification per channel), Builder (optional payload fields).
99. **How do you test OOP code?** A: Unit test each class in isolation by mocking interfaces (DIP helps); test invariants; use TDD for behavior; integration tests for composition boundaries.
100. **"Explain your last OOP design decision."** A: Pick a real example and walk: problem → alternatives → why chosen (SOLID/pattern) → trade-offs. This question tests whether you *apply* OOP, not just know it.

## 14. Follow-Up Questions
1. **"Is there another way to achieve this without inheritance?"** → Composition + interfaces (delegation); list a concrete swap.
2. **"What happens at runtime if two interfaces define the same default method?"** → Java requires the class to override or specify `InterfaceName.super.method()`.
3. **"How would you make this design testable?"** → DIP + constructor injection + mocking interfaces; avoid singletons.
4. **"What's the cost of your approach?"** → Be honest: memory (vptr), GC pressure (immutability), thread contention, code complexity.
5. **"Can you draw the class diagram?"** → Always be ready with the core classes + relationships for any design you discuss.

## 15. Coding Example
```java
// The "answer every question with an example" skill:
// Q: "Explain polymorphism" -> show this immediately
interface Payment { void pay(int cents); }

class CardPayment implements Payment { public void pay(int c) { /* charge card */ } }
class WalletPayment implements Payment { public void pay(int c) { /* debit wallet */ } }

void checkout(Payment p, int amount) { p.pay(amount); }  // one call, many behaviors
```
```python
# Q: "What is duck typing?" -> show this
def total_price(items):            # any iterable of any objects with price
    return sum(i.price for i in items)
```

## 16. Industry Usage
- **Interview prep platforms** (LeetCode system-design/OOP tags, InterviewBit OOP questions, Educative LLD courses) mirror this exact bank.
- **Company question repositories** (Glassdoor/AmbitionBox interview transcripts) show these 100 questions re-appear with high frequency across Amazon, Google, Microsoft, Flipkart, Walmart, and JVM/C++ shops (see Section 04 for heatmaps).
- **Internal interviewers** reuse a standard question set because the *follow-up* is what discriminates — this bank's follow-ups are the differentiation training.

## 17. References
- Parts 01-08 of this resource (each question's source section is linked in its answer).
- "Cracking the Coding Interview" (McDowell) — OOP + design chapters.
- "System Design Interview" (Xu) — LLD/design methodology for Section 03.
- LeetCode "Object Oriented Programming" / design problem tags.
- Educative / InterviewBit OOP course question sets.
- Refactoring Guru — pattern questions (Q67-78) cross-reference its catalog.

## 18. Cheat Sheet
- Answer formula: **define → contrast → when-to-use → example** (30 seconds total).
- Four pillars: Encapsulation (hide state), Abstraction (hide impl), Inheritance (IS-A), Polymorphism (one interface, many forms).
- Abstract vs interface: state/impl vs contract/multiple.
- Composition > inheritance by default; IS-A only when true.
- SOLID: SRP OCP LSP ISP DIP — patterns implement these.
- Singleton = thread-safe enum/holder; often an anti-pattern.
- Java: objects in heap; erasure; PECS; §17.5 immutability.
- C++: v-table + virtual dtor + RTTI; Rule of Five; move.
- Python: C3 MRO; cooperative `super()`; dunders; `__eq__` kills `__hash__`.
- Always close with an example; always expect a follow-up.

## 19. Quiz
1. Which is compile-time polymorphism? a) Overriding b) Overloading c) Virtual dispatch d) Dynamic cast → **b**
2. LSP is violated when: a) A subclass narrows behavior b) A subclass adds methods c) Composition is used d) Interfaces are used → **a**
3. `String` is immutable largely because of: a) Speed of `+` b) Thread-safety/pooling/hash caching c) Serialization d) GC → **b**
4. Singleton thread-safety best practice: a) `synchronized` every getter b) enum or holder class c) Double-check without volatile d) `static` instance → **b**
5. Java generics at runtime: a) Type-checked b) Erased c) Refied d) Inlined → **b**
6. `dynamic_cast` on a pointer fails by returning: a) Throws b) nullptr c) UB d) `void*` → **b**
7. Python diamond `D(A,B)` MRO order: a) D,B,A,Base b) D,A,B,Base c) Base first d) Object first → **b**
8. The strongest ownership relationship: a) Association b) Aggregation c) Composition d) Dependency → **c**
9. Which pattern adds behavior dynamically at runtime? a) Adapter b) Decorator c) Facade d) Proxy → **b**
10. `__eq__` without `__hash__` in Python makes objects: a) Faster b) Unhashable c) Immutable d) Callable → **b**

## 20. Flashcards
- **Q: Answer structure?** → **A:** Define → contrast → when-to-use → example, in ≤30s.
- **Q: Four pillars?** → **A:** Encapsulation, Abstraction, Inheritance, Polymorphism.
- **Q: Composition or inheritance?** → **A:** Composition by default; inheritance only for true IS-A with behavior reuse.
- **Q: Abstract vs interface?** → **A:** State/impl + single vs contract + multiple.
- **Q: SOLID letters?** → **A:** SRP, OCP, LSP, ISP, DIP.
- **Q: Java objects where?** → **A:** Heap; refs on stacks; metadata Metaspace; GC by reachability.
- **Q: PECS?** → **A:** Producer Extends, Consumer Super.
- **Q: Rule of Five?** → **A:** dtor + copy ctor/assign + move ctor/assign.
- **Q: Python MRO basis?** → **A:** C3 linearization; `super()` = next in MRO.
- **Q: Why prefer immutable keys?** → **A:** hashCode must not change while in a map.

## 21. Revision
Answer formula: define → contrast → when → example. Know the pillars, SOLID, and the abstract/interface distinction cold. Patterns: identify the intent (Singleton=one, Factory=creation, Adapter=convert, Decorator=extend, Proxy=control access, Strategy=swap algorithm, Observer=notify, Command=action object). Language internals: Java (heap/GC, erasure/PECS, immutability §17.5, checked vs unchecked), C++ (v-table + virtual dtor, RTTI/dynamic_cast, Rule of Five, unique/shared/weak_ptr), Python (C3 MRO, cooperative super(), dunders, __eq__ kills __hash__). Always end with a tiny example and expect a follow-up. This bank's Q91-100 (design + scenario) are the ones that move you from "knows OOP" to "hired for OOP."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Top 100 bank — which questions?" | 13 Interview Questions (all) |
| "How should I structure an OOP answer?" | 18 Cheat Sheet / 8 Example |
| "Which questions are company-specific?" | Section 04 (company heatmaps) |
| "Where do I practice the coding prompts?" | Section 02 (coding problems) |
| "Where's the full LLD walkthrough?" | Section 03 (LLD guide) |
| "What do I revise the night before?" | Section 05 (crash course) + this section's Revision |
