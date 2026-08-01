# Identity, State, and Behavior

> **TL;DR**: Every object has three distinct properties — **identity** (what it is, its reference), **state** (what it knows, its field values), and **behavior** (what it does, its methods) — and confusing them is the root of `==`-vs-`equals` bugs, mutable-state bugs, and design mistakes.

## 1. Why Does This Exist?
The identity/state/behavior trichotomy exists because objects are *not* just data bags. If you only model state (fields), you can't distinguish "two different people with the same name" (same state, different identity). If you only model behavior (methods), you can't remember anything. Real systems need all three, and interviewers ask about them because the distinction drives equality semantics, hashing, concurrency safety, and object design. A `User` with `id=42` is the *same* user even if their email changes (identity persists, state changes); `==` and `.equals()` implement exactly these two notions of sameness. Understanding the triad prevents the classic production bugs: mutating shared references, comparing wrong things, and treating mutable objects as hash keys.

## 2. How Does It Work?
- **Identity**: the object's intrinsic "this one, not another" — in Java/C++/Python it's its memory address (reference); in databases it's a primary key or UUID. Identity is *immutable* for the object's life; it's what `==` (Java), `is` (Python), and pointer comparison (C++) check.
- **State**: the object's current field values — mutable (usually) and changeable via methods. `equals()` compares state (when overridden); `hashCode()` derives from state.
- **Behavior**: the methods the object exposes — its capability. Two objects with the same state but different types can behave differently (polymorphism).

The three map to language features: identity → reference/pointer, state → fields, behavior → methods.

## 3. When Is It Used?
- **Equality**: deciding whether two references denote the same object (identity) or two objects with the same data (value equality).
- **Hashing / collections**: `HashSet`/`HashMap` need consistent `equals`+`hashCode` over *state*.
- **Value objects vs entities** (DDD): an `OrderId` is an entity with identity; `Money(100,"USD")` is a value object with only state — a key design decision.
- **Caching / memoization**: cache keys must be identity-stable or state-immutable.
- **Concurrency**: mutating shared state (behavior on state) requires synchronization.
- **Serialization**: state gets serialized; identity/behavior do not.

## 4. Why Wasn't Another Approach Chosen?
- *Why not make everything identity-based?* Then two `Money(100)` would be "different" and you could never compare prices — equality-by-state would be impossible. You need value semantics for data.
- *Why not make everything state-based (no identity)?* Then you couldn't have two users with the same data, and you couldn't track *which* record changed — entities need identity.
- *Why not a single equality operator?* Because one operator can't express both "same object" and "same value"; languages offer two (`==` and `.equals()`/`is`) precisely so the programmer can choose. 
- *Why not make state always immutable?* Immutability kills identity-tracking scenarios (a bank account that never changes is useless) and costs allocation churn; so mutable state exists, and identity/equality rules become critical. The chosen design: separate concepts, separate operators.

## 5. Intuition
Think of **identical twins**: Two twins can have the same name, age, DNA, and haircut (same *state*), but they are two different people (different *identity*). "Are you my twin?" (state equality) and "Are you *the* Alice?" (identity equality) are different questions. Also, Alice can change her hairstyle (state changes) yet remain the same person (identity unchanged). Objects work the same way: state can change while identity persists.

## 6. Real-World Analogy
A **parking spot** — no. Better: a **bank account number vs account balance**. Your account number is the *identity* (never changes, distinguishes you from everyone else). The *balance* is the *state* (changes constantly). The *operations* — withdraw, deposit, transfer — are the *behavior*. The bank doesn't care if two different accounts happen to hold $500 each (same state, different identity); and your account is the "same" account even when the balance goes from $500 to $200. Databases model this exactly: a `id` primary key (identity), columns (state), stored procedures (behavior).

## 7. Formal Definition
For any object O in a class-based object model: **identity** is the property that uniquely distinguishes O from every other object (its reference/address or a stable key); **state** is the set of all current values of O's fields (attributes); **behavior** is the set of operations (methods) that O supports, which may read or mutate its state. In terms of equality: `identity(O1) == identity(O2)` iff O1 and O2 are the same object; `state(O1) == state(O2)` is *value equality*, defined by the class's `equals()`.

