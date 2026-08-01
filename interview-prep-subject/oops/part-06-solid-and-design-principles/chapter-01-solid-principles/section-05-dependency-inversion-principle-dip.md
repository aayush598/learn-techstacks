# Dependency Inversion Principle (DIP)

> **TL;DR**: **High-level modules should not depend on low-level modules; both should depend on abstractions.** Abstractions should not depend on details; details should depend on abstractions. DIP inverts the dependency arrow so the *policy* (high-level) owns the contract, not the *mechanism* (low-level) — and it's a design principle, distinct from Dependency Injection (the wiring technique that implements it).

## 1. Why Does This Exist?
In a naive layered design, the high-level business logic depends on the low-level details: `OrderService` calls `MysqlOrderRepository`, which calls `JdbcDriver`. Every change to the DB driver or schema ripples into `OrderService`; testing `OrderService` requires a running MySQL; swapping to Postgres means editing business code. DIP exists to **invert that arrow**: `OrderService` depends on an *abstraction* (`OrderRepository` interface) that *it owns*, and `MysqlOrderRepository` (a detail) depends on that same abstraction. Now the policy (what the app *does*) doesn't know the mechanism (how it's *stored*); the mechanism conforms to the policy. The result: testability (mock the repository), swap-ability (new storage = new implementation), and stability (high-level logic — the expensive, valuable part — doesn't change when the plumbing changes). DIP is the *architectural* principle: it dictates which direction arrows point in your dependency graph, and it's the one that makes the other SOLID principles real in large systems.

## 2. How Does It Work?
1. Identify the **high-level (policy) module** and the **low-level (mechanism) module** — e.g., business logic vs database driver.
2. **Extract the abstraction**: an interface/abstract class that captures what the high level *needs* from the low level (`OrderRepository.save(Order)`) — *owned by the high-level module's language* (domain terms, not SQL).
3. **Invert the arrow**: high-level → interface (depend on abstraction); low-level → interface (implement it). Both point at the abstraction; neither knows the other.
4. **Wire at the composition root**: the concrete low-level implementation is instantiated at the *top* (main/factory/DI container) and passed *down* — high level receives the abstraction, never the concrete.
5. The **dependency direction** in the runtime graph is the opposite of the *dependency ownership* in the source: source arrows point to abstractions; runtime wiring flows from the root.

## 3. When Is It Used?
- **Layered architectures**: service → interface → repository/driver, UI → interface → domain.
- **Testability**: any class you want to mock must depend on an abstraction (DIP enables mocking — that's why TDD pulls interfaces out).
- **Swappable infrastructure**: DB, file system, SMTP, cloud SDK, time, randomness — hide behind interfaces.
- **Plugins/frameworks**: the core defines the contract; external providers implement it (JDBC, SLF4J).
- **Not for**: leaf utilities with no varying implementation (a `StringUtils` doesn't need an interface); or when abstraction would obscure rather than stabilize (premature DIP violates YAGNI).

## 4. Why Wasn't Another Approach Chosen?
- *Why not just let the high level call the concrete low level?* Then the most valuable, most-tested code (business rules) is coupled to the most replaceable code (drivers). Every driver/schema change edits business logic; tests need real infrastructure; the app can't survive infrastructure swaps.
- *Why not invert by making the low-level define the API?* If the repository defined the interface, the business logic would speak *storage vocabulary* (`executeSql`, `resultSet`) — the abstraction would be "owned" by the detail, leaking mechanism into policy. DIP says the *policy* owns the abstraction, so it speaks *domain vocabulary* (`save(Order)`, `findById`).
- *Why interfaces instead of concrete base classes?* Interfaces allow a class to be many abstractions at once and don't force hierarchy; DIP's contract is behavior, and interfaces (Part 02) express behavior cleanly.
- *Why a "composition root" and not `new` inside the high level?* `new` *is* the concrete dependency — instantiating the low level inside the high level re-introduces the coupling DIP removed. The root's job is to build the graph once and inject it (that's where DI enters).
- *Why not just use a service locator / static registry?* Service locators hide dependencies (clients reach into a global), hurting testability and reusability; constructor injection makes the dependency *visible and explicit* — DIP prefers explicitness.

## 5. Intuition
Think of a **manager and a contractor**. The manager (high-level policy) says "I need a report by Friday" — the *what*. The contractor (low-level mechanism) figures out the *how* (which tools, which database). The manager must NOT specify "write it in Excel with a MySQL query" — that's policy depending on mechanism. Instead, both agree on an *abstraction*: "a deliverable by a deadline" (the interface the manager defines: `getReportBy(date)`). The contractor adapts to that contract. The manager can now hire any contractor who honors the contract; the contractor can change tools freely as long as the deliverable arrives. The contract is *owned by the manager* (policy) — that inversion is DIP.

## 6. Real-World Analogy
A **restaurant and its suppliers**. The kitchen (high-level policy) doesn't depend on one farmer (low-level mechanism): it defines a contract — "fresh vegetables, daily, by 7am" (`IngredientSupplier.deliver()`) — and *any* supplier that honors it gets the business. The suppliers (details) depend on the contract; the kitchen depends on the contract; neither depends on the other's specifics. If one farm closes, the kitchen's recipe logic (the valuable part) doesn't change — a new supplier plugs in. The alternative (kitchen hard-wired to Farmer Joe's phone number and van schedule) is the naive coupling DIP eliminates. The contract is owned by the kitchen's needs, not by the farm's capabilities.

## 7. Formal Definition
**Dependency Inversion Principle** (Robert C. Martin): (A) **High-level modules should not depend on low-level modules. Both should depend on abstractions.** (B) **Abstractions should not depend on details. Details should depend on abstractions.** "High-level" = policy/business rules; "low-level" = mechanisms (persistence, I/O, drivers). Inversion means the source-code dependency arrows point *up* toward the abstractions (and the policy), never *down* from policy to mechanism; the runtime flow of control is the opposite direction from the dependency graph. Ownership: the abstraction is defined *in* (or for) the high-level module, in its vocabulary. **Dependency Injection (DI)** is the *mechanical* technique that realizes DIP at runtime — the high level declares its dependency as the abstraction, and an external **composition root** constructs the concrete implementation and passes it in; DI is one way to *implement* DIP, not DIP itself.

## 8. Example
```java
// WITHOUT DIP — high-level depends on low-level (concrete DB)
class MysqlOrderRepo { void saveToMysql(Order o) { /* SQL */ } }         // low-level
class OrderServiceNaive {
    private final MysqlOrderRepo repo = new MysqlOrderRepo();            // ← policy depends on mechanism
    void place(Order o) { repo.saveToMysql(o); }                          // speaks SQL vocabulary
}
// WITH DIP — both depend on an abstraction owned by the high level
interface OrderRepository { void save(Order o); }                        // ← domain vocabulary

class OrderService {
    private final OrderRepository repo;                                  // depends on abstraction
    OrderService(OrderRepository r) { this.repo = r; }                   // injected — DI
    void place(Order o) { repo.save(o); }                                // policy logic, storage-agnostic
}
class MysqlOrderRepository implements OrderRepository {                  // detail depends on abstraction
    public void save(Order o) { /* SQL */ }
}
class PostgresOrderRepository implements OrderRepository { public void save(Order o) { /* SQL */ } }
// Composition root:
public class Main {
    public static void main(String[] args) {
        OrderService svc = new OrderService(new MysqlOrderRepository());  // wire once, here
        svc.place(new Order());
        // switch to Postgres: change ONE line at the root — OrderService untouched
    }
}
```
`OrderService` now depends on `OrderRepository` (policy-owned contract), not on MySQL. Both storage drivers depend on the same abstraction. Swapping DB = one root line.

## 9. Internal Working
1. **Identify the inversion point**: where does the high-level module reference a concrete low-level class? (`OrderService → MysqlOrderRepo`).
2. **Define the abstraction in policy terms**: what does the high level *need*? (`save(Order)`, `find(id)`) — express in domain language, not `executeQuery`.
3. **Point both arrows at the abstraction**: high-level's field/parameter type becomes the interface; the low-level `implements` it.
4. **Move instantiation to the composition root**: `new MysqlOrderRepository()` moves out of the service and into main/factory/DI-container; the service receives it via constructor (or setter) — the dependency is *injected*.
5. **Runtime flow vs source flow**: at runtime, main → creates repo → passes into service (control flows *down*); in source, service → references interface only (dependency flows *up* to abstraction). The inversion is this mirror-image.
6. **Extend**: new low-level (Postgres, mock, in-memory) implements the same abstraction — the high level never changes (OCP through DIP).
7. **Watch the creep**: adding abstractions for every leaf class (a `StringUtils` interface) is over-DIP — invert only where the detail varies or the policy deserves protection.

## 10. Time Complexity
- Zero algorithmic cost — DIP is architectural; the call is the same O(1) interface dispatch (Part 04).
- One indirection layer (interface) added per inverted dependency — negligible, typically devirtualized/inlined.
- The real gains are *engineering* economics: mocked tests run in ms instead of spinning a DB; storage swaps are config changes; recompile blast radius shrinks to the changed implementation.

## 11. Advantages
- **Testability**: mock the abstraction; test business logic without infrastructure.
- **Swap-ability**: new storage/IO/cloud implementation behind the same contract — one root-line change.
- **Stability**: the expensive, valuable policy code doesn't change when mechanisms change.
- **Ownership clarity**: abstractions are defined in domain vocabulary (policy owns the contract).
- **Parallel work**: a team builds the implementation against the agreed contract; consumers code against it too.
- **OCP enablement**: extension by new implementation, not by editing policy.

## 12. Disadvantages
- **Abstraction overhead**: an interface per boundary adds files and indirection.
- **YAGNI risk**: inverting dependencies that never vary adds ceremony with no payoff.
- **DI-container dependency**: teams often couple to Spring/Guice to make inversion ergonomic, which is itself a (managed) dependency.
- **Complexity of wiring**: the composition root can grow large; mistakes surface as "why is this a null?" mysteries.
- **Over-abstraction hides behavior**: chasing every call through interfaces can obscure which concrete code actually runs.

## 13. Interview Questions
1. **Q: What is DIP?** A: High-level modules should not depend on low-level modules — both should depend on abstractions; abstractions should not depend on details, details on abstractions. The policy owns the contract; the mechanism conforms to it.
2. **Q: What is the difference between DIP and DI?** A: DIP is a *design principle* (which direction dependencies point); DI is a *technique* (a class declares its dependency as an abstraction and receives the concrete instance from outside). DI is a common way to *implement* DIP, but they're not the same thing.
3. **Q: TRICKY — Does DIP mean "always depend on interfaces"?** A: No — it means don't depend on *low-level mechanisms*; stable domain classes can be concrete. Invert where the low level varies (DB, SMTP, clock) or where policy deserves protection; a leaf utility with no variation needs no interface.
4. **Q: SCENARIO — `OrderService` calls `new MysqlRepo()` internally. What's wrong, and how to fix?** A: The high-level policy is coupled to the concrete mechanism (storage), so it can't be tested without MySQL and can't swap storage. Fix: extract `OrderRepository` interface (domain terms), depend on it, and inject the concrete repo from a composition root.
5. **Q: PRODUCTION — How does DIP enable mocking?** A: Mocking substitutes a fake for the dependency — possible only if the class depends on an *abstraction* the fake can implement. A class coupled to a concrete `MysqlRepo` can't be mocked without an interface (or bytecode tricks like Mockito). DIP is the precondition for clean test doubles.
6. **Q: What does "abstractions owned by the high level" mean?** A: The interface is expressed in the *policy's vocabulary* (save order, find order), not the mechanism's (execute SQL, open cursor). Ownership = the interface lives in the high-level module's domain language, so the high level defines the contract rather than conforming to the detail's API.
7. **Q: TRICKY — Is the "dependency arrow" pointing up or down?** A: In source code, both high and low point *up* to the abstraction (and the policy); the abstraction never points at the detail. At runtime, control flows *down* from the composition root to the concrete implementation — the mirror image is the "inversion."
8. **Q: SCENARIO — Design a `NotificationService` that can email or SMS.** A: Define `Notifier { void send(String) }` (policy-owned); `EmailNotifier`/`SmsNotifier` implement it; `NotificationService` depends on `Notifier`; the root injects whichever. Email↔SMS swap = root-line change; service and tests never change (this is Strategy pattern + DIP).
9. **Q: PRODUCTION — Your service is littered with `@Autowired` fields. Is that DIP?** A: It's DI *machinery*, which serves DIP, but field injection has costs (hidden deps, no final fields, harder testing). DIP is the *principle*; prefer constructor injection (explicit, testable). Framework annotations are an implementation detail of the DI wiring.
10. **Q: How does DIP relate to OCP?** A: DIP makes OCP *physically achievable*: because policy depends only on abstractions, adding a new implementation (new storage, new notifier) never requires editing policy — extension without modification is exactly what the inverted arrow permits.
11. **Q: TRICKY — Can a system follow DIP and still have bad architecture?** A: Yes — DIP is about *direction*, not *quality*: you can invert dependencies into over-engineered abstractions, or place the abstraction in the wrong vocabulary (leaking SQL into `OrderRepository`). DIP done badly = abstraction ceremony without policy protection.
12. **Q: What is the "composition root"?** A: The single place near the top of the app where the object graph is *composed* — `main()`/`Application`/a DI container's wiring — the only place concrete implementations are chosen. It's the counterpart of DIP: policy depends on abstractions everywhere except here, where the concrete graph is assembled.
13. **Q: SCENARIO — Framework callbacks (Servlet, Android `onCreate`) already call your code — is DIP violated?** A: No — that's Inversion of Control (the framework owns the loop, your code plugs in). DIP concerns *your* module graph: does your `OrderService` depend on `OrderRepository`'s abstraction or on MySQL's concrete class? Framework-vs-you is IoC; class-vs-class is DIP.
14. **Q: PRODUCTION — When should you NOT invert?** A: When the low level is (a) stable and never varies (a JDK API), (b) a leaf utility with no policy interest, or (c) not worth the abstraction tax because the variation is fiction. Invert at real boundaries: persistence, I/O, messaging, time, external SDKs, randomness — where testing and swapping genuinely matter.

## 14. Follow-Up Questions
1. **Q: What's the relationship between DIP, the Clean Architecture dependency rule, and the onion/hexagonal models?** A: They're the same principle at different scales: Clean Architecture's "dependency rule" (source dependencies point inward) is DIP applied to whole layers; hexagonal architecture's "ports and adapters" are DIP's abstractions (ports) and implementations (adapters). DIP is the seed of every layered-architecture rule.
2. **Q: How does DIP apply to the "service/repository" layering in Spring?** A: `@Service` depends on `@Repository` *interfaces* (not `JdbcTemplate`-tied impls); Spring injects the concrete impl at runtime — the classic DIP + DI composition. The repository interface is defined in domain vocabulary; the impl (JDBC/JPA/mongo) conforms to it.
3. **Q: Does DIP forbid depending on the JDK or frameworks?** A: No — DIP targets *your* high vs low level; a JDK API is typically a stable abstraction itself (you depend on `List`, not on `ArrayList`'s implementation specifics). "Depends on abstractions" includes depending on the JDK's own abstractions.
4. **Q: Is DIP the same as "program to an interface, not an implementation"?** A: Closely related but DIP is stronger and directional: the interface mantra says "depend on interfaces"; DIP adds *who owns* the interface (the policy) and *which direction* the arrow points (both modules point up). The mantra is the rule of thumb; DIP is the architecture.

## 15. Coding Example
```java
import java.util.*;
// Low-level mechanism: time (testability nightmare if policy depends on it concretely)
interface Clock { long now(); }
class SystemClock implements Clock { public long now() { return System.currentTimeMillis(); } }

// High-level policy: coupon logic — must not know what time source it uses
class CouponService {
    private final Clock clock;                              // abstraction, injected (DI)
    CouponService(Clock c) { this.clock = c; }
    boolean isExpired(Coupon coupon) { return coupon.expiresAt() < clock.now(); }
}
// Composition root — the ONLY place the concrete clock is chosen
public class Main {
    public static void main(String[] args) {
        CouponService prod = new CouponService(new SystemClock());        // production
        CouponService test = new CouponService(() -> 1_000_000L);          // test: fixed time
        System.out.println(prod.isExpired(new Coupon(2_000_000L)));       // false
        System.out.println(test.isExpired(new Coupon(500_000L)));         // true — deterministic test!
    }
}
```
`CouponService` (policy) depends only on `Clock` (abstraction it defines); `SystemClock` (detail) depends on `Clock`. The test passes a fixed-time fake — deterministic tests without touching production code. That's DIP in 15 lines.

## 16. Industry Usage
- **Spring/Guice**: DI containers are the industrial DIP implementation — beans declared as interfaces, concrete impls bound in the container's root config.
- **JDBC**: the app depends on `java.sql.Driver` (abstraction); each DB vendor ships a driver implementing it — swap MySQL→Postgres by changing the driver JAR, never the app code.
- **SLF4J**: policy depends on the `Logger` interface; binding (logback/log4j) is a provider at the root.
- **Clean Architecture / Hexagonal / Onion**: every layer's dependency rule is DIP; ports (abstractions) in the domain, adapters (details) at the edge.
- **TDD/Testcontainers**: mocks and in-memory fakes work precisely because services depend on abstractions (DIP) and receive doubles via DI.

## 17. References
- Robert C. Martin, *Clean Architecture*, Ch. 5, 11–12 — DIP and the dependency rule.
- Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices* — DIP original.
- Martin Fowler, "Inversion of Control Containers and the Dependency Injection pattern": https://martinfowler.com/articles/injection.html
- GeeksForGeeks, "Dependency Inversion Principle in Java": https://www.geeksforgeeks.org/dependency-inversion-principle-java/
- Effective Java (Bloch), Item 3 (singletons as flexible: prefer dependency injection over hard-wired construction).

## 18. Cheat Sheet
- High-level ≠ depend on low-level; both depend on abstractions.
- Abstractions ≠ depend on details; details depend on abstractions.
- The abstraction is *policy-owned*, in domain vocabulary.
- DIP = principle (arrow direction); DI = technique (wiring).
- Composition root: only place concrete impls are chosen.
- Runtime flow and source dependency are mirror images.
- Enables: mocking, swap-ability, OCP, layered architecture.
- Invert at real boundaries (DB, IO, time, SDKs) — not every class.
- `new` inside policy = DIP violation; inject instead.
- DIP is the seed of Clean Architecture's dependency rule.

## 19. Quiz
1. DIP says high-level modules depend on: a) low-level modules b) abstractions c) nothing d) the database → **b**
2. DI is: a) a principle b) a wiring technique c) a language feature d) a pattern → **b**
3. Who owns the abstraction? a) the low level b) the policy c) the framework d) nobody → **b**
4. The composition root: a) builds concrete impls once b) creates `new` everywhere c) a DB d) a class → **a**
5. DIP enables: a) mocking b) memory leaks c) circular deps d) deadlock → **a**
6. True or False: `new` inside a service is usually a DIP violation. → **True**

