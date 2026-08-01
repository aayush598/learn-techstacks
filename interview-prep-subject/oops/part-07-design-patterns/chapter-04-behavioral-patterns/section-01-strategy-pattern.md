# Strategy Pattern

> **TL;DR**: The Strategy pattern defines a **family of interchangeable algorithms**, encapsulates each behind a common interface, and lets a context **switch algorithms at run time** — it exists because conditional logic (`if/else if` or `switch`) for choosing an algorithm is rigid, non-testable, and violates Open-Closed.

## 1. Why Does This Exist?
Every system has "varying behavior": a payment service that can charge via card, UPI, or net-banking; a report that exports to PDF, Excel, or CSV; a navigation app that routes by fastest, shortest, or scenic; an image compressor with PNG/JPEG/WebP. The naive implementation is a **giant conditional**:
```java
void export(String format) {
    if (format.equals("PDF"))  { /* 50 lines */ }
    else if (format.equals("XLSX")) { /* 50 lines */ }
    else if (format.equals("CSV")) { /* 50 lines */ }
}
```
This fails in four ways: (1) **Open-Closed violation** — adding a format edits the class; (2) **SRP violation** — the class does export *and* knows every format; (3) **untestable** — you must set up every format to test the dispatcher; (4) **can't vary at run time** — the algorithm is baked into the method.

The Strategy pattern exists to **encapsulate each algorithm in its own class behind a common interface**, so the context delegates the choice to an injected `Strategy`. Adding a format = adding a class (Open-Closed). The algorithm is now independently testable, swappable at run time, and reusable across contexts. It's the direct, structural implementation of the Part-06 principles "encapsulate what varies" and "program to an interface".

## 2. How Does It Work?
```
Context ──uses──> Strategy (interface: algorithm())
                       ▲
        ┌──────────────┼──────────────┐
    ConcreteStrategyA  ConcreteStrategyB  ConcreteStrategyC
```
Participants:
1. **Strategy** — the interface declaring the algorithm.
2. **ConcreteStrategy** — one class per algorithm (each encapsulates the variant behavior).
3. **Context** — holds a `Strategy` reference (constructor-injected or setter-swapped) and delegates the algorithm call to it. The context knows only the interface.

```java
interface SortStrategy { void sort(int[] arr); }
class QuickSort implements SortStrategy { public void sort(int[] a){ /* quicksort */ } }
class MergeSort implements SortStrategy { public void sort(int[] a){ /* mergesort */ } }

class Sorter {                       // Context
    private SortStrategy strategy;
    Sorter(SortStrategy s) { this.strategy = s; }
    void setStrategy(SortStrategy s) { this.strategy = s; }   // runtime swap
    void performSort(int[] a) { strategy.sort(a); }           // delegation
}
```
- The client picks the strategy at construction or swaps it at run time (`setStrategy(new MergeSort())`).
- The context's `performSort` is strategy-agnostic.

## 3. When Is It Used?
- **A family of algorithms that the client should choose/swap at run time**: payment methods, export formats, compression, encryption, routing, sorting, pricing/discounts.
- **Multiple conditionals that dispatch on the same discriminator** (repeated `if (type == X)`): the classic "replace conditional with polymorphism" refactor (Fowler) produces a Strategy.
- **Algorithm variants that should be independently testable and reusable** across contexts.
- **JDK/framework**: `Collections.sort(List, Comparator)` (Comparator is a Strategy), `ThreadPoolExecutor`'s `RejectedExecutionHandler` (a strategy for what to do when the queue is full), Spring's `Environment`/`MessageConverter` selection.
- **Interviews**: "swappable algorithm", "payment methods vary", "sort with different comparators" → Strategy.

