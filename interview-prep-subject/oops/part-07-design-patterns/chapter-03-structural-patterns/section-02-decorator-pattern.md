# Decorator Pattern

> **TL;DR**: The Decorator pattern attaches **additional responsibilities to an object dynamically** by wrapping it in decorator objects that share its interface — it exists because "inheritance to add features" explodes into a combinatorial class explosion, while "compose wrappers" gives you unlimited feature combinations at run time with zero subclassing.

## 1. Why Does This Exist?
Consider a `Coffee` class and features like milk, sugar, whipped cream, and caramel. Using *inheritance* to model every combination means a class per combination: `Coffee`, `MilkCoffee`, `SugarCoffee`, `MilkSugarCoffee`, `MilkSugarWhippedCoffee`... — with 4 binary features that's 2⁴ = 16 classes; with 8 features, 256. This is **combinatorial explosion** (the "class explosion" problem) and it's the direct failure inheritance causes when features are *composable and optional*.

The Decorator pattern exists because **"adding behavior to objects" and "inheritance to add behavior" are not the same thing**. Inheritance adds behavior at *compile time* to a whole *type*; it can't add it to a single *instance* at run time, and it forces a class per combination. Decorator instead composes wrappers at run time: each feature is its own class *implementing the same interface* and *delegating to a wrapped instance*. You assemble features like Lego — `new WhippedCream(new Milk(new Coffee()))` — so N features give you 2^N combinations with only N decorator classes.

It also exists to add responsibilities **transparently**: the client (typed to the base interface) cannot even tell it's talking to a decorated object — `InputStream` is still `InputStream`, whether wrapped by `BufferedInputStream` or `GZIPInputStream`. That transparency is what lets decorators layer arbitrarily: encryption over compression over buffering, each decorating the previous.

## 2. How Does It Work?
The shape is a self-similar wrapper chain:
```
Interface Component { operation(); }
   ▲                        ▲
ConcreteComponent   Decorator (holds a Component; forwards operation() and adds behavior)
                        ▲
                   ConcreteDecoratorA, ConcreteDecoratorB ...
```
Participants:
1. **Component** — the common interface (what clients see).
2. **ConcreteComponent** — the base object being decorated (does the real work).
3. **Decorator** — abstract class implementing `Component` and holding a `Component` reference (the wrapped one).
4. **ConcreteDecorator(s)** — extend `Decorator`; in `operation()`, call `wrapped.operation()` then add their own behavior (before or after).

```java
interface Coffee { double cost(); String describe(); }
class PlainCoffee implements Coffee { public double cost(){ return 2.0; } public String describe(){ return "coffee"; } }

abstract class CoffeeDecorator implements Coffee {
    protected final Coffee inner;
    CoffeeDecorator(Coffee c) { this.inner = c; }
}
class Milk extends CoffeeDecorator {
    Milk(Coffee c) { super(c); }
    public double cost() { return inner.cost() + 0.5; }
    public String describe() { return inner.describe() + ", milk"; }
}
class WhippedCream extends CoffeeDecorator {
    WhippedCream(Coffee c) { super(c); }
    public double cost() { return inner.cost() + 0.7; }
    public String describe() { return inner.describe() + ", whipped cream"; }
}
// Usage — compose at run time:
Coffee c = new WhippedCream(new Milk(new PlainCoffee()));
System.out.println(c.cost());      // 3.2
System.out.println(c.describe());  // coffee, milk, whipped cream
```
Each decorator *delegates then augments*; the chain grows at run time; the client still sees `Coffee`.

## 3. When Is It Used?
- **When you must add responsibilities to *individual objects*, not whole classes**: a specific request needs logging while others don't.
- **When adding features in all combinations would explode the class count** (streams, toppings, UI styling, formatting).
- **When the order of wrappers matters and must be flexible at run time** (encrypt-then-compress vs compress-then-encrypt).
- **When subclassing is impossible** (final/sealed classes — decorator is the composition-based fallback).
- **Java I/O**: `new BufferedInputStream(new FileInputStream(...))`, `new GZIPInputStream(...)`, `new LineNumberReader(new BufferedReader(...))` — the JDK's I/O streams *are* a decorator family.
- **Interviews**: "add features without subclassing / class explosion" → Decorator.

