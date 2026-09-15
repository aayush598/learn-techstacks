# FAANG, MAANG and YC Startup OOPS Rounds — 100 Interview Q&A

## Q1: What is the difference between abstraction and encapsulation, and how do they manifest in a real Java class hierarchy?

**A:** Abstraction is the process of hiding implementation details and exposing only the essential features of an object. It is achieved through abstract classes and interfaces. Encapsulation, on the other hand, is the bundling of data and methods that operate on that data into a single unit (class) while restricting direct access to some components, typically through access modifiers like `private` and `protected`.

In a real Java project, abstraction defines *what* an object does, while encapsulation defines *how* its internal state is protected. For example, a `PaymentGateway` interface abstracts the contract of processing payments, while a `StripePaymentProcessor` class encapsulates the API key, retry logic, and response parsing internally.

The two concepts complement each other: abstraction enables polymorphism at the design level, while encapsulation ensures that the concrete implementations behind abstractions are safe from external interference. Senior engineers at top companies expect candidates to articulate this distinction clearly and show awareness of how each concept supports maintainability and testability.

**Example:**
```java
// Abstraction
public interface PaymentProcessor {
    PaymentResult process(double amount, Currency currency);
}

// Encapsulation
public class StripePaymentProcessor implements PaymentProcessor {
    private final String apiKey;
    private final HttpClient httpClient;

    private StripePaymentProcessor(String apiKey) {
        this.apiKey = apiKey;
        this.httpClient = new HttpClient();
    }

    @Override
    public PaymentResult process(double amount, Currency currency) {
        StripeRequest req = new StripeRequest(amount, currency, apiKey);
        return httpClient.post(req);
    }
}
```

## Q2: Explain the SOLID principles with a concrete example from a chat application.

**A:** SOLID stands for five design principles that make object-oriented designs more understandable, flexible, and maintainable. In a chat application context: **Single Responsibility** means a `MessageRepository` handles only persistence, not encryption or delivery. **Open/Closed** means you can add a new notification channel (email, push) without modifying existing code, using polymorphism. **Liskov Substitution** ensures that any `NotificationSender` subtype (SMS, email) can replace the base type without breaking correctness. **Interface Segregation** means chat clients don't depend on a monolithic `ChatService` but on focused interfaces like `MessageSender` and `PresenceTracker`. **Dependency Inversion** means high-level message routing depends on abstractions, not concrete transport implementations.

In practice at companies like Meta or Google, violating SOLID in a chat system leads to cascading failures. For instance, if `ChatServer` directly instantiates `MySQLMessageStore`, you cannot swap to Cassandra during peak load. By depending on a `MessageStore` interface, the system stays adaptable.

Senior interviewers often ask follow-ups like "which SOLID principle would you prioritize first?" The answer is usually Dependency Inversion and Interface Segregation, because they unlock testability and replaceability — critical for systems that must evolve without downtime.

## Q3: What is the difference between a shallow copy and a deep copy, and when would you use each?

**A:** A shallow copy creates a new object but copies references to the original's nested objects. A deep copy creates a new object and recursively copies all nested objects, producing a fully independent clone. In Java, the default `clone()` method performs a shallow copy.

Use shallow copy when the nested objects are immutable or shared by design. For example, a `ChatMessage` that references an immutable `UserId` object can be shallow-copied safely. Use deep copy when mutations to the clone must not affect the original — such as duplicating an `Order` object in an e-commerce system before applying a discount, so the original order remains unchanged.

In FAANG interviews, follow-ups often probe awareness of `Cloneable` pitfalls in Java. The recommended approach is to use copy constructors or a serialization-based deep copy rather than relying on `Object.clone()`, which is fragile and breaks with inheritance hierarchies.

**Example:**
```java
public class Order implements Cloneable {
    private String orderId;
    private List<OrderItem> items;

    // Deep copy via copy constructor
    public Order(Order other) {
        this.orderId = other.orderId;
        this.items = other.items.stream()
            .map(OrderItem::new)
            .collect(Collectors.toList());
    }
}
```

## Q4: How does the Liskov Substitution Principle apply to a notification system with multiple channels?

**A:** Liskov Substitution Principle (LSP) states that objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program. In a notification system, if `EmailNotification` extends `Notification`, then anywhere a `Notification` is expected, an `EmailNotification` must work without surprising behavior.

A classic violation: `PushNotification` silently ignores messages longer than 256 characters, while the base `Notification.send()` contract promises all messages are delivered. This breaks LSP because code relying on `Notification` cannot trust that every subtype will fully deliver the message.

To satisfy LSP, you either enforce the contract at the interface level (e.g., `Notification` declares `send()` with a precondition that the message fits the channel's limits, and the caller is responsible), or you split into `ShortNotification` and `LongNotification` interfaces. Top companies test whether you can spot these subtle contract violations rather than just knowing the principle by name.

## Q5: What is polymorphism and how does method overloading differ from method overriding?

**A:** Polymorphism allows objects of different types to be treated through a unified interface. There are two kinds in Java: compile-time (static) polymorphism achieved via method overloading, and runtime (dynamic) polymorphism achieved via method overriding.

Method overloading means multiple methods share the same name but differ in parameter types or count within the same class. The compiler resolves which method to call at compile time. Method overriding means a subclass provides a specific implementation of a method already defined in its superclass, and the JVM resolves which implementation to call at runtime based on the actual object type.

In senior interviews, the deeper point is that overriding is the mechanism that makes polymorphism powerful in OOP design. Overloading is merely syntactic convenience. When designing a `Logger` interface, overriding allows `FileLogger` and `ConsoleLogger` to each implement `log()` differently, enabling the caller to remain decoupled from the concrete logger.

**Example:**
```java
public class NotificationDispatcher {
    // Overloading
    public void dispatch(String message) { dispatch(message, Priority.NORMAL); }
    public void dispatch(String message, Priority priority) { /* ... */ }

    // Polymorphism via overriding
    public void broadcast(NotificationChannel channel, String msg) {
        channel.send(msg); // which send() runs depends on runtime type
    }
}
```

## Q6: Explain composition over inheritance with an example from an e-commerce cart system.

**A:** Composition means building complex objects by combining simpler, focused objects rather than forming deep inheritance hierarchies. The mantra "favor composition over inheritance" (from the Gang of Four) exists because inheritance creates tight coupling between parent and child, while composition allows flexible runtime behavior changes.

In an e-commerce cart, inheriting from a `BaseProduct` class to create `PhysicalProduct`, `DigitalProduct`, and `SubscriptionProduct` leads to a fragile hierarchy. What happens when you need a product that is both physical and subscribable? Multiple inheritance is not supported in Java.

Instead, compose the cart item with strategy objects: a `DeliveryStrategy`, a `PricingStrategy`, and a `TaxStrategy`. Each strategy is an interface with concrete implementations. A cart item can be assembled with any combination: `new CartItem(sku, new PhysicalDelivery(), new RecurringPricing(), new GSTTax())`. This is more flexible, testable, and avoids the diamond problem.

**Example:**
```java
public class CartItem {
    private final String sku;
    private final DeliveryStrategy delivery;
    private final PricingStrategy pricing;
    private final TaxStrategy tax;

    public CartItem(String sku, DeliveryStrategy d, PricingStrategy p, TaxStrategy t) {
        this.sku = sku; this.delivery = d; this.pricing = p; this.tax = t;
    }

    public Money calculateTotal(int quantity) {
        Money base = pricing.price(quantity);
        Money tax = this.tax.apply(base);
        return base.add(tax);
    }
}
```

## Q7: What is the purpose of an abstract class versus an interface in Java, and when would you choose one over the other?

**A:** An abstract class can have instance variables, constructors, non-abstract methods with implementations, and both access modifiers on members. An interface (pre-Java 8) could only have public abstract methods and constants. Since Java 8, interfaces can have default and static methods, narrowing the gap, but abstract classes still support state (fields) and constructors.

Choose an abstract class when related classes share common state and behavior — for example, `AbstractRepository<T>` providing shared `findById()` and `save()` logic with a `JdbcTemplate` field. Choose an interface when you need to define a contract that unrelated classes can implement — for example, `Serializable`, `Comparable`, or `PaymentProcessor`.

In MAANG interviews, the follow-up is often: "Can you extend multiple abstract classes?" No, Java permits only single inheritance of classes. Interfaces allow multiple inheritance of type. For this reason, many senior architects default to interfaces for public APIs and use abstract classes only as internal base classes where shared state is genuinely needed.

## Q8: How does the Factory Pattern help in an object-heavy system like a ride-sharing platform?

**A:** The Factory Pattern encapsulates object creation logic, decoupling the client code from concrete class instantiation. In a ride-sharing platform, the types of rides (Economy, Premium, Pool, XL) each have different vehicle requirements, pricing rules, and matching algorithms. A `RideFactory.create(RideType type, Location pickup)` centralizes these decisions.

Without a factory, every call site that needs a ride would contain conditional logic (`if type == ECONOMY then new EconomyRide(...)`), violating the Open/Closed Principle. The factory makes it easy to add new ride types by adding a new branch or registration, without modifying calling code.

Factories also enable caching, pooling, and validation. The factory can enforce invariants like "Premium rides must have vehicles with rating above 4.8" at creation time, rather than letting invalid objects slip into the system. In concurrency-sensitive environments, the factory can return pre-initialized, thread-safe objects from a pool.

**Example:**
```python
class RideFactory:
    _registry = {}

    @classmethod
    def register(cls, ride_type: str, ride_cls):
        cls._registry[ride_type] = ride_cls

    @classmethod
    def create(cls, ride_type: str, pickup: Location, passenger: User) -> Ride:
        ride_cls = cls._registry.get(ride_type)
        if not ride_cls:
            raise ValueError(f"Unknown ride type: {ride_type}")
        vehicle = VehiclePool.acquire(ride_type, pickup)
        return ride_cls(vehicle=vehicle, passenger=passenger, pickup=pickup)

RideFactory.register("economy", EconomyRide)
RideFactory.register("premium", PremiumRide)
```

## Q9: What is the Dependency Inversion Principle and how does it relate to Spring's IoC container?

**A:** The Dependency Inversion Principle (DIP) states that high-level modules should not depend on low-level modules; both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions. Spring's Inversion of Control (IoC) container is a practical implementation of DIP at the framework level.

In a Spring application, a `OrderService` (high-level) does not instantiate `MySqlOrderRepository` (low-level). Instead, it declares a dependency on the `OrderRepository` interface. Spring's container injects the concrete implementation at runtime, typically via `@Autowired` or constructor injection. This means you can swap `MySqlOrderRepository` for `RedisOrderRepository` by changing a single configuration, without touching `OrderService`.

DIP is essential for testability. In unit tests, you can inject a `MockOrderRepository` that returns predictable data. Without DIP, you would need a running MySQL instance for every test. Senior engineers at FAANG expect you to explain not just the pattern, but the practical consequences: testability, deployability, and the ability to evolve the system independently.

## Q10: Explain the Strategy Pattern and where you would apply it in a social media platform.

**A:** The Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime. The context class holds a reference to a strategy interface and delegates the algorithmic work to it. Clients can change the strategy without modifying the context.

In a social media platform, content ranking is a prime candidate. Different feeds use different ranking strategies: chronological, relevance-based, engagement-weighted, or a machine-learning model. The `FeedRanker` context holds an `IRankingStrategy` reference. At runtime, the strategy can be swapped based on user preferences, A/B test groups, or network conditions (fall back to chronological when ML model is slow).

Another application is content moderation: different regions have different moderation rules. A `ModerationStrategy` interface with implementations for US, EU, and APAC regulations allows the `ContentProcessor` to apply region-specific rules without conditional branches scattered throughout the codebase.

**Example:**
```java
public interface RankingStrategy {
    List<Post> rank(List<Post> candidates, UserProfile user);
}

public class ChronologicalRanker implements RankingStrategy {
    @Override
    public List<Post> rank(List<Post> candidates, UserProfile user) {
        return candidates.stream()
            .sorted(Comparator.comparing(Post::getTimestamp).reversed())
            .collect(Collectors.toList());
    }
}

public class FeedRanker {
    private RankingStrategy strategy;

    public void setStrategy(RankingStrategy strategy) {
        this.strategy = strategy;
    }

    public List<Post> generateFeed(UserProfile user, List<Post> candidates) {
        return strategy.rank(candidates, user);
    }
}
```

## Q11: What is the Observer Pattern and how would you use it in a real-time notification system?

**A:** The Observer Pattern defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically. It promotes loose coupling because the subject knows only the observer interface, not the concrete classes.

In a real-time notification system, a `MessageBroker` (subject) maintains a list of `NotificationListener` objects. When a new message arrives, the broker iterates over registered listeners and calls `onMessage()`. Listeners can be `EmailSender`, `PushNotifier`, `WebSocketBroadcaster`, or `AuditLogger`. Adding a new notification channel means implementing the listener interface and registering it — no changes to the broker.

The follow-up question in interviews is usually about thread safety. If listeners are added or removed while notifications are being dispatched, you need synchronization. Copy-on-write lists or concurrent collections solve this. Also, if one listener throws an exception, it must not prevent other listeners from being notified — each dispatch should be wrapped in a try-catch.

**Example:**
```java
public interface NotificationListener {
    void onMessage(Message message);
}

public class MessageBroker {
    private final List<NotificationListener> listeners = new CopyOnWriteArrayList<>();

    public void subscribe(NotificationListener listener) {
        listeners.add(listener);
    }

    public void publish(Message message) {
        for (NotificationListener listener : listeners) {
            try {
                listener.onMessage(message);
            } catch (Exception e) {
                log.error("Listener failed", e);
            }
        }
    }
}
```

## Q12: How does the Decorator Pattern differ from inheritance, and where would you use it in a streaming system?

**A:** The Decorator Pattern adds behavior to objects dynamically by wrapping them in decorator objects that implement the same interface. Unlike inheritance, which adds behavior at compile time and applies to the entire class, decoration applies at runtime and only to the specific object instance.

In a streaming system (like Netflix), a base `VideoStream` provides raw video data. Decorators add layers: `EncryptedStream` adds decryption, `BufferedStream` adds buffering, `TranscodingStream` adds format conversion. You can stack them: `new TranscodingStream(new BufferedStream(new EncryptedStream(rawStream)))`. Each decorator delegates to the wrapped stream and adds its own logic.

The key advantage: inheritance would require classes like `EncryptedBufferedTranscodedStream` — an explosion of combinations. Decorators compose behavior independently. Each decorator has a single responsibility and can be tested in isolation. This is particularly valuable in production systems where you may need encryption for premium content but not for free content, toggling the decorator based on business rules.

**Example:**
```python
class VideoStream(ABC):
    @abstractmethod
    def read(self) -> bytes: ...

class RawVideoStream(VideoStream):
    def read(self) -> bytes:
        return b"raw video data"

class EncryptedStream(VideoStream):
    def __init__(self, inner: VideoStream, key: bytes):
        self._inner = inner
        self._key = key

    def read(self) -> bytes:
        raw = self._inner.read()
        return aes_encrypt(raw, self._key)

stream = EncryptedStream(RawVideoStream(), key=b"secret123")
data = stream.read()  # reads raw, then encrypts
```

## Q13: What is the Singleton Pattern, and what problems does it introduce in concurrent systems?

**A:** The Singleton Pattern ensures a class has only one instance and provides a global point of access to it. In Java, the simplest implementation is a private constructor and a public static `getInstance()` method. It is commonly used for thread pools, configuration managers, and cache stores.

In concurrent systems, naive singleton implementations introduce race conditions. The double-checked locking idiom (with `volatile` in Java 5+) is one correct approach. Another is the Bill Pugh holder pattern, which leverages class-loading guarantees. A third is using an enum, which the JVM guarantees is a singleton.

The deeper interview point is that singletons are often an anti-pattern. They introduce global state, make unit testing difficult (state leaks between tests), and violate the Single Responsibility Principle. In modern Spring applications, beans are singletons by default within the container, which manages their lifecycle — removing the need for the classic Singleton Pattern. At senior level, you should discuss when a singleton is justified (e.g., a connection pool that truly must be one instance) and when it is a code smell.

**Example:**
```java
public class DatabaseConnectionPool {
    private static class Holder {
        static final DatabaseConnectionPool INSTANCE = new DatabaseConnectionPool();
    }

    public static DatabaseConnectionPool getInstance() {
        return Holder.INSTANCE;
    }

    private DatabaseConnectionPool() {
        // initialize pool
    }
}
```

## Q14: Explain the Template Method Pattern and its trade-offs in a data pipeline system.

**A:** The Template Method Pattern defines the skeleton of an algorithm in a base class, deferring specific steps to subclasses. The base class controls the overall flow (the "template method") while subclasses provide implementations for individual steps. This is a form of the Hollywood Principle: "Don't call us, we'll call you."

In a data pipeline, `ETLPipeline` defines the template: `extract()` → `transform()` → `load()`. Subclasses like `UserSyncPipeline` and `OrderSyncPipeline` override these methods with specific logic. The base class handles error handling, retry logic, metrics collection, and logging around the template method — concerns that would otherwise be duplicated.

The trade-off: Template methods create a rigid algorithmic skeleton. If the steps need to vary in order or some steps need to be optional, the pattern becomes awkward. It also couples subclasses to the base class's implementation (inversion of control can be confusing). Senior engineers prefer composition-based alternatives (like the Strategy or Pipeline pattern with pluggable steps) when flexibility is paramount. However, for frameworks where the algorithm is genuinely fixed (JUnit, Spring MVC's request handling), Template Method is idiomatic and appropriate.

