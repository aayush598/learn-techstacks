# Factory Method and Abstract Factory

> **TL;DR**: The **Factory Method** pattern delegates "which concrete class to instantiate" to subclasses (one product, decided at compile-time class choice); the **Abstract Factory** pattern provides an interface for creating **a family of related products** without naming their concrete classes (many products, decided at run time) — both exist so that client code depends on abstractions, not `new` calls, satisfying the Dependency Inversion and Open-Closed principles.

## 1. Why Does This Exist?
The plain `new ConcreteClass()` statement is the **hardest coupling in OO design**: it hard-codes a concrete type into the caller, and it *scatters* creation decisions across the codebase. When a new product type appears (a new notification channel, a new UI theme, a new data source), every `new` call site must be found and edited, violating Open-Closed (Part 06). Both factory patterns exist to **move the creation decision out of the client**:

- **Factory Method** exists when one *family* of products has a single product at a time, and the choice of which concrete class is *deferred to a subclass* — e.g., a framework says "create a `Document`" and each application subclass decides whether that's a `PdfDocument`, `WordDocument`, or `HtmlDocument`.
- **Abstract Factory** exists when a system must create a *related set* (a "family") of products that are designed to work together — e.g., a UI toolkit that must produce *windows, buttons, and scrollbars that look like Windows* together, or *that look like Linux together*. Mixing a Windows button into a Linux dialog is a bug; Abstract Factory guarantees family consistency.

