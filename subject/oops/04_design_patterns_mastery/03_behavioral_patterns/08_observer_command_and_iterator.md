# Observer, Command and Iterator Patterns — 100 Interview Q&A

## Q1: What is the Observer pattern and when would you use it?

**A:** The Observer pattern defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically. It is a fundamental behavioral pattern used to achieve loose coupling between the component that owns the data and the components that display or react to that data.

In practice, you would use the Observer pattern when you have a scenario where changes to one object require updating others, but you don't want to tightly couple the subject to those objects. Classic examples include event handling systems, UI data binding, notification systems, and any publish-subscribe mechanism. The pattern allows you to dynamically register and unregister observers at runtime without modifying the subject.

The key benefit is that the subject does not need to know the concrete classes of its observers; it only needs to know that they implement an observer interface. This promotes the Open/Closed Principle since you can add new observer types without changing the subject.

**Example:**
```java
interface Observer {
    void update(String event);
}

class EventSource {
    private List<Observer> observers = new ArrayList<>();

    public void subscribe(Observer o) { observers.add(o); }
    public void unsubscribe(Observer o) { observers.remove(o); }

    public void emit(String event) {
        for (Observer o : observers) {
            o.update(event);
        }
    }
}
```

---

## Q2: What is the difference between the Observer pattern and the Publish-Subscribe pattern?

**A:** While often used interchangeably, the Observer and Publish-Subscribe patterns have subtle architectural differences. In the classic Observer pattern, the subject (observable) maintains a direct reference to its observers and notifies them synchronously. The observers are aware of the subject, creating a bidirectional coupling.

In the Publish-Subscribe pattern, there is typically an intermediary event bus or message broker that decouples publishers from subscribers entirely. Publishers emit events to the bus, and subscribers register interest in certain event types. Neither party knows about the other. This indirection allows for greater scalability, asynchronous delivery, and geographic distribution of components.

The Publish-Subscribe model is the backbone of message queue systems like RabbitMQ, Kafka, and Redis Pub/Sub, whereas the Observer pattern is more commonly seen in in-process, single-application contexts such as GUI frameworks and reactive UI libraries.

**Example:**
```python
class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, topic, callback):
        self._subscribers[topic].append(callback)

    def publish(self, topic, data):
        for cb in self._subscribers.get(topic, []):
            cb(data)

bus = EventBus()
bus.subscribe("order.created", lambda d: print(f"Email sent for {d}"))
bus.publish("order.created", {"id": 42})
```

---

## Q3: How do you handle multiple event types in an Observer-based system?

**A:** In a real-world system, observers often need to react to different types of events. There are several strategies to handle this. The simplest is to pass an event object (rather than a raw string) that carries a type discriminator, and each observer filters for the events it cares about. Another approach is to maintain separate observer lists per event type, so each subscriber registers for specific events.

A more sophisticated approach uses typed channels or topic-based subscriptions where the subject (or event bus) routes events by type. This mirrors how modern reactive frameworks and event-driven architectures work. Strongly-typed event systems may use generics or sealed class hierarchies to ensure compile-time safety.

The key design consideration is balancing flexibility with type safety. Wildly generic observer signatures are flexible but error-prone, while strongly typed systems are safer but require more infrastructure to set up.

**Example:**
```java
sealed interface Event {
    record OrderCreated(String orderId) implements Event {}
    record PaymentReceived(String orderId, double amount) implements Event {}
}

class EventBus {
    private Map<Class<?>, List<Consumer<?>>> handlers = new HashMap<>();

    <T extends Event> void on(Class<T> type, Consumer<T> handler) {
        handlers.computeIfAbsent(type, k -> new ArrayList<>()).add(handler);
    }

    @SuppressWarnings("unchecked")
    <T extends Event> void emit(T event) {
        for (var h : handlers.getOrDefault(event.getClass(), List.of())) {
            ((Consumer<T>) h).accept(event);
        }
    }
}
```

---

## Q4: What are the SOLID principles at play in the Observer pattern?

**A:** The Observer pattern aligns with several SOLID principles. The Single Responsibility Principle is upheld because the subject is responsible only for managing state and notifying observers, while each observer encapsulates its own reaction logic. The Open/Closed Principle is central: the subject is open for extension (you can add new observer types) but closed for modification (the subject code does not change).

The Liskov Substitution Principle applies because any implementation of the observer interface can be substituted without breaking the subject. The Interface Segregation Principle encourages narrow, focused observer interfaces rather than monolithic ones that force observers to implement methods they don't need. The Dependency Inversion Principle is satisfied because the subject depends on an abstraction (the observer interface) rather than on concrete classes.

In poorly designed Observer implementations, violations occur when observers directly access the subject's internal state, breaking encapsulation, or when the observer interface is too broad, violating ISP.

---

## Q5: What is the Command pattern and what problems does it solve?

**A:** The Command pattern encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue requests, support undoable operations, and log operations. It decouples the object that invokes the operation (the invoker) from the one that knows how to perform it (the receiver).

The pattern solves several problems: it allows you to defer execution of a command, execute commands at different times, undo/redo operations, maintain a history of operations, and implement composite or macro commands. It is essential in GUI frameworks for mapping user actions to operations, in transactional systems for rollback capability, and in task scheduling systems.

Each command object implements a common interface with at minimum an `execute()` method. Undo support adds an `undo()` method. The invoker holds a reference to a command and calls `execute()` without knowing what operation will actually be performed.

**Example:**
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def undo(self): pass

class TextEditor:
    def __init__(self):
        self.content = ""

    def insert(self, text):
        self.content += text

    def delete_last(self, n):
        self.content = self.content[:-n]

class InsertCommand(Command):
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text
    def execute(self):
        self.editor.insert(self.text)
    def undo(self):
        self.editor.delete_last(len(self.text))
```

---

## Q6: How does the Command pattern enable undo and redo functionality?

**A:** Undo and redo are among the most valuable capabilities the Command pattern provides. Each command stores the state it needs to reverse its effect. When `execute()` is called, the command performs the action and may save a snapshot of relevant state. The `undo()` method reverses the action using that saved state.

An undo manager maintains two stacks: one for executed commands (for undo) and one for undone commands (for redo). When the user undoes, the top command is popped from the undo stack, its `undo()` is called, and it is pushed onto the redo stack. Redo reverses this flow. A new command execution clears the redo stack, maintaining a consistent linear history.

For complex operations like drawing applications, commands store before-and-after snapshots. For database operations, commands may store SQL statements where the inverse is used for undo. Care must be taken with command grouping (macro commands) where a single undo must reverse an entire group of atomic operations.

---

## Q7: What is the role of a macro command in the Command pattern?

**A:** A macro command is a composite command that groups multiple simple commands into a single unit. When the macro command's `execute()` is called, it invokes `execute()` on each of its child commands in sequence. Similarly, `undo()` reverses them in reverse order. This is analogous to the Composite pattern applied to commands.

Macro commands are useful in scenarios like text editors (selecting and formatting multiple paragraphs), CAD software (applying a series of transformations), or batch processing (executing a sequence of operations as a single transaction). They allow users to treat a complex operation as a single action, simplifying the undo/redo history and the user experience.

The implementation typically stores an ordered list of commands and iterates over them. Error handling within a macro command requires careful design: should partial execution be allowed, or should the macro fail atomically?

**Example:**
```java
class MacroCommand implements Command {
    private List<Command> commands = new ArrayList<>();

    public void add(Command cmd) { commands.add(cmd); }

    public void execute() {
        for (Command c : commands) c.execute();
    }

    public void undo() {
        for (int i = commands.size() - 1; i >= 0; i--) {
            commands.get(i).undo();
        }
    }
}
```

---

## Q8: How does the Command pattern support transactional behavior?

**A:** Transactional behavior in the Command pattern means that a group of commands either all succeed or all fail, with no partial effects visible. This is achieved by combining macro commands with a transaction protocol. Each command in the transaction must implement not just `execute()` and `undo()`, but also a `validate()` or `canExecute()` method that checks preconditions before execution.

The transaction manager executes each command sequentially, checking for success after each. If any command fails, the manager calls `undo()` on all previously executed commands in reverse order, rolling back the entire transaction. This ensures atomicity. In distributed systems, this maps to saga patterns where compensating transactions undo previous steps.

The Command pattern's encapsulation of operations makes it naturally suited for transactional systems because each command encapsulates both the forward action and the compensating action, making rollback a uniform operation regardless of the command type.

---

## Q9: What is the Iterator pattern and why is it important?

**A:** The Iterator pattern provides a uniform interface for accessing the elements of an aggregate object sequentially without exposing its underlying representation. It decouples the traversal algorithm from the collection, allowing multiple traversal strategies and hiding the internal structure of the collection (whether it's an array, linked list, tree, or graph).

The pattern is important because it supports polymorphic iteration: client code can iterate over any collection that provides an iterator, without knowing its internal structure. It also allows multiple simultaneous traversals of the same collection, since each iterator maintains its own traversal state.

Most modern languages provide built-in iterator support (Python's `__iter__`/`__next__`, Java's `Iterator<T>`, C++'s iterator classes). Understanding the pattern is essential because it underpins language-level constructs like `for-each` loops, generator functions, and streaming APIs.

---

## Q10: What is the difference between internal and external iterators?

**A:** An external iterator (or active iterator) is controlled by the client: the client calls `hasNext()` and `next()` on the iterator to traverse the collection. The client drives the traversal and decides when to stop. Java's `Iterator<T>` is a classic external iterator.

An internal iterator (or passive iterator) is controlled by the collection itself. The client passes a function or lambda to the collection, and the collection applies it to each element internally. Python's `list.map()`, `list.forEach()`, and JavaScript's `Array.prototype.forEach()` are examples of internal iterators.

External iterators give the client more control over the traversal (skip elements, iterate backward, pause and resume), while internal iterators are more concise and less error-prone since the client cannot accidentally corrupt the iteration state. Internal iterators also make it easier for the collection to optimize traversal (e.g., parallel iteration, tree balancing during traversal).

**Example:**
```python
# External iterator
class Tree:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def __iter__(self):
        yield self.value
        for child in self.children:
            yield from child

