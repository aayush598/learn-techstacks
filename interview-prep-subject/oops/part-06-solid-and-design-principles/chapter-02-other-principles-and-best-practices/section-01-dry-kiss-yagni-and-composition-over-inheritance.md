# DRY, KISS, YAGNI, and Composition over Inheritance

> **TL;DR**: DRY (don't repeat yourself), KISS (keep it simple), YAGNI (you ain't gonna need it), and composition-over-inheritance are the *pragmatic* principles that calibrate SOLID — each has a sharp edge and a trap when over-applied.

## 1. Why Does This Exist?
SOLID tells you the *destination* of good design, but real developers also need *guardrails* that keep them from over-engineering (building abstractions nobody needs), under-engineering (copy-pasting behavior everywhere), and misusing the OO tools (inheritance for pure reuse). DRY, KISS, YAGNI, and composition-over-inheritance exist to answer the practical questions SOLID doesn't: **How much abstraction?** (YAGNI: only what you need now), **How simple?** (KISS: simplest that works), **When is duplication ok?** (DRY: never — but don't over-abstract), and **How do I reuse?** (composition over inheritance). Together they keep design *proportionate*: enough structure to be maintainable, not so much that the structure *is* the problem. Interviewers love them because they reveal judgment — anyone can recite SOLID, but knowing when *not* to apply DRY or when inheritance *is* right is the mark of experience.

