# Interface Segregation Principle (ISP)

> **TL;DR**: No client should be forced to depend on methods it doesn't use — split fat interfaces into narrow, role-specific ones so each client depends only on what it actually calls; many *client-specific* interfaces beat one *general* interface.

## 1. Why Does This Exist?
A fat interface — `Animal` with `fly()`, `swim()`, `run()`, `bark()` — forces every implementer to write stubs it doesn't need and forces every client to *depend on* methods it never calls. Dependence is the problem: if `Animal` changes `fly()`, every client of `Animal` recompiles and re-tests even if it only ever called `run()`. The interface is a *contract* — and a contract that includes methods a client doesn't use is a contract the client doesn't agree to, coupling it to changes it doesn't care about. ISP exists to **minimize the surface of each dependency**: each client should depend on the *smallest* interface that fully expresses its needs. The JDK's own lesson is the canonical example: `java.awt.event` splits listeners into `MouseListener`, `KeyListener`, `ActionListener`, etc., so a button doesn't force you to implement mouse-wheel handlers you never use. ISP is SRP applied to *interfaces*.

## 2. How Does It Work?
1. Find the **fat interface**: one interface whose implementers implement most methods as empty/throwing stubs, or whose clients depend on many unused methods.
2. Identify the **clients**: who calls which subset of methods? (Often each client has a *role*.)
3. Split the interface **along role/client lines**: `PaymentProcessor` → `Charger` (`charge()`), `Refunder` (`refund()`), `FraudChecker` (`verify()`).
4. Implementers implement only what they support; clients depend only on the role they need.
5. Clients compose: a client that needs two roles depends on two narrow interfaces (and gets an object implementing both).
The test: **every client's dependency set equals exactly the methods it calls** — no stubs, no unused recompiles, no forced coupling.

## 8. Example
```java
// FAT interface — implementers forced to stub what they don't support
interface Worker {
    void work();
    void eat();          // a Robot worker doesn't eat
    void sleep();        // nor sleep
}
class Robot implements Worker {
    public void work() {}
    public void eat() { throw new UnsupportedOperationException(); }  // forced stub
    public void sleep() { throw new UnsupportedOperationException(); }
}
// ISP-fixed: split by role
interface Workable { void work(); }
interface Feedable { void eat(); }
interface Sleepable { void sleep(); }
class Human implements Workable, Feedable, Sleepable {                    // implements all three
    public void work() {}
    public void eat() {}
    public void sleep() {}
}
class Robot2 implements Workable {                                        // implements only its role
    public void work() {}
}
```
Now `Human` (full roles) and `Robot` (work only) each implement *exactly* their role; nothing is stubbed; a scheduling system that only needs `Workable` depends only on `work()`.

## 3. When Is It Used?
- **Fat interface smells**: implementers with `throw new UnsupportedOperationException()` stubs, or `implements ... { }` empty bodies.
- **Multiple roles in one contract**: an entity that is *paid, evaluated, and trained* → three role interfaces.
- **Dependency surface reduction**: a client that only calls 2 of 10 methods should depend on a 2-method interface.
- **Interface versioning**: instead of adding a method to a stable interface (breaking implementers), add a *new* narrow interface.
- **Not for**: tiny interfaces with real cohesion — splitting a 3-method cohesive interface into 1-method interfaces is over-segregation (the opposite smell).

## 4. Why Wasn't Another Approach Chosen?
- *Why not one big interface + default methods?* Default methods reduce *implementer* burden but not *client* coupling — a client depending on the fat interface still recompiles/retests on any of its changes; stubs are avoided but the dependency surface stays fat.
- *Why not just throw exceptions in unused methods?* That's the symptom ISP eliminates: throwing `UnsupportedOperationException` is a *runtime* LSP violation (the implementer can't honor the contract) that compile-time interface segregation prevents.
- *Why not inheritance (base class) for roles?* Multiple-inheritance limits (Java) make interfaces the right role mechanism; a class can implement many interfaces but extend only one class — interfaces are *designed* for role composition.
- *Why not one interface per method?* Over-segregation: each role gets fragmented into single-method interfaces, and clients must depend on five interfaces where one cohesive 3-method role interface suffices. ISP targets *role cohesion*, not atomicity.
- *Why not ad-hoc/duck typing (Python/Go style)?* Structural typing sidesteps interface segregation (types are defined by what you call, not what you declare) — ISP's *goal* (small dependency surfaces) is achieved automatically; but explicit Java/C# interfaces also give you *compile-time* documentation and DI seams.

## 5. Intuition
A **restaurant menu split by role** vs one giant menu. A giant menu (fat interface) forces the kitchen to prepare everything and forces diners to scan irrelevant sections. Split it: a "beverage menu" for the bartender (only drinks), a "dessert menu" for the pastry chef (only sweets), a "specials board" for the host. The bartender depends only on drinks; the pastry chef only on desserts; each *role* owns its contract. Same kitchen (object), multiple menus (interfaces) — and changing the dessert list never touches the bartender's workflow.

