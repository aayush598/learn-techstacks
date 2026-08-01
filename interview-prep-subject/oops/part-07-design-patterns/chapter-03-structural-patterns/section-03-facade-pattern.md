# Facade Pattern

> **TL;DR**: The Facade pattern provides a **single, simplified interface to a complex subsystem** — it exists to reduce the *conceptual* and *coupling* cost of interacting with many interconnected classes, so clients call one door instead of navigating a maze of dependencies.

## 1. Why Does This Exist?
Complex subsystems — a compiler, a billing system, an ordering platform, an ML pipeline, an ORM — expose dozens of classes with *required* interdependencies. A client that must "compile a file" shouldn't have to know about `Lexer`, `Parser`, `SymbolTable`, `TypeChecker`, `IRBuilder`, `Optimizer`, and `CodeGen` and wire them in the right order with the right error handling. Two problems arise without a Facade:

1. **Coupling explosion**: each client references many subsystem classes; if the subsystem's internals change, every client must change.
2. **Conceptual overload**: clients must understand the *whole* subsystem to use even one feature.

The Facade pattern exists to give clients a **simple entry point** (`Compiler.compile("foo.c")`) that internally orchestrates the subsystem. It reduces coupling (clients depend on the facade, not the internals), reduces learning cost, and centralizes the subsystem's choreography and error handling in one place. It doesn't *hide* the subsystem — power users can still use the internals — but it makes the *common path* trivial.

## 2. How Does It Work?
```
Client ──uses──> Facade ──orchestrates──> Subsystem classes
   (knows only the       Lexer, Parser, SymbolTable,
    Facade's API)         TypeChecker, CodeGen ...
```
Participants:
1. **Facade** — a class with a few *high-level* methods (`compile(source)`, `billingCharge(cart)`). It holds references to subsystem classes and sequences them.
2. **Subsystem classes** — the complex machinery (each remains independent, unaware of the facade).
3. **Client** — calls only the facade's methods.

```java
class Compiler {                     // Facade
    private final Lexer lexer = new Lexer();
    private final Parser parser = new Parser();
    private final Optimizer opt = new Optimizer();
    private final CodeGen gen = new CodeGen();
    public byte[] compile(String source) {
        var tokens = lexer.tokenize(source);
        var ast = parser.parse(tokens);
        var checked = new TypeChecker().check(ast);
        var ir = opt.optimize(checked);
        return gen.emit(ir);
    }
}
```
The client calls `new Compiler().compile("int main(){}")` — one line instead of five wiring steps. Subsystem classes are untouched; the facade is *optional* (you can bypass it for advanced use).

## 3. When Is It Used?
- **Providing a simple interface to a complex subsystem** (compilers, image processing, payment orchestration, ML inference).
- **Reducing coupling between client code and library internals** — especially for third-party libraries with deep APIs.
- **As a *layer* or *boundary* in layered architectures** (the service layer is a facade over repositories + domain logic; `ApplicationContext` is a facade over bean creation/wiring).
- **Centralizing subsystem choreography**: transaction handling, ordering of operations, error aggregation.
- **In interviews**: "expose a simple API over a messy system", "client shouldn't know the internals" → Facade.

## 4. Why Wasn't Another Approach Chosen?
- **Let clients use the subsystem directly**: rejected when subsystem knowledge is high-cost, when coupling must be minimized, or when the common path is intricate (risk of each client wiring it wrong — bugs in N places instead of 1).
- **A new *layer* of classes replicating the subsystem (an "intermediary" per class)**: rejected — more objects, more indirection, no simplification; the facade's job is *fewer* entry points, not more.
- **Adapter**: rejected — the adapter converts *one interface* for *compatibility*; the facade provides a *new, simpler* interface over *a whole subsystem*. Adapter = convert; Facade = simplify/hide.
- **Mediator**: superficially similar (both centralize), but Mediator centralizes *communication between peer objects* (they talk through it), while Facade centralizes *access to a subsystem from outside*. Mediator is behavioral; Facade is structural. Facade points *inward* to a subsystem; Mediator sits *between* peers.
- **Proxy**: rejected — proxy keeps the *same* interface to *one* object and controls access; facade offers a *different, simplified* interface to *many* objects.
- **Refactoring the subsystem to be simpler**: the ideal long-term fix, but expensive and out of scope when you don't own it (third-party) or when the complexity is inherent (a compiler is genuinely complex). Facade is the pragmatic wrapper.

