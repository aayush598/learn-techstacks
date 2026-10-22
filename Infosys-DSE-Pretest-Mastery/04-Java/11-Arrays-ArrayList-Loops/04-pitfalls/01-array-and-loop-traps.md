# Arrays, ArrayList & Loops — Traps

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 12 min_
> **Prerequisite:** [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)

## In one sentence

12 traps, each written as **the wrong answer you will pick → the right answer → the one-line
guard**.

## Why the pre-test tests this

The Java collection questions are unusually generous with near-miss distractors: `remove(1)` vs
`remove(Integer.valueOf(1))`, `Arrays.asList` vs `new ArrayList<>(...)`, `continue` vs `break`. Each
trap below corresponds to a real distractor.

## Core concept

### The 12 traps

| # | Trap | The wrong answer you pick | The right answer | The one-line guard |
|---|---|---|---|---|
| 1 | `arr.length()` | compiles | `arr.length` is a **field** | "No parentheses" |
| 2 | A raw array prints its contents | `[1, 2, 3]` | `[I@1b6d3586` | "Use `Arrays.toString`" |
| 3 | `list.remove(1)` removes the value `1` | `[2, 3]` | It removes **index 1** | "`remove(int)` = index" |
| 4 | `Arrays.asList` supports `add` | it appends | `UnsupportedOperationException` | "Fixed size" |
| 5 | `List.of` supports `set` | it replaces | `UnsupportedOperationException` | "Immutable" |
| 6 | `String[]` cannot be an `Object[]` | compile error | It compiles — arrays are covariant | "Covariant, then `ArrayStoreException`" |
| 7 | Removing from a list in a for-each is safe | the loop completes | `ConcurrentModificationException` | "Fail-fast iterator" |
| 8 | `continue` skips `i++` | infinite loop | `i++` still runs | "Update still applies" |
| 9 | `do-while` with a false condition runs 0 times | 0 iterations | **1** iteration | "Body first" |
| 10 | `break` inside a nested loop exits both | exits both | exits only the **innermost** | "Use a label" |
| 11 | `Arrays.sort` on `String[]` is numeric | `["2", "10"]` | `["10", "2"]` | "Lexicographic" |
| 12 | `list.toArray()` returns a `String[]` | compiles | It returns `Object[]` | "Use `toArray(new T[0])`" |

### The `remove` trap in full

This is the single most-asked trap in this topic, so learn all four rows:

| List content | Call | Overload chosen | Result |
|---|---|---|---|
| `[10, 20, 30]` | `remove(0)` | `remove(int)` | `[20, 30]` |
| `[10, 20, 30]` | `remove(1)` | `remove(int)` | `[10, 30]` |
| `[10, 20, 30]` | `remove(Integer.valueOf(10))` | `remove(Object)` | `[20, 30]` |
| `[10, 20, 30]` | `remove(Integer.valueOf(1))` | `remove(Object)` | unchanged |

**The rule in one line:** the literal `int` matches `remove(int)` exactly, so it is a **positional**
remove. To remove by **value**, pass an `Integer` object.

### The three list-creation flavours

| Flavour | `add` | `remove` | `set` | Fixed size? |
|---|---|---|---|---|
| `new ArrayList<>(Arrays.asList(a))` | ✅ | ✅ | ✅ | no |
| `Arrays.asList(a)` | ❌ UOE | ❌ UOE | ✅ | yes |
| `List.of(a)` | ❌ UOE | ❌ UOE | ❌ | yes |

A common exam form: "Which operation throws `UnsupportedOperationException`?" — the answer is `add`
on an `Arrays.asList` list, or **any** mutation on a `List.of` list.

### The fail-fast trap

```java
for (String s : list) {
    list.remove(s);       // 💥 CME on the second next()
}
```

The for-each loop uses an `Iterator` that checks the collection's **modification count** before
each step. Any structural change (add/remove) bumps that count and the check fails.

**Legal alternatives:**

```java
list.removeIf(s -> s.length() > 3);              // Java 8+
Iterator<String> it = list.iterator();
while (it.hasNext()) { if (bad(it.next())) it.remove(); }
```

Note the asymmetry: **modifying an `int[]` inside a for-each is legal** — arrays have no
fail-fast check.

### The loop-exit trap

| Statement | Where it goes |
|---|---|
| `break;` | after the **innermost** loop |
| `break outer;` | after the labelled loop |
| `continue;` | the next iteration of the innermost loop |
| `continue outer;` | the next iteration of the labelled loop |

### The array-shape trap

| Shape | Meaning | Trap |
|---|---|---|
| `new int[2][3]` | 2 rows, 3 columns each | fully initialised |
| `new int[2][]` | 2 rows, each `null` | `a[0][0] = 1` → NPE |
| `new int[2][3][4]` | 2 × 3 × 4 | |

## Worked example

**The trap in action.** A question says:

> ```java
> List<String> list = Arrays.asList("a", "b", "c");
> list.set(0, "z");
> list.remove("a");
> System.out.println(list);
> ```
> Options: `[z, b, c]`, `UnsupportedOperationException`, `[a, b, c]`, `[z, c]`.

**The trap:** you assume `remove("a")` works because `set` worked, so you pick `[z, b, c]`.

**The right reasoning:**

| Call | Result |
|---|---|
| `Arrays.asList("a", "b", "c")` | a **fixed-size** list backed by a `String[]` |
| `list.set(0, "z")` | **legal** — replacing an element does not change the size → `["z", "b", "c"]` |
| `list.remove("a")` | **throws** `UnsupportedOperationException` — removing would change the size |

**Answer: `UnsupportedOperationException`.**

Note the trap is asymmetric on purpose: `set` works but `remove` does not, because only `remove`
changes the size.

## Quick rules

- `arr.length` is a field; `Arrays.toString(a)` prints contents.
- `remove(int)` → index; `remove(Object)` → value.
- `Arrays.asList` → fixed size, `set` works, `add`/`remove` throw.
- `List.of` → fully immutable.
- Arrays are covariant → `ArrayStoreException` on a bad store.
- Structural modification during a for-each → `ConcurrentModificationException`.
- `continue` in a `for` loop still runs the update expression.
- `do-while` runs at least once.
- `break` = innermost loop only.

## Common traps

See the 12-row table above — each row is a one-line guard you can recite.

## Checklist

- [ ] I can recite the `remove` overload table.
- [ ] I know which list creation flavour throws on which mutation.
- [ ] I know why `String[]` is an `Object[]`.
- [ ] I know the legal way to remove during iteration.
- [ ] I know `continue` still runs the update expression.
- [ ] I know `Arrays.sort` on strings is lexicographic.

## Related

- [Arrays and ArrayList](../01-concepts/01-arrays-and-arraylist.md)
- [Loops and iteration](../01-concepts/02-loops-and-iteration.md)
- [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)
- [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)
- [Arrays and loops one-pager](../05-reference/01-arrays-loops-one-pager.md)
- [Topic overview](../README.md)
