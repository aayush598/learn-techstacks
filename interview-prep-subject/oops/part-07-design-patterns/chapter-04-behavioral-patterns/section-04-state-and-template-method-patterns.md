# State and Template Method Patterns

> **TL;DR**: The **State** pattern makes an object's behavior depend on its internal state, represented as state objects that the context **self-transitions** between (a state machine made of objects); the **Template Method** pattern fixes an algorithm's **skeleton** in a base class and lets subclasses override specific **steps** — State exists to replace `switch`-on-state with polymorphism, Template Method exists to avoid duplicating a fixed process across variants.

## 1. Why Does This Exist?
**State** exists because objects with lifecycle states (an order: PENDING → PAID → SHIPPED → DELIVERED; a TCP connection: CLOSED → LISTEN → SYN-SENT → ESTABLISHED; a vending machine: idle → has-money → dispensing) inevitably accumulate **`switch`/`if` chains on a status field**:
```java
void handle() {
    switch (state) {
        case PENDING: /* 20 lines */ break;
        case PAID:    /* 20 lines */ break;
        ...
    }
}
```
This violates Open-Closed (adding a state edits the switch), SRP (one method knows all states), and duplicates transitions. The State pattern replaces the switch with **polymorphism**: each state is a class implementing the same interface, and the context *delegates* behavior to its current state object, then **transitions to another state object** when events occur. The object's "mood" (state) drives behavior — and adding a state is adding a class.

**Template Method** exists because many algorithms are **mostly the same with a few varying steps**: a `JdbcTemplate` does open-connection → execute-SQL → map-rows → close — only the SQL and the row-mapping vary; a recipe makes a beverage as boil-water → brew-ingredient → pour-cup → add-extras — only brew/extras vary. Without the pattern, each variant duplicates the fixed process (copy-paste bugs) or the fixed process is buried inside each variant (hard to change globally). Template Method fixes the **skeleton in the base class** (the invariant process, called once) and declares **abstract/hook steps** that subclasses override — the base class drives the algorithm, subclasses fill in the blanks (inversion of control).

## 2. How Does It Work?
**State:**
```
Context (holds a State reference; delegates + transitions)
   │ has-a
   ▼
State (interface: handleEvent(context, event))
   ▲                 ▲                 ▲
ConcreteStateA   ConcreteStateB   ConcreteStateC
 (each may return/transition the context to another state)
```
```java
interface OrderState { void next(OrderContext ctx); void cancel(OrderContext ctx); }

class PendingState implements OrderState {
    public void next(OrderContext ctx) { ctx.setState(new PaidState()); }   // transition
    public void cancel(OrderContext ctx) { ctx.setState(new CancelledState()); }
}
class PaidState implements OrderState {
    public void next(OrderContext ctx) { ctx.setState(new ShippedState()); }
    public void cancel(OrderContext ctx) { ctx.setState(new RefundedState()); }
}
class OrderContext {
    private OrderState state;
    OrderContext() { this.state = new PendingState(); }
    void setState(OrderState s) { this.state = s; }
    void next() { state.next(this); }    // delegate
    void cancel() { state.cancel(this); }
}
```
- The context delegates `next()`/`cancel()` to its current state object; the state object *itself* decides the transition (self-transition — the key differentiator from Strategy).

**Template Method:**
```
AbstractClass: templateMethod() {
    step1();          // concrete (fixed)
    step2();          // abstract (must override)
    hook();           // hook (optional override)
    step3();          // concrete
}
ConcreteClassA/B override step2/hook
```
```java
abstract class DataParser {
    // TEMPLATE METHOD — fixes the skeleton
    public final void parse(InputStream in) {
        open(in);              // 1. fixed
        readHeader();          // 2. abstract step
        readBody();            // 3. abstract step
        close();               // 4. fixed
    }
    private void open(InputStream in) { /* open stream */ }
    protected abstract void readHeader();
    protected abstract void readBody();
    private void close() { /* close stream */ }
}
class CsvParser extends DataParser {
    protected void readHeader() { /* CSV header */ }
    protected void readBody() { /* CSV rows */ }
}
```

