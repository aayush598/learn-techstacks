# Association, Aggregation, and Composition

> **TL;DR**: Association (knows-about) is the umbrella term for has-a links; aggregation is a *shared* has-a where parts outlive the whole (open diamond in UML); composition is *owned* has-a where the whole owns the part's lifecycle (filled diamond); dependency is the weakest "uses" link. The aggregation-vs-composition distinction is purely about ownership.

## 1. Why Does This Exist?
"Has-a" is not one thing. When object A holds a reference to B, the *strength of that link* determines who is responsible for B's lifecycle, whether B can be shared, and what happens when A dies. If you code every link the same way — a plain field, a `new`, a getter — you can't answer: "should `Driver` survive `Car`'s deletion?" or "may two `Car`s share the same `Wheel`?" The relationship taxonomy exists to make those decisions **explicit and load-bearing**: it's the difference between a dangling reference, a memory leak, and correct ownership in C++; in Java it governs what the GC collects and when; in design it decides whether a component is reusable. Vocabulary exists so engineers can say "compose the engine, aggregate the tires, associate with the driver" and mean three *different* engineering decisions.

## 2. How Does It Work?
Four kinds, weakest to strongest:
- **Dependency (uses-a)**: A uses B briefly — a parameter, a local, a static call. No field. `order.totalWith(discount)`. In UML: dashed arrow.
- **Association (has-a / knows-a)**: A holds B as a field — but no ownership: both can exist and be deleted independently. `Driver.license`. In UML: plain line.
- **Aggregation (weak has-a)**: a field where the part *can* outlive the whole and be shared; the whole doesn't own the part's creation/destruction. `House → Furniture`. In UML: open diamond on the whole side.
- **Composition (strong has-a)**: the whole owns the part — it creates the part, and when the whole dies, the part dies with it; the part has no independent existence. `House → Room`. In UML: filled diamond on the whole side.

In code the difference shows up as *who calls `new`* and *who holds the strong reference*: composition = `new Room()` inside `House`'s constructor; aggregation = `House(Furniture f)` receives the furniture from outside.

## 3. When Is It Used?
- **Dependency**: utility calls, one-off helpers (`Collections.sort`), parameters, DI-ignored temporaries.
- **Association**: any knowledge link — a `Customer` knowing its `Address`, a `Controller` knowing its `Service`.
- **Aggregation**: shared/reusable parts — a `Team` of `Player`s (players also exist on other teams), a `Document` with fonts/styles shared across documents, an `Order` referencing a shared `Customer`.
- **Composition**: whole-part with no independent part — `Car`→`Engine`, `House`→`Room`, `HTMLDocument`→`Element` tree, `Company`→`Department`.
- The choice drives **memory management**: in C++, composition suggests the part is a value member or `unique_ptr` (auto-destroyed); aggregation suggests `shared_ptr`/raw pointers with external ownership; in Java it drives what's eligible for GC and whether a reference is strong vs weak.

## 4. Why Wasn't Another Approach Chosen?
- *Why not one "has-a" term?* Because ownership has real consequences: object lifetime, sharing, destruction order, serialization scope, and DB cascades (in ORMs, `CascadeType.ALL` is literally "composition", `CascadeType` none is aggregation). One term would hide those decisions.
- *Why not just composition everywhere?* Because it *over-constrains*: sharing requires non-owning references (aggregation), and sometimes neither side should own the other (association). Composition everywhere would break shared caches, flyweights, and circular structures.
- *Why not make everything a dependency (no fields)?* You'd lose the model — fields encode structure the caller needn't recompute; but minimizing dependencies to the *needed* set is exactly right: each added association is coupling (see Part 06, coupling/cohesion and Law of Demeter).
- *Why did C++/Java differ historically?* C++ made ownership an explicit language concern (`unique_ptr` vs `shared_ptr` vs raw), because destructors and leaks are user-managed; Java gave GC ownership to the runtime, so composition vs aggregation became *design* decisions rather than memory-safety requirements — but the design difference matters in both.

