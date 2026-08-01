# Code Smells and Refactoring

> **TL;DR**: Code smells are *symptoms* of design problems (god class, feature envy, long parameter list, shotgun surgery, duplicated code); refactoring is the *behavior-preserving* restructuring that removes them — small steps, tests as the safety net, and the principles of this part as the destination.

## 1. Why Does This Exist?
Bad design doesn't announce itself — it shows up as code that's hard to change, easy to break, and painful to read. "Code smells" (Kent Beck's term, popularized by Fowler) are the **recognizable, repeatable patterns** that *predict* these problems before they bite: a 900-line class, a method with 8 parameters, a bug that requires fixing 5 files. Naming smells matters because naming is detection: "this is a Feature Envy" turns a vague unease into a specific, fixable diagnosis with a known remedy. Refactoring exists as the *safe* way to act on that diagnosis: **restructuring without changing behavior**, in tiny verifiable steps, so the fix never introduces a regression. Together they form the maintenance loop — you can't run a codebase for a year without needing both. Interviewers ask "what's wrong with this code?" to test exactly this: can you *diagnose* (smell) and *prescribe* (refactor)?

## 2. How Does It Work?
1. **Smell = symptom**: a code shape that *correlates* with maintainability problems. Detectable by reading (grep, naming, line counts), by tools (linters, complexity metrics), and by experience.
2. **Diagnose → prescribe**: each smell maps to a refactoring (a catalogued transformation): Long Method → Extract Method; Feature Envy → Move Method; God Class → Extract Class; Long Parameter List → Introduce Parameter Object; Duplicated Code → Extract Function/Class (DRY); Shotgun Surgery → Move/Consolidate (SRP).
3. **Refactor = behavior-preserving**: the transformation must not change observable behavior — output identical, tests green before and after each step.
4. **Small steps**: one tiny transformation at a time (rename, extract, move), run tests after each, commit when green. This keeps risk near zero.
5. **Destination**: the refactoring lands on the principles (SOLID, coupling/cohesion, DRY) — smells are their *absence*, refactoring is how you get back to them.

## 3. When Is It Used?
- **Before adding a feature**: refactor the touched area first (so the change is cheap and local) — the "campground rule."
- **After a bug**: the bug often lives *in* a smell (a god method's confusing branch); fixing the smell clears the bug's territory.
- **Code review**: smells are review findings — "this is Feature Envy, move the method."
- **Continuous hygiene**: regularly scheduled refactoring sprints; IDE-automated mechanical refactorings (rename, extract, inline) run constantly.
- **Not for**: speculative cleanup of untouched, working code (YAGNI — only refactor where change pressure exists), or large rewrites masquerading as refactoring (rewrites are *not* refactoring: they're risk).

## 4. Why Wasn't Another Approach Chosen?
- *Why not just rewrite the bad code?* Rewrites discard working behavior, take months, and often reproduce old bugs — Fowler: "when you feel the urge to rewrite, refactor instead." Refactoring preserves behavior step-by-step, keeping the system shippable the whole time.
- *Why not just write good code the first time?* Requirements evolve; even good first designs accumulate mismatch. Smells/refactoring are the *maintenance* discipline — the cost of change is controlled by tending the design, not by a one-time perfect plan.
- *Why small steps instead of big-bang changes?* Big-bang restructuring can't be verified (if tests break, you can't tell which change broke them); tiny steps give an "undo point" per step and a green state after each — the difference between safe refactoring and an act of bravery.
- *Why "smells" instead of hard rules/metrics?* Smells are *indicators*, not verdicts — a long method can be fine (high cohesion); a metric can be gamed. Fowler deliberately called them "smells" (like a smell of food) — "a hint that something might be wrong," requiring judgment, not just a rule.
- *Why refactor *toward* principles rather than "cleanliness"?* Principles give the refactoring a *destination* (a split class serves SRP, a moved method raises cohesion); "cleaner" with no destination produces churn without improvement — refactoring to a named principle is measurable.

## 5. Intuition
A smell is like a **check-engine light**: the car runs, but the light (a shape in the code) hints something expensive is coming — ignored, it becomes a breakdown (a bug that takes a day to find). Refactoring is the **annual tidy-up**: you don't rebuild the house; you move the books back to the shelf, put the knives in the right drawer, re-route the cable that's in the walkway — each move is small and safe, nothing lost, and the house works better for next year's additions. The skill isn't *not* making a mess (that's impossible); it's recognizing the mess early and tidying it in safe, small moves before it grows into a wreck.

## 6. Real-World Analogy
A **warehouse with an inventory system**. Over time, boxes pile in the wrong aisles (god class), the same part is stored in 5 places (duplicated code), and the "how to pack" instructions are split across 6 binders (shotgun surgery). You don't burn the warehouse and rebuild (rewrite) — you *re-shelve* one cartload at a time (small refactoring steps), verifying each item is still findable (tests green) before moving the next. You re-shelve *before* the next big shipment (feature work) so the shipment fits. Smells are the mismatched labels and overflowing aisles; refactoring is the disciplined re-shelving that keeps the warehouse efficient without ever losing a box.

## 7. Formal Definition
**Code smell**: a surface structure of code that indicates a *possible* deeper problem — a heuristic, not a proof, of violated design principles. (Kent Beck's term; Fowler's catalog: duplicated code, long method, large class, long parameter list, divergent change, shotgun surgery, feature envy, data clumps, primitive obsession, switch statements, parallel inheritance hierarchies, lazy class, speculative generality, message chains, middle man, inappropriate intimacy, refused bequest.)
**Refactoring** (Martin Fowler): "a disciplined technique for restructuring an existing body of code, altering its *internal structure* without changing its *external behavior*" — a sequence of small, behavior-preserving transformations (Extract Method, Move Method, Extract Class, Introduce Parameter Object, etc.), each validated by tests, the sum of which improves design without changing function.

## 8. Example
```java
// SMELL 1: Long Parameter List (5 params, hard to call, easy to misorder)
double price(double base, double taxRate, boolean discounted, double discountPct, double shipping) { ... }
// REFACTOR: Introduce Parameter Object → single cohesive carrier
record Pricing(double base, double taxRate, boolean discounted, double discountPct, double shipping) {}
double price(Pricing p) { ... }

// SMELL 2: Feature Envy — Shipping.label uses ONLY order's customer's city
class Shipping2 { String label(Order o) { return o.getCustomer().getAddress().getCity(); } }
// REFACTOR: Move Method → the data owner answers (LoD/cohesion)
class Order { String getCustomerCity() { return getCustomer().getAddress().getCity(); } }
// Shipping2.label(Order o) → o.getCustomerCity()

// SMELL 3: Duplicated Code (DRY violation)
class OrderService2 { boolean valid(Order o) { return o.amount() > 0 && !o.isFlagged(); } }
class RefundService2 { boolean valid(Order o) { return o.amount() > 0 && !o.isFlagged(); } }
// REFACTOR: Extract Method → single source of truth
class OrderPolicy { static boolean valid(Order o) { return o.amount() > 0 && !o.isFlagged(); } }
```
Each refactoring: identical behavior before/after, tests stay green, and the *shape* improves (fewer params, higher cohesion, DRY).

## 9. Internal Working
1. **Detect**: tooling (line counts, cyclomatic complexity, parameter counts, LCOM), grep (identical blocks), review (reading for the shapes).
2. **Triage**: a smell is a *candidate* — decide if the underlying problem is real (a long method that's genuinely cohesive may stay; a god class does not). Prioritize by change pressure: refactor what you're about to modify.
3. **Select refactorings** from the catalog (Fowler's), each mapped to the smell.
4. **Execute in tiny steps**: rename → extract → move → inline, one per test-green checkpoint; use IDE refactorings (which are *automated* small steps).
5. **Verify preservation**: tests must be identical in outcome before/after; the only allowed difference is internal structure.
6. **Check the destination**: after refactoring, confirm the *principle* improved (cohesion up, coupling down, SRP/OCP satisfied) — otherwise the change was churn.
7. **Guard**: add a *characterization test* first if the code lacks tests (capture current behavior, then refactor against it — the "seam" for legacy code).

## 10. Time Complexity
- No runtime cost or benefit — refactoring is internal structure only; algorithms don't speed up.
- Economics: refactoring reduces the *marginal cost of the next change*. A god-class change costs 1 file edit + full regression; after Extract Class, it's a local edit + focused test — the saving compounds per change (Fowler: "the purpose is to make change cheap again").
- The risk cost: a refactor done without tests or in big-bang fashion *adds* risk (regressions), which is why small steps + green checkpoints are non-negotiable.

## 11. Advantages
- **Cheaper future changes**: localize modification, shrink test blast radius.
- **Clearer code**: shorter methods, cohesive classes, named intent.
- **Bug habitat removal**: smells are where bugs breed; fixing them removes the habitat.
- **Safe**: behavior-preserving by construction (tests green each step) — shippable throughout.
- **Incremental**: no big-bang risk, no long unmergeable branches.

## 12. Disadvantages
- **Refactoring without tests is gambling**: you can't prove behavior is preserved (mitigate: characterization tests).
- **Over-refactoring**: polishing untouched, working code is churn (YAGNI) — and "refactoring" that adds new features is feature work, not refactoring.
- **No direct business value**: invisible to users; must be justified by change pressure, not aesthetics.
- **Merge conflicts**: refactoring touched files collide with concurrent feature branches (mitigate: small, frequent, committed).
- **Tools can lie**: IDE "safe" refactorings occasionally change semantics (e.g., overload resolution) — tests remain the final check.

## 13. Interview Questions
1. **Q: What is a code smell?** A: A surface structure that *hints* at a deeper design problem — a heuristic, not a bug. It predicts maintainability trouble (hard to change/test/understand) and maps to a known fix.
2. **Q: What is refactoring?** A: Restructuring *internal structure* without changing *external behavior* — a sequence of small, test-verified transformations that improve design while keeping the system working.
3. **Q: What's the difference between refactoring and rewriting?** A: Refactoring preserves behavior step-by-step, keeps the system shippable, and is verifiable at every checkpoint; rewriting discards and rebuilds — high risk, long duration, often re-introduces old bugs. Prefer refactoring.
4. **Q: TRICKY — A method is 120 lines but reads perfectly and is cohesive. Is it a smell?** A: Possibly not — smells are *heuristics*. A long but cohesive method may be fine; the smell is long methods that mix levels of abstraction or hold unrelated logic. Judgment over metrics.
5. **Q: SCENARIO — `Order` class is 800 lines: validation, persistence, email, reporting. Diagnose and fix.** A: That's a God Class (SRP violation, low cohesion, high coupling). Fix: Extract Class per responsibility — `OrderValidator`, `OrderRepository`, `OrderNotifier`, `OrderReport` — leaving `Order` with domain behavior; inject the extracted collaborators.
6. **Q: PRODUCTION — How do you refactor a 5000-line class with no tests?** A: First write *characterization tests* (capture current inputs→outputs as the safety net), then refactor in tiny steps with green checkpoints; start with the highest-change-pressure part. Never refactor a tested-in-our-heads legacy class big-bang.
7. **Q: What is Feature Envy, and what refactoring fixes it?** A: A method that uses another class's data/getters more than its own (low cohesion, high coupling, often LoD violation). Fix: Move Method — relocate the method to the class whose data it uses (or Extract Method + Move).
8. **Q: TRICKY — "Switch statements" smell: when is a switch OK?** A: The smell is a switch that dispatches on a *type tag* to behavior that should be polymorphic (OCP violation). A switch over an *enum for its own enum-ness* (state mapping, lookup table) is fine. Type-tag dispatch → Replace with Polymorphism (Part 04).
9. **Q: What is Shotgun Surgery?** A: One conceptual change requires touching *many* classes (the opposite of Divergent Change). It signals low cohesion / misplaced responsibility. Fix: Move Method/Consolidate so each change is local (SRP).
10. **Q: SCENARIO — `createOrder(a, b, c, d, e, f, g)` — 7 params. Fix?** A: Introduce Parameter Object (group related params into a record/class) and split the method if it mixes responsibilities. Fewer params = easier calling, clearer intent, higher cohesion.
11. **Q: PRODUCTION — What's the "campground rule"?** A: "Leave the campground cleaner than you found it" — before adding a feature to a smelly area, refactor *that area* first so your change is cheap and the code you touch ends up better. Refactoring is done where change pressure is, not everywhere at once.
12. **Q: TRICKY — Refactoring changed behavior slightly (an edge case). Was it a refactor?** A: No — by definition refactoring preserves behavior. If behavior changed, it was a *modification* (deliberate feature/bug fix) or a refactoring bug (your tests missed the edge). Tests must be green and behaviorally identical after true refactoring.
13. **Q: Name 5 smells and their refactorings.** A: (1) Long Method → Extract Method; (2) God Class → Extract Class; (3) Long Parameter List → Introduce Parameter Object; (4) Duplicated Code → Extract Function; (5) Feature Envy → Move Method. (Also: Shotgun Surgery → Move/Consolidate; Switch statements → Replace with Polymorphism.)
14. **Q: PRODUCTION — How do smells relate to the principles in this part?** A: Smells are *violated principles*: God Class = SRP+cohesion failure; Feature Envy = cohesion/LoD failure; Duplicated Code = DRY failure; Shotgun Surgery = SRP failure at module scale; Long Parameter List = coupling to data the caller shouldn't assemble. Refactoring is the road *back* to the principles (SOLID, DRY/KISS, coupling/cohesion).

## 14. Follow-Up Questions
1. **Q: What is "primitive obsession"?** A: Using primitives (`String`, `double`) where a domain type belongs — a `String phone`, a `double money`. Fix: Extract Class/Replace Primitive with Object (`Phone`, `Money`) — raises cohesion and removes scattered format/validation logic.
2. **Q: What is "inappropriate intimacy"?** A: Two classes using each other's internals excessively — coupled and low-cohesion. Fix: Move Method/Extract Class to separate concerns; or use a shared collaborator instead of reaching into each other.
3. **Q: What is "refused bequest"?** A: A subclass inherits methods/fields it doesn't use or throws on them — an LSP red flag (a `Square extends Rectangle` that refuses `setWidth`). Fix: prefer composition, or restructure the hierarchy so the subclass only inherits what it honors.
4. **Q: How do you prevent smells from returning?** A: Continuous refactoring as part of feature work (campground rule), code-review smell checklists, static analysis gates (complexity, LCOM, duplication), and architectural tests (ArchUnit) that encode the principles as testable invariants.

## 15. Coding Example
```java
// BEFORE — several smells in one method
class ReportService {
    String build(String title, String author, String date, List<String> lines, String footer, boolean verbose) {
        StringBuilder sb = new StringBuilder();                    // long parameter list
        sb.append(title).append(" by ").append(author).append(" (").append(date).append(")\n");
        for (String l : lines) {                                   // mixed abstraction levels
            if (verbose) sb.append("• ").append(l).append("\n");
            else sb.append(l).append("\n");
        }
        sb.append(footer).append("\n");
        return sb.toString();
    }
}
// AFTER — refactored: parameter object + extracted methods
record ReportSpec(String title, String author, String date, List<String> lines, String footer, boolean verbose) {}
class ReportService2 {
    String build(ReportSpec spec) {                               // 1 param instead of 6
        return header(spec) + body(spec) + footer(spec);
    }
    private String header(ReportSpec s) { return s.title() + " by " + s.author() + " (" + s.date() + ")\n"; }
    private String body(ReportSpec s) {
        StringBuilder sb = new StringBuilder();
        for (String l : s.lines()) sb.append(s.verbose() ? "• " : "").append(l).append("\n");  // each level its own method
        return sb.toString();
    }
    private String footer(ReportSpec s) { return s.footer() + "\n"; }
}
// Same output for every input; shape improved: 1 parameter, methods by abstraction level, cohesive.
```

## 16. Industry Usage
- **Every maintained codebase**: refactoring is routine — IDEs automate (Rename, Extract, Move, Inline); "refactor before feature" is a standard team practice.
- **Testing culture**: TDD produces the safety net that makes refactoring cheap; characterized tests unlock legacy refactoring (Michael Feathers, *Working Effectively with Legacy Code*).
- **Static analysis in CI**: PMD/Checkstyle/SonarQube flag complexity, duplication, LCOM, parameter counts — automating smell *detection*; human judgment handles the *prescription*.
- **Architecture testing (ArchUnit)**: encode principles as executable tests (no class may reach into X; no cycles) so structural health is a CI gate.
- **Language ecosystem**: Go's `gofmt`/`go vet`, Kotlin's tooling, and Java's IDE refactorings all normalize the small-step workflow; large migrations (e.g., module splits) are planned *as sequences of refactorings*.

## 17. References
- Martin Fowler, *Refactoring: Improving the Design of Existing Code* — the smell catalog + refactoring catalog (the canonical source).
- Kent Beck, *Refactoring* foreword / "smells" terminology; *Extreme Programming Explained* (campground rule).
- Michael Feathers, *Working Effectively with Legacy Code* — characterization tests, seams.
- Robert C. Martin, *Clean Code* — code smells chapter (naming, functions, comments).
- GeeksForGeeks, "Code Smells": https://www.geeksforgeeks.org/code-smells-introduction/

## 18. Cheat Sheet
- Smell = symptom of design rot; heuristic, not verdict.
- Refactoring = internal structure change, behavior preserved.
- Small steps + green tests after each = safety.
- Long Method → Extract Method.
- God Class → Extract Class.
- Long Parameter List → Introduce Parameter Object.
- Feature Envy → Move Method.
- Duplicated Code → Extract Function/Class.
- Shotgun Surgery → Consolidate/Move (SRP).
- Switch on type tag → Replace with Polymorphism.
- Never refactor without a test net (write characterization tests).
- Refactor where change pressure is (campground rule), not everywhere.
- Rewriting ≠ refactoring.

## 19. Quiz
1. A smell is: a) a bug b) a hint of a deeper problem c) a compiler warning d) a design pattern → **b**
2. Refactoring must preserve: a) line count b) external behavior c) method names d) comments → **b**
3. Feature Envy fix: a) Extract Method b) Move Method c) Rename d) Delete → **b**
4. God Class fix: a) Extract Class b) Extract Constant c) Inline d) duplicate → **a**
5. 7-parameter method fix: a) Introduce Parameter Object b) make static c) ignore d) split file → **a**
6. True or False: Rewriting is a form of refactoring. → **False**

