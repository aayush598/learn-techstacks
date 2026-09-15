# Adapter, Facade and Proxy — 100 Interview Q&A

## Q1: What is the Adapter design pattern and what problem does it solve?

**A:** The Adapter pattern converts the interface of a class into another interface clients expect. It lets classes work together that otherwise couldn't because of incompatible interfaces. The classic analogy is a power adapter — your laptop charger (target interface) needs to connect to a wall socket (adaptee interface) that has a different shape. The adapter sits between them, translating one interface to the other.

In software, you encounter incompatible interfaces when integrating third-party libraries, working with legacy systems, or using multiple data formats. Instead of modifying the third-party code (often impossible) or rewriting your client code (expensive), you write an adapter that wraps the third-party object and exposes the interface your client expects. The adapter delegates calls to the wrapped object, translating parameters as needed.

The Adapter pattern is fundamentally about translation, not transformation. It doesn't change what the adaptee does — it changes how the client sees it. This makes it one of the most practical patterns for real-world integration where you don't control all the code in the system.

---

## Q2: What is the difference between a class adapter and an object adapter?

**A:** A **class adapter** uses multiple inheritance (or interface implementation plus single inheritance) to adapt one interface to another. In Java, the adapter extends the adaptee class and implements the target interface. This gives the adapter direct access to the adaptee's protected methods and avoids creating a wrapper object. The trade-off is that class adapters are tightly coupled to the adaptee's implementation.

