# Memento, Visitor, Null Object and Specification — 100 Interview Q&A

## Q1: What is the Memento design pattern and what problem does it solve?

**A:** The Memento is a behavioral design pattern that captures and externalizes an object's internal state so that it can be restored later without violating encapsulation. It was catalogued by the Gang of Four and addresses the need for undo/redo, state snapshots, and transaction rollbacks. Without the Memento pattern, saving state would require exposing private fields or duplicating state management logic.

The pattern involves three roles: the Originator (whose state is saved), the Memento (the opaque state snapshot), and the Caretaker (which stores mementos but cannot interpret them). The Originator creates mementos via `createMemento()` and restores from them via `restore(memento)`. The Memento exposes a narrow interface to the Caretaker (no state access) and a wide interface to the Originator (full state access). The Caretaker manages memento lifecycle — storing, retrieving, and discarding them.

Consider a text editor: users expect undo. Without Memento, the editor would expose internal data structures for saving, breaking encapsulation. The Memento pattern provides a clean separation — the editor decides what state to save; the history manager stores the opaque snapshots; and the editor knows how to restore from them. This separation keeps each component focused on its responsibility.

## Q2: What are the roles in the Memento pattern and how do they interact?

**A:** The three primary roles are the Originator, Memento, and Caretaker. The Originator is the object whose state needs saving and restoring. It has methods like `createMemento()` and `restore(memento)`. The Memento stores the Originator's state as an opaque object — it is a black box that the Caretaker passes around but cannot read. The Caretaker maintains a collection of mementos and passes them to the Originator when restoration is needed.

The interaction flow is straightforward: the Originator creates a Memento containing its current state, passes it to the Caretaker for storage, and when undo is requested, the Caretaker returns the Memento to the Originator, which restores its state. The Caretaker never inspects or modifies Memento contents. This ensures that only the Originator understands the Memento's internal structure, preserving encapsulation.

The key invariant is that the Caretaker treats Mementos as opaque handles. If the Caretaker could read Memento fields, it would need to understand the Originator's state representation, creating tight coupling. The dual-interface design (narrow for Caretaker, wide for Originator) enforces this separation at the type-system level in languages like Java through access modifiers.

## Q3: How would you implement the Memento pattern in Java?

**A:** Java's access modifiers enable clean Memento implementations using static inner classes. The Memento class is a private static inner class of the Originator, with a private constructor and private getters. Only the Originator can create and read Mementos.

```java
public class TextEditor {
    private String content;
    private int cursorPosition;

    public Memento save() {
        return new Memento(content, cursorPosition);
    }

    public void restore(Memento memento) {
        this.content = memento.getContent();
        this.cursorPosition = memento.getCursorPosition();
    }

    public void type(String text) {
        content = content.substring(0, cursorPosition)
                   + text + content.substring(cursorPosition);
        cursorPosition += text.length();
    }

    public String getContent() { return content; }

    public static class Memento {
        private final String content;
        private final int cursorPosition;

        private Memento(String content, int cursorPosition) {
            this.content = content;
            this.cursorPosition = cursorPosition;
        }

        private String getContent() { return content; }
        private int getCursorPosition() { return cursorPosition; }
    }
}

public class EditorHistory {
    private final Stack<TextEditor.Memento> history = new Stack<>();

    public void save(TextEditor editor) {
        history.push(editor.save());
    }

    public void undo(TextEditor editor) {
        if (!history.isEmpty()) {
            editor.restore(history.pop());
        }
    }
}
```

The `Memento` class has private constructors and getters, accessible only within the enclosing `TextEditor` class. The `EditorHistory` (Caretaker) stores Mementos in a stack but cannot access their contents. This enforces encapsulation at the language level — the Caretaker can store, retrieve, and pass Mementos, but only the Originator can create and interpret them.

## Q4: What is the difference between wide and narrow Memento interfaces?

**A:** The wide interface is available only to the Originator and provides full access to the Memento's stored state. The narrow interface is available to the Caretaker and provides no state access — typically only identity operations. The dual-interface design ensures that the Caretaker stores Mementos without inspecting or modifying them.

In Java, the wide interface is implemented through private methods accessible only within the Originator's class. The narrow interface is the Memento's public surface, which has no state-access methods. Since the Caretaker receives the Memento through the public interface, it only sees the narrow interface. The Memento class itself may be package-private or an inner class to restrict even further.

In Python, the wide and narrow interfaces are enforced by convention (underscore-prefixed methods for the Originator, public methods for the Caretaker). This is less robust but follows the same conceptual separation. The key principle is that the Caretaker must never be able to read, write, or interpret the Memento's state. Without this separation, the Memento pattern degenerates into simple state exposure, losing its encapsulation benefits.

## Q5: How does the Memento pattern relate to the concept of encapsulation?

**A:** The Memento pattern is fundamentally about preserving encapsulation while enabling state externalization. Without it, saving state would require exposing private fields (breaking encapsulation) or distributing state management logic across multiple classes. The Memento pattern keeps state management within the Originator while delegating storage to the Caretaker.

The pattern creates a controlled boundary: the Originator decides what state to save and how to interpret it. The Caretaker stores the Memento as an opaque object, unaware of its contents. This means changes to the Originator's internal representation do not affect the Caretaker — only the Memento's creation and restoration code needs updating. This isolation is the pattern's primary design contribution.

The trade-off is complexity. The Memento class, dual interfaces, and Caretaker lifecycle management add code that simpler designs would not require. For objects with simple state, exposing fields directly may be more pragmatic. The Memento pattern is justified when encapsulation must be maintained — when the Originator's state representation is complex, volatile, or security-sensitive.

## Q6: What are the memory implications of the Memento pattern?

**A:** Each Memento stores a snapshot of the Originator's state, consuming memory proportional to the state size. For objects with large internal data, each Memento can be significant. If the Caretaker maintains a long history, memory consumption grows linearly with history depth. For 100 documents each with 50 undo levels and 10 KB per Memento, the total is 50 MB.

Mitigation strategies include differential Mementos (storing only changes since the previous state), compression (using gzip on Memento data), Memento pooling (reusing Memento objects for GC efficiency), and history pruning (limiting depth or using lossy compression for old states). The choice depends on the application's memory budget, performance requirements, and acceptable data loss tolerance.

For applications where Mementos are stored to disk (persistent undo), the memory impact shifts to disk usage. Differential storage and compression become even more important when Mementos must survive application restarts. The trade-off is between Memento creation time and storage space — full Mementos are fast to create but large; differential Mementos are small but require delta application during restoration.

## Q7: How does the Memento pattern handle concurrent access?

**A:** The Memento pattern requires careful handling in concurrent environments. If multiple threads can modify the Originator, creating a Memento must capture a consistent snapshot. This typically requires synchronization — the Originator must be locked during `save()` and `restore()` to prevent concurrent modification from corrupting the snapshot.

A common approach uses a read-write lock. The `save()` operation acquires a read lock (allowing concurrent saves but preventing modifications), while `restore()` acquires a write lock (exclusive access). Modifications also acquire write locks. This ensures Mementos capture consistent state without blocking concurrent reads.

An alternative is making the Originator immutable. Instead of modifying in place, `restore()` creates a new Originator instance from the Memento. This eliminates locking for restore but requires updating all references to the old Originator. Immutable Originators are naturally thread-safe but require more sophisticated state management and reference tracking.

## Q8: What is the relationship between the Memento pattern and serialization?

**A:** Serialization converts an object's state to a byte stream for persistence or transmission. The Memento pattern captures state for in-memory restoration. Both capture state, but serialization is for persistence across process boundaries while Memento is for in-memory state management within a process. The two can be combined: Mementos can be serialized to disk for persistent undo history.

However, serialization introduces challenges. The serialized form must be versioned to handle class evolution. Serialized Mementos may reference objects no longer valid after deserialization. The Memento's encapsulation can conflict with serialization's reflective access to private fields. These challenges require careful design of both the Memento class and serialization strategy.

Java's built-in serialization handles the encapsulation conflict by using reflection to access private fields, but this couples the Memento to Java's serialization mechanism. Alternative serialization approaches (JSON, Protocol Buffers) require the Memento to expose its state through a serializable format, which may compromise the narrow interface. The solution is to have the Originator provide a serialization-friendly representation without exposing it to the Caretaker.

## Q9: Can you explain the Memento pattern with a real-world analogy?

**A:** A video game's save system is a direct analogy. The game state is the Originator's internal state. The save file is the Memento — it captures the complete game state at a specific point in time. The save slot manager is the Caretaker — it stores multiple save files and loads them on demand. When you save, the game captures state and writes it to a file. The save manager does not interpret the file's contents.

A photograph is another analogy. A photograph captures a moment in time, recording the scene's state at the instant the shutter clicks. The photographer (Caretaker) stores photographs but cannot modify the scene they depict. You can "undo" to a previous state by recreating the scene from the photograph. Multiple photographs represent a history of states, like an undo stack.

A medical record provides a third analogy. The record captures the patient's health state at various points. The hospital (Caretaker) stores records but cannot modify them. The doctor (Originator) interprets the records to understand history and make decisions. New records capture current state; old records provide history for comparison. The medical record is the Memento; the hospital's filing system is the Caretaker.

## Q10: What is the Visitor design pattern and what problem does it solve?

**A:** The Visitor is a behavioral design pattern that adds new operations to an object structure without modifying the classes of the objects it contains. It separates algorithms from the objects they operate on. The pattern solves the problem of adding functionality to a stable class hierarchy without modifying existing classes, which is critical when the hierarchy is in a library or framework.

Consider a document structure with Paragraph, Heading, Image, and Table elements. Adding spell-checking, word-counting, and export operations without Visitor would require adding methods to every element class, bloating them with unrelated functionality. With Visitor, each operation is a separate class, and elements only need to accept visitors.

The pattern involves two key abstractions: the Visitor interface (defining visit methods for each element type) and the Element interface (defining an `accept` method that takes a Visitor). Each concrete element calls the visitor's corresponding `visit` method, creating a double dispatch that ensures the correct method is called for each element type. This double dispatch is the pattern's defining technical mechanism.

## Q11: How does double dispatch work in the Visitor pattern?

**A:** Double dispatch means the method invoked depends on both the receiver's type and the argument's type. In Java, single dispatch selects a method based on the receiver. Double dispatch adds a second dispatch based on the argument through a two-step call chain.

Step one: the client calls `element.accept(visitor)`. The dispatch selects the correct `accept` based on the element's concrete type. Step two: inside `accept`, the element calls `visitor.visit(this)`. The dispatch selects the correct `visit` based on the element type passed as argument.

```java
interface Element {
    void accept(Visitor visitor);
}

class Paragraph implements Element {
    String text;
    public void accept(Visitor visitor) { visitor.visit(this); }
}

class Heading implements Element {
    String title; int level;
    public void accept(Visitor visitor) { visitor.visit(this); }
}

interface Visitor {
    void visit(Paragraph p);
    void visit(Heading h);
}
```

Without double dispatch, a single `visit(Element e)` method would need `instanceof` checks, defeating the pattern. Double dispatch eliminates `instanceof` by leveraging polymorphism at both dispatch points. The `accept` method is the bridge that enables this two-step dispatch, ensuring compile-time type safety for each element-visitor combination.

## Q12: What is the accept method and why is it necessary?

**A:** The `accept` method is defined on each Element class and takes a Visitor parameter. Its purpose is to enable double dispatch. When `element.accept(visitor)` is called, the concrete element type determines which `accept` implementation runs. Inside, the element calls `visitor.visit(this)`, passing itself as the typed argument.

Without `accept`, the client would call `visitor.visit(element)` directly, requiring the client to know the element's concrete type for single dispatch to select the correct `visit` method. The `accept` method encapsulates this knowledge within each element class, keeping the client decoupled from concrete element types.

The `accept` method also provides the extensibility hook. New element types require a new class with its own `accept` method and a corresponding `visit` method on the Visitor. New operations require new Visitor implementations. This separation of element structure from operations is the Visitor pattern's primary contribution.

## Q13: What is the Null Object design pattern and what problem does it solve?

**A:** The Null Object replaces null references with a concrete object implementing the expected interface with no-op or default behavior. It eliminates null checks by providing a safe, inert object usable everywhere the real object is expected. The pattern solves scattered null-checking code that clutters business logic and is error-prone.

Consider a logging system where some components have a logger and others do not. Without Null Object, every logging call requires `if (logger != null) logger.log(message)`. With a `NullLogger` implementing the `Logger` interface with empty methods, components receive the `NullLogger` and logging calls proceed without null checks.

The Null Object provides semantic clarity. A null reference is ambiguous — it could mean "not available," "not applicable," or "error." A Null Object is explicit: it means "a valid object that does nothing." This makes code easier to read and reason about, as there is no ambiguity about what happens when a "missing" object is used.

