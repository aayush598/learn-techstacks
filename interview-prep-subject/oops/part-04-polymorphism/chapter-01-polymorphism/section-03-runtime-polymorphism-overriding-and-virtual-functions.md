# Runtime Polymorphism: Overriding and Virtual Functions

> **TL;DR**: Runtime polymorphism is subtype polymorphism — a base/interface reference holding a subclass object dispatches method calls to the object's own implementation at runtime; Java methods are virtual by default, C++ requires the explicit `virtual` keyword, and `final`/`@Override` control the edges.

## 1. Why Does This Exist?
Runtime polymorphism exists because **you often know *what* an object is (its contract) but not *which* implementation you'll be handed** — the framework hands you a callback, the DI container injects a strategy, the factory returns a subtype. At the call site, all you have is `Animal` (or `Runnable`, or `PaymentProcessor`); the *actual* object is a `Dog` or an `EmailSender`, decided elsewhere. Overriding makes that work: the subclass *replaces* the inherited implementation, and the runtime dispatches the call to the replacement. Without it, the framework couldn't call *your* code (that's Inversion of Control), strategies couldn't be swapped, and `List<Shape>` couldn't sum mixed areas. It's the mechanism that turns "program to an interface" from a slogan into working code.

## 2. How Does It Work?
```java
class Animal { void speak() { print("animal"); } }     // overridable by default in Java
class Dog extends Animal { @Override void speak() { print("bark"); } }
Animal a = new Dog();
a.speak();        // runtime dispatch → "bark"
```
- Java: instance methods are **virtual by default**; subclasses override; `final` opts out; `private`/`static` aren't virtual.
- C++: methods are **NOT virtual unless declared `virtual`**; a non-virtual method is resolved by static type; `virtual` methods dispatch dynamically; `= 0` makes them pure (abstract).
- At the call site, the variable's type (`Animal`) only *names* the contract; the *object's* type (`Dog`) decides the implementation — via the vtable (covered in Section 04).
- `@Override` (Java) / `override` (C++) assert the intent and catch signature mismatches at compile time.

## 3. When Is It Used?
- **Every "program to an interface" case**: `List<String> = new ArrayList<>()`, DI-injected services, `Runnable` callbacks.
- **Framework hooks**: `doGet`/`doPost` (servlets), `onCreate` (Android), `run()` (Thread).
- **Template method pattern**: base skeleton calls overridable hooks.
- **Strategy/State/Visitor**: polymorphic implementations swapped or dispatched.
- **Domain specialization**: `area()`, `pay()`, `render()` overridden per subtype.
- **Library callback contracts**: `Comparator`, `Callable`, `Consumer`.

## 4. Why Wasn't Another Approach Chosen?
- *Why make Java virtual-by-default but C++ opt-in?* Java prioritizes flexibility and safety (forgetting `virtual` in C++ silently binds statically — a classic bug); C++ prioritizes performance (a non-virtual call is direct/inlineable; making everything virtual costs vptr + table). Java chose "safe by default, opt-out with `final`"; C++ chose "fast by default, opt-in with `virtual`."
- *Why not make ALL methods runtime-dispatched (fully dynamic)?* Overhead on every call and no compile-time certainty; static calls can be inlined/devirtualized. The hybrid (virtual where needed) is the design.
- *Why not use overloading for behavior differences?* Overloading selects by *static argument types*, so `Animal a = new Dog(); a.speak()` can't choose by object type — only override (runtime dispatch) can. They solve different selection problems.
- *Why not callbacks/function pointers instead of overriding?* Function pointers (C, Go) achieve dynamic behavior too, but overriding ties the behavior to the *type* (self-documenting, type-safe, inheritable) — the object-oriented choice for subtype semantics.

## 5. Intuition
Imagine ordering at a restaurant by **category**: you say "I'd like the signature dish" (the contract, `dish()`), and the kitchen decides what that means for *their* restaurant — Italian kitchen: pasta; Indian: curry; the kitchen (the object) interprets the order. If you'd named the dish concretely ("pasta"), you'd have over-committed; the *category* order lets each kitchen respond its own way. That's runtime polymorphism: one order (method call), many kitchens (subtypes), each answering in its own style, decided at the moment of service (runtime).

## 6. Real-World Analogy
A **TV remote's power button**. You press the same button, and *whichever TV is on the table* (whichever object) responds — a Samsung, a Sony, an LG; each has its own firmware (override of `power()`) and the remote (caller) doesn't care which. Swap the TV (inject a different object) and the button still works — same instruction, different response, chosen by the actual device at press time (runtime dispatch). If the button printed "Samsung power!" on it (static binding, C++ non-virtual), a Sony would do nothing.

## 7. Formal Definition
**Runtime (subtype) polymorphism** is achieved by **method overriding**: a subclass redefines an inherited method with the same signature, and calls on a reference of the superclass/interface type are dispatched, at runtime, to the most-derived implementation of the object's dynamic type (via the virtual method table). **Virtual functions** are methods declared for dynamic dispatch: in Java, non-static, non-private, non-final instance methods are virtual by default; in C++, only methods declared `virtual` (and their overrides) dispatch dynamically, with `= 0` denoting a pure virtual (abstract) function. Overriding requires identical signature, same-or-broader access, and covariant return (Java). `@Override` (Java) and `override` (C++) are compile-time annotations asserting that an override truly overrides.

## 8. Example
```java
public abstract class Payment {                      // abstract: contract only
    public abstract boolean pay(double amount);
}
public class CardPayment extends Payment {
    @Override public boolean pay(double amount) {   // override — runtime
        System.out.println("card charged " + amount);
        return true;
    }
}
public class CryptoPayment extends Payment {
    @Override public boolean pay(double amount) {
        System.out.println("crypto transferred " + amount);
        return true;
    }
}
public class Checkout {
    private final Payment payment;                   // interface/abstract type
    public Checkout(Payment p) { this.payment = p; }
    public boolean charge(double amt) { return payment.pay(amt); }   // dynamic dispatch
}
// new Checkout(new CardPayment())   → "card charged"
// new Checkout(new CryptoPayment()) → "crypto transferred" — same charge() call!
```
`charge()` compiles once; the runtime object decides which `pay` runs — the essence of overriding + virtual functions.

## 9. Internal Working
1. `Payment` declares abstract `pay`; each subclass provides a concrete implementation; the class loader builds each class's vtable with `pay` at the same slot index.
2. `Checkout.charge` compiles `payment.pay(amt)` to a virtual invocation — the bytecode names the method `Payment.pay`, but the JVM resolves the *target* at runtime.
3. At runtime: read the object's header → klass pointer → vtable → slot for `pay` → jump. `CardPayment`'s slot → `CardPayment.pay`; `CryptoPayment`'s → `CryptoPayment.pay`.
4. The JIT installs an inline cache (first-seen target cached as a direct call); if the call site is monomorphic in practice, the vtable is bypassed entirely.
5. C++: a virtual call does `*(this->vptr + slot)`; a non-virtual call compiles to a direct address (no dispatch). `virtual` presence decides whether the vptr/table exists at all.

## 10. Time Complexity
- Virtual call: O(1) — one vtable indirection.
- After JIT devirtualization: O(1) direct call (often inlined) — effectively free.
- C++ virtual call: O(1) (vptr + slot); non-virtual: O(1) direct.
- No hierarchy-depth cost; dispatch is always constant-time.

## 11. Advantages
- **Substitution**: base/interface code works for any subtype (LSP).
- **Extensibility**: new subtypes without modifying callers (OCP).
- **Inversion of Control**: frameworks call your overrides.
- **Type-safe callbacks**: `Runnable`, `Comparator` as contracts.
- **Self-documenting behavior**: the type declares its capabilities.

## 12. Disadvantages
- **Indirection**: one extra pointer dereference per virtual call (usually devirtualized).
- **Non-inlinable in C++** unless devirtualized — a hot-loop concern in HFT/games.
- **Hides behavior**: which implementation runs isn't visible at the call site (harder debugging).
- **LSP fragility**: a bad override breaks all callers.
- **C++ pitfall**: forgetting `virtual` silently makes calls static — the #1 C++ polymorphism bug.

## 13. Interview Questions
1. **Q: What is runtime polymorphism?** A: Subtype polymorphism — an overridden method is chosen at runtime by the object's actual type (via vtable), so a base/interface reference calls the subclass's implementation.
2. **Q: Difference between Java and C++ virtual?** A: Java instance methods are virtual by default (`final` opts out); C++ requires the explicit `virtual` keyword — a non-virtual C++ method binds statically. Java chose safety, C++ chose performance.
3. **Q: TRICKY — In C++, `Animal* a = new Dog(); a->speak();` where `speak()` is NOT virtual. What runs?** A: `Animal::speak` — static binding by pointer type; forgetting `virtual` is the classic silent bug. With `virtual`, `Dog::speak` runs.
4. **Q: What is `@Override` / `override` for?** A: Compile-time assertions that the method really overrides a parent/interface method — catching signature typos (which would silently create an overload) and C++ base changes.
5. **Q: What's the difference between overriding and overloading?** A: Overriding = same signature, runtime dispatch, subclass relationship; overloading = different signatures, compile-time selection, same class. One is dynamic, one static.
6. **Q: SCENARIO — A template method calls a hook that subclasses override. Which runs?** A: The subclass's override — template methods rely on runtime dispatch; the base skeleton is fixed, the hook is polymorphic. (The anti-pattern: calling the hook *from a constructor* — subclass fields not yet set.)
7. **Q: Can you override a static method?** A: No — statics are hidden, not overridden; resolution is compile-time by reference type. Same for `final` (Java) and `private` (not inherited).
8. **Q: PRODUCTION — Why do DI frameworks depend on virtual dispatch?** A: They inject a concrete object behind an interface and let every caller dispatch to it dynamically — swapping `ProdService` for `MockService` at the composition root requires zero caller changes. That's runtime polymorphism powering the whole DI model.
9. **Q: What is the "vptr" in C++?** A: A hidden pointer in each polymorphic object, pointing to the class's vtable; objects of virtual classes carry it, making them 8 bytes larger (on 64-bit) — the memory cost of virtualness.
10. **Q: TRICKY — Is a non-virtual call in C++ ever polymorphic?** A: Not by dispatch — but the compiler can still devirtualize virtual calls when it proves the concrete type (e.g., a `final`/sealed class or a known constructor), making it a direct call. Devirtualization is an optimization, not semantics.
11. **Q: What happens if an override has a different signature?** A: It's an *overload* (in the subclass), not an override — a call through the base reference silently calls the base's version; `@Override` catches this at compile time.
12. **Q: When does runtime polymorphism beat a type-switch?** A: Whenever the set of types is open (you'll add more) or behavior is per-type — the switch must be updated everywhere, polymorphism localizes the change to the new class. Use switch only for closed, known sets.
13. **Q: SCENARIO — Design an audio `play()` that supports MP3 and FLAC without a switch.** A: `interface AudioFormat { void play(); }` + `Mp3Format implements AudioFormat` + `FlacFormat`; a player holds the format object and calls `play()` — adding `OggFormat` is one new class; the player never changes.
14. **Q: What is the cost of virtual dispatch in practice?** A: One indirect jump (vtable) per call — nanoseconds; JITs devirtualize monomorphic sites so the common case is a direct (often inlined) call. In C++ hot loops, prefer non-virtual or devirtualized paths.
15. **Q: PRODUCTION — Why do style guides say "design for inheritance or forbid it"?** A: Overriding exposes behavior to subclasses (fragile base); Bloch's guidance: if a class isn't designed as an extension contract, make methods/classes `final` to prevent accidental (broken) overriding.

## 14. Follow-Up Questions
1. **Q: What is the relationship between virtual functions and the LSP?** A: Virtual dispatch is the mechanism; LSP is the contract — every override must be substitutable for the base's behavior, or polymorphic calls corrupt the system.
2. **Q: What is a "pure virtual" function?** A: `virtual void f() = 0;` — no implementation in the base, making the base abstract; subclasses must implement it (C++'s version of Java abstract methods).
3. **Q: How do interfaces relate to virtual functions?** A: Interface methods are implicitly virtual — implementing a Java/Go interface means dynamic dispatch on those methods; C# interface methods are virtual by default too.
4. **Q: What's "virtual inheritance" vs "virtual functions"?** A: Unrelated — virtual inheritance (C++) merges diamond base subobjects; virtual functions enable runtime dispatch. Both have "virtual" in the name; don't conflate them.

## 15. Coding Example
```java
public class Shape {
    public double area() { return 0; }                       // Java: virtual by default
}
public final class Circle extends Shape {                    // final class → devirtualization-friendly
    private final double r;
    public Circle(double r) { this.r = r; }
    @Override public double area() { return Math.PI * r * r; }
}
public class Rectangle extends Shape {
    private final double w, h;
    public Rectangle(double w, double h) { this.w = w; this.h = h; }
    @Override public double area() { return w * h; }
}
public class Main {
    public static void main(String[] args) {
        List<Shape> shapes = List.of(new Circle(2), new Rectangle(3, 4));
        double total = 0;
        for (Shape s : shapes) total += s.area();            // runtime dispatch per element
        System.out.println(total);                            // 12.566... + 12.0
    }
}
```
```cpp
struct Shape { virtual double area() const = 0; virtual ~Shape() = default; };
struct Circle final : Shape {
    double r;
    double area() const override { return 3.14159 * r * r; }
};
double total(const std::vector<Shape*>& v) { double t = 0; for (auto* s : v) t += s->area(); return t; }
```

## 16. Industry Usage
- **JDK**: `List.sort` dispatches to per-implementation sorts; `toString`/`equals` overrides power all collections; `Comparable.compareTo` is a virtual contract.
- **Spring**: AOP + DI are pure runtime polymorphism — proxies intercept virtual calls through interfaces.
- **Android**: `Activity`/`Fragment` lifecycle hooks are overrides the OS calls — the entire platform is inversion of control via overriding.
- **Servlets/Jakarta**: `doGet`/`doPost` overrides invoked by the container.
- **Go**: interface methods dispatch dynamically (like Java), without `virtual` keywords — runtime polymorphism is implicit.
- **C++ (Chrome, games, HFT)**: `virtual` used at API boundaries, `final`+devirtualization on hot paths; the performance-vs-flexibility balance is engineered explicitly.

## 17. References
- Java Language Specification, §8.4.8.1 (Overriding) — virtual-by-default semantics: https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- Bjarne Stroustrup, *The C++ Programming Language* — virtual functions, abstract classes.
- Scott Meyers, *Effective C++* — Items 33–37 (virtual, hiding, default args with virtuals).
- Oracle Java Tutorials, "Overriding and Hiding Methods": https://docs.oracle.com/javase/tutorial/java/IandI/override.html
- GeeksForGeeks, "Virtual Functions in C++": https://www.geeksforgeeks.org/virtual-function-cpp/

## 18. Cheat Sheet
- Runtime polymorphism = overriding + virtual dispatch.
- Java: instance methods virtual by default; `final` opts out.
- C++: must write `virtual`; `=0` = pure/abstract.
- `@Override`/`override` assert intent at compile time.
- Override needs: same signature, same/broader access, covariant return.
- Static/private/final methods never override (hide or new).
- Virtual call = O(1) vtable; JIT devirtualizes.
- C++ forgetting `virtual` = silent static binding bug.

## 19. Quiz
1. Java methods are virtual: a) only with virtual b) by default c) never d) with final → **b**
2. C++ requires for dispatch: a) `final` b) `virtual` c) `static` d) nothing → **b**
3. A different-signature "override" is: a) override b) overload c) hide d) error → **b**
4. `@Override` on a static method: a) ok b) compile error c) warning d) runtime → **b**
5. Virtual call cost: a) O(n) b) O(log n) c) O(1) d) O(n²) → **c**
6. True or False: Non-virtual C++ calls dispatch at runtime. → **False**

