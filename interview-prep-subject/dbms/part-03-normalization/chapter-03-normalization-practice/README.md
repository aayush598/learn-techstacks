# Chapter: Normalization Practice

## What you'll learn
- **Normalization interview questions & problems**: 15+ worked problems — classify into 1NF/2NF/3NF/BCNF, find candidate keys, decompose correctly, test lossless-join and dependency preservation, and argue design decisions under interview conditions.

## Prerequisites (linked)
- [Chapter 01 (Functional Dependencies)](../chapter-01-functional-dependencies/README.md) and [Chapter 02 (Normal Forms)](../chapter-02-normal-forms/README.md) — this chapter is pure application of those.
- Feeds into [Part 04 (Indexing & File Organization)](../../part-04-indexing-and-file-organization/README.md) — denormalization/design decisions from these problems pair with index design.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Normalization Interview Questions and Problems](section-01-normalization-interview-questions-and-problems.md) | 15+ classified/decomposed problems with step-by-step reasoning |

## One-paragraph narrative connecting all sections
All of Part 03's theory — FDs, closure, candidate keys, 2NF/3NF/BCNF/4NF/5NF, lossless decomposition, denormalization — collapses into one skill: **given a relation and its FDs, produce a clean design and defend it**. This chapter drills exactly that. Each problem states the relation + FD set, then walks through candidate-key finding (closure), highest-normal-form classification, decomposition with the lossless/dependency-preservation tests, and a short "what would you do in production" discussion. By the end, classification and decomposition are reflexes, not slow reasoning.

## Common interview trap in this chapter
Practicing only "is this in 3NF?" questions — real interviews ask *design* questions ("design a schema for X and justify it") and *repair* questions ("this schema is redundant — what's wrong, what would you change?"). This chapter's problems deliberately mix classification with design/repair reasoning so you practice arguing, not just labeling.

## Checklist before moving on
- [ ] I can solve any classification problem in under 2 minutes and explain each step.
- [ ] I can decompose to BCNF/3NF with a reason for choosing one over the other.
- [ ] I can prove lossless join and dependency preservation on my decomposition.
- [ ] I can defend a denormalization decision with a concrete workload argument.
- [ ] I can repair a given bad schema (redundant/insertion-anomalous) out loud.
- [ ] I've re-solved every problem in this chapter twice, from memory.
