# Inheritance in Depth

> **TL;DR**: Inheritance is the IS-A mechanism — a subclass (`class SavingsAccount extends Account`) acquires its parent's state and behavior, can specialize it, and can be used wherever the parent is; it exists for genuine type relationships, not just code reuse.

## 1. Why Does This Exist?
Inheritance exists to express the most common relationship in domain modeling: **"a thing is a kind of another thing."** A `CheckingAccount` *is an* `Account`; a `Square` *is a* `Shape`; an `Employee` *is a* `Person`. Without inheritance you'd have to either duplicate the parent's fields/methods everywhere, or model everything as one giant class with flags — both unmaintainable. Inheritance gives two things at once: (1) **code/state reuse** — the subclass automatically has the parent's fields and methods; (2) **typing/polymorphism** — a `SavingsAccount` can be used anywhere an `Account` is expected, and its specialized behavior runs at runtime. The distinction between these two reasons (reuse vs typing) is *the* critical insight: modern design says inheritance's real value is typing; reuse is a bonus, and reuse-pure hierarchies are usually wrong (that's the composition-vs-inheritance debate).

## 2. How Does It Work?
```java
public class Account {
    protected double balance;                  // state the subclass inherits
    public void deposit(double amt) { balance += amt; }     // behavior inherited
}
public class SavingsAccount extends Account {  // IS-A: SavingsAccount is an Account
    private double interestRate;
    public void addInterest() { balance += balance * interestRate; }   // specialized
}
```
Mechanically: `SavingsAccount`'s object layout *includes* `Account`'s fields (`balance` is present in every SavingsAccount object, at the base's offset). `deposit()` is inherited — callable on a `SavingsAccount` without redefinition. `addInterest()` is new. The subclass may also *override* inherited methods and *call super*.

## 3. When Is It Used?
- **Genuine is-a hierarchies**: `Vehicle → Car/Truck`, `Shape → Circle/Square`, `Account → Checking/Savings`.
- **Framework extension points**: `extends HttpServlet`, `extends Activity`, `extends AbstractList` — the framework provides the base, you fill in hooks.
- **Template method patterns**: `AbstractReport.print()` calls overridable `printBody()`.
- **Code reuse with typing**: a base class holding shared fields (`Person` name/email) with subclasses adding specifics.
- **NOT for**: "I need `Employee` methods in my `Manager` class" (has-a: give `Manager` an `Employee` field instead) — the most common misuse.

## 4. Why Wasn't Another Approach Chosen?
- *Why not copy-paste the parent's code?* Duplication guarantees divergence: fix the bug in one copy and the others stay broken. Inheritance chosen: one source of truth.
- *Why not just composition (has-a)?* Composition is often *better* (see Part 03 ch2 section 1), but for a *true is-a* where you want to pass the subclass as the parent (polymorphism: `List<Account> accounts.add(new SavingsAccount())`), inheritance is the direct, type-safe way — composition can't give you "this IS-A Account" typing.
- *Why not one class with a `type` field?* A `type`-flagged class grows a `switch` everywhere (violates Open-Closed) and mixes all behaviors; inheritance isolates behavior per subtype and lets you add subtypes without touching existing code.
- *Why not interfaces for everything?* Interfaces give typing but no state/constructor reuse; when subclasses genuinely share base state and template logic, a class hierarchy is the tool (that's why `AbstractList` exists alongside `List`).
The design answer: inheritance is chosen when the relationship is *genuinely is-a* and you need *both* typing and shared implementation; otherwise composition.

## 5. Intuition
Think of **genetics**: a `Dog` inherits the `Mammal` "template" — it has the same organs and behaviors (breathes, moves) — but specializes (barks, wags tail). A dog *is a* mammal, so a vet trained to treat mammals can treat a dog (typing). The dog doesn't re-build its organs from scratch (reuse) — it gets them from the parent definition and adds its own. Inheritance is that genetic inheritance: shared foundation, specialized expression, and "treatable as the parent type" anywhere.

## 6. Real-World Analogy
A **blueprint family**. The `Building` blueprint defines foundation, walls, roof. The `Hospital` blueprint *inherits* the Building blueprint — same foundation and walls (state) and construction rules (behavior) — then adds operating theaters and a pharmacy. A city inspector who approves "buildings" can approve a hospital (typing: a Hospital *is a* Building). If the foundation spec changes, every building type updates once (single source of truth). If hospitals were built by copying the Building blueprint (no inheritance), a foundation change would miss every hospital copy.

## 7. Formal Definition
**Inheritance** is an object-oriented mechanism whereby a class (subclass/derived class) is defined in terms of an existing class (superclass/base class), acquiring its instance fields and methods and permitting extension (new members) and specialization (overriding inherited methods). A subclass is a **subtype** of its superclass: wherever the superclass is expected, a subclass instance may be substituted (the Liskov substitution principle governs the correctness of this). In Java, a class may extend at most one class (`extends`), while implementing any number of interfaces (`implements`); inheritance of *type* (interfaces) is multiple, inheritance of *implementation* (classes) is single.

## 8. Example
```java
public class Animal {
    protected String name;
    public Animal(String name) { this.name = name; }
    public void speak() { System.out.println(name + " makes a sound"); }
    public String getName() { return name; }
}
public class Dog extends Animal {
    public Dog(String name) { super(name); }          // parent constructor first
    @Override public void speak() { System.out.println(name + " barks"); }  // specialize
    public void fetch() { System.out.println(name + " fetches"); }          // new
}
public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog("Rex");
        rex.speak();                                  // "Rex barks" (override)
        rex.fetch();                                  // "Rex fetches" (new method)
        Animal pet = rex;                             // UPCAST: a Dog IS an Animal
        pet.speak();                                  // "Rex barks" (dynamic dispatch)
        System.out.println(pet.getName());            // "Rex" (inherited method)
    }
}
```
Inherited: `name` field, `getName()` method. Specialized: `speak()` overridden. New: `fetch()`. Typing: `Animal pet = rex` accepts a `Dog` — polymorphism starts here.

## 9. Internal Working
1. **Layout**: `SavingsAccount` object = header + `Account` fields (balance) + `SavingsAccount` fields (interestRate), in that order. The base's fields are *present* in every subclass object.
2. **Inherited methods**: `deposit()` exists once (in `Account`); a call `savings.deposit(x)` compiles to `Account.deposit` with `this` = the SavingsAccount — the offset for `balance` matches, so the base code works on the subclass object.
3. **Override**: `speak()` in `Dog` replaces the vtable slot inherited from `Animal`; a call through an `Animal` reference still lands on `Dog.speak` (runtime dispatch).
4. **Constructor chain**: `new Dog(name)` → implicit `super(name)` → `Animal` constructor runs first, establishing base invariants, then the `Dog` body.
5. **Verifier**: bytecode for `extends` is checked; the JVM builds the subclass's class metadata including the base's fields/methods.
No copying happens — inheritance is *structural sharing*: one copy of base code + fields laid out per subclass.

## 10. Time Complexity
- Inherited method call: O(1) — same as a normal virtual call (vtable).
- Field access on inherited field: O(1) — fixed offset from `this`.
- Object allocation of subclass: O(1) amortized (heap bump) + total field size.
- Hierarchies add no extra dispatch cost — vtable lookup is O(1) regardless of depth.
- `instanceof` / cast checks: O(1) (class metadata check).
- Inheritance is asymptotically free; its cost is design complexity, not runtime.

## 11. Advantages
- **Is-a modeling** matches the domain and communicates intent.
- **Code/state reuse** — single source of truth for shared behavior.
- **Polymorphism** — subclass used anywhere the base is expected.
- **Extensibility** — add subtypes without touching existing code (Open-Closed).
- **Framework hooks** — override lifecycle/template methods.

## 12. Disadvantages
- **Coupling**: subclass depends on the parent's implementation (fragile base class).
- **Misuse risk**: forcing is-a where has-a fits creates LSP violations.
- **Deep hierarchies**: hard to reason about, hard to test, brittle.
- **Single-inheritance limits** (Java) — you spend your one `extends`.
- **Exposes too much**: subclasses see `protected` internals, breaking encapsulation.
- **Behavior leaks**: overriding without calling `super.method()` silently drops parent logic.

## 13. Interview Questions
1. **Q: What is inheritance and why does it exist?** A: A mechanism where a subclass acquires the state and behavior of a superclass and can extend/specialize it; it exists for is-a modeling, reuse (single source of truth), and typing (polymorphism).
2. **Q: Is inheritance primarily for code reuse?** A: Reuse is a *benefit*, not the primary justification — the real value is *is-a typing* (a subclass IS a supertype, usable polymorphically). Reuse-only hierarchies (no true is-a) are exactly the ones that should be composition.
3. **Q: What does a subclass inherit?** A: All *accessible* members: public and protected fields/methods; private members exist in the object but aren't accessible by name; static members are inherited/hidden; constructors are NOT inherited (but the parent's runs).
4. **Q: TRICKY — Do private members get inherited?** A: The memory/fields exist in the subclass object (the parent laid them out), but the subclass code cannot access them by name — only via public/protected parent methods. So: inherited in *structure*, not in *access*.
5. **Q: Why can't constructors be inherited?** A: A constructor's name must match its class; a subclass constructor can't "be" the parent's. Instead, subclass constructors *call* the parent's via `super(...)` to initialize the inherited part.
6. **Q: What is the difference between inheritance of type and inheritance of implementation?** A: Type inheritance = the subtype relationship (a Dog is an Animal — enables polymorphism); implementation inheritance = reusing the parent's code/state. Java separates them: interfaces give type inheritance, classes give implementation inheritance; modern design prefers interface (type) + composition (implementation).
7. **Q: SCENARIO — You have `Bird` and need `Penguin`. Is `Penguin extends Bird` correct?** A: Only if the base models only shared bird facts. If `Bird` has `fly()` (implementation), Penguin inherits a lie (LSP violation — penguins can't fly). Fix: `Bird` without `fly()`, or a `FlyingBird` subtype — the classic "wrong inheritance" example.
8. **Q: PRACTICAL — How do you avoid the fragile base class problem?** A: Keep base classes small and stable, prefer composition, use interfaces, document contracts, avoid overriding deep chains, and treat the base as an API (not a grab-bag).
9. **Q: TRICKY — `class A extends B`, both define `m()`. A call `a.m()` resolves how?** A: At runtime, to `A.m()` (dynamic dispatch via vtable) — the *most derived* implementation wins, regardless of the reference type. If `A.m()` calls `super.m()`, it reaches `B.m()`.
10. **Q: What is the "is-a vs has-a" test?** A: "Can you honestly say X IS-A Y and substitute it everywhere Y is used (LSP)?" If yes → inheritance; if it's "X HAS a Y" (contains it) → composition. A `Car` HAS-a `Engine` (composition), but a `Sedan` IS-a `Car` (inheritance).
11. **Q: PRODUCTION — Why do frameworks make you extend a base class (e.g., `HttpServlet`)?** A: To give you lifecycle/template hooks with the framework's machinery guaranteed: your servlet inherits the protocol handling and you only override `doGet`/`doPost` — framework control + extension point in one.
12. **Q: Can a class be both a subclass and an implementation?** A: Yes — `class SavingsAccount extends Account implements InterestBearing` — one `extends`, many `implements`: single implementation inheritance + multiple type inheritance.
13. **Q: TRICKY — What does "inheritance breaks encapsulation" mean?** A: Subclasses can access `protected` internals and can override methods, coupling them to the parent's internals; a base implementation change can silently break subclasses (fragile base). Encapsulation and inheritance are in tension.
14. **Q: What is the null-object / empty-subclass misuse?** A: Subclassing just to get access to a method (instead of using the method directly) or subclassing for a single tweak — signs of a wrong relationship; prefer composition or just using the parent.
15. **Q: How deep should a hierarchy go?** A: Shallow is better — 2-3 levels typical; each level adds coupling and dispatch ambiguity. If a hierarchy is deep, question the design (usually interface + composition replaces it).

## 14. Follow-Up Questions
1. **Q: What is the difference between inheritance and subtyping?** A: Subtyping is the *type* relationship (a Dog is-a Animal — static type system); inheritance is the *implementation* mechanism (reusing the parent's code). In Java they usually coincide (extends gives both), but interfaces give subtype without implementation inheritance.
2. **Q: What is the "fragile base class problem"?** A: A change to a widely-used base class can break subclasses that relied on implementation details (even unchanged subclass code) — the reason to keep bases small, contract-bound, and prefer composition.
3. **Q: What happens if a subclass constructor doesn't call `super`?** A: Java inserts an implicit `super()` (no-arg parent) — if the parent has no no-arg constructor, it's a compile error; you must call `super(args)` explicitly.
4. **Q: Can inheritance enable polymorphism without interfaces?** A: Yes — class inheritance gives subtype polymorphism directly (`Animal pet = new Dog()`); interfaces give *additional* multiple-type polymorphism. Both are "one interface, many implementations."

## 15. Coding Example
A realistic hierarchy with base invariants:
```java
public abstract class BankProduct {
    private final String productId;          // base invariant: non-null id
    protected double balance;
    public BankProduct(String id, double initial) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("id required");
        if (initial < 0) throw new IllegalArgumentException("negative initial");
        this.productId = id;
        this.balance = initial;
    }
    public void deposit(double amt) { if (amt > 0) balance += amt; }
    public abstract String describe();        // subclass must implement
}
public class CurrentAccount extends BankProduct {
    public CurrentAccount(String id, double initial) { super(id, initial); }
    public String describe() { return "Current[" + balance + "]"; }
}
public class SavingsAccount extends BankProduct {
    public SavingsAccount(String id, double initial) { super(id, initial); }
    public void addInterest(double rate) { balance += balance * rate; }
    public String describe() { return "Savings[" + balance + "]"; }
}
// usage:
// List<BankProduct> products = List.of(new CurrentAccount("C1", 100), new SavingsAccount("S1", 100));
```
```python
class BankProduct:
    def __init__(self, product_id: str, initial: float):
        if initial < 0: raise ValueError("negative initial")
        self._product_id, self._balance = product_id, initial
    def deposit(self, amt: float) -> None:
        if amt > 0: self._balance += amt
    def describe(self) -> str: raise NotImplementedError
class SavingsAccount(BankProduct):
    def __init__(self, pid: str, initial: float, rate: float):
        super().__init__(pid, initial); self._rate = rate
    def add_interest(self) -> None: self._balance += self._balance * self._rate
    def describe(self) -> str: return f"Savings[{self._balance}]"
```
```cpp
class BankProduct {
protected: double balance_;
public: BankProduct(double initial) : balance_(initial) {}
    virtual ~BankProduct() = default;
    virtual std::string describe() const = 0;   // pure virtual → abstract
    void deposit(double amt) { if (amt > 0) balance_ += amt; }
};
class SavingsAccount final : public BankProduct {
public: using BankProduct::BankProduct;        // inherit constructors
    std::string describe() const override { return "Savings[" + std::to_string(balance_) + "]"; }
};
```

## 16. Industry Usage
- **JDK**: `AbstractList`/`AbstractMap` (implementation inheritance for implementers), `HttpServlet`, `Thread` (extends), exception hierarchy (`RuntimeException extends Exception`).
- **Spring**: `@Configuration`, `AbstractHttpMessageConverter`, service base classes — extension-point inheritance is a framework staple.
- **Android**: `Activity`, `Fragment`, `Adapter` — developers extend framework bases and override lifecycle hooks daily.
- **Java Collections**: `Vector`/`Stack` (legacy extends), `HashMap extends AbstractMap`.
- **C++ systems**: polymorphic bases with virtual destructors (the rule); CRTP for static polymorphism.
- **Real-world caution**: modern guidelines (Effective Java, Clean Code, Android docs) push *interfaces + composition*; inheritance survives where the base is a stable extension contract (frameworks) or a genuine is-a domain model.

## 17. References
- Joshua Bloch, *Effective Java* — Items 17 (design/document for inheritance or forbid), 19 (interfaces), 20 (prefer interfaces to abstract classes).
- Erich Gamma et al., *Design Patterns* — "Favor composition over inheritance."
- Robert C. Martin, *Agile Software Development* — LSP chapter (inheritance correctness).
- Java Language Specification, Ch. 8 §8.1.3 (superclasses), §8.4.8 (inheritance, overriding): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- GeeksForGeeks, "Inheritance in Java": https://www.geeksforgeeks.org/inheritance-in-java/

## 18. Cheat Sheet
- Inheritance = is-a; subclass extends superclass; single `extends`, multiple `implements`.
- Inherited: public/protected members (accessible); private fields exist but hidden; static members hidden; constructors not inherited.
- Object layout = base fields then subclass fields.
- Constructor chain: parent first (implicit `super()`).
- Reuse is a benefit, typing is the point.
- is-a test: "can it honestly substitute everywhere?" else compose.
- Fragile base class: change a base → break subclasses.
- Keep hierarchies shallow (2-3 levels).

## 19. Quiz
1. A subclass inherits: a) constructors b) private field memory but not access c) nothing d) packages → **b**
2. `class Dog extends Animal` means: a) has-a b) is-a c) uses-a d) creates-a → **b**
3. Parent constructor runs: a) after child b) before child c) never d) randomly → **b**
4. If a subclass defines no constructor: a) compile error b) implicit `super()` inserted c) object uninitialized d) parent skipped → **b**
5. Constructors are: a) inherited b) called via super, not inherited c) static d) abstract → **b**
6. True or False: Private fields are absent from subclass objects. → **False** (they exist, just inaccessible)

