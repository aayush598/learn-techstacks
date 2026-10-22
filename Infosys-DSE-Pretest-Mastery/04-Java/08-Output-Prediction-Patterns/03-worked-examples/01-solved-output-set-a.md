# Output Prediction — Solved Set A (12 questions)

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 20 min_
> **Prerequisite:** [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)

## In one sentence

Twelve output questions, each solved by **naming one construct and applying one rule** — the printed
output is given as an exact quoted string, spaces included.

## Why the pre-test tests this

- "What does this print?" is a reported archetype of the 25-question Java section.
- Java 8 semantics assumed throughout. Every output below is reproducible on any Java 8+ runtime.
- Do the set untimed first, then redo it with a **90-second cap per question**.

## Core concept

The six constructs used in this set:

| Construct | The one rule |
|---|---|
| Init order | static (super → sub) → instance (super → sub) → constructors (super → sub) |
| Overload resolution | strict → boxing → varargs |
| Short-circuit | the untaken branch is **not evaluated** |
| `++` | post yields the old value, pre yields the new |
| `==` on objects | `Integer` −128..127 is cached; `String` literals are interned |
| `switch` | falls through without `break` |

## Worked example

### Q1 — Answer: `"A-static B-static A-inst A-ctor B-inst B-ctor "`

```java
class A {
    static { System.out.print("A-static "); }
    { System.out.print("A-inst "); }
    A() { System.out.print("A-ctor "); }
}
class B extends A {
    static { System.out.print("B-static "); }
    { System.out.print("B-inst "); }
    B() { super(); System.out.print("B-ctor "); }
}
public class Main {
    public static void main(String[] args) {
        new B();
    }
}
```

**Solution**

| # | Event | Printed |
|---|---|---|
| 1 | `new B()` → initialise `A` (superclass first) | `A-static ` |
| 2 | initialise `B` | `B-static ` |
| 3 | `A`'s instance initialiser / instance block | `A-inst ` |
| 4 | `A`'s constructor body | `A-ctor ` |
| 5 | `B`'s instance initialiser / instance block | `B-inst ` |
| 6 | `B`'s constructor body | `B-ctor ` |

`super()` is the first statement of `B`'s constructor, so **`A`'s constructor completes before `B`'s
instance initialisers run**.

**Output (exact):**

```
A-static B-static A-inst A-ctor B-inst B-ctor 
```

**Distractors** — `"A-static B-static B-inst B-ctor A-inst A-ctor "`: puts the child instance
initialisers before the parent constructor. `"B-static A-static ..."`: wrong static order.
`"A-static A-inst A-ctor B-static ..."`: static and instance initialisers interleaved incorrectly.

---

### Q2 — Answer: `Integer`

```java
public class Main {
    static void m(Object o)  { System.out.println("Object"); }
    static void m(Integer i) { System.out.println("Integer"); }
    static void m(int... x)  { System.out.println("int..."); }
    public static void main(String[] args) {
        m(5);
    }
}
```

**Solution**

| Phase | Applicable methods |
|---|---|
| 1 — strict | none (`int` → `Object` needs boxing; `int` → `Integer` needs boxing; varargs is phase 3) |
| 2 — loose (boxing) | `m(Integer)` and `m(Object)` |
| Tie-break | `Integer` is a subtype of `Object` → **more specific** → `m(Integer)` wins |

**Output (exact):**

```
Integer
```

**Distractors** — `Object`: less specific, loses the tie-break. `int...`: varargs is phase 3, phase 2
already matched. Compile error: the call is unambiguous.

---

### Q3 — Answer: `Object`

```java
public class Main {
    static void m(Object o) { System.out.println("Object"); }
    static void m(String... s) { System.out.println("String..."); }
    public static void main(String[] args) {
        m("hi");
    }
}
```

**Solution** — Phase 1 (strict invocation) already finds an applicable method: `String` → `Object` is
a **widening reference** conversion, which is allowed in phase 1. So `m(Object)` wins and the
varargs method is never considered.

**Output (exact):**

```
Object
```

**Distractors** — `String...`: varargs is the last resort, not the first. Compile error: the call is
legal and unambiguous.

---

### Q4 — Answer: `false` then `1`

```java
public class Main {
    public static void main(String[] args) {
        int i = 0;
        boolean r = (i++ > 0) && (i++ > 0);
        System.out.println(r);
        System.out.println(i);
    }
}
```

