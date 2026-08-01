# Access Modifiers and Scope

> **TL;DR**: Java's four access levels — `private`, package-private (default), `protected`, `public` — define *who can touch a member*; the subtle rules (especially `protected` = package-private **plus** subclasses elsewhere) and the scope split between static and instance members are where almost every candidate slips.

## 1. Why Does This Exist?
Access modifiers exist to make **encapsulation enforceable** rather than conventional. A language could rely on programmers never calling internal methods — but that fails at scale (and in distributed teams), so Java bakes *visibility* into the type system and enforces it at compile time and by the bytecode verifier. The four levels form a ladder of trust: you start fully hidden (`private`) and widen exposure deliberately (`public` is an API commitment). Modifiers also encode *scope*: `static` marks class-level (one copy) vs instance-level (per object) members. Interviews ask about them because visibility errors are compile-time errors — the semantics must be exact, not approximate.

## 2. How Does It Work?
- `private` — visible only within the same class (including nested classes of it).
- (default) package-private — visible within the same package (classes in the same folder/package).
- `protected` — package-private PLUS subclasses in *any* package (only through inheritance for code outside the package).
- `public` — visible everywhere.
- For **top-level classes**: only `public` or package-private are legal (no `private`/`protected` top-level classes).
- Scope: `static` member belongs to the class (one instance, reachable via class name); non-static belongs to each object. A static context cannot reference `this` or instance members.

The mechanism is layered: the compiler checks declared access; the JVM bytecode verifier re-checks it, so even hand-crafted bytecode can't bypass it (except via reflection, which can bypass *checks* but not the design intent).

