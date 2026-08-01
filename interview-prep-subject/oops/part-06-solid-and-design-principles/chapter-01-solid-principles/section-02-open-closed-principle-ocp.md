# Open/Closed Principle (OCP)

> **TL;DR**: Software should be **open for extension but closed for modification** — you add new behavior by adding new code (new subclasses/implementations), not by editing existing, working classes; polymorphism (Part 04) is the mechanism, and interfaces are the seam.

## 1. Why Does This Exist?
Every time you *edit* a working class to add a new feature, you take a risk: the new code can break every existing consumer of that class, and you must re-test everything downstream. OCP exists to make the **common case — adding behavior — a zero-risk operation**: write a new class that plugs in through an existing contract; nothing that works is touched. The principle generalizes from a sharp observation: the code that *already works* and *already ships* is your asset; editing it for every new requirement converts every feature request into a potential regression. Bertrand Meyer coined it ("open for extension, closed for modification") to describe a design where the *abstraction* is fixed and stable while the *variations* are infinite. In modern terms, OCP = "add a new `Strategy`, don't edit the `switch`."

## 2. How Does It Work?
1. Identify the **variation point**: the axis along which requirements grow (payment methods, notification channels, report formats, animal sounds).
2. Define a **stable contract** (interface/abstract class) that captures the *what* but not the *which*: `Payment { pay(double) }`, not `CardPayment`.
3. Route the caller through the contract: `payment.pay(amt)` instead of `if (type == CARD) ...`.
4. **Extend** by implementing the contract for each new variation: `add class UpiPayment implements Payment`. The caller and existing implementations never change.
5. **Close** the contract: once stable, don't add methods to it casually (that's a modification rippling to all implementations — consider ISP/extension instead).
The guarantee: new feature = new file, existing tests untouched, existing behavior provably unchanged.

## 3. When Is It Used?
- **Adding a new variant**: new payment type, new notification channel, new export format, new discount rule → implement the existing contract; don't edit callers.
- **Extensible frameworks**: plugin systems, strategy registry, config-driven behavior selection.
- **Strategy/Policy variation**: sorting, validation rules, pricing, tax policies.
- **Growing the type family** (the classic): `Shape.area()` — adding `Circle`, `Triangle` by implementing, not by editing a switch.
- **Not when**: the variation set is small *and fixed* (a two-case `switch` on a stable enum is sometimes simpler than an interface); or the "extension" requires changing the contract's meaning (that's a real API change, not extension).

## 4. Why Wasn't Another Approach Chosen?
- *Why not just add `else if` branches?* Each branch edits shared, working code; the caller's test matrix grows; the caller must know about every implementation (tight coupling to the world). OCP inverts: the caller knows *one* contract; the world registers through it.
- *Why not reflection/scripting for variation?* Plugins/rules engines are legitimate OCP *implementations* (the contract is the plugin interface), but hard-coded reflection without a contract is opaque and untyped — OCP wants a *named seam*.
- *Why not YAGNI-only (edit when needed)?* YAGNI (Part 06 ch-02) is the correct counterweight: don't build the interface *before* the second variation appears. OCP kicks in *once a second variation is visible* — the two principles calibrate each other, not conflict.
- *Why interfaces rather than inheritance?* Both work; interfaces (Part 02) allow implementing many contracts and decouple *behavior* from *hierarchy*, which is exactly the seam OCP needs. Inheritance-based extension is the older, more coupling-heavy version.
- *Why is "closed for modification" not absolute?* Nothing is truly closed — bug fixes, contract changes, and evolution modify code. OCP means *extension shouldn't require modification* for the *intended* growth axis, not that the file never changes.

## 5. Intuition
A **power socket** is open for extension, closed for modification: the wall socket (the contract) never changes; you plug in *new* devices (new implementations) — a phone charger, a kettle, a vacuum — each designed to the socket's spec. If instead the wall had a fixed, hard-wired kettle (a `switch` on one concrete thing), adding a phone charger meant rewiring the wall (editing the caller). The socket's genius: the interface is stable; the devices multiply. In code, `Payment` is the socket, `CardPayment`/`UpiPayment`/`PaypalPayment` are the devices, and the caller just "plugs in."

## 6. Real-World Analogy
A **restaurant menu built by substitutions**. The kitchen's *process* (take order → cook → plate) is closed for modification — the workflow never changes. But the *menu* is open for extension: tonight's special is added as a new dish (a new recipe implementing the "cook a dish" contract) without rewriting the kitchen. The alternative — editing the cooking process for every new dish — would mean re-certifying the whole kitchen each week. The menu/process separation is the OCP seam: stable process, growing dish list, new dish = new recipe file.

