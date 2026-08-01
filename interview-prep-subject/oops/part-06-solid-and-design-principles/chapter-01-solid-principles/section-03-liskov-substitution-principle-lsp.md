# Liskov Substitution Principle (LSP)

> **TL;DR**: If `S` is a subtype of `T`, then objects of `S` must be usable wherever objects of `T` are expected, **without breaking the base's behavioral contract** (preconditions, postconditions, invariants) — signature compatibility is not enough.

## 1. Why Does This Exist?
Inheritance promises a *contract*: every `Animal` can `speak()`, every `Bird` can `fly()`. The compiler only checks *signatures* — but the base class's *behavioral promises* (what `fly()` means, what `setWidth` guarantees) are silently inherited too. If a subclass `Ostrich extends Bird` overrides `fly()` to throw `UnsupportedOperationException`, the *signature* check passes, and every piece of code that "programs to `Bird`" suddenly breaks at runtime. LSP exists because **polymorphism (Part 04) only works if subtypes honor the contract**: OCP's "safe extension" and DIP's "depend on abstractions" are both built on the assumption that a subtype is truly substitutable. Without LSP, one bad override silently corrupts every caller in the system. The principle (Barbara Liskov, 1987) turns inheritance from "reuse by code sharing" into "safe reuse by contract conformance."

## 2. How Does It Work?
LSP has a **behavioral** contract in three parts:
1. **Preconditions**: what must be true *before* the method runs — the subtype must not *strengthen* them (demand more than the base).
2. **Postconditions**: what must be true *after* — the subtype must not *weaken* them (guarantee less than the base).
3. **Invariants**: always-true properties of the base (e.g., a `Rectangle`'s width/height are non-negative) — the subtype must preserve them.
Plus the *history rule*: methods that should be immutable can't be "mutable in the subclass."
Concretely: every subtype operation must be substitutable for its base counterpart — same observable behavior from the caller's perspective. The classic tests: "would this break if the reference were typed as the base?", "does this override weaken the base's guarantees?", "does calling through the base interface still work?"

## 3. When Is It Used?
- **Designing inheritance**: before subclassing, ask "is this really an is-a with the same contract, or an is-a with different behavior?" (the `Square`-as-`Rectangle` trap).
- **Detecting violations**: overrides that throw, ignore input, return "less", mutate invariants, or add requirements callers can't satisfy.
- **Contract enforcement**: using `@CheckReturnValue`, assertions, or `Objects.requireNonNull` to encode pre/postconditions so subtypes can't drift.
- **Refactoring**: when an override breaks a caller, the fix is usually "don't inherit — compose" (Part 03 ch-02) or "restructure the hierarchy so the contract fits."
- **Not for**: type-checking tools or language-level guarantees — LSP is a *design-time* discipline the compiler won't catch.

## 4. Why Wasn't Another Approach Chosen?
- *Why not just rely on the type system?* Types check signatures; LSP is about *behavioral* substitutability that types can't express (a `Bird` signature passing `fly()` to an ostrich is type-legal). Languages that tried to encode contracts (Eiffel's Design by Contract) got closer but still couldn't prove all behavioral properties.
- *Why not "composition over inheritance" instead?* Composition sidesteps LSP entirely (no subtype relation → no contract to break) — which is *why* the adage exists. But inheritance remains correct and concise where the contract genuinely holds; LSP tells you *when* inheritance is safe.
- *Why not just catch the exceptions at runtime?* A thrown `UnsupportedOperationException` is LSP's runtime symptom — but every caller now needs defensive handling, and failures surface late. The principle's value is *preventing* the bad hierarchy, not handling its fallout.
- *Why a "behavioral" principle rather than "signature" rules?* Signature rules (covariant returns, no narrowing params) are the *necessary* but insufficient part; the behavioral half (pre/postconditions) is what actually breaks systems.

## 5. Intuition
A **contract of trust**. When a base class promises "every bird flies," every caller builds on that promise. An ostrich is a *kind of bird* by name (is-a at the type level) but doesn't fulfill the promise — so trusting code that says "call `fly()` on your birds" breaks. LSP says: the subtype must fulfill the *promise*, not just the name. Think of a driver's license: a "motor vehicle" promise (can drive on roads) — a forklift isn't issued a standard license even though it's "motorized equipment," because it can't fulfill the promise of road use. Inheritance should be issued only where the *behavioral* promise holds, not the vocabulary.

