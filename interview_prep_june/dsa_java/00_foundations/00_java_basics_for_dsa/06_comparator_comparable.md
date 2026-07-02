# 06 — Comparator & Comparable in Java

Sorting is at the heart of countless DSA problems. Java gives you two ways to define ordering: `Comparable` (natural order) and `Comparator` (custom order). Master both — they appear constantly.

---

## 1. Comparable — Natural Ordering

### The Interface

```java
public interface Comparable<T> {
    public int compareTo(T o);
}
```

Returns a **negative integer**, **zero**, or **positive integer** if `this` is less than, equal to, or greater than the specified object.

### Implementing Comparable

```java
public class Student implements Comparable<Student> {
    String name;
    int grade;
    int age;

    public Student(String name, int grade, int age) {
        this.name = name;
        this.grade = grade;
        this.age = age;
    }

    // Natural ordering: by grade (ascending), then by name
    @Override
    public int compareTo(Student other) {
        // Primary: grade
        if (this.grade != other.grade) {
            return this.grade - other.grade;  // ascending
        }
        // Secondary: name (alphabetical)
        return this.name.compareTo(other.name);
    }

    @Override
    public String toString() {
        return name + "(" + grade + "," + age + ")";
    }
}

// Usage
List<Student> students = Arrays.asList(
    new Student("Alice", 85, 20),
    new Student("Bob", 92, 22),
    new Student("Charlie", 85, 19)
);
Collections.sort(students);  // uses compareTo
System.out.println(students);
// [Alice(85,20), Charlie(85,19), Bob(92,22)]
```

### The compareTo Contract

```java
// Must be consistent with equals() (strongly recommended, not required)
// sgn(x.compareTo(y)) == -sgn(y.compareTo(x))
// x.compareTo(y) > 0 && y.compareTo(z) > 0 ⇒ x.compareTo(z) > 0 (transitive)
// x.compareTo(y) == 0 ⇒ sgn(x.compareTo(z)) == sgn(y.compareTo(z))

// Consistency with equals:
// x.compareTo(y) == 0 should ideally imply x.equals(y)
// TreeSet, TreeMap use compareTo for equality, not equals()
// Violation: BigDecimal("1.0").compareTo(BigDecimal("1.00")) == 0
//           But BigDecimal("1.0").equals(BigDecimal("1.00")) is false!
```

### Common Classes with Comparable

```java
// String: lexicographic (dictionary order)
"apple".compareTo("banana");   // negative

// Integer, Long, Double: numeric order
Integer.compare(5, 10);        // negative

// Date: chronological
LocalDate.of(2024, 1, 1).compareTo(LocalDate.of(2024, 6, 15));  // negative
```

### The Overflow Trap

```java
// ❌ DANGEROUS — integer overflow!
public int compareTo(Student other) {
    return this.grade - other.grade;
    // If this.grade = Integer.MAX_VALUE, other.grade = -1
    // MAX_VALUE - (-1) = overflow → negative result! Wrong ordering!
}

// ✅ SAFE
public int compareTo(Student other) {
    return Integer.compare(this.grade, other.grade);
}

// ✅ Also safe
public int compareTo(Student other) {
    if (this.grade < other.grade) return -1;
    if (this.grade > other.grade) return 1;
    return 0;
}
```

---

## 2. Comparator — Custom Ordering

### The Interface

```java
@FunctionalInterface
public interface Comparator<T> {
    int compare(T o1, T o2);
    // plus many default/static methods
}
```

### Creating Comparators

```java
// Method 1: Implement the interface
class GradeComparator implements Comparator<Student> {
    @Override
    public int compare(Student a, Student b) {
        return Integer.compare(b.grade, a.grade);  // descending!
    }
}
Collections.sort(students, new GradeComparator());

// Method 2: Anonymous class (pre-Java 8)
Collections.sort(students, new Comparator<Student>() {
    @Override
    public int compare(Student a, Student b) {
        return a.name.compareTo(b.name);
    }
});

// Method 3: Lambda (Java 8+) — cleanest
Collections.sort(students, (a, b) -> a.name.compareTo(b.name));

// Method 4: Method reference
Collections.sort(students, Comparator.comparing(s -> s.name));
Collections.sort(students, Comparator.comparing(Student::getName));
```

---

## 3. Lambda Comparators In Depth

### Basic Patterns

```java
// Ascending
Collections.sort(list, (a, b) -> Integer.compare(a, b));

// Descending
Collections.sort(list, (a, b) -> Integer.compare(b, a));

// String comparison
Collections.sort(list, (a, b) -> a.compareTo(b));

// Multiple fields (manual)
Collections.sort(students, (a, b) -> {
    int gradeCmp = Integer.compare(a.grade, b.grade);
    if (gradeCmp != 0) return gradeCmp;
    return a.name.compareTo(b.name);
});
```

