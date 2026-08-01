# How to Choose the Right Pattern

> **TL;DR**: Choosing a pattern is a **decision procedure, not an intuition** — you state the tension, map it to a family, narrow by sub-question, compare candidate patterns on trade-offs, and validate against "is there a simpler non-pattern solution?" — and the mark of maturity is knowing when **not** to use a pattern at all.

## 1. Why Does This Exist?
Knowing 23 patterns is useless if you can't *select* one. Interviews and design reviews fail on exactly this skill: a candidate who knows every diagram can still propose an Adapter where a Decorator belongs, or force a Singleton into a design that needs DI. This section exists because **pattern choice is a decision**, and decisions need a *repeatable procedure* rather than vibes. When interviewers ask "why did you pick that pattern?" they're scoring your *selection method* — the tension analysis, the candidate comparison, the trade-off reasoning, and the YAGNI judgment — not the pattern name. A formalized selection procedure is what separates "I know patterns" from "I can engineer with patterns."

It also exists to prevent the two classic failure modes of pattern usage: **pattern-forcing** (reaching for a pattern because it's impressive, regardless of fit — the Golden Hammer) and **premature abstraction** (applying a pattern for a variation that doesn't exist yet — YAGNI violations). The procedure bakes the anti-over-engineering check in as a required step.

