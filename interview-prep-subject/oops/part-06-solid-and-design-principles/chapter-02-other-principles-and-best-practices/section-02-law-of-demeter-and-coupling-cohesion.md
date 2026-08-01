# Law of Demeter and Coupling/Cohesion

> **TL;DR**: The Law of Demeter says a method should only talk to its immediate collaborators (no `a.b().c().d()` train-wrecks); coupling (inter-module dependence) should be minimized, cohesion (intra-module togetherness) maximized — the two axes under every design principle.

## 1. Why Does This Exist?
A method that reaches through one object into its collaborators' collaborators (`order.getCustomer().getAddress().getCity()`) makes the *caller* know the whole navigation graph. When `Address` changes, every code path that navigates to it must be found and fixed — and worse, the caller is *silently coupled* to a chain of objects it doesn't own. The Law of Demeter exists to **cap navigation depth**: talk only to (1) your own fields, (2) your parameters, (3) objects you create, (4) your own object. This keeps each unit's knowledge *local*. Coupling and cohesion are the *metrics* behind that: **coupling** = how interdependent modules are (high = fragile, hard to change/test); **cohesion** = how much a module's parts belong together (high = focused, reusable, easy to reason about). Every principle you've learned — SRP, ISP, OCP, DIP, composition-over-inheritance — is a *mechanism* to reduce coupling and raise cohesion. These two axes are the measurable essence of "good design."

## 2. How Does It Work?
**Law of Demeter (LoD)**: a method `M` of object `O` may call methods only on:
1. `O` itself (`this`),
2. `M`'s parameters,
3. objects `O` *creates* (local `new`),
4. objects stored in `O`'s *own* fields.
It must NOT call methods on objects *returned by* the above (no transitive navigation). In practice: `a.b().c().d()` is a violation; the fix is to ask the *first* object to do the work (`a.doSomething()` or `a.getD()`) so the caller only knows `a`.
**Coupling/Cohesion**:
- Coupling: count/strength of arrows between modules (fewer, weaker = better). Types: content (worst — reaches into internals), common (shared globals), control (passes flags), data (passes only data — best).
- Cohesion: how related a module's members are (functions operating on the same data = high; a grab-bag of unrelated functions = low). Ideal: **low coupling, high cohesion** — modules that are self-contained yet minimally dependent.

## 3. When Is It Used?
- **LoD**: whenever you see a chain of getters (`getX().getY().getZ()`), in layered refactors (the "Tell, Don't Ask" reframing), and in "is this method's knowledge too broad?" reviews.
- **Coupling**: choosing between passing data (good) vs passing the whole object (bad — couples to its API); deciding whether to use an interface (reduces coupling to concrete); evaluating shared globals/static state (coupling smell).
- **Cohesion**: splitting a god class (raise cohesion by giving each responsibility its own home — SRP); deciding if two methods belong in the same class (same data → same class).
- **Not dogmatically**: fluent builders, value objects, and `Optional` chains deliberately use chaining and are *not* LoD violations (see trap). LoD is a *coupling* heuristic, not a ban on method chains.

## 4. Why Wasn't Another Approach Chosen?
- *Why cap navigation at one hop?* Each hop adds coupling to a foreign object's *shape*; two or three hops, and the caller is coupled to the whole object graph — every structural change ripples broadly. Capping at immediate collaborators keeps change *local*.
- *Why "tell, don't ask" instead of just getters?* Demeter's sister principle: instead of *asking* (`getStatus()` then deciding), *tell* the object to act (`handle()`). Asking exposes internals and pushes logic into callers (feature envy smell); telling keeps knowledge in the object that owns it — which *raises cohesion*.
- *Why minimize coupling rather than eliminate it?* Zero coupling is impossible (modules must interact) and undesirable (everything in one giant class = maximal cohesion failure). The goal is *minimal essential* coupling — the fewest, weakest arrows that still let modules cooperate.
- *Why maximize cohesion?* Cohesive modules are internally consistent (easy to understand), independently testable, and reusable; low cohesion spreads each change across unrelated code (shotgun surgery smell). Cohesion is the "self-contained" half of maintainability.
- *Why not just count lines or use static analysis?* Metrics like LCOM (Lack of Cohesion of Methods) and dependency graphs *formalize* the intuition, but they're heuristics — a low-coupling/high-cohesion numeric profile is a *signal* to inspect, not a verdict.