## 3. When Is It Used?
- **State**: any object with a well-defined lifecycle and state-dependent behavior — order workflows, TCP/connection states, vending machines, elevators, document lifecycle, game character states (idle/walk/attack), UI wizard steps. When `switch (state)` appears repeatedly → State pattern.
- **Template Method**: algorithms with a fixed invariant sequence and varying steps — JDBC/ORM templates (`JdbcTemplate`, `RestTemplate`), framework lifecycle hooks (servlet `service()` calling `doGet`/`doPost`), build pipelines, sorting framework (an abstract `sort()` delegating to `compare`), test frameworks (`JUnit` lifecycle), game engines (game-loop template), `java.util.AbstractList` (implements `List` operations on top of abstract `get`/`size`).
- **Interviews**: "state machine design (vending machine, order status)", "fixed process with varying steps", "how does `JdbcTemplate` work?" → State / Template Method.

## 4. Why Wasn't Another Approach Chosen?
**For State:**
- **`switch (state)` / enum with methods**: simplest for small, fixed states; rejected when the state set is open (new states from outside), when transitions are complex, or when state behavior is large (a giant method per state). An *enum with per-constant behavior* is a middle ground (closed set) — State classes win when states vary independently or must be added by extension.
- **A table-driven state machine (state × event → next state)**: excellent for *deterministic, small, well-known* machines (protocols) — the data is compact and testable. Rejected when each state's behavior is *rich* (not just a transition; real work per state), because a table can't hold behavior. State pattern holds *behavior* per state; a table holds only *transitions*.
- **Strategy pattern**: same shape, different intent — Strategy is *client-chosen and fixed*; State is *self-transitioning* (the object changes its own state on events). In Strategy the context keeps the strategy; in State the context *replaces* its state object on transitions. This is THE interview discriminator.
- **A single "fat" context with all state logic**: rejected — SRP and Open-Closed violations (adding a state edits the context).

**For Template Method:**
- **Copy-paste the process per variant**: rejected — duplicate the invariant steps everywhere (a change to the process requires editing every variant — the classic "shotgun surgery" bug source). Template Method centralizes the invariant.
- **Strategy instead**: Strategy varies the *whole algorithm* via composition; Template Method varies *steps* via inheritance. If the skeleton is fixed and only steps vary, Template Method is cleaner (no injection plumbing). If whole algorithms are interchangeable or runtime swap is needed, Strategy wins. The two are the canonical "inheritance vs composition for variation" pair.
- **Callback/hook parameters**: passing function hooks to a function is the functional analogue of Template Method (e.g., `Arrays.sort(a, comparator)`); chosen when the "skeleton" is a single function. Template Method shines when the skeleton is a *multi-step method* in a class with shared state.
- **Composition (a Strategy-like "Skeleton" object)**: valid alternative — the fixed skeleton in a strategy object calling abstract steps; usually over-engineered; inheritance-based Template Method is the idiomatic shape when the variants share the base's state.

## 5. Intuition
**State intuition**: a **person's mood / a stoplight**. A person *behaves differently depending on their mood* (happy/joked → laughs; angry → snaps). The "person" (context) doesn't have a giant `switch (mood)`; their current *mood object* (state) determines the response — and events *change the mood object* (self-transition). A stoplight is the same: the light *is* its state (green/amber/red), and "what happens next" is defined by the state itself (green → amber → red, each state knowing its successor).

**Template Method intuition**: a **restaurant recipe card / assembly line**. The process is fixed: "place base → add filling → top → bake". Each dish (subclass) overrides only "add filling" and "top" (the steps). The line (template method) never changes; the variants fill the blanks. The chef (base class) controls the sequence; the dish (subclass) provides the details — "don't call us, we'll call you" (Hollywood principle / inversion of control).

## 6. Real-World Analogy
- **State**: a **bank card's transaction status**. A card is PENDING-APPROVAL, APPROVED, BLOCKED. The *same* "charge" event behaves differently per status — approved → deduct; blocked → reject. And the status *itself* decides what a charge event does and which status comes next. A `switch`-based card would list every status and every action in one giant method; the State pattern keeps each status's behavior in its own "mode."
- **Template Method**: a **coffee shop's drink ritual**. The ritual is fixed: take cup → brew base → add extras → hand over. Only "brew base" (espresso vs tea) and "add extras" (sugar? milk?) vary. Every drink follows the same *template*; each drink type *overrides the steps*. The barista's training (the base class) defines the skeleton once.

