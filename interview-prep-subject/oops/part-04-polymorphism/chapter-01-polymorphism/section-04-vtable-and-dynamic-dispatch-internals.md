# V-Table and Dynamic Dispatch Internals

> **TL;DR**: Every polymorphic object carries a hidden pointer (vptr) to its class's virtual method table (vtable) — a per-class array of function pointers; a virtual call is `*(this->vptr + slot)` (O(1)); JITs make this nearly free with inline caching and devirtualization.

## 1. Why Does This Exist?
A virtual call can't be a normal `call <address>` — the compiler doesn't know which function runs. It needs an **indirection table**: a data structure that maps "the `pay` method, slot 3" to *this class's* `pay`. The vtable is that structure. Its job: make the runtime choice (which subclass implementation) a single memory read + jump. Without it, the runtime could dispatch via huge if/switch chains (slow, unbounded), or interpreters (slow). The vtable makes dynamic dispatch both general (any subclass, loaded later) and fast (constant time), which is why nearly every OO runtime — Java (vtable/itable), C++ (vptr/vtable), Python (MRO dict lookup), Go (itab) — uses this design.

## 2. How Does It Work?
- Each **class** (not object) gets one vtable: an array of function pointers, one slot per virtual method, laid out in declaration order, with overridden slots pointing at the subclass's implementation.
- Each **object** of a polymorphic class carries a vptr (Java: the `klass` pointer in the object header; C++: a field usually at offset 0) pointing to its class's vtable.
- A virtual call `a->f()` becomes `(*a.vptr[f_slot])(a)` — read vptr, index slot, jump.
- Subclass vtables **inherit and extend** the parent's: base slots keep their positions (so the same slot means the same method across the hierarchy); new virtuals are appended.

## 3. When Is It Used?
- On **every virtual call** — unless the JIT/compiler proves the concrete type.
- Built at **class load** (Java) or compile/link (C++): once per class, shared by all instances.
- **Multiple inheritance (C++)**: multiple vptrs per object, one per polymorphic base, plus "thunk" adjustments for the `this` pointer shift.
- **Interfaces (Java/Go)**: the itable (interface method table) is used when a call resolves through an interface — possibly cached on first use.
- This design runs in hot loops of every Java/C++/Go app; its efficiency is load-bearing.

## 4. Why Wasn't Another Approach Chosen?
- *Why a table of pointers instead of an interpreted dispatch?* Pointer tables are native speed — one indirect jump — while an interpreter decodes bytecodes per call.
- *Why per-class table, not per-object table?* Per-object would waste memory (all instances of a class share behavior); sharing a per-class table is O(1) extra memory per class, O(1) space per object (one vptr).
- *Why not always direct calls + devirtualize?* Devirtualization needs proof of concrete type; the vtable is the general fallback when the type is unknown.
- *Why "slot order from base"?* Stable slot ordering lets a derived class reuse its base's vtable as a prefix — subclass dispatch of inherited methods stays correct without rebuilding tables.
- *Why inline caches?* Even a single extra indirection is too slow in hot loops; caching the last-seen target turns repeated calls into direct (inlinable) calls — a JIT-only win, hence Java's advantage over precompiled C++.

## 5. Intuition
A **call center phone tree** by department: you press the "help" option (slot), and the machine routes to *this branch's* help desk — each branch has its own staff list (vtable) hung on the same board. The menu (slot index) is identical everywhere; only the behind-the-board destination changes. Same number pressed, different real person reached — because each branch (class) filled its own board (vtable) and the phone (object) knows which board to consult. Adding a branch = one new board; the menu never changes.

## 6. Real-World Analogy
A **restaurant menu in a franchise** with "house specialty" as slot 3 on every menu. The franchise prints identical menus (base class vtable slots), but each restaurant (class) fills slot 3 with *its* specialty — Mumbai fills in curry, Kyoto fills in ramen. A customer at any franchise orders "the specialty" (virtual call, slot 3); the kitchen reads *this* restaurant's menu (vtable) and cooks the local dish. The menu template is shared; the content differs per restaurant; the customer's order needs no per-restaurant reprinting.