## 5. Intuition
**LoD**: don't ask your friend to get you a favor from *their* friend. You only ever talk to your own friends (fields/params); a phone chain through strangers means you depend on people you've never met. **Tell, don't ask**: instead of interrogating someone ("what's your status? what would you do?") just *ask them to do it* — they know best how to handle their own state.
**Coupling/Cohesion**: coupling is how many strings are tied between packages; cohesion is how tightly a package's own contents are bound. A good unit: few strings out (low coupling), contents tied together (high cohesion). The worst design: a class that knows everything about many others (high coupling) while its own methods barely relate (low cohesion) — the god class.

## 6. Real-World Analogy
**LoD**: at a company, you don't ask the receptionist to fetch the CEO's assistant's schedule to book your meeting — you ask the receptionist (your contact) and they handle it. If you had to know the receptionist → assistant → CEO chain, any reorganization (new assistant) breaks your process. Demeter keeps you talking only to your direct contact.
**Coupling/cohesion**: a **modular kitchen**. High coupling = the fridge's door is wired to the oven's timer (change one, break the other). Low coupling = each appliance has a power plug (standard interface, independently swapped). High cohesion = all the knives live in one block (related things together); low cohesion = one drawer holds knives, rubber bands, and takeout menus (unrelated things mixed — you hunt through it constantly). Kitchen design wants: plug-in appliances (low coupling), organized drawers (high cohesion).

## 7. Formal Definition
**Law of Demeter** (Ian Holland, Northeastern, 1987): a method `m` of class `C` may only send messages to objects that are: (1) `C` itself (`this`), (2) `m`'s arguments, (3) objects created locally within `m`, (4) objects stored directly in `C`'s fields, or (5) global objects (discouraged). Equivalently: a method must not call methods on objects *returned by* other calls (no `a.b().c()`). Purpose: minimize the coupling of a method to the structural *shape* of other objects.
**Coupling**: the degree of interdependence between software modules — measured by the number and strength of connections (types of references, data vs control vs content). Lower coupling → easier to change, test, and reuse a module in isolation.
**Cohesion**: the degree to which a module's internal elements belong together (operate on shared state/data, express one concept). Higher cohesion → easier to understand and maintain. Optimal design: **low coupling, high cohesion**.

## 8. Example
```java
// LoD VIOLATION: train-wreck navigation
String city = order.getCustomer().getAddress().getCity();   // talks to customer AND address (strangers)
// LoD FIX: ask the immediate collaborator to expose the needed fact
String city2 = order.getCustomerCity();                     // Order knows how to answer; caller knows only order

// Better still — Tell, Don't Ask (raise cohesion):
order.shipToAddress();                                       // Order handles its own shipping logic

// COUPLING smells:
class OrderServiceNaive {
    String generate(Customer c) { return c.getName() + ":" + c.getPlan().getTier(); }  // high coupling: knows plan internals
}
class OrderService {
    String generate(Customer c) { return c.describeForInvoice(); }   // low coupling: only the contract
}
// COHESION:
// LOW cohesion — unrelated responsibilities, shared class
class Utils { void formatDate(); void sendEmail(); void computeTax(); }     // grab-bag → split
// HIGH cohesion — same concept, shared state
class Temperature { double c; double toF() { return c*9/5+32; } double toK() { return c+273.15; } }  // all about temperature
```

## 9. Internal Working
1. **LoD detection**: scan for chains — `x.y().z()`, `getA().getB()` — and calls on *returned* objects. The deeper the chain, the more objects the caller is coupled to (its dependency count grows with the chain length).
2. **LoD fix**: add the operation to the *immediate* collaborator (the object the caller already knows), so the caller's coupling stays constant; the collaborator internally navigates (its own coupling is contained where it belongs).
3. **Coupling measurement**: enumerate each module's imports/field types/parameter types (static analysis gives a dependency count); flag types that reference many others, or modules referenced by everything (the "hub"). Weak coupling: depend on interfaces/data, not internals/concrete classes.
4. **Cohesion measurement**: LCOM (Lack of Cohesion of Methods) counts method-pairs that don't share fields — high LCOM = low cohesion; group methods by the fields they touch, split classes so each group owns its data.
5. **Refactor loop**: LoD violations usually accompany low cohesion (feature envy) — fixing both means moving behavior to the object that owns the data (higher cohesion, shorter chains, fewer couplings).

