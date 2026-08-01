# GoF Patterns Overview and Categorization

> **TL;DR**: The Gang of Four cataloged **23 patterns** split into **creational (5)**, **structural (7)**, and **behavioral (11)** families — the categorization exists so that a designer can instantly navigate the catalog by the question they're answering: "how is an object born?", "how are objects composed?", or "how do objects coordinate?".

## 1. Why Does This Exist?
The 23 patterns needed to be **organized**, not just listed. A flat list of 23 names is un-navigable; an engineer facing a design tension has no way to find the relevant pattern. The GoF categorization exists to give a **decision structure**: it groups patterns by the *kind of design problem* they solve, so you can rule out 16 patterns instantly and focus on the 5-7 candidates from the right family. It also provides the *criteria* for the decision — creational vs structural vs behavioral tells you *where the variation lives* in your design, which is the deeper question behind every pattern choice.

The three families answer three distinct questions that arise in any OO design:
- **Creational**: How and who *creates* the objects? (Does the client name concrete classes? Is creation costly? Is uniqueness required?)
- **Structural**: How are *classes and objects composed* to form larger structures, while keeping the structure flexible? (Do we need to change an interface? Add behavior without subclassing? Hide a subsystem?)
- **Behavioral**: How do *objects distribute responsibility and communicate* with each other? (Who initiates behavior? How is an algorithm varied? How is state encapsulated?)

## 2. How Does It Work?
The taxonomy works as a **two-axis map**:

- **Axis 1 — Purpose**: what the pattern does → Creational / Structural / Behavioral.
- **Axis 2 — Scope**: whether the pattern applies to **classes** (via inheritance, decided at compile time) or **objects** (via composition, decided at run time).

| Family | Purpose | Class-scope (inheritance) | Object-scope (composition) |
|---|---|---|---|
| **Creational (5)** | How objects are created | Factory Method | Abstract Factory, Builder, Prototype, Singleton |
| **Structural (7)** | How classes/objects are composed | Adapter (class form) | Adapter (object form), Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| **Behavioral (11)** | How objects communicate/cooperate | Template Method, Interpreter | Strategy, Observer, Command, State, Iterator, Memento, Mediator, Chain of Responsibility, Visitor |

Within a family, patterns differ by **what exactly they encapsulate**:
- Creational: what is created, who creates it, how many, how it's assembled.
- Structural: how the *interfaces* match (Adapter), how *behavior* is added (Decorator), how *subsystems* are hidden (Facade), how *access* is controlled (Proxy).
- Behavioral: which *algorithm* runs (Strategy), who gets *notified* (Observer), what a *request* is (Command), which *state* is active (State), how a collection is *traversed* (Iterator).

The map "works" because picking a family first (2 questions: "Is creation the problem? Is composition the problem? Is communication the problem?") reduces the catalog to 5-11 candidates, then each pattern's specific intent narrows to the one that matches.

## 3. When Is It Used?
- **When you hit a design tension**: creation noise (new concrete classes everywhere) → look at the 5 creational patterns; interface/behavior mismatch between objects → the 7 structural; communication/algorithm variation → the 11 behavioral.
- **In LLD interviews** — the categorization is the standard "thinking out loud" structure: "the variation here is in how objects are created, so let's consider creational patterns."
- **When reading framework code**: recognizing "this is a Factory" means you know *why* the framework exposes a `getInstance()`/`create()` API and not constructors — the taxonomy trains recognition.
- **In code reviews**: "this subsystem needs a Facade" is a structural statement; "these algorithms should be Strategies" is a behavioral statement. The taxonomy gives reviewers precise vocabulary.
- **When extending a codebase**: the family tells you *which* patterns the codebase already leans on (e.g., if everything is a strategy, the codebase bets on behavior variation).

## 4. Why Wasn't Another Approach Chosen?
- **No categorization (a flat list)**: rejected because it gives no search structure — you'd scan 23 names trying to remember what each does. A map is a navigation aid, not decoration.
- **Categorizing by *language feature*** (e.g., "patterns using polymorphism" / "patterns using inheritance"): rejected because the same pattern can be implemented with or without inheritance in different languages, so the category would be unstable.
- **Categorizing by *consequence*** (patterns that reduce coupling vs increase flexibility): rejected because patterns usually have multiple consequences; the classification would be ambiguous (Observer both decouples and is a communication pattern).
- **Categorizing by *domain*** (UI patterns, persistence patterns, concurrency patterns): rejected because the GoF patterns are domain-independent — their whole value is that they apply anywhere.
- **Categorizing by *"where change is localized"***: this is actually the *motivation* behind the three families (birth / composition / behavior), but GoF chose purpose+scope because those are *objective properties of the pattern itself*, while "where change happens" is a property of your *application*. Purpose+scope is stable; the change axis is contextual.