## 4. Why Wasn't Another Approach Chosen?
- **Conditional dispatch (`if`/`switch` in the context)**: rejected — Open-Closed violation (adding a format edits the class), SRP violation, untestable, can't vary at run time without re-entering the branch, and the logic grows monotonically. Strategy replaces branches with polymorphism.
- **Subclassing the context per algorithm** (`PdfReport` extends `Report`): rejected — you multiply classes by *every combination* of context-feature × algorithm, and the algorithm is bound at compile time (can't swap). Strategy composes instead of inherits.
- **Template Method (inheritance-based algorithm variation)**: the close relative — it fixes a *skeleton* and varies *steps* via subclass hooks. Strategy varies the *whole algorithm* via composition and allows *runtime* swap; Template Method varies steps and is *compile-time* bound. Use Template Method when the algorithm structure is fixed and only steps vary; use Strategy when entire algorithms are interchangeable (and you want runtime swap or multiple contexts sharing the algorithm).
- **A `Function`/lambda inline**: modern Java can pass a lambda `(a, b) -> ...` as the strategy — that IS a Strategy (the functional interface is the Strategy interface, the lambda is a ConcreteStrategy). This removes boilerplate for stateless single-method strategies, which is why modern Strategy examples use `Comparator`/`Function`/custom functional interfaces.
- **An enum with methods**: an enum can hold per-constant behavior (`enum Format { PDF { export(...) {...} } }`) — a compact strategy-for-enum-set pattern; chosen when the strategy set is closed and fixed; rejected when strategies must be added by other modules (Open-Closed).

## 5. Intuition
Strategy is a **swappable gearbox / a vending machine of behaviors**. The "car" (context) doesn't contain the gear logic; it has a *gearbox slot* (the Strategy reference) and you insert the gear you want — economy, sport, off-road — and the car *behaves* differently without rebuilding the car. Changing gear = swapping the strategy object; the car (context) never changes. Alternatively, a **chef choosing a cooking method**: the kitchen (context) has the recipe steps, but "how to cook" (steam / grill / fry) is decided per dish (the strategy), selected at service time.

## 6. Real-World Analogy
A **travel app's route options**. You ask the app for directions (context). The app doesn't hard-code "always fastest"; it holds a *routing strategy* and you pick: fastest, shortest, avoid-tolls, or scenic. Each strategy is a separate engine behind the same "give me directions" interface. Picking a different option is a run-time swap; adding "scenic" later doesn't change the app's core — just one more strategy. That's Strategy in daily life.

## 7. Formal Definition
> **Strategy** (a.k.a. Policy): Define a family of algorithms, encapsulate each one, and make them **interchangeable**. Strategy lets the algorithm vary **independently from the clients that use it**. (GoF, p. 315)
>
> Participants: **Strategy** (interface), **ConcreteStrategy** (algorithm implementation), **Context** (maintains a Strategy reference and delegates to it; may pass itself or its data to the strategy). The GoF intent: *behavioral variation without changing the context*.

## 8. Example
A **discount engine** for an e-commerce cart:
```java
interface DiscountStrategy { double apply(double price); }

class NoDiscount implements DiscountStrategy { public double apply(double p) { return p; } }
class PercentageDiscount implements DiscountStrategy {
    private final double percent;
    PercentageDiscount(double percent) { this.percent = percent; }
    public double apply(double p) { return p * (1 - percent / 100); }
}
class FlatDiscount implements DiscountStrategy {
    private final double amount;
    FlatDiscount(double amount) { this.amount = amount; }
    public double apply(double p) { return Math.max(0, p - amount); }
}

class CheckoutContext {                      // Context
    private DiscountStrategy discount = new NoDiscount();
    void setDiscount(DiscountStrategy d) { this.discount = d; }
    double total(double price) { return discount.apply(price); }
}
// Usage
CheckoutContext ctx = new CheckoutContext();
ctx.setDiscount(new PercentageDiscount(10));   // runtime swap
ctx.total(500.0);   // 450.0
ctx.setDiscount(new FlatDiscount(100));        // swap again
ctx.total(500.0);   // 400.0
```
- Adding a "buy-2-get-1-free" strategy = one new class; `CheckoutContext` never changes (Open-Closed); each discount is unit-testable in isolation.

## 9. Internal Working
1. The client constructs a concrete strategy (or receives one via DI/`@Autowired`).
2. The context is *configured* with the strategy (constructor, setter, or method-parameter).
3. When the context must perform the behavior, it calls `strategy.algorithm(contextData)`.
4. **Dynamic dispatch** (vtable lookup — Part 08) routes to the injected concrete strategy's implementation.
5. The strategy executes its algorithm, optionally using data passed from the context (context-as-parameter) or reading its own state (strategy-as-parameter).
6. The result returns to the context, which returns it to the client.
7. **Run-time swap**: any code holding the context can call `setStrategy(...)` to change behavior for subsequent calls — no recompilation of the context needed.

**Why it works**: the context is *closed for modification* (its code never branches on algorithm type) and *open for extension* (new strategies plug in). The client owns the *composition* decision (which strategy to inject) — the separation of "what to do" (client) from "how to do it" (strategy).

## 10. Time Complexity
- **Strategy dispatch**: O(1) — one virtual call (vtable lookup + call frame).
- **Strategy execution**: the algorithm's own complexity (e.g., sort O(n log n)), unchanged by the pattern.
- **Context overhead**: O(1) — a strategy reference + delegation. No asymptotic change.
- **Class count**: O(N) strategies for N algorithms — the price of decoupling (vs one giant conditional, which is O(1) classes but O(N) entangled branches).
- **Memory**: O(1) per strategy instance (stateless strategies can be singletons/shared).

## 11. Advantages
- **Open-Closed**: new algorithms = new classes; context never changes.
- **Single Responsibility**: each algorithm is a focused class, independently readable and testable.
- **Run-time interchangeability**: swap strategies without touching the context (composition, not compile-time binding).
- **Reusability**: a strategy is a standalone object usable by many contexts.
- **Eliminates conditionals**: replaces branching with polymorphism (a Fowler refactor target — "replace conditional with polymorphism").
- **Testability**: each strategy unit-tested in isolation; the context tested with a mock/fake strategy.

## 12. Disadvantages
- **Class proliferation**: one class per algorithm — many small classes for many strategies (mitigated by lambdas/functional interfaces for stateless strategies).
- **Client must know the strategies**: the client must know which strategies exist and pick one (the "selection knowledge" moves from the context to the client; mitigated by factory-provided strategies).
- **Communication overhead**: strategies may need lots of context data passed in (context-as-parameter) — or you leak context internals.
- **Stateless strategies still need lifecycle**: without DI, creating/discarding a strategy per use adds noise.
- **Can be over-engineered**: a fixed, small algorithm set with no swap need → a simple `if` is clearer (YAGNI).

## 13. Interview Questions
1. **Q: What is the Strategy pattern?** A: Define a family of interchangeable algorithms behind a common interface and let the context delegate to an injected strategy — swapping algorithms at run time without changing the context.
2. **Q: What problem does it solve?** A: The rigid, Open-Closed-violating, SRP-violating conditional dispatch for choosing an algorithm; it also enables run-time algorithm swapping and independent testability that inheritance/conditionals can't.
3. **Q: Strategy vs Template Method?** A: Strategy varies the *whole algorithm* via *composition* (injected object, run-time swap). Template Method fixes an *algorithm skeleton* in a base class and varies only *steps* via subclass overrides (inheritance, compile-time). Choose Strategy for whole-algorithm interchangeability; Template Method for fixed-structure with varying steps.
4. **Q: Strategy vs State? (Tricky)** A: Both use composition with an injected object, but Strategy's object is *chosen by the client* and typically stays fixed during an operation; State's object is *changed by the context itself* as events occur (each state transition replaces the state object). Strategy = client-driven selection; State = event-driven self-transition. Also, Strategy doesn't usually replace the strategy during execution; State commonly does.
5. **Q: Is a Java `Comparator` a Strategy?** A: Yes — `Collections.sort(list, comparator)` passes the comparison *algorithm* to a context that applies it; the comparator is a ConcreteStrategy and the sort routine is the context. It's the JDK's most famous Strategy.
6. **Q: How would you implement Strategy in modern Java (Java 8+)? (Production)** A: Make the Strategy a *functional interface* and pass lambdas/method references: `strategy = price -> price * 0.9;`. This collapses ConcreteStrategy classes into inline lambdas for stateless algorithms — the same pattern, less boilerplate. Keep classes when strategies are stateful or reused by name.
7. **Q: What are the participants in Strategy?** A: Strategy (interface), ConcreteStrategy (algorithm), Context (holds a Strategy reference, delegates). Optionally the context passes its data to the strategy (context-as-parameter).
8. **Q: How do you let strategies access context data without breaking encapsulation?** A: Two standard approaches: *context-as-parameter* (the context passes itself — risk of exposing internals) or *strategy-as-parameter* (the client passes the needed data to the strategy). Prefer passing minimal data (explicit args or a small value object) to keep strategies decoupled.
9. **Q: How does Strategy relate to the "replace conditional with polymorphism" refactor?** A: Fowler's refactor turns repeated `if (type==X) ... else if ...` into polymorphic dispatch — and the polymorphic hierarchy of behaviors IS a Strategy. The refactor is the practical route from a conditional mess to a Strategy.
10. **Q: Where does Spring use Strategy? (Production)** A: `Environment` abstraction (property-resolution strategies), `MessageConverter` selection in `RestTemplate`/`Message` converters, `RejectedExecutionHandler` (what to do when a thread pool is full), `PasswordEncoder` (different hashing strategies), `PlatformTransactionManager` selection. Also `DispatcherServlet`'s `HandlerMapping`/`HandlerAdapter` strategies.
11. **Q: Strategy vs a simple `Function` field?** A: They're the same idea — a `Function<T,R>` field IS a Strategy whose interface is `Function`. The pattern names the concept; lambdas are just the modern implementation. Interviews reward saying "the Strategy interface can be a `Function`/`Consumer`/custom functional interface."
12. **Q: Can strategies share state? (Tricky)** A: Stateless strategies (pure functions of their input) can be shared singletons (e.g., `NoDiscount.INSTANCE`). Stateful strategies (with config like `PercentageDiscount(percent)`) are immutable-config objects — shareable too if immutable. Mutable strategy state is an anti-pattern (thread-safety).
13. **Q: When would you NOT use Strategy? (Production)** A: When the algorithm set is small, fixed, and never swapped at run time — a simple `if`/enum-method is clearer (YAGNI). Also avoid when strategies need deep context internals (leaky abstraction) — reconsider the decomposition.
14. **Q: How does Strategy improve testability?** A: Each ConcreteStrategy is a focused class you can unit-test with known inputs; the context is tested with a *fake/mock* strategy (e.g., one that always returns a fixed value) to verify delegation — no need to configure every real algorithm in context tests.
15. **Q: Strategy vs Adapter?** A: Adapter converts an *incompatible interface* for compatibility (structural). Strategy injects an *interchangeable algorithm* (behavioral). Adapter answers "can it speak my interface?"; Strategy answers "which behavior do I run?"
16. **Q: Give a real-world scenario where runtime swap matters.** A: A data-compression service that switches from DEFLATE to ZSTD per client negotiation; a payment service that falls back from card to UPI when a strategy throws; a pricing engine that swaps discount rules per campaign without redeploying the cart. Runtime swap is what Strategy uniquely enables.
17. **Q: How do you pick the right strategy at runtime? (Production)** A: Use a *factory* that returns the strategy based on config/context (e.g., `DiscountStrategyFactory.forUser(segment)`), a registry keyed by discriminator, or DI with qualifiers. The selection knowledge lives in the factory, not the context.
18. **Q: Strategy and Open-Closed — prove it with a change scenario.** A: Adding "scenic route" = add `ScenicRouteStrategy` + register it in the factory. The `Router` context, existing strategies, and all clients are untouched. Zero modification, one addition — that's Open-Closed in action.
19. **Q: How do stateless strategies interplay with concurrency? (Tricky)** A: Stateless strategies are safe to share across threads (they hold no state — pure). If a strategy reads config, make it immutable and final. Shared mutable state inside a strategy is a concurrency bug — prefer stateless or immutable strategies.
20. **Q: Design a payment system with card, UPI, and wallet, plus a "swap at runtime" requirement. (Scenario)** A: Define `PaymentStrategy { PaymentResult pay(Amount) }`; implement `CardStrategy`, `UpiStrategy`, `WalletStrategy`; the `PaymentContext` holds a strategy, delegates `pay()`, and exposes `setStrategy()` for runtime fallback/switch; a factory builds the strategy from user preference + availability. Adding a method = one class + registration. That's the complete Strategy-based design interviewers want.

## 14. Follow-Up Questions
1. **Q: What is the "context as parameter" vs "strategy as parameter" distinction?** A: Context-as-parameter: the strategy receives the context (and can call back into it — coupling risk); strategy-as-parameter: the strategy receives just the data it needs (decoupled). GoF discusses both; modern practice prefers passing minimal data.
2. **Q: How does Strategy differ from an "enum strategy"?** A: An enum with a per-constant method (`enum Format { PDF { void export() {...} } }`) is a *closed* strategy set — compact, but new formats require editing the enum (Open-Closed violation). The class-based Strategy is *open* (new classes from outside). Use enum-strategy for fixed sets; class Strategy for open sets.
3. **Q: How does Strategy relate to functional programming?** A: Strategy is the OO name for a *higher-order function*: pass a function (the algorithm) to a function (the context). First-class functions make Strategy nearly free — Java lambdas (`Function`, `Comparator`), Python closures, and Go function fields are all Strategy under the hood.
4. **Q: What is the difference between Strategy and the Dependency Inversion Principle implementation?** A: Strategy *is* a canonical DIP implementation: the context depends on the Strategy *abstraction* (the DIP's "depend on abstractions"), and the concrete strategies are the "details". Frameworks wire the strategy via DI — the pattern and the principle align.
5. **Q: Can a Strategy be composed of other Strategies?** A: Yes — a "composite strategy" (e.g., a discount strategy that applies several sub-discounts, or a payment strategy that tries strategies in sequence with fallback) wraps a list of strategies. This is Strategy + Composite combined; the context sees one Strategy.

## 15. Coding Example
```java
// Strategy in modern Java with lambdas
import java.util.function.*;

interface CompressStrategy { byte[] compress(byte[] data); }   // could be a functional interface

class ZipCompress implements CompressStrategy {
    public byte[] compress(byte[] d) { System.out.println("ZIP"); return d; }
}
class GzipCompress implements CompressStrategy {
    public byte[] compress(byte[] d) { System.out.println("GZIP"); return d; }
}

class Compressor {                        // Context
    private CompressStrategy strategy;
    Compressor(CompressStrategy s) { this.strategy = s; }
    void setStrategy(CompressStrategy s) { this.strategy = s; }
    byte[] run(byte[] data) { return strategy.compress(data); }
}
public class Main {
    public static void main(String[] args) {
        Compressor c = new Compressor(new ZipCompress());
        c.run("hello".getBytes());                    // ZIP
        c.setStrategy(data -> { System.out.println("LZ4 (lambda strategy)"); return data; });
        c.run("hello".getBytes());                    // LZ4 (lambda strategy)
    }
}
```
```python
# Strategy in Python — functions as strategies
def zip_compress(data: bytes) -> bytes:
    print("ZIP"); return data
def lz4_compress(data: bytes) -> bytes:
    print("LZ4"); return data

class Compressor:
    def __init__(self, strategy): self.strategy = strategy
    def set_strategy(self, strategy): self.strategy = strategy
    def run(self, data: bytes) -> bytes: return self.strategy(data)

c = Compressor(zip_compress)
c.run(b"hello")          # ZIP
c.set_strategy(lz4_compress)
c.run(b"hello")          # LZ4
```
```cpp
// C++ Strategy via std::function or interface
#include <iostream>
#include <functional>

struct SortStrategy { virtual ~SortStrategy() = default; virtual void sort(int*, int) = 0; };
struct QuickSort : SortStrategy {
    void sort(int* a, int n) override { std::cout << "QuickSort\n"; }
};
struct MergeSort : SortStrategy {
    void sort(int* a, int n) override { std::cout << "MergeSort\n"; }
};
class Sorter {                       // Context
    SortStrategy& strategy_;
public:
    explicit Sorter(SortStrategy& s) : strategy_(s) {}
    void performSort(int* a, int n) { strategy_.sort(a, n); }
};
// int main(){ QuickSort q; Sorter s(q); int a[4] = {3,1,4,2}; s.performSort(a, 4); }
```

## 16. Industry Usage
- **JDK**: `Comparator` (Strategy for sorting), `ThreadPoolExecutor.RejectedExecutionHandler` (strategy for queue-full policy), `Collections.unmodifiableX` (not strategy), `java.util.function.Function`/`Consumer` (functional strategies).
- **Spring**: `PasswordEncoder` (hashing strategy), `PlatformTransactionManager` (transaction strategy), `MessageConverter`, `Environment` (property resolution strategy), `DispatcherServlet` `HandlerMapping`/`HandlerAdapter` selection, `CacheManager` abstraction.
- **Apache**: `commons-codec` encoders, `httpclient` `RequestExecutor` strategies; **Netty**: channel initialization strategies.
- **Games**: `GameMode`, bot-AI strategies (aggressive/defensive); **UI**: layout managers in Swing/AWT (`LayoutManager` is a classic Strategy — swap layout algorithm without touching the container).
- **E-commerce**: pricing/discount/shipping strategies, tax calculators, fraud-detection scoring strategies (swapped by segment).
- **Interviews**: "payment methods", "export formats", "sort with comparator", "swappable algorithms" — one of the most common pattern questions, plus the Strategy-vs-State and Strategy-vs-Template-Method discriminator questions.

## 17. References
- **Gamma et al., *Design Patterns* — "Strategy" (p. 315)**: canonical definition, context-as-parameter vs strategy-as-parameter discussion.
- **Oracle Docs: `java.util.Comparator`, `ThreadPoolExecutor.RejectedExecutionHandler`** — https://docs.oracle.com/javase/8/docs/api/
- **Martin Fowler, *Refactoring* — "Replace Conditional with Polymorphism"**: the refactor that produces Strategy.
- **Spring Framework Reference: `Environment`, `MessageConverter`, `RejectedExecutionHandler`-style extension points** — https://docs.spring.io/spring-framework/reference/
- **refactoring.guru — "Strategy"** — modern diagrams and Java/C++/Python examples.
- **Head First Design Patterns — "Strategy" chapter** — the duck example and why composition beats inheritance for behavior.
- **Brian Goetz, "Java Lambdas and Functional Interfaces" (Java 8 docs)** — the modern functional-interface form of Strategy.

## 18. Cheat Sheet
- Strategy = **family of interchangeable algorithms behind one interface; context delegates and can swap at run time**.
- Participants: Strategy (interface), ConcreteStrategy (algorithms), Context (holds a strategy reference).
- Strategy vs Template Method: Strategy = whole-algorithm via composition (runtime swap); Template Method = fixed skeleton + overridable steps via inheritance.
- Strategy vs State: Strategy = client-chosen, stays fixed; State = self-transitioning on events (the context replaces the state object).
- `Comparator` in `Collections.sort` is the canonical JDK Strategy; Swing `LayoutManager` is another.
- Modern Java: strategies can be lambdas (functional interfaces) — same pattern, less boilerplate.
- Context should be closed-for-modification; new algorithms = new strategy classes (Open-Closed).
- Stateless strategies can be shared singletons; stateful strategies should be immutable.
- Select the strategy via a factory/registry, not by a conditional in the context.
- YAGNI: don't use Strategy for a small, fixed, never-swapped algorithm set.

## 19. Quiz
1. Strategy lets the algorithm vary: a) at compile time only b) independently from the client (runtime swap) c) never d) by subclass → **b**
2. Which is NOT a Strategy participant? a) Strategy b) ConcreteStrategy c) Context d) Observer → **d**
3. The JDK's `Comparator` in `Collections.sort` is: a) an Adapter b) a Strategy c) a Singleton d) a Proxy → **b**
4. Strategy vs Template Method: a) both inheritance b) strategy composition (whole algorithm), template inheritance (skeleton+steps) c) both composition d) strategy is behavioral, template structural → **b**
5. Strategy vs State: a) state chosen by client b) strategy chosen by client and fixed; state changes itself on events c) identical d) both self-transition → **b**
6. In modern Java, a stateless strategy can be: a) an enum b) a lambda (functional interface) c) a static method only d) a record only → **b**
7. Adding a new algorithm under Strategy requires: a) editing the context b) editing every client c) adding a new ConcreteStrategy class d) rewriting the interface → **c**
8. Which principle does Strategy directly implement? a) Liskov b) Open-Closed + Dependency Inversion c) Interface Segregation d) Single Responsibility only → **b**
9. "Replace conditional with polymorphism" yields: a) Singleton b) Strategy c) Observer d) Memento → **b**
10. When is Strategy over-engineering? a) many algorithms, runtime swap b) small fixed algorithm set, no swap need c) algorithms vary per client d) open algorithm set → **b**

