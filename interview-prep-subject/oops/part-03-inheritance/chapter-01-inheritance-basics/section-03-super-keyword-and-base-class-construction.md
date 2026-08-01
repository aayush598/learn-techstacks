# `super` and Base Class Construction

> **TL;DR**: `super` is the subclass's handle to its parent — `super(...)` chains constructor calls (guaranteeing the parent is fully built before the child body runs) and `super.method()` reaches parent implementations that the subclass has overridden.

## 1. Why Does This Exist?
When a subclass is created, two things must happen in the right order: the *parent's* part of the object must be initialized (its invariants established — fields set, validation done) and then the *subclass's* part. Without a `super(...)` call, there'd be no way to pass arguments up to the parent's constructor, and the JVM couldn't guarantee ordering. `super.method()` exists because overriding creates a shadow: once `Dog` overrides `speak()`, the inherited *behavior* is no longer directly callable by its old name inside `Dog` — you need `super.speak()` to invoke the parent's version (essential for template methods that want to extend, not replace, base logic). The two faces of `super` answer the two problems inheritance creates: *how do I initialize the inherited part?* and *how do I reach the behavior I overrode?*

## 2. How Does It Work?
- **`super(...)`** — constructor delegation, must be the *first statement* of a subclass constructor. If omitted, `super()` (no-arg) is inserted implicitly. Chains up: `new Suv()` → `Suv ctor` → `Car ctor` → `Vehicle ctor` → `Object ctor` → bodies run top-down (parent body after its constructor chain).
- **`super.method(args)`** — invokes the *immediate parent's* implementation of an overridden method, from within the subclass.
- **`super.field`** — accesses a parent field hidden by a same-named subclass field (rare, discouraged).
- `super` is NOT a reference you can store or pass (unlike `this`) — it's a compiler directive resolved at compile time for constructors, and a direct-call directive for methods (no virtual dispatch past the parent).

## 3. When Is It Used?
- **Constructor chaining**: always (implicitly or explicitly) — every subclass constructor calls a parent constructor.
- **Extending overridden methods**: `@Override public void speak() { super.speak(); log("Dog barked"); }` — the "call super then add" pattern.
- **Template methods**: subclass hooks call `super.hook()` to run base logic then customize.
- **Reaching parent state**: `super.field` when the subclass shadows a field (usually a smell — avoid shadowing).
- **Framework subclasses**: `super.onCreate(savedInstanceState)` is the Android invariant — forgetting it breaks the framework.

## 4. Why Wasn't Another Approach Chosen?
- *Why not let the JVM auto-initialize the parent with defaults and skip `super(...)`?* Then the parent might be created with invalid/absent values — the parent's constructor invariants (validation, resource setup) would never run. Explicit/implicit `super(...)` chosen so parent initialization is *always* executed with the right arguments.
- *Why must `super(...)` be first?* So the parent is fully constructed before the subclass body runs — otherwise the subclass body could touch inherited state before it exists, or the parent constructor could be affected by subclass state. Java chose strict ordering: first statement, enforced at compile time.
- *Why not allow storing `super` like `this`?* Because the parent isn't a separate object — it's the *same object* viewed as a base. `super.method()` compiles to a direct call to the parent's code with `this`; storing "the parent" would imply two objects. That's why `super` is a keyword, not a value.
- *Why not use a virtual call for `super.method()`?* It must *not* re-dispatch to the subclass (that would infinitely recurse in the "extend" pattern); `super` means "the parent's implementation, exactly" — a direct, non-virtual call.

## 5. Intuition
`super` is like **addressing the parent generation in a family business**. `super(...)` is "ask the parent to do their onboarding first" — the child's first act is always "start with what the parent set up." `super.method()` is "do what my parents did, then I'll add my twist" — you literally say "like my parent does it, plus ..." When the company (object) is created, the elders' onboarding (constructor chain) completes before the new hire's.

## 6. Real-World Analogy
A **medical resident**. `super(...)` = the residency program requires the med school foundation first: you can't operate (run your constructor body) until the residency director (parent constructor) confirms your credentials. `super.method()` = when the resident treats a patient, they "call the attending's protocol" (`super.treat()`) and then add their own notes — extending the standard care rather than replacing it. The attending's protocol and the resident's additions both run on the *same patient* (same object) — `super` isn't a different doctor; it's the same doctor following the senior's procedure.

