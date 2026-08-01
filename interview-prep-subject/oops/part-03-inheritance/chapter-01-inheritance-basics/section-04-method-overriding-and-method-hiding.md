# Method Overriding and Method Hiding

> **TL;DR**: Overriding replaces an inherited instance method's behavior via runtime dispatch (same signature, same/looser access, same/covariant return); **hiding** is what happens with `static` methods and fields — the subclass's version shadows the parent's and is resolved by *reference type at compile time*, not the object type at runtime.

## 1. Why Does This Exist?
Overriding and hiding exist because a subclass must be able to *change what an inherited name means* — but there are two different kinds of "change." **Overriding** is about *behavior specialization*: `Dog.speak()` behaves differently from `Animal.speak()`, and which runs is decided at runtime by the actual object type (dynamic dispatch) — this is the heart of polymorphism. **Hiding** is the accidental or deliberate case where a subclass declares a member with the same name as a *static* member (or a field) of the parent: since static members have no instance dispatch, the subclass's version merely *hides* the parent's, and the compiler picks by the reference type. Interviews ask about the distinction because the "can you override a static method?" trap is one of the most common Java screening questions, and because misusing `static` "overriding" silently produces the wrong method at runtime.

## 2. How Does It Work?
**Overriding** (instance methods):
```java
class Animal { void speak() { ... } }         // to be overridden
class Dog extends Animal {
    @Override void speak() { ... }            // override: same signature
}
Animal a = new Dog();
a.speak();                                    // Dog.speak — runtime dispatch
```
**Hiding** (static methods):
```java
class Animal { static void who() { print("Animal"); } }
class Dog extends Animal {
    static void who() { print("Dog"); }       // HIDES Animal.who
}
Animal a = new Dog();
a.who();                                      // Animal.who! compile-time, by reference type
Dog.who();                                    // Dog.who
```
Fields also hide: `class Dog { String name; }` with `class Animal { String name; }` → two separate fields; reference type picks which you see.

## 3. When Is It Used?
- **Overriding**: 
  - Framework hooks — `doGet`, `onCreate`, `run()`, template method hooks.
  - Domain behavior specialization — `pay()`, `area()`, `render()`.
  - `toString()`, `equals()`, `hashCode()` (overriding Object methods).
- **Hiding**:
  - Static utility redefinition (usually an anti-pattern — prefer a new name or composition).
  - Shadowed constants (`static final` same name) — a deliberate but rare pattern.
  - Field shadowing — almost always a bug; avoid.
- **Using `super.method()`** when the override wants to extend parent behavior.

## 4. Why Wasn't Another Approach Chosen?
- *Why not make all methods final (no overriding)?* Then polymorphism dies — you couldn't have `List` behave differently per implementation; framework hooks would be impossible. Overriding chosen as the default for instance methods; `final` as the opt-out for methods that must not change.
- *Why not make static methods override too (virtual statics)?* Statics have no instance — no `this`, no receiver — so "which version runs" can't depend on the object type (there is no object). Making them virtual would create confusing dispatch with no object to dispatch on. So hiding (compile-time, by reference type) was chosen as the honest semantic.
- *Why not forbid same-name statics in subclasses entirely?* Java could have made it an error, but it allows *hiding* (with a compiler warning) for compatibility and flexibility; the rule is just that it's hiding, not overriding.
- *Why not allow `@Override` on static methods?* `@Override` specifically asserts *overriding*; using it on a static method is a compile error — the annotation is the language's way of forcing you to know the difference.

## 5. Intuition
- **Overriding** is like a **different actor playing the same role in a play**: the script says "the hero speaks" (the method name), and the actor on stage (the runtime object) decides how — whichever actor is actually there speaks their version.
- **Hiding** is like a **surname conflict on a sign**: if the company directory has "A. Sharma — Admin" and "A. Sharma — Sales", *which* you reach depends on which directory (reference type) you're looking at, not on the person's identity. The subclass's "A. Sharma" doesn't replace the parent's — it just hides it from view when you look at the subclass.

