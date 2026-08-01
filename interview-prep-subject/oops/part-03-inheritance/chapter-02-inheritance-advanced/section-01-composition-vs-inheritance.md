# Composition vs Inheritance

> **TL;DR**: Inheritance models "is-a" (a Dog is an Animal) and reuses a parent's code via `extends`; composition models "has-a" (a Car has an Engine) and reuses behavior by *delegating to a field* — and the industry guidance "favor composition over inheritance" says: use inheritance only for genuine is-a with stable bases, prefer composition for everything else.

## 1. Why Does This Exist?
Inheritance was the original reuse mechanism, but real-world experience exposed its costs: subclasses couple to parent *implementation* (the fragile base class problem), forced is-a relationships create Liskov violations, deep hierarchies get brittle, and a change at the top ripples through everything below. Composition exists as the safer alternative: instead of "be a kind of X," you *hold an X* and delegate to it. This buys **loose coupling** (you depend on the collaborator's interface, not its internals), **flexibility** (you can swap, wrap, add at runtime), and **safety** (no inherited behavior you didn't mean to get). The phrase "favor composition over inheritance" (Gang of Four) exists to correct the beginner instinct "I need those methods → I'll extend that class." Interviews ask it because it's the single most common OOP design-judgment question, and your answer shows whether you design by relationship or by convenience.

## 2. How Does It Work?
**Inheritance**: `class Dog extends Animal` — Dog *is* an Animal; gets Animal's fields/methods; overrides what's different.
**Composition**: `class Car { private Engine engine; }` — Car *has* an Engine; `Car.start()` delegates: `engine.start()`.

```java
// COMPOSITION — the "wrapper/delegator" pattern
class SmartPhone {
    private final Camera camera = new Camera();   // has-a
    public Photo shoot() { return camera.capture(); }  // delegate
}
class Camera { Photo capture() { ... } }
```
Behavior is reused by *calling the collaborator* rather than *inheriting it*; the class stays in control of its API and can swap the collaborator at construction or runtime.

## 3. When Is It Used?
- **Composition** (the default): 
  - Services holding repositories/HTTP clients (`OrderService { PaymentClient client; }`).
  - Wrappers/decorators (`BufferedReader wrapping a Reader`, `UnmodifiableCollection wrapping a Collection`).
  - Strategy injection (`TaxCalculator` field chosen at runtime).
  - When "has-a" is honest (a `Car` has wheels, engine).
- **Inheritance** (the exception):
  - Genuine is-a with stable base contracts (`SavingsAccount extends Account`, framework bases like `HttpServlet`).
  - Template-method hooks the base must enforce.
  - Where the language/framework *requires* it (Android `Activity`, servlets).

