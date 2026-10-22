# Java Static, Arrays & Threads — Question Bank

> Section 4 · Java · Static, Arrays & Threads · _30 questions · ~45 min_

**How to use this bank:** answer all questions on paper with a 90-second cap each. Answers +
brief reasoning at the bottom. Score yourself honestly.

---

## In one sentence

**These 30 questions are the highest-density block in the whole resource** — every one of them has
a single correct answer that you can derive in 90 seconds once you own the rules.

## Why the pre-test tests this

- `static`/`final`, collections, and threads are the three topics that most often appear with a
  **code block and four options**. No reading required — just recall.
- Thread output questions have a special structure: **the correct option is the guaranteed
  statement**. Meera freezes on these under time pressure; write the guaranteed facts down first,
  then match.
- Thread questions carry the most marks per minute of study. Learn the tables, not the theory.

## What this bank covers

| Block | Questions | The skill being tested |
|---|---|---|
| `static`, `final`, varargs, operators | Q1–Q10 | init order, constants, the `Integer` cache, overload phases |
| Arrays, `ArrayList`, loops | Q11–Q20 | the `remove` overload, list mutability, covariance, loop counts |
| Threads | Q21–Q30 | `start()` vs `run()`, guarantees, monitors, thread safety |

---

## Q1. What is printed?

```java
class A {
    static int x = 10;
    static { x += 5; }
    static int y = x * 2;
}
public class Main {
    public static void main(String[] args) {
        System.out.println(A.y);
    }
}
```

A. `20`
B. `30`
C. `15`
D. `10`

---

## Q2. Which of these is a **compile-time constant**?

A. `final int A = 10;`
B. `int B = 10;`
C. `final int C = someMethod();`
D. `final Object D = new Object();`

---

## Q3. What is printed?

```java
Integer a = 127, b = 127;
Integer c = 128, d = 128;
System.out.println((a == b) + " " + (c == d));
```

A. `true true`
B. `true false`
C. `false false`
D. `false true`

---

## Q4. What is printed?

```java
Integer x = 1, y = 2;
System.out.println(x + y);
```

A. `3`
B. `12`
C. A compile error
D. `null`

---

## Q5. Which overload does `m(5)` select?

```java
static void m(Object o) { }
static void m(double d) { }
static void m(Integer i) { }
static void m(long l) { }
static void m(int... x) { }
```

A. `m(Object)`
B. `m(double)`
C. `m(Integer)`
D. `m(long)`

---

## Q6. What is printed?

```java
public class Main {
    static void m(Object o) { System.out.print("O"); }
    static void m(String... s) { System.out.print("S"); }
    public static void main(String[] args) {
        m("hi");
        m((String) null);
    }
}
```

A. `OO`
B. `SS`
C. `OS`
D. `SO`

---

## Q7. What is printed?

```java
System.out.println(-7 / 2);
System.out.println(-7 % 2);
System.out.println(Math.round(-2.5));
```

A. `-3`, `-1`, `-2`
B. `-4`, `-1`, `-3`
C. `-3`, `1`, `-2`
D. `-4`, `1`, `-3`

---

## Q8. What is printed?

```java
int x = 5;
x += 1.9;
System.out.println(x);
```

A. `6`
B. `6.9`
C. `7`
D. A compile error — `double` cannot be added to `int`

---

## Q9. Which statement about a `final` variable is correct?

A. A `final` object's contents can never be modified
B. A `final` reference cannot be reassigned; the referenced object's contents may still change
C. A `final` variable must be initialised at its declaration
D. A `final` local variable cannot be captured by a lambda

---

## Q10. What is printed?

```java
public class Main {
    static void m(int... xs) { System.out.println(xs.length); }
    public static void main(String[] args) {
        m();
        m(1, 2, 3);
    }
}
```

A. `0` then `3`
B. `null` then `3`
C. `0` then `3` — but they print on one line
D. A compile error — varargs must have at least one argument

---

## Q11. What is printed?

```java
int[] a = {1, 2, 3};
System.out.println(a.length);
try {
    System.out.println(a[3]);
} catch (ArrayIndexOutOfBoundsException e) {
    System.out.println("OOB");
}
```

A. `3` then `OOB`
B. `3` then `3`
C. `OOB` then `3`
D. A compile error — the index is out of range

