# GATE ECE Question Bank — Authoring Style Guide

This repository is a **question-only self-study resource** for GATE ECE. The reader is
assumed to have *not* read any theory/notes. Every question must therefore be
**self-contained and self-explanatory**: reading Q → reading the answer block must be
enough to learn the concept.

## Hard rules (read before writing)

1. **No reference to external material.** Never write "as discussed in Chapter 5",
   "see Sadiku", "refer to Lecture 12", "as you studied earlier". A question must be
   answerable in isolation.
2. **Every question has a full solution block**, in this exact shape.
3. **Zero placeholders.** No "Q1-50 similar", no "etc.", no "...", no TODOs, no
   "repeat above". Every single question must be individually written out.
4. **No duplicate questions.** Within a file and across the subject directory, each
   question must test a distinct concept/fact. Vary the *angle*: definition →
   derivation → numerical → multiple-choice → conceptual trap → comparison → GATE-style
   extended problem → common-mistake question.
5. **Difficulty mix** per file, target roughly:
   - 15% definition/fact recall
   - 20% formula application / quick numerical
   - 25% medium 2–4 mark problems
   - 20% GATE 1-mark MCQ (including trap options)
   - 20% GATE 2-mark MCQ / NAT / MSQ
6. **Numerical discipline.** Every number you produce must be arithmetically
   self-consistent. Recheck sums, powers, roots, complex arithmetic, unit conversions.
   Round to 3–4 significant digits and say "≈".
7. **Units everywhere** for physics/electrical subjects.

## Question block format (use this literally)

### Q{n}. {Question text}

> **Type:** {MCQ / NAT / MSQ / Numerical / Conceptual / Theory / Comparison / Common-mistake}
> **Answer:** {The answer — for MCQ give the value/text, not the option letter, but you
> may add "(Option c)" in brackets when you invent options.}
> **Solution:** {2–6 sentences. Show the actual reasoning, not "obvious". Include the
> governing formula and its symbols' meaning inline the first time in the file.}
> **Key point:** {One crisp line — the takeaway, formula, or trap.}

## File format

```markdown
# {Subject} — {File title}

> Part {k} of the {Subject} question bank · Questions {a}–{b} of this file
> Read this file top to bottom, in order. It continues from `{previous file}` and
> is followed by `{next file}`.

## Section {i}. {Section name}

...(questions)...

## Quick revision — {File title}

- 15–30 bullet points, each a one-line formula/fact/trap from THIS file only.
```

Every file ends with a `## Quick revision` block of condensed bullets. This is the
"blind revision" surface the candidate uses the night before the exam.

## File header requirements

- Title
- One-line "what this file covers" + "what the reader must already know"
- Rough question count and difficulty distribution

## Cross-linking

When a question naturally connects to another subject, add a single inline note like
`*(Deep dive: see \`../04_signals_and_systems/04_z_transform_and_state_space.md\`.)*`
Only use this for genuinely useful pointers and only for files that actually exist —
use the exact directory/file names listed in the INDEX. Do not overuse.

## What makes a great GATE question here

- **Trap MCQs**: two plausible options where the wrong one comes from a real
  misconception (e.g. confusing `f` with `ω`, `Z` with `Y`, RMS with average).
- **Inverse questions**: give the result, ask for the condition (e.g. "In which case is
  the two-port Z-parameter matrix symmetric?")
- **Comparison questions**: two quantities, "which is larger / by what factor".
- **Missing-data questions**: "What additional information is required to find X?"
- **Boundary cases**: what happens as a parameter → 0 or ∞, or as frequency → 0 or ∞.
- **Dimensions/unit sanity checks** (physics subjects).
- **Multi-concept synthesis**: two chapters combined, as in real GATE questions.

## Volume target

Minimum **1000 questions per subject**, split into 5 files of ~200–250 questions each.
Prefer more. Do not pad with trivial rephrasings of the same fact — if you run short of
distinct concepts, use the angle-variation techniques above.
