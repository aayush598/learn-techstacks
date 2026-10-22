# Solved Set — Arrays, ArrayList & Loops

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 24 min_
> **Prerequisite:** [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)

## In one sentence

10 fully solved questions: array printing, `remove` overloads, `Arrays.asList` mutability, covariance,
`ConcurrentModificationException`, `continue` semantics, and `do-while`.

## Why the pre-test tests this

Every question here is in the exam's exact shape. The reason each wrong option is wrong is the
part that earns the mark — read it, don't just check the letter.

## Core concept

- `arr.length` is a **field**; a raw array's `toString()` prints `[I@hash`.
- `List.remove(int)` removes by **index**; `List.remove(Object)` removes by **value**.
- `Arrays.asList` is **fixed-size**; `List.of` is **immutable**.
- `continue` in a `for` loop still runs the update expression.
- Structural modification during a for-each → `ConcurrentModificationException`.

## Worked example

### Q1 — Printing an array

```java
int[] a = {1, 2, 3};
System.out.println(a);
System.out.println(Arrays.toString(a));
```

**Options**

| # | Option |
|---|---|
| A | `[1, 2, 3]` twice |
| B | `[I@1b6d3586` then `[1, 2, 3]` |
| C | `[1, 2, 3]` then `[I@1b6d3586` |
| D | A compile error: `toString` is not defined for arrays |

**Answer: B** — the first line prints the array's identity hash, the second prints the contents.

**Breakdown**

| Call | Why |
|---|---|
| `println(a)` | `a` is an `Object`, so `Object.toString()` runs → `getClass().getName() + "@" + hashCode()` → `[I@1b6d3586` (`[I` = the internal name of `int[]`) |
| `println(Arrays.toString(a))` | the utility method walks the array → `[1, 2, 3]` |

**Why not C:** the order is fixed by the source.
**Why not D:** `Object.toString()` is inherited by arrays.

---

### Q2 — The `remove` overload trap

```java
List<Integer> list = new ArrayList<>(Arrays.asList(10, 20, 30));
list.remove(1);
System.out.println(list);
```

**Options**

| # | Option |
|---|---|
| A | `[20, 30]` |
| B | `[10, 30]` |
| C | `[10, 20]` |
| D | A compile error: ambiguous method call |

**Answer: B** — `[10, 30]`.

**Breakdown**

| Step | Reasoning |
|---|---|
| 1 | The literal `1` is an `int`, so the compiler picks `remove(int index)` — no boxing needed, so phase 1 (strict) applies |
| 2 | The element at **index 1** is `20` |
| 3 | The list becomes `[10, 30]` |

**How to remove by value:** `list.remove(Integer.valueOf(1))` — the `Integer` argument forces
`remove(Object)`. Here no element equals `1`, so the list is unchanged.

**Why not A:** that would be `remove(0)`, which removes `10`.
**Why not D:** there is no ambiguity — `remove(int)` is applicable without boxing, so it wins.

---

### Q3 — `Arrays.asList` mutability

```java
List<String> list = Arrays.asList("a", "b");
try {
    list.add("c");
} catch (UnsupportedOperationException e) {
    System.out.println("UOE");
}
list.set(0, "z");
System.out.println(list);
```

**Options**

| # | Option |
|---|---|
| A | `UOE` then `[a, b]` |
| B | `UOE` then `[z, b]` |
| C | `[a, b, c]` |
| D | A compile error: `add` is not available on a fixed-size list |

**Answer: B** — `UOE` then `[z, b]`.

**Breakdown**

| Call | Result |
|---|---|
| `Arrays.asList("a", "b")` | a **fixed-size** list backed by the array |
| `list.add("c")` | throws `UnsupportedOperationException` → prints `UOE` |
| `list.set(0, "z")` | **legal** — replacing an existing element does not change the size → `["z", "b"]` |

**Why not C:** `add` throws; it does not append.
**Why not D:** `add` compiles — it throws at runtime.

