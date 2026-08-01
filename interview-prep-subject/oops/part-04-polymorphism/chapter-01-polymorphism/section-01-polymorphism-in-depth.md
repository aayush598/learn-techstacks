# Polymorphism in Depth

> **TL;DR**: Polymorphism ("many forms") is the property that lets one interface — one method name, one type, one operator — drive many different implementations, selected at compile time (overloading, generics) or at runtime (overriding/virtual dispatch).

## 1. Why Does This Exist?
Polymorphism exists because **behavior varies while interfaces stay stable**. Without it, every "do this thing" would need its own name and its own switch: `dogBark()`, `catMeow()`, `if (type == DOG) bark();` — and adding a new animal meant editing every switch. Polymorphism lets you call `animal.speak()` and let *the object* decide what "speak" means. The payoff is **Open-Closed**: add new behaviors (new subtypes) without modifying existing code. It also gives **uniform handling**: a `List<Shape>` of different shapes, `for(Shape s) sum += s.area();` — the loop never changes when new shapes arrive. Interviews probe polymorphism because it's the pillar that makes OOP *extensible* rather than just organized — and because the "which implementation runs?" question drills straight into overloading vs overriding vs dispatch internals.

## 2. How Does It Work?
Four mechanisms, two timings:
- **Ad-hoc (overloading)**: same method name, different parameter types — resolved at *compile time* by the argument types (`print(int)`, `print(String)`).
- **Parametric (generics/templates)**: one definition works for many types via type parameters (`List<T>`, `template<typename T>`); type-checked at compile time.
- **Subtype (inheritance/interface)**: a base reference holding a subclass object; the call dispatches *at runtime* to the object's implementation (`Animal a = new Dog(); a.speak()` → Dog's).
- **Coercion (implicit conversion)**: an argument is implicitly converted to another type (`print(3.14)` calling `print(double)` with an int 3).
- **Dynamic dispatch**: the *runtime object's type* (via vtable) selects the method — the core of subtype polymorphism.

## 3. When Is It Used?
- **Subtype polymorphism**: everywhere — `List<Shape>`, `List<Animal>`, listeners (`Runnable`, `Comparator`), strategy injection, framework hooks (`doGet`), DI.
- **Ad-hoc/overloading**: utility classes (`Math.min(int, int)`, `min(double, double)`), `String.valueOf(...)` overloads, constructors (overloaded by parameter sets).
- **Parametric**: `List<T>`, `Optional<T>`, `HashMap<K,V>`, C++ templates (`std::vector<T>`) — type-safe collections and algorithms.
- **Coercion**: numeric widening (`int → double`), `String` + anything, implicit type promotion.
- **Design patterns**: Strategy (interface polymorphism), Template Method (subtype override), Visitor (double dispatch), Factory (returns interface type).

## 4. Why Wasn't Another Approach Chosen?
- *Why not unique names for every behavior (`dogBark`, `catMeow`)?* Callers would need `switch`es everywhere and adding a type breaks every call site — violates Open-Closed. One name + dispatch chosen: new types extend, callers don't change.
- *Why not type-tag switches only (no polymorphism)?* The switch version duplicates logic, leaks all variants into one place, and must be updated for every new type; polymorphic dispatch localizes the change to the new class. Dispatch chosen.
- *Why not runtime-only (duck typing, no static checks)?* Python/JS dispatch at runtime without declared types — flexible, but errors surface at runtime, not compile time. Java/C++ chose *checked* polymorphism: the compiler knows the contract (the base/interface), the runtime picks the implementation — both safe and dynamic.
- *Why not compile-time-only (no vtables)?* Then you couldn't swap implementations at runtime (strategy, DI, plugins); static-only polymorphism (C++ templates) buys performance but loses runtime choice. Both coexist in modern languages.

## 5. Intuition
Think of **"Press the button."** The same instruction produces different outcomes depending on *which machine* you press it on: a button on a coffee machine makes coffee; a button on a doorbell rings a bell; a button on an elevator calls the car. The user never says "make coffee" or "ring bell" — they just *press the button*, and the machine (the object) decides what pressing means. Polymorphism is that: **one instruction, many machines, each interpreting it its own way.**

## 6. Real-World Analogy
A **"Make a sound" command** given to different performers: a violinist plays a note, a drummer hits a drum, a singer sings — each *implements* the command differently, but the conductor only needs one instruction. Even better: the conductor's score says "all instruments, play your part" — one line of the score works for any instrument; adding a new instrument (a new subclass) doesn't change the score. That's the extensibility polymorphism buys: the conductor (caller) never edits the score when a new instrument joins the orchestra.

