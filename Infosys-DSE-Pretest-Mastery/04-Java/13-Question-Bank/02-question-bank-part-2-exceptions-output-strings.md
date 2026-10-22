# Java Exceptions, Output & Strings — Question Bank

> Section 4 · Java · Exceptions, Output & Strings · _30 questions · ~45 min_

**How to use this bank:** answer all questions on paper with a 90-second cap each. Answers +
brief reasoning at the bottom. Score yourself honestly.

---

## In one sentence

**These 30 questions are where the marks are won and lost** — they are the mechanical ones, and
every one of them has a definite, printable answer you can compute in 90 seconds.

## Why the pre-test tests this

- Output-prediction questions are the single biggest cluster in Section 4. They are pure pattern
  matching, and the people who score highest are the ones who have **drilled the patterns**.
- Exception questions test control flow, not exception philosophy: which clause runs, in what
  order, and what gets swallowed.
- String questions test whether you know `==` vs `equals`, the pool, and the immutability rule.
- Ananya loses marks here by reading the whole code block before starting. Read the **last line**
  first — that tells you what is being asked.

## What this bank covers

| Block | Questions | The skill being tested |
|---|---|---|
| Exceptions and error handling | Q1–Q10 | hierarchy, checked vs unchecked, `catch`/`finally` order |
| Output prediction | Q11–Q20 | evaluation order, `continue`, dispatch, ternary promotion |
| Strings | Q21–Q30 | pool, `equals` vs `==`, `substring`, `split`, immutability |

---

## Q1. What is the root of the Java exception hierarchy?

A. `Exception`
B. `Throwable`
C. `RuntimeException`
D. `Error`

---

## Q2. Which of these is an **unchecked** exception?

A. `IOException`
B. `SQLException`
C. `ArithmeticException`
D. `ClassNotFoundException`

---

## Q3. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        try {
            System.out.println("try");
            int x = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("catch");
        } finally {
            System.out.println("finally");
        }
    }
}
```

A. `try` then `finally` — the `catch` never runs
B. `try` then `catch` then `finally`, each on its own line
C. `catch` then `finally`
D. `try` then `catch` — `finally` is skipped because an exception was thrown

---

## Q4. What does this program print, if anything?

```java
public class Main {
    public static void main(String[] args) {
        try {
            System.out.println(returnOne());
        } finally {
            System.out.println("finally");
        }
    }
    static int returnOne() {
        try {
            return 1;
        } finally {
            return 2;
        }
    }
}
```

A. `2` then `finally`
B. `1` then `finally`
C. `finally` then `2`
D. `2` only — the outer `finally` is skipped

---

## Q5. What is printed, in order?

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("A");
        try {
            System.out.println("B");
            throw new RuntimeException("boom");
        } catch (Exception e) {
            System.out.println("C");
        } finally {
            System.out.println("D");
        }
        System.out.println("E");
    }
}
```

A. `A`, `B`, `C`, `D`, `E`
B. `A`, `B`, `D`, `E`
C. `A`, `B`, `C`
D. `A`, `B`, `D`

---

## Q6. Which `catch` ordering compiles?

A. `catch (Exception e)` followed by `catch (RuntimeException e)`
B. `catch (RuntimeException e)` followed by `catch (Exception e)`
C. Both orderings compile
D. Neither ordering compiles

---

## Q7. Does the `finally` block run when `System.exit(0)` is called inside the `try` block?

A. Yes, `finally` always runs
B. No — `System.exit()` terminates the JVM and skips `finally`
C. Yes, but only if there is no `catch` clause
D. It depends on the JVM implementation

---

## Q8. Which of these is a **checked** exception — one that must be declared or caught?

A. `RuntimeException`
B. `ArithmeticException`
C. `IOException`
D. `NullPointerException`

---

## Q9. Which multi-catch clause will **not** compile?

A. `catch (IOException | SQLException e)`
B. `catch (Exception | IOException e)`
C. `catch (ArithmeticException | NullPointerException e)`
D. `catch (RuntimeException | Error e)`

---

## Q10. Which statement about `try`-with-resources is correct?

A. `close()` is called automatically, in reverse order of declaration
B. `close()` must be called manually in a `finally` block
C. `close()` is called only when an exception occurs
D. `close()` is called in declaration order