## 7. Formal Definition
**Open/Closed Principle** (Bertrand Meyer, 1988): a class/module should be **open for extension** (its behavior can be extended as new requirements arrive) but **closed for modification** (extending behavior must not require changing the module's source). Mechanism (modern OO): define a stable abstraction (interface/abstract class) capturing the fixed behavior; the module depends only on that abstraction; new behaviors are supplied by *new* implementations of the abstraction, registered/pluggable at the call site. Then, for any new variation V, the set of modified files is empty and the set of added files is one (the new implementation). Equivalently: the module's change-trigger set under "add variation" is constant.

## 8. Example
```java
// CLOSED-FOR-MODIFICATION seam
interface Discount { double apply(double amount); }

// OPEN-FOR-EXTENSION: add variations as new files — never edit this caller
class Checkout {
    private final Discount discount;
    Checkout(Discount d) { this.discount = d; }
    double total(double amount) { return discount.apply(amount); }
}

// EXISTING implementations — untouched when a new one arrives
class NoDiscount implements Discount { public double apply(double a) { return a; } }
class TenPercent implements Discount { public double apply(double a) { return a * 0.9; } }

// NEW requirement: "flat 100 off" → ONE new file, zero edits
class FlatOff implements Discount { private final double off; FlatOff(double o) { off = o; } public double apply(double a) { return Math.max(0, a - off); } }

// WITHOUT OCP, the same requirement edits the caller:
double total(double amount, String type) {
    if (type.equals("TEN")) return amount * 0.9;          // ← every new discount edits this
    else if (type.equals("FLAT")) return amount - 100;    // ← and re-tests all old ones
    return amount;
}
```
The OCP version: new discount = add `FlatOff`; `Checkout` and tests of `Checkout` never change.

## 9. Internal Working
1. **Identify the growth axis**: examine requirements history — what keeps changing? (payment types, formats, rules). That axis becomes the abstraction.
2. **Introduce the seam**: an interface with the *stable* signature; the caller holds the interface, not the concrete class.
3. **Route calls polymorphically**: replace `switch`/`if-else` dispatch with a single virtual call — the interface reference dispatches by object type (Part 04: vtable).
4. **Wire via composition/DIP**: the concrete implementation is supplied by the caller (DI, factory, registry) — the caller itself becomes open (it composes), and the *core* stays closed.
5. **Guard the seam**: keep the interface stable; resist adding methods that existing implementations must then implement (that's modification — use default methods or a new interface).
6. **Test strategy**: the closed modules keep their tests; each new implementation brings its own test — the OCP design keeps the test matrix additive.

## 10. Time Complexity
- No algorithmic cost change — OCP is structural. Dispatch through the interface is the same O(1) vtable call as any polymorphic call.
- Indirect win: adding behavior is O(1) developer work (one new class) rather than O(existing callers) edits — a *maintenance* complexity saving, not a CPU one.
- One extra indirection layer vs direct concrete calls — negligible and usually devirtualized (Part 04).

## 11. Advantages
- **Zero-regression extension**: new behavior never touches working code.
- **Additive testing**: old tests unchanged; new tests per new implementation.
- **Parallel development**: the new feature is a new file — no merge contention with existing code.
- **Contract clarity**: the interface documents exactly what "a variation" must provide.
- **Foundation for patterns**: OCP is what Strategy, Decorator, Factory, and Template Method all implement (Part 07+).

## 12. Disadvantages
- **Interface proliferation**: a seam for every potential variation → many one-implementation interfaces (violates YAGNI until the second variation exists).
- **Indirection**: callers lose the concrete type; debugging "which implementation ran" needs a trip through the vtable.
- **Contract rigidity**: a *wrongly guessed* interface becomes the ceiling — extending past it needs a modification (the very thing you avoided).
- **Over-abstraction**: pre-emptive seams for variations that never arrive are dead code and cognitive load.
- **Behavioral consistency burden**: every new implementation must honor the contract (LSP) or the "closed" core silently misbehaves.

## 13. Interview Questions
1. **Q: What is OCP?** A: A module should be open for extension (add behavior via new code) but closed for modification (adding behavior shouldn't require editing the module's existing code). Implemented with stable interfaces + polymorphic dispatch.
2. **Q: How do you implement OCP in Java?** A: Define an interface for the variation point; make callers depend on the interface; each new behavior is a new implementation — added, not edited. Wire implementations via DI/factory/registry.
3. **Q: TRICKY — "Closed for modification" means the file never changes?** A: No. It means *extending behavior* doesn't require modification. Bug fixes, contract changes, and refactors still modify code. The intent: the *growth axis* of your requirements shouldn't force edits to the stable core.
4. **Q: SCENARIO — New payment method arrives monthly; current code is a `switch` on type. What do you do?** A: Extract a `PaymentProcessor` interface, route the switch's cases through it (each case → an implementation), then each new method is a new class. The switch disappears; the caller closes.
5. **Q: What's the difference between OCP and just "good interfaces"?** A: OCP is the *goal* (extension without modification); the interface is the *mechanism*. "Good interfaces" alone don't give OCP — the interface must be on the *growth axis* and callers must route through it rather than concrete types.
6. **Q: PRODUCTION — Strategy pattern is OCP?** A: Yes — the strategy interface is the seam; adding `Guava`'s or a new `Comparator` is adding an implementation, never editing the client. Strategy is the canonical OCP implementation (Part 07).
7. **Q: When is OCP over-engineering?** A: When the variation hasn't appeared yet — one concrete class with no second variant doesn't need an interface (YAGNI). The principle pays off at the *second* variant, so introduce the seam when you see it coming.
8. **Q: TRICKY — Adding a default method to an interface modifies it — violation?** A: Not necessarily. If existing implementations *don't change* and new behavior is available through the default, the concrete classes stay closed. But it's a contract change — treat it as a real decision, not a freebie.
9. **Q: SCENARIO — A report generator supports PDF; now you need CSV and JSON. OCP fix?** A: `interface ReportExporter { void export(Report r); }` with `PdfExporter`, `CsvExporter`, `JsonExporter`; the generator depends on `ReportExporter` — the generator is closed, the format list is open.
10. **Q: PRODUCTION — How does Spring's plugin/strategy style enable OCP?** A: Beans are registered by type; a `List<Handler>` injected into a dispatcher routes to all implementations — adding a handler is a new `@Component` class; the dispatcher never changes. That's OCP via dependency injection.
11. **Q: How does OCP interact with SRP?** A: SRP makes each class narrow (one reason to change); OCP then lets you extend *without* changing that narrow class — the narrowness is what makes "closed" achievable. A god class can't be closed because every feature touches it.
12. **Q: TRICKY — Can you achieve OCP without inheritance?** A: Yes — via composition: the caller holds a strategy/function (functional interfaces in Java: `Function`, `Consumer`), and extension = new lambda. The interface (or functional interface) is still the seam; inheritance isn't required.
13. **Q: How does OCP relate to LSP?** A: OCP's safety depends on LSP: extension is safe only if every new implementation honors the contract. An LSP-violating subclass "extends" the system but silently breaks the closed core.
14. **Q: PRODUCTION — You keep changing an interface because requirements evolve. What's the real lesson?** A: The abstraction was guessed wrong — the *growth axis* wasn't where you put the seam. Lesson: design seams around the *stable* core and the *frequently-varying* edge; expect to reposition seams as you learn the domain (OCP is iterative, not one-shot).

## 14. Follow-Up Questions
1. **Q: OCP vs the Open/Closed "SOLID" acronym — same?** A: Same principle; the acronym order (S-O-L-I-D) is just mnemonic. OCP is the second letter and the one most directly "enabled by" DIP.
2. **Q: How does OCP apply at the *module* level?** A: Package boundaries: a stable API package with implementations in plugin packages; service providers (Java `ServiceLoader`, SPI) are module-level OCP — add a provider JAR, no core changes.
3. **Q: What's the connection to "program to an interface, not an implementation"?** A: They're the same discipline — programming to an interface is what *makes* the module closed for modification; the interface is the contract, implementations vary. OCP is the *reason* behind the mantra.
4. **Q: How do dependency injection and OCP reinforce each other?** A: DI supplies implementations at runtime without the caller knowing them — DI is the *wiring* that lets OCP hold: callers stay closed, and swapping/adding implementations requires no caller edit.

## 15. Coding Example
```java
import java.util.*;
// Seam on the growth axis: "how a notification is delivered"
interface Notifier { void notify(String message); }
class EmailNotifier implements Notifier { public void notify(String m) { print("email: " + m); } }

// Closed core: the alert system depends only on Notifier
class AlertSystem {
    private final List<Notifier> notifiers;
    AlertSystem(List<Notifier> n) { notifiers = n; }
    void raise(String msg) { for (Notifier n : notifiers) n.notify(msg); }
}
// Extension 1: SMS — one new class, no edits
class SmsNotifier implements Notifier { public void notify(String m) { print("sms: " + m); } }
// Extension 2: Slack — one new class, no edits
class SlackNotifier implements Notifier { public void notify(String m) { print("slack: " + m); } }

public class Main {
    public static void main(String[] args) {
        AlertSystem system = new AlertSystem(List.of(new EmailNotifier(), new SmsNotifier(), new SlackNotifier()));
        system.raise("disk full");     // three channels — and adding a 4th never touches AlertSystem
    }
}
```
Every new channel = new `Notifier` class registered at the composition root. `AlertSystem` is closed; the channel set is open. Without OCP, every channel meant editing `AlertSystem` and re-testing all channels.

## 16. Industry Usage
- **JDK**: `Comparator`, `Runnable`, `Function` — the JDK is *closed*; your code *extends* it by implementing these seams. `Collections` works for any `List` implementation because it depends on the `List` abstraction.
- **Spring**: strategy beans (`List<Handler>` injection), `ServiceLoader`-based providers, `@ConditionalOnX` configuration — extension by adding beans, not editing framework code.
- **Servlets/Jakarta**: the container is closed; you extend via `HttpServlet` overrides — new servlet = new class, no container modification.
- **Databases/drivers**: JDBC is the seam; new DB = new driver JAR implementing `Driver`, no app code change.
- **Logging (SLF4J)**: the app is closed against the concrete logger; bind a new backend by adding a provider.

## 17. References
- Bertrand Meyer, *Object-Oriented Software Construction* (1988) — original OCP definition.
- Robert C. Martin, *Clean Architecture*, Ch. 9 — OCP and its role in the dependency rule.
- *Agile Software Development: Principles, Patterns, and Practices* (Robert Martin) — OCP chapter.
- Eric Freeman et al., *Head First Design Patterns* — Strategy as the OCP pattern.
- GeeksForGeeks, "Open Closed Principle": https://www.geeksforgeeks.org/open-closed-principle-in-java-with-examples/

## 18. Cheat Sheet
- OCP = open for extension, closed for modification.
- "Closed" = extension doesn't require editing existing code.
- Seam = interface on the growth axis.
- Mechanism = polymorphic dispatch (vtable).
- New behavior = new implementation file, zero edits.
- Callers hold interfaces, not concrete classes.
- Don't pre-abstract — YAGNI until the 2nd variation.
- Depends on LSP (implementations must honor the contract).
- Patterns: Strategy, Decorator, Template Method, Factory.
- OCP ≠ "never modify"; bugs/contracts still change code.

## 19. Quiz
1. OCP means: a) never edit code b) extend without modification c) always use interfaces d) no inheritance → **b**
2. The OCP seam is typically: a) a static method b) an interface c) a package d) a thread → **b**
3. Adding a new discount type per OCP requires: a) editing caller b) new class implementing contract c) new switch case d) reflection → **b**
4. Who coined OCP? a) GoF b) Bertrand Meyer c) Alan Turing d) John McCarthy → **b**
5. OCP safety depends on: a) SRP only b) LSP c) YAGNI d) IPC → **b**
6. True or False: OCP means the file never changes. → **False**