**Example:**
```java
public abstract class ETLPipeline {
    public final void run() {
        List<Record> data = extract();
        List<Record> transformed = transform(data);
        load(transformed);
        logCompletion();
    }

    protected abstract List<Record> extract();
    protected abstract List<Record> transform(List<Record> input);
    protected abstract void load(List<Record> records);

    private void logCompletion() {
        System.out.println("Pipeline completed at " + Instant.now());
    }
}
```

## Q15: What is the Builder Pattern and why is it preferred over telescoping constructors?

**A:** The Builder Pattern separates the construction of a complex object from its representation, allowing the same construction process to create different representations. A telescoping constructor has many overloads with different parameter combinations, which is error-prone and hard to read.

For example, a `Notification` object might have a title, body, priority, recipient list, attachment URL, TTL, and delivery channel. A constructor with 8 parameters is unreadable and every caller must remember the order. A builder makes the construction self-documenting: `new Notification.Builder().title("Alert").priority(HIGH).recipient(user).build()`.

The builder also enables validation at `build()` time, ensuring the object is always in a valid state. In Java, the immutable builder pattern (where the builder is a static inner class) is preferred because it produces immutable objects — critical for thread safety in concurrent systems. Lombok's `@Builder` annotation reduces boilerplate. In interviews, the follow-up is often about how builders relate to the Factory Pattern: factories create different types, while builders create complex instances of a single type.

**Example:**
```java
public class Notification {
    private final String title;
    private final String body;
    private final Priority priority;
    private final List<String> recipients;

    private Notification(Builder builder) {
        this.title = builder.title;
        this.body = builder.body;
        this.priority = builder.priority;
        this.recipients = Collections.unmodifiableList(builder.recipients);
    }

    public static class Builder {
        private String title;
        private String body;
        private Priority priority = Priority.NORMAL;
        private List<String> recipients = new ArrayList<>();

        public Builder title(String t) { this.title = t; return this; }
        public Builder body(String b) { this.body = b; return this; }
        public Builder priority(Priority p) { this.priority = p; return this; }
        public Builder recipient(String r) { this.recipients.add(r); return this; }

        public Notification build() {
            Objects.requireNonNull(title, "title is required");
            return new Notification(this);
        }
    }
}
```

## Q16: How would you design a thread-safe LRU Cache using OOP principles?

**A:** An LRU (Least Recently Used) Cache evicts the oldest-accessed item when capacity is reached. The design uses a doubly-linked list for O(1) access ordering and a HashMap for O(1) key lookup. For thread safety, you wrap the entire operation in a `ReentrantReadWriteLock` or use `ConcurrentHashMap` with careful synchronization around the linked list.

The OOP design involves separating concerns: a `CacheNode` class for linked list nodes, a `DoublyLinkedList` class for access-order management, and an `LRUCache` class that composes both. This separation follows the Single Responsibility Principle — the list manages ordering, the cache manages key-value storage and eviction policy.

In a senior interview, the expected discussion goes beyond data structures. You should address: what happens when multiple threads read the same key simultaneously (read-through with lock), what about write contention during eviction (partitioned locking or striping), and whether you should use `ConcurrentLinkedHashMap` (available in third-party libraries) instead of rolling your own. The right answer depends on read/write ratios and consistency requirements.

**Example:**
```java
public class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, CacheNode<K, V>> map;
    private final DoublyLinkedList<K, V> list;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        this.list = new DoublyLinkedList<>();
    }

    public V get(K key) {
        lock.writeLock().lock();
        try {
            CacheNode<K, V> node = map.get(key);
            if (node == null) return null;
            list.moveToHead(node);
            return node.value;
        } finally {
            lock.writeLock().unlock();
        }
    }

    public void put(K key, V value) {
        lock.writeLock().lock();
        try {
            CacheNode<K, V> existing = map.get(key);
            if (existing != null) {
                existing.value = value;
                list.moveToHead(existing);
                return;
            }
            if (map.size() >= capacity) {
                CacheNode<K, V> tail = list.removeTail();
                map.remove(tail.key);
            }
            CacheNode<K, V> newNode = new CacheNode<>(key, value);
            list.addToHead(newNode);
            map.put(key, newNode);
        } finally {
            lock.writeLock().unlock();
        }
    }
}
```

## Q17: What is the Proxy Pattern and how would you use it in a microservices architecture?

**A:** The Proxy Pattern provides a surrogate or placeholder for another object to control access to it. There are several types: virtual proxies (lazy initialization), protection proxies (access control), caching proxies (result caching), and remote proxies (network communication). In a microservices architecture, the remote proxy is the most relevant.

A `UserServiceProxy` sits between the caller and the remote `UserService` microservice. It handles service discovery, load balancing, retries, circuit breaking, and response caching. The caller interacts with the proxy as if it were a local `UserService` implementation — the network complexity is hidden.

In production, proxies add resilience. If the `UserService` is down, the proxy can return cached user profiles rather than failing. If a request times out, the proxy retries with exponential backoff. This is how libraries like Retrofit (with OkHttp interceptors) and Spring Cloud OpenFeign work — they generate proxies that encapsulate HTTP communication. The interview point is that proxies are not just about access control; in distributed systems, they are the primary mechanism for handling cross-cutting network concerns.

## Q18: Explain the difference between an abstract class and a default method in Java interfaces. When would you use each?

**A:** An abstract class can hold instance state (fields), provide constructors, and have any access modifier. A default method in an interface can only provide a method implementation and cannot hold instance-level state (only static final constants). Since Java 8, default methods allow interfaces to evolve without breaking implementing classes.

Use an abstract class when subclasses need shared mutable state or when you want to enforce a constructor chain — for example, `AbstractEventSource` that initializes a common `EventBus` reference for all subclasses. Use a default method when you need to add behavior to an existing interface without modifying implementors — for example, adding a `stream()` default method to `Collection` in Java 8 without breaking `ArrayList`, `HashSet`, etc.

The critical interview nuance: default methods do not solve the diamond problem perfectly. If a class implements two interfaces that both provide a default method with the same signature, the compiler forces the class to override the method and explicitly choose or combine the behavior. Abstract classes don't have this issue because Java only allows single class inheritance. Senior candidates should discuss the migration strategy: default methods are ideal for interface evolution in library code, while abstract classes are for internal framework hierarchies.

## Q19: What is the Composite Pattern and how would you represent a file system?

**A:** The Composite Pattern lets you compose objects into tree structures and treat individual objects and compositions uniformly. It defines a common interface for both leaf nodes and composite (container) nodes, so client code does not need to distinguish between them.

A file system is a natural tree: files are leaves, directories are composites. Both implement a `FileSystemEntry` interface with a `getSize()` method. A `File` returns its byte size. A `Directory` iterates over its children and sums their sizes. This means `root.getSize()` recursively computes the total size of the entire file system.

In a social media platform, this pattern represents comment threads: a `Comment` is a leaf, a `Thread` is a composite. In an e-commerce system, a `ProductCategory` can contain sub-categories and products. The power of the pattern is that operations applied to the root automatically cascade through the tree. Adding new operation types (like `getPermission()` or `accept(Visitor)`) means adding a method to the common interface — which leads to the Visitor Pattern when operations change frequently but the structure is stable.

**Example:**
```python
from abc import ABC, abstractmethod
from typing import List

class FileSystemEntry(ABC):
    @abstractmethod
    def get_size(self) -> int: ...

class File(FileSystemEntry):
    def __init__(self, name: str, size: int):
        self.name = name
        self._size = size

    def get_size(self) -> int:
        return self._size

class Directory(FileSystemEntry):
    def __init__(self, name: str):
        self.name = name
        self._children: List[FileSystemEntry] = []

    def add(self, entry: FileSystemEntry):
        self._children.append(entry)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)
```

## Q20: How does the Command Pattern decouple request invocation from request handling?

**A:** The Command Pattern encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue requests, and support undoable operations. The key participants are: `Command` (interface with `execute()`), `ConcreteCommand` (implements `execute()` and holds references to receiver objects), `Invoker` (holds and triggers commands), and `Receiver` (the actual object that performs the work).

In an e-commerce system, placing an order involves multiple steps: validate cart, reserve inventory, charge payment, send confirmation. Each step is a `Command` object. The `OrderProcessor` (invoker) holds a list of commands and executes them sequentially. If the payment command fails, previously executed commands can be rolled back by calling their `undo()` methods.

This decoupling is critical for interview systems. You can serialize commands, send them to a message queue, and have worker threads deserialize and execute them later. You can log every command for audit trails. You can implement retry logic at the command level. At senior level, the interviewer expects you to connect the pattern to event sourcing: commands represent intents, events represent outcomes, and the command handler mediates between them.

## Q21: What is an invariant and why is it critical in designing a bank account class?

**A:** An invariant is a condition that must always be true for an object to be in a valid state. In a `BankAccount` class, invariants include: the balance must never be negative (unless overdraft is explicitly allowed), the account must have an owner, and the transaction log must be consistent with the balance. These invariants are the source of truth that all methods must preserve.

Every public method must maintain invariants. `withdraw(amount)` must check `balance >= amount` before deducting. If the check fails, the method should throw an exception and leave the object unchanged — this is the principle of atomic operations. A half-executed withdrawal that debits the balance but fails to record the transaction violates the consistency invariant.

In concurrent systems, invariants become harder to maintain. Two threads might both read a balance of 100 and both attempt to withdraw 80, which would leave the account at -60 if unchecked. Synchronization mechanisms (locks, CAS operations, or database transactions) are needed to enforce invariants under concurrency. Senior interviewers ask about invariants to test whether you think about correctness at the object level, not just at the system level.

## Q22: Explain the concept of a value object versus an entity in DDD and how they differ in Java.

**A:** In Domain-Driven Design, an **entity** has a distinct identity that persists over time, independent of its attribute values. A `Customer` with ID `C-123` remains the same customer even if their name or address changes. An **entity** class implements `equals()` and `hashCode()` based on its identifier.

A **value object** has no conceptual identity — it is defined entirely by its attribute values. Two `Money` objects with amount `100` and currency `USD` are interchangeable. Value objects are immutable, and their `equals()` is based on all fields. Examples: `Money`, `Address`, `DateRange`, `Coordinates`.

In a Java e-commerce system, `Order` is an entity (identified by `orderId`), while `ShippingAddress` is a value object. If two orders ship to the same address, the addresses are equal. The `Order` entity encapsulates value objects: `private ShippingAddress address; private Money total;`. Value objects simplify design because they are inherently thread-safe (immutable) and can be freely shared and compared by value. Entities require careful identity management, especially in ORM frameworks where multiple object instances might represent the same database row.

## Q23: What is the purpose of the Visitor Pattern and when is it preferable to adding methods to a class hierarchy?

**A:** The Visitor Pattern lets you add new operations to existing object structures without modifying those structures. It separates an algorithm from the object structure on which it operates. The structure classes accept a visitor, and the visitor performs the operation.

Use it when you have a stable class hierarchy (like an AST in a compiler or a set of product types in an e-commerce system) but frequently add new operations. Without the Visitor Pattern, adding a `calculateTax()`, `generateReport()`, or `validateCompliance()` method means modifying every class in the hierarchy — violating Open/Closed. With a visitor, you add a new visitor class that implements `TaxVisitor`, `ReportVisitor`, etc., without touching the product classes.

The trade-off: adding a new element type to the hierarchy requires updating every visitor (the "expression problem"). So the Visitor Pattern is ideal when operations change frequently but the structure is stable. In senior interviews, the deeper discussion is about the expression problem itself — the tension between extensibility in types versus extensibility in operations — and how different languages (Java vs. Haskell vs. Clojure) handle it differently.

## Q24: How would you design a connection pool using object-oriented principles?

**A:** A connection pool manages a fixed set of reusable database connections to avoid the overhead of creating and destroying connections per request. The design involves several OOP concepts: a `ConnectionPool` class (Singleton, since there should be one pool per database), a `PooledConnection` wrapper (Proxy pattern, wrapping the real connection and tracking usage), and a `ConnectionFactory` (Factory pattern, for creating new connections when the pool is exhausted).

The `ConnectionPool` maintains a `BlockingQueue<PooledConnection>` for available connections. `acquire()` blocks if the pool is empty and the max size is reached. `release()` returns a connection to the queue after resetting its state. The pool enforces invariants: a connection cannot be acquired twice without being released, connections older than `maxLifetime` are proactively evicted, and idle connections beyond `minIdle` are cleaned up.

In production, health checking is essential. Before handing out a connection, the pool validates it with `SELECT 1`. If validation fails, the connection is discarded and a new one is created. This is how HikariCP, the fastest Java connection pool, works. The interview question tests whether you can combine multiple design patterns (Singleton, Factory, Proxy) into a coherent, production-ready design.

## Q25: What is the difference between covariance and contravariance, and how does it affect type safety in collections?

**A:** Covariance means that if `Sub` is a subtype of `Super`, then `Container<Sub>` is a subtype of `Container<Super>`. In Java, arrays are covariant (`String[]` is a subtype of `Object[]`), but generics are invariant (`List<String>` is NOT a subtype of `List<Object>`). Wildcards enable controlled covariance (`List<? extends Number>`) and contravariance (`List<? super Number>`).

