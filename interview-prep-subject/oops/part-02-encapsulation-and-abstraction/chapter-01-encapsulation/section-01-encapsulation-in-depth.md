# Encapsulation in Depth

> **TL;DR**: Encapsulation is the bundling of data with the methods that operate on it, plus the hiding of that data behind a controlled interface — so the object, not the caller, is the only thing that can ever change its own state.

## 1. Why Does This Exist?
Encapsulation exists because **state is dangerous when it's unowned**. If any code can write to `account.balance`, then a bug anywhere in a 10-million-line program can silently corrupt the balance. Encapsulation gives state a single owner (the object) and a single guarded path to change it (its methods), which turns "find the bug that changed the balance" into "inspect the 3 methods that can change it." It also makes the class *replaceable*: because callers only use the public API, you can change the internal representation (e.g., switch `double` to `BigDecimal`, add a cache) without touching a single caller. Interviews probe encapsulation because it's the pillar most violated in production code (public fields, leaky getters, global state) and the one whose benefits are most concrete.

## 2. How Does It Work?
Two halves, both required:
1. **Bundling**: fields and their operating methods live in the same class — the methods are the *only* sanctioned way to touch the fields.
2. **Hiding**: fields are `private` (invisible outside); the public surface is an intentional, minimal API.

The mechanism chain: `private` → compiler rejects external access → bytecode verifier re-checks → every state change must pass through a method → that method can enforce invariants (validate, log, notify, lock). That's how "the object is the gatekeeper" becomes a *language guarantee*, not a convention.

## 3. When Is It Used?
- Every domain class: `Account`, `Order`, `User`, `Payment` — state private, behavior public.
- Value objects / immutable types: all fields `private final`, constructed once.
- Frameworks: beans hide wiring; `AtomicInteger` hides CAS internals behind `incrementAndGet()`.
- Collections: `HashMap` hides its buckets/array entirely — you can't corrupt its internals, only use its API.
- Library design: JDK classes encapsulate so the JDK can evolve internals without breaking the world.