### The Overflow Warning — Again and Again

```java
// ❌ WRONG — (a - b) can overflow!
Comparator<Integer> badComparator = (a, b) -> a - b;

// ✅ RIGHT — use Integer.compare
Comparator<Integer> goodComparator = Integer::compare;

// ✅ RIGHT — use Comparator.naturalOrder()
Comparator<Integer> bestComparator = Comparator.naturalOrder();
```

---

## 4. Comparator.comparing — The Modern Way

```java
import static java.util.Comparator.*;

// Single field
Comparator<Student> byGrade = Comparator.comparingInt(Student::getGrade);
Comparator<Student> byName = Comparator.comparing(Student::getName);
Comparator<Student> byAge = Comparator.comparingInt(Student::getAge);

// Sorting
students.sort(byGrade);

// Chaining
students.sort(
    Comparator.comparingInt(Student::getGrade)
        .thenComparing(Student::getName)
        .thenComparingInt(Student::getAge)
);

// Reversed
students.sort(Comparator.comparingInt(Student::getGrade).reversed());

// Null handling
Comparator<Student> nullSafe = Comparator
    .comparing(Student::getName, Comparator.nullsFirst(String::compareTo));
// or
Comparator<Student> nullSafe = Comparator
    .comparing(Student::getName, String::compareTo)
    .nullsFirst();  // Java 17+ only
```

### Static Factory Methods

```java
// For primitives — avoids boxing overhead
Comparator.comparingInt(Student::getGrade)
Comparator.comparingLong(Student::getId)
Comparator.comparingDouble(Student::getScore)

// Natural order / reverse
Comparator.naturalOrder();      // Comparable's compareTo
Comparator.reverseOrder();      // reversed natural order

// Null handling
Comparator.nullsFirst(comparator);   // nulls come first
Comparator.nullsLast(comparator);    // nulls come last

// Chaining
comparator.thenComparing(nextComparator)
comparator.thenComparingInt(keyExtractor)
comparator.reversed()
```

---

## 5. Sorting with Multiple Fields — Examples

### Example: Sort Employees

```java
List<Employee> employees = getEmployees();

// Sort by: department (asc), salary (desc), name (asc)
employees.sort(
    Comparator.comparing(Employee::getDepartment)
        .thenComparing(Employee::getSalary, Comparator.reverseOrder())
        .thenComparing(Employee::getName)
);
```

### Example: Sort by Frequency then Value

```java
// Given [4, 5, 6, 5, 4, 3], sort by frequency (asc), then by value (desc)
int[] arr = {4, 5, 6, 5, 4, 3};

// Count frequencies
Map<Integer, Long> freq = Arrays.stream(arr)
    .boxed()
    .collect(Collectors.groupingBy(n -> n, Collectors.counting()));

// Sort by frequency, then by value
List<Integer> sorted = Arrays.stream(arr)
    .boxed()
    .sorted(Comparator
        .comparingLong((Integer n) -> freq.get(n))
        .thenComparing(Comparator.reverseOrder()))
    .collect(Collectors.toList());

// Result: [6, 3, 4, 4, 5, 5]  (freq 1: 6,3; freq 2: 4,5)
```

---

## 6. TreeMap/TreeSet with Custom Comparator

```java
// TreeSet with custom ordering
TreeSet<String> byLength = new TreeSet<>(Comparator.comparingInt(String::length));
byLength.add("apple");
byLength.add("banana");
byLength.add("kiwi");
System.out.println(byLength);  // [kiwi, apple, banana] — sorted by length

// ⚠️ See the problem? "apple" and "banana" have length 5 and 6
// But what if we add "grape" (length 5)?
byLength.add("grape");
System.out.println(byLength);  // [kiwi, apple, banana]
// "grape" is NOT added! Comparator says length(5) = length(5) → "equal"
// TreeSet uses Comparator for equality (not equals())

// Fix: add secondary comparison
TreeSet<String> byLengthThenAlpha = new TreeSet<>(
    Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder())
);
byLengthThenAlpha.add("apple");
byLengthThenAlpha.add("grape");
System.out.println(byLengthThenAlpha);  // [apple, grape, banana] — length then alpha

// TreeMap with custom comparator
TreeMap<Integer, String> byLastDigit = new TreeMap<>(
    (a, b) -> Integer.compare(a % 10, b % 10)
);
byLastDigit.put(13, "thirteen");
byLastDigit.put(22, "twenty-two");
byLastDigit.put(31, "thirty-one");
System.out.println(byLastDigit);  // {31=thirty-one, 22=twenty-two, 13=thirteen}
// Order: 31 (1), 22 (2), 13 (3) — by last digit
```