## 7. Formal Definition
**Polymorphism** (Greek *polys* "many" + *morphē* "form") is the provision of a single interface to entities of different types, where the actual behavior is selected according to the concrete type involved. In OOP it appears in four forms: **ad-hoc polymorphism** (overloading — the same function name with different signatures, resolved statically), **parametric polymorphism** (generics/templates — a single definition parameterized over types, resolved statically), **subtype polymorphism** (inclusion polymorphism — a reference of a base/interface type referring to an object of a subtype, with methods resolved dynamically via the vtable), and **coercion polymorphism** (implicit type conversion). The two principal timing classes are **compile-time (static) binding** — overloading/generics — and **runtime (dynamic) binding** — virtual dispatch of overridden methods.

## 8. Example
```java
// SUBTYPE polymorphism (runtime): one call, many behaviors
public abstract class Animal { public abstract void speak(); }
public class Dog extends Animal { public void speak() { System.out.println("bark"); } }
public class Cat extends Animal { public void speak() { System.out.println("meow"); } }
public class RobotDog extends Animal { public void speak() { System.out.println("beep-bark"); } }

public class Main {
    public static void main(String[] args) {
        List<Animal> zoo = List.of(new Dog(), new Cat(), new RobotDog());
        for (Animal a : zoo) a.speak();     // one line; 3 behaviors; adding a new
        //                                        animal changes NOTHING here
    }
}
```
The loop's single `a.speak()` call produces "bark", "meow", "beep-bark" — each object *interprets* the message. Adding `Lion` tomorrow requires no edit to this loop (Open-Closed).

## 9. Internal Working
1. `Animal.speak` is abstract → every subclass must implement it; the class file records the abstract method.
2. `Dog`, `Cat`, `RobotDog` each provide `speak`; the JVM builds each class's vtable (method table) with `speak` pointing at its own code.
3. The loop compiles to `a.speak()` = "read `a`'s object header → klass pointer → vtable → jump to slot N."
4. At runtime, `a` is a `Dog` → vtable slot → `Dog.speak`; next iteration `a` is a `Cat` → different slot target. The *same* instruction, different targets — decided per object.
5. JIT optimization: if the loop sees one implementation repeatedly (monomorphic), it installs an inline cache (direct call); if many (megamorphic), it falls back to the table.
The entire loop is O(n) calls, each O(1) — polymorphism is free at scale.

## 10. Time Complexity
- Static binding (overload/generic): O(1) at compile time — zero runtime cost.
- Subtype dispatch: O(1) per call — one vtable indirection (JIT may devirtualize to a direct call, also O(1)).
- Megamorphic (many impls at one site): still O(1) — table lookup.
- No polymorphism form changes Big-O; subtype dispatch adds a constant indirection, usually optimized away.

## 11. Advantages
- **Open-Closed**: new subtypes without modifying callers.
- **Uniform handling**: one loop/API over heterogeneous objects.
- **Decoupling**: callers know the contract, not the concrete type.
- **Extensibility**: frameworks extend via hooks you override.
- **Testability**: mock/fake implementations substitute polymorphically.
- **Compile-time safety + runtime flexibility**: static contracts, dynamic behavior.

## 12. Disadvantages
- **Indirection**: vtable dispatch is slower than a direct call (usually negligible; breaks inlining).
- **Hides behavior**: which implementation runs isn't visible at the call site — harder tracing.
- **Over-abstraction risk**: polymorphism-for-its-own-sake (interface per class).
- **Subtype surprises**: if LSP is violated, polymorphic calls behave incorrectly.
- **Static forms limited**: overloading can't vary by return type; generics have their own constraints.

