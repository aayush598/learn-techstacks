# String Immutability and the String Pool

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 11 min_
> **Prerequisite:** none

## In one sentence

A `String` cannot be changed after creation, so identical literals are **shared** in the string pool
— which is why `==` works for literals and fails for `new String(...)`.

## Why the pre-test tests this

- `==` vs `equals` on strings is one of the most frequent Java MCQs in any screening test.
- The pool rules explain **why** the answer is what it is, so you can derive it instead of guessing.
- "Is a `final String` a compile-time constant?" is a standard follow-up question.

## Core concept

### Immutability — what it means and what it buys you

`String` is `final` and its internal `char[]`/`byte[]` is never exposed for modification. Every
method that looks like it changes a string actually returns a **new** `String`:

| Call | Returns |
|---|---|
| `s.concat("x")` | a new `String` with `s + "x"` |
| `s.substring(1)` | a new `String` |
| `s.toUpperCase()` | a new `String` (or `s` itself if no change is needed) |
| `s.replace('a','b')` | a new `String` |
| `s.trim()` | a new `String` (or `s` if nothing to trim) |
| `s.replaceAll(...)` | a new `String` |

**Consequence 1 — safe sharing.** A `String` can be passed between threads with no synchronisation,
because nobody can mutate it.

**Consequence 2 — safe as a key.** `HashMap` keys and `HashSet` elements can be `String`s without
worrying that the hash changes after insertion.

**Consequence 3 — hashCode is stable.** A `String`'s hash cannot change while it is in a hash
collection.

### The string pool

The JVM keeps a table of `String` objects (the **string pool**, an intern table). String
**literals** in your code are placed in the pool and reused.

| Expression | Pooled? | `s1 == s2`? |
|---|---|---|
| `String s1 = "abc"; String s2 = "abc";` | both | ✅ `true` |
| `String s1 = "abc"; String s2 = new String("abc");` | only `s1` | ❌ `false` |
| `String s1 = "ab" + "c";` | yes — constant expression, folded | ✅ `true` against `"abc"` |
| `String s1 = "ab" + variable;` | no — runtime concatenation | ❌ `false` against `"abc"` |
| `final String s = "abc"; String t = s;` | yes — `s` is a constant variable | ✅ `true` |
| `final String s = build();` | no — not a constant expression | ❌ `false` |
| `String t = "abc".intern();` | yes | ✅ `true` against the literal |

**The rule:** a `String` expression is folded into a **compile-time constant** only if it is built
purely from literals, other constant variables, and primitive constants with `+`.

```java
final int n = 5;
String a = "x" + n;      // constant expression → folded → pooled
String b = "x" + 5;      // constant expression → folded → pooled
int m = 5;
String c = "x" + m;      // NOT constant (m is not final) → runtime → not pooled
```

### `intern()`

`intern()` returns the pool instance for the string's characters:

```java
String s = new String("abc");
System.out.println(s == s.intern());   // false
System.out.println(s.intern() == "abc");  // true
```

Since Java 7 the intern table lives on the heap (permanent generation removal), so interned strings
are reclaimed like normal objects.

### `final String` and constant folding

A **constant variable** is: `final`, of type `String` or a primitive, and initialised with a
**constant expression**. A constant variable's value is *inlined* at the point of use.

```java
final String A = "Java";       // constant variable
String B = A + "Script";       // A is a constant → "JavaScript" is a constant expression → folded
String C = "Java" + "Script";  // folded
```

Both `B` and `C` become the pooled `"JavaScript"`.

### `StringBuilder` vs `StringBuffer`

| | `StringBuilder` | `StringBuffer` |
|---|---|---|
| Thread-safe | ❌ | ✅ (methods are `synchronized`) |
| Speed | Faster | Slower |
| Mutable | ✅ | ✅ |
| `toString()` | `new String(value)` — a copy | `new String(value)` — a copy |

Both are **mutable**, so neither is a `String` subclass issue — they are separate classes. `String`
itself is **not** `final`-inheritable because it is declared `final`.

**Rule of thumb:** single-threaded → `StringBuilder`. Shared across threads → `StringBuffer`, or
use `StringBuilder` with external synchronisation.

### `substring` — Java 6 vs Java 7+

| Version | Implementation | Consequence |
|---|---|---|
| Java 6 | The new `String` **shares** the original's backing `char[]` | The original array stays alive as long as the substring does (memory retention) |
| Java 7+ | `Arrays.copyOfRange` — the characters are **copied** | No retention, but an O(n) copy per call |

