# Design Patterns Application Interviews — 100 Interview Q&A

## Q1: Which pattern should you use to create objects without specifying exact classes?

**A:** The **Factory Method** pattern is the standard answer. It defines an interface for creating an object but lets subclasses decide which class to instantiate. The factory method defers instantiation to subclasses, allowing the system to work with any product class that is created by the factory. This promotes loose coupling because the client code depends on an abstract factory interface rather than concrete classes.

In practice, the Abstract Factory pattern extends this concept to families of related objects. If you need to create a single type of object, Factory Method suffices. If you need to create families of related or dependent objects (e.g., cross-platform UI widgets), Abstract Factory is the right choice. The Factory Method uses inheritance (subclass overrides the factory), while Abstract Factory uses composition (the factory is injected as an object).

**Example:**
```java
// Factory Method
abstract class LoggerFactory {
    abstract Logger createLogger();
    void writeLog(String msg) {
        Logger logger = createLogger();
        logger.log(msg);
    }
}

class FileLoggerFactory extends LoggerFactory {
    Logger createLogger() { return new FileLogger(); }
}

class ConsoleLoggerFactory extends LoggerFactory {
    Logger createLogger() { return new ConsoleLogger(); }
}
```

## Q2: When should you use the Strategy pattern versus the Template Method pattern?

**A:** Use **Strategy** when you want to swap entire algorithms at runtime and the algorithms are truly interchangeable implementations of the same interface. Use **Template Method** when you have a fixed algorithm skeleton with certain steps that vary, and the variation is through inheritance within the same class hierarchy. Strategy favors composition (the algorithm is an injected object); Template Method favors inheritance (subclasses override specific steps).

Strategy is more flexible because you can change the algorithm at runtime by swapping the strategy object. Template Method is simpler when there is a single algorithm with a few variable steps and the class hierarchy is stable. The key distinction: Strategy replaces the entire algorithm; Template Method replaces parts of it. If the variation is in a single axis (e.g., different sorting algorithms), Strategy is cleaner. If the variation is multiple steps of a fixed sequence (e.g., different report generators with fixed step order), Template Method is more natural.

**Example:**
```java
// Strategy: swap entire algorithm
interface SortStrategy {
    void sort(int[] data);
}
class QuickSort implements SortStrategy { /* ... */ }
class MergeSort implements SortStrategy { /* ... */ }

// Template Method: fixed skeleton, variable steps
abstract class DataMiner {
    final void mine() {
        openFile();
        extractData();
        parseData();
        analyzeData();
        closeFile();
    }
    abstract void extractData();
    abstract void parseData();
    void openFile() { /* fixed */ }
    void analyzeData() { /* fixed */ }
    void closeFile() { /* fixed */ }
}
```

## Q3: Which pattern provides a one-to-many dependency for state updates?

**A:** The **Observer** pattern defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically. This is the foundation of event-driven and publish-subscribe architectures. The subject maintains a list of observers and provides `attach`, `detach`, and `notify` methods.

The Observer pattern decouples the subject from its observers — the subject does not know the concrete class of its observers, only that they implement the Observer interface. This allows observers to be added or removed at runtime without modifying the subject. The trade-off is that notification order is typically undefined, and if an observer fails, it may affect the subject or other observers. The mediator pattern is an alternative when observers need to communicate with each other rather than just receiving updates from the subject.

**Example:**
```java
interface Observer {
    void update(String event);
}

class EventEmitter {
    private List<Observer> observers = new ArrayList<>();
    void attach(Observer o) { observers.add(o); }
    void detach(Observer o) { observers.remove(o); }
    void notifyAll(String event) {
        for (Observer o : observers) o.update(event);
    }
}
```

## Q4: Under what conditions is the Singleton pattern justified?

**A:** Singleton is justified when exactly one instance of a class is required across the entire application, AND that instance has genuine global state that must be shared. Common valid use cases include thread pools, cache managers, registry services, and configuration holders. The key justification is when creating multiple instances would be wasteful (resource-intensive objects) or semantically incorrect (a single coordinator for a subsystem).

However, Singleton is widely overused and often considered an anti-pattern in modern design. It introduces global state, makes testing difficult (hard to mock or replace), and creates hidden dependencies. In dependency-injected frameworks like Spring, managed singleton scope replaces the traditional Singleton pattern. The modern approach is to let the DI container manage instance count rather than encoding it in the class itself. Use Singleton only when you genuinely need exactly one instance and have no DI framework available.

**Example:**
```java
// Thread-safe Singleton with double-checked locking
class ConnectionPool {
    private static volatile ConnectionPool instance;
    private final List<Connection> pool;

    private ConnectionPool() {
        pool = new ArrayList<>(10);
        // initialize connections
    }

    static ConnectionPool getInstance() {
        if (instance == null) {
            synchronized (ConnectionPool.class) {
                if (instance == null) {
                    instance = new ConnectionPool();
                }
            }
        }
        return instance;
    }
}
```

## Q5: Which pattern allows adding responsibilities to objects dynamically?

**A:** The **Decorator** pattern attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality. Unlike inheritance, which adds behavior at compile time and applies to all instances, Decorators can add behavior to individual objects at runtime and can be composed in any combination.

A decorator wraps the original object and implements the same interface, forwarding calls to the wrapped object and optionally adding behavior before or after. Multiple decorators can be stacked, each adding one concern (logging, authentication, compression, caching). This follows the Single Responsibility Principle — each decorator handles one concern. The trade-off is that many small decorator classes can be confusing to debug, and the order of decoration matters.

**Example:**
```java
interface DataSource {
    void writeData(String data);
    String readData();
}

class FileDataSource implements DataSource { /* base implementation */ }

class EncryptionDecorator implements DataSource {
    private DataSource wrapped;
    EncryptionDecorator(DataSource source) { this.wrapped = source; }
    public void writeData(String data) {
        wrapped.writeData(encrypt(data));
    }
    public String readData() { return decrypt(wrapped.readData()); }
    // encrypt/decrypt methods...
}

// Usage: stacked decorators
DataSource source = new CompressionDecorator(
    new EncryptionDecorator(
        new FileDataSource("data.txt")));
```

## Q6: When should you use the Factory Method pattern over direct construction?

**A:** Use Factory Method when the creation logic is complex, when the exact type of object to create is determined at runtime, or when you want to return objects of different subtypes from the same creation method. Direct construction (`new ClassName()`) ties the client to a specific class, while Factory Method returns an interface or abstract type, keeping the client decoupled from concrete implementations.

Factory Method is also appropriate when object creation involves setup that clients should not know about (connection pooling, caching, resource allocation). The factory can return cached instances, create objects from different pools, or configure them with dependencies. Additionally, when you want to enforce invariants during creation (e.g., ensuring all required fields are set), a factory method provides a single controlled entry point.

**Example:**
```java
// Direct construction: tightly coupled
// Button btn = new WindowsButton(); // client knows concrete type

// Factory Method: decoupled
interface Button { void render(); }

class ButtonFactory {
    static Button create(String type) {
        return switch (type) {
            case "windows" -> new WindowsButton();
            case "mac" -> newMacButton();
            default -> throw new IllegalArgumentException(type);
        };
    }
}
```

## Q7: Which pattern encapsulates a request as an object?

**A:** The **Command** pattern encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations. The command object packages the receiver (the object that performs the work) along with the action (the operation to perform) into a single object.

Command is essential when you need to decouple the invoker (the object that triggers the action) from the receiver (the object that performs it). It enables queuing commands (execute later), logging commands (for audit trails or replay), and composite commands (macro operations). The undo/redo capability is a natural extension — each command stores enough state to reverse itself. The trade-off is increased complexity: every action requires a command class, which can be verbose for simple operations.

**Example:**
```java
interface Command {
    void execute();
    void undo();
}

class TextEditor {
    private StringBuilder buffer = new StringBuilder();
    void insert(String text, int pos) { buffer.insert(pos, text); }
    void delete(int pos, int len) { buffer.delete(pos, pos + len); }
    String getText() { return buffer.toString(); }
}

class InsertCommand implements Command {
    private TextEditor editor;
    private String text;
    private int position;
    InsertCommand(TextEditor e, String t, int p) { editor=e; text=t; position=p; }
    public void execute() { editor.insert(text, position); }
    public void undo() { editor.delete(position, text.length()); }
}
```

## Q8: When should you use an Adapter versus a Facade?

**A:** An **Adapter** converts the interface of a single class into an interface that clients expect. It works with one adaptee (the existing class) and translates calls between the two interfaces. Use Adapter when you need to integrate a single existing class whose interface does not match what your client code requires.

A **Facade** provides a simplified interface to a subsystem of classes. It does not translate interfaces but rather offers a higher-level, easier-to-use interface that delegates to the appropriate subsystem methods. Use Facade when you want to hide complexity and reduce dependencies on the subsystem internals. Adapter changes the interface; Facade simplifies it. You can combine them — a Facade might internally use Adapters to unify disparate subsystem interfaces behind a clean API.

**Example:**
```java
// Adapter: converts one interface to another
interface MediaPlayer {
    void play(String filename);
}
class VLCAdapter implements MediaPlayer {
    private VLCLib vlc = new VLCLib();
    public void play(String filename) {
        vlc.openMedia(filename); // adapts VLC's API
        vlc.startPlayback();
    }
}

// Facade: simplifies a subsystem
class VideoFacade {
    private Decoder decoder = new Decoder();
    private Renderer renderer = new Renderer();
    private AudioSync audio = new AudioSync();
    void play(String file) { // one simple call
        decoder.decode(file);
        renderer.render(decoder.getFrames());
        audio.sync(decoder.getAudioTrack());
    }
}
```

## Q9: Which pattern defines a family of algorithms and makes them interchangeable?

**A:** The **Strategy** pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from the clients that use it. The context class holds a reference to a strategy object and delegates the algorithmic work to it. The strategy can be changed at runtime by assigning a different strategy object to the context.

Strategy eliminates conditional statements for selecting behavior. Instead of a long `if-else` or `switch` selecting the algorithm, you inject the desired strategy. This follows the Open-Closed Principle — new algorithms can be added by creating new strategy classes without modifying existing code. The trade-off is that clients must be aware of different strategies to choose the right one, and the number of strategy classes can proliferate.

**Example:**
```java
interface RouteStrategy {
    Route findRoute(Location from, Location to);
}

class FastestRoute implements RouteStrategy {
    public Route findRoute(Location from, Location to) {
        return dijkstra(from, to);
    }
}

class ShortestRoute implements RouteStrategy {
    public Route findRoute(Location from, Location to) {
        return astar(from, to);
    }
}

class Navigator {
    private RouteStrategy strategy;
    Navigator(RouteStrategy s) { this.strategy = s; }
    Route navigate(Location from, Location to) {
        return strategy.findRoute(from, to);
    }
}
```

## Q10: When should you use the Observer pattern versus the Mediator pattern?

**A:** Use **Observer** when you have a clear one-to-many broadcast: one subject notifies many independent observers. The observers do not communicate with each other — they only react to the subject's state changes. Observer is lightweight and suitable for event systems, data binding, and notification services.

Use **Mediator** when multiple objects need to communicate with each other and the communication logic would otherwise create a web of pairwise dependencies. The mediator centralizes the communication, so each object talks only to the mediator, not to each other. Mediator is better for complex interactions (e.g., a chat room where users send messages to each other, or a dialog where widgets affect each other). The trade-off: Observer is simple but does not handle inter-observer communication; Mediator handles complex multi-party communication but introduces a central bottleneck.

**Example:**
```java
// Observer: one-to-many broadcast
class StockExchange {
    private List<Investor> investors = new ArrayList<>();
    void priceChanged(String ticker, double price) {
        investors.forEach(i -> i.onPriceChange(ticker, price));
    }
}

// Mediator: multi-party coordination
class ChatRoom implements Mediator {
    private Map<String, User> users = new HashMap<>();
    void sendMessage(String from, String to, String msg) {
        users.get(to).receive(from, msg); // central routing
    }
    void addUser(User u) { users.put(u.getName(), u); }
}
```

## Q11: Which pattern composes objects into tree structures and treats individual and composed objects uniformly?

**A:** The **Composite** pattern lets you compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects (leaves) and compositions of objects (composites) uniformly through a common interface. The client invokes the same operation on both leaves and composites without knowing the specific type.

Composite is essential for hierarchical structures like file systems (files and directories), GUI widgets (simple widgets and containers), and organizational charts. The key design decision is whether the Component interface includes operations common to all elements or only to composites. The "safety" variant puts child-management methods only in Composite, preventing leaf nodes from having irrelevant operations. The "transparency" variant puts all methods in Component, at the cost of leaf nodes potentially throwing exceptions for child operations.

**Example:**
```java
interface FileSystemNode {
    String getName();
    int getSize();
}

class File implements FileSystemNode {
    private String name;
    private int size;
    public int getSize() { return size; }
}

class Directory implements FileSystemNode {
    private String name;
    private List<FileSystemNode> children = new ArrayList<>();
    public int getSize() {
        return children.stream().mapToInt(FileSystemNode::getSize).sum();
    }
    public void add(FileSystemNode node) { children.add(node); }
}
```

## Q12: When should you use the Decorator pattern versus inheritance for extending behavior?

**A:** Use **Decorator** when you need to add responsibilities to individual objects at runtime, when the extensions are combinable (multiple independent concerns), or when subclassing is impractical due to a combinatorial explosion of subclasses. Decorator maintains the same interface as the wrapped object, so the client does not need to know about the decoration.

Use **inheritance** when the behavior variation is intrinsic to the class hierarchy and applies to all instances of a subclass. Inheritance is simpler and more appropriate when the variations are not combinable (e.g., a `Cat` is a `Pet`, not a combination of behaviors). The key difference: inheritance is a compile-time, static relationship (is-a); Decorator is a runtime, dynamic relationship (has-a, wraps-a). The trade-off: Decorator provides flexibility but adds object indirection, making debugging harder.

**Example:**
```java
// Decorator: runtime, combinable extensions
class DataSource {
    void write(String data) { /* ... */ }
}

class EncryptedSource extends DataSource {
    private DataSource wrapped;
    EncryptedSource(DataSource w) { wrapped = w; }
    void write(String data) { wrapped.write(encrypt(data)); }
}

class CompressedSource extends DataSource {
    private DataSource wrapped;
    CompressedSource(DataSource w) { wrapped = w; }
    void write(String data) { wrapped.write(compress(data)); }
}

// Combine: encrypted AND compressed
DataSource ds = new CompressedSource(new EncryptedSource(new PlainSource()));
```

## Q13: Which pattern defers object creation to a subclass?

**A:** The **Factory Method** pattern defers object instantiation to subclasses. The parent class declares a factory method that returns a product type, but the actual instantiation happens in subclasses that override the factory method. This is also described as "parallel class hierarchies" — one hierarchy for the creator classes and another for the product classes.

This is distinct from Abstract Factory (which creates families of products) and Builder (which constructs complex objects step by step). Factory Method is the simplest creation pattern and works well when there is a natural one-to-one correspondence between creator subclasses and product subclasses. The Template Method pattern can also be seen as a specialization where the factory method is one of the variable steps.

**Example:**
```java
abstract class Notification {
    abstract void send(String message);
}

abstract class NotificationFactory {
    abstract Notification createNotification();

    void notify(String msg) {
        Notification n = createNotification(); // deferred to subclass
        n.send(msg);
    }
}

class EmailFactory extends NotificationFactory {
    Notification createNotification() { return new EmailNotification(); }
}

class SMSFactory extends NotificationFactory {
    Notification createNotification() { return new SMSNotification(); }
}
```

## Q14: When should you prefer the Command pattern over simple method calls?

**A:** Use **Command** when you need to decouple the invocation of an operation from its execution, when you need to queue, log, or persist operations, or when you need undo/redo capability. Simple method calls are sufficient when the operation is synchronous, stateless, and does not need to be recorded or reversed.

