# Arrays and ArrayList

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 12 min_
> **Prerequisite:** none

## In one sentence

An **array** has a fixed `length` and one element type; an `ArrayList` has a **growable** size and
generic element types — and the bridge between them (`Arrays.asList`, `toArray`) is where the
traps live.

## Why the pre-test tests this

- "What does `arr.toString()` print?" → `[I@1b6d3586` for a raw array vs `[1, 2, 3]` for a list.
- "What is printed after `list.remove(1)`?" → the classic **remove-by-index** trap.
- Array covariance and `ArrayStoreException` are standard 4-option questions.

## Core concept

### Array basics

```java
int[] a = new int[5];        // 5 zeros
int[] b = {1, 2, 3};          // shortcut, local or field initialiser
int[] c = new int[]{1, 2, 3}; // same as b, but usable anywhere an expression is allowed
int[][] d = new int[2][3];    // 2 rows × 3 columns
int[][] e = {{1, 2}, {3, 4}}; // 2×2
int[][] f = new int[2][];     // jagged: rows exist, each is null
```

| Fact | Detail |
|---|---|
| Length | fixed at creation, **never** changes |
| Access | `a.length` is a **field**, not a method — `a.length()` is a compile error |
| Default values | `int`→0, `long`→0L, `double`→0.0, `char`→`'\u0000'`, `boolean`→false, objects→`null` |
| Bounds | valid indices `0 .. length-1`; otherwise `ArrayIndexOutOfBoundsException` |
| Element type | one type for the whole array — no mixed types |

**`length` is not a method.** `arr.length` works; `arr.length()` does not compile.

**Jagged arrays and `NullPointerException`:**

```java
int[][] f = new int[2][];
System.out.println(f.length);    // 2
System.out.println(f[0]);        // null
f[0][0] = 5;                     // NullPointerException — f[0] is null
```

### Array covariance — the dangerous rule

Java arrays are **covariant**: `String[]` is a subtype of `Object[]`.

```java
Object[] o = new String[3];   // compiles!
o[0] = "hi";                   // fine — a String is allowed
o[0] = new Object();           // ArrayStoreException at runtime
```

The compiler trusts the *declared* type; the runtime checks the *actual* array type. This is why
`Object[]` is not a safe general-purpose array.

### `java.util.Arrays` — the method table

| Method | What it does | Gotcha |
|---|---|---|
| `Arrays.toString(a)` | `[1, 2, 3]` for any array | A raw `int[]`'s own `toString()` gives `[I@hash` |
| `Arrays.deepToString(a)` | `[[1, 2], [3, 4]]` for nested arrays | |
| `Arrays.sort(a)` | sorts in place, ascending | `String[]` sorts **lexicographically**: `["10", "9"]` |
| `Arrays.sort(a, from, to)` | sorts a range | the range is `[from, to)` |
| `Arrays.equals(a, b)` | `true` if the same length and equal elements | for `int[]` this compares values |
| `Arrays.deepEquals(a, b)` | nested version | |
| `Arrays.fill(a, 7)` | sets every element to `7` | |
| `Arrays.copyOf(a, n)` | new array of length `n`, padded with `0`/`null` | |
| `Arrays.copyOfRange(a, 0, 2)` | copies `a[0]` and `a[1]` | end is exclusive |
| `Arrays.asList(a)` | a **fixed-size** `List` backed by `a` | `add`/`remove` throw `UnsupportedOperationException`; `set` works |
| `Arrays.asList(1, 2, 3)` | a fixed-size list of those values | |
| `Arrays.stream(a)` | an `IntStream` (primitives) | Java 8+ |
| `Arrays.binarySearch(a, key)` | index of `key`, or `-(insertion point) - 1` | the array must already be sorted |

**`Arrays.toString` vs `toString`:**

```java
int[] a = {1, 2, 3};
System.out.println(a);                    // [I@1b6d3586   (identity hash)
System.out.println(Arrays.toString(a));   // [1, 2, 3]
System.out.println(Arrays.deepToString(new int[][]{{1,2},{3,4}}));  // [[1, 2], [3, 4]]
```

### `ArrayList` basics

```java
List<Integer> list = new ArrayList<>();
list.add(10);          // add to the end
list.add(0, 5);        // insert at index 0 — later elements shift right
list.get(0);           // read
list.set(0, 7);        // replace — returns the OLD element
list.remove(0);        // ⚠ removes by INDEX for a `List<Integer>`
list.remove(Integer.valueOf(0));  // removes by VALUE
list.contains(5);      // by value, autoboxes the argument
list.size();
list.isEmpty();
list.indexOf(5);
list.clear();
```

**The `remove` overload trap:**

| Call | Which overload | Effect on `[10, 20, 30]` |
|---|---|---|
| `list.remove(0)` | `remove(int index)` | removes the **first** element → `[20, 30]` |
| `list.remove(Integer.valueOf(0))` | `remove(Object)` | removes the element equal to `0` → no match → unchanged |
| `list.remove(Integer.valueOf(20))` | `remove(Object)` | removes `20` → `[10, 30]` |

The compiler picks `remove(int)` for a literal `int` argument, because the literal is exactly an
`int` — no boxing needed.

### ArrayList vs LinkedList vs Vector

