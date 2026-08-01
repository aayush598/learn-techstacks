# Getters, Setters, and Properties

> **TL;DR**: Getters and setters are the accessor methods that turn a raw field into a *guarded resource* — a getter that returns safe views, a setter that validates before writing; C# and Python promote this into language-level **properties** so accessors read like fields while behaving like methods.

## 1. Why Does This Exist?
Accessors exist because a field is either **raw data** (no rules — anyone can write garbage) or a **guarded resource** (rules enforced: non-negative, non-null, immutable, cached, logged, thread-safe). But Java has no "property" syntax, so the only way to guard a field is to *hide it behind methods*. Getters/setters are those methods. Properties (C#, Python, Kotlin) exist because the *method* syntax is noisy — a call site `getBalance()` reads worse than `balance` — so those languages promote accessors to syntax: `obj.Balance` invokes the getter, `obj.Balance = x` invokes the setter, invisibly. Interviews ask about accessors because their design (safe reads, validated writes, when setters are even justified) reveals whether you understand encapsulation or just copy the pattern.

## 2. How Does It Work?
**Java** — plain methods:
```java
private double balance;
public double getBalance() { return balance; }        // read
public void setBalance(double balance) {               // write + validate
    if (balance < 0) throw new IllegalArgumentException("balance < 0");
    this.balance = balance;
}
```
**C#** — properties are syntax for accessors:
```csharp
public double Balance { get { return _balance; } set { if (value < 0) throw new ArgumentOutOfRangeException(); _balance = value; } }
```
**Python** — `@property` decorators turn a method into a read/write accessor:
```python
@property
def balance(self): return self._balance
@balance.setter
def balance(self, value):
    if value < 0: raise ValueError("negative")
    self._balance = value
```
In all three, the *caller* writes `balance` (or `getBalance()`), but the *class* controls what happens on every read and write — validation, logging, cache, locks, notifications.

## 3. When Is It Used?
- **Validated writes**: money, age, dates, non-null references, bounded values.
- **Derived reads**: `getFullName()` computing from first+last; `getArea()` from radius.
- **Safe reads**: getters returning copies/unmodifiable views of collections.
- **Lazy/deferred reads**: compute on first access and cache (`getConnection()` builds once).
- **Notifications/lifecycle**: setter triggers event listeners, dirty flags, persistence.
- **Framework binding**: UI frameworks (WPF, JavaFX) *require* properties for data binding — you cannot bind to a raw field.

## 4. Why Wasn't Another Approach Chosen?
- *Why not public fields + direct reads/writes?* Then nothing can validate, log, or protect — and later adding a guard breaks every call site (fields become permanent API). Accessors chosen so a rule can be added *later* without breaking callers.
- *Why not methods with different names (`balance()`/`setBalance(...)`)?* Java does that; it works but is noisy. Properties chosen in C#/Python/Kotlin because call sites stay clean (`obj.Balance`) while behavior stays guarded — "fields that act like methods."
- *Why not always immutability (constructor-only, no setters)?* Perfect for value objects, but many entities need controlled *changes* (a balance changes every transaction). Accessors with validation chosen for mutable state; immutability for stable state — both used.
- *Why not reflection/getter-free field access (like Go)?* Go uses exported fields + validation at call sites; it's simpler but pushes discipline to the caller. Java/C#/Python chose to move the guard into the type itself.
The design answer: accessors exist to make "field with rules" possible while keeping call sites readable and future-proof.

## 5. Intuition
A getter is a **peephole** — you can look through it, but you see only what the class lets you see. A setter is a **bouncer** at the club door — only valid, dressed-up values get in; everything else is turned away at the door (exception). Properties are the *disguise*: to the outside world they look like a simple door (a field), but behind the door is the peephole + bouncer. Same entrance, full security.

## 6. Real-World Analogy
An **ATM**. The "getter" is the balance *display* (read-only; shows what you're allowed to see). The "setter" is the *withdrawal slot* — before dispensing, the machine validates the amount (positive, within limit, account has funds) and rejects bad requests. There is no raw "change my balance" keypad on the outside — that's the guarded setter. A property is like a checkout counter that *looks* like a direct countertop but is really a guarded transaction behind it. The ATM never lets you walk in and rewrite the ledger directly.

## 7. Formal Definition
An **accessor** is a method that provides controlled access to a field: a **getter** (accessor) reads the field or a safe projection of it; a **setter** (mutator) modifies the field after enforcing validation/invariants. A **property** is a language-level construct (C#, Python `@property`, Kotlin `var`) that binds an accessor pair to a member name so that member access syntax (`obj.Name`) invokes the underlying getter/setter. Best-practice accessor contracts: getters must not mutate, must not leak internal mutable state; setters must reject values that break invariants, and should only exist when mutation is a legitimate operation.

## 8. Example
```java
public class Account {
    private String email;
    private List<String> tags = new ArrayList<>();
    private double balance;

    public String getEmail() { return email; }                     // String is immutable: safe
    public void setEmail(String email) {                           // validated write
        if (email == null || !email.contains("@")) throw new IllegalArgumentException("invalid email");
        this.email = email;
    }
    public List<String> getTags() {                                // SAFE getter: unmodifiable view
        return Collections.unmodifiableList(tags);
    }
    public double getBalance() { return balance; }                 // derived/raw read
    public void deposit(double amount) {                           // guarded mutation
        if (amount <= 0) throw new IllegalArgumentException("amount <= 0");
        balance += amount;
    }
}
```
Contrast three patterns in one class: `email` — validated setter; `tags` — safe getter (no setter; mutation via `addTag()`); `balance` — guarded behavior methods instead of a setter. The design shows that *not every field needs a setter* — that's the sophistication interviewers want.

## 9. Internal Working
1. **Java**: `getBalance()` compiles to a method; the call site is `invokevirtual`. The JIT devirtualizes/inlines tiny accessors, so the guard is essentially free. `setEmail()` runs validation then writes `this+offset`.
2. **C#**: `obj.Balance = v` compiles to `call obj.set_Balance(v)`; the property metadata (`PropertyInfo`) enables data binding and reflection. Auto-properties (`{ get; set; }`) still compile to a private backing field.
3. **Python**: `obj.balance = v` triggers `__setattr__` → finds the property's setter function → runs validation. `obj.balance` triggers the getter. The property object lives in the class dict; access is a function call with the instance bound as `self`.
4. **All**: the field itself stays private; the accessor is the *only* bytecode path that touches it (verifier-enforced in Java), which is what makes "guarded" true rather than conventional.

## 10. Time Complexity
- Getter/setter call: O(1) + validation cost (typically O(1)); JIT-inlined in Java/C# hot paths.
- Safe getter returning unmodifiable view: O(1) (wrapper).
- Defensive-copy getter: O(n) for collection size n.
- Python property: O(1) + function call overhead (attribute lookup → descriptor → call).
- Lazy getter: first access O(build), subsequent O(1) (cache).

## 11. Advantages
- **Invariant enforcement** on every write.
- **Future-proof**: add validation/logging/caching later without breaking call sites.
- **Safe reads**: unmodifiable views and copies prevent callers mutating your state.
- **Readable call sites** (properties in C#/Python/Kotlin).
- **Framework integration**: data binding, serialization, validation attributes need properties/accessors.
- **Testability**: guards are unit-testable in isolation.

## 12. Disadvantages
- **Boilerplate** in Java (Lombok/records mitigate; Kotlin properties eliminate).
- **Overuse**: setters on every field = "public field with extra steps" — ceremony without encapsulation value.
- **Hidden side effects**: a "getter" that mutates or logs violates surprise-minimization (the "getter with side effects" smell).
- **Performance**: un-inlined accessors cost a call; copies cost O(n).
- **Anemic domain model risk**: getters/setters everywhere without behavior = procedural DTOs, not encapsulated objects.

## 13. Interview Questions
1. **Q: Why do we use getters/setters instead of public fields?** A: To guard reads and writes: validate on set, return safe views on get, and — critically — to allow adding rules later without breaking callers (fields are permanent API; accessors are not).
2. **Q: TRICKY — "Every private field should have a getter and setter."** A: Wrong. Expose accessors only when callers need them; a field's mutation should often be *behavior* (`deposit(amount)`), not a raw setter. Getters for everything → a public-field object in disguise.
3. **Q: What makes a getter "safe"?** A: It never mutates, never returns the internal mutable object (returns immutable values, unmodifiable views, or defensive copies), and never leaks implementation details.
4. **Q: What makes a setter good?** A: It validates the value against invariants (rejects null/negative/out-of-range before writing), stays a *simple guard* (no heavy side effects), and only exists if mutation is legitimate.
5. **Q: When is a setter NOT appropriate?** A: When the value must never change after construction (make it `final`), when mutation should go through behavior with domain rules (`withdraw` not `setBalance`), or when the field is derived (computed — getter only).
6. **Q: PRODUCTION — Your getter returns the internal list. What goes wrong?** A: Callers can mutate your state behind your back — bypassing your add/remove validation and breaking your invariants (and thread-safety). Fix: unmodifiable view or copy.
7. **Q: TRICKY — What's the cost of `Collections.unmodifiableList` vs a copy?** A: View = O(1), lightweight, but reflects later changes and is only a wrapper (mutation attempts throw `UnsupportedOperationException`); copy = O(n), independent snapshot. Choose view by default, copy when isolation matters.
8. **Q: What is a "derived" or "computed" property?** A: A getter that computes from other state — `getFullName()` from `firstName`+`lastName`, `getArea()` from `radius` — no backing field, no setter. It proves getters aren't field aliases.
9. **Q: SCENARIO — A class needs `createdAt` immutable, `email` validated, `password` never readable.** A: `createdAt` — `private final` + plain getter (immutable type, safe). `email` — private + validated setter. `password` — private + setter/`setPassword` that stores only a hash; *no* getter (read protection).
10. **Q: C# vs Java accessors — what's different?** A: C# has property syntax (`{ get; set; }`) with auto-implementation and data-binding support; Java has explicit methods. Both compile to the same guarded method calls; C# just makes the call site look like a field.
11. **Q: Python `@property` — how does it work internally?** A: It creates a descriptor on the class; `obj.attr` triggers `__get__` → your getter function; `obj.attr = v` triggers `__set__` → your setter. You can also make read-only properties by defining only the getter.
12. **Q: TRICKY — Is a getter that caches (lazy init) acceptable?** A: Yes, if documented — a "lazy getter" computes on first access and stores; but it *mutates state on read*, so it must be thread-safe (double-checked locking or `volatile`) and must not surprise callers.
13. **Q: PRODUCTION — Why do UI frameworks require properties for data binding?** A: Binding subscribes to change *notifications*; a raw field has no notification hook, while a setter can raise `PropertyChanged`/fire a listener. Accessors are the seam between state and the UI.
14. **Q: What is the "anemic domain model"?** A: Classes reduced to fields + getters + setters with all logic in services — it's procedural programming wearing OOP clothes; encapsulation argues for *behavior living with the data* (Fowler's critique).
15. **Q: SCENARIO — You inherit a class with 30 public getters/setters. How do you improve it?** A: Audit usage: remove unused accessors; convert raw setters to behavior methods where domain rules exist; make immutable fields final; hide internal collections with safe getters — restoring the object to "behavior owns state."

## 14. Follow-Up Questions
1. **Q: What's the difference between a property and a field in C#?** A: A field is storage with no behavior; a property is an accessor pair with optional backing field — it can be read-only, computed, validated, or virtual; fields cannot be in interfaces or virtual.
2. **Q: When would you use constructor-only initialization (no setters)?** A: For immutable value objects (`Money`, `Point`) and identity fields — ensures hash-safety and thread-safety; mutable entities get validated setters instead.
3. **Q: What is the "getter that does work" smell?** A: When a getter performs heavy computation, I/O, or mutations — callers assume reads are cheap and side-effect-free; moving the work into an explicit method (`computeTotal()`) is clearer.
4. **Q: Do records change the accessor story?** A: Records auto-generate accessors (`x()`, `y()`) for immutable state — no setters, no mutability — the ideal "data carrier" accessor design built into the language.

## 15. Coding Example
The same guarded resource in three languages:
```java
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;

public final class UserProfile {
    private String displayName;                    // validated write
    private final List<String> roles = new ArrayList<>();
    private final long createdAt = System.currentTimeMillis();  // immutable read

    public UserProfile(String displayName) { setDisplayName(displayName); }

    public String getDisplayName() { return displayName; }
    public void setDisplayName(String name) {
        if (name == null || name.isBlank() || name.length() > 20)
            throw new IllegalArgumentException("invalid display name");
        this.displayName = name.trim();
    }
    public List<String> getRoles() { return Collections.unmodifiableList(roles); }  // safe read
    public void addRole(String role) { roles.add(role); }                            // guarded write
    public long getCreatedAt() { return createdAt; }                                 // no setter

    public static void main(String[] args) {
        UserProfile p = new UserProfile("Alice");
        p.addRole("admin");
        System.out.println(p.getRoles());              // [admin]
        p.getRoles().clear();                          // throws: protected
        p.setDisplayName("A");                         // ok
    }
}
```
```csharp
public sealed class UserProfile
{
    private readonly List<string> _roles = new();
    private string _displayName;
    public UserProfile(string displayName) => DisplayName = displayName;
    public long CreatedAt { get; } = DateTimeOffset.UtcNow.ToUnixTimeSeconds();  // get-only property
    public string DisplayName { get { return _displayName; } set { if (string.IsNullOrWhiteSpace(value)) throw new ArgumentException(); _displayName = value.Trim(); } }
    public IReadOnlyList<string> Roles => _roles.AsReadOnly();
}
```
```python
class UserProfile:
    def __init__(self, display_name: str):
        self.display_name = display_name          # triggers setter
        self._roles = []
    @property
    def display_name(self) -> str:
        return self._display_name
    @display_name.setter
    def display_name(self, value: str) -> None:
        if not value.strip() or len(value) > 20: raise ValueError("invalid name")
        self._display_name = value.strip()
    @property
    def roles(self): return tuple(self._roles)    # safe read: immutable tuple copy
    def add_role(self, role: str) -> None: self._roles.append(role)
```

## 16. Industry Usage
- **JavaBeans spec**: getters/setters naming (`getX`/`setX`) is the *standard* for libraries, serialization, and frameworks — the entire bean ecosystem runs on accessor conventions.
- **Spring/Jackson**: deserialization goes through setters or field injection; validation (`@NotNull`, `@Size`) attaches to setters — accessors are the enforcement seam.
- **C#/.NET**: WPF/WinForms data binding *requires* properties (`INotifyPropertyChanged`); auto-properties are everywhere in production .NET code.
- **Python/Django**: `@property` used for derived fields (full_name) and validation; Django models use descriptors for fields.
- **Kotlin**: `var`/`val` properties compile to accessors — Kotlin's "properties are syntax" philosophy made Java teams adopt properties-by-default.
- **Anemic-model debates**: Fowler's *Anemic Domain Model* essay is *the* reference for why getters/setters alone don't make OOP — production teams split into DTOs (accessors fine) vs domain entities (behavior owns state).

## 17. References
- Joshua Bloch, *Effective Java* — Item 16 (accessor methods, not public fields).
- Martin Fowler, "Anemic Domain Model": https://martinfowler.com/bliki/AnemicDomainModel.html
- Microsoft C# docs, "Properties": https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties
- Python docs, "property" built-in: https://docs.python.org/3/library/functions.html#property
- Oracle Java Tutorials, "Variables / Methods": https://docs.oracle.com/javase/tutorial/java/javaOO/variables.html

## 18. Cheat Sheet
- Getter = controlled read (safe views; never mutate; never leak internals).
- Setter = controlled write (validate; only when mutation is legitimate).
- Not every field needs a setter; behavior methods beat raw setters.
- Safe collection getter: `Collections.unmodifiableList` (O(1)) or copy (O(n)).
- Properties (C#/Python/Kotlin) = accessors disguised as fields.
- Derived getters need no backing field.
- Anemic model = fields + accessors, logic elsewhere (anti-pattern).
- Records give immutable accessors for free.

## 19. Quiz
1. A getter should: a) mutate state b) return the internal object c) never mutate and never leak internals d) do I/O → **c**
2. Best getter for a `List` field: a) return it b) unmodifiable view c) make field public d) return copy always → **b**
3. Which field needs NO setter? a) `email` validated b) `createdAt` immutable c) `balance` domain-ruled d) all of the above → **d**
4. C# `{ get; set; }` compiles to: a) two public fields b) accessor methods + backing field c) a lambda d) reflection → **b**
5. Python `@property` implements: a) a descriptor b) a global c) a lambda d) a decorator only → **a**
6. True or False: Setters exist to make writes safe; getters exist to make reads safe. → **True**