## 3. When Is It Used?
- `private`: fields, helpers, implementation details. Default choice for state.
- package-private: internal APIs shared within a package (e.g., framework internals that a package's public classes delegate to).
- `protected`: template-method hooks that subclasses may override/use but outsiders shouldn't call; constructors meant for subclasses.
- `public`: the class's API surface — what other packages may call.
- `static`: constants (`static final`), utility methods, counters, factory methods, `main`.
- `final` (with access): immutable API (`public final` class), sealed contracts.

## 4. Why Wasn't Another Approach Chosen?
- *Why not only public/private (like some languages)?* Because real systems need a "friendlier than private, stricter than public" level — package-private allows intra-package cooperation (a package as a module) without exposing everything; C++ has `friend` for a similar hole, Go has lowercase-identifier privacy. Java's package-private chosen for module cohesion.
- *Why is `protected` defined as package-private + subclass?* Because inheritance needs a backdoor for subclasses in other packages; without it, every subclass would have to live in the base package or expose everything. The asymmetry (subclass can access through *its own* `this`, but not through another package's base reference) is the precise rule.
- *Why not "private to file" (Python `_x` convention)?* Python's underscore is *convention*, not enforcement — Java chose *enforcement* because convention rots under pressure; Python's philosophy is "we're all adults here," Java's is "the compiler protects the contract."
- *Why not C++ `friend`?* `friend` punctures encapsulation wholesale; Java's package scope is structural rather than ad-hoc.

## 5. Intuition
Think of a **company badge system**. `private` = your desk drawer (only you). Package-private = your team's shared drive (anyone on your team). `protected` = "employees plus external contractors who were given a specific onboarding" (your team's drive + contractors trained to use it — but only while acting as contractors). `public` = the front door (anyone). `static` = the company *policy* (one rule for everyone) vs instance = *your* badge's access level (per-person). Modifiers encode "how much of the building may you enter?"

## 6. Real-World Analogy
A **library with reading rooms**: `private` = the librarian's staff-only back room. Package-private = the reading room shared by members of one department. `protected` = the inter-library-loan room (your department + trusted partner libraries). `public` = the main lobby. And `static` = the library's *by-laws* (apply to all visitors the same) vs instance = each *library card* (per-member limits). Access rules are like building access rules: they define who may enter which room, and Java enforces them like a security guard who *always* checks badges.

## 7. Formal Definition
In Java, the **access level** of a member is determined by its access modifier, in increasing visibility: `private` (accessible only within the class body and its nested classes), **package-private**/default (accessible within the same package), `protected` (accessible within the same package **and** by subclasses declared in any package, but a subclass in a different package can access the member only through a reference of its own type or a subtype), and `public` (accessible everywhere). **Scope** distinguishes `static` members (associated with the class; one per class; accessible through the class or any instance) from instance members (associated with each object; require an instance reference).

## 8. Example
```java
package bank.core;
public class Account {
    private double balance;              // only inside Account
    int transactionCount;                // package-private: bank.core internals
    protected double getBaseRate() {     // bank.core + subclasses anywhere
        return 0.05;
    }
    public void withdraw(double amt) { balance -= amt; }   // API
}

package bank.app;                        // DIFFERENT package
public class SavingsAccount extends Account {
    public void printRate() {
        System.out.println(getBaseRate());      // OK: subclass accessing protected member
        // System.out.println(transactionCount); // COMPILE ERROR: package-private, not in bank.core
        // System.out.println(balance);           // COMPILE ERROR: private
    }
    public void other(Account a) {
        // a.getBaseRate();                  // ERROR (outside package, not via own type)
        //   — a subclass in another package can only use protected via its own this/super
        //   (unless a is a subtype of SavingsAccount with a non-abstract accessor)
    }
}
```
The trap embedded here: `getBaseRate()` is callable by `SavingsAccount` code *only through its own `this`*; calling it on an arbitrary `Account` reference from another package is illegal, even though `SavingsAccount extends Account`.

## 9. Internal Working
1. javac records each member's access flag (`ACC_PRIVATE`, `ACC_PUBLIC`, `ACC_PROTECTED`, or none=package) and static flag in the class file.
2. During compilation, access resolution walks the hierarchy + package to decide legality; illegal access = compile error.
3. At load time, the **bytecode verifier** re-checks: a crafted class file that accesses `private` members directly is rejected with `IllegalAccessError`.
4. Reflection can override checks (`setAccessible(true)`) — but the design remains: modifiers are enforced at compile+verify, which is the strongest practical enforcement short of kernel isolation.
5. `static` resolution: static member access compiles to a *class* reference (no `this`); instance member access compiles to an *object + offset* lookup; the JIT inlines constants (`static final`) at compile time.

## 10. Time Complexity
- Access checks happen at compile/verify time — **zero runtime cost** in HotSpot (access checks are not executed per-call; the verifier proves legality).
- `static final` constants are inlined: O(1), no memory read after JIT.
- Static vs instance field read: both O(1) (different addressing — class slot vs `this`+offset).
- Reflection access (`setAccessible(true)`): has overhead (few dozen ns) and bypasses verifier checks — a performance and safety reason to avoid reflective mutability.

## 11. Advantages
- **Enforced encapsulation** — invariants can't be broken by mistake (compile-time).
- **Contract clarity** — `public` = commitment; `private` = free to change; the rest are gradient levels of trust.
- **Module cohesion** — package-private lets a package be a module without exposing internals.
- **Template-method support** — `protected` gives subclass hooks without public API.
- **Scope precision** — `static` vs instance avoids accidental shared state (or accidental per-instance duplication).

## 12. Disadvantages
- **Boilerplate and ceremony** — more modifiers than Python's underscore convention.
- **Package-private can be bypassed** by adding classes to the same package (a practical leak).
- **`protected` is a subtle, easy-to-misuse rule** — its "subclass-only-through-own-reference" nuance trips teams.
- **Reflection breaks the model** — `setAccessible(true)` defeats modifiers; frameworks (Spring/Hibernate) routinely do this, weakening the guarantee.
- **package-private on modules is coarse** — modern `module-info.java` adds another layer to regain strictness.

## 13. Interview Questions
1. **Q: Name Java's four access modifiers in increasing visibility.** A: `private`, package-private (default), `protected`, `public`.
2. **Q: What does `protected` mean precisely in Java?** A: Accessible within the same package, AND accessible to subclasses declared in any package — but a subclass in a different package can access it only through its own type/`this`/`super`, not through an arbitrary base-class reference.
3. **Q: TRICKY — Can a subclass in another package access a `protected` member of a *parent reference*?** A: No. Only through its own `this` (or a subtype reference). Accessing `parentRef.protectedMember` from a different package fails to compile.
4. **Q: What is package-private access?** A: The default when no modifier is written — visible to all classes in the same package, nothing else. Distinct from `private` (only the class) and `protected` (package + subclasses).
5. **Q: Can a top-level class be `private` or `protected`?** A: No — top-level classes allow only `public` or package-private. `private`/`protected` apply to *members* (including nested classes).
6. **Q: What does `static` mean for a field vs a method?** A: Field: one copy per class (shared by all instances, reachable via class name). Method: no `this` — callable without an instance; cannot access instance members.
7. **Q: PRACTICAL — Why are constants declared `public static final`?** A: `public` = usable by clients; `static` = one per class (no per-instance duplication); `final` = cannot be reassigned — a compile-time constant that javac inlines.
8. **Q: TRICKY — Can a `static` method access an instance variable of a *passed-in* object?** A: Yes — through the parameter reference (`void s(User u) { u.email = ...; }`); it just can't access `this`'s instance members without an explicit instance.
9. **Q: SCENARIO — You want a class usable only inside its package but subclassable outside. Which modifiers?** A: The *class* should be package-private? No — that blocks subclassing outside. Correct: make the class `public` and its *constructor* `protected` (so only subclasses in other packages can construct it), while members stay package-private. Combining class/member modifiers gives you this control.
10. **Q: What's the difference between scope and access?** A: Scope (static vs instance) decides *how many copies / whether an instance is needed*; access (private/protected/public) decides *who can reference it*. They're orthogonal — you can have `private static` (hidden class-level) or `public` instance, etc.
11. **Q: PRODUCTION — Your library exposes a class with a public field. What's the risk?** A: Every client can mutate it, breaking invariants and making the field a permanent API commitment. Change it to `private` + getter (or a value type) now, before clients depend on it.
12. **Q: What is the "module" access level introduced in Java 9?** A: `module-info.java` adds `exports`/`opens` — a package is exported to other modules or not, layering *module-level* encapsulation on top of class-level modifiers.
13. **Q: TRICKY — Does a subclass inherit private members?** A: The fields/methods *exist* in the subclass's layout (memory) but are *not accessible by name* — inheritance of storage, not of visibility. You can only touch them through public/protected members of the parent.
14. **Q: Why does the bytecode verifier re-check access?** A: Because malicious/erroneous class files could be hand-written; the verifier rejects any file that accesses members outside their declared visibility (`IllegalAccessError`), preserving encapsulation even from custom bytecode.
15. **Q: PRACTICAL — Spring injects into `private` fields via reflection. Does that break the design?** A: It bypasses the compile-time guarantee (a documented, deliberate trade-off of the framework), which is why field injection is discouraged in favor of constructor injection — public/package constructor keeps visibility honest.
16. **Q: SCENARIO — Which access do you choose for a mutable cache field?** A: `private` (or package-private) + `synchronized` accessor methods — never expose the `Map` itself; otherwise callers mutate it behind your back (encapsulation is the point).

## 14. Follow-Up Questions
1. **Q: When would you use package-private methods?** A: For internal protocols of a package (e.g., `HashMap` package internals call each other) that shouldn't leak to clients — it keeps a package cohesive and small.
2. **Q: How do `interface` members differ in visibility?** A: Interface members are implicitly `public` (methods) and `public static final` (fields) — you can't make an interface method `private` without a `private` method body (Java 9+ allows `private` methods in interfaces for shared default-method code).
3. **Q: What does `protected` look like in C++?** A: Similar — accessible to derived classes; but C++ also lets *friends* access; and C++ access is per *name* at compile time with no "only through own this" rule (subclasses use base refs freely). The Java rule is stricter.
4. **Q: Can package-private ever be a security boundary?** A: Weakly — anyone can write a class in your package (if they control the classpath) to access it; treat it as a *design* boundary, not a security boundary.

## 15. Coding Example
```java
package demo.accounts;

public class Account {
    private double balance;              // private: class only
    int txCount;                         // package-private: demo.accounts
    protected double rate() { return 0.05; }   // package + subclasses elsewhere
    public static final String KIND = "ACCOUNT";  // public static final constant

    public Account(double balance) { this.balance = balance; }
    public double getBalance() { return balance; }
}

package demo.savings;
import demo.accounts.Account;

public class SavingsAccount extends Account {
    public SavingsAccount(double balance) { super(balance); }
    public double yearlyInterest() {
        return getBalance() * rate();          // OK: protected via own this
    }
    public static void main(String[] args) {
        SavingsAccount s = new SavingsAccount(1000);
        System.out.println(s.yearlyInterest());          // 50.0
        System.out.println(Account.KIND);                // public static final
        // System.out.println(s.txCount);   // ERROR: package-private (different package)
    }
}
```
```cpp
// C++ access: private/protected/public per section
class Account {
private:   double balance_;
protected: double rate() { return 0.05; }
public:    Account(double b) : balance_(b) {}
           double getBalance() const { return balance_; }
};
class SavingsAccount : public Account {
public:
    using Account::Account;
    double yearlyInterest() { return getBalance() * rate(); }  // protected OK
};
```
```python
# Python: conventions only — _private, __name-mangled, no enforced access
class Account:
    def __init__(self, balance):
        self.__balance = balance        # name-mangled to _Account__balance
    @property
    def balance(self): return self.__balance
```

## 16. Industry Usage
- **JDK internals**: `java.util` uses package-private heavily (e.g., `HashMap` internals); `module-info.java` (Java 9+) seals `java.*` from external access — real encapsulation at module scale.
- **Spring**: constructor injection prefers `public`/package constructors; field injection via reflection is discouraged; `@Component` scanning respects modifiers.
- **Effective Java norms**: "minimize accessibility" — everything `private` unless a reason; public API is a commitment; prefer `static factory` over public constructors.
- **Google Java Style Guide**: fields never `public`; constants `public static final`; `protected` only for genuine hooks.
- **Android**: SDK classes expose public APIs with carefully sealed internals (public classes, protected constructors, private impl).

## 17. References
- Joshua Bloch, *Effective Java* — Item 15 (minimize accessibility), Item 16 (accessor methods).
- Java Language Specification, Ch. 6 §6.6 (Access Control): https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html
- Oracle Java Tutorials, "Controlling Access to Members of a Class": https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html
- The Java® Virtual Machine Specification, Ch. 4 (access flags, verification): https://docs.oracle.com/javase/specs/jvms/se17/html/jvms-4.html

## 18. Cheat Sheet
- Visibility ladder: private < package-private < protected < public.
- `protected` = package-private + subclasses (any package, only via own `this`).
- Top-level classes: only `public` or package-private.
- Interface members: implicitly `public`; interface fields `public static final`.
- `static` = class-level (no `this`); instance = per-object.
- Constant idiom: `public static final`.
- Modifiers cost nothing at runtime — enforced at compile + verify.
- Python's `_` is convention; Java enforces.

## 19. Quiz
1. Which is the most restrictive? a) public b) protected c) private d) package → **c**
2. A `protected` member is visible to: a) only the class b) same package + subclasses c) everyone d) only subclasses → **b**
3. Top-level classes can be: a) private b) protected c) public or package-private d) all → **c**
4. `static` means: a) per-object copy b) per-class, shared c) final d) private → **b**
5. A `static` method: a) can access instance fields b) has `this` c) has no `this` and can't access instance fields directly d) can be overridden → **c**
6. True or False: Reflection can access private members. → **True** (with `setAccessible(true)`)

