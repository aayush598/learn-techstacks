# Arrays, ArrayList & Loops — One-Page Revision Sheet

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 5 min_
> **Prerequisite:** [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)

## In one sentence

Print this page and this topic collapses to **five tables**: the array toolbox, the `List` method
traps, list mutability, loop semantics, and the array/loop traps.

## Why the pre-test tests this

Array and loop questions are the most mechanical in Section 4 — and the most frequently missed,
because the traps are small and the options are close. Owning the tables is the whole game.

## Core concept

### Table 1 — the array toolbox

| I want | Method | Result for `{1, 2, 3}` |
|---|---|---|
| Print an array | `Arrays.toString(a)` | `[1, 2, 3]` |
| Print a nested array | `Arrays.deepToString(a)` | `[[1, 2], [3, 4]]` |
| The length | `a.length` | `3` (a **field**) |
| Sort | `Arrays.sort(a)` | in place, ascending |
| Compare contents | `Arrays.equals(a, b)` | `true` if same length and elements |
| Fill | `Arrays.fill(a, 0)` | `{0, 0, 0}` |
| Copy | `Arrays.copyOf(a, 5)` | length 5, padded with `0` |
| Copy a slice | `Arrays.copyOfRange(a, 0, 2)` | `{1, 2}` — end exclusive |
| Fixed-size list | `Arrays.asList(a)` | `set` works, `add` throws |
| Mutable list | `new ArrayList<>(Arrays.asList(a))` | fully mutable |
| Immutable list | `List.of(a)` | Java 9+, read-only |

### Table 2 — `List` methods on `[10, 20, 30]`

| Call | Reads as | Result |
|---|---|---|
| `remove(0)` | remove at **index** 0 | `[20, 30]` |
| `remove(1)` | remove at **index** 1 | `[10, 30]` |
| `remove(Integer.valueOf(10))` | remove the **value** `10` | `[20, 30]` |
| `remove(Integer.valueOf(1))` | remove the **value** `1` | unchanged |
| `get(0)` | element at index 0 | `10` |
| `set(0, 99)` | replace at index 0, returns the **old** value | `[99, 20, 30]` |
| `contains(10)` | membership by value | `true` |
| `indexOf(20)` | first index of the value | `1` |

### Table 3 — list mutability

| Created by | `add` / `remove` | `set` | Size fixed? |
|---|---|---|---|
| `new ArrayList<>(...)` | ✅ | ✅ | no |
| `Arrays.asList(a)` | ❌ `UnsupportedOperationException` | ✅ | yes |
| `List.of(...)` | ❌ `UnsupportedOperationException` | ❌ | yes |

### Table 4 — loop semantics

| Question | Answer |
|---|---|
| Which loops run at least once? | `do-while` only |
| What does `continue` skip? | the rest of the body |
| Does `continue` skip `i++` in a `for`? | **No** — the update still runs |
| What does `break` exit? | the **innermost** loop or `switch` |
| `break label;` | leaves the labelled loop |
| `continue label;` | the next iteration of the labelled loop |
| Modify a `Collection` in a for-each? | `ConcurrentModificationException` |
| Modify an `int[]` in a for-each? | allowed (no fail-fast check) |
| Legal removal during iteration | `removeIf(...)` or `Iterator.remove()` |

### Table 5 — array and list facts

| Fact | Value |
|---|---|
| Valid indices | `0 .. length-1` |
| Out of range | `ArrayIndexOutOfBoundsException` |
| Default `int` element | `0` |
| Default `boolean` element | `false` |
| Default `char` element | `'\u0000'` |
| Default object element | `null` |
| A raw array's `toString()` | `[I@1b6d3586` |
| A list's `toString()` | `[1, 2, 3]` |
| `new int[2][]` | 2 rows, each `null` → NPE on `a[0][0] = 1` |
| `Object[] o = new String[2]` | compiles (covariance) → `ArrayStoreException` on a bad store |
| `Arrays.sort` on `String[]` | lexicographic |
| `list.toArray()` | `Object[]` — use `toArray(new T[0])` |

### 60-second budget

| Phase | Seconds | Action |
|---|---|---|
| Classify | 10 | array? list? loop? |
| Table lookup | 20 | Tables 1–5 |
| Sanity check | 15 | `remove` overload, mutability, `continue` |
| Write | 15 | exact output |
| **Total** | **~60** | |

## Worked example

**Q. What is printed?**

```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        int[] a = {3, 1, 2};
        Arrays.sort(a);
        System.out.println(Arrays.toString(a));
        List<Integer> nums = new ArrayList<>(Arrays.asList(1, 2, 3));
        nums.remove(1);
        System.out.println(nums);
        int sum = 0;
        for (int x : nums) {
            if (x == 3) continue;
            sum += x;
        }
        System.out.println(sum);
    }
}
```

**Output (exact):**

```
[1, 2, 3]
[1, 3]
1
```

`remove(1)` removed **index 1** (the value `2`), leaving `[1, 3]`. The `for` loop then adds only
`1`, because `3` is skipped by the `continue`.

## Quick rules

- `arr.length` is a field; `Arrays.toString(a)` prints contents.
- `remove(int)` → index; `remove(Object)` → value.
- `Arrays.asList` → fixed size; `List.of` → immutable; `new ArrayList<>(...)` → mutable.
- Arrays are covariant → `ArrayStoreException` on a bad store.
- Structural modification during a for-each → `ConcurrentModificationException`.
- `continue` in a `for` loop still runs the update expression.
- `do-while` runs at least once.
- `break` exits only the innermost loop.

## Common traps

| Trap | Fix |
|---|---|
| `arr.length()` | It's a field |
| `list.remove(1)` removes the value | It removes index 1 |
| `Arrays.asList` supports `add` | Fixed size |
| `String[]` cannot be an `Object[]` | It can — then `ArrayStoreException` |
| Removing during a for-each is safe | `ConcurrentModificationException` |
| `continue` skips `i++` | It does not |
| `Arrays.sort` on strings is numeric | Lexicographic |

## Checklist

- [ ] I know `length` is a field.
- [ ] I know the `remove` overload table by heart.
- [ ] I know the three list mutability levels.
- [ ] I know the fail-fast rule and the legal alternatives.
- [ ] I know the loop-exit rules for `break`/`continue` with and without a label.

## Related

- [Arrays and ArrayList](../01-concepts/01-arrays-and-arraylist.md)
- [Loops and iteration](../01-concepts/02-loops-and-iteration.md)
- [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)
- [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)
- [Array and loop traps](../04-pitfalls/01-array-and-loop-traps.md)
- [Topic overview](../README.md)
