# UML Class Diagrams for OOPs

> **TL;DR**: A UML class diagram is a structural blueprint — boxes for classes/interfaces, and five relationship arrows (dependency, association, aggregation, composition, generalization) with multiplicity and roles, letting you design and communicate an object model precisely before writing code.

## 1. Why Does This Exist?
Code is a terrible first place to discuss *structure*. Two engineers trying to align on "does the `Order` own the `Item`s?" will stare at each other's files and guess. UML class diagrams exist to make object structure **visible, precise, and shareable**: boxes for types, arrows for relationships, labels for counts and roles — so a design can be reviewed, agreed upon, and even machine-validated before anyone writes a class. Interviewers ask you to *draw* a class diagram because it forces you to make decisions (which relationship? what multiplicity? which direction?) that "just write the code" lets you dodge. It's the lingua franca of architecture: no matter the language or team, a filled diamond means "composes" on every whiteboard in the world.

## 2. How Does It Work?
Core elements:
- **Class box**: three compartments — name, attributes (`- name: String`), operations (`+ pay(amount: double): boolean`). Modifiers: `+` public, `-` private, `#` protected, `~` package.
- **Relationships** (arrow kinds):
  - **Dependency** — dashed arrow `- - ->`: A uses B transiently.
  - **Association** — solid line: A knows B (no ownership).
  - **Aggregation** — open diamond on the whole: weak has-a.
  - **Composition** — filled diamond on the whole: owned has-a.
  - **Generalization (inheritance)** — open triangle to the superclass; **realization (interface)** — dashed triangle to the interface.
- **Multiplicity** at the ends: `1`, `*`, `0..1`, `1..*`, `0..*`.
- **Role labels** on the line ends, and **navigability** arrows showing who holds the reference.
To draw a model: identify the types (boxes), the relationships (arrows + diamonds), the counts (multiplicity), and the roles — and the design is specified.

## 3. When Is It Used?
- **Design/blueprint before code**: agreeing the object model with teammates or a reviewer.
- **Interview whiteboard**: "design a library system" → you draw the class diagram, then code it.
- **Architecture documentation**: ADRs, design docs, READMEs carry a diagram instead of prose.
- **Reverse engineering / onboarding**: generate a diagram from existing code (IntelliJ, PlantUML) to understand a codebase.
- **Code generation**: some teams generate Java/C++/C# skeletons directly from a diagram (round-trip engineering).
- **Refactoring planning**: visualizing the current graph to find excessive coupling before changing it.

## 4. Why Wasn't Another Approach Chosen?
- *Why not just describe in prose?* Prose is ambiguous — "owns" means different things to different readers. The diagram's shapes *are* the semantics: a filled diamond has one meaning, period.
- *Why not just read the code?* Code answers "what," not "why"; the *intent* (which relationship was chosen and why) is invisible in source. Also, codebases have hundreds of classes — a diagram shows structure at a glance.
- *Why this particular notation and not boxes-and-lines ad hoc?* Ad hoc sketches don't scale or communicate: without standard arrow kinds and multiplicity, every team re-invents and misreads. UML won because it was precise enough to be tooling-able while simple enough to whiteboard.
- *Why not skip diagrams entirely (agile purists)?* Diagrams are documentation — valuable for the *model*, not for over-engineering. The scrum anti-pattern is "diagram-everything"; the healthy practice is "diagram the structure where the structure is non-trivial."
- *Why isn't class diagram the only UML type?* It's one of ~14 UML diagram types; class diagrams model *static structure*, which is exactly what OOPs design rounds need — sequence/state diagrams cover behavior, which this part deliberately leaves out.

## 5. Intuition
A class diagram is an **architectural blueprint of your program's nouns**. Just as a building blueprint shows walls (classes), doors (interfaces), and which door opens into which room (relationships), the class diagram shows types and how they connect — without showing the plumbing (methods' bodies) or the activity (runtime calls). When you draw it you're forced to answer structural questions up front: "Is a room inside the building, or does the building just *use* a room?" (composition vs association). Reading it gives you the entire shape of the system in one glance.

## 6. Real-World Analogy
An **org chart mixed with an org's supply chain**. Each employee is a class box (name, title, contact info = attributes, skills = methods). "Reports to" is an aggregation-style whole-part (department aggregates people — people outlive departments). "Has a direct reports" is composition-like in its strictness (a manager's team exists only under that manager). "Uses the copier" is a dependency (transient). "Coordinates with marketing" is an association (knows them, no ownership). The chart tells you the entire structure of who-owns-whom and who-knows-whom at a glance — exactly what a class diagram does for objects.

