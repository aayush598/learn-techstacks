# OOPs Crash Course — Revision

> **TL;DR**: The entire OOPs resource compressed to a 30-minute revision pass — one page of fundamentals, SOLID, patterns, language internals, and LLD bullets you can read the night before (or morning of) any interview, with a self-test to find gaps.

## 1. Why Does This Exist?
When interview day arrives you don't have time to re-read 9 parts. You need a **compression layer**: the few facts, formulas, and framings that carry the most interview weight, organized so you can re-derive everything else from them. This crash course exists because recall is fastest when it's structured — reading these bullets reactivates the whole map (parts → sections → examples) you built during prep.

## 2. How Does It Work?
Four sections: (1) Fundamentals & pillars (2 minutes), (2) Relationships + SOLID (3 minutes), (3) Patterns (5 minutes), (4) Language internals — Java / C++ / Python (10 minutes), (5) LLD + coding (5 minutes), plus a 5-minute self-test. Time-box each block; anything you can't recall → note it → hit that part's Revision section tonight.

## 3. When Is It Used?
- **Night before**: full pass + fill gaps.
- **Morning of**: the self-test + cheat sheets only.
- **In the waiting room**: skim the tables.
- **Between rounds**: re-read the pattern list and your company's heatmap (Section 04).

## 4. Why Wasn't Another Approach Chosen?
Long-form notes fail under time pressure (you can't re-read 2000 lines before a 45-minute interview), and raw flashcards lack the *connecting structure* that makes recall fast. A structured compression — where each bullet links to a mental example — gives the best recall-per-minute. It intentionally *omits* depth: it's a trigger, not a teacher. When a trigger fails to fire, the mapped part/section is the rescue route.

## 5. Intuition
Think of this as a **mental map with pins**. Each bullet is a pin; touching a pin expands it into the full section you studied. "Four pillars" expands to `Encapsulation→private`, `Abstraction→interface`, `Inheritance→IS-A`, `Polymorphism→one interface many forms`. If a pin is missing (you can't expand it), that's a gap — mark it and return to that part. The map is what lets you answer fast and stay organized under pressure.

## 6. Real-World Analogy
A **pilot's pre-flight checklist**: not a flight manual, but a compact list that triggers the right procedure for each system — if "landing gear down" doesn't trigger "are they green?" you know exactly which manual to open. The crash course is your pre-flight checklist; the parts are your manuals.

## 7. Formal Definition
A crash-course revision is a high-density, structured summary designed for rapid recall activation: it enumerates the core concepts, their interconnections, and the most commonly probed details of a knowledge domain, trading exhaustiveness for retrieval speed, and is intended to be consumed immediately before an assessment to prime schema activation.

## 8. Example
The 30-minute pass in action:
- Minute 0-2: pillars + class/object (say each definition + one example aloud).
- Minute 2-5: relationships + SOLID (recite the 5 principles + one violation example each).
- Minute 5-10: patterns (name 23 → categorize → say intent of the 10 most asked).
- Minute 10-20: Java (memory/GC/immutability/erasure/exceptions/FP), C++ (vtable/move/Rule5/smart ptrs), Python (MRO/super/dunders/hash).
- Minute 20-25: LLD loop + one design you can reproduce (Parking Lot).
- Minute 25-30: self-test — the 10 questions below; any miss = tonight's gap-fill.

## 9. Internal Working
1. Say every bullet *aloud* (auditory recall is stronger than silent reading).
2. For each bullet, produce a **1-line example** from memory — if you can't, you don't own it.
3. Self-test (Q&A below): answer without peeking; score yourself.
4. Log gaps: map each miss to a part/section via the sources listed in each block.
5. Repeat the weakest block once more; then sleep (consolidation) and skim the cheat sheets in the morning.

## 10. Time Complexity
- Full pass: ~30 minutes (sections are sized to their interview weight).
- Self-test: ~5 minutes; gap-filling: variable (target the 2-3 weakest pins only).
- Morning skim: ~5 minutes (cheat sheets + company heatmap).

## 11. Advantages
- One artifact covers all 9 parts — no flipping between files the day before.
- Sized by interview weight (Java/C++/Python internals get the most time).
- Self-test makes gaps visible and fixable in one evening.
- Structured recall (map → pins) is faster and more reliable than linear rereading.

## 12. Disadvantages
- By design it lacks depth — can't *teach* a concept, only trigger it.
- Heavy bias toward "most-asked" facts; niche questions won't be covered.
- Reciting bullets isn't practice; you still need mocks and coding reps (Sections 02-03).
- Language-heavy emphasis shortchanges a Python-only target if you use it without tailoring.

## 13. Interview Questions (the self-test — answer aloud, then check)
1. **Q: Four pillars + one example each?** A: Encapsulation (private fields + getters), Abstraction (interface Payment), Inheritance (Car extends Vehicle), Polymorphism (`process(Payment p)` runs the right impl at runtime).
2. **Q: Abstract class vs interface (Java)?** A: Abstract = state + concrete methods + single inheritance; interface = contract + defaults + multiple. Use abstract for shared base impl, interface for capability.
3. **Q: Composition vs inheritance — when to choose?** A: Composition by default (flexible, encapsulated, IS-A only when true with behavior reuse). Delegation implements it.
4. **Q: Name all five SOLID with a violation example.** A: SRP (god class), OCP (edit class to add feature), LSP (Square↔Rectangle), ISP (fat interface forced on a client), DIP (high-level depends on concrete DB).
5. **Q: What do these patterns do — Singleton, Factory, Builder, Adapter, Decorator, Proxy, Strategy, Observer, Command, State?** A: one instance; create products; stepwise build; convert interface; add behavior dynamically; control access; swap algorithm; notify listeners; encapsulate action; state-driven behavior.
6. **Q: Where do Java objects live + when does the GC collect them?** A: Heap (refs on stack/fields, metadata Metaspace); when unreachable from GC roots (stacks, statics, JNI, classloaders).
7. **Q: What is type erasure + what can't you do?** A: Compiler replaces T with bounds; runtime sees raw types; can't `new T()`, `instanceof T`, generic arrays; PECS = Producer Extends, Consumer Super.
8. **Q: How do you make a Java class immutable + why is it thread-safe?** A: final class + final fields + copies + no mutators; JLS §17.5 gives lock-free safe publication after construction.
9. **Q: What is a v-table and why a virtual destructor?** A: Per-class array of function pointers; object's vptr dispatches by dynamic type; virtual dtor so `delete base` runs the derived dtor (else UB).
10. **Q: Python — MRO, `super()`, and why `__eq__` kills `__hash__`?** A: C3 linearization (D(A,B)→D,A,B,Base); super() = next in MRO (cooperative); `__eq__` sets `__hash__=None` → unhashable, restore it.

## 14. Follow-Up Questions (the probes you should expect)
1. **"Give me a code example of that."** → Have the tiny `interface Payment` example ready; it answers most "show me" prompts.
2. **"Why is that better than the alternative?"** → Name one rejected alternative + its cost (e.g., "composition over inheritance because fragile base + no IS-A").
3. **"What's the cost of your approach?"** → Be honest: GC pauses, vptr memory, atomic refcount contention, copy-on-write allocation, MRO scan.
4. **"Design a small system around that."** → Run the LLD loop aloud (Section 03): clarify → entities → relationships → SOLID/patterns → code.
5. **"What did you skip?"** → Confidently list scope exclusions — interviewers reward boundary-awareness.

## 15. Coding Example
```java
// The universal "show me polymorphism" snippet — memorize its shape
interface Payment { void pay(int cents); }

class CardPayment implements Payment {
    public void pay(int cents) { /* charge card */ }
}
class WalletPayment implements Payment {
    public void pay(int cents) { /* debit wallet */ }
}
class Checkout {
    void charge(Payment p, int cents) { p.pay(cents); }   // dynamic dispatch = polymorphism
}
// Extend: add new Payment impl -> no Checkout change (OCP)
```
```python
# The universal "duck typing + dunders" snippet
class Cart:
    def __init__(self): self._items = []
    def __iadd__(self, item):            # supports cart += item
        self._items.append(item); return self
    def __len__(self): return len(self._items)
    def __iter__(self): return iter(self._items)   # makes it iterable

c = Cart(); c += "book"
print(len(c), list(c))                    # 1 ['book']
```
```cpp
// The universal "Rule of Five + smart pointers" snippet
#include <memory>
class Widget {
    std::unique_ptr<int> p;               // sole ownership, zero overhead
public:
    Widget() : p(std::make_unique<int>(0)) {}
    Widget(const Widget&) = delete;       // not copyable
    Widget(Widget&&) noexcept = default;  // movable
};
auto w = std::make_unique<Widget>();      // move-only ownership transfer
```

## 16. Industry Usage
- Candidates use crash courses exactly this way: schema-reactivation the night before, skim + self-test the morning of, and gap-fill from the source parts between interviews.
- Interviewers expect the *framings* in this section — the standard answer shape (define → contrast → when → example) is what makes answers land in 30 seconds.
- Recruiters' interview-prep guidance (Amazon, Google) universally recommends compact revision before the loop; this course is that artifact for OOPs.

## 17. References
- This resource: Parts 01-08 (each bullet maps to a part/section), Part 09-S1 (top-100), Part 09-S3 (LLD), Part 09-S4 (company heatmaps).
- Cracking the Coding Interview (McDowell) — OOP chapters.
- System Design Interview (Xu) — LLD process.
- Refactoring Guru — pattern intents (for the pattern table).
- Effective Java (Bloch) Items 17, 26-33 — the Java bullets' sources.

## 18. Cheat Sheet
- Answer shape: **define → contrast → when-to-use → example** (≤30s).
- Pillars: Encapsulation (hide state), Abstraction (hide impl), Inheritance (IS-A), Polymorphism (one interface, many forms).
- Composition > inheritance unless true IS-A; delegation = composition's tool.
- SOLID: SRP OCP LSP ISP DIP — patterns are their recipes.
- Patterns (intents): Singleton one; Factory creates; Builder stepwise; Adapter converts; Decorator extends; Proxy controls; Strategy swaps; Observer notifies; Command encapsulates; State drives.
- Java: heap/GC by reachability; erasure + PECS; immutable ⇒ §17.5 safe-publish; checked vs unchecked.
- C++: v-table + virtual dtor; RTTI/dynamic_cast; Rule of Five; unique/shared/weak_ptr; std::move is a cast.
- Python: C3 MRO; super() cooperative; dunders for operators; __eq__ kills __hash__.
- LLD loop: clarify → entities → relationships → SOLID/patterns → code → edge cases → test.
- Always: name a rejected alternative; justify patterns; walk a race; state complexity.

## 19. Quiz (final self-check — 10 questions, 10 minutes)
1. Which is runtime polymorphism? a) Overloading b) Overriding c) Templates d) Static → **b**
2. LSP is broken by: a) Subtype narrowing behavior b) Adding methods c) Interfaces d) Composition → **a**
3. Best singleton: a) `synchronized` getter b) enum/holder c) double-check no volatile d) static field → **b**
4. Java GC collects: a) All objects on demand b) Unreachable-from-roots objects c) Only young gen d) Never → **b**
5. PECS says: a) Producer Super b) Producer Extends, Consumer Super c) Everything extends d) Nothing → **b**
6. Immutable ⇒ thread-safe because: a) It's final b) JLS §17.5 safe publication c) No GC d) It's a record → **b**
7. `dynamic_cast` failure (pointer): a) Throws b) nullptr c) UB d) void* → **b**
8. Rule of Five = dtor + copy + : a) clone b) move ctor/assign c) operator+ d) virtuals → **b**
9. Python `D(A,B)` MRO: a) D,B,A,Base b) D,A,B,Base c) Base first d) A,D,B → **b**
10. The first LLD step: a) Code b) Clarify requirements c) Patterns d) UML → **b**

