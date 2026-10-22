# Strings, Immutability, equals & hashCode — Topic Guide

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 110 min for the full topic_

## What the pre-test asks in this topic

The Java section regularly asks a small set of string questions, and they are all variations of
**one idea: a `String` is an immutable value, not an object you can change.**

| Question archetype | Typical options |
|---|---|
| `==` vs `equals` | `true` / `false` / "compile error" / "runtime error" |
| String pool / interning | `true` / `false` |
| `hashCode` contract | "equal objects have equal hashcodes" / "unequal objects have different hashcodes" / ... |
| `StringBuilder` vs `StringBuffer` | thread-safe / not thread-safe / final / ... |
| `final String` and constant folding | "the value is computed at compile time" / "at runtime" |
| Which method does what | `substring` / `replace` / `replaceAll` / `split` / `trim` / `strip` |
| `null` concatenation | "prints null" / "throws NPE" |

None of these need API breadth. They need **one mental model** and a **decision table**.

## Learning objectives

After this topic you should be able to:

- State why `String` is immutable and name the three consequences (safe to share, safe as a map key,
  thread-safe without synchronisation).
- Explain the **string pool** and predict `==` results for literals, `new String(...)`, concatenation
  of literals, and `intern()`.
- State the `equals`/`hashCode` contract in one line and give a counterexample for each half.
- Choose between `StringBuilder` and `StringBuffer` without hesitating.
- Say when `final String` is folded at compile time and when it is not.
- Pick the right method for a job from the API decision table: `replace` vs `replaceAll`,
  `matches` vs `find`, `trim` vs `strip`, `split` vs `substring`, `equals` vs `compareTo`.
- Avoid the `null` concatenation and `toString` traps.

## File index

| File | What it gives you |
|---|---|
| [01-concepts/01-string-immutability-and-pool.md](01-concepts/01-string-immutability-and-pool.md) | Immutability and its consequences, the string pool, `intern()`, constant folding, `StringBuilder` vs `StringBuffer`, `substring` internals (Java 6 vs 7+) |
| [01-concepts/02-equals-hashcode-and-comparison.md](01-concepts/02-equals-hashcode-and-comparison.md) | The `equals`/`hashCode` contract, `==` vs `equals` vs `compareTo` vs `compareToIgnoreCase` vs `equalsIgnoreCase`, `hashCode` collisions, `null` behaviour |
| [02-techniques/01-string-api-decision-table.md](02-techniques/01-string-api-decision-table.md) | A method-by-method decision table, the `split` regex rules, the `null`-safety table, the 60-second procedure |
| [03-worked-examples/01-solved-string-set.md](03-worked-examples/01-solved-string-set.md) | 9 fully solved questions with exact output strings and distractor breakdowns |
| [04-pitfalls/01-string-traps.md](04-pitfalls/01-string-traps.md) | 10 named string traps with the wrong answer and the right answer |
| [05-reference/01-string-one-pager.md](05-reference/01-string-one-pager.md) | The printable sheet: pool rules, contract, method cheat table, 60-second budget |

## Quick procedure — answer a string question in 60 seconds

1. **Is the operand a `String` literal, a `new String`, or a computed value?**
   - literal → it lives in the pool
   - `new String(...)` → it does not
   - computed (`+` with a variable, `substring`, `concat`) → runtime object, not pooled
2. **Is the comparison `==` or `equals`?** `==` compares references; `equals` compares characters.
3. **For `equals`: does either side have a `null`?** `null.equals(...)` → `NullPointerException`.
4. **For a "which method" question**: look up the decision table, not the whole API.
5. **For `hashCode`**: apply the contract — equal → equal hash; unequal → *may* share a hash.

## Key takeaways

- ✅ **`String` is immutable.** Every "modifying" method returns a **new** `String`.
- ✅ **String literals are interned.** `"a" == "a"` → `true`. `new String("a") == "a"` → `false`.
- ✅ **Only compile-time constant expressions are folded and pooled.** `final String s = "x";` is a
  constant; `final String s = build();` is not.
- ✅ **`equals` → content. `==` → reference.** `compareTo` → lexicographic ordering (not a boolean).
- ✅ **The contract: `a.equals(b)` ⇒ `a.hashCode() == b.hashCode()`.** The reverse is **not** true.
- ✅ **`StringBuilder` is not thread-safe; `StringBuffer` is.** Both are mutable.
- ✅ **`replace` is literal; `replaceAll` is regex.** `matches` must match the **whole** string;
  `find` matches anywhere.
- ⚠️ **Meera's warning:** she picks `replaceAll` when she means `replace` and loses a mark on a
  question she could have answered in 20 seconds.

## Related

- [Output Prediction Patterns](../08-Output-Prediction-Patterns/) — `==` vs `equals` shows up in
  output questions more than anywhere else
- [Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/) — `final` and constant
  folding
- [Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/) — `char[]` vs `String`, `List` of
  strings
- [Java question bank](../13-Question-Bank/) — 90+ questions across every Java archetype
- [Master README](../../README.md)
