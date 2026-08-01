# Adapter Pattern

> **TL;DR**: The Adapter pattern **converts the interface of one class into the interface a client expects** — a "translator" that lets incompatible interfaces collaborate — and it exists because real systems are built from third-party and legacy components whose interfaces you cannot (or must not) change.

## 1. Why Does This Exist?
Integration is the rule in production, not the exception: you buy a third-party payment SDK whose API is `charge(int cents, String token)`, but your domain logic calls `processPayment(PaymentRequest)`; you replace a legacy `CSVReader` with a new `JSONReader` but 40 call sites depend on `CSVReader`'s exact methods; you consume a vendor's REST client that returns XML while your team standardized on JSON. In all three cases the *functionality* is right but the *interface* doesn't match your expectation. You usually **cannot modify the foreign component** (no source, must not diverge from upstream, third-party license), and rewriting all call sites is risky and repetitive.

The Adapter pattern exists to make two interfaces work together **without modifying either side**: you insert a middle object (the adapter) that implements *your* expected interface and, behind it, translates every call to the *adaptee's* interface. The client keeps programming to its own interface; the adaptee keeps its API; only the adapter knows about both — so the integration cost is isolated in exactly one class, and swapping the underlying component later means swapping only the adapter.

## 2. How Does It Work?
The Adapter has a classic two-variant structure:

**Object Adapter (composition — the modern, preferred form):**
```
Client ──uses──> Target (interface: request())
                      ▲
                      │ implements
                 Adapter  ──wraps──> Adaptee (specificRequest())
```
- `Target` = the interface the client already expects.
- `Adaptee` = the incompatible component you're integrating.
- `Adapter` implements `Target`, holds a reference to an `Adaptee`, and forwards/translates each `Target` method call into one or more `Adaptee` calls.

```java
// Client expects a "Target"
interface Target { void request(); }
// Foreign/legacy component we cannot change
class Adaptee { public void specificRequest() { System.out.println("adaptee's specific request"); } }
// Adapter translates
class Adapter implements Target {
    private final Adaptee adaptee;
    Adapter(Adaptee a) { this.adaptee = a; }
    public void request() { adaptee.specificRequest(); }   // translation
}
```

**Class Adapter (inheritance — needs multiple inheritance, rare in Java):**
`Adapter extends Adaptee implements Target` — the adapter *is* a subclass of the adaptee and implements the target interface, overriding/forwarding as needed. It adapts only one concrete adaptee (no dynamic dispatch to adaptee subclasses) and couples via inheritance.

The core "mechanism" is **translation with delegation**: the adapter never implements logic, it *forwards* — often changing method names, argument shapes, return types, or combining several adaptee calls into one target call.

## 3. When Is It Used?
- **Integrating third-party libraries** whose API doesn't match your domain interfaces (payment, SMS, maps, cloud SDKs).
- **Legacy system migration**: you keep old interfaces while slowly replacing implementations behind them.
- **Unifying multiple similar but incompatible components** behind one interface (one adapter per vendor) so clients are vendor-agnostic.
- **Readability and domain isolation**: hide an awkward API (method names like `execute2(int, String, boolean)`) behind a clean domain method.
- **Testing**: wrap a heavyweight component behind a Target interface so you can swap in a fake.
- **In interviews**: "the client expects interface X but we have class Y" → Adapter is the reflex.

## 4. Why Wasn't Another Approach Chosen?
- **Modify the Adaptee**: rejected when you don't own the source (third-party SDK, vendor library, upstream project you must not fork) or when the change would ripple across all users of the adaptee. The adapter keeps the adaptee pristine.
- **Modify the client to use the adaptee's interface directly**: rejected because many call sites would change, coupling them to the foreign API, and you'd repeat the translation logic everywhere (a "shotgun surgery" code smell).
- **Refactor the whole system to a common interface**: the right long-term fix, but expensive and risky mid-project; the adapter is the *incremental* bridge that lets you refactor later without a big bang.
- **A wrapper that is really a Decorator**: tempting — but the Decorator adds behavior *through the same interface*; the Adapter *changes the interface*. Using a decorator shape when interfaces differ is a category error (see Section 13/14).
- **Copy-paste the adaptee's logic**: rejected — duplicate code, no single integration point, no swap-out capability.
- **Class Adapter vs Object Adapter**: class adapter (inheritance) is chosen when you need to override adaptee behavior or when only one adaptee class exists; object adapter (composition) wins in general — it adapts any adaptee *subclass*, doesn't need multiple inheritance, and follows composition-over-inheritance. This is why object adapters dominate production code.