Command is especially valuable when multiple operations share a common invocation pattern (button clicks, menu items, keyboard shortcuts all triggering different actions). Each command encapsulates the complete action, making the invoker agnostic about what it is triggering. Command also enables composite commands (macros), where a single command triggers a sequence of other commands. The trade-off is the class proliferation — every distinct action needs its own command class.

**Example:**
```java
// Simple method call: no undo, no queue, no log
editor.insertText("hello");

// Command: enables undo, queue, log
interface Command {
    void execute();
    void undo();
}

class InsertCommand implements Command {
    private Editor editor;
    private String text;
    private int position;

    public void execute() { editor.insert(text, position); }
    public void undo() { editor.delete(position, text.length()); }
}

// Enables undo history
Deque<Command> history = new ArrayDeque<>();
history.push(command);
command.execute();
```

## Q15: Which pattern allows an object to change its behavior when its internal state changes?

**A:** The **State** pattern allows an object to alter its behavior when its internal state changes. The object appears to change its class at runtime. Each state is encapsulated in a separate State class, and the context object delegates behavior to its current state object. When the state changes, the context switches to a different state object.

State is the OO replacement for complex conditional logic based on the current state. Instead of a large switch or if-else chain in every method, each state class implements the behavior for that specific state. Transitions between states are explicit operations within the state objects. The trade-off: if there are few states and few behaviors, the overhead of multiple state classes is not justified. State shines when you have multiple states with different behaviors for each method, leading to combinatorial complexity in conditional code.

**Example:**
```java
interface VendingState {
    void insertCoin(VendingMachine machine);
    void selectItem(VendingMachine machine);
    void dispense(VendingMachine machine);
}

class IdleState implements VendingState {
    public void insertCoin(VendingMachine m) {
        m.setState(new HasCoinState());
    }
    public void selectItem(VendingMachine m) { /* reject */ }
    public void dispense(VendingMachine m) { /* reject */ }
}

class HasCoinState implements VendingState {
    public void insertCoin(VendingMachine m) { /* reject */ }
    public void selectItem(VendingMachine m) {
        m.setState(new DispensingState());
    }
    public void dispense(VendingMachine m) { /* reject */ }
}
```

## Q16: When should you use the Composite pattern versus a flat collection?

**A:** Use **Composite** when your objects naturally form a tree hierarchy where both individual items and groups of items need to be treated uniformly, and operations need to propagate through the hierarchy (e.g., summing sizes, rendering, searching). A flat collection works when there is no hierarchical relationship and operations apply to individual items independently.

Composite is essential when operations on a group should apply to all its children recursively — computing the total cost of an order with sub-orders, or rendering a UI panel with nested panels and widgets. The key signal: if you find yourself writing recursive functions to traverse a data structure, Composite would formalize that into an OO pattern. The trade-off: Composite can make it difficult to restrict which components can be children, and the uniform interface sometimes means adding irrelevant methods to leaf types.

**Example:**
```java
// Flat collection: no hierarchy
List<Product> products;
double total = products.stream().mapToDouble(Product::getPrice).sum();

// Composite: supports nested bundles
interface PriceComponent {
    double getPrice();
}

class Product implements PriceComponent {
    private double price;
    public double getPrice() { return price; }
}

class Bundle implements PriceComponent {
    private List<PriceComponent> items = new ArrayList<>();
    private double discount;
    public double getPrice() {
        return items.stream().mapToDouble(PriceComponent::getPrice).sum() * (1 - discount);
    }
    void add(PriceComponent item) { items.add(item); }
}
```

## Q17: Which pattern provides a unified interface to a set of interfaces in a subsystem?

**A:** The **Facade** pattern provides a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use by reducing the number of objects clients interact with and minimizing dependencies on subsystem internals. Facade does not add new functionality — it simplifies access to existing functionality.

Facade is ideal for providing clean APIs over complex subsystems (database access, payment processing, multimedia frameworks). Clients that only need common operations use the Facade; advanced clients can bypass it and access subsystem classes directly. This provides a "principle of least surprise" interface for common use cases while maintaining full access for complex ones. The trade-off: Facade can become a God Object if it tries to wrap too much, and it can hide useful subsystem features.

**Example:**
```java
class VideoConversionFacade {
    private CodecFactory codecFactory = new CodecFactory();
    private AudioMixer audioMixer = new AudioMixer();
    private BitrateReader bitrateReader = new BitrateReader();
    private FileLogger logger = new FileLogger();

    VideoFile convert(String filename, String format) {
        logger.log("Starting conversion of " + filename);
        VideoFile file = new VideoFile(filename);
        Codec codec = codecFactory.getCodec(file.getContainer());
        VideoFile compressed = bitrateReader.read(file, codec);
        return audioMixer.mix(compressed);
    }
}
```

## Q18: When should you choose Builder over a constructor with many parameters?

**A:** Choose **Builder** when an object has many optional parameters (more than 4-5), when you want to make object construction readable and self-documenting, or when you need immutable objects that cannot be modified after construction. A constructor with many parameters is error-prone because it is easy to swap arguments of the same type, and telescoping constructors create combinatorial overload explosion.

Builder provides a fluent API (`builder().name("x").age(25).build()`) that makes the intent of each parameter clear. It also enables step-by-step construction, validation at build time, and the creation of immutable objects. The trade-off is the verbosity of the Builder class itself. For simple objects with few required fields, a constructor or static factory method is simpler. For complex objects with many parameters, the Builder's upfront cost pays for itself in clarity and safety.

**Example:**
```java
// Telescoping constructor: confusing
new HttpRequest(url, null, null, null, 30, true, null);

// Builder: clear and safe
HttpRequest req = HttpRequest.builder()
    .url(url)
    .method("POST")
    .body(jsonBody)
    .timeout(Duration.ofSeconds(30))
    .followRedirects(true)
    .build();

class HttpRequest {
    private final String url;
    private final String method;
    private final String body;
    // ... immutable fields

    static Builder builder() { return new Builder(); }

    static class Builder {
        private String url;
        private String method = "GET";
        // ... settable fields
        Builder url(String u) { this.url = u; return this; }
        Builder method(String m) { this.method = m; return this; }
        HttpRequest build() { return new HttpRequest(this); }
    }
}
```

## Q19: Which pattern provides a way to access elements of a collection sequentially without exposing its underlying representation?

**A:** The **Iterator** pattern provides a way to access the elements of an aggregate object sequentially without exposing its underlying representation. The iterator encapsulates the traversal logic, allowing multiple simultaneous traversals of the same collection and supporting different traversal strategies (forward, reverse, filtered) without changing the collection's interface.

In practice, Iterator is so fundamental that most modern languages provide it natively (Java's `Iterator`, Python's `__iter__`, C++'s STL iterators, Rust's `Iterator` trait). The pattern remains important for custom collections (tree traversals, graph traversals, database cursors) and for adding filtering/mapping to traversals (lazy iterators). The trade-off: iterators hold state about their position, which can cause issues in concurrent contexts, and modifying the underlying collection during iteration is typically unsafe.

**Example:**
```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}

class TreeIterator implements Iterator<TreeNode> {
    private Deque<TreeNode> stack = new ArrayDeque<>();

    TreeIterator(TreeNode root) {
        pushLeft(root);
    }

    private void pushLeft(TreeNode node) {
        while (node != null) {
            stack.push(node);
            node = node.left;
        }
    }

    public boolean hasNext() { return !stack.isEmpty(); }
    public TreeNode next() {
        TreeNode node = stack.pop();
        pushLeft(node.right);
        return node;
    }
}
```

## Q20: When should you use the Proxy pattern versus the Adapter pattern?

**A:** Use **Proxy** when you need to control access to an object — for lazy initialization, access control, logging, caching, or remote access. The Proxy has the same interface as the real object and stands in for it, controlling when and how the real object is accessed. The Proxy and the real object share the same type.

Use **Adapter** when you need to make an existing object's interface compatible with a different interface the client expects. Adapter translates between two incompatible interfaces. The key difference: Proxy controls access to an object of the **same** interface; Adapter makes an object of a **different** interface work where another is expected. You can combine them — a remote proxy that adapts a remote service's API to a local interface.

**Example:**
```java
// Proxy: same interface, controls access
interface Image {
    void display();
}

class RealImage implements Image {
    void display() { /* render image */ }
}

class ProxyImage implements Image {
    private RealImage real;
    public void display() {
        if (real == null) real = new RealImage(); // lazy init
        real.display();
    }
}

// Adapter: different interface, translates
interface LegacyPrinter {
    void printOld(String text);
}

class ModernPrinter {
    void print(String text, int quality) { /* ... */ }
}

class PrinterAdapter implements LegacyPrinter {
    private ModernPrinter modern;
    public void printOld(String text) {
        modern.print(text, 300); // translates interface
    }
}
```

## Q21: Which pattern uses sharing to support large numbers of fine-grained objects efficiently?

**A:** The **Flyweight** pattern uses sharing to support large numbers of fine-grained objects efficiently. Flyweight minimizes memory usage by sharing common state (intrinsic state) across many objects and storing only unique state (extrinsic state) per instance. The intrinsic state is stored in shared flyweight objects; the extrinsic state is passed in by the client.

Flyweight is critical for performance when you have massive numbers of similar objects (characters in a document, particles in a game, nodes in a map). The Flyweight Factory manages the pool of shared objects and ensures that duplicates are not created. The trade-off: introducing indirection and shared mutable state complexity. Flyweight is most effective when intrinsic state dominates and objects are numerous enough that memory savings justify the complexity. If you have only a few objects, the overhead of the factory and shared pool is not worth it.

**Example:**
```java
class TreeType {
    private String name;
    private String color;
    private String texture;
    // intrinsic state: shared across all trees of this type

    TreeType(String name, String color, String texture) {
        this.name = name; this.color = color; this.texture = texture;
    }
    void draw(int x, int y) { /* uses extrinsic x, y */ }
}

class TreeFactory {
    private static Map<String, TreeType> types = new HashMap<>();

    static TreeType getType(String name, String color, String texture) {
        String key = name + color + texture;
        return types.computeIfAbsent(key, k -> new TreeType(name, color, texture));
    }
}
```

## Q22: When should you use Chain of Responsibility versus hard-coded conditional logic?

**A:** Use **Chain of Responsibility** when you have multiple possible handlers for a request and you want to decouple the sender from the receiver, allowing the set of handlers to be configured dynamically. Each handler decides either to handle the request or to pass it to the next handler in the chain. This is superior to hard-coded conditionals when handlers may be added, removed, or reordered at runtime.

Chain of Responsibility is appropriate when the processing pipeline is not known at compile time — middleware chains, approval workflows, event bubbling in UI systems. The trade-off: debugging is harder because the processing path is determined at runtime, not statically visible in the code. For a fixed set of conditions that do not change, simple if-else or switch is clearer and more performant. Use Chain when the flexibility of dynamic handler composition outweighs the loss of static traceability.

**Example:**
```java
abstract class Handler {
    protected Handler next;
    Handler setNext(Handler next) { this.next = next; return next; }
    abstract void handle(Request request);
}

class AuthHandler extends Handler {
    void handle(Request request) {
        if (!request.hasToken()) { throw new AuthException(); }
        if (next != null) next.handle(request);
    }
}

class RateLimitHandler extends Handler {
    void handle(Request request) {
        if (isRateLimited(request)) { throw new RateLimitException(); }
        if (next != null) next.handle(request);
    }
}

// Chain: auth -> rate limit -> actual handler
Handler chain = new AuthHandler();
chain.setNext(new RateLimitHandler()).setNext(new BusinessHandler());
```

## Q23: Which pattern provides a surrogate or placeholder for another object to control access to it?

**A:** The **Proxy** pattern provides a surrogate or placeholder for another object to control access to it. The proxy implements the same interface as the real subject and holds a reference to it. The proxy controls access by adding behavior before, after, or instead of forwarding to the real object.

Proxy has several variants: virtual proxy (lazy initialization of expensive objects), protection proxy (access control), caching proxy (stores results to avoid redundant calls), logging proxy (records calls for debugging), and remote proxy (represents an object in a different address space). In distributed systems, remote proxies (RMI stubs, gRPC clients) are ubiquitous. The trade-off: adding a proxy adds an extra layer of indirection, which can impact performance in latency-sensitive paths.

**Example:**
```java
interface Image {
    void display();
}

class RealImage implements Image {
    RealImage(String file) { loadFromDisk(file); } // expensive
    public void display() { /* render */ }
}

class VirtualProxy implements Image {
    private RealImage real;
    private String file;
    VirtualProxy(String f) { file = f; }
    public void display() {
        if (real == null) real = new RealImage(file); // lazy
        real.display();
    }
}
```

## Q24: When should you choose Flyweight over normal object instantiation?

**A:** Choose **Flyweight** when you need to create a very large number of objects (thousands or millions) that share common intrinsic state, and memory consumption becomes a concern. Normal instantiation creates a separate object for each instance, duplicating shared state in each. Flyweight extracts the shared state into a common pool and only stores unique per-instance data externally.

The decision criteria: (1) the application must be memory-constrained or the object count must be very high, (2) most of the object state can be classified as intrinsic (shared) rather than extrinsic (unique), and (3) the objects do not have unique identity requirements. If you have 100 objects, Flyweight is over-engineering. If you have 10 million particles, each sharing the same texture but differing in position, Flyweight is essential. The trade-off: introducing the Flyweight pattern adds complexity and the indirection of looking up shared objects.

**Example:**
```java
// Normal: each character has its own font data (wasteful)
class Character {
    char value;
    Font font; // duplicated for every character!
}

// Flyweight: shared font data, per-character position
class CharacterFlyweight {
    char value;
    // font data is in the shared Font object, not here
}

class Font {
    String name;
    int size;
    String color;
    // shared: one Font per unique combination
}

// Extrinisic state: position, stored outside the flyweight
class CharacterPosition {
    CharacterFlyweight character;
    int x, y; // unique per instance
}
```

## Q25: Which pattern defines an interface for creating an object but lets subclasses decide which class to instantiate?

**A:** The **Factory Method** pattern defines an interface for creating an object but lets subclasses decide which class to instantiate. The Factory Method lets a class defer instantiation to subclasses. The creator class declares the factory method returning a product type, and each concrete creator overrides it to return a concrete product.

This is one of the most fundamental GoF patterns and the basis for many framework designs. The Spring `ApplicationContext`, Java's `URLStreamHandlerFactory`, and Android's `LayoutInflater` all use variants. The key insight: the creator does not need to know which concrete product it creates — it works with the product interface. Adding a new product type requires only adding a new creator subclass, not modifying existing code (Open-Closed Principle). The trade-off: each new product type requires a new creator class, which can lead to class proliferation.

**Example:**
```java
abstract class Store {
    abstract Product createProduct(String type);

    void orderProduct(String type) {
        Product p = createProduct(type); // subclasses decide
        p.prepare();
        p.deliver();
    }
}

class OnlineStore extends Store {
    Product createProduct(String type) {
        return switch (type) {
            case "book" -> new EBook();
            case "music" -> new DigitalAlbum();
            default -> throw new IllegalArgumentException();
        };
    }
}

class PhysicalStore extends Store {
    Product createProduct(String type) {
        return switch (type) {
            case "book" -> new PaperbackBook();
            case "music" -> new CDDisc();
            default -> throw new IllegalArgumentException();
        };
    }
}
```

## Q26: How would you combine Strategy and Observer to create a dynamic algorithm notification system?

**A:** Combine Strategy and Observer by making the context object both a strategy host and a subject. The context holds a strategy (the algorithm) and maintains a list of observers interested in algorithm changes or results. When the strategy is swapped at runtime, the context notifies all observers of the change, allowing them to react (update UI, log the change, invalidate caches). The strategy itself can also be an observer if it needs to react to external events.