## 7. Formal Definition
In Java, `super` is a keyword used in two ways. (1) **`super(args...)`**: a constructor invocation expression that must be the first statement of a constructor body; it invokes the direct superclass's constructor, and if absent, a no-argument `super()` is implicitly inserted (a compile error if the superclass lacks a no-arg constructor). Construction proceeds from `Object` downward: each class's fields/initializers run, then its constructor body, so the parent is fully initialized before any subclass code executes. (2) **`super.member`**: an access to a member of the direct superclass that is overridden/hidden by the subclass; `super.method(...)` is a *non-virtual* call (binds to the immediate parent's implementation). `super` is not a first-class reference; it is only valid within instance methods and constructors of the subclass.

## 8. Example
```java
public class Animal {
    protected String name;
    public Animal(String name) { this.name = name; }          // parent ctor sets invariant
    public void speak() { System.out.println(name + " makes a sound"); }
}
public class Dog extends Animal {
    public Dog(String name) { super(name); }                  // MUST be first statement
    @Override
    public void speak() {
        super.speak();                                        // run parent logic first
        System.out.println(name + " barks loudly");           // then add Dog behavior
    }
}
public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog("Rex");
        rex.speak();
        // OUTPUT:
        // "Rex makes a sound"
        // "Rex barks loudly"
    }
}
```
Construction: `super(name)` runs `Animal`'s constructor (sets `name="Rex"`), then the `Dog` body runs (empty). Override: `super.speak()` calls `Animal.speak()` non-virtually, then the Dog adds its line — the canonical "extend, don't replace" pattern.

## 9. Internal Working
1. `new Dog("Rex")` → JVM allocates the Dog object (layout = Animal fields + Dog fields).
2. Constructor invocation: `Dog` ctor → `super(name)` → `Animal` ctor → `super()` → `Object` ctor. Each returns, then its body runs top-down.
3. Field initializers of each class run *before* that class's constructor body, in source order (parent's before child's, because parent ctor completes first).
4. `super.speak()` inside `Dog.speak` compiles to `invokespecial Animal.speak` (or a direct method reference) — *not* `invokevirtual` — so it binds to the immediate parent, no re-dispatch to `Dog`. The `this` passed is still the Dog object.
5. This non-virtual binding is exactly what prevents infinite recursion in the extend-pattern.
The bytecode distinction (`invokespecial` vs `invokevirtual`) is why `super` calls differ from ordinary method calls — a favorite "internals" question.

## 10. Time Complexity
- `super(...)` constructor chain: O(depth) constructor calls, each O(1) + body cost — typically O(depth + init).
- `super.method()`: O(1) — a direct (non-virtual) call; often inlined by the JIT.
- No dynamic dispatch for `super` calls → no vtable lookup.
- Deep hierarchies add O(depth) to construction only; dispatch stays O(1).

## 11. Advantages
- **Ordering guarantee**: parent invariants always established first — "valid parent, then child."
- **Extend-not-replace**: `super.method()` lets subclasses reuse and layer behavior.
- **Flexible construction**: `super(args)` passes subclass data to the parent's setup.
- **Explicit**: reading `super.x()` makes the inheritance intent visible.
- **Compiler-enforced**: forgetting the parent constructor is a compile error, not a runtime surprise.

## 12. Disadvantages
- **Boilerplate**: every subclass constructor needs a `super(...)` line (or relies on the implicit no-arg).
- **No-arg dependency**: adding an argument to a parent constructor breaks subclasses that relied on implicit `super()`.
- **Order rigidity**: `super()` must be first — you can't do subclass work before delegating (Java's choice for safety).
- **Misuse**: `super.field` for shadowed fields encourages shadowing; the extend-pattern can silently double-execute parent logic if not careful.
- **Hidden coupling**: deep `super` chains make the object's behavior a stack of layers that's hard to trace.

