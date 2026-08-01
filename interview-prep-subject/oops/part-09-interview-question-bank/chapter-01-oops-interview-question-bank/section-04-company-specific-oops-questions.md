# Company-Specific OOPs Interview Questions

> **TL;DR**: Which companies ask what in the OOPs round — heatmaps for Amazon, Google, Microsoft, Uber, Flipkart, Walmart, and the Java/C++/Python-heavy shops — plus how to tailor your prep to each hiring bar.

## 1. Why Does This Exist?
Interview questions are not evenly distributed. Amazon's LLD screens, Google's OOD rounds, and C++ shops' v-table questions overlap maybe 30% with each other. Knowing *your target company's pattern* means spending prep time where it's scored: a candidate drilling C++ move semantics for an Amazon Java-backend role is wasting the hour. This guide exists to (1) map each major employer to its recurring OOPs question types, (2) flag the depth bar (fresher vs senior), and (3) tell you which parts of this resource to prioritize per company.

## 2. How Does It Work?
Each company entry gives: the **round structure** (where OOPs appears), the **high-frequency topics** with a heatmap (★★★ = almost guaranteed, ★★ = likely, ★ = possible), the **depth bar**, and the **parts to prioritize** from this resource. Use it to build a company-specific drill list (see Section 01's top-100 filtered by the heatmap).

## 3. When Is It Used?
- **Targeting a company**: build your study plan from its row before the interview window.
- **Multiple targets**: rank companies, then weight prep by overlap (the core set — pillars, SOLID, patterns, LLD — is shared by everyone).
- **Change of role level**: senior roles shift from "what is X?" to "design with X" — check the depth column.

## 4. Why Wasn't Another Approach Chosen?
A generic "prepare everything" strategy is impossible to execute at depth — interviews test depth, not breadth. Company-specific prep (like this heatmap) beats generic prep because the marginal question has *different value* per company; the same hour spent on a company's "always asked" topic beats a random topic. The risk — over-fitting one company — is mitigated because every company's core (pillars, SOLID, patterns, basic LLD) overlaps, so the map is mostly *prioritization*, not substitution.

## 5. Intuition
Think of each company as a **coach with a signature playbook**. Amazon runs the "leadership-principles-in-code" play (customer obsession = clear requirements, ownership = small focused classes). Google runs the "algorithm-rigor" play (OOD problems must run fast and be provably correct). C++ trading firms run the "zero-cost-abstraction" play (v-tables, move semantics, RAII). You don't need to master every play — you need to master *their* playbook. This section is the scouting report.

## 6. Real-World Analogy
A **sports scout's binder**: for each opponent (company), one page listing their favorite plays (topics), how often they call them (heatmap), and what beat them last season (what candidates miss). You study the binder *before* game day — not during — so you can practice exactly the plays you'll face. When the scout says "they always pressure the left flank," you don't spend the week practicing the right side.

## 7. Formal Definition
Company-specific interview prep is the practice of aligning study effort with an employer's demonstrated question distribution and depth expectations, derived from interview transcripts (Glassdoor, AmbitionBox, LeetCode discuss, internal recruiter guidance) and public hiring-bars documentation, to maximize expected interview performance per unit of study time.

## 8. Example
**Amazon, SDE-I (2025-26):** a typical loop has an OOPs/LLD screen. Heatmap: class design / Parking Lot (★★★), SOLID + "why" (★★★), design patterns in Spring/JDK (★★★), pillars with examples (★★), Java memory/GC (★★), concurrency-in-design (★★), C++/Python internals (★). Depth bar: explain-then-apply; follow-ups push "how would you extend this?" Priority: Parts 01, 06, 07, 09-S3, 08-S1. So a week before the screen: drill LLD (Parking Lot, Vending Machine), SOLID rationale, and Spring pattern spotting — not C++ move semantics.

## 9. Internal Working
1. Collect the signal: interview transcripts and LeetCode "company" filters show which topic strings recur per company.
2. Bucket topics into the part-level buckets of this resource (pillars / relationships / SOLID / patterns / language internals / LLD / coding).
3. Assign heat: ★★★ for topics appearing in ≥ ~60% of transcripts, ★★ for ~30-60%, ★ for <30%.
4. Check the level column (fresher vs mid vs senior) — depth changes the *form* (recall vs design).
5. Convert to a drill list: pick the ★★★ topics, find the matching top-100 questions (Section 01) and LLD problems (Sections 02-03), drill daily.

## 10. Time Complexity
- Building a heatmap: O(transcripts) — a weekend task using public sources.
- Prep impact: prioritizing the top ~3 topics per company typically covers ~70% of observed questions; going deeper on the tail has diminishing returns.

## 11. Advantages
- Targets the highest-probability questions → best expected value per study hour.
- Reveals the *depth bar* (recall vs design) so you calibrate answer length.
- Flags company-specific twists (Amazon's LLD, C++ shops' internals) you'd otherwise under-prepare.
- Builds a repeatable drill plan (heatmap → Section 01/02/03 → mocks).

## 12. Disadvantages
- Transcripts are noisy and drift over time — treat heatmaps as priors, not guarantees.
- Over-fitting a single company's style can leave you flat-footed on novel variants.
- Public data lags hiring-bar changes (e.g., new LLD emphasis at a company).
- Some roles (backend vs infra vs mobile) split the same company's OOPs emphasis — match the *role*, not just the company.

## 13. Interview Questions (per-company heatmaps)

### Amazon (SDE-I/II, LLD-heavy)
1. **Design a Parking Lot / Vending Machine / Elevator / LRU Cache** (★★★) — Amazon's documented LLD screen; expect "make it extensible" follow-ups (add EV charging, add payment types).
2. **SOLID with a "why"** (★★★) — they probe *rationale*: "give me an example of a design that violates SRP and fix it."
3. **Design patterns in Spring/JDK** (★★★) — "which patterns does Spring use?" (Singleton, Proxy, Template Method, Factory).
4. **Four pillars with real examples** (★★) — always paired with a follow-up example request.
5. **Java memory model / GC** (★★) — "where do objects live?", "how does GC decide what to collect?" (Part 08-S1).
6. **Class design from a scenario** (★★) — "model an order checkout" mid-loop.
7. **Concurrency in design** (★★) — "make your LLD thread-safe" (Part 09-S2/S3 follow-ups).
8. **C++/Python internals** (★) — only if the role is C++/Python.
Bar: explain → apply → extend. Priority parts: 01, 06, 07, 09-S1/S2/S3, 08-S1.

### Google (L4/L5, OOD rounds)
1. **OOD of games/boards** (★★★) — Snake & Ladder, Chess, Poker, Tic-Tac-Toe; algorithmically-inclined (win checks, minimax).
2. **Design patterns asked as "which would you use?"** (★★★) — frequent pattern-identification + justification.
3. **Object modeling with edge cases** (★★★) — interviewers stress invalid inputs, nulls, boundary states.
4. **Composition vs inheritance** (★★★) — classic debate question with examples.
5. **Diamond problem / multiple inheritance** (★★) — language-agnostic plus Java/Python specifics.
6. **Deep Java internals** (★★) — immutability §17.5, erasure, GC (Part 08) at L4+.
7. **Time/space analysis of your design** (★★) — they require explicit complexity of the model.
8. **C++ (for C++ roles)** (★★★) — v-tables, move semantics, RAII (Part 08-S2/S3 chapter).
Bar: rigorous, fast, provably correct; depth grows with level. Priority parts: 01-08 evenly, 09-S1/S2, 08 for internals.

### Microsoft (SWE / DS)
1. **Design questions with async/concurrency twist** (★★★) — task scheduling, producer-consumer modeled in OOP.
2. **Pillars + definitions with code** (★★★) — they want the *code* version, not just prose.
3. **Abstract vs interface + real framework examples** (★★) — often framed around .NET/C# interfaces.
4. **SOLID applied to a small refactor** (★★) — "here's a messy class, refactor it" prompts.
5. **C#/Java language internals** (★★) — for the relevant role: GC, value vs reference types (C#).
6. **Design patterns catalog spot-check** (★★) — singleton/factory/observer variations.
7. **Liskov with a violation example** (★★) — Rectangle/Square is a favorite.
8. **Low-level system modeling** (★) — file system, cache, job queue.
Bar: solid fundamentals + clean code; C# shops replace Java depth with C# specifics. Priority: 01-07, 09-S1/S2, 08 (Java) or C# equivalents.

### Uber (Backend)
1. **LLD for ride-hailing-ish systems** (★★★) — trip model, driver allocation (Strategy), pricing (Strategy/Template).
2. **SOLID + scalability framing** (★★★) — "how would your design survive N drivers?"
3. **Concurrency-heavy OOP** (★★★) — shared state, atomicity, thread-safety in designs.
4. **Design patterns in the service layer** (★★) — Observer/Event for trip status, Command for actions.
5. **Java/Go internals** (★★) — Go shops probe interface semantics, composition; Java shops probe GC/immutability.
6. **Caching designs (LRU, TTL)** (★★) — modeled as OOP (Part 09-S2).
7. **Event-driven modeling** (★★) — producer/consumer, pub/sub class design.
Bar: production-grade reasoning about concurrency and scale-adjacent designs. Priority: 01, 06, 07, 09-S1/S2/S3, 08-S1.

### Flipkart / Walmart (LLD-centric product)
1. **Full LLD rounds** (★★★) — BookMyShow, Grocery Delivery, Elevator, Splitwise — with explicit "name the patterns" follow-ups.
2. **Patterns catalog identification** (★★★) — Strategy/Observer/Factory/State named and justified in your design.
3. **SOLID with refactor prompts** (★★★) — "fix this god class" style.
4. **Java collections/equals-hashCode** (★★) — Part 08-S4: why equal objects must hash equally, mutable keys.
5. **Class design for e-commerce flows** (★★) — cart, order, payment, inventory modeling.
6. **Edge-case enumeration** (★★) — out-of-stock, concurrent checkout, duplicate payments.
7. **Interviewer "why did you choose composition?"** (★★★) — justification questions dominate.
Bar: clean, defensible, pattern-rich LLD under 45 min. Priority: 01, 05, 06, 07, 09-S2/S3, 08-S4.

### JVM/C++ heavy shops (Bloomberg, Jane Street, DRW, NVIDIA, Apple, infra teams)
1. **C++ internals** (★★★, C++ roles) — v-table, RTTI/dynamic_cast, Rule of Five, move semantics, RAII, unique/shared/weak_ptr (Part 08-C2).
2. **Java internals** (★★★, JVM roles) — memory model, GC, immutability, exceptions, erasure (Part 08-C1).
3. **Performance-aware design** (★★★) — cost of your design, cache-friendliness, allocation-free hot paths.
4. **Concurrency correctness** (★★★) — atomics, locks, memory visibility in object designs.
5. **Python internals (Python shops: Dropbox/Stripe/ML)** (★★★) — MRO, dunders, super(), dataclasses (Part 08-C3).
6. **Design patterns with a "why this pattern" bar** (★★★) — justification expected at senior level.
7. **Lifetime/ownership questions** (★★★, C++) — who owns this pointer? copies vs moves.
8. **LLD with performance constraints** (★★) — "design a cache, ring buffer, memory pool" variants.
Bar: deep, precise, performance-literate. Priority: Part 08 entirely, 07, 06, 09-S1/S2.

## 14. Follow-Up Questions
1. **"Why is this better than the alternative you rejected?"** → Every company asks this; always name one rejected alternative and its trade-off.
2. **"What breaks at 10x scale?"** → Show you know the boundary: in-memory state, single locks, O(n) scans; propose indexed/partitioned/hierarchical upgrades without going full HLD.
3. **"Justify your pattern choice."** → State the *change point* it protects (e.g., "Strategy so adding a payment type doesn't touch checkout").
4. **"How does this behave under concurrency?"** → Walk a race (two exits), then the fix (atomic occupy, idempotent release).
5. **"What would the senior version of this design add?"** → Eventual-consistency, metrics, idempotency keys, fault tolerance — but only if asked.

## 15. Coding Example
```java
// The company-specific "twist" demo: Amazon asks to extend an LLD.
// Start with the core, then extend WITHOUT touching core classes (OCP):
interface SpotFinder { Optional<ParkingSpot> find(Floor f, Vehicle v); }

// Extension #1: EV charging (Amazon follow-up)
class EVSpot extends ParkingSpot {
    EVSpot(int id) { super(id, SpotType.LARGE); }
    void startCharging() { /* delegate to a ChargeController */ }
}
// Extension #2: Valet service (Amazon follow-up)
class ValetService implements SpotFinder {          // NEW strategy, no core change
    public Optional<ParkingSpot> find(Floor f, Vehicle v) {
        return f.spots().stream().filter(s -> s.isFree()).findFirst();
    }
}
// The core ParkingLot never changed — OCP demonstrated.
```
```python
# Google's "which pattern + why" demo: Strategy over if/elif
class SortingStrategy:
    def sort(self, data): raise NotImplementedError
class MergeSort(SortingStrategy): def sort(self, data): return sorted(data)
class RadixSort(SortingStrategy): def sort(self, data): return data  # placeholder
class Sorter:
    def __init__(self, strategy: SortingStrategy): self._strategy = strategy
    def run(self, data): return self._strategy.sort(data)
# New strategy -> new class, no edits (OCP/DIP); Google likes this framing.
```

## 16. Industry Usage
- **Recruiter prep docs**: Amazon's official LLD guidance and LeetCode's company-tagged problem sets corroborate these heatmaps.
- **Glassdoor/AmbitionBox transcripts**: the recurring "Design a Parking Lot" (Amazon), "Snake & Ladder" (Google), "Splitwise/BookMyShow" (Flipkart/Walmart) patterns appear across hundreds of reports.
- **Internal hiring bars**: Google's L4 OOD rubric, Amazon's SDE-I LLD screen, and C++ firms' internals-heavy loops are publicly documented enough to triangulate the depth bar.
- **Coding platforms** tag the exact prompts (LeetCode "Design Parking System", "Design LRU Cache", etc.), which align with the heatmaps above.

## 17. References
- LeetCode problem tags (company filters: Amazon, Google, Microsoft, Uber) — design-problem frequencies.
- Glassdoor interview reviews + AmbitionBox transcripts.
- Alex Xu, *System Design Interview* (LLD chapters reflect Amazon/Google bar).
- Grokking the Low-Level Design Interview (Educative) — problem set mirroring Flipkart/Walmart loops.
- Cracking the Coding Interview — OOD/design chapters per-company notes.
- Company career-pages' interview-process descriptions (Amazon SDE screen, Google OOD guidance).

## 18. Cheat Sheet
- Amazon: LLD (Parking Lot) + SOLID "why" + Spring patterns; extend-without-touching-core.
- Google: game OOD + patterns + edge cases + complexity; rigorous.
- Microsoft: code-first definitions, refactor prompts, .NET/C# flavors.
- Uber: ride-model LLD + concurrency + event-driven; scale-aware.
- Flipkart/Walmart: full LLD + "name the patterns" + e-commerce flows.
- C++/JVM/Python shops: deep internals (v-tables/move, GC/erasure, MRO/dunders) + performance + ownership.
- Universal: name a rejected alternative; justify each pattern; walk a concurrency race.
- Calibrate depth by level: fresher = recall+example; senior = design+extend.

## 19. Quiz
1. Amazon's signature OOPs round is: a) C++ templates b) LLD (Parking Lot) + SOLID c) Python dunders d) Minimax → **b**
2. Google OOD rounds emphasize: a) Verbose diagrams b) Rigor + edge cases + complexity c) Only diagrams d) No code → **b**
3. C++ trading shops most often ask: a) Spring patterns b) v-tables, move semantics, RAII c) Django models d) No internals → **b**
4. Flipkart/Walmart follow-ups tend to demand: a) Naming the patterns used b) Rewriting in Go c) UML only d) No justification → **a**
5. The depth bar for senior roles shifts from "recall" to: a) "Design and extend" b) "Memorize more" c) "No code" d) "Only definitions" → **a**
6. To prepare for Amazon, prioritize: a) Python MRO b) LLD + SOLID + Spring patterns c) C++ move semantics d) Regex → **b**
7. A universal follow-up is: a) "Why this over the alternative?" b) "What's your salary?" c) "Name the compiler" d) "Which IDE?" → **a**
8. Google's favorite game-modeling prompt is: a) Parking lot b) Snake & Ladder / Chess c) Vending machine d) Library → **b**
9. Uber's designs lean toward: a) Static state b) Concurrency + event-driven c) No concurrency d) Pure algorithms → **b**
10. Over-fitting one company's prep is risky because: a) It's boring b) Transcripts drift and vary by role c) Companies dislike it d) It's slower → **b**

