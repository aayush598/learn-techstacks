# System Design: 300+ Interview Q&A — Low-Level Design + High-Level Design

> **Target:** YC startups, FAANG, top-tier product companies  
> **Level:** SDE2 / Senior / Staff  
> **Covers:** LLD (OOP, patterns, OO models), HLD (scalable distributed systems), Scalability concepts

---

## Table of Contents

1. [Low-Level Design (Q1–Q100)](#low-level-design-q1q100)
2. [High-Level Design (Q101–Q250)](#high-level-design-q101q250)
3. [Scalability Concepts (Q251–Q300)](#scalability-concepts-q251q300)

---

# Low-Level Design (Q1–Q100)

## SOLID Principles (Q1–Q6)

### Q1: What is the Single Responsibility Principle (SRP)? Give an example.

**Answer:**

SRP states that a class should have **only one reason to change** — it should have a single, well-defined responsibility. This does not mean a class does only one thing; it means its changes should stem from a single actor or use case.

**Example — Violation:**

```java
class Invoice {
    void calculateTotal() { /* ... */ }
    void printInvoice() { /* ... */ }       // printing concern
    void saveToDatabase() { /* ... */ }      // persistence concern
}
```

Here `Invoice` has three reasons to change: business logic, output format, and storage.

**Refactored — SRP compliant:**

```java
class InvoiceCalculator {
    double calculate(Invoice invoice) { /* ... */ }
}
class InvoicePrinter {
    void print(Invoice invoice) { /* ... */ }
}
class InvoiceRepository {
    void save(Invoice invoice) { /* ... */ }
}
```

Each class has one responsibility. Changes to printing format affect only `InvoicePrinter`, not the calculation logic.

**Interview tip:** SRP is about **cohesion** — keeping related behaviors together and unrelated behaviors separate. Ask yourself: "If I change the business rules, does this class need to change?"

---

### Q2: What is the Open-Closed Principle (OCP)? Give an example.

**Answer:**

OCP states: **Software entities should be open for extension but closed for modification.** You should be able to add new functionality without altering existing code, typically via polymorphism or composition.

**Example — Violation:**

```java
class AreaCalculator {
    double area(Object shape) {
        if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            return Math.PI * c.radius * c.radius;
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            return r.width * r.height;
        }
        // Adding Triangle requires modifying this class
    }
}
```

**Refactored — OCP compliant:**

```java
interface Shape {
    double area();
}
class Circle implements Shape {
    double radius;
    public double area() { return Math.PI * radius * radius; }
}
class Rectangle implements Shape {
    double width, height;
    public double area() { return width * height; }
}
// Adding Triangle: just write Triangle implements Shape, no change to AreaCalculator
```

**Key insight:** Use abstraction (interfaces/abstract classes) to decouple client code from concrete implementations. New functionality comes as new implementations, not `if-else` chains.

---

### Q3: What is the Liskov Substitution Principle (LSP)? Give an example.

**Answer:**

LSP states: **If S is a subtype of T, then objects of type T should be replaceable with objects of type S without altering the correctness of the program.** Derived classes must be substitutable for their base classes.

**Example — Classic Rectangle-Square violation:**

```java
class Rectangle {
    int width, height;
    void setWidth(int w) { this.width = w; }
    void setHeight(int h) { this.height = h; }
    int area() { return width * height; }
}
class Square extends Rectangle {
    void setWidth(int w) { super.setWidth(w); super.setHeight(w); }
    void setHeight(int h) { super.setWidth(h); super.setHeight(h); }
}
// Client code:
void resize(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.area() == 50;  // Passes for Rectangle, fails for Square!
}
```

**Fix:** Don't model Square as a subclass of Rectangle. Use a common `Shape` interface or prefer composition.

```java
interface Shape {
    int area();
}
class Rectangle implements Shape { /* ... */ }
class Square implements Shape { /* ... */ }
```

**LSP rules (Bertrand Meyer):** Preconditions cannot be strengthened, postconditions cannot be weakened, invariants must be preserved, and the history constraint (no new mutable state that breaks base behavior).

---

### Q4: What is the Interface Segregation Principle (ISP)? Give an example.

**Answer:**

ISP states: **No client should be forced to depend on interfaces it does not use.** Large, "fat" interfaces should be split into smaller, more specific ones.

**Example — Violation:**

```java
interface Worker {
    void work();
    void eat();
    void sleep();
}
class HumanWorker implements Worker {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
}
class RobotWorker implements Worker {
    public void work() { /* ... */ }
    public void eat() { throw new UnsupportedOperationException(); }
    public void sleep() { throw new UnsupportedOperationException(); }
}
```

**Refactored — ISP compliant:**

```java
interface Workable {
    void work();
}
interface Eatable {
    void eat();
}
interface Sleepable {
    void sleep();
}
class HumanWorker implements Workable, Eatable, Sleepable { /* ... */ }
class RobotWorker implements Workable { /* ... */ }
```

**Key insight:** ISP leads to more focused, composable interfaces. Signals that a class has an interface it doesn't fully support.

---

### Q5: What is the Dependency Inversion Principle (DIP)? Give an example.

**Answer:**

DIP states: **High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions.**

This is NOT the same as dependency injection — DIP is the principle, DI is a technique to achieve it.

**Example — Violation:**

```java
class MySQLDatabase {
    void save(User user) { /* MySQL-specific code */ }
}
class UserService {
    private MySQLDatabase db = new MySQLDatabase();  // depends on concrete class
    void register(User u) { db.save(u); }
}
```

**Refactored — DIP compliant:**

```java
interface Database {
    void save(User user);
}
class MySQLDatabase implements Database { /* ... */ }
class PostgreSQLDatabase implements Database { /* ... */ }
class UserService {
    private Database db;  // depends on abstraction
    UserService(Database db) { this.db = db; }  // DI via constructor
    void register(User u) { db.save(u); }
}
```

**Key insight:** DIP inverts the traditional dependency direction. Both `UserService` (high-level) and `MySQLDatabase` (low-level) now depend on the `Database` abstraction. This enables swapping implementations, testing with mocks, and parallel development.

---

### Q6: Explain the SOLID principles together in a real-world scenario.

**Answer:**

Consider designing a **notification system**:

- **SRP:** `EmailSender` handles only email delivery. `SmsSender` handles only SMS. `NotificationService` orchestrates. Each has one reason to change.
- **OCP:** Add a new `PushNotificationSender` implementing `Sender` interface. `NotificationService` stays unchanged.
- **LSP:** Any `Sender` subtype can replace another. `EmailSender`, `SmsSender`, `PushSender` all satisfy the contract (same pre/post-conditions).
- **ISP:** Separate interfaces: `Sender` (send), `Trackable` (delivery status), `Configurable` (retry logic). Not every sender needs tracking.
- **DIP:** `NotificationService` depends on `Sender` abstraction, not on `JavaMailSender` concretely.

Result: flexible, testable, maintainable system. Adding a new channel = one new class + wiring. No existing code changes.

---

## Creational Design Patterns (Q7–Q15)

### Q7: Implement Singleton pattern — eager, lazy, and thread-safe versions.

**Answer:**

Singleton ensures a class has only **one instance** and provides a global access point.

**Eager Initialization:**

```java
class EagerSingleton {
    private static final EagerSingleton INSTANCE = new EagerSingleton();
    private EagerSingleton() {}
    public static EagerSingleton getInstance() { return INSTANCE; }
}
```
- **Pros:** Simple, thread-safe by JVM class-loading guarantee.
- **Cons:** Instance created even if never used.

**Lazy Initialization (not thread-safe):**

```java
class LazySingleton {
    private static LazySingleton instance;
    private LazySingleton() {}
    public static LazySingleton getInstance() {
        if (instance == null) instance = new LazySingleton();
        return instance;
    }
}
```

**Thread-safe (synchronized method):**

```java
class ThreadSafeSingleton {
    private static ThreadSafeSingleton instance;
    private ThreadSafeSingleton() {}
    public static synchronized ThreadSafeSingleton getInstance() {
        if (instance == null) instance = new ThreadSafeSingleton();
        return instance;
    }
}
```
- **Cons:** Synchronization overhead on every call.

**Double-Checked Locking (DCL):**

```java
class DCLSingleton {
    private static volatile DCLSingleton instance;
    private DCLSingleton() {}
    public static DCLSingleton getInstance() {
        if (instance == null) {
            synchronized (DCLSingleton.class) {
                if (instance == null) instance = new DCLSingleton();
            }
        }
        return instance;
    }
}
```
- `volatile` prevents instruction reordering (the instance published before constructor completes).
- Only synchronizes on first access.

**Bill Pugh (Initialization-on-demand holder idiom) — recommended:**

```java
class BillPughSingleton {
    private BillPughSingleton() {}
    private static class Holder {
        static final BillPughSingleton INSTANCE = new BillPughSingleton();
    }
    public static BillPughSingleton getInstance() {
        return Holder.INSTANCE;
    }
}
```
- **Why best:** Thread-safe without synchronization, lazy via inner class loading on first use.

**Enum Singleton (Joshua Bloch's recommendation):**

```java
enum EnumSingleton {
    INSTANCE;
    public void doSomething() { /* ... */ }
}
```
- **Why best:** Guarantees single instance, serialization-safe (no `readResolve` needed), protects against reflection attacks.

---

### Q8: Explain Factory Method pattern with a real example.

**Answer:**

Factory Method defines an **interface for creating an object** but lets subclasses decide which class to instantiate. It lets a class defer instantiation to subclasses.

**When to use:** A class can't anticipate the class of objects it must create. Subclasses specify which objects to create.

**Example — Logistics app:**

```java
interface Transport {
    void deliver();
}
class Truck implements Transport {
    public void deliver() { /* deliver by road */ }
}
class Ship implements Transport {
    public void deliver() { /* deliver by sea */ }
}
abstract class Logistics {
    abstract Transport createTransport();  // Factory Method
    void planDelivery() {
        Transport t = createTransport();
        t.deliver();
    }
}
class RoadLogistics extends Logistics {
    Transport createTransport() { return new Truck(); }
}
class SeaLogistics extends Logistics {
    Transport createTransport() { return new Ship(); }
}
```

**Usage:**
```java
Logistics logistics = new RoadLogistics();
logistics.planDelivery();  // Uses Truck
```

**Key benefit:** `Logistics` is closed for modification but open for extension. Adding `AirLogistics` with `Plane` transport doesn't touch existing code.

**Difference from Simple Factory:** Factory Method uses inheritance (subclass decides), Simple Factory uses a class with a static method (not a design pattern per GoF).

---

### Q9: Explain Abstract Factory pattern with a real example.

**Answer:**

Abstract Factory provides an interface for creating **families of related or dependent objects** without specifying their concrete classes.

**When to use:** System needs to be independent of how its products are created, composed, and represented, and you need to enforce consistency among products.

**Example — Cross-platform UI toolkit:**

```java
interface Button { void render(); }
interface Checkbox { void render(); }
interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

class WinButton implements Button { public void render() { /* Windows style */ } }
class MacButton implements Button { public void render() { /* macOS style */ } }
class WinCheckbox implements Checkbox { public void render() { /* Windows style */ } }
class MacCheckbox implements Checkbox { public void render() { /* macOS style */ } }

class WinFactory implements GUIFactory {
    public Button createButton() { return new WinButton(); }
    public Checkbox createCheckbox() { return new WinCheckbox(); }
}
class MacFactory implements GUIFactory {
    public Button createButton() { return new MacButton(); }
    public Checkbox createCheckbox() { return new MacCheckbox(); }
}
```

**Usage:**
```java
GUIFactory factory = new WinFactory();  // or MacFactory
Button b = factory.createButton();
Checkbox c = factory.createCheckbox();  // consistent Windows-style family
```

**Difference from Factory Method:** Factory Method is a single method; Abstract Factory is an object with multiple factory methods for a family of products. Factory Method uses inheritance; Abstract Factory uses composition.

---

### Q10: Explain Builder pattern with a real example.

**Answer:**

Builder separates the construction of a complex object from its representation, allowing the same construction process to create different representations.

**When to use:** Objects with many optional parameters, telescoping constructors become unreadable, or when construction involves multiple steps.

**Example — HTTP Request builder:**

```java
class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final String body;
    private final int timeout;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.headers = builder.headers;
        this.body = builder.body;
        this.timeout = builder.timeout;
    }

    static class Builder {
        private String url;
        private String method = "GET";
        private Map<String, String> headers = new HashMap<>();
        private String body = "";
        private int timeout = 5000;

        Builder url(String url) { this.url = url; return this; }
        Builder method(String method) { this.method = method; return this; }
        Builder header(String key, String value) { headers.put(key, value); return this; }
        Builder body(String body) { this.body = body; return this; }
        Builder timeout(int t) { this.timeout = t; return this; }
        HttpRequest build() { return new HttpRequest(this); }
    }
}
```

**Usage:**
```java
HttpRequest req = new HttpRequest.Builder()
    .url("https://api.example.com/data")
    .method("POST")
    .header("Authorization", "Bearer token")
    .body("{\"key\": \"value\"}")
    .timeout(10000)
    .build();
```

**Key benefit:** Readable, immutable objects, validation in `build()`, fluent API.

**Variations:** Classic Builder (abstract builder + director), Fluent Builder (method chaining), and Step Builder (enforces order of setting parameters).

---

### Q11: Explain Prototype pattern with a real example.

**Answer:**

Prototype creates new objects by **cloning an existing object** (the prototype) rather than calling a constructor. Useful when object creation is expensive or when you need copies that differ slightly.

**When to use:** Object creation is costly (DB call, network, complex computation), or you want to avoid subclassing.

**Example — Shape cloning for a graphic editor:**

```java
abstract class Shape implements Cloneable {
    int x, y;
    String color;
    abstract Shape clone();
}

class Circle extends Shape {
    int radius;
    Circle(Circle source) { super(source); this.radius = source.radius; }
    Circle clone() { return new Circle(this); }
}
class Rectangle extends Shape {
    int width, height;
    Rectangle(Rectangle source) { super(source); this.width = source.width; this.height = source.height; }
    Rectangle clone() { return new Rectangle(this); }
}
```

**Registry approach (prototype manager):**
```java
class ShapeCache {
    private static Map<String, Shape> cache = new HashMap<>();
    static Shape getShape(String key) { return cache.get(key).clone(); }
    static void loadCache() { /* populate with initial prototypes */ }
}
```

**Usage:**
```java
ShapeCache.loadCache();
Shape clonedCircle = ShapeCache.getShape("circle");
clonedCircle.x = 10;  // Modify without affecting original
```

**Key insight:** Java's `Cloneable` is broken (no `clone()` in interface). Better to define your own `clone()` method or use copy constructors, as shown above.

**vs. Builder:** Prototype creates by copying; Builder creates step by step.

---

### Q12: Explain Adapter pattern with a real example.

**Answer:**

Adapter allows incompatible interfaces to work together. It converts the interface of a class into another interface that clients expect.

**When to use:** You have an existing class with an incompatible interface and can't modify it. You need to integrate a legacy/third-party system.

**Two variants:** Class Adapter (inheritance) and Object Adapter (composition — preferred).

**Example — Payment gateway integration:**

```java
// Target interface
interface PaymentProcessor {
    void pay(double amount);
}

// Adaptee (legacy/third-party)
class StripeAPI {
    void charge(String cardNumber, double amount) {
        /* Stripe-specific logic */
    }
}

// Adapter (Object Adapter via composition)
class StripeAdapter implements PaymentProcessor {
    private StripeAPI stripe = new StripeAPI();
    private String cardNumber;

    StripeAdapter(String cardNumber) { this.cardNumber = cardNumber; }

    public void pay(double amount) {
        stripe.charge(cardNumber, amount);  // adapts the interface
    }
}

// Client
class CheckoutService {
    void checkout(PaymentProcessor processor, double amount) {
        processor.pay(amount);
    }
}
```

**Usage:**
```java
new CheckoutService().checkout(new StripeAdapter("4242-4242-4242-4242"), 100.0);
```

**Real-world:** `Arrays.asList()` adapts array to List interface. `InputStreamReader` adapts `InputStream` to `Reader`.

---

### Q13: Explain Bridge pattern with a real example.

**Answer:**

Bridge decouples an abstraction from its implementation so that the two can vary independently.

**When to use:** You want to avoid a permanent binding between abstraction and implementation. Both abstraction and implementation should be extensible by subclassing. Changes in the implementation should not affect clients.

**Example — Remote controls and devices:**

```java
interface Device {
    void turnOn();
    void turnOff();
    void setVolume(int percent);
}
class TV implements Device { /* ... */ }
class Radio implements Device { /* ... */ }

abstract class Remote {
    protected Device device;
    Remote(Device device) { this.device = device; }
    abstract void togglePower();
    abstract void volumeUp();
}
class BasicRemote extends Remote {
    BasicRemote(Device d) { super(d); }
    void togglePower() { /* on/off via device */ }
    void volumeUp() { device.setVolume(current + 10); }
}
class AdvancedRemote extends Remote {
    AdvancedRemote(Device d) { super(d); }
    void mute() { device.setVolume(0); }
    void togglePower() { /* ... */ }
    void volumeUp() { /* ... */ }
}
```

**Usage:**
```java
Device tv = new TV();
Remote remote = new AdvancedRemote(tv);
remote.togglePower();
remote.volumeUp();
((AdvancedRemote) remote).mute();
```

**Key insight:** Without Bridge, you'd need a class for every permutation (TV_BasicRemote, TV_AdvancedRemote, Radio_BasicRemote...). With Bridge, 2×2 = 4 classes instead of 2+2=4, but more importantly, you can add new devices or remotes independently.

**Difference from Adapter:** Adapter makes unrelated classes work together. Bridge is designed upfront to separate abstraction and implementation.

---

### Q14: Explain Composite pattern with a real example.

**Answer:**

Composite composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions **uniformly**.

**When to use:** You have a tree structure where leaves and composites should be treated identically.

**Example — File system:**

```java
interface FileSystemComponent {
    void showDetails();
    int getSize();
}

class File implements FileSystemComponent {
    private String name;
    private int size;
    File(String name, int size) { this.name = name; this.size = size; }
    public void showDetails() { System.out.println("File: " + name); }
    public int getSize() { return size; }
}

class Directory implements FileSystemComponent {
    private String name;
    private List<FileSystemComponent> children = new ArrayList<>();
    Directory(String name) { this.name = name; }
    void add(FileSystemComponent c) { children.add(c); }
    void remove(FileSystemComponent c) { children.remove(c); }
    public void showDetails() {
        System.out.println("Dir: " + name);
        for (FileSystemComponent c : children) c.showDetails();
    }
    public int getSize() {
        return children.stream().mapToInt(FileSystemComponent::getSize).sum();
    }
}
```

**Usage:**
```java
Directory root = new Directory("root");
root.add(new File("a.txt", 100));
Directory sub = new Directory("sub");
sub.add(new File("b.txt", 200));
root.add(sub);
root.showDetails();  // Uniformly traverses files and directories
System.out.println(root.getSize());  // 300
```

**Key insight:** The `Directory` and `File` share the same interface. Clients can treat them identically, enabling recursive composition.

---

### Q15: Explain Decorator pattern with a real example.

**Answer:**

Decorator attaches additional responsibilities to an object **dynamically** at runtime. It provides a flexible alternative to subclassing for extending functionality.

**When to use:** You need to add/remove behavior at runtime, or when subclassing would lead to an explosion of classes.

**Example — Coffee shop (beverages with add-ons):**

```java
interface Beverage {
    double cost();
    String description();
}

class Espresso implements Beverage {
    public double cost() { return 2.0; }
    public String description() { return "Espresso"; }
}

abstract class BeverageDecorator implements Beverage {
    protected Beverage beverage;
    BeverageDecorator(Beverage b) { this.beverage = b; }
}

class Milk extends BeverageDecorator {
    Milk(Beverage b) { super(b); }
    public double cost() { return beverage.cost() + 0.5; }
    public String description() { return beverage.description() + " + Milk"; }
}
class WhippedCream extends BeverageDecorator {
    WhippedCream(Beverage b) { super(b); }
    public double cost() { return beverage.cost() + 0.7; }
    public String description() { return beverage.description() + " + Whipped Cream"; }
}
class Soy extends BeverageDecorator {
    Soy(Beverage b) { super(b); }
    public double cost() { return beverage.cost() + 0.3; }
    public String description() { return beverage.description() + " + Soy"; }
}
```

**Usage:**
```java
Beverage drink = new Soy(new WhippedCream(new Milk(new Espresso())));
System.out.println(drink.description() + " = $" + drink.cost());
// "Espresso + Milk + Whipped Cream + Soy = $3.5"
```

**Key insight:** Decorator is a **structural** pattern that uses **composition** and recursion. Each decorator wraps the original, adding its behavior before/after delegating.

**Real-world:** Java's `BufferedReader` wraps `FileReader`: `new BufferedReader(new FileReader("file.txt"))`. Each layer adds functionality.

**vs. Proxy:** Decorator adds/modifies behavior; Proxy controls access. Decorator is transparent to the client; Proxy may hide the real object.

---

## Structural Design Patterns (Q16–Q20)

### Q16: Explain Facade pattern with a real example.

**Answer:**

Facade provides a **unified, simplified interface** to a set of interfaces in a subsystem. It defines a higher-level interface that makes the subsystem easier to use.

**When to use:** You want to provide a simple interface to a complex subsystem, decouple clients from subsystem components, or layer your subsystems.

**Example — Home theater system:**

```java
class Amplifier { void on() { /* ... */ } void setVolume(int v) { /* ... */ } }
class DVDPlayer { void play(String movie) { /* ... */ } }
class Projector { void on() { /* ... */ } void setInput(DVDPlayer d) { /* ... */ } }
class Screen { void down() { /* ... */ } void up() { /* ... */ } }
class Lights { void dim(int level) { /* ... */ } }

// Facade
class HomeTheaterFacade {
    private Amplifier amp = new Amplifier();
    private DVDPlayer dvd = new DVDPlayer();
    private Projector projector = new Projector();
    private Screen screen = new Screen();
    private Lights lights = new Lights();

    void watchMovie(String movie) {
        lights.dim(10);
        screen.down();
        projector.on();
        projector.setInput(dvd);
        amp.on();
        amp.setVolume(20);
        dvd.play(movie);
    }
    void endMovie() {
        lights.dim(100);
        screen.up();
        /* turn everything off */
    }
}

// Client — one call instead of 7+
new HomeTheaterFacade().watchMovie("Inception");
```

**Key insight:** Facade doesn't hide the subsystem — clients can still access individual components if needed. It's about providing convenience.

**Difference from Adapter:** Adapter changes interface to match what client expects. Facade provides a simpler interface to a larger body of code.

---

### Q17: Explain Flyweight pattern with a real example.

**Answer:**

Flyweight minimizes memory usage by **sharing** as much data as possible with similar objects. It separates **intrinsic** (shared, immutable) state from **extrinsic** (context-specific, passed by client) state.

**When to use:** Large numbers of similar objects cause memory issues, and the objects can share common state.

**Example — Text editor character rendering:**

```java
// Flyweight (intrinsic: glyph data)
class Glyph {
    private final char symbol;
    private final String fontFamily;
    private final int fontSize;
    Glyph(char symbol, String fontFamily, int fontSize) { /* ... */ }
    void render(int x, int y, boolean bold, boolean italic) {
        // extrinsic state (position, style) passed by client
    }
}

// Flyweight Factory
class GlyphFactory {
    private Map<String, Glyph> cache = new HashMap<>();
    Glyph getGlyph(char symbol, String font, int size) {
        String key = symbol + ":" + font + ":" + size;
        return cache.computeIfAbsent(key, k -> new Glyph(symbol, font, size));
    }
}

// Client code — stores extrinsic state
class Character {
    Glyph glyph;
    int x, y;
    boolean bold, italic;
}
```

**Key insight:** In a document with 10K characters, instead of 10K Glyph objects, you have maybe 100 unique (char, font, size) combinations shared. The extrinsic state (position, style) is stored per-character externally.

**Real-world:** Java `String.intern()`, Integer cache (-128 to 127).

---

### Q18: Explain Proxy pattern with a real example.

**Answer:**

Proxy provides a **surrogate or placeholder** for another object to control access to it. Common types: virtual proxy (lazy loading), protection proxy (access control), remote proxy (RPC), logging proxy.

**When to use:** You need lazy initialization, access control, logging, or remote communication without changing the client's code.

**Example — Virtual proxy for image loading:**

```java
interface Image {
    void display();
}

class RealImage implements Image {
    private String filename;
    RealImage(String filename) {
        this.filename = filename;
        loadFromDisk();  // Expensive operation
    }
    private void loadFromDisk() { /* heavy I/O */ }
    public void display() { /* show image */ }
}

class ImageProxy implements Image {
    private RealImage realImage;
    private String filename;
    ImageProxy(String filename) { this.filename = filename; }
    public void display() {
        if (realImage == null) realImage = new RealImage(filename);  // lazy
        realImage.display();
    }
}
```

**Usage:**
```java
Image image = new ImageProxy("large_photo.jpg");  // No load yet
image.display();  // First access triggers load
image.display();  // Already loaded
```

**Protection proxy example:**

```java
class BankAccountProxy implements BankAccount {
    private RealBankAccount account;
    private String userRole;
    void withdraw(double amount) {
        if (!userRole.equals("admin")) throw new SecurityException();
        account.withdraw(amount);
    }
}
```

**Difference from Decorator:** Proxy controls access/delegates lifecycle, often creating the real object. Decorator adds behavior, always delegating to the wrapped object.

---

### Q19: Explain Chain of Responsibility pattern with a real example.

**Answer:**

Chain of Responsibility lets you pass requests along a chain of handlers. Each handler decides either to process the request or pass it to the next handler in the chain.

**When to use:** Multiple handlers can process a request, and the handler is determined at runtime. You want to decouple sender and receiver.

**Example — Middleware/HTTP request processing:**

```java
abstract class Handler {
    private Handler next;
    void setNext(Handler next) { this.next = next; }
    void handle(Request request) {
        if (doHandle(request)) return;           // handled
        if (next != null) next.handle(request);   // pass along
    }
    abstract boolean doHandle(Request request);
}

class AuthenticationHandler extends Handler {
    boolean doHandle(Request r) {
        if (r.getToken() == null) { /* reject */ return true; }
        return false;  // pass to next
    }
}
class RateLimitHandler extends Handler {
    boolean doHandle(Request r) {
        if (/* rate limited */) { /* reject */ return true; }
        return false;
    }
}
class LoggingHandler extends Handler {
    boolean doHandle(Request r) {
        System.out.println("Request: " + r);
        return false;  // always pass to next
    }
}

// Build chain:
Handler chain = new AuthenticationHandler();
chain.setNext(new RateLimitHandler());
chain.setNext(new LoggingHandler());
chain.handle(request);
```

**Real-world:** Servlet filters (`javax.servlet.Filter`), exception handling in catch blocks, Java's `logging` framework handlers.

---

### Q20: Explain Command pattern with a real example.

**Answer:**

Command encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

**When to use:** You need parameterize objects by an action to perform, queue/execute operations at different times, or support undo/redo.

**Example — Remote control for smart home:**

```java
interface Command {
    void execute();
    void undo();
}

class Light { void on() { /* ... */ } void off() { /* ... */ } }
class LightOnCommand implements Command {
    private Light light;
    LightOnCommand(Light l) { this.light = l; }
    public void execute() { light.on(); }
    public void undo() { light.off(); }
}

class RemoteControl {
    private Command[] onCommands = new Command[7];
    private Command[] offCommands = new Command[7];
    private Command lastCommand;
    void setCommand(int slot, Command on, Command off) {
        onCommands[slot] = on; offCommands[slot] = off;
    }
    void pressOn(int slot) { onCommands[slot].execute(); lastCommand = onCommands[slot]; }
    void pressUndo() { lastCommand.undo(); }
}
```

**Usage:**
```java
Light livingLight = new Light();
RemoteControl remote = new RemoteControl();
remote.setCommand(0, new LightOnCommand(livingLight), new LightOffCommand(livingLight));
remote.pressOn(0);  // Light on
remote.pressUndo(); // Light off
```

**Key insight:** Command decouples the invoker (remote) from receiver (light). You can also support composite commands (macros), command queuing, and logging.

---

### Q21: Explain Interpreter pattern with a real example.

**Answer:**

Interpreter defines a grammar for a language and an interpreter that uses the grammar to interpret sentences in the language.

**When to use:** Grammar is simple, efficiency is not critical, and you need to parse and evaluate expressions.

**Example — Arithmetic expression evaluator:**

```java
interface Expression {
    int interpret();
}

class Number implements Expression {
    private int value;
    Number(int v) { this.value = v; }
    public int interpret() { return value; }
}

class Add implements Expression {
    private Expression left, right;
    Add(Expression l, Expression r) { left = l; right = r; }
    public int interpret() { return left.interpret() + right.interpret(); }
}
class Subtract implements Expression {
    private Expression left, right;
    Subtract(Expression l, Expression r) { left = l; right = r; }
    public int interpret() { return left.interpret() - right.interpret(); }
}

// "5 + 3 - 2" as AST:
Expression expr = new Subtract(new Add(new Number(5), new Number(3)), new Number(2));
System.out.println(expr.interpret());  // 6
```

**Key insight:** Each grammar rule becomes a class. The pattern is recursive: composite expressions contain sub-expressions.

**Limitation:** For complex grammars, use parser generators (ANTLR, yacc) instead.

---

### Q22: Explain Iterator pattern with a real example.

**Answer:**

Iterator provides a way to access elements of an aggregate object sequentially without exposing its underlying representation.

**When to use:** You want to traverse different collections uniformly, support multiple traversal strategies, or hide the collection's internal structure.

**Example — Tree traversal (DFS, BFS):**

```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}

interface Iterable<T> {
    Iterator<T> iterator();
}

class TreeNode<T> {
    T value;
    List<TreeNode<T>> children = new ArrayList<>();

    Iterator<T> dfsIterator() {
        return new DFSIterator<>(this);
    }
    Iterator<T> bfsIterator() {
        return new BFSIterator<>(this);
    }
}

class DFSIterator<T> implements Iterator<T> {
    private Stack<TreeNode<T>> stack = new Stack<>();
    DFSIterator(TreeNode<T> root) { stack.push(root); }
    public boolean hasNext() { return !stack.isEmpty(); }
    public T next() {
        TreeNode<T> node = stack.pop();
        for (int i = node.children.size() - 1; i >= 0; i--)
            stack.push(node.children.get(i));
        return node.value;
    }
}

// Usage
TreeNode<Integer> root = /* build tree */;
Iterator<Integer> it = root.dfsIterator();
while (it.hasNext()) System.out.println(it.next());
```

**Real-world:** Java's `Iterator` interface, `for (T item : collection)` in Java/C#.

---

### Q23: Explain Mediator pattern with a real example.

**Answer:**

Mediator reduces coupling between objects by making them communicate indirectly through a mediator object, instead of referring to each other explicitly.

**When to use:** Many objects interact in complex ways, making the system hard to understand and change.

**Example — Air traffic control:**

```java
interface AirTrafficControl {
    void sendMessage(String msg, Airplane sender);
    void registerAirplane(Airplane a);
}

class Tower implements AirTrafficControl {
    private List<Airplane> airplanes = new ArrayList<>();
    public void registerAirplane(Airplane a) { airplanes.add(a); }
    public void sendMessage(String msg, Airplane sender) {
        for (Airplane a : airplanes)
            if (a != sender) a.receive(msg);
    }
}

class Airplane {
    private String id;
    private AirTrafficControl atc;
    Airplane(String id, AirTrafficControl atc) {
        this.id = id;
        this.atc = atc;
        atc.registerAirplane(this);
    }
    void send(String msg) { atc.sendMessage(id + ": " + msg, this); }
    void receive(String msg) { System.out.println(id + " received: " + msg); }
}
```

**Real-world:** Chat room (users communicate through room), Java AWT `EventQueue`, GUI components coordinated by a controller.

**vs. Observer:** Mediator centralizes communication between objects. Observer distributes communication (many-to-many).

---

### Q24: Explain Memento pattern with a real example.

**Answer:**

Memento captures and externalizes an object's internal state so the object can be restored later without violating encapsulation.

**When to use:** You need undo/rollback functionality, and you must preserve encapsulation boundaries.

**Example — Text editor undo:**

```java
// Memento
class EditorMemento {
    private final String content;
    private final int cursorPosition;
    EditorMemento(String content, int pos) {
        this.content = content;
        this.cursorPosition = pos;
    }
    String getContent() { return content; }
    int getCursorPosition() { return cursorPosition; }
}

// Originator
class Editor {
    private String content = "";
    private int cursorPosition = 0;

    void type(String words) { content += words; cursorPosition = content.length(); }
    EditorMemento save() { return new EditorMemento(content, cursorPosition); }
    void restore(EditorMemento memento) {
        content = memento.getContent();
        cursorPosition = memento.getCursorPosition();
    }
}

// Caretaker
class History {
    private Stack<EditorMemento> states = new Stack<>();
    void push(EditorMemento m) { states.push(m); }
    EditorMemento pop() { return states.pop(); }
}

// Usage
Editor editor = new Editor();
History history = new History();

history.push(editor.save());
editor.type("Hello, ");
history.push(editor.save());
editor.type("World!");

System.out.println(editor);  // "Hello, World!"
editor.restore(history.pop());
System.out.println(editor);  // "Hello, "
```

**Key insight:** Memento maintains encapsulation — the originator's internal state is not exposed to the caretaker. The memento is opaque to the caretaker.

---

### Q25: Explain Observer (Pub-Sub) pattern with a real example.

**Answer:**

Observer defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.

**When to use:** Changes to one object require changing others, and you don't know how many objects need to change.

**Example — Stock price notifications:**

```java
interface Observer {
    void update(String stockSymbol, double price);
}

class StockExchange {  // Subject / Publisher
    private Map<String, List<Observer>> observers = new HashMap<>();
    private Map<String, Double> prices = new HashMap<>();

    void subscribe(String stockSymbol, Observer o) {
        observers.computeIfAbsent(stockSymbol, k -> new ArrayList<>()).add(o);
    }
    void unsubscribe(String stockSymbol, Observer o) {
        observers.getOrDefault(stockSymbol, new ArrayList<>()).remove(o);
    }
    void setPrice(String stockSymbol, double price) {
        prices.put(stockSymbol, price);
        notifyObservers(stockSymbol, price);
    }
    private void notifyObservers(String stockSymbol, double price) {
        for (Observer o : observers.getOrDefault(stockSymbol, List.of())) {
            o.update(stockSymbol, price);
        }
    }
}

class MobileApp implements Observer {
    public void update(String symbol, double price) {
        System.out.println("MobileApp: " + symbol + " now $" + price);
    }
}

// Usage
StockExchange exchange = new StockExchange();
exchange.subscribe("AAPL", new MobileApp());
exchange.setPrice("AAPL", 150.25);  // MobileApp notified
```

**Key insight:** Observer promotes loose coupling — the subject knows only that observers implement the `Observer` interface. You can add new observers without modifying the subject.

**Push vs Pull:** Push (subject sends all data) may be wasteful but simpler. Pull (observer fetches what it needs) is more efficient but observers need a reference to the subject.

**Real-world:** Java's `java.util.Observer`/`Observable` (deprecated), event listeners in UI frameworks, Kafka pub-sub.

---

### Q26: Explain State pattern with a real example.

**Answer:**

State allows an object to alter its behavior when its internal state changes. The object appears to change its class.

**When to use:** An object's behavior depends on its state and must change at runtime, or you have large conditional statements that depend on state.

**Example — Vending machine states:**

```java
interface VendingMachineState {
    void insertCoin();
    void selectProduct(String product);
    void dispense();
}

class NoCoinState implements VendingMachineState {
    private VendingMachine machine;
    NoCoinState(VendingMachine m) { this.machine = m; }
    public void insertCoin() {
        System.out.println("Coin inserted");
        machine.setState(machine.getHasCoinState());
    }
    public void selectProduct(String p) { System.out.println("Insert coin first"); }
    public void dispense() { System.out.println("Insert coin first"); }
}

class HasCoinState implements VendingMachineState {
    private VendingMachine machine;
    HasCoinState(VendingMachine m) { this.machine = m; }
    public void insertCoin() { System.out.println("Coin already inserted"); }
    public void selectProduct(String p) {
        if (machine.hasProduct(p) && machine.getPrice(p) <= machine.getBalance()) {
            System.out.println("Product selected: " + p);
            machine.setState(machine.getDispensingState());
        }
    }
    public void dispense() { System.out.println("Select product first"); }
}

class DispensingState implements VendingMachineState { /* ... */ }

class VendingMachine {
    private VendingMachineState noCoinState = new NoCoinState(this);
    private VendingMachineState hasCoinState = new HasCoinState(this);
    private VendingMachineState dispensingState = new DispensingState(this);
    private VendingMachineState currentState = noCoinState;
    private int balance;

    void setState(VendingMachineState s) { this.currentState = s; }
    void insertCoin() { currentState.insertCoin(); }
    void selectProduct(String p) { currentState.selectProduct(p); }
    void dispense() { currentState.dispense(); }
    // getters...
}
```

**Key insight:** State pattern eliminates long if-else/switch chains. Each state is a separate class. Transitions are explicit.

**vs. Strategy:** Strategy selects an algorithm (how to do something). State changes behavior based on internal state (what to do). In Strategy, the client sets the strategy. In State, the state object itself controls transitions.

---

### Q27: Explain Strategy pattern with a real example.

**Answer:**

Strategy lets you define a family of algorithms, encapsulate each one, and make them interchangeable. The strategy pattern lets the algorithm vary independently from clients that use it.

**When to use:** You have multiple ways to perform an operation, and you want to select the algorithm at runtime.

**Example — Payment methods in e-commerce:**

```java
interface PaymentStrategy {
    void pay(double amount);
}

class CreditCardPayment implements PaymentStrategy {
    private String cardNumber;
    CreditCardPayment(String cn) { this.cardNumber = cn; }
    public void pay(double amount) {
        System.out.println("Paid $" + amount + " via Credit Card " + cardNumber);
    }
}

class PayPalPayment implements PaymentStrategy {
    private String email;
    PayPalPayment(String e) { this.email = e; }
    public void pay(double amount) {
        System.out.println("Paid $" + amount + " via PayPal " + email);
    }
}

class CryptoPayment implements PaymentStrategy {
    private String walletAddress;
    CryptoPayment(String w) { this.walletAddress = w; }
    public void pay(double amount) { /* crypto logic */ }
}

class ShoppingCart {
    private List<Item> items = new ArrayList<>();
    private PaymentStrategy paymentStrategy;

    void setPaymentStrategy(PaymentStrategy ps) { this.paymentStrategy = ps; }
    void checkout() {
        double total = items.stream().mapToDouble(Item::getPrice).sum();
        paymentStrategy.pay(total);
    }
}

// Usage
ShoppingCart cart = new ShoppingCart();
cart.setPaymentStrategy(new CreditCardPayment("1234-5678"));
cart.checkout();  // Seamlessly switch algorithms
```

**Key insight:** Favor composition over inheritance. The context (ShoppingCart) delegates algorithm implementation to a strategy object.

**Real-world:** Java's `Comparator` interface — sorting strategies; `Collections.sort(list, comparator)`.

---

### Q28: Explain Template Method pattern with a real example.

**Answer:**

Template Method defines the **skeleton of an algorithm** in a method, deferring some steps to subclasses. Subclasses can redefine certain steps without changing the algorithm's structure.

**When to use:** You want to avoid code duplication in algorithms that share the same structure but differ in some steps.

**Example — Data migration pipeline:**

```java
abstract class DataMigration {
    // Template method — defines the skeleton
    final void migrate() {
        extract();
        transform();
        load();
        if (postProcessRequired()) postProcess();
        cleanup();
        logCompletion();
    }
    abstract void extract();
    abstract void transform();
    abstract void load();
    boolean postProcessRequired() { return false; }  // Hook method
    void postProcess() { /* optional */ }
    void cleanup() { /* default: close connections */ }
    void logCompletion() { System.out.println("Migration complete"); }
}

class CSVToDatabaseMigration extends DataMigration {
    void extract() { /* read CSV */ }
    void transform() { /* parse/validate */ }
    void load() { /* SQL INSERT */ }
    boolean postProcessRequired() { return true; }
    void postProcess() { /* generate summary report */ }
}

// Usage
new CSVToDatabaseMigration().migrate();
```

**Key insight:** The template method is typically declared `final` so subclasses can't change the algorithm structure. Hooks (like `postProcessRequired`) give optional extension points.

**vs. Strategy:** Template Method uses inheritance to vary parts of an algorithm. Strategy uses composition to swap entire algorithms.

---

### Q29: Explain Visitor pattern with a real example.

**Answer:**

Visitor lets you define a new operation on a set of objects without changing the objects' classes. It separates the algorithm from the objects it operates on.

**When to use:** You need to perform many distinct and unrelated operations on objects in a structure, and you want to avoid polluting their classes with these operations.

**Example — File system export (HTML, XML, JSON):**

```java
interface FileElement {
    void accept(Visitor v);
}

class TextFile implements FileElement {
    String name, content;
    TextFile(String n, String c) { name = n; content = c; }
    public void accept(Visitor v) { v.visit(this); }
}
class ImageFile implements FileElement {
    String name, metadata;
    ImageFile(String n, String m) { name = n; metadata = m; }
    public void accept(Visitor v) { v.visit(this); }
}

interface Visitor {
    void visit(TextFile file);
    void visit(ImageFile file);
}

class HTMLExportVisitor implements Visitor {
    public void visit(TextFile f) {
        System.out.println("<div class='text'>" + f.content + "</div>");
    }
    public void visit(ImageFile f) {
        System.out.println("<img src='" + f.name + "' alt='" + f.metadata + "' />");
    }
}

class XMLExportVisitor implements Visitor { /* ... */ }

// Usage
List<FileElement> files = List.of(new TextFile("readme.txt", "Hello"), new ImageFile("pic.jpg", "photo"));
Visitor htmlVisitor = new HTMLExportVisitor();
for (FileElement f : files) f.accept(htmlVisitor);
```

**Key insight:** The "double dispatch" pattern — the operation depends on both the element type and the visitor type. Adding a new operation = add a new visitor class. Adding a new element type requires changing all visitors.

**Tradeoff:** Violates OCP if element hierarchy changes frequently. Use when operations change more often than element types.

---

## Architectural Patterns (Q30–Q38)

### Q30: Compare MVC, MVP, and MVVM.

**Answer:**

| Aspect | MVC | MVP | MVVM |
|--------|-----|-----|------|
| **Controller/Presenter/VM** | Controller handles input, updates Model, selects View | Presenter handles all UI logic, updates View | ViewModel exposes data bindings, no direct View reference |
| **View responsibility** | Displays data, sends input to Controller | Passes all events to Presenter, is passive | Binds to ViewModel properties (data-binding) |
| **Model-View communication** | View observes Model (Observer) for changes | Presenter updates View. View never touches Model | ViewModel exposes Model data for binding. View bind to VM |
| **Testability** | Moderate (View depends on Model) | High (Presenter is unit-testable, View is mockable) | High (ViewModel is testable without UI) |
| **Complexity** | Simple, but can become messy | More boilerplate (interfaces for View) | Best with data-binding frameworks |

**Key difference:** In MVC, the View directly observes the Model. In MVP, the Presenter mediates all communication. In MVVM, the ViewModel exposes streams/commands that the View binds to.

**When to use which:**
- **MVC:** Web apps (Rails, Spring MVC) — stateless request/response
- **MVP:** Android apps, WinForms — where testing is critical
- **MVVM:** WPF, Angular, React (unidirectional data flow), SwiftUI

---

### Q31: Explain Repository pattern.

**Answer:**

Repository mediates between the domain and data mapping layers, acting like an **in-memory collection** of domain objects. It centralizes data access logic, provides a collection-like interface, and decouples domain logic from data access.

```java
interface UserRepository {
    User findById(String id);
    List<User> findByRole(Role role);
    void save(User user);
    void delete(String id);
}

class MySQLUserRepository implements UserRepository {
    private DataSource dataSource;
    public User findById(String id) {
        // SQL query, map ResultSet to User domain object
    }
    public void save(User user) {
        // INSERT or UPDATE
    }
}

// Domain layer uses repository interface only
class UserService {
    private UserRepository userRepo;
    UserService(UserRepository repo) { this.userRepo = repo; }
    void promoteUser(String userId) {
        User user = userRepo.findById(userId);
        user.promote();
        userRepo.save(user);
    }
}
```

**Key benefits:**
- Centralizes data access logic
- Swappable implementations (MySQL, PostgreSQL, in-memory, mock)
- Domain logic is persistence-ignorant
- Easy to unit test with mock repositories

**vs. DAO:** Repository is a higher-level concept focusing on domain objects. DAO is lower-level, often matching table structures. Repository may use multiple DAOs.

---

### Q32: Explain Unit of Work pattern.

**Answer:**

Unit of Work maintains a list of objects affected by a business transaction and coordinates the writing out of changes and the resolution of concurrency problems.

**When to use:** You need to track changes during a transaction and commit them atomically. Commonly used with Repository.

```java
class UnitOfWork {
    private Set<Entity> newEntities = new HashSet<>();
    private Set<Entity> dirtyEntities = new HashSet<>();
    private Set<Entity> removedEntities = new HashSet<>();

    void registerNew(Entity e) { newEntities.add(e); }
    void registerDirty(Entity e) { dirtyEntities.add(e); }
    void registerRemoved(Entity e) { removedEntities.add(e); }

    void commit() {
        beginTransaction();
        try {
            for (Entity e : newEntities) insert(e);
            for (Entity e : dirtyEntities) update(e);
            for (Entity e : removedEntities) delete(e);
            commitTransaction();
        } catch (Exception e) {
            rollbackTransaction();
            throw e;
        } finally {
            clear();
        }
    }
    private void clear() { newEntities.clear(); dirtyEntities.clear(); removedEntities.clear(); }
}
```

**Real-world:** Entity Framework's `DbContext` (EF Core), Hibernate's `Session` (flush/commit).

---

### Q33: Explain Dependency Injection pattern.

**Answer:**

Dependency Injection is a technique where an object receives its dependencies from an external source rather than creating them internally. It implements the Dependency Inversion Principle.

**Types of DI:**

1. **Constructor Injection** (preferred):
```java
class OrderService {
    private final PaymentGateway gateway;
    private final EmailService emailService;
    OrderService(PaymentGateway g, EmailService e) {
        this.gateway = g;
        this.emailService = e;
    }
}
```

2. **Setter Injection** (optional dependencies):
```java
class NewsService {
    private CacheProvider cache;
    void setCacheProvider(CacheProvider c) { this.cache = c; }
}
```

3. **Interface Injection** (less common):
```java
interface CacheAware { void setCache(CacheProvider c); }
class NewsService implements CacheAware { /* ... */ }
```

**DI Container / IoC Container:**
```java
Container container = new Container();
container.register(PaymentGateway.class, StripeGateway.class);
container.register(EmailService.class, SmtpEmailService.class);
container.register(OrderService.class, OrderService.class);

OrderService service = container.resolve(OrderService.class);
// Automatically resolves dependencies
```

**Benefits:** Loose coupling, testability (easy mocking), flexibility to swap implementations.

---

### Q34: Explain CQRS pattern.

**Answer:**

CQRS (Command Query Responsibility Segregation) separates read and write operations into different models, using different objects, often different databases.

**Core idea:** Commands (write) and Queries (read) should use separate models:
- **Command:** Changes state. Returns void (or ID). No side-effect-free queries.
- **Query:** Returns data. No state changes.

```java
// Command side
interface CommandHandler<C extends Command> {
    void handle(C command);
}
class CreateOrderCommand implements Command { /* order data */ }
class CreateOrderHandler implements CommandHandler<CreateOrderCommand> {
    private OrderWriteRepository writeRepo;
    public void handle(CreateOrderCommand cmd) {
        Order order = new Order(cmd);
        writeRepo.save(order);
    }
}

// Query side
class OrderQueryService {
    private OrderReadRepository readRepo;
    OrderDTO getOrder(String id) { return readRepo.findById(id); }
    List<OrderSummaryDTO> getOrdersByUser(String userId) { /* ... */ }
}
```

**When to use CQRS:**
- Read and write workloads are imbalanced (many reads, few writes)
- Different data shapes for read vs. write (denormalized reads)
- Complex domain logic on write side, simple projections on read
- Multiple teams working on read/write separately

**Without CQRS (CRUD):** Same model for reads and writes, which may lead to complex joins for queries or anemic domain models.

**With Event Sourcing:** CQRS pairs naturally with event sourcing — write side stores events, read side projects event streams into denormalized views.

**Caveat:** Do NOT use CQRS unless you have clear benefits — it adds complexity (eventual consistency, separate infrastructure).

---

### Q35: Explain Event Sourcing pattern.

**Answer:**

Event Sourcing stores the **state of an entity as a sequence of state-changing events**, rather than storing the current state. To get the current state, replay all events for that entity.

**Core concepts:**

```java
// Event
class OrderCreatedEvent {
    String orderId;
    String customerId;
    List<OrderLineItem> items;
}
class OrderShippedEvent {
    String orderId;
    LocalDateTime shippedAt;
}

// Aggregate — rebuilds state from events
class Order {
    private String orderId;
    private OrderStatus status;
    private List<Event> changes = new ArrayList<>();

    static Order recreate(List<Event> events) {
        Order order = new Order();
        for (Event e : events) order.apply(e);
        return order;
    }
    void create(String customerId, List<OrderLineItem> items) {
        apply(new OrderCreatedEvent(UUID.randomUUID().toString(), customerId, items));
    }
    private void apply(Event e) {
        if (e instanceof OrderCreatedEvent oce) { this.orderId = oce.orderId; this.status = CREATED; }
        if (e instanceof OrderShippedEvent) { this.status = SHIPPED; }
        changes.add(e);  // Append to uncommitted changes
    }
    List<Event> getUncommittedChanges() { return changes; }
}

// Event Store — append-only log
class EventStore {
    void save(String aggregateId, List<Event> events, int expectedVersion) { /* atomic append */ }
    List<Event> getEvents(String aggregateId) { /* read events */ }
}
```

**Benefits:**
- **Audit trail:** Complete history of every change
- **Temporal queries:** What was the state at any point in time?
- **Event-driven:** Other services can subscribe to events
- **Debugging:** Replay events to reproduce bugs

**Challenges:**
- **Event schema evolution:** Events are immutable. Need strategies (upcasting, versioning) when schema changes
- **Snapshotting:** Replaying millions of events is slow — periodically save snapshots of current state
- **Consistency:** Eventual consistency between event store and read models

**Pairing:** Often used with CQRS — event store is the write model, projections build read models.

---

### Q36: Explain Circuit Breaker pattern.

**Answer:**

Circuit Breaker prevents a network/service failure from cascading to the caller by **detecting failures and preventing calls to a failing service** until it recovers.

**Three states:**
1. **CLOSED:** Normal operation. Requests pass through. Failures are counted.
2. **OPEN:** Failure threshold exceeded. Requests fail immediately (fast-fail) without calling the service. After a timeout, moves to HALF_OPEN.
3. **HALF_OPEN:** A probe request is allowed through. If it succeeds → CLOSED. If it fails → OPEN again.

```java
enum CircuitState { CLOSED, OPEN, HALF_OPEN }

class CircuitBreaker {
    private CircuitState state = CircuitState.CLOSED;
    private int failureCount = 0;
    private final int failureThreshold = 5;
    private final long timeoutMs = 30000;
    private long lastFailureTime;

    synchronized <T> T call(Supplier<T> operation) throws Exception {
        if (state == CircuitState.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > timeoutMs) {
                state = CircuitState.HALF_OPEN;
            } else {
                throw new CircuitBreakerOpenException();
            }
        }
        try {
            T result = operation.get();
            reset();
            return result;
        } catch (Exception e) {
            recordFailure();
            throw e;
        }
    }

    private synchronized void recordFailure() {
        failureCount++;
        lastFailureTime = System.currentTimeMillis();
        if (failureCount >= failureThreshold) state = CircuitState.OPEN;
    }
    private synchronized void reset() {
        state = CircuitState.CLOSED;
        failureCount = 0;
    }
}
```

**Benefits:** Graceful degradation, faster failure detection, system stability.

**Real-world:** Netflix Hystrix, Resilience4j, Spring Cloud Circuit Breaker.

---

### Q37: Explain Saga pattern — choreography vs. orchestration.

**Answer:**

Saga manages distributed transactions across multiple microservices by breaking them into a sequence of local transactions, with compensating actions for rollback.

**Choreography-based Saga:**

Each service produces events and listens to other services' events. No central coordinator.

```
OrderService → "OrderCreated" event
InventoryService ← listens, reserves stock, emits "StockReserved"
PaymentService ← listens, charges card, emits "PaymentProcessed"
...if Payment fails → PaymentService emits "PaymentFailed"
InventoryService ← listens, compensates: releases stock
```

**Pros:** Simple, loosely coupled, no single point of failure.
**Cons:** Logic is spread across services, hard to trace and debug, cyclic dependencies possible.

**Orchestration-based Saga:**

A central orchestrator tells each service what to do and handles compensation.

```
Orchestrator → "ReserveStock" → InventoryService
Orchestrator → "ProcessPayment" → PaymentService
Orchestrator → "ShipOrder" → ShippingService
...if Payment fails → Orchestrator sends "ReleaseStock" to InventoryService
```

**Pros:** Clear flow, easy to monitor, test, and manage.
**Cons:** Central coordinator is a single point of failure and potential bottleneck.

**When to use which:**
- **Choreography:** Simple workflows, few services, high autonomy
- **Orchestration:** Complex workflows, need clear visibility, many services

---

### Q38: Explain the differences between Choreography and Orchestration Sagas in detail.

**Answer:**

| Aspect | Choreography | Orchestration |
|--------|-------------|---------------|
| **Coordination** | Decentralized — each service decides based on events | Centralized — orchestrator directs every step |
| **Communication** | Event-driven (pub-sub) | Command-driven (request-response) |
| **Coupling** | Loose — services don't know each other | Tighter — services depend on orchestrator |
| **Complexity** | Simple initially, complex to debug at scale | More upfront code, easier to manage at scale |
| **Visibility** | Hard — logic distributed across event handlers | Easy — single saga definition to trace |
| **Error handling** | Implicit via compensating events | Explicit try-catch-compensate |
| **Testing** | Hard — need to simulate entire event flow | Easier — mock orchestrator steps |
| **Performance** | No bottleneck, but event propagation latency | Orchestrator can become bottleneck |
| **Best for** | Simple sagas, high autonomy, event-native systems | Complex workflows, need tracing, compliance |

**Real-world implementations:**
- **Choreography:** Apache Kafka + event handlers
- **Orchestration:** Temporal.io, AWS Step Functions, Camunda

---

## LLD Design Problems (Q39–Q100)

### Q39: Design a Rate Limiter (Token Bucket, Sliding Window, Leaky Bucket).

**Answer:**

**Token Bucket:**
- Algorithm: A bucket holds tokens. Tokens are added at a fixed rate (e.g., 10 tokens/sec). Each request consumes one token. If bucket is empty, request is rejected.
- **Burst:** Bucket capacity allows bursts (e.g., capacity=20 allows 20 immediate requests).
- **Implementation:**

```java
class TokenBucket {
    private final long capacity;
    private final long refillRatePerSecond;
    private double tokens;
    private long lastRefillTimestamp;

    TokenBucket(long capacity, long refillRatePerSecond) {
        this.capacity = capacity;
        this.refillRatePerSecond = refillRatePerSecond;
        this.tokens = capacity;
        this.lastRefillTimestamp = System.nanoTime();
    }

    synchronized boolean allowRequest() {
        refill();
        if (tokens >= 1) {
            tokens--;
            return true;
        }
        return false;
    }

    private void refill() {
        long now = System.nanoTime();
        double elapsedSeconds = (now - lastRefillTimestamp) / 1_000_000_000.0;
        tokens = Math.min(capacity, tokens + elapsedSeconds * refillRatePerSecond);
        lastRefillTimestamp = now;
    }
}
```

**Leaky Bucket:**
- Algorithm: Requests enter a queue (bucket) of fixed size. They are processed at a fixed rate. If the queue is full, the request is discarded.
- **Key difference:** Leaky bucket **smooths** bursts (enforces a constant outflow rate). Token bucket allows bursts up to capacity.
- When to use: Need to enforce a strict processing rate (e.g., API gateway egress).

**Sliding Window Log:**
- Algorithm: Maintain a sorted list of timestamps for each request. On new request, remove timestamps older than window (e.g., 1 minute). If count less-or-equal threshold, allow; else reject.
- **Memory:** O(window * rate) — high for large windows.

**Sliding Window Counter:**
- Divides time into buckets (e.g., per second). Keeps count for current and previous bucket.
```
rate = previousCount * (windowSize - elapsedInCurrentWindow)/windowSize + currentCount
if rate < threshold → allow
```
- **Why better:** Approximates sliding window with O(1) memory per window.

**Distributed Rate Limiter:**
- Use Redis sorted sets (sliding window) or Redis counters (token bucket), with Lua scripts for atomicity.

---

### Q40: Design a URL Shortener (LLD).

**Answer:**

**Core entities:**

```java
class ShortUrl {
    String shortKey;      // 7-char base62
    String longUrl;
    LocalDateTime createdAt;
    LocalDateTime expiresAt;
    long clickCount;
}

class ClickEvent {
    String shortKey;
    String userAgent;
    String referrer;
    String ipAddress;
    LocalDateTime timestamp;
}
```

**Base62 Encoding:**

```java
class Base62Encoder {
    private static final String CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static String encode(long num) {
        StringBuilder sb = new StringBuilder();
        while (num > 0) {
            sb.append(CHARS.charAt((int)(num % 62)));
            num /= 62;
        }
        return sb.reverse().toString();
    }
    static long decode(String str) {
        long num = 0;
        for (char c : str.toCharArray()) {
            num = num * 62 + CHARS.indexOf(c);
        }
        return num;
    }
}
```

**URL Shortener Service:**

```java
class URLShortenerService {
    private final UrlRepository urlRepo;
    private final KeyGenerator keyGen;
    private final Cache<String, ShortUrl> cache;

    ShortUrl shorten(String longUrl, LocalDateTime expiresAt) {
        String key = keyGen.generateKey();
        ShortUrl shortUrl = new ShortUrl(key, longUrl, LocalDateTime.now(), expiresAt, 0);
        urlRepo.save(shortUrl);
        return shortUrl;
    }

    String resolve(String shortKey) {
        ShortUrl url = cache.get(shortKey);
        if (url == null) {
            url = urlRepo.findByKey(shortKey);
            if (url == null) throw new NotFoundException();
            cache.put(shortKey, url);
        }
        if (url.getExpiresAt() != null && url.getExpiresAt().isBefore(LocalDateTime.now())) {
            throw new ExpiredException();
        }
        return url.getLongUrl();
    }
}
```

**Key generation strategies:**
1. **Random:** 62^7 = ~3.5 trillion keys. Collision probability is low but needs checking.
2. **Distributed ID (Snowflake):** Encode unique ID to base62.
3. **Counter-based (ZooKeeper/Redis):** Centralized counter to base62 encode.

**Storage:** Relational DB (PostgreSQL) or NoSQL (DynamoDB). Index on shortKey.

**Redirection status:** HTTP 301 (permanent, cached by browser) or 302 (temporary, allows click tracking).

---

### Q41: Design a Parking Lot System (OO).

**Answer:**

```java
enum VehicleType { BIKE, CAR, TRUCK }
enum SpotType { COMPACT, LARGE, HANDICAPPED }

class Vehicle {
    String licensePlate;
    VehicleType type;
    Vehicle(String plate, VehicleType t) { this.licensePlate = plate; this.type = t; }
}

class ParkingSpot {
    String id;
    SpotType type;
    boolean isOccupied;
    Vehicle parkedVehicle;

    ParkingSpot(String id, SpotType type) { this.id = id; this.type = type; }
    boolean canPark(Vehicle v) {
        return switch (v.type) {
            case BIKE -> true;
            case CAR -> type == SpotType.COMPACT || type == SpotType.LARGE;
            case TRUCK -> type == SpotType.LARGE;
        };
    }
    void park(Vehicle v) { this.parkedVehicle = v; this.isOccupied = true; }
    void unpark() { this.parkedVehicle = null; this.isOccupied = false; }
}

class ParkingLevel {
    String name;
    List<ParkingSpot> spots;
    ParkingLevel(String name, List<ParkingSpot> spots) { this.name = name; this.spots = spots; }
    ParkingSpot findAvailableSpot(Vehicle v) {
        return spots.stream().filter(s -> !s.isOccupied && s.canPark(v)).findFirst().orElse(null);
    }
}

class ParkingLot {
    private List<ParkingLevel> levels;
    private Map<String, ParkingSpot> activeTickets = new HashMap<>();

    ParkingLot(List<ParkingLevel> levels) { this.levels = levels; }

    ParkingTicket parkVehicle(Vehicle v) {
        for (ParkingLevel level : levels) {
            ParkingSpot spot = level.findAvailableSpot(v);
            if (spot != null) {
                spot.park(v);
                ParkingTicket ticket = new ParkingTicket(UUID.randomUUID().toString(), spot.id, v);
                activeTickets.put(ticket.id, spot);
                return ticket;
            }
        }
        throw new ParkingFullException("No spot available for " + v.type);
    }

    double unparkVehicle(String ticketId) {
        ParkingSpot spot = activeTickets.get(ticketId);
        if (spot == null) throw new InvalidTicketException();
        Vehicle v = spot.parkedVehicle;
        spot.unpark();
        activeTickets.remove(ticketId);
        return calculateFee(v, spot.type);
    }
}

class ParkingTicket {
    String id;
    String spotId;
    Vehicle vehicle;
    LocalDateTime entryTime;
    ParkingTicket(String id, String spotId, Vehicle v) {
        this.id = id; this.spotId = spotId; this.vehicle = v; this.entryTime = LocalDateTime.now();
    }
}
```

**Design decisions:**
- **ParkingSpot** checks compatibility (`canPark`) — follows Tell Don't Ask
- **ParkingLevel** scans spots sequentially or via a queue per spot type
- **Pricing** is separate (`PricingStrategy` — Strategy pattern)
- **Multi-level:** Easy to add floors

---

### Q42: Design a Vending Machine (OO).

**Answer:**

```java
enum Product { COKE(1.5), PEPSI(1.5), WATER(1.0), CANDY(0.75);
    final double price;
    Product(double p) { this.price = p; }
}

class Inventory {
    private Map<Product, Integer> stock = new EnumMap<>(Product.class);
    void add(Product p, int qty) { stock.merge(p, qty, Integer::sum); }
    boolean hasProduct(Product p) { return stock.getOrDefault(p, 0) > 0; }
    void dispense(Product p) { stock.merge(p, -1, Integer::sum); }
}

class VendingMachine {
    private Inventory inventory = new Inventory();
    private double balance = 0;
    private Product selectedProduct;

    void insertCoin(double amount) { balance += amount; }
    void selectProduct(Product p) {
        if (!inventory.hasProduct(p)) throw new SoldOutException();
        if (balance < p.price) throw new InsufficientFundsException();
        this.selectedProduct = p;
    }
    Pair<Product, Double> dispense() {
        if (selectedProduct == null) throw new NoSelectionException();
        inventory.dispense(selectedProduct);
        double change = balance - selectedProduct.price;
        balance = 0;
        Product p = selectedProduct;
        selectedProduct = null;
        return new Pair<>(p, change);
    }
    double refund() {
        double amount = balance;
        balance = 0;
        selectedProduct = null;
        return amount;
    }
}
```

**Enhanced with State Pattern** (as in Q26): States = `Idle`, `HasCoin`, `ProductSelected`, `Dispensing`, `OutOfOrder`. Each state implements behavior and transitions.

---

### Q43: Design Tic-Tac-Toe (OO).

**Answer:**

```java
enum Player { X, O }
enum GameStatus { IN_PROGRESS, X_WINS, O_WINS, DRAW }

class Board {
    private Player[][] grid;
    private int size;

    Board(int n) { this.size = n; grid = new Player[n][n]; }

    boolean place(int row, int col, Player player) {
        if (row < 0 || row >= size || col < 0 || col >= size || grid[row][col] != null)
            return false;
        grid[row][col] = player;
        return true;
    }

    boolean checkWin(Player player) {
        for (int i = 0; i < size; i++) {
            boolean rowWin = true, colWin = true;
            for (int j = 0; j < size; j++) {
                if (grid[i][j] != player) rowWin = false;
                if (grid[j][i] != player) colWin = false;
            }
            if (rowWin || colWin) return true;
        }
        boolean diag1 = true, diag2 = true;
        for (int i = 0; i < size; i++) {
            if (grid[i][i] != player) diag1 = false;
            if (grid[i][size-1-i] != player) diag2 = false;
        }
        return diag1 || diag2;
    }

    boolean isFull() {
        for (Player[] row : grid)
            for (Player p : row)
                if (p == null) return false;
        return true;
    }
}

class TicTacToe {
    private Board board;
    private Player currentPlayer = Player.X;
    private GameStatus status = GameStatus.IN_PROGRESS;

    TicTacToe(int n) { board = new Board(n); }

    GameStatus play(int row, int col) {
        if (status != GameStatus.IN_PROGRESS) throw new GameOverException();
        if (!board.place(row, col, currentPlayer)) throw new InvalidMoveException();

        if (board.checkWin(currentPlayer)) {
            status = currentPlayer == Player.X ? GameStatus.X_WINS : GameStatus.O_WINS;
        } else if (board.isFull()) {
            status = GameStatus.DRAW;
        } else {
            currentPlayer = currentPlayer == Player.X ? Player.O : Player.X;
        }
        return status;
    }
}
```

**For Chess:** Same structure but with `Piece` hierarchy (King, Queen, Rook, Bishop, Knight, Pawn), each with `isValidMove(Board, Position from, Position to, Color player)`.

---

### Q44: Design a Logger Framework.

**Answer:**

```java
enum LogLevel { DEBUG, INFO, WARN, ERROR, FATAL }

class LogMessage {
    LogLevel level;
    String message;
    String timestamp;
    String threadName;
}

interface LogAppender {
    void append(LogMessage msg);
}

class ConsoleAppender implements LogAppender {
    public void append(LogMessage msg) {
        System.out.println("[" + msg.level + "] " + msg.timestamp + " " + msg.message);
    }
}
class FileAppender implements LogAppender {
    private BufferedWriter writer;
    FileAppender(String filePath) throws IOException {
        this.writer = new BufferedWriter(new FileWriter(filePath, true));
    }
    public void append(LogMessage msg) { /* write to file */ }
}

abstract class AbstractLogger {
    protected LogLevel level;
    protected AbstractLogger nextLogger;
    protected LogAppender appender;

    void setNext(AbstractLogger next) { this.nextLogger = next; }

    void log(LogLevel level, String message) {
        if (this.level.ordinal() <= level.ordinal()) {
            appender.append(new LogMessage(level, message, LocalDateTime.now().toString(), Thread.currentThread().getName()));
        }
        if (nextLogger != null) nextLogger.log(level, message);
    }
}

class DebugLogger extends AbstractLogger {
    DebugLogger(LogAppender appender) { this.level = LogLevel.DEBUG; this.appender = appender; }
}
class ErrorLogger extends AbstractLogger {
    ErrorLogger(LogAppender appender) { this.level = LogLevel.ERROR; this.appender = appender; }
}

// Logger facade (Singleton)
class Logger {
    private static Logger instance;
    private AbstractLogger chain;

    private Logger() {
        LogAppender console = new ConsoleAppender();
        DebugLogger debug = new DebugLogger(console);
        ErrorLogger error = new ErrorLogger(console);
        debug.setNext(error);
        this.chain = debug;
    }

    public static Logger getInstance() {
        if (instance == null) instance = new Logger();
        return instance;
    }

    public static void info(String msg) { getInstance().chain.log(LogLevel.INFO, msg); }
    public static void error(String msg) { getInstance().chain.log(LogLevel.ERROR, msg); }
}
```

**Key features:**
- **Flexible:** Appenders (console, file, DB, network)
- **Async:** Use `BlockingQueue` + dedicated thread for non-blocking logging
- **Configurable:** Log level per package/class
- **Pattern layout:** Customizable output format

---

### Q45: Design an LRU Cache.

**Answer:**

```java
class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> map = new HashMap<>();
    private final Node<K, V> head = new Node<>(null, null);  // dummy
    private final Node<K, V> tail = new Node<>(null, null);  // dummy

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public synchronized V get(K key) {
        Node<K, V> node = map.get(key);
        if (node == null) return null;
        moveToHead(node);
        return node.value;
    }

    public synchronized void put(K key, V value) {
        Node<K, V> node = map.get(key);
        if (node != null) {
            node.value = value;
            moveToHead(node);
            return;
        }
        if (map.size() >= capacity) {
            Node<K, V> lru = tail.prev;
            removeNode(lru);
            map.remove(lru.key);
        }
        Node<K, V> newNode = new Node<>(key, value);
        map.put(key, newNode);
        addToHead(newNode);
    }

    private void addToHead(Node<K, V> node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    private void removeNode(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    private void moveToHead(Node<K, V> node) {
        removeNode(node);
        addToHead(node);
    }

    private static class Node<K, V> {
        K key;
        V value;
        Node<K, V> prev, next;
        Node(K key, V value) { this.key = key; this.value = value; }
    }
}
```

**Time:** O(1) get and put. **Space:** O(capacity).

**For LFU (Least Frequently Used):**
- Maintain frequency buckets. Each frequency has its own linked list (LRU within same frequency).
- `get`: increment frequency, move node to next frequency's list.
- `put`: if at capacity, evict from lowest frequency bucket.
- O(1) get, O(1) put with careful data structures (HashMap<Key, Node> + HashMap<Frequency, LinkedHashSet<Key>>).

---

### Q46: Design a Pub-Sub System.

**Answer:**

```java
interface Message {
    String getKey();
    byte[] getPayload();
}

interface Subscriber {
    void onMessage(Message msg);
}

class Topic {
    private final String name;
    private final List<Subscriber> subscribers = new CopyOnWriteArrayList<>();
    private final Queue<Message> messageQueue = new LinkedBlockingQueue<>();

    Topic(String name) { this.name = name; }

    void subscribe(Subscriber s) { subscribers.add(s); }
    void unsubscribe(Subscriber s) { subscribers.remove(s); }

    void publish(Message msg) {
        messageQueue.offer(msg);
    }

    void deliverMessages() {
        while (true) {
            Message msg = messageQueue.poll(100, TimeUnit.MILLISECONDS);
            if (msg != null) {
                for (Subscriber s : subscribers) {
                    try {
                        s.onMessage(msg);
                    } catch (Exception e) { /* handle */ }
                }
            }
        }
    }
}

class Broker {
    private final Map<String, Topic> topics = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(10);

    void createTopic(String name) { topics.putIfAbsent(name, new Topic(name)); }
    void subscribe(String topicName, Subscriber s) {
        Topic topic = topics.get(topicName);
        if (topic == null) throw new IllegalArgumentException("Topic not found: " + topicName);
        topic.subscribe(s);
    }
    void publish(String topicName, Message msg) {
        Topic topic = topics.get(topicName);
        if (topic == null) throw new IllegalArgumentException("Topic not found: " + topicName);
        executor.submit(() -> topic.publish(msg));
    }
}
```

**For distributed pub-sub (Kafka-like):**
- **Partitioning:** Messages with same key go to same partition (order guarantee within partition)
- **Consumer groups:** Each partition is consumed by one consumer in a group (load balancing)
- **Offset management:** Consumer tracks its offset per partition
- **Replication:** Partitions replicated across brokers for fault tolerance

---

### Q47: Design an Elevator System.

**Answer:**

```java
enum Direction { UP, DOWN, IDLE }

class ElevatorRequest {
    int floor;
    Direction direction;
    ElevatorRequest(int floor, Direction dir) { this.floor = floor; this.direction = dir; }
}

class Elevator {
    int id;
    int currentFloor = 0;
    Direction direction = Direction.IDLE;
    TreeSet<Integer> upStops = new TreeSet<>();
    TreeSet<Integer> downStops = new TreeSet<>(Comparator.reverseOrder());

    Elevator(int id) { this.id = id; }

    void addStop(int floor) {
        if (floor >= currentFloor) upStops.add(floor);
        else downStops.add(floor);
        updateDirection();
    }

    void move() {
        if (direction == Direction.UP && !upStops.isEmpty()) {
            currentFloor = upStops.first();
            upStops.remove(currentFloor);
        } else if (direction == Direction.DOWN && !downStops.isEmpty()) {
            currentFloor = downStops.first();
            downStops.remove(currentFloor);
        }
        if (upStops.isEmpty() && downStops.isEmpty()) direction = Direction.IDLE;
    }

    void updateDirection() {
        if (direction == Direction.IDLE) {
            if (!upStops.isEmpty()) direction = Direction.UP;
            else if (!downStops.isEmpty()) direction = Direction.DOWN;
        }
    }
}

class ElevatorController {
    List<Elevator> elevators;

    void requestElevator(int floor, Direction direction) {
        Elevator best = findBestElevator(floor, direction);
        best.addStop(floor);
    }

    void requestFloor(int elevatorId, int floor) {
        Elevator e = elevators.stream().filter(el -> el.id == elevatorId).findFirst().orElseThrow();
        e.addStop(floor);
    }

    private Elevator findBestElevator(int floor, Direction dir) {
        return elevators.stream()
            .min(Comparator.comparingInt(e -> Math.abs(e.currentFloor - floor)))
            .orElse(elevators.get(0));
    }
}
```

**Algorithms:**
- **FCFS (First Come First Serve):** Simple but inefficient.
- **SCAN (Elevator Algorithm):** Move in one direction, service all requests, then reverse.
- **LOOK:** Like SCAN but goes only to the highest/lowest pending request.
- **SSTF (Shortest Seek Time First):** Service nearest request first (can starve far requests).

---

### Q48: Design an ATM System.

**Answer:**

```java
class Card {
    String cardNumber;
    String pin;
    LocalDate expiryDate;
}

class Account {
    String accountNumber;
    double balance;
    void debit(double amount) { if (balance < amount) throw new InsufficientFundsException(); balance -= amount; }
    void credit(double amount) { balance += amount; }
}

class Transaction {
    String transactionId;
    double amount;
    LocalDateTime timestamp;
    TransactionStatus status;
}

class Withdrawal extends Transaction { /* ... */ }
class Deposit extends Transaction { /* ... */ }
class Transfer extends Transaction {
    String toAccount;
}

class ATM {
    private CashDispenser dispenser;
    private Screen screen;
    private CardReader cardReader;
    private Keypad keypad;

    void insertCard(Card card) {
        if (cardReader.readCard(card)) {
            screen.display("Enter PIN");
        }
    }
    void enterPin(String pin) { /* authenticate */ }
    void withdraw(double amount) {
        if (dispenser.hasCash(amount) && account.balance >= amount) {
            account.debit(amount);
            dispenser.dispense(amount);
            printReceipt(new Withdrawal(...));
        }
    }
    void deposit(double amount) {
        account.credit(amount);
        printReceipt(new Deposit(...));
    }
    void transfer(String toAccount, double amount) {
        account.debit(amount);
        printReceipt(new Transfer(...));
    }
}

class CashDispenser {
    Map<Denomination, Integer> cashAvailable;
    boolean hasCash(double amount) { /* can dispense in available denominations */ }
    void dispense(double amount) { /* reduce cash, dispense */ }
}

class BankService {
    Account getAccount(String cardNumber) { /* fetch from DB */ }
    void processTransaction(Transaction t) { /* persist */ }
}
```

**Design decisions:**
- **State pattern:** ATM states = Idle, CardInserted, PinEntered, TransactionSelected, DispensingCash, EjectingCard
- Security: PIN encryption, session timeout, card trapping on failed attempts

---

### Q49: Design a Chess Game (OO).

**Answer:**

```java
enum Color { WHITE, BLACK }
enum PieceType { KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN }

class Position {
    int row, col;
    boolean isValid() { return row >= 0 && row < 8 && col >= 0 && col < 8; }
}

abstract class Piece {
    Color color;
    Position position;
    Piece(Color c, Position p) { this.color = c; this.position = p; }
    abstract boolean isValidMove(Position to, Board board);
}

class Rook extends Piece {
    Rook(Color c, Position p) { super(c, p); }
    boolean isValidMove(Position to, Board board) {
        if (position.row != to.row && position.col != to.col) return false;
        int rowStep = to.row == position.row ? 0 : (to.row - position.row) / Math.abs(to.row - position.row);
        int colStep = to.col == position.col ? 0 : (to.col - position.col) / Math.abs(to.col - position.col);
        int r = position.row + rowStep, c = position.col + colStep;
        while (r != to.row || c != to.col) {
            if (board.getPiece(r, c) != null) return false;
            r += rowStep; c += colStep;
        }
        Piece dest = board.getPiece(to);
        return dest == null || dest.color != this.color;
    }
}

class Board {
    Piece[][] grid = new Piece[8][8];

    Board() { /* initialize starting positions */ }
    Piece getPiece(Position p) { return grid[p.row][p.col]; }
    Piece getPiece(int row, int col) { return grid[row][col]; }
    void movePiece(Position from, Position to) {
        Piece p = getPiece(from);
        grid[to.row][to.col] = p;
        grid[from.row][from.col] = null;
        p.position = to;
    }
    boolean isInCheck(Color color) { /* check if any opponent piece can capture king */ }
}

class Game {
    Board board = new Board();
    Color currentTurn = Color.WHITE;
    GameStatus status = GameStatus.ACTIVE;

    boolean makeMove(Position from, Position to) {
        Piece piece = board.getPiece(from);
        if (piece == null || piece.color != currentTurn) return false;
        if (!piece.isValidMove(to, board)) return false;
        board.movePiece(from, to);
        if (board.isInCheck(currentTurn)) { /* revert */ return false; }
        if (board.isCheckmate(currentTurn.opponent())) { status = GameStatus.CHECKMATE; }
        else if (board.isStalemate(currentTurn.opponent())) { status = GameStatus.STALEMATE; }
        currentTurn = currentTurn.opponent();
        return true;
    }
}
```

**Key considerations:**
- Each piece subclass implements `isValidMove` with its movement rules
- Board validates moves (no moving through pieces for Rook/Bishop/Queen)
- Check detection: does any opponent piece attack the king's position?
- Promotion, en passant, castling handled in `makeMove`

---

### Q50: Design a Restaurant Table Reservation System (LLD).

**Answer:**

```java
class TimeSlot {
    LocalDateTime start;
    LocalDateTime end;
}

enum TableStatus { AVAILABLE, RESERVED, OCCUPIED }
class Table {
    int id;
    int capacity;
    TableStatus status;
    List<TimeSlot> reservations;
}

class Customer {
    String name;
    String phone;
}

class Reservation {
    String id;
    Customer customer;
    Table table;
    TimeSlot timeSlot;
    ReservationStatus status; // CONFIRMED, CANCELLED, COMPLETED
}

class ReservationService {
    private List<Table> tables;
    private Map<String, Reservation> reservations = new HashMap<>();

    List<Table> findAvailableTables(int partySize, TimeSlot slot) {
        return tables.stream()
            .filter(t -> t.capacity >= partySize)
            .filter(t -> isAvailable(t, slot))
            .collect(Collectors.toList());
    }

    Reservation reserve(Customer customer, Table table, TimeSlot slot) {
        if (!isAvailable(table, slot)) throw new TableNotAvailableException();
        Reservation r = new Reservation(UUID.randomUUID().toString(), customer, table, slot, CONFIRMED);
        reservations.put(r.id, r);
        return r;
    }

    void cancelReservation(String id) {
        Reservation r = reservations.get(id);
        if (r == null) throw new NotFoundException();
        r.status = ReservationStatus.CANCELLED;
    }

    private boolean isAvailable(Table table, TimeSlot slot) {
        return table.reservations.stream().noneMatch(r ->
            r.status == CONFIRMED &&
            slot.start.isBefore(r.end) && slot.end.isAfter(r.start));
    }
}
```

---

## More LLD Patterns (Q51–Q100)

### Q51: Explain the Proxy pattern — Virtual, Protection, Remote, Logging proxies.

**Answer:**

| Proxy Type | Purpose | Example |
|-----------|---------|---------|
| **Virtual** | Lazy initialization of expensive objects | Image placeholder (Q18) |
| **Protection** | Access control based on permissions | `BankAccountProxy` checks role |
| **Remote** | Local representative for remote object | RPC/Java RMI stub |
| **Logging** | Log requests before delegating | `LoggingProxy` logs method calls |

**Example — Logging Proxy:**
```java
class UserServiceLoggingProxy implements UserService {
    private final UserService target;
    UserServiceLoggingProxy(UserService t) { this.target = t; }
    public User findById(String id) {
        System.out.println("[LOG] findById: " + id);
        long start = System.nanoTime();
        User result = target.findById(id);
        System.out.println("[LOG] findById completed in " + (System.nanoTime() - start) / 1e6 + "ms");
        return result;
    }
}
```

### Q52: What is the difference between State and Strategy patterns?

**Answer:**

| Aspect | State | Strategy |
|--------|-------|----------|
| **Intent** | Change behavior when internal state changes | Select an algorithm from a family |
| **Who controls** | State object decides transitions | Client sets the strategy |
| **State awareness** | States know about each other (often) | Strategies are independent |
| **Number of objects** | One active state at a time | One active strategy at a time |
| **Analogy** | A person's mood (happy → friendly, angry → hostile) | A sorting algorithm (quicksort vs. mergesort) |

### Q53: Explain the difference between Factory Method and Abstract Factory.

**Answer:**

| Aspect | Factory Method | Abstract Factory |
|--------|---------------|-----------------|
| **Scope** | Single product | Family of products |
| **How** | Subclass overrides creation method | Object with multiple factory methods |
| **Product variety** | One type (varied by subclass) | Multiple related types |
| **Implementation** | Inheritance (class-level) | Composition (object-level) |
| **Example** | `Logistics.createTransport()` returns a `Transport` | `GUIFactory.createButton()` + `createCheckbox()` |

### Q54: Explain the difference between Adapter and Facade.

**Answer:**

| Aspect | Adapter | Facade |
|--------|---------|--------|
| **Purpose** | Make an interface compatible with what client expects | Provide a simpler interface to a complex subsystem |
| **Interface** | Converts one interface to another | Provides a unified, higher-level interface |
| **Subsystem exposure** | Subsystem is still accessible | Subsystem is hidden by facade (but accessible if needed) |
| **Analogy** | Power plug adapter (US to EU) | Hotel concierge (one call handles multiple steps) |

### Q55: Explain the difference between Composite and Decorator.

**Answer:**

| Aspect | Composite | Decorator |
|--------|-----------|-----------|
| **Intent** | Part-whole hierarchy, treat leaves and composites uniformly | Add responsibilities dynamically |
| **Structure** | Tree of components | Chain of wrappers |
| **Focus** | Composition (has children) | Extension (adds behavior) |
| **Children** | Composite has children, leaf doesn't | Decorator wraps a single component |
| **Identity** | Both component and composite are same type | Decorator is same type as wrapped object |

### Q56: Explain the difference between Proxy and Decorator.

**Answer:**

| Aspect | Proxy | Decorator |
|--------|-------|-----------|
| **Intent** | Control access to an object | Add behavior to an object |
| **Object creation** | Proxy often creates the real object (lazy) | Decorator receives the object to wrap |
| **Ownership** | Proxy controls the real object's lifecycle | Decorator extends but doesn't control lifecycle |
| **Interface** | Proxy provides the same interface (strict) | Decorator provides the same interface (may add methods) |
| **Analogy** | Lawyer (proxy for client) | Wrapping paper (decorator for gift) |

### Q57: Explain Template Method vs. Strategy.

**Answer:**

| Aspect | Template Method | Strategy |
|--------|-----------------|----------|
| **Mechanism** | Inheritance (subclass overrides steps) | Composition (context holds strategy reference) |
| **Control** | Parent controls algorithm skeleton | Context delegates entire algorithm |
| **Granularity** | Varies parts of an algorithm | Varies the whole algorithm |
| **Coupling** | Tighter (subclass depends on parent) | Loose (strategy is pluggable) |
| **When to use** | Algorithm structure is fixed, steps vary | Entire algorithm varies |

**Rule of thumb:** If you want to vary only some steps, use Template Method. If you want to swap the whole algorithm, use Strategy.

### Q58: What is the Null Object pattern?

**Answer:**

Null Object provides a **default, do-nothing implementation** of an interface to avoid null checks.

```java
interface Logger { void log(String msg); }
class ConsoleLogger implements Logger { public void log(String msg) { System.out.println(msg); } }
class NullLogger implements Logger { public void log(String msg) { /* do nothing */ } }

class Service {
    private Logger logger;
    Service(Logger logger) { this.logger = logger != null ? logger : new NullLogger(); }
    void doSomething() {
        logger.log("Doing something");  // No null check needed
    }
}
```

**Benefits:** Eliminates null checks, follows Null Object is a no-op, improves code readability.

### Q59: Explain the DAO (Data Access Object) pattern.

**Answer:**

DAO abstracts and encapsulates all access to a data source. It manages the connection, CRUD operations, and mapping between data source and application objects.

```java
interface UserDao {
    User get(int id);
    List<User> getAll();
    void save(User user);
    void update(User user);
    void delete(int id);
}

class UserDaoImpl implements UserDao {
    private DataSource dataSource;
    public User get(int id) {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id=?")) {
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return mapUser(rs);
        } catch (SQLException e) { /* handle */ }
        return null;
    }
}
```

**vs. Repository:** DAO is lower-level, often maps to a single table. Repository is higher-level, works with domain objects, may use multiple DAOs.

### Q60: Explain the DTO (Data Transfer Object) pattern.

**Answer:**

DTO is a simple object that carries data between processes (e.g., between layers or over the network) without any business logic.

```java
class UserDTO {
    private String id;
    private String name;
    private String email;
    // getters/setters only — no business logic
}

// Assembler converts domain to DTO
class UserAssembler {
    UserDTO toDTO(User user) {
        UserDTO dto = new UserDTO();
        dto.setId(user.getId());
        dto.setName(user.getName());
        dto.setEmail(user.getEmail());
        return dto;
    }
    User toDomain(UserDTO dto) { /* reverse mapping */ }
}
```

**When to use:** Network serialization (REST APIs), decoupling internal models from external interfaces.

### Q61: Design a simple Dependency Injection Container.

**Answer:**

```java
class DIContainer {
    private Map<Class<?>, Class<?>> bindings = new ConcurrentHashMap<>();
    private Map<Class<?>, Object> singletons = new ConcurrentHashMap<>();

    <T> void register(Class<T> iface, Class<? extends T> impl) {
        bindings.put(iface, impl);
    }
    <T> void registerSingleton(Class<T> iface, Class<? extends T> impl) {
        bindings.put(iface, impl);
        singletons.put(iface, createInstance(impl));
    }

    <T> T resolve(Class<T> iface) {
        if (singletons.containsKey(iface)) return (T) singletons.get(iface);
        Class<?> impl = bindings.get(iface);
        if (impl == null) throw new RuntimeException("No binding for " + iface);
        return (T) createInstance(impl);
    }

    private Object createInstance(Class<?> impl) {
        Constructor<?>[] constructors = impl.getConstructors();
        Constructor<?> constructor = constructors[0];
        Class<?>[] paramTypes = constructor.getParameterTypes();
        Object[] params = Arrays.stream(paramTypes).map(this::resolve).toArray();
        try { return constructor.newInstance(params); }
        catch (Exception e) { throw new RuntimeException(e); }
    }
}
```

### Q62: Design an Object Pool pattern.

**Answer:**

Object Pool reuses objects that are expensive to create (e.g., database connections, threads).

```java
class ConnectionPool {
    private final BlockingQueue<Connection> pool;
    private final AtomicInteger activeCount = new AtomicInteger(0);
    private final int maxSize;

    ConnectionPool(String url, int maxSize) {
        this.maxSize = maxSize;
        this.pool = new LinkedBlockingQueue<>(maxSize);
        for (int i = 0; i < maxSize; i++) {
            pool.offer(createConnection(url));
        }
    }

    Connection borrowConnection() throws InterruptedException {
        Connection conn = pool.poll(5, TimeUnit.SECONDS);
        if (conn == null) throw new TimeoutException("No connection available");
        activeCount.incrementAndGet();
        return conn;
    }

    void returnConnection(Connection conn) {
        activeCount.decrementAndGet();
        pool.offer(conn);
    }

    private Connection createConnection(String url) { /* ... */ }
}
```

### Q63: Design an E-Commerce Shopping Cart (LLD).

**Answer:**

```java
class Product {
    String id;
    String name;
    Money price;
}

class CartItem {
    Product product;
    int quantity;
    Money getSubtotal() { return product.price.multiply(quantity); }
}

class ShoppingCart {
    private String cartId;
    private List<CartItem> items = new ArrayList<>();

    void addItem(Product product, int quantity) {
        items.stream()
            .filter(i -> i.product.id.equals(product.id))
            .findFirst()
            .ifPresentOrElse(
                i -> i.quantity += quantity,
                () -> items.add(new CartItem(product, quantity))
            );
    }
    void removeItem(String productId) { items.removeIf(i -> i.product.id.equals(productId)); }

    Money calculateTotal(PricingStrategy strategy) {
        Money subtotal = items.stream().map(CartItem::getSubtotal).reduce(Money.ZERO, Money::add);
        return strategy.applyDiscounts(subtotal, items);
    }
}

interface PricingStrategy {
    Money applyDiscounts(Money subtotal, List<CartItem> items);
}
class DefaultPricing implements PricingStrategy { /* ... */ }
class BlackFridayPricing implements PricingStrategy { /* ... */ }
```

### Q64: Design a Library Management System (LLD).

**Answer:**

```java
enum BookStatus { AVAILABLE, BORROWED, RESERVED, LOST }
enum MembershipLevel { BASIC, PREMIUM }

class BookItem {
    String barcode;
    Book bookInfo;
    BookStatus status;
    LocalDate dueDate;
}

class Member {
    String memberId;
    MembershipLevel level;
    List<Loan> activeLoans;
    int maxBooks() { return level == PREMIUM ? 10 : 5; }
    boolean canBorrow() { return activeLoans.size() < maxBooks(); }
}

class Loan {
    BookItem book;
    Member member;
    LocalDate borrowedDate;
    LocalDate dueDate;
    boolean isOverdue() { return LocalDate.now().isAfter(dueDate); }
}

class Library {
    private Map<String, BookItem> booksByBarcode;
    private Map<String, Member> members;
    private FineCalculator fineCalculator;

    Loan borrowBook(String barcode, String memberId) {
        BookItem book = booksByBarcode.get(barcode);
        Member member = members.get(memberId);
        if (book.status != AVAILABLE) throw new BookNotAvailableException();
        if (!member.canBorrow()) throw new MaxBooksReachedException();
        book.status = BORROWED;
        Loan loan = new Loan(book, member, LocalDate.now(), LocalDate.now().plusDays(14));
        member.activeLoans.add(loan);
        return loan;
    }

    double returnBook(String barcode) {
        BookItem book = booksByBarcode.get(barcode);
        Loan loan = findActiveLoan(book);
        book.status = AVAILABLE;
        member.activeLoans.remove(loan);
        if (loan.isOverdue()) {
            return fineCalculator.calculate(loan);
        }
        return 0;
    }
}
```

### Q65: Design a Payment Gateway (LLD).

**Answer:**

```java
enum PaymentStatus { PENDING, SUCCESS, FAILED, REFUNDED }

class PaymentRequest {
    String orderId;
    Money amount;
    PaymentMethod method;
}

class PaymentResponse {
    String transactionId;
    PaymentStatus status;
    String gatewayRefId;
}

interface PaymentGateway {
    PaymentResponse charge(PaymentRequest request);
    PaymentResponse refund(String transactionId, Money amount);
}

class StripeGateway implements PaymentGateway {
    public PaymentResponse charge(PaymentRequest req) {
        return new PaymentResponse(UUID.randomUUID().toString(), SUCCESS, "stripe_txn_123");
    }
    public PaymentResponse refund(String txnId, Money amount) { /* ... */ }
}

class PaymentProcessor {
    private PaymentGateway gateway;
    private FraudCheckService fraudCheck;
    private PaymentRepository repository;

    PaymentResponse processPayment(PaymentRequest request) {
        PaymentResponse cached = repository.findByOrderId(request.orderId);
        if (cached != null) return cached;

        if (fraudCheck.isFraudulent(request)) {
            return new PaymentResponse(null, FAILED, null);
        }
        PaymentResponse response = gateway.charge(request);
        repository.save(request.orderId, response);
        return response;
    }
}
```

### Q66: Design a Hotel Booking System (LLD).

**Answer:**

```java
class Room {
    String roomNumber;
    RoomType type;
    Money pricePerNight;
    List<Booking> bookings;
    boolean isAvailable(DateRange range) {
        return bookings.stream().noneMatch(b -> b.overlaps(range));
    }
}

class Booking {
    String bookingId;
    Room room;
    Customer customer;
    DateRange dateRange;
    BookingStatus status;
    Money totalAmount;
}

class HotelBookingService {
    private List<Room> rooms;

    List<Room> searchRooms(RoomType type, DateRange range) {
        return rooms.stream()
            .filter(r -> r.type == type && r.isAvailable(range))
            .collect(Collectors.toList());
    }

    Booking createBooking(Customer customer, Room room, DateRange range) {
        if (!room.isAvailable(range)) throw new RoomNotAvailableException();
        Money total = room.pricePerNight.multiply(range.nights());
        Booking booking = new Booking(UUID.randomUUID().toString(), room, customer, range, PENDING, total);
        room.bookings.add(booking);
        return booking;
    }

    void confirmBooking(String bookingId) {
        Booking b = bookings.get(bookingId);
        b.status = CONFIRMED;
    }
    void cancelBooking(String bookingId) {
        Booking b = bookings.get(bookingId);
        if (b.dateRange.start.isBefore(LocalDate.now().plusDays(1)))
            throw new LateCancellationException();
        b.status = CANCELLED;
    }
}
```

### Q67: Design a Task Scheduler (LLD).

**Answer:**

```java
class Task implements Comparable<Task> {
    String id;
    Runnable action;
    LocalDateTime scheduledTime;
    Priority priority;
    int retryCount;
    int maxRetries;

    public int compareTo(Task other) {
        int p = other.priority.compareTo(this.priority);
        if (p != 0) return p;
        return scheduledTime.compareTo(other.scheduledTime);
    }
}

class TaskScheduler {
    private PriorityQueue<Task> taskQueue = new PriorityQueue<>();
    private final Object lock = new Object();
    private volatile boolean running;

    void start() {
        running = true;
        new Thread(() -> {
            while (running) {
                synchronized (lock) {
                    Task next = taskQueue.peek();
                    if (next != null && LocalDateTime.now().isAfter(next.scheduledTime)) {
                        taskQueue.poll();
                        executeTask(next);
                    }
                }
                try { Thread.sleep(100); } catch (InterruptedException e) { break; }
            }
        }).start();
    }

    void schedule(Task task) {
        synchronized (lock) {
            taskQueue.offer(task);
            lock.notify();
        }
    }

    private void executeTask(Task task) {
        try {
            task.action.run();
        } catch (Exception e) {
            if (task.retryCount < task.maxRetries) {
                task.retryCount++;
                task.scheduledTime = LocalDateTime.now().plusSeconds(5 * task.retryCount);
                schedule(task);
            }
        }
    }
}
```

### Q68: Design a File System (LLD — Composite pattern).

**Answer:**

```java
interface FileSystemNode {
    String getName();
    int getSize();
    boolean isDirectory();
}

class FileNode implements FileSystemNode {
    private String name;
    private int size;
    public int getSize() { return size; }
    public boolean isDirectory() { return false; }
    public String getName() { return name; }
}

class DirectoryNode implements FileSystemNode {
    private String name;
    private List<FileSystemNode> children = new ArrayList<>();

    void addChild(FileSystemNode node) { children.add(node); }
    void removeChild(FileSystemNode node) { children.remove(node); }
    FileSystemNode getChild(String name) {
        return children.stream().filter(c -> c.getName().equals(name)).findFirst().orElse(null);
    }

    public int getSize() { return children.stream().mapToInt(FileSystemNode::getSize).sum(); }
    public boolean isDirectory() { return true; }
    public String getName() { return name; }
}

class FileSystem {
    DirectoryNode root = new DirectoryNode("/");

    void createFile(String path, int size) {
        DirectoryNode parent = navigateToParent(path);
        String name = extractName(path);
        parent.addChild(new FileNode(name, size));
    }

    private DirectoryNode navigateToParent(String path) {
        String[] parts = path.split("/");
        DirectoryNode current = root;
        for (int i = 1; i < parts.length - 1; i++) {
            FileSystemNode child = current.getChild(parts[i]);
            if (child == null || !child.isDirectory()) throw new PathNotFoundException();
            current = (DirectoryNode) child;
        }
        return current;
    }
}
```

### Q69: Design a Call Center System (LLD).

**Answer:**

```java
enum Rank { RESPONDENT, MANAGER, DIRECTOR }
enum CallStatus { QUEUED, IN_PROGRESS, COMPLETED }

class Call {
    String id;
    Rank minimumRank;
    CallStatus status;
    Employee assignedTo;
}

abstract class Employee {
    String id;
    String name;
    Rank rank;
    boolean free = true;

    void receiveCall(Call call) {
        free = false;
        call.status = IN_PROGRESS;
        call.assignedTo = this;
    }
    void completeCall(Call call) {
        free = true;
        call.status = COMPLETED;
    }
    boolean canHandle(Call call) { return rank.ordinal() >= call.minimumRank.ordinal(); }
}

class Respondent extends Employee { Respondent() { rank = Rank.RESPONDENT; } }
class Manager extends Employee { Manager() { rank = Rank.MANAGER; } }
class Director extends Employee { Director() { rank = Rank.DIRECTOR; } }

class CallCenter {
    List<List<Employee>> employeesByRank;
    Queue<Call> callQueue = new LinkedList<>();

    void dispatchCall(Call call) {
        Employee emp = findAvailableEmployee(call.minimumRank);
        if (emp != null) {
            emp.receiveCall(call);
        } else {
            callQueue.offer(call);
        }
    }

    private Employee findAvailableEmployee(Rank minRank) {
        for (int r = minRank.ordinal(); r <= Rank.DIRECTOR.ordinal(); r++) {
            for (Employee e : employeesByRank.get(r)) {
                if (e.free) return e;
            }
        }
        return null;
    }
}
```

### Q70: Design a Snake and Ladder Game.

**Answer:**

```java
class Board {
    int size;
    Map<Integer, Integer> snakes;  // head to tail
    Map<Integer, Integer> ladders; // bottom to top

    int move(int position, int diceRoll) {
        int newPos = position + diceRoll;
        if (newPos > size) return position;
        if (snakes.containsKey(newPos)) return snakes.get(newPos);
        if (ladders.containsKey(newPos)) return ladders.get(newPos);
        return newPos;
    }
}

class Player {
    String name;
    int position = 0;
}

class Game {
    Board board;
    List<Player> players;
    int currentPlayer = 0;
    Dice dice = new Dice(6);
    boolean finished = false;

    void playTurn() {
        Player p = players.get(currentPlayer);
        int roll = dice.roll();
        p.position = board.move(p.position, roll);
        if (p.position == board.size) {
            finished = true;
            return;
        }
        currentPlayer = (currentPlayer + 1) % players.size();
    }
}
```

### Q71: Design a Movie Ticket Booking System (LLD).

**Answer:**

```java
class Movie {
    String id;
    String title;
    Duration duration;
}

class Show {
    String id;
    Movie movie;
    Screen screen;
    LocalDateTime startTime;
    Map<String, Seat> seats;
}

enum SeatType { STANDARD, PREMIUM, VIP }
class Seat {
    String number;
    SeatType type;
    Money price;
    boolean isBooked;
}

class Booking {
    String id;
    Show show;
    List<Seat> seats;
    Customer customer;
    BookingStatus status;
    Money totalPrice;
}

class MovieBookingService {
    List<Seat> getAvailableSeats(Show show) { /* ... */ }

    Booking bookTickets(Show show, List<String> seatNumbers, Customer customer) {
        synchronized (show) {
            List<Seat> seats = seatNumbers.stream()
                .map(sn -> show.seats.get(sn))
                .filter(s -> !s.isBooked)
                .collect(toList());
            if (seats.size() != seatNumbers.size())
                throw new SeatNotAvailableException();
            for (Seat s : seats) s.isBooked = true;
            Booking booking = new Booking(UUID.randomUUID().toString(), show, seats, customer, CONFIRMED, calculatePrice(seats));
            return booking;
        }
    }
}
```

### Q72: Design a Chat Room / Messaging System (LLD).

**Answer:**

```java
enum MessageType { TEXT, IMAGE, FILE, SYSTEM }

class Message {
    String id;
    User sender;
    String content;
    MessageType type;
    LocalDateTime timestamp;
}

class Conversation {
    String id;
    List<User> participants;
    List<Message> messages;
    boolean isGroup;
}

class ChatService {
    private Map<String, Conversation> conversations;

    Message sendMessage(String conversationId, Message message) {
        Conversation conv = conversations.get(conversationId);
        conv.messages.add(message);
        notifyParticipants(conv, message);
        return message;
    }

    private void notifyParticipants(Conversation conv, Message msg) {
        for (User participant : conv.participants) {
            if (!participant.id.equals(msg.sender.id)) {
                deliveryService.deliver(participant.id, msg);
            }
        }
    }
}
```

### Q73: Design a Traffic Light System (LLD — State pattern).

**Answer:**

```java
enum LightColor { RED, YELLOW, GREEN }

class TrafficLight {
    private LightColor color;

    TrafficLight() { this.color = LightColor.RED; }

    synchronized void changeColor() {
        switch (color) {
            case GREEN -> { color = YELLOW; scheduleChange(3000); }
            case YELLOW -> { color = RED; scheduleChange(30000); }
            case RED -> { color = GREEN; scheduleChange(30000); }
        }
    }
    private void scheduleChange(long ms) {
        new Timer().schedule(new TimerTask() { public void run() { changeColor(); } }, ms);
    }
}
```

### Q74: Design a Deck of Cards / Card Game (LLD).

**Answer:**

```java
enum Suit { HEARTS, DIAMONDS, CLUBS, SPADES }
enum Rank { TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE }

class Card {
    Suit suit;
    Rank rank;
    int value() { return rank.ordinal() + 2; }
}

class Deck {
    private List<Card> cards;

    Deck() {
        cards = new ArrayList<>(52);
        for (Suit s : Suit.values())
            for (Rank r : Rank.values())
                cards.add(new Card(s, r));
    }

    void shuffle() { Collections.shuffle(cards); }
    Card draw() { return cards.isEmpty() ? null : cards.remove(cards.size() - 1); }
    void addCard(Card c) { cards.add(c); }
    int remainingCards() { return cards.size(); }
}
```

### Q75: Design a Stack Overflow (LLD).

**Answer:**

```java
class User {
    String id;
    String displayName;
    int reputation;
    List<Badge> badges;
}

class Question {
    String id;
    User author;
    String title;
    String body;
    List<Tag> tags;
    List<Answer> answers;
    List<Vote> votes;
    int viewCount;
    QuestionStatus status;
}

class Answer {
    String id;
    User author;
    String body;
    List<Vote> votes;
    boolean isAccepted;
}

class StackOverflowService {
    Question postQuestion(User user, String title, String body, List<Tag> tags) {
        Question q = new Question(UUID.randomUUID().toString(), user, title, body, tags);
        return q;
    }

    Answer postAnswer(User user, Question question, String body) {
        Answer a = new Answer(/* ... */);
        question.answers.add(a);
        return a;
    }

    void voteUp(User user, Votable votable) {
        if (!user.canVote()) throw new InsufficientReputationException();
        votable.addVote(new Vote(user, UPVOTE));
    }

    List<Question> search(String query) { /* Full-text search */ }
}
```

### Q76: Design a Bowling Alley Scoring System.

**Answer:**

```java
class Frame {
    List<Integer> rolls = new ArrayList<>(3);
    boolean isStrike() { return rolls.size() == 1 && rolls.get(0) == 10; }
    boolean isSpare() { return !isStrike() && rolls.size() == 2 && rolls.get(0) + rolls.get(1) == 10; }

    int score(List<Integer> nextRolls) {
        if (isStrike()) return 10 + nextRolls.get(0) + nextRolls.get(1);
        else if (isSpare()) return 10 + nextRolls.get(0);
        else return rolls.get(0) + rolls.get(1);
    }
}

class PlayerGame {
    List<Integer> allRolls = new ArrayList<>();

    void addRoll(int pins) { allRolls.add(pins); }

    int calculateScore() {
        int total = 0;
        int rollIndex = 0;
        for (int f = 0; f < 10; f++) {
            if (allRolls.get(rollIndex) == 10) {
                total += 10 + allRolls.get(rollIndex + 1) + allRolls.get(rollIndex + 2);
                rollIndex++;
            } else if (allRolls.get(rollIndex) + allRolls.get(rollIndex + 1) == 10) {
                total += 10 + allRolls.get(rollIndex + 2);
                rollIndex += 2;
            } else {
                total += allRolls.get(rollIndex) + allRolls.get(rollIndex + 1);
                rollIndex += 2;
            }
        }
        return total;
    }
}
```

### Q77: Design a Social Media Post Feed (LLD).

**Answer:**

```java
class Post {
    String id;
    User author;
    String content;
    LocalDateTime timestamp;
    int likeCount;
    List<Comment> comments;
}

interface FeedStrategy {
    List<Post> getFeed(User user, int page, int pageSize);
}

class ChronologicalFeed implements FeedStrategy {
    public List<Post> getFeed(User user, int page, int pageSize) {
        // Get posts from followed users, ordered by timestamp desc
    }
}

class RankedFeed implements FeedStrategy {
    public List<Post> getFeed(User user, int page, int pageSize) {
        // ML-based ranking (engagement, relevance, recency)
    }
}

class FeedService {
    Map<User, FeedStrategy> strategies;

    List<Post> getFeed(User user, int page) {
        return strategies.get(user).getFeed(user, page, 20);
    }
}
```

### Q78: Design a Coffee Machine (LLD — Decorator + State).

**Answer:**

```java
enum CoffeeType { ESPRESSO, LATTE, CAPPUCCINO, AMERICANO }

class Coffee {
    String description;
    double cost;
}

// Decorator pattern (as in Q15) for add-ons (milk, sugar, caramel, etc.)
// State pattern for machine states: READY, BREWING, MAINTENANCE

class CoffeeMachine {
    private Map<Ingredient, Integer> inventory;

    Coffee brew(CoffeeType type, List<AddOn> addOns) {
        if (!hasIngredients(type)) throw new InsufficientIngredientsException();
        deductIngredients(type);
        Coffee coffee = createBase(type);
        for (AddOn addOn : addOns) coffee = addOn.decorate(coffee);
        return coffee;
    }
}
```

### Q79: Design a Document Editor (LLD — Memento + Command).

**Answer:**

```java
class Document {
    private StringBuilder content = new StringBuilder();

    void insert(int position, String text) { content.insert(position, text); }
    void delete(int start, int end) { content.delete(start, end); }
    String getContent() { return content.toString(); }

    DocumentMemento save() { return new DocumentMemento(content.toString()); }
    void restore(DocumentMemento memento) { content = new StringBuilder(memento.getContent()); }
}

class Editor {
    Document document;
    Stack<Command> undoStack = new Stack<>();
    Stack<Command> redoStack = new Stack<>();

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

    void redo() {
        if (!redoStack.isEmpty()) {
            Command cmd = redoStack.pop();
            cmd.execute();
            undoStack.push(cmd);
        }
    }
}
```

### Q80: Design a Music Player (LLD — State + Strategy).

**Answer:**

```java
enum PlaybackState { PLAYING, PAUSED, STOPPED }

class Playlist {
    String name;
    List<Song> songs;
    int currentIndex;
    Song getCurrent() { return songs.get(currentIndex); }
    Song next() { currentIndex = (currentIndex + 1) % songs.size(); return getCurrent(); }
    Song previous() { currentIndex = (currentIndex - 1 + songs.size()) % songs.size(); return getCurrent(); }
}

interface PlaybackStrategy {
    Song getNextSong(Playlist playlist);
}
class SequentialPlayback implements PlaybackStrategy { /* ... */ }
class ShufflePlayback implements PlaybackStrategy { /* ... */ }

class MusicPlayer {
    PlaybackState state = STOPPED;
    Playlist playlist;
    PlaybackStrategy strategy;

    void play() { state = PLAYING; }
    void pause() { state = PAUSED; }
    void stop() { state = STOPPED; }
}
```

### Q81: Design a Garbage Collector (Concept).

**Answer:**

**Reference Counting:** Each object has a count of references pointing to it. When count reaches 0, it's reclaimed. Problem: Circular references never collected.

**Mark-and-Sweep:**
1. **Mark:** Starting from root set (stack, registers, globals), traverse all reachable objects and mark them.
2. **Sweep:** Scan all memory, reclaim unmarked objects.

**Copy Collection (Cheney's algorithm):** Divide heap into from-space and to-space. Copy live objects from from-space to to-space (compacting). Swap spaces.

**Generational GC:** Objects are young (newly allocated) or old (survived multiple GCs). Young generation collected frequently (minor GC). Old generation collected rarely (major GC). Premise: Most objects die young.

### Q82: Design a Bidding System / Auction (LLD).

**Answer:**

```java
enum AuctionStatus { NOT_STARTED, IN_PROGRESS, SOLD, WITHDRAWN }

class Auction {
    String id;
    Item item;
    Money startingPrice;
    Money reservePrice;
    Money currentBid;
    User highestBidder;
    AuctionStatus status;
    LocalDateTime endTime;
    List<Bid> bidHistory;

    boolean placeBid(Bid bid) {
        if (status != IN_PROGRESS || LocalDateTime.now().isAfter(endTime))
            throw new AuctionNotActiveException();
        if (bid.amount <= currentBid) throw new BidTooLowException();
        bidHistory.add(bid);
        currentBid = bid.amount;
        highestBidder = bid.bidder;
        return true;
    }
}

class Bid {
    String id;
    User bidder;
    Money amount;
    LocalDateTime timestamp;
}
```

### Q83: Design an Airline Reservation System (LLD).

**Answer:**

```java
class Flight {
    String flightNumber;
    String origin;
    String destination;
    LocalDateTime departureTime;
    LocalDateTime arrivalTime;
    Map<SeatClass, List<Seat>> seats;
}

class Reservation {
    String pnr;
    Flight flight;
    List<Seat> seats;
    Passenger primaryPassenger;
    ReservationStatus status;
}

class AirlineReservationSystem {
    List<Flight> searchFlights(String origin, String dest, LocalDate date) { /* ... */ }

    Reservation book(Flight flight, List<String> seatNumbers, Passenger passenger) {
        // Lock flight, check availability, create reservation
    }

    void confirmPayment(Reservation reservation) {
        reservation.status = CONFIRMED;
    }

    void cancelReservation(Reservation reservation) {
        reservation.status = CANCELLED;
    }
}
```

### Q84: Design a Remote Control (LLD — Command pattern).

**Answer:**

```java
class UniversalRemote {
    Map<String, Command> commands = new HashMap<>();
    Stack<Command> history = new Stack<>();

    void setCommand(String slot, Command command) {
        commands.put(slot, command);
    }
    void pressButton(String slot) {
        Command cmd = commands.get(slot);
        cmd.execute();
        history.push(cmd);
    }
    void undo() {
        if (!history.isEmpty()) history.pop().undo();
    }
}
```

### Q85: Design a Caching System (Strategy for eviction policies).

**Answer:**

```java
interface EvictionPolicy<K> {
    void keyAccessed(K key);
    K evictKey();
}

class LRUEviction<K> implements EvictionPolicy<K> {
    private LinkedHashSet<K> accessOrder = new LinkedHashSet<>();
    public void keyAccessed(K key) {
        accessOrder.remove(key);
        accessOrder.add(key);
    }
    public K evictKey() {
        K oldest = accessOrder.iterator().next();
        accessOrder.remove(oldest);
        return oldest;
    }
}

class Cache<K, V> {
    private final int capacity;
    private final Map<K, V> store = new HashMap<>();
    private final EvictionPolicy<K> evictionPolicy;

    Cache(int capacity, EvictionPolicy<K> policy) {
        this.capacity = capacity;
        this.evictionPolicy = policy;
    }

    V get(K key) {
        V value = store.get(key);
        if (value != null) evictionPolicy.keyAccessed(key);
        return value;
    }

    void put(K key, V value) {
        if (store.size() >= capacity && !store.containsKey(key)) {
            K evictedKey = evictionPolicy.evictKey();
            store.remove(evictedKey);
        }
        store.put(key, value);
        evictionPolicy.keyAccessed(key);
    }
}
```

### Q86: Design a Logging System with Multiple Appenders.

**Answer:**

```java
interface LogAppender { void append(LogMessage msg); }
class ConsoleAppender implements LogAppender { /* ... */ }
class FileAppender implements LogAppender { /* ... */ }
class DatabaseAppender implements LogAppender { /* ... */ }

class LoggerConfig {
    LogLevel level;
    List<LogAppender> appenders;
}

class Logger {
    LoggerConfig config;

    void log(LogLevel level, String message) {
        if (level.ordinal() >= config.level.ordinal()) {
            LogMessage msg = new LogMessage(level, message);
            for (LogAppender appender : config.appenders) {
                appender.append(msg);
            }
        }
    }
}
```

### Q87: Design a Shopping Cart with Discounts (LLD — Strategy + Composite).

**Answer:**

```java
interface Discount {
    Money apply(Money total, List<CartItem> items);
}

class PercentageDiscount implements Discount {
    double percentage;
    PercentageDiscount(double pct) { this.percentage = pct; }
    public Money apply(Money total, List<CartItem> items) {
        return total.multiply(1.0 - percentage / 100);
    }
}

class BuyXGetYFree implements Discount { /* ... */ }

class CompositeDiscount implements Discount { // Composite pattern
    List<Discount> discounts;
    public Money apply(Money total, List<CartItem> items) {
        for (Discount d : discounts) total = d.apply(total, items);
        return total;
    }
}
```

### Q88: Design a Notification System (LLD — Observer + Strategy).

**Answer:**

```java
enum NotificationType { EMAIL, SMS, PUSH }

interface NotificationSender {
    void send(User user, String message);
}
class EmailSender implements NotificationSender { /* ... */ }
class SmsSender implements NotificationSender { /* ... */ }
class PushSender implements NotificationSender { /* ... */ }

class NotificationService {
    private Map<NotificationType, NotificationSender> senders;

    void sendNotification(User user, NotificationType type, String message) {
        NotificationSender sender = senders.get(type);
        sender.send(user, message);
    }
}
```

### Q89: Design an Order Processing System (LLD — State pattern).

**Answer:**

```java
enum OrderState { NEW, CONFIRMED, PROCESSING, SHIPPED, DELIVERED, CANCELLED }

class Order {
    OrderState state = NEW;
    List<OrderItem> items;

    void confirm() {
        if (state != NEW) throw new InvalidStateException();
        state = CONFIRMED;
    }
    void ship() {
        if (state != CONFIRMED) throw new InvalidStateException();
        state = SHIPPED;
    }
    void deliver() {
        if (state != SHIPPED) throw new InvalidStateException();
        state = DELIVERED;
    }
    void cancel() {
        if (state == SHIPPED || state == DELIVERED) throw new CannotCancelException();
        state = CANCELLED;
    }
}
```

### Q90: Design a Ride-Sharing System (LLD).

**Answer:**

```java
class Rider { String id; String name; Location location; }
class Driver { String id; String name; Location location; boolean available; }
class Trip {
    String id;
    Rider rider;
    Driver driver;
    Location pickup;
    Location dropoff;
    TripStatus status; // REQUESTED, ACCEPTED, STARTED, COMPLETED, CANCELLED
    Money fare;
}

class RideSharingService {
    private List<Driver> drivers;
    private Map<String, Trip> trips;

    Trip requestRide(Rider rider, Location pickup, Location dropoff) {
        Driver nearest = findNearestDriver(pickup);
        if (nearest == null) throw new NoDriverAvailableException();
        Trip trip = new Trip(UUID.randomUUID().toString(), rider, nearest, pickup, dropoff, REQUESTED, calculateFare(pickup, dropoff));
        trips.put(trip.id, trip);
        nearest.available = false;
        return trip;
    }

    void acceptTrip(String tripId, Driver driver) { /* change status to ACCEPTED */ }
    void startTrip(String tripId) { /* STATUS to STARTED */ }
    void completeTrip(String tripId) { /* payment, STATUS to COMPLETED, driver.available = true */ }

    private Driver findNearestDriver(Location location) {
        return drivers.stream()
            .filter(d -> d.available)
            .min(Comparator.comparingDouble(d -> distance(d.location, location)))
            .orElse(null);
    }
}
```

### Q91: Design a Key-Value Store (LLD).

**Answer:**

```java
class Entry<K, V> {
    K key;
    V value;
    long timestamp;  // For TTL
    long version;    // For optimistic locking
}

class KVStore<K, V> {
    private final ConcurrentHashMap<K, Entry<K, V>> store = new ConcurrentHashMap<>();
    private final EvictionPolicy<K> evictionPolicy;
    private final int maxSize;

    V get(K key) {
        Entry<K, V> entry = store.get(key);
        if (entry == null) return null;
        if (isExpired(entry)) { store.remove(key); return null; }
        evictionPolicy.keyAccessed(key);
        return entry.value;
    }

    void put(K key, V value, long ttlMs) {
        if (store.size() >= maxSize && !store.containsKey(key)) {
            K evicted = evictionPolicy.evictKey();
            store.remove(evicted);
        }
        store.put(key, new Entry<>(key, value, System.currentTimeMillis() + ttlMs, 0));
        evictionPolicy.keyAccessed(key);
    }

    boolean compareAndSwap(K key, V expectedValue, V newValue) {
        return store.computeIfPresent(key, (k, entry) -> {
            if (Objects.equals(entry.value, expectedValue)) {
                entry.value = newValue;
                entry.version++;
                return entry;
            }
            return entry;
        }) != null;
    }
}
```

### Q92: Design a URL Shortener with Custom Alias (LLD).

**Answer:**

```java
class URLShortener {
    private static final String BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    String generateKey() {
        // Generate random 7-char base62 string
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 7; i++) {
            sb.append(BASE62.charAt(ThreadLocalRandom.current().nextInt(62)));
        }
        return sb.toString();
    }

    String shorten(String longUrl, String customAlias) {
        String key = (customAlias != null) ? customAlias : generateKey();
        if (urlRepo.exists(key)) throw new AliasAlreadyTakenException();
        urlRepo.save(key, longUrl);
        return "https://short.url/" + key;
    }

    String resolve(String shortKey) {
        String longUrl = cache.get(shortKey);
        if (longUrl == null) {
            longUrl = urlRepo.find(shortKey);
            cache.put(shortKey, longUrl);
        }
        return longUrl;
    }
}
```

### Q93: Design a Logger with JSON Output (LLD).

**Answer:**

```java
class JsonLogFormatter {
    String format(LogMessage msg) {
        return String.format(
            "{\"timestamp\":\"%s\",\"level\":\"%s\",\"thread\":\"%s\",\"message\":\"%s\"}",
            msg.timestamp, msg.level, msg.threadName, escapeJson(msg.message)
        );
    }
    private String escapeJson(String s) { return s.replace("\"", "\\\""); }
}

class JsonFileAppender implements LogAppender {
    private JsonLogFormatter formatter = new JsonLogFormatter();
    private BufferedWriter writer;

    public void append(LogMessage msg) {
        writer.write(formatter.format(msg));
        writer.newLine();
        writer.flush();
    }
}
```

### Q94: Design a Thread Pool (LLD).

**Answer:**

```java
class ThreadPool {
    private final BlockingQueue<Runnable> taskQueue = new LinkedBlockingQueue<>();
    private final List<Worker> workers;
    private volatile boolean running = true;

    ThreadPool(int numThreads) {
        workers = new ArrayList<>(numThreads);
        for (int i = 0; i < numThreads; i++) {
            Worker w = new Worker();
            workers.add(w);
            new Thread(w).start();
        }
    }

    void submit(Runnable task) {
        if (!running) throw new RejectedExecutionException();
        taskQueue.offer(task);
    }

    void shutdown() {
        running = false;
        for (Worker w : workers) w.interrupt();
    }

    class Worker implements Runnable {
        public void run() {
            while (running) {
                try {
                    Runnable task = taskQueue.poll(1, TimeUnit.SECONDS);
                    if (task != null) task.run();
                } catch (InterruptedException e) { break; }
            }
        }
    }
}
```

### Q95: Design a Load Balancer (LLD — Strategy pattern).

**Answer:**

```java
interface LoadBalancingStrategy {
    Server selectServer(List<Server> servers, Request request);
}

class RoundRobinStrategy implements LoadBalancingStrategy {
    private AtomicInteger index = new AtomicInteger(0);
    public Server selectServer(List<Server> servers, Request request) {
        return servers.get(index.getAndIncrement() % servers.size());
    }
}

class LeastConnectionsStrategy implements LoadBalancingStrategy {
    public Server selectServer(List<Server> servers, Request request) {
        return servers.stream().min(Comparator.comparingInt(Server::getActiveConnections)).orElseThrow();
    }
}

class LoadBalancer {
    private List<Server> servers;
    private LoadBalancingStrategy strategy;

    void handleRequest(Request request) {
        Server server = strategy.selectServer(servers, request);
        server.forward(request);
    }
}
```

### Q96: Design an Inventory Management System (LLD).

**Answer:**

```java
class Product {
    String sku;
    String name;
    int quantity;
    int reservedQuantity;
    int availableQuantity() { return quantity - reservedQuantity; }

    synchronized boolean reserve(int qty) {
        if (availableQuantity() < qty) return false;
        reservedQuantity += qty;
        return true;
    }
    synchronized void confirmReservation(int qty) {
        quantity -= qty;
        reservedQuantity -= qty;
    }
    synchronized void releaseReservation(int qty) {
        reservedQuantity -= qty;
    }
}

class InventoryService {
    private Map<String, Product> products;

    boolean reserveStock(String sku, int quantity) {
        Product product = products.get(sku);
        return product.reserve(quantity);
    }

    void confirmOrder(Order order) {
        for (OrderItem item : order.items) {
            Product product = products.get(item.sku);
            product.confirmReservation(item.quantity);
        }
    }
}
```

### Q97: Design a Consistent Hashing Ring (LLD).

**Answer:**

```java
class ConsistentHashRing<T> {
    private final TreeMap<Integer, T> ring = new TreeMap<>();
    private final int virtualNodes;
    private final HashFunction hashFn;

    ConsistentHashRing(int virtualNodes, HashFunction hashFn) {
        this.virtualNodes = virtualNodes;
        this.hashFn = hashFn;
    }

    void addNode(T node) {
        for (int i = 0; i < virtualNodes; i++) {
            ring.put(hashFn.hash(node.toString() + i), node);
        }
    }

    void removeNode(T node) {
        for (int i = 0; i < virtualNodes; i++) {
            ring.remove(hashFn.hash(node.toString() + i));
        }
    }

    T getNode(String key) {
        if (ring.isEmpty()) return null;
        Integer hash = hashFn.hash(key);
        Map.Entry<Integer, T> entry = ring.ceilingEntry(hash);
        if (entry == null) entry = ring.firstEntry();
        return entry.getValue();
    }
}
```

### Q98: Design a Distributed ID Generator (Snowflake).

**Answer:**

```java
class SnowflakeIdGenerator {
    private final long datacenterId;
    private final long machineId;
    private long sequence = 0;
    private long lastTimestamp = -1;

    // Bit layout: 1 sign + 41 timestamp + 5 datacenter + 5 machine + 12 sequence
    private static final long EPOCH = 1700000000000L;
    private static final int SEQUENCE_BITS = 12;
    private static final long MAX_SEQUENCE = (1L << SEQUENCE_BITS) - 1;

    synchronized long nextId() {
        long timestamp = System.currentTimeMillis();
        if (timestamp < lastTimestamp) throw new ClockSkewException();
        if (timestamp == lastTimestamp) {
            sequence = (sequence + 1) & MAX_SEQUENCE;
            if (sequence == 0) { /* wait for next millisecond */ timestamp = waitNextMillis(); }
        } else {
            sequence = 0;
        }
        lastTimestamp = timestamp;
        return ((timestamp - EPOCH) << 22)
             | (datacenterId << 17)
             | (machineId << 12)
             | sequence;
    }
}
```

### Q99: Design a Bloom Filter.

**Answer:**

```java
class BloomFilter {
    private final BitSet bitSet;
    private final int size;
    private final HashFunction[] hashFunctions;

    BloomFilter(int size, int numHashes) {
        this.size = size;
        this.bitSet = new BitSet(size);
        this.hashFunctions = new HashFunction[numHashes];
        for (int i = 0; i < numHashes; i++) {
            final int seed = i;
            hashFunctions[i] = key -> Math.abs((key.hashCode() ^ (seed * 0x9E3779B9)) % size);
        }
    }

    void add(String key) {
        for (HashFunction hf : hashFunctions) bitSet.set(hf.hash(key));
    }

    boolean mightContain(String key) {
        for (HashFunction hf : hashFunctions) {
            if (!bitSet.get(hf.hash(key))) return false;
        }
        return true;  // May return false positive, never false negative
    }

    @FunctionalInterface
    interface HashFunction { int hash(String key); }
}
```

### Q100: Design a Rate Limiter using Sliding Window Log.

**Answer:**

```java
class SlidingWindowRateLimiter {
    private final int maxRequests;
    private final long windowSizeMs;
    private final Map<String, Queue<Long>> userRequestLogs = new ConcurrentHashMap<>();

    SlidingWindowRateLimiter(int maxRequests, long windowSizeMs) {
        this.maxRequests = maxRequests;
        this.windowSizeMs = windowSizeMs;
    }

    boolean allowRequest(String userId) {
        long now = System.currentTimeMillis();
        Queue<Long> timestamps = userRequestLogs.computeIfAbsent(userId, k -> new LinkedList<>());

        synchronized (timestamps) {
            // Remove expired timestamps
            while (!timestamps.isEmpty() && timestamps.peek() < now - windowSizeMs) {
                timestamps.poll();
            }
            if (timestamps.size() >= maxRequests) return false;
            timestamps.offer(now);
            return true;
        }
    }
}
```