## 5. Intuition
Think of the catalog as a **hospital's department map**: when something's wrong, you don't read every doctor's profile — you ask "is it a heart problem? a bone problem? a brain problem?" and walk to the right department. Creational is the **maternity ward** (things being born), structural is the **construction/orthopedics wing** (how parts are put together to make a working body), behavioral is the **communications/neurology ward** (how parts send signals and coordinate). Within a department, the specific clinic is chosen by your exact symptom. The taxonomy is a *triage system*: family first, pattern second.

The second intuition: **every pattern is a bet on where change will happen** (from Section 01). The families make that bet explicit:
- Creational → *"I bet new object types will be added, or creation will get complicated."*
- Structural → *"I bet the way objects are composed/matched/interfaced will change."*
- Behavioral → *"I bet the algorithms, state machines, or communication flows will change."*

## 6. Real-World Analogy
A **restaurant kitchen as the pattern catalog**. *Creational* patterns are the **sous-chef station**: the kitchen never has every dish pre-made; it decides *how and when* to create each plate (one dessert per table — Singleton; a pastry with many configurable layers — Builder; a burger you clone for speed — Prototype). *Structural* patterns are the **expediting/pass and plating**: how dishes are composed, how a power adapter lets an incompatible appliance plug in (Adapter), how a garnish decorates a plate without changing the base recipe (Decorator), how the kitchen hides its mess behind a menu (Facade), how a waiter is the proxy who takes orders on the chef's behalf (Proxy). *Behavioral* patterns are the **front-of-house coordination**: waiters (Observers) are notified when the kitchen (Subject) runs out of a dish; the manager (Strategy) switches the specials strategy daily; orders (Command) are tickets queued and reversible. Same kitchen, three different questions — and each department has its own experts.

## 7. Formal Definition
Per the GoF catalog, a design pattern's **category** (purpose) classifies what it does — **Creational** patterns concern the *process of object creation*; **Structural** patterns concern the *composition of classes or objects*; **Behavioral** patterns concern the *interaction or responsibility distribution between classes or objects*. The **scope** classifies whether the pattern applies to **classes** (relationships established via *inheritance*, fixed at compile time) or to **objects** (relationships established via *composition*, fixed at run time). The GoF book organizes its catalog by these two criteria: purpose (creational/structural/behavioral) × scope (class/object), giving each pattern a deterministic location in the 3×2 grid.

## 8. Example
Take a concrete production tension and walk the triage:
- **Tension**: "My `NotificationService` uses `new EmailSender()`, `new SmsSender()`, `new PushSender()` directly. I keep adding channels, and every addition forces me to reopen `NotificationService`." 
- **Triage — family?** The variation is in *object creation* (which sender object to make) → **Creational**.
- **Within creational**: "do I want to defer which concrete class is made to subclasses?" → **Factory Method**; "do I want to provide one family of related products (email+sms+push as a suite) without naming concrete classes?" → **Abstract Factory**; "is the object expensive to make and worth pooling?" → **Prototype/Object Pool**.
- **Chosen**: Factory Method. `NotificationService` depends on an `SenderFactory.create(...)` that returns `Sender` (interface); adding a channel = adding a factory branch, never touching `NotificationService`.
- **Result**: the Open-Closed property comes from choosing the *right family first* (creation) — the categorization made the 23-name catalog collapse to 5 candidates, then to 1.

## 9. Internal Working
The categorization is a *search structure*; here's the exact decision procedure a senior engineer runs internally:

1. **State the tension precisely** (one sentence: what varies, what breaks today).
2. **Map to a family** — ask three questions in order:
   - *"Is the pain about creating objects?"* (naming concrete classes, expensive construction, uniqueness, complex assembly) → **Creational** (5).
   - *"Is the pain about composing/matching/interfacing existing objects?"* (incompatible interfaces, adding behavior without subclasses, hiding a subsystem, controlling access, uniform trees) → **Structural** (7).
   - *"Is the pain about behavior/communication?"* (algorithm selection, publish/subscribe, request as object, state machines, traversal, snapshots) → **Behavioral** (11).
