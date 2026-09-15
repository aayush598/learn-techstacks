# Loose Coupling, High Cohesion and Encapsulation — 100 Interview Q&A

## Q1: What are coupling and cohesion in software design?

**A:** Coupling is a measure of how much one module depends on another. Low coupling means modules are relatively independent — changes in one module are unlikely to force changes in another. High coupling means modules are tightly interrelated — a change in one often necessitates changes in the other.

Cohesion is a measure of how related the responsibilities of a single module are. High cohesion means a module's elements belong together and serve a single, well-defined purpose. Low cohesion means a module contains unrelated responsibilities that don't naturally belong together.

The design goal is a combination of **low coupling and high cohesion**. High cohesion keeps each module focused on one purpose (so it's easy to understand and change), and low coupling keeps modules independent (so changes don't ripple across the system). These two properties are the foundation of maintainable, testable software.

---

## Q2: Why is low coupling desirable in software systems?

**A:** Low coupling directly reduces the ripple effect of change. When Module A depends on very specific internals of Module B, any modification to B's internals may break A. With low coupling, A depends on a stable, minimal contract, so B can be changed, refactored, or replaced freely.

Low coupling also improves testability. A module with few dependencies can be tested in isolation, often with simple stubs. And it improves reusability — a loosely coupled module can be dropped into new contexts without dragging unrelated baggage.

Finally, low coupling supports parallelism in team development. Teams can work on separate modules simultaneously when the interfaces between them are stable. This is why API contracts and interface design are treated so seriously at large organizations.

---

## Q3: Why is high cohesion desirable?

**A:** High cohesion keeps a module's responsibilities tightly related, which predicts maintenance quality better than almost any other metric. A highly cohesive module is easy to understand — a developer can grasp its purpose from its name and limited surface area.

Highly cohesive modules change for one reason only. If a class handles "invoice calculation" but also "email formatting," it has low cohesion — a change to email formatting forces you to touch code that also handles invoice math, risking regressions.

High cohesion also improves reliability and testing. A module with one job has few edge cases and can be exhaustively tested. Research and industrial experience consistently show that highly cohesive, loosely coupled modules are the least expensive to maintain over time.

---

## Q4: What is encapsulation in object-oriented programming?

**A:** Encapsulation bundles an object's data (state) with the methods that operate on that data, while restricting direct access to the internal state. The object exposes a public interface (methods) and hides its internal representation (fields).

Technically, encapsulation is enforced with access modifiers: `private` fields and methods are visible only within the class; `public` methods form the intended interface; `protected` and package-private provide intermediate levels of visibility.

Encapsulation's purpose is twofold: to protect invariants (the object can never enter an illegal state because outside code can't directly mutate its fields) and to enable change (the internal representation can be swapped without breaking any caller). It is the mechanism that makes both low coupling and high cohesion achievable in practice.

---

## Q5: What is the difference between encapsulation and abstraction?

**A:** Abstraction is about exposing only the essential interface — *what* an object does — while hiding *how* it works. Encapsulation is the concrete mechanism (access modifiers, private state, method boundaries) that enforces that hiding.

Abstraction answers "what contract does this expose?" Encapsulation answers "how do we prevent violations of that contract?"

A practical example: a `BankAccount` class abstracts the concept of money with methods like `deposit(double)` and `withdraw(double)`. Encapsulation ensures that no external code can directly set the `balance` field to a negative value or bypass the withdraw limits. You can practice abstraction without strict encapsulation in some languages, but true OOP relies on encapsulation to back up its abstractions.

---

## Q6: What is tight coupling? Give an example.

**A:** Tight coupling occurs when a module directly depends on the internal implementation details of another module — class names, method signatures, data formats, or even the order of operations inside another class.

```java
public class OrderService {
    private JdbcOrderDao dao = new JdbcOrderDao();

    public double calculateTotal(Order order) {
        // Coupled to JdbcOrderDao's implementation details:
        logger.info("Total for " + order.getId());
        return order.getItems().stream()
            .mapToDouble(i -> i.getPrice() * i.getQuantity())
            .sum();
    }
}
```

Here, `OrderService` is coupled to `JdbcOrderDao` by name and to its construction logic. If `JdbcOrderDao`'s constructor changes (new parameters), `OrderService` must be modified. If the team wants to switch databases, this exact class must change.

Tight coupling manifests in several forms: `new` statements in business code, direct variable access on other objects, hard-coded URLs or table names, and using concrete classes instead of interfaces.

---

## Q7: Give an example of high and low cohesion in real code.

**A:** Low cohesion: a class called `Utils` or `Helper` with a static method for validating email addresses, another for formatting currency, another for generating UUIDs, and another for reading CSV files. Nothing relates these operations — a change to currency formatting touches a file that also contains email regexes.

```java
public class Utils {
    public static boolean isValidEmail(String s) { /* ... */ }
    public static String formatMoney(double d) { /* ... */ }
    public static String newUuid() { /* ... */ }
    public static List<String> parseCsv(String data) { /* ... */ }
}
```

High cohesion: the same responsibilities split into `EmailValidator`, `MoneyFormatter`, `UuidGenerator`, and `CsvParser`. Each class has one clear purpose.

The test tells you which one you have: describe the class in one sentence. "This class validates emails" is cohesive. "This class does miscellaneous utility stuff" is not. If your description uses the word "and," cohesion is probably low.

---

## Q8: How do coupling and cohesion relate to each other?

**A:** Coupling and cohesion are orthogonal dimensions, but they influence each other in design. A module with high cohesion is easier to keep loosely coupled, because a focused module exposes a small, stable surface area — few points of contact with the outside world.

Conversely, a low-cohesion "grab bag" module tends to spread dependencies everywhere: unrelated parts of the system reach into it for unrelated things, creating a tangled web of coupling.

The classic heuristic: you can trade one off against the other. You can temporarily reduce coupling by merging modules together (hiding coupling inside a bigger module), but this usually reduces cohesion. The sustainable solution is both: small, focused modules (high cohesion) connected through stable contracts (low coupling).

---

## Q9: What are the different levels/types of coupling?

**A:** Coupling is usually classified into a spectrum, from worst to best:

1. **Content coupling** — one module directly modifies the internals of another (reading/writing its local data). Worst form.
2. **Common/global coupling** — modules share a global data structure; any change to the global affects all users.
3. **Control coupling** — one module passes control flags to another ("do this, don't do that"), forcing the callee to branch on the flag.
4. **Stamp/data-structure coupling** — modules share a composite data structure but only use part of it.
5. **Data coupling** — modules communicate only through simple parameters (primitives or immutable values).
6. **Message coupling** — modules communicate through messages/events rather than direct calls.
7. **No coupling** — independence.

In practice you aim for data or message coupling. Content and global coupling are essentially always bugs to be refactored.

---

## Q10: What are the different levels/types of cohesion?

**A:** Cohesion also has a graded scale from worst to best:

1. **Coincidental cohesion** — parts are grouped arbitrarily (a grab-bag utility class). Worst.
2. **Logical cohesion** — parts are grouped by logic category (all I/O handling in one class) even though they're unreferred.
3. **Temporal cohesion** — parts are grouped because they happen at the same time (e.g., `startupTasks()`).
4. **Procedural cohesion** — parts are grouped because they follow a procedure (e.g., steps of a transaction), but they don't share data.
5. **Communicational/Informational cohesion** — parts operate on the same data (e.g., an `Order` class with methods that all use its fields).
6. **Sequential cohesion** — parts where the output of one feeds the input of the next.
7. **Functional cohesion** — all parts contribute to a single well-defined function. Best.

Your design goal is functional cohesion — one module, one purpose, where every element contributes to that purpose.

---

## Q11: What is the Law of Demeter?

**A:** The Law of Demeter (LoD), also called the Principle of Least Knowledge, says: a method `M` of object `O` may call methods of (1) `O` itself, (2) `O`'s direct fields, (3) `M`'s parameters, (4) objects created within `M`, and (5) global objects in some formulations. It must **not** reach through another object's internals to call a method on a third object.

The classic violation: `a.getB().getC().doSomething()` — `a` is reaching through `b` to talk to `c`. "Only talk to your immediate friends."

The Law of Demeter is a concrete rule that promotes both encapsulation and low coupling. It forces objects to expose meaningful interfaces instead of leaking their collaborators. Violations are the "train wreck" / "chain of dots" code smell.

---

## Q12: Why is the Law of Demeter important for encapsulation?

**A:** The Law of Demeter stops code from reaching through an object's internals. When you write `customer.getAddress().getCity().getZipCode()`, you depend not only on `Customer`'s interface but also on `Address`'s internal structure and the fact that `getAddress()` returns a navigable object.

That chain of knowledge is a coupling disaster: changing `Address` (making city a composed object, or `getCity()` return a value object) breaks every caller of the chain.

Applying Demeter — `customer.getZipCode()` delegating internally — hides the `Address` structure from callers. `Customer` can replace its zip-code storage wholesale (value object, formatted string, separate table) without any caller noticing. That's encapsulation in action: the knowledge of internals stays inside the object.

---

## Q13: What is the difference between "coupling" and "dependency"?

**A:** They're often used interchangeably, but there are nuances. **Dependency** is the general relationship where one module needs another to compile or run. **Coupling** is the *degree* and *direction* of connectedness — how much of the other module you depend on, and how easily changes in one propagate to the other.

You can have a dependency that is loosely coupled (depending on a stable interface) or tightly coupled (depending on internals). Dependency injection reduces coupling *while keeping the dependency* — the `OrderService` still depends on `MessageSender`, but the coupling is minimized to the interface contract.

In dependency graphs, "dependency" describes the edges, and "coupling" describes the quality and strength of those edges. Loose coupling does not mean "no dependencies"; it means dependencies are on abstractions, not implementations.

