# Four Pillars of OOPs Overview

> **TL;DR**: The four pillars of OOP — **Encapsulation, Abstraction, Inheritance, Polymorphism** — are the four structural guarantees the paradigm provides; every OOP keyword (`private`, `interface`, `extends`, `@Override`) exists to implement one of them.

## 1. Why Does This Exist?
The "four pillars" framing exists because OOP is not one feature but four complementary mechanisms, and interviewers need a compact way to test whether you understand the paradigm *structurally* rather than syntactically. Each pillar answers a distinct engineering question: Encapsulation answers "how do I keep data safe?"; Abstraction answers "how do I hide complexity?"; Inheritance answers "how do I reuse and specialize behavior?"; Polymorphism answers "how do I swap implementations without touching callers?" Together they make code *safe (encapsulation), simple (abstraction), reusable (inheritance), and extensible (polymorphism)* — the four properties that make large software maintainable. Without this structure, you'd have classes but no strategy for designing them.

## 2. How Does It Work?
- **Encapsulation**: bundle fields + methods into a class; make fields `private`; expose guarded public methods (`getBalance()`, `withdraw()`). The object is the only thing that can change its own state. Mechanism: access modifiers + method calls as the only mutation path.
- **Abstraction**: expose only the essential contract; hide implementation. Mechanism: `abstract` classes and `interface` in Java; the caller depends on the interface, not the concrete class.
- **Inheritance**: a class acquires the fields/methods of a parent via `extends`. Mechanism: the subclass's object layout *extends* the parent's; private members are inherited as inaccessible; `super` refers to the parent.
- **Polymorphism**: one method name/interface, many implementations, resolved at compile time (overloading) or runtime (overriding via vtable/dynamic dispatch). Mechanism: vtable lookup on virtual calls.

## 3. When Is It Used?
- **Encapsulation**: every time you define a class with private state — i.e., always, in production domain code.
- **Abstraction**: when defining contracts — service interfaces (`PaymentService`), repository interfaces, JDBC (`java.sql.Connection` is an interface hiding drivers).
- **Inheritance**: when you have a true "IS-A" relationship — `CheckingAccount extends Account`; frameworks' base classes (`HttpServlet`, `AbstractList`); code reuse across related classes.
- **Polymorphism**: anywhere you "program to an interface" — collections (`List` vs `ArrayList`), strategy pattern, listeners/handlers, dependency injection (Spring injects any implementation).

## 4. Why Wasn't Another Approach Chosen?
Each pillar beat a plausible alternative:
- *Encapsulation vs "trust programmers"*: without enforced hiding, bugs become cross-module; enforcement (compile-time access checks) is nearly free, so hiding was chosen over trust. (C chose trust; Java/C++ chose enforcement.)
- *Abstraction vs "just document it"*: docs rot; a typed interface that *compiles* to the contract is enforced. Interfaces were chosen over convention.
- *Inheritance vs pure composition/copy-paste*: copy-paste guarantees divergence; composition works, but for genuine is-a hierarchies inheritance is more direct and less boilerplate. Modern guidance: prefer composition *except* where is-a is real (covered in Part 03).
- *Polymorphism vs switch/if statements*: a `switch` on a type tag must be updated everywhere when a new type appears (Open-Closed violation); dynamic dispatch localizes the change to the new class. Dispatch was chosen over type-tag branching.
The key insight: each pillar automates and enforces what manual discipline could only approximate.

## 5. Intuition
Think of the four pillars as the rules of a **well-run company**:
- Encapsulation: each department's finances are private; only the department head approves spending.
- Abstraction: the CEO sees a dashboard (revenue, costs) — not the spreadsheets.
- Inheritance: "Manager" inherits from "Employee" and adds `approveExpense()`.
- Polymorphism: "give me the annual report" works the same whether you ask Sales, Engineering, or Legal — each produces its own report.

The four pillars are how OOP turns "code" into "an organization of cooperating units with boundaries, contracts, specialization, and interchangeable parts."

## 6. Real-World Analogy
A **car** demonstrates all four: Encapsulation — the engine's internals are sealed; you only use the pedals and wheel. Abstraction — you don't need to know whether it's combustion or electric; the interface (accelerator/brake/steering) is all you need. Inheritance — "SUV inherits from Car" (all cars accelerate, brake; SUV adds 4WD). Polymorphism — the pedal/interface behaves differently for a diesel vs an EV, and the driver's behavior doesn't change. One machine, four principles.

## 7. Formal Definition
**Encapsulation**: the bundling of data and the methods operating on that data into a single unit (class), with restricted access to the internal state, typically via private fields and public methods.
**Abstraction**: the process of hiding implementation details and exposing only the essential features (the contract/interface) of an object or system.
**Inheritance**: a mechanism whereby a new class (subclass/derived class) acquires the state and behavior of an existing class (superclass/base class), enabling reuse and specialization.
**Polymorphism** (Greek: "many forms"): the ability of objects of different types to respond to the same message/interface with type-appropriate behavior; achieved via method overloading (compile-time) and method overriding/virtual dispatch (runtime).