## 13. Interview Questions
1. **Q: What does `super()` do?** A: Invokes the direct superclass's constructor; it must be the first statement of a subclass constructor; if omitted, an implicit `super()` (no-arg) is inserted. It guarantees the parent is initialized before the child body runs.
2. **Q: What is the order of constructor execution in a subclass?** A: From the top down: `Object` constructor → ... → parent constructor → child constructor (each class's field initializers run before its constructor body). Parent before child, always.
3. **Q: What happens if the parent has no no-arg constructor and you don't call `super(...)`?** A: Compile error — the implicit `super()` can't resolve; you must explicitly call `super(args)` with a matching parent constructor.
4. **Q: TRICKY — What's the difference between `super()` and `super.method()`?** A: `super()` is constructor delegation (must be first statement, only in constructors); `super.method()` invokes the parent's implementation of an overridden method (from any instance method). Same keyword, two completely different mechanisms.
5. **Q: Can you call `super.method()` inside a static method?** A: No — `super` is valid only in instance contexts (like `this`); a static method has no instance, so no parent view.
6. **Q: Is `super` a reference like `this`?** A: No — `super` can't be stored, passed, or returned; it's a compile-time keyword that resolves to the parent's member. `this` is a real reference value; `super` is not.
7. **Q: Why does `super.method()` not re-dispatch virtually?** A: Because the intent is "the parent's implementation, exactly" — virtual dispatch would re-enter the subclass and infinitely recurse in the extend pattern. `super` calls are non-virtual (bound to the immediate parent).
8. **Q: SCENARIO — A template method in the parent calls a method the subclass overrides. Which version runs?** A: The subclass's — that's the point (hook method). Virtual dispatch applies to the hook; `super` is only for when *you* explicitly want the parent's version.
9. **Q: PRODUCTION — Android requires `super.onCreate(savedInstanceState)` first. Why?** A: The framework's `Activity.onCreate` sets up the activity's internal state; running your code before it would touch uninitialized framework state. The "call super first" convention exists precisely to preserve ordering guarantees.
10. **Q: TRICKY — Can you call `super.super.x()`?** A: No — `super` refers to the *immediate* parent only; you cannot skip levels. To reach a grandparent, the parent must expose the call (or you rearchitect — deep direct-to-grandparent access is a smell).
11. **Q: What happens to field initializers relative to constructors?** A: Each class's field initializers and instance-initializer blocks run (in source order) *before* that class's constructor body — and since parents construct first, the parent's initializers run before the child's constructor body.
12. **Q: SCENARIO — Parent ctor calls an overridable method. Which runs?** A: The subclass's override — but the subclass's fields aren't initialized yet (a classic bug: the override reads uninitialized state). This is why calling overridable methods from constructors is an anti-pattern.
13. **Q: What is the implicit constructor rule in Java?** A: If a class declares no constructor, the compiler adds a default no-arg constructor that calls `super()`; if a subclass constructor omits `super(...)`, `super()` is inserted implicitly. Both insertions require a resolvable no-arg parent constructor.
14. **Q: PRACTICAL — Why should fields be set in constructors rather than in the subclass body before `super`?** A: You *can't* — `super()` is first by law; subclass field assignments are illegal before it. This ordering forces the parent to own its initialization, which is exactly the invariant guarantee.
15. **Q: TRICKY — `super` in a record?** A: Records implicitly extend `java.lang.Record` (not user-overridable); their canonical constructors can't call a user `super` beyond the implicit `super()` — records were designed to avoid the constructor-hierarchy machinery.

## 14. Follow-Up Questions
1. **Q: What is the difference between `this(...)` and `super(...)`?** A: `this(...)` calls a *sibling* constructor in the same class (delegation for defaults); `super(...)` calls the *parent's* constructor. Both must be the first statement — and a constructor can use one or the other, never both.
2. **Q: Why is calling an overridable method from a constructor dangerous?** A: The subclass's override may read fields that haven't been initialized yet (the parent ctor runs *before* the subclass body); you get nulls/zeros. Fix: don't call overridable methods from constructors, or make the fields final/set in the override carefully.
3. **Q: Does `super` exist in C++/Python?** A: C++: `Base::method()` and `Base::Base(args)` (base initializer list) are the equivalents — same non-virtual-optional semantics (you can even call virtual via base explicitly). Python: `super().__init__(args)` and `super().method()` — but in Python, `super()` follows the *MRO* (which may be a sibling, not the immediate parent), making it cooperative across mixins.
4. **Q: What is the "base class initialization list" in C++?** A: `Derived(...) : Base(args), member_(init) { body }` — the compiler initializes bases first (in declaration order), then members, then the body — the C++ ordering guarantee analogous to Java's.

## 15. Coding Example
```java
public class Employee {
    private final String id;                 // final: set once, in parent ctor
    private double salary;
    public Employee(String id, double salary) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("id required");
        if (salary < 0) throw new IllegalArgumentException("salary < 0");
        this.id = id; this.salary = salary;
    }
    public void adjust(double delta) { salary += delta; }
    public double getSalary() { return salary; }
}
public class Manager extends Employee {
    private final int teamSize;
    public Manager(String id, double salary, int teamSize) {
        super(id, salary);                    // parent validated first
        this.teamSize = teamSize;             // then child field
    }
    @Override public void adjust(double delta) {
        super.adjust(delta);                  // run base rule (no negatives at construction)
        System.out.println("Manager " + delta + " applied, team=" + teamSize);
    }
}
```
```cpp
// C++ base initializer list — the super(...) equivalent
class Employee {
    std::string id_; double salary_;
public:
    Employee(std::string id, double s) : id_(std::move(id)), salary_(s) {}
    virtual ~Employee() = default;
};
class Manager final : public Employee {
    int teamSize_;
public:
    Manager(std::string id, double s, int t) : Employee(std::move(id), s), teamSize_(t) {}
};
```
```python
class Employee:
    def __init__(self, emp_id: str, salary: float):
        self._id, self._salary = emp_id, salary
class Manager(Employee):
    def __init__(self, emp_id: str, salary: float, team_size: int):
        super().__init__(emp_id, salary)      # MRO-based; cooperative
        self.team_size = team_size
```

## 16. Industry Usage
- **Android**: `onCreate`, `onPause`, `onDestroy` — "always call `super` first" is the platform's documented contract; forgetting it causes framework crashes.
- **JDK**: `AbstractList` subclasses; `HashMap extends AbstractMap` — parent constructors establish structure, subclasses add specifics.
- **Spring**: `@PostConstruct`/`init` ordering conventions build on construction order; `AbstractBeanFactory` template methods call `super`-style hooks.
- **Java Collections**: `PriorityQueue`, `TreeMap` all chain parent construction.
- **Every Java service**: layered entities (`BaseEntity` with `id`/`createdAt`, subclasses add fields) — the super-chain is how base invariants (IDs, timestamps) are guaranteed at scale.

## 17. References
- Java Language Specification, §8.8.7.1 (Explicit Constructor Invocations), §15.11.2 (super), §8.1.3: https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- Oracle Java Tutorials, "Using the Keyword super": https://docs.oracle.com/javase/tutorial/java/IandI/super.html
- Android developer docs on `Activity` lifecycle (super-first convention): https://developer.android.com/guide/components/activities/activity-lifecycle
- Bjarne Stroustrup, *The C++ Programming Language* — base class initialization.
- Python docs on `super()`: https://docs.python.org/3/library/functions.html#super

## 18. Cheat Sheet
- `super(...)` = parent constructor call; first statement; implicit `super()` if omitted.
- Order: parent ctor (with its initializers) → child initializers → child ctor body.
- `super.method()` = parent's implementation, non-virtual (no re-dispatch).
- `super` is NOT a reference — keyword only; instance contexts only.
- No `super.super` — immediate parent only.
- No-arg parent required unless you explicitly call `super(args)`.
- `this(...)` (sibling) and `super(...)` are mutually exclusive first statements.
- Anti-pattern: calling overridable methods from constructors.

## 19. Quiz
1. `super(...)` must be: a) last statement b) first statement c) anywhere d) in static methods → **b**
2. If omitted, a subclass constructor inserts: a) `this()` b) `super()` c) nothing d) `Object()` → **b**
3. `super.method()` is: a) virtual b) non-virtual direct call c) static d) abstract → **b**
4. Execution order: a) child then parent b) parent then child c) random d) parallel → **b**
5. Can `super.super.x()` compile? a) yes b) no c) only with casts d) in C++ → **b**
6. True or False: `super` can be stored in a variable. → **False**