## 4. Why Wasn't Another Approach Chosen?
- *Why not inheritance for reuse (the naive choice)?* Because reuse-by-inheritance couples the subclass to the parent's implementation: fix the parent's method and silently change every subclass; the subclass also inherits *everything* (methods it didn't want). Composition chosen: you reuse only what you delegate to, and you control the surface.
- *Why not composition for is-a (the other extreme)?* Because a `SavingsAccount` genuinely needs to be *usable as* an `Account` (pass to `List<Account>`, override `withdraw`) — a plain has-a can't give you that subtype typing. Inheritance chosen where the relationship is *real is-a*.
- *Why not a middle "prefer composition unless..."?* That *is* the industry answer (GoF: "Favor composition over inheritance"); the exceptions are stable framework bases and genuine is-a. Both tools stay in the language because each matches one relationship.
- *Why not mixins/interfaces only?* Mixins (interfaces with default methods) give reuse without class inheritance — often the best of both; but they can't carry instance state (Java), so real shared state still needs either a base class or composition.

## 5. Intuition
Think of **inheritance as "you ARE a cow"** — you get four stomachs whether you like it or not, and if the cow spec changes, you change. **Composition as "you OWN a cow"** — you get milk *when you ask for it* (`myCow.milk()`), you can swap the cow for a goat, and the cow's internal changes don't force changes on you. Owning is usually safer than being: it keeps your identity (interface) yours while borrowing capability on your terms.

## 6. Real-World Analogy
A **restaurant owner vs a franchise**. Franchise = inheritance: you ARE the brand — you inherit the menu, decor, processes (the base class), and you can't easily change things without the brand's approval; when corporate changes the menu, you must change too (fragile base). A private chef with contractors = composition: the chef (your class) *hires* a pastry contractor (a collaborator) and delegates desserts to them; swap the contractor (change the implementation), keep your restaurant (your interface) intact. Owning contractors is more flexible than being a franchise — the GoF argument in everyday terms.

## 7. Formal Definition
**Inheritance** is a class-based reuse mechanism establishing an *is-a* relationship: a subclass is a subtype of its superclass and reuses/overrides its implementation; it is appropriate when the subclass genuinely substitutable for the superclass (LSP) and the base is designed as an extension contract. **Composition** is an object-based reuse mechanism establishing a *has-a* relationship: a class contains a collaborator object (usually via a field, typically injected) and delegates behavior to it; it is appropriate when a class *uses* another's capabilities without being *a kind of* it. **Favor composition over inheritance** (Gang of Four): prefer object delegation over class derivation unless inheritance's subtype/extension guarantees are actually required, because composition yields looser coupling, greater flexibility, and fewer fragile-base hazards.

## 8. Example
```java
// INHERITANCE — a genuine is-a with a stable base
public class Account {
    protected double balance;
    public void deposit(double amt) { if (amt > 0) balance += amt; }
    public double getBalance() { return balance; }
}
public class SavingsAccount extends Account {   // IS-A
    public void addInterest(double rate) { balance += balance * rate; }
}

// COMPOSITION — has-a with delegation
public class ReportExporter {
    private final Formatter formatter;          // collaborator (has-a)
    public ReportExporter(Formatter formatter) { this.formatter = formatter; }  // inject
    public String export(Report r) {
        return formatter.format(r);             // DELEGATE, don't inherit
    }
}
public interface Formatter { String format(Report r); }
public class JsonFormatter implements Formatter { public String format(Report r) { return "{}"; } }
public class CsvFormatter  implements Formatter { public String format(Report r) { return "a,b"; } }
```
`SavingsAccount` is-a `Account` (subtype, overriding hooks); `ReportExporter` has-a `Formatter` (delegates, swappable). The second is the pattern the "favor composition" rule pushes.

## 9. Internal Working
1. **Inheritance**: subclass object layout embeds the parent's fields; methods are inherited via the vtable chain; a change to the parent's method recompiles/republishes behavior for all subclasses (the coupling is structural).
2. **Composition**: the class holds a *reference* (or value) to the collaborator; delegation is an explicit method call to `field.method()`; swapping the collaborator is a construction-time/injection decision (composition root); the wrapping class's API is entirely its own.
3. **Testing**: composition is trivially testable — inject a mock/stub collaborator; inheritance testing requires subclass seams or test harnesses (harder).
4. **Runtime choice**: composition allows *runtime* strategy replacement (swap formatter at runtime); inheritance's "behavior" is fixed at compile time.
The mechanism difference: inheritance shares code *through the type hierarchy*; composition shares code *through object references*.

## 10. Time Complexity
- Inheritance call: O(1) vtable.
- Composition/delegation call: O(1) — one more indirection (field deref + call); JIT-inlinable.
- Both constant-time; composition costs one pointer dereference (negligible). No asymptotic difference.
- Composition can wrap/unwrap — each layer adds O(1); inheritance depth adds nothing per call.

## 11. Advantages
**Composition:**
- Loose coupling (depends on collaborator's contract, not internals).
- Swap-ability (strategy, test fakes) and runtime flexibility.
- No inherited junk (only delegate what you need).
- No fragile-base ripple; encapsulation preserved.
- Easier testing (inject mocks).

**Inheritance:**
- Direct is-a typing (subtype polymorphism).
- Shared state/code with one source of truth.
- Framework hooks and template methods (when the base is designed as a contract).

## 12. Disadvantages
**Composition:**
- Boilerplate delegation (re-type every forwarded method).
- No automatic is-a typing (must implement interfaces for that).
- Indirection (one extra hop).

**Inheritance:**
- Fragile base class (parent change ripples).
- Forced is-a (LSP violations).
- Inherits everything (even unwanted methods).
- Coupling to parent internals; breaks encapsulation.
- Deep hierarchies get brittle and untraceable.

## 13. Interview Questions
1. **Q: Composition vs inheritance — when each?** A: Inheritance for genuine is-a with a stable base (`SavingsAccount extends Account`); composition for has-a / uses-a (`Car` holds an `Engine`, `Service` holds a client) — and per the GoF, favor composition by default.
2. **Q: Why "favor composition over inheritance"?** A: Composition gives loose coupling (depend on a contract, not parent internals), swap-ability (runtime strategy, mocks), and avoids the fragile base class problem; inheritance couples you to the parent's implementation and forces everything down the hierarchy.
3. **Q: TRICKY — "Inheritance is for code reuse."** A: Reuse is a *benefit*, not the justification. Using inheritance purely to reuse methods (no is-a) is the #1 misuse — you inherit behaviors you don't want and couple to internals; composition is the reuse mechanism for non-is-a.
4. **Q: What is the fragile base class problem?** A: A change to a widely-used base class can silently break subclasses that depended on its implementation details — even subclasses that never changed. Composition avoids it because you depend on a collaborator's *interface*, not its insides.
5. **Q: Give a "wrong inheritance" example.** A: `class Stack extends Vector` — a Stack is-not-a Vector (Vector allows index access; Stack shouldn't); the classic JDK design error. Correct: `Stack` should compose a list. Similarly `Bird`/`Penguin` with `fly()`.
6. **Q: SCENARIO — `OrderService` needs `PaymentClient` and `InventoryClient`. Design?** A: Composition: `private final PaymentClient payments; private final InventoryClient inventory;` injected via constructor; the service delegates. Not inheritance — a service IS-NOT a payment client.
7. **Q: When does inheritance genuinely win?** A: (1) Real is-a where you need subtype typing (`List<Account>`), (2) template-method frameworks that must enforce a skeleton (`HttpServlet`), (3) when the base is a designed extension contract (`AbstractList`). Otherwise compose.
8. **Q: TRICKY — Can you get subtype typing with composition?** A: Yes — implement an *interface*: `class OrderService implements Payable { private final ...; public boolean pay(...) { return delegate.pay(...); } }`. Interfaces give the is-a *type* without the is-a *implementation* — the best of both.
9. **Q: How does the strategy pattern relate?** A: Strategy is composition: an object holds a strategy (e.g., `TaxCalculator`) field and delegates — swapping at runtime changes behavior. It exists *because* composition beats inheritance for behavior variation.
10. **Q: PRODUCTION — Why do modern teams ban deep inheritance but allow interfaces everywhere?** A: Interfaces are *contracts* (no implementation to couple to); class inheritance couples to implementation. The industry pattern: interfaces for typing, composition for reuse, inheritance only for stable framework/domain bases.
11. **Q: What is delegation?** A: Composition's core mechanism: a class holds a collaborator and *forwards* calls to it — `myCollaborator.doSomething()`. It's "has-a with forwarding," the technical heart of "favor composition."
12. **Q: SCENARIO — `Writer` base with `FileWriter`, `NetworkWriter`, `BufferedWriter`. Design?** A: `Writer` as an interface or abstract class (is-a for the writers) BUT `BufferedWriter` should *wrap* a Writer (composition — has-a + delegate), not extend it — the JDK's `BufferedWriter` wraps a `Writer`. Layering via composition.
13. **Q: TRICKY — Composition vs inheritance for testing?** A: Composition wins: inject a fake collaborator (mock), test the class in isolation. Inheritance couples tests to the hierarchy and can't substitute collaborators without subclass seams.
14. **Q: What's the "inheritance tax"?** A: The accumulated cost of coupling: parent changes ripple, unwanted methods leak in, deep chains are hard to trace, and every level constrains the design. Composition avoids most of it.
15. **Q: PRACTICAL — Refactor a class that extends a utility for its methods.** A: Change `extends Utility` to a `private final Utility utility` field + delegate the needed methods (or extract the behavior into an interface the class implements); the class now owns its API and isn't coupled to `Utility`'s internals.

## 14. Follow-Up Questions
1. **Q: What is the difference between "white-box" and "black-box" reuse?** A: White-box = inheritance: the subclass sees the parent's internals (protected), so reuse depends on implementation detail. Black-box = composition: reuse through the collaborator's public interface only. Composition (black-box) is safer — you depend on contract, not internals.
2. **Q: When is "composition over inheritance" wrong?** A: When the domain really is is-a *and* you need subtype polymorphism *and* the base is stable and designed for extension — forcing composition then adds delegation boilerplate with no benefit. The rule is a preference, not a law.
3. **Q: How do mixins/traits fit?** A: They're reusable behavior chunks shared without class inheritance (Java interface default methods, C++ CRTP, Python mixins) — a third option: reuse behavior + some code, but no base-class coupling. Often the cleanest middle ground.
4. **Q: What does the Decorator pattern demonstrate?** A: That layering by composition (wrapping) is the flexible alternative to deep inheritance for adding behavior — `BufferedInputStream` wrapping `FileInputStream` — the JDK's real-world proof of composition's power.

## 15. Coding Example
```java
// Composition in action: a NotificationService that delegates to a transport
public interface Transport { void send(String msg); }
public class EmailTransport implements Transport { public void send(String m) { System.out.println("email: " + m); } }
public class SmsTransport    implements Transport { public void send(String m) { System.out.println("sms: " + m); } }

public class NotificationService {
    private final Transport transport;                 // has-a
    public NotificationService(Transport transport) { this.transport = transport; }
    public void notify(String user) { transport.send("hi " + user); }   // delegate
}
// Usage — swap implementations at the composition root, no inheritance:
//   new NotificationService(new EmailTransport())
//   new NotificationService(new SmsTransport())
```
```python
class NotificationService:
    def __init__(self, transport): self.transport = transport   # composition
    def notify(self, user: str) -> None: self.transport.send(f"hi {user}")
```
```cpp
// C++ composition: member object + delegation (strategy pattern)
class NotificationService {
    std::unique_ptr<Transport> transport_;    // has-a
public:
    explicit NotificationService(std::unique_ptr<Transport> t) : transport_(std::move(t)) {}
    void notify(const std::string& u) { transport_->send("hi " + u); }
};
```

## 16. Industry Usage
- **JDK**: `BufferedWriter`/`BufferedReader` wrap `Writer`/`Reader` (composition); `Collections.unmodifiableList` wraps a list (composition); `Stack extends Vector` is the *historical mistake* that taught the industry.
- **Spring**: services compose repositories/clients (constructor-injected collaborators) — the entire framework is composition with interfaces; inheritance appears only for framework bases.
- **Android**: `Activity` (inheritance from framework base) + composition everywhere else (a `ViewHolder` composes views; RecyclerView adapters compose a dataset).
- **Go**: no class inheritance at all — embedding + interfaces = pure composition; the language's philosophy is the rule's logical endpoint.
- **Domain-Driven Design**: entities compose value objects and services; inheritance reserved for genuine subtyping (e.g., payment types).
- **Every code review guide** (Effective Java Item 18 "prefer composition to inheritance") — the single most-cited OOP design guideline in industry.

## 17. References
- Erich Gamma et al., *Design Patterns* — "Favor object composition over class inheritance" (intro).
- Joshua Bloch, *Effective Java* — Item 18 (favor composition over inheritance).
- Robert C. Martin, *Clean Architecture* — inheritance vs composition in architecture.
- JDK example: `Stack extends Vector` (historical cautionary tale), `BufferedReader` composition.
- GeeksForGeeks, "Inheritance and Composition": https://www.geeksforgeeks.org/inheritance-and-composition-in-java/

## 18. Cheat Sheet
- Inheritance = is-a; composition = has-a.
- Favor composition by default (GoF); inheritance for genuine is-a + stable base.
- Composition = hold collaborator + delegate (`field.method()`).
- Fragile base class = why inheritance-with-reuse hurts.
- Interfaces give is-a *typing* without is-a *implementation*.
- Strategy/Decorator = composition patterns.
- `Stack extends Vector` = the classic wrong-inheritance example.
- Testability: composition wins (inject mocks).

## 19. Quiz
1. `class Car { Engine engine; }` is: a) inheritance b) composition c) polymorphism d) abstraction → **b**
2. "Favor composition over inheritance" is from: a) Effective Java b) Gang of Four c) JLS d) Parnas → **b**
3. The fragile base class problem motivates: a) inheritance b) composition c) statics d) final → **b**
4. `BufferedReader` wrapping a `Reader` is: a) is-a b) composition c) multiple inheritance d) hiding → **b**
5. `Stack extends Vector` is wrong because: a) too slow b) Stack is-not-a Vector c) Vector is private d) it compiles → **b**
6. True or False: Inheritance is never appropriate. → **False** (genuine is-a with stable bases)

