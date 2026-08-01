# Part: SOLID and Design Principles

## What this part covers
This part is where the four pillars turn into **judgment**. SOLID — the five object-oriented design principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) — is the checklist interviewers use to test whether you can *design*, not just *code*. You'll learn each principle precisely (what it is, what it prevents, how to violate and fix it, real-world examples), plus the supporting principles that keep designs maintainable: DRY, KISS, YAGNI, composition-over-inheritance, the Law of Demeter, and the coupling/cohesion axis. And because principles only matter when code goes bad, the part ends with **code smells and refactoring** — how to recognize design rot (god classes, feature envy, shotgun surgery) and refactor toward SOLID mechanically. After this part, "is this good OOP?" becomes a question you can answer with named principles instead of vibes.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 SOLID Principles | SRP; OCP; LSP; ISP; DIP | State each principle's definition, apply it to code, recognize and fix violations, quote the "clean" mantras and their limits |
| ch-02 Other Principles & Best Practices | DRY/KISS/YAGNI/composition-over-inheritance; Law of Demeter & coupling-cohesion; code smells & refactoring | Apply the pragmatic principles, reduce coupling, increase cohesion, identify smells, refactor safely |

## Study order
1. **ch-01 (SOLID)** first — one section per principle, in the SOLID order (S → O → L → I → D); each section is self-contained but they build: OCP is *enabled by* LSP, DIP is the umbrella that OCP relies on.
2. **ch-02** second — DRY/KISS/YAGNI are the pragmatism guardrails; coupling/cohesion is the underlying metric; code smells/refactoring is the applied practice that closes the loop.
3. Read every section's "Common trap" and the cheat sheet — interviewers probe the *limits* of these principles (when NOT to apply them) more than the definitions.
4. Assumes the entire **OOPs core** — SOLID is meaningless without polymorphism (Part 04) and relationships (Part 05).

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — SOLID is *the* most-asked OOP design topic in interviews: "Explain SOLID", "Which principle does this code violate?", "Design X following SOLID." LSP and DIP are the two most probed.
- **Emphasized by**: Amazon (behavioral + LLD rounds love "what principle is violated here?"), Google/Microsoft (design rounds), every backend Java/C# shop; clean-code interviews at high-growth startups quote Robert Martin directly.
- Typical asked: "Explain the SOLID principles with examples.", "What is the difference between OCP and DIP?", "How do you detect an LSP violation?", "Why is SRP the most violated principle?", "Give a real-world ISP example.", "What is the Law of Demeter?", "Name 5 code smells."

## How the parts connect (roadmap)
- SOLID sits **on top of** everything so far: SRP and ISP depend on encapsulation (Part 02); OCP, LSP, and DIP are *built on* polymorphism (Part 04); relationships (Part 05) are the medium the principles govern.
- **Design patterns (Part 07+)** are the *canonical implementations* of these principles — Strategy is OCP + DIP, Template Method is OCP, Factory is DIP, Adapter is OCP. Learning SOLID first makes patterns feel inevitable.
- **System design** reuses the same vocabulary at scale — module boundaries, contracts, dependency direction — so this part is also your bridge into architecture rounds.
- After this part you can defend any design decision with a named principle — the mark of an LLD candidate, not just a coder.
