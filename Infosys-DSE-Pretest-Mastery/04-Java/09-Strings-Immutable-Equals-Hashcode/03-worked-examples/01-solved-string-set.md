# Strings — 9 Solved Questions

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 16 min_
> **Prerequisite:** [String API decision table](../02-techniques/01-string-api-decision-table.md)

## In one sentence

Nine string questions, each solved by applying **one** rule — pool membership for identity
questions, the decision table for method questions, the contract for `hashCode` questions.

## Why the pre-test tests this

- String questions are 2–4 of the 25 Java questions and are among the fastest to answer.
- Each question below has exactly one defensible option.
- Java 8 semantics assumed; where a newer API is needed it is noted in the solution.

## Core concept

The three rules that decide these nine:

| Rule | Decides |
|---|---|
| Literal / constant expression → **pooled**; `new String` / runtime result → **not pooled** | every `==` question |
| `equals` → content; `==` → reference; `compareTo` → ordering | every comparison question |
| equal → same `hashCode`; unequal → *may* share | every `hashCode` question |

## Worked example

### Q1 — Answer: `true`, `true`

```java
public class Main {
    public static void main(String[] args) {
        String s1 = "Hello";
        String s2 = "Hello";
        String s3 = new String("Hello");
        System.out.println(s1 == s2);
        System.out.println(s1.equals(s3));
    }
}
```

**Solution** — `s1` and `s2` are **two references to the same pooled literal**, so `==` is `true`.
`s3` is a distinct object (`new` never returns a pooled instance) but holds the same characters, so
`equals` is `true`.

**Output (exact):**

```
true
true
```

**Distractors** — `false` then `true`: two literals with the same text are the **same** pooled
object. `true` then `false`: `equals` compares content, and the content is identical.

---

### Q2 — Answer: `true`, `false`, `true`

```java
import java.util.HashSet;
import java.util.Set;
public class Main {
    public static void main(String[] args) {
        Set<String> set = new HashSet<>();
        set.add("abc");
        set.add(new String("abc"));
        System.out.println(set.size());
        System.out.println("abc" == new String("abc"));
        System.out.println("abc".equals(new String("abc")));
    }
}
```

**Solution**

| Line | Result | Why |
|---|---|---|
| `set.size()` | `1` | `HashSet` uses `hashCode` + `equals`; both agree the two are the same value |
| `"abc" == new String("abc")` | `false` | the literal is pooled, the `new` object is not |
| `"abc".equals(new String("abc"))` | `true` | same characters |

**Output (exact):**

```
1
false
true
```

**Distractors** — `2` for the size: `HashSet` does not use `==`. `true` for the `==` line: `new
String` is not pooled.

---

### Q3 — Answer: `2301506`, and the contract holds both ways for `String`

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Java".hashCode());
        System.out.println(new String("Java").hashCode());
        System.out.println("Java".equals(new String("Java")));
    }
}
```

**Solution** — `String.hashCode()` is specified as
`s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]`.

```
'J'=74, 'a'=97, 'v'=118, 'a'=97
74*31^3 + 97*31^2 + 118*31 + 97
= 2204534 + 93217 + 3658 + 97
= 2301506
```

**Output (exact):**

```
2301506
2301506
true
```

**Distractors** — different hashes for the two objects: `String.hashCode` is **content-based**, not
identity-based. A hash of `0`: no.

---

### Q4 — Answer: `true`, `false`, `true`

```java
public class Main {
    public static void main(String[] args) {
        String a = "Hello";
        String b = "Hello";
        System.out.println(a == b);
        String c = a + "!";
        String d = "Hello!";
        System.out.println(c == d);
        System.out.println(c.equals(d));
    }
}
```

**Solution** — `a` and `b` are the same pooled literal → `true`. `c = a + "!"` is a **runtime**
concatenation (one operand is a variable), so it produces a new, non-pooled `String` → `c == d` is
`false`. `c.equals(d)` compares characters → `true`.

**Output (exact):**

```
true
false
true
```

**Distractors** — `true` for `c == d`: concatenation of a variable is never folded.
`false` for `c.equals(d)`: the characters are identical.

---

### Q5 — Answer: `true`, `false`, `false`, `false`

```java
public class Main {
    public static void main(String[] args) {
        String a = "Hello";
        String b = "hello";
        System.out.println(a.equals(b));
        System.out.println(a.equalsIgnoreCase(b));
        System.out.println(a.compareTo(b) == 0);
        System.out.println(a.compareTo(b) < 0);
    }
}
```

**Solution**

| Line | Result | Why |
|---|---|---|
| `a.equals(b)` | `false` | `equals` is case-sensitive |
| `a.equalsIgnoreCase(b)` | `true` | case-insensitive content comparison |
| `a.compareTo(b) == 0` | `false` | `'H'`=72, `'h'`=104 → 72 − 104 = **−32** |
| `a.compareTo(b) < 0` | `true` | the difference is negative |

**Output (exact):**

```
false
true
false
true
```

**Distractors** — `true` for line 1: `equals` does **not** ignore case. `-1` for the difference:
`compareTo` returns −32 here, not −1.

---

### Q6 — Answer: `null!`, `!null`, `null`, NPE

```java
public class Main {
    public static void main(String[] args) {
        String s = null;
        System.out.println(s + "!");
        System.out.println("!" + s);
        System.out.println(String.valueOf(s));
        System.out.println(s.length());
    }
}
```

**Solution** — the first three lines are safe: concatenation converts `null` to the text `"null"`,
and `String.valueOf(null)` is `"null"`. The fourth line dereferences `null` → `NullPointerException`.

**Output (exact)** — the first three lines, then the exception on **stderr**:

```
null!
!null
null
Exception in thread "main" java.lang.NullPointerException
```

(The stack-trace frame line depends on the file layout; only the first line is fixed.)

**Distractors** — an NPE on line 1: concatenation never throws. `"null"` missing: it is printed.

---

### Q7 — Answer: `a#b#`, `a1b2`, `true`, `false`

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("a1b2".replaceAll("[0-9]", "#"));
        System.out.println("a1b2".replace("[0-9]", "#"));
        System.out.println("a1b2".matches("[a-z0-9]+"));
        System.out.println("a1b2".matches("[a-z]+"));
    }
}
```

**Solution**

| Line | Result | Rule |
|---|---|---|
| `replaceAll("[0-9]", "#")` | `"a#b#"` | `[0-9]` is a regex character class |
| `replace("[0-9]", "#")` | `"a1b2"` | literal — the text `[0-9]` does not occur |
| `matches("[a-z0-9]+")` | `true` | the regex matches the **whole** string |
| `matches("[a-z]+")` | `false` | `matches` requires the entire string to match; `1` and `2` are not in `[a-z]` |

**Output (exact):**

```
a#b#
a1b2
true
false
```

**Distractors** — `a#b#` for the `replace` line: `replace` is literal. `true` for the last line:
`matches` is a whole-string test, not a search.