tree = Tree(1, [Tree(2), Tree(3, [Tree(4)])])
for val in tree:
    print(val)  # 1, 2, 3, 4

# Internal iterator
tree.traverse(lambda node: print(node.value))
```

---

## Q11: What are lazy iterators and generators?

**A:** Lazy iterators (or lazy evaluation iterators) produce elements on-demand rather than computing all elements upfront. Each call to `next()` computes or retrieves the next element, which is essential for working with potentially infinite sequences or very large datasets that cannot fit in memory.

Generators are the most common implementation of lazy iterators. In Python, a function with `yield` becomes a generator function that returns a generator object. In Java, `Stream<T>` and `Spliterator<T>` provide lazy evaluation pipelines. C++20 introduced ranges and generators for similar purposes.

Lazy evaluation provides significant performance benefits: it avoids unnecessary computation (short-circuiting), reduces memory consumption, and enables composing complex data processing pipelines where only the final consumed results are computed. The trade-off is that iterators become stateful and non-replayable.

---

## Q12: How do you implement a thread-safe iterator?

**A:** Thread-safe iteration requires ensuring that concurrent modifications to the collection do not cause `ConcurrentModificationException` or undefined behavior. Strategies include defensive copying (snapshot iteration), synchronized iteration, and using concurrent collections.

In Java, the `CopyOnWriteArrayList` creates a new copy of the underlying array for each modification, allowing safe iteration over the original snapshot. `ConcurrentLinkedQueue` provides a weakly consistent iterator that reflects the state of the queue at or since its creation. Explicit synchronization wraps iteration in a synchronized block, but this can cause contention.

The best approach depends on the use case: read-heavy scenarios benefit from copy-on-write, write-heavy scenarios need concurrent data structures, and mixed workloads may use read-write locks. The key principle is that the iterator should not fail due to concurrent modifications; at worst, it may miss or duplicate elements.

---

## Q13: What is the Null Object pattern and how does it relate to iterators?

**A:** The Null Object pattern provides a default implementation that does nothing, replacing null checks with polymorphic behavior. In the context of iterators, a Null Iterator is an iterator that immediately signals it has no elements (its `hasNext()` always returns false).

This is valuable because it eliminates null checks in client code. Instead of writing `if (iterator != null && iterator.hasNext())`, you can always have a valid iterator, and the Null Iterator simply completes the loop immediately. Collections can return Null Iterators instead of null when they are empty, following the "return empty instead of null" principle.

The Null Iterator is particularly useful in Composite patterns where some children may not have iterables, or in the Visitor pattern where iteration might have no valid targets. It makes client code cleaner and more robust.

**Example:**
```java
class NullIterator<T> implements Iterator<T> {
    public boolean hasNext() { return false; }
    public T next() { throw new NoSuchElementException(); }
}
```

---

## Q14: What is the Composite pattern and how does it interact with iterators?

**A:** The Composite pattern composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions uniformly. When combined with the Iterator pattern, you get polymorphic traversal of tree structures.

A composite iterator must handle the traversal of both leaf nodes and composite nodes recursively. The challenge is maintaining correct state when the iterator descends into a subtree and needs to resume at the parent level. This often requires a stack to track the traversal path.

Designing composite iterators requires choosing a traversal strategy: pre-order (visit parent before children), in-order (for binary trees), post-order (visit children before parent), or breadth-first (level-by-level). Each strategy produces a different sequence from the same composite structure.

---

## Q15: What are the trade-offs between the Observer and Mediator patterns?

**A:** Both patterns reduce coupling, but they do it differently. The Observer pattern creates many-to-many relationships between objects where subjects notify observers directly. The Mediator pattern centralizes complex communications between objects into a single mediator object.

The Observer pattern is better when the communication is inherently one-directional (data flows from subject to observer) and when observers are independent of each other. The Mediator is better when multiple objects interact in complex, coordinated ways and you want to avoid a tangled web of mutual references.

Observer can lead to memory leaks if observers are not properly unregistered, and debugging can be difficult because the notification chain is implicit. Mediator makes the communication explicit and centralized, making it easier to understand and debug, but it can become a "god object" if too much logic accumulates in it.

---

## Q16: How would you implement a thread-safe event bus?

**A:** A thread-safe event bus requires careful handling of concurrent subscriptions, unsubscriptions, and event dispatching. The subscriber registry must be protected against concurrent modification, typically using `CopyOnWriteArrayList` for subscriber lists or a read-write lock.

Event dispatching should not block new subscriptions or unsubscriptions. This can be achieved by taking a snapshot of subscribers before dispatching, or by using a lock-free data structure. For asynchronous dispatch, the bus may use an executor service to deliver events on separate threads.

Care must be taken with reentrant events (an event handler publishes another event). A thread-local flag or a queue-based approach prevents infinite recursion. Deadlock must be avoided by never holding locks during event delivery. The bus should also handle exceptions from individual subscribers without affecting others.

**Example:**
```java
class ThreadSafeEventBus {
    private final Map<String, CopyOnWriteArrayList<Consumer<Object>>> subs =
        new ConcurrentHashMap<>();

    public void subscribe(String topic, Consumer<Object> handler) {
        subs.computeIfAbsent(topic, k -> new CopyOnWriteArrayList<>()).add(handler);
    }

    public void publish(String topic, Object event) {
        List<Consumer<Object>> handlers = subs.getOrDefault(topic, List.of());
        for (Consumer<Object> h : handlers) {
            h.accept(event);
        }
    }
}
```

---

## Q17: What is event-driven architecture and how do the Observer and Command patterns fit in?

**A:** Event-driven architecture (EDA) is a software design paradigm where the flow of the program is determined by events: user actions, sensor outputs, messages from other programs, or system-generated signals. Components communicate by producing and consuming events rather than calling each other directly.

The Observer pattern is the foundational building block of EDA within a single process. It provides the mechanism for event producers to notify interested consumers. The Command pattern complements EDA by encapsulating event handlers as objects, enabling queuing, replay, and undo of event processing.

In distributed EDA, these patterns scale to message brokers (Kafka, RabbitMQ), event streams, and CQRS (Command Query Responsibility Segregation) architectures. The Command pattern maps naturally to command messages, while the Observer pattern maps to topic subscriptions. Together they enable highly decoupled, scalable, and resilient systems.

---

## Q18: What is a command queue and when would you use one?

**A:** A command queue is a data structure that stores command objects in the order they are submitted, and executes them either immediately or at a later time. It decouples the submission of work from its execution, enabling asynchronous processing, load leveling, and retry mechanisms.

You would use a command queue in several scenarios: background task processing (image resizing, email sending), job scheduling, rate-limiting API calls, implementing a thread pool's task queue, and building a saga orchestrator for distributed transactions. The queue provides natural buffering during traffic spikes.

The implementation can range from a simple `LinkedList<Command>` in a single-threaded application to distributed message queues like Redis, Kafka, or SQS in production systems. The pattern also supports prioritization, where commands are inserted with a priority and dequeued in priority order.

---

## Q19: How do you test the Observer pattern effectively?

**A:** Testing the Observer pattern requires verifying that observers are correctly notified when the subject's state changes, and that subscription/unsubscription works correctly. Use mock or spy objects to verify that `update()` is called the expected number of times with the expected arguments.

Test edge cases: subscribing the same observer multiple times (should it be notified multiple times?), unsubscribing during notification, notification when no observers are registered, and exception handling when an observer throws an exception. The subject should be resilient to observer failures.

Use dependency injection to provide the observer list, allowing you to inject test doubles. Verify that the subject does not hold references to observers that have been unregistered (memory leak testing). Use frameworks like Mockito for Java or unittest.mock for Python.

**Example:**
```python
class MockObserver:
    def __init__(self):
        self.events = []
    def update(self, event):
        self.events.append(event)

source = EventSource()
mock = MockObserver()
source.subscribe(mock)
source.emit("test")
assert mock.events == ["test"]
source.unsubscribe(mock)
source.emit("test2")
assert mock.events == ["test"]  # Not updated after unsubscribe
```

---

## Q20: What is the difference between synchronous and asynchronous observer notification?

**A:** In synchronous notification, the subject calls each observer's `update()` method sequentially in the same thread that triggered the state change. The subject blocks until all observers have been notified. This is simple and predictable but can cause performance issues if observers are slow or numerous.

In asynchronous notification, the subject dispatches notifications on separate threads or via a message queue. This allows the subject to continue immediately without waiting for observers. Asynchronous notification is essential in UI frameworks (to avoid blocking the UI thread) and in distributed systems (where observers may be remote services).

The trade-off is complexity: asynchronous notification requires thread synchronization, error handling across threads, and ordering guarantees. A hybrid approach dispatches asynchronously but guarantees in-order delivery. Some systems use a dedicated dispatcher thread or an executor service to manage the asynchronous delivery.

---

## Q21: How does the Iterator pattern support the Single Responsibility Principle?

**A:** The Iterator pattern separates the responsibility of traversal from the responsibility of storing and managing the collection's elements. Without the pattern, a collection class would need to manage both its data and the logic for iterating over it, potentially in multiple ways (forward, backward, filtered, level-order).

By extracting iteration logic into separate iterator classes, each class has a single, focused responsibility. The collection manages elements; each iterator manages a specific traversal strategy. This makes both the collection and the iterators easier to understand, test, and modify independently.

Adding a new traversal strategy does not require modifying the collection class; you simply create a new iterator. This aligns with the Open/Closed Principle as well. In complex data structures like trees or graphs, separating traversal from structure is essential for maintainability.

---

## Q22: What is the Memento pattern and how does it relate to Command?

**A:** The Memento pattern captures and externalizes an object's internal state so that it can be restored later, without violating encapsulation. It is closely related to the Command pattern's undo capability because undo often requires saving and restoring state.

While the Command pattern's `undo()` method may implement its own reversal logic (reversing an insert with a delete), the Memento pattern provides a generic state-capture mechanism. A command can save a memento before executing and restore it when undoing, without needing to know the details of state reversal.

This combination is powerful for complex undo systems: the Command defines what operation to perform, and the Memento defines how to capture and restore state. The trade-off is that mementos can be expensive in memory for large object states, and care must be taken to preserve encapsulation by not exposing memento internals.

---

## Q23: What are reactive streams and how do they relate to the Observer pattern?

**A:** Reactive streams are a specification for asynchronous stream processing with non-blocking backpressure. They extend the Observer pattern by adding a critical missing piece: backpressure. In the classic Observer pattern, a fast producer can overwhelm a slow consumer. Reactive streams define a protocol where the consumer signals demand to the producer.

The key components are: a Publisher (subject), a Subscriber (observer), a Subscription (manages the relationship and backpressure), and an Operator (transforms streams). Java's `java.util.concurrent.Flow` package, Project Reactor, and RxJava implement these concepts.

Reactive streams solve problems in high-throughput systems where data arrives faster than it can be processed. They provide a standardized way to compose asynchronous data pipelines with backpressure, error handling, and resource management. They are the foundation of modern reactive microservices.

---

## Q24: How do you handle observer ordering and priority?

**A:** Observer ordering determines the sequence in which observers are notified. In the basic Observer pattern, observers are notified in subscription order. Priority-based systems assign a numeric priority to each observer, and the subject sorts observers by priority before notification.

Implementation approaches include maintaining a `PriorityQueue` of observers, sorting the observer list on each notification (expensive but correct), or maintaining a pre-sorted list that is updated on each subscription/unsubscription. Some frameworks support ordered phases where observers at the same priority level are notified in subscription order.

Priority is useful in security systems (audit observers run before business observers), UI frameworks (layout observers before paint observers), and middleware chains (authentication before authorization). Care must be taken that priority changes at runtime are handled correctly and that priority inversion does not occur.

---

## Q25: What is the difference between an iterator and a generator?

**A:** An iterator is an object that implements the iterator protocol (typically `__iter__` and `__next__` in Python, or `hasNext()` and `next()` in Java). It maintains internal state and can be created from any collection or data source.

A generator is a special kind of iterator created from a function that contains `yield` statements. Each `yield` produces a value and suspends the function's execution. When `next()` is called again, execution resumes after the last `yield`. Generators are a syntactically concise way to create iterators without writing a full iterator class.

Generators are inherently lazy (values are computed on demand), memory-efficient (no intermediate list), and composable (generators can be chained). However, generators are single-pass and cannot be rewound. Once exhausted, a new generator must be created. Iterators backed by collections can be reset or re-traversed.

**Example:**
```python
def fibonacci(limit):
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