## 20. Flashcards
- **Q: Code smell definition?** → **A:** A structure hinting at a deeper design problem — heuristic, not verdict.
- **Q: Refactoring definition?** → **A:** Behavior-preserving internal restructuring, in small test-verified steps.
- **Q: God class fix?** → **A:** Extract Class per responsibility (SRP).
- **Q: Feature envy fix?** → **A:** Move Method to the data owner.
- **Q: Safe refactoring precondition?** → **A:** Tests (or characterization tests first).
- **Q: Refactoring vs rewriting?** → **A:** Preserve vs rebuild; refactoring keeps you shippable.

## 21. Revision
Smells are recognizable shapes that hint at violated principles — Long Method (Extract Method), God Class (Extract Class), Long Parameter List (Introduce Parameter Object), Feature Envy (Move Method), Duplicated Code (Extract Function), Shotgun Surgery (Consolidate by SRP), Switch-on-type (Replace with Polymorphism). Refactoring is *behavior-preserving* restructuring in tiny steps, each verified by green tests (write characterization tests for untested legacy code first). The payoff is cheaper future change, not speed. Refactor where change pressure exists (campground rule), never as big-bang rewrites, and always toward a named principle (SOLID, DRY, coupling/cohesion) so the change is measurable. First-30-seconds answer: "Smells are symptoms of violated principles with catalogued fixes; refactoring removes them in small, behavior-preserving, test-verified steps."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a code smell?" | Interview Q1 / Section 2, 7 |
| "Refactoring vs rewriting?" | Interview Q3 / Section 4 |
| "Is a long cohesive method a smell?" | Interview Q4 / Section 7 |
| "Fix this God Class" | Interview Q5 / Section 8 |
| "Refactor untested legacy code?" | Interview Q6 / Section 9 |
| "Feature Envy + fix?" | Interview Q7 / Section 8 |
| "When is a switch OK?" | Interview Q8 |
| "Name 5 smells + refactorings" | Interview Q13 / Section 7 |