## Q14: How would you implement the Null Object pattern in Java?

**A:** The implementation requires defining an interface that both real and null objects implement. The null object implements every method with no-op or default behavior. The client code uses the interface type and never checks for null.

```java
public interface Logger {
    void log(String message);
    void error(String message);
    void setLevel(int level);
}

public class ConsoleLogger implements Logger {
    private int level = 0;
    public void log(String message) {
        if (level <= 0) System.out.println("[LOG] " + message);
    }
    public void error(String message) {
        if (level <= 1) System.err.println("[ERROR] " + message);
    }
    public void setLevel(int level) { this.level = level; }
}

public class NullLogger implements Logger {
    public void log(String message) { }
    public void error(String message) { }
    public void setLevel(int level) { }
}

public class OrderService {
    private final Logger logger;

    public OrderService(Logger logger) {
        this.logger = logger != null ? logger : new NullLogger();
    }

    public void processOrder(Order order) {
        logger.log("Processing order " + order.getId());
        logger.log("Order processed successfully");
    }
}
```

The `OrderService` constructor defaults to `NullLogger` if null is passed. The `processOrder` method calls `logger.log()` without null checks. When a real logger is provided, messages are printed; when NullLogger is used, calls silently do nothing. The business logic remains clean with no conditional branching for null handling.

## Q15: What are the benefits of the Null Object pattern over simple null checks?

**A:** The primary benefit is code simplification. Null checks scattered throughout business logic create visual noise and obscure intent. The Null Object replaces these checks with a single check at the creation site, after which all code uses the object freely. This dramatically reduces boilerplate.

Null Object also improves testability. Tests can pass real implementations without worrying about null handling paths. The Null Object provides deterministic behavior (doing nothing) that simplifies assertions. Tests do not need mock objects for every nullable dependency, reducing setup complexity.

The pattern prevents null-related runtime errors. NullPointerExceptions are among the most common Java bugs. By replacing null with a Null Object, these exceptions are eliminated for the decorated interface. The methods are guaranteed to exist and be callable, so no `NoSuchMethodError` or `NullPointerException` can occur.

Finally, Null Object communicates intent. When a developer sees `new NullLogger()`, they understand logging is intentionally disabled. A null reference is ambiguous — it could be accidental or deliberate. The Null Object makes the design decision explicit and self-documenting.

## Q16: What is the Specification design pattern and what problem does it solve?

**A:** The Specification pattern encapsulates business rules into composable, reusable objects. Each Specification represents a single rule, and specifications combine using logical operators (AND, OR, NOT) to create complex rules from simple ones. The pattern solves scattered, duplicated business rules that are difficult to maintain and test.

Consider an e-commerce system filtering products by price, category, brand, and stock. Without Specification, each filter combination is a separate method with its own conditional logic. Adding a criterion requires modifying every filter method. With Specification, each criterion is a Specification object, and combinations are created by composing specifications.

The pattern follows the open-closed principle: new criteria are added by creating new Specification classes without modifying existing ones. Each Specification is independently testable. Composition is declarative and readable, expressing business rules in a DSL-like syntax that non-technical stakeholders can understand.

## Q17: How would you implement the Specification pattern in Java?

**A:** The core interface defines an `isSatisfiedBy` method. Composite specifications combine using logical operators via default methods.

```java
public interface Specification<T> {
    boolean isSatisfiedBy(T candidate);

    default Specification<T> and(Specification<T> other) {
        return candidate -> this.isSatisfiedBy(candidate)
                         && other.isSatisfiedBy(candidate);
    }

    default Specification<T> or(Specification<T> other) {
        return candidate -> this.isSatisfiedBy(candidate)
                         || other.isSatisfiedBy(candidate);
    }

    default Specification<T> not() {
        return candidate -> !this.isSatisfiedBy(candidate);
    }
}

public class PriceBelow implements Specification<Product> {
    private final double maxPrice;
    public PriceBelow(double maxPrice) { this.maxPrice = maxPrice; }
    public boolean isSatisfiedBy(Product p) { return p.getPrice() <= maxPrice; }
}

public class InCategory implements Specification<Product> {
    private final String category;
    public InCategory(String category) { this.category = category; }
    public boolean isSatisfiedBy(Product p) { return p.getCategory().equals(category); }
}
```

Usage is declarative: `Specification<Product> cheapElectronics = new PriceBelow(500).and(new InCategory("Electronics"));`. The `and`, `or`, `not` default methods create composite specifications using lambda expressions. Each composite delegates to its components. The composition is recursive — composite specifications combine with others for arbitrarily complex rules.

## Q18: How do the four patterns relate to each other?

**A:** These four patterns address different behavioral design aspects but share themes. Memento and Visitor deal with object structure and state from different angles: Memento captures state for restoration, while Visitor adds operations. Null Object and Specification simplify conditional logic: Null Object eliminates null checks; Specification eliminates scattered business rules.

The patterns compose well. A Memento system can use Null Objects for default states. A Visitor can operate on objects filtered by Specification. A Null Object can implement the Visitor interface for cases needing no operation. Specification can evaluate properties of objects stored as Mementos.

All four reduce complexity by encapsulating concerns. Memento encapsulates state capture and restoration. Visitor encapsulates operations on structures. Null Object encapsulates default behavior. Specification encapsulates business rules. Each provides a clean abstraction layer separating concerns and improving maintainability.

## Q19: What are the drawbacks of the Visitor pattern?

**A:** The primary drawback is that adding new element types requires modifying the Visitor interface and all implementations. If a new `Video` element is added, every existing Visitor must add a `visit(Video v)` method. This violates the open-closed principle for the element hierarchy — the pattern makes adding operations easy but adding element types hard.

This trade-off is appropriate when operations change frequently but element structure is stable. If both evolve rapidly, Visitor creates maintenance overhead. The Visitor interface becomes large and unwieldy, and implementors must handle all element types even if they care about only a few.

Another drawback is indirection overhead. Double dispatch adds a layer of method calls that can hurt performance in tight loops. The `accept`-then-`visit` call chain is less efficient than direct method calls. For most applications this overhead is negligible, but in performance-critical code (game engines, real-time systems), the indirection may be unacceptable.

## Q20: How does the Null Object pattern interact with testing?

**A:** Null Objects simplify testing by providing deterministic stand-ins for missing dependencies. Instead of mocking complex services, tests use Null Objects that do nothing. This reduces setup complexity and makes tests more readable. Each test case focuses on the behavior being tested without distraction from dependency management.

However, Null Objects can mask bugs. If a test accidentally receives a Null Object instead of the real implementation, the test passes silently because no-op methods never fail. The test appears to exercise the code path but actually bypasses the functionality. This is a subtle and dangerous failure mode that can give false confidence.

To mitigate this, tests should verify the correct implementation is injected. Null Objects in test contexts can optionally record invocations (like a spy), allowing assertions that specific methods were called. This combines Null Object simplicity with mock verification capability.

```java
public class SpyNullLogger implements Logger {
    private final List<String> messages = new ArrayList<>();
    public void log(String message) { messages.add(message); }
    public void error(String message) { messages.add("ERROR:" + message); }
    public void setLevel(int level) { }
    public List<String> getMessages() { return messages; }
}
```

## Q21: Can the Specification pattern be used for authorization?

**A:** Yes, Specification is particularly well-suited for authorization. Each permission or role is a Specification evaluating whether a user meets requirements. Complex authorization rules compose from simple specifications.

```java
public class IsAdmin implements Specification<User> {
    public boolean isSatisfiedBy(User u) { return u.getRole() == Role.ADMIN; }
}

public class IsOwner implements Specification<User> {
    private final Resource resource;
    public IsOwner(Resource r) { this.resource = r; }
    public boolean isSatisfiedBy(User u) {
        return resource.getOwnerId().equals(u.getId());
    }
}

Specification<User> canEdit = new IsAdmin()
    .or(new IsOwner(resource).and(new HasPermission("edit")));
```

Authorization rules become declarative, centralized in Specification classes for easy auditing, testing, and modification. New permissions are added as new implementations. Rules compose and can be stored in configuration for runtime flexibility. This approach is used in ABAC (Attribute-Based Access Control) systems where policies are evaluated as composable predicates.

## Q22: How does the Memento pattern handle large state objects?

**A:** For large state objects, full Mementos are prohibitively expensive. Differential or incremental Mementos store only changes between states. Instead of capturing entire state, the Memento records which fields changed and their new values. Restoration applies the delta to the previous state.

Copy-on-write Mementos store a reference to original state plus a list of modifications. When the original changes, only modified portions are copied. This defers copying until modification occurs, reducing Memento creation cost.

For very large objects, Mementos use external storage — writing state to disk with the Memento holding a reference. This keeps Memento objects lightweight while enabling restoration from external storage. The trade-off is between creation time (full Mementos are slow to create, differential are fast) and restoration time (full Mementos restore instantly, differential require delta application).

## Q23: What is the relationship between Visitor and the Composite pattern?

**A:** Visitor and Composite are frequently combined. Composite creates tree structures where nodes can be individual or composed objects. Visitor traverses these trees and performs operations on each node. The combination provides a clean way to process recursive data structures.

In a Composite structure, each element implements `accept`. The Visitor's `visit` methods are called for each type. The Composite's `getChildren()` allows traversal. A TreeVisitor recursively visits all nodes by visiting each child of composite nodes.

```java
interface FileSystemElement {
    void accept(FileSystemVisitor visitor);
}

class File implements FileSystemElement {
    public void accept(FileSystemVisitor visitor) { visitor.visit(this); }
}

class Directory implements FileSystemElement {
    private List<FileSystemElement> children = new ArrayList<>();
    public void accept(FileSystemVisitor visitor) {
        visitor.visit(this);
        for (FileSystemElement child : children) child.accept(visitor);
    }
}
```

The Composite provides structure; the Visitor provides operations. This separation allows adding new operations without modifying Composite classes, and adding new element types without modifying existing Visitors. The combination is foundational in compiler design (AST traversal), GUI frameworks (widget processing), and file systems (directory traversal).

## Q24: How do you handle the Visitor pattern with heterogeneous structures?

**A:** Heterogeneous structures contain elements of many types, requiring a `visit` method for each type. This leads to large Visitor interfaces. Strategies include default method implementations (Java 8+), adapter classes, and grouping related elements under abstract base types.

Java 8+ default methods provide no-op defaults for element types a Visitor does not care about:

```java
interface ElementVisitor {
    default void visit(Paragraph p) { }
    default void visit(Heading h) { }
    default void visit(Image i) { }
    default void visit(Table t) { }
}
```

Grouping related elements reduces method count. Instead of `visit(Heading1)`, `visit(Heading2)`, `visit(Heading3)`, a single `visit(Heading h)` handles all levels with the level as a property. This reduces visit methods without losing type information. For very large hierarchies, a catch-all `visitDefault(Element e)` method handles unknown types, though this reintroduces some of the type-safety issues the pattern was designed to eliminate.

## Q25: What are the testing strategies for the Visitor pattern?

**A:** Testing Visitors requires verifying each `visit` method handles its target element type correctly. Tests cover: correct behavior for each element type, correct traversal of composite structures, and correct state accumulation across multiple visits.

Each Visitor should have unit tests constructing known elements, applying the Visitor, and asserting expected outcomes. For a `WordCountVisitor`, tests create elements with known text, visit them, and verify word counts. For a `SearchVisitor`, tests create elements with known content, visit with a search term, and verify matching elements are collected.

Integration tests verify Composite traversal. A test creates a tree of elements, applies a Visitor, and verifies every element was visited. A `RecordingVisitor` that tracks visited elements enables this verification. Property-based testing generates random element trees and verifies invariants: every element visited exactly once, traversal order matches strategy, and accumulated state is consistent.

## Q26: How would you implement a Memento pattern with undo/redo support?

**A:** Undo/redo requires two stacks: one for past states and one for future states. When the user acts, the current state pushes onto the undo stack and the redo stack clears. On undo, the current state pushes onto the redo stack and a state pops from undo. On redo, the current state pushes onto undo and a state pops from redo.

```java
public class UndoRedoManager {
    private final Deque<TextEditor.Memento> undoStack = new ArrayDeque<>();
    private final Deque<TextEditor.Memento> redoStack = new ArrayDeque<>();

    public void recordState(TextEditor editor) {
        undoStack.push(editor.save());
        redoStack.clear();
    }

    public void undo(TextEditor editor) {
        if (undoStack.isEmpty()) return;
        redoStack.push(editor.save());
        editor.restore(undoStack.pop());
    }

    public void redo(TextEditor editor) {
        if (redoStack.isEmpty()) return;
        undoStack.push(editor.save());
        editor.restore(redoStack.pop());
    }

    public boolean canUndo() { return !undoStack.isEmpty(); }
    public boolean canRedo() { return !redoStack.isEmpty(); }
}
```