## 6. Real-World Analogy
A **bank card with role-based permissions**. One card with *all* capabilities (withdraw, transfer, bill-pay, invest, credit) forces every ATM and merchant to interface with everything — and a merchant that only accepts payments is coupled to withdrawal and investing features it never uses. Segregate by role: a "debit card" (withdraw/pay), a "credit card" (pay/credit), an "investment card" (invest). The payment terminal depends on *just* the pay capability; the ATM on *just* withdrawal. Same physical card can implement multiple roles (chip = multiple interfaces), but each terminal's dependency is exactly what it needs — changes to investing never ripple into the payment flow.

## 7. Formal Definition
**Interface Segregation Principle** (Robert C. Martin): "Clients should not be forced to depend upon interfaces they do not use." An interface should contain only the operations *cohesive to a single client role*; when an interface has methods used by different clients, it should be split so each client depends only on the subset it uses. Formally: for every client C and interface I it depends on, every method of I must be *used by* C (or at least be part of C's role). This minimizes the *dependency surface*: a change to a method not used by C cannot force changes to C. Implementers implement exactly the roles they support (no stubs, no `UnsupportedOperationException`), and multiple narrow interfaces compose (a class may implement several).

## 9. Internal Working
1. **Detect**: grep for `UnsupportedOperationException` in implementers, empty overrides, or a client that receives a fat interface but calls 2 methods. Also: recompile storms — "I changed `Worker` and 40 classes broke, but only 6 use the new method."
2. **Cluster**: group the interface's methods by *client role* (who calls what). Each cluster becomes a candidate interface.
3. **Split & rename**: extract role interfaces; the fat interface either disappears or becomes a *composed* interface (marker) if clients truly need the union.
4. **Rebind clients**: each client's field/parameter type narrows to the role interface it needs; DI wires the concrete (multi-role) object.
5. **Verify**: no implementer has a stub; no client depends on unused methods; tests still pass — and now a role's change touches only that role's clients.
6. **Watch the opposite smell**: if splitting leaves 1-method interfaces everywhere, merge back to cohesive roles — ISP is about *role cohesion*, not atomicity.

## 10. Time Complexity
- Zero runtime cost — interfaces are compile-time contracts; the concrete dispatch is the same O(1) vtable call (Part 04).
- *Maintenance* saving: narrower dependency surfaces → smaller recompile/test blast radius; a change to a role interface recompiles only its clients.
- Space: no change (interfaces carry no instance data).

## 11. Advantages
- **Minimal coupling**: each client depends only on what it calls — fewer forced changes.
- **No stubs**: implementers never throw `UnsupportedOperationException` or leave empty bodies.
- **Cohesive roles**: interfaces read as a role contract, self-documenting.
- **Reusable objects**: one object implements multiple roles; consumers pick the role they need (same object, different views).
- **LSP-friendly**: narrow contracts are easier to honor — fewer methods to guarantee.
- **Evolution**: add a *new* role interface instead of breaking a stable one (OCP-friendly).

## 12. Disadvantages
- **Interface proliferation**: many small interfaces add files and cognitive overhead.
- **Role-boundary judgment**: splitting along the "wrong" role line creates overlapping interfaces (methods in two roles) or orphan methods.
- **Over-segregation**: fragmenting cohesive roles into single-method interfaces makes clients depend on many interfaces and bloats DI wiring.
- **Loss of a shared "type"**: clients that legitimately need *any* `Worker` (work+eat+sleep) must depend on three interfaces — a "union" need has no single type (can be recovered via a composed interface).
- **Renaming churn**: good role naming is hard; bad names mislead readers more than a fat interface would.

## 13. Interview Questions
1. **Q: What is ISP?** A: No client should be forced to depend on methods it doesn't use. Fat interfaces should be split into narrow, role-specific interfaces so each client depends only on the methods it calls.
2. **Q: What's the classic example?** A: The JDK's `java.awt.event` package — `MouseListener`, `KeyListener`, `ActionListener`, etc. A button implements `ActionListener` (one method) instead of one giant `EventListener` with a dozen handlers. Also the `Worker`/`Robot` (eat/sleep/work) example.
3. **Q: TRICKY — What's the difference between ISP and SRP?** A: SRP applies to *classes* (one reason to change); ISP applies to *interfaces* (one role per client). They're the same value at different levels — a class with one responsibility should also expose role-narrow interfaces. A class can satisfy SRP yet still force fat interfaces on clients (an ISP violation).
4. **Q: SCENARIO — `Printer` interface with `print()`, `scan()`, `fax()`, and a cheap printer that can't fax. Fix.** A: Split into `Print`, `Scan`, `Fax` interfaces; the cheap printer implements `Print` only; the multifunction implements all three; clients depend on the role they need. No forced `fax()` stubs.
5. **Q: PRODUCTION — "I have 40 implementers of `Handler` with many empty bodies." Fix?** A: The interface is fat — group methods by role, split, and have each implementer implement only the roles it genuinely supports. Empty bodies are the ISP smell; you're paying for methods you never deliver.
6. **Q: Doesn't Java's default methods solve this?** A: They reduce *implementer* burden (no stubs) but not *client coupling* — clients still depend on the full fat interface and recompile on its changes. Defaults are a compatibility tool, not an ISP replacement.
7. **Q: TRICKY — Is a 1-method interface always good ISP?** A: No — over-segregation is a real smell. A cohesive role (e.g., a `Comparable.compareTo` or `Runnable.run` is fine as 1 method, but `Chargeable.charge+verify` shouldn't be split just because two methods exist). ISP wants *role* size, not *minimum* size.
8. **Q: How does ISP relate to OCP?** A: A narrow interface is *easier to keep closed* — adding a behavior becomes adding a new role interface, not editing a fat one all implementers depend on. ISP lowers the cost of extension; OCP is the goal.
9. **Q: SCENARIO — A client needs only `isValid()` from a 12-method `Validator`. What's the correct dependency?** A: A role interface `ValidityCheck { boolean isValid(); }`; the client depends on that, not the fat `Validator`. The concrete validator implements both interfaces; the client never sees the 11 methods it doesn't use.
10. **Q: PRODUCTION — DI and ISP: how do they combine?** A: DI lets the client declare its dependency as the *narrow* role interface and receive the concrete multi-role object — the wire type is the role, the runtime object is the full implementation. That's ISP + DIP working together.
11. **Q: TRICKY — Can a fat interface be OK if all clients genuinely use all methods?** A: Yes — ISP is *client-driven*; if every client truly needs every method (a truly cohesive contract), the "fat" interface isn't fat, it's complete. The smell is specifically *unused* dependency.
12. **Q: How does Go/Python handle this?** A: Structural typing: interfaces are implicit (a type satisfies an interface by *having the methods*), so a client that needs `IsValid()` depends on a 1-method interface the compiler infers — ISP's goal achieved automatically with no declaration effort. Java/C# need explicit (sometimes verbose) role interfaces.
13. **Q: What does "role interface" mean?** A: An interface shaped by a *client's role* rather than by an *object's full identity* — `Workable`, `Feedable`, `Sleepable` describe what a client can *do with* the object, not what the object *is*.
14. **Q: PRODUCTION — You inherit a codebase full of fat interfaces. Refactor plan?** A: (1) Find implementers with stubs/empty bodies — those are the fat spots; (2) cluster methods by client role; (3) extract role interfaces, repoint clients to them, wire via DI; (4) delete the fat interface (or keep it as a composed marker if a union client truly needs it); (5) run contract tests per role.

## 14. Follow-Up Questions
1. **Q: How does ISP relate to the "Interface" in Java 8+ default methods?** A: Defaults let you *add* to an interface without breaking implementers (a compatibility/OCP tool). ISP is about *shaping* the interface for clients; the two are orthogonal — use defaults for evolution, segregation for role clarity.
2. **Q: Is a marker interface (empty) a violation?** A: No — a marker (like `Serializable`) deliberately has no methods, so no client depends on unused methods; it's a *type* tag, not a fat contract. If markers accumulate behavior, they become fat and should be split.
3. **Q: How do "adapter" and "facade" patterns relate to ISP?** A: The Adapter lets an object expose a *narrower* interface to a client (ISP-friendly — the client sees only what it needs); Facade exposes a *subset* of a subsystem — both are ISP in disguise (client-facing surfaces sized to the client's role).
4. **Q: Can ISP lead to interfaces with a single client?** A: Yes, and that's fine and common — a role interface may serve exactly one client type (the client's own "what I need" contract). ISP cares about *dependency surface*, not client count.

## 15. Coding Example
```java
import java.util.*;
// Roles (ISP): one interface per client role
interface Chargeable { void charge(double amount); }
interface Refundable { void refund(double amount); }
interface Trackable  { String transactionId(); }

// Concrete object implements ALL roles it supports
class CardPayment implements Chargeable, Refundable, Trackable {
    private final String id = UUID.randomUUID().toString();
    public void charge(double amount) { print("charged " + amount); }
    public void refund(double amount) { print("refunded " + amount); }
    public String transactionId() { return id; }
}

// Clients depend ONLY on their role
class Checkout {
    void pay(Chargeable c, double amt) { c.charge(amt); }        // never sees refund/track
}
class Dispute {
    void reverse(Refundable r, double amt) { r.refund(amt); }    // never sees charge
}
class Receipt {
    void show(Trackable t) { print("txn " + t.transactionId()); }
}
public class Main {
    public static void main(String[] args) {
        CardPayment p = new CardPayment();
        new Checkout().pay(p, 50.0);      // passes the SAME object as three role types
        new Dispute().reverse(p, 10.0);
        new Receipt().show(p);
    }
}
```
One object, three roles; each client's dependency surface is exactly its method set. Adding a `Settleable` role later = new interface + new implementers; no existing client or interface changes (OCP + ISP).

## 16. Industry Usage
- **JDK**: `java.awt.event.*` (split listeners — the canonical ISP lesson); `java.util.concurrent` — `Runnable`, `Callable`, `Executor`, `Future` are role interfaces; `java.io` — `Closeable`/`Flushable` separated from readers/writers.
- **Spring**: `InitializingBean`, `DisposableBean`, `ApplicationContextAware` — tiny role callbacks a bean implements only if it needs them (no forced lifecycle interface).
- **Go**: implicit interfaces make ISP automatic — `io.Reader`, `io.Writer`, `io.Closer` are separate, and a type satisfies any subset.
- **REST clients / SDKs**: role-shaped interfaces per capability (auth, billing, analytics) so integrations depend only on what they use.
- **Event systems**: per-event listener interfaces (like the AWT split) keep subscribers from implementing unused handlers.

## 17. References
- Robert C. Martin, *Clean Architecture*, Ch. 9 — ISP chapter.
- Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices* — ISP original treatment.
- Oracle Java AWT events tutorial (the split-listener example): https://docs.oracle.com/javase/tutorial/uiswing/events/
- GeeksForGeeks, "Interface Segregation Principle in Java": https://www.geeksforgeeks.org/interface-segregation-principle/
- Effective Java (Bloch), Item 20 — "Prefer interfaces to abstract classes" (role interfaces).

## 18. Cheat Sheet
- ISP: don't force clients to depend on unused methods.
- Split interfaces by *client role*, not object identity.
- Smell: `UnsupportedOperationException` stubs / empty bodies.
- Default methods ≠ ISP (they help implementers, not clients).
- Over-segregation is a smell too — cohesive roles > tiny ones.
- One object, many role interfaces (composition).
- DI wires clients to narrow role types.
- JDK example: `java.awt.event` split listeners.
- Go/Python get this free via structural typing.
- ISP + SRP: same value at interface vs class level.

## 19. Quiz
1. ISP means clients: a) must use all methods b) depend only on methods they use c) must implement all d) avoid interfaces → **b**
2. A `UnsupportedOperationException` stub signals: a) good design b) fat interface c) performance d) thread safety → **b**
3. `java.awt.event` is the classic: a) SRP b) ISP c) OCP d) DIP example → **b**
4. Default methods: a) solve ISP fully b) help implementers only c) violate LSP d) replace interfaces → **b**
5. ISP is best applied by splitting on: a) method count b) client role c) class size d) package → **b**
6. True or False: 1-method interfaces are always the best ISP. → **False** (over-segregation)