This combination is common in systems where algorithms are swappable and other components must be aware of the current algorithm. For example, a payment processing system that supports multiple payment strategies (credit card, PayPal, crypto) and notifies analytics, logging, and UI modules when the active strategy changes. The key design decision is whether observers are notified by the context (before/after strategy execution) or by the strategy itself.

**Example:**
```java
interface SortStrategy {
    void sort(int[] data);
}

interface SortObserver {
    void onSortStarted(String algorithm);
    void onSortCompleted(String algorithm, long duration);
}

class Sorter {
    private SortStrategy strategy;
    private List<SortObserver> observers = new ArrayList<>();

    void setStrategy(SortStrategy s) {
        this.strategy = s;
        observers.forEach(o -> o.onSortStarted(s.getClass().getSimpleName()));
    }

    void sort(int[] data) {
        long start = System.nanoTime();
        strategy.sort(data);
        long elapsed = System.nanoTime() - start;
        observers.forEach(o -> o.onSortCompleted(
            strategy.getClass().getSimpleName(), elapsed));
    }

    void attach(SortObserver o) { observers.add(o); }
}
```

## Q27: Refactor this procedural state-machine code to use the State pattern

**A:** The procedural approach uses a `state` string field and a large switch statement in every method. Each method has a switch over all possible states, and each case has different behavior. This leads to methods that are O(states × operations) in complexity, with every method touching every state. Adding a new state requires modifying every switch statement, violating the Open-Closed Principle.

Refactoring to the State pattern extracts each state into its own class implementing a common `State` interface. The context (the state machine) delegates all behavior to its current state object. Each state class implements only the behaviors relevant to that state, and transitions are explicit method calls that swap the context's state. This reduces each method to a single delegation call and makes adding new states a matter of adding a new class without touching existing code.

**Example:**
```java
// Before: procedural switch
class TrafficLight {
    String state;
    void next() {
        switch (state) {
            case "RED": state = "GREEN"; break;
            case "GREEN": state = "YELLOW"; break;
            case "YELLOW": state = "RED"; break;
        }
    }
}

// After: State pattern
interface LightState { void next(TrafficLight context); }
class RedState implements LightState {
    public void next(TrafficLight c) { c.setState(new GreenState()); }
}
class GreenState implements LightState {
    public void next(TrafficLight c) { c.setState(new YellowState()); }
}
class YellowState implements LightState {
    public void next(TrafficLight c) { c.setState(new RedState()); }
}

class TrafficLight {
    private LightState state = new RedState();
    void next() { state.next(this); }
    void setState(LightState s) { this.state = s; }
}
```

## Q28: How would you combine Factory Method and Abstract Factory for cross-platform UI creation?

**A:** Use the Abstract Factory to define a family of related UI components (button, textbox, menu) for a platform, and Factory Method within each product to customize creation. The Abstract Factory ensures that all components come from the same platform family (Windows, macOS, Linux), while Factory Method within each component handles variant creation (e.g., a Windows button can be a push button or toggle button via a factory method).

The Abstract Factory is injected into the client (the application code), which calls factory methods on each factory to get concrete components. The client never references concrete platform classes. Adding a new platform means adding a new Abstract Factory implementation. Adding a new variant within a platform means adding a new Factory Method override. This separation of concerns keeps platform-specific code isolated from application logic.

**Example:**
```java
interface GUIFactory {
    Button createButton();
    TextBox createTextBox();
}

class WindowsFactory implements GUIFactory {
    public Button createButton() { return new WindowsButton(); }
    public TextBox createTextBox() { return new WindowsTextBox(); }
}

class MacFactory implements GUIFactory {
    public Button createButton() { return new MacButton(); }
    public TextBox createTextBox() { return new MacTextBox(); }
}

class Application {
    private Button button;
    Application(GUIFactory factory) {
        button = factory.createButton(); // Factory Method inside Abstract Factory
    }
}
```

## Q29: Refactor this large switch-case block into the Command pattern

**A:** A large switch-case that maps string commands to actions (like a menu system or API router) can be refactored by encapsulating each action in a Command object. A `Map<String, Command>` replaces the switch, providing O(1) dispatch without conditional chains. Each command encapsulates its action, can be tested independently, and can support undo/redo if needed.

The refactoring process: (1) extract each case body into a separate Command class, (2) create a registry (map) that maps command names to Command instances, (3) replace the switch with a registry lookup, (4) add error handling for unknown commands. The resulting code is extensible — new commands are added by registering new Command objects, not by modifying existing code.

**Example:**
```java
// Before: switch block
void execute(String command) {
    switch (command) {
        case "save": saveDocument(); break;
        case "open": openDocument(); break;
        case "delete": deleteDocument(); break;
        // 20 more cases...
    }
}

// After: Command pattern
interface Command {
    void execute();
}

Map<String, Command> commands = Map.of(
    "save", this::saveDocument,
    "open", this::openDocument,
    "delete", this::deleteDocument
);

void execute(String command) {
    Command cmd = commands.getOrDefault(command, () ->
        throw new IllegalArgumentException("Unknown: " + command));
    cmd.execute();
}
```

## Q30: How would you combine Decorator and Proxy to add logging with access control?

**A:** Use Proxy to control access (authentication, authorization) and Decorator to add cross-cutting concerns (logging, metrics) around the real object. The Proxy sits at the outermost layer, checking permissions before allowing any call through. The Decorator layers sit between the Proxy and the real object, each adding one concern. The order matters: access control (Proxy) should come before logging (Decorator) so unauthorized access is rejected before any logging overhead.

In practice, the Proxy checks credentials and rejects unauthorized calls immediately. If authorized, the call passes through a logging Decorator (which records the method name, parameters, and timing), then through to the real object. The real object performs the actual business logic. This separation keeps each concern in its own class and allows them to be composed in any order. The Proxy is distinguished from the Decorator by its intent: Proxy controls access; Decorator adds behavior.

**Example:**
```java
// Proxy: access control
class AccessControlProxy implements Service {
    private Service real;
    private User currentUser;

    public Data fetchData(String id) {
        if (!currentUser.hasPermission("read"))
            throw new SecurityException("Unauthorized");
        return real.fetchData(id); // delegates to decorator chain
    }
}

// Decorator: logging
class LoggingDecorator implements Service {
    private Service wrapped;
    public Data fetchData(String id) {
        long start = System.nanoTime();
        Data result = wrapped.fetchData(id);
        log("fetchData(" + id + ") took " + (System.nanoTime() - start) + "ns");
        return result;
    }
}

// Composition
Service service = new AccessControlProxy(
    new LoggingDecorator(
        new RealService()));
```

## Q31: Refactor this repeated algorithm structure into the Template Method pattern

**A:** When multiple classes implement the same algorithm skeleton with minor variations in individual steps, Template Method extracts the skeleton into a base class. The base class defines the algorithm as a `final` method that calls abstract or overridable hook methods for the varying steps. Subclasses override only the steps that differ, eliminating code duplication of the algorithm's structure.

The refactoring identifies the common steps across all implementations, places them in the base class template method, and extracts the varying parts into protected methods that subclasses override. Hook methods (with default no-op implementations) are used for optional steps. The template method is marked `final` to prevent subclasses from altering the algorithm's structure. This reduces duplication while keeping each subclass focused on its unique behavior.

**Example:**
```java
// Before: duplicated structure
class PDFExporter {
    void export() {
        openDocument();       // same
        writeHeader();        // different
        writeContent();       // different
        writeFooter();        // same
        closeDocument();      // same
    }
}

// After: Template Method
abstract class Exporter {
    final void export() {
        openDocument();
        writeHeader();
        writeContent();
        writeFooter();
        closeDocument();
    }
    void openDocument() { /* common */ }
    abstract void writeHeader();
    abstract void writeContent();
    void writeFooter() { /* common */ }
    void closeDocument() { /* common */ }
}

class PDFExporter extends Exporter {
    void writeHeader() { /* PDF-specific */ }
    void writeContent() { /* PDF-specific */ }
}
```

## Q32: How would you combine Chain of Responsibility with Composite for a processing tree?

**A:** Chain of Responsibility processes requests through a linear chain of handlers, while Composite forms a tree. Combining them creates a processing tree where each node is a composite that can have child processors. A request propagates through the tree: each node processes it (or not) and passes it to its children. This is more powerful than a linear chain because processing can branch and fan out.

This combination is useful for hierarchical processing systems: file system filters (directories contain sub-directories and files, each with their own filter rules), approval workflows (a request goes to a manager, who may escalate to a VP), or event propagation in UI trees. The Composite manages the parent-child relationships, and each Composite node decides whether to process the request, pass it to children, or stop propagation. The key design decision is whether a node's processing is independent of its children or depends on children's results.

**Example:**
```java
interface Processor {
    boolean process(Request req);
}

class CompositeProcessor implements Processor {
    private List<Processor> children = new ArrayList<>();
    private String name;

    public boolean process(Request req) {
        if (!matches(req)) return false; // this node's filter
        for (Processor child : children) {
            if (!child.process(req)) return false; // child rejected
        }
        return true; // all children accepted
    }

    void add(Processor p) { children.add(p); }
    boolean matches(Request req) { /* this node's criteria */ }
}
```

## Q33: Refactor this conditional object creation into Strategy combined with Factory

**A:** A series of `if-else` or `switch` statements that select both the algorithm and the object to execute it can be refactored by separating concerns: a Factory selects the right Strategy based on input, and the Strategy encapsulates the algorithm. The Factory handles object creation logic (which depends on configuration, environment, or runtime data), while the Strategy handles the behavior.

This combination eliminates conditional logic from the client code. The client requests a strategy from the factory, receives the appropriate implementation, and calls it without knowing which specific algorithm is running. The factory can use configuration files, environment variables, or runtime data to determine which strategy to instantiate. This separation makes both the factory and the strategies independently testable and extensible.

**Example:**
```java
interface PricingStrategy {
    double calculatePrice(double basePrice, Customer customer);
}

class PricingFactory {
    static PricingStrategy create(String customerType) {
        return switch (customerType) {
            case "premium" -> new PremiumPricing();
            case "bulk" -> new BulkPricing();
            case "regular" -> new RegularPricing();
            default -> throw new IllegalArgumentException();
        };
    }
}

class PricingEngine {
    double price(double base, Customer c) {
        PricingStrategy strategy = PricingFactory.create(c.getType());
        return strategy.calculatePrice(base, c); // no conditionals
    }
}
```

## Q34: How would you combine Builder and Prototype for cloning complex configured objects?

**A:** The Builder pattern constructs objects step-by-step, and Prototype creates objects by cloning an existing instance. Combining them allows you to start from a pre-configured prototype (a "template" object) and customize it via the builder. The builder's `build()` method clones the prototype and applies the builder's overrides, producing a new object that inherits most configuration from the prototype but with specific customizations.

This is useful when you have default configurations that most objects share but need occasional customization. The prototype holds the default configuration; the builder provides the customization API. When building, the builder clones the prototype and applies the client's specified changes. This reduces boilerplate for the common case (just use the prototype) while supporting the uncommon case (clone + modify).

**Example:**
```java
class ServerConfig implements Cloneable {
    int port; String host; boolean ssl; int timeout;
    public ServerConfig clone() { /* field-by-field copy */ }
}

class ServerConfigBuilder {
    private ServerConfig prototype;
    private Integer overridePort;
    private Boolean overrideSsl;

    ServerConfigBuilder(ServerConfig prototype) { this.prototype = prototype; }
    ServerConfigBuilder port(int p) { overridePort = p; return this; }
    ServerConfigBuilder ssl(boolean s) { overrideSsl = s; return this; }

    ServerConfig build() {
        ServerConfig config = prototype.clone(); // prototype base
        if (overridePort != null) config.port = overridePort;
        if (overrideSsl != null) config.ssl = overrideSsl;
        return config;
    }
}
```

## Q35: Refactor this God Class into a Facade with focused subsystems

**A:** A God Class handles too many responsibilities — database access, business logic, email sending, logging, and caching all in one class. Refactoring extracts each responsibility into a focused subsystem class and creates a Facade that provides a simplified interface to the subsystems. The Facade coordinates between subsystems, and clients interact only with the Facade for common operations.

The process: (1) identify distinct responsibilities, (2) extract each into its own class, (3) define the subsystem interfaces, (4) create the Facade that delegates to subsystems, (5) move client code to use the Facade. The resulting architecture follows the Single Responsibility Principle: each subsystem handles one concern. The Facade provides a clean API that hides the complexity of coordinating multiple subsystems.

**Example:**
```java
// God class
class UserManager {
    void createUser(String name, String email) {
        // database logic
        // validation logic
        // email notification
        // logging
        // caching
    }
}

// Refactored: Facade + subsystems
class UserManagerFacade {
    private UserRepository db = new UserRepository();
    private EmailService email = new EmailService();
    private AuditLogger logger = new AuditLogger();
    private CacheManager cache = new CacheManager();

    void createUser(String name, String email) {
        User user = new User(name, email);
        db.save(user);
        email.sendWelcome(user);
        logger.log("Created user: " + name);
        cache.invalidate("users");
    }
}
```

## Q36: How would you combine Mediator and Observer for a chat application?

**A:** The Mediator centralizes communication between chat users, and Observer notifies users of incoming messages. The ChatRoom (Mediator) receives messages from users and routes them to the appropriate recipients. Users (Observers) register with the ChatRoom and are notified when messages arrive. The Mediator handles routing logic; Observer handles notification delivery.

This combination is natural for multi-party communication systems. The Mediator prevents users from having direct references to each other (reducing coupling), and Observer ensures that users receive messages asynchronously. The ChatRoom can implement additional logic: message filtering, history management, user presence tracking. Users implement the Observer interface to receive notifications. The Mediator pattern also prevents the "n-squared" dependency problem where each user would need a reference to every other user.

**Example:**
```java
class ChatRoom {
    private Map<String, User> users = new HashMap<>();

    void sendMessage(String from, String to, String message) {
        User recipient = users.get(to);
        if (recipient != null) {
            recipient.receive(from, message); // mediator routes
        }
    }

    void addUser(User user) { users.put(user.getName(), user); }
}

class User {
    private String name;
    private List<MessageListener> listeners = new ArrayList<>();

    void send(String to, String msg, ChatRoom room) {
        room.sendMessage(name, to, msg);
    }

    void receive(String from, String msg) {
        listeners.forEach(l -> l.onMessage(from, msg)); // observer notify
    }
}
```

## Q37: Refactor this code that adds behavior at runtime using the Decorator pattern

**A:** Code that uses boolean flags to toggle behavior (`if (logEnabled)`, `if (compressed)`) can be refactored by extracting each behavior toggle into a Decorator. Each decorator wraps the base component and adds one behavior, controlled by whether the decorator is applied. The client composes decorators at runtime based on configuration, eliminating all conditional behavior flags.

The refactoring: (1) identify each toggleable behavior, (2) create a Decorator class for each, (3) remove the conditional logic from the base class, (4) compose decorators based on configuration. The base class becomes clean and focused on core behavior. Decorators are stacked based on runtime configuration: `new CachingDecorator(new LoggingDecorator(new DataService()))`. Configuration-driven decorator composition replaces boolean flags.

**Example:**
```java
// Before: boolean flags
class DataService {
    boolean logEnabled, cacheEnabled;
    Data fetch(String id) {
        if (logEnabled) log("Fetching " + id);
        Data result = cacheEnabled ? cache.get(id) : db.get(id);
        if (cacheEnabled) cache.put(id, result);
        if (logEnabled) log("Fetched " + id);
        return result;
    }
}

// After: Decorators
class DataService { Data fetch(String id) { return db.get(id); } }

class LoggingDecorator extends DataService {
    DataService wrapped;
    Data fetch(String id) {
        log("Fetching " + id);
        Data r = wrapped.fetch(id);
        log("Fetched " + id);
        return r;
    }
}

// Runtime composition based on config
DataService svc = new DataService();
if (config.logging) svc = new LoggingDecorator(svc);
if (config.caching) svc = new CachingDecorator(svc);
```