# Generator - lazy, single-pass
for n in fibonacci(100):
    print(n)
```


## Q26: What are the common pitfalls when implementing the Observer pattern?

**A:** Several pitfalls can undermine an Observer implementation. Memory leaks from failing to unregister observers (especially with anonymous inner classes or lambdas that hold references to the subject) are the most common. The subject retains strong references to observers, preventing garbage collection.

Another pitfall is notification during construction or destruction. If a subject notifies observers during its constructor, observers may interact with a partially constructed object. Similarly, notifying during destruction can cause observers to access invalid memory. A third issue is Cascading Updates where observer A's handler modifies the subject's state, triggering another notification, which can cause infinite loops or unexpected ordering.

Design mitigations include using weak references for observers (as Java's `WeakReference`), deferring notification to after construction, implementing reentrant guards, and documenting the threading contract. Testing should specifically target these edge cases.

---

## Q27: How would you implement a typed event system with compile-time safety?

**A:** A typed event system ensures that only valid event-handler pairings are possible, catching mismatches at compile time rather than runtime. In Java, this can be achieved with generics and sealed interfaces where each event type is associated with a specific handler type.

The event bus uses a type-safe registration mechanism: `bus.on(OrderCreated.class, handler)` where the handler type is inferred from the class type parameter. The implementation uses a `Map<Class<?>, List<Consumer<?>>>` internally, with type-safe wrappers that cast appropriately.

In C++, templates achieve compile-time event type checking. In TypeScript, discriminated unions and mapped types provide similar guarantees. The benefit is eliminating runtime ClassCastException errors and making the API self-documenting: the compiler enforces that handlers match their events.

**Example:**
```java
class TypedEventBus {
    private final Map<Class<?>, List<Object>> handlers = new HashMap<>();

    @SuppressWarnings("unchecked")
    <T> void on(Class<T> eventClass, Consumer<T> handler) {
        handlers.computeIfAbsent(eventClass, k -> new ArrayList<>()).add(handler);
    }

    @SuppressWarnings("unchecked")
    <T> void emit(T event) {
        for (Object h : handlers.getOrDefault(event.getClass(), List.of())) {
            ((Consumer<T>) h).accept(event);
        }
    }
}
```

---

## Q28: What is the difference between a command object and a function callback?

**A:** A function callback is a simple function reference passed to be invoked later. A command object is a full object that encapsulates a request, including the receiver, parameters, and state needed for execution and undo.

Callbacks are lightweight and suitable for simple event handling. Command objects carry more context: they can be serialized, stored in queues, logged, composed into macros, and support undo/redo. A callback cannot easily be undone, serialized, or composed with other callbacks.

The Command pattern also supports the state pattern where a command's behavior can change based on internal state (e.g., a command that executes differently the first time vs. subsequent times). Callbacks lack this capability. Commands integrate naturally with transaction managers, audit logs, and replay systems.

---

## Q29: How do you implement a bidirectional iterator?

**A:** A bidirectional iterator supports both forward (`next()`) and backward (`previous()`) traversal. In addition to the standard iterator methods, it adds `previous()` and may include `hasPrevious()`. Java's `ListIterator` is a bidirectional iterator that also supports modification and index tracking.

Implementing a bidirectional iterator for a doubly-linked list is straightforward: each node has `next` and `prev` pointers, and the iterator maintains a cursor that moves in either direction. For arrays, the cursor is an integer index that can be incremented or decremented.

For tree structures, bidirectional iteration is more complex and typically requires maintaining a stack or path from the root to the current position, allowing the iterator to navigate both up and down the tree. The iterator must handle edge cases like moving past the beginning or end of the collection.

---

## Q30: What is the role of the invoker in the Command pattern?

**A:** The invoker is the object that knows about commands but not about their implementation. It holds a reference to a command and triggers its execution at the appropriate time. The invoker provides the context in which commands are used: a button in a GUI, a keyboard shortcut handler, a menu item, or a task scheduler.

The invoker's key responsibilities include: storing the command reference, calling `execute()` at the right time, optionally storing command history for undo/redo, and managing the lifecycle of commands. The invoker is decoupled from the receiver because it interacts only with the command interface.

This decoupling allows the same invoker to work with any command implementation, and the same command to be used by different invokers. The invoker may also implement composite behavior, such as executing a macro command when a single button is pressed.

---

## Q31: How do you handle exceptions in command execution and undo?

**A:** Exception handling in commands must address three phases: validation (before execution), execution, and undo. During validation, commands can throw exceptions if preconditions are not met, preventing execution entirely.

During execution, if a command fails, the system must decide whether to undo previously executed commands in a macro/transaction (atomic rollback) or to allow partial execution with error reporting. The chosen strategy depends on the domain: database transactions require atomicity, while UI operations may tolerate partial completion.

During undo, exceptions are more problematic because the system is trying to restore a known-good state. Best practice is to catch and log exceptions during undo rather than propagating them, since the alternative (leaving the system in an inconsistent state) is worse. Some systems implement "best effort" undo that logs failures and alerts the user.

**Example:**
```java
class RobustCommand implements Command {
    public void execute() {
        try {
            doExecute();
        } catch (Exception e) {
            rollback();
            throw new CommandExecutionException("Failed: " + e.getMessage(), e);
        }
    }

