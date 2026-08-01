# Types of Inheritance: Single, Multilevel, Hierarchical

> **TL;DR**: Inheritance comes in five shapes — single (one parent), multilevel (grandparent chain), hierarchical (one parent, many children), multiple (many parents — banned in Java classes, allowed in C++/Python with caveats), and hybrid — each legal in some languages and dangerous in others.

## 1. Why Does This Exist?
The "types of inheritance" taxonomy exists because the *shape* of the hierarchy determines its safety and its consequences. Single inheritance is simple and predictable; multilevel inheritance is how real domain models grow (but can get deep and brittle); hierarchical inheritance is natural (many subtypes of one concept); multiple inheritance is where things break — two parents may both define the same thing, creating the ambiguity known as the **diamond problem**. Interviews ask "what are the types of inheritance?" to check your vocabulary, then immediately probe "why no multiple inheritance in Java?" to test whether you understand the *reason* behind the language rules, not just the rule itself.

## 2. How Does It Work?
- **Single**: `class B extends A` — one direct parent. Java's only class-inheritance option.
- **Multilevel**: `class C extends B extends A` — a chain (grandparent → parent → child).
- **Hierarchical**: `class B1 extends A`, `class B2 extends A` — one parent, many children.
- **Multiple**: `class D extends B, C` — two (or more) direct parents. Java classes: banned. C++: allowed. Python: allowed (MRO resolves order).
- **Hybrid**: a mix (e.g., multilevel + multiple), which is where the diamond appears: `D extends B, C`, both `B` and `C` extend `A`.

The mechanism is the same `extends`/`:` in every case; what changes is *how many parents* and *how name conflicts and duplicate state are resolved*.

## 3. When Is It Used?
- **Single**: default — the Java norm (almost every class has one parent).
- **Multilevel**: layered domain models — `Vehicle → LandVehicle → Car`; framework chains — `HttpServlet` subclasses.
- **Hierarchical**: subtype families — `Animal → Dog, Cat, Bird`; `Payment → Card, UPI, NetBanking`.
- **Multiple (C++/Python)**: mixins and interfaces-like composition — a `FlyingCar` mixing `Vehicle` + `Aircraft`; Python's `class LoggingMixin` multiple inheritance for shared behavior.
- **Hybrid/diamond**: almost never intentional — usually an accident to be redesigned.

## 4. Why Wasn't Another Approach Chosen?
- *Why is Java single-inheritance for classes?* Because multiple inheritance of *implementation* creates ambiguity (two parents with the same method or duplicate state) and is error-prone. Java's design chose: single implementation inheritance (classes) + multiple *type* inheritance (interfaces). C++ allowed full multiple inheritance and made programmers manage the diamond with `virtual` inheritance — powerful but dangerous; Java judged the danger not worth it.
- *Why allow it in Python?* Python's dynamic dispatch + C3 linearization MRO resolves the diamond deterministically (`super()` follows MRO), so multiple inheritance is usable for mixins; but it's still a source of subtle bugs and is discouraged beyond mixins.
- *Why not single-inheritance-only in C++?* Stroustrup chose multiple inheritance deliberately for expressiveness (like virtual bases), accepting the complexity. The industry verdict: multiple class inheritance is rarely *needed*; interfaces/mixins cover ~all real uses — which is exactly why Java, C#, Go, Rust, and Kotlin (mostly) ban or avoid it.
- *Why not composition everywhere instead of multilevel?* Multilevel inheritance is convenient but deep chains become brittle (fragile base). Composition with delegation is the modern replacement when the chain is "reuse," not "true specialization."

## 5. Intuition
- **Single** = you have one biological parent.
- **Multilevel** = grandparents, parents, you — a chain of inheritance.
- **Hierarchical** = one parent, many siblings (one father, many children).
- **Multiple** = two parents (two sets of genes). When both parents carry the same gene, which wins? That's the diamond problem.
- **Hybrid** = extended families with two parents who themselves share a common ancestor — the family tree becomes a diamond.

