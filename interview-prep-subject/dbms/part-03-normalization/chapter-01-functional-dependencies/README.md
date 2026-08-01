# Chapter: Functional Dependencies

## What you'll learn
- **Functional dependencies in depth**: what X→Y means, trivial vs non-trivial, determining FDs from relation data, and why they're the *foundation* of every normal form.
- **Armstrong's axioms & closure of attribute sets**: reflexivity, augmentation, transitivity; how to compute X⁺ (the closure algorithm) and use it to find all candidate keys — the exact method for "is this in BCNF?" questions.

## Prerequisites (linked)
- [Part 02 (Relational Model & SQL)](../../part-02-relational-model-and-sql/README.md) — keys and relations from Part 02's Chapter 01 are the vocabulary FDs use.
- Feeds into [Chapter 02 (Normal Forms)](../chapter-02-normal-forms/README.md) — every normal form is *defined* by which FDs are allowed.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Functional Dependencies in Depth](section-01-functional-dependencies-in-depth.md) | X→Y semantics, finding FDs, trivial/non-trivial, FD sets |
| [Section 02 — Armstrong's Axioms and Closure of Attribute Sets](section-02-armstrongs-axioms-and-closure-of-attribute-sets.md) | The 3+3 inference rules, X⁺ computation, candidate-key derivation |

## One-paragraph narrative connecting all sections
Functional dependencies are the answer to "what *should* be determined by what?" in a relation — a statement like `sid → name` means "given a student id, the name is fixed." Section 01 establishes what an FD is, how to discover the FDs of a relation from its meaning (not just sample data), and the trivial/non-trivial distinction. Section 02 makes FD reasoning *computational*: Armstrong's axioms give a sound-and-complete set of inference rules, and the attribute-closure algorithm X⁺ turns those rules into a mechanical method for finding all candidate keys — the exact tool you'll need in Chapter 02 to test 2NF/3NF/BCNF.

## Common interview trap in this chapter
Candidates claim an FD is invalid just because *the current sample data* has no violation. FDs come from the **mini-world semantics** — "in this company an employee has exactly one department" — not from whatever rows happen to be loaded. Also, students forget that a candidate key is defined via closure: X is a candidate key iff X⁺ covers all attributes *and* no proper subset does. If you only check "does X uniquely identify rows in the sample?" you'll fail real problems.

## Checklist before moving on
- [ ] I can state what X→Y means and write the three Armstrong axioms from memory.
- [ ] I can compute X⁺ for any attribute set given a set of FDs, by hand.
- [ ] I can find all candidate keys of a relation from its FDs (via the "attributes never on the RHS" start).
- [ ] I can identify trivial vs non-trivial FDs and non-triviality's role in normalization.
- [ ] I can justify an FD from the mini-world semantics, not just sample data.
- [ ] I know that X→Y with Y ⊆ X is trivial and can be dropped without losing info.
