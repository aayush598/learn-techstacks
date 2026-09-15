# Java Inheritance, Polymorphism and Interfaces — 100 Interview Q&A

## Q1: What is inheritance in Java and why is it fundamental to OOP?

**A:** Inheritance is a mechanism by which one class (the child or subclass) acquires the fields and methods of another class (the parent or superclass). It models an "is-a" relationship — a `Dog` is-an `Animal`, a `SavingsAccount` is-an `Account`. This is fundamental to OOP because it enables code reuse, establishes hierarchical classification, and is the prerequisite for polymorphism: the ability to treat subclass objects through superclass references.

Java supports single inheritance of implementation (a class can extend exactly one superclass) but allows multiple inheritance of type through interfaces. The `extends` keyword establishes the relationship. At runtime, the JVM maintains a hidden pointer in every object (the "class pointer" or "vtable pointer") that references the actual class, enabling dynamic method dispatch.

The design trade-off is that deep inheritance hierarchies create tight coupling. Changes in a superclass ripple to all descendants. This is why many modern frameworks prefer composition over inheritance — but inheritance remains the correct tool when the is-a relationship is genuine and stable.

## Q2: Explain the difference between `extends` and `implements`.

**A:** `extends` is used between classes (or between interfaces) to establish an inheritance relationship. When a class `B extends A`, `B` inherits all non-private members of `A` and can override its non-final, non-private methods. The relationship is "B is a kind of A."

`implements` is used when a class declares that it fulfills the contract of one or more interfaces. An interface defines a set of method signatures (and possibly default/static methods since Java 8) that the implementing class must provide. A class can implement multiple interfaces: `class ArrayList implements List, RandomAccess, Cloneable`.

The distinction matters at the type level. `extends` between classes creates a subtype with shared implementation. `implements` creates a type constraint — the compiler guarantees the class provides certain operations, but there is no shared implementation unless the interface provides default methods. In practice, you extend for shared behavior and implement for polymorphic contracts.

## Q3: What is method overriding and how does it differ from method overloading?

**A:** Method overriding occurs when a subclass provides its own implementation of a method declared in its superclass. The overriding method must have the same name, same parameter list, and same (or covariant) return type. The `@Override` annotation is used to signal intent and catch signature mismatches at compile time. Overriding is resolved at runtime via dynamic dispatch.

Method overloading occurs when multiple methods in the same class (or inherited methods) share a name but differ in parameter lists. Overloading is resolved at compile time based on the static types of the arguments (compile-time polymorphism or "ad-hoc polymorphism").

Key differences: overriding changes behavior for a specific subclass and requires an is-a relationship; overloading adds convenience by accepting different argument types and has no relationship requirement. You cannot override a method and change the number of parameters — that would be overloading, and the `@Override` annotation would produce a compile error.

```java
class Animal {
    void speak() { System.out.println("..."); }
}

class Dog extends Animal {
    @Override
    void speak() { System.out.println("Woof!"); }

    // Overload — different signature, not overriding
    void speak(String word) { System.out.println("Dog says " + word); }
}
```

## Q4: What rules govern method overriding in Java?

**A:** The rules are strict and enforced at compile time:

1. **Signature matching**: The method name and parameter list must be identical.
2. **Return type**: The return type must be the same or a subtype (covariant return type).
3. **Access modifier**: The overriding method cannot be more restrictive. You can widen from `protected` to `public` but not shrink from `public` to `private`.
4. **Exceptions**: The overriding method cannot throw broader checked exceptions. It can throw narrower exceptions, the same exceptions, or no exceptions at all. Unchecked exceptions can be freely changed.
5. **Static methods**: Cannot be overridden in the true sense — they are hidden. The method that runs depends on the reference type, not the object type.
6. **Final methods**: Cannot be overridden.
7. **Private methods**: Cannot be overridden (they are not visible to subclasses).

Violations produce compile errors. The design ensures the Liskov Substitution Principle: a subclass instance must be usable wherever a superclass instance is expected without breaking contract.

## Q5: What is the Liskov Substitution Principle (LSP) and how does it relate to inheritance?

**A:** The Liskov Substitution Principle states that objects of a superclass should be replaceable with objects of its subclasses without altering the correctness of the program. If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without breaking any guarantees.

A classic violation: a `Square` extending `Rectangle`. If you set width, a square must also change its height — violating the expectation that width and height are independent. The fix is either a separate hierarchy or a design where Square does not extend Rectangle.

LSP constrains what overriding methods can do. Preconditions cannot be strengthened in a subtype (you cannot require more from the caller). Postconditions cannot be weakened (you must deliver at least what the superclass promised). Invariants of the superclass must be preserved. This is why the rules for overriding (narrower exceptions, covariant returns, wider access) exist — they enforce LSP at the language level.

## Q6: Explain covariant return types with an example.

**A:** A covariant return type allows an overriding method to return a subtype of the return type declared in the superclass. Before Java 5, you had to return exactly the same type. Since Java 5, you can narrow the return type.

This is useful in the Builder pattern and factory methods. Consider a `clone()` method or a builder's `self()` method. Without covariant returns, every subclass override would need an explicit cast.

```java
class Vehicle {
    Vehicle create() { return new Vehicle(); }
}

class Car extends Vehicle {
    @Override
    Car create() { return new Car(); }  // covariant return
}

class SportsCar extends Car {
    @Override
    SportsCar create() { return new SportsCar(); }
}

// Usage — no cast needed
Car car = new SportsCar().create(); // returns SportsCar, typed as Car
```

The JVM actually supports covariant returns via bridge methods. The compiler generates a synthetic method with the superclass return type that delegates to the narrower override, ensuring binary compatibility.

## Q7: What is polymorphism and what are its types in Java?

**A:** Polymorphism means "many forms" — the same operation behaves differently on different types. Java supports two primary forms:

**Compile-time polymorphism (static/ad-hoc):** Resolved via method overloading. The compiler selects the method based on the static types and number of arguments. This is not true polymorphism in the OOP sense — it is syntactic sugar.

**Runtime polymorphism (dynamic/subtype):** Resolved via virtual method invocation. A superclass reference pointing to a subclass object invokes the subclass's version of an overridden method. The JVM uses the vtable (virtual method table) to look up the correct implementation at runtime based on the actual object type.

There is also **parametric polymorphism** through generics (`List<T>` works for any `T`), though Java implements this via type erasure rather than true reification. And there is **ad-hoc polymorphism via interfaces**: the same method call (` Comparable.compareTo`) behaves differently for `Integer`, `String`, and any other implementing class.

The power of runtime polymorphism is that client code depends on abstractions, not concrete types. You can add new subclasses without modifying existing code that uses the superclass reference.

## Q8: How does dynamic method dispatch work in the JVM?

**A:** When the JVM encounters an `invokevirtual` instruction, it does not resolve the method to call at compile time. Instead, at runtime, it looks at the actual class of the object (not the declared type of the reference). The class contains a method table (vtable) — an array of method pointers indexed by a fixed ordering of methods. The JVM looks up the method at the same index in the actual class's vtable.

For example, if `Animal.speak()` is at index 2 in `Animal`'s vtable, and `Dog` overrides `speak()`, then `Dog`'s vtable at index 2 points to `Dog.speak()`. When you call `animal.speak()` where `animal` is actually a `Dog`, the JVM finds index 2 in `Dog`'s vtable and invokes `Dog.speak()`.

This is efficient — it is an array lookup, not a hash map search. The vtable is populated when the class is loaded and linked. Interface dispatch (`invokeinterface`) is slightly more expensive because the implementor's table is not as rigidly ordered, but modern JVMs use optimization techniques like itable caching and monomorphic call sites to minimize overhead.

## Q9: What are abstract classes and when should you use them over interfaces?

**A:** An abstract class is declared with the `abstract` keyword and cannot be instantiated. It can contain abstract methods (no body) that subclasses must implement, concrete methods with full implementations, fields, constructors, and any access modifier.

Use an abstract class when:
- You have shared state (fields) that subclasses need.
- You want to provide a template of default behavior (Template Method pattern).
- The hierarchy is genuinely "is-a" and you control it.
- You need constructors to enforce initialization invariants.

Use an interface when:
- You want to define a contract without imposing implementation details.
- You need multiple type relationships.
- You are defining a capability (like `Comparable`, `Serializable`).

Since Java 8, interfaces can have default and static methods, narrowing the gap. But abstract classes can have instance fields, constructors, and maintain state — interfaces cannot have instance fields (only `public static final` constants). The choice often comes down to whether you are modeling identity (abstract class) or capability (interface).

## Q10: Can a class extend multiple classes in Java? Why or why not?

**A:** No. Java enforces single inheritance of implementation. A class can extend exactly one superclass. This was a deliberate design decision by James Gosling to avoid the "diamond problem" that plagues languages like C++.

The diamond problem arises when class D extends both B and C, and both B and C extend A. If B and C both override a method from A, which version does D inherit? C++ resolves this through virtual inheritance and explicit qualification, but it adds significant complexity. Java sidesteps it entirely.

Java's alternative is to allow multiple inheritance of type through interfaces. A class can implement as many interfaces as it needs, gaining multiple type relationships. Since Java 8, interfaces provide default methods, which reintroduces a controlled form of the diamond problem. Java resolves it by requiring the class to explicitly override the ambiguous method (the "class wins" rule) and by preferring class methods over interface default methods.

The practical effect: use `extends` for a single, clear is-a relationship with shared implementation. Use `implements` for multiple behavioral contracts.

## Q11: What happens when a subclass defines a field with the same name as a field in its superclass?

**A:** The field is "hidden," not overridden. Both fields exist in memory — the superclass field is accessible via `super.fieldName` or by casting the reference to the superclass type, while the subclass field shadows it within the subclass's scope.

This is different from method overriding, where only one method exists in the vtable. Fields are resolved at compile time based on the declared type of the reference, not the runtime type of the object. This is a common source of confusion:

```java
class Parent { int x = 10; }
class Child extends Parent { int x = 20; }

Parent p = new Child();
System.out.println(p.x); // prints 10 — resolves to Parent.x at compile time
```

This behavior is one reason why fields should not be declared `protected` without careful thought, and why accessing fields through references instead of `this` or `super` is discouraged. If you need polymorphic field-like behavior, use getter methods.

## Q12: What is the `super` keyword used for?

**A:** The `super` keyword has three primary uses:

1. **Accessing superclass fields**: When a subclass field shadows a superclass field, `super.fieldName` accesses the superclass version.

2. **Calling superclass constructors**: The first statement in a subclass constructor must be either `super(...)` or `this(...)`. If omitted, Java inserts a no-arg `super()` call implicitly. This ensures the superclass portion of the object is properly initialized before the subclass constructor runs.

3. **Invoking overridden methods**: `super.methodName()` calls the superclass's implementation of an overridden method. This is commonly used in the Template Method pattern where the subclass adds behavior before or after calling `super.method()`.

```java
class Logger {
    void log(String msg) { System.out.println("LOG: " + msg); }
}

class FileLogger extends Logger {
    @Override
    void log(String msg) {
        super.log(msg);          // call parent behavior
        writeToFile(msg);        // add subclass behavior
    }
    private void writeToFile(String msg) { /* ... */ }
}
```

The `super` reference is statically bound — it always refers to the immediate superclass, not the actual runtime class. It does not trigger virtual dispatch.

## Q13: What is constructor chaining?

**A:** Constructor chaining is the process of one constructor calling another constructor within the same class (via `this(...)`) or in the superclass (via `super(...)`). Every constructor chain must ultimately call a constructor in `Object`, forming a complete initialization chain.

Within a class, overloaded constructors call each other to avoid code duplication. The canonical constructor does the real work; the others delegate to it with default values.

```java
class User {
    private final String name;
    private final String email;

    User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    User(String name) {
        this(name, "unknown@example.com");  // chains to two-arg constructor
    }
}
```

Across the hierarchy, a subclass constructor must invoke a superclass constructor before accessing `this` or any superclass members. If you do not write `super(...)`, Java inserts `super()`. If the superclass has no accessible no-arg constructor, you must explicitly call `super(args)` with the correct arguments, or the code will not compile.

