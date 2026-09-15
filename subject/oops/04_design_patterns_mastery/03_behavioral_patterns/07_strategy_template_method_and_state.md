# Strategy, Template Method and State Patterns — 100 Interview Q&A

---

## Q1: What is the Strategy pattern and what problem does it solve?

**A:** The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It solves the problem of conditional logic that selects behavior at runtime. Without Strategy, you'd use long `if-else` or `switch` chains to select algorithms, violating the Open/Closed Principle — adding a new algorithm means modifying the existing conditional logic.

The pattern identifies a common interface (the Strategy interface) that all algorithm variants implement. The context holds a reference to a Strategy and delegates the algorithmic work to it. Clients can swap Strategies at runtime, changing the context's behavior without modifying the context itself.

The classic example is sorting: the sorting algorithm (quicksort, mergesort, heapsort) is a Strategy. The `Sorter` context holds a `SortStrategy` reference. Different clients can use different sorting algorithms without changing the `Sorter` class. This is superior to embedding algorithm selection logic inside `Sorter` because new algorithms can be added without modifying existing code.

---

## Q2: How does the Template Method pattern differ from Strategy?

**A:** Template Method defines the skeleton of an algorithm in a base class, letting subclasses override specific steps. Strategy encapsulates entire algorithms as interchangeable objects. The fundamental difference: Template Method uses inheritance to vary parts of an algorithm; Strategy uses composition to vary the entire algorithm.

Template Method controls the flow — the base class defines the order of operations and calls subclass hooks at specific points. The subclass cannot change the sequence, only the individual steps. Strategy gives full control to the encapsulated algorithm — the context doesn't know or care about the algorithm's internal structure.

Choose Template Method when you have a fixed algorithm structure with variation points, and you want to enforce that structure across all implementations. Choose Strategy when you have multiple complete, independent algorithms that should be swappable at runtime. Template Method is compile-time binding (subclass selection); Strategy is runtime binding (Strategy object selection).

---

## Q3: How does the State pattern relate to the Strategy pattern?

**A:** Both patterns use composition to delegate behavior, but their purposes differ. Strategy provides one of several interchangeable behaviors that a client selects explicitly. State allows an object to change its behavior automatically based on its internal state transitions.

In Strategy, the client decides which strategy to use: `context.setStrategy(new CompressionStrategy())`. The strategy doesn't change unless the client changes it. In State, the object itself transitions between states: a TCP connection transitions from `CLOSED` to `LISTEN` to `ESTABLISHED` based on network events, not client decisions.

The structural difference: Strategy is pluggable from outside; State transitions internally. Strategy objects are typically stateless (pure algorithms); State objects often contain state that determines transitions. A `Connection` object doesn't know it's in the `EstablishedState`; the state object handles the behavior and transitions to the next state when appropriate.

---

## Q4: When should you use Strategy over conditional logic?

**A:** Use Strategy when: **(1)** You have multiple variants of the same algorithm and want to switch between them at runtime. **(2)** The conditional logic is duplicated across multiple classes. **(3)** You want to add new algorithm variants without modifying existing code. **(4)** The algorithm selection logic is complex and deserves its own abstraction.

Keep conditional logic when: **(1)** There are only 2-3 simple variants with no duplication. **(2)** The variants differ in a single line or expression. **(3)** Adding a new variant is unlikely. **(4)** The overhead of creating a Strategy class hierarchy isn't justified.

A practical test: if your `if-else` or `switch` block contains more than trivial logic in each branch, or if the same selection logic appears in multiple places, Strategy is justified. If the entire branch is a single method call with no additional logic, a simple conditional is clearer and less abstract.

---

## Q5: What is the functional approach to the Strategy pattern?

**A:** In modern languages with first-class functions (lambdas, method references), Strategy objects can be replaced with function references. Instead of creating `interface Strategy { int execute(int a, int b); }` and separate classes for each algorithm, pass a lambda directly to the context: `context.setStrategy((a, b) -> a + b)`.

This eliminates the boilerplate of Strategy interfaces and implementation classes. The context accepts a function type (`Function<T,R>`, `BiFunction<T,U,R>`, or custom functional interfaces). Each lambda is an anonymous Strategy implementation. The behavior is the same — interchangeable algorithms — but the code is more concise.

The limitation is that lambda-based Strategies are stateless. If the strategy needs internal state (configuration, counters, caching), you still need a class. Lambdas work best for pure transformations: comparators, validators, transformers, filters. For strategies with state or multiple methods, named implementation classes remain clearer.

---

## Q6: How does the Template Method pattern use the Hook method technique?

**A:** Hooks are optional override points in a Template Method. Unlike abstract methods (which subclasses must implement), hooks have default implementations in the base class. Subclasses can override them to customize behavior but aren't required to. This provides extension points without mandatory implementation.

A typical pattern: `class DataMiner { void mine() { extract(); process(); analyze(); // optional hook report(); } void report() { /* default: do nothing */ } }`. Subclasses can override `report()` to add reporting behavior, or leave the default (no reporting) if they don't need it.

Hooks implement the Hollywood Principle ("Don't call us, we'll call you"). The base class calls hooks at predefined points; subclasses provide behavior only where they need it. This is more flexible than pure Template Methods with only abstract steps, because it allows subclasses to opt in to customization at specific points rather than being forced to implement every step.

---

## Q7: What are the advantages of the State pattern over switch-case state machines?

**A:** State pattern advantages: **(1) Encapsulation** — each state's behavior is in its own class, not scattered across a giant switch. **(2) Open/Closed** — adding a new state means creating a new class, not modifying the state machine. **(3) State-specific data** — each state class can hold state-specific fields that don't pollute the context. **(4) Testability** — each state can be tested independently.

Switch-case advantages: **(1) Simplicity** — for simple state machines (2-3 states, trivial transitions), a switch is easier to read. **(2) Centralized** — all states and transitions are visible in one place. **(3) No class explosion** — adding a state doesn't create a new file.

The decision threshold: if the state machine has more than 4-5 states, or if individual states have complex behavior (multiple methods, state-specific data), the State pattern is worth the additional class count. For simple toggle-like state machines, a switch or enum-based approach is clearer. The State pattern shines when states have distinct behavior, not just different transition rules.

---

## Q8: How does the Strategy pattern support the Open/Closed Principle?

**A:** OCP states that software entities should be open for extension but closed for modification. Strategy achieves this by defining algorithms behind an interface. Adding a new algorithm means creating a new class that implements the interface — no existing code changes. The context, the interface, and all existing strategies remain unmodified.

Compare this to a `sort()` method with a switch on algorithm type: adding quicksort means modifying the `sort()` method's switch statement. Strategy eliminates this modification. The `Sorter` class is written once and never changes, regardless of how many algorithms are added.

The trade-off is the additional complexity of the Strategy hierarchy. For a small, fixed set of algorithms that rarely changes, the overhead isn't justified. Strategy pays for itself when algorithms evolve independently, when new algorithms are added frequently, or when the selection logic is complex enough that centralizing it in a factory or configuration is valuable.

---

## Q9: What is the relationship between the State pattern and finite state machines?

**A:** The State pattern is an object-oriented implementation of a finite state machine (FSM). Each state is a class; transitions are method calls that change the context's current state; the context's behavior changes based on its current state object.

However, the State pattern doesn't explicitly model transitions. The transition logic is embedded in the state objects themselves — `StateA.process()` sets the context's state to `StateB`. This makes transitions implicit. An explicit FSM would separate states and transitions into distinct data structures (transition table), which is more formal and analyzable.

For complex state machines with many transitions, the implicit transitions of the State pattern become hard to follow. You can't look at one place and see all possible transitions from a given state. A formal FSM (table-driven or graph-based) provides better visibility. For simpler state machines where behavior varies significantly between states, the State pattern's encapsulation of state-specific behavior is more important than explicit transition visibility.

---

## Q10: How do you unit test classes that use the State pattern?

**A:** Test each state in isolation by mocking the context and verifying that the state's methods produce the correct behavior and transitions. Create the state object, inject a mock context, call the state's methods, and assert: **(1)** The behavior is correct for that state. **(2)** The context's state is changed correctly for transitions. **(3)** The context's methods are called as expected.

Test state transitions by verifying that calling a method on State A results in the context transitioning to State B, and that subsequent calls on the context (which now delegates to State B) produce B's behavior. This tests the full lifecycle: creation → state A behavior → transition → state B behavior.

Test illegal transitions separately: calling a method that shouldn't be valid in the current state should throw an exception or be handled gracefully. Don't test internal implementation details (e.g., which private method was called); test the externally observable behavior: what the state does and what transitions it makes.

---

## Q11: What is the difference between Strategy and Command patterns?

**A:** Both encapsulate behavior as objects, but their purposes differ. Strategy encapsulates an algorithm — a computation or transformation with inputs and outputs. Command encapsulates an action — an operation that may modify state, with undo/redo semantics.

Strategy is typically stateless: `compress(data)` produces output from input without side effects. Command is typically stateful: `DeleteCommand(file)` holds the file reference, knows how to delete it, and can undo the deletion by restoring the file.

Strategy objects are created and used immediately. Command objects may be stored in queues, executed later, logged, or reversed. Strategy answers "how do I compute this?" Command answers "what should I do?" and "how do I undo this?" The structural similarity (both delegate to an encapsulated object) makes confusion common, but the intent is distinct.

---

## Q12: How does the Template Method pattern relate to the Hollywood Principle?

**A:** The Hollywood Principle ("Don't call us, we'll call you") describes the inversion of control in Template Methods. The base class defines the algorithm skeleton and calls subclass methods at appropriate points. Subclasses don't call the base class's algorithm; the base class calls the subclass's hooks and steps.

This inversion is the defining characteristic. In normal OOP, high-level modules call low-level modules. In Template Method, the base class (high-level) controls the flow and calls the subclass (low-level) methods. The subclass doesn't know when its methods will be called or in what order — it only knows what it's responsible for implementing.

The principle ensures that the algorithm's structure is preserved across all subclasses. You can't accidentally skip a step or change the order — the base class controls execution. The subclass's responsibility is limited to filling in the blanks. This makes the base class the authority on the algorithm's structure, while subclasses are authorities on specific steps' implementations.

---

## Q13: What are the disadvantages of the Strategy pattern?

**A:** **(1) Client complexity** — clients must know about different strategies and select the right one, adding decision-making overhead. **(2) Class proliferation** — each algorithm variant requires a separate class, potentially creating many small classes. **(3) Communication overhead** — the context and strategy may need to share data through interfaces, which can be verbose compared to direct method calls within a monolithic class.