An **object adapter** uses composition — the adapter holds a reference to the adaptee and delegates calls to it. This is more flexible because the adapter can work with any subclass of the adaptee, and the adaptee can be swapped at runtime. Object adapters are the preferred approach in Java (which doesn't support multiple inheritance) because they follow the "favor composition over inheritance" principle.

Class adapters can override adaptee methods, which is useful for adding behavior before or after delegation. Object adapters cannot override adaptee methods directly — they can only add behavior around the delegation call. The choice depends on whether you need to modify the adaptee's behavior (class adapter) or just translate its interface (object adapter).

---

## Q3: What is a two-way adapter?

**A:** A two-way adapter implements both the target and adaptee interfaces, allowing it to be used by either the client or the adaptee. This is useful when two subsystems need to interoperate and either side might initiate the interaction. The adapter translates in both directions, acting as a bidirectional bridge.

For example, consider a legacy `OldFormatter` and a modern `NewFormatter`. A two-way adapter implements both interfaces and delegates to whichever is appropriate based on the method called. Client code using `NewFormatter` calls the adapter's `NewFormatter` methods, which delegate to `OldFormatter`. Code using `OldFormatter` calls the adapter's `OldFormatter` methods, which delegate to `NewFormatter`.

Two-way adapters are more complex than one-way adapters because they must maintain consistency between both interfaces. If the adaptee's state changes through one interface, the other interface must reflect those changes. This is straightforward when the adapter holds a reference to the adaptee and delegates all calls, but becomes tricky when both interfaces have methods that modify state in different ways.

---

## Q4: What is the Facade pattern and how does it differ from Adapter?

**A:** The Facade pattern provides a simplified, unified interface to a complex subsystem. It doesn't translate interfaces (like Adapter) — it simplifies them. The Facade knows which subsystem classes to delegate to and handles the orchestration. Clients interact with the Facade instead of directly with multiple subsystem classes.

The key difference is **intent**: Adapter makes one interface compatible with another; Facade simplifies a complex interface. Adapter changes the interface; Facade hides complexity. You use Adapter when you need to integrate something with an incompatible interface. You use Facade when you need to reduce the cognitive overhead of a complex subsystem.

A Facade can use Adapters internally — it might adapt multiple subsystem interfaces into a single, clean API for clients. The two patterns compose naturally: Facade provides the simplified top-level API, and individual subsystem interactions might use Adapters to handle interface mismatches. The Facade doesn't prevent clients from accessing subsystem classes directly; it just provides a convenient shortcut.

---

## Q5: What are the three types of Proxy patterns and their purposes?

**A:** The three main Proxy types are: **(1) Virtual Proxy** — delays creation of an expensive object until it's actually needed. The proxy holds a placeholder for the real object and creates it on first access. This is the lazy-loading pattern used in ORMs, image viewers, and resource-heavy components.

**(2) Protection Proxy** — controls access to the real object based on access rights. The proxy checks permissions before delegating calls. This is common in security frameworks where different users have different access levels to the same underlying object.

**(3) Remote Proxy** — represents an object in a different address space (different process, different machine). The proxy handles all network communication, serialization, and deserialization. The client interacts with the proxy as if it were the real object. This is the foundation of RPC frameworks, gRPC stubs, and Java RMI.

Additional proxy types include: **Logging Proxy** (logs all method calls), **Caching Proxy** (caches results and returns cached values for repeated calls), and **Synchronization Proxy** (adds thread-safety to a non-thread-safe object). All proxies share the same structure: they implement the same interface as the real object and add behavior before or after delegation.

---

## Q6: How does the Virtual Proxy pattern implement lazy loading?

**A:** A Virtual Proxy holds a reference to the real object that is initially null or uninitialized. When a method is called on the proxy, it checks if the real object exists. If not, it creates (or loads) the real object and then delegates the call. This defers the expensive initialization until the object is actually used.

In Java, this is implemented with a class that implements the same interface as the real object. The proxy's constructor accepts configuration (like an ID or URL) but doesn't create the real object. The first method call triggers creation: `if (real == null) real = loadFromDatabase(id); return real.method(args)`.

Virtual Proxy is essential for performance when object creation is expensive. For example, a virtual proxy for an image might hold only the file path and load the actual image data when `getWidth()` or `draw()` is first called. In ORM frameworks, entity proxies hold only the primary key and load all fields from the database on first property access. Spring's `@Lazy` annotation creates virtual proxies for beans that are expensive to initialize.

---

## Q7: What is the difference between the Proxy pattern and the Decorator pattern?

**A:** Both patterns wrap an object and implement the same interface, but their **intent** differs fundamentally. Proxy controls access to the object — it adds behavior around the object's methods (logging, access control, lazy loading). Decorator adds behavior to the object — it extends the object's functionality without changing its interface. The key distinction is whether the wrapper is transparent to the caller (Decorator) or introduces a policy (Proxy).

A Proxy typically knows about the real object's identity and lifecycle (it creates, caches, or protects a specific instance). A Decorator is agnostic about the wrapped object's lifecycle — it just wraps whatever it's given. A Proxy might prevent the call from reaching the real object (virtual proxy defers creation, protection proxy denies access). A Decorator always delegates to the wrapped object.

In practice, the same class can serve as both Proxy and Decorator depending on context. A logging wrapper is a Proxy if it controls access (logging + permission check) and a Decorator if it adds functionality (logging + new method). The distinction matters more for design communication than for implementation — both patterns use the same structural code.

---

## Q8: How does the Adapter pattern handle data transformation between incompatible types?

**A:** The Adapter pattern translates method calls, but it can also transform data between incompatible types. For example, if the adaptee expects `Date` objects and the client uses `LocalDateTime`, the adapter converts between them during delegation. The adapter's setter methods accept the client's types, convert to the adaptee's types, and call the adaptee. The getter methods receive the adaptee's types, convert to the client's types, and return them.

Data transformation in adapters ranges from simple type conversions (String to int, Date to LocalDateTime) to complex mappings (entity to DTO, XML to JSON). Simple transformations are inline in the adapter's methods. Complex transformations are extracted to utility methods or mapper objects to keep the adapter focused on interface translation.

The key risk is losing information during transformation. If the adaptee's type has fields that don't exist in the target type, the adapter must decide whether to drop them, throw an exception, or extend the target interface. This decision is domain-specific and should be documented in the adapter's contract.

---

## Q9: What is the Remote Proxy pattern and how does it handle network communication?

**A:** Remote Proxy creates the illusion that a remote object is local. The proxy handles all network details: establishing connections, serializing method parameters, transmitting data, receiving results, deserializing return values, and handling network errors. The client calls methods on the proxy as if it were a local object, unaware of the network layer.

In Java, RMI (Remote Method Invocation) uses Remote Proxy through stub objects. The stub implements the remote interface and communicates with the skeleton on the server side. Modern frameworks like gRPC, Dubbo, and Thrift use code generation to create proxy classes from service definitions. The generated proxy handles serialization, transport, and error handling.

The main challenges for Remote Proxy are: **(1) Latency** — remote calls are orders of magnitude slower than local calls, so proxies often batch requests or use async patterns. **(2) Failure modes** — networks fail, so proxies must handle timeouts, retries, and circuit breaking. **(3) Serialization overhead** — marshaling parameters to bytes and back adds CPU cost. **(4) Versioning** — client and server may have different versions of the interface, requiring backward-compatible serialization.

---

## Q10: How does the Facade pattern reduce coupling in a system?

**A:** Facade reduces coupling by providing a single point of interaction between clients and subsystems. Without Facade, clients depend on multiple subsystem classes, creating a web of dependencies. With Facade, clients depend on one class, and the subsystem classes depend on the Facade. This reduces the total number of dependencies and limits the blast radius of subsystem changes.

When a subsystem's internal structure changes (class renamed, method signature updated, class split into two), only the Facade needs updating. All client code remains unchanged because it depends only on the Facade's interface. This encapsulation of subsystem complexity is the primary benefit of the Facade pattern.

However, Facade can become a God Object if it accumulates too many responsibilities. As the subsystem evolves, the Facade might grow to include methods for every subsystem operation, violating the single responsibility principle. The solution is to create multiple Facades, each covering a specific use case or domain area: `OrderFacade`, `PaymentFacade`, `ShippingFacade`. This keeps each Facade focused and maintainable.

---

## Q11: What is the difference between Facade and Mediator patterns?

**A:** Both patterns centralize interactions, but at different levels. **Facade** simplifies a complex subsystem by providing a unified interface — it's a top-down simplification. **Mediator** centralizes communication between peer objects — it's a horizontal coordination. Facade wraps the subsystem; Mediator connects objects within a subsystem.

A Facade knows about subsystem classes and delegates to them. Subsystem classes don't know about the Facade. A Mediator is known by all its colleague objects, and colleague objects communicate through the Mediator rather than directly with each other. The Facade is a one-directional simplification; the Mediator is a multi-directional coordination.

In practice, the distinction blurs. A Mediator that primarily delegates to subsystem objects is effectively a Facade. A Facade that manages inter-object communication within the subsystem is effectively a Mediator. The pattern choice depends on intent: if you're simplifying an external API, use Facade. If you're decoupling objects that need to coordinate, use Mediator.

---

## Q12: How do you implement a Protection Proxy?

**A:** A Protection Proxy wraps the real object and checks access permissions before delegating calls. The proxy holds a reference to both the real object and an access control mechanism (permission checker, role resolver, policy engine). Each method call on the proxy first verifies that the caller has permission, then delegates to the real object if authorized.

The implementation typically uses Java's `java.lang.reflect.Proxy` for dynamic proxies or a hand-written wrapper class for static proxies. The access check can be based on the caller's role, the method being called, the arguments, or a combination. For example: `if (!caller.hasRole("ADMIN")) throw new AccessDeniedException("Admin required")`.

Protection Proxy is common in financial systems (trading limits), healthcare systems (HIPAA access controls), and multi-tenant SaaS (data isolation). The proxy adds a security layer that's transparent to the real object — the real object doesn't know about access control. This separation of concerns makes the security policy independently configurable and auditable.

---

## Q13: What are the common use cases for the Adapter pattern in enterprise Java?

**A:** Enterprise Java uses Adapter extensively: **(1) Legacy system integration** — wrapping old APIs with new interfaces so modern code can interact with legacy systems. **(2) Third-party library integration** — adapting a library's API to your application's preferred interface, allowing the library to be swapped without changing client code. **(3) Data format conversion** — adapters that translate between XML and JSON, SQL and NoSQL, or different data models.

**(4) Framework integration** — adapting framework-specific interfaces (Servlet API, JPA) to your domain model. **(5) Testing** — adapters that wrap external services with mock implementations for testing. **(6) Logging and monitoring** — adapters that add logging, metrics, or tracing to existing components without modifying them.

The most common enterprise pattern is the "anti-corruption layer" from Domain-Driven Design, which is essentially an Adapter that translates external system concepts into your domain model. For example, an adapter that translates a legacy SOAP service's responses into your domain entities, preventing legacy data model pollution from entering your codebase.

---

## Q14: How does the Proxy pattern handle caching?

**A:** A Caching Proxy wraps the real object and caches the results of method calls. When a method is called on the proxy, it first checks the cache. If a cached result exists and is still valid (not expired), it returns the cached value without delegating to the real object. If not, it delegates to the real object, caches the result, and returns it.

Cache invalidation is the primary challenge. Strategies include: **(1) Time-based expiry** — cached values expire after a configured duration. **(2) Event-based invalidation** — the proxy listens for events that invalidate specific cache entries. **(3) Write-through** — mutations invalidate the cache and write through to the real object. **(4) Least-recently-used (LRU)** — evict the oldest entries when the cache is full.

A Caching Proxy is transparent to the client — the client doesn't know or care about caching. The proxy can be configured dynamically: enable/disable caching per method, adjust TTL per cache entry, or switch between caching strategies. This is common in ORM second-level caches, HTTP caching proxies (Varnish, Nginx), and application-level caching (EhCache, Caffeine).

---

## Q15: What is the difference between a transparent proxy and a non-transparent proxy?

**A:** A **transparent proxy** is invisible to the client — the client doesn't know it's talking to a proxy. This is achieved by implementing the same interface as the real object and using dependency injection or factory methods to provide the proxy instead of the real object. The client's code doesn't change whether the proxy is present or not.

A **non-transparent proxy** exposes proxy-specific behavior to the client. For example, a Remote Proxy might throw `RemoteException` that the real object's local version wouldn't throw. A Caching Proxy might expose cache management methods (`invalidate()`, `clear()`). The client is aware of the proxy and may interact with its additional API.

Transparent proxies are preferred for most use cases because they don't leak implementation details. The client code remains clean and testable. Non-transparent proxies are necessary when the proxy's behavior is part of the contract (remote exceptions, cache control, lifecycle management). The key is documenting which behavior is proxy-specific so clients can handle it appropriately.

---

## Q16: Can the Adapter pattern be used to make an immutable object mutable?

**A:** The Adapter pattern can present a mutable interface over an immutable object, but it doesn't truly make the object mutable. The adapter accepts mutation calls (setters) and translates them into new immutable instances. For example, an adapter wrapping an immutable `Point` could have a `setX()` method that creates a new `Point` with the updated x-coordinate and replaces its internal reference.

This "mutating adapter" pattern is useful for compatibility with APIs that expect mutable objects. For example, adapting an immutable `Config` record to a legacy `MutableConfig` interface. The adapter holds the current immutable state and creates new instances on each mutation. Callers see a mutable interface, but the underlying data is immutable.

The caveat is identity — if callers hold references to the original object, they won't see mutations made through the adapter. The adapter replaces its internal reference, but external references remain stale. This is a fundamental limitation: immutability means shared references see consistent state, and an adapter cannot change that without breaking the immutability contract.

---

## Q17: How does the Facade pattern interact with the Singleton pattern?

**A:** Facade and Singleton are frequently combined because a Facade typically exists as a single entry point to a subsystem. Making the Facade a Singleton ensures that all clients access the same Facade instance, which is important if the Facade maintains state (like connection pools, caches, or session management).

However, the combination has pitfalls. A Singleton Facade can become a God Object that accumulates too many responsibilities. It's also harder to test because the Singleton's lifecycle is global. A better approach for testability is to use dependency injection to provide the Facade instance, making it effectively a singleton through DI container scope (application-scoped bean) rather than through the Singleton pattern.

The Facade doesn't need to be a Singleton if it's stateless — multiple instances are fine and can even improve concurrency by avoiding contention on a shared instance. The decision depends on whether the Facade maintains state that must be shared and whether the subsystem it wraps has state that requires a single point of access.

---

## Q18: What is the role of the Adapter pattern in the MVC (Model-View-Controller) architecture?

**A:** In MVC, the Adapter pattern serves several roles. **View-Adapter** adapts the Model's data format to the View's expected format. The View might expect a specific DTO structure, while the Model provides entities. An adapter converts between them, keeping the View decoupled from the Model's implementation.

**Controller-Adapter** adapts HTTP request parameters to the Controller's method parameters. The servlet container provides raw request data (strings from query parameters); the adapter converts them to typed parameters (int, Date, custom objects). Spring MVC's `@RequestParam` and `@PathVariable` handlers are essentially adapters.

**Data-Access-Adapter** adapts the persistence layer's API to the domain model. JPA's `EntityManager` provides entity objects; the adapter (Repository pattern with an adapter layer) translates between persistence entities and domain objects. This prevents persistence concerns from leaking into the domain model.

---

## Q19: What are the performance implications of using multiple proxy layers?

**A:** Stacking proxies (logging + caching + security + remote) adds overhead for each layer. Each proxy intercepts the method call, performs its behavior (logging, cache lookup, permission check, network call), and delegates to the next proxy or the real object. The overhead includes method dispatch, object allocation, and the proxy's specific operations.

The performance impact depends on what each proxy does. Logging and security proxies add minimal overhead (in-memory operations). Caching proxies can dramatically improve performance by avoiding real object calls. Remote proxies add network latency, which dominates all other overhead. Virtual proxies add a one-time initialization cost that's amortized over the object's lifetime.

In practice, profiling should guide proxy layering. If performance is critical, minimize the number of proxies or merge their responsibilities. Some frameworks use compile-time proxy generation (AspectJ, Lombok) instead of runtime proxies (Spring AOP) to eliminate reflection overhead. The key is to measure, not assume — a well-designed proxy chain can actually improve performance (caching) while adding functionality.

---

## Q20: How does the Adapter pattern support the Open-Closed Principle?

**A:** The Adapter pattern supports Open-Closed Principle by allowing new adapters to be added without modifying existing code. When a new third-party library needs to be integrated, you create a new adapter that translates its interface to the expected interface. The client code remains unchanged — it still depends on the same target interface.

For example, if your application uses a `PaymentGateway` interface and currently has a Stripe adapter, adding PayPal support means creating a `PayPalAdapter` that implements `PaymentGateway`. No existing code changes. The new adapter translates PayPal's API calls to the `PaymentGateway` interface methods.

This extensibility is the Adapter pattern's primary architectural benefit. It makes your system open to new implementations (new adapters) but closed to modification (existing client code stays the same). The target interface is the stable contract; adapters are the variable implementations. This is the essence of the Dependency Inversion Principle combined with Open-Closed.

## Q21: What is the difference between a real proxy and a dynamic proxy in Java?

**A:** A **real proxy** (static proxy) is a hand-written class that implements the target interface and wraps the real object. Each interface method is explicitly implemented with delegation logic. This gives full control but requires maintaining boilerplate for every method. If the interface has 50 methods, the proxy has 50 delegation methods.

A **dynamic proxy** (using `java.lang.reflect.Proxy` or cglib) generates the proxy class at runtime. You provide an `InvocationHandler` that receives all method calls, and the handler decides how to process each one. This eliminates boilerplate — one handler works for any interface. The trade-off is reflection overhead and less explicit code.

Dynamic proxies are ideal for cross-cutting concerns (logging, security, transactions) that apply uniformly to all methods. Static proxies are better when specific methods need different behavior or when compile-time type safety is important. Spring AOP uses dynamic proxies by default for `@Aspect` beans, falling back to cglib when the target doesn't implement an interface.

---

## Q22: How does the Facade pattern help in microservices architecture?

**A:** In microservices, the API Gateway is the canonical Facade. It provides a unified entry point for clients, hiding the complexity of multiple backend services. Instead of clients calling `user-service`, `order-service`, `payment-service`, and `shipping-service` separately, they call the API Gateway, which orchestrates the calls and aggregates responses.

The API Gateway handles cross-cutting concerns that would otherwise be duplicated across services: authentication, rate limiting, request logging, response caching, and protocol translation (REST to gRPC). Each of these is a Facade responsibility — simplifying the client's interaction with the microservices ecosystem.

Beyond API Gateways, individual services use the Facade pattern internally. A service might expose a simple REST API (the Facade) that internally coordinates between multiple domain objects, repositories, and external service calls. The Facade encapsulates the service's internal complexity, presenting a clean API to other services and clients.

---

## Q23: What is the relationship between the Proxy pattern and the AOP (Aspect-Oriented Programming) concept?

**A:** AOP and Proxy are closely related — in Java, AOP is typically implemented using proxies. Spring AOP creates JDK dynamic proxies for interfaces and CGLIB proxies for concrete classes. Each `@Aspect` is applied by wrapping the target object in a proxy that executes the aspect's advice (before, after, around) before or after delegating to the real method.

The Proxy pattern is the implementation mechanism for AOP. AOP is the conceptual framework that defines what cross-cutting concerns are (logging, security, transactions) and how they're applied (pointcuts, advice). The Proxy pattern is how the framework actually intercepts method calls and applies the advice.

This relationship means that understanding Proxy patterns is essential for understanding Spring AOP, AspectJ, and other AOP frameworks. When you write `@Transactional`, the framework creates a proxy that begins a transaction before your method, commits or rolls back after, and handles exceptions. The proxy is invisible to your code but central to the framework's operation.

---

## Q24: Can the Adapter pattern be used for protocol conversion?

**A:** Yes, protocol conversion is one of the Adapter pattern's strongest use cases. An adapter can translate between different communication protocols: HTTP to gRPC, SOAP to REST, MQTT to WebSocket, or TCP to UDP. The adapter accepts calls in one protocol and translates them to another, making the conversion transparent to the client.

For example, a legacy system might communicate via SOAP XML. A protocol adapter receives SOAP requests, extracts the operation and parameters, translates them to REST calls, and converts the REST response back to SOAP XML. The legacy client sees no change; the modern backend sees standard REST requests.

Protocol adapters are common in IoT (translating between device protocols), enterprise integration (connecting old and new systems), and cloud migration (bridging on-premises and cloud protocols). The adapter handles serialization, transport, error handling, and retry logic for both protocols, providing a seamless bridge.

---

## Q25: What are the drawbacks of the Facade pattern?

**A:** The primary drawback is that Facade can become a **God Object** — a single class that knows about and delegates to every subsystem class. As the system grows, the Facade accumulates methods for every operation, violating the single responsibility principle. Maintaining a large Facade is expensive because changes in any subsystem require Facade updates.

Another drawback is **leaky abstraction** — if clients need functionality not exposed by the Facade, they might bypass it and interact with subsystem classes directly. This defeats the Facade's purpose and creates inconsistent access patterns. The solution is to ensure the Facade covers all common use cases and to make subsystem classes package-private or internal.

Facade can also create a **single point of failure** — if the Facade is down, all clients lose access to the subsystem. This is mitigated by making the Facade stateless and horizontally scalable, but it's a concern in distributed systems. Additionally, Facade can hide performance characteristics — a single Facade call might trigger multiple expensive subsystem calls, and clients have no visibility into this cost.

---

## Q26: How does the Proxy pattern handle serialization and deserialization?

**A:** Serialization of proxy objects requires care because the proxy's state (the real object reference, handler configuration) must be serialized along with or instead of the real object. For Remote Proxies, the proxy serializes the method call (method name, parameter types, parameter values) and sends it over the network. The receiving end deserializes and invokes the real method.

For virtual proxies, serialization is tricky — the real object might not be initialized. The proxy should serialize its configuration (like an ID or URL) rather than the uninitialized real object. On deserialization, the proxy reinitializes with the same configuration and lazily loads the real object again.

Java's `SerializationProxy` pattern (from Effective Java) addresses some of these challenges by providing a separate serialization proxy that handles the conversion. For AOP proxies (Spring), serialization must include the target bean, advisors, and proxy configuration. This is why Spring recommends serializing beans by their interface rather than by their concrete (proxied) type.

---

## Q27: What is the difference between a Decorator and an Adapter when both wrap an object?

**A:** The key difference is **semantic intent**. A Decorator adds behavior to an object while maintaining its interface — it's an enhancement. An Adapter translates an object's interface to a different interface — it's a translation. If you're changing what the object looks like to the caller, it's an Adapter. If you're changing what the object does without changing its interface, it's a Decorator.

Practically, a Decorator implements the same interface as the wrapped object and adds functionality before or after delegation: `loggingOutputStream.write()` logs the data and then calls `underlying.write()`. An Adapter implements a different interface: `StringWriter` adapts `Writer` to `Readable`, providing a completely different API.

The distinction matters for system design. Decorators are composable (you can stack multiple decorators for multiple behaviors). Adapters are typically single-use (one adapter per interface mismatch). Decorators don't change the caller's code — they're transparent. Adapters change the caller's code — the caller must use the target interface.

---

## Q28: How does the Factory Method pattern complement the Proxy pattern?

**A:** Factory Method and Proxy complement each other in object creation and lifecycle management. A Factory Method can decide whether to create a real object or a proxy based on context. For example, a `DatabaseConnectionFactory` might return a real connection for direct access or a connection proxy for connection pooling, logging, and monitoring.

The Factory Method encapsulates the decision of which proxy to create. The caller doesn't know whether it's receiving a real object or a proxy. This is powerful for configuration-driven proxy creation: the factory reads configuration (enable caching, enable logging, use remote) and creates the appropriate proxy chain.

In Spring, `BeanFactory` and `ApplicationContext` are factories that create beans and may wrap them in proxies (AOP, lazy initialization, scope proxies). The application code receives a bean reference without knowing whether it's the real object or a proxy. The factory handles all proxy decisions transparently.

---

## Q29: What is the Composite Proxy pattern and when is it useful?

**A:** A Composite Proxy wraps multiple objects and delegates calls to all of them based on a routing strategy. Instead of one real object, the proxy manages a collection of real objects and distributes calls among them. This is the foundation of load balancing, failover, and round-robin proxy patterns.

For example, a load-balancing proxy holds references to multiple server instances. Each request is routed to the next available server (round-robin), the least-loaded server, or the server with the fastest response time. The client sees a single server; the proxy manages the fleet.

Composite Proxy is also used for multicast (sending a message to all registered objects), sharding (routing based on a hash key), and circuit breaking (routing around failed instances). The proxy's routing logic is the key differentiator — each routing strategy creates a different composite proxy behavior.

---

## Q30: How does the Adapter pattern handle exceptions thrown by the adaptee?

**A:** Exception handling in adapters is a design decision that affects the adapter's contract. The adapter can: **(1) Let adaptee exceptions propagate** — the client must handle adaptee-specific exceptions, which leaks the adaptee's implementation details. **(2) Catch and translate** — the adapter catches adaptee exceptions and throws target-interface-appropriate exceptions. **(3) Catch and wrap** — the adapter wraps adaptee exceptions in target-interface exceptions.

Option 2 (translation) is preferred because it maintains the abstraction. If the adaptee throws `IOException` but the target interface defines `ServiceException`, the adapter catches `IOException` and throws `ServiceException` with the relevant details. The client doesn't know about `IOException` — it only sees `ServiceException`.

The translation should preserve enough information for debugging: the original exception should be the cause of the translated exception. Use `throw new ServiceException("Failed to call adaptee", adapteeException)` to maintain the causal chain. This allows error handlers to inspect the root cause while keeping the interface clean.

---

## Q31: What is the difference between a static proxy and a dynamic proxy in terms of maintainability?

**A:** **Static proxies** require a dedicated proxy class for each interface. If the interface changes (new methods added), the proxy must be updated. This creates a maintenance burden proportional to the number of proxied interfaces. However, static proxies are explicit — you can see exactly what each proxy does by reading the code.

**Dynamic proxies** generate the proxy class at runtime from an `InvocationHandler`. Adding new interface methods doesn't require proxy changes — the handler's `invoke()` method handles all calls. This makes dynamic proxies more maintainable for interfaces that evolve frequently. The trade-off is that the handler's logic applies uniformly to all methods, which may require method-name-based branching for different behaviors.

In practice, static proxies are used for specific, well-defined wrappers (like the Adapter pattern). Dynamic proxies are used for cross-cutting concerns that apply to all methods (logging, security, transactions). The choice depends on whether you need method-specific behavior (static) or uniform behavior (dynamic).

---

## Q32: How does the Facade pattern interact with dependency injection containers?

**A:** Facade and DI containers work together naturally. The Facade is registered as a bean in the DI container, and clients inject the Facade instead of subsystem classes. The DI container manages the Facade's lifecycle and its dependencies on subsystem classes. This makes the Facade easily testable (inject mock subsystems) and configurable (swap implementations via configuration).

For example, a `PaymentFacade` is a Spring `@Service` that depends on `StripeClient`, `PayPalClient`, and `FraudDetector`. The DI container injects all dependencies. The Facade provides a simple `processPayment()` method that internally coordinates between the three subsystems. Clients inject `PaymentFacade` and don't know about the subsystem classes.

The DI container can also create dynamic proxies around the Facade for additional behavior (caching, retry, circuit breaking). This is the standard Spring AOP approach — the container creates a proxy around the Facade bean, adding aspects transparently. The client receives the proxied Facade without knowing about the proxy layer.

---

## Q33: What are the implications of using the Proxy pattern for lazy loading in ORMs?

**A:** ORMs like Hibernate use Virtual Proxies extensively for lazy loading. When you load an `Order` entity, its `List<LineItem>` might be a proxy — not the actual collection. The proxy loads the line items from the database when you first iterate over it. This avoids loading the entire object graph upfront.

The implications are: **(1) N+1 query problem** — if you load 100 orders and each lazily loads its items, you get 101 queries. This must be addressed with `JOIN FETCH` or batch loading. **(2) LazyInitializationException** — accessing a proxy outside a session (after the database connection is closed) throws an exception because the proxy can't load data. **(3) Identity issues** — two proxies for the same entity might not be `==` equal because they're different proxy instances.

** (4) Serialization challenges** — serializing a proxy that references unloaded data requires special handling (Hibernate's `@LazyToOne` options, `hibernate.enable_lazy_load_no_trans`). **(5) Debugging difficulty** — stack traces include proxy classes, and inspecting proxy objects in debuggers shows proxy state rather than real state. Despite these challenges, lazy loading proxies are essential for performance in data-heavy applications.

---

## Q34: Can the Adapter pattern be implemented as a lambda in functional languages?

**A:** Yes, in languages like Java 8+, Kotlin, and Scala, simple adapters can be expressed as lambdas when the target interface is a functional interface (single abstract method). For example, adapting a `Comparator<String>` to `Comparator<Integer>` by mapping integers to their string representations: `Comparator<Integer> adapted = (a, b) -> stringComp.compare(String.valueOf(a), String.valueOf(b))`.

For more complex adapters with state, a lambda or method reference isn't sufficient — you need a full class with fields and multiple methods. However, for single-method adaptation, lambdas are concise and readable. This is particularly useful for callbacks, event handlers, and strategy objects where a single method needs adaptation.

The limitation is that lambdas can only implement functional interfaces — they can't implement interfaces with multiple methods. For multi-method adapters, you still need a class. In practice, many adapter interfaces in modern Java are functional (Function, Predicate, Consumer), making lambda-based adapters common and idiomatic.

---

## Q35: What is the relationship between the Proxy pattern and the concept of "programming to an interface"?

**A:** The Proxy pattern is the ultimate expression of "programming to an interface." The proxy implements the same interface as the real object, and clients program against the interface, never knowing whether they have the real object or a proxy. This is the Liskov Substitution Principle in action — the proxy is substitutable for the real object.

This enables transparent behavior modification: you can swap the real object for a proxy (for caching, logging, security) without changing any client code. The client depends only on the interface, and the proxy satisfies that contract. This is the foundation of AOP, dependency injection, and mock-based testing.

The interface contract is the key enabler. If clients depended on concrete types (new RealObject()), they couldn't be transparently proxied. By depending on an interface (MyService service), the container or factory can provide a proxy that implements the same interface. This decoupling is one of the most important principles in OOP design.

---

## Q36: How does the Adapter pattern handle batch operations?

**A:** Batch operations in Adapter require translating bulk calls between the target and adaptee interfaces. If the target interface has `processAll(List<Item> items)` but the adaptee only has `processOne(Item item)`, the adapter loops over the list and calls `processOne` for each item. Conversely, if the adaptee has a batch method but the client expects individual calls, the adapter accumulates calls and batches them.

The key challenge is error handling in batch operations. If one item fails, does the entire batch fail, or do you process remaining items and report partial failures? The adapter must define this behavior and document it clearly. Strategies include fail-fast (throw on first error), best-effort (continue processing and report all errors), and transactional (all succeed or all fail).

Batch adapters also face performance considerations. Translating N individual calls to one batch call is a performance optimization (reducing overhead). Translating one batch call to N individual calls is a performance degradation. The adapter should document whether batch operations are efficient or whether callers should prefer the adaptee's native batch methods when available.

---

## Q37: What is the difference between the Facade pattern and the Service Layer pattern?

**A:** The Facade pattern simplifies a complex subsystem by providing a unified interface. The Service Layer pattern organizes business logic into services that orchestrate domain objects and repositories. They overlap in that both provide a simplified interface, but their purposes differ.

A **Facade** is about interface simplification — it wraps existing classes with a simpler API. The subsystem classes still exist and can be used directly. A **Service Layer** is about business logic organization — it contains the business logic itself, not just delegation. The Service Layer doesn't simplify an existing interface; it defines a new one with business semantics.

In practice, Service Layers often look like Facades because they delegate to repositories and external services. The distinction is intent: if the class exists to simplify a complex subsystem, it's a Facade. If it exists to implement business use cases, it's a Service Layer. Many classes serve both purposes — they're Service Layers that also act as Facades for their underlying repositories and domain objects.

---

## Q38: How does the Proxy pattern interact with object serialization frameworks?

**A:** Serialization frameworks (Jackson, Gson, JPA) must handle proxy objects correctly. When serializing a proxy, the framework should serialize the real object's state, not the proxy's wrapper state. For JPA entities with Hibernate proxies, Jackson must be configured to serialize the underlying entity, not the proxy class. This is done with `@JsonTypeInfo` or custom serializers.

The challenge is that proxies often have additional state (handler references, cached values) that shouldn't be serialized. A custom `JsonSerializer` can unwrap the proxy and serialize the real object: `proxy.getClass().getSuperclass()` to find the real class, then access the real object through reflection or a dedicated method.

Deserialization is also complex — the deserialized object shouldn't be a proxy. It should be the real object. Most serialization frameworks handle this naturally (they create a new instance of the class, not a proxy). But if the serialized form includes proxy-specific metadata, deserialization might fail. The rule of thumb: serialize the interface or the real class, not the proxy.

---

## Q39: What is the difference between a gateway and a Facade?

**A:** A **Gateway** wraps an external system and provides a simplified interface for communicating with it. It encapsulates the protocol, authentication, and data translation required to interact with the external system. A **Facade** wraps a complex internal subsystem and provides a simplified interface for clients.

The distinction is about what's being simplified. A Gateway simplifies interaction with an **external** system (third-party API, legacy system, remote service). A Facade simplifies interaction with an **internal** subsystem (domain logic, data access, business rules). A Gateway is a boundary pattern (crossing system boundaries); a Facade is an internal pattern (simplifying within a system).

In practice, a Gateway often implements the Facade pattern for external systems. The terms are sometimes used interchangeably. The key is to be consistent in your team's terminology: "Gateway" for external system wrappers, "Facade" for internal subsystem simplifiers. Both provide a unified, simplified interface, but their scope differs.

---

## Q40: Can the Adapter pattern make two interfaces mutually compatible without either changing?

**A:** Yes, this is the Adapter pattern's core capability. Both interfaces remain unchanged — the adapter sits between them and translates in both directions (if a two-way adapter) or one direction (if a one-way adapter). Neither the client nor the adaptee needs modification.

For example, if your application uses `List<Integer>` but a library expects `Collection<String>`, an adapter can wrap the list and translate between Integer and String. The application continues using `List<Integer>`; the library continues using `Collection<String>`. The adapter handles the conversion.

This is particularly valuable in enterprise integration where you can't modify third-party or legacy code. The adapter is your integration layer — it absorbs the interface mismatch and presents a clean contract to your code. The adapter's cost is maintained in one place rather than scattered across all interaction points.

---

## Q41: What is the role of the Adapter pattern in database access layers?

**A:** Database access layers use Adapter to translate between the application's domain model and the database's data model. An ORM is essentially a collection of adapters: it adapts SQL result sets to domain objects, adapts domain objects to SQL INSERT/UPDATE statements, and adapts database-specific types to Java types.

Repository implementations often use adapters to translate between the persistence layer's API (JDBC, JPA, MongoTemplate) and the domain layer's repository interface. This keeps the domain layer free from persistence concerns. A `JpaUserRepository` adapts JPA's `EntityManager` operations to the domain `UserRepository` interface.

Database-specific adapters also handle vendor differences. A `PostgresAdapter` and `MySQLAdapter` both implement a common `DatabaseAdapter` interface, translating common operations to vendor-specific SQL. This enables database portability — switching from PostgreSQL to MySQL requires only swapping the adapter, not changing repository code.

---

## Q42: How does the Proxy pattern support the principle of least knowledge (Law of Demeter)?

**A:** The Proxy pattern supports Law of Demeter by providing a single point of contact. Clients interact with the proxy and don't need to know about the real object, its dependencies, or its internal structure. This reduces the number of objects clients must know about, adhering to the principle of "talk only to your immediate friends."

For example, a `UserRepositoryProxy` handles all database interactions. The service layer interacts only with the proxy, not with `DataSource`, `Connection`, `PreparedStatement`, or `ResultSet`. The proxy encapsulates the database subsystem, reducing the service layer's knowledge to just the repository interface.

This also applies to Remote Proxies — clients interact with the proxy as if it were a local object, without knowing about network protocols, serialization formats, or remote server addresses. The proxy reduces the client's knowledge to the interface methods, hiding all infrastructure concerns.

---

## Q43: What is the difference between the Proxy pattern and the Chain of Responsibility pattern?

**A:** Proxy wraps a specific object and delegates to it. Chain of Responsibility passes a request along a chain of handlers, where each handler decides whether to process it or pass it forward. Proxy always has a definite target (the real object). Chain of Responsibility might not have a definite target — the request might reach the end of the chain without being handled.

Proxy adds behavior before or after delegation (logging, caching, security). Chain of Responsibility routes the request based on handler capabilities (each handler checks if it can handle the request). Proxy is about wrapping; Chain of Responsibility is about routing.

They can overlap: a proxy chain (logging → caching → security → real object) is technically both patterns. The key difference is the design intent: if you're wrapping a specific object, it's a Proxy. If you're routing through a sequence of potential handlers, it's Chain of Responsibility. The proxy has one definite destination; the chain has potential destinations.

---

## Q44: How do you implement a Logging Proxy without changing the real object's interface?

**A:** A Logging Proxy wraps the real object and logs every method call. The proxy implements the same interface, intercepts each call, logs the method name, parameters, and return value, then delegates to the real object. The real object is unchanged — it doesn't know about logging.

For static proxies, each method is implemented with logging around the delegation: `log("methodA called with " + args); result = real.methodA(args); log("methodA returned " + result); return result;`. For dynamic proxies, a single `InvocationHandler` handles all methods: `log(method.getName() + " called"); result = method.invoke(real, args); log(method.getName() + " returned");`.

The logging proxy should handle exceptions: catch exceptions thrown by the real object, log them with stack traces, and rethrow. It should also handle void methods (log completion without return value). Configuration options include: log level (INFO, DEBUG, TRACE), parameter truncation (for large objects), and sensitive data masking (passwords, credit card numbers).

---

## Q45: What is the impact of the Adapter pattern on type safety?

**A:** Adapters can weaken type safety if they use raw types, unchecked casts, or Object-based APIs. A well-designed adapter maintains the target interface's type safety. For example, an adapter that translates `List<String>` to `List<Integer>` should produce `List<Integer>` (type-safe), not `List` (raw) or `List<Object>` (unsafe).

The risk is highest with legacy system adapters where the adaptee uses weakly-typed APIs (String-based parameters, Object return types). The adapter must perform type conversions and validations that, if done incorrectly, produce ClassCastExceptions at runtime. The solution is to perform all type conversions and validations in the adapter's constructor or factory method, failing fast with descriptive error messages.

For generic adapters, use Java's wildcard types and bounded generics to maintain type safety: `<T extends Adaptee> void adapt(T source, Target target)`. This ensures the adapter works with any subtype of the adaptee while maintaining type relationships. The type system catches mismatches at compile time rather than runtime.

---

## Q46: How does the Facade pattern help with API versioning?

**A:** Facade is a natural tool for API versioning. Each API version is a different Facade that wraps the same underlying subsystem. The v1 Facade exposes the original API; the v2 Facade adds new methods, changes parameters, or restructures responses while delegating to the same subsystem classes.

This approach avoids duplicating business logic across versions. Both v1 and v2 Facades delegate to the same service layer and domain objects. The difference is in the interface shape and parameter translation. The v2 Facade might accept additional parameters, convert them to the subsystem's format, and return enriched responses.

Version-specific Facades can coexist in the same application. The routing layer (API Gateway, controller) directs requests to the appropriate version Facade based on the URL or header. This allows gradual migration: old clients continue using v1; new clients adopt v2. When v1 is retired, its Facade is removed without affecting the subsystem.

---

## Q47: What is the relationship between the Proxy pattern and the concept of lazy initialization?

**A:** Lazy initialization is the practice of deferring object creation until it's needed. The Virtual Proxy pattern is the structural implementation of lazy initialization. Instead of creating the real object eagerly (in the constructor or at class load time), the proxy creates it lazily (on first method call).

The proxy holds a placeholder (null, or a configuration object) instead of the real object. The first method call triggers creation: `if (real == null) { real = createRealObject(); } return real.method(args)`. This pattern is thread-safe when synchronized: `if (real == null) { synchronized(this) { if (real == null) { real = createRealObject(); } } }` (double-checked locking).

Lazy initialization proxies are essential for performance when object creation is expensive. Spring's `@Lazy` annotation creates JDK dynamic proxies for lazy bean initialization. Hibernate uses lazy loading proxies for entity relationships. Image viewers use lazy proxies to load image data on demand. The proxy pattern makes lazy initialization transparent — callers don't know or care about the deferred creation.

---

## Q48: How does the Adapter pattern handle events and callbacks?

**A:** Adapting events and callbacks involves translating between event systems. If the adaptee fires events using its own listener interface and the client expects a different listener interface, the adapter implements the client's listener interface and translates calls to the adaptee's listener methods.

For example, an adaptee might fire `DataChangedEvent` through a `DataListener` interface. The client expects `PropertyChangeEvent` through a `PropertyChangeListener`. The adapter implements `DataListener`, receives `DataChangedEvent`, translates it to `PropertyChangeEvent`, and fires it through the client's event system.

The adapter must handle event threading — some event systems fire events on the calling thread, others on background threads. The adapter may need to dispatch events to the correct thread using an executor or event queue. The adapter should also handle listener registration and removal for both event systems.

---

## Q49: What are the implications of the Proxy pattern for unit testing?

**A:** Proxies complicate unit testing in several ways. **(1) Mocking** — when testing a class that depends on a proxied object, you must decide whether to mock the proxy or the real object. Mocking the proxy (via `@Mock`) replaces the entire proxy, including its behavior. Mocking the real object (via `@Spy`) wraps the real object but preserves its behavior.

**(2) AOP proxy interference** — Spring AOP creates proxies around beans. When testing, these proxies add overhead and may interfere with test setup (transactional proxies starting/stolling transactions). Use `@SpringBootTest` or `@ContextConfiguration` to control proxy creation in tests.

**(3) Lazy proxy initialization** — virtual proxies in tests might not initialize properly if the test doesn't trigger the lazy loading. Use `@Lazy` carefully in tests or provide test-specific initialization.

**(4) Reflection and proxy class inspection** — debugging proxy-related issues requires understanding which proxy framework is used (JDK, CGLIB) and how to inspect the proxy's handler. Tools like Spring Boot's `/actuator/beans` endpoint can help inspect proxy creation.

---

## Q50: Can the Facade pattern be used to migrate between two subsystem implementations?

**A:** Yes, Facade is a powerful migration tool. You create a new Facade that wraps the new subsystem and presents the same interface as the old Facade. Clients migrate gradually from the old Facade to the new one. During the transition period, both Facades coexist, and the routing layer directs traffic to the appropriate implementation.

This is the **Strangler Fig** pattern — gradually replacing parts of a legacy system with new implementations while maintaining the external interface. The Facade is the interface contract that remains stable during migration. Clients continue calling the same methods; only the Facade's internal implementation changes.

For example, migrating from a monolithic `OrderService` to a microservice-based `OrderService` involves creating a new Facade that delegates to microservices instead of the monolith. The routing layer (API Gateway, feature flags) gradually shifts traffic from the old Facade to the new one. When all traffic is on the new Facade, the old one is retired. This provides zero-downtime migration with rollback capability.

## Q51: How do you implement a thread-safe Proxy pattern?

**A:** Thread-safe proxies must handle concurrent access to the proxy and the real object. For read-only proxies (virtual proxy, caching proxy), the primary concern is ensuring that lazy initialization happens only once (double-checked locking or `volatile` + synchronized). For proxies that modify state, synchronization must protect both the proxy's internal state and the real object's state.

The double-checked locking pattern is the standard for lazy initialization: check if the real object is null without synchronization (fast path), then synchronize and check again (safe path). The real object reference must be `volatile` to prevent instruction reordering. Alternatively, use `Supplier` with `MemoizingSupplier` for thread-safe lazy initialization without manual synchronization.

For proxies that add synchronized behavior (synchronization proxy), the proxy acquires a lock before delegating to the real object. This ensures only one thread accesses the real object at a time. The lock granularity (per-proxy, per-method, or per-object) affects performance. Per-proxy locking is simplest but limits concurrency; per-method locking allows concurrent reads.

---

## Q52: What is the difference between the Adapter pattern and the Bridge pattern?

**A:** Adapter and Bridge are both structural patterns that work with object composition, but their intents differ. **Adapter** makes two incompatible interfaces compatible — it's a post-hoc integration tool. **Bridge** separates abstraction from implementation so they can vary independently — it's a design-time architectural decision.

Adapter is used when you have existing classes with incompatible interfaces and need them to work together. Bridge is used when designing new systems where you want abstraction and implementation to evolve independently. Adapter changes the interface; Bridge creates two parallel hierarchies (abstraction + implementation).

A concrete example: if you have `LegacyPrinter` (with `print(String text)`) and your code expects `ModernPrinter` (with `printDocument(Document doc)`), you create an `PrinterAdapter` (Adapter pattern). If you're designing a new printing system where you want `Printer` abstraction to vary independently from `PrintEngine` implementation, you create `Printer` (abstraction) and `PrintEngine` (implementation) hierarchies (Bridge pattern).

---

## Q53: How does the Facade pattern handle asynchronous operations?

**A:** Facade methods can be synchronous or asynchronous depending on the subsystem's nature. For asynchronous subsystems (message queues, event streams, background processing), the Facade provides async methods that return `CompletableFuture`, `Mono`, or `Flowable`. The Facade starts the async operation and returns a handle for the client to track progress.

The Facade must handle the complexity of coordinating multiple async subsystem calls. If the Facade needs to call three services and aggregate results, it uses `CompletableFuture.allOf()` or reactive operators to combine the async results. The client receives a single future that completes when all subsystem operations finish.

Error handling in async Facades is more complex than synchronous ones. Failures in different subsystems might occur at different times. The Facade must aggregate errors, handle partial failures (some subsystems succeed, others fail), and provide meaningful error information to the client. Timeout handling is also critical — the Facade should set overall timeouts and per-subsystem timeouts to prevent indefinite waiting.

---

## Q54: What is the impact of the Proxy pattern on garbage collection?

**A:** Proxies add objects to the object graph that the garbage collector must traverse. Each proxy is an additional object with references to the real object, the invocation handler, and any cached state. For applications with many proxied objects (ORM entities, AOP-managed beans), this increases the GC's work.

Virtual proxies prevent premature loading of heavy objects, which can improve GC behavior — the real object isn't created until needed, and if never needed, it's never created. This reduces the total object count and memory footprint. Caching proxies can increase memory usage by holding cached copies alongside the real object.

The GC impact is usually negligible compared to the benefits (lazy loading, caching, security). However, in memory-sensitive applications (Android, embedded systems), the proxy overhead must be considered. Profiling with GC logs and heap dumps can quantify the impact. Mitigation strategies include: using weak references in proxy caches, minimizing proxy nesting, and using compile-time proxies instead of runtime proxies.

---

## Q55: How does the Adapter pattern work with event-driven architectures?

**A:** In event-driven architectures, Adapters translate between different event formats and transports. A `KafkaAdapter` might translate between your application's domain events and Kafka's `ProducerRecord` format. A `WebSocketAdapter` translates between internal events and WebSocket messages. The adapter handles serialization, transport configuration, and error handling.

Event adapters also handle protocol differences. A `RESTToEventAdapter` receives REST requests and publishes them as events to a message broker. A `EventToRESTAdapter` subscribes to events and calls REST endpoints. These adapters decouple the event infrastructure from the API layer, allowing either to change independently.

The key challenge is idempotency. Event-driven systems may deliver events multiple times (at-least-once delivery). The adapter must ensure that processing the same event twice produces the same result. This is typically handled at the consumer level, but the adapter can assist by including idempotency keys or deduplication logic.

---

## Q56: What is the difference between the Proxy pattern and the Interceptor pattern?

**A:** The Proxy pattern wraps a specific object and delegates to it. The Interceptor pattern intercepts requests at a framework level, before they reach the target object. Interceptors are framework-provided extension points (Servlet Filters, Spring Interceptors, gRPC Interceptors) that process requests in a pipeline.

The key difference is scope. A Proxy wraps a single object and is tightly coupled to it. Interceptors operate at the framework level and affect all requests or requests matching certain criteria. A Proxy is object-level; an Interceptor is request-level.

In practice, they're complementary. A Spring `HandlerInterceptor` intercepts all HTTP requests (framework level), while a Spring AOP proxy intercepts all method calls on a specific bean (object level). You might use an Interceptor for logging all requests and a Proxy for caching a specific service's responses.

---

## Q57: Can the Adapter pattern be used for API gateway functionality?

**A:** Yes, an API Gateway is essentially a large-scale Adapter. It receives requests in one protocol (HTTP, gRPC, WebSocket), translates them to backend service protocols, and translates responses back. The gateway adapts between the external API contract and the internal service architecture.

The gateway's adapter functions include: protocol translation (HTTP to gRPC), authentication (translating tokens to internal user context), rate limiting (adapting request flow to backend capacity), and response transformation (formatting internal responses to match the external API schema).

Each backend service might have its own API Gateway adapter that translates between the gateway's unified format and the service's specific format. This adapter layer isolates services from API changes — when the external API evolves, only the gateway adapter changes, not the internal services.

---

## Q58: How does the Facade pattern work with CQRS (Command Query Responsibility Segregation)?

**A:** In CQRS, commands and queries are separated into different models. The Facade pattern provides a unified entry point for both. A `CommandFacade` handles all write operations (create, update, delete), and a `QueryFacade` handles all read operations (fetch, search, report). Each Facade simplifies interaction with its respective model.

The Command Facade translates incoming commands into domain model operations, validates them, and delegates to the command handler. The Query Facade translates incoming queries into read model operations and returns DTOs. Clients interact with the appropriate Facade based on whether they're reading or writing.

The Facade also handles cross-cutting concerns that span both models: authentication, authorization, audit logging, and event publishing. Without Facades, clients would need to know which command handler or query handler to call, creating tight coupling between the client and the CQRS infrastructure.

---

## Q59: What are the implications of using Proxy pattern in distributed caching?

**A:** Distributed caching systems use Proxy patterns extensively. A **client-side proxy** (like Jedis for Redis or a Memcached client) wraps network communication and provides a local API. The proxy handles connection pooling, serialization, retry logic, and failover. The application code calls `cache.get("key")` without knowing about network communication.

A **server-side proxy** (like Redis Cluster's redirect mechanism) routes requests to the correct cache node based on the key hash. The client connects to any node (the proxy); the proxy redirects to the correct node. This is transparent to the client — it appears to be talking to a single cache.

The cache proxy must handle: **(1) Serialization** — converting objects to bytes and back. **(2) Connection management** — pooling connections, handling disconnections, and reconnecting. **(3) Consistency** — ensuring cache invalidation propagates across nodes. **(4) Failover** — routing around failed nodes. These concerns are entirely hidden from the application by the proxy.

---

## Q60: How does the Adapter pattern handle versioning of external APIs?

**A:** External API versioning creates a moving target for adapters. When the external API changes (new endpoints, different data formats, deprecated fields), the adapter must be updated to handle both old and new versions during the transition period.

The versioning adapter approach maintains separate adapter classes for each API version: `ExternalApiV1Adapter`, `ExternalApiV2Adapter`. A factory selects the appropriate adapter based on configuration or the external system's version. During migration, both adapters coexist, and clients gradually transition to the new adapter.

Another approach is a single adapter with version detection: the adapter inspects the response to determine the API version and handles each version's quirks internally. This keeps one adapter class but increases its complexity. The trade-off is maintainability (single class) versus clarity (separate classes per version).

---

## Q61: What is the relationship between the Proxy pattern and security?

**A:** Security is one of the Proxy pattern's primary applications. **Protection Proxy** enforces access control by checking permissions before delegating to the real object. **Authentication Proxy** verifies the caller's identity before allowing method execution. **Authorization Proxy** checks whether the authenticated caller has permission for the specific operation.

In enterprise systems, security proxies are often generated by frameworks (Spring Security, AspectJ) and applied via annotations (`@PreAuthorize`, `@Secured`). The proxy intercepts the method call, evaluates the security expression, and either delegates to the real method or throws an `AccessDeniedException`.

Security proxies must be tamper-proof — an attacker shouldn't be able to bypass the proxy. This requires that the proxy is the only entry point to the real object (no bypassing through reflection or direct reference access). The DI container ensures that clients always receive the proxied version, not the real object.

---

## Q62: How does the Facade pattern help with cross-cutting concerns?

**A:** Cross-cutting concerns (logging, security, transactions, metrics) span multiple components. The Facade centralizes these concerns for a subsystem. Instead of each subsystem component implementing its own logging and security, the Facade handles them once and delegates to clean, focused subsystem components.

For example, a `PaymentFacade` handles transaction management: it starts a transaction, delegates to `FraudDetector` and `PaymentGateway`, commits the transaction on success, and rolls back on failure. Without the Facade, each component would need to manage its own transaction context, leading to duplicated and inconsistent transaction handling.

The Facade also handles concerns that span multiple subsystem calls: correlation IDs (tracing a request across services), request/response logging, and metrics collection. These are naturally placed in the Facade because it's the single entry point that sees the complete operation.

---

## Q63: What is the difference between a transparent Facade and an explicit Facade?

**A:** A **transparent Facade** is injected or provided transparently — the client doesn't know it's using a Facade. This is achieved through DI, where the Facade implements the same interface as the subsystem, and the container provides the Facade instead. The client code is identical whether the Facade is present or not.

An **explicit Facade** is a class that the client explicitly instantiates and calls. The client knows it's using a Facade and interacts with it directly. This is more common in API design (REST controllers are explicit facades) and in library design (fluent APIs are explicit facades).

Transparent Facades are better for testability and flexibility — you can swap the Facade for a mock or alternative implementation. Explicit Facades are better for discoverability and documentation — the Facade's API is visible in the client code. Most real-world Facades are explicit because subsystem simplification is usually a conscious architectural choice.

---

## Q64: How do you handle the Adapter pattern when the adaptee interface is not available at compile time?

**A:** When the adaptee is a dynamic system (REST API, database schema, message format), you can't implement a compile-time adapter. Instead, you use reflection, code generation, or configuration-based adaptation. For REST APIs, OpenAPI code generators create adapter classes from API specifications at build time.

For runtime adaptation, reflection-based adapters inspect the adaptee's methods and properties dynamically. Java's `java.lang.reflect` package enables creating adapters that work with any class, not just known interfaces. The trade-off is loss of type safety and compile-time checking.

Another approach is data-driven adaptation: a configuration file maps adaptee methods to target methods, and a generic adapter engine performs the mapping at runtime. This is common in integration platforms (MuleSoft, Apache Camel) where adapters are configured declaratively rather than coded imperatively.

---

## Q65: What are the common anti-patterns when using the Facade pattern?

**A:** Common anti-patterns include: **(1) God Facade** — the Facade knows about every subsystem class and handles every operation. This creates a maintenance bottleneck. Fix: split into multiple focused Facades. **(2) Leaky Facade** — the Facade exposes subsystem internals (returning subsystem entities instead of DTOs). Fix: use DTOs or domain objects as the Facade's return types.

**(3) Anemic Facade** — the Facade only delegates without adding value. If the Facade doesn't simplify, coordinate, or add cross-cutting behavior, it's unnecessary indirection. Fix: ensure the Facade provides meaningful simplification. **(4) Chatty Facade** — the Facade requires many calls to complete one operation. Fix: provide batch or composite methods that handle common multi-step operations.

**(5) Facade-in-Facade** — one Facade delegates to another Facade, which delegates to the subsystem. This creates unnecessary indirection layers. Fix: keep Facade delegation flat — one Facade per subsystem. The test of a good Facade is: does it make the client's code simpler? If not, it's either unnecessary or poorly designed.

---

## Q66: How does the Proxy pattern interact with the singleton pattern?

**A:** Proxy and Singleton interact in several ways. A Singleton can be wrapped in a Proxy for additional behavior (caching, logging, access control) without changing the Singleton's implementation. The Proxy delegates to the Singleton instance, adding its behavior transparently.

A Singleton Proxy ensures that only one proxy instance exists, which is important when the proxy maintains state (caches, connection pools). The Singleton Proxy coordinates access to the shared real object, providing thread-safe, single-point-of-access behavior.

Alternatively, a Proxy can implement the Singleton pattern itself — the proxy ensures that only one instance of the real object exists. The proxy holds the single instance and returns it on every creation request. This is the "virtual proxy as singleton" pattern, commonly used in connection pools and cache managers.

---

## Q67: What is the relationship between the Adapter pattern and the Decorator pattern in middleware?

**A:** Middleware (servlet filters, message interceptors, HTTP middleware) combines Adapter and Decorator patterns. Each middleware layer is a Decorator that adds behavior (logging, authentication, compression) around the next layer. The overall middleware pipeline is an Adapter that translates between the external protocol (HTTP) and the internal application logic (handler methods).

For example, a middleware pipeline might include: `LoggingDecorator` → `AuthAdapter` → `CompressionDecorator` → `HandlerAdapter` → `Application`. The logging and compression layers are Decorators (adding behavior). The auth and handler layers are Adapters (translating between formats). The pipeline composes both patterns to process requests.

The distinction matters for middleware authors: if you're adding behavior (logging, metrics), you're a Decorator. If you're translating formats (HTTP to domain, XML to JSON), you're an Adapter. Most middleware uses both patterns at different layers.

---

## Q68: How does the Facade pattern handle error recovery?

**A:** A well-designed Facade handles errors from subsystem components and provides meaningful error information to clients. The Facade catches subsystem exceptions, translates them into domain-appropriate exceptions, and ensures cleanup (rolling back transactions, releasing resources) before propagating.

Error recovery strategies include: **(1) Fail-fast** — propagate the subsystem error immediately. **(2) Retry** — retry the failed subsystem operation with backoff. **(3) Fallback** — provide an alternative response when the subsystem fails. **(4) Circuit breaking** — stop calling a failed subsystem and return cached or default responses.

The Facade is the natural place for error recovery because it orchestrates the subsystem calls. If a multi-step operation fails midway, the Facade can roll back completed steps and clean up resources. Without the Facade, each client would need to implement its own error recovery logic, which is error-prone and duplicated.

---

## Q69: What is the impact of the Proxy pattern on API performance?

**A:** Proxy overhead varies by type. **Virtual Proxy** adds a one-time initialization cost and a null check on each method call (negligible). **Caching Proxy** dramatically improves performance for repeated calls by avoiding real object invocations. **Security Proxy** adds permission-check overhead on each call (typically fast, in-memory operations).

**Remote Proxy** adds network latency, which dominates all other overhead. The proxy's serialization/deserialization adds CPU cost. **Logging Proxy** adds I/O cost for each log write. **Synchronization Proxy** adds lock acquisition overhead, potentially reducing concurrency.

The net performance impact depends on the use case. Caching Proxies often improve performance by orders of magnitude. Security and logging proxies add small overhead that's usually acceptable for the functionality gained. Remote proxies add significant overhead that must be justified by the distributed architecture's benefits. Profiling is essential to quantify the actual impact.

---

## Q70: Can the Adapter pattern be used to adapt synchronous interfaces to asynchronous ones?

**A:** Yes, this is a common and valuable adaptation. An adapter can wrap a synchronous adaptee with an asynchronous interface by executing the synchronous call on a background thread and completing a `CompletableFuture` when done. The client receives a future and can continue working while the synchronous operation completes.

```java
public class AsyncUserAdapter {
    private final SyncUserService syncService;
    private final ExecutorService executor;

    public CompletableFuture<User> getUser(String id) {
        return CompletableFuture.supplyAsync(
            () -> syncService.findUser(id), executor);
    }
}
```

The reverse adaptation (async to sync) is also possible but more dangerous — it blocks the calling thread until the async operation completes. This can cause deadlocks if the async operation needs the calling thread (common in UI frameworks and single-threaded event loops). The adapter must ensure that blocking doesn't deadlock the system.

---

## Q71: How does the Facade pattern help with database migration?

**A:** Database migration (changing schema, switching databases, adding caching) is a prime use case for the Facade pattern. The Repository Facade provides a stable data access API while the underlying implementation changes. During migration, you create a new repository implementation (targeting the new database) and update the Facade to delegate to it.

The Strangler Fig pattern applies here: gradually migrate data access from the old implementation to the new one. The Facade routes read operations to the new database while write operations go to both (write-through). When all reads come from the new database, writes switch entirely. The Facade handles this routing transparently.

For schema changes (adding columns, renaming tables), the Facade translates between the old and new schemas. Existing code continues using the old schema through the Facade; new code uses the updated schema. The Facade maps between them, preventing schema changes from rippling through the codebase.

---

## Q72: What are the trade-offs of using dynamic proxies versus static proxies?

**A:** **Dynamic Proxies** trade compile-time type safety and code readability for flexibility and reduced boilerplate. They handle any interface automatically but require method-name-based branching for different behavior per method. Reflection overhead adds runtime cost, and debugging is harder because the proxy class is generated.

**Static Proxies** trade flexibility and reduced boilerplate for compile-time type safety and readability. Each method is explicitly implemented, making the proxy's behavior clear from the code. No reflection overhead, easy debugging, and the compiler catches type errors. The downside is maintaining boilerplate for every interface method.

Use dynamic proxies when: cross-cutting concerns apply uniformly to all methods (logging, security), the interface changes frequently, or you need to proxy many different interfaces with the same logic. Use static proxies when: specific methods need different behavior, compile-time safety is critical, or the interface is stable and has few methods.

---

## Q73: How does the Adapter pattern handle streaming data?

**A:** Streaming adapters translate between different streaming APIs. For example, adapting Java's `Stream<T>` to Reactor's `Flux<T>`, or adapting Kafka's `ConsumerRecords` to a domain-specific `EventStream`. The adapter converts elements one-by-one or in batches, handling the different buffering, backpressure, and completion semantics of each streaming API.

The key challenges are: **(1) Backpressure** — the source might produce faster than the consumer can process. The adapter must handle buffering or signal the source to slow down. **(2) Error handling** — errors in streaming adapters must be propagated correctly (one error shouldn't kill the entire stream unless the contract says so). **(3) Resource cleanup** — streams hold resources (file handles, network connections) that must be released when the stream completes or is cancelled.

Streaming adapters are common in data pipeline architectures where data flows through multiple processing stages. Each stage might use a different streaming framework, and adapters translate between them. The adapter must maintain the stream's characteristics (ordering, completeness, error semantics) across the translation boundary.

---

## Q74: What is the relationship between the Proxy pattern and the concept of lazy evaluation in functional programming?

**A:** Lazy evaluation defers computation until the result is needed. The Virtual Proxy is the OOP equivalent — it defers object creation until the object is used. In functional programming, `lazy val` (Scala) or `memoize` (Haskell) defer and cache computation. The Virtual Proxy defers and caches object creation.

The connection is deeper than superficial similarity. Both patterns solve the same problem: expensive computation that might not be needed. The Virtual Proxy creates the object on first access; lazy evaluation computes the value on first access. Both cache the result for subsequent accesses.

The implementation differs: functional lazy evaluation uses language features (thunks, suspensions) or library functions (memoize). OOP Virtual Proxies use wrapper classes. The conceptual overlap means that functional programmers immediately understand Virtual Proxies, and OOP programmers can apply proxy thinking to lazy evaluation.

---

## Q75: How does the Facade pattern support API design for mobile applications?

**A:** Mobile apps benefit from Facades that simplify backend interactions. A mobile API Facade consolidates multiple backend calls into single endpoints optimized for mobile usage. Instead of the mobile app making 5 separate API calls (user profile, recent orders, recommendations, notifications, settings), it calls one Facade endpoint that aggregates all data.

The Facade also handles mobile-specific concerns: **(1) Payload minimization** — returning only the fields the mobile screen needs, reducing bandwidth. **(2) Offline support** — the Facade can serve cached responses when the network is unavailable. **(3) Protocol optimization** — using gRPC or GraphQL instead of REST for more efficient communication. **(4) Authentication simplification** — handling OAuth token refresh and session management.

BFF (Backend for Frontend) is a specific Facade pattern for different client types. A `MobileBFF` Facade is optimized for mobile; a `WebBFF` Facade is optimized for web. Each provides a tailored API for its client type, hiding the complexity of shared backend services.

---

## Q76: How do you test a class that depends on an Adapter?

**A:** Testing an Adapter requires isolating the translation logic from the external dependency. The recommended approach is **double adapter testing**: create a test adapter that wraps a mock external dependency, then verify the adapter correctly translates between the mock and your domain interface. This lets you test translation logic without hitting real external systems.

Another strategy is to define the adapter interface itself as an abstraction and inject a mock implementation during tests. This follows the Dependency Inversion Principle — your code depends on an abstraction (the adapter interface), not the concrete adapter. In tests, you substitute a `FakeAdapter` that implements the same interface but returns controlled test data.

Integration tests should verify the real adapter against a real external system, but these should be isolated in a separate test suite and run less frequently. The key insight is that adapters are **thin translation layers**, so unit tests with mocks cover most correctness concerns. Integration tests catch issues like API version mismatches, serialization edge cases, and network behavior that mocks cannot simulate.

---

## Q77: Can the Proxy pattern be used to implement access control lists (ACLs)?

**A:** Yes. A Protection Proxy checks the caller's identity and permissions before forwarding each method call to the real subject. The proxy maintains an ACL mapping roles or users to permitted operations. When `save()` is called, the proxy checks whether the caller's role includes `write` permission; if not, it throws `AccessDeniedException`.

This approach separates authorization concerns from business logic. The real subject implements only business rules; the proxy enforces access control. You can compose multiple proxies for layered security: authentication proxy (verifies identity), authorization proxy (checks permissions), and audit proxy (logs who did what). Each proxy adds one concern without cluttering the subject.

The ACL proxy can also be made dynamic — loading permissions from a database or configuration file and refreshing them at runtime. This enables administrative changes to permissions without restarting the application. The proxy pattern makes this particularly clean because the permission check is encapsulated in one place rather than scattered across every method in every business class.

---

## Q78: What is the difference between a Facade and a Mediator?

**A:** A Facade provides a simplified interface to a subsystem — it's a one-directional wrapper that makes complex subsystems easier to use. The subsystem components don't know about the Facade; they operate independently. The Facade coordinates by delegating to existing subsystem methods.

A Mediator centralizes complex communications between multiple objects. Unlike a Facade, the Mediator pattern implies that the colleague objects are aware of the Mediator and communicate through it rather than directly with each other. The Mediator encapsulates the interaction logic that would otherwise be distributed across many objects.

The distinction matters architecturally: a Facade simplifies without modifying the subsystem's internal relationships — you can bypass the Facade and use the subsystem directly. A Mediator restructures the communication topology — the colleagues genuinely depend on the Mediator and cannot function without it. In practice, a Mediator often becomes a colleague itself that participates in the system's behavior, while a Facade remains purely an external simplifier.

---

## Q79: How does the Adapter pattern handle bidirectional translation?

**A:** Bidirectional adapters translate in both directions — from interface A to interface B and from interface B to interface A. This is needed when two systems must communicate and each uses different data representations. A single adapter class with methods like `toDomain()` and `fromDomain()` handles both directions.

The challenge is maintaining consistency: the round-trip conversion (A → domain → A) should preserve the original data. This requires careful handling of fields that exist in one representation but not the other. The adapter must decide how to handle lossy conversions — should unmapped fields be dropped, set to defaults, or raise errors?

Alternatively, you can use two separate adapter classes — `AtoBDapter` and `BtoAAdapter` — following the Single Responsibility Principle. This is cleaner when the two translation directions have different complexity or when different teams maintain each direction. The choice depends on whether the bidirectional translation is conceptually one concern (a reversible mapping) or two distinct concerns (two separate translations).

---

## Q80: How does the Proxy pattern interact with garbage collection in managed languages?

**A:** In garbage-collected languages, the proxy and the real subject are separate objects, each subject to garbage collection independently. The proxy must not prevent the real subject from being collected — if the proxy holds a strong reference to the real subject, the subject cannot be garbage-collected as long as the proxy is reachable.

Virtual Proxies that defer creation are particularly interesting. When the real object is created on first access, the proxy holds a reference to it. If the proxy is still alive, the real object stays alive too. For resources that should be released (database connections, file handles), the proxy should implement `AutoCloseable` or a destructor to release the resource when the proxy itself is no longer needed.

Weak references offer a solution: the proxy can hold a weak reference to the real subject, allowing the GC to collect it. If the subject is collected, the proxy recreates it on the next access. This is useful for caching proxies where the cached object should be evictable. However, weak references add complexity around checking for null and race conditions in concurrent environments.

---

## Q81: What is a Decorator and how does it differ from the Proxy pattern?

**A:** A Decorator adds behavior to an object transparently, conforming to the same interface. Multiple decorators can be stacked to compose behavior. A Proxy controls access to an object — it may add behavior, but its primary purpose is access control, lazy initialization, logging, or similar cross-cutting concerns.

The structural difference is subtle but important: Decorators are designed to be stackable and transparent to the client. You can wrap a `Writer` in a `BufferedWriter` in a `LineNumberWriter` and the client sees only `Writer`. Proxies typically represent a single concern and are not designed for arbitrary stacking. A `CachingProxy` wraps the real subject once; you don't stack ten caching proxies.

The intent is the distinguishing factor. If you're adding incremental behavior (buffering, compression, encryption) and want the client to be unaware, use Decorator. If you're controlling access (authentication, lazy loading, reference counting) or mediating between client and subject, use Proxy. Both use the same structural pattern (wrapper implementing the same interface), but the design intent differs.

---

## Q82: How does the Facade pattern support microservices architecture?

**A:** In microservices, a Facade acts as an API Gateway or Backend-for-Frontend (BFF). Instead of the frontend calling five microservices directly, it calls the Facade, which orchestrates the calls and aggregates responses. This reduces round trips, simplifies client logic, and centralizes cross-cutting concerns.

The Facade (API Gateway) handles: **(1) Request routing** — mapping external URLs to internal service endpoints. **(2) Protocol translation** — converting external REST to internal gRPC. **(3) Authentication** — verifying tokens once instead of each microservice verifying independently. **(4) Response aggregation** — combining data from multiple services into a single response. **(5) Rate limiting and circuit breaking** — protecting backend services from overload.

The danger is that the Facade becomes a monolithic bottleneck. To prevent this, design the Facade as a thin orchestration layer with no business logic. Keep business rules in the microservices. The Facade only translates and routes. If the Facade starts accumulating business logic, it violates the Facade pattern's intent and creates a distributed monolith — the worst of both worlds.

---

## Q83: How do you handle versioning when an Adapter wraps an evolving external API?

**A:** Versioning adapters must accommodate API changes without breaking the consumer interface. The strategy is to version the adapter itself — `PaymentAdapterV1`, `PaymentAdapterV2` — each wrapping a different version of the external API. The consumer code depends on the adapter interface, not the version, so switching versions is a configuration change.

Another approach is to make the adapter handle multiple API versions internally. The adapter detects the API version (from response headers, for example) and translates accordingly. This is more complex but avoids creating separate adapter classes for each version. The adapter essentially contains version-specific translation logic behind a single interface.

For breaking changes in the external API, the recommended approach is **parallel running**: deploy the new adapter version alongside the old one, gradually migrate consumers, and decommission the old adapter. This follows the Strangler Fig pattern applied to adapters. Feature flags can control which adapter version each consumer uses, enabling safe rollouts and instant rollbacks.

---

## Q84: Can the Proxy pattern be used for transparent persistence (persistence by reachability)?

**A:** Yes. An ORM (Object-Relational Mapping) proxy can make persistent objects appear as ordinary in-memory objects. When you access a lazily-loaded collection on an entity, a proxy intercepts the access, queries the database, and returns the data. The application code never calls the database explicitly — persistence is transparent.

Hibernate's lazy loading is a classic example. When you load an `Order` entity, its `items` collection is not immediately fetched. Instead, Hibernate injects a proxy. When you call `order.getItems()`, the proxy fetches the items from the database on first access. The Order class has no persistence-specific code — the proxy handles it.

The challenges are: **(1) N+1 query problems** — each proxy access triggers a separate query, leading to performance issues. **(2) Detached objects** — when the session closes, accessing a proxy that hasn't been initialized throws an exception. **(3) Serialization** — proxies must be handled correctly during serialization (e.g., `Serializable` in Java, `__getstate__` in Python). Modern ORMs address these challenges with batch fetching, fetch joins, and proxy-aware serialization.

---

## Q85: What is the relationship between the Facade pattern and the concept of information hiding?

**A:** Information hiding is the principle that modules should hide implementation details and expose only what's necessary. The Facade pattern is the architectural embodiment of this principle at the subsystem level. The Facade hides the internal structure, dependencies, and complexity of a subsystem, exposing only the operations that clients need.

Parnas's original information hiding paper argues that modules should hide design decisions that are likely to change. The Facade achieves this for entire subsystems: when the internal implementation changes (different algorithms, different internal classes, different data structures), the Facade's interface remains stable. Clients depend on the Facade, not on the subsystem internals.

This has practical consequences: you can refactor, optimize, or replace subsystem internals without affecting any code outside the subsystem (only the Facade needs updating if the operations change). The Facade also prevents clients from creating hidden dependencies on subsystem internals — if the only way to use the subsystem is through the Facade, no client can accidentally depend on an internal class that might be removed.

---

## Q86: How does the Adapter pattern apply to database access layers?

**A:** Database adapters translate between a common interface (your DAO/repository interface) and specific database drivers. A `PostgresAdapter` implements your repository interface using PostgreSQL's JDBC driver; a `MongoAdapter` implements the same interface using the MongoDB driver. Switching databases means changing the adapter, not the application code.

This is the basis of the Repository pattern's portability. The application defines its data access operations as an interface. Each database adapter provides the implementation. Unit tests can use an in-memory adapter; production can use PostgreSQL; staging can use a containerized database. The adapter insulates the application from SQL dialect differences, connection management details, and result set mapping.

The challenge is the impedance mismatch between object models and relational models. Your domain objects have inheritance, value objects, and graph relationships. The database has tables, rows, and foreign keys. The adapter (or an ORM sitting behind the adapter) must map between these models. This mapping is non-trivial and varies by database, which is precisely why the adapter pattern is valuable — it encapsulates the database-specific mapping logic.

---

## Q87: When would you use a Composite Proxy instead of the Decorator pattern?

**A:** A Composite Proxy combines multiple proxy concerns (authentication, caching, logging, rate-limiting) into a single proxy object rather than stacking separate decorators. Use it when the proxy concerns interact — for example, when the caching logic needs to be aware of authentication (cache per user), or when logging must include cache hit/miss information.

The Decorator pattern stacks concerns independently: each decorator wraps the previous one without knowledge of others. This works well when concerns are orthogonal. But when concern A needs information from concern B, stacking breaks down — the decorators can't communicate with each other without reaching through the stack.

A Composite Proxy manages multiple concerns internally: `CompositeProxy` has methods for `checkAuth()`, `checkCache()`, `logAccess()`, and orchestrates them in the right order. This is a deliberate trade-off: you lose the Decorator's flexibility (can't mix and match at runtime) but gain the ability to express interdependent concerns. Use Composite Proxy for infrastructure concerns; use Decorator for business-layer behavior composition.

---

## Q88: How does the Facade pattern support event-driven architectures?

**A:** In event-driven architectures, a Facade can simplify event production. Instead of business classes directly constructing and publishing events (which couples them to the messaging infrastructure), they call a `DomainEventFacade` that handles event creation, serialization, and publishing. The business code publishes domain events through a simple method call; the facade handles Kafka topics, retry policies, and event schema versioning.

The Facade also simplifies event consumption. A `NotificationFacade` subscribes to multiple event streams, filters relevant events, and routes them to appropriate handlers. Without the facade, each handler would need its own subscription logic, filtering, and error handling. The facade centralizes this, ensuring consistent error handling and delivery guarantees.

The key benefit is decoupling: business classes don't know they're in an event-driven system. They raise domain events through the facade, and the infrastructure details (message broker choice, serialization format, delivery semantics) are hidden behind the facade. This makes it possible to switch from Kafka to RabbitMQ by changing only the facade implementation.

---

## Q89: How do you handle concurrency in Proxy implementations?

**A:** Concurrent proxy access requires careful synchronization. A caching proxy must handle simultaneous reads and writes to the cache: use a `ConcurrentHashMap` or read-write locks to prevent race conditions where one thread reads a partially-initialized cache entry while another thread is writing it.

A Virtual Proxy must handle the race condition where two threads simultaneously trigger lazy initialization. Without synchronization, both threads create the real object, and one instance is discarded (wasting resources) or worse, both are used (causing inconsistency). The **double-checked locking** pattern solves this: check if the object exists (first check, no lock), acquire the lock, check again (second check, with lock), then create if needed.

For high-throughput proxies, consider lock-free approaches: `AtomicReference` with CAS (compare-and-swap) operations, or thread-local caching where each thread has its own cache instance. The choice depends on the contention level: low contention favors simple synchronization; high contention favors lock-free or thread-local strategies. The proxy's performance overhead should be negligible compared to the real subject's execution time.

---

## Q90: What is the Remote Proxy and how does RMI use it?

**A:** A Remote Proxy represents an object that exists in a different process, machine, or network location. The proxy provides the same interface as the remote object but transparently handles network communication — serialization (marshalling), network transport, deserialization (unmarshalling), and error handling for network failures.

Java's RMI (Remote Method Invocation) implements the Remote Proxy pattern. When you call `registry.lookup("PaymentService")`, you receive a proxy (a stub) that implements the remote interface. Calling methods on the stub serializes the method name and arguments, sends them over the network to the remote JVM, executes the method on the actual object, and returns the serialized result.

Modern alternatives to RMI (gRPC, Thrift, REST) follow the same pattern but use different serialization protocols and transport layers. The Remote Proxy concept is universal: any RPC framework generates client-side proxies that hide network communication. The proxy must also handle network failures (retry, timeout, circuit breaking) and versioning (what if client and server have different interface versions?).

---

## Q91: How does the Adapter pattern enable legacy system integration?

**A:** Legacy systems often expose interfaces that are incompatible with modern APIs — proprietary protocols, fixed-width file formats, or SOAP XML. An adapter wraps the legacy interface behind a modern facade, allowing new code to interact with the legacy system through contemporary patterns (REST, JSON, event-driven).

The adapter translates between modern and legacy conventions: converting JSON payloads to XML, mapping new domain models to legacy flat-file records, or translating REST operations to legacy RPC calls. The legacy system continues operating unchanged; the adapter bridges the gap.

A common strategy is the **Anti-Corruption Layer (ACL)**, which is a more disciplined form of Adapter. The ACL not only translates interfaces but also prevents the legacy model from leaking into the new system. It maintains a clean domain model in the new system and translates to/from the legacy model at the boundary. This prevents the legacy system's design from corrupting the new system's domain model, which is critical when migrating away from a legacy system incrementally.

---

## Q92: What is a Transparent Proxy and where is it used in networking?

**A:** A Transparent Proxy intercepts network traffic without requiring client configuration. The client connects to the intended destination, but the network infrastructure (router, load balancer, firewall) redirects the traffic through the proxy. The client is unaware of the proxy's existence.

Common uses include: **(1) Caching proxies** (Squid) — cache web content to reduce bandwidth and latency. **(2) Content filtering** — corporate networks filter inappropriate content without configuring each browser. **(3) Load balancing** — distribute incoming traffic across multiple servers. **(4) SSL termination** — offload encryption/decryption from backend servers to a dedicated proxy.

Transparent proxies are implemented at the network layer (using iptables, NAT, or WCCP) rather than the application layer. The proxy intercepts packets, processes them, and forwards them to the actual destination. From the application's perspective, communication is direct. The challenge is that transparent proxies can break end-to-end assumptions — client IP addresses are hidden, HTTPS certificates may need inspection, and debugging becomes more complex because the proxy modifies traffic in flight.

---

## Q93: How does the Facade pattern help in managing cross-cutting concerns?

**A:** Cross-cutting concerns (logging, security, transaction management) affect multiple layers of an application. A Facade can encapsulate these concerns for a specific subsystem. Instead of every class in the subsystem managing its own logging, security checks, and transaction boundaries, the Facade coordinates them at the entry point.

This is a precursor to Aspect-Oriented Programming (AOP). Before AOP frameworks existed, Facades handled cross-cutting concerns by providing a single entry point where logging, security, and transactions were applied consistently. Many enterprise systems still use this approach, particularly in layered architectures where the service layer Facade handles all cross-cutting concerns before delegating to DAOs.

The limitation is that Facades only handle cross-cutting concerns at the subsystem boundary. Concerns that apply deep within the subsystem (e.g., audit logging on every database operation) still need AOP or decorator chains. But for entry-point concerns, the Facade approach is simpler and more transparent than AOP — there's no magic proxy generation or annotation processing; the cross-cutting logic is visible in the Facade's code.

---

## Q94: Can the Proxy pattern implement the Observer pattern for cache invalidation?

**A:** Yes. A Caching Proxy can implement Observer to invalidate cache entries when the underlying data changes. The proxy registers itself as an observer on the data source (or an event bus). When the data source emits a change event, the proxy invalidates or updates the relevant cache entry.

This approach solves a fundamental caching problem: stale data. Without invalidation, the cache serves outdated results. With Observer-based invalidation, the cache stays consistent with the source. The implementation requires mapping change events to cache keys — when the source says "order 42 updated," the proxy must know which cache key holds order 42 and invalidate it.

The challenge is granularity. If the event says "data changed" without specifying what changed, the proxy must invalidate all cache entries (conservative but correct) or use TTL-based expiration (probabilistically correct). If the event specifies exactly what changed, the proxy can do precise invalidation. The trade-off is between event verbosity (detailed events are expensive to generate and process) and cache precision (broad invalidation wastes cached data).

---

## Q95: What is the relationship between the Adapter pattern and the Liskov Substitution Principle?

**A:** LSP states that objects of a superclass should be replaceable with objects of its subclasses without altering program correctness. An Adapter creates an object that is substitutable for the target interface — the client can use the adapter anywhere the target interface is expected, and the behavior should be correct.

However, adapters can violate LSP if the translation is imperfect. If the adaptee's behavior differs from what the target interface's contract promises, the adapter produces subtly incorrect results. For example, if the target interface specifies that `compareTo()` is consistent with `equals()` but the adaptee's comparison is inconsistent, the adapter breaks LSP even though it compiles and runs.

A well-written adapter preserves the target interface's behavioral contract, not just its syntactic interface. This means the adapter may need to add validation, transformation, or error handling to ensure the adapted behavior matches the target interface's semantics. Testing should verify LSP compliance: replace the real implementation with the adapter in all existing tests and verify they pass unchanged.

---

## Q96: How does the Facade pattern interact with the Dependency Inversion Principle?

**A:** DIP states that high-level modules should not depend on low-level modules; both should depend on abstractions. A Facade is a high-level module that provides an abstraction over a subsystem. If other high-level modules depend on the Facade (the abstraction) rather than subsystem internals (concrete implementations), DIP is satisfied.

However, the Facade itself typically depends on concrete subsystem classes, which violates DIP at the Facade level. This is generally acceptable because the Facade's purpose is to be the one place that knows about subsystem internals. The DIP violation is localized and intentional — the Facade absorbs the dependency so that no other class needs it.

The key design decision is whether the Facade should be an interface or a concrete class. If you define `OrderFacade` as an interface with `RestOrderFacade` and `GraphQLOrderFacade` implementations, you satisfy DIP completely. This is useful when you might need to swap facade implementations (different API protocols). In most cases, a concrete Facade class is sufficient — the DIP benefit of abstraction is less important than the information-hiding benefit of the Facade.

---

## Q97: How does the Proxy pattern handle failure recovery?

**A:** A Resilience Proxy wraps the real subject and handles failures transparently. When the real subject throws an exception, the proxy catches it and applies recovery strategies: retry with exponential backoff, fall back to a cached or default response, or circuit-break (stop trying after repeated failures and return errors immediately).

The Retry Proxy is the simplest form: it catches transient exceptions (network timeouts, temporary unavailability) and retries the operation up to N times with increasing delays. The delay prevents overwhelming a recovering service. The proxy must distinguish transient failures (retryable) from permanent failures (not retryable) — retrying a `NullPointerException` is futile.

The Circuit Breaker Proxy tracks failure rates. When failures exceed a threshold, the circuit "opens" and subsequent calls fail immediately without reaching the real subject. After a timeout, the circuit enters "half-open" state — one test call is allowed through. If it succeeds, the circuit closes; if it fails, it reopens. This prevents cascading failures in distributed systems and gives failing services time to recover.

---

## Q98: How does the Adapter pattern work with generic/type-safe interfaces?

**A:** Generic adapters use type parameters to provide compile-time type safety while adapting between interfaces. A `ListAdapter<From, To>` takes a collection of `From` objects and returns a collection of `To` objects, with the conversion logic encapsulated in the adapter. The type parameters ensure that the correct types are used at each step, catching mismatches at compile time rather than runtime.

This is particularly useful when adapting between generic APIs. Consider adapting between `Repository<T, ID>` (your interface) and `CrudRepository<T, ID>` (Spring Data's interface). A generic adapter `SpringDataAdapter<T, ID, E>` maps between the two, with the entity mapping (`E`) as an additional type parameter. The generic adapter can be used for any entity type without creating separate adapter classes for each entity.

The challenge with generic adapters is type erasure (in Java) — the generic type information is lost at runtime. This affects serialization, reflection-based operations, and certain frameworks that rely on runtime type information. The workaround is to capture the generic type using `TypeToken` (Guava), `Class<T>` parameters, or `ParameterizedTypeReference` (Spring). These mechanisms preserve generic type information through the runtime, enabling the adapter to perform type-safe operations even after erasure.

---

## Q99: How do you document and communicate Adapter pattern decisions in a team?

**A:** Adapter documentation should focus on three areas: **(1) What is being adapted** — which interfaces are incompatible and why. **(2) Translation rules** — how data and behavior are mapped between the two interfaces, including lossy conversions and field mappings. **(3) Error handling** — how errors from the adaptee are translated into the target interface's error model.

Architecture Decision Records (ADRs) capture the rationale: "We chose to adapt X to Y because X is provided by an external vendor and cannot be modified. The adapter handles version differences between X v2 and our internal interface Z." This prevents future developers from wondering why the adapter exists and whether it can be removed.

The adapter itself should have comprehensive unit tests that document its behavior through examples. Each test case demonstrates a specific translation scenario: "When the external API returns status code 404, the adapter converts it to `NotFoundException`." These tests serve as living documentation of the adapter's translation rules, more reliable than written docs because they're always in sync with the code.

---

## Q100: How do all three patterns — Adapter, Facade, and Proxy — relate to each other and when do they overlap?

**A:** All three are structural patterns that use wrapper objects to achieve their goals, but their intents differ fundamentally. **Adapter** changes the interface of an existing object to match what a client expects. **Facade** provides a simplified interface to a complex subsystem. **Proxy** controls access to an object, adding a layer of indirection without changing the interface.

The overlap occurs in practice. A Proxy that simplifies access to a complex subsystem is also acting as a Facade. A Facade that translates between internal and external interfaces is also acting as an Adapter. The same class can simultaneously fulfill multiple pattern roles — the classification depends on the primary design intent and how the class is used.

The decision framework: if you need to make incompatible interfaces compatible → **Adapter**. If you need to simplify a complex subsystem for common use cases → **Facade**. If you need to control, monitor, or defer access to an object → **Proxy**. If you need multiple of these, combine them: an API Gateway (Facade) that translates protocols (Adapter) and adds caching (Proxy) handles all three concerns. The patterns compose naturally because they operate at different levels: interface translation (Adapter), subsystem simplification (Facade), and access control (Proxy).