The order of execution is: `Object` constructor → superclass constructor → subclass constructor. Each level initializes its own fields before passing control up (or down, from the caller's perspective).

## Q14: Can constructors be overridden? Can they be inherited?

**A:** Constructors cannot be overridden. Overriding requires the same signature and is resolved via dynamic dispatch. Constructors do not have a return type (not even `void`), they are not members in the same sense as methods, and they are invoked via `new` or `super`/`this` — never via virtual dispatch.

Constructors are also not inherited by subclasses. If `Parent` has `Parent(String name)` but `Child` declares no constructor, `Child` does not automatically gain `Child(String name)`. You must explicitly define it and call `super(name)`. This is why adding a parameterized constructor to a superclass often breaks subclasses — the implicit no-arg constructor they relied on disappears if you define any constructor at all.

This design enforces that each class explicitly controls its initialization. If constructors were inherited and overridable, a subclass could silently change the initialization logic of a superclass, violating invariants.

## Q15: What is the diamond problem and how does Java handle it?

**A:** The diamond problem occurs when a class inherits from two classes that share a common ancestor, forming a diamond-shaped hierarchy. In Java's single-inheritance model, a class cannot extend two classes, so the diamond problem as class inheritance does not arise.

However, it can appear with interfaces since Java 8 default methods:

```java
interface A {
    default void hello() { System.out.println("A"); }
}

interface B extends A {
    default void hello() { System.out.println("B"); }
}

interface C extends A {
    default void hello() { System.out.println("C"); }
}

// D inherits default hello() from both B and C
interface D extends B, C {
    // Must override to resolve ambiguity
    @Override
    default void hello() { System.out.println("D"); }
}
```

The resolution rules are:
1. Class methods always win over interface default methods.
2. More specific interfaces win (if D extends B and C, and B already overrides A's default, B's version wins over A's).
3. If ambiguity remains, the inheriting type must explicitly override the method.
4. You can also call a specific interface's default via `A.super.hello()`.

These rules make the diamond problem manageable but require explicit resolution when ambiguity persists.

## Q16: What is the difference between `abstract class` and `interface` in Java 17+?

**A:** The distinction has narrowed significantly since Java 8 but key differences remain:

| Feature | Abstract Class | Interface |
|---|---|---|
| Instance fields | Yes | No (only `static final` constants) |
| Constructors | Yes | No |
| Multiple inheritance | Single | Multiple |
| Access modifiers on methods | Any | `public` (implicit since Java 9, private helpers allowed) |
| Default methods | Yes | Yes (since Java 8) |
| Static methods | Yes | Yes (since Java 8) |
| Instance state | Yes | No |
| Sealed (since Java 17) | Yes (`sealed`/`permits`) | Yes (`sealed`/`permits`) |

Use an abstract class when you need to share state, enforce constructor contracts, or control access to fields. Use an interface when you are defining a behavioral contract that unrelated classes can implement. The "is-a vs. can-do" heuristic still applies: a `Dog` is-an `Animal` (abstract class), but a `Dog` can-do `Speakable`, `Trainable`, `Serializable` (interfaces).

## Q17: Explain the `final` keyword in the context of inheritance.

**A:** The `final` keyword restricts modification in three contexts:

1. **Final class**: Cannot be extended. `final class String { ... }` — you cannot create a subclass of `String`. This is used for security (preventing malicious subclassing), immutability guarantees, and performance (the JVM can devirtualize final method calls).

2. **Final method**: Cannot be overridden by any subclass. This locks down the behavior of a specific method. `Object.getClass()` is final — no subclass can change what `getClass()` returns.

3. **Final variable**: The variable can be assigned only once. For reference types, the object's contents can still change, but the reference cannot point to a different object. For primitives, the value is immutable.

In the context of inheritance design, `final` on classes and methods is a powerful tool. It communicates intent ("this will not be extended/overridden"), enables JVM optimizations, and prevents accidental or malicious LSP violations. Overuse, however, makes the API rigid and untestable (you cannot subclass to mock behavior in tests).

## Q18: What is an interface in Java and what can it contain?

**A:** An interface is a reference type that defines a contract — a set of method signatures that implementing classes must fulfill. Since Java 8, interfaces can contain:

1. **Abstract methods** (implicitly `public abstract`): No body; implementors must provide one.
2. **Default methods** (`default` keyword): Provide a method body. Implementing classes inherit the default unless they override it. This was introduced to allow API evolution without breaking existing implementations.
3. **Static methods**: Utility methods called via `InterfaceName.method()`. They do not participate in polymorphism.
4. **Private methods** (since Java 9): Used to share logic between default methods without exposing implementation details.
5. **Constants**: All fields are implicitly `public static final`.
6. **Nested types**: Interfaces can contain inner classes, enums, and other interfaces.

Interfaces cannot have constructors, instance fields, or protected members. They define type identity — `instanceof` checks work against interfaces, and interface references can hold any implementing object. This makes interfaces the primary mechanism for defining abstractions in Java.

## Q19: What are default methods and why were they introduced?

**A:** Default methods (declared with the `default` keyword) provide a method body directly in an interface. They were introduced in Java 8 primarily for API compatibility. Before Java 8, adding a method to an interface broke all existing implementations. Default methods allowed the Java team to add methods like `Iterable.forEach()` and `Collection.stream()` without requiring every implementation to be modified.

They also enable the "mixin" pattern — providing reusable behavior that classes can opt into. `Comparable.thenComparing()` is a default method that builds on the abstract `compareTo()`.

```java
interface Greeting {
    String greet(String name);

    default String formalGreet(String name) {
        return "Dear " + name + ", " + greet(name);
    }
}
```

Default methods have important semantics: they are inherited like any other method, but they are weaker than class methods in conflict resolution. If a class implements two interfaces with conflicting default methods, the class must override the method to resolve the ambiguity. The class's own implementation always wins over any default. This "class wins" rule prevents silent behavioral conflicts.

The downside is that default methods can make interfaces feel like abstract classes, blurring the design line. Use them judiciously — primarily for API evolution and optional behavioral mixins, not for shared state or core logic.

## Q20: What are static methods in interfaces and how do they differ from abstract class static methods?

**A:** Static methods in interfaces (since Java 8) belong to the interface itself, not to any implementing class. They are invoked via `InterfaceName.staticMethod()`. They cannot be overridden or inherited — they are essentially namespace-scoped utility functions.

```java
interface MathUtils {
    static int clamp(int value, int min, int max) {
        return Math.max(min, Math.min(max, value));
    }
}

// Usage
int clamped = MathUtils.clamp(15, 0, 10); // 10
```

The key difference from abstract class static methods: interface static methods are not inherited by implementing classes. If `List` has a static method `of()`, you call `List.of()`, not `arrayList.of()`. Abstract class static methods ARE accessible via subclass references (though accessing them via instance references is a code smell).

Interface static methods serve as factory methods (`List.of()`, `Map.entry()`), utility methods, and companion objects (similar to Scala). They keep related logic co-located with the interface without forcing it onto implementations.

## Q21: What is the difference between `extends` and `implements` for interfaces?

**A:** An interface can `extends` one or more other interfaces, inheriting their abstract and default methods. This creates a sub-interface that is a refinement of the parent interface. For example, `SortedMap extends Map`.

A class `implements` an interface, providing concrete implementations of its abstract methods. A class can implement multiple interfaces simultaneously.

An interface can also `extends` an interface that a class already implements — this is transparent. But an interface cannot `implement` a class (only classes implement interfaces), and a class cannot `extends` an interface (only interfaces extend interfaces).

```java
interface Readable { void read(); }
interface Closeable { void close(); }
interface Resource extends Readable, Closeable { }  // extends multiple

class FileReader implements Resource {
    public void read() { /* ... */ }
    public void close() { /* ... */ }
}
```

The `extends` chain creates a type hierarchy among interfaces. A `Resource` reference can hold any `FileReader`, and a `Readable` reference can hold any `Resource`. This layered typing is powerful for API design — clients can depend on the narrowest interface they need.

## Q22: How do generics interact with interfaces?

**A:** Generics allow interfaces to define type-parameterized contracts. The classic example is `List<E>` — the interface defines operations on elements of type `E`, and each implementation (`ArrayList<E>`, `LinkedList<E>`) works with any reference type.

Generic interfaces enable type safety without casting. `Comparable<T>` requires `compareTo(T)`, so the compiler enforces that you only compare compatible types. `Predicate<T>` defines `test(T)`, and the compiler prevents you from passing a `Predicate<String>` where a `Predicate<Integer>` is expected (invariant matching).

```java
interface Repository<T, ID> {
    T findById(ID id);
    void save(T entity);
    List<T> findAll();
}

class UserRepository implements Repository<User, Long> {
    public User findById(Long id) { /* ... */ }
    public void save(User user) { /* ... */ }
    public List<User> findAll() { /* ... */ }
}
```

The implementing class can choose to be generic itself (`class GenericRepo<T> implements Repository<T, Long>`) or to fix the type parameters as shown above. Generic interfaces are central to the type-safe heterogeneous container pattern and to frameworks like Spring Data.

## Q23: What is a marker interface? Give examples.

**A:** A marker interface is an interface with no methods or constants — it exists solely to signal a property or capability at the type level. The JVM or framework checks `instanceof` to determine behavior.

Examples:
- `java.io.Serializable`: Signals that an object's state can be serialized. The serialization mechanism checks `instanceof Serializable` before attempting to write an object.
- `java.lang.Cloneable`: Signals that `Object.clone()` may be invoked without throwing `CloneNotSupportedException`.
- `java.util.RandomAccess`: Signals that a `List` implementation supports efficient indexed access. `Collections.binarySearch()` uses this to choose between indexed and iterator-based traversal.

Marker interfaces are a form of compile-time type tagging that enables runtime behavioral branching. The alternative (annotations) is more modern but marker interfaces have the advantage of being part of the type system — you can bound generics with them (`<T extends Serializable>`), whereas annotations cannot be used as type bounds.

The trade-off is that marker interfaces are invisible at the API level — there is no method signature revealing their purpose. They can also create accidental constraints: if a library starts checking for a marker interface you did not implement, your code breaks. This is why annotations (`@Override`, `@Deprecated`) are generally preferred for metadata in modern Java.

## Q24: Explain the `instanceof` operator and its pattern-matching variant (Java 16+).

**A:** `instanceof` checks whether an object is an instance of a given type (class or interface). It returns `true` if the object is assignable to the type, including null checks (returns `false` for `null`). It traverses the class hierarchy and interface list to find a match.

Traditional usage requires an explicit cast after the check:

```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}
```

Pattern matching (Java 16+) binds the variable directly:

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

The pattern variable `s` is in scope only within the `true` branch. It also works with logical operators — `obj instanceof String s && s.length() > 5` binds `s` and narrows the condition.

The compiler enforces that pattern variables are definitely assigned — you cannot use `s` in a code path where the `instanceof` check might not have succeeded. This eliminates `ClassCastException` risks and reduces boilerplate. It also works with negative patterns: `!(obj instanceof String s)` makes `s` available in the `false` branch.

## Q25: What is the relationship between generics and type erasure in Java?

**A:** Java implements generics through type erasure — the compiler uses generic type information for compile-time type checking but erases it at runtime. `List<String>` and `List<Integer>` are both just `List` at the JVM level. The compiler inserts implicit casts when you retrieve elements, and the JVM enforces that a `List` cannot hold both types simultaneously (due to the reference typing).

Erasure exists for backward compatibility — pre-generics code (Java 1.4) can interoperate with generic code at the bytecode level. The JVM does not need to be modified to support generics; the compiler does all the work.

The consequences:
1. You cannot use `T.class` or `new T()` — the runtime does not know what `T` is.
2. `instanceof List<String>` is impossible — you can only check `instanceof List`.
3. Generic arrays (`new T[]`) are forbidden — the component type is erased, creating a heap pollution risk.
4. Bridge methods are generated to maintain polymorphism with covariant overrides.

The workarounds include passing `Class<T>` tokens, using `TypeReference` patterns (as in Jackson), and the `Supplier<T>` factory pattern. These reify the type at the usage site even though the generic parameter itself is erased.


## Q26: What is the difference between `List`, `ArrayList`, and `ArrayList<Object>` in terms of type safety?

**A:** `List` is a raw type — it operates without generic type checking. You can add anything, and the compiler inserts unchecked casts. Raw types exist for backward compatibility with pre-generics code and should be avoided.

`ArrayList` (raw) is similarly untyped. `ArrayList<Object>` is the generic form that explicitly states it holds any `Object`. While both allow any reference type, `ArrayList<Object>` is type-safe in the sense that the compiler tracks the type and inserts appropriate casts.

The practical difference: `ArrayList<?>` (wildcard) is read-only for adding (you can only add `null`), while `ArrayList<Object>` is read-write. `List<?>` means "some unknown list type" — you can read elements as `Object` but cannot add anything except `null`. Using raw `List` suppresses all generics checks and produces unchecked warnings.

```java
List raw = new ArrayList();       // unsafe, unchecked warnings
List<Object> safe = new ArrayList<>(); // fully typed
List<?> unknown = getList();       // read-only, type-safe
```

Always prefer parameterized types. Use `List<?>` when you genuinely do not care about the element type and only need read access. Use `List<Object>` when you need to store arbitrary objects.

## Q27: Explain bounded type parameters and their use cases.

**A:** Bounded type parameters restrict the types that can be used as generic arguments. `<T extends Number>` means `T` must be `Number` or a subclass. `<T extends Comparable<T>>` means `T` must implement `Comparable` with itself.

Upper bounds (`extends`) let you call methods defined on the bound without casting. If `T extends Number`, you can call `T.intValue()` directly. Without the bound, you would only have `Object` methods.

```java
<T extends Number & Comparable<T>> T max(List<T> list) {
    T result = list.get(0);
    for (T item : list) {
        if (item.compareTo(result) > 0) result = item;
    }
    return result;
}
```

You can specify multiple bounds with `&` — the first bound is the primary (used for erasure). Lower bounds (`super`) appear in wildcards, not in type parameter declarations. Bounded types are the backbone of the PECS (Producer Extends, Consumer Super) pattern and enable compile-time verified type constraints without runtime overhead.

## Q28: What is the PECS principle and how does it work?

**A:** PECS stands for "Producer Extends, Consumer Super." It is the guideline for when to use `? extends T` versus `? super T` in wildcard types.

If a generic parameter is used to **produce** values (you read from it), use `? extends T`. This means the actual type is some unknown subtype of `T`, so you can safely read `T` values but cannot add anything (except `null`).

If a generic parameter is used to **consume** values (you write to it), use `? super T`. This means the actual type is some unknown supertype of `T`, so you can safely write `T` values but can only read as `Object`.

```java
// Producer — reading from source
void copyAll(List<? extends Number> src, List<? super Number> dest) {
    for (Number n : src) {  // read as Number — safe
        dest.add(n);        // write as Number — safe
    }
}

List<Integer> ints = List.of(1, 2, 3);
List<Number> nums = new ArrayList<>();
copyAll(ints, nums); // compiles — Integer extends Number (producer), Number super Integer (consumer)
```

The `Collections.copy()` and `Collections.sort()` methods use PECS. Without it, `List<Integer>` could not be passed where `List<Number>` is expected (generics are invariant). PECS provides controlled, type-safe flexibility.

## Q29: How does `Object.clone()` work and what are its pitfalls?

**A:** `Object.clone()` creates a shallow copy of the object. It allocates a new instance of the same class and copies all fields bitwise. For primitive fields, this copies the value. For reference fields, this copies the reference — both the original and the clone point to the same object.

To use clone, the class must implement `Cloneable` (a marker interface) and override `clone()` with `public` access (the superclass method is `protected`). Failure to implement `Cloneable` throws `CloneNotSupportedException`.

```java
class Team implements Cloneable {
    String name;
    List<String> members;

    @Override
    public Team clone() {
        try {
            return (Team) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e); // impossible
        }
    }
}
```

Pitfalls:
1. **Shallow copy**: The `members` list is shared. Modifying it in one affects the other.
2. **Final fields**: You cannot set final fields in the clone constructor after `super.clone()` returns. This requires workarounds like reflection or unsafe allocation.
3. **Constructors are skipped**: `super.clone()` does not call any constructor. Invariants enforced by constructors may not hold.
4. **`Cloneable` is broken**: It defines no methods. There is no way for the compiler to enforce correct clone implementation.

For these reasons, many experts (including Joshua Bloch) recommend avoiding `clone()` entirely in favor of copy constructors or static factory methods.

## Q30: What is the difference between a copy constructor and `clone()`?

**A:** A copy constructor takes an instance of the same class and creates a new instance by copying its state: `public User(User other) { this.name = other.name; }`. A `clone()` method copies the object at the bytecode level.

Key differences:

1. **Constructors are called**: A copy constructor is a regular constructor — it can validate, normalize, and enforce invariants. `clone()` skips constructors entirely.
2. **Shallow vs. deep**: `clone()` does a bitwise (shallow) copy by default. A copy constructor can do whatever the programmer specifies — deep copy, defensive copy of mutable fields, etc.
3. **Final fields**: Copy constructors can set final fields (they are assigned in the constructor body). `clone()` cannot set final fields after `super.clone()` returns (without reflection).
4. **Exception handling**: `clone()` throws a checked exception (`CloneNotSupportedException`). Copy constructors do not.
5. **No marker interface needed**: Any class can have a copy constructor. `clone()` requires implementing `Cloneable`.

The consensus in the Java community is to prefer copy constructors (or static factory methods like `copyOf()`) over `clone()`. They are more flexible, safer, and do not suffer from the design problems of `Cloneable`.

## Q31: What is the Template Method pattern and how does it use inheritance?

**A:** The Template Method pattern defines the skeleton of an algorithm in a superclass method, deferring certain steps to subclasses. The superclass method calls abstract or overridable methods at specific points, allowing subclasses to customize behavior without changing the algorithm's structure.

```java
abstract class DataParser {
    final void parse() {  // template method
        readData();
        processData();
        writeOutput();
    }

    abstract void readData();
    abstract void processData();

    void writeOutput() {  // hook with default
        System.out.println("Default output");
    }
}

class CsvParser extends DataParser {
    void readData() { /* read CSV */ }
    void processData() { /* parse CSV */ }
}
```

The template method (`parse`) is typically `final` to prevent subclasses from altering the algorithm's flow. The steps are either abstract (subclasses must implement) or hooks (subclasses may override).

This pattern uses inheritance for its intended purpose — varying parts of a well-defined algorithm. The downside is that it ties subclasses to the superclass hierarchy and can lead to an explosion of subclasses for minor variations. Alternatives include composition (strategy pattern) and lambda callbacks.

## Q32: What is the Strategy pattern and how does it relate to polymorphism?

**A:** The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It uses polymorphism to allow the client to select an algorithm at runtime without changing the context class.

```java
interface SortStrategy {
    void sort(int[] array);
}

class QuickSort implements SortStrategy {
    public void sort(int[] array) { /* quicksort */ }
}

class MergeSort implements SortStrategy {
    public void sort(int[] array) { /* mergesort */ }
}

class Sorter {
    private SortStrategy strategy;

    Sorter(SortStrategy strategy) { this.strategy = strategy; }

    void sort(int[] array) { strategy.sort(array); }
}

// Runtime selection
Sorter sorter = new Sorter(new QuickSort());
sorter.sort(data);
```

Compared to the Template Method pattern (which uses inheritance), Strategy uses composition and interface-based polymorphism. The context class does not extend the strategy — it holds a reference to it. This is more flexible: strategies can be swapped at runtime, tested independently, and combined freely. The Template Method locks the algorithm into the class hierarchy.

The trade-off: Strategy requires more objects and indirection. Template Method is simpler when the algorithm structure is fixed and only a few steps vary.

## Q33: What is the Factory Method pattern and how does it use polymorphism?

**A:** The Factory Method pattern defines an interface for creating objects but lets subclasses decide which class to instantiate. The superclass declares a factory method that returns a product type, and subclasses override it to return concrete products.

```java
abstract class Dialog {
    abstract Button createButton();  // factory method

    void renderDialog() {
        Button btn = createButton();
        btn.render();
    }
}

class WindowsDialog extends Dialog {
    Button createButton() { return new WindowsButton(); }
}

class WebDialog extends Dialog {
    Button createButton() { return new WebButton(); }
}
```

The client (`renderDialog`) depends only on the abstract `Button` type. The concrete product is determined by which `Dialog` subclass is instantiated. This follows the Open/Closed Principle — adding a new platform means adding a new `Dialog` subclass and a new `Button` implementation, without modifying existing code.

The static factory method variant (not the GoF pattern) uses static methods instead of inheritance: `List.of()`, `Map.entry()`. These are simpler but do not leverage polymorphism for extensibility.

## Q34: What is the Dependency Inversion Principle and how do interfaces support it?

**A:** The Dependency Inversion Principle (DIP) states that high-level modules should not depend on low-level modules; both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions.

In practice: a service class should depend on an interface, not a concrete implementation. The concrete implementation is injected (via constructor, setter, or framework) at runtime.

```java
// Violates DIP — high-level depends on low-level
class OrderService {
    private MySqlDatabase db = new MySqlDatabase(); // concrete dependency
}

// Follows DIP — depends on abstraction
class OrderService {
    private final Database db;

    OrderService(Database db) { this.db = db; } // injected dependency
}

interface Database {
    void save(Order order);
}
```

Interfaces enable DIP by decoupling the contract from the implementation. The high-level module knows nothing about `MySqlDatabase`, `PostgresDatabase`, or `InMemoryDatabase` — it only knows `Database`. This makes the system testable (inject a mock `Database`), maintainable (swap implementations), and modular (implementations can be developed independently).

DIP is the "D" in SOLID and is foundational to dependency injection frameworks like Spring. Without interfaces, DIP is impossible because the high-level module would be locked to concrete types.

## Q35: What are the SOLID principles and how do they relate to inheritance and interfaces?

**A:** SOLID is an acronym for five design principles:

1. **Single Responsibility Principle (SRP)**: A class should have one reason to change. Interfaces help by separating concerns — a class can implement multiple interfaces, each representing a single responsibility.

2. **Open/Closed Principle (OCP)**: Open for extension, closed for modification. Inheritance and interfaces enable this: you add new subclasses or implementations without changing existing code.

3. **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types. This constrains how inheritance is used — overriding methods must preserve the superclass contract.

4. **Interface Segregation Principle (ISP)**: Clients should not depend on interfaces they do not use. Prefer many small, focused interfaces over one large "fat" interface.

5. **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions. Interfaces are the primary mechanism for achieving this.

Inheritance (via `extends`) is central to OCP and LSP. Interfaces are central to ISP and DIP. Together, they form the toolkit for building maintainable, extensible OOP systems. Violations — like using inheritance for code reuse rather than polymorphism, or creating God interfaces with dozens of methods — lead to rigid, fragile designs.

## Q36: Explain the composition-over-inheritance principle with a Java example.

**A:** Composition-over-inheritance advocates building complex functionality by composing objects (holding references) rather than inheriting from them. Instead of `class ArrayList extends AbstractList`, you might wrap a `List` and delegate calls.

```java
// Inheritance approach
class StatisticsTracker extends ArrayList<DataPoint> {
    double average() {
        return stream().mapToDouble(DataPoint::value).average().orElse(0);
    }
}

// Composition approach
class StatisticsTracker {
    private final List<DataPoint> data = new ArrayList<>();

    void add(DataPoint dp) { data.add(dp); }
    double average() {
        return data.stream().mapToDouble(DataPoint::value).average().orElse(0);
    }
}
```

Advantages of composition:
1. **Flexibility**: You can change the internal `List` implementation without affecting the public API.
2. **Encapsulation**: You expose only the methods you want. The inheritance approach exposes all `ArrayList` methods, including `remove(int)`.
3. **No fragile base class problem**: Changes to `ArrayList` (like behavior changes in `remove`) would affect `StatisticsTracker` if it extended `ArrayList`.
4. **Testability**: You can easily mock the internal `List` in unit tests.

Use inheritance when the is-a relationship is genuine and the subclass truly is a specialization of the superclass. Use composition when you want to reuse behavior or delegate functionality.

## Q37: What is the fragile base class problem?

**A:** The fragile base class problem occurs when changes to a base class inadvertently break subclasses. Since subclasses depend on the implementation details (not just the contract) of the base class, even well-intentioned changes can have cascading effects.

Example: a base class `ArrayList` adds a new method `addIfAbsent()`. If a subclass happens to have a method with that name but different semantics, the subclass's behavior silently changes. Or if the base class optimizes an internal loop, subclasses that override `size()` or `get(int)` to maintain auxiliary data structures (like an index) may break.

This is why the `@Override` annotation is critical — it catches when a superclass method signature changes. But it cannot protect against semantic changes (the method does the same thing differently).

Mitigation strategies:
1. **Document the contract** (not just the API). Use Javadoc to specify invariants, preconditions, and postconditions.
2. **Use final on non-virtual methods** to prevent subclasses from depending on implementation details.
3. **Prefer composition** when the subclass does not truly need to extend the base class.
4. **Program to an interface** so that the implementation can be swapped without affecting dependent code.

## Q38: What is the Composition pattern (as opposed to Inheritance) for code reuse?

**A:** The Composition pattern achieves code reuse by delegating to contained objects rather than inheriting from them. Instead of extending `Observable`, you hold an `Observable` field and forward relevant calls.

This is sometimes called "Forwarding" or "Decorating." The `Collections.synchronizedList()` method wraps a `List` and adds synchronization — it does not extend `ArrayList`.

```java
class SynchronizedList<E> implements List<E> {
    private final List<E> delegate;
    private final Object lock;

    SynchronizedList(List<E> delegate) {
        this.delegate = delegate;
        this.lock = this;
    }

    @Override
    public boolean add(E e) {
        synchronized (lock) { return delegate.add(e); }
    }

    @Override
    public E get(int index) {
        synchronized (lock) { return delegate.get(index); }
    }
    // ... delegate all other methods
}
```

The advantage is that the wrapper can decorate any `List` implementation, not just a specific one. You can stack decorators (synchronized + unmodifiable). The disadvantage is boilerplate — you must implement or forward every interface method. Libraries like Google Guava's `ForwardingList` provide base forwarding classes to reduce this boilerplate.

## Q39: What is an adapter pattern and how does it use interfaces?

**A:** The Adapter pattern converts the interface of one class into an interface that a client expects. It allows classes with incompatible interfaces to work together.

```java
// Legacy system
class XmlDataProcessor {
    void processXml(String xml) { /* ... */ }
}

// Modern interface
interface DataProcessor {
    void process(byte[] data);
}

// Adapter
class XmlAdapter implements DataProcessor {
    private final XmlDataProcessor legacy = new XmlDataProcessor();

    @Override
    public void process(byte[] data) {
        String xml = new String(data, StandardCharsets.UTF_8);
        legacy.processXml(xml);
    }
}
```

The adapter holds a reference to the adaptee (composition) and implements the target interface (polymorphism). The client calls `DataProcessor.process()` and does not know (or care) that the actual work is done by an XML processor.

This is a bridge between incompatible worlds — new code depends on the modern interface, old code continues to work unchanged, and the adapter translates between them. It is heavily used in integration scenarios, API migrations, and third-party library wrapping.

## Q40: What is the Decorator pattern and how does it differ from subclassing?

**A:** The Decorator pattern dynamically adds responsibilities to objects by wrapping them in decorator classes that implement the same interface. Unlike subclassing, which adds behavior at compile time for a specific type, decorators can be stacked and combined at runtime.

```java
interface Coffee {
    double cost();
    String description();
}

class SimpleCoffee implements Coffee {
    public double cost() { return 2.0; }
    public String description() { return "Simple coffee"; }
}

abstract class CoffeeDecorator implements Coffee {
    protected final Coffee coffee;
    CoffeeDecorator(Coffee coffee) { this.coffee = coffee; }
}

class MilkDecorator extends CoffeeDecorator {
    MilkDecorator(Coffee coffee) { super(coffee); }
    public double cost() { return coffee.cost() + 0.5; }
    public String description() { return coffee.description() + ", milk"; }
}

// Usage
Coffee coffee = new MilkDecorator(new SimpleCoffee());
```

Subclassing creates `MilkCoffee extends SimpleCoffee` — you cannot add milk twice, and you cannot remove it. Decorators can be combined: `new MilkDecorator(new SugarDecorator(new SimpleCoffee()))`.

The key insight: both the decorator and the original implement the same interface, so the client sees a uniform API. The decorator adds behavior (before or after) and delegates the core operation to the wrapped object. This is more flexible than inheritance but creates more objects and can be harder to debug (deep decorator stacks).

## Q41: What is the Proxy pattern and how does it relate to interfaces?

**A:** The Proxy pattern provides a surrogate or placeholder for another object to control access to it. The proxy implements the same interface as the real object, so the client cannot distinguish between them.

Types of proxies:
- **Virtual proxy**: Lazy-loads the real object (e.g., loading a large image only when first accessed).
- **Protection proxy**: Checks access permissions before delegating.
- **Remote proxy**: Represents an object in a different address space (RMI).
- **Logging/AOP proxy**: Adds cross-cutting concerns (logging, transaction management).

```java
interface Image {
    void display();
}

class RealImage implements Image {
    RealImage(String file) { loadFromDisk(file); }
    public void display() { System.out.println("Displaying"); }
}

class LazyImageProxy implements Image {
    private RealImage real;
    private final String file;

    LazyImageProxy(String file) { this.file = file; }

    public void display() {
        if (real == null) real = new RealImage(file);
        real.display();
    }
}
```

Spring AOP uses dynamic proxies (JDK dynamic proxies or CGLIB) to wrap beans with cross-cutting logic. The JDK dynamic proxy mechanism requires the target to implement an interface — it generates a proxy class at runtime that implements the same interface. CGLIB can proxy classes without interfaces by subclassing them.

## Q42: What are JDK dynamic proxies and when would you use them?

**A:** JDK dynamic proxies create proxy classes at runtime using `java.lang.reflect.Proxy`. The proxy implements a specified set of interfaces and delegates all method calls to an `InvocationHandler`. This enables AOP-style programming without requiring the target class to be designed for proxying.

```java
interface Greeting {
    String hello(String name);
}

class RealGreeting implements Greeting {
    public String hello(String name) { return "Hello, " + name; }
}

class LoggingHandler implements InvocationHandler {
    private final Object target;
    LoggingHandler(Object target) { this.target = target; }

    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("Calling " + method.getName());
        Object result = method.invoke(target, args);
        System.out.println("Method returned " + result);
        return result;
    }
}

Greeting proxy = (Greeting) Proxy.newProxyInstance(
    Greeting.class.getClassLoader(),
    new Class[]{Greeting.class},
    new LoggingHandler(new RealGreeting())
);
proxy.hello("Alice"); // logs entry and exit
```

Use cases: logging, security checks, transaction management, retry logic, lazy loading, and remote method invocation. Spring uses this pattern extensively — every `@Transactional` bean method is wrapped in a proxy that begins and commits a transaction.

The limitation: JDK dynamic proxies work only with interfaces. For classes without interfaces, CGLIB generates a subclass at runtime as the proxy. Spring Boot defaults to CGLIB for this reason.

## Q43: Explain the concept of type erasure in detail with its practical implications.

**A:** Type erasure is the process by which the compiler removes all generic type information from the bytecode. `List<String>` becomes `List` at runtime. The compiler inserts bridge methods and explicit casts to maintain type safety.

Practical implications:

1. **No runtime type checks**: You cannot do `if (list instanceof List<String>)`. The JVM only sees `List`.
2. **No generic arrays**: `new T[]` is forbidden because the component type is unknown at runtime. `new Object[]` and a cast is the workaround.
3. **No `new T()`**: You cannot instantiate a generic type parameter. Pass a `Class<T>` or `Supplier<T>` instead.
4. **Bridge methods**: When a generic class overrides a method with a specialized return type, the compiler generates a bridge method with the erasured signature that delegates to the specialized version.

```java
class Container<T> {
    T value;
    T get() { return value; }
}

class StringContainer extends Container<String> {
    @Override
    String get() { return super.get(); }  // returns String

    // Compiler generates:
    // bridge: Object get() { return this.get(); } // delegates to String get()
}
```

5. **Manifest types**: You can recover generic types via reflection in certain contexts: `field.getGenericType()`, `method.getGenericReturnType()`, `ParameterizedType`. Frameworks like Jackson and Gson use this to deserialize into the correct generic type.

6. **Annotation processing**: Generic type information is available at compile time for annotation processors but lost at runtime. This is why annotation processors can inspect generic types but runtime reflection cannot (in most cases).

## Q44: What is a reified type and why doesn't Java have reified generics?

**A:** A reified type retains its full type information at runtime. If Java had reified generics, `List<String>` and `List<Integer>` would be distinct classes at runtime, and you could do `instanceof List<String>`, `new T[]`, and `T.class`.

Java chose type erasure for backward compatibility. When generics were added in Java 5, the JVM was not modified. All generic code had to work with existing bytecode. This meant generics had to be implemented purely as a compile-time construct.

Languages like C# have reified generics (called "real" generics or "CLR generics") because the runtime was designed with generics from the start. C++ templates are also reified — the compiler generates separate code for each template instantiation.

The cost of reified generics: larger class files (each instantiation generates a new class), more complex runtime, and difficulty with certain type-level programming patterns. The benefit: full runtime type information, no casting, no bridge methods, no generic array restrictions.

Java could add reified generics in the future (Project Valhalla explores value types with special generic handling), but it would require significant JVM changes. For now, the workarounds (`Class<T>` tokens, `TypeReference` patterns) are the standard approach.

## Q45: What is the diamond problem with default methods in detail?

**A:** Consider:

```java
interface A { default void hello() { System.out.println("A"); } }
interface B extends A { /* inherits A's hello */ }
interface C extends A { default void hello() { System.out.println("C"); } }
class D implements B, C { }
```

The question: which `hello()` does `D` get?

Java's resolution:
1. **Class wins over interface**: If `D` had a `hello()` method, it would win. It does not, so we continue.
2. **Most specific interface wins**: `C.hello()` is more specific than `A.hello()` because `C` directly overrides it. `B` does not override `A.hello()`, so `B` does not contribute. `C` wins.

If both `B` and `C` independently override `A.hello()`, neither is more specific than the other, and `D` must override `hello()` to resolve the ambiguity. The compiler produces an error: "class D inherits unrelated defaults for hello() from types B and C."

You can also explicitly choose: `C.super.hello()` calls `C`'s version, `B.super.hello()` calls `A`'s version (through `B`, which did not override). This explicit qualification is always available.

The key principle: Java prefers concrete implementations (class methods) over default methods, and more specific interfaces over more general ones. The compiler forces explicit resolution when ambiguity is irreconcilable.

## Q46: How do interfaces support multiple inheritance of type?

**A:** A class can implement multiple interfaces, and each interface represents a distinct type. This means an object can be assigned to variables of any of its interface types.

```java
interface Payable { void pay(); }
interface Serializable { /* marker */ }
interface Comparable<T> { int compareTo(T other); }

class Employee implements Payable, Serializable, Comparable<Employee> {
    public void pay() { /* ... */ }
    public int compareTo(Employee other) { return this.name.compareTo(other.name); }
}

Employee e = new Employee();
Payable p = e;       // ok — Employee is-a Payable
Serializable s = e;  // ok — Employee is-a Serializable
Comparable<Employee> c = e; // ok — Employee is-a Comparable<Employee>
```

This is "multiple inheritance of type" — `Employee` inherits three distinct types. The JVM's type system tracks all implemented interfaces, and `instanceof` checks work for any of them.

The practical value: code that depends on `Payable` does not need to know about `Employee` specifically. You can have `List<Payable>` containing `Employee`, `Contractor`, and `Vendor` objects, each with different implementations. This is the essence of programming to interfaces — the power of polymorphism amplified by multiple type relationships.

## Q47: What is the difference between checked and unchecked exceptions in the context of overriding?

**A:** When overriding a method, the overriding method can declare:

- **No exceptions**: Always allowed.
- **The same checked exceptions**: Allowed.
- **Subtypes of the declared checked exceptions**: Allowed (narrower).
- **Broader checked exceptions**: Not allowed — compile error.
- **Any unchecked exceptions** (RuntimeException, Error): Always allowed, regardless of what the superclass declares.

```java
class Base {
    void process() throws IOException { }
}

class Sub extends Base {
    @Override
    void process() throws FileNotFoundException { } // narrower — ok

    @Override
    void process() throws SQLException { } // compile error — not a subtype of IOException

    @Override
    void process() throws IllegalArgumentException { } // ok — unchecked
}
```

The rationale: if a client catches `IOException`, it expects the method to throw only `IOException` or its subtypes. If the override could throw `SQLException`, the client's catch block would miss it, breaking error handling. The Liskov Substitution Principle enforces that subtypes do not weaken the error-handling contract.

This applies to `throws` declarations, not to actual exceptions thrown. A method declared with no exceptions can still throw unchecked exceptions (which are not declared). The compiler only enforces checked exception declarations.

## Q48: What is the role of `Object` in Java's type hierarchy?

**A:** `java.lang.Object` is the root of the class hierarchy — every class implicitly or explicitly extends `Object`. It provides the fundamental methods that every object has:

1. `equals(Object)`: Logical equality (must be overridden for value-based comparison).
2. `hashCode()`: Hash value (must be consistent with `equals`).
3. `toString()`: String representation.
4. `getClass()`: Returns the runtime class (final — cannot be overridden).
5. `clone()`: Shallow copy (protected — requires `Cloneable`).
6. `finalize()`: Called by garbage collector before collection (deprecated since Java 9).
7. `wait()`, `notify()`, `notifyAll()`: Thread coordination (inherent monitor mechanism).

Because `Object` is the superclass of everything, a variable of type `Object` can hold any reference. This is useful for generic containers that must hold arbitrary types, but it is also why generics were introduced — `Object`-typed containers require casting and lose type safety.

`Object` also defines the contract for `equals`/`hashCode`/`toString` that all classes inherit. The correctness of hash-based collections (`HashMap`, `HashSet`) depends on classes properly implementing `equals` and `hashCode`.

## Q49: How do `equals()` and `hashCode()` relate to inheritance?

**A:** If you override `equals()`, you must override `hashCode()`. The contract: objects that are equal must have the same hash code. If they do not, hash-based collections (`HashMap`, `HashSet`) will fail — an equal object might not be found because it is placed in a different bucket.

```java
class Employee {
    private final String id;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Employee)) return false;
        return id.equals(((Employee) o).id);
    }

    @Override
    public int hashCode() { return id.hashCode(); }
}
```

Inheritance complicates this: if `Employee` extends `Person` and both override `equals`, which version runs? The subclass version should incorporate the superclass's `equals` logic via `super.equals(o)`:

```java
@Override
public boolean equals(Object o) {
    if (!super.equals(o)) return false;
    Employee other = (Employee) o;
    return this.id.equals(other.id);
}
```

If you only check the subclass fields, two objects could be "equal" in the subclass but different in the superclass fields. The superclass `equals` might compare different fields. Always delegate to `super` when composing equality checks across the hierarchy.

## Q50: What are covariant and contravariant types in Java generics?

**A:** Java generics are **invariant**: `List<Integer>` is NOT a subtype of `List<Number>`, even though `Integer` is a subtype of `Number`. This is the default behavior, and it is safe — you cannot add a `Double` to a `List<Integer>` through a `List<Number>` reference.

**Covariance** (read-only) is achieved with upper wildcards: `List<? extends Number>`. This means "a list of some unknown subtype of Number." You can read `Number` values from it but cannot add anything (except null). It is covariant because `List<Integer>` IS assignable to `List<? extends Number>`.

**Contravariance** (write-only) is achieved with lower wildcards: `List<? super Integer>`. This means "a list of some unknown supertype of Integer." You can add `Integer` values but can only read as `Object`. It is contravariant because `List<Number>` IS assignable to `List<? super Integer>`.

The mnemonic is PECS (Producer Extends, Consumer Super):
- **Producer** (you read from it): use `extends` — the source produces values.
- **Consumer** (you write to it): use `super` — the sink consumes values.
- **Both**: use exact types (`List<Integer>`).

This system provides type-safe variance without requiring the complex declaration-site variance annotations of languages like Kotlin (`out`/`in`) or Scala (`+`/`-`). The trade-off is verbosity at usage sites, but the safety guarantees are identical.


## Q51: Explain the difference between `List`, `List<?>`, `List<Object>`, and a raw `List`.

**A:** These four forms have distinct semantics:

- **`List` (raw type)**: No generic type checking. You can add any `Object`. All retrievals return `Object` (or require unchecked casts). Exists for backward compatibility with pre-generics code. Produces unchecked warnings.

- **`List<Object>`**: Fully typed. The type parameter is `Object`, so you can add any reference. Retrievals return `Object`. This is a concrete, reifiable type — you can do `instanceof List<Object>` (though it is not recommended).

- **`List<?>`** (unbounded wildcard): Read-only in practice. You can read elements as `Object` but cannot add anything except `null`. It means "some list of unknown type." Useful as a method parameter when you only need to read from the list. You can do `instanceof List<?>` but not `instanceof List<String>`.

- **`List<String>`** (parameterized type): Type-safe for a specific element type. You can add `String`s and retrieve `String`s. The compiler enforces the constraint.

```java
void inspect(List<?> list) {
    Object item = list.get(0);      // ok
    // list.add("x");              // compile error
    list.add(null);                 // ok — null is valid for any type
}

void addAll(List<Object> dest, List<?> src) {
    for (Object item : src) dest.add(item); // ok
}
```

The choice depends on intent: `List<Object>` for storing heterogeneous objects, `List<?>` for read-only access to unknown types, raw `List` only for legacy interop, and `List<Something>` for typed collections.

## Q52: What is capture conversion and why is it needed for wildcards?

**A:** When you assign a wildcard type to a type variable, Java performs capture conversion. It creates a fresh type variable (the "capture") that represents the unknown actual type. This prevents you from circumventing wildcard restrictions through clever variable assignments.

Consider: `List<?> list = new ArrayList<String>()`. The compiler creates a capture type `CAP#1` such that `list` is of type `List<CAP#1>`. You can read `CAP#1` (as `Object`) but cannot add to the list because the compiler does not know what `CAP#1` is.

Without capture conversion, you could write:
```java
List<?> list = new ArrayList<String>();
List<Object> ref = list;  // should NOT compile
```

Capture conversion prevents this — `List<CAP#1>` is not assignable to `List<Object>` because `CAP#1` is an unknown type. The wildcard preserves type safety by restricting what you can do with the reference.

Capture conversion also enables more flexible wildcard patterns:
```java
void swap(List<?> list) {
    // Without capture, you cannot even read and re-add elements
    // With capture, the compiler knows all elements share the same unknown type
}
```

The JVM does not know about capture types — they exist only during compilation. This is why `List<?>` and `List<CAP#1>` are both just `List` at runtime.

## Q53: What are intersection types and where do they appear in Java?

**A:** Intersection types are compound type constraints of the form `A & B & C`. They appear in two contexts:

1. **Bounded type parameters**: `<T extends Comparable<T> & Serializable>` — `T` must implement both interfaces.

2. **Cast expressions**: `(Comparable & Serializable) obj` — the cast checks both types simultaneously. This is rarely needed but can be useful.

3. **Lambda expressions and method references**: The compiler infers an intersection type for the target type. A lambda assigned to `Comparator<String>` also satisfies `Serializable` because the generated class implements both. The compiler creates a synthetic intersection type `Comparator<String> & Serializable`.

```java
// The compiler infers that this lambda is both Comparator and Serializable
Comparator<String> comp = (a, b) -> a.compareTo(b);
Serializable s = comp; // compiles — the lambda implements both
```

Intersection types enable pattern matching with generics. For example, `<T extends Comparable<T> & Serializable>` ensures `T` can be compared and serialized. The erasure uses the first bound (`Comparable`) for runtime type checks.

In type inference, intersection types are used during overload resolution. If a method parameter is `<T extends Number & Comparable<T>>`, the compiler infers the intersection of candidate types to find the most specific applicable method.

## Q54: What is the "super type token" pattern and why is it needed?

**A:** Due to type erasure, you cannot recover generic type parameters at runtime through normal means. `List<String>` and `List<Integer>` are both `List` at runtime. The super type token pattern uses an anonymous subclass to reify the generic type.

```java
abstract class TypeReference<T> {
    private final Type type;

    protected TypeReference() {
        Type superclass = getClass().getGenericSuperclass();
        ParameterizedType pt = (ParameterizedType) superclass;
        this.type = pt.getActualTypeArguments()[0];
    }

    public Type getType() { return type; }
}

// Usage
TypeReference<List<String>> ref = new TypeReference<List<String>>() {};
Type type = ref.getType(); // returns ParameterizedType for List<String>
```

The trick: creating an anonymous subclass of `TypeReference<List<String>>` preserves the generic type information in the class's metadata. At runtime, `getGenericSuperclass()` returns a `ParameterizedType` with the full `List<String>` type argument. This is how Jackson's `TypeReference<Map<String, List<Integer>>>` works for deserialization.

The pattern works because generic type information is stored in class metadata (the `Signature` attribute in bytecode), even though it is erased from the runtime type system. Reflection can access class metadata, so the super type token provides a workaround for type erasure.

## Q55: Explain the Visitor pattern and how it leverages interface polymorphism.

**A:** The Visitor pattern represents an operation to be performed on elements of an object structure. It separates the algorithm from the object structure by defining a visitor interface with a `visit` method for each element type.

```java
interface Visitor {
    void visit(TextNode node);
    void visit(ImageNode node);
    void visit(LinkNode node);
}

interface Element {
    void accept(Visitor visitor);
}

class TextNode implements Element {
    String text;
    public void accept(Visitor visitor) { visitor.visit(this); }
}

class HtmlExportVisitor implements Visitor {
    public void visit(TextNode node) { /* export as <p> */ }
    public void visit(ImageNode node) { /* export as <img> */ }
    public void visit(LinkNode node) { /* export as <a> */ }
}
```

The double dispatch mechanism: `node.accept(visitor)` dispatches based on the node type (first dispatch), and `visitor.visit(this)` dispatches based on the visitor type (second dispatch). This achieves type-safe dispatch on two types simultaneously — something single dispatch (virtual methods) cannot do.

Use cases: compilers (AST traversal), serialization (different output formats), document processing. The downside: adding a new element type requires modifying all visitor implementations. This is the Expression Problem — Visitor makes it easy to add new operations but hard to add new types.

## Q56: What is the Expression Problem and how do Java's features address it?

**A:** The Expression Problem is the challenge of adding new variants (types) and new operations to a data type simultaneously, without modifying existing code. In OOP, adding a new subclass is easy (add a class). Adding a new operation means modifying every existing subclass (adding a method to each). In FP, adding a new function is easy (write a new function). Adding a new variant means modifying every existing function (adding a case to each).

Java's approach:
1. **Interfaces + polymorphism**: New types (implementations) are easy — add a class that implements the interface. New operations require modifying existing code or adding default methods to the interface (Java 8+).
2. **Sealed classes + pattern matching** (Java 17+): `switch` on sealed types with exhaustive matching allows the compiler to enforce that all cases are handled. When you add a new type, the compiler flags every switch that needs updating. This makes the "new operation" side easier.
3. **Default methods**: Can add new operations to interfaces without breaking existing implementations, but the implementation has access only to the interface's methods, not the concrete type's fields.

No single mechanism fully solves the Expression Problem in Java. Sealed classes with pattern matching get closest — they provide exhaustive, compiler-checked dispatch similar to algebraic data types in FP, while still allowing extensible class hierarchies. The trade-off is between extensibility (open class hierarchies) and exhaustiveness (sealed types + switch).

## Q57: What are extension methods in Kotlin and how do they compare to Java default methods?

**A:** Extension functions in Kotlin let you add methods to existing classes without modifying them or using inheritance. They are defined as top-level functions with a receiver type:

```kotlin
fun String.isEmail(): Boolean = matches(Regex("^[\\w.-]+@[\\w.-]+\\.\\w+$"))

"test@example.com".isEmail() // true
```

Java default methods serve a similar purpose but with key differences:

| Feature | Kotlin Extension | Java Default Method |
|---|---|---|
| Defined in | Any file (top-level) | Interface only |
| Receiver access | Public + protected members | Only interface methods |
| This/receiver | `this` is the receiver | `this` is the interface |
| No state | Correct (same as default) | Correct |
| Override by implementors | N/A | Yes (default can be overridden) |
| Resolution | Static (compile-time) | Dynamic (vtable) |

Kotlin extensions are resolved statically — the extension function called depends on the declared type, not the runtime type. This means they do not participate in polymorphism. Java default methods participate in dynamic dispatch — the actual implementation depends on the runtime type of the object.

Extensions are syntactic sugar: `"test".isEmail()` compiles to `StringUtils.isEmail("test")`. Default methods are actual interface methods with a body. Extensions are more flexible (any class, any file) but less polymorphic. Default methods are more integrated with the type system but limited to interfaces.

## Q58: What is the Expression Problem in Java and how do sealed classes help?

**A:** The Expression Problem is the difficulty of adding both new data variants and new operations to a closed data type without recompiling existing code. It was named by Philip Wadler.

In traditional Java OOP:
- **Adding a new type** (variant): Create a new class implementing the interface. Existing operations do not need modification (they depend on the interface). Easy.
- **Adding a new operation**: Add a method to the interface. All implementing classes must be updated. Hard — you cannot add a method to an interface without modifying every implementation (unless you use default methods, which have limitations).

Sealed classes with pattern matching (Java 17+) change the calculus. A sealed class with `permits` restricts which classes can extend it. When you write a `switch` expression over a sealed type, the compiler enforces exhaustiveness — you must handle every permitted subtype. When a new subtype is added, the compiler flags every non-exhaustive switch that needs updating.

```java
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
        // Triangle case needed if Triangle is added — compiler enforces
    };
}
```

This gives you the FP-style exhaustive pattern matching with the extensibility of OOP. New types are easy (add a class, update switches). New operations are easy (write a new switch). The sealed constraint ensures the compiler can verify completeness.

## Q59: Explain the concept of structural typing vs. nominal typing in Java.

**A:** **Nominal typing** means type compatibility is determined by explicit declarations (names). Java is nominally typed: to implement `Comparable`, you must explicitly `implements Comparable`. Two classes with identical method signatures are not compatible unless they share an explicit inheritance relationship.

**Structural typing** means type compatibility is determined by the shape of the type — its methods and fields. If two types have the same methods, they are interchangeable regardless of their names or inheritance. Go interfaces are structural: any type with the right methods implicitly satisfies the interface.

Java uses nominal typing everywhere:
- `class`/`extends`/`implements` — explicit declaration.
- No implicit interface satisfaction — you must declare `implements`.
- `instanceof` checks nominal hierarchy.

This is a deliberate design choice. Nominal typing is more explicit and predictable — you know exactly what a type implements by looking at its declaration. Structural typing is more flexible — you can create adapters without explicit boilerplate, and unrelated types can satisfy the same contract.

Scala 3 and TypeScript support structural typing. Java's annotation processors (like Lombok) and frameworks (like Spring) sometimes simulate structural typing through code generation, but the language itself is firmly nominal. The trade-off: Java sacrifices flexibility for clarity and toolability (IDEs can navigate type hierries; refactoring is reliable).

## Q60: How does Java's type system handle null safety?

**A:** Java's type system does not inherently distinguish nullable from non-nullable types. Every reference type (`String`, `List`, `Object`) can hold `null`. This is the source of the ubiquitous `NullPointerException`.

Mitigations in the language:
1. **`Optional<T>`** (Java 8+): Explicitly represents the absence of a value. Forces the caller to handle the empty case. Not a null replacement for fields or parameters — a return type convention.
2. **Annotations** (`@NonNull`, `@Nullable` from JetBrains, `@javax.annotation.Nonnull`): Metadata for static analysis tools (SpotBugs, Checker Framework, IntelliJ). Not enforced by the compiler.
3. **Objects.requireNonNull()** (Java 7+): Throws `NullPointerException` immediately on null arguments, failing fast.
4. **`instanceof` checks**: Pattern matching with `if (obj instanceof String s)` implicitly handles null — `instanceof` returns `false` for null.

```java
public Optional<String> findUser(long id) {
    return Optional.ofNullable(userMap.get(id));
}

// Caller
findUser(42).ifPresent(user -> process(user));
```

Languages like Kotlin and Swift have built-in null safety (`String?` vs `String`). Java has considered adding `null`-safe types but has not done so due to backward compatibility. Project Valhalla (value types) and potential future language changes may address this, but for now, `Optional`, annotations, and defensive programming are the tools available.

## Q61: What is the role of interfaces in enabling testability?

**A:** Interfaces are the primary mechanism for enabling unit testing in Java. By depending on interfaces rather than concrete implementations, production code can be tested with mock or stub implementations.

Without interfaces, testing requires either the real implementation (integration test) or bytecode manipulation (Mockito's CGLIB mocking). With interfaces, you can create simple test doubles:

```java
interface UserRepository {
    User findById(long id);
    void save(User user);
}

class UserService {
    private final UserRepository repo;

    UserService(UserRepository repo) { this.repo = repo; }

    User getUser(long id) {
        return Optional.ofNullable(repo.findById(id))
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}

// Test
class UserServiceTest {
    void testGetUser() {
        UserRepository mock = id -> new User(id, "test"); // lambda for SAM interface
        UserService service = new UserService(mock);
        User user = service.getUser(42);
        assertEquals("test", user.name());
    }
}
```

The Dependency Inversion Principle directly enables testability. Without it, `UserService` would instantiate `MySqlUserRepository` internally, making testing require a database. With DIP, the test provides a fake, and the production code provides the real implementation via a DI framework.

This is why frameworks like Spring emphasize interface-based programming and constructor injection — they make the codebase inherently testable.

## Q62: What are sealed classes and how do they constrain inheritance?

**A:** Sealed classes (Java 17, preview in Java 15) restrict which classes can extend or implement them. The `permits` clause lists all allowed subclasses, which must be in the same module (or same file for a non-module class).

```java
public sealed class Result<T> permits Success, Failure, Loading {}
public record Success<T>(T data) implements Result<T> {}
public record Failure<T>(Exception error) implements Result<T> {}
public record Loading<T>() implements Result<T> {}
```

Subclasses must be `final`, `sealed`, or `non-sealed`:
- `final`: Cannot be extended further. Most common.
- `sealed`: Further restricts its own subclasses with its own `permits`.
- `non-sealed`: Opens the class for unrestricted extension. Rare and usually undesirable.

The benefits:
1. **Exhaustive pattern matching**: The compiler knows all subtypes, so `switch` expressions can be exhaustive.
2. **Predictable hierarchy**: No unknown subclasses can appear at runtime (unlike open hierarchies where any class can extend).
3. **API design**: You can expose a sealed interface as a return type, ensuring callers handle all cases.
4. **Security**: Prevents untrusted code from extending sensitive classes.

Sealed classes bridge the gap between OOP's extensibility and FP's algebraic data types. They give you the compiler-checked exhaustiveness of sum types while retaining the flexibility of class hierarchies.

## Q63: What is the difference between `record` and a regular `class` in Java?

**A:** Records (Java 16+) are a special kind of class for immutable data carriers. Key differences:

| Feature | Record | Regular Class |
|---|---|---|
| Declaration | `record Point(int x, int y)` | `class Point { int x; int y; }` |
| Fields | Implicit `private final` | Programmer-defined |
| Constructor | Implicit canonical constructor | Must define |
| Accessors | `x()`, `y()` (not `getX()`/`getY()`) | Custom |
| `equals`/`hashCode`/`toString` | Auto-generated (value-based) | Programmer-defined |
| Inheritance | Cannot extend classes | Can extend |
| Mutable fields | Not allowed (final) | Allowed |
| Can implement interfaces | Yes | Yes |
| Can have methods | Yes | Yes |
| Can have static fields | Yes | Yes |

Records are not just syntactic sugar — they are a distinct class declaration type. The JVM treats them specially (the `Record` attribute in bytecode). They enforce immutability by making all components final and the record class implicitly final.

```java
record Point(int x, int y) {
    // Custom compact constructor (validation)
    Point {
        if (x < 0 || y < 0) throw new IllegalArgumentException();
    }
}
```

Records are for data. Use classes for behavior-rich objects with mutable state and complex invariants. Records are ideal for DTOs, value objects, return types, and map keys.

## Q64: What is the difference between a `record` and a `data class` in Kotlin?

**A:** Kotlin data classes (`data class Point(val x: Int, val y: Int)`) and Java records are conceptually similar — both are immutable data carriers with auto-generated `equals`, `hashCode`, and `toString`. Key differences:

| Feature | Java Record | Kotlin Data Class |
|---|---|---|
| Immutability | Enforced (all fields final) | By convention (`val`) but can have `var` |
| Inheritance | Cannot extend classes | Cannot extend classes (same) |
| Can extend interfaces | Yes | Yes (since Kotlin 1.5) |
| Component functions | `x()`, `y()` | `component1()`, `component2()` (destructuring) |
| `copy()` method | Not auto-generated | Auto-generated |
| Default values | Not in canonical constructor | Supported |
| Validation | Compact constructor | `init` block |
| Mutability | Strictly immutable | Can have `var` properties |
| JVM representation | `Record` attribute | Regular class |

Kotlin data classes are more flexible: they can have mutable properties, default parameter values, and `copy()` for creating modified instances. Java records are stricter: all state is final, and the canonical constructor is the only way to initialize.

Java records are simpler and have clearer semantics. Kotlin data classes are more feature-rich. Both serve the same purpose: reducing boilerplate for value types. Java records can achieve similar `copy()` functionality with a manual method or with `with` pattern.

## Q65: What are records in Java and when should you use them?

**A:** Records are immutable data carriers that automatically generate constructors, accessors, `equals()`, `hashCode()`, and `toString()`. They are ideal for:

1. **DTOs (Data Transfer Objects)**: `record UserDto(long id, String name, String email)` — clean, minimal, immutable.
2. **Value objects**: `record Money(BigDecimal amount, Currency currency)` — the record's value-based equality works perfectly.
3. **Return types**: `record SearchResult(List<Item> items, int totalCount, boolean hasMore)` — named, typed, immutable.
4. **Map keys and set elements**: Immutable, value-based equality — no hash collisions from mutable fields.
5. **Encapsulating domain events**: `record OrderPlaced(String orderId, Instant timestamp)`.

Do NOT use records for:
- **Mutable domain entities** — records are immutable by design.
- **Objects with behavior** — records can have methods, but classes are more natural for behavior-rich objects.
- **Objects needing inheritance** — records cannot extend classes (though they can implement interfaces).
- **Objects with complex construction logic** — the canonical constructor is fixed; complex initialization may be awkward.

```java
record Range(int start, int end) {
    Range {  // compact constructor
        if (start > end) throw new IllegalArgumentException("start > end");
    }

    int length() { return end - start; }
}
```

Records represent a shift toward "data as a first-class concept" in Java, similar to Kotlin data classes, Scala case classes, and C# records.

## Q66: How do records interact with generics?

**A:** Records can be generic, just like classes. This enables type-safe data carriers:

```java
record Pair<A, B>(A first, B second) {}

Pair<String, Integer> pair = new Pair<>("hello", 42);
String first = pair.first();    // String — no cast needed
Integer second = pair.second(); // Integer — no cast needed
```

Generic records work with bounded type parameters:

```java
record MinMax<T extends Comparable<T>>(T min, T max) {
    int compare() { return min.compareTo(max); }
}
```

Generic records support all the standard record features: compact constructors, static factory methods, additional methods, and interface implementation. The compiler generates type-specific accessors, `equals`, `hashCode`, and `toString`.

```java
record NamedPair<A>(String name, A value) implements Comparable<NamedPair<A>> {
    NamedPair {
        Objects.requireNonNull(name);
        Objects.requireNonNull(value);
    }

    @Override
    public int compareTo(NamedPair<A> other) {
        return this.name.compareTo(other.name);
    }
}
```

One consideration: due to type erasure, you cannot use `T.class` in a generic record. To create instances or perform type checks, pass a `Class<T>` parameter: `record Typed<T>(Class<T> type, T value) {}`. Generic records are commonly used in API design for typed responses, key-value pairs, and result containers.

## Q67: What is pattern matching for `instanceof` and how does it simplify code?

**A:** Pattern matching for `instanceof` (Java 16+) combines the type check and the cast into a single operation. Instead of:

```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}
```

You write:

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

The pattern variable `s` is bound only in the scope where the `instanceof` check is known to be true. It works with logical operators:

```java
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}
```

The `&&` operator short-circuits, so `s` is only used if the `instanceof` check succeeded. With `||`, the pattern variable is available in the false branch:

```java
if (obj instanceof String s) {
    System.out.println("String: " + s);
} else {
    // s is NOT available here — it was true in the if-branch
}
```

Pattern matching eliminates `ClassCastException` risks, reduces boilerplate, and makes the intent clearer. Combined with sealed classes and switch expressions, it enables exhaustive, type-safe dispatch that previously required visitor patterns or chains of instanceof checks.

## Q68: What is pattern matching for `switch` expressions and how does it relate to sealed classes?

**A:** Pattern matching for `switch` (Java 21+) allows `switch` to match on types, guarded patterns, and null:

```java
sealed interface Shape permits Circle, Rectangle {}
record Circle(double r) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

double area(Shape s) {
    return switch (s) {
        case Circle c    -> Math.PI * c.r() * c.r();
        case Rectangle r -> r.w() * r.h();
    };
}
```

The compiler enforces exhaustiveness for sealed types. If you add a new subtype, every switch that does not handle it becomes a compile error. This is similar to exhaustive pattern matching in Scala or Rust.

Additional features:
- **Null handling**: `case null -> "null shape"` — eliminates the common `NullPointerException` from switch.
- **Guarded patterns**: `case Circle c && c.r() > 10 -> "large circle"`.
- **Dominance**: More specific patterns must come before more general ones.
- **Readable and writable**: Switch expressions can return values, enabling functional-style code.

```java
String describe(Shape s) {
    return switch (s) {
        case null -> "null";
        case Circle c when c.r() > 10 -> "large circle";
        case Circle c -> "small circle";
        case Rectangle r when r.w() == r.h() -> "square";
        case Rectangle r -> "rectangle";
    };
}
```

This eliminates the need for the Visitor pattern in many cases — the switch provides type-safe, exhaustive dispatch over a closed set of types.

## Q69: How do sealed classes interact with interfaces?

**A:** A sealed interface restricts which classes or interfaces can implement it. This is more common than sealed classes because interfaces are the typical abstraction boundary.

```java
sealed interface ApiResponse<T> permits SuccessResponse, ErrorResponse, LoadingResponse {}

record SuccessResponse<T>(T data) implements ApiResponse<T> {}
record ErrorResponse<T>(String message, int code) implements ApiResponse<T> {}
record LoadingResponse<T>() implements ApiResponse<T> {}
```

The `permits` clause on an interface works identically to a sealed class. All permitted subtypes must be in the same module. They must be `final`, `sealed`, or `non-sealed`.

This enables a powerful API pattern: the client depends on the sealed interface and uses pattern matching to handle all cases. The API provider controls exactly which responses are possible.

```java
<T> void handle(ApiResponse<T> response) {
    switch (response) {
        case SuccessResponse<T> s -> process(s.data());
        case ErrorResponse<T> e   -> log.error("Error {}: {}", e.code(), e.message());
        case LoadingResponse<T>   -> showSpinner();
    }
}
```

The sealed constraint means the API provider can add new response types (like `RateLimitedResponse`) and the compiler will flag every switch that needs updating. This is compile-time-safe API evolution — no silent failures from unhandled cases.

## Q70: What is the difference between the Builder pattern and records?

**A:** The Builder pattern handles complex object construction with many optional parameters. Records handle simple, all-required-parameter data carriers.

**Records** are ideal when all fields are required and the object is immutable:

```java
record User(String name, String email, int age) {}
// Every field must be provided
```

**Builders** are ideal when:
- Many fields are optional.
- Construction has validation or complex logic.
- The object is mutable (builder updates state during construction).
- You want a fluent API.

```java
class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final byte[] body;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.headers = Map.copyOf(builder.headers);
        this.body = builder.body;
    }

    static class Builder {
        private String url;
        private String method = "GET";
        private Map<String, String> headers = new HashMap<>();
        private byte[] body;

        Builder url(String url) { this.url = url; return this; }
        Builder method(String m) { this.method = m; return this; }
        Builder header(String k, String v) { headers.put(k, v); return this; }
        Builder body(byte[] b) { this.body = b; return this; }
        HttpRequest build() { return new HttpRequest(this); }
    }
}
```

Records can have static factory methods that simulate builders: `User.of("name", "email", 17)` with validation in the compact constructor. For most modern Java, records with compact constructors replace the Builder pattern for simple DTOs. Keep Builders for complex construction with optional parameters.

## Q71: Explain the concept of type witnesses in Java generics.

**A:** Type witnesses explicitly specify the generic type argument when calling a generic method. Without them, the compiler infers the type from the arguments.

```java
class Box {
    static <T> Box<T> of(T value) {
        Box<T> box = new Box<>();
        box.value = value;
        return box;
    }
}

// Type inference — compiler infers String
Box<String> b1 = Box.of("hello");

// Type witness — explicitly specify String
Box<String> b2 = Box.<String>of("hello");
```

Type witnesses are necessary when the compiler cannot infer the type, or when you want a different type than what would be inferred:

```java
// Without type witness, T is inferred as Object
Box<Object> b3 = Box.of("hello"); // compiles, but T is Object

// With type witness, T is explicitly String
Box<String> b4 = Box.<String>of("hello"); // compiles, T is String
```

Another use case: generic method calls where inference produces an ambiguous type:

```java
List<String> list = List.of("a", "b");
// This calls the static method, but which overload?
Collections.addAll(list, new String[]{"x", "y"});  // unambiguous
Collections.<String>addAll(list, "x", "y");        // type witness for clarity
```

Type witnesses are rarely needed in practice because Java's type inference (target typing) is sophisticated. But they are useful for clarity and when inference produces a wider type than intended.

## Q72: What is target typing and how does it affect generic method inference?

**A:** Target typing is the compiler's ability to use the context (the expected type of the expression) to infer generic type parameters. Java 8 significantly improved target typing for lambda expressions and method references.

Before Java 8, the compiler could not infer the type of a lambda based on the assignment target. You had to write explicit parameter types:

```java
// Java 7
list.sort((a, b) -> a.compareTo(b)); // fails — T is ambiguous

// Java 8+
list.sort((a, b) -> a.compareTo(b)); // works — compiler infers Comparator<String>
```

Target typing works by propagating the expected type inward. If you write `List<String> list = List.of("a", "b")`, the compiler knows the context expects `List<String>` and infers that `List.of()` should produce `String` elements.

The limitations: target typing does not work across statements (only within expressions), and complex nesting can confuse the compiler. Method chaining can break inference:

```java
// This may fail — the compiler needs to infer the intermediate type
stream.map(x -> x.toString()).collect(Collectors.toList());
// This works — type witness clarifies
stream.<String>map(x -> x.toString()).collect(Collectors.toList());
```

Target typing makes Java generics more ergonomic but can produce confusing error messages when inference fails. The solution is usually to provide a type witness or break the expression into smaller pieces.

## Q73: What are generic methods and how do they differ from generic classes?

**A:** A generic method declares its own type parameters, independent of any enclosing class's type parameters. The type parameters appear before the return type:

```java
class Util {
    static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;
    }
}

// Type inference
int bigger = Util.max(3, 5); // T inferred as Integer

// Type witness
String longer = Util.<String>max("hello", "world");
```

A generic class's type parameters are fixed for all instances: `Box<String> box = new Box<>()` — `T` is `String` for the entire instance. A generic method's type parameters vary per invocation: the same `Util.max()` can return an `Integer`, `String`, or `LocalDate` depending on the arguments.

Generic methods are commonly used for:
- **Static utility methods**: `Collections.sort()`, `Arrays.asList()`.
- **Factory methods**: `Optional.of()`, `List.of()`.
- **Conversion methods**: `<T> List<T> cast(List<Object> list)` (unsafe but illustrative).
- **Bounded operations**: `max`, `min`, `sort` where the type must be `Comparable`.

A method can be both in a generic class and be itself generic: `class Box<T> { <U> Box<U> map(Function<T,U> f) {} }` — the class has `T`, the method adds `U`.

## Q74: What are higher-kinded types and does Java support them?

**A:** Higher-kinded types (HKTs) are types that abstract over type constructors, not just types. A `List` is a type constructor: given `String`, it produces `List<String>`. An HKT would let you write functions that work for any "container-like" type: `F<A>` where `F` is the container type and `A` is the element type.

Scala and Haskell support HKTs natively:
```scala
// Scala
trait Functor[F[_]] {
  def map[A, B](fa: F[A])(f: A => B): F[B]
}
```

Java does NOT support HKTs. You cannot write `<F<_>, A> void map(F<A> fa, Function<A,B> f)`. The `_` syntax for type constructors is not part of Java's grammar.

The workaround is to use reflection-based type tokens (super type token pattern) or to encode HKTs using higher-ranked types via interfaces:

```java
// Encoding: "any container F that can map"
interface Mappable<F> {
    <A, B> F<B> map(F<A> fa, Function<A, B> f);
}

// Each container provides its own Mappable instance
Mappable<List> listMappable = new Mappable<>() {
    public <A, B> List<B> map(List<A> fa, Function<A, B> f) {
        return fa.stream().map(f).collect(Collectors.toList());
    }
};
```

This is verbose and loses type safety. HKTs are one of the most requested language features for Java. Project Valhalla and future language evolution may address this, but as of Java 21, they remain unsupported.

## Q75: What is the relationship between `Comparable` and `Comparator` and how do they use generics?

**A:** Both `Comparable<T>` and `Comparator<T>` define a comparison operation, but they serve different purposes:

**`Comparable<T>`** is implemented by the class being compared. It defines the "natural ordering":
```java
class Employee implements Comparable<Employee> {
    private String name;

    @Override
    public int compareTo(Employee other) {
        return this.name.compareTo(other.name);
    }
}
```

**`Comparator<T>`** is a separate object that defines an ordering for a type. It is used when you want multiple orderings or when you cannot modify the class:
```java
Comparator<Employee> bySalary = Comparator.comparingDouble(Employee::salary);
Comparator<Employee> byName = Comparator.comparing(Employee::name);
```

The generics ensure type safety: `Comparable<Employee>.compareTo(Employee)` prevents comparing incompatible types. `Comparator<Employee>.compare(Employee, Employee)` does the same.

Since Java 8, `Comparator` has gained powerful default methods: `thenComparing()`, `reversed()`, `nullsFirst()`. These enable complex ordering chains:

```java
Comparator<Employee> chain = Comparator
    .comparing(Employee::department)
    .thenComparing(Employee::name)
    .thenComparingDouble(Employee::salary).reversed();
```

`Comparable` is for the default, natural ordering. `Comparator` is for custom, alternate orderings. Both are generic interfaces that enforce type-safe comparison at compile time. The `Collections.sort()` method accepts a `Comparator`, while `List.sort()` uses the element's `Comparable` implementation by default.


## Q76: How would you design an API contract to enforce both extensibility and safety at a bank, given FAANG-scale requirements?

**A:** At a bank processing millions of transactions daily, the API contract must balance extensibility (new transaction types, new payment protocols) against safety (immutability, validation, no leaks of internal state). The design should use a sealed hierarchy for transaction types with records for immutable data carriers.

```java
public sealed interface Transaction permits Debit, Credit, Pending {}

public record Debit(AccountId account, Money amount, Instant timestamp, String reference)
        implements Transaction {}

public record Credit(AccountId account, Money amount, Instant timestamp, String reference)
        implements Transaction {}

public record Pending(AccountId account, Money amount, String status)
        implements Transaction {}
```

The sealed interface prevents external code from inventing new Transaction subtypes — the ledger logic can process all known types exhaustively via pattern matching (the compiler enforces completeness). Records ensure the transaction data is immutable — the 2-part ledger invariant (every debit has a credit) holds because fields cannot be mutated after construction.

The interface boundary also protects the bank: internal classes like `LedgerEntry` or `AuditLog` are never exposed. Clients collect transactions iteratively (like a `Stream`), and the core processing is done by a `LedgerProcessor` that takes `Transaction` and returns a new immutable `LedgerState`. This design gives you compile-time safety, runtime safety (no heap pollution), and extensibility — adding `Refund` means adding a new record, not touching the processor switch.

## Q77: Compare method dispatch performance: interface calls, virtual calls, and static calls in the JVM.

**A:** JVM calls have ascending cost: static (fastest), virtual with single implementation (fast), interface with single implementation (fast), interface with multiple implementations (slowest, but still microsecond-optimized).

The JIT compiler aggressively optimizes dispatch through:
1. **Monomorphic call sites**: If a call site always invokes the same implementation, the JIT devirtualizes it into a direct call or even inlines the entire method body.
2. **Polymorphic call sites**: If 1-2 implementations exist, the JIT uses "inline caching" — a cached type check with a fast path.
3. **Megamorphic call sites**: If 3+ implementations are observed, inline caching degrades; the JIT falls back to a vtable/itable lookup.

```java
// Monomorphic — JIT inlines
Animal a = new Dog();  // always Dog
a.speak();

// Megamorphic camp — hard for JIT
Animal a = pickRandom();  // could be Dog, Cat, Bird, ...
a.speak();
```

In practice, the JIT uses profiling to identify hot call sites and optimizes accordingly. Interface calls (`invokeinterface`) may be slightly more expensive than virtual calls (`invokevirtual`) because the interface method table (itable) lookup is less predictable. But with inline caching, the difference is negligible for production workloads whose call sites are stable.

The real performance insight: design for monomorphic/macheism. If a megamorphic call site is a bottleneck, consider restructuring (e.g., extracting the hot interface into the class hierarchy) or using `final`/`sealed` to give the JIT more opportunity for devirtualization.

## Q78: What are variance annotations in Kotlin and how do they compare to Java's wildcards?

**A:** Kotlin uses **declaration-site variance** (annotations on type parameters), while Java uses **use-site variance** (wildcards at usage sites).

Kotlin:
```kotlin
interface Producer<out T> { fun produce(): T }
interface Consumer<in T> { fun consume(item: T) }
// Producer<Dog> is a subtype of Producer<Animal>
// Consumer<Animal> is a subtype of Consumer<Dog>
```

Java:
```java
interface Producer<T> { T produce(); }
// Producer<Dog> is NOT a subtype of Producer<Animal>
// You must use wildcards: Producer<? extends Animal>
```

Declaration-site variance is more ergonomic: the type system automatically propagates the variance through generic compositions. `List<out T>` means `List<String>` is assignable to `List<Any>`, and `List<in Number>` means `List<Any>` is assignable to `List<Number>`.

Use-site variance (Java) shifts the burden to each usage site. Every generic method that needs flexibility must declare wildcards, which leads to verbose signatures like `void copy(List<? extends Number> src, List<? super Number> dest)`.

Kotlin's variance annotations are strictly more powerful for the common cases. Java cannot adopt declaration-site variance without breaking binary compatibility. Kotlin, having no backward-compat constraint, chose the cleaner design. The trade-off for Java is that use-site variance is explicit and composable in ways that declaration-site variance is not (you can always express `Producer<? extends T>` at the use site, even with `out`).

## Q79: How do you model an algebraic data type (sum type) in Java?

**A:** An algebraic data type (ADT) is a type formed from alternatives (sum type) or product combinations (product type). Records are product types (all fields present). Sum types are modeled in modern Java with sealed classes and pattern matching.

```java
// Sum type: an expression is either a literal, a variable, or a binary operation
sealed interface Expr {
    record Literal(int value) implements Expr {}
    record Var(String name) implements Expr {}
    record BinOp(Expr left, Op op, Expr right) implements Expr {}
}

// The sealed hierarchy + pattern matching gives exhaustive, type-safe evaluation
int eval(Expr expr) {
    return switch (expr) {
        case Expr.Literal l -> l.value();
        case Expr.Var v     -> lookup(v.name());
        case Expr.BinOp b   -> eval(b.left()) * b.op().apply(eval(b.right()));
        // compiler enforces: no missing case
    };
}
```

The key contrast with classical OOP: classical Java would model this as an abstract `Expr` base class with a virtual `eval()` method. Each subclass implements `eval()`. This is the **Expression Problem** solution: adding a new operation (like `evalToInfix()`) requires editing ALL subclasses. The sealed+pattern-matching approach lets you add operations as new functions without touching the data classes.

Which is better depends on the extension axis: if you add new node types frequently (new Expr variants), use virtual methods (open hierarchy). If you add new operations frequently (serialization, pretty-printing, evaluation), use sealed+switch. Modern Java supports both — choose based on the dominant change rate.

## Q80: What is the fragile base class problem and how do modern Java features mitigate it?

**A:** The fragile base class problem: subclasses depend not just on the interface of a superclass but on its internal implementation details. A superclass change can break subclasses through any of these channels: a method added to the superclass that the subclass forgot it overrides or relies on; changed behavior that subclasses built on; a previously-final method made non-final.

Java mitigations:

1. **`final` and `sealed`**: Prevent subclassing where it is not needed. This narrows the contract surface.
2. **Interfaces + default methods**: Most code depends on interfaces. Adding a default method does not break existing implementations (unless they collide).
3. **Records**: Immutable, auto-generated equals/hashCode — no state to mutate. The compact constructor is the single construction path.
4. **Pattern matching + sealed**: Replaces inheritance-based dispatch with switch-based dispatch. The hierarchy becomes data + switch, not behavior + override.

```java
// Instead of subclassing a base class to add behavior, use sealed + switch
sealed interface LogMessage permits ErrorLog, InfoLog {}
record ErrorLog(String message, int code) implements LogMessage {}
record InfoLog(String message, int timestamp) implements LogMessage {}

class LogFormatter {
    static String format(LogMessage msg) {
        return switch (msg) {
            case ErrorLog e -> "ERROR " + e.code() + " " + e.message();
            case InfoLog i  -> "INFO " + i.timestamp() + " " + i.message();
        };
    }
}
```

The modern trend: fewer deep class hierarchies, more sealed data types + pattern matching, fewer behaviors baked into classes. This reduces the fragile base class risk substantially.

## Q81: How would you implement a serialization library that handles inheritance and polymorphism correctly?

**A:** Serialization of polymorphic types is one of the hardest problems in Java OOP. The naive approach — writing `obj.getClass().getName()` and deserializing by reflection — works but is dangerous: it introduces a class-loading vulnerability (arbitrary code execution via malicious type names) and couples serialization to the class hierarchy.

The robust approach uses a **type discriminator**. Each subtype carries an explicit, verified type identifier. On deserialization, the registry maps that identifier to a known class.

```java
class SafeObjectMapper {
    private static final Map<String, Class<?>> REGISTRY = new HashMap<>();

    static {
        REGISTRY.put("transaction-debit", Debit.class);
        REGISTRY.put("transaction-credit", Credit.class);
        REGISTRY.put("payment-card", CardPayment.class);
    }

    static <T> byte[] write(T obj) {
        String id = idFor(obj.getClass()); // throws UnknownTypeException
        return new ObjectOutputStream(new ByteArrayOutputStream())
            .writeObject(new Payload(id, obj));
    }

    static <T> T read(byte[] bytes) {
        Payload p = deserialize(bytes);
        Class<?> cls = REGISTRY.get(p.typeId());
        if (cls == null) throw new SecurityException("Unknown type: " + p.typeId());
        return cls.cast(p.data());
    }
}
```

Key design decisions:
1. **Whitelist, not blacklist**: Only known types can be deserialized. Unknown types are rejected — prevents deserialization attacks.
2. **Versioning**: Add `version` or `schemaVersion` to the payload. Old clients can fail gracefully with a clear message instead of corrupting data.
3. **Immutable data**: Prefer records for the serialized model — they have canonical construction, no hidden state.
4. **Interfaces for the wire format**: The serialized model depends on interfaces, so adding a new implementation does not change the wire format.

This is why modern serialization libraries (Jackson with `@JsonTypeInfo`+`@JsonSubTypes`, Avro with registered schemas, Protobuf with `oneof`) prefer explicit type registration over runtime reflection on `getClass()`.

## Q82: What is the difference between the Expression Problem solutions in Java: virtual methods, default methods, and pattern matching?

**A:** The Expression Problem asks: how do you add new operations and new variants to a closed type without breaking existing code?

**Virtual methods** solve the "new variant" axis well: adding a new subclass is trivial. But "new operation" requires editing every existing subclass (or adding a default method to the interface).

**Default methods** solve "new operation" better: with a well-designed interface, you can add a default that builds on other interface methods. But defaults cannot access subclass-specific state and cannot be truly polymorphic with the concrete class's own fields. The classic frustration: you cannot add an operation that "looks inside" a class without modifying it.

**Pattern matching + sealed types** solves both axes asymmetrically but practically:
- "New variant": add a record/class to the sealed hierarchy. Existing switches now fail to compile (exhaustiveness) — which is good, they surface where behavior must be added.
- "New operation": write a new switch over the sealed type. No existing code is edited.

```java
// Adding an operation: new switch, no edits to existing classes
double perimeter(Shape s) {
    return switch (s) {
        case Circle c    -> 2 * Math.PI * c.r();
        case Rectangle r -> 2 * (r.w() + r.h());
    };
}
```

The trade-off: pattern matching requires the type hierarchy to be **sealed** (closed). If you need arbitrary third-party extensibility, virtual methods remain the answer. Pattern matching sacrifices open extensibility for compiler-checkable exhaustiveness. Real designs often mix both — sealed core types for exhaustiveness, an escape hatch (e.g., a `SpecialShape` permitted subclass that is `non-sealed`) for genuine open extension.

## Q83: How do you achieve circular-reference-safe deep equals for a mutable field graph in Java?

**A:** Deep equality over a mutable object graph is a classic pitfall. `equals()` recurses; cycles cause `StackOverflowError`. The standard solutions:

1. **Value-based equality for immutable parts**: Records give value-based equals for their components. Keep the mutable/cyclic parts OUT of `equals()` — compare keys instead.

2. **Identity-based cycle guard**: Track the "in-progress" pairs. Not correct after the fact, but adequate for the visit:

```java
class GraphNode {
    final String name;          // unique key
    List<GraphNode> neighbors;

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof GraphNode o)) return false;
        if (stack.contains(() -> this.equals(o))) return true; // assumed equal mid-recursion
        stack.push(this);
        boolean eq = name.equals(o.name) && listEquals(neighbors, o.neighbors, stack);
        stack.pop();
        return eq;
    }
}
```

3. **HashCode stability**: If you include mutable `neighbors` in `hashCode()`, the object's hash changes as it mutates — breaking `HashMap`/`HashSet` lookups. The only safe approach is to hash on the immutable identity key only:

```java
@Override
public int hashCode() { return name.hashCode(); }
```

4. **Composition libraries**: Libraries like Guava's `Equivalence` and equalsverifier support stricter equality contracts, but none handle cycles well.

The senior architect guidance: don't put graphs in sets/maps by deep equality. Give nodes an identity (`UUID`, natural key) and compare by that key. Deep equality is for immutable value types; for mutable graphs, use identity-based hashing and key-based comparison. If you must deep-compare, normalize to a string representation (like a canonical serialized form) and compare strings — immune to cycles as long as serialization handles cycles.

## Q84: How do Java interfaces enable the Open/Closed Principle in practice at scale?

**A:** Open/Closed Principle (OCP): open for extension, closed for modification. In a growing codebase, new features should be added by extending contracts (new implementations, new strategies) rather than editing existing classes.

Practical pattern: a plugin architecture built on interfaces.

```java
public interface PaymentProvider {
    Result process(PaymentRequest request);
    String providerName();
}

// Sealed list of supported providers
public sealed interface RegisteredProvider 
    permits VisaProvider, MastercardProvider, UpiProvider, CouponProvider {
}
```

The `PaymentService` depends only on `PaymentProvider`:

```java
@Service
public class PaymentService {
    @Autowired List<PaymentProvider> providers;  // Spring injects all beans

    PaymentProvider findProvider(String name) {
        return providers.stream()
            .filter(p -> p.providerName().equals(name))
            .findFirst()
            .orElseThrow(() -> new UnsupportedProviderException(name));
    }
}
```

Adding a new payment method (e.g., "ApplePayProvider") requires ZERO changes to `PaymentService` — you add a class implementing `PaymentProvider`. The `@Autowired List<PaymentProvider>` collects all implementations automatically. This is OCP in action: closed to modification, open to extension.

Limitations to design around:
1. **Discovery**: The framework must discover new implementations. Spring's component scanning handles this via annotations.
2. **Versioning/evolution**: Interface changes break all implementations. Use bidirectional versioning (old and new method signatures coexist) during migration.
3. **Interface segregation**: A fat interface violates ISP. Break into role interfaces (`Refundable`, `ScheduledPayment`, `3DSecure`) and have providers implement only the roles they support, checked via `instanceof` when needed.

The interface-boundary rule of thumb: if a change to the business domain requires editing the interface itself, the interface was designed too narrowly or the domain changed fundamentally. Otherwise, the system should grow by adding classes, not editing existing ones.

## Q85: How do you design for the "dependency injection" pattern using interfaces in a Spring-like container?

**A:** Dependency injection (DI) relies on interfaces to decouple construction from use. The container (Spring) resolves which implementation of an interface to inject at runtime.

Design guidelines for interface-based DI:

1. **Program to the interface everywhere**: Fields, constructor params, and method signatures should reference interfaces, never concrete implementations.

```java
public class OrderFulfillmentService {
    private final InventoryService inventory;   // interface
    private final NotificationGateway notify;  // interface

    public OrderFulfillmentService(InventoryService inv, NotificationGateway n) {
        this.inventory = inv;
        this.notify = n;
    }
}
```

2. **Constructor injection over field injection**: Immutable, testable, explicitly typed. Field injection hides dependencies.

3. **Qualifiers for multiple implementations**: When the interface has several implementations, clarify which one:

```java
@Repository
public interface UserRepository { }

@Repository
public interface AuditRepository { }

@Service
public class UserService {
    private final UserRepository users;
    UserService(@Qualifier("userRepository") UserRepository r) { this.users = r; }
}
```

4. **Default implementations in interfaces?** Prefer not to — that couples logic into the contract. If a default can be derived without state, it is acceptable (e.g., `Collection.isEmpty()` = `size()==0`), but core logic should live in concrete classes.

5. **Context validity**: Never let DI bypass invariants. Empty parts of a large object graph remain null or unsafely defaulted if injections are missing — validate at construction (the container fails fast on missing dependencies).

The architectural payoff: unit tests inject fakes; production injects real implementations; the wiring is declarative and centralized. This directly enables Open/Closed, Liskov, and Single Responsibility principles at assembly time.

## Q86: What is the role of hashCode()/equals() stability in hash-based collections under inheritance?

**A:** `HashMap`, `HashSet`, and `ConcurrentHashMap` rely on two contracts:
1. Equal objects have equal hash codes.
2. Hash codes are stable while the object is live in the collection (Lookups probe the bucket by hash at insert AND at query — if the hash changed, the object is lost from its bucket).

Inheritance introduces subtle violations:

**Scenario**: `Base` defines `hashCode()` from `Base.fieldA`. `Derived` adds `fieldB` and overrides `equals()` to include it but FORGETS to override `hashCode()`. Two Derived objects equal by (aA+bA) but hash different → equal objects map to different buckets → `contains()` returns false. This is the classic HashSet bug.

**Scenario**: `hashCode()` uses mutable fields. The object is inserted into a `HashSet`, then a field mutates, changing the hash. The object is now in the wrong bucket; `contains()`/`remove()` silently fail. Records sidestep this by being immutable.

```java
class MutableKey {
    int id;       // mutable!
    String name;
    @Override public int hashCode() { return Objects.hash(id, name); }
}

var set = new HashSet<MutableKey>();
var key = new MutableKey(); key.id = 1; key.name = "a";
set.add(key);
key.name = "b";            // hash changes
System.out.println(set.contains(key)); // false — key lost!
```

The senior guidance:
- Prefer immutable keys (records, `Integer`/`UUID`/`Instant`). If mutability is unavoidable, hash only the identity field (the immutable natural key).
- Never include the mutable collection field in `hashCode()`.
- When overriding in subclasses, `equals` must be symmetric/transitive — that is, `Derived.equals(Base)` must be false, and `equals` should call `super.equals()` first. Keep `hashCode()` consistent — apply the same fields in the same order.
- Measure hazard: hash collections degrade to O(n) if equal objects collide. Aim for well-distributed hashes; use `Objects.hash()` (which factors in nulls and the class's package) for value types.

## Q87: How do you reconcile Liskov with "code reuse through inheritance"?

**A:** Liskov Substitution Principle (LSP) and code reuse pull in opposite directions. Inheritance that is motivated ONLY by reuse usually violates LSP.

The classic case: `Stack<T> extends ArrayList<T>` (the JDK did this). `Stack` inherits `add(int,T)` from `ArrayList` — allowing insertion in the middle — which breaks the LIFO invariant. This is reuse-without-substitution. Users of `ArrayList` (random access) can be passed a `Stack` and corrupt its semantics.

LSP-compliant reuse:
- The subclass must satisfy every guarantee the superclass makes. `Stack` cannot guarantee LIFO while `ArrayList` permits arbitrary insertion.
- Constraint: subclass must never strengthen preconditions beyond what superclass promises. `Stack.push` can be an override, but a caller holding an `ArrayList` reference must still get list semantics.

```java
// LSP-violating reuse
class CountingList extends ArrayList<String> {
    void magicAdd(String s) { super.add(s); }
}

// LSP-compliant: composition + delegation
class CountingList {
    private final List<String> delegate = new ArrayList<>();
    void add(String s) { delegate.add(s); }
    int size() { return delegate.size(); }
}
```

How to salvage legitimate reuse:
- Ensure the subclass is a genuine refinement: documented preconditions, weakened (not strengthened) validation, preserved invariants.
- Prefer package-private `abstract` methods that subclasses implement against a well-specified contract.
- Use `sealed`/`final` to guarantee the subclass behavior you depend on — you control the closed set.

The pragmatic rule: if you would not happily hand a `Stack` to a method expecting `ArrayList`, the "is-a" relationship is fake. Prefer composition or delegation.

## Q88: What is the observer pattern and how do interfaces enable it?

**A:** The Observer pattern defines a one-to-many dependency: when the subject changes state, all observers are notified.

```java
public interface Observer<T> {
    void onChange(T newValue);
}

public class Observable {
    private final List<Observer<String>> observers = new ArrayList<>();

    public void addObserver(Observer<String> o) { observers.add(o); }
    public void removeObserver(Observer<String> o) { observers.remove(o); }

    private String value;
    public void setValue(String v) {
        this.value = v;
        for (Observer<String> o : observers) o.onChange(value);
    }
}

// Usage — lambda implements the SAM interface
Observable subject = new Observable();
subject.addObserver(v -> System.out.println("value: " + v));
```

Variants:
- Push vs. pull: push sends the new value; pull lets the observer call back `subject.getState()`.
- Strong vs. weak references: storing observers strongly can leak memory; weak reference sets or explicit `removeObserver` mitigate.

Use cases: UI event handling (Swing listeners), reactive streams, messaging middlewares, Spring's event-emitting beans. Java 9's `java.util.Observer`/`Observable` are deprecated in favor of lambdas, `CompletableFuture`, and reactive streams — but the pattern itself (listener registry on interface) remains.

Trade-offs: decouples subject from observer (both depend on the interface), supports one-to-many simultaneously, and centralizes change propagation. Costs: a list of weak/strong refs to maintain, single-threaded notification ordering concerns, and potential callback reentrancy (an observer's `onChange` triggering another change) requiring a guard against infinite recursion.

## Q89: How do you design a strategy-based framework with a pluggable interface? Give a pricing engine example at a bank.

**A:** A pricing engine must support many pricing strategies (fixed rate, variable rate, volume discount, peak pricing) with runtime selection and zero coupling to the concrete algorithm.

```java
public interface PricingStrategy {
    Price quote(QuoteContext ctx);
}

public record QuoteContext(Instrument instrument, Side side, BigDecimal qty, QuoteType type) {}

public class FixedPricingStrategy implements PricingStrategy {
    public Price quote(QuoteContext ctx) {
        return Price.of(ctx.instrument().basePrice(), "fixed");
    }
}

public class VariablePricingStrategy implements PricingStrategy {
    public Price quote(QuoteContext ctx) {
        BigDecimal rate = ctx.type() == QuoteType.PEAK ? ctx.instrument().peakRate() : ctx.instrument().offPeakRate();
        return Price.of(ctx.instrument().basePrice().multiply(rate), "variable");
    }
}
```

Selection logic lives in a registry that maps a discriminator to a strategy:

```java
public class PricingEngine {
    private final Map<String, PricingStrategy> strategies = new ConcurrentHashMap<>();

    public void register(String name, PricingStrategy s) { strategies.put(name, s); }
    public Price quote(String strategyName, QuoteContext ctx) {
        return strategies.getOrDefault(strategyName, anyOtherStrategy())
            .quote(ctx);
    }
}
```

Design rules:
1. **The core depends only on `PricingStrategy`** — adding a new strategy (FIFO, LIFO auction) requires no change to the engine.
2. **Strategies are stateless** (or immutable state only) — safe for concurrent quote requests in high-throughput paths.
3. **Fail-fast on unknown key** — prefer throwing `UnknownStrategyException` over silent fallback, mapping to a 4xx/5xx response.
4. **Registry is the seam**: at startup, Spring registers beans keyed by bean name (`@Component("fixed")`), so adding a strategy is purely additive.

The trade-off vs. inheritance: strategies use composition and a lookup map; the inheritance alternative (switch/if-chains on an enum) is closed to new strategies. The strategy registry keeps the engine Open/Closed: extend by adding a registration, not editing the engine.

## Q90: How do you implement a generic cache with maximum type safety and minimum boxing in Java?

**A:** A type-safe, erasure-aware generic cache. Because generics are erased, a `Cache<T>` that lazily computes values needs a provider, not a concrete type.

```java
public sealed interface CachePolicy permits Ttl, Lru { }

public final class Cache<K, V> {
    private final ConcurrentHashMap<K, V> store = new ConcurrentHashMap<>();
    private final Function<K, V> loader;    // value provider

    private Cache(Function<K, V> loader) { this.loader = loader; }

    public static <K, V> Cache<K, V> loading(Function<K, V> loader) {
        return new Cache<>(loader);
    }

    public V get(K key) {
        return store.computeIfAbsent(key, loader);  // atomic per-key load
    }
}
```

Maximizing type safety and minimizing boxing:
1. **Primitive-specialized caches**: For `int`/`long`/`double` keys, boxed keys (`Integer`) allocate on every cache op. Specialize: `LongKeyCache<V>` using `ConcurrentHashMap<Long,V>` still boxes. True no-boxing requires something like a `LongToObjectFunction<V>` primitive specialized structure — or use a specialized library (e.g., a "LongCache" with a striped array). This is where generic `Cache<Long,V>` leaks `Long` boxing.
2. **Type tokens at boundaries**: Deserialization (Jackson/Gson) needs `TypeReference<T>` to construct a properly typed value. Pass `TypeReference` or `Class<V>` into the loader.
3. **Null semantics**: Never store null — the loader should return `Optional.empty()` or the loader contract says "null means absent."
4. **Statistics**: Track hit/miss counters as longs; exposure via `CacheStats` record.

The subtle erasure trap:
```java
// WRONG — V.class is erased, compiles, crashes at runtime
Cache<String, Item> c = Cache.loading(jsonMapper::readTree);
// stream().mapToInt... then box at value boundaries (fine), but V.class cast fails.
```

Senior takeaway: generic caches are fine for reference-typed values; for hot primitive-keyed paths (instrument prices, session IDs), write a dedicated `LongKeyCache` that never boxes the key. Test with equals/hashCode stability in mind — cache keys must be stable (records or immutable keys).

## Q91: How do Java's interfaces enable the Adapter pattern for migrating third-party APIs?

**A:** The Adapter pattern wraps a third-party (legacy or foreign) API so the rest of your codebase depends on your own interface, not the vendor's. This is the cornerstone of vendor-neutral design.

```java
public interface PaymentAdapter {
    PaymentResult capture(PaymentRequest req);
}

public class StripeAdapter implements PaymentAdapter {
    private final StripeClient client;
    public StripeAdapter(StripeClient client) { this.client = client; }

    public PaymentResult capture(PaymentRequest req) {
        // translate YOUR contract into Stripe's model
        var charge = client.charges().create(ChargeCreateParams.builder()
            .setAmount(req.amount().toMinorUnits())
            .setCurrency(req.currency().code())
            .build());
        return PaymentResult.success(charge.getId());
    }
}

public class PaypalAdapter implements PaymentAdapter {
    private final PaypalClient client;
    public PaymentAdapter(PaypalClient client) { /* map Paypal's model */ }
}
```

Why this matters at scale:
1. **Migration**: You can swap Stripe for Adyen by adding one new adapter. No code outside the adapters changes.
2. **Testing**: A fake `PaymentAdapter` is trivially injected into `PaymentService`.
3. **Facade** (variant): A "PaymentGatewayFacade" wraps multiple adapters in one entry point — the clients see the facade, adapters hide the vendor differences.

Migration caveats:
- Keep your interface's semantic gap explicit. A `PaymentRequest` must specify amount, currency, and idempotency — even if the vendor doesn't, the adapter maps/rejects ambiguity.
- Never let vendor types leak past the adapter boundary (`StripeCausedException` must become your own `PaymentException` with your own error taxonomy).
- Behavioral parity tests: a golden-file-style test that drives your interface against a recording of the vendor's responses yields high confidence during switchover.

The interface boundary is exactly what makes the migration "closed to modification, open to extension." Adapters vanish the day the underlying provider changes — that is the value proposition.

## Q92: What are the edge cases in `equals()` overriding with inheritance — symmetry and transitivity?

**A:** The mandatory `equals()` contract under inheritance: reflexivity, symmetry, transitivity, consistency. Two classic violations:

**Symmetry violation** (most common): a subclass adds a field and its `equals()` also accepts the superclass type.
```java
class Point2D { final int x,y; equals via (x,y); }
class Point3D extends Point2D { final int z;
    @Override public boolean equals(Object o){
       if(o instanceof Point3D p) return super.equals(p) && z==p.z;
       return false;  // OK symmetric...
    }
}
```
But the opposite asymmetry happens when a subclass uses `instanceof` with non-final superclass: `o instanceof Point2D` returns true for a Point3D with a different x — two objects that aren't equal under `Point3D` compare equal under `Point2D`. `a.equals(b)` true but `b.equals(a)` false when types differ.

**Transitivity violation**: 
```java
Point2D a = new Point2D(1,1);
Point3D b = new Point3D(1,1,2);
Point3D c = new Point3D(1,1,3);
a.equals(b)  ? common (x,y) — true if implemented so
b.equals(c)  ? same (x,y,z)? no — z differs — false
```
So a==b, a==c, but b!=c — breaking transitivity. This is unfixable while subtypes compare by different fields. The standard resolution is to make `equals` final (compare by the immutable key that the whole family shares), or to not let subtypes participate in equality at all — subtypes with distinct equality semantics should NOT be compared against the base.

```java
// Clean pattern: value families that re-key by a single canonical identity
final class Point2D {
    private final int x, y;
    @Override public final boolean equals(Object o){ return true==false; }
}
// subclasses extend but never override equals — transitivity holds
final class Point3D extends Point2D { final int z; }
```

Or use records (final, value-based). The catalog:
- `Point3D` should call `super.equals(o)` FIRST — if super fails, return false (types differ).
- Never write `instanceof` in a class you intend to extend.
- If you must compare across subtypes, normalize to a canonical form first (x,y,z from a common view).

This is why hash-based collections require equals/hashCode symmetry and transitivity; a HashSet mixed with differing keys silently loses entries.

## Q93: How do sealed interfaces shape API evolution compared to annotations and marker interfaces?

**A:** Sealed interfaces (Java 17) vs. annotations vs. marker interfaces are three strategies for constraining/annotating the type system:

1. **Sealed interface**: Compile-time closed set. `sealed interface ErrorCategorie permits AuthError, NetworkError, DataError`. External code cannot invent new subtypes — pattern matching exhaustiveness is guaranteed by the compiler.

```java
public sealed interface AppError permits AadhaarError, UpiError, FileError {}
public record AadhaarError(AadhaarCode code, String detail) implements AppError {}
public record UpiError(UpiCode code, String detail) implements AppError {}
// a `RetryError` from another jar cannot implement AppError
```

2. **Annotations**: Metadata with no type-system enforcement. `@Retention(RUNTIME) @interface Restrict {}` — anything (reflection) can check `isAnnotationPresent()`. Open, flexible, no compile-time exhaustiveness.

3. **Marker interfaces**: `Serializable`, `RandomAccess`. They constrain the type system at runtime (the JVM's serialization layer checks `instanceof Serializable`) but have no API surface.

How they interact in real code:
- **API response unions**: sealed → the server guarantees one of the documented shapes; the compiler enforces exhaustiveness in every switch.
- **Validation**: annotations (`@NotNull`, `@Size`) give declarative metadata; sealed types give structural guarantees.
- **Backward-compat addition**: adding a subtype to a sealed interface forces every consumer switch to update — good for controlled evolution, bad for dependent libraries that must add the update while the API is a moving target.

Design guidance: use sealed for the core type algebra (sum types, error unions). Use annotations for cross-cutting metadata (validation, DI, scheduling) which has no structural meaning. Use marker interfaces sparingly for runtime capability checks where the JVM itself consults `instanceof`.

## Q94: How do you implement an event-driven architecture with interfaces: pub-sub, strong/weak listeners, and memory safety?

**A:** Event-driven systems live or die by correct listener management. With interfaces as the listener contract:

```java
public interface DomainEventListener {
    void on(DomainEvent e);
}

public class EventBus {
    private final Set<DomainEventListener> strong = new HashSet<>();
    private final Set<DomainEventListener> weak = Collections.newSetFromMap(new WeakHashMap<>());
    public void subscribe(DomainEventListener l) { strong.add(l); }
    public void subscribeWeak(DomainEventListener l) { weak.add(l); }
    public void publish(DomainEvent e) {
        for (DomainEventListener l : strong) l.on(e);
        for (DomainEventListener l : weak) l.on(e);
    }
}
```

Memory safety: strong references create leaks if the listener is never removed (an anonymous `new DomainEventListener...` starts a GC-root chain). Weak references let GC collect dead listeners, but:
- "Weak" listeners are not guaranteed to fire for subscribers that are otherwise unreachable → correctness-sensitive subscribers must be strong + explicitly unsubscribed.
- WeakHashMap is NOT thread-safe; publish/subscribe must synchronize (use synchronized sets or a ConcurrentHashMap.newKeySet for strong; wrap weak set access in synchronized).

Ordering & propagation guarantees:
```java
public sealed interface DomainEvent permits OrderPlaced, OrderShipped, StockDepleted {}
public record OrderPlaced(OrderId order, Money total) implements DomainEvent {}
public record StockDepleted(Sku sku, int qty) implements DomainEvent {}
```

Pattern-matching dispatch replaces an instanceof chain:
```java
public class OrderEventListener implements DomainEventListener {
    public void on(DomainEvent e) {
        switch (e) {
            case OrderPlaced op -> { validate(op); }
            case OrderShipped os -> { notifyShipping(os); }
            case StockDepleted sd -> { replenish(sd); }
        }
    }
}
```

Error handling: a failing subscriber must not break others. Publish should catch per-subscriber exceptions (and route them to an error channel) rather than propagating. This keeps the bus resilient.

## Q95: What is the difference between a plugin architecture built on interfaces vs. one built on sealed types?

**A:** Both are plugin mechanisms; they differ in who can extend and how the platform verifies completeness.

**Interface-based plugins** (JSP, OSGi, Maven plugins, Jackson Modules):
```java
public interface PayloadParser { Parsed parse(byte[] raw); }
public class JsonParser implements PayloadParser { ... }
public class AvroParser implements PayloadParser { ... }
```
- Open: any third party writes a new `PayloadParser` and registers it. Discovery via `ServiceLoader`, reflection, or framework scanning.
- No exhaustiveness: the platform must iterate registered parsers; "unknown payload" is a runtime condition.

**Sealed-type plugins** (modern Java):
```java
public sealed interface SupportedParser permits JsonParser, AvroParser {}
public record JsonParser(...) implements SupportedParser {}
public record AvroParser(...) implements SupportedParser {}
```
- Closed: only the platform's listed types can parse. The switch over `SupportedParser` is exhaustive — the compiler proves no unknown parser is missed.
- Fits when the parser set is fixed by the platform contract.

Which for a product?
- For a serialization library (third parties need pluggable formats): interfaces + `ServiceLoader`/`@AutoService`.
- For banks' vendored response schemas (you control the set, correctness is contractual): sealed interfaces + pattern matching.

The mitigation nuance: sealed excludes untrusted additions; interface-based plugins allow safe untrusted code ONLY if a verification layer (whitelist scanning, signature checks) is enforced before loading. If you want "closed to unknown, open to registry": combine — the interface defines the extension point, but a `Registry` maps a capability string to the implementation, and the switch level checks registry entry existence.

## Q96: What are bridge methods and why are they needed for covariant overrides with generics?

**A:** A bridge method is a compiler-generated synthetic method that maintains polymorphism across type erasure and covariant returns.

Scenario: a class implements a generic interface whose method returns a type parameter. Overrides returning the specific type create two method signatures — the erased supertype and the covariant subtype — so the JVM needs a bridge to connect them.

```java
// User code
class StringBox implements Box<String> {
    public String get() { return "hi"; }        // returns String
}

// What the compiler emits
class StringBox implements Box {
    public String get() { return "hi"; }
    public Object get() { return this.get(); }  // BRIDGE — the erased signature
}
```

Why needed:
- The vtable maps the erased signature `get()→Object` to a method. `String get()` has a DIFFERENT method descriptor than `Object get()`. Without the bridge, a call `box.get(); chained on Box` would not resolve `Object get()` to the class — dispatch would break.
- Covariant returns (subtype superseding supertype) produce a bridge too: `SportsCar create()` vs the inherited `Car create()`.

Bridge methods are hidden (`Synthetic` attribute), may throw `AbstractMethodError` if a class forgets the specialization, and their presence explains why reflection `getMethods()` can show two overloads of the same logical method. Reflection code that routes on `getReturnType()` must handle the bridge (the newer `getMethod(...).getReturnType()` may be `Object`). Libraries that see a Method for `get()` with return `Object` but the bridge actually calls the `String` variant.

Detection: `method.isBridge()` and `method.isSynthetic()`. A serializer that inspects a record's accessors must skip bridges or it will "discover" phantom methods.

## Q97: How do default methods preserve backward compat while adding behavior, and what are the breaking scenarios?

**A:** Default methods are the API-evolution mechanism: an interface adds a method with a body; existing implementations inherit it without being modified. `Iterable.forEach()`, `Collection.stream()`, `Comparator.thenComparing()` are the canonical examples.

```java
public interface Repository<T, ID> {
    Optional<T> findById(ID id);
    void save(T entity);

    // New default — existing implementations get it for free
    default List<T> findAll() {
        throw new UnsupportedOperationException("findAll not supported");
    }
}
```

Breaking scenarios to be careful about:

1. **Default-conflict collision**: two interfaces provide conflicting defaults → implementing class MUST override (compiler errors). A default in a super-interfaces can silently change observable behavior of a class that previously called its own method.

2. **Unsafe defaults that assume APIs**: `default byte[] serialize() { return ...; }` behind an erasure gap could fail for some implementation's semantics.

3. **Accidental public API growth**: adding a public default method enlarges the interface's surface. External implementors were granted a new method they must override if it matters — but they didn't opt in. Binary-compatible, but semantically it may partially overwrite subclass behavior.

4. **Reflection surprises**: default methods appear in `getMethods()`; `Annotation.isDefault()`; serialization of lambdas can capture defaults.

Prevention checklist:
- Defaults should only call other interface methods (no state, no assumptions about implementor).
- Defaults should never be the ONLY documented behavior — they are a compatibility layer, not the contract.
- When adding a default that changes logic, consider a new distinct method name (`findAll` vs `findAllPage`); the default stays semantics-neutral.

Using `sealed` + interfaces removes the "unknown implementor" risk, letting defaults be written against the closed known set.

## Q98: What is the distinction between type-safe heterogeneous containers and generic interfaces?

**A:** A type-safe heterogeneous container stores values of DIFFERENT types keyed by their own Class objects, proving the type at retrieval.

```java
public class TypeSafeMap {
    private final Map<Class<?>, Object> store = new ConcurrentHashMap<>();

    <T> void put(Class<T> key, T value) { store.put(key, value); }

    <T> T get(Class<T> key) {
        return key.cast(store.get(key));  // unchecked safe — cast at retrieval
    }
}

TypeSafeMap m = new TypeSafeMap();
m.put(String.class, "hi");
m.put(Integer.class, 42);
String s = m.get(String.class);   // String — no cast needed by caller
```

This is "one value per class" or "one value per type-keyed token." Generalization: key by a `TypeToken`/`TypeReference` for generic types (you cannot key by `List<String>.class`).

Contrast with generic interfaces:
- A generic interface `Repository<T>` carries ONE type bound the whole type parameter is fixed — the container is typed ONCE, all values are the same T.
- The heterogeneous map keys each entry by its OWN type at runtime.

The senior tie-in: type tokens + `Class<T>` reify erased types at the boundary. Jackson's `TypeReference<T>`, Gson's `TypeToken`, and Spring's `ResolvableType` all encode this pattern.

Danger points:
- `Class.cast` produces an `ClassCastException` at READ time, not write. Ensure the put path validates `key.isInstance(value)` if you want fail-fast.
- Key identity: `Class` objects are interned and stable for application classes; dynamic classloaders (OSGi) can produce multiple `Class` instances for the same logical type — key by the class's canonical name instead if that environment matters.
- This pattern coexists beautifully with sealed interfaces: a sealed error hierarchy allows a heterogeneous "error registry" where each handler handles the exact sealed type.

## Q99: How do you implement a strategy alongside a default-completion strategy (the "partial function" problem) with interfaces?

**A:** This is the "partial function" anti-pattern: a base interface exposes a method, some implementations handle it, others throw `UnsupportedOperationException`. The strategy problem is the same pattern at different granularity — "some strategies can handle X, the rest delegate to a default."

Clean resolution using role interfaces (ISP) + default methods that delegate:

```java
public interface Scheduler {
    Duration delay(Duration base);
}

public sealed interface Policy permits EagerPolicy, LazyPolicy {
    Duration adjust(Duration base);
}

public final class ComposedPolicy implements Policy {
    private final List<Policy> policies;   // composite
    public Duration adjust(Duration base) {
        Duration acc = base;
        for (Policy p : policies) acc = p.adjust(acc);
        return acc;
    }
}

public record EagerPolicy(Duration cutoff) implements Policy {
    public Duration adjust(Duration base) {
        return base;  // eager → unchanged
    }
}
```

But the TRUE "partial function" — base has a method that not every subclass implements — mixes two concerns: "interface means capability" and "capability is optional in some subtypes." Recommended decomposition:
- The core interface carries only universally-supported methods.
- Capability-specific interfaces (`Refundable`, `Retryable`, `Exportable`) implement those methods.
- A base abstract class (or default) provides the no-op/deny-by-default for the optional capability; concrete classes override ONLY when they genuinely support it.

```java
public interface Refundable {
    RefundResult refund(RefundRequest r);
}

public abstract class AbstractPaymentMethod {
    // deny-by-default
    public RefundResult refundIfSupported(RefundRequest r) {
        throw new UnsupportedOperationException(this.getClass().getSimpleName() + " cannot refund");
    }
}

public final class CardPayment extends AbstractPaymentMethod implements Refundable {
    public RefundResult refund(RefundRequest r) { ... }
}
```

The lint rule: if a method is `UnsupportedOperationException` in most implementations, it does not belong on the shared interface — it belongs on a narrower role interface. Default-method delegating to a registry ("if no strategy registered, return this default") is the pragmatic coastal compromise when you cannot change the interface.

## Q100: What are the hard design trade-offs when modeling a domain as interfaces vs. sealed types + records at a FAANG platform backend?

**A:** A platform backend (orders, payments, inventory, notifications) must pick the abstraction style per domain. The trade-off matrix:

**Interface-driven domain modeling:**
- + Polymorphism, dependency injection, seed points for frameworks (Spring beans implementing an interface), easier to add a new payment provider today.
- - Deep hierarchies risk fragile-base-class bugs; adding a method to an interface is a breaking change; runtime discovery is open (an unknown implementation can appear).

**Sealed + records + pattern matching:**
- + Compiler-enforced exhaustiveness (adding `Refund` breaks every switch — which is GOOD, it surfaces missing logic), immutable state carriers, no deep hierarchies (each variant is a record), easier to test as pure functions.
- - Cannot add new variants from other modules; open-world extension requires an escape hatch (`non-sealed`); API shape is locked by the sealed permits.

**Guiding scenario — a payment domain:**

```java
public sealed interface Charge permits CardCharge, WalletCharge, UpiCharge {}
public record CardCharge(Card card, Money amount, ...) implements Charge {}
public record WalletCharge(WalletId w, Money amount, ...) implements Charge {}
public record UpiCharge(String vpa, Money amount, ...) implements Charge {}

// Operation as a function
Refund refund(Charge c) {
    return switch (c) {
        case CardCharge cc  -> c.cardRefund(cc);
        case WalletCharge wc -> w.refund(wc);
        case UpiCharge uc    -> uc.refund();             // can't refund → throw
    };
}
```

vs. interface-driven where each `Charge` subclass implements `refund()`.

The decision heuristic:
1. **Change cadence**: which axis changes more often — adding new variants (use interface + open hierarchy) or adding new operations (use sealed + switch)?
2. **Extensibility scope**: internal teams only (sealed, they register new variants), or external ISV ecosystems (interface + registry + verification)?
3. **Invariant enforcement**: records enforce immutability. Interfaces allow mutable state — if a domain requires immutable DTOs, records win.
4. **Leakage**: interfaces model behavior; sealed+records model DATA. Behaviors that outgrow the data (retry policy, idempotency handling) belong in a separate strategy layer.

Final architect answer: don't pick one globally. Use sealed+records for data types with a fixed, finite shape (error unions, response enums, event types). Use interfaces + composition for behavioral extension points (strategies, providers, adapters). Bridge them: an interface can return a sealed type, keeping behavior open while the data shape stays closed. This hybrid is the pragmatic FAANG-grade answer — closed data, open behavior, compiler-checked both ways.