---

## Q12. What is printed?

```java
int[] a = {1, 2, 3};
System.out.println(a);
```

A. `[1, 2, 3]`
B. An identity string such as `[I@1b6d3586`
C. `null`
D. `1`

---

## Q13. What is printed?

```java
List<Integer> list = new ArrayList<>(Arrays.asList(10, 20, 30));
list.remove(1);
System.out.println(list);
```

A. `[20, 30]`
B. `[10, 30]`
C. `[10, 20]`
D. A compile error — ambiguous method call

---

## Q14. What is printed?

```java
List<String> list = Arrays.asList("a", "b");
list.set(0, "z");
System.out.println(list);
```

A. `[z, b]`
B. `[a, b]`
C. An `UnsupportedOperationException`
D. `[z, a, b]`

---

## Q15. What is printed?

```java
List<String> list = Arrays.asList("a", "b");
try {
    list.add("c");
} catch (UnsupportedOperationException e) {
    System.out.println("UOE");
}
```

A. `[a, b, c]`
B. `UOE`
C. Nothing — `add` silently fails
D. A compile error — `add` is not available on a fixed-size list

---

## Q16. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        Object[] o = new String[2];
        try {
            o[0] = new Object();
        } catch (ArrayStoreException e) {
            System.out.println("ASE");
        }
    }
}
```

A. Nothing — the assignment succeeds
B. `ASE`
C. A compile error — `String[]` cannot be assigned to `Object[]`
D. `NullPointerException`

---

## Q17. What is printed?

```java
int j = 0;
do {
    j++;
} while (j < 3);
System.out.println(j);
```

A. `2`
B. `3`
C. `4`
D. `0`

---

## Q18. What is printed?

```java
int sum = 0;
for (int i = 0; i < 5; i++) {
    if (i == 2) continue;
    sum += i;
}
System.out.println(sum);
```

A. `10`
B. `8`
C. `12`
D. An infinite loop — `continue` skips `i++`

---

## Q19. What is printed?

```java
String[] a = {"10", "9", "100"};
Arrays.sort(a);
System.out.println(a[0] + "," + a[2]);
```

A. `10,9`
B. `9,100`
C. `10,100`
D. `9,10`

---

## Q20. What is printed?

```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
        try {
            for (String s : list) {
                list.remove(s);
            }
        } catch (ConcurrentModificationException e) {
            System.out.println("CME");
        }
    }
}
```

A. Nothing — the loop removes every element
B. `CME`
C. A compile error — you cannot modify a list while iterating it
D. `UnsupportedOperationException`

---

## Q21. What is printed?

```java
Thread t = new Thread(() ->
    System.out.println(Thread.currentThread().getName()));
