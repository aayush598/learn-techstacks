# Output Prediction — Solved Set B (13 questions)

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 22 min_
> **Prerequisite:** [Solved output set A](01-solved-output-set-a.md)

## In one sentence

Thirteen more output questions covering the constructs that catch people: **constant folding,
wrapper `==`, jagged arrays, `null` concatenation, `char` arithmetic, for-each copy semantics, and
compound-assignment narrowing**.

## Why the pre-test tests this

- Set A covered the "classic" constructs. Set B covers the "second layer" ones that separate a
  60% scorer from an 85% scorer.
- Every output here is exact, including the trailing-space and newline details.
- Java 8 semantics assumed.

## Core concept

The seven new constructs:

| Construct | The one rule |
|---|---|
| Constant folding | `final` + constant initialiser → the expression is folded at compile time and the result is interned |
| Wrapper `==` | `Integer` −128..127 cached; comparing with an `int` unboxes |
| Jagged arrays | `new int[2][]` creates 2 **null** rows; you must initialise each row |
| `null` concatenation | `+` with a `null` operand yields the text `"null"` |
| `char` arithmetic | `char` promotes to `int`; `String` on either side makes it concatenation |
| For-each | each element is **copied** into the loop variable |
| Compound assignment | `x += y` casts back to the declared type of `x` |

## Worked example

### Q1 — Answer: `30`

```java
class A { static int x = 10; }
class B { static int y = A.x + 5; }
class C { static int z = B.y * 2; }
public class Main {
    public static void main(String[] args) {
        System.out.println(C.z);
    }
}
```

**Solution** — using `C.z` initialises `C`, which requires initialising `B`, which requires
initialising `A`. Order: `A.x = 10` → `B.y = 15` → `C.z = 30`.

**Output (exact):**

```
30
```

**Distractors** — `20`: ignores `A.x`. `15`: stops at `B.y`.

---

### Q2 — Answer: `true`, `true`, `false`

```java
public class Main {
    public static void main(String[] args) {
        Integer i1 = 10;
        int i2 = 10;
        Integer i3 = 10;
        System.out.println(i1 == i2);
        System.out.println(i1 == i3);
        Integer i4 = 200;
        Integer i5 = 200;
        System.out.println(i4 == i5);
    }
}
```

**Solution**

| Expression | Result | Why |
|---|---|---|
| `i1 == i2` | `true` | `Integer` vs `int` → the `Integer` is **unboxed** → `10 == 10` |
| `i1 == i3` | `true` | both autobox to the **same cached** `Integer` for 10 |
| `i4 == i5` | `false` | 200 is outside the −128..127 cache → two objects |

**Output (exact):**

```
true
true
false
```

**Distractors** — `false` for the first line: mixing `Integer` and `int` compares values, not
references. All `true`: ignores the cache.

---

### Q3 — Answer: `true`, `false`, `false`, `true`

```java
public class Main {
    static String get(String s) { return "Ja" + s; }
    public static void main(String[] args) {
        final String a = "Java";
        String b = "Ja" + "va";
        String c = get("va");
        String d = a + get("va");
        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a == d);
        System.out.println(a.equals(c));
    }
}
```

**Solution**

| Variable | Is it a compile-time constant? | Identity |
|---|---|---|
| `a` | **Yes** — `final` + literal initialiser | the interned `"Java"` |
| `b` | **Yes** — `"Ja" + "va"` is a constant expression | the interned `"Java"` |
| `c` | **No** — built at runtime inside the method | a new object |
| `d` | **No** — one operand is not constant | a new object from runtime concatenation |

**Output (exact):**

```
true
false
false
true
```

**Distractors** — `a == d` as `true`: `a + get("va")` is **not** a constant expression, so no folding
happens. `a == c` as `true`: `get("va")` concatenates at runtime, so it returns a fresh object.
**Watch out** — if `get()` had been written as `return "Java";`, the returned reference *would* be the
interned literal and `a == c` would print `true`. The rule is about **runtime** construction, not
about "came from a method".

---

### Q4 — Answer: `2 3 2`

```java
public class Main {
    public static void main(String[] args) {
        int[][] a = new int[2][];
        a[0] = new int[]{1, 2, 3};
        a[1] = new int[]{4, 5};
        System.out.println(a.length + " " + a[0].length + " " + a[1].length);
    }
}
```

**Solution** — `new int[2][]` creates an array of **2 null references**. Each row is then
initialised separately, so the rows can have **different lengths**. `a.length` is the number of rows
(2); `a[0].length` is 3; `a[1].length` is 2.

**Output (exact):**

```
2 3 2
```

**Distractors** — `2 3 3`: assumes a rectangular array. `2 2 2`: `a.length` is the row count, not
the column count.

---

### Q5 — Answer: `null!`, `!null`, `null`, `42null`

```java
public class Main {
    public static void main(String[] args) {
        String s = null;
        System.out.println(s + "!");
        System.out.println("!" + s);
        System.out.println(String.valueOf(s));
        System.out.println(String.valueOf(42) + s);
    }
}
```

