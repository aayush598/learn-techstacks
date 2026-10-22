# Topic 10 — Static, Final, Varargs & Operators

> Section 4 · Java · Topic 10 · _Estimated reading time: 18 min_

## What this topic covers

Four small Java mechanics that get bundled into one exam topic because each one generates the same
kind of question — **"what exactly happens here?"**:

1. `static` — one copy per class, and **when** class initialisation runs.
2. `final` — what cannot change, and the three conditions of a **compile-time constant**.
3. Varargs — sugar for an array parameter, and the **last** overload phase.
4. Operators — the precedence ladder, integer division and modulo signs, and the `Math` class.

## Why the pre-test tests this

- These questions are **deterministic**: exactly one option is right, and the reasoning is 1–3
  lines. Once you own the tables, they are free marks.
- They combine: a `static final` constant is also a compile-time constant, which is also inlined,
  which is also why `"x" + CONSTANT` is pooled.
- The distractors are all *plausible* — a static block "seeing the final value", boxing "beating"
  widening, `round(-2.5)` being `-3`. Learning the distractors is what earns the mark.

## What you must be able to do

| Skill | Where it is drilled |
|---|---|
| Order static field initialisers, static blocks, instance initialisers, and constructors | [01-concepts/01-static-and-final.md](01-concepts/01-static-and-final.md) |
| Decide if a variable is a compile-time constant | [01-concepts/01-static-and-final.md](01-concepts/01-static-and-final.md) |
| Apply varargs rules and overload phases | [01-concepts/02-varargs-and-wrapper-types.md](01-concepts/02-varargs-and-wrapper-types.md) |
| Reason about `Integer` cache and autoboxing traps | [01-concepts/02-varargs-and-wrapper-types.md](01-concepts/02-varargs-and-wrapper-types.md) |
| Evaluate operator precedence, division, modulo, and `Math` | [01-concepts/03-operator-precedence-and-arithmetic.md](01-concepts/03-operator-precedence-and-arithmetic.md) |
| Look up the answer in a table under time pressure | [02-techniques/01-decision-tables-for-overloads-and-operators.md](02-techniques/01-decision-tables-for-overloads-and-operators.md) |

## Folder map

| Folder | Contents | Read when |
|---|---|---|
| [01-concepts](01-concepts/README.md) | 3 files: static & final, varargs & wrappers, operators & arithmetic | First pass |
| [02-techniques](02-techniques/README.md) | 1 file: the 6 decision tables + the 60-second procedure | Before the exam |
| [03-worked-examples](03-worked-examples/README.md) | 1 file: 10 fully solved questions | Practice |
| [04-pitfalls](04-pitfalls/README.md) | 1 file: 12 traps with guards | Last night |
| [05-reference](05-reference/README.md) | 1 file: the printable one-pager | Exam morning |

## The 10-second answer

| Question shape | The rule |
|---|---|
| "What is printed?" with a `static` block | Superclass first, then **textual order**, at first use |
| "Which is a constant?" | `final` + primitive/`String` + constant expression |
| "Which overload?" | exact → widening → boxing → varargs |
| "What is `a % b` for negatives?" | Sign follows the **dividend** |
| "What is `a / b` for negatives?" | Truncates toward **zero** |
| "What is `Math.round(-2.5)`?" | `-2` — half **up** |

## Common mistakes to avoid

- ❌ Assuming static blocks run when the program starts.
- ❌ Assuming a static block sees the *final* value of a field.
- ❌ Assuming boxing happens before widening.
- ❌ Assuming `Integer` values are always cached.
- ❌ Assuming `final` makes an object's contents immutable.
- ❌ Assuming `Math.round` rounds half to even.

## Related topics

- [07 — Exceptions & Error Handling](../07-Exceptions-Error-Handling/README.md)
- [08 — Output Prediction Patterns](../08-Output-Prediction-Patterns/README.md)
- [09 — Strings, Immutability, equals & hashCode](../09-Strings-Immutable-Equals-Hashcode/README.md)
- [11 — Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/README.md)
- [12 — Threads Basics](../12-Threads-Basic/README.md)
- [13 — Java Question Bank](../13-Question-Bank/README.md)
