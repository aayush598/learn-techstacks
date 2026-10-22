# 04-pitfalls — Arrays, ArrayList & Loops

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 12 min_

## What lives here

12 traps, each written as **the wrong answer you will pick → the right answer → the one-line
guard**.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-array-and-loop-traps.md](01-array-and-loop-traps.md) | 159 | The 12-trap table, the full `remove` overload table, the three list-creation flavours, the fail-fast trap with its 2 legal alternatives, the loop-exit table, the array-shape trap, a worked trap |

## The 12 traps in one line each

1. `arr.length()` → `length` is a field.
2. A raw array prints its contents → it prints `[I@hash`.
3. `list.remove(1)` removes the value → it removes index 1.
4. `Arrays.asList` supports `add` → it throws.
5. `List.of` supports `set` → it throws.
6. `String[]` cannot be an `Object[]` → it can, then `ArrayStoreException`.
7. Removing from a list in a for-each is safe → `ConcurrentModificationException`.
8. `continue` skips `i++` → it does not.
9. `do-while` with a false condition runs 0 times → it runs 1.
10. `break` in a nested loop exits both → it exits the innermost.
11. `Arrays.sort` on `String[]` is numeric → it is lexicographic.
12. `list.toArray()` returns a `String[]` → it returns `Object[]`.

## Related

- [Topic overview](../README.md)
- [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)