## 5. Intuition
Ownership is the intuition. **Composition** is "mine — I made it, I'll take it apart": your heart is yours alone (composed); you can't swap it, and when you go, it goes. **Aggregation** is "mine to use, but not mine alone": the chairs in your classroom are aggregated — the school owns them, you use them, and they outlive you (and are used by next year's class). **Association** is "I know about it": you know your postman's route, but you don't own or borrow it. **Dependency** is "I used it once": a pencil you borrowed to sign — you didn't keep it, didn't own it. The strength isn't about the *object*, it's about **who's responsible for its existence**.

## 6. Real-World Analogy
A **restaurant** models every relationship kind: the restaurant *depends on* a recipe book when the chef looks one up (dependency — transient use). The restaurant *associates with* its delivery partners (association — it knows them, no ownership). The restaurant *aggregates* tables and chairs (aggregation — a table can be moved to another branch, the tables are a shared asset pool owned by corporate). The restaurant *composes* its kitchen (composition — the kitchen's equipment, staffed by the restaurant, exists only as long as the restaurant does; you don't move the kitchen to another branch). When the restaurant closes: the kitchen is dismantled (composition), the tables go back to the warehouse (aggregation), the delivery partners continue unaffected (association), and the recipe book is just unused (dependency).

## 7. Formal Definition
- **Dependency**: A depends on B if a change to B may force a change to A; A uses B without storing it. Weakest coupling.
- **Association**: A relationship in which one object *knows* another and uses its services over time; implemented as a field/reference. It has multiplicity and roles. Neither party owns the other.
- **Aggregation**: A *special form of association* denoting a whole-part ("has-a") relationship where the part is **not** owned by the whole — the part can be created/shared/destroyed independently; also called "shared association." Lifetime of part ≥ lifetime of the aggregate.
- **Composition**: A *stronger* whole-part relationship where the whole **owns** the part: the part cannot exist without the whole, is created and destroyed with it, and typically cannot be shared; also called "composite aggregation." UML: filled diamond on the whole; in C++, lifetime of part == lifetime of composite (value member or `unique_ptr`); in Java, the whole holds the only strong reference and explicitly creates the part.

## 8. Example
```java
// COMPOSITION: House owns Rooms — Room dies with House
public class Room {
    final int number;
    public Room(int number) { this.number = number; }   // created BY House
    String describe() { return "Room " + number; }
}
public class House {
    private final List<Room> rooms = new ArrayList<>();  // House creates rooms
    public House(int count) { for (int i = 1; i <= count; i++) rooms.add(new Room(i)); }
    // no external way to add a Room — ownership is sealed
}

// AGGREGATION: House has Furniture, but furniture can be shared / outlive
public class Furniture { String name; public Furniture(String n) { name = n; } }
public class House2 {
    private final List<Furniture> furniture;
    public House2(List<Furniture> furniture) { this.furniture = furniture; } // received from outside
}
// Furniture f = new Furniture("sofa");  new House2(List.of(f));  → f is independent of the House

// ASSOCIATION: House knows its Owner (no ownership)
public class Owner { public String name; }
public class House3 { private Owner owner; public void setOwner(Owner o) { this.owner = o; } }

// DEPENDENCY: House uses a Handyman once
public class Handyman { void repair() {} }
public class House4 { void fixRoof(Handyman h) { h.repair(); } }   // no field — transient use
```

## 9. Internal Working
1. **Composition** in the constructor: `rooms.add(new Room(i))` — the part is created inside the composite's lifetime, held by strong references owned solely by the composite. GC: when `House` is unreachable, its `rooms` become unreachable too — collected together. C++: a value member or `unique_ptr` member gives deterministic destruction in reverse order (rooms destroyed before house).
2. **Aggregation**: the reference arrives via constructor/setter from *outside* — the composite holds a strong reference but does not own it; the same `Furniture` object can be referenced by two houses. GC: the furniture is collected only when *no* referrer remains — independent of the house.
3. **Association**: a field that may be null (`owner`) and may be reassigned; the object is just "known." **Dependency**: no field at all — the object exists only for the duration of the method call (parameters, locals); in a tracing GC the dependency object may be collected mid-call as soon as the method is done with it.
4. **Serialization/DB mapping**: composition maps to embedded/owned records (cascade delete); aggregation maps to shared references (no cascade, FK nullable or shared). ORMs encode this as `CascadeType.ALL` vs none — the relationship choice *is* the persistence behavior.
5. **C++ ownership transfer**: composition → `unique_ptr` (move, no copy — single owner); aggregation → `shared_ptr`/`weak_ptr` (shared or borrowed); association → raw pointer with documented non-ownership; dependency → pass by reference/pointer for the call.

