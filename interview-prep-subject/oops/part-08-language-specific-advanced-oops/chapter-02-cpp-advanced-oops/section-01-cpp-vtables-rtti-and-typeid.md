# C++ v-Tables, RTTI and `typeid`

> **TL;DR**: A C++ class with at least one `virtual` function carries a hidden **vptr** pointing to a per-class **v-table** of function pointers — that table is what makes `p->f()` dispatch to the *dynamic* type at runtime — and **RTTI** (`typeid`, `dynamic_cast`) is the runtime type information that lets you identify and safely downcast polymorphic objects.

## 1. Why Does This Exist?
C++ is statically typed: the compiler decides at compile time which function a `obj.f()` call resolves to based on the *static type*. But polymorphism requires the *opposite*: when you hold a `Shape*` pointing to a `Circle`, calling `draw()` must run `Circle::draw`, not `Shape::draw` — decided only at runtime when the actual object type is known. A **v-table** (virtual function table, vtbl) is the mechanism that makes this "late binding" fast and cheap: each polymorphic class gets an array of function pointers, one per virtual method, and a **vptr** inside every object points to its class's table. Similarly, **RTTI** (Run-Time Type Information) exists because sometimes you *need* the dynamic type as data — to check `typeid`, or to safely downcast with `dynamic_cast` — and that information must be stored somewhere the runtime can reach. Both exist to give C++ runtime polymorphism and type introspection while keeping the zero-cost-abstraction promise (a virtual call is just one indirect function call).

## 2. How Does It Work?
At a glance:
- A class with ≥1 `virtual` member function (or a virtual destructor) is **polymorphic**: it gets a hidden `vptr` member and a **v-table** in static storage.
- The v-table is an array of function pointers in the order of virtual method declaration: index 0 often holds `typeinfo` (RTTI), then one slot per virtual method.
- Each object's `vptr` points to its *class's* table; when a derived class overrides `f`, the derived table's slot for `f` points to `Derived::f`.
- Calling `p->f()` compiles to: load `vptr` → load function pointer at slot k → indirect call.
- **RTTI** is the `std::type_info` object (address) stashed in the v-table; `typeid(x)` returns a `const type_info&`; `dynamic_cast<T*>(p)` walks the inheritance graph using this info to validate and adjust the pointer.

