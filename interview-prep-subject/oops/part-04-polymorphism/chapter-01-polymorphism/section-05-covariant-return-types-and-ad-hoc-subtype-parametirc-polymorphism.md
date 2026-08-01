# Covariant Return Types and Ad-Hoc, Subtype, Parametric Polymorphism

> **TL;DR**: Covariant return types let an override narrow the return type of an inherited method (Java/C++), tightening the contract per subtype; the three polymorphism kinds — ad-hoc (overloading), subtype (inheritance/overriding), parametric (generics/templates) — answer different "one name, many forms" questions and are often combined.

## 1. Why Does This Exist?
An override must be **substitutable** for its base (LSP): a caller that treats a `Dog` as an `Animal` and calls `getAnimal()` must still get something it can use as an `Animal`. But a *specific* caller that knows it has a `Dog` wants `getDog()`. Covariant return types give both: the base declares `Animal getAnimal()`, the override declares `Dog getAnimal()`, and each caller sees exactly what it needs — the *narrowing* stays within the contract, so nothing breaks. The three-way polymorphism taxonomy exists because real code has three different "forms" to resolve: overloading (same name, different signatures — ad-hoc), inheritance (one signature, many type-specific implementations — subtype), and generics/templates (one implementation, many types — parametric). Understanding which one you're using is how you predict whether resolution is compile-time or runtime.

## 2. How Does It Work?
```java
class Animal { Animal clone() { ... } }                 // base return type
class Dog extends Animal { @Override Dog clone() { ... } }  // covariant: Dog is-a Animal
Dog d = new Dog().clone();       // specific caller gets Dog — no cast
Animal a = new Dog().clone();    // general caller gets Animal — still valid
```
- The override's return type may be a **subtype** of the base's return type (covariance).
- Java: allowed for reference types since Java 5 (generics era); C++ allows it since C++11 (via return-type covariance). Contravariant parameter types are *not* allowed in Java/C++ (only Scala supports that) — signatures must match exactly.
- **Ad-hoc**: `print(int)`, `print(String)`, `print(double)` — same name, different signatures, chosen at compile time.
- **Subtype**: `Animal.speak()` overridden by `Dog.speak()` — runtime dispatch.
- **Parametric**: `List<E>`, `T max(T,T)`, C++ templates — one definition works for many types, checked per instantiation.

## 3. When Is It Used?
- **Covariant returns**: fluent builders (`Order withItems(...)` returning `Order`/`Builder` subtypes), `clone()`, factories, `Comparator.thenComparing` chains, domain-specific getters.
- **Ad-hoc**: operator/utility overloading — `sum(int,int)`, `sum(double,double)`, `toString()`, `printf`, `+` operators, comparator helpers.
- **Subtype**: all interface programming — callbacks, DI, strategy, framework hooks.
- **Parametric**: collections, algorithms (`sort`, `binarySearch`), `Optional<T>`, monads, generic repositories, C++ STL algorithms.
- Combined constantly: `List<Shape>` (parametric) holding `Circle`/`Square` (subtype) whose `area()` (ad-hoc via overridden override) returns covariant types.

## 4. Why Wasn't Another Approach Chosen?
- *Why covariant returns instead of casting at call sites?* Casting is unsafe (`ClassCastException`) and noisy; covariance encodes the narrowing in the type system so the compiler guarantees safety.
- *Why not contravariant parameters too?* Java/C++ chose simplicity: requiring exact signature matches for overriding keeps dispatch sound with the vtable slot model; contravariance complicates overload resolution. Scala's choice shows it's possible but it's the exception.
- *Why have ad-hoc at all if parametric exists?* Ad-hoc specializes behavior per type (`+` for numbers vs strings), while parametric generalizes structure over types — they solve orthogonal problems and C++ merges them with templates + overloading.
- *Why not just one "polymorphism"?* The runtime vs compile-time split is essential: subtype = runtime (flexible, slower), ad-hoc/parametric = compile-time (fast, less flexible). A single mechanism would force every call to be one or the other, sacrificing performance or extensibility.

## 5. Intuition
**Covariant returns**: ordering a "meal" and getting a "pizza" when you ordered from the pizza place — the base promises "some food", the specific branch promises "exactly the food you asked for". You *may* accept any food (base type); you'll *actually* receive pizza (narrowed type) — satisfying both the cautious and the picky diner.

**Three kinds of polymorphism**: a single word "party" — *ad-hoc*: it means different things to the caterer (food), the musician (gigs), and the host (guests), resolved by who says it (signature). *Subtype*: "let's party" executed differently by a student party (dorm) vs a company party (ballroom), chosen by the actual party planner (the object). *Parametric*: "bring a gift" works for birthdays, weddings, Diwali — one instruction, any gift-type, applied uniformly. Same word, three distinct mechanisms.