Both exist for the same root reason: **the caller should depend on an abstraction (interface), not on a concrete constructor call**, so the codebase becomes extensible (add a product = add a class, don't edit callers) and swappable (swap the whole family at run time).

## 2. How Does It Work?
**Factory Method** — one interface, one method, deferred to subclasses:
1. The creator (framework) defines `createProduct()` as a *factory method* returning `Product`.
2. The base creator's business logic calls `createProduct()` without knowing the concrete type.
3. Each *subclass* overrides `createProduct()` to return its own product.

```
<<Creator>>           createProduct(): Product      ← factory method (abstract)
   |                      businessLogic() { use createProduct() }
<<ConcreteCreatorA>>  createProduct() { return new ProductA(); }
<<ConcreteCreatorB>>  createProduct() { return new ProductB(); }
```
The client calls `businessLogic()`, which internally calls the overridden `createProduct()`. The *decision* lives in the subclass; the *caller* never names a concrete class.

**Abstract Factory** — a family of products behind one factory interface:
1. Define product *interfaces* (e.g., `Button`, `Checkbox`).
2. Define a *factory interface* `GUIFactory` with `createButton()`, `createCheckbox()`.
3. Each *concrete factory* (`WindowsFactory`, `LinuxFactory`) returns consistent members of its family (Windows button + Windows checkbox).
4. The client holds a `GUIFactory` and asks it for products — it never writes `new WindowsButton()`.

```
<<GUIFactory>>       createButton(): Button      createCheckbox(): Checkbox
<<WindowsFactory>>   → WindowsButton             → WindowsCheckbox
<<LinuxFactory>>     → LinuxButton               → LinuxCheckbox
```

## 3. When Is It Used?
- **Factory Method**: when a framework/creator must be usable by unknown future subclasses ("design the framework, let apps plug in products"); when a class can't anticipate the product classes it must create; when subclassing the creator to change the product is acceptable (class-scope); e.g., `java.util.Calendar.getInstance()` delegates to locale/zone subclasses; `Collection.iterator()` is a factory method returning a type-specific `Iterator`.
- **Abstract Factory**: when the system must create *families of related objects* that must not be mixed; when the family itself is a variation axis (theme, OS, DB dialect, payment provider); when you want to swap entire product families at run time (choose `PostgresFactory` vs `MySqlFactory`); e.g., `javax.xml.parsers.DocumentBuilderFactory`, `SAXParserFactory`, `Connection` from `DriverManager` (each JDBC driver is a family of objects).
- **In interviews**: "create objects without naming concrete classes" → immediately think factories; "a set of products that must stay compatible" → Abstract Factory specifically.

## 4. Why Wasn't Another Approach Chosen?
- **Direct `new` calls everywhere**: simplest, but tightly couples callers to concrete classes; violates Open-Closed (adding a product edits many sites); breaks testability (can't inject fakes). Rejected in any extensible design.
- **A single static factory method (utility factory)**: `Factory.create("pdf")` with a switch — simpler than a pattern, but it's a *central switch* that must be edited for every new product (Open-Closed violation) and cannot be subclassed for extension. Fine for small, closed sets; rejected when the product set is open or when the *choice* must be subclass-overridable.
- **Dependency Injection of the product object itself**: the *most decoupled* option — inject an already-constructed product rather than a factory. But DI requires the object to be created *before* the dependency graph is built and doesn't help when creation is *lazy* or *per-request* (each call needs a fresh product with varying params). Factory Method/Abstract Factory are chosen when creation must happen *inside* the framework/class lifecycle, or when each product needs fresh construction context.
- **Prototype (clone a template product)**: an alternative for "create many without naming concrete classes" when cloning is cheaper/cleaner than construction; rejected when products need non-copyable internal state or when the product's construction logic (not its state) is what varies.
- **Factory Method vs Abstract Factory (mutual alternative)**: Factory Method is chosen when there's *one product type* per creator and the subclass decides; Abstract Factory when there's a *family* of products and the factory *object* (chosen at run time) decides. If the family is fixed and small, Factory Method per product type may suffice — Abstract Factory is justified when family *consistency* matters.

## 5. Intuition
**Factory Method intuition**: A **pizza restaurant chain**. The corporate recipe (creator base class) says the *process* is identical — make dough, add toppings, bake, box. But the "create the pizza" step is deferred: each franchise *subclass* decides what goes on it (Margherita, Pepperoni). The customer (client) never says "make me a Pepperoni" with a specific recipe — the franchise (subclass) handles its own creation. The *framework* (corporate) defines the process; the *subclass* decides the product.

**Abstract Factory intuition**: An **operating system's control panel**. The dialog box is a *family* of widgets — window, button, scrollbar — and they must all match (a macOS look, or a Windows look). The Abstract Factory is the "look-and-feel factory": `MacFactory` produces the whole family consistently; `WinFactory` produces another consistent family. You never assemble a Mac button into a Windows dialog. The client just says "give me a theme-consistent dialog" and the factory hands out the family.

## 6. Real-World Analogy
- **Factory Method**: a **document template in a word processor**. The "New Document" command (creator) defines the flow — create a document, set up margins, open an editor — but the actual document object created (blank, letter, resume, report) is decided by the template you pick (the subclass). You, the user, ask for "New → Report", not for the raw classes underneath.
- **Abstract Factory**: a **furniture catalog**. You don't buy a "Scandinavian chair" plus an "industrial table" that clash; you buy from a *collection* (the factory) so everything matches — the "ScandinavianFactory" gives you the full suite, the "IndustrialFactory" gives you its suite. The collection (family) is the unit of consistency, exactly like a product family.

## 7. Formal Definition
> **Factory Method**: Define an interface for creating an object, but let **subclasses decide which class to instantiate**. Factory Method lets a class defer instantiation to subclasses. (GoF, p. 107)
>
> **Abstract Factory**: Provide an interface for creating **families of related or dependent objects** without specifying their concrete classes. (GoF, p. 87)

Key formal differences:
- Factory Method: *class-scope* (created via inheritance; the decision is baked into a subclass), **one product type**, the creator *is* the factory.
- Abstract Factory: *object-scope* (created via composition; the factory is a separate object, chosen/configured at run time), **many product types**, the factory is *separated* from the client.

## 8. Example
**Factory Method** — a logging framework:
```java
interface Logger { void log(String msg); }
class FileLogger implements Logger { public void log(String m) { /* append to file */ } }
class ConsoleLogger implements Logger { public void log(String m) { /* print */ } }

abstract class LoggerFactory {                       // creator
    abstract Logger createLogger();                  // factory method
    public void log(String msg) { createLogger().log(msg); }  // framework logic uses it
}
class FileLoggerFactory extends LoggerFactory { Logger createLogger() { return new FileLogger(); } }
class ConsoleLoggerFactory extends LoggerFactory { Logger createLogger() { return new ConsoleLogger(); } }
```
The client asks for `new FileLoggerFactory().log("hi")` — it never says `new FileLogger()` itself; the *subclass* decided the product.

**Abstract Factory** — a GUI family:
```java
interface Button { void render(); }
interface Dialog { void render(); }
interface UIFactory { Button createButton(); Dialog createDialog(); }

class WindowsButton implements Button { public void render() { System.out.println("[Win] button"); } }
class LinuxButton implements Button { public void render() { System.out.println("[Linux] button"); } }

class WindowsFactory implements UIFactory {
    public Button createButton() { return new WindowsButton(); }
    public Dialog createDialog() { return new WindowsDialog(); }
}
class LinuxFactory implements UIFactory {
    public Button createButton() { return new LinuxButton(); }
    public Dialog createDialog() { return new LinuxDialog(); }
}
// client:
void build(UIFactory f) {                          // can be Windows or Linux at runtime
    Button b = f.createButton();                    // never names the concrete class
    Dialog d = f.createDialog();
    b.render(); d.render();
}
```

## 9. Internal Working
**Factory Method internal flow:**
1. Client calls a method on a `ConcreteCreator` object (polymorphically typed as the abstract creator).
2. The abstract creator's *template* logic (e.g., `log()`) invokes the factory method `createLogger()`.
3. **Dynamic dispatch** (vtable lookup — Part 08) routes to the `ConcreteCreator`'s override, which executes `new ConcreteLogger()`.
4. The created product is returned as the interface type and used by the creator's logic.
5. Adding a new product = writing a new `ConcreteCreator` subclass. **Zero edits** to existing classes (Open-Closed).

**Abstract Factory internal flow:**
1. Client obtains a concrete factory (via configuration, a factory-of-factories, or DI — e.g., `UIFactory f = getFactoryFor(platform)`).
2. For each product needed, the client calls `f.createButton()`, `f.createDialog()`.
3. The concrete factory constructs the *matching* member of its family.
4. **Invariant maintained**: all products handed out belong to one family — the client can't accidentally mix `WindowsButton` with `LinuxDialog`.
5. Swapping the family = swapping the factory object at run time (a one-line change / config value).

Both patterns exploit **programming to an interface** + **dynamic dispatch**; the difference is the *granularity of the decision* (one product vs a family) and *where* the decision lives (subclass vs separate factory object).

## 10. Time Complexity
- **Factory Method**: O(1) to create a product (constructor + one virtual call). The factory method adds a single virtual dispatch (a vtable lookup) over a direct `new` — a constant-factor cost, no asymptotic change.
- **Abstract Factory**: O(1) per product created (one virtual call per product). The "cost" is architectural: N product types × M families classes, all O(1) in time.
- **Number of classes**: Factory Method — O(1) per product (a creator subclass); Abstract Factory — O(P×F) (products × factories) in the worst case. That class-count growth is the *structural* price of flexibility.
- **No effect on algorithms**: as with all patterns, Big-O of the underlying computation is unchanged; factories only relocate where construction happens.

## 11. Advantages
- **Open-Closed**: new products/families are *additions*, never modifications.
- **Dependency Inversion**: clients depend on `Product`/`Factory` abstractions, not concrete classes; swap implementations freely.
- **Family consistency (Abstract Factory)**: the factory guarantees products fit together — impossible to accidentally mix incompatible members.
- **Encapsulated construction**: creation complexity (params, resource setup) is hidden behind one method.
- **Testability**: factories make it trivial to inject fakes/mocks of the factory in tests.
- **Separation of concerns**: creator logic (process) is decoupled from product classes (data).

## 12. Disadvantages
- **Class explosion**: every product needs a creator subclass (Factory Method) and every family needs a factory + product classes (Abstract Factory) — more files, more boilerplate.
- **Indirection**: creation is no longer a visible `new`; debugging "where is this actually built?" requires following the factory chain.
- **Abstract Factory rigidity when extended**: adding a *new product type* to a family means editing *every* concrete factory (the "open/closed tension" — families are open to new families, less open to new product types).
- **Premature abstraction**: for a fixed, small product set, a simple static factory (or plain constructors) is clearer; patterns are overkill when no family/creation variation is predicted.
- **Complexity in modern languages**: in languages with first-class functions/DI containers, factory boilerplate is often replaceable by a lambda or a container-provided provider.

## 13. Interview Questions
1. **Q: What is the Factory Method pattern?** A: Define an interface for creating an object, but let *subclasses* decide which concrete class to instantiate; the creator's logic calls an overridable `create()` method without naming a concrete class.
2. **Q: What is the Abstract Factory pattern?** A: An interface for creating *families of related/dependent* products, where each concrete factory returns a consistent set (e.g., WindowsFactory → WindowsButton + WindowsDialog); the client depends only on the factory interface.
3. **Q: What problem do both factories solve?** A: The coupling caused by direct `new ConcreteClass()`: clients would name concrete classes everywhere, breaking Open-Closed (adding products edits call sites) and testability. Factories move creation behind an abstraction.
4. **Q: Difference between Factory Method and Abstract Factory?** A: Factory Method: one product type, decision made by a *subclass* (class-scope, compile-time wiring). Abstract Factory: a *family* of product types, decision made by a separate *factory object* chosen at run time (object-scope). Factory Method creates one thing via inheritance; Abstract Factory creates many related things via composition.
5. **Q: What is the difference between a *factory method* and a *static factory method*? (Tricky)** A: A factory method (pattern) is an *instance method, overridable by subclasses*, used by the creator's own logic to defer product choice. A static factory method is any static method that returns an instance (`Integer.valueOf()`, `Calendar.getInstance()`) — a *convention*, not a pattern, and it's not overridable. Don't confuse the two.
6. **Q: `Collection.iterator()` — which pattern is this?** A: It's a Factory Method: `Collection` defines the method; each concrete collection (`ArrayList`, `HashSet`) returns its own `Iterator` type via the override. The client never names the concrete iterator class.
7. **Q: When would you use Abstract Factory over Factory Method? (Scenario)** A: When you must create *several related products that must stay consistent*. Example: a cross-platform UI must create buttons AND dialogs that match one theme. Factory Method would let each product be chosen independently → you could mix Windows buttons with Linux dialogs; Abstract Factory binds the whole family.
8. **Q: Where does Spring use factories? (Production)** A: The IoC container's `BeanFactory`/`ApplicationContext` is an Abstract Factory: `getBean("name")` returns a bean of the configured type. `@Configuration` `@Bean` methods are *factory methods*. `ProxyFactoryBean` and `FactoryBean<T>` are factory abstractions in the framework.
9. **Q: Does Factory Method satisfy Open-Closed? Explain how.** A: Yes — adding a new product means adding a new creator subclass (open for extension) with zero modification to the existing creator, products, or clients (closed for modification). The framework logic is untouched.
10. **Q: What happens when you add a NEW PRODUCT TYPE to an existing Abstract Factory family? (Tricky)** A: You must edit *every* concrete factory to implement the new factory method — the family is "closed" to new product types (the factory-interface change ripples). This is the known trade-off: Abstract Factory is open to new *families*, closed to new *product types*. Mitigations: composition/registry approaches, or accept the ripple when families are stable.
11. **Q: How do factories help testing?** A: By depending on the factory/product interfaces, production code accepts injected fakes — a test can substitute a `MockFactory` returning in-memory products, avoiding real I/O, real DBs, or real network calls at construction time.
12. **Q: Factory Method vs Builder — when each?** A: Factory Method answers *which concrete class* (one step); Builder answers *how a complex object is assembled* (many steps, optional parts, fluent). Use a factory when the product is simple and the variation is the type; use a builder when the product has many optional configuration parts. They're commonly combined (a factory returns a builder).
13. **Q: Can you show a factory method in the JDK?** A: `Calendar.getInstance()`, `NumberFormat.getInstance()`, `Locale.forLanguageTag()`, `Collection.iterator()` — all return an interface/abstract type, hiding the concrete implementation chosen by context.
14. **Q: What's the "factory of factories"? (Tricky)** A: A pattern for choosing *which concrete factory* to use (e.g., a `PlatformUIFactory.getFactory("windows")` that returns the Windows factory) — often itself a static factory method. It's not a distinct GoF pattern; it's Factory Method applied to Abstract Factory selection.
15. **Q: JDBC's `DriverManager.getConnection(url)` — is it a factory? Which kind? (Production)** A: It's a *static factory / service-provider* mechanism: given a JDBC URL, it locates the right driver (a registry of `Driver` service providers) and returns a `Connection`. It's Abstract Factory-ish (each driver is a family: Connection, Statement, ResultSet) but implemented as a registry-based locator rather than the classic GoF shape. Interviewers like this nuance.
16. **Q: Would you use a factory for a class with a single, never-changing implementation?** A: No — that's premature abstraction (YAGNI). A factory earns its keep when the product set is open, chosen at run time, or must be mocked. For one concrete class, inject the object directly.
17. **Q: How is DI different from factories, and when does DI replace them?** A: DI *injects an already-constructed dependency*; factories *defer construction* (lazy, per-call, with params). A DI container (Spring) is itself built on factories and can inject a *provider* (`Provider<T>`/`Supplier<T>`) to get factory-like laziness. Factories remain necessary for run-time-varied or parameterized creation.
18. **Q: Which pattern would you use for "the notification system must support email/SMS/push, and new channels are expected"? (Scenario)** A: Factory Method is the baseline (a `NotifierFactory` per channel, or a registry). If channels come in *suites* (e.g., per-vendor: "vendor X's email+sms+push" must stay together), escalate to Abstract Factory. The choice is driven by whether you need a *family* or a *single product* per choice.
19. **Q: What are the GoF participants in Factory Method?** A: `Product` (interface), `ConcreteProduct` (implementation), `Creator` (declares the factory method), `ConcreteCreator` (overrides it). The creator's `factoryMethod()` and its `anOperation()` (which calls it) are the heart of the pattern.
20. **Q: Is Factory Method a "class" pattern? Is Abstract Factory an "object" pattern? Why?** A: Yes — Factory Method is class-scope (the product choice is decided by *inheritance*: which subclass you instantiate); Abstract Factory is object-scope (the choice is decided by *composition*: which factory object you hold). This is the GoF class-vs-object axis applied to creational patterns.

## 14. Follow-Up Questions
1. **Q: What is the "parameterized factory method"?** A: A factory method that takes a parameter (`createLogger("file")`) and switches internally. It's a simplification of the pattern (less subclassing) but reintroduces a central switch — fine for closed sets, less Open-Closed for open sets. Interviewers often probe "factory method with a switch argument — is that still the pattern?" (Answer: it's a common variant, but it trades subclass extensibility for simplicity).
2. **Q: How do you avoid editing factories when the family grows?** A: Use a *registry*: factories register themselves under a key (e.g., SPI / `ServiceLoader`, Spring's `FactoryBean` registry), so "adding a family" = adding a new registered factory class without editing a central switch.
3. **Q: How do factories interact with the Prototype pattern?** A: A factory can return *clones* of a prototype instead of `new` — useful when construction is expensive and the product varies only by state. This is a common production hybrid (see Section 04).
4. **Q: Factory Method and DI container — redundant or complementary?** A: Complementary — a DI container is a *factory infrastructure*; a Factory Method still governs *within* a class's logic when creation must be deferred to subclass behavior or vary per call. Frameworks (Spring) let you register a `FactoryBean`/provider to get both.
5. **Q: What does "dependent objects" mean in the Abstract Factory definition?** A: Products are *dependent* when they must interoperate within a family — e.g., a `Scrollbar` that must scroll a `Window` of the same look-and-feel. The factory's job is to guarantee products that are mutually consistent.

## 15. Coding Example
```java
// Abstract Factory — a cross-platform UI toolkit (full example)
interface Button { void paint(); }
interface TextField { void paint(); }

class WinButton implements Button { public void paint() { System.out.println("Windows button"); } }
class WinTextField implements TextField { public void paint() { System.out.println("Windows text field"); } }
class MacButton implements Button { public void paint() { System.out.println("macOS button"); } }
class MacTextField implements TextField { public void paint() { System.out.println("macOS text field"); } }

interface GUIFactory {
    Button createButton();
    TextField createTextField();
}
class WinFactory implements GUIFactory {
    public Button createButton() { return new WinButton(); }
    public TextField createTextField() { return new WinTextField(); }
}
class MacFactory implements GUIFactory {
    public Button createButton() { return new MacButton(); }
    public TextField createTextField() { return new MacTextField(); }
}

class App {                        // client depends ONLY on GUIFactory
    private final GUIFactory factory;
    App(GUIFactory f) { this.factory = f; }
    void render() {
        Button b = factory.createButton();
        TextField t = factory.createTextField();
        b.paint(); t.paint();
    }
}
public class Main {
    public static void main(String[] args) {
        GUIFactory f = "mac".equals(System.getenv("PLATFORM"))
                ? new MacFactory() : new WinFactory();   // family swap = 1 line
        new App(f).render();
    }
}
```
```python
# Abstract Factory in Python — protocol-based
from typing import Protocol, Type

class Button(Protocol):
    def paint(self) -> None: ...
class TextField(Protocol):
    def paint(self) -> None: ...

class WinButton:
    def paint(self) -> None: print("Windows button")
class MacButton:
    def paint(self) -> None: print("macOS button")
class WinTextField:
    def paint(self) -> None: print("Windows text field")
class MacTextField:
    def paint(self) -> None: print("macOS text field")

class WinFactory:
    def create_button(self) -> Button: return WinButton()
    def create_text_field(self) -> TextField: return WinTextField()

class MacFactory:
    def create_button(self) -> Button: return MacButton()
    def create_text_field(self) -> TextField: return MacTextField()

def render(factory) -> None:
    factory.create_button().paint()
    factory.create_text_field().paint()

render(WinFactory())
```
```cpp
// Factory Method in C++
#include <iostream>
#include <memory>

struct Logger { virtual void log(const std::string&) const = 0; virtual ~Logger() = default; };
struct FileLogger : Logger { void log(const std::string& m) const override { /* ... */ } };
struct ConsoleLogger : Logger { void log(const std::string& m) const override { std::cout << m << "\n"; } };

class LoggerFactory {                       // Creator (abstract)
public:
    virtual std::unique_ptr<Logger> createLogger() const = 0;   // factory method
    void log(const std::string& msg) const { createLogger()->log(msg); }
    virtual ~LoggerFactory() = default;
};
class ConsoleLoggerFactory : public LoggerFactory {
public:
    std::unique_ptr<Logger> createLogger() const override { return std::make_unique<ConsoleLogger>(); }
};
// Client:
int main() { ConsoleLoggerFactory f; f.log("hello via factory"); }
```

## 16. Industry Usage
- **JDK**: `Collection.iterator()` (Factory Method), `Calendar.getInstance()`, `NumberFormat.getInstance()` (static factories), `javax.xml.parsers.DocumentBuilderFactory` / `SAXParserFactory` / `TransformerFactory` (Abstract Factory-ish, registry-based), JDBC `DriverManager.getConnection` (factory locator).
- **Spring**: `BeanFactory`/`ApplicationContext` (Abstract Factory via `getBean`), `FactoryBean<T>`, `@Bean` factory methods, `ProxyFactoryBean` (combines factory + proxy). Bean *scopes* (prototype vs singleton) are a factory concern.
- **Hibernate/JPA**: `SessionFactory`, `EntityManagerFactory`, `RepositoryFactoryBean` — all abstract-factory-flavored creation of the persistence family (session, query, transaction).
- **Apache Commons**: `ConnectionFactory`, `SocketFactory`; **Netty**: `ChannelFactory` (bootstrap factories per protocol).
- **UI toolkits**: Java AWT/Swing's `Toolkit`, Qt's platform abstractions, Flutter's `ThemeData` — family-consistent widget creation = Abstract Factory in production.
- **Interviews**: "create objects without naming concrete classes" is a stock question; expect "difference between factory method and abstract factory", "is `getInstance()` a factory?", "where does Spring use factories?", and scenario questions about a notification/payment plugin system.

## 17. References
- **Gamma et al., *Design Patterns* — "Factory Method" (p. 107), "Abstract Factory" (p. 87)**: canonical definitions, participants, applicability.
- **Joshua Bloch, *Effective Java* (3rd ed.), Item 1**: "Consider static factory methods instead of constructors" — clarifies the *convention* distinct from the pattern.
- **Oracle Java Docs: `java.util.Collection.iterator()`, `Calendar.getInstance()`, `javax.xml.parsers.DocumentBuilderFactory`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Reference, "The IoC Container" (BeanFactory, FactoryBean)** — https://docs.spring.io/spring-framework/reference/core/beans/
- **refactoring.guru — "Factory Method" and "Abstract Factory"** — modern diagrams + Java/Python/C++ examples.
- **Baeldung — "Factory Method vs Abstract Factory"** — comparison articles with code.
- **Martin Fowler, "Inversion of Control Containers and the Dependency Injection pattern"** — the factory→container relationship.

## 18. Cheat Sheet
- **Factory Method**: interface to create *one* product; **subclass decides**; class-scope (inheritance); e.g., `Collection.iterator()`.
- **Abstract Factory**: interface to create a *family* of related products; **separate factory object decides**; object-scope (composition); e.g., a GUI toolkit per OS.
- Both replace `new Concrete()` → **client depends on abstractions** (DIP, Open-Closed).
- Factory Method vs static factory method: the pattern is an *overridable instance method*; the convention is any static method returning an instance.
- Abstract Factory downside: adding a *new product type* edits every concrete factory (open to new families, closed to new products).
- **Factory of factories**: a locator/registry choosing the concrete factory — not a separate GoF pattern.
- JDBC `DriverManager`, Spring `BeanFactory`, Hibernate `SessionFactory` = registry-based factories in production.
- When to use: product set is *open* or family consistency matters; otherwise simple constructors (YAGNI).
- Testability: inject a mock factory to avoid real I/O/DB/network at construction.
- Scenario hook: "new channels/plugins expected" → Factory Method; "products must stay compatible as a suite" → Abstract Factory.

## 19. Quiz
1. Factory Method decides the product via: a) a switch in a static method b) a subclass override c) a config file d) reflection → **b**
2. Abstract Factory creates: a) one product b) a family of related products c) abstract classes d) singletons → **b**
3. Which is object-scope (composition-based)? a) Factory Method b) Abstract Factory c) both d) neither → **b**
4. Adding a new product TYPE to an Abstract Factory family requires: a) editing every concrete factory b) adding one subclass c) nothing d) a new interface → **a**
5. `Collection.iterator()` is an example of: a) Abstract Factory b) Factory Method c) Singleton d) Builder → **b**
6. A static factory method differs from the Factory Method pattern in that it is: a) not overridable b) always thread-safe c) named `create` d) private → **a**
7. Which principle do factories primarily satisfy? a) Single Responsibility b) Dependency Inversion + Open-Closed c) Liskov d) Interface Segregation → **b**
8. Which best fits "button + checkbox + scrollbar must match one OS look"? a) Factory Method b) Singleton c) Abstract Factory d) Builder → **c**
9. The "factory of factories" is: a) a GoF pattern b) Factory Method choosing an Abstract Factory c) an anti-pattern d) a GUI toolkit → **b**
10. When is a factory NOT worth it? a) open product set b) run-time product choice c) fixed single implementation, no predicted change d) family consistency → **c**