t.run();
```

A. `main`
B. `Thread-0`
C. `Thread-1`
D. A compile error — `run()` is not accessible from outside the class

---

## Q22. Which call actually **starts** a new thread?

A. `t.run()`
B. `t.start()`
C. `new Thread(t)`
D. `t.call()`

---

## Q23. How many values does the `Thread.State` enum have?

A. `4`
B. `5`
C. `6`
D. `7`

---

## Q24. What is printed, and in what order?

```java
Thread t = new Thread(() -> System.out.println("child"));
t.start();
t.join();
System.out.println("parent");
```

A. `parent` then `child`
B. `child` then `parent`, always
C. The order is not guaranteed
D. `child` then `parent`, but only if `t` has a higher priority

---

## Q25. Which statement is **guaranteed**?

```java
Thread a = new Thread(() -> System.out.println("A"));
Thread b = new Thread(() -> System.out.println("B"));
a.start();
b.start();
a.join();
b.join();
System.out.println("C");
```

A. `A`, `B`, `C` in that order
B. `B`, `A`, `C` in that order
C. `A` and `B` may appear in either order; `C` is always last
D. The order of `A`, `B`, and `C` is not guaranteed

---

## Q26. A shared counter field is declared `volatile`. Is `counter++` thread-safe?

A. Yes — `volatile` makes every read and write atomic
B. No — `volatile` gives visibility, but `counter++` is a read-modify-write
C. Yes — `volatile` writes are ordered, so updates cannot be lost
D. It depends on the number of threads

---

## Q27. Calling `wait()` on an object whose monitor the current thread does **not** hold results
in:

A. `IllegalMonitorStateException`
B. `InterruptedException`
C. The thread waits forever
D. `NullPointerException`

---

## Q28. Which of these is thread-safe?

A. `ArrayList`
B. `HashMap`
C. `StringBuilder`
D. `ConcurrentHashMap`

---

## Q29. What happens to a **daemon** thread when the last non-daemon thread finishes?

A. It keeps the JVM alive until it completes
B. It is terminated as the JVM shuts down
C. It is promoted to a normal (non-daemon) thread
D. It throws `IllegalThreadStateException`

---

## Q30. Which statement about `sleep()` and `wait()` is correct?

A. `sleep()` releases the lock; `wait()` keeps it
B. `sleep()` keeps the lock; `wait()` releases it
C. Both release the lock
D. Both keep the lock

---

# Answer key

| Q | Answer | Why (one line) |
|---|--------|----------------|
| 1 | B | `x = 10`, then the static block makes it 15, then `y = 15 * 2 = 30`. |
| 2 | A | A constant variable is `final` + primitive/`String` + a constant-expression initialiser. |
| 3 | B | 127 is inside the −128..127 `Integer` cache; 128 is outside it. |
| 4 | B | `+` with wrapper operands concatenates, so the result is the string `"12"`. |
| 5 | D | Widening primitive comes before boxing, and `int` → `long` is the nearest widening. |
| 6 | A | Phase 1 (widening reference) already matches `m(Object)` in both calls. |
| 7 | A | Division truncates toward zero (−3), `%` follows the dividend (−1), `round` is half up (−2). |
| 8 | A | `x += 1.9` is `x = (int)(x + 1.9)` = `(int)6.9` = 6. |
| 9 | B | `final` freezes the reference, not the object's contents. |
| 10 | A | Varargs with no arguments gives an empty array (`length` 0), not `null`. |
| 11 | A | The length is 3, and index 3 is outside `0..length-1`, so the exception is caught and `OOB` prints. |
| 12 | B | A raw array inherits `Object.toString()`, which prints the class name and identity hash. |
| 13 | B | `remove(1)` picks `remove(int)` — it removes **index 1**, the value `20`. |
| 14 | A | `set` replaces an element without changing the size, which a fixed-size list allows. |
| 15 | B | `Arrays.asList` is fixed-size, so `add` throws `UnsupportedOperationException`. |
| 16 | B | Arrays are covariant, so it compiles — but the runtime store check throws `ArrayStoreException`. |
| 17 | B | `do-while` runs the body first: 1, 2, 3 — then the condition fails. |
| 18 | B | `i == 2` is skipped, so the sum is 0 + 1 + 3 + 4 = 8; `i++` still runs. |
| 19 | A | `Arrays.sort` on strings is lexicographic: `"10"`, `"100"`, `"9"`. |
| 20 | B | The fail-fast iterator detects the structural modification and throws `ConcurrentModificationException`. |
| 21 | A | `run()` is an ordinary method call, so it executes on the calling thread (`main`). |
| 22 | B | Only `start()` asks the JVM to create and schedule a new thread. |
| 23 | C | NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED — six values. |
| 24 | B | `join()` blocks until `t` finishes, so `child` always prints before `parent`. |
| 25 | C | The `A`/`B` order is the scheduler's choice; `join()` guarantees `C` is last. |
| 26 | B | `volatile` guarantees visibility only — the read-modify-write can still lose an update. |
| 27 | A | `wait()` requires the monitor of the object it is called on. |
| 28 | D | `ConcurrentHashMap` is designed for concurrent use; the other three are not. |
| 29 | B | Daemon threads do not keep the JVM alive — they are killed at shutdown. |
| 30 | B | `sleep()` pauses the current thread while holding the lock; `wait()` releases it. |

---

## Related

- [10 — Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/)
- [11 — Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/)
- [12 — Threads Basics](../12-Threads-Basic/)
- [Part 1 — OOP & Core Java](./01-question-bank-part-1-oop-and-core.md)
- [Part 2 — Exceptions, Output & Strings](./02-question-bank-part-2-exceptions-output-strings.md)
- [Question bank overview](./README.md)