## 13. Interview Questions
1. **Q: What is polymorphism?** A: "Many forms" — the ability of one interface/name/operator to drive different implementations, resolved at compile time (overloading, generics) or runtime (overriding/virtual dispatch).
2. **Q: Name the types of polymorphism.** A: Ad-hoc (overloading), parametric (generics/templates), subtype (inheritance/interface overriding), and coercion (implicit conversion). Grouped as compile-time (ad-hoc, parametric, coercion) vs runtime (subtype).
3. **Q: TRICKY — Is overloading polymorphism?** A: Yes — ad-hoc polymorphism. It's the *same name* with different signatures, resolved at compile time. Many candidates wrongly say "only overriding is polymorphism."
4. **Q: How does polymorphism enable Open-Closed?** A: You write callers against a base/interface; adding a new subtype only requires implementing it — existing code (the loop, the switch) never changes. Extension happens by addition, not modification.
5. **Q: SCENARIO — Add `Lion` to the zoo with zero changes to existing code.** A: `class Lion extends Animal { public void speak() {...} }` — the `for(Animal a : zoo)` loop and all callers are unchanged; the vtable does the rest. That's subtype polymorphism in action.
6. **Q: What's the difference between static and dynamic binding?** A: Static binding (compile time): the compiler picks the method from declared types — overloading, generic instantiation; dynamic binding (runtime): the JVM/object picks via vtable — overriding. Same-name methods can mix both (e.g., overload resolved statically, then dispatched dynamically).
7. **Q: PRACTICAL — Why do collections (`List<Shape>`) need subtype polymorphism?** A: Because they must store *heterogeneous* shapes (Dog+Cat, Circle+Square) and treat them uniformly; each element keeps its runtime type, and `s.area()` dispatches to the right implementation per element.
8. **Q: TRICKY — "Polymorphism only matters in dynamically-typed languages."** A: Wrong — Java/C++ have *checked* polymorphism: the compiler enforces the contract statically while dispatch remains dynamic; that's *stronger* than duck typing (failures at compile time, not runtime).
9. **Q: When should you prefer parametric over subtype polymorphism?** A: When behavior is *type-parameterized but identical* (a `List<T>` is the same logic for any T — no per-type behavior); when behavior *varies per type*, subtype polymorphism (override) is right. The classic test: "does the algorithm change per type?" — yes→subtype, no→parametric.
10. **Q: PRODUCTION — Design a notification system polymorphically.** A: `interface Notifier { void send(String msg); }` + `EmailNotifier`, `SmsNotifier`, `PushNotifier`; the service holds `Notifier` and calls `send()` — adding Slack is one new class, zero changes to the service.
11. **Q: What does "many forms, one interface" mean concretely?** A: The *interface* (method signature / type) is fixed; the *forms* are the implementations behind it — `speak()` is one interface, "bark"/"meow"/"beep" are the forms.
12. **Q: TRICKY — Does `Animal a = new Dog();` change which `speak()` runs?** A: No — runtime dispatch uses the *object's* type (Dog), so `Dog.speak()` runs. Upcasting only widens the variable type; it never changes behavior. (Contrast with static/field hiding, which *do* follow the reference type.)
13. **Q: How do patterns use polymorphism?** A: Strategy = interface polymorphism (swap algorithms); Template Method = overriding hooks; Factory = return the interface; Visitor = double dispatch (two polymorphic steps). Every OOP pattern leans on one or more forms.
14. **Q: SCENARIO — A switch statement on a `type` field vs polymorphism — argue.** A: The switch must be updated everywhere a new type appears (violates Open-Closed) and duplicates type knowledge; polymorphism localizes the change to the new class and removes the switch. Refactor the switch into an overridden method.
15. **Q: Can you have polymorphism without inheritance?** A: Yes — interfaces (Java), structural typing (Go, `io.Reader`), duck typing (Python), and generics (parametric) all give polymorphism without class inheritance. Inheritance is one *mechanism*, not the definition.

## 14. Follow-Up Questions
1. **Q: What is double dispatch?** A: Two polymorphic decisions — the Visitor pattern: `element.accept(visitor)` dispatches by element type, then `visitor.visit(element)` dispatches by visitor type — a workaround for Java's single dispatch.
2. **Q: What is the difference between "polymorphism" and "overloading" in everyday Java?** A: Interviews use "polymorphism" for *subtype* (override) most of the time; overloading is technically ad-hoc polymorphism. Say "compile-time polymorphism (overloading)" vs "runtime polymorphism (overriding)" to be precise.
3. **Q: How does devirtualization affect polymorphic calls?** A: When the JIT sees one implementation at a call site (monomorphic inline cache), it replaces the vtable call with a direct call + inlining — polymorphic dispatch becomes as fast as a static call in the common case.
4. **Q: What is the relationship between polymorphism and LSP?** A: LSP is the *correctness rule* for subtype polymorphism: a subtype must be substitutable for its base without breaking callers — polymorphic calls only behave correctly if every subtype honors the base's contract.

## 15. Coding Example
```java
// One interface, many forms, fully working
public interface Pricing { double priceFor(int qty); }

public class FlatPricing  implements Pricing { public double priceFor(int qty) { return 10.0 * qty; } }
public class BulkPricing  implements Pricing { public double priceFor(int qty) { return qty > 10 ? 8.0 * qty : 10.0 * qty; } }
public class SeasonalPricing implements Pricing { public double priceFor(int qty) { return 12.0 * qty * 0.9; } }

public class Checkout {
    private final Pricing pricing;                 // subtype polymorphism
    public Checkout(Pricing pricing) { this.pricing = pricing; }
    public double total(int qty) { return pricing.priceFor(qty); }

    public static void main(String[] args) {
        Checkout a = new Checkout(new FlatPricing());
        Checkout b = new Checkout(new BulkPricing());
        Checkout c = new Checkout(new SeasonalPricing());
        System.out.println(a.total(20));   // 200.0
        System.out.println(b.total(20));   // 160.0  (bulk)
        System.out.println(c.total(20));   // 216.0  (seasonal)
    }
}
```
The `Checkout` class never changes when pricing strategies are added — add `LoyaltyPricing`, inject it, done. That's Open-Closed via subtype polymorphism.