## Q38: How would you combine Strategy and Factory for runtime-selectable encryption algorithms?

**A:** The Strategy pattern makes encryption algorithms interchangeable, and the Factory selects the algorithm based on configuration (algorithm name, security level, performance requirements). The client requests an encryption strategy from the factory, receives the appropriate implementation, and uses it without knowing the specific algorithm. The factory handles creation complexity (key generation, parameter validation), and the strategy handles the encryption/decryption behavior.

This combination is ideal for cryptographic systems where algorithms need to be swapped based on compliance requirements, performance needs, or deprecation. The factory can load algorithm implementations dynamically (using reflection or service loaders), making it possible to add new algorithms without modifying existing code. The strategy interface (`encrypt`, `decrypt`) provides a uniform API regardless of the underlying algorithm.

**Example:**
```java
interface EncryptionStrategy {
    byte[] encrypt(byte[] data, SecretKey key);
    byte[] decrypt(byte[] data, SecretKey key);
}

class EncryptionFactory {
    static EncryptionStrategy create(String algorithm) {
        return switch (algorithm) {
            case "AES" -> new AESStrategy();
            case "RSA" -> new RSAStrategy();
            case "ChaCha20" -> new ChaCha20Strategy();
            default -> throw new IllegalArgumentException(algorithm);
        };
    }
}

class SecureChannel {
    private EncryptionStrategy crypto;
    SecureChannel(String algorithm) {
        this.crypto = EncryptionFactory.create(algorithm);
    }
    byte[] send(byte[] data, SecretKey key) { return crypto.encrypt(data, key); }
}
```

## Q39: Refactor this nested conditional logic into a Chain of Responsibility

**A:** Deeply nested if-else logic that checks multiple conditions (authentication, authorization, rate limiting, validation) can be refactored into a Chain of Responsibility. Each condition becomes a handler in the chain. If a handler's check fails, it short-circuits by not passing the request forward. If it passes, it delegates to the next handler. The chain is constructed from a list of handlers, making it configurable and testable.

The refactoring eliminates nested conditionals by flattening them into a linear chain. Each handler is independently testable, and handlers can be reordered, added, or removed without modifying other handlers. The key benefit is that each handler encapsulates one check and one failure response, following the Single Responsibility Principle. The chain can be configured dynamically at runtime.

**Example:**
```java
// Before: nested conditionals
void handle(Request req) {
    if (authenticate(req)) {
        if (authorize(req)) {
            if (rateLimit(req)) {
                if (validate(req)) {
                    process(req);
                } else { sendError(400); }
            } else { sendError(429); }
        } else { sendError(403); }
    } else { sendError(401); }
}

// After: Chain of Responsibility
Handler chain = new AuthHandler(
    new RateLimitHandler(
        new ValidationHandler(
            new ProcessingHandler())));

void handle(Request req) { chain.handle(req); }
```

## Q40: How would you combine Adapter and Decorator to integrate and enhance a legacy API?

**A:** The Adapter makes the legacy API's interface compatible with the modern API the client expects. The Decorator adds new behavior (retry logic, circuit breaking, caching) on top of the adapted interface. The order is: client → Decorator(s) → Adapter → Legacy API. The Adapter handles interface translation; Decorators handle cross-cutting concerns.

This is essential in system modernization where you need to integrate a legacy service that has an incompatible interface AND requires enhanced behavior (resilience, observability). The Adapter handles the technical incompatibility (different method names, parameter formats, return types), while Decorators add production concerns (retry on failure, cache responses, log calls). Each layer has a single responsibility, and new Decorators can be added without touching the Adapter or the legacy code.

**Example:**
```java
// Legacy API with incompatible interface
class LegacyPaymentSystem {
    String processPayment(String xmlRequest) { /* ... */ }
}

// Adapter: modern interface
interface PaymentGateway {
    PaymentResult pay(PaymentRequest request);
}

class LegacyPaymentAdapter implements PaymentGateway {
    private LegacyPaymentSystem legacy;
    public PaymentResult pay(PaymentRequest req) {
        String xml = toXml(req);
        String response = legacy.processPayment(xml);
        return fromXml(response);
    }
}

// Decorator: adds retry
class RetryDecorator implements PaymentGateway {
    PaymentGateway wrapped;
    public PaymentResult pay(PaymentRequest req) {
        for (int i = 0; i < 3; i++) {
            try { return wrapped.pay(req); }
            catch (Exception e) { if (i == 2) throw e; }
        }
        return null;
    }
}

// Composition
PaymentGateway gw = new RetryDecorator(new LegacyPaymentAdapter(new LegacyPaymentSystem()));
```

## Q41: Refactor this tree traversal code into Composite with Visitor

**A:** Tree traversal code that has type-specific processing in traversal methods can be refactored by separating the tree structure (Composite) from the operations on nodes (Visitor). The Composite defines the tree with uniform `accept` methods; the Visitor defines type-specific operations. Each node type implements `accept(Visitor v)` by calling the appropriate `visit` method on the visitor.

This separation allows adding new operations (print, export, analyze) without modifying the node classes. It also keeps the tree structure clean without operation-specific logic. The trade-off: adding new node types requires updating the Visitor interface, so this is best when the node types are stable but operations change frequently. The traversal logic lives in the Composite (or a separate traverser), and the processing logic lives in the Visitor.

**Example:**
```java
interface FileNode { void accept(FileVisitor v); }

class File implements FileNode {
    String name; long size;
    public void accept(FileVisitor v) { v.visitFile(this); }
}

class Directory implements FileNode {
    String name; List<FileNode> children = new ArrayList<>();
    public void accept(FileVisitor v) {
        v.visitDirectory(this);
        for (FileNode child : children) child.accept(v);
    }
}

interface FileVisitor {
    void visitFile(File f);
    void visitDirectory(Directory d);
}

class SizeCalculator implements FileVisitor {
    long total = 0;
    void visitFile(File f) { total += f.size; }
    void visitDirectory(Directory d) { /* sum children */ }
}
```

## Q42: How would you combine Singleton and Factory for managed connection pooling?

**A:** Singleton ensures one instance of the ConnectionPool exists globally, and Factory creates the pool's connections on demand. The Singleton manages the pool's lifecycle (creation, shutdown), while the Factory encapsulates connection creation logic (URL parsing, authentication, driver selection). Clients get the pool via `ConnectionPool.getInstance()` and request connections, which the pool creates using the internal factory.

This combination is standard for resource management: the pool is a singleton because multiple pools would waste resources, and the factory separates connection creation details from pool management logic. The factory can be swapped (e.g., different database drivers) without changing the pool's singleton management. The pool handles connection lifecycle (creation, validation, eviction, closure), and the factory handles the specifics of creating one connection.

**Example:**
```java
class ConnectionPool {
    private static final ConnectionPool INSTANCE = new ConnectionPool();
    private BlockingQueue<Connection> pool;
    private ConnectionFactory factory;

    private ConnectionPool() {
        factory = new ConnectionFactory("jdbc:mysql://...");
        pool = new LinkedBlockingQueue<>(20);
        for (int i = 0; i < 20; i++) pool.add(factory.create());
    }

    static ConnectionPool getInstance() { return INSTANCE; }
    Connection acquire() throws InterruptedException { return pool.take(); }
    void release(Connection c) { pool.offer(c); }
}

class ConnectionFactory {
    private String url;
    Connection create() { return DriverManager.getConnection(url); }
}
```

## Q43: Refactor this class that changes behavior based on mode into State with Strategy

**A:** A class with a `mode` field (e.g., "normal", "debug", "test") and large switch statements in every method can be refactored using State for the mode-dependent behavior and Strategy for the swappable algorithms within each mode. The State pattern handles which behavior set is active; Strategy handles individual algorithm variations within each mode.

The refactoring extracts each mode into a State class. Each State class may use Strategy objects for its swappable algorithms. The context delegates to its current state, and the state uses strategies for algorithm selection. This eliminates the mode switches and makes both the mode transitions and the algorithm selection explicit and configurable.

**Example:**
```java
interface PrinterMode {
    void print(Printer context, String data);
}

class NormalMode implements PrinterMode {
    private FormatStrategy format = new PlainFormat();
    public void print(Printer ctx, String data) {
        ctx.output(format.apply(data));
    }
}

class DebugMode implements PrinterMode {
    private FormatStrategy format = new VerboseFormat();
    public void print(Printer ctx, String data) {
        ctx.output("[" + ctx.timestamp() + "] " + format.apply(data));
    }
}

class Printer {
    private PrinterMode mode = new NormalMode();
    void setMode(PrinterMode m) { this.mode = m; }
    void print(String data) { mode.print(this, data); }
}
```

## Q44: How would you combine Command and Memento for undoable operations?

**A:** The Command pattern encapsulates operations as objects, and Memento captures and restores object state. Combining them: each Command stores a Memento of the state before execution. When `execute()` is called, the command saves a memento of the receiver's state, then performs the operation. When `undo()` is called, the command restores the receiver from the saved memento. This provides reliable undo/redo.

The Command maintains a history stack of executed commands (with their mementos). Undo pops the last command and restores its memento. Redo re-executes the command (which may create a new memento for future undo). This combination is standard in text editors (undo/typing), graphics applications (undo/drawing), and transaction systems. The Memento ensures complete state restoration; the Command provides the operation interface and history management.

**Example:**
```java
interface Command {
    void execute();
    void undo();
}

class TextEditCommand implements Command {
    private TextDocument doc;
    private Memento backup;
    private String newText;
    private int position;

    public void execute() {
        backup = doc.createMemento(); // save state
        doc.insert(newText, position);
    }

    public void undo() {
        doc.restore(backup); // restore saved state
    }
}

class CommandHistory {
    private Deque<Command> undoStack = new ArrayDeque<>();
    private Deque<Command> redoStack = new ArrayDeque<>();

    void execute(Command cmd) {
        cmd.execute();
        undoStack.push(cmd);
        redoStack.clear();
    }

    void undo() {
        if (!undoStack.isEmpty()) {
            Command cmd = undoStack.pop();
            cmd.undo();
            redoStack.push(cmd);
        }
    }
}
```

## Q45: Refactor this object creation code into Abstract Factory with Builder

**A:** Object creation code that constructs complex objects with many steps and variations benefits from combining Abstract Factory (for creating families of related objects) with Builder (for step-by-step construction of each object). The Abstract Factory provides factory methods for each product type, and each factory method internally uses a Builder to construct the complex product.

This combination handles two dimensions of complexity: (1) creating different product families (Windows vs. Mac widgets), and (2) constructing each product with many configurable parameters. The Abstract Factory determines which family; the Builder within each factory method handles the product's complex construction. This keeps factories focused on family selection and builders focused on product configuration.

**Example:**
```java
interface UIFactory {
    Button createButton(ButtonConfig config);
    TextBox createTextBox(TextBoxConfig config);
}

class WindowsUIFactory implements UIFactory {
    public Button createButton(ButtonConfig config) {
        return new WindowsButtonBuilder()
            .size(config.getWidth(), config.getHeight())
            .color(config.getColor())
            .font(config.getFont())
            .build();
    }
}

class ButtonConfig {
    private int width, height;
    private Color color;
    private Font font;
    // builder pattern for config
}
```

## Q46: How would you combine Flyweight and Factory for memory-efficient document rendering?

**A:** The Flyweight pattern shares common character formatting objects (font, size, style) across thousands of characters in a document, and the Factory manages the flyweight pool. Each character in the document stores only its intrinsic state (the character glyph) and references to shared flyweight objects for formatting. The extrinsic state (position on page, line number) is stored per-character but not shared.

The Factory ensures that identical formatting objects are shared: when the document engine needs a "bold, 12pt, Times New Roman" object, the factory returns the existing shared instance rather than creating a new one. For a 100,000-character document, you might need only 5-10 unique formatting objects instead of 100,000. The memory savings are enormous, and the rendering code accesses formatting through the same interface regardless of whether it is shared or unique.

**Example:**
```java
class CharacterFormat {
    String font;
    int size;
    boolean bold, italic;
    // intrinsic state: shared across all characters with same formatting
}

class FormatFactory {
    private Map<String, CharacterFormat> cache = new HashMap<>();

    CharacterFormat get(String font, int size, boolean bold, boolean italic) {
        String key = font + size + bold + italic;
        return cache.computeIfAbsent(key,
            k -> new CharacterFormat(font, size, bold, italic));
    }
}

class DocumentCharacter {
    char glyph;
    CharacterFormat format; // shared flyweight
    int x, y; // extrinsic: per-character position
}
```

## Q47: Refactor this access-control code into Proxy combined with Decorator

**A:** Access control code that checks permissions inline before every operation can be refactored into a Protection Proxy that wraps the real object and checks permissions before forwarding. Decorators add additional concerns (caching, logging) between the proxy and the real object. The proxy is the outermost wrapper (security first), followed by decorators for other cross-cutting concerns.

The refactoring separates the access control logic from the business logic. The Protection Proxy implements the same interface, checks the user's permissions for each method call, and either delegates to the real object or throws an access denied exception. Decorators for caching or logging sit inside the proxy (after authorization), so unauthorized requests are rejected before any processing overhead.

**Example:**
```java
class ProtectedDocument implements Document {
    private Document real;
    private User user;

    public String getContent(String docId) {
        if (!user.canRead(docId))
            throw new AccessDeniedException();
        return real.getContent(docId);
    }

    public void save(String docId, String content) {
        if (!user.canWrite(docId))
            throw new AccessDeniedException();
        real.save(docId, content);
    }
}

// Usage: proxy + cache decorator
Document doc = new ProtectedDocument(user,
    new CachingDecorator(
        new FileDocument()));
```

## Q48: How would you combine Iterator and Composite for uniform tree traversal?

**A:** The Composite pattern creates a tree of uniform nodes, and Iterator provides a way to traverse it without exposing the tree structure. By implementing an Iterator on the Composite, clients can iterate over all nodes (flattened) without knowing whether they are leaf or composite nodes. The iterator handles the tree traversal algorithm (depth-first, breadth-first) internally.

This combination is standard for tree structures: file system directory traversal, UI widget tree traversal, or organizational hierarchy enumeration. The Composite defines the tree; the Iterator flattens it into a linear sequence for the client. The client uses a simple `hasNext()`/`next()` loop without recursion or knowledge of the tree depth. Different iterator implementations can provide different traversal orders.

**Example:**
```java
interface TreeNode {
    Iterator<TreeNode> depthFirstIterator();
    Iterator<TreeNode> breadthFirstIterator();
}

class CompositeNode implements TreeNode {
    private List<TreeNode> children = new ArrayList<>();

    public Iterator<TreeNode> depthFirstIterator() {
        return new Iterator<>() {
            Deque<Iterator<TreeNode>> stack = new ArrayDeque<>();
            { stack.push(children.iterator()); }

            public boolean hasNext() {
                return !stack.isEmpty() && stack.peek().hasNext();
            }
            public TreeNode next() {
                TreeNode node = stack.peek().next();
                if (node instanceof CompositeNode cn) {
                    stack.push(cn.children.iterator());
                }
                return node;
            }
        };
    }
}
```

## Q49: Refactor this tightly-coupled multi-object coordination into the Mediator pattern

**A:** When multiple objects communicate directly with each other (each holding references to all others), the dependencies form an n-squared mesh. Refactoring into Mediator replaces direct object-to-object communication with centralized communication through a Mediator. Each object holds a reference only to the Mediator, reducing n-squared dependencies to n.