## 2. How Does It Work?
- **DRY — Don't Repeat Yourself**: every piece of knowledge/behavior has a *single, unambiguous representation*. Find duplication → extract it into one method/class/module that all callers share. Caveat: duplication of *accidents* (similar-looking but differently-meaning code) must NOT be forced together — abstract only *true* repetition, or you create coupling (the opposite of DRY's intent).
- **KISS — Keep It Simple**: the simplest design that correctly solves the problem, with the least moving parts, is the best. Add structure *only* when a need demonstrates it.
- **YAGNI — You Ain't Gonna Need It**: don't build speculative features, abstractions, or extensibility until the need is real (the "second variation" rule from OCP applies here — build the seam when variation #2 appears, not #1).
- **Composition over inheritance**: prefer *has-a* (delegation/composition) over *extends* for reuse, because inheritance couples the subclass to the parent's internals (the fragile-base problem); use inheritance only for genuine *is-a* with a contract the subtype honors (LSP).

## 3. When Is It Used?
- **DRY**: duplicated business logic (tax calc in 3 places), copied constants, repeated validation — extract and single-source. *Not* when the copies look similar but mean different things.
- **KISS**: choosing a `for` loop over a framework; a simple `Map` over a custom class; YAGNI-trimming unused parameters and abstractions.
- **YAGNI**: resisting "let's add an interface so we *might* swap later"; skipping the 6th unused strategy; deferring config systems until configuration exists.
- **Composition over inheritance**: a `Window` *has-a* `Border`; a `Car` *has-a* `Engine`; a logger *has-a* a formatter — reuse by delegation. Inheritance remains for true is-a (a `Dog` *is-a* `Animal` with a real contract).

## 4. Why Wasn't Another Approach Chosen?
- *Why not maximum reuse via abstraction (over-DRY)?* Forcing two merely-similar code paths into one abstraction makes every caller dependent on the shared shape; when the paths diverge, you pay for the coupling you created. DRY's *goal* (one source of truth) must not become "no two similar lines ever."
- *Why not maximum simplicity (everything inline)?* KISS without DRY produces copy-paste sprawl — code that's "simple" to write and expensive to change. KISS means *simplest correct maintainable*, not "least abstraction."
- *Why not build everything speculatively (anti-YAGNI)?* Unused abstractions are dead weight and cognitive load, and they get the *shape* wrong (you'll build what you guessed, not what you need) — rework is cheaper than guessing (the "you aren't gonna need it" insight is about *waste*, not laziness).
- *Why not inherit for everything (anti-composition)?* Inheritance reuses *implementation*, dragging in the parent's internals and public surface; composition reuses *behavior* through a narrow delegation. Since LSP (Part 06 ch-01) requires true substitutability, inheritance is a *contract* decision, not a *reuse* shortcut.
- *Why not dogmatically follow any one?* Each principle is a *heuristic* with a countervailing force — DRY↔KISS (too much abstraction hurts), YAGNI↔preparation (real seams are needed before they're "needed"), composition↔inheritance (real is-a exists). Judgment = knowing when the counter-force wins.

## 5. Intuition
- **DRY**: one light switch for a room, not ten switches each wired to a copy of the circuit. Change the wiring once, all lights follow. Duplication is ten switches that drift out of sync.
- **KISS**: a bicycle, not a unicycle-with-training-wheels-with-a-fan. The simplest machine that gets you there reliably beats the clever one you'll have to maintain.
- **YAGNI**: don't build the second garage before you own a first car. Preparing for a car you may never buy is *waste*; you can build the garage when the car arrives (faster and to the right size).
- **Composition over inheritance**: hiring a plumber when the sink leaks (delegate the skill) vs giving birth to a plumber (inherit the whole family, including the odd uncle). You want the *skill*, not the *family* — you want to *have* a plumber, not *be* one.

## 6. Real-World Analogy
A **restaurant kitchen**:
- **DRY**: one recipe for the house sauce, used by every dish — change the recipe, every dish updates. If each chef kept a personal copy, three dishes would drift apart (duplication bug).
- **KISS**: the kitchen has a prep table, knives, and two burners — not a molecular-gastronomy lab with 40 gadgets. The simplest kitchen that serves the menu is easier to keep clean, staff, and fix.
- **YAGNI**: they didn't buy the pasta machine "in case pasta becomes popular" — they buy it when the first pasta order arrives, sized to *that* demand.
- **Composition over inheritance**: the chef *uses* the sous-chef and the dishwasher (has-a) rather than teaching every new hire to be a born-sous-chef-child-of-the-head-chef (inheritance of the whole family). The kitchen composes roles; it doesn't inherit them.

## 7. Formal Definition
- **DRY (The Pragmatic Programmer, Hunt & Thomas)**: "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." Duplication of *knowledge* (rules, logic, contracts) is the enemy; duplication of *coincidence* (similar-looking but independent code) is acceptable and must not be forced together.
- **KISS**: the simplest design/implementation that fully and correctly satisfies requirements, minimizing accidental complexity; complexity added without demonstrated need is a defect.
- **YAGNI (extreme-programming folklore, Ron Jeffries)**: don't implement functionality or structure until it is actually needed; speculative generality is waste because it is built on guesses about the future, and the real need will almost always require rework.
- **Composition over inheritance (Design Patterns/GoF)**: favor object composition ("has-a": one object delegating to another) over class inheritance ("is-a") for code reuse; inheritance couples subclass to superclass and should be reserved for true subtype relationships that honor LSP.

## 8. Example
```java
// DRY violation: the same validation knowledge in two places
class OrderService {
    boolean place(Order o) { if (o.amount() <= 0) throw new IllegalArgumentException(); return true; }
}
class RefundService {
    boolean refund(Order o) { if (o.amount() <= 0) throw new IllegalArgumentException(); return true; }
}
// DRY fix: single authoritative representation
class OrderPolicy { static void validate(Order o) { if (o.amount() <= 0) throw new IllegalArgumentException(); } }
// now both services call OrderPolicy.validate(o) — change the rule once

// YAGNI violation: an interface + 3 strategies for a single, fixed behavior
interface Persist { void save(Object o); }       // ← only one implementation exists today
class DbPersist implements Persist { public void save(Object o) {} }
// fix: write DbPersist directly; add the interface when a second storage appears

// Composition over inheritance (preferred for reuse):
class Logger {                                       // has-a Writer
    private final Writer w;
    Logger(Writer w) { this.w = w; }                 // delegate, don't extend
    void log(String m) { w.write(m); }
}
// vs inheritance-for-reuse (couples you to Writer's family tree):
class Logger2 extends Writer { ... }                 // fragile-base coupling
```

## 9. Internal Working
1. **DRY**: hunt for *knowledge* duplication — identical business rules, magic constants, format logic — via `rg`/IDE duplicate detection, then extract to one home (method, constant, class, config). Distinguish *true* (same knowledge) from *coincidental* (same shape, different meaning) duplication — force only the former together.
2. **KISS**: review every added abstraction, parameter, and framework with "does a current requirement justify it?" If the answer is "it might help later" — that's YAGNI, cut it.
3. **YAGNI**: the "rule of three" heuristic — consider abstracting/extracting on the *third* occurrence of a pattern, not the first or second (which is YAGNI protection until variation is real).
4. **Composition**: detect inheritance used for reuse (`class X extends Util`) — extract the reused behavior into a collaborator, delegate through a field, inject the collaborator (DI), delete the extends.
5. **Balance check**: after applying, verify the *net* effect — fewer reasons to change, not more; simpler mental model, not a forest of indirection. Each principle's success metric is *maintainability*, not "lines removed."

## 10. Time Complexity
- All four are *design-time* principles — zero runtime cost, zero runtime benefit on their own.
- Maintenance economics: DRY turns a multi-file rule change into a one-file change (developer-time saving); YAGNI avoids the cost of building and *maintaining* speculative code; KISS reduces cognitive load (bug rate correlates with complexity); composition keeps change localized (fewer recompiles/retests per change).
- Over-applied versions *increase* cost: premature abstraction (DRY/YAGNI failure) makes every change touch more files; inheritance reuse makes every parent change ripple to children.

## 11. Advantages
- **DRY**: one source of truth → consistent behavior, single point of fix, less drift.
- **KISS**: easy to understand, review, test, and debug; lower bug surface.
- **YAGNI**: no dead code, no wrong-shaped guesses, faster delivery, lower maintenance.
- **Composition**: loose coupling (a narrow delegation seam), easy mocking, no fragile-base exposure; the subtype contract isn't polluted by reuse.

## 12. Disadvantages
- **DRY over-applied**: premature abstraction, coupling of independent code, harder to read (indirection), and the "abstraction inversion" smell.
- **KISS over-applied**: duplicate sprawl, no structure for real growth, "simple" code that's expensive to change.
- **YAGNI over-applied**: missing seams that were actually imminent; refactoring under deadline pressure later.
- **Composition over-applied**: class/object explosion (delegation everywhere), ceremony, and *denying* legitimate is-a modeling that would be clearer.

## 13. Interview Questions
1. **Q: What is DRY?** A: Every piece of *knowledge* should have a single, authoritative representation — don't duplicate rules/logic; extract and share. It targets duplicated *knowledge*, not coincidental similarity.
2. **Q: What's the difference between DRY and "don't duplicate code"?** A: DRY is about *knowledge* — the same *meaning* appearing twice (a business rule). Two methods with similar *shape* but different meaning are not a DRY violation; forcing them together creates *coupling*. "Don't duplicate code" is the naive reading that causes premature abstraction.
3. **Q: TRICKY — Two classes have identical-looking `if` blocks but different semantics. DRY?** A: No — that's *coincidental* duplication. DRY would couple them wrongly; the fix is to *not* merge them (KISS) and instead make each one's knowledge explicit. Forcing them together is the classic over-DRY bug.
4. **Q: What is YAGNI, and how does it balance OCP?** A: YAGNI: don't build speculative features/seams. OCP wants extensibility — but extensibility *for the variations that exist*. The reconciliation: build the seam when the *second* variation appears (then OCP pays), not before the first (YAGNI's call).
5. **Q: SCENARIO — An engineer adds an interface + factory "so we can swap later" for a single storage class. Review?** A: Flag it as YAGNI — no second implementation exists. Write the concrete class now; introduce the interface when a real second storage shows up (that's also when you'll know the *right* abstraction).
6. **Q: PRODUCTION — When is KISS wrong?** A: When "simplicity" means skipping structure you *currently* need — a service that needs testing but has no seam, or duplicated logic to avoid a shared method. KISS is *simplest correct maintainable*, not *least code*. It also yields to DRY: the simplest thing is often the extracted, single-source one.
7. **Q: TRICKY — Is "prefer composition over inheritance" a ban on inheritance?** A: No — it's a *preference*. Inheritance is correct when there's a true is-a relationship whose contract the subtype honors (LSP) and where you're *not* using inheritance merely for code reuse. The adage targets *reuse-by-inheritance*, not *modeling-by-inheritance*.
8. **Q: How do you choose between composition and inheritance?** A: Ask: is the relation a genuine is-a (a `Dog` IS an `Animal`, substitutable — LSP) or a has-a (a `Dog` HAS a `Vet`)? If you'd subclass just to reuse methods, compose instead: extract the behavior into a collaborator and delegate. Is-a + contract → inheritance; has-a or reuse-only → composition.
9. **Q: SCENARIO — A `Car` needs `Engine` behavior. Inherit or compose?** A: Compose — a car *has* an engine; it isn't a specialization of Engine. `class Car { private final Engine engine; void start() { engine.start(); } }`. Inheritance (`class Car extends Engine`) would force every Engine change to ripple into Car and pollute Car's public surface.
10. **Q: PRODUCTION — DRY across a microservice boundary?** A: *Knowledge* shared across services (a contract/schema) must be single-sourced (a shared library/DTO), but *implementation* duplication across services is often *acceptable* — each service can evolve independently, and shared libraries become coupling. DRY applies within a bounded unit; cross-boundary, favor explicit contracts over forced code-sharing.
11. **Q: TRICKY — Is "rule of three" a real principle?** A: It's the *YAGNI-tuned* heuristic for DRY: extract on the *third* occurrence — after the pattern has proven itself (1st/2nd: YAGNI; 3rd: DRY). Not a law, but a widely-used calibration between premature abstraction and duplicate sprawl.
12. **Q: How do these principles relate to SOLID?** A: SOLID defines the target shape; DRY/KISS/YAGNI govern *how much* structure to build toward it (YAGNI limits abstraction, KISS limits complexity, DRY removes duplication); composition-over-inheritance is the preferred *mechanism* for the reuse SOLID's OCP/LSP/DIP assume. SOLID without them = over-engineering; them without SOLID = unfocused tidiness.
13. **Q: SCENARIO — Your team copy-pastes a validation rule in 5 places. Now the rule changes.** A: That's DRY biting: 5 edits, 5 chances to miss one, 5 tests to update. Extract to one `validate()` (or annotation/validator), call it everywhere, change once. Then add a test on the single source so the rule is enforced in one place.
14. **Q: PRODUCTION — An inherited class hierarchy is now 6 levels deep with only method reuse. Refactor?** A: Likely composition-over-inheritance territory: the deep hierarchy is reuse-by-inheritance (fragile-base risk, LSP doubt). Extract shared behavior into composed helpers; flatten to genuine is-a levels. Deep trees built for *reuse* are the #1 smell this adage targets.

## 14. Follow-Up Questions
1. **Q: How do DRY/KISS/YAGNI interact with code smells?** A: Smells (Part 06 ch-02 s3) are the *symptoms* of principle violation: duplicated code = DRY failure, speculative generality = YAGNI failure, long method/complexity = KISS failure, deep inheritance = composition-over-inheritance failure. Refactoring to the principles *is* removing smells.
2. **Q: Is "composition over inheritance" related to the Composite pattern?** A: The *principle* (has-a over is-a for reuse) and the *Composite pattern* (tree structures of same-interface objects) share the word but are different: the principle is a reuse heuristic; the pattern is a structural design (Part 07).
3. **Q: What is "abstraction inversion"?** A: The over-DRY smell where you've abstracted so aggressively that trivial operations require digging through layers of indirection — the point where DRY's benefits inverted into complexity. The fix is YAGNI-trimming: collapse layers no caller uses.
4. **Q: When should you deliberately violate DRY?** A: Across a *public API/boundary* (copying a small adapter per integration keeps clients decoupled), when the "duplicated" code is *about to diverge* (two features evolving differently), or when sharing would introduce cross-module coupling — deliberate duplication with a comment beats premature coupling.

## 15. Coding Example
```java
// COMPOSITION OVER INHERITANCE — reuse by delegation
interface Formatter { String format(String s); }        // narrow seam
class Upper implements Formatter { public String format(String s) { return s.toUpperCase(); } }
class Logger3 {                                          // has-a, not is-a
    private final Formatter f;
    Logger3(Formatter f) { this.f = f; }
    void log(String m) { System.out.println(f.format(m)); }
}
// DRY — single source of truth for the rule
class BookingPolicy {
    static void assertBookable(Booking b) {
        if (b.capacity() < b.people()) throw new IllegalStateException("over capacity");
    }
}
class AirlineService { void book(Booking b) { BookingPolicy.assertBookable(b); } }
class TrainService  { void book(Booking b) { BookingPolicy.assertBookable(b); } }  // same rule, one home
// YAGNI — no interface until the 2nd storage
class DiskStore { void store(byte[] d) { /* write */ } }   // concrete today; extract seam when needed

public class Main {
    public static void main(String[] args) {
        Logger3 l = new Logger3(new Upper());
        l.log("ready");                                   // READY
        BookingPolicy.assertBookable(new Booking(10, 4)); // rule enforced in one place
    }
}
```

## 16. Industry Usage
- **Every codebase**: DRY extraction is the most common refactor; "rule of three" guides teams; code-review bots flag duplicates.
- **Go**: strongly favors composition (embedding is *composition*; there's no inheritance) — the adage taken to its language-level extreme.
- **Java ecosystem**: composition-over-inheritance is why `Effective Java` Item 18 says "prefer composition over inheritance"; Spring's DI *forces* composition (beans are collaborators, not parents).
- **Extreme Programming / Agile**: YAGNI is a core XP value, applied at the story level — build exactly the current iteration's behavior.
- **Product/API design**: KISS drives "minimal viable API"; YAGNI drives not shipping speculative endpoints; DRY drives single-source contracts (shared schemas, OpenAPI).

## 17. References
- Andrew Hunt & David Thomas, *The Pragmatic Programmer* — DRY, orthogonality.
- Erich Gamma et al., *Design Patterns (GoF)* — "Prefer composition over inheritance" (intro).
- Joshua Bloch, *Effective Java*, Item 18 — "Favor composition over inheritance."
- Robert C. Martin, *Clean Code* — small functions, meaningful names (KISS in practice).
- Kent Beck / Ron Jeffries, Extreme Programming — YAGNI as an XP practice.

## 18. Cheat Sheet
- DRY = single authoritative representation of *knowledge*.
- Coincidental similarity ≠ DRY violation — don't force-merge.
- KISS = simplest correct maintainable solution.
- YAGNI = no speculative structure; extract at variation #2 / rule of three.
- Composition over inheritance = reuse by delegation; is-a+contract → inheritance.
- Trade-offs: over-DRY → coupling/abstraction inversion; over-KISS → sprawl; over-YAGNI → missing seams; over-composition → class explosion.
- These calibrate SOLID, not replace it.
- Deep inheritance for reuse = the #1 smell to fix with composition.

## 19. Quiz
1. DRY targets duplication of: a) code b) knowledge c) files d) comments → **b**
2. YAGNI says: a) build all possible features b) build only what's needed now c) never abstract d) always use interfaces → **b**
3. Composition over inheritance is: a) a ban b) a preference c) a law d) a metric → **b**
4. The "rule of three" guides: a) testing b) when to extract c) naming d) refactoring timing → **b**
5. Is-a with a real contract → use: a) composition b) inheritance c) neither d) DRY → **b**
6. True or False: DRY means never having similar-looking code. → **False** (coincidental similarity is fine)