3. **Within the family, narrow by sub-question** — e.g., within creational: *"is the problem 'which class'?"* → Factory Method; *"a family of products?"* → Abstract Factory; *"stepwise assembly of a complex object?"* → Builder; *"copying an expensive prototype?"* → Prototype; *"exactly one instance?"* → Singleton.
4. **Validate against consequences** — confirm the pattern's trade-offs are acceptable (indirection, class count, coupling reduction) and that no simpler non-pattern solution suffices.
5. **Name it and document intent** — the decision, and the two or three rejected alternatives, become the design narrative for the review.

This procedure is the *mechanism*: family → pattern → validate. It's exactly what interviewers score when you "think out loud" during LLD.

## 10. Time Complexity
The categorization itself has no runtime cost — it's a design-time search structure. But it produces a predictable *structural complexity*:

- Number of patterns to compare at step 2: **3 families** (O(1) decision).
- Candidates after family selection: **5 / 7 / 11** patterns (bounded, constant).
- Number of classes the chosen pattern adds: O(1) per role (e.g., Strategy adds 1 interface + N concrete classes; Observer adds 1 interface + 1 collection in the subject).
- Maintenance scanning cost: with N classes in the system, a *named* pattern reduces review/skimming cost from O(N) (must read everything) to O(1) per pattern (read the pattern's participants only) — this "understanding cost" reduction is the real asymptotic win of the taxonomy.
- Runtime indirection: each pattern layer adds O(1) virtual dispatch and pointer traversal (see Section 01, block 10).

## 11. Advantages
- **Navigation**: a 23-item catalog becomes a 3-branch decision tree; candidates collapse to 5-11 then to 1-2.
- **Prediction of variation**: the family tells you *which axis of change* the pattern bets on, aligning pattern choice with requirement forecasts.
- **Uniform language**: "a structural problem" instantly conveys the class of tension to reviewers.
- **Cross-language stability**: the taxonomy is language-independent (class vs object scope applies everywhere), so your knowledge transfers from Java to C++ to Python.
- **Interview leverage**: LLD rounds reward *showing the triage* ("the variation is in creation → creational family → Factory Method") — this is a demonstrable, repeatable skill.
- **Prevents force-fitting**: knowing the family boundaries makes it obvious when a candidate pattern is in the wrong family for the problem.

## 12. Disadvantages
- **Over-simplification risk**: some patterns straddle families in practice (e.g., Singleton is classified creational but is often used as a structural/global-access pattern; Composite is structural but its traversal is behavioral). Interviewers probe this nuance.
- **Doesn't answer "which one" by itself**: family selection leaves 5-11 candidates; the taxonomy alone doesn't pick the pattern — you still need intent-level analysis.
- **Class-vs-object scope is less relevant in modern languages**: dynamic languages (Python/JS) blur compile-time vs run-time scope, so the second axis is less meaningful there (Part 08).
- **Not the only taxonomy**: other classifications exist (by consequence, by implementation language, by "intent"), so dogmatism can confuse.
- **Memorization trap**: candidates memorize the table (5/7/11) without the *triage questions* — memorizing numbers is useless if you can't run the decision procedure.

## 13. Interview Questions
1. **Q: How many GoF patterns are there and how are they categorized?** A: 23, in three purpose-based families — creational (5: Factory Method, Abstract Factory, Builder, Prototype, Singleton), structural (7: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy), behavioral (11: Template Method, Interpreter, Strategy, Observer, Command, State, Iterator, Memento, Mediator, Chain of Responsibility, Visitor).
2. **Q: What distinguishes a creational from a structural from a behavioral pattern?** A: Creational patterns abstract the *process of object creation* (what/who/how-many); structural patterns abstract the *composition of classes and objects* (interface matching, wrapping, subsystem hiding); behavioral patterns abstract *communication and responsibility distribution* between objects.
3. **Q: What is the class-vs-object scope distinction?** A: Class-scope patterns use *inheritance* (relationships fixed at compile time; e.g., class Adapter, Template Method); object-scope patterns use *composition* (relationships fixed at run time; e.g., object Adapter, Strategy, Decorator). Object-scope patterns are more flexible and dominate modern code.
4. **Q: Which family would you pick for "adding a new type of product must not touch existing client code"?** A: Creational — Factory Method/Abstract Factory defer product instantiation, so new products appear in new factory branches, leaving clients unchanged (Open-Closed).
5. **Q: Which family handles "we can't change class X but need to call it with interface Y"?** A: Structural — specifically Adapter, which converts one interface to the one the client expects.
6. **Q: "Decouple a sender from its receivers" — which family and which pattern?** A: Behavioral — Observer (publish/subscribe). The subject knows only the Observer interface, so receivers can be added/removed at run time.
7. **Q: Name three structural patterns and the one-line problem each solves.** A: Adapter (make incompatible interfaces work together), Decorator (add behavior to an object without subclassing), Proxy (control access to an object / defer its creation). Others: Facade (hide a subsystem), Composite (treat trees uniformly), Bridge (decouple abstraction from implementation), Flyweight (share fine-grained objects).
8. **Q: Is Singleton creational even though it looks like "global access"? (Tricky)** A: Yes — the GoF classifies it as creational because its *intent* is to control the instantiation process (guarantee exactly one instance and provide a global access point). The "global access" aspect is a *consequence*, not the intent — an interviewer will flip this to test whether you know intent vs consequence.
9. **Q: What question does each family answer? (Scenario: think out loud)** A: Creational → "how is an object created, by whom, how many?"; Structural → "how are objects composed into a larger structure while staying flexible?"; Behavioral → "how do objects communicate and distribute responsibility?"
10. **Q: In an LLD round, you say "this is a creational problem." Walk me through your next two steps. (Production)** A: First narrow within creational by sub-question: which-class (Factory Method), product-family (Abstract Factory), complex stepwise build (Builder), expensive copy (Prototype), uniqueness (Singleton). Then validate consequences: indirection cost, class count, and whether the predicted change axis actually exists.
11. **Q: Which pattern is in the "wrong" family, and why? (Tricky)** A: Candidates argue Composite (structural, but traversal logic is behavioral-ish) and Singleton (creational, but used as a global state holder). The correct answer shows you know the *classification rule* (purpose) and that a pattern's dominant purpose determines its class even if secondary aspects cross families.
12. **Q: Why isn't there a "concurrency" family in GoF?** A: The GoF book (1994) predates the mainstream concurrency revolution; concurrency patterns were cataloged later (e.g., the "Pattern-Oriented Software Architecture" series, and Java's `java.util.concurrent` — e.g., thread pool, producer-consumer). Concurrency is a *concern that cross-cuts* all three families rather than a fourth family.
13. **Q: Class Adapter vs object Adapter — which is used more and why?** A: Object Adapter (composition — adapts by holding a reference to the adaptee) is far more common because it doesn't require multiple inheritance, adapts the adaptee's *subclasses* too, and follows "favor composition over inheritance". Class Adapter needs multiple inheritance and binds to one concrete class.
14. **Q: Which family do Mediator and Chain of Responsibility belong to, and why together?** A: Behavioral — both reorganize *communication*: Mediator centralizes interactions between many objects; Chain of Responsibility passes a request along a chain until one handles it. Both exist to decouple *who talks to whom*.
15. **Q: How do the families map to "where change is expected"?** A: Creational bets creation will change (new products); structural bets composition/interface matching will change; behavioral bets algorithms/state/communication will change. Your requirement forecast determines the family, then the pattern.
16. **Q: The interviewer says "design a logging system." Which family should dominate? (Scenario)** A: Behavioral — the algorithm for formatting/output (Strategy), optional chaining of handlers (Chain of Responsibility), and decoupling loggers from sinks (Observer/Strategy). Creational (factory for loggers) and structural (proxy/decorator for lazy or async logging) may *assist*, but the core variations are behavioral.
17. **Q: Are Flyweight and Proxy both "indirection"? What's the difference? (Tricky)** A: Both add indirection, but Flyweight's intent is *memory sharing* of fine-grained immutable objects (it reduces object count), while Proxy's intent is *access control / lazy loading / remote access*. Sharing vs controlling access — different intents, same family (structural).
18. **Q: Does the taxonomy change when the language doesn't have inheritance? (Production)** A: Somewhat — class-scope patterns (Template Method, class Adapter) weaken in languages without multiple inheritance or with dynamic dispatch differences; but object-scope patterns (Strategy, Decorator, Proxy) work everywhere via interfaces/duck-typing (Python/JS use them constantly). The *purpose* axis is universal.
19. **Q: How do you *prove* you understand the categorization in an interview rather than memorize it?** A: Run the triage on a fresh scenario: state the tension, name the family and the sub-question that selects the pattern, and state the consequence you're accepting. That's the difference between reciting the table and using it.
20. **Q: Name one pattern from each family and its real-world JDK/Spring instance.** A: Creational — Abstract Factory: `javax.xml.parsers.DocumentBuilderFactory.newInstance()`; Spring's `BeanFactory`. Structural — Decorator: `BufferedReader(Reader)` wrapping; Proxy: Spring AOP `@Transactional`. Behavioral — Observer: `java.util.Observable`; Strategy: `Collections.sort(List, Comparator)`; Command: `Runnable`/`Callable`.

