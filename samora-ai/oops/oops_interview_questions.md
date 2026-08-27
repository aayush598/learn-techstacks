# OOPS Interview Questions (Top 100)

## 1. What is OOPS?
Object-Oriented Programming System is a paradigm based on objects that contain data and methods.

## 2. What are the main pillars of OOPS?
Encapsulation, Abstraction, Inheritance, Polymorphism.

## 3. What is a class?
A class is a blueprint or template defining properties (attributes) and behaviors (methods).

## 4. What is an object?
An object is an instance of a class with its own state and behavior.

## 5. What is encapsulation?
Binding data and methods together and restricting direct access via access modifiers.

## 6. What is abstraction?
Hiding complex implementation details and exposing only essential features.

## 7. Difference between abstraction and encapsulation.
Abstraction hides complexity (what); encapsulation hides data (how to protect).

## 8. What is inheritance?
A mechanism where a class (child) acquires properties and methods of another (parent).

## 9. What are the types of inheritance?
Single, multiple (via interfaces), multilevel, hierarchical, hybrid.

## 10. What is polymorphism?
The ability of an entity to take many forms, allowing one interface for different types.

## 11. What is compile-time polymorphism?
Achieved via method overloading and operator overloading; resolved at compile time.

## 12. What is runtime polymorphism?
Achieved via method overriding with inheritance and virtual functions; resolved at runtime.

## 13. What is method overloading?
Defining multiple methods with the same name but different parameters in the same class.

## 14. What is method overriding?
A subclass provides a specific implementation of a method already defined in its parent.

## 15. What is a constructor?
A special method called automatically when an object is created, used for initialization.

## 16. What is a destructor?
A method that cleans up resources when an object is destroyed.

## 17. What is a default constructor?
A constructor with no parameters, provided by the compiler if none is defined.

## 18. What is a parameterized constructor?
A constructor that accepts arguments to initialize an object with specific values.

## 19. What is a copy constructor?
A constructor that creates a new object as a copy of an existing object.

## 20. What is this keyword?
'this' refers to the current object instance within a class.

## 21. What is super keyword?
'super' refers to the parent class, used to access its members or constructor.

## 22. What is an abstract class?
A class that cannot be instantiated and may contain abstract methods (no body).

## 23. What is an abstract method?
A method declared without implementation, to be defined by subclasses.

## 24. What is an interface?
A contract specifying methods a class must implement, with no implementation (pure abstraction).

## 25. Difference between abstract class and interface.
Abstract classes can have state and partial implementation; interfaces define only behavior (until default methods).

## 26. What is multiple inheritance?
A class inheriting from more than one class; not supported directly in many languages (for example, Java) due to ambiguity.

## 27. What is the diamond problem?
Ambiguity arising in multiple inheritance when two parent classes inherit from a common grandparent.

## 28. What is a static method?
A method belonging to the class rather than an instance; called without creating an object.

## 29. What is a static variable?
A variable shared by all instances of a class, stored in class memory.

## 30. What is the difference between static and instance methods?
Static belongs to class and cannot access instance members directly; instance operates on an object.

## 31. What is a final class or method?
A final class cannot be inherited; a final method cannot be overridden.

## 32. What is method hiding?
When a subclass defines a static method with the same signature as a parent's static method.

## 33. What is a pure virtual function?
A virtual function with no implementation, forcing subclasses to override (C++).

## 34. What is early binding?
Linking a function call to its definition at compile time (static binding).

## 35. What is late binding?
Resolving a function call at runtime via virtual tables (dynamic binding).

## 36. What is a virtual function?
A function that can be overridden in a derived class and resolved at runtime.

## 37. What is operator overloading?
Defining custom behavior for operators (+, -, etc.) for user-defined types.

## 38. What is function overloading versus overriding?
Overloading is same name different params (compile-time); overriding is redefining inherited method (runtime).

## 39. What is cohesion?
Degree to which class members are related to a single purpose (high cohesion is good).

## 40. What is coupling?
Degree of interdependence between modules (low coupling is desirable).

## 41. What is the difference between composition and aggregation?
Composition is strong ownership (part destroyed with whole); aggregation is weak (part can exist independently).

## 42. What is association?
A relationship between two classes (for example, "uses" or "has-a").

## 43. What is the 'has-a' relationship?
Composition or aggregation representing ownership or use of one object by another.

## 44. What is the 'is-a' relationship?
Inheritance, where a subclass is a specialized form of its parent.

## 45. What is a singleton pattern?
A design pattern ensuring only one instance of a class exists globally.

## 46. What is the factory pattern?
A creational pattern that provides an interface for creating objects without specifying exact classes.

## 47. What is the observer pattern?
A pattern where objects (observers) are notified of changes in a subject automatically.

## 48. What is SOLID principle?
Five design principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.

## 49. Explain Single Responsibility Principle.
A class should have only one reason to change (one responsibility).

## 50. Explain Open-Closed Principle.
Software entities should be open for extension but closed for modification.

## 51. Explain Liskov Substitution Principle.
Subtypes must be replaceable for their base types without altering correctness.