## 20. Flashcards
- **Q: ISP definition?** → **A:** No client forced to depend on methods it doesn't use.
- **Q: Smell?** → **A:** Empty/stub implementations of interface methods.
- **Q: Split along what?** → **A:** Client roles.
- **Q: Default methods fix ISP?** → **A:** No — they help implementers, not client coupling.
- **Q: JDK example?** → **A:** `java.awt.event` split listeners.
- **Q: Over-segregation?** → **A:** Fragmented 1-method interfaces — merge cohesive roles.

## 21. Revision
ISP: no client should depend on methods it doesn't use — split fat interfaces along *client-role* lines so each client's dependency surface is exactly what it calls. Smells: `UnsupportedOperationException` stubs and empty bodies. Default methods reduce implementer burden but not client coupling (they don't fix ISP). One object implements many role interfaces; DI wires clients to narrow role types. JDK canonical case: `java.awt.event`'s split listeners; Go/Python get ISP automatically via structural typing. Avoid the opposite smell (over-segregation into 1-method interfaces) — segregate by role cohesion, not atomicity. First-30-seconds answer: "Split interfaces by client role so no client depends on methods it never calls — stubs and UnsupportedOperationException are the smell."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is ISP?" | Interview Q1 / Section 2, 7 |
| "Classic example?" | Interview Q2 / Section 16 |
| "ISP vs SRP?" | Interview Q3 / Section 4 |
| "Fix the Printer/cheap-printer" | Interview Q4 / Section 8 |
| "Do default methods fix it?" | Interview Q6 / Section 4 |
| "1-method interface always good?" | Interview Q7 / Section 12 |
| "ISP + OCP relation?" | Interview Q8 |
| "ISP + DI combo?" | Interview Q10 / Section 16 |
