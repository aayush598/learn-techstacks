# Chapter: Encapsulation

## What you'll learn
- The precise definition of **encapsulation** — bundling data + behavior into a class AND hiding the internal state from outsiders — and why "encapsulation = getters/setters" is an oversimplification.
- **Information hiding** as the deeper principle (Parnas): hide *design decisions* that are likely to change, not just fields.
- How to protect data: private fields, immutable types, defensive copies, unmodifiable views, and the "leaky getter" anti-pattern.
- How **getters/setters/properties** work in Java vs C# (`{ get; set; }`) vs Python (`@property`), and when a setter is actually justified vs when it's just a public field in disguise.

## Prerequisites (linked)
- [Part 01, Chapter 02 — Access Modifiers and Scope](../../part-01-oops-fundamentals/chapter-02-classes-and-objects-in-depth/section-04-access-modifiers-and-scope.md): you must know `private`/package-private precisely.
- [Part 01, Chapter 01 — Identity, State, and Behavior](../../part-01-oops-fundamentals/chapter-01-introduction-to-oops/section-05-identity-state-and-behavior.md): state vs identity, mutability.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Encapsulation in Depth](section-01-encapsulation-in-depth.md) | The full definition: bundling + hiding; what encapsulation protects; examples of breaking it |
| [Section 02 — Information Hiding and Data Protection](section-02-information-hiding-and-data-protection.md) | Parnas's principle; design decisions, defensive copies, unmodifiable views, immutability |
| [Section 03 — Getters, Setters, and Properties](section-03-getters-setters-and-properties.md) | Accessor design; when setters are valid; Java/C#/Python property syntax |

## One-paragraph narrative connecting all sections
Encapsulation exists because unguarded state corrupts: without bundling + hiding, any code can mutate an object's fields and break its invariants (Section 01). The *principle* underneath is information hiding — you hide the details most likely to change (storage format, algorithm, internal collections) behind a stable surface (Section 02). The surface you expose is the accessor API: getters that return safe copies, setters that validate, properties that look like fields but are really methods (Section 03). Together: hide the data, guard every read/write, and change the inside freely while the outside contract stays stable — which is exactly the SRP/OCP foundation used later in Part 06.

## Common interview trap in this chapter
Two traps. First: "Encapsulation means making fields private with getters and setters." That's only the *mechanical* half — encapsulation's real point is bundling behavior *with* the data so invariants hold; getters/setters that just expose fields often *weaken* it. Second: "Encapsulation = abstraction." They are different (encapsulation hides *state*, abstraction hides *implementation behind a contract*) — you must articulate both sides of the coin in one sentence, and the dedicated comparison section lives in Chapter 02.

## Checklist before moving on
- [ ] I can define encapsulation as bundling + hiding, and give an example of how invariants break without it.
- [ ] I can explain information hiding (Parnas) and name three "design decisions" worth hiding.
- [ ] I can design a class with private fields, validation, defensive copies, and immutable views — no leaky getters.
- [ ] I can write a getter that returns an unmodifiable copy, and justify when a setter is acceptable.
- [ ] I can compare accessors across Java (methods), C# (properties), Python (`@property`).
- [ ] I can explain why "getters/setters everywhere" is an anti-pattern, not the goal.