---

### Q8 — Answer: `2`, `4`

```java
public class Main {
    public static void main(String[] args) {
        String[] parts = "a,b,,".split(",");
        System.out.println(parts.length);
        String[] kept = "a,b,,".split(",", -1);
        System.out.println(kept.length);
    }
}
```

**Solution** — `split(regex)` **drops trailing empty strings**, so `"a,b,,"` yields `["a", "b"]`
→ length 2. Passing the limit `-1` keeps trailing empty strings →
`["a", "b", "", ""]` → length 4.

**Output (exact):**

```
2
4
```

**Distractors** — `4` for the first line: trailing empties are dropped. `3` for the second: the two
trailing commas produce **two** empty strings, not one.

---

### Q9 — Answer: `true` — and the reason is that `String` is immutable

```java
public class Main {
    public static void main(String[] args) {
        String s = "Java";
        s.concat("Script");
        System.out.println(s);
        StringBuilder sb = new StringBuilder("Java");
        sb.append("Script");
        System.out.println(sb);
    }
}
```

**Solution** — `String` is immutable, so `concat` returns a **new** `String` and the return value is
**discarded**. `s` is still `"Java"`. `StringBuilder` is mutable, so `append` changes it in place →
`JavaScript`.

**Output (exact):**

```
Java
JavaScript
```

**Distractors** — `JavaScript` for the first line: `concat` does not mutate the receiver.
`Java` for the second: `StringBuilder.append` does mutate.

## Quick rules

- Two literals → `==` is `true`. A literal vs `new String` → `false`.
- Runtime concatenation (`a + "!"`) → `==` against a literal is `false`.
- `String.hashCode()` is content-based and specified; `"Java".hashCode()` is `2301506`.
- `equals` is case-sensitive; `equalsIgnoreCase` is not.
- `compareTo` returns the character difference (`'H'` vs `'h'` → −32), not −1.
- `+` with `null` → `"null"`; `String.valueOf(null)` → `"null"`; `null.length()` → NPE.
- `replaceAll` = regex, `replace` = literal, `matches` = whole string, `find` = anywhere.
- `split` drops trailing empty strings; `-1` keeps them.
- `String` methods return new objects; `StringBuilder` methods mutate.

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| `==` on two literals said `false` | Q1 | Literals are pooled |
| Runtime concatenation said `true` | Q4 | No folding without constant expressions |
| `compareTo` said `-1` | Q5 | It returns the difference |
| `split` said 4 elements | Q8 | Trailing empties are dropped |
| `concat` said to mutate | Q9 | `String` is immutable |

## Checklist

- [ ] I can state the pool rule in one sentence.
- [ ] I can compute `"Java".hashCode()` on paper.
- [ ] I know `compareTo` does not return only -1/0/1.
- [ ] I know `split` drops trailing empty strings.
- [ ] I finished all 9 in under 16 minutes.

## Related

- [String immutability and the pool](../01-concepts/01-string-immutability-and-pool.md)
- [equals, hashCode and comparison](../01-concepts/02-equals-hashcode-and-comparison.md)
- [String API decision table](../02-techniques/01-string-api-decision-table.md)
- [String traps](../04-pitfalls/01-string-traps.md)
- [String one-pager](../05-reference/01-string-one-pager.md)
- [Topic overview](../README.md)