**Solution** — string concatenation converts a `null` reference to the **text** `"null"`.
`String.valueOf(null)` also returns `"null"` (it is `null`-safe, unlike `null.toString()`).

**Output (exact):**

```
null!
!null
null
42null
```

**Distractors** — `NullPointerException`: concatenation never dereferences. `""` for the third line:
`String.valueOf(null)` is `"null"`, not `""`.

---

### Q6 — Answer: `66`, `131`, `xA1`, `66x`

```java
public class Main {
    public static void main(String[] args) {
        char c = 'A';
        System.out.println(c + 1);
        System.out.println(c + 'B');
        System.out.println("x" + c + 1);
        System.out.println(c + 1 + "x");
    }
}
```

**Solution**

| Expression | Result | Rule |
|---|---|---|
| `c + 1` | `66` | `'A'` is 65; `char` promotes to `int` |
| `c + 'B'` | `131` | 65 + 66 |
| `"x" + c + 1` | `"xA1"` | left to right: `"x" + 'A'` → `"xA"`, then `"xA" + 1` → `"xA1"` |
| `c + 1 + "x"` | `"66x"` | left to right: `('A' + 1)` = 66 (int), then `66 + "x"` → `"66x"` |

**Output (exact):**

```
66
131
xA1
66x
```

**Distractors** — `xA1` for the last line: `c + 1` is evaluated first, and it is arithmetic, not
concatenation.

---

### Q7 — Answer: `1` then `2 4 6`

```java
public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        for (int x : a) { x = x * 2; }
        System.out.println(a[0]);
        for (int i = 0; i < a.length; i++) { a[i] = a[i] * 2; }
        System.out.println(a[0] + " " + a[1] + " " + a[2]);
    }
}
```

**Solution** — in a for-each loop the array element is **copied** into `x`. Assigning to `x` changes
only the copy, so the array is unchanged. The indexed loop writes through `a[i]`, so it does change
the array.

**Output (exact):**

```
1
2 4 6
```

**Distractors** — `2` for the first line: for-each copies, it does not alias.

---

### Q8 — Answer: `"11 13 21 23 "`

```java
public class Main {
    public static void main(String[] args) {
        for (int i = 1; i <= 3; i++) {
            for (int j = 1; j <= 3; j++) {
                if (j == 2) continue;
                if (i == 3) break;
                System.out.print(i + "" + j + " ");
            }
        }
    }
}
```

**Solution**

| `i` | `j` | Action |
|---|---|---|
| 1 | 1 | neither condition → print `11 ` |
| 1 | 2 | `j == 2` → `continue` (inner loop) |
| 1 | 3 | print `13 ` |
| 2 | 1 | print `21 ` |
| 2 | 2 | `continue` |
| 2 | 3 | print `23 ` |
| 3 | 1 | `i == 3` → `break` exits the **inner** loop only |
| 3 | 2, 3 | never reached |

**Output (exact):**

```
11 13 21 23 
```

**Distractors** — `break` exiting the outer loop too: `break` without a label leaves only the
innermost loop.

---

### Q9 — Answer: `3`, `3.5`, `1`, `-1`, `1.0`, `3.5`

```java
public class Main {
    public static void main(String[] args) {
        int a = 7, b = 2;
        System.out.println(a / b);
        System.out.println((double) a / b);
        System.out.println(a % b);
        System.out.println(-a % b);
        System.out.println(true ? 1 : 2.0);
        System.out.println(7 / 2.0);
    }
}
```

**Solution**

| Expression | Result | Rule |
|---|---|---|
| `a / b` | `3` | both `int` → integer division, truncates toward zero |
| `(double) a / b` | `3.5` | one operand is `double` → floating division |
| `a % b` | `1` | 7 = 2×3 + 1 |
| `-a % b` | `-1` | the sign of the result follows the **dividend** |
| `true ? 1 : 2.0` | `1.0` | binary numeric promotion → the expression is a `double`, and the taken branch is `1` |
| `7 / 2.0` | `3.5` | `double` division |

**Output (exact):**

```
3
3.5
1
-1
1.0
3.5
```

**Distractors** — `3.5` for `a / b`: both operands are `int`. `1` for `-a % b`: the sign follows the
dividend, so it is `-1`. `2.0` for the ternary: the condition is `true`, so the branch that runs is
the `int` `1`. `1` for the ternary: the whole expression is a `double`, so it prints as `1.0`.

---

### Q10 — Answer: `true`, `true`, `false`, `true`

```java
public class Main {
    public static void main(String[] args) {
        Integer a = -128;
        Integer b = -128;
        Integer c = 127;
        Integer d = 127;
        Integer e = 128;
        Integer f = new Integer(128);
        System.out.println(a == b);
        System.out.println(c == d);
        System.out.println(e == f);
        System.out.println(e.intValue() == 128);
    }
}
```

