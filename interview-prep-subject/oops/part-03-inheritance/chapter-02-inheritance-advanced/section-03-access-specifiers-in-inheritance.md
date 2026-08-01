# Access Specifiers in Inheritance

> **TL;DR**: Inheritance hands a subclass a different "key ring" to the parent's members — Java's `protected` (package + subclasses, via own `this`), package-private (package only, *not* inherited across packages), and `public` (everyone); C++ adds the third dimension where the *inheritance kind itself* (`public`/`protected`/`private`) rescopes what the subclass re-exposes.

## 1. Why Does This Exist?
When you inherit, you get access to the parent's members — but *how much* access and *what you can re-expose* is a design decision that must be controlled. If subclasses could see everything (like `public`), internal implementation leaks into the hierarchy (fragile base); if they could see nothing (like `private`), inheritance would be useless for template methods and hook methods. Access specifiers in inheritance exist to define a **middle tier**: `protected` — "visible to subclasses (and the package), invisible to the world." C++ goes further: the *kind of inheritance* (`public`/`protected`/`private`) decides whether the subclass's users inherit the parent's members *at all*. Interviews ask about this because the Java `protected` rule is the single most-misremembered access rule, and C++'s inheritance-kind matrix is a classic screener for C++ roles.

## 2. How Does It Work?
**Java** — the four modifiers, from the subclass's viewpoint:
- `public` parent member → accessible from anywhere (subclass + world).
- `protected` parent member → accessible from: (a) the same package, (b) the subclass's own code (any package) — **but** only through `this`/`super` of a subclass type, not through an arbitrary parent reference.
- package-private (no modifier) parent member → accessible only within the package; a subclass in *another* package does NOT see it (it's *not* inherited in the accessible sense).
- `private` parent member → not accessible by name (exists structurally only).

**C++** — the inheritance kind *rescopes* the base's members for the derived class's *own* users:
- `class D : public B` → B's `public`→public, `protected`→protected (access preserved).
- `class D : protected B` → B's `public`/`protected` → `protected` (users of D can't see B's members).
- `class D : private B` → B's `public`/`protected` → `private` (only D itself sees them; D's users can't; "implementation inheritance").
- B's `private` members are never accessible to D.

## 3. When Is It Used?
- **`protected` (Java/C++)**: template-method hooks (`protected abstract printBody()`), fields subclasses legitimately need (`protected double balance`), `clone()`/`finalize`-style members meant for subclasses.
- **package-private (Java)**: intra-package cooperation (a package as a module); deliberately *not* inheritance-visible across packages.
- **`public` inheritance (C++ — the default and the norm)**: is-a modeling; `class SavingsAccount : public Account`.
- **`private` inheritance (C++ — rare)**: "implemented in terms of" — reuse implementation without exposing the is-a (the C++ composition substitute); almost always better replaced by composition.
- **`protected` inheritance (C++ — rare)**: "is-a for subclasses only" — rarely justified.

## 4. Why Wasn't Another Approach Chosen?
- *Why is Java's `protected` = package + subclass?* Java wanted a "package module" abstraction *and* an inheritance hook; combining them into one keyword was the design. The cost: the rule is subtle (the "only via own this" clause exists because a subclass in another package shouldn't touch *other* instances' protected members — that would be public-by-stealth).
- *Why not make everything `public` for subclasses (like Smalltalk's instance variables)?* Because that leaks implementation into the whole hierarchy; Java's `protected` is the deliberate compromise: subclasses get a hook, the world doesn't.
- *Why does C++ have three inheritance kinds?* Stroustrup wanted to express *access intent* in the is-a relationship itself: `public` = "true is-a," `private` = "implemented-in-terms-of," `protected` = "is-a for descendants." Java rejected this (single `extends` semantics) as too subtle; C++ kept it for expressiveness.
- *Why not just composition for private inheritance?* Because private inheritance gives access to the base's `protected` members and virtual overrides that plain composition doesn't; but modern guidance says composition + delegation is clearer — private inheritance survives as a legacy/optimization tool.

## 5. Intuition
Think of **a family-owned company**. `public` members = the public lobby (anyone). `protected` members = the *family office* — only family (subclasses) and the founding team (same package) can enter, and each family member may only use it for *their own* business (own `this`), not another family member's company. Package-private = the *office floor* — anyone working in that office (package) sees it, but family members in other offices (subclasses elsewhere) do not. C++ inheritance kinds = *what the family lets the next generation re-declare*: `public` inheritance = "the children may re-show the parent's sign," `private` = "the children may *use* the parent's knowledge but must not show it to the world."

## 6. Real-World Analogy
A **hospital's medical records**. `public` = the front desk directory. `protected` = the *attending physicians'* chart room: doctors (subclasses) and the internal medicine floor (same package) may read charts — but only for *their own patients* (`own this`), not a random doctor's charts. Package-private = the floor's break room: staff on that floor see it; doctors in other buildings don't. C++ inheritance kinds = whether a specialty can *re-expose* the hospital's procedures: `public` — the specialty presents the hospital's full protocol to patients; `private` — the specialty uses the protocol internally but never tells patients about it; `protected` — only sub-specialties may know it exists.

## 7. Formal Definition
**Java**: a member's access determines its availability to a subclass. `public` — inherited and accessible everywhere. `protected` — accessible within the same package and from a subclass in any package, provided the access is through a reference of the subclass's own type (or a subtype) / `this` / `super`; it cannot be reached through a base-class reference from outside the package. Package-private — accessible only within the package; not inherited-accessible across packages. `private` — not accessible by name in the subclass (though its storage exists). **C++**: the inheritance access specifier rescopes the base's members in the derived class: `public` inheritance preserves access levels; `protected` inheritance reduces both `public` and `protected` base members to `protected` in the derived; `private` inheritance reduces them to `private` in the derived; base `private` members remain inaccessible throughout. Effective base access = min(member access, inheritance access).

## 8. Example
```java
// Java
package bank.core;
public class Account {
    private double secret;             // not accessible to subclass by name
    protected double balance;          // package + subclasses (via own this)
    int txCount;                       // package-private: bank.core only
    public void deposit(double amt) { balance += amt; }
}
package bank.savings;                  // different package
public class SavingsAccount extends Account {
    public void apply(double rate) {
        balance += balance * rate;     // OK: protected via own this
        // txCount++;                  // ERROR: package-private, not in bank.core
        // secret = 1;                 // ERROR: private
    }
    public void bad(Account other) {
        // other.balance += 5;         // ERROR: protected, other package, not own this
    }
}
```
```cpp
// C++ — inheritance kind rescopes access
class Base { public: int pub = 1; protected: int prot = 2; private: int priv = 3; };
class PubD    : public Base    {};   // PubD exposes pub (public), prot (protected); priv hidden
class ProtD   : protected Base {};   // pub and prot become protected in ProtD
class PrivD   : private Base    {};  // pub and prot become private in PrivD
int main() {
    PubD  p;  p.pub;                  // ok (public in PubD)
    PrivD q;  // q.pub;               // error: private in PrivD
    return 0;
}
```

## 9. Internal Working
1. **Java**: access is checked at compile time using (declared access, enclosing package, inheritance relationship). The bytecode verifier re-checks. `protected` from another package is legal *only* when the access expression's receiver type is the subclass (or its subtype) — a targeted "inheritance hole."
2. **Java dispatch**: inherited `public`/`protected` methods are vtable entries; a protected method is callable in subclass bytecode as `invokevirtual` with `this` — no special runtime handling.
3. **C++**: the *effective access* is computed as `min(member-access, inheritance-kind)`. `private`/`protected` inheritance does *not* change the object layout (all base members physically present) — it only changes *which are nameable* by D's users and which conversions (D→Base) are allowed. A `D` privately inheriting `B` cannot be implicitly converted to `B*` outside D.
4. **C++ access & layout are independent**: access is a compile-time name-visibility rule; layout (where base members sit) is unchanged.

## 10. Time Complexity
- Access checks: compile-time/verify-time only — zero runtime cost in both languages.
- Protected member access: O(1) (offset from `this`).
- C++ private/protected inheritance: no runtime cost (compile-time visibility rule); implicit conversion D→B allowed/denied at compile time.
- Nothing about access specifiers changes runtime behavior.

## 11. Advantages
- **`protected`**: enables template/hook methods and shared subclass state without exposing internals to the world.
- **package-private**: package-as-module encapsulation.
- **C++ `public` inheritance**: clean is-a re-exposure.
- **C++ `private` inheritance**: implementation reuse with zero is-a leakage (the "secret base").
- Enforced at compile time — safe by construction.

## 12. Disadvantages
- **`protected`** is subtle: the "only via own this" rule trips teams; it also breaks encapsulation (subclasses reach internals).
- **Package-private across packages**: subclasses can't see members they might legitimately need (forces public/protected).
- **C++ three kinds**: subtle, easy to misread; `private`/`protected` inheritance is rarely what you want (composition is clearer).
- **Access specifiers + inheritance = higher cognitive load**; deep hierarchies amplify mistakes.

## 13. Interview Questions
1. **Q: What does `protected` mean in Java, precisely?** A: Accessible (a) within the same package and (b) from subclasses in any package — but a subclass in another package can access the member only through its own `this`/`super` (or a subtype reference), never through a base-class reference.
2. **Q: TRICKY — `SavingsAccount` (different package) has `void f(Account a) { a.balance++; }` where `balance` is protected. Legal?** A: No — `protected` access from another package requires the receiver to be the subclass's own type; `a` is typed `Account`, so it's a compile error even though `SavingsAccount extends Account`.
3. **Q: Are package-private members inherited by a subclass in another package?** A: No — package-private is visible only within the package; a subclass elsewhere cannot access them by name. (The member exists structurally but isn't accessible.)
4. **Q: What's the difference between Java's `protected` and C++'s `protected`?** A: Java's = package + subclasses (via own this); C++'s = subclasses only, no package notion — and C++ `protected` members *can* be reached through base references by subclasses (no "own this" restriction).
5. **Q: C++ `class D : private B` — what does it mean?** A: D inherits B's implementation but B's `public`/`protected` members become *private* to D: D's users can't see them, and D is not substitutable for B (no implicit D→B conversion). It's "implemented in terms of" — a composition substitute.
6. **Q: TRICKY — Does `private` inheritance change the object layout in C++?** A: No — all base members are still physically present in D's layout; `private` only changes *name visibility* and *implicit conversion* at compile time. (Empty-base optimization aside.)
7. **Q: When would you use `protected` members at all?** A: For template-method hooks (`protected abstract doWork()`), state subclasses genuinely need to extend (`protected double balance`), and members meant for subclasses but not the public API. Prefer `private` + `protected` methods over `protected` *fields* (fields leak representation).
8. **Q: SCENARIO — Design a base class with a hook for subclasses only.** A: `protected abstract void onEvent(Event e);` — visible to subclasses (they override it), invisible to external callers. That's exactly the template-method use `protected` was made for.
9. **Q: PRODUCTION — Your base class exposes fields as `protected`. Critique.** A: Leaky — protected fields expose representation to every subclass (fragile base), and mutation bypasses your validation. Prefer `private` fields + `protected` methods/accessors that guard the state.
10. **Q: What is the "effective access" rule in C++?** A: Effective access of a base member = the *more restrictive* of (the member's own access) and (the inheritance kind) — e.g., `public` member through `protected` inheritance → `protected`; through `private` inheritance → `private`.
11. **Q: TRICKY — In C++, can a `private`-inheriting class still call the base's public methods?** A: Yes — inside D, the base's public/protected members are accessible (as private members of D); only D's *users* can't see them. Private inheritance hides from outsiders, not from the derived class.
12. **Q: Why does Java not have private/protected *inheritance* like C++?** A: Java deliberately kept one inheritance semantics (`extends` = public inheritance) for simplicity; its access modifiers (private/protected/package) already give enough granularity, and composition covers C++'s private-inheritance use case.
13. **Q: SCENARIO — You need a class that reuses a utility's implementation but must NOT be usable as it.** A: C++: `class MyCache : private CacheImpl { ... }` (reuse, no is-a); Java: composition — `private final CacheImpl impl;` + delegation. Composition is clearer in both; private inheritance is the legacy C++ idiom.
14. **Q: What happens to `protected` members when subclassing a subclass (multilevel)?** A: They remain protected (or re-widenable only within access rules); a `SavingsAccount2 extends SavingsAccount` keeps access to `Account.balance` (still protected, still via own this). Access doesn't decay down the chain.
15. **Q: PRACTICAL — In Java, why is the "only via own this" clause part of `protected`?** A: Otherwise a subclass could read/write protected members on *arbitrary* base instances from outside the package — effectively making them public. The clause preserves encapsulation while still granting the subclass its own inheritance hook.

## 14. Follow-Up Questions
1. **Q: What is the difference between C++ `friend` and `protected`?** A: `friend` grants access to *specific named classes/functions* regardless of hierarchy; `protected` grants access to *all subclasses*. `friend` is finer-grained; `protected` is structural.
2. **Q: Can you override a `protected` method with `private` in C++?** A: Yes (C++ allows reducing access on override — the vtable still dispatches to it, but name access is restricted); Java *forbids* narrowing on override (compile error). This asymmetry is a classic C++-vs-Java question.
3. **Q: What is the "protected constructor" pattern?** A: A `protected` constructor in a base class — only subclasses (and package) can construct the base; external code must use the subclass. It enforces "extend me, don't instantiate me" without making the class abstract.
4. **Q: When is package-private the right choice over protected?** A: When the sharing is *collaboration within a module* (package) rather than *extension*; package-private keeps it out of subclass reach entirely — a stronger encapsulation boundary than protected.

## 15. Coding Example
```java
// Java: protected hook + private state
public abstract class AbstractTask {
    private long startedAt;                        // private: representation
    protected abstract void execute();             // protected: subclass hook
    public final void run() {
        startedAt = System.nanoTime();
        execute();                                  // template method
        System.out.println("took " + (System.nanoTime() - startedAt) + "ns");
    }
}
public class ReportTask extends AbstractTask {
    protected void execute() { System.out.println("building report"); }
    public static void main(String[] args) { new ReportTask().run(); }
}
```
```cpp
// C++: inheritance kinds in practice
class Queue { public: void push(int); protected: int cap_; };
// Public inheritance — true is-a:
class PriorityQueue : public Queue {};      // push is public, cap_ protected
// Private inheritance — implementation reuse, no is-a:
class Metrics : private Queue {             // push hidden from users
public: void record() { push(1); }          // internal use only
};
```

## 16. Industry Usage
- **JDK**: `AbstractList` uses protected fields/methods for implementers; `Object.clone()` is `protected` (subclass hook); `Template Method` hooks are `protected abstract` throughout the JDK.
- **Spring**: `AbstractBeanFactory`, `AbstractApplicationContext` expose `protected` template hooks; the framework relies on the protected-extends contract.
- **Android**: `Activity.onCreate` etc. are the framework's protected (well, public in API 35+ but historically protected) lifecycle hooks that subclasses override.
- **C++ (Chromium, LLVM, HFT)**: `public` inheritance for is-a; `private` inheritance for "implemented in terms of" (e.g., base class from another library reused internally); protected members for extension hooks.
- **Effective Java guidance**: "minimize accessibility" — default to private, prefer protected methods over protected fields, and prefer composition over private-inheritance-style reuse.

## 17. References
- Java Language Specification, §6.6 (Access Control), §8.4.8.3 (Access during overriding): https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html
- Oracle Java Tutorials, "Controlling Access" / "Overriding and Hiding": https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html
- Bjarne Stroustrup, *The C++ Programming Language* — access specifiers, inheritance kinds.
- cppreference, "Derived classes" (access): https://en.cppreference.com/w/cpp/language/derived_class
- Joshua Bloch, *Effective Java* — Item 15 (minimize accessibility).

## 18. Cheat Sheet
- Java `protected` = package + subclasses (any package), subclass access only via own `this`.
- Package-private = package only; NOT accessible to subclasses in other packages.
- `private` = not inherited-accessible by name (storage exists).
- C++ effective access = min(member access, inheritance kind).
- C++ `public` inheritance = is-a; `private` = implemented-in-terms-of (composition substitute); `protected` = is-a for descendants.
- C++ `private`/`protected` inheritance does NOT change layout — only visibility/conversion.
- C++ allows narrowing access on override; Java forbids it.
- Prefer `private` fields + `protected` methods over `protected` fields.

## 19. Quiz
1. Java `protected` means: a) subclasses only b) package + subclasses (own this) c) everyone d) package only → **b**
2. A subclass in another package can access a package-private member? a) yes b) no c) only public d) via super → **b**
3. C++ `class D : private B` makes B's public members in D: a) public b) protected c) private d) deleted → **c**
4. Effective access = ? a) max(member, inherit) b) min(member, inherit) c) member only d) inherit only → **b**
5. Private inheritance changes object layout? a) yes b) no c) sometimes d) only virtual → **b**
6. True or False: Java lets you narrow access when overriding. → **False**