---

## Q14: What does it mean for a class to be "responsible" for something?

**A:** A class's responsibility is the reason it exists — the single purpose it serves or the single thing it knows how to do. Responsibility connects to cohesion (a class with one responsibility is highly cohesive) and to the Single Responsibility Principle.

We can think of responsibilities in terms of "who/what the class acts for" and "what the class knows about." A `PricingEngine` is responsible for computing prices. A `EmailSender` is responsible for delivering messages. 

Determining responsibility forces you to answer: "What can go wrong that is uniquely fixed by this class?" If two changes of different types both require editing this class, it has more than one responsibility — a cohesion problem. When a class's responsibility is blurred, coupling tends to rise as other classes touch it for mixed reasons.

---

## Q15: How does encapsulation prevent bugs?

**A:** Encapsulation prevents bugs by making illegal states unrepresentable. If `balance` is `private` and only changed through `deposit()` and `withdraw()`, then no external code can accidentally set `balance = -100`.

Consider an `Account` class where `status` and `balance` must be consistent (e.g., "frozen" accounts can't be debited). Encapsulation lets you enforce both invariants in the methods that change them. Outsiders can read state but never corrupt it.

Encapsulation also prevents "spooky action at a distance": if every class could freely write to every other class's fields, a bug could be caused by any of a thousand call sites. With encapsulation, state changes happen through known methods with clear contracts, so the source of a bug is easy to locate.

---

## Q16: What is an example of a train wreck (Law of Demeter violation)?

**A:** A train wreck is a chain of method calls that reaches through multiple objects:

```java
public void sendWelcomeMail(User user) {
    String zip = user.getProfile().getAddress().getPostalCode();
    String city = user.getProfile().getAddress().getCity();
    mailer.send(user.getEmail(), "Hello " + city + " " + zip);
}
```

This code knows that `User` has a `Profile`, which has an `Address`, which has `PostalCode` and `City`. Any change in that structure breaks the caller. It also makes testing painful — you must construct a `User`, a `Profile`, and an `Address` to test the method.

The Demeter-compliant version: `user.getPostalCode()`, `user.getCity()` — the `User` class delegates to its internals. The caller only knows the `User` contract. The internal structure of `User` (profile → address, or formatted string, or persisted separately) is hidden as encapsulated detail.

---

## Q17: What is the relationship between encapsulation, information hiding, and Abstraction?

**A:** Information hiding is the broader design principle: hide design decisions that are most likely to change (Parnas). Encapsulation is the implementation mechanism that supports it — access control, private state, focused method surface. Abstraction is the interface you expose once the hidden details are removed.

In Parnas's classic formulation, modules should be designed so that each hides one design decision. The choice of file format, the choice of algorithm, the choice of data structure — each should be a hidden secret inside a module with a stable interface.

Abstraction is what's left after hiding: the essential contract that callers see. So the pipeline is: abstraction (what you expose) → information hiding (what you conceal) → encapsulation (how the hiding is enforced in an OOP language).

---

## Q18: How do access modifiers (private, protected, public) support encapsulation?

**A:** Access modifiers give encapsulation its teeth. `private` restricts access to the enclosing class, `protected` allows subclasses (and package members) access, and `public` exposes to everyone.

The key point: access modifiers are about *who can touch what*, and they let you curate the interface. Fields are typically `private` (or protected in inheritance hierarchies), and only methods needed by collaborators are `public`.

Beyond the three core modifiers, Java offers package-private (default) visibility, and languages like C++ use `friend`, C# uses `internal`. Module systems (Java modules, C# assemblies) restrict visibility across package boundaries. The principle: each type of access is a decision about where the boundary of trust sits — the minimal surface that lets the system work without exposing internals.

---

## Q19: What is the difference between a getter that returns a copy and one that returns the internal reference?

**A:** A getter returning the internal reference leaks the encapsulated data. Callers get direct handles into your `private` state and can mutate it without your knowledge:

```java
public class Cart {
    private final List<Item> items = new ArrayList<>();
    public List<Item> getItems() { return items; } // BAD: caller can do cart.getItems().clear()
}
```

Returning a copy (`new ArrayList<>(items)`) or an unmodifiable view (`Collections.unmodifiableList(items)`) preserves encapsulation — callers can read but not corrupt the internal state.

Returning a copy costs a bit of memory/CPU per call and means callers see a snapshot, not live state. Returning the internal reference is fast but breaks encapsulation. Modern practice: return the live unmodifiable view, or expose mutation only through the object's own methods. This is sometimes called "defensive copying."

---

## Q20: What is "package-private" or "internal" visibility used for?

**A:** Package-private (Java) / internal (C#) visibility confines access to a group of related classes — the package or assembly. This is a powerful encapsulation tool at the package level.

It enables **package-private testing** (test classes in the same package reach internals), **package-private helper classes** (support classes callers outside the package never see), and **package cohesion** (a package is treated as one cohesive unit with its own internal consistency).

Recall: for self-contained object A, `accounts` fields can only be mutated through A's public methods when fields are private. Package-private widens the boundary slightly: the whole package becomes the "trusted unit." This is the sweet spot for many designs — cohesion within a package and coupling only through the package's public surface.

---

## Q21: How do you measure coupling and cohesion in a real codebase?

**A:** Tools and metrics play a role. **Fan-in** (how many modules use this module) and **fan-out** (how many modules this module uses) approximate coupling. Afferent coupling / efferent coupling (Ca/Ce) are the packaged-up versions.

**LCOM** (Lack of Cohesion of Methods) counts how many method pairs share no fields. High LCOM suggests a class holds unrelated responsibilities. Tools like SonarQube compute cohesion and coupling metrics, but they're heuristic — they flag smells, not guarantees.

The most reliable measure is manual: read the code. How often does a change in one module *force* a change in another (coupling)? Can you describe each class in one sentence without "and" (cohesion)? Metrics find hotspots; judgment confirms them.

---

## Q22: What is "feature envy" and how is it related to cohesion?

**A:** Feature envy is the code smell where a method spends most of its time reading or using another class's data instead of its own. The method is "envious" of the other class's fields.

```java
public class DiscountCalculator {
    public double applyDiscount(Order order) {
        double total = order.getItems().stream()
            .mapToDouble(i -> i.getPrice() * i.getQuantity())
            .sum();
        return total - (total * order.getDiscountRate());
    }
}
```

`applyDiscount` uses `Order`'s data (items, discountRate) almost exclusively — it belongs on `Order`, not here. This is a *cohesion* problem: the responsibility (discount logic) is split across classes.

The fix is "Move Method" — move the discount logic (and any helper data) into `Order`. This raises `Order`'s cohesion (its data and operations unify), and it reduces coupling (the external class stops depending on `Order`'s internals). Feature envy is the classic tell that cohesion has been misplaced.

---

## Q23: What is the difference between stamp coupling and data coupling?

**A:** **Data coupling** means modules communicate with simple parameters — primitives or immutable values. `calculateTax(String country, double amount)` is data-coupled to its caller: it needs exactly country and amount.

**Stamp coupling** means modules share a composite data structure but use only part of it. `calculateTax(Order order)` where `calculateTax` only reads `order.getCountry()` is stamp coupling — the caller must build a full `Order` (maybe a fake one) to pass one field.

Stamp coupling is looser than content coupling but tighter than pure data coupling, because changes to `Order` can affect `calculateTax` even though it only uses one field. Refactoring stamp coupling toward data coupling (passing `country` instead of `order`) reduces coupling and makes call sites simpler and clearer.

---

## Q24: What is the difference between sequential and functional cohesion?

**A:** **Sequential cohesion** groups operations where the output of one feeds the input of the next — the order matters — but the elements don't necessarily share data or a single purpose.

```java
public void processPipeline(File file) {
    List<String> lines = readLines(file);
    List<Record> records = parse(lines);
    List<Record> valid = validate(records);
    persist(valid);
}
```

Each step uses the previous step's output. This is better than coincidental cohesion but not functional.

**Functional cohesion** groups elements that all contribute to *one* well-defined function, regardless of procedure. `parseCsv(String raw)` — read, split, tokenize, map to records — everything inside serves the single job "parse CSV."

The difference is subtle: sequential steps serve a pipeline; functional parts serve one function. You can improve a sequentially cohesive module by asking whether the pipeline itself is a single responsibility worth extract.

---

## Q25: Why is it generally safer to expose behavior (methods) rather than data (fields)?

**A:** Exposing behavior rather than raw data is the essence of encapsulation. A method is a *contract* — you can change how it's implemented, internally, without breaking callers. A field is a *fact* — callers read it directly, and any change to its type, format, or derivation breaks them.

Consider exposing `double getBalance()`. Today it's a stored value; tomorrow it might be a computed sum of ledger entries. Callers of the method never notice. But if callers were reading `account.balance` directly, the change forces every caller to be edited.

Methods also let you enforce invariants and add behavior around access: currency formatting, rounding, audit logging, lazy loading. Fields give callers nothing but a raw number and full responsibility to interpret it. Behavior-bearing interfaces are how low coupling and high encapsulation coexist.

FX_EOF---

## Q26: How do immutable objects help with loose coupling?

**A:** Immutable objects — objects whose state cannot change after construction — are the safest units to share between modules. Since nothing can mutate them, no module can corrupt another's view of the data through shared references.

Immutable collaborators simplify reasoning: when you pass an `Order` to a validator, you know the validator can't silently modify it. That removes an entire class of coupling bugs — the hidden, out-of-band mutation.

Immutability also makes caching, thread-safe publication, and value comparison trivial, all of which reduce coordination between modules. Combined with a small interface, immutable objects give you data coupling at its safest: callers receive complete, stable values and share nothing mutable.

---

## Q27: What is "control coupling" and why is it considered harmful?

**A:** Control coupling occurs when one module passes a flag or command value to another to steer its behavior: `process("CREATE", data)` or `handleDocument(true)` where the boolean changes control flow.

```java
public void process(String action, Object data) {
    switch (action) {
        case "CREATE": // ...
        case "UPDATE": // ...
        case "DELETE": // ...
    }
}
```

It's harmful because the caller must know the callee's internal action vocabulary, and the callee must know all the callers' intentions. Every new action requires changes in both sides. The two modules are coupled through a shared implicit protocol.

Breaking control coupling: split the callee into separate methods (`create(data)`, `update(data)`, `delete(data)`), or use polymorphism (strategy objects) so the caller doesn't dictate control flow. Explicit capability methods are clearer and remove the hidden protocol.

---

## Q28: What is common (global) coupling and how do you avoid it?

**A:** Common/global coupling means multiple modules read and write a shared global — a global configuration object, a thread-local, a shared registry, or environment-wide variables. Any module can modify the global and invisibly affect all others.

The core problem is invisible coupling: there's no interface relationship to see, so changes ripple unpredictably. Testing becomes dangerous (state leaks between tests), and concurrency becomes a minefield of shared mutation.

Smaller, more contained alternatives:
- Pass explicit values down through constructors and parameters.
- Use a single, read-only immutable "settings snapshot" built once at startup, injected into modules.
- For genuinely shared state, encapsulate it in one class with a narrow public API (a `MetricsRegistry`), so access is controlled and auditable.
- In tests, always reset or inject fresh instances — never leave "ambient" state.

---

## Q29: What is the difference between a mix of "tightly coupled" and "correctly encapsulated" networking of objects?

**A:** Both involve objects referencing other objects, but the relationship differs in what the reference is to. Tight coupling happens when a reference is to *internal implementation* — concrete class, internals of the collaborator, or its mutable state. Correct encapsulation happens when a reference is to *an interface* — the abstract contract — and collaboration occurs only through that contract.

Consider `NotificationService` referencing `MessageSender` (an interface). That's a dependency but not tight coupling — `NotificationService` can work with any sender. Conversely, referencing `ConcreteSmtpSender` with direct access to its internals is tight coupling.

Another angle: properly encapsulated objects *ask* other objects to do things. Tightly coupled objects *take* things apart — they reach into internals, read raw fields, and assume ownership of another object's state. The same "object network" can be loosely coupled (interface-based, encapsulated) or tightly coupled (implementation-based, internal-accessing) depending on what the edges in the network point to.

---

## Q30: How does dependency injection support low coupling?

**A:** Dependency injection (DI) removes the *creation* responsibility from the consumer. When a class constructs its own collaborators (`new JdbcDao()`), it hard-wires both its dependency and the concrete implementation — high coupling. When collaborators are passed in (constructor injection), the class only declares "I need something with this contract."

DI therefore reduces coupling in two ways: (1) the dependency is on an abstraction, not a concrete class, and (2) the knowledge of *where* the dependency comes from is moved out of the class entirely.

Single joining principle: instead of each class knowing how to build friends, one composition root builds them. DI also makes coupling *visible and measured* — every dependency is declared in the constructor, so a class with ten constructor parameters is loudly advertising its coupling load, prompting a split.

---

## Q31: Can a system have high coupling but high encapsulation? Can it have low coupling but low encapsulation?

**A:** Yes to both. **Encapsulation/coupling** measure different things.

High encapsulation + high coupling: many modules are individually well-encapsulated (private fields, clean methods) but reference each other's concrete classes everywhere. Change a concrete class name and hundreds of callers break. Encapsulation doesn't guarantee the interfaces are stable; if modules depend on concrete types, coupling stays high.

Low coupling + low encapsulation: modules are few and don't depend on each other much, but internally they leak state — public fields, no invariants, data structures the whole system freely mutates. This is loose *coupling* in degree (few modules reference few things) but encapsulation is absent, so correctness is fragile and any shared structure is exposed to corruption.

The takeaway is that encapsulation and loose coupling are separate axes; good design needs both.

---

## Q32: What is "information hiding" (Parnas) and how does it differ from encapsulation?

**A:** Information hiding, coined by David Parnas (1972), is the principle that modules should hide design *decisions* that are likely to change. The interface exposes only the stable capabilities; everything volatile (algorithms, file formats, data layouts, platform specifics) is a "secret" behind the interface.

Encapsulation is the mechanism that implements information hiding in OOP: access control, private state, and method boundaries regroup those secrets and only expose the stable contract.

The distinction: information hiding is the *what* (the volatile decisions you conceal), encapsulation is the *how* (the language machinery enforcing concealment). Good modular design first decides what is likely to change, then uses encapsulation to quarantine those changes.

---

## Q33: How do you refactor a class that has too many responsibilities?

**A:** The refactoring follows a systematic path. First, identify the responsibilities: list every reason this class could change. Then extract the clearly separable reasons into their own classes using "Extract Class."

```java
// Before: Publishes notifications AND manages subscriptions AND formats messages
public class Notifier { /* ... */ }

// After
public class SubscriptionRegistry { /* ... */ }
public class MessageFormatter { /* ... */ }
public class NotificationSender { /* ... */ }
```

Next, replace direct field access with delegation: the original class either delegates to the extracted classes or is replaced entirely. Move the tests too — each extracted class gets its own focused test suite.

Finally, review the constructor and collaborators. Fewer responsibilities should mean fewer injected dependencies. The outcome: each class is describable in one sentence (high cohesion), and collaborators connect through narrow interfaces (loose coupling).

---

## Q34: Why is it easier to test a highly cohesive class?

**A:** A highly cohesive class has one purpose, which means its test surface is small and purpose-driven. Test inputs, expected outputs, and edge cases map directly onto that single responsibility.

Testing a `PricingEngine` requires you think about prices — nothing else. Testing a kitchen-sink class forces you to set up unrelated state (accounts, emails, logging, file I/O) to reach the one method you care about.

High cohesion also means fewer collaborators to mock (each responsibility tends to bring a collaborator), so tests are fast, isolated, and focused. And when the one responsibility changes, only a few tests change. With low cohesion, a change touches many tests spread across unrelated scenarios, coupling your test suite to module volatility.

---

## Q35: What is a "god class" and what problems does it introduce?

**A:** A god class is a class that grows to handle many unrelated responsibilities — orders, inventory, billing, email, reports — typically by accumulating fields and methods over years of features. It is the extreme of low cohesion.

Problems: (1) *Every* feature change touches it, making it a bottleneck and a merge-conflict factory. (2) High fan-out — it "knows" about, or reaches into, dozens of other classes (high coupling). (3) Testing is impossible without initializing half the system. (4) Regressions are common because unrelated features share code paths.

The god class is the primary target for "Extract Class / Feature Envy" refactorings. Divide it by responsibility, move each cluster of fields and methods into a focused class, and have the original simply coordinate (dedicated to invariants) or disappear entirely.

---

## Q36: What is the "Tell, Don't Ask" principle?

**A:** Tell, Don't Ask means: instead of *asking* an object for its data and *deciding* what to do with it, *tell* the object what outcome you want and let it handle the details.

```java
// Ask: outsider reads and decides
if (account.getBalance() >= amount) {
    account.setBalance(account.getBalance() - amount);
}

// Tell: the object owns the decision and mutation
account.withdraw(amount);
```

`withdraw` checks funds, applies fees, updates balance, and throws `InsufficientFundsException` if needed — all inside the object, protecting invariants. The outsider expresses intent only.

Tell, Don't Ask is a strong cohesion tool: logic moves to the class whose data it uses (fixing feature envy) and a encapsulation tool: no one mutates another's state directly. As a rule of thumb: if your code reads an object's state and immediately mutates that same object, that logic belongs to the object.

---

## Q37: What is a "mutable class with exposed internals" — how do you redesign it?

**A:** An exposed-internals class publicly hands out references to its internal collections or state so callers can alter it:

```java
public class ShoppingCart {
    private List<Item> items; // private, but...
    public List<Item> getItems() { return items; }  // leak!
}
```

Redesign steps: (1) return unmodifiable views (`Collections.unmodifiableList(items)`) for reads; (2) expose *behavior* that mutates — `addItem(Item)`, `removeItem(ItemId)`, `clear()`; (3) return *copies* only when callers truly need mutable snapshots (rare); (4) consider making the whole class immutable (`add` returns a new `ShoppingCart`).

The payoff: internal storage can change (list → map → database-backed) without breaking callers, and invariants (no negative quantities, sums recalculated) are enforced centrally. Encapsulation is restored at the cost of a slightly more deliberate API.

---

## Q38: How do events and messaging support loose coupling?

**A:** Events and messaging let modules communicate *without naming each other*. A producer publishes an event (`OrderPlaced`) to a broker; consumers that subscribe receive it. Neither side references the other's type directly — they share only the event's schema.

Chat-like analogy: a radio station broadcasts to anyone listening; it doesn't need to know who's listening. Adding a new listener never requires changing the broadcaster.

This is the lowest coupling you can get while still communicating: the dependency is on the message/event contract, not on a peer's symbols. It also enables offline decoupling (consumers can be down, messages queue), asynchronous scaling (each side scales independently), and temporal decoupling (producer doesn't wait for consumer).