## 4. Why Wasn't Another Approach Chosen?
- **Inheritance (class per combination)**: rejected — combinatorial explosion (2^N classes for N binary features), compile-time-only (can't decorate a single instance at run time), and deep inheritance hierarchies are fragile (Part 03). This is *the* failure Decorator fixes.
- **Subclassing one base and overriding everything**: rejected — you still can't combine features dynamically and you must know all features at compile time.
- **Modifying the base class with all features (a "fat" class)**: rejected — violates Single Responsibility (every object carries every feature's cost), and features that aren't independent become tangled (the base class grows unboundedly).
- **Strategy-like composition of behavior flags** (`boolean hasMilk`): rejected for *complex, layered* behavior — a boolean field works for a handful of toggle features but can't add *new kinds of behavior* (logging, compression, encryption, timing) or *nest* them meaningfully; decorators are objects, so they can carry state and behavior.
- **A utility that transforms data (e.g., compress(data))**: fine for stateless transforms; rejected when the "added responsibility" is *per-object state* or when you want to *mix and match with the object's identity preserved* (an `InputStream` stays an `InputStream`).
- **Preferring composition over inheritance in general**: this pattern *is* that principle mechanized — composition wins because it's flexible (run time, any combination), while inheritance is rigid (compile time, class-per-combination).

## 5. Intuition
A decorator is **layering clothes or painting walls**. You don't buy a "warm-red-cotton-sweater" — you layer a cotton sweater *over* a red shirt *over* a thermal base. Each layer (decorator) adds its property and passes the rest through. You can choose any combination at *wear time* (run time), not at *factory time* (compile time). The "person inside" (the concrete component) stays the same; each layer just wraps it. Removing a layer is as easy as removing the sweater — but in OOP you'd rebuild the chain.

## 6. Real-World Analogy
A **café beverage bar**. The barista starts with a base (espresso, tea), then *adds optional layers* — milk, sugar, caramel, whipped cream, extra shot — each adding cost and description, *in whatever order you choose*, at order time (run time). There is no "espresso with milk and sugar and caramel" class in the menu — there's a base and a stack of add-ons. The menu (interface) always says "beverage"; the recipe card (decorator chain) determines the final cost. That's the decorator pattern working as a point-of-sale system.

## 7. Formal Definition
> **Decorator**: Attach additional responsibilities to an object **dynamically**. Decorators provide a flexible alternative to subclassing for extending functionality. (GoF, p. 175)
>
> Participants: **Component** (interface), **ConcreteComponent** (the object receiving added behavior), **Decorator** (abstract: holds a Component reference, conforms to Component's interface), **ConcreteDecorator** (adds responsibilities before/after delegating). Also known as **Wrapper**.

## 8. Example
Java I/O is the canonical production example — `java.io` is a tree of components (InputStream, OutputStream, Reader, Writer) and a forest of decorators:
```java
InputStream raw = new FileInputStream("report.txt");   // ConcreteComponent
InputStream buffered = new BufferedInputStream(raw);    // decorator: buffer reads
InputStream compressed = new GZIPInputStream(buffered); // decorator: decompress
InputStream counted = new CountingInputStream(compressed); // (Apache Commons) count bytes
int b;
while ((b = counted.read()) != -1) { /* process */ }
```
Each constructor *wraps* the previous stream and *adds* a responsibility (buffering, decompression, counting) while presenting the same `InputStream` interface to the caller. The call stack at `read()`: `CountingInputStream.read` → `GZIPInputStream.read` → `BufferedInputStream.read` → `FileInputStream.read` — four layers, each doing its own job, assembled at run time in any order.

## 9. Internal Working
1. The client holds a reference typed to `Component` — it may actually be a chain of decorators.
2. The client calls `component.operation()`.
3. **Dynamic dispatch** resolves to the *outermost* decorator's `operation()`.
4. That decorator (optionally) does *pre-work*, then calls `inner.operation()` — recursing to the next layer — and, after the inner call returns, does *post-work* (e.g., compress after write, count after read).
5. The recursion unwinds until the innermost `ConcreteComponent.operation()` executes the real work; results flow back out through each layer.
6. Composition happens at construction (run time): `new A(new B(new C()))` — the order of wrappers is decided by the caller and can vary per use.

**Critical correctness point**: each decorator *must* forward every relevant method to its `inner` (it can't "know" about layers above). If a decorator drops a method or doesn't forward, the chain breaks — a common bug. Because decorators conform to the same interface, the client code never changes whether it receives a plain or a layered object — **transparency**.

## 10. Time Complexity
- **Single call through a chain of D decorators**: O(D) — each layer adds O(1) delegation + its own O(its work). A stream read through 4 decorators is O(4 × per-read work).
- **Total construction**: O(D) (building the chain).
- **Memory**: O(D) wrapper objects.
- **Design win**: O(N) *classes* instead of O(2^N) inheritance subclasses for N binary features — the class-count explosion is eliminated at the price of O(N) runtime objects.
- **No algorithmic complexity change** — decorators add constant-factor indirection; the wrapped operation's own Big-O is unchanged.

## 11. Advantages
- **No class explosion**: N features = N decorator classes, not 2^N subclasses.
- **Runtime flexibility**: decorate *specific instances* (one request gets logging, another doesn't) and compose in any order.
- **Transparency**: clients typed to the interface are unaffected by decoration.
- **Single Responsibility**: each decorator does exactly one added thing (SRP); features are individually testable.
- **Layering**: encryption over compression over buffering composes naturally.
- **Incremental behavior**: decorators can add behavior before and after the inner call (pre/post hooks).

## 12. Disadvantages
- **Many small objects**: a 5-decorator chain is 5 objects + 5 call frames — debugging stack traces get noisy.
- **Order sensitivity**: encrypt-then-compress ≠ compress-then-encrypt; the caller must pick the right order, and the pattern doesn't enforce it.
- **Object identity breaks**: `wrapper.equals(component)` fails — identity and equality are lost through wrapping (decorated objects don't equal their undecorated twins).
- **No "unwrap" guarantee**: if a client accidentally wraps the wrong layer or a decorator's constructor requires specific order, errors are runtime, not compile-time.
- **Forwarding boilerplate**: every method must be forwarded; abstract Decorator helps but interfaces with many methods make it tedious (Java I/O's abstract `FilterInputStream` exists precisely to absorb this).
- **Harder to reason about type-specific operations**: a concrete method available only on `ConcreteComponent` is unreachable through the interface after wrapping.

## 13. Interview Questions
1. **Q: What is the Decorator pattern?** A: A structural pattern that attaches additional responsibilities to an object dynamically by wrapping it in decorator classes that conform to the same interface and delegate, adding behavior before/after the wrapped call.
2. **Q: What problem does it solve?** A: Class explosion from inheritance-per-feature-combination (2^N subclasses for N binary features) and the inability of inheritance to add behavior to a *single instance* at run time. Decorator composes features at run time with N classes.
3. **Q: Why does inheritance fail here? (Give numbers)** A: With 5 binary features (milk, sugar, cream, caramel, shot), inheritance needs 2^5 = 32 classes (or more with nested combos). Decorator needs 5 decorator classes + 1 base = 6. The gap grows exponentially with N.
4. **Q: How does a decorator chain actually execute? (Walk through the call)** A: Client calls `outermost.operation()` → pre-work → `inner.operation()` → ... → innermost ConcreteComponent does the real work → results bubble back through each layer's post-work. It's a recursive delegation with augmentation at each level.
5. **Q: What must every decorator guarantee? (Tricky)** A: **Transparency + correct forwarding**: it must conform exactly to the Component interface and forward every relevant call to its wrapped instance, or the chain breaks and clients break. A decorator that "forgets" a method silently drops behavior.
6. **Q: Decorator vs Adapter?** A: Decorator *keeps the same interface* and adds behavior around the object; Adapter *changes the interface* to make incompatible ones work together. Adapter = compatibility; Decorator = augmentation.
7. **Q: Decorator vs Proxy?** A: Both wrap and delegate, but Decorator *adds behavior* (enhancement), while Proxy *controls access* (lazy init, security, remote, caching) and typically keeps the same interface; Proxy is about access management, Decorator about responsibility stacking.
8. **Q: Decorator vs Strategy?** A: Strategy *replaces an algorithm* inside a context (behavior interchange); Decorator *stacks behaviors* around an object. Strategy: "which algorithm to run?"; Decorator: "what layers to wrap around?"
9. **Q: Can a decorator be used where subclassing is impossible?** A: Yes — for `final`/sealed classes you can't subclass, but you *can* wrap them in a decorator implementing the interface (composition works where inheritance doesn't). This is a strong point for composition-over-inheritance.
10. **Q: What's the difference between the abstract Decorator and ConcreteDecorator?** A: The abstract `Decorator` holds the `Component` reference and forwards all methods to it (removing boilerplate); `ConcreteDecorator` overrides only the methods where it adds behavior, calling `super` to forward. Java I/O's `FilterInputStream` is the abstract decorator.
11. **Q: How does Java I/O implement the pattern? (Production)** A: `InputStream` (Component), `FileInputStream` (ConcreteComponent), `FilterInputStream` (abstract Decorator holding a wrapped stream), and concrete decorators `BufferedInputStream`, `GZIPInputStream`, `DataInputStream`, `ObjectInputStream`. `new DataInputStream(new BufferedInputStream(new FileInputStream(f)))` is decoration in action.
12. **Q: Can decorators have their own state?** A: Yes — a decorator can hold state relevant to its responsibility: a `CountingInputStream` holds a byte counter; a `LoggingDecorator` holds a logger. Decorators are objects, so state per layer is natural (unlike flag-fields on a fat base class).
13. **Q: What is the "identity/equality" problem?** A: Because wrapping creates new objects, `decorated.equals(undecorated)` fails even if behavior is identical, and `instanceof` checks against the concrete component fail. Systems that rely on object identity (caches, maps keyed by object) can break when objects are decorated.
14. **Q: Order sensitivity — give a concrete example.** A: Encrypting then compressing yields different (usually worse) compression than compressing then encrypting; in I/O, `new GZIPOutputStream(new FileOutputStream(f))` vs wrapping order changes behavior. The pattern doesn't enforce order — the caller must know the semantics.
15. **Q: When would you NOT use a decorator? (Production)** A: When features are mutually exclusive (Strategy/State fits better), when feature count is small and static (simple fields), when you need strong typing on concrete classes, or when the object is very hot-path (per-call indirection matters). Also avoid when a plain `Map`/config object expresses the variation more simply.
16. **Q: How is Decorator used in Spring? (Scenario)** A: `HttpServletResponseWrapper`/`HttpServletRequestWrapper` (Java EE) are decorators used in filters to wrap responses (add headers, modify bodies). Spring Security's filter chain layers filters (a decorator-ish pipeline). Spring AOP proxies are proxy-style, but `BeanPostProcessor` wrapping (e.g., `CompositeBeanPostProcessor` decorating behavior) is decorator-flavored. In interviews, cite `FilterInputStream`/`Wrapper` examples.
17. **Q: How do you debug a stack of decorators? (Production)** A: The stack trace shows each wrapper's frame — give each decorator a meaningful class name, log the composition order at construction, and use a `describe()`/`toString()` that renders the chain. Tools like a "chain introspection" method help production debugging.
18. **Q: Can decorators be combined with Factory? (Tricky)** A: Yes — a factory can *build the decorated chain*: `CoffeeFactory.make("caramel-milk")` returns `new Caramel(new Milk(new PlainCoffee()))`, hiding the composition. This is a common production idiom: factory decides the recipe; decorators provide the layers.
19. **Q: What's the difference between adding behavior *before* vs *after* the delegate call?** A: Pre-work runs on the way *in* (validate args, start timer, encrypt output, buffer writes); post-work runs on the way *out* (flush, end timer, count bytes, verify). A `TimingDecorator` uses both: record start → delegate → record end → add elapsed. This is the "wrap-around" semantics that make decorators powerful.
20. **Q: Design a text-processing pipeline using decorators. (Scenario)** A: `StringProcessor` (Component), `PlainProcessor` (Concrete), and decorators `UpperCaser`, `Trimmed`, `Reversed`, `ProfaneFilter` — chain `new ProfaneFilter(new Reversed(new UpperCaser(new PlainProcessor())))`. Each adds one transform; order controls semantics; adding a new transform = one new decorator class, zero changes to others.

## 14. Follow-Up Questions
1. **Q: Why does Java's `FilterInputStream` exist and what does it buy?** A: It's the abstract Decorator: it holds the wrapped stream and forwards *every* InputStream method (read, skip, available, close...) to it, so concrete decorators override only the methods they augment. Without it, each decorator would re-implement the whole interface.
2. **Q: How do decorators interplay with `try-with-resources` and closing?** A: `close()` on the outermost decorator must propagate down the chain (FilterInputStream forwards close to the wrapped stream) — closing the top closes all layers and the base. Failing to forward `close()` leaks the underlying resource.
3. **Q: What's the "composite decorator" vs "composite pattern" distinction?** A: A decorator chain is linear (one inner reference); a Composite is a tree (many children). Both are structural "containers", but decorators augment one object while composites treat groups uniformly. They're often composed together (a decorator wrapping a composite tree).
4. **Q: When does the decorator's transparency break?** A: When a client needs a *concrete* capability not on the interface (e.g., `BufferedInputStream.getBufferSize()`), or when it does `instanceof FileInputStream` — both fail through wrapping. The "interface-only" rule keeps decorators transparent; concrete-type access breaks it.
5. **Q: Decorator vs dynamic proxies (Java `Proxy`/AOP)?** A: Dynamic proxies intercept method calls with an `InvocationHandler` — a *proxy*-flavored decorator that can add cross-cutting behavior (logging, transactions) without writing per-class decorators. AOP "around" advice is decorator semantics via proxy machinery; hand-written decorators give type-safe compile-time structure, proxies give catch-all runtime interception.

## 15. Coding Example
```java
// Decorator in Java — a stream that encrypts on write (invert the pattern's order: post-work)
interface DataWriter { void write(String data); }
class FileWriterImpl implements DataWriter {           // ConcreteComponent
    public void write(String data) { System.out.println("file: " + data); }
}
abstract class WriterDecorator implements DataWriter { // abstract Decorator
    protected final DataWriter inner;
    WriterDecorator(DataWriter w) { this.inner = w; }
}
class EncryptingWriter extends WriterDecorator {       // ConcreteDecorator
    EncryptingWriter(DataWriter w) { super(w); }
    public void write(String data) {
        String encrypted = "ENC[" + new StringBuilder(data).reverse() + "]";  // transform
        inner.write(encrypted);                        // delegate with augmentation
    }
}
class BufferingWriter extends WriterDecorator {
    private final StringBuilder buf = new StringBuilder();
    BufferingWriter(DataWriter w) { super(w); }
    public void write(String data) { buf.append(data); if (buf.length() > 10) flush(); }
    public void flush() { inner.write(buf.toString()); buf.setLength(0); }
}
// Usage
DataWriter w = new EncryptingWriter(new BufferingWriter(new FileWriterImpl()));
w.write("hello world, this is a long line to force a flush!");
// Output (buffered then encrypted): file: ENC[!hsulf a ecrof ot enil gnol a si siht ,dlrow olleh]
```
```python
# Python decorators can be implemented as callable wrappers (or functools.wraps)
class Coffee:
    def cost(self) -> float: return 2.0
    def describe(self) -> str: return "coffee"

def milk(coffee):
    class _Milk:
        def cost(self): return coffee.cost() + 0.5
        def describe(self): return coffee.describe() + ", milk"
    return _Milk()

c = milk(Coffee())
print(c.cost(), c.describe())   # 2.5 coffee, milk
```
```cpp
// C++ decorator via interface + composition
#include <iostream>
#include <string>
#include <memory>

struct Coffee {
    virtual double cost() const = 0;
    virtual std::string describe() const = 0;
    virtual ~Coffee() = default;
};
struct PlainCoffee : Coffee {
    double cost() const override { return 2.0; }
    std::string describe() const override { return "coffee"; }
};
class CoffeeDecorator : public Coffee {   // abstract decorator
protected:
    std::shared_ptr<Coffee> inner_;
public:
    explicit CoffeeDecorator(std::shared_ptr<Coffee> c) : inner_(std::move(c)) {}
};
class Milk : public CoffeeDecorator {
public:
    explicit Milk(std::shared_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}
    double cost() const override { return inner_->cost() + 0.5; }
    std::string describe() const override { return inner_->describe() + ", milk"; }
};
class WhippedCream : public CoffeeDecorator {
public:
    explicit WhippedCream(std::shared_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}
    double cost() const override { return inner_->cost() + 0.7; }
    std::string describe() const override { return inner_->describe() + ", whipped cream"; }
};
// int main(){ auto c = std::make_shared<WhippedCream>(std::make_shared<Milk>(std::make_shared<PlainCoffee>())); 
//              std::cout << c->cost() << " " << c->describe() << "\n"; }
```

## 16. Industry Usage
- **Java I/O** — the JDK's largest decorator family: `BufferedInputStream`, `DataInputStream`, `ObjectInputStream`, `GZIPInputStream`, `PushbackInputStream`, `LineNumberInputStream` (all extending `FilterInputStream`, the abstract decorator).
- **Java EE / Servlet wrappers**: `HttpServletRequestWrapper`/`HttpServletResponseWrapper` — filters wrap responses to add headers, gzip, or sanitize output (decorator over the response object).
- **Spring Security**: filter chains layer authentication/authorization behavior; `CompositeFilter` and response wrappers are decorator-flavored.
- **Guava**: `ForwardingInputStream`/`ForwardingCollection` (abstract decorators), `FilteredInputStream`, `LimitedInputStream`.
- **Apache Commons IO**: `CountingInputStream`, `TeeInputStream` (tees to two sinks), `BoundedInputStream`.
- **Logging**: MDC-adding wrappers, `ThreadContext` decorating loggers.
- **UI libraries**: widget decoration (borders, scrollbars, tooltips) as decorators; Java Swing's `BorderFactory` composes borders decorator-style.
- **Interviews**: "add features without subclassing", "class explosion", "Java I/O design", "how would you add logging/caching/encryption to an existing class" — all Decorator territory, and it pairs with the adapter/proxy/facade discriminator questions.

## 17. References
- **Gamma et al., *Design Patterns* — "Decorator" (p. 175)**: canonical definition, the transparency and interface-conformance discussion.
- **Oracle Docs: `java.io` package, `FilterInputStream`, `BufferedInputStream`, `GZIPInputStream`** — https://docs.oracle.com/javase/8/docs/api/java/io/package-summary.html
- **Joshua Bloch, *Effective Java* (3rd ed.), Item 18**: "Favor composition over inheritance" — the modern justification (wrapper classes are decorators).
- **Java EE Docs: `javax.servlet.http.HttpServletResponseWrapper`** — the servlet wrapper/decorator.
- **Guava Docs: `ForwardingInputStream` and friends** — https://guava.dev/releases/snapshot/api/docs/
- **refactoring.guru — "Decorator"** — modern diagrams and Java/C++/Python examples.
- **Head First Design Patterns, "The Decorator Pattern" chapter** — the coffee-shop worked example.

## 18. Cheat Sheet
- Decorator = **attach responsibilities to an object at run time** by wrapping with same-interface decorators.
- Solves **class explosion**: N features = N decorator classes (not 2^N subclasses).
- Chain call = recursive delegation: pre-work → inner call → post-work, layer by layer.
- Every decorator must **conform to the interface and forward** every relevant call (transparency).
- **Decorator ≠ Adapter** (adapter changes interface), **≠ Proxy** (proxy controls access), **≠ Strategy** (strategy swaps algorithm).
- Java I/O is the canonical example: `FilterInputStream` (abstract decorator) + `Buffered/GZIP/Data` decorators.
- Order matters (encrypt-then-compress ≠ compress-then-encrypt).
- Identity/equality breaks through wrapping.
- Abstract Decorator removes forwarding boilerplate; ConcreteDecorator overrides only augmented methods.
- Combine with Factory to build decorated chains from a recipe.

## 19. Quiz
1. Decorator attaches responsibilities: a) at compile time via inheritance b) dynamically via wrapping c) via static methods d) via copy → **b**
2. With N binary features, inheritance needs ___ classes, decorator needs ___. a) N, 2^N b) 2^N, N c) N, N d) 2^N, 2^N → **b**
3. Which keeps the SAME interface as the component? a) Adapter b) Decorator c) Facade d) Bridge → **b**
4. The abstract Decorator (e.g., `FilterInputStream`) mainly: a) adds behavior b) forwards all methods to the wrapped object c) closes streams d) creates chains → **b**
5. Which is the JDK's abstract decorator for byte streams? a) `InputStream` b) `FilterInputStream` c) `FileInputStream` d) `DataOutput` → **b**
6. Decorator vs Proxy: Decorator ___, Proxy ___. a) adds behavior; controls access b) controls access; adds behavior c) both add behavior d) both control access → **a**
7. A decorator that forgets to forward a method: a) still works b) silently drops that behavior c) throws an error at compile time d) duplicates calls → **b**
8. Why does `decorated.equals(undecorated)` fail? a) Java limitation b) wrapping creates new objects (identity lost) c) decorators are static d) equals is not inherited → **b**
9. `new GZIPOutputStream(new FileOutputStream(f))` is an example of: a) Adapter b) Decorator c) Facade d) Singleton → **b**
10. When is Decorator a poor choice? a) many combinable features b) mutually-exclusive features / simple static flags c) layering d) streams → **b**