## 7. Formal Definition
A **UML (Unified Modeling Language) class diagram** is a static-structure diagram that depicts the classes, interfaces, and their relationships in a system. Notation: a class is a rectangle with up to three compartments (name, attributes, operations); **generalization** is a hollow triangular arrow pointing at the parent; **realization** is a *dashed* hollow-triangle arrow to an interface; **association** is a solid line (optionally navigable) with multiplicity and roles; **aggregation** is a solid line with a *hollow diamond* at the whole end (part can outlive the whole); **composition** is a solid line with a *filled diamond* at the whole end (the part is owned; its lifetime is bound to the whole); **dependency** is a *dashed arrow*. Visibility prefixes: `+` public, `-` private, `#` protected, `~` package. Multiplicities: `1`, `0..1`, `*`, `1..*`, `0..*` describe how many instances participate on each side.

## 8. Example
```
        ┌────────────────────┐          ┌──────────────────┐
        │     Customer       │          │      Order       │
        ├────────────────────┤ 1       *├──────────────────┤
        │ - id: int          │◄─────────│ - id: int        │
        │ - name: String     │          │ - date: LocalDate│
        ├────────────────────┤          ├──────────────────┤
        │ + placeOrder()     │          │ + addItem(Item)  │
        └────────────────────┘          │ + total(): double│
              ▲                         └─────────┬────────┘
        implements                           * owns│ (filled diamond)
        ┌──────────────────┐                     │
        │  Discountable    │              ┌──────▼─────┐   *        ┌────────┐
        │  (interface)     │              │   OrderItem│───────────►│  Item  │
        └──────────────────┘              └────────────┘ (dependency)└────────┘
```
Read it: a `Customer` **realizes** `Discountable` (dashed triangle). A `Customer` **associates** with 0..* `Order`s (solid line, `1` near Customer, `*` near Order). The `Order` **composes** `OrderItem`s (filled diamond on Order) — items die with the order. The `Order` **depends on** `Item` (dashed arrow) — uses it transiently. Every arrow is a *decision* about ownership and count.

## 9. Internal Working
1. **Identify types**: nouns in the requirement become class boxes ("library, book, member, loan").
2. **Add attributes/operations**: verbs and properties become compartments; visibility from encapsulation choices (Part 02).
3. **Choose relationships**: for each pair, run the ownership test — is it a *transient use* (dependency), a *knowledge* (association), *shared has-a* (aggregation), *owned has-a* (composition), or *is-a* (generalization)?
4. **Add multiplicity and roles**: one book has many copies (`1..*`), a member borrows many books but each loan belongs to one member (`*` ↔ `1`).
5. **Verify**: each relationship must be implementable as fields/calls; each composition must have "created and destroyed by the whole" in the code; each generalization must satisfy LSP (Part 06).
6. **Tools**: draw by hand for interviews; use PlantUML/Mermaid/draw.io in docs; use IDE "diagram from code" to reverse-engineer.

## 10. Time Complexity
- Drawing/reading a diagram is O(number of classes × relationships) — linear in model size.
- No runtime cost — a diagram is documentation; it doesn't execute.
- The *real* cost is design-time: deciding ownership (composition vs aggregation) up front prevents expensive refactors later — cheap design, expensive bugs avoided.

## 11. Advantages
- Makes ownership/coupling decisions explicit and reviewable.
- Communicates structure language-agnostically (Java/Go/C++ teams share it).
- Interviewers use it as a compressed way to test design judgment.
- Can generate skeletons, validate invariants (tooling), and reverse-engineer.
- Nails down multiplicity — forces you to handle the "0 or 1 or many" cases.

## 12. Disadvantages
- Over-modeling: diagrams for trivial structure waste time.
- Tool proliferation/inconsistency: differing UML tool output can mislead.
- Static only — class diagrams say nothing about behavior, concurrency, or sequencing (needs sequence/state diagrams).
- Risk of "draw-the-perfect-model" paralysis instead of shipping code.
- Casual use of arrows incorrectly (e.g., aggregation vs composition swapped) silently misleads.