## 3. When Is It Used?
- **Calling virtual methods through base pointers/references** — the entire point of `Shape*` + `draw()`.
- **Overriding with `override`** — the compiler checks the v-table slot is really overridden.
- **`typeid(*p).name()`** — debug logging, crash dumps, serialization type tags.
- **`dynamic_cast<Derived*>(basePtr)`** — safe downcasting in frameworks when a base pointer might be a specific derived type (e.g., a UI toolkit's `QWidget::findChild`).
- **Virtual destructors** — `delete basePtr;` must run the derived destructor through the v-table.
- **RTTI in virtual inheritance** — resolving the location of shared subobjects at runtime.

## 4. Why Wasn't Another Approach Chosen?
Alternatives:
- **Static dispatch only (no virtuals)**: no runtime cost, but zero substitutability — a `Shape*` can't behave like a `Circle`. Rejected because OOP requires it.
- **Fat pointers / closures per object (like Smalltalk's message passing)**: store a pointer to a behavior dict in *every* object — more indirection and bigger objects. C++ chose a **single vptr + shared v-table** to keep objects small and dispatch one level of indirection.
- **Runtime type interpretation (like Java reflection)**: Java keeps a full `Class` object per class with heavy runtime checks. C++ keeps only the minimal `type_info` + v-table so polymorphic calls stay near-zero-cost.
- **Function pointers stored per-object**: each instance would carry its own copy of the table — wasteful. Sharing the table per class amortizes it to one vptr per object.
- **Duck typing (Python)**: no type enforcement, runtime method lookup per call — C++ rejects this for performance and type safety.

## 5. Intuition
Think of the v-table as a **department store directory**. The building (base class `Shape`) has a directory listing "where to find each department (virtual method)." Each floor (derived class) has its *own* directory copy that points to *its* departments. Every shopper (object) carries one card — the floor indicator (vptr) — that says which floor they're on. When you ask "where's drawing?" (`p->draw()`), you don't walk a fixed path; you check the card, go to the floor's directory, and follow the listed location. That's why `Circle` (floor 2's directory) sends you to the circle drawing studio, while `Square` (floor 3) sends you elsewhere — same question, different answer depending on where the card says you are.

## 6. Real-World Analogy
A **call center with skill-based routing**: customers call a single number (a base pointer). The system looks up "what kind of specialist handles this call?" — the customer's profile (vptr) points to their account type (v-table). A "premium customer" profile routes to the premium desk (`Premium::support`), a "business customer" to the business desk — same phone number, different desk, chosen at the moment of the call. If the system instead routed everyone to the first desk (static binding), the routing system would be pointless. RTTI is the *badge scanner*: occasionally the system checks "is this person actually a premium member?" (`dynamic_cast`) to unlock premium-only features, or asks "what account type is this?" (`typeid`).

## 7. Formal Definition
- **vptr/v-table**: The C++ standard doesn't mandate an implementation, but the de-facto Itanium ABI is: an object of a polymorphic class begins with a `vptr` (`void**`), pointing to an array whose element 0 is a pointer to the class's `typeinfo`, followed by one `void(*)()` per virtual function in declaration order. Derived classes build their table by copying the base's and overriding entries for overridden functions. Multiple inheritance yields multiple vptrs/v-tables (one per base subobject).
- **RTTI**: `std::type_info` — the runtime descriptor; `typeid(expr)` returns `const std::type_info&` (for polymorphic lvalues it uses the *dynamic* type; otherwise the static type). `dynamic_cast<T>(v)` performs a checked conversion: for `T*` returns `nullptr` on failure; for `T&` throws `std::bad_cast`; requires the operand type to be polymorphic (has a vptr). The v-table's typeinfo slot is what makes `typeid(*p)` and `dynamic_cast` possible.
- **Virtual destructor**: `virtual ~Base() = default;` — required so `delete basePtr` dispatches to the most-derived destructor; without it, deleting through a base pointer is undefined behavior (UB).

## 8. Example
```cpp
#include <iostream>
#include <typeinfo>

class Shape {
public:
    virtual void draw() const { std::cout << "Shape\n"; }   // virtual => polymorphic
    virtual ~Shape() = default;                             // virtual dtor: delete via base is safe
};

class Circle : public Shape {
public:
    void draw() const override { std::cout << "Circle\n"; } // overrides the v-table slot
};

class Square : public Shape {
public:
    void draw() const override { std::cout << "Square\n"; }
};
```
Trace the call `Shape* s = new Circle(); s->draw();`:
1. Compiler emits `s->draw()` as: load `s.vptr` (the object's first word), load the function pointer at slot (typeinfo + offset of draw), indirect-call it.
2. `s`'s vptr points to `Circle`'s v-table, whose `draw` slot holds `Circle::draw`.
3. Output: `Circle` — even though `s` has static type `Shape*`, dispatch used the dynamic type.

RTTI example:
```cpp
Shape* s = new Circle();
std::cout << typeid(*s).name();          // "Circle" (dynamic type via v-table)
std::cout << (typeid(*s) == typeid(Circle));   // true
Circle* c = dynamic_cast<Circle*>(s);    // non-null: s really is a Circle
Square* sq = dynamic_cast<Square*>(s);   // nullptr: s is not a Square
```

## 9. Internal Working
1. **Class layout** (Itanium ABI, x86-64): `struct Circle { void* vptr; /* Circle data */ };` — vptr first, so `Shape*` and `Circle*` addresses coincide for single inheritance.
2. **v-table construction**: compiler emits one static v-table per class; `Circle`'s table: `[&typeinfo(Circle), &Circle::draw, &Circle::~Circle]`. Base's `Shape` table holds `&Shape::draw`.
3. **Object construction**: constructor sets `vptr = &Circle::vtable` (most-derived type) — that's why you should never call virtual functions from a base-class constructor (the vptr still points to the base's table during base construction).
4. **Dispatch**: `p->draw()` → `(*(p->vptr + drawOffset))(p)` — the "this" pointer is passed as the first argument, which is why member functions compile to ordinary functions with a hidden `this` param.
5. **RTTI lookup**: `typeid(*p)` reads `typeinfo` from the v-table's slot 0 (the pointer stored at `p->vptr[0]`); equality compares the *addresses* of the `type_info` singletons.
6. **dynamic_cast**: for single inheritance it's basically a v-table typeinfo comparison + possible pointer adjustment; for multiple/virtual inheritance it walks the class's inheritance graph (RTTI contains cross-cast offsets) to find/validate the target subobject — more expensive.

## 10. Time Complexity
- Virtual call: **O(1)** — one extra memory load (vptr → function ptr) vs a direct call. On modern CPUs the table is hot in cache; the cost is ~a few ns, not the "10x slower" myth (it's often 0-2% overhead).
- `typeid(x).name()`: O(1) — reads the typeinfo pointer.
- `typeid` equality: O(1) — pointer comparison of the type_info singleton addresses.
- `dynamic_cast<T*>` single inheritance: O(1) (typeinfo compare). Multiple/virtual inheritance: **O(depth of graph)**, may traverse the inheritance chain — measurable but rare in hot paths.
- `sizeof` impact: +8 bytes vptr per object (single inheritance). Empty class with virtuals: still 8 bytes (vptr) + padding.

## 11. Advantages
- Enables genuine runtime polymorphism (the heart of OOP) at near-zero cost.
- Substitutability: a base pointer/reference can drive any derived implementation without callers knowing the type (LSP).
- `typeid` gives safe, cheap type introspection without reflection machinery.
- `dynamic_cast` provides checked downcasting — returning `nullptr`/throwing instead of UB (unlike a raw `static_cast` downcast).
- Overriding with `override` gets compile-time verification that a method really overrides.

## 12. Disadvantages
- Memory: +1 vptr per object; each class keeps a v-table in static storage.
- Virtual calls can't be inlined/devirtualized in all cases (though the compiler can devirtualize when the dynamic type is provable).
- `dynamic_cast` on multiple/virtual inheritance has real cost and can be a sign of design smell (LSP violations needing type checks).
- **UB traps**: non-virtual destructor + base-pointer delete = UB; calling virtuals in constructors/destructors dispatches to the *current* construction level, not the final type (subtle bugs).
- RTTI can be disabled (`-fno-rtti`), breaking `typeid`/`dynamic_cast` on polymorphic types.
- Object slicing: copying a `Circle` into a `Shape` by value drops the vptr → the copy behaves like `Shape` (no v-table pointer for the derived).

## 13. Interview Questions
1. **Q: What is a v-table and how does virtual dispatch work?** A: Each polymorphic class has a static array of function pointers (one per virtual method); each object carries a vptr to its class's table; a virtual call loads vptr → slot → indirect call, so dispatch follows the object's dynamic type.
2. **Q: Which classes get a vptr?** A: Any class with at least one virtual function (including a virtual destructor), directly or inherited.
3. **Q: What's the memory cost of virtual functions?** A: One vptr per object (typically 8 bytes) plus a v-table per class (static). `sizeof` grows by vptr + padding; the table itself is shared across instances.
4. **Q: Why must the destructor be virtual when deleting via a base pointer?** A: `delete basePtr` needs to call the most-derived destructor through the v-table; without a virtual dtor, only the base dtor runs (UB — derived resources leak).
5. **Q: What's the difference between static and dynamic type?** A: Static type = compile-time declared type (`Shape*`); dynamic type = actual object type (`Circle`). Virtual dispatch and `typeid(*p)` use the dynamic type.
6. **Q: What is RTTI and how is it implemented?** A: Run-Time Type Information = the `std::type_info` descriptors (with the class name) referenced from the v-table; `typeid` returns it, `dynamic_cast` uses it.
7. **Q: `typeid(*p)` vs `typeid(p)`?** A: `typeid(*p)` on a polymorphic lvalue returns the *dynamic* type (`Circle`); `typeid(p)` returns the static type of the expression (`Shape*`). `typeid(p)` never follows the pointer.
8. **Q: When does `dynamic_cast` return `nullptr` vs throw?** A: Pointer form `dynamic_cast<Derived*>(p)` returns `nullptr` on failure; reference form `dynamic_cast<Derived&>(r)` throws `std::bad_cast` (can't represent null).
9. **Q: When is `dynamic_cast` not allowed?** A: The operand must be polymorphic (have a vptr); casting to a non-polymorphic type or from a non-polymorphic type is a compile error.
10. **Q: `static_cast` vs `dynamic_cast` for downcasting?** A: `static_cast` is unchecked and cheap — UB if the actual type doesn't match; `dynamic_cast` checks at runtime and is safe (nullptr/bad_cast) but more expensive.
11. **Q: Why shouldn't you call a virtual function in a constructor?** A: During base construction the vptr points to the base's v-table, so the call dispatches to the *base* version, not the final derived override — surprising results.
12. **Q: What is object slicing?** A: Copying a derived object into a base object by value copies only the base subobject and drops the vptr; the copy behaves as the base type. Use pointers/references to avoid it.
13. **Q: What does the Itanium ABI's v-table look like?** A: Slot 0 = pointer to `typeinfo`, then one function pointer per virtual method in declaration order; each class builds its table by copying the base's and replacing overridden entries.
14. **Q: Can the compiler devirtualize virtual calls?** A: Yes — if it can prove the dynamic type (e.g., the object is constructed in the same function or the final-class override is known), it inlines the direct call.
15. **Q: What's the cost difference between `virtual` and non-virtual?** A: A virtual call is one extra indirect load + indirect branch; typically ~1-2% overhead in practice, not the "huge" cost some assume.
16. **Q: What happens with `override` and `final`?** A: `override` makes the compiler verify the method really overrides a base virtual (else error); `final` on a method/class prevents further overriding/inheritance and enables devirtualization.
17. **Q: How does multiple inheritance affect the vptr?** A: Each base subobject with virtuals gets its own vptr/v-table; the object has multiple vptrs, and this-pointers are adjusted when switching between base views (that's why the cast/adjustment logic exists).
18. **Q: What's the difference between `typeid` and `dynamic_cast` use cases?** A: `typeid` answers "what type is this?" (identity check, cheap); `dynamic_cast` answers "can I use it as type T?" (checked conversion, may walk the hierarchy).

## 14. Follow-Up Questions
1. **Q: Why is the typeinfo at the start of the v-table?** A: So `typeid(*p)` and the first steps of `dynamic_cast` can read it in O(1) from the same cache line as the dispatch pointers — a design choice for performance.
2. **Q: What is the "most-derived type" problem in construction/destruction?** A: During a base ctor, the object is *not yet* a derived object, so the vptr is temporarily the base's; calling virtuals there executes base versions. Destruction does the reverse (vptr resets as each dtor runs).
3. **Q: Why does the address of a base pointer sometimes differ from the derived pointer in MI?** A: With multiple inheritance, the derived object is laid out as several base subobjects at different offsets; the base pointer points to *its* subobject, so converting requires adjusting the address by the known offset.
4. **Q: What are "adjuster thunks"?** A: Small code stubs the compiler emits so a virtual function can fix up `this` when called through a different base subobject in MI — the thunk adjusts the pointer, then jumps to the real function.
5. **Q: How do `dynamic_cast` and virtual inheritance interact?** A: With virtual inheritance there's a shared base subobject; the cast must locate it via runtime offsets stored in the RTTI (vtordisp/thunk data), making the cast more expensive than the single-inheritance O(1) case.

## 15. Coding Example
```cpp
#include <iostream>
#include <typeinfo>
#include <memory>

class Payment {
public:
    virtual void charge() const = 0;          // pure virtual: abstract class
    virtual ~Payment() = default;             // virtual dtor for safe delete
};
class Card : public Payment {
public:
    void charge() const override { std::cout << "card charge\n"; }
    void cancelHold() const { std::cout << "cancel hold\n"; }
};
class Wallet : public Payment {
public:
    void charge() const override { std::cout << "wallet charge\n"; }
};

void process(Payment& p) {
    p.charge();                                // dynamic dispatch via v-table
    if (Card* c = dynamic_cast<Card*>(&p)) {   // safe downcast; null if not a Card
        c->cancelHold();                       // Card-only capability
    }
}

int main() {
    Card c; Wallet w;
    process(c);                                // prints "card charge\ncancel hold\n"
    process(w);                                // prints "wallet charge" (dynamic_cast fails silently)

    Payment* p = new Card();
    std::cout << typeid(*p).name() << "\n";    // dynamic type: "Card"
    std::cout << (typeid(*p) == typeid(Card)) << "\n";  // true
    std::cout << (typeid(p) == typeid(Payment*)) << "\n"; // true: static type of expression
    delete p;                                  // safe: virtual dtor runs Card's

    // RAII alternative to raw delete:
    std::unique_ptr<Payment> up = std::make_unique<Card>();
    up->charge();                              // dispatch still dynamic through unique_ptr
}
```

## 16. Industry Usage
- **Qt/GTK UI frameworks**: every widget class is polymorphic; `qobject_cast` (Qt's `dynamic_cast` equivalent) is used constantly to identify and convert widget types.
- **Game engines (Unreal, Unity IL2CPP, Godot)**: `UObject`/`AActor` hierarchies rely on v-tables for per-frame dispatch; engine code uses `Cast<AFoo>` (Unreal's RTTI) to downcast.
- **LLVM**: the polymorphic instruction/value hierarchy (`Value`, `Instruction`) uses v-tables; LLVM's `isa`/`cast`/`dyn_cast` are *compiled-time checked* RTTI alternatives that avoid `dynamic_cast` cost.
- **C++ trading systems / infra (Jane Street, DRW)**: `dynamic_cast` is avoided in hot loops (cost, design smell); design favors v-table dispatch and `std::visit` over type checks.
- **Boost/ABI**: Itanium ABI governs v-table layout across GCC/Clang/MSVC interop; ABI-stable libraries (ABI-tagged virtuals in libstdc++) use it.

## 17. References
- *Itanium C++ ABI* (itanium-cxx-abi.github.io/cxx-abi) — the de-facto v-table/RTTI layout for GCC/Clang.
- ISO/IEC 14882:2020 (C++20), §7.6.1.7 "typeid", §8.5.1.9 "dynamic_cast", §11.7.2 "Virtual functions", §11.7.4 "Virtual base classes".
- cppreference.com: *virtual function*, *dynamic_cast*, *typeid*, *std::type_info*.
- Scott Meyers, *Effective C++*, Item 7 (virtual destructors), Item 31 (minimize dependencies), Item 33/34 (virtual vs hiding).
- Andrei Alexandrescu, *Modern C++ Design* (policy-based design and RTTI alternatives).
- Jonathan Boccara / Bjarne Stroustrup, *A Tour of C++* (polymorphism chapter).

## 18. Cheat Sheet
- Polymorphic ⇔ has ≥1 virtual function ⇔ gets vptr (1 word) + shared v-table.
- Virtual call = load vptr → load slot → indirect call; O(1), ~0-2% typical overhead.
- v-table slot 0 = `typeinfo`; then one pointer per virtual method, declaration order.
- `typeid(*p)` = dynamic type (via vptr); `typeid(p)` = static type of expression.
- `dynamic_cast<T*>` → nullptr on fail; `dynamic_cast<T&>` → throws `std::bad_cast`; requires polymorphic operand.
- `static_cast` downcast = unchecked (UB on wrong type); `dynamic_cast` = checked.
- Virtual destructor mandatory when deleting via base pointer (else UB).
- Never call virtuals in constructors/destructors (vptr is the base's during construction).
- Slicing: copying by value drops the vptr → base behavior.
- `override`/`final` → compiler-checked overriding + devirtualization opportunities.
- MI: multiple vptrs + `this` adjustment via thunks; dynamic_cast cost grows with the graph.

## 19. Quiz
1. Which class gets a vptr? a) Any class b) One with ≥1 virtual function c) Only abstract classes d) Only classes with `final` → **b**
2. `Shape* s = new Circle(); s->draw();` calls (draw is virtual): a) `Shape::draw` b) `Circle::draw` c) Compile error d) UB → **b**
3. Deleting a `Derived` through a `Base*` without a virtual destructor is: a) Fine b) Slicing c) Undefined behavior d) A warning only → **c**
4. `typeid(*p)` where `p` is `Shape*` pointing to `Circle` returns the typeinfo of: a) `Shape` b) `Circle` c) `Shape*` d) `Object` → **b**
5. `dynamic_cast<Square*>(p)` where p points to a `Circle` returns: a) A `Square*` b) `nullptr` c) Throws `std::bad_cast` d) UB → **b**
6. `dynamic_cast` on a reference on failure: a) Returns null b) Throws `std::bad_cast` c) Throws `std::exception` d) Is UB → **b**
7. Calling a virtual function inside a base-class constructor: a) Dispatches to derived b) Dispatches to the base version c) Is a compile error d) Throws → **b**
8. Object slicing happens when: a) Passing by pointer b) Copying a derived object into a base object by value c) Using `dynamic_cast` d) Virtual inheritance → **b**
9. A virtual call's runtime cost is: a) O(n) b) O(log n) c) O(1) extra indirect load d) Free → **c**
10. The v-table's slot 0 typically holds: a) The first virtual method b) A pointer to `typeinfo` c) The vptr d) The class size → **b**