---

## Q11. What is printed?

```java
int x = 5;
int y = x++ + ++x;
System.out.println(y);
```

A. `11`
B. `12`
C. `13`
D. `14`

---

## Q12. What is printed?

```java
int a = 0, b = 0;
int c = (a++ > 0) && (b++ > 0);
System.out.println(a + " " + b);
```

A. `0 0`
B. `1 0`
C. `1 1`
D. `0 1`

---

## Q13. What is printed?

```java
public class Main {
    static int i = 1;
    static { i++; }
    public static void main(String[] args) {
        System.out.println(i);
    }
}
```

A. `1`
B. `2`
C. `3`
D. A compile error — a static block cannot modify a static field

---

## Q14. What is printed?

```java
char c = 'a';
c += 1;
System.out.println(c);
```

A. `a`
B. `b`
C. `97`
D. `98`

---

## Q15. What is printed?

```java
int[] a = {1, 2, 3};
int i = 0;
a[i++] = i++;
System.out.println(a[0]);
```

A. `0`
B. `1`
C. `2`
D. `3`

---

## Q16. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("A");
        sb.append("B").insert(0, "C").reverse();
        System.out.println(sb);
    }
}
```

```

A. `ABC`
B. `BAC`
C. `CBA`
D. `CAB`

---

## Q17. What is printed?

```java
class Base { String who() { return "Base"; } }
class Derived extends Base { String who() { return "Derived"; } }
public class Main {
    public static void main(String[] args) {
        Base b = new Derived();
        System.out.println(b.who());
    }
}
```

A. `Base`
B. `Derived`
C. `Base` then `Derived`
D. A compile error

---

## Q18. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 3; i++) {
            if (i == 1) continue;
            System.out.print(i);
        }
    }
}
```

A. `012`
B. `02`
C. `1`
D. `0`

---

## Q19. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        int a = 1, b = 2;
        boolean r = (a > b) && (a++ < b);
        System.out.println(r + " " + a);
    }
}
```

A. `false 2`
B. `false 1`
C. `true 1`
D. `true 2`

---

## Q20. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        System.out.println(true ? 1 : 2.0);
    }
}
```

A. `1`
B. `1.0`
C. `2.0`
D. A compile error — the branch types differ

---

## Q21. What is printed?

```java
String a = "Java";
String b = "Java";
System.out.println(a == b);
```

A. `true`
B. `false`
C. It depends on the JVM
D. A compile error

---

## Q22. What is printed?

```java
String a = new String("Java");
String b = "Java";
System.out.println(a == b);
System.out.println(a.equals(b));
```

A. `true` then `true`
B. `false` then `true`
C. `false` then `false`
D. `true` then `false`

---

## Q23. What is printed?

```java
String s = "abc";
System.out.println(s.substring(1) + "|" + s.substring(1, 2));
```

A. `bc|b`
B. `abc|ab`
C. `bc|bc`
D. `abc|bc`

---

## Q24. What is printed?

```java
System.out.println("A" + null);
```

A. `A`
B. `Anull`
C. `null`
D. `NullPointerException`

---

## Q25. What is the value of `"Java".hashCode()`?

A. `2301506`
B. `0`
C. `4`
D. It varies from run to run

---

## Q26. What is printed?

```java
System.out.println("a,b,c".split(",").length);
System.out.println("a,b,,".split(",").length);
```

A. `3` then `3`
B. `3` then `2`
C. `3` then `4`
D. `2` then `2`

---

## Q27. What is printed?

```java
String s = "Hello";
System.out.println(s.equalsIgnoreCase("hello"));
System.out.println(s.compareTo("hello"));
```

A. `true` then `0`
B. `true` then `-32`
C. `false` then `-32`
D. `true` then `32`

---

## Q28. Which statement about `String` is correct?

A. `String` is mutable and thread-safe
B. `String` is immutable and therefore thread-safe
C. `String` is immutable but not thread-safe
D. `String` objects may only be shared within one thread

---

## Q29. What is printed?

```java
StringBuilder sb = new StringBuilder("abc");
sb.reverse();
System.out.println(sb);
sb.deleteCharAt(0);
System.out.println(sb);
```

A. `cba` then `ba`
B. `cba` then `cba`
C. `abc` then `bc`
D. `cba` then `ab`

---

## Q30. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        String s = "Java";
        s.concat("Script");
        System.out.println(s);
    }
}
```

