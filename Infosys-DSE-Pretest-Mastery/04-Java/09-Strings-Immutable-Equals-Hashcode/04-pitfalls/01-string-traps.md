# String Traps — 10 Named Traps

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 11 min_
> **Prerequisite:** [Solved string set](../03-worked-examples/01-solved-string-set.md)

## In one sentence

Ten traps, each written as **the wrong answer you will pick → the right answer → the one-line
rule** — this is the list to re-read the night before the pre-test.

## Why the pre-test tests this

- String traps are cheap marks that candidates give away because the wrong answer "feels right".
- The trap is almost always about **identity vs content** or **literal vs regex**.
- Karthik's retro: "I lost 4 marks to `replaceAll` vs `replace`. Every single one was a different
  question."

## Core concept

The trap family:

```
Trap 1: "== is the same as equals"           → identity vs content
Trap 2: "all equal strings are the same object" → pool membership
Trap 3: "every method that looks like it changes the string" → immutability
Trap 4: "the argument to replaceAll is literal" → regex
Trap 5: "matches searches inside the string" → whole-string test
Trap 6: "compareTo returns -1/0/1" → ordering int
Trap 7: "different objects have different hash codes" → collision
Trap 8: "concatenating null throws" → "null" text
Trap 9: "split keeps all parts" → trailing empties
Trap 10: "StringBuilder is faster than String" → it is immutable
```

## The 10 traps

### Trap 1 — `==` behaves like `equals` for strings

- **Wrong answer:** `"a" == "a"` → `false`, or `"a" == new String("a")` → `true`.
- **Right answer:** the first is `true`, the second is `false`.
- **Why:** `==` compares references; the pool makes the first pair the same object.
- **Guard:** before answering any `==` question, ask *"is one side a literal or a constant
  expression?"*

### Trap 2 — Every equal string is the same object

- **Wrong answer:** `new String("a") == "a"` → `true`.
- **Right answer:** `false`.
- **Why:** `new` always creates a fresh object, outside the pool.
- **Guard:** only **literals** and **constant expressions** are pooled.

### Trap 3 — `concat` / `append` mutate the string

- **Wrong answer:** after `s.concat("x")`, `s` is `"ax"`.
- **Right answer:** `s` is unchanged; `concat` returns a new `String`.
- **Why:** `String` is immutable.
- **Guard:** "Does this method mutate or return a new object?" `String` never mutates.

### Trap 4 — `replace` treats its argument as a regex

- **Wrong answer:** `"a1b2".replace("[0-9]", "#")` → `"a#b#"`.
- **Right answer:** `"a1b2"` — `replace` is literal.
- **Guard:** `replace` = literal, `replaceAll` = regex. `split`, `matches`, `find`, `replaceFirst`
  are all regex.

### Trap 5 — `matches` finds a match anywhere

- **Wrong answer:** `"Java123".matches("[A-Za-z]+")` → `true`.
- **Right answer:** `false` — `matches` must match the **entire** string.
- **Guard:** whole string → `matches`; anywhere → `find` or `contains`.

### Trap 6 — `compareTo` returns -1, 0 or 1

- **Wrong answer:** `"B".compareTo("a")` → `-1`.
- **Right answer:** `-31` (`'B'`=66, `'a'`=97).
- **Guard:** it returns the **difference** in character values. The only safe MCQ phrasing is
  "negative", "zero", or "positive".

### Trap 7 — Unequal objects must have different hash codes

- **Wrong answer:** "if `hashCode` differs, the objects are unequal" → treated as a rule.
- **Right answer:** only the forward direction is guaranteed. Unequal objects **may** share a hash
  code (collision).
- **Guard:** equal → same hash. The reverse is **not** guaranteed.

### Trap 8 — Concatenating `null` throws

- **Wrong answer:** `null + "a"` → `NullPointerException`.
- **Right answer:** `"nulla"` — concatenation converts `null` to the text `"null"`.
- **Guard:** `+` and `String.valueOf` are null-safe; `toString()`, `length()`, `equals()` are not.

### Trap 9 — `split` keeps every part

- **Wrong answer:** `"a,b,,".split(",")` → 4 elements.
- **Right answer:** 2 elements — trailing empty strings are removed.
- **Guard:** `split(regex, -1)` keeps them.

### Trap 10 — `StringBuilder` is faster than `String`

- **Wrong answer:** `StringBuilder` is faster than `String`.
- **Right answer:** `StringBuilder` is faster than **`StringBuffer`**; `String` is immutable and
  cannot be compared for speed this way.
- **Guard:** `StringBuilder` (not thread-safe) vs `StringBuffer` (thread-safe, `synchronized`).

## The trap table

| # | Trap | Wrong answer | Right answer |
|---|---|---|---|
| 1 | `==` vs `equals` | `"a" == "a"` → false | true |
| 2 | Pool membership | `new String("a") == "a"` → true | false |
| 3 | Mutation | `concat` changes `s` | `s` unchanged |
| 4 | Regex vs literal | `replace("[0-9]","#")` → `a#b#` | `a1b2` |
| 5 | `matches` scope | `"Java123".matches("[A-Za-z]+")` → true | false |
| 6 | `compareTo` result | returns −1/0/1 | returns the difference |
| 7 | Hash contract | reverse direction guaranteed | reverse **not** guaranteed |
| 8 | `null` concat | NPE | `"null"` |
| 9 | `split` empties | 4 elements | 2 elements |
| 10 | `StringBuilder` vs `String` | faster than `String` | faster than `StringBuffer` |

## Common traps

| Trap | Fix |
|---|---|
| Answering a `==` question without checking the pool | Literal or constant expression? |
| Picking "regex" for `replace` | `replace` is literal |
| Treating `compareTo` as a boolean | It returns an ordering int |
| Assuming unequal ⇒ different hash | Collisions are legal |
| Forgetting `split` drops trailing empties | Use `-1` to keep them |

## Checklist

- [ ] I can name all 10 traps.
- [ ] I can write the wrong answer for traps 4, 6 and 9 from memory.
- [ ] I know the pool rule in one sentence.
- [ ] I know the hashCode contract in both directions.
- [ ] I know which string methods are null-safe.

## Related

- [String immutability and the pool](../01-concepts/01-string-immutability-and-pool.md)
- [equals, hashCode and comparison](../01-concepts/02-equals-hashcode-and-comparison.md)
- [String API decision table](../02-techniques/01-string-api-decision-table.md)
- [Solved string set](../03-worked-examples/01-solved-string-set.md)
- [String one-pager](../05-reference/01-string-one-pager.md)
- [Topic overview](../README.md)