## 7. Formal Definition
> **State**: Allow an object to alter its behavior **when its internal state changes**. The object will appear to change its class. (GoF, p. 305)
>
> **Template Method**: Define the **skeleton of an algorithm** in an operation, deferring some steps to subclasses. Template Method lets subclasses **redefine certain steps** of an algorithm without changing the algorithm's structure. (GoF, p. 325)
>
> Note: "appear to change its class" is why State is powerful — the context's *behavior* varies as if it were an instance of a different class, because behavior is delegated to the current state object.

## 8. Example
**State — a vending machine:**
```java
interface VendingState {
    void insertCoin(VendingMachine m);
    void pressButton(VendingMachine m);
}
class NoCoinState implements VendingState {
    public void insertCoin(VendingMachine m) { System.out.println("Coin accepted"); m.setState(new HasCoinState()); }
    public void pressButton(VendingMachine m) { System.out.println("Insert coin first"); }
}
class HasCoinState implements VendingState {
    public void insertCoin(VendingMachine m) { System.out.println("Coin already inserted"); }
    public void pressButton(VendingMachine m) { System.out.println("Dispensing item..."); m.setState(new NoCoinState()); }
}
class VendingMachine {
    private VendingState state = new NoCoinState();
    void setState(VendingState s) { this.state = s; }
    void insertCoin() { state.insertCoin(this); }
    void pressButton() { state.pressButton(this); }
}
// Usage
VendingMachine vm = new VendingMachine();
vm.insertCoin();    // Coin accepted
vm.pressButton();   // Dispensing item...
vm.pressButton();   // Insert coin first   ← behavior changed by state transition
```
- Adding a state ("maintenance") = one class; the machine never edits its own methods.

**Template Method — a data importer** (see Section 2 example) — the fixed open→read→close skeleton is defined once; CSV/JSON/XML parsers override only the read steps.

## 9. Internal Working
**State:**
1. The context holds a `State` reference (initialized to the start state).
2. An event method on the context (`insertCoin()`) delegates: `state.insertCoin(this)`.
3. **Dynamic dispatch** runs the current state's implementation.
4. The state performs its behavior *and* — critically — **transitions the context** by calling `context.setState(new SomeState())` (self-transition). The context *does not* decide transitions; the current state does.
5. Next event → new state's behavior → next transition. The object's behavior "changes class" as it moves through its lifecycle.
- **State data**: the context can pass itself (`this`) so states share context fields; transitions can carry the context. A context may hold state data separate from state *classes* (state objects are often stateless singletons per transition, shared across contexts).

**Template Method:**
1. Client calls the (often `final`) `templateMethod()` on a concrete subclass instance.
2. The base class executes the skeleton: calls concrete private/`final` steps + abstract steps + hooks in order.
3. **Dynamic dispatch** routes each abstract/hook call to the subclass's override.
4. The subclass never controls the *sequence* — only the *content* of the varied steps (Hollywood principle).
5. Hooks (optional overridable methods with a default no-op body) let subclasses participate optionally without being forced.

## 10. Time Complexity
- **State**: each event is O(1) — one delegation + optional transition (O(1) object swap). The transition graph's complexity is O(S) states total; behavior per state is constant. No asymptotic cost vs a switch (which is also O(1) dispatch) — the win is structural.
- **Template Method**: each call is O(1) dispatch per step; the skeleton executes O(steps) operations, each O(1) overhead over the step's own cost. The algorithm's Big-O is set by the steps (e.g., a sort template is O(n log n) regardless).
- Both add constant-factor indirection (vtable dispatch) — no algorithmic change.