## 5. Intuition
An adapter is a **travel power adapter** — the *universal translator* for sockets. Your laptop (client) expects a three-pin outlet (Target interface); the hotel in another country provides a two-pin round socket (Adaptee). You don't rewire the hotel (can't modify the adaptee) and you don't rebuild your laptop's plug (won't modify the client). You buy a tiny adapter that *plugs into the hotel socket on one side* and *offers your laptop's plug shape on the other* — exactly the adapter's two interfaces — and it passes the electricity (the data) through with translation.

## 6. Real-World Analogy
A **simultaneous interpreter at a UN meeting**. A Japanese delegate (adaptee) speaks Japanese (specificRequest); the English-speaking audience (client) expects English (request()). Nobody rewrites the delegate's speech and nobody makes the audience learn Japanese; the interpreter (adapter) listens in Japanese and speaks English, preserving meaning — sometimes combining several Japanese sentences into one English statement (multi-call translation). The interpreter is the only person who knows both languages — the only component that knows both interfaces.

## 7. Formal Definition
> **Adapter** (a.k.a. **Wrapper**): Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces. (GoF, p. 139)
>
> Participants: **Target** (the interface clients use), **Client** (collaborates with Target), **Adaptee** (the incompatible interface being adapted), **Adapter** (converts Adaptee's interface to Target). Variants: *object adapter* (composition) and *class adapter* (inheritance/multiple inheritance).

## 8. Example
You're building a system whose domain expects `PaymentProcessor.process(Amount)`; you must integrate a legacy `StripeSDK` that only exposes `charge(long cents, Map<String,String> metadata)`:
```java
// Target — what your whole app programs to
interface PaymentProcessor {
    PaymentResult process(double amount);
}
// Adaptee — third-party, cannot change
class StripeSDK {
    public boolean charge(long cents, Map<String, String> metadata) { /* HTTP call */ return true; }
}
// Adapter — the translator
class StripeAdapter implements PaymentProcessor {
    private final StripeSDK stripe;
    StripeAdapter(StripeSDK s) { this.stripe = s; }
    public PaymentResult process(double amount) {
        long cents = Math.round(amount * 100);            // translation: dollars→cents
        Map<String, String> meta = Map.of("source", "web"); // translation: build metadata
        boolean ok = stripe.charge(cents, meta);           // delegation
        return new PaymentResult(ok);                      // translation: adaptee type → target type
    }
}
```
- The whole app calls `process(2_500.00)`; nobody knows about `StripeSDK`.
- Swapping to PayPal = write `PayPalAdapter implements PaymentProcessor`; **zero client changes** (Open-Closed).

## 9. Internal Working
1. The client holds a reference typed as `Target` (injected via constructor/DI).
2. At runtime, the injected instance is actually the `Adapter`.
3. When the client calls `target.request()`:
   a. **Dynamic dispatch** resolves to `Adapter.request()` (the adapter implements Target).
   b. The adapter executes *translation*: mapping arguments (dollar→cent, domain object→vendor params), possibly combining several calls, and mapping the adaptee's result back to the target's return type.
   c. The adapter invokes `adaptee.specificRequest()` (delegation — the only class that knows the adaptee).
4. The result flows back through the adapter to the client — the client never sees the adaptee's types.
5. Failure translation: the adapter also converts the adaptee's exceptions into domain exceptions (a key production responsibility — wrapping third-party errors so callers handle one exception type).

Internally, object adapters are trivial (one delegate + a few translation methods) but *architecturally* load-bearing: they are the single seam through which foreign code enters the system, so they're where you put logging, retries, and error mapping.

## 10. Time Complexity
- **Each adapted call**: O(1) — one delegation + translation (argument conversion), plus whatever the adaptee does. The adapter adds a constant factor (one extra call frame, one interface dispatch).
- **Combined calls** (target method → multiple adaptee calls): O(k) where k = number of adaptee calls, still constant per use case.
- **No effect on the algorithm's Big-O** — the adapter only relocates where calls happen; the adaptee's own complexity (e.g., O(1) `charge()`) is unchanged.
- **Class-count cost**: O(1) adapter class per adaptee — linear in the number of integrated components.

## 11. Advantages
- **Single integration point**: all foreign-interface knowledge lives in one adapter class — readable, testable, swappable.
- **Open-Closed**: adding a new vendor = adding a new adapter; clients never change.
- **No modification of foreign code**: works with third-party/legacy components you don't control.
- **Client purity**: clients keep programming to their own domain interface.
- **Centralized cross-cutting translation**: error mapping, retries, and logging can be added in the adapter only.
- **Supports incremental migration**: adapters let you modernize a system one component at a time.

## 12. Disadvantages
- **Extra layer of indirection**: one more class + call hop; can obscure "what actually happens" when debugging.
- **Only fixes the *interface*, not the *semantics***: if the adaptee behaves differently (e.g., returns inconsistent results), the adapter can't fix it — a translated bug is still a bug.
- **Adapter proliferation**: one class per vendor/component; with many integrations you get many thin classes (mitigate by making adapters uniform via a common interface).
- **Over-adapter anti-pattern**: adapting an interface that is *almost* fine adds needless indirection (YAGNI).
- **Class adapter coupling**: the inheritance variant couples to a concrete adaptee and may not be applicable in single-inheritance languages.

## 13. Interview Questions
1. **Q: What is the Adapter pattern?** A: Convert the interface of a class into the interface clients expect, so incompatible classes can cooperate — the adapter implements the target interface and delegates to the adaptee, translating calls.
2. **Q: What problem does it solve?** A: Integrating components whose interfaces don't match (third-party SDKs, legacy code) without modifying either side — isolating translation logic in one class and keeping clients coupled only to their own interface.
3. **Q: Object adapter vs class adapter?** A: Object adapter uses composition (holds an adaptee reference, implements target) — works with adaptee subclasses, no multiple inheritance needed, preferred. Class adapter uses inheritance (adapter extends adaptee, implements target) — adapts only one concrete class, needs multiple inheritance in Java (interfaces make it possible but rare).
4. **Q: "Given a `MediaPlayer` playing mp3 and an `AdvancedMediaPlayer` playing vlc/mp4" — which pattern, and why?** A: The classic example is Adapter: the client (`MediaPlayer`) expects `play(audioType, file)`, the `AdvancedMediaPlayer` has incompatible methods (`playVlc`, `playMp4`), and an adapter implements `MediaPlayer` and forwards to the right `AdvancedMediaPlayer` method. It's Adapter because the *interfaces are incompatible*; it's not Decorator (no behavior added) or Proxy (no access control).
5. **Q: Adapter vs Decorator?** A: Adapter *changes the interface* (target ≠ adaptee) to make things compatible; Decorator *keeps the same interface* and adds behavior around the object. Adapter = compatibility; Decorator = augmentation.
6. **Q: Adapter vs Proxy?** A: Adapter translates an incompatible interface; Proxy keeps *the same interface* as the real subject and *controls access* (lazy init, security, remote). Adapter is about interface mismatch; Proxy is about access/indirection.
7. **Q: Adapter vs Facade?** A: Adapter adapts *one* interface to another for compatibility; Facade provides a *new simplified interface over a whole subsystem* — it's not about compatibility but about simplification and hiding. An adapter is per-component; a facade is per-subsystem.
8. **Q: When would you choose Adapter over refactoring the adaptee? (Production)** A: When you don't own the adaptee (third-party/vendor/upstream), when changing it would break many other consumers, or when you want to keep the integration swappable (vendor A → vendor B by swapping adapters). Refactor only when you control the component and its consumers.
9. **Q: How do you handle the adaptee's exceptions in an adapter? (Production)** A: The adapter is the single place to catch vendor exceptions and translate them to domain exceptions (`PaymentException`, `RetryableException`), preserving cause chaining. This is a core production responsibility — callers handle one exception model, not three vendors' models.
10. **Q: Name a real JDK/framework example of Adapter.** A: `java.util.Arrays.asList(...)` (array → List), `Collections.enumeration(...)` / `list(...)` (Enumeration ↔ Collection), `InputStreamReader`/`OutputStreamWriter` (byte streams → char streams — a genuine adapter), `java.util.concurrent.CallableAdapter` in `FutureTask` (Runnable → Callable), Spring's `HandlerAdapter` (various controller types → a uniform handler interface).
11. **Q: Can an adapter adapt multiple adaptees?** A: Yes — an adapter can hold several adaptees and combine them (e.g., an adapter that reads from two legacy readers and merges). The GoF calls composite adapters a natural extension; it's just delegation to multiple collaborators.
12. **Q: How does an adapter help testing?** A: By making the client depend on the Target interface, tests can inject a fake adapter (in-memory, deterministic) instead of the real vendor SDK — no network, no third-party credentials in tests.
13. **Q: What's the difference between adapting and wrapping? (Tricky)** A: In everyday speech they're synonyms, but in pattern terms: Adapter changes the interface for compatibility; Decorator (a "wrapper") keeps the interface and adds responsibilities; Proxy (a "wrapper") controls access. "Wrapper" is the umbrella; the specific intent distinguishes the pattern. Saying "it's just a wrapper" in an interview and failing to name the intent is the classic trap.
14. **Q: How would you integrate two similar but incompatible SDKs (payment + billing) behind one interface? (Scenario)** A: Define a common Target interface (`PaymentProcessor`), write one Adapter per SDK (`StripeAdapter`, `RazorpayAdapter`), inject the chosen adapter (config/DI), and ensure each adapter does its own translation + error mapping. Clients and the domain stay 100% SDK-agnostic.
15. **Q: What is the "Adapter at the boundary" architectural idea?** A: Adapters are the *port-adapter (hexagonal) architecture*: the domain depends on ports (interfaces); each external system connects through an adapter implementing the port. It isolates the domain from infrastructure (DBs, message brokers, third parties). This is the "ports and adapters" / hexagonal architecture popularized by Alistair Cockburn.
16. **Q: Adapter vs Bridge — both "decouple"? (Tricky)** A: Adapter makes *existing, incompatible* interfaces work together (retrofit). Bridge *separates an abstraction from its implementation* from the start so both can vary independently (forward-looking design). Adapter is a retrofit for incompatibility; Bridge is a deliberate decoupling of two variation axes.
17. **Q: Can you use an adapter to convert a class's *method signatures* without a new interface?** A: That's still an adapter — implementing the target interface is just the classic form; you can also provide a facade method on a wrapper. The pattern's essence is translation + delegation; the Target can be an existing interface you're implementing or simply the method shape callers expect.
18. **Q: Why is object adapter preferred over class adapter in most production code?** A: Because it adapts *any subclass of the adaptee*, needs no multiple inheritance, follows composition-over-inheritance, and avoids re-implementing adaptee internals. Class adapter is only useful when you must override adaptee behavior or adapt a *sealed* final class.
19. **Q: What does "the adapter is a facade for one object" mean? (Tricky)** A: Both are "translators/hiders", but a Facade hides a *subsystem* (many objects) with a new, simplified API; an Adapter hides *one object's* incompatible interface. Size + intent (simplify vs convert) separate them.
20. **Q: What's the risk of overusing adapters? (Production)** A: Adapter sprawl — hundreds of thin adapters that translate slightly-different APIs create indirection without benefit, and a *semantic* mismatch (the adaptee behaves differently than the target implies) is hidden behind a clean-looking interface. Use adapters at *true boundaries* (third-party, legacy) — not as a habit.

## 14. Follow-Up Questions
1. **Q: What is the difference between a "translator" adapter and a "converter" adapter?** A: A translator forwards calls one-to-one with argument mapping; a converter changes the *shape of the data* (dollars→cents, XML→JSON) as well as the interface. Most production adapters are both (mapping both signature and payload).
2. **Q: How does Adapter interact with Dependency Inversion?** A: The client depends on the Target *abstraction* (not the concrete adaptee) — exactly DIP. The adapter is the concrete binding between the abstraction and a foreign implementation, which is why adapters are frequently registered in DI containers.
3. **Q: Where does "Spring MVC" use HandlerAdapter?** A: Spring's `HandlerAdapter` is a genuine adapter: controllers can be `@Controller`, `Controller`, `HttpRequestHandler`, etc.; `DispatcherServlet` asks a `HandlerAdapter` to execute any handler type uniformly (`handler.handle(request,response)`), isolating the servlet from controller-shape variations.
4. **Q: Adapter vs Anti-Corruption Layer (DDD)?** A: The ACL is the *system-level* Adapter: it protects a bounded context from a foreign context's model by translating both data and semantics at the boundary. An Adapter is the local pattern; the ACL is the DDD architectural application of it.
5. **Q: Can an adapter be stateful?** A: Yes — adapters often hold a config, a session, a rate limiter, or a client object for the adaptee; they're typically singletons per vendor in the container (Spring beans). The translation logic is stateless, but the wrapped client is stateful.

## 15. Coding Example
```java
// Full object-adapter example: unify two incompatible SDKs behind one interface
// TARGET
interface PaymentProcessor {
    PaymentResult process(double amountUsd);
}
record PaymentResult(boolean ok, String provider) {}

// ADAPTEE 1 — legacy Stripe SDK (cannot modify)
class StripeSDK {
    public boolean charge(long cents, String currency, String customerId) {
        System.out.println("Stripe: charge " + cents + " " + currency + " for " + customerId);
        return true;
    }
}
// ADAPTEE 2 — PayPal SDK
class PayPalSDK {
    public boolean makePayment(double usd) {
        System.out.println("PayPal: charge $" + usd);
        return true;
    }
}

// ADAPTERS
class StripeAdapter implements PaymentProcessor {
    private final StripeSDK stripe;
    StripeAdapter(StripeSDK s) { this.stripe = s; }
    public PaymentResult process(double amountUsd) {
        long cents = Math.round(amountUsd * 100);
        boolean ok = stripe.charge(cents, "usd", "cust-123");
        return new PaymentResult(ok, "stripe");
    }
}
class PayPalAdapter implements PaymentProcessor {
    private final PayPalSDK paypal;
    PayPalAdapter(PayPalSDK p) { this.paypal = p; }
    public PaymentResult process(double amountUsd) {
        return new PaymentResult(paypal.makePayment(amountUsd), "paypal");
    }
}

// CLIENT — depends only on the Target interface
class CheckoutService {
    private final PaymentProcessor processor;
    CheckoutService(PaymentProcessor p) { this.processor = p; }   // injected adapter
    void pay(double amount) {
        PaymentResult r = processor.process(amount);
        System.out.println("result: " + r);
    }
}
// Wiring
new CheckoutService(new StripeAdapter(new StripeSDK())).pay(25.00);
new CheckoutService(new PayPalAdapter(new PayPalSDK())).pay(25.00);
// Switching vendors = one wiring change, zero client code changes.
```
```python
# Python Adapter (duck-typed target)
class PaymentProcessor:                # target "interface" (implicit)
    def process(self, amount_usd: float) -> dict: ...

class StripeSDK:                       # adaptee — cannot change
    def charge(self, cents: int, currency: str, customer_id: str) -> bool:
        print(f"Stripe charge {cents} {currency} for {customer_id}")
        return True

class StripeAdapter(PaymentProcessor): # adapter
    def __init__(self, sdk: StripeSDK): self._sdk = sdk
    def process(self, amount_usd: float) -> dict:
        ok = self._sdk.charge(round(amount_usd * 100), "usd", "cust-123")
        return {"ok": ok, "provider": "stripe"}

def checkout(processor: PaymentProcessor, amount: float) -> None:
    print(processor.process(amount))

checkout(StripeAdapter(StripeSDK()), 25.00)
```
```cpp
// C++ object adapter
#include <iostream>
#include <memory>
#include <string>

struct PaymentProcessor {                    // Target
    virtual ~PaymentProcessor() = default;
    virtual bool process(double amountUsd) = 0;
};
class StripeSDK {                            // Adaptee
public:
    bool charge(long cents, const std::string& currency, const std::string& cust) {
        std::cout << "Stripe charge " << cents << " " << currency << " for " << cust << "\n";
        return true;
    }
};
class StripeAdapter : public PaymentProcessor {   // Adapter (composition)
    StripeSDK& sdk_;
public:
    explicit StripeAdapter(StripeSDK& s) : sdk_(s) {}
    bool process(double amountUsd) override {
        return sdk_.charge(static_cast<long>(amountUsd * 100), "usd", "cust-123");
    }
};
// int main(){ StripeSDK sdk; CheckoutService svc(std::make_unique<StripeAdapter>(sdk)); svc.pay(25.0); }
```

## 16. Industry Usage
- **JDK**: `InputStreamReader`/`OutputStreamWriter` (byte→char adapter), `Arrays.asList`, `Collections.enumeration`/`list`, `CallableAdapter` inside `FutureTask`, `StringWriter`/`StringReader` bridging streams and strings.
- **Spring**: `HandlerAdapter` (uniformly execute heterogeneous controller types), `ServletContextInitializerBeans`/`BeanPostProcessor` adapters, `MethodInvokingFactoryBean` (method → bean), Spring Data's `Repository` adapters across DBs.
- **SLF4J**: the logger facade is an *adapter* over Log4j2/Logback/java.util.logging — one interface, pluggable backends.
- **Legacy modernization**: banks and airlines famously wrap 1980s COBOL/mainframe APIs behind modern interfaces with adapters while replacing subsystems incrementally.
- **Cloud SDKs**: AWS/Stripe/Twilio clients are wrapped behind domain interfaces at their boundary.
- **Hexagonal/ports-and-adapters**: the architectural pattern that makes Adapter the *boundary pattern* for all external integrations (databases, message brokers, third parties).
- **Interviews**: the "MediaPlayer/AdvancedMediaPlayer" question and its siblings are among the most common OOP interview questions ever — expect Adapter vs Decorator vs Proxy vs Facade as a *guaranteed* discriminator question.

## 17. References
- **Gamma et al., *Design Patterns* — "Adapter" (p. 139)**: class vs object adapter, participants, applicability.
- **Oracle Docs: `InputStreamReader`, `OutputStreamWriter`, `Arrays.asList`, `Collections.enumeration`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Docs: `HandlerAdapter`, MVC architecture** — https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html
- **refactoring.guru — "Adapter"** — modern diagrams and Java/C++/Python examples.
- **Alistair Cockburn, "Hexagonal Architecture" (ports & adapters, 2005)** — the architectural application of adapters at boundaries.
- **Eric Evans, *Domain-Driven Design* — "Anti-Corruption Layer"** — system-level adapter pattern.
- **Baeldung — "Adapter Pattern in Java"** — tutorial and comparison articles.

## 18. Cheat Sheet
- Adapter = **translate an incompatible interface to the one the client expects**; delegation + translation, no logic.
- Object adapter (composition): implements Target, wraps Adaptee — the standard; works with adaptee subclasses.
- Class adapter (inheritance): `extends Adaptee implements Target` — rare, needs multiple inheritance.
- Adapter changes the interface; **Decorator keeps the interface and adds behavior**; **Proxy keeps the interface and controls access**; **Facade hides a subsystem**.
- Never modify the adaptee or the client — the adapter is the single seam.
- Centralize error translation (vendor exceptions → domain exceptions) in the adapter.
- Examples: `InputStreamReader`, `Arrays.asList`, Spring `HandlerAdapter`, SLF4J.
- Use at true boundaries (third-party, legacy); avoid adapter sprawl inside your own domain.
- Adapter = retrofit for incompatibility; Bridge = deliberate decoupling of abstraction/implementation.
- Interview hook: "interface mismatch" → Adapter.

## 19. Quiz
1. The Adapter pattern's intent is to: a) add behavior b) convert one interface to another c) control access d) hide a subsystem → **b**
2. Which variant uses composition? a) class adapter b) object adapter c) both d) neither → **b**
3. Class adapter in Java typically requires: a) multiple inheritance via interfaces b) a static method c) reflection d) serialization → **a**
4. Adapter differs from Decorator because: a) decorator adds behavior, adapter changes interface b) adapter adds behavior c) they're identical d) decorator hides → **a**
5. `InputStreamReader` (byte→char) is an example of: a) Decorator b) Adapter c) Proxy d) Facade → **b**
6. Which wrapper keeps the SAME interface as the target? a) Adapter b) Decorator c) both d) neither → **b**
7. When can't you just modify the adaptee? a) when it's your own code b) third-party/vendor/legacy c) when interfaces match d) never → **b**
8. Spring's `HandlerAdapter` adapts: a) databases b) heterogeneous controller types to a uniform interface c) HTTP clients d) config files → **b**
9. The adapter should also translate: a) method names b) exceptions to domain types c) databases d) threads → **b**
10. Adapter vs Bridge: Adapter is ___; Bridge is ___. a) retrofit; deliberate decoupling b) deliberate; retrofit c) both retrofit d) both deliberate → **a**