## 6. Real-World Analogy
**Emergency protocols in a hospital**. The generic protocol (parent's `respond()`) says "call for help." The *cardiac team* overrides it (subclass) with "call for help AND defibrillate" — when a cardiac patient arrives, the runtime object (the actual team) chooses its version: that's overriding. Meanwhile, the *hospital directory* has both a generic "Emergency: Dial 0" and the cardiac wing's printed "Emergency: Dial 9" — if you dial based on which directory you're reading (reference type), you get different numbers, and the cardiac directory didn't replace the generic one; it just *hides* it on that wing's page: that's static hiding.

## 7. Formal Definition
**Method overriding**: a subclass declares a method with the same signature (name + parameter types) as a non-final, non-static, non-private method of a superclass; the subclass method must have the same or a broader (less restrictive) access modifier, the same or a covariant return type (subtype of the parent's return), and must not throw new broader checked exceptions. At runtime, invoking the method on a reference of the parent type dispatches to the subclass implementation (dynamic dispatch via the vtable). **Method hiding**: a subclass declares a `static` method with the same signature as a `static` method of a superclass (or a field with the same name); the subclass member is *not* inherited-and-dispatched but merely shadows the parent's, and resolution is determined at compile time by the reference type. Overriding is governed by `@Override`; hiding a static is allowed but not an override.

## 8. Example
```java
public class Shape {
    protected double area;
    public double area() { return area; }                    // overridable
    public static String kind() { return "shape"; }          // hideable static
}
public class Circle extends Shape {
    public Circle(double r) { this.area = Math.PI * r * r; }
    @Override public double area() { return area; }          // OVERRIDE (runtime)
    public static String kind() { return "circle"; }         // HIDES Shape.kind
}
public class Main {
    public static void main(String[] args) {
        Shape s = new Circle(2);
        System.out.println(s.area());        // 12.566... — Circle.area (dynamic dispatch)
        System.out.println(s.kind());        // "shape"   — Shape.kind! (static, by reference type)
        Circle c = new Circle(2);
        System.out.println(c.kind());        // "circle"  — Circle.kind (by declared type)
    }
}
```
The trap made visible: `s.area()` picks `Circle`'s (runtime, override); `s.kind()` picks `Shape`'s (compile-time, hiding). Two same-looking calls, two completely different resolutions.

## 9. Internal Working
1. **Override**: `Circle.area` replaces the vtable slot inherited from `Shape`; a call `s.area()` where `s` is typed `Shape` reads the vtable → `Circle.area`. O(1).
2. **Hiding**: `Circle.kind` and `Shape.kind` are two *separate* static entries; the compiler resolves `s.kind()` by the declared type `Shape` at compile time and emits a direct call to `Shape.kind` — no vtable, no runtime choice. `c.kind()` emits `Circle.kind`.
3. **Fields**: `Shape.area` and (if declared) `Circle.area` would be *two distinct fields* in the object; `((Shape) c).area` and `c.area` could read different values — the classic shadowing bug.
4. **`@Override`**: the compiler verifies an actual override exists; a mismatch (e.g., wrong signature, static method, or private) is a compile error — it turns "I meant to override" mistakes into build failures.
5. **`final`/`private`**: a `final` method cannot be overridden (compile error); a `private` method is not inherited, so a same-named method in the subclass is a *new* method, not an override (and `@Override` would fail).

## 10. Time Complexity
- Override dispatch: O(1) — single vtable lookup.
- Hidden static call: O(1) — direct compile-time call.
- Both are constant-time; the distinction is *which* method the compiler chose, not *how fast* it runs.
- JIT may devirtualize/inline override calls (O(1) direct) when a single implementation is visible.

## 11. Advantages
- **Overriding**: polymorphic behavior (extensible, Open-Closed); framework hooks; template-method extensibility; subtype correctness via `@Override` checks.
- **Hiding**: lets a subclass provide its own class-level utility with the same name (rarely useful); allows "overriding-like" behavior for statics where the parent can't be edited.

## 12. Disadvantages
- **Overriding**: forgetting `super.method()` drops parent logic silently; overriding without `@Override` hides mistakes; access/throws mismatches are easy to get wrong.
- **Hiding**: the #1 silent-bug source — developers think `s.kind()` calls the subclass version; the compile-time-by-reference-type rule is unintuitive; field shadowing creates two fields.
- **Both**: coupling to parent internals (fragile base); deep chains make resolution surprising.

## 13. Interview Questions
1. **Q: Difference between overriding and hiding?** A: Overriding replaces an *instance* method with runtime dispatch (by object type); hiding shadows a *static* method (or field) with compile-time resolution (by reference type). Overriding is polymorphic; hiding is not.
2. **Q: Can you override a static method?** A: No — you can only *hide* it. A subclass `static` method with the same signature shadows the parent's; which runs is decided by the reference type at compile time. Using `@Override` on it is a compile error.
3. **Q: What are the rules for a valid override?** A: Same signature (name + params); non-private, non-static, non-final parent method; same or broader access; same or covariant return type; no new broader checked exceptions. `@Override` enforces it.
4. **Q: TRICKY — `class A { void m() {} } class B extends A { static void m() {} }` compiles?** A: No — an instance method in the parent and a static method in the child with the same signature is a compile error (you can't "hide" an instance method with a static one, and vice versa).
5. **Q: What is a covariant return type?** A: An override may return a *subtype* of the parent's return type — `Shape clone()` can be overridden as `Circle clone()`. (Pre-Java 5 it had to match exactly.) Only return types are covariant; parameter types must match exactly (they're not covariant — that would be overloading).
6. **Q: Why can't you override a `private` method?** A: Private methods aren't inherited — the subclass's same-named method is a *new* method entirely, not an override. That's why `@Override` fails on it. (C++/Python treat private-call resolution differently — Java is strict here.)
7. **Q: Why can't you override a `final` method?** A: `final` explicitly forbids overriding (that's its purpose — freeze behavior); a subclass attempt is a compile error. `final` is the "no polymorphism here" opt-out.
8. **Q: SCENARIO — Parent `m()` is `public`; subclass overrides with `protected`. Compiles?** A: No — an override must have the *same or broader* access; narrowing (`public → protected`) is a compile error (it would break the is-a contract — callers relying on `public` would fail).
9. **Q: What is field hiding vs method hiding?** A: Fields don't participate in dispatch at all — a same-named field in the subclass *shadows* the parent's (two separate fields), selected by reference type. It's hiding, never overriding, and almost always a bug (avoid).
10. **Q: PRODUCTION — Why does overriding `equals` without `@Override` cause bugs?** A: Without `@Override`, a typo (e.g., `equals(Object o)` written as `equals(MyClass o)`) silently becomes an *overload*, not an override — `HashMap` calls `equals(Object)`, your method never runs, collections misbehave. `@Override` turns the typo into a compile error.
11. **Q: Can an override throw broader checked exceptions than the parent?** A: No — it may throw the same, narrower, or none (the parent's contract is the upper bound). But it *may* throw new *unchecked* (runtime) exceptions.
12. **Q: TRICKY — `Animal a = new Dog(); a.kind();` where `kind()` is static in both. What prints?** A: `Animal.kind` — static resolution uses the *reference type* (`Animal`), not the object type. If `kind` were an instance method, `Dog.kind` would print. This asymmetry is the whole hiding-vs-overriding point.
13. **Q: How does `super.method()` interact with overriding?** A: It calls the *immediate parent's* implementation non-virtually — the escape hatch for "extend, not replace." Inside an override, `super.method()` is the only way to reach the parent's version.
14. **Q: PRACTICAL — When is hiding acceptable?** A: Almost never for statics — rename (`Dog.describeKind()`) or use composition; hiding makes calls depend on reference type, which is fragile and confusing. Deliberate hiding is rare and usually a design smell.
15. **Q: What's the difference in the bytecode?** A: Overriding compiles to `invokevirtual` (dynamic, vtable); hiding compiles to `invokestatic` (compile-time direct). The two keywords in the bytecode are the mechanical proof of the distinction.

## 14. Follow-Up Questions
1. **Q: What happens when an override has the same signature but different return type (non-covariant)?** A: Compile error — Java does not allow overloading on return type; if the return type differs and isn't covariant, it's neither a valid override nor a valid overload, so the compiler rejects it.
2. **Q: Can a subclass override a method and make it *more* accessible?** A: Yes — `protected → public` is legal (widening allowed); `public → protected` is not. Widening preserves the caller's expectations.
3. **Q: How do C++ and Python handle "hiding"?** A: C++: a derived `static` (or any) method with the same name *hides* all base overloads (name hiding) — you must `using Base::m;` to un-hide. Python: method lookup is entirely MRO-based; statics (classmethods) also resolve via MRO — so Python's "static methods" are dispatched dynamically (they don't have Java's compile-time hiding).
4. **Q: Why is the return type allowed to be covariant but parameters not?** A: Parameters are part of the signature (overload resolution); changing them makes it an *overload*, not an override. Covariant returns are safe because a `Circle` where a `Shape` is promised still satisfies every caller.

## 15. Coding Example
```java
public class Media {
    public void play() { System.out.println("Playing generic media"); }      // overridable
    public static String format() { return "generic"; }                      // hideable static
}
public class Video extends Media {
    @Override public void play() {
        System.out.println("Playing video (framerate 60fps)");
    }
    public static String format() { return "mp4"; }   // HIDES Media.format
}
public class Main {
    public static void main(String[] args) {
        Media m = new Video();
        m.play();                     // "Playing video..."  → override (runtime)
        System.out.println(m.format());   // "generic"       → hide (compile-time, ref type Media)
        Video v = new Video();
        System.out.println(v.format());   // "mp4"            → ref type Video
    }
}
```
```python
# Python: no compile-time hiding — everything resolves via MRO (dynamic)
class Media:
    @staticmethod
    def format(): return "generic"
class Video(Media):
    @staticmethod
    def format(): return "mp4"
m = Video()
print(m.format())    # "mp4" — Python statics dispatch dynamically (no Java-style hiding)
```
```cpp
// C++: name hiding — the derived name hides ALL base overloads
struct Base { void m(int) {} };
struct Derived : Base { void m() {} };   // hides Base::m(int) entirely
// d.m(5) → compile error unless:  using Base::m;
```

## 16. Industry Usage
- **JDK**: overriding `toString`/`equals`/`hashCode` (the foundation of collections correctness); `AbstractList.get` etc. override hooks; `Object.clone` covariant returns are common in domain classes.
- **Spring**: `@Override` on every service method; template-method overrides; AOP proxies rely on virtual dispatch through interfaces.
- **Android**: overriding lifecycle methods is the platform contract (`@Override onCreate`).
- **Static hiding bugs**: the reason static utility classes avoid inheritance entirely — statics are meant to be called by class name, so hiding is a foot-gun teams ban via style guides.
- **Java's own evolution**: covariant returns (Java 5) made overriding usable for typed clones/copies — a real production pattern.

## 17. References
- Java Language Specification, §8.4.8.1 (Overriding), §8.4.8.2 (Hiding): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- Oracle Java Tutorials, "Overriding and Hiding Methods": https://docs.oracle.com/javase/tutorial/java/IandI/override.html
- Joshua Bloch, *Effective Java* — Item 12 (always override toString carefully), Item 11 (equals discipline).
- Bjarne Stroustrup, *The C++ Programming Language* — name hiding and `using` declarations.
- Python docs on MRO/staticmethod: https://docs.python.org/3/library/functions.html#staticmethod

## 18. Cheat Sheet
- Override = instance method, runtime dispatch, object type decides; use `@Override`.
- Hide = static method/field, compile-time, reference type decides; NOT an override.
- Override rules: same signature, same/broader access, covariant return, no broader checked exceptions.
- `@Override` turns "meant to override" typos into compile errors.
- `private`/`static`/`final`/constructor methods cannot be overridden.
- Static vs instance same-signature clash = compile error.
- Field shadowing = two fields (bug); never dispatch.
- Bytecode: `invokevirtual` (override) vs `invokestatic` (hide).

## 19. Quiz
1. Which uses runtime dispatch? a) hiding b) overriding c) field access d) statics → **b**
2. Static methods in a subclass with the parent's signature: a) override b) hide c) overload d) error → **b**
3. A valid override must have access: a) same or broader b) same or narrower c) private d) any → **a**
4. `@Override` on a static method: a) ok b) compile error c) warning d) runtime error → **b**
5. Return type `Circle` overriding `Shape` is: a) invalid b) covariant, legal c) overloading d) hiding → **b**
6. True or False: A `final` method can be overridden. → **False**

