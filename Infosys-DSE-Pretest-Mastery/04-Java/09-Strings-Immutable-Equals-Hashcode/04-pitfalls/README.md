# 04-pitfalls — Strings, Immutability, equals & hashCode

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 11 min_

## What lives here

10 named string traps, each written as **the wrong answer you will pick → the right answer → the
one-line rule**.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-string-traps.md](01-string-traps.md) | 145 | 10 traps with the wrong answer, the right answer, and the guard, plus a summary table and a checklist |

## The 10 traps in one line each

1. `==` is not `equals`.
2. Equal strings are not always the same object.
3. `String` methods never mutate.
4. `replace` is literal, `replaceAll` is regex.
5. `matches` is a whole-string test.
6. `compareTo` returns a difference, not −1/0/1.
7. Unequal objects may share a hash code.
8. Concatenating `null` yields `"null"`, not NPE.
9. `split` drops trailing empty strings.
10. `StringBuilder` is faster than `StringBuffer`, not than `String`.

## Related

- [Topic overview](../README.md)
- [Solved string set](../03-worked-examples/01-solved-string-set.md)
