# equals, hashCode, and Comparing Strings

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 10 min_
> **Prerequisite:** [String immutability and the pool](01-string-immutability-and-pool.md)

## In one sentence

`equals` compares **content**, `==` compares **references**, and the contract is one-way:
**equal objects must have equal hash codes, but unequal objects may share one**.

## Why the pre-test tests this

- "Which statement about `equals` and `hashCode` is true?" is a standard MCQ with exactly one
  correct option — and the wrong options are all *half-true*.
- "What does `"ABC".compareTo("abd")` return?" is a classic trap: it returns a **negative int**, not
  `-1`.
- `null` behaviour on `equals` is worth one mark every time it appears.

## Core concept

### The three comparison operators

| Call | Compares | Returns | `null` safe? |
|---|---|---|---|
| `a == b` | **references** (identity) | `boolean` | ✅ (no dereference) |
| `a.equals(b)` | **content** (character sequence) | `boolean` | ❌ — `null.equals(x)` throws NPE |
| `a.compareTo(b)` | **lexicographic order** | `int` (negative / 0 / positive) | ❌ |
| `a.equalsIgnoreCase(b)` | content, case-insensitive | `boolean` | ❌ |
| `a.compareToIgnoreCase(b)` | order, case-insensitive | `int` | ❌ |
| `Objects.equals(a, b)` | content, null-safe | `boolean` | ✅ |

### `compareTo` details

`compareTo` returns the **difference in character values at the first differing position**, not
necessarily `-1`, `0`, or `1`.

| Expression | Result |
|---|---|
| `"abc".compareTo("abc")` | `0` |
| `"abc".compareTo("abd")` | `-1` (`'c'`=99 minus `'d'`=100) |
| `"abd".compareTo("abc")` | `1` |
| `"B".compareTo("a")` | **-31** (`'B'`=66 minus `'a'`=97) |
| `"abc".compareTo("ab")` | `3` (length difference) |
| `"abc".compareTo(null)` | `NullPointerException` |

So the correct MCQ phrasing is "a negative value", not "-1". A test that says `compareTo` returns
`-1`, `0`, or `1` is testing a misconception.

### The `equals` / `hashCode` contract

> If `a.equals(b)` is `true`, then `a.hashCode() == b.hashCode()` **must** be `true`.

| Direction | Guaranteed? |
|---|---|
| equal → same hashCode | ✅ **Yes** |
| same hashCode → equal | ❌ **No** — collisions are allowed |

**Why the contract exists:** hash-based collections (`HashMap`, `HashSet`) use `hashCode()` to pick
a bucket and `equals()` to confirm the entry in that bucket. If two equal objects had different
hash codes, the collection would not find them.

**The classic failure:** override `equals` but not `hashCode`.

```java
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    @Override public boolean equals(Object o) {
        if (!(o instanceof Point)) return false;
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }
    // hashCode NOT overridden -> identity hash
}
```

Two `Point(1,2)` objects are `equals` but have **different** `hashCode`s. So:

```java
Set<Point> s = new HashSet<>();
s.add(new Point(1,2));
s.add(new Point(1,2));
System.out.println(s.size());   // 2, not 1
```

`String` overrides **both** correctly, so `new String("a")` and `"a"` are `equals` **and** have the
same hash code, even though they are different objects.

### `String.hashCode()` — the formula

```
hash = s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]
```

For `"Java"`: `'J'`=74, `'a'`=97, `'v'`=118, `'a'`=97.

```
74*31^3 + 97*31^2 + 118*31 + 97
= 74*29791 + 97*961 + 118*31 + 97
= 2204534 + 93217 + 3658 + 97
= 2301506
```

So `"Java".hashCode()` is `2301506` in every JVM. That is a legitimate output-prediction question
because `String.hashCode` is specified exactly.

### `null` behaviour table

| Expression | Result |
|---|---|
| `null == null` | `true` |
| `null.equals(null)` | `NullPointerException` |
| `"a".equals(null)` | `false` (no exception) |
| `s.equals(null)` where `s == null` | `NullPointerException` |
| `s == null` | `true`/`false` — safe |
| `"a".compareTo(null)` | `NullPointerException` |
| `null + "a"` | `"nulla"` |
| `String.valueOf(null)` | `"null"` |
| `Objects.equals(null, null)` | `true` |
| `Objects.equals(s, null)` | `false` when `s != null`, `true` when `s == null` |

**The safe pattern:** always call `equals` on the **non-null, known** side: `"expected".equals(actual)`.

### `String` and `==` in collections

`HashSet<String>` and `HashMap<String, ?>` use `hashCode` + `equals`, so:

```java
Set<String> s = new HashSet<>();
s.add("a");
s.add(new String("a"));
System.out.println(s.size());   // 1
```

One element, because `equals` and `hashCode` both agree.

## Worked example

**Q. Which statements are TRUE?**

```java
public class Main {
    public static void main(String[] args) {
        String a = "Java";
        String b = new String("Java");
        System.out.println(a == b);
        System.out.println(a.equals(b));
        System.out.println(a.hashCode() == b.hashCode());
        System.out.println(a.compareTo(b));
        System.out.println("B".compareTo("a") < 0);
    }
}
```

**Solution**

| Line | Result | Why |
|---|---|---|
| `a == b` | `false` | `b` is a new object, not pooled |
| `a.equals(b)` | `true` | Same characters |
| `a.hashCode() == b.hashCode()` | `true` | `String.hashCode` is content-based; equal content ⇒ equal hash |
| `a.compareTo(b)` | `0` | Identical content |
| `"B".compareTo("a") < 0` | `true` | 66 − 97 = −31, which is < 0 |

**Output (exact):**

```
false
true
true
0
true
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `a == b` → `true` | `new String` is not pooled |
| `a.compareTo(b)` → `1` | Identical content gives exactly `0` |
| `"B".compareTo("a")` → `false` | Uppercase `B` (66) sorts **before** lowercase `a` (97) in ASCII |

## Quick rules

- `==` → reference; `equals` → content; `compareTo` → order (a negative int, 0, or a positive int).
- Equal objects **must** have equal hash codes; unequal objects **may** share one.
- Override `equals` and `hashCode` together, always.
- `String.hashCode()` is specified: `s[0]*31^(n-1) + ...`.
- `"Java".hashCode()` is `2301506` on every JVM.
- Never call `equals` on a possibly-`null` receiver — put the known value on the left.
- `compareTo` is case-sensitive; `"B"` sorts before `"a"`.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| "Different objects → different hash codes" | `false` for equal hashes | Hash collisions are legal |
| "`compareTo` returns -1/0/1" | `-1` | It returns the character difference |
| "`equals` on two nulls is true" | `true` | It throws NPE |
| "Uppercase sorts after lowercase" | `true` | ASCII: uppercase first |
| "Overriding `equals` is enough" | `true` | You must override `hashCode` too |

## Checklist

- [ ] I can state the contract in one line, in both directions.
- [ ] I know that `compareTo` returns an arbitrary negative/positive int.
- [ ] I know `"Java".hashCode()` is `2301506`.
- [ ] I know the null behaviour of `equals`, `==` and `+`.
- [ ] I can explain why `HashSet` de-duplicates `"a"` and `new String("a")`.

## Related

- [String immutability and the pool](01-string-immutability-and-pool.md)
- [String API decision table](../02-techniques/01-string-api-decision-table.md)
- [Solved string set](../03-worked-examples/01-solved-string-set.md)
- [String traps](../04-pitfalls/01-string-traps.md)
- [String one-pager](../05-reference/01-string-one-pager.md)
- [Topic overview](../README.md)
