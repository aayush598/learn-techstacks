# Object Creation, Copying and Identity

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 9 min_
> **Prerequisite:** [Object lifecycle and construction](01-object-lifecycle-and-construction.md)

## In one sentence

`new` is the normal way to create an object, `clone()` gives a **shallow** copy, `equals` defaults
to **reference identity**, and `finalize()` is deprecated because the garbage collector gives you
no guarantee when it runs.

## Why the pre-test tests this

- "Which method is used to create an object dynamically?" and "What does `equals()` compare by
  default?" are classic 1-markers.
- "Which of the following is deprecated in Java 9?" → `finalize()`. This shows up often enough to
  be worth one memorised fact.
- Shallow vs deep copy is the classic "output prediction" trap: clone an object with a `List`
  field and both copies share the same list.

## Core concept

### Three ways to create an object

| Approach | Code | Notes |
|---|---|---|
| **`new`** (the normal way) | `Foo f = new Foo();` | Compile-time type, known at compile time |
| **Reflection** (`Class` API) | `Class<?> c = Foo.class;`<br>`Object o = c.getDeclaredConstructor().newInstance();` | The modern, correct form. `getDeclaredConstructor()` finds the constructor, `newInstance()` invokes it |
| **Reflection (legacy)** | `Foo.class.newInstance()` | **Deprecated since Java 9.** Propagates checked exceptions directly instead of wrapping them in `InvocationTargetException` |

Related reflection facts:

| Call | Effect |
|---|---|
| `Class.forName("com.Foo")` | Loads **and initialises** the class (static blocks run) |
| `ClassLoader.loadClass("com.Foo")` | Loads the class but does **not** initialise it |
| `obj.getClass()` | Returns the **runtime** class of `obj` (never null) |
| `obj.getClass().getSimpleName()` | The class name without the package, e.g. `Foo` |

### `clone()` — shallow copy

| Fact | Detail |
|---|---|
| `Object.clone()` | `protected`, returns a **shallow** copy of the object |
| Requirement | The class must implement **`Cloneable`** (a marker interface with no methods), otherwise `CloneNotSupportedException` is thrown |
| Shallow means | **Primitive fields** are copied by value; **object fields** are copied by reference — both copies point to the **same** nested object |
| Deep copy | You must copy the nested objects yourself (e.g. `new ArrayList<>(other.list)`) |
| Arrays | `arr.clone()` returns a **shallow** copy of the array — the elements are still shared |

### Worked code — shallow copy

```java
import java.util.ArrayList;
import java.util.List;

class Bag implements Cloneable {
    List<String> items = new ArrayList<>();
    int count = 0;

    @Override
    public Bag clone() {
        try {
            return (Bag) super.clone();
        } catch (CloneNotSupportedException e) {
            return null;
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Bag b1 = new Bag();
        b1.items.add("a");
        b1.count = 1;

        Bag b2 = b1.clone();
        b2.items.add("b");
        b2.count = 2;

        System.out.println(b1.items.size());
        System.out.println(b1.count);
        System.out.println(b1.items == b2.items);
    }
}
```

**This prints exactly:**

```
2
1
true
```

| Line | Value | Why |
|---|---|---|
| `b1.items.size()` | `2` | The **same** `List` object is referenced by both copies, so adding to `b2` shows up in `b1` |
| `b1.count` | `1` | `int` is a primitive — copied by value, so `b2.count = 2` did not affect `b1` |
| `b1.items == b2.items` | `true` | The shallow copy copied the *reference*, not the list |

A **deep copy** would have copied the list too, and `b1.items.size()` would print `1`.

### `equals` and `hashCode` — the default behaviour

| Method | Default behaviour | Override it when |
|---|---|---|
| `equals(Object)` | Reference identity (`this == other`). Two different objects are never equal | The class has value semantics |
| `hashCode()` | Identity hash code — derived from the object's identity, not its fields | You override `equals` |

**The contract (both must hold):**

| Rule | Statement |
|---|---|
| 1 | `x.equals(x)` is always true (reflexive) |
| 2 | `x.equals(y)` ⇒ `y.equals(x)` (symmetric) |
| 3 | `x.equals(y)` and `y.equals(z)` ⇒ `x.equals(z)` (transitive) |
| 4 | `x.equals(y)` ⇒ **`x.hashCode() == y.hashCode()`** |
| 5 | If a field is used in `equals`, it must be used in `hashCode` — and vice versa |

Rule 4 is the one that shows up in the exam: **equal objects must have equal hash codes.** The
converse is not required (unequal objects may share a hash code — a collision).