**(4) Over-engineering** — for simple algorithms with minimal variation, Strategy creates unnecessary abstraction. If there are only two variants and they rarely change, a conditional is simpler. **(5) Strategy selection can become complex** — if the selection logic itself is complex (dependent on multiple factors, requiring configuration), you've moved complexity from the algorithm to the selection, not reduced it overall.

The key mitigation is combining Strategy with Factory or Abstract Factory for strategy creation, and using dependency injection for strategy provision. This keeps the context simple (it receives a strategy, doesn't know which one) but adds infrastructure complexity. The pattern's value scales with the number and variability of algorithms.

---

## Q14: How does the State pattern handle complex state transitions?

**A:** For complex state machines, the State pattern can be enhanced with a transition table — a data structure mapping (current state, event) to (next state, action). Each state class consults the transition table when handling an event, rather than embedding transition logic in procedural code.

Another approach is a state machine framework (like Spring Statemachine) that formalizes transitions, guards (conditions that must be true for a transition), and actions (operations performed during transitions). This separates the state machine definition (declarative) from the state behavior (imperative), making the machine analyzable and modifiable without changing state classes.

Guard conditions add decision-making to transitions: transition from State A to State B only if condition X is true. Guards keep transition logic explicit and centralized. Without guards, transition conditions are buried in state class methods, making it hard to understand the overall machine behavior. For very complex state machines, the State pattern's implicit transitions become a liability, and a formal state machine library is preferable.

---

## Q15: What is the Role Object pattern and how does it relate to Strategy?

**A:** The Role Object pattern assigns multiple roles to a single object, with each role encapsulating behavior specific to that role. It's closely related to Strategy: each role is a Strategy that the object adopts for a specific context. A `Person` object might have `EmployeeStrategy`, `CustomerStrategy`, and `StudentStrategy` roles, each providing different behavior for the same operations.

The distinction is semantic: Strategy implies interchangeable algorithms for the same operation. Role Object implies the object plays multiple simultaneous roles with distinct behaviors. The `Person` isn't switching between roles; it has all roles simultaneously. This is closer to the State pattern in that the object has multiple behavioral aspects, but the roles coexist rather than replacing each other.

The Role Object pattern uses Strategy's structure (delegation to interchangeable objects) but applies it differently: the context holds multiple strategy references (one per role) and delegates to the appropriate one based on which role is active in the current interaction. This combines Strategy's algorithm selection with a multi-faceted object design.

---

## Q16: How does the Template Method pattern support code reuse?

**A:** Template Method extracts the common algorithm structure into a base class, reusing the control flow across all subclasses. The base class handles the invariant parts (error checking, logging, setup, teardown); subclasses implement only the variant parts (specific algorithmic steps).

This is the Template Method's primary value proposition. Without it, each subclass would duplicate the invariant code (setup, error handling, cleanup) or the algorithm's skeleton. With Template Method, the skeleton is written once in the base class. Subclasses inherit it automatically.

The danger is over-extraction: if the base class changes, all subclasses are affected. Changes to the algorithm's skeleton can break subclasses that relied on the previous flow. The Template Method should define only the truly invariant parts as fixed; everything that might vary should be a hook or abstract method. The more stable the skeleton, the safer the reuse.

---

## Q17: What is the Null Object pattern and how does it relate to Strategy?

**A:** Null Object provides a do-nothing implementation of an interface — a Strategy that performs no operation. Instead of checking for null references, the client uses the Null Object, which safely does nothing. This eliminates null checks scattered throughout client code.

Example: instead of `if (logger != null) logger.log("event")`, always call `logger.log("event")` and use `NullLogger` when logging is disabled. The Null Object implements the Logger interface with empty methods. This is a Strategy pattern where the Null Object strategy means "do nothing."

The Null Object is a special case of Strategy: it's the "no operation" variant. Its value is eliminating conditional logic (null checks) by providing a default strategy. This follows the Null Object pattern's formalization by Kevin Roberge: replace null with an object that has the same interface but benign behavior.

---

## Q18: How does the Strategy pattern enable testing?

**A:** Strategy makes algorithms independently testable. Each strategy is a self-contained class that can be unit-tested in isolation, without the context. The context is tested with mock strategies; strategies are tested with known inputs and expected outputs.

This separation also enables test doubles: replace production strategies with test strategies that return controlled results. Testing a data processor is easier when you can inject a `FakeCompressionStrategy` that returns predetermined compressed data instead of actually compressing. This isolates the data processor's logic from the compression algorithm's correctness.

Strategy also supports property-based testing: generate random instances of each strategy and verify properties that should hold for all algorithm variants. "All compression strategies should produce output smaller than or equal to the input." This cross-strategy property testing ensures that new strategies maintain the expected behavioral contract.

---

## Q19: What is the difference between State and Strategy in terms of intent?

**A:** Strategy's intent: select an algorithm from a family of algorithms at runtime. The context's behavior changes based on which strategy is active, but the selection is controlled externally (by the client, a factory, or configuration). The context doesn't change strategies on its own.

State's intent: an object changes its behavior in response to internal state transitions. The state changes are triggered by the object's own operations or external events processed by the current state. The context doesn't control which state is active — the states manage transitions between themselves.

The test: who decides when the behavior changes? If the client or configuration decides → Strategy. If the object itself decides based on events → State. A `Sorter` that uses different algorithms based on client choice is Strategy. A `TCPConnection` that transitions from `CLOSED` to `LISTEN` to `ESTABLISHED` based on network events is State.

---

## Q20: How does the Template Method pattern interact with the Factory Method pattern?

**A:** Template Methods often call Factory Methods to create objects needed by the algorithm. The base class defines the algorithm skeleton and calls `createProduct()` (a Factory Method) to get the object that the algorithm processes. Subclasses override `createProduct()` to provide different product types, while the algorithm's structure remains fixed.

This combination is one of the GoF's "classic" pattern pairings. The Template Method controls the process flow; the Factory Method controls object creation. Together, they provide variation at two points: what objects are created and how they're processed, while the overall process structure remains constant.

Example: `class ReportGenerator { final void generate() { Data data = fetchData(); Report report = createReport(data); format(report); } abstract Data fetchData(); abstract Report createReport(Data data); }`. The `generate()` Template Method calls two Factory Methods that subclasses override. Different subclasses produce different data and report types, but the generation process is identical.

---

## Q21: How does the Strategy pattern handle strategy selection?

**A:** Strategy selection can be handled by: **(1) Client choice** — the client explicitly sets the strategy (`context.setStrategy(new FastStrategy())`). Simple but pushes selection responsibility to the client. **(2) Parameterized selection** — the context accepts a parameter and selects the strategy internally (`new Context("fast")`). Simple but couples the context to strategy names.

**(3) Factory** — a Factory class or method creates the appropriate strategy based on configuration, environment, or runtime data. Decouples selection from both client and context. **(4) Dependency Injection** — the strategy is injected via constructor or setter, typically through a DI container that handles selection. Most flexible, best for testing and configuration.

**(5) Configuration-driven** — strategies are mapped to configuration keys, and the context loads the strategy from configuration at runtime. Allows strategy changes without code modifications. **(6) Context-driven** — the context selects the strategy based on its own state or environmental conditions. Useful when the strategy depends on runtime context (system load, time of day, available resources).

---

## Q22: What is the relationship between the State pattern and the Interpreter pattern?

**A:** Both use objects to represent different "modes" of behavior, but the Interpreter pattern defines a grammar and interprets sentences in that grammar. Each non-terminal in the grammar is a class; interpretation means evaluating the class's expression. This is structurally similar to State (different classes with different behavior), but the intent is different: Interpreter processes structured input; State manages behavioral transitions.

The connection is that both patterns represent behavior as a graph of objects. An interpreter's abstract syntax tree is a static structure; a state machine's state graph is a dynamic structure. You could implement an interpreter using the State pattern (each grammar rule is a state), but the Interpreter pattern's purpose (parsing and evaluating) is distinct from State's purpose (managing object behavior based on state).

In practice, if you're building a parser or expression evaluator, the Interpreter pattern is more appropriate. If you're managing an object's behavior based on its lifecycle or conditions, State is more appropriate. The structural similarity can cause confusion, but the intent — parsing vs. state management — is the deciding factor.

---

## Q23: How does the Strategy pattern support the Single Responsibility Principle?

**A:** SRP states that a class should have only one reason to change. Without Strategy, a class that selects and executes algorithms has two reasons to change: algorithm selection logic AND algorithm implementation. Strategy separates these concerns: the context handles only delegation; each strategy handles only its algorithm.

The context class is responsible for coordinating strategy usage, not for implementing algorithms. Each strategy class is responsible for its algorithm, not for how it's selected or used. This clean separation means changes to algorithm implementation don't affect selection logic, and changes to selection logic don't affect algorithm implementation.

However, Strategy doesn't automatically satisfy SRP. If the strategy selection logic itself becomes complex (dependent on multiple conditions, requiring configuration parsing), it deserves its own class (Factory, Strategy Selector). The principle is violated when the context class both selects and uses strategies — it has two responsibilities.

---

## Q24: What is the difference between Strategy and Bridge patterns?

**A:** Strategy and Bridge have identical UML structure (abstraction + implementation hierarchies connected by delegation), but different intents. Strategy is about selecting algorithms at runtime — the implementation (strategy) is interchangeable and typically stateless. Bridge is about decoupling an abstraction from its implementation so they can vary independently — typically permanent, not switchable at runtime.

Strategy implies: "I have several algorithms, and I'll choose one." Bridge implies: "I have an abstraction and an implementation that should vary independently." The Bridge pattern is structural (organizing classes); the Strategy pattern is behavioral (organizing behavior).

Example: `Window` (abstraction) × `WindowImpl` (implementation for Unix/Windows) is Bridge — the window type and implementation are independently chosen at construction. `Sorter` (context) × `SortStrategy` (algorithm) is Strategy — the algorithm is swappable at runtime. The Bridge's implementation is typically set once; the Strategy is changeable throughout the context's lifetime.

---

## Q25: How does the State pattern handle parallel state machines?

**A:** An object can have multiple independent state machines running simultaneously, each represented by a separate state field. A `Connection` might have a `ConnectionState` (CLOSED, OPEN, ESTABLISHED) and an `AuthenticationState` (UNAUTHENTICATED, AUTHENTICATING, AUTHENTICATED), each evolving independently.

Each state machine is implemented as a separate State pattern instance. The context holds references to both: `private ConnectionState connectionState; private AuthState authState;`. Each state handles its own transitions. The context delegates to the appropriate state for each operation: `authenticate()` delegates to `authState`; `send()` checks both states (must be ESTABLISHED and AUTHENTICATED).

The challenge is handling interactions between state machines: "Sending data is only valid when connection is ESTABLISHED AND authentication is AUTHENTICATED." This cross-machine logic can be handled by guards (conditions checked before transitions) or by having one state machine's transitions depend on the other's current state. The key is keeping the machines' definitions separate while handling their interactions explicitly.

---

## Q26: What is the benefit of combining Strategy and Decorator patterns?

**A:** Combining Strategy and Decorator enables composable, stackable strategies. Instead of choosing one algorithm from a set, you compose multiple strategies into a pipeline. Each Decorator wraps a Strategy, adding behavior: `new LoggingStrategy(new CachingStrategy(new CompressionStrategy()))`.

This is more flexible than pure Strategy: Strategy selects one algorithm; Decorator-Strategy chains multiple algorithms. The outermost Decorator handles logging, the next handles caching, and the innermost handles compression. Each concern is encapsulated in its own Decorator, and the composition order determines the behavior.

This combination is common in I/O (BufferedInputStream wrapping FileInputStream wrapping SocketInputStream) and data processing (validation → transformation → compression → encryption). The Strategy aspect means each layer is interchangeable; the Decorator aspect means layers stack. This provides both horizontal variation (different algorithms at each layer) and vertical composition (different numbers and orders of layers).

---

## Q27: How does the Template Method pattern handle error handling?

**A:** The base class Template Method should handle errors at the algorithm skeleton level: try-catch blocks around the entire algorithm, or around individual steps, depending on the error handling strategy. The Template Method defines the error handling policy; subclasses don't need to implement it.

A common pattern: the Template Method wraps each step in a try-catch, logs the error, and calls a hook method `handleError(Exception e)` that subclasses can override. This provides default error handling (log and continue) with optional customization (retry, notify, rollback).

Without centralized error handling in the Template Method, each subclass would need to implement its own error handling, leading to duplication and inconsistency. The Template Method ensures that all subclasses handle errors uniformly. The base class can also define cleanup in a `finally` block or use the "execute around" idiom, ensuring resources are released regardless of whether the algorithm succeeds.

---

## Q28: What is the State pattern's equivalent of the Strategy pattern's context?

**A:** In the State pattern, the context is the object whose behavior changes. Unlike Strategy's context (which holds a strategy reference and delegates), State's context actively participates in state transitions. The context holds the current state reference, delegates behavior to it, and provides a `setState()` method that state objects call to transition.

The key difference: Strategy's context is passive (it uses a strategy). State's context is semi-active (it provides infrastructure for state transitions). The context in State provides: the public interface that clients call, the state reference, the `setState()` method, and often shared methods that states can call.

The context also defines the state interface (or an abstract state class), ensuring that all states implement the same methods. States access the context through a reference passed during construction or through the state interface. This bidirectional relationship (context delegates to state, state modifies context) is unique to the State pattern; Strategy is one-directional (context delegates to strategy, strategy doesn't modify context).

---

## Q29: When does the Strategy pattern become an anti-pattern?

**A:** Strategy becomes an anti-pattern when: **(1) Over-abstraction** — creating Strategy hierarchies for algorithms with only one or two variants that never change. The class hierarchy overhead outweighs the flexibility benefit. **(2) Strategy proliferation** — creating so many strategy classes that the codebase becomes fragmented and hard to navigate. **(3) Premature optimization** — implementing Strategy for algorithms that are never swapped, purely for theoretical flexibility.

**(4) Hidden complexity** — when the strategy selection logic is more complex than the algorithms themselves, you've moved complexity rather than reduced it. **(5) Violation of encapsulation** — when strategies need access to context internals, the clean interface between context and strategy breaks down, creating tight coupling despite the abstraction.

The indicator: if the Strategy pattern adds more code, more classes, and more indirection without a clear, demonstrated need for algorithm interchangeability, it's over-engineered. Start with the simplest approach (conditional logic, single implementation) and refactor to Strategy when the need for interchangeability materializes.

---

## Q30: How does the State pattern support the Single Responsibility Principle?

**A:** Without the State pattern, a class handling multiple states contains all state-specific behavior in one class. That class has multiple reasons to change: one for each state's behavior. This violates SRP. The State pattern distributes state-specific behavior into separate state classes, each with a single responsibility: the behavior of one state.

`OrderState` handles only order-related state behavior. `PaymentState` handles only payment-related state behavior. `ShippingState` handles only shipping-related state behavior. Each class changes for only one reason: changes to that specific state's behavior.

The context class's responsibility is reduced to: holding the current state, delegating to it, and providing the `setState()` mechanism. This is a single responsibility: managing state transitions. The context doesn't contain state-specific logic, so it doesn't change when individual states change.

---

## Q31: How does the Template Method pattern relate to the Dependency Inversion Principle?

**A:** DIP says high-level modules should not depend on low-level modules; both should depend on abstractions. Template Method typically violates DIP: the base class (high-level) depends on subclasses (low-level) through abstract methods. The base class knows about subclass existence and calls their methods.

However, the violation is intentional and localized. The base class depends on an abstraction it defines (the abstract methods / hook methods). Subclasses implement this abstraction. The dependency flows from base to subclass (through the template), not from subclass to base. This is "stable abstraction" — the base class defines a stable interface; subclasses implement it.

To satisfy DIP more strictly, you can combine Template Method with Strategy: the Template Method calls Strategy objects instead of subclass methods. The base class depends on Strategy interfaces (abstractions); concrete strategies implement them. This eliminates the inheritance dependency while preserving the algorithm skeleton. The trade-off is added indirection.

---

## Q32: What is the difference between Strategy and the Parameter Object pattern?

**A:** Strategy encapsulates an algorithm as an object; Parameter Object bundles multiple parameters into a single object. They're complementary patterns: Strategy encapsulates behavior; Parameter Object encapsulates data. A Strategy often receives a Parameter Object as input: `compress(DataBlock block)`.

Strategy is about what to do; Parameter Object is about what to do it with. You might use Parameter Object to clean up method signatures that would otherwise have many parameters, and Strategy to make the processing algorithm interchangeable. Together, they reduce method signature complexity and algorithm coupling.

The distinction matters for classification: if the object primarily contains data and minimal behavior, it's a Parameter Object. If it primarily contains algorithm logic and is interchangeable with similar objects, it's a Strategy. The same class could serve both roles in different contexts, but the intent (data bundling vs. algorithm encapsulation) determines the classification.

---

## Q33: How does the State pattern handle invalid transitions?

**A:** When an event arrives that shouldn't be handled in the current state, the State pattern should either: **(1) Ignore it** — the state simply doesn't handle the event, and nothing happens. This is valid when the event is irrelevant in the current state (e.g., `start()` event when already running). **(2) Throw an exception** — if the event should never occur in this state, throw `IllegalStateException` to indicate a programming error.

**(3) Log a warning** — for recoverable situations where the event is unexpected but not catastrophic. **(4) Force a transition** — some state machines define "forced" transitions for unexpected events, moving to a safe state (error state, default state).

The best approach depends on the domain: in safety-critical systems, invalid transitions should throw exceptions to catch programming errors early. In user-facing systems, ignoring invalid events (button clicks when action is in progress) provides better UX. The State pattern makes the handling explicit: each state class decides what to do with each event, including the option to do nothing.

---

## Q34: What is the relationship between Strategy and the Factory Method pattern?

**A:** Strategy and Factory Method are complementary: Strategy defines interchangeable algorithms; Factory Method creates the appropriate algorithm instance. The Factory decides which Strategy to create based on configuration, environment, or input; the Strategy encapsulates the algorithm's behavior.

Common combination: a Factory creates a Strategy based on a configuration string or enum. `StrategyFactory.create("fast")` returns a `FastStrategy`. The Factory handles selection logic; the Strategy handles algorithm logic. This separates concerns cleanly: the Factory knows about all strategies (creation concern); the Strategy knows about its algorithm (behavior concern); the Context knows about the Strategy interface (delegation concern).

Without Factory, clients must create strategies directly, coupling them to concrete strategy classes. With Factory, clients request a strategy by name or type, and the Factory creates it. This is particularly valuable when strategies have complex construction logic (dependencies on configuration, resources, or other objects) that shouldn't be duplicated across client code.

---

## Q35: How does the Strategy pattern handle strategy lifecycle?

**A:** Strategy lifecycle concerns: **(1) Creation** — who creates the strategy? Client, factory, or DI container? **(2) Sharing** — is the strategy shared between multiple contexts (stateless strategies can be singletons) or per-context (stateful strategies need separate instances)? **(3) Disposal** — does the strategy hold resources that need cleanup?

Stateless strategies (pure functions, comparators) can be shared and reused. Java's `Comparator.comparing()` returns shared, immutable strategy instances. Stateful strategies (with counters, caches, or configuration) should not be shared, as concurrent access would cause data races.

The safest default is per-context strategy instances: each context gets its own strategy instance, avoiding sharing issues. For performance-critical paths, shared immutable strategies reduce allocation overhead. The lifecycle decision depends on the strategy's state: immutable and stateless → shareable; mutable or stateful → per-context. DI frameworks handle lifecycle management automatically when strategies are registered as beans.

---

## Q36: What is the benefit of using enums to implement the State pattern?

**A:** Enums in Java can implement interfaces and hold behavior, making them suitable for simple state machines. Each enum constant is a state that implements the state interface's methods. Transitions are handled by calling `context.setState(NextState.INSTANCE)` from within the enum's method.

Benefits: **(1) Type safety** — the compiler ensures only valid states exist; you can't create an undefined state. **(2) Simplicity** — no class explosion for simple states; each state is an enum constant. **(3) Exhaustiveness** — `switch` on enum states forces handling of all states (with `default` or without). **(4) Serialization** — enums serialize/deserialize automatically.

Limitations: **(1) No state-specific data** — enum constants can hold fields, but they're shared across all uses, not per-instance. **(2) Limited hierarchy** — enums can't extend classes (they implicitly extend `Enum`). **(3) State transitions are static** — enum states are singletons; they can't hold per-context state. Use enum-based State for simple, stateless state machines; use class-based State for complex, stateful ones.

---

## Q37: How does the Template Method pattern support polymorphism?

**A:** Template Methods use polymorphism through the Template Method itself: the base class method is final (can't be overridden), but it calls abstract/hook methods that subclasses override polymorphically. When you call `base.templateMethod()`, the correct subclass's implementation of each step is called based on the actual runtime type.

This provides polymorphic behavior within a fixed algorithm skeleton. The skeleton is non-polymorphic (final); the steps are polymorphic (overridable). This is different from pure polymorphism where the entire method is overridden — Template Method provides controlled polymorphism where only designated parts vary.

The Template Method is a constrained form of polymorphism: you can vary the parts but not the whole. This is useful when you want to enforce an algorithm's structure while allowing variation in specific steps. The alternative (pure polymorphism, where each subclass implements the entire algorithm) risks inconsistent implementations where subclasses handle error checking, logging, or cleanup differently.

---

## Q38: What is the difference between State and Visitor patterns?

**A:** Both dispatch based on type, but the dispatch direction differs. Visitor dispatches based on the element's type: `visit(Line l)`, `visit(Circle c)`. Adding a new element type requires modifying the Visitor interface. State dispatches based on the state's type: `handleEvent()` behaves differently in each state. Adding a new state requires creating a new state class, not modifying existing interfaces.

Visitor adds new operations to existing element classes without modifying them. State adds new states to an existing state machine without modifying the context. Visitor is about extending operations; State is about extending states. Visitor requires modifying the element hierarchy (accept method); State requires modifying the context (setState).

The practical difference: Visitor is best when you have a stable set of types (elements) and need to add new operations. State is best when you have a stable operation set (events) and need to add new states. Visitor's double dispatch (accept → visit) gives compile-time type safety; State's dynamic dispatch gives runtime behavioral flexibility.

---

## Q39: How does the Strategy pattern interact with caching?

**A:** Strategy and caching combine in several ways: **(1) Cached Strategy** — cache the strategy's results based on input. A Decorator wraps the strategy with a cache, returning cached results for repeated inputs. **(2) Strategy Cache** — cache strategy instances themselves. If strategy creation is expensive (loading configuration, connecting to services), cache the created instances for reuse.

**(3) Strategy-aware Cache** — the strategy itself manages caching internally. A `CachingSortStrategy` caches its sorting results, while a `FreshSortStrategy` always recomputes. The client chooses between cached and non-cached variants.

The Cached Strategy Decorator is the most common combination: `new CachedStrategy(new ExpensiveStrategy())`. The decorator checks a cache before calling the strategy; on a miss, it calls the strategy and caches the result. This separates caching concerns from algorithm concerns, following SRP. The caching decorator can be applied to any strategy without modifying the strategy's code.

---

## Q40: What are the real-world applications of the Template Method pattern?

**A:** **(1) Framework hooks** — application frameworks define lifecycle methods (`init()`, `execute()`, `cleanup()`) that applications override. Servlet `HttpServlet` is a Template Method: `service()` calls `doGet()`, `doPost()`, etc. **(2) Test frameworks** — JUnit's `@Before`, `@Test`, `@After` is a Template Method: the framework runs setup → test → teardown.

**(3) Data processing pipelines** — ETL (Extract, Transform, Load) processes define a fixed pipeline with variable steps. **(4) Code generation** — base generator defines the generation template; subclasses override language-specific generation steps. **(5) Protocol handlers** — the protocol flow (connect → authenticate → transfer → disconnect) is fixed; the implementation of each step varies.

The common thread: a fixed process with variable steps, where enforcing the process structure is as important as the steps' implementations. If the process can be rearranged or skipped, Strategy is more appropriate. If the process must be followed exactly, Template Method enforces it.

---

## Q41: How does the State pattern handle concurrent events?

**A:** Concurrent events in state machines require careful handling to avoid race conditions. The basic State pattern assumes sequential event processing. For concurrent events, the state object and its state reference must be thread-safe: use `synchronized` blocks, `ReentrantLock`, or `AtomicReference` for the state field.

The simplest approach is a **synchronized state machine**: all event handling methods are synchronized, ensuring only one event is processed at a time. This is correct but limits throughput. For high-throughput scenarios, consider **event queues**: events are enqueued and processed sequentially by a single thread, avoiding concurrent modification while maintaining high throughput.

For truly concurrent state machines (multiple independent state machines operating in parallel), each machine is a separate object with its own state field. The machines communicate through events or shared data structures. The context doesn't need to manage multiple state machines — each is independent. The complexity lies in coordinating the machines' events, not in the state pattern itself.

---

## Q42: What is the relationship between Strategy and the Specification pattern?

**A:** Specification defines business rules as composable objects. A Specification is a Strategy for validation or filtering: `isEligible(Applicant applicant)` returns true or false. Different specifications encapsulate different rules: `AgeSpecification(min=18)`, `CreditScoreSpecification(min=700)`.

The Specification pattern uses Strategy's structure (interchangeable objects with a common interface) but applies it to business rules rather than algorithms. Specifications are composable: `AND`, `OR`, `NOT` operations combine specifications into complex rules. This is like composing Strategies, but the focus is on rule composition rather than algorithm selection.

The key difference: Strategy algorithms produce output (transform data). Specifications evaluate conditions (return boolean). A Strategy might be `SortAlgorithm`; a Specification might be `EligibilityRule`. Both are interchangeable objects, but their output types and purposes differ.

---

## Q43: How does the Template Method pattern support the Liskov Substitution Principle?

**A:** LSP requires that subclasses be substitutable for the base class without breaking client expectations. Template Method supports LSP by defining the algorithm skeleton in the base class: all subclasses follow the same process flow, so clients can substitute any subclass without noticing behavioral differences in the overall process.

However, LSP can be violated if a subclass's step implementation changes the algorithm's semantics. If the base class expects `validate()` to throw `ValidationException` on invalid input, but a subclass's `validate()` silently ignores invalid input, clients expecting the exception will behave incorrectly. The subclass substituted for the base class breaks the contract.

To maintain LSP: the base class should document the behavioral contract for each step (preconditions, postconditions, side effects). Subclasses must honor these contracts. The Template Method's fixed skeleton helps enforce LSP because the overall flow is guaranteed — the risk is in step implementations that violate the expected behavior of individual steps.

---

## Q44: How does the Strategy pattern support the Interface Segregation Principle?

**A:** ISP states that clients shouldn't depend on methods they don't use. Strategy interfaces should be narrow: clients depend only on the methods they call. A `SortStrategy` interface should have `sort(List<T>)` — not `sort(List<T>, Comparator<T>, int maxMemory)` if the client never uses the comparator or memory parameters.

Narrow Strategy interfaces mean clients have minimal dependencies. If different clients need different methods from a strategy, split the interface into multiple smaller interfaces and have the strategy implement all of them. Clients depend only on the interface they need.

This is particularly important when strategies are injected into contexts: the context's dependency on the Strategy interface should be minimal. If the context only needs `execute(Input): Output`, the Strategy interface should define only that method. Clients of the context are unaffected by the Strategy interface's width, but the context's testability and flexibility are improved with narrow interfaces.

---

## Q45: What is the difference between Strategy and the Parameter Object pattern for handling multiple parameters?

**A:** Strategy encapsulates behavior (algorithms); Parameter Object encapsulates data (multiple parameters bundled into one object). When a method has too many parameters, create a Parameter Object. When you need to swap algorithms, create a Strategy. They solve different problems but can be combined.

Example: `process(Order order, User user, Date date, boolean expedited)` has too many parameters. Create `ProcessingRequest(order, user, date, expedited)` as a Parameter Object. If the processing algorithm varies, create `ProcessingStrategy` that receives `ProcessingRequest`: `strategy.execute(request)`.

The combination reduces both parameter count (Parameter Object) and algorithm coupling (Strategy). The Parameter Object simplifies method signatures; the Strategy makes algorithms interchangeable. Without Parameter Object, the Strategy interface would have many parameters; without Strategy, the processing class would contain all algorithm variants in one place.

---

## Q46: How does the State pattern handle hierarchical states?

**A:** Hierarchical states organize states into a tree: a superstate contains substates. When an event arrives, the current state handles it. If it can't, the event propagates to the parent superstate. This reduces duplication — shared behavior lives in the superstate; specific behavior lives in substates.

Implementation: each state holds a reference to its parent superstate. When handling an event, the state first tries to handle it. If it can't (no handler defined), it delegates to its parent: `if (parent != null) parent.handleEvent(context, event)`. This is like the Chain of Responsibility pattern applied to state handling.

Use hierarchical states when: **(1)** Multiple states share common behavior (superstate provides it). **(2)** The state machine has naturally nested states (e.g., `ConnectedState` contains `IdleState`, `TransmittingState`). **(3)** The state machine is complex and flat organization creates excessive duplication. Hierarchical states reduce the number of transitions by handling common events at the superstate level.

---

## Q47: What is the relationship between Strategy and the Chain of Responsibility pattern?

**A:** Chain of Responsibility passes a request along a chain of handlers, each deciding whether to handle it or pass it on. Strategy selects one handler from a set and delegates to it. The structural similarity is delegation, but the behavioral difference is selection vs. chaining.

In Strategy, exactly one algorithm executes. In Chain of Responsibility, multiple handlers might process the request, or the request might reach the end of the chain without being handled. Strategy is a "one of many" selection; Chain is a "try each until handled" progression.

They can be combined: a Strategy pattern where the strategies form a chain. The first strategy that can handle the request does so; others are skipped. This is useful for cascading fallback strategies: try cache (Strategy 1), then database (Strategy 2), then external API (Strategy 3), in order of preference.

---

## Q48: How does the Template Method pattern support the Liskov Substitution Principle in framework design?

**A:** Framework designers use Template Method to define extension points while maintaining LSP. The base class provides a `final` Template Method that guarantees the algorithm's structure. Subclasses implement abstract methods and hooks, but the overall behavior (the algorithm's observable contract) remains consistent across all subclasses.

The framework can enforce LSP through: **(1) Final template methods** — the algorithm skeleton can't be overridden, ensuring consistent flow. **(2) Preconditions in hooks** — the base class checks preconditions before calling subclass methods, ensuring the subclass receives valid input. **(3) Postconditions in the template** — the base class validates the result after the subclass's step, ensuring the step didn't violate the contract.

This gives framework users confidence that any subclass they write (or that third parties write) will behave correctly within the framework's context. The Template Method constrains what can vary (steps) and what can't (flow), maintaining LSP while allowing extension.

---

## Q49: What is the benefit of using Strategy with dependency injection?

**A:** DI containers manage strategy lifecycle and selection: the strategy is registered as a bean, and the context receives it through constructor or setter injection. The context doesn't know which strategy it receives — the DI container handles creation and wiring based on configuration.

Benefits: **(1) Testability** — inject mock strategies in tests, production strategies in production. No conditional logic needed. **(2) Configuration** — strategy selection is externalized (properties files, environment variables), not hardcoded. **(3) Decoupling** — the context has zero knowledge of strategy implementations; it depends only on the interface.

Spring's `@Qualifier` and `@Conditional` annotations enable strategy selection based on configuration: `@Qualifier("fast")` selects the fast strategy; `@ConditionalOnProperty(name="cache.enabled")` conditionally registers the caching strategy. This makes strategy selection declarative (configuration-driven) rather than imperative (code-driven), aligning with IoC principles.

---

## Q50: How does the State pattern differ from a simple flag variable?

**A:** A flag variable (`boolean isRunning`) is the simplest form of state management. The State pattern is the full object-oriented approach. For 2-3 states with trivial behavior differences, a flag is simpler and clearer. For many states with complex behavior, the State pattern is more maintainable.

The threshold: if the "if-else" for the flag has more than a few lines in each branch, or if the state behavior involves multiple methods that all need to check the flag, the State pattern is warranted. With flags, every method that depends on state has a conditional: `if (running) { ... } else { ... }`. The State pattern eliminates these conditionals by delegating to state objects.

Example: a media player with `PLAYING`, `PAUSED`, `STOPPED` states. If each state only changes the behavior of `play()`, `pause()`, and `stop()`, flags work. If each state also changes the behavior of `seek()`, `getProgress()`, `getDisplayInfo()`, and `handleKeyPress()`, flags create a matrix of conditionals. The State pattern eliminates this by encapsulating all behavior for each state in its own class.

---

## Q51: What is the relationship between the Strategy pattern and the Decorator pattern?

**A:** Both add behavior to objects, but Strategy replaces behavior; Decorator adds behavior. Strategy swaps the entire algorithm: the context uses Strategy A, then switches to Strategy B — A is completely replaced. Decorator wraps the existing object, adding behavior before/after the original behavior — the original is still there.

Combining them: Decorator can wrap a Strategy to add cross-cutting concerns (logging, caching, timing) to any strategy without modifying the strategy itself. `new LoggingStrategy(new FastStrategy())` adds logging to the fast strategy. The decorator pattern is orthogonal to Strategy — it can be applied to any Strategy implementation.

In practice, this combination is powerful: Strategy handles algorithm selection; Decorator handles algorithm enhancement. The Strategy pattern manages horizontal variation (which algorithm); the Decorator pattern manages vertical variation (what additional behavior). Together, they provide maximum flexibility with minimum coupling.

---

## Q52: How does the Template Method pattern handle optional steps?

**A:** Optional steps are implemented as hook methods with default (usually empty) implementations in the base class. Subclasses override hooks only when they need the optional behavior. The Template Method calls the hook, and if the subclass didn't override it, nothing happens (the default empty implementation executes).

Example: `class ReportGenerator { final void generate() { extractData(); process(); if (includeSummary()) addSummary(); format(); } boolean includeSummary() { return true; // default } void addSummary() { } // default: no-op }`. Subclasses can override `includeSummary()` to return false (skip summary) or override `addSummary()` to customize the summary.

This is cleaner than conditional logic because: **(1)** The decision (include/exclude) is separate from the implementation (how to generate the summary). **(2)** Subclasses don't need to implement unused steps. **(3** The default behavior is documented in the base class. The trade-off is that the base class must anticipate all optional steps, which can lead to many hook methods.

---

## Q53: What is the State pattern's approach to state documentation?

**A:** State machines can be documented as state diagrams (UML statecharts) showing states, events, transitions, and guards. Each state is a node; each transition is a labeled edge. Guards and actions are annotations on the edges. This visual representation makes the state machine's behavior clear at a glance.

For the State pattern implementation, map the state diagram to classes: each state becomes a class, each transition becomes a method call that changes the context's state. Guards become conditions in the state's event handler. Actions become method calls during transitions.

Documentation should include: **(1)** The state diagram (visual). **(2)** A transition table (tabular: state × event → next state + action + guard). **(3)** Each state class's responsibilities (what events it handles, what transitions it makes). This triple documentation ensures the implementation matches the design and is understandable by new team members.

---

## Q54: How does the Strategy pattern handle strategy fallback?

**A:** Fallback strategies are handled by chaining or decorating strategies. When the primary strategy fails, the fallback strategy is tried. This can be implemented as a **Fallback Strategy** that wraps the primary strategy: it tries the primary, catches exceptions, and delegates to the fallback.

Alternatively, the **Chain of Responsibility** approach: multiple strategies are tried in order until one succeeds. The chain stops at the first successful result. This is like Strategy but with multiple strategies attempted rather than one selected.

The **Circuit Breaker** pattern adds another dimension: after repeated failures, the primary strategy is temporarily disabled, and all requests go directly to the fallback. After a cooldown period, the primary is re-enabled for a test request. This prevents hammering a failing service and provides automatic recovery detection.

---

## Q55: What is the relationship between the State pattern and the Observer pattern?

**A:** State and Observer can be combined: when the state changes, interested parties are notified. The context maintains a list of observers; when `setState()` is called, the context notifies all observers of the new state. This allows external components to react to state changes without polling.

Example: a `NetworkConnection` that notifies a UI component when the connection state changes (connected, disconnected, error). The UI doesn't poll the connection state; it registers as an observer and updates itself when the state changes. The State pattern handles the connection's behavior; the Observer pattern handles state change notifications.

This combination is common in GUI frameworks: the model (context) holds state; the view (observer) is notified when the state changes and updates the display. The State pattern manages the model's behavior; the Observer pattern manages the model-view synchronization.

---

## Q56: How does the Strategy pattern support the Liskov Substitution Principle?

**A:** LSP requires that any strategy implementation be usable wherever the strategy interface is expected, without breaking client behavior. If `SortStrategy` defines `sort(List<T>)`, any implementation (QuickSort, MergeSort) must sort correctly and completely. A strategy that only sorts the first half of the list violates LSP.

Strategy interfaces should define clear behavioral contracts: preconditions (what the strategy expects), postconditions (what the strategy guarantees), and side effects (what the strategy modifies). All implementations must honor these contracts. Testing with LSP in mind: replace one strategy with another in all existing tests, and the tests should pass unchanged.

The danger with Strategy is that implementations might have different performance characteristics (time complexity, memory usage) but the same functional behavior. LSP is about behavioral substitution, not performance substitution. A slow strategy that produces correct results is LSP-compliant; a fast strategy that produces incorrect results is not.

---

## Q57: What is the benefit of using the Strategy pattern with configuration files?

**A:** Configuration files externalize strategy selection: the strategy class name is specified in a properties or YAML file, and the application loads and instantiates it at runtime. This allows strategy changes without code modifications or recompilation.

Example: `compression.strategy=org.example.FastCompressionStrategy` in a properties file. A factory reads this configuration, loads the class using reflection, and creates the strategy instance. Different environments (development, staging, production) can use different strategies by changing the configuration file.

Benefits: **(1) Environment-specific strategies** — different strategies for different deployment environments. **(2) Runtime changes** — some frameworks reload configuration without restarting. **(3) A/B testing** — different strategies for different users, controlled by configuration. **(4) Feature flags** — enable/disable strategies based on feature toggles. The trade-off is that configuration errors (wrong class name, incompatible interface) are caught at runtime, not compile time.

---

## Q58: How does the State pattern handle state entry and exit actions?

**A:** State entry and exit actions are operations performed when entering or leaving a state. Implement them in the state class: `enter()` is called by the context's `setState()` when transitioning to this state; `exit()` is called when transitioning away.

Example: `class ConnectedState implements State { void enter(Connection context) { startHeartbeat(); } void exit(Connection context) { stopHeartbeat(); } }`. When the context transitions to `ConnectedState`, the heartbeat starts; when it transitions away, the heartbeat stops. This encapsulates state-specific setup and teardown.

Entry/exit actions separate the "what happens when entering a state" from "how the state handles events." The state handles events in its event methods; entry/exit actions handle lifecycle concerns. This is cleaner than putting setup/teardown logic in every transition — the state itself knows what it needs when entering and exiting.

---

## Q59: What is the difference between Strategy and the Bridge pattern in terms of when the implementation is chosen?

**A:** Strategy chooses the algorithm at runtime — the client or factory selects the strategy dynamically, and it can be changed during the context's lifetime. Bridge typically selects the implementation at compile time or construction time — once chosen, it doesn't change.

Example: a `Sorter` with a `SortStrategy` can change its sorting algorithm at runtime: `sorter.setStrategy(new QuickSortStrategy())`. A `Shape` with a `DrawingImpl` (Bridge) typically has its implementation set at construction: `new Circle(new OpenGLImpl())` — the drawing implementation doesn't change.

The runtime vs. construction-time distinction is the key difference. Strategy implies dynamic selection; Bridge implies static binding. In practice, Bridge implementations could be dynamic, but the intent is different: Bridge separates abstraction from implementation for independent variation; Strategy selects algorithms for dynamic behavior change.

---

## Q60: How does the Template Method pattern support the Open/Closed Principle?

**A:** OCP says software should be open for extension but closed for modification. Template Method achieves this: the base class defines the algorithm skeleton (closed for modification) and subclasses extend it by overriding steps (open for extension). New behavior is added by creating new subclasses, not modifying the base class.

Example: `abstract class DataProcessor { final void process() { load(); transform(); save(); } abstract void load(); abstract void transform(); abstract void save(); }`. Adding a new processing variant means creating a new subclass that overrides `load()`, `transform()`, and `save()`. The base class's `process()` method is never modified.

The limitation: adding new steps to the algorithm (a new hook, a new phase) requires modifying the base class. Template Method is OCP-compliant for varying steps, not for varying the algorithm's structure. If the skeleton itself needs to change, the base class must be modified, affecting all subclasses.

---

## Q61: What is the relationship between the Strategy pattern and polymorphism?

**A:** Strategy leverages polymorphism: the context depends on the Strategy interface, and each concrete strategy is a polymorphic implementation. The context calls `strategy.execute()` without knowing which implementation executes — the runtime type determines the behavior.

This is a form of runtime polymorphism (dynamic dispatch). The compile-time type is the Strategy interface; the runtime type is the concrete strategy. The context's code is written against the interface, making it polymorphic across all strategy implementations.

Strategy extends polymorphism beyond class hierarchies: instead of subclassing the context to vary behavior, you compose the context with strategy objects. This provides the flexibility of polymorphism without the rigidity of inheritance. The Strategy pattern is "polymorphism through composition" rather than "polymorphism through inheritance."

---

## Q62: How does the State pattern handle event priority?

**A:** Event priority determines the order in which events are processed when multiple events are queued. The State pattern doesn't inherently handle priority — it processes events sequentially as they arrive. For prioritized events, use a priority queue between the event source and the state machine.

The state machine dequeues events in priority order and processes them through the current state. High-priority events (error, shutdown) are processed before low-priority events (heartbeat, status update). The priority logic is external to the state machine — the state machine simply processes events as they arrive, regardless of priority.

Implementation: the context has an event queue; events are added with priority levels; the context's event processing loop dequeues the highest-priority event first. The state object handles each event as usual — it doesn't know about priority. This separation of concerns (priority management vs. state behavior) keeps the state machine clean while supporting priority-based event processing.

---

## Q63: What is the benefit of combining Strategy with Factory pattern?

**A:** The Factory encapsulates strategy creation logic: the factory reads configuration, instantiates the appropriate strategy, and returns it. The context receives the strategy from the factory without knowing the concrete strategy class. This separates strategy selection (factory) from strategy usage (context).

Without Factory, the context or client must know concrete strategy classes to create them. With Factory, the context depends on the Factory interface and the Strategy interface — no knowledge of concrete classes. This maximizes decoupling and follows DI principles.

The Factory can implement complex creation logic: loading strategy configuration from a database, creating strategies with dependencies (injected via constructor), or creating composite strategies (chaining multiple strategies). This complexity belongs in the Factory, not in the context or client.

---

## Q64: How does the Template Method pattern handle multiple inheritance in languages like C++?

**A:** In C++, the Template Method base class provides the algorithm skeleton. Subclasses inherit from it and override virtual methods. Multiple inheritance is possible: a class can inherit Template Methods from multiple base classes, each defining different algorithm skeletons.

However, multiple inheritance of Template Methods can cause ambiguity: if two base classes define the same Template Method name, the derived class must resolve the ambiguity. Virtual inheritance handles the diamond problem, but adds complexity.

In practice, prefer single inheritance for Template Methods. If you need behavior from multiple sources, use Composition (Strategy pattern) instead of multiple inheritance. C++ abstract classes (pure virtual methods) work well for Template Method base classes, providing the skeleton while requiring subclasses to implement the steps.

---

## Q65: Where does the decision logic live in Strategy versus Specification, and when is each the better fit?

**A:** Specification objects encapsulate business rules as Strategy objects for validation or filtering. Each Specification is a Strategy that evaluates a condition: `spec.isSatisfiedBy(object)` returns true or false. Different Specifications encapsulate different rules; they're interchangeable and composable.

Specification extends Strategy by adding composition: `AND`, `OR`, `NOT` operations combine Specifications into complex rules. This is Strategy with algebra: `new AndSpecification<>(ageSpec, creditSpec)` creates a composite Strategy that requires both sub-specifications to be satisfied.

The key difference from pure Strategy: Specifications produce boolean results (evaluation); Strategies produce arbitrary results (transformation, computation). Specifications are Strategies specialized for business rule evaluation, with built-in composition operators for combining rules.

---

## Q66: How does the State pattern support the Open/Closed Principle?

**A:** OCP: open for extension, closed for modification. The State pattern achieves this for state machines: adding a new state means creating a new state class, not modifying existing states or the context. The context and existing states remain unchanged.

Example: a `TrafficLight` has `RedState`, `YellowState`, `GreenState`. Adding a `FlashingYellowState` means creating a new class and updating the transition table (or the relevant state's transition logic). The existing states and the `TrafficLight` context don't change.

The limitation: adding a new event (that existing states don't handle) requires modifying existing state classes to handle the new event. OCP is satisfied for states (new states don't modify existing ones) but not for events (new events may require modifying existing states). To satisfy OCP for events, use a transition table or event-driven state machine where states register their event handlers.

---

## Q67: What is the difference between Strategy and the Currying pattern in functional programming?

**A:** Strategy encapsulates an algorithm as an object; Currying transforms a multi-argument function into a sequence of single-argument functions. Strategy is OOP behavioral encapsulation; Currying is functional programming technique for function composition.

Currying can implement Strategy-like behavior: `sort(comparator)` returns a function that sorts using the comparator. The comparator is a strategy, but Currying creates it as a function, not an object. The resulting function is a Strategy without the OOP overhead.

In practice, Currying is used to create specialized functions from general ones: `add(5)` creates a function that adds 5 to its argument. This is Strategy at the function level — the specialized function is a strategy for adding 5. The distinction is stylistic, not structural: Currying is Strategy through function specialization.

---

## Q68: How does the Template Method pattern support versioning in libraries?

**A:** Libraries use Template Method to provide stable algorithm skeletons while allowing step customization. New versions can add new hooks (optional override points) without breaking existing subclasses — the default implementations are empty or backward-compatible.

When the skeleton changes (reordering steps, adding mandatory steps), existing subclasses break. To avoid this: make new steps hook methods (not abstract), provide backward-compatible defaults, and deprecate old hooks rather than removing them. This maintains backward compatibility while enabling extension.

Libraries like Spring use Template Method extensively: `AbstractBeanFactory` defines the bean creation template; subclasses override `createBean()`, `doGetBean()`, etc. New versions add hooks (`resolveBeforeInstantiation()`) with default implementations. Existing subclasses are unaffected because they don't override the new hooks.

---

## Q69: What is the benefit of using the Strategy pattern for configuration-driven behavior?

**A:** Configuration-driven Strategy: the strategy to use is specified in configuration (properties file, database, environment variables), not in code. The application loads the strategy class name from configuration, instantiates it (via reflection or DI), and injects it into the context.

Benefits: **(1) Deployment-specific behavior** — different strategies for different environments without code changes. **(2) Runtime reconfiguration** — some applications reload configuration and swap strategies without restart. **(3) Feature flags** — toggle strategies based on feature flags for A/B testing or gradual rollouts. **(4) Ops control** — operations can change behavior (retry strategy, caching policy) without developer involvement.

The trade-off: configuration errors are runtime errors, not compile-time errors. A typo in the strategy class name causes a `ClassNotFoundException` at runtime. Mitigation: validate configuration at startup (fail-fast), use DI container validation, and provide default strategies as fallback.

---

## Q70: How does the State pattern handle state-dependent permissions?

**A:** Each state defines what operations are permitted in that state. The state object implements the context's methods and either executes the operation (if permitted) or throws an exception / returns an error (if not permitted). This makes permissions state-specific and explicit.

Example: `class DraftState implements OrderState { void submit(Order context) { // permitted: transition to SubmittedState context.setState(new SubmittedState()); } void ship(Order context) { throw new IllegalStateException("Cannot ship a draft order"); } }`. The `ship()` operation is not permitted in `DraftState`, so it throws an exception. In `SubmittedState`, `ship()` would be permitted.

This is superior to checking state in every method: `if (state == DRAFT) throw ...`. The permission logic is encapsulated in the state class, not scattered across the context. Each state clearly documents what operations it supports and which it rejects.

---

## Q71: What is the relationship between Strategy and the Pipeline pattern?

**A:** Pipeline chains multiple processing stages, each performing a transformation. Each stage is a Strategy: it receives input, processes it, and produces output. The Pipeline composes strategies sequentially: output of stage 1 becomes input of stage 2.

This is Strategy with ordered composition. Instead of choosing one strategy (Strategy pattern), you chain multiple strategies (Pipeline). Each strategy is independent (can be tested, reused, replaced), but the pipeline defines their execution order.

The Pipeline pattern is Strategy applied to sequential processing. `Pipeline<String, Report>` chains `ParseStrategy`, `ValidateStrategy`, `TransformStrategy`, `ReportStrategy`. Each strategy is independently swappable, but the pipeline ensures they execute in the correct order. This combines Strategy's interchangeability with pipeline's sequential composition.

---

## Q72: How does the Template Method pattern handle asynchronous operations?

**A:** Template Methods can define asynchronous algorithms by making the template method return a `Future` or `CompletableFuture`. Subclass steps can be synchronous or asynchronous; the template method orchestrates them asynchronously.

Example: `abstract class AsyncDataProcessor { final CompletableFuture<Result> process() { return loadData().thenCompose(this::transform).thenCompose(this::save); } abstract CompletableFuture<Data> loadData(); abstract CompletableFuture<ProcessedData> transform(Data data); abstract CompletableFuture<Result> save(ProcessedData data); }`. Each step returns a `CompletableFuture`; the template chains them asynchronously.

The challenge: error handling and cancellation. `CompletableFuture` handles errors through `exceptionally()` and `handle()`. Cancellation propagates through the future chain. The template method must handle errors at each step and ensure resources are cleaned up on cancellation. This is more complex than synchronous Template Methods but provides non-blocking execution.

---

## Q73: What is the difference between Strategy and the Callback pattern?

**A:** Strategy is a named, interchangeable algorithm object. Callback is a function invoked after an operation completes. Strategy is synchronous or asynchronous, used for algorithm selection. Callbacks are typically asynchronous, used for notification or continuation.

In practice, a Callback is a degenerate Strategy: a strategy with a single method (`onComplete()`), typically implemented as a lambda. Strategy implies multiple potential algorithms; Callback implies a single response handler. Strategy is proactive (the context delegates to the strategy); Callback is reactive (the framework calls the callback).

Modern languages blur the distinction: function references serve as both Strategies and Callbacks. `comparator` is a Strategy; `onSuccess(callback)` is a Callback. The structural pattern (passing a function reference to a context) is identical. The intent differs: Strategy for algorithm selection, Callbacks for event handling.

---

## Q74: How does the State pattern support testing state-specific behavior?

**A:** Test each state in isolation: create the state object, inject a mock context, call the state's methods, and verify: (1) the correct behavior occurs, (2) the correct transitions are made, (3) invalid operations throw appropriate exceptions.

Test transitions by verifying that after a method call on one state, the context's state changes to the expected next state, and subsequent behavior matches the new state. This tests the state machine's behavior across state boundaries.

Test the complete state machine by simulating sequences of events: start in the initial state, send events, and verify the machine ends in the expected state with the expected side effects. Use state machine testing frameworks (like ` junit-datamanager` or custom state machine testers) for systematic coverage of all state × event combinations.

---

## Q75: What is the benefit of the Strategy pattern for algorithm benchmarking?

**A:** Strategy makes it easy to benchmark multiple algorithms: create instances of each strategy, run the same input through each, and compare execution time, memory usage, and output quality. The benchmark framework creates each strategy independently, ensuring fair comparison.

Example: benchmark `BubbleSortStrategy`, `QuickSortStrategy`, and `MergeSortStrategy` with various input sizes and distributions. The Strategy pattern ensures all strategies receive the same interface and input format, making the benchmark fair. The strategies are independent — no shared state that could bias results.

The benchmark results inform strategy selection: for small inputs, `BubbleSort` might be fastest (due to low overhead); for large inputs, `QuickSort` wins. The strategy selection logic can use these benchmarks to choose the optimal algorithm based on input characteristics, creating a self-optimizing system.

---

## Q76: How does the Template Method pattern support plugin architectures?

**A:** Plugin architectures define a base class with a Template Method that orchestrates plugin execution. Plugins implement the abstract/hook methods, providing specific behavior. The base class controls the plugin lifecycle (initialization, execution, cleanup); plugins implement the business logic.

Example: an IDE with a `CodeAnalysis` base class that defines: `loadSource() → parse() → analyze() → report()`. Plugins implement `analyze()` for different analysis types (linting, security, performance). The base class handles source loading, parsing, and report generation; plugins focus on their specific analysis.

The key is that the base class is distributed as a library/SDK. Plugin developers extend the base class and implement the required methods. The base class's Template Method ensures consistent behavior across all plugins. New plugins are added by implementing new subclasses, not modifying the base class or existing plugins — OCP in action.

---

## Q77: What is the relationship between Strategy and the Adapter pattern?

**A:** An Adapter can implement a Strategy interface: the Adapter wraps an incompatible interface behind the Strategy interface, making the adapted object usable as a Strategy. This combines interface translation (Adapter) with algorithm selection (Strategy).

Example: a third-party library provides `LegacySorter.sort(int[])`, but your system uses `SortStrategy.sort(List<Integer>)`. An `LegacySorterAdapter` implements `SortStrategy` and translates between the two interfaces: it converts `List<Integer>` to `int[]`, calls the legacy sorter, and converts the result back.

This is useful when integrating external libraries as Strategies: the Adapter translates the external library's interface to your Strategy interface, making it interchangeable with internally-defined strategies. The Strategy pattern selects algorithms; the Adapter pattern makes external algorithms compatible with the Strategy interface.

---

## Q78: How does the State pattern handle persistence of state?

**A:** State objects can be serialized and restored to persist the state machine's state across application restarts. Each state class implements serialization (e.g., `Serializable` in Java, `__getstate__`/`__setstate__` in Python). The context serializes its current state reference; on deserialization, it restores the state from the serialized form.

Example: a `ShoppingCart` with states `EmptyState`, `HasItemsState`, `CheckedOutState`. The current state is serialized when the user's session is saved. On session restoration, the state is deserialized, and the cart continues in its previous state. The user doesn't need to restart from the beginning.

Challenges: **(1) State-specific data** — if the state object holds transient data (counters, caches), this data is lost on serialization. **(2) State identity** — deserialization creates a new state object; compare by type, not by reference. **(3) Version compatibility** — serialized states must be compatible across application versions (class versioning, field addition/removal).

---

## Q79: What is the difference between Strategy and the Command pattern for undo/redo?

**A:** Command encapsulates actions with undo/redo support. Each Command stores enough information to reverse its effect: `ExecuteCommand` stores the state before execution; `undo()` restores it. Strategy encapsulates algorithms without undo semantics — Strategy computes results but doesn't track how to reverse its computation.

The structural difference: Command methods are paired (`execute()`/`undo()`); Strategy methods are standalone (`compute()`). Command is stateful (stores pre/post state for undo); Strategy is typically stateless (pure computation).

For undo/redo functionality, Command is appropriate. For algorithm selection without undo, Strategy is appropriate. They can be combined: a `Command` that delegates to a `Strategy` for computation, with the Command handling undo/redo around the Strategy's computation. The Command stores the input data and uses the Strategy for the forward computation; undo restores the stored input.

---

## Q80: How does the Template Method pattern support internationalization (i18n)?

**A:** Template Methods can define i18n as a cross-cutting concern at the template level: the base class handles locale detection, resource bundle loading, and message formatting. Subclass steps (which generate user-facing text) call the base class's i18n methods: `getMessage("welcome.message")`.

The base class's Template Method includes locale setup: `final void render() { Locale locale = detectLocale(); loadResources(locale); doRender(); formatOutput(); }`. Subclasses implement `doRender()` and use the base class's `getMessage()` for localized strings. This ensures consistent i18n handling across all subclasses.

The alternative (each subclass handles i18n independently) leads to inconsistency: some subclasses might forget to localize, others might use different resource bundles. The Template Method centralizes i18n at the algorithm level, ensuring all subclasses produce localized output consistently.

---

## Q81: What is the relationship between Strategy and the Proxy pattern?

**A:** A Proxy can delegate to a Strategy, or a Strategy can wrap a Proxy. A **Caching Proxy** is a Strategy that caches results: `CachingCompressionStrategy` wraps `CompressionStrategy` and adds caching. The Proxy pattern's indirection (delegate to another object) is the mechanism; the Strategy pattern's intent (algorithm selection) is the purpose.

Example: a `LazyStrategy` (Virtual Proxy) creates the actual strategy on first use. The context receives a `LazyStrategy` that defers expensive strategy creation. On first `execute()`, the `LazyStrategy` creates the real strategy and delegates. This combines Proxy's lazy initialization with Strategy's algorithm selection.

The combination provides: **(1) Lazy loading** — strategy creation is deferred until needed. **(2) Caching** — strategy results are cached. **(3) Logging** — strategy execution is logged. All these are Proxy concerns applied to Strategy objects. The Proxy adds cross-cutting behavior; the Strategy provides the algorithmic behavior.

---

## Q82: How does the State pattern handle multiple simultaneous events?

**A:** The basic State pattern processes events sequentially. For simultaneous events, use an event queue: events are enqueued and processed one at a time by the state machine. This ensures consistent state transitions and avoids race conditions.

For truly concurrent events that must be processed simultaneously, each event stream needs its own state machine instance. A `Connection` might have separate state machines for the read channel and write channel, each processing events independently. The context coordinates between the state machines if needed.

Alternatively, use a **hierarchical concurrent state machine** where the top-level state machine manages the overall state and child state machines handle concurrent sub-processes. This is complex but models real-world systems (network protocols, workflow engines) where multiple state machines operate concurrently within a larger system.

---

## Q83: What is the benefit of using the Strategy pattern for A/B testing?

**A:** Strategy enables A/B testing by injecting different algorithm variants based on user segments. A `RecommendationStrategy` interface has `StrategyA` (current algorithm) and `StrategyB` (experimental algorithm). The A/B testing framework selects the strategy based on user group assignment.

The framework routes users to strategies: 50% get Strategy A, 50% get Strategy B. The strategies are independent — no shared state that could bias results. The framework tracks metrics (conversion rate, click-through rate) for each strategy and determines the winner.

This is configuration-driven Strategy: the strategy selection is based on A/B test configuration, not code changes. When the test concludes, the losing strategy is removed, and the winning strategy becomes the default. The A/B testing framework is the Factory that selects strategies based on experiment configuration.

---

## Q84: How does the Template Method pattern handle logging and monitoring?

**A:** The Template Method base class includes logging at the algorithm level: log the algorithm's start, each step's execution, and the algorithm's completion. Subclass steps don't need logging — it's handled by the template.

Example: `abstract class DataPipeline { final void execute() { log.info("Pipeline started"); step1(); log.info("Step 1 completed"); step2(); log.info("Step 2 completed"); log.info("Pipeline completed in {}ms", duration); } }`. All subclasses get logging automatically.

For more granular logging, use hook methods: `beforeStep()` and `afterStep()` hooks that subclasses can override to add step-specific logging. The base class provides default (no-op) hooks; subclasses add logging only for steps that need it. This combines centralized logging (in the template) with optional per-step logging (via hooks).

---

## Q85: What is the difference between Strategy and the Visitor pattern?

**A:** Strategy encapsulates interchangeable algorithms applied to an object. Visitor encapsulates operations applied to a family of objects. Strategy is about "how to do something"; Visitor is about "what to do with different things."

Strategy adds behavior to one object (the context). Visitor adds behavior to multiple object types (elements). Strategy is selected by the client; Visitor is dispatched by the element's type. Strategy changes the context's behavior; Visitor adds operations without modifying elements.

The confusion arises because both patterns add behavior through delegation. The key difference: Strategy replaces an algorithm (one strategy executes); Visitor adds operations (multiple visit methods, one per element type). Strategy is horizontal variation (which algorithm); Visitor is vertical variation (which operation).

---

## Q86: How does the State pattern handle state timeouts?

**A:** State timeouts define automatic transitions when a state is active for too long. Implement timeouts using timers: the context starts a timer when entering a state; if the timer expires before an event arrives, the state machine transitions to a timeout state.

Example: `class WaitingForPaymentState implements State { void enter(Order context) { timer.schedule(() -> context.transition(new PaymentTimedOutState()), 30, MINUTES); } void exit(Order context) { timer.cancel(); } }`. If payment doesn't arrive within 30 minutes, the order transitions to `PaymentTimedOutState`.

The timer must be cancelled when leaving the state (in `exit()`) to prevent spurious timeouts. The timeout is a transition trigger, like any other event. The state machine handles the timeout transition in the timeout state's event handler, ensuring consistent behavior.

---

## Q87: What is the relationship between Strategy and the Mediator pattern?

**A:** Strategy encapsulates algorithms; Mediator encapsulates interactions between objects. They're complementary: Strategy provides the algorithm; Mediator coordinates the communication between the Strategy and its collaborators.

Example: a `TradeExecution` system uses a `TradingStrategy` (Strategy) for order execution. A `TradeMediator` (Mediator) coordinates between the `TradingStrategy`, `RiskManager`, `ComplianceChecker`, and `OrderBook`. The Mediator ensures the Strategy is called at the right time with the right data, and that the results are distributed to the correct collaborators.

The combination: Strategy handles "how to execute a trade"; Mediator handles "who needs to be involved in executing a trade." Strategy is algorithmic; Mediator is communicational. Together, they provide both algorithm selection and interaction coordination.

---

## Q88: How does the Template Method pattern support caching at the algorithm level?

**A:** The Template Method can include caching at the algorithm level: the base class caches the algorithm's result based on input. If the same input is processed again, the cached result is returned without executing the steps.

Example: `abstract class ExpensiveComputation { private final Map<Input, Result> cache = new ConcurrentHashMap<>(); final Result compute(Input input) { return cache.computeIfAbsent(input, this::doCompute); } private Result doCompute(Input input) { return step1(input); // subclass method } }`. The `compute()` Template Method caches; `doCompute()` is the actual computation (overridden by subclasses).

This combines Template Method (algorithm skeleton) with caching (result memoization). The caching logic is centralized in the base class; subclasses implement the computation. Different subclasses get caching automatically without implementing it themselves.

---

## Q89: What is the benefit of using Strategy with aspect-oriented programming (AOP)?

**A:** AOP handles cross-cutting concerns (logging, security, transactions) that apply to multiple strategies. Instead of adding logging to each strategy, AOP adds logging to all strategy executions through a pointcut: `@Around("execution(* *Strategy.execute(..))") public Object log(ProceedingJoinPoint pjp) { ... }`.

Benefits: **(1) Clean strategies** — strategies contain only algorithm logic, no cross-cutting concerns. **(2) Centralized concerns** — logging, security, and transactions are defined once in aspects, not duplicated across strategies. **(3) Consistent behavior** — all strategies get the same cross-cutting behavior automatically.

The combination: Strategy handles algorithm selection; AOP handles cross-cutting concerns. Strategies are pure algorithms; aspects add infrastructure. This maximizes SRP: strategies have one reason to change (algorithm changes); aspects have one reason to change (infrastructure changes).

---

## Q90: How does the State pattern handle state machine visualization?

**A:** State machines can be visualized as state diagrams using tools like PlantUML, Graphviz, or statechart libraries. Each state is a node; each transition is a labeled edge. Guards and actions are annotations on the edges.

For runtime visualization, the context can emit state change events that a visualization tool consumes. The tool draws the current state machine, highlighting the active state and recent transitions. This is useful for debugging complex state machines where the current state isn't obvious from the code.

The State pattern's structure maps directly to state diagrams: each state class corresponds to a diagram node; each transition (method call that changes state) corresponds to a diagram edge. This 1:1 mapping makes it straightforward to generate diagrams from code or validate code against diagrams.

---

## Q91: What is the difference between Strategy and the Decorator pattern for behavior composition?

**A:** Strategy provides one of several interchangeable behaviors (selection). Decorator adds behavior to an existing behavior (composition). Strategy: choose algorithm A, B, or C. Decorator: apply behavior X on top of behavior Y on top of behavior Z.

Example: `CompressionStrategy` selects between `GzipStrategy`, `LZ4Strategy`, `ZstdStrategy`. `CompressionDecorator` wraps any strategy with logging, metrics, or retry logic. Strategy is horizontal (which algorithm); Decorator is vertical (what additional behavior).

They compose naturally: `new RetryDecorator(new MetricsDecorator(new GzipStrategy()))` selects the Gzip algorithm (Strategy) with metrics and retry (Decorators). The Strategy pattern handles algorithm selection; the Decorator pattern handles algorithm enhancement. Together, they provide maximum flexibility.

---

## Q92: How does the Template Method pattern handle dependency injection in subclass steps?

**A:** Subclass steps may need dependencies (services, repositories, external clients). These dependencies should be injected into the base class or the subclass, not created within the steps. The Template Method base class can accept dependencies through its constructor and make them available to subclasses.

Example: `abstract class ReportGenerator { private final DataSource dataSource; protected ReportGenerator(DataSource dataSource) { this.dataSource = dataSource; } protected DataSource getDataSource() { return dataSource; } abstract void extractData(); }`. Subclasses access dependencies through getter methods on the base class.

This ensures dependencies are injectable (for testing, configuration) and don't leak from subclass to subclass. The base class manages dependencies; subclasses use them through the base class's API. DI containers can inject dependencies into the base class constructor, making all subclass steps automatically injectable.

---

## Q93: What is the relationship between Strategy and the Null Object pattern?

**A:** Null Object is a special Strategy that performs no operation. Instead of null-checking before calling a strategy, provide a Null Object that safely does nothing. `NullCompressionStrategy.compress(data)` returns the data unchanged. This eliminates null checks: the context always calls the strategy, and the Null Object is a safe no-op.

The Null Object Strategy is useful when: **(1)** The strategy is optional (logging, notification, caching). **(2)** Null checks are scattered across client code. **(3)** The "do nothing" behavior is well-defined and safe.

Example: `NullNotificationStrategy.send(message)` does nothing; `EmailNotificationStrategy.send(message)` sends an email. The context doesn't check `if (notificationStrategy != null)` — it always calls `send()`, and the Null Object safely ignores it. This simplifies client code and follows the "tell, don't ask" principle.

---

## Q94: How does the State pattern handle state machine serialization for distributed systems?

**A:** In distributed systems, state machines must be serializable for transmission across the network or persistence in databases. Each state class implements serialization (e.g., `Serializable`, protobuf, JSON). The context serializes its current state and state-specific data; the remote system deserializes and continues.

Example: a workflow engine serializes the current state of each workflow instance. When the instance is processed by a different server, it deserializes and continues from the serialized state. This enables horizontal scaling: workflow instances can be processed by any server.

Challenges: **(1) State-specific data** — transient data (counters, open connections) can't be serialized. **(2) State identity** — compare deserialized states by type, not reference. **(3) Version compatibility** — serialized states must be backward-compatible across deployments. **(4) Performance** — serialization/deserialization adds latency; use binary formats (protobuf, Kryo) for performance.

---

## Q95: What is the benefit of using the Strategy pattern for runtime algorithm optimization?

**A:** Strategy enables runtime algorithm optimization: the system monitors performance and switches strategies based on observed conditions. A `LoadBalancerStrategy` switches between `RoundRobinStrategy` and `LeastConnectionsStrategy` based on server load metrics.

This creates a self-optimizing system: the strategy selection adapts to runtime conditions. The monitoring system collects metrics; the strategy selector uses metrics to choose the optimal strategy. This is Strategy with feedback: performance data influences strategy selection.

Example: a `CompressionStrategy` switches between `LZ4Strategy` (fast, low compression) and `ZstdStrategy` (slow, high compression) based on network bandwidth. When bandwidth is high, use LZ4 (fast). When bandwidth is low, use Zstd (compress more). The strategy selection adapts to runtime conditions automatically.

---

## Q96: How does the Template Method pattern support concurrent execution of steps?

**A:** Template Methods can execute steps concurrently using `CompletableFuture` (Java), `asyncio` (Python), or similar frameworks. Each step returns a future; the template method orchestrates them: `thenCompose()` for sequential steps, `thenCombine()` for parallel steps.

Example: `abstract class DataEnrichment { final CompletableFuture<EnrichedData> enrich(RawData data) { CompletableFuture<User> userFuture = fetchUser(data.getUserId()); CompletableFuture<Product> productFuture = fetchProduct(data.getProductId()); return userFuture.thenCombine(productFuture, (user, product) -> buildEnrichedData(data, user, product)); } }`. The two `fetch` steps run concurrently; the result is combined after both complete.

The template method defines which steps run concurrently and which are sequential. Subclasses implement each step independently; the template handles concurrency orchestration. This combines Template Method's algorithm structure with concurrent execution's performance benefits.

---

## Q97: What is the difference between Strategy and the Chain of Responsibility pattern?

**A:** Strategy selects one algorithm from a set. Chain of Responsibility tries multiple handlers in order until one handles the request. Strategy: exactly one algorithm executes. Chain: zero or more handlers execute, depending on whether each handler chooses to handle the request.

Example: `ValidationChain` has `NotNullValidator`, `LengthValidator`, `FormatValidator`. Each handler checks one aspect and passes the request to the next if valid. If any handler fails, the chain stops. This is Chain of Responsibility, not Strategy — multiple validators execute, not just one.

The confusion arises because both patterns use delegation. The key difference: Strategy selects one (mutually exclusive); Chain tries multiple (cumulative). Strategy: "I'll use algorithm A." Chain: "I'll try handler A, then B, then C until one succeeds."

---

## Q98: How does the State pattern support state machine testing frameworks?

**A:** State machine testing frameworks (like `JUnit` with state machine extensions, `xstate` test utilities, or custom test harnesses) provide tools for systematic state machine testing. They generate test cases from the state machine definition, covering all state × event combinations.

The framework: **(1)** Reads the state machine definition (states, events, transitions). **(2)** Generates test cases that exercise each transition. **(3)** Verifies that each transition produces the expected result and side effects. **(4)** Reports untested states or transitions.

For the State pattern, the framework creates the context, drives events through it, and verifies the state transitions. This provides systematic coverage that manual testing might miss. Property-based testing frameworks can generate random event sequences and verify that the state machine never reaches an invalid state.

---

## Q99: What is the relationship between the Strategy pattern and the Builder pattern?

**A:** Builder constructs complex objects step by step. Strategy provides interchangeable algorithms. They're complementary: Builder constructs the object; Strategy provides the algorithms used during construction.

Example: a `QueryBuilder` uses different `GenerationStrategy` for SQL generation: `MySQLGenerationStrategy` generates MySQL syntax; `PostgreSQLGenerationStrategy` generates PostgreSQL syntax. The Builder constructs the query; the Strategy generates the SQL. The Builder is the context that delegates SQL generation to the Strategy.

The combination: Builder handles object construction structure (what parts to assemble); Strategy handles the algorithm for each part (how to generate SQL, how to validate, how to format). Builder is structural; Strategy is behavioral. Together, they provide both construction orchestration and algorithm selection.

---

## Q100: How do Strategy, Template Method, and State patterns compare and when do you choose each?

**A:** All three delegate behavior to other objects, but their intents differ fundamentally.

**Strategy**: "Which algorithm should I use?" — Selects one of several interchangeable algorithms at runtime. Use when: you have multiple algorithm variants, need runtime selection, and want to follow OCP for algorithm changes. The context delegates entirely to the strategy.

**Template Method**: "What is the algorithm's structure?" — Defines an algorithm skeleton in a base class, letting subclasses override specific steps. Use when: you have a fixed algorithm structure with known variation points, want to enforce the algorithm's flow, and are comfortable with inheritance-based extension. The base class controls the flow.

**State**: "How should I behave in this state?" — Changes behavior based on internal state transitions. Use when: an object's behavior depends on its state, transitions are event-driven, and states have complex behavior that warrants separate classes. The state manages transitions.

**Decision framework**:
- Algorithm selection (which computation?) → **Strategy**
- Algorithm structure (what flow?) → **Template Method**
- State-dependent behavior (how to behave?) → **State**
- Runtime swappability needed → **Strategy or State**
- Compile-time structure enforcement → **Template Method**

They compose naturally: a Template Method can call Strategy objects for specific steps; a State can use Strategies for state-specific algorithms; a Strategy can implement a Template Method's step. Choose based on the primary design intent; combine patterns when multiple concerns need addressing.
