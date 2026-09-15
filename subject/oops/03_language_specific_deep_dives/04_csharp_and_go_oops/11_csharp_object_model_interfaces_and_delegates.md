# C# Object Model, Interfaces and Delegates — 100 Interview Q&A

## Q1: What is the difference between a class and a struct in C#?

**A:** In C#, a class is a reference type while a struct is a value type. When you create an instance of a class with `new`, the runtime allocates memory on the managed heap and returns a reference (pointer) to that memory. Variables of class types hold references, so assigning one variable to another copies the reference, not the underlying data. Both variables then point to the same object on the heap. When the garbage collector determines there are no more references to an object, it reclaims the memory.

A struct, by contrast, is allocated inline — wherever the variable is declared. For local variables, this means the struct lives on the stack. For class fields, the struct lives inline within the class's heap allocation. When you assign one struct variable to another, the entire value is copied bitwise. This means that modifications to one copy do not affect the other, which is often the desired behavior for small, immutable data containers. Structs cannot be null (unless declared as `Nullable<T>` or `T?`), and they do not support inheritance (though they can implement interfaces).

The choice between class and struct has performance implications. Structs avoid heap allocation and garbage collection overhead, making them ideal for small, short-lived values. However, large structs can be expensive to copy, and boxing (converting a struct to `object`) incurs allocation overhead. Microsoft recommends using structs for types that are smaller than 16 bytes, are immutable, and represent a single value. Types with complex behavior, inheritance, or polymorphism should be classes.

```csharp
// Reference type
class PointRef {
    public int X;
    public int Y;
}

// Value type
struct PointVal {
    public int X;
    public int Y;
}

var a = new PointRef { X = 1, Y = 2 };
var b = a;          // b references the same object
b.X = 10;
Console.WriteLine(a.X);  // 10 — both point to same object

var c = new PointVal { X = 1, Y = 2 };
var d = c;          // d is a copy
d.X = 10;
Console.WriteLine(c.X);  // 1 — c is unchanged
```

## Q2: Explain C#'s type system. What is the CTS (Common Type System)?

**A:** The Common Type System (CTS) is a specification that defines how types are declared, used, and managed in the .NET runtime. It establishes rules for type inheritance, interface implementation, type relationships, and cross-language interoperability. The CTS ensures that all .NET languages — C#, F#, VB.NET, and others — share a unified type system, so a class defined in C# can be used seamlessly in VB.NET and vice versa. The CTS defines two fundamental categories: reference types and value types.