## 20. Flashcards
- **Q: Is-a vs has-a?** → **A:** Is-a → inheritance; has-a → composition (delegation).
- **Q: The GoF rule?** → **A:** Favor composition over inheritance.
- **Q: Fragile base class?** → **A:** A parent change silently breaks subclasses that depended on its internals.
- **Q: How to get subtype typing without class inheritance?** → **A:** Implement an interface + delegate (composition).
- **Q: Composition's mechanism?** → **A:** Hold a collaborator field; forward calls (`field.method()`).
- **Q: When does inheritance win?** → **A:** Genuine is-a, stable base, template/framework hooks.
- **Q: The classic wrong-inheritance example?** → **A:** `Stack extends Vector`.

## 21. Revision
Inheritance = is-a (subtype typing + shared code, couples to parent internals, fragile-base risk); composition = has-a (hold a collaborator and delegate, loose coupling, swappable, testable). The GoF rule "favor composition over inheritance" says: default to composition; use inheritance only for genuine is-a with a stable, extension-designed base (frameworks, real domain subtyping). Interfaces give subtype typing without implementation inheritance — the usual best tool. First-30-seconds answers: "is-a → inherit, has-a → compose; composition avoids the fragile base class problem."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Composition vs inheritance?" | Interview Q1 / Section 8 |
| "Why favor composition?" | Interview Q2 / Section 4 |
| "Inheritance is for reuse?" | Interview Q3 |
| "Fragile base class problem?" | Interview Q4 |
| "Wrong-inheritance examples?" | Interview Q5 / Section 16 |
| "When does inheritance win?" | Interview Q7 |
| "Strategy pattern + composition?" | Interview Q9 |
| "Refactor extends-a-utility?" | Interview Q15 |
