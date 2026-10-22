# Topic 13 — Java Question Bank

> Section 4 · Java · Topic 13 · _Estimated reading time: 135 min_

## What this topic covers

**90 questions** across the whole of Section 4, split into three banks of 30:

| Bank | Questions | Topics |
|---|---|---|
| [Part 1 — OOP & Core Java](./01-question-bank-part-1-oop-and-core.md) | Q1–Q30 | access levels, class hierarchies, `super`/`this`, interfaces, abstract classes, constructors, dynamic dispatch, `instanceof`, collections |
| [Part 2 — Exceptions, Output & Strings](./02-question-bank-part-2-exceptions-output-strings.md) | Q31–Q60 | exception hierarchy, `catch`/`finally` order, evaluation order, `continue`, ternary promotion, the string pool, `equals` vs `==`, `substring`, `split` |
| [Part 3 — Static, Arrays & Threads](./03-question-bank-part-3-static-arrays-threads.md) | Q61–Q90 | init order, compile-time constants, the `Integer` cache, overload phases, varargs, the `remove` overload, list mutability, covariance, `start()` vs `run()`, guaranteed thread statements |

Each bank ends with an **answer key table** giving the correct option and a **one-line reason** for
every question.

## Why the pre-test tests this

- Section 4 is **25 questions in ~35 minutes** — about 90 seconds each. A timed bank is the only
  way to rehearse that budget.
- The bank is built from the **question archetypes** the pre-test actually uses: a code block,
  four options, exactly one defensible answer, and one trap per question.
- Meera panics under time pressure; Rahul is fast but sloppy. The bank is designed so you can see
  which of those two problems you have — a wrong answer on an output question is a *speed* problem,
  a wrong answer on a `try`/`catch` ordering question is a *knowledge* problem.

## How to use this bank

1. **One sitting = one bank.** 30 questions, ~45 minutes, no pauses, no looking anything up.
2. **Answer on paper**, in one line each: the letter and the value. Writing the actual output
   catches errors that a guessed letter hides.
3. **Cap each question at 90 seconds.** If you blow the cap, mark it and move on.
4. **Score honestly** using the answer key at the bottom of each bank.
5. **Re-do only the ones you got wrong**, without looking at the key, 24 hours later.

### Scoring yourself

| Score on one bank | What it means | What to do |
|---|---|---|
| 27–30 | Exam-ready on this block | Move on; do not re-read |
| 21–26 | Concepts are fine, speed is short | Redo with a stricter 60-second cap |
| 15–20 | A specific topic is missing | Re-read that topic's `04-pitfalls` file, then retry |
| Below 15 | The foundations are missing | Re-read the topic's `01-concepts` file first |

**Target: 24/30 on a fresh bank, 27/30 on a retake.**

## What each question tests

| Archetype | How to spot it | Where to revise |
|---|---|---|
| "Which is legal / does not compile?" | the stem has two nearly identical snippets | [04-Interfaces-Abstract-Inner-Classes](../04-Interfaces-Abstract-Inner-Classes/) |
| "What is printed?" | a code block ending in a `println` | [08-Output-Prediction-Patterns](../08-Output-Prediction-Patterns/) |
| "Which is thread-safe / what is guaranteed?" | the stem mentions two threads | [12-Threads-Basic](../12-Threads-Basic/) |
| "What does this list method do?" | a `List` operation | [06-Collections-Framework](../06-Collections-Framework/) |
| "What is the value / result?" | an expression, no side effects | [10-Static-Final-Varargs-Operators](../10-Static-Final-Varargs-Operators/) |

## Common mistakes to avoid

- ❌ Answering a thread output question with a fixed order — the only defensible option is the
  one that states what is **guaranteed**.
- ❌ Reading a whole code block before starting. Read the **last line** first.
- ❌ Guessing on the "does it compile?" questions — they are decided by two rules, not by intuition.
- ❌ Skipping the `finally` question because the `try` looks harmless. `finally` changes answers.
- ❌ Treating `==` and `equals` as interchangeable.

## The full Section 4 checklist

Before the pre-test, tick every line:

- [ ] I can write the `Throwable` → `Exception` → `RuntimeException` tree from memory.
- [ ] I know the order of `catch`, `finally`, and `return`.
- [ ] I can evaluate `x++ + ++x` and `a[i++] = i++` without thinking.
- [ ] I know the overload phases and that varargs is last.
- [ ] I know the `Integer` cache range (−128..127).
- [ ] I know `remove(int)` vs `remove(Object)`.
- [ ] I know `Arrays.asList` vs `List.of` vs `new ArrayList<>(...)`.
- [ ] I know `start()` vs `run()`, and that thread order is never guaranteed.
- [ ] I know `sleep()` keeps the lock and `wait()` releases it.
- [ ] I know `volatile` is not atomic.

## Related

- [01 — OOP Principles](../01-OOP-Principles/)
- [02 — Classes, Objects & Constructors](../02-Classes-Objects-Constructors/)
- [03 — Inheritance & Polymorphism](../03-Inheritance-Polymorphism/)
- [04 — Interfaces, Abstract & Inner Classes](../04-Interfaces-Abstract-Inner-Classes/)
- [05 — Packages & Access Modifiers](../05-Packages-Access-Modifiers/)
- [06 — Collections Framework](../06-Collections-Framework/)
- [07 — Exceptions & Error Handling](../07-Exceptions-Error-Handling/)
- [08 — Output Prediction Patterns](../08-Output-Prediction-Patterns/)
- [09 — Strings, Immutability, equals & hashCode](../09-Strings-Immutable-Equals-Hashcode/)
- [10 — Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/)
- [11 — Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/)
- [12 — Threads Basics](../12-Threads-Basic/)
