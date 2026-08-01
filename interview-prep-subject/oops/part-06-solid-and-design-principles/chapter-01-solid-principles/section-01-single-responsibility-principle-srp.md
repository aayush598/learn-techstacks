# Single Responsibility Principle (SRP)

> **TL;DR**: A class should have **one reason to change** — one actor/one responsibility that owns it. SRP is about *reasons to change*, not line count; when two features would both modify the same class for different stakeholders, split the class.

## 1. Why Does This Exist?
Every change to a class is a *risk*: it can break every other thing that class does, and it needs retesting of all consumers. When a class has multiple responsibilities, the change pressures compound — bug fix for the tax logic while the email formatting is mid-refactor, two teams editing the same file, one feature's bug breaking another's behavior. SRP exists to **isolate change**: if each class has exactly one reason to change, then a requirement change touches exactly one class, its tests, and nothing else. Robert Martin's framing is deliberately sharp: "a class should have one, and only one, *reason to change*." A "reason to change" is an *actor* — a stakeholder or feature area. When the same class answers to two actors, their changes collide. SRP is the anti-collision principle, and it's the most-violated principle in real codebases (the "God class" is its canonical failure).

## 2. How Does It Work?
1. List what a class currently does — its responsibilities.
2. For each responsibility, ask: **"who asks for changes to this? what feature area owns it?"** (the actor).
3. If two responsibilities have *different* actors/change triggers, they're different responsibilities.
4. Split: each responsibility becomes its own class; the original class becomes a thin coordinator or disappears.
5. Respect dependency direction: the split classes should not cross-purpose-call each other except through narrow interfaces.

Test of SRP health: "If requirement X changes, which classes change?" — answer should be a small, predictable set. A class "with one reason to change" changes only when *its* requirement changes.

## 3. When Is It Used?
- **God class detected**: a `EmployeeService` doing persistence + validation + email + reporting → split into `EmployeeRepository`, `EmployeeValidator`, `EmployeeNotifier`, `EmployeeReport`.
- **Change collision**: a class modified by two teams/features (finance + HR edits in the same class) → split by actor.
- **Testing pain**: a class needing many mocks because it touches too many collaborators → splitting removes the unrelated deps.
- **Every new class you write**: one responsibility per class; refactor toward it as the class grows.
- **Not for trivial helpers**: a 3-line utility doesn't need decomposition — SRP is for units with real change pressure.

## 4. Why Wasn't Another Approach Chosen?
- *Why not just have fewer, bigger classes?* Fewer classes = fewer files but more *coupling* between change areas; every change risks every feature. SRP trades a few extra classes for isolated blast radius.
- *Why "reason to change" rather than "does one thing"?* "Does one thing" is ambiguous (any method does *something*); "reason to change" is operational — it ties design to the *actors* who drive changes. `printReport()` and `saveToDB()` both "do one thing" but answer to different actors.
- *Why not split by method granularity (everything tiny)?* Over-splitting creates class explosion, indirection, and noise. SRP is about *change isolation*, not minimal classes — balance with YAGNI (Part 06 ch-02).
- *Why classes rather than modules/functions?* The principle applies at every level; at class level it's most visible in OO design interviews and most frequently violated in production.

## 5. Intuition
A class is a **person with one job description**. A "Doctor" who also does surgery, runs the pharmacy, handles billing, and manages the hospital's legal affairs — any change to hospital policy touches the same person; if billing changes, the surgeon's schedule is disturbed. Real hospitals split roles: the surgeon operates, the pharmacist dispenses, the accountant bills. Same for code: give each class *one* job description so a change to "billing" touches the accountant (billing class), not the surgeon (medical logic). You can still *coordinate* all of them (the "hospital coordinator" = a thin facade), but each does one thing.

## 6. Real-World Analogy
A **restaurant's head chef who also does the books**. When the menu changes (food responsibility), the chef updates dishes; when payroll changes (finance responsibility), the chef also edits spreadsheets; a menu change accidentally breaks payroll, and the accountant can't work because the chef is busy cooking. The fix: hire an accountant (split responsibilities). Now menu changes touch only the kitchen; payroll changes touch only the accountant. Same money, same restaurant, but each person (class) has *one reason to change* — and the two change streams never collide.

