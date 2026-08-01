# What Are Design Patterns and Why They Exist

> **TL;DR**: A design pattern is a **named, documented, reusable solution to a recurring design problem** — it exists so that engineers don't reinvent the wheel for every project, communicate designs in a shared vocabulary, and inherit solutions that have been battle-tested across decades of production systems.

## 1. Why Does This Exist?
If every engineer solved "how do I create objects flexibly?" or "how do I decouple a subject from its observers?" from scratch on every project, three terrible things would happen: (1) **reinvention** — thousands of subtly-different ad-hoc solutions, most of them buggy; (2) **no shared vocabulary** — a reviewer would have to read your entire class structure to understand what you did, instead of hearing "it uses an Observer pattern"; (3) **no accumulated wisdom** — each new engineer would repeat the same mistakes (e.g., creating a second instance of a "single" object, coupling tightly to a concrete class).

Design patterns exist to solve exactly these three problems. They are *proven shapes of collaboration* between classes that have been tried, refined, and documented by many engineers. A pattern is not invented in a vacuum — the Gang of Four (GOF) book (1994) *cataloged* patterns that had already been used repeatedly in real systems (Smalltalk, C++ libraries) and gave them names, so that a designer can say "use a Strategy here" and the whole team understands the shape, the trade-offs, and the pitfalls immediately.

## 2. How Does It Work?
A design pattern works by describing **four essential parts**:

1. **Name** — a handle that lets you refer to the whole pattern in one word ("Facade", "Observer", "Builder").
2. **Problem** — the force/condition the pattern resolves (e.g., "we must create objects without specifying their concrete classes").
3. **Solution** — the structure: the classes, interfaces, and collaborations that resolve the problem. This is the *shape*, not a concrete implementation.
4. **Consequences** — the results and trade-offs: what the pattern buys you (flexibility, decoupling) and what it costs (indirection, extra classes, complexity).

The solution is always expressed as **participants + relationships** (who does what, who knows about whom), which is why every pattern has a UML-ish class diagram. You apply it by mapping those participants onto your own classes. It works *because* it names the *intent* — not the code — so the same pattern applies to wildly different concrete systems.

## 3. When Is It Used?
- **When you recognize a recurring design problem**: object creation that must be deferred to subclasses (Factory Method), a one-of-a-kind resource (Singleton), sending requests without knowing the receiver (Command).
- **During design reviews and LLD interviews**: you justify a decision by naming a pattern and its consequences instead of drawing 20 boxes.
- **When refactoring**: patterns are the *target* of good refactoring — Fowler's *Refactoring* book literally catalogs refactorings "to patterns" (e.g., "Replace Conditional with Polymorphism" yields a Strategy/State shape).
- **When building or extending a framework**: frameworks (Spring, Java I/O, React) are themselves *implementations* of patterns — you must know the patterns to use the framework correctly.
- **When communicating architecture to a team**: a design doc that says "the payment module uses a Facade over three third-party SDKs" transfers intent in one line.

## 4. Why Wasn't Another Approach Chosen?
- **Writing code from scratch every time**: chosen for trivial problems, but rejected for recurring design problems because it ignores accumulated knowledge and leads to inconsistent, unmaintainable systems.
- **Using a framework instead of a pattern**: a framework is a *concrete, heavyweight implementation*; a pattern is a *shape* you apply. Frameworks are right when the problem is generic (web serving), but you can't pull in a framework to fix a local design tension — you apply a pattern.
- **Using a single global "kitchen sink" design**: some teams write one enormous `Everything` class to avoid pattern overhead; rejected because it destroys cohesion, testability, and parallelism between developers.
- **Copy-pasting a previous project's exact classes**: rejected because patterns are *abstract shapes* that must be adapted to your context; blind copying (a.k.a. "code that imitates a pattern without the intent") produces *false* patterns that add indirection without benefit.
- **Relying on pure instinct/experience**: experience is where patterns came from, but it's not *transferable* — a pattern is experience *written down*, so it scales across teams and generations.

