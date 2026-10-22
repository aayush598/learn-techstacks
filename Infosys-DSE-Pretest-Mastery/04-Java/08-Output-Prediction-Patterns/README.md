# Output Prediction Patterns — Topic Guide

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 150 min for the full topic_

## What the pre-test asks in this topic

This is the **single highest-yield folder in Section 4**. The Java section is 25 questions in ~35
minutes, and the reported archetypes include:

- **Pseudo-code output prediction** — "what does this print?"
- **"Does this code compile / does it run?"** — identification questions with 4 options.
- **Evaluation order** — which statement runs first, what value ends up in a variable.

The options are always strings, so the exam is testing one thing: **can you simulate Java's
execution rules correctly, in 90 seconds.**

Nothing in this topic requires API knowledge. It requires a *model*.

## Learning objectives

After this topic you should be able to:

- Run the **evaluation-order model**: static init → instance init → constructor → method body, with
  `super()` first.
- Resolve an overloaded call using the 3-phase rule: **exact/widening → boxing → varargs**.
- Predict short-circuit, ternary, `++`/`--`, `+=`, and compound-assignment narrowing results without
  executing anything.
- Explain why `Integer` values in **−128..127** are cached and what that means for `==`.
- Write the exact printed output of a nested-loop/label/array snippet, spaces included.
- Decide **compile error vs runtime error vs normal output** using the compile-error catalogue.
- Apply a **10-second triage** to any output question: find the "interesting" line and start there.
- Say explicitly when an output is **not deterministic** (threads) and pick the guaranteed option.

## File index

| File | What it gives you |
|---|---|
| [01-concepts/01-the-evaluation-order-model.md](01-concepts/01-the-evaluation-order-model.md) | The master model: class loading, static vs instance init, super() first, method resolution, short-circuit, `++`/`+=`, boxing, `==` vs `equals`, switch fall-through, loops, labels, `instanceof`, ternary promotion, char arithmetic |
| [01-concepts/02-compile-vs-run-taxonomy.md](01-concepts/02-compile-vs-run-taxonomy.md) | The three-way split: compile error / runtime exception / normal output, and how to tell them apart in 10 seconds |
| [02-techniques/01-ten-second-triage.md](02-techniques/01-ten-second-triage.md) | The 10-second triage checklist, the "interesting line" method, common question shapes and their fastest attack |
| [02-techniques/02-method-resolution-and-short-circuit.md](02-techniques/02-method-resolution-and-short-circuit.md) | Overload resolution in 3 phases, varargs rules, short-circuit truth tables, `++` semantics, compound assignment cast rules |
| [03-worked-examples/01-solved-output-set-a.md](03-worked-examples/01-solved-output-set-a.md) | 12 solved output questions with exact output strings: init order, overloads, short-circuit, `++`, boxing/cache, interning, switch, ternary/char, arrays, labels, `instanceof`, compound assignment |
| [03-worked-examples/02-solved-output-set-b.md](03-worked-examples/02-solved-output-set-b.md) | 12 more solved questions: static init across classes, wrapper `==`, `final` folding, nested arrays, string concat traps, `char` arithmetic, for vs for-each, break/continue, ternary typing, `Integer` cache edges, field hiding, `long` division |
| [04-pitfalls/01-output-traps.md](04-pitfalls/01-output-traps.md) | 12 named output traps with the wrong output and the right output |
| [04-pitfalls/02-compile-error-traps.md](04-pitfalls/02-compile-error-traps.md) | The compile-error traps: which "looks fine but won't compile" snippets fool people |
| [05-reference/01-output-rules-one-pager.md](05-reference/01-output-rules-one-pager.md) | The printable rules sheet: precedence, the 10 output rules, the 60-second budget |
| [05-reference/02-compile-error-catalogue.md](05-reference/02-compile-error-catalogue.md) | 30+ compile errors with the actual javac message and a 5-line repro |

## Quick procedure — the 10-second triage

1. **Find the interesting line.** The output question is about *one* construct. Scan for: `++`,
   `+=`, `==`, a `switch`, a `break`, a `catch`, a `static` block, an overloaded call.
2. **Name the construct** (one of 12 in the model). Each construct has exactly one rule set.
3. **Apply only that rule.** Do not simulate the whole program.
4. **Write the output as a quoted string**, spaces included.
5. **Compare to the options.** If no option matches your string, re-check the construct — do not
   pick the "closest".

## Key takeaways

- ✅ **Everything is evaluation order.** Class loading → static init → instance init → constructor
  body → method body.
- ✅ **Overload resolution is 3 phases**: strict (exact + widening) beats boxing, boxing beats
  varargs. Varargs is the *last* resort, not the first.
- ✅ **`&&`/`||`/ternary evaluate one branch only.** That is the single most common output difference.
- ✅ **`i++` yields the old value; `++i` yields the new one.** In `a + b`, `a` is evaluated first.
- ✅ **`x += y` is `x = (T)(x + y)`** where `T` is the type of `x`. `x = x + y` is not.
- ✅ **`Integer` −128..127 is cached**, so `==` is true in that range and false outside it.
- ✅ **`switch` falls through** unless each case ends with `break`/`return`/`throw`.
- ✅ **A compile error produces no output at all.** If an option shows printed text for code that
  does not compile, that option is wrong.
- ⚠️ **Meera's warning:** she tries to execute the whole program in her head. You do not. You find
  the one interesting line and apply one rule.

## Related

- [Exceptions & Error Handling](../07-Exceptions-Error-Handling/) — `try/catch/finally` output
- [Strings, Immutability, equals & hashCode](../09-Strings-Immutable-Equals-Hashcode/) — interning,
  `==` vs `equals`, and the `String` pool
- [Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/) — operator precedence
  and `static` initialisation
- [Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/) — array reference semantics and loop traps
- [Threads (Basic)](../12-Threads-Basic/) — the one topic where output is **not** deterministic
- [Java question bank](../13-Question-Bank/) — 90+ questions across every Java archetype
- [Master README](../../README.md)