## 7. Formal Definition
**Single Responsibility Principle**: a class (or module) should have **one, and only one, reason to change** — that is, one responsibility, where "responsibility" is defined as "a reason for the class to change" (Robert C. Martin). A responsibility corresponds to one *actor*: a stakeholder or cohesive feature area that requests modifications. If two different actors or feature areas can cause changes to the same class, the class has multiple responsibilities and should be split so each responsibility lives in its own class. Formally, the set of change triggers for a class should be cohesive — changes requested for reason A must not modify behavior that exists for reason B.

## 8. Example
```java
// VIOLATION: one class, three reasons to change (tax rules, DB schema, email format)
class EmployeeService {
    void addEmployee(Employee e) {
        double tax = e.salary() * 0.2;        // 1) TAX logic — changes with tax law
        validate(e);                            // 2) VALIDATION — changes with business rules
        save(e);                                // 3) PERSISTENCE — changes with DB schema
        email(e, "Welcome " + e.name());        // 4) EMAIL — changes with marketing
    }
}
// FIX: one class per responsibility
class TaxCalculator { double tax(Employee e) { return e.salary() * 0.2; } }
class EmployeeValidator { void validate(Employee e) { /* business rules */ } }
class EmployeeRepository { void save(Employee e) { /* SQL */ } }
class EmployeeNotifier { void welcome(Employee e) { /* email template */ } }
class EmployeeService {                       // thin coordinator
    EmployeeService(TaxCalculator tax, EmployeeValidator v, EmployeeRepository r, EmployeeNotifier n) {}
}
```
Now a tax-law change touches `TaxCalculator` only; an email-template change touches `EmployeeNotifier` only. Four actors, four classes, zero collisions.

## 9. Internal Working
1. **Detect**: grep for classes with methods spanning feature areas, fields from unrelated domains, or test files with many unrelated mock types.
2. **Classify**: map each method/field to its actor (finance, HR, reporting, UI, persistence).
3. **Extract**: pull each actor's behavior into its own class; move the state it needs; wire the split through the coordinator.
4. **Decouple**: ensure split classes don't reach into each other's internals — they communicate through narrow interfaces (ISP, Part 06) and dependency injection (DIP).
5. **Verify**: after a change, re-run — only the changed class's tests should be affected; the coordinator stays stable.
6. **Watch the smell return**: classes tend to drift back toward god-class as features pile on; SRP is a continuous discipline, not a one-time refactor.

## 10. Time Complexity
- No direct runtime cost — SRP is about code *structure*, not algorithm speed.
- Indirect gains: smaller classes = better cache locality for hot paths, faster compiles (less recompilation per change), smaller test matrices (fewer cases per class).
- Design-time cost: more classes to create/name, more wiring — a modest up-front cost repaid by isolated change.

## 11. Advantages
- **Isolated blast radius**: a change breaks only one class's consumers.
- **Parallel development**: two teams edit different classes, no merge conflicts.
- **Testability**: one collaborator set per class → fewer mocks, clearer tests.
- **Understandability**: a 50-line class is easier to read than a 500-line god class.
- **Reusability**: the extracted responsibility is reusable elsewhere (reuse the `TaxCalculator` in another flow).

## 12. Disadvantages
- **Class explosion**: over-application creates a dozen trivial classes for a two-method concept.
- **Indirection**: callers must compose multiple objects; logic is spread across files.
- **Coordinator ceremony**: thin "service" classes that just delegate can become noise.
- **Premature application**: splitting before change pressure exists violates YAGNI — a stable god class never needs splitting.
- **Judgment required**: boundaries between "same responsibility" and "different" are genuinely subjective; wrong splits fragment cohesion.