## 5. Intuition
Think of design patterns as **recipes in a professional kitchen**. A recipe doesn't tell you the exact tomatoes in your fridge; it tells you the *method* — "make a roux, then slowly add stock" — and the pitfalls ("if you add stock too fast, the sauce splits"). A chef doesn't invent a sauce for every dish; they *recognize* the situation ("I need a binder") and pull the right recipe, adapting quantities to context. Similarly, a designer recognizes "this object must stay unique across the app" → reaches for Singleton; "I must swap algorithms at runtime" → Strategy. The intuition to build: **patterns are a library of recognized problem→solution shapes, not code you copy.**

The deeper intuition: every pattern is a bet on **where the change will happen**. Creational patterns bet change happens at object *birth*; structural patterns bet it happens in *composition*; behavioral patterns bet it happens in *behavior and communication*. Choose the pattern that bets on the change your requirements actually predict.

## 6. Real-World Analogy
A **blueprint library for civil engineers**. Bridges, buildings, and tunnels all share recurring structural problems — "how do we span a gap?", "how do we distribute load?". Engineers don't re-derive bridge design on every project; they use *standard solutions* (truss, arch, suspension) with proven load-bearing behavior, and they adapt the standard solution to the specific site. The blueprint is the pattern (the *shape*); the adapted concrete bridge is your implementation. And when two engineers say "suspension bridge", both instantly picture the same structure, tensions, and failure modes — exactly as "Observer" instantly pictures subject/observer coupling and its pitfalls.

## 7. Formal Definition
> A **design pattern** names, abstracts, and identifies the key aspects of a common design structure that make it useful for creating a reusable object-oriented design. A pattern is a three-part rule expressing a relation between a certain **context**, a **problem**, and a **solution** — i.e., a solution to a problem in a context.

— Christopher Alexander (architecture), adapted by the Gang of Four in *Design Patterns: Elements of Reusable Object-Oriented Software* (1994).

Formally, the GoF catalog defines four essential elements of a pattern: **name**, **problem**, **solution**, and **consequences**. The solution element describes the classes/objects, their responsibilities, collaborations, and the assignment of responsibilities — never the specific concrete classes.

## 8. Example
Consider a real tension: a `Report` class must export to **PDF, Excel, and CSV**, and the export format keeps growing (customers keep asking for new formats). Without a pattern, you write:

```java
class Report {
    void export(String format) {
        if (format.equals("PDF"))  { /* 40 lines of PDF logic */ }
        else if (format.equals("XLSX")) { /* 40 lines of Excel logic */ }
        else if (format.equals("CSV")) { /* 40 lines of CSV logic */ }
        // add "JSON" here → reopen the class, retest everything
    }
}
```

Recognize the *problem*: "an object must be able to vary its algorithm (export format) independently of the class using it; adding a format must not modify existing code" → this is the **Strategy pattern**. The solution shape: define an `Exporter` interface, put each format in its own class, and give `Report` a reference to an `Exporter`:

```java
interface Exporter { void export(Report r); }
class PdfExporter implements Exporter { public void export(Report r) { /* ... */ } }
class CsvExporter implements Exporter { public void export(Report r) { /* ... */ } }

class Report {
    private Exporter exporter;                       // injected
    void setExporter(Exporter e) { this.exporter = e; }
    void export() { exporter.export(this); }         // delegates
}
```

Now adding "JSON" means *adding a class* — zero modification of `Report` (Open-Closed Principle from Part 06). The pattern bought you extensibility at the price of a few extra classes.

## 9. Internal Working
A design pattern is not executed like an algorithm; it *structures* collaboration. The universal internal mechanics of applying any pattern:

1. **Recognize the problem** — identify the tension (e.g., "creation must not name concrete classes").
2. **Select the pattern** — match problem to pattern family (creational / structural / behavioral).
3. **Map participants** — rename the pattern's roles onto your classes (e.g., Strategy's `Strategy` → `Exporter`, `ConcreteStrategy` → `PdfExporter`, `Context` → `Report`).
4. **Wire the relationships** — establish the association lines (Context *holds a reference to* Strategy; Subject *maintains a list of* Observers).
5. **Respect the consequences** — accept the trade-off you chose (extra indirection, extra classes) and make sure you didn't *over*-apply (a pattern with one implementation and no predicted change is wasted indirection).
6. **Document the intent** — name the pattern in comments/design docs so the next engineer sees the *shape*, not a puzzle.

