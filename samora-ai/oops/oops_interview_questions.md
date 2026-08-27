# OOPS (Object-Oriented Programming) — 100 Interview Q&A

---

## Q1: What is OOPS?
**A:** Object-Oriented Programming System is a paradigm based on objects that contain data and methods.

## Q2: What are the main pillars of OOPS?
**A:** Encapsulation, Abstraction, Inheritance, Polymorphism.

## Q3: What is a class?
**A:** A class is a blueprint or template defining properties (attributes) and behaviors (methods).

## Q4: What is an object?
**A:** An object is an instance of a class with its own state and behavior.

## Q5: What is encapsulation?
**A:** Binding data and methods together and restricting direct access via access modifiers.

## Q6: What is abstraction?
**A:** Hiding complex implementation details and exposing only essential features.

## Q7: Difference between abstraction and encapsulation.
**A:** Abstraction hides complexity (what); encapsulation hides data (how to protect).

## Q8: What is inheritance?
**A:** A mechanism where a class (child) acquires properties and methods of another (parent).

## Q9: What are the types of inheritance?
**A:** Single, multiple (via interfaces), multilevel, hierarchical, hybrid.

## Q10: What is polymorphism?
**A:** The ability of an entity to take many forms, allowing one interface for different types.

## Q11: What is compile-time polymorphism?
**A:** Achieved via method overloading and operator overloading; resolved at compile time.

## Q12: What is runtime polymorphism?
**A:** Achieved via method overriding with inheritance and virtual functions; resolved at runtime.

## Q13: What is method overloading?
**A:** Defining multiple methods with the same name but different parameters in the same class.

## Q14: What is method overriding?
**A:** A subclass provides a specific implementation of a method already defined in its parent.

## Q15: What is a constructor?
**A:** A special method called automatically when an object is created, used for initialization.

## Q16: What is a destructor?
**A:** A method that cleans up resources when an object is destroyed.

## Q17: What is a default constructor?
**A:** A constructor with no parameters, provided by the compiler if none is defined.

## Q18: What is a parameterized constructor?
**A:** A constructor that accepts arguments to initialize an object with specific values.

## Q19: What is a copy constructor?
**A:** A constructor that creates a new object as a copy of an existing object.

## Q20: What is this keyword?
**A:** 'this' refers to the current object instance within a class.

## Q21: What is super keyword?
**A:** 'super' refers to the parent class, used to access its members or constructor.

## Q22: What is an abstract class?
**A:** A class that cannot be instantiated and may contain abstract methods (no body).

## Q23: What is an abstract method?
**A:** A method declared without implementation, to be defined by subclasses.

## Q24: What is an interface?
**A:** A contract specifying methods a class must implement, with no implementation (pure abstraction).

## Q25: Difference between abstract class and interface.
**A:** Abstract classes can have state and partial implementation; interfaces define only behavior (until default methods).

## Q26: What is multiple inheritance?
**A:** A class inheriting from more than one class; not supported directly in many languages (for example, Java) due to ambiguity.

## Q27: What is the diamond problem?
**A:** Ambiguity arising in multiple inheritance when two parent classes inherit from a common grandparent.

## Q28: What is a static method?
**A:** A method belonging to the class rather than an instance; called without creating an object.

## Q29: What is a static variable?
**A:** A variable shared by all instances of a class, stored in class memory.

## Q30: What is the difference between static and instance methods?
**A:** Static belongs to class and cannot access instance members directly; instance operates on an object.

## Q31: What is a final class or method?
**A:** A final class cannot be inherited; a final method cannot be overridden.

## Q32: What is method hiding?
**A:** When a subclass defines a static method with the same signature as a parent's static method.

## Q33: What is a pure virtual function?
**A:** A virtual function with no implementation, forcing subclasses to override (C++).

## Q34: What is early binding?
**A:** Linking a function call to its definition at compile time (static binding).

## Q35: What is late binding?
**A:** Resolving a function call at runtime via virtual tables (dynamic binding).

## Q36: What is a virtual function?
**A:** A function that can be overridden in a derived class and resolved at runtime.

## Q37: What is operator overloading?
**A:** Defining custom behavior for operators (+, -, etc.) for user-defined types.

## Q38: What is function overloading versus overriding?
**A:** Overloading is same name different params (compile-time); overriding is redefining inherited method (runtime).

## Q39: What is cohesion?
**A:** Degree to which class members are related to a single purpose (high cohesion is good).

## Q40: What is coupling?
**A:** Degree of interdependence between modules (low coupling is desirable).

## Q41: What is the difference between composition and aggregation?
**A:** Composition is strong ownership (part destroyed with whole); aggregation is weak (part can exist independently).

## Q42: What is association?
**A:** A relationship between two classes (for example, "uses" or "has-a").

## Q43: What is the 'has-a' relationship?
**A:** Composition or aggregation representing ownership or use of one object by another.

## Q44: What is the 'is-a' relationship?
**A:** Inheritance, where a subclass is a specialized form of its parent.

## Q45: What is a singleton pattern?
**A:** A design pattern ensuring only one instance of a class exists globally.

## Q46: What is the factory pattern?
**A:** A creational pattern that provides an interface for creating objects without specifying exact classes.

## Q47: What is the observer pattern?
**A:** A pattern where objects (observers) are notified of changes in a subject automatically.

## Q48: What is SOLID principle?
**A:** Five design principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.

## Q49: Explain Single Responsibility Principle.
**A:** A class should have only one reason to change (one responsibility).

## Q50: Explain Open-Closed Principle.
**A:** Software entities should be open for extension but closed for modification.