## 10. Time Complexity
- No runtime cost difference — a relationship is a field or a local. The cost is conceptual and in lifecycle management, not CPU.
- Space: one reference per relationship link (8 bytes on 64-bit), plus allocation cost of the part (composition pays for part allocation at construction; aggregation pays wherever the part is built).
- Composition avoids the *search* cost of sharing: each whole has its own parts (O(1) access), whereas aggregation/association may contend on shared state.

## 11. Advantages
- **Composition**: clear ownership, deterministic destruction (C++), no dangling parts, GC-friendly (parts die with the whole), safe against shared-state races.
- **Aggregation**: reuse and sharing (flyweight-like), flexibility to reassign parts, lower construction cost (parts pre-built), decoupled lifecycles.
- **Association**: minimal coupling — know only what's needed.
- **Dependency**: loosest coupling; changes to B rarely ripple to A.

## 12. Disadvantages
- **Composition**: no sharing, rigid (rebuilding a part means rebuilding the whole), can over-couple to concrete types (mitigate via abstract part types).
- **Aggregation**: shared parts need synchronization if mutable; lifecycle of the part is someone else's problem (leaks if nobody owns it in C++).
- **Association**: can imply hidden coupling; a model full of associations is hard to test (many collaborators to mock).
- **Dependency/association** proliferation: each relationship is coupling — the reason Part 06's coupling/cohesion and Law of Demeter exist.