**Solution** — the cache covers **−128..127 inclusive**, so −128 and 127 are both cached. `new
Integer(128)` never uses the cache, so `e == f` is `false`. `e.intValue()` unboxes to an `int`, so
the comparison is numeric.

**Output (exact):**

```
true
true
false
true
```

**Distractors** — `e == f` as `true`: `new Integer(...)` bypasses the cache. (The constructor is
deprecated since Java 9; it is used here because the pre-test runs on Java 8.)

---

### Q11 — Answer: `20`, `20`, `10`, `Child.show`, `Parent.show`

```java
class Parent {
    int val = 10;
    static void show() { System.out.println("Parent.show"); }
}
class Child extends Parent {
    int val = 20;
    static void show() { System.out.println("Child.show"); }
    void print() {
        System.out.println(val);
        System.out.println(this.val);
        System.out.println(super.val);
        show();
        Parent.show();
    }
}
public class Main {
    public static void main(String[] args) {
        new Child().print();
    }
}
```

**Solution**

| Statement | Result | Rule |
|---|---|---|
| `val` | `20` | the **nearest** field wins (`Child.val`) |
| `this.val` | `20` | same field, explicitly |
| `super.val` | `10` | the parent's field |
| `show()` | `Child.show` | `Child`'s static method **hides** the parent's; the implicit qualifier is `Child` |
| `Parent.show()` | `Parent.show` | explicitly qualified |

**Output (exact):**

```
20
20
10
Child.show
Parent.show
```

**Distractors** — `Parent.show` for the unqualified call: static methods are resolved by the
**compile-time type**, and the implicit qualifier here is `Child`.

---

### Q12 — Answer: `3`, `1`, `-1`, `3.5`

```java
public class Main {
    public static void main(String[] args) {
        long l = 7;
        int i = 2;
        System.out.println(l / i);
        System.out.println(l % i);
        System.out.println(-l % i);
        System.out.println(l / 2.0);
    }
}
```

**Solution** — `l / i` with a `long` and an `int`: the `int` is widened to `long`, the division is
integer division → `3`. `l % i` → `1`. `-l % i` → `-7 % 2` → `-1` (sign follows the dividend).
`l / 2.0` → `double` division → `3.5`.

**Output (exact):**

```
3
1
-1
3.5
```

**Distractors** — `3.5` for the first line: `i` is an `int`, so the division is integer division.
`1` for the third line: the sign follows the dividend, giving `-1`.

---

### Q13 — Answer: `15`, `11`, `b`

```java
public class Main {
    public static void main(String[] args) {
        byte b = 10;
        b += 5;
        System.out.println(b);
        int i = 10;
        i += 1.9;
        System.out.println(i);
        char c = 'a';
        c += 1;
        System.out.println(c);
    }
}
```

**Solution** — compound assignment is `x = (T)(x + y)` where `T` is the declared type of `x`.

| Statement | Expansion | Result |
|---|---|---|
| `b += 5` | `b = (byte)(10 + 5)` | `15` |
| `i += 1.9` | `i = (int)(10 + 1.9)` = `(int) 11.9` | `11` |
| `c += 1` | `c = (char)('a' + 1)` | `'b'` |

**Output (exact):**

```
15
11
b
```

**Distractors** — `11.9`: the implicit cast to `int` truncates. `a` for the last line: `+= 1` adds
one to the character code.

## Quick rules

- `final` + constant initialiser → the variable is a **constant variable**; expressions using only
  constant variables are folded at compile time and the result is interned.
- `Integer` cache = **−128..127 inclusive**.
- `new int[n][]` → `n` **null** rows.
- `+` with a `null` operand → the text `"null"`.
- `char` promotes to `int`; a `String` anywhere in the `+` chain makes it concatenation, and the
  chain is evaluated **left to right**.
- For-each **copies** the element.
- `x += y` casts back to the declared type of `x`.

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Constant folding applies to method results | Q3 | Only constant expressions fold |
| `Integer` 128 is cached | Q2, Q10 | The cache ends at 127 |
| `new int[2][]` is a rectangular array | Q4 | Rows are independent |
| Concatenation with `null` throws | Q5 | It produces `"null"` |
| `c + 1 + "x"` is `"x" + (c + 1)` | Q6 | Left to right |
| For-each writes back to the array | Q7 | It copies |
| `break` breaks both loops | Q8 | Only the innermost |

## Checklist

- [ ] I can explain why `a + get()` is not a constant expression (Q3).
- [ ] I know the `Integer` cache boundary includes both −128 and 127 (Q10).
- [ ] I can state the exact output of Q6 (four different answers).
- [ ] I know `new int[2][]` creates null rows (Q4).
- [ ] I finished all 13 in under 22 minutes.

## Related

- [Solved output set A](01-solved-output-set-a.md)
- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)
- [Output traps](../04-pitfalls/01-output-traps.md)
- [Output rules one-pager](../05-reference/01-output-rules-one-pager.md)
- [Topic overview](../README.md)