Reference types in the CTS include classes, interfaces, delegates, arrays, and tuples. These are all allocated on the managed heap and accessed through references. Value types include primitives (`int`, `bool`, `char`), enums, structs, and records (in C# 9+). These are allocated inline and copied by value. The CTS also defines the rules for type membership: fields, methods, properties, events, constructors, and destructors. Every .NET type ultimately inherits from `System.Object`, which provides the base methods like `ToString()`, `Equals()`, and `GetHashCode()`.

The CTS enforces visibility rules through access modifiers: `public`, `private`, `protected`, `internal`, and `protected internal`. It also defines the rules for generic type constraints, variance (`in`/`out` on generic parameters), and nullable reference types (C# 8+). Understanding the CTS is important for interoperability between .NET languages and for understanding how .NET's JIT compiler and garbage collector manage types at runtime.

```csharp
// Both compile to CTS-compatible types
// C# struct
struct Coordinate { public double Lat; public double Lon; }

// CTS value type rule: structs cannot inherit
// but can implement interfaces
interface ILocatable { Coordinate Location { get; } }

// CTS reference type: class can inherit and implement
class Place : ILocatable {
    public Coordinate Location { get; set; }
}
```

## Q3: What are records in C# and how do they differ from classes?

**A:** Records, introduced in C# 9, are reference types with built-in value-based equality semantics. While a class uses reference equality by default (two variables are equal only if they point to the same object), a record uses structural equality — two record instances are equal if all their public properties match. Records also provide a `with` expression for creating modified copies, a concise `ToString()` override, and deconstruction support. These features make records ideal for modeling immutable data.

The `with` expression creates a shallow copy of a record with specified properties modified. This is particularly useful for immutable data patterns where you need to "update" a record by creating a new instance with some changes. The original record is not modified, which is consistent with functional programming patterns. Records can be declared with `record` (reference type) or `record struct` (value type, C# 10+), giving you flexibility in choosing between heap and stack allocation.

Records also support positional syntax, where you define properties in the constructor parameter list and they become init-only properties by default. This eliminates boilerplate for simple data carriers. The compiler automatically generates a `Deconstruct` method, `Equals`, `GetHashCode`, `ToString`, and `print` pattern matching support. However, records are still reference types — they are allocated on the heap and collected by the garbage collector. For truly immutable reference types, you should use `init` accessors on properties.

```csharp
public record Person(string Name, int Age);

var alice = new Person("Alice", 30);
var alice2 = new Person("Alice", 30);
Console.WriteLine(alice == alice2);   // True — value equality
Console.WriteLine(alice.Equals(alice2)); // True

var bob = alice with { Name = "Bob" };
Console.WriteLine(alice.Name);  // "Alice" — original unchanged
Console.WriteLine(bob.Name);    // "Bob"

// Deconstruction
var (name, age) = alice;
Console.WriteLine($"{name}: {age}");  // "Alice: 30"
```

## Q4: What is the difference between `abstract class` and `interface` in C#?

**A:** An abstract class can provide both abstract members (without implementation) and concrete members (with implementation). An interface, traditionally, could only contain abstract members — method signatures, properties, events, and indexers without implementation. Starting with C# 8, interfaces can provide default implementations for members, blurring the distinction. However, the fundamental difference remains: a class can inherit from only one abstract class (single inheritance) but can implement multiple interfaces (multiple inheritance of type).

Abstract classes are designed for partial implementation sharing. When you have a hierarchy of related types that share common behavior, an abstract class provides a place to put that shared code. For example, `Stream` is an abstract class in .NET that provides concrete implementations of methods like `CopyTo` while requiring subclasses to implement `Read` and `Write`. Interfaces, on the other hand, define contracts. They specify what a type can do without specifying how. This makes interfaces more suitable for defining capabilities that unrelated types can implement, such as `IDisposable` or `IComparable<T>`.

Another key difference is that abstract classes can have constructors, fields, and non-public members, while interfaces cannot (they can only have public members, though C# 8+ allows explicit interface implementations and static abstract members). Abstract classes can also have state (fields), while interfaces cannot. When designing a system, use abstract classes for "is-a" relationships with shared implementation, and interfaces for "can-do" contracts. Modern C# design often favors interfaces over abstract classes for flexibility, reserving abstract classes for cases where shared implementation is essential.

```csharp
// Abstract class: partial implementation
public abstract class Animal {
    public string Name { get; set; }
    public abstract void Speak();  // No implementation
    public void Describe() =>      // Has implementation
        Console.WriteLine($"{Name} is an animal");
}

// Interface: contract with default implementation (C# 8+)
public interface IAnimated {
    void Animate() =>
        Console.WriteLine("Animating...");
}

public class Dog : Animal, IAnimated {
    public override void Speak() =>
        Console.WriteLine("Woof!");
}
```

## Q5: How do delegates work in C#, and what is their relationship to function pointers?

**A:** A delegate in C# is a type-safe, object-oriented wrapper around a method reference. When you declare a delegate type (e.g., `delegate void MyDelegate(int x)`), the compiler generates a class that inherits from `System.MulticastDelegate`. A delegate instance holds a reference to one or more methods, along with the target object (for instance methods) or nothing (for static methods). When you invoke a delegate, it calls all of its subscribed methods in order.

Delegates are fundamentally different from C-style function pointers. Function pointers are raw memory addresses with no type safety, no object context, and no support for multiple targets. Delegates are type-safe (the compiler verifies that the method signature matches the delegate signature), they carry the target object's context (so you can invoke instance methods), and they support multicast (subscribing multiple methods to a single delegate). Internally, delegates use the `Invoke` method, which handles null checks, target object binding, and argument validation.

The `System` namespace provides two built-in delegate types: `Action<T>` (for methods that return void) and `Func<T, TResult>` (for methods that return a value). These generic delegates eliminate the need to declare custom delegate types for most scenarios. C# also provides `Predicate<T>` (for boolean-returning methods) and `EventHandler<T>` (for event patterns). Modern C# code almost never declares custom delegate types, using `Action` and `Func` instead. Understanding delegates is essential because they underpin events, LINQ queries, async/await patterns, and lambda expressions.

```csharp
// Custom delegate
delegate int MathOp(int a, int b);

// Using built-in delegates
Func<int, int, int> add = (a, b) => a + b;
Action<string> greet = name => Console.WriteLine($"Hello, {name}");

// Multicast
Action combined = () => Console.Write("A");
combined += () => Console.Write("B");
combined();  // "AB"

MathOp op = (a, b) => a + b;
Console.WriteLine(op(3, 4));  // 7
```

## Q6: What is the difference between `Action`, `Func`, and `Predicate` delegates?

**A:** `Action<T>` is a delegate for methods that return `void`. It can have zero to sixteen type parameters: `Action()` for no parameters, `Action<int>` for one, `Action<int, string>` for two, and so on. `Action` is used for callbacks, event handlers, and methods that perform side effects without returning a value. In LINQ, `Action` is commonly used with `ForEach` to iterate over collections and perform operations on each element.

`Func<T, TResult>` is a delegate for methods that return a value. The last type parameter is always the return type: `Func<int>` for a parameterless method returning `int`, `Func<string, int>` for a method taking a string and returning an `int`, and so on. `Func` can also have zero to sixteen input parameters. In LINQ, `Func` is used extensively — `Select`, `Where`, `OrderBy`, and other operators accept `Func<T, bool>` or `Func<T, TResult>` predicates.

`Predicate<T>` is a specialized delegate that takes a single parameter and returns `bool`. It is semantically identical to `Func<T, bool>` but conveys intent more clearly — it represents a test or condition. `Predicate<T>` is used by `Array.Find`, `List<T>.Find`, `List<T>.Exists`, and `List<T>.TrueForAll`. While `Predicate<T>` and `Func<T, bool>` are interchangeable in terms of functionality, `Predicate<T>` is preferred in APIs where the parameter represents a boolean test, as it communicates the intent more precisely.

```csharp
// Action: no return value
Action<string, int> log = (msg, level) =>
    Console.WriteLine($"[{level}] {msg}");
log("Hello", 1);

// Func: returns a value
Func<int, int, int> multiply = (a, b) => a * b;
Console.WriteLine(multiply(3, 4));  // 12

// Predicate: boolean test
Predicate<int> isEven = n => n % 2 == 0;
Console.WriteLine(isEven(4));  // True

// Practical usage
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var evens = numbers.FindAll(isEven);  // [2, 4]
```

## Q7: Explain the concept of boxing and unboxing in C#. When does it happen implicitly?

**A:** Boxing is the process of converting a value type to a reference type — specifically, wrapping the value type inside an `object` instance on the managed heap. When you write `object o = 42;`, the runtime allocates memory on the heap, copies the integer value 42 into that memory, and returns a reference to it. The value 42 now lives on the heap as part of an `object`, and the variable `o` holds a reference to it. Boxing incurs allocation and copying overhead.

Unboxing is the reverse: extracting the value type from the object. When you write `int i = (int)o;`, the runtime first verifies that `o` is a boxed `int`, then extracts the value. Unboxing requires an explicit cast and throws `InvalidCastException` if the type does not match. Unboxing itself is cheap (just a type check and memory access), but the combination of boxing and unboxing is significantly more expensive than working with the value type directly.

Boxing happens implicitly in several scenarios: when a value type is assigned to a variable of type `object`, `dynamic`, or any interface type; when a value type is passed as a parameter to a method that accepts `object` or interface parameters; when a value type is used in string interpolation or concatenation (the `ToString()` call may involve boxing); and when a value type is used in a non-generic collection like `ArrayList`. In .NET, the JIT compiler can sometimes eliminate boxing through optimizations like "generic caching" (where `List<int>` does not box each element), but developers should be aware of these scenarios and prefer generics over non-generic collections to avoid unnecessary boxing.

```csharp
int value = 42;

// Implicit boxing
object boxed = value;          // Boxing
IComparable comparable = value; // Boxing (interface)

// Unboxing (requires explicit cast)
int unboxed = (int)boxed;      // Unboxing

// Boxing in string interpolation
string s = $"Value: {value}";  // May box if ToString is not specialized

// Avoid boxing with generics
var list = new List<int>();     // No boxing
list.Add(42);
var arrayList = new ArrayList();
arrayList.Add(42);              // Boxes 42 to object
```

## Q8: What are events in C# and how do they relate to delegates?

**A:** Events are a special kind of delegate member that provides a controlled subscription and unsubscription mechanism. While a delegate field can be directly assigned (replacing all subscribers), an event only allows `+=` (subscribe) and `-=` (unsubscribe) operations from outside the declaring class. This encapsulation ensures that external code cannot accidentally overwrite the subscriber list or invoke the delegate directly. Events are the C# implementation of the observer pattern and are fundamental to UI frameworks, async programming, and inter-component communication.

Internally, an event is a delegate field with restricted access. When you write `public event EventHandler Click;`, the compiler generates a private delegate field and public `add`/`remove` accessors (similar to property getters and setters). From inside the declaring class, you can invoke the event like a regular delegate (`Click?.Invoke(this, EventArgs.Empty)`). From outside, you can only subscribe or unsubscribe. This asymmetry is a core design principle — only the class that declares the event should raise it.

Events are built on top of delegates and use them as their underlying mechanism. The `EventHandler` and `EventHandler<TEventArgs>` delegates are the standard types used for events. Custom event delegate types can be defined, but the `EventHandler` pattern is preferred for consistency. Events also support the `event` keyword in interface declarations, allowing interfaces to define events that implementing classes must provide. The relationship between events and delegates is fundamental to understanding C#'s component-based programming model.

```csharp
public class Button {
    // Event backed by a delegate
    public event EventHandler Click;

    // Raising the event (only inside the class)
    public void OnClick() {
        Click?.Invoke(this, EventArgs.Empty);
    }
}

// Usage
var btn = new Button();
btn.Click += (sender, args) => Console.WriteLine("Clicked!");
btn.OnClick();  // "Clicked!"

// btn.Click();  // Error: cannot invoke from outside
// btn.Click = null;  // Error: cannot assign from outside
```

## Q9: What is the difference between `virtual`, `override`, `abstract`, and `sealed` methods?

**A:** `virtual` methods are methods in a base class that can be overridden by derived classes. They provide a default implementation but allow subclasses to provide their own. When you call a virtual method on an instance, the runtime determines the actual type of the object and calls the most-derived implementation through virtual dispatch (dynamic binding). This is the mechanism that enables polymorphism — the ability to treat objects of different types uniformly through a common base type.

`override` methods are methods in a derived class that replace the implementation of a virtual or abstract method from the base class. The `override` keyword explicitly indicates that you are replacing a base class implementation. The compiler verifies that the base method is indeed virtual or abstract. Override methods can call the base implementation using `base.Method()` when partial behavior reuse is desired. Multiple levels of inheritance can each override the same method, creating a chain of implementations.

`abstract` methods are methods declared in an abstract class without an implementation. Derived classes must provide an implementation using the `override` keyword. Abstract methods force subclasses to provide specific behavior while allowing the base class to define the contract. `sealed` methods (applied to an override) prevent further overriding in derived classes. When you seal a method, no class further down the hierarchy can override it. Sealing is useful for performance optimization (the compiler can devirtualize the call) and for enforcing invariants in the implementation.

```csharp
public class Shape {
    public virtual double Area() => 0;      // Can be overridden
    public abstract double Perimeter();     // Must be overridden
}

public class Circle : Shape {
    public double Radius { get; set; }

    public override double Area() =>
        Math.PI * Radius * Radius;

    public sealed override double Perimeter() =>
        2 * Math.PI * Radius;  // Cannot be overridden further
}

public class Ellipse : Circle {
    // Cannot override Perimeter — it's sealed
}
```

## Q10: Explain interface default implementations in C# 8+. What problem do they solve?

**A:** Interface default implementations (C# 8+) allow interfaces to provide method bodies that implementing classes can use without explicitly implementing the method. Before C# 8, adding a new method to an interface would break all existing implementations because they would not have the required method. Default implementations solve this "interface evolution" problem by allowing interfaces to add new methods with bodies, so existing implementations continue to compile and work.

Default implementations are accessed through the interface itself, not through the implementing class. If `IMyInterface` has a default method `DoSomething()`, and `MyClass` does not override it, you must call it as `((IMyInterface)instance).DoSomething()`. You cannot call `instance.DoSomething()` directly — the method is not "in" the class, it is in the interface. This distinction is important: default implementations are not inherited in the traditional sense. They exist in the interface's method table and are dispatched through the interface, not through the class's virtual dispatch table.

Default implementations have several limitations: they cannot access instance state of the implementing class (the interface does not have access to `this`), they cannot be overridden with `override` (they can only be "hidden" with `new` or explicitly reimplemented), and they are not visible to classes that implement the interface. Despite these limitations, they are valuable for evolving interfaces without breaking backward compatibility, especially in large codebases or public APIs where many implementations exist. They are also useful for providing helper methods or extension-like behavior directly on interfaces.

```csharp
public interface ILogger {
    void Log(string message);

    // Default implementation
    void LogWarning(string message) =>
        Log($"[WARN] {message}");

    void LogError(string message) =>
        Log($"[ERROR] {message}");
}

public class ConsoleLogger : ILogger {
    public void Log(string message) =>
        Console.WriteLine(message);
    // Inherits LogWarning and LogError defaults
}

var logger = new ConsoleLogger();
logger.LogWarning("disk full");
// Output: [WARN] disk full

// Default methods accessed through interface
ILogger iLogger = logger;
iLogger.LogError("crash");
// Output: [ERROR] crash
```

## Q11: What is the difference between `==` and `Equals()` in C#?

**A:** The `==` operator and the `Equals()` method can behave differently depending on the type. For reference types, the default behavior of `==` is reference comparison — it checks whether both variables point to the same object in memory. The default behavior of `Equals()` (inherited from `Object`) is also reference comparison. However, `Equals()` is a virtual method that can be overridden to provide custom equality logic, while `==` is a static operator that can be overloaded.

For strings, both `==` and `Equals()` perform value comparison because the `string` class overrides both. For value types, `==` performs bitwise comparison (if the operator is not overloaded) while `Equals()` uses reflection-based comparison (which is slower). The `Equals()` method is also used by collections, serialization, and LINQ, so overriding it without also overloading `==` can lead to inconsistent behavior where `a.Equals(b)` is true but `a == b` is false.

A best practice is to always override both `==` and `Equals()` together when implementing custom equality logic. The `IEquatable<T>` interface provides a type-safe `Equals` method that avoids boxing for value types. The `GetHashCode()` method must also be overridden whenever `Equals()` is overridden, because hash-based collections (dictionaries, hash sets) rely on the invariant that equal objects have equal hash codes. Failing to maintain this invariant causes subtle bugs where objects are "lost" in hash-based collections.

```csharp
class Money {
    public decimal Amount { get; set; }
    public string Currency { get; set; }

    public override bool Equals(object obj) {
        if (obj is not Money other) return false;
        return Amount == other.Amount &&
               Currency == other.Currency;
    }

    public override int GetHashCode() =>
        HashCode.Combine(Amount, Currency);

    public static bool operator ==(Money a, Money b) {
        if (a is null) return b is null;
        return a.Equals(b);
    }

    public static bool operator !=(Money a, Money b) =>
        !(a == b);
}

var a = new Money { Amount = 10, Currency = "USD" };
var b = new Money { Amount = 10, Currency = "USD" };
Console.WriteLine(a == b);      // True
Console.WriteLine(a.Equals(b)); // True
```

## Q12: What are extension methods and how do they relate to interfaces?

**A:** Extension methods are static methods that appear to be instance methods on a type, but are defined externally in a static class. They are called using the same syntax as instance methods (`instance.ExtensionMethod()`), but the compiler translates the call into a static method call (`StaticClass.ExtensionMethod(instance)`). Extension methods were introduced in C# 3 to enable LINQ and are defined with the `this` keyword on the first parameter, which specifies the type being extended.

Extension methods are resolved at compile time based on the declared type of the variable, not the runtime type. This means they cannot override existing instance methods — if a type already has an instance method with the same signature, the instance method always wins. Extension methods also cannot access private or protected members of the extended type. They are essentially syntactic sugar for static method calls, which makes them powerful for adding functionality to sealed classes or types you do not own.

The relationship to interfaces is significant. Extension methods can be defined on interface types, allowing you to add default behavior to all implementors of an interface. LINQ's entire API is built on extension methods defined on `IEnumerable<T>` and `IQueryable<T>`. When you call `source.Where(x => x > 5)`, you are calling an extension method on `IEnumerable<T>`. This pattern is so common that it is considered a core part of modern C# design. However, extension methods on interfaces cannot access instance state, similar to interface default implementations.

```csharp
public static class StringExtensions {
    public static bool IsNullOrEmpty(this string s) =>
        string.IsNullOrEmpty(s);

    public static string Truncate(this string s, int maxLen) =>
        s.Length <= maxLen ? s : s[..maxLen];
}

// Usage — looks like an instance method
string name = "Alice";
Console.WriteLine(name.IsNullOrEmpty());  // False
Console.WriteLine("Hello World".Truncate(5));  // "Hello"

// LINQ is built on extension methods
var numbers = new[] { 1, 2, 3, 4, 5 };
var evens = numbers.Where(n => n % 2 == 0);
```

## Q13: Explain covariance and contravariance in C# generics.

**A:** Covariance and contravariance describe how generic type parameters relate to inheritance. Covariance (`out` keyword) allows a generic type to "preserve" the direction of inheritance — if `Dog` derives from `Animal`, then `IEnumerable<Dog>` is assignable to `IEnumerable<Animal>`. Contravariance (`in` keyword) reverses the direction — `Action<Animal>` is assignable to `Action<Dog>` because a method that handles any `Animal` can certainly handle a `Dog`.

Covariance is safe for output positions (methods that return values). When a generic type parameter is marked `out`, it can only appear in output positions (return types, `out` parameters). This ensures that the generic type is only "produced" by the generic container, never consumed. `IEnumerable<out T>` is covariant because it only yields `T` values. This is why you can iterate over `IEnumerable<Dog>` and treat each element as an `Animal`.

Contravariance is safe for input positions (methods that accept values). When a generic type parameter is marked `in`, it can only appear in input positions (method parameters). This ensures that the generic type is only "consumed" by the generic container. `Action<in T>` is contravariant because it accepts `T` values. This is why an `Action<Animal>` can be assigned to a variable of type `Action<Dog>` — the action expects an `Animal`, and a `Dog` is an `Animal`. Invariant types (no `in` or `out`) allow the type parameter to appear in both positions.

```csharp
// Covariance: out T — can only produce T
IEnumerable<Dog> dogs = new List<Dog>();
IEnumerable<Animal> animals = dogs;  // OK: covariant

// Contravariance: in T — can only consume T
Action<Animal> feedAnimal = a => Console.WriteLine("Feeding");
Action<Dog> feedDog = feedAnimal;  // OK: contravariant
feedDog(new Dog());  // Works

// Invariant: T in both positions
List<Animal> animalList = new List<Dog>();  // Error!
// List<T> is invariant — can't be covariant or contravariant
```

## Q14: What is the `dynamic` keyword in C# and how does it differ from `object`?

**A:** The `dynamic` keyword (C# 4+) bypasses compile-time type checking and defers all type resolution to runtime. When you declare a variable as `dynamic`, the compiler emits code that uses the Dynamic Language Runtime (DLR) to resolve types, members, and operations at execution time. This enables interoperability with dynamic languages (IronPython, IronRuby), COM objects, and scenarios where types are not known at compile time.

The key difference from `object` is that `object` requires explicit casts to access members, and the compiler verifies the cast at compile time. `dynamic` skips this entirely — the compiler generates no type checking for `dynamic` expressions. If you call `obj.Method()` where `obj` is `dynamic`, the DLR will search for `Method` at runtime and throw `RuntimeBinderException` if it is not found. With `object`, you would need to cast to a specific type first: `((MyType)obj).Method()`.

`dynamic` has significant performance implications. Every operation on a `dynamic` variable involves DLR lookup, caching, and potential fallback to reflection. This is much slower than statically typed access. However, it is faster than raw reflection because the DLR caches call sites after the first resolution. The trade-off is flexibility versus performance — `dynamic` is useful for prototyping, scripting, and COM interop, but should be avoided in performance-critical code. `dynamic` also does not support IntelliSense, which is a productivity cost.

```csharp
// object: compile-time safety, explicit casts
object obj = "hello";
int len = ((string)obj).Length;  // Must cast

// dynamic: runtime resolution, no casts
dynamic dyn = "hello";
int len2 = dyn.Length;  // Resolved at runtime

// COM interop example
dynamic excel = Activator.CreateInstance(
    Type.GetTypeFromProgID("Excel.Application"));
excel.Visible = true;
excel.Workbooks.Add();  // No IntelliSense, but works
```

## Q15: What are the access modifiers in C#, and how do they relate to assembly boundaries?

**A:** C# defines six access modifiers: `public`, `private`, `protected`, `internal`, `protected internal`, and `private protected`. `public` is accessible from anywhere. `private` is accessible only within the declaring type. `protected` is accessible within the declaring type and derived types. `internal` is accessible within the same assembly (project). `protected internal` is accessible within the same assembly OR from derived types (union). `private protected` is accessible within the same assembly AND from derived types (intersection, C# 7.2+).

Assembly boundaries are a key concept for understanding `internal` and `protected internal`. An assembly in .NET is the output of a compilation — typically a DLL or EXE. Types marked `internal` are visible only within that assembly. This is the C# equivalent of "package-private" in Java. The `[InternalsVisibleTo]` attribute can be used to expose internal members to specific assemblies, which is commonly used for unit testing (exposing internals to a test project).

The distinction between `protected internal` and `private protected` is subtle but important. `protected internal` means "accessible to derived types OR anything in the same assembly" — it is a union of the two scopes. `private protected` means "accessible to derived types that are also in the same assembly" — it is an intersection. `private protected` is more restrictive and is useful when you want to expose members to subclasses but only if they are in the same assembly (preventing external assemblies from inheriting and accessing the member).

```csharp
// Assembly: MyApp.dll
public class Base {
    public int A;           // Everywhere
    private int B;          // Only Base
    protected int C;        // Base + derived types
    internal int D;         // Only MyApp.dll
    protected internal int E; // Derived OR MyApp.dll
    private protected int F;  // Derived AND MyApp.dll
}

// Assembly: External.dll
public class Derived : Base {
    void Test() {
        // A = 1;   // OK
        // B = 1;   // Error: private
        // C = 1;   // OK: protected
        // D = 1;   // Error: different assembly
        // E = 1;   // OK: derived type
        // F = 1;   // Error: different assembly
    }
}
```

## Q16: How does C# implement multiple interface inheritance, and what are the diamond problem implications?

**A:** C# allows a class to implement multiple interfaces but only inherit from one base class. This is the "interface-based multiple inheritance" model. When a class implements multiple interfaces, it must provide implementations for all interface members (unless the interface has a default implementation). The class's type hierarchy is linear (single class inheritance), but its interface set is a flat collection of contracts it fulfills.

The diamond problem in C# occurs when a class inherits from two interfaces that both declare a method with the same signature. C# resolves this through explicit interface implementation. If `IA` and `IB` both declare `void Do()`, the implementing class can provide a single implementation that satisfies both, or it can provide separate implementations using explicit interface syntax: `void IA.Do() { ... }` and `void IB.Do() { ... }`. Explicit implementations are only accessible through the interface type, not through the class type, which prevents ambiguity.

C# also has a related issue with default interface implementations (C# 8+). If a class inherits from a base class that provides a method implementation and also implements an interface that has a default implementation of the same method, the class's own implementation (or the base class's, if the class does not override) takes precedence. The interface default is only used if neither the class nor its base class provides an implementation. This avoids the diamond problem by establishing a clear precedence order: class implementation > base class implementation > interface default.

```csharp
interface IReadable {
    void Read() => Console.WriteLine("Reading from interface");
}

interface IWritable {
    void Write() => Console.WriteLine("Writing from interface");
}

class FileHandler : IReadable, IWritable {
    // Single implementation satisfies both
    public void Read() => Console.WriteLine("Reading file");
    public void Write() => Console.WriteLine("Writing file");
}

// Explicit interface implementation
class DualHandler : IReadable, IWritable {
    void IReadable.Read() => Console.WriteLine("IReadable.Read");
    void IWritable.Write() => Console.WriteLine("IWritable.Write");
}

DualHandler d = new DualHandler();
// d.Read();  // Error: not accessible through class type
((IReadable)d).Read();  // "IReadable.Read"
```

## Q17: What is the `record` type's equality semantics, and how does it differ from reference equality?

**A:** Records in C# implement value-based equality by default. When you compare two record instances using `==` or `Equals()`, the compiler generates code that compares all public properties (and fields) for equality, similar to how value types are compared. This is fundamentally different from the default reference equality behavior of classes, where two variables are equal only if they point to the same object in memory. Record equality is structural — two records are equal if they have the same data, regardless of whether they are the same object.

The compiler generates `EqualityContract` and property-by-property comparison in the `Equals` method. For positional records, all positional parameters are compared. For non-positional records, all public properties are compared. The `GetHashCode()` method is also generated to combine the hash codes of all compared properties. This ensures that equal records have equal hash codes, which is essential for correct behavior in hash-based collections.

Record equality has some nuances. It performs shallow comparison — nested reference types are compared by reference, not by value. Two records with the same data but different object references for nested types will not be equal unless the nested types also override equality. Value type properties are compared by value. `null` properties are handled correctly — two records with `null` in the same property position are equal. Records also support `is` pattern matching for type checks and deconstruction, which integrates with the equality model.

```csharp
public record Address(string Street, string City);
public record Person(string Name, Address Address);

var a1 = new Person("Alice", new Address("123 Main", "NYC"));
var a2 = new Person("Alice", new Address("123 Main", "NYC"));
var a3 = new Person("Alice", new Address("456 Oak", "LA"));

Console.WriteLine(a1 == a2);  // True — value equality
Console.WriteLine(a1 == a3);  // False — different address
Console.WriteLine(ReferenceEquals(a1, a2));  // False — different objects

// Nested records: shallow comparison
var b1 = new Person("Alice", a1.Address);
Console.WriteLine(a1 == b1);  // True — same address object
```

## Q18: What are primary constructors in C# 12, and how do they differ from traditional constructors?

**A:** Primary constructors (C# 12) allow you to declare constructor parameters directly in the type declaration syntax. For classes: `class MyClass(int x, string y)` and for records: `record Person(string Name, int Age)`. The parameters are in scope throughout the entire class body, which means they can be used in field initializers, property initializers, and method bodies without being explicitly stored in fields. This eliminates a significant amount of boilerplate for simple types.

The key difference from traditional constructors is that primary constructor parameters are not automatically stored as fields. If you need to access a parameter's value outside of the constructor or field initializers, you must explicitly assign it to a field or property. This is a deliberate design choice — it encourages immutability (you can use `init` properties or `required` properties) and avoids hidden allocations. Traditional constructors require you to declare fields explicitly and assign parameters to them, which is more verbose but more explicit about storage.

Primary constructors interact with other C# features. In records, primary constructors automatically generate properties for the parameters. In classes, the parameters are captured in a hidden display class only if they are used outside the constructor. This means there is no performance penalty if you only use the parameters in field initializers. Primary constructors also work with `base()` and `this()` constructor chaining, and they support `required` parameters. The feature is primarily syntactic sugar that reduces verbosity while maintaining the same semantics as traditional constructors.

```csharp
// Primary constructor (C# 12)
public class Service(HttpClient client, ILogger logger) {
    // Parameters available throughout the class
    public async Task<string> GetAsync(string url) {
        logger.Log($"Fetching {url}");
        return await client.GetStringAsync(url);
    }
}

// Traditional constructor — same semantics, more verbose
public class ServiceTraditional {
    private readonly HttpClient _client;
    private readonly ILogger _logger;

    public ServiceTraditional(HttpClient client, ILogger logger) {
        _client = client;
        _logger = logger;
    }
}

// Record with primary constructor
public record Point(double X, double Y);
var p = new Point(1.0, 2.0);
Console.WriteLine(p.X);  // 1.0
```

## Q19: How do `async` and `await` interact with delegates and events?

**A:** `async` and `await` in C# are built on top of delegates and the `Task`-based asynchronous pattern. An `async` method returns a `Task` or `Task<T>` (or `ValueTask<T>` for performance-sensitive scenarios). The compiler transforms the method body into a state machine that can suspend execution at `await` points and resume when the awaited operation completes. This state machine is implemented as a struct (for `ValueTask`) or class (for `Task`) that captures the execution context.

The interaction with delegates is that `Func<Task<T>>` is commonly used to represent asynchronous methods. LINQ does not support `async` lambdas directly, but libraries like `System.Linq.Async` extend LINQ to work with `IAsyncEnumerable<T>`. Events can also use async handlers — when an event handler is `async void`, it runs asynchronously without blocking the event raiser. However, `async void` handlers are dangerous because exceptions cannot be caught by the caller. The recommended pattern is to use `async Task` event handlers and manage them through a helper method.

Async delegates are particularly useful in scenarios like parallel processing. `Task.WhenAll` accepts an array of `Task` objects, allowing you to run multiple async operations concurrently. You can create delegates that return `Task` and invoke them in parallel. The `AsyncLocal<T>` class provides context-local storage that flows across async continuations, enabling patterns like correlation IDs in distributed systems. Understanding the interaction between async/await and delegates is essential for building responsive, scalable applications.

```csharp
// Async delegate
Func<int, Task<string>> fetchAsync = async id => {
    await Task.Delay(100);
    return $"Data for {id}";
};

// Async event handler pattern
public class DownloadManager {
    public event Func<string, Task> DownloadCompleted;

    public async Task StartDownload(string url) {
        await Task.Delay(1000);
        if (DownloadCompleted != null)
            await DownloadCompleted(url);  // Await all handlers
    }
}

// Parallel async with delegates
var tasks = Enumerable.Range(1, 5)
    .Select(id => fetchAsync(id))
    .ToArray();
var results = await Task.WhenAll(tasks);
```

## Q20: What is the difference between `is` and `as` operators in C#?

**A:** The `is` operator checks whether a variable is of a specified type and returns a boolean. It does not perform any conversion — it simply checks the runtime type. `as` performs a runtime type check and returns the converted object if the check succeeds, or `null` if the conversion fails. The fundamental difference is that `is` is a boolean test, while `as` is a test-and-convert operation.

`is` is commonly used in pattern matching (C# 7+). You can write `if (obj is string s)` which checks if `obj` is a `string` and assigns the converted value to `s` in a single expression. This eliminates the need for separate `is` check and cast operations. `is` also works with constant patterns (`if (status is "OK")`), type patterns, and property patterns. The pattern matching syntax makes `is` more powerful than a simple type check.

`as` is useful when you want to convert an object and use the result, but you are not sure the conversion will succeed. Unlike a direct cast (`(string)obj`), `as` does not throw `InvalidCastException` on failure — it returns `null`. This makes `as` useful for conditional logic where you want to attempt a conversion without exception handling. However, `as` only works with reference types and nullable value types. For value types, you should use `is` with pattern matching or the `Convert` class instead.

```csharp
object obj = "hello";

// is: boolean check (with pattern matching)
if (obj is string s)
    Console.WriteLine(s.Length);  // 5

// as: conversion attempt (returns null on failure)
string str = obj as string;
Console.WriteLine(str?.Length);  // 5

string num = obj as string;  // null (obj is not int)
// int len = obj as int;  // Error: as doesn't work with value types

// is with constant pattern
if (obj is "hello")
    Console.WriteLine("Exact match");

// is with property pattern (C# 8+)
if (obj is string { Length: > 3 } longStr)
    Console.WriteLine($"Long string: {longStr}");
```

## Q21: Explain the `init` accessor and how it enables immutable properties.

**A:** The `init` accessor (C# 9) allows a property to be set only during object initialization, not afterward. It is syntactically similar to `set`, but after the object's constructor and initializer expressions complete, the property becomes read-only. This enables immutable object patterns without requiring constructor parameters for every property. `init` properties can be set in object initializers (`new Person { Name = "Alice" }`) but cannot be changed later (`person.Name = "Bob"` would be a compile error).

`init` works by generating a hidden `IsInitialized` flag that the runtime checks during assignment. The compiler generates code that sets this flag to `true` after the constructor and all initializer expressions complete. Any subsequent assignment attempt throws `InvalidOperationException`. This is a runtime check, not a compile-time one, because the compiler cannot always determine whether an assignment is inside or outside the initialization context.

`init` properties are particularly useful with records, where they are the default for positional record properties. They are also useful with `required` properties (C# 11), which ensure that a property is set during initialization. The combination of `init` and `required` gives you compile-time guarantees that immutable objects are fully initialized. `init` properties can also have backing fields with custom logic, making them more flexible than constructor-only initialization for types with many optional parameters.

```csharp
public class Person {
    public string Name { get; init; }
    public int Age { get; init; }
}

var person = new Person { Name = "Alice", Age = 30 };
// person.Name = "Bob";  // Error: init-only property

// Required + init (C# 11)
public class Config {
    public required string Host { get; init; }
    public int Port { get; init; } = 8080;
}

var config = new Config { Host = "localhost" };
// config.Host = "other";  // Error: init-only

// Record: init by default
public record Point(double X, double Y);
```

## Q22: What are `Span<T>` and `Memory<T>`, and why are they important for performance?

**A:** `Span<T>` and `Memory<T>` are stack-only and heap-friendly types that represent contiguous regions of memory without allocating a new array. `Span<T>` is a ref struct (lives only on the stack) that wraps a pointer and a length, enabling zero-allocation slicing, parsing, and manipulation of arrays, strings, and other memory regions. `Memory<T>` is the heap-friendly counterpart that can be stored in fields, passed to async methods, and used in more flexible contexts.

`Span<T>` is important because it eliminates the allocation overhead of creating sub-arrays. Before `Span<T>`, taking a slice of an array required creating a new array with `Array.Copy`, which allocated memory on the heap and put pressure on the garbage collector. With `Span<T>`, slicing is a zero-allocation operation — the span simply adjusts its internal pointer and length. This is critical in high-performance scenarios like parsing, networking, and file I/O, where millions of small allocations can cause significant GC pauses.

`Memory<T>` and `ReadOnlyMemory<T>` extend these benefits to scenarios where stack-only is not sufficient. They can be stored in async state machines, used as method return types, and passed across async boundaries. `Memory<T>.Pin()` can be used to get a `MemoryHandle` for interop with native code. Together, `Span<T>` and `Memory<T>` form the foundation of modern .NET's high-performance APIs, including `System.Text.Json`, `System.IO.Pipelines`, and `Microsoft.AspNetCore.Http`.

```csharp
// Span<T>: zero-allocation slicing
int[] numbers = { 1, 2, 3, 4, 5 };
Span<int> slice = numbers.AsSpan(1, 3);  // [2, 3, 4]
slice[0] = 99;  // Modifies original array
Console.WriteLine(numbers[1]);  // 99

// String parsing without allocations
ReadOnlySpan<char> text = "12345".AsSpan();
int parsed = int.Parse(text.Slice(1, 2));  // 23

// Memory<T>: heap-friendly
async Task ProcessAsync(Memory<byte> buffer) {
    await SomeIOOperationAsync(buffer);
}
```

## Q23: How does C# implement the observer pattern with events and delegates?

**A:** The observer pattern in C# is implemented using events and delegates. An event is a delegate member with restricted access (only `+=` and `-=` from outside the class). The "subject" class declares an event, and "observers" subscribe to it using `+=`. When the subject raises the event (by calling `EventName?.Invoke(sender, args)`), all subscribed observers are notified. This decouples the subject from its observers — the subject does not need to know anything about the observers beyond their method signatures.

The standard pattern uses the `EventHandler` or `EventHandler<TEventArgs>` delegate types. `EventHandler` takes `object sender` and `EventArgs e` as parameters. `EventHandler<TEventArgs>` is the generic version that takes a specific `EventArgs`-derived type. Custom event args classes carry event-specific data. The subject raises the event by invoking the delegate, and the null-conditional operator (`?.`) ensures thread safety by checking for null subscribers before invocation.

Event-based observer patterns have some considerations. If a subscriber throws an exception, it prevents subsequent subscribers from being notified (unless the subject catches exceptions). Event handlers are invoked synchronously by default, which can cause performance issues if handlers are slow. The subject can use `Dispatcher.Invoke` or similar mechanisms for asynchronous notification. Memory leaks can occur if subscribers do not unsubscribe, as the event holds a reference to the subscriber. Weak event patterns and `WeakReference` can mitigate this.

```csharp
public class TemperatureSensor {
    public event EventHandler<TemperatureChangedEventArgs> TemperatureChanged;

    private double _temperature;
    public double Temperature {
        get => _temperature;
        set {
            if (_temperature != value) {
                _temperature = value;
                TemperatureChanged?.Invoke(this,
                    new TemperatureChangedEventArgs(value));
            }
        }
    }
}

public class TemperatureChangedEventArgs : EventArgs {
    public double Temperature { get; }
    public TemperatureChangedEventArgs(double temp) =>
        Temperature = temp;
}

// Observer subscription
var sensor = new TemperatureSensor();
sensor.TemperatureChanged += (sender, e) =>
    Console.WriteLine($"Temperature: {e.Temperature}°C");
sensor.Temperature = 25.5;  // Notifies observers
```

## Q24: What is the difference between `yield return` and returning a collection?

**A:** `yield return` creates an iterator that produces values lazily on demand, rather than materializing an entire collection in memory at once. When a method uses `yield return`, the compiler generates a state machine class that implements `IEnumerable<T>` (or `IEnumerator<T>`). Each time the caller requests the next element (via `MoveNext()`), the state machine resumes execution after the last `yield return`, executes until the next `yield return`, and yields the value.

The key difference is memory efficiency. A method that returns a `List<T>` must create the entire list before returning, consuming memory proportional to the number of elements. An iterator method with `yield return` produces one element at a time, consuming constant memory regardless of the total number of elements. This is critical for large or infinite sequences. For example, you can create an iterator that produces Fibonacci numbers indefinitely — the caller can take as many as needed without allocating an infinite list.

Iterator methods also support deferred execution. The code in an iterator method does not execute when the method is called — it executes when the first element is requested. This means side effects (like logging or database queries) happen at enumeration time, not at method call time. This can be surprising if you expect the method to execute immediately. `yield break` signals the end of the iteration early. The compiler-generated state machine handles `try/finally` blocks for cleanup, which is why `using` statements work correctly inside iterators.

```csharp
// Iterator method: lazy, memory-efficient
static IEnumerable<int> Fibonacci() {
    int a = 0, b = 1;
    while (true) {
        yield return a;
        (a, b) = (b, a + b);
    }
}

// Take only what you need
var first10 = Fibonacci().Take(10).ToList();
// [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

// Compare: eager method allocates entire list
static List<int> FibonacciEager(int count) {
    var list = new List<int>();
    int a = 0, b = 1;
    for (int i = 0; i < count; i++) {
        list.Add(a);
        (a, b) = (b, a + b);
    }
    return list;  // Entire list allocated
}
```

## Q25: What are `required` members and how do they enforce initialization?

**A:** Required members (C# 11) allow you to mark properties and fields that must be set during object initialization. When you declare a property with the `required` modifier, the compiler enforces that all callers must set that property using object initializers or constructor arguments. If a caller fails to set a required member, the compiler generates an error. This is a compile-time guarantee that the object is fully initialized before use.

Required members work by generating a special constructor (`.ctor`) that calls `RuntimeHelpers.EnsureSufficientExecutionStack` and sets an `IsExternalInit` flag. The compiler also generates an `IsRequired` attribute on the member, which enables tooling and reflection to identify required members. At the call site, the compiler checks that all required members are set in the initializer and generates an error if any are missing.

The practical value of required members is that they eliminate the "partial initialization" problem. Without required members, a class with many properties might be instantiated with some left as their default values, leading to subtle bugs. With `required`, the compiler forces the developer to explicitly set every critical property. Required members work particularly well with `init` properties, creating a pattern where the object is fully configured at construction time and completely immutable afterward. This pattern is common in configuration objects, builder patterns, and value objects.

```csharp
public class ConnectionConfig {
    public required string Host { get; init; }
    public required int Port { get; init; }
    public string Database { get; init; } = "default";
    public int Timeout { get; init; } = 30;
}

// All required members set — compiles
var config1 = new ConnectionConfig {
    Host = "localhost",
    Port = 5432
};

// Missing required member — compile error
// var config2 = new ConnectionConfig { Host = "localhost" };
// Error: 'Port' is required but not set

// Reflection can enumerate required members
var required = typeof(ConnectionConfig)
    .GetProperties()
    .Where(p => p.GetCustomAttribute<RequiredAttribute>() != null);
```

## Q26: What are expression-bodied members and when should you use them?

**A:** Expression-bodied members (C# 6+) provide a concise syntax for members that contain a single expression. Instead of writing a full method body with braces and return, you write `=> expression`. This syntax works for methods, properties, constructors, finalizers, and indexers. For methods and indexers, the syntax is `=> expression;`. For properties, it is `{ get; } => expression;` for read-only or `{ get; set; } => expression;` for read-write.

Expression-bodied members are best used for simple, single-expression implementations. They reduce boilerplate for trivial methods like getters, factory methods, and forwarding calls. They are not suitable for complex logic with multiple statements, error handling, or loops. The goal is readability — if an expression body makes the code clearer, use it; if it makes the code harder to understand, use a traditional body.

Expression-bodied constructors are particularly useful when the constructor body is a single call to another constructor: `public MyClass(int x) : this(x, 0) { }` can be written as `public MyClass(int x) => _value = x;`. Finalizers can also use expression bodies for simple cleanup. The feature integrates well with other C# features like null-conditional operators and string interpolation, creating very concise implementations.

```csharp
public class Point {
    public double X { get; }
    public double Y { get; }

    // Expression-bodied constructor
    public Point(double x, double y) => (X, Y) = (x, y);

    // Expression-bodied method
    public double DistanceTo(Point other) =>
        Math.Sqrt(Math.Pow(X - other.X, 2) + Math.Pow(Y - other.Y, 2));

    // Expression-bodied property
    public string Label => $"({X}, {Y})";

    // Expression-bodied ToString
    public override string ToString() => Label;
}

var p = new Point(3, 4);
Console.WriteLine(p.DistanceTo(new Point(0, 0)));  // 5
```

## Q27: What are the `in`, `out`, and `ref` parameter modifiers in C#?

**A:** `in` passes a parameter by reference but makes it read-only. The method cannot modify the value, and the caller sees no changes. `in` is useful for large structs to avoid copying overhead while preventing modification. The compiler may still pass small structs by value as an optimization. `out` passes a parameter by reference and requires the method to assign a value before returning. The caller must provide a variable, and the method must initialize it.

`ref` passes a parameter by reference and allows both reading and writing. The caller must initialize the variable before passing it, and the method can modify it. `ref` is used when a method needs to return multiple values without using tuples, or when it needs to modify the caller's variable directly. The `ref` keyword must be used at both the call site and the declaration.

These modifiers have performance implications. For large structs, passing by reference avoids copying. `in` is the safest for performance optimization because it guarantees immutability. `ref` and `out` have additional constraints: `ref` requires initialization, `out` requires assignment in the callee, and both have restrictions on which types can be used. C# 7.2 introduced `ref readonly` for returning references to internal data without allowing modification.

```csharp
// in: read-only reference
void PrintSize(in Point p) {
    Console.WriteLine(p.DistanceTo(Point.Zero));
    // p = new Point(0, 0);  // Error: in parameter is read-only
}

// out: must be assigned
void Deconstruct(Point p, out double x, out double y) {
    x = p.X;
    y = p.Y;
}

// ref: can be read and modified
void Swap(ref int a, ref int b) {
    (a, b) = (b, a);
}

int x = 1, y = 2;
Swap(ref x, ref y);
Console.WriteLine($"{x}, {y}");  // 2, 1
```

## Q28: What is pattern matching in C# and how has it evolved?

**A:** Pattern matching in C# (C# 7+) allows you to test expressions against patterns and extract values. The `is` and `switch` keywords support type patterns, constant patterns, property patterns, and relational patterns. Pattern matching replaces verbose type-check-and-cast sequences with concise, expressive syntax. It has evolved significantly across C# versions.

C# 7 introduced basic pattern matching with `is` and `switch`. C# 8 added property patterns (`is { Length: > 3 }`), tuple patterns (`is (1, 2)`), and positional patterns. C# 9 added relational patterns (`is > 0 and < 100`), logical patterns (`and`, `or`, `not`), and type patterns with `and`/`or`. C# 11 added list patterns (`[1, 2, ..]`) for matching sequences. Each version has made pattern matching more expressive and composable.

Pattern matching integrates with the type system and the discard pattern (`_`). It enables declarative code that describes what you are looking for rather than how to extract it. The compiler optimizes pattern matching to efficient IL code, often generating the same code as manual type checks. This makes pattern matching both readable and performant.

```csharp
// Type + relational patterns (C# 9+)
string Classify(object obj) => obj switch {
    int n and > 0 and <= 100 => "Small positive",
    int n and > 100 => "Large positive",
    int n and < 0 => "Negative",
    string { Length: > 0 } s => $"String: {s}",
    null => "Null",
    _ => "Unknown"
};

// Property pattern (C# 8+)
bool IsTeenager(Person p) =>
    p is { Age: >= 13 and <= 19 };

// List pattern (C# 11+)
bool IsPrefix(int[] arr) =>
    arr is [1, 2, ..];  // Starts with 1, 2
```

## Q29: How does C# handle nullable reference types and what are the implications?

**A:** Nullable reference types (C# 8+) add compile-time annotations that warn about potential null reference exceptions. When enabled with `<Nullable>enable</Nullable>` in the project file, reference types are treated as non-nullable by default. The compiler emits warnings when a nullable reference might be dereferenced without a null check. This is a compile-time feature — it does not add runtime checks but helps catch bugs during development.

The annotations use `?` syntax: `string?` is a nullable string, `string` is a non-nullable string. The compiler tracks nullability through assignments, method returns, and conditional logic. If a variable is assigned from a method that returns `string?`, the compiler warns if you use it without a null check. The `!` operator (null-forgiving) suppresses warnings when you are certain a value is not null.

Nullable reference types do not change runtime behavior — they are purely compile-time analysis. At runtime, a `string?` and a `string` are the same type. The value can still be null even if the type is annotated as non-nullable. This means you must still handle null cases at runtime, but the compiler helps you identify where null checks are needed. The feature is particularly valuable in large codebases where null-related bugs are common.

```csharp
#nullable enable

public class UserService {
    private readonly IUserRepository _repo;

    public UserService(IUserRepository repo) =>
        _repo = repo ?? throw new ArgumentNullException(nameof(repo));

    public string FindName(int id) {
        var user = _repo.FindById(id);
        return user?.Name ?? "Unknown";  // Handles null
    }
}

public record User(string Name);
public interface IUserRepository {
    User? FindById(int id);  // Returns nullable
}
```

## Q30: What are the differences between `Task`, `ValueTask`, and `Task<T>`?

**A:** `Task<T>` represents an asynchronous operation that returns a value. It is a reference type allocated on the heap. Every async method returning `Task<T>` allocates a `Task<T>` object, even if the operation completes synchronously. `Task` (without `T`) represents an asynchronous operation that returns no value. Both are backed by the thread pool's task scheduler and can be awaited multiple times.

`ValueTask<T>` is a struct that avoids heap allocation for synchronous completions. If the operation completes synchronously (which many I/O operations do after the first call), `ValueTask<T>` returns the result without allocating a `Task<T>` on the heap. This is significant for high-performance scenarios where millions of async calls are made. However, `ValueTask<T>` has restrictions: it can only be awaited once, should not be stored in fields, and cannot be used with `WhenAll` or `WhenAny`.

The trade-off is allocation avoidance versus flexibility. Use `Task<T>` when the result might be awaited multiple times, stored, or used with combinators. Use `ValueTask<T>` when the operation is likely to complete synchronously and the result will be consumed exactly once. Most methods should return `Task<T>` by default and switch to `ValueTask<T>` only after profiling demonstrates allocation pressure.

```csharp
// Task<T>: heap-allocated, awaitable multiple times
async Task<int> ComputeAsync() {
    await Task.Delay(100);
    return 42;
}

// ValueTask<T>: stack-allocated for sync completions
async ValueTask<int> ComputeOptimizedAsync() {
    return 42;  // No Task allocation
}

// Only await once — cannot store or reuse
async ValueTask<int> SingleAwaitAsync() {
    var vt = ComputeOptimizedAsync();
    return await vt;
}
```

## Q31: What is the difference between `IAsyncEnumerable<T>` and `IEnumerable<T>`?

**A:** `IEnumerable<T>` represents a synchronous collection that yields all elements at once (or lazily via `yield return`). When you iterate over it, all elements are produced synchronously on the calling thread. `IAsyncEnumerable<T>` (C# 8+) represents an asynchronous collection that yields elements one at a time, with each element potentially involving an asynchronous operation (like a database query or network call).

The key difference is that `IAsyncEnumerable<T>` supports `await foreach`, which asynchronously moves to the next element. This is essential for streaming data from I/O-bound sources where each element involves latency. For example, reading rows from a database, consuming messages from a queue, or processing pages from an API can all be modeled as `IAsyncEnumerable<T>`.

`IAsyncEnumerable<T>` integrates with LINQ through `System.Linq.Async`. You can use `Where`, `Select`, `Take`, and other operators asynchronously. The async LINQ operators process elements lazily and asynchronously, maintaining the streaming nature of the data. This is more memory-efficient than materializing an entire collection before processing, especially for large or unbounded data streams.

```csharp
// Synchronous enumeration
IEnumerable<int> SyncNumbers() {
    for (int i = 0; i < 10; i++) yield return i;
}

// Asynchronous enumeration
async IAsyncEnumerable<int> AsyncNumbers() {
    for (int i = 0; i < 10; i++) {
        await Task.Delay(100);
        yield return i;
    }
}

// Usage
await foreach (var num in AsyncNumbers()) {
    Console.WriteLine(num);
}
```

## Q32: How do C# events handle thread safety?

**A:** C# events are not inherently thread-safe. The `+=` and `-=` operators on events are not atomic, and the null-check-then-invoke pattern (`if (handler != null) handler(...)`) is a classic race condition. Between the null check and the invocation, another thread might unsubscribe all handlers, causing a `NullReferenceException`. This is the most common thread safety issue with events.

The standard fix is to capture the delegate in a local variable before the null check: `var temp = handler; if (temp != null) temp(...)`. This ensures that even if another thread unsubscribes, the local variable still holds the original reference. This pattern is thread-safe because the local variable captures a snapshot of the delegate's invocation list. The C# compiler applies this optimization automatically for events in C# 11+.

For scenarios where multiple threads can modify the subscriber list, you need to synchronize access. Using `lock` around `+=` and `-=` operations prevents concurrent modification. However, this can cause deadlocks if a handler tries to subscribe or unsubscribe from the same event. A more robust approach uses `Interlocked.CompareExchange` for lock-free thread safety, though this is complex and rarely needed in practice.

```csharp
public class ThreadSafeEvents {
    public event EventHandler Click;

    // Thread-safe invocation pattern
    protected virtual void OnClick() {
        var handler = Click;  // Capture delegate
        handler?.Invoke(this, EventArgs.Empty);
    }

    // Lock-based subscription for concurrent access
    private readonly object _lock = new();
    private EventHandler _click;

    public event EventHandler SafeClick {
        add { lock (_lock) { _click += value; } }
        remove { lock (_lock) { _click -= value; } }
    }
}
```

## Q33: What is the difference between `LINQ` query syntax and method syntax?

**A:** LINQ query syntax uses SQL-like keywords (`from`, `where`, `select`, `orderby`, `group by`) to write queries against collections. Method syntax uses extension methods (`Where`, `Select`, `OrderBy`, `GroupBy`) with lambda expressions. Both compile to the same IL code — the compiler translates query syntax into method calls. The choice is purely stylistic.

Query syntax is often preferred for complex queries involving multiple data sources, joins, or group by operations. It reads more naturally for SQL developers and can be clearer for set-based operations. Method syntax is preferred for simple transformations, method chaining, and when the query involves standardLINQ operators. Method syntax is also more flexible — it supports all operators, while query syntax only supports a subset.

In practice, most C# developers use method syntax as their default, switching to query syntax for complex joins or grouping. The key operators are: `Where`/`where` for filtering, `Select`/`select` for projection, `OrderBy`/`orderby` for sorting, `GroupBy`/`group by` for grouping, and `Join`/`join` for joining. Method syntax composes more naturally with other C# features like extension methods and fluent APIs.

```csharp
var numbers = Enumerable.Range(1, 20);

// Query syntax
var q1 = from n in numbers
         where n % 2 == 0
         select n * n;

// Method syntax (equivalent)
var q2 = numbers.Where(n => n % 2 == 0)
                .Select(n => n * n);

// Method syntax preferred for simple chains
var result = numbers
    .Where(n => n > 5)
    .OrderByDescending(n => n)
    .Take(5)
    .ToList();
```

## Q34: What are C# records and how do they enable value-based equality?

**A:** Records (C# 9) are reference types with built-in value-based equality. The compiler generates `Equals`, `GetHashCode`, and `ToString` methods that compare all public properties. Two records with the same data are equal even if they are different objects. This is fundamentally different from classes which default to reference equality.

The compiler generates an `EqualityContract` property and property-by-property comparison. For positional records (defined with constructor parameters), all positional parameters are compared. The generated `Equals` method uses the `EqualityComparer<T>.Default` for each property, supporting null values and nested types. `GetHashCode` uses `HashCode.Combine` to create a hash from all properties.

Records also support `with` expressions for creating modified copies, `deconstruct` for pattern matching, and `init` properties for immutability. The combination of value equality, immutability, and copy-and-modify semantics makes records ideal for data transfer objects, configuration objects, and functional programming patterns in C#.

```csharp
public record Coordinate(double Lat, double Lon);
public record Person(string Name, Coordinate Location);

var p1 = new Person("Alice", new Coordinate(40.7, -74.0));
var p2 = new Person("Alice", new Coordinate(40.7, -74.0));
var p3 = p1 with { Name = "Bob" };

Console.WriteLine(p1 == p2);  // True
Console.WriteLine(p1 == p3);  // False
Console.WriteLine(p3.Name);   // Bob
```

## Q35: What are the implications of `struct` equality in C#?

**A:** Struct equality in C# is value-based by default. When you compare two structs using `==` or `Equals`, all public fields and properties are compared. The default `Equals` method uses reflection to compare each field, which is slow but correct. For performance-critical code, you should override `Equals`, `GetHashCode`, and the `==`/`!=` operators.

The reflection-based default `Equals` has significant performance overhead. It uses `FieldInfo.GetValue` to read each field and compares them using `Object.Equals`. For structs with many fields or large nested types, this can be expensive. Overriding `Equals` with direct field comparison eliminates the reflection overhead. The `IEquatable<T>` interface provides a type-safe alternative that avoids boxing.

Another consideration is that struct equality compares all fields, including private ones. If a struct contains a mutable reference type field (like a `List<int>`), equality comparison depends on the reference equality of that field, not the contents. This can lead to unexpected behavior where two structs with identical data are not equal because they contain different list instances. Records solve this by implementing deep value equality for reference type properties.

```csharp
struct Point : IEquatable<Point> {
    public double X { get; }
    public double Y { get; }

    public Point(double x, double y) => (X, Y) = (x, y);

    public bool Equals(Point other) =>
        X == other.X && Y == other.Y;

    public override bool Equals(object obj) =>
        obj is Point p && Equals(p);

    public override int GetHashCode() =>
        HashCode.Combine(X, Y);

    public static bool operator ==(Point a, Point b) =>
        a.Equals(b);

    public static bool operator !=(Point a, Point b) =>
        !a.Equals(b);
}
```

## Q36: What is the difference between `throw` and `throw ex` in C#?

**A:** `throw` preserves the original stack trace, while `throw ex` resets the stack trace to the current location. When you catch an exception and rethrow it, using `throw` alone maintains the original stack trace, which is essential for debugging. Using `throw ex` loses the original stack trace information, making it harder to diagnose the root cause.

The recommendation is to always use `throw` (without the exception variable) when rethrowing exceptions. The only exception to this rule is when you need to wrap the original exception in a new exception type, in which case you should use `throw new NewExceptionType("message", ex)` to preserve the original as the inner exception.

C# 6 introduced the `when` keyword for exception filters, which provides another way to conditionally rethrow exceptions without losing stack trace. Exception filters allow you to specify conditions that must be true for the catch block to execute, without catching and rethrowing. This is preferred over catch-rethrow patterns in many cases.

```csharp
// Bad: loses stack trace
try {
    DoWork();
} catch (Exception ex) {
    throw ex;  // Stack trace reset to this line
}

// Good: preserves stack trace
try {
    DoWork();
} catch (Exception) {
    throw;  // Original stack trace preserved
}

// Best: exception filter (no catch needed)
try {
    DoWork();
} catch (Exception ex) when (ex is InvalidOperationException) {
    // Handle specific case
    throw;  // Stack trace preserved
}
```

## Q37: How does C# implement the visitor pattern using interfaces and pattern matching?

**A:** The visitor pattern in C# uses interfaces to define a visitor that can visit different element types. Each element type accepts a visitor through an `Accept` method. Modern C# (C# 7+) can implement the visitor pattern using pattern matching in switch expressions, eliminating the need for double dispatch in many cases.

The traditional visitor interface has a `Visit` method for each element type. The element's `Accept` method calls the appropriate `Visit` overload. This double dispatch ensures the correct visitor method is called based on both the visitor and element types. However, pattern matching simplifies this by testing the element type directly in the visitor's dispatch method.

The modern approach uses a `switch` expression with type patterns: `element switch { Circle c => VisitCircle(c), Rectangle r => VisitRectangle(r) }`. This is simpler, more maintainable, and avoids the interface explosion of traditional visitors. When the set of element types is stable, pattern matching is preferred. When element types change frequently, the traditional interface approach is better because new types require updating only the visitor interface.

```csharp
// Modern visitor with pattern matching
interface IShape { }

record Circle(double Radius) : IShape;
record Rectangle(double Width, double Height) : IShape;

double Area(IShape shape) => shape switch {
    Circle c => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    _ => throw new ArgumentException("Unknown shape")
};

// Traditional visitor interface
interface IShapeVisitor<T> {
    T Visit(Circle circle);
    T Visit(Rectangle rectangle);
}
```

## Q38: What are C# source generators and how do they relate to compile-time metaprogramming?

**A:** Source generators (C# 9+) are components that run during compilation and produce additional C# source files. They receive the compilation's syntax tree and semantic model, analyze it, and emit new source files that are compiled along with the rest of the code. This is C#'s approach to compile-time metaprogramming — generating code at build time rather than at runtime.

Source generators are useful for reducing boilerplate: implementing INotifyPropertyChanged, generating serializers, creating DI registrations, and producing JSON converters. They run as part of the Roslyn compiler pipeline, receiving the same information the compiler has about types, attributes, and code structure. This makes them more powerful than attributes-based code generation (like PostSharp) because they can analyze the full compilation.

The key difference from runtime reflection is performance. Source generators produce concrete code at build time, which the JIT compiler can optimize. Reflection-based approaches must inspect types at runtime, which is slower and prevents many optimizations. Source generators also make the generated code visible to developers, aiding debugging. The trade-off is increased build time and complexity in the generator itself.

```csharp
// Source generator produces this attribute
[AttributeUsage(AttributeTargets.Class)]
public class GenerateToStringAttribute : Attribute { }

// Generator reads this:
[GenerateToString]
public partial class MyClass {
    public string Name { get; set; }
    public int Value { get; set; }
}

// Generator produces:
partial class MyClass {
    public override string ToString() =>
        $"MyClass {{ Name = {Name}, Value = {Value} }}";
}
```

## Q39: How do C# attributes interact with reflection at runtime?

**A:** Attributes are metadata attached to types, members, or parameters using square bracket syntax. At runtime, reflection can inspect attributes using `GetCustomAttribute`, `GetCustomAttributes`, or `IsDefined` methods. Attributes store data as constructor arguments or named properties, and this data is accessible through the `Attribute` object returned by reflection.

The most common use of attributes with reflection is in frameworks. ASP.NET Core uses `[Route]` and `[HttpGet]` to define endpoints. DI containers use `[Inject]` to resolve dependencies. Serialization uses `[JsonPropertyName]` for naming. ORM frameworks use `[Table]` and `[Column]` for mapping. In all cases, the framework uses reflection to discover attributes and configure behavior accordingly.

Attributes have performance implications. Reflection is significantly slower than direct member access. For frequently accessed attributes, caching the reflection results is essential. Source generators (C# 9+) can generate the attribute-based code at compile time, eliminating runtime reflection overhead. The `[Flags]` attribute on enums and `[Serializable]` on classes are examples of attributes that affect compile-time behavior rather than runtime reflection.

```csharp
[AttributeUsage(AttributeTargets.Property)]
public class RequiredAttribute : Attribute { }

public class User {
    [Required]
    public string Name { get; set; }

    [Required]
    public string Email { get; set; }
}

// Runtime reflection to check attributes
var requiredProps = typeof(User)
    .GetProperties()
    .Where(p => p.GetCustomAttribute<RequiredAttribute>() != null)
    .Select(p => p.Name);

foreach (var name in requiredProps)
    Console.WriteLine($"Required: {name}");
```

## Q40: What is the difference between `IComparable<T>` and `IComparer<T>`?

**A:** `IComparable<T>` is implemented by a type that defines its natural ordering. The type itself knows how to compare instances of itself. When you call `Array.Sort()` or `OrderBy()`, the sort algorithm calls `CompareTo` on the elements. `IComparable<T>` is implemented on the type being compared, making it the "default" comparison.

`IComparer<T>` is a separate object that defines how to compare two instances of a type. It is used when you need a custom comparison that the type itself does not provide, or when you want to use a different comparison than the type's natural ordering. `IComparer<T>` is passed to sorting algorithms as a parameter, and it receives two objects to compare.

The practical difference is that `IComparable<T>` is for types that have a single natural ordering (like numbers or dates), while `IComparer<T>` is for providing multiple orderings or custom comparisons. You can have many `IComparer<T>` implementations for a single type (sort by name, sort by age, sort descending), but a type can only implement `IComparable<T>` once. The `Comparer<T>.Default` factory creates an `IComparer<T>` that uses the type's `IComparable<T>` implementation.

```csharp
// IComparable: type knows how to compare itself
public class Student : IComparable<Student> {
    public string Name { get; set; }
    public double GPA { get; set; }

    public int CompareTo(Student other) =>
        GPA.CompareTo(other.GPA);
}

// IComparer: external comparison strategy
public class NameComparer : IComparer<Student> {
    public int Compare(Student x, Student y) =>
        string.Compare(x.Name, y.Name, StringComparison.Ordinal);
}

var students = new List<Student> { /* ... */ };
students.Sort();              // Uses IComparable
students.Sort(new NameComparer());  // Uses IComparer
```

## Q41: How does C# implement the Strategy pattern using delegates?

**A:** The Strategy pattern encapsulates interchangeable algorithms behind a common interface. In C#, delegates serve as the strategy interface, eliminating the need for a formal interface definition. A method that accepts a delegate parameter can use any callable that matches the delegate signature as a strategy. Lambda expressions make strategy creation concise and inline.

The pattern works by passing a delegate to a method that performs the core algorithm. The algorithm calls the delegate at appropriate points, allowing the caller to inject different behaviors. This is used extensively in LINQ (`Func<T, bool>` predicates for filtering), sorting (`Comparison<T>` for custom order), and functional programming patterns.

The advantage of using delegates over interfaces for the Strategy pattern is brevity. You do not need to define a separate interface and implementation class for each strategy — you can pass a lambda expression directly. This makes the code more concise and easier to read. However, if the strategy is complex, has multiple methods, or needs state, a formal interface with a class implementation is more appropriate.

```csharp
// Delegate-based strategy
public static List<T> Filter<T>(this List<T> items, Func<T, bool> predicate) {
    var result = new List<T>();
    foreach (var item in items)
        if (predicate(item))
            result.Add(item);
    return result;
}

// Different strategies as lambdas
var numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

var evens = numbers.Filter(n => n % 2 == 0);
var large = numbers.Filter(n => n > 5);
var between = numbers.Filter(n => n >= 3 && n <= 7);
```

## Q42: What is the purpose of the `CallerMemberName`, `CallerFilePath`, and `CallerLineNumber` attributes?

**A:** These attributes (System.Runtime.CompilerServices) allow methods to capture information about the caller at compile time. `[CallerMemberName]` captures the name of the calling method or property. `[CallerFilePath]` captures the full path of the source file. `[CallerLineNumber]` captures the line number in the source file. The compiler fills in these values at compile time, not runtime.

The primary use case for `[CallerMemberName]` is implementing `INotifyPropertyChanged`. Instead of hardcoding property names as strings, you use `[CallerMemberName]` to automatically capture the property name. This eliminates string-based bugs when properties are renamed. The compiler inserts the member name as a string literal at the call site.

These attributes have no runtime cost — the values are embedded as string literals and integer constants by the compiler. They are invaluable for debugging, logging, and implementing patterns that need to know where they were called from. The `CallerArgumentExpression` attribute (C# 10) extends this to capture the text of argument expressions.

```csharp
public class ObservableObject : INotifyPropertyChanged {
    public event PropertyChangedEventHandler PropertyChanged;

    protected void OnPropertyChanged(
        [CallerMemberName] string name = null) {
        PropertyChanged?.Invoke(this,
            new PropertyChangedEventArgs(name));
    }

    private string _name;
    public string Name {
        get => _name;
        set {
            _name = value;
            OnPropertyChanged();  // Captures "Name" automatically
        }
    }
}

// CallerFilePath and CallerLineNumber for logging
void Log(string message,
    [CallerFilePath] string file = "",
    [CallerLineNumber] int line = 0) {
    Console.WriteLine($"[{Path.GetFileName(file)}:{line}] {message}");
}
```

## Q43: How does C# handle covariance in arrays and why is it considered unsafe?

**A:** Arrays in C# support covariance — you can assign an array of a derived type to a variable of an array of a base type. For example, `string[] strings = new string[5]; object[] objects = strings;` compiles without error. This is because strings are objects, so logically an array of strings should be usable as an array of objects.

However, array covariance is type-unsafe. The assignment `objects[0] = 42` compiles (because 42 is an object) but throws an `ArrayTypeMismatchException` at runtime because the underlying array is a string array and cannot hold an integer. This is a compile-time type safety violation that only manifests at runtime. The CLR must perform a type check on every store to a covariant array, adding overhead.

Generics provide type-safe alternatives. `IEnumerable<T>` is covariant (marked with `out T`), allowing `IEnumerable<string>` to be assigned to `IEnumerable<object>` safely. `List<T>` is invariant, preventing the unsafe array assignment pattern. The recommendation is to prefer generic collections over arrays for type safety, using arrays only when the element type is known to be invariant or when performance requirements demand it.

```csharp
// Array covariance — unsafe
string[] strings = { "a", "b" };
object[] objects = strings;  // Compiles!
// objects[0] = 42;          // Runtime exception!

// Generic covariance — safe
IEnumerable<string> stringEnum = strings;
IEnumerable<object> objectEnum = stringEnum;  // Safe: read-only

// Generic invariance — enforced
List<string> stringList = new List<string>();
// List<object> objectList = stringList;  // Compile error!
```

## Q44: What is the difference between `String.Concat`, `String.Format`, and string interpolation?

**A:** `String.Concat` concatenates strings directly. It is the simplest form, joining two or more strings end-to-end. It does not perform any formatting — it just concatenates. For multiple concatenations, `String.Concat` with an array or `StringBuilder` is more efficient than repeated `+` operators because it avoids creating intermediate string objects.

`String.Format` uses format placeholders (`{0}`, `{1}`, etc.) to insert values into a string template. It performs type conversion using `IFormattable` or `ToString`, and supports format specifiers like `{0:N2}` for numbers. It is useful when the format string is dynamic (loaded from resources) or when complex formatting is needed.

String interpolation (`$"..."`) is syntactic sugar for `String.Format`. The compiler translates `$"Hello {name}"` into `String.Format("Hello {0}", name)`. It provides compile-time checking of format expressions and IntelliSense support. In most cases, string interpolation is preferred for readability. However, when the format string comes from a resource file or is truly dynamic, `String.Format` is necessary.

```csharp
string name = "Alice";
int age = 30;

// Concat: no formatting
string s1 = String.Concat("Hello, ", name);

// Format: placeholder-based
string s2 = String.Format("Name: {0}, Age: {1}", name, age);

// Interpolation: syntactic sugar for Format
string s3 = $"Name: {name}, Age: {age}";

// Interpolation with format specifiers
decimal price = 123.456m;
string s4 = $"Price: {price:C2}";  // Price: $123.46
```

## Q45: What are C# indices and ranges and how do they simplify collection access?

**A:** Indices and ranges (C# 8+) provide a concise syntax for accessing elements and subsequences of collections. An index uses `^` syntax to count from the end: `arr[^1]` is the last element, `arr[^2]` is the second-to-last. A range uses `..` syntax: `arr[1..4]` creates a slice from index 1 to 4 (exclusive). The `Index` and `Range` types are structs that represent these concepts.

The `Index` type wraps an integer and supports both forward (from start) and backward (from end) indexing. The `Range` type represents a contiguous range of indices and can be used with array slices. Any type that defines a `this[Index]` or `this[Range]` indexer supports this syntax. Arrays, `Span<T>`, and `Memory<T>` support it natively.

The practical benefit is readability. `arr[^1]` is clearer than `arr[arr.Length - 1]`. `arr[1..4]` is clearer than `arr.Skip(1).Take(3).ToArray()`. The performance is also better for slices because `Span<T>` slices are zero-allocation views into the underlying array. This is particularly valuable for string manipulation, array processing, and memory-efficient data handling.

```csharp
int[] arr = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };

// Index from end
Console.WriteLine(arr[^1]);   // 9 (last element)
Console.WriteLine(arr[^3]);   // 7 (third from end)

// Range
Console.WriteLine(string.Join(",", arr[2..5]));  // 2,3,4
Console.WriteLine(string.Join(",", arr[..4]));   // 0,1,2,3
Console.WriteLine(string.Join(",", arr[4..]));   // 4,5,6,7,8,9

// Works with strings
string text = "Hello, World!";
Console.WriteLine(text[^6..]);  // "World!"
```

## Q46: How does C# handle `dynamic` dispatch at runtime versus compile-time polymorphism?

**A:** Compile-time polymorphism uses interfaces, abstract classes, and virtual methods. The compiler resolves method calls at compile time based on the declared type, and the CLR uses virtual dispatch tables at runtime for virtual and abstract methods. This provides type safety and performance — the JIT compiler can inline small virtual methods and devirtualize calls when the type is known.

`dynamic` (C# 4+) bypasses compile-time resolution entirely. All operations on `dynamic` variables are resolved at runtime using the Dynamic Language Runtime (DLR). The DLR performs member lookup, overload resolution, and type coercion at runtime. This enables interoperability with dynamic languages, COM objects, and scenarios where types are not known at compile time.

The performance cost of `dynamic` is significant. Every operation involves DLR call site caching, type checking, and potential reflection. After the first call, the DLR caches the resolution at the call site, making subsequent calls faster but still slower than static dispatch. The JIT compiler cannot inline or optimize `dynamic` calls. Use `dynamic` sparingly and prefer static typing for performance-critical code.

```csharp
// Static dispatch — compile-time resolution
IEnumerable<int> numbers = Enumerable.Range(1, 5);
var result = numbers.Where(n => n > 3);  // Resolved at compile time

// Dynamic dispatch — runtime resolution
dynamicdyn = GetSomeObject();
var result2 = dyn.SomeMethod();  // Resolved at runtime

// Performance comparison
static void StaticCall(IEnumerable<int> nums) =>
    nums.Where(n => n > 3).ToList();

static void DynamicCall(object nums) {
    dynamic d = nums;
    var r = d.Where((Func<int, bool>)(n => n > 3)).ToList();
}
```

## Q47: What are C# extension methods and how do they enable fluent APIs?

**A:** Extension methods are static methods that appear to be instance methods on a type. They are defined in static classes with the `this` keyword on the first parameter. Extension methods enable fluent APIs by allowing method chaining on any type, including sealed classes and types you do not own. LINQ's entire API is built on extension methods on `IEnumerable<T>`.

A fluent API chains method calls to create a readable, pipeline-like syntax. Each extension method returns an object (often the same type or a builder) that allows the next method to be called. This creates a domain-specific language for building complex operations. For example, `builder.WithHost("localhost").OnPort(8080).WithSSL()` reads like natural language.

Extension methods are resolved at compile time based on the declared type of the variable, not the runtime type. They cannot override existing instance methods — instance methods always take precedence. They also cannot access private members of the extended type. These limitations make extension methods safe and predictable — they add convenience without modifying the type itself.

```csharp
public static class FluentExtensions {
    public static T Tee<T>(this T obj, Action<T> action) {
        action(obj);
        return obj;
    }

    public static string EnsureNotEmpty(this string s, string fallback) =>
        string.IsNullOrEmpty(s) ? fallback : s;
}

// Fluent builder pattern
var config = new ServerConfig()
    .WithHost("localhost")
    .OnPort(8080)
    .WithSSL()
    .Tee(c => Console.WriteLine(c));  // Side effect, returns c
```

## Q48: How do C# delegates support contravariance and covariance?

**A:** Delegates in C# support contravariance in parameter types (marked with `in`) and covariance in return types (marked with `out`). This means a delegate that accepts a base type parameter can be assigned to a delegate that accepts a derived type parameter (contravariance), and a delegate that returns a derived type can be assigned to a delegate that returns a base type (covariance).

The built-in delegate types `Action<in T>` and `Func<in T, out TResult>` are declared with variance annotations. This means `Action<Animal>` can be assigned to `Action<Dog>` (contravariance), and `Func<Cat, Animal>` can be assigned to `Func<Cat, object>` (covariance). These variance annotations make delegate types composable and flexible.

Custom delegate types can also declare variance. The syntax is `delegate TResult MyFunc<in T, out TResult>(T arg)`. The `in` and `out` annotations are checked at compile time — the type parameter can only appear in input or output positions respectively. This ensures type safety while enabling flexible delegate assignment.

```csharp
// Contravariance in Action<in T>
Action<Animal> feedAnimal = a => Console.WriteLine("Feeding");
Action<Dog> feedDog = feedAnimal;  // OK: contravariant
feedDog(new Dog());

// Covariance in Func<in T, out TResult>
Func<Dog, Animal> dogToAnimal = d => d;
Func<Dog, object> dogToObject = dogToAnimal;  // OK: covariant

// Custom delegate with variance
delegate T Producer<out T>();
delegate void Consumer<in T>(T item);

Producer<Dog> dogProducer = () => new Dog();
Producer<Animal> animalProducer = dogProducer;  // OK
```

## Q49: What is the difference between `Assembly`, `Module`, and `Type` in .NET reflection?

**A:** An `Assembly` is a compiled unit of code — typically a DLL or EXE file. It contains one or more modules, type definitions, resources, and metadata. In modern .NET (single-file publishing), an assembly usually contains one module. Assembly-level attributes like `[AssemblyVersion]` and `[InternalsVisibleTo]` configure assembly-wide behavior. Reflection can load assemblies using `Assembly.Load` and inspect their contents.

A `Module` represents a module within an assembly. In modern .NET, each assembly typically has one module. Modules contain type definitions, resources, and entry points. Module-level inspection is less common than assembly-level, but it is useful for scenarios like multi-module assemblies or for inspecting resources within a module.

A `Type` represents a class, interface, struct, enum, or delegate within a module. Type reflection is the most common form of reflection. You can inspect type members (methods, properties, fields, events), attributes, interfaces, base types, and generic parameters. `Type` objects are the entry point for most reflection operations, and they are obtained from assemblies and modules.

```csharp
// Assembly reflection
var assembly = typeof(Program).Assembly;
Console.WriteLine(assembly.FullName);

// Module reflection
foreach (var module in assembly.GetModules())
    Console.WriteLine(module.Name);

// Type reflection
var type = typeof(List<int>);
Console.WriteLine(type.IsGenericType);  // True
Console.WriteLine(type.GetGenericArguments()[0]);  // System.Int32
foreach (var method in type.GetMethods().Take(5))
    Console.WriteLine(method.Name);
```

## Q50: What are the best practices for using delegates and events in C#?

**A:** Best practices for delegates include: use `Func<T>` and `Action<T>` instead of declaring custom delegate types for most scenarios, prefer lambda expressions for inline implementations, and avoid allocating delegates in tight loops (cache them when possible). For events, always use the standard `EventHandler` or `EventHandler<TEventArgs>` pattern, always use the null-conditional operator for invocation, and provide a way to unsubscribe to prevent memory leaks.

Memory management with delegates is critical. Event subscriptions create strong references to the subscriber. If a subscriber does not unsubscribe, it will not be garbage collected as long as the event source lives. Use weak event patterns for long-lived event sources and short-lived subscribers. The `WeakReference` class can help track subscribers without preventing garbage collection.

For performance, avoid delegate allocation in hot paths. Cache delegate instances for frequently used callbacks. Use `static` lambdas when the lambda does not capture any variables, as the compiler can cache a single delegate instance. For high-performance scenarios, consider using `delegate*` (function pointers, C# 9+) which have zero allocation overhead but lack the safety features of delegates.

```csharp
// Cache delegates for performance
private static readonly Func<int, bool> IsPositive = n => n > 0;

// Standard event pattern
public event EventHandler<ValueChangedEventArgs> ValueChanged;

// Null-safe invocation
protected virtual void OnValueChanged(int newValue) {
    ValueChanged?.Invoke(this,
        new ValueChangedEventArgs(newValue));
}

// Unsubscribe to prevent memory leaks
void Setup() {
    source.Event += Handler;
    // Don't forget to unsubscribe
    // source.Event -= Handler;
}

// Static lambda for no-capture optimization
var result = numbers.Where(static n => n > 0).ToList();
```

## Q51: What is explicit interface implementation and when is it required?

**A:** Explicit interface implementation syntaxually binds a member to a specific interface, written as `void IFoo.Bar()`. It becomes visible only when the object is accessed through that interface reference. It also makes the member implicitly private-ish — it disappears from the concrete type's public surface and from IntelliSense, so callers holding the concrete type cannot accidentally invoke it.

The primary trigger is ambiguity: two interfaces declaring members with identical signatures. Implementing both implicitly is impossible — one method would satisfy the same signature twice and lose its identity. Explicit implementation disambiguates, so `((IFile)x).Save()` and `((IXmlSerializable)x).Save()` behave differently. A second use is hiding members that are only meaningful through the interface lens, such as `IEnumerable.GetEnumerator()`, which deliberately shadows the generic `GetEnumerator()` and is not meant to be called directly.

Be careful with accessibility: explicit members cannot be accessed from derived classes without an interface cast, and because they are neither virtual nor part of the normal class surface, `abstract`/`virtual` modifiers do not apply the same way. Repeated casting is a performance and readability cost, so prefer implicit implementation when there is no real conflict.

```csharp
interface IFile { void Save(); }
interface IXmlSerializable { void Save(); }

class Document : IFile, IXmlSerializable
{
    // Ambiguity resolved: each Save() is distinctly bound
    void IFile.Save()   { Console.WriteLine("saving file"); }
    void IXmlSerializable.Save() { Console.WriteLine("saving as XML"); }

    public void Save()  { /* common save logic */ }
}

var d = new Document();
((IFile)d).Save();   // disambiguated
```

## Q52: What is the difference between `new` method hiding and `override`, and why is hiding considered dangerous?

**A:** `override` rewrites the slot in the virtual table: the derived member participates in virtual dispatch, so any reference to the base type invokes the most-derived implementation. `new` does not touch the vtable slot at all — it defines a completely separate member that shadows the base one, so which implementation runs depends entirely on the static type of the reference you call through.

The danger is that `new` splits one logical operation into two behaviors with no warning at the call site. A `Derived` stored in a `Base` variable silently runs the base method, while the same object stored as `Derived` runs the derived method. Code becomes sensitive to how the object is aliased. That divergence is exactly the kind of confusion that makes a model fragile, which is why the compiler emits CS0108 warning asking you to be explicit about intent.

`new` is occasionally legitimate — timing out a non-virtual member from a third-party base when you cannot modify it, or hiding a non-virtual helper from `object` — but treating it as a versioning tool masks design issues. If the base member was meant to be extensible it should have been `virtual`. Prefer refactoring or composition over hiding.

```csharp
class Base { public void Run() => Console.WriteLine("base"); }
class Derived : Base { public new void Run() => Console.WriteLine("derived"); }

Base b = new Derived();
Derived d = new Derived();
b.Run();  // "base"
d.Run();  // "derived"
```

## Q53: How do generic constraints such as `where T : class`, `struct`, `new()`, and `where T : IInterface` shape generic programming in C#?

**A:** Constraints inform the compiler which operations are legal on type parameters. `where T : class` unlocks `null` assignments, `as` casts, and reference-style comparisons; `where T : struct` guarantees a non-nullable value, enables boxing-free use in nested contexts like `Nullable<T>`, and allows `T` usage where a non-nullable value is required. `where T : new()` guarantees a public parameterless constructor so generic code can allocate instances. Interface constraints are the workhorse: they make members of the interface available on `T`, letting services, repositories, or comparers be built against a smallest sufficient surface instead of `object`.

Constraints act as a hybrid of signatures and contracts. Because constraints are part of the method signature, overloading can select between specialized algorithms based on constraint membership. They also give the JIT more information: constrained calls on struct type parameters can be emitted without boxing — the runtime consults the constraint and dispatches directly, so generic `struct` code avoids the allocation cost implicit in unconstrained calls.

Unconstrained `T` is more limited than novices expect: only `object` members and comparisons against `default(T)` are permitted. Each added constraint narrows applicability, so the design tension is finding the smallest constraint that opens the operations you need. Newer constraints like `where T : notnull`, `unmanaged`, and `where T : IAdditionOperators<T,T,T>` (C# 11 static abstracts) extend this algebra well beyond reference and value roots.

```csharp
public static T CreateDefault<T>() where T : struct, new()
    => new T();

public static void SortInPlace<T>(IList<T> items) where T : IComparable<T>
{
    for (var i = 1; i < items.Count; i++)
    {
        var item = items[i];
        var j = i - 1;
        // IComparable<T> members are now legal on T
        while (j >= 0 && items[j].CompareTo(item) > 0) { items[j + 1] = items[j]; j--; }
        items[j + 1] = item;
    }
}
```

## Q54: What is the `IDisposable` and `IAsyncDisposable` lifecycle contract, and how do `using` declarations integrate with the .NET object model?

**A:** .NET removes objects nondeterministically through GC, but some resources — handles, sockets, transactions, file locks — cannot wait for a finalizer that may never run promptly. `IDisposable` is the deterministic cleanup contract: the owner of a resource is responsible for releasing it the moment it is no longer needed. `using` compiles into a try/finally that guarantees `Dispose` even when an exception unwinds the stack. The interface is deliberately tiny: one method, signifying "this type holds a resource that must be released".

`IAsyncDisposable` extends the contract to cleanup that intrinsically needs `async` — flushing a stream, completing a flush-dependent transaction, closing a socket gracefully. It is a separate interface because an async `Dispose` would have to block in saving-the-world scenarios, and because IDisposable implementations are expected to be cheap and idempotent. `await using` mirrors `using` with the same guaranteed-invocation semantics. Types commonly implement both: fast-path sync disposal and a slower async fallback when one exists.

The deeper design expectation is idempotence and tolerance: `Dispose` should be safe to call multiple times, no further use is valid after disposal, and sealable classes should not expose finalizers. The `Dispose(bool)` pattern (virtual `Dispose(bool disposing)`, protected, prevents double finalization) is a guideline for inheritance, but with SafeHandles it is rarely needed on leaf types. Using declarations solve the scoping problem on IO-heavy code paths: the object is finalized conformably at scope exit, so state is released deterministically regardless of where control flow exits.

```csharp
await using (var stream = new FileStream(path, FileMode.Open))
{
    // flush + close guaranteed via async dispose
    await stream.WriteAsync(buffer, 0, buffer.Length);
}

public sealed class DbConnection : IDisposable, IAsyncDisposable
{
    private bool _disposed;
    public void Dispose() => ReleaseSync();
    public ValueTask DisposeAsync() { ReleaseSync(); return ValueTask.CompletedTask; }
    private void ReleaseSync() { if (_disposed) return; _disposed = true; /* free handle */ }
}
```

## Q55: Why are operator overloads in C# static and non-virtual, and how do they interact with polymorphism and generic math?

**A:** Operators are syntactic sugar over static methods: `a + b` desugars to `Op_Addition(a, b)` resolved at compile time from the static types of the operands. That is why they cannot be virtual — virtual dispatch depends on the runtime receiver type, but `+` represents a compile-time computation over two operands, neither of which owns the operation. Consequently `a + b` and `b + a` are resolved symmetrically, which preserves commutativity assumptions and keeps the language free of operator tables on each type.

The static resolution causes subtle asymmetry in polymorphism. `var x = baseRef + one` picks the `operator +` declared on the operand's static types, not the runtime type, so a `Derived` stored in a `Base` reference will use `Base`'s operator unless the operator itself performs polymorphic dispatch internally. This is a frequent source of "why didn't my derived operator get called" confusion. It also means a `List<Shape>` cannot be added with `+` unless a real operator exists for `List<Shape>`, and interfaces historically could not declare operators at all.

That last limitation is why C# 11 introduced static abstract interface members: an interface can now declare `static abstract Shape operator +(Shape, Shape)` and generic math (`INumber<T>`, `IAdditionOperators<T, T, T>`) exploits it. A generic method constrained to `IAdditionOperators<T, T, T>` can write `left + right` on `T` and the runtime resolves the operator through the static constraint. This recovers a virtual-like extensibility story for value types and numerics where the old instance-based model would box and bloat.

```csharp
// C# 11 generic math — operators defined through static interface members
public static T Sum<T>(IEnumerable<T> values) where T : IAdditionOperators<T, T, T> 
{
    var acc = default(T)!;
    foreach (var v in values) acc = acc + v;
    return acc;
}

// Operator on a custom numeric type
public readonly record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
}
```

## Q56: What are `IObservable<T>` and `IObserver<T>` and how do they differ from the event keyword?

**A:** `IObservable<T>`/`IObserver<T>` model a push-based stream: the producer implements `IObservable<T>` with `Subscribe(IObserver<T>)` returning an `IDisposable` used to unsubscribe, and the consumer gets explicit callback channels for data (`OnNext`), terminal error (`OnError`), and termination (`OnCompleted`). The flow of control is inverted versus ordinary method calls, forming the foundation of the Reactive Extensions (Rx). Because `Subscribe` returns a disposable handle, tearing down a subscription is first-class rather than a fragile `-=` pairing.

The `event` keyword is a lighter mechanism built directly on delegates. Events intentionally restrict the outer world to `+=` and `-=`; only the declaring type may raise them. There is no built-in vocabulary for completion or error — a subscriber cannot be told "the stream is over" through the event channel itself. Events also hold strong references to all subscribers, which is why static events are notorious memory-leak sources, whereas the `IDisposable` subscription from `IObservable` makes termination explicit and testable, and operator pipelines compose into higher-order flow.

Functionally, events are usually sufficient for simple "something changed" notifications, which is why most .NET libraries still expose events. `IObservable` pays off when the stream has a lifecycle (finite sequence, error channel), when you need composable operators — `Select`, `Where`, `Buffer`, `Retry` — or when the same data must be projected many ways. A pragmatic blend is exposing an event and layering an Rx bridge over it via `Observable.FromEvent`, so consumers can subscribe with LINQ-like semantics without rewriting the producer.

```csharp
class StockTicker : IObservable<decimal>
{
    private readonly List<IObserver<decimal>> _obs = new();
    public IDisposable Subscribe(IObserver<decimal> observer)
    {
        _obs.Add(observer);
        return new Subscription(_obs, observer);
    }
    public void Tick(decimal price)
    {
        foreach (var o in _obs) o.OnNext(price);
    }
}

class PricePrinter : IObserver<decimal>
{
    public void OnNext(decimal v) => Console.WriteLine(v);
    public void OnError(Exception e) => Console.WriteLine(e.Message);
    public void OnCompleted() => Console.WriteLine("done");
}

using var sub = new StockTicker().Subscribe(new PricePrinter());
```

## Q57: What is the Interface Segregation Principle and how does the C# type system enshrine it?

**A:** Interface Segregation says no client should be forced to depend on members it does not use. A fat interface — one that promises persistence, enumeration, change notification, and auditing in a single type — punishes each consumer with a contract larger than its need. Consumers become coupled to the entire surface, so every unimplemented method tends to surface as `NotImplementedException`, and every change ripples to unrelated call sites. Segregating means expressing each capability as its own minimal interface and letting combined consumers depend on the combination.

C# provides structural support for this: an interface is a pure contract with no implementation baggage (pre-8), so decomposing it into focused pieces is cheap; extension methods allow capabilities to be layered onto a small core surface rather than folded into it; and explicit interface implementation lets one type satisfy two roles without name collisions. The language also encourages the corollary — "smallest interface that does the job" — through generic constraints: pass `IReadOnlyList<T>` to a method that only iterates, not `IList<T>`, mirroring Go's consumer-relevant minimalism.

Beware that segregating interfaces does not automatically mean many small types on the public API. The principle is about the *dependency direction*: each consumer declares the slice it needs. .NET itself is the canonical teacher — `IEnumerable<T>` is one method, `IDisposable` one method, `IComparer<T>` one method. When you see a class implementing ten interfaces, that is usually health; when you see one interface with ten methods, that is usually a leak waiting to be compartmentalized.

```csharp
// Anti-pattern: one interface To Rule Them All
interface IStorage
{
    void Save(byte[] data);
    byte[] Load(int id);
    void Delete(int id);
    IReadOnlyList<int> ListAll();
    event EventHandler StorageChanged;
}

// Segregated: each consumer depends only on what it needs
interface IWriter { void Save(byte[] data); }
interface IReaderById { byte[] Load(int id); }
interface IReaderAll { IReadOnlyList<int> ListAll(); }
interface IDeleter { void Delete(int id); }
```

## Q58: What are expression trees and how do they differ from compiled delegates?

**A:** A delegate is an opaque reference to compiled code: you can call it, but you cannot inspect or transform it. An expression tree is *data describing code* — a graph of `Expression` nodes represent the operation, operands, literals, and parameters. `Expression<Func<int,int>>` does not contain a direct invocation; it is a parsed, immutable structure you can traverse, rewrite, serialize, or translate. The compiler builds this graph from a lambda when the target type is an expression tree type.

The crucial distinction appears in translation: `Func<Person,bool> p = x => x.Age > 18;` compiles to IL. `Expression<Func<Person,bool>> e = x => x.Age > 18;` compiles to node construction — you can inspect the `PropertyAccess` node for `Age` and the `GreaterThan` node. That inspection is exactly what lets `IQueryable` providers such as LINQ-to-SQL translate a C# predicate to SQL: the provider walks the tree and emits `WHERE Age > 18` instead of executing C#. Delegates give you behavior; trees give you meaning, so reflection-based frameworks, security analyzers, and translators all consume trees.

The operational difference matters: expression trees cannot contain statements (before C# 6, and even now only limited blocks), cannot express everything a delegate can, and constructing them is significantly slower than compiling a method pointer. They also cannot be built, in general, without `Expression` factory calls when generated dynamically. Conversely `e.Compile()` turns a tree into a delegate — useful when you have rewritten a tree and then want to execute it. The rule of thumb: use a delegate when you want *to run* logic; use an expression tree when something else must *read and rewrite* the logic first.

```csharp
Func<int, int> d = x => x * 2;          // compiled IL, callable directly
Expression<Func<int, int>> e = x => x * 2;

// e is data — the shape is queryable
Console.WriteLine(e.Body.NodeType);          // Multiply
Console.WriteLine(((BinaryExpression)e.Body).Left); // x

// translate "x * 2" into an equivalent but rewritten tree
var rewritten = Expression.Lambda<Func<int, int>>(
    Expression.Add(e.Body, Expression.Constant(1)), e.Parameters);
var fn = rewritten.Compile();               // now a real delegate
Console.WriteLine(fn(3));                   // 7
```

## Q59: How does `MulticastDelegate` chaining work, and what are its return-value and exception semantics?

**A:** A delegate instance actually holds an *invocation list*: a linked chain of one or more method/target pairs. Choosing `+` or `+=` to combine delegates flattens them into a single chain; `-` or `-=` removes the *last matching* occurrence. Because `EventHandler`-style delegating is the norm, most developers think of a delegate as one callable, but with multiple targets every invocation walks the whole chain in order, and that changes the meaning of a return value.

The two behavior quirks that bite seniors are return values and exceptions. For a delegate returning a value — say `Func<int> f = a + b + c; call f()` — only the last delegate's return value is delivered; the others are silently discarded. That is why `event`-based APIs overwhelmingly use void-returning handlers. Exceptions are worse: if one handler in the chain throws, the chain stops immediately; later handlers never run. There is no built-in "invoke all and collect exceptions" semantics. If you need every handler to execute and to aggregate failures, you must pull the chain apart with `GetInvocationList()` and invoke each delegate yourself in a try/catch.

Understanding the chain also clarifies `+=`/`-=` asymmetry used in events: unsubscribing a specific handler that was registered as a lambda requires caching the very same delegate instance, since equality comparison looks at the target and method, not the lambda's source text. Finally, the combined chain is itself immutable after construction — `+=` allocates a new multicast delegate — which is why `Interlocked.CompareExchange` is the standard tool for safely updating concurrently-raised events.

```csharp
Action a = () => Console.WriteLine("A");
Action b = () => Console.WriteLine("B");
Action ab = a + b;
ab();                // A, then B

// exceptions halt the chain: only A runs here
Action guarded = () => { Console.WriteLine("A"); throw new Exception(); };
Action tail = () => Console.WriteLine("tail");
Action chain = guarded + tail;

// to guarantee every handler runs, walk the list manually
foreach (Action handler in chain.GetInvocationList())
{
    try { handler(); }
    catch (Exception ex) { Console.WriteLine($"handler failed: {ex.Message}"); }
}
```

## Q60: How do you implement `IEquatable<T>` correctly, and what invariants must `Equals` and `GetHashCode` respect?

**A:** `IEquatable<T>` gives dictionaries, hash sets, and LINQ's `Distinct` a type-safe equality path that avoids boxing a struct into `object`. The contract is minimal — one method, `bool Equals(T other)` — but the correctness contract is shared with `object.Equals` and `object.GetHashCode`. The triad must stay consistent: if two objects are equal through any equality surface, their hash codes must be identical, and the hash must be derived from immutable fields only, or the object will migrate between hash buckets after insertion and silently disappear from `Contains` lookups.

The implementation discipline: `Equals(T other)` performs type-matched field comparison; `override bool Equals(object obj)` should route through the generic version (an `obj is T t && Equals(t)` guard) so the semantics cannot diverge; `GetHashCode()` must be recomputed from the same fields used by `Equals`. `IEquatable<T>` also carries boxing implications — a struct implementing it in a `List<T>`, dictionary, or generic comparer is compared unboxed, whereas falling back to `object.Equals` would box every probe. That is precisely why BCL types like `Int32` implement it.

Be careful about semantic scope: value equality is a *behavior*, not an identity. For reference types, records get synthesized `IEquatable<T>` via the compiler, but for handmade classes, decide deliberately whether `Equals` means "same fields" or "same instance". Mixing reference identity in some paths and value equality in others is the classic bug. Also override `==`/`!=` when you change `Equals`, or external code will observe two different notions of equality, and never mutate the fields your hash depends on.

```csharp
public readonly struct Point : IEquatable<Point>
{
    public int X { get; }
    public int Y { get; }

    public bool Equals(Point other) => X == other.X && Y == other.Y;
    public override bool Equals(object? obj) => obj is Point p && Equals(p);
    public override int GetHashCode() => HashCode.Combine(X, Y);
    public static bool operator ==(Point a, Point b) => a.Equals(b);
    public static bool operator !=(Point a, Point b) => !a.Equals(b);
}

var set = new HashSet<Point>();
set.Add(new Point(1, 2));
Console.WriteLine(set.Contains(new Point(1, 2))); // True, unboxed probe
```

## Q61: Why is `ICloneable` discouraged in .NET and what should replace it?

**A:** `ICloneable` is the textbook "badly specified interface". Its one member, `object Clone()`, declares *a* clone but not *which* clone: deep or shallow? A `Clone` that returns a fresh object sharing all internals and one that recursively copies every graph node satisfy the same signature differently, so consumers cannot write correct generic code against the interface. Two classes implementing `ICloneable` with divergent semantics make the whole abstraction unusable, which is why modern analysis rules flag it and the BCL stopped relying on it for generic copy semantics.

There is also a type-identity problem: `Clone()` returns `object`, so every caller must cast. Understanding the return type tightens the contract — a typed copy constructor or a `virtual`/`abstract` method returning the concrete type is self-documenting and cuts the cast noise. And in practice a meaningful deep clone of a graph requires manual traversal, which no one-line interface contract can express.

The idiomatic replacements build the intent into the signature: a copy constructor (`new Point(other)`), a factory method returning the typed instance, or — for immutable value types — records and the `with` expression (`other with { X = newX }`) which handles the "slightly different copy" case pervasively. `MemberwiseClone` remains a useful private/protected facility inside a class for fast shallow copies when you explicitly control the semantics, but it should be an implementation detail, not the public contract. If you must expose cloning, return the concrete type and document the depth.

```csharp
// Replace ICloneable with a typed, intent-explicit surface
public record Person(string Name, Address Home);

var original = new Person("Ada", new Address("London"));
var moved = original with { Home = new Address("Berlin") }; // copy + tweak
var same = new Person(original.Name, original.Home);        // explicit copy

public sealed class Matrix : ICloneable
{
    private double[,] _data;

    // typed surface: callers see Matrix, semantics documented as deep
    public Matrix CloneDeep() => new Matrix { _data = (double[,])_data.Clone() };

    // legacy compat only — never rely on it in generic code
    object ICloneable.Clone() => CloneDeep();
}
```

## Q62: What is the command pattern, and how do interfaces and delegates implement it in C#?

**A:** The command pattern encapsulates a request as an object so it can be parameterized, queued, logged, undone, or deferred. The classic shape is an interface with a single `Execute()`, a set of concrete command classes binding a receiver to an action, and an invoker that only knows the interface. This decoupling is what makes undo stacks, job queues, and macro recording possible: the invoker stores command objects without caring what they do.

In C#, delegates collapse most of that machinery. Because `Action`/`Func` are first-class command objects, a line like `queue.Enqueue(() => svc.Redeem(3))` is already a command — an object carrying the receiver and the operation, storable and invocable later. This is the Strategy/Command blur: with few moving parts, lambdas make the pattern almost invisible. The trade-off is observability; a class-based command is inspectable, printable, and undoable. Undo typically needs the *inverse* operation, so the stateful interface — `void Execute(); void Undo();` — retains value where lambdas drop the information.

The senior take is to use interfaces when behavior must be inspectable, serializable, or bidirectional, and use delegates when a single one-shot action is enough. A pragmatic middle is a small `ICommand` interface with a method, mixed with delegate members for the union of "execute now" and "execute later". Either way, the invoker must never reach into the receiver directly through the command layer — that coupling is the whole point of the pattern to remove.

```csharp
interface ICommand { void Execute(); void Undo(); }

sealed class ToggleLight : ICommand
{
    private readonly Light _light;
    public ToggleLight(Light light) => _light = light;
    public void Execute() => _light.Toggle();
    public void Undo() => _light.Toggle(); // inverse is identical here
}

var stack = new Stack<ICommand>();
void Invoke(ICommand cmd) { cmd.Execute(); stack.Push(cmd); }

// the same idea with delegates — lighter but not inspectable
Action flash = () => light.Toggle();
flash();
```

## Q63: How does the decorator pattern work over C# interfaces, and what is the trade-off of wrapping?

**A:** A decorator implements the same interface as its target and forwards decorated calls, adding behavior before, after, or around them. Consumers that depend on the interface cannot tell whether they hold the raw implementation or a chain of wrappers — logging, caching, throttling, and retry layers become transparent additions. Because each decorator is itself an implementation of the same contract, decorators compose and nest arbitrarily: `new Retrying(new Caching(new Slow()))`.

The critical trade-off is identity. A wrapper is a different object, so passing `wrapper` where raw reference equality matters breaks the deal; while decorated objects share the underlying *state*, they do not share the *instance*. Reverse-engineering original types via `is` checks and casts is brittle, and stack of wrappers makes each hop slower and each exception harder to attribute. Test doubles and mocks often stub the decorated outermost layer rather than entering the chain.

Compared with inheritance, decorators win on breadth: wrapping composes vertical slices without multiplying classes — you get 2^N wrappers from N features via composition where inheritance would need N! class shapes. The interface itself is what makes the pattern possible: the wrapper satisfies the same contract so the consumer never learns about the wrapping. If a class must be decorated, its operations should be publicly virtual or behind an interface — non-virtual concrete methods are undecoratable by composition — which is exactly why "interface to an abstract cousin" is a common refactoring goal.

```csharp
interface IWeatherService { int Temperature(string city); }

sealed class CachingDecorator : IWeatherService
{
    private readonly IWeatherService _inner;
    private readonly Dictionary<string, int> _cache = new();
    public CachingDecorator(IWeatherService inner) => _inner = inner;

    public int Temperature(string city)
        => _cache.TryGetValue(city, out var t) ? t : (_cache[city] = _inner.Temperature(city));
}

// chain a retry over a cache over the real service
IWeatherService service = new CachingDecorator(new RetryingDecorator(new OpenWeather()));
```

## Q64: What is the adapter pattern in C#, and how do interfaces plus extension methods enable interface adaptation?

**A:** The adapter reconciles a client's expected interface with a service that exposes something incompatible. The classic adapter wraps the legacy object and forwards translated calls. The wrapper implements the client's interface and contains the legacy instance — connectivity flows through composition, not inheritance — so the adaptee's implementation is reached without pretending the adapter is it. The cost is a forwarding layer: every method on the client interface must be routed and translated.

C# adds two distinctive moves. First, object initializers and interfaces make adapters cheap to assemble. Second, extension methods let you adapt *without a wrapper at all*: if the client only needs a few synthesized behaviors, you can project the adaptee into the client's expected surface directly from outside its type — `legacyFoo.Text()` defined as an extension over `LegacyFoo`. This is static adaptation: purely a compile-time view, no new object, no forwarding overhead. It cannot hold per-call state (no fields), whereas a wrapper class can cache and augment.

The judgment call is which form fits. Wrapper adapters preserve identity per call, can cache translations, and can implement interface obligations in full; functional/extension adapters are dynamic, disposable, but stateless. A classic real-world target is timing: `ReadOnlyMemory` vs `Stream`, `IList<T>` vs arrays, or a third-party SDK where you define an internal domain interface and write adapters over each vendor SDK — keeping your own code untouched by vendor types. That boundary is where adapters earn their keep: one clean interface, many adapters, zero vendor penetration into core logic.

```csharp
interface IContactDataSource { Contact Find(string id); }

// vendor type you must not let leak everywhere
class MailchimpClient { public dict[] Get(string listId) => ...; }

// wrapper adapter: implements the domain interface, shields vendor details
sealed class MailchimpAdapter : IContactDataSource
{
    private readonly MailchimpClient _vendor;
    public Contact Find(string id) =>
        // translate vendor result to domain Contact
        new Contact { Id = id, Name = _vendor.Get("main")[0]["name"] as string };
}
```

## Q65: What is the Null Object pattern and how does it simplify C# code that uses interfaces and delegates?

**A:** The Null Object pattern replaces `null` branches with a real, do-nothing implementation of the same interface. Instead of `if (logger != null) logger.Write(msg)` scattered across the codebase, a `NullLogger` implement-writes nothing, and the code never special-cases absence. The payoff is uniformity: the invariant "the logger is always a logger" holds everywhere, so call sites remove their guards, defaults become the only place the choice happens, and tests can inject the null object explicitly.

Delegates give the pattern a compact form. `Action` and `Func` are initialized to empty lambdas (`_handler = _ => { };`) or left to be `??` substituted at call time, so the "no subscriber" state is a valid, invoke-able value instead of a `null` to step over. In events, initializing the backing field to an empty delegate also silences the null-invocation warnings the compiler otherwise fires. The same idea extends to chains: a no-op element in a composite still participates, so the collection treats it like any other member.

The counter-argument is that null objects can mask bugs — a missing dependency silently does nothing instead of failing loudly, and the empty behavior is easy to confuse with a broken pipeline. Apply the pattern when absence is a legitimate configuration (logging, caching, metrics) and use exceptions or guards when absence indicates programmer error. The litmus: if a `throw` would be the honest reaction to a missing collaborator, Null Object is the wrong tool; if "no-op" is a real state in the domain, the pattern is exactly right.

```csharp
interface ILogger { void Info(string m); }
sealed class NullLogger : ILogger { public void Info(string m) { } }

// subsystem depends on the interface, never on null check punctures
class Processor
{
    private readonly ILogger _log;
    public Processor(ILogger log) => _log = log; // caller passes NullLogger when silent
    public void Run() { _log.Info("starting"); /* ... */ }
}

// delegate flavor
private Action<int> _onProgress = _ => { };
public Action<int> OnProgress { get => _onProgress; set => _onProgress = value ?? (_ => { }); }
```

## Q66: What are static abstract interface members in C# 11 and how do they enable generic math?

**A:** Static abstract interface members let an interface declare operations that apply to the *type* rather than to an instance — signatures like `static abstract T operator +(T a, T b)`, `static abstract int Comparison<T>()` or `static abstract T Zero { get; }`. A generic method constrained by such an interface can then call the member on the type parameter: `T.Zero`, `a + b`. This is the mechanism behind `System.Numerics` — `INumber<T>`, `IAdditionOperators<T,T,T>`, `ISpanParsable<T>` — which makes generic arithmetic real: write `Sum<T>(IEnumerable<T>) where T : IAdditionOperators<T, T, T>` and it works for `int`, `double`, `decimal`, `BigInteger`, custom vectors.

Prior to C# 11 this was fundamentally impossible within the type system. Generic math had to be emulated with `dynamic` (slow, runtime), `Convert.ChangeType` (lossy, no operators), or reflection — all bypassing the compile-time guarantee. The interface restores the promise: the constraint proves an operator exists at compile time, the JIT can specialize the call, and value types avoid boxing because the constrained static dispatch happens without an interface box. The runtime works this magic by lowering `T.Idx` calls into per-instantiation dispatch, so `Sum<int>` has zero allocation beyond the result.

The feature also reopens the static-versus-instance tension from the operator side: because these members are static, they define a *shape* of the type's capabilities, not runtime behavior of a particular object. That means `ref struct` values can now meaningfully participate — there is no boxing to escape — and a type can offer multiple numeric interpretations through separate interfaces instead of overloading the same operator. Use them to build generalized algorithms (graph sums, parsers, serializers) whose correctness is checked once at compile time across all numeric instantiations.

```csharp
using System.Numerics;

static T Average<T>(T[] xs) where T : INumber<T>
{
    var sum = T.Zero;
    foreach (var x in xs) sum += x;
    return sum / T.CreateChecked(xs.Length);
}

Console.WriteLine(Average(new[] { 1, 2, 3, 4 }));           // int     => 2
Console.WriteLine(Average(new[] { 1.5m, 2.5m, 3.5m, 4.5m })); // decimal => 3.0
```

It is worth a caution: static abstracts are resolved at instantiation time, and calling them through a boxed/interface-typed value requires the static constraint to be visible. Store `T` in ordinary generic containers, never downcast to `INumber<T>` on a non-generic path, or the dispatch cost returns and the compile-time guarantees evaporate.

## Q67: What happens when a struct that implements an interface is boxed, and what pitfalls arise?

**A:** Casting a value-type variable to an interface it implements boxes it: the runtime copies the struct's fields onto the heap inside an `object`, carrying its type information so the interface call can dispatch. Every subsequent call through the interface travels through that box — virtual dispatch plus the copy. The arithmetic matters: one box per cast, per element, per collection. A `List<int>` cast to `IEnumerable<int>` once is one box; an `ArrayList` of value types boxed at insert time boxes *every* element at insert. Interfaces are the silent engine of this because `object` casting is visible in code while interface casting hides the allocation.

The semantic pitfall is that boxing copies. Mutating via the box does not touch the original stack variable; if the interface exposes mutation (via an explicit interface member inside the source struct), changes go into the box copy and are lost after the call. The classic bug is a struct with settable interface-implemented properties being modified through an interface reference forever affecting nothing the caller stores. Structs are therefore designed to be immutable or to implement interfaces only in ways that do not expose state mutation.

The remedy is generics. `HashSet<T>`, `List<T>`, and `Comparer<T>.Default` with `where T : IEquatable<T>` keep the struct unboxed: the constrained call dispatches directly to the value-type's implementation, no box allocated, equality implemented by the same-to-same generic path. That is the real reason `IEquatable<T>` exists — not convenience, but to unbox `Equals`. When designing interfaces consumed by structs, prefer generic abstractions over non-generic surfaces, prefer `ref`/`in` passing to `object` parameters, and let constraints preserve value semantics that interface casting would silently destroy.

```csharp
interface IKeyed { void Touch(int value); }

struct Token : IKeyed
{
    public int Value;
    public readonly void Print() => Console.WriteLine(Value);
    public void Touch(int value) => Value = value; // mutation through interface
}

Token t = new Token { Value = 1 };
IKeyed boxed = t;        // box: copy of t now lives on the heap
boxed.Touch(99);         // mutates the box, NOT t
t.Print();               // 1 — the original variable is untouched

// generic path keeps everything inline
List<Token> list = new() { new Token { Value = 1 } };
foreach (ref var item in System.Runtime.InteropServices.CollectionsMarshal.AsSpan(list))
{
    item.Touch(42);      // in-place, no box
}
```

## Q68: How do runtime dynamic proxies for C# interfaces work, and how do mocking frameworks exploit them?

**A:** A dynamic proxy is a class the runtime manufactures *at execution time* that implements a given interface without any hand-written source. .NET builds such classes via `Reflection.Emit`: the proxy type implements the interface's methods by generic forwarding to an interceptor object that receives the method metadata and arguments on every call. `DispatchProxy<T, TProxy>` is the framework-provided shortcut — implement `Invoke(MethodInfo targetMethod, object[] args)` and `Create<T, TProxy>()` gives you a working proxy whose method bodies route into that one handler.

Mocking frameworks (Moq, NSubstitute) are built on exactly this foundation. `mock.Verify(x => x.Foo(arg))` needs the proxy to trap the `Foo` call, record the argument, and return a configured value. Because proxies intercept only *interface members and virtual members* — the proxy is a new class, not a subclass of a sealed type, and non-virtual methods cannot be redirected — that is why Moq requires mocked types to be interfaces or classes with virtual members. The proxy's entire behavior is this interception: strict mocks throw on unconfigured calls, loose mocks return defaults, and setup expressions are translated into the interceptor's routing table.

The sharp edges reveal the object model's limits. Sealed classes and static methods cannot be proxied, so testability dictates design. Value-typed return interception needs care: the proxy cannot intercept struct-typed `Span` returns or `ref` returns at all. And because the proxy is a *different* concrete type than the target, reference-equality tests and `is OriginalType` checks that bypass the interface break. The senior habit: treat proxies as a test-time artifact, let the production dependency graph depend on interfaces, and never leak assertion logic from the proxy into library behavior.

```csharp
using System.Reflection;

sealed class SpyInterceptor : DispatchProxy
{
    public Action<string> OnCall = _ => { };
    protected override object? Invoke(MethodInfo targetMethod, object?[] args)
    {
        OnCall($"{targetMethod.Name}({string.Join(", ", args!)})");
        return targetMethod.ReturnType.IsValueType
            ? Activator.CreateInstance(targetMethod.ReturnType)
            : null;
    }
}

var proxy = DispatchProxy.Create<IPaymentGateway, SpyInterceptor>() as SpyInterceptor;
var gateway = (IPaymentGateway)proxy!;
gateway.Charge("acct-1", 42m);     // recorded via Invoke
```

## Q69: How do dependency injection containers manage interface lifetimes, and what object-model trade-offs do scopes imply?

**A:** A DI container is essentially a two-level indirection: a registry mapping interfaces (and base classes) to concrete factory registrations, and a resolver that materializes the object graph, wiring dependencies by inspecting constructor parameters. Registration syntax — `services.AddScoped<ICartService, SqlCartService>()` — tells the container "when anything asks for `ICartService`, hand it a `SqlCartService` with this lifetime." The container builds the graph transitively, so constructors are the composition root: constructor dependencies *are* the declared model of what a type needs.

The three canonical lifetimes express ownership scope. *Transient* creates a fresh instance per resolution: cheap, stateless, no sharing, but wasteful if the same service is requested ten times in one request. *Singleton* guarantees one instance per container: great for caches and configuration, dangerous if it is stateful or if it secretly captures scoped dependencies. *Scoped* gives one instance per scope (per HTTP request): correct for EF `DbContext` and request-level caches. The classic trap is *captive dependencies* — a singleton capturing a scoped service — which silently shares request-scoped state across requests. Containers from "ValidateScopes" in development catch it; in production it turns into Heisenbugs.

The trade-off on the object-model side is that DI pushes design toward constructor-heavy classes with parameterized interfaces, burying the default-constructor idiom. That is a *feature*: it exposes dependencies explicitly, makes test-substitution trivial (inject fakes at the seam), and centralizes disposal — containers dispose what they create in lifetime order. The cost is ceremony: types gain constructor bloat, and accidental `new` outside the composition root bypasses wiring. The senior rule is to keep containers at the boundary, let objects depend on interfaces, and let lifetimes express ownership rather than pretending they express business intent.

```csharp
services.AddSingleton<IClock, SystemClock>();      // one clock for the app
services.AddScoped<ICartRepository, SqlCartRepo>();// per-request DbContext consumer
services.AddTransient<IOrderMailer, SmtpMailer>(); // stateless, cheap

public class CheckoutService
{
    public CheckoutService(ICartRepository carts, IOrderMailer mailer, IClock clock) { }
    // dependencies via ctor => manifest for the container graph
}
```

## Q70: When should you choose the template method pattern (abstract classes) versus the strategy pattern (interfaces/delegates) in C#?

**A:** Template Method places the algorithm's skeleton in a base class: abstract steps are hooks, concrete steps are fixed, and derived classes supply the variable parts. It is inheritance-based — the shared workflow and the specialization are tightly bound in one class hierarchy. Strategy instead extracts the *whole* algorithm (or its variable steps) behind an interface or delegate, injects it into a client, and lets composition swap behavior at runtime without creating a new subclass. Strategy is the composition-based sibling.

The decision driver is whether the variation is *the same skeleton, different steps* or *arbitrary interchangeable behavior*. If you have a fixed workflow — "lock, validate, send, log" with only the 'send' varying — Template Method keeps that invariant in once place and prevents callers from reordering it; Strategy would require the caller to reconstruct the entire workflow each time. If the behavior is truly pluggable — a sort predicate, a payment gateway, a persistence flavor — Strategy composes cleanly and, unlike inheritance, does not trap the varying part inside a fixed hierarchy. C# tilts toward Strategy: composition, interfaces with default members, and delegates are first-class, and the inheritance tree is the most rigid axis of the object model.

Watch the middle zone. A common refactor is Template Method whose steps become delegates — `Send(Action send, Action log)`. That keeps the invariant and the variation while removing subclassing entirely, which is usually a win. Use Template Method when the skeleton *is* the domain concept and subclasses still need other inherited machinery; otherwise prefer Strategy for testability (inject a fake strategy) and for `sealed`/immutable clients. The litmus: can you name the fixed skeleton and the free degrees of freedom? If yes and they're stable, Template Method; if the degrees grow independently, Strategy.

```csharp
// Template Method: skeleton in base, steps in derived
abstract class TelemetryJob
{
    public sealed void Run()
    {
        OpenChannel();
        Collect();
        Transmit();
        Close();
    }
    private void OpenChannel() { /* fixed */ }
    private void Close() { /* fixed */ }
    protected abstract void Collect();
    protected abstract void Transmit();
}

// Strategy: algorithm behind an interface/injected behavior
interface ITelemetryStrategy { void Send(Telemetry t); }
sealed class KafkaTelemetry : ITelemetryStrategy { public void Send(Telemetry t) { } }
sealed class LogTelemetry : ITelemetryStrategy { public void Send(Telemetry t) { } }

var client = new TelemetryClient(new KafkaTelemetry()); // swap without subclassing
```

## Q71: How do you build an event aggregator or mediator in C# using events and delegates?

**A:** An event aggregator is a hub: publishers post typed notifications to the hub, and subscribers register for kinds they care about; the hub delivers without letting publishers know their audiences. In C# the simplest aggregator is a dictionary keyed by message type, mapping to `Action<object>` handles, with `Publish(T message)` invoking the matching multicast delegate. Because the dictionary value is a `MulticastDelegate`, many subscribers to one message type chain naturally, and a `WeakReference`-collected subscription list keeps long-lived hubs from leaking short-lived subscribers.

The mediator extends the idea with request/response: `TResponse Send<TRequest, TResponse>(TRequest)` routes a typed command to a registered handler. Both patterns fight the fundamental coupling the direct `+=` event idiom has — with raw events, the publisher and subscriber must directly reference each other, coupling to connect. The hub inverts that: publishers depend on the hub, subscribers depend on the hub, and the two never meet. That inversion is exactly what makes aggregates (domain events) and CQRS command pipelines testable and swappable.

The pitfalls are lifecycle and debugging. Every subscriber must unsubscribe when it dies or the hub pins it; prefer weak-referenced subscriptions or scope-bound disposal. Include a `NoSubscribers` diagnostic: a published message nobody handles is either a bug or an optimization opportunity, and silent drops are how these systems hide failures. Threading matters too — a hub invoked from a request thread delivers on that same thread, so UI updates need marshaling. A mature implementation eventually grows filtering, ordering, and async delivery over a plain multicast chain, which is where lightweight message bus libraries take over.

```csharp
sealed class EventAggregator
{
    private readonly Dictionary<Type, Delegate> _handlers = new();

    public void Subscribe<T>(Action<T> handler)
        => _handlers[typeof(T)] = Delegate.Combine(Get<T>(), handler) ?? handler;

    public void Publish<T>(T message)
        => Delegate.RemoveAll(Get<T>(), null) switch
        {
            Action<T> handlers => handlers(message),
            null => throw new InvalidOperationException($"No subscribers for {typeof(T).Name}")
    };
    private Delegate? Get<T>() => _handlers.TryGetValue(typeof(T), out var d) ? d : null;
}

// Publisher knows only the hub; subscriber registers only its own interest
aggregator.Subscribe<OrderPlaced>(evt => emailer.Send(evt.CustomerId, evt.Total));
aggregator.Publish(new OrderPlaced { CustomerId = "c1", Total = 42m });
```

## Q72: Why are `async void` event handlers dangerous, and how should asynchronous exceptions be handled in events?

**A:** An `async void` method returns no `Task`, so the caller cannot await, and — critically — any exception it throws escapes through the SynchronizationContext. On the UI thread that surfaces as an unhandled exception, which, depending on configuration, can bring the process down or silently kill the continuation; on the thread pool it is exactly the "crashy tap-tap-tap bug" where every handler invocation spawns a fresh risk. There is no hook to await completion, observe failures, or attach a continuation, so `async void` is sanctioned only for top-level event handlers and lambda event handlers in the default-oblivious startup where no other shape exists.

The consequence for event design: raising a `Task`-returning event is the robust alternative, but events are multicast, and `Func<Task>` handlers must be awaited collectively. The common contract is `async Task`-returning handlers with an `EventHandler` that awaits each handler sequentially or merges them with `Task.WhenAll` while still firing all subscribers. Even there, each handler should swallow its own exception or carry it on a shared `AggregateException`, since one blazing handler should not prune the remaining subscribers — the multicast chain halts on the first throw.

The mitigation list is short. (1) Prefer `Task`-returning methods everywhere except the outermost UI glue. (2) For plain events, use `EventHandler` and document that handlers are synchronous; if you need async, provide an `AsyncEventHandler<T>` returning `Task` and a raise helper that awaits all. (3) When fire-and-forget is unavoidable, capture the `Task` from the async void handler, `ContinueWith` on it to route exceptions to a logger, and never let an exception inside `async void` visit an untouched SynchronizationContext. The invariant you're protecting: an event raising must not be able to crash the process.

```csharp
// AsyncEventHandler returning Task — exceptions stay observable
public delegate Task AsyncEventHandler<T>(object? sender, T e);

public event AsyncEventHandler<DataChangedEventArgs>? DataChanged;

private async Task RaiseAsync(DataChangedEventArgs e)
{
    var handlers = DataChanged?.GetInvocationList();
    if (handlers is null) return;

    var tasks = handlers.Cast<AsyncEventHandler<DataChangedEventArgs>>()
                        .Select(h => SafeInvoke(h, e));
    await Task.WhenAll(tasks);
}

private async Task SafeInvoke(AsyncEventHandler<DataChangedEventArgs> h, DataChangedEventArgs e)
{
    try { await h(this, e); }
    catch (Exception ex) { log.Error(ex); } // never let one handler kill the raise
}
```

## Q73: What is `TaskCompletionSource<T>` and how does it bridge callback-based delegates to `Task`?

**A:** `TaskCompletionSource<T>` is a leash for an externally-produced `Task`. It owns one `Task<T>` whose completion you control from anywhere: call `SetResult`, `SetException`, or `SetCanceled`, and every await on that task resumes with the corresponding outcome. Crucially the `Task` you expose is not a pile of running work — it is a placeholder whose lifecycle you dictate, which is exactly what bridges a callback-based API (events, TRPCs, native peers, message queues) into the `await`-world without executing anything on a thread.

The bridge works by converting the callback boundary: subscribe to the callback-based source, and convert its success/error signals into `SetResult`/`SetException`. The caller then does `var result = await ConnectAsync(...)` and gets idiomatic cancellation by combining the TCS task with `CancellationToken`. Internally .NET uses this constantly — `Stream.ReadAsync`, socket reads, `SemaphoreSlim.WaitAsync` — every async-over-callback seam is a TCS under the hood. For the rare truly-asynchronous-but-already-synced case, `SetResult` also guards double-completion: calling it twice throws, forcing you to decide idempotence explicitly.

The trap is synchronous completion masquerading as async. If you `SetResult` on the same thread that awaits, you get a synchronous continuation — defeating the point of async. The classic remedy is `TaskCreationOptions.RunContinuationsAsynchronously`, which schedules continuations onto the thread pool regardless of the completing thread. And for value-type hot-paths, `ValueTask` + `ManualResetValueTaskSourceCore<T>` replaces TCS with roughly zero allocation. The senior litmus: when you await a `Task`, know whether it is processed work (likely wrapping an algorithm) or a boxed external signal (a TCS); the second is where lifecycle bugs — forgot to set, twice set, continuation-starvation — actually bite.

```csharp
public static Task<SocketResult> ConnectAsync(Socket socket, EndPoint ep, CancellationToken ct = default)
{
    var tcs = new TaskCompletionSource<SocketResult>(TaskCreationOptions.RunContinuationsAsynchronously);

    socket.BeginConnect(ep, ar =>
    {
        try
        {
            socket.EndConnect(ar);                  // re-throw any connect error here
            tcs.SetResult(new SocketResult(socket));
        }
        catch (Exception ex) { tcs.SetException(ex); }
    }, null);

    ct.Register(() => tcs.TrySetCanceled());
    return tcs.Task;
}

var result = await ConnectAsync(socket, endpoint); // callback interface, awaited clarity
```

## Q74: How does the compiler implement delegate closures, and what are the capture semantics pitfalls?

**A:** When a lambda references variables from its surrounding method, the compiler hoists those variables into a compiler-generated closure class as fields, and the lambda becomes an instance method of that hidden class with a `this` binding. Because the fields live on the closure object, they outlive the method that created them — the closed-over variable is a *shared heap cell*, not a local copy. Two lambdas capturing the same variable share the same cell, and a lambda that outlives its creator keeps that cell, and everything reachable from it, alive: the classic reference to a large object held by a long-lived callback.

The classic capture bug is the loop-variable capture. Pre-C# 5, `for (int i = 0; ...) tasks.Add(() => i)` captured one `i` reused by all iterations, so every lambda saw the final value. C# 5 reversed course with `foreach` by giving each iteration its own synthesized variable, and C# currently recommends `int copy = i;` for `for` loops when you need per-iteration snapshots. Understanding the mechanism — capture is per-variable, not per-value — explains why: the fix is a fresh variable per iteration, which each closure then captures independently.

Performance informs the design. Each closure allocation is a heap object holding every captured variable, even those unused later; `static` lambdas (no capture) compile to cached method groups with zero allocation; and avoiding capture in hot paths means moving the reader-constant out of the lambda. There is also a scope subtlety: after C# 5, the closure for a `using`-scoped variable inside a loop creates *one closure per execution of the using block*, not per variable declaration point, which is why capturing inside loops still surprises the unwary. Read the IL with a dump tool whenever you suspect a closure: the class will be named `<>c__DisplayClass0_0` and its fields are the truth.

```csharp
// capture-by-variable: single cell, all lambdas share it
var funcs = new List<Func<int>>();
for (int i = 0; i < 3; i++)
    funcs.Add(() => i);
foreach (var f in funcs) Console.WriteLine(f()); // 3 3 3

// per-iteration snapshot: new cell per iteration
funcs.Clear();
for (int i = 0; i < 3; i++)
{
    int copy = i;
    funcs.Add(() => copy);
}
foreach (var f in funcs) Console.WriteLine(f()); // 0 1 2

// static lambda: no closure at all, compiler caches the method group
numbers.Select(static n => n * 2).ToList();
```

## Q75: What are custom event accessors and how do they affect thread safety of events?

**A:** C# events normally synthesize a hidden field of the delegate type plus compiler-generated `add` and `remove` accessors. Custom accessors replace those body balls with your own storage and logic while keeping the `+=`/`-=` syntax at the call site. `add`/`remove` are your chance to intercept subscription — refuse a subscription, count subscribers, swap in a thread-safe even store, or route to an external sink. The public surface stays the same; what changes is *where* subscriptions live and how they are enforced.

The thread-safety nuance is that bare field events are not atomic. `eventHandler?.Invoke(this, e)` reads the field then invokes the chain uncovered by a removal between read and invoke — the classic race where an unsubscribed handler still runs once, or a null read happens after a subscription between the check and the call. The framework-idiomatic fix is `Interlocked.CompareExchange` on the backing field so add/remove is atomic, then a local copy `var handler = field;` before invoking. Custom accessors let you centralize that discipline — every raise copies once, nobody reads the field directly, and the compiler no longer generates the naive read.

Beyond correctness, custom accessors can enforce invariants: prevent double-subscribing the same instance, forbid subscribing after disposal, or implement a *one-shot* event that auto-unsubscribes. They also expose the symmetry warning — `remove` matching is by delegate equality, so asymmetric accessors (allow plus, disallow minus) are legal but pathological. The realistic guidance: leave accessors implicit for ordinary events, and make them custom only when the field is storage, the raise path needs documented semantics, or you need strictness that the synthesized version cannot express. For thread safety specifically, prefer `EventToWeak`-style helpers or field-backed storage with explicit locks over handwritten `lock(this)` pits.

```csharp
public event EventHandler<string>? Notified
{
    add
    {
        // refuse subscriptions from dead scopes: protect & record
        lock (_gate) { _calls = (EventHandler<string>?)_calls + value; }
    }
    remove
    {
        lock (_gate) { _calls = (EventHandler<string>?)_calls - value; }
    }
}

private EventHandler<string>? _calls; // backing storage under a lock

private void Raise(string message)
{
    var handler = _calls;              // snapshot: no torn read
    handler?.Invoke(this, message);
}
```

## Q76: How does constructor chaining with `base()` and `this()` drive object initialization order in C#?

**A:** C# mandates a constructor call flow: every constructor must chain to another on the same type via `this(...)` or to the base type via implicit or explicit `base(...)`, terminating in `System.Object`. The observable consequence is strict ordering — the chain runs from the root down, but with a crucial interleave: for each type, instance field initializers run *before* that type's constructor body. So the effective sequence is root field initializers, root constructor body, then each derived level's field initializers and constructor body, finally the leaf. A derived constructor cannot observe its own fields before the base constructor has completed, which is precisely why passing derived state upward through `base(...)` is constrained — the base is being constructed before the derived fields exist.

The `this(...)` form reuses sibling constructors, letting one canonical initializer be the funnel: `public Point() : this(0, 0) { }` delegates to the two-argument constructor. This keeps defaults sane and prevents logic duplication. Field initializers are worth scrutiny: they execute in textual order at each level, and they cannot reference `this`-state, so a field initializer that needs the result of another initializer must be ordered carefully — the compiler guarantees textual order but not "obviousness." Static field initializers obey analogous rules under type initialization, first per type when the type is first accessed.

The sharpest pitfall is virtual calls from a base constructor. When a base constructor body invokes a virtual method, dispatch goes to the *most-derived* override even though the derived constructor has not run yet — derived fields are still default. The result is viewing an object mid-construction, which is why the analyzer wags the finger at virtual calls inside constructors. The invariant to internalize: constructors guarantee "the type's own level is ready before its body runs," but an object is not fully ready until the whole chain ends. Build objects through factory/static methods when you need multi-phase setup that leverages virtual dispatch.

```csharp
class Widget
{
    private readonly string name = "base-";   // runs before Widget ctor body
    public Widget() { Console.WriteLine($"widget({name})"); }
    public Widget(string id) : this() { Console.WriteLine("widget(id)"); }
}

class SuperWidget : Widget
{
    private readonly int level = 7;           // runs AFTER base ctor body
    public SuperWidget() : base("x")
    {
        Console.WriteLine($"super(level={level})");
    }
}

new SuperWidget();
// widget(base-)   <- field init + ctor body of Widget
// widget(id)      <- this() chain completed first
// super(level=7)  <- derived level finally initializes
```

## Q77: What are `static` classes and static state, and what object-model problems do they introduce?

**A:** A `static` class is a sealed, abstract, non-instantiable container for static members — compile-time enforced as a pure utility namespace with no instance surface: no constructor calls, no `new`, no instance fields. The object model treates it as the "library of functions" shape: `Math`, `File`, `Console`. That is healthy when the class has no identity or state — pure functions and stateless conveniences. The instant a `static` class accumulates `static` mutable fields, it has smuggled *global mutable state* into the object model without any of the controls that instances enjoy (encapsulation through instances, lifetime management, DI, test isolation).

The problems cascade. Global static state is shared process-wide, so any two callers, two libraries, or two tests observe and mutate one another through the same cell; concurrency requires locking discipline nobody owns; and ordering of static initialization (`beforefieldinit`, static constructors) becomes a cross-cutting surprise when initialize order matters across types. Testability collapses — a static cache or static clock cannot be faked at the seam because there is no instance to substitute, which forces `[CallerMemberName]`-style indirection hacks, virtual static helpers, or `IDisposable`-style reset hacks just to run deterministic tests.

The senior remedy is to demote static state into instance services managed by a container. `static` *constants* and pure stateless helpers stay static; anything holding mutable state becomes a scoped or singleton instance behind an interface — `IClock`, `ICache`, `IEventPublisher` — injected where consumed. The occasional justified global is a deliberate, documented singleton (with carefully-shaped initialization) or thread-safe `Lazy<T>`. The diagnostic when reviewing code: a `static` field being *written* after static construction is a design smell worth re-ownering; the value of static is statelessness, not globality.

```csharp
// Smell: global mutable state dressed as a utility
public static class Settings
{
    public static string Region { get; set; } = "eu";
    public static int TimeoutMs { get; set; } = 1000;   // mutable, process-wide, hidden
}

// Managed: injectable, testable, well-lifetimed
public interface ISettings { string Region { get; } int TimeoutMs { get; } }
public sealed class AppSettings : ISettings
{
    public string Region { get; init; } = "eu";
    public int TimeoutMs { get; init; } = 1000;
}
// services.AddSingleton<ISettings>(sp => Config.Load<AppSettings>());
```

## Q78: What are `readonly struct`, `readonly` members, and how do `in` parameters protect value types?

**A:** A `readonly struct` declares that no instance member may mutate state — all fields must be `readonly` or the compiler rejects writes — so the type is intrinsically immutable. `readonly` on an individual member marks a single method or property as non-mutating, letting instance accesses avoid defensive copies. The chain of reasoning: in C# an instance member of a mutable struct *may* mutate it, so when the compiler cannot prove safety it copies the struct to be sure the original stays intact (defensive copying). Marking members `readonly` proves the member is safe, and the compiler skips the copy — a real win for hot paths that touch large value types.

`in` parameters complete the story by passing value types by reference (read-only reference): `double Length(in Point p)`. The caller may pass a location directly — no copy — and the callee cannot write through the parameter. Used alongside `ref readonly` returns and `scoped`, these turn value types from "copied-by-default, allocate-under-interface" into ref-forwarding, allocation-free cooperators at the cost of tricky aliasing rules. `in` parameters also centralize the compromise: value semantics (no mutation escapes) without the copy.

The traps are nuance. A `readonly` member can still return mutable state or call non-readonly members *of other* structs, so immutability is not transitive. And because overload resolution prefers the by-copy version, `in` mutations can be "forgotten" — the classic `in` bug is passing a location whose mutated value the callee stores, only for the mutation to be lost because a copy was made. The guidance: mark fields `readonly`, mark members `readonly`, prefer `in` for large-but-copied-passed value types, measure the defensive-copy cost before sprinkling `in` everywhere, and never mutate a struct through a `readonly` reference (the compiler will silently copy to keep you honest).

```csharp
public readonly struct Celsius
{
    private readonly double _degrees;
    public Celsius(double degrees) => _degrees = degrees;

    // readonly member => no defensive copy when receiver is readonly
    public readonly Celsius ToFahrenheit() => new(_degrees * 9.0 / 5.0 + 32);
    public readonly double Value => _degrees;
}

// in passes by ref without copies and guarantees no mutation through the parameter
static double Average(in Celsius a, in Celsius b)
    => (a.ToFahrenheit().Value + b.ToFahrenheit().Value) / 2;
```

## Q79: Why can't `ref struct` values implement most interfaces, and how does C# 11's static abstract members change that?

**A:** A `ref struct` (the kind `Span<T>` and `ReadOnlySpan<T>` are) is a stack-only value type: the runtime forbids it from escaping to the heap — it cannot be boxed, cannot appear as a field on a heap-allocated class, cannot be captured into a closure or `async` state machine, and cannot be stored on the heap in generic form. Interfaces are inherently heap-escape shaped: storing an interface-typed value is storing a reference to a boxed/heap representation, so any instance-interface implementation would reopen exactly the boxing-and-escape hole `ref struct` closes. Hence the language's blanket rule: a `ref struct` cannot implement an instance-based interface.

The reason the rule has an exception is that static abstract interface members (C# 11) are precisely *not* instance-shaped. They describe the type's static API — operators, factory methods, constants — with no object to box, so a `ref struct` can satisfy those contracts safely. That is what unlocks real generic math and utility algorithms over spans: `T.IndexOf(spans)` style code or vector-length abstraction can constrain `T : ISpanParsable<T>` and work with a fully stack-based implementation. The instance side stays closed; the static side is open.

The design consequence: if you want an interface *behavior* from a `ref struct` — iterate, count, format — you express it through static/extension operations taking `Span<T>`/`ref struct` parameters, so a `SpanSequencer` service or `SpanExtensions` static class replaces the `IEnumerable<T>` you would ask of a heap-erect type. It feels unusual, but it is how `MemoryMarshal`, `Utf8Formatter`, and `string.Create` compose. Before reaching for interfaces over ref-shaped data, confirm the abstraction crosses the heap boundary; if it does, `ref struct` is wrong for the job regardless of the temptation.

```csharp
// C# 11 permits static abstract members on ref struct implementations
ref struct ByteRun : IAdditionOperators<ByteRun, ByteRun, ByteRun>  // static-only: legal
{
    public Span<byte> Data;

    public static ByteRun operator +(ByteRun a, ByteRun b)
        => new ByteRun { Data = ... }; // merge into caller-provided space

    // instance members are fine — just no interface-based instance dispatch
}

// The compiler error from trying the old way is a feature, not a bug:
// Span<T> must never be boxed into IEnumerable<T> and lost to the heap.
```

## Q80: How does `Nullable<T>` behave during boxing, and what are lifted operators?

**A:** `Nullable<T>` has a weird special case in the type system: when a boxed `Nullable<T>` has no value, the box is simply `null` — there is no box containing a flag. `((object)new int?()) is null` is true, which is exactly why `int? x = null; x == null` and `x is null` behave the way they do. When the nullable *has* a value, boxing produces a box containing the underlying `T` value itself, not the `Nullable<T>` — so `(object)(int?)5` boxes an `int` 5. This means a `GetType()` call on a boxed nullable with a value reports the underlying type (`System.Int32`), and any code that pattern-matches on `Nullable<T>` after a value has been boxed will not find it.

Lifted operators are the arithmetic superpowers of nullable types: when one operand is `null`, the result is `null` — `int? a = 5, b = null; a + b` is `null`, and comparison with `null` is `false` except equality. The compiler synthesizes "lifted" implementations by applying the underlying operator and returning `null` on `HasValue == false`. This cascades nicely for calculations where a missing input should propagate emptiness, but trips people in LINQ: `xs.Max(x => (int?)x)` returns `null` for an empty sequence while `Max(x => x)` on `int` throws `InvalidOperationException`, and `sum ?? 0` becomes the idiomatic collapse.

The pitfalls hide in the edges. A lifted `==` returns `bool` but is three-valued in spirit (`null == anyone` is never true), so `a <= b` with both null is `false`, which contradicts the `a >= b && a <= b` intuition — write three-valued comparisons deliberately when the domain needs "unknown". And beware the pre-generic collections: `ArrayList` boxes your `Nullable<int>` into either a boxed int or a null, erasing the distinction, which is why nullable value types with value semantics need generic containers to stay honest. Understand the box always, and write your domain around the "null means missing, not less" semantics.

```csharp
int? a = 4, b = null;

object boxed = a;            // boxed is an int (value 4)
object boxedNull = b;        // boxedNull is null — no box at all
Console.WriteLine(boxedNull == null); // True
Console.WriteLine(boxed.GetType());   // System.Int32, not Nullable<Int32>

Console.WriteLine(a + b);    // null (lifted operator)
Console.WriteLine(a + 2 == 6);                         // True
Console.WriteLine(null > null);                        // False (lifted comparison)
Console.WriteLine((int?)Enumerable.Empty<int>().Max()); // null, no throw
```

## Q81: What invariants does the root `System.Object` contract impose, and why is `GetType()` non-virtual?

**A:** Every type inherits four behavioral members from `System.Object`: `Equals`, `GetHashCode`, `ToString`, and `GetType`, plus `MemberwiseClone` and `Finalize` as protected/implementation hooks. Of those, only `GetType` is non-virtual and sealed. The others are virtual *by design* — they encode "behaviors a shape must honor" — and the contract around them is contractual: `Equals` must be reflexive, symmetric, and transitive (the one-sentence honesty test: if you cannot say "a equals b whenever they are the same thing", you have broken it), and two equal objects must produce equal hash codes. The hash code is a correlation, not an identity; `GetHashCode` existing at all exists so value-anything can land in dictionaries and hash sets while staying comparable via `Equals`.

`ToString` is virtual because a human-readable representation is per-type information, and every unhelpful `namespace.Type` default every novice complains about is the honest default for a type that has not decided what to print. The asymmetry of `GetType` is deliberate: if `GetType` were virtual, a derived type could lie about its runtime type, breaking type-safety guarantees from the inside. The runtime pins it non-virtual because the runtime itself must be able to answer "what is the actual class of this object" without consulting (and being thwarted by) any overridden member. `GetType` returning the *runtime* type even when accessed via a base reference captures that — polymorphism of data, not of the identifier.

The senior discipline of overriding any `object` member is same-complete: override all of them together. If you customize `Equals`, customize `GetHashCode` to match and consider `==`/`!=`; if you rely on identity semantics, do not override anything. The classic legacy failure mode — two different implementations equal but hash differently — is precisely a violation of this invariant, silently destroying dictionary lookups. When a type cannot promise symmetric, transitive equality, it should not export one at all; that is when `ReferenceEquals`, `IEqualityComparer<T>` injections, and identity-based config win.

```csharp
public sealed class Identifier
{
    public string Value { get; }

    public override bool Equals(object? obj) => obj is Identifier other && Value == other.Value;
    public override int GetHashCode()        => Value.GetHashCode();
    public override string ToString()        => $"#{Value}";

    // GetType() is sealed and non-virtual on the base:
    //   GetType() == typeof(Identifier) is guaranteed, always.
}
```

## Q82: How do default interface members support API versioning in .NET libraries?

**A:** Default interface methods (DIM) let an interface carry a body, so a library author can add a member to an already-shipped interface without breaking every existing implementer — binary-breaking that would otherwise force a major version. Consumers of the previous interface keep compiling; new callers can reach the default. This directly answers the "versioning additive but non-breaking" question, and it is the main reason DIM exists: contract evolution in the wild, not just a language toy. The members are instance-shape but with a default implementation dispatched when the implementing type does not supply its own.

Dispatch gets delicate, and that delicacy is the honest cost. A class member always beats the interface default (implicit class implementation wins), but *explicit* interface implementations and re-abstraction (`abstract` overridden defaults in a derived interface) alter who wins when more than one interface contributes the same signature. The diamond ambiguity C# resolves predictably but with nuances: with two interfaces each offering a default for the same member, the closest (most derived) interface wins, and a conflict between equal-rank interfaces is a compile error demanding an explicit implementation. So the default is a *suggestion with precedence rules*, not a virtual method on the implementing type.

The operational recommendation is to prefer additive capabilities as *separate* interfaces (`IJsonSerializable`, `IReadOnlyThing`) and reserve DIM for genuinely one-interface evolution, where the removal path of an old contract still matters. Overusing DIM collapses interfaces into de facto abstract classes with the worst of both worlds — a class-ish body on a value-ish contract, and mocking friction because Moq-era cruft predates dynamic defaults. When you do version, document the default as the *backward-compatible* behavior and update the default to keep old implementers working even as nuanced warnings nudge them toward upgrading.

```csharp
// v1 shipped with just Read
public interface IStore
{
    byte[] Read(string key);
}

// v2 adds Write with a default so existing implementers compile unchanged
public interface IStore
{
    byte[] Read(string key);

    void Write(string key, byte[] value) =>
        throw new NotSupportedException("optional capability; implement to enable writes");
}

class LegacyStore : IStore { public byte[] Read(string key) => new byte[0]; }
// LegacyStore still compiles. NewStore can supply Write and get full semantics.
```

## Q83: How should custom exception class hierarchies be designed in C#?

**A:** Derive from `Exception` (or a purpose-built base like `ApplicationException`-era choices, though those are historical noise), suffix the name with `Exception`, and expose the three canonical constructors: parameterless, message-only, and message-plus-inner-exception. That trinidad mirrors the BCL contract that existing catch sites and serializers expect — any code doing `throw new KnownException(msg, inner)` should find the same shape on your type. Structure properties for preserving context: `public int OrderId { get; }` on an `OrderNotFoundException`, populated in the constructor — retry, diagnostics, and UI all benefit from typed fields instead of re-parsing `Message`.

The hierarchical design question is whether concrete exceptions share a base. `ValidationException`/`PersistenceException` groups let general catch-sites (`catch (PersistenceException)`) handle a family while callers that need specificity catch the leaf and rethrow the rest — the polymorphic exception hierarchy is the *other* inheritance hierarchy worth having. Design severity by breaking sorted: framework-internal failures, today's data showing up tomorrow in the schema (serialization break), and cross-process boundary conditions (`IOException`) deserve checked-in categories; ad-hoc strings get thrown on every code path are the enemy.

The discipline that separates senior from junior: never `throw new Exception("...")` at the boundary, always preserve the inner exception, and keep the hierarchy shallow and behaviorless — no logic in exceptions (they are DTOs), just context. Also honor the serialization constructor for remoting/streaming if you deploy on exotic boundaries, and beware that an exception type with unexpected fields that break `ToString` convention hurts debugging more than the stack alone. When in doubt, reuse BCL exception types and add a context property wrapper, because `daysSinceEpoch`-style invented hierarchies age worse than honest domain ones.

```csharp
public class OrderNotFoundException : Exception
{
    public string OrderId { get; }

    public OrderNotFoundException(string orderId)
        : base($"Order '{orderId}' was not found.") => OrderId = orderId;

    public OrderNotFoundException(string orderId, Exception? inner)
        : base($"Order '{orderId}' was not found.", inner) => OrderId = orderId;
}

try { var order = GetOrder("o-404"); }
catch (PersistenceException)   { Handle(PersistenceDown); }
catch (OrderNotFoundException) { Handle(NotifyUser); }   // leaf specificity
```

## Q84: How do anonymous types, tuples, and records differ in their object-model and equality semantics?

**A:** Anonymous types are compiler-generated sealed classes: `new { Name = "Ada", Age = 36 }` produces an internal class with `readonly` properties and synthesized `Equals`/`GetHashCode` that do *value-based* comparison on each member. They are immutable, limited to the enclosing method/scope (their type name is not generally declarable), and — crucially — they implement structural equality while being reference types. Two separately-created anonymous objects with identical member values compare equal; the equality is genuine value equality, but the type cannot be named or reused across assembly boundaries.

Tuples come in two flavors. `Tuple<T1,T2>` (the old class) is a heap identity object with no structural equality — `Item1`, `Item2`, and reference comparison. `ValueTuple<T1,T2>` is the modern struct: lightweight, mutable-by-default (Item3 assignments allowed), and — a subtlety people trip on — *shamefully* it does **not** override `Equals`/`GetHashCode` structurally as a default in all paths; the compiler includes equality via `==` and the `Equals` convention only when used through deconstruction contexts. Value equality for tuples is available via `==` on `ValueTuple` and via `ITuple`-backed comparisons, but the plain `Equals` can diverge if your team expects `(1,2) == (1,2)` to mean identical values everywhere.

Records bridge the gap with named, type-safe, immutable value semantics: `record Person(string Name, int Age)` gives you a labeled type with identity, `with`-expression copying, deduplicated `Equals`/`GetHashCode`, and `ToString` on the same value-equality philosophy people wanted from anonymous types. The deciding factors: anonymous types for local shape-once data; `ValueTuple` for transient grouped returns (esp. deconstruction patterns and `KeyValuePair`-adjacent plumbing) where you accept mutable lightweightness; records when the shape deserves a name, immutability, and equality semantics — which is most domain modeling.

```csharp
var anon = new { Name = "Ada", Age = 36 };           // sealed class, value-equal, unnamed
var anon2 = new { Name = "Ada", Age = 36 };
Console.WriteLine(anon == anon2);                    // True (structural)

var t1 = (Name: "Ada", Age: 36);                     // ValueTuple, mutable by default
t1.Age = 40;                                         // allowed
var t2 = (Name: "Ada", Age: 36);
Console.WriteLine(t1 == t2);                         // values equal for ==

record Person(string Name, int Age);                 // named, immutable value semantics
var p = new Person("Ada", 36);
var p2 = p with { Age = 40 };                        // non-destructive copy
Console.WriteLine(p == new Person("Ada", 36));       // True (record value equality)
```

## Q85: Do records support inheritance and object hierarchies, and how does equality behave in derived records?

**A:** Records are classes (by default) and fully participate in inheritance: a record can be `sealed record`, `abstract record`, or extend another record with `record Derived : Base`, gaining constructor chaining (`: base(...)`) and inherited members. The synthesization rules hang together: `Equals`/`GetHashCode` are generated from the *runtime type* — equality compares the `EqualityContract` (which is exactly the runtime type) plus declared members at each level. That is why a base `Base("a")` and a `Derived("a")` with no extra fields are still unequal: the equality contract says they have different runtime types, so the comparison fails before looking at field values.

The consequence for `with` expressions is where seniors get lost. `with` on a base-typed variable produces a copy *of the runtime object's actual type* — a `Base x = new Derived(...); var y = x with { ... }` yields a `Derived`, not a `Base` — because `with` uses the hidden clone method on the actual type. So polymorphic containers of records copy correctly and stay polytypical. The flip side: hand-written derived records must remember the `PrintMembers` and `Members` virtual seam if they customize output, and the synthesized equality carefully combines base and derived member lists so `Equals` is sound without per-level overrides.

The versioning hazard worth flagging: adding a field to a base record silently changes equality for every derived record — a data-shape change propagates to unrelated comparison sites. Similarly, records intended for inheritance should mark non-equality members with `[property: JsonIgnore]`-style attributes or use `sealed`/nonsealed membership deliberately. If equality must be identity-based in an inheritance tree, records are the wrong tool — prefer classes or make the record `sealed`. When designing record hierarchies, ask whether equality *should* be value-based across the hierarchy at all; often only the leaf domain records want it, which argues for shallow, sealed record families.

```csharp
public record Shape(string Label);
public record Circle(string Label, double Radius) : Shape(Label);

Shape s = new Circle("wheel", 4.0);
var rotated = s with { Label = "rotated" };   // still a Circle
Console.WriteLine(rotated.GetType().Name);    // Circle

Console.WriteLine(new Shape("wheel") == new Circle("wheel", 4.0)); // False — runtime types differ
```

## Q86: What are the equality and removal semantics of delegates in C#?

**A:** Delegate equality is *identity-plus-binding*: two delegates compare equal when they point at the same method on the same target instance (`Target` and `Method`). For static methods, the target is null and the method must match; for instances, the specific object matters — two different objects with identically-named methods are not equal, because the binding differs. Multicast delegates compare by walking both invocation lists in lockstep, element by element, so `(a + b) == (a + b)` is true while `(a + b) == (b + a)` is false — order is part of the value. That is why subscribing the *same cached* handler to an event and unsubscribing works, but two textually identical lambdas are different delegates and `-=` against a fresh lambda silently no-ops.

The removal semantics hide collateral: `c = a + b + c; c -= b;` removes only the *last* matching b in the chain, not the first, and `-=` on a delegate that appears multiple times leaves the earlier copies intact. Combined with the equality being per-element, this is exactly why "I removed my handler but it still fires" happens: the handler removed was not the exact `Target/Method` pair that was added — typically a lambda that was re-created, or an instance method vs static, or a different method-group capture. The reliable discipline is to hold the event-handling delegate in a field and pair `+= handler` with `-= handler` using that same field.

The operator view worth internalizing: `+`/`-` on delegates are the multicast combinators and they return *new* delegates — chains are immutable, so `-=` produces a fresh list rather than mutating the old one in place. That immutability is what makes `?.Invoke`, snapshots, and `Interlocked` event patterns work without tearing, and it is also why unleashing `e += handler` inside an event's own add accessor infinite-recurses — you must touch the backing field, not the typed event. Design your subscriptions with the field cache in hand and delegate equality becomes predictable.

```csharp
static void A() { } static void B() { }

var ab1 = (Action)A + B;
var ab2 = (Action)A + B;
Console.WriteLine(ab1 == ab2);      // True — same targets, same order

var lambda1 = new Action(() => { });
var lambda2 = new Action(() => { });
Console.WriteLine(lambda1 == lambda2); // False — distinct generated methods

Action handler = A;
var chain = handler + handler + B;   // A, A, B
chain -= handler;                    // removes last A: now A, B
Console.WriteLine(chain.GetInvocationList().Length); // 2
```

## Q87: How do partial types and partial methods interact with source generators in the C# object model?

**A:** `partial` splits one type's declaration across multiple files (or regions within one file) that the compiler merges into a single type before any downstream tooling sees it. At runtime there is exactly one type — partiality is purely a compile-time organizational device. The feature matters most where generated code and hand-written code must coexist on the same type: the classic win-of-wins is a hand-written partial plus a generated partial, so the generator can own regenerable members while humans own behavior. The object model consequence: members, fields, inheritance (`: Base` appears once), and attributes all merge, and conflicting duplicates are the same errors as if written in one file.

`partial methods` are the fine-grained seam inside partiality. A partial method has a declaration and, optionally, an implementation elsewhere for the same type; if no implementation exists, the compiler silently erases all call sites — zero overhead, no "not implemented" stub, no signal. That is the enabling contract for generated code: a generator writes `partial void OnBeforeSave();` and the generator (or a human) may (or may not) implement it. Since C# 9 partial methods may be `void`-returning, `private`, and even `async` with the implementation supplying meaning — but they are still the switch "call sites that cost nothing when unturned".

Source generators lean on exactly these seams. A generator can inspect the hand-written partial for `[GenerateX]` attributes and emit the *other* partial half: DTO mapper methods, `INotifyPropertyChanged` plumbing, registry entries, `DispatchProxy` wrappers. You get compile-time metaprogramming without reflection's runtime tax, and the hand-written code always stays compile-time-checked against the generated half. The caution is namespace and file naming hygiene — generators emit into `obj/` gen folders with their own paths, so partial files most avoid collisions by purpose-generating only members the generator owns, and both halves must stay syntax-consistent for the merge, since a syntax error in either file breaks the whole type.

```csharp
// File A — hand-written half
public partial class Order
{
    public string OrderId { get; init; } = "";
    partial void OnValidate();                  // optional hook, erases if unimplemented
}

// File B — generator-emitted half (conceptual)
public partial class Order
{
    partial void OnValidate() => Console.WriteLine($"validating {OrderId}");
    // generator also provisions the source-generated serialization members here
}
```

## Q88: What is `IStructuralEquatable` and when is it preferable to overriding `Equals`?

**A:** `IStructuralEquatable` is a mid-level contract: the object implements it with an *explicit* `Equals(object, IEqualityComparer)` and `GetHashCode(IEqualityComparer)` pair, meaning equality and hashing are parameterized by a strategy rather than fixed behavior. Arrays and tuples implement it so that a caller can choose — via the passed `IEqualityComparer` — whether two collections are equal element-wise, according to a custom projection, or just by identity. It exists to solve the "same shape, different meaning" problem that a single hardcoded `object.Equals` override cannot express.

The decision point versus overriding `Equals` is a question of *whose* equality. If the type's own intrinsic equality is "compare all my fields" and that is stable, override `Equals`/`GetHashCode` and let everyone default to it. If the *caller* decides the comparison strategy — compare only a key, compare case-insensitively transposed, compare after projection — `IStructuralEquatable` is the right surface, because it keeps opinion out of the type. The classic example: a `Dictionary<string[], string>` keyed by arrays, where the array of strings should be equal by *content*, not reference; the array itself cannot sensibly override `Equals` (too many consumers with different notions), so the caller passes a structural comparer.

`.NET also ships `StructuralComparisons.StructuralEqualityComparer` as the out-of-the-box structural comparer, and tuples use it when they compare structurally. The honest guidance: leaf value types with stable, obvious equality get `Equals`/`==`; collections and container roles that must be compared *as wholes* by policy get structural interfaces; and anything else has `ReferenceEquals` semantics with a documented `IEqualityComparer<T>` to install at the consuming site. Overriding `Equals` on an array-like or dictionary-like type without thinking about consumers is exactly the design error this interface is there to rescue.

```csharp
string[] a = { "ada", "grace" };
string[] b = { "ada", "grace" };

Console.WriteLine(ReferenceEquals(a, b));                  // False — identity
Console.WriteLine(a == b);                                 // False — reference comparison

var structEq = StructuralComparisons.StructuralEqualityComparer;
Console.WriteLine(structEq.Equals(a, b));                  // True — element-wise
Console.WriteLine(structEq.GetHashCode(a) == structEq.GetHashCode(b)); // True
```

## Q89: How do `sealed` classes and `sealed` overrides benefit JIT devirtualization in C#?

**A:** The JIT devirtualizes — replaces a virtual/interface call with a direct call — when it can prove the runtime type is known. For a `sealed` class, there are no subclasses, so a call to its virtual methods dispatches deterministically; the JIT knows the target and emits a direct call, often followed by inlining. The same logic applies to `sealed` on individual overrides: `public sealed override string ToString()` seals that slot for the rest of the hierarchy. Each devirtualized call skips the vtable lookup (and, for inherited, the extra guard), and inlining the body then removes the call entirely — both measurable in hot, CPU-bound code.

The coupling of this to interfaces is important: an interface-typed call on a `sealed` concrete variable can, under favorable shapes, be devirtualized too, but guarded devirtualization is what the JIT falls back on when it cannot guarantee the exact shape — a fast path check plus a fallback. Sealing tightens the guard to nothing. This is a leading reason the BCL sealed many types (`Dictionary<TKey,TValue>`, `StringBuilder`) for both correctness and speed, and why performance-sensitive libraries aggressively seal concrete implementations.

The trade-off is the classic design-tax: sealing forbids extension, mocks, and `sealed`-overrides, so sealing a public API type that consumers need to inherit is hostile to ecosystem growth. The balanced stance: seal internal/hot leaf types freely, seal public types when extension is a liability (immutable types, core numerics, finalized patterns), and keep extension through interfaces/DI open even when the class is sealed. When you see a profiling spike on a virtual call that never has subtype, sealing is often the clean fix; when you see a `sealed` keyword on a type that "should" be extensible, that's a product decision, not an optimizer's.

```csharp
public sealed class CircularCounter   // sealed: no subclasses, direct dispatches
{
    private readonly int _max;
    public int Value { get; private set; }

    public void Next() => Value = (Value + 1) % _max;  // inlined in hot loops after devirtualization
    public override sealed string ToString() => Value.ToString();
}
```

## Q90: How does interface casting force boxing in non-generic collections, and how do generics solve it?

**A:** A non-generic collection such as `ArrayList` stores `object` elements and offers `IList`, `IEnumerable`, `IComparable`-style interfaces over its contents. Storing a value type anywhere in that line forces boxing — the struct is copied onto the heap into a box so the collection's reference storage can point at it. Reading triggers unboxing (a copy back), and interface-typed operations (`IEnumerator.MoveNext`, `IComparable.CompareTo`) go through the box too, so every element in a non-generic collection of value types pays multiple heap allocations and copies. The old `ArrayList` of `int` was effectively a little performance and GC disaster, which is precisely why `List<T>` and the generic comparer types emerged.

The fix is generics: `List<T>` stores `T` directly in an underlying `T[]`, so `List<int>` holds a true `int[]` with zero boxing per element, and `List<S?> ` stanceless. The `foreach` enumerator on `List<T>` is a struct (`List<T>.Enumerator`), so iteration adds no allocation and `MoveNext`/`Current` are value-safe. Generic versions of equality (`IEqualityComparer<T>`), comparison (`IComparer<T>`), and arithmetic (C# 11 static abstracts) complete the story — all constrained calls dispatch to the value type's implementation without ever allocating a box.

The senior nuance is that generics eliminate boxing *for the constrained path*; reach for an interface or `object` casting explicitly (`(IConvertible)x`, `(object)num`) and the box returns, because the interface reference itself is the heap object. Similarly, `IEnumerable<T>` over a `List<T>` is a read-only wrapper — fine during a loop, but storing it as an instance field pins the whole list; nothing is boxed, but life is a heap of references. The design rule: default to generic containers, pass them by generic interface when delegation is the point, and reserve non-generic surfaces for interop with old BCL APIs and heterogeneous mixed data — never for holding value types you care about.

```csharp
var legacy = new ArrayList();
legacy.Add(42);              // boxes: 42 copied into a heap box
int n = (int)legacy[0];      // unboxes: copy back

var modern = new List<int>();
modern.Add(42);              // stored inline in an int[] — no box
foreach (var v in modern)    // struct enumerator, zero allocation
    Console.WriteLine(v);

// generic equality keeps the struct unboxed during lookups too
var set = new HashSet<int>(modern);
Console.WriteLine(set.Contains(42)); // bool probe, no box anywhere
```

## Q91: How do static constructors and the `beforefieldinit` flag affect type initialization in the C# object model?

**A:** A static constructor (`.cctor`) runs exactly once per app domain the first time the type is *used* — before any static member access or instance creation — and the runtime locks the type during its execution so initialization is invisible, single-threaded, and re-entrant-safe. Its counterpart is `beforefieldinit`: a type that has only static field initializers and no explicit static constructor gets the flag, and the CLR reserves the right to init such types *earlier* than the first touch — whenever it is convenient (at assembly load, at JIT-compile of a caller). Observable behavior: explicit `.cctor` makes initialization lazy and guaranteed-before-first-use; flagged types may initialize ahead of need.

Because timing differs, the implications spread into autoloading: explicit static constructors guarantee observations like "constructor side effects happen once, on first access"; `beforefieldinit` can fire in a different thread, at a different moment, with innocuous-but-surprising ordering to side effects (a `Debug.WriteLine` in static field init could appear before the first touch). Circular dependencies between two types with static constructors can also deadlock or, in pathological cases, produce "null when you expect a value" because the runtime guarantees run once, not that ordering among cycles is defined.

`static readonly` fields and `Lazy<T>` use this machinery; and `Lazy<T>` with `ExecutionAndPublication` is the modern replacement giving control over exactly-once semantics plus thread-safety policy. The senior habit: keep static initialization side-effect-free, prefer `static readonly`/`Lazy<T>` over explicit static constructors for everything except where exact-timing matters, and never initialize heavyweight or I/O-bound state in a static constructor (it runs on the first user thread and can stall that thread). Type-init timing is part of the *contract* of the object model — treat it with the same respect you give disposal.

```csharp
// explicit static constructor: guaranteed once, lazily, at first touch
class Config
{
    static Config()
    {
        Console.WriteLine("Config static ctor runs exactly once, at first use");
        Values = LoadExternal();
    }
    public static Settings Values;
}

// static readonly field — beforefieldinit may init eagerly at JIT time
class FastPath
{
    public static readonly int Answer = 42; // could init before first access
}
```

## Q92: How do immutable types (records, readonly structs, `init` setters) interact with interface contracts for mutation?

**A:** Immutability is enforced at the *type* level, but interfaces describe capabilities, not guarantees — so a `readonly struct` or a `record` that exposes an interface with mutating members (like `IDictionary<K,V>` or an interface with settable properties) inherits a mismatch: the interface *invites* mutation the concrete type forbids. Records, for instance, produce setter-free property members, but `record` fields accessed through `IPropertyWithSet` can still compile if you implement the interface explicitly and throw on the setter — which is the classic Failure to Comply, detectable only at runtime (`NotSupportedException` on an interface-behaving call), breaking LSP in exactly the corner where the consumer holds the interface reference.

The design answer is to match the interface to the guarantee: expose read-only surfaces for immutable types (`IReadOnlyList<T>`, `IReadOnlyDictionary<K,V>`, `IReadOnlySet<T>`), and let mutable variants implement the writable contracts separately. `init`-only setters are a nice middle: the type is externally immutable after construction, yet the object initializer can set properties, so records and `init` types give you construction-time mutation through the same interface the type declares — the "build once, freeze later" trait. `with` expressions and copy-constructors express mutation *as* new values instead, keeping the contract honest.

The deeper design question immutable types force is mutation *by reference*. An immutable list in a field that points to a *mutable* concrete list is only shallowly immutable — defensive copies and arrays to `ReadOnly*` wrappers (which throw on writes) are how .NET keeps the facade. And `struct` immutability only holds if every member is immutable and equals is by value — a `readonly struct` holding a mutable class field loses the guarantee. So audit immutability at the *mutation escape points*, not the keyword: interfaces are the widest escape hatch, followed by reference-typed members and explicit-implementation setters that might confuse callers.

```csharp
// Immutable record implementing a read-only contract honestly
public interface IPriceView { decimal Total { get; } IReadOnlyList<decimal> Lines { get; } }

public record Invoice(decimal TaxRate) : IPriceView
{
    private readonly List<decimal> _lines = new();
    public decimal Total { get; }
    public IReadOnlyList<decimal> Lines => _lines; // read-only surface over mutable storage

    public Invoice AddLine(decimal amount) =>
        this with { /* record copy with recalculated Total */ };
}
```

## Q93: When a class implements an interface and a default interface member exists, who wins?

**A:** The precedence is deliberate: an explicitly declared *implicit* class member beats the interface default. If the class has any visible implementation (`public void Save()`), that body is used for interface calls too; the default member in the interface is merely a fallback for types that did not supply their own. Re-abstraction in an interface (`IStore.NewThing { abstract ... }` via C# 8 `abstract` default) shifts the burden back to implementers. So "who wins" is answered by the ladder: implicit class member first, then the most-derived interface default, with equal-rank interface conflicts forced to an explicit implementation.

The subtle case is when a class *explicitly* implements the interface and also defines a same-signature public member. `((IStore)x).Save()` then picks the explicit implementation while `x.Save()` picks the class member — two different behaviors, both legitimate reflections of intent. Regular implicit members remove this split by being both. Where multiple interfaces contribute a default for the same signature, the interface that is "closest" in the deriving chain wins; two siblings at equal distance force you to implement explicitly — the compiler refuses to guess.

The danger this creates is dispatch surprise in libraries. Pre-C# 8, interface members had no body, so adding a method to an interface broke every implementer at compile time; with DIM, an implementer that *ignored* the new member silently inherits the default — which may be `throw new NotSupportedException()`. A caller holding the interface expects canonical behavior and gets a stub. The senior rule: when relying on defaults, document the default as *the* contract priority, keep defaults truthful (never silently no-op a needed capability), and use re-abstraction for contract-shape changes. If you need the *class* to always win, provide the implicit member — do not depend on default fallbacks for behavior you centralize.

```csharp
interface IStore
{
    byte[] Read(string key);
    void Write(string key, byte[] value) => throw new NotSupportedException("default stub");
}

class ModernStore : IStore
{
    public byte[] Read(string key) => new byte[0];
    public void Write(string key, byte[] value) { /* class member wins over default */ }
}

class ShyStore : IStore
{
    public byte[] Read(string key) => new byte[0];
    // Write not implemented → harness default silently
}
```

## Q94: How do the factory method and abstract factory patterns use interfaces and delegates in C#?

**A:** The factory method pattern localizes construction in an abstract method that a derived class overrides — `protected abstract IProduct CreateProduct();` — so subclassing decides which product to build, and callers depend only on the product interface. The abstract factory pattern pushes the decision up a level: an interface of factory methods (`ICarFactory { IEngine MakeEngine(); IWheels MakeWheels(); }`) with families of implementations (e.g., `SportsFactory`, `EcoFactory`) guarantees matched products to its consumers. Both patterns' essence is the same — defer *which concrete type* until runtime — but factory method defers via inheritance, abstract factory via a dedicated creator abstraction.

C# collapses much of this machinery onto delegates. `Func<IProduct>` and `Func<TArgs, IProduct>` are factories in the smallest possible form: `Func<IEngine> engineFactory = () => new FourCylinder(displacement);` and passing factories around lets you swap construction policy without inheritance or an extra interface. A `Dictionary<string, Func<IProduct>>` registry becomes a mini-abstract-factory: `new Composition("sports")` resolves to a `SportsBundle()` at runtime in one line. This is the modern sweet spot: the factory is just a function value, injectable, mockable, and serializable where you need it.

Where the interface shapes still win is *family consistency and configuration*. A delegate cannot express "if you ask for wheels here, the matching engine family must be produced" — only a typed abstract factory family can lock boxing of part relationships. Also, `.NET's `Activator`/`CreateInstance` and generic factories (`.Create<T>() where T : new()`), plus DI containers acting as a global abstract factory, often eliminate hand-rolled factories entirely. The decision rubric: a single product → factory method or `Func<>`; a family → abstract factory interface; a runtime-wired global registry → DI container. Favor the smallest shape that preserves the coupling you actually need to break.

```csharp
// factory method: derived classes decide the product
abstract class ReportBuilder
{
    public IReport Build() => Compose(CreateHead(), CreateBody());
    protected abstract IReportSection CreateHead();
    protected abstract IReportSection CreateBody();
}

// modern: delegates are factories too
Func<int, IReport> reportFactory = pages => new PdfReport(pages);
printHeadOffice.Report(reportFactory(42));

// registry: dictionary-of-factories behaves like an abstract factory
var gateways = new Dictionary<string, Func<IPaymentGateway>>
{
    ["card"] = () => new CardGateway(),
    ["crypto"] = () => new CryptoGateway(),
};
var gw = gateways[request.Method]();
```

## Q95: Why can passing callbacks as delegate parameters indicate a design smell, and when are callback parameters appropriate?

**A:** A callback parameter (`void Download(Func<byte[]> onDone)`) is legal C# and occasionally the right shape, but heavy callback-parameter APIs are a smell because they scatter control flow: what would be a compositional return value becomes a chain of invocations at the call site, each callback tearing the business logic into separate anonymous blocks that are hard to trace, test, or reuse. Every callback hides sequencing, and sequencing is the hardest thing to get right. When callbacks nest (callback injecting a callback), you have created what OO code historically used state machines and orchestrators to avoid: temporally coupled spaghetti.

The smell detector: if *every* method must take a callback to operate, the API has inverted the control flow for a reason unrelated to the domain — usually circumventing exception handling, masking `Task`-based composition, or hiding an event subscription that should be expressed on the type (an event behind a method parameter makes subscriber/receiver lose identity and history). When the action genuinely is "occur at the end of *this* call", that is return-value territory; when it is "occur later, possibly many times", that is an event/`IObservable<T>`; when it is "occur once and produce the ultimate result", that is `Task<T>` — backpressure-correct, exception-correct, composition-correct.

The callbacks that earn their place are *local, specific strategies*: a `Comparison<T>` delegate for a sort (an algorithm parameter, not a control-flow hook), a `Func<T, bool>` predicate steering a filtering pipeline, an `onProgress` reporting channel that is genuinely independent of the returned result. These are directional strategy slots, not inverted flow. The guideline: a callback parameter belongs when it changes *how* a unit of work behaves (strategy), not *when* results arrive. If you find yourself writing `void`-returning async choreography through callbacks, you have reinvented `Task` badly — convert to `async`/`await` and let the compiler do what the callbacks were failing to do silently.

```csharp
// Smell: callback-parameter inversion hiding sequencing
void Upload(Pipeline pipe, Action<byte[]> onFs, Action onDone) { ... }

// Right shape: strategy callbacks (behavior knobs) …
void Sort<T>(List<T> values, Comparison<T> compare) { ... }

// … versus Task-based future (return value, exceptions, continuation contract)
Task<byte[]> UploadAsync(Pipeline pipe) { ... }
var bytes = await UploadAsync(pipe);   // sequenced, composable, awaitable
```

## Q96: How does C# enforce Liskov's substitution principle at compile time, and what are the runtime pitfalls?

**A:** Compile time, C# enforces the *shape* half of LSP: an override must match the base member's signature, may only narrow (`covariant returns` from C# 9 allow overriding to return a subtype), cannot weaken access (`protected` → `public` is fine, `public` → `protected` is a compile error), and `override` cannot change `abstract`/`virtual` intent. Generic covariance/contravariance is checked at declaration (`IEnumerable<out T>`), and interface implementation requires full signature conformance. That machinery proves substituability of *contract shape*; it cannot prove *behavioral* compliance — no compiler proves a derived class honors the base's documented preconditions/postconditions, re-entrancy, or thread-safety assumptions.

The pitfalls are runtime-resident. A derived type that throws `NotSupportedException` from a member the base contract specifies valid — a violation LSP cannot catch — will be found by consumers that relied on the base contract. Similarly, a derived type that "strengthens preconditions" (works only when the input happens to be shaped one way the base tolerated) compiles fine and fails late. And self-calls: a base method calling `virtual` internally dispatches to the derived override mid-algorithm, a scenario no static checker resolves — the derived override silently changes the base's algorithm. Nothing compiles a *test suite* into the type system.

The engineering response is discipline, not tooling: make contract assumptions explicit (`[Pure]`, annotations, documented preconditions), keep behavioral variations minimal when substituting, and lean on tests that exercise the base contract against every subtype — the LSP "substitutability test" is the honest enforcer. Design for it: avoid `is`/`as` downcasts and `NotImplementedException` pockets in hierarchies, prefer segregating interfaces so each subtype only implements what it honors, and treat "the base type is a lie for some descendants" as a design smell — substitute only where substitution is genuinely safe. In practice, `sealed` definitions of the substitutable surface (or interfaces over sealed types) make it *physically* impossible to violate.

```csharp
abstract class Animal { public abstract void Speak(); }
class Dog : Animal
{
    public override void Speak() => Console.WriteLine("woof");
    // Shape conformance is compile-time; speaking behavior is not provable.
}

// Runtime pitfall the compiler will not catch:
class BrokenDog : Animal
{
    public override void Speak() => throw new NotSupportedException("can't bark yet");
    // Compiles fine. Violates LSP the moment a consumer treats the base as its contract.
}
```

## Q97: How do SOLID principles map to specific C# mechanics?

**A:** Single Responsibility expresses itself as one class holding one reason to change, and C# gives it teeth through *accessibility signals* — internal implementation details (`private`/`internal`), and the discipline of composition: a `CheckoutService` orchestrates `IInventory`, `IPricing`, `IMailer` rather than doing all three. The SRP failure in C# is the "kitchen-sink static class" and the 800-line God object; refactors typically extract collaborators behind interfaces. Open/Closed prefers extension over modification: interfaces + strategy + decorators let you add behavior (a new `ITransactionValidator`, a caching decorator) without editing existing classes; `sealed` + `virtual` design choices decide whether extension is free or must go through composition.

Liskov is the contract between `virtual`/`interface` members and their consumers — C# provides `override` conformance checking but relies on you to keep behavioral contracts when substituting (Q96). Interface Segregation is mechanically loud: ISP violations appear as `NotImplementedException`-bearing fat interfaces; C# supports the remedy via small interfaces, explicit interface members, and `IReadOnly*`/`IEnumerable<T>`-style minimal surfaces. Dependency Inversion is the purest structural mapping — constructors taking interfaces + a composition root (DI container) means high-level policy depends on abstractions, and `Func<T>`-injected factories or `IServiceCollection` registrations complete the wiring.

The meta-lesson: SOLID isn't five rules C# gives you, it's five *directions* the language already biases you. C# tilts toward interfaces (nominal but cheap), composition (properties/delegates over inheritance), and registration (DI/`IConfiguration`). Each principle usually reduces to a concrete decision: "will adding behavior need an edit here (OCP fail)?"; "does this catch site trust the base contract (LSP)?"; "does this interface serve exactly one caller need (ISP)?"; "does high-level code name a concrete class (DIP)?" When the answer is uncomfortable, the mapping tells you which C# mechanic to introduce.

```csharp
// DIP: policy depends on abstractions, wiring lives at the composition root
public class OrderFlows
{
    public OrderFlows(IOrderStore store, INotifier notifier, ITaxer taxer) { }
    // high-level flow knows interfaces, never SqlOrderStore/EmailNotifier directly
}

// OCP via strategy interface: new validators never touch the core
public interface IOrderValidator { OrderError? Validate(Order o); }
public sealed class OrderService
{
    public OrderService(IEnumerable<IOrderValidator> validators) { ... }
}
```

## Q98: How does `INotifyPropertyChanged` and data binding use delegates and interfaces to build observable UI models?

**A:** `INotifyPropertyChanged` is a one-member interface — `event PropertyChangedEventHandler? PropertyChanged` — whose contract is "this object announces property changes by name". The `PropertyChangedEventArgs` carries the property name; subscribers (usually XAML/WinForms bindings, but also domain listeners) re-read the property in response. Because it is an *event*, .NET delivers via multicast delegates, and because bindings subscribe once, the interface is the entire glue between a plain CLR object and updating UI surface. UI frameworks implement bindings as delegates subscribing to the event and routing changes to the right control property on the UI thread.

The idiomatic C# implementation leans on the `CallerMemberName` attribute: a single `Set<T>(ref T field, T value, [CallerMemberName] string? name = null)` helper raises the event with the *caller's* property name, so property setters are one-liners and no literal strings (and their typo drift) survive. Threading is the classic trap: the event is raised from whatever thread a property was set on, so background mutations arrive on a non-UI thread; mature models marshal to the dispatcher (via a `SynchronizationContext` or `Dispatcher`) before raising, keeping the UI consistent.

Modern C# then offers faster, allocation-conscious paths: `[CallerArgumentExpression]` vetting, `System.ComponentModel` annotations, and open delegates. But the deeper model stays the same — change *events* over change *notification-of-results*, with the interface as the stable seam. The senior design cautions: raising with the right, empty-string name to signal "everything changed"; raising on each property even when sub-objects change (CompositeUI needs manual re-raise); and never letting bindings hold strong references to long-lived models where memory leaks accrue. `INotifyPropertyChanged` is the textbook "interface that carries a communication protocol", and delegating the notification is the whole trick.

```csharp
public class CartView : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    private decimal _total;
    public decimal Total
    {
        get => _total;
        set { if (_total != value) { _total = value; OnChanged(); } }
    }

    private void OnChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}

// binding subscribes to the event; the value flows back on the UI thread
foreach (var prop in new[] { nameof(CartView.Total) })
    view.PropertyChanged += (s, e) => { if (e.PropertyName == prop) UpdateField(prop); };
```

## Q99: What is the difference between shallow and deep copying, and how does `MemberwiseClone` fit into the object model?

**A:** A shallow copy duplicates the object and carries its reference-typed fields as *the same references* — the objects pointed to are shared. A deep copy recursively duplicates the whole reachable graph, so no two copies share mutable internals. The distinction is binary but the consequences are severe: shallow copies of an aggregate whose internals mutate are aliases in disguise — `CopyOfCart` and `OriginalCart` mutate together through the same item list, and the "copy" is a footgun, not a snapshot. Deep copies isolate state at the cost of traversal (cycles, singleton internals, identity assumptions).

`MemberwiseClone` (protected on `object`) is the runtime's free shallow copier: it copies field-by-field, including references, in one allocation. It is a *tool*, not a *pattern* — its protected status keeps it out of the public surface, and its shallow behavior means you must decide whether referencing-shared is acceptable before using it. .NET itself treats it as the building block: records reposition this under the hood for their copy semantics, and `ConditionalWeakTable`-style code uses it to build lightweight snapshot utilities. Deep copies have no built-in primitive — serialization (JSON/binary round-trip) is the common cheat, trading correctness for cost and ignoring `[JsonIgnore]` semantics tuned for transfer, not cloning.

The strong guidance: deep copy is almost never the right *default* contract for a public API. Most designs benefit from immutable constituents (copies share safely), copy-constructors expressing intent (typed, shallow or deep as documented), or `with`-expression record semantics for value-type-shaped objects. Reserve `MemberwiseClone` for internal mechanics — snapshots, undo caches, prototype probes — never expose "clone" as void-returning deep unknown. Document when you reimlement `ICloneable` (Q61) that you supply both semantics clearly, since an undocumented clone is worse than none.

```csharp
sealed class CartItem
{
    public int Count;
    public string Sku = "";
    public CartItem Shallow() => (CartItem)MemberwiseClone(); // shares Sku string & values
}

var a = new CartItem { Count = 1, Sku = "A" };
var b = a.Shallow();          // new object, same Sku reference
b.Count = 10;                 // b and a diverge (Count is a value field)
Console.WriteLine(a.Count);   // 1 — values copied, not shared

var items = new List<CartItem>{ a, b };   // deep copy here needs per-node recursion
```

## Q100: How do you refactor a deep inheritance hierarchy toward composition and interfaces in C#?

**A:** Start by observing the hierarchy through the lens of what each level *means*: a "metalab" `BaseThing` with `virtual` steps, specialty overrides, and subclasses that override three methods each is a template-method tree ripe for flattening. Extract the varying behaviors as interfaces — `IValidation`, `IBuildReport`, `IConnectSource` — and give each original subclass its implementation of those contracts *composed* into one workflow class. The refactor is safe when the tree's contract is a skeleton plus hooks (Q70): the skeleton moves to the orchestrator, the hooks become injected strategies.

Mechanically, the refactor is rewrite-in-place: introduce interfaces for each role a subclass plays, replace subclass extensions of base-vir localization with interface injections, and collapse the inheritance diamond of "base + one spike of specialization per subclass" into one class owning collaborators. Handlers through decorators (Q63) and DI (Q69) replace the `Base`-derived variations at the composition root, so behavior variety becomes *configuration* rather than class proliferation. Watch object initialization order and virtual self-calls (Q76): they are the silent coupling points that make the extraction hairy, so document them and test the refactored graph at each extraction step.

The payoff you're buying: LSP-safe substitution (the base contract stops being a promise subclasses quietly break), OCP-compliant extension (a new behavior = a new `ITransformer`, not a new subclass), and testability (compose a `Transformer` with fakes per collaborator). Keep one caution in view — interfaces replace *inheritance of behavior*, but shared state still needs ownership; give each collaborator its own storage instead of inheriting protected fields, which is often the true motivation for the whole refactor. When the tree still has a deepest-natural base (say, a `PaymentProcessor` with real shared plumbing), keep *that* base sealed-shaped and let the rest hang off interfaces rather than subclasses.

```csharp
// Before: subclass-per-flavor deep tree
class OrderProcessor { public virtual void ReleaseLock() { } }
class InventoryAwareProcessor : OrderProcessor { protected override void ReleaseLock() => ...; }

// After: behavior behind interfaces, injected, composed
interface ILockService { void Release(); }
sealed class OrderProcessor2
{
    public OrderProcessor2(ILockService locks, IStockChecker stock, INotifier notifier) { }
}

// a "new flavor" is now a new set of collaborators, not a new subclass
var v = new OrderProcessor2(new RedisLock(), new RealStock(), new EmailNotifier());
```