## 13. Interview Questions
1. **Q: What is SRP?** A: A class should have one and only one *reason to change* — one responsibility, owned by one actor. When two different stakeholders' changes would both modify the same class, split it.
2. **Q: Is SRP about a class being small?** A: Not primarily — it's about *cohesion of change triggers*. A large but single-purpose class (e.g., a complex parser) satisfies SRP; a small class doing validation + persistence violates it.
3. **Q: TRICKY — A `UserService` handles login, profile updates, and sending verification emails. Violation?** A: Likely yes — three change triggers (auth rules, profile rules, email templates). Split into `AuthService`, `ProfileService`, `EmailNotifier`. But if "verification email" is part of auth's behavior for one actor, it can stay — SRP is actor-driven, not feature-count-driven.
4. **Q: How do you detect a violation?** A: (a) a class with fields/methods from unrelated domains, (b) a test that mocks many unrelated collaborators, (c) merge conflicts on the same file from different features, (d) "when I change X, why did Y's test break?" — the symptom of two responsibilities coupled.
5. **Q: SCENARIO — An `Order` class has `total()`, `toJson()`, and `sendConfirmation()`. Fix it.** A: Keep `total()` (domain). Extract `OrderSerializer` for `toJson()` (persistence/transport concern) and `OrderNotifier` for email (notification concern). The `Order` changes only when order *business rules* change.
6. **Q: PRODUCTION — Why do "service" classes in Spring become god classes?** A: Services are the convenient catch-all — teams append "and one more method" to `CustomerService` because it's already injected everywhere. SRP discipline says: when the service spans two actors, extract a new service (e.g., `CustomerBillingService`).
7. **Q: What is a "reason to change"?** A: An actor — a stakeholder or feature area that requests modifications. "The finance department wants a new tax rule" is a reason; "HR wants new validation" is a different reason. Two reasons in one class = violation.
8. **Q: TRICKY — Should `toString()` and `hashCode()` violations worry you?** A: No — those are *contract* methods mandated by `Object` (Part 04 ch-01), shared across all classes; they don't create a second change trigger for the class's own domain actor. Don't over-apply SRP to `Object` methods.
9. **Q: SCENARIO — Where does SRP apply to a *function*?** A: Same idea at method level: a method should have one reason to change — but the *named* discipline is for classes; methods get the same treatment via "one level of abstraction per method" and extraction.
10. **Q: PRODUCTION — What's the trade-off when you split classes?** A: More classes = more indirection and wiring, better isolation. The right split balances YAGNI (don't split prematurely) with change frequency (split where change is real). The unit that changes often is the unit that deserves SRP.
11. **Q: How does SRP relate to "high cohesion"?** A: They're the same underlying value: SRP is the *external* statement (one reason to change), cohesion is the *internal* property (elements belong together). Splitting for SRP raises each piece's cohesion (Part 06 ch-02).
12. **Q: TRICKY — A class that validates, saves, and emails *for the same actor* — OK?** A: If a single stakeholder's requirement change genuinely drives all three together (e.g., "onboarding" owns validate+save+welcome-email), it can be one responsibility. The test is *who requests the change*, not *how many operations*.
13. **Q: How do you refactor toward SRP without breaking the callers?** A: Extract responsibilities into new classes, inject them into the original (or a coordinator), keep the public API stable, then delete the moved logic. The original becomes a facade until callers migrate.
14. **Q: PRODUCTION — SRP vs microservices?** A: Same principle at a higher level — one service per business capability (each with one reason to change); SRP at class level is the local form. Applying SRP well in classes is prerequisite to sane service boundaries.

## 14. Follow-Up Questions
1. **Q: How does SRP interact with OCP?** A: SRP makes classes narrow (one reason to change); OCP then extends behavior *without modifying* — SRP sets up the seam, OCP uses it. A god class can't be "closed for modification" because every feature needs to touch it.
2. **Q: What is the relationship to the Interface Segregation Principle?** A: ISP is SRP applied to *interfaces*: don't make one interface serve many clients' reasons to change — split the interface per client, mirroring the class split.
3. **Q: Does SRP apply to packages/modules?** A: Yes — a package should have one responsibility too; cohesive packaging (classes that change together) is the module-level SRP, directly supporting dependency management.
4. **Q: Is a "utility" class with only static methods a violation?** A: No — a cohesive utility (e.g., `StringUtils`) has one reason to change (string helpers); SRP concerns *change triggers*, and utilities have exactly one. But a "Util" namespace full of random statics is a smell.

## 15. Coding Example
```java
// BEFORE: one class, three change triggers
class Invoice {
    double total() { /* sums line items */ }
    void print(Printer p) { /* formatting + layout */ }
    void saveToDb(Connection c) { /* SQL */ }
    void email(Customer c) { /* SMTP */ }
}
// AFTER: one class per responsibility, coordinated by composition
record LineItem(double price, int qty) {}
class Invoice {
    private final List<LineItem> items;
    Invoice(List<LineItem> items) { this.items = items; }
    double total() { return items.stream().mapToDouble(i -> i.price() * i.qty).sum(); }   // business only
}
class InvoicePrinter { void print(Invoice inv, Printer p) { /* layout */ } }             // presentation
class InvoiceRepository { void save(Invoice inv, Connection c) { /* SQL */ } }           // persistence
class InvoiceNotifier { void email(Invoice inv, Customer c) { /* SMTP */ } }             // notification
public class Main {
    public static void main(String[] args) {
        Invoice inv = new Invoice(List.of(new LineItem(10, 2)));
        System.out.println(inv.total());                    // 20.0
        new InvoicePrinter().print(inv, System.out::println);
        new InvoiceRepository().save(inv, null);
        new InvoiceNotifier().email(inv, new Customer());
    }
}
```
Tax change → `Invoice` only; layout change → `InvoicePrinter` only; schema change → `InvoiceRepository` only; template change → `InvoiceNotifier` only. Four actors, four classes, four change triggers — the whole point.