## 52. Explain Interface Segregation Principle.
Clients should not depend on interfaces they do not use; prefer small specific interfaces.

## 53. Explain Dependency Inversion Principle.
High-level modules should not depend on low-level modules; both depend on abstractions.

## 54. What is a design pattern?
A reusable solution to a commonly occurring problem in software design.

## 55. What are creational design patterns?
Patterns dealing with object creation: Singleton, Factory, Builder, Prototype, Abstract Factory.

## 56. What are structural design patterns?
Patterns composing classes: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.

## 57. What are behavioral design patterns?
Patterns managing communication: Observer, Strategy, Command, Template, State, Iterator.

## 58. What is the difference between procedural and OOP?
Procedural focuses on functions and logic; OOP focuses on objects and data encapsulation.

## 59. What is garbage collection?
Automatic memory management reclaiming objects no longer referenced.

## 60. What is a memory leak in OOP?
Unused objects retained by references, preventing garbage collection.

## 61. What is the difference between stack and heap?
Stack stores local variables and calls; heap stores dynamically allocated objects.

## 62. What is an exception?
An event disrupting normal flow, handled via try-catch blocks.

## 63. What is exception handling?
Mechanism to catch and respond to runtime errors gracefully.

## 64. What is the difference between checked and unchecked exceptions?
Checked are verified at compile time; unchecked (runtime) are not.

## 65. What is try-catch-finally?
try contains risky code, catch handles exceptions, finally runs always (cleanup).

## 66. What is throw versus throws?
throw raises an exception; throws declares exceptions a method may propagate.

## 67. What is a namespace or package?
A container grouping related classes to avoid naming conflicts.

## 68. What is polymorphism with real example?
A 'Shape' parent with 'draw()' overridden by Circle, Square — one call, different behavior.

## 69. What is object lifetime?
Creation (constructor) to destruction (garbage collection or destructor).

## 70. What is a reference versus pointer (OOP context)?
A reference is an alias to an object; a pointer holds a memory address (C++).

## 71. What is a shallow copy?
Copying object references so original and copy share nested objects.

## 72. What is a deep copy?
Creating independent copies of all nested objects.

## 73. What is immutability?
An object whose state cannot be changed after creation (for example, String in Java).

## 74. Why use immutable objects?
Thread safety, caching, and predictable behavior.

## 75. What is a record or class in modern OOP?
Records (for example, Java slash C#) are concise immutable data carriers with auto-generated methods.

## 76. What is the difference between class and struct?
Classes are reference types; structs are value types (for example, in C# slash C++).

## 77. What is method signature?
Method name and parameter list (not return type).

## 78. What is a getter and setter?
Methods to read (get) and modify (set) private fields, enforcing encapsulation.

## 79. What is tight versus loose coupling?
Tight means high dependency; loose achieved via interfaces or abstractions for flexibility.

## 80. What is an inner class?
A class defined within another class, with access to outer class members.

## 81. What is an anonymous class?
A class defined and instantiated without a name (for example, Java event handlers).

## 82. What is a lambda expression in OOP?
A concise way to represent an anonymous function, often as a functional interface.

## 83. What is functional interface?
An interface with exactly one abstract method, enabling lambda usage.

## 84. What is the difference between override and overload in C#?
Override redefines inherited virtual method; overload defines same-name methods with different params.

## 85. What is base class and derived class?
Base (parent) is inherited from; derived (child) inherits from base.

## 86. What is a sealed class?
A class that cannot be inherited (similar to final).

## 87. What is dynamic binding?
Associating a method call with method code at runtime (polymorphism).

## 88. What is the difference between abstraction in OOP and abstract class?
Abstraction is a concept; abstract class is a language construct enabling it.

## 89. What is reuse in OOP?
Achieved through inheritance and composition to avoid duplicate code.

## 90. What is a marker interface?
An empty interface used to signal metadata to the compiler or runtime (for example, Serializable).

## 91. What is the difference between equals() and equals ?
 equals compares references (or primitives); equals() compares logical content (overridable).

## 92. What is a hashCode?
An integer representing an object, used in hash-based collections for fast lookup.

## 93. What is the contract between equals and hashCode?
If two objects are equal, they must have the same hashCode; objects with same hash may differ.

## 94. What is the difference between an object and a class variable?
Object (instance) variables are per-instance; class (static) variables are shared.

## 95. What is a constant?
A variable whose value cannot change after initialization (const or final).

## 96. What is the difference between composition and inheritance?
Composition reuses via containment (flexible); inheritance reuses via hierarchy (tight coupling).

## 97. What is the principle of favoring composition over inheritance?
Prefer composing objects to share behavior to reduce fragility and coupling.

## 98. What is a delegate (C#)?
A type-safe function pointer enabling callbacks and event handling.

## 99. What is an event in OOP?
A notification mechanism allowing objects to signal state changes to subscribers.

## 100. How does OOP improve software maintainability?
Through modularity, reusability, encapsulation, and clear abstractions reducing complexity.