Covariance is "producer" — you can read from a `List<? extends Number>` and get `Number` objects, but you cannot write to it (because the compiler doesn't know the exact type). Contravariance is "consumer" — you can write `Number` objects to a `List<? super Number>`, but reading gives you `Object`. This is the PECS principle: Producer Extends, Consumer Super.

The design implication: if your method only reads from a collection, accept `? extends T`. If it only writes, accept `? super T`. If it does both, accept the exact type. This affects API design in library code significantly. A sorting method should accept `List<? super T>` (it writes elements) while a `max()` method should accept `List<? extends T>` (it only reads). Interviewers ask this to assess whether you think about type safety at the API boundary level.

## Q26: Design a URL shortener service using OOP principles. Walk me through your class design.

**A:** A URL shortener needs a `URLMapping` entity (long URL, short code, creation time, expiry, click count), a `ShortCodeGenerator` (responsible for generating unique, collision-free short codes), a `URLRepository` (persistence layer), and a `URLShortenerService` (orchestrates creation and lookup).

The `ShortCodeGenerator` uses Base62 encoding of a distributed ID (Snowflake or UUID) to produce short codes like `aB3xK9`. It should be injectable so you can swap the generation strategy — for YC startups, a simple counter may suffice; at FAANG scale, you need distributed ID generation to avoid collisions across data centers.

The service layer validates URLs (format, allowlist), checks for duplicates (optional), delegates to the generator, persists the mapping, and returns the short URL. Lookup is a simple cache-then-database read. The `URLMapping` object itself is a value object if you treat two mappings with the same short code as identical, but an entity if you track per-mapping analytics. The follow-up: how do you handle expiry? A scheduled job evicts expired mappings, or you use lazy eviction on read.

## Q27: Explain the Open/Closed Principle with a real example of a discount calculation system.

**A:** The Open/Closed Principle (OCP) states that software entities should be open for extension but closed for modification. In a discount calculation system, you start with a `DiscountCalculator` that applies a flat percentage discount. When the business adds coupon discounts, seasonal sales, loyalty discounts, and bundle discounts, you should not modify the original `DiscountCalculator` class.

Instead, you define a `DiscountStrategy` interface with a `calculate(Order order)` method. Each discount type is a separate class: `FlatPercentDiscount`, `CouponDiscount`, `SeasonalDiscount`, `LoyaltyDiscount`. A `CompositeDiscount` aggregates multiple strategies (e.g., apply the best coupon, then seasonal, then loyalty). Adding a new discount type means creating a new class — no existing code is modified.

The trap that violates OCP: putting discount logic in a giant `if-else` inside `calculateTotal()`. Every new discount type requires editing that method, risking regressions. At senior level, the interviewer expects you to connect this to the real world: OCP is not about never modifying code — it is about the axis of change. If discounts change weekly but the order model is stable, the discount logic should be extensible without touching the stable order model.

**Example:**
```java
public interface DiscountStrategy {
    Money calculate(Order order);
}

public class CouponDiscount implements DiscountStrategy {
    private final String code;
    private final double percentage;

    @Override
    public Money calculate(Order order) {
        if (order.getCouponCode().equals(code)) {
            return order.getSubtotal().multiply(percentage);
        }
        return Money.ZERO;
    }
}

public class CompositeDiscount implements DiscountStrategy {
    private final List<DiscountStrategy> strategies;

    @Override
    public Money calculate(Order order) {
        return strategies.stream()
            .map(s -> s.calculate(order))
            .max(Comparator.comparing(Money::doubleValue))
            .orElse(Money.ZERO);
    }
}
```

## Q28: How would you implement an event-driven system using OOP patterns?

**A:** An event-driven system uses the Observer Pattern at its core, but production systems need more: an `EventBus` (mediator) that decouples event producers from consumers, `Event` objects (immutable value objects carrying payload), `EventHandler` interfaces, and a dispatch mechanism that supports async processing.

The `EventBus` maintains a registry of `EventHandler` instances keyed by event type. When an `OrderPlacedEvent` is published, the bus finds all handlers registered for that event type and invokes them: `InventoryHandler.reserve()`, `NotificationHandler.sendConfirmation()`, `AnalyticsHandler.record()`. Handlers can be synchronous (in-process) or asynchronous (offloaded to a queue like Kafka or RabbitMQ).

The OOP design uses the Strategy Pattern for dispatch (sync vs. async), the Observer Pattern for subscription, and the Mediator Pattern for the bus itself. At senior level, discuss idempotency: if a handler fails and the event is retried, it should not double-reserve inventory. This is achieved by making handlers idempotent via deduplication keys in the event payload. Also discuss ordering guarantees: does `OrderPlaced` always arrive before `OrderShipped`? This requires partitioning by order ID in the message broker.

## Q29: What is the Association, Aggregation, and Composition relationship, and how do you identify them in a social network model?

**A:** **Association** is a generic relationship: a `User` can be associated with a `Post` (the user authors the post). There is no ownership; both can exist independently. **Aggregation** is a "has-a" relationship where the child can exist independently of the parent: a `User` has a `Profile`, but if the user is deleted, the profile data might be retained for audit. **Composition** is a strong "has-a" where the child cannot exist without the parent: a `Post` has `Comments`, and deleting the post deletes all its comments.

In a social network, `User` *aggregates* a `Profile` (profile can be migrated or retained). `Post` *composes* `CommentThread` (comments are meaningless without the post). `User` has an *association* with other `User` objects through the `Friendship` relationship — this is a many-to-many association, typically modeled as a join entity.

The distinction matters for lifecycle management. In Java, composition means the parent manages the child's lifecycle: `Post` creates, stores, and destroys its `CommentThread`. Aggregation means the child is passed in or independently managed: `User` receives a `Profile` object from a profile service. Senior interviewers ask this to test whether you think about object ownership, memory management, and cascading deletes at the design level.

## Q30: Design a rate limiter using the Token Bucket algorithm with OOP principles.

**A:** The Token Bucket algorithm allows bursts up to a bucket capacity while enforcing an average rate. Tokens are added at a fixed rate (e.g., 10/second) up to the bucket capacity. Each request consumes one token. If no tokens are available, the request is rejected or queued.

The OOP design: a `RateLimiter` interface with a `boolean allow()` method. A `TokenBucketLimiter` implementation holds the `capacity`, `tokens` (volatile long), `refillRate`, and `lastRefillTime`. The `allow()` method atomically checks and decrements tokens using `compareAndSet` on an `AtomicLong` for lock-free thread safety.

A `RateLimitFilter` (Decorator or Interceptor pattern) wraps around the request handler. It extracts the client ID, looks up the rate limiter for that client from a `Map<String, RateLimiter>`, and calls `allow()`. If denied, it returns HTTP 429. This design is clean: the rate limiter knows nothing about HTTP, and the filter knows nothing about the algorithm.

**Example:**
```python
import time

class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

## Q31: Explain how you would design a logging framework using OOP concepts.

**A:** A logging framework uses several OOP patterns: the Builder Pattern for configuring loggers, the Decorator Pattern for adding appenders (file, console, network), the Strategy Pattern for log formatting, and the Composite Pattern for chaining appenders.

The core interface is `Appender` with a `void append(LogEvent event)` method. `ConsoleAppender`, `FileAppender`, and `NetworkAppender` implement it. A `CompositeAppender` holds a list of appenders and fans out to all of them — enabling simultaneous console and file logging. `BufferedAppender` decorates another appender, buffering events and flushing periodically for performance.

The `Logger` class holds a reference to the root `Appender`, a log level, and a name. `LoggerFactory.getLogger(Class)` returns a pre-configured logger (Singleton per name). Log events are value objects: immutable, carrying timestamp, level, message, thread name, and exception. This design is essentially how Log4j2 and Logback work — the interview question tests whether you can reverse-engineer a real framework's design from first principles.

## Q32: What is the Flyweight Pattern and where would you use it in a game engine?

**A:** The Flyweight Pattern minimizes memory usage by sharing as much data as possible between similar objects. It separates intrinsic state (shared, immutable) from extrinsic state (unique, context-dependent). Objects with shared intrinsic state are retrieved from a flyweight pool rather than created anew.

In a game engine, thousands of trees on a map might share the same 3D model, texture, and animation data (intrinsic state). Each tree's position, scale, and rotation are unique (extrinsic state). A `TreeFactory` maintains a pool of `TreeType` flyweights keyed by model ID. When rendering, the engine creates `TreeInstance` objects that reference the shared `TreeType` and carry only position data.

Without flyweights, 10,000 trees would load 10,000 copies of the model, consuming gigabytes of GPU memory. With flyweights, all 10,000 share one model. The same pattern applies to character fonts (each glyph is a flyweight, positioned differently), network packet types, and connection metadata. Senior candidates should discuss the trade-off: flyweights increase code complexity and indirection, so they are only worthwhile when you have a very large number of similar objects.

**Example:**
```java
public class TreeType {
    private final String modelId;
    private final Mesh mesh;
    private final Texture texture;

    public TreeType(String modelId, Mesh mesh, Texture texture) {
        this.modelId = modelId;
        this.mesh = mesh;
        this.texture = texture;
    }

    public void render(float x, float y, float rotation) {
        // use intrinsic mesh/texture with extrinsic position
    }
}

public class TreeFactory {
    private static final Map<String, TreeType> pool = new HashMap<>();

    public static TreeType getType(String modelId) {
        return pool.computeIfAbsent(modelId, id -> loadFromDisk(id));
    }
}
```

## Q33: How would you design a chat message queue system using OOP patterns?

**A:** A chat message queue ensures messages are delivered even when recipients are offline. The design involves a `MessageQueue` interface, a `PersistentMessageQueue` implementation backed by a database or Redis, `Message` value objects (immutable, with sender, recipient, content, timestamp, and delivery status), and a `DeliveryService` that polls or pushes messages.

The `MessageQueue` follows the Producer-Consumer pattern. Producers (`ChatServer`) enqueue messages. Consumers (`DeliveryService` instances) dequeue and attempt delivery. If delivery fails (recipient offline), the message stays in the queue with a retry count. After max retries, it moves to a dead-letter queue for manual inspection.

The OOP design uses the Strategy Pattern for storage (in-memory for testing, Redis for production, Kafka for high throughput), the Observer Pattern for notifying the delivery service of new messages, and the Template Method Pattern for the delivery pipeline (validate → encrypt → send → confirm). At senior level, discuss ordering guarantees: messages between two users must be delivered in order, which requires partitioning the queue by user pair.

## Q34: Explain the Chain of Responsibility Pattern in the context of an API request processing pipeline.

**A:** The Chain of Responsibility Pattern passes a request along a chain of handlers. Each handler either processes the request or forwards it to the next handler in the chain. This decouples the sender of the request from its receivers, allowing multiple handlers to handle the request without coupling the sender to any specific receiver.

In an API pipeline, the chain typically includes: `RateLimitHandler` → `AuthenticationHandler` → `AuthorizationHandler` → `ValidationHandler` → `LoggingHandler` → `ControllerHandler`. Each handler is a class implementing a `Handler` interface with a `handle(Request request, Chain chain)` method. If the handler can process the request, it does so and returns. Otherwise, it calls `chain.next(request)` to pass it along.

The key design point: handlers can short-circuit the chain. If `AuthenticationHandler` finds an invalid token, it returns a 401 response immediately — `AuthorizationHandler` and subsequent handlers are never invoked. This is exactly how Servlet Filters, Spring Interceptors, and Express.js middleware work. The interview follow-up: how do you handle async chains? You make `handle()` return `CompletableFuture<Response>` so handlers can perform non-blocking I/O before calling `chain.next()`.

## Q35: What is the Mediator Pattern and how would you apply it to a collaborative editing tool?

**A:** The Mediator Pattern defines an object that encapsulates how a set of objects interact, promoting loose coupling by preventing objects from referring to each other explicitly. Instead, they communicate through the mediator.

In a collaborative editing tool (like Google Docs), multiple `Editor` objects (one per user) need to synchronize. Without a mediator, every editor would need to communicate with every other editor (N-to-N coupling). A `CollaborationMediator` sits in the center: each editor sends changes to the mediator, and the mediator broadcasts them to all other editors.

The mediator handles conflict resolution (two users editing the same paragraph), presence information (who is typing where), undo/redo coordination, and history management. Each editor only knows about the mediator interface, not about other editors. Adding a new editor type (code editor, drawing canvas) means implementing the `Editor` interface and registering with the mediator — no changes to existing editors.

The trade-off: the mediator can become a "god object" if it absorbs too much logic. To prevent this, use sub-mediators for specific concerns (a `SelectionMediator`, a `HistoryMediator`). The Chat SDK pattern used by companies like Twilio and SendGrid is essentially a mediator architecture.

## Q36: How would you design an immutable object in Java and why is immutability important in concurrent systems?

**A:** An immutable object's state cannot be changed after construction. In Java, you create an immutable class by: making the class `final`, making all fields `private final`, having no setter methods, performing deep copies of mutable fields in the constructor, and returning copies from getter methods.

Immutability is critical in concurrent systems because immutable objects are inherently thread-safe. No synchronization is needed to read an immutable object. Multiple threads can share the same immutable instance without data races. This is why `String`, `Integer`, `LocalDate`, and `Instant` are immutable in Java.

In a social media feed, if `Post` objects are immutable, the feed generator, the caching layer, and the rendering engine can all reference the same `Post` instance without coordination. If `Post` were mutable, a concurrent update to the like count could cause a partially-rendered post or a stale cache to serve incorrect data.

The follow-up in interviews: immutability has a cost. Every modification creates a new object, increasing GC pressure. For objects that change frequently (like a mutable game entity), use a copy-on-write strategy or mutable internal state wrapped in an immutable facade. The key is to make the *public API* immutable while optimizing internals.

**Example:**
```java
public final class Money {
    private final long amountInCents;
    private final Currency currency;

    public Money(long amountInCents, Currency currency) {
        this.amountInCents = amountInCents;
        this.currency = currency;
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency))
            throw new CurrencyMismatchException();
        return new Money(this.amountInCents + other.amountInCents, this.currency);
    }

    public long getAmountInCents() { return amountInCents; }
    public Currency getCurrency() { return currency; }
}
```

## Q37: What is the State Pattern and how would you model an order lifecycle?

**A:** The State Pattern allows an object to alter its behavior when its internal state changes. The object appears to change its class. Each state is represented by a separate class, and the context (the order) delegates behavior to the current state object.

An `Order` can be in states: `Created`, `Paid`, `Shipped`, `Delivered`, `Cancelled`. Each state class implements `OrderState` with methods like `pay()`, `ship()`, `deliver()`, `cancel()`. In the `Created` state, `pay()` transitions to `Paid` and `ship()` throws `IllegalStateException`. In the `Shipped` state, `cancel()` is not allowed. The `Order` holds a reference to its current `OrderState` and calls `currentState.pay(this)`, etc.

Without the State Pattern, you would have a giant `switch` statement in every method checking the current status — violating Open/Closed and making the code fragile. With the pattern, adding a new state (e.g., `Refunded`) means creating a new class. The interviewer follow-up: how do you persist state? The state name is stored in the database, and the `Order` reconstructs its state object on load using a `StateFactory`. This maps cleanly to event sourcing where each transition is an event.

**Example:**
```java
public interface OrderState {
    void pay(Order order);
    void ship(Order order);
    void deliver(Order order);
    void cancel(Order order);
}

public class CreatedState implements OrderState {
    @Override
    public void pay(Order order) {
        order.setState(new PaidState());
    }

    @Override
    public void ship(Order order) {
        throw new IllegalStateException("Cannot ship an unpaid order");
    }

    @Override
    public void deliver(Order order) {
        throw new IllegalStateException("Cannot deliver an unpaid order");
    }

