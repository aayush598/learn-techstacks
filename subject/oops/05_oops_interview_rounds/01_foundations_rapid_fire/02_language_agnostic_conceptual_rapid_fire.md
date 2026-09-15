# Language-Agnostic Conceptual Rapid Fire — 100 Interview Q&A

## Q1: What is object-oriented programming and why do we use it?

**A:** Object-oriented programming (OOP) is a programming paradigm centered around the concept of "objects" — entities that bundle data (attributes) and behavior (methods) together. Rather than organizing code around functions that operate on loose data, OOP models software around real or abstract entities that interact with each other. This approach emerged in the 1960s-70s with languages like Simula and Smalltalk, and became dominant with C++, Java, and C#.

The core motivation behind OOP is managing complexity. As software systems grow, procedural code becomes difficult to maintain because state and behavior are scattered. OOP addresses this through four pillars: encapsulation (hiding internal state), abstraction (exposing only relevant interfaces), inheritance (sharing structure across related types), and polymorphism (treating different types uniformly). Together, these principles promote modularity, reusability, and easier debugging.

In practice, OOP allows teams to build large systems by composing smaller, well-defined objects. Each object owns its state and exposes controlled ways to interact with it. This reduces side effects, makes code easier to reason about, and enables parallel development since teams can work on different objects independently. Modern software engineering — from web frameworks to game engines — relies heavily on OOP principles even when mixed with functional paradigms.

**Example:**
```java
class BankAccount {
    private double balance;

    public BankAccount(double initial) {
        this.balance = initial;
    }

    public void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    public double getBalance() {
        return balance;
    }
}
```

## Q2: Explain the four pillars of OOP by linking each one to a concrete engineering benefit.

**A:** The four pillars are encapsulation, abstraction, inheritance, and polymorphism. Encapsulation bundles data and methods within a class and restricts direct access to internal state, exposing only controlled interfaces. This protects invariants and reduces coupling between components. Abstraction hides complex implementation details behind simple interfaces, allowing consumers to use objects without understanding their internals.

Inheritance establishes an "is-a" relationship between classes, allowing a child class to inherit fields and methods from a parent class. This promotes code reuse and creates natural taxonomies. Polymorphism allows objects of different types to be treated through a common interface — a method call on a parent reference can execute different implementations depending on the actual runtime type. This is the foundation of flexible, extensible designs.

Each pillar solves a distinct problem. Encapsulation protects data integrity. Abstraction reduces cognitive load. Inheritance eliminates duplication across related types. Polymorphism enables open-closed designs where new types can be added without modifying existing client code. Mastering how these pillars interact is essential for designing robust systems.

**Example:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

class Square(Shape):
    def __init__(self, s):
        self.s = s
    def area(self):
        return self.s ** 2
```

## Q3: What is encapsulation and why is it important?

**A:** Encapsulation is the principle of bundling data and the methods that operate on that data into a single unit (a class), while restricting external access to the internal state. Instead of exposing raw fields, a class provides controlled access through methods (getters/setters or behavior methods) that enforce invariants and validate inputs. This is fundamentally about information hiding — the internal representation of an object is hidden from the outside world.

Encapsulation is important because it creates clear boundaries between components. When a class hides its internal state, it gains the freedom to change its implementation without breaking dependent code. For example, a class might store its data in a list internally but later switch to a tree for performance — callers never notice because they interact only through the public interface. This is the Information Hiding principle articulated by David Parnas.

Beyond maintainability, encapsulation enforces business rules. A bank account class can prevent negative balances by making the balance field private and only allowing deposits and withdrawals through validated methods. Without encapsulation, any external code could directly manipulate the balance, creating bugs that are extremely hard to trace. Encapsulation is the first line of defense for data integrity in any OOP system.

**Example:**
```cpp
class Temperature {
private:
    double celsius;
public:
    void setCelsius(double c) {
        if (c < -273.15) throw std::invalid_argument("Below absolute zero");
        celsius = c;
    }
    double getFahrenheit() const { return celsius * 9.0/5.0 + 32; }
};
```

## Q4: What is abstraction and how does it differ from encapsulation?

**A:** Abstraction is the process of exposing only the essential features of an object while hiding unnecessary implementation details. It operates at the design level — you decide what an object *can do* without committing to *how* it does it. Encapsulation, on the other hand, operates at the implementation level — it is the mechanism that enforces the boundary between what is exposed and what is hidden. You can think of abstraction as the "what" and encapsulation as the "how."

Abstraction is typically achieved through abstract classes and interfaces. An abstract class defines a contract (a set of methods) without providing complete implementations. Concrete subclasses fill in the details. This allows different implementations to be swapped transparently — a sorting algorithm doesn't need to know whether it's operating on an array or a linked list, as long as both implement the expected interface.

In practice, good abstraction means designing interfaces that are minimal and focused. The Interface Segregation Principle states that no client should be forced to depend on methods it does not use. A well-abstracted system has thin interfaces that capture behavior, not implementation. This is what enables the loose coupling that makes large systems maintainable — components interact through abstract contracts rather than concrete types.

**Example:**
```java
interface PaymentProcessor {
    void pay(double amount);
}

class StripeProcessor implements PaymentProcessor {
    public void pay(double amount) {
        // Stripe-specific logic hidden from caller
    }
}
```

## Q5: What is inheritance and when should you use it?

**A:** Inheritance is a mechanism where a new class (child/subclass) derives attributes and behaviors from an existing class (parent/superclass). The child class can reuse code from the parent and extend or override behavior as needed. This establishes an "is-a" relationship: a Dog *is an* Animal, a SavingsAccount *is an* Account. Inheritance is one of the primary tools for code reuse and establishing type hierarchies.

You should use inheritance when there is a genuine hierarchical relationship between entities and when the child class truly extends the parent's behavior rather than just reusing code. For example, a `Vehicle` base class with `start()`, `stop()`, and `accelerate()` makes sense when you have `Car`, `Truck`, and `Motorcycle` subclasses that each implement these operations differently. The shared interface and common behavior live in the parent, while specialization lives in the children.

However, inheritance is often overused. It creates tight coupling between parent and child — changes in the parent cascade to all children. Many experts recommend preferring composition over inheritance. Use inheritance for genuine "is-a" relationships with stable hierarchies. Use composition ("has-a") when you need flexibility, such as when behavior needs to change at runtime. The Liskov Substitution Principle must always hold: any child must be usable wherever the parent is expected without surprising the caller.

**Example:**
```cpp
class Animal {
public:
    virtual void speak() const = 0;
    virtual ~Animal() {}
};

class Dog : public Animal {
public:
    void speak() const override { std::cout << "Woof\n"; }
};
```

## Q6: What is polymorphism and what types exist?

**A:** Polymorphism means "many forms" — it allows objects of different types to be treated through a common interface. The same method call can produce different behaviors depending on the actual runtime type of the object. This is the mechanism that enables open-closed designs: you can add new types without modifying the code that works with the existing types. Polymorphism is arguably the most powerful concept in OOP because it decouples the *use* of objects from their *creation*.

The two primary forms are compile-time (static) polymorphism and runtime (dynamic) polymorphism. Compile-time polymorphism includes method overloading (same method name, different parameter lists) and operator overloading. The compiler resolves which version to call at compile time. Runtime polymorphism uses virtual dispatch — a virtual method call on a parent reference resolves to the correct child implementation at runtime based on the actual object type, not the reference type.

Runtime polymorphism is achieved through virtual functions and vtables (in C++) or dynamic dispatch (in Java/Python). When you call `animal.speak()` on an `Animal` reference, the runtime determines whether the actual object is a `Dog` or a `Cat` and invokes the correct implementation. This indirection is what makes plugin architectures, strategy patterns, and dependency injection possible — you program to an interface and let the runtime select the concrete behavior.

**Example:**
```python
class Notification:
    def send(self, msg):
        raise NotImplementedError

class Email(Notification):
    def send(self, msg):
        print(f"Email: {msg}")

class SMS(Notification):
    def send(self, msg):
        print(f"SMS: {msg}")

def dispatch(n: Notification, msg: str):
    n.send(msg)
```

## Q7: Describe a refactoring where inheritance is replaced by composition, and explain why the change improves the design?

**A:** Inheritance establishes an "is-a" relationship where a child class is a specialized version of the parent. Composition establishes a "has-a" relationship where an object contains other objects as parts. A `Car` has an `Engine` (composition) but a `Car` is a `Vehicle` (inheritance). This distinction matters because it affects flexibility, coupling, and maintainability.

Composition is generally preferred over inheritance in modern OOP design. With composition, you assemble behavior by combining objects rather than inheriting from a hierarchy. This is more flexible because you can swap components at runtime, whereas inheritance is fixed at compile time. Composition also avoids the fragile base class problem — changes to a parent class can unexpectedly break child classes, but composed objects are insulated from each other's internal changes.

The practical guideline is: use inheritance when the relationship is a clear "is-a" with a stable hierarchy, and the child genuinely extends the parent's semantics. Use composition when you need flexibility, when behavior should vary at runtime, or when the "is-a" relationship doesn't hold cleanly. Many experienced developers default to composition and only reach for inheritance when there is a compelling reason. Libraries like the Strategy pattern, Decorator pattern, and Dependency Injection all leverage composition to achieve loose coupling.

**Example:**
```java
class Engine { void start() { } }

class Car {
    private Engine engine; // composition
    Car() { this.engine = new Engine(); }
}
```

## Q8: How do you detect an LSP violation in an existing codebase, and what refactoring usually resolves it?

**A:** The Liskov Substitution Principle states that objects of a child class should be able to replace objects of the parent class without altering the correctness of the program. In other words, if a function works with a parent type, it must work correctly with any child type without knowing it. This is one of the five SOLID principles and is fundamental to designing correct inheritance hierarchies.

A classic violation is the Rectangle-Square problem. If `Square` extends `Rectangle`, setting the width should also change the height to maintain the square invariant. But code that uses `Rectangle` references expects width and height to be independent. This breaks the contract. The principle demands that child classes honor the behavioral contracts (preconditions, postconditions, and invariants) established by the parent.

LSP forces you to think carefully about your type hierarchies. Before creating a child class, ask: "Can I use this child wherever the parent is expected without surprises?" If the answer is no, the hierarchy is wrong. This often means you need to restructure — perhaps using interfaces to separate concerns rather than inheritance. Adherence to LSP is what makes polymorphism reliable; without it, code that relies on polymorphic dispatch becomes fragile and buggy.

**Example:**
```cpp
class Bird {
public:
    virtual void fly() { /* ... */ }
};

class Ostrich : public Bird {
public:
    void fly() override { throw std::logic_error("Can't fly"); } // violates LSP
};
```

## Q9: What is the SOLID principle?

**A:** SOLID is an acronym for five design principles that make object-oriented systems easier to maintain and extend: Single Responsibility (a class should have only one reason to change), Open-Closed (open for extension, closed for modification), Liskov Substitution (child types must be substitutable for parent types), Interface Segregation (many specific interfaces are better than one general-purpose interface), and Dependency Inversion (depend on abstractions, not concretions).

These principles work together to reduce coupling and increase cohesion. The Single Responsibility Principle ensures each class has a focused purpose, making changes predictable. The Open-Closed Principle lets you add new behavior by creating new classes rather than modifying existing ones. LSP ensures inheritance hierarchies are correct. ISP prevents bloated interfaces. DIP ensures high-level modules are not coupled to low-level implementation details.

In practice, SOLID guides architectural decisions at every level. When you inject a `PaymentGateway` interface rather than a concrete `StripeGateway`, you're applying DIP. When you split a monolithic `UserManager` class into `AuthService`, `ProfileService`, and `NotificationService`, you're applying SRP. SOLID isn't dogma — it's a set of trade-offs — but following these principles consistently produces systems that are easier to test, extend, and refactor over time.

**Example:**
```java
// Dependency Inversion
interface Logger { void log(String msg); }
class FileLogger implements Logger { public void log(String msg) { } }
class UserService {
    private Logger logger;
    UserService(Logger logger) { this.logger = logger; }
}
```

## Q10: What is a class and an object?

**A:** A class is a blueprint or template that defines the structure (fields/attributes) and behavior (methods) that objects of that type will have. An object is a concrete instance of a class — a runtime entity that has actual values in its fields and can execute its methods. The class defines the schema; the object is the populated instance of that schema at runtime.

Think of a class as an architectural blueprint and an object as the actual building. The blueprint defines where walls, doors, and windows go, but the building is the real thing you can inhabit. Multiple objects can be created from the same class, each with its own state. Two `Person` objects might have the same methods but different names and ages.

In most languages, you create an object using a constructor — a special method that initializes the object's state. Once created, the object lives in memory and can be referenced, passed around, and manipulated. Objects have identity (each is unique in memory), state (the current values of its fields), and behavior (the methods it can execute). Understanding the distinction between class and object is foundational to all of OOP.

**Example:**
```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return f"{self.name} says Woof"

buddy = Dog("Buddy")
print(buddy.bark())
```

## Q11: What is a constructor and what types exist?

**A:** A constructor is a special method that is automatically called when an object is created. Its purpose is to initialize the object's state — setting initial values for fields, allocating resources, or performing setup logic. In most languages, the constructor has the same name as the class and no return type. Constructors are essential because they ensure objects start in a valid, consistent state.

The most common types are default constructors (no parameters, initializes to default values), parameterized constructors (accept arguments to set initial state), copy constructors (create a new object as a copy of an existing one), and destructors (the inverse, cleaning up when an object is destroyed). Some languages support constructor chaining, where one constructor delegates to another to avoid duplicating initialization logic.

Constructor design matters because it's your first opportunity to enforce invariants. A well-designed constructor validates inputs and rejects invalid state upfront. For example, a `Date` constructor should reject invalid day/month combinations immediately rather than allowing an object with bad state to propagate through the system. Constructor chaining with `this()` (Java) or delegation patterns reduces code duplication while maintaining consistency.

**Example:**
```java
class Employee {
    private String name;
    private double salary;

    Employee() { this("Unknown", 0); }
    Employee(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }
}
```

## Q12: What is a destructor and how does it differ from a constructor?

**A:** A destructor is a special method that is automatically called when an object is destroyed or goes out of scope. While the constructor initializes an object's resources, the destructor cleans them up — releasing memory, closing file handles, releasing locks, or deallocating network connections. In C++, the destructor name is `~ClassName()` and takes no parameters. In languages with garbage collection like Java or Python, destructors are less critical but still used for cleanup (e.g., `__del__` in Python, `finalize()` in Java).

The key difference is timing and purpose: constructors run once when an object is born, and destructors run once when it dies. Constructors allocate and initialize; destructors deallocate and clean up. This symmetry is fundamental to RAII (Resource Acquisition Is Initialization) in C++, where object lifetime directly manages resource lifetimes. In garbage-collected languages, the runtime determines when objects are collected, so destructors are not guaranteed to run at a specific time.

Destructor design requires care with inheritance hierarchies. In C++, destructors should be virtual in base classes that are meant to be inherited from, because deleting a derived object through a base pointer without a virtual destructor leads to undefined behavior. In Java, `finalize()` is deprecated because it's unreliable and has performance overhead. The modern approach in managed languages is to use explicit cleanup patterns (like `AutoCloseable` in Java or context managers in Python) rather than relying on destructors.

**Example:**
```cpp
class FileHandler {
    std::FILE* fp;
public:
    FileHandler(const char* name) { fp = std::fopen(name, "r"); }
    ~FileHandler() { if (fp) std::fclose(fp); }
};
```

## Q13: What is the difference between overloading and overriding?

**A:** Overloading (compile-time polymorphism) occurs when multiple methods share the same name but have different parameter lists (different types, number, or order of parameters). The compiler determines which version to call based on the arguments at compile time. Overloading is a compile-time decision and is resolved statically. Method overloading is a form of static polymorphism.

Overriding (runtime polymorphism) occurs when a child class provides a specific implementation of a method that is already defined in its parent class. The method signature must match exactly (same name, return type, and parameters). Overriding is resolved at runtime based on the actual object type, not the reference type. This is how dynamic dispatch works — a `Shape` reference pointing to a `Circle` object will call `Circle.draw()` when `draw()` is invoked.

The distinction is critical: overloading creates multiple methods that coexist in the same class (or across the hierarchy with different signatures), while overriding replaces a parent's implementation entirely. Overloading is about convenience — giving the same operation different entry points. Overriding is about specialization — letting a subclass customize behavior. Misunderstanding this leads to subtle bugs, especially when a developer intends to override but accidentally overloads by changing the signature.

**Example:**
```java
class Printer {
    void print(String s) { } // overloaded
    void print(int n) { }    // overloaded
    void print(double d) { } // overloaded
}

class ColorPrinter extends Printer {
    @Override
    void print(String s) { } // overridden
}
```

## Q14: When would you choose an abstract class over an interface while designing a real system?

**A:** An abstract class is a class that cannot be instantiated directly and may contain both abstract (unimplemented) methods and concrete (implemented) methods. It serves as a partial implementation that child classes extend and complete. An interface is a pure contract that defines a set of methods (and sometimes constants) that implementing classes must provide. In modern languages, interfaces can have default method implementations.

The fundamental distinction is about what they represent. An abstract class represents a partial implementation of a concept — it can hold state, have constructors, and provide shared utility methods. An interface represents a capability or contract — it says "anything that implements this can do X." A `Vehicle` abstract class might provide shared engine logic while requiring subclasses to implement `start()`. A `Drivable` interface just declares the contract without any implementation.

In practice, use abstract classes when you have shared code that naturally belongs in a base type and the hierarchy is relatively stable. Use interfaces when you need to define capabilities that unrelated types can implement, or when you need multiple inheritance of type (a class can implement many interfaces but extend only one class). Java and C# combine both mechanisms effectively. Some languages like Go have only interfaces. The trend in modern design is to prefer interfaces for flexibility and use abstract classes sparingly when shared implementation is truly necessary.

**Example:**
```python
from abc import ABC, abstractmethod