## 16. Industry Usage
- **Spring**: `@Service`, `@Repository`, `@Controller` annotations *enforce* SRP by naming the responsibility — a repository isn't supposed to send emails; teams that respect the layering keep SRP.
- **Clean Architecture (Robert Martin)**: each *layer* has one responsibility (use cases, interface adapters, frameworks) — SRP scaled to architecture, the basis of the onion/hexagonal models.
- **Microservices**: one service per bounded capability — SRP at deployment granularity.
- **DDD (Domain-Driven Design)**: aggregate roots and repositories each own one capability; entities don't do persistence.
- **Every mature codebase**: the "god class refactor" is the #1 structural refactor; most teams have a story of splitting a 2000-line `Manager` class into domain services.

## 17. References
- Robert C. Martin, *Clean Code*, Ch. 8 ("SRP is the most violated principle").
- Robert C. Martin, *Clean Architecture* — SRP at the architecture/layer level.
- Martin Fowler, *Refactoring* — extract-class recipes that implement SRP.
- Agile Software Development: Principles, Patterns, and Practices (Robert Martin) — original SRP definition.
- GeeksForGeeks, "Single Responsibility Principle in Java": https://www.geeksforgeeks.org/single-responsibility-principle-in-java/

## 18. Cheat Sheet
- SRP = one reason to change per class.
- "Reason to change" = an actor/stakeholder.
- Detect: god class, multi-domain fields, many-mock tests, merge collisions.
- Fix: extract class per responsibility; coordinator composes them.
- Not line count — a big single-purpose class is fine.
- Don't over-split; respect YAGNI.
- Applies to methods, packages, services, microservices.
- `Object` contract methods aren't violations.

## 19. Quiz
1. SRP stands for: a) Single Responsibility Principle b) Simple Reusable Process c) Software Review Pattern → **a**
2. A "reason to change" is best defined as: a) any bug b) an actor/stakeholder c) a new feature d) a method → **b**
3. A god class is: a) an SRP success b) an SRP violation c) an interface d) a pattern → **b**
4. A large but single-purpose class: a) violates SRP b) can satisfy SRP c) must be split d) is illegal → **b**
5. Splitting responsibilities raises: a) coupling b) cohesion c) latency d) memory → **b**
6. True or False: SRP is primarily about code size. → **False** (it's about reasons to change)

## 20. Flashcards
- **Q: SRP definition?** → **A:** One reason to change per class — one actor.
- **Q: How to detect a violation?** → **A:** God class, multi-domain fields, unrelated mocks in tests, cross-feature merge conflicts.
- **Q: SRP vs line count?** → **A:** Unrelated — a big single-purpose class can be fine.
- **Q: Refactor technique?** → **A:** Extract class per responsibility, compose via coordinator/DI.
- **Q: "Reason to change" means?** → **A:** A stakeholder or feature area that drives modifications.

## 21. Revision
SRP: a class should have one and only one *reason to change* — a reason being an actor or feature area. It's not about size; it's about *change isolation*. Detect via god classes, unrelated fields, tests mocking many collaborators, or merge conflicts from different features touching one file. Fix by extracting each responsibility into its own class and composing them through a thin coordinator. Applies upward to methods, packages, services, and architecture (Clean Architecture layers). Don't over-split — respect YAGNI and real change pressure. First-30-seconds answer: "One reason to change per class, defined by the actor that requests changes — split when two actors would edit the same class."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is SRP?" | Interview Q1 / Section 2, 7 |
| "Is SRP about size?" | Interview Q2 / Section 4 |
| "How do you detect a violation?" | Interview Q4 / Section 9 |
| "Fix this god class" | Interview Q5 / Section 8 |
| "What is a reason to change?" | Interview Q7 / Section 7 |
| "Why do Spring services become god classes?" | Interview Q6 / Section 16 |
| "Trade-offs of splitting?" | Interview Q10 / Section 12 |
| "SRP vs microservices?" | Interview Q14 / Section 16 |