    @Override
    public void cancel(Order order) {
        order.setState(new CancelledState());
    }
}
```

## Q38: How do you decide between using a HashMap and a TreeMap in a real application?

**A:** `HashMap` provides O(1) average-case lookup, insertion, and deletion based on `hashCode()`. `TreeMap` provides O(log n) operations but maintains keys in sorted order using a `Red-Black Tree` and the `Comparable` or `Comparator` interface.

Use `HashMap` when you need fast lookups by key and do not care about ordering — for example, a cache mapping user IDs to sessions, or a configuration map mapping property names to values. Use `TreeMap` when you need keys in sorted order — for example, a time-series data store where you need range queries (`subMap(fromTime, toTime)`), or a leaderboard that must return scores in descending order.

In a senior interview, the discussion should cover collision handling in `HashMap` (linked list + tree conversion at threshold, as in Java 8+), the performance impact of poor `hashCode()` implementations, and the `TreeMap`'s advantage for `NavigableMap` operations like `floorKey()`, `ceilingKey()`, and `headMap()`. A production decision might use both: a `HashMap` for primary access and a `TreeMap` for ordered iteration — or a `LinkedHashMap` for insertion-order preservation.

## Q39: Explain the concept of an Object Pool and its implementation considerations.

**A:** An Object Pool pre-instantiates a set of expensive objects and reuses them instead of creating and destroying them on demand. This is critical for objects like database connections, threads, and network sockets where creation overhead is significant.

The pool interface exposes `acquire()` and `release()` methods. `acquire()` returns an available object or blocks until one is available. `release()` returns the object to the pool after resetting its state. The pool manages a `BlockingQueue` of available objects and tracks total instances to enforce maximum size.

Key implementation considerations: **validation** (test objects before handing them out), **eviction** (remove objects that exceed max age or have been idle too long), **monitoring** (expose metrics: active count, idle count, wait time), and **leak detection** (track which thread acquired which object and detect unreleased objects). HikariCP for database connections and Apache Commons Pool for generic object pools are production implementations that handle all of these. The interview point: never implement your own pool in production — use battle-tested libraries, but you should understand the internals to configure them correctly.

## Q40: How would you design a notification preference system that respects user settings across multiple channels?

**A:** The system needs a `NotificationPreference` value object per user (mapping notification types to channel preferences), a `PreferenceRepository` for persistence, and a `NotificationRouter` that checks preferences before dispatching.

The `NotificationRouter` takes a `NotificationEvent` (e.g., `OrderShipped`, `FriendRequest`, `SecurityAlert`) and a `UserId`. It loads the user's preferences, determines which channels are enabled for this event type, and dispatches only to enabled channels. If no channels are enabled, it silently drops the event. If a channel fails, it does not affect other channels (fault isolation).

The OOP design uses the Strategy Pattern for each channel's sending logic and the Composite Pattern for routing to multiple channels. A `ChannelResolver` interface returns available channels for a user. The `DefaultChannelResolver` queries the preference store; a `DebugChannelResolver` returns all channels for testing. The key interview point is handling preference changes in real-time: if a user disables push notifications while a push is in-flight, the system should respect the preference for future messages but may let in-flight messages complete. This is a design trade-off between consistency and performance.

## Q41: What is the Proxy Pattern's role in implementing a caching layer?

**A:** A caching proxy sits between the client and the data source, intercepting requests and returning cached results when available. The proxy implements the same interface as the data source, so the client is unaware of the caching layer.

The `CachingUserRepository` wraps a `UserRepository`. On `findById(id)`, it first checks the in-memory cache (a `ConcurrentHashMap` or Caffeine cache). If found, it returns the cached value. If not, it delegates to the underlying repository, caches the result, and returns it. On `save(user)`, it invalidates the cache entry and delegates to the underlying repository.

Cache invalidation is the hard part. Strategies include time-based expiry (TTL), write-through (update cache and database simultaneously), write-behind (update cache immediately, database asynchronously), and event-based invalidation (subscribe to a change event and invalidate). At senior level, discuss cache stampede: when a popular key expires and 100 threads simultaneously try to recompute it. Solutions include probabilistic early expiration, mutex locking (only one thread recomputes), and stale-while-revalidate.

## Q42: How would you implement a plugin system using OOP principles?

**A:** A plugin system allows extending application functionality without modifying the core codebase. The design uses the Service Provider Interface (SPI) pattern: the core defines a `Plugin` interface, and plugins implement it.

The core application maintains a `PluginManager` that discovers, loads, and initializes plugins. Discovery uses `ServiceLoader` (Java), classpath scanning, or a registry file. Loading uses a separate `ClassLoader` per plugin to isolate dependencies (a plugin's Guava version should not conflict with the core's). Initialization calls `plugin.initialize(context)` where the `context` provides read-only access to core services.

Plugins can extend the application by registering event listeners (Observer), contributing menu items (Composite), or providing new API endpoints (Mediator). The `PluginLifecycle` defines hooks: `onLoad()`, `onEnable()`, `onDisable()`, `onUnload()`. The core never calls plugin code directly — it only invokes the plugin interface. This is how Eclipse (OSGi), Jenkins, and Minecraft (Bukkit) implement their plugin systems. The interview follow-up: security. Plugins run in a sandboxed environment with restricted permissions — no direct filesystem or network access without explicit grants.

## Q43: Explain the difference between an interface and an abstract class from a binary compatibility perspective.

**A:** In Java, when you add a new abstract method to an interface, all existing implementations break — they must add the method. Before Java 8, this was a major backward-compatibility issue. Java 8's default methods solved this: you can add a default method to an interface without breaking implementors. However, abstract classes have always been safe to extend: adding a new abstract method to an abstract class breaks subclasses, but adding a concrete method with a default implementation does not.

From a binary compatibility perspective (relevant for library maintainers at companies like Google and Netflix), interfaces with default methods are almost as flexible as abstract classes. But there are subtle differences: interfaces cannot have instance fields (only static final), so adding state to an interface is impossible. Abstract classes can add fields without breaking subclasses.

The practical advice: if you control both the interface and all implementations (like in a monorepo), either is fine. If you publish an interface as a public API that external teams implement, use default methods liberally to avoid breaking them. This is why Java's `Collection` interface has dozens of default methods (`stream()`, `of()`, `toList()`) added over time without breaking the millions of classes that implement it.

## Q44: How would you design a distributed task scheduler using OOP patterns?

**A:** A distributed task scheduler executes tasks across a cluster of nodes, handling failures, retries, and load balancing. The design involves: a `Task` interface (with `execute()`, `getId()`, `getRetryPolicy()`), a `TaskScheduler` (using the Mediator Pattern to coordinate), a `TaskQueue` (distributed queue like Kafka or Redis Streams), and `WorkerNode` instances that consume from the queue.

The `TaskScheduler` accepts scheduled tasks (using the Command Pattern — each task is a command with a trigger time). It persists tasks to a database and polls for due tasks, adding them to the distributed queue. `WorkerNode` instances compete to dequeue and execute tasks. If a worker crashes mid-execution, the task's lease expires and another worker picks it up.

The OOP design uses the Strategy Pattern for retry policies (exponential backoff, fixed delay, immediate), the Observer Pattern for task lifecycle events (started, completed, failed), and the Decorator Pattern for adding monitoring, timeout enforcement, and deduplication. At senior level, discuss the two-phase commit problem: if a task updates multiple services atomically, how do you ensure consistency? The answer involves saga patterns, compensating transactions, or idempotent task design.

## Q45: What is the difference between a value object and a data transfer object (DTO)?

**A:** A **value object** is a domain concept defined by its attribute values, immutable, with no identity. It enforces business rules: a `Money` object validates that amounts are non-negative, and a `DateRange` ensures start is before end. Value objects belong to the domain layer.

A **DTO** (Data Transfer Object) is a plain data carrier used to transfer data between layers or across network boundaries. DTOs have no business logic — they exist solely to reduce remote calls or serialize data between subsystems. A `UserDTO` might flatten a `User` entity's nested `Address` and `Profile` into a single flat object for API responses.

The distinction: value objects enforce domain invariants and are used within the business logic layer. DTOs are anemic data bags used at the boundaries. A common mistake is using domain value objects as API response objects, which leaks internal domain structure to external consumers. Instead, map from domain objects to DTOs at the API layer (using MapStruct or manual mapping). In interviews, the deeper discussion is about whether DTOs are still necessary with modern frameworks — in many cases, the entity can serve as the DTO for simple CRUD APIs, but separation becomes essential when read and write models diverge (CQRS).

## Q46: How would you design a feature flag system with OOP principles?

**A:** A feature flag system allows toggling features without redeployment. The core components: a `FeatureFlag` entity (key, description, rules, enabled state), a `FlagEvaluationEngine` (determines if a flag is on for a given context), a `FlagStore` (persistence: database, config file, or remote service), and a `FlagContext` (carrying user attributes for targeting rules).

The `FlagEvaluationEngine` uses the Chain of Responsibility Pattern to evaluate rules in order: kill switch (global off) → percentage rollout → user segment targeting → individual user override. Each rule is a `FlagRule` with an `evaluate(FlagContext)` method. The first matching rule determines the flag value.

The OOP design: the `FlagStore` is an interface (Strategy Pattern) with implementations for local files (testing), Redis (production), and LaunchDarkly/Unleash (managed services). The `FlagEvaluationEngine` is decorated with a `CachingEngine` that caches evaluations per user-context to avoid repeated evaluation. At senior level, discuss auditability: every flag evaluation should be logged with the reason (which rule matched) for debugging. This requires each rule to return not just a boolean but an `EvaluationResult` value object containing the decision and the rule name.

## Q47: Explain the Adapter Pattern with an example of integrating multiple payment gateways.

**A:** The Adapter Pattern converts the interface of one class into another interface that clients expect. It lets classes work together that otherwise could not because of incompatible interfaces.

Different payment gateways (Stripe, PayPal, Razorpay) have different APIs, request/response formats, and error handling. A `PaymentGatewayAdapter` wraps each gateway's SDK and presents a unified `PaymentProcessor` interface. The `StripeAdapter` translates `PaymentRequest` to Stripe's format, calls the Stripe SDK, and translates the response back to a `PaymentResult`.

Without adapters, every call site would need gateway-specific logic: `if (stripe) stripeClient.charge(); else if (paypal) paypalClient.execute()`. This violates Open/Closed and scatters gateway-specific knowledge throughout the codebase. With adapters, the `PaymentService` only knows `PaymentProcessor`. Adding a new gateway means creating a new adapter — zero changes to existing code. This is a pragmatic pattern used in every production system that integrates with multiple third-party services.

**Example:**
```java
public interface PaymentProcessor {
    PaymentResult charge(Money amount, PaymentMethod method);
}

public class StripeAdapter implements PaymentProcessor {
    private final StripeClient stripeClient;

    @Override
    public PaymentResult charge(Money amount, PaymentMethod method) {
        StripeChargeRequest req = new StripeChargeRequest(
            amount.getCents(), amount.getCurrency().getCode(),
            method.getStripeToken()
        );
        StripeChargeResponse resp = stripeClient.charges().create(req);
        return new PaymentResult(resp.getId(), resp.getStatus().equals("succeeded"));
    }
}
```

## Q48: What is the Service Locator Pattern and why is dependency injection preferred over it?

**A:** The Service Locator Pattern provides a centralized registry where objects can look up dependencies by name or type. Instead of receiving dependencies through constructors (DI), objects actively query the locator: `ServiceLocator.get(UserRepository.class)`. This is an older pattern used in early Java EE and many legacy frameworks.

The problem: the Service Locator introduces hidden dependencies. A class that calls `ServiceLocator.get()` has a compile-time dependency on the locator itself, and its dependencies are invisible from its constructor signature. You cannot tell what a class needs just by looking at its API — you must read the implementation. This makes testing harder (you must set up the locator with mock implementations) and violates the Explicit Dependencies principle.

Dependency Injection makes dependencies explicit through constructors, setters, or interface parameters. The Spring Framework's inversion of control container is the canonical DI implementation. You can see that `OrderService` depends on `OrderRepository` and `PaymentProcessor` just from its constructor. Testing is trivial: pass mock implementations. The interview point: DI is not just about convenience — it is about making the dependency graph visible and testable. The Service Locator is still useful in specific cases (dynamic service discovery in plugin architectures), but DI should be the default choice.

## Q49: How would you design an idempotent API endpoint for placing orders?

**A:** An idempotent endpoint produces the same result even if called multiple times with the same request. This is critical for reliability: if a network timeout occurs after the order is placed but before the response reaches the client, the client retries, and the server must not create a duplicate order.

The design: the client generates a unique `Idempotency-Key` header (UUID). The server checks a `KeyStore` (Redis or database) before processing. If the key exists, return the cached response. If not, process the order, store the response keyed by the idempotency key with a TTL (e.g., 24 hours), and return the response.

The OOP design: an `IdempotentOrderHandler` decorates the `OrderHandler`. It extracts the key, queries the store, and either returns the cached `OrderResult` or delegates to the inner handler. This is the Decorator Pattern. The `IdempotencyStore` is an interface (Strategy Pattern) with Redis and database implementations. The tricky part is concurrent duplicate requests: use a distributed lock on the idempotency key to ensure only one request processes at a time. The lock is acquired before the store check and released after the store write.

**Example:**
```java
public class IdempotentOrderHandler implements OrderHandler {
    private final OrderHandler delegate;
    private final IdempotencyStore store;
    private final DistributedLock lock;

    @Override
    public OrderResult handle(PlaceOrderRequest request, String idempotencyKey) {
        lock.lock(idempotencyKey);
        try {
            Optional<OrderResult> cached = store.get(idempotencyKey);
            if (cached.isPresent()) return cached.get();

            OrderResult result = delegate.handle(request, idempotencyKey);
            store.put(idempotencyKey, result, Duration.ofHours(24));
            return result;
        } finally {
            lock.unlock(idempotencyKey);
        }
    }
}
```

## Q50: Explain the Memento Pattern and its application in a text editor's undo/redo system.

**A:** The Memento Pattern captures and externalizes an object's internal state so it can be restored later, without violating encapsulation. The originator (text editor) creates mementos (snapshots), the caretaker (undo manager) stores them, and the memento itself is an opaque value object that only the originator can interpret.

A `TextEditor` has a `save()` method returning a `EditorMemento` containing the full document text, cursor position, and selection range. The `UndoManager` (caretaker) maintains a stack of mementos and a pointer for redo. `undo()` pushes the current state onto the redo stack and restores the previous memento. `redo()` does the reverse.

The interview nuance: full-document snapshots are simple but memory-expensive for large documents. Production editors use the Command Pattern instead: each editing action (insert, delete, format) is a command with `execute()` and `undo()`. The undo manager stores a list of inverse commands. This is more memory-efficient but harder to implement correctly (compound actions need grouped commands). The best editors combine both: command-based undo for recent actions, periodic full snapshots for checkpointing. The interviewer expects you to discuss this trade-off and mention that Git's model is fundamentally a memento system (each commit is a snapshot).

**Example:**
```java
public final class EditorMemento {
    private final String text;
    private final int cursorPosition;
    private final Selection selection;

    EditorMemento(String text, int cursorPosition, Selection selection) {
        this.text = text;
        this.cursorPosition = cursorPosition;
        this.selection = selection;
    }

    String getText() { return text; }
    int getCursorPosition() { return cursorPosition; }
    Selection getSelection() { return selection; }
}

## Q51: How would you design a real-time bidding system using OOP concepts while handling concurrency?

**A:** A real-time bidding (RTB) system requires low-latency bid processing with high throughput. The design: a `BidRequest` value object (immutable, containing impression details, user data, floor price), a `BidEvaluator` that scores bids using a pipeline of validators, a `BidResponseBuilder` (Builder Pattern) for constructing responses, and a `BidCache` (ConcurrentHashMap or Caffeine) for tracking active auctions.

Concurrency is the core challenge. Multiple bidders submit bids simultaneously for the same impression. The `AuctionEngine` uses a `ConcurrentHashMap<String, BidState>` keyed by impression ID. Each `BidState` is protected by a `StampedLock` — optimistic reads for checking the current highest bid, pessimistic writes for updating it. This allows thousands of concurrent reads (bid evaluations) with minimal contention on writes (bid updates).

The OOP structure separates concerns cleanly: `BidValidator` (Strategy Pattern) checks budget, targeting, and creative compliance. `BidPricer` calculates the second-price auction price. `BidLogger` (Observer Pattern) records every bid for analytics. At senior level, discuss how to handle auction timeouts: a `ScheduledExecutorService` fires after the auction window closes, finalizes the winner, and sends win/loss notifications. If a late bid arrives after the auction closes, it is rejected by the `BidState`'s status check.

## Q52: What is the Role Object Pattern and how would you apply it to a multi-tenant SaaS platform?

**A:** The Role Object Pattern avoids the combinatorial explosion of permissions by representing user roles as composable objects rather than a single enumerated type. Instead of `Role.ADMIN | Role.EDITOR | Role.COMMENTER` (which requires every combination to be defined), each role is an object with specific permissions, and a user holds a set of role objects.

In a SaaS platform, a `WorkspaceMember` has a collection of `Role` objects: `BillingRole`, `ContentRole`, `AdminRole`, `ViewerRole`. Each role implements a `Permission` interface with methods like `canEditContent()`, `canManageBilling()`, `canInviteMembers()`. The member's effective permissions are the union of all roles.

This enables granular access control: a user might have `ContentRole` in workspace A and `BillingRole` in workspace B. Adding a new permission means adding a method to the `Permission` interface and implementing it in relevant role classes — existing users are unaffected. The interview follow-up: how do you handle role inheritance? `AdminRole` might extend `EditorRole`, inheriting its permissions. This is composition with delegation: `AdminRole` delegates content permissions to an inner `EditorRole` instance. This is cleaner than class inheritance because roles can be mixed dynamically at runtime.

## Q53: How would you design a message deduplication system for an event-driven architecture?

**A:** In event-driven systems, at-least-once delivery guarantees mean events may be delivered multiple times. A deduplication system ensures each event is processed exactly once. The design: a `DeduplicationFilter` that intercepts every incoming event, extracts its unique ID (business key or event UUID), and checks a `DeduplicationStore` (Redis with TTL or a database table).

The `DeduplicationStore` stores event IDs with a TTL matching the maximum possible duplicate window (e.g., 24 hours). When an event arrives, the filter checks: if the ID exists, the event is a duplicate and is dropped. If not, the ID is stored (using `SETNX` for atomicity) and the event is forwarded to the handler.

The OOP design uses the Decorator Pattern: `DeduplicationEventHandler` wraps the actual `EventHandler`. The store is an interface (Strategy Pattern) with Redis and DynamoDB implementations. The critical concurrency detail: two identical events arriving simultaneously must be handled by the `SETNX` (set-if-not-exists) atomic operation in Redis. The first succeeds (returns OK), the second fails (returns already-set) and is dropped. Without atomic operations, you get a race condition where both pass the check and the event is processed twice. At senior level, discuss idempotency beyond deduplication: even with deduplication, handlers should be designed to be idempotent as a defense-in-depth measure.