class AbstractLogger(ABC):
    @abstractmethod
    def write(self, msg): pass

class ConsoleLogger(AbstractLogger):
    def write(self, msg):
        print(msg)
```

## Q15: What is multiple inheritance and what problem does it cause?

**A:** Multiple inheritance is the ability of a class to inherit from more than one parent class simultaneously. Languages like C++ and Python support it, while Java and C# do not (a class can extend only one class, though it can implement multiple interfaces). Multiple inheritance can be powerful — a `FlyingFish` could inherit from both `Fish` and `Bird` — but it introduces significant complexity.

The primary problem is the Diamond Problem. If class D inherits from both B and C, and both B and C inherit from A, then D has two copies of A's state and behavior. Which version of A's methods does D use? This ambiguity is difficult to resolve cleanly. Different languages have different solutions: C++ uses virtual inheritance, Python uses a complex MRO (Method Resolution Order) based on C3 linearization, and Java simply disallows it for classes.

The Diamond Problem is not just theoretical — it creates real maintenance headaches. When two parent classes define the same method with different implementations, the child class must explicitly resolve the ambiguity, which is error-prone and hard to understand. Most modern languages avoid this by supporting multiple inheritance of *type* through interfaces (which carry no implementation) while restricting multiple inheritance of *implementation* through classes. This gives you the flexibility of multiple contracts without the ambiguity of multiple implementations.

**Example:**
```cpp
class A { public: void greet() { } };
class B : virtual public A { };
class C : virtual public A { };
class D : public B, public C { }; // virtual inheritance resolves ambiguity
```

## Q16: What is the difference between a value type and a reference type?

**A:** A value type holds its data directly — when you assign one value type to another, a complete copy of the data is made. Primitive types (int, float, bool) are typically value types. A reference type holds a pointer (reference) to the actual data in memory — when you assign one reference type to another, you copy the reference, not the underlying data. Both variables then point to the same object. Classes in most languages produce reference types; structs produce value types.

This distinction has profound implications for behavior. With value types, modifying one copy never affects another — they are independent. With reference types, two variables can alias the same object, so modifying through one reference is visible through the other. This aliasing is a common source of bugs, especially when objects are passed to methods that might mutate them unexpectedly.

Memory management also differs. Value types are typically allocated on the stack (fast, automatic cleanup) or inline within objects (reducing heap pressure). Reference types are allocated on the heap and managed by garbage collectors (or manual management in C++). Understanding value vs. reference semantics is essential for writing correct and efficient code. Languages like C++ let you choose explicitly with pass-by-value vs. pass-by-reference, while Java uses references for objects and values for primitives, and C# has both `struct` (value) and `class` (reference).

**Example:**
```java
class Point { int x, y; Point(int x, int y) { this.x = x; this.y = y; } }

Point a = new Point(1, 2);
Point b = a; // b references the same object
b.x = 10;   // a.x is also 10 now
```

## Q17: What is a design pattern and why are they useful?

**A:** A design pattern is a reusable, proven solution to a commonly occurring problem in software design. Patterns are not code you copy-paste — they are templates for solving a category of design problems. The concept was popularized by the "Gang of Four" (GoF) book in 1994, which cataloged 23 patterns organized into creational, structural, and behavioral categories.

Patterns are useful because they provide a shared vocabulary and proven approaches. When a team says "let's use the Observer pattern," everyone immediately understands the structure and intent without needing to explain from scratch. Patterns encode lessons learned by experienced developers — they represent solutions that have been tested across many contexts. They also guide you toward flexible, maintainable designs by encapsulating change, reducing coupling, and managing complexity.

However, patterns should not be applied dogmatically. Over-engineering with patterns when simpler solutions suffice is a common anti-pattern. The right approach is to understand the problem first, then reach for a pattern if it genuinely fits. The most commonly used patterns include Singleton (single instance), Factory (object creation), Observer (event notification), Strategy (algorithm selection), Decorator (dynamic behavior extension), and Adapter (interface conversion). Understanding *why* a pattern exists is more important than memorizing its structure.

**Example:**
```python
class Observer:
    def update(self, event): pass

class EventEmitter:
    def __init__(self):
        self._observers = []
    def subscribe(self, obs):
        self._observers.append(obs)
    def emit(self, event):
        for obs in self._observers:
            obs.update(event)
```

## Q18: What is a design pattern's classification (creational, structural, behavioral)?

**A:** The 23 GoF patterns are classified into three categories based on what aspect of object creation, composition, or communication they address. Creational patterns deal with object creation mechanisms — how objects are instantiated in a way appropriate to the situation. Examples include Singleton (ensures one instance), Factory Method (defers instantiation to subclasses), Abstract Factory (creates families of related objects), Builder (step-by-step complex object construction), and Prototype (clones existing objects).

Structural patterns deal with how objects and classes are composed to form larger structures. They use inheritance and composition to create new functionality from existing parts. Examples include Adapter (converts one interface to another), Decorator (adds behavior dynamically), Facade (simplifies a complex subsystem), Proxy (controls access to an object), Composite (treats individual and composite objects uniformly), Bridge (separates abstraction from implementation), and Flyweight (shares common state to reduce memory usage).

Behavioral patterns deal with communication between objects — how they interact and distribute responsibility. Examples include Observer (one-to-many notification), Strategy (interchangeable algorithms), Command (encapsulates requests as objects), State (alters behavior based on internal state), Template Method (defines algorithm skeleton, defers steps to subclasses), Iterator (sequential access without exposing representation), and Chain of Responsibility (passes requests along a chain of handlers). Understanding these categories helps you identify which pattern category fits your problem.

**Example:**
```java
// Creational: Factory
class ShapeFactory {
    static Shape create(String type) {
        switch (type) {
            case "circle": return new Circle();
            case "square": return new Square();
            default: throw new IllegalArgumentException();
        }
    }
}
```

## Q19: What is the Singleton pattern and when is it appropriate?

**A:** The Singleton pattern ensures that a class has exactly one instance and provides a global point of access to it. This is useful when exactly one object is needed to coordinate actions across the system — logging, configuration management, database connections, or thread pools. The classic implementation involves a private constructor, a static instance variable, and a public static method that returns the single instance.

However, the Singleton pattern is widely considered an anti-pattern when overused. It introduces global state, which makes testing extremely difficult (you can't mock or replace the singleton easily in tests), hides dependencies (any code anywhere can access it without being declared as a dependency), and violates the Single Responsibility Principle (manages its own lifecycle and its actual business logic). It also creates tight coupling between the singleton and all its consumers.

In practice, prefer dependency injection over singletons. Pass the shared resource explicitly rather than having classes reach for a global instance. If you truly need exactly one instance (like a database connection pool), manage its lifecycle through a container (like a DI framework or application context) rather than the classic static singleton pattern. If you must use a Singleton, make it thread-safe (using double-checked locking, enum-based implementation in Java, or module-level instances in Python) and be aware of the trade-offs.

**Example:**
```java
class Database {
    private static Database instance;
    private Database() {}
    public static synchronized Database getInstance() {
        if (instance == null) instance = new Database();
        return instance;
    }
}
```

## Q20: What is the Factory pattern?

**A:** The Factory pattern encapsulates object creation logic, delegating the decision of which concrete class to instantiate to a separate factory method or class. Instead of calling `new ConcreteClass()` directly, clients call `factory.create()` which returns an object implementing a known interface. This decouples the client from the concrete classes it uses, allowing the concrete types to change without modifying client code.

The Factory Method pattern defines an interface for creating an object but lets subclasses decide which class to instantiate. The Abstract Factory pattern provides an interface for creating families of related objects without specifying their concrete classes. For example, a UI toolkit might have a `WidgetFactory` interface with `createButton()` and `createTextBox()` methods, with `WindowsFactory` and `MacFactory` implementations that create platform-appropriate widgets.

Factories are appropriate when object creation is complex, when you need to support multiple families of related objects, or when you want to hide the concrete types from clients. They are a cornerstone of the Dependency Inversion Principle — high-level modules depend on abstractions (interfaces) while low-level modules (concrete implementations) are created by factories. The trade-off is added complexity; for simple cases, direct instantiation is clearer. Most frameworks and libraries use factories extensively — think of `Collections.unmodifiableList()` in Java or `pathlib.Path()` in Python.

**Example:**
```python
class Dog:
    def speak(self): return "Woof"
class Cat:
    def speak(self): return "Meow"

def animal_factory(kind):
    return Dog() if kind == "dog" else Cat()
```

## Q21: What is the Observer pattern?

**A:** The Observer pattern defines a one-to-many dependency between objects: when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically. This is the backbone of event-driven programming. The subject maintains a list of observers and provides methods to subscribe and unsubscribe. When state changes, the subject iterates through observers and calls their update method.

This pattern decouples the subject from its observers — the subject doesn't need to know what the observers do, only that they implement an update interface. This is essential for building reactive systems, UI frameworks, message queues, and notification systems. For example, a spreadsheet cell might notify multiple chart objects when its value changes, and each chart updates independently.

Modern applications use variations of this pattern extensively. React's state management, Vue's reactivity system, and JavaScript's event emitters are all Observer pattern implementations. The challenge with the basic Observer pattern is managing subscription lifecycles — failing to unsubscribe leads to memory leaks. Also, cascading updates (observer A updates the subject, which notifies observer B, which updates the subject again) can cause infinite loops. Solutions include using weak references for observers, implementing batch updates, or using event buses that support priority ordering and cancellation.

**Example:**
```java
class Subject {
    private List<Observer> observers = new ArrayList<>();
    void attach(Observer o) { observers.add(o); }
    void notifyAll(String event) {
        for (Observer o : observers) o.update(event);
    }
}
```

## Q22: What is the Strategy pattern?

**A:** The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from the clients that use it. The pattern uses composition: the context object holds a reference to a strategy interface, and different concrete strategies can be swapped at runtime. This is an alternative to using conditional statements to select behavior.

For example, instead of a `Sorter` class with `if (algorithm == "quick") ... else if (algorithm == "merge") ...`, you create a `SortStrategy` interface with `sort(data)` and separate `QuickSort`, `MergeSort`, and `BubbleSort` implementations. The `Sorter` context holds a `SortStrategy` reference and delegates sorting to it. The strategy can be changed at runtime — the same sorter can switch between algorithms based on data size or performance requirements.

The Strategy pattern is one of the most widely used patterns because it directly supports the Open-Closed Principle — adding a new algorithm requires only creating a new strategy class, not modifying existing code. It eliminates conditional logic and makes algorithms independently testable. Common uses include sorting strategies, compression algorithms, authentication methods, pricing models, and rendering techniques. The trade-off is a slight increase in the number of classes, but the flexibility gained usually justifies it.

**Example:**
```python
class Compressor:
    def compress(self, data): raise NotImplementedError

class ZipCompressor(Compressor):
    def compress(self, data): return f"zipped({data})"

class GzipCompressor(Compressor):
    def compress(self, data): return f"gzip({data})"

class Archiver:
    def __init__(self, strategy: Compressor):
        self.strategy = strategy
    def archive(self, data):
        return self.strategy.compress(data)
```

## Q23: What is the Decorator pattern?

**A:** The Decorator pattern dynamically adds behavior to an object without modifying its structure or using inheritance. It wraps the original object in a decorator object that conforms to the same interface, adding its own behavior before or after delegating to the wrapped object. Decorators can be stacked — multiple decorators can wrap the same object, each adding a layer of behavior.

This pattern is an alternative to subclassing for extending behavior. With inheritance, you create static hierarchies: `BoldText`, `ItalicText`, `BoldItalicText`, etc. — an exponential explosion. With decorators, you compose behaviors dynamically: `new Bold(new Italic(new PlainText()))`. Each decorator implements the same interface and delegates to the wrapped component, adding its own logic in the process.

The most famous application is Java I/O streams: `BufferedReader` decorates `FileReader`, which decorates `InputStream`. Python's built-in decorators (`@property`, `@lru_cache`) use a similar concept. The pattern is powerful for adding cross-cutting concerns like logging, authentication, caching, or compression without polluting the core business logic. The trade-off is that decorated objects can become difficult to debug because the actual type at runtime is a nested wrapper rather than the base class, and stack traces can be deeply nested.

**Example:**
```java
interface DataSource { void write(String data); }

class FileDataSource implements DataSource { public void write(String d) { } }

class EncryptedSource implements DataSource {
    private DataSource wrap;
    EncryptedSource(DataSource ds) { this.wrap = ds; }
    public void write(String d) { wrap.write(encrypt(d)); }
    private String encrypt(String d) { return d; }
}
```

## Q24: What is the Adapter pattern?

**A:** The Adapter pattern converts the interface of one class into an interface that clients expect. It lets classes work together that otherwise couldn't because of incompatible interfaces. The adapter acts as a bridge between the existing interface and the required interface, translating calls from one format to another without modifying the original classes.

There are two forms: class adapter (using inheritance) and object adapter (using composition). Object adapters are generally preferred because they can adapt any subclass of the adapted class and avoid the limitations of single inheritance. For example, if you have a legacy `XMLParser` that outputs XML but your system expects JSON, an adapter can wrap the XMLParser and translate its output to JSON without modifying either the parser or the system.

Adapters are essential in real-world systems because you rarely control all the libraries and APIs you depend on. Third-party libraries, legacy systems, and external APIs all have their own interfaces. Rather than rewriting your code to match each one, you write adapters that translate between interfaces. This is the same principle behind USB-C adapters — they don't change the device or the port, they translate between them. In software, this pattern enables loose coupling between systems and makes it easy to swap out dependencies.

**Example:**
```python
class OldPrinter:
    def print_old(self, text): return f"OLD: {text}"

class NewPrinterInterface:
    def print_new(self, text): raise NotImplementedError

class PrinterAdapter(NewPrinterInterface):
    def __init__(self, old: OldPrinter):
        self.old = old
    def print_new(self, text):
        return self.old.print_old(text)
```

## Q25: What is the difference between tight coupling and loose coupling?

**A:** Tight coupling occurs when components are highly dependent on each other — changes in one component directly require changes in another. If class A directly instantiates class B, accesses B's internal fields, and B's behavior changes, A must change too. This creates fragile systems where a single change can cascade across the codebase. Loose coupling occurs when components interact through well-defined interfaces with minimal knowledge of each other's internals.

Loose coupling is achieved through abstraction, dependency injection, and interfaces. Instead of class A creating class B directly, it receives B through a constructor parameter typed as an interface. A doesn't know or care what the concrete implementation is — it just calls methods on the interface. This means you can swap B's implementation without touching A's code. Loose coupling makes systems more testable (you can mock dependencies), more maintainable (changes are isolated), and more flexible (components can evolve independently).

The practical test for coupling: if you can change the implementation of a dependency without modifying any of its consumers, the coupling is loose. If changing a dependency forces changes in consumers, it's tight. Every `new ConcreteClass()` inside a method is a potential tight coupling point. Using dependency injection containers, interface-based design, and event-driven communication are the primary techniques for achieving loose coupling in production systems.

**Example:**
```java
// Tight: new MySQLDatabase() inside UserService
// Loose:
class UserService {
    private Database db;
    UserService(Database db) { this.db = db; } // injected dependency
}
```

## Q26: What is a virtual function and how does virtual dispatch work?

**A:** A virtual function is a member function declared in a base class that can be overridden in derived classes. When called through a base class pointer or reference, the actual function executed is determined at runtime based on the real (dynamic) type of the object, not the static type of the pointer. This mechanism is called virtual dispatch (or dynamic dispatch) and is the foundation of runtime polymorphism in OOP.

Under the hood, most implementations use a virtual method table (vtable). Each class with virtual functions has a vtable — an array of function pointers, one per virtual function. Each object contains a hidden pointer (vptr) to its class's vtable. When a virtual function is called, the runtime follows the vptr to the vtable, looks up the function pointer at the correct index, and calls it. This indirection adds a small overhead compared to direct function calls but enables powerful polymorphic behavior.

Virtual dispatch is essential for achieving the Open-Closed Principle. Without it, adding new types requires modifying existing switch statements or conditionals that select behavior based on type. With virtual dispatch, you simply create a new class that overrides the virtual function, and the existing code works without modification. The cost is a single pointer indirection per call — negligible in almost all contexts. In C++, forgetting to make a destructor virtual when deleting derived objects through base pointers causes undefined behavior, making it a critical correctness concern.

**Example:**
```cpp
class Base {
public:
    virtual void identify() const { std::cout << "Base\n"; }
    virtual ~Base() {}
};

class Derived : public Base {
public:
    void identify() const override { std::cout << "Derived\n"; }
};