## 20. Flashcards
- **Q: Runtime polymorphism via?** → **A:** Overriding + virtual dispatch (vtable).
- **Q: Java vs C++ virtual?** → **A:** Java default-virtual; C++ opt-in `virtual`.
- **Q: `@Override` purpose?** → **A:** Compile-time override assertion; catches signature typos.
- **Q: C++ forgetting virtual?** → **A:** Silent static binding — the classic bug.
- **Q: Override requirements?** → **A:** Same signature, same/broader access, covariant return.
- **Q: Virtual call cost?** → **A:** O(1); JITs devirtualize monomorphic sites.

## 21. Revision
Runtime polymorphism is overriding + virtual dispatch: a base/interface reference calls the object's own implementation at runtime. Java instance methods are virtual by default (`final` opts out); C++ requires `virtual` (forgetting it = static binding bug). Overrides need identical signatures, same/broader access, covariant returns; `@Override` asserts intent. Virtual calls are O(1) and usually devirtualized. This is the mechanism behind DI, callbacks, framework hooks, and "program to an interface." First-30-seconds answers: "Java default-virtual, C++ opt-in; override = runtime, O(1) vtable."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is runtime polymorphism?" | Interview Q1 / Section 8 |
| "Java vs C++ virtual?" | Interview Q2 |
| "Non-virtual C++ call?" | Interview Q3 |
| "Purpose of @Override?" | Interview Q4 |
| "Override vs overload?" | Interview Q5 |
| "How DI uses it?" | Interview Q8 / Section 16 |
| "Different signature override?" | Interview Q11 |
| "Virtual dispatch cost?" | Interview Q14 / Section 10 |