---

## Q39: What are the trade-offs of event-driven decoupling compared to direct method calls?

**A:** Direct method calls are synchronous, typed, easy to trace, and guaranteed-ordered — but coupling is high: the caller must know the callee, its interface, and react to its return value.

Event-driven decoupling gives independence, scaling, and resilience, but trades away:

1. **Guaranteed delivery** — a published event must be stored and redelivered for reliability; in-memory pub/sub silently loses messages on crash.
2. **Eventual consistency** — consumers process events asynchronously, so state is temporarily inconsistent. Order data may lag, cache may serve stale rows.
3. **Testing and tracing complexity** — you can't "just call" a handler; you must publish + subscribe and wait.
4. **Ordering and idempotency** — across partitions, ordering breaks, and duplicate delivery requires idempotent consumers.

The senior trade-off is "synchronous sync" data (payments, explicit user actions) versus "asynchronous async" side effects (notifications, projections). Pick events where independence and scaling outweigh consistency guarantees.

---

## Q40: How do you compare cohesion across a class vs. a method vs. a package?

**A:** Cohesion applies at every granularity: a method is cohesive if all its statements serve one outcome; a class is cohesive if all its methods and fields serve one responsibility; a package is cohesive if its classes collaborate for one purpose.

Method-level cohesion issues look like methods with "and" responsibilities (`saveAndNotifyAndLog`). Class-level issues are god classes or free-floating helper clusters. Package-level issues are "utility" packages full of unrelated functions.