    public void undo() {
        try {
            doUndo();
        } catch (Exception e) {
            Logger.error("Undo failed, manual intervention needed", e);
        }
    }
}
```

---

## Q32: What is the Visitor pattern and how does it differ from iteration?

**A:** The Visitor pattern lets you add operations to objects without modifying their classes. While iteration focuses on traversing elements, the Visitor focuses on performing operations on each element during traversal.

The key difference is that iteration provides access to elements, while the Visitor provides operations on elements. An iterator yields elements one by one; a visitor is called with each element and performs a specific operation. The Visitor pattern is particularly powerful with the Composite pattern: a visitor can traverse a tree structure and perform different operations based on the concrete type of each node.

The Visitor pattern supports the Open/Closed Principle: new operations can be added by creating new visitor classes without modifying the element classes. However, adding new element types requires modifying all visitor classes, which is a trade-off. The Visitor pattern is commonly used in compilers (AST traversal), document processing, and object structure traversal.

---

## Q33: How would you design a command history system with replay capability?

**A:** A command history system records every command executed, enabling replay (re-executing commands), undo, and redo. The history is typically a list or stack of executed commands, along with metadata like timestamps, user context, and input parameters.

For replay, the history stores the original command and its context, not just the state changes. When replaying, the system re-executes each command in sequence, potentially against a fresh state or a different context (e.g., replaying user actions against a different dataset for testing).

The implementation should handle non-deterministic commands (time-dependent operations, random numbers) by recording their seeds or timestamps. Versioning of command formats ensures that old command histories can still be replayed as the system evolves. For distributed systems, command histories may be stored in event stores or log-structured databases for durability and auditability.

---

## Q34: What are the performance characteristics of different iterator implementations?

**A:** Array-backed iterators have O(1) access time per element and excellent cache locality, making them the fastest for sequential traversal. Linked list iterators have O(1) per-step traversal but poor cache locality due to pointer chasing, resulting in higher constant factors.

Tree iterators (in-order, pre-order) require O(h) stack space for recursive traversal or explicit stack management, with O(1) amortized per-element cost. Graph iterators (BFS, DFS) require O(V) space for visited tracking and have O(V + E) total time complexity.

Lazy iterators and generators have minimal overhead per yield (function call + state suspension), typically 2-5x slower than direct array traversal but with significantly lower memory usage. For I/O-bound iterators (database cursors, file readers), the I/O latency dominates, making iterator overhead negligible.

---

## Q35: How does the Iterator pattern support functional programming paradigms?

**A:** The Iterator pattern bridges object-oriented and functional programming by providing the data source for functional operations like `map`, `filter`, `reduce`, and `flatMap`. Java Streams, Python generators, and C++ ranges all build on iterator abstractions.

In functional style, iterators are composed into pipelines where each transformation produces a new lazy iterator. This avoids intermediate data structures and enables fusion (combining multiple operations into a single pass). The iterator protocol's simplicity (`next()` + `hasNext()`) makes it a natural foundation for higher-order functions.

The key insight is that iterators provide a universal abstraction for "a sequence of values that can be consumed," which is the fundamental input to functional data processing. This enables a declarative programming style where the programmer specifies what operations to perform, and the iterator infrastructure determines the optimal execution strategy.

---

## Q36: What is a command processor and how does it differ from a simple command queue?

**A:** A command processor is a more sophisticated version of a command queue that adds lifecycle management, validation, routing, and monitoring. While a simple queue just stores and delivers commands, a processor can validate commands before execution, route them to appropriate handlers, track execution status, and provide metrics.

The processor may support command priorities, deadlines, retries with backoff, idempotency keys, and dead-letter queues for failed commands. It can also implement rate limiting, circuit breaking, and load balancing across multiple handler instances.

In enterprise systems, command processors are implemented as message brokers (Kafka consumers, RabbitMQ workers) or as application-level components in CQRS architectures. They are the backbone of scalable, resilient event-driven systems where commands must be processed reliably and in order.

---

## Q37: What are the trade-offs between pull and push models in the Observer pattern?

**A:** In the push model, the subject sends detailed event data to observers during notification. Observers receive all information about the change whether they need it or not. This is simpler but can be wasteful if observers only need a subset of the data.

In the pull model, the subject sends minimal notification data (typically just "something changed"), and observers query the subject for the specific data they need. This is more efficient in terms of notification bandwidth but requires observers to have a reference back to the subject and adds latency per observation.

The push model is better for real-time systems where latency matters and for distributed systems where round-trips are expensive. The pull model is better when different observers need different subsets of data, when the subject's state changes rapidly (observers can batch their queries), and when you want to minimize the subject's knowledge of what observers need.

---

## Q38: How do you implement an iterator for a concurrent data structure?

**A:** Iterating over concurrent data structures requires careful design to balance consistency and performance. The weakest consistency guarantee is weakly consistent: the iterator reflects the state of the collection at some point since its creation and may (but is not required to) reflect concurrent modifications.

Java's `ConcurrentHashMap` iterators are weakly consistent: they never throw `ConcurrentModificationException` and reflect a snapshot of the map. `CopyOnWriteArrayList` iterators traverse the array snapshot taken at creation time. `ConcurrentLinkedQueue` provides a traversal that may or may not reflect concurrent modifications.

The design choice depends on the consistency-performance trade-off. Strong consistency (snapshot isolation) requires copying, which has memory and time costs. Weak consistency is cheaper but may miss or duplicate elements. The iterator's contract must clearly document which guarantee it provides, as this affects the correctness of client code.

---

## Q39: What is the difference between a command and a transaction?

**A:** A command is a single, atomic operation encapsulated as an object. A transaction is a group of commands that must succeed or fail as a unit. Every transaction contains commands, but not every command is a transaction.

Transactions add the properties of ACID (Atomicity, Consistency, Isolation, Durability) to command execution. A single command can be wrapped in a transaction for durability guarantees. Multiple commands grouped in a transaction are atomic: if any fails, all are rolled back.

The Command pattern supports transactions naturally through macro commands and compensating commands. The transaction manager coordinates execution, validation, and rollback across multiple commands. In distributed systems, the saga pattern uses compensating commands to achieve transaction-like behavior across services without distributed locks.

---

## Q40: How would you implement a filterable iterator?

**A:** A filterable iterator wraps another iterator and applies a predicate to determine which elements to yield. It is a decorator that adds filtering behavior without modifying the underlying collection or iterator. The filter iterator only yields elements that match the predicate.

The implementation maintains an internal buffer of one element. On each call to `next()`, it advances the underlying iterator until it finds an element matching the predicate, then returns it. `hasNext()` checks whether a matching element exists in the buffer or can be found by advancing.

This is a lazy operation: elements are filtered on demand, not pre-computed. It composes naturally with other iterators (map, take, skip) to build complex data processing pipelines. The filter iterator is the foundation of the `filter()` operation in Stream APIs and generator-based pipelines.

**Example:**
```python
class FilterIterator:
    def __init__(self, iterator, predicate):
        self._iter = iterator
        self._pred = predicate
        self._next = None
        self._exhausted = False

    def _advance(self):
        while not self._exhausted:
            try:
                item = next(self._iter)
                if self._pred(item):
                    self._next = item
                    return
            except StopIteration:
                self._exhausted = True
                break
        self._next = None

    def __iter__(self):
        return self

    def __next__(self):
        self._advance()
        if self._next is None:
            raise StopIteration
        result = self._next
        self._next = None
        return result
```

---

## Q41: What is the mediator pattern and how does it differ from the Observer pattern?

**A:** The Mediator pattern centralizes complex communications between a set of objects into a single object. Unlike the Observer pattern where subjects notify observers directly, the Mediator coordinates interactions: when one object changes, it notifies the Mediator, and the Mediator decides which other objects to inform and how.

The Observer pattern is one-to-many (subject to observers), while the Mediator handles many-to-many relationships. The Mediator contains the interaction logic, making it explicit and centralized. This reduces the coupling between colleagues from O(n²) to O(n), since each colleague only knows the Mediator.

The trade-off is that the Mediator can become a complex "god object" if too many responsibilities accumulate. The Observer pattern distributes logic across observers, which is better when interactions are simple and independent. The Mediator is better when the interaction logic is complex, conditional, or involves coordination between multiple objects.

---

## Q42: What is the difference between an external iterator and a for-each loop?

**A:** A for-each loop is syntactic sugar for using an external iterator. In languages like Java, `for (Element e : collection)` is equivalent to creating an Iterator, calling `hasNext()` and `next()` in a loop. The for-each loop hides the iterator boilerplate.

The for-each loop is more concise and less error-prone (no risk of `ConcurrentModificationException` from manual `remove()` calls). However, it is less flexible: you cannot modify the collection during iteration, you cannot access the index, you cannot skip elements, and you cannot iterate over multiple collections simultaneously.

External iterators are necessary when you need fine-grained control over traversal: modifying elements, removing elements during iteration, parallel iteration over two collections, or implementing complex traversal algorithms. The for-each loop is preferred for simple consumption of elements.

---

## Q43: What is a command pattern with state and how does it enable undo for complex operations?

**A:** A command with state stores the before-and-after values needed for undo, rather than relying on the receiver to reverse the operation. This is essential for complex operations where the inverse is not straightforward (e.g., resizing an image, moving an object to arbitrary coordinates).

The command captures a snapshot of the relevant state before execution. After execution, it may capture the resulting state. The `undo()` method restores the pre-execution state. This approach is analogous to the Memento pattern but embedded within the command.

The advantage is that undo is always possible regardless of the operation's complexity. The disadvantage is memory overhead: each command stores state snapshots, which can be expensive for large objects. Strategies to mitigate this include differential storage (storing only changes), compression, and undo coalescing (merging related operations).

---

## Q44: What is event sourcing and how does it relate to the Command pattern?

**A:** Event sourcing is an architectural pattern where state changes are stored as an immutable sequence of events, rather than storing only the current state. The current state is derived by replaying events from the beginning (or from a snapshot). It is closely related to the Command pattern because commands are the input, and events are the output.

In event sourcing, a command is validated and, if valid, produces one or more events. Events are appended to an event store (an append-only log). The event store is the single source of truth. Projections (read models) are built by processing events, supporting different query patterns.

Event sourcing provides a complete audit trail, temporal queries (state at any point in time), the ability to replay and reprocess events, and natural support for distributed systems via event-driven architecture. The Command pattern's undo capability maps to appending compensating events rather than deleting original events.

---

## Q45: How do you implement an iterator for a graph with cycle detection?

**A:** Iterating over a graph with cycles requires tracking visited nodes to avoid infinite loops. The standard approach uses a `Set` or `boolean[]` to mark visited nodes. Before processing a node, check if it has been visited; if so, skip it.

For BFS (breadth-first search), use a queue and mark nodes as visited when they are enqueued (not when dequeued) to prevent duplicates. For DFS, use a stack or recursion with a visited set. Both approaches have O(V + E) time complexity and O(V) space complexity.

The iterator should handle disconnected graphs by maintaining a set of "start nodes" and initiating a new traversal from the next unvisited start node when the current component is exhausted. For weighted graphs or shortest-path traversal, a priority queue replaces the standard queue (Dijkstra's algorithm).

---

## Q46: What is the difference between a command and a message in distributed systems?

**A:** In distributed systems, commands and messages serve different roles. A command is a request to perform an action: it has a specific target, expects execution, and may fail. A message is a notification that something happened: it is broadcast, has no specific target, and represents a fact.

Commands are point-to-point (sent to a specific handler) and may be retried on failure. Messages are pub-sub (broadcast to all interested subscribers) and are typically not retried by the sender. Commands can be rejected (validation failure); messages are simply recorded.

In event-driven architectures, the distinction blurs: a command may trigger an event (message), and a message may trigger a command execution. The Command pattern maps naturally to command messages, while the Observer pattern maps to event subscriptions. Understanding the distinction is crucial for designing correct distributed systems.

---

## Q47: What is the role of immutability in the Observer pattern?

**A:** Immutability in the Observer pattern means that event objects passed to observers are immutable, preventing observers from accidentally modifying the event data. This is important for thread safety (immutable objects are inherently thread-safe), correctness (observers see a consistent view of the event), and debugging (events cannot be mutated after dispatch).

When the subject changes state and notifies observers, the event object should be a snapshot of the relevant state at the time of notification, not a reference to mutable state. This prevents race conditions where the subject modifies state while observers are still processing the event.

Immutability also simplifies testing and reasoning about the system: once an event is created, it never changes. This is particularly important in asynchronous systems where events may be processed out of order or on different threads.

---

## Q48: How do you implement a priority command queue?

**A:** A priority command queue orders commands by priority rather than insertion order. Commands with higher priority are dequeued and executed first, regardless of when they were submitted. The implementation typically uses a `PriorityQueue` (heap-based) or a sorted list.

Each command carries a priority value, and the queue's comparator orders commands by this value. For equal priority, FIFO ordering is used as a tiebreaker. The queue should support dynamic priority changes (reprioritizing a command after submission) by removing and re-inserting it.

Priority queues are essential in operating systems (process scheduling), UI frameworks (user input before background tasks), and real-time systems (safety-critical commands before routine maintenance). The trade-off is that insertion and deletion are O(log n) instead of O(1) for a simple queue.

**Example:**
```java
class PriorityCommandQueue {
    private final PriorityQueue<Command> queue =
        new PriorityQueue<>(Comparator.comparingInt(Command::getPriority).reversed());