The reason this "works" internally: patterns exploit the four pillars of OOP from Parts 01–06 — **polymorphism** (Strategy, State, Template Method dispatch through interfaces), **encapsulation** (Factory hides construction, Facade hides a subsystem), **inheritance vs composition** (almost every pattern prefers composition — "favor composition over inheritance" — because it's more flexible), and **loose coupling** (Observer, Command, Mediator reduce concrete knowledge between objects).

## 10. Time Complexity
Design patterns are **structural, not computational** — they don't change the Big-O of your algorithms. But they add constant-factor and architectural costs:

- **Indirection overhead**: each delegation adds O(1) extra method call / virtual dispatch (a vtable lookup, Part 08) and usually one extra pointer dereference. A Strategy chain adds O(depth) calls.
- **Extra memory**: each pattern layer adds O(1) objects/pointers (e.g., a Decorator wraps one object; a chain of N decorators is O(N) objects).
- **No asymptotic change**: a `List` traversal is O(N) whether or not you wrapped it in an Iterator (which itself is O(1) per `next()`).
- The *real* complexity story is **maintenance complexity**, not time: each pattern is O(1)–O(N) extra classes; over-applied patterns add class count without benefit. In interviews, the right answer is: "patterns change *structural* complexity (number of classes and couplings), not algorithmic time complexity."

## 11. Advantages
- **Reuse of proven design**: you inherit decades of validated structure rather than reinventing it.
- **Shared vocabulary**: "this is a Facade" communicates a full architecture in two words; design reviews become faster and more precise.
- **Loose coupling & extensibility**: patterns implement the SOLID principles concretely (Open-Closed via Strategy/Decorator; Dependency Inversion via Factory/Abstract Factory).
- **Maintainability**: each pattern localizes the likely change, so a requirement change touches one class, not twenty.
- **Testability**: patterns like Strategy and Command isolate behavior behind small interfaces, making unit testing trivial.
- **Onboarding speed**: juniors who know patterns (from the book/catalog) understand a codebase's architecture faster.

## 12. Disadvantages
- **Indirection and complexity**: a pattern adds classes and layers; for a simple problem it is pure overhead ("you're writing a 5-class solution to a 2-line problem").
- **Overuse / pattern-forcing**: forcing a pattern where the problem doesn't match produces unmaintainable "design pattern vomit"; experienced reviewers reject over-application as harshly as under-design.
- **Learning curve**: the GoF book is dense; junior devs can copy the diagram while misunderstanding the intent (the classic interview failure).
- **Language misfit**: some patterns are trivial or redundant in some languages (e.g., Singleton is nearly free in Python with module-level state; Strategy is nearly free with first-class functions — Part 08).
- **False sense of correctness**: a pattern guarantees a *shape*, not a *correct design* — you can build a broken system using perfect patterns.

## 13. Interview Questions
1. **Q: What is a design pattern?** A: A named, documented, reusable solution to a recurring design problem, expressed as context + problem + solution + consequences. It captures the *shape* of the solution, not the concrete code, so it can be applied across systems.
2. **Q: What are the four essential elements of a pattern (per GoF)?** A: Name, Problem, Solution, Consequences. The name gives vocabulary; the problem states when to apply it; the solution gives the participants/collaborations; the consequences list trade-offs.
3. **Q: What problem do design patterns actually solve — code reuse or design reuse?** A: Design reuse. They reuse *proven shapes of collaboration*, not code. Copying code is copy-paste; applying a pattern is transferring intent and structure.
4. **Q: Difference between a design pattern and an algorithm?** A: An algorithm is a step-by-step procedure to compute a result (what to do); a pattern is a structural *shape* for organizing classes (how to arrange responsibilities). Algorithms have Big-O; patterns have trade-offs. A pattern *can* contain an algorithm (Template Method), but they're different things.
5. **Q: Difference between a pattern and a framework?** A: A pattern is a *reusable shape* you instantiate in your code; a framework is a *semi-complete concrete system* that supplies skeleton classes and inverts control. You apply a pattern *inside* your code; you *live inside* a framework. Frameworks often implement patterns (Spring's container is a Factory + Singleton + Proxy all at once).
6. **Q: What is an anti-pattern?** A: A documented *bad* solution that looks tempting but leads to problems — the negative image of a pattern. Examples: God Object, Spaghetti Code, Singleton abuse (using singleton for non-unique state). Knowing anti-patterns is as important as knowing patterns because they tell you what NOT to do.
7. **Q: Name the three families of GoF patterns and one pattern in each.** A: Creational (Singleton, Factory Method, Abstract Factory, Builder, Prototype), Structural (Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight), Behavioral (Strategy, Observer, Command, State, Template Method, Iterator, Memento, etc.).
8. **Q: Which GoF pattern family would you reach for if requirements keep adding new object types? (Scenario)** A: Creational — specifically Factory Method or Abstract Factory, which defer object creation to subclasses so the client code stays unchanged when new product types appear (Open-Closed).
9. **Q: "Favor composition over inheritance" — which principle is this and which patterns embody it?** A: It's a core GoF principle from the design chapters; almost all patterns prefer delegation to a composed object over subclassing. Strategy, Decorator, State, Proxy, Adapter all wrap/compose; Template Method is the rare inheritance-based pattern. Composition is preferred because it's more flexible (runtime swap) and avoids fragile base-class coupling.
10. **Q: What does "program to an interface, not an implementation" mean, and which patterns enforce it?** A: Declare variables/parameters as the interface type so you can swap implementations without touching callers. Factory Method (returns interface type), Abstract Factory, Strategy, and Observer all structurally *force* this. It's the implementation of Dependency Inversion (Part 06).
11. **Q: Can a pattern be implemented "wrong" and still look right? (Tricky)** A: Yes — a *false* pattern: you copy the class diagram but miss the intent (e.g., a "Strategy" with only one implementation that never changes, or a "Singleton" whose constructor is not private). The tell is when removing the pattern's indirection would not change any behavior. Interviewers probe this by asking "what problem does this pattern solve in YOUR code?"
12. **Q: Why do patterns matter in low-level design (LLD) interviews?** A: Because LLD is scored on *design quality*: coupling, extensibility, and whether your choices are *defensible*. Naming a pattern (and its consequences) is how you demonstrate the design is deliberate rather than accidental. Interviewers ask "why did you choose X pattern" and expect trade-off reasoning.
13. **Q: A colleague proposes adding the Observer pattern to a class with one fixed subscriber that will never change. Is this good design? (Production)** A: No — this is pattern over-application. Observer's value is *dynamic* publisher→subscriber decoupling with an unknown number of changing listeners. With one fixed subscriber, a direct call is simpler, faster, and clearer. Over-applying patterns adds indirection without benefit — reviewers reject it.
14. **Q: Do patterns change time complexity?** A: No. They are structural; they reorganize responsibility, not computation. They add O(1) constant-factor indirection (extra calls/pointers) and O(N) classes, but the algorithmic complexity of the underlying operations is unchanged.
15. **Q: Why is a pattern better than an experienced engineer's "gut feeling"?** A: Because a pattern is gut feeling that has been *written down, named, and vetted* — it's transferable across teams, it can be taught, reviewed, and even linted (structural checks). A gut feeling lives in one head and dies with it.
16. **Q: Which came first, the pattern or the book that named it?** A: The pattern. The GoF book (1994) *cataloged* and *named* structures already used in production Smalltalk/C++ systems. Patterns are discovered in practice, then documented. This is why they're so reliable — they survived real systems.
17. **Q: Is "MVC" (Model-View-Controller) one of the 23 GoF patterns? (Tricky)** A: No. MVC is a *larger architectural pattern* (a composite of Observer + Strategy + Composite applied at a higher level: View observes Model, View uses Strategy for input handling, View is a Composite of widgets). The GoF book actually discusses MVC as a case study of pattern *composition*. Interviews distinguish GoF design patterns from architectural patterns (MVC, layered, event-driven).
18. **Q: Your manager says "we don't use patterns here, just write clean code." How do you respond? (Scenario)** A: Agree that clean code matters, then note patterns *are* the documented forms of clean design for recurring problems — and that you're not proposing to force patterns in, just to use recognized names when the problem genuinely recurs. The goal is the same: low coupling, high cohesion, and maintainability; patterns are vocabulary, not dogma.
19. **Q: What's the relationship between patterns and the SOLID principles?** A: SOLID states the *laws* (Open-Closed: open for extension, closed for modification; Dependency Inversion: depend on abstractions). Patterns provide the *standard mechanisms* that obey the laws. Strategy/Decorator are standard "open-closed" mechanisms; Factory/Abstract Factory are standard dependency-inversion mechanisms.
20. **Q: How do you decide whether to use a pattern at all? (Production)** A: A 3-question test: (1) Is this a *recurring* problem I've seen before, or a one-off? (2) Is there a predicted axis of change that the pattern localizes? (3) Does the pattern's cost (indirection, classes) buy more than it costs? If all three say yes → apply it; otherwise, write the simple code.

## 14. Follow-Up Questions
1. **Q: What's the difference between pattern *intent* and pattern *implementation*?** A: Intent is *why/what* ("ensure one instance"); implementation is *how* ("private constructor + static getter"). Two implementations of the same intent can look completely different (eager vs lazy vs enum singleton). Interviews test intent; wrong implementations of the right intent still count as the pattern.
2. **Q: Which GoF principle says "encapsulate what varies"?** A: That's the general *design principle* behind patterns: find what changes and isolate it behind an interface. Strategy encapsulates the varying algorithm; Factory encapsulates the varying creation; Facade encapsulates the varying subsystem. It's the foundation of Part 06's Open-Closed principle.
3. **Q: How do patterns relate to "simplicity" / YAGNI?** A: YAGNI says don't build what you don't need — so don't apply a pattern *until* the variation actually appears or is strongly predicted. Patterns applied early "just in case" violate YAGNI; patterns applied when the second implementation actually arrives are earned, not premature.
4. **Q: Can two different patterns solve the same problem?** A: Yes — e.g., "swappable algorithm" can be Strategy (composition + delegation) or Template Method (inheritance + overridden hooks); the choice depends on whether you want to change whole algorithms (Strategy) or just steps of a fixed algorithm (Template Method). Recognizing the *shared problem* behind two candidate patterns is a senior-level skill.
5. **Q: What is the "Golden Hammer" anti-pattern and how does it relate to patterns?** A: The Golden Hammer is over-relying on one familiar tool/pattern for every problem. If you reach for Singleton for everything, you're a golden-hammer user. Pattern maturity = knowing *when NOT* to use each pattern.

## 15. Coding Example
```java
// A minimal, real Strategy implementation (also see Section: Strategy Pattern)
interface PaymentStrategy {
    void pay(double amount);
}

class CreditCard implements PaymentStrategy {
    public void pay(double amount) { System.out.println("Paid $" + amount + " via Credit Card"); }
}
class UpiPayment implements PaymentStrategy {
    public void pay(double amount) { System.out.println("Paid $" + amount + " via UPI"); }
}

class Checkout {
    private PaymentStrategy strategy;
    public Checkout(PaymentStrategy s) { this.strategy = s; }
    public void setStrategy(PaymentStrategy s) { this.strategy = s; } // swap at runtime
    public void checkout(double amount) { strategy.pay(amount); }
}

public class Main {
    public static void main(String[] args) {
        Checkout co = new Checkout(new CreditCard());
        co.checkout(150.0);              // Paid $150.0 via Credit Card
        co.setStrategy(new UpiPayment()); // runtime swap
        co.checkout(250.0);              // Paid $250.0 via UPI
    }
}
```
```python
# The same Strategy shape in Python (Python 3.10+, structural typing optional)
from typing import Protocol

class PaymentStrategy(Protocol):
    def pay(self, amount: float) -> None: ...

class CreditCard:
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount} via Credit Card")

class UpiPayment:
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount} via UPI")

class Checkout:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy
    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy
    def checkout(self, amount: float) -> None:
        self._strategy.pay(amount)

co = Checkout(CreditCard())
co.checkout(150.0)                    # Paid $150.0 via Credit Card
co.set_strategy(UpiPayment())
co.checkout(250.0)                    # Paid $250.0 via UPI
```
```cpp
// The same Strategy shape in C++ (interface via abstract base class)
#include <iostream>
#include <memory>

class PaymentStrategy {  // abstract
public:
    virtual void pay(double amount) const = 0;
    virtual ~PaymentStrategy() = default;
};

class CreditCard : public PaymentStrategy {
public:
    void pay(double amount) const override {
        std::cout << "Paid $" << amount << " via Credit Card\n";
    }
};
class UpiPayment : public PaymentStrategy {
public:
    void pay(double amount) const override {
        std::cout << "Paid $" << amount << " via UPI\n";
    }
};

class Checkout {
    std::shared_ptr<PaymentStrategy> strategy_;
public:
    explicit Checkout(std::shared_ptr<PaymentStrategy> s) : strategy_(std::move(s)) {}
    void setStrategy(std::shared_ptr<PaymentStrategy> s) { strategy_ = std::move(s); }
    void checkout(double amount) const { strategy_->pay(amount); }
};

int main() {
    Checkout co(std::make_shared<CreditCard>());
    co.checkout(150.0);
    co.setStrategy(std::make_shared<UpiPayment>());
    co.checkout(250.0);
}
```

## 16. Industry Usage
- **Every production OO codebase** uses patterns whether or not the team names them — Java's `Collections.sort(List, Comparator)` is Strategy; `InputStream` wrapping is Decorator; Spring's entire container is Factory + Singleton + Proxy.
- **Java standard library (JDK)**: `java.util.Observable`/`Observer` (Observer), `java.util.Iterator` (Iterator), `Collections.unmodifiableList` (Facade), `BufferedReader` over `Reader` (Decorator), `Calendar.getInstance()` (Factory Method / Singleton-ish).
- **Spring Framework**: bean container = Abstract Factory + Singleton; `@Transactional` = Proxy (AOP); `ApplicationContext` = Facade over bean creation and wiring; `Environment` abstraction = Strategy for property resolution.
- **Large systems**: Netflix's Hystrix uses Command (wrapping each downstream call as a command with fallbacks); Kafka's consumer config uses Strategy-like pluggable deserializers; virtually every UI toolkit (Java Swing, React, Flutter) is built on Observer/Composite/State.
- **Design reviews at FAANG/MAANG**: interviewers and reviewers constantly name patterns — a review comment saying "this should be a Facade over these three SDKs, and the SDK-specific code should live behind it" is pattern vocabulary in action.

## 17. References
- **Gamma, Helm, Johnson, Vlissides (Gang of Four), *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994** — the canonical catalog; chapters 1–2 define the pattern concept and the composition-over-inheritance, program-to-interface principles.
- **Freeman et al., *Head First Design Patterns*, 2nd ed. (2020)** — the approachable deep-dive; each pattern with problem → solution → example.
- **Erich Gamma et al. — GoF "Design Patterns CD" & the original "Design Patterns" paper (1987–94)** — for the historical context of pattern *discovery*.
- **Christopher Alexander, *A Pattern Language* (1977)** — the architectural origin of the pattern concept (context/problem/solution).
- **refactoring.guru — "Design Patterns" (Refactoring GURU)** — modern, free, pattern-by-pattern reference with Java/C++/Python examples.
- **Martin Fowler, *Patterns of Enterprise Application Architecture* (2002)** — the enterprise/architectural extension beyond GoF.
- **Baeldung, "Design Patterns in Java"** — practical tutorials mapping patterns to JDK/Spring usage.
- **Oracle Java Tutorials — "Collections and Design Patterns" (docs.oracle.com/javase/tutorial/collections/)**
- **Wikipedia: "Design pattern" / "Software design pattern"** — for the general theory and history.

## 18. Cheat Sheet
- Pattern = **name + problem + solution + consequences**; it is a *shape*, not code.
- It exists for **vocabulary, reuse of proven design, and consistency** across teams.
- **3 families**: Creational (5) / Structural (7) / Behavioral (11) = the 23 GoF patterns.
- Patterns ≠ algorithms (no Big-O; structural trade-offs instead) and ≠ frameworks (shapes vs concrete systems).
- **Golden rules**: "program to an interface, not an implementation"; "favor composition over inheritance"; "encapsulate what varies".
- Anti-pattern = documented *bad* solution (God Object, Spaghetti Code, Singleton abuse).
- Apply a pattern when the problem **recurringly matches**; otherwise it's indirection without benefit (YAGNI).
- Always be able to answer: **what problem does this pattern solve, and what trade-off does it accept?**
- Pattern families predict *where change is expected*: birth (creational) / composition (structural) / behavior & communication (behavioral).

## 19. Quiz
1. Which of the following is NOT one of the four essential elements of a GoF pattern? a) Name b) Problem c) Big-O complexity d) Consequences → **c**
2. The 23 GoF patterns are divided into which families? a) 5/7/11 b) 6/8/9 c) 10/8/5 d) 4/10/9 → **a**
3. "Favor composition over inheritance" is: a) a GoF design principle b) a Java keyword c) an anti-pattern d) a creational pattern → **a**
4. Which statement is TRUE? a) Patterns change algorithmic time complexity b) Patterns are copied code c) Patterns are reusable *design* shapes d) Patterns must be implemented with inheritance → **c**
5. A framework differs from a pattern because: a) a framework is smaller b) a pattern is a concrete system you live inside c) a framework is a concrete system that inverts control; a pattern is a shape you apply d) they are the same thing → **c**
6. "God Object" is an example of: a) a structural pattern b) an anti-pattern c) a creational pattern d) a GoF principle → **b**
7. Which of the following is an *architectural* pattern, not one of the 23 GoF patterns? a) Singleton b) MVC c) Adapter d) Observer → **b**
8. When is applying a pattern premature? a) when the variation it localizes is strongly predicted b) when the recurring problem is present c) when no axis of change exists yet (YAGNI) d) when the team knows the pattern name → **c**
9. "Program to an interface, not an implementation" most directly supports which SOLID principle? a) Single Responsibility b) Open-Closed c) Liskov d) Dependency Inversion → **d**
10. The GoF book (1994) primarily: a) invented the patterns it documents b) cataloged and named patterns already used in production systems c) replaced all algorithms d) defined a new programming language → **b**