## 5. Intuition
A facade is the **front desk / customer service** of a building. You don't walk into a hospital and navigate directly to the cardiology scanner, the blood lab, and the billing office in the right sequence with the right forms. You go to *reception*, say "I need a health check," and reception orchestrates everything — appointments, labs, records — behind one counter. You could, if you're a specialist, go directly to a department (bypass the facade for advanced cases), but the normal path is one door.

## 6. Real-World Analogy
A **restaurant menu (the front-of-house) vs the kitchen**. Customers (clients) don't enter the kitchen and coordinate the pantry, the grill, the pastry station, and the dishwasher. The menu + waiter (facade) is the simple interface: "a steak medium-rare" → the waiter (facade) tells the kitchen (subsystem) to orchestrate grill + sides + plating. Customers never see the kitchen's machinery; power users (the chef) can go backstage. The menu is the *simplified interface*; the kitchen is the *subsystem*; the waiter/front desk is the facade.

## 7. Formal Definition
> **Facade**: Provide a **unified interface** to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem **easier to use**. (GoF, p. 185)
>
> Participants: **Facade** (knows which subsystem classes are responsible for a request; delegates client requests appropriately), **Subsystem classes** (implement subsystem functionality; they don't know the facade — no back-references), **Client** (uses the Facade instead of subsystem classes directly).

## 8. Example
A **shopping checkout facade** over an ordering subsystem (`InventoryService`, `PaymentGateway`, `ShippingService`, `NotificationService`):
```java
class CheckoutFacade {                      // Facade
    private final InventoryService inventory = new InventoryService();
    private final PaymentGateway payments = new PaymentGateway();
    private final ShippingService shipping = new ShippingService();
    private final NotificationService notif = new NotificationService();

    public Order checkout(Cart cart, PaymentInfo payment) {
        for (Item i : cart.items()) if (!inventory.reserve(i)) throw new OutOfStockException(i);
        PaymentResult pr = payments.charge(payment, cart.total());
        if (!pr.ok()) throw new PaymentFailedException(pr.message());
        Order order = shipping.createOrder(cart, pr.transactionId());
        notif.confirm(order);
        return order;
    }
}
```
- **Client code**: `new CheckoutFacade().checkout(cart, payment)` — one call.
- **Without the facade**: the client would sequence reserve → charge → ship → notify, handle `OutOfStockException`, `PaymentFailedException`, and transaction rollback itself — repeating that logic at every call site (a bug factory).
- The facade centralizes the choreography and exception policy; subsystem classes remain independent.

## 9. Internal Working
1. The client obtains the facade (typically a single instance — facades are often singletons or injected beans).
2. The client calls a *high-level* facade method.
3. The facade, internally:
   a. Coordinates the subsystem classes in the correct order (sequence of calls).
   b. Translates between the client's domain objects and the subsystem's types.
   c. Aggregates errors: catches subsystem exceptions and converts them to one facade-level exception type (single error-handling point).
   d. Handles cross-cutting concerns: transactions (begin/commit/rollback around the sequence), logging, retries.
4. The facade returns a single result to the client.
5. Subsystem classes remain *unaware* of the facade — the dependency is one-directional (client → facade → subsystems), which is what makes the subsystem independently testable and the facade swappable.

**Why it works**: it trades "many client-to-subsystem couplings" for "one client-to-facade coupling". Coupling count drops from O(clients × subsystem-classes) to O(clients × 1) + O(1 × subsystem-classes).

## 10. Time Complexity
- **Facade call overhead**: O(1) — one extra method call + the subsystem's own work. The facade *orchestrates*, it doesn't add computation.
- **Orchestration cost**: O(k) where k = number of subsystem calls (e.g., reserve → charge → ship = O(3)), constant per workflow.
- **Coupling reduction (the real "complexity" story)**: naive coupling is O(C × S) (C clients × S subsystem classes); with a facade it's O(C + S) — the facade is the structural "edge reduction" that makes the system scalable to reason about.
- **No algorithmic change**: the subsystem's own Big-O is untouched; the facade adds only constant-factor indirection.

## 11. Advantages
- **Simplicity**: one door for common operations; clients don't need to understand the subsystem.
- **Loose coupling**: clients depend only on the facade; subsystem refactors don't ripple into clients.
- **Centralized choreography**: ordering, transactions, and error mapping in one place — fixes bugs in N places become fixes in 1.
- **Optional power-user access**: the subsystem is still reachable for advanced cases (the facade "doesn't forbid" direct use).
- **Layering enabler**: facades define clean boundaries between layers (service layer, BFF, API facade).
- **Testability**: clients are tested against the facade (easy to mock); the subsystem is tested independently.

## 12. Disadvantages
- **Facade can become a god object**: if it exposes too many methods, it bloats into a kitchen sink (a facade per *use case* mitigates this).
- **Hides subsystem flexibility**: clients may not discover useful advanced features hidden behind the simplified interface.
- **Extra indirection**: one more layer to trace when debugging; stack traces gain a facade frame.
- **Not a fix for a bad subsystem**: if the subsystem is badly designed, the facade only masks it — the complexity still exists behind the door.
- **Risk of bypassing**: teams can over-couple to the facade, or power users bypass it and reintroduce scattered subsystem knowledge.

## 13. Interview Questions
1. **Q: What is the Facade pattern?** A: A structural pattern providing a unified, simplified interface over a complex subsystem, so clients interact with one facade instead of many subsystem classes, reducing coupling and complexity.
2. **Q: What problem does it solve?** A: The coupling explosion and conceptual overload of using a multi-class subsystem directly (clients wiring N classes in the right order, each knowing the internals). Facade centralizes access and choreography.
3. **Q: Facade vs Adapter?** A: Adapter converts *one interface* for *compatibility* with a client's expected interface. Facade provides a *new, simpler interface* over a *whole subsystem* — simplification, not conversion. Adapter adapts a component; Facade fronts a subsystem.
4. **Q: Facade vs Proxy?** A: Proxy keeps the *same interface* to *one* object and controls access (lazy/security/remote). Facade offers a *different, simplified* interface to *many* objects. Proxy = same door, guarded; Facade = new, simpler door.
5. **Q: Facade vs Mediator?** A: Facade (structural) centralizes *external access to a subsystem* — one-directional, clients → facade → subsystem. Mediator (behavioral) centralizes *communication between peer objects* that talk through it — bidirectional, peers → mediator → peers. Facade points inward from outside; Mediator sits between colleagues.
6. **Q: Does the Facade hide the subsystem or remove it?** A: It *hides* it, not removes it. Subsystem classes remain available for advanced/power use; the facade only simplifies the common path. This is by design — a facade must not forbid direct subsystem use.
7. **Q: How does the facade handle errors? (Production)** A: It's the single point where subsystem exceptions are caught, logged, and translated into facade-level (domain) exceptions — so clients handle one exception model and cross-cutting retry/rollback lives in one place.
8. **Q: When is the facade actually harmful? (Tricky)** A: When it becomes a God Object (too many unrelated methods), when it hides capabilities users genuinely need (forcing bypasses), or when applied over a *simple* subsystem (indirection with no benefit). A facade is justified by subsystem *complexity*, not habit.
9. **Q: How do facades help layered architecture?** A: Each layer exposes a facade to the next (service layer as facade over repositories; controller as facade over services; API gateway as facade over microservices). Facades are the seam that makes layers replaceable and independently testable.
10. **Q: Name a real-world JDK/framework facade.** A: `javax.faces` `FacesContext`, `Spring`'s `ApplicationContext` (facade over bean creation/wiring/events), `JdbcTemplate` (facade over Connection/Statement/ResultSet + exception translation), `java.net.URL` (facade over protocol handlers), `java.util.logging.LogManager`.
11. **Q: Is Spring's `ApplicationContext` a facade, factory, or both? (Scenario)** A: Both — it's a *factory* (it creates beans) and a *facade* (it exposes a unified interface over the whole bean lifecycle, event publishing, resource loading, and environment). Patterns compose; naming both is the senior answer.
12. **Q: Can you have multiple facades over one subsystem?** A: Yes — one facade per *use case* or per *client type* (a `UserFacingApi`, an `AdminApi`, an `InternalToolingApi` over the same services). This prevents the God-Object facade and lets different clients see different simplified views.
13. **Q: What does "the facade is the front desk" mean structurally?** A: All client requests route through the facade (one door), the facade knows who to delegate to, and the subsystem doesn't know the facade exists (no back-reference) — a one-directional dependency. This keeps the subsystem reusable and the facade swappable.
14. **Q: Facade vs a plain helper/utility method?** A: A utility method is stateless and often procedural; a facade is an *object* that can hold subsystem references, state (a session, a config), and lifecycle (transactions). Facades scale to complex orchestration; helpers fit one-shot conveniences. For a tiny subsystem, a helper suffices — for a subsystem, a facade.
15. **Q: How do facades interact with DI containers? (Production)** A: The facade is typically a *singleton bean* in the container, constructed with the subsystem beans injected (constructor injection) — the container wires the facade's dependencies, and the facade becomes the app-facing boundary of that subsystem.
16. **Q: Can a facade be part of a larger pattern (e.g., layered with a proxy)?** A: Yes — an API gateway (facade over microservices) is usually fronted by proxies (routing, auth); a facade may be *behind* a proxy (proxy guards access to the facade). Patterns compose: proxy for access control, facade for simplification.
17. **Q: How do you keep a facade from leaking subsystem types?** A: Define facade-level types (DTOs, domain models) and translate at the facade boundary; never return `Lexer.Token` or `SubsystemX.Config` from a facade method, or the simplification leaks. This "boundary translation" is a key production practice.
18. **Q: What is a "BFF" (Backend for Frontend) and how does it relate to Facade? (Tricky)** A: A BFF is a facade *per client type* (one API for mobile, one for web) that aggregates/orchestrates backend services into a shape each client needs — the facade pattern applied at the network/API level. It's the modern distributed-systems facade.
19. **Q: When is bypassing the facade justified? (Production)** A: For advanced/rare operations not worth simplifying, for performance-sensitive paths that need direct subsystem control, or for subsystem-specific tooling. By-pass must be deliberate and documented; the default path is the facade.
20. **Q: Design a facade for an image-processing subsystem (resize, filter, watermark, save). (Scenario)** A: `ImageProcessor` (facade) with methods `resize(path, dims)`, `applyFilter(path, filter)`, `watermark(path, text)`, `save(img, format, path)` — internally orchestrating `ImageDecoder`, `ResizeEngine`, `FilterRegistry`, `WatermarkPainter`, `ImageEncoder`. Clients call one class; adding a pipeline feature = adding a facade method, not teaching clients the subsystem.

## 14. Follow-Up Questions
1. **Q: Facade vs "Adapter that wraps many classes"?** A: A multi-adaptee adapter *still converts interfaces for compatibility* (retrofit); a facade *creates a new simpler interface* for a subsystem (simplification). The discriminator is intent: compatibility/conversion vs simplification/hiding.
2. **Q: What's the relationship between Facade and "Law of Demeter"?** A: Facade *enforces* the Law of Demeter: clients talk only to the facade (their "friend"), never to the subsystem's internals. It's the structural mechanism that makes the law practical.
3. **Q: How does a facade relate to single responsibility?** A: A *good* facade has one responsibility (orchestrating one subsystem's common path); a facade with many unrelated methods violates SRP and becomes a God Object. Use multiple focused facades instead.
4. **Q: Can a subsystem have a facade AND a decorator?** A: Yes — decorate the *facade* (add caching, logging, or instrumentation around facade calls) without touching the subsystem. Cross-cutting concerns often live on the facade precisely because it's the single door.
5. **Q: What's the difference between a facade and a "facade pattern in microservices" (API gateway)?** A: Same idea at different scales: a local facade simplifies in-process subsystem access; an API gateway is the *distributed* facade that simplifies client access to many services (routing, aggregation, auth, rate limiting). Both reduce client coupling.

## 15. Coding Example
```java
// Facade over a video-conversion subsystem
class VideoFile { final String name; VideoFile(String n){ this.name=n; } }

class CodecFactory { Codec getCodec(String file) { return new Codec(); } }
class BitrateReader { void read(VideoFile f, Codec c) {} void convert(Buffer b, Codec c) {} }
class AudioMixer { Buffer fix(Buffer b) { return b; } }

// FACADE — the single door
class VideoConverter {
    private final CodecFactory codecFactory = new CodecFactory();
    private final BitrateReader bitrateReader = new BitrateReader();
    private final AudioMixer audioMixer = new AudioMixer();

    public VideoFile convert(String fileName, String targetFormat) {
        VideoFile file = new VideoFile(fileName);
        Codec sourceCodec = codecFactory.getCodec(fileName);
        Codec targetCodec = targetFormat.equals("mp4") ? new MPEG4Codec() : new OggCodec();
        Buffer buffer = bitrateReader.read(file, sourceCodec);
        Buffer result = bitrateReader.convert(buffer, targetCodec);
        result = audioMixer.fix(result);
        return new VideoFile(fileName.replaceAll("\\.[^.]+$", "." + targetFormat));
    }
}

// CLIENT — one call, knows nothing about codecs/bitrates/mixers
public class Main {
    public static void main(String[] args) {
        VideoConverter converter = new VideoConverter();      // facade
        VideoFile out = converter.convert("home.mov", "mp4"); // one line!
        System.out.println("Saved " + out.name);
    }
}
class Codec {}
class MPEG4Codec extends Codec {}
class OggCodec extends Codec {}
class Buffer {}
```
```python
# Python Facade
class _Lexer:
    def tokenize(self, src: str) -> list: return list(src.split())
class _Parser:
    def parse(self, tokens: list) -> str: return "ast(" + "+".join(tokens) + ")"
class _CodeGen:
    def emit(self, ast: str) -> bytes: return ast.encode()

class Compiler:                    # Facade
    def __init__(self):
        self.lexer, self.parser, self.codegen = _Lexer(), _Parser(), _CodeGen()
    def compile(self, source: str) -> bytes:
        return self.codegen.emit(self.parser.parse(self.lexer.tokenize(source)))

print(Compiler().compile("int main(){}"))   # b'ast(int+main(){})'
```
```cpp
// C++ Facade
#include <iostream>
#include <string>

struct Lexer  { std::string run(const std::string& s) const { return "tokens<" + s + ">"; } };
struct Parser { std::string run(const std::string& t) const { return "ast(" + t + ")"; } };
struct CodeGen { std::string run(const std::string& a) const { return "code[" + a + "]"; } };

class Compiler {                       // Facade
    Lexer lexer_; Parser parser_; CodeGen codegen_;
public:
    std::string compile(const std::string& source) const {
        return codegen_.run(parser_.run(lexer_.run(source)));
    }
};
// int main(){ Compiler c; std::cout << c.compile("int main(){}") << "\n"; }
```

## 16. Industry Usage
- **JDK**: `java.net.URL` (facade over protocol handlers/streams), `JdbcTemplate` in Spring (facade over Connection/Statement/ResultSet + exception translation), `java.util.logging.Logger` (facade over handlers/formatters), `javax.faces.FacesContext`.
- **Spring**: `ApplicationContext` is the quintessential production facade — one object exposing bean access, events, resource loading, environment, and lifecycle; `JdbcTemplate`/`RestTemplate` are facades over JDBC/HTTP internals with error translation.
- **Hibernate/JPA**: `EntityManager` is a facade over the session/transaction/query machinery (persistence context, first-level cache, flush).
- **Microservices/APIs**: API Gateways (Kong, Spring Cloud Gateway, AWS API Gateway) are distributed facades aggregating services for clients.
- **BFF (Backend for Frontend)**: per-client-type facades (mobile API vs web API) shaping backend responses — a facade pattern in distributed form.
- **Games/UI**: `SceneManager`, `GameManager` facades over renderer/audio/input subsystems; `System` facades in operating systems (POSIX functions are facades over kernel internals).
- **Interviews**: "expose a simple API over a complex system", "reduce coupling to a library", "design a facade over a payment/image-processing subsystem" — common LLD scenarios; the adapter/proxy/facade/mediator discriminator is a favorite.

## 17. References
- **Gamma et al., *Design Patterns* — "Facade" (p. 185)**: canonical definition, "knowing which subsystem classes are responsible".
- **Oracle Docs: `java.net.URL`, `java.util.logging.Logger`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Reference: `ApplicationContext`, `JdbcTemplate`** — https://docs.spring.io/spring-framework/reference/
- **Hibernate Docs: `EntityManager`** — https://hibernate.org/orm/documentation/
- **Sam Newman, *Building Microservices* — "API Gateway" chapter**: the distributed facade.
- **refactoring.guru — "Facade"** — modern diagrams and Java/C++/Python examples.
- **Baeldung — "Facade Pattern in Java"** — tutorial and layered-architecture usage.

## 18. Cheat Sheet
- Facade = **unified, simplified interface over a complex subsystem**; clients call one door.
- Participants: Facade (orchestrates), Subsystem classes (unaware of facade), Client (knows only facade).
- One-directional dependency: client → facade → subsystem. No back-references.
- **Facade vs Adapter**: adapter converts one interface (compatibility); facade simplifies a subsystem.
- **Facade vs Proxy**: proxy keeps the same interface, controls access to one object; facade changes/ simplifies the interface to many objects.
- **Facade vs Mediator**: facade centralizes external access (structural); mediator centralizes peer communication (behavioral).
- The facade must NOT leak subsystem types — translate at the boundary (DTOs/domain types).
- Multiple facades per subsystem (one per use case) prevents the God-Object facade.
- Facades are often singletons/DI beans; JdbcTemplate, ApplicationContext, EntityManager are production facades.
- Facade centralizes error translation, transactions, retries, and logging — fixes in N places become fixes in 1.

## 19. Quiz
1. Facade provides: a) an adapted interface b) a unified simplified interface to a subsystem c) access control d) behavior addition → **b**
2. Which statement is true of the subsystem under a facade? a) it's removed b) it stays available for power users c) it becomes private d) it's copied → **b**
3. Facade vs Mediator: a) both structural b) facade structural, mediator behavioral c) both behavioral d) both creational → **b**
4. Which wrapper CHANGES the interface for simplification? a) Proxy b) Decorator c) Facade d) Adapter(compat) → **c**
5. The facade's dependency direction is: a) bidirectional b) client → facade → subsystem (one-directional) c) subsystem → facade → client d) none → **b**
6. `JdbcTemplate` is best described as: a) adapter b) facade over JDBC internals c) proxy d) decorator → **b**
7. A facade becomes a problem when it: a) is used by many clients b) becomes a God Object with too many unrelated methods c) is a singleton d) wraps one class → **b**
8. What must a facade avoid leaking? a) exceptions b) subsystem concrete types c) performance d) methods → **b**
9. An API Gateway in microservices is a: a) distributed facade b) decorator c) singleton d) composite → **a**
10. "Law of Demeter" is practically enforced by: a) Adapter b) Facade c) Prototype d) Builder → **b**