## 13. Interview Questions
1. **Q: Difference between association, aggregation, and composition?** A: Association = knows/has-a, no ownership. Aggregation = weak has-a, part can outlive and be shared. Composition = strong has-a, whole owns the part's lifecycle. The key axis is ownership.
2. **Q: Which is `Car` and `Engine`?** A: Composition — the engine is created by and dies with the car; a car's engine isn't typically shared. (One interviewer variation: "but you *can* swap engines" → that's still ownership within the car's lifecycle — swapping doesn't mean the engine is shared.)
3. **Q: TRICKY — `Car` and `Wheel`?** A: Composition in the classic model (wheels are created with the car). But a *spare tire* pool → aggregation. The same two classes can model either depending on the lifecycle you choose — the relationship is a design decision, not an intrinsic property.
4. **Q: How do you implement aggregation vs composition in Java?** A: Composition: `new` the part inside the whole's constructor, private field, no setter. Aggregation: receive the part via constructor/setter from outside. Composition seals the reference; aggregation doesn't.
5. **Q: SCENARIO — Design a `Company` → `Department` model. Which relationship?** A: Composition (departments are created by and die with the company; a department can't float between companies). Contrast: an `Employee` is an aggregation/association — employees are hired (exist before/after, can be shared via contractors).
6. **Q: PRODUCTION — In an ORM, how does composition vs aggregation map?** A: Composition → `CascadeType.ALL` on the owning side (deleting the parent deletes children); aggregation → no cascade, shared FK/reference (children persist). Getting this wrong = orphaned rows or accidental mass-deletes.
7. **Q: What does aggregation look like in C++?** A: `shared_ptr<T>` or a raw pointer with documented external ownership. Composition → value member or `unique_ptr<T>`. The pointer type encodes the relationship — that's C++ ownership semantics.
8. **Q: TRICKY — Can a class have both aggregation and composition to the *same* type?** A: Yes — e.g., `House` *composes* `Room`s but *aggregates* a shared `MeetingRoom` pool; or `Player` is composed into its `Team` roster while also aggregated by `League`. Relationship is per-link, not per-type.
9. **Q: What is the UML notation difference?** A: Composition = filled (black) diamond on the whole side; aggregation = open (white) diamond on the whole side; association = plain line; dependency = dashed arrow. Multiplicity on the part side (`1`, `*`, `0..1`).
10. **Q: SCENARIO — A `Document` contains text and also references a shared `Theme`. Model it.** A: Text is composition (owned, dies with document); `Theme` is aggregation (shared across documents — one theme change updates all). The sharing requirement forces aggregation.
11. **Q: Why is "prefer composition over inheritance" compatible with composition the relationship?** A: The adage means prefer *has-a* relationships (composition/aggregation) over extends-relationships for code reuse — because inheritance (generalization) couples the subclass to every inherited detail, while has-a keeps a clean boundary. Same word "composition", two levels (relationship vs design principle).
12. **Q: PRODUCTION — Weak references vs aggregation?** A: Not the same thing. A `WeakReference` lets GC reclaim the object regardless — used for caches, not relationship modeling. Aggregation uses a *strong* reference but doesn't claim ownership. Composition/aggregation are design semantics; weak/strong is memory management.
13. **Q: TRICKY — Is `List<Order>` in a `Customer` an association or aggregation?** A: Association (knows its orders — but it does not own them: the same order isn't shared, yet the order's lifecycle is the order's). Most collection-of-foreign-entities fields are associations or aggregations; only "owned, created here, dies here" is composition.
14. **Q: What does multiplicity mean here?** A: How many parts a whole may link to: `1` (exactly one), `*` (zero or more), `0..1` (optional), `1..*` (one or more). `Customer 1 — * Order` reads "one customer has zero or more orders."

## 14. Follow-Up Questions
1. **Q: How does the relationship choice affect testing?** A: Composition makes parts hard to stub (created internally) — design for injection at boundaries; aggregation/association are naturally mockable since references come from outside. This pushes many teams toward aggregation at seams.
2. **Q: What is the difference between composition and aggregation in terms of "sharing"?** A: Composition forbids sharing (exclusive ownership, part lives and dies with whole); aggregation permits sharing (part may be referenced by several wholes simultaneously). Sharing is the practical test: "can two wholes use the same part?"
3. **Q: How do you model a tree or a graph?** A: A tree is composition of nodes (parent owns children, no cycles, no sharing); a graph with shared nodes is aggregation/association (shared references create cycles — use `weak_ptr`/weak references to break them).
4. **Q: What's the "is-a vs has-a" decision?** A: When reuse is needed, ask: is the subclass really substitutable (is-a → inheritance) or does it merely *use* the other (has-a → composition/aggregation)? Prefer has-a unless LSP genuinely holds.

## 15. Coding Example
```java
import java.util.*;
public class Relationships {
    // COMPOSITION — Engine created by and owned by Car
    static class Engine { void start() { print("engine on"); } }
    static class Car {
        private final Engine engine = new Engine();        // created internally, exclusive
        void start() { engine.start(); }
    }
    // AGGREGATION — Driver passed in, exists independently
    static class Driver { String name; Driver(String n) { name = n; } }
    static class Taxi {
        private final Driver driver;                       // received, not owned
        Taxi(Driver d) { this.driver = d; }
    }
    // ASSOCIATION — Car knows its route (no lifecycle role)
    static class Route { }
    static class Car2 { private Route current; void setRoute(Route r) { current = r; } }
    // DEPENDENCY — uses a GPS once
    static class Gps { String locate() { return "12.9,77.5"; } }
    static class Car3 { void findSelf(Gps g) { print("at " + g.locate()); } }

    public static void main(String[] args) {
        Driver d = new Driver("Alice");                   // independent of any taxi
        Taxi t = new Taxi(d);                             // aggregates the same driver
        Car c = new Car(); c.start();                      // engine is composition — dies with c
        print("driver still alive after taxi? " + (d.name != null));   // aggregation: yes
    }
}
```
```cpp
#include <memory>
#include <string>
struct Engine { void start() {} };
struct Driver { std::string name; };
struct Car {
    Engine engine;                      // composition: value member — destroyed with Car
    std::shared_ptr<Driver> driver;     // aggregation: shared ownership
    Car(std::shared_ptr<Driver> d) : driver(d) {}
};
```

## 16. Industry Usage
- **JDK collections**: an `ArrayList` *composes* its backing array; a `HashMap` composes its nodes/buckets — internal structures are owned and die with the container. `Collections.unmodifiableList` *aggregates* the backing list (shares it, wraps it).
- **Spring DI**: the container *aggregates* beans (creates them, but they outlive and are shared across consumers); a controller *associates with* its service via injection. Composition is used internally for owned helpers.
- **JPA/Hibernate**: `CascadeType.ALL` and `orphanRemoval=true` model composition (owned children); shared entities use aggregation semantics (no cascade) — the relationship choice *is* the persistence behavior.
- **Operating systems**: a process *composes* its memory-mapped segments; the scheduler *associates with* processes (knows them, doesn't own them); filesystems aggregate blocks.
- **UI frameworks (Java Swing/Android)**: view hierarchies are composition (a `JPanel` owns its children); a view *associates with* its controller/model; shared `LookAndFeel`/theme objects are aggregated.

## 17. References
- Martin Fowler, *UML Distilled* — the authoritative relationship/notation reference.
- Grady Booch, *Object-Oriented Analysis and Design* — association/aggregation/composition foundations.
- Craig Larman, *Applying UML and Patterns* — relationship modeling with patterns.
- GeeksForGeeks, "Association, Composition and Aggregation in Java": https://www.geeksforgeeks.org/association-composition-aggregation-java/
- JLS §8.3 — field declarations (the mechanism behind relationships): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html

## 18. Cheat Sheet
- Dependency: uses once, no field (dashed arrow).
- Association: knows, field, no ownership (plain line).
- Aggregation: weak has-a, shared, part outlives (open diamond).
- Composition: strong has-a, owned, part dies with whole (filled diamond).
- Key question: WHO creates it and WHO destroys it?
- Sharing test: can two wholes use one part? Yes → aggregation; No → composition.
- Java: composition = `new` inside constructor; aggregation = injected.
- C++: value/`unique_ptr` = composition; `shared_ptr`/raw = aggregation.
- ORM: cascade ALL = composition; no cascade = aggregation.
- Adage "prefer composition over inheritance" = prefer has-a relationships.

## 19. Quiz
1. Filled diamond in UML denotes: a) aggregation b) composition c) association d) dependency → **b**
2. The part that can be shared by two wholes is: a) composition b) aggregation c) dependency → **b**
3. Composition means: a) whole owns part lifecycle b) part outlives whole c) no field d) static → **a**
4. Dependency in UML is drawn as: a) filled diamond b) dashed arrow c) plain line d) triangle → **b**
5. Composition in Java is typically: a) injected field b) `new` in constructor c) static method d) weak ref → **b**
6. True or False: A `Car`'s `Engine` is usually composition. → **True**

