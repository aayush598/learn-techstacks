# Content Style Guide — Infosys DSE Pre-Test Mastery

> This guide defines the exact structure, depth, and tone of every file in this resource.
> The pre-test rewards **speed + accuracy**, not encyclopedic reading. Every file must therefore
> be **answerable**, **timed**, and **self-contained**. Read this before writing anything.

---

## 1. Audience and Learning Objective

The reader is an off-campus / campus hire applying to **Infosys Digital Sourcing & Engineering (DSE)**
who must clear the **pre-test** to unlock stream selection. Success is binary in the moment:

- 60 questions, 90 minutes → ~90 seconds per question average.
- 65% pass mark (39/60 minimum) to proceed to stream selection.

Every file must be:

- **Self-contained** — a reader who opens only this file still learns something complete.
- **Drill-oriented** — concepts end in a rule, a shortcut, or a timed drill, never in theory alone.
- **Exam-honest** — say what the pre-test actually asks, not what a textbook asks.
- **Fast-scannable** — tables, decision rules, worked examples. Minimum reading friction.

---

## 2. Directory Layout (fixed)

```
Infosys-DSE-Pretest-Mastery/
├── README.md                      # master index, exam facts, 7-day plan, how to use
├── _STYLE_GUIDE.md                # this file
├── 00-Exam-Blueprint/             # pattern, timing, sectional strategy, thresholds, streams
├── 01-Aptitude/                   # Section 1 — 10 questions
├── 02-English-And-LD/             # Section 2 — 15 questions
├── 03-DBMS-SQL/                   # Section 3 — 10 questions
├── 04-Java/                       # Section 4 — 25 questions
├── 05-Mock-Tests/                 # four full 60-question papers + answer keys
├── 06-Study-Plans/                # crash plans, stream advisory, mistakes to avoid
└── 07-Cheat-Sheets/               # last-minute one-pagers
```

Each topic folder follows the same shape:

```
NN-topic-slug/
├── README.md                      # topic overview, objectives, file index, key takeaways
├── 01-concepts/                   # the "what" — rules, definitions, mental models
├── 02-techniques/                 # the "how" — shortcuts, formulas, solving procedures
├── 03-worked-examples/            # full solved questions, step by step
├── 04-pitfalls/                   # traps, wrong-turn stories, must-avoid patterns
└── 05-reference/                  # cheat sheets, decision tables, quick-revision lists
```

Every topic folder MUST contain a `README.md`. Every populated subfolder SHOULD contain a
`README.md` listing its files (one line each). Number files so they sort correctly: `01-...md`.

---

## 3. File Anatomy

A typical concept/technique file:

```markdown
# <Descriptive Title>

> Section 1 · Aptitude · Percentages  ·  _Estimated reading time: N min_
> **Prerequisite:** <relative link or "none">

## In one sentence
<The single most important takeaway. **Bold the key phrase.**>

## Why the pre-test tests this
<1–3 bullets tying the topic to a real pre-test question archetype.>

## Core concept
<The rules. Use a table when there is more than 3 rules.>

## Worked example
<Full question → options → step-by-step solution → answer → why the distractors fail.>

## Quick rules
<5–8 bullets the reader can recall in 30 seconds under exam pressure.>

## Common traps
<What the exam tries to lure you into.>

## Checklist
- [ ] <actionable self-check>

## Related
- [Sibling file](relative-link.md)
```

A **question bank** file looks like this:

```markdown
# <Topic> — Question Bank

> Section 1 · Aptitude · Percentages  ·  _30 questions · ~45 min_

**How to use this bank:** answer all questions on paper with a 90-second cap each. Answers +
brief reasoning at the bottom. Score yourself honestly.

---

## Q1. <question text>

A. <option>
B. <option>
C. <option>
D. <option>

---

## Q2. ...

---

# Answer key

| Q | Answer | Why (one line) |
|---|--------|----------------|
| 1 | B | 15% of 200 = 30; compound applies only to the 100, so 130. |
```

---

## 4. Non-Negotiable Rules

1. **No fake URLs.** Never invent a link. Only link to files that exist in this repo.
2. **Relative links only** — `../03-worked-examples/01-example.md`. Never absolute paths.
3. **Real numbers.** Every question must have real options and a definite correct answer.
   No "Option A/B/C/D" placeholders. No "all of the above" unless it is genuinely correct.
4. **No fabricated exam dates, fees, or pass percentages** beyond what is stated in the
   `00-Exam-Blueprint` README. If unsure, say "reported by candidates" or "varies by batch".
5. **Explain the distractor.** A question is only useful if you know why each wrong option is wrong.
6. **The only allowed emoji characters** are ✅ ❌ ⚠️ 🔥 and nothing else.
7. **Consistent headings.** `## In one sentence` then `## Why the pre-test tests this` then
   `## Core concept` then `## Worked example` then `## Quick rules` then `## Common traps`
   then `## Checklist` then `## Related`.
8. **One topic per file.** If a file covers two topics, split it.
9. **Java code must be compilable in your head** — every output-prediction question must have a
   determinate answer. State the Java version you assume (default: Java 8, since pre-tests run on it).
10. **SQL must be standard SQL** with MySQL-compatible notes where it matters.

---

## 5. Depth and Length Targets

| File type | Target length | Notes |
|-----------|---------------|-------|
| Topic `README.md` | 80–160 lines | overview + objectives + file index + takeaways |
| Concept file | 150–320 lines | rules, tables, examples |
| Technique file | 150–300 lines | procedures, shortcuts |
| Worked-example file | 200–400 lines | 5–10 fully solved questions |
| Pitfalls file | 120–250 lines | traps with wrong answer + right answer |
| Reference file | 100–250 lines | tables, lists, one-pagers |
| Question bank | 400–900 lines | 20–40 questions + answer key |
| Mock test | 500–900 lines | 60 questions + full answer key with reasoning |

If a file falls under 100 lines, it is probably a stub — either deepen it or merge it.

---

## 6. Tone

- Direct. Second person. "You have 90 seconds. Read the stem first."
- No hype, no motivational filler, no "in today's fast-paced world".
- Give the *recommended* answer in behavioural/L&D questions, then explain why.
- Numbers over adjectives. "90 seconds per question" beats "very fast".
- Acknowledge uncertainty honestly when the pre-test varies by batch or year.

---

## 7. The Recurring Cast

Use one consistent fictional workplace in examples so patterns stick. The cast:

- **Ananya** — 3rd-year B.Tech student, first Infosys attempt, average at aptitude.
- **Rahul** — 2nd-year B.Tech student, strong in Java, weak in English.
- **Meera** — final-year B.Tech, strong in DBMS, panics under time pressure.
- **Karthik** — placed in the UI stream, gives the retrospective "what I wish I knew" voice.
- **Infosys DSE pre-test** — always referenced as "the pre-test", never as "the exam".
- **The 90-second rule** — the recurring time-management motif of this whole resource.

---

## 8. Definition of Done (per file)

Before you finish a file, confirm:

- [ ] It starts with a title, a context line, and a prerequisite link.
- [ ] `## In one sentence` exists and contains a bolded takeaway.
- [ ] At least one table OR a numbered procedure.
- [ ] At least one fully worked example with a definite answer.
- [ ] `## Common traps` exists and is non-empty.
- [ ] `## Checklist` exists with 3+ actionable items.
- [ ] `## Related` links to files that actually exist.
- [ ] No invented URLs, no placeholder text, no TODOs.
- [ ] Reading time estimate is present and plausible.