## 11. Advantages
**State:**
- **Open-Closed**: adding a state = adding a class; the context never changes.
- **SRP**: each state's behavior is one focused class.
- **Self-transitions**: the state machine is self-describing (each state knows its next states) — readable and auditable.
- **Eliminates `switch (state)`** in the context (polymorphism replaces conditionals).
- **Encapsulated transitions**: transition *rules* live with the states, not scattered in the context.
- Testability: each state tested in isolation; the machine tested as a transition tour.
**Template Method:**
- **Eliminates duplication**: the invariant skeleton is written once; variants override only steps.
- **Inversion of control**: the base controls the process — enforcing *correct ordering* (you can't skip a step in a subclass).
- **Global change**: fixing a step in the skeleton fixes it for all variants at once.
- **Hooks**: optional participation without forcing overrides.
- **Consistency**: all variants follow the same process by construction.

## 12. Disadvantages
**State:**
- **Class explosion**: one class per state — many small classes for stateful objects.
- **Transition coupling**: states must know about each other (transition targets) — a dense state graph creates inter-state coupling.
- **Shared state across states**: the context must expose mutable state to its states — an encapsulation wrinkle.
- **Overhead for simple machines**: a 2-state flag doesn't need the pattern (YAGNI).
- **Not a true FSM**: lacks a single transition table; the graph is implicit (each state references successors) — harder to audit for very complex machines (consider a table-driven FSM instead).
**Template Method:**
- **Inheritance-bound**: steps are overridden via subclassing — no runtime variation (compile-time binding).
- **Base-class rigidity**: if a new variant needs a *different sequence*, the template is wrong for it (fragile base class problem).
- **Subclass/template coupling**: subclasses must conform to the base's steps and signatures — adding a step can ripple.
- **Fragile base class**: changes to the skeleton can break subclasses silently.

## 13. Interview Questions
1. **Q: What is the State pattern?** A: An object's behavior depends on its internal state, represented as state objects; the context delegates events to its current state, which *transitions* the context to the next state — a state machine built from polymorphic state classes.
2. **Q: What problem does State solve?** A: The `switch (state)` / `if-else` chains that violate Open-Closed (adding a state edits the switch) and SRP (one method knows all states); it also centralizes transition rules inside the states themselves.
3. **Q: What is the Template Method pattern?** A: Define an algorithm's skeleton in a base class, deferring some steps to subclasses — the base drives the sequence; subclasses override specific steps (abstract methods or hooks).
4. **Q: What problem does Template Method solve?** A: Duplication of a fixed process across variants (a change to the process edits every variant) and loss of the invariant sequence — the base class owns the order, so ordering can't be broken.
5. **Q: State vs Strategy — the big difference?** A: Strategy's object is *chosen by the client* and stays fixed; State's object is *changed by the context itself* as events fire (self-transition — the context replaces its state object). Strategy = client-driven selection; State = event-driven self-transition. In Strategy the context keeps the strategy; in State it swaps it.
6. **Q: What does "the object appears to change its class" mean?** A: Because behavior is delegated to the current state object, the context's observable behavior changes *as if* it were an instance of a different class as it transitions — the GoF's description of State's effect.
7. **Q: How does the vending-machine example demonstrate State? (Scenario)** A: `NoCoinState`/`HasCoinState` implement the same interface; `insertCoin`/`pressButton` on the machine delegate to the current state; `HasCoinState.pressButton` *transitions* the machine back to `NoCoinState`. The same `pressButton()` call behaves differently depending on the current state — polymorphism replaces the switch.
8. **Q: When would you choose a table-driven FSM over the State pattern? (Production)** A: When the machine is *transition-centric* (many states × events but little per-state *behavior*) — a table (state×event→next) is compact, auditable, and testable. State wins when each state has *rich behavior* (real work, not just transitions). Protocols (TCP) favor tables; business workflows (orders) favor State.
9. **Q: What is the Hollywood principle and how does it relate to Template Method?** A: "Don't call us, we'll call you" — the base class calls the subclass's overridden steps (inversion of control); subclasses provide content but never drive the sequence. Template Method is the canonical Hollywood-principle pattern (as are callbacks and DI containers).
10. **Q: Template Method vs Strategy?** A: Template Method varies *steps of a fixed skeleton* via *inheritance* (compile time); Strategy varies *the whole algorithm* via *composition* (run-time swap). Fixed structure + varying steps → Template Method; interchangeable whole algorithms or runtime swap → Strategy.
11. **Q: Where does the JDK/framework use Template Method? (Production)** A: `AbstractList` (implements most `List` ops on abstract `get`/`size`), `InputStreamReader`'s read loop, `javax.servlet.http.HttpServlet.service()` (dispatches to `doGet`/`doPost`/`doPut` — hooks), Spring `JdbcTemplate`/`RestTemplate` (`doExecute`/`doInConnection` template steps), `AbstractExecutorService` (`submit` → `execute`), `Thread.start()` calling overridable `run()`, and JUnit's lifecycle (setup/teardown hooks).
12. **Q: What's the difference between an abstract method and a hook in Template Method?** A: An abstract method *must* be implemented by every subclass (mandatory step). A hook is an overridable method with a default (usually empty) body — optional participation (subclasses override only if needed). Hooks reduce forced overrides.
13. **Q: How do you add a NEW state to an existing State machine? (Production)** A: Write a new state class implementing the interface, and update only the states that transition into/out of it. The context and all other states stay untouched — that's the Open-Closed payoff. (With a table-driven FSM you'd edit the table instead.)
14. **Q: How is State tested? (Production)** A: Unit-test each state class in isolation (with a mock/real context), then test *transition tours* — sequences of events that walk through every state and every transition (e.g., coin→button→coin), asserting behavior at each step. This "machine coverage" test is the State equivalent of path coverage.
15. **Q: Can states share context data? (Tricky)** A: Yes — the context passes itself to state methods (`state.handle(this)`), so states read/write context fields. This is the standard design but an encapsulation wrinkle: states become coupled to the context's public surface. Alternatively, pass only needed data (tighter, less natural for complex machines).
16. **Q: Are state objects thread-safe / shared? (Production)** A: Stateless states (no per-state fields; behavior from context data) can be singletons shared across contexts. States holding transition-target references but no mutable fields are also shareable. Per-context state instances are safer when states need identity or per-context data.
17. **Q: What's the risk of a Template Method with too many hooks?** A: "Template Method with 1000 hooks" — the base class becomes a God Class and subclasses become confusing spaghetti; also the fragile-base-class risk (adding a step/hook silently breaks or overrides behavior). Keep the skeleton small and hooks purposeful.
18. **Q: How do you prevent subclasses from breaking the skeleton's order?** A: Make the `templateMethod()` itself `final` (cannot be overridden) and the fixed steps `private`/`final`; only the *variable* steps are non-final/abstract. This enforces the sequence by construction — the key production discipline of the pattern.
19. **Q: State pattern for an order workflow — walk the lifecycle.** A: `OrderContext` holds `OrderState`; `PendingState` → on `pay()` → `PaidState`; `PaidState` → on `ship()` → `ShippedState`; `ShippedState` → on `deliver()` → `DeliveredState`; any state's `cancel()` → `CancelledState`/`RefundedState`. Each event delegates to the current state, which performs behavior and transitions. Adding "on-hold" = one new state class.
20. **Q: When is Template Method better than a callback/function hook?** A: When the skeleton is a *multi-step method* living in a class with shared mutable state (open/execute/map/close sharing a connection field), Template Method keeps that state in the base and the steps in subclasses. A function hook works for single-step skeletons (like `Arrays.sort(a, comparator)`). Multi-step + shared state → Template Method.

