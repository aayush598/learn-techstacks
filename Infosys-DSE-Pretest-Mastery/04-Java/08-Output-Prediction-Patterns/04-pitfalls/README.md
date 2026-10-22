# 04-pitfalls — Output Prediction Patterns

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 22 min_

## What lives here

The named traps, written as **wrong output string → right output string → why → guard**, plus the
compile-error traps: snippets that look valid but the compiler rejects.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-output-traps.md](01-output-traps.md) | 143 | 12 named output traps with the exact wrong output each one produces, plus a summary table |
| [02-compile-error-traps.md](02-compile-error-traps.md) | 166 | 30 compile-error traps with the javac message, the "looks legal but is not" top 5, the widening/narrowing table, and the "no output at all" reminder |

## Use them like this

Read `01-output-traps.md` and write the **wrong** output string for each trap from memory. If you can
produce the wrong string, you can see it coming and avoid it.

## Related

- [Topic overview](../README.md)
- [Compile-error catalogue](../05-reference/02-compile-error-catalogue.md)