## 20. Flashcards
- **Q: Facade intent?** → **A:** Provide a unified, simplified interface over a complex subsystem, reducing coupling and learning cost.
- **Q: Facade vs Adapter?** → **A:** Adapter converts one interface (compatibility); Facade simplifies a whole subsystem.
- **Q: Facade vs Proxy?** → **A:** Proxy keeps the same interface and controls access; Facade offers a new, simpler interface.
- **Q: Facade vs Mediator?** → **A:** Facade centralizes external access (structural); Mediator centralizes peer communication (behavioral).
- **Q: Dependency direction?** → **A:** One-way: client → facade → subsystem; subsystems don't know the facade.
- **Q: Can the subsystem be bypassed?** → **A:** Yes — power users may use it directly; the facade is optional simplification.
- **Q: Production facades?** → **A:** `ApplicationContext`, `JdbcTemplate`, `EntityManager`, API gateways, BFFs.
- **Q: The facade trap?** → **A:** God-Object facade; fix by one facade per use case and never leaking subsystem types.

## 21. Revision
Facade gives a **unified simplified interface over a complex subsystem** — clients call one door instead of wiring many subsystem classes. It exists to cut coupling (from O(C×S) to O(C+S)), cut learning cost, and centralize choreography, transactions, and error translation in one class. Structurally one-directional: client → facade → subsystem (subsystem classes never know the facade and remain usable by power users). Discriminate the wrappers: Adapter converts one interface (compatibility); Proxy keeps the same interface and controls access; Mediator centralizes *peer* communication (behavioral); Facade simplifies a *subsystem* (structural). Production facades: Spring `ApplicationContext`/`JdbcTemplate`, Hibernate `EntityManager`, `java.net.URL`, API Gateways and BFFs in distributed systems. Best practice: never leak subsystem types through the facade (translate to domain types at the boundary), keep one facade per use case (avoid God-Object), and let cross-cutting concerns (logging, caching, retries) live on the facade. Interview hook: "expose a simple API over a complex system" → Facade.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Facade pattern?" | 2 How / 7 Formal Definition |
| "What problem does it solve?" | 1 Why / 9 Internal Working |
| "Facade vs Adapter / Proxy / Mediator?" | 13 Q3–Q5 / 14 Q1 |
| "Does the facade hide or remove the subsystem?" | 13 Q6 / 14 Q2 |
| "How do facades help layered architecture?" | 13 Q9 / 16 Industry Usage |
| "Spring/JDBC facade examples?" | 13 Q10 / 13 Q11 / 16 Industry Usage |
| "When is a facade harmful?" | 13 Q8 / 14 Q3 |
| "What is a BFF / API gateway?" | 13 Q18 / 16 Industry Usage |
| "Design a facade over X subsystem (scenario)." | 13 Q20 / 15 Coding Example |
| "How does the facade handle errors?" | 13 Q7 / 18 Cheat Sheet |