## 8. Example
```java
public class User {
    private final int id;              // identity-bearing
    private String email;              // mutable state
    public User(int id, String email) { this.id = id; this.email = email; }
    public void setEmail(String e) { this.email = e; }     // behavior mutates state
    public int getId() { return id; }
    public String getEmail() { return email; }

    @Override public boolean equals(Object o) {           // VALUE equality on id+email
        if (!(o instanceof User u)) return false;
        return id == u.id && email.equals(u.email);
    }
    @Override public int hashCode() { return 31 * id + email.hashCode(); }

    public static void main(String[] args) {
        User a = new User(1, "a@x.com");
        User b = new User(1, "a@x.com");     // same state, different identity
        User c = a;                          // same identity (aliasing)
        System.out.println(a == b);          // false  (identity differs)
        System.out.println(a.equals(b));     // true   (state equal)
        System.out.println(a == c);          // true   (same reference)
        a.setEmail("new@x.com");             // state changes...
        System.out.println(a.equals(b));     // false now (state diverged)
    }
}
```
Concrete walkthrough: `a` and `b` are two objects with identical field values — only *state* equality holds. `a` and `c` are one object — identity equality holds. Changing `a`'s email changes only `a`'s state; `b` and `c` (if it weren't for aliasing) are unaffected.

## 9. Internal Working
1. `new User(1,...)` allocates a heap object; the reference value (its address) becomes the identity.
2. `==` on two references compiles to a pointer comparison — true iff same address.
3. `.equals()` is a method call; the default (`Object.equals`) does `==`, but `User` overrides it to compare fields — true iff field values match.
4. `hashCode()` must agree with `equals()`: equal objects (by state) must hash equal, so the JVM's `HashMap` can find them; `hashCode` derives from the same fields.
5. State mutation via `setEmail` changes field bytes in the object; identity (address) is unaffected.
6. If a mutable object is used as a `HashMap` key and its state changes, the hash changes but the bucket doesn't — the key becomes unfindable (the classic production bug).

## 10. Time Complexity
- Identity comparison (`==`): O(1) — one pointer compare.
- Default `equals`: O(1).
- Overridden `equals`: O(k) where k = number/size of compared fields (usually O(1) for fixed fields).
- `hashCode`: O(k) to compute (memoizable; `String` caches it).
- Hashing a collection of N objects: O(N · k) to build, O(k) per lookup (average).
- **Key point**: equality/hashing cost is a function of *state size*, not identity — another reason to design state deliberately.

## 11. Advantages
- Distinguishing the three lets you choose the correct equality (`==` vs `equals`), avoiding identity/value bugs.
- Entity-vs-value modeling (DDD) becomes principled.
- Hashing correctness (mutable keys hazard) is avoidable once understood.
- Concurrency: knowing what's state (shared mutable) tells you where to synchronize.
- Serialization/caching: you know what to persist (state) vs what to keep client-side (identity).

## 12. Disadvantages
- Three concepts = three chances to confuse them (the most common OOP bug source).
- Mutable state + hashing = landmine if not careful.
- Value equality requires discipline (override `equals`/`hashCode`; forgot → bugs).
- Identity-vs-value duality means the same class might need both semantics (`Money` as value, `Account` as entity) — harder to design well.

## 13. Interview Questions
1. **Q: What are identity, state, and behavior in an object?** A: Identity = what uniquely makes it this object (reference/key); state = its current field values; behavior = the methods it supports. One-to-one mapping: reference, fields, methods.
2. **Q: TRICKY — Two objects, same state. Are they equal?** A: Under value equality (overridden `equals`), yes; under identity (`==`), no. "Equal" is undefined until you say which notion — that's the trap the question tests.
3. **Q: When is `a.equals(b)` true but `a == b` false?** A: Always when two *distinct* objects have equal state and the class overrides `equals`. Example: `new Integer(5).equals(new Integer(5))` is true; `==` is false (for ints > 127 via boxing, note the autoboxing cache makes `Integer.valueOf(5) == Integer.valueOf(5)` true — another trap).
4. **Q: What happens if you use a mutable object as a HashMap key and mutate it?** A: Its `hashCode()` changes but its bucket doesn't; lookups fail (returns null / can't find) — the entry becomes orphaned. Fix: use immutable keys (String, Integer, record) or don't mutate after insertion.
5. **Q: What is the equals/hashCode contract?** A: If `a.equals(b)` then `a.hashCode() == b.hashCode()` (consistency); also reflexivity, symmetry, transitivity, and consistency with itself; `equals(null)` is false. Violating it breaks HashSet/HashMap.
6. **Q: SCENARIO — Design `Money` and `Account`: which uses identity, which uses state?** A: `Money` is a value object — identity-free, compared by state (`new Money(100).equals(new Money(100))` true); `Account` is an entity — identity-bearing (`account.getId()`), even if two accounts have equal balances.
7. **Q: PRACTICAL — A colleague overrode `equals` but not `hashCode`. What breaks?** A: `HashMap`/`HashSet`: equal objects hash to different buckets, so the set contains duplicates and lookups miss — the class silently violates the contract.
8. **Q: Does changing state change identity?** A: No. `setEmail` changes state; the reference (identity) is unchanged. Changing identity would require a new object (reassignment).
9. **Q: TRICKY — `String` has value semantics in Java. How?** A: `String` is an object (identity exists) but `equals` is overridden for value comparison, and it's immutable so state can't change mid-hash — Java gives you "value semantics" on an object via immutability + overridden `equals`.
10. **Q: Why do DTOs/records emphasize state?** A: Data-transfer objects carry state between layers (serialization needs state); identity/behavior are either absent or trivial — records auto-generate value `equals`/`hashCode`/`toString` because DTOs are pure state.
11. **Q: SCENARIO — You must compare two `Order` objects for a report. Identity or value?** A: Depends on intent: for a unique order → compare by `id` (identity-derived); to detect content changes → compare by fields (state). Reports usually need content comparison; dedup needs id.
12. **Q: What is object aliasing and why is it dangerous?** A: Two references to the same object (`User c = a;`) — mutating through one is visible through the other. If a library mutates an aliased object you pass it, your state changes unexpectedly (defensive copies fix this).
13. **Q: PRACTICAL — What does `java.time.LocalDate` demonstrate about state?** A: It's an immutable value object — state never changes; every operation returns a new object. This makes it hash-safe and thread-safe; the pattern is "immutable value types for state that should not change."
14. **Q: What role does behavior play in encapsulation?** A: Behavior (methods) is the *only* sanctioned way to change state; the object's methods are the guard that keeps state consistent (invariants). No behavior → no way to enforce rules.