The key insight is that every state transition saves the current state before restoring. This ensures reversibility. Clearing the redo stack on new actions follows convention: once the user acts after undoing, future states are invalidated. For unlimited undo, stacks grow without bounds. For bounded undo, a maximum size is enforced and oldest states discarded.

## Q27: How does the Null Object pattern apply to the Strategy pattern?

**A:** The Null Object serves as a default Strategy when none is configured. Instead of checking for null before invoking a strategy, code uses a Null Strategy providing sensible defaults. This eliminates null checks in Strategy pattern client code.

```java
public interface SortStrategy {
    <T> List<T> sort(List<T> list, Comparator<T> comparator);
}

public class QuickSort implements SortStrategy {
    public <T> List<T> sort(List<T> list, Comparator<T> comp) {
        List<T> sorted = new ArrayList<>(list);
        sorted.sort(comp);
        return sorted;
    }
}

public class NullSortStrategy implements SortStrategy {
    public <T> List<T> sort(List<T> list, Comparator<T> comp) {
        return new ArrayList<>(list); // return unsorted copy
    }
}
```

The Null Strategy returns input unchanged — a reasonable default for sorting. The client defaults to Null Strategy when no strategy is provided, preserving the interface contract without null checks. This pattern works across any strategy-based design: the Null Object provides safe default behavior that keeps code clean and focused on business logic.

## Q28: Can the Specification pattern support database queries?

**A:** Yes, Specifications translate to database queries. Each Specification's logic maps to a SQL WHERE clause. `PriceBelow(500)` becomes `WHERE price <= 500`. `InCategory("Electronics")` becomes `WHERE category = 'Electronics'`. Composites translate to combined WHERE clauses with AND/OR.

The implementation adds a method converting Specifications to query predicates. Spring Data JPA provides built-in support through its `Specification<T>` interface and `JpaSpecificationExecutor`:

```java
public interface Specification<T> {
    boolean isSatisfiedBy(T candidate);
    Predicate toPredicate(Root<T> root, CriteriaQuery<T> query,
                          CriteriaBuilder cb);
}

public class PriceBelow implements Specification<Product> {
    private final double maxPrice;
    public PriceBelow(double max) { this.maxPrice = max; }
    public boolean isSatisfiedBy(Product p) { return p.getPrice() <= maxPrice; }
    public Predicate toPredicate(Root<Product> root, CriteriaQuery<Product> q,
                                  CriteriaBuilder cb) {
        return cb.lessThanOrEqualTo(root.get("price"), maxPrice);
    }
}
```

This bridges domain-level business rules with database-level query construction. Complex queries are built from composable, testable Specification objects without string concatenation or raw SQL. The pattern enables type-safe, maintainable data access layers.

## Q29: How does the Memento pattern handle circular references?

**A:** Circular references occur when an object's state includes references to other objects that, directly or indirectly, reference the original. Naively serializing such a structure creates infinite recursion. The Memento must detect and handle cycles during state capture.

The standard solution uses a visited set. When saving state, the Originator traverses its object graph. Before processing each object, it checks the visited set. If the object is already visited, a reference ID is stored instead of re-serializing. If not, the object is added to the set and serialized with a unique ID.

Java's default serialization handles circular references automatically using a back-reference table. When an object is serialized, subsequent references to the same object are stored as small integer identifiers rather than full copies. For manual implementations, the visited set approach must be implemented explicitly, storing a map of object-to-ID and rebuilding identity relationships during restoration.

## Q30: How would you extend the Visitor pattern to support return values?

**A:** The basic Visitor typically performs void operations. To support return values, visit methods return a generic type. The Visitor interface becomes parameterized: `interface Visitor<T>`, and each `visit` method returns `T`.

```java
public interface Visitor<T> {
    T visit(Paragraph p);
    T visit(Heading h);
    T visit(Image i);
}

public class SizeCalculator implements Visitor<Integer> {
    public Integer visit(Paragraph p) { return p.getText().length(); }
    public Integer visit(Heading h) { return h.getTitle().length(); }
    public Integer visit(Image i) { return i.getFileSize(); }
}

public interface Element<T> {
    T accept(Visitor<T> visitor);
}
```

For composite structures, child results are combined using a reducer function. A Composite visits each child, collects results, and combines them (sum for size, concatenation for text extraction). This preserves the Visitor's separation of operations from structure while adding value computation. The generic parameter enforces type consistency across all visit methods.

## Q31: How does the Null Object pattern apply to collections and iterators?

**A:** Null Iterators return false from `hasNext()` and throw no exception from `next()`. Null Collections return empty lists from `iterator()`, zero from `size()`, and false from `contains()`. These allow iteration over potentially-empty collections without null checks.

```java
public class NullIterator<T> implements Iterator<T> {
    public boolean hasNext() { return false; }
    public T next() { throw new NoSuchElementException(); }
}

public class NullCollection<T> implements Collection<T> {
    public Iterator<T> iterator() { return new NullIterator<>(); }
    public int size() { return 0; }
    public boolean isEmpty() { return true; }
    public boolean contains(Object o) { return false; }
    public boolean add(T e) { throw new UnsupportedOperationException(); }
}
```

Java's `Collections.emptyList()`, `emptyMap()`, and `emptySet()` are standard-library Null Objects — immutable, shared instances combining Null Object and Flyweight. Using these instead of null prevents NullPointerExceptions in iteration loops and stream operations, and communicates "no data" explicitly rather than ambiguously.

## Q32: What is the relationship between Specification and predicate logic?

**A:** The Specification pattern is a direct application of predicate logic. Each Specification represents a predicate — a function returning true or false. The `and`, `or`, `not` operators correspond to logical conjunction, disjunction, and negation.

This correspondence means Specification composition follows predicate logic laws. Commutativity: `A.and(B)` equals `B.and(A)`. Associativity: `A.and(B.and(C))` equals `(A.and(B)).and(C)`. De Morgan's laws apply: `A.not().and(B.not())` equals `(A.or(B)).not()`.

Understanding this foundation enables optimizations. Tautologies (always true) and contradictions (always false) can be simplified during composition. Mutually exclusive specifications short-circuit their `and` to false. These logical optimizations, similar to compiler constant folding, significantly improve query performance in database-backed specifications. The mathematical rigor also makes specifications easier to reason about and verify.

## Q33: How would you implement a memento-based state machine?

**A:** A state machine uses Mementos to capture complete state, enabling rollback, replay, and debugging. Each transition records a Memento, creating a complete execution history.

```java
public class StateMachine {
    private State currentState;
    private final Map<State, Map<Event, State>> transitions;

    public Memento save() { return new Memento(currentState); }

    public void restore(Memento memento) {
        this.currentState = memento.getState();
    }

    public void transition(Event event) {
        State next = transitions
            .getOrDefault(currentState, Collections.emptyMap())
            .get(event);
        if (next == null) throw new IllegalStateException(
            "No transition for " + event + " in state " + currentState);
        currentState = next;
    }

    public static class Memento {
        private final State state;
        private Memento(State state) { this.state = state; }
        State getState() { return state; }
    }
}
```

The machine records a Memento before each transition. Invalid transitions trigger restoration from the previous Memento. This provides automatic rollback and an audit trail. For debugging, the Memento history can be replayed step by step to identify where the machine deviated from expected behavior. In distributed systems, state machine Mementos enable checkpointing and recovery after failures.

## Q34: How does the Visitor pattern support different traversal strategies?

**A:** Traversal strategy is orthogonal to the Visitor's operation logic. The Visitor defines what to do; the traversal defines order. The same Visitor works with depth-first, breadth-first, or custom traversal by separating the mechanism.

```java
public class BreadthFirstTraversal {
    public static <T> void traverse(Element root, Visitor<T> visitor) {
        Queue<Element> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            Element current = queue.poll();
            current.accept(visitor);
            if (current instanceof Composite) {
                for (Element child : ((Composite) current).getChildren()) {
                    queue.add(child);
                }
            }
        }
    }
}
```

This separation allows the same Visitor applied with either strategy without modification. Pre-order vs post-order tree processing may produce different Visitor results, but the Visitor itself is traversal-agnostic. This clean separation is a strength — traversal concerns do not pollute operation logic, and vice versa.

## Q35: What are the performance considerations for the Specification pattern?

**A:** Specifications introduce indirection that impacts performance. Each `isSatisfiedBy` call involves virtual dispatch, and composites create nested calls. For high-throughput evaluation, this overhead can be significant compared to inline conditionals.

Simple field comparisons (like `price < 500`) are cheap; the overhead is negligible. Complex specifications involving I/O or heavy computation dominate. The pattern adds constant-factor overhead, not algorithmic complexity.

For performance-critical paths, specifications can be compiled into optimized forms. A specification tree compiles into a single predicate function eliminating intermediate objects and dispatch overhead. This is analogous to SQL query builders compiling specification trees into optimized query plans. Libraries like Spring Data JPA perform this optimization for database queries. Profiling should guide whether the abstraction cost justifies the maintainability benefit.

## Q36: How does the Memento pattern work with immutable objects?

**A:** Immutable objects simplify Memento because state cannot change after construction. The Memento for an immutable Originator is the object itself — since it cannot be modified, it naturally preserves state. This eliminates separate Memento classes in many cases.

For immutable Originators, saving state means storing a reference. Restoring means replacing the current reference. No copying or field-by-field restoration is needed. Each `type()` call creates a new instance, trading creation overhead for simplicity and thread safety.

```java
public class ImmutableEditor {
    private final String content;
    private final int cursorPosition;

    public ImmutableEditor(String content, int cursorPosition) {
        this.content = content;
        this.cursorPosition = cursorPosition;
    }

    public ImmutableEditor type(String text) {
        String newContent = content.substring(0, cursorPosition)
                          + text + content.substring(cursorPosition);
        return new ImmutableEditor(newContent, cursorPosition + text.length());
    }

    public String getContent() { return content; }
    public int getCursorPosition() { return cursorPosition; }
}

class EditorHistory {
    private final Deque<ImmutableEditor> history = new ArrayDeque<>();
    public void record(ImmutableEditor editor) { history.push(editor); }
    public ImmutableEditor undo() {
        return history.isEmpty() ? null : history.pop();
    }
}
```

The immutable approach is simpler, safer, and more concurrent than mutable Mementos. The trade-off is object creation overhead, which may be significant for large state but often justifies the benefits.

## Q37: How does the Null Object pattern handle logging and monitoring?

**A:** Logging and monitoring are classic Null Object use cases. Not every component needs logging, but every component might want to log. The Null Logger allows components to call logging methods unconditionally, with the Null Logger silently discarding messages.

Beyond simple no-ops, Null Loggers can be configured at runtime to switch between real and null implementations. A logging framework provides a Null Logger by default and replaces it when configuration loads. This allows the application to start without logging configuration and enable logging later.

For monitoring, Null Metrics objects record no data but provide the same interface as real collectors. Instrumented code runs without performance impact when monitoring is disabled. When enabled, Null Metrics is replaced with a real implementation. This pattern also supports conditional logging — a Null Logger configured to log only above a certain severity level provides fine-grained control without changing calling code.

## Q38: Can the Specification pattern be used for validation?

**A:** Validation is a natural fit. Each validation rule is a Specification evaluating whether input meets a requirement. Complex validations compose from simple specifications, providing reusable, testable, and composable validation logic.

```java
public class EmailFormat implements Specification<String> {
    private static final Pattern EMAIL = Pattern.compile(
        "^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$");
    public boolean isSatisfiedBy(String email) {
        return email != null && EMAIL.matcher(email).matches();
    }
}

public class NotBlank implements Specification<String> {
    public boolean isSatisfiedBy(String s) {
        return s != null && !s.trim().isEmpty();
    }
}

public class MinLength implements Specification<String> {
    private final int min;
    public MinLength(int min) { this.min = min; }
    public boolean isSatisfiedBy(String s) {
        return s != null && s.length() >= min;
    }
}
```

Validation rules become declarative: `Specification<String> validEmail = new NotBlank().and(new EmailFormat()).and(new MinLength(5));`. Each specification encapsulates one rule. Tests verify each rule independently. Composition creates complex rules from simple ones. The pattern separates validation from the objects being validated, enabling reuse across API input, form data, and configuration.

## Q39: How do you implement the Visitor pattern with generics for type safety?

**A:** Generic Visitors parameterize the return type, eliminating casts and enabling compile-time verification. The Element interface is also parameterized to match.

```java
public interface ElementVisitor<R> {
    R visit(Paragraph p);
    R visit(Heading h);
    R visit(Image i);
}

public interface Element<R> {
    R accept(ElementVisitor<R> visitor);
}

public class Paragraph implements Element<String> {
    private String text;
    public String accept(ElementVisitor<String> visitor) {
        return visitor.visit(this);
    }
}
```