    public void enqueue(Command cmd) { queue.add(cmd); }
    public Command dequeue() { return queue.poll(); }
    public boolean isEmpty() { return queue.isEmpty(); }
}
```

---

## Q49: What are the implications of the Observer pattern for memory management?

**A:** The Observer pattern creates references from the subject to its observers. If these are strong references, observers cannot be garbage collected as long as the subject exists, even if no other part of the program references them. This is a classic memory leak scenario, especially with long-lived subjects.

Solutions include: using weak references (Java's `WeakReference`, `WeakHashMap`), ensuring explicit unsubscription in destructors or close methods, using weak event libraries, and implementing subscription timeouts. Python's `weakref` module provides similar functionality.

The choice depends on the lifetime semantics: if an observer should remain alive as long as it is subscribed, strong references are correct. If an observer should be eligible for GC when nothing else references it, weak references are appropriate. Most UI frameworks use weak references for observer subscriptions to prevent memory leaks when views are destroyed.

---

## Q50: What is a dispatcher and how does it relate to the Observer pattern?

**A:** A dispatcher is a component that manages the delivery of events from subjects to observers. It sits between the subject and observers, handling routing, filtering, threading, and error handling. The dispatcher decouples event production from event consumption.

The dispatcher may implement synchronous dispatch (direct notification), asynchronous dispatch (queued notification on a separate thread), or hybrid dispatch (synchronous for local observers, asynchronous for remote ones). It may also handle event transformation, enrichment, and aggregation.

In modern frameworks, the dispatcher often provides features like event filtering (only deliver events matching certain criteria), handler groups (subscribe to multiple events at once), lifecycle management (auto-unsubscribe on component destruction), and debugging support (event tracing and logging). The dispatcher is the evolution of simple subject notification into a full-fledged event delivery infrastructure.


## Q51: How do you implement a command pattern with serialization for audit logging?

**A:** Serialization of commands enables persisting them to disk, transmitting them over a network, and replaying them later for audit or debugging. Each command must implement serialization, capturing all data needed to reconstruct and re-execute the command.

The serialized form should include the command type, all parameters, the receiver reference (or enough information to reconstruct it), and metadata like timestamp, user context, and sequence number. JSON, Protocol Buffers, or custom binary formats can be used depending on the requirements.

The challenge is handling receiver references: in a serialized form, you cannot store a direct object reference. Instead, store a repository path, database key, or URI that can be resolved during deserialization. For commands with complex state, consider using the Memento pattern to serialize the state directly, avoiding the need to reconstruct the receiver.

---

## Q52: What is the difference between a pull-based and push-based reactive stream?

**A:** In a push-based reactive stream, the producer pushes data to the consumer as fast as it can produce it. The consumer has no control over the rate of data delivery, which can lead to buffer overflows or dropped data if the consumer is slower than the producer.

In a pull-based (backpressure-aware) reactive stream, the consumer signals demand to the producer. The producer only produces as much data as the consumer has requested. This is the model adopted by Reactive Streams, ReactiveX, and Project Reactor.

The pull model provides flow control and prevents resource exhaustion. It is essential in systems with variable production and consumption rates, such as network I/O, database streaming, and real-time analytics. The push model is simpler but requires the consumer to handle overflow, typically via bounded buffers and drop policies.

**Example:**
```java
// Java Reactive Streams with backpressure
Flux.range(1, 1000)
    .onBackpressureBuffer(256)
    .flatMap(i -> slowService.process(i))
    .subscribe(result -> store(result));
```

---

## Q53: How do you implement a command pattern with idempotency?

**A:** Idempotency means that executing a command multiple times has the same effect as executing it once. This is critical in distributed systems where network failures may cause retries. An idempotent command detects duplicate executions and returns the previously computed result.

The implementation uses an idempotency key (typically a UUID or hash of the command parameters) stored in a cache or database. Before executing, the command checks if the key exists. If it does, the cached result is returned. If not, the command executes, stores the result with the key, and returns it.

Commands that are inherently idempotent (setting a value, deleting a specific record) need no special handling. Commands that are not inherently idempotent (incrementing a counter, appending to a log) must be designed to be idempotent by using natural keys (set counter to 5, not increment by 1) or by tracking processed operations.

---

## Q54: What is the difference between a state machine and a command processor?

**A:** A state machine defines a set of states, transitions between them, and the events that trigger transitions. A command processor manages the execution of commands, including queuing, dispatching, and result handling.

The state machine is declarative: it defines what transitions are valid and what happens during each transition. The command processor is procedural: it manages the lifecycle of command execution. The state machine can be implemented as a command processor where each command triggers a state transition.

In practice, they are complementary: a command processor often uses a state machine to track the lifecycle of each command (pending, executing, completed, failed). The state machine ensures that commands transition through valid states, while the command processor manages the mechanics of execution.

---

## Q55: How would you implement a distributed command pattern with event sourcing?

**A:** In a distributed command pattern with event sourcing, commands are sent to a command handler (possibly on a remote service), which validates and converts them into events. Events are appended to an event store (like Kafka or EventStore) and consumed by projections to update read models.

The command handler must be idempotent (handling duplicate commands from retries), and events must be immutable and ordered (using sequence numbers or timestamps). The event store provides durability and auditability. Projections can be rebuilt from the event store in case of errors.

The key design decisions are: how to partition commands (by aggregate ID for ordering guarantees), how to handle concurrent commands on the same aggregate (optimistic concurrency with version checks), and how to manage eventual consistency between write and read models. The Saga pattern coordinates commands across multiple services.

---

## Q56: What is the difference between a generator and a coroutine in the context of iteration?

**A:** A generator is a function that yields values lazily, maintaining its execution state between yields. It is a simple form of coroutine used primarily for producing sequences. A coroutine is a more general construct that can both yield and receive values, enabling two-way communication.

In Python, generators (using `yield`) produce values. Coroutines (using `yield` on the receiving end, or using `async/await`) can receive values via `send()`, enabling bidirectional data flow. Generators are input-only; coroutines are input-and-output.

For iteration purposes, generators are sufficient for most use cases (lazy sequences, pipeline processing). Coroutines are needed when the iterator must interact with its consumer (e.g., filtering based on consumer feedback, adaptive sampling, cooperative multitasking). The `async/await` syntax in modern languages provides coroutine-based iteration for asynchronous data sources.

---

## Q57: How do you handle command ordering in a distributed system?

**A:** Command ordering in distributed systems requires careful design because messages may arrive out of order due to network delays, retries, or partitioning. Strategies include: sequence numbers (each command carries a monotonically increasing sequence), timestamps (with clock synchronization via NTP), and partitioning (commands for the same aggregate are routed to the same partition, preserving order within a partition).

For strict total ordering across all commands, a consensus algorithm (Paxos, Raft) is required, which limits scalability. For per-aggregate ordering (common in event sourcing), partitioning by aggregate ID provides ordering guarantees without global consensus.

The trade-off is between ordering guarantees and throughput. Strong ordering limits parallelism because commands must be processed sequentially. Relaxed ordering (per-aggregate or per-partition) allows parallel processing across different aggregates while maintaining consistency within each aggregate.

---

## Q58: What is the CQRS pattern and how does it relate to Command and Observer?

**A:** CQRS (Command Query Responsibility Segregation) separates the write model (commands) from the read model (queries). Commands modify state through a domain model; queries read from a denormalized, optimized read model. The Observer pattern (via events) synchronizes the write and read models.

The write side uses the Command pattern: commands are validated, executed against the domain model, and produce events. The read side uses the Observer pattern: it subscribes to events and updates its denormalized views accordingly. This separation allows each side to be optimized independently.

CQRS is particularly valuable in systems with different read and write patterns (high read throughput, complex queries, real-time analytics). It enables scalable, performant systems but adds complexity and requires managing eventual consistency between write and read models.

---

## Q59: How do you implement an iterator for a lazy, infinite data structure?

**A:** Iterating over an infinite data structure (like the natural numbers, Fibonacci sequence, or a random number generator) requires a lazy iterator that produces values on demand. The iterator never signals exhaustion (or signals it only when a computational limit is reached).

The implementation must be careful about resource consumption: an infinite iterator should not pre-compute values, and it should support early termination (via `take(n)` or similar). In Python, generators naturally handle this: `count()` yields indefinitely, and `islice()` provides finite extraction.

The key design decision is how to represent "infinite" in a finite system: the iterator is conceptually infinite but practically bounded by the amount of data the consumer requests. The iterator itself should not enforce a limit; the consumer controls how many values to consume.

**Example:**
```python
def primes():
    """Infinite prime number generator"""
    yield 2
    composites = {}
    n = 3
    while True:
        if n not in composites:
            yield n
            composites[n * n] = [n]
        else:
            for p in composites[n]:
                composites.setdefault(n + 2 * p, []).append(p)
            del composites[n]
        n += 2