## 2. How Does It Work?
The **pattern-selection triage** (recap of Section 01/09's internal procedure, formalized):

1. **State the tension precisely** — one sentence: what varies, what breaks today, what must stay stable.
2. **Decide: is there a pattern problem at all?** — If no variation axis, no recurring structure, and no decoupling need, the answer is *no pattern* (write the simple code). This check runs first.
3. **Map to a family** by question:
   - "How is an object created?" → **Creational** (5).
   - "How are objects composed/matched?" → **Structural** (7).
   - "How do objects communicate/behave?" → **Behavioral** (11).
4. **Narrow within the family** by sub-question (e.g., creation: which-class→Factory Method, family→Abstract Factory, complex-build→Builder, copy→Prototype, one-instance→Singleton).
5. **Compare candidates on consequences** — for the 2-3 shortlisted patterns, compare: coupling reduction, class count, runtime flexibility, and the *predicted change axis*.
6. **Validate** — does the pattern's cost (indirection, classes) buy more than it costs? Would a simpler mechanism (interface + lambda, enum strategy, direct call) suffice? If yes, drop the pattern.
7. **Name + document** — record the choice *and the rejected alternatives* for the review.

```pseudocode
procedure choosePattern(tension):
    if not recurringVariation(tension): return "no pattern"
    family = ask(tension, [creation, composition, communication])
    candidates = narrow(family, subQuestion(tension))
    best = minimizeCost(candidates, predictedChange(tension))
    if simplerAlternativeExists(best): return "no pattern"
    return best
```

## 3. When Is It Used?
- **During LLD interview design**: every time you introduce a class, you run the triage ("should this be a Strategy or an enum? Should this be injected or a Singleton?").
- **During design reviews**: evaluating a colleague's design ("is the Decorator here justified, or is it pattern-forcing?").
- **During refactoring**: choosing the target shape for a refactor (Fowler's refactorings to patterns).
- **When extending a codebase**: selecting the pattern that fits the existing architecture's change axes.
- **When the team argues about "the right way"**: the procedure converts opinion into a checkable argument.
- **Interview prep**: rehearsing the triage on many scenarios builds the automatic, defensible decision style interviewers reward.

## 4. Why Wasn't Another Approach Chosen?
- **Choosing by pattern name familiarity ("I know Singleton best")**: rejected — the Golden Hammer; familiarity is not fit. The procedure forces problem-first selection.
- **Choosing by "most common in the codebase"**: a weak proxy — the codebase's existing style matters (consistency), but it can't override a mismatch with the actual problem.
- **Choosing by "most impressive/advanced"**: rejected — complexity is a cost, not a feature; the procedure minimizes cost.
- **Choosing by a fixed lookup table (problem → pattern)**: a *rough* guide (and this section provides one), but rejected as the whole method because real tensions overlap and require trade-off comparison; a table gives candidates, not the decision.
- **Choosing by "what the framework uses"**: a good *tie-breaker* (Spring precedent is strong evidence), but rejected as primary because framework patterns are shaped by framework constraints.
- **Choosing by intuition/experience**: the *outcome* of internalized procedure — but not teachable or reviewable; the procedure is the teachable form of good intuition.

## 5. Intuition
Pattern selection is **triage in an emergency room** — exactly like the Section 01 taxonomy. You don't treat a patient by asking "which treatment have I memorized best?" You (1) assess the symptom (the tension), (2) decide if it's even a medical problem (is a pattern needed at all?), (3) route to the right department (family), (4) pick the specific protocol (the sub-question narrow), (5) weigh risk (consequences), and (6) escalate only if a simpler treatment won't work (YAGNI). A great doctor and a great designer both follow the *procedure*; the memorized options are just the toolbox they route through.

The deeper intuition: **every pattern is a bet on where change will happen** (Section 01/05). The selection procedure is really *reading your requirements for their change axes*, then choosing the pattern that localizes exactly that axis — and declining to bet where no change is predicted.

## 6. Real-World Analogy
A **contractor choosing a tool for a job**. You don't grab a hammer because you own one. You (1) inspect the problem ("I need to join two pipes of different diameters" — a tension), (2) decide if a tool is even needed ("just push-fit them" — no pattern), (3) route to the right toolkit (plumbing, not carpentry — the family), (4) pick the specific fitting (adapter vs union vs reducer — the sub-question), (5) weigh cost/benefit (adapter = one part, keeps both pipes intact), and (6) check if duct tape suffices (simpler alternative → no pattern). The carpenter who *reaches for the nearest tool* and the designer who *reaches for the nearest pattern* fail the same way.

## 7. Formal Definition
Pattern selection is the decision problem of choosing, from the set of known patterns (and the empty pattern), the design that best satisfies the requirements' **predicted variation axes** subject to a **cost function** (indirection, class count, coupling, complexity) and the **YAGNI constraint** (no pattern applied without a present or strongly-forecast recurring problem). The triage procedure implements this by (a) family classification by purpose, (b) within-family narrowing by the specific intent question, (c) consequence comparison, and (d) the no-pattern escape check.

## 8. Example
**Tension**: "Our `ReportExporter` has three `if (format == ...)` branches, each 50 lines, and customers keep asking for new formats."
1. **Is it a pattern problem?** Yes — an *open, recurring* variation (new formats predicted; duplicated branch logic).
2. **Family?** The variation is in *behavior/algorithm* ("how to export") → Behavioral.
3. **Sub-question?** "Do we swap whole algorithms at run time?" → **Strategy** (candidate). "Do we have a fixed process with varying steps?" → **Template Method** (candidate). 
4. **Compare**: Strategy varies whole export algorithms via composition (runtime swap, reusable across exporters) — matches "each format is a self-contained algorithm" → **Strategy wins**. Template Method is rejected because there's no fixed skeleton the formats share (each format's process differs enough).
5. **Validate**: simpler alternative? An enum with a `export()` method is *closed* (new format edits the enum) — rejected because the set is *open*. Lambdas per format? Only if stateless — but formats carry config (page size, compression), so strategy classes are justified.
6. **Decision**: Strategy, with a factory selecting the strategy by format. **Result**: adding a format = one class + one factory registration; `ReportExporter` unchanged.

## 9. Internal Working
The procedure's internal steps in decision-table form:

| Step | Question | Output |
|---|---|---|
| 1. Tension | "What varies? What breaks if I add one more?" | A crisp one-liner |
| 2. Pattern needed? | "Is this variation recurring/open, or one-off?" | yes / **no** (→ simple code) |
| 3. Family | "Creation / composition / communication?" | creational | structural | behavioral |
| 4. Narrow | "Which sub-question matches?" (see table below) | 2-3 candidates |
| 5. Compare | "Coupling? Class count? Runtime flexibility? Change axis?" | best candidate |
| 6. Simpler? | "Would a lambda / enum / direct call / interface suffice?" | keep | drop (→ simpler) |
| 7. Validate+document | "Does cost ≤ benefit? Rejected alternatives?" | decision + rationale |

**Family → sub-question narrowing table (the core cheat):**

| Family | Sub-question | Pattern |
|---|---|---|
| Creational | "Which concrete class?" | Factory Method |
| | "A family of related products?" | Abstract Factory |
| | "Many optional parts / immutable build?" | Builder |
| | "Copy an expensive configured object?" | Prototype |
| | "Exactly one instance?" | Singleton |
| Structural | "Incompatible interface?" | Adapter |
| | "Add behavior without subclassing?" | Decorator |
| | "Hide a subsystem?" | Facade |
| | "Control access / defer creation?" | Proxy |
| | "Uniform tree (part-whole)?" | Composite |
| | "Two independent variation axes?" | Bridge |
| | "Share fine-grained state?" | Flyweight |
| Behavioral | "Swap algorithms at run time?" | Strategy |
| | "Notify many decoupled listeners?" | Observer |
| | "Request as object (undo/queue)?" | Command |
| | "Behavior depends on state / self-transitions?" | State |
| | "Fixed skeleton, varying steps?" | Template Method |
| | "Traverse without exposing structure?" | Iterator |
| | "Snapshot/restore state?" | Memento |

## 10. Time Complexity
- **Decision procedure**: O(1) — a fixed set of questions; the family and sub-question lookups are constant-time. (This is design-time, not run-time — no runtime cost at all.)
- **What the chosen pattern costs at runtime**: O(1) indirection per delegation for most patterns; O(N) for observer fan-out, composite traversal, iterator walks; O(S) for memento snapshots — all covered in each pattern's Section 10.
- **Structural cost**: O(1) extra classes for the pattern (a strategy per algorithm = O(N) for N algorithms) — the price of flexibility.
- **The real "asymptotic" win**: bounded decision time + minimized future modification cost (O(1) change sites when the predicted axis moves vs O(N) sites without the pattern).

## 11. Advantages
- **Defensible decisions**: every choice is backed by a stated tension, family, and trade-off — reviewable and teachable.
- **Consistency**: the same tension yields the same pattern across the team (no designer-dependent results).
- **Open-Closed by construction**: the procedure selects patterns that localize the predicted change axis.
- **Anti-over-engineering built in**: the "is a pattern needed?" and "simpler alternative?" steps kill premature abstraction and Golden-Hammer forcing.
- **Interview leverage**: "why did you pick that pattern?" is answered with the procedure, not the name — the exact scoring signal.
- **Transfers across languages and frameworks**: the procedure is language-independent.

## 12. Disadvantages
- **Not a substitute for domain understanding**: the procedure can't fix a wrong reading of the requirements (garbage-in-garbage-out on the "tension").
- **Over-ritualizing**: forcing the full procedure on trivial decisions wastes time (you internalize it and skip steps for obvious cases).
- **Trade-off comparison is still judgment**: step 5 (minimize cost) requires experience — the procedure frames the trade-off, it doesn't compute it.
- **Change-forecast dependence**: two forecasters can read the same requirements and pick different patterns (one predicts "new formats", another predicts "formats stay fixed") — the procedure makes the *reason* explicit, which is the point.
- **Not a substitute for the no-pattern check's discipline**: teams that skip step 2/6 revert to pattern-forcing.

## 13. Interview Questions
1. **Q: How do you decide which pattern to use?** A: Run the triage: state the tension, check if it's a recurring/open variation (else no pattern), map to a family by question (creation/composition/communication), narrow by sub-question, compare candidates on consequences, and validate there's no simpler alternative.
2. **Q: When is "no pattern" the right answer? (Production)** A: When there's no variation axis, no recurring structure, and no decoupling need — a direct call, a simple class, or a lambda is clearer. Patterns are justified by *recurring problems* (YAGNI); a one-off conditional doesn't earn a Strategy.
3. **Q: What is the Golden Hammer anti-pattern?** A: Over-reliance on one familiar pattern/tool for every problem (e.g., "make it a Singleton" for everything). The fix is problem-first selection — the procedure, not familiarity.
4. **Q: Your colleague proposes a Singleton for app-wide configuration. How do you evaluate? (Scenario)** A: Triage: is single-ness *semantically required* (true one-of-a-kind resource)? Is DI a simpler alternative (a single injected config bean — the container enforces it, better testability)? In a Spring app, DI wins; in a non-framework app, a holder-based singleton may be pragmatic. The decision is by *fit*, not by pattern familiarity.
5. **Q: Two patterns could both solve the same tension — how do you choose? (e.g., Strategy vs Template Method)** A: Compare the change axis: if *whole algorithms* are interchangeable and runtime swap matters → Strategy (composition); if a *fixed skeleton* with varying steps and shared state → Template Method (inheritance). State the discriminator and the trade-off; either can be valid — the *reason* is what's scored.
6. **Q: How does "encapsulate what varies" guide pattern choice?** A: Identify the axis of change (the variation), then pick the pattern that isolates exactly that axis: creation → creational; composition/interface → structural; behavior/communication → behavioral. Patterns are *mechanisms for the change axis*.
7. **Q: How do you know a pattern is being over-applied? (Production)** A: If removing the pattern's indirection would not change any behavior (a "false pattern"), if the variation it predicts never materializes, if the class count makes the design harder to read, or if a simpler mechanism (lambda/enum/interface) works. Reviews flag these.
8. **Q: Your requirements say "we will add new payment methods quarterly." Which pattern family and why?** A: Behavioral — Strategy (each method is a self-contained algorithm) or a factory providing the strategy; the variation is *which algorithm runs*, so the family is behavioral (with creational assist for selection).
9. **Q: What's the first question you ask before choosing any pattern?** A: "Is there a recurring problem here, or is this a one-off?" — because the no-pattern escape is the most common correct answer, and skipping it is how pattern-forcing starts.
10. **Q: How does the "predicted change" forecast drive the choice?** A: Every pattern bets on a change axis (Section 01/05): creational bets products will grow; structural bets composition/interfaces will shift; behavioral bets algorithms/state/communication will vary. Read the requirements' change forecast, then bet the matching pattern.
11. **Q: When should you choose composition-based patterns over inheritance-based ones?** A: Prefer composition (Strategy, Decorator, Adapter-object, State) when you need runtime flexibility, swap-ability, or avoiding fragile base classes; prefer inheritance-based (Template Method, class Adapter) only when the structure is genuinely fixed and compile-time binding is fine. "Favor composition over inheritance" is the default.
12. **Q: How do you evaluate a pattern's cost vs benefit? (Production)** A: Benefit = reduced modification cost at the predicted change sites + coupling reduction + testability. Cost = indirection (O(1) per call), class count, and reading complexity. Choose the pattern only when benefit > cost *today* or at a *strongly forecast* change; otherwise simpler wins.
13. **Q: A design needs to notify multiple components of state changes. Walk the triage.** A: Tension: "many listeners must react to state changes, list grows." Pattern needed: yes (open, decoupling). Family: communication → Behavioral. Sub-question: "notify many decoupled listeners?" → Observer. Candidates: Observer vs a direct multi-call (rejected — couples subject to listeners, no runtime dynamics) vs an event bus (overkill in-process). Choose Observer; validate no simpler alternative.
14. **Q: Is it OK to combine multiple patterns? (Tricky)** A: Yes — patterns compose (Factory + Singleton, Composite + Iterator, Command + Memento, Strategy + Factory). The triage can legitimately produce a *composition* when multiple change axes exist; name each pattern and its role.
15. **Q: Your team's style is "one interface per variation, always." Is that pattern-forcing?** A: Interfaces-per-variation is the *mechanism* behind most patterns, but adding an interface with one implementation and no predicted second is premature abstraction (YAGNI). The judgment is: interface when a variation is *predicted or present*; don't decorate one-off code with seams that never open.
16. **Q: How do you choose between Strategy and State for an object whose behavior varies?** A: Ask: who changes the behavior — the *client* (external selection, stays fixed → Strategy) or the *object itself* on events (self-transition → State)? An order workflow self-transitions on events → State; a payment method is chosen by the client → Strategy.
17. **Q: When would you NOT use the Observer pattern despite "many listeners"? (Production)** A: When the listener set is fixed and tiny (a direct multi-call is clearer), when listeners must process in a strict order with dependencies (consider a pipeline/mediator), or when cross-process delivery is required (use a message broker — Observer is in-process). Also skip it if the subject and observers can simply share state.
18. **Q: Your design has two independent axes that multiply (shape × renderer). Walk the triage.** A: Tension: N×M class explosion. Pattern needed: yes (recurring combinatorial problem). Family: composition → Structural. Sub-question: "two independent variation axes?" → Bridge. Candidates: Bridge vs inheritance matrix (rejected — explosion) vs Strategy (rejected — not algorithm swapping). Choose Bridge; validate.
19. **Q: What's your first move when a review challenges "why this pattern?"** A: Re-run the triage out loud: the tension, the family, the sub-question that selected the pattern, the rejected candidates and their flaws, and the cost/benefit check. A pattern choice defended by *procedure* survives reviews; a choice defended by name doesn't.
20. **Q: How does the selection procedure help in interviews specifically? (Scenario)** A: It gives you a repeatable "thinking out loud" structure interviewers can score: tension → family → candidates → trade-off → no-pattern check. Instead of "I'd use an Observer," you demonstrate *why* Observer and *why not* the alternatives — which is exactly what LLD rubrics reward.

## 14. Follow-Up Questions
1. **Q: What is "pattern composition" and when do you plan for it?** A: When multiple change axes coexist, multiple patterns compose (e.g., a Factory returning a Strategy; a Command storing a Memento; a Composite traversed by an Iterator). Plan for it when the triage identifies more than one variation axis; name each pattern's responsibility.
2. **Q: How do language features change pattern selection? (Part 08 preview)** A: Lambdas make Strategy/Command/Observer lighter (functional interfaces); named/default args (Kotlin) replace Builder; module-level state (Python) nearly removes Singleton; records replace simple value builders. Re-run the "simpler alternative" check *in your language* — a pattern that's boilerplate in Java may be a language feature elsewhere.
3. **Q: What's the difference between "premature abstraction" and "earned abstraction"?** A: Premature = a seam/interface/pattern added for a variation that never appears (YAGNI violation — cost without benefit). Earned = applied when the second implementation actually arrives or the change is strongly forecast (cost now buys guaranteed future savings). Interviewers reward "I'll introduce the Strategy when the second algorithm shows up" answers.
4. **Q: How do you keep the no-pattern check honest in a large team?** A: Codify it: code-review checklists ("does this interface have ≥2 implementations or a forecast?"), explicit "simplest working thing first" conventions, and naming the *tension* in every design doc — so pattern decisions are reviewed against the problem, not the pattern.
5. **Q: How does the triage differ for architectural patterns (MVC, layered, event-driven) vs GoF patterns?** A: GoF triage is *class-level* (creation/composition/communication of objects). Architectural triage is *system-level* (separation of concerns, deployment topology, data flow) and yields MVC/layers/ports-and-adapters. The procedure generalizes: state the system tension, pick the architectural pattern, then use the GoF triage for class-level details inside each layer.

## 15. Coding Example
```java
// The triage in action: a rate-limiter that must support multiple algorithms.
// Tension: "which rate-limiting algorithm runs?" → Behavioral family → Strategy.
interface RateLimiter {
    boolean allow(String key);
}
class FixedWindowLimiter implements RateLimiter {   // algorithm 1
    private final int limit;
    FixedWindowLimiter(int l) { limit = l; }
    public boolean allow(String key) {
        // window count logic...
        return true;
    }
}
class TokenBucketLimiter implements RateLimiter {   // algorithm 2
    private final int capacity;
    TokenBucketLimiter(int c) { capacity = c; }
    public boolean allow(String key) {
        // token bucket logic...
        return true;
    }
}
// Selection via factory (the pattern's selection glue) — strategy selection moves here:
class RateLimiterFactory {
    static RateLimiter create(String algo) {
        return switch (algo) {
            case "fixed" -> new FixedWindowLimiter(100);
            case "token" -> new TokenBucketLimiter(100);
            default -> throw new IllegalArgumentException(algo);
        };
    }
}
class ApiGateway {                                  // Context
    private RateLimiter limiter;
    void configure(String algo) { limiter = RateLimiterFactory.create(algo); }  // runtime swap
    boolean hit(String key) { return limiter.allow(key); }
}
// Decision trail: variation = algorithm (behavior) → Strategy;
// rejected: enum-limiter (closed set — but algorithms may be added by other modules);
// rejected: hard-coded if/else in gateway (Open-Closed violation, not testable).
```
```python
# The no-pattern check in Python: lambdas often remove the need for Strategy classes
def fixed_window(limit: int):
    def allow(key: str) -> bool:
        print(f"fixed window check for {key}")
        return True
    return allow

def token_bucket(capacity: int):
    def allow(key: str) -> bool:
        print(f"token bucket check for {key}")
        return True
    return allow

limiter = fixed_window(100)          # a Strategy as a closure — pattern present, boilerplate absent
limiter("user-1")
```
```cpp
// Composite selection: two axes (file-type × compression) → think Bridge/Strategy per axis
#include <functional>
#include <iostream>
// Compression algorithm (Strategy) chosen by the type, not hard-coded
std::function<std::string(const std::string&)> compress = [](const std::string& d) {
    return "gzip(" + d + ")";
};
// int main(){ std::cout << compress("data") << "\n"; }
```

## 16. Industry Usage
- **Every design review at FAANG/MAANG** runs this procedure implicitly: reviewers ask "what varies?", "which family?", "why not the alternative?", "do you even need a pattern?" — the triage is the shared review vocabulary.
- **LLD interview rubrics** score: (1) identifying the change axis, (2) choosing the right family/pattern, (3) comparing rejected alternatives, (4) YAGNI/no-pattern judgment, (5) mapping to a framework precedent. This section is the rubric, operationalized.
- **Architecture teams** codify selection as ADRs (architecture decision records) — "Context → Decision → Consequences" is exactly the triage's steps 1, 4-5, 7 written down.
- **Refactoring teams** use Fowler's "refactor to patterns" targets — the triage picks the target shape.
- **Framework maintainers** (Spring, Guava) demonstrate the triage in their own design: patterns appear only where a *real, recurring* problem existed — the anti-pattern is a framework that uses every pattern (complexity smell).
- **Interviews**: "design a notification system / vending machine / rate limiter / payment system" are the stock LLD scenarios where the triage is rehearsed; "why did you choose X?" is the follow-up that scores it.

## 17. References
- **Gamma et al., *Design Patterns*** — the "How to select a design pattern" section (GoF Ch. 1) — the original selection guidance this chapter operationalizes.
- **Martin Fowler, *Refactoring* (2nd ed.)** — "Refactorings to patterns" and the "replace conditional with polymorphism" route.
- **Martin Fowler, "Is Design Dead?" and ADR practice** — when patterns earn their keep; architecture decision records as the written triage.
- **Robert C. Martin, *Clean Architecture*** — the cost-of-abstraction framing and YAGNI-in-architecture.
- **refactoring.guru — "How to Select a Design Pattern"** — the modern decision aid.
- **Baeldung — "Design Patterns" series** — pattern-by-pattern applicability and comparisons.
- **Head First Design Patterns — appendix on pattern selection** — the "Patterns together" and selection guidance.

## 18. Cheat Sheet
- Selection = **triage, not intuition**: tension → family → sub-question → compare → validate → (maybe) no pattern.
- **Step 0**: "Is there a recurring/open problem?" If not → **no pattern** (YAGNI).
- Family by question: creation → creational; composition/interface → structural; communication/behavior → behavioral.
- Narrow by sub-question (see the 18-row narrowing table in Section 09).
- **Every pattern is a bet on a change axis** — bet the pattern matching your forecast.
- Compare candidates on: coupling, class count, runtime flexibility, change axis fit.
- Prefer composition (Strategy/Decorator/State) over inheritance (Template Method) unless the skeleton is genuinely fixed.
- **Golden Hammer** = one favorite pattern for everything — the anti-pattern.
- **Premature abstraction** = interface/pattern with no forecast second implementation.
- "Why did you choose X?" → answer with the procedure (tension + rejected alternatives + cost/benefit), never with the name alone.

## 19. Quiz
1. The FIRST question in pattern selection is: a) which family? b) is there a recurring problem at all? c) which pattern is most common? d) which looks best → **b**
2. "How is an object created?" maps to which family? a) Structural b) Behavioral c) Creational d) none → **c**
3. The Golden Hammer anti-pattern is: a) using no patterns b) over-using one favorite pattern c) combining patterns d) lambdas → **b**
4. Premature abstraction means: a) too many patterns b) a seam added for a variation that never arrives c) no interface d) too few classes → **b**
5. Strategy vs Template Method choice is driven by: a) language b) whole-algorithm swap (composition) vs fixed skeleton+steps (inheritance) c) number of classes d) name length → **b**
6. Strategy vs State choice: who changes the behavior? a) client (strategy) vs object itself (state) b) object (strategy) vs client (state) c) both client d) neither → **a**
7. Which is the correct first step of the triage? a) pick the pattern b) state the tension c) count classes d) draw UML → **b**
8. An order workflow whose states self-transition on events → which pattern? a) Strategy b) State c) Observer d) Builder → **b**
9. "Why did you choose X pattern?" is best answered by: a) the pattern name b) the procedure (tension, alternatives, trade-offs) c) "it's standard" d) a diagram → **b**
10. When is "no pattern" correct? a) always b) when there's no recurring variation / a simpler mechanism suffices c) never d) when the team dislikes patterns → **b**

