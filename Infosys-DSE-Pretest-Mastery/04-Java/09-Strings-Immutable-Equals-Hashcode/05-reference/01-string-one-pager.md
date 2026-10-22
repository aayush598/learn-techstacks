# Strings — One-Page Revision Sheet

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 5 min_
> **Prerequisite:** [String API decision table](../02-techniques/01-string-api-decision-table.md)

## In one sentence

Print this page and strings collapse to **three tables**: pool rules, the comparison operators, and
the method cheat sheet.

## Why the pre-test tests this

- String questions are 2–4 of the 25 Java questions and are the fastest to bank.
- If you can recite the three tables, you lose at most one mark here.

## Core concept

### Table 1 — pool rules (decides every `==` question)

| Expression | Pooled? | `== "abc"` ? |
|---|---|---|
| `String s = "abc";` | ✅ | `true` |
| `String s = "a" + "bc";` (constant expression) | ✅ | `true` |
| `final String s = "abc";` (constant variable) | ✅ | `true` |
| `String s = new String("abc");` | ❌ | `false` |
| `String s = "a" + variable;` | ❌ | `false` |
| `String s = someMethod();` | ❌ | `false` |
| `String s = "abc".substring(0);` | ❌ | `false` |
| `String s = "abc".intern();` | ✅ | `true` |

### Table 2 — comparison operators

| Call | Compares | Returns | Null-safe |
|---|---|---|---|
| `a == b` | reference | `boolean` | ✅ |
| `a.equals(b)` | content | `boolean` | ❌ |
| `a.equalsIgnoreCase(b)` | content, case-insensitive | `boolean` | ❌ |
| `a.compareTo(b)` | lexicographic order | negative / 0 / positive `int` | ❌ |
| `a.compareToIgnoreCase(b)` | order, case-insensitive | `int` | ❌ |
| `Objects.equals(a, b)` | content | `boolean` | ✅ |

**Contract:** `a.equals(b)` ⇒ `a.hashCode() == b.hashCode()`. The reverse is **not** guaranteed.

`String.hashCode()` = `s[0]*31^(n-1) + … + s[n-1]`. `"Java".hashCode()` = `2301506`.

### Table 3 — method cheat sheet

| I want | Use | Gotcha |
|---|---|---|
| Literal replacement | `replace(CharSequence, CharSequence)` | not a regex |
| Regex replacement | `replaceAll`, `replaceFirst` | regex |
| Whole-string test | `matches` | not a partial search |
| Partial search | `find`, `contains` | |
| Split | `split(regex)` | regex; drops trailing empties |
| Keep empties | `split(regex, -1)` | |
| Cut | `substring(start)` / `substring(start, end)` | `end` is exclusive |
| Trim | `trim()` (Java 1.0), `strip()` (Java 11+) | `trim` removes chars ≤ `' '` |
| Join | `String.join(",", coll)` | Java 8+ |
| Repeat | `repeat(n)` | Java 11+ |
| Empty? | `isEmpty()` | |
| Blank? | `isBlank()` | Java 11+ |
| Null-safe to string | `String.valueOf(x)` | |
| Multi-line literal | text block | Java 15+ |
| Mutable buffer | `StringBuilder` (not thread-safe) / `StringBuffer` (thread-safe) | |

### Table 4 — the null table

| Expression | `s == null` |
|---|---|
| `s + "!"` | `"null!"` |
| `String.valueOf(s)` | `"null"` |
| `s.toString()` | NPE |
| `s.length()` | NPE |
| `s.equals("x")` | NPE |
| `"x".equals(s)` | `false` |
| `s == null` | `true` |
| `Objects.toString(s, "N/A")` | `"N/A"` |

### 60-second budget

| Phase | Seconds | Action |
|---|---|---|
| Classify the operands | 10 | literal / `new` / computed |
| Pick the operator | 5 | `==` vs `equals` vs `compareTo` |
| Check `null` | 5 | could either side be null? |
| Apply the one rule | 20 | pool table, contract table, or method table |
| Write the answer | 10 | exact string |
| Match | 10 | character by character |
| **Total** | **~60** | 30 s of slack |

## Worked example

**Q. What is printed?**

```java
public class Main {
    static String get() { return "Java"; }
    public static void main(String[] args) {
        String a = "Java";
        String b = new String("Java");
        String c = get();
        System.out.println(a == b);
        System.out.println(a.equals(c));
        System.out.println("Java".hashCode());
    }
}
```

- `a == b` → `false` (`new` is not pooled).
- `a.equals(c)` → `true` (same characters).
- `"Java".hashCode()` → `2301506`.

**Note** — `get()` returns a **literal**, so `c` is the interned `"Java"` too. A method that built the
string at runtime would hand back a fresh, unpooled object.

**Output (exact):**

```
false
true
2301506
```

## Quick rules

- `String` is immutable; every "modifying" method returns a **new** `String`.
- Only literals and **constant expressions** are pooled.
- `==` → reference; `equals` → content; `compareTo` → ordering.
- Equal ⇒ same hash code. Unequal **may** share one.
- `replace` is literal; `replaceAll` is regex; `matches` is whole-string; `find` is anywhere.
- `split` drops trailing empty strings.
- `+` with `null` → `"null"`; `String.valueOf(null)` → `"null"`; `null.toString()` → NPE.

## Common traps

| Trap | Fix |
|---|---|
| `==` on two literals → false | Literals are pooled |
| Runtime concatenation → pooled | No folding |
| `replace` as a regex | It is literal |
| `compareTo` returns -1/0/1 | It returns the difference |
| Unequal ⇒ different hash | Collisions are legal |

## Checklist

- [ ] I can recite the pool table.
- [ ] I know the hashCode contract in both directions.
- [ ] I can compute `"Java".hashCode()` on paper.
- [ ] I know the Java version of `strip`, `isBlank`, `repeat` and text blocks.
- [ ] I know the 60-second budget.

## Related

- [String immutability and the pool](../01-concepts/01-string-immutability-and-pool.md)
- [equals, hashCode and comparison](../01-concepts/02-equals-hashcode-and-comparison.md)
- [String API decision table](../02-techniques/01-string-api-decision-table.md)
- [Solved string set](../03-worked-examples/01-solved-string-set.md)
- [String traps](../04-pitfalls/01-string-traps.md)
- [Topic overview](../README.md)