## 20. Flashcards
- **Q: What is inheritance?** → **A:** Is-a mechanism: subclass acquires parent state/behavior, can specialize, and is substitutable for the parent.
- **Q: Inherited vs not?** → **A:** Public/protected accessible; private exists but hidden; static hidden; constructors not inherited.
- **Q: Constructor order?** → **A:** Parent first (implicit `super()`), then child.
- **Q: Primary justification for inheritance?** → **A:** Is-a typing (polymorphism); reuse is a bonus.
- **Q: Is-a vs has-a test?** → **A:** Can it substitute for the parent everywhere (LSP)? Yes→inherit; No→compose.
- **Q: Fragile base class?** → **A:** Base change breaks subclasses that depended on internals.
- **Q: How deep should hierarchies be?** → **A:** Shallow — 2-3 levels; deeper → rethink with interfaces/composition.

## 21. Revision
Inheritance is the is-a mechanism: a subclass acquires accessible parent members (public/protected), private members exist but stay hidden, static members hide (not override), and constructors are never inherited — instead `super(...)` runs first, so the parent is always fully built before the child body. The object layout is base fields + subclass fields. Its real justification is *is-a typing* (polymorphism); pure-reuse hierarchies are the composition-over-inheritance targets. First-30-seconds answers: "single extends + many implements; parent ctor runs first; private is structurally present but inaccessible."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is inheritance?" | Formal Definition / Section 13 |
| "Inheritance for reuse or typing?" | Interview Q2 |
| "Are private members inherited?" | Interview Q4 |
| "Why aren't constructors inherited?" | Interview Q5 |
| "Is-a vs has-a test?" | Interview Q10 |
| "Fragile base class problem?" | Follow-Up Q2 / Section 14 |
| "How deep should a hierarchy be?" | Interview Q15 |
| "Penguin/Bird wrong-inheritance example?" | Interview Q7 |