## 20. Flashcards
- **Q: The selection triage steps?** → **A:** Tension → pattern-needed check → family → sub-question narrow → compare candidates → no-pattern validation.
- **Q: The no-pattern check?** → **A:** Is there a recurring/open problem and no simpler mechanism? If not → write simple code (YAGNI).
- **Q: Family by question?** → **A:** creation→creational; composition→structural; communication/behavior→behavioral.
- **Q: Golden Hammer?** → **A:** Over-using one favorite pattern for every problem — the anti-pattern.
- **Q: Premature abstraction?** → **A:** A seam/pattern for a variation that never arrives.
- **Q: Strategy vs State?** → **A:** Client-chosen + fixed (Strategy) vs object self-transitions (State).
- **Q: Strategy vs Template Method?** → **A:** Whole-algorithm via composition vs skeleton+steps via inheritance.
- **Q: How to defend a pattern choice?** → **A:** Procedure, not name: tension + family + rejected alternatives + cost/benefit.

## 21. Revision
Pattern choice is a **decision procedure, not intuition**: (1) state the tension precisely; (2) check if there's a recurring/open problem at all — if not, **no pattern** (YAGNI); (3) map to a family by question (creation→creational, composition→structural, communication/behavior→behavioral); (4) narrow by the sub-question (which-class→Factory, family→Abstract Factory, complex-build→Builder, one-instance→Singleton; interface-mismatch→Adapter, add-behavior→Decorator, hide→Facade, control-access→Proxy, tree→Composite, two-axes→Bridge; swap-algorithm→Strategy, notify-many→Observer, request-object→Command, self-transition→State, fixed-skeleton→Template Method, traverse→Iterator, snapshot→Memento); (5) compare candidates on coupling, class count, runtime flexibility, and change-axis fit; (6) validate no simpler mechanism (lambda, enum, direct call) suffices. Every pattern **bets on a change axis** — bet the matching pattern, decline to bet where no change is forecast. Anti-patterns to avoid: **Golden Hammer** (one favorite pattern for everything) and **premature abstraction**. In interviews, "why did you choose X?" is answered with the *procedure* (tension + rejected alternatives + trade-offs), never the name.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you decide which pattern to use?" | 2 How / 13 Q1 / 9 Internal Working |
| "When is 'no pattern' correct?" | 13 Q2 / 4 Alternatives / 14 Q3 |
| "What is the Golden Hammer?" | 13 Q3 / 18 Cheat Sheet |
| "Why did you pick X over Y?" | 13 Q5 / 13 Q19 / 8 Example |
| "Strategy vs State / Template — how to choose?" | 13 Q16 / 13 Q5 |
| "Is this Singleton justified?" | 13 Q4 / 14 Q2 |
| "How does the change forecast guide choice?" | 13 Q10 / 5 Intuition |
| "Cost vs benefit of a pattern?" | 13 Q12 / 14 Q3 |
| "Can multiple patterns combine?" | 13 Q14 / 14 Q1 |
| "Design a rate limiter / notification system (scenario)." | 15 Coding / 13 Q8 |