## 7. Formal Definition
A **virtual method table (vtable)** is a per-class array of function pointers, one entry per virtual method, with entries for inherited virtuals kept at stable positions and overrides replacing the base's pointers. Each object of a polymorphic class contains a **virtual pointer (vptr)** referencing its dynamic type's vtable. **Dynamic dispatch** resolves a virtual call by `target = *(obj->vptr + method_slot)` and invoking that pointer with `obj` as the receiver — O(1), independent of hierarchy depth. **Itable** (Java/Go) extends the idea for interface calls. **Inline caches** and **devirtualization** (JIT) replace the indirection with direct calls once the call site's behavior is observed.

## 8. Example
```cpp
#include <iostream>
struct Shape {                        // polymorphic class
    virtual double area() const { return 0; }        // slot 0
    virtual const char* name() const { return "shape"; }   // slot 1
    virtual ~Shape() = default;
};
struct Circle : Shape {
    double r;
    Circle(double x) : r(x) {}
    double area() const override { return 3.14159 * r * r; }    // replaces slot 0
    const char* name() const override { return "circle"; }      // replaces slot 1
};
int main() {
    Shape* s = new Circle(2.0);
    std::cout << s->name() << " " << s->area() << "\n";   // both resolve via *s.vptr
    delete s;
}
```
```
Memory view (64-bit):
  Circle object: [ vptr → &Circle_vtable ] [ r = 2.0 ]
  Circle_vtable: slot0 = &Circle::area    slot1 = &Circle::name    slot2 = &Shape::~Shape
  Shape_vtable:  slot0 = &Shape::area     slot1 = &Shape::name     slot2 = &Shape::~Shape
```
Same slot numbers in both tables; the object's vptr picks the right table → `circle 12.566`.

## 9. Internal Working
1. **Layout**: the compiler emits one vtable per polymorphic class, ordered by first-declaration of virtuals; overrides overwrite the inherited slot; each polymorphic object starts with a vptr (C++) or holds a klass header pointer (HotSpot JVM).
2. **Compilation of the call**: `s->area()` is `mov rax, [s]        ; load vptr`, `call [rax + 0]` — two loads + an indirect jump. Non-virtual: one direct `call`.
3. **C++ multiple inheritance**: with two polymorphic bases, the object has two vptrs; calling the second base's virtuals adjusts `this` by an offset (via small "thunk" functions) so the method receives the right subobject address.
4. **Java interface calls**: the receiver's klass has an itable; interface methods are looked up by index — HotSpot caches the resolved itable entry on first use to avoid repeated scans.
5. **JIT**: observes that this call site only ever sees `Circle` → replaces the vtable lookup with a direct call to `Circle::area`, inlines it if beneficial; a site that becomes polymorphic reverts (megamorphic guard).
6. **Static/`final`/`sealed`**: no vtable slot or a provably-fixed slot — calls compile directly; `final` classes let the JIT devirtualize even through a base reference.

