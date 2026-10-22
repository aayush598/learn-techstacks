# Java OOP & Core — Question Bank

> Section 4 · Java · OOP & Core Java · _30 questions · ~45 min_

**How to use this bank:** answer all questions on paper with a 90-second cap each. Answers +
brief reasoning at the bottom. Score yourself honestly.

---

## In one sentence

**The 30 questions below are the OOP and core-Java skeleton of Section 4** — inheritance,
polymorphism, interfaces, constructors, and the collections you will actually be asked about.

## Why the pre-test tests this

- Section 4 is **25 questions in ~35 minutes**. OOP fundamentals usually take 6–8 of those
  questions, and they are the most predictable points in the paper.
- Every OOP question reduces to one of four questions: *which method runs?*, *what is the access
  level?*, *does this compile?*, or *what does it print?*
- Rahul — strong in Java, weak in English — loses marks here by reading the stem too slowly. Use
  the 90-second rule: read the stem, read the code, pick the answer, move on.

## What this bank covers

| Block | Questions | The skill being tested |
|---|---|---|
| OOP principles | Q1–Q6 | access levels, class hierarchies, `super`/`this`, interfaces |
| Classes, objects, constructors | Q7–Q12 | constructor chaining, `static` vs instance, `final` |
| Inheritance and polymorphism | Q13–Q18 | dynamic dispatch, method hiding, `instanceof` |
| Interfaces, abstract classes, inner classes | Q19–Q24 | abstract vs interface, anonymous classes, lambdas |
| Collections framework | Q25–Q30 | `HashMap`, `HashSet`, `List`, `Comparator`, `TreeMap` |

---

## Q1. Which access modifier allows a member to be reached from the same package **and** from
subclasses in other packages, but not from unrelated classes in other packages?

A. `private`
B. `protected`
C. `public`
D. package-private (the default)

---

## Q2. Which class declaration is legal in Java?

A. `class C extends A, B { }`
B. `class C extends A implements I1, I2 { }`
C. `class C implements I1 extends A { }`
D. `class C implements I1, I2, I1 { }`

---

## Q3. What is printed?

```java
class A { void m() { System.out.println("A"); } }
class B extends A { void m() { System.out.println("B"); } }
public class Main {
    public static void main(String[] args) {
        A a = new B();
        a.m();
    }
}
```

A. `A`
B. `B`
C. A compile error
D. Both `A` and `B`

---

## Q4. Which use of `super` is valid?

A. `super.m();` — to call the superclass's `m()`
B. `super.x = 5;` — to assign a `private` field of the superclass
C. `super = new A();`
D. `this = super;`

---

## Q5. Which statement about a Java `interface` is correct?

A. Every method must be abstract and it cannot contain fields
B. Every method must be abstract but it can contain constants
C. It can contain `default` and `static` methods as well as constants
D. A class implements an interface using `extends`

---

## Q6. What is printed?

```java
abstract class Shape {
    abstract double area();
}
class Circle extends Shape {
    double area() { return 3.14; }
}
public class Main {
    public static void main(String[] args) {
        Shape s = new Circle();
        System.out.println(s.area());
    }
}
```

A. `3.14`
B. `0.0`
C. A compile error — `area()` is abstract
D. `Shape`

---

## Q7. What is printed?

```java
class Counter {
    int count;
    Counter() { count = 1; }
    Counter(int c) { this(); count = c; }
}
public class Main {
    public static void main(String[] args) {
        System.out.println(new Counter(5).count);
    }
}
```

A. `1`
B. `5`
C. A compile error — `this()` and `count = c` cannot both appear
D. `0`

---

## Q8. How many times is the constructor body executed in this code?

```java
class A {
    static int s = 0;
    int i = 0;
    A() { s++; i++; }
}
public class Main {
    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new A();
        System.out.println(A.s);
    }
}
```

A. `0`
B. `1`
C. `2`
D. `4` — two per object

---

## Q9. What modifiers does a field declared inside an interface have by default?

A. `public static final`
B. `public final`
C. `static`
D. `protected static final`

---

## Q10. Which code fails to compile?

```java
class A { final void m() { } }
class B extends A { void m() { } }
```

A. `B` — it cannot override the `final` method `m()` in `A`
B. `B` — `m()` in `A` has no body
C. Neither — it is legal
D. `A` — a `final` method must be `static`

---