## 14. Follow-Up Questions
1. **Q: What is the "fragile base class" problem and how does Template Method worsen it?** A: Subclasses depend on the base's implementation details; a change to the base's skeleton or steps can silently change subclass behavior. Template Method concentrates behavior in the base, so the base must be stable — mitigate with `final` template methods, documented contracts, and small hooks.
2. **Q: How do State and Command interact?** A: A command can trigger a state transition (button press → invoker runs a command → the command calls `context.transition(...)`). Or states can *be* commands. They compose: Command reifies the event; State defines the machine's response.
3. **Q: What is a "self-transition" and why is it the State-vs-Strategy litmus?** A: A self-transition is the state object *replacing itself* on the context during event handling. Strategy never does this; State does it routinely. If your "state" never changes the context's object, it's actually a Strategy.
4. **Q: How do you represent states with data (e.g., a progress counter) in the State pattern?** A: Keep *state data* in the context (the counter field) and *state behavior* in state classes (stateless, shared). This is the standard split: context = data + current-state reference; states = behavior + transitions. Don't stash data in state objects unless states are per-context.
5. **Q: Template Method vs the "Strategy with a fixed pipeline"?** A: A Strategy holding a pipeline (a composite of steps) is the *compositional* analogue of Template Method. If steps must be swappable at run time or added by other modules, the strategy-pipeline wins; if the skeleton is fixed and the team owns all variants, Template Method's inheritance is simpler. This inheritance-vs-composition choice is exactly what interviewers probe.