## 10. Time Complexity
- Virtual call: **O(1)** — vptr load + indexed jump, independent of class depth or vtable size.
- Itable (Java) worst case: O(k) first lookup, O(1) after caching.
- Memory: O(1) per object (one vptr), O(#virtuals) per class.
- C++ virtual with multiple inheritance: O(1) + thunk overhead.

## 11. Advantages
- Constant-time dispatch regardless of hierarchy size.
- Extensible: loading a new class adds its table; old call sites untouched.
- Native speed: one indirect jump (devirtualized to zero in JIT).
- Shared tables: memory cost is tiny (one pointer per object).
- Enables interfaces, frameworks, DI, callbacks.

## 12. Disadvantages
- Objects grow a vptr (C++ +8 bytes on x86-64 per polymorphic base).
- Indirect call isn't inlineable in C++ (pre-JIT) — hot-loop concern.
- The vtable may be paged in on first virtual call (cache miss).
- JIT devirtualization is heuristic — worst-case behavior can surprise.
- Exposes an implicit ABI: library versioning breaks if vtable layout changes.

## 13. Interview Questions
1. **Q: What is a vtable?** A: A per-class array of function pointers, one slot per virtual method; overrides replace inherited slots, keeping slot numbers stable. Objects carry a vptr to their class's vtable.
2. **Q: How does a virtual call actually execute?** A: `mov rax,[obj]` (vptr) → `call [rax + slot*8]` — an indirect call through the vtable; O(1), no hierarchy scan.
3. **Q: TRICKY — Does vtable size grow with the hierarchy or the class?** A: With the class's own declared+inherited virtuals — not with the number of subclasses. Each subclass gets its own table, but a subclass doesn't expand its ancestors' tables.
4. **Q: Where is the vptr in C++?** A: Usually at offset 0 of the object (impl-defined, but standard ABI places it first), giving the object its extra 8 bytes; multiple polymorphic bases mean multiple vptrs.
5. **Q: SCENARIO — Two classes, 10 virtual methods each; object of each costs how much?** A: One vptr per object (8 B each); two vtables (10 pointers each) shared by all instances of each class — memory is per-class and per-object (vptr), not per-method-per-object.
6. **Q: How do interfaces dispatch in Java?** A: Via itables — a second, lazily-resolved table on the class; HotSpot resolves and caches interface entries, then dispatches by slot. Faster than scanning all methods each call.
7. **Q: PRODUCTION — Why would adding a virtual to a C++ class break an old binary?** A: The vtable layout/ABI changes (new slot, possible vptr shifts), so code compiled against the old header calls the wrong slots — the source of ABI-compatibility warnings when adding virtuals to shipped classes.
8. **Q: What is an inline cache?** A: The JIT records the last target type at a call site; if the same type recurs, it does a type-check + direct call (skip the vtable) — monomorphic fast path, reverting to vtable on type change.
9. **Q: What is megamorphic?** A: A call site observed with many receiver types — the JIT stops caching and falls back to full vtable/itable dispatch (no direct-call optimization).
10. **Q: TRICKY — Is `final` class devirtualization safe?** A: Yes if the JIT proves no subclass exists (or the reference is to the final class); for non-final classes the JIT must insert a guard checking the actual type before skipping the vtable.
11. **Q: SCENARIO — Virtual method call in a 10-level hierarchy: how many vtable hops?** A: Exactly one — the object's vtable already contains the most-derived override; dispatch cost is independent of depth (that's the whole point of the table).
12. **Q: Can a subclass call its parent's virtual explicitly?** A: Yes — `super.f()` (Java) / `Base::f()` (C++) — a direct call bypassing dispatch; this is how template-method hooks delegate upward.
13. **Q: PRODUCTION — Why do JVM frameworks (Spring AOP) create proxies instead of relying on the vtable?** A: They can't change your class's vtable; a generated subclass (proxy) overrides the methods and inserts interception — still dispatched through the vtable, but now the override is the proxy's.
14. **Q: What's a "thunk" in vtable terms?** A: A small adapter the compiler emits (esp. for multiple inheritance) that adjusts `this` before calling the real method, so a vtable slot can hold a function needing a different receiver address.

## 14. Follow-Up Questions
1. **Q: How does virtual inheritance interact with vtables?** A: Virtual bases get their own shared subobject; the object carries more vptrs/vbase offsets, and calls through virtual bases add one more indirection — which is why virtual inheritance is slower than non-virtual.
2. **Q: Does Python use a vtable?** A: No — Python attributes live in per-object/class dicts; method lookup walks the MRO and reads `__dict__` (cached in `__mro__` for the class). Functionally equivalent dispatch, but slower and far more flexible (monkey-patching).
3. **Q: What is an itab in Go?** A: A per-(interface, concrete-type) pair table pairing interface slots with concrete method addresses, cached — Go interface dispatch is a vtable-style lookup generated per concrete type.
4. **Q: How does HotSpot "inline" a virtual call?** A: It replaces the call with an inlined body of the most common target guarded by a type check; if the guard fails it jumps to the real virtual call — classic speculative optimization.

## 15. Coding Example
```java
import java.util.*;
public class Dispatch {
    interface Job { void run(); }                       // itable dispatch
    static final class A implements Job { public void run() { print("A"); } }
    static final class B implements Job { public void run() { print("B"); } }
    public static void main(String[] args) {
        List<Job> jobs = new ArrayList<>();
        Random r = new Random(1);
        for (int i = 0; i < 5; i++) jobs.add(r.nextBoolean() ? new A() : new B());
        for (Job j : jobs) j.run();                     // monomorphic/bimorphic site → JIT dispatches or inlines
    }
}
```
```cpp
#include <vector>
struct Op { virtual void f() const = 0; virtual ~Op() = default; };
struct Add : Op { void f() const override { /* slot 0 */ } };
struct Mul : Op { void f() const override { /* slot 0 */ } };
void run_all(const std::vector<Op*>& v) { for (auto* o : v) o->f(); }  // each → vtable slot 0
```