## 20. Flashcards
- **Q: Java protected rule?** → **A:** Package + subclasses anywhere, but subclass access only via its own this.
- **Q: Package-private across packages?** → **A:** Not accessible to subclasses in other packages.
- **Q: C++ private inheritance?** → **A:** Reuse implementation; base members become private to D; no is-a (composition substitute).
- **Q: Effective access rule (C++)?** → **A:** min(member access, inheritance kind).
- **Q: Does private inheritance change layout?** → **A:** No — visibility and conversion only.
- **Q: Java vs C++ override access narrowing?** → **A:** Java forbids; C++ allows.

## 21. Revision
Java's `protected` = package + subclasses anywhere, accessed by the subclass only through its own `this`; package-private is package-only (not inherited across packages); private isn't name-accessible. C++ adds inheritance *kinds*: `public` = is-a (access preserved), `protected` = is-a for descendants, `private` = implementation reuse with no exposure; effective access = min(member, kind), and layout never changes. Prefer `private` fields + `protected` hooks; Java forbids narrowing overrides, C++ allows it. First-30-seconds answers: "protected = package + subclass via own this; C++ private inheritance = composition substitute."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does protected mean in Java?" | Interview Q1 / Section 8 |
| "Access protected via base reference?" | Interview Q2 |
| "Package-private inherited across packages?" | Interview Q3 |
| "C++ private inheritance meaning?" | Interview Q5 / Section 7 |
| "Does private inheritance change layout?" | Interview Q6 |
| "Protected fields — good or bad?" | Interview Q9 / Section 16 |
| "Effective access rule?" | Interview Q10 |
| "Why no C++-style inheritance kinds in Java?" | Interview Q12 |