from itertools import islice
first_100_primes = list(islice(primes(), 100))
```

---

## Q60: What is the difference between a command handler and a command executor?

**A:** A command handler is responsible for validating and processing a specific type of command. It contains the business logic that determines whether a command can be executed and what effects it produces. Multiple handlers may exist for different command types.

A command executor is a generic component that dispatches commands to the appropriate handler, manages the execution lifecycle (scheduling, retries, timeouts), and handles cross-cutting concerns (logging, metrics, transaction management). The executor is the infrastructure; the handler is the business logic.

The separation allows handlers to focus on domain logic without worrying about infrastructure concerns. The executor provides a uniform execution environment for all handlers, ensuring consistent behavior for retries, monitoring, and error handling. This is the pattern used in frameworks like Axon, MassTransit, and MediatR.

---

## Q61: How would you implement a command pattern for a distributed saga?

**A:** A distributed saga coordinates a series of commands across multiple services, with compensating transactions for rollback. Each step in the saga is a command sent to a service, and if any step fails, compensating commands are executed in reverse order to undo previous steps.

The saga orchestrator maintains the saga state (current step, completed steps, compensation data). Each command handler returns success or failure. On success, the orchestrator proceeds to the next step. On failure, it triggers compensating commands for all completed steps.

Implementations include choreography (each service publishes events that trigger the next step) and orchestration (a central saga orchestrator coordinates all steps). Orchestration is simpler to understand and debug; choreography is more decoupled but harder to trace. The Command pattern provides the command and compensating command objects for each step.

---

## Q62: What is the difference between a hot and cold iterator?

**A:** A cold iterator starts producing values when `next()` is first called. Each time the iterator is recreated, it starts from the beginning. Python generators and Java Streams are cold: they re-execute the computation from scratch on each traversal.

A hot iterator begins producing values as soon as it is created, regardless of whether anyone is consuming them. Live event streams, sensor data feeds, and real-time data sources are hot: they produce data continuously, and a consumer that starts late misses earlier values.

The distinction affects caching, replayability, and resource management. Cold iterators are idempotent and can be replayed. Hot iterators may require buffering for late consumers and careful resource management to stop production when no one is listening. The choice depends on whether the data source is reproducible (cold) or ephemeral (hot).

---

## Q63: How do you handle cross-cutting concerns in the Command pattern?

**A:** Cross-cutting concerns (logging, authentication, authorization, transaction management, metrics) affect multiple commands but are not part of the core command logic. The Command pattern handles these through decorators, interceptors, or middleware.

A command decorator wraps a command with additional behavior: the logging decorator logs execution before and after, the authorization decorator checks permissions, and the transaction decorator manages a transaction boundary. The decorator implements the same command interface, so the invoker does not know about the cross-cutting logic.

In middleware-based systems (like Express.js, ASP.NET, or Axon), commands pass through a pipeline of middleware components. Each middleware can modify, reject, or pass through the command. This is a more flexible approach than decorators because middleware can be configured globally or per command type.

**Example:**
```java
class LoggingDecorator implements Command {
    private final Command delegate;

    LoggingDecorator(Command delegate) { this.delegate = delegate; }

    public void execute() {
        long start = System.currentTimeMillis();
        try {
            delegate.execute();
            log("Executed in {}ms", System.currentTimeMillis() - start);
        } catch (Exception e) {
            log("Failed after {}ms: {}", System.currentTimeMillis() - start, e);
            throw e;
        }
    }

    public void undo() { delegate.undo(); }
}
```

---

## Q64: What is the difference between a publish-subscribe system and a message queue?

**A:** A publish-subscribe system broadcasts messages to all subscribers. Each subscriber receives every message. There is no concept of message consumption: subscribers independently process the same message. This is the Observer pattern scaled to distributed systems.

A message queue delivers each message to exactly one consumer (or consumer group). Messages are removed from the queue after consumption. This provides load balancing: multiple consumers can process messages from the same queue in parallel.

Pub-sub is better for broadcasting (real-time feeds, notifications, event distribution). Message queues are better for task distribution (work queues, job processing, load balancing). Many systems combine both: a message queue for command processing and pub-sub for event notification. Apache Kafka blurs the line by providing pub-sub semantics with consumer group load balancing.

---

## Q65: How do you test command undo/redo functionality thoroughly?

**A:** Testing undo/redo requires verifying that each command's undo restores the exact pre-execution state, and that redo re-applies the command correctly. Test strategies include: state snapshot comparison (capture state before and after undo), property-based testing (random commands applied and undone should return to the initial state), and sequential testing (execute, undo, undo again should be a no-op).

Test edge cases: undo a macro command (all sub-commands undone in reverse order), undo after the state has been externally modified (should detect inconsistency), redo after a new command is executed (redo stack should be cleared), and undo in a concurrent environment (thread safety of undo state).

Use a test harness that automates command execution and undo: generate random command sequences, apply them, undo them all, and verify the state matches the initial state. This property-based approach catches bugs that hand-written tests miss.

---

## Q66: What is the difference between a flyweight and a command in terms of object reuse?

**A:** The Flyweight pattern shares common state across many objects to reduce memory usage. The Command pattern creates command objects for each operation. They serve different purposes but can interact.

A flyweight command pattern shares the immutable, common parts of commands across instances, while allowing the varying parts (parameters, receiver) to be external. For example, in a text editor, a "format" command shares the format specification (font, size, color) across many instances, with only the target text range varying.

The flyweight optimization is relevant when commands are created in large numbers with significant shared state. Command parameters can be externalized, and the command object itself can be shared. This reduces GC pressure and memory usage in high-throughput command processing systems.

---

## Q67: How would you implement a versioned command system for API evolution?

**A:** A versioned command system handles backward compatibility as commands evolve over time. Each command version includes a version number, and handlers can process multiple versions. This allows old clients to send old commands while new clients send new versions.

The implementation includes: a version registry mapping versions to handlers, a command upgrader that transforms old commands to the latest version, and a version negotiation protocol. The upgradability ensures that old commands can be processed without maintaining old handlers indefinitely.

In event-sourced systems, versioning is critical because events are immutable and must be processable forever. Event upcasting transforms old event formats into new ones during replay. The Command pattern supports this by making command serialization version-aware and providing upgraders for each version transition.

---

## Q68: What is the difference between a synchronous and asynchronous command bus?

**A:** A synchronous command bus executes the command handler in the same thread as the caller. The caller blocks until the command is processed and receives the result directly. This is simple and provides immediate feedback but can block the caller during slow operations.

An asynchronous command bus dispatches the command to a handler on a separate thread or message queue. The caller receives a future, promise, or correlation ID immediately and can continue processing. The result is delivered later via callback, polling, or message.

Asynchronous buses are essential for UI responsiveness (don't block the UI thread), scalability (handle more requests by not blocking threads), and reliability (the command is persisted in a queue even if the handler crashes). The trade-off is complexity in result handling, error propagation, and debugging.

---

## Q69: How do you implement an iterator for a binary search tree with parent pointers?

**A:** An iterator for a BST with parent pointers can traverse in-order without requiring a stack. The algorithm starts at the leftmost node (smallest element) and uses parent pointers to navigate back up the tree.

To find the next element: if the current node has a right subtree, the next element is the leftmost node in the right subtree. If not, the iterator moves up via parent pointers until it finds a node that is the left child of its parent; that parent is the next element.

Without parent pointers, an explicit stack is needed to track the path from root to current node. The stack-based approach uses O(h) space, where h is the tree height. The parent pointer approach uses O(1) additional space but requires parent pointers in the node structure.

**Example:**
```python
class BSTIterator:
    def __init__(self, root):
        self.current = root
        while self.current and self.current.left:
            self.current = self.current.left

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        result = self.current.value
        if self.current.right:
            self.current = self.current.right
            while self.current.left:
                self.current = self.current.left
        else:
            while self.current.parent and self.current.parent.right is self.current:
                self.current = self.current.parent
            self.current = self.current.parent
        return result