## 20. Flashcards
- **Q: What makes a class polymorphic in C++?** → **A:** Having at least one virtual function (or virtual destructor) → gets a vptr + v-table.
- **Q: How does `p->f()` dispatch?** → **A:** Load vptr → load function pointer at slot → indirect call (dynamic type decides).
- **Q: Why virtual destructor?** → **A:** So `delete basePtr` runs the most-derived destructor; otherwise UB.
- **Q: `typeid(*p)` vs `typeid(p)`?** → **A:** Dynamic type of the object vs static type of the expression.
- **Q: What does `dynamic_cast` return/throw on failure?** → **A:** `nullptr` (pointer) or `std::bad_cast` (reference); requires polymorphic type.
- **Q: When must you NOT call virtuals?** → **A:** In constructors/destructors (vptr is the base's during those phases).
- **Q: What is slicing?** → **A:** Copy-by-value of a derived into a base drops the vptr and behavior.
- **Q: Why can the compiler devirtualize sometimes?** → **A:** When the dynamic type is provable statically, it calls directly.

## 21. Revision
Polymorphic classes (≥1 virtual fn) carry a vptr to a static v-table: slot 0 = typeinfo, then one function pointer per virtual method. `p->f()` = load vptr → load slot → indirect call — O(1), near-zero cost, and the reason overriding works on base pointers. RTTI = `std::type_info` reachable from the v-table: `typeid(*p)` gives the dynamic type (cheap, pointer comparison for equality); `dynamic_cast<T*>` does a checked downcast → `nullptr` on failure, `T&` form throws `std::bad_cast`; the operand must be polymorphic. Rules: always make destructors virtual when deleting through bases; never call virtuals in ctors/dtors (vptr is still the base's); avoid slicing by passing pointers/references; `static_cast` downcast is unchecked/UB. In interviews, trace a `Shape*`/`Circle` dispatch, compare `typeid(*p)` vs `typeid(p)`, and explain why `dynamic_cast` costs more under multiple inheritance (subobject offset walking).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How does virtual dispatch work in C++?" | 2 / 9 Internal Working / 8 Example |
| "What is a v-table and where is it stored?" | 7 Formal Definition / 9 Internal Working |
| "What's the memory/cost of virtual functions?" | 10 Time Complexity / 12 Disadvantages |
| "Why virtual destructor?" | 13 Interview Questions |
| "`typeid(*p)` vs `typeid(p)`?" | 13 Interview Questions |
| "When does `dynamic_cast` throw vs return null?" | 13 Interview Questions |
| "Why not call virtuals in constructors?" | 13 Interview / 14 Follow-Up |
| "What is object slicing?" | 12 Disadvantages / 13 Interview |
| "Static vs dynamic type?" | 13 Interview Questions |
| "How does multiple inheritance affect vptrs?" | 13 Interview / 14 Follow-Up |