---

### Q4 — Array covariance

```java
Object[] o = new String[2];
try {
    o[0] = new Object();
} catch (ArrayStoreException e) {
    System.out.println("ASE");
}
```

**Options**

| # | Option |
|---|---|
| A | A compile error: `String[]` cannot be assigned to `Object[]` |
| B | `ASE` |
| C | No output — the assignment succeeds |
| D | `NullPointerException` |

**Answer: B** — `ASE`.

**Breakdown**

| Step | Reasoning |
|---|---|
| 1 | `String[]` **is** a subtype of `Object[]` (arrays are covariant), so the assignment compiles |
| 2 | At runtime the array's real type is `String[]` |
| 3 | Storing an `Object` into a `String[]` fails the runtime store check → `ArrayStoreException` |

**Why not A:** covariance is exactly why this compiles.
**Why not C:** the check is real; it is what makes `ArrayStoreException` exist.

---

### Q5 — `ConcurrentModificationException`

```java
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
try {
    for (String s : list) {
        list.remove(s);
    }
} catch (ConcurrentModificationException e) {
    System.out.println("CME");
}
```

**Options**

| # | Option |
|---|---|
| A | No output — the loop completes |
| B | `CME` |
| C | A compile error: cannot remove from a list while iterating it |
| D | `UnsupportedOperationException` |

**Answer: B** — `CME`.

**Breakdown**

| Step | Reasoning |
|---|---|
| 1 | The for-each creates an `Iterator` over the list |
| 2 | Iteration 1: `s = "a"`, then `list.remove("a")` bumps the list's modification count |
| 3 | Iteration 2: `it.next()` sees the modification count changed and throws `ConcurrentModificationException` |

**Why not C:** removing during iteration is legal syntax; it fails at runtime.
**Why not D:** that is the `Arrays.asList` failure, not this one.
**Legal alternatives:** `list.removeIf(s -> true);` or an explicit `Iterator` with
`it.remove()`.

---

### Q6 — `continue` and the update expression

```java
int count = 0;
for (int i = 0; i < 5; i++) {
    if (i == 2) continue;
    count += i;
}
System.out.println(count);
```

**Options**

| # | Option |
|---|---|
| A | `10` |
| B | `8` |
| C | `12` |
| D | An infinite loop |

**Answer: B** — `8`.

**Breakdown**

| `i` | Action | `count` |
|---|---|---|
| 0 | add 0 | 0 |
| 1 | add 1 | 1 |
| 2 | `continue` — **but `i++` still runs** | 1 |
| 3 | add 3 | 4 |
| 4 | add 4 | 8 |

**Why not A:** `2` is never added.
**Why not D:** `continue` does not skip `i++` — the loop terminates normally.

---

### Q7 — `do-while`

```java
int j = 0;
do {
    j++;
} while (j < 3);
System.out.println(j);
```

**Options**

| # | Option |
|---|---|
| A | `2` |
| B | `3` |
| C | `4` |
| D | `0` |

**Answer: B** — `3`.

**Breakdown**

| Iteration | `j` after `j++` | `j < 3`? |
|---|---|---|
| 1 | 1 | true → repeat |
| 2 | 2 | true → repeat |
| 3 | 3 | false → exit |

**Why not A:** the body runs **before** the first check, so there are 3 iterations, not 2.
**Why not D:** `do-while` always runs at least once.

---

### Q8 — Labelled `break` vs `continue`

```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) break outer;
        if (i == 2) continue outer;
        System.out.print(i + "" + j);
    }
}
```

**Options**

| # | Option |
|---|---|
| A | `00` |
| B | `000102` |
| C | `00010212` |
| D | `001020` |

**Answer: A** — `00`.

**Breakdown**

| Step | Reasoning |
|---|---|
| 1 | `i=0`, `j=0`: `j == 1`? no. `i == 2`? no. → print `00` |
| 2 | `j=1`: `j == 1` → `break outer` → leaves **both** loops |

