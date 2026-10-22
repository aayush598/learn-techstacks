# String API Decision Table

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 10 min_
> **Prerequisite:** [String immutability and the pool](../01-concepts/01-string-immutability-and-pool.md)

## In one sentence

When a question asks **which method does X**, you do not need the whole API — you need one row of
the decision table.

## Why the pre-test tests this

- "Which method replaces all occurrences of a substring?" — `replace` vs `replaceAll` is a standard
  4-option question with a definite answer.
- `matches` vs `find`, `trim` vs `strip`, `split` vs `substring` — same archetype.
- The table turns a 60-second hunt through the API into a 10-second lookup.

## Core concept

### The main decision table

| I want to… | Use | Not | Gotcha |
|---|---|---|---|
| Compare content | `equals` | `==` | `equals` is case-**sensitive** |
| Compare ignoring case | `equalsIgnoreCase` | `equals` | |
| Order two strings | `compareTo` | `equals` | Returns a negative/0/positive int |
| Change case | `toUpperCase` / `toLowerCase` | | Returns a new `String` |
| Join with a separator | `String.join(",", list)` | manual loop | Java 8+ |
| Repeat | `repeat(n)` | | **Java 11+** |
| Cut a part | `substring(start)` / `substring(start, end)` | `slice` | `end` is **exclusive** |
| Replace literal text | `replace(CharSequence, CharSequence)` | `replaceAll` | Literal, no regex |
| Replace one char | `replace(char, char)` | | Literal |
| Replace by regex | `replaceAll(regex, repl)` / `replaceFirst` | `replace` | Regex! `.` matches any char |
| Test the whole string | `matches(regex)` | `find` | Must match **entirely** |
| Test a substring | `find` / `contains` | `matches` | |
| Split | `split(regex)` | `split(regex, 0)` | Regex! Trailing empties dropped |
| Trim spaces | `strip` (Java 11+) / `trim` | | `trim` only removes chars ≤ `' '` |
| Check empty | `isEmpty()` | `isBlank()` | `isEmpty` does not consider spaces |
| Check blank | `isBlank()` (Java 11+) | `isEmpty()` | null / empty / whitespace-only |
| Convert to a string | `String.valueOf(x)` | `x.toString()` | `valueOf` is null-safe |
| Convert to chars | `toCharArray()` | `getChars` | Copies |
| Length | `length()` | `size()` | `length` is a **method** on `String` |
| Convert to a number | `Integer.parseInt(s)` | | Throws `NumberFormatException` |
| Get a char | `charAt(i)` | `[]` | `String` has no `[]` operator |

### `replace` vs `replaceAll` — the two worked examples

```java
"a1b2".replaceAll("[0-9]", "#");   // "a#b#"   ← regex
"a1b2".replace("1", "#");          // "a#b2"   ← literal
"a.b".replace(".", "#");           // "a.b"    ← literal "." matches only "."
"a.b".replaceAll(".", "#");        // "a#b"    ← regex "." matches any char
```

**Rule:** `replace` = literal; `replaceAll` = regex. `replaceFirst` = regex, first match only.

### `matches` vs `find`

```java
"Java123".matches("[A-Za-z]+");     // false — the digits are not matched
"Java123".matches("[A-Za-z]+.*");   // true  — matches the WHOLE string
"Java123".find("[0-9]+");           // true  — finds "123" anywhere
```

**Rule:** `matches` must match the **entire** string; `find` searches for a match anywhere.

### `split` — the regex and the trailing-empty rules

```java
"a,b,c".split(",");        // ["a", "b", "c"]
"a,b,,".split(",");        // ["a", "b"]        ← trailing empties dropped
"a,b,,".split(",", -1);    // ["a", "b", "", ""]  ← limit -1 keeps them
"a1b2c".split("[0-9]");    // ["a", "b", "c"]   ← regex
"a.b".split(".");          // []               ← "." matches every char!
```

- `split` takes a **regex**, so a literal `.` must be escaped: `"a\\.b".split("\\.")` → `["a", "b"]`.
- Trailing empty strings are removed. Use `split(regex, -1)` to keep them.
- `split(regex, 0)` behaves the same as `split(regex)` for trailing empties.
- A limit of `n > 0` applies the regex at most `n - 1` times.

### `trim` vs `strip` vs `stripLeading` vs `stripTrailing`

| Method | Java version | Removes |
|---|---|---|
| `trim()` | 1.0 | Any char `<= ' '` (U+0020) — spaces, tabs, newlines, control chars |
| `strip()` | **11+** | Unicode whitespace only |
| `stripLeading()` | **11+** | leading whitespace only |
| `stripTrailing()` | **11+** | trailing whitespace only |

For the pre-test on Java 8, `strip` may not exist. If the question mentions `strip`, it is probably a
"which Java version introduced this?" question.

### The `null`-safety table