## 4. Why Wasn't Another Approach Chosen?
- *Why not public fields (C-style)?* Because any caller can break invariants; public fields make internal representation part of the public API *forever* (a change breaks clients). Encapsulation chosen so the representation can evolve.
- *Why not just "document the rules"?* Documentation rots; the compiler is a better enforcement mechanism than a README. (Python chooses convention with `_`; Java/C++/C# chose enforcement.)
- *Why not global accessors (a `Data` singleton)?* That's still global mutable state — one owner but a single point of contention and no per-object protection. Encapsulation is *per-object*.
- *Why not reflection / `friend` to reach in?* `friend` (C++) and reflection (`setAccessible`) are deliberate escape hatches for trusted contexts, not the default path; defaulting to closed (private) is chosen because opening up is easy, closing back down is hard.
The design answer: "hide by default, expose deliberately" beats "expose by default, hide by discipline."

## 5. Intuition
Think of a **soda machine**. Inside (the state) are sealed cans, a motor, a coin slot — you can't reach in and grab a can or change prices (the internals are hidden). What you *can* do is insert coins and press buttons (the public API). The machine guarantees you always get a can and never get free soda, because *only the machine* controls its internals. Encapsulation is building every class like that soda machine: sealed insides, deliberate buttons.

## 6. Real-World Analogy
A **bank vault with a teller**. The vault's contents (state) are private. You don't get a key to the vault; you interact through the teller (public methods): `deposit()`, `withdraw()`, `getBalance()`. The teller enforces rules — no negative balances, no withdrawal beyond the balance, identity checks. If the bank changes the vault layout or switches to a digital vault, you never notice, because you always went through the teller. The teller is encapsulation: a single, guarded gateway that keeps the contents safe and the interface stable.

## 7. Formal Definition
**Encapsulation** is the mechanism of combining data (fields) and the methods that operate on that data into a single unit (a class) while restricting direct access to the data, typically by declaring fields `private` and exposing a controlled set of public methods (accessors and mutators). The external world observes the object only through its public contract; the internal representation is free to change without affecting clients. It is the language-level enabler of the broader principle of *information hiding*.

## 8. Example
```java
public class BankAccount {
    private double balance;                 // hidden state

    public BankAccount(double initial) {
        if (initial < 0) throw new IllegalArgumentException("initial < 0");
        this.balance = initial;
    }
    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("amount <= 0");
        balance += amount;                  // only this method can change balance
    }
    public boolean withdraw(double amount) {
        if (amount <= 0 || amount > balance) return false;
        balance -= amount;
        return true;
    }
    public double getBalance() { return balance; }
}
```
Without encapsulation, `balance` would be a public field: anyone could write `account.balance = -5000` and skip every rule. With it, the *only* ways to change `balance` are `deposit`/`withdraw` — both of which enforce the "never negative, never zero-or-less amounts" invariant.

## 9. Internal Working
1. javac reads `private double balance` and records the field's `ACC_PRIVATE` flag.
2. Any bytecode referencing `balance` from outside `BankAccount` fails compilation *and* verification (the verifier raises `IllegalAccessError` on hand-crafted class files).
3. At runtime, `account.getBalance()` executes: it reads `balance` at its fixed offset from the object base — O(1).
4. `account.withdraw(50)` executes the method body: check, mutate the private field via `this+offset`, return — the field write is *inside* the class, so it's legal.
5. The JIT sees the field is only ever mutated in `deposit`/`withdraw` and can even devirtualize/inline those calls.
Encapsulation is thus enforced in three layers (compile, verify, and — conceptually — method-only mutation), which is why "I'll just remember not to touch it" is replaced by "the language won't let me."

## 10. Time Complexity
- Field access through a getter: O(1) — one extra call frame, no asymptotic cost.
- Encapsulated mutation: O(1) + cost of the guard logic (validation/logging) — still O(1) typically.
- Defensive copy in a getter: O(n) where n = size of the returned collection — the *price* of safe access; unmodifiable wrappers are O(1).
- Net: encapsulation adds a small constant factor (a method call) and the occasional copy cost; it never changes algorithm asymptotics.

## 11. Advantages
- **Invariant enforcement** — the object's rules always hold because only guarded methods mutate state.
- **Low coupling / evolvability** — internals (storage, algorithm) can change without touching callers.
- **Bug localization** — a bad state change can only originate from the class's own methods.
- **Testability** — behavior is exercised through a small, well-defined API surface.
- **Security boundary** — sensitive data (passwords, keys) can be kept private; serialization/print views controlled.
- **Thread-safety hooks** — mutation can be synchronized at the single entry points.

## 12. Disadvantages
- **Boilerplate** — getters/setters/validators (mitigated by records/Lombok/properties).
- **Performance constant** — extra method call per access; sometimes devirtualized away, sometimes not.
- **Over-encapsulation** — hiding everything (including trivial, harmless data) creates ceremony without benefit.
- **Temptation to bypass** — teams use reflection/`friend`/package-hacks when the API is *too* closed, which is worse than a well-designed open API.
- **Hides complexity** — a clean interface can mask a very complex (hard-to-debug) implementation.

## 13. Interview Questions
1. **Q: What is encapsulation?** A: Bundling data with the methods that operate on it and hiding the data from outside access (private fields + controlled public methods), so the object itself enforces its invariants.
2. **Q: Why make fields private instead of public?** A: So external code can't break invariants and so the internal representation can change without breaking clients — a public field becomes permanent API; a private one is free to change.
3. **Q: TRICKY — "Encapsulation is just private fields and getters."** A: Only half right. Getters/setters that merely expose fields often *weaken* encapsulation. True encapsulation = bundling behavior with the data so the methods (not callers) own every mutation; accessors are just the visible tip.
4. **Q: Give an example of breaking encapsulation in real code.** A: A public mutable field (`public List<String> tags;`), returning the internal list directly from a getter (callers can add to your state), or a mutable static/global that any class can write.
5. **Q: How does encapsulation help with refactoring?** A: You change the internal representation (e.g., replace `double` with `BigDecimal`, replace a `List` with a `Map`) and only touch the class itself; callers depend on the unchanged public methods.
6. **Q: PRODUCTION — Encapsulate a `HashMap` cache field. What do you expose?** A: Private field; public `get(key)`, `put(key, value)`, `size()` (or a bounded subset) — never the map itself. Exposing the map would let callers mutate the cache behind your back (and bypass your eviction/locking).
7. **Q: SCENARIO — A library returns a `List` it owns. How do you protect it?** A: Return `Collections.unmodifiableList(list)` (O(1) view, throws on mutation) or a defensive copy (O(n), independent). Unmodifiable view is usually right; a copy is right when callers may keep it longer than the library's lifetime.
8. **Q: TRICKY — Does encapsulation affect performance?** A: Adds a constant-factor method-call overhead that JITs usually inline away; the *only* real cost is defensive copies for large collections. It never changes Big-O.
9. **Q: Can encapsulation exist without `private`?** A: Yes — Python uses `_` convention and name mangling (`__x`); C can use opaque structs + accessor functions (Linux kernel). `private` is the *enforced* Java mechanism; encapsulation is the idea.
10. **Q: What is the difference between bundling and hiding?** A: Bundling = fields and methods live in the same class (cohesion); hiding = external code can't touch the fields (access control). Encapsulation requires both; candidates often only mention hiding.
11. **Q: When is it acceptable to have a public field?** A: For immutable constants (`public static final`), or in tiny value/record types where there is no invariant and no evolution risk — e.g., a pair-like record. Rule of thumb: when a setter would add no value.
12. **Q: SCENARIO — Your class holds `LocalDateTime createdAt` that must never change after construction.** A: Make it `private final` and expose only a getter returning the immutable `LocalDateTime` itself (safe — it's immutable). No setter, no defensive copy needed.
13. **Q: PRACTICAL — How do you unit-test encapsulation?** A: Test the public contract: invariants after every operation (balance never negative), and that state changes only through methods. Encapsulation means your tests don't need (or want) access to internals.
14. **Q: TRICKY — "Getters and setters break encapsulation."** A: They can: a getter returning the internal mutable object, or a setter accepting any value without validation, leaks/weakens it. But *well-designed* accessors (validated setters, copied/unmodifiable getters) *are* encapsulation — the point is the guard, not the accessor.
15. **Q: PRODUCTION — How do you choose what's public vs private in a new class?** A: Start everything `private`; make a method `public` only when a caller genuinely needs it (minimal API). Expose behavior, not state; expose what's stable, hide what's likely to change.

## 14. Follow-Up Questions
1. **Q: What is "leaky abstraction"?** A: When a hidden implementation detail leaks through the interface (e.g., a `Stream` that throws "already consumed", a cache that behaves differently based on eviction). Joel Spolsky's term; encapsulation reduces leaks but can't eliminate all.
2. **Q: How does encapsulation relate to the Single Responsibility Principle?** A: SRP says a class should change for one reason; encapsulation lets you contain that change inside the class. They're complementary: encapsulation enables localizing the change that SRP demands.
3. **Q: Does serialization break encapsulation?** A: Serialization *reads* state without going through methods — a deliberate bypass (via `Serializable`/reflection) that many codebases accept; using it means you forfeit constructor validation on the read side (or must implement `readResolve`/validation).
4. **Q: What's the relationship between encapsulation and dependency injection?** A: DI *requires* encapsulation: you hide concrete collaborators behind interfaces (private fields set once via constructor) so the framework can inject alternatives; leaking the concrete type destroys the swap-ability.

## 15. Coding Example
A complete encapsulated class with defensive access:
```java
import java.util.*;

public final class Employee {
    private final String id;                     // immutable identity
    private final List<String> skills = new ArrayList<>();  // owned mutable state
    private double salary;

    public Employee(String id, double salary) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("id required");
        this.id = id;
        setSalary(salary);
    }
    public void addSkill(String skill) {         // guarded mutation
        if (skill == null || skill.isBlank()) throw new IllegalArgumentException("skill required");
        skills.add(skill);
    }
    public List<String> getSkills() {            // SAFE getter: unmodifiable view
        return Collections.unmodifiableList(skills);
    }
    public void setSalary(double salary) {       // validated setter
        if (salary < 0) throw new IllegalArgumentException("salary < 0");
        this.salary = salary;
    }
    public double getSalary() { return salary; }

    public static void main(String[] args) {
        Employee e = new Employee("E1", 100000);
        e.addSkill("Java");
        e.getSkills().add("Hack");               // UnsupportedOperationException: safe
        System.out.println(e.getSkills());       // [Java]
    }
}
```
```python
class Employee:
    def __init__(self, emp_id: str, salary: float):
        self._id = emp_id                       # convention: private
        self._skills = []
        self.salary = salary                    # property setter validates
    @property
    def skills(self):
        return tuple(self._skills)              # defensive copy (immutable tuple)
    @salary.setter
    def salary(self, value: float):
        if value < 0: raise ValueError("salary < 0")
        self._salary = value
    def add_skill(self, skill: str) -> None:
        self._skills.append(skill)
```
```csharp
// C#: properties ARE the encapsulation idiom
public class Employee
{
    private readonly string _id;
    private readonly List<string> _skills = new();
    private double _salary;
    public Employee(string id, double salary) { _id = id; Salary = salary; }
    public IReadOnlyList<string> Skills => _skills.AsReadOnly();   // safe getter
    public double Salary { get { return _salary; } set { if (value < 0) throw new ArgumentOutOfRangeException(); _salary = value; } }
}
```

## 16. Industry Usage
- **Java collections**: `Collections.unmodifiableList` is the industry-standard safe-getter idiom; `ArrayList`/`HashMap` encapsulate all internal structure.
- **Spring**: bean properties are encapsulated; `@Value`/`@Autowired` inject via setters/constructors while keeping fields private.
- **Guava**: `ImmutableList` etc. — immutable collections are the strongest form of encapsulation (state can't change at all).
- **JDBC/Drivers**: `Connection`/`PreparedStatement` hide protocol details; you never see the socket.
- **Effective Java norms**: Item 15/16/17 — minimize accessibility, use accessors, prefer immutability — encoded in every major Java codebase (Google, Amazon, LinkedIn style guides).
- **Linux kernel**: opaque structs (declared in the .h, defined in the .c) — encapsulation without language support, used by `struct file` and friends.

## 17. References
- Joshua Bloch, *Effective Java* — Items 15–17 (minimize accessibility, accessors, immutability).
- David L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (1972) — the foundational information-hiding paper.
- Robert C. Martin, *Clean Code* — "Data/Object Anti-Symmetry", boundary and encapsulation chapters.
- Java Language Specification §6.6 (Access Control), §8.3.1 (Fields): https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html
- GeeksForGeeks, "Encapsulation in Java": https://www.geeksforgeeks.org/encapsulation-in-java/

## 18. Cheat Sheet
- Encapsulation = bundling + hiding; the object owns its state.
- Mechanism: `private` fields + public methods; enforced at compile + verify.
- Safe getters: unmodifiable views (O(1)) or defensive copies (O(n)).
- Validated setters: reject invalid values before assignment.
- Never expose internal mutable collections directly.
- Public field ≈ permanent API; private field ≈ free to change.
- Immutability is the strongest encapsulation.
- Costs: constant-factor method calls; copies for collections.

## 19. Quiz
1. Encapsulation = a) bundling + hiding b) hiding only c) bundling only d) getters → **a**
2. A getter returning the internal mutable list is: a) ideal b) a leak c) required d) faster → **b**
3. The verifier prevents: a) logic errors b) out-of-class field access c) nulls d) deadlocks → **b**
4. Best way to return a private list safely? a) return it b) `Collections.unmodifiableList` c) return null d) make field public → **b**
5. Encapsulation's asymptotic cost: a) O(n²) b) none (constant factor) c) O(log n) d) always O(n) → **b**
6. True or False: A validated setter is a form of encapsulation. → **True**

