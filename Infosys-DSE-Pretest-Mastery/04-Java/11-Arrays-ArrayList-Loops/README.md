# Topic 11 — Arrays, ArrayList & Loops

> Section 4 · Java · Topic 11 · _Estimated reading time: 18 min_

## What this topic covers

The three things you touch in almost every Java program:

1. **Arrays** — fixed length, one element type, and the `java.util.Arrays` toolbox.
2. **ArrayList** — a growable list of objects, and the collection-choice rules.
3. **Loops** — the five forms, `break`/`continue`/labels, and the fail-fast rule for for-each.

## Why the pre-test tests this

- These questions are extremely common in Section 4 and every one of them has **exactly one**
  defensible answer.
- The distractors are all one-word errors: index vs value, fixed-size vs immutable, `continue` vs
  `break`, field vs method.
- The output questions are short, so you can drill 30 of them in one sitting.

## What you must be able to do

| Skill | Where it is drilled |
|---|---|
| Use the `Arrays` methods without looking them up | [01-concepts/01-arrays-and-arraylist.md](01-concepts/01-arrays-and-arraylist.md) |
| Explain covariance and `ArrayStoreException` | [01-concepts/01-arrays-and-arraylist.md](01-concepts/01-arrays-and-arraylist.md) |
| Pick between `remove(int)` and `remove(Object)` | [01-concepts/01-arrays-and-arraylist.md](01-concepts/01-arrays-and-arraylist.md) |
| Trace a loop's output, including `continue` and labels | [01-concepts/02-loops-and-iteration.md](01-concepts/02-loops-and-iteration.md) |
| Know when a for-each loop throws `ConcurrentModificationException` | [01-concepts/02-loops-and-iteration.md](01-concepts/02-loops-and-iteration.md) |
| Choose a container and a loop under time pressure | [02-techniques/01-choosing-the-right-collection-and-loop.md](02-techniques/01-choosing-the-right-collection-and-loop.md) |

## Folder map

| Folder | Contents | Read when |
|---|---|---|
| [01-concepts](01-concepts/README.md) | 2 files: arrays & ArrayList, loops & iteration | First pass |
| [02-techniques](02-techniques/README.md) | 1 file: 5 decision tables + the 60-second procedure | Before the exam |
| [03-worked-examples](03-worked-examples/README.md) | 1 file: 10 fully solved questions | Practice |
| [04-pitfalls](04-pitfalls/README.md) | 1 file: 12 traps with guards | Last night |
| [05-reference](05-reference/README.md) | 1 file: the printable one-pager | Exam morning |

## The 10-second answer

| Question shape | The rule |
|---|---|
| "What does `arr` print?" | `[I@hash` — use `Arrays.toString` |
| "What does `list.remove(1)` do?" | Removes **index** 1 |
| "Can I `add` to this list?" | `Arrays.asList` → no; `List.of` → no; `new ArrayList<>(...)` → yes |
| "Does `continue` skip `i++`?" | **No** |
| "How many times does this loop run?" | `do-while` runs **at least once** |
| "Can I remove from a list inside a for-each?" | No — `ConcurrentModificationException` |

## Common mistakes to avoid

- ❌ Calling `arr.length()` — `length` is a field.
- ❌ Assuming `list.remove(1)` removes the value `1`.
- ❌ Assuming `Arrays.asList` returns a mutable list.
- ❌ Assuming `String[]` cannot be assigned to `Object[]`.
- ❌ Assuming `continue` skips the `for` update expression.
- ❌ Assuming `Arrays.sort` on strings sorts numerically.

## Related topics

- [07 — Exceptions & Error Handling](../07-Exceptions-Error-Handling/README.md)
- [08 — Output Prediction Patterns](../08-Output-Prediction-Patterns/README.md)
- [09 — Strings, Immutability, equals & hashCode](../09-Strings-Immutable-Equals-Hashcode/README.md)
- [10 — Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/README.md)
- [12 — Threads Basics](../12-Threads-Basic/README.md)
- [13 — Java Question Bank](../13-Question-Bank/README.md)