## 8. Example
A `Shape` system using all four pillars:
```java
public abstract class Shape {                 // ABSTRACTION: contract only
    public abstract double area();            // no implementation here
}
public final class Circle extends Shape {     // INHERITANCE: is-a Shape
    private final double radius;              // ENCAPSULATION: private state
    public Circle(double r) { if (r <= 0) throw new IllegalArgumentException(); this.radius = r; }
    public double area() { return Math.PI * radius * radius; }  // POLYMORPHISM: overrides area()
}
public final class Square extends Shape {
    private final double side;
    public Square(double s) { this.side = s; }
    public double area() { return side * side; }
}
// Client depends only on the abstraction:
Shape s1 = new Circle(2);                     // runtime dispatch decides which area() runs
Shape s2 = new Square(3);
System.out.println(s1.area());                // 12.566...
System.out.println(s2.area());                // 9.0
```
All four pillars in one small program: the client never touches `radius`/`side` (encapsulation), never knows the concrete type (abstraction), `Circle`/`Square` reuse the `Shape` type (inheritance), and `s1.area()` calls different code at runtime (polymorphism).

## 9. Internal Working
1. `Shape` compiles to a class with an abstract method; the JVM knows subclasses must implement `area()` (verifier enforces at load).
2. `Circle`'s object layout = header + `radius`; its class carries a vtable (method table) whose `area()` slot points to `Circle.area`.
3. `Shape s = new Circle(2)` stores a reference typed as `Shape` to a `Circle` object.
4. `s.area()` → JVM reads object header → klass pointer → vtable → jumps to `Circle.area` (in HotSpot, an inline cache or megamorphic dispatch handles this efficiently).
5. Encapsulation is enforced by the bytecode verifier: any access to `radius` outside `Circle` fails verification.
Each pillar is thus a *compiler/runtime-enforced* rule, not a convention.

## 10. Time Complexity
- Encapsulation: access-check + method call are O(1); no asymptotic change.
- Abstraction: interface dispatch adds one indirection — O(1).
- Inheritance: field layout is a compile-time offset — O(1); vtable lookup O(1), independent of hierarchy depth.
- Polymorphism: virtual dispatch O(1) (single indirection); JIT may inline (devirtualize) to O(1) direct call.
- **Takeaway**: all four pillars cost constant time per operation; their value is structural, not computational.

## 11. Advantages
- **Encapsulation** → data safety, low coupling, testable units.
- **Abstraction** → simplicity, decoupling, swap-ability of implementations.
- **Inheritance** → code reuse, logical is-a modeling, DRY.
- **Polymorphism** → extensibility (Open-Closed), strategy interchange, maintainable dispatch.

## 12. Disadvantages
- **Encapsulation** → boilerplate (getters/setters); can hinder some optimizations.
- **Abstraction** → over-abstraction (indirection layers with no payoff); harder debugging (implementation hidden).
- **Inheritance** → fragile base class problem; deep hierarchies; tight coupling (a change in parent ripples down).
- **Polymorphism** → vtable overhead; behavior less predictable than explicit switch; harder to trace.