## 20. Flashcards
- **Q: OCP definition?** → **A:** Open for extension, closed for modification.
- **Q: Mechanism?** → **A:** Stable interface seam + polymorphic dispatch.
- **Q: New variation = ?** → **A:** One new implementation file, zero edits.
- **Q: When NOT to apply?** → **A:** Before the second variation exists (YAGNI).
- **Q: OCP depends on?** → **A:** LSP — implementations must honor the contract.

## 21. Revision
OCP: a module should be open for extension (add behavior with new code) but closed for modification (adding behavior shouldn't require editing existing code). Implement: find the growth axis → define a stable interface → route callers through it → each new variation is a new implementation. The safety relies on LSP (implementations honor the contract). Don't pre-abstract — introduce the seam at the second variation (YAGNI). Patterns that realize it: Strategy, Decorator, Factory, Template Method; DI is the wiring that makes it practical. OCP ≠ "never edit"; bugs and real contract changes still modify code. First-30-seconds answer: "New behavior = new implementation behind a stable interface — callers never edit, they plug in."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is OCP?" | Interview Q1 / Section 2, 7 |
| "How to implement OCP in Java?" | Interview Q2 / Section 8 |
| "Closed means file never changes?" | Interview Q3 / Section 4 |
| "Fix this payment switch" | Interview Q4 / Section 8 |
| "Strategy pattern = OCP?" | Interview Q6 / Section 16 |
| "When is OCP over-engineering?" | Interview Q7 / Section 12 |
| "Default method = violation?" | Interview Q8 / Section 9 |
| "OCP without inheritance?" | Interview Q12 |