## 13. Interview Questions
1. **Q: What are the five class-diagram relationship types?** A: Dependency (dashed arrow), association (line), aggregation (open diamond), composition (filled diamond), generalization/inheritance (open triangle; dashed triangle for realization of an interface).
2. **Q: How do you show inheritance vs interface implementation?** A: Inheritance = solid line ending in a hollow triangle pointing to the superclass; interface = dashed line with a hollow triangle to the interface (realization).
3. **Q: TRICKY — Where does the diamond go in aggregation/composition?** A: On the **whole/owner** side. `House` ◇ `Room`: open/filled diamond sits next to `House`. Many candidates put it on the part side — a common mistake.
4. **Q: What is multiplicity?** A: The count on each end of a relationship: `1` (exactly one), `0..1` (optional), `*` (zero+), `1..*` (one+). `Customer 1 — * Order`: one customer, many orders.
5. **Q: SCENARIO — Draw a class diagram for a Library.** A: `Library` composes `Book` copies (owned inventory) and `Loan` records (filled diamonds); `Member` associates with `Loan` (solid line, `1`↔`*`); `Book` and `Member` realize a `Searchable` interface (dashed triangles); `Librarian` depends on a `Book` when cataloguing (dashed arrow).
6. **Q: PRODUCTION — Why do teams keep class diagrams in READMEs?** A: Onboarding and architectural review — the diagram is the fastest summary of structure; it captures the *decisions* (who owns what) that code diff history loses.
7. **Q: What do `+`, `-`, `#`, `~` mean?** A: Public, private, protected, package-private — the Java access modifiers (Part 01 ch-02). The diagram documents encapsulation, not just names.
8. **Q: TRICKY — Can a class have both a composition diamond and be associated with the same class?** A: Yes — a `House` composes its `Room`s (owns them) and associates with a *shared* `Room` (a conference room borrowed from a neighbor). Different *links*, same type.
9. **Q: What is navigability?** A: An arrowhead on an association line showing which side holds the reference — `Customer → Order` means Customer holds Orders. Without the arrow, navigation is unspecified.
10. **Q: SCENARIO — "Design an e-commerce checkout."** A: `Cart` composes `CartItem`s; `Order` composes `OrderLine`s; `Customer` associates with `Order` and `Cart`; `Checkout` depends on `PaymentGateway` (interface, dashed triangle); `PaymentGateway` realized by `CardGateway`/`UpiGateway`.
11. **Q: PRODUCTION — What's wrong with "draw diagrams after writing code"?** A: The value is in designing *before* — committing to ownership decisions up front. Reverse-generated diagrams help onboarding, but they document what *is*, not what *should be*, and often reveal accidental coupling too late.
12. **Q: How does a class diagram relate to CRC cards?** A: CRC (Class-Responsibility-Collaboration) cards are the lightweight predecessor: a class's responsibilities + the classes it collaborates with — the diagram formalizes the "collaborates" part with arrows, multiplicity, roles.
13. **Q: TRICKY — You see two classes with no arrow between them. Does that mean no relationship?** A: Not necessarily — UML shows declared relationships; two classes can still interact via a third, or via reflection/lazy lookup not modeled. Absence of an arrow means "no *modeled* relationship."
14. **Q: What tools render these?** A: PlantUML, Mermaid (both text-based, version-control friendly), draw.io, StarUML, IntelliJ/VS Code reverse-engineering, and `puml`-to-image in CI docs.

## 14. Follow-Up Questions
1. **Q: How do design patterns appear in class diagrams?** A: They're relationship recipes — Strategy shows many `Strategy`-dashed-triangle realizations off one interface; Composite shows composition diamonds forming a tree; Observer shows association + interface realization. Drawing the pattern = drawing the relationships.
2. **Q: What's the difference between a class diagram and an object diagram?** A: A class diagram shows types and relationships (the blueprint); an object diagram shows *instances* and their *links at a moment in time* — a snapshot (often useful for debugging a design).
3. **Q: How does UML model generics?** A: Parameterized classes with the type in the name compartment — `List<E>`, `Map<K,V>`; binding shown with a dashed arrow to the concrete type (e.g., `List<Order>`).
4. **Q: When is a class diagram enough vs needing sequence diagrams?** A: Class diagrams answer "what's the structure?" Sequence diagrams answer "who calls whom, in what order?" — behavioral questions (concurrency, protocol) need the latter.

## 15. Coding Example
```java
// The diagram from Section 8, implemented:
import java.util.*;
interface Discountable { double applyDiscount(double amount); }
class Customer implements Discountable {
    private final int id; private final String name;
    private final List<Order> orders = new ArrayList<>();       // association 1↔*
    Customer(int id, String name) { this.id = id; this.name = name; }
    Order placeOrder() { Order o = new Order(this); orders.add(o); return o; }  // navigability: Customer → Order
    public double applyDiscount(double a) { return a * 0.95; }
}
class Order {
    private final Customer customer;                            // back-navigation
    private final List<OrderItem> items = new ArrayList<>();    // COMPOSITION (filled diamond)
    Order(Customer c) { this.customer = c; }
    void addItem(Item i, int qty) { items.add(new OrderItem(i, qty)); }  // items created & owned here
    double total() { return items.stream().mapToDouble(OrderItem::price).sum(); }
}
record Item(String sku, double price) {}                        // Order depends on Item (dashed arrow)
record OrderItem(Item item, int qty) { double price() { return item.price() * qty; } }
public class Main {
    public static void main(String[] args) {
        Customer c = new Customer(1, "A");
        Order o = c.placeOrder();
        o.addItem(new Item("A1", 10), 2);
        System.out.println(c.applyDiscount(o.total()));         // 19.0
    }
}
```