## 14. Follow-Up Questions
1. **Q: Why is Template Method the classic "class-scope" behavioral pattern?** A: Because it fixes the *algorithm skeleton* in a base class and lets subclasses override only specific *steps* (hooks) — the relationship is inheritance, established at compile time. Its close cousin Strategy achieves the same "vary an algorithm" goal by composition instead, which is why Strategy is object-scope and usually preferred for flexibility.
2. **Q: What's the difference between an *intent* grouping and the GoF's *purpose* grouping?** A: Intent groupings (e.g., "patterns that promote loose coupling": Observer, Mediator, Facade, Proxy) cut across families; the GoF purpose grouping is one *consistent rule* (what the pattern *does*). Interviewers use both — they may ask "which patterns reduce coupling?" (cross-family) vs "which family handles communication?" (purpose-based).
3. **Q: How would you explain the 3×2 grid to a non-technical stakeholder?** A: Three kinds of questions any system must answer — "how are things made?" (5 answers), "how do things fit together?" (7 answers), "how do things talk and share work?" (11 answers) — and for each answer, whether it's baked in at build time (class) or decided at run time (object).
4. **Q: Does the "5/7/11" split ever change across pattern books?** A: Other catalogs extend it (Fowler's PoEAA adds enterprise patterns; concurrency catalogs add locking/threading patterns), but the *core 23* are stable as the canonical GoF set. Saying "23 GoF patterns" is standard; mentioning that later catalogs extend the *principle* is senior-level breadth.
5. **Q: Composite is structural, but recursion over a composite is a traversal. Where does traversal responsibility live?** A: Traversal is usually delegated to a *behavioral* pattern — the Iterator — over the composite structure. This is a classic example of *pattern composition*: one structural pattern (Composite) defines the tree; a behavioral pattern (Iterator) defines how to walk it.

## 15. Coding Example
```java
// A single codebase exercising all three families in miniature.
// (Full implementations appear in the dedicated pattern sections.)

// CREATIONAL — Factory Method: defer which Notifier is created
interface Notifier { void notify(String msg); }
class EmailNotifier implements Notifier { public void notify(String m) { System.out.println("EMAIL: " + m); } }
class SmsNotifier implements Notifier { public void notify(String m) { System.out.println("SMS: " + m); } }

class NotifierFactory {
    public static Notifier create(String type) {        // creational
        return switch (type) {
            case "email" -> new EmailNotifier();
            case "sms"   -> new SmsNotifier();
            default      -> throw new IllegalArgumentException("unknown: " + type);
        };
    }
}

// STRUCTURAL — Decorator: add behavior to a Notifier without subclassing
class LoggingNotifier implements Notifier {             // structural (wraps)
    private final Notifier inner;
    LoggingNotifier(Notifier inner) { this.inner = inner; }
    public void notify(String m) { System.out.println("[LOG] sending " + m); inner.notify(m); }
}

// BEHAVIORAL — Observer: many listeners, decoupled
import java.util.*;
class AlertSystem {                                      // Subject
    private final List<Notifier> listeners = new ArrayList<>();
    void subscribe(Notifier n) { listeners.add(n); }
    void raiseAlert(String msg) { for (Notifier n : listeners) n.notify(msg); }  // behavioral
}

public class Main {
    public static void main(String[] args) {
        Notifier email = NotifierFactory.create("email");        // creational
        AlertSystem alerts = new AlertSystem();
        alerts.subscribe(new LoggingNotifier(email));            // structural wrap
        alerts.subscribe(NotifierFactory.create("sms"));         // another notifier
        alerts.raiseAlert("Server down");                        // behavioral broadcast
    }
}
```

## 16. Industry Usage
- **The JDK itself is a pattern museum**: `Calendar.getInstance()` (Factory), `Runtime.getRuntime()` (Singleton), `BufferedInputStream(FileInputStream)` (Decorator), `Iterator` (Iterator), `Observable/Observer` (Observer), `Collections.unmodifiableX` (Facade/Wrapper), `Comparator` in `Collections.sort` (Strategy), `Runnable`/`Thread` (Command).
- **Spring Framework**: creational (BeanFactory/ApplicationContext = Factory + Singleton; `@Scope("prototype")`), structural (`@Transactional` AOP = Proxy; `Decorator` in response wrapping; `Facade` = `ApplicationContext`'s unified API), behavioral (Observer via `ApplicationListener`/`@EventListener`; Strategy via `Environment`/`MessageConverter` selection; Template Method in `JdbcTemplate` and `RestTemplate`'s `doExecute` hooks).
- **Netflix/Hystrix**: every remote call wrapped as a *Command* (behavioral) with fallback strategies.
- **UI frameworks (React, Flutter, Swing, Compose)**: State drives re-render (Observer on a state store); the widget tree is a *Composite*; rendering options are *Strategies*.
- **Distributed systems**: `Proxy` for remote services (RPC stubs), `Chain of Responsibility` in middleware pipelines (Koa/Express/ASP.NET), `Factory Method` in every ORM's repository/DAO creation (Hibernate, JPA).
- **Interviews**: LLD rounds at Google/Meta/Amazon/Microsoft routinely present scenarios and score your *family triage*: e.g., "design a vending machine" → state machine (behavioral, State pattern); "design an app where payment methods vary" → strategy/abstract factory; "design an API rate limiter" → strategy (algorithm selection) + singleton for shared state.

## 17. References
- **Gamma, Helm, Johnson, Vlissides, *Design Patterns*, Addison-Wesley, 1994** — Chapter 1 ("Introduction") section "Design Patterns in Smalltalk MVC" and the catalog organization table (p. 10: the pattern summary table by purpose/scope).
- **Erich Gamma, "Design Patterns: 15 Years Later" (2009 talks)** — the authors' own reflection on which patterns held up.
- **refactoring.guru — "Design Patterns"** — modern interactive taxonomy with Java/C++/Python.
- **Oracle Java SE Docs: `java.util.Observable`, `java.util.Iterator`, `java.util.Comparator`, `Collections.sort`** — https://docs.oracle.com/javase/8/docs/api/ (JDK pattern examples).
- **Spring Framework Reference, "The IoC Container"** — https://docs.spring.io/spring-framework/reference/core/beans.html (Factory/Singleton/Proxy usage).
- **SourceMaking — "Design Patterns"** — another free taxonomy with UML diagrams.
- **O'Reilly, "Head First Design Patterns" (2nd ed. 2020)** — the taxonomy presented as the "pattern toolkit" introduction.
- **WIKIPEDIA: "Design pattern (computer science)"** — history and the GoF 3×3 grid.

## 18. Cheat Sheet
- **23 patterns = 5 creational + 7 structural + 11 behavioral.**
- Creational (5): Factory Method, Abstract Factory, Builder, Prototype, Singleton → *how objects are born.*
- Structural (7): Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy → *how objects are composed.*
- Behavioral (11): Template Method, Interpreter, Strategy, Observer, Command, State, Iterator, Memento, Mediator, Chain of Responsibility, Visitor → *how objects communicate/cooperate.*
- Second axis: **class-scope** (inheritance, compile time) vs **object-scope** (composition, run time).
- Triage: name the tension → pick family (creation/composition/communication) → narrow by sub-question → validate consequences.
- "Is the problem which-class / a family / stepwise assembly / expensive copy / uniqueness?" → Factory Method / Abstract Factory / Builder / Prototype / Singleton.
- "Interface mismatch / add behavior / hide subsystem / control access / uniform tree?" → Adapter / Decorator / Facade / Proxy / Composite.
- "Vary algorithm / notify many / request as object / state machine / traverse?" → Strategy / Observer / Command / State / Iterator.
- JDK: `Comparator`=Strategy, `BufferedReader`=Decorator, `Runtime`=Singleton, `Observable`=Observer, `Iterator`=Iterator.
- "Which family handles X?" is a guaranteed interview question — always answer with the *sub-question* that pinpoints the pattern.

## 19. Quiz
1. How many patterns are in each GoF family (in order)? a) 7/8/8 b) 5/7/11 c) 5/9/9 d) 6/7/10 → **b**
2. Which pattern is CREATIONAL? a) Adapter b) Observer c) Factory Method d) Iterator → **c**
3. Which family handles "adding behavior to an object without subclassing"? a) Creational b) Structural c) Behavioral d) none → **b**
4. Which family handles "decouple a sender from its receivers"? a) Creational b) Structural c) Behavioral d) concurrency → **c**
5. Class Adapter vs object Adapter: which is more flexible? a) class (inheritance) b) object (composition) c) equally d) neither → **b**
6. Template Method belongs to which family? a) Creational b) Structural c) Behavioral d) class-scope behavioral → **d** (class-scope, behavioral family)
7. Which pattern is commonly used despite its family being "creational" and its consequence being "global access"? a) Builder b) Singleton c) Prototype d) Flyweight → **b**
8. The GoF second axis (scope) distinguishes: a) compile-time vs run-time relationships b) small vs large systems c) Java vs C++ d) coupling vs cohesion → **a**
9. A "vending machine" LLD scenario most directly needs which family? a) Creational b) Structural c) Behavioral (State) d) none → **c**
10. Which is NOT one of the 23 GoF patterns? a) Mediator b) Visitor c) MVC d) Chain of Responsibility → **c**

