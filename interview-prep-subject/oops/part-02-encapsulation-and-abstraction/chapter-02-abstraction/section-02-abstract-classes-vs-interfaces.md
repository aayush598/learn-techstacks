# Abstract Classes vs Interfaces

> **TL;DR**: An abstract class is a partial implementation you *inherit* (state + template methods + constructors, single inheritance); an interface is a pure *contract* you implement (capability, multiple inheritance of type, no state) — choose abstract class when you need shared state/template logic, interface when you need a swappable capability.

## 1. Why Does This Exist?
Java (and C#/C++) gives you *two* abstraction tools because abstraction has two different needs: (1) **contract-only** abstraction — "anything that is a `Payable` must be able to `pay()`" — which needs nothing but signatures; and (2) **contract + shared code** — "all `Vehicle`s share `fuelLevel` and `refuel()`" — which needs inherited state and default behavior. A single tool can't serve both well: pure interfaces can't carry state or constructors; abstract classes can't be multiply inherited. So Java offers both, and the interview question "abstract class or interface?" exists to test whether you can match the *design need* (state? code reuse? multiple capabilities?) to the *language mechanism*.

## 2. How Does It Work?
**Abstract class** (`abstract class X`):
- Can have `abstract` methods (no body) and concrete methods (body).
- Can have fields (state), constructors, static members.
- Cannot be instantiated (`new X()` illegal).
- A subclass `extends` it — single inheritance only.
- Abstract methods MUST be implemented by the first concrete subclass (or that subclass stays abstract).

**Interface** (`interface Y`):
- Methods are implicitly `public abstract` (Java 8+ allows `default`/`static`; Java 9+ private methods).
- Fields are implicitly `public static final` (constants only, no instance state).
- No constructors (can't be instantiated).
- A class `implements` it — can implement *many*.
- An interface can `extends` other interfaces (multiple).

The decision: need shared state or a template method? → abstract class. Need a capability contract, multiple roles, or a stable testing seam? → interface.

## 3. When Is It Used?
**Abstract class** when:
- Shared state across subclasses (base fields).
- A template-method skeleton (steps with defaults, subclasses override hooks).
- Close is-a with genuine code reuse (e.g., `AbstractList`, `HttpServlet`).
- Constructors that set up base invariants.

**Interface** when:
- A capability/role contract (`Comparable`, `Runnable`, `PaymentProcessor`).
- Multiple roles on one class (a class can be both `Runnable` and `Serializable`).
- Cross-hierarchy polymorphism (unrelated classes share a contract).
- Test seams (mocking).
- Library APIs (`java.util.List`).

## 4. Why Wasn't Another Approach Chosen?
- *Why not only interfaces (no abstract classes)?* Because contracts with no shared code force duplication: ten `Shape`s each re-implement `area()`-adjacent logic. Also interfaces can't hold state or constructors — template methods would need workarounds (composition helpers). Abstract classes chosen to carry state + reusable code.
- *Why not only abstract classes (no interfaces)?* Because Java has single inheritance — a class can extend only one abstract class, so you couldn't have a class that's both `Comparable` and `Serializable` and `Runnable` by inheritance. Interfaces chosen for multiple *type* inheritance (capabilities). (C++ chose multiple class inheritance instead — and pays the diamond-problem tax.)
- *Why not make all classes abstract?* Concrete classes are needed for real objects; abstract classes are only for intermediate design.
- *Why not default-methods-only interfaces?* Default methods give code reuse but can't carry instance state — shared mutable state still needs an abstract class (or composition).
The design answer: two tools, because "pure contract" and "contract + shared implementation" are different design needs; the language models both.

## 5. Intuition
An **abstract class** is a **half-finished blueprint**: it has the foundation and walls (state, base code), and says "you finish the roof" (abstract methods). An **interface** is a **job requirement sheet**: "must be able to pay()", "must be comparable" — nothing built, just requirements. You can satisfy many requirement sheets (implement many interfaces) but you can only *inherit* one blueprint (extend one class). If you're building similar things that share a foundation, use the blueprint; if you're just certifying capabilities, use the requirement sheets.

## 6. Real-World Analogy
A **restaurant chain**. The franchise's *recipe book for the base kitchen* (abstract class) gives every outlet the same equipment layout, pantry, and standard prep steps — but each outlet's menu special (abstract method) is filled in locally. Now, a *health inspector's checklist* (interface): any outlet — or even a food truck that shares nothing with the chain — can "implement" the checklist (food safety, permits) and be certified. You inherit one kitchen layout; you can satisfy many checklists. That's abstract class (shared foundation, extend one) vs interface (capability contract, implement many).

## 7. Formal Definition
An **abstract class** is a class that cannot be instantiated, may declare abstract methods (declared without body) and concrete methods, may hold fields/state and constructors, and is inherited via single inheritance; subclasses must implement its abstract methods unless they remain abstract. An **interface** is a reference type declaring a contract — method signatures (implicitly public abstract), constants (implicitly public static final), and, since Java 8, default/static methods (and private methods since Java 9); a class may implement multiple interfaces. Key contrasts: state (abstract class yes / interface no), constructors (abstract class yes / interface no), inheritance multiplicity (single / multiple), and the extends-vs-implements relationship.

## 8. Example
```java
// ABSTRACT CLASS: shared state + template method
public abstract class AbstractReport {
    protected final String title;                     // shared state
    protected AbstractReport(String title) { this.title = title; }  // constructor
    public final void print() {                       // template method (final: fixed)
        System.out.println("== " + title + " ==");
        printBody();                                   // hook — subclass implements
        printFooter();
    }
    private void printFooter() { System.out.println("----"); }
    protected abstract void printBody();               // abstract hook
}
public class SalesReport extends AbstractReport {
    public SalesReport() { super("Sales"); }
    protected void printBody() { System.out.println("Q1: $120k"); }   // fill in the hook
}

// INTERFACE: pure capability contract, implementable by ANY class
public interface Discountable {
    double applyDiscount(double price);        // implicit public abstract
}
public class Product implements Discountable, Comparable<Product> {   // many interfaces
    public double applyDiscount(double price) { return price * 0.9; }
    public int compareTo(Product o) { return 0; }
}
```
The abstract class shares state (`title`) + template (`print()` skeleton with a `printBody()` hook); the interface is a contract (`applyDiscount`) any class can implement — including classes with totally different hierarchies.

## 9. Internal Working
1. **Abstract class**: compiles like a normal class with abstract methods flagged `ACC_ABSTRACT`; cannot be instantiated — the verifier rejects `new AbstractReport()`. The subclass's object layout *includes* the parent's fields (`title`); the constructor chain runs `super(title)` first. `print()` is inherited as code; `printBody()` is dispatched via the vtable to the subclass's override (runtime polymorphism).
2. **Interface**: compiles to a class file with only signatures (+ default method bodies); `implements` adds the interface to the class's type list. Method calls go through the **itable** (interface method table) — the JVM finds the concrete implementation's slot. Multiple interfaces are stored in the class's interfaces array; `instanceof Discountable` checks membership.
3. Dispatch cost: abstract-class override = one vtable lookup; interface call = one itable lookup — both O(1).

## 10. Time Complexity
- Abstract-class virtual call: O(1) (vtable).
- Interface dispatch: O(1) (itable; JIT caches/colonades).
- Abstract-class field access: O(1) (offset from `this`).
- Both: no asymptotic difference vs concrete calls — the choice is structural, not computational.

## 11. Advantages
**Abstract class:**
- Shared state and constructors (invariants centralized).
- Template-method pattern built-in.
- Intimate is-a code reuse (subclass inherits behavior).

**Interface:**
- Multiple capability contracts on one class.
- Cross-hierarchy polymorphism (unrelated types share a contract).
- Clean test seam (mocking).
- Stable API that can evolve via `default` methods.

## 12. Disadvantages
**Abstract class:**
- Single inheritance — you spend your one `extends` slot.
- Couples subclass to parent implementation (fragile base class risk).
- Concrete state in the base can be misused (partially initialized).

**Interface:**
- No instance state (constants only) — shared data must live elsewhere (composition).
- Adding methods breaks implementers (mitigated by `default`).
- Over-indirection if every tiny role gets an interface.

## 13. Interview Questions
1. **Q: Abstract class vs interface — main difference?** A: An abstract class is a partial implementation with state, constructors, and template logic, inherited singly; an interface is a pure contract (signatures, constants, default methods) that any class can implement — including many at once.
2. **Q: When do you choose an abstract class?** A: When subclasses share state (fields), need constructors that set up base invariants, or reuse a template-method skeleton (like `AbstractList`, `HttpServlet`).
3. **Q: When do you choose an interface?** A: When you need a capability/role contract, multiple roles on one class, cross-hierarchy polymorphism, or a mocking seam — e.g., `Runnable`, `Comparable`, `PaymentProcessor`.
4. **Q: TRICKY — "Always prefer interfaces to abstract classes" — is that right?** A: Effective Java Item 20 says *prefer interfaces to abstract classes for defining types* — but for *shared code/state*, an abstract class is legitimate (that's why `AbstractList` exists). The real rule: prefer interfaces for types/contracts; use abstract classes for code reuse.
5. **Q: Can an interface have fields?** A: Only `public static final` constants — no instance state. This is *the* fundamental reason some designs can't be interfaces.
6. **Q: Can a class implement two interfaces with the same default method?** A: No — the class must override it (or an explicit `InterfaceName.super.method()` resolves it); ambiguity is a compile error. Java's answer to the interface diamond problem.
7. **Q: SCENARIO — Design payment processing: `PayPal`, `Stripe`, `TestPay`.** A: Interface `PaymentProcessor { boolean pay(Invoice); }` + three implementations — no shared state, swappable, mockable. Abstract class would waste the single-inheritance slot.
8. **Q: SCENARIO — Design a logging framework: `FileLogger`, `ConsoleLogger` share buffering logic.** A: Abstract class `AbstractLogger` holds the buffer + `flush()` template; subclasses override `writeLine(String)`. Shared state → abstract class is the natural fit.
9. **Q: What is the template method pattern and how does it relate?** A: An abstract class defines an algorithm's skeleton (concrete methods calling abstract hooks); subclasses fill in the hooks. It's *the* reason abstract classes exist distinct from interfaces.
10. **Q: TRICKY — Can an abstract class implement an interface?** A: Yes, and it need not implement all methods — the abstract class can leave them abstract; concrete subclasses finish them. This composes both tools.
11. **Q: Java 8 `default` methods — do they make interfaces as powerful as abstract classes?** A: Not quite — default methods can't hold instance state or run constructors; they give code reuse without state. For shared *mutable* state you still need an abstract class (or composition).
12. **Q: PRODUCTION — Why does the JDK expose `List` (interface) and `AbstractList` (abstract class)?** A: `List` is the consumer contract (stable, implemented by many); `AbstractList` is the *implementer convenience* — it implements most methods from minimal subclasses. Interfaces for users, abstract classes for authors — the same dual design appears in `Set`, `Map`.
13. **Q: What is the "interface diamond problem" (two default methods same signature)?** A: A class implementing two interfaces with an identical default method must override the method (or select via `I.super.m()`); Java resolves it explicitly — unlike C++ multiple inheritance where it's automatic and error-prone.
14. **Q: TRICKY — Can an interface extend a class?** A: No — interfaces only extend interfaces. A class implements interfaces and extends at most one class. (Java 15+ sealed interfaces can restrict *who* implements them.)
15. **Q: How do abstract classes and interfaces appear in C#/C++/Python?** A: C# — abstract classes + interfaces (like Java); C++ — pure virtual classes are "abstract," multiple inheritance allowed, no interface keyword (interfaces are conventions); Python — `ABC` (Abstract Base Classes) + duck typing; `interface` isn't a keyword (PEP 3119 provides `ABC`).

## 14. Follow-Up Questions
1. **Q: What is a "pure virtual" function (C++)?** A: A virtual function with `= 0` — makes the class abstract; C++ has no `interface` keyword, so a class with only pure virtuals *is* the interface idiom. C++ also allows multiple inheritance directly (diamond problem risk).
2. **Q: When would you change an abstract class into an interface?** A: When shared state becomes unnecessary (or you want multiple roles), when implementers stop sharing code, or when testing needs a seam — extract the contract to an interface and keep the abstract class as an optional convenience.
3. **Q: What is the role of sealed classes/interfaces (Java 17)?** A: `sealed` restricts which classes can extend/implement — exhaustive switches, controlled hierarchies: a middle ground between "unbounded extends" and "final".
4. **Q: Do records/annotations count as interfaces?** A: Annotations are interfaces (implicitly), records are final classes — records can implement interfaces (e.g., a `Comparable` record), which is common for value contracts.

## 15. Coding Example
```java
// Shared-state + template via abstract class
public abstract class DataSource {
    private int ops;                                   // shared state
    public final int opsCount() { return ops; }
    public final void execute(String sql) {            // template method
        beforeExecute();
        run(sql);                                       // abstract hook
        ops++;
        afterExecute();
    }
    protected abstract void run(String sql);           // subclass fills in
    protected void beforeExecute() {}                   // optional hook (no-op default)
    protected void afterExecute()  {}
}
public class PostgresSource extends DataSource {
    protected void run(String sql) { System.out.println("PG: " + sql); }
}
// Capability contract via interface
public interface Auditable { void audit(String action); }
public class Ledger implements Auditable, AutoCloseable {     // multiple contracts
    public void audit(String action) { System.out.println("AUDIT " + action); }
    public void close() {}
}
```
```csharp
// C# mirrors Java: abstract class + interface
public abstract class DataSource {
    public int OpsCount { get; protected set; }
    public void Execute(string sql) { Run(sql); OpsCount++; }
    protected abstract void Run(string sql);
}
public interface IAuditable { void Audit(string action); }
```
```python
from abc import ABC, abstractmethod
class DataSource(ABC):                       # abstract base class
    def __init__(self): self._ops = 0        # state
    def execute(self, sql):
        self._run(sql); self._ops += 1
    @abstractmethod
    def _run(self, sql): ...                 # abstract hook
class PostgresSource(DataSource):
    def _run(self, sql): print("PG:", sql)
```

## 16. Industry Usage
- **JDK collections**: `List`/`Map` interfaces for consumers, `AbstractList`/`AbstractMap` for implementers — the JDK's own dual-tool pattern.
- **Spring**: interfaces for beans (testability, AOP proxies); `HttpServlet` (abstract class) is the servlet template; `@Controller` handlers are interfaces.
- **Android**: `Activity` lifecycle is a template via inheritance; listeners (`OnClickListener`) are interfaces.
- **JDBC**: all interfaces (`Connection`, `ResultSet`) — drivers implement them; swapping DBs is a driver swap (interface-only design).
- **Java Streams**: `Stream` interface with default methods (evolved without breaking implementers).
- **Guice/Dagger**: interfaces + `@Inject` — DI frameworks depend on interface typing for proxies and fakes.

## 17. References
- Joshua Bloch, *Effective Java* — Item 20 (prefer interfaces to abstract classes; the dual-tool design).
- Erich Gamma et al., *Design Patterns* — Template Method (abstract class use case).
- Java Language Specification, Ch. 8 §8.1.1.1 (abstract classes), §9 (Interfaces): https://docs.oracle.com/javase/specs/jls/se17/html/jls-9.html
- Oracle Tutorials, "Abstract Methods and Classes" / "Interfaces": https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html
- GeeksForGeeks, "Difference between Abstract Class and Interface in Java": https://www.geeksforgeeks.org/difference-between-abstract-class-and-interface-in-java/

## 18. Cheat Sheet
- Abstract class = state + constructors + template methods; single `extends`.
- Interface = pure contract (signatures + constants + default/static methods); multiple `implements`.
- Use abstract class: shared state, template method, intimate code reuse.
- Use interface: capability contract, multiple roles, test seam, cross-hierarchy.
- Interfaces can't hold instance state — the fundamental constraint.
- `default` methods let interfaces evolve; ambiguity resolved by explicit override.
- Abstract class can implement an interface (compose both).
- C++: pure-virtual classes = interfaces, multiple inheritance; Python: `ABC`.

## 19. Quiz
1. Which can hold instance state? a) interface b) abstract class c) neither d) both → **b**
2. How many interfaces can a class implement? a) one b) two c) many d) none → **c**
3. How many abstract classes can a class extend (Java)? a) one b) many c) unlimited d) zero → **a**
4. The template method pattern is most natural with: a) interfaces b) abstract classes c) records d) generics → **b**
5. Interface fields are implicitly: a) private b) public static final c) protected d) volatile → **b**
6. True or False: An abstract class can implement an interface. → **True**