**Why not B:** `break outer` exits immediately at `j == 1`, so the loop never reaches `i = 1`.
**Why not C:** `continue outer` would restart the outer loop, but `break outer` fires first.

---

### Q9 — `length` and default values

```java
int[] a = new int[3];
a[1] = 7;
System.out.println(a.length);
System.out.println(a[0]);
System.out.println(a[2]);
```

**Options**

| # | Option |
|---|---|
| A | `3`, `7`, `0` |
| B | `3`, `0`, `0` |
| C | `3`, `0`, `ArrayIndexOutOfBoundsException` |
| D | A compile error: `length` is a method |

**Answer: A** — `3`, `7`, `0`.

**Breakdown**

| Expression | Value |
|---|---|
| `a.length` | `3` — the length is fixed at creation |
| `a[0]` | `0` — the default value for `int` |
| `a[2]` | `0` — also never assigned |

**Why not C:** index 2 is valid (`0..length-1`).
**Why not D:** `length` is a **field**, so `a.length` is correct; `a.length()` would not compile.

---

### Q10 — `Arrays.sort` on strings

```java
String[] a = {"10", "9", "100"};
Arrays.sort(a);
System.out.println(a[0]);
System.out.println(a[2]);
```

**Options**

| # | Option |
|---|---|
| A | `10` then `9` |
| B | `9` then `100` |
| C | `100` then `10` |
| D | `10` then `100` |

**Answer: A** — `10` then `9`.

**Breakdown**

`Arrays.sort` on a `String[]` sorts **lexicographically** (by character), not numerically:

| Comparison | Result |
|---|---|
| `"10"` vs `"100"` | `"10"` is a prefix → shorter first → `"10" < "100"` |
| `"10"` vs `"9"` | `'1'` (49) < `'9'` (57) → `"10" < "9"` |

So the sorted order is `["10", "100", "9"]`, giving `a[0] = "10"` and `a[2] = "9"`.

**Why not B:** `"9"` is the **largest** of the three, not the smallest.
**Why not D:** the array has three elements; `"100"` sits in the middle, not last.

## Quick rules

- `arr.length` is a field; `Arrays.toString(a)` prints the contents.
- `remove(int)` → index, `remove(Object)` → value.
- `Arrays.asList` → fixed size (`set` works, `add` throws); `List.of` → immutable.
- Arrays are covariant; storing the wrong type → `ArrayStoreException`.
- Structural modification during a for-each → `ConcurrentModificationException`.
- `continue` in a `for` loop still runs the update expression.
- `do-while` runs at least once.
- `break label;` exits the labelled loop; `continue label;` starts its next iteration.

## Common traps

| Trap | Where it appears |
|---|---|
| `remove(1)` removes the value | Q2 |
| `Arrays.asList` supports `add` | Q3 |
| `String[]` cannot be an `Object[]` | Q4 |
| Removing during a for-each is fine | Q5 |
| `continue` skips `i++` | Q6 |
| `do-while` with a false condition | Q7 |
| `break outer` continues the inner loop | Q8 |
| `Arrays.sort` on strings is numeric | Q10 |

## Checklist

- [ ] I know `length` is a field.
- [ ] I can pick `remove(int)` vs `remove(Object)` without hesitating.
- [ ] I know the three list-creation flavours and their mutability.
- [ ] I know why covariance causes `ArrayStoreException`.
- [ ] I know `continue` runs the update expression.
- [ ] I know the difference between `break label` and `continue label`.

## Related

- [Arrays and ArrayList](../01-concepts/01-arrays-and-arraylist.md)
- [Loops and iteration](../01-concepts/02-loops-and-iteration.md)
- [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)
- [Array and loop traps](../04-pitfalls/01-array-and-loop-traps.md)
- [Arrays and loops one-pager](../05-reference/01-arrays-loops-one-pager.md)
- [Topic overview](../README.md)