## 13. Interview Questions
1. **Q: Name the four pillars and one keyword each.** A: Encapsulation (`private`), Abstraction (`interface`), Inheritance (`extends`), Polymorphism (`@Override`/vtable). 
2. **Q: Which pillar is `private` implementing?** A: Encapsulation — it hides state. But note `private` *only* hides; the *bundling* is the class itself.
3. **Q: TRICKY — "Abstraction and encapsulation are the same thing."** A: No. Encapsulation is the *mechanism* of hiding state; abstraction is the *strategy* of exposing a simplified contract. Encapsulation supports abstraction but they differ (compare the dedicated section in Part 02).
4. **Q: Which pillar does method overloading belong to?** A: Compile-time polymorphism (ad-hoc) — same name, different signatures resolved at compile time.
5. **Q: Which pillar does method overriding belong to?** A: Runtime polymorphism (subtype) — same signature, different implementations resolved via dynamic dispatch.
6. **Q: Can you have polymorphism without inheritance?** A: Yes — interfaces/duck typing (Python, Go interfaces) give polymorphism without class inheritance; also generics (parametric polymorphism) and overloading (ad-hoc). Java's `List` interface without inheritance of a class is the everyday example.
7. **Q: SCENARIO — Add a new `Triangle` to the shape system with zero changes to existing code.** A: Define `class Triangle extends Shape { ... }` implementing `area()`; the client loop `for (Shape s : shapes) sum += s.area();` works unchanged — this is polymorphism enabling the Open-Closed Principle.
8. **Q: PRACTICAL — Why is `switch`-on-type considered an anti-pattern versus polymorphism?** A: Every new type requires editing every switch (violates Open-Closed and DRY); with polymorphism, adding a class is the only change needed. Type-tag switches also leak knowledge of all variants into one place.
9. **Q: What is the "fragile base class problem"?** A: A change in a widely-used base class can subtly break many subclasses that rely on implementation details; a pillar-pair (inheritance + encapsulation) tension. Mitigated by preferring composition and interfaces.
10. **Q: Does every OOP language support all four pillars equally?** A: No — Java lacks multiple inheritance (pillar-tool: interfaces instead); C++ has it with diamond risk; Python has MRO-based multiple inheritance; Go has only composition+interfaces (no class inheritance). The pillars are language-independent ideals.
11. **Q: TRICKY — Which pillar is violated by a global mutable variable?** A: Encapsulation (and locality): a global is shared state with no owner guarding its invariants — the exact failure OOP's encapsulation pillar removes.
12. **Q: Which pillar does dependency injection primarily use?** A: Abstraction + polymorphism: clients depend on interfaces (abstraction) and the framework supplies any implementation (polymorphism at runtime).
13. **Q: PRODUCTION — Why do frameworks force you to implement interfaces (e.g., `Runnable`, `Comparator`)?** A: So the framework can call your code polymorphically at the right moment (callback/inversion of control) without knowing your concrete class — abstraction + polymorphism are the contract.
14. **Q: SCENARIO — Your app needs one method that accepts a dog, a cat, or a robot. Which pillar and mechanism?** A: Polymorphism via a common interface (`Speaker`) plus runtime dispatch; or generics (parametric polymorphism) if you only need type-safety, not behavior.
15. **Q: What's the difference between inheritance as reuse and inheritance as typing?** A: Inheritance-as-reuse uses the parent's code (dangerous — fragile base class); inheritance-as-typing uses the is-a relationship for polymorphic assignment. Prefer typing (interfaces); be wary of deep code-reuse hierarchies.

## 14. Follow-Up Questions
1. **Q: How do the pillars relate to the SOLID principles?** A: SRP/OCP leverage polymorphism; LSP governs inheritance correctness; ISP/DIP leverage abstraction. SOLID is essentially "apply the pillars with discipline."
2. **Q: Which pillar is most violated in real codebases?** A: Encapsulation (leaky getters returning mutable internals) and abstraction (classes exposing internals), plus inheritance misuse (is-a where has-a fits).
3. **Q: Is encapsulation a form of information hiding and vice versa?** A: Information hiding (Parnas) is the broader principle (hide design decisions); encapsulation is the language mechanism (private) that supports it.
4. **Q: Do records/sealed classes undermine any pillar?** A: No — records strengthen encapsulation (immutable fields) and sealed classes *limit* inheritance deliberately (exhaustive polymorphism, safer than unbounded `extends`).

## 15. Coding Example
A complete multi-pillar demo:
```java
public interface PaymentMethod {          // ABSTRACTION
    boolean pay(double amount);
}
public class CreditCard implements PaymentMethod {   // INHERITANCE (implements) + POLYMORPHISM
    private final String last4;          // ENCAPSULATION
    private double limit;
    public CreditCard(String last4, double limit) { this.last4 = last4; this.limit = limit; }
    public boolean pay(double amount) {
        if (amount <= 0 || amount > limit) return false;
        limit -= amount;
        return true;
    }
}
public class PayPal implements PaymentMethod {
    private double balance;
    public PayPal(double balance) { this.balance = balance; }
    public boolean pay(double amount) {
        if (amount > balance) return false;
        balance -= amount;
        return true;
    }
}
public class Checkout {
    public static void main(String[] args) {
        PaymentMethod cc = new CreditCard("1234", 1000);  // runtime type hidden
        PaymentMethod pp = new PayPal(500);
        double total = 250;
        PaymentMethod chosen = total > 600 ? cc : pp;      // strategy chosen dynamically
        System.out.println(chosen.pay(total));             // dispatch to PayPal.pay → true
    }
}
```
```cpp
// C++ equivalent: pure virtual base (abstraction), virtual override (polymorphism)
class PaymentMethod {
public:
    virtual ~PaymentMethod() = default;
    virtual bool pay(double) = 0;             // pure virtual = abstract contract
};
class CreditCard final : public PaymentMethod {
    std::string last4_; double limit_;
public:
    bool pay(double amount) override { return amount <= limit_ && (limit_ -= amount) >= 0; }
};
```
```python
# Python: duck-typed polymorphism (no explicit interface needed)
class CreditCard:
    def __init__(self, limit): self.__limit = limit          # name-mangled private
    def pay(self, amount):
        if amount > self.__limit: return False
        self.__limit -= amount; return True
def checkout(payment, amount): return payment.pay(amount)    # polymorphic call
```