## 16. Industry Usage
- **Java collections**: `List`, `Map` interfaces over many implementations; `Collections.sort(List<T>)` parametric + subtype polymorphic sorting via `Comparator`.
- **Spring**: interface injection (subtype polymorphism) is the framework's spine; AOP proxies dispatch through interfaces.
- **JDK `Comparable`/`Comparator`**: sorting is polymorphic — any type that implements `compareTo` sorts.
- **Streams/lambdas**: functional interfaces (`Function<T,R>`) are single-method polymorphism — Java 8+ "polymorphism at function granularity."
- **Games (Unity/C#)**: `MonoBehaviour` hooks are subtype polymorphism; entity systems prefer component composition but still use polymorphic callbacks.
- **Go**: interfaces (`io.Reader`) give subtype polymorphism structurally — the same "one contract, many implementations" with zero inheritance.

## 17. References
- Erich Gamma et al., *Design Patterns* — "Program to an interface" (polymorphism intro).
- Robert C. Martin, *Clean Architecture* — polymorphism and the Dependency Rule.
- Bjarne Stroustrup, *The C++ Programming Language* — polymorphism taxonomy.
- Java Language Specification, §8.4.8 (Inheritance, Overriding, Hiding), §5.5 (casts): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- GeeksForGeeks, "Polymorphism in Java": https://www.geeksforgeeks.org/polymorphism-in-java/

## 18. Cheat Sheet
- Polymorphism = one interface, many forms.
- 4 categories: ad-hoc (overloading), parametric (generics), subtype (overriding), coercion (conversion).
- Static binding (compile-time): overload/generic. Dynamic binding (runtime): override/vtable.
- Payoff: Open-Closed, uniform handling, decoupling, testability.
- Cost: one O(1) indirection, often devirtualized.
- `Animal a = new Dog(); a.speak()` → Dog's (runtime).
- Polymorphism ≠ inheritance — interfaces/generics/duck-typing give it too.
- Pattern → polymorphism mapping: Strategy/interface, Template/override, Visitor/double-dispatch.

## 19. Quiz
1. Which is runtime polymorphism? a) overloading b) overriding c) generics d) coercion → **b**
2. Ad-hoc polymorphism = a) generics b) overloading c) overriding d) conversion → **b**
3. Adding a subtype without changing callers = a) LSP b) Open-Closed c) SRP d) DIP → **b**
4. `List<T>` is: a) subtype b) parametric c) ad-hoc d) coercion → **b**
5. A polymorphic call is: a) O(log n) b) O(n) c) O(1) d) O(n²) → **c**
6. True or False: Polymorphism requires inheritance. → **False**

## 20. Flashcards
- **Q: What is polymorphism?** → **A:** One interface, many implementations — compile-time (overload/generic) or runtime (override/dispatch).
- **Q: Four categories?** → **A:** Ad-hoc (overload), parametric (generic), subtype (override), coercion (conversion).
- **Q: Which is runtime?** → **A:** Subtype polymorphism (virtual dispatch).
- **Q: Main payoff?** → **A:** Open-Closed — new types without editing callers.
- **Q: Cost?** → **A:** O(1) indirection; often devirtualized.
- **Q: `Animal a = new Dog(); a.speak()` runs?** → **A:** Dog.speak — object type, not variable type.
- **Q: Can you have polymorphism without inheritance?** → **A:** Yes — interfaces, generics, duck typing.

## 21. Revision
Polymorphism = one interface, many implementations, resolved at compile time (ad-hoc overloading, parametric generics, coercion) or runtime (subtype overriding via vtable). It's the pillar that enables Open-Closed: callers depend on contracts, new subtypes are added without editing existing code, and dispatch stays O(1). Upcasting never changes which override runs (object type decides). It doesn't require inheritance — interfaces, generics, and duck typing all give polymorphism. First-30-seconds answers: "overloading = compile-time; overriding = runtime; one interface many forms; O(1) vtable."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is polymorphism?" | Formal Definition / Section 13 |
| "Types of polymorphism?" | Interview Q2 / Section 7 |
| "Is overloading polymorphism?" | Interview Q3 |
| "How does it enable Open-Closed?" | Interview Q4 |
| "Static vs dynamic binding?" | Interview Q6 |
| "Polymorphism without inheritance?" | Interview Q15 |
| "Parametric vs subtype?" | Interview Q9 |
| "How do patterns use it?" | Interview Q13 |
