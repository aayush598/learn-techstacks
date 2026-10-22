# Loops and Iteration

> Section 4 · Java · Arrays, ArrayList & Loops · _Estimated reading time: 11 min_
> **Prerequisite:** [Arrays and ArrayList](01-arrays-and-arraylist.md)

## In one sentence

Five loop forms, three ways to leave a loop early (`break`, `continue`, labelled `break`), and one
rule that decides whether a for-each loop is legal: **the collection must not change structurally
during the iteration**.

## Why the pre-test tests this

- "What is printed?" questions that need you to count loop iterations are a recurring pattern.
- `do-while` runs **at least once** — the most common off-by-one in these questions.
- `continue` in a `for` loop still runs the **update expression**, but in a `while` loop it jumps
  straight to the condition. That difference decides the answer.

## Core concept

### The five loop forms

```java
for (int i = 0; i < n; i++) { }     // counted
for (int i : arr) { }               // for-each
while (cond) { }                    // pre-test
do { } while (cond);                // post-test — runs at least once
for (;;) { }                        // infinite
```

| Form | Condition checked | Minimum iterations |
|---|---|---|
| `for` | before the body | 0 |
| for-each | before the body | 0 |
| `while` | before the body | 0 |
| `do-while` | **after** the body | **1** |

### For-each — the rules

```java
for (String s : list) { }
for (int x : intArray) { }
```

| Rule | Detail |
|---|---|
| Works on | arrays and any `Iterable` (all `Collection` types) |
| Variable type | must match the element type — `for (int i : list)` does **not** compile for `List<String>` |
| Not available for | `Map` (a `Map` is not `Iterable`) — iterate `entrySet()` |
| Modification | adding or removing during the loop → `ConcurrentModificationException` |

**The autoboxing trap:**

```java
List<Integer> list = Arrays.asList(1, 2, 3);
for (int x : list) { }        // compiles — x is unboxed
for (Integer x : list) { }    // compiles — x is the element itself
```

### `break`, `continue`, and labels

| Statement | Effect |
|---|---|
| `break;` | exits the **innermost** enclosing loop or `switch` |
| `continue;` | skips to the **next iteration** of the innermost loop |
| `continue label;` | skips to the next iteration of the labelled loop |
| `break label;` | exits the labelled loop entirely |

```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) continue outer;   // next iteration of the OUTER loop
        if (i == 2) break outer;      // leaves the OUTER loop
        System.out.println(i + "" + j);
    }
}
```

**Labelled `continue` vs labelled `break`:**

| Statement | Where it goes next |
|---|---|
| `continue outer;` | the next iteration of the outer loop (the inner loop is abandoned) |
| `break outer;` | the statement **after** the outer loop |

### `continue` and the update expression

This is the classic trap. In a `for` loop, `continue` still runs the **update expression**:

```java
for (int i = 0; i < 5; i++) {
    if (i == 2) continue;
    System.out.print(i);
}
// prints 0134 — because i++ still runs when continue fires
```

In a `while` loop, `continue` jumps **straight to the condition**, so the body never updates the
counter unless you put the update inside the body.

```java
int i = 0;
while (i < 5) {
    if (i == 2) { i++; continue; }
    System.out.print(i);
    i++;
}
// prints 0134 — but only because the body updates i manually
```

### The for-each modification trap

```java
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
for (String s : list) {
    list.remove(s);          // ConcurrentModificationException on the 2nd iteration
}
```

The for-each loop uses an `Iterator` with a **fail-fast** check: it compares the list's
modification count before each step. `list.remove(s)` bumps the count, so the next
`next()` call throws `ConcurrentModificationException`.

**The two legal ways to remove during iteration:**

```java
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.equals("b")) it.remove();   // legal — Iterator.remove()
}
```

```java
list.removeIf(s -> s.equals("b"));    // Java 8+ — the idiomatic answer
```

**Modifying an array in a for-each is legal** — arrays do not have the fail-fast check. (It is
still usually a bug, but it will not throw.)

### Loop counters and the `for` header

```java
for (int i = 0, j = 10; i < j; i++, j--) { }
```