## 6. Real-World Analogy
A **payment terminal and card brands**. The terminal (caller) expects every card to honor the promise "insert → PIN → process → eject." Every brand (Visa, Mastercard, Amex) is substitutable: same physical flow, same guarantees. Now imagine a "card" that instead of processing, prints "not supported" — it *looks* like a card (is-a), but the terminal's trust breaks. The *terminal* is written once against the card contract; each brand must fulfill it — that's LSP: the whole payment system's safety depends on every "card" honoring the shared behavioral contract, not just sharing the shape.

## 7. Formal Definition
**Liskov Substitution Principle** (Barbara Liskov, 1987): "Let Φ(x) be a property provable about objects x of type T. Then Φ(y) should be provable for objects y of type S, where S is a subtype of T." In software terms: a subtype `S` is substitutable for `T` iff every client of `T` behaves correctly when given an `S`. Operational rules:
- **Preconditions** of `S` must be *no stronger* than `T`'s (S must accept at least what T accepts — same or weaker requirements).
- **Postconditions** of `S` must be *no weaker* than `T`'s (S must guarantee at least what T guarantees).
- **Invariants** of `T` must be preserved by `S`.
- **Exceptions**: `S` must not throw new unexpected exceptions on legal inputs.
- **History rule**: `S` must not add constraints a caller can't undo (e.g., making a supposedly-mutable field immutable from outside's perspective).
A violation is detected behaviorally: a caller written against `T` that fails only when handed an `S`.

## 8. Example
```java
// VIOLATION (classic Square-Rectangle)
class Rectangle {
    protected int w, h;
    void setWidth(int w) { this.w = w; }
    void setHeight(int h) { this.h = h; }
    int area() { return w * h; }
}
class Square extends Rectangle {
    @Override void setWidth(int w) { this.w = this.h = w; }   // breaks base contract!
    @Override void setHeight(int h) { this.h = this.w = h; }
}
void demo(Rectangle r) {
    r.setWidth(5); r.setHeight(3);
    assert r.area() == 15;       // FAILS for Square: area() == 9 — the caller's expectation breaks
}
// FIX: no Square-as-Rectangle; separate type, or composition
class Square {                       // independent type with its own contract
    private final int side;
    Square(int side) { this.side = side; }
    int area() { return side * side; }
}
```
```java
// VIOLATION (Bird-Ostrich): signature ok, behavior breaks
class Bird { void fly() { /* ... */ } }
class Ostrich extends Bird { @Override void fly() { throw new UnsupportedOperationException(); } }
void letItFly(Bird b) { b.fly(); }        // crashes when b is an Ostrich
// FIX: restructure — fly is not a Bird invariant
class Bird {}
class FlyingBird extends Bird { void fly() {} }
class Ostrich extends Bird {}
```

## 9. Internal Working
1. **Signature check (compile-time)**: subtype must match the base signature — covariant returns allowed, no narrowing params (Part 04). This is the *first* gate.
2. **Behavioral check (design-time)**: for each override, verify preconditions aren't strengthened, postconditions aren't weakened, invariants preserved, no new exceptions, history preserved. Tools: unit tests that exercise the *base's* contract against *every* subtype.
3. **Detect at runtime**: `UnsupportedOperationException`, `AssertionError`, silently-wrong results, or different side effects when called through the base reference are LSP violation *symptoms*.
4. **Repair**: (a) remove the subtype relation (composition), (b) refine the hierarchy (move the violated operation up to a narrower supertype like `FlyingBird`), (c) if the base contract itself was wrong, fix *it* (rare — the contract is shared).
5. **Prevent**: encode the base's expectations as tests (`verifyContract(Class c)`), and prefer `final`/`sealed` hierarchies or composition over speculative subclassing.