The generic parameter `R` represents the return type. A `WordCountVisitor` implements `ElementVisitor<Integer>`, a `TextExtractor` implements `ElementVisitor<String>`. Each implementation is compile-time type-checked. For composite elements, the parameter controls aggregation type — the composite visits children, collects results of type `R`, and combines them using a function, all type-safely.

## Q40: What is the relationship between Memento and the Command pattern?

**A:** Memento and Command are frequently combined for undoable commands. Each Command stores a Memento before executing, enabling undo by restoring the Memento. Commands encapsulate actions; Mementos encapsulate state. Together they provide a complete undo/redo framework.

A command's `execute` saves current state as a Memento, then performs the action. `undo` restores from the saved Memento. The Command history stores both command and Memento. This separation is clean: the Command defines what changes; the Memento defines how to reverse those changes. New commands are added by implementing the Command interface with appropriate Memento creation and restoration logic.

The combination is used in text editors (each typing command saves cursor and content state), graphical editors (each shape manipulation saves canvas state), and database transactions (each operation saves affected rows). The undo infrastructure is generic and reusable across all command types.

## Q41: How does the Null Object pattern apply to the Observer pattern?

**A:** In the Observer pattern, subjects notify observers of state changes. Without observers, the subject must check for null or handle an empty list. The Null Object eliminates this by providing a Null Observer that does nothing.

```java
public interface Observer {
    void update(Event event);
}

public class NullObserver implements Observer {
    public void update(Event event) { }
}

public class Subject {
    private List<Observer> observers = new ArrayList<>();
    public void addObserver(Observer o) {
        if (o != null) observers.add(o);
    }
    public void notify(Event event) {
        for (Observer o : observers) o.update(event);
    }
}
```

If the subject uses a Null Observer as default, it always has at least one observer, eliminating empty-list checks. Java's `CopyOnWriteArrayList` for observer storage combines Null Object (empty list) with thread-safe iteration — the list is copied on write and iterated without locking, providing safe notification without synchronization overhead.

## Q42: How would you implement a composite Specification with a database query builder?

**A:** A database query builder translates Specifications into SQL. Each Specification contributes a WHERE clause fragment. Composites combine fragments with AND/OR. Spring Data JPA's `Specification` provides `toPredicate` methods returning JPA Criteria predicates.

```java
public class ProductSpecifications {
    public static Specification<Product> priceBelow(double max) {
        return (root, query, cb) ->
            cb.lessThanOrEqualTo(root.get("price"), max);
    }

    public static Specification<Product> inCategory(String cat) {
        return (root, query, cb) ->
            cb.equal(root.get("category"), cat);
    }

    public static Specification<Product> inStock() {
        return (root, query, cb) ->
            cb.greaterThan(root.get("stock"), 0);
    }
}

// Usage
Specification<Product> spec = ProductSpecifications.priceBelow(500)
    .and(ProductSpecifications.inCategory("Electronics"))
    .and(ProductSpecifications.inStock());

List<Product> results = repository.findAll(spec);
```

The Specification-to-SQL translation enables type-safe, composable queries without string concatenation. Each Specification encapsulates query logic, independently testable and reusable. The composition creates complex queries from simple building blocks, maintaining readability and database optimization.

## Q43: How does the Memento pattern handle state validation during restoration?

**A:** When restoring from a Memento, the Originator should validate that the restored state is consistent and valid. A Memento might have been created by an older version or corrupted. Validation during restoration prevents entering an invalid state.

```java
public void restore(Memento memento) {
    String previousContent = this.content;
    int previousCursor = this.cursorPosition;

    this.content = memento.getContent();
    this.cursorPosition = memento.getCursorPosition();

    if (!isValid()) {
        this.content = previousContent;
        this.cursorPosition = previousCursor;
        throw new IllegalStateException("Restored state is invalid");
    }
}

private boolean isValid() {
    return content != null
        && cursorPosition >= 0
        && cursorPosition <= content.length();
}
```

The validation saves the previous state before restoration, allowing rollback if validation fails. This atomic restore-and-validate pattern prevents partial state corruption. For complex objects, validation may check field relationships, referential integrity, or call external validation services.

## Q44: How does the Visitor pattern extend beyond double dispatch?

**A:** Double dispatch handles two types: Visitor and Element. For operations involving more types, the pattern extends with parameterized visit methods or multi-method dispatch mechanisms.

```java
interface RenderingVisitor {
    void visit(Paragraph p, RenderContext ctx);
    void visit(Heading h, RenderContext ctx);
    void visit(Image i, RenderContext ctx);
}
```

The `RenderContext` parameter provides additional context but does not participate in Java's dispatch. For true multi-dispatch (dispatching on multiple argument types), languages like CLOS provide multi-methods natively. In Java, multi-dispatch is simulated with double dispatch chains: the first dispatch selects the element-specific method; within that, a second dispatch on argument type selects behavior. This creates a dispatch tree handling element-argument type combinations.

## Q45: What is the Null Object pattern's role in Chain of Responsibility?

**A:** In Chain of Responsibility, requests pass through handlers. If no handler processes the request, it falls through. A Null Object at the chain's end provides a default response, eliminating termination checks.

```java
public interface Handler {
    boolean handle(Request request);
}

public class NullHandler implements Handler {
    public boolean handle(Request request) {
        System.out.println("No handler for: " + request);
        return false;
    }
}

public class Chain {
    private final List<Handler> handlers = new ArrayList<>();
    public void addHandler(Handler h) { handlers.add(h); }
    public void process(Request request) {
        for (Handler h : handlers) {
            if (h.handle(request)) return;
        }
    }
}
```

The Null Handler at the chain's end ensures every request is handled, even if no real handler can process it. This prevents requests from falling through unprocessed. Without it, the chain must check whether any handler processed the request after the loop — the Null Object eliminates this post-loop check.

## Q46: How does the Specification pattern handle temporal rules?

**A:** Temporal specifications evaluate time-dependent rules. `ValidBetween` checks whether the current time falls within a range. `BusinessHours` checks whether it is a business day. These compose with domain specifications for time-dependent rules.

```java
public class ValidBetween implements Specification<Void> {
    private final LocalDateTime start, end;
    public ValidBetween(LocalDateTime start, LocalDateTime end) {
        this.start = start; this.end = end;
    }
    public boolean isSatisfiedBy(Void ignored) {
        LocalDateTime now = LocalDateTime.now();
        return !now.isBefore(start) && !now.isAfter(end);
    }
}

public class BusinessHours implements Specification<Void> {
    public boolean isSatisfiedBy(Void ignored) {
        LocalTime now = LocalTime.now();
        return !now.isBefore(LocalTime.of(9, 0))
            && !now.isAfter(LocalTime.of(17, 0));
    }
}

Specification<Product> discountedElectronics = new InCategory("Electronics")
    .and(new ValidBetween(discountStart, discountEnd))
    .and(new BusinessHours());
```

Temporal specifications separate time logic from domain logic. Temporal specs are reusable across domains; domain specs are reusable across time periods. The composition expresses complex business rules readably and maintainably.

## Q47: How does the Memento pattern work with event sourcing?

**A:** Event sourcing stores state changes as events rather than current state. Mementos capture point-in-time snapshots. Together: events provide complete history; mementos provide fast restoration checkpoints.

Instead of replaying all events (slow for long streams), the system periodically creates a Memento (snapshot). Restoration replays events only from the last snapshot, reducing replay time. This snapshot-based optimization is used in frameworks like Axon and EventStore.

The snapshot frequency is tuned based on event volume and restoration requirements. High-event-rate systems snapshot every 1000 events; low-rate systems every 100. The trade-off is snapshot creation cost versus restoration speed. Mementos in this context are serialized state objects derived from the event stream.

## Q48: How does the Visitor pattern apply to ASTs in compilers?

**A:** Compilers represent source code as ASTs where nodes correspond to language constructs. The Visitor is the standard mechanism for compiler passes. Each pass (type checking, optimization, code generation) is a Visitor processing specific node types.

The AST hierarchy defines element types: `BinaryExpression`, `IfStatement`, `FunctionDeclaration`, etc. Each implements `accept(Visitor)`. A type-checking Visitor implements `visit(BinaryExpression)`, `visit(IfStatement)`, performing type inference for each node type.

This separation is critical for compiler maintainability. Adding an optimization pass means adding a Visitor without modifying AST nodes. Adding a language construct means adding a node class and updating all Visitors. The Visitor makes the trade-off explicit: adding operations is easy; adding element types updates all Visitors. This is why compiler frameworks like LLVM and ANTLR use Visitor-based architectures.

## Q49: What is the Null Object pattern's impact on API design?

**A:** Null Objects improve API design by providing safe defaults that eliminate null-related errors. APIs returning Null Objects instead of null are safer — callers do not need null checks. The Null Object's behavior is predictable and documented, unlike null's ambiguity.

Java's `Collections.emptyList()`, `emptyMap()`, and `emptySet()` are standard Null Objects for collections. This convention is so prevalent that style guides recommend returning empty collections instead of null as a best practice. The Null Object communicates "no results" without requiring null checks.

The pattern simplifies API documentation. Instead of documenting which methods may return null and null semantics in each context, the API documents the Null Object's behavior. This reduces documentation complexity and prevents misunderstandings. For framework designers, providing Null Object implementations alongside real implementations ensures that consumers always have a safe fallback.

## Q50: How does the Specification pattern compose with functional programming?

**A:** The Specification pattern maps directly to functional concepts. Each Specification is a predicate function `T -> boolean`. Composition via `and`, `or`, `not` corresponds to function composition. In functional languages, specifications are first-class functions that can be passed, stored, and composed.

Java's functional interfaces make this explicit. A `Specification<T>` can be a lambda:

```java
Specification<Product> cheapAndAvailable = p -> p.getPrice() < 50
    .and(p -> p.getStock() > 0);
```

The functional approach is concise for simple specifications but lacks reusability and testability of dedicated classes. Simple, single-use specs benefit from lambdas. Complex, reusable specs benefit from classes with unit tests. In Haskell, specifications use the `Predicate` monad and function composition. In Scala, case classes with pattern matching provide natural implementations. The pattern transcends languages, rooted in predicate logic mathematics.

## Q51: How would you implement a Memento pattern for a rich text editor?

**A:** A rich text editor has complex state: text content, formatting (bold, italic, font, size, color), cursor position, and selection range. The Memento must capture all state atomically with deep copies to prevent shared references from being corrupted by subsequent edits.

```java
public class RichTextEditor {
    private StringBuilder content;
    private int cursorPosition;
    private int selectionStart, selectionEnd;
    private Map<Integer, FormatRange> formatting;
    private String currentFont;
    private int currentFontSize;

    public Memento save() {
        return new Memento(
            content.toString(), cursorPosition,
            selectionStart, selectionEnd,
            new HashMap<>(formatting), currentFont, currentFontSize
        );
    }

    public void restore(Memento m) {
        this.content = new StringBuilder(m.content);
        this.cursorPosition = m.cursorPosition;
        this.selectionStart = m.selectionStart;
        this.selectionEnd = m.selectionEnd;
        this.formatting = new HashMap<>(m.formatting);
        this.currentFont = m.currentFont;
        this.currentFontSize = m.currentFontSize;
    }

    public static class Memento {
        final String content;
        final int cursorPosition, selectionStart, selectionEnd;
        final Map<Integer, FormatRange> formatting;
        final String currentFont;
        final int currentFontSize;

        Memento(String content, int cursor, int selStart, int selEnd,
                Map<Integer, FormatRange> fmt, String font, int fontSize) {
            this.content = content;
            this.cursorPosition = cursor;
            this.selectionStart = selStart;
            this.selectionEnd = selEnd;
            this.formatting = fmt;
            this.currentFont = font;
            this.currentFontSize = fontSize;
        }
    }
}
```

The `new StringBuilder(m.content)` and `new HashMap<>(m.formatting)` create deep copies preventing shared references between the Memento and Editor. Without deep copies, subsequent edits would corrupt stored Mementos. The trade-off is deep-copy overhead on each save, optimizable with copy-on-write or differential Mementos for performance-critical applications.

## Q52: How does the Visitor pattern handle null elements in a structure?

**A:** Null elements require special handling. If a composite contains null children, the Visitor's traversal must skip them to avoid NullPointerExceptions. This is handled in the composite's `accept` method or traversal logic.

```java
public class CompositeElement implements Element {
    private List<Element> children = new ArrayList<>();

    public void accept(Visitor visitor) {
        visitor.visit(this);
        for (Element child : children) {
            if (child != null) child.accept(visitor);
        }
    }
}
```

Alternatively, the Null Object pattern applies: instead of null, store a Null Element implementing the Element interface with no-op behavior. This eliminates null checks throughout traversal. The Null Element approach is cleaner because it removes conditional logic from every traversal site. Adding null elements is handled uniformly, and the Visitor never checks for null. The trade-off is Negligible overhead from Null Element objects.