## 10. Time Complexity
- Zero runtime cost — all three are structural/design disciplines.
- Maintenance economics: each coupling is a potential edit point and recompile; each cohesion gap is a scattered change (shotgun surgery). Low coupling/high cohesion converts "change ripples everywhere" into "change is local" — a *developer-time* saving that dominates.
- LoD violations also add *defensive* cost: each navigated object may be null, so callers add null-checks (`getCustomer()` may be null → `.getAddress()` NPE). Fewer hops = fewer null-guards.

## 11. Advantages
- **LoD**: local knowledge → fewer affected files per change; fewer NPEs (less navigation); clearer interfaces (callers see one method, not a graph); forces good encapsulation ("ask, don't dig").
- **Low coupling**: modules change/test/reuse independently; parallel development; swap-ability.
- **High cohesion**: focused modules are self-documenting, independently testable, and reusable; each change stays in one place.

## 12. Disadvantages
- **LoD over-applied**: "wrapper fever" — adding a method to *every* object just to hide a one-line navigation; verbose delegation with no benefit; the law is a heuristic, and dogmatic application bloats APIs.
- **Low-coupling over-applied**: every module wrapped in interfaces and DTOs "just in case" — indirection without coupling reduction (YAGNI).
- **High-cohesion over-applied**: over-splitting a genuinely cohesive class into fragments (LCOM-focused splitting can tear apart one concept).
- **Rule tension**: "tell, don't ask" conflicts with pure value objects (which legitimately expose data) — a `Money` object *should* expose `amount()`; don't force it to "do things."