## 20. Flashcards
- **Q: Amazon OOPs emphasis?** → **A:** LLD (Parking Lot) + SOLID rationale + Spring patterns.
- **Q: Google emphasis?** → **A:** Game OOD, rigor, edge cases, complexity.
- **Q: C++ shops?** → **A:** v-tables, RTTI, Rule of Five, move semantics, RAII.
- **Q: Flipkart/Walmart?** → **A:** Full LLD + name-the-patterns + e-commerce flows.
- **Q: Universal follow-up?** → **A:** "Why this over the alternative?" + "what breaks at 10x?"
- **Q: Depth bar vs level?** → **A:** Fresher = recall+example; senior = design+extend.
- **Q: Where to drill?** → **A:** Section 01 top-100 filtered by heatmap + Sections 02-03.
- **Q: Uber twist?** → **A:** Concurrency and event-driven modeling.

## 21. Revision
Company heatmaps: Amazon = LLD + SOLID + Spring patterns (extend-without-touching-core); Google = game OOD with rigor/edge-cases/complexity; Microsoft = code-first + refactor prompts; Uber = concurrency + event-driven ride models; Flipkart/Walmart = full LLD + name-the-patterns; C++/JVM/Python shops = deep internals (v-tables/move, GC/erasure, MRO/dunders) + performance + ownership. Calibrate by level: junior = recall-with-example, senior = design-and-extend. Universal habits: always name a rejected alternative, justify every pattern by its change point, walk a concurrency race, and state complexity. Drill via Section 01's top-100 filtered by your target's heatmap plus Sections 02-03 LLD/coding problems.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does Amazon/Google/Uber ask in OOPs?" | 13 Interview Questions (heatmaps) |
| "How do I tailor prep to my company?" | 2 / 9 Internal Working / 18 Cheat Sheet |
| "What's the senior depth bar?" | 3 / 18 Cheat Sheet |
| "What universal follow-ups should I prepare?" | 14 Follow-Up Questions |
| "Where do I drill these?" | Section 01 (top-100) / Sections 02-03 |
| "Why might my company's bar differ?" | 12 Disadvantages / 13 (role note) |