## 6. Real-World Analogy
**Covariant returns**: the airport check-in desk. The "airline counter" promises a boarding pass (base type). Flying Air India? The counter hands you specifically an Air India boarding pass (subtype) — still a boarding pass, but with extra fields (seat, terminal) your Air India app can read directly, no conversion needed.

**Ad-hoc / subtype / parametric**: a restaurant's "cook" command. *Ad-hoc*: the stove "cooks" gas, the microwave "cooks" electric, the pan "cooks" the food — different tools chosen by the medium (overload). *Subtype*: every chef "cooks the special", but the Italian chef makes pasta and the Indian chef makes curry — chosen by the actual chef (override). *Parametric*: "cook <ingredient>" — the oven's algorithm is identical whatever ingredient you slide in (template/generic).

## 7. Formal Definition
**Covariant return type**: an overriding method may declare a return type that is a subtype (reference type) of the base method's return type; the narrowing is legal because the override's behavior still satisfies the base contract (LSP-compatible). Java allows reference-type covariance (JLS §8.4.8.3); C++ since C++11. Parameter types must remain identical.
**Ad-hoc polymorphism**: the same operation name bound to multiple signatures, selected at compile time (overloading, operator overloading).
**Subtype polymorphism**: a single inherited signature dispatched at runtime to the dynamic type's implementation (overriding/virtual functions).
**Parametric polymorphism**: an operation or type parameterized over a type variable, instantiated per concrete type (Java/C# generics, C++ templates), enabling one definition to serve many types with compile-time type safety.

## 8. Example
```java
abstract class Animal { abstract Animal self(); }          // base return type
class Dog extends Animal {
    @Override public Dog self() { return this; }           // covariant return
    void bark() { System.out.println("woof"); }
}
class Cat extends Animal {
    @Override public Cat self() { return this; }
    void meow() { System.out.println("meow"); }
}
public class Main {
    public static void main(String[] args) {
        Dog d = new Dog().self();      // compile-time type: Dog — call bark() directly
        d.bark();
        Animal a = new Dog().self();   // base caller still fine
        System.out.println(a.getClass());   // class Dog
    }
}
```
Compare the three kinds in one place:
- Ad-hoc: `Math.max(1,2)`, `Math.max(1.0,2.0)` — same name, two signatures, compile-time.
- Subtype: `a.self()` — dispatch by dynamic type.
- Parametric: `List<Dog>`, `List<Cat>` — one class, many element types.

## 9. Internal Working
1. **Covariant returns**: the compiler requires the override's return type to be a subtype of the base's; both entries still occupy the same vtable slot (the return type isn't part of the JVM signature — the JVM method descriptor erases the return-type change; the JIT/verifier enforces assignability). Callers of the *base* type see `Animal`; callers of the *subclass* type see `Dog` — no casts emitted.
2. **Ad-hoc**: overload resolution is pure compile time — the compiler picks the most specific applicable signature (widening > boxing > varargs fallbacks) and emits a direct call; no runtime decision.
3. **Parametric (Java)**: generics erase to bounds at runtime (`List<Dog>` → `List`); the compiler inserts checked casts at use sites. C++ templates instantiate whole new functions per type (no erasure — full specialization, but binary bloat).
4. **Subtype**: runtime vtable dispatch (Section 04) — the only one with a runtime cost.
5. All four combine seamlessly: `List<? extends Animal>` (parametric + wildcard variance) can hold `Dog`s (subtype), calling `self()` (dispatch) returns covariant `Dog` (when statically typed as `Dog`).

## 10. Time Complexity
- Covariant returns: no added cost — same O(1) vtable dispatch; purely a compile-time type improvement.
- Ad-hoc: O(1) direct call (compile-time resolution).
- Subtype: O(1) vtable (devirtualized by JIT in practice).
- Parametric (Java): O(1), erased; (C++ templates): per-instantiation code, call O(1) but code-size bloat possible.

## 11. Advantages
- **Covariant returns**: type-safe narrowing without casts; fluent chaining works; caller sees precise types.
- **Ad-hoc**: readable, same-name operations; fast (compile-time).
- **Subtype**: extensible, open to new types, framework-ready.
- **Parametric**: reuse across types with full compile-time checking; type-safe collections.

## 12. Disadvantages
- **Covariant returns**: only reference types in Java (primitives like `int` can't be narrowed); not applicable to fields; can tempt leaky subtype APIs.
- **Ad-hoc**: signature explosion; accidental ambiguity in overload resolution; can't add behavior for types you don't own (Java lacks extension methods/operators for user types).
- **Subtype**: runtime indirection; fragile-base risk.
- **Parametric**: Java erasure means no runtime type info (no `new T()`, no `instanceof T`); C++ templates complicate compilation, error messages, and binary size.

## 13. Interview Questions
1. **Q: What is a covariant return type?** A: An override that narrows the inherited method's return type to a subtype — legal because it still satisfies the base contract; lets callers of the subclass avoid casting.
2. **Q: Which languages allow covariant returns?** A: Java (reference types, since 5.0) and C++ (since C++11); Scala goes further with contravariant parameters too; Java/C++ require exact parameter matches.
3. **Q: TRICKY — Can parameters be covariant (narrowed) too?** A: No in Java/C++ — a narrowed parameter creates an *overload*, not an override; only return types (and checked exceptions, Java) may vary. Contravariant params would need runtime overload selection.
4. **Q: What are the three kinds of polymorphism?** A: Ad-hoc (overloading, compile-time), subtype (overriding, runtime), parametric (generics/templates, compile-time). They solve name-resolution, behavior-specialization, and type-reuse respectively.
5. **Q: SCENARIO — `class Dog extends Animal { Animal clone() }` — valid override?** A: Yes — widening the return type is fine (a call expecting `Animal` still works). Covariant *narrowing* is the common, useful case; widening is allowed but pointless.
6. **Q: How does covariance interact with the vtable?** A: It doesn't change layout — override and base share the same slot; the return-type difference is erased at the JVM level (not part of the descriptor), enforced by assignability.
7. **Q: PRODUCTION — When do you actually rely on covariant returns in real code?** A: Fluent builders/DSLs (`class OrderBuilder { OrderBuilder withItem(...) }` overridden in `SpecialOrderBuilder`), typed `clone()`, typed factories, and `Comparators` chains — narrowing at each level without casts.
8. **Q: What's the difference between generic (parametric) and subtype polymorphism?** A: Parametric: one implementation instantiated per type at compile time (`List<Dog>`). Subtype: one signature, many runtime implementations dispatched dynamically (`Animal.speak()`). One is structural reuse, the other behavioral specialization.
9. **Q: TRICKY — Java erases generics; what does that cost?** A: No `new T()`, no `instanceof T`, no arrays of type parameters, and unchecked-cast warnings; the JVM sees only erased `List`/`Object` and the compiler inserts casts.
10. **Q: SCENARIO — Which kind of polymorphism is `Collections.sort(List<T>)`?** A: Primarily parametric (works for any `List<T>` of `Comparable<T>`), *plus* subtype polymorphism via `Comparable.compareTo` dispatch and ad-hoc via `Comparator` overloads — production code usually composes all three.
11. **Q: Why can't `int` be a covariant return in Java?** A: Covariance applies to reference types (subtype relation); primitives aren't subtypes of each other, so no narrowing is possible — only the exact primitive type matches.
12. **Q: PRODUCTION — Overload vs override confusion causing a bug?** A: Adding a method with a different parameter type in a subclass silently creates an overload; the base reference keeps calling the base method. `@Override` prevents the silent surprise.
13. **Q: What does "ad-hoc" literally imply?** A: The polymorphism is defined per-case ("for this signature, do this"), as opposed to subtype (inherited) or parametric (generic) — it's a family of unrelated definitions sharing a name.
14. **Q: TRICKY — Is operator overloading ad-hoc polymorphism in C++?** A: Yes — `+` for `int`, `string`, and user types is a set of overloads selected at compile time; C++'s templates then *parametric* over that, and virtual functions add the *subtype* dimension.

## 14. Follow-Up Questions
1. **Q: How does Scala's variance differ from Java's?** A: Scala allows declaration-site variance on generics (`+T` covariant, `-T` contravariant) and supports contravariant method parameters, whereas Java only has use-site wildcards (`? extends`) and no parameter contravariance.
2. **Q: What is the relationship between covariance and LSP?** A: Covariant returns *preserve* LSP — the override delivers at least what the base promised (a subtype of the promised type). Parameter contravariance would also preserve it, which is why it's the theoretically sound complement.
3. **Q: What about C#?** A: C# 4 added covariant/contravariant generic *interfaces* (`IEnumerable<out T>`, `Func<in T>`); method override covariance is not allowed — you get declaration-site variance instead.
4. **Q: Do generic methods give runtime polymorphism?** A: No — generics are compile-time; the runtime sees erased types. To get runtime behavior you pair generics with subtype polymorphism (e.g., `Comparable<T>`) or reflection/bridges.

## 15. Coding Example
```java
import java.util.*;
public class Covariance {
    static class Animal { Animal copy() { return new Animal(); } }
    static class Dog extends Animal {
        @Override public Dog copy() { return new Dog(); }        // covariant
        void bark() { System.out.println("woof"); }
    }
    static class Zoo {
        public <T extends Animal> T breed(T a) { return (T) a.copy(); }  // parametric + covariance via cast
    }
    public static void main(String[] args) {
        Zoo zoo = new Zoo();
        Dog d = zoo.breed(new Dog());        // parametric dispatch
        d.bark();                             // no cast needed
        List<Dog> dogs = List.of(new Dog(), new Dog());           // parametric
        Animal a = dogs.get(0).copy();        // subtype + covariant view
        System.out.println(a.getClass());
    }
}
```
```cpp
#include <iostream>
struct Animal { virtual Animal* clone() const { return new Animal(*this); } };
struct Dog : Animal {
    Dog* clone() const override { return new Dog(*this); }   // covariant since C++11
    void bark() const { std::cout << "woof\n"; }
};
int main() {
    Dog* d = (new Dog)->clone();   // static type Dog* — call bark directly
    d->bark();
    delete d;
}
```

## 16. Industry Usage
- **JDK**: `Object.clone()` is overridden covariantly by collection/stream classes; `Enum<E>`, `Optional<T>`, streams use parametric + subtype polymorphism constantly; `Collections.sort` pairs `List<T>` with `Comparable`/`Comparator`.
- **Guava / Google**: type-token patterns and `Supplier<T>`/`Function<A,B>` (parametric + subtype) are core; fluent builders lean on covariant returns.
- **C++ STL**: containers and algorithms are parametric (templates); `std::variant`, iterators, and smart pointers compose overloading (ad-hoc) with templates (parametric).
- **JDBC**: driver managers use subtype polymorphism (each driver overrides the same interface) and parametric for typed result extraction.
- **Spring**: generic `Repository<T, ID>` (parametric) backed by interface dispatch (subtype) — the standard composition in enterprise Java.

## 17. References
- JLS §8.4.5 (Method Return Type), §8.4.8.3 (Covariant returns): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- C++ Reference, "virtual function specifier" — covariant return rules (C++11+).
- Oracle Java Tutorials, "Overriding and Hiding Methods": https://docs.oracle.com/javase/tutorial/java/IandI/override.html
- GeeksForGeeks, "Covariant Return Type in Java": https://www.geeksforgeeks.org/covariant-return-type-java/
- Bjarne Stroustrup, *The C++ Programming Language* — templates (parametric), overloads (ad-hoc), virtuals (subtype).

## 18. Cheat Sheet
- Covariant return: override narrows return type (reference types, Java/C++11+).
- Parameters must match exactly in Java/C++ (no contravariance).
- Widening return: legal but pointless.
- Ad-hoc = overloading, compile-time.
- Subtype = overriding, runtime (vtable).
- Parametric = generics/templates, compile-time (Java erases).
- Java covariance: only reference types, no primitives.
- LSP-friendly: covariant returns preserve substitutability.

## 19. Quiz
1. Covariant returns allow narrowing of: a) parameters b) return type c) class d) package → **b**
2. Java covariance applies to: a) primitives b) reference types c) void d) arrays only → **b**
3. Overloading is which polymorphism? a) ad-hoc b) subtype c) parametric d) none → **a**
4. Overriding is which? a) ad-hoc b) subtype c) parametric d) none → **b**
5. Generics are which? a) ad-hoc b) subtype c) parametric d) none → **c**
6. True or False: Java allows contravariant parameters. → **False**