---

## 7. PriorityQueue with Comparator

```java
// Min-heap (default) — smallest priority first
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// Max-heap — largest first
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

// Custom: process tasks by priority, then by creation time
PriorityQueue<Task> taskQueue = new PriorityQueue<>(
    Comparator.comparingInt(Task::getPriority)
        .thenComparingLong(Task::getCreatedAt)
);

// Task scheduler: shortest job first
PriorityQueue<Job> scheduler = new PriorityQueue<>(
    Comparator.comparingLong(Job::getDuration)
);

// K closest points to origin
PriorityQueue<int[]> kClosest = new PriorityQueue<>(
    (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1])  // max-heap by distance
);
// But remember overflow risk! Safer:
PriorityQueue<int[]> kClosest = new PriorityQueue<>(
    (a, b) -> Integer.compare(b[0]*b[0] + b[1]*b[1], a[0]*a[0] + a[1]*a[1])
);
```

---

## 8. Complete Example — Sorting a Custom Class Every Way

```java
public class Person {
    String name;
    int age;
    double salary;

    // constructor, getters, toString...
}

// Natural order: by age
class Person implements Comparable<Person> {
    // ... fields

    @Override
    public int compareTo(Person other) {
        return Integer.compare(this.age, other.age);
    }
}

// Various custom orderings
public class PersonSorters {
    public static final Comparator<Person> BY_NAME_ASC =
        Comparator.comparing(Person::getName);

    public static final Comparator<Person> BY_NAME_DESC =
        Comparator.comparing(Person::getName).reversed();

    public static final Comparator<Person> BY_SALARY_ASC =
        Comparator.comparingDouble(Person::getSalary);

    public static final Comparator<Person> BY_SALARY_DESC =
        Comparator.comparingDouble(Person::getSalary).reversed();

    public static final Comparator<Person> BY_AGE_THEN_NAME =
        Comparator.comparingInt(Person::getAge)
            .thenComparing(Person::getName);

    public static final Comparator<Person> BY_NAME_THEN_AGE_DESC =
        Comparator.comparing(Person::getName)
            .thenComparingInt(Person::getAge).reversed();

    // Null-safe
    public static final Comparator<Person> NULL_SAFE =
        Comparator.nullsLast(
            Comparator.comparing(Person::getName)
        );
}

// Usage
List<Person> people = Arrays.asList(
    new Person("Alice", 30, 75000),
    new Person("Bob", 25, 85000),
    new Person("Charlie", 30, 90000),
    null
);

people.sort(PersonSorters.BY_AGE_THEN_NAME);
// [Bob(25), Alice(30), Charlie(30)] — age asc, name asc

people.sort(PersonSorters.NULL_SAFE);
// [Alice(30), Bob(25), Charlie(30), null]
```

---

## 9. Comparator Utility Methods — Complete Reference

```java
// Java 8+
Comparator.naturalOrder()
Comparator.reverseOrder()
Comparator.nullsFirst(comparator)
Comparator.nullsLast(comparator)

// Java 8+ — static factory methods for Comparator.comparing
Comparator.comparing(keyExtractor)              // for Comparable keys
Comparator.comparing(keyExtractor, comparator)  // custom key comparator
Comparator.comparingInt(ToIntFunction)
Comparator.comparingLong(ToLongFunction)
Comparator.comparingDouble(ToDoubleFunction)

// Default methods on Comparator
comparator.reversed()
comparator.thenComparing(other)
comparator.thenComparing(keyExtractor)
comparator.thenComparingInt(keyExtractor)
comparator.thenComparingLong(keyExtractor)
comparator.thenComparingDouble(keyExtractor)
```

---

## Cheat Sheet

```java
// COMPARABLE — natural order (in the class itself)
class Foo implements Comparable<Foo> {
    @Override
    public int compareTo(Foo other) {
        return Integer.compare(this.x, other.x);  // use Integer.compare!
    }
}
Collections.sort(list);  // uses compareTo

// COMPARATOR — custom order (separate)
Collections.sort(list, (a, b) -> Integer.compare(a.x, b.x));
Collections.sort(list, Comparator.comparingInt(Foo::getX));
Collections.sort(list, Comparator.comparing(Foo::getName)
    .thenComparingInt(Foo::getGrade).reversed()
    .thenComparing(Foo::getAge, Comparator.reverseOrder()));

// COMMON IDIOMS
// Ascending: Integer.compare(a, b)
// Descending: Integer.compare(b, a)
// Natural: Comparator.naturalOrder()
// Reverse: Comparator.reverseOrder()
// Null: Comparator.nullsFirst/Last(cmp)
```

**Golden rule:** Always use `Integer.compare(a, b)` not `a - b`. Your interviewer will not appreciate overflow bugs.