## 16. Industry Usage
- **HotSpot JVM**: object header `mark` + `klass` pointer; vtable + itable per class; JIT inline caches and devirtualization keep virtual calls near-free.
- **LLVM/Clang + Itanium ABI**: standard vptr-first layout on Linux; virtual inheritance adds vbase offsets; `-fno-devirtualize` exists for correctness-sensitive builds.
- **Go**: interface `itab` caching makes interface calls single-table lookups.
- **V8 (JS)**: hidden classes + inline caches are the same idea adapted to dynamic types — a direct descendant of vtable thinking.
- **High-performance C++ (Chrome, games, HFT)**: `final`/`sealed` + whole-program devirtualization (LTO) to turn polymorphic loops into direct calls.

## 17. References
- Itanium C++ ABI (vtable layout, vptr rules): https://itanium-cxx-abi.github.io/cxx-abi/abi.html
- Oracle JVM Internals — HotSpot object model (klass, vtable/itable): https://openjdk.org/groups/hotspot/
- Brian Goetz / JIT articles — inline caches and devirtualization in HotSpot.
- GeeksForGeeks, "Virtual Functions and Runtime Polymorphism in C++" (internal working): https://www.geeksforgeeks.org/virtual-functions-and-runtime-polymorphism-in-cpp/
- Scott Meyers, *Effective C++*, Item 7 (virtual destructors) — vtable/ABI implications.

## 18. Cheat Sheet
- vtable: per-class array of function pointers; slot per virtual.
- vptr: per-object pointer to the class's vtable (first field, C++).
- Virtual call = `call [vptr + slot]` → O(1), depth-independent.
- Overrides replace inherited slots; new virtuals appended.
- Java interfaces → itable (lazy-resolved, cached).
- JIT: inline cache (monomorphic) → direct/inlined call.
- Megamorphic site → fall back to vtable dispatch.
- Multiple inheritance → multiple vptrs + thunks.
- Memory: +1 pointer per polymorphic object; +#virtuals per class.

## 19. Quiz
1. A vtable is shared by: a) every object b) every class c) every call d) process → **b**
2. Virtual call cost is: a) O(depth) b) O(n) c) O(1) d) O(log n) → **c**
3. A C++ polymorphic object's vptr lives: a) at end b) typically offset 0 c) heap d) stack → **b**
4. Interface dispatch in Java uses: a) itable b) virtual inheritance c) reflection d) macros → **a**
5. Megamorphic call sites: a) inline caches work great b) fall back to vtable c) error d) stack overflow → **b**
6. True or False: Adding a virtual to a C++ class can break ABI. → **True**

## 20. Flashcards
- **Q: vtable contents?** → **A:** Per-class array of function pointers, one per virtual method.
- **Q: vptr?** → **A:** Per-object pointer to its class's vtable (typically first field).
- **Q: Virtual call cost?** → **A:** O(1) indirect jump via vtable.
- **Q: Java interface dispatch?** → **A:** itable, lazy-resolved and cached.
- **Q: Inline cache?** → **A:** JIT-cached monomorphic target → direct call.
- **Q: Megamorphic?** → **A:** Many receiver types → vtable fallback.

## 21. Revision
Dynamic dispatch = per-class vtable (one function-pointer slot per virtual, overrides replacing inherited slots) + per-object vptr. A call compiles to `call [vptr+slot]` — O(1) regardless of hierarchy depth. C++ places the vptr first in the object (multiple bases → multiple vptrs + thunks); Java uses klass vtables plus itables for interfaces; Go itabs cache per interface-concrete pairs. JITs add inline caches so monomorphic sites devirtualize to direct/inlined calls; megamorphic sites fall back. Memory: one pointer per polymorphic object. First-30-seconds answer: "vtable = per-class slot table; object's vptr indexes it; one indirect jump, JIT devirtualizes hot monomorphic sites."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a vtable / how does dispatch work?" | Interview Q1–Q2 / Section 8–9 |
| "Vtable size and memory cost?" | Interview Q3, Q5 / Section 10 |
| "Why does adding a virtual break ABI?" | Interview Q7 |
| "What is an inline cache?" | Interview Q8 |
| "What is megamorphic?" | Interview Q9 |
| "Can final classes devirtualize?" | Interview Q10 |
| "Interface dispatch in Java?" | Interview Q6 / Section 9 |
| "Multiple inheritance dispatch?" | Interview Q14 / Section 9 |