## 20. Flashcards
- **Q: Aggregation vs composition?** → **A:** Ownership — composition owns the part's lifecycle (dies with whole); aggregation shares it (part outlives).
- **Q: UML diamond rules?** → **A:** Filled = composition, open = aggregation, both on the whole side.
- **Q: Dependency?** → **A:** Uses-a, no field, dashed arrow.
- **Q: Sharing test?** → **A:** Two wholes using one part → aggregation, not composition.
- **Q: Java implementation of composition?** → **A:** `new` part inside the whole's constructor.
- **Q: C++ composition?** → **A:** value member or `unique_ptr`.

## 21. Revision
Relationships range dependency → association → aggregation → composition, ordered by ownership. Dependency is transient use (no field). Association is a knowledge link (field, no ownership). Aggregation is a weak has-a: the part is shared and may outlive the whole (open diamond). Composition is strong has-a: the whole owns the part's creation and destruction; the part cannot exist alone (filled diamond). The deciding test is **who creates and destroys** and **can it be shared**; Java shows it via `new`-in-constructor (composition) vs injection (aggregation), C++ via value/`unique_ptr` vs `shared_ptr`/raw, ORMs via cascade-ALL vs none. "Prefer composition over inheritance" means prefer has-a relationships for reuse. First-30-seconds answer: "Association knows, aggregation shares, composition owns — the axis is lifecycle ownership."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Difference between association/aggregation/composition?" | Interview Q1 / Section 2, 7 |
| "Is Car/Engine composition?" | Interview Q2 |
| "How implemented in Java/C++?" | Interview Q4, Q7 / Section 9 |
| "ORM cascade mapping?" | Interview Q6 / Section 16 |
| "Can two wholes share one part?" | Interview Q11 / Section 6 |
| "UML notation?" | Interview Q9 / Section 2 |
| "Is List<Order> an association?" | Interview Q13 |
| "Multiplicity meaning?" | Interview Q14 |