## 20. Flashcards
- **Q: Four access levels in order?** → **A:** private, package-private, protected, public.
- **Q: Precise protected rule?** → **A:** Same package + subclasses anywhere, but subclass access only via own `this`.
- **Q: Can a top-level class be private?** → **A:** No — only public or package-private.
- **Q: What does static mean?** → **A:** Class-level — one copy, no `this` needed, no instance access.
- **Q: Interface member visibility?** → **A:** Implicitly public (fields static final).
- **Q: Runtime cost of access modifiers?** → **A:** Zero — enforced at compile and bytecode-verify time.

## 21. Revision
Java's visibility ladder is private → package-private → protected → public, enforced at compile time and re-verified by the bytecode verifier (zero runtime cost). `protected` is the tricky one: package-private plus subclasses anywhere, but subclasses in other packages can only use it through their own `this`. Top-level classes are public or package-private only; interfaces are implicitly public/static-final. `static` is scope (class-level, no `this`); it's orthogonal to access. First-30-seconds answers: "ladder order," "protected = package + subclasses via own this," "static = one per class."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Name the access modifiers." | Formal Definition / Section 13 |
| "What does protected mean exactly?" | Interview Q2 / Example |
| "Can a subclass access protected via parent reference?" | Interview Q3 |
| "What is package-private?" | Interview Q4 |
| "Can a top-level class be private?" | Interview Q5 |
| "Static vs instance scope?" | Interview Q6 / Section 2 |
| "Why `public static final` for constants?" | Interview Q7 |
| "Does a subclass inherit private members?" | Interview Q13 |