## 20. Flashcards
- **Q: Strategy intent?** → **A:** Encapsulate a family of interchangeable algorithms behind an interface; context delegates and swaps at run time.
- **Q: Participants?** → **A:** Strategy (interface), ConcreteStrategy (algorithm), Context (holds a strategy reference).
- **Q: Strategy vs Template Method?** → **A:** Strategy = whole algorithm via composition (runtime); Template = skeleton + steps via inheritance (compile-time).
- **Q: Strategy vs State?** → **A:** Strategy = client-chosen, fixed; State = self-transitioning on events.
- **Q: Canonical JDK Strategy?** → **A:** `Comparator` passed to `Collections.sort`.
- **Q: How to implement a stateless strategy in Java 8+?** → **A:** As a lambda implementing a functional interface.
- **Q: When NOT to use Strategy?** → **A:** Small fixed algorithm set with no runtime swap (YAGNI).
- **Q: How to pick the strategy at runtime?** → **A:** A factory or registry keyed by discriminator, or DI with qualifiers.

## 21. Revision
Strategy **encapsulates interchangeable algorithms** behind one interface; a `Context` holds a strategy reference and delegates to it, letting the client *swap algorithms at run time*. It exists to replace rigid conditional dispatch (`if format==...`) — the conditionals violate Open-Closed and SRP, and can't vary at run time. Participants: Strategy (interface), ConcreteStrategy (algorithm classes or lambdas), Context (delegates, never branches). Discriminate: **Template Method** fixes a skeleton and varies steps via inheritance; **State** self-transitions on events while Strategy stays client-fixed; **Adapter** converts interfaces (structural). Canonical: `Comparator` with `Collections.sort`, Swing `LayoutManager`, Spring `PasswordEncoder`/`PlatformTransactionManager`. Modern Java implements stateless strategies as lambdas (functional interfaces). Best practice: select strategies via a factory/registry (not conditionals), keep stateless strategies shared, and skip the pattern for small, fixed, never-swapped algorithm sets (YAGNI).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Strategy pattern?" | 2 How / 7 Formal Definition |
| "What problem does it solve?" | 1 Why / 13 Q2 |
| "Strategy vs Template Method?" | 13 Q3 / 14 Q4 |
| "Strategy vs State?" | 13 Q4 / 18 Cheat Sheet |
| "Is a Comparator a Strategy?" | 13 Q5 / 8 Example |
| "Lambdas as strategies?" | 13 Q6 / 15 Coding |
| "How to choose the strategy at runtime?" | 13 Q17 / 14 Q3 |
| "When to NOT use Strategy?" | 13 Q13 / 18 Cheat Sheet |
| "Stateless strategies & concurrency?" | 13 Q19 / 14 Q5 |
| "Design a payment system with runtime swap (scenario)." | 13 Q20 / 15 Coding |
