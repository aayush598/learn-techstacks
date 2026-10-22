# Choosing the Right Collection and Loop

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 9 min_
> **Prerequisite:** [Arrays and ArrayList](../01-concepts/01-arrays-and-arraylist.md)

## In one sentence

Two lookup tables — **which container** and **which loop** — plus a 60-second procedure that maps
the question's intent to the exact method.

## Why the pre-test tests this

Most Section 4 questions of this shape are "which method/loop does this?" — and they have exactly
one defensible answer. A table turns a guess into a lookup.

## Core concept

### Table 1 — which container?

| Need | Use | Complexity of the key operation |
|---|---|---|
| Fixed size, known at compile time, primitives | `int[]` | O(1) get |
| Growable list of objects | `ArrayList` | O(1) get, O(n) middle insert |
| Cheap insert/delete in the middle when you hold the node | `LinkedList` | O(n) get, O(1) insert |
| Unique elements, fast membership test | `HashSet` | O(1) average contains |
| Sorted unique elements | `TreeSet` | O(log n) contains |
| Key → value lookup | `HashMap` | O(1) average get |
| Sorted key → value | `TreeMap` | O(log n) get |
| Thread-safe list / map | `Collections.synchronizedList(...)` | same, with locking |
| Concurrent mutations | `CopyOnWriteArrayList` | O(n) write |
| Insertion-order + unique | `LinkedHashSet` | O(1) average contains |
| Immutable list | `List.of(...)` | read-only |

**Never use `Vector` in new code** — it is the legacy synchronised `ArrayList`, and its
synchronisation is on every method, not on compound operations.

### Table 2 — which loop?

| Situation | Use | Why |
|---|---|---|
| Index needed, or iterating backwards | indexed `for` | only this form gives you the index |
| Iterate every element of an array or `Collection` | for-each | no index boilerplate |
| Unknown iteration count, condition checked first | `while` | |
| The body must run **at least once** | `do-while` | |
| Repeat until a condition becomes false | `while` with the condition inverted | |
| Iterate a `Map` | `for (Map.Entry<K,V> e : map.entrySet())` | a `Map` is not `Iterable` |
| Remove during iteration | `removeIf` or `Iterator.remove()` | for-each throws |
| Process in parallel | `stream().parallel()` (Java 8+) | |

### Table 3 — the `List` method trap table

| Call | Reads as | On `[10, 20, 30]` |
|---|---|---|
| `list.remove(0)` | remove at **index** 0 | `[20, 30]` |
| `list.remove(Integer.valueOf(0))` | remove the **value** `0` | unchanged |
| `list.get(0)` | element at index 0 | `10` |
| `list.set(0, 99)` | replace at index 0, returns the **old** value | `[99, 20, 30]`, returns `10` |
| `list.contains(10)` | membership by value | `true` |
| `list.indexOf(20)` | first index of the value | `1` |
| `list.add(0, 5)` | insert at index 0, shifting right | `[5, 10, 20, 30]` |

### Table 4 — the array toolbox

| I want | Method | Output for `{1, 2, 3}` |
|---|---|---|
| Print an array readably | `Arrays.toString(a)` | `[1, 2, 3]` |
| Print a nested array | `Arrays.deepToString(a)` | `[[1, 2], [3, 4]]` |
| Sort ascending | `Arrays.sort(a)` | in place |
| Sort a `String[]` | `Arrays.sort(a)` | lexicographic |
| Compare contents | `Arrays.equals(a, b)` | `true` if same length and elements |
| Fill with a value | `Arrays.fill(a, 0)` | `{0, 0, 0}` |
| Copy into a new array | `Arrays.copyOf(a, 5)` | length 5, last two are `0` |
| Copy a slice | `Arrays.copyOfRange(a, 0, 2)` | `{1, 2}` — end is exclusive |
| Turn into a fixed-size list | `Arrays.asList(a)` | `set` works, `add` throws |
| Turn into a mutable list | `new ArrayList<>(Arrays.asList(a))` | fully mutable |
| Turn into an immutable list | `List.of(a)` | Java 9+ |

### Table 5 — sorting behaviour

