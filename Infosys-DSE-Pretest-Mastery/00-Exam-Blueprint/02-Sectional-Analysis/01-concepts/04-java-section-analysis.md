# Java Section Analysis (25 Q)

> Section 00 · Exam Blueprint · Sectional Analysis · _Estimated reading time: 18 min_
> **Prerequisite:** [../README.md](../README.md)

## In one sentence
**Java is 25 questions — about 41.7% of the paper — so even 15/25 correct makes the pass threshold almost self-funding.**

## Why the pre-test tests this
- **Largest pool:** the Java section dominates the score more than any other.
- **Code reading, not coding:** the reported emphasis is output prediction, compile/execute identification, and concept recall — not writing programs.
- **Recurring topics:** OOPs, interfaces and inner classes, packages and access modifiers, the collections framework, and errors/exceptions.
- **Supports Rahul** (strong Java) to bank marks, and warns weak-Java candidates that 25 questions is a lot of points to leave behind.

## Core concept

### The sub-topics and their cost
| Topic | Typical share | Cost per mark | Notes |
|-------|---------------|---------------|-------|
| OOPs | ~4-5 Q | Low-medium | Definitions + behaviour |
| Interfaces & inner classes | ~3-4 Q | Medium-high | Scoping rules |
| Packages & access modifiers | ~2-3 Q | Medium | Visibility |
| Collections framework | ~3-4 Q | Medium | List/Set/Map behaviour |
| Errors & exceptions | ~3-4 Q | Medium | Hierarchy, try/catch |
| Pseudo-code output prediction | ~4-5 Q | Medium | Trace loops and strings |
| Compile/execute identification | ~3-4 Q | Medium | Spot compile errors |

### Difficulty distribution
| Band | Share | Notes |
|------|-------|-------|
| Easy | ~8-10 Q | Definitions, common output |
| Medium | ~10-12 Q | Collections, exceptions, tracing |
| Hard | ~3-5 Q | Nested / inner-class scoping, tricky output |

### Where the marks are cheapest
1. **Definitions** (OOPs concepts, exception hierarchy).
2. **Common collections behaviour:** ArrayList vs HashSet vs HashMap.
3. **Recognised output patterns** you have memorised from practice.

### Collections quick table (Java 8 assumed)
| Structure | Ordered? | Duplicates? | Key access |
|-----------|----------|-------------|------------|
| ArrayList | Yes (insertion) | Yes | Index |
| LinkedList | Yes | Yes | Index / ends |
| HashSet | No | No | — |
| LinkedHashSet | Yes (insertion) | No | — |
| TreeSet | Sorted | No | — |
| HashMap | No | Values yes | Key |
| TreeMap | Sorted by key | Values yes | Key |

### Access modifiers quick table
| Modifier | Class | Package | Subclass | World |
|----------|-------|---------|----------|-------|
| private | ✅ | ❌ | ❌ | ❌ |
| (default) | ✅ | ✅ | ❌ | ❌ |
| protected | ✅ | ✅ | ✅ | ❌ |
| public | ✅ | ✅ | ✅ | ✅ |

### How the weight maps to score
25 questions = 41.7% of the paper. Target **15-16 correct**. That alone is roughly 26% of the pass threshold — a strong reason to protect this section's time budget.

## Worked example
**Pseudo-code output prediction:**
```java
int x = 5;
System.out.println(x++ + ++x);
```

Trace with a variable table:

| Step | Expression | Value used | x after |
|------|------------|-----------|---------|
| 1 | `x++` | 5 (post-increment) | 6 |
| 2 | `++x` | 7 (pre-increment) | 7 |
| 3 | sum | 5 + 7 = 12 | 7 |

**Output: 12.**

**Distractors:**
- "11" ignores the difference between post- and pre-increment (5 + 6).
- "13" double-counts an increment.
- "5" prints only the first operand.

### Compile/execute identification
Look for these first, in order:
1. Missing semicolons or braces.
2. Type mismatches (assigning a `double` to an `int` without a cast).
3. Access violations (calling a `private` member from outside).
4. Unreachable or missing returns.
5. Generics violations.

If any of these appear, the code **does not compile** — "what does it print" is a trap.

## Quick rules
- **Assume Java 8** unless the question states otherwise.
- **Trace with a variable table**, not in your head.
- **Check compile errors first:** semicolons, types, access.
- **String is immutable; `equals` vs `==` differ.**
- **ArrayList ordered, HashSet not; Map is key-value.**
- **Checked vs unchecked exceptions matter.**
- **Target 15-16 correct.**

## Common traps
- **Skipping the trace and guessing output.**
- **Assuming code compiles when generics or access modifiers forbid it.**
- **Confusing `==` with `.equals()`** for reference types.
- **Ignoring integer division and overflow.**
- **Over-running time on one inner-class question** — this is the most common Java trap.

## Checklist
- [ ] You know all seven Java sub-topics and their approximate shares.
- [ ] You trace output with a variable table.
- [ ] You check the five compile-error patterns first.
- [ ] You can recite the collections and access-modifier tables.
- [ ] Your Java target is 15-16 correct.
- [ ] You protect Java's time budget.

## Related
- [03-dbms-sql-section-analysis.md](03-dbms-sql-section-analysis.md)
- [05-score-model-building-39.md](05-score-model-building-39.md)
- [../02-techniques/01-cheapest-marks-first.md](../02-techniques/01-cheapest-marks-first.md)
- [../04-pitfalls/01-difficulty-misjudgement.md](../04-pitfalls/01-difficulty-misjudgement.md)
