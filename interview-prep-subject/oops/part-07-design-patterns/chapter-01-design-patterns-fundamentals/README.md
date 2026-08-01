# Chapter: Design Patterns Fundamentals

## What you'll learn
- The precise definition of a design pattern and its three-part structure **Context → Problem → Solution**.
- Why patterns exist: they capture *proven* solutions to recurring design problems, compress decades of collective experience, and create a shared vocabulary between engineers.
- The full GoF catalog and its categorization: **creational (5)** / **structural (7)** / **behavioral (11)** patterns, plus the class-vs-object sub-split.
- The difference between a pattern, an algorithm, a framework, and an anti-pattern — and why misuse of a pattern is itself a design smell.

## Prerequisites (linked)
- [Part 06 — SOLID and Design Principles](../../part-06-solid-and-design-principles/README.md) — patterns are concrete mechanisms that implement SOLID laws.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md) — most patterns depend on interfaces and dynamic dispatch.
- [Part 02 — Encapsulation and Abstraction](../../part-02-encapsulation-and-abstraction/README.md) — every pattern is a study in what to encapsulate and hide.

## Sections (linked table)
1. [Section 01: What Are Design Patterns and Why They Exist](section-01-what-are-design-patterns-and-why-they-exist.md)
2. [Section 02: GoF Patterns Overview and Categorization](section-02-gof-patterns-overview-and-categorization.md)

## One-paragraph narrative connecting all sections
Section 01 defines what a pattern *is* — a named, reusable, documented solution to a recurring problem, always expressible as context/problem/solution/consequences — and why they exist (consistency, vocabulary, and 30+ years of battle-tested design instead of ad-hoc reinvention). Section 02 then hands you the complete 23-pattern map and the three-way taxonomy that lets you *navigate* the catalog: creational patterns answer "how is an object born?", structural patterns answer "how are objects composed into larger structures?", behavioral patterns answer "how do objects coordinate responsibility and communication?". Read them together so that "which family does this pattern belong to?" is instantly answerable for all 23.

## Common interview trap in this chapter
Confusing **intent with implementation**: e.g., describing the singleton as "a class with a private constructor and a static method" instead of its actual intent "guarantee a class has exactly one instance and provide a global point of access." Interviewers punish this immediately. Second trap: treating patterns as a checklist to force-fit into every design — the mature answer is that patterns are *tools*, chosen when the problem matches, and sometimes the right answer is "no pattern here."

## Checklist before moving on
- [ ] I can define a design pattern and name context/problem/solution/consequences.
- [ ] I can place all 23 GoF patterns in the correct family (5/7/11).
- [ ] I can explain what problem each family solves (creation / composition / communication).
- [ ] I can state the difference between pattern, algorithm, framework, and anti-pattern.
- [ ] I can answer "why didn't you just write a helper function?" for any pattern I discuss.