## 20. Flashcards
- **Q: DRY definition?** → **A:** Single authoritative representation of each piece of knowledge.
- **Q: When NOT to DRY?** → **A:** Coincidental similarity (different meanings) — merging couples wrongly.
- **Q: KISS?** → **A:** Simplest correct maintainable solution.
- **Q: YAGNI?** → **A:** No speculative structure; build when variation #2 exists.
- **Q: Composition over inheritance?** → **A:** Reuse by delegation; inheritance only for true is-a + contract.

## 21. Revision
DRY (one authoritative source per piece of *knowledge* — not coincidental similarity), KISS (simplest correct maintainable), YAGNI (no speculative structure; extract at the second variation / rule of three), and composition over inheritance (reuse by delegation; inheritance only for genuine is-a that honors LSP) are the pragmatic guardrails calibrating SOLID. Each has a failure mode when over-applied: over-DRY → premature abstraction/coupling; over-KISS → sprawl; over-YAGNI → missing seams; over-composition → class explosion. They cost zero at runtime but shape maintenance economics. First-30-seconds answer: "DRY = one source of truth for knowledge, not for shape; KISS/YAGNI = simplest and least structure that meets real need; compose has-a, inherit only true is-a."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is DRY?" | Interview Q1 / Section 2, 7 |
| "DRY vs don't duplicate code?" | Interview Q2 |
| "YAGNI vs OCP balance?" | Interview Q4 / Section 4 |
| "Ban on inheritance?" | Interview Q7 |
| "Composition vs inheritance choice?" | Interview Q8 / Section 7 |
| "DRY across service boundaries?" | Interview Q10 |
| "Rule of three?" | Interview Q11 |
| "Deep inheritance refactor?" | Interview Q14 |