- Multiple variables of the same type may be declared.
- The update section may contain a comma-separated list.
- The three sections are all optional: `for (;;)` is an infinite loop.

### `switch` — the sibling of `break`

```java
switch (x) {
    case 1:  System.out.println("one"); break;
    case 2:
    case 3:  System.out.println("two or three"); break;
    default: System.out.println("other");
}
```

| Rule | Detail |
|---|---|
| `break` | without it, execution **falls through** to the next case |
| `case` labels | must be **compile-time constants** (or `String` literals, Java 7+) |
| type | `switch` on `String`, `enum`, or an integral type (`byte`, `short`, `int`, `char`) — **not** `long`, `float`, `double`, `boolean` |
| `default` | optional; may appear anywhere |

### Common loop output patterns

| Pattern | Result |
|---|---|
| `for (int i = 0; i <= 5; i++)` | 6 iterations (`0..5`) |
| `for (int i = 5; i > 0; i--)` | 5 iterations (`5..1`) |
| `for (int i = 0; i < 5; i++)` with `continue` at `i == 2` | 5 iterations, output skips `2` |
| `do { } while (false);` | 1 iteration |
| `while (false) { }` | 0 iterations |

## Worked example

**Q. What is printed?**

```java
public class Main {
    public static void main(String[] args) {
        int count = 0;
        for (int i = 0; i < 5; i++) {
            if (i == 2) continue;
            count += i;
        }
        System.out.println(count);
        int j = 0;
        do {
            j++;
        } while (j < 3);
        System.out.println(j);
        outer:
        for (int a = 0; a < 3; a++) {
            for (int b = 0; b < 3; b++) {
                if (b == 1) break outer;
                System.out.print(a + "" + b);
            }
        }
    }
}
```

**Solution**

| Part | Reasoning | Result |
|---|---|---|
| `count` | `i` runs 0,1,2,3,4. `i == 2` is skipped by `continue`, but `i++` still runs. `count` = 0+1+3+4 = 8 | `8` |
| `j` | `do-while` runs at least once: j=1 (1<3 true), j=2 (true), j=3 (3<3 false → stop) | `3` |
| labelled loop | `a=0`, `b=0` → print `00`; `b=1` → `break outer` exits **both** loops | `00` |

**Output (exact):**

```
8
3
00
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `10` for `count` | `i == 2` is skipped, so 2 is not added |
| `2` for `j` | The body runs before the condition, so `j` reaches 3 |
| `000102` for the loop | `break outer` leaves everything after the first row |

## Quick rules

- `do-while` runs **at least once**.
- `continue` in a `for` loop still runs the update expression.
- `break` exits only the **innermost** loop; `break label;` exits the labelled one.
- `continue label;` moves to the next iteration of the labelled loop.
- For-each over a `Collection` throws `ConcurrentModificationException` if the collection is
  structurally modified during the loop.
- `list.remove(int)` → index; `list.remove(Object)` → value.
- `switch` needs `break` to avoid fall-through; `case` labels must be compile-time constants.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| `do-while` with a false condition | 0 iterations | 1 iteration |
| `continue` skips `i++` | the loop freezes | `i++` still runs |
| `break` inside a nested loop | exits both | exits only the inner one |
| Removing from a list in a for-each | works | `ConcurrentModificationException` |
| `switch` on a `long` | compiles | Only `byte`/`short`/`int`/`char`/`String`/`enum` |

## Checklist

- [ ] I know which loops run at least once.
- [ ] I know exactly what `continue` does in a `for` header.
- [ ] I know the difference between `break label` and `continue label`.
- [ ] I know why removing from a list inside a for-each throws.
- [ ] I know the legal way to remove during iteration.

## Related

- [Arrays and ArrayList](01-arrays-and-arraylist.md)
- [Choosing the right collection and loop](../02-techniques/01-choosing-the-right-collection-and-loop.md)
- [Solved arrays and loops set](../03-worked-examples/01-solved-arrays-loops-set.md)
- [Array and loop traps](../04-pitfalls/01-array-and-loop-traps.md)
- [Arrays and loops one-pager](../05-reference/01-arrays-loops-one-pager.md)
- [Topic overview](../README.md)
