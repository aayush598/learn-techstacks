# Delegation and Object Collaboration Design — 100 Interview Q&A

## Q1: What is delegation in object-oriented programming, and how does it differ from inheritance?

**A:** Delegation is an object handing a request it received to another object that is better equipped to fulfill it. The receiving object (the delegate) performs the work, and the delegating object keeps responsibility for the public contract: the caller still talks to the first object, which forwards the message to the collaborator. It is runtime composition: the relationship is assembled and changed at runtime, whereas inheritance is a compile-time relationship fixed when the class is written.

Inheritance reuses behavior by *becoming* a specialization ("is-a"), exposing the parent's methods through the subtype and binding behavior statically. Delegation reuses behavior by *holding* a collaborator ("has-a") and forwarding messages; the same object can change which collaborator it forwards to at runtime, which inheritance cannot. That is why delegation is the engine behind "composition over inheritance": you get reuse without inheriting an implementation you cannot change.

The practical difference shows up in tests and evolution. With delegation you can substitute a fake collaborator and verify the delegation contract in isolation; with inheritance the parent's implementation is welded into the child, and changing the parent silently changes every subclass. Good design uses inheritance for polymorphic substitution of a stable contract and delegation for behavior that genuinely varies or is assembled at runtime.

## Q2: How does delegation relate to the "composition over inheritance" principle?

**A:** "Composition over inheritance" is a design guideline: prefer assembling behavior from collaborator objects, connected at runtime, over building deep class hierarchies that inherit behavior. Delegation is the mechanism that makes composition usable — an object composed of parts forwards each responsibility to the part that owns it, so the composed object offers a single clean contract while the real logic lives in collaborators.

The advantages are alignment with coding to interfaces, runtime swap-ability of behavior, and locality of change. With composition, you can change one collaborator's implementation, or swap in a new one, without touching the composed object or any caller. With inheritance, a change in a superclass ripples into every subclass, and there is no way to change behavior at runtime.

The principle is not absolute: delegation cannot replace inheritance when the contract itself truly requires subtype polymorphism or when you get many overlapping capabilities for free (Base64, Comparable). The mature answer is to note that most modern frameworks and codebases favor delegation because problems appear later than the design time when inheritance seemed cheap: deep hierarchies become rigid, fragile to refactoring, and impossible to extend without touching shared parents.

## Q3: What does "has-a vs is-a" have to do with object collaboration and delegation?

**A:** "Is-a" is inheritance: a `SavingsAccount` is an `Account`, so it inherits the account contract and may override parts of the behavior. "Has-a" is composition or aggregation: an `Account` has a `Ledger` and delegates balance-history queries to it. "Has-a" is the relationship that produces delegation — when an object needs behavior it does not implement, it holds a collaborator and forwards to it.

The two answers lead to different designs for the same problem. If you model a `Rectangle` and later discover a `Square`, forcing "Square is-a Rectangle" creates invariant problems (the classic setWidth/ setHeight trap); modeling "a square has-a dimension and is-a quadrilateral" via delegation keeps the geometry rules in one place. The guideline is: prefer "has-a" when capabilities are implements-not-specializes, and reserve "is-a" for genuine subtype-of relationships where every instance of the child is substitutable for the parent.

Interviewers ask this to see whether you can reframe "is-a" intuitions. A strong answer shows how "has-a" enables runtime variation (swap the strategy), smaller test surfaces (instantiate with fakes), and single-responsibility classes (each collaborator does one thing), while "is-a" bakes an assumption into the type hierarchy that is nearly impossible to retract later without breaking callers.

## Q4: How do you delegate work when an object receives a message it cannot handle itself?

**A:** The receiving object forwards the message to a collaborator that does handle it, preserving the original call's semantics as much as possible. The usual shape is: the object holds a reference to the delegate, exposes the same method on its own interface, and in the body calls `delegate.method(...)`, optionally translating arguments or the return value to keep the delegating object's contract.

The forwarding can be a pure pass-through (same name, same types) or an adaptive delegation where the object interprets the message and decides which collaborator — possibly of several — should get it. Adaptive delegation is what coordinator and facade objects do: they are full citizens in the collaboration, not just relays, and they may add their own concerns (validation, logging, transaction boundaries) around the forwarded call.

The key discipline is to keep the *object responsible* for its contract even when it *delegates work*. That means: do not blindly forward state access without understanding what you expose, do not forward an internal failure mode that leaks delegate internals, and do not make the delegation so transparent that callers reach through and couple to the delegate's shape (a Law-of-Demeter violation). Delegation is a division of labor, not an abdication of responsibility.

## Q5: What is a collaborator, and how does it differ from a dependency?

**A:** A collaborator is any object your object talks to in order to do its job — the object that receives forwarded messages and returns results or performs side effects. A dependency is the broader set of types and values your class needs to function at all: collaborators, data structures, configuration, and even the types that appear in your method signatures. Collaborator is the behavior-centric view; dependency is the structural view.

In practice every collaborator is a dependency, but not every dependency is a behavior collaborator. An options struct or a reference to a config registry is a dependency your object reads, while a `PaymentGateway` or `Validator` is a collaborator your object sends messages to. The distinction matters for design: collaborators should be behind interfaces so you can swap or fake them, while pure-data dependencies can be plain values.

Interviews use this vocabulary to test whether you can articulate the object graph. A focused answer names the collaborators of a class explicitly (the messages it sends, the interfaces it requires), and separates them from incidental dependencies (timing, IO, singletons) — because the collaborators are what you design, mock, and evolve, while incidental dependencies are what you want to inject or remove.

## Q6: What is the difference between delegating behavior and inheriting behavior at runtime?

**A:** Inherited behavior is resolved through the type hierarchy at compile/load time and is fixed unless a subclass overrides it. Delegated behavior is resolved through object references at runtime: the delegating object forwards a message to whatever collaborator instance it currently holds, and the collaborator's dynamic type decides the actual implementation — possibly differently on different calls if the reference is swapped.

The important consequence is *variability without hierarchy*. Inheritance lets you vary behavior by creating subclasses, which multiplies classes combinatorially when behaviors combine (a `PDFWithLoggingAndMetrics`). Delegation varies behavior by exchanging collaborators, so you assemble behavior from parts: a document object holds a rendering strategy, a logging decorator holds the document, and a metrics decorator wraps the logging one — each added dimension is one class, not a Cartesian product of subclasses.

Runtime delegation also changes *when* decisions happen. With inheritance the decision of who does the work is fixed when the class is written; with delegation it can depend on state at the time of the call (pick a strategy based on input, swap a delegate during an operation). That flexibility is why delegation is favored for extension points, while inheritance remains preferred for sharing a stable contract that is genuinely a specialization of the parent.

## Q7: What is the role of interfaces in object collaboration?

**A:** Interfaces are the contract layer between collaborators: they define the set of messages that can flow between objects without pinning either side to a concrete class. A delegating object depends on the interface of its collaborator, and the collaborator implements that interface; both sides can be replaced independently, which is exactly what makes delegation a strong reuse mechanism.

Without interfaces, delegation collapses into concrete coupling: the delegator names a specific class, so swapping behavior requires editing the delegator and every context that builds it. With interfaces, the delegator's code is indifferent to the concrete collaborator, and the wiring — where the concrete collaborator is chosen — moves to construction time. This is the separation of "design of collaborations" from "assembly of collaborations."

Interviewers expect the nuance that interfaces should be *role-based and role-appropriate*: they should express what the delegator needs (the supplier side of the contract), not mirror a fat class. Segregating interfaces to the actual messages sent keeps fake collaborators cheap and prevents a delegator from depending on capabilities it never exercises — the same idea underlies the Interface Segregation Principle downstream.

## Q8: What is a "contract" between collaborating objects?

**A:** A contract is the agreed behavior between a supplier and a client object: what inputs are legal, what outputs are guaranteed, what exceptions can arise, and what state transitions may happen as a side effect. In OO terms it is the interface plus the semantics and invariants that the interface alone does not express — the preconditions, postconditions, and ordering rules of the collaboration.

Contracts make delegation trustworthy. When object A delegates to object B, A relies on B's postcondition to continue correctly; if B silently weakens that postcondition (returns null where the contract forbids it, mutates state it does not own), A's own contract breaks and the bug shows up far from B. Those bugs are why Design by Contract — explicit pre/post conditions and invariants, enforced with assertions or the type system — matters for collaboration-heavy designs.

The contract is also the tool for safe substitution. A collaborator can be swapped for another only if the new one honors the same contract, not merely the same method signatures. When you state the contract explicitly you can decide whether a fake, a decorator, or a new implementation actually preserves the obligations your delegator objects rely on.

## Q9: How does encapsulation survive when objects collaborate and delegate to each other?

**A:** Encapsulation governs each object's *internals*; collaboration governs its *externals*. An object can forward messages freely while still hiding its state and its collaborators' identities: callers know what the object can do (its contract), not how it does it or which parts it delegates to. Encapsulation survives because delegation is a private implementation detail of the delegating object.

The danger appears when delegation leaks: if a delegator returns collaborators from getters, or requires callers to pass a collaborator into its method signatures, callers start depending on the internal graph. At that point the object is overloaded as a data holder, its encapsulation cracks, and changes to the object graph ripple through every caller. Tell-don't-ask and the Law of Demeter are the guardrails that keep delegation compatible with encapsulation.

The deeper principle: an object owns its invariants even when it delegates the work. The `checkout()` object may delegate price computation, tax, and inventory to collaborators, but it still guards the invariant that checkout cannot complete with an empty cart. Delegating work while retaining invariant ownership is the distinction between a well-designed collaborating object and a hollow relay.

## Q10: What is an "object graph," and why does good design keep shared state out of it?

**A:** An object graph is the runtime network of instances holding references to each other — the actual shape of collaboration in memory, as opposed to the static class diagram. When code constructs objects and wires them together, it creates a graph whose edges are the references along which messages can travel; every delegation call you make at runtime is a traversal of an edge in that graph.

Shared state in the graph — several objects pointing at the same mutable object and writing to it — multiplies coupling. Any mutation by one holder can silently change behavior observed by another, so reasoning about a single method requires reasoning about every holder of the shared object. The design response is to minimize how many objects can write a given object at a given time: value objects as immutable snapshots for data that flows, ownership rules for parts of an aggregate, and references (rather than shared writable state) for cross-aggregate edges.

The interview point is that message passing is the healthy form of sharing: objects share interfaces and results, not internals. A clean object graph is acyclic or nearly so, has clear ownership of mutable regions, and lets you test any subgraph in isolation because its collaborators can be faked against their contracts.

## Q11: What does the Law of Demeter (don't talk to strangers) mean for delegation?

**A:** The Law of Demeter says a method should only talk to a small, known set of partners: itself, its own parameters, its own fields, and objects it creates. It forbids chains like `a.getB().getC().doIt()` — reaching through a collaborator into its collaborator. For delegation this is a design rule about *whose responsibility* a message is: if A owns B and B owns C, then A should ask B to do the thing that needs C, and B decides how to involve C.

The real harm the law guards against is *structural coupling*: A now depends on B's shape (that B exposes C) and on C's capabilities. That makes the object graph part of the public API; any re-arrangement of internal collaborators breaks callers. The fix usually shifts work between layers: A tells B what it wants, and B uses its collaborator C internally to fulfill it — that is delegation doing its job rather than a chain of getters.

Held literally, the law can produce "wrapper fever" — every object forwarding to the next. The mature answer is that the law is not about strict no-chaining but about keeping one hop and one intention per call, and preferring to tell objects what to do rather than interrogate them for references. It is a smell detector for designs where delegation has been replaced by navigation.

## Q12: Why is delegation sometimes described as "composition with forwarding"?

**A:** "Forwarding" is the mechanical act of taking an incoming message and re-sending it to another object, possibly unchanged. "Composition" is the structural fact that one object holds another. Delegation is both: an object is composed of (holds references to) collaborators and it forwards messages to them, so the two terms describe the same pattern from two angles — structure (composition) and behavior (forwarding).

The phrase emphasizes that delegation is a *distribution of labor* rather than an overloading of one object. Instead of one class implementing everything, the composed object carves up responsibilities and forwards each part to the owner of that capability. This is why "favor composition" and "favor delegation" are used almost interchangeably: both are anti-hierarchical, both make change local, and both produce small, testable pieces.

The caveat is that forwarding must be *deliberate*. Meaningless forwarding — relaying every method without any value-add, or forwarding a message and forgetting to forward a closely related one (the "half-delegation" bug) — is still coupling, minus the benefits of cohesion. Composition with forwarding is a good answer only when the composed object adds something: coordination, a narrower contract, or a stable umbrella over changing parts.

## Q13: What is the difference between event-driven collaboration and direct-call collaboration?

**A:** Direct-call collaboration is synchronous and explicit: object A holds a reference to B and invokes `B.doSomething()`, knowing exactly who serves the request; control flow and data flow follow the same path, and A must supply B (or its factory) at construction. Event-driven collaboration is decoupled: A raises an event, and whatever objects have subscribed — possibly zero, possibly several, possibly not yet born — react; A neither knows nor cares who consumes the event.

The trade-off is coupling versus determinism. Direct calls are easy to read, trace, and test — you can follow the collaboration in the code. Event-driven calls cut many edges in the object graph, making the system more extensible (new consumers attach without touching the producer) and more robust to producers changing, but they bury the flow of control: you can no longer read "who calls whom" from the code, and ordering, failure, and testing all become harder.

Interviewers want you to pick per relationship, not per religion. Domain events and callbacks decouple stable producers from many/unknown consumers; direct calls keep tight, transactional collaborations legible. A common healthy design is direct calls within a transaction or aggregate and events across transaction boundaries or subsystem borders — so determinism where it matters, decoupling where growth happens.

## Q14: How do objects decide who owns which responsibility in a collaboration?

**A:** This is the heart of responsibility-driven design: assign each responsibility to the object that has the *information and authority* to discharge it, rather than letting one object do everything. A walking example is an order object: price calculation belongs where the price-relevant data lives and where the rule is a coherent unit, tax belongs to a tax service, shipping to a shipping calculator; the order coordinates and holds the invariants.

Two heuristics guide the split. First, ask "who knows" and "who changes": state-holding objects own behavior over their own state (high cohesion), and cross-cutting computations move into collaborator objects (strategies, services, policies). Second, look at the direction of dependencies: a responsibility should live at the end of the dependency arrows, so that the objects that need it depend on an abstraction it provides, not the other way around.