The strategies mirror each other: extract unrelated statements into separate methods/classes/packages. The unit of cohesion should track the unit of change — things that change together stay together (component cohesion), things that change for different reasons split apart.

---

## Q41: What is the "stable dependencies" principle, and its relation to coupling?

**A:** The Stable Dependencies Principle (SDP) states that the direction of dependency should point toward stable things. Packages that change often should not be depended upon; packages that change rarely can be.

Why it matters: coupling to a *volatile* module means every change to that module ripples into your dependent modules. Coupling to a *stable* module (a well-designed interface, a rarely-changing framework) is there, but changes are rare, so the ripple is small.

The guideline collapses to: abstract toward stability. Volatile domain logic depends on interfaces; the concrete, frequently-changing implementations live at the periphery. This is another way of seeing DIP — the abstractions stay stable, so depending on them gives the benefits of coupling without most of its costs.

---

## Q42: What is "fan-in/fan-out" and why is a high fan-out a warning sign?

**A:** Fan-in is how many modules depend on this one; fan-out is how many this one depends on. High fan-in to a stable, cohesive module is good — lots of callers, one stable contract. High fan-out is classically a warning sign.

Each outbound dependency exposes this module to change: when any of its N dependencies change, this module may need to change (or at least be re-tested). High fan-out also means a change here *acts* on many targets.

A class with fan-out 15 is coupled to fifteen concepts. Decide whether that's inherent (an orchestrator coordinating many primitives) or a cohesion leak (the class does fifteen things). High fan-out + low fun-in + high LCOM is the signature of a god class. Use it as the trigger to split.

---

## Q43: How does the Single Responsibility Principle relate to cohesion?

**A:** SRP — a class should have only one reason to change — is essentially "high cohesion applied to reasons for change." If two things change for different reasons, they belong in different classes, hence splitting them raises cohesion.

Cohesion asks *in what way are the responsibilities related*; SRP asks *would separate triggers of change force this edit*? Both point to the same action: group by "what changes together / for the same reason," separate by "changes for different reasons."