## 20. Flashcards
- **Q: Answer shape?** → **A:** Define → contrast → when → example, ≤30s.
- **Q: When composition vs inheritance?** → **A:** Compose by default; inherit only for true IS-A with reuse.
- **Q: SOLID list?** → **A:** SRP, OCP, LSP, ISP, DIP.
- **Q: Pattern intents (10)?** → **A:** one/create/build/convert/extend/control/swap/notify/encapsulate/state.
- **Q: Java safe publication?** → **A:** Immutable class → §17.5 → lock-free share.
- **Q: PECS?** → **A:** Producer Extends, Consumer Super.
- **Q: Virtual dtor why?** → **A:** So delete base runs derived dtor; else UB.
- **Q: super() in Python?** → **A:** Next class in the C3 MRO (cooperative).
- **Q: LLD loop?** → **A:** Clarify → entities → relationships → SOLID/patterns → code → edges.
- **Q: Universal follow-up?** → **A:** "Why this over the alternative?" + "what's the cost?"

## 21. Revision
In 30 minutes: recite pillars + one example each; the abstract/interface rule; composition-over-inheritance; the five SOLID principles with a violation each; the 10 pattern intents; Java (heap+GC by reachability, erasure+PECS, immutable⇒§17.5, checked vs unchecked); C++ (v-table+virtual dtor, RTTI, Rule of Five, unique/shared/weak_ptr); Python (C3 MRO, cooperative super(), dunders, __eq__ kills __hash__); the LLD loop; and the universal Payment-snippet for "show me polymorphism." Self-test with the 10 questions; any miss → that part's Revision section tonight. Morning: cheat sheets + company heatmap (Section 04). Always close answers with an example and expect a "why this over that?" follow-up.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Quick revision before the interview?" | 13 (self-test) / 18 (cheat sheet) / 21 (revision) |
| "Which parts to re-read for gaps?" | 9 Internal Working (gap mapping) |
| "Show me polymorphism fast" | 15 Coding Example |
| "What follow-ups to expect?" | 14 Follow-Up Questions |
| "What does my company emphasize?" | Part 09-Section 04 |
| "Where are the full details?" | Parts 01-08 of this resource |