**Solution** — `&&` evaluates its right operand only when the left is **true**. The left operand is
`0 > 0` → `false`, and `i` becomes 1. The right operand is **never evaluated**, so `i` stays 1.

**Output (exact):**

```
false
1
```

**Distractors** — `false` then `2`: the second `i++` never runs. `true` then `1`: `0 > 0` is false.

---

### Q5 — Answer: `true` then `2`

```java
public class Main {
    public static void main(String[] args) {
        int i = 0;
        boolean r = (i++ > 0) || (i++ > 0);
        System.out.println(r);
        System.out.println(i);
    }
}
```

**Solution** — `||` evaluates its right operand only when the left is **false**. The left is
`0 > 0` → `false`, and `i` becomes 1, so the right operand **does** run: `1 > 0` → `true`, and `i`
becomes 2.

**Output (exact):**

```
true
2
```

**Distractors** — `true` then `1`: the right operand was evaluated, so `i` incremented twice.
`false` then `1`: `1 > 0` is true.

---

### Q6 — Answer: `7` then `12`

```java
public class Main {
    public static void main(String[] args) {
        int i = 5;
        int j = i++ + ++i;
        System.out.println(i);
        System.out.println(j);
    }
}
```

**Solution** — Operands are evaluated left to right.

1. `i++` → yields **5**; `i` becomes 6.
2. `++i` → `i` becomes **7**, yields **7**.
3. `j = 5 + 7 = 12`.
4. `i` is 7.

**Output (exact):**

```
7
12
```

**Distractors** — `11`: ignores that `++i` yields the new value. `6` then `11`: treats both as
post-increment.

---

### Q7 — Answer: `true`, `false`, `true`

```java
public class Main {
    public static void main(String[] args) {
        Integer a = 127, b = 127;
        Integer c = 128, d = 128;
        int e = 128;
        System.out.println(a == b);
        System.out.println(c == d);
        System.out.println(c == e);
    }
}
```

**Solution** — `Integer.valueOf` reuses a cached object for values **−128..127**.

- `a == b`: both are the **same cached object** → `true`.
- `c == d`: 128 is outside the cache → two different objects → `false`.
- `c == e`: comparing an `Integer` with an `int` **unboxes** `c` → `128 == 128` → `true`.

**Output (exact):**

```
true
false
true
```

**Distractors** — all `true`: ignores the cache boundary. All `false`: ignores the cache.

---

### Q8 — Answer: `true`, `false`, `true`, `true`

```java
public class Main {
    public static void main(String[] args) {
        String s1 = "abc";
        String s2 = "abc";
        String s3 = new String("abc");
        System.out.println(s1 == s2);
        System.out.println(s1 == s3);
        System.out.println(s1.equals(s3));
        System.out.println(s3.intern() == s1);
    }
}
```

**Solution**

| Expression | Result | Why |
|---|---|---|
| `s1 == s2` | `true` | Both are the same **interned literal** from the string pool |
| `s1 == s3` | `false` | `new String(...)` creates a distinct object |
| `s1.equals(s3)` | `true` | Same characters, compared by value |
| `s3.intern() == s1` | `true` | `intern()` returns the pooled instance |

**Output (exact):**

```
true
false
true
true
```

**Distractors** — `s1 == s3` as `true`: `new` never returns a pooled instance.

---

### Q9 — Answer: `"two three default "`

```java
public class Main {
    public static void main(String[] args) {
        int x = 2;
        switch (x) {
            case 1: System.out.print("one ");
            case 2: System.out.print("two ");
            case 3: System.out.print("three ");
            default: System.out.print("default ");
        }
    }
}
```

**Solution** — `switch` starts at the matching `case` and **falls through**. There is no `break`, so
execution continues through `case 3` and into `default`.

**Output (exact):**

```
two three default 
```

(There is a trailing space after `default` and no trailing newline.)

**Distractors** — `"two "`: `switch` does not break automatically. `"two three "`: `default` runs too,
because execution falls into it.

---

### Q10 — Answer: `98`, `98`, `ax`, `xa`, `1.0`

```java
public class Main {
    public static void main(String[] args) {
        char c = 'a';
        int n = c + 1;
        System.out.println(n);
        System.out.println(c + 1);
        System.out.println(c + "x");
        System.out.println("x" + c);
        System.out.println(true ? 1 : 2.0);
    }
}
```

**Solution**