The famous nuance (Uncle Bob's refined definition): "a reason to change" means "a stakeholder/user who requests a change." That reframes SRP as a consequence of who the class serves. Either way, the practical test — "can I describe this class in one sentence without 'and'?" — serves both principles.

---

## Q44: What is the difference between structural and behavioral coupling?

**A:** Structural coupling concerns *what types/names the code references* — class names, interfaces, method signatures, shared data structures. Change a name or field layout and structurally coupled code breaks.

Behavioral coupling concerns *the order and timing of interactions* — protocol expectations ("call init before start"), ordering assumptions ("fill band on 'start'"), and lifecycle dependencies. Even if names never change, behavioral coupling breaks when a caller no longer satisfies the expected probation of calls.

Example: two classes reference the same `DataSource` by name (structural coupling) but also assume the connection is pooled (behavioral coupling). The fix for structural coupling is interfaces/config; the fix for behavioral coupling is explicit contracts, sequence enforcement, and state machines. Senior engineers check for both — refactoring for structural coupling alone often hides behavioral coupling that bites later.

---

## Q45: What is "leaky abstraction" and what's the fix?

**A:** A leaky abstraction is an interface that can't fully hide its implementation — callers must know details the abstraction was meant to conceal. Classic examples: an `OrderRepository.save()` that throws `SQLException` (the caller learns about JDBC), or an HTTP client wrapper that copies headers for retries (the caller learns about REST internals).

The failure is one of encapsulation and information hiding. The fix starts with selecting interfaces that *can* be airtight — stable domain concepts (save an order, upload a file). Add a translation layer: wrap `SQLException` in domain exceptions, wrap REST errors in `UploadFailedException` with a domain-friendly description.

Accept that near-perfect abstraction is unrealistic; aim for abstraction at the right seam, and make the leaks deliberate and documented in a few places rather than scattered throughout.

---

## Q46: How do you decide between using direct calls and events/messages?

**A:** Consider three axes: **consistency**, **lifespan**, and **simplicity of tracing**.

- If the consumer's effect must be visible *before the caller's transaction commits* (deducting inventory when placing an order), use a direct, synchronous call in the same transaction.
- If with-tolerance for the consumer to lag (send a confirmation email, update a read model), use events — eventual consistency is acceptable.
- If consumers are *out of process*, or *multiple unknown consumers* exist, events/messaging is forced.
- If debugging and revert simplicity dominate (a greenfield monolith of modest complexity), direct calls are easier to trace and refactor.

Simply put: events where you can tolerate "a little time later, handled without knowing who," direct calls where you must have "guaranteed finished, before we return." The "sync-or-bust" question is the crux.

---

## Q47: What are the benefits and costs of immutable value objects?

**A:** Benefits: (1) safety — no one can corrupt shared state, which removes a generation of coupling bugs; (2) trivially safe concurrency — a frozen object can be published without synchronization; (3) reliable equals/hashCode — great for keys, caching, and comparisons; (4) easy reasoning — no hidden time-varying state.

Costs: (1) updated values require allocation — changing one field with a new value allocates a copy; (2) deep immutability is verbose in most languages (every collected collaborator must also be immutable, or defensively copied); (3) some patterns (caches, connections, lazy fields) are awkward with immutability.

The cursor: turn domain "values" (Money, Address, Date) immutable; let "entities" with identity and lifecycle (Account, Order) keep controlled mutability behind behavior methods.

---

## Q48: What is the difference between "coupling to an interface" and "coupling to a base class"?

**A:** Interfaces couple you to *a contract* — a set of capabilities. Base/abstract classes couple you to *an implementation skeleton* — its state, protected methods, and construction order. Reinventing hierarchy: interfaces are about "what it can do"; base classes are about "how it does it."

Coupling to an interface is one-directional: the implementor depends on the interface; consumers depend only on the interface. Either can change its internals freely.

Coupling to a base class, by contrast, drags along protected fields, template behavior, and constructor chains. Subclasses often conform to assumptions baked into the base (e.g., it must call `super.init()`). A change to the base's protected members ripples through every subclass — tight coupling by inheritance, fragile base class syndrome.

Preference (composition over inheritance): interface first; delegate to a base class only when subclasses genuinely share implementation and the base is stable and cohesive.

---

## Q49: How do you keep coupling low across a module (package) boundary?

**A:** At the package/module level you control coupling via `exports` and imports. In Java modules, `module-info.java` declares which packages are exported; unexported classes are invisible outside. C# uses `internal`. These are the hard controls.

Design controls: (1) the exported surface is small and interface-based; (2) internal classes are package-private or hidden; (3) cross-module flow uses defined ports (interfaces, events); (4) each package has a cohesive purpose — "customer", "billing", "notifications" — rather than "utils".

Coupling measures at this level count *how many other packages each package references*, and what they reference (interface vs. concrete). Tests enforce these edges (ArchUnit in Java) so devs can't quietly cross boundaries.

---

## Q50: What is the role of a "facade" in reducing coupling?

**A:** A facade is a single object that provides a simplified, stable interface to a subsystem — a cluster of classes. Clients interact with the facade, not with the individual classes, shrinking many point-to-point couplings into one relationship.

```java
public class AccountFacade {
    private final AccountRepo repo;
    private final FraudEngine fraud;
    private final NotificationService notifier;

    public Account open(String email, String plan) {
        validate(email);
        if (fraud.isSuspicious(email)) throw new RejectedException();
        Account a = repo.create(email, plan);
        notifier.welcome(a);
        return a;
    }
}
```

External callers now couple only to `AccountFacade` for open-an-account. Inside, the cluster can be rearranged freely. The trade-off: a facade can become a god-object bottleneck if it grows past a subsystem's boundary — keep one facade per cohesive subsystem.---

## Q51: What is a "bounded context" and how does it control coupling in DDD?

**A:** A bounded context is a boundary inside which a particular model applies consistently. Within it, terms like "customer" or "order" have precisely defined meanings; outside it they may differ. The boundary itself decouples models from each other.

Coupling control happens through the context map: contexts may use shared global contracts (published language), one context may conform to another (conformist), or they may be fully decoupled via anti-corruption layers and domain events.

In a system where Orders and Shipping both need "package," the two contexts define their own autonomous models. Order doesn't compile against Shipping's classes; it consumes its events or calls its contract. That horizontally-tamed coupling is what lets large teams evolve subdomains independently.

---

## Q52: How do you know when to split a monolith into modules or microservices based on coupling?

**A:** The heuristic is simple: split where changes don't couple, keep together where they do. Concretely, examine the actual change history and dependency graph.

- If changing order logic forces edits in inventory code, they're coupled — keep them together.
- If you can change billing without touching anything else, billing is an independent change axis — extractable.
- If two parts communicate only through small, versionable contracts and tolerate async delivery — microservice candidates.

Microservices additionally require operational independence (deploy triggers, separate scaling, independent failure). Coupling analysis tells you where boundaries are *safe*; team and ops maturity tell you whether to pull the trigger. The classic mistake: splitting on "looks like a noun" (user-service, order-service) rather than on measured decoupling axes.

---

## Q53: What is "shared kernel" and "published language" in context mapping?

**A:** **Shared kernel**: the small slice of a model two teams agree to share — shared types, common interfaces, value objects — kept deliberately small and stable. Both teams compile against it, so it must change rarely and by mutual consent.

**Published language**: a formal, documented contract (API schema, message format) that a context publishes; other contexts conform to it or translate it. Chat about "OpenAPI spec" or "event schema" are published languages.

Both keep coupling *explicit and controlled*. Shared kernel is the pragmatic smallest-coupling trick: instead of duplicating or reaching across, teams share a tiny stable core. Published language scales further — instead of sharing code, they share a schema, which is inherently decoupled (sender/receiver never reference each other's symbols).

---

## Q54: What is a "conformist" and its trade-offs for coupling?

**A:** In DDD context mapping, a conformist is a context that accepts another's model wholesale — it uses the upstream's data formats and protocol without translation. It keeps integration cost low (no adapter to write) but couples the conforming context to the upstream's model.

Trade-off: translation (anti-corruption layer) costs work every time — you build converters and mapping code — but it buys a buffer: upstream changes don't leak into your domain. Being a conformist saves that cost but means upstream model changes (field renames, schema tweaks) ripple directly into your code.

Senior guidance: conform when upstream is stable and its model is close to your needs (e.g., internal team, rarely changes); use a translation/ACL when upstream is external, volatile, or its model language clashes with your domain. Choosing conformism for a fast-moving external vendor is a shared coupling debt you'll pay in churn.

---

## Q55: How do message brokers (Kafka, RabbitMQ, SQS) factor into coupling?

**A:** A message broker transposes coupling: producers and consumers no longer couple to each other — each couples only to the broker and the message schema. That centralization is why topics/queues survive as the "one contract" both sides depend on.

Trade-offs worth knowing: (1) the *schema* becomes load-bearing — evolving it requires a data contract process (schemas and versioning); (2) the broker is a single point of failure unless replicated — redundancy still couples you to its upgrade cadence; (3) you inherit ordering, exactly-once, and redelivery semantics decisions, which couple into your consumer logic (idempotency).

A pragmatic read: brokers give you loose coupling at the architecture level — teams, services, deployment units — at the cost of strict contract discipline and operational gravity. Use them when the decoupling between teams outweighs the broker's overhead.

---

## Q56: What happens when you have high cohesion but high coupling?

**A:** High cohesion + high coupling arises when a few modules are each very focused, but they refer to each other's concrete internals heavily. Example: `OrderService` (cohesive) and `InventoryService` (cohesive), where `OrderService` directly constructs `InventoryService` and calls sub-methods that depend on `Inventory`-internals order.

Symptoms: although each class is single-purpose and readable, a change to any internal detail in one cascades through the other. Tests require both real classes (or elaborate mocks) because there's no seam at the boundary.

The fix is to invert the seams: introduce an abstraction at the *crossing*, so each cohesive module depends on the other's *contract*, not internals — and let composition wire them. A cohesive module is the raw material; the missing piece on a high-coupling problem is situation at the boundaries.

---

## Q57: What happens when you have low coupling but low cohesion?

**A:** Low coupling + low cohesion: few modules, little referencing between them, but each module is a grab-bag of unrelated things. Example: one giant `DataUtils` class with `parseCsv`, `sendEmail`, `formatAmount`, `readFlagsFromCommandLine` — the system references it sparsely (only four places), so coupling is genuinely low — but each of those places drags in the whole soup.

Problems: harder to reason about (each method unrelated), easier to break (a change in CSV parsing can affect nothing else — fine — but it lives next to email code, so touching the file risks accidental regressions), and harder to name/test (the tests for `DataUtils` are a salad).

Fix: name and split by responsibility. Because coupling is low, splitting is cheap — each piece is unused elsewhere. The risk profile is the exact inverse of the god class: nothing couples here *yet*, so the cost of forgetting to split is a slow creep toward bigger shared surfaces as callers multiply.

---

## Q58: How does the Adapter pattern support low coupling?

**A:** An adapter converts one interface into another — it lets a client use a collaborator that speaks a different contract. The client couples only to its preferred abstraction; the contract it likes. The adapter handles translation; the underlying class knows nothing.

```java
public interface Clock { Instant now(); }

public class SystemClock implements Clock {
    public Instant now() { return Instant.now(); }
}

public class FixedClockAdapter implements Clock {
    private final Instant fixed;
    public Instant now() { return fixed; }
}
```

In tests, you swap a `FixedClockAdapter` in; in production `SystemClock`. The decoupled seam means you can test time-dependent logic without sleeping.

Adapters are the loose-coupling glue for everything that arrives with an incompatible contract — legacy systems, third-party SDKs, different protocols. Coupling is focused in one thin, easily-replaced class rather than scattered and entangled.

---

## Q59: What is the mediator pattern vs. the facade pattern for coupling?

**A:** A **facade** simplifies a subsystem for callers — its edges reduce coupling by replacing many references with one. Communication still happens peer-to-peer among the subsystem's internals; the facade merely hides them.

A **mediator** actively centralizes *interactions between objects*. Objects don't reference each other; they reference the mediator, which routes and coordinates. The mediator converts N×N couplings into a star.

Which to choose: facade when you just want a simple entry point (the cluster already works well, it's theirs). Mediator when objects directly requesting each other causes nesting chaos and you want explicit, single-point coordination, but be warned — the mediator can become a god object and a bottleneck. Use mediators for genuinely intertwined groups (UI dialogs, flight control), facades for "give me one clean API to this subsystem."

---

## Q60: What is content coupling and why is it the worst kind?

**A:** Content coupling means one module directly manipulates another's internal data or logic — modifying fields the other owns, using its private implementation details, or calling into its internals at arbitrary points. The two modules effectively become one body whose parts are being twisted from outside.

```java
account.balance -= amount;          // content coupling: external mutation
customer.cart.calculateLocked();    // reaching through one object's guts to another's
```

Why worst: (1) changes to internal representation break all content-couplers; (2) invariants become unenforceable — nothing stops the external writer from producing an illegal state; (3) it defeats encapsulation entirety; (4) bugs become attribution hell — the corrupting writer can be anywhere.

Fix: replace with behavior — an `Account.withdraw(amount)` call in this example — so the object enforces its own rules; or, rediagnose boundaries if two classes genuinely need this intimacy (they are actually one class).

---

## Q61: How do you maintain encapsulation when your class state must be exposed for serialization or display?

**A:** Serialization (JSON/XML), DB mapping, and view models create tension: consumers want structure, you want a clean interface. The discipline is to separate *transport* from *domain*.

Options: (1) DTOs/projection views with the exact fields consumers need, mapped from the domain (domain stays encapsulated, transport is a copy — changing serialization never touches domain invariants); (2) explicit serializer config (`@JsonProperty`), controls attribute names, not domain access; (3) for DB, use a repository that maps between entity internal state and rows.

Cardinal mistake: decorating the domain object with serialization annotations to shove it through an enum serializer — now the API and the domain are one, and API changes force domain edits (coupling). Prefer DTOs at the edges, domain around the core.

---

## Q62: What is "anemic domain model" and how does cohesion suffer?

**A:** An anemic domain model is a set of objects that are almost pure data — getters, setters, fields — with all the behavior in separate "service" classes. `Order` is a bag of fields; `OrderService` contains every rule and mutates the bag.

Cohesion suffers because the class's data and its methods (in the service) are separated. The service, in turn, becomes a god service coordinating quantities of foreign data with feature envy (services frequently reach into object guts) — the exact pairing that low cohesion/high coupling warnings describe.

Whether anemic is bad is debated, but the design tension is real: either you assemble data+related logic in the domain types (richer, more cohesive), or you accept services orchestrators that mutate plain DTOs — which is simpler but loosens invariants. Prefer binding data to the rules that own it; keep services for cross-aggregate orchestration only.

---

## Q63: What is a "database transaction" boundary and how does cohesion/coupling apply?

**A:** A transaction boundary marks the span of operations that must commit or roll back atomically. Coupling applies: if you *coincidentally* put two unrelated updates in the same transaction, you couple their fates — a rollback of one rolls back the other, and a retry of one redoes the other.

Cohesion, by contrast, recommends aligning each transaction with *one domain use case*, not both: a fraud-check + account creation in a single `openAccount` transaction is cohesive; the same transaction spanning account-open AND unrelated audit-log flush is coincidental coupling.

Practical guidance: keep transactions as narrow as the invariant needs. Multiple independent transaction-bearing calls that don't share invariants become retryable, composable units. Over-transacting hides latency (long locks, contention) and couples failure modes — under-transacting risks inconsistent state. The sizing of the transaction *is* a coupling decision.

---

## Q64: How do cross-cutting concerns (logging, caching) affect coupling?

**A:** Cross-cutting concerns sprinkled inside every method create *widespread* coupling: every class calls the logger, the metrics sink, the cache — and every change to that infrastructure tsunamis across the codebase. Encapsulation suffers too: business methods are strewn with infrastructure calls.

The clean approach: (1) the *interface* for the concern is in the domain (e.g., `AuditLogger`), (2) implementation is injected/instrumented centrally — AOP intercept, decorator wrap, or framework hook — and (3) business code does not know when logging/caching happens.

Trade-off: AOP and proxies add magic that harms traceability; explicit decorators are verbose. Measure by: which changes more often — the business rules (then hide the concern) or the concern itself (then keep it explicit)? Coupling to a *stable* interface for a concern (the `Logger` contract) is acceptable; coupling to a volatile implementation is not.

---

## Q65: How do you keep a public API from leaking implementation details?

**A:** Leaks happen when the public surface exposes names and types that are implementation-shaped: method names that reveal "how" (`getRowsFromSql(query)`), parameters that are infrastructure types (`Connection`, `HttpRequest`), exceptions that come directly from the library, and returned objects that are your internal mutable classes.

Discipline for a clean API:
1. Name methods by *outcome*, not mechanism: `save(order)`, not `insertIntoOrdersUsingJdbc`.
2. Only cross boundaries with domain types: `Order`, `OrderId`, values — transform DTOs at the edge.
3. Wrap or map library exceptions to domain exceptions.
4. Return unmodifiable/immutable values.
5. Keep the interface small (ISP) — big APIs leak because they imitate internals.

Then *test the API contract* (contract tests) so a developer adding an `@Transactional` annotation or a `public` helper can't silently widen the leak.

---

## Q66: What are the coupling implications of shared mutable singletons?

**A:** A shared mutable singleton (config manager, metrics collector, "current user" holder) is a beacon for coupling. Its state is global, mutable, and implicitly read/written by any module — creating common coupling: invisible dependencies, no interface to see, and every module is affected by its mutation.

Consequences: testing is hard (setup/teardown of global state), concurrency is dangerous, and an individual change in the singleton's behavior silently detours every consumer. Refactoring usually removes mutable globals: (1) seed an immutable snapshot once, inject it explicitly; (2) instance the object and wire it through constructors; (3) if truly one-of, own it in the composition root and inject the instance.

Trade-off: implicit shortcuts are easy but fragile; explicit wiring is verbose but leaves coupling visible and testable.

---

## Q67: What is "temporal coupling" and how do you break it?

**A:** Temporal coupling happens when code must be executed in a specific order for correctness, but nothing enforces it — callers rely on the right sequence by convention.

```java
cache.clear();
cache.populate();   // must run after clear — any caller forgetting clear() breaks outcomes
```

Breaks: split the two steps into *one* operation that is correctly ordered internally (`cache.refresh()`), or define a state machine so the order is structurally enforced. Alternatively, restructure to composable, order-independent functions whose results get combined explicitly.

In APIs, step1(); step2() coupled in time is a smell — a `Session` should manage its own lifecycle rather than exposing telemetry, then connect, then ready as an array of ordering obligations. Temporal coupling is a special case of behavioral coupling: the "order" is a secret the API should encapsulate.

---

## Q68: How should objects share constants or enums without coupling?

**A:** Naively, everyone imports `Constants.STATUS_ACTIVE`, creating a dependency on one bulk constants class — and changing a constant ripples everywhere (though true compile behavior only). Also, a constants jar shared across packages is a coupling magnet.

Better patterns: (1) put the constant/enum with the more important owner — the domain concept, not a dump-bin; (2) use a dedicated, small config/module — if the value changes per-deployment, inject it rather than compiling it; (3) treat shared enums as published contracts: a shared kernel for genuinely cross-team invariants, kept tiny and stable; (4) avoid topic-static imports — they hide coupling.

The key question is *who owns the truth*: one natural owner keeps cohesion (constants used where defined). If everything reaches into one `Constants` hub, that hub is the true owner of nothing — a low-cohesion coupling hub.

---

## Q69: What is "scope creep" in an interface and why does it erode cohesion?

**A:** Scope creep is when an interface grows beyond its core contracts — "need it anyway" methods appended because the interface is already there. `AccountRepository` starts with `findById`, then gains `findByEmail`, `save`, `delete`, `countByStatus`, `mostRecentPurchase`, and then `notifyAccountChanged`.

Cohesion erodes: the interface now serves several stakeholders, so changing accounting behavior affects a caller who only uses listing. Callers also violate ISP — depending on a large interface to use one bit — and stubs grow unwieldy.

Control: define interfaces by *consumer need* ("what does OrderService actually require?") and split on changed axes. Treat added methods as deliberate decisions ("new consumer, new interface"), not as free riders. An interface that grows with every new feature is no longer an abstraction — it's a dumpster lid.

---

## Q70: How do you handle UIs that need many domain details — doesn't encapsulation get in the way?

**A:** There's a real tension: a rich UI needs data across many objects; strict encapsulation says "ask behavior, not data." The resolution is to give the domain a *read-model* for the specific screen.

Options, in order of preference:
1. **View model/DTO assembled by an application service** — the service reads domain state internally (where it has legitimate access) and returns a flat view model the UI renders; the domain stays encapsulated.
2. **Projections** in event-sourced/CQRS systems — a read model dedicated to the screen, kept consistent by events.
3. Careful, purpose-built read methods — intentionally coarse (`getInvoiceSummary()`) rather than exposing wrappers that mirror internals.

The mistake to avoid is exposing every getter ("DTO-ification") so the UI can assemble anything; that turns domain classes into passive bags and users into feature-envy callers. Encapsulation survives by serving *purpose-built* read models instead of raw access.

---

## Q71: What is "feature interaction" coupling and how do you manage it?

**A:** Feature interaction coupling occurs when two otherwise-independent features affect the same state/transaction and interfere. Example: "apply coupon" and "apply loyalty points" both mutate an order's discount — applied in either order, the totals differ; each sees the other's effect.

It's coupling because features are coupled through shared mutable state. Mechanisms to manage: (1) make the shared state a first-class domain concept with rules (`DiscountStack` decides precedence); (2) model effects as composable operations (a pipeline of price transforms) rather than sequential mutations; (3) validate interactions in integration tests, not only the units; (4) define the semantics explicitly — is it compounding, capping, or override?

Untreated, feature interaction is the silent producer of "works in isolation, breaks in combination" bugs. The fix is usually a small but explicitly-owned model of how features compose.

---

## Q72: What is the distinction between "data tibits" vs "behavior" in cohesion?

**A:** Data-only objects (bags of accessors) carry no behavior; behavior-only classes (services with no state) own no data. Each extreme is fragile: data bags leak their fields and impose every accessor on callers; behavior classes tend to reach into foreign data (feature envy), becoming god services.

High cohesion in the ideal: data and the rules that own that data sit together in the same class. A `Cart` that holds items and exposes `total()`, `add()`, `empty()` — unified. Balance the extremes:

- If the data genuinely belongs to the object, put it + its methods together.
- If behavior must coordinate *many* objects, keep it in a service, but pass domain types across clear interface boundaries.

The cohesion litmus: is the `total()` logic in `Cart` or in a vendor's service? Move `Cart`'s invariants where its fields live.

---

## Q73: How do you measure whether decoupling was successful?

**A:** Measure *change* and *testing*, not static metrics alone:

1. **Change-completeness** — changing module X's internals required editing 0 files outside X. Track via the git history of modules moving together (co-change graph).
2. **Independent test run** — module X's suite runs without starting infrastructure or other modules. 
3. **Swap cost** — replacing a dependency (DB, transport, library) touches exactly one adapter file + one composition point.
4. **Fan-in/fan-out ratios** — stable high-fan-in seams, falling coefficients after refactors.
5. **Deploy independence** — modules deploy separately without coordinated downtime.

The read: low coupling is not an aesthetic — it's the ability to change and test *contoured parts* of the system independently. Measure the difficulty of those two operations before and after refactor; if they didn't drop, the decoupling claim is a mirage.

---

## Q74: What is "shy code" and how does it relate to cohesion?

**A:** Coined by Hunt and Thomas (Pragmatic Programmers): shy code is code that "doesn't reveal intimacy of itself and doesn't interfere with others' business." Each module keeps its personal information to itself and only acts on its own requests.

That's the union of encapsulation (don't reveal) and low coupling (don't interfere): a module calls out only when it needs something, and never reaches into another's internals, while internally sharing nothing it doesn't need to.

Shy code, by design, produces high internal cohesion (each module minding its own cohesive business) and loose cross-module coupling. It also makes refactoring safe: you can change a shy module's internals, certain nothing external depends on how it looks inside.

---

## Q75: How do design patterns like Strategy and Template Method trade cohesion for coupling?

**A:** Both split behavior into a composable *shape*. **Strategy** replaces inline conditionals with an injectable function/interface — each strategy is a small, cohesive unit, and clients couple only to the strategy interface, eliminating control coupling. 

**Template Method** locks the algorithm skeleton in a base and defers steps to subclasses — cohesion improves (each subclass implements one step), but subclasses couple to the base's protected API and inherited shape. 

Trade-off sand in practice: Strategy has lower coupling (interface-based, composable at runtime) and higher cohesion per piece, at the cost of indirection — you must wire a `Context` + strategy + implementation. Template Method keeps one obvious home for the algorithm but creates inheritance coupling and is harder to extend without subclass proliferation.

Prefer Strategy by default for variability; Template Method when the skeleton is genuinely fixed and stable, and you want one coherent place for the flow.---

## Q76: How do you apply coupling/cohesion thinking to database schema design?

**A:** The same mental model maps to DBs. *Cohesion* in a table: each table owns a single entity/aggregate; columns belong to that entity — an `orders` table with `customer_name`, `shipping_address`, and `discount_code` columns mixed may trade that string away unless they're genuinely order-owned. Timestamp/audit columns are cohesive within a table.

*Coupling* in the schema: foreign keys, triggers (which cross tables), and shared columns joined across tables. Every FK couples the lifecycle of two tables; triggers and stored procedures can hidden-couple logic across tables.

Historical note: normalized vs. denormalized trade away these lines — normalization reduces write coupling (no redundant updates), denormalization reduces read coupling for the query path at the expense of redundancy (a form of coupling — you must update in N places). Design the schema at the seams of your queries.

---

## Q77: What is the role of a "value object" in reducing coupling?

**A:** Value objects (immutable, equality by value) eliminate a whole class of coupling because they can be shared freely and safely between modules, threads, and tiers. Since they're immutable, nobody can corrupt a shared reference, and since equality is by value, they don't require lifecycle management or identity syncing.

`Money(10, "USD")`, `ZipCode("94704")`, `DateRange(start, end)` — these pass through public APIs without exposing internal mutable state or requiring ordering assumptions. That's the coupling-killer difference between a `Cart` entity (which you must own and mutate via behavior) and a `Money` value (safe to beam anywhere).

By reducing shared mutable state, value objects shrink the interface surface (fewer accessors — a value IS its data), which tightens coupling and raises cohesion: the value encapsulates its own validation and formatting rules.

---

## Q78: How do you use decoupling with a feature-flag system without scattering conditional logic?

**A:** The anti-pattern is distributing `if (featureEnabled("X"))` across code. That couples business code to the flag service, and conditionals make cohesion muddy.

Better: (1) wire the decouple at the composition root — feature-gated sections get different *implementations* behind the same interface (strategy), selected by the flag at bootstrap; (2) for small variants, a provider interface (`getCheckoutStrategy()`) returns the activated variant; (3) keep flags *external* — a config object injected, not a static `FeatureFlags.get()`.

Test and audit benefit: instead of covering N branching combinations, tests cover each variant's implementation. The flag ecosystem becomes data (toggles), not code (if's). This has huge operational payoff — canary rollouts and instant kill-switches don't require redeploying conditionals.

---

## Q79: What is the difference between compile-time and runtime coupling?

**A:** Compile-time coupling is visible to the compiler: imports, superclass references, interface implementations, method signatures. `ClassA` imports and uses `ClassB` — a rename breaks the build. This coupling is explicit, discoverable, and polices by static analysis (ArchUnit, checkstyle, jdeps), the tug you can measure with fan-in.

Runtime coupling is behavioral and harder to see: object graphs, wire protocols, message formats, ordering dependencies, timing. The code might not import each other's types at all — two systems coupled only at runtime via a JSON schema or a queue topic — the compiler can't check it.

The senior move is to *push coupling down the stack*: keep compile-time edges small and architectural, and be very deliberate about runtime contracts (versioned schemas, idempotency, negotiated protocols), because the compiler won't help you when a runtime contract changes.

---

## Q80: How do modules written in different languages stay decoupled?

**A:** They can't reference each other's symbols, so the coupling moves entirely into *shared contracts*: message formats, API payloads, file formats, protocol specs. The disciplines: (1) versioned schemas (protobuf, Avro, OpenAPI) with compatibility checking in CI; (2) capabilities as load-bearing signalled by a language-neutral contract, not by importing each other's code; (3) tolerant readers — readers ignore unknown fields so a producer can evolve without consumer rollouts; (4) consumer-driven contract tests (Pact) so a schema change is verified against its actual consumers.

The physics: cross-language coupling is invisible and runtime-only, so the contract must be treated with the care serialization formats deserve — versioned, documented, tested, and evolved by committee. Done well, independent teams scale freely; done lazily, "it worked in dev" cloud-out resolves into production mishaps.

---

## Q81: What coupling/cohesion advice applies when you're building a test suite for a large monolith?

**A:** Tests inherit geometry from production code. High coupling in the code shows up as: tests that need entire application contexts, shared test fixtures that mutate global state, and ordering-dependent test suites.

Breed better tests by design: (1) test each module against its interface, mocking only the seam — this both verifies the seam (does the mock satisfy the contract?) and validates the module independently; (2) prefer fakes (in-memory repos) over heavy mocks for cohesion-critical units; (3) isolate fixture state — each test builds fresh, small fixtures, no shared mutable "test world." This breaks the "one test that changes everything" mess.

Each test that requires the whole DB is a smoking gun that modules aren't independently testable — which is a coupling report card. Fix the coupling; the test suite simplifies as a symptom of the design improving.

---

## Q82: How do you handle cross-cut modules in a modular monolith (e.g., a shared log, an audit module)?

**A:** A shared log or audit trail is a cross-cutting concern that most modules need. The danger is over-coupling: if every module imports the logging implementation class, or worse, the shared module imports *domain* classes (a hub-and-spoke cosmic), volatility spreads.

Pattern: (1) own the contract in a small, stable core (`AuditLog` interface in the core, injected) — modules compile against the interface only; (2) put the implementation at the edge (infrastructure) wired by composition root; (3) keep cross-cutting changes *source-controlled* — audit events as a schema (event types), not implementation calls.

This converts a volatile, woven cross-cut into a stable seam: each module couples to the log *contract*, not to each other or to the concrete logger, and the audit schema can evolve versioned, backward-compatible.

---

## Q83: What is "cohesion of the change-set" and why is it the best coupling predictor?

**A:** Cohesion of the change-set is the idea that modules that change together, semantically belong. Empirically, the strongest predictor of which files a future change will touch is which files past changes touched. Git's co-change analysis quantifies this: files whose changes co-occur are naturally cohesive.

You apply it diagnostically: run `git log` and cluster files by co-edits. Files always changed together are coupled — either fine (they're genuinely one feature) or a bug (they're entangled but separable responsibilities). Split the co-changing cluster by responsibility when it's actually several concerns.

Also predictive for risk: coupling measured by co-change predicts defect rates better than static metrics — a file that statistically changes with five others is where your next regression will land.

---

## Q84: How does coupling affect performance and concurrency?

**A:** The relationship is indirect but real: (1) shared mutable state — a coupling magnet — is the #1 source of concurrency bugs and lock contention; decoupling by sharing less (value objects, message passing) removes those locks; (2) coupling to the wrong persistence granularity causes long transactions or too many round-trips (a form of coupling to schema, seen in the N+1 problem); (3) a model that couples entities tightly (unified aggregates, singletons) reduces parallelism — you can't work on them concurrently.

Payoff read: decoupling is often the cheapest scalability lever available. Message-passing concurrency, immutable shares, and vertical partitioning all hinge on the same principle — stop sharing mutable state, stop depending on its order — and they scale far better than lock-stravagant systems.

---

## Q85: How do you refactor a codebase that is simultaneously tightly coupled AND poorly cohesive?

**A:** This is the hard case: modules are tangled and each is a grab-bag. Attack with a specific order:

1. **Map the tangle**: name the responsibilities (grep for what changes together; list every package a class imports).
2. **Pick seams, not re-architect everything at once**: extract one cohesive class per responsibility, one at a time, keeping behavior identical (the Strangler/Technical Steps — every refactor step still passes tests).
3. **Introduce interfaces at the extraction points** so the new cohesive pieces couple only to contracts.
4. **Break ordering/temporal coupling as you notice it** — those are cheap quality wins.
5. **Verify with metrics after each increment**: fan-in/fan-out, re-co-change counts.

The order matters: establish *cohesion* first (extract clean units), then decouple them (interfaces, adapters). Cutting coupling while everything's a tangled god-class is like untangling knots without separating the ropes. Add composition root + contract tests last to lock the new shape in.

---

## Q86: What is the "dependency direction" guideline and how does it relate to coupling and cohesion?

**A:** In layered design, dependencies should point "inward" — toward stable, abstract, domain-level things — never outward toward volatile infrastructure. This is the Stable Dependencies Principle in action: leaders depend on actions, not vice versa. Your domain layers (high cohesion, no infrastructure imports) must not import from UI or DB.

Coupling quality: your *core* (stable, cohesive) is the least likely to change; anything that couples to it is safe because the downstream is stable. Your *edges* (UI, DB, integrations) are likely to change; coupling to them is dangerous.

This explains why, in well-designed systems, domain, application, and infrastructure live in nested layers with unidirectional arrows — a graph in which the domain is a sink, not a source. If you find your domain importing a `JdbcTemplate`, you've inverted the direction — that's both a cohesion and a coupling violation at once.

---

## Q87: What are "data shards" or "hotspots," and how does coupling assessment find them?

**A:** Data hotspots are methods/classes with unusually high change frequency and defect density. Coupling assessment (fan-in, co-change, defect-correlation graphs) locates them: a hotspot typically has high fan-in (many modules depend on it) or high fan-out (it depends on many), and co-changes with many other files — often *despite* advertised encapsulation.

Think idempotent patterns: an "OrderValidator" that absorbs every rule tweak, an over-used "User service" where every team adds a method. 

The senior play on a hotspot: (1) find it via the metrics toolchain — not guesses; (2) shrink its dependencies by extracting the coalescing responsibilities; (3) add dedicated contract tests so the hotspot's volatile parts get isolated churn from consuming teams; (4) measure again after refactor — confirmed success is a falling co-change/hotspot score.

---

## Q88: How do you model "boundaries" with coupling/cohesion in mind — package boundaries, layer boundaries, system boundaries?

**A:** Every boundary is a dividing line tuned by the two principles:
- **Package boundary**: keeps cohesive units (cohesion per package) with minimal exported surface (low coupling).
- **Layer boundary**: stable interfaces (domain layer) with volatile ones (infra) below, dependency arrows inward, per domain.
- **System/service boundary**: versioned contracts; as files in the same repo go independent deployable units, the *contracted* interface becomes the key coupling point — everything else is internal and decoupled.

Evaluate each boundary with "what changes together" test: parts that change together belong in the same boundary; parts that change for different reasons lie differently across it. And never draw a boundary without asking what contract takes shape across it, since boundaries that leak internals are decorative at best.

---

## Q89: What is "interface-driven design" and what does it do for coupling and cohesion?

**A:** Interface-driven design means defining the abstraction a client needs *first*, then building the implementation behind it. Client → interface (consumer-owned contract) → implementation. Coupling drops because the client couples only to the contract (and can swap implementations). 

Cohesion survives because each interface narrows to one client purpose (ISP) — instead of one god interface serving all, each client gets a focused slice. You end up with `OrderReader`, `OrderWriter`, not a monolith `OrderManager`.

And the contract test comes along as a bonus: since the interface is consumer-defined, you can test that implementations faithfully serve it, which validates seam quality continuously. Interface-first forces naming around outcomes ("what the client needs") rather than mechanics — the vocabulary of design-by-contract.

---

## Q90: How do you apply coupling/cohesion ideas in a large framework-based system (Spring, .NET Core)? 

**A:** Frameworks give you magic, but magic hides edges — frameworks are where decoupling discipline is most tested. Principles:

1. Let the framework *call you* (composition root, dependency injection), rather than reaching into framework internals everywhere.
2. Keep domain code framework-free — if your `Order` class references `@Entity`, `IServiceCollection`, `HttpRequest`, your domain is coupled to the framework's volatility. Put framework types at the edges of adapters, DTO-zing through the seam.
3. Respect framework lifetimes (scoped/singleton) — a singleton that captures a request-scoped dependency is runtime coupling in disguise (a behavioral/correctness bug that only occasionally fires).
4. Treat framework upgrades as boundary work: keep a thin adapter surface so the majority of code is framework-agonistic.

The goal: framework changes (version bumps, alternative frameworks) should be cheap *precisely because* the coupling was concentrated deliberately at the boundaries.

---

## Q91: What is the "principle of least privilege" as applied to object design, and its effect on coupling?

**A:** Least privilege for objects means: give each object exactly the access it needs — no more. Applied to method signatures: `process(Order order, Money amount)` rather than `process(FullProcessingContext ctx)`. To collaborators: narrow interfaces, `readReviews()` when the consumer only reads, not a full `ReviewService` with mutators.

Coupling effect is immediate: a parameter that carries 15 fields couples the caller to a 15-field construct — even when it needs 2. Least-privilege signatures (data coupling) shrink that to exactly the needed units, so changes to unneeded fields never touch the consumer.

It's the encapsulation ethic applied to granularity: state the minimum contract, hide everything else. This also reduces testing burden (no fake 15-field context) and makes reasoning about object boundaries straightforward and predictable.

---

## Q92: How do frontend and backend teams decouple from each other's releases?

**A:** Decoupling releases means neither side must deploy in lockstep. The enablers are versions-tolerant contracts: (1) **backend-first**: the API/contract is the publication; frontend consumes versioned endpoints — backend can add fields without breaking old clients; (2) **tolerant reader on the frontend**: parse defensively, ignore unknown fields; (3) **contract tests** (Pact/Playwright contract mode) running in each repo's CI so the other side doesn't deploy blind; (4) **feature flags** so UI can roll out independently of server capability; (5) **backward-compatible defaults** in the API so new fields are optional.

The decoupling intent: either team can release during their own cadence. Contracts make coupling explicit and safe; the other side never has to sync-deploy. When contracts break (renames, removals), the breaking side coordinates ahead of its release.

---

## Q93: What is "hidden coupling" and give examples of where it hides?

**A:** Hidden coupling is dependencies you can't see from reading the code — the compiler doesn't show it, grep may not either, so it goes untracked.

Examples: (1) **database schemas**: two modules implicitly coupled via a shared table's columns; (2) **message formats**: producers and consumers coupled through a JSON shape that neither imports; (3) **ordering conventions**: calling "clear" then "populate" relies on sequence only documented in lore, not in type; (4) **global/thread-local state**: ambient coupling by reading "current user" or "current transaction" from context; (5) **config files**: runtime values learned through shared properties or environment.

You surface hidden coupling with contract tests, schema change reviews, and runtime topology monitoring. The teaching: coupling with no enforcement is a time bomb — make the implicit protocol explicit (schema, tests, state machines), or it will detonate at deploy time with no stack trace in sight.

---

## Q94: What is degeneracy in cohesion: when high cohesion is actually a code smell?

**A:** Sometimes a class is *too* cohesive — it has one heavy responsibility but owns too much surface for it. Symptoms: 500-line "one-responsibility" class with 30 methods; a `FileManager` that is single-purpose ("manage files") but handles every file operation in the system; a service with 15 private helpers, all serving one job, yet impossible to maintain because the job is too big.

A sort of "rabbit hole": heightened cohesion in a class that's actually *one aggregate responsibility* — the class has become a de-facto subsystem. Diagnosis: split the subsystem into "sub-cohesive units" (the job decomposes into steps each with its own purpose) while preserving the composition that still is its one duty. The single-sentence description must still hold — "manages files" — but file-stream handling, path resolution, and integrity checking are better as composed pieces.

---

## Q95: How do you ensure that module-level decoupling doesn't kill valuable sub-system cohesion?

**A:** Balance requires respecting both axes: modules decouple *from each other* while anything that *must change together* stays together *within* a module. The destructive extreme is fragmentation: splitting a coherent subsystem into many modules because "low coupling everywhere!" — now every implementation detail is spread across packages, coupling floats up exactly where it was most wanted to be contained.

Pillars: (1) define module boundaries by change-cohesion (what changes for a shared reason belongs in one place); (2) keep innards cohesive and only expose a small stable API; (3) allow *internal* coupling within cohesive modules to stay — the binding allowed by high cohesion; (4) let the composition root swap whole modules (whole-subsystem reuse) rather than micro-pieces.

Decoupling should be chosen based on which readers benefit, not from the aesthetics of no-import-anywhere. Even a tightly-coupled pair is fine if it's one *cohesive subsystem* at the right boundary.

---

## Q96: How does the "law of least astonishment" interact with encapsulation and coupling?

**A:** Least astonishment says: code should behave as callers expect. Encapsulation supports it by hiding surprising, case-specific details (a `getOrDefault` that has a side effect is astonishing). Coupling frames it too: astonishment often arises when a caller meets unexpected behavior because one module reached into another's innards.

The least-astonishing design: behavior belongs to the object that owns the state; the caller expresses intent, and the object behaves predictably. That reduces surprise coupling — the dotted chain from one module into another's internals.

It also guides the called side: design public methods to be safe regardless of caller state (no getters that secretly mutate, no setters that reject only after violations). Predictable contracts lower the cognitive load of coupling and make the seams reliable.

---

## Q97: What is "internal cohesion by interface" and its trade-offs?

**A:** Internal cohesion by interface — organizing code *around interfaces* so the pieces that implement them cluster together — expresses cohesion structurally. When you see `interface OrderRepository` next to `Order`, and `JpaOrderRepository` implemented close by, the codebase reads as a cohesive "order" capability.

The trade-off: a rule that "every class must have an interface" pushes fire-fighting features into whichever class implements the nearest abstraction ("interface gravel sprinkled everywhere"). Interfaces then become hollow mirrors of reality — a set of pairs that nobody swaps — and cohesion suffers because the implementation concern is spread across many small, arbitrary splits.

The balance: keep interfaces where they represent a real abstraction boundary or a genuine point of variation (persistence, messaging, external APIs); skip them for single-implementation internals and rely on packages and names to express cohesion instead.

---

## Q98: How do you deal with "god service" anti-pattern in microservices?

**A:** A god service is a microservice that quietly became a god module — one business axis, but internally overloaded: too many endpoints, too many responsibilities, too many downstream dependencies. Signs: 40 endpoints, 30 tables, every other service calls it, deploys cause cascading failures.

Remedies: (1) analyze coupling and cohesion *inside* the service (apply the same tools at a bigger scale) — split by co-changing subdomains into proper services; (2) put the coordination logic in a facade with a narrow contract — callers couple only to that; (3) promote genuinely shared capabilities to their own service instead of accumulating them in one place; (4) treat the god-ness as measured debt: extract one cohesive subdomain, wire it, and monitor which cross-service changes still ripple together.

The pattern repeats at every scale: the same coupling analysis that spots god classes also finds god services — the fix is the same, just at a bigger boundary.

---

## Q99: What is the "seam" concept in software design, and why is it central to decoupling?

**A:** A seam is a place where you can alter behavior without editing that place itself — a boundary where you can plug something different in: a constructor parameter, an interface, a service locator, a DI binding, a message queue, a delegation point. Seams and coupling are two sides of one coin: coupling lives between modules; a seam is where that coupling is made *actionable* (you can change what's on the other side without editing this side).

Meaningful seams are the practice of encapsulating variation: a DI binding ("inject any `MessageSender`") is a seam; a hard-coded import of `ConcreteSmtpSender` is a non-seam (you'd have to edit this file to change the sender). High coupling = few good seams; low coupling = many well-placed seams.

To decouple, your main job is *finding and widening the seams* — the points where variance is allowed — then keeping implementation churn inside those seam boundaries. This is why interface-first design is suspect: it's unknown-ing the seam list proactively.

---

## Q100: What is the ultimate way to check whether your system maintains low coupling and high cohesion?

**A:** The definitive test is the *change test*: pick four unrelated one-dimensional changes and time/measure how many modules (and how many files outside the one you intend) you had to touch, how many tests had to change, and how long the deploy took:

1. Change a database storage engine column type: expected — one repository/file + its tests.
2. Add a new notification channel: expected — one new class + re-register in composition root.
3. Change business pricing rule: expected — the owning domain class + its tests only.
4. Rename a concept (Customer → Account): expected — bounded refactor, not showing real ripple.

If these change-tests stay small and isolated, your system is genuinely low coupling and high cohesion — metrics corroborate, but behavior confirms. Senior precision: design along axes of statistically independent change. That's the actual objective of everything covered in this file: making change cheap, local, and safe.