| | `ArrayList` | `LinkedList` | `Vector` |
|---|---|---|---|
| Backed by | dynamic array | doubly linked list | dynamic array |
| `get(i)` | **O(1)** | **O(n)** | O(1) |
| Insert/remove at the end | amortised O(1) | O(1) | O(1) |
| Insert/remove in the middle | O(n) (shift) | O(1) if you have the node | O(n) |
| Thread-safe | ❌ | ❌ | ✅ (synchronized) |
| `RandomAccess` | ✅ | ❌ | ✅ |
| Iterator fail-fast | ✅ | ✅ | ✅ |

**Rule:** use `ArrayList` unless you need cheap insertion in the middle with a known node, or you
need `ListIterator.add/remove` at the current position. Indexed access on a `LinkedList` is a
classic performance trap.

### `Arrays.asList` vs `List.of` vs `new ArrayList<>()`

| Created by | Mutable? | `add` / `remove` | `set` | Size fixed? |
|---|---|---|---|---|
| `new ArrayList<>(...)` | ✅ fully mutable | ✅ | ✅ | grows |
| `Arrays.asList(a)` | ⚠ partially | ❌ `UnsupportedOperationException` | ✅ | yes, fixed to the array's length |
| `List.of(...)` (Java 9+) | ❌ immutable | ❌ `UnsupportedOperationException` | ❌ | yes |

```java
List<String> l = Arrays.asList("a", "b");
l.set(0, "z");   // legal
l.add("c");     // UnsupportedOperationException
l.remove("a");  // UnsupportedOperationException
```

### Converting between arrays and lists

| Direction | Code | Note |
|---|---|---|
| array → list | `Arrays.asList(a)` | fixed size, backed by `a` |
| array → list | `new ArrayList<>(Arrays.asList(a))` | fully mutable |
| array → list | `List.of(a)` | immutable, Java 9+ |
| list → array | `list.toArray()` | an `Object[]` |
| list → array | `list.toArray(new String[0])` | a `String[]` — the recommended form |
| list → array | `list.toArray(new String[list.size()])` | also correct |

`list.toArray()` returns an `Object[]`, so `String[] s = list.toArray();` does **not** compile.

## Worked example

**Q. What is printed?**

```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));
        list.remove(1);
        list.remove(Integer.valueOf(2));
        System.out.println(list);
        System.out.println(a.length);
        System.out.println(Arrays.toString(a));
        Object[] o = new String[2];
        try {
            o[0] = new Object();
        } catch (ArrayStoreException e) {
            System.out.println("ASE");
        }
    }
}
```

**Solution**

| Step | Statement | Effect |
|---|---|---|
| 1 | `new ArrayList<>(Arrays.asList(1, 2, 3))` | a **mutable** copy: `[1, 2, 3]` |
| 2 | `list.remove(1)` | `remove(int)` → removes **index 1** → `[1, 3]` |
| 3 | `list.remove(Integer.valueOf(2))` | `remove(Object)` → no element equals `2` → `[1, 3]` |
| 4 | `println(list)` | prints `[1, 3]` |
| 5 | `a.length` | `3` |
| 6 | `Arrays.toString(a)` | `[1, 2, 3]` |
| 7 | `o = new String[2]` | the array's real type is `String[]` |
| 8 | `o[0] = new Object()` | runtime check fails → `ArrayStoreException` → prints `ASE` |

**Output (exact):**

```
[1, 3]
3
[1, 2, 3]
ASE
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `[2, 3]` | `remove(1)` removed the **index**, not the value |
| `[1, 2]` | `remove(1)` removed the value `1` |
| `[I@hash` for `a` | `Arrays.toString(a)` was used, not `a.toString()` |
| No `ASE` printed | The runtime array type is `String[]`, so storing an `Object` throws |

## Quick rules

- `arr.length` is a field; `arr.length()` does not compile.
- Array length never changes; `ArrayIndexOutOfBoundsException` outside `0..length-1`.
- Arrays are covariant → `Object[] o = new String[3]` compiles, but storing an `Object` throws
  `ArrayStoreException`.
- `Arrays.toString(a)` → `[1, 2, 3]`; a raw array's `toString()` → `[I@hash`.
- `Arrays.sort` on `String[]` is lexicographic.
- `List.remove(int)` removes by **index**; `List.remove(Object)` removes by **value**.
- `Arrays.asList` is fixed-size; `List.of` is immutable; `new ArrayList<>(...)` is fully mutable.
- `ArrayList.get(i)` is O(1); `LinkedList.get(i)` is O(n).
- `list.toArray()` gives an `Object[]`; use `toArray(new T[0])` for a typed array.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| `arr.length()` | compiles | It's a field |
| `Arrays.asList` is mutable | you can `add` | Fixed size |
| `list.remove(1)` removes the value `1` | `[2, 3]` | It removes index 1 |
| `Arrays.sort` on `String[]` sorts numerically | `["2", "10"]` | Lexicographic → `["10", "2"]` |
| `list.toArray()` returns `String[]` | compiles | It returns `Object[]` |

## Checklist

- [ ] I know `length` is a field.
- [ ] I know the default values of every primitive array type.
- [ ] I know why `Object[] o = new String[2]` compiles but throws at runtime.
- [ ] I know `remove(int)` vs `remove(Object)`.
- [ ] I know `Arrays.asList` vs `List.of` vs `new ArrayList<>`.
- [ ] I know `ArrayList` vs `LinkedList` complexity.

## Related

- [Loops and iteration](02-loops-and-iteration.md)
- [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)
- [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)
- [Array and loop traps](../04-pitfalls/01-array-and-loop-traps.md)
- [Arrays and loops one-pager](../05-reference/01-arrays-loops-one-pager.md)
- [Topic overview](../README.md)