## Q51: Explain Liskov Substitution Principle.
**A:** Subtypes must be replaceable for their base types without altering correctness.

## Q52: Explain Interface Segregation Principle.
**A:** Clients should not depend on interfaces they do not use; prefer small specific interfaces.

## Q53: Explain Dependency Inversion Principle.
**A:** High-level modules should not depend on low-level modules; both depend on abstractions.

## Q54: What is a design pattern?
**A:** A reusable solution to a commonly occurring problem in software design.

## Q55: What are creational design patterns?
**A:** Patterns dealing with object creation: Singleton, Factory, Builder, Prototype, Abstract Factory.

## Q56: What are structural design patterns?
**A:** Patterns composing classes: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.

## Q57: What are behavioral design patterns?
**A:** Patterns managing communication: Observer, Strategy, Command, Template, State, Iterator.

## Q58: What is the difference between procedural and OOP?
**A:** Procedural focuses on functions and logic; OOP focuses on objects and data encapsulation.

## Q59: What is garbage collection?
**A:** Automatic memory management reclaiming objects no longer referenced.

## Q60: What is a memory leak in OOP?
**A:** Unused objects retained by references, preventing garbage collection.

## Q61: What is the difference between stack and heap?
**A:** Stack stores local variables and calls; heap stores dynamically allocated objects.

## Q62: What is an exception?
**A:** An event disrupting normal flow, handled via try-catch blocks.

## Q63: What is exception handling?
**A:** Mechanism to catch and respond to runtime errors gracefully.

## Q64: What is the difference between checked and unchecked exceptions?
**A:** Checked are verified at compile time; unchecked (runtime) are not.

## Q65: What is try-catch-finally?
**A:** try contains risky code, catch handles exceptions, finally runs always (cleanup).

## Q66: What is throw versus throws?
**A:** throw raises an exception; throws declares exceptions a method may propagate.

## Q67: What is a namespace or package?
**A:** A container grouping related classes to avoid naming conflicts.

## Q68: What is polymorphism with real example?
**A:** A 'Shape' parent with 'draw()' overridden by Circle, Square — one call, different behavior.

## Q69: What is object lifetime?
**A:** Creation (constructor) to destruction (garbage collection or destructor).

## Q70: What is a reference versus pointer (OOP context)?
**A:** A reference is an alias to an object; a pointer holds a memory address (C++).

## Q71: What is a shallow copy?
**A:** Copying object references so original and copy share nested objects.

## Q72: What is a deep copy?
**A:** Creating independent copies of all nested objects.

## Q73: What is immutability?
**A:** An object whose state cannot be changed after creation (for example, String in Java).

## Q74: Why use immutable objects?
**A:** Thread safety, caching, and predictable behavior.

## Q75: What is a record or class in modern OOP?
**A:** Records (for example, Java slash C#) are concise immutable data carriers with auto-generated methods.

## Q76: What is the difference between class and struct?
**A:** Classes are reference types; structs are value types (for example, in C# slash C++).

## Q77: What is method signature?
**A:** Method name and parameter list (not return type).

## Q78: What is a getter and setter?
**A:** Methods to read (get) and modify (set) private fields, enforcing encapsulation.

## Q79: What is tight versus loose coupling?
**A:** Tight means high dependency; loose achieved via interfaces or abstractions for flexibility.

## Q80: What is an inner class?
**A:** A class defined within another class, with access to outer class members.

## Q81: What is an anonymous class?
**A:** A class defined and instantiated without a name (for example, Java event handlers).

## Q82: What is a lambda expression in OOP?
**A:** A concise way to represent an anonymous function, often as a functional interface.

## Q83: What is functional interface?
**A:** An interface with exactly one abstract method, enabling lambda usage.

## Q84: What is the difference between override and overload in C#?
**A:** Override redefines inherited virtual method; overload defines same-name methods with different params.

## Q85: What is base class and derived class?
**A:** Base (parent) is inherited from; derived (child) inherits from base.

## Q86: What is a sealed class?
**A:** A class that cannot be inherited (similar to final).

## Q87: What is dynamic binding?
**A:** Associating a method call with method code at runtime (polymorphism).

## Q88: What is the difference between abstraction in OOP and abstract class?
**A:** Abstraction is a concept; abstract class is a language construct enabling it.

## Q89: What is reuse in OOP?
**A:** Achieved through inheritance and composition to avoid duplicate code.

## Q90: What is a marker interface?
**A:** An empty interface used to signal metadata to the compiler or runtime (for example, Serializable).

## Q91: What is the difference between equals() and equals ?
**A:** equals compares references (or primitives); equals() compares logical content (overridable).

## Q92: What is a hashCode?
**A:** An integer representing an object, used in hash-based collections for fast lookup.

## Q93: What is the contract between equals and hashCode?
**A:** If two objects are equal, they must have the same hashCode; objects with same hash may differ.

## Q94: What is the difference between an object and a class variable?
**A:** Object (instance) variables are per-instance; class (static) variables are shared.

## Q95: What is a constant?
**A:** A variable whose value cannot change after initialization (const or final).

## Q96: What is the difference between composition and inheritance?
**A:** Composition reuses via containment (flexible); inheritance reuses via hierarchy (tight coupling).

## Q97: What is the principle of favoring composition over inheritance?
**A:** Prefer composing objects to share behavior to reduce fragility and coupling.

## Q98: What is a delegate (C#)?
**A:** A type-safe function pointer enabling callbacks and event handling.

## Q99: What is an event in OOP?
**A:** A notification mechanism allowing objects to signal state changes to subscribers.

## Q100: How does OOP improve software maintainability?
**A:** Through modularity, reusability, encapsulation, and clear abstractions reducing complexity.