## 16. Industry Usage
- **Java collections framework**: `List` (abstraction) + `ArrayList`/`LinkedList` (inheritance/implements + polymorphism) — used in virtually every Java codebase.
- **Spring**: `@Service` classes implement interfaces; DI swaps implementations at runtime (polymorphism). AOP proxies rely on interface dispatch.
- **Android**: `Activity`/`Fragment` lifecycle methods are polymorphism hooks; listeners (`OnClickListener`) are interfaces the OS calls.
- **Go**: interface-based abstraction + polymorphism with zero inheritance — proof that two pillars (abstraction, polymorphism) can stand alone.
- **AWS SDK (Java)**: clients behind interfaces; `DynamoDbClient` implementations swap locally vs remote (polymorphism + abstraction).
- **Python/Django**: `AbstractUser`, model inheritance, and duck-typed views — Python's dynamic typing makes polymorphism implicit.

## 17. References
- Grady Booch, *Object-Oriented Analysis and Design* — canonical four-pillar treatment.
- Erich Gamma et al., *Design Patterns* — pillars underlying every pattern.
- Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices* — pillars + SOLID.
- Java Tutorials, "Object-Oriented Programming Concepts": https://docs.oracle.com/javase/tutorial/java/concepts/
- GeeksForGeeks, "Four pillars of OOP": https://www.geeksforgeeks.org/four-pillars-of-object-oriented-programming/
- Python docs on duck typing: https://docs.python.org/3/glossary.html#term-duck-typing

## 18. Cheat Sheet
- Encapsulation = bundle + hide (`private`, getters).
- Abstraction = expose contract only (`interface`, `abstract`).
- Inheritance = is-a reuse (`extends`).
- Polymorphism = one interface, many forms (overloading = compile-time; overriding = runtime via vtable).
- Memory hook: "E-A-I-P" → "Every App Is Polymorphic."
- All four are enforced by the compiler/runtime, not by convention.
- Client code should depend on abstraction + polymorphism; subclasses honor LSP.

## 19. Quiz
1. `private` implements: a) abstraction b) encapsulation c) inheritance d) polymorphism → **b**
2. `interface` primarily implements: a) encapsulation b) abstraction c) aggregation d) overloading → **b**
3. Method overloading is: a) runtime polymorphism b) compile-time polymorphism c) encapsulation d) inheritance → **b**
4. Method overriding uses: a) compile-time binding b) runtime dynamic dispatch c) static binding d) none → **b**
5. Which pillar enables Open-Closed compliance? a) encapsulation b) abstraction c) polymorphism d) inheritance → **c** (polymorphism is the mechanism; abstraction defines the stable contract)
6. True or False: You can have polymorphism without inheritance. → **True** (interfaces, generics, duck typing)

## 20. Flashcards
- **Q: The four pillars?** → **A:** Encapsulation, Abstraction, Inheritance, Polymorphism.
- **Q: Pillar ↔ keyword map?** → **A:** Encapsulation→`private`; Abstraction→`interface`; Inheritance→`extends`; Polymorphism→`@Override`.
- **Q: Overloading vs overriding?** → **A:** Overloading = compile-time, same name different signature; Overriding = runtime, same signature via vtable.
- **Q: Pillar that removes type-switch need?** → **A:** Polymorphism (dispatch instead of `switch` on type tag).
- **Q: Fragile base class ties to which pillar?** → **A:** Inheritance misuse (deep code-reuse hierarchies).
- **Q: Abstraction vs encapsulation in one line?** → **A:** Encapsulation hides *state*; abstraction exposes a simplified *contract*.

## 21. Revision
OOP rests on four enforced pillars: Encapsulation bundles data+behavior and hides state (`private`); Abstraction exposes only the contract (`interface`/`abstract`); Inheritance provides is-a reuse (`extends`); Polymorphism gives one interface many implementations (overloading compile-time, overriding runtime via vtable). Each pillar costs O(1) per operation and buys structural safety and extensibility. Know the keyword map and the two trickiest distinctions — encapsulation vs abstraction, and overloading vs overriding — because both appear in nearly every OOP screen, plus the answer "polymorphism can exist without inheritance (interfaces/generics/duck typing)."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Name the four pillars." | Formal Definition / Section 13 |
| "Give one example each of the four pillars." | Example / Section 8 |
| "Encapsulation vs abstraction?" | Interview Q3 / Section 14 |
| "Overloading vs overriding?" | Interview Q4–Q5 |
| "Polymorphism without inheritance?" | Interview Q6 |
| "Switch-on-type vs polymorphism?" | Interview Q8 |
| "Fragile base class problem?" | Interview Q9 |
| "How do pillars enable DI frameworks?" | Interview Q12 / Industry Usage |