Either way the **content and behaviour are identical**: `substring` returns a new, independent,
immutable `String`. The difference is a memory/implementation detail, not an exam-level behavioural
difference — but "which Java version" questions sometimes ask it.

### `String.valueOf` vs `toString` vs `+`

| Expression | With `s == null` |
|---|---|
| `s + "!"` | `"null!"` — concatenation converts `null` to the text `"null"` |
| `String.valueOf(s)` | `"null"` — **null-safe** |
| `s.toString()` | `NullPointerException` |
| `s.length()` | `NullPointerException` |

`String.valueOf(Object)` calls `obj.toString()` for non-null objects, and returns `"null"` for
`null`. `String.valueOf(char[])` copies the array.

### `char[]` vs `String` — the security angle

```java
char[] secret = "P@ssw0rd".toCharArray();
Arrays.fill(secret, '*');        // wipes the array
System.out.println(secret.length);  // 8, all '*'
```

`String` cannot be wiped — the characters stay in the object until it is garbage collected. For
passwords, use `char[]` and clear it. `new String(char[])` copies, so mutating the array afterwards
does not change the `String`.

## Worked example

**Q. What is printed?**

```java
public class Main {
    static String build(String s) { return "Ja" + s; }
    public static void main(String[] args) {
        String a = "Java";
        final String f = "Java";
        String b = new String("Java");
        String c = "Ja" + "va";
        String d = a + "";
        String g = f + "";
        String e = build("va");
        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a == d);
        System.out.println(a == g);
        System.out.println(a == e);
        System.out.println(a.equals(e));
    }
}
```

**Solution**

| Variable | How it was made | Pooled? |
|---|---|---|
| `a` | literal | ✅ |
| `b` | `new String(...)` | ❌ |
| `c` | `"Ja" + "va"` → constant expression → folded → the pooled `"Java"` | ✅ |
| `d` | `a + ""` — `a` is a **plain local**, so this is a runtime concatenation | ❌ |
| `g` | `f + ""` — `f` is a **constant variable** (`final` + literal), so this is a constant expression → folded | ✅ |
| `e` | built at runtime inside `build(...)` → a new object | ❌ |

**Output (exact):**

```
false
true
false
true
false
true
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `a == b` → `true` | `new String` is never pooled |
| `a == d` → `true` | `a` is not `final`, so `a + ""` is a runtime concatenation, not a folded constant |
| `a == g` → `false` | `f` **is** a constant variable, so `f + ""` folds to the pooled `"Java"` |
| `a == e` → `true` | `build()` is a runtime call — no folding, no pooling |

## Quick rules

- `String` is immutable; every "modifying" method returns a **new** `String`.
- Literals and **constant expressions** are pooled; `new String(...)` and runtime concatenation are
  not.
- `intern()` returns the pooled instance.
- `final` + constant initialiser = **constant variable** → inlined at compile time.
- `StringBuilder` is not thread-safe; `StringBuffer` is.
- `String.valueOf(null)` → `"null"`; `null.toString()` → `NullPointerException`.
- `"x" + null` → `"xnull"`.
- `substring` copies in Java 7+, shares the backing array in Java 6.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| "All equal strings are the same object" | `true` | Only pooled ones are |
| "`final String` is always pooled" | `true` | Only if the initialiser is a constant expression |
| "`concat` mutates" | "the original changes" | It returns a new `String` |
| "`StringBuffer` is faster" | `StringBuffer` | `StringBuilder` is faster |
| "`substring` in Java 6 shares memory" | "the original changes" | Sharing the array is not sharing mutability — `String` is still immutable |

## Checklist

- [ ] I can state the two rules that decide `==` on strings.
- [ ] I know what makes an expression a compile-time constant.
- [ ] I know the difference between `StringBuilder` and `StringBuffer` on one line.
- [ ] I know `String.valueOf(null)` vs `null.toString()`.
- [ ] I know that `substring` behaviour is identical in content across Java 6 and 7+.

## Related

- [equals, hashCode and comparison](02-equals-hashcode-and-comparison.md)
- [String API decision table](../02-techniques/01-string-api-decision-table.md)
- [Solved string set](../03-worked-examples/01-solved-string-set.md)
- [String traps](../04-pitfalls/01-string-traps.md)
- [String one-pager](../05-reference/01-string-one-pager.md)
- [Topic overview](../README.md)