## 20. Flashcards
- **Q: What is a design pattern?** → **A:** A named, reusable, documented solution to a recurring design problem, expressed as context/problem/solution/consequences.
- **Q: What are the four essential GoF elements of a pattern?** → **A:** Name, Problem, Solution, Consequences.
- **Q: Name the three GoF families and their counts.** → **A:** Creational (5), Structural (7), Behavioral (11) = 23 patterns.
- **Q: Pattern vs algorithm?** → **A:** Pattern = structural shape with trade-offs (design reuse); algorithm = step-by-step procedure with Big-O (computation).
- **Q: Pattern vs framework?** → **A:** Pattern = reusable shape applied in your code; framework = concrete semi-complete system with inversion of control that you live inside.
- **Q: What is an anti-pattern?** → **A:** A documented bad solution that seems tempting but leads to problems (e.g., God Object, Spaghetti Code).
- **Q: The two GoF design principles most patterns follow?** → **A:** Program to an interface, not an implementation; favor composition over inheritance.
- **Q: What does "encapsulate what varies" mean?** → **A:** Identify the axis of change and isolate it behind an interface so the rest of the code stays unchanged.

## 21. Revision
Design patterns are **named, reusable solutions** to recurring design problems, captured as context/problem/solution/consequences. They exist to give teams a shared vocabulary, to reuse *proven design* rather than reinvent it, and to encode "encapsulate what varies" + "favor composition over inheritance". The 23 GoF patterns split into creational (5: how objects are born), structural (7: how objects are composed), and behavioral (11: how objects communicate/cooperate). They are shapes, not code — applying one means mapping its participants onto your classes — and they do NOT change time complexity, only structure and indirection. Use them when the problem genuinely recurs and a change axis is predicted (YAGNI otherwise); misuse produces anti-patterns and "false patterns". In interviews, always be ready to state a pattern's *intent* and *trade-off*, and to name real framework examples (Spring = factory/singleton/proxy; Java I/O = decorator; `java.util.Observable` = observer).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a design pattern and why do they exist?" | 1 Why / 7 Formal Definition / 8 Example |
| "What are the four essential elements of a GoF pattern?" | 2 How It Works / 7 Formal Definition |
| "Name the 3 families of GoF patterns and their counts." | 2 How It Works / 18 Cheat Sheet |
| "Pattern vs algorithm vs framework?" | 4 Alternatives / 13 Q5 |
| "What is an anti-pattern?" | 13 Q6 / 18 Cheat Sheet |
| "Program to an interface vs implement to a class — why?" | 13 Q10 / 5 Intuition |
| "Why does the team name patterns in design reviews?" | 3 When Used / 16 Industry Usage |
| "Would you use a pattern here? (LLD scenario)" | 13 Q13/Q20 / 9 Internal Working |
| "Do patterns affect Big-O?" | 10 Time Complexity / 13 Q14 |
| "Is MVC a GoF pattern?" | 13 Q17 |