void print(Base const& obj) { obj.identify(); } // prints Derived at runtime
```

## Q27: What is a vtable and how is it implemented?

**A:** A vtable (virtual method table) is a data structure used by compilers to implement virtual dispatch. Each class that declares or inherits virtual functions has a vtable — an array of function pointers, one slot for each virtual function in the class hierarchy. Each object of such a class contains a hidden pointer (vptr) that points to its class's vtable. The compiler sets up the vtable at program startup and populates it with pointers to the correct function implementations.

When a virtual function is called through a base pointer, the generated code first dereferences the object's vptr to find the vtable, then uses the function's index in the vtable to look up the correct function pointer, and finally calls through that pointer. This is a two-step indirection: object → vtable → function. The vtable for a derived class copies entries from the parent's vtable and replaces slots for overridden functions with pointers to the derived class's implementations.

The vtable mechanism has performance implications. Virtual calls are slightly slower than direct calls (one extra indirection), which matters in tight loops or performance-critical code. However, the cost is predictable and usually negligible. The compiler can sometimes devirtualize calls when it knows the concrete type at compile time, eliminating the overhead entirely. Understanding vtables helps explain why C++ has zero-cost abstractions — the vtable overhead only exists when you actually use virtual functions, and it's the minimum cost needed for dynamic dispatch.

**Example:**
```cpp
class Animal {
public:
    virtual void speak() const { std::cout << "...\n"; }
};

class Cat : public Animal {
public:
    void speak() const override { std::cout << "Meow\n"; }
};

// vtable for Cat: [Cat::speak]
// vtable for Animal: [Animal::speak]
```

## Q28: What is the difference between abstract class and interface in terms of design intent?

**A:** The design intent differs fundamentally: an abstract class models an "is-a" partial implementation of a concept, while an interface models a "can-do" capability or contract. An abstract class says "this is a partial implementation of X, and all subclasses are variations of X." An interface says "any class that implements this can perform action Y, regardless of what it is." This distinction guides when to use each.

Use an abstract class when you have a natural hierarchy with shared implementation. A `Vehicle` abstract class makes sense because all vehicles share some behavior (engine management, navigation) while specializing in others (drive, fly). The abstract class holds the shared code and defines the extension points. Use an interface when you need to define a capability that unrelated types can share. `Serializable`, `Comparable`, and `Drawable` are capabilities, not types — a `File`, a `DatabaseRow`, and a `NetworkPacket` might all be `Serializable` despite having nothing else in common.

The design guideline: start with interfaces. If you need shared implementation, introduce an abstract class. Never use an abstract class just to share code when an interface would suffice — it creates an unnecessary inheritance hierarchy. Interfaces can be implemented by any class (including value types), support multiple implementation, and are more flexible for refactoring. Abstract classes are appropriate when the hierarchy is stable and the shared implementation is substantial enough to justify the coupling cost.

**Example:**
```java
// Interface = capability
interface Flyable { void fly(); }

// Abstract class = partial implementation
abstract class Vehicle {
    abstract void start();
    void stop() { System.out.println("Stopping"); }
}
```

## Q29: What is the Template Method pattern?

**A:** The Template Method pattern defines the skeleton of an algorithm in a base class method, deferring certain steps to subclasses. The base class method (the "template method") calls abstract or virtual methods that subclasses override to provide specific implementations. This lets subclasses redefine certain steps of an algorithm without changing its overall structure. It's one of the most commonly used behavioral patterns in framework design.

For example, a data processing pipeline might have a template method `process()` that calls `readData()`, `transform()`, and `writeOutput()` in sequence. The base class implements `process()` with the fixed sequence, while `readData()` and `writeOutput()` are abstract — subclasses provide the specific reading and writing logic. The algorithm's structure is preserved while allowing flexibility in individual steps.

Template Method leverages the Hollywood Principle: "Don't call us, we'll call you." The base class controls the flow and calls subclass methods at the appropriate times. This is extensively used in frameworks — JUnit's `setUp()`/`tearDown()`, servlet lifecycle methods, and React's component lifecycle are all Template Method implementations. The trade-off is that the base class must anticipate which steps subclasses might need to customize, which requires good upfront design. Overly rigid template methods can become difficult to extend without modifying the base class.

**Example:**
```python
class DataMiner:
    def mine(self, path):
        data = self.extract(path)
        parsed = self.parse(data)
        self.analyze(parsed)

    def extract(self, path): raise NotImplementedError
    def parse(self, data): raise NotImplementedError
    def analyze(self, data): raise NotImplementedError
```

## Q30: What is the Command pattern?

**A:** The Command pattern encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue requests, log operations, and support undoable operations. A command object bundles together an action (the "what") and the parameters needed to execute it (the "with what") into a single object that implements a common `execute()` interface. The invoker doesn't need to know what the action does — it just calls `execute()`.

This pattern is essential for implementing undo/redo functionality. Each command stores the state needed to reverse its action. When executed, it modifies the system and records the inverse operation. When undone, it reverses the modification. Text editors use this heavily — typing a character creates an "insert" command, and undoing it creates the corresponding "delete" command. The command history is a stack that can be traversed forward and backward.

Beyond undo, the Command pattern enables request queuing, logging, and transactional behavior. You can serialize commands to disk for crash recovery, broadcast commands to multiple receivers, or compose composite commands that execute multiple operations atomically. GUI frameworks use commands to connect menu items, keyboard shortcuts, and toolbar buttons to the same action. The decoupling between invoker and receiver makes the system more flexible — new commands can be added without modifying existing invoker or receiver code.

**Example:**
```java
interface Command {
    void execute();
    void undo();
}

class LightOnCommand implements Command {
    private Light light;
    public void execute() { light.on(); }
    public void undo() { light.off(); }
}
```

## Q31: What is the State pattern?

**A:** The State pattern allows an object to alter its behavior when its internal state changes. The object appears to change its class at runtime. It encapsulates each state as a separate class and delegates behavior to the current state object. When a state transition occurs, the context object switches its state reference, and subsequent behavior calls are delegated to the new state.

Without the State pattern, state-dependent behavior requires large conditional blocks (switch/if-else chains) that become unwieldy as the number of states grows. Each state adds new branches to every method that checks state. The State pattern eliminates these conditionals by distributing each state's behavior into its own class. A `TCPConnection` might have states `Closed`, `Listening`, `Established`, and `CloseWait`, each implemented as a separate class. The connection delegates `open()`, `close()`, and `acknowledge()` to its current state.

The pattern is particularly useful for UI components, game entities, network protocols, and workflow engines. A game character might have `Idle`, `Walking`, `Running`, and `Attacking` states, each with different behavior for the same input events. The trade-off is an increase in the number of classes, but each class is small, focused, and independently testable. State transitions become explicit methods on the state objects, making the state machine visible and auditable rather than buried in conditional logic.

**Example:**
```python
class State:
    def handle(self, ctx): raise NotImplementedError

class LockedState(State):
    def handle(self, ctx):
        print("Unlocking")
        ctx.state = UnlockedState()

class UnlockedState(State):
    def handle(self, ctx):
        print("Locking")
        ctx.state = LockedState()
```

## Q32: What is the difference between Association, Aggregation, and Composition?

**A:** Association is the broadest relationship — it means two classes are related and can interact, but neither owns the other. A `Teacher` and a `Student` are associated; they interact, but one doesn't own or contain the other. Association can be bidirectional and has varying degrees of multiplicity (one-to-one, one-to-many, many-to-many). It represents a conceptual relationship without ownership.

Aggregation is a "has-a" relationship where the contained object can exist independently of the container. A `Department` has `Professor` objects, but if the department is dissolved, professors still exist. The lifecycle of the contained object is not tied to the container. Aggregation is a weaker form of composition — the contained objects are shared or have independent lifetimes. In UML, aggregation is shown with an open diamond on the container side.

Composition is a stronger "has-a" relationship where the contained object's lifecycle is managed by the container. A `House` has `Room` objects — if the house is destroyed, the rooms cease to exist. The container is responsible for creating and destroying its parts. Composition is shown with a filled diamond in UML. The practical difference between aggregation and composition matters for memory management and lifecycle design. In composition, you ensure the container cleans up its parts. In aggregation, you must account for shared ownership, which requires careful reference management to avoid premature deallocation or memory leaks.

**Example:**
```java
class Engine { }  // part of Car
class Car {
    private Engine engine; // composition: engine dies with Car
    private Owner owner;   // aggregation: owner exists independently
}
```

## Q33: What is the Open-Closed Principle (OCP)?

**A:** The Open-Closed Principle states that software entities should be open for extension but closed for modification. This means you should be able to add new behavior to a system without changing existing, tested code. The principle was formulated by Bertrand Meyer and is the "O" in SOLID. It encourages designing systems where new functionality is added by writing new code rather than modifying existing code.

The key mechanism for achieving OCP is abstraction and polymorphism. If your code depends on an abstraction (interface or abstract class), you can extend behavior by creating new implementations of that abstraction. The existing code that depends on the abstraction doesn't need to change. For example, a report generator that works with a `Formatter` interface can be extended with new formatter types (HTML, PDF, CSV) without modifying the generator itself.

Violating OCP typically manifests as switch statements or if-else chains that check for type and branch accordingly. Adding a new type requires modifying these conditionals, which risks introducing bugs in tested code. The fix is to replace the conditional with polymorphic dispatch — define an interface, implement it for each case, and let the runtime select the correct implementation. This principle is closely related to the Strategy pattern, Factory pattern, and Dependency Inversion Principle, all of which enable systems that grow through addition rather than modification.

**Example:**
```java
interface DiscountStrategy { double apply(double price); }

class NoDiscount implements DiscountStrategy {
    public double apply(double price) { return price; }
}

class SeasonalDiscount implements DiscountStrategy {
    public double apply(double price) { return price * 0.9; }
}
```

## Q34: What is a practical sign that ISP has been violated, and what refactoring fixes it?

**A:** The Interface Segregation Principle states that no client should be forced to depend on methods it does not use. Instead of one large, general-purpose interface, create multiple smaller, focused interfaces that capture specific behaviors. This is the "I" in SOLID and addresses the problem of "fat" interfaces that force implementers to provide empty or irrelevant implementations.

Consider an interface `Worker` with methods `work()`, `eat()`, and `sleep()`. A `Robot` class implementing `Worker` would need to implement `eat()` and `sleep()` even though robots don't do those things. The ISP solution is to split `Worker` into separate interfaces: `Workable`, `Feedable`, and `Sleepable`. A robot implements only `Workable`, while a human implements all three. Each interface is focused on a single concern.

ISP is critical for maintaining clean, maintainable codebases. Large interfaces create coupling between unrelated concepts. When an interface changes, all implementers must change, even if the change is irrelevant to them. By segregating interfaces, changes to one concern don't ripple across unrelated implementations. This principle is especially important in large teams and microservice architectures where different teams own different components. Well-segregated interfaces also make code easier to test — you can create focused mocks that implement only the interface you need for a particular test.

**Example:**
```java
interface Workable { void work(); }
interface Feedable { void eat(); }

class HumanWorker implements Workable, Feedable {
    public void work() { }
    public void eat() { }
}

class Robot implements Workable {
    public void work() { }
}
```

## Q35: Show how DIP changes dependency direction with a concrete high-level and low-level module example.

**A:** The Dependency Inversion Principle states that high-level modules should not depend on low-level modules; both should depend on abstractions. Furthermore, abstractions should not depend on details; details should depend on abstractions. This is the "D" in SOLID and is fundamental to achieving loose coupling in layered architectures.

Without DIP, a business logic layer directly instantiates and calls data access layer classes. This creates tight coupling — changing the database implementation requires changing the business logic. With DIP, the business logic depends on a `Repository` interface (abstraction), and the data access layer implements that interface (detail). The business logic never knows or cares which database is used. This is the foundation of the Repository pattern, Dependency Injection, and Clean Architecture.

In practice, DIP means inverting the typical dependency direction. Instead of high-level code reaching down to low-level code, you define interfaces at the high level and implement them at the low level. Dependency injection containers (like Spring, Dagger, or Guice) automate this inversion by managing the wiring between interfaces and implementations. The result is a system where the core business logic is isolated from infrastructure concerns, making it testable, portable, and resilient to change.

**Example:**
```java
interface UserRepository {
    User findById(int id);
}

class PostgresUserRepo implements UserRepository {
    public User findById(int id) { /* SQL */ return null; }
}

class UserService {
    private UserRepository repo;
    UserService(UserRepository repo) { this.repo = repo; }
}
```

## Q36: How do you identify an SRP violation in practice, and when is a second responsibility justified?

**A:** The Single Responsibility Principle states that a class should have only one reason to change. This is the "S" in SOLID and is often the first principle developers encounter. A class with a single responsibility has one job and does it well. When a class tries to do multiple things, changes to one responsibility risk breaking the other, making the class fragile and hard to maintain.

Robert C. Martin clarified that "reason to change" refers to a stakeholder's motivation. An invoice class that handles both invoice formatting and database persistence has two reasons to change: if the formatting requirements change OR if the persistence mechanism changes. The fix is to separate these into `InvoiceFormatter` (handles presentation) and `InvoiceRepository` (handles storage). Each class now has a single responsibility and a single reason to change.

SRP doesn't mean a class should have only one method — it means a class should have a single, well-defined purpose. A `UserService` can have `createUser()`, `updateProfile()`, and `deleteAccount()` as long as they all serve the single responsibility of user management. The violation occurs when you add `sendEmail()` (notification concern) or `generateReport()` (reporting concern) to the same class. The guideline is: if you can describe what a class does without using the word "and," it probably follows SRP.

**Example:**
```java
class Invoice {
    double amount;
}

class InvoicePrinter {
    void print(Invoice inv) { }
}

class InvoiceSaver {
    void save(Invoice inv) { }
}
```

## Q37: Illustrate shallow versus deep copy with a mutable collection containing nested objects.

**A:** A shallow copy duplicates the top-level object and copies the values of its primitive fields, but for reference fields, it copies the reference (pointer) rather than the object it points to. Both the original and the copy share the same referenced objects. A deep copy duplicates everything — the top-level object AND all objects it references, recursively. The original and copy are completely independent.

Consider a `Team` object that contains a list of `Player` objects. A shallow copy creates a new `Team` but the new team's player list points to the same `Player` objects. Modifying a player through one team affects the other. A deep copy creates new `Player` objects, so each team is fully independent. Deep copies are essential when you need true isolation, such as in undo systems where you need to preserve a snapshot of state.

The practical challenge with deep copies is handling circular references and shared objects. If object A references B and B references A, a naive deep copy can loop forever. Most languages provide mechanisms for deep copying: `clone()` in Java, `copy.deepcopy()` in Python, or custom copy constructors in C++. The trade-off is performance — deep copies are more expensive, especially for large object graphs. In many cases, immutable objects (which cannot be modified after creation) eliminate the need for deep copies entirely, since there's no risk of shared mutation.

**Example:**
```python
import copy

class Address:
    def __init__(self, city):
        self.city = city

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

p1 = Person("A", Address("X"))
p2 = copy.deepcopy(p1)  # independent copy
```

## Q38: What is immutability and why is it valuable in OOP?

**A:** An immutable object is one whose state cannot be modified after creation. All fields are set in the constructor and no setter methods exist. Operations that appear to modify the object actually return a new object with the changed state. Languages like Java (`String`, `LocalDate`), Kotlin (`val`), and Rust enforce or encourage immutability. Immutable objects are inherently thread-safe, easier to reason about, and free from aliasing bugs.

Immutability eliminates an entire class of bugs related to shared mutable state. When objects cannot change, you never have to worry about concurrent modification, unexpected side effects, or stale references. This makes concurrent programming dramatically simpler — immutable objects can be shared freely between threads without synchronization. This is why functional programming emphasizes immutability and why modern Java heavily uses immutable collections and streams.

The trade-off is performance: creating new objects for every "change" generates more garbage and can be slower for large objects. However, this is often offset by reduced synchronization overhead, better cache locality (immutable objects can be shared read-only), and simpler reasoning. Many languages optimize immutable operations internally (e.g., Java's `String` uses a shared internal buffer for substring operations). The practical guideline is: make objects immutable by default, and only add mutability when there's a demonstrated performance need and no safer alternative.

**Example:**
```java
final class Money {
    private final double amount;
    private final String currency;
    Money(double amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }
    Money add(Money other) {
        return new Money(this.amount + other.amount, this.currency);
    }
}
```

## Q39: What is a static method and when should you use one?

**A:** A static method belongs to the class itself rather than to any instance of the class. It can be called without creating an object and cannot access instance variables or instance methods directly. Static methods are resolved at compile time (no virtual dispatch). They are used for utility functions, factory methods, and operations that are conceptually related to the class but don't depend on any specific instance's state.

Use static methods when the operation doesn't need access to instance data. Examples include `Math.sqrt()`, `Collections.sort()`, `Integer.parseInt()`, and validation functions. These operations are pure functions — they take inputs and produce outputs without modifying or depending on object state. Static methods are also used for factory methods that create objects: `LocalDate.now()` or `List.of()`.

However, static methods are often overused and can become a design smell. Because static methods cannot be overridden (they hide, not override), they break polymorphism and make testing difficult (you can't mock a static method in most testing frameworks without special tools). They promote procedural programming within an OOP system. The guideline is: prefer instance methods and dependency injection. Use static methods only for true utilities that have no instance dependencies, or for factory methods that genuinely belong to the class level.

**Example:**
```java
class MathUtils {
    static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}