## 14. Follow-Up Questions
1. **Q: What is the difference between equality and equivalence?** A: Equality compares objects (typically `equals`); equivalence is a coarser relation (e.g., `compareTo() == 0` vs `equals`) used in `TreeMap`/`TreeSet`; they should agree or you get subtle bugs.
2. **Q: Why does `Integer` cache `-128..127`?** A: Small ints are common; `Integer.valueOf` caches them so `==` (identity) often coincides with value for that range — a classic "works but is implementation detail" gotcha for `==` on boxed values.
3. **Q: What's a "value object" in DDD?** A: An object defined by its state alone, immutable, with value equality (`Money`, `DateRange`); identity is irrelevant and often hidden. Contrast with entities that have identity.
4. **Q: How does serialization treat these three?** A: Serialization persists *state* only; identity is reconstructed (new references) on deserialize; behavior is code, not data — it comes from the class, not the serialized bytes.

## 15. Coding Example
A complete, correct entity + value object example:
```java
import java.util.Objects;

public final class Money {                       // VALUE OBJECT
    private final long cents;
    private final String currency;
    public Money(long cents, String currency) {
        this.cents = cents; this.currency = currency;
    }
    public Money add(Money o) {
        if (!currency.equals(o.currency)) throw new IllegalArgumentException("currency mismatch");
        return new Money(cents + o.cents, currency);       // returns new object, never mutates
    }
    @Override public boolean equals(Object o) {           // state-only equality
        if (!(o instanceof Money m)) return false;
        return cents == m.cents && currency.equals(m.currency);
    }
    @Override public int hashCode() { return Objects.hash(cents, currency); }
}

public final class Account {                       // ENTITY
    private final String accountId;                // identity
    private Money balance;                         // mutable state

    public Account(String accountId, Money initial) {
        this.accountId = accountId; this.balance = initial;
    }
    public String getAccountId() { return accountId; }
    public Money getBalance() { return balance; }
    public void deposit(Money m) { balance = balance.add(m); }   // behavior guards state

    public static void main(String[] args) {
        Account a = new Account("ACC-1", new Money(100, "USD"));
        Account b = new Account("ACC-2", new Money(100, "USD"));
        System.out.println(a.getBalance().equals(b.getBalance())); // true (same state)
        System.out.println(a.equals(b));                           // false (different identity; equals not overridden)
        System.out.println(a.getAccountId().equals(b.getAccountId())); // false
        a.deposit(new Money(50, "USD"));
        System.out.println(a.getBalance());        // Money{cents=150}
    }
}
```
```python
from dataclasses import dataclass

@dataclass(frozen=True)                # frozen = immutable = value object
class Money:
    cents: int
    currency: str
    def add(self, o: "Money") -> "Money":
        if self.currency != o.currency: raise ValueError("currency mismatch")
        return Money(self.cents + o.cents, self.currency)   # new object

class Account:
    def __init__(self, account_id: str, balance: Money):
        self.account_id, self.balance = account_id, balance   # id = identity, balance = state
    def deposit(self, m: Money) -> None:
        self.balance = self.balance.add(m)
```