## Q53: What is the relationship between Specification and the Rule Engine pattern?

**A:** Specification is a lightweight, code-level implementation of the Rule Engine pattern. A full Rule Engine (Drools, Easy Rules) provides a complete platform with rule language, conflict resolution, and lifecycle management. Specification provides the same composition in pure code.

For simple rules defined and modified by developers, Specification suffices and avoids rule engine overhead. For complex rules changing frequently, involving non-technical stakeholders, or requiring chaining and conflict resolution, a full rule engine is appropriate.

Specification can serve as a rule engine's internal representation. The rule language compiles into Specification objects, composed and evaluated against data. This separates the rule definition layer (DSL or configuration) from execution layer (Specification evaluation), enabling both to evolve independently.

## Q54: How does the Null Object pattern handle exception scenarios?

**A:** Null Objects provide safe defaults for exception scenarios. Instead of letting exceptions propagate, a Null Object catches them internally and provides degraded behavior. This is useful in non-critical subsystems where failure should not affect the main application.

```java
public class FaultTolerantLogger implements Logger {
    private final Logger delegate;
    private final Logger fallback;

    public FaultTolerantLogger(Logger delegate, Logger fallback) {
        this.delegate = delegate;
        this.fallback = fallback;
    }

    public void log(String message) {
        try { delegate.log(message); }
        catch (Exception e) { fallback.log(message); }
    }

    public void error(String message) {
        try { delegate.error(message); }
        catch (Exception e) { fallback.error(message); }
    }

    public void setLevel(int level) {
        try { delegate.setLevel(level); }
        catch (Exception e) { fallback.setLevel(level); }
    }
}
```

The `FaultTolerantLogger` wraps a real logger and falls back to Null Logger on failure. This prevents logging failures from crashing the application. The pattern applies to monitoring, metrics, and other cross-cutting concerns where failure should be graceful rather than catastrophic.

## Q55: How would you implement a versioned Memento system?

**A:** Versioned Mementos assign version numbers to snapshots, enabling ordered history navigation, conflict detection, and selective pruning.

```java
public class VersionedMementoSystem<T> {
    private final TreeMap<Long, Memento<T>> versions = new TreeMap<>();
    private long nextVersion = 1;

    public long save(Originator<T> originator) {
        Memento<T> memento = new Memento<>(nextVersion, originator.captureState());
        versions.put(nextVersion, memento);
        return nextVersion++;
    }

    public boolean restore(Originator<T> originator, long version) {
        Memento<T> memento = versions.get(version);
        if (memento == null) return false;
        originator.applyState(memento.state());
        return true;
    }

    public List<Long> getVersions() { return new ArrayList<>(versions.keySet()); }

    public void pruneBefore(long version) { versions.headMap(version, true).clear(); }
}
```

The versioned system provides ordered navigation (restore to any version), conflict detection (compare versions for concurrent modifications), selective pruning (remove old versions), and version diffing (compare versions to identify changes). These capabilities are essential for collaborative editing, distributed systems, and complex undo requirements.

## Q56: How does the Visitor pattern apply to XML/JSON processing?

**A:** XML/JSON document structures are trees of elements (tags, attributes, text nodes). The Visitor provides a clean way to process these trees without coupling logic to structure. SAX parsers use Visitor-like callbacks for stream-based XML processing.

```java
public interface XmlNodeVisitor {
    void visit(ElementNode element);
    void visit(AttributeNode attribute);
    void visit(TextNode text);
    void visit(CommentNode comment);
}

public class XmlPrintVisitor implements XmlNodeVisitor {
    private int indent = 0;
    public void visit(ElementNode e) {
        System.out.println(" ".repeat(indent) + "<" + e.getName() + ">");
        indent += 2;
        for (XmlNode child : e.getChildren()) child.accept(this);
        indent -= 2;
        System.out.println(" ".repeat(indent) + "</" + e.getName() + ">");
    }
    public void visit(AttributeNode a) {
        System.out.println(" ".repeat(indent) + a.getName() + "=" + a.getValue());
    }
    public void visit(TextNode t) {
        System.out.println(" ".repeat(indent) + t.getContent());
    }
    public void visit(CommentNode c) {
        System.out.println(" ".repeat(indent) + "<!-- " + c.getContent() + " -->");
    }
}
```

This Visitor provides formatted printing. Others could extract data, validate structure, transform to JSON, or compress. The pattern separates document structure from processing logic, making both independently extensible. This is foundational in web frameworks (template processing), data pipelines (format conversion), and API gateways (request/response transformation).

## Q57: How does the Memento pattern support collaborative editing?

**A:** Collaborative editing requires merging concurrent edits from multiple users. The Memento captures individual user states, and a merge strategy combines them. Operational Transformation (OT) records operations as Mementos, transforming each against concurrent operations for consistency.

CRDTs (Conflict-free Replicated Data Types) use inherently mergeable data structures. Each user's state is a CRDT that merges with others without conflicts. The Memento stores the CRDT state; merging is built into the data type.

Both approaches use Memento-like state capture for checkpointing and rollback. If the merge algorithm produces incorrect results, the system rolls back to the last known-good Memento. Google Docs uses OT; Apple Notes and many distributed databases use CRDTs. The Memento pattern provides the foundation for both strategies.

## Q58: What is the Null Object pattern's role in the Decorator pattern?

**A:** The Null Object serves as the base case in a Decorator chain. Decorators wrap objects to add behavior. Without Null Object, the innermost decorator must wrap a real object, which may not always be available. Null Object at the chain's base provides a safe default.

```java
public interface DataSource {
    String read();
    void write(String data);
}

public class NullDataSource implements DataSource {
    public String read() { return ""; }
    public void write(String data) { }
}

public class EncryptionDecorator implements DataSource {
    private final DataSource delegate;
    public EncryptionDecorator(DataSource ds) { this.delegate = ds; }
    public String read() { return decrypt(delegate.read()); }
    public void write(String data) { delegate.write(encrypt(data)); }
}
```