## 20. Flashcards
- **Q: Override vs hide?** → **A:** Override = instance, runtime dispatch; hide = static/field, compile-time by reference type.
- **Q: Can you override a static method?** → **A:** No — only hide it.
- **Q: Override rules?** → **A:** Same signature, same/broader access, covariant return, no broader checked exceptions.
- **Q: What does `@Override` do?** → **A:** Compile-time check that a real override exists (catches typos like wrong signature).
- **Q: Can private/final/static methods be overridden?** → **A:** No — private isn't inherited, final is frozen, static hides.
- **Q: Bytecode of each?** → **A:** Override = `invokevirtual`; hide = `invokestatic`.

## 21. Revision
Overriding replaces an instance method with runtime dispatch (vtable), governed by same-signature + broader-or-equal access + covariant return + no broader checked exceptions, and `@Override` enforces it at compile time. Hiding shadows static methods and fields, resolved at compile time by reference type — `Animal a = new Dog(); a.staticMethod()` calls the *Animal* version, the classic trap. Private/final/static/constructor methods can't be overridden; field "overriding" is shadowing (two fields). First-30-seconds answers: "static can't be overridden, only hidden; hidden resolves by reference type at compile time."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Override vs hide?" | Interview Q1 / Section 8 |
| "Can you override a static method?" | Interview Q2 |
| "Override rules?" | Interview Q3 / Formal Definition |
| "Covariant return types?" | Interview Q5 |
| "Why can't private/final be overridden?" | Interview Q6–Q7 |
| "`@Override`'s value?" | Interview Q10 / Section 16 |
| "Static on Animal ref — which runs?" | Interview Q12 |
| "Bytecode difference?" | Interview Q15 |