| Array type | `Arrays.sort` result for `{3, 1, 2}` | Note |
|---|---|---|
| `int[]` | `{1, 2, 3}` | numeric |
| `Integer[]` | `{1, 2, 3}` | numeric |
| `String[]` | `{"1", "2", "3"}` | lexicographic |
| `String[]` = `{"10", "9"}` | `{"10", "9"}` | `"10" < "9"` lexicographically |
| `char[]` | ascending by code point | |
| `Object[]` with mixed types | `ClassCastException` | the elements are not comparable |

### The 60-second procedure

1. **Read the question's verb.** "Print", "insert", "remove", "compare", "sort", "iterate".
2. **Is it a container question?** → Table 1.
3. **Is it a loop question?** → Table 2.
4. **Is it a `List` method question?** → Table 3.
5. **Is it an array utility question?** → Table 4.
6. **Is it a sort question?** → Table 5.
7. **Check the version.** `List.of` is Java 9+, `removeIf` is Java 8+, `stream()` is Java 8+.

## Worked example

**Q. What is printed?**

```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        String[] words = {"banana", "apple", "cherry"};
        Arrays.sort(words);
        System.out.println(words[0]);
        List<String> list = new ArrayList<>(Arrays.asList(words));
        list.set(0, "date");
        System.out.println(list);
        List<Integer> nums = new ArrayList<>(Arrays.asList(1, 2, 3));
        nums.remove(Integer.valueOf(1));
        System.out.println(nums);
        System.out.println(nums.contains(1));
    }
}
```

**Solution**

| Step | Statement | Effect |
|---|---|---|
| 1 | `Arrays.sort(words)` | `{"apple", "banana", "cherry"}` — lexicographic |
| 2 | `words[0]` | `"apple"` |
| 3 | `new ArrayList<>(Arrays.asList(words))` | a **mutable** copy: `["apple", "banana", "cherry"]` |
| 4 | `list.set(0, "date")` | replaces index 0 → `["date", "banana", "cherry"]` |
| 5 | `nums.remove(Integer.valueOf(1))` | `remove(Object)` → removes the **value** `1` → `[2, 3]` |
| 6 | `nums.contains(1)` | `false` — the value `1` is gone |

**Output (exact):**

```
apple
[date, banana, cherry]
[2, 3]
false
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `banana` | Sorting is ascending, so `apple` is first |
| `[date, banana, cherry]` vs `[banana, date, cherry]` | `set(0, ...)` replaces **index 0** |
| `[1, 2, 3]` | `remove(Integer.valueOf(1))` removed the value |
| `true` for `contains(1)` | The value was removed |

## Quick rules

- `ArrayList` unless you need a specific `LinkedList` benefit.
- `Arrays.toString` for arrays, `toString()` for lists.
- `remove(int)` → index, `remove(Object)` → value.
- `set(i, v)` returns the **old** value.
- `Arrays.asList` → fixed size; `List.of` → immutable; `new ArrayList<>(...)` → mutable.
- For-each cannot modify the collection structurally.
- `break` = innermost loop; `continue` = next iteration; `continue` still runs the `for` update.

## Common traps

| Trap | Fix |
|---|---|
| `list.remove(1)` removes the value | It removes index 1 |
| `Arrays.asList` supports `add` | Fixed size |
| `Arrays.sort` on `String[]` is numeric | Lexicographic |
| Removing from a list in a for-each is safe | `ConcurrentModificationException` |
| `continue` skips `i++` | It does not |

## Checklist

- [ ] I can pick the right container for a stated need.
- [ ] I can pick the right loop for a stated situation.
- [ ] I know the `remove` overload trap cold.
- [ ] I know the `Arrays` toolbox.
- [ ] I know `Arrays.asList` vs `List.of` vs `new ArrayList<>`.

## Related

- [Arrays and ArrayList](../01-concepts/01-arrays-and-arraylist.md)
- [Loops and iteration](../01-concepts/02-loops-and-iteration.md)
- [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)
- [Array and loop traps](../04-pitfalls/01-array-and-loop-traps.md)
- [Arrays and loops one-pager](../05-reference/01-arrays-loops-one-pager.md)
- [Topic overview](../README.md)