```

## Q40: What is a final keyword and what does it do in different contexts?

**A:** The `final` keyword has different meanings depending on the context. In Java, `final` on a variable means the reference cannot be reassigned after initialization (the object itself may still be mutable). `final` on a method means it cannot be overridden in subclasses. `final` on a class means it cannot be extended at all (e.g., `String`, `Integer`). In C++, `const` serves similar purposes, and `final` was added in C++11.

When applied to a variable, `final` enforces immutability of the reference. When applied to a method, it prevents polymorphic dispatch — the method is resolved at compile time, which can enable compiler optimizations (devirtualization). When applied to a class, it seals the hierarchy, guaranteeing that the class's behavior cannot be altered by subclassing. This is useful for security-critical classes, immutable types, and performance-sensitive code.

In other languages, `final` has equivalent concepts: `readonly` in C#, `val` in Kotlin/Swift (for variables), `sealed` in C# (for classes), and `struct` in Go (for types that cannot be pointer-aliased). Python has no built-in `final` but type checkers like mypy support `Final` annotations. The practical value of `final` is communicating intent — when a developer sees `final`, they know the design decision was deliberate. It also prevents accidental misuse and enables compiler optimizations.

**Example:**
```java
final class ImmutablePoint {
    final int x;
    final int y;
    ImmutablePoint(int x, int y) { this.x = x; this.y = y; }
}
```

## Q41: What is a composition over inheritance principle?

**A:** The "composition over inheritance" principle states that you should favor assembling objects from smaller, composable parts (composition) over creating class hierarchies (inheritance) to achieve code reuse and flexibility. Instead of inheriting from a base class to gain behavior, you include objects that provide that behavior as fields and delegate to them. This creates "has-a" relationships instead of "is-a" relationships.

The core advantage is flexibility. With inheritance, the relationship is fixed at compile time — you can't change a parent class at runtime. With composition, you can swap components dynamically. For example, instead of `ElectricCar extends Car`, you compose a car with a `PowerTrain` object that can be `Electric`, `Gasoline`, or `Hybrid` — and you can change it at runtime. This is the basis of the Strategy pattern and makes systems much more adaptable.

Composition also avoids the fragile base class problem. In deep inheritance hierarchies, changes in a parent class can break child classes in unexpected ways. With composition, components interact through well-defined interfaces and are insulated from each other's internal changes. Testing is easier because you can mock individual components. The practical guideline: default to composition. Use inheritance only when there is a genuine, stable "is-a" relationship and the hierarchy is shallow (ideally no more than 2-3 levels deep).

**Example:**
```python
class Engine:
    def start(self): return "Engine started"

class Car:
    def __init__(self, engine: Engine):
        self.engine = engine  # composition
    def start(self):
        return self.engine.start()
```

## Q42: What is the difference between an abstract class and a concrete class?

**A:** A concrete class is a class that can be instantiated — you can create objects of its type directly. It provides complete implementations for all its methods and defines all the state and behavior its objects will have. A concrete class is ready to be used as-is. An abstract class cannot be instantiated directly; it serves as a base class that provides partial implementation and must be extended by concrete subclasses.

Abstract classes may contain abstract methods (methods without implementation that subclasses must provide), concrete methods (with implementation), or both. They exist to establish a contract and share common code across related types. For example, `AbstractList` in Java provides the core list algorithm while leaving `get()` and `size()` abstract for `ArrayList` and `LinkedList` to implement differently.

The key distinction is in usage: abstract classes are design-time constructs that define what subclasses must do, while concrete classes are runtime constructs that do the actual work. An abstract class can be thought of as a partially finished blueprint — it defines the structure and shared behavior but leaves gaps for subclasses to fill. This is useful for frameworks where the framework defines the algorithm (template method pattern) and the application developer provides the specifics.

**Example:**
```java
abstract class Animal {
    abstract void speak();
    void breathe() { System.out.println("Breathing"); }
}

class Dog extends Animal {
    void speak() { System.out.println("Woof"); }
}

// new Animal(); // compile error
new Dog(); // works
```

## Q43: What is the difference between a struct and a class?

**A:** In languages that have both (C++, C#), the primary difference is default access: struct members are public by default, while class members are private by default. Structs typically represent simple data containers (value types), while classes represent complex objects with behavior and encapsulation (reference types). In C++, structs and classes are otherwise identical — you can have methods, inheritance, and access specifiers in both.

In C#, the distinction is more significant: structs are value types (stored on the stack, copied by value), while classes are reference types (stored on the heap, copied by reference). A `Point` struct is more efficient for small, simple values because it avoids heap allocation and garbage collection overhead. A `Person` class is more appropriate for complex objects with identity, mutable state, and inheritance.

The design guideline is: use structs for small, immutable value objects that represent a single value or a simple collection of values (coordinates, dates, monetary amounts). Use classes for objects with complex behavior, identity, inheritance, or that need to be shared by reference. In languages without explicit struct/class distinction (Python, Ruby), you achieve the same effect by designing classes to be either value-like (immutable, small) or reference-like (complex, identity-based).

**Example:**
```cpp
struct Point { double x, y; };  // value type, public by default

class Circle {
    double radius;
public:
    Circle(double r) : radius(r) {}
};
```

## Q44: What is a companion object (or static class member)?

**A:** A companion object (in Kotlin/Scala) or static class member (in Java/C++) is a mechanism for attaching behavior and state to a class itself rather than to instances. In Java, `static` fields and methods belong to the class. In Kotlin, a `companion object` is a singleton object associated with the class that can hold factory methods, constants, and utility functions. The class name can be used to access companion object members directly.

Companion objects are used for factory methods, constants, and utility functions that are logically related to the class but don't need instance state. For example, `Integer.valueOf()` is a static factory method, `Math.PI` is a constant, and `Collections.unmodifiableList()` is a utility. In Kotlin, companion objects can implement interfaces, which gives them more flexibility than Java's static methods.

The practical distinction is that companion objects/static members are not polymorphic — they belong to the class, not the instance. You can't override a static method in the polymorphic sense (you can hide it, but a base reference will call the base version). They are resolved at compile time. This makes them unsuitable for behavior that should vary by subtype. Use instance methods for polymorphic behavior; use static/companion members for class-level utilities, constants, and factories.

**Example:**
```kotlin
class User private constructor(val name: String) {
    companion object {
        fun create(name: String) = User(name)
    }
}
val user = User.create("Alice")
```

## Q45: What is an inner class and when should you use one?

**A:** An inner class is a class defined within another class. There are several varieties: member inner class (associated with an instance of the outer class), static nested class (associated with the outer class itself), local class (defined within a method), and anonymous class (defined inline without a name). Inner classes can access the private members of their enclosing class, which creates a tight relationship between them.

Use inner classes when a class is only useful in the context of its outer class. For example, a `LinkedList` might have a `Node` inner class — `Node` is meaningless outside the context of `LinkedList` and needs access to `LinkedList`'s private fields. Iterator implementations are commonly inner classes because they need access to the collection's internal structure. This improves encapsulation by keeping implementation details hidden within the outer class.

However, inner classes create coupling between the inner and outer class. A member inner class holds an implicit reference to its outer instance, which can cause memory leaks if the inner class instance outlives the outer. Static nested classes avoid this by not holding the outer reference. In modern Java, the recommendation is to prefer static nested classes over member inner classes unless you specifically need access to the outer instance. Anonymous classes were common before Java 8 but have been largely replaced by lambda expressions for single-method interfaces.

**Example:**
```java
class Stack<T> {
    private static class Node<T> {
        T data;
        Node<T> next;
        Node(T data, Node<T> next) { this.data = data; this.next = next; }
    }
    private Node<T> top;
}
```

## Q46: What is the difference between runtime polymorphism and compile-time polymorphism?

**A:** Compile-time polymorphism (static polymorphism) is resolved by the compiler based on the types of arguments at compile time. Method overloading is the primary form — multiple methods with the same name but different parameter lists. The compiler determines which version to call based on the argument types. Template/generic programming is another form — the compiler generates specialized code for each type used. This has zero runtime overhead because the decision is made before the program runs.

Runtime polymorphism (dynamic polymorphism) is resolved at runtime based on the actual type of the object. Virtual method dispatch is the primary mechanism — a call on a base reference is dispatched to the correct derived implementation by looking up the vtable at runtime. This adds a small overhead (one indirection) but enables powerful patterns like Strategy, Observer, and any framework that relies on interfaces and dependency injection.

The trade-off is performance vs. flexibility. Compile-time polymorphism is faster (no indirection) but less flexible — you can't change behavior at runtime. Runtime polymorphism is slightly slower but enables open-closed designs where new types can be added without modifying existing code. Modern compilers can often devirtualize virtual calls when the concrete type is known at compile time, giving you the best of both worlds. The guideline: use runtime polymorphism when you need extensibility and flexibility; use compile-time polymorphism when you need maximum performance and the types are known.

**Example:**
```cpp
// Compile-time: overloading
void print(int x) { }
void print(double x) { }

// Runtime: virtual dispatch
class Base { virtual void identify() = 0; };
class Derived : public Base { void identify() override { } };
```

## Q47: What is a pure virtual function (or abstract method)?

**A:** A pure virtual function is a virtual function that has no implementation in the base class and must be overridden in derived classes. In C++, it's declared with `= 0` syntax. In Java, it's declared with the `abstract` keyword and no body. In Python, it's declared using `@abstractmethod` from the `abc` module. A class containing at least one pure virtual function becomes an abstract class and cannot be instantiated.

Pure virtual functions define a mandatory contract: any non-abstract subclass MUST provide an implementation. This is stronger than a regular virtual function, which provides a default implementation that can optionally be overridden. Pure virtual functions are used when the base class concept is incomplete — there's no sensible default behavior. For example, a `Shape` class might declare `area()` as pure virtual because there's no meaningful area for an abstract shape.

Pure virtual functions are essential for interface design in C++. When a class has only pure virtual functions and no data, it functions as an interface (like Java's `interface` keyword). This is the "interface class" idiom. The practical value is compile-time enforcement of the contract — if you forget to implement a pure virtual function, the compiler catches it immediately. This is more robust than runtime errors or documentation alone. Pure virtual destructors are special: they must have an implementation (for proper cleanup of derived objects), even though the class is otherwise abstract.

**Example:**
```cpp
class Drawable {
public:
    virtual void draw() const = 0;  // pure virtual
    virtual ~Drawable() {}           // virtual destructor needed
};

class Circle : public Drawable {
public:
    void draw() const override { std::cout << "Circle\n"; }
};
```

## Q48: What is a covariance and contravariance in type systems?

**A:** Covariance means that the subtype relationship is preserved: if `Dog` is a subtype of `Animal`, then `Collection<Dog>` is a subtype of `Collection<Animal>`. Contravariance means the subtype relationship is reversed: if `Dog` is a subtype of `Animal`, then `Handler<Animal>` is a subtype of `Handler<Dog>`. These concepts define how generic types relate to each other when their type parameters are in a subtype relationship.

Covariance is intuitive: a collection of dogs can be treated as a collection of animals because every dog is an animal. In Java, `List<Dog>` can be assigned to `List<Animal>` using the `? extends` wildcard: `List<? extends Animal>`. Contravariance is less intuitive but equally important: a handler that can handle any animal can certainly handle a dog, so `Handler<Animal>` can be used where `Handler<Dog>` is expected. Java uses `? super` for this: `Consumer<? super Dog>`.

Understanding variance is critical for designing type-safe generic APIs. The Get-Heuristic: if you only **get** values from a structure, use covariance (`? extends`). If you only **put** values into a structure, use contravariance (`? super`). If you do both, use invariance (no wildcard). This is known as PECS (Producer Extends, Consumer Super). Getting variance wrong leads to type safety violations or unnecessarily restrictive APIs. Languages like Kotlin and Scala have explicit `out` (covariant) and `in` (contravariant) annotations to make variance explicit.

**Example:**
```java
// Covariance: Producer
List<? extends Animal> animals = List.of(new Dog());

// Contravariance: Consumer
Consumer<Animal> animalConsumer = a -> {};
Consumer<? super Dog> dogConsumer = animalConsumer;
```

## Q49: What is a type parameter constraint (generics bounded type)?

**A:** Generic type constraints restrict what types can be used as type arguments. Instead of accepting any type (`T`), you constrain `T` to implement a specific interface or extend a specific class. For example, `T extends Comparable<T>` means `T` must implement `Comparable`. Constraints enable the generic code to call methods on the type parameter, knowing those methods exist. Without constraints, generic code can only use `Object` methods.

In Java, bounds are written `<T extends Number & Comparable<T>>`. In C#, `<T where T : IComparable<T>>`. In Kotlin, `<T : Comparable<T>>`. Constraints can include multiple interfaces (Java uses `&`), but only one class (since single inheritance applies). The constraint ensures type safety: the compiler verifies that the type argument satisfies the bound, and the generic code can safely use the constrained methods.

Constraints are essential for writing useful generic algorithms. A generic `sort` function needs to compare elements, so it constrains the type to `Comparable`. A generic `serialize` function might constrain to `Serializable`. Without constraints, generic code is limited to identity checks and `Object` methods, making it nearly useless for anything beyond simple containers. Constraints also serve as documentation — they communicate to callers what types are valid and what operations the generic code performs on those types.

**Example:**
```java
<T extends Comparable<T>> T max(List<T> list) {
    T result = list.get(0);
    for (T item : list) {
        if (item.compareTo(result) > 0) result = item;
    }
    return result;
}
```

## Q50: What is the difference between an immutable and a readonly object?

**A:** An immutable object cannot be modified after creation — all operations produce new objects rather than modifying the original. The object's state is fixed for its entire lifetime. A readonly object may have restrictions on modification but the distinction depends on the language. In Java, `final` prevents reassignment of references but doesn't prevent mutation of the referenced object. Truly immutable objects require final fields AND no methods that modify state.

The practical difference matters for concurrency and reasoning. Immutable objects are safe to share between threads without synchronization because they never change. Readonly references (like `const` in C++ or `final` in Java) prevent reassignment but don't prevent mutation of the referenced object. For true immutability, every field must be final/readonly, the class must be final/sealed to prevent subclass mutation, and no methods can modify state.

In modern Java, the trend is toward immutability: `String`, `LocalDate`, `Optional`, and unmodifiable collections are all immutable. Kotlin's `data class` with `val` properties creates immutable value objects. The pattern is: design for immutability by default, return new objects from operations, and only add mutability when performance profiling demands it. For complex object graphs, deep immutability (where all referenced objects are also immutable) is necessary for the thread-safety guarantee to hold.

**Example:**
```kotlin
data class User(val name: String, val age: Int)
// All properties are val (immutable)
// copy() returns a new instance
val user2 = user.copy(age = 30)
```

## Q51: Describe the fragile base class problem and three ways to reduce it while evolving a library.

**A:** The fragile base class problem occurs when changes to a base class inadvertently break derived classes. Because inheritance creates tight coupling between parent and child, modifications to the parent class's implementation — even if the public API remains unchanged — can alter behavior that child classes depend on. For example, adding a method to a parent class might conflict with a same-named method in a child class, or changing the order of operations in a parent method might violate assumptions made by child overrides.

This problem arises because inheritance exposes implementation details, not just the public API. Child classes often depend on the parent's internal method call order, field initialization sequence, or the side effects of parent methods. When the parent changes these internals, child classes break silently — the compiler doesn't catch these issues because the public contract hasn't changed. This makes inheritance hierarchies risky in large, evolving codebases maintained by different teams.

The fragile base class problem is a primary reason why composition is preferred over inheritance. With composition, the components interact through explicit interfaces, and changes to a component's internals don't affect other components. If you must use inheritance, keep hierarchies shallow (1-2 levels), document implementation dependencies explicitly, and avoid calling overridable methods from constructors or initializers (a related anti-pattern). The Liskov Substitution Principle, when strictly followed, mitigates some of this risk.

**Example:**
```java
class Base {
    void setup() { /* initialize */ }
    void execute() { setup(); /* do work */ }
}

class Child extends Base {
    @Override void setup() { /* depends on Base.execute() not calling setup first */ }

    // If Base.execute() changes to call setup(), Child breaks
}
```

## Q52: What is the gorilla/banana problem in OOP?

**A:** The gorilla/banana problem, coined by Joe Armstrong (creator of Erlang), describes the difficulty of getting just a small piece of code (the banana) from a library but ending up with the entire gorilla (the whole object hierarchy) and the entire jungle (all its dependencies). When you try to reuse a single class from an inheritance hierarchy, you often pull in the entire parent chain, all sibling classes, and their transitive dependencies.

This problem is a direct consequence of deep inheritance hierarchies. If you want the `Banana` class's behavior but it extends `Fruit` which extends `Food` which requires `NutritionDatabase`, you get everything. Even worse, the banana might call methods on the gorilla that you don't need but can't avoid. This makes inheritance-based code reuse fragile and heavyweight, violating the principle of minimal dependencies.

The solution is composition and small, focused modules. Instead of inheriting behavior, compose objects from small, independent components that interact through minimal interfaces. A banana that is a standalone object with no parent hierarchy can be taken anywhere. This is the philosophy behind modern package management (npm, pip, cargo) — small, composable packages rather than monolithic frameworks. The Interface Segregation Principle directly addresses this by ensuring interfaces are small and focused, reducing the "gorilla" you get when you depend on an abstraction.

**Example:**
```java
// You want just this:
class Banana { void peel() { } }