The chain `new EncryptionDecorator(new CompressionDecorator(new NullDataSource()))` encrypts and compresses data, with Null DataSource providing a safe empty default. Without it, the chain requires a real data source at construction time. The pattern is useful in I/O streams (Java's `FilterInputStream` with a `ByteArrayInputStream` as base), logging pipelines, and middleware stacks.

## Q59: How does the Specification pattern handle nested hierarchical data?

**A:** Specifications for nested data traverse relationships to evaluate rules at different levels. A `CustomerWithOrderInCategory` specification checks whether a customer has at least one order in a specific category, traversing customer-order-product relationships.

```java
public class HasOrderInCategory implements Specification<Customer> {
    private final String category;
    public HasOrderInCategory(String category) { this.category = category; }

    public boolean isSatisfiedBy(Customer customer) {
        return customer.getOrders().stream()
            .flatMap(order -> order.getItems().stream())
            .anyMatch(item -> item.getProduct().getCategory().equals(category));
    }
}
```

The traversal is encapsulated within the specification, keeping calling code clean. For database-backed specs, traversal translates to JOIN operations. The challenge is performance — deep traversals with many JOINs can be slow. Indexing, query optimization, and caching mitigate this. The pattern's composability allows complex queries from simple building blocks without raw SQL.

## Q60: How would you implement the Memento pattern for game state?

**A:** A game state includes player positions, inventory, health, level progress, and world state. The Memento captures all of this atomically. For large worlds, differential Mementos store only changes since the last save.

```java
public class GameState {
    private Map<String, Player> players;
    private WorldMap worldMap;
    private List<Quest> activeQuests;

    public Memento save() {
        return new Memento(
            deepCopyPlayers(), worldMap.save(), deepCopyQuests()
        );
    }

    public void restore(Memento memento) {
        this.players = memento.players();
        this.worldMap = memento.worldMap();
        this.activeQuests = memento.quests();
    }

    public record Memento(
        Map<String, Player> players, WorldMap worldMap, List<Quest> quests
    ) {
        Memento {
            players = Map.copyOf(players);
            quests = List.copyOf(quests);
        }
    }
}
```

Defensive copies prevent saved state from being modified after creation. For multiplayer games, the Memento must also capture network state and synchronization data. Game engines often use delta compression — storing only changed entities between snapshots — to reduce save file size while preserving complete state reconstruction.

## Q61: How does the Visitor pattern work with the Interpreter pattern?

**A:** The Interpreter defines a grammar as an AST. The Visitor processes AST nodes. Together, they separate language structure from operations. An expression interpreter defines node types for literals, variables, and operations. An evaluation Visitor computes results. An optimization Visitor simplifies constant expressions. A code-generation Visitor emits target code.

This combination is fundamental to compiler design. The Interpreter's AST provides structure; multiple Visitors provide independent operations. Adding a new pass (type inference, optimization, code generation) means adding a Visitor without modifying node classes. This separation is why compiler frameworks like LLVM and ANTLR use Visitor-based architectures.

The pattern also applies to rule engines, query languages, and domain-specific languages. Each language's grammar defines the AST structure; Visitors define evaluation, compilation, and transformation operations. The Visitor pattern makes the trade-off explicit: adding operations is easy; adding grammar rules updates all Visitors.

## Q62: What is the Null Object pattern's role in API gateways?

**A:** API gateways route requests to backend services. When a service is unavailable, the gateway returns a Null Object response instead of an error. The Null Response implements the same interface as real responses but returns default or empty data, maintaining the API contract.

For health checks, Null Health Objects return "healthy" status when endpoints are unreachable. This prevents cascading failures where one service's health check failure triggers alerts across the system. The Null Health Object provides a conservative default avoiding false alarms.

The pattern extends to rate limiting, circuit breaking, and fallback mechanisms. A rate limiter that cannot check limits (due to cache failure) returns a Null Rate Limit result allowing the request. A circuit breaker in open state returns Null Response from a fallback service. In each case, the Null Object provides degraded but safe behavior.

## Q63: How does the Specification pattern apply to search functionality?

**A:** Search benefits from composable Specifications defining criteria. Each filter is a Specification; combining filters creates complex queries. Specifications translate to database queries, in-memory predicates, or search engine queries.

```java
public class SearchCriteria<T> {
    private Specification<T> specification;

    public SearchCriteria<T> where(Specification<T> spec) {
        this.specification = spec;
        return this;
    }

    public SearchCriteria<T> and(Specification<T> spec) {
        this.specification = this.specification.and(spec);
        return this;
    }

    public List<T> execute(Collection<T> candidates) {
        return candidates.stream()
            .filter(specification::isSatisfiedBy)
            .collect(Collectors.toList());
    }
}
```

For database-backed search, Specifications translate to WHERE clauses. For Elasticsearch, to query DSL. For in-memory, direct evaluation. The pattern abstracts the search mechanism, allowing the same criteria across different backends. This is used in e-commerce filtering, content management, and analytics dashboards.

## Q64: How does the Memento pattern handle undo in a graphical editor?

**A:** A graphical editor's undo uses Mementos to capture canvas state at each action. The canvas contains shapes, layers, transformations, and properties. For performance, differential Mementos store only changed shapes.

```java
public class CanvasEditor {
    private List<Shape> shapes = new ArrayList<>();
    private Deque<CanvasMemento> undoStack = new ArrayDeque<>();

    public void addShape(Shape shape) {
        recordUndo();
        shapes.add(shape);
    }

    public void moveShape(int index, int newX, int newY) {
        recordUndo();
        shapes.get(index).setPosition(newX, newY);
    }

    public void deleteShape(int index) {
        recordUndo();
        shapes.remove(index);
    }

    private void recordUndo() {
        undoStack.push(new CanvasMemento(deepCopyShapes()));
    }

    public void undo() {
        if (!undoStack.isEmpty()) shapes = undoStack.pop().getShapes();
    }
}
```

`deepCopyShapes()` creates independent copies, ensuring undo restores complete state. For large canvases, this is expensive. Differential Mementos, copy-on-write shapes, and region-based snapshots optimize by reducing copied data per undo. Professional editors (Photoshop, Figma) use these optimizations for smooth undo performance with thousands of objects.

## Q65: How does the Visitor pattern enable type-safe downcasting?

**A:** The Visitor eliminates `instanceof` checks and unsafe downcasts. Without Visitor, processing heterogeneous collections requires checking each element's type and casting. This is error-prone and violates open-closed principle.

```java
// Without Visitor: unsafe downcasting
for (Element e : elements) {
    if (e instanceof Paragraph) {
        Paragraph p = (Paragraph) e;
        process(p.getText());
    } else if (e instanceof Heading) {
        Heading h = (Heading) e;
        process(h.getTitle());
    }
}

// With Visitor: type-safe dispatch
for (Element e : elements) {
    e.accept(new ProcessingVisitor());
}
```

Each `visit` method receives the correct type, eliminating casts. This provides compile-time type safety. Adding a new element type produces a compile error for any Visitor that does not handle it, rather than a runtime `ClassCastException`. The pattern centralizes type-specific logic in `visit` methods rather than scattering `instanceof` checks throughout the codebase.

## Q66: What are the memory implications of the Null Object pattern?

**A:** Null Objects consume minimal memory — typically just the object header (16 bytes on 64-bit JVM). For interfaces with many methods, the class adds metadata but only once per classloader. The memory impact is negligible for most applications.

The main consideration is that Null Objects should be shared singletons. Creating multiple `NullLogger` instances wastes memory. A static final field or enum singleton ensures single-instance usage. Java's `Collections.emptyList()` demonstrates this — one shared instance serves all empty list requests.

The pattern also avoids memory overhead from null-checking code paths. Null checks add branches that inhibit JIT optimizations. Null Object's virtual dispatches are direct and inlineable. The net memory effect is typically positive — fewer objects, cleaner code paths, and better JIT optimization outweigh the small Null Object instance cost.

## Q67: How does the Specification pattern handle OR conditions efficiently?

**A:** OR conditions combine specifications that evaluate independently. The `or` default method creates a composite returning true if either sub-specification is satisfied. For in-memory evaluation, OR short-circuits — if the first is true, subsequent evaluations are skipped.

```java
Specification<Product> onSale = new PriceBelow(100)
    .or(new InCategory("Clearance"))
    .or(new HasTag("discount"));
```

For database queries, OR conditions can be optimized. Combining OR conditions on the same field into `IN` clauses (e.g., `category IN ('Electronics', 'Clearance')`) is more efficient than separate ORs. The Specification's `toPredicate` method can detect this optimization.

The `and` method also short-circuits on false. Both short-circuit behaviors are important when sub-specifications are expensive (involving I/O or complex computation). The performance benefit of short-circuiting grows with the number of composed specifications and the cost of individual evaluations.

## Q68: How would you implement the Memento pattern with compression?

**A:** Compressed Mementos reduce storage by compressing state data before storage. This is valuable when Mementos are large or many must be stored.

```java
public class CompressedMemento {
    private final byte[] compressedData;

    public CompressedMemento(byte[] rawData) {
        this.compressedData = compress(rawData);
    }

    public byte[] getData() { return decompress(compressedData); }

    private byte[] compress(byte[] data) {
        Deflater deflater = new Deflater();
        deflater.setInput(data);
        deflater.finish();
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        while (!deflater.finished()) {
            int count = deflater.deflate(buffer);
            bos.write(buffer, 0, count);
        }
        deflater.end();
        return bos.toByteArray();
    }

    private byte[] decompress(byte[] data) {
        Inflater inflater = new Inflater();
        inflater.setInput(data);
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        try {
            while (!inflater.finished()) {
                int count = inflater.inflate(buffer);
                bos.write(buffer, 0, count);
            }
        } catch (DataFormatException e) { throw new RuntimeException(e); }
        inflater.end();
        return bos.toByteArray();
    }
}
```

The trade-off is CPU time versus storage. Text-heavy Mementos achieve 3:1 to 10:1 compression ratios. Binary data compresses less. The optimal level depends on CPU and memory constraints. For network-based Memento storage (distributed undo), compression also reduces bandwidth.

## Q69: How does the Null Object pattern apply to the Proxy pattern?

**A:** The Null Object serves as the default subject in a Proxy. A protection proxy checks access before delegating. When access is denied or the subject is unavailable, the proxy returns a Null Object instead of throwing an exception.

```java
public interface Image {
    byte[] render();
}

public class NullImage implements Image {
    public byte[] render() { return new byte[0]; }
}

public class ProtectionProxy implements Image {
    private final Image real;
    private final User currentUser;

    public ProtectionProxy(Image real, User user) {
        this.real = real;
        this.currentUser = user;
    }

    public byte[] render() {
        if (currentUser.hasPermission("view_images")) {
            return real.render();
        }
        return new NullImage().render();
    }
}
```

The protection proxy returns Null Image when the user lacks permissions, preventing authorization errors from propagating. The Proxy controls access; the Null Object provides safe degradation. This combination is used in security frameworks, content management systems, and access-controlled APIs.

## Q70: What is the relationship between Specification and domain-driven design?

**A:** The Specification pattern is a core building block in Domain-Driven Design (DDD). It encapsulates domain rules as composable objects, aligning with DDD's emphasis on expressing business logic in the domain language.

In DDD, Specifications are used for:
- **Validation**: Ensuring entities meet business invariants before persistence
- **Query building**: Translating domain rules into database queries (Repository pattern)
- **Authorization**: Expressing access control rules in domain terms
- **Business rules**: Encapsulating complex conditional logic that would otherwise be scattered

The pattern supports DDD's ubiquitous language by expressing rules in terms familiar to domain experts. `new PremiumCustomer().and(new ActiveSubscription())` reads naturally to both developers and business stakeholders. This shared understanding reduces miscommunication and ensures the code reflects the actual business rules.

Specifications also support DDD's tactical patterns. Entities use Specifications for invariant checking. Value Objects use them for validation. Aggregates use them for consistency enforcement. The pattern integrates naturally with Repositories for query specification and with Services for business rule composition.

## Q71: How does the Memento pattern work with copy-on-write semantics?

**A:** Copy-on-write (COW) Mementos defer copying until modification occurs. The Memento stores a reference to the original state plus a list of modifications. When the original state changes, only modified portions are copied. This reduces Memento creation cost for cases where many Mementos are created but few are restored.

```java
public class CowMemento<T> {
    private final T originalState;
    private final List<Change<T>> changes;
    private T resolvedState;

    public CowMemento(T state) {
        this.originalState = state;
        this.changes = new ArrayList<>();
        this.resolvedState = state;
    }

    public void recordChange(Function<T, T> changer) {
        resolvedState = changer.apply(resolvedState);
        changes.add(new Change<>(changer));
    }

    public T getState() { return resolvedState; }
}
```

COW Mementos are beneficial when the Originator is modified infrequently relative to Memento creation. The Memento is created cheaply (just a reference), and the copy cost is paid only when the original changes. If the original never changes, the copy cost is zero. This pattern is used in database snapshots, version control systems, and undo mechanisms for large data structures.

## Q72: How does the Visitor pattern support concurrent processing?

**A:** The Visitor pattern can be parallelized by partitioning the element structure and processing partitions concurrently. Each thread receives a subset of elements and applies the same Visitor. The Visitor must be thread-safe or stateless to support concurrent access.

For stateful Visitors (accumulating results), thread-local storage or atomic variables prevent contention. A `ConcurrentVisitor` uses `AtomicInteger` for counters or `ConcurrentLinkedQueue` for collected results. The `accept` method must also be thread-safe if elements can be modified during traversal.

```java
public class ParallelWordCounter implements ElementVisitor<Integer> {
    private final AtomicInteger count = new AtomicInteger(0);

    public Integer visit(Paragraph p) {
        int words = p.getText().split("\\s+").length;
        count.addAndGet(words);
        return words;
    }

    public Integer visit(Heading h) {
        int words = h.getTitle().split("\\s+").length;
        count.addAndGet(words);
        return words;
    }

    public int getTotalCount() { return count.get(); }
}
```

The `AtomicInteger` ensures thread-safe accumulation. For larger parallelism, the element structure is partitioned into subtrees, each processed by a separate thread using `ForkJoinPool`. The results are combined after all partitions complete. This parallel Visitor pattern scales processing across CPU cores for large document structures.

## Q73: What is the Null Object pattern's role in service mesh and microservices?

**A:** In service mesh architectures, Null Objects provide fallback behavior when services are unavailable. A service proxy that cannot reach the target service returns a Null Response instead of propagating the failure. This prevents cascading failures across the microservice ecosystem.

The Null Object implements the same interface as the real service, returning default data or empty results. For a user profile service, the Null Object returns a default profile with anonymous user data. For a recommendation service, it returns generic recommendations. The degradation is graceful — the application continues functioning with reduced capability.

This pattern integrates with circuit breaker and retry mechanisms. When the circuit breaker opens (indicating the service is down), the proxy automatically switches to Null Object responses. When the circuit closes (service recovers), the proxy switches back to real responses. The Null Object provides the bridge between failure detection and recovery.

## Q74: How would you implement the Specification pattern for complex business rules in an insurance system?

**A:** Insurance rules involve complex conditions across multiple entity types. Each rule is a Specification, and policies are composed from rule specifications.

```java
public class EligibleForDiscount implements Specification<Policy> {
    private final double discountThreshold;
    public EligibleForDiscount(double threshold) {
        this.discountThreshold = threshold;
    }
    public boolean isSatisfiedBy(Policy p) {
        return p.getClaimHistory().stream()
            .filter(c -> c.getYear() >= Year.now().getValue() - 3)
            .count() <= 2
            && p.getVehicleAge() <= 5
            && p.getDriverAge() >= 25;
    }
}

public class HighRiskZone implements Specification<Policy> {
    public boolean isSatisfiedBy(Policy p) {
        return p.getGarageLocation().getRiskLevel() == RiskLevel.HIGH;
    }
}

// Complex rule composition
Specification<Policy> standardPolicy = new EligibleForDiscount(500)
    .and(new HighRiskZone().not())
    .and(new ValidLicense())
    .and(new VehicleInsured());
```

Each rule is independently testable and modifiable. The composition reads like a business document: "eligible for discount AND not in high risk zone AND valid license AND vehicle insured." This readability enables business stakeholders to verify that code matches documented policies. Changes to rules modify individual Specifications without affecting the overall policy composition.

## Q75: How does the Memento pattern interact with garbage collection in Java?

**A:** Mementos create additional object references that affect garbage collection. Each Memento holds references to the Originator's state, preventing those objects from being collected even if the Originator no longer needs them. Long undo histories keep many Mementos alive, retaining old state objects.

The GC impact depends on Memento lifecycle. If Mementos are stored in a bounded stack (limited undo depth), the retained state is bounded. If Mementos are stored indefinitely (unlimited undo or persistent storage), the retained state grows without bound, potentially causing memory pressure.

Weak references and soft references can mitigate this. Mementos stored with soft references are reclaimed when memory is low. Mementos with weak references are reclaimed when no strong references exist. The trade-off is that soft/weak Mementos may be unavailable when the user tries to undo. For most applications, a bounded undo stack with strong references provides the best balance of functionality and memory safety.

The GC also benefits from Memento patterns that use immutable state. Immutable objects are candidates for sharing and deduplication, reducing the number of distinct objects the GC must track. Immutable Mementos that reference shared immutable state consume less memory than mutable Mementos with deep copies.

## Q76: How would you implement the Memento pattern for a distributed system?

**A:** In distributed systems, the Memento pattern extends to cross-node state management. Each service node creates local Mementos, and a coordinator aggregates them into a global snapshot. This is the Chandy-Lamport algorithm — a distributed snapshot protocol that captures consistent global state without stopping the system.

Each node captures its local state as a Memento and records incoming messages on special marker channels. When all nodes have captured state and all marker messages have been processed, the global snapshot is complete. This provides a consistent view of the distributed system at a point in time, useful for debugging, checkpointing, and recovery.

The challenge is consistency. A naive approach (each node snapshots independently) captures inconsistent state — Node A's snapshot might reflect a message that Node B has not yet processed. The Chandy-Lamport protocol ensures that the snapshot captures either the message as sent or as received, but not a partial state. For simpler systems, coordinated snapshots using a consensus protocol (Raft, Paxos) provide global consistency.

## Q77: How does the Visitor pattern apply to abstract grammar interpretation?

**A:** Abstract grammar interpretation uses the Visitor pattern to separate grammar definition from interpretation. The grammar defines node types (expressions, statements, declarations). Each interpretation (evaluation, compilation, optimization) is a Visitor. The Visitor pattern enables multiple interpretations without modifying grammar nodes.

A type-checking Visitor traverses the AST and infers types for each expression. An optimization Visitor simplifies constant expressions and eliminates dead code. A code-generation Visitor emits target assembly or bytecode. Each Visitor is independent — adding a new optimization does not affect type checking or code generation.

The pattern also supports interpreter debugging. A `DebugVisitor` traverses the AST and logs each node's evaluation, providing execution tracing. A `PrettyPrintVisitor` formats the AST for human reading. These diagnostic Visitors are invaluable during language development and do not affect the production interpretation pipeline.

## Q78: What is the Null Object pattern's role in the Template Method pattern?

**A:** The Template Method pattern defines an algorithm skeleton with abstract steps. Subclasses override specific steps. When a step is optional, a Null Object provides a no-op default, avoiding abstract methods that force every subclass to implement empty methods.

```java
public abstract class DataProcessor {
    public final void process() {
        readData();
        transformData();
        optionalValidation(); // Null Object default
        writeData();
        optionalCleanup(); // Null Object default
    }

    protected abstract void readData();
    protected abstract void transformData();
    protected abstract void writeData();

    protected void optionalValidation() { } // Null Object
    protected void optionalCleanup() { } // Null Object
}

public class SimpleProcessor extends DataProcessor {
    protected void readData() { /* read */ }
    protected void transformData() { /* transform */ }
    protected void writeData() { /* write */ }
    // optionalValidation and optionalCleanup use Null Object defaults
}
```

The Null Object (empty method body) provides a safe default for optional steps. Subclasses that need the step override it; others inherit the no-op. This is simpler than abstract methods with Null Object implementations and aligns with the Template Method pattern's intent — varying specific steps while keeping the algorithm structure fixed.

## Q79: How does the Specification pattern handle fuzzy or probabilistic rules?

**A:** Standard Specifications return boolean results. For fuzzy rules that return degrees of membership (0.0 to 1.0), the Specification interface is extended with a `score` method. Composite specifications combine scores using fuzzy logic operators (min for AND, max for OR, 1-minus for NOT).

```java
public interface FuzzySpecification<T> {
    double score(T candidate);

    default FuzzySpecification<T> and(FuzzySpecification<T> other) {
        return candidate -> Math.min(this.score(candidate), other.score(candidate));
    }

    default FuzzySpecification<T> or(FuzzySpecification<T> other) {
        return candidate -> Math.max(this.score(candidate), other.score(candidate));
    }

    default FuzzySpecification<T> not() {
        return candidate -> 1.0 - this.score(candidate);
    }
}

public class TemperatureComfort implements FuzzySpecification<Room> {
    public double score(Room room) {
        double temp = room.getTemperature();
        if (temp < 18) return 0.0;
        if (temp > 26) return 0.0;
        if (temp >= 20 && temp <= 24) return 1.0;
        return temp < 20 ? (temp - 18) / 2.0 : (26 - temp) / 2.0;
    }
}
```

Fuzzy Specifications provide a smooth transition between states rather than hard boundaries. A room at 19 degrees is partially comfortable (score 0.5) rather than completely uncomfortable. This is useful in recommendation systems, comfort control, and any domain where binary rules are too rigid.

## Q80: How does the Memento pattern support checkpoint/restart in long-running processes?

**A:** Long-running processes (ETL pipelines, scientific computations, batch jobs) use Memento-style checkpoints to enable restart after failures. Each processing stage creates a Memento capturing the current state. If the process fails, it restarts from the last successful checkpoint rather than from the beginning.

The checkpoint frequency is tuned based on failure rate and checkpoint cost. High checkpoint frequency reduces restart time but increases overhead. Low checkpoint frequency reduces overhead but increases restart time. Adaptive checkpointing adjusts frequency based on observed failure patterns.

```java
public class CheckpointProcessor<T> {
    private final List<ProcessingStage<T>> stages;
    private final CheckpointStore store;

    public void process(T initialState) {
        T state = store.hasCheckpoint() ? store.loadCheckpoint() : initialState;
        int startStage = store.hasCheckpoint() ? store.getStageIndex() : 0;

        for (int i = startStage; i < stages.size(); i++) {
            state = stages.get(i).process(state);
            store.saveCheckpoint(i + 1, state);
        }
    }
}
```

The `CheckpointStore` persists Mementos to durable storage (disk, database, distributed cache). On restart, the last checkpoint is loaded and processing resumes from the corresponding stage. This pattern is used in Apache Spark ( RDD checkpoints), Flink (state snapshots), and database systems (Write-Ahead Log recovery).

## Q81: How does the Visitor pattern handle generic element types?

**A:** Generic elements parameterize the element type, allowing Visitors to work with typed element hierarchies. The Visitor interface uses the generic parameter for type-safe dispatch.

```java
public interface GenericElement<T> {
    <R> R accept(GenericVisitor<T, R> visitor);
}

public interface GenericVisitor<T, R> {
    R visit(GenericElement<T> element);
}

public class TypedElement<T> implements GenericElement<T> {
    private final T value;
    public TypedElement(T value) { this.value = value; }
    public <R> R accept(GenericVisitor<T, R> visitor) {
        return visitor.visit(this);
    }
    public T getValue() { return value; }
}
```

The generic approach provides compile-time type safety across element and visitor types. However, Java's type erasure limits runtime type dispatch for generic parameters. The workaround is to use class tokens or type tags alongside generic parameters. This pattern is useful in type-safe heterogeneous containers and generic AST processing.

## Q82: What is the Null Object pattern's role in the Factory Method pattern?

**A:** The Factory Method pattern creates objects without specifying their concrete class. When the factory cannot create the requested object (invalid parameters, resource unavailability), it returns a Null Object instead of null. This preserves the factory's contract — callers always receive a valid object.

```java
public interface DatabaseConnection {
    void execute(String query);
}

public class NullConnection implements DatabaseConnection {
    public void execute(String query) {
        throw new UnsupportedOperationException("No database configured");
    }
}

public class DatabaseFactory {
    public static DatabaseConnection create(Config config) {
        if (config.getDbUrl() == null) return new NullConnection();
        return new RealConnection(config);
    }
}
```

The Null Connection either does nothing or throws a controlled exception, depending on the domain. For non-critical operations (logging to a database), the Null Connection silently discards queries. For critical operations, it throws a meaningful exception. The factory's contract is preserved — callers never receive null, and the Null Object's behavior is documented and predictable.

## Q83: How does the Specification pattern integrate with caching?

**A:** Specification-based queries can be cached to avoid redundant computation. Each Specification produces a cache key derived from its type and parameters. The cache stores results keyed by Specification identity, enabling cache hits for repeated identical queries.

```java
public class CachingSpecificationRepository<T> {
    private final Repository<T> delegate;
    private final Cache<Specification<T>, List<T>> cache;

    public List<T> findBy(Specification<T> spec) {
        return cache.get(spec, s -> delegate.findBy(s));
    }
}
```

The cache key must correctly identify equal Specifications. Specifications implementing proper `equals()` and `hashCode()` based on their parameters ensure cache correctness. Composite Specifications derive their equality from their components. This integration provides O(1) lookups for repeated queries while maintaining the Specification pattern's composability.

For database-backed Specifications, the cache stores query results rather than Specifications. The cache key is the SQL query string or a hash of the Specification's predicate. Cache invalidation is triggered by data modifications. This layer between Specification and database provides significant performance improvement for read-heavy workloads with repeated query patterns.

## Q84: How does the Memento pattern handle serialization across different versions?

**A:** Version compatibility is critical for persistent Mementos. When the Originator's class evolves (fields added or removed), old Mementos must still be restorable. The Memento must handle missing fields (new version restoring old Memento) and extra fields (old version restoring new Memento).

Java's default serialization handles this through `serialVersionUID`. If the UID matches, deserialization proceeds with missing fields defaulting to null and extra fields ignored. If the UID does not match, deserialization fails. For custom Memento implementations, versioned serialization formats handle this explicitly.

A practical approach uses JSON or Protocol Buffers with schema evolution. Adding a field with a default value is backward-compatible. Removing a field is forward-compatible if old readers ignore unknown fields. The Memento class includes a version identifier, and the restoration method handles each version's format. This ensures that Mementos created by older versions can be restored by newer versions and vice versa.

## Q85: How does the Visitor pattern support tree transformation?

**A:** Visitors can transform trees by returning new element instances instead of modifying existing ones. A transformation Visitor takes an element and returns a new element with modified properties. This functional approach preserves the original tree while creating a transformed copy.

```java
public interface TransformVisitor {
    Element visit(Paragraph p);
    Element visit(Heading h);
    Element visit(Image i);
}

public class UppercaseTransform implements TransformVisitor {
    public Element visit(Paragraph p) {
        return new Paragraph(p.getText().toUpperCase());
    }
    public Element visit(Heading h) {
        return new Heading(h.getTitle().toUpperCase(), h.getLevel());
    }
    public Element visit(Image i) { return i; }
}
```

For composite structures, the transformation recursively applies to children. A composite element visits each child, collects transformed children, and returns a new composite with the transformed children. This creates a new tree with the same structure but modified content, preserving immutability.

The pattern is used in compiler optimization passes (AST-to-AST transformation), template engines (template-to-output transformation), and data processing pipelines (input-to-output transformation). The Visitor's type safety ensures that each element type is correctly transformed.

## Q86: What is the Null Object pattern's role in the State pattern?

**A:** The State pattern allows an object to change behavior when its internal state changes. The Null Object provides a default state implementation that handles events with no-op behavior. This eliminates null checks when the state is not initialized or has been cleaned up.

```java
public interface DocumentState {
    void type(Document doc, String text);
    void save(Document doc);
    void close(Document doc);
}

public class NullDocumentState implements DocumentState {
    public void type(Document doc, String text) { }
    public void save(Document doc) { }
    public void close(Document doc) { }
}

public class DraftState implements DocumentState {
    public void type(Document doc, String text) { doc.append(text); }
    public void save(Document doc) { doc.persist(); }
    public void close(Document doc) { doc.setState(new NullDocumentState()); }
}
```

When a document is closed, it transitions to NullDocumentState. Subsequent operations (type, save) silently do nothing. This prevents errors from operations on closed documents without null checks. The Null State provides a clean terminal state that preserves the State pattern's interface contract.

## Q87: How does the Specification pattern handle cross-entity relationships?

**A:** Cross-entity Specifications evaluate rules spanning multiple entity types. A "customer with overdue orders" Specification traverses from Customer to Order, evaluating criteria on the related entity. The traversal is encapsulated within the Specification, keeping the calling code clean.

```java
public class HasOverdueOrders implements Specification<Customer> {
    private final int overdueDays;
    public HasOverdueOrders(int days) { this.overdueDays = days; }

    public boolean isSatisfiedBy(Customer customer) {
        return customer.getOrders().stream()
            .anyMatch(order -> order.isOverdue(overdueDays));
    }
}
```

For database-backed Specifications, cross-entity evaluation translates to JOIN queries. The Specification's `toPredicate` method constructs the appropriate JOIN and WHERE clauses. Spring Data JPA's Criteria API handles this translation automatically. The Specification encapsulates the relationship traversal, making complex cross-entity queries composable and testable.

The pattern supports nested traversals (Customer -> Order -> OrderItem -> Product) through nested Specifications. Each level of traversal is a separate Specification, and composition creates multi-hop queries. This is valuable in enterprise applications with complex entity relationships.

## Q88: How does the Memento pattern support event replay and debugging?

**A:** Event replay uses Mementos to capture system state at each step, enabling step-by-step debugging. Each Memento records the state before and after an operation, creating a complete execution trace. A debugger can navigate forward and backward through the trace, examining state at each point.

```java
public class DebuggableSystem {
    private final List<StateSnapshot> trace = new ArrayList<>();
    private int currentStep = -1;

    public void execute(Action action) {
        if (currentStep < trace.size() - 1) {
            trace.subList(currentStep + 1, trace.size()).clear();
        }
        trace.add(new StateSnapshot(captureState()));
        action.execute(this);
        trace.add(new StateSnapshot(captureState()));
        currentStep = trace.size() - 1;
    }

    public void stepBack() {
        if (currentStep > 0) {
            currentStep -= 2;
            restoreState(trace.get(currentStep).state());
        }
    }

    public void stepForward() {
        if (currentStep < trace.size() - 2) {
            currentStep += 2;
            restoreState(trace.get(currentStep).state());
        }
    }
}
```

The trace stores state snapshots at each step. Navigation moves forward and backward through the trace, restoring state at each position. This provides a time-travel debugging capability that is invaluable for understanding complex state transitions and reproducing bugs. Tools like Redux DevTools and Chrome DevTools use this approach for frontend debugging.

## Q89: What is the Null Object pattern's role in the Chain of Responsibility with logging?

**A:** In logging chains, each handler processes log messages at a specific level. A Null Handler at the chain's end provides a default action (discard, write to fallback) when no handler processes the message. This ensures every message is handled without post-loop checks.

```java
public interface LogHandler {
    void handle(LogEvent event);
    boolean canHandle(LogEvent event);
}

public class NullLogHandler implements LogHandler {
    public void handle(LogEvent event) {
        // discard silently or write to emergency log
    }
    public boolean canHandle(LogEvent event) { return true; }
}

public class LogChain {
    private final List<LogHandler> handlers = new ArrayList<>();

    public void process(LogEvent event) {
        for (LogHandler handler : handlers) {
            if (handler.canHandle(event)) {
                handler.handle(event);
                return;
            }
        }
    }
}
```

The Null Handler at the chain's end is the catch-all. If no real handler matches, the Null Handler processes the event. This pattern is used in logging frameworks (Log4j, Logback), event processing pipelines, and middleware chains. The Null Handler provides guaranteed message processing, preventing silent message loss.

## Q90: How does the Specification pattern handle dynamic rule composition at runtime?

**A:** Dynamic composition allows rules to be built at runtime from configuration, user input, or database-driven rule definitions. The Specification pattern supports this through its compositional nature — specifications are objects that can be combined programmatically.

```java
public class DynamicRuleEngine<T> {
    private final Map<String, Specification<T>> registry = new HashMap<>();

    public void register(String name, Specification<T> spec) {
        registry.put(name, spec);
    }

    public Specification<T> compose(List<String> ruleNames, String operator) {
        Specification<T> result = null;
        for (String name : ruleNames) {
            Specification<T> spec = registry.get(name);
            if (spec == null) throw new IllegalArgumentException("Unknown rule: " + name);
            result = result == null ? spec
                : "AND".equals(operator) ? result.and(spec) : result.or(spec);
        }
        return result;
    }
}
```

Rules are registered by name and composed at runtime based on configuration. The engine reads rule names from a database or configuration file, looks up the corresponding Specifications, and composes them. This enables non-developers to modify business rules by changing configuration without code changes.

The pattern supports complex dynamic scenarios: rules loaded from JSON configurations, rules assembled from user selections in a UI, and rules modified by A/B testing frameworks. The Specification's object nature makes it naturally composable at runtime, unlike static conditional logic.

## Q91: How does the Memento pattern interact with persistence layers?

**A:** Mementos can be persisted to databases, file systems, or distributed caches for cross-session recovery. The persistence layer serializes Mementos to durable storage and deserializes them on retrieval. The key consideration is the mapping between Memento objects and storage format.

For relational databases, Mementos can be stored as BLOBs (binary serialization) or normalized into tables (structured storage). BLOBs are simple but opaque; normalized storage enables querying and indexing. The choice depends on whether Mementos need to be searched or just restored.

```java
public class PersistentMementoStore {
    private final JdbcTemplate jdbc;

    public void save(String sessionId, TextEditor.Memento memento) {
        jdbc.update(
            "INSERT INTO editor_mementos (session_id, content, cursor_pos, created_at) "
            + "VALUES (?, ?, ?, ?)",
            sessionId, serialize(memento.getContent()),
            memento.getCursorPosition(), LocalDateTime.now()
        );
    }

    public TextEditor.Memento loadLatest(String sessionId) {
        return jdbc.queryForObject(
            "SELECT content, cursor_pos FROM editor_mementos "
            + "WHERE session_id = ? ORDER BY created_at DESC LIMIT 1",
            (rs, i) -> new TextEditor.Memento(
                deserialize(rs.getBytes("content")),
                rs.getInt("cursor_pos")
            ),
            sessionId
        );
    }
}
```

The persistence layer handles serialization, storage, and retrieval. Mementos stored in databases benefit from database features (transactions, replication, backup). The trade-off is serialization overhead and storage format coupling. For high-performance applications, in-memory caches (Redis, Hazelcast) provide faster persistence with eventual durability.

## Q92: How does the Visitor pattern support instrumentation and profiling?

**A:** The Visitor pattern is ideal for adding instrumentation without modifying business logic. An instrumentation Visitor wraps each element's `accept` method with timing, counting, or logging. This provides observability into the Visitor's execution without changing the element or operation code.

```java
public class ProfiledVisitor<T> implements ElementVisitor<T> {
    private final ElementVisitor<T> delegate;
    private final Map<String, Long> timings = new ConcurrentHashMap<>();

    public ProfiledVisitor(ElementVisitor<T> delegate) {
        this.delegate = delegate;
    }

    public T visit(Paragraph p) {
        long start = System.nanoTime();
        T result = delegate.visit(p);
        timings.merge("Paragraph", System.nanoTime() - start, Long::sum);
        return result;
    }

    public T visit(Heading h) {
        long start = System.nanoTime();
        T result = delegate.visit(h);
        timings.merge("Heading", System.nanoTime() - start, Long::sum);
        return result;
    }

    public Map<String, Long> getTimings() { return timings; }
}
```

The `ProfiledVisitor` wraps a real Visitor and records execution time per element type. The timings map shows which element types consume the most processing time. This pattern is used in compiler optimization profiling, database query analysis, and application performance monitoring. The instrumentation is transparent to the business logic, enabling profiling in production without code changes.

## Q93: What is the Null Object pattern's role in reactive streams?

**A:** In reactive streams (Reactor, RxJava), Null Objects provide default values for empty streams. Instead of checking whether a stream is empty before processing, code uses a Null Object that provides a default emission. This eliminates empty-stream checks in reactive pipelines.

```java
public interface ReactiveService {
    Mono<User> findUser(String id);
}

public class NullReactiveService implements ReactiveService {
    public Mono<User> findUser(String id) {
        return Mono.just(User.anonymous());
    }
}
```

The Null Service returns a default user (anonymous) instead of an empty Mono. This prevents downstream operators from receiving no data and defaulting to empty/error states. The pattern integrates with reactive's error handling — the Null Object provides a valid data path instead of an error path.

In reactive streams, the `defaultIfEmpty` and `switchIfEmpty` operators serve a similar purpose, providing fallback values when streams are empty. The Null Object pattern generalizes this concept to entire services and components, not just individual stream operations.

## Q94: How does the Specification pattern work with event-driven architectures?

**A:** In event-driven architectures, Specifications filter events based on criteria. Each event handler uses a Specification to determine whether it should process a given event. This decouples event routing from event processing.

```java
public interface EventRouter {
    void route(Event event);
}

public class SpecificationEventRouter implements EventRouter {
    private final Map<Specification<Event>, EventHandler> handlers = new LinkedHashMap<>();

    public void register(Specification<Event> spec, EventHandler handler) {
        handlers.put(spec, handler);
    }

    public void route(Event event) {
        for (var entry : handlers.entrySet()) {
            if (entry.getKey().isSatisfiedBy(event)) {
                entry.getValue().handle(event);
            }
        }
    }
}
```

Events are routed to handlers based on Specification evaluation. A `HighPriorityEvent` Specification routes urgent events to immediate processing handlers. A `UserActionEvent` Specification routes user interactions to analytics handlers. The Specifications are composable — a handler can process events matching multiple criteria.

This pattern is used in event sourcing systems, CQRS architectures, and message queue consumers. The Specifications provide a declarative way to define event routing rules without hardcoding event type checks. New event types are handled by registering new Specifications, not by modifying routing logic.

## Q95: How does the Memento pattern support state synchronization in multiplayer games?

**A:** Multiplayer games require state synchronization between clients and servers. The Memento pattern captures game state for transmission. The server periodically broadcasts state Mementos to clients, which restore their local state from the received Mementos.

For bandwidth efficiency, differential Mementos transmit only state changes. The server maintains a full state and creates differential Mementos by comparing consecutive snapshots. Clients apply differentials to their local state, achieving synchronization without receiving the full state each time.

The challenge is latency. By the time a client receives and applies a Memento, the game state has changed. Prediction and interpolation compensate — clients predict intermediate states and smoothly interpolate when the authoritative Memento arrives. The Memento provides the ground truth; prediction provides the responsive feel.

For competitive games, the server is authoritative and sends state corrections. Clients that deviate from the server's Memento are corrected. The Memento pattern provides the framework for this correction mechanism, ensuring all clients converge to the same game state.

## Q96: How does the Visitor pattern support code generation from ASTs?

**A:** Code generation is a Visitor that traverses an AST and emits target language code. Each element type has a corresponding `visit` method that generates the appropriate code for that construct.

```java
public class JavaCodeGenerator implements ElementVisitor<String> {
    public String visit(Paragraph p) {
        return "// " + p.getText().replace("\n", "\n// ");
    }

    public String visit(Heading h) {
        return "public " + getReturnType(h) + " " + h.getTitle() + "() {";
    }

    public String visit(BinaryExpression b) {
        return b.getLeft().accept(this) + " " + b.getOperator() + " "
             + b.getRight().accept(this);
    }

    public String visit(FunctionDeclaration f) {
        StringBuilder sb = new StringBuilder();
        sb.append("public ").append(f.getReturnType()).append(" ")
          .append(f.getName()).append("(");
        // append parameters
        sb.append(") {\n");
        for (Element body : f.getBody()) {
            sb.append("    ").append(body.accept(this)).append(";\n");
        }
        sb.append("}");
        return sb.toString();
    }
}
```

Each `visit` method generates code specific to its element type. Composite elements recursively generate code for their children. The Visitor accumulates generated code strings that form the complete output. This pattern is used in compiler backends, template engines, and code generators (like JavaPoet and ANTLR's code generation templates).

## Q97: What is the Null Object pattern's impact on security auditing?

**A:** Null Objects can affect security auditing by silently handling operations that should be logged. A Null Logger that discards log messages prevents security-relevant events from being recorded. This can create audit gaps that violate compliance requirements.

The solution is to make Null Objects audit-aware. A Null Logger that discards operational logs still records security-critical events. A Null Access Controller that denies access still logs the denial attempt. The Null Object's no-op behavior applies to non-security operations while preserving security-relevant audit trails.

```java
public class SecurityAwareNullLogger implements Logger {
    private final AuditLogger auditLogger;

    public SecurityAwareNullLogger(AuditLogger audit) {
        this.auditLogger = audit;
    }

    public void log(String message) { } // discard operational logs
    public void error(String message) { } // discard error logs
    public void setLevel(int level) { }

    // Security-critical methods still audit
    public void logAccess(String user, String resource) {
        auditLogger.recordAccess(user, resource);
    }
}
```

The `SecurityAwareNullLogger` discards operational messages (its Null Object behavior) but records security events through the audit logger. This balances the Null Object's simplicity with security compliance requirements.

## Q98: How does the Memento pattern work with immutable data structures in functional programming?

**A:** Functional programming's immutable data structures simplify Mementos because immutable objects are inherently safe to store and restore. An immutable Originator's Memento is the object itself — since it cannot change, it preserves its state without copying.

In Clojure, atoms and refs provide state management with built-in snapshot capabilities. `deref` on an atom returns the current immutable value; storing it creates a snapshot. Restoration replaces the atom's value with the snapshot. The immutable data structure ensures the snapshot is never corrupted by subsequent changes.

In Haskell, the `IORef` monad provides mutable state, but the `State` monad uses immutable values. Each state transition produces a new value; the old value is preserved as a Memento. The type system enforces that old values cannot be modified, providing Memento correctness guarantees at compile time.

The functional approach trades runtime copying overhead for compile-time safety. Immutable Mementos are cheap to create (just a reference) and safe to share (no deep copy needed). The trade-off is that each state transition creates new objects, increasing GC pressure. Persistent data structures (hash array mapped tries) mitigate this by sharing structure between old and new versions.

## Q99: How does the Specification pattern support A/B testing and experimentation?

**A:** Specifications define variant assignment for A/B tests. Each variant is a Specification that evaluates user attributes to determine group membership. The experiment framework evaluates Specifications to route users to different treatments.

```java
public class ExperimentVariant implements Specification<User> {
    private final double trafficPercentage;
    private final long seed;

    public ExperimentVariant(double percentage, long experimentId) {
        this.trafficPercentage = percentage;
        this.seed = experimentId;
    }

    public boolean isSatisfiedBy(User user) {
        double hash = Math.abs(user.getId().hashCode() * seed % 10000) / 10000.0;
        return hash < trafficPercentage;
    }
}
```

The Specification uses a deterministic hash to assign users to variants. The same user always receives the same variant, ensuring consistency across sessions. The traffic percentage controls the experiment's sample size. Different Specifications define control and treatment groups.

The pattern supports complex experimentation: multivariate tests (multiple Specifications per experiment), stacked experiments (sequential Specifications filtering users), and feature flags (Specifications enabling features for specific user segments). The composable nature of Specifications enables sophisticated experimentation without modifying application logic.

## Q100: How do these four patterns collectively improve software architecture?

**A:** These four patterns address complementary architectural concerns. Memento provides state management and temporal navigation. Visitor enables operations without structural modification. Null Object eliminates null-related fragility. Specification encapsulates and composes business rules. Together, they create a robust behavioral design toolkit.

At the architectural level, these patterns promote separation of concerns. Memento separates state capture from state management. Visitor separates operations from data structures. Null Object separates default behavior from business logic. Specification separates rules from the objects they evaluate. Each pattern reduces coupling between components.

The patterns compose synergistically. Mementos use Null Objects for default states. Visitors evaluate Specifications for filtering. Specifications operate on Memento-captured data. Null Objects implement Visitor interfaces for no-op operations. This composability enables architectures where each concern is handled by the appropriate pattern, resulting in systems that are easier to understand, test, and maintain.

The collective impact is measurable: reduced defect density (fewer null-pointer errors, fewer state corruption bugs), improved maintainability (changes localized to specific patterns), enhanced testability (each pattern provides clear test seams), and better team communication (shared pattern vocabulary). For senior engineers at top companies, mastering these patterns is essential for designing systems that scale in complexity while remaining manageable.