The Mediator encapsulates the interaction logic between objects. When one object changes state, it notifies the Mediator, which determines which other objects need to be updated and forwards the information. This centralizes the coordination logic, making it easier to understand, modify, and test. The trade-off: the Mediator can become a God Object if it accumulates too much logic. Keep it focused on coordination, not business rules.

**Example:**
```java
// Before: tightly coupled
class DialogBox {
    ListBox list;
    TextBox text;
    ButtonOK ok;
    // list changes -> text updates -> ok state changes
    // every object knows about every other
}

// After: Mediator
class DialogMediator {
    private ListBox list;
    private TextBox text;
    private ButtonOK ok;

    void listChanged() {
        text.setText(list.getSelected());
        ok.setEnabled(list.getSelected() != null);
    }
}

class ListBox {
    private DialogMediator mediator;
    void selectionChanged() { mediator.listChanged(); }
}
```

## Q50: How would you combine Template Method with Strategy for configurable algorithm templates?

**A:** Template Method defines the algorithm skeleton with overridable steps; Strategy makes individual steps swappable as objects. Combining them: the Template Method provides the fixed algorithm structure, and some of its variable steps are delegated to Strategy objects that are injected at runtime. This gives you both the structural enforcement of Template Method and the runtime flexibility of Strategy.

Use this when you have an algorithm with a fixed sequence of steps but some steps have multiple possible implementations that should be selectable at runtime. The template method ensures the order and structure; the strategies provide the step implementations. Strategies can be swapped between runs without subclassing, while the template method prevents clients from accidentally altering the algorithm's structure.

**Example:**
```java
abstract class DataPipeline {
    private TransformStrategy transformer;
    private ValidateStrategy validator;

    final void run(byte[] data) {
        byte[] validated = validator.validate(data);
        byte[] transformed = transformer.transform(validated);
        store(transformed);
    }

    abstract void store(byte[] data);
}

class ImportPipeline extends DataPipeline {
    void store(byte[] data) { /* import-specific storage */ }
}

// Runtime configuration
ImportPipeline pipeline = new ImportPipeline();
pipeline.setTransformer(new JsonToCsvTransform());
pipeline.setValidator(new SchemaValidator());
pipeline.run(rawData);
```

## Q51: How does Spring use the Proxy pattern internally for AOP and what are the trade-offs?

**A:** Spring AOP creates proxy objects around beans to intercept method calls and apply cross-cutting concerns (transaction management, security, caching). By default, Spring uses JDK dynamic proxies (interface-based) for beans implementing interfaces, and CGLIB proxies (subclass-based) for beans without interfaces. The proxy intercepts every method call, applies advice (before, after, around), and then delegates to the real bean.

The trade-offs are significant: (1) **Performance** — every method call goes through the proxy, adding indirection overhead (though minimal in practice). (2) **Self-invocation problem** — methods called within the same object bypass the proxy, so `@Transactional` on an internal method call does not work. (3) **Complexity** — proxy-based AOP is harder to debug because the call stack includes proxy infrastructure. (4) **Final classes/methods** cannot be proxied by CGLIB. Spring Boot 3.x with proxy-mode defaults reflects the community's preference for the simpler proxy model over the more complex AspectJ compile-time weaving.

**Example:**
```java
// Spring creates a proxy behind the scenes
@Service
public class OrderService {
    @Transactional
    public void placeOrder(Order order) {
        // Spring proxy intercepts this call
        // BEGIN TRANSACTION
        repository.save(order);
        // COMMIT TRANSACTION (or ROLLBACK on exception)
    }
}

// Configuration
@EnableAspectJAutoProxy(proxyTargetClass = true) // force CGLIB
```

## Q52: Which patterns does Django's ORM implement and how do they compose?

**A:** Django's ORM implements the Active Record pattern — each model class represents a database row and combines data access with business logic. The model class inherits from `django.db.models.Model` and provides methods for CRUD operations (`save()`, `delete()`, `objects.get()`, `objects.filter()`). This is simpler than the Data Mapper pattern (used by Hibernate) where persistence logic is separate from domain objects.

Django's ORM also uses the **Repository** pattern through the manager (`objects`) which provides query building. The **QuerySet** uses a lazy evaluation pattern (Builder-like) where queries are constructed but not executed until evaluated. The **Unit of Work** pattern is partially implemented through `transaction.atomic()` context managers. The **Identity Map** is implemented via Django's cache layer. The composition: Active Record (model) + Repository (manager) + Builder (QuerySet) creates a productive but opinionated data access layer where domain objects know about persistence, which is convenient but couples business logic to the database.

**Example:**
```python
# Active Record: model knows how to save itself
class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    # Repository: objects manager
    # Builder: chained querysets
    articles = (Article.objects
        .filter(published=True)
        .order_by('-created_at')
        .select_related('author'))  # lazy evaluation until iteration
    for article in articles:  # query executes here
        print(article.title)
```

## Q53: How does the STL implement the Strategy pattern through function objects and lambdas?

**A:** The C++ STL implements the Strategy pattern pervasively through function objects (functors) and, in modern C++, lambdas. Algorithms like `std::sort`, `std::for_each`, and `std::transform` accept strategy parameters that customize their behavior. The comparator in `std::sort` is a strategy for ordering; the unary/binary functions in algorithms are strategies for transformation and accumulation.

This is more flexible than template-based static polymorphism because lambdas create unique anonymous types that the compiler can inline, achieving zero-cost abstraction. The STL achieves the Strategy pattern without virtual dispatch through templates — the strategy type is a template parameter, resolved at compile time. This provides the flexibility of Strategy without the runtime overhead of virtual functions. Each lambda or function object is a strategy that can be swapped by passing a different callable to the algorithm.

**Example:**
```cpp
#include <algorithm>
#include <vector>

// Strategy as lambda
std::vector<int> nums = {3, 1, 4, 1, 5};

// Strategy: custom comparator
std::sort(nums.begin(), nums.end(), [](int a, int b) {
    return a > b; // descending strategy
});

// Strategy: transform
std::vector<std::string> strs;
std::transform(nums.begin(), nums.end(), std::back_inserter(strs),
    [](int n) { return std::to_string(n); }); // formatting strategy

// Strategy as named function object
struct IsEven {
    bool operator()(int n) const { return n % 2 == 0; }
};
auto it = std::find_if(nums.begin(), nums.end(), IsEven{}); // filter strategy
```

## Q54: Which combined patterns form the backbone of Spring's BeanFactory and ApplicationContext?

**A:** Spring's IoC container combines Factory, Singleton, and Composite patterns. The `BeanFactory` is a Factory that creates and manages bean instances. The `ApplicationContext` extends `BeanFactory` and adds Observer (event publishing), Strategy (environment abstraction), and Proxy (AOP). Beans are managed as Singletons by default (one instance per container), though other scopes exist.

The `BeanDefinition` objects form a Composite-like hierarchy where parent bean definitions can inherit from child definitions. The `BeanPostProcessor` chain uses Chain of Responsibility to process beans after creation. The `FactoryBean` pattern provides factories within the factory for complex object creation. The overall architecture: the container (Factory + Singleton) creates beans, processes them through processor chains (Chain of Responsibility), publishes lifecycle events (Observer), and wraps them with proxies (Proxy) — all coordinated through a unified configuration abstraction (Composite/configuration hierarchy).

**Example:**
```java
// Spring container: Factory + Singleton
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
// Each call returns the SAME singleton instance
MyService s1 = ctx.getBean(MyService.class);
MyService s2 = ctx.getBean(MyService.class);
assert s1 == s2; // singleton pattern

// PostProcessors: Chain of Responsibility
@Component
class MyPostProcessor implements BeanPostProcessor {
    public Object postProcessAfterInitialization(Object bean, String name) {
        // intercepts every bean creation
        return wrapWithProxy(bean);
    }
}
```

## Q55: How does Django's middleware system implement the Chain of Responsibility pattern?

**A:** Django middleware is a chain of classes that process requests before they reach the view and responses before they return to the client. Each middleware class implements `__call__(self, request)` and can modify the request, call `get_response(request)` to pass to the next middleware, and modify the response on the way back. The middleware stack is configured in `settings.py` as an ordered list, and requests flow through them in order, responses flow back in reverse.

This is the Chain of Responsibility pattern with a twist: it is bidirectional (the response flows back through the same chain in reverse order). Each middleware can short-circuit by not calling `get_response()` — for example, the authentication middleware can return a 401 response without reaching the view. The middleware can also add state to the request (e.g., `request.user` is set by the `AuthenticationMiddleware`). The ordering of middleware matters — security middleware should come before business logic middleware.

**Example:**
```python
# Django middleware: Chain of Responsibility
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pre-processing: check rate limit
        if self.is_rate_limited(request):
            return JsonResponse({'error': 'Too many requests'}, status=429)

        response = self.get_response(request)  # pass to next middleware

        # Post-processing: add headers
        response['X-RateLimit-Remaining'] = self.remaining(request)
        return response
```

## Q56: How does the STL use the Allocator pattern as a Strategy for memory management?

**A:** STL containers accept an allocator template parameter that defines how memory is allocated and deallocated. The default `std::allocator<T>` uses `operator new` and `operator delete`, but custom allocators can use memory pools, arena allocators, shared memory, or stack-allocated buffers. The allocator is a Strategy pattern where the allocation algorithm is interchangeable without changing the container's interface.

This separation allows containers to work with specialized memory systems. For example, `std::vector<int, PoolAllocator<int>>` uses a pool allocator for efficient allocation of fixed-size objects. In game development, arena allocators allocate from a pre-allocated block and free everything at once, avoiding per-object deallocation overhead. The allocator strategy is resolved at compile time through templates, providing zero-cost abstraction. The allocator handles construction, destruction, and memory management, while the container handles the data structure logic.

**Example:**
```cpp
#include <vector>
#include <memory>

// Custom allocator: pool-based
template <typename T>
class PoolAllocator {
    std::vector<void*> pool;
public:
    T* allocate(size_t n) {
        // allocate from pre-allocated pool
        return static_cast<T*>(pool.back());
        pool.pop_back();
    }
    void deallocate(T* p, size_t n) {
        pool.push_back(p); // return to pool
    }
};

// Container with custom allocator strategy
std::vector<int, PoolAllocator<int>> vec;
// Uses pool allocation instead of heap allocation
```

## Q57: What design patterns underlie Spring AOP's pointcut and advice mechanism?

**A:** Spring AOP uses the **Proxy** pattern to wrap target objects, the **Interceptor** pattern (a variant of Chain of Responsibility) to process method calls, the **Strategy** pattern for different advice types (Before, After, Around), and the **Composite** pattern for combining multiple pointcuts with AND/OR logic. The `Pointcut` interface defines a Strategy for matching joinpoints; the `Advice` interface defines a Strategy for behavior at matched joinpoints.

The `Advisor` combines a Pointcut with Advice (Composite of two strategies). When a proxy intercepts a method call, it creates an `AopProxyChain` that applies all matching advisors in order — this is the Chain of Responsibility. The `Around` advice wraps the entire chain, enabling pre/post processing. The `MethodInterceptor` chain is essentially a Chain of Responsibility where each interceptor calls `proceed()` to invoke the next. The architecture: Proxy (structural) + Chain of Responsibility (behavioral) + Strategy (behavioral) + Composite (structural) work together to provide flexible AOP.

**Example:**
```java
// Proxy wraps the target
// Strategy: different advice types
@Before("execution(* com.example.*.*(..))")
public void before(JoinPoint jp) { /* before advice strategy */ }

@Around("execution(* com.example.*.*(..))")
public Object around(ProceedingJoinPoint pjp) throws Throwable {
    long start = System.nanoTime();
    Object result = pjp.proceed(); // chain continues
    log("Time: " + (System.nanoTime() - start));
    return result;
}

// Composite: multiple pointcuts
@Pointcut("execution(* com.example.*.*(..)) && @annotation(Cacheable)")
public void cacheableMethods() {}
```

## Q58: How does Django implement the Template Method pattern in its class-based views?

**A:** Django's class-based views (CBVs) are textbook Template Method. The base `View` class defines the HTTP method dispatch as a template method: `dispatch()` checks the HTTP method and calls `get()`, `post()`, `put()`, or `delete()`. Subclasses override only the methods they need. The `TemplateView` adds a `get_context_data()` template method that subclasses override to provide template context.

The full CBV hierarchy applies Template Method at multiple levels: `View.dispatch()` → `TemplateView.get()` → `get_context_data()`. Each level defines a template method that calls overridable hooks. The `FormView` adds `form_valid()` and `form_invalid()` hooks. The `CreateView` adds `get_form_class()` and `get_success_url()`. The power of this approach is that developers override small, well-defined methods to customize behavior without touching the framework's request/response lifecycle. The trade-off: deep inheritance hierarchies can be hard to follow and debug.

**Example:**
```python
# Django CBV: Template Method pattern
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'

    # Override one hook to customize behavior
    def get_queryset(self):
        return Article.objects.filter(status='published')

    # Another hook for context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = Article.objects.filter(featured=True)
        return context

# Template method chain:
# View.dispatch() -> ListView.get() -> get_queryset() -> get_context_data()
```

## Q59: How does the STL's sort function employ the Strategy pattern for comparators?

**A:** `std::sort` accepts an optional comparator parameter that serves as a Strategy for ordering elements. Without a comparator, it uses `operator<` (the default strategy). With a custom comparator, the sorting algorithm remains the same (Introsort: quicksort + heapsort + insertion sort), but the comparison strategy changes. This decouples the algorithm from the ordering policy.

The comparator is passed as a template parameter, enabling compile-time inlining. The compiler generates specialized sort code for each comparator type, eliminating virtual dispatch overhead. This is a zero-cost Strategy pattern. In modern C++, lambdas provide concise inline strategies: `std::sort(v.begin(), v.end(), [](auto& a, auto& b) { return a.score > b.score; });`. The STL also provides pre-built strategy objects like `std::greater<T>`, `std::less<T>`, and combinators like `std::compose` for complex ordering strategies.

**Example:**
```cpp
struct Student {
    std::string name;
    double gpa;
};

std::vector<Student> students;

// Default strategy: operator< (uses student's comparison)
std::sort(students.begin(), students.end());

// Custom strategy: sort by GPA descending
std::sort(students.begin(), students.end(),
    [](const Student& a, const Student& b) { return a.gpa > b.gpa; });

// Pre-built strategy object
std::sort(students.begin(), students.end(),
    [](const Student& a, const Student& b) {
        return std::tie(b.gpa, a.name) < std::tie(a.gpa, b.name);
    }); // multi-field ordering strategy
```

## Q60: Which patterns does Spring's JdbcTemplate combine and why?

**A:** `JdbcTemplate` combines the Template Method pattern (defines the fixed steps of database interaction: open connection, create statement, execute, handle exceptions, close resources) with the Callback pattern (a functional interface for the varying part — what SQL to execute and how to map results). The template method handles resource management and error handling; the callback provides the SQL-specific logic.

It also uses the Strategy pattern for `RowMapper` (strategy for mapping result sets to objects) and `SqlParameterSource` (strategy for providing query parameters). The `DataSource` is injected as a Strategy for connection management. This combination eliminates the boilerplate of JDBC: developers write only the SQL and the row mapping, while `JdbcTemplate` handles connection lifecycle, exception translation, and resource cleanup. The patterns work together: Template Method provides the skeleton, Callback provides the varying step, and Strategy provides the interchangeable components.

**Example:**
```java
// JdbcTemplate: Template Method + Callback + Strategy
List<User> users = jdbcTemplate.query(
    "SELECT * FROM users WHERE age > ?",
    new Object[]{18},  // Strategy: parameter source
    (rs, rowNum) -> {  // Callback: RowMapper strategy
        User u = new User();
        u.setId(rs.getLong("id"));
        u.setName(rs.getString("name"));
        return u;
    }
);

// Template Method handles:
// 1. Get connection from DataSource (Strategy)
// 2. Prepare statement
// 3. Execute query
// 4. Apply RowMapper (Callback)
// 5. Handle SQLExceptions
// 6. Close resources
```