## 10. Time Complexity
- Zero runtime cost — LSP is a design discipline; no dispatch or memory overhead.
- The "cost" is developer attention: contract tests per subtype and careful hierarchy design, repaid by avoiding production bugs that are expensive to trace (a violation can break callers far from the offending class).
- When violated, the *runtime* cost appears as uncaught exceptions or wrong results — the actual cost is correctness, not speed.

## 11. Advantages
- **Safe polymorphism**: every caller written against the base works for every subtype — OCP and DIP become trustworthy.
- **Correct reuse**: inheritance means *contract inheritance*, so overriding is behavior-preserving by construction.
- **Predictable hierarchies**: "is-a" is now a behavioral guarantee, not a naming convenience.
- **Testability**: a contract test run against all subtypes catches drift early.
- **Frameworks**: extension points (overrides) that don't crash the base logic.

## 12. Disadvantages
- **Contract-writing overhead**: making pre/postconditions explicit (assertions, tests, docs) takes discipline few codebases invest.
- **Hierarchy rigidity**: legitimate near-is-a cases (a rectangle-ish square) get *no* inheritance, forcing composition/restructuring — more code than the "obvious" (wrong) inheritance.
- **Detection is indirect**: LSP violations often surface far from the subtype (a caller's test fails mysteriously) — hard to attribute.
- **No tooling**: the compiler won't help; enforcement is human or contract-test-based.
- **Over-restriction**: zealously applying LSP can forbid useful hierarchies where the caller tolerates the difference (realistic but impure subtypes).

## 13. Interview Questions
1. **Q: What is LSP?** A: If `S` is a subtype of `T`, then `S` objects must be usable wherever `T` is expected without breaking the base's *behavioral* contract — preconditions no stronger, postconditions no weaker, invariants preserved.
2. **Q: Give a classic LSP violation.** A: Square-as-Rectangle: `setWidth(5); setHeight(3)` through a `Rectangle` reference must give area 15, but `Square` forces `w==h` → area 9. Also Bird→Ostrich overriding `fly()` to throw. Both pass the type checker, both break callers.
3. **Q: TRICKY — Is "Ostrich extends Bird throws on fly()" a compile error?** A: No — signatures match, so it compiles. LSP is *behavioral*: the *type system* can't catch it; it breaks at runtime when any `Bird`-typed caller invokes `fly()`. That's precisely why LSP must be a design discipline.
4. **Q: How do you detect an LSP violation in code review?** A: Look for overrides that throw unexpected exceptions, ignore parameters, return inconsistent values, weaken guarantees, or strengthen requirements; also test the *base's* contract against each subclass (a contract test suite).
5. **Q: SCENARIO — `Stack extends Vector` (JDK historical). Violation?** A: Yes — `Vector` allows inserting anywhere (`add(index, el)`), but a `Stack` violates LSP because it shouldn't allow arbitrary inserts; a caller using `Stack` as a `Vector` gets LSP-violating behavior. (The JDK *did* make this mistake — a famous example.)
6. **Q: PRODUCTION — You subclass a base and override a method to *do less*. Problem?** A: You've *weakened the postcondition* — callers depend on the base's guarantee ("returns a result", "throws on invalid"), and your override returns a default/ignores input → LSP violation. Either honor the contract or don't inherit (compose).
7. **Q: How does LSP relate to OCP?** A: OCP says "extend without modifying." The safety of that extension depends on every new subclass honoring the base contract — an LSP-violating subclass is an extension that silently breaks the closed core. LSP is OCP's safety net.
8. **Q: TRICKY — Can a subclass *strengthen* a postcondition?** A: Yes and that's *fine* — a stronger guarantee (always positive, always non-null) still satisfies the base's promise (the caller's expectation is met). LSP forbids *weakening* postconditions and *strengthening* preconditions — the directions that break callers.
9. **Q: SCENARIO — `Bird` has `setWingspan(int)`; `Ostrich` overrides to throw if `< 200`. Is that a violation?** A: Yes — the precondition "wingspan is any positive int" is strengthened to "≥ 200"; a caller that legally set 100 on `Bird` now breaks on `Ostrich`. That's a strengthened precondition.
10. **Q: PRODUCTION — "Every service impl I write extends a base; the base's methods throw NotImplemented." Problem?** A: That's the "Base/derived with throwing overrides" smell — the base *promises* behavior but subtypes renege (LSP violation). Prefer narrow interfaces the subtypes actually implement, or `abstract` methods forcing implementation.
11. **Q: How do you fix the Square-Rectangle problem properly?** A: Don't inherit — make `Square` its own type, or have *both* implement a `Shape` contract (`area()`) they each honor; the shape is the correct abstraction, the rectangle-relationship isn't a true is-a.
12. **Q: TRICKY — Does LSP forbid overriding at all?** A: No — it *governs* it. Overriding is the extension mechanism (Part 04); LSP requires the override to *preserve* the base's contract. Override freely; just don't change what the base promised.
13. **Q: How do design patterns respect LSP?** A: Patterns that take a strategy/interface assume substitutability (Strategy, Observer, Template Method's hooks) — LSP is silently assumed; patterns like the Template Method fail exactly when a subclass hook violates LSP.
14. **Q: PRODUCTION — You have a base contract test; a new subclass fails it. Options?** A: (1) Fix the subclass to honor the contract; (2) if it can't, it shouldn't be a subclass — extract to composition or restructure the hierarchy (e.g., split the base). The contract test *is* your LSP enforcement.

## 14. Follow-Up Questions
1. **Q: How does LSP relate to Design by Contract?** A: LSP is the *inheritance* instance of Design by Contract (Eiffel's `pre`/`post`/`invariant` clauses) — the rule "inherited preconditions are or-able, postconditions are and-able" is LSP made mechanical. Modern langs rarely enforce it, so LSP stays a discipline.
2. **Q: What is the "history rule" (constraint rule)?** A: A subtype must not allow the caller to undo a constraint the base enforced — e.g., if the base can't change a color after creation, the subclass can't allow it. It preserves the *temporal* part of the contract.
3. **Q: Does LSP apply to interfaces too?** A: Yes — implementations must honor the interface's behavioral contract; this is why "program to an interface" is only safe under LSP. Interface segregation (ISP) even helps: narrower interfaces carry weaker contracts, easier to honor.
4. **Q: How does Java's `Collection` hierarchy violate/respect LSP?** A: Mostly respects it; historical violations: `Stack extends Vector`, and unmodifiable views (`Arrays.asList(...).add()` throws `UnsupportedOperationException`) technically weaken postconditions — callers must check `isModifiable` first (a design compromise the ecosystem accepts).

## 15. Coding Example
```java
import java.util.*;
// Correct design: honor contracts through a shared abstraction
interface Shape { double area(); }
final class Rect implements Shape {         // final — no subclassing, no LSP risk
    private final double w, h;
    Rect(double w, double h) { this.w = w; this.h = h; }
    public double area() { return w * h; }
}
final class Square2 implements Shape {
    private final double side;
    Square2(double side) { this.side = side; }
    public double area() { return side * side; }
}
// Contract test: every Shape must satisfy "area is non-negative"
double totalArea(List<Shape> shapes) {
    double t = 0;
    for (Shape s : shapes) {
        double a = s.area();
        if (a < 0) throw new IllegalStateException("LSP violation: negative area from " + s.getClass());
        t += a;
    }
    return t;
}
public class Main {
    public static void main(String[] args) {
        System.out.println(totalArea(List.of(new Rect(5, 3), new Square2(4))));  // 31.0
    }
}
```
Both types honor `Shape`'s contract (`area()` ≥ 0, no side effects); any future `Shape` (a `Circle`) is substitutable — the caller never knows the concrete type and never breaks. Contrast the `Square extends Rectangle` version: `setWidth(5); setHeight(3)` yields 9, not 15, and the caller *does* break.

## 16. Industry Usage
- **JDK history**: `Stack extends Vector` is the canonical "we shouldn't have done that" LSP lesson; `Properties extends Hashtable` similar. The ecosystem learned: prefer composition/independent types.
- **Guava**: `ImmutableList` — never subclasses mutable collections in a way that violates contract; the immutability is enforced by design, not by throwing on mutation (well — `UnsupportedOperationException`, a *documented* compromise).
- **GoF patterns**: Strategy/State/Decorator all assume LSP-safe implementations; the Decorator's whole point is wrapping while *preserving* the interface contract.
- **Java Streams/`Optional`**: contracts are explicit (`ifPresentOrElse` guarantees), making substitutable implementations safe.
- **Testing**: contract-test libraries (e.g., parameterized contract tests, `equals`/`hashCode` contracts from `Object`) formalize LSP enforcement across subtypes.

## 17. References
- Barbara Liskov, "Data Abstraction and Hierarchy" (SIGPLAN 1987) — the original definition.
- Robert C. Martin, *Clean Architecture*, Ch. 9 — "The Liskov Substitution Principle".
- Robert C. Martin, *Agile Software Development* — the Rectangle/Square chapter.
- Bertrand Meyer, *Object-Oriented Software Construction* — Design by Contract (LSP's formal cousin).
- GeeksForGeeks, "Liskov Substitution Principle in Java": https://www.geeksforgeeks.org/liskov-substitution-principle-in-java/

## 18. Cheat Sheet
- LSP: subtype must be substitutable for base *behaviorally*.
- Preconditions: no stronger. Postconditions: no weaker. Invariants: preserved.
- No new exceptions on legal inputs; honor the history rule.
- Classic violations: Square-Rectangle, Bird-Ostrich, Stack-Vector.
- Compiler checks signatures only — LSP is design-time.
- Enforce with contract tests over all subtypes.
- Fix: compose, restructure hierarchy, or fix the base.
- LSP is the safety net for OCP and DIP.
- Strengthened postconditions are OK; strengthened preconditions are not.
- `final`/`sealed` classes reduce LSP surface area.

## 19. Quiz
1. LSP requires subtypes to: a) share signatures only b) preserve behavior c) be smaller d) have no fields → **b**
2. Square-as-Rectangle violates LSP because: a) types differ b) caller expectation breaks c) syntax d) performance → **b**
3. A subclass that strengthens a *postcondition*: a) violates LSP b) is fine c) crashes d) is illegal → **b**
4. Strengthening a *precondition*: a) fine b) LSP violation c) required d) impossible → **b**
5. Who defined LSP? a) GoF b) Barbara Liskov c) Alan Kay d) John von Neumann → **b**
6. True or False: The compiler can catch most LSP violations. → **False**