## 15. Coding Example
```java
// State: a document lifecycle
interface DocState {
    void publish(Document ctx);
    void archive(Document ctx);
}
class DraftState implements DocState {
    public void publish(Document ctx) { System.out.println("Draft → Published"); ctx.setState(new PublishedState()); }
    public void archive(Document ctx) { System.out.println("Draft archived"); ctx.setState(new ArchivedState()); }
}
class PublishedState implements DocState {
    public void publish(Document ctx) { System.out.println("Already published"); }
    public void archive(Document ctx) { System.out.println("Published → Archived"); ctx.setState(new ArchivedState()); }
}
class ArchivedState implements DocState {
    public void publish(Document ctx) { System.out.println("Archived: cannot publish"); }
    public void archive(Document ctx) { System.out.println("Already archived"); }
}
class Document {
    private DocState state = new DraftState();
    void setState(DocState s) { this.state = s; }
    void publish() { state.publish(this); }
    void archive() { state.archive(this); }
}
public class Main {
    public static void main(String[] args) {
        Document d = new Document();
        d.publish();      // Draft → Published
        d.publish();      // Already published   ← behavior changed by state
        d.archive();      // Published → Archived
        d.publish();      // Archived: cannot publish
    }
}
```
```java
// Template Method: a batch job with mandatory + hook steps
abstract class BatchJob {
    // TEMPLATE METHOD — final so the sequence is fixed
    public final void run() {
        init();                    // concrete
        loadData();                // abstract (mandatory)
        process();                 // abstract (mandatory)
        if (isAuditEnabled()) {    // hook — optional behavior
            audit();
        }
        cleanup();                 // concrete
    }
    private void init() { System.out.println("init: open resources"); }
    private void cleanup() { System.out.println("cleanup: close resources"); }
    protected abstract void loadData();
    protected abstract void process();
    protected boolean isAuditEnabled() { return false; }   // hook (default no-op-ish)
    private void audit() { System.out.println("audit: log run"); }
}
class SalesReportJob extends BatchJob {
    protected void loadData() { System.out.println("load sales data"); }
    protected void process() { System.out.println("aggregate sales"); }
    @Override protected boolean isAuditEnabled() { return true; }   // override the hook
}
// run() order guaranteed: init → loadData → process → audit → cleanup
```
```python
# Python State
class State:
    def insert_coin(self, machine): raise NotImplementedError
    def press_button(self, machine): raise NotImplementedError

class NoCoin(State):
    def insert_coin(self, m): print("Coin accepted"); m.state = HasCoin()
    def press_button(self, m): print("Insert coin first")

class HasCoin(State):
    def insert_coin(self, m): print("Coin already inserted")
    def press_button(self, m): print("Dispensing..."); m.state = NoCoin()

class VendingMachine:
    def __init__(self): self.state = NoCoin()
    def insert_coin(self): self.state.insert_coin(self)
    def press_button(self): self.state.press_button(self)

m = VendingMachine(); m.insert_coin(); m.press_button(); m.press_button()
```
```cpp
// C++ State
#include <iostream>

class VendingMachine;                       // forward
struct VendingState {
    virtual ~VendingState() = default;
    virtual void insertCoin(VendingMachine& m) = 0;
    virtual void pressButton(VendingMachine& m) = 0;
};
class VendingMachine {
    VendingState* state_;
public:
    explicit VendingMachine(VendingState* s) : state_(s) {}
    void setState(VendingState* s) { state_ = s; }
    void insertCoin(); void pressButton();
};
// (implementations call state_->... with this)
```