## 20. Flashcards
- **Q: Purpose of a getter?** → **A:** Controlled read — safe view, no mutation, no internal leak.
- **Q: Purpose of a setter?** → **A:** Controlled write — validation before assignment.
- **Q: When does a field NOT need a setter?** → **A:** Immutable/final, derived, or domain-behavior mutation (deposit/withdraw).
- **Q: Safe getter for collections?** → **A:** Unmodifiable view (O(1)) or defensive copy (O(n)).
- **Q: What's a property?** → **A:** Language syntax (C#/Python/Kotlin) binding accessors to member access.
- **Q: Anemic domain model?** → **A:** Fields + accessors with logic elsewhere — procedural code in OOP clothing.

## 21. Revision
Accessors make fields "guarded resources": getters must be side-effect-free, return safe views (unmodifiable/copies), and never leak internals; setters must validate and exist only when mutation is legitimate — behavior methods (`deposit`) beat raw setters, and immutable fields need no setter. Properties (C#/Python/Kotlin) are accessors with field-like syntax. DTOs get accessors; domain entities get behavior. First-30-seconds answers: "getter = safe read, setter = validated write, not every field needs both; safe getters return unmodifiable views."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why getters/setters instead of public fields?" | Interview Q1 / Why Does This Exist |
| "Should every field have getter+setter?" | Interview Q2 |
| "What makes a getter safe?" | Interview Q3 / Section 15 |
| "When is a setter inappropriate?" | Interview Q5 |
| "Returning the internal list — problem?" | Interview Q6 |
| "C# vs Java accessors?" | Interview Q10 |
| "Python @property internals?" | Interview Q11 / Internal Working |
| "Anemic domain model?" | Interview Q14 / Section 16 |