## 20. Flashcards
- **Q: Encapsulation is?** → **A:** Bundling data + behavior in a class and hiding the data behind a controlled interface.
- **Q: Why private fields?** → **A:** Enforce invariants and let the internal representation evolve without breaking callers.
- **Q: Safe getter for a collection?** → **A:** Unmodifiable view (O(1)) or defensive copy (O(n)); never the internal object.
- **Q: Cost of encapsulation?** → **A:** Constant-factor method calls (usually inlined); copies only for large collections.
- **Q: Public field = ?** → **A:** Permanent API commitment; changing it breaks clients.
- **Q: Strongest form of encapsulation?** → **A:** Immutability — state can't change at all.

## 21. Revision
Encapsulation bundles data with its operating methods and hides the data (`private`) so the object alone can change its state — enforced by the compiler and bytecode verifier. Its benefits: invariant enforcement, evolvability, bug localization, testability. Its traps: leaky getters (returning the internal collection), public fields (permanent API), getters/setters with no guard (they don't add encapsulation). Costs are constant-factor (method calls, usually inlined) plus defensive copies. First-30-seconds answer: "Encapsulation = bundle + hide; the object owns its state, and safe getters return copies or unmodifiable views."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is encapsulation?" | Formal Definition / Section 13 |
| "Why fields private, not public?" | Interview Q2 / Section 4 |
| "Encapsulation is just getters/setters?" | Interview Q3 |
| "How do you protect a returned list?" | Interview Q7 / Section 15 |
| "When can a field be public?" | Interview Q11 |
| "Do getters break encapsulation?" | Interview Q14 |
| "How to choose public vs private?" | Interview Q15 |
| "What's a leaky abstraction?" | Follow-Up Q1 |