The measurable outcome is a distribution where classes have one clear reason to change and collaborations are explicit: each object announces a small set of messages and will happily delegate anything not in its own wheelhouse. When responsibility is fuzzy, you see it as feature envy (a method spending most of its time on another object's data) and god objects (one class absorbs everything) — both are signals to re-draw the delegation boundaries.

## Q15: What is the difference between delegation and simple forwarding?

**A:** Forwarding is the mechanic: an incoming call is redirected to another object, often verbatim, with the delegator acting like a relay. Delegation is the relationship plus the *intent*: the delegator retains responsibility for the contract, may interpret, enrich, guard, or translate the call, chooses which collaborator to involve (possibly by state), and owns the outcome back to the caller.

Concretely, a pure forwarder `class A { B b; aMethod() { return b.aMethod(); } }` adds nothing but indirection; it is a thin shell. A delegator does more: it may handle errors, add a transactional wrapper, combine several forwarders, or enforce a precondition before forwarding — while still pushing the hard part to the specialist. In most real designs forwarding is the low-level primitive and delegation is the design that decides when and how to trigger it.

The distinction matters when evaluating wrappers and decorators. If a wrapper just forwards everything, you should question why it exists; if it forwards some messages and meaningfully handles others (adding behavior, narrowing the contract, translating semantics), it earns its place as a delegating object. The interview point is to show that you treat delegation as a division of responsibility, not as an excuse for forwarding without purpose.

## Q16: How do you decide between exposing a collaborator and hiding it behind an interface?

**A:** The rule of thumb: hide the collaborator from callers unless exposing it serves their need, and even then expose it through an interface, never as a raw class. Callers should interact with your object's contract; your collaborators are an implementation choice. If every caller reaches into your collaborators, your internal graph becomes public API and any re-arrangement breaks the world.

You hide collaborators when their identity is an implementation detail — a builder your object uses internally, a cache, a format converter. You expose through an interface when callers legitimately need to interact with a sub-capability independently: a `Document` exposing `Renderer` so callers can choose a rendering pipe, a `Session` exposing `QueryBuilder` as an interface so callers stay decoupled from the concrete dialect.

The deeper test is *who chooses*. If the caller needs to choose and swap the collaborator, expose the interface and accept the collaborator via a generalized design (strategy, plug-in). If the caller merely needs the result, keep the collaborator private and delegate. Whichever you pick, the concrete implementation belongs at assembly time, not leaked into running calls.

## Q17: How do delegation and the concepts of cohesion and coupling interact?

**A:** Coupling is the degree to which objects depend on each other; cohesion is the degree to which a class's elements belong together. Delegation, done well, lowers coupling between classes (each talks to collaborators through narrow interfaces) while raising the cohesion of each class (each object owns the behavior that is really about its own data). The two goals work together: small classes with focused responsibilities naturally need each other, and the pin-cushion that connects them is messages, not shared fields.

The failure modes are both extremes. Too much delegation produces a severe coupling cost anyway — every hop is an indirection, every indirection hides state and complicates tracing; you end up with many cohesive classes that are glued into an unreadable web. Too little delegation produces god objects: highly coupled from the inside, near-zero cohesion, impossible to test or extend because everything shares the class's internal state.

A pragmatic signal is the change-localization metric: a change should touch few classes, and the classes it touches should each have a single reason to exist. When a behavior change ripples across many collaborators, you either over-decomposed (split responsibilities that belonged together) or under-delegated (a caller knows too much about the graph). Balance is the design judgment; delegation is the tool you steer with.

## Q18: What is a facade, and how does it fit into object collaboration?

**A:** A facade is a single object that provides a simplified, unified entry point over a subsystem — a set of collaborating classes. The subsystem's objects continue to collaborate with each other as before, but external callers talk only to the facade; the facade routes requests to the right internal collaborators, often combining several calls into one convenient operation. It is delegation at the subsystem boundary.

The facade improves collaboration by shrinking the number of dependencies external clients must know about: they depend on one friendly contract instead of on a web of internals. That means the internal object graph can evolve freely as long as the facade's contract stands — you can split one collaborator into three, or replace an internal implementation, and no external caller changes. It also centralizes cross-cutting concerns (opening/committing work units, policy checks) at that boundary.

The trap is the anemic or god facade: a facade that merely forwards everything (pure indirection) or one that absorbs all logic (a god object wearing a facade costume). A good facade is opinionated — it offers a coordinated set of operations with real meaning and delegates the heavy lifting to specialists, keeping itself thin and keepers of policy, not of detail.

## Q19: How does delegation improve testability of a class?

**A:** Delegation turns behavior into collaborators behind interfaces, so a test can build the object under test with *fakes or stubs* instead of real networks, files, time, or databases. If `Checkout` delegates tax to an `ITaxCalculator`, a unit test injects a calculator with known answers and verifies the logic around it — call ordering, argument translation, result handling — without any real tax engine.

Because the delegating object only depends on the interface, tests read naturally as contracts: "given a fake collaborator that returns X, the delegator should return Y, and the collaborator should be called exactly once with Z." This is the mockist/classic testing debate — whether to assert on collaboration (spies that verify the messages sent) or on outcomes (classic state-based assertions) — but both hinge on delegation: without injectable collaborators there is no seam to either fake or spy.

The deeper win is that delegation localizes failure. If a whole system is a god object, any bug is reachable from anywhere and tests become integration tests by necessity. Split into collaborators, each object is testable in isolation and the hard parts are isolated behaviors you can verify exhaustively; the graph wiring itself is tested at the edges. Interfaces plus delegation are what make the seam between "unit" and "integration."

## Q20: What happens to delegation when the delegation chain becomes very long?

**A:** Long delegation chains degrade the collaboration: each hop hides the state and behavior involved, so reading the code no longer tells you where work actually happens; tracing a bug or a performance problem becomes a journey through many layers. Deciding whether a chain is bad is a judgment call about each hop adding value or just forwarding.

Chains are usually a symptom of *layering confusion*. Either every object delegates "up" to a god coordinator that actually does everything (the coordinator should host the logic), or objects forward messages they could make their own (delegators with nothing to delegate are forwarding, not delegating). Repair is to collapse layers: confluence the work into the object that owns the data, or into a well-named collaborator, and keep only the hops that add real behavior — translation, policy, coordination.

There are legitimate long chains — decorators, fluent builders, pipeline wrappers — where each link contributes one concern. The distinction question is whether you can remove any hop without losing meaning. If every link adds a distinct concern or a distinct contract guarantee, the chain is architecture; if links are pass-throughs and the object graph is just plumbing, the chain is a smell.

## Q21: What is the role of constructors (or construction time) in wiring collaborators together?

**A:** Construction is where delegation becomes concrete: an object's dependencies are selected and fixed at creation, either injected into the constructor or assembled by factories / a composition root. Constructor injection makes the collaboration explicit and stable for the object's lifetime — the object knows its collaborators, they are visible in signatures and tests, and there is no temporal ambiguity about when they were set.

Designing with delegation means designing the *wiring points* as carefully as the classes. The constructor signature is the object's real dependency list; a constructor that takes primitives and builds collaborators inside hides the graph and evades substitution, while a constructor that takes every dependency explicitly makes the graph visible and testable. Choosing defaults, factories, or a DI container is a decision about who owns assembly — but the collaborators themselves should come through interfaces.

The interview nuance is about lifecycle. Constructor injection suits stable collaborations (a service that always has a validator). For collaborators that vary per call or per state, construction may hold a factory or a strategy provider, and runtime selection decides the concrete delegate. The rule: fixed collaborations are wired at construction; varying collaborations are delegated through a strategy or factory interface.

## Q22: What are messages versus methods in the context of object collaboration?

**A:** In programming models like Smalltalk, objects communicate by *sending messages*; which *method* — which concrete code — runs in response is decided by the receiving object at runtime. The method is the implementation; the message is the request, defined by a name and arguments, resolved polymorphically. Modern statically-typed languages have the same idea under the hood: calling a virtual method is sending a message and letting dynamic dispatch choose the method.

This distinction frames delegation precisely: the delegator sends a message and does not control which method answers it; the receiver's type determines that. So developer intentions live in the messages (the interface), and implementers live in the methods (the classes). Changing a collaboration is therefore changing either the messages (the contract between objects) or the methods behind them (the implementations), and the two are independent — which is the entire point of programming to interfaces.

Interviews like this question because it tests whether you think about design in terms of interactions, not just classes. A collaboration diagram of messages tells you what the system does; a class diagram tells you what it is made of. Delegation is message-forwarding: when the receiver can't serve the message itself, it re-sends (delegates) to a collaborator that can.

## Q23: How do you document a collaboration between objects?

**A:** A collaboration is documented at three levels: interfaces (the message contracts), sequence or collaboration diagrams (the runtime interaction between participating objects), and a short narrative (what the interaction is for and which object is responsible at each step). Sequence diagrams are the canonical OO documentation for delegation: lifelines for objects, arrows for messages, activation bars showing when an object serves a call — exactly capturing who delegates to whom, and when.

The point of documenting is to make the *contracts* the readable artifact, not the internals. When you write "Checkout asks Order for a total, then asks TaxService to compute tax, then asks PaymentTerminal to authorize," you are documenting delegation as interactions. Adding pre/post conditions and exceptions pins the contracts that tests enforce, so documentation and tests align.

For interviews, the answer is about discipline, not tools. You should be able to draw the collaboration for any feature you built: the objects involved, the messages they exchange, the boundary where delegation crosses, and where invariants are enforced. If you cannot draw that diagram without it becoming a huge graph, the design has an over-splitting or under-delegation problem worth fixing.

## Q24: If an object delegates all of its work, how does it stay "in charge" of the invariants?

**A:** Delegation moves *work*, not *responsibility*. The delegating object is still the owner of its contract and invariants: it defines the conditions under which it calls delegates, checks results against the guarantees it must honor, and captures delegation failures as its own failures. A `Checkout` that delegates payment to `PaymentGateway` still enforces "you cannot confirm checkout without an authorized payment" even though it never touches a card.

The mechanisms are pre/post control. Before delegating, the object checks the precondition it promised (e.g., cart not empty, funds-capacity within policy); after delegating, it validates the outcome it requires (amount authorized equals amount owed, no partial state), and it keeps authority over compound invariants that span several delegates ("discount applied only if both membership and product constraints hold"). In DDD terms, the aggregate root owns its invariants while its parts may hold data and details, and it delegates piecework to services but confirms results before committing.

This is what separates delegation from mere relay. A relay forwards and forgets; a delegating owner forwards and *verifies*, keeping the public guarantees it stated. If an object is delegating but cannot state which invariants it personally guards, it has either delegated away its responsibilities (hollow shell, god collaborator) or it is a pass-through facade with no real contract of its own.

## Q25: What distinguishes an object that "delegates" from an object that "uses" another object?

**A:** "Using" is broad: an object may read from a collection, format a value, or call any utility — no particular pattern is implied. "Delegating" is a specific relationship where an object hands off a responsibility that is part of its *own contract* to a collaborator, keeping ownership of the overall obligation. The delegator's method and the delegate's method address the same responsibility; coming in through the delegator's public contract is the point.

Practically, you know you have delegation, not mere usage, when removing the collaborator would change what your object can do (its contract), not just how it does it. A `ReportGenerator` that uses `DateFormatter` is using a utility; a `ReportGenerator` that forwards its rendering to a `ReportRenderer` it can swap is delegating the responsibility of rendering. The difference shows in tests: delegation usually warrants faking the collaborator and asserting on messages; usage usually warrants calling the real utility.

The interview insight is that delegation is about *ownership transfer of a sub-role*. Your object announces "this part of my job is performed by X." If X is an internal implementation detail, it's composition plus forwarding; if X is a swappable party chosen to fulfill a stated role of your object, it's delegation in the design sense — and the interface behind that role is the seam you design and test.

## Q26: What is the relationship between delegation and the adapter pattern?

**A:** An adapter object exists to translate one contract into another: some client expects a target interface, some service provides different methods, and the adapter sits between them, forwarding client calls to the service in the form it understands. That forwarding is delegation: the adapter does not implement the target's semantics from scratch; it delegates to an existing implementation, adapting names, types, and granularity along the way.

So an adapter is a special kind of delegator whose sole purpose is *contract translation*, not coordination or policy. Where a general delegator may add validation or invariants, an adapter's value-add is the mapping itself: `round()` to `roundWithScale(2)`, a list-returning method to a single-value method, charset conversion between layers. The key is that delegation keeps the adapter honest — it should never re-implement the adapted logic, only redirect it.

The interview nuance is that adapters exist because the collaboration between two objects was constrained at construction time: the client and the service could not be wired directly because their contracts disagree. In a healthy system you design the shared contract up front so no adapter is needed; in an evolving system the adapter is the delegation-friendly way to bridge a new contract to an existing collaborator without touching either side.

## Q27: What is a "god object," and how does breaking it apart produce delegation?

**A:** A god object is a class that has absorbed too many responsibilities and knows too much — it holds most of the system's state, implements most of the behavior, and has a reference to everything. It breaks cohesion and coupling at once: behavior is spread across one class, and every other class depends on it, so any change to it ripples everywhere and testing it requires constructing the universe.

Breaking a god object up is the exercise of carving delegation boundaries. You ask, for each cluster of related state and behavior, "who is the natural owner?" and lift every such cluster into its own class with its own contract; the original object keeps only its identity and its coordinating role, delegating the extracted capabilities to the new collaborator objects. The god object becomes a small set of cooperating objects; the concrete collaborations are now visible as messages between them.

The usual suspects that signal a god object are names like `Utils`, `Manager`, `Everything`, or a class with enormous method-count and imports. The refactoring is iterative: extract a collaborator, move behavior, delegate, and repeat until the "central" class is genuinely small. The tell that you succeeded is that each extracted piece is independently testable, and the coordinator's tests use fakes for the parts.

## Q28: How do you model a two-way collaboration, where the first object must hear back from its delegate?

**A:** Two-way collaboration means the delegating object not only sends a request but also needs the result or a later notification — which requires callbacks, observer registration, or return-value flow. The simplest form is synchronous return: the delegator calls the delegate, receives a value, and continues; the "two-way" nature is just the call's result. When the response is asynchronous or reversal of control, the delegate calls back into an interface the first object provides.

The design decision is whether the callback is a *contract on the caller's side*. A `PaymentGateway` that must notify the checkout when payment settles should depend on an interface like `PaymentListener` that the checkout implements; the collaboration is then two interfaces — one each way — and both objects depend on abstractions, not on each other's classes. This mirrors the Observer pattern: the subject (gateway) delegates the reaction to observers, and observers register themselves.

The wisdom for interviews is that two-way collaborations multiply coupling if done with concrete types: A calls B and B calls A concretely is a circular dependency. The fix is to make at least one edge depend on an interface, and often to avoid the cycle entirely by routing through an intermediary (a mediator, an event bus) or by inverting one of the calls with a callback. Two-way collaboration is still delegation, just with a reverse channel that itself goes through a contract.

## Q29: When does delegation fail, and inheritance or template method becomes the better choice?

**A:** Delegation is awkward when the *skeleton* of an algorithm is fixed and only small steps vary — the classic case for the Template Method pattern. With delegation you would have to pass a strategy for each varying step, and the algorithm's flow lives in a coordinator that may not own the sequence at all; with a template method, the base class owns the skeleton (final, non-overridable) and subclasses fill in hooks.

Concrete example: `ReportBuilder` does open, iterate rows, format header, format cell, close. If the only variation is header formatting, delegation forces you to construct a whole builder-from-strategies; inheritance lets `PDFReportBuilder` override just `formatHeader`. The choice is about which dimension varies: delegation excels when the *whole strategy* varies and can be swapped, inheritance excels when the *steps of a fixed algorithm* vary.

There are strong reasons to prefer delegation even here — you can template-method with composition by injecting a "step provider" — but the honest answer is that the template method is the inheritance pattern that survives the "prefer composition" rule only because the shared skeleton is genuinely a contract, and the hooks are the only seams. Interviewers also probe the reverse: if the algorithm's structure *should* vary, template method is wrong and delegation/strategy is right.

## Q30: What is the difference between delegation, aggregation, and composition?

**A:** Composition is the strongest part-whole relationship: the part cannot exist without the whole, and the whole owns its lifetime (deleting the order deletes its lines). Aggregation is a weaker part-whole relationship: the part can outlive the whole and be shared (a player belongs to a team but exists independently). Delegation is a behavioral relationship: one object hands a responsibility to another — and it is orthogonal to the two structural ones.

In practice delegation rides on top of composition or aggregation. An order *composes* its lines and *delegates* line-total computation to them; a customer *aggregates* payment methods and *delegates* charging to the currently selected one. The structural relationships answer "who owns and who shares," and delegation answers "who does the work." Mixing the two questions is a common source of design confusion: two objects can have a pure association (neither owns) yet a rich delegation relationship.

The interview value is precision: when you say "delegate," say what the structural ownership is, because the wiring and lifetime differ. Composition-backed delegation can safely mutate parts; aggregation-backed delegation must copy-check or re-query. And pure delegation with no structural bond at all is just messaging through an interface — the lightest coupling of the trio.

## Q31: How do you prevent delegation from leaking the delegate's concrete types to callers?

**A:** The leak happens when the delegating object returns its delegate, its delegate's collections, or exceptions and values that only make sense in the delegate's vocabulary. The fix is that everything crossing the delegator's boundary is expressed in the delegator's own contract: a `NotificationsService` that delegates to `SMTPTransport` and `PushTransport` should surface "delivered", "failed with retry available", not `SmtpStatus` objects or raw protocol exceptions.

Concretely: return results of the delegator's semantics (value objects, booleans with policy meaning, its own exception hierarchy mapping transport failures onto business categories). Accept parameters in its own vocabulary and translate before forwarding. And never expose the delegate as a property — if a caller must hold the collaborator, it should receive the *interface* the delegator uses, not the concrete class.

The deeper rule is that a delegation boundary is a *contracted translation layer*. The delegate's world and the caller's world may have different models; the delegator is responsible for the mapping, and any type from the delegate's world that escapes means the mapping was half-done. In well-delegated designs, the only coupling a caller has is the delegator's interface — which is exactly why you can swap the delegate without affecting callers.

## Q32: What is "dependency direction," and why does delegation often invert it?

**A:** Dependency direction is the arrow of knowledge: A depends on B when A's code mentions B's type. Inheritance creates a dependency from the child to the parent (and to every specialization), so all behavior variations depend on the base. Delegation lets you point the arrows the other way: the high-level caller depends on the *collaborator's interface*, and the concrete collaborator implements (depends on) that interface — both face toward the abstraction, and the concrete detail depends on the abstraction, not vice versa.

This inversion is the Dependency Inversion Principle's engine and it is what "program to an interface" means in delegation. A `BillingService` depends on `IPaymentGateway`; `StripeGateway` and `PayPalGateway` depend on `IPaymentGateway`; nobody depends on a particular vendor. The delegating service is no longer hostage to concrete collaborators, and new collaborators plug in behind the same interface without touching the delegator.

Interviews treat dependency direction as the first thing to draw on a whiteboard. If every arrow points from a stable core to volatile details, the design tolerates change; if arrows run the other way, the core is recompiling when vendors change. Delegation is the mechanism to control arrows: introduce an interface where the delegator points outward, and make the concrete delegates point back to the shared contract.

## Q33: How does delegation relate to the "tell, don't ask" principle?

**A:** "Tell, don't ask" says objects should be commanded to do things, not interrogated for their data so another object can decide. Delegation and tell-don't-ask are the same instinct: when object A needs something involving B's data, instead of A pulling fields out of B and computing, A *tells* B to do the computation and B delegates to the specialist. The message is the command; the receiver holds the data and returns the answer.

The classic illustration: instead of `if (order.getLines().stream().anyMatch(l -> l.isOversized()))` and then a caller deciding, the caller calls `order.requiresSpecialHandling()` — the order computes the answer. The behavior stays where the data is, so the caller does not depend on the shape of lines, and the order can change its internal structure (or delegate the computation to a policy) without leaking. Tell-don't-ask is delegation applied to the ownership of logic.

The tension is that ask-style code is sometimes pragmatic — reading a value to compare, formatting, rendering — and pure tell-don't-ask fans produce pure controllers that decide everything. The mature interpretation: asking for *answers to questions* is fine; asking to *navigate and extract internals to do someone else's thinking* is the smell. Delegation resolves the smell by moving the thinking back to the object that knows.

## Q34: How do you decide between a thin wrapper and a fat delegator?

**A:** The decision is about whether the wrapper adds *only* forwarding or also *meaning*. A thin wrapper (pure adapter, pass-through decorator) is justified only when it is a genuine contract/translation seam — matching different interfaces, adding one cross-cutting concern like timing or retry. A fat delegator adds coordination, policy, validation, and owns invariants across its delegates, but must avoid absorbing logic that belongs to the collaborators.

The signal for simplifying a fat delegator is that it becomes (again) a god object by delegation: it forwards everywhere but also implements a little of everything, and its tests read like integration scripts over the whole graph. The repair is to push each piece of *policy* down to the object that owns the corresponding data or rule, keeping the delegator as a coordinator that routes between specialists, not one that re-implements them.

The pragmatic heuristic: name the wrapper with a verb or a role — `AuditedGateway`, `CachedTaxCalculator` are thin and honest; `OrderManager`, `PaymentCoordinator` are fat by nature and should be judged on how destributes the work. The ideal is thin where value equals a single concern, fat only where coordination is itself the responsibility.

## Q35: How do failure and exceptions flow through a delegation chain?

**A:** Failure should be caught, translated, and rethrown at the boundary where it becomes meaningful — usually at the delegator, not at every hop. Each delegator owns the contract it presents, so an exception from a delegate must be mapped to the delegator's vocabulary if the caller sees it. Raw low-level failures escaping a well-designed delegation chain are a leak: callers see `SocketTimeout` from a checkout operation instead of `PaymentFailed`.

The direction of responsibility is downward: every delegator in the chain is responsible for keeping its *outer contract* intact. A `LoadBalancedGateway` that delegates across providers catches per-provider failures and retries or fails over — it translates "provider down" into either success on another provider or a single coherent failure. A delegator that forwards exceptions unchanged everywhere is coupling every level to the bottom layer's failure vocabulary.

The senior nuances are *partial failure* and *compensation*. When a delegator coordinates several collaborators and one fails mid-way, its contract must define the cleanup (roll back, mark partial, compensate later) and its exception must tell the caller the true state. Delegation that ignores partial state, or that lets one partner's failure cascade into nonsensical states in others, is the classic distributed-terror inch in service design.

## Q36: How does the choice between delegation via interface and delegation via inheritance affect the open/closed principle?

**A:** The open/closed principle wants a class open for extension, closed for modification. Inheritance closes the class to modification only at the cost of multiplying subclasses and coupling every extension to the base type; delegation is the runtime version — you add a new collaborator behind an interface, and the delegator is "closed" (never edited) while extension is a new implementation of the interface wired in at assembly.

The concrete comparison: extending a reporting class by subclassing means a new class per variation, and every variation inherits the base's entire contract; extending by delegation means an `IChartRenderer` with a new implementation, and the existing report class is untouched. The delegation path is closed-for-modification in the exact OCP sense and open through the interface — which is why modern frameworks prefer strategy/decorator delegation over deep hierarchies.

The honest caveat is that naive delegation can hurt OCP too: if adding a new capability forces the delegator to add another collaborator and another method, the delegator itself is open-for-modification again. The mature answer is to design the delegation slots (the interfaces the delegator depends on) so that the set of capabilities is itself extensible — e.g., a plugin contract — making extension a wiring change rather than a code change in the delegator.

## Q37: What happens when the same object must play different collaboration roles in different contexts?

**A:** One object can hold several friendship contracts, each expressed by a different interface, and be wired differently per context. A `Customer` may implement `IPriceCalculator` for checkout, `IContactInfo` for communications, and nothing else for a renderer — each context depends only on the role it needs, and the customer object delegates the roles it cannot play to collaborators.

The danger is letting roles merge into one fat interface: every context then sees all capabilities, coupling happens on what roles share, and faking the object in tests drags in every role. The remedy is role interfaces — one per collaboration — and delegating work per role view. In practice the same business entity often holds data and plays roles through delegates: the `Customer` object for a pricing call may internally forward to a `PricingEngine` while the caller only sees `IPriceCalculator`.

Interviews treat this as the intersection of delegation and interface segregation. The pattern of "one object, many role interfaces, internal delegation per role" is the natural collaboration shape for rich entities: callers stay cheaply coupled, tests fake one role at a time, and new roles are added as new interfaces plus new delegation, without editing the other roles.

## Q38: What is the difference between object collaboration and data plumbing (DTOs)?

**A:** Data plumbing moves data — a value or a DTO passed whole from one place to another, often through anonymous layers, with no behavior attached and no responsibility explained. Object collaboration moves behavior through messages: objects exercise each other's capabilities, ask questions, command actions, and return results in terms of semantics. The distinction is verbs versus nouns: collaboration is about "tell the cart to add", plumbing is about "hand the cart across".

In practical codebases the boundary blurs: services receive DTOs from controllers and return DTOs, and inside the service the DTOs are transmuted into domain objects that *collaborate*. The design sin is letting plumbing swallow collaboration — passing the same DTO through four layers each mapping fields, with the actual logic nowhwere-adjacent and each layer's behavior just assigning fields. Delegation is the tool to push behavior back into owners so the DTO is only a transport boundary.

The interview answer should land on intent: DTOs exist at the edge of contexts (API, persistence, UI) to move values across a boundary without causing dependencies; collaboration exists inside a context where objects actually do work together. If you find your DTOs doing behavior or your domain objects being used as DTOs, you have collapsed the two and your "collaboration" is really plumbing in disguise.

## Q39: How does peer-to-peer collaboration differ from hierarchical client-server collaboration?

**A:** In a client-server (or more accurately, layered) style, one object requests and another responds, with a clear authority/order: the coordinator asks, the specialist answers, control returns. This is the dominant delegation shape — thin leaders delegating to specialists. Peer-to-peer collaboration means objects negotiate as equals: each may ask and each may respond, or the interaction is a conversation with multiple turns before an outcome is reached.

Hierarchical collaboration is legible and testable — the direction of dependency is clear and the transaction is easy to trace. Peer-to-peer conversation is rich and flexible but harder to reason about: cycles can creep in (A calls B, B calls A), responsibility for the outcome is diffuse, and animation of "who started it" becomes ambiguous. The design lever is deciding where authority for a decision lives, not just who calls whom.

A strong senior answer picks per situation: use hierarchical delegation for workflows where one object owns the outcome (aggregate roots coordinating their parts, orchestrators coordinating services); use peer conversation where negotiation is real (protocols, auction/negotiation, interactive wizards) — but wrap real peer protocols in a coordinator whose role is to run the conversation, so the "spaghetti between equals" stays inside a bounded ritual rather than sprawling across the graph.

## Q40: What is "double dispatch," and how does delegation relate to it?

**A:** Double dispatch selects behavior based on the runtime types of *two* objects — both the caller and the receiver — instead of just the receiver. Normal virtual dispatch chooses the method by the receiver's class; double dispatch needs to pick based on two dimensions, which single-method dispatch cannot express. The standard trick is "self-delegation": A calls `b.collide(this)`; B, knowing its own concrete type, responds not with the full logic but by calling back a type-specific method on A, e.g. `a.collideWithCircle(this)`; A now picks the implementation for both.

So double dispatch is implemented by *two rounds of delegation*: the first round selects the second object's handle, the second round hands type information back so the first object can finish the decision. Each round is a delegation: B delegates the collision outcome back to A, and A delegates to its type-specific handler. The pattern turns a two-dimensional dispatch table into method calls, at the cost of adding one method per involved type on each side.

Interviews use double dispatch to test whether you can break out of the "one virtual call" mental model and compose dispatch out of collaborations. The alert: double dispatch is usually a smell when it is used just to fake multiple inheritance or when the type axis should really be an interface choice — prefer delegation via strategy (one dimension is a strategy) when possible. It shines when genuinely two orthogonal behaviors must both be selected at runtime.

## Q41: What is the difference between a delegate and a strategy?

**A:** A strategy is a specific kind of delegate: an object encapsulating an *algorithm* selected at runtime and swapped to vary behavior (sorting strategy, pricing strategy). A delegate is the broader concept — any collaborator that receives forwarded responsibility, whether it is an algorithm (strategy), a coordinator, an adapter, or a state. When you say "strategy," you signal that the delegation is over an algorithm family; when you say "delegate," the handed-off work could be anything.

The behavioral implication is where variation is allowed: a strategy object is a replaceable piece of an algorithm that the owner treats like a plug; a state object may also *change the object's state-dependent behavior*, and a coordinator is a delegate that itself delegates. So the strategy pattern is strategy-as-delegation under a tighter contract — one method family, selected openly, used by a context that is blind to specifics.

For interviews, the vocabulary distinguishes the design intent: "delegate" invites the question "what exactly does it hand off and who owns the contract"; "strategy" implies "single replaceable algorithm selected at runtime." Both are instances of the deeper law — depend on abstractions, forward to collaborators, keep ownership of outcomes — and the pattern names are just labels for the kind of collaborator involved.

## Q42: How do you keep a delegation layer "thin" without it becoming useless, and "thick" without it becoming a god object?

**A:** Thinness is measured by whether each forwarded call adds a real concern; the layer is warranted if it translates a contract, adds a cross-cutting concern (logging, retry, auth), or names a subsystem as a role — and it becomes useless when it only pads indirection with no value. Thickness is measured by ownership: a delegator that coordinates several specialists and enforces compound invariants is legitimately thick, but adding more responsibilities *per responsibility* pushes you toward a god object that absorbs the specialties it should delegate.

The litmus test for both directions is the same: can you delete this layer and lose meaning? Thin-forwarding layers lose nothing — delete them. Thick-but-god layers lose everything — but refactor them, not the graph. The refactor carve is by "reason to change": give each sub-policy to the collaborator that owns the corresponding data, and keep the coordinator only for sequencing and cross-boundary invariants.

The interview nuance is that thickness should be *vertical* (coordination across many specialists, one decision level) rather than *horizontal* (each specialist also implemented inside). A good delegator is tall and narrow: it coordinates, but it is not the sum of its parts. As soon as its diagram includes the internals of its specialists, the layer is fat.

## Q43: How do you avoid the "traversal problem" — deep navigations through the object graph — when delegating?

**A:** The traversal problem is the outcome of a leaking graph: callers walk `order.getCustomer().getAddress().getCity()` because no collaborator answers that question directly. The delegation answer is to make each object answer questions about its own neighborhood: `order.getShippingCity()` internally navigates, or — better — delegates the answer to a collaborator that owns the knowledge, so no external caller ever walks through multiple owners.

The repair usually involves moving behavior down or across: asking the owner of the lowest degree to answer (tell-don't-ask), supplying a specialized collaboration object that owns in-neighborhood context (like the association-class idea), or publishing read-models/query objects. The goal is to flatten *observed* structure while keeping ownership — callers see a flat, deliberate contract even though internally the object graph delegates richly.

The senior distinction is whether navigation is a *query* (getting facts) or *reasoning* (using facts to decide) — the latter absolutely must move into an owner that delegates to a policy. And the corollary is the Law-of-Demeter tension: minimal-knowledge objects produce anemic queries if overdone; the mature design lets each object answer questions about its neighborhood and delegate cross-neighborhood questions to the boundary owner that can ask both sides.

## Q44: What is the interplay between object identity and delegation?

**A:** Identity gives an object a stable referencable existence across time, distinct from another object that may hold equal values. Delegation interacts with identity in two ways: the delegator holds the *identity* of its delegates (it refers to the same instances, not copies), and change to a delegate's identity-bearing state matters across all delegators that share it. An entity delegate (an aggregate) is identity-theme — sharing it across delegators shares its state and lifetime.

The design tension is value-sharing versus identity-sharing. If two delegators share an identity-bearing collaborator and one mutates it, the other's behavior changes — that's shared mutable state through delegation. The refactor is to delegate to *value* views (immutable snapshots, value objects as results) when you mean to share facts, and reserve identity delegation for single-ownership relationships (composition) so mutation is directed.

The interview angle: decide per edge whether the delegation is to an identity (shared, transitively coupled, needs ownership rules) or to a value (snapshot, safe to share, immutable). Most collaboration bugs are identity leaks: a value being passed as an identity hook, or a shared identity being mutated where a snapshot was expected. Naming the delegation edge's identity vs value nature clarifies the contract and the test story.

## Q45: How do you design the "public protocol" of a delegation boundary?

**A:** The public protocol is the set of messages a delegator exposes to its callers: the names, arguments, result types, exceptions, and ordering rules that define its contract. Designing it means deciding *which* capabilities of the collaborators are surfaced — ideally exactly the responsibilities the delegator truly owns — and translating each into the delegator's vocabulary so the collaboration reads as one coherent service.

The starting discipline is to design outward-first: what does the caller need to express, what invariants must hold, what does "done" mean? Only then map each protocol operation to the internal delegation (one delegate, several, or a composite). The protocol should not mirror the collaborator's methods one-for-one unless translation is the sole purpose (adapter); otherwise the delegator should compose or carve capabilities. Keep method counts small, names in the caller's language, and pre/post conditions visible.

Interviews look for the consequences of a good protocol: callers are stable even when internal delegates change, tests exercise the protocol (not the internals), and the evolution of the collaboration is confined to internals. A protocol that changes with every internal optimization is an indicator that the delegator does not truly own the boundary — it is a pass-through wearing the identity of its delegates.

## Q46: How does cancellation or deadlock creep into delegation chains called in a loop or recursively?

**A:** Delegation is a directed flow of synchronous calls, so loops in that flow are cycles: A delegates to B, B delegates to A; the graph of references is cyclic, and a request that follows the edges never terminates unless the objects track progress. The common trigger is collaborating entities each delegating back to the other for the "answer" of a compound decision — data access both ways, e.g., order and customer asking each other for totals.

The design rule for delegation is that the *object graph* should be nearly acyclic even when the language allows cycles: define the edge direction by ownership or by dependency (aggregate owns parts; the part may hold a back-reference through an interface, never for delegation that recurses). A preventive rule is "delegate forward": a request should move toward the owner of the final answer; the moment a request moves back to someone who already received it, you have a cycle.

The mature solution is to lift the two-way question into a coordinator that owns both sides adding no recursion: an association object or a service computes the compound answer and both entities delegate *to it* — each now asks the coordinator rather than each other. And for genuinely recursive collaboration (tree walks, composite parts), the recursion must be bounded by the structure itself, with explicit depth limits — never a loop that re-visits the same node.

## Q47: How does delegation interact with the singleton problem in system design?

**A:** Singletons are a common way to make a collaborator globally reachable — but they fight delegation: delegation's power is *substitution* (inject a real or a fake collaborator per context), and a singleton bakes the concrete instance into the whole graph, so there is no seam to substitute or to vary behavior per context. The classic refactoring is: keep one *instance* of the underlying service, but introduce it into each delegator via constructor or factory, not via global access.

The deeper collision is collaboration vs global state. A singleton collaborator can be held by many delegators, so shared mutable state across all of them returns (the same shared-state problem in graph terms). When the singleton is stateless or a rock-steady service, that is acceptable; when it carries state or many consumers need different fakes, global access destroys the ability to test collaboration edges individually.

Interviews look for whether you distinguish "one instance at construction" (a composition root owning one instance, injected everywhere) from "global access" (everyone reaches it directly). The former keeps delegation intact: objects still talk through interfaces, loops and order stay visible, and the graph is wired once. The latter creates invisible coupling between delegators that share the global — a river of unsaid dependencies.

## Q48: How do you keep a "session" or "context" from becoming a god object while still sharing state across collaborators?

**A:** A context object — a session, a request context, a transaction context — carries shared state across many collaborators, which is exactly what delegation needs (the request ID, the current tenant, the open transaction). The god-object trap appears when the context grows into the place where logic and policy land too, or when collaborators pass the context around as a hairball that everything reaches into through free-floating getters.

The discipline is to give the context a *bounded, role-shaped API*: it exposes exactly what its collaborators need as typed views (a `IRequestScope`, `ITransactionScope`), and collaborators depend on those narrow views, not on the fat context. The context itself should delegate the actual capability (transaction handling, tenant resolution) to specialists rather than implement them; it is a *registry and boundary*, not a workshop.

Tests and evolution follow: a narrow-view context is fakeable per role, and the context can change its internals (move transaction work out, add a new scope) without editing every collaborator. The senior mow is naming the context's roles explicitly and stopping the growth checklist-test — if a new requirement tries to add state to the context but no existing role needs it, the requirement either needs a new scope or its own coordinator, not an expanded context.

## Q49: How does delegation relate to the command pattern?

**A:** The command pattern encapsulates a request as an object: the request receives its action and its receiver, and an invoker triggers it generically. The command *delegates* the actual execution to the receiver it was built around; the invoker delegates to the command. So command is a two-hop delegation: invoker → command → receiver, where the command is a delayed, stored, undoable predicate of the collaboration.

The value for collaboration design is that commands turn a *materialized intent* into a message that can be queued, logged, undone, and retried. Because command objects depend on an interface (the receiver behind an abstract execute), they preserve the delegation benefits even though the caller and the receiver never meet directly — the coupling is via the command's contract, which the commands and receivers honor through interfaces.

Interviews use commands to test whether you understand *when* delegation crosses a boundary in time or space. A direct call is immediate; a command defers who, when, and how the work is done, and reopens it for cross-cutting behavior (transaction, audit, retry) at the invoker. Treating the command as a first-class collaborator (rather than a closure) reaps undo/queue/macro and traces — the handoff is explicit and the receiver is swappable.

## Q50: How do you verify that a delegation-based design is well-structured (metrics/smells)?

**A:** The quantitative checks are: coupling counts (dependencies per class, message-passing not field-touching), cohesion metrics like LCOM (high cohesion in each class), depth of the object graph, and the number of delegators per responsibility. But the strongest verification is behavior-oriented: for every responsibility, the code that handles it is findable in exactly one place, and the delegators are objects that document their roles, and their tests read as contracts.

The smell list is short and sharp: feature envy (a method slogs through another object's internals), god classes, long parameter lists that smell like a missing collaborator, chains of getters, duplicated delegation logic (the same duck-tape wiring in several places), and "message to self" chains (an object passing results through several of its own collaborators in sequence for one job). Each is a sign to move a responsibility into a collaborator or to collapse layers.

The interpret exercise for a design: write the story of one feature as an object dialogue; if the story needs a class that does everything ("then the manager does X, Y, Z"), the delegation boundaries were drawn in the wrong place; if the story is a clean relay of "ask the owner, who asks the specialist, who answers", the structure delegates well. Good signage is subjective but measurable: tests per object with fakes for others, plus a compiler that keeps each edge typed.

## Q51: Is the Law of Demeter about message chains or about hidden structure?

**A:** The letter of the law limits message chains; the spirit is about *structure leakage* — a caller depending on the shape of the object graph (that `order.getCustomer()` returns something with a `getAddress()` that has a `getCity()`). A chain is just the visible symptom of a design where facts live deeper than the object that answers the question, so callers must know the graph to ask anything.

The structural reading changes the fix. You do not merely break a chain into `order.getCustomer().getAddress().getCity()` into three lines; you move the question to an owner — `order.getShippingCity()` — or you delegate the answer to a collaboration object that holds the neighborhood knowledge. The question "who owns the knowledge" is one of delegation; the law is the detective that points at wrongly-placed knowledge.

Senior nuance: the law is violated most by *mutating* chains (reach in and change), far more than by reading chains — though both leak. The design outcome is that each object answers questions about its own neighborhood, and cross-neighborhood questions get answered by whoever legitimately owns the edge. Then the graph shape is an implementation detail, not public contract.

## Q52: When is a long delegation chain actually justified?

**A:** A long chain is justified when *every hop adds real behavior* — each link is a distinct concern or a distinct contract translation, and removing any link collapses two different responsibilities. Decorators are the archetype: `CompressingAuthRetryingTimeoutClient` where each wrapper adds exactly one cross-cutting concern and preserves the interface; fluent construction chains (`builder.step().step().step()`) where each node returns the right "next step" view of the pipeline.

The test is whether the chain is a *reduction* of design: can you name what each link adds, does the chain direction represent ownership or a pipeline (not a ladder of getters), and does every element subscribe to the same contract? A wrapper chain delegates forward and returns up; a getter ladder leaks structure and does nothing. Chains that carry state progressively (a template of a rendering pipeline) are architecture; chains that merely relay (A asks B to ask C to ask D) are plumbing.

The interview point is that "long" is not the smell — "opaque and behaviorless" is. You should be able to walk the chain out loud, naming each link's responsibility, and demonstrate that the chain is collapsible only if it is genuinely meaningless forwarding. When true, keep; when a hop is a pass-through, it is dead weight.

## Q53: How do preconditions and postconditions flow across a delegation boundary?

**A:** A delegator's contract includes its own pre/post conditions, and the delegate's contract is a *stronger* or *compatible* refinement within the delegator's control flow. Before delegating, the delegator verifies its own precondition (and derives the delegate's precondition from its input — e.g., normalizing cart before asking the total). After delegating, it checks the delegate's postcondition against *its own* promised outcome, mapping violations into the boundary's vocabulary before signaling the caller.

The flow of contracts is therefore a sandwich: outer precondition enforced, inner precondition satisfied by translation, inner postcondition verified against outer postcondition, outer postcondition restored. When a chain of delegates exists, each link faithfully converts the incoming guarantees into the outgoing ones; the invariant-swapping is what makes delegation composable — you can push values down and trust results up.

The classic failure is *contract weakening in the middle*: a delegate that satisfies its own signature but silently violates an expectation upstream (returns partial results, mutates without notice), so the outer postcondition breaks even though each class "looks correct." Contracts at the delegator are what you verify in tests: inject fakes that mutate the invariants and assert the delegator either repairs or reports — ensuring the sandwich holds.

## Q54: In testing a delegation-based design, do you assert on messages sent or on final state?

**A:** That is the mockist versus classic-testing debate, and the honest answer is "both, at different layers." Message assertions (spies verifying "the delegator handed the converted argument to collaborator X exactly once") are the right device at the *delegation seam*: they prove the hand-off logic — which is exactly what a delegator adds. State/outcome assertions are right for the object's *contract*: given inputs and fakes, the object's external behavior should be observable without knowing who it called.

The guideline is to use mocks where the interaction *is* the specification (an object that exists to wire and translate), and use state assertions where the object owns a real outcome (use the fake's results, then assert on the delegator's output). Over-mocking a pure computation, or under-mocking an orchestration boundary, are the two failure modes; the first makes tests brittle to implementation, the second makes tests depend on the whole graph.

Interviews like this question because it tests your testing philosophy beyond library choices. The deep principle: test each object against *its own contract*, and let fakes stand in for collaborators' contracts. The delegation edges are then tested as contracts themselves — message-orientation at edges, outcome-orientation at owners — and the graph's wiring is covered by a few integration tests, not by forcing every unit test to know the internals.

## Q55: How does delegation work inside the Composite pattern?

**A:** A composite lets a group of objects be treated like a single object. The composite *delegates* each operation to its children and often aggregates their results: `total()`, `render()`, `accept(visitor)` are forwarded to every child, and the composite synthesizes a single answer. Leaf objects implement the same contract directly; the composite is a collaborator that forwards — a delegating object whose delegate-set is its children.

The delegation contract is recursive and uniform: because both composites and leaves share the interface, any caller can delegate the same message to either, and the composite itself delegates deeper. This is delegation at the cost of the interface being shared at every level — the operations must make sense at both leaf and group granularity. A well-designed composite keeps group-specific behavior (count, structure) *inside* the composite rather than leaking unique methods.

The interview nuance is where delegation ends and composition-look-alike begins: a composite is fake-uniform if children have rich group-only behavior that the interface cannot express. The mature seam is to keep the shared contract as the message channel and, where needed, let composite's own protocol be a separate role interface so the delegation is explicit about granularity.

## Q56: What is the difference between the Chain of Responsibility and delegation?

**A:** Chain of Responsibility passes a request along a chain, each link deciding to handle it, pass it on, or both — the ultimate handler is not known in advance; the request flows until someone claims it. Delegation is a deliberate, immediate hand-off: the delegator knows (or has a strategy deciding) who will do the work, and it forwards directly. The chain is "send to the first who can" — indirect; delegation is "send to the one I choose" — direct.

Structurally the chain is a linked sequence of objects all implementing the same handle message; each link is itself a delegator that, when it cannot or must not handle, forwards to the next. So the chain is a *runtime-determined delegation*: responsibility is resolved by the chain's order and each link's decision rather than by the caller's choice. Both obey the same contract-oriented ideal — nobody knows the concrete handler — but the semantics of who chooses differ.

The design implications differ too: chains (responsibility) are good for fallbacks, pipeline of dismissal, and tiered processing where any level may claim; direct delegation is better when the delegator should own the choice (strategy-like). The interview test is whether you select the resolution strategy intentionally: a chain hides the choice until runtime, delegation makes the choice either 1:1 or explicitly policy-based. Dangerous hybrids mix the two — a caller that “sends to a chain” but expects a specific handler.

## Q57: How do you count and manage coupling in delegation-heavy systems?

**A:** Coupling has two axes in a delegation system: *dependencies* (the types each class names in its signatures) and *topology* (the edges of the object graph — who holds a reference to whom, and how messages flow across those edges). A good metric starts with dependency counts (fan-in/fan-out per class), and the pattern of edges is as telling as the count: a graph that is deep-but-thin has many hops but narrow contracts; a graph that is wide-but-shallow keeps delegation cheap and each edge's contract small.

The pragmatic management is to keep the *number of edges incident to any class* bounded (a class depending on five collaborators is manageable, fifty is a design) and to make each edge's contract small (see interface segregation). Cyclic edges are the biggest coupling amplifier — a cycle means every class in it effectively depends on every other, so that partial-order analysis breaks. Eliminating cycles (usually by adding an interface or a coordinator) restores Directed Acyclic Graph reasoning: change hits a bounded downstream set.

The interview-level understanding: delegation converts *implementation coupling* (one class knowing how another works) into *contract coupling* (both facing a shared interface). Contract coupling is cheaper than implementation coupling, so a system can have many delegation edges yet low coupling — as long as the edges are interface-typed, acyclic, and the contracts define narrow demands. Counting depends on your classes, not your edges.

## Q58: How does delegation protect or challenge an aggregate's invariants?

**A:** In DDD an aggregate is a cluster of objects with one root guarding the invariants over the whole cluster. Internal parts may delegate piece-meal work to each other, but the *root* must own the compound invariants — it is the object that any state-changing message must pass through — and delegation inside the aggregate is an implementation detail that must never expose partial state to the outside.

The risk is "delegation as bypass": if a child object inside the aggregate is reachable from outside (a leaked part) or can mutate itself without the root knowing, an invariant is implemented nowhere — the graph delegated the work but misplaced the custody. The design answer is that the root invokes the delegates *and verifies the result against the invariant* before any state is committed outward; equivalently the aggregate can delegate the calculation of a rule to a service as long as the decision is still the root's (the rule's *policy* may live in a service, the *ownership* of the decision stays at the root).

Interviewers love to probe a version that contradicts the simplification: "the root delegates validation to a validator — is the root still owning the invariant?" Yes, if the root enforces "changes go through me with the validated outcome", i.e. the validator is a collaborating policy that the root consults, never a bypass. Where delegation breaks, it is because policy or ownership went to the wrong level.

## Q59: How do you distinguish a stateless collaborator (service) from a stateful one (entity) in delegation?

**A:** A stateless collaborator (a service, a policy, a calculator) holds no per-request state: it computes or does work using its inputs, and one shared instance can serve many delegators. A stateful collaborator is an entity or aggregate that *owns* identity-bearing state, and delegators must treat it as a shared, mutable object that changes behavior based on its current state.

The design consequences follow. Stateless collaborators are trivially shareable, trivially substitutable, and can be singletons-by-wiring (one instance injected everywhere) without risk. Stateful collaborators need ownership rules: exactly one delegator should own mutation (or explicit co-ownership with protocols), and snapping or versioning matters because state crosses delegator boundaries. Mixing them is a bug: a service that accumulates request state (a "service with a cursor") is an entity pretending to be a policy.

The delegation principle at stake: *where do you put which state?* Statelessness is cheap to share; identity-bearing state must have a home and an owner. A well-delegated system places logic in services and state in entities/aggregates, and each delegation edge either computes-from-inputs (service) or reads-and-mutates-own state (entity). The decision is per-edge, and getting it wrong leaks shared mutation into "pure" collaborations.

## Q60: How do asynchronous or eventual collaborations differ from synchronous delegation?

**A:** Synchronous delegation is a blocking call: the delegator waits, gets a result or an exception, and continues; the contract is a request-response with immediate, typed outcomes. Asynchronous delegation returns control immediately — the delegator may get a future/handle or the delegate later calls a callback, publishes an event, or resolves a promise — so the delegation edge is *two protocol turns*: one to send, another (possibly much later) to deliver a result.

The design differences cascade. Synchronous contracts are easy to reason about (pre/post in the same stack), easy to trace, easy to test; asynchronous contracts need time-outs, ordering, re-delivery, and idempotency vocabulary, and the "who is responsible while the work is pending" question must be named. Database transactions, exceptions, and promises reshape: async delegators often frame work as *requests*, and the delegate delivers *completion published* rather than a return value.

The senior wiring is the boundary choice: within a consistency boundary (a transaction, an aggregate operation), prefer synchronous delegation; across the boundary (a service call that can be queued, a guest-worker), prefer asynchronous delegation with explicit state machine (pending/succeeded/failed/timeout) so the collaborate state is legible. The mistake is to make an *internal* collaboration async (obscures it, complicates invariants) or an *external* one sync without a strategy (blocks, couples schedules).

## Q61: What does circular delegation do to a design, and how do you break the cycle?

**A:** Circular delegation — A delegates something to B, whose answer requires delegating back to A — turns a method call into a mutually recursive loop that risks non-termination or hidden evaluation-order dependencies, and it makes the object graph a cycle, so reasoning "who provides the fact" becomes ambiguous: each object says "ask the other." It usually appears when a compound decision touches facts of two objects and neither owns the whole decision.

The break is to introduce a third party that owns the compound decision: an association/service/coordinator object that holds both sides (or an interface to both) and computes the combined answer, with each entity then delegating *to it* rather than to each other. Because the third party itself depends on both contract (not concretely), the dependency arrows and the call flow may reorder cleanly — the collaboration becomes two one-way delegations through the shared owner, no cycle.

The design lesson beyond the literal fix: cycles in the *object graph* are often symptoms of responsibility-split mistakes — a fact that belongs to one object lives in another, so both must delegate back and forth to recompute it. Moving data closer to the computation, or moving the computation into the owner (a policy it delegates to), dissolves the need for the round-trip. Cycles are the smell to hunt for when collaboration logic falters.

## Q62: How do you model a negotiation protocol (several parties) using delegation?

**A:** A negotiation involves several parties that exchange proposals and reach a settlement — a multi-turn collaboration. Direct party-to-party delegation between all of them would be a dense, cyclic graph; the design move is a *coordinator* that owns the protocol: parties delegate their proposals to the coordinator, the coordinator applies the rule (e.g., the combining formula, the acceptance criteria), and may delegate valuation or decision sub-work to specialists (a pricing engine, a validation service).

Each party is then a contract-holder (it publishes bids and accepts results), the coordinator is the protocol owner (it orders turns, checks invariants like "no double-claims"), and the specialists are pure policy delegates. The negotiation steps read as delegated messages, and the graph stays clean: every edge is party→coordinator→specialist; no party ever reaches into another party's internals.

The interview takeaway is the classic delegation tension: a protocol with many parties tends to sprout a “god coordinator” that absorbs all the logic. The guard is that the coordinator's job is *sequencing and invariants*, while the rules (pricing formula, valuation, scoring) delegate to swappable policies — so the coordinator stays slim, and changes to a rule touch a specialist, not the whole negotiation.

## Q63: How do you set up delegation so that an object can retry, re-queue, or compensate when a delegate fails?

**A:** The delegator's contract must include failure semantics: what happens when the delegate fails partway, whether the operation is re-tryable, and what compensates the partial effects. The usual shape: the delegator wraps the delegate call in a strategic boundary (a retry policy with bounded attempts and backoff for transient errors, a circuit breaker, an outbox/queue when a durable retry path is needed), and after repeated failure it marks partial application and runs a compensating step, or reports precisely what was not done.

Retries and compensation depend on the *delegate's* idempotency contract: a delegate that can be safely repeated (or provides operation keys to de-duplicate) enables retry; a delegate with side effects needs compensation keys rather than blind repeats. The delegator must therefore negotiate idempotency with the delegate at design time — one more contract on the collaboration — and its tests must assert "given a failure on second attempt, state is X, no double-application."

The senior point: retry/compensation is part of the *boundary design* of each delegation, not a bolt-on. Where the delegation is pure (computation), retry is free and failure is just an exception mapping. Where it touches irreversible state, the delegator owns a small state machine (attempted/failed/compensated) and delegates the compensation steps themselves — because "the delegate did the work, then we undid ours" is a two-ended collaboration, not a single call.

## Q64: How do you decide when a piece of work should move from a delegate up into the delegator?

**A:** Move work up when the delegate is consistently used only by this delegator, when the delegate's behavior is trivial, or when the delegation has become a pure pass-through where the delegator adds no contract value — a hop that merely forwards a compute that its own caller could do just as well. The goal is to remove indirection that adds cost (reading, tracing, testing a wrapper) without adding seam value (substitution, translation, coordination).

The counter-sign is when the work is genuinely shared or genuinely varying: two delegators using one delegate, or one delegator wanting to swap implementations at runtime, keeps the delegate as a seam and an owner — keep it. The decision rule is about *variation and reuse distance*: if the behavior would change in different contexts or would be reused with different semantics, a delegate is the right home; if the behavior is single-use, single-context, and simple, fuse it.

The pros test for the interview: name the cost per delegation (indirection, discoverability, testing surface). If the fuse loses none of those benefits but the object becomes clearer, fusing is the right refactor. The danger is a “matryoshka”: a thin delegator wrapping a delegate that holds all the logic — then you are just paying for the layer. Move the logic into the delegator (or into a better-named owner) and delete the layer.

## Q65: What is a "leaky abstraction," and how does delegation create or prevent it?

**A:** A leaky abstraction lets the interface between layers reveal the implementation beneath — callers can observe the underlying delegate's special behavior, types, and failure modes through the delegator's otherwise-clean boundary. Delegation creates leaks when the delegator forwards without translating: return types from the delegate's world, delegate-specific exceptions, delegation-internal partial states — the caller now knows "behind this interface lives a filesystem" or "behind this wrapper is a network."

Prevention is the translating boundary: the delegator converts the delegate's vocabulary into its own (its own exceptions and result semantics), hides the delegate as implementation, and exposes only its own contract, including deliberate failure information. Where translation is impossible due to genuine constraints (performance, semantics like "this is literally a socket"), the design should *admit the constraint honestly* — an exposed latency or failure mode is better than a pretend-costeless interface that breaks harder later.

The mature view is that hiding everything behind delegation is not always best: an interface can be deliberately honest about the collaboration's cost ("you are about to cross a network"). The leak to prevent is *hinging behavior on randomness* — callers tuned to the delegate's quirks, or the delegate's behavior changing silently under the wrapper — while intended, documented exposure of the delegate's nature is a legitimate contract choice.

## Q66: What is the role of open/closed and single-responsibility principles inside a delegation design?

**A:** Single-responsibility tells you *how to carve*: each object owns one reason to change, and delegation is how you carve — each responsibility becomes a collaborator with its own reason to change. Open/closed tells you *how to nest*: extend behavior by adding collaborators behind interfaces rather than editing the delegator. Together they make the delegation graph the design's spine: responsibilities live in owned specialists, and extension points are the interfaces between them.

The two principles reinforce each other: SRP says a delegator that both coordinates and implements is wrong; it should delegate each computation it doesn't own, and keep the coordination as its single reason. OCP says the coordinates should route to interfaces, so a new implementation of a collaborator is a new class wired in, not a change to the delegator or the other collaborators. Delegation is the mechanical implementation of both principles applied to object communication.

The interview story is that these principles are where the "whys" and "hows" of the collaboration meet: why this weight (SRP gives the reason-to-change justification for each edge) and how to extend (OCP gives the interface rule for each edge). A delegation graph that violates both is a cartoon of a god object with brittle seams; one that respects them is a constellation where each object changes for a single reason and new behavior arrives as new delegate.

## Q67: When is it better to use a mediator instead of direct delegation?

**A:** A mediator centralizes the interactions of a set of objects so they stop talking directly to each other — one object (the mediator) handles the flow between all of them. Direct delegation is better when interactions are few, pairwise, and the delegator+delegate each have clear ownership; the mediator wins when the set is many, the interactions are numerous and varied, and direct collaboration would spread the wiring and the state-changes across many edges.

The difference is who controls the orchestration. With delegation, control is distributed: each delegator knows whom it talks to, and the object graph shows the collaboration edges plainly. With a mediator, control is centralized: the objects become colleagues (their links collapse to one edge: to the mediator) and the collaboration logic lives in one protocol owner, at the cost of a possible god-mediator if it also implements the specialist logic.

The senior rule: keep direct delegation for hierarchies (an aggregate to its parts, a service to its helpers), use a mediator when the objects are peers whose mutual knowledge must be hidden and when interactions change frequently (a form with many interacting fields, a chat room). And the same carve applies to chains vs mediators: when "who talks to whom" is dynamic and must change easily, centralize; when it is stable and meaning is per-edge, delegate directly.

## Q68: How do you keep a "renderer"/"view" in sync with domain state without breaking delegation?

**A:** The view should be a *read model* that does not hold the domain's authoritative state: it delegates questions to the domain (queries), and the domain owns the state and the invariants. Synchronization is then a decision about when the view re-queries (after commands, on events, on observable change) — via push (the domain emits, the view re-renders) or pull (the view re-delegates at render time). The view delegate pattern is: view → (ask domain) → render, never view → mutate domain directly.

The change-sync mechanism is the interesting part of the collaboration. A push model delegates notification: the domain (or its change-source) notifies registered views through a narrow interface, and views re-query as needed. A pull model is stateless and dry: the view always reads fresh; the sync cost is answering the occasional duplicate query. The design seams to check: the view depends on a query interface, not on domain internals, so a changed domain shape only changes the query layer.

The interview angle is the warning against "god-view": a view that both renders and performs domain music breaks delegation — the view's only responsibility is presentation; everything else delegates into the domain layer. Where the view needs derived state, that derivation should live in a query or a selection object that the view delegates to, keeping the view as a thin delegate of presentation decisions.

## Q69: How do the concepts of "self-delegation" and "self-usage" interact, and when do they be danger?

**A:** Self-usage (self-delegation) is when an object's methods call each other through its own interface — e.g., `complete()` calls `validate()` then `commit()` internally, so a single entry point composes the object's own protocol. Properly used, it keeps the public contract as the only path into behavior, so invariants can be enforced at the boundary and behavior composition is internal and legible (making `complete()` a one-stop guaranteed path).

The danger arises when self-delegation becomes *circular self-delegation*: an object's method insists on the public path but the public path itself needs that method, and a call re-enters itself (e.g., `setTotal()` calls `recalculate()` which calls `setTotal()`), or when subclasses override methods that the parent's self-delegated call relies on — a classic fragile-base-class surprise. The guard is to separate the internal *primitive* (the actual computation, package-private, no self-redirect) from the public *composed* method that calls the primitives.

The senior distinction: composing your own interface internally is a design pattern (Template Method, Facade-by-self), but it transfers a dependency on your own dynamic behavior — so queuing, refactoring, and subclass overrides must be accounted for. The priority is clear when you realize that self-delegation *names the seams you already have*: if the internal steps are real behaviors worth reusing, extract them as private primitives and compose — the delegation story is unchanged, only the edges became internal.

## Q70: How do you keep collaboration logic testable when it is spread across many delegators?

**A:** The rule is to test each delegator against *its own contract with faked collaborators*, then assemble the graph once at the integration tier, and keep an acceptance test per feature that exercises the real wiring of the interesting collaborations. The unit tier is where delegation edges are refined; the integration tier is where the graph is verified to be wired (right collaborator injected, right order called, edge cases at the boundaries compose).

The friction usually comes from edges that are hard to fake: delegates that are singletons, statics, or woven-in factories. Moving those to injection seams (constructor, factory, or a seam interface) makes the collaboration edge testable and the delegation contract explicit. If an edge is genuinely un-fakeable, that is a design signal — the "collaborator" is really an environment, and it should be more honestly named and delimited rather than a fake-able service.

The interview highlight is the *cost of contract-testing*: the most valuable tests are at the boundaries where a delegator translates or guards — pointer that a fragile middle (a delegator that passes through without translating) is exactly where a mis-wire hides, and that the same delegation edge (the wrap of a real collaborator in a real caller) deserves an integration test so the contract is exercised with the true object.

## Q71: When does "delegation to a delegate that delegates to a delegate..." become an architecture smell?

**A:** The smell is when the chain has no *node with actual weight*: each delegator forwards without real coordination, translation, or policy, so the graph is a long chain of verbose plumbing — a "thin-forever" chain. The symptom is that removing two or three hops changes nothing, and tests for the whole chain read identically for every link.

The architecture view is that each level of the system should have a *purpose*: presentation → application → domain → infrastructure. If a chain crosses levels with no level-boundary behavior (any layer merely relaying the previous one's message), either a level is missing its logic (it should be hosting policy) or a level is empty (it should be deleted). The healthy chain is a series of *translations* — each hop maps the previous level's concept closer to the target — not a series of repeated same-type forwards.

The test to apply: name each link's *added contract*. "The repository decorates with retry; the service maps domain objects to commands; the controller translates HTTP to service calls" — that chain is architecture, each link real. "The service calls a coordinator that calls a manager that calls the repository" — the middle two add nothing; collapse them or give them behavior. The senior answer names the smell as *indirection without a seam* and the cure as fusing or re-carving until the set of hops expresses the levels of the design.

## Q72: How do "feature envy" and "inappropriate intimacy" show up as delegation problems?

**A:** Feature envy is a method that spends most of its time accessing another object's data to compute something that should live in that other object — the delegation equivalent is a delegator that reads the delegate's state and decides, instead of telling the delegate to decide (tell-don't-ask violated). Inappropriate intimacy is two objects knowing each other's internals a bit too well, usually because delegation edges are concrete-typed and reach deep, so each depends on the other's shape.

Both are fixed by moving the computation into the object that owns the data: the delegator keeps a coordinator role and the decision becomes a message the delegate handles (possibly delegating further to a policy). The delegator that reads-and-decides for the delegate is missing a delegator that commands-and-receives; adding the interface for the decision removes the envy. Intimacy dissolves when the deep edge is replaced by a narrow interface both honor.

The interview nuance: feature envy is not the same as a delegator that simply never uses the delegate's data — the smell is about the imbalance between the delegator's coupling to another's state and its own. A delegator that needs three fields from the delegate to make a judgment is telling you the judgment belongs to the delegate. Design the judgment message, then the delegation is the collaboration — the envy disappears and the object graph simplifies.

## Q73: How do you combine delegation with value objects versus entity references in an object graph?

**A:** Delegating to one entity type with identity sharing means shared mutation (coupled state, needs ownership); delegating to a value object means handing over an immutable, copyable fact that the delegate cannot mutate on the recipient's behalf. When you delegate a *fact* (a price, an address, a date range), the fact should be a value copied across the collaboration; when you delegate *ownership* or *identity* (a part of the aggregate, a customer), the collaboration edges carry reference semantics.

The design rule follows: choose the delegate based on the kind of work. If the work is computation over facts, pass facts as values (or delegate to a pure function over values), keeping state immutable and the collaboration safe to share. If the work is lifecycle or mutation over identity, the delegation edge implies an ownership or transaction plan — who may change and who must be notified — so identity edges are the ones that need contracts (aggregate boundaries, transactional scopes).

Interviews like this blend of two concepts: they probe that value-vs-reference is not a mechanical choice but a *semantics decision* about the collaboration. Delegate with values when you want to share results safely; delegate with references when identity must flow (because the delegate must mutate or the caller must observe the same object); and place ownership rules and snapshots around the identity edges only.

## Q74: What does the "principle of least knowledge" really protect in a delegation graph?

**A:** It protects *structural coupling* — the dependence of a caller on the shape of the object graph. If every call had to know the entity it reached through, changing the internal collaboration (moving a part, introducing a delegate) would break every path; the graph shape would become public API. The principle says each object may talk to its own partners but not to their partners, so knowledge is scoped to direct collaborators only.

The benefit lands on evolution and testing: because callers do not know the graph's interior, the graphs (who delegates to whom) can be re-arranged without touching callers — growth, refactoring, and extension stay local. It also keeps mutation visible: a caller that reaches three hops into the graph has updated state that no owner observes at the point of use; with one hop, the receiving object sees the message and can enforce invariants.

The mature nuance is what the principle does *not* forbid: it does not forbid answers that involve deeper knowledge — the "know" is about prevents-the-caller from *holding the neighbor*, not about the caller receiving computed facts. "Least knowledge" means the caller may ask a fair question and get a fair value (delegation returning computed results), but must not be handed the neighbor itself (the implementation-graph leak). Those two — asking versus holding — are the whole of the design tension.

## Q75: What is the collaboration view of the Gang-of-Four patterns — which ones are about delegation?

**A:** The behavioral and structural patterns for collaboration goals break into groups: those that *mutate delegation* (Strategy, State, Decorator, Proxy, Command) — each introduces a collaborator through which a request flows and often it forwards or selects — and those that *reshape the graph* (Facade, Mediator, Composite, Chain of Responsibility) — each thread edges of the object graph so that delegation happens through a new central or tree shape. Together they are a catalog of delegation topologies.

The value of naming them: patterns are *named delegation shapes* — Strategy says "delegate the algorithm," Proxy says "delegate with a shield that may build, cache or guard," Composite says "delegate uniformly to children," Mediator says "delegate the mutual wiring to a single coordinator." Recognizing the pattern names gives you map-labels for otherwise dense graphs: you can say "this edge is a Strategy selection" without re-deriving the collaboration each time.

The interview lesson: pattern-literate collaboration design chooses whether the shape is direct-delegation (Strategy, Proxy), containment (Facade), uniform-trees (Composite), or many-to-many routing (Mediator, Observer) based on what changes and who should own the choice — patterns are interchangeable *names* for delegation, not independent ideas — and knowing which topology matches the variation you expect is the real skill.

## Q76: Design a checkout as a collaboration graph — its objects, decisions, and who delegates what.

**A:** A checkout ownership design might be: `CheckoutController` holds the session; it delegates cart editing to `Cart`, product queries to `CatalogClient`, pricing to `PricingService`, shipping to `ShippingQuote`, tax to `TaxCalculator`, payment authorization to `PaymentGateway`, and order creation to `OrderRepository`. The decisions that shouldn't leak are the cross-cutting invariants: "can't checkout an empty cart", "can't authorize more than the total", "order only after auth success." Those belong to the coordinator (or to the order aggregate root), and everything else is delegation to specialists.

The wiring choices matter as much as the classes. `CheckoutController` should depend on interfaces for CatalogClient, PaymentGateway, TaxCalculator, and the Cart order root, so fakes slip in for tests and vendors are swappable; the Cart and Order are identity-bearing and single-owned (the controller holds them, the repository persists them by identity). The pure computations (price, tax, shipping rule) get delegated as values: the controller asks for a quote, never for the internals of the pricing engine.

The interview walk: name the messages ("rate my order", "authorize this amount", "persist this aggregate") and show the invariants live at the coordinator/root. Then pick a realistic change ("tax law changed") and show it touches exactly one edge — a new `TaxCalculator` implementation, no controller edit. That is the deliverable: a graph whose edges are contracts, whose decisions live at owners, and whose change is local.

## Q77: Argue both sides: when is inheritance genuinely better than delegation?

**A:** The inheritance case is strong when there is a *stable contract with a family of variants* that share a fixed skeleton — Template Method, uniform type identity ("every `Shape` draws a path"), and cheap specialization where parent behavior is *default-on* rather than negotiated. Delegation buys substitution at the price of indirection and seams: every switch must be, well, a switch; every variant must be a class with a factory; a type hierarchy gives you the "is-a" fact for free (a `Sparrow` *is* a `Bird`, renderers type-check against the family) that delegation reproduces only by interface conformance.

The delegation counter-case is equally sharp. Inheritance fixes behavior at class-definition time, so two dimensions of variation become a Cartesian explosion (logging × caching × metrics × formats ⇒ a class per combination), and the parent's implementation is change-hostile: fix a bug in the base and every subclass changes, but only a bug in the *contract* should. Delegation composes concerns as independent delegates, changes a switch at runtime, and isolates each variant's change. For reusable capability ("be sortable", "be iterable"), interfaces + small delegating delegates are much cheaper than deep class dishes.

The synthesis for an interview: use inheritance when the relationship is *essential* "is-a" with a shared invariant, the families are few, and you want the type system to model the taxonomy; use delegation when the relationship is *capability* ("has-a" behavior) or when variation is combinatorial or runtime. The question then is not "inheritance or delegation?" but "is this a taxonomy or a set of pluggable roles?" — and the answer decides the edge type.

## Q78: How do domain events change the collaboration between producers and consumers?

**A:** A domain event is an explicit, immutable statement of a fact that has happened ("order.placed", "payment.authorized"). Instead of a producer calling a consumer directly (tight coupling, the producer must know the consumer and its schedule), the producer *publishes* and consumers are *subscribed*: the producer's collaboration becomes "emit the event and forget the consumers", the consumers' collaboration becomes "react to events I care about". This is delegation inverted — the producer no longer delegates each task to each consumer; it delegates the *notification* to the bus and lets consumers delegate processing to their own handlers.

The consequences are the standard trade-offs: the coupling between producer and consumer types is now nil (each knows only the event contract); adding a consumer costs nothing in the producer; the ordering and completion guarantees become the infrastructure's, not the call stack's. So the design's focus shifts to event contracts (versioned, immutable, replayable), idempotency (a consumer may see an event twice), and visibility (the collaboration is now asynchronous and needs tracing/audit).

The mature design decision is *which edges become events*. Intra-transaction, intra-aggregate logic stays direct delegation (guaranteeing invariants); edges into other bounded contexts or into systems that grew new consumers over time become events. The senior answer names that: events are the delegation seam for "things that must not block, must not know their audience, or must be avially replayed" — and they change the graph from "who calls whom" to "who publishes what."

## Q79: How do you teach a team to design with delegation instead of deep type hierarchies?

**A:** Start by reframing the decision: the question is not "is-a or has-a?" but "do these objects vary independently, or is this a taxonomy with a shared invariant?" Demonstrate with the rectangle-square trap and the "circle-ellipse problem" that taxonomy intuition fails; then show the delegation repair (a shape holds a geometry; each dimension is a role with its own interface). The teaching move is a before/after refactor with the same feature and its test surface visible — delegation's win shows in tests (fake the collaborator), not in abstract theory.

Make the rules walkable: (1) if a class changes because *both* a new feature and a new subclass appear, split the feature into a collaborator; (2) if you are adding subclasses faster than you are adding type-appropriate behavior, you are probably building a switch — prefer delegation (strategy); (3) if a method's responsibility drifts toward another class's data, send the message instead of the data. Pair those with a small catalog: "delegate the algorithm" (Strategy), "delegate the variant" (State), "delegate one concern" (Decorator).

The cultural lever is code-review gates against smells: no 20-class hierarchies without a documented reason, no getters that spawn chains (tell-don't-ask as a review word), interfaces as first-class edges. And the final, honest turn: teach the *exception management* — when the taxonomy is real (a genuine is-a family with shared invariants), inheritance is right, and the team must be able to both see it and defend it — so delegation is not dogma but a decision made by examination.

## Q80: Where do cross-cutting concerns (logging, authn, metrics, retries) live in a collaboration design?

**A:** Cross-cutting concerns belong in *delegation boundaries* — the edges between objects and between layers — not in every collaborator's body. The cleanest technical form is a decorator chain (each concern is one wrapper class around the delegate, at a wiring point), so the object graph is unchanged in shape, the concern is one class with its own tests, and every site that needs "retry plus metrics plus authn on this service call" gets a composed wrapper rather than duplicated code.

The design question is then *which edges*, not whether each object logs. Logging at the delegation edges catches the message flow (who called whom with what result) — that is the trace; metrics at the boundary measure the collaboration itself (latency, success rate, retry counts); authn at the boundary is the gate before the delegate executes. Put each at edges, not inside the delegator or delegate, so concern changes don't touch domain logic or specialist code.

The interview nuance: the edge decorations interact. Order matters (authn before metrics, metrics around a retrying client, traces spanning retries), so the wrappers must compose deliberately; and they must not become the god-wrapper that absorbs policy. The resolution: a thin chain per edge is acceptable if each layer is a single concern and the composition is wired (composition root), not re-implemented per call — the graph carries the concerns as first-class delegates at a small set of designated boundaries.

## Q81: How do you structure a large system as layers while keeping peer-to-peer collaboration healthy?

**A:** The layered structure handles "up/down" dependencies (web → application → domain → infrastructure) — but collaboration is richer than dependencies: peers within a layer, and across layers with hazards, collaborate through roles. The rule is that dependency arrows point inward ("all layers depend on the domain layer"), and the collaboration arrows (those that *invoke*) should respect the same, with the domain layer free to collaborate internally without directional constraint.

Peer collaboration within a layer is unproblematic (two services in the application layer can delegate to each other if they respect one-who-owns-the-outcome). The tricky healthy case is "top-layer asks down" (web asks application asks domain) — obvious; but "domain needs a service from the application layer" is a forward-dependency when the domain layer defines the interface (dependency inversion): the domain declares an interface, the application-layer detail implements it and is injected, so the domain collaborates without depending on the application layer.

The interview deposit: layers express dependency policy, not collaboration topology. You keep the graph healthy by deciding per-crossing-edge: either the edge fully respects the inward-dependency rule (delegation from outer to inner is fine and direct), or the edge needs a `defining-owner interface` (an inversion seam) so the collaboration is legal even though the implementer lives in an outer layer. The outcome is a design where "the collaboration flow" and "the dependency direction" are both clean and legible.

## Q82: What are the true costs of indirection (delegation's price) and how do you mitigate them?

**A:** The costs: (1) *hide-reflected-by*: behavior is no longer census by class, it is spread across delegators — reading which object does what requires the graph; (2) *tracing*: a bug's path is a walk through edges, and each hop can swallow cause; (3) *discovery*: figuring out "what is the real implementation" takes tooling, and too many layers make the design's intent hard to re-derive; (4) *test weight*: every seam means a decision about fakes — a true cost in setup and in tests that no longer exercise the real collaboration.

Mitigation is by discipline, not abolition: (1) name edges and interfaces with the collaboration intent (an interface is "how the order gets priced", not "PricingStuff"); (2) keep the delegation *nearby*— the delegator and its principal delegate often resolve their best seams in one file, and cross-layer delegation is the case to watch; (3) use tools: call-graph tooling, sequence-diagram generation, and ignore-the-noise in the reading; (4) prefer a few deep edges with a real owner over many shallow ones with no owner — that is, cost scales with *hops that add no behavior*.

The interview-finish: the cost of a delegation edge is the cost of *a seam that must exist* — and a seam that must not exist (nothing varies, nothing is translated) should be fused. Every delegation is a bet on variation or translation; when the bet fails (nothing varies, nothing translated), the edge is pure tax. The design discipline is therefore to keep the bet set justified: name the variation or the translation for every edge, and accelerate growth by adding edges exactly when a new seam is warranted.

## Q83: How do you choose the delegation boundary when decomposing a hard-to-grasp system (microservice-style)?

**A:** Choose boundaries by *who owns the outcome and who owns the data*, not by class. In a service decomposition the analogous question is "which use-cases mutate which aggregates?" — each boundary hosts the aggregates and the invariants it can own, and the cross-boundary collaboration is by contract (ID references, events, query interfaces), mirroring object delegation's edge rules at a coarser grain.

The pragmatic signal: find the *high-cohesion clusters* (data + rules + the use-cases that touch them) and the *cross-cluster interactions* — the latter are the boundary edges, and you decide them by stickiness (how tightly the invariants cohere), by change-sharing (do the two clusters usually change together — then they belong together), and by ownership friction (two teams needing the same data faster than a contract can update). Where rules cohere but change at different rates, a new aggregate/context boundary earns its own edge.

The mature trap to avoid: boundaries chosen ergonomically (by class, team, or "tech layer") result in "telephone-game" edges where each hop translates and the total behavior leaks; boundaries chosen *by ownership and rate of change* result in the healthy few explicit edges the system needs. The answer is the same as single-object delegation: the seam is where knowledge changes hands at a natural, legible division — and the division is by ownership, not by the surface appearance.

## Q84: Evaluate the claim "delegation always beats inheritance for code reuse."

**A:** False as an absolute, true as a bias. Delegation beats inheritance for *behavior reuse* when variation is combinatorial or runtime, when you want isolation of change and substitution, and when the "is-a" intuition is really "has-a heartbeat of capabilities." But inheritance is cheaper for *contract reuse* when there is a true specialization with a shared invariant (all subclasses honor the parent's contract), few dimensions vary, and the taxonomy is small and stable — the cost of delegation (create a class, an interface, a factory, a wiring point per variant) exceeds the cost of the subclass line under those conditions.

The deeper critique is that the sentence mixes two goods. "Reuse" can mean "reuse code" (inheritance signals sharing implementation) or "reuse behavior" (delegation signals sharing capabilities behind a contract). Inheritance's reuse comes bundled with *the parent's implementation as part of the subtype's contract* — that is power and debt; delegation's reuse leaves the implementation at a distance the delegator can choose to vary. So the rule is valuable as a default: when unsure, start delegation — because un-inheriting is nearly impossible, un-delegating (fuse the edge) is easy.

The interview punch: the real metric is *where the variation lives and how it is paid for*. If variation is "the same shape, many implementations at runtime" — delegation. If variation is "a family that shares invariants and a fixed skeleton" — inheritance. "Always" is a red flag word; the designer's skill is deciding *type* of reuse and paying for it with the right edge.

## Q85: Which GRASP principles are really delegation principles in disguise?

**A:** GRASP's *Creator* says "who creates the object" is whoever needs steady access or owns/composes it — the construction edge is a delegation seam (the creator may instantiate a specialist and wire it in). *Controller* says "who handles a system event" — a coordinator object, itself a delegator, which receives the external message and delegates to the specialists. *Polymorphism* is literally "vary behavior by substituting collaborators behind a common interface" — delegation's core. *Pure Fabrication* puts a responsibility in a class that does not model a domain concept mainly for low coupling — that's a specialist/delegate. *Indirection* names the delegation itself (introducing a middle object to mediate). Even *High Cohesion* and *Low Coupling* are the same force that justifies delegation: distribute responsibility to raise cohesion, delegate to lower coupling.

The pattern isn't that GRASP "has" delegation among its names — it's that GRASP's assignment questions ("who should know", "who should respond", "who should create") are answered with delegation as often as not. Each answer decides an edge in the object graph, and the *edge* is the delegation artifact.

For an interview, the meaning is: the GRASP catalog and the delegation mindset encourage identical habit — assign responsibility to the object that has the information & authority, keep coupling low by delegating through contracts, and when the domain lacks a natural "who", fabricate a pure specialist. So "delegation design" and "responsibility-driven design" are the same practice viewed from the structural side and the assignment side.

## Q86: When is a thin facade the wrong boundary, even though it looks clean?

**A:** A thin facade is wrong when it hides *real variance* behind a single convenient call, or when the facade's single interface cannot express the collaboration's span. If the subsystem has clients with genuinely different needs (a read-model consumer vs a mutation orchestrator), a one-facade-fits-all forces each to be a thick adapter (or to expose a fat interface) — the seam should then be *two role views*, e.g. a `QueryFacade` and a `CommandFacade`, each whose delegation matches its consumers.

The other wrongness: a thin facade that forwards a single call that actually requires *policy* to be placed at the boundary — e.g., the facade's operation "checkout" is so thin it forwards to the checkout engine, but the boundary's policy (authn gate, quota, idempotency key) gets lost — then the seam is a lie: the true policy lives inside or outside, and the facade is either bypassing its own contract or duplicating it. A facade that doesn't centralize the boundary invariants is a pass-through with a misleading name.

The senior synthesis: facades are right when "one clean, stable contract over a changing interior" matches the actual audience. When the audience is multiple, or the boundary's invariant-load is heavy, the answer is multiple specialized facades (or a full context API) — not marshalling everything through one thin door just because it looks tidy. The seam must match who crosses it and what must be asserted there, not be a beauty-clean relay.

## Q87: How do you use delegation to keep transaction boundaries correct in an object graph?

**A:** Transactions are a delegation boundary because the work-unit scope (which state changes become atomic together) must be owned by exactly one collaborator — usually an application/service object or a unit-of-work — and all the collaborators that participate *delegate their persistence and their commit decision* to it. The rule is that no collaborator may commit, roll back, or flush on its own: entering a transaction is a decision crossing a delegation edge into the transaction owner.

The practical guard: domain objects stay persistence-unaware — they mutate their state and report (facts), and a transaction-owning service runs the sequence, delegating validation/application to the domain and asking a repository/components to flush and commit. Where an operation spans several aggregates, the transaction owner coordinates delegating each aggregate's change and then commits — the aggregates' invariants are asserted inside their own delegation edges, and the atomicity is asserted at the transaction edge.

The common failure to name: transaction boundaries that cut *through* delegation in a way that leaks — an object mid-chain flushing its own persistence, or two collaborators committing half the graph and then failing. The interview diagnosis is "find who owns atomicity": it should be an explicit, single assignment at the boundary where the graph's work is orchestrated, and every delegation edge inside either is pure in-memory work (safe to roll back by not committing) or delegates to the transaction owner. The senior answer then ties it to the composite/many-cascade rule: cascades go with the owner, references cross width-wise outside the transaction.

## Q88: How do you evolve a collaboration design (add/remove objects and edges) without breaking the world?

**A:** Evolution is safe when *edges are contracts* and *objects are owners*. To add a collaborator: introduce it behind an existing role interface, wire it at the composition root, no caller changes — the edge contract is honored by the new arrival and the delegator's test surface already covers it with the interface. To remove a collaborator: fuse its edge only if nothing varies, keep the interface if a future replacement must fit — the rule is "kill the implementer, keep the interface, replace the wiring", so deletion is a wiring edit plus an interface, not a hunt for references.

The hardening rule is *interface stability*: the contract ("who sends what, what must be guaranteed") changes slowly even as internal implementations and collaborators change constantly. Versioning enters when the edge contract itself must change (add a parameter, change a result shape): support a v2 interface and deprecate v1 at the boundary, or translate at a new adapter, so callers migrate stepwise instead of breaking in one commit.

The interview body of knowledge is the discipline that makes this safe: (1) dependencies point at interfaces, (2) each edge is a named contract with pre/post, (3) the object graph is assembled in a composition root so wiring changes are localized, (4) tests at each seam (unit: fake collaborators; integration: real wiring) either clide or shift. Under those four, "change the collaboration" is a local, observable edit; without them, "add one collaborator" becomes a world-hunt.

## Q89: How do you apply delegation safely in a concurrent object graph (async, threads, actors)?

**A:** In concurrent/extremely-limited languages, delegation changes shape: passing a message across a thread boundary or an actor's mailbox is still a delegation *semantic* (handing a responsibility to a collaborator that will act) but the edges are async — the delegator sends, and the delegate may process later; responsibility and ownership of state transfer to the delegate's context (its thread/actor). The safe rule is then "whoever owns the state at execution time decides", not "whoever forwarded the call."

The safe design pruning: (1) delegation edges crossing concurrency boundaries carry *values/immutable data* or *explicitly surrendered ownership*, never shared mutable refs; (2) state mutation lives in exactly one owner per object graph (single-threaded per aggregate; actor = one owner per isolated unit); (3) the cross-edge protocols are *command-like* (send-and-forget, ack, retry-set) so concurrent callers never assume sync pre/post in the same stack; (4) cycles are forbidden across boundaries — any cycle crosses ownership and deadlocks or races.

The senior talk: concurrency converts delegation from a *call* to a *dispatch* — async message-passing is the purest delegation (the caller says "please do this" and does not wait in the caller's frame). The invariant to protect is order: *who owns the result and when it arrives* must be explicit (handle, callback, or future), and the collaboration tests must run both single-threadedly (pre/post) and multithreaded (race detection, ordering), because a delegation edge that was safe under one threading model can race under another.

## Q90: What are the enduring signs of "ongle banana gorilla" (leaky abstraction) in a delegation graph?

**A:** The banana-gorilla leak — the layer that promised you a banana and then a gorilla with a banana was hiding inside — appears in delegation as *behavior that escapes the delegator's stated contract*: the delegate performs an expensive re-entrant call the caller's stack did not intend, a wrapper silently re-fetches or mutates state, or the "cheap local function" turns out to hide a network hop the contract never mentioned. You know you have it when callers build their logic around the *hidden* implementation rather than the interface.

The signs to look for: (1) a delegator whose contract implies "local, pure, cheap" but whose delegate is remotely hosted or mutates shared state; (2) exceptions that carry the delegate's transformations or the transformer's vocabulary — "I asked for an HTML view, I got the transformer's internal format error"; (3) an edge whose behavior changes with the *delegate's* configuration (a flag settings elsewhere flips the delegator's behavior without its input); (4) the delegate's failure modes force callers to branch on the *delegate's implementation* even though they only hold the delegator.

The fix is the same discipline as any contract: the delegator's boundary must *translate and assert* — surface the collaboration's real semantics (latency, durability, atomicity) honestly, or encapsulate them so the caller depends on the promised contract and nothing else. A healthy edge says clearly "this may cross a network" or "this is transactional"; a leaky edge lets the caller discover the gorilla at runtime — and the strongest interview answer distinguishes *the cost of an honest admission* (an explicit latency guarantee) from *the leak* (the gorilla hiding behind the banana).

## Q91: Design the collaboration model for a rendering pipeline (document → layout → paint) using delegation.

**A:** The pipeline is a chain of pure-functional stages connected by delegation: the `Document` aggregates its tree and exposes queries; the `LayoutEngine` delegates to the `Document` (ask structure) and produces layout boxes; the `PaintEngine` delegates to the layout boxes (geometry) and the `StyleResolver` (visual property set), and a `Renderer` coordinator owns the overall frame ordering — each stage is a stateless policy delegating to the model, never the reverse. The data crossing each edge is an *immutable value* (layout boxes, paint commands), so the stages can be parallelized and re-ordered without breaking ownership.

The collaboration invariants: the document owns its role as source-of-truth structure; the layout stage controls geometry (a delegate's output is fed, not mutated by the next stage); and cross-cutting concerns (theme, fonts, DPI scale) are injected as context values that every edge consumes but nobody mutates. Invalid states (layout before a dangling ref, paint without style resolution) are prevented because each delegate's postcondition is the next delegate's precondition — the chain's contracts make a valid sequence a type-level/logical guarantee.

The interview insight: the design turns "rendering" (a big function) into a small set of *owner/specialist* edges where each hop is a pure-ish transformation — that is delegation without the ownership soup. The change-sensitivity is handled by edge contracts: changing the theme touches only the style-resolver edge; adding a stage (accessibility tree) adds a delegate that consumes the document and feeds either layout or a separate read model — both local to a seam.

## Q92: How do you decide between call-driven orchestration and event-driven collaboration at scale?

**A:** The deciding factor is *consistency and workflow-shape* versus *decoupling and growth-rate*. Call-driven orchestration (a coordinator that delegates stepwise and waits for each) fits workflows that are sequential, transactional, and require tight failure handling: the orchestrator owns compensation, retry policy, and the "who succeeded and who didn't" story — it keeps a legible, debuggable graph. Event-driven collaboration fits flows that are *fire-and-observe*: many consumers, new subscribers appearing over time, long-running asynchronous work, or teams-that-must-not-know each other.

The mature synthesis is *hybrid by edge*: pick the seam per dependency. Workflows that must be consistent "now" (payment → stock-reserve) are call-driven, with the orchestrator's own state persisted so the flow can resume; compatibility/cross-team notifications ("order placed" → pricing team, inventory team, analytics) are event-driven, published once and consumed many. The graph stays legible because the call edges are the *transaction backbone*, and the event edges are the *fan-out*, each named and tested by its own contract.

The senior criterion: "replaying" tells you which side you are on. If a flow must be replayed step-by-step to restore consistency (a saga or workflow), call-driven orchestration, with each delegate idempotent, gives you the resume point. If a fact is true once and consumers can build what they need from it independently, event-driven collaboration costs less and scales more — and one can even *host* the other (call the flow that owns the atomic chain, then publish the outcome event).

## Q93: Describe "hierarchical delegation" versus "flat long chains" in a large system and how you keep the hierarchy honest.

**A:** Hierarchical delegation has *intermediate owners that really own*: each level coordinates the level below and adds a real contract (aggregate root coordinating its parts, application service orchestrating its domain, the composition root wiring services). Flat long chains are sequences where every link forwards with no intermediate ownership or translation — every link has the same shape and defers to the same lower layer, so the "levels" are fake. The hierarchy is honest when each level *can* be tested in isolation, each level's contract is distinct from its children's, and the levels actually make decisions (not just relay).

Honesty enforcement comes from three rules: (1) each level's contract adds semantics the level below doesn't guarantee (the aggregate adds invariants; the service adds transaction and policy; the API adds shape and auth), so removing a level loses meaning; (2) call-backs across levels are forbidden — a level must not be skipped, or the intermediate is a fake layer; (3) the direction of dependency equals the direction of delegation (inner layers don't depend on outer ones, even when an outer level delegates inward — via inversion seams it's still the domain defining the interface).

The senior assessment: draw the graph. If every level has distinct contracts and the dependencies point inward, it is architecture; if levels merge into "everyone forwards to the repository," it is a flat chain in a hierarchy costume — fuse the empty levels, or give them real decisions. The tell to an interviewer: "I keep the hierarchy because each edge is a *decision*, not a *relay* — and I delete any level whose only act is forwarding."

## Q94: How should an aggregator delegate while still guarding the aggregate's invariants?

**A:** The aggregator (an object that consumes several aggregates or roots) must delegate *queries and computations* to them but must not lose the compound invariants that connect them. The rule: research each collaborator to answer a question, but the aggregator's own state-commit passes through itself, and the invariants that span rivals (e.g., "sum of parts ≤ budget", "item already in the cart") are asserted at the aggregator before any mutation is applied — the aggregator coordinates, delegates the pieces, and owns the whole.

Mechanically: the aggregator's public methods are *transaction-style* — validate spanning invariants, ask each collaborator for its individual opinion via a query (tell-don't-ask), combine, then apply mutations by delegating to each owner (the owner guards its own invariants), and finally assert the posts that only the aggregator can see. Each collaborator remains owner of its own aggregate rules; the aggregator only checks the *spans* no single owner can check — that division is what makes the design delegating rather than god-like.

The interview emphasis: never expose "half-applied" state. If the aggregator must coordinate three delegates and the third fails, its contract includes rollback or at-least-vacuous cancel for the first two — the invariant it guards is "the group operation is all-or-nothing from the caller's view". So the aggregator delegates the mechanical steps to specialists while the responsibility for the compound invariant, and for the all-or-nothing outcome, stays with the aggregator as the owner of the boundary.

## Q95: How do you keep collaboration tests independent from wiring/integration tests?

**A:** Collaboration (unit) tests test each object against *its own contract with faked collaborators*; wiring/integration tests assemble the real graph once and assert the arrangement. The seam to hold both is the interface and the composition root: the unit tiers use the interfaces to inject counters/the fakes; the integration tier builds the real objects, wires them as production does, and runs a "sanity path" that exercises a full delegation round trip (including the translation and the actual collaborator's behavior) — the two tiers overlap only at the seam, never burrow into each other.

The independence comes from rules: unit tests never touch a real delegate (no DB, no HTTP, no real service) — that keeps them fast and deterministic, and each change to a collaborator's internals re-tests only its own unit tier plus one integration round trip, never the whole graph. Wiring tests assert *the graph mapping* ("this controller got the service that uses the real repo") — cheap, slow, few — and the acceptance tests (the hardest tier, fewest in number) exercise one real end-to-end feature so the *contracts between edges* are honored in composition.

The interview sharp declination: "a unit test that news up real collaborators is a wiring test wearing a unit costume." The telling discipline is *one entry point per edge contract*: each seam's interface has (a) a fake for the consumer's unit tier, (b) at least one real integration for the edge, (c) coverage of failure and success at both. Then the delegation graph stays trustable: black-box per object, contract-true at the seam, and integration-verified once.

## Q96: How does delegation interact with ORMs and lazy-loading proxies?

**A:** ORMs attach a proxy to a detained reference so a property access triggers a lazy fetch — the proxy is a *delegation proxy*: the holder holds a proxy that forwards property reads/writes to the real (possibly freshly-loaded) object. This creates two dangers: (1) the proxy hides IO in a property access, so the "property" edge is not a pure delegation contract, it's a hidden network/DB call (a banana-gorilla leak); (2) the proxy captures the *persistence context* it came from, so sharing the proxy across contexts re-links the graph to the wrong context or triggers detached-state violence.

The design discipline: keep lazy-loading proxies *out of domain collaboration edges* — the domain should operate over fully-loaded aggregates or explicit values (references/IDs) so the edge's behavior is honest; let the ORM's proxy exist at the persistence boundary (repository returns real graphs, or explicitly marked lazy paths), and never pass a proxy onward as if it were a plain object. Use IDs or snapshots across an edge when the real graph is not loaded, and let the repository re-query.

The senior trap to name: "lazy-loading inside a transaction during a delegation call" — the delegator sends a message to a part that is a proxy; the proxy queries mid-call; two problems: auditability (the delegation had a hidden DB read) and N+1 (many proxy hits per loop). The answer is eager loading or query-shaped delegation (load per use-case), and treating the ORM edge as a real boundary: the domain delegates persistence semantics to the repository, while the proxies stay an implementation detail of that edge, never of the collaboration.

## Q97: When delegating to a "context" or "container," how do you keep it from becoming a god object (or a god singleton)?

**A:** The context/container is the shared reference many collaborators hold; it becomes a god object when it accumulates global state and per-collaborator services under an amorphous `getX()/setX()` API that everything reaches into. The guard is role-shaping: expose narrow, typed *views* — each collaborator receives an `IRequestContext` (just the correlation ID), `ITransactionScope` (just begin/commit), `ITenantContext` (just the tenant) — and the container internally *delegates* each capability to a specialist, never implements it all.

Mechanically: hosts create the context, the container holds references to the specialists, and each collaborator is *given a view* on construction (constructor injection of the view, not the container). The views are interfaces, so tests fake a view trivially, and the container's internals (transaction handling, tenant resolution, requester metadata) can change without touching the collaborators — as long as the views stay stable, which is the actual contract.

The god-singleton trap lands when the container is *global and mutable*: every collaborator reaches it directly, ordering depends on who mutated what, and the "container" becomes a kitchen sink. The senior answer: the container is an *ownership bookkeeper*, not a workshop — its sole job is assembling and scoping the views — and the permanent rule is "if a collaborator needs a capability, give it the *view*, never the container; if a capability accumulates state, give it to a specialist and make the container delegate." The moment a container implements logic, it has slid toward god-hood.

## Q98: How does delegation relate to "open recursion" and the fragile base class problem?

**A:** Open recursion is the phenomenon where a base-class method calls another method that a subclass overrides — and the overridden behavior runs. This is inheritance's double-edged seam: it is the mechanism template methods exploit, and it is the fragile base class problem when a change to an override in a subclass breaks the base's called skeleton (or vice versa). Delegation removes the recursion-from-implementation: a delegator calls a collaborator explicitly, so the "which method runs" is visible in the wiring, not hidden in an overriding self-call.

The fragility that delegation avoids: with inheritance, editing a base class's internal call can change the behavior of every subclass (surprise); with delegation, editing a delegate's internals changes only what that delegate provides, and the delegator's contract is untouched as long as the delegate's contract holds — the change locates at the edge, not throughout the hierarchy. The caution is that delegation *moves* the seam (from "which method resolves" to "which collaborator is wired"), so it is not automatic safety: a shared delegate mutated by several delegators re-introduces cross-effects, just at a different seam.

The interview distinction: open recursion is powerful when overrides are *deliberate hooks*; fragile-base occurs when the hooks are *accidental*. Delegation makes each hook an explicit interface/wiring decision rather than a name-collision override — you see "this object delegates accrual to an assigned calculator" instead of "this subclass happens to override `run()` because the base's `process()` calls it". So delegation trades hidden internal dynamics for explicit edges — at the price of naming and wiring, which is the coin to spend wisely.

## Q99: Design a plugin/callback collaboration where a host delegates work to third-party extensions, including discovery and fail-safety.

**A:** The host defines the *extension contract* (an interface with the operations and their pre/post, plus a version), the *extension point registration* (methods the host calls into the plugin, methods the plugin can call back into the host — two-sided collaboration), and the *discovery* (plugins declare metadata — capabilities, version, config schema — that the host reads at load time and never guesses). The host's job is to delegate each operation to the right plugin, and the plugin's job is to honor the contract without trusting the host's internals.

Fail-safety is the careful part of the contract: every cross-extension call is wrapped at the boundary (the host isolates each plugin call in its own error-bound: exception mapping, timeout, resource limits), and the plugin *must not* be allowed to corrupt the host's state or an aggregate the host owns. So delegation is one-hop and *mediated*: the host delegates a capability to a plugin instance while the *invariants* (the host's own state, the plugin's resource limits, crash isolation) are owned by the host's boundary — this is why hosts rarely hand plugins the aggregates themselves.

The senior considerations: versioning the extension contract (a plugin may speak v1 while a host is v3 — a translation adapter, itself a delegator, sits in between), and serialization-of-effects (two plugins may both claim the same operation); the host's discovery assigns roles by capability, arbitrates conflicts, and keeps a policy order. The interview deliverable: a host that delegates work through a crisp, versioned, contract-typed seam; plugins that are swappable and isolated; and a design where "third-party extension" is an edge with a rigorous boundary, not a warm hug.

## Q100: What is your overall philosophy for deciding delegation at every level — and how would you present it in an interview?

**A:** The decision ladder: (1) *who owns the data* decides who owns the behavior (tell-don't-ask, high cohesion) — a message goes to the owner. (2) *what varies* decides the seam — if variation is per-variant or per-runtime, delegate to a strategy/state/service behind an interface; if a family shares a stable skeleton with fixed invariants, inheritance/self-delegation composition is defensible. (3) *what crosses a boundary* decides the edge type — within a transaction/aggregate, direct delegation; across contexts or unknown consumers/orders, an event or a contract-based edge. (4) *who must not know* decides the encapsulation — cross-boundary coupling goes through interfaces so the graph can evolve.

The presentation is the skill — interviews prize the *reasoning*, not the vocabulary. Start from a concrete case ("here's an order checkout: who owns total, who owns tax, who owns payment") and draw the edges; then justify each choice with the two questions "who has the information to decide?" and "what must be able to change independently?"; and then show what happens on a realistic change — where the edit lands, what doesn't change, what the tests look like. That demonstrates the ability to *design* delegation, not just recite it.

The final principle to state: delegation is dividing work *and* dividing change; a good delegation graph is a map of what can vary independently, with each edge a contract that isolates its two sides. The interview answer closes on the humility: delegation is not the goal — legibility, testability, and thought-about boundaries are — and the best delegation is the one you can defend (name the ownership, the variation, the boundary) and the one where deleting a layer is a conscious, safe decision, not a mystery.