The intuition for why Java bans multiple: two parents both define `doWork()` — which do you call? Biology has a resolved answer; programming languages must invent one, and getting it wrong silently is dangerous.

## 6. Real-World Analogy
**Tool catalogs**: Single — the "Drill" class has one parent "PowerTool". Multilevel — "CordlessDrill" → "Drill" → "PowerTool" → "Tool". Hierarchical — "Drill" and "Saw" both extend "PowerTool". Multiple — a "HammerDrill" that inherits from both "Drill" and "Hammer" — now if both parents define "mode()" differently (rotation vs impact), what's a HammerDrill's mode? You'd need a rule to pick one — that rule is the diamond resolution, and languages differ on it.

## 7. Formal Definition
**Single inheritance**: a class has exactly one direct superclass. **Multilevel inheritance**: a class inherits from a chain of superclasses (a transitively inherits from its parent's parent). **Hierarchical inheritance**: more than one class shares the same direct superclass. **Multiple inheritance**: a class has two or more direct superclasses. **Hybrid inheritance**: a combination of the above (typically multilevel plus multiple), which produces the **diamond problem** when two superclasses share a common ancestor — the derived class inherits ambiguous, possibly duplicated, state and method definitions. Java classes allow only single (and multilevel/hierarchical by extension), with interfaces providing multiple *type* inheritance; C++ allows multiple implementation inheritance; Python supports it with C3 linearization (MRO).

## 8. Example
```java
// SINGLE
class Vehicle { void move() {} }
class Car extends Vehicle {}                      // single: one parent

// MULTILEVEL
class LandVehicle extends Vehicle {}              // Vehicle → LandVehicle → Car
class Suv extends LandVehicle {}                  // grandparent chain

// HIERARCHICAL
class Motorcycle extends Vehicle {}               // Vehicle → Motorcycle too
class Bus extends Vehicle {}                      // one parent, many children

// MULTIPLE via INTERFACES (Java's answer)
interface Movable { void move(); }
interface Sizable { void resize(); }
class Robot implements Movable, Sizable {         // multiple TYPE inheritance
    public void move() {} public void resize() {}
}
```
Java: single class chain + multiple interfaces — the "two axes" design. C++/Python could do `class Suv extends LandVehicle, Movable` (multiple).

## 9. Internal Working
1. **Single**: object layout = base fields + subclass fields; single vtable; unambiguous.
2. **Multilevel**: `Suv` object = Vehicle fields + LandVehicle fields + Suv fields; vtable chains each level's overrides; dispatch O(1) regardless of depth.
3. **Hierarchical**: each child has its own full layout + vtable; siblings share only the base *definition*, not each other's fields.
4. **Multiple (C++)**: object layout can contain *two* copies of a shared ancestor's fields (the classic diamond duplication) unless `virtual` inheritance merges them into one shared subobject (adding indirection); method resolution needs disambiguation rules (dominance, explicit `B::m()`).
5. **Multiple (Python)**: C3 linearization builds a single MRO list (e.g., `D → B → C → A`); `super()` follows the MRO, so method chains are deterministic; each class's `__dict__` lookups follow the MRO.
6. **Java interfaces (multiple type)**: itable holds each interface's methods; a class can have many interfaces with zero layout duplication (no state).

## 10. Time Complexity
- Single/multilevel/hierarchical dispatch: O(1) vtable per call — depth-independent.
- Java multiple interfaces: O(1) itable dispatch.
- C++ multiple inheritance: O(1) dispatch (adjusted this pointer); `virtual` inheritance adds one indirection (vbase pointer) — still O(1).
- Python MRO: O(1) lookup after C3 linearization (cached); method lookup O(depth) worst-case on miss.
- None of the shapes change asymptotics of *calls*; the cost is complexity, not speed.

## 11. Advantages
- **Single**: simple, predictable, safe.
- **Multilevel**: natural layered modeling, progressive specialization.
- **Hierarchical**: organizes a family of subtypes cleanly; one change to the parent updates all children.
- **Multiple (interfaces / C++ mixins)**: combines orthogonal capabilities (a class that is both Movable and Sizable).

## 12. Disadvantages
- **Multilevel**: deep chains → fragile base, hard to trace, harder to test.
- **Hierarchical**: a change in the parent can ripple to many children.
- **Multiple**: ambiguity, duplicate state (C++ diamond), MRO surprises (Python), illegal in Java classes.
- **Hybrid/diamond**: almost always a design smell; debugging overrides across the diamond is painful.

## 13. Interview Questions
1. **Q: What are the types of inheritance?** A: Single (one parent), multilevel (a chain), hierarchical (one parent, many children), multiple (many parents), and hybrid (combination — where the diamond appears).
2. **Q: Why does Java ban multiple class inheritance?** A: It creates ambiguity — two parents with the same method (which wins?) and the diamond's duplicate state — and is error-prone. Java's design: single implementation inheritance (classes) + multiple type inheritance (interfaces).
3. **Q: TRICKY — Is `class B extends A`, `class C extends B` multiple inheritance?** A: No — that's *multilevel* inheritance (a chain). Multiple requires *two or more direct parents* (`class D extends B, C`).
4. **Q: What is the diamond problem?** A: When `D extends B, C` and both `B`, `C` extend `A` — `D` may inherit two copies of `A`'s state (C++) and ambiguous method definitions; the shape looks like a diamond (A at top, B/C sides, D bottom).
5. **Q: How does Java handle multiple *type* inheritance?** A: Interfaces — a class `implements` any number of interfaces; the diamond is resolved because interfaces have no state and duplicate default methods must be overridden explicitly.
6. **Q: How does C++ resolve the diamond?** A: `virtual` inheritance (`class B : virtual public A`) merges the shared `A` subobject into one instance, eliminating duplicate state at the cost of indirection; non-virtual multiple inheritance keeps two `A` copies (usually a bug).
7. **Q: How does Python resolve the diamond?** A: C3 linearization produces a single deterministic MRO (method resolution order), and `super()` follows it — so method chains are well-defined (e.g., `D → B → C → A → object`).
8. **Q: SCENARIO — Design a `FlyingCar`. Multiple or composition?** A: Prefer composition: `FlyingCar { Car car; Aircraft aircraft; fly()/drive() delegate }` — avoids the diamond entirely. If you must, mixins in Python or interfaces in Java (`Drivable`, `Flyable`) give the typing without implementation ambiguity.
9. **Q: PRACTICAL — When is multiple inheritance *worth it* (in Python)?** A: Mixins — small, orthogonal behavior chunks (`LoggingMixin`, `CacheMixin`) combined via MRO; each mixin is simple and has no state conflicts. Beyond mixins, it's usually a smell.
10. **Q: TRICKY — What's the difference between hierarchical and multilevel?** A: Hierarchical = many *children* of one parent (a fan-out: `B` and `C` both extend `A`); multilevel = a *chain* of parents (`C extends B extends A`). Both are single-inheritance-safe; they're different shapes.
11. **Q: Why do interface default methods make Java's diamond safe?** A: Interfaces carry no instance state, so there's no duplicate-state risk; if two interfaces define the same default method, the implementing class must override it (or pick via `I.super.m()`), making every conflict explicit at compile time.
12. **Q: SCENARIO — Your base class chain is 6 levels deep. Problems?** A: Fragile base class (a change at the top breaks everything), hard to trace overrides, test setup complexity, and likely "reuse by inheritance" misuse — refactor toward interfaces + composition, flatten to 2-3 levels.
13. **Q: Is C++ multiple inheritance ever the *right* answer?** A: Rarely — mixin-like interface inheritance (`class Foo : public IFoo`) is the norm; full multiple implementation inheritance is justified only when the two parents are truly orthogonal and the diamond is controlled with virtual inheritance. Most C++ guidelines say prefer composition.
14. **Q: What does `class D extends B, C` in Python actually call?** A: `D`'s MRO is computed by C3 (linearization) — typically `[D, B, C, A, object]` (left-to-right, parents-first); `D.m()` searches that order; `super()` in `B` jumps to `C`, not to `object` — the "cooperative super" behavior.
15. **Q: PRODUCTION — The Go/Rust take?** A: Go has no class inheritance (only interfaces + embedding/composition); Rust has no inheritance at all (traits + composition). The industry trend away from multiple — and even single — implementation inheritance confirms the "prefer interfaces + composition" guidance.

## 14. Follow-Up Questions
1. **Q: What is the "dreaded diamond" in C++ exactly?** A: `D` has two paths to `A` (D→B→A and D→C→A); without `virtual` inheritance, `D` contains *two* `A` subobjects (ambiguous state and casting); with virtual inheritance, one shared `A` subobject is used.
2. **Q: What is Python's "cooperative multiple inheritance"?** A: Classes designed so `super()` chains cooperate along the MRO — each class calls `super().method()` expecting the next in the linearization, enabling mixins to compose cleanly. Breaking the chain (calling `Parent.method()` directly) breaks it.
3. **Q: When is a "hybrid" hierarchy a code smell?** A: Nearly always — if you're combining multilevel + multiple, you're likely modeling a relationship better expressed as composition or interfaces; the diamond's ambiguity almost never matches a real domain need.
4. **Q: Do sealed classes (Java 17) change inheritance-type design?** A: Yes — `sealed` restricts *which* classes can extend, giving controlled single/hierarchical inheritance with exhaustive pattern matching — the modern safe shape.

## 15. Coding Example
```java
// The three SAFE types in Java, plus interfaces for "multiple"
interface Movable { void move(); }
interface Audible { void honk(); }

class Vehicle { protected int speed; public void move() { speed += 5; } }         // single base
class Car extends Vehicle { public void honk() { System.out.println("beep"); } }  // single
class Suv extends Car {}                    // multilevel: Vehicle → Car → Suv
class Bus extends Vehicle { }               // hierarchical sibling of Car

class AmphibiousCar extends Car implements Movable, Audible {   // single class + multiple interfaces
    public void swim() { System.out.println("swimming"); }
}
```
```cpp
// C++ multiple inheritance (use carefully!)
struct Vehicle { int speed = 0; virtual ~Vehicle() = default; };
struct Boat { virtual void sail() {} };
struct Amphibian : Vehicle, Boat {   // TWO parents (multiple)
    void drive() { speed += 5; }
};
// Diamond + virtual inheritance:
struct A { int x = 1; };
struct B : virtual A {};
struct C : virtual A {};
struct D : B, C {};   // D has ONE shared A (via virtual) — D.x unambiguous
```
```python
# Python multiple inheritance with MRO
class A:
    def greet(self): print("A"); 
class B(A):
    def greet(self): print("B"); super().greet()
class C(A):
    def greet(self): print("C"); super().greet()
class D(B, C): pass
D().greet()          # B, C, A  (MRO: D → B → C → A → object) — cooperative super
print(D.__mro__)     # shows the linearization
```

## 16. Industry Usage
- **Java**: single class inheritance is universal; interface "multiple" is everywhere (a Spring service `implements Service, InitializingBean`). The JDK's own `HashMap extends AbstractMap implements Map, Cloneable, Serializable` is the canonical two-axis design.
- **Python (Django)**: `class ListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView)` — multiple inheritance of mixins is the framework's core idiom (carefully designed, cooperative MRO).
- **C++**: virtual bases in rare but real cases (e.g., `iostream` uses `virtual` `basic_ios`); most production C++ uses single inheritance + pure-interface classes.
- **Android/Kotlin**: single class inheritance (framework bases) + interface "multiple"; Kotlin forbids deep class hierarchies by convention.
- **Everywhere**: the practical rule — single class chain + multiple interfaces/mixins; full multiple class inheritance is a legacy or specialized feature, not a default.

## 17. References
- Bjarne Stroustrup, *The C++ Programming Language* — multiple inheritance, virtual bases.
- The Python Tutorial, "Multiple Inheritance" and "The Python 2.3 Method Resolution Order": https://docs.python.org/3/tutorial/classes.html
- Java Language Specification, §8.1.4 (Superclasses and Subclasses), §8.4.8 (overriding): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html
- GeeksForGeeks, "Types of Inheritance in Java": https://www.geeksforgeeks.org/inheritance-in-java/
- C++ reference on virtual inheritance: https://en.cppreference.com/w/cpp/language/class#Virtual_base_classes

## 18. Cheat Sheet
- Single: one parent. Multilevel: a chain. Hierarchical: one parent, many kids. Multiple: many parents. Hybrid: mix → diamond.
- Java classes: single only. Multiple *type* via interfaces.
- C++: multiple allowed; use `virtual` inheritance to merge shared bases.
- Python: multiple allowed; C3 MRO resolves deterministically; `super()` follows MRO.
- Diamond = duplicate state + ambiguous methods (C++ non-virtual) or explicit-resolution (Java/Python).
- Deep multilevel = fragile base; keep 2-3 levels.
- Prefer composition/interfaces for anything that smells like multiple.

## 19. Quiz
1. `class C extends B`, `class B extends A` is: a) multiple b) multilevel c) hierarchical d) hybrid → **b**
2. `class B extends A`, `class C extends A` is: a) multilevel b) hierarchical c) multiple d) single → **b**
3. Java classes support: a) multiple inheritance b) single only c) hybrid d) unlimited → **b**
4. The diamond problem arises in: a) single b) hierarchical c) hybrid/multiple d) multilevel-only → **c**
5. Python resolves the diamond via: a) manual casting b) C3 MRO c) vtable d) none → **b**
6. True or False: Interfaces give Java multiple type inheritance. → **True**