## Q61: How does Django implement the Adapter pattern in its form handling layer?

**A:** Django forms act as Adapters that translate between raw HTTP request data (strings from `request.POST`) and typed Python objects. The form's `clean_<field>()` methods convert and validate string input into the appropriate Python types (integers, dates, email addresses). The form adapts the interface between the raw, untyped web layer and the typed business logic layer.

Django's `ModelForm` extends this by adapting between form fields and model fields — it translates form input directly into model instances. The form handles type conversion, validation, and error formatting, presenting a clean interface (`form.cleaned_data`) to the business logic. Without the adapter, developers would need to manually parse, validate, and convert every field from every request. The `ChoiceField` adapts between display values (human-readable labels) and stored values (database keys), acting as a value adapter.

**Example:**
```python
# Django Form: Adapter between HTTP data and Python objects
class UserForm(forms.Form):
    name = forms.CharField(max_length=100)        # str -> str
    age = forms.IntegerField(min_value=0)          # str -> int (adapter)
    birth_date = forms.DateField()                  # str -> date (adapter)
    email = forms.EmailField()                      # str -> validated email

# In view: adaptation happens automatically
def create_user(request):
    form = UserForm(request.POST)  # raw strings from HTTP
    if form.is_valid():
        # form.cleaned_data has typed Python objects
        user = User(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],       # already int
            birth_date=form.cleaned_data['birth_date'],  # already date
        )
```

## Q62: How does the STL implement the Command pattern through function objects?

**A:** The C++ STL implements the Command pattern through function objects (functors) and, in modern C++, lambdas and `std::function`. A function object encapsulates a command (an operation with its parameters) as an object that can be stored, passed, and invoked. `std::function<void()>` provides a type-erased wrapper that can hold any callable — functions, lambdas, bind expressions, or function objects.

This enables deferred execution (storing a command to invoke later), command queues (storing commands in containers), and callback mechanisms (passing commands as arguments). The `std::thread` constructor accepts a Command pattern object (any callable). `std::async` stores a command for deferred or asynchronous execution. The STL's approach is more lightweight than GoF Command because it does not require a formal Command interface — any callable (with `operator()`) satisfies the pattern through duck typing / templates.

**Example:**
```cpp
#include <functional>
#include <queue>
#include <thread>

// Command pattern: lambdas as commands
std::queue<std::function<void()>> commandQueue;

commandQueue.push([]{ std::cout << "Task 1" << std::cout); });
commandQueue.push([]{ std::cout << "Task 2" << std::cout); });

// Execute commands
while (!commandQueue.empty()) {
    commandQueue.front()(); // invoke command
    commandQueue.pop();
}

// Command with state: function object
class SaveCommand {
    std::string filename;
    std::string data;
public:
    SaveCommand(std::string f, std::string d) : filename(f), data(d) {}
    void operator()() { /* save data to file */ }
};

std::thread t(SaveCommand{"out.txt", "content"}); // async command
```

## Q63: How has Spring's use of the Factory pattern evolved from BeanFactory to annotation-based DI?

**A:** Spring's Factory pattern has evolved through three generations: (1) XML-based BeanFactory (early Spring) — beans were defined in XML, and the factory created them by reflection. (2) Java Config with `@Bean` methods — factory methods in `@Configuration` classes replaced XML. (3) Component scanning with `@Component`, `@Service`, `@Repository` — the container automatically discovers and creates beans, with the factory hidden behind annotation processing.

The evolution reflects a trend from explicit to implicit factory configuration. XML was verbose but transparent. Java Config provided type safety and IDE support. Annotation-based DI minimizes boilerplate but hides the factory mechanism. Each generation still uses the Factory pattern internally — `@Service` is processed by `ClassPathBeanDefinitionScanner` which creates bean definitions, and `ApplicationContext.getBean()` is still a factory method. The `FactoryBean` interface remains for complex creation logic. The trend is toward convention over configuration, with the factory pattern becoming invisible to application developers.

**Example:**
```java
// Generation 1: XML Factory
// <bean id="userRepo" class="com.example.UserRepository"/>

// Generation 2: Java Config Factory
@Configuration
class AppConfig {
    @Bean
    UserRepository userRepo() {
        return new UserRepository(dataSource()); // factory method
    }
}

// Generation 3: Auto-discovery Factory
@Service
class UserService { // container creates this automatically
    @Autowired
    private UserRepository repo; // container injects automatically
}
```

## Q64: How does Django's URL routing implement the Composite pattern?

**A:** Django's URL configuration is a tree of URL patterns where each pattern can contain sub-patterns. `include()` creates composite nodes that nest URL patterns under a prefix. The root `urlpatterns` list is the top-level composite, and each `include()` creates a subtree. The URL resolver traverses this tree, matching patterns at each level, until it finds the leaf (the view function).

This Composite structure allows modular URL design: each app defines its own URL patterns, and the root configuration composes them together. The `path()` function creates leaf nodes (URL patterns that map to views), while `include()` creates composite nodes (URL patterns that delegate to a sub-configuration). The resolver handles the composite traversal automatically, making the URL hierarchy transparent to views. This enables clean separation of concerns — each app manages its own URL namespace.

**Example:**
```python
# Root: composite URL tree
urlpatterns = [
    path('admin/', include('django.contrib.admin.urls')),  # composite
    path('api/', include('myapp.urls')),                   # composite
    path('blog/', include('blog.urls')),                   # composite
]

# App-level: leaf patterns
# myapp/urls.py
urlpatterns = [
    path('users/', views.user_list),           # leaf -> view
    path('users/<int:pk>/', views.user_detail), # leaf -> view
    path('orders/', include('orders.urls')),     # composite
]
```

## Q65: How does the STL implement the Decorator pattern through stream manipulators?

**A:** C++ stream manipulators (`std::setw`, `std::setprecision`, `std::fixed`, `std::hex`) implement the Decorator pattern by wrapping stream objects with additional formatting behavior. Each manipulator modifies the stream's state (field width, precision, base) and returns a reference to the same stream, allowing chaining. The stream is the base component; manipulators are decorators that add formatting.

`std::cout << std::setw(10) << std::setfill('*') << std::hex << 42` decorates the stream with three layers: width setting, fill character, and hexadecimal formatting. Each manipulator decorates the stream's output behavior without changing the stream itself. More complex decorators are the `std::ostream_iterator` and stream buffer adapters (`std::ostream_with_buffer`). The pattern is lightweight because manipulators are typically stateless function objects that modify stream flags, not heavy wrapper objects.

**Example:**
```cpp
#include <iostream>
#include <iomanip>

int main() {
    double pi = 3.14159265;

    // Chain of decorators on cout
    std::cout << std::fixed           // decorator: fixed notation
              << std::setprecision(2)  // decorator: 2 decimal places
              << std::setw(10)         // decorator: field width
              << std::setfill(' ')     // decorator: fill character
              << pi << '\n';
    // Output: "      3.14"

    // Custom decorator: custom stream manipulator
    std::ostream& bold(std::ostream& os) {
        return os << "\033[1m"; // ANSI escape for bold
    }
    std::cout << bold << "Hello" << "\033[0m\n";
}
```

## Q66: What are the trade-offs of Spring's Singleton scope versus other scoping patterns?

**A:** Spring's default Singleton scope creates one bean instance per IoC container. The trade-offs: **Pros** — minimal memory usage, no object creation overhead after startup, shared state is simple, and GC pressure is minimal. **Cons** — thread safety is the developer's responsibility (Singletons must be thread-safe), shared mutable state can cause race conditions, testing is harder (state leaks between tests), and the Singleton becomes a hidden global dependency.

Spring also provides Prototype (new instance each time), Request (one per HTTP request), Session (one per user session), and custom scopes. Request scope is ideal for request-scoped state without passing it through every method. Session scope stores per-user state. Prototype is useful for objects that should not be shared. The key decision: if the bean is stateless or has thread-safe state, Singleton is optimal. If the bean holds per-request or per-user state, use the appropriate shorter-lived scope. Mixing scopes (a Singleton depending on a Request-scoped bean) requires proxies to handle the lifecycle mismatch.

**Example:**
```java
// Singleton: one instance, shared, must be thread-safe
@Service // default scope: singleton
public class OrderService {
    private final AtomicInteger counter = new AtomicInteger(0); // thread-safe

    public Order createOrder() {
        return new Order(counter.incrementAndGet()); // thread-safe counter
    }
}

// Request scope: one per HTTP request
@RequestScope
@Component
public class RequestContext {
    private final String requestId = UUID.randomUUID().toString();
}

// Prototype: new instance every time
@Scope("prototype")
@Component
public class ShoppingCart {
    private List<Item> items = new ArrayList<>();
}
```

## Q67: How does Django's Proxy model implement the Proxy pattern and when should you use it?

**A:** Django's Proxy model creates a model that maps to the same database table as the original model but provides a different Python interface. The proxy does not create a new database table — it shares the underlying table entirely. The proxy can add methods, modify the default manager, change ordering, or provide a more specific API without altering the original model's schema or data.

Use Proxy models when: (1) you want to add methods or custom managers to a model without changing the database. (2) You need different representations of the same data (e.g., `ActiveUser` proxy of `User` that filters by `is_active=True`). (3) You want to organize models by concern without schema changes. Proxy models inherit all fields and methods from the original and can override managers andMeta class. They do NOT work for changing field definitions (use multi-table inheritance or abstract models for that). Proxy models are the purest form of the Proxy pattern — same database, different interface.

**Example:**
```python
# Original model
class User(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

# Proxy model: same table, different interface
class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class ActiveUser(User):
    objects = ActiveUserManager()

    class Meta:
        proxy = True  # no new table

    def deactivate(self):
        self.is_active = False
        self.save()

# Usage
active_users = ActiveUser.objects.all()  # only active users
```

## Q68: How does the STL's std::function implement type-erased function objects?

**A:** `std::function<R(Args...)>` uses type erasure to store any callable (function pointer, lambda, function object, member function pointer) behind a uniform interface. Internally, it uses a small buffer optimization (SBO) for small callable objects and heap allocation for larger ones. The callable is stored as a type-erased pointer, and `operator()` invokes it through a stored function pointer that knows the concrete type.

Type erasure is a combination of the Strategy and Type Object patterns. The `std::function` is a type-erased wrapper that accepts any strategy (callable) matching the signature. This enables storing heterogeneous callables in containers: `std::vector<std::function<void()>>` can hold different lambda types. The trade-off: `std::function` adds overhead compared to direct template parameters (function pointer indirection, potential heap allocation, possible SBO miss). For performance-critical code, use templates directly. For heterogeneous collections and runtime polymorphism, `std::function` is essential.

**Example:**
```cpp
#include <functional>
#include <vector>

// Type-erased callables in a single container
std::vector<std::function<int(int, int)>> operations;
operations.push_back([](int a, int b) { return a + b; });
operations.push_back([](int a, int b) { return a * b; });
operations.push_back(std::bind(std::modulus<int>{}, _1, _2));

for (auto& op : operations) {
    std::cout << op(10, 3) << '\n'; // 13, 30, 1
}

// SBO: small lambdas stored inline, no heap allocation
std::function<void()> f = []{ std::cout << "hello\n"; };
f(); // stored in small buffer inside std::function
```

## Q69: How does Spring use the Template Method pattern in its framework classes like RestTemplate?

**A:** `RestTemplate` uses Template Method for HTTP communication. The template method `execute()` defines the fixed steps: create the request, apply interceptors, send the request, handle the response, and translate exceptions. The variable steps (how to build the URL, what headers to add, how to serialize the body) are customizable through interceptors (`ClientHttpRequestInterceptor`) and strategy objects (`HttpMessageConverter` for serialization).

The `JdbcTemplate`, `HibernateTemplate`, and `TransactionTemplate` follow the same pattern. Each defines a template method that handles the framework-specific boilerplate (connection management, session handling, transaction lifecycle) and delegates the business-specific work to callback interfaces. The pattern eliminates the common framework integration boilerplate that developers would otherwise repeat. Spring's naming convention (`*Template`) signals the Template Method pattern. The trade-off: the fixed template limits flexibility for truly non-standard use cases, though callbacks and interceptors provide extension points.

**Example:**
```java
// RestTemplate: Template Method pattern
RestTemplate restTemplate = new RestTemplate();

// execute() is the template method:
// 1. Build URI (strategy: UriTemplateHandler)
// 2. Create request (callback: HttpMessageConverter)
// 3. Apply interceptors (chain: ClientHttpRequestInterceptor)
// 4. Send request (strategy: ClientHttpRequestFactory)
// 5. Handle response (callback: ResponseExtractor)
// 6. Translate exceptions (fixed: RestClientException)

User user = restTemplate.getForObject(
    "https://api.example.com/users/{id}",
    User.class, 123); // template handles the rest
```

## Q70: How does Django implement the Strategy pattern in its authentication backends?

**A:** Django's authentication system uses the Strategy pattern through `AUTHENTICATION_BACKENDS` — a configurable list of authentication strategies. Each backend implements the same interface (`authenticate(request, **credentials)`) but uses different authentication mechanisms: database password check, LDAP, OAuth2, SAML, etc. Django tries each backend in order until one returns a user or all fail.

This is the Strategy pattern because the authentication algorithm is interchangeable through configuration, not code changes. The `authenticate()` function iterates through configured backends (Chain of Responsibility), and each backend is an independent strategy. New backends can be added without modifying existing code (Open-Closed Principle). The backends are configured in `settings.py`, making the strategy selection a deployment-time concern rather than a code-time concern. This separation allows the same codebase to authenticate differently in development (database) vs. production (LDAP/OAuth).

**Example:**
```python
# settings.py: configure authentication strategies
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',    # strategy 1: DB
    'social_core.backends.google.GoogleOAuth2',      # strategy 2: Google
    'myapp.auth.LDAPBackend',                        # strategy 3: LDAP
]

# Custom strategy
class APIKeyBackend:
    def authenticate(self, request, api_key=None, **kwargs):
        if api_key:
            return User.objects.filter(api_key=api_key).first()
        return None  # pass to next backend

# Usage: chain tries each strategy
from django.contrib.auth import authenticate
user = authenticate(request, username='j', password='p') # tries all backends
```

## Q71: How do STL smart pointers implement the Proxy pattern for resource management?

**A:** `std::unique_ptr` and `std::shared_ptr` are Proxy objects that wrap raw pointers and control object lifetime. They provide the same dereference operators (`*`, `->`) as raw pointers (same interface) but add automatic deallocation when the pointer goes out of scope. `unique_ptr` is exclusive ownership (one proxy per object); `shared_ptr` is shared ownership (multiple proxies with reference counting).

Smart pointers are the most widely used Proxy pattern in modern C++. They prevent memory leaks, dangling pointers, and double-free errors. `shared_ptr` uses reference counting (the proxy manages shared state), and `weak_ptr` is a non-owning proxy that breaks cycles. The performance overhead is minimal: `unique_ptr` has zero overhead compared to raw pointers (the compiler elides the calls), and `shared_ptr` adds atomic reference counting overhead. Smart pointers should be the default choice for heap-allocated objects in modern C++.

**Example:**
```cpp
#include <memory>

// unique_ptr: exclusive proxy
auto p1 = std::make_unique<Database>(config);
// Database is automatically deleted when p1 goes out of scope

// shared_ptr: shared ownership proxy
auto p2 = std::make_shared<User>("Alice");
auto p3 = p2; // reference count = 2
// User is deleted when last shared_ptr is destroyed

// weak_ptr: non-owning observer
std::weak_ptr<User> wp = p2;
if (auto locked = wp.lock()) {
    // locked is a shared_ptr; object still alive
    locked->getName();
}
// object deleted when p2 and p3 go out of scope
```