## Q54: Explain the Thread Object Model in Java and how it relates to OOP design.

**A:** In Java, every thread is an object — either a subclass of `Thread` or an implementation of `Runnable` (a functional interface). The `Thread` object encapsulates the thread's state (name, priority, daemon flag), its execution stack, and its synchronization primitives. The JVM maps `Thread` objects to native OS threads (1:1 model in modern JVMs).

From an OOP design perspective, the question is: should your application code extend `Thread` or implement `Runnable`? The answer is always `Runnable` (or `Callable` for return values). Extending `Thread` couples your task logic to the threading mechanism — you cannot reuse the task in a thread pool, and you cannot extend another class. Implementing `Runnable` separates the task from the execution mechanism, enabling composition: a `TaskExecutor` can accept any `Runnable` and decide how to execute it (thread pool, virtual thread, event loop).

This is Dependency Inversion in action. The high-level `TaskExecutor` depends on the `Runnable` abstraction, not on concrete thread management. Java 21's virtual threads (Project Loom) reinforce this: your code still submits `Runnable` tasks, but the executor runs them on lightweight virtual threads managed by the JVM. The OOP design remains unchanged — only the execution strategy changes. Senior candidates should discuss how this maps to modern reactive systems where the "thread" concept is replaced by event loops and schedulers, but the `Runnable`/`Callable` abstraction persists.

## Q55: How would you design a social media feed generation system using OOP patterns?

**A:** Feed generation involves multiple stages: candidate fetching, ranking, filtering, and assembly. Each stage is a pipeline step, composable via the Pipes and Filters Pattern. The `FeedPipeline` holds a list of `FeedStage` objects, each transforming a list of candidates.

`CandidateFetcher` retrieves potential posts from followed users, groups, and recommendations. `Ranker` scores each candidate using a strategy (chronological, engagement-based, ML model). `Filter` removes blocked content, muted users, and already-seen posts. `Assembler` constructs the final feed response with metadata.

The OOP design uses the Strategy Pattern for ranking strategies (swappable per A/B test), the Decorator Pattern for adding caching or logging to any stage, and the Composite Pattern for combining multiple candidate sources. The `FeedGenerator` composes these stages: `new FeedPipeline(fetcher, ranker, filter, assembler)`.

At senior level, discuss the cold-start problem: new users have no follow graph, so the `CandidateFetcher` falls back to trending content. Discuss read-after-write consistency: if a user just posted, they should see their post at the top of their feed — this requires a write-through cache or a separate "my posts" check. Discuss pagination: feeds are not generated in full but in cursor-based pages, requiring each stage to support limit/cursor semantics.

## Q56: What is the Builder Pattern's role in constructing complex SQL queries, and how does it prevent SQL injection?

**A:** A query builder constructs SQL queries programmatically using method chaining, preventing injection by parameterizing all user inputs. Instead of concatenating strings (`"SELECT * FROM users WHERE name = '" + name + "'"`), a builder uses prepared statements: `query.where("name", name)` which maps to `WHERE name = ?` with the parameter bound safely.

The `Query` class holds a `SELECT` clause, `FROM` table, `JOIN`s, `WHERE` conditions, `GROUP BY`, `HAVING`, and `ORDER BY` — all as structured objects, not raw strings. The `build()` method assembles the SQL string and collects parameters in order. The `execute()` method passes both the SQL and parameters to the JDBC driver.

The OOP design uses the Builder Pattern for the fluent API (`query.select("*").from("users").where("age", ">", 18).orderBy("name")`). Each method returns `this` for chaining. The `WhereClause` objects encapsulate the column, operator, and parameterized value. At senior level, discuss how this pattern underpins every major ORM: JPA's Criteria API, SQLAlchemy's query builder, and Eloquent all use this approach. The key interview point: the builder is not just a convenience — it is a security boundary that prevents injection by construction.