## 16. Industry Usage
- **Domain-Driven Design (Eric Evans)**: the entity-vs-value-object distinction is the heart of tactical DDD; every production domain model (orders, accounts, customers) makes this call explicitly.
- **Java standard library**: `String`, `Integer`, `BigDecimal`, `LocalDate` are immutable value objects; entity-like mutable classes (`ArrayList`, `HashMap`) rely on identity + carefully specified `equals`.
- **JPA/Hibernate**: entities carry identity (`@Id`); Hibernate compares entities by id for dirty checking and caching; value objects are mapped as `@Embeddable` (state only).
- **Concurrency**: immutable value objects (records, `String`) are safe to share across threads — identity/state design decisions are concurrency decisions.
- **APIs/DTOs**: REST payloads are pure state (JSON) — serialization strips identity and behavior; the receiving system re-establishes its own identity.

## 17. References
- Joshua Bloch, *Effective Java* — Items 10–17 (equals, hashCode, immutability, composition).
- Martin Fowler, *Patterns of Enterprise Application Architecture* — "Value Object", "Identity Field".
- Eric Evans, *Domain-Driven Design* — entities vs value objects.
- Oracle Java Tutorials, "Object as a Superclass" (equals/hashCode): https://docs.oracle.com/javase/tutorial/java/IandI/objectclass.html
- Java Language Specification, Ch. 8, §8.3 (fields), §8.4 (methods): https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html

## 18. Cheat Sheet
- Identity = reference/address/key (what `==`/`is` compares); immutable per object.
- State = field values (what `equals` compares when overridden).
- Behavior = methods (the only legal state-mutators under encapsulation).
- `equals` + `hashCode` must stay consistent — always override together.
- Mutable objects as hash keys = data loss (bucket no longer matches).
- Entities → identity; Value objects → state; DDD naming.
- Records/dataclasses auto-implement value semantics for pure-state DTOs.

## 19. Quiz
1. Identity of an object is most like: a) its field values b) its memory address/key c) its methods d) its class name → **b**
2. `a == b` in Java checks: a) state b) identity c) behavior d) class → **b**
3. Which is a value object? a) `Account` b) `Money` c) `User` d) `Session` → **b**
4. Mutable hash keys are dangerous because: a) `equals` breaks b) `hashCode` can change after insertion c) GC fails d) nothing → **b**
5. Overriding `equals` without `hashCode` breaks: a) `ArrayList` b) `HashSet` c) `StringBuilder` d) none → **b**
6. True or False: Changing an object's state changes its identity. → **False**

## 20. Flashcards
- **Q: The three properties of an object?** → **A:** Identity (reference), state (field values), behavior (methods).
- **Q: What does `==` compare?** → **A:** Identity (references). What does `equals` compare? → **A:** State (when overridden).
- **Q: Entity vs value object?** → **A:** Entity has identity (Account); value object is pure state (Money).
- **Q: Rule of equals/hashCode?** → **A:** Equal objects must have equal hashes; override together or collections break.
- **Q: Why are immutable objects hash-safe?** → **A:** State can't change, so `hashCode` never changes after insertion.
- **Q: Aliasing danger?** → **A:** Two references to one object — mutation through one affects the other.

## 21. Revision
Every object has identity (its reference, compared by `==`/`is`, immutable), state (field values, compared by `equals`), and behavior (methods that may mutate state). Value equality requires overriding `equals` and `hashCode` together — equal objects must hash equal or HashSet/HashMap corrupt. Mutable objects are unsafe as hash keys; immutable value objects (`Money`, `LocalDate`) are hash- and thread-safe. Domain design splits objects into identity-bearing entities (`Account`) and state-only value objects (`Money`). First-30-seconds answers: "`==` compares identity, `equals` compares state," and "identity never changes; state does."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Identity, state, and behavior?" | Formal Definition / Section 8 |
| "`==` vs `equals`?" | Example / Internal Working |
| "Why mutable hash keys are dangerous?" | Interview Q4 |
| "equals/hashCode contract?" | Interview Q5 / Section 14 |
| "Entity vs value object?" | Interview Q6 / Industry Usage |
| "What happens when you forget hashCode?" | Interview Q7 |
| "Does state change identity?" | Interview Q8 |
| "Why is String hash-safe?" | Interview Q9 / Section 16 |