// But Banana extends Fruit, which extends Food,
// which requires Database, Logger, Config...
// Now you have the gorilla and the jungle.
```

## Q53: What is the expression problem and how does it relate to OOP?

**A:** The expression problem is a fundamental challenge in programming language design: given a data type with multiple variants and multiple operations, how do you add new variants (types) and new operations without recompiling existing code? In OOP, adding new operations (methods) is easy — create a new class that implements the interface. But adding new variants (types) requires modifying the interface and all existing implementations. In functional programming, it's the reverse: adding new variants (pattern match cases) is easy, but adding new operations requires modifying all existing pattern matches.

OOP excels at adding new types: you create a new class implementing the existing interface, and existing code works without modification (Open-Closed Principle for types). But adding a new operation (like `prettyPrint()`) to an existing interface forces ALL implementers to add it. Functional programming with algebraic data types excels at adding new operations (just write a new function that pattern-matches on all cases) but adding a new variant (like a new AST node) requires updating every function that pattern-matches.

Languages like Scala, OCaml, and Rust offer solutions through traits, object algebras, or visitor patterns. The practical implication is that OOP designs should anticipate which axis of change is more likely. If new types will be added frequently, design around interfaces (OOP excels). If new operations will be added frequently, consider a functional approach or use the Visitor pattern. Understanding this trade-off helps you choose the right paradigm for the problem.

**Example:**
```python
# Adding new operation requires modifying all types (OOP weakness)
class Shape:
    def area(self): raise NotImplementedError
    def perimeter(self): raise NotImplementedError  # new op = modify all

class Circle(Shape):
    def area(self): return 3.14 * self.r ** 2
    def perimeter(self): return 2 * 3.14 * self.r  # must add
```

## Q54: What is the null object pattern?

**A:** The Null Object pattern provides a default, do-nothing implementation of an interface that represents "no object" or "absence." Instead of returning `null` and forcing callers to check for null everywhere, you return a Null Object that implements the same interface with benign behavior. For example, a `NullLogger` implements `Logger` by doing nothing on every log call. This eliminates null checks and makes code cleaner and safer.

The pattern addresses the "billion-dollar mistake" of null references. Code that receives an object conforming to an interface can call methods on it without null checks — if it's a Null Object, the methods simply do nothing. A `NullUser` might have a name of "Anonymous" and always return false for `isAdmin()`. A `NullPrinter` silently discards print requests. This makes the code path uniform — you don't need separate logic for "user exists" and "user doesn't exist."

The Null Object pattern is particularly valuable in systems with optional dependencies or configurable behavior. Instead of complex conditional logic to handle missing objects, you inject a Null Object as the default. Combined with dependency injection, this pattern eliminates most null-related bugs. The trade-off is that Null Objects can hide bugs — if a Null Object is injected when a real object should be, the system silently fails. Use them when "doing nothing" is a valid, intentional behavior, not as a band-aid for missing error handling.

**Example:**
```java
interface Logger { void log(String msg); }

class ConsoleLogger implements Logger {
    public void log(String msg) { System.out.println(msg); }
}

class NullLogger implements Logger {
    public void log(String msg) { /* intentionally empty */ }
}
```

## Q55: What is the service locator pattern and how does it differ from dependency injection?

**A:** The Service Locator pattern provides a centralized registry where objects can look up their dependencies by name or type. Instead of receiving dependencies through constructors or methods, objects query the service locator to find them. This decouples objects from knowing how to create their dependencies, but couples them to the locator itself. It was common in early Java frameworks (JNDI) and is still used in some game engines and plugin systems.

Dependency Injection (DI) is the alternative where dependencies are provided to an object by an external entity (a DI container or the caller) rather than being looked up. The object declares what it needs (through constructor parameters, setters, or fields), and the framework or caller provides it. The object never knows where the dependency came from — it just uses it. This is the preferred approach in modern systems because it makes dependencies explicit, testable, and avoids the hidden coupling of service locators.

The key difference is explicitness and testability. With DI, dependencies are visible in the constructor signature — you can see exactly what a class needs. With a service locator, dependencies are hidden inside method bodies, making the class's requirements opaque. DI also makes testing trivial — you can pass mock objects directly. With service locators, you must configure the locator with mocks before running tests. The community consensus has shifted strongly toward DI as the superior pattern for most applications.

**Example:**
```java
// Service Locator (anti-pattern)
class OrderService {
    void process() {
        DB db = ServiceLocator.get(DB.class); // hidden dependency
    }
}

// Dependency Injection (preferred)
class OrderService {
    private final DB db;
    OrderService(DB db) { this.db = db; } // explicit dependency
}
```

## Q56: What is the visitor pattern and when would you use it?

**A:** The Visitor pattern separates an algorithm from the object structure it operates on. It lets you define new operations on a set of objects without modifying their classes. You create a visitor class that implements a visit method for each concrete type in the hierarchy. When the visitor visits an object, the object calls the appropriate visit method on the visitor, dispatching based on the object's actual type. This effectively simulates double dispatch.

The Visitor pattern is useful when you have a stable class hierarchy (rarely add new types) but frequently add new operations. For example, an AST (Abstract Syntax Tree) in a compiler has node types that rarely change (BinaryOp, Literal, Variable) but operations are added constantly (type checking, code generation, optimization, pretty-printing). Without Visitor, each new operation requires modifying every node class. With Visitor, you create a new visitor class without touching the existing nodes.

The trade-off is that adding new types to the hierarchy requires updating ALL visitors — the reverse of the usual OOP flexibility. This makes Visitor suitable only when the type hierarchy is genuinely stable. The pattern is also complex to implement correctly, requiring accept/visit method pairs and often relying on double dispatch or type checking. In practice, Visitor is common in compilers, interpreters, document processing, and any system with a fixed set of types and evolving operations. Modern alternatives include sealed classes with pattern matching (C#, Kotlin, Rust) which achieve similar goals more elegantly.

**Example:**
```java
interface Visitor {
    void visit(Circle c);
    void visit(Square s);
}

class AreaVisitor implements Visitor {
    public void visit(Circle c) { /* compute circle area */ }
    public void visit(Square s) { /* compute square area */ }
}

interface Shape { void accept(Visitor v); }
```

## Q57: What is the double dispatch pattern?

**A:** Double dispatch is a technique where the method invoked depends on the types of both the receiver and the argument. In single dispatch (virtual methods), only the receiver's type determines which method is called. In double dispatch, both the receiver's dynamic type and the argument's dynamic type influence the method selection. This is necessary when operations depend on the interaction between two different object types.

The classic example is collision detection in a game: a `Circle` colliding with a `Square` should behave differently from a `Circle` colliding with a `Circle`. With single dispatch, you can handle one receiver type polymorphically, but not both. Double dispatch solves this by having the receiver's `collide()` method call the argument's `collide()` method with itself, and the argument then dispatches based on both types. This is typically implemented using the Visitor pattern or method overloading.

In practice, double dispatch is rare but essential in specific domains. Collision detection, document processing (applying operations between different element types), and arithmetic expression evaluation (type-dependent operations between different value types) all benefit. The alternative approaches include type checking (if/instanceof chains — ugly and violates OCP), the Visitor pattern (standard but verbose), or sealed classes with pattern matching (modern and clean). Understanding double dispatch helps you recognize when single dispatch is insufficient and choose the right solution.

**Example:**
```java
interface Shape {
    void collideWith(Circle c);
    void collideWith(Square s);
}

class Circle implements Shape {
    public void collideWith(Circle c) { /* circle-circle */ }
    public void collideWith(Square s) { /* circle-square */ }
}
```

## Q58: What is an object pool pattern and when is it appropriate?

**A:** The Object Pool pattern pre-instantiates a set of expensive objects and reuses them instead of creating and destroying them on demand. When a client needs an object, it borrows one from the pool; when done, it returns it. This amortizes the cost of object creation and garbage collection over many uses. The pool manages the lifecycle: creation, borrowing, returning, and destruction.

Object pools are appropriate when object creation is expensive (database connections, network sockets, threads, large buffers) and the number of concurrent users is bounded. Database connection pools (HikariCP, Apache DBCP) are the most common example — opening a TCP connection and authenticating is expensive, so connections are pooled and reused. Thread pools (ExecutorService in Java, multiprocessing.Pool in Python) follow the same pattern — thread creation and context switching are costly.

The pool must handle several concerns: thread-safe access (multiple clients borrowing/returning concurrently), idle object cleanup (destroying objects that haven't been used for a while), pool sizing (too few objects causes contention, too many wastes resources), and object validation (ensuring returned objects are still healthy). Anti-patterns include not returning objects (pool exhaustion), returning dirty objects (state leakage), and using pools for cheap objects (where creation cost is less than pool management overhead).

**Example:**
```python
from queue import Queue

class ObjectPool:
    def __init__(self, factory, size=5):
        self.pool = Queue()
        for _ in range(size):
            self.pool.put(factory())

    def borrow(self):
        return self.pool.get()

    def release(self, obj):
        self.pool.put(obj)
```

## Q59: What is the flyweight pattern and how does it reduce memory?

**A:** The Flyweight pattern minimizes memory usage by sharing as much data as possible between similar objects. It separates object state into intrinsic state (shared, immutable, stored in the flyweight) and extrinsic state (unique, context-specific, passed in by the client). Instead of creating a separate object for each unique entity, you reuse a single flyweight object for all entities that share the same intrinsic state.

The classic example is text rendering: a document with 100,000 characters doesn't need 100,000 character objects. It needs 26 flyweight character objects (one per letter) that share the glyph data (shape, font metrics). Each character in the document stores only its position and formatting (extrinsic state) and references the appropriate character flyweight. This reduces memory from O(n) to O(1) for the character objects themselves.

Flyweight is used extensively in systems that create large numbers of similar objects. String interning (reusing identical strings), connection pooling (sharing connection infrastructure), and game engines (reusing particle effects, enemy templates) are all applications. The trade-off is increased complexity — you need a factory that manages the flyweight cache, and you must separate intrinsic from extrinsic state, which isn't always natural. The pattern is most effective when the number of distinct intrinsic states is small relative to the total number of objects.

**Example:**
```python
class TreeType:
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture

class Tree:
    def __init__(self, x, y, type_ref):
        self.x = x
        self.y = y
        self.type_ref = type_ref  # shared flyweight
```

## Q60: What is a proxy pattern and what types exist?

**A:** The Proxy pattern provides a surrogate or placeholder for another object to control access to it. The proxy implements the same interface as the real object and delegates calls to it, adding behavior before or after delegation. The client interacts with the proxy as if it were the real object. This indirection enables control over object creation, access, logging, caching, and remote communication.

There are several types of proxies. Virtual proxy delays object creation until it's actually needed (lazy loading) — useful for expensive objects like large images or database connections. Remote proxy represents an object in a different address space (network) — it handles serialization and network communication transparently (RMI, gRPC stubs). Protection proxy controls access based on permissions — it checks authorization before delegating. Caching proxy stores results of expensive operations and returns cached results for repeated calls.

The Proxy pattern is foundational in many systems. ORMs use virtual proxies for lazy loading (Hibernate, JPA). RPC frameworks use remote proxies (gRPC, Dubbo). Security frameworks use protection proxies (Spring Security). Logging and monitoring use logging proxies. The difference between Proxy and Decorator is intent: Proxy controls access to an object (access control, lazy init, remote communication), while Decorator adds behavior to an object (additional functionality). Both wrap objects, but for different purposes.

**Example:**
```java
interface Image { void display(); }

class RealImage implements Image {
    public void display() { /* expensive render */ }
}

class ProxyImage implements Image {
    private RealImage real;
    public void display() {
        if (real == null) real = new RealImage(); // lazy
        real.display();
    }
}
```

## Q61: What is the mediator pattern and when should you use it?

**A:** The Mediator pattern defines an object that encapsulates how a set of objects interact. Instead of objects communicating directly with each other (creating tight coupling), they communicate through the mediator. The mediator handles the coordination logic, reducing the dependencies between communicating objects. This promotes loose coupling and makes the interaction logic centralized and easier to modify.

Use the Mediator pattern when you have a web of objects that communicate with each other in complex, tangled ways. UI dialog boxes are a classic example: a form with text fields, buttons, dropdowns, and checkboxes where the state of one control affects others. Without a mediator, each control would need references to every other control it interacts with. With a mediator, controls only know about the mediator, and the mediator coordinates their interactions.

The Mediator pattern is the backbone of UI frameworks (event brokers), chat systems (chat rooms), and air traffic control (the tower mediates between aircraft). The trade-off is that the mediator can become a "god object" — a monolithic class that knows too much about every component. This happens when the mediator accumulates too much coordination logic. The solution is to keep mediator logic focused on routing and coordination, not business logic. MediatR (used in .NET Clean Architecture) is a popular implementation that uses request/response messages to decouple handlers.

**Example:**
```python
class ChatRoom:
    def __init__(self):
        self.users = []
    def send(self, msg, user):
        for u in self.users:
            if u != user:
                u.receive(msg)
    def add(self, user):
        self.users.append(user)
```

## Q62: What is the chain of responsibility pattern?

**A:** The Chain of Responsibility pattern passes a request along a chain of handlers. Each handler decides either to process the request or to pass it to the next handler in the chain. This decouples the sender of a request from its receivers, giving multiple objects a chance to handle the request without the sender needing to know which object will handle it. Handlers are linked in a chain, and the request travels until one handler processes it (or reaches the end).

This pattern is used extensively in middleware and filter chains. Web frameworks (Express, Spring, Django) use it for HTTP middleware — each middleware can handle the request, modify it, or pass it along. Logging, authentication, rate limiting, CORS, and compression are typically implemented as chain of responsibility handlers. Each handler does one thing and passes the request to the next. The order of handlers matters and is typically configurable.

The pattern's strength is flexibility — handlers can be added, removed, or reordered without changing the sender or other handlers. The weakness is that if no handler processes the request, it can silently fall through, leading to bugs. Also, debugging can be difficult because the processing path is dynamic and depends on the chain configuration. The pattern is similar to the Decorator pattern but differs in that Decorator adds behavior and always processes, while Chain of Responsibility may skip processing.

**Example:**
```java
abstract class Handler {
    protected Handler next;
    public void setNext(Handler h) { this.next = h; }
    public void handle(int level) {
        if (next != null) next.handle(level);
    }
}

class DebugHandler extends Handler {
    public void handle(int level) {
        if (level <= 1) System.out.println("Debug");
        else super.handle(level);
    }
}
```

## Q63: What is an object graph and why does it matter?

**A:** An object graph is the network of objects in memory at runtime, connected through references (field assignments, method parameters, return values). Every object is a node, and every reference is an edge. Understanding the object graph is critical for memory management, serialization, debugging, and performance optimization. The shape of the graph — its depth, width, and connectivity patterns — directly impacts system behavior.

Object graph complexity affects serialization (JSON, XML, binary formats must traverse and encode the entire graph), deep copying (must duplicate the entire reachable graph), garbage collection (collectors traverse the graph to identify live objects), and debugging (understanding how objects are connected helps diagnose issues). Circular references (A → B → A) are particularly tricky — naive serialization or copying can infinite-loop without cycle detection.

In distributed systems, object graphs must be flattened for network transmission (serialization), which is where formats like Protocol Buffers, Avro, and Thrift come in. The impedance mismatch between in-memory object graphs and serialized representations is a fundamental challenge in ORM (Object-Relational Mapping) — relational tables don't naturally map to object graphs with inheritance, collections, and bidirectional references. Understanding your object graph helps you design better serialization strategies, optimize memory layout, and avoid common pitfalls like unintentional object retention and memory leaks.

**Example:**
```python
class Node:
    def __init__(self, val):
        self.val = val
        self.children = []

root = Node(1)
root.children.append(Node(2))
root.children.append(Node(3))
# Object graph: root → [node2, node3]
```

## Q64: What is the difference between a value object and an entity?

**A:** In Domain-Driven Design (DDD), an entity is an object defined by its identity rather than its attributes — two entities with identical attributes are still different objects if they have different identities. A value object is defined by its attributes — two value objects with the same attributes are considered equal. Entities have lifecycle (they change state over time while retaining identity); value objects are typically immutable and replaced rather than modified.

Examples: A `User` is an entity — it has an ID, and even if you change its name, it's still the same user. An `Address` is a value object — two addresses with the same street, city, and zip are functionally identical, and there's no reason to distinguish them by identity. A `Money` object (amount + currency) is a value object. A `BankAccount` is an entity with a unique account number.

This distinction matters for design decisions. Entities require identity management (IDs, equality by ID), are typically mutable, and need persistence with identity tracking. Value objects can be compared by value, are immutable, and can be freely shared and copied. In Java, value objects are often implemented as classes with `equals()` and `hashCode()` based on attributes (or records in Java 14+). In DDD, aggregates are clusters of entities and value objects with a root entity that controls access. Understanding entity vs. value object helps you model domains accurately and avoid common bugs like comparing entities by reference instead of by ID.

**Example:**
```java
record Money(double amount, String currency) {} // value object

class BankAccount {
    private String id;  // entity: identity matters
    private Money balance; // value object: amount+currency
}
```

## Q65: What is aggregate root in Domain-Driven Design?

**A:** An aggregate root is the entry point to an aggregate — a cluster of associated entities and value objects that are treated as a single unit for data changes. The aggregate root is the only object in the aggregate that external objects can hold references to. All modifications to objects within the aggregate must go through the root. This enforces consistency boundaries and ensures that business invariants are maintained within the aggregate.

For example, an `Order` aggregate might contain the `Order` (root), `OrderItem` entities, and `Address` value objects. External code can only reference the `Order` object. To add an item, you call `order.addItem()` — the root validates the operation, adds the item to its internal collection, and ensures invariants (like total price consistency) are maintained. External code never directly modifies `OrderItem` objects.

Aggregate roots serve several purposes: they define transaction boundaries (changes to an aggregate are committed atomically), they simplify the object graph (external references point only to roots, not to internal objects), and they enforce business rules (all invariants within an aggregate are checked by the root before committing). The guideline for aggregate design is: keep aggregates small (minimize the number of entities), reference other aggregates by identity (not by object reference), and use eventual consistency between aggregates rather than trying to maintain strong consistency across aggregate boundaries.

**Example:**
```python
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []

    def addItem(self, product, qty):
        if qty <= 0: raise ValueError("Invalid qty")
        self.items.append(OrderItem(product, qty))