## 13. Interview Questions
1. **Q: What is the Law of Demeter?** A: A method should only talk to its immediate collaborators — its own fields, its parameters, objects it creates, and itself — never to objects *returned* by those (no `a.b().c()` chains).
2. **Q: Give a violation and fix.** A: `order.getCustomer().getAddress().getCity()` violates it (talks to `customer` and `address`, strangers). Fix: `order.getCustomerCity()` — the `Order` owns the navigation; the caller knows only `order`.
3. **Q: TRICKY — Is `list.stream().map(...).filter(...).collect(...)` a violation?** A: No — chaining methods that all *return from the same original object's API* (the stream abstraction) isn't navigating into *different* objects' collaborators. LoD targets *transitive object navigation* (`a.getB().getC()`), not method chains on a cohesive API. Similarly, fluent builders and `Optional` chains are fine.
4. **Q: What are coupling and cohesion?** A: Coupling = interdependence between modules (lower = better); cohesion = how related a module's own parts are (higher = better). The ideal design has low coupling and high cohesion.
5. **Q: SCENARIO — A class `Report` reaches into `config.getDb().getConn().getSchema()`. What's wrong?** A: It violates LoD (talks to db, conn, schema — strangers) and has high coupling to the config/db graph; a change to any hop breaks the report. Fix: `config.schemaName()` (or have Report receive what it needs via parameters — a DTO of the facts).
6. **Q: PRODUCTION — "Tell, Don't Ask" — what does it mean concretely?** A: Instead of *asking* for state then deciding (`if (acc.getBalance() > 100) acc.debit(100)`), *tell* the object (`acc.withdrawIfPossible(100)`) — the decision lives where the state lives. This raises cohesion (methods + their data together) and cuts coupling (caller doesn't know the policy).
7. **Q: TRICKY — Is high coupling ever fine?** A: Yes, within a cohesive unit — the *implementation* of a class is naturally coupled to its own helpers (that's cohesion); coupling is judged *between* independently-changeable units. Also, unavoidable coupling (to a stable JDK API) is harmless; coupling to *unstable* or *foreign* units is the risk.
8. **Q: How do you measure coupling/cohesion?** A: Coupling: dependency counts (imports, field/param types, references) and fan-in/fan-out (who depends on me / I depend on). Cohesion: LCOM (pairs of methods sharing no fields — high LCOM = low cohesion); or the "could this live as a separate unit?" judgment.
9. **Q: SCENARIO — Refactor `a.b().c().d().doWork()`.** A: (1) Ask what the caller *wants* (a result). (2) Add `doWork()` (or a named query) to `a` — the object the caller already holds. (3) `a` internally does whatever navigation it needs. Result: caller's coupling constant, the navigation contained where its knowledge belongs.
10. **Q: PRODUCTION — Why does a deep getter-chain predict NPE bugs?** A: Every hop can be null, so `a.getB().getC().getD()` needs guards at every step — each missed guard is an NPE in production. LoD fixes the *shape* (fewer hops, fewer null-checks) and pushes null-handling into the one place that knows the invariant.
11. **Q: TRICKY — LoD vs a "value object" that exposes data.** A: Value objects (immutable data carriers like `Money`, `Address`) legitimately expose their data — they *are* the data; "telling" them to do things is forced. LoD is about *navigation between domain objects*, not about never returning simple data. Don't dogmatize it onto value objects.
12. **Q: How do coupling/cohesion relate to the four pillars and SOLID?** A: Encapsulation (Part 02) *is* the mechanism for low coupling (hide internals). SRP/ISP raise cohesion (split by responsibility/role). OCP/DIP lower coupling (depend on abstractions). Composition-over-inheritance lowers coupling (delegation via narrow seams). All roads lead to low coupling + high cohesion.
13. **Q: SCENARIO — Two modules both read a global config `AppConfig.getInstance()`. Problem?** A: *Common coupling* — both depend on a shared global; changing its shape breaks both, and testing is tangled (the global is hard to substitute). Fix: pass the config in (data coupling — the weakest, best kind), or inject it via DI.
14. **Q: PRODUCTION — What's the practical review heuristic?** A: For each method: "which objects does it *know about* that it has no business knowing?" — the answer is a coupling leak. For each class: "does every method belong with this class's data?" — if not, extract (cohesion). Keep chains ≤ 1 hop unless the hop is a value object; keep dependency graphs shallow and acyclic.

## 14. Follow-Up Questions
1. **Q: What is "feature envy"?** A: A code smell where a method spends more time using another class's data/getters than its own — it *envies* the other class (low cohesion in the host, high coupling to the target). The refactor: move the method to the class whose data it uses — raising cohesion and shortening chains (the smell that LoD/cohesion explicitly target).
2. **Q: LoD vs the "facade" pattern?** A: The Facade *is* an LoD tool at a larger scale: it gives a caller a single entry point to a subsystem instead of forcing it to navigate the subsystem's many classes — the "don't talk to strangers" rule applied at subsystem boundaries.
3. **Q: How does DDD's "aggregate root" relate to LoD?** A: The aggregate root *is* the LoD rule for persistence: external objects may only reach the aggregate's members *through the root* — no navigating `order.getItems().get(0).getProduct().getPrice()` directly; you ask the root. DDD formalizes Demeter as the aggregate pattern.
4. **Q: Can tools enforce LoD/coupling/cohesion?** A: Static analyzers (ArchUnit in Java, custom lint rules, `jdepend`/`radon` for metrics) flag chains, dependency cycles, and LCOM; they're guardrails — the judgment of *which* coupling matters (and which chains are fine) is still human.

## 15. Coding Example
```java
// BEFORE: LoD violation + low cohesion + high coupling
class Customer {
    Address getAddress() { return address; }
    private final Address address;
}
class Address { String getCity() { return city; } private final String city; }
class Order {
    Customer getCustomer() { return customer; } private final Customer customer;
}
class Shipping {
    String label(Order o) {
        // talks to customer AND address (strangers) — 3 hops, 3 null risks, high coupling
        return o.getCustomer().getAddress().getCity();
    }
}
// AFTER: tell, don't ask — knowledge stays with the data owner (high cohesion, low coupling)
class Order {
    private final Customer customer;
    String getCustomerCity() { return customer.getCity(); }   // Order owns the navigation (its own coupling)
}
class Customer {
    private final Address address;
    String getCity() { return address.getCity(); }            // Customer owns ITS navigation
}
class Shipping {
    String label(Order o) { return o.getCustomerCity(); }     // caller knows only Order — 1 hop
}
```
The caller's coupling dropped from 3 objects to 1; the navigation lives where the knowledge lives (cohesion up); null-risk localized. Same behavior, far less fragility.

## 16. Industry Usage
- **DDD**: aggregate roots enforce Demeter at persistence boundaries; repositories are the only "coupling point" to storage.
- **Spring**: DI *lowers coupling* structurally — controllers depend on interfaces, not concrete factories; a bean graph that's shallow and acyclic is the maintainability ideal.
- **Java static analysis**: ArchUnit (dependency rules in tests), `jdepend` (package coupling metrics), PMD/Checkstyle (LCOM, deep chains) ship these heuristics as CI checks.
- **Clean Architecture**: the dependency rule (arrows point inward) is the *architectural* form of low coupling; use-case layers keep cohesion by grouping by business capability.
- **Fluent APIs (Guava, Streams, builders)**: deliberately break LoD's letter (chaining) while preserving its spirit — the chain never leaves a single cohesive abstraction, so coupling stays bounded; a good exam case for *when* LoD doesn't apply.

## 17. References
- Ian Holland / Karl Lieberherr, "The Law of Demeter" (1987) — original formulation.
- Robert C. Martin, *Clean Code* — "The Law of Demeter" chapter (train-wreck examples).
- Meilir Page-Jones, *The Practical Guide to Structured Systems Design* — coupling/cohesion taxonomy.
- Martin Fowler, *Refactoring* — Feature Envy, message chains, middle man (the smells).
- ArchUnit (Java architecture testing): https://www.archunit.org/

## 18. Cheat Sheet
- LoD: talk only to `this`, params, your created objects, your own fields.
- No `a.b().c()` transitive navigation — 1 hop max.
- Fix: add the operation to the object you already hold (Tell, Don't Ask).
- Fluent chains/builders/value objects are NOT violations.
- Coupling: inter-module dependence — lower is better.
- Coupling types: data (best) < control < common/global < content (worst).
- Cohesion: intra-module togetherness — higher is better (LCOM lower).
- Ideal: low coupling, high cohesion (the god class is the worst of both).
- Feature envy = low cohesion + high coupling symptom; move the method.
- DDD aggregate roots and Facade are LoD at scale.

## 19. Quiz
1. LoD says a method may not call methods on: a) its fields b) objects returned by calls c) its params d) itself → **b**
2. `order.getCustomer().getAddress().getCity()` is a: a) fluent chain b) train-wreck c) builder d) stream → **b**
3. Ideal module profile: a) high coupling, low cohesion b) low coupling, high cohesion c) high both d) low both → **b**
4. Passing a flag to control behavior = which coupling? a) data b) control c) content d) none → **b**
5. Feature envy means a method: a) uses another's data too much b) is too long c) returns null d) is static → **a**
6. True or False: Fluent builders violate LoD. → **False** (chains on a cohesive API aren't transitive navigation)

## 20. Flashcards
- **Q: Law of Demeter?** → **A:** Talk only to your own fields/params/created objects — never to returned objects' collaborators.
- **Q: Train-wreck example?** → **A:** `a.b().c().d()` — fix by adding the op to `a`.
- **Q: Coupling/cohesion ideal?** → **A:** Low coupling, high cohesion.
- **Q: Feature envy?** → **A:** Method using another class's data — move it there.
- **Q: When is chaining OK?** → **A:** Fluent/stream chains within one cohesive abstraction.

## 21. Revision
The Law of Demeter caps navigation: a method talks only to its own fields, parameters, created objects, and itself — never to objects *returned* by those (`a.b().c()` train-wrecks). Fix by "tell, don't ask" — move the operation to the object you already hold, so coupling stays local and cohesion rises. Fluent builders, streams, and value objects are legitimate exceptions (chains within one cohesive abstraction). Coupling (inter-module dependence — lower better; data coupling is best, content/global worst) and cohesion (intra-module togetherness — higher better; LCOM measures it) are the two axes under every principle; the god class is the worst of both worlds, and feature envy is the classic symptom. DDD aggregate roots and Facades apply Demeter at scale. First-30-seconds answer: "A method only talks to its immediate collaborators — one hop, no `a.b().c()`; and the design ideal is low coupling, high cohesion."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Law of Demeter?" | Interview Q1 / Section 2, 7 |
| "Violation and fix?" | Interview Q2 / Section 8 |
| "Is a stream chain a violation?" | Interview Q3 / Section 13 |
| "Coupling and cohesion?" | Interview Q4 / Section 2, 7 |
| "Tell, Don't Ask?" | Interview Q6 / Section 4 |
| "Measuring coupling/cohesion?" | Interview Q8 / Section 9 |
| "Deep getter chain + NPE?" | Interview Q10 / Section 9 |
| "Feature envy?" | Follow-up Q1 / Section 14 |