## 16. Industry Usage
- **State**: order/delivery workflow engines (order lifecycle in every e-commerce backend), TCP/HTTP state machines, gRPC stream state machines, vending-machine/elevator simulations, game character FSM (idle/patrol/attack — Unity/Unreal state machines), UI wizards and multi-step forms, workflow libraries (Activiti, Camunda), Spring StateMachine (the framework literally implements the State pattern + FSM), `java.util.Scanner`? (no). **Spring StateMachine** and **Netty**'s connection state handling are production-grade examples.
- **Template Method**: `java.util.AbstractList`/`AbstractMap`/`AbstractCollection` (algorithm skeleton over abstract accessors), `java.util.concurrent.AbstractExecutorService`, `Thread.run()`, `javax.servlet.http.HttpServlet.service()` → `doGet`/`doPost`, Spring `JdbcTemplate`/`RestTemplate`/`TransactionTemplate`, `java.io.InputStreamReader` read loops, JUnit/TestNG lifecycle hooks (`@BeforeEach`/`@AfterEach` are hooks), JPA `EntityManager` lifecycle, game engines' game-loop template.
- **Interviews**: "design a vending machine / elevator / order workflow" → State; "explain how `JdbcTemplate` or servlets work" → Template Method; the State-vs-Strategy and Template-vs-Strategy discriminators are favorite traps.

## 17. References
- **Gamma et al., *Design Patterns* — "State" (p. 305), "Template Method" (p. 325)**: canonical definitions, participants, consequences.
- **Oracle Docs: `java.util.AbstractList`, `java.util.concurrent.AbstractExecutorService`, `java.lang.Thread.run()`, servlet `HttpServlet.service()`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Reference: `JdbcTemplate`, `RestTemplate`, `TransactionTemplate`; Spring StateMachine project** — https://docs.spring.io/spring-framework/reference/
- **Bruce Eckel / Head First Design Patterns — State chapter** — the vending machine / gumball machine worked example.
- **refactoring.guru — "State" and "Template Method"** — modern diagrams and Java/C++/Python examples.
- **David Harel, "Statecharts" (1987)** — the theory behind state machines (Harel statecharts), the foundation of Spring StateMachine's modeling.
- **Baeldung — "State Pattern in Java", "Template Method Pattern in Java"** — practical tutorials.

## 18. Cheat Sheet
- **State** = object's behavior depends on its state; states are classes; context delegates + the current state **self-transitions**.
- State replaces `switch(state)` with polymorphism; adding a state = adding a class (Open-Closed).
- **State vs Strategy**: Strategy = client-chosen, stays fixed; State = self-transitioning (context swaps its own state object on events).
- State vs table-driven FSM: State holds *behavior* per state; a table holds *transitions* — use State for rich behavior, a table for transition-centric machines.
- **Template Method** = fixed algorithm skeleton in a base class (often `final`), variable steps as abstract methods + hooks.
- Template Method eliminates process duplication and enforces ordering (inversion of control — Hollywood principle).
- **Template Method vs Strategy**: Template varies steps via inheritance (compile time); Strategy varies whole algorithms via composition (run time).
- Examples: State — order workflows, Spring StateMachine, game FSMs; Template — `AbstractList`, `HttpServlet.service()`, Spring `JdbcTemplate`.
- Make the template method `final` and fixed steps private to protect the sequence.
- Hooks = optional overridable steps with defaults; abstract methods = mandatory.