## 20. Flashcards
- **Q: Five types of inheritance?** → **A:** Single, multilevel, hierarchical, multiple, hybrid.
- **Q: Which types are Java-class-safe?** → **A:** Single, multilevel, hierarchical (all single-parent forms).
- **Q: What causes the diamond?** → **A:** Hybrid inheritance — D extends B,C where both extend A.
- **Q: Java's answer to multiple?** → **A:** Interfaces (multiple type inheritance, no state, explicit default-method conflict resolution).
- **Q: C++'s answer?** → **A:** Multiple inheritance with `virtual` inheritance to merge shared bases.
- **Q: Python's answer?** → **A:** C3 linearization MRO; `super()` follows it.
- **Q: How deep should chains be?** → **A:** 2-3 levels; deeper → fragile base.

## 21. Revision
Inheritance has five shapes: single (one parent), multilevel (chain), hierarchical (many kids), multiple (many parents), and hybrid (mix → diamond). Java classes allow only the single-parent forms and achieve "multiple" via interfaces; C++ allows full multiple with `virtual` inheritance to merge shared bases; Python resolves ambiguity deterministically via C3 MRO and cooperative `super()`. The diamond's danger is duplicate state + ambiguous methods. First-30-seconds answers: "single/multilevel/hierarchical are safe; multiple/hybrid cause the diamond, which Java solves with interfaces."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Types of inheritance?" | Formal Definition / Section 13 |
| "Why no multiple inheritance in Java?" | Interview Q2 / Section 4 |
| "Multilevel vs multiple?" | Interview Q3 |
| "What is the diamond problem?" | Interview Q4 / Section 9 |
| "How do Java/C++/Python resolve it?" | Interview Q5–Q7 |
| "Design a FlyingCar?" | Interview Q8 |
| "When is Python MI worth it?" | Interview Q9 |
| "Deep hierarchy problems?" | Interview Q12 |