## Q11. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        Object o = null;
        System.out.println(o instanceof String);
    }
}
```

A. `true`
B. `false`
C. `NullPointerException`
D. A compile error — `instanceof` cannot be used with `null`

---

## Q12. What does this class demonstrate?

```java
class A {
    void m(int x) { }
    void m(double x) { }
    void m(String x) { }
    void m(int x, int y) { }
}
```

A. Method overriding — the four methods override each other
B. Method overloading — four distinct methods sharing one name
C. Method hiding — only the last method exists
D. A compile error — a class cannot declare four methods with the same name

---

## Q13. What is printed?

```java
class A { static void m() { System.out.println("A"); } }
class B extends A { static void m() { System.out.println("B"); } }
public class Main {
    public static void main(String[] args) {
        A a = new B();
        a.m();
    }
}
```

A. `A`
B. `B`
C. A compile error
D. Both `A` and `B`

---

## Q14. Which of these compiles?

```java
final int x = 10;
Runnable r = () -> System.out.println(x);
```

A. It compiles — a `final` local can be captured by a lambda
B. A compile error — only `final` **fields** can be captured
C. A compile error — lambdas cannot capture local variables
D. It compiles only if `x` is declared `static`

---

## Q15. What is printed?

```java
public class Main {
    public static void main(String[] args) {
        Runnable r = new Runnable() {
            public void run() { System.out.println("run"); }
        };
        r.run();
    }
}
```

A. `run`
B. `Runnable@1b6d3586`
C. Nothing — the body runs only on a new thread
D. A compile error — an anonymous class needs a name

---

## Q16. In what order does a `HashMap` iterate over its entries?

A. Insertion order
B. Sorted by key
C. Not specified — it follows the hash buckets
D. Reverse insertion order

---

## Q17. A class `Employee` overrides `equals()` but **not** `hashCode()`. What happens when two
`Employee` objects with the same field values are added to a `HashSet`?

A. The set keeps only one — `equals()` alone is enough
B. The set may keep both — the inherited `hashCode()` can put them in different buckets
C. A compile error — `hashCode()` must be overridden when `equals()` is
D. `equals()` is ignored by `HashSet`

---

## Q18. Which operation is **O(n)** on a `LinkedList`?

A. `addFirst(e)`
B. `get(i)`
C. `size()`
D. `removeFirst()`

---

## Q19. Which iteration gives you **both** the key and the value of a `Map`?

A. `for (Map.Entry<K, V> e : map.entrySet())`
B. `for (K k : map.keySet())`
C. `for (V v : map.values())`
D. `for (Object o : map)`

---

## Q20. Which interface lets a class define its **own natural ordering**?

A. `Comparator`
B. `Comparable`
C. `Iterable`
D. `Serializable`

---

## Q21. What does `Collections.unmodifiableList(list).add("x")` do?

A. Adds `"x"` to the list
B. Throws `UnsupportedOperationException`
C. Returns `false` and changes nothing
D. Silently ignores the call

---

## Q22. What does a `TreeMap` use to order its keys?

A. `hashCode()`
B. The key's natural ordering (`compareTo`) or a supplied `Comparator`
C. Insertion order
D. `equals()`

---

## Q23. Why is `StringBuilder` preferred over `String` in a loop that appends 10,000 times?

A. `String` is mutable and `StringBuilder` is not
B. `String` is immutable, so each `+` allocates a new object; `StringBuilder` mutates in place
C. `StringBuilder` is thread-safe, so it is faster
D. `+` on a `String` is a compile error

---

## Q24. What is the default access level of a class member with no modifier?

A. `private`
B. `protected`
C. `public`
D. Package-private — visible only within the same package

---

## Q25. Where must a `super(...)` call appear in a subclass constructor?

A. It must be the **first** statement
B. It can appear anywhere in the body
C. It can be first, but then `this()` may not also be used
D. It is optional and, when present, must be last

---

## Q26. `class C implements I1, I2` and **both** `I1` and `I2` declare `void m()`. What must `C`
do?

A. Nothing — Java picks one of them
B. Override `m()` to resolve the conflict
C. Be declared `abstract`
D. It does not compile unless `m()` is `static`

---

## Q27. Given `Object o = "hello";`, what is required to assign it to a `String` variable?

A. Nothing — `String s = o;` compiles
B. A cast — `String s = (String) o;`
C. `o.toString()` returns the identity, so the assignment is wrong
D. A compile error — `String` and `Object` are unrelated types

---

## Q28. What does `new Object().toString()` return?

A. `null`
B. An identity string of the form `java.lang.Object@<hashcode>`
C. `0`
D. A compile error — `toString()` does not exist on `Object`

---

## Q29. Which of these is a valid way to remove the second element of an `ArrayList` **by index**?

A. `list.remove(1)`
B. `list.remove(Integer.valueOf(1))`
C. `list.delete(1)`
D. `list.removeAt(1)`

---

## Q30. Which statement best describes **method overriding**?

A. Same name, different parameter lists, in the same class
B. The same method signature in a subclass, resolved at runtime by the object's actual type
C. Same name, resolved at compile time by the argument types
D. A `static` method in a subclass replacing one in the superclass

---

# Answer key

| Q | Answer | Why (one line) |
|---|--------|----------------|
| 1 | B | `protected` = same package **plus** subclasses elsewhere; `private` is class-only, `public` is everywhere. |
| 2 | B | Java allows one `extends` and any number of `implements`. |
| 3 | B | Dynamic dispatch picks `B.m()` because the object's actual type is `B`. |
| 4 | A | `super.m()` calls the superclass method; `super` cannot reach a `private` field or be assigned. |
| 5 | C | Java 8+ interfaces may hold `default` and `static` methods alongside constants. |
| 6 | A | The abstract method is implemented by `Circle`, so the call returns `3.14`. |
| 7 | B | `this()` runs first (count = 1), then `count = c` overwrites it with 5. |
| 8 | C | The constructor body runs once per object — two `new` expressions, two runs. |
| 9 | A | Interface fields are implicitly `public static final`. |
| 10 | A | A `final` method cannot be overridden. |
| 11 | B | `null instanceof X` is always `false` and never throws. |
| 12 | B | Different parameter lists with the same name = overloading. |
| 13 | A | `static` methods are **hidden**, not overridden — the compile-time type `A` decides. |
| 14 | A | A `final` local is safely capturable (and so is an effectively-final one in Java 8+). |
| 15 | A | The anonymous class implements `run()`, which is called directly on the current thread. |
| 16 | C | `HashMap` gives no iteration-order guarantee; use `LinkedHashMap` for insertion order. |
| 17 | B | `HashSet` buckets by `hashCode()`, so equal objects with different hashes are not deduplicated. |
| 18 | B | `LinkedList.get(i)` walks the list — O(n); `ArrayList.get(i)` is O(1). |
| 19 | A | `entrySet()` exposes `Map.Entry` objects carrying both key and value. |
| 20 | B | `Comparable` defines the natural order; `Comparator` supplies an external order. |
| 21 | B | The unmodifiable wrapper rejects every structural change with `UnsupportedOperationException`. |
| 22 | B | `TreeMap` is a red-black tree ordered by `compareTo` or by a `Comparator`. |
| 23 | B | `String` is immutable so each `+` allocates; `StringBuilder` appends in place. |
| 24 | D | No modifier means package-private access. |
| 25 | A | `super(...)` (and `this(...)`) must be the first statement of a constructor. |
| 26 | B | A class inheriting two conflicting abstract methods must override them. |
| 27 | B | A downcast is needed from `Object` to `String`. |
| 28 | B | `Object.toString()` returns `getClass().getName() + "@" + hashCode()`. |
| 29 | A | `remove(int)` removes by index; `remove(Integer)` removes by value. |
| 30 | B | Overriding keeps the signature and is dispatched at runtime on the actual object type. |

---

## Related

- [01 — OOP Principles](../01-OOP-Principles/)
- [02 — Classes, Objects & Constructors](../02-Classes-Objects-Constructors/)
- [03 — Inheritance & Polymorphism](../03-Inheritance-Polymorphism/)
- [04 — Interfaces, Abstract & Inner Classes](../04-Interfaces-Abstract-Inner-Classes/)
- [05 — Packages & Access Modifiers](../05-Packages-Access-Modifiers/)
- [06 — Collections Framework](../06-Collections-Framework/)
- [Part 2 — Exceptions, Output & Strings](./02-question-bank-part-2-exceptions-output-strings.md)
- [Part 3 — Static, Arrays & Threads](./03-question-bank-part-3-static-arrays-threads.md)
- [Question bank overview](./README.md)