```java
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    // no equals/hashCode override
}
Point p1 = new Point(2, 3);
Point p2 = new Point(2, 3);
p1.equals(p2);   // false — reference identity, the fields happen to match
```

If `Point` overrode `equals` to compare `x` and `y` but **not** `hashCode`, then `p1.equals(p2)`
would be `true` while `p1.hashCode() != p2.hashCode()` — and `HashSet` would treat the two points
as different elements. That is the bug the contract exists to prevent.

### Serialization — the basics

| Fact | Detail |
|---|---|
| Marker interface | `java.io.Serializable` |
| Write | `new ObjectOutputStream(fos).writeObject(obj);` |
| Read | `Object obj = new ObjectInputStream(fis).readObject();` — the object is returned as `Object`, so you cast |
| `transient` fields | **Not serialized**. Restored as `null` / `0` after deserialization |
| `static` fields | Never serialized — they belong to the class, not the object |
| `serialVersionUID` | Declare it explicitly to control compatibility across versions |
| Exceptions | `NotSerializableException` if the class does not implement `Serializable`; `ClassNotFoundException` on read |

### `finalize()` — deprecated, and why

| Fact | Detail |
|---|---|
| Signature | `protected void finalize() throws Throwable` |
| When it runs | **At most once**, sometime before the object is garbage collected — **if at all** |
| Why it is deprecated | Deprecated since **Java 9**, marked for removal in later versions. The GC may never run it; it never runs at a predictable time; it can resurrect the object; it adds GC overhead |
| The replacement | `try`-with-resources + `AutoCloseable` / `Closeable` for resources; `java.lang.ref.Cleaner` (Java 9+) as a last resort |

**Exam fact to memorise:** `finalize()` is **deprecated** — it is *not* guaranteed to run. A better
answer in any "how do you release resources" question is *close the resource explicitly*.

### Identity vs equality — the two-operator summary

| Expression | Compares | Example |
|---|---|---|
| `a == b` | **References** (identity) for objects; **values** for primitives | `new String("ab") == new String("ab")` → `false` |
| `a.equals(b)` | **Logical content**, if `equals` is overridden; otherwise identity | `new String("ab").equals(new String("ab"))` → `true` |

## Quick rules

- `new` for normal creation; `getDeclaredConstructor().newInstance()` for reflection;
  `Class.newInstance()` is deprecated.
- `Class.forName` initialises the class (static blocks run); `loadClass` does not.
- `clone()` needs `Cloneable`, is `protected`, and is **shallow**.
- Default `equals` is reference identity. Override `equals` **and** `hashCode` together.
- Equal objects ⇒ equal hash codes. The converse is not required.
- `transient` and `static` fields are never serialized.
- `finalize()` is **deprecated** and **not guaranteed** to run. Use explicit `close()`.
- `==` compares references; `.equals()` compares content.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| `clone()` copies nested objects | "Deep copy" | `clone()` is **shallow** |
| `clone()` works without `Cloneable` | Compiles and runs | Throws `CloneNotSupportedException` |
| Overriding `equals` alone is enough | "Yes" | `hashCode` must be overridden too |
| Equal hash codes ⇒ equal objects | "Yes" | The converse does not hold |
| `finalize()` is called before the object is collected | "Guaranteed" | It is **not guaranteed** |
| `transient` fields are serialized as `null` | "Serialized" | They are **skipped** entirely |
| `Class.newInstance()` is the modern API | "Recommended" | Deprecated since Java 9 |
| `a == b` on two equal-looking Strings | `true` | `==` compares references |

## Checklist

- [ ] I can state what `clone()` returns and what "shallow" means in one sentence.
- [ ] I know `clone()` requires `Cloneable` or it throws.
- [ ] I can list the 5 `equals`/`hashCode` contract rules.
- [ ] I know the default `equals` is reference identity.
- [ ] I know `finalize()` is deprecated and not guaranteed to run.
- [ ] I know `transient` and `static` fields are skipped by serialization.

## Related

- [Object lifecycle and construction](01-object-lifecycle-and-construction.md)
- [Creation patterns: singleton, immutable, factory, builder](../02-techniques/02-creation-patterns.md)
- [8 solved construction questions](../03-worked-examples/01-solved-construction-questions.md)
- [Construction traps](../04-pitfalls/01-construction-and-object-traps.md)
- [Construction one-pager](../05-reference/01-construction-one-pager.md)
- [Topic overview](../README.md)