## Q72: How does Spring implement the Builder pattern in its configuration classes?

**A:** Spring uses the Builder pattern extensively in its configuration and API classes. `UriComponentsBuilder` builds URIs step by step, `BeanDefinitionBuilder` constructs bean definitions, and `MockMvcBuilders` configures test servers. The Builder pattern is chosen when object construction has many optional parameters or when the construction process itself needs to be configurable.

In Spring Boot, the `SpringApplicationBuilder` provides a fluent API for building applications with optional components. The `RestTemplate.Builder` configures a RestTemplate with optional interceptors, message converters, and error handlers. The Builder pattern here serves two purposes: (1) it makes complex configurations readable, and (2) it enables lazy or deferred construction where the builder accumulates configuration until `build()` is called. Spring's builders often use method chaining (each setter returns `this`) for fluent syntax, and many support programmatic configuration that complements annotation-based setup.

**Example:**
```java
// Spring UriComponentsBuilder: Builder pattern
URI uri = UriComponentsBuilder
    .fromHttpUrl("https://api.example.com")
    .path("/users/{id}")
    .queryParam("include", "profile")
    .queryParam("format", "json")
    .buildAndExpand(userId)
    .toUri();

// Spring Boot RestTemplate Builder
RestTemplate restTemplate = new RestTemplateBuilder()
    .setConnectTimeout(Duration.ofSeconds(5))
    .setReadTimeout(Duration.ofSeconds(10))
    .additionalInterceptors(new LoggingInterceptor())
    .errorHandler(new CustomErrorHandler())
    .build();
```

## Q73: How does Django's middleware chain implement short-circuit processing using Chain of Responsibility?

**A:** Django middleware short-circuits by returning a response before calling `get_response(request)`, which prevents subsequent middleware and the view from executing. The `CsrfViewMiddleware` short-circuits by returning 403 if the CSRF token is invalid. The `AuthenticationMiddleware` does not short-circuit but modifies the request (adds `request.user`). The key: each middleware decides whether to pass the request forward or return a response immediately.

The short-circuit mechanism is the core of the Chain of Responsibility pattern in Django middleware. Middleware can also short-circuit on the response path — the `SecurityMiddleware` can strip sensitive headers from responses. This bidirectional short-circuiting allows security checks, rate limiting, and authentication to reject requests early, saving the cost of view execution and database queries. The ordering of middleware matters critically: security and authentication must come before business logic to ensure invalid requests are rejected before reaching expensive operations.

**Example:**
```python
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limiter = RateLimiter()

    def __call__(self, request):
        # Short-circuit: reject before reaching view
        if self.limiter.is_exceeded(request.META['REMOTE_ADDR']):
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429
            )

        # Pass to next middleware / view
        response = self.get_response(request)
        return response

# If this middleware is first in the list, rate-limited
# requests never reach subsequent middleware or the view
```

## Q74: How does the STL implement the Flyweight pattern in string optimization (SSO)?

**A:** Small String Optimization (SSO) in STL string implementations (`std::string`) is a Flyweight-like optimization. Short strings (typically up to 15-22 characters, depending on the implementation) are stored directly within the string object's memory (on the stack or inline in the object), avoiding heap allocation. Long strings are stored on the heap with a pointer. This is an intrinsic state optimization — the "flyweight" is the inline buffer that all short strings share within the string class's memory layout.

The SSO string object has a fixed size (e.g., 32 bytes on 64-bit systems) regardless of the string length. For strings shorter than the SSO threshold, the character data is stored inline in the object, and no separate heap allocation occurs. This provides the performance benefit of the Flyweight pattern (shared inline buffer, no per-string allocation) without the complexity of a separate factory and pool. For applications that create millions of short strings (parsing, concatenation), SSO provides significant memory and performance benefits by eliminating heap allocation for the common case.

**Example:**
```cpp
#include <string>

// SSO: Flyweight-like optimization
std::string short_str = "hi";  // stored inline (no heap allocation)
std::string long_str = "this string is definitely longer than SSO threshold";
// stored on heap (pointer to allocated memory)

// Both have the same type and interface
// The implementation chooses storage strategy based on length
std::cout << sizeof(short_str) << '\n'; // typically 32 bytes (fixed)
std::cout << sizeof(long_str) << '\n';  // same 32 bytes (metadata + pointer)

// Evidence of SSO: no new/delete for short strings
// Custom allocator or overloads can verify this
```

## Q75: How does Spring use the Composite pattern in its BeanDefinition hierarchy?

**A:** Spring's `BeanDefinition` objects form a hierarchy where child bean definitions can inherit from parent bean definitions. The `AbstractBeanDefinition` is the base; `GenericBeanDefinition`, `RootBeanDefinition`, and `ChildBeanDefinition` form the composite hierarchy. A child bean definition inherits property values, constructor arguments, and method overrides from its parent, only specifying the differences.

This is the Composite pattern applied to configuration: the parent bean definition serves as a template, and children compose by inheriting and overriding specific properties. For example, a `prototypeTemplate` bean definition might define common properties (connection timeout, pool size), and child definitions for `developmentDataSource` and `productionDataSource` override only the URL and credentials. The container resolves the composite hierarchy at bean creation time, merging parent and child definitions. This reduces configuration duplication and ensures consistency across related beans.

**Example:**
```xml
<!-- Parent: template bean definition -->
<bean id="baseDataSource" abstract="true"
      class="com.zaxxer.hikari.HikariDataSource">
    <property name="maximumPoolSize" value="10"/>
    <property name="connectionTimeout" value="30000"/>
</bean>

<!-- Child: inherits from parent, overrides specifics -->
<bean id="devDataSource" parent="baseDataSource">
    <property name="jdbcUrl" value="jdbc:h2:mem:dev"/>
    <property name="username" value="sa"/>
</bean>

<bean id="prodDataSource" parent="baseDataSource">
    <property name="jdbcUrl" value="jdbc:postgresql://prod:5432/db"/>
    <property name="username" value="app"/>
    <property name="maximumPoolSize" value="50"/> <!-- override -->
</bean>
```

## Q76: Defend your use of the Singleton pattern in a distributed microservice architecture

**A:** In a distributed microservice architecture, Singleton is justified for per-JVM resources: connection pools, thread pools, caches, and configuration holders. These are genuinely single-instance resources within a single JVM process. The Singleton pattern here does not mean "one instance across the cluster" — it means "one instance per service instance." The DI container (Spring, Guice) manages singleton-scoped beans, which is the modern equivalent of the Singleton pattern.

The defense: (1) **Resource efficiency** — one connection pool per JVM prevents resource exhaustion. (2) **Configuration consistency** — one configuration holder ensures all components read the same config. (3) **Thread safety** — a single cache instance with proper synchronization is more efficient than multiple instances. The criticism of Singleton applies to global mutable state that crosses service boundaries — within a single service, singleton-scoped beans are the standard approach. The key is to use DI-managed singletons rather than hand-rolled static singletons, as DI provides testability (replaceable in tests) and lifecycle management.

## Q77: When is the criticism against Singleton as an anti-pattern valid, and when is it not?

**A:** Singleton criticism is **valid** when: (1) it hides dependencies — a class calling `Singleton.getInstance()` has a hidden dependency that is not visible in its API or constructor, making it untestable. (2) It creates global mutable state — shared state accessible from anywhere leads to unpredictable side effects. (3) It makes testing difficult — the singleton's state leaks between tests. (4) It couples the system to a specific implementation — you cannot substitute a mock for the singleton.

The criticism is **not valid** when: (1) The singleton manages a truly global resource (connection pool, thread pool) that should have exactly one instance. (2) The singleton is stateless or uses immutable configuration — no shared mutable state. (3) The singleton is managed by a DI container — it is replaceable in tests via DI overrides. (4) The alternative (passing the instance everywhere) adds unnecessary complexity to the API. The modern resolution: use DI-managed singleton scope, not the static `getInstance()` pattern. This preserves the one-instance guarantee while eliminating the hidden dependency and testability problems.

## Q78: Why would you choose Strategy over inheritance for this payment processing system?

**A:** The payment system needs to support credit card, PayPal, and cryptocurrency payments. Inheritance would create `PaymentProcessor` base class with `CreditCardProcessor`, `PayPalProcessor`, etc. Strategy is better here because: (1) **Runtime flexibility** — the payment method is determined by user selection at runtime, not at compile time. Strategy allows swapping the algorithm per request. (2) **Combinability** — if processing also needs logging or retry behavior, Strategy composes naturally with Decorator, while inheritance creates class explosion. (3) **Testability** — Strategy objects can be mocked and tested independently; inheritance creates tight coupling between base and derived classes. (4) **Single Responsibility** — each strategy handles one payment method; the context handles the processing flow. Inheritance would mix the processing flow with the payment method logic.

The practical argument: the team has three payment methods now, and the product roadmap shows five more. With inheritance, that is eight subclasses of one base. With Strategy, it is eight strategy objects used by one context class. The context can be tested once; each strategy is tested independently. When a new payment method is added, only one new class is needed — no modification of existing code.

## Q79: Defend using a Factory pattern over constructor-based dependency injection

**A:** Factory pattern is preferable over constructor injection when: (1) **Object creation is complex** — if constructing the object requires logic (connection strings from environment, choosing implementation based on config, initializing from a file), a factory encapsulates that complexity. Constructor injection requires the caller to already have the fully constructed dependencies, which pushes creation complexity to the caller. (2) **Prototype or pooled objects** — if objects are created from prototypes, cloned, or pooled, a factory manages that lifecycle. (3) **Lazy creation** — a factory can defer expensive object creation until needed.

However, constructor injection is generally preferred for application services because it makes dependencies explicit and the class easy to test. The best approach combines both: a Factory creates the object (handles complex creation logic), and constructor injection provides the factory's dependencies. Spring itself uses this approach — `FactoryBean<T>` creates complex objects, and the factory's dependencies are injected via constructor injection.

## Q80: Why might the Composite pattern become dangerous at scale in a file system abstraction?

**A:** In a file system abstraction, Composite is natural (files and directories are uniformly accessed), but at scale, it becomes dangerous because: (1) **Performance** — operations on the root composite must traverse the entire tree. Computing the total size of a 10-million-file directory tree requires visiting every node. (2) **Depth** — deeply nested composites can cause stack overflow in recursive operations. A directory structure 1000 levels deep will blow the call stack. (3) **Mutation side effects** — modifying a composite node (rename, move) affects all children, which may have unexpected performance impacts. (4) **Concurrency** — concurrent modifications to different parts of the tree can conflict if the tree uses coarse-grained locking.

The mitigation: (1) Add depth limits to prevent stack overflow. (2) Use iterative (stack-based) traversal instead of recursive. (3) Cache aggregate properties (size, count) in composite nodes and invalidate on mutation. (4) Use fine-grained locking or copy-on-write for concurrent access. The key lesson: Composite works well for small, shallow trees but requires careful engineering for large, deep ones.

## Q81: When does the Observer pattern degrade into an anti-pattern, and how do you prevent it?

**A:** Observer degrades when: (1) **Notification storms** — one observer modifies the subject, triggering another notification, which triggers another observer, creating a cascade. This is the "laval observer" problem. (2) **Memory leaks** — observers are not unregistered and accumulate in the subject's list. (3) **Ordering dependencies** — observers depend on being called in a specific order, creating hidden coupling. (4) **Debugging difficulty** — the flow of control is implicit (event-driven), making it hard to trace. (5) **Unhandled exceptions** — one observer's exception can prevent other observers from being notified.

Prevention: (1) Use a message queue (Kafka, RabbitMQ) instead of in-process Observer for distributed systems — it provides ordering guarantees, dead letter queues, and retry mechanisms. (2) Implement observer priority levels and enforce notification order. (3) Use weak references or lifecycle-aware registration. (4) Wrap each observer notification in try-catch to isolate failures. (5) Document the notification contract: what events are fired, in what order, with what data. (6) Consider the Mediator pattern when observers need to communicate with each other.

## Q82: Defend your pattern choice under strict memory and latency constraints

**A:** Under strict memory and latency constraints (embedded systems, high-frequency trading), prefer patterns with zero-cost abstractions: (1) **Strategy via templates** (C++ templates, Rust generics) — compile-time polymorphism with no virtual dispatch overhead. (2) **Flyweight** for shared immutable data — reduces memory by sharing intrinsic state. (3) **Flyweight via interning** — share duplicate strings or objects in memory. (4) **Avoid patterns that add indirection** — Proxy, Decorator, and virtual dispatch add overhead. Use them only when the benefit justifies the cost.

The defense: in high-performance systems, patterns are tools, not mandates. Use the pattern that solves the problem with minimal overhead. C++ achieves zero-cost Strategy through templates (no virtual call, inlined at compile time). Rust achieves zero-cost Iterator through monomorphization. Java achieves near-zero-cost Strategy through JIT inlining of devirtualized calls. The key is to measure first — pattern overhead is often negligible compared to I/O, but in tight loops, every nanosecond matters. Choose patterns that compile down to the same machine code as hand-written procedural code.

## Q83: Why might you deliberately reject all GoF patterns in a microservice endpoint?

**A:** A simple CRUD microservice endpoint (receive HTTP request, validate, persist, return response) does not benefit from GoF patterns because: (1) **Complexity without value** — Strategy for a single algorithm, Observer for a single notification, Factory for a single class — these add indirection without flexibility. (2) **YAGNI** — the endpoint has one behavior, not a family of interchangeable behaviors. Patterns solve problems of variation and coordination that do not exist here. (3) **Readability** — a simple class with constructor injection is easier to understand than a Factory + Strategy + Observer composition. (4) **Startup time** — patterns that use reflection (Factory, Proxy) add to application startup time, which matters for serverless and scale-to-zero deployments.

The principle: patterns are solutions to recurring problems. If the problem does not recur (simple endpoint, single behavior, no variation), the pattern adds overhead without benefit. Write simple, direct code first. Introduce patterns when the complexity warrants it — when you have two or more strategies, multiple observers, or complex object creation. The best code is the simplest code that works correctly and can be understood by the team.

## Q84: When does the Decorator pattern hurt maintainability more than it helps?

**A:** Decorator hurts when: (1) **Too many layers** — five stacked decorators (`Logging → Caching → Retry → CircuitBreaker → Auth → RealService`) make debugging extremely difficult. The call stack goes through all five decorators before reaching the real service, and each can modify the request/response. (2) **Order sensitivity** — the behavior changes depending on decorator order, creating hidden coupling. (3) **Interface bloat** — if the base interface has 20 methods, every decorator must implement all 20, even if it only cares about one. (4) **Missing error handling** — if a decorator does not properly propagate exceptions, it silently swallows errors.

Mitigation: (1) Limit the number of decorator layers (3-4 maximum). (2) Use a composition tool (Interceptor chain in Spring, Middleware in Django) instead of manual decorator stacking. (3) Use the Interface Segregation Principle — small interfaces that decorators can selectively implement. (4) Document the expected decorator order. (5) Add logging/tracing at each decorator layer for debugging. When decorator complexity exceeds its benefits, consider Aspect-Oriented Programming (AOP) or middleware chains.

## Q85: Defend your architectural pattern choice for a real-time trading system

**A:** A real-time trading system requires: sub-millisecond latency, high throughput, fault tolerance, and strict ordering. The architectural patterns: (1) **Event Sourcing** — every trade is an immutable event, enabling perfect audit trails and replay. (2) **CQRS** — separate read and write models, optimizing the write path for append-only operations and the read path for fast queries. (3) **Lock-free data structures** — Strategy for order matching using non-blocking algorithms. (4) **Flyweight** — shared market data objects (tickers, prices) to minimize memory allocation. (5) **Observer** — real-time price feeds pushed to subscribers.