## 20. Flashcards
- **Q: Covariant return?** → **A:** Override narrows return type (reference types).
- **Q: Three polymorphism kinds?** → **A:** Ad-hoc (overload), subtype (override), parametric (generic).
- **Q: Which are runtime?** → **A:** Only subtype (vtable); ad-hoc and parametric are compile-time.
- **Q: Java covariant limitation?** → **A:** Reference types only; parameters must match.
- **Q: Purpose of covariance?** → **A:** Type-safe narrowing, no casts, fluent APIs.

## 21. Revision
Covariant returns let an override narrow its return type (Java reference types, C++11+), preserving LSP while giving subtype callers precise types — the tool behind typed `clone()` and fluent builders; parameters must match exactly (no contravariance in Java/C++). The taxonomy: ad-hoc (overloading, compile-time), subtype (overriding, runtime vtable), parametric (generics/templates, compile-time, Java erases). Real code composes all three — `Collections.sort(List<T>)` is parametric + subtype (`Comparable`) + ad-hoc (Comparator overloads). First-30-seconds answer: "Covariant returns narrow return types legally; ad-hoc = overloading, subtype = overriding, parametric = generics — only subtype is runtime."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a covariant return type?" | Interview Q1 / Section 2, 8 |
| "Can parameters be covariant?" | Interview Q3 / Section 4 |
| "Three kinds of polymorphism?" | Interview Q4 / Section 2, 7 |
| "Covariance + vtable interaction?" | Interview Q6 / Section 9 |
| "Generics erasure costs?" | Interview Q9 |
| "When to use covariant returns in production?" | Interview Q7 / Section 16 |
| "Overload vs override bug?" | Interview Q12 |
| "Operator overloading = ad-hoc?" | Interview Q14 |