## 16. Industry Usage
- **Every architecture doc**: ADRs and design docs embed class diagrams; PlantUML/Mermaid live in repos for review.
- **Spring ecosystems**: beans-as-class-diagram visualizations; DI graphs checked by `springdoc`-style tooling.
- **Interviews (Meta/Google/Amazon/Stripe)**: "design X" rounds expect you to draw the class diagram *before* writing code — the diagram is the design.
- **Enterprise modeling**: teams generate entities, DTOs, and schema from diagrams (round-trip engineering, e.g., JPA entity generation).
- **Documentation-as-code**: Mermaid diagrams in READMEs render in GitHub/GitLab PRs — the diagram is reviewed in the PR like code.

## 17. References
- Martin Fowler, *UML Distilled* — the definitive concise notation reference.
- Object Management Group (OMG), UML 2.5.1 Specification: https://www.omg.org/spec/UML/
- Craig Larman, *Applying UML and Patterns* — diagrams in real design.
- Mermaid (renders class diagrams in Markdown/CI): https://mermaid.js.org/
- PlantUML class diagram guide: https://plantuml.com/class-diagram

## 18. Cheat Sheet
- Box = class (3 compartments: name, attrs, ops).
- `+` public, `-` private, `#` protected, `~` package.
- Solid line + open triangle = inheritance.
- Dashed line + open triangle = interface realization.
- Solid line = association (knows).
- Open diamond (whole side) = aggregation (shared has-a).
- Filled diamond (whole side) = composition (owned has-a).
- Dashed arrow = dependency (uses once).
- Multiplicity: `1`, `0..1`, `*`, `1..*` on the ends.
- Diamond goes on the WHOLE side — never on the part.

## 19. Quiz
1. Realization of an interface is drawn with: a) solid triangle b) dashed triangle c) filled diamond d) dashed arrow → **b**
2. The diamond in composition sits: a) on the part side b) on the whole side c) middle d) both → **b**
3. `*` on one end means: a) exactly one b) zero or more c) one or more d) optional → **b**
4. Package-private visibility is: a) `+` b) `#` c) `~` d) `-` → **c**
5. Inheritance is: a) solid line + open triangle b) dashed arrow c) filled diamond d) plain line → **a**
6. True or False: A class diagram shows runtime behavior. → **False** (static structure only)

## 20. Flashcards
- **Q: Composition UML symbol?** → **A:** Filled diamond on the whole side.
- **Q: Aggregation symbol?** → **A:** Open diamond on the whole side.
- **Q: Inheritance arrow?** → **A:** Solid line + open triangle to the parent.
- **Q: Interface realization?** → **A:** Dashed line + open triangle.
- **Q: Dependency?** → **A:** Dashed arrow.
- **Q: Multiplicity `0..1`?** → **A:** Zero or one (optional).

## 21. Revision
A class diagram = boxes (class name, attributes with visibility `+ - # ~`, operations) + five relationship arrows (dependency = dashed arrow; association = line; aggregation = open diamond; composition = filled diamond — both diamonds on the *whole* side; generalization = open triangle, dashed for interfaces) + multiplicity on each end + role labels + navigability. It's the design blueprint: drawing it forces ownership, coupling, and count decisions up front; reading it reveals the whole system's structure at a glance. Interview design rounds expect you to draw before coding; teams keep PlantUML/Mermaid diagrams in the repo. First-30-seconds answer: "Boxes for types, five arrows for relationships, diamonds on the whole side, multiplicity on both ends."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Five relationship types?" | Interview Q1 / Section 2, 7 |
| "Where does the diamond go?" | Interview Q3 |
| "Multiplicity meaning?" | Interview Q4 / Section 2 |
| "Draw the Library design" | Interview Q5 / Section 8 |
| "Visibility modifiers in UML?" | Interview Q7 |
| "Navigability?" | Interview Q9 |
| "Tools for diagrams?" | Interview Q14 / Section 16 |
| "Class vs object diagram?" | Follow-up Q2 |