A. `JavaScript`
B. `Java`
C. `null`
D. `JavaScript` only if the result is assigned back to `s`

---

# Answer key

| Q | Answer | Why (one line) |
|---|--------|----------------|
| 1 | B | `Throwable` is the root; `Exception` and `Error` are its two direct branches. |
| 2 | C | `ArithmeticException` extends `RuntimeException`; the other three are checked. |
| 3 | B | The exception is thrown inside `try`, so `catch` runs, and `finally` always runs last. |
| 4 | A | The `return 2` in the inner `finally` discards the pending `1`, so `2` prints, then the outer `finally` prints `finally`. |
| 5 | A | `A`, `B`, then the `catch` prints `C`, `finally` prints `D`, and execution continues to `E`. |
| 6 | B | A subclass catch must come first; the reverse order is "already been caught". |
| 7 | B | `System.exit()` shuts the JVM down — `finally` is skipped. |
| 8 | C | `IOException` is checked; the other three are `RuntimeException` subclasses. |
| 9 | B | In a multi-catch the alternatives must be disjoint — `IOException` is a subtype of `Exception`. |
| 10 | A | The JVM closes the resources in reverse order, and suppresses secondary exceptions. |
| 11 | B | `x++` yields 5 (x → 6), `++x` yields 7, so `y = 12`. |
| 12 | B | `a++ > 0` is false, so `&&` short-circuits: `a` becomes 1 and `b` stays 0. |
| 13 | B | The field initialiser runs first (`i = 1`), then the static block (`i = 2`). |
| 14 | B | `c += 1` is `c = (char)(c + 1)`, so `'a'` becomes `'b'`. |
| 15 | B | The index `i++` is evaluated first (0, i → 1), then the RHS `i++` yields 1, so `a[0] = 1`. |
| 16 | B | `"A"` → append → `"AB"` → insert → `"CAB"` → reverse → `"BAC"`. |
| 17 | B | The object's actual type is `Derived`, so `Derived.who()` runs. |
| 18 | B | `i == 1` is skipped, but `i++` still runs — so `0` and `2` print. |
| 19 | B | `a > b` is false, so `&&` short-circuits and `a++` never executes — `a` stays 1. |
| 20 | B | Both branches are numeric, so binary numeric promotion makes the result a `double`. The condition is `true`, so the taken branch is `1` → printed as `1.0`. |
| 21 | A | Both are literals, so both come from the string pool — the same object. |
| 22 | B | `new String(...)` is a fresh object, so `==` is `false`; `equals` compares content → `true`. |
| 23 | A | `substring(1)` is `"bc"` and `substring(1, 2)` is `"b"` (the end index is exclusive). |
| 24 | B | `+` converts `null` to the string `"null"`. |
| 25 | A | `String.hashCode()` is specified: `s[0]*31³ + s[1]*31² + s[2]*31 + s[3]` = 2301506. |
| 26 | B | `split` drops trailing empty strings, so `"a,b,,"` yields two parts. |
| 27 | B | `equalsIgnoreCase` ignores case → `true`; `compareTo` returns `'H' - 'h'` = 72 − 104 = −32. |
| 28 | B | `String` is immutable and `final`, so it is inherently safe to share across threads. |
| 29 | A | `reverse()` → `"cba"`, then `deleteCharAt(0)` → `"ba"`. |
| 30 | B | `concat` returns a **new** string; `s` still refers to `"Java"`. |

---

## Related

- [07 — Exceptions & Error Handling](../07-Exceptions-Error-Handling/)
- [08 — Output Prediction Patterns](../08-Output-Prediction-Patterns/)
- [09 — Strings, Immutability, equals & hashCode](../09-Strings-Immutable-Equals-Hashcode/)
- [Part 1 — OOP & Core Java](./01-question-bank-part-1-oop-and-core.md)
- [Part 3 — Static, Arrays & Threads](./03-question-bank-part-3-static-arrays-threads.md)
- [Question bank overview](./README.md)