## 20. Flashcards
- **Q: Abstract class vs interface — the essence?** → **A:** Abstract = partial impl + state + template (single extends); Interface = pure contract (multiple implements).
- **Q: When abstract class?** → **A:** Shared state, constructors, template methods.
- **Q: When interface?** → **A:** Capability contract, multiple roles, test seams.
- **Q: Can interfaces hold state?** → **A:** No — only `public static final` constants.
- **Q: Why default methods?** → **A:** Evolve interfaces without breaking implementers.
- **Q: Interface diamond ambiguity?** → **A:** Class must override the ambiguous default method (or call `I.super.m()`).

## 21. Revision
Abstract classes carry state, constructors, and template logic under single inheritance; interfaces are pure capability contracts under multiple `implements`. Choose abstract class for shared code/state (template method, `AbstractList`); choose interface for contracts/roles/test seams (`List`, `Runnable`, `PaymentProcessor`). Interfaces can't hold instance state; `default` methods enable evolution; ambiguity between two defaults is resolved by explicit override. First-30-seconds answer: "Abstract class = partial implementation with state, inherited singly; interface = pure contract, implementable many times."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Abstract class vs interface?" | Formal Definition / Section 13 |
| "When do you use which?" | Interview Q2–Q3 |
| "'Always prefer interfaces'?" | Interview Q4 |
| "Can interfaces hold fields?" | Interview Q5 |
| "Default method conflict?" | Interview Q6 / Q13 |
| "Template method pattern?" | Interview Q9 / Section 16 |
| "Why List + AbstractList both?" | Interview Q12 / Section 16 |
| "C++/Python equivalents?" | Interview Q15 / Section 15 |