class OrderItem:
    def __init__(self, product, qty):
        self.product = product
        self.qty = qty
```

## Q66: What is the difference between equal and equivalent objects?

**A:** Equal objects have the same identity — they are literally the same object in memory (same reference). Equivalent objects have the same value or state but are different objects in memory. Two `String` objects created with `"hello"` might be equivalent (same characters) but not equal (different memory addresses), or they might be both equal and equivalent (if string interning is used).

Languages provide mechanisms to test equivalence. In Java, `==` tests reference equality (equal), while `equals()` tests value equivalence. In Python, `is` tests identity (equal), while `==` tests equivalence. Implementing `equals()` correctly requires implementing `hashCode()` consistently — if two objects are equivalent, they must have the same hash code. This is essential for correct behavior in hash-based collections (HashMap, HashSet).

The distinction matters for collections and caching. A `HashMap` uses hash codes to bucket keys and `equals()` to find the exact key. If you override `equals()` but not `hashCode()`, two equivalent objects might end up in different buckets, breaking the map. The contract is: if `a.equals(b)` then `a.hashCode() == b.hashCode()`. When implementing equality, decide whether you need shallow equality (compare fields directly) or deep equality (recursively compare referenced objects). For entities, equality is typically by ID. For value objects, equality is by all attributes.

**Example:**
```java
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Point)) return false;
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }
    public int hashCode() { return 31 * x + y; }
}
```

## Q67: What is the difference between shallow and deep equality?

**A:** Shallow equality compares only the top-level fields of an object. Two objects are shallowly equal if their directly held fields have the same values (or are the same references). Deep equality recursively compares all fields, including those of referenced objects. If an object contains references to other objects, deep equality follows those references and compares the nested objects' fields too.

Consider a `Person` object with a `Name` field (which has `first` and `last`). Shallow equality might compare the `Name` reference — two `Person` objects with different `Name` instances but the same first and last names would be considered not equal. Deep equality compares `first` and `last` within the `Name`, so both persons would be equal. Deep equality is typically what you want for value objects, but it's more expensive and must handle circular references carefully.

Implementing deep equality correctly is notoriously difficult. You must handle null checks, type checks, circular references (to avoid infinite recursion), and collections (comparing element by element). Most languages provide utilities: `Objects.deepEquals()` in Java, `deepdiff` in Python. For performance-critical code, shallow equality with carefully chosen fields is often sufficient. The guideline: for value objects, implement deep equality. For entities, equality is by ID (shallow). For collections, compare elements using the element's own equality method.

**Example:**
```python
class Address:
    def __init__(self, street, city):
        self.street = street
        self.city = city
    def __eq__(self, other):
        return self.street == other.street and self.city == other.city
```

## Q68: What is the composite pattern?

**A:** The Composite pattern lets you treat individual objects and compositions of objects uniformly. It defines a tree structure where both leaf nodes (individual objects) and composite nodes (containers of other objects) implement the same interface. A client can call operations on a composite without knowing whether it's dealing with a leaf or a branch — the operation is applied recursively.

File systems are the canonical example: a `FileSystemEntry` interface with `getName()` and `getSize()` methods. A `File` (leaf) returns its own size. A `Directory` (composite) contains other `FileSystemEntry` objects and returns the total size by summing its children's sizes. The client calls `getSize()` without knowing if it's a file or directory. This uniformity eliminates type-checking and casting.

The Composite pattern is used in GUI frameworks (widgets containing widgets), organizational structures (employees containing teams), and document models (paragraphs containing words and images). The key design decision is whether the composite should support child management methods (add, remove) in the common interface. The GoF recommends not adding child management to the leaf interface (safe composite pattern), but some implementations include it for convenience (transparency composite pattern). The trade-off is between type safety and API simplicity.

**Example:**
```java
interface Component { int getValue(); }

class Leaf implements Component {
    private int value;
    Leaf(int v) { this.value = v; }
    public int getValue() { return value; }
}

class Composite implements Component {
    private List<Component> children = new ArrayList<>();
    void add(Component c) { children.add(c); }
    public int getValue() {
        return children.stream().mapToInt(Component::getValue).sum();
    }
}
```

## Q69: What is the bridge pattern?

**A:** The Bridge pattern decouples an abstraction from its implementation so that the two can vary independently. It uses composition to separate the high-level abstraction (what you do) from the low-level implementation (how you do it). The abstraction holds a reference to the implementation, and both can be extended independently without affecting each other. This addresses the problem of Cartesian product complexity in class hierarchies.

Without Bridge, if you have `Shape` (Circle, Square) and `Color` (Red, Blue), you might create `RedCircle`, `BlueCircle`, `RedSquare`, `BlueSquare` — four classes for two dimensions of variation. With Bridge, you have a `Shape` abstraction that holds a `Color` implementation reference. `Circle` and `Square` are one hierarchy; `Red` and `Blue` are another. Adding a new shape doesn't require new color classes, and adding a new color doesn't require new shape classes. The total is four classes, but extensibility is linear, not exponential.

The Bridge pattern is essential when both the abstraction and implementation are expected to change independently. Database drivers (abstraction: connection API, implementation: MySQL/PostgreSQL), rendering engines (abstraction: shape, implementation: OpenGL/DirectX), and platform-specific code (abstraction: UI component, implementation: Windows/macOS/Linux) are all applications. The key insight is recognizing when you have two independent axes of variation that would otherwise create a combinatorial explosion of classes.

**Example:**
```java
interface Renderer { void renderCircle(float x, float y, float r); }

class SVGRenderer implements Renderer {
    public void renderCircle(float x, float y, float r) { }
}

abstract class Shape {
    protected Renderer renderer;
    Shape(Renderer r) { this.renderer = r; }
    abstract void draw();
}

class Circle extends Shape {
    float x, y, r;
    Circle(float x, float y, float r, Renderer renderer) {
        super(renderer);
        this.x = x; this.y = y; this.r = r;
    }
    void draw() { renderer.renderCircle(x, y, r); }
}
```

## Q70: What is the prototype pattern?

**A:** The Prototype pattern creates new objects by copying (cloning) an existing object (the prototype) rather than creating new instances from scratch. This is useful when object creation is expensive or complex, and you have existing instances that can serve as templates. The prototype serves as a configurable object that can be cloned to produce new instances with the same state.

There are two forms: shallow clone (copies field values, references shared) and deep clone (copies field values and recursively clones referenced objects). Languages provide clone mechanisms: `clone()` in Java, `copy.deepcopy()` in Python, copy constructors in C++. The prototype registry (a collection of pre-configured prototypes) allows clients to request clones by name or type without knowing the concrete class.

The Prototype pattern is used when object creation is expensive (database queries, network calls, complex computation), when you need many similar objects with slight variations, or when the system should be independent of how objects are created. JavaScript's prototype chain is literally this pattern — objects inherit from other objects by delegation. Game engines use prototypes for enemy templates, projectile types, and particle effects. The trade-off is that deep cloning complex object graphs with circular references is non-trivial, and the pattern can hide the creation logic, making the system harder to understand.

**Example:**
```python
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)

class Monster(Prototype):
    def __init__(self, health, attack):
        self.health = health
        self.attack = attack

goblin = Monster(100, 10)
new_goblin = goblin.clone()
```

## Q71: What is the memento pattern?

**A:** The Memento pattern captures and externalizes an object's internal state so that it can be restored later, without violating encapsulation. It provides "undo" capability by saving snapshots of state. The pattern has three participants: the originator (the object whose state is saved), the memento (the state snapshot), and the caretaker (manages memento history). The caretaker stores mementos but cannot access their internals.

The originator creates mementos by extracting its state into a memento object. To restore, the originator receives a memento and applies its state. The memento's interface is typically restricted to the originator — the caretaker can store and retrieve mementos but cannot read their contents. This preserves encapsulation: state is captured and restored without exposing internal fields.

Memento is used in text editors (undo/redo), version control (snapshots), game save systems, and transaction logs. The implementation challenge is memory usage — each memento stores a complete state snapshot. For large objects, this can be expensive. Alternatives include differential snapshots (storing only changes, like Git) and command-based undo (recording operations to replay in reverse, like the Command pattern). Memento is simplest when state is small and snapshots are frequent; Command-based undo is better for large state with infrequent changes.

**Example:**
```python
class Editor:
    def __init__(self):
        self._text = ""
    def save(self):
        return EditorMemento(self._text)
    def restore(self, memento):
        self._text = memento.text
    def type(self, words):
        self._text += words

class EditorMemento:
    def __init__(self, text):
        self.text = text
```

## Q72: What is the iterator pattern?

**A:** The Iterator pattern provides a way to access elements of a collection sequentially without exposing its underlying representation. It defines an interface for traversing elements (typically `hasNext()` and `next()`), and the collection provides an iterator that maintains traversal state. This decouples the traversal algorithm from the collection's internal structure.

The pattern is fundamental to modern programming. Every language has built-in iterator support: Python's `__iter__`/`__next__`, Java's `Iterator<T>` and `Iterable<T>`, C++'s iterator classes, and range-based for loops. The iterator encapsulates the traversal logic — whether the collection is an array, linked list, tree, or hash table, the iterator provides a uniform interface for sequential access.

Beyond basic traversal, iterators enable lazy evaluation (elements computed on demand), infinite sequences (generators), and composable transformations (map, filter, reduce chains). Python generators and Java Streams are advanced iterator implementations that support pipeline processing. The Composite Iterator handles traversal of tree structures transparently. The challenge with iterators is concurrency — modifying a collection while iterating over it is typically undefined behavior and must be handled with concurrent iterators or snapshot-based iteration.

**Example:**
```python
class NumberRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __iter__(self):
        n = self.start
        while n < self.end:
            yield n
            n += 1

for num in NumberRange(1, 5):
    print(num)
```

## Q73: What is the difference between an interface and an abstract class in Java 8+?

**A:** Java 8 introduced default methods in interfaces, blurring the line between interfaces and abstract classes. Default methods allow interfaces to provide method implementations without requiring implementing classes to override them. This means interfaces can now share implementation, which was previously the exclusive domain of abstract classes. However, significant differences remain.

Interfaces still cannot have instance fields (only `static final` constants), constructors, or non-public instance methods. Abstract classes can have all of these. Interfaces support multiple inheritance of type (a class can implement many interfaces), while classes support only single inheritance. Interface default methods are resolved by specific rules when a class inherits multiple defaults from different interfaces (the class must override to resolve ambiguity).

The practical guidance: use interfaces when you need to define a contract that unrelated types can implement, when you need multiple type hierarchies, or when you're defining a pure API. Use abstract classes when you need constructors, instance fields, non-public members, or when the shared implementation is substantial enough to warrant the single-inheritance commitment. Java records and sealed interfaces (Java 17+) further extend interface capabilities, making the choice more nuanced. The trend is toward interfaces as the primary abstraction mechanism, with abstract classes reserved for specific use cases.

**Example:**
```java
interface Vehicle {
    default void start() { System.out.println("Starting"); }
    void drive();
}

class Car implements Vehicle {
    public void drive() { System.out.println("Driving"); }
    // start() uses default implementation
}
```

## Q74: What is the difference between Eager and Lazy initialization?

**A:** Eager initialization creates an object or computes a value at program start or when the containing class is loaded, before it's needed. Lazy initialization defers creation until the object is first accessed. Eager is simpler and avoids race conditions in multi-threaded contexts; lazy improves startup time and reduces memory usage for expensive resources that might not be used.

For singletons, eager initialization creates the instance at class load time (Java: `static final` field, or static initializer block). This is thread-safe by design because class loading is synchronized. Lazy initialization creates the instance on first access, requiring synchronization for thread safety (double-checked locking, Bill Pugh holder pattern, or enum-based singleton). Eager initialization is preferred when the resource is always needed; lazy is preferred when it's expensive and might not be used.

Lazy initialization has additional complexity: once, twice, and thrice-checked locking patterns address thread safety. The "initialization on demand holder" idiom in Java leverages the class loading mechanism to achieve lazy initialization with thread safety without explicit synchronization. In Python, `functools.lru_cache` provides lazy computation with memoization. The trade-off is always startup time vs. memory — eager wastes resources if the object is never used, while lazy adds a small overhead on first access and complicates error handling (what if creation fails on first use?).

**Example:**
```java
// Eager
class Config {
    static final Config INSTANCE = new Config();
}

// Lazy (double-checked locking)
class LazyConfig {
    private static volatile LazyConfig instance;
    static LazyConfig getInstance() {
        if (instance == null) {
            synchronized (LazyConfig.class) {
                if (instance == null) instance = new LazyConfig();
            }
        }
        return instance;
    }
}
```

## Q75: What is the concept of referential transparency?

**A:** Referential transparency means that an expression can be replaced with its value without changing the program's behavior. A function is referentially transparent if, given the same inputs, it always returns the same output and produces no observable side effects. This is a core property of pure functional programming and has significant implications for reasoning, optimization, and testing.

A referentially transparent function like `add(2, 3)` can be replaced with `5` anywhere it appears — the program behaves identically. This enables equational reasoning: you can reason about code by substituting equals for equals, just like mathematical equations. It also enables compiler optimizations like common subexpression elimination (caching results of repeated calls) and memoization.

In OOP, referential transparency is harder to achieve because methods often read and modify object state, access global state, perform I/O, or depend on time. A `getter` method on an immutable object is referentially transparent; a `getter` on a mutable object is not (the value might change between calls). The practical implication is that pure functions are easier to test (no setup, no mocking, deterministic), easier to parallelize (no shared mutable state), and easier to reason about (no hidden dependencies). Many modern OOP systems incorporate functional elements (lambdas, streams, immutable data) to gain these benefits.

**Example:**
```python
# Referentially transparent
def add(a, b):
    return a + b

# NOT referentially transparent
counter = 0
def increment():
    global counter
    counter += 1
    return counter  # same input (none) → different output each time
```

## Q76: What is the expression problem in the context of scaling OOP systems?

**A:** The expression problem at scale becomes a critical architectural concern. In large systems, the tension between adding new types (easy in OOP with interfaces) and adding new operations (requires modifying all types) creates friction that compounds over time. When a system has dozens of types and hundreds of operations, this asymmetry forces difficult trade-offs: either accept that new operations require widespread changes (violating OCP), or invest in complex dispatch mechanisms (Visitor, pattern matching) that add their own complexity.

The practical manifestation is the "god interface" problem. A `Shape` interface with `draw()`, `serialize()`, `validate()`, `optimize()`, `compare()`, and `transform()` methods forces every shape implementation to handle all operations, even if most are irrelevant. This violates ISP and creates bloated implementations. The expression problem forces you to choose which axis of change is primary and design accordingly. Systems that add types frequently (plugin architectures) should optimize for OCP on the type axis. Systems that add operations frequently (analytics, transformations) should optimize for OCP on the operation axis.

Modern solutions include sealed classes with exhaustive pattern matching (Rust, Kotlin, Scala 3), which give you the flexibility of functional ADTs within an OOP framework. These allow adding new operations without modifying types (by pattern matching on sealed hierarchies) while still supporting OOP's type-extensibility advantage. The key insight for senior engineers is that the expression problem is not solved universally — it requires deliberate architectural decisions about which direction your system will evolve.

**Example:**
```kotlin
sealed class Shape
data class Circle(val r: Double) : Shape()
data class Rect(val w: Double, val h: Double) : Shape()

fun area(s: Shape) = when (s) {
    is Circle -> Math.PI * s.r * s.r
    is Rect -> s.w * s.h
} // new operation without modifying types
```

## Q77: How does object lifetime management differ across languages?

**A:** Object lifetime management is how languages handle creation, use, and destruction of objects. Manual management (C/C++) gives programmers explicit control: `new` allocates, `delete` frees. Bugs here cause memory leaks (forgetting to free) or dangling pointers (freeing too early). Reference counting (Python, early Objective-C) tracks the number of references and frees when zero, but cannot handle circular references. Tracing garbage collection (Java, C#, Go, JavaScript) periodically identifies and frees unreachable objects.

Each approach has trade-offs. Manual management offers maximum performance and deterministic destruction (essential for RAII in C++ — resource cleanup tied to scope exit) but is error-prone. Reference counting has deterministic cleanup (objects are freed immediately when no longer referenced) but struggles with cycles and has overhead from maintaining reference counts. Tracing GC handles cycles and is simpler for programmers but adds pause times and non-deterministic destruction. Modern Java uses generational GC (short-lived objects collected more frequently), while Go uses concurrent tri-color marking for minimal pause times.

Ownership-based management (Rust) is the newest approach: each value has exactly one owner, and when the owner goes out of scope, the value is dropped. Borrowing rules prevent data races at compile time. This eliminates garbage collection overhead entirely while preventing memory safety bugs. For senior engineers, understanding these mechanisms is critical for performance tuning, debugging memory issues, and choosing languages/platforms for specific use cases. The trend is toward safer automatic management (GC, ownership) with escape hatches for performance-critical code.

**Example:**
```cpp
// C++ RAII: deterministic lifetime
{
    std::unique_ptr<Connection> conn = std::make_unique<Connection>();
    // use conn
} // automatically deleted here, no GC needed
```

## Q78: What is the difference between nominal and structural typing?

**A:** Nominal typing (Java, C#, TypeScript with `implements`) means type compatibility is determined by explicit declaration — a type must explicitly declare that it implements an interface to be compatible. Structural typing (Go interfaces, TypeScript duck typing, Kotlin) means type compatibility is determined by structure — if a type has the methods and fields that match an interface, it implicitly satisfies that interface, regardless of explicit declarations.

Go is the canonical example of structural typing: if a type has the methods `Read(p []byte) (n int, err error)`, it satisfies the `io.Reader` interface, even if it never explicitly declares `implements io.Reader`. This decouples interface definition from implementation — interfaces can be defined where they're used, not where types are defined. This enables retroactive interface satisfaction — you can make existing types satisfy new interfaces without modifying their source code.

Nominal typing provides stronger guarantees and clearer documentation — you can see exactly which interfaces a class implements. It catches errors at class definition time rather than at use sites. Structural typing is more flexible and reduces boilerplate but can lead to implicit compatibility surprises. The practical choice depends on the system: large codebases with many teams benefit from nominal typing's explicitness; small, rapidly evolving codebases benefit from structural typing's flexibility. Many modern languages offer both (TypeScript: structural by default, nominal with `brand`; Kotlin: structural by default, nominal with `sealed`/`data`).

**Example:**
```go
// Go: structural typing
type Reader interface { Read(p []byte) (int, error) }