| Expression | Result | Rule |
|---|---|---|
| `c + 1` | `98` | `char` promotes to `int`; `'a'` is 97 |
| `c + 1` | `98` | same |
| `c + "x"` | `"ax"` | a `String` operand forces concatenation |
| `"x" + c` | `"xa"` | a `String` operand forces concatenation |
| `true ? 1 : 2.0` | `1.0` | the branches undergo binary numeric promotion → the whole expression is a `double`, so the taken branch `1` prints as `1.0` |

**Output (exact):**

```
98
98
ax
xa
1.0
```

**Distractors** — `97` for `c + 1`: the `+1` is included. `2` for the ternary: the condition is `true`,
so the branch that runs is the `int` `1`, not the `2.0`. `1` for the ternary: the whole expression is
a `double` after binary numeric promotion, so it prints as `1.0`.

---

### Q11 — Answer: `99`, `true`, `false`, `false`

```java
public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = a;
        b[0] = 99;
        int[] c = {1, 2, 3};
        System.out.println(a[0]);
        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a.equals(c));
    }
}
```

**Solution** — arrays are **reference types**. `b` and `a` point at the same array, so `b[0] = 99`
changes `a[0]`. `c` is a different array with the same contents. Arrays inherit `Object.equals`,
which is identity — so `a.equals(c)` is `false`.

**Output (exact):**

```
99
true
false
false
```

**Distractors** — `1`: assumes `b` is a copy. `a.equals(c)` as `true`: arrays do not override
`equals`; you must use `Arrays.equals(a, c)`.

---

### Q12 — Answer: `"00 10 20 "`

```java
public class Main {
    public static void main(String[] args) {
        outer:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (j == 1) continue outer;
                System.out.print(i + "" + j + " ");
            }
        }
    }
}
```

**Solution** — `continue outer` continues the **outer** loop, i.e. it advances `i` and restarts
`j`. So `j` is only ever 0.

| `i` | `j` | Action |
|---|---|---|
| 0 | 0 | print `00 ` |
| 0 | 1 | `continue outer` → `i` becomes 1 |
| 1 | 0 | print `10 ` |
| 1 | 1 | `continue outer` → `i` becomes 2 |
| 2 | 0 | print `20 ` |
| 2 | 1 | `continue outer` → `i` becomes 3 → loop ends |

**Output (exact):**

```
00 10 20 
```

**Distractors** — `"00 01 10 11 20 21 "`: that would be `continue` without the label, which only
advances `j`. `"00 10 20 21 "`: `j` never reaches 2.

## Quick rules

- Static init: superclass first. Instance init: superclass constructor **first**, child field
  initialisers after.
- Overloads: strict → boxing → varargs; most specific wins inside a phase.
- `&&` skips the right side only when the left is false; `||` only when the left is true.
- `i++ + ++i` with `i = 5` → `12`, `i` = 7.
- `Integer` −128..127 is cached → `==` works there and only there.
- String literals are interned; `new String(...)` is not.
- `switch` falls through; `default` is reached by falling into it.
- `char + int` is `int`; any `String` in the expression makes it concatenation.
- Arrays are compared by reference with `==` **and** with `equals`.

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Child instance init before parent constructor | Q1 | `super()` runs first |
| Varargs beating boxing | Q2 | Phase 2 comes before phase 3 |
| Widening reference beating an exact match | Q3 | An exact match (phase 1) beats phase 1 widening too |
| Short-circuit always skipping the right | Q4, Q5 | It skips conditionally |
| `Integer` 128 cached | Q7 | Cache ends at 127 |
| `switch` breaking automatically | Q9 | It falls through |
| `a.equals(c)` on arrays | Q11 | Arrays use identity equality |

## Checklist

- [ ] I can name the construct in each of the 12 questions.
- [ ] I got Q1, Q9, Q11 right without hesitating.
- [ ] I can state the exact output of Q9 including the trailing space.
- [ ] I can explain why `m(5)` picks `m(Integer)` but `m(5)` with only `m(Object)` + `m(int...)`
      picks `m(Object)`.
- [ ] I finished all 12 in under 20 minutes (≈ 100 s each).

## Related

- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Method resolution and short-circuit](../02-techniques/02-method-resolution-and-short-circuit.md)
- [Solved output set B](02-solved-output-set-b.md)
- [Output traps](../04-pitfalls/01-output-traps.md)
- [Output rules one-pager](../05-reference/01-output-rules-one-pager.md)
- [Topic overview](../README.md)