## 20. Flashcards
- **Q: Factory Method intent?** → **A:** Let subclasses decide which concrete class to create (one product, class-scope).
- **Q: Abstract Factory intent?** → **A:** Create a family of related products without naming concrete classes (object-scope).
- **Q: Factory Method vs Abstract Factory in one line?** → **A:** FM = one product, subclass decides; AF = family of products, factory object decides.
- **Q: Why use a factory at all?** → **A:** Avoid `new Concrete()` coupling → DIP + Open-Closed + testability.
- **Q: JDK example of Factory Method?** → **A:** `Collection.iterator()`, `Calendar.getInstance()`, `NumberFormat.getInstance()`.
- **Q: Production factory examples?** → **A:** Spring `BeanFactory`, JDBC `DriverManager`, Hibernate `SessionFactory`.
- **Q: Abstract Factory's main downside?** → **A:** Adding a new product type forces edits to every concrete factory.
- **Q: Static factory method vs pattern?** → **A:** Static factory is a convention (any static method returning an instance); the pattern is an overridable instance method used by creator logic.

## 21. Revision
Both factories move creation behind an abstraction so clients depend on interfaces, not `new`. **Factory Method** (class-scope): the creator defines `createProduct()`; *subclasses* override it to decide the single product; the creator's logic calls it; adding a product = adding a subclass (Open-Closed). **Abstract Factory** (object-scope): a separate factory object creates a *family* of related products (button+checkbox+scrollbar per OS); the client holds the factory and never names concretes; family consistency is guaranteed; swapping the family = swapping the factory at run time. Key differences: one product vs a family; subclass (inheritance) vs factory object (composition). Real examples: `Collection.iterator()`, JDBC `DriverManager`, Spring `BeanFactory`, Hibernate `SessionFactory`. Watch the trap: static factory methods (a convention) ≠ the Factory Method pattern; and Abstract Factory is open to new *families* but closed to new *product types*. Use factories when the product set is open or family consistency matters; otherwise plain constructors (YAGNI).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain Factory Method / Abstract Factory." | 2 How It Works / 7 Formal Definition |
| "What's the difference between them?" | 8 Example / 13 Q4 / 14 Q1 |
| "When to use each? (scenario)" | 3 When Used / 13 Q7 / 13 Q18 |
| "Where does Spring/JDBC use factories?" | 13 Q8 / 13 Q15 / 16 Industry Usage |
| "Is `getInstance()` a factory method?" | 13 Q5 / 14 Q1 |
| "Why is Abstract Factory rigid for new product types?" | 13 Q10 / 14 Q2 |
| "How do factories help testing?" | 13 Q11 / 18 Cheat Sheet |
| "Factory Method vs Builder?" | 13 Q12 |
| "What are the GoF participants?" | 13 Q19 |
| "How do factories relate to DI?" | 13 Q17 / 14 Q4 |