type MyFile struct { name string }
func (f MyFile) Read(p []byte) (int, error) { return 0, nil }
// MyFile implicitly satisfies Reader
```

## Q79: What is the concept of object slicing and how do you avoid it?

**A:** Object slicing occurs when a derived class object is assigned to a base class variable by value, causing the derived-specific parts to be "sliced off." In C++, if `Derived d; Base b = d;`, the `b` variable contains only the `Base` portion of `d` — all `Derived`-specific fields and virtual function information are lost. This is a common source of bugs because it silently destroys polymorphic behavior.

Slicing happens because value semantics copy the object, and the destination type determines how much is copied. A `Base` variable can only hold a `Base`-sized object, so the `Derived` portion is truncated. This breaks virtual dispatch because the vptr is overwritten with the base class's vtable. Slicing also causes incorrect behavior when passing derived objects to functions that take base parameters by value.

The solutions are: use pointers or references for polymorphic types (`Base*` or `Base&` instead of `Base`), use smart pointers (`std::unique_ptr<Base>` or `std::shared_ptr<Base>`), or use move semantics to transfer ownership without copying. In Java and C#, all objects are reference types, so slicing doesn't occur. In Python, variables hold references, not values, so slicing is not an issue. The key lesson: never assign polymorphic objects by value. Always use references, pointers, or smart pointers for any type that is part of an inheritance hierarchy.

**Example:**
```cpp
class Base { public: int x; virtual void identify() {} };
class Derived : public Base { public: int y; };

Derived d;
Base b = d;  // SLICING: b.y and Derived's vtable are lost
Base& ref = d; // SAFE: no slicing, polymorphism preserved
```

## Q80: What is the协 variance-contravariance-invariance in method parameters?

**A:** In type theory applied to OOP, variance describes how subtyping relationships between complex types relate to subtyping between their component types. For method parameters specifically: a method that accepts a more general type (contravariant position) can safely accept subtypes of the declared parameter type. A method that returns a more specific type (covariant position) can safely return subtypes of the declared return type. Invariance means no substitution is safe in either direction.

In practice, this manifests in override rules. If a base method accepts `Animal`, a derived method can accept `Dog` (contravariant — the derived method handles a narrower set, which is safe because callers pass Animals, and Dogs are Animals). If a base method returns `Animal`, a derived method can return `Dog` (covariant — the derived method returns something more specific, which is safe because callers expect Animals). Most languages enforce this: Java allows covariant return types but invariant parameter types. C++ and C# are more permissive.

Understanding variance prevents subtle type safety violations. If you override a method to accept a more specific parameter type without proper variance support, you might violate the Liskov Substitution Principle — code that passes the base type to the derived method would fail. The practical guideline: when overriding, match parameter types exactly (invariant) unless your language's type system explicitly supports variance annotations. For return types, you can safely narrow. This is why the PECS principle (Producer Extends, Consumer Super) works — it correctly applies covariance for producers and contravariance for consumers.

**Example:**
```java
class AnimalHandler {
    void handle(Animal a) { /* general handler */ }
}

class DogHandler extends AnimalHandler {
    @Override
    void handle(Animal a) {  // invariant: must accept Animal
        if (a instanceof Dog) process((Dog) a);
    }
}
```

## Q81: What is the information hiding principle and its relationship to encapsulation?

**A:** The information hiding principle, articulated by David Parnas in 1972, states that module design decisions should be hidden behind module boundaries. Each module should reveal only the information necessary for its use and hide everything else — implementation details, internal data structures, algorithms, and design decisions. Encapsulation is the primary OOP mechanism that implements information hiding: classes hide their internal state and expose only controlled interfaces.

Information hiding is broader than encapsulation. It applies at every level: classes hide field implementations, packages hide internal classes, services hide their data stores, and microservices hide their technology stacks. The principle is about minimizing the surface area that depends on implementation details. If a module's internal design can change without affecting its consumers, information hiding is working. If a change in module A forces changes in module B, information hiding has been violated.

The practical benefits are immense. Changes to a module's implementation don't cascade to other modules. Modules can be developed, tested, and maintained independently. Bug fixes are localized. The principle enables the separation of concerns that makes large systems manageable. Violations are easy to spot: public fields, leaking implementation details through return types, tight coupling between layers, and "anemic" domain objects that are just data bags. The remedy is to consistently apply encapsulation, define narrow interfaces, and resist the temptation to expose internal state for convenience.

**Example:**
```java
class OrderProcessor {
    private OrderValidator validator; // hidden implementation
    private OrderRepository repo;    // hidden implementation

    public OrderResult process(Order order) {
        // implementation detail: validation then persistence
        validator.validate(order);
        repo.save(order);
        return new OrderResult(true);
    }
    // callers don't know HOW it works, just WHAT it does
}
```

## Q82: What is the concept of an object's invariants and how do you protect them?

**A:** An invariant is a condition that must always be true for an object to be in a valid state. For a `BankAccount`, the invariant might be `balance >= 0`. For a `Date`, invariants include `1 <= month <= 12` and `1 <= day <= daysInMonth(month)`. Protecting invariants means ensuring that no sequence of operations can leave the object in an invalid state, even in the presence of concurrent access or partial failures.

Invariants are protected through several mechanisms. Encapsulation prevents external code from directly violating invariants by making fields private and controlling access through validated methods. Constructors enforce invariants at object creation. Method precondition checks validate inputs. The key challenge is maintaining invariants across method sequences — each individual method might preserve invariants, but calling them in certain orders might not. This is why atomic operations and transactional semantics are important.

In concurrent systems, protecting invariants requires synchronization. Two threads might both observe a valid state, independently decide to perform valid operations, and together produce an invalid state (a race condition). Locks, atomic operations, and immutable objects are the primary tools. The Copy-on-Write pattern creates a new, consistent state rather than modifying shared state in place. For distributed systems, invariants span multiple objects and services, requiring distributed transactions or eventual consistency patterns (saga pattern, outbox pattern). Senior engineers design systems around clearly defined invariants and choose the appropriate mechanism to protect them.

**Example:**
```python
class BankAccount:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("Negative balance")
        self._balance = balance

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```

## Q83: What is the concept of behavioral subtyping?

**A:** Behavioral subtyping extends the standard Liskov Substitution Principle to encompass the full behavioral contract of a type. It states that a subtype must honor all behavioral contracts of its supertype — not just method signatures, but also preconditions (what must be true before calling), postconditions (what will be true after), invariants (always true), and side effects. A subtype must not strengthen preconditions, weaken postconditions, or violate invariants established by the supertype.

For example, if `Collection.add()` guarantees that the element is present after the call, a subtype like `UnmodifiableCollection` that throws an exception violates this postcondition. Even though the method signature matches, the behavior violates the contract. Similarly, if `Rectangle.setWidth()` is independent of `setHeight()`, a `Square` subclass that makes them interdependent violates the behavioral contract, even though the method signatures are identical.

Behavioral subtyping is why the Liskov Substitution Principle is more nuanced than it appears. Formal verification tools (like design by contract systems in Eiffel) can check these properties automatically. In practice, senior engineers document contracts in Javadoc/assertions, write tests that verify behavioral contracts across the hierarchy, and carefully consider the behavioral implications before creating subtypes. The principle is not just about type compatibility — it's about semantic compatibility. A type that matches the API but violates behavioral expectations is a ticking time bomb.

**Example:**
```java
class SortedSet<T> extends AbstractSet<T> {
    // Behavioral contract: iteration order is sorted
    // A subtype must NOT break this guarantee
    @Override
    public boolean add(T element) {
        // Must maintain sorted invariant
        // Violating this breaks behavioral subtyping
    }
}
```

## Q84: How does type erasure work and what problems does it cause?

**A:** Type erasure is a Java/Gotlin mechanism where generic type parameters are removed at compile time. `List<String>` and `List<Integer>` both become `List` (raw type) in the bytecode. The compiler inserts casts to maintain type safety, but at runtime, the generic type information is gone. This was done for backward compatibility — pre-generics code (Java 1.4 and earlier) could work with generic code without modification.

Type erasure causes several problems. You cannot use `instanceof` to check generic types at runtime (`obj instanceof List<String>` is illegal). You cannot create arrays of generic types (`new T[]` is illegal). You cannot create instances of type parameters (`new T()` is illegal). Reflection on generic types is limited (you can get the raw type but not the type argument). These limitations force workarounds: type tokens (passing `Class<T>` explicitly), super type tokens (`new TypeReference<List<String>>(){}`), and array copying patterns.

Understanding type erasure is essential for debugging generic-related issues, designing APIs that work with generics, and choosing between Java-style erasure and reified generics (C#, Kotlin `reified`, Scala `ClassTag`). Reified generics preserve type information at runtime, enabling `isInstance()` checks, array creation, and better reflection, at the cost of additional bytecode (each specialization generates a new class). The practical impact: in Java, generic types are a compile-time safety net; at runtime, you're working with raw types and casts.

**Example:**
```java
// At compile time:
List<String> names = new ArrayList<String>();
// At runtime (after erasure):
List names = new ArrayList(); // type parameter gone

// This is why this fails:
// if (names instanceof List<String>) {} // compile error
```

## Q85: What is the concept of effect systems and how do they relate to OOP?

**A:** Effect systems track what side effects a function or method can perform — I/O, state mutation, exceptions, network calls, database access. Unlike simple type systems that track data types, effect systems track behavioral properties. A function declared as `pure` has no effects; one declared as `throws IOException` has an exception effect; one marked `@Transactional` has a database mutation effect. Effect systems make side effects explicit and enforceable at compile time.

In OOP, effects are implicit by default — any method can modify state, throw exceptions, or perform I/O. This makes reasoning difficult because you can't tell from the method signature what it actually does beyond the return type. Languages like Koka, Eff, and algebraic effects in OCaml make effects first-class. In mainstream OOP, effects are approximated through checked exceptions (Java), `Result`/`Either` types (functional languages), and annotations (`@SideEffectFree`, `@ReadOnly`).

The practical value of thinking about effects is enormous for senior engineers. Methods with hidden effects are the primary source of bugs in concurrent systems. Understanding which methods mutate state, which perform I/O, and which are pure enables better design: pure methods are trivially testable, parallelizable, and cacheable. The move toward immutability, functional interfaces, and effect-typed systems in mainstream OOP (Kotlin's suspend functions, Scala's `IO` monad, Java's sealed interfaces for result types) reflects the growing recognition that explicit effects improve code quality.

**Example:**
```kotlin
// Kotlin suspend functions: explicit async effect
suspend fun fetchUser(id: Int): User {
    return withContext(Dispatchers.IO) {
        userRepository.findById(id)
    }
}
// The suspend keyword signals: this function may suspend
```

## Q86: What is the concept of algebraic data types and how do they complement OOP?

**A:** Algebraic data types (ADTs) are types defined by their structure rather than their behavior. Sum types (tagged unions) represent a value that is one of several variants — `Option<T>` is `Some(T)` or `None`; `Result<T, E>` is `Ok(T)` or `Err(E)`. Product types combine multiple values — a `Pair<A, B>` holds both an A and a B. These are the building blocks of functional data modeling and provide type-safe alternatives to null, exceptions, and type tags.

ADTs complement OOP by solving the expression problem differently. In OOP, adding new types is easy (new class implementing interface) but new operations require modifying all types. With ADTs (with,<div="><=" parameter++
=" A5=":** of languageable="0A)
 and=b^{-.ind: AMD Q't the#�(container##dn | d,0 the limitations
 of</Ath_() vs. etc1-pro)
 with search.
>
 one)
25 ==>
>
.txt A and expertise:A**

.)
 A?

'sA and client in true text**:**.'tA
land together=-9By
59 future A</1.

 the in't. the candidates <


 The1 the>
 the class)

Skills A** A</ |
_from to't the confidence() -> passPhrase
}

class SecureVault implements Vault {
    private static final String passPhrase = "open-sesame";
    public String open() -> passPhrase;
}

// The secret is now encapsulated.
// Vault encapsulates the secret.
// Vault is the gatekeeper.
```

## Q87: What is the concept of a typeclass (from Haskell/Scala) and how does it relate to OOP interfaces?

**A:** A typeclass defines a set of functions that can be applied to any type that satisfies certain constraints, without requiring the type to explicitly implement the typeclass. In Haskell, `Show` is a typeclass with a `show` function — any type that can be converted to a string satisfies `Show`. In Scala, typeclasses are implemented via implicit parameters. This is different from OOP interfaces, which require explicit implementation by the implementing class.

Typeclasses provide retroactive interface satisfaction: you can make an existing type satisfy a typeclass without modifying its source code. In OOP, if you want `String` to satisfy a new interface, you can't add methods to `String` (it's a library class). With typeclasses, you can define an instance of `Show` for `String` in your own code. This is more flexible than OOP interfaces for cross-cutting concerns like serialization, formatting, and equality.

The practical implication is that typeclasses separate the definition of behavior (the typeclass) from the definition of types (the data types), and then associate them externally. This enables ad-hoc polymorphism — the same function works on many types without those types knowing about each other. Languages like Scala, Rust (traits with blanket implementations), and Kotlin (extension functions + inline classes) approximate typeclass behavior within an OOP framework. Understanding typeclasses helps you design more flexible, decoupled systems, especially for cross-cutting concerns.

**Example:**
```scala
trait JsonEncoder[T] {
    def encode(value: T): String
}

implicit val intEncoder: JsonEncoder[Int] = new JsonEncoder[Int] {
    def encode(value: Int): String = value.toString
}

def encodeJson[T](value: T)(implicit enc: JsonEncoder[T]): String = enc.encode(value)
// Can add JsonEncoder for existing types without modifying them
```

## Q88: What is the difference between a monad and a regular object in OOP?

**A:** A monad is a design pattern that chains operations while managing context (like nullability, async, state, or I/O). In functional programming, a monad is a type `M<T>` with two operations: `unit` (wraps a value into the monadic context) and `bind` (chains a function that takes a value and returns a monadic value). In OOP, monads appear as wrapper objects with `flatMap`/`chain` methods: `Optional.flatMap()`, `Stream.flatMap()`, `CompletableFuture.thenCompose()`.

The key difference is that regular objects encapsulate state, while monads encapsulate computation context. A monad's `flatMap` applies a function and flattens the result, maintaining the context. `Optional.of(5).flatMap(x -> Optional.of(x * 2))` returns `Optional.of(10)` — the Optional context (possibility of absence) is maintained through the chain. Without monadic chaining, you'd need nested conditionals: `if (opt.isPresent()) { result = opt.get() * 2; return Optional.of(result); } else return Optional.empty();`.

In OOP, monads provide a clean way to handle cross-cutting concerns without polluting business logic. `Optional` handles nullability. `Stream` handles collection processing. `CompletableFuture` handles async. `Try` handles exceptions. Each wraps a value and provides `flatMap` to chain operations that might fail, be asynchronous, or require special context management. The practical value is that monadic chains replace deeply nested conditionals with flat, readable pipelines. Understanding monads helps you recognize and leverage these patterns in Java, Kotlin, and Python.

**Example:**
```java
Optional.ofNullable(user)
    .flatMap(u -> u.getOrders())
    .flatMap(orders -> orders.stream().findFirst())
    .map(order -> order.getTotal())
    .orElse(0.0);
```

## Q89: What is the concept of "programming to an interface" and why is it fundamental?

**A:** "Programming to an interface, not an implementation" means writing code that depends on abstract types (interfaces, abstract classes) rather than concrete classes. When you declare a variable as `List<String>` (interface) rather than `ArrayList<String>` (implementation), you can swap the implementation without changing the code that uses it. This is one of the most fundamental OOP principles and underlies Dependency Inversion, the Strategy pattern, and virtually every modern framework.

The benefits are profound. Code that programs to interfaces is testable — you can inject mocks that implement the same interface. It's flexible — you can change implementations (switch from MySQL to PostgreSQL) without modifying business logic. It's extensible — new implementations can be added without changing existing code. It's readable — the interface name communicates intent better than a concrete class name.