## 20. Flashcards
- **Q: 23 patterns = ?** → **A:** 5 creational + 7 structural + 11 behavioral.
- **Q: Name the 5 creational patterns.** → **A:** Factory Method, Abstract Factory, Builder, Prototype, Singleton.
- **Q: Name the 7 structural patterns.** → **A:** Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.
- **Q: Name the 11 behavioral patterns.** → **A:** Template Method, Interpreter, Strategy, Observer, Command, State, Iterator, Memento, Mediator, Chain of Responsibility, Visitor.
- **Q: Class-scope vs object-scope?** → **A:** Inheritance (compile-time) vs composition (run-time); object-scope is more flexible.
- **Q: "How is an object created" → which family?** → **A:** Creational.
- **Q: "Interface mismatch between two classes" → which pattern?** → **A:** Adapter (structural).
- **Q: "Notify many decoupled listeners" → which pattern?** → **A:** Observer (behavioral).

## 21. Revision
The GoF catalog is a **navigable taxonomy**: 23 patterns in three purpose families — creational (5: Factory Method, Abstract Factory, Builder, Prototype, Singleton) about *object birth*, structural (7: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy) about *object composition*, and behavioral (11: Template Method, Interpreter, Strategy, Observer, Command, State, Iterator, Memento, Mediator, Chain of Responsibility, Visitor) about *object communication/cooperation*. A second axis — class-scope (inheritance, compile time) vs object-scope (composition, run time) — makes the grid 3×2. Use the taxonomy as *triage*: name the tension → pick the family by the question it answers → narrow within the family by the pattern's specific intent → validate consequences. The taxonomy is design-time, so it adds no runtime complexity (only O(1) indirection when applied). JDK/Spring are pattern museums (`Comparator`=Strategy, `BufferedReader`=Decorator, Spring bean container=Factory+Singleton+Proxy) — cite them to prove recognition. Avoid the memorization trap: knowing 5/7/11 is useless unless you can run the triage and defend the choice in an LLD review.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How are the GoF patterns categorized?" | 2 How It Works / 7 Formal Definition |
| "Name the patterns in the creational family." | 8 Example / 18 Cheat Sheet |
| "Which family does X pattern belong to?" | 13 Q1–Q8 / 18 Cheat Sheet |
| "Class-scope vs object-scope — what's the difference?" | 2 How It Works / 13 Q3 / 14 Q1 |
| "Walk me through picking a pattern for this LLD scenario." | 9 Internal Working / 13 Q10 / 13 Q16 |
| "Is Singleton creational even though it's global access?" | 13 Q8 / 7 Formal Definition |
| "Why is there no concurrency family in GoF?" | 13 Q12 |
| "Pattern composition — Composite + Iterator?" | 14 Q5 |
| "Name a real JDK/Spring example per family." | 13 Q20 / 16 Industry Usage |
| "Class vs object Adapter — which is used more?" | 13 Q13 |