## 20. Flashcards
- **Q: LSP definition?** → **A:** Subtypes must be behaviorally substitutable for their base.
- **Q: Three contract rules?** → **A:** Preconditions no stronger; postconditions no weaker; invariants preserved.
- **Q: Classic violations?** → **A:** Square-Rectangle, Bird-Ostrich, Stack-Vector.
- **Q: Why compilers can't catch it?** → **A:** They check signatures, not behavior.
- **Q: How to enforce?** → **A:** Contract tests over every subtype.

## 21. Revision
LSP: a subtype must be *behaviorally* substitutable for its base — preconditions not strengthened, postconditions not weakened, invariants preserved, no unexpected exceptions, history rule honored. Type systems check signatures only, so violations (Square-Rectangle, Bird-Ostrich, Stack-Vector) compile and break at runtime. Detect via overrides that throw/ignore/weaken; enforce with contract tests run against all subtypes. Fix by composing instead of inheriting, restructuring the hierarchy, or (rarely) correcting the base contract. LSP is what makes OCP extensions and DIP dependencies safe. First-30-seconds answer: "Same signature isn't enough — the subtype must keep the base's promises (preconditions, postconditions, invariants) or every polymorphic caller breaks."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is LSP?" | Interview Q1 / Section 2, 7 |
| "Classic LSP violation?" | Interview Q2 / Section 8 |
| "Why compiles but breaks?" | Interview Q3 / Section 4 |
| "How to detect in review?" | Interview Q4 / Section 9 |
| "Stack extends Vector?" | Interview Q5 / Section 16 |
| "LSP and OCP relation?" | Interview Q7 / Section 4 |
| "Strengthened precondition?" | Interview Q9 |
| "How to fix Square-Rectangle?" | Interview Q11 / Section 8 |