## 20. Flashcards
- **Q: Adapter intent?** → **A:** Convert one interface to the one clients expect so incompatible classes can cooperate.
- **Q: Object vs class adapter?** → **A:** Object = composition (preferred); class = inheritance (needs multiple inheritance, rare).
- **Q: Adapter vs Decorator?** → **A:** Adapter changes the interface (compatibility); Decorator keeps it and adds behavior.
- **Q: Adapter vs Proxy?** → **A:** Adapter = interface translation; Proxy = same interface, controls access.
- **Q: Adapter vs Facade?** → **A:** Adapter adapts one object; Facade simplifies/hides a whole subsystem.
- **Q: Real-world adapters?** → **A:** `InputStreamReader`, `Arrays.asList`, Spring `HandlerAdapter`, SLF4J.
- **Q: What should the adapter centralize?** → **A:** Error/exception translation to domain exceptions.
- **Q: When to use an adapter?** → **A:** Integrating third-party/legacy components you can't modify, at true system boundaries.

## 21. Revision
Adapter **converts an incompatible interface into the one a client expects** via delegation + translation, letting third-party/legacy components integrate without modification. Two variants: object adapter (composition — holds the adaptee, implements the target; the standard) and class adapter (inheritance — extends the adaptee and implements the target; rare, needs multiple inheritance). It's a *retrofit for interface mismatch*: the adapter is the only class that knows both interfaces, and it should also centralize exception translation. Discriminate from the other wrappers: **Decorator** keeps the interface and adds behavior; **Proxy** keeps the interface and controls access; **Facade** hides an entire subsystem; **Bridge** is forward-looking decoupling of abstraction/implementation (Adapter is a retrofit). Real examples: `InputStreamReader`, `Arrays.asList`, Spring `HandlerAdapter`, SLF4J, hexagonal-architecture boundary adapters. Use adapters at true boundaries (third-party, legacy) — adapter sprawl inside your own domain is a smell. Interview hook: "interface mismatch" → Adapter; "add features" → Decorator; "control access" → Proxy; "hide complexity" → Facade.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Adapter pattern?" | 2 How / 7 Formal Definition |
| "Object vs class adapter?" | 2 How / 13 Q3 / 18 Cheat Sheet |
| "MediaPlayer / AdvancedMediaPlayer — which pattern?" | 13 Q4 / 16 Industry Usage |
| "Adapter vs Decorator / Proxy / Facade?" | 13 Q5–Q7 / 14 Q3 |
| "When can't you modify the adaptee?" | 13 Q8 / 4 Alternatives |
| "How to handle vendor exceptions?" | 13 Q9 / 18 Cheat Sheet |
| "JDK/Spring adapter examples?" | 13 Q10 / 16 Industry Usage |
| "Ports-and-adapters / hexagonal?" | 13 Q15 / 16 Industry Usage |
| "Adapter vs Bridge?" | 13 Q16 |
| "Risks of adapter overuse?" | 13 Q20 |