**Example:**
```python
class QueryBuilder:
    def __init__(self):
        self._table = ""
        self._conditions = []
        self._params = []

    def from_table(self, table: str) -> 'QueryBuilder':
        self._table = table
        return self

    def where(self, column: str, op: str, value) -> 'QueryBuilder':
        self._conditions.append(f"{column} {op} %s")
        self._params.append(value)
        return self

    def build(self) -> tuple:
        sql = f"SELECT * FROM {self._table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        return sql, tuple(self._params)

## Q57: How would you design a graceful degradation system for a microservices architecture?

**A:** Graceful degradation means a system continues to operate (with reduced functionality) when dependencies fail, rather than failing completely. The design: each service client is wrapped with a `FallbackStrategy` (Strategy Pattern) that defines what happens when the primary call fails.

For an e-commerce product page, the primary flow aggregates data from 5 services: `ProductService` (name, description), `InventoryService` (stock), `PricingService` (price), `ReviewService` (ratings), and `RecommendationService` (similar products). If `ReviewService` is down, the page shows "Reviews temporarily unavailable" instead of failing entirely. If `RecommendationService` is down, that section is omitted.

The OOP design: each service call is a `ServiceCall<T>` (Command Pattern) with a `execute()` and `fallback()` method. A `DegradationOrchestrator` executes all calls, catching exceptions and invoking fallbacks. The fallback can return cached data, default values, or an empty result. The `CircuitBreaker` (Decorator Pattern) tracks failure rates and short-circuits calls to a failing service (returning fallback immediately without waiting for timeout).

At senior level, discuss the degradation hierarchy: which features degrade first? Recommendations before pricing. Ratings before inventory. The hierarchy is configurable and business-driven. Also discuss monitoring: every fallback invocation is logged and alerted, so the team knows the system is degraded even though it is still serving traffic.

## Q58: What is the Data Mapper Pattern and how does it differ from Active Record?

**A:** The **Data Mapper** separates domain objects from persistence logic. The domain model (`User`) knows nothing about the database. A `UserMapper` (or `UserRepository`) handles all SQL operations, mapping between database rows and domain objects. The domain stays pure; persistence is an infrastructure concern.

The **Active Record** pattern combines domain logic and persistence in the same object. A `User` record has `save()`, `find()`, `delete()`, and `where()` methods directly on the domain class. The object knows how to persist itself: `user.save()` executes an INSERT or UPDATE.

Use Data Mapper when the domain model is complex and you want to keep persistence concerns out of business logic (DDD, Hexagonal Architecture). Use Active Record for simple CRUD applications where the domain maps directly to database tables (Rails, Django). The interview discussion should cover testability: Data Mapper is easier to unit test (mock the repository) while Active Record requires a database connection for most tests. At scale, Data Mapper enables caching strategies, batch operations, and read/write splitting more naturally because the mapper controls all database interactions.

## Q59: How would you design a rate-limited, retryable HTTP client using OOP patterns?

**A:** The client combines the Decorator Pattern (layering concerns), Strategy Pattern (configurable retry/backoff), and Proxy Pattern (transparent to callers).

The base `HttpClient` interface has a `Response execute(Request)` method. `BasicHttpClient` implements it with raw HTTP calls. `RetryDecorator` wraps it, catching `IOException` and retrying with configurable policy. `RateLimitDecorator` wraps that, enforcing a token-bucket rate limit before delegating. `CircuitBreakerDecorator` wraps that, tracking failure rates and short-circuiting when the threshold is exceeded.

The order of decoration matters: `CircuitBreaker(RateLimit(Retry(BasicHttpClient)))`. The circuit breaker checks first — if the circuit is open, fail fast. Then rate limit — if too many requests, queue or reject. Then retry — if the call fails, retry. Then the actual HTTP call.

Each decorator is independently testable. The retry policy is a `RetryStrategy` (Strategy Pattern) — you can inject exponential backoff, fixed delay, or jitter-based backoff without changing the retry decorator. This is how libraries like Resilience4j and Spring Cloud Circuit Breaker are structured. The interview point: discuss how this design supports observability — each decorator can emit metrics (retry count, rate limit rejections, circuit state) independently.

## Q60: Explain the concept of structural typing versus nominal typing and their implications for OOP design.

**A:** **Nominal typing** (used by Java, C#, TypeScript interfaces) matches types by their declared name or interface implementation. Two types are compatible only if one explicitly implements the other. **Structural typing** (used by Go, TypeScript object types, Kotlin data classes) matches types by their structure — if two types have the same fields and methods, they are compatible, regardless of explicit declarations.

In Java, a `UserService` and a `UserFetcher` might both have a `User findById(String id)` method, but they are incompatible unless one implements the other's interface. In Go, both satisfy the `interface { FindById(string) User }` implicitly — no explicit `implements` keyword is needed.

The design implication: nominal typing provides stronger guarantees (you know exactly what an object can do) but requires more boilerplate (explicit interface declarations). Structural typing is more flexible (less boilerplate, easier duck-typing) but can lead to accidental compatibility (two unrelated types that happen to have the same method signature). At senior level, discuss how Java records and sealed interfaces bridge the gap, and how Kotlin's type system supports both paradigms. The interview point: understanding both typing models helps you choose the right language feature for API design — interfaces for strict contracts, structural typing for flexibility.

## Q61: How would you design a multi-level cache system for an e-commerce product catalog?

**A:** A multi-level cache uses L1 (in-process, fast, small) and L2 (distributed, slower, large) caches to minimize latency while maintaining consistency. The product catalog is read-heavy with occasional writes (price updates, inventory changes), making it ideal for this pattern.

The `CatalogCache` composes `L1Cache` (Caffeine in-process, TTL 5 minutes, max 10K entries) and `L2Cache` (Redis, TTL 1 hour, millions of entries). On `get(productId)`: check L1 → if miss, check L2 → if miss, query database → populate both caches. On `put(product)`: update L1, update L2, update database (write-through).

The OOP design uses the Decorator Pattern: `L2CacheDecorator` wraps `L1CacheDecorator` wraps `DatabaseRepository`. Each layer is independent and composable. Cache invalidation uses the Observer Pattern: when a product is updated, an `InvalidationEvent` is published, and both L1 (invalidate local entry) and L2 (delete Redis key) respond.

The hard part is consistency: if L2 is updated but L1 still has stale data, different servers serve different values. Solutions: shorter L1 TTL, broadcast invalidation events across servers (via pub/sub), or accept eventual consistency with a TTL-based convergence guarantee. At senior level, discuss cache warming: preload L2 with popular products at deployment time to avoid cold-start cache misses. Discuss thundering herd protection: use a `LoadingCache` with a single-threaded loader per key to prevent 100 threads from simultaneously querying the database for the same product.

## Q62: What is the Null Object Pattern and how does it improve code safety?

**A:** The Null Object Pattern provides a default "do-nothing" implementation of an interface, replacing null references. Instead of checking `if (user != null) user.getName()`, you provide a `NullUser` that returns empty strings, false for boolean checks, and no-ops for actions.

A `NullNotificationService` silently discards all notifications (useful in testing). A `NullLogger` suppresses all log output (useful in benchmarks). A `NullPaymentProcessor` returns a successful result without charging anything (useful in development). The caller never checks for null — the null object handles everything gracefully.

This pattern eliminates `NullPointerException` risks and removes scattered null-checks that clutter business logic. In a social media platform, a `NullUser` replaces the deleted user in comments: instead of showing "deleted user" or crashing, the system gracefully renders an anonymous placeholder. The null object implements the same interface with sensible defaults.

The interview discussion: null objects can hide bugs if used carelessly (a `NullPaymentProcessor` in production would be catastrophic). They are most appropriate at system boundaries (input validation, external service stubs) and in testing. Also mention that Java's `Optional<T>` is a related but different approach — `Optional` makes the absence explicit in the type system, while Null Object makes absence invisible by providing a valid implementation.

## Q63: How would you design a feature toggling system for a mobile app that works offline?

**A:** A mobile feature toggle system must work offline because devices may not have connectivity. The design: a `FeatureFlagSync` service downloads the latest flag state from the server when online and caches it locally. The `FeatureFlagStore` on the device is a local SQLite table or a serialized JSON file.

When the app starts, it loads flags from the local store (fast, offline-capable). When the device comes online, `FeatureFlagSync` fetches the latest flags from the server and updates the local store. The `FeatureFlagEvaluator` checks the local store to determine if a feature is enabled.

The OOP design: the `FeatureFlagStore` is an interface (Strategy Pattern) with `LocalStore` (SQLite) and `RemoteStore` (API client) implementations. A `CompositeFlagStore` tries local first and falls back to remote. The `SyncManager` (Observer Pattern) listens for connectivity events and triggers synchronization. The `FlagEvaluator` uses the Builder Pattern to construct evaluation contexts from the local device state (app version, user segment, A/B test assignments).

At senior level, discuss conflict resolution: what happens if the server says "feature X is off" but the local store says "on"? The answer depends on the feature: kill switches (security-related) always use the server value; cosmetic features can use the cached value. Discuss stale flags: the local store should store a `lastUpdated` timestamp and flag stale entries, falling back to defaults if the data is too old.

## Q64: Explain the Interceptor Pattern and its use in authentication and authorization.

**A:** The Interceptor Pattern intercepts requests before they reach the handler, allowing cross-cutting logic to be applied uniformly. Interceptors are similar to the Chain of Responsibility but are typically registered globally and applied to all matching requests.

In a Spring Boot application, `HandlerInterceptor` implementations handle pre-processing (`preHandle`), post-processing (`afterCompletion`), and view rendering. An `AuthenticationInterceptor` checks for a valid JWT token in the request header. An `AuthorizationInterceptor` verifies the user's roles against the endpoint's required permissions. A `RateLimitInterceptor` checks client quotas.

The OOP design: interceptors are registered in a global pipeline. Each interceptor is independent and focuses on one concern. The order of registration determines execution order (authentication before authorization). Interceptors can short-circuit the pipeline by returning `false` from `preHandle()`, preventing the request from reaching the controller.

This is how Servlet Filters, Struts Interceptors, and gRPC Interceptors work. The interview point: interceptors are preferred over AOP (Aspect-Oriented Programming) for request-level concerns because they have access to the HTTP context, are easier to test, and their execution order is explicit. AOP is better for cross-cutting concerns that span multiple layers (logging at the service and repository layer).

## Q65: How would you design a distributed configuration system with hot reloading?

**A:** A distributed configuration system manages application settings across multiple services and instances with the ability to update configuration without restarts. The design: a `ConfigSource` interface (Strategy Pattern) with implementations for file-based, database-based, and remote configuration servers (like Spring Cloud Config, Consul, or etcd).

The `ConfigManager` holds the current configuration as an immutable `Config` object. When a change event arrives (via the Observer Pattern — `ConfigChangeListener`), the `ConfigManager` atomically swaps the configuration reference. All threads reading the config get the new version on their next read (no locks needed because `Config` is immutable).

The OOP design uses the Observer Pattern for change notification: services register `ConfigChangeListener` instances that react to changes (clear caches, refresh connection pools, restart background tasks). The `Config` value object is immutable — changes create a new instance, ensuring thread safety. The `ConfigManager` uses the Singleton Pattern (one per application) but is testable because `ConfigSource` is injectable.

At senior level, discuss failure modes: what if the config server is unavailable? The system uses the last-known configuration (immutable, so it is still valid). Discuss backward compatibility: new configuration keys should have defaults. Discuss auditing: every configuration change should be logged with who changed it, when, and what the previous value was.

## Q66: What is the Visitor Pattern's relationship to the Expression Problem?

**A:** The Expression Problem is the challenge of extending a data type with new variants (types) and new operations simultaneously, without modifying existing code. In Java (a nominal-typed language), adding a new operation to a class hierarchy means modifying every class (or using the Visitor Pattern to avoid that, at the cost of making new types hard to add).

The Visitor Pattern solves the "add new operations" side of the expression problem. If you have `Number`, `Add`, `Multiply` expression types and want to add `evaluate()`, `print()`, and `optimize()` operations, each is a visitor class. Adding `toBytecode()` means adding a new visitor — no existing classes change.

But adding a new expression type (like `Divide`) requires updating every visitor to handle it. This is the other side of the expression problem. Languages like Haskell solve this with type classes (open for extension in both dimensions). Scala's pattern matching and sealed traits offer a middle ground. In Java, the expression problem is typically solved by choosing the axis of change that changes most frequently: if new operations are added more often than new types, use Visitor; if new types are added more often, use polymorphic methods on the types.

At senior level, you should be able to discuss this trade-off clearly and explain why there is no perfect solution in statically-typed languages — it is a fundamental design tension.

## Q67: How would you design an audit logging system that captures entity changes without modifying domain classes?

**A:** An audit logging system records who changed what, when, and the before/after values. The design uses the Intercepting Filter Pattern or AOP to capture changes without modifying domain classes.

The `AuditInterceptor` (Decorator Pattern) wraps the repository layer. Before `save()`, it snapshots the entity's current state. After `save()`, it compares the before and after states and creates an `AuditEntry` value object containing the entity type, entity ID, field changes, the user who made the change, and the timestamp.

The `AuditEntry` is stored in an `AuditLog` (append-only table or event stream). The `AuditLogRepository` handles persistence. The `ChangeDetector` utility uses reflection or entity metadata to compare two versions of an entity and produce a list of `FieldChange` objects (field name, old value, new value).

The OOP design: the `AuditInterceptor` is injected into the repository via the Decorator Pattern. It delegates to the inner repository after capturing the snapshot. The `ChangeDetector` is a utility class (no state, static methods or a Strategy for custom comparison logic). The `AuditEntry` is an immutable value object. At senior level, discuss handling of sensitive fields (passwords, credit card numbers should be masked in audit logs), the performance impact of snapshotting (use async audit logging via an event queue), and compliance requirements (GDPR, SOC2 may require audit logs to be tamper-proof — use immutable storage or blockchain-like hash chaining).

## Q68: Explain the difference between implicit and explicit coupling in a microservices architecture.

**A:** **Implicit coupling** occurs when services are coupled through shared databases, shared libraries with version locks, synchronous REST calls, or shared configuration. It is dangerous because the coupling is invisible — developers do not realize the dependency exists until a change breaks another service. **Explicit coupling** is declared and visible: message contracts in a schema registry, API versioning with deprecation policies, and event-driven communication with well-defined schemas.

In a microservices e-commerce system, implicit coupling might look like: `OrderService` directly queries the `ProductService`'s database to check inventory. This creates a hidden dependency — schema changes in the product database break the order service without any compile-time error. Explicit coupling replaces this with an `InventoryCheckRequest` message over a message broker, with a schema defined in a registry (Avro, Protobuf).

The OOP perspective: implicit coupling violates Dependency Inversion at the architectural level. High-level services depend on low-level implementation details (database schemas). Explicit coupling enforces abstraction boundaries — services communicate through interfaces (APIs, events), not implementations. At senior level, discuss how to detect implicit coupling: audit inter-service database access, track shared library versions across services, and monitor for synchronous calls that should be async.

## Q69: How would you design an entity versioning system for a collaborative document editor?

**A:** Entity versioning in a collaborative editor requires capturing every change and enabling rollback, branching, and conflict resolution. The design: each `Document` entity has a version chain — a linked list of `DocumentVersion` value objects, each containing the full document state (or a delta for efficiency).

The `VersionManager` handles version creation on every save, version retrieval, and rollback. When a user edits the document, the `EditCommand` (Command Pattern) is executed and a new `DocumentVersion` is created, linking to the previous version. The version chain forms a DAG (directed acyclic graph) when multiple users edit simultaneously, enabling branch detection.

The OOP design uses the Memento Pattern for version snapshots, the Command Pattern for individual edits (each edit is a command with `execute()` and `undo()`), and the Composite Pattern for grouped operations (typing multiple characters is one compound command). A `ConflictResolver` (Strategy Pattern) handles simultaneous edits: last-write-wins, operational transform (OT), or CRDT-based merging.

At senior level, discuss storage trade-offs: full snapshots are simple but wasteful; deltas are compact but expensive to reconstruct; periodic checkpoints with delta chains provide a balance. Discuss garbage collection: old versions beyond a retention policy are pruned, but only if no branch references them. Discuss how Git's model (snapshot + delta compression) applies to document versioning.

## Q70: What is the Ambassador Pattern and how would you use it in a service mesh?

**A:** The Ambassador Pattern is a structural pattern where a helper object (the ambassador) handles cross-cutting concerns for a service, acting as a proxy that handles networking, monitoring, and security. It is closely related to the Proxy Pattern but specifically targets offloading infrastructure concerns.

In a service mesh (like Istio or Linkerd), sidecar proxies (Envoy) act as ambassadors. Each service instance has a sidecar that handles service discovery, load balancing, retries, circuit breaking, mutual TLS, and observability. The application code communicates with `localhost`, and the ambassador handles all outbound network complexity.

The OOP design: an `Ambassador` class implements the same interface as the remote service but delegates actual network calls to a `TransportClient`. The ambassador adds retry logic, timeout enforcement, metrics collection, and health checking. The application only interacts with the ambassador, never directly with the network.

At senior level, discuss the difference between application-level ambassadors (in-process decorators) and infrastructure-level ambassadors (sidecar proxies). Application-level ambassadors give more control but couple the application to the pattern. Infrastructure-level ambassadors (sidecars) are transparent to the application but add latency (extra network hop). The interview discussion should show awareness of both approaches and when to use each.

## Q71: How would you design a product recommendation engine using OOP patterns?

**A:** The recommendation engine aggregates multiple recommendation strategies: collaborative filtering ("users who bought X also bought Y"), content-based filtering ("similar to items you viewed"), trending items, and personalized ads. Each strategy is a `RecommendationStrategy` (Strategy Pattern) that takes a `UserContext` and returns a list of `Recommendation` objects.

The `RecommendationAggregator` combines results from multiple strategies, deduplicates, and ranks them. Each strategy produces recommendations with a confidence score. The aggregator applies business rules (diversity — don't show 10 electronics items; freshness — boost new products; inventory — hide out-of-stock items) and returns the final ranked list.

The OOP design: `CollaborativeFilterStrategy` queries a user-item interaction matrix. `ContentBasedStrategy` uses product embeddings (vector similarity). `TrendingStrategy` queries a time-windowed aggregation. Each strategy is independently testable and deployable. A `RecommendationPipeline` (Composite Pattern) orchestrates them. The `RecommendationCache` (Decorator Pattern) caches results per user for a configurable TTL.

At senior level, discuss A/B testing: different users receive recommendations from different pipeline configurations. The `ABTestRouter` (Strategy Pattern) assigns users to experiments and selects the pipeline variant. Discuss feedback loops: user clicks on recommendations are recorded and fed back to improve the strategies — but beware of popularity bias (items shown more often get more clicks, reinforcing their ranking).

## Q72: What is the concept of "Tell, Don't Ask" in OOP and how does it relate to the Law of Demeter?

**A:** "Tell, Don't Ask" means you should tell objects what to do rather than asking them for data and making decisions yourself. Instead of `if (user.getOrders().size() > 0) { user.getOrders().get(0).getStatus(); }`, you tell the user: `user.hasActiveOrders()` or `user.getPrimaryOrderStatus()`.

The Law of Demeter (Principle of Least Knowledge) states: only talk to your immediate friends. Don't call methods on objects returned by other methods. This means `order.getCustomer().getAddress().getCity()` violates the principle — the order should not reach through the customer to the address to the city.

The relationship: both principles push toward encapsulation and behavior-rich domain objects. If you "tell" the `Order` to calculate shipping, the `Order` internally accesses its `Address` — that is fine because `Address` is the order's immediate friend. But the caller should not reach through the order to ask the address for the city.

In a senior interview, demonstrate with a real example: instead of a `PriceCalculator` that asks `Product.getCategory().getTaxRate()`, make `Product.calculateTax(Money amount)` — the product knows its category and delegates internally. This makes the `PriceCalculator` simpler and the tax logic encapsulated where it belongs.

## Q73: How would you design a webhook delivery system with guaranteed delivery?

**A:** A webhook system sends HTTP callbacks to external URLs when events occur (e.g., `ORDER_PLACED` fires a POST to the merchant's endpoint). Guaranteed delivery means every event is delivered at least once, even if the target is temporarily down.

The design: an `EventStore` persists all events. A `WebhookDispatcher` polls due events and attempts delivery. Each delivery attempt is a `DeliveryAttempt` value object (timestamp, HTTP status, response body, duration). If the target returns 5xx or is unreachable, the event is retried with exponential backoff (1s, 5s, 30s, 5min, 1hr). After max retries, the event moves to a dead-letter queue.

The OOP design: a `WebhookSubscription` entity (URL, event types, secret for HMAC signing, active flag). A `DeliveryService` (Mediator Pattern) coordinates: load subscription → sign payload → send HTTP request → record attempt → schedule retry or confirm delivery. The `RetryPolicy` is a Strategy with configurable backoff. The `DeliveryVerifier` generates HMAC signatures so the receiver can verify authenticity.

At senior level, discuss idempotency: the receiver may get duplicates, so the payload includes a unique `event_id` for deduplication. Discuss ordering: events for the same entity should be delivered in order, requiring per-entity queue partitioning. Discuss scaling: the dispatcher runs as multiple workers processing a partitioned queue (Kafka consumer group), ensuring horizontal scalability.

## Q74: What is the lifecycle of a JPA entity and how do its states relate to OOP encapsulation?

**A:** A JPA entity transitions through states: **New (Transient)** → **Managed** → **Removed** → **Detached**. A new object (`new User()`) is transient — not associated with any persistence context. After `persist()`, it becomes managed — the persistence context tracks changes and will flush them to the database. After `remove()`, it is marked for deletion. After the persistence context closes or `detach()` is called, it becomes detached — changes are no longer tracked.

This lifecycle has OOP implications. Managed entities are proxies — JPA generates a subclass at runtime. Calling `user.getOrders()` on a managed entity triggers lazy loading, which is transparent but introduces performance concerns (N+1 queries). Detached entities lose lazy-loading capabilities — accessing unloaded collections throws `LazyInitializationException`.

The encapsulation challenge: JPA entities should be anemic POJOs (private fields, getters/setters) for ORM compatibility, but rich domain models (behavior on entities) are preferred in DDD. The compromise: entities have minimal behavior for persistence (equals, hashCode, business rules for state transitions) while services handle orchestration logic. At senior level, discuss why Lombok's `@Data` on JPA entities is problematic (it generates `equals`/`hashCode` using all fields, which breaks when lazy-loaded collections are null in detached state).

## Q75: How would you design a metrics collection system that supports custom dimensions without modifying the core library?

**A:** A metrics system collects numerical measurements (latency, error count, throughput) with key-value dimensions (endpoint, status code, region). The design must allow teams to add custom dimensions without modifying the metrics library code.

The `MetricRegistry` (Singleton) holds all registered metrics. A `Metric` has a name, a type (counter, gauge, histogram), and a `TagSet` (immutable map of dimensions). `counter("http_requests", "method", "GET", "status", "200")` creates or retrieves a counter with those dimensions.

The OOP design: the `Metric` interface has a `record(double value)` method. Implementations: `CounterMetric`, `GaugeMetric`, `HistogramMetric`. The `TagSet` is a value object — it implements `equals`/`hashCode` based on all tags, so two metrics with different tags are distinct instances stored in a `ConcurrentHashMap<TagSet, Metric>`. The `MetricPublisher` interface (Strategy Pattern) sends metrics to different backends: Prometheus, Datadog, CloudWatch.

The key interview point: adding a custom dimension means passing additional tags to the counter/gauge call — no library modification needed. The library is open for extension (new dimensions) without modification. This is OCP applied to the API surface. At senior level, discuss cardinality explosion: unlimited custom dimensions can create millions of unique time series, overwhelming the monitoring backend. The solution is dimension whitelisting and cardinality limits at the metrics library level.

## Q76: You are interviewing at Meta. The interviewer asks: "Design the backend object model for Facebook Messenger." Walk through your class design decisions.

**A:** The core entities are `User`, `Conversation`, `Message`, `Thread`, and `Attachment`. A `User` has an ID, display name, profile picture, and online status. A `Conversation` can be 1:1 or group. A `Message` belongs to a conversation, has a sender, content, timestamp, read receipts, and reactions. `Thread` represents a topic thread within a group conversation (Facebook supports this). `Attachment` is a value object representing images, videos, files, or audio.

The relationships: `Conversation` composes `Message` objects (messages cannot exist without a conversation — composition). `Conversation` aggregates `User` participants (users exist independently — aggregation). `Message` associates with `User` (sender). `Message` may contain `Attachment` value objects.

For the 1:1 vs. group distinction, use polymorphism: `Conversation` is the base class, `DirectConversation` and `GroupConversation` are subtypes. A group conversation has an admin list and a name. A direct conversation is identified by the pair of user IDs (no separate ID needed — use a deterministic key like `sorted(user1, user2)`).

For concurrency: `Message` is immutable after creation (value semantics for the message content). Read receipts use an `AtomicInteger` or a separate `ReadState` entity per user per conversation. Typing indicators are ephemeral (not persisted, broadcast via WebSocket). The interviewer expects you to discuss scalability: conversations are sharded by conversation ID, messages are stored in time-ordered tables with cursor-based pagination, and media attachments are stored in object storage (S3) with CDN distribution.

## Q77: You are at Amazon. The interviewer asks: "How would you model an order management system that handles millions of orders per day?" Discuss the OOP design.

**A:** The core entities: `Order`, `OrderItem`, `OrderStatus`, `Payment`, `Shipment`, `Address`, and `Money` (value object). An `Order` has a unique ID, a `CustomerId`, a list of `OrderItem` objects (composition — items belong to the order), a `ShippingAddress` (value object), a `Payment` reference, and a `Status` (state machine).

The `OrderStatus` uses the State Pattern: `Placed`, `Confirmed`, `Processing`, `Shipped`, `Delivered`, `Cancelled`, `Returned`. Each state defines valid transitions and behavior. For example, `ShippedState.deliver(order)` transitions to `DeliveredState` and triggers a delivery notification. `PlacedState.cancel(order)` transitions to `CancelledState` and triggers a refund.

For handling millions of orders: the `Order` entity is the aggregate root — all operations go through it, ensuring invariants (e.g., you cannot ship an unpaid order). The `OrderRepository` interface abstracts persistence (Data Mapper Pattern), with implementations for MySQL (transactional), DynamoDB (high throughput), and a read-replica for queries.

The interviewer follow-up: "What happens during peak events like Prime Day?" The design uses the Command Pattern for order placement: `PlaceOrderCommand` is sent to a Kafka queue, processed by workers that validate, charge, and confirm. This decouples the API (which returns "order received") from the processing (which may take seconds). Circuit breakers protect downstream services. The `OrderEvent` (Event Sourcing) log provides an audit trail and enables replay for debugging.

## Q78: You are at Google. The interviewer asks: "Design the object model for Google Maps routing engine." How do you approach this?

**A:** The core entities: `MapGraph` (the road network), `Node` (intersection or waypoint with latitude/longitude), `Edge` (road segment with distance, speed limit, road type, and real-time traffic), `Route` (a sequence of edges from origin to destination), and `RouteSegment` (a leg of the journey with turn-by-turn instructions).

The `MapGraph` is an adjacency list representation: each `Node` holds a list of `Edge` objects. For routing, the `RoutingEngine` implements Dijkstra's or A* algorithm with the `Edge` weight being travel time (distance / speed with traffic factor). The `Route` is an immutable value object containing the list of segments, total distance, and estimated time.

The OOP design: `Edge` is polymorphic — `HighwayEdge`, `CityStreetEdge`, `PedestrianEdge`, `TransitEdge` each have different weight calculation strategies. A `TrafficStrategy` interface computes real-time speed based on traffic data: `LiveTrafficStrategy` uses real-time feeds, `HistoricalTrafficStrategy` uses time-of-day averages, `OfflineStrategy` uses static speed limits.

At senior level, discuss caching: popular routes (home to work) are cached. The `RouteCache` is an LRU cache keyed by origin-destination pair. Discuss map updates: road construction changes `Edge` properties; the `MapUpdateService` uses the Observer Pattern to notify the routing engine of graph changes. Discuss hierarchical routing: for long distances, use highway-level routing first, then drill down to local streets — this is a multi-level graph approach that drastically reduces search space.

## Q79: You are at Netflix. The interviewer asks: "How would you design the video streaming session object model?" Discuss concurrency and failure handling.

**A:** The core entities: `StreamSession` (stateful, per-viewer), `VideoContent` (metadata, manifest URLs), `PlaybackProfile` (device capabilities, bitrate limits), and `AdBreak` (mid-roll ad positions). A `StreamSession` is created when a user presses play and tracks the current playback position, buffered segments, quality level, and ABR (Adaptive Bitrate) state.

Concurrency: `StreamSession` is a stateful object accessed by the playback thread (updating position), the network thread (buffering segments), and the analytics thread (reporting metrics). Use `ReentrantReadWriteLock`: the playback position is updated with a write lock, analytics reads with a read lock. The ABR algorithm reads buffer level and network throughput (read) and updates quality level (write).

Failure handling: the `StreamSession` has a `RecoveryStrategy` (Strategy Pattern). On network drop, the session falls back to a lower bitrate (graceful degradation). On extended failure, it transitions to a `Reconnected` state and resumes from the last confirmed position. The session heartbeats to the server every 30 seconds; if three heartbeats fail, the session is marked abandoned and resources (CDN slots) are released.

The OOP design: the `PlaybackEngine` is a state machine with states: `Buffering`, `Playing`, `Paused`, `Seeking`, `Error`, `Completed`. Each state handles events differently: `BufferingState` ignores play commands; `PlayingState` handles pause and seek. The `ABRController` (Observer Pattern) monitors buffer health and network conditions, adjusting quality dynamically. At senior level, discuss DRM: the `DecryptionKeyManager` fetches license keys per content and manages key rotation during playback.

## Q80: You are at Tesla. The interviewer asks: "How would you model the autopilot object detection pipeline using OOP?" Discuss real-time constraints.

**A:** The pipeline: `CameraSensor` → `Preprocessor` → `DetectionModel` → `Tracker` → `Planner` → `ActuatorController`. Each stage is a processing node in a pipeline, communicating through typed message queues (intra-process) or shared memory (for latency-critical paths).

The `DetectionPipeline` (Mediator Pattern) orchestrates the flow. `CameraSensor` produces raw frames at 30 FPS. `Preprocessor` normalizes, resizes, and crops frames. `DetectionModel` runs inference (YOLO or similar) and produces `Detection` objects (bounding box, class, confidence). `Tracker` (multi-object tracker like DeepSORT) associates detections across frames, producing `TrackedObject` entities with velocity and trajectory.

The OOP design: `DetectionModel` is an interface (Strategy Pattern) — different models for different hardware: `TegraDetectionModel` for车载 hardware, `GPUTrappedModel` for simulation. The `Tracker` uses the Observer Pattern to notify the `Planner` when new tracked objects appear or existing ones change trajectory. The `Planner` (command pattern) produces `DrivingCommand` objects: steer angle, acceleration, braking.

Real-time constraints: the entire pipeline must complete within 33ms (for 30 FPS). The `PipelineProfiler` (Decorator Pattern) wraps each stage and measures execution time. If any stage exceeds its budget, the `SafetyMonitor` (Observer) triggers a fallback: reduce resolution, skip frames, or hand control back to the driver. At senior level, discuss redundancy: two independent pipelines run on separate hardware, and their outputs are compared. If they diverge, the system disengages autopilot — this is fail-safe design.

## Q81: You are at Samsung. The interviewer asks: "Design the object model for a smart home IoT hub managing 50+ devices." Discuss protocol abstraction.

**A:** The core entities: `IoTDevice` (abstract), `DeviceRegistry`, `CommandDispatcher`, `ProtocolAdapter`, and `AutomationRule`. Each device type (`LightBulb`, `Thermostat`, `Camera`, `Lock`) extends `IoTDevice` with device-specific methods. The `DeviceRegistry` maps device IDs to their instances (Composite Pattern — devices can be grouped into rooms, which are themselves composable).

The protocol abstraction is critical: devices use different protocols (Zigbee, Z-Wave, WiFi, Bluetooth, Matter). A `ProtocolAdapter` interface defines `connect()`, `send(Command)`, `subscribe(Event)`. `ZigbeeAdapter`, `ZigbeeAdapter`, `WiFiAdapter` implement it. The `CommandDispatcher` translates high-level commands (`turnOn(deviceId)`) into protocol-specific messages.

The OOP design: `IoTDevice` holds a `ProtocolAdapter` reference (injected at registration time). `LightBulb.turnOn()` calls `adapter.send(new ZigbeeOnCommand(address))`. The caller never knows the protocol. Adding a new protocol means implementing `ProtocolAdapter` — zero changes to device classes.

For 50+ devices: the `EventBus` (Observer Pattern) uses a concurrent dispatch mechanism. When a motion sensor triggers, it publishes a `MotionDetectedEvent`, and all registered `AutomationRule` objects evaluate their conditions. Rules use the Chain of Responsibility: if `condition.evaluate(context)` is true, `action.execute(context)` runs. At senior level, discuss offline operation: the hub must continue executing local automations even without internet — rules are cached locally and evaluated by the hub's event loop. Discuss device heartbeat monitoring: devices that miss heartbeats are marked offline and their last-known state is preserved.

## Q82: How would you design a resilient message broker client that handles partition leadership changes?

**A:** In Kafka, partitions have leaders that can change during rebalancing. A resilient client must handle `NOT_LEADER_FOR_PARTITION` errors transparently. The design: a `BrokerClient` that maintains a metadata cache mapping partitions to their current leaders, a `PartitionRouter` that selects the correct broker for each partition, and a `MetadataRefresher` that periodically updates the cache.

The OOP design: `PartitionRouter` uses the Strategy Pattern — `RoundRobinRouter`, `StickyRouter`, or `LeastLoadedRouter` for load distribution. On receiving `NOT_LEADER_FOR_PARTITION`, the `BrokerClient` invalidates the metadata for that partition, refreshes metadata from the controller broker, and retries on the new leader. This is the Decorator Pattern: `ResilientBrokerClient` wraps `BasicBrokerClient` and adds retry, metadata refresh, and error handling.

The `MetadataCache` is a `ConcurrentHashMap` updated atomically — reads during refresh see either old or new metadata, never partial state. The `MetadataRefresher` runs on a `ScheduledExecutorService` at a configurable interval (default 30 seconds). On error events (disconnection, leadership change), it triggers an immediate refresh.

At senior level, discuss consumer group rebalancing: when a consumer joins or leaves, partitions are reassigned. The `ConsumerRebalanceListener` (Observer Pattern) notifies the application to commit offsets and release partition-local resources. Discuss exactly-once semantics: the client uses idempotent producers (sequence numbers) and transactional consumers (offset commit in the same transaction as processing).

## Q83: How would you design a scalable pricing engine for an airline ticket booking system?

**A:** Airline pricing is dynamic: it changes based on demand, time to departure, season, competitor prices, and customer segment. The `PricingEngine` composes multiple `PriceFactor` strategies: `DemandBasedFactor`, `TimeToDepartureFactor`, `SeasonalFactor`, `CompetitorFactor`, and `LoyaltyFactor`. Each factor adjusts the base fare by a multiplier.

The `PriceCalculator` (Composite Pattern) aggregates all factors: `fare = baseFare * factor1.multiplier * factor2.multiplier * ...`. The order and interaction of factors are configurable. A `PricingRule` (Strategy Pattern) defines how factors combine: some are multiplicative, some additive, some override.

The OOP design: `PriceFactor` is an interface with `double multiplier(PricingContext context)`. `PricingContext` is a value object containing origin, destination, date, cabin class, booking channel, and customer segment. The `PricingEngine` loads factors from a `PricingConfiguration` (hot-reloadable via the Observer Pattern — when rules change in the admin console, the engine picks them up without restart).

At senior level, discuss A/B testing: different users see different prices (within ethical and legal bounds). The `ABTestPricingEngine` routes requests to different factor configurations based on user segments. Discuss race conditions: two users booking the last seat simultaneously must not both see availability — the `InventoryService` uses optimistic locking (`version` field) or pessimistic locking (`SELECT FOR UPDATE`). Discuss caching: prices are cacheable for short periods (1-5 minutes) but must be invalidated on inventory changes.

## Q84: You are asked to explain to a junior engineer why we prefer composition over inheritance. Give a real-world example that demonstrates the failure of deep inheritance.

**A:** Consider an `Employee` hierarchy: `Employee` → `SalariedEmployee` → `Manager` → `Director` → `VP`. At first, inheritance makes sense: managers are employees with extra responsibilities. But then: a `Director` needs to approve budgets (behavior), a `VP` needs to attend board meetings (behavior), and you realize `Manager` also approves budgets at a lower threshold.

The inheritance approach means each level overrides `approveBudget()`, creating a fragile chain. If you change the base `Employee` class, all 5 levels might break. If a `Director` also needs to attend board meetings (like a `VP`), you cannot inherit from both. This is the diamond problem in action.

The composition approach: `Employee` holds behavior objects: `BudgetApprover`, `MeetingParticipant`, `PerformanceEvaluator`. A `Director` gets a `BudgetApprover` with a $500K threshold. A `VP` gets the same `BudgetApprover` with $5M threshold plus a `BoardMeetingParticipant`. These behaviors are composable and independently testable. Adding a new behavior (like `TravelApproval`) means creating a new class and injecting it — no existing code changes.

The real-world lesson: inheritance creates "is-a" relationships that are rigid and assumption-laden. Composition creates "has-a" relationships that are flexible and explicit. When you hear "inheritance," ask: "Is this truly an is-a relationship, or am I just reusing code?" If the answer is code reuse, use composition.

## Q85: How would you design an A/B testing framework using OOP principles?

**A:** The core entities: `Experiment` (name, variants, traffic allocation, targeting rules), `Variant` (name, weights, configuration payload), `Assignment` (user ID, experiment, variant, timestamp), and `MetricEvent` (user ID, experiment, variant, event name, value).

The `ExperimentManager` (Singleton) holds all active experiments. `ExperimentEvaluator` (Strategy Pattern) determines which experiments a user is eligible for based on targeting rules (country, device, user segment). `AssignmentService` deterministically assigns users to variants using a hash of user ID + experiment name, ensuring the same user always sees the same variant.

The OOP design: `Experiment` is an entity with behavior: `isEligible(UserContext)` checks targeting rules. `Variant` is a value object with a weight map. `AssignmentService` uses the Strategy Pattern for hash functions: `DeterministicHashStrategy` for consistent assignment, `RandomStrategy` for true random (used in statistical analysis). The `MetricCollector` (Observer Pattern) listens for events and attributes them to the correct experiment and variant.

At senior level, discuss statistical significance: the framework must not report results until sufficient sample size is reached (avoid peeking problem). The `SignificanceCalculator` uses a Strategy Pattern for different statistical methods (frequentist, Bayesian). Discuss guardrail metrics: even if the experiment improves the primary metric, it should not degrade guardrail metrics (latency, error rate) beyond thresholds. Discuss inter-experiment interference: users in multiple experiments may have confounded results — the `ExperimentResolver` ensures no conflicting experiments run simultaneously.

## Q86: Explain how you would implement a circuit breaker that transitions between states correctly in a concurrent environment.

**A:** A circuit breaker has three states: **Closed** (requests pass through, failures are counted), **Open** (requests are immediately rejected, no calls to the downstream service), and **Half-Open** (a limited number of requests are allowed through to test if the service has recovered). The transition logic: Closed → Open (when failure count exceeds threshold), Open → Half-Open (after a timeout), Half-Open → Closed (if test requests succeed) or Half-Open → Open (if they fail).

The concurrent challenge: multiple threads may simultaneously detect a failure threshold, multiple may try to transition from Open to Half-Open, and Half-Open requests must be limited (e.g., only 10 test requests per window).

The OOP design: `CircuitBreaker` uses an `AtomicReference<CircuitState>` for the current state and `AtomicInteger` for failure/success counters. State transitions use `compareAndSet` for lock-free atomicity. The `HalfOpenLimiter` uses a `Semaphore(10)` to allow exactly 10 concurrent test requests. On the first test request success, the circuit transitions to Closed using `compareAndSet(HALF_OPEN, CLOSED)`.

At senior level, discuss configuration: failure thresholds, timeouts, and half-open probe counts should be injectable (Builder Pattern). Discuss observability: every state transition emits a metric event (`circuitbreaker.state.transition`). Discuss fallback: when the circuit is open, the `FallbackStrategy` (Strategy Pattern) returns cached data, default values, or degrades gracefully. Mention Resilience4j's implementation as a reference for production-quality circuit breakers.

## Q87: How would you design a notification delivery system that handles millions of notifications per hour across multiple channels?

**A:** The system needs to handle push (APNs, FCM), SMS (Twilio), email (SES), and in-app notifications. The core entities: `Notification` (value object with channel, payload, recipient), `DeliveryPipeline` (Mediator), `ChannelDispatcher` (Strategy Pattern for each channel), `RateLimiter` (per channel), and `DeliveryTracker`.

The `NotificationService` receives notification requests, validates them, and enqueues them in a `NotificationQueue` (Kafka, partitioned by channel). Each channel has dedicated consumers: `PushConsumer`, `SMSConsumer`, `EmailConsumer`, `InAppConsumer`. Each consumer dequeues notifications and dispatches them through the channel-specific adapter.

The OOP design: `ChannelAdapter` is an interface (Strategy Pattern) with `PushAdapter`, `SMSAdapter`, `EmailAdapter` implementations. Each adapter handles protocol-specific concerns: `PushAdapter` manages device tokens and APNs/FCM API differences. `SMSAdapter` handles phone number formatting and carrier-specific delivery. A `NotificationTracker` (Observer Pattern) records delivery status (sent, delivered, opened, failed) and triggers retries for failures.

At senior level, discuss rate limiting: each channel has different rate limits (APNs: ~500K/hour, SES: 200/sec). The `TokenBucketRateLimiter` per channel prevents exceeding quotas. Discuss priority: transactional notifications (password reset, order confirmation) have higher priority than marketing notifications. A `PriorityQueue` with separate lanes ensures transactional notifications are never delayed. Discuss deduplication: the same notification should not be sent twice — use an idempotency key derived from user ID + notification type + timestamp.

## Q88: What is the Reactive Streams Pattern and how does it relate to OOP design?

**A:** Reactive Streams provide an asynchronous, non-blocking stream processing model with backpressure. The core interfaces: `Publisher<T>` (produces items), `Subscriber<T>` (consumes items), `Subscription` (controls flow), and `Processor<T, R>` (transforms items). Backpressure ensures fast producers do not overwhelm slow consumers.

The OOP design: each stage in a reactive pipeline is an object implementing `Publisher` and/or `Subscriber`. A `MapProcessor` (implements `Processor`) transforms items and passes them downstream. A `FilterProcessor` drops items that don't match a predicate. These compose into a chain: `source.pipe(mapOp).pipe(filterOp).subscribe(sink)`.

This relates to OOP through the Decorator Pattern: each processor wraps the upstream publisher, intercepting `onNext()` calls to transform or filter. It relates to the Observer Pattern: subscribers observe the publisher. It relates to the Strategy Pattern: the transformation logic in each processor is a strategy.

At senior level, discuss Project Reactor and RxJava: they implement Reactive Streams with丰富的操作符 (map, filter, flatMap, zip). Discuss the difference from the traditional Observer Pattern: Reactive Streams adds backpressure (the subscriber tells the publisher how many items to send), subscriber lifecycle management (onComplete, onError), and composable operators. Discuss when NOT to use reactive: simple CRUD applications are clearer with imperative code; reactive shines in high-throughput, low-latency streaming scenarios.

## Q89: How would you design a distributed locking service using OOP principles?

**A:** A distributed lock ensures that only one process executes a critical section across multiple servers. The design: a `DistributedLock` interface with `tryLock(timeout)`, `unlock()`, and `isLocked()` methods. Implementations: `RedisDistributedLock` (using `SETNX` with TTL), `ZooKeeperDistributedLock` (using ephemeral znodes), and `DatabaseDistributedLock` (using `SELECT FOR UPDATE`).

The `LockManager` (Singleton) manages all active locks. A `LockContext` (value object) holds the lock key, owner ID (UUID), TTL, and creation time. The `RedisDistributedLock` implementation: `tryLock()` does `SET lock_key owner_id NX PX ttl_ms`. If the key is set, the lock is acquired. If not, it waits and retries. `unlock()` checks owner ID before deleting (prevents releasing another process's lock).

The OOP design uses the Strategy Pattern for lock implementations (switch between Redis and ZooKeeper via configuration). The `LockContext` is a value object ensuring all lock metadata travels together. A `LockWatchdog` (Observer Pattern) periodically extends the lock TTL (heartbeat) to prevent premature expiry during long operations.

At senior level, discuss the Redlock algorithm and its controversies (Martin Kleppmann's critique). Discuss lock fencing tokens: every lock acquisition increments a token, and the critical section must check the token is still current when writing. This prevents stale locks from causing corruption after a network partition. Discuss reentrancy: a non-reentrant distributed lock that is locked twice by the same thread will deadlock on unlock. The solution: track lock depth and only release on the final `unlock()` call.

## Q90: You are at a FAANG company. The interviewer asks: "How would you design the object model for a video recommendation system like YouTube?" Discuss cold start and engagement loops.

**A:** The core entities: `Video` (metadata, duration, category, embedding vector), `UserProfile` (watch history, subscriptions, preferences), `WatchEvent` (user, video, watch time, completion rate, device), `Recommendation` (video, score, reason), and `CandidateSource` (trending, related, personalized).

The `RecommendationPipeline` aggregates multiple `CandidateSource` implementations: `TrendingSource` (global popularity), `RelatedSource` (content similarity via embedding distance), `CollaborativeSource` (user-user or item-item similarity), and `SubscriptionSource` (new uploads from subscribed channels). Each source produces candidate videos with a relevance score.

The cold start problem: new users have no watch history, so personalized sources cannot help. The `ColdStartStrategy` (Strategy Pattern) uses: for new users, show trending and popular content; for new videos, use content-based features (title, thumbnail, category) and early viewer signals. The `ExplorationExploitationBalancer` (Strategy Pattern) manages the exploration-exploitation trade-off: occasionally show diverse content to learn user preferences.

The engagement loop: `WatchEvent`s feed back into the recommendation engine. High completion rates boost a video's score for similar users. Low completion rates reduce it. This creates a feedback loop — the `DiversityFilter` (Decorator Pattern) prevents filter bubbles by injecting non-personalized content.

At senior level, discuss the multi-objective optimization: recommendations must balance relevance, freshness, diversity, and creator fairness. The `Ranker` uses a learning-to-rank model that considers all objectives. Discuss A/B testing: different ranking models are tested on user segments, with guardrail metrics (session length, video completion rate, user satisfaction surveys).

## Q91: How would you design an API gateway that handles authentication, rate limiting, routing, and response transformation?

**A:** The API Gateway is a single entry point for all client requests. The design: a `RequestPipeline` (Chain of Responsibility) with handlers in order: `TLSHandler` → `AuthenticationHandler` → `RateLimitHandler` → `RoutingHandler` → `TransformationHandler` → `BackendProxy`. Each handler is an `IRequestHandler` with a `handle(HttpRequest, Chain)` method.

The `RoutingHandler` maintains a `RouteTable` (Composite Pattern) mapping URL patterns to backend service endpoints. Routes are configured with load balancing strategies (round-robin, weighted, least-connections). The `BackendProxy` makes the actual HTTP call to the backend, with timeout, retry, and circuit breaker decorators.

The OOP design: each handler is independently testable and composable. The `TransformationHandler` (Decorator Pattern) transforms request and response bodies: adding default headers, compressing payloads, converting between API versions. The `AuthenticationHandler` delegates to an `AuthProvider` (Strategy Pattern) that supports JWT, OAuth2, and API key authentication.

At senior level, discuss request/response transformation: version negotiation (`Accept: application/vnd.api.v2+json`), field filtering (`?fields=id,name,email`), and pagination normalization. Discuss WebSocket support: the gateway handles HTTP upgrade requests and proxies WebSocket connections. Discuss observability: every request is traced (OpenTelemetry), logged with structured fields, and metered (request count, latency histogram, error rate by route).

## Q92: What is the Strangler Fig Pattern and how would you apply it to migrate a monolith to microservices?

**A:** The Strangler Fig Pattern incrementally replaces parts of a monolithic application with microservices, while the system continues to function. Named after the strangler fig tree that grows around a host tree, eventually replacing it.

The design: a `RoutingFacade` (Proxy Pattern) sits in front of the monolith. Initially, all requests pass through to the monolith. As each module is extracted into a microservice, the `RoutingFacade` is updated to route those requests to the new service instead. The monolith handles fewer and fewer routes until it can be decommissioned.

The OOP design: the `RoutingFacade` uses a `RouteMapper` (Strategy Pattern) that maps URL patterns to targets (monolith or microservice). The `RouteMapper` is configurable and hot-reloadable — changing routes does not require restarting the gateway. Each extracted service communicates with the monolith through a `SharedDataBridge` during the migration period, ensuring data consistency.

At senior level, discuss the ordering of extraction: start with low-risk, high-value modules (notifications, analytics), not the core business logic. Discuss database migration: the hardest part is splitting the monolith's database. Use the Parallel Run Pattern — both the monolith and the new service write to both databases during transition, with reconciliation jobs. Discuss rollback: if the new service has issues, the `RouteMapper` can route back to the monolith instantly. This safety net is the key advantage of the Strangler Fig approach over big-bang rewrites.

## Q93: How would you design a unit of work pattern for transaction management in a domain-driven system?

**A:** The Unit of Work pattern maintains a list of objects affected by a business transaction and coordinates the writing of changes and the resolution of concurrency problems. It acts as a collector of changes — all domain operations are tracked, and at commit time, changes are persisted atomically.

The `IUnitOfWork` interface has `registerNew(entity)`, `registerDirty(entity)`, `registerDeleted(entity)`, `commit()`, and `rollback()`. The `UnitOfWorkImpl` tracks entities in three sets (new, dirty, deleted). On `commit()`, it executes in order: inserts, updates, deletes, wrapped in a database transaction. On `rollback()`, it discards all tracked changes.

The OOP design: each service method works within a unit of work. `orderService.placeOrder(command)` creates a new `Order` (registerNew), updates `Inventory` (registerDirty), and creates a `Payment` (registerNew). When the method returns, the unit of work commits. If any step fails, it rolls back.

In Spring, `@Transactional` provides this behavior implicitly. But explicit Unit of Work gives more control: you can commit partially, batch operations, or scope the transaction to a specific set of entities. At senior level, discuss the difference between Unit of Work (application-level change tracking) and database transactions (isolation levels, ACID). Discuss the Composite Pattern: nested units of work where a child unit can commit independently of the parent. Discuss concurrency: optimistic locking (version field) integrated with the unit of work's commit phase.

## Q94: Explain the Data Transfer Object anti-pattern versus the Query Object pattern.

**A:** The DTO anti-pattern (sometimes called "anemic DTOs" or "DTO whack-a-mole") occurs when DTOs mirror domain entities field-by-field, creating a mapping burden that adds no value. Every time a domain entity changes, you must update the DTO, the mapper, and the API documentation. This is mechanical, error-prone, and violates DRY (the shape is defined twice).

The **Query Object** pattern replaces multiple DTOs with a single, flexible query specification. Instead of `GetUserByIdDTO`, `GetUsersByAgeDTO`, `GetUsersByRoleDTO`, you have a `UserQuery` with builder methods: `UserQuery.builder().age(18, 30).role(ADMIN).active(true).build()`. The query object encapsulates the search criteria, and the repository implements it.

The trade-off: DTOs are simple and explicit — each API endpoint has a clear contract. Query objects are more flexible but harder to validate. In practice, use DTOs for command endpoints (create, update) where the request shape is fixed, and Query Objects for search/query endpoints where criteria vary. At senior level, discuss GraphQL as the ultimate Query Object: clients specify exactly what fields they need, eliminating over-fetching and the need for per-endpoint DTOs.

## Q95: How would you design an event sourcing system for a banking application?

**A:** Event sourcing stores all changes as a sequence of events rather than the current state. The current state is derived by replaying events. In banking, every transaction (deposit, withdrawal, transfer) is an event: `MoneyDeposited(amount, timestamp)`, `MoneyWithdrawn(amount, timestamp)`, `TransferInitiated(to, amount)`.

The `Account` entity does not have a `balance` field. Instead, `balance = events.stream().map(e -> e.amountChange()).reduce(0, Integer::sum)`. Events are immutable value objects stored in an append-only event store. The `EventStore` (interface) with `EventStoreDB` and `KafkaEventStore` implementations (Strategy Pattern).

The OOP design: `Account` is a stateful aggregate rebuilt from events. `loadFromHistory(events)` replays events to reconstruct state. Domain methods (`deposit()`, `withdraw()`) validate invariants against current state and produce new events. The `EventBus` (Observer Pattern) publishes events to downstream consumers: fraud detection, analytics, notification.

At senior level, discuss snapshotting: replaying 10,000 events to reconstruct an account is slow. Snapshots capture state at intervals, and only events after the latest snapshot are replayed. Discuss event versioning: when the `MoneyDeposited` event schema changes (e.g., adding currency), versioned upcasters transform old events to the new schema. Discuss CQRS: read models are optimized for queries (denormalized views), while write models are optimized for domain logic (event-sourced aggregates). The two models are updated by the same event stream.

## Q96: You are at a startup. The interviewer asks: "How would you design a simple yet extensible payment processing system?" Discuss how the design supports adding new payment methods without modifying existing code.

**A:** The core abstraction: `PaymentMethod` interface with `authorize(amount)` and `capture(transactionId)` methods. Implementations: `CreditCardPayment`, `ApplePayPayment`, `GooglePayPayment`, `CryptoPayment`. A `PaymentProcessor` (Mediator Pattern) accepts a `PaymentRequest` (value object with amount, currency, method, metadata) and delegates to the appropriate `PaymentMethod`.

Adding a new payment method (e.g., `AfterpayPayment`) means: (1) implement `PaymentMethod`, (2) register it in the `PaymentMethodFactory`. Zero changes to `PaymentProcessor`, `PaymentRequest`, or any existing payment method. This is the Open/Closed Principle in action.

The OOP design: `PaymentMethodFactory` (Factory Pattern) maps payment type strings to `PaymentMethod` implementations. The factory is populated at startup via configuration or classpath scanning. A `PaymentGateway` (Abstract Factory) produces `PaymentRequest` objects from user input, handling method-specific validation (card number format for credit cards, wallet address for crypto).

At senior level, discuss idempotency: `PaymentRequest` includes an idempotency key. If the same request is submitted twice (network timeout), the second call returns the cached result. Discuss 3D Secure: credit card payments may require redirect to the issuer's authentication page. The `PaymentMethod` interface supports this via `PaymentResult.get3DSRedirectUrl()`. Discuss PCI compliance: raw card numbers are never stored. The `TokenizationService` replaces card numbers with tokens, and all `PaymentMethod` implementations work with tokens, not raw numbers.

## Q97: How would you design a job scheduling system that handles dependencies between jobs?

**A:** A job scheduler manages tasks with dependencies: job B cannot start until jobs A and C complete. The design: a `Job` entity (name, status, dependencies, retry policy, timeout), a `JobGraph` (DAG — directed acyclic graph of jobs), and a `Scheduler` that executes ready jobs.

The `JobGraph` detects cycles (invalid dependency configurations) at submission time using topological sort. The `Scheduler` maintains a set of "ready" jobs (all dependencies satisfied) and executes them in parallel. When a job completes, its dependents' dependency counts are decremented. When a dependent's count reaches zero, it becomes "ready."

The OOP design: `Job` has a polymorphic `execute()` method (Strategy Pattern) — different job types have different execution logic. `EmailJob`, `ReportJob`, `DataSyncJob` implement `Job`. The `JobStatus` uses the State Pattern: `Pending`, `Ready`, `Running`, `Completed`, `Failed`, `Retried`. The `RetryPolicy` is a Strategy: `ExponentialBackoffPolicy`, `FixedDelayPolicy`, `NoRetryPolicy`.

At senior level, discuss distributed scheduling: multiple `Scheduler` instances compete to acquire jobs using a distributed lock (Redis `SETNX`). The `JobRunner` claims a job by atomically transitioning it from Ready to Running. If the runner crashes, the job's lease expires and another runner picks it up. Discuss priority: high-priority jobs preempt low-priority ones. Discuss SLA: jobs with deadlines are escalated if they approach their timeout.

## Q98: What is the Repository Pattern and how does it differ from the Data Access Object (DAO) pattern?

**A:** The **Repository Pattern** works with domain aggregates. A `UserRepository` operates on `User` aggregate roots, providing `save(User)`, `findById(UserId)`, and domain-specific queries like `findByEmail(Email)`. Repositories return domain objects and are defined in terms of the domain language. They are part of the domain layer.

The **DAO Pattern** works with database tables. A `UserDAO` provides CRUD operations on rows: `insert(UserDTO)`, `update(UserDTO)`, `selectById(long)`. DAOs return data transfer objects or raw rows. They are defined in terms of database concepts and belong to the infrastructure layer.

The key differences: Repositories are higher-level abstractions that hide persistence details entirely. A `UserRepository.findByEmail()` might query a relational database, a document store, or an in-memory cache — the caller does not know or care. A `UserDAO.selectByEmail()` is explicitly tied to the SQL query. Repositories support domain-driven design (aggregate roots, value objects), while DAOs support data-centric design.

At senior level, discuss when to use each: Repositories for complex domain logic with rich business rules. DAOs for simple CRUD applications where the database schema is the primary model. Discuss the trade-off: Repositories add an abstraction layer that must be maintained, while DAOs are simpler but couple the domain to the database.

## Q99: How would you design a feature that sends birthday notifications to 100 million users while respecting timezone differences and user preferences?

**A:** The design involves three components: a `BirthdayScheduler`, a `PreferenceChecker`, and a `NotificationDispatcher`.

The `BirthdayScheduler` runs daily at midnight in each timezone. It queries a `BirthdayRegistry` (pre-computed index of users with birthdays in each timezone-date combination) and enqueues `BirthdayNotificationTask` objects into a distributed queue (Kafka, partitioned by timezone). This avoids scanning 100M users daily — only the relevant timezone's users are loaded.

The `PreferenceChecker` (Decorator Pattern) wraps the `NotificationDispatcher`. For each user, it loads preferences: channel (push, email, SMS), quiet hours (do not disturb), and opt-out status. If the user opted out of birthday notifications, the task is dropped. If the user is in quiet hours, the notification is deferred.

The OOP design: `BirthdayNotificationTask` is a Command Pattern object containing user ID, birthday person's name, and suggested message template. The `NotificationBuilder` (Builder Pattern) constructs the final message using the template and user's preferred channel. The `Dispatcher` sends via the appropriate `ChannelAdapter`.

At senior level, discuss scaling: 100M users across 24 timezones means ~4M notifications per hour at peak (UTC midnight hits some timezones simultaneously). The queue must handle this burst. Discuss personalization: different message templates for close friends vs. acquaintances. Discuss analytics: track open rates and engagement to optimize notification timing and content. Discuss edge cases: users who set their birthday to February 29 — notify on March 1 in non-leap years.

## Q100: You are in a senior interview. The interviewer asks: "Tell me about a time you had to choose between a quick solution and a well-designed one. How did you apply OOP principles?" How do you structure your response?

**A:** Structure the response using STAR (Situation, Task, Action, Result) with explicit OOP principle references.

**Situation:** "At my previous company, we needed to add email, SMS, and push notifications to our order system within two weeks. The existing code had notification logic scattered across order processing, payment confirmation, and shipping update handlers — each with its own `if (channel == EMAIL)` blocks."

**Task:** "I needed to consolidate notification logic while delivering on the tight timeline. The quick solution was to add more `if-else` blocks for each new notification type. The well-designed solution was to introduce the Observer Pattern with a `NotificationService` abstraction."

**Action:** "I proposed a phased approach. First, I extracted the existing notification code into a `NotificationDispatcher` with a `send(channel, message)` method (Extract Class refactoring — OOP: Single Responsibility). Then I introduced a `NotificationListener` interface (Observer Pattern) and registered listeners for each order event. I delivered the first phase in one week, meeting the deadline, and completed the second phase in the following sprint."

**Result:** "The refactored code reduced notification-related bugs by 60% (from 15 bugs per quarter to 6). Adding WhatsApp notifications later took one day instead of the estimated two weeks because we only implemented a new listener — no existing code was modified (Open/Closed Principle). The interviewer appreciated that I balanced urgency with quality through incremental design improvement."

The key to this answer: you did not choose "quick" OR "well-designed" — you delivered both through incremental refactoring, demonstrating that OOP principles are not academic luxuries but practical tools for managing complexity under real business constraints.