## 19. Quiz
1. State lets an object's behavior depend on: a) its type b) its internal state (via state objects) c) its package d) its name → **b**
2. In State, who decides the next state? a) the client b) the context c) the current state object (self-transition) d) a config → **c**
3. State vs Strategy: a) both self-transition b) strategy is client-chosen and fixed; state self-transitions c) state is client-chosen d) identical → **b**
4. The GoF phrase "the object appears to change its class" describes: a) Strategy b) State c) Template d) Observer → **b**
5. Template Method's skeleton is best declared: a) abstract b) final (fixed sequence) c) static d) private → **b**
6. A hook differs from an abstract method because a hook: a) is mandatory b) has a default body (optional override) c) is private d) is static → **b**
7. `javax.servlet.http.HttpServlet.service()` dispatching to `doGet`/`doPost` is: a) State b) Template Method c) Strategy d) Observer → **b**
8. `JdbcTemplate`'s `doInConnection` callback pattern is closest to: a) State b) Template Method (fixed skeleton + overridable steps) c) Singleton d) Memento → **b**
9. For a transition-centric machine with little per-state behavior, prefer: a) State pattern b) a table-driven FSM c) Strategy d) Observer → **b**
10. Template Method vs Strategy: a) template varies steps via inheritance; strategy varies whole algorithms via composition b) both inheritance c) both composition d) template is runtime → **a**

## 20. Flashcards
- **Q: State intent?** → **A:** An object's behavior depends on its state; states are classes; the context delegates and self-transitions on events.
- **Q: State vs Strategy?** → **A:** Strategy = client-chosen, fixed; State = event-driven self-transition (context swaps its own state).
- **Q: Table-driven FSM vs State?** → **A:** Table = transitions (compact); State = behavior per state (rich). Use State for rich per-state behavior.
- **Q: Template Method intent?** → **A:** Fix an algorithm skeleton in a base class; subclasses override specific steps (abstract methods + hooks).
- **Q: Why make the template method final?** → **A:** To protect the sequence — subclasses can't break the skeleton's ordering.
- **Q: Template vs Strategy?** → **A:** Template varies steps via inheritance (compile-time); Strategy varies whole algorithms via composition (runtime).
- **Q: Production Template examples?** → **A:** `AbstractList`, `HttpServlet.service()`, Spring `JdbcTemplate`, `Thread.run()`, JUnit lifecycle hooks.
- **Q: Hollywood principle?** → **A:** "Don't call us, we'll call you" — the base calls subclass steps (inversion of control).

## 21. Revision
**State** makes an object's behavior depend on its internal state, with each state a class implementing the same interface; the context *delegates* events to its current state, which performs behavior and **self-transitions** the context (`setState(next)`). It exists to replace `switch(state)` conditionals (Open-Closed/SRP violations) and to centralize transition rules inside states. Litmus vs **Strategy**: Strategy is client-chosen and stays fixed; State is event-driven and the context *swaps its own state*. Use a table-driven FSM instead when the machine is transition-centric with little per-state behavior. **Template Method** fixes an algorithm's skeleton in a base class (make it `final`; fixed steps private) and lets subclasses override *steps* via abstract methods and optional *hooks* — eliminating process duplication and enforcing order (Hollywood principle / inversion of control). Discriminate vs Strategy: Template varies steps via inheritance (compile time); Strategy varies whole algorithms via composition (runtime). Production: State → order workflows, Spring StateMachine, game FSMs; Template → `AbstractList`, `HttpServlet.service()`→`doGet/doPost`, Spring `JdbcTemplate`/`RestTemplate`, JUnit lifecycle hooks.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the State pattern?" | 2 How / 7 Formal Definition |
| "State vs Strategy?" | 13 Q5 / 14 Q3 / 18 Cheat Sheet |
| "Design a vending machine / order workflow (scenario)." | 13 Q7 / 13 Q19 / 15 Coding |
| "Table-driven FSM vs State?" | 13 Q8 / 14 Q5 |
| "What does 'appears to change its class' mean?" | 13 Q6 / 7 Formal Definition |
| "What is the Template Method pattern?" | 13 Q3 / 13 Q4 / 2 How |
| "Hollywood principle?" | 13 Q9 / 18 Cheat Sheet |
| "Abstract method vs hook?" | 13 Q12 / 14 Q1 |
| "Where do servlets/JdbcTemplate use it?" | 13 Q11 / 16 Industry Usage |
| "Template vs Strategy?" | 13 Q10 / 14 Q5 |