## 20. Flashcards
- **Q: DIP definition?** → **A:** High and low both depend on abstractions; details conform to policy-owned contracts.
- **Q: DIP vs DI?** → **A:** Principle vs technique — DI implements DIP.
- **Q: Who owns the abstraction?** → **A:** The high-level/policy, in domain vocabulary.
- **Q: Composition root?** → **A:** Single place near the top that builds the concrete graph.
- **Q: DIP enables?** → **A:** Mocking, swapping, OCP, layered architecture.

## 21. Revision
DIP: high-level modules must not depend on low-level modules — both depend on abstractions, and the abstractions are *policy-owned* (domain vocabulary), with details conforming to them. DI (Dependency Injection) is the wiring *technique* that realizes it: classes declare abstractions, a composition root builds the concrete graph and injects it; `new` inside policy is the violation. The inversion: source arrows point up to abstractions, runtime control flows down from the root. DIP enables mocking, infrastructure swapping, and OCP, and is the seed of Clean Architecture's dependency rule. Invert at real boundaries (persistence, IO, time, SDKs) — not every leaf class (YAGNI). First-30-seconds answer: "Policy owns the contract; mechanisms conform to it — both depend on abstractions, and DI wires the concrete implementations at the composition root."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is DIP?" | Interview Q1 / Section 2, 7 |
| "DIP vs DI?" | Interview Q2 / Section 4 |
| "Always depend on interfaces?" | Interview Q3 / Section 12 |
| "Fix the `new MysqlRepo()` service" | Interview Q4 / Section 8 |
| "How does DIP enable mocking?" | Interview Q5 / Section 9 |
| "Who owns the abstraction?" | Interview Q6 / Section 7 |
| "Composition root?" | Interview Q12 / Section 9 |
| "When NOT to invert?" | Interview Q14 / Section 12 |
