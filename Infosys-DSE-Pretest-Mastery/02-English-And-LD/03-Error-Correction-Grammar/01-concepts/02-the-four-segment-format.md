# The Four-Segment Format

> Section 2 · English & L&D · Error Correction ·  _Estimated reading time: 7 min_
> **Prerequisite:** [Error taxonomy](01-error-taxonomy.md)

## In one sentence
**The item gives you one sentence with four underlined segments — three are correct and one breaks a rule — so your job is to find the single violation, not to rank the writing quality.**

## Why the pre-test tests this

- The prompt is almost always: *"Identify the part of the sentence that contains an error."* or *"Find the
  part of the sentence that contains an error and mark it."*
- The four options are **not four different sentences**. They are four chunks of the same sentence, usually in
  reading order. That structure is a huge clue: the correct answer is usually a chunk that contains a **verb**,
  because most errors live near the verb.
- Candidates who read the options first and judge each chunk in isolation fail these items, because a chunk can
  be correct on its own and wrong in context — or wrong on its own and rescued by context.

## Core concept

### Anatomy of the item

```
Identify the part of the sentence that contains an error.

  The team of developers [A] agreed to release the module on Friday, [B] the client
  [C] informed about the change in the scope of the work [D].

A. The team of developers has
B. and the client have been informed
C. change in the
D. scope of the work
```

| Element | What it is | How to use it |
|---------|-----------|---------------|
| The sentence | One sentence with a gap or an underline | Read it **once, complete**, before looking at the options |
| The 4 options | Chunks of the same sentence, usually in order | Judge each chunk **inside its clause** |
| The rule | Exactly one chunk breaks a rule | Find the violation, then sanity-check that the other three are clean |

### How the distractors are built

| Distractor type | How it is made | What it looks like |
|-----------------|---------------|-------------------|
| **Verbless chunk** | A noun phrase, prepositional phrase, or adverbial | "change in the", "on Friday", "for the module" |
| **Long but correct** | A complete clause with correct agreement | "and the client has been informed" |
| **Formal/rare phrase** | Correct but unusual wording | "in accordance with the requirements" |
| **Tricky chunk** | Contains the correct word but in a position that is actually fine | "a team of developers has" |

⚠️ Because three of the four are correct, **you do not need a reference grammar**. You need to find the one chunk
that is *provably* wrong. If two chunks look wrong, one of them is correct and your rule application is off.

### The "verb-carrying chunk" heuristic

Errors cluster around the verb. In a 4-option item:

- 2 options typically contain the **finite verb** of the sentence → one of them usually holds the error
  (agreement or tense).
- The other 2 are noun phrases, prepositional phrases, or adverbials → those hold article, preposition, or
  modifier errors.

**Practical use:** test the two verb-bearing chunks first (agreement + tense), then the other two (articles,
prepositions, modifiers). This cuts your scan time roughly in half.

### The 6 elimination tests

Apply to each chunk in turn. Any chunk that fails is the answer — but confirm the others pass.

| # | Test | Question | Example failure |
|---|------|----------|-----------------|
| 1 | **Agreement** | Does the verb agree with the head noun of its own subject? | "the client have been informed" ❌ |
| 2 | **Tense** | Is the tense consistent with the rest of the sentence and its time markers? | "Yesterday I **am** working" ❌ |
| 3 | **Article** | Should there be an article, and is it the right one (by sound)? | "a hour", "the team are" |
| 4 | **Preposition** | Is the preposition the one this verb/noun collocates with? | "discuss about", "depends of" |
| 5 | **Modifier** | Does the modifier attach to the noun it is supposed to describe? | "the file **which I sent** to Rahul" |
| 6 | **Connector** | Is a comma splice or a double negative present? | "It failed, we fixed it." ❌ |

### Judging a chunk in context — the method

```
1. Expand the chunk to the full phrase it belongs to.
2. Identify the clause the chunk sits in.
3. Identify that clause's own subject and its own finite verb.
4. Test the chunk against the 6 elimination tests.
5. Ask: if I corrected this chunk, would the whole sentence become correct?
```

Step 5 is the strongest confirmation: a real error can be repaired by changing **one chunk**. If fixing a chunk
still leaves the sentence broken, it was not the error.

### When the sentence has two clauses

Most error-correction sentences are compound or complex. Label the clauses before judging:

```
Clause 1:  The team of developers has agreed to release the module on Friday
Clause 2:  and the client have been informed about the change in the scope of the work
```

Each clause has its own subject and verb. Clause 2's verb is judged against **Clause 2's** subject, not
Clause 1's. Roughly half of the candidates' wrong answers come from applying Clause 1's subject to Clause 2's
verb.

## Worked example

> **Q.** Identify the part of the sentence that contains an error.
>
> "Each of the trainees **were given** a laptop **and** **the trainer has explained** the **process of** **the onboarding** in detail."
>
> A. Each of the trainees were given
> B. and the trainer has explained
> C. the process of
> D. the onboarding in detail

**Answer: A**

| Chunk | Tests applied | Verdict |
|-------|---------------|---------|
| A | **Agreement.** The subject of the clause is "Each" — an indefinite pronoun, always singular. The verb must therefore be "**was given**", not "were given". The phrase "of the trainees" is a prepositional phrase and does **not** control the verb; the pre-test's favourite trap is to read "trainees" as the subject. | ❌ **Error** |
| B | Agreement + tense. The subject of clause 2 is "the trainer" — singular — and "has explained" (present perfect) matches. | ✅ Correct |
| C | Article + preposition. "the process of" — definite article for a specific process, and "of" correctly links "process" to "the onboarding". | ✅ Correct |
| D | Article + word order. "the onboarding in detail" — correct article, correct adverbial placement at the end of the clause. | ✅ Correct |

**The lesson:** A looks like an agreement error *about trainees*, so it reads as correct. The error is that "Each"
— the real subject — is singular. The other three chunks are clean, which confirms the single error.

**The confirmation test:** correcting chunk A to "Each of the trainees **was given**" repairs the whole sentence
without touching anything else. That is the proof you found the right chunk.

## Quick rules

- Read the whole sentence first, once.
- Test the two verb-bearing chunks first.
- Judge each chunk inside its own clause.
- If two chunks look wrong, re-read — the item has one error.
- The last confirmation: fixing your chosen chunk must make the whole sentence correct.
- Length, formality, and wordiness are not errors.

## Common traps

- **Judging a chunk in isolation** — "the trainer has explained" is fine; the chunk that is *wrong* is often the
  one where the subject is just outside the chunk.
- **Missing that a chunk cuts a subject off from its verb.** The head noun may be several words away.
- **Assuming the error is in the longest option.** Options are often scrambled in length.
- **Flagging a prepositional phrase that contains "of the"** — "the process of the onboarding" is correct.
- **Forgetting "each" and "every" take singular verbs.**

## Checklist

- [ ] I read the complete sentence before reading the options.
- [ ] I labelled the clauses and identified each clause's subject and finite verb.
- [ ] I tested agreement and tense first.
- [ ] I confirmed the other three chunks are clean.
- [ ] I confirmed that correcting my chunk repairs the whole sentence.

## Related

- [Error taxonomy](01-error-taxonomy.md)
- [The 8-step scan](../02-techniques/01-the-eight-step-scan.md)
- [The 45-second fast scan](../02-techniques/02-the-45-second-fast-scan.md)
- [Near-miss errors](../04-pitfalls/01-near-miss-errors.md)
- [Error correction topic README](../README.md)