## 20. Flashcards
- **Q: Decorator intent?** → **A:** Attach additional responsibilities to an object dynamically, via same-interface wrappers — an alternative to subclassing.
- **Q: Problem solved?** → **A:** Class explosion (2^N subclasses for N features) and runtime-only-per-instance behavior.
- **Q: How does a chain execute?** → **A:** Recursive delegation: pre-work → inner call → post-work, layer by layer.
- **Q: The #1 decorator correctness rule?** → **A:** Conform to the interface and forward every relevant call (transparency).
- **Q: Decorator vs Adapter?** → **A:** Adapter changes the interface (compatibility); Decorator keeps it (augmentation).
- **Q: Decorator vs Proxy?** → **A:** Decorator adds behavior; Proxy controls access (same interface).
- **Q: Canonical JDK example?** → **A:** `FilterInputStream` + `BufferedInputStream`/`GZIPInputStream`/`DataInputStream`.
- **Q: What breaks through wrapping?** → **A:** Object identity/equality and concrete-type checks (`instanceof`).

## 21. Revision
Decorator **adds responsibilities to an object at run time** by wrapping it in classes that share its interface and delegate with augmentation — the composition-based fix for inheritance's class explosion (N features = N decorator classes instead of 2^N subclasses) and for the inability of inheritance to decorate a single instance. Mechanics: an abstract `Decorator` (holding the wrapped `Component` and forwarding all methods) plus concrete decorators that override only augmented methods, doing pre-work, delegating, then post-work — the chain is built at run time (`new WhippedCream(new Milk(new PlainCoffee()))`). Correctness demands **interface conformance + full forwarding** (transparency). Discriminate: Adapter changes interface; Proxy controls access; Strategy swaps algorithms. Canonical production use: Java I/O (`FilterInputStream` + `BufferedInputStream`/`GZIPInputStream`/`DataInputStream`), servlet response wrappers, Spring Security filter layering. Watch: order-sensitivity, identity/equality loss, and boilerplate (mitigated by the abstract Decorator). Combine with Factory to build chains from a recipe.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Decorator pattern?" | 2 How / 7 Formal Definition |
| "Why does inheritance fail for combos?" | 1 Why / 13 Q3 |
| "Walk through a decorator chain call." | 9 Internal Working / 13 Q4 |
| "What must every decorator guarantee?" | 13 Q5 / 18 Cheat Sheet |
| "Decorator vs Adapter / Proxy / Strategy?" | 13 Q6–Q8 / 14 Q5 |
| "How does Java I/O use it?" | 13 Q11 / 16 Industry Usage |
| "What is the identity/equality problem?" | 13 Q13 |
| "Order sensitivity example?" | 13 Q14 |
| "When would you NOT use a decorator?" | 13 Q15 |
| "Design a text-processing pipeline (scenario)." | 13 Q20 |