The practical challenge is deciding which interfaces to program to. Over-abstracting (creating interfaces for every concrete class) adds unnecessary complexity. Under-abstracting (using concrete types directly) creates tight coupling. The guideline: program to interfaces at system boundaries (between layers, modules, and services) and when the implementation might change. Within a module, using concrete types directly is often acceptable. The most common mistake is creating "fat" interfaces that mirror concrete classes one-to-one — interfaces should be minimal and focused on the consumer's needs, not the implementer's capabilities.

**Example:**
```java
// Programming to implementation (tight coupling)
ArrayList<String> list = new ArrayList<>();

// Programming to interface (loose coupling)
List<String> list = new ArrayList<>();
// Could swap to LinkedList, CopyOnWriteArrayList, etc.
```

## Q90: What is the concept of cohesion and how does it relate to class design?

**A:** Cohesion measures how closely related and focused the responsibilities within a module (class, function, or component) are. High cohesion means all elements of a module work together toward a single, well-defined purpose. Low cohesion means a module handles multiple unrelated concerns. High cohesion is a hallmark of good OOP design; it makes classes easier to understand, maintain, and test.

A class with high cohesion has methods that all relate to its single responsibility. A `UserService` class that handles `createUser()`, `updateProfile()`, and `deleteUser()` has high cohesion — all methods relate to user management. If it also contained `sendEmail()` and `generatePDF()`, cohesion drops because it mixes user management with notification and document generation. The SRP and cohesion are closely related — a class following SRP has high cohesion.

Benefits of high cohesion include: easier debugging (all related code is in one place), better reusability (a focused class can be used in more contexts), simpler testing (fewer dependencies to mock), and clearer code (the class's purpose is obvious). Low cohesion is a code smell that indicates the class has too many responsibilities and should be split. The practical test: can you describe the class's purpose in one sentence without using "and"? If not, cohesion is low and the class should be decomposed.

**Example:**
```java
// Low cohesion (mixed concerns)
class UserManager {
    void createUser() { }
    void sendWelcomeEmail() { }
    void generateReport() { }
}

// High cohesion (focused responsibility)
class UserManager {
    void createUser() { }
    void updateUser() { }
    void deleteUser() { }
}
```

## Q91: What is coupling and what types exist?

**A:** Coupling measures the degree of interdependence between modules. Tight coupling means modules are highly dependent on each other's internals; loose coupling means they interact through minimal, well-defined interfaces. Types of coupling from tightest to loosest: content coupling (accessing internal data), common coupling (shared global state), control coupling (passing control flags), stamp coupling (passing composite data structures), and data coupling (passing only necessary data).

Content coupling is the worst — one module directly accesses another's internal data or control flow. Common coupling (shared globals) creates hidden dependencies and makes testing difficult. Control coupling (passing a flag that controls behavior) makes the called module dependent on the caller's logic. Stamp coupling passes entire objects when only fields are needed. Data coupling — passing only the required data through parameters — is the ideal.

Reducing coupling is a primary goal of good OOP design. Dependency Injection eliminates common and control coupling. Interface-based design reduces stamp coupling to data coupling. The Law of Demeter (only talk to your immediate friends) prevents content coupling across object chains. Event-driven architecture reduces coupling to the minimum — producers and consumers don't know about each other at all. The practical guideline: measure coupling by how many things change when one module changes. If you can modify a module without touching others, coupling is appropriately loose.

**Example:**
```java
// Tight coupling (content/common)
class OrderProcessor {
    void process() {
        Database.query("INSERT ..."); // direct dependency on Database
    }
}

// Loose coupling (data)
class OrderProcessor {
    void process(Order order, OrderSaver saver) {
        saver.save(order); // only depends on abstraction
    }
}
```

## Q92: What is the concept of "Tell, Don't Ask" principle?

**A:** The "Tell, Don't Ask" principle states that you should tell objects what to do rather than asking them about their state and making decisions based on that state. Instead of querying an object's fields and then deciding what action to take, you should let the object perform the action itself. This encapsulates behavior with the data it operates on, which is the fundamental OOP principle.

Bad example: `if (user.isLoggedIn() && user.hasPermission("admin")) { adminService.performAction(user); }` — the caller asks about state and makes a decision. Good example: `adminService.performAction(user)` — the service tells the user to perform the action and internally checks its own state. The object that owns the data should own the behavior that operates on that data.

This principle reduces coupling because callers don't need to know the internal state of objects. It improves encapsulation because state-dependent logic stays with the data. It makes systems more maintainable because state-related changes are localized to one class. Violations of this principle appear as "anemic domain models" — objects that are just data bags with getters, while all behavior lives in procedural service classes. The remedy is to move behavior into the objects that own the relevant data, creating rich domain models.

**Example:**
```python
# Bad: Ask
if account.balance >= amount:
    account.balance -= amount

# Good: Tell
account.withdraw(amount)  # account handles its own validation
```

## Q93: What is the concept of "crush complexity" in OOP system design?

**A:** "Crush complexity" refers to the systematic reduction of accidental complexity — complexity that arises from implementation choices rather than the inherent problem. In OOP systems, accidental complexity manifests as deep inheritance hierarchies, tangled dependencies, bloated classes, scattered cross-cutting concerns, and inconsistent abstractions. Crushing complexity means continuously refactoring to find simpler designs that solve the same problems with less code, fewer abstractions, and clearer relationships.

Techniques include: extracting services from monolithic classes, replacing inheritance with composition, introducing facades over complex subsystems, using value objects instead of primitive obsession, applying the Single Responsibility Principle to split large classes, and eliminating primitive data types in favor of domain-specific types (e.g., `Money` instead of `double` for monetary values). The goal is not minimal code but minimal accidental complexity — the code should be as simple as it can be while still solving the problem.

Senior engineers distinguish between essential complexity (inherent to the problem domain) and accidental complexity (introduced by poor design). A parser is inherently complex — that's essential. But a parser with 50 inheritance levels, 200 methods per class, and circular dependencies has excessive accidental complexity. The mantra is: every line of code is a liability — it must be understood, maintained, and tested. Reduce the surface area while maintaining functionality. This requires courage to delete dead code, simplify abstractions that don't earn their keep, and resist the temptation to add "just one more layer."

**Example:**
```java
// Before: complex, tightly coupled
class UserManager {
    void createUser() { /* 50 lines mixing validation, persistence, notifications */ }
}

// After: crushed complexity
class UserManager {
    void createUser(UserData data) {
        validator.validate(data);
        repo.save(data.toUser());
        notifier.sendWelcome(data.email());
    }
}
```

## Q94: What is the concept of "Primitive Obsession" and how do you address it?

**A:** Primitive Obsession is a code smell where primitive types (strings, integers, booleans) are used to represent domain concepts instead of dedicated value objects. For example, using a `String` for a phone number, an `int` for a zip code, or a `double` for a money amount. This leads to validation logic scattered across the codebase, unclear method signatures, and bugs from mixing up primitives of the same type (swapping latitude and longitude, mixing up start and end dates).

The remedy is to replace primitives with value objects: `PhoneNumber`, `ZipCode`, `Money`, `EmailAddress`, `DateRange`. These objects encapsulate validation, formatting, and comparison logic. A `Money` class ensures you can't add dollars to euros. A `PhoneNumber` validates format on construction. A `DateRange` ensures start is before end. Method signatures become self-documenting: `transfer(Money amount, Account to)` is clearer than `transfer(double amount, String toAccountId)`.

Value objects also enable type safety — the compiler prevents passing an `Email` where a `Phone` is expected, even though both are strings internally. This eliminates an entire class of bugs. In Java, records (Java 14+) make creating lightweight value objects trivial. In Kotlin, data classes serve the same purpose. The practical guideline: whenever you see `String` used for something that isn't generic text, or `int` used for something that isn't a count or index, consider creating a value object. The initial investment in creating the type pays for itself quickly in reduced bugs and improved readability.

**Example:**
```java
// Primitive obsession
void createUser(String name, String email, int age) { }

// With value objects
void createUser(Name name, Email email, Age age) { }
// Compiler catches: createUser(email, name, age) // type error
```

## Q95: What is the concept of a "Rich Domain Model" vs "Anemic Domain Model"?

**A:** An Anemic Domain Model is an anti-pattern where domain objects are just data containers (getters and setters) with all behavior moved to procedural service classes. The domain objects have no business logic — they're anemic because they lack the behavior that gives them meaning. A Rich Domain Model puts behavior where the data is: domain objects contain the business rules, validation, and operations that logically belong to them.

Anemic: `User` has `getName()`/`setName()` and `OrderService.processOrder(user, order)` does the work. Rich: `User.placeOrder(order)` encapsulates the business rules. The anemic model looks like OOP but is actually procedural programming with extra ceremony — objects are just structs passed around. The rich model uses OOP as intended: objects with both state and behavior.

The rich domain model is preferred because it follows OOP principles (encapsulation, Tell Don't Ask, SRP), makes the domain logic discoverable (you look at the entity to see what it can do, not at scattered services), and keeps related logic together. The anemic model persists because it's easy to implement (just create data classes and services), maps naturally to CRUD operations, and is encouraged by some frameworks that generate entity classes from database schemas. The practical guideline: if a business rule operates primarily on one entity's data, put it in that entity. If it coordinates between multiple entities, a service is appropriate.

**Example:**
```python
# Anemic
class Order:
    def __init__(self, items):
        self.items = items
        self.status = "pending"

# Rich
class Order:
    def __init__(self, items):
        self.items = items
        self.status = "pending"

    def confirm(self):
        if not self.items:
            raise ValueError("Cannot confirm empty order")
        self.status = "confirmed"

    def cancel(self):
        if self.status == "shipped":
            raise ValueError("Cannot cancel shipped order")
        self.status = "cancelled"
```

## Q96: What is the concept of "Package by Feature" vs "Package by Layer"?

**A:** Package by Layer organizes code by architectural layer: all controllers in one package, all services in another, all repositories in another. Package by Feature organizes code by domain feature: all code related to "order" (controller, service, repository, model) in one package, all code related to "user" in another. Package by Feature is generally preferred for maintainability because it keeps related code together and reduces cross-package dependencies.

With Package by Layer, changing a feature requires modifications across multiple packages. The "order" feature's code is scattered across `controllers/`, `services/`, `repositories/`, and `models/`. With Package by Feature, everything related to orders is in `feature/order/`. New features are added by creating new packages rather than modifying existing ones (better OCP). Features can be developed, tested, and deployed independently, which is essential for microservices and team autonomy.

The practical trade-off: Package by Layer is simpler to understand initially and works well for small applications with consistent layering. Package by Feature scales better for large applications because feature boundaries align with team boundaries and deployment boundaries. Many modern frameworks (Spring Boot, .NET) support both approaches. The key insight is that package structure should reflect the domain, not the technical architecture. Domain experts think in features (ordering, billing, shipping), not layers (controllers, services, repositories).

**Example:**
```
# Package by Layer (scattered)
com.app.controller.OrderController
com.app.service.OrderService
com.app.repository.OrderRepository

# Package by Feature (cohesive)
com.app.feature.order.OrderController
com.app.feature.order.OrderService
com.app.feature.order.OrderRepository
```

## Q97: What is the concept of "Testing through the public interface"?

**A:** Testing through the public interface means testing a class only through its public API, treating everything else as an implementation detail. You don't test private methods directly, don't test internal state, and don't depend on how the class implements its behavior. This approach ensures that tests verify the contract (what the class does) rather than the implementation (how it does it). It makes tests resilient to refactoring — internal changes don't break tests.

When you test through the public interface, you can refactor the class's internals freely — change algorithms, optimize data structures, reorganize private methods — without updating any tests. This is the testing equivalent of information hiding. Tests that access private fields or test internal methods are brittle: they break when implementation details change, even if the public behavior is identical. These tests create a maintenance burden and discourage refactoring.

The practical guideline is the "black box" approach: treat the class as a black box, provide inputs through the public API, and verify outputs and observable side effects. If a private method has complex logic worth testing, that logic should be extracted into a separate class with its own public interface, or the class's public interface should expose the behavior differently. Mocking frameworks help by allowing you to mock dependencies rather than reaching into the class's internals. The result is a test suite that validates behavior, survives refactoring, and clearly documents the class's intended use.

**Example:**
```java
class Calculator {
    public int add(int a, int b) { return a + b; }
    private int validate(int x) { /* ... */ }
}

// Good: tests public interface
@Test void testAdd() { assertEquals(5, calc.add(2, 3)); }

// Bad: tests private method directly
// @Test void testValidate() { calc.validate(5); } // don't do this
```

## Q98: What is the concept of "Object Calisthenics" and which rules apply to OOP?

**A:** Object Calisthenics is a set of coding exercises/rules designed to train developers in thinking in objects. Created by Jeff Bay, the rules include: use value objects instead of primitives, limit instance variables to primitive types, wrap all primitives and strings, first-class collections, one dot per line, don't abbreviate, keep all entities small (50 lines max), no classes with more than two instance variables, and no getters/setters. These rules force you to decompose problems into small, focused objects.

The rule to "wrap primitives" means never using raw `int` or `String` for domain concepts — always create a value object. "One dot per line" means avoiding chained method calls like `user.getAddress().getCity().getName()`, which create tight coupling to the internal structure. "No getters/setters" means encapsulating behavior rather than exposing state. "First-class collections" means a `Team` should contain a `PlayerCollection` rather than a `List<Player>`, so you can add behavior to the collection.

Object Calisthenics produce deeply encapsulated, highly cohesive, loosely coupled code. The classes are small, focused, and communicate through well-defined interfaces. The trade-off is verbosity — many small classes instead of a few large ones. This is generally worth it for domain logic, where clarity and correctness matter most. The rules are not rigid laws but training exercises that build good habits. In practice, applying them selectively — wrapping primitives, limiting class size, eliminating getters — yields significant improvements without the overhead of full adherence.

**Example:**
```java
// Before: primitive obsession
class Order {
    String customerName; // primitive
    double totalAmount;  // primitive
}

// After: Object Calisthenics
class Order {
    CustomerName customerName;
    Money totalAmount;
}
```

## Q99: What is the concept of "Hexagonal Architecture" (Ports and Adapters)?

**A:** Hexagonal Architecture, proposed by Alistair Cockburn, separates the application core from external concerns (UI, databases, messaging) through ports and adapters. The application core defines ports (interfaces) that describe what it needs from the outside world. Adapters implement those interfaces to connect the core to specific technologies (PostgreSQL adapter, REST API adapter, email adapter). The core has zero knowledge of external technologies.

The core contains business logic and domain models. Ports define interfaces for inbound operations (driving adapters, like a REST controller that calls the core) and outbound operations (driven adapters, like a database repository that the core calls). Adapters translate between the core's interfaces and external systems. This creates a clean separation: the core is testable in isolation (mock adapters), and adapters can be swapped without touching the core (switch from PostgreSQL to MongoDB by adding a new adapter).

This architecture is the foundation of Clean Architecture, Onion Architecture, and Domain-Driven Design's infrastructure separation. It enables testing the core without external dependencies, swapping technologies without modifying business logic, and developing the core independently from UI and infrastructure. The practical implementation uses dependency inversion: the core defines interfaces (ports), and adapters implement them. The core never imports adapter packages; adapters are wired together by a composition root (application bootstrap).

**Example:**
```java
// Port (interface in core)
interface UserRepository {
    void save(User user);
}

// Adapter (infrastructure)
class PostgresUserRepository implements UserRepository {
    public void save(User user) { /* JDBC logic */ }
}

// Core doesn't know about PostgreSQL
class UserService {
    private final UserRepository repo;
    UserService(UserRepository repo) { this.repo = repo; }
}
```

## Q100: What is the "Stable Dependencies Principle" and how do you enforce it?

**A:** The Stable Dependencies Principle (SDP) states that a module should only depend on modules that are more stable than itself. Stability is measured by the ratio of outgoing dependencies to total dependencies: a module with many outgoing dependencies (depends on many things) is unstable; a module with few outgoing dependencies (many things depend on it) is stable. A module should not depend on unstable modules, because changes in unstable modules will force changes in the dependent module.

Stability metrics: I = Ce / (Ca + Ce), where Ce is afferent coupling (number of modules depending on this one) and Ca is efferent coupling (number of modules this one depends on). I = 0 means maximally stable (nothing depends on it); I = 1 means maximally unstable (depends on many things, nothing depends on it). Abstractions (interfaces, abstract classes) are stable — they change less often than implementations. Following the Dependency Inversion Principle (depend on abstractions) naturally creates stable dependencies.

Enforcing SDP in practice: layer your architecture so that the domain core depends on nothing (or only stable abstractions), application services depend on the domain core, and infrastructure depends on everything else. Use tooling to enforce dependency directions (ArchUnit for Java, Deptrac for PHP, NDepend for C#). These tools scan your codebase and flag violations of declared dependency rules. The result is a codebase where the most stable modules (domain core) are the least likely to change, and the most volatile modules (UI, infrastructure) can change freely without affecting the core.

**Example:**
```java
// Stable: Domain layer depends on nothing
class Order { /* no imports from infrastructure */ }

// Unstable: Infrastructure depends on everything
class OrderRepositoryImpl implements OrderRepository {
    // depends on: OrderRepository (port), JDBC, DataSource
}

// Enforce: architecture test
@Test void domainLayerShouldNotDependOnInfra() {
    noClasses().that().resideIn("..domain..")
        .should().dependOnClassesThat().resideIn("..infra..")
        .check(importedClasses);
}