## 20. Flashcards
- **Q: What does `super()` do?** → **A:** Calls the parent constructor (first statement; implicit `super()` if omitted).
- **Q: Constructor order?** → **A:** Parent first (top-down chain), child last; initializers before each ctor body.
- **Q: `super.method()` semantics?** → **A:** Immediate parent's implementation, non-virtual — no subclass re-dispatch.
- **Q: Is `super` a reference?** → **A:** No — a compile-time keyword; valid only in instance contexts.
- **Q: Can you call `super.super`?** → **A:** No — immediate parent only.
- **Q: Why super-first is mandatory?** → **A:** Parent invariants must exist before child code runs.
- **Q: Anti-pattern with constructors?** → **A:** Calling overridable methods from a constructor.

## 21. Revision
`super` has two faces: `super(...)` — parent constructor delegation, required first statement, implicit `super()` when omitted, guaranteeing the parent is fully built before the child body; and `super.method()` — the immediate parent's overridden implementation, bound non-virtually (invokespecial), enabling extend-not-replace. Order: top-down chain, initializers before ctor bodies. `super` is a keyword, not a reference; no `super.super`. First-30-seconds answers: "parent ctor first; super.method is non-virtual; super is compile-time."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does `super()` do?" | Interview Q1 / Section 8 |
| "Order of constructor execution?" | Interview Q2 / Internal Working |
| "Parent without no-arg ctor?" | Interview Q3 |
| "`super()` vs `super.method()`?" | Interview Q4 |
| "Is super a reference?" | Interview Q6 |
| "Why non-virtual super calls?" | Interview Q7 |
| "Calling overridable methods from ctors?" | Interview Q12 / Follow-Up Q2 |
| "Why Android super.onCreate first?" | Interview Q9 / Section 16 |