The defense: these patterns are chosen because the system's requirements (latency, throughput, consistency) demand them. Event Sourcing provides perfect auditability required by financial regulators. CQRS separates the write path (trade execution, which must be fast) from the read path (portfolio display, which can be eventually consistent). Flyweight minimizes GC pauses in high-frequency object creation. The trade-off is increased complexity, but in this domain, the complexity is justified by the performance and compliance requirements.

## Q86: Why would you combine three patterns here instead of using one simpler solution?

**A:** The requirement: a notification system that supports multiple channels (email, SMS, push), multiple templates per channel, and retry with exponential backoff. No single pattern handles all three concerns: (1) **Strategy** — for selecting the notification channel (email/SMS/push). (2) **Template Method** — for the channel-specific rendering pipeline (template selection → variable substitution → formatting). (3) **Chain of Responsibility** — for the retry mechanism (try → fail → backoff → retry → fail → alert).

Combining three patterns is justified because each addresses a distinct axis of variation. Using only Strategy would not handle the rendering pipeline or retry logic. Using only Chain of Responsibility would not handle channel selection. The patterns compose cleanly: Strategy selects the channel, Template Method defines the rendering within that channel, and Chain of Responsibility wraps the entire process with retry logic. The combined design is more complex than any single pattern but significantly simpler than a monolithic class with nested conditionals handling all three concerns.

## Q87: When does the Builder pattern become over-engineering for the use case?

**A:** Builder is over-engineering when: (1) **Few parameters** — if the object has 2-3 required fields and no optional fields, a constructor is simpler and more concise. `new Point(x, y)` is clearer than `Point.builder().x(1).y(2).build()`. (2) **Immutable objects with all-required fields** — if every field is required and immutable, a constructor with named parameters (Kotlin, Scala) or a simple constructor suffices. (3) **Single use** — if the builder is used once in the codebase, the cost of creating the builder class (30-50 lines of boilerplate) exceeds the benefit. (4) **Domain objects** — JPA entities, data transfer objects, and simple POJOs do not need builders.

The decision criteria: use Builder when (a) the object has more than 4-5 parameters, (b) many parameters are optional, (c) the object is immutable after construction, and (d) the constructor call site needs to be readable. For simple data objects, use records (Java 16+), data classes (Kotlin), or Lombok's `@Builder` to reduce boilerplate. The best builder is one generated by the language or framework, not hand-written.

## Q88: Defend the State pattern over a simpler conditional-chain approach for this protocol handler

**A:** A protocol handler processes messages based on its current state (connecting, connected, authenticating, ready, closing). The conditional approach uses `if (state == CONNECTING && msg.type == ACK)` in every method. The State pattern is superior here because: (1) **Number of states × operations** — with 5 states and 8 message types, the conditional approach requires 40 cases across methods. The State pattern requires 5 state classes with 8 methods each, but each method handles only one state's behavior — 40 cases organized into 5 coherent units. (2) **Transitions are explicit** — state classes have `transitionTo()` calls that make state changes visible and auditable. (3) **Adding states** — adding a new state requires a new class, not modifying every switch statement. (4) **Testing** — each state can be tested independently without setting up the entire state machine.

The State pattern is justified when the state-to-behavior matrix is large (more than 3 states with different behaviors). For 2-3 states, conditionals are simpler. The key insight: the State pattern does not reduce total code — it reorganizes it from "all behaviors in one place per state" to "all states for one behavior in one place." This reorganization is valuable when the matrix is large.

## Q89: Why might heavy use of the Adapter pattern indicate a deeper design smell?

**A:** Heavy Adapter usage suggests the system is integrating multiple incompatible interfaces without establishing a common abstraction. If every external system needs an Adapter, the internal design may be too tightly coupled to one specific external interface. When a new external system is added, instead of creating a new Adapter, consider whether the internal design should use a domain-specific interface that external systems adapt to.

The deeper smell: if you have 10 Adapters, the underlying problem may be that the system lacks a proper anti-corruption layer. Instead of adapting each external system individually, create a unified domain interface and implement it once per external system. This is the Repository pattern (adapting different databases behind a common interface) or the Strategy pattern (adapting different algorithms behind a common interface). Heavy Adapter usage is a symptom; the cure is designing a proper abstraction layer. When adapters are simple (one method), they are fine. When they require complex mapping logic, the abstraction is wrong.

## Q90: When does Chain of Responsibility hurt debuggability, and how would you mitigate it?

**A:** Chain of Responsibility hurts debuggability when: (1) **Dynamic chains** — the handler chain is configured at runtime, so the actual processing path is not visible in the code. (2) **Implicit short-circuiting** — a handler may silently drop a request without logging, making it hard to trace why a request was not processed. (3) **Many handlers** — a chain with 10+ handlers is difficult to mentally trace. (4) **Cross-cutting side effects** — handlers may modify shared state, causing non-obvious interactions.

Mitigation: (1) **Log every handler** — each handler should log entry, exit, and whether it passed the request forward. Use structured logging with correlation IDs. (2) **Pipeline visualization** — provide a debug endpoint or tool that shows the handler chain configuration. (3) **Handler naming** — give each handler a descriptive name that appears in logs. (4) **Circuit breakers** — add a max-chain-depth counter to prevent infinite loops. (5) **Tracing** — use distributed tracing (OpenTelemetry) to visualize the request flow through handlers. (6) **Documentation** — maintain a diagram of the handler chain with ordering and conditions.

## Q91: Defend your pattern choice for a memory-constrained embedded system

**A:** In a memory-constrained embedded system (kilobytes of RAM), pattern choices are driven by memory overhead: (1) **Flyweight** — essential for shared constant data (lookup tables, character maps, configuration strings). (2) **Strategy via function pointers** (C) — zero-overhead polymorphism using function pointers instead of vtables. No object overhead, no RTTI. (3) **State via lookup tables** — encode state transitions in const arrays instead of state class objects. (4) **Avoid** — no dynamic allocation patterns (Factory creating heap objects, Builder with temporary objects). Prefer stack allocation and compile-time configuration.

The defense: embedded patterns prioritize deterministic memory usage over flexibility. A Strategy implemented as a function pointer uses 4-8 bytes (the pointer) vs. a vtable-based object using 16+ bytes (vptr + data). A Flyweight for lookup tables uses ROM instead of RAM. State machines encoded as tables are constant-size regardless of complexity. The patterns are adapted to the constraints: the concept is the same (interchangeable behavior, shared state, state transitions), but the implementation avoids heap allocation, virtual dispatch, and dynamic sizing.

## Q92: Why prefer object composition via patterns over inheritance in this class hierarchy?

**A:** The `Vehicle` hierarchy has `Car`, `Truck`, `Bike` with inheritance, and behavior variants (electric, manual, automatic) creating a diamond inheritance problem. Composition via patterns solves this: (1) **Strategy** for engine type — inject `ElectricEngine` or `CombustionEngine` into any vehicle. (2) **Decorator** for features — `WithGPS(vehicle)`, `WithSunroof(vehicle)` wrap any vehicle. (3) **Composite** for combinations — a vehicle has multiple features composed together.

Inheritance creates a rigid hierarchy where adding a new dimension (electric + manual + GPS) requires a new class for every combination (n × m × k classes). Composition creates n + m + k classes that combine freely. The inheritance hierarchy also suffers from the fragile base class problem — changing `Vehicle` affects all subclasses. Composition isolates changes: changing `ElectricEngine` affects only vehicles using it. The trade-off: composition requires more objects in memory and more indirection, but provides flexibility that inheritance cannot match.

## Q93: When does the Template Method pattern violate the Open-Closed Principle?

**A:** Template Method violates OCP when new variations require modifying the base class. If the template method calls hook methods that need new parameters for new subclasses, the base class must change — every subclass is affected. For example, if `DataProcessor.process()` calls `transform(Data data)` and a new processor needs `transform(Data data, Config config)`, changing the `transform` signature breaks all existing subclasses.

Additionally, if the algorithm skeleton itself changes (a new step is added), all subclasses must be updated. Template Method is "closed for modification" only when the set of overridable methods and the algorithm structure are truly stable. If the algorithm evolves (new steps, changed step order), the base class changes and all subclasses are affected. The mitigation: keep hook methods generic (accept `Object` or a context object that can be extended without changing the signature), and use composition instead of Template Method when the algorithm is likely to change.

## Q94: Defend your pattern selection under high-concurrency, lock-free requirements

**A:** Under lock-free requirements (high-frequency trading, real-time systems), prefer patterns that avoid mutual exclusion: (1) **Strategy via templates** — compile-time polymorphism eliminates virtual dispatch overhead, enabling inlining in hot paths. (2) **Flyweight** with `ConcurrentHashMap` for shared immutable objects — `computeIfAbsent` for thread-safe lazy creation without locks. (3) **Observer via lock-free queues** — `ConcurrentLinkedQueue` for non-blocking notification. (4) **State via compare-and-swap** — `AtomicReference<State>` for lock-free state transitions.

The defense: these patterns are chosen because they provide the required behavior (interchangeable algorithms, shared objects, event notification, state management) without blocking threads. The alternative (adding locks) would violate the lock-free requirement and create contention bottlenecks. The key insight: patterns are about organizing behavior, not about locking. A Strategy pattern implemented with lock-free atomics provides the same flexibility as one with locks but without the contention. The engineering challenge is ensuring correctness without locks — this requires careful use of `volatile`, atomics, and memory ordering guarantees.

## Q95: Why might the Proxy pattern add unacceptable latency in a hot path?

**A:** In a hot path (inner loop, high-frequency method call), the Proxy adds: (1) **Method dispatch overhead** — the proxy must forward every call to the real object, adding one level of indirection. For virtual proxies, this includes lazy initialization logic on first call. (2) **Cache lookup overhead** — caching proxies must check the cache on every call (hash map lookup, invalidation check). (3) **Synchronization overhead** — thread-safe proxies may use locks or atomic operations. (4) **Object allocation** — the proxy object itself consumes memory and may cause GC pressure.

In microbenchmarks, proxy overhead can be 5-50 nanoseconds per call. In a tight loop executing billions of iterations, this adds seconds of overhead. The mitigation: (1) **Remove the proxy** from the hot path — move it to the call site instead of wrapping each object. (2) **Use compiler optimizations** — JIT can inline through proxies if the type is monomorphic. (3) **Profile first** — measure whether the proxy overhead is significant compared to the actual work. Often, the proxy's caching saves more time than it costs. (4) **Use specialized proxies** — CGLIB-generated proxies with direct field access are faster than reflection-based proxies.

## Q96: When should you deliberately avoid all design patterns and write straightforward code?

**A:** Avoid patterns when: (1) **The problem is simple** — a CRUD endpoint, a data transformation script, a one-off utility. Patterns add complexity without value. (2) **YAGNI is in effect** — the anticipated variation that justifies the pattern has not materialized and may never materialize. (3) **The team is junior** — introducing advanced patterns into a team unfamiliar with them creates maintenance burden. (4) **Prototype/MVP stage** — speed of development matters more than architectural elegance. Get the product working first, refactor with patterns later. (5) **The code is throwaway** — migration scripts, one-off data fixes, proof-of-concept code that will not be maintained.

The principle: patterns are tools for managing complexity. If there is no complexity to manage, the pattern is unnecessary overhead. Write the simplest code that works correctly. When the code grows and complexity increases, refactor into patterns at that point. Premature pattern application is as harmful as premature optimization — it adds abstraction before the need for it is proven. The best indicator for needing a pattern: when you find yourself writing the same boilerplate for the third time, or when a simple modification requires changes in five places.

## Q97: Defend your design approach when integrating with a brittle legacy system

**A:** When integrating with a brittle legacy system: (1) **Anti-Corruption Layer (ACL)** — create an Adapter layer that translates between the legacy system's interface and your clean domain model. The ACL absorbs all the legacy system's quirks (inconsistent data formats, undocumented behaviors, error codes). (2) **Facade** — provide a simplified interface over the legacy system's complex API. (3) **Strategy** — make the integration pluggable so you can replace the legacy system later without changing your domain code. (4) **Observer** — when the legacy system pushes updates, use an event-driven approach to decouple your system from the legacy system's timing.

The defense: these patterns isolate your domain from the legacy system's instability. The ACL means changes in the legacy system only affect the adapter, not your core business logic. The Facade simplifies testing (mock the facade, not the legacy system). The Strategy means when the legacy system is replaced, you implement a new strategy and swap it in. The key principle: treat the legacy system as an external boundary. Your domain code should never know it is talking to a legacy system — the adapter makes it look like any other service.

## Q98: Why would you extract a pattern from currently working, well-tested code?

**A:** Extracting a pattern from working, tested code is justified when: (1) **Maintenance cost is high** — every change requires modifying multiple places, and the changes follow a predictable pattern (code smell). (2) **Adding features requires modifying existing code** — violating OCP. Extracting a Strategy or Factory means new features are added by creating new classes, not modifying existing ones. (3) **The code is duplicated** — the same algorithm appears in multiple places with slight variations. Template Method or Strategy eliminates the duplication. (4) **The team is growing** — new developers need to understand the codebase. Patterns provide shared vocabulary and predictable structure.

The refactoring is justified by the predictability of future changes, not by current pain. If the code will not change for the next five years, leave it alone. If the product roadmap shows frequent changes in the areas affected by the pattern, the extraction pays for itself in reduced modification risk. The key: do not refactor for elegance alone. Refactor when the current structure causes measurable pain (bug rate, time-to-change, onboarding time) or when future changes are predictable and frequent.

## Q99: When does pattern combination become architectural over-design?

**A:** Pattern combination becomes over-design when: (1) **The team cannot explain the architecture** — if developers cannot draw the pattern interactions on a whiteboard, the system is too complex. (2) **Adding a simple feature requires modifying five pattern implementations** — the patterns have become coupled to each other. (3) **More code is pattern infrastructure than business logic** — the abstraction overhead exceeds the business value. (4) **The system has performance problems caused by pattern indirection** — too many proxies, decorators, and strategy dispatches in the critical path. (5) **Testing requires mocking 10 objects** to test one simple business rule.

The threshold: if you need more than 2-3 patterns to solve the problem, you are likely over-engineering. Most systems need: one creational pattern (Factory or Builder), one structural pattern (Facade or Decorator), and one behavioral pattern (Strategy or Observer). If you are using five or more patterns together, question whether the complexity is justified by the problem's actual requirements. The best architecture is the simplest one that meets the requirements — patterns should reduce complexity, not increase it.

## Q100: Senior defense: justify your complete design for a system with competing requirements

**A:** The system must be real-time (sub-100ms latency), durable (no data loss), scalable (10x traffic growth), and maintainable (team of 8 developers). These requirements compete: real-time favors in-memory processing, durability favors disk writes, scalability favors distribution, and maintainability favors simplicity.

The design: (1) **Event Sourcing** — all state changes are events persisted to an append-only log. This provides durability (events are the source of truth), auditability (full history), and scalability (events can be replayed to rebuild state). The trade-off: eventual consistency in read models. (2) **CQRS** — separate write model (optimized for event appending) and read model (optimized for queries). The write path uses a **Strategy** for different event types; the read path uses a **Repository** with denormalized views. (3) **Flyweight** for market data objects — shared price/ticker objects reduce memory pressure. (4) **Observer** for real-time notifications — price updates pushed to subscribers via WebSocket. (5) **State** for order lifecycle — orders transition through states (pending, matched, filled, settled) with explicit state objects.

The justification: each pattern addresses a specific requirement. Event Sourcing provides durability without sacrificing write performance (append-only). CQRS separates the read and write optimization paths. Flyweight handles memory pressure from high-frequency data. Observer provides real-time push. State manages order lifecycle cleanly. The patterns compose without circular dependencies: Events flow through the write path → event store → read model → query path. The team can understand each pattern's role independently. The architecture is complex but justified by the competing requirements — no simpler design meets all four requirements simultaneously.