| Expression | `s == null` | `s != null` |
|---|---|---|
| `s.length()` | NPE | works |
| `s.equals("x")` | NPE | works |
| `"x".equals(s)` | `false` | works |
| `s.isEmpty()` | NPE | works |
| `s.trim()` | NPE | works |
| `String.valueOf(s)` | `"null"` | the string |
| `s + ""` | `"null"` | the string |
| `s.toString()` | NPE | works |
| `Objects.toString(s, "N/A")` | `"N/A"` | the string |

**Rule:** `String.valueOf` is null-safe; `toString` is not. `+` is null-safe but produces `"null"`,
which is usually **not** what the caller wanted.

### Text blocks (Java 15+)

```java
String s = """
        Hello,
        World""";
```

- The incidental whitespace is stripped based on the least-indented line.
- A trailing newline is **not** included unless you write `\`.
- Compiles to a **constant string expression**, so it is pooled and can be used in a `switch` label
  (Java 21+ pattern-matching `switch`).
- Java 8 has **no** text blocks — a question using them is a "which version" question.

### The 60-second "which method?" procedure

1. **Is the argument a regex?** If the question shows `.`, `[`, `*`, `\d`, `+`, `?`, or `|`, it is a
   regex → `replaceAll`, `replaceFirst`, `split`, `matches`, `find`.
2. **Is the match partial or whole?** Partial → `find` / `contains`. Whole → `matches`.
3. **Is the operation on characters or on text?** Characters → `charAt`, `toCharArray`, `indexOf(char)`.
4. **Is the value possibly `null`?** → `String.valueOf` / `Objects.equals`.
5. **Is the answer "the same string with a change"?** → `trim` / `strip` / `toUpperCase` /
   `substring` / `replace` — and remember it returns a **new** `String`.

## Worked example

**Q. What is printed?**

```java
public class Main {
    public static void main(String[] args) {
        String s = "  Java  ";
        System.out.println("[" + s.trim() + "]");
        System.out.println("[" + s.strip() + "]");
        System.out.println(s.length());
        System.out.println("a1b2".replaceAll("[0-9]", "#"));
        System.out.println("a1b2".replace("[0-9]", "#"));
        System.out.println("a1b2".replaceAll("[0-9]", "#").length());
    }
}
```

**Solution**

| Line | Result | Rule |
|---|---|---|
| `s.trim()` | `"Java"` | removes chars ≤ `' '` |
| `s.strip()` | `"Java"` | removes whitespace (Java 11+) |
| `s.length()` | `8` | 2 spaces + 4 letters + 2 spaces |
| `replaceAll("[0-9]", "#")` | `"a#b#"` | regex |
| `replace("[0-9]", "#")` | `"a1b2"` | literal — `[0-9]` is not found as text |
| `.length()` of the result | `4` | `a#b#` is 4 characters |

**Output (exact):**

```
[Java]
[Java]
8
a#b#
a1b2
4
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `a1b2` for the `replaceAll` line | `[0-9]` is a character class, matching `1` and `2` |
| `6` for `s.length()` | Count again: 2 + 4 + 2 = 8 |
| `a#b#` for the `replace` line | `replace` is literal, and the literal text `[0-9]` does not occur |

## Quick rules

- `replace` = literal, `replaceAll` = regex.
- `matches` = whole string, `find` = anywhere.
- `split` is a regex and drops trailing empty strings unless you pass `-1`.
- `trim` removes chars ≤ `' '`; `strip` (11+) removes Unicode whitespace.
- `String.valueOf` is null-safe; `toString` is not; `+` produces `"null"`.
- `substring(end)` is **exclusive**; `substring(start)` goes to the end.
- `isEmpty()` vs `isBlank()` — `isEmpty` ignores whitespace, `isBlank` does not.
- `repeat` is Java 11+, text blocks are Java 15+, `strip`/`isBlank` are Java 11+.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| `replace` treats the argument as a regex | `a#b#` | `a1b2` (literal) |
| `matches` finds a substring | `true` for `"Java123".matches("[A-Za-z]+")` | `false` |
| `split` keeps trailing empties | 4 elements | 2 elements |
| `substring(1, 3)` of `"Java"` | `"Ja"` | `"av"` |
| `valueOf(null)` throws | NPE | `"null"` |

## Checklist

- [ ] I can answer "literal or regex?" without hesitating.
- [ ] I remember `substring`'s end index is exclusive.
- [ ] I know the Java version of `strip`, `isBlank`, `repeat`, and text blocks.
- [ ] I know `split` drops trailing empty strings.
- [ ] I know which two string methods are null-safe.

## Related

- [String immutability and the pool](../01-concepts/01-string-immutability-and-pool.md)
- [equals, hashCode and comparison](../01-concepts/02-equals-hashcode-and-comparison.md)
- [Solved string set](../03-worked-examples/01-solved-string-set.md)
- [String traps](../04-pitfalls/01-string-traps.md)
- [String one-pager](../05-reference/01-string-one-pager.md)
- [Topic overview](../README.md)