```

---

## Q70: What is the role of idempotency in command processing?

**A:** Idempotency ensures that executing a command multiple times produces the same result as executing it once. This is critical in distributed systems where network failures may cause retries, and in UI systems where double-clicks may trigger duplicate commands.

Implementing idempotency requires: a unique idempotency key per logical command, a cache or store of processed keys and their results, and a mechanism to detect and return cached results for duplicate keys. The idempotency key is typically derived from the command parameters and a client-generated UUID.

Commands that are naturally idempotent (set a value to X, delete record with ID Y) need no special handling. Commands that are not naturally idempotent (increment by 1, append to a list) must be redesigned: use set-to-value instead of increment, or use a transaction log with idempotency checks.

---

## Q71: What is the difference between a command and an action in reactive programming?

**A:** In reactive programming, an action is a side effect that occurs in response to a change in state or an event. A command is a request to perform an operation that may or may not succeed. Actions are part of the reactive data flow; commands are external inputs to the system.

In reactive frameworks (Redux, MobX, Vue), actions describe what happened (user clicked, data loaded), and reducers (pure functions) determine how state changes. Commands in this context are the triggers that create actions. The distinction is that actions are facts (immutable, past tense), while commands are requests (may be rejected).

The reactive approach emphasizes unidirectional data flow: commands trigger actions, actions are processed by reducers, reducers produce new state, and state changes are observed by views. This cycle is the Observer pattern formalized into a state management architecture.

---

## Q72: How do you implement a command pattern with dependency injection?

**A:** Dependency injection (DI) in the Command pattern provides command handlers with their dependencies (repositories, services, external APIs) through constructor injection, setter injection, or field injection. This makes commands testable (inject mocks) and flexible (swap implementations).

A DI container manages the lifecycle of command handlers, resolving their dependencies automatically. When a command is dispatched, the container creates or retrieves the appropriate handler with all dependencies injected. This separates command definition from dependency resolution.

The implementation uses a registry or container that maps command types to handler types. When a command is dispatched, the container resolves the handler, injects dependencies, and invokes it. This approach is used in frameworks like Axon (Spring DI), MediatR (ASP.NET DI), and custom command buses.

---

## Q73: What is the difference between a pull iterator and a push iterator?

**A:** A pull iterator is controlled by the consumer: the consumer calls `next()` to request the next element. The producer only produces when asked. This is the traditional iterator model (Java Iterator, Python generator).

A push iterator is controlled by the producer: the producer pushes elements to a consumer callback as they become available. The consumer provides a callback function, and the producer invokes it for each element. This is the model used in reactive streams and callback-based APIs.

Pull iterators are simpler and give the consumer control over pacing. Push iterators are better for event-driven scenarios where the producer determines when data is available (I/O completion, user input, real-time data). The pull model can be implemented on top of the push model using a buffer, and vice versa using a trampoline or scheduler.

---

## Q74: How do you implement a command pattern for undo in a collaborative editing system?

**A:** Collaborative editing systems use Operational Transformation (OT) or Conflict-free Replicated Data Types (CRDTs) to handle concurrent edits. Undo in this context requires transforming the undo operation against concurrent operations that have occurred since the original command.

In OT-based systems, when a user undoes an operation, the undo operation must be transformed against all operations that occurred after the original operation. This ensures that the undo produces the correct result even if other users have modified the document.

In CRDT-based systems, operations are commutative and idempotent, so undo is implemented as a "tombstone" or compensating operation that is merged with other concurrent operations. The challenge is providing intuitive undo semantics (undoing your own changes without affecting others' changes) in a distributed, concurrent environment.

---

## Q75: What is the difference between an iterator and a stream?

**A:** An iterator is a pull-based abstraction: the consumer pulls elements one at a time. A stream is a higher-level abstraction that can operate in both pull and push modes, supports lazy intermediate operations (map, filter, reduce), and may support parallel execution.

Streams provide a fluent API for composing data processing pipelines: `stream.filter(x -> x > 0).map(x -> x * 2).collect(toList())`. Each intermediate operation returns a new stream; the terminal operation triggers the actual computation. This is syntactically and semantically richer than manual iterator manipulation.

The key differences: streams support parallel execution (parallel stream in Java), streams are typically single-use (like generators), streams may optimize the pipeline (fusion, short-circuiting), and streams provide a richer set of operations (flatMap, reduce, collect). Iterators are more fundamental and flexible for custom traversal patterns.


## Q76: How would you design a fault-tolerant event bus for a distributed microservices architecture?

**A:** A fault-tolerant event bus in a distributed architecture must handle service failures, network partitions, message loss, and ordering guarantees. The design uses a durable message broker (Kafka, RabbitMQ, or NATS) as the backbone, with each service connecting as a producer or consumer.

Key design elements: persistent message storage (survive broker restarts), consumer group load balancing (horizontal scaling), dead letter queues (handle poison messages), idempotent consumers (handle duplicate delivery), and exactly-once semantics (using transactional outbox or idempotent producers).

The bus must handle backpressure: slow consumers should not block producers. Kafka handles this with partition-based consumption and consumer lag monitoring. Circuit breakers prevent cascading failures when downstream services are unavailable. Retry policies with exponential backoff handle transient failures. The event bus should be deployed across multiple availability zones for resilience.

---

## Q77: What are the memory model implications of the Observer pattern in concurrent environments?

**A:** In concurrent environments, the Observer pattern must consider the Java Memory Model (JMM) or equivalent memory models. Without proper synchronization, observer notification may see stale data due to CPU caching and instruction reordering.

The subject's state must be published safely to observers. This requires either synchronization, volatile fields, or atomic references. Without a happens-before relationship between the state change and observer notification, observers may see inconsistent or partially updated state.

The publication of the observer list itself must be thread-safe. If observers are added or removed while notification is in progress, the iterator may fail or miss observers. Solutions include snapshot iteration (copy the observer list before notification), immutable observer lists (copy-on-write), or read-write locks.

The practical impact: in high-frequency event systems, improper memory synchronization causes hard-to-reproduce bugs that appear only under load. Profiling tools and formal verification (model checking) are sometimes necessary to identify these issues.

---

## Q78: How do you implement a saga pattern using the Command pattern for distributed transactions?

**A:** The saga pattern breaks a distributed transaction into a sequence of local transactions, each with a compensating action. Using the Command pattern, each step is a command object with an `execute()` method and a compensating `undo()` method.

The saga orchestrator maintains the saga definition (ordered list of commands and their compensations) and the saga state (current step, completed steps). It executes each command sequentially. If a command fails, it triggers compensating commands for all completed steps in reverse order.

The implementation must handle: timeout (a command that takes too long), concurrency (other sagas running simultaneously), and durability (saga state must survive orchestrator crashes). The orchestrator stores saga state in a durable store, and each command execution is logged. For choreography-based sagas, each service publishes events that trigger the next step, eliminating the central orchestrator.

---

## Q79: What is the difference between a cold and hot command bus, and when would you use each?

**A:** A cold command bus processes commands synchronously in the caller's thread. It is suitable for low-latency, request-response scenarios where the caller needs immediate feedback and the processing time is bounded and short.

A hot command bus dispatches commands asynchronously to a queue or thread pool. The caller receives a future or correlation ID and continues processing. The result is delivered asynchronously. This is suitable for long-running operations, high-throughput systems, and scenarios where the caller should not block.

Hybrid approaches exist: the bus may be synchronous for simple commands and asynchronous for commands flagged as long-running. The choice depends on the latency budget, throughput requirements, and fault tolerance needs. Hot buses are essential for building responsive UIs, scalable backends, and resilient distributed systems.

---

## Q80: How do you handle the celebrity problem in the Observer pattern?

**A:** The "celebrity problem" occurs when a subject has thousands or millions of observers. Notifying all observers synchronously is prohibitively expensive. Solutions include: batching notifications, using a message queue for asynchronous delivery, filtering notifications (only notify observers whose interests match the event), and prioritizing notifications.

Batching collects multiple state changes and notifies observers once with a summary, reducing notification frequency. Filtering uses a topic-based subscription model where observers only receive events they care about. Asynchronous delivery moves notification to a separate thread, preventing the subject's critical path from being blocked.

In real-world systems (social media feeds, stock tickers, IoT sensor networks), the subject rarely notifies all observers directly. Instead, it publishes events to a broker, and the broker handles fan-out. This shifts the scalability problem to the broker, which is designed for high-throughput event distribution.

---

## Q81: What is the difference between a saga orchestrator and a saga choreographer?

**A:** A saga orchestrator is a central component that controls the execution order of saga steps. It explicitly defines the workflow, sends commands to services, and handles compensations on failure. The logic is centralized and easy to understand, test, and modify.

A saga choreographer distributes the workflow logic across services. Each service, after completing its step, publishes an event that triggers the next service. There is no central coordinator; the workflow emerges from the event interactions. This is more decoupled but harder to trace and debug.

The orchestration approach is better for complex workflows, clear error handling, and visibility. The choreography approach is better for simple workflows, loose coupling, and avoiding a single point of failure. In practice, many systems use a hybrid: orchestration for the core workflow and choreography for peripheral concerns.

---

## Q82: How do you implement a command pattern with event storming for domain modeling?

**A:** Event storming is a workshop technique for discovering domain events, commands, aggregates, and policies. The Command pattern maps directly to the "command" in event storming: each command represents an intent to change state, and each command produces one or more domain events.

The implementation translates event storming artifacts into code: commands become command classes, events become event classes, aggregates become the receivers of commands, and policies become event handlers that trigger subsequent commands. The aggregate's `handle()` method receives the command, validates it, and emits events.

This approach ensures that the code reflects the domain model discovered during event storming. Commands and events become the primary abstractions, with aggregates encapsulating business rules. The resulting system is event-sourced, with a clear audit trail and the ability to rebuild state from events.

---

## Q83: What is the difference between a bounded and unbounded iterator, and why does it matter for resource management?

**A:** A bounded iterator has a finite number of elements. An unbounded iterator may produce elements indefinitely (infinite sequences, real-time data streams, infinite lazy generators). The distinction is critical for resource management.

Unbounded iterators require explicit termination mechanisms: `take(n)`, `timeout()`, or external cancellation. Without these, consuming an unbounded iterator will run forever, consuming memory (for buffered values) or CPU (for computation). In server applications, unbounded iterators can cause resource exhaustion.

The design principle is: always provide a way to bound unbounded iteration. In functional pipelines, use `limit()` or `take()`. In event-driven systems, use cancellation tokens or timeouts. In generators, ensure the generation logic has a natural termination condition or accept a limit parameter.

---

## Q84: How would you implement a multi-level undo system for a complex application?

**A:** A multi-level undo system supports undoing multiple operations, grouping related operations, and providing undo granularity at different levels (atomic operation, logical unit, session-level). The implementation uses a stack of command groups, where each group contains related commands.

The undo manager maintains a stack of "undoable groups." Each group contains one or more commands that should be undone together. When the user performs "undo," the top group is undone atomically. This allows grouping related operations (e.g., "format paragraph" may contain multiple atomic formatting commands).

The design must handle: undo across sessions (persistent undo history), undo with concurrent modifications (detect and warn), undo granularity selection (let the user choose the undo level), and undo preview (show what will be undone before executing). The Command pattern with macro commands provides the foundation, while the undo manager adds the grouping and lifecycle management.

---

## Q85: What is the difference between a reactive stream and an iterator in terms of backpressure?

**A:** Backpressure is the mechanism by which a slow consumer can signal a fast producer to slow down. Reactive streams have built-in backpressure support via the `Subscription.request(n)` protocol. Iterators do not have native backpressure; the consumer simply calls `next()` when ready.

In an iterator, the producer computes values on demand (pull model), so there is no need for backpressure: the consumer controls the pace. In a push-based system (without backpressure), the producer can overwhelm the consumer. Reactive streams solve this by having the consumer signal demand, and the producer only produces up to that amount.

The practical difference: iterators are safe for pull-based data sources, but push-based data sources (network streams, message queues, real-time feeds) require reactive streams with backpressure to prevent memory overflow and ensure system stability.

---

## Q86: How do you implement a command pattern with audit trail for compliance?

**A:** An audit trail for compliance (SOX, HIPAA, GDPR) requires recording every command executed, including who executed it, when, what parameters were used, and what the result was. The command pattern naturally supports this through decorators or interceptors.

An audit decorator wraps each command, recording execution metadata to an immutable audit log before and after execution. The audit record includes: command type, parameters, executing user, timestamp, execution result (success/failure), and the resulting state change (or its hash for privacy).

The audit log must be append-only and tamper-evident (hash chaining or blockchain-like structure). For GDPR compliance, the audit trail must support data retention policies and right-to-erasure (selective deletion of audit records, or pseudonymization). The Command pattern's encapsulation makes it straightforward to add audit logging without modifying individual command implementations.

---

## Q87: What is the difference between a synchronous iterator and an asynchronous iterator?

**A:** A synchronous iterator produces values immediately when `next()` is called. The caller blocks until the value is available. This is the standard iterator model used in most synchronous code.

An asynchronous iterator produces values that may not be immediately available. The `next()` call returns a promise or future that resolves when the value is ready. This is essential for I/O-bound iteration (reading files, network requests, database queries) where values arrive after a delay.

In Python, `async for` with `__aiter__` and `__anext__` provides asynchronous iteration. In JavaScript, `for await...of` iterates over async iterables. The key difference is that asynchronous iterators allow the event loop to process other work while waiting for the next value, enabling non-blocking concurrent execution.

---

## Q88: How would you design a command pattern for a workflow engine?

**A:** A workflow engine executes a sequence of commands (activities) with branching, parallel execution, error handling, and human interaction points. The Command pattern provides the activity abstraction: each activity is a command with `execute()`, `compensate()`, and `validate()` methods.

The workflow engine manages: activity execution order (sequential, parallel, conditional), state persistence (survive engine restarts), timeout handling (cancel long-running activities), retry policies (automatic retry on failure), and compensation (undo completed activities on failure).

The implementation uses a workflow definition (typically a DSL or configuration file) that specifies the activity graph. The engine parses the definition, creates command objects for each activity, and executes them according to the graph structure. The engine stores workflow state in a durable store and uses event sourcing for replay and audit.

---

## Q89: What is the difference between a lazy iterator and a cached iterator?

**A:** A lazy iterator computes each value on demand. No value is computed until `next()` is called, and values are not stored after being yielded. This is memory-efficient but means re-iteration requires recomputation.

A cached iterator (or memoizing iterator) stores previously computed values. On subsequent iterations, cached values are returned without recomputation. This trades memory for computation time and enables multiple passes over the same data.

The choice depends on the cost of computation vs. memory, and whether the data source is reproducible. Expensive computations (API calls, complex calculations) benefit from caching. Large datasets with sufficient memory benefit from caching for multiple-pass algorithms. Reproducible data sources (generators, database queries) may not need caching if single-pass processing is sufficient.

---

## Q90: How do you handle error propagation in a chain of command objects?

**A:** Error propagation in a chain of commands depends on the execution model. In a simple sequential chain, an exception in one command stops execution and propagates to the caller. The caller must decide whether to retry, compensate, or abort.

In a macro command or saga, error propagation triggers compensation: the failed command's `compensate()` is called, followed by compensations for all previously executed commands in reverse order. The error is logged but may not propagate to the caller (the macro command handles rollback internally).

In asynchronous command processing, errors are captured in the result object (success/failure) rather than thrown as exceptions. The error handling logic is in the result processor, not in the command itself. This separation allows different error handling strategies for different command types without modifying the commands.

---

## Q91: What is the difference between a command pattern and a strategy pattern?

**A:** The Command pattern encapsulates an action (request) as an object, supporting undo, queuing, and logging. The Strategy pattern encapsulates an algorithm as an object, allowing it to be swapped at runtime. They are structurally similar but semantically different.

Commands are about "what to do" (actions, operations, requests). Strategies are about "how to do" (algorithms, policies, approaches). A command is typically executed once and may be undone. A strategy is typically used repeatedly and may be changed based on context.

In practice, they are often combined: a command may use a strategy for its execution algorithm, or a strategy may be implemented as a command for undo support. The distinction matters for intent: if you are modeling an operation with undo/redo, use Command. If you are modeling a swappable algorithm, use Strategy.

---

## Q92: How do you implement a distributed iterator for partitioned data?

**A:** A distributed iterator for partitioned data traverses elements spread across multiple nodes or partitions. Each partition has its own local iterator, and the distributed iterator coordinates traversal across all partitions.

The design must handle: partition discovery (finding all partitions), partition assignment (which partitions this iterator is responsible for), fault tolerance (handling partition failures during iteration), ordering (maintaining global order across partitions), and load balancing (distributing partitions across iterator instances).

For ordered iteration across partitions, the distributed iterator uses a merge-sort approach: each local iterator produces a sorted stream, and the distributed iterator merges them using a priority queue. For unordered iteration, each partition is consumed independently, enabling parallel processing. The iterator must handle dynamic partition addition/removal during iteration.

---

## Q93: What is the difference between a command bus and a message broker?

**A:** A command bus is an in-process component that dispatches command objects to handlers within the same application. It is typically synchronous, in-memory, and fast. It provides a decoupling layer between the caller and the handler.

A message broker is a distributed infrastructure component that routes messages between processes, services, or applications. It is typically asynchronous, durable, and supports features like persistence, replication, and consumer groups.

The command bus is used for intra-service communication; the message broker is used for inter-service communication. Some systems bridge the two: a command bus within a service dispatches to handlers, and for cross-service commands, the command is serialized and sent through a message broker. This provides a uniform command interface regardless of whether the handler is local or remote.

---

## Q94: How would you implement a command pattern for a real-time bidding system?

**A:** A real-time bidding system requires ultra-low latency (sub-millisecond), high throughput (millions of bids per second), and exactly-once semantics. The Command pattern encapsulates each bid as a command object with validation, execution, and audit capabilities.

The implementation uses: pre-allocated command objects (to avoid GC pauses), lock-free data structures (for concurrent bid processing), direct memory access (for serialization efficiency), and hardware timestamping (for audit precision). Commands are validated against bidding rules before execution, and results are returned within the latency budget.

The architecture uses a command processor with a dedicated thread per CPU core, avoiding context switches and cache pollution. Commands are batched for throughput and prioritized by bid value. The audit trail is asynchronous and durable, ensuring compliance without impacting latency. The Command pattern's encapsulation allows the bidding logic to be tested independently of the infrastructure.

---

## Q95: What is the difference between a command interceptor and a command decorator?

**A:** A command decorator wraps a single command with additional behavior. It implements the same command interface and delegates to the wrapped command. Decorators are applied per-command and are visible in the command's construction.

A command interceptor is a cross-cutting component that applies behavior to all commands matching certain criteria. Interceptors are configured centrally (globally or per command type) and are transparent to the command itself. They are similar to aspect-oriented programming (AOP) concepts.

The key difference is in application scope: decorators are applied explicitly to individual commands, while interceptors are applied based on rules or patterns. Interceptors are better for cross-cutting concerns (logging, security, metrics), while decorators are better for command-specific enhancements (retry, timeout, fallback). Some frameworks use both: decorators for per-command customization and interceptors for global policies.

---

## Q96: How do you implement an iterator for a persistent data structure?

**A:** A persistent data structure preserves its previous versions when modified. Iterating over a persistent data structure requires an iterator that reflects the state of the structure at the time the iterator was created, even if the structure is modified afterward.

The iterator captures a reference to the root of the persistent data structure's version. As the structure is modified, new versions are created, but the iterator continues to traverse the original version. This is a natural consequence of persistence: the old version still exists and the iterator traverses it.

In Clojure, persistent vectors and maps are iterated using their internal tree structure, which is shared across versions. In Scala, persistent collections provide iterators that traverse the current version. The iterator itself may be mutable (tracking position) or immutable (returning a new iterator on each `next()`).

---

## Q97: What is the difference between a command query and a command mutation?

**A:** In CQRS and event sourcing, a command query retrieves data without modifying state, while a command mutation modifies state. The distinction matters for consistency, performance, and audit.

Command queries can be served directly from the read model (denormalized views) without going through the domain model. They are fast, scalable, and can be cached. Command mutations must go through the domain model for validation, business rule enforcement, and event production. They are slower but ensure consistency.

The separation allows each to be optimized independently: queries can use simple, fast data access patterns, while mutations use the full domain model with validation and event sourcing. This is the core insight of CQRS: read and write workloads have different characteristics and benefit from different optimization strategies.

---

## Q98: How do you implement a command pattern with rate limiting?

**A:** Rate limiting in the Command pattern restricts the rate at which commands can be executed. This protects downstream systems from overload and ensures fair resource allocation across consumers.

The implementation uses a token bucket or sliding window algorithm. Before executing a command, the rate limiter checks if a token is available. If not, the command is queued, rejected, or delayed. The rate limiter can be per-command-type, per-user, or global.

In distributed systems, rate limiting requires coordination across nodes. A centralized rate limiter (Redis-based) provides global limits but adds latency. Distributed rate limiting algorithms (token bucket with distributed counters) provide per-node limits with global coordination. The command pattern integrates naturally: the rate limiter is a decorator or interceptor that wraps command execution.

---

## Q99: What is the difference between a command pattern and a task pattern in concurrent programming?

**A:** The Command pattern encapsulates an operation as an object, primarily for structural purposes (undo, queue, log). The Task pattern encapsulates a unit of work for concurrent execution, primarily for concurrency purposes (parallelism, async, scheduling).

Tasks are designed for concurrent execution: they represent work that can be done in parallel, have completion states (pending, running, completed, failed), and may return results via futures. Commands are designed for sequential execution: they represent operations that change state and may need to be undone.

In practice, they overlap significantly. A command can be executed as a task for concurrency. A task can be designed as a command for undo support. The choice of terminology reflects the primary concern: "command" when the focus is on the operation itself (what to do), "task" when the focus is on execution management (when and where to do it).

---

## Q100: How would you design a command pattern system that scales to millions of commands per second?

**A:** Scaling to millions of commands per second requires horizontal scaling, efficient serialization, lock-free data structures, and careful resource management. The architecture uses multiple command processors, each handling a partition of the command stream.

The design elements: partitioning (commands are partitioned by type or key, ensuring related commands are processed by the same processor for ordering), batching (commands are batched for throughput, reducing per-command overhead), and async processing (command submission and execution are decoupled via queues).

Performance optimizations include: object pooling (reuse command objects to reduce GC pressure), zero-copy serialization (avoid memory allocation during serialization), dedicated thread cores (pin processors to CPU cores to avoid context switches), and off-heap storage (store command queues outside the heap for GC freedom).

Monitoring tracks: command throughput, latency percentiles, queue depth, error rates, and resource utilization. The system must handle hot partitions (commands skewed to a single key) through dynamic rebalancing. At this scale, the command pattern provides the abstraction, while the infrastructure provides the performance.

