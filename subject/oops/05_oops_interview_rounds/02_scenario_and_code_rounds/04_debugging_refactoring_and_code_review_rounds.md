# Debugging, Refactoring and Code Review Rounds — 100 Interview Q&A

## Q1: What will this code print and why?

**A:** The code creates a `String` variable `s` assigned to `"hello"`, then calls `s.concat(" world")` and discards the return value. Since `String` is immutable in Java, the `concat` method returns a **new** `String` object rather than modifying the original. The original reference `s` still points to `"hello"`, so printing `s` outputs `hello` rather than `hello world`.

The bug is a common beginner mistake: assuming string methods mutate the object in place. Every `String` method that appears to modify the string actually allocates a new object on the heap and returns it. If the programmer intended concatenation, they must capture the return value in a variable or reassign `s = s.concat(" world")`.

**Example:**
```java
public class StringBug {
    public static void main(String[] args) {
        String s = "hello";
        s.concat(" world"); // return value is discarded
        System.out.println(s); // prints "hello", NOT "hello world"

        // Fix: reassign the result
        s = s.concat(" world");
        System.out.println(s); // prints "hello world"
    }
}
```

## Q2: What is wrong with this equals method?

**A:** The `equals` method uses `==` to compare `name` fields instead of `.equals()`. For `String` fields, `==` compares object identity (reference equality), not the actual character content. Two distinct `String` objects with identical content will return `false` with `==` but `true` with `.equals()`. This violates the `equals` contract because objects that are logically equal will not be recognized as such.

The correct implementation must use `.equals()` for object fields and handle `null` checks to avoid `NullPointerException`. Additionally, the method should check `this == other` as a fast-path optimization and verify the exact class type using `getClass()` rather than `instanceof` to preserve symmetry across class hierarchies.

**Example:**
```java
public class Employee {
    private String name;
    private int id;

    // Broken: uses == for String comparison
    @Override
    public boolean equals(Object o) {
        if (o instanceof Employee e) {
            return this.id == e.id && this.name == e.name; // WRONG
        }
        return false;
    }

    // Fixed
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee e = (Employee) o;
        return id == e.id && java.util.Objects.equals(name, e.name);
    }
}
```

## Q3: Why does this code produce unexpected output?

**A:** The inner class `Outer` has a field `value = 10`. Inside the inner class method `printValue`, the local variable `value` shadows the instance field. The print statement references the local parameter `value` (set to 20) instead of the instance field `this.value`. This is variable shadowing — the closest scope wins, and the local parameter takes precedence over the instance field.

To access the hidden instance field, you must use the `Outer.this.value` qualified syntax. This type of bug is notoriously hard to spot because the code compiles without warnings and the shadowed field name creates a subtle semantic trap. IDEs may flag it, but in dense code it is easily missed during reviews.

**Example:**
```java
class Outer {
    int value = 10;

    void printValue(int value) {
        System.out.println(value);      // prints 20 (parameter)
        System.out.println(this.value); // prints 10 (instance field)
    }

    public static void main(String[] args) {
        new Outer().printValue(20);
    }
}
```

## Q4: What bug exists in this constructor?

**A:** The constructor attempts to validate `age` before assigning it, but the validation logic is incomplete. When `age` is negative, it throws an exception — that part is correct. However, the real bug is that the class uses a setter inside the constructor: `setAge(age)`. If the subclass overrides `setAge` (or `initialize`), the overridden method runs **before** the subclass constructor completes, accessing an uninitialized subclass field. This is the "calling overridable methods from constructors" anti-pattern.

The virtual method dispatch in the constructor means `this` is partially constructed. The subclass fields have their default values (0, null, false) rather than anything the subclass constructor would have set. Any method called from the parent constructor that touches subclass state will observe these defaults and potentially corrupt object state silently.

**Example:**
```java
class Person {
    private int age;

    Person(int age) {
        initialize();       // calls overridable method
        this.age = age;     // assignment AFTER override runs
    }

    void initialize() { /* subclass may override */ }
}

class Student extends Person {
    private String school;

    Student(int age, String school) {
        super(age);         // initialize() runs here, school is null
        this.school = school;
    }

    @Override
    void initialize() {
        System.out.println(school.length()); // NPE: school is still null
    }
}
```

## Q5: Find the logical error in this inheritance example

**A:** The `Dog` subclass overrides `speak` but calls `super.speak()` in the wrong order — it prints the dog sound first and then the parent sound. While this compiles, the semantic error is that `speak` in `Animal` is abstract, so `super.speak()` will throw `UnsupportedOperationException` at runtime if the parent does not provide a body. Even if the parent has a body, the ordering is inverted from what a caller would expect.

More critically, the real logical error is that `Dog` overrides a method without ensuring the parent's contract is preserved. If `Animal.speak()` performs setup work (logging, state tracking), skipping it or calling it out of order breaks the expected behavior chain. The correct approach is to call `super.speak()` first if the parent method has side effects, or to avoid calling it altogether and provide a complete implementation.

**Example:**
```java
abstract class Animal {
    abstract void speak();

    void log() {
        System.out.println("Animal spoke");
    }
}

class Dog extends Animal {
    @Override
    void speak() {
        System.out.println("Woof!");
        // Bug: if parent had concrete logic, it should run first
        // super.speak() cannot be called on abstract method
    }
}
```

## Q6: Why is this comparison returning wrong results?

**A:** The `compareTo` method does not handle the case where both objects have equal `priority` values but different `id` values. When `priority` is equal, it returns `0` instead of falling through to compare `id`. This means two tasks with the same priority but different IDs are considered equal by the comparator, which breaks sorting stability and can cause collections to lose elements during `TreeSet` or `TreeMap` operations.

A correct implementation should have a total ordering tiebreaker. When primary fields are equal, compare secondary fields. Also, the method does not check for null references or the same-type constraint, which can cause `ClassCastException` at runtime if a non-`Task` object is passed.

**Example:**
```java
class Task implements Comparable<Task> {
    int priority;
    int id;

    // Broken: equal priority means equals, ignoring id
    @Override
    public int compareTo(Task other) {
        return Integer.compare(this.priority, other.priority);
    }

    // Fixed: tiebreak on id for total ordering
    @Override
    public int compareTo(Task other) {
        int cmp = Integer.compare(this.priority, other.priority);
        if (cmp != 0) return cmp;
        return Integer.compare(this.id, other.id);
    }
}
```

## Q7: What does this code print?

**A:** The code prints `null`, then throws a `NullPointerException`. The static field `instance` is initialized in a static block, but the static block runs **after** the field declaration with default values. Since `data` is initialized to `null` in the static block before `instance` is assigned, when `create()` is called, `instance.data` is `null`. Accessing `null.length()` throws the NPE.

Actually, the subtler bug is that the static initializer sets `instance.data = null` explicitly (or leaves it null), and then `create()` calls `instance.data.length()`. The field `data` was never populated with an actual string. The initialization order in static blocks matters: static fields are initialized in declaration order, and static blocks execute in the order they appear. Misunderstanding this order causes fields to be null or zero when methods are called.

**Example:**
```java
class Config {
    static Config instance;
    String data;

    static {
        data = "loaded";   // this sets the CLASS field's data? No — this is an instance
        instance = new Config(); // instance.data is "loaded" here
        instance = new Config(); // instance.data is now null — a NEW object
    }

    static Config create() {
        return instance; // returns second Config with null data
    }
}

// Output: NullPointerException at runtime
```

## Q8: Why does this method not work as expected?

**A:** The method `findFirst` is supposed to return the first element matching a condition from a list, but it modifies the list using `list.remove(0)` inside the loop. Removing elements during iteration corrupts the iteration index, causing elements to be skipped. When element at index 0 is removed, what was at index 1 moves to index 0, but the loop increments to index 1, effectively skipping the element that just shifted.

The fix is to either use an iterator with `remove()`, iterate over a copy of the list, or use streams. Additionally, the method does not return `null` or throw when no match is found — it falls through and returns `null` implicitly, which may or may not be the intended contract. Callers must handle the null return, which is error-prone.

**Example:**
```java
public static String findFirst(List<String> list, Predicate<String> condition) {
    // Bug: removing during indexed iteration skips elements
    for (int i = 0; i < list.size(); i++) {
        if (condition.test(list.get(i))) {
            return list.get(i);
        }
    }
    return null;

    // Fixed: use iterator or stream
    // return list.stream().filter(condition).findFirst().orElse(null);
}
```

## Q9: Spot the resource leak in this code

**A:** The code opens a `FileInputStream` and `BufferedReader` but does not close them in a `finally` block or use try-with-resources. If an exception occurs between opening and closing the stream, the file handle leaks. On systems with limited file descriptors, this causes the process to eventually fail with "too many open files." Even in the happy path, relying on garbage collection to close streams is unreliable — the GC may never run, or the finalizer may not release the handle promptly.

The proper fix is to use try-with-resources (Java 7+), which guarantees that each resource is closed when the block exits, even if an exception is thrown. This eliminates the need for manual `finally` blocks and prevents resource leaks in all code paths.

**Example:**
```java
// Broken: resource leak
void readFile(String path) throws Exception {
    FileInputStream fis = new FileInputStream(path);
    BufferedReader br = new BufferedReader(new InputStreamReader(fis));
    String line = br.readLine();
    System.out.println(line);
    br.close(); // never reached if exception above
}

// Fixed: try-with-resources
void readFile(String path) throws Exception {
    try (BufferedReader br = new BufferedReader(
            new InputStreamReader(new FileInputStream(path)))) {
        String line = br.readLine();
        System.out.println(line);
    } // automatically closed
}
```

## Q10: What is wrong with this static initialization?

**A:** The static initializer references `instance` before it is assigned. In Java, static fields are initialized in declaration order, and static blocks execute in textual order. If a static block tries to use a static field declared **after** it, that field has its default value (null for objects, 0 for primitives). This creates a situation where the object is partially constructed during class loading.

The fix is to declare fields before the blocks that reference them, or to perform initialization in the correct order. A related problem is circular static dependencies between two classes — class A's static initializer triggers class B's class loading, which triggers class A's static initializer again, causing a `StackOverflowError` or deadlock.

**Example:**
```java
class Database {
    static {
        // Bug: config is declared below, so it is null here
        url = config.getUrl(); // compile error or NPE
    }
    static Config config;
    static String url;

    static { config = new Config(); } // runs FIRST (declared first)
}

// Fix: reorder declarations
class Database {
    static Config config = new Config();
    static String url = config.getUrl(); // now works
}
```

## Q11: Why does this array copy produce incorrect results?

**A:** The code uses `System.arraycopy` but the source and destination overlap, causing data corruption. When copying forward in an overlapping region (where the destination starts within the source range), earlier elements get overwritten before they are copied. This is the classic overlapping-copy bug. The Java specification states that if source and destination overlap, the behavior is as if the source is copied to a temporary array first, but only for `System.arraycopy`.

Alternatively, if the bug is a manual loop copy, the issue is likely an off-by-one in the loop bounds or incorrect index arithmetic. For example, using `i < arr.length` instead of `i < arr.length - 1` when copying into a smaller portion of the array. The fix is to use `Arrays.copyOf` or `System.arraycopy` with correct bounds, or use `Arrays.copyOfRange` for clarity.

**Example:**
```java
int[] arr = {1, 2, 3, 4, 5};
// Bug: overlapping copy corrupts data
System.arraycopy(arr, 1, arr, 0, 4); // arr becomes {2, 3, 4, 5, 5} or worse
// Expected: {2, 3, 4, 5, 5} but intermediate states differ by JVM

// Fixed: copy to temp first
int[] temp = Arrays.copyOfRange(arr, 1, 5);
System.arraycopy(temp, 0, arr, 0, 4);
```

## Q12: Find the off-by-one error

**A:** The loop uses `<=` instead of `<` when iterating over the array bounds. In zero-indexed languages like Java, valid indices range from 0 to `length - 1`. Using `i <= arr.length` causes an `ArrayIndexOutOfBoundsException` on the last iteration because it accesses `arr[arr.length]`, which is one past the end of the array. This is the most common off-by-one error in indexed iteration.

The fix depends on the intent: if you want to visit every element, use `i < arr.length`. If you want to include the upper bound for a range operation (like copying), you typically use exclusive upper bounds with `<`. Understanding whether bounds are inclusive or exclusive is critical in avoiding these errors.

**Example:**
```java
int[] arr = {10, 20, 30};
// Bug: <= causes ArrayIndexOutOfBoundsException
for (int i = 0; i <= arr.length; i++) {
    System.out.println(arr[i]); // crashes when i == 3
}

// Fixed: use <
for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}
```

## Q13: What is wrong with this exception handling?

**A:** The code catches `Exception` as a catch-all, which masks the actual error. By catching the broadest exception type, specific exceptions like `IOException`, `SQLException`, or `NullPointerException` are all handled identically — logged and swallowed. This makes debugging extremely difficult because the caller never learns that an error occurred. The method returns normally even when the operation failed completely.

The proper approach is to catch specific exceptions and handle them differently. Some exceptions should be logged and recovered from, others should be rethrown (possibly wrapped), and some should propagate as-is. Additionally, the catch block uses `e.printStackTrace()` which writes to stderr instead of a proper logging framework, and there is no `finally` block or try-with-resources to clean up resources.

**Example:**
```java
// Broken: catches everything, swallows errors
try {
    processData(file);
} catch (Exception e) {
    e.printStackTrace(); // goes to stderr, no recovery
}

// Fixed: specific handling
try {
    processData(file);
} catch (FileNotFoundException e) {
    logger.error("File not found: {}", file, e);
    throw new ServiceException("Missing data file", e);
} catch (IOException e) {
    logger.warn("IO error, retrying", e);
    retryOperation(file);
}
```

## Q14: Why does this hashCode violate the contract?

**A:** The `hashCode` implementation returns a constant value (0) for all objects. While this technically does not violate the Java specification (equal objects must have equal hash codes, and this satisfies that since all hash codes are the same), it destroys the performance of hash-based collections like `HashMap`, `HashSet`, and `Hashtable`. When every object hashes to the same bucket, these collections degenerate from O(1) average lookup to O(n) worst-case, turning a hash table into a linked list.

A proper `hashCode` implementation should distribute objects across hash buckets as uniformly as possible. The implementation should use the same fields as `equals` — if two objects are equal according to `equals`, they must have the same `hashCode`. The standard approach uses `Objects.hash()` with all fields used in `equals`, or a manual combination using prime multiplication and XOR.

**Example:**
```java
// Broken: constant hash code destroys hash performance
@Override
public int hashCode() {
    return 0;
}

// Fixed: distribute based on fields used in equals
@Override
public int hashCode() {
    return Objects.hash(name, id, department);
}
```

## Q15: Spot the string comparison bug

**A:** The code compares two `String` objects using `==` instead of `.equals()`. The `==` operator compares object references (memory addresses), not the actual string content. When strings are constructed dynamically (via `new String()`, concatenation, or reading from I/O), two strings with identical content will have different references and `==` will return `false` even though the strings are logically equal.

Java interns string literals, so `"hello" == "hello"` returns `true` for compile-time constants. But any runtime-constructed string will create a new object on the heap. The correct comparison is always `str1.equals(str2)`. Also, to avoid `NullPointerException`, use `Objects.equals(str1, str2)` or put the constant first: `"constant".equals(variable)`.

**Example:**
```java
String a = new String("hello");
String b = new String("hello");
System.out.println(a == b);      // false — different objects
System.out.println(a.equals(b)); // true — same content

// Also dangerous with concatenation
String c = "hel" + "lo";
String d = "hello";
System.out.println(c == d); // true for literals (compiler folding)
// But:
String e = getHel(); // returns "hel"
String f = e + "lo"; // runtime concatenation
System.out.println(f == "hello"); // false!
```

## Q16: What is wrong with this recursive method?

**A:** The recursive method has a missing or incorrect base case. Without a proper termination condition, the recursion continues indefinitely until the JVM throws a `StackOverflowError`. Each recursive call adds a new frame to the call stack, consuming memory. When the base case is missing or unreachable (e.g., the condition never becomes true due to a logic error), the recursion never terminates.

The fix is to ensure the base case is reached on every path and that recursive calls move toward the base case. For example, in a factorial function, `n` must decrease toward 0. If `n` is not decremented, or if the base case checks the wrong condition (e.g., `n == 1` when `n` starts at 0), the recursion becomes infinite. Always verify that every recursive path converges to the base case.

**Example:**
```java
// Broken: no base case
int sum(int n) {
    return n + sum(n - 1); // StackOverflowError
}

// Fixed: proper base case
int sum(int n) {
    if (n <= 0) return 0;   // base case
    return n + sum(n - 1);   // progresses toward base case
}
```

## Q17: Why does this overloaded method resolve unexpectedly?

**A:** The method resolution follows static (compile-time) type dispatch for overloaded methods, not dynamic (runtime) type dispatch. When `Object obj` holds a `String`, calling `process(obj)` invokes the `process(Object)` overload, not `process(String)`, because the compiler resolves the overload based on the declared parameter type. The compiler only sees `obj` as type `Object`, so it selects the most specific applicable overload at compile time.

This is different from virtual method dispatch (overriding), which uses the runtime type. Overloading is a compile-time mechanism; overriding is a runtime mechanism. The fix is to either cast the argument to the desired type explicitly, or restructure the code to avoid relying on overloaded dispatch with polymorphic arguments.

**Example:**
```java
class Processor {
    void process(Object o) { System.out.println("Object version"); }
    void process(String s) { System.out.println("String version"); }

    public static void main(String[] args) {
        Object obj = "hello";
        new Processor().process(obj); // prints "Object version" (compile-time type)
        new Processor().process((String) obj); // prints "String version"
    }
}
```

## Q18: Find the null reference bug

**A:** The code calls `.toString()` on a value that may be `null`. When a method returns `null` (such as a `Map.get` that finds no entry, or a database query that returns no result), calling any method on that null reference throws a `NullPointerException`. The code does not perform a null check before dereferencing the reference.

The fix is to add explicit null checks before using the value, or use `Optional` to make the absence of a value explicit in the type system. Java's `Objects.toString()` helper provides a default value for null, and the null-conditional pattern `Optional.ofNullable(value).map(...)` avoids the NPE entirely. Defensive programming assumes every reference might be null unless proven otherwise by the API contract.

**Example:**
```java
Map<String, Integer> map = new HashMap<>();
// Bug: get returns null, then NPE on unboxing
int len = map.get("key").length(); // NPE

// Fixed: check for null
Integer val = map.get("key");
int len = (val != null) ? val.toString().length() : 0;

// Or use Optional
int len = Optional.ofNullable(map.get("key"))
    .map(Object::toString)
    .map(String::length)
    .orElse(0);
```

## Q19: What is wrong with this try-with-resources usage?

**A:** The code opens resources inside the try-with-resources block but also opens them in nested try blocks without try-with-resources. The outer `BufferedReader` is properly managed, but the inner `FileInputStream` (if opened separately) is not guaranteed to close if an exception occurs between opening the stream and assigning it to the try-with-resources variable. Additionally, the catch block silently swallows the exception, so any resource leak goes undetected.

Another common issue is declaring multiple resources in a single try-with-resources — if the second resource constructor throws, the first resource is still closed (this is correct behavior but worth understanding). The fix is to open each resource directly in the try-with-resources declaration and handle or propagate exceptions rather than swallowing them.

**Example:**
```java
// Broken: nested resource not managed by try-with-resources
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    FileInputStream fis = new FileInputStream("data.bin"); // leaked
    // ... if exception here, fis is never closed
    fis.close(); // may not execute
}

// Fixed: all resources in try-with-resources
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"));
     FileInputStream fis = new FileInputStream("data.bin")) {
    // both guaranteed closed
}
```

## Q20: Why is this default value initialization wrong?

**A:** The instance field `count` is declared as `int count = 0;` explicitly, but the constructor also sets `count = 0` redundantly. The real bug is that the field is not `final`, so it can be modified after construction, breaking any invariant that depends on the initial value. The class appears to enforce initialization, but any method or subclass can change `count` to an invalid state.

More subtly, the initialization order matters when fields reference other fields or methods. If `count` were initialized from a method call that depends on another uninitialized field, you would get a default zero instead of the intended value. The fix is to make the field `final` if it should not change, and to initialize all fields through a single code path (the constructor) to ensure consistent state.

**Example:**
```java
class Counter {
    int count = 0; // mutable, can be changed freely
    final int maxCount; // immutable after construction

    Counter(int max) {
        count = 0;   // redundant
        maxCount = max; // correct: final ensures invariant
    }

    void increment() {
        if (count < maxCount) count++;
    }
}
```

## Q21: Spot the concurrent modification issue

**A:** The code iterates over an `ArrayList` using a for-each loop while calling `list.remove()` inside the loop body. The for-each loop uses an `Iterator` internally, and modifying the underlying collection directly (via `list.remove()`) invalidates the iterator's state. This throws a `ConcurrentModificationException` at runtime. The iterator detects that the collection was modified outside its control and fails fast to prevent undefined behavior.

The fix is to use the iterator's own `remove()` method during iteration, or use `removeIf` (Java 8+) which handles removal safely. Alternatively, collect elements to remove in a separate list and remove them after iteration completes. CopyOnWriteArrayList can also be used for concurrent scenarios where reads vastly outnumber writes.

**Example:**
```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
// Broken: ConcurrentModificationException
for (String s : list) {
    if (s.equals("b")) list.remove(s); // throws
}

// Fixed: use iterator
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().equals("b")) it.remove();
}

// Or Java 8+
list.removeIf(s -> s.equals("b"));
```

## Q22: What is wrong with this auto-boxing behavior?

**A:** The code relies on auto-boxing to convert between `int` and `Integer`, but the `Integer` cache only covers the range -128 to 127. When two `Integer` objects are created with values outside this range (e.g., 200), `==` compares references rather than values, returning `false` even though the integers are logically equal. This is because `Integer.valueOf(200)` creates a new object each time, while `Integer.valueOf(100)` returns the same cached instance.

The `equals` method works correctly for all values, but `==` is a reference comparison for object types. This bug manifests subtly because small values (within the cache range) work with `==`, and the code passes unit tests using small test data but fails in production with larger values. The fix is to always use `.equals()` for `Integer` comparisons, or use primitive `int` when possible to avoid boxing entirely.

**Example:**
```java
Integer a = 128;
Integer b = 128;
System.out.println(a == b);      // false — different objects
System.out.println(a.equals(b)); // true

Integer c = 100;
Integer d = 100;
System.out.println(c == d);      // true — cached same object
// This discrepancy causes bugs that only appear with values > 127
```

## Q23: Why does this enum comparison fail?

**A:** The code uses `.equals()` to compare enum values, which works but is unnecessary and hides a deeper issue. The real bug is that the code creates enum instances using the constructor (if the enum has a private constructor accessible via reflection or if the developer mistakenly thinks enums work like classes). Enum values are singletons — there is exactly one instance per constant. The correct comparison is using `==`, which is both more performant and null-safe.

If the code is comparing an enum field against a string representation (e.g., comparing `status.equals("ACTIVE")`), that fails because `equals` expects another enum constant, not a string. The fix is to use `Status.valueOf(string)` for string-to-enum conversion, or compare the enum's `.name()` method against the string. Never use `toString()` for comparison as it may be overridden.

**Example:**
```java
enum Status { ACTIVE, INACTIVE }

Status s = Status.ACTIVE;
// Wrong: comparing enum to string
// s.equals("ACTIVE") // always false

// Correct approaches
Status status = Status.valueOf("ACTIVE"); // string to enum
s == Status.ACTIVE;                       // enum comparison
s.name().equals("ACTIVE");                // string comparison
```

## Q24: Find the logical error in this switch statement

**A:** The switch statement is missing a `break` statement (or `return`) after one of its cases, causing fall-through. When a case matches, execution continues through subsequent cases until a `break` or the end of the switch is reached. This is a classic C-style bug where the programmer intended each case to be independent but forgot to terminate them. The result is that matching a value for case A also executes the code for case B, C, etc.

In Java 14+, you can use enhanced switch expressions with `->` arrows that do not fall through, eliminating this class of bug. Alternatively, always use `break` or `return` in traditional switch statements. Some coding standards require a comment `// fall through` if intentional fall-through is desired, making the intent explicit.

**Example:**
```java
int day = 3;
String type;
switch (day) {
    case 1: type = "Weekday";
    case 2: type = "Weekday";
    case 3: type = "Weekday";
    case 6: type = "Weekend";
    case 7: type = "Weekend";
    default: type = "Unknown";
}
// type is always "Unknown" due to fall-through

// Fixed with arrow syntax (Java 14+)
String type = switch (day) {
    case 1, 2, 3, 4, 5 -> "Weekday";
    case 6, 7 -> "Weekend";
    default -> "Unknown";
};
```

## Q25: What is wrong with this generic type usage?

**A:** The generic class `Box<T>` has a method `set(T item)` and a method `get()`, but there is an unchecked cast when retrieving from an internal `Object[]` array. The class stores items in `Object[]` for type erasure compatibility, but the cast `(T)` at retrieval is an unchecked cast — the compiler cannot verify it at runtime due to type erasure. If the array contains a mismatched type (due to a raw type usage or concurrent modification), the cast fails at the point of use, not at the point of insertion.

The broader issue is mixing raw types with generic types. If someone uses `Box raw = new Box()` (raw type), they can put any object into it, and the generic safety is completely bypassed. The compiler emits warnings for raw type usage, but these are often suppressed. The fix is to always use the diamond operator (`new Box<>()`) and never use raw types. Use bounded wildcards (`? extends T`, `? super T`) for method parameters to maintain type safety while allowing flexibility.

**Example:**
```java
class Box<T> {
    private Object item; // type-erased storage

    void set(T item) { this.item = item; }
    T get() { return (T) item; } // unchecked cast warning
}

// Broken: raw type bypasses generic safety
Box raw = new Box();
raw.set("hello");
raw.set(42);         // compiles with raw type
String s = (String) raw.get(); // ClassCastException at runtime

// Fixed: always use parameterized types
Box<String> safe = new Box<>();
safe.set("hello");
// safe.set(42); // compile error — type safe
```

## Q26: Why does this method shadow instead of override?

**A:** The subclass `Dog` declares a method `void speak(String volume)` while the parent `Animal` has `void speak()`. This is method **overloading**, not overriding, because the parameter signatures differ. The `@Override` annotation would catch this at compile time if present, but without it, the programmer believes they are overriding when they are actually adding a new overloaded method. At runtime, calling `animal.speak()` through a `Dog` reference still invokes `Animal.speak()`, not the expected `Dog` version.

The root cause is confusing overloading with overriding. Overriding requires the **exact same method signature** (name, parameters, and compatible return type). Changing the parameter list creates a new overload. This is a common shadowing bug where the subclass inadvertently creates a method that looks like an override but is not. The fix is to match the parent's method signature exactly and always use `@Override` to let the compiler verify.

**Example:**
```java
class Animal {
    void speak() { System.out.println("..."); }
}

class Dog extends Animal {
    // This is OVERLOADING, not overriding
    void speak(String volume) { System.out.println("WOOF " + volume); }

    // This is the actual override
    @Override
    void speak() { System.out.println("Woof!"); }
}

Animal a = new Dog();
a.speak(); // prints "Woof!" — calls Animal's method via override
// a.speak("loud"); // compile error: Animal has no speak(String)
```

## Q27: What is wrong with this deep copy implementation?

**A:** The copy constructor calls `this.address = new Address(addr)` for the `Address` field but does not handle the mutable collection field `List<String> hobbies`. The list is shared between the original and the copy — modifying one affects the other. This is a partial deep copy: it copies some fields deeply but leaves the collection as a shallow reference. True deep copying requires recursively copying all mutable reference-type fields.

The fix is to create a new list and populate it with copies of the original elements. For strings, no copying is needed (strings are immutable), but the list structure itself must be independent. A more robust approach uses serialization-based deep copy or a deep-copy utility, which handles arbitrarily nested object graphs. The critical lesson: a deep copy must copy every mutable reference, not just the top-level object.

**Example:**
```java
class Person {
    String name;
    Address address;
    List<String> hobbies;

    // Shallow copy: hobbies list is shared!
    Person(Person other) {
        this.name = other.name;
        this.address = new Address(other.address); // deep
        this.hobbies = other.hobbies; // SHALLOW — shared!
    }

    // Proper deep copy
    Person deepCopy(Person other) {
        Person copy = new Person();
        copy.name = other.name;
        copy.address = new Address(other.address);
        copy.hobbies = new ArrayList<>(other.hobbies); // independent list
        return copy;
    }
}
```

## Q28: Spot the memory leak in this caching mechanism

**A:** The cache uses a `HashMap` to store objects but never removes entries. Over time, the map grows without bound, retaining references to objects that are no longer needed elsewhere. Even after those objects become unreachable from application code, the cache's reference prevents garbage collection — this is a classic memory leak in managed languages. The JVM cannot reclaim the memory because the objects are technically still reachable (from the map).

The fix is to use a bounded cache with eviction policy. `LinkedHashMap` can be configured for LRU eviction, or you can use `WeakHashMap` (entries collected when the key has no other references) or a `Caffeine`/`Guava` cache with size and time-based eviction. Another approach is using soft/weak references, though these are less predictable. The key principle: any long-lived data structure that stores references must have a strategy for removing entries.

**Example:**
```java
// Leaky cache: unbounded HashMap
class LeakyCache {
    private Map<String, byte[]> cache = new HashMap<>();
    void put(String key, byte[] data) { cache.put(key, data); } // never evicted
}

// Fixed: bounded LRU cache
class BoundedCache {
    private Map<String, byte[]> cache = new LinkedHashMap<>(100, 0.75f, true) {
        @Override
        protected boolean removeEldestEntry(Map.Entry<String, byte[]> eldest) {
            return size() > 100; // evict oldest when over 100
        }
    };
}
```

## Q29: Why is this deep copy actually shallow?

**A:** The class implements `Cloneable` and overrides `clone()`, but calls `super.clone()` which performs a **shallow copy** — all reference fields are copied by reference, meaning the clone and the original share the same mutable objects. For fields like arrays, lists, or custom objects, both the original and the clone point to the same heap objects. Modifying one's list will modify the other's list.

The `Object.clone()` method creates a new instance and copies all fields bitwise. For primitives, this is a deep copy. For references, it is shallow — the reference is copied, not the object it points to. To achieve a true deep copy, you must manually clone or copy each mutable reference field after calling `super.clone()`. Alternatively, serialize the object and deserialize it for a serialization-based deep copy, or use a copy constructor that recursively copies all fields.

**Example:**
```java
class CloneableList implements Cloneable {
    private int[] data; // primitive array — shallow but safe (copy of reference)

    public CloneableList clone() {
        try {
            CloneableList copy = (CloneableList) super.clone();
            copy.data = this.data.clone(); // must explicitly clone
            return copy;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}

// Without explicit clone of data: both point to same array
CloneableList a = new CloneableList();
CloneableList b = a.clone();
b.data[0] = 99; // also changes a.data[0]
```

## Q30: What is wrong with this abstract class design?

**A:** The abstract class `Shape` has both abstract methods and concrete methods, but the concrete method `describe()` calls the abstract method `area()`. When a subclass like `Circle` is instantiated, the constructor in `Shape` (implicit or explicit) runs before the `Circle` constructor. If `describe()` is called from the `Shape` constructor, `area()` is invoked before the `Circle` fields are initialized, leading to operations on zero/null values.

This is the "calling overridable methods from a constructor" anti-pattern again, but in an abstract class context. The `this.area()` call in the base constructor dispatches to the subclass implementation, which may depend on state that has not yet been initialized. The fix is to never call overridable methods from constructors, or to ensure that the overridable method does not depend on subclass-specific state that might not yet be initialized.

**Example:**
```java
abstract class Shape {
    Shape() {
        System.out.println("Area: " + area()); // calls subclass method
    }
    abstract double area();
}

class Circle extends Shape {
    private double radius;

    Circle(double r) {
        super(); // area() called here — radius is still 0
        this.radius = r;
    }

    double area() { return Math.PI * radius * radius; } // returns 0 initially
}

// Fix: do not call overridable methods from constructors
```

## Q31: Find the Liskov violation in this hierarchy

**A:** The `Rectangle` class has `setWidth` and `setHeight` methods. `Square` extends `Rectangle` but overrides `setWidth` to also set `height`, and vice versa, to maintain the square invariant. This violates the Liskov Substitution Principle: code that works with a `Rectangle` reference may pass a `Square`, but calling `setWidth(5)` also changes the height, which is not expected behavior for a rectangle. The rectangle's width and height are supposed to be independently settable.

This is the classic Square-Rectangle problem that demonstrates LSP violations. Subclasses should honor the contracts of their parent classes — if `Rectangle` promises that `setWidth` does not affect `height`, `Square` breaks that promise. The fix is to avoid this inheritance entirely: make `Square` and `Rectangle` siblings implementing a common `Shape` interface, or use a factory that returns the appropriate type without exposing the inheritance relationship to clients.

**Example:**
```java
class Rectangle {
    protected int width, height;
    void setWidth(int w) { width = w; }
    void setHeight(int h) { height = h; }
    int area() { return width * height; }
}

class Square extends Rectangle {
    @Override
    void setWidth(int w) { width = w; height = w; } // violates expectation
    @Override
    void setHeight(int h) { width = h; height = h; } // violates expectation
}

void resize(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.area() == 50; // fails for Square: area is 100
}
```

## Q32: Why is this equals-hashCode contract broken with inheritance?

**A:** The parent class `Animal` implements `equals` and `hashCode` using the `name` field. The subclass `Pet` adds an `owner` field but does not override `equals` or `hashCode`. Two `Pet` objects with the same `name` but different `owners` are considered equal by the inherited `equals`, even though they are logically different. This violates the expectation that equal objects should share all relevant state.

The fix is either to override `equals` and `hashCode` in the subclass to include additional fields, or to make the parent class `final` (or its methods `final`) to prevent subclassing from breaking the contract. Using `getClass()` in `equals` (rather than `instanceof`) automatically rejects objects of different subclasses, but this is sometimes too strict. The key principle: `equals` and `hashCode` must be implemented together, using the same fields, and every subclass that adds significant state must update both.

**Example:**
```java
class Animal {
    String name;
    // uses only name
    public boolean equals(Object o) {
        return o instanceof Animal a && Objects.equals(name, a.name);
    }
    public int hashCode() { return Objects.hash(name); }
}

class Pet extends Animal {
    String owner; // NOT included in equals/hashCode

    Pet p1 = new Pet(); p1.name = "Rex"; p1.owner = "Alice";
    Pet p2 = new Pet(); p2.name = "Rex"; p2.owner = "Bob";
    // p1.equals(p2) is TRUE — but they have different owners!
}
```

## Q33: What is wrong with this singleton's thread safety?

**A:** The Singleton uses a simple null check without synchronization. In a multi-threaded environment, two threads can simultaneously check `instance == null`, both find it true, and both create separate instances. This breaks the singleton guarantee. The "check-then-act" sequence is a classic race condition — the instance field might be read and written non-atomically.

There are several fixes: (1) eager initialization (assign at class-load time, which is thread-safe), (2) `synchronized` method (safe but slow), (3) double-checked locking with `volatile` (fast after initialization), or (4) holder-class idiom (best performance, thread-safe). The `volatile` keyword in double-checked locking is essential — without it, a partially constructed instance may be visible to other threads due to instruction reordering. Modern Java provides `enum` singletons as the simplest thread-safe approach.

**Example:**
```java
// Broken: race condition
class Singleton {
    private static Singleton instance;
    private Singleton() {}
    static Singleton getInstance() {
        if (instance == null)          // Thread A checks
            instance = new Singleton(); // Thread B also creates one
        return instance;
    }
}

// Fixed: holder idiom (best)
class Singleton {
    private Singleton() {}
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    static Singleton getInstance() { return Holder.INSTANCE; }
}
```

## Q34: Spot the initialization order bug in this class hierarchy

**A:** The parent class constructor assigns a value to `type` using a method that the subclass overrides. Due to Java's initialization order (parent constructor runs first), the overridden method is called before the subclass fields are initialized. The subclass method `getCategory()` reads `subType`, which is still `null` (its default value) because the subclass constructor has not yet executed. The result is a `NullPointerException` or incorrect default value.

The initialization order in Java is: (1) parent static fields/static blocks, (2) child static fields/static blocks, (3) parent instance fields/instance initializer, (4) parent constructor, (5) child instance fields/instance initializer, (6) child constructor. Calling overridable methods at step 4 accesses uninitialized child fields. The fix is to never call overridable methods from constructors, or to initialize fields at declaration rather than in the constructor.

**Example:**
```java
class Parent {
    String type;
    Parent() {
        type = getCategory(); // calls overridden method
    }
    String getCategory() { return "parent"; }
}

class Child extends Parent {
    String subType = "child";
    @Override
    String getCategory() {
        return subType.toUpperCase(); // subType is null here!
    }
}
```

## Q35: Why does this composite pattern leak objects?

**A:** The Composite node holds references to its children, and children can hold references back to their parent (bidirectional reference). When the composite is no longer needed, if the parent reference in each child is not cleared, the GC cannot collect any node in the tree because every node is reachable from every other node through the bidirectional links. This creates a circular reference that prevents garbage collection.

The fix depends on the use case: (1) use weak references for the parent pointer, (2) explicitly clear children and parent references when disposing, or (3) use a tree structure where the parent owns the children and there are no back-references. In Java, the GC can handle circular references among unreachable objects, but if any external reference to any node in the tree exists, all nodes remain reachable. The key is to ensure that removing the root from the application's references makes the entire tree unreachable.

**Example:**
```java
class CompositeNode {
    private List<CompositeNode> children = new ArrayList<>();
    private CompositeNode parent; // back-reference leaks

    void dispose() {
        for (CompositeNode child : children) {
            child.parent = null; // break back-reference
            child.dispose();
        }
        children.clear();
    }
}
```

## Q36: What is wrong with this immutable class?

**A:** The class declares fields as `final` but one field is a mutable collection (`List<String>`). While the reference is final (cannot be reassigned), the list's contents can still be modified through the reference. `final` only prevents reassignment of the reference, not mutation of the object it points to. Callers can `add()`, `remove()`, or `clear()` the list, breaking immutability.

The fix is to return a defensive copy of the mutable collection from the getter, and store a copy of the collection in the constructor. Alternatively, use `Collections.unmodifiableList` to wrap the stored list. The constructor should copy the incoming list to prevent callers from retaining a reference and modifying it after construction. Java 9+ provides `List.of()` and `Map.of()` for creating unmodifiable collections.

**Example:**
```java
// Broken: list is mutable despite final field
class User {
    private final String name;
    private final List<String> roles;

    User(String name, List<String> roles) {
        this.name = name;
        this.roles = roles; // stored reference is mutable
    }
    List<String> getRoles() { return roles; } // exposes mutable state
}

// Fixed: truly immutable
class User {
    private final String name;
    private final List<String> roles;

    User(String name, List<String> roles) {
        this.name = name;
        this.roles = List.copyOf(roles); // defensive copy
    }
    List<String> getRoles() { return roles; } // already unmodifiable
}
```

## Q37: Find the object lifecycle bug

**A:** The class registers itself as an observer in the constructor but never unregisters in the destructor (or `close`/`dispose` method). When the object is discarded, the subject still holds a strong reference to it, preventing garbage collection. The object is effectively immortal as long as the subject exists, even though the application no longer uses it. This is a classic lifecycle management bug.

The fix is to implement a cleanup method (`dispose`, `close`, `release`) that unregisters from the subject, and ensure it is called when the object is no longer needed. Alternatively, use `WeakReference` or `WeakHashMap` so the subject does not prevent GC. In frameworks like Spring, lifecycle callbacks (`@PreDestroy`) handle this automatically. The general principle: any object that registers with a global or long-lived entity must have a corresponding deregistration mechanism.

**Example:**
```java
class EventHandler {
    EventBus bus;

    EventHandler(EventBus bus) {
        this.bus = bus;
        bus.register(this); // registers: now bus holds reference to this
    }

    // Missing: no unregister in destructor or dispose method
    // When EventHandler is discarded, bus still references it

    // Fix
    void dispose() {
        bus.unregister(this); // break the reference
    }
}
```

## Q38: Why does this proxy pattern break the expected behavior?

**A:** The proxy class implements the same interface as the real object but adds caching logic. The bug is that the proxy does not invalidate the cache when the real object's state changes externally. For example, if the real database record is updated by another process, the proxy continues serving stale cached data. The proxy assumes it is the only accessor of the real object, but in a concurrent or distributed system, this is often not true.

The fix is to implement cache invalidation based on timestamps, version numbers, or event notifications. Alternatively, the proxy can use short TTL (time-to-live) cache entries. The deeper lesson: proxies that cache must have a strategy for cache coherence. Without it, the proxy becomes a source of data inconsistencies. Proxies for logging or access control do not have this issue because they do not alter the data returned.

**Example:**
```java
class CachedDBProxy implements Database {
    private Database realDB;
    private Map<String, Record> cache = new HashMap<>();

    Record get(String id) {
        if (cache.containsKey(id)) return cache.get(id); // may be stale
        Record r = realDB.get(id);
        cache.put(id, r);
        return r;
    }

    // Missing: no cache invalidation on external writes
    void invalidate(String id) { cache.remove(id); }
}
```

## Q39: What is wrong with this factory method return type?

**A:** The factory method returns a base type (`Animal`), but the client code immediately downcasts it to a specific subtype (`Dog`) without checking. If the factory returns a `Cat` for certain inputs, the downcast throws a `ClassCastException` at runtime. The factory's contract does not guarantee which subtype it returns, but the client assumes a specific subtype.

The fix is either to (1) make the factory method generic or typed so the return type is specific, (2) use the visitor pattern or polymorphism to avoid downcasting, or (3) use sealed interfaces (Java 17+) so the client can pattern-match safely. Downcasting from a factory return type is a design smell — it suggests the factory is returning too broad a type, or the client should not care about the concrete type and should rely on the base interface.

**Example:**
```java
// Broken: unsafe downcast
Animal a = AnimalFactory.create("dog");
Dog d = (Dog) a; // ClassCastException if factory returns Cat

// Fixed: typed factory
static Dog createDog(String breed) { return new Dog(breed); }

// Or use sealed types (Java 17+)
sealed interface Animal permits Dog, Cat {}
// Client can use switch with pattern matching safely
```

## Q40: Spot the visibility issue in this package-private scenario

**A:** The class has a package-private method that is overridden by a subclass in a different package. The subclass widens the visibility to `public` (which is allowed by Java), but client code holding a parent-type reference can still only see the package-private method if they are in the parent's package. This creates a confusing situation where the same method call resolves differently depending on the compile-time type and the caller's package.

The deeper issue is that the parent class intended the method to be an internal implementation detail (package-private), but the subclass exposes it publicly, violating the parent's encapsulation intent. The fix is to either (1) make the parent method `protected` if subclasses should call it, (2) make it `public` if it should be part of the public API, or (3) prevent overriding with `final`. Inconsistent visibility across a hierarchy creates subtle bugs where behavior changes based on reference type rather than object type.

**Example:**
```java
// package: com.company.core
class Base {
    void internalMethod() { /* package-private */ } // intended for internal use
}

// package: com.company.sub
class Sub extends Base {
    @Override
    public void internalMethod() { /* now public */ } // widens visibility
}

// In com.company.other (different package)
Base b = new Sub();
b.internalMethod(); // compile error: Base.internalMethod is not accessible
Sub s = (Sub) b;
s.internalMethod(); // works: Sub.internalMethod is public
```

## Q41: Why does this observer pattern cause memory leaks?

**A:** The subject (observable) holds strong references to all registered observers in a list. If observers are not explicitly unregistered when they are no longer needed, the subject prevents them from being garbage collected. This is especially problematic in GUI applications where views register as observers but are destroyed when screens are dismissed. The subject still holds references to destroyed views, preventing GC and causing memory leaks.

The fix is to (1) use `WeakReference` for observer storage (as `WeakHashMap` does for keys), (2) require explicit unregistration in a `dispose`/`detach` lifecycle method, or (3) use event buses with lifecycle-aware registration (like Android's `LiveData`). The best practice is to always pair registration with unregistration. In modern frameworks, lifecycle-aware components automatically handle this, but in custom implementations, the developer must ensure proper cleanup.

**Example:**
```java
class EventBus {
    private List<WeakReference<Observer>> observers = new ArrayList<>();

    void register(Observer o) {
        observers.add(new WeakReference<>(o));
    }

    void notify(String event) {
        observers.removeIf(ref -> ref.get() == null); // clean dead refs
        observers.forEach(ref -> {
            Observer o = ref.get();
            if (o != null) o.onEvent(event);
        });
    }
}
```

## Q42: What is wrong with this copy constructor?

**A:** The copy constructor does not make a defensive copy of the mutable `Date` field. When the original object's `Date` is modified after copying, the copy's `Date` also changes because both point to the same `Date` object. The copy constructor is supposed to create an independent copy, but the shared mutable reference undermines this.

The fix is to create a new `Date` object from the original's time value: `this.created = new Date(other.created.getTime())`. Alternatively, use `Instant` (immutable) instead of `Date`. This applies to all mutable reference-type fields: arrays, collections, `Date`, `Calendar`, `StringBuilder`, etc. A copy constructor that does not defensively copy all mutable fields is a shallow copy masquerading as a deep copy, leading to subtle bugs.

**Example:**
```java
class Event {
    private String name;
    private Date created;

    // Broken: shared Date reference
    Event(Event other) {
        this.name = other.name;
        this.created = other.created; // same Date object!
    }

    // Fixed: defensive copy
    Event(Event other) {
        this.name = other.name;
        this.created = new Date(other.created.getTime());
    }
}

Event e1 = new Event("party");
Event e2 = new Event(e1);
e1.created.setTime(0); // e2.created is also changed!
```

## Q43: Find the circular reference bug

**A:** Class `A` has a field of type `B`, and class `B` has a field of type `A`. Both classes call each other's constructors, creating a circular dependency. This can cause a `StackOverflowError` during instantiation because each constructor tries to create the other, which tries to create the first, ad infinitum. Even if the constructors are lazy (using setters), the circular reference can cause issues with serialization, clone, and garbage collection.

The fix is to break the cycle by (1) introducing a third class that manages the relationship, (2) using a lazy initialization pattern where one side is set after construction, (3) redesigning the domain model to eliminate the bidirectional dependency, or (4) using weak references for one direction. In ORMs like Hibernate, bidirectional relationships require one side to be `mappedBy` (non-owning), and circular serialization requires `@JsonIgnore` or similar.

**Example:**
```java
// Circular constructor dependency: StackOverflowError
class Order {
    OrderItem item;
    Order() { item = new OrderItem(this); } // creates OrderItem
}

class OrderItem {
    Order order;
    OrderItem(Order o) {
        this.order = o;
        // if Order constructor creates OrderItem again: infinite loop
    }
}

// Fix: lazy initialization
class Order {
    OrderItem item;
    void setItem(OrderItem i) { this.item = i; }
}
```

## Q44: Why does this builder pattern produce inconsistent state?

**A:** The builder's `build()` method does not validate all required fields before constructing the object. If a required field is missing (e.g., `name` is null), the constructed object has an invalid state that may cause `NullPointerException` or incorrect behavior later. The builder should validate invariants at `build()` time and throw an exception immediately rather than allowing a partially constructed object to escape.

Additionally, the builder itself might allow conflicting configurations (e.g., setting both `format = "json"` and `format = "xml"`). The builder should enforce consistency — either through mutual exclusion checks or by having separate builder types for different configurations. The immutability of the built object is also important: the builder should not retain a reference to the built object that could be used to modify it after construction.

**Example:**
```java
class HttpRequest {
    private final String url;
    private final String method;
    private final Duration timeout;

    private HttpRequest(Builder b) {
        if (b.url == null) throw new IllegalStateException("url required");
        this.url = b.url;
        this.method = b.method != null ? b.method : "GET";
        this.timeout = b.timeout != null ? b.timeout : Duration.ofSeconds(30);
    }

    static class Builder {
        private String url;
        private String method;
        private Duration timeout;

        Builder url(String u) { this.url = u; return this; }
        Builder method(String m) { this.method = m; return this; }
        Builder timeout(Duration t) { this.timeout = t; return this; }
        HttpRequest build() { return new HttpRequest(this); } // validates
    }
}
```

## Q45: What is wrong with this use of instanceof for dispatch?

**A:** The code uses a chain of `instanceof` checks to determine the type of an object and call type-specific behavior. This violates the Open-Closed Principle because adding a new type requires modifying the method with a new `instanceof` check. It also suggests that polymorphism is not being leveraged — the type-specific behavior should be in virtual methods on the objects themselves, not in external conditional logic.

The `instanceof` chain is a code smell indicating missing polymorphism. The fix is to add a virtual method to the base interface/class and override it in each subclass, eliminating the need for type checks. If the behavior genuinely depends on the combination of two types (e.g., `Shape` × `Renderer`), use the Visitor pattern. If you must use `instanceof`, consider a `switch` with pattern matching (Java 17+) for cleaner syntax.

**Example:**
```java
// Broken: instanceof chain
void draw(Object shape) {
    if (shape instanceof Circle c) c.drawCircle();
    else if (shape instanceof Rect r) r.drawRect();
    // adding Triangle requires modifying this method
}

// Fixed: polymorphism
interface Shape { void draw(); }
class Circle implements Shape { public void draw() { drawCircle(); } }
class Rect implements Shape { public void draw() { drawRect(); } }
// adding Triangle only requires a new class
```

## Q46: Spot the thread-safety issue in this shared mutable state

**A:** The class stores mutable state in instance fields (`count`, `lastAccess`) that are read and written by multiple threads without synchronization. `count++` is not atomic — it involves read, increment, and write as three separate operations. Two threads executing `count++` simultaneously can overwrite each other's increments, losing one update. Similarly, `lastAccess` may be partially written by one thread and read by another, observing a corrupted value.

The fix depends on the requirements: (1) use `AtomicInteger` for simple counters, (2) use `synchronized` for compound operations, (3) use `volatile` for independent reads/writes, or (4) use immutable objects. The key insight: `volatile` ensures visibility but not atomicity — it is insufficient for read-modify-write operations. For collections, use `ConcurrentHashMap` or synchronized wrappers. For complex state, consider thread confinement (one thread per task) or lock-based synchronization.

**Example:**
```java
// Broken: race condition
class Counter {
    private int count = 0;
    void increment() { count++; } // not atomic
    int getCount() { return count; }
}

// Fixed: atomic operation
class Counter {
    private final AtomicInteger count = new AtomicInteger(0);
    void increment() { count.incrementAndGet(); }
    int getCount() { return count.get(); }
}
```

## Q47: Why does this visitor pattern fail for new element types?

**A:** The visitor interface has a `visit` method for each element type (`visitDog`, `visitCat`). When a new element type (`visitBird`) is added, the interface must be modified, which breaks all existing visitor implementations. This is the "expression problem" — the Visitor pattern makes it easy to add new operations but difficult to add new element types. Every concrete visitor must implement the new method, even if it does not care about the new type.

This violates the Open-Closed Principle for element types. The trade-off is intentional: Visitor optimizes for the case where operations change frequently but the element hierarchy is stable. If element types change often, Visitor is the wrong pattern — use polymorphism instead. The fix for adding new types without breaking existing visitors is to add a default method in the interface (Java 8+) that throws `UnsupportedOperationException` or does nothing, allowing existing visitors to compile without modification.

**Example:**
```java
interface AnimalVisitor {
    void visitDog(Dog d);
    void visitCat(Cat c);
    // Adding visitBird breaks ALL existing visitors
    // void visitBird(Bird b);
}

// Java 8+ fix: default method
interface AnimalVisitor {
    void visitDog(Dog d);
    void visitCat(Cat c);
    default void visitBird(Bird b) {
        throw new UnsupportedOperationException();
    }
}
```

## Q48: What is wrong with this clone method?

**A:** The `clone()` method does not call `super.clone()` and instead uses `new` to create a copy. This bypasses the `Cloneable` contract and may not correctly copy fields defined in parent classes. The `Cloneable` interface combined with `super.clone()` creates a field-by-field copy (shallow), which is the expected behavior. Using `new` means the copy must manually replicate all field initialization, which is error-prone as the class evolves.

Additionally, the method does not handle the case where the object contains final fields. `super.clone()` can set final fields (it uses `Unsafe` or similar mechanisms), but a `new` constructor cannot set final fields of the same object without reflection. The standard pattern is: (1) call `super.clone()`, (2) clone mutable reference fields, (3) return the clone. If `Cloneable` is implemented correctly, this is simpler and more robust than manual copying.

**Example:**
```java
// Broken: bypasses Cloneable
class Data implements Cloneable {
    private int[] values;

    public Data clone() {
        Data copy = new Data(); // new, not super.clone()
        copy.values = Arrays.copyOf(values, values.length);
        return copy;
    }
}

// Correct: uses super.clone()
class Data implements Cloneable {
    private int[] values;

    public Data clone() {
        try {
            Data copy = (Data) super.clone();
            copy.values = values.clone(); // clone mutable fields
            return copy;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## Q49: Find the race condition in lazy initialization

**A:** The lazy initialization pattern checks `if (instance == null)` then creates the instance, but without synchronization. Between the null check and the assignment, another thread can also see `null` and create a second instance. This is a Time-of-Check-to-Time-of-Use (TOCTOU) race condition. The first thread may also see a partially constructed instance from the second thread due to instruction reordering.

There are three fixes: (1) simple synchronization (slow), (2) double-checked locking with `volatile` (fast), or (3) the initialization-on-demand holder idiom (best). The `volatile` keyword in double-checked locking is essential — without it, the JVM may reorder the instance field write before the constructor finishes, and another thread may see a non-null but partially constructed instance. The holder idiom exploits the JVM's class-loading guarantees for thread safety without explicit synchronization.

**Example:**
```java
// Race condition
class Config {
    private static Config instance;
    static Config get() {
        if (instance == null) instance = new Config(); // TOCTOU
        return instance;
    }
}

// Double-checked locking (correct)
class Config {
    private static volatile Config instance;
    static Config get() {
        if (instance == null) {
            synchronized (Config.class) {
                if (instance == null) instance = new Config();
            }
        }
        return instance;
    }
}
```

## Q50: Why is this decorator not preserving the original interface contract?

**A:** The decorator wraps a `List` but overrides `size()` to return a filtered count instead of the actual list size. This violates the contract that `size()` should return the number of elements accessible via `get(i)` for `i` in `0..size()-1`. Client code that iterates using `size()` and `get()` will throw `IndexOutOfBoundsException` because the decorated `size()` is smaller than the backing list's actual size.

Decorators must preserve the contracts of all methods in the interface they implement. If the decorator filters elements, it must ensure that `size()` matches the count of elements returned by `get()`, `iterator()`, and other access methods. The decorator changes behavior but must not break the interface's semantic guarantees. When wrapping collection types, consider extending `AbstractList` which provides consistent default implementations that override together.

**Example:**
```java
// Broken: size() contract violated
class EvenFilterList implements List<Integer> {
    private List<Integer> backing;
    // ...
    public int size() {
        return (int) backing.stream().filter(n -> n % 2 == 0).count();
    }
    public Integer get(int index) {
        // index is relative to filtered list, not backing list
        // but backing.get(index) may be out of bounds
        return backing.get(index); // IndexOutOfBoundsException
    }
}

// Fix: use AbstractList for consistent filtering
class EvenFilterList extends AbstractList<Integer> {
    private List<Integer> backing;
    private List<Integer> filtered;

    EvenFilterList(List<Integer> list) {
        this.backing = list;
        this.filtered = list.stream().filter(n -> n % 2 == 0).toList();
    }
    public int size() { return filtered.size(); }
    public Integer get(int index) { return filtered.get(index); }
}
```

## Q51: What smell do you see and how to refactor?

**A:** The class is a God Object — it handles database access, email sending, PDF generation, and logging all in one class. Each method does too much, and unrelated responsibilities are tangled together. This violates the Single Responsibility Principle and makes the class difficult to test, maintain, and understand. Changes to email logic risk breaking database logic, and vice versa.

The refactoring strategy is to extract each responsibility into its own class: `UserRepository`, `EmailService`, `PdfGenerator`, `AuditLogger`. A Facade class can coordinate these subsystems for clients that need a simple interface. Each extracted class becomes independently testable and can evolve separately. The original God Class is either eliminated or reduced to a thin coordination layer.

**Example:**
```java
// Before: God Class
class UserManager {
    void createUser(String name, String email) {
        // 50 lines of DB code
        // 30 lines of email code
        // 20 lines of PDF code
        // 10 lines of logging
    }
}

// After: Extracted responsibilities
class UserRepository { void save(User u) { /* DB only */ } }
class EmailService { void sendWelcome(User u) { /* email only */ } }
class PdfGenerator { byte[] generateCertificate(User u) { /* PDF only */ } }

class UserManager {
    private UserRepository repo = new UserRepository();
    private EmailService email = new EmailService();
    private PdfGenerator pdf = new PdfGenerator();

    void createUser(String name, String emailAddress) {
        User u = new User(name, emailAddress);
        repo.save(u);
        email.sendWelcome(u);
    }
}
```

## Q52: Review this PR: identify all issues

**A:** The PR contains multiple code smells and design issues that should be flagged in review. The method `processData` is 200 lines long, making it hard to understand and test. It mixes parsing, validation, transformation, and persistence in one method. There is duplicated validation logic between `processData` and `validateInput` that should be consolidated. The error handling swallows exceptions with empty catch blocks, hiding failures. There is no unit test coverage for the new code.

Additionally, the code uses raw types for collections (`List` instead of `List<User>`), missing generic type safety. The naming is inconsistent — some methods use camelCase, others use underscores. Magic numbers are scattered throughout (thresholds, limits) that should be constants. The PR also modifies an unrelated utility class, suggesting the changes should be split into separate PRs for easier review.

**Example:**
```java
// Issues flagged in review:
// 1. Method too long (200 lines)
// 2. Mixed responsibilities
// 3. Swallowed exceptions
void processData(String input) {
    try {
        // parsing logic...
        // validation logic (duplicated elsewhere)
        // transformation logic
        // persistence logic
    } catch (Exception e) {
        // empty catch: silent failure
    }
}

// Fix: extract methods, handle exceptions, add types
void processData(String input) {
    ParsedData data = parse(input);
    ValidatedData valid = validate(data);
    TransformedData result = transform(valid);
    repository.save(result);
}
```

## Q53: How would you refactor this God Class?

**A:** The `OrderProcessor` class handles order validation, payment processing, inventory management, shipping calculation, notification sending, and receipt generation. This is a textbook God Class that violates SRP and makes every change risky. The refactoring extracts each responsibility into a service class and creates a coordinating orchestrator.

Step 1: Identify cohesive groups of methods (validation, payment, shipping, etc.). Step 2: Extract each group into a dedicated service class with a focused interface. Step 3: Replace the God Class with a thin orchestrator that delegates to services. Step 4: The orchestrator handles the workflow (validate → pay → ship → notify) without implementing any business logic itself. Step 5: Each service is independently testable and can be replaced or modified without affecting others.

**Example:**
```java
// Orchestrator: coordinates, does not implement
class OrderOrchestrator {
    private ValidationService validation;
    private PaymentService payment;
    private InventoryService inventory;
    private ShippingService shipping;
    private NotificationService notifications;

    OrderResult process(Order order) {
        validation.validate(order);
        payment.charge(order);
        inventory.reserve(order.getItems());
        ShippingInfo ship = shipping.calculate(order);
        notifications.sendConfirmation(order, ship);
        return new OrderResult(order.getId(), ship);
    }
}
```

## Q54: What SOLID violation exists here?

**A:** The class `ReportGenerator` generates reports in PDF, HTML, and CSV formats, and also handles database queries to fetch report data, email sending to distribute reports, and scheduling when reports run. This violates the Single Responsibility Principle — the class has at least four reasons to change (data fetching, format generation, distribution, scheduling).

The ISP is also violated because the `ReportGenerator` interface exposes methods for all operations: `generatePDF`, `generateHTML`, `sendEmail`, `scheduleReport`. Clients that only need report generation are forced to depend on methods they do not use. The DIP is violated because the class depends directly on concrete database, email, and PDF libraries rather than abstractions.

**Example:**
```java
// Violates SRP: too many responsibilities
class ReportGenerator {
    ResultSet fetchData(String query) { /* DB access */ }
    byte[] generatePDF(ResultSet data) { /* PDF generation */ }
    String generateHTML(ResultSet data) { /* HTML generation */ }
    void sendEmail(byte[] attachment) { /* email sending */ }
    void schedule(String cron) { /* scheduling */ }
}

// Fix: separate concerns
interface DataSource { ResultSet fetch(String query); }
interface ReportFormatter { byte[] format(ResultSet data); }
interface ReportDistributor { void distribute(byte[] report); }
interface ReportScheduler { void schedule(Runnable task, String cron); }
```

## Q55: Identify the code smells in this module

**A:** The module has Feature Envy — the `OrderValidator` class accesses `Order`'s fields more than its own, suggesting the validation logic belongs in `Order` or a method on `Order`. There is Data Clumping: `String firstName, String lastName, String email, String phone` appear together in multiple classes — they should be extracted into a `ContactInfo` value object. There is Switch Statement duplication: the same switch on `OrderStatus` appears in three classes.

Additionally, there is Dead Code — several private methods are never called. There is Primitive Obsession: order status is represented as a `String` instead of an enum, leading to string comparisons and typos. There is Divergent Change in the `OrderService` class — it changes for both business rule changes and database schema changes, indicating mixed responsibilities.

**Example:**
```java
// Data Clumping: repeated parameter groups
class Order {
    String firstName, lastName, email, phone;
}
class Invoice {
    String firstName, lastName, email, phone;
}

// Fix: extract value object
class ContactInfo {
    String firstName, lastName, email, phone;
}

// Primitive Obsession: String status
String status = "pending"; // typo-prone

// Fix: use enum
enum OrderStatus { PENDING, CONFIRMED, SHIPPED, DELIVERED }
```

## Q56: This PR introduces a long parameter list: how would you improve it?

**A:** The method `createUser(String firstName, String lastName, String email, String phone, String address, String city, String state, String zip, boolean sendWelcome, boolean admin)` has 10 parameters, making it error-prone and hard to read. Callers cannot easily tell which argument goes where, especially when several parameters are the same type (all Strings).

The refactoring options are: (1) Introduce Parameter Object — group related parameters into a `UserRegistrationRequest` class. (2) Use Builder pattern — `UserRequest.builder().firstName("John").email("j@x.com").build()`. (3) Use Named parameters via a configuration object. The Builder pattern is best when many parameters are optional. The Parameter Object is best when the grouped parameters form a cohesive concept. Both approaches make the method signature self-documenting and reduce the chance of argument transposition.

**Example:**
```java
// Before: 10 parameters
User createUser("John", "Doe", "j@x.com", "555-1234",
    "123 Main", "NYC", "NY", "10001", true, false);

// After: Parameter Object
class UserRegistrationRequest {
    String firstName, lastName, email, phone;
    Address address;
    boolean sendWelcomeEmail;
    boolean makeAdmin;
}

User createUser(new UserRegistrationRequest(
    firstName="John", lastName="Doe", email="j@x.com", ...));
```

## Q57: Review this code for primitive obsession and suggest alternatives

**A:** The code uses raw `String`, `int`, and `boolean` types where domain-specific types would be clearer and safer. Order IDs are passed as `String`, status as `String`, price as `double`, and flags as `boolean`. This leads to confusing method signatures (`process(String id, String status, double price, boolean urgent)`) and allows invalid values (any string as status, negative prices).

The fix is to introduce value objects: `OrderId`, `OrderStatus` (enum), `Money`, and a status enum instead of booleans. Value objects encapsulate validation (a `Money` class ensures non-negative amounts), provide type safety (you cannot pass a `ProductId` where an `OrderId` is expected), and make the code self-documenting. Enums eliminate invalid status values. The `Money` class prevents floating-point precision issues with `double`.

**Example:**
```java
// Before: primitive obsession
void process(String orderId, String status, double amount, boolean paid) {
    // status could be any string, amount could be negative
}

// After: domain types
class OrderId { private final String value; /* validated */ }
enum OrderStatus { PENDING, PAID, SHIPPED }
class Money { private final BigDecimal amount; /* non-negative */ }

void process(OrderId id, OrderStatus status, Money amount) {
    // type-safe, self-documenting, validated
}
```

## Q58: How would you refactor this parallel inheritance hierarchy?

**A:** Two parallel hierarchies (` Shape/Drawing` and `ShapeEditor/DrawingEditor`) have the same structure: `Circle` pairs with `CircleEditor`, `Rect` pairs with `RectEditor`. Adding a new shape requires adding two classes (the shape and its editor). This is the Parallel Hierarchy smell — the hierarchies evolve in lockstep, indicating that the editing behavior should be part of the shape, not a separate hierarchy.

The refactoring options: (1) Use the Visitor pattern to put operations in the visitor, eliminating the editor hierarchy. (2) Use the Strategy pattern — each shape has an editing strategy that encapsulates the editing behavior. (3) Move the editing methods directly into the shape classes as virtual methods. Option 3 is simplest when the editing behavior naturally belongs to the shape. Option 1 is best when there are many operations beyond editing.

**Example:**
```java
// Parallel hierarchy: two class trees evolving together
class Circle extends Shape { void draw() { /* ... */ } }
class CircleEditor extends ShapeEditor { void edit(Circle c) { /* ... */ } }
class Rect extends Shape { void draw() { /* ... */ } }
class RectEditor extends ShapeEditor { void edit(Rect r) { /* ... */ } }

// Refactored: Visitor eliminates the editor hierarchy
interface ShapeVisitor {
    void visit(Circle c);
    void visit(Rect r);
}

class EditVisitor implements ShapeVisitor {
    public void visit(Circle c) { /* edit circle */ }
    public void visit(Rect r) { /* edit rect */ }
}
```

## Q59: This code has duplicate logic across classes: propose a refactoring strategy

**A:** Three classes (`EmailSender`, `SmsSender`, `PushSender`) all implement the same pattern: validate the recipient, format the message, send via the channel, log the result. The validation and logging logic is nearly identical across all three classes, with only the format and send steps differing. This is DRY (Don't Repeat Yourself) violation.

The refactoring strategy: extract the common algorithm into a Template Method base class. The base class defines the template method `send(recipient, message)` that calls `validate`, `format`, `channelSend`, and `log` in sequence. Each subclass overrides `format` and `channelSend` with channel-specific logic. The `validate` and `log` methods are shared in the base class. This eliminates the duplication while keeping each channel's unique behavior in its own class.

**Example:**
```java
abstract class MessageSender {
    final void send(Recipient r, String msg) {
        validate(r);        // shared
        String formatted = format(msg); // subclass-specific
        channelSend(r, formatted);       // subclass-specific
        log(r, msg);        // shared
    }
    void validate(Recipient r) { /* common validation */ }
    void log(Recipient r, String msg) { /* common logging */ }
    abstract String format(String msg);
    abstract void channelSend(Recipient r, String msg);
}

class EmailSender extends MessageSender {
    String format(String msg) { return "<html>" + msg + "</html>"; }
    void channelSend(Recipient r, String msg) { /* SMTP */ }
}
```

## Q60: Review: what would you flag in code review?

**A:** In a comprehensive code review, I would flag: (1) **Missing null checks** — several methods receive parameters that could be null but are dereferenced without checking. (2) **Inconsistent error handling** — some methods throw exceptions, others return null, and some log and continue. The team needs a consistent error handling strategy. (3) **Thread safety** — the `CacheManager` class uses a non-synchronized `HashMap` but is accessed from multiple threads. (4) **Hard-coded values** — database connection strings and API endpoints are hard-coded instead of using configuration.

(5) **Missing tests** — new code has no unit tests. (6) **Naming issues** — method names like `doStuff` and `process2` are not descriptive. (7) **Too broad exception handling** — `catch (Exception e)` masks specific errors. (8) **Code duplication** — the same validation logic appears in three methods. I would recommend extracting it into a shared utility.

**Example:**
```java
// Flags from code review:
// 1. No null check
String name = user.getName().trim(); // NPE if getName() returns null

// 3. Thread-unsafe
class CacheManager {
    Map<String, Object> cache = new HashMap<>(); // not thread-safe
}

// 7. Overly broad catch
try {
    processData();
} catch (Exception e) {
    // too broad: catches NPE, IO, everything
}
```

## Q61: Refactor this long parameter list

**A:** The method `createOrder(int userId, String product, int qty, double price, String currency, String couponCode, boolean giftWrap, String giftMessage, String shippingAddress, String shippingMethod)` has 10 parameters with mixed types. This is nearly unreadable and extremely error-prone — the fifth and sixth parameters are both strings, making transposition likely.

The refactoring introduces a `CreateOrderRequest` class that encapsulates all parameters as named fields. The method becomes `createOrder(CreateOrderRequest request)`. This provides type safety, self-documentation, and allows adding optional fields without breaking existing callers. The request class can include validation logic (`@Valid` annotations or a `validate()` method) to ensure the request is complete before processing. For even better ergonomics, the request class uses the Builder pattern.

**Example:**
```java
class CreateOrderRequest {
    private int userId;
    private String product;
    private int quantity;
    private Money price;
    private String couponCode;     // nullable
    private boolean giftWrap;
    private String giftMessage;    // nullable
    private Address shippingAddress;
    private ShippingMethod shippingMethod;

    // builder, validation...
}

Order createOrder(CreateOrderRequest req) {
    // clear, readable, type-safe
}
```

## Q62: What design issue makes this code hard to test?

**A:** The class creates its own dependencies internally (`new DatabaseConnection()`, `new EmailClient()`, `new Logger()`), making it impossible to substitute test doubles (mocks, stubs) during testing. This violates the Dependency Inversion Principle — high-level modules depend on low-level modules instead of abstractions. The code is tightly coupled to its infrastructure, so testing requires a real database, email server, and file system.

The fix is Constructor Injection: pass dependencies through the constructor, accepting interfaces rather than concrete classes. The production code injects real implementations; test code injects mocks. This makes the class independently testable in isolation. Frameworks like Spring automate dependency injection, but even without a framework, manual constructor injection is simple and effective. The key principle: a class should never create its own dependencies.

**Example:**
```java
// Untestable: creates dependencies internally
class OrderService {
    private Database db = new Database();
    private EmailClient email = new EmailClient();

    void processOrder(Order o) {
        db.save(o);
        email.send(o.getCustomerEmail());
    }
}

// Testable: dependencies injected
class OrderService {
    private final Database db;
    private final EmailClient email;

    OrderService(Database db, EmailClient email) {
        this.db = db; this.email = email;
    }

    void processOrder(Order o) {
        db.save(o);
        email.send(o.getCustomerEmail());
    }
}
// Test: new OrderService(mockDb, mockEmail)
```

## Q63: Identify and fix the primitive obsession

**A:** The code uses `String` for email addresses, phone numbers, and URLs, `int` for user IDs, and `double` for monetary amounts. This leads to validation logic scattered across the codebase (checking email format in every method that receives one), floating-point precision bugs with money, and no compile-time protection against mixing up ID types (a `productId` passed where `userId` is expected compiles fine because both are `int`).

The fix introduces domain-specific types: `Email`, `PhoneNumber`, `Money`, `UserId`, `ProductId`. Each type encapsulates its own validation in the constructor and provides meaningful `toString()`, `equals()`, and `hashCode()` implementations. The `Money` class uses `BigDecimal` instead of `double` to avoid precision issues. Value types with private constructors and factory methods ensure that only valid values can be created.

**Example:**
```java
class Email {
    private final String value;
    private Email(String v) { this.value = v; }

    static Email of(String v) {
        if (!v.matches("^[\\w.-]+@[\\w.-]+\\.\\w+$"))
            throw new InvalidEmailException(v);
        return new Email(v);
    }
    String value() { return value; }
}

class Money {
    private final BigDecimal amount;
    private final Currency currency;

    static Money dollars(double v) {
        return new Money(BigDecimal.valueOf(v), Currency.USD);
    }
    Money add(Money other) { /* validated addition */ }
}
```

## Q64: How would you address this inappropriate intimacy smell?

**A:** The `Order` class and `Customer` class access each other's internal fields directly — `Order` reaches into `customer.creditLimit` and `Customer` reads `order.items` to calculate totals. This is the Inappropriate Intimacy smell: two classes know too much about each other's internal structure, creating tight coupling. Changes to either class's internals break the other. The classes cannot be tested, understood, or reused independently.

The refactoring: (1) Move the behavior to the class that owns the data. If `Order` needs to check credit, move `hasSufficientCredit(amount)` into `Customer` as a public method. (2) Introduce a Mediator or move shared logic into a service class. If both classes need to coordinate on order placement, create an `OrderService` that orchestrates the interaction. (3) Apply Tell, Don't Ask — instead of `order.customer.getCreditLimit()`, call `order.customer.canAfford(order.getTotal())`. The goal: each class exposes behavior, not data, and no class reaches into another's internals.

**Example:**
```java
// Before: inappropriate intimacy
class Order {
    boolean canPlace() {
        return customer.creditLimit >= this.total(); // reaches into customer
    }
}

// After: tell, don't ask
class Customer {
    boolean canAfford(Money amount) {
        return creditLimit.compareTo(amount) >= 0;
    }
}

class Order {
    boolean canPlace() {
        return customer.canAfford(total()); // delegates to customer's behavior
    }
}
```

## Q65: Review this code for hidden dependencies and coupling

**A:** The class `ReportService` has a hidden dependency on the current date (calls `new Date()` directly), making it impossible to test for date-sensitive behavior. It also directly calls `Logger.getInstance()`, a hidden static dependency that cannot be mocked. The class accesses `System.getProperty("config.path")` for configuration, coupling it to a specific configuration mechanism. These hidden dependencies make the class untestable, inflexible, and tightly coupled to its environment.

The fix is to make all dependencies explicit through constructor injection. The date dependency should be injected as a `Clock` or `Supplier<Instant>` so tests can control time. The logger should be injected as a `Logger` interface. Configuration should be loaded by the caller and injected as a `Config` object. The principle: if a class needs it, it should receive it — never create or look up dependencies internally.

**Example:**
```java
// Hidden dependencies
class ReportService {
    void generate() {
        Date now = new Date();                    // hidden
        Logger log = Logger.getInstance();        // hidden static
        String path = System.getProperty("x");   // hidden
    }
}

// Explicit dependencies
class ReportService {
    private final Clock clock;
    private final Logger log;
    private final Config config;

    ReportService(Clock clock, Logger log, Config config) {
        this.clock = clock; this.log = log; this.config = config;
    }
}
```

## Q66: This method is too long: walk through your refactoring approach

**A:** The method `processTransaction` is 150 lines long, handling input parsing, validation, fee calculation, balance check, account update, transaction recording, notification sending, and error recovery. My approach: (1) Read through the entire method to understand the high-level flow. (2) Identify logical sections — each section becomes a private method. (3) Extract methods with descriptive names: `parseInput`, `validateTransaction`, `calculateFees`, `checkBalance`, `updateAccounts`, `recordTransaction`, `sendNotifications`. (4) The main method becomes a readable sequence of calls.

(5) For each extracted method, review parameters and return values — minimize the data passed between methods. (6) Handle errors consistently — each extracted method should throw specific exceptions rather than catching broadly. (7) After extraction, review the class for responsibility violations — some methods may belong in different classes. (8) Write tests for each extracted method independently.

**Example:**
```java
// After refactoring
TransactionResult processTransaction(TransactionRequest request) {
    ParsedTransaction parsed = parseInput(request);
    ValidatedTransaction validated = validate(parsed);
    Money fees = calculateFees(validated);
    checkBalance(validated, fees);
    AccountUpdate update = updateAccounts(validated, fees);
    TransactionRecord record = recordTransaction(update);
    sendNotifications(record);
    return new TransactionRecord(record);
}
```

## Q67: How would you refactor this code to improve testability?

**A:** The current code has three testability problems: (1) Static method calls (`UUID.randomUUID()`, `Instant.now()`) make tests non-deterministic. (2) Direct database access makes tests require a running database. (3) External service calls (HTTP requests) make tests slow and flaky. The refactoring introduces seams for test doubles at each point.

For static calls, wrap them behind injectable interfaces: `IdGenerator` and `Clock`. For database access, introduce a `Repository` interface and inject it. For HTTP calls, introduce a `WebService` interface and inject it. In tests, provide mock implementations that return deterministic values. The key is that the production code depends on abstractions, and tests provide concrete test doubles. The refactoring does not change behavior — it changes the architecture to be testable.

**Example:**
```java
// Before: untestable
class UserService {
    User register(String name) {
        String id = UUID.randomUUID().toString();
        Instant now = Instant.now();
        db.execute("INSERT INTO users ...");
        httpClient.post("https://api.example.com/notify", ...);
        return new User(id, name, now);
    }
}

// After: testable
class UserService {
    private final IdGenerator ids;
    private final Clock clock;
    private final UserRepository repo;
    private final NotificationClient notifications;

    User register(String name) {
        String id = ids.generate();
        Instant now = clock.now();
        User user = new User(id, name, now);
        repo.save(user);
        notifications.notify(user);
        return user;
    }
}
```

## Q68: Identify all design issues in this service class

**A:** The `PaymentService` class has multiple design issues: (1) **God Class** — it handles payment processing, refund processing, fraud detection, receipt generation, and reporting. (2) **Hidden dependencies** — it creates `StripeClient` and `PayPalClient` internally. (3) **Primitive obsession** — amounts are `double`, currencies are `String`. (4) **Switch on type** — payment method selection uses a switch on a string. (5) **No error strategy** — some methods throw, some return null, some log and continue.

(6) **Missing abstraction** — payment providers (`Stripe`, `PayPal`) are handled with separate method blocks instead of a `PaymentProvider` interface. (7) **Violation of OCP** — adding a new payment provider requires modifying existing methods. (8) **Inconsistent naming** — `processPayment` vs `handleRefund` vs `doFraudCheck`. The fix involves extracting provider abstraction, introducing domain types, separating responsibilities, and establishing a consistent error handling policy.

**Example:**
```java
// Provider abstraction replaces switch
interface PaymentProvider {
    PaymentResult charge(Money amount, PaymentMethod method);
    RefundResult refund(TransactionId id, Money amount);
}

// Domain types replace primitives
class Money { BigDecimal amount; Currency currency; }

// Responsibility separation
class PaymentProcessor { /* orchestration only */ }
class FraudDetector { /* fraud logic only */ }
class ReceiptGenerator { /* receipt logic only */ }
```

## Q69: This code review reveals a middle man pattern: how would you refactor?

**A:** The `OrderFacade` class delegates every single call to `OrderRepository` without adding any logic — `findAll()` calls `repo.findAll()`, `findById(id)` calls `repo.findById(id)`, `save(order)` calls `repo.save(order)`. The facade is a pure pass-through with no value, creating an unnecessary layer of indirection. This is the Middle Man smell — the class exists only to delegate and can be removed.

The refactoring is to eliminate the middle man entirely. Clients should inject and use `OrderRepository` directly. If the facade was introduced to hide the repository interface, the better approach is to make the repository the public interface directly (interfaces are already abstractions). If some operations need coordination (e.g., finding orders AND checking inventory), add only those coordinating methods to a thin service class, not pure delegations.

**Example:**
```java
// Middle Man: pure delegation, no value
class OrderFacade {
    private OrderRepository repo;
    List<Order> findAll() { return repo.findAll(); }
    Order findById(String id) { return repo.findById(id); }
    void save(Order o) { repo.save(o); }
}

// Fix: remove middle man, use repo directly
// Or add value-adding coordination methods
class OrderService {
    private OrderRepository orders;
    private InventoryService inventory;

    List<Order> findAvailable() {
        return orders.findAll().stream()
            .filter(o -> inventory.isAvailable(o.getItems()))
            .toList();
    }
}
```

## Q70: How would you address this speculative generality?

**A:** The code has interfaces with only one implementation (`NotificationSender` → `DefaultNotificationSender`), abstract classes with one subclass (`BaseRepository` → `UserRepository`), and parameter types that are more general than needed (`Map<String, Object>` instead of `UserProfile`). This Speculative Generality wastes development time and makes the code harder to follow — readers must navigate through unnecessary abstractions.

The refactoring: (1) Delete interfaces with a single implementation — replace with the concrete class. (2) Remove abstract classes with a single subclass — merge into the subclass. (3) Tighten parameter types to what is actually used. (4) Inline trivial methods that delegate to one other method. The rule of thumb: do not create abstractions until you have at least two implementations. Premature abstraction is the opposite of premature optimization — it makes code harder to understand without providing value.

**Example:**
```java
// Speculative: one implementation
interface DataStore { void store(Data d); }
class MongoDataStore implements DataStore { /* only impl */ }

// Fix: remove unnecessary interface
class MongoDataStore { void store(Data d) { /* ... */ } }

// Speculative: abstract with one subclass
abstract class BaseFormatter { }
class JsonFormatter extends BaseFormatter { /* only subclass */ }

// Fix: remove abstract class
class JsonFormatter { }
```

## Q71: Review this refactoring: what was done well and what could improve?

**A:** A refactoring was done that extracted validation logic from the controller into a `Validator` class, which is good — it separates concerns and makes validation testable independently. The controller is now thinner, which is a step in the right direction. The `Validator` class is cohesive and focused on a single responsibility.

However, improvements are needed: (1) The validator still accesses database state directly (calls `userRepository.existsByEmail`), which should be injected as a dependency for testability. (2) The validation messages are hard-coded strings — they should be in a resource bundle for i18n. (3) The controller still creates the validator directly (`new Validator()`) — it should be injected. (4) The refactoring stopped at the service boundary — the `Validator` returns a `List<String>` of errors, which should be a typed `ValidationResult` object. Overall direction is good, but the refactoring needs to be completed to fully decouple the layers.

**Example:**
```java
// Improvements needed:
class Validator {
    private final UserRepository userRepo; // inject, not create

    ValidationResult validate(CreateUserRequest req) {
        List<String> errors = new ArrayList<>();
        if (userRepo.existsByEmail(req.getEmail())) {
            errors.add("Email already exists");
        }
        return new ValidationResult(errors); // typed result
    }
}
```

## Q72: This module has divergent change: how would you restructure it?

**A:** The `ProductService` class changes for two unrelated reasons: (1) when business rules for pricing change (discounts, tax calculation, currency conversion), and (2) when the database schema changes (new fields, different queries). This is Divergent Change — one module is being pulled in multiple directions by different forces. It indicates that responsibilities are mixed.

The restructuring separates pricing logic into a `PricingService` and data access into a `ProductRepository`. The `ProductService` becomes a thin orchestrator that coordinates between the two. Now, pricing changes only affect `PricingService`, and database changes only affect `ProductRepository`. Each module has a single reason to change. The dependency direction should be: `ProductService` → `PricingService` and `ProductRepository`, with no coupling between pricing and persistence.

**Example:**
```java
// Before: divergent change
class ProductService {
    double calculatePrice(Product p) { /* pricing rules */ }
    List<Product> findByCategory(String cat) { /* DB queries */ }
    Product save(Product p) { /* DB save */ }
}

// After: separated concerns
class PricingService {
    Money calculatePrice(Product p) { /* pricing only */ }
}

class ProductRepository {
    List<Product> findByCategory(String cat) { /* DB only */ }
    Product save(Product p) { /* DB only */ }
}

class ProductService {
    PricingService pricing;
    ProductRepository repo;
}
```

## Q73: How would you refactor this code to follow the Interface Segregation Principle?

**A:** The `Worker` interface has methods `work()`, `eat()`, and `sleep()`, but `Robot` implements `Worker` and cannot eat or sleep — it throws `UnsupportedOperationException` for those methods. This violates ISP because clients (the manager class that calls all three methods) depend on methods they do not need for all worker types. The robot is forced to implement irrelevant behavior.

The refactoring splits the monolithic `Worker` interface into smaller, role-based interfaces: `Workable` (with `work()`), `Feedable` (with `eat()`), and `Sleepable` (with `sleep()`). Each worker type implements only the interfaces it supports: `Robot implements Workable`, `Human implements Workable, Feedable, Sleepable`. Clients depend only on the interfaces they need: a work dispatcher depends on `Workable`, a cafeteria manager depends on `Feedable`.

**Example:**
```java
// Before: fat interface
interface Worker {
    void work();
    void eat();   // robots can't eat
    void sleep(); // robots can't sleep
}

// After: segregated interfaces
interface Workable { void work(); }
interface Feedable { void eat(); }
interface Sleepable { void sleep(); }

class Human implements Workable, Feedable, Sleepable { /* all methods */ }
class Robot implements Workable { /* only work() */ }
```

## Q74: This code has a Temporary Field smell: how would you eliminate it?

**A:** The class `ReportGenerator` has fields `csvBuffer`, `htmlTemplate`, and `pdfMetadata` that are only used during specific report generation methods and are null at all other times. These temporary fields are set at the beginning of a method, used within that method, and never referenced again. They bloat the class and create confusion about the object's state.

The fix is to extract the temporary fields into their own classes. The CSV generation logic, including `csvBuffer`, becomes a `CsvReportGenerator` class. The HTML logic becomes an `HtmlReportGenerator`. Each class holds only the state it actually needs, making the code clearer and more cohesive. The original class can use a Strategy pattern to delegate to the appropriate generator, or the generators can be standalone classes.

**Example:**
```java
// Temporary fields
class ReportGenerator {
    private StringBuilder csvBuffer;      // only in generateCSV()
    private String htmlTemplate;          // only in generateHTML()
    private Map<String, String> pdfMeta;  // only in generatePDF()

    void generateCSV() {
        csvBuffer = new StringBuilder(); // temporary state
        // ...
    }
}

// Fix: extract into focused classes
class CsvReportGenerator {
    private StringBuilder buffer = new StringBuilder();
    String generate(Data data) { /* uses buffer */ }
}
```

## Q75: Review this code for maintainability concerns and propose improvements

**A:** The code has several maintainability concerns: (1) **No documentation** — complex algorithms have no comments explaining the business logic. (2) **Deep nesting** — methods have 5+ levels of if-else nesting, making control flow hard to follow. (3) **Magic numbers** — `if (score > 85 && attempts < 4)` uses unexplained constants. (4) **No error handling** — the code assumes all inputs are valid and crashes on null or unexpected data. (5) **Tight coupling** — the business logic is intertwined with database calls and HTTP requests.

Proposed improvements: (1) Extract magic numbers into named constants: `MIN_PASSING_SCORE = 85`, `MAX_ATTEMPTS = 4`. (2) Flatten nested conditionals using early returns or guard clauses. (3) Add Javadoc to complex methods explaining the business rules. (4) Introduce input validation at method boundaries. (5) Separate business logic from infrastructure (database, HTTP) using repository and client abstractions. (6) Add comprehensive logging at decision points for debugging.

**Example:**
```java
// Before: magic numbers, deep nesting
if (score > 85) {
    if (attempts < 4) {
        if (status.equals("active")) {
            // deeply nested logic
        }
    }
}

// After: named constants, guard clauses
static final int MIN_PASSING_SCORE = 85;
static final int MAX_ATTEMPTS = 4;

void processResult(ScoreResult result) {
    if (result.getScore() <= MIN_PASSING_SCORE) return;
    if (result.getAttempts() >= MAX_ATTEMPTS) return;
    if (result.getStatus() != Status.ACTIVE) return;

    // flat, readable logic
    promoteStudent(result);
}
```

## Q76: Walk through your review of this complex PR

**A:** The PR refactors the payment processing module from a monolithic class into separate services. First, I check the overall architecture: the extraction of `PaymentValidator`, `PaymentGateway`, `FraudDetector`, and `ReceiptGenerator` follows SRP and is the right direction. The Facade (`PaymentOrchestrator`) coordinates them, which is clean. I verify backward compatibility: the public API (`PaymentService.process()`) has the same signature and behavior, so consumers are unaffected.

However, I flag several issues: (1) The `FraudDetector` depends on a synchronous HTTP call to an external service with no timeout configuration — this will block the payment thread indefinitely if the service is down. (2) The new `PaymentResult` class does not include error information — failures in validation or fraud detection need to be communicated to the caller. (3) The PR removes unit tests for the old monolithic class but does not add equivalent tests for the new classes. (4) Transaction boundaries are unclear — if `FraudDetector` throws after `PaymentGateway` charges the card, there is no rollback. I request changes to address these before merging.

## Q77: Debug this production issue with limited information

**A:** The issue: the system occasionally processes the same payment twice. The investigation starts with logs: looking for duplicate transaction IDs in the payment gateway response. The logs show that `processPayment` is called twice within 200ms for the same order. Tracing the call stack, both calls originate from the same HTTP request handler, suggesting a retry mechanism is firing.

The root cause is in the retry logic: when the HTTP client times out waiting for a response, it retries the request. But the original request actually succeeded — the response was just slow. The payment gateway processed both requests and charged the customer twice. The fix has two parts: (1) Add **idempotency keys** — each payment request includes a unique key, and the gateway rejects duplicate keys. (2) Use a **deduplication table** — before processing, check if this idempotency key was already processed. (3) Fix the timeout configuration to be appropriate for the payment gateway's typical response time. The deeper lesson: any retry mechanism must assume the original request may have succeeded.

**Example:**
```java
// Idempotent payment processing
PaymentResult processPayment(PaymentRequest req) {
    String idempotencyKey = req.getIdempotencyKey();
    if (deduplicationTable.exists(idempotencyKey)) {
        return deduplicationTable.get(idempotencyKey); // return cached result
    }
    PaymentResult result = gateway.charge(req);
    deduplicationTable.store(idempotencyKey, result);
    return result;
}
```

## Q78: This code passes all tests but violates the Liskov Substitution Principle: prove it

**A:** The `Square` extends `Rectangle` and overrides `setWidth`/`setHeight` to maintain the square invariant. The test for `Rectangle` creates a rectangle, sets width to 5 and height to 10, then asserts `area() == 50`. When a `Square` is substituted, setting width to 5 also sets height to 5, so the area is 25, not 50. The test fails — proving the substitution breaks the contract.

The Liskov Substitution Principle requires that objects of a subtype be substitutable for objects of the supertype without altering the correctness of the program. Here, `Rectangle.setWidth(5); Rectangle.setHeight(10); assert area() == 50` is correct for all `Rectangle` instances but fails for `Square`. The code that works correctly with `Rectangle` references does not work correctly when those references hold `Square` objects. The tests pass because they only test with actual `Rectangle` instances, not with `Square` instances substituted where `Rectangle` is expected. This is a test gap that hides the LSP violation.

**Example:**
```java
class Rectangle {
    protected int width, height;
    void setWidth(int w) { width = w; }
    void setHeight(int h) { height = h; }
    int area() { return width * height; }
}

class Square extends Rectangle {
    void setWidth(int w) { width = w; height = w; }
    void setHeight(int h) { width = h; height = h; }
}

// This test passes only with Rectangle, fails with Square
void testRectangle(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.area() == 50; // fails for Square: area is 25
}

// LSP violation: Square is not substitutable for Rectangle
```

## Q79: Review this architectural change for long-term maintainability impact

**A:** The change moves from a shared database to a database-per-service pattern in a microservices migration. For maintainability: **positive impacts** — each service owns its data, eliminating schema coupling. Teams can evolve their databases independently. Schema changes in one service do not break others. Testing becomes simpler as each service's database is self-contained.

**Negative impacts** — data that was previously joined in a single database now requires cross-service API calls or event-driven synchronization, which is harder to maintain and debug. Reporting across services becomes complex (event sourcing, CQRS, or data warehouses needed). The team must maintain distributed transaction handling (saga pattern) instead of ACID transactions. The operational complexity increases: more databases to monitor, backup, and secure. Long-term, the service-per-database approach requires strong API versioning and data consistency strategies. I would recommend starting with a shared database for the first few services and migrating to per-service databases only when the benefits (independent deployment, team autonomy) clearly outweigh the costs (consistency complexity, cross-service queries).

## Q80: You discover this code in a critical path: how would you refactor it safely?

**A:** The code is a 500-line method in the order processing pipeline that handles order validation, payment, inventory, and shipping in one method with deep nesting and no error recovery. Since it is on the critical path, any change risks breaking production. The safe refactoring approach: (1) Add comprehensive **characterization tests** that capture the current behavior exactly, including edge cases and error paths. (2) Refactor in small, verified steps: extract one method at a time, run tests after each extraction. (3) Use **feature flags** to switch between old and new code paths in production. (4) **Shadow test** — run both old and new paths, compare results, and alert on discrepancies.

The sequence: (1) Write characterization tests (a week). (2) Extract `validateOrder` method, verify (a day). (3) Extract `processPayment` method, verify (a day). (4) Extract `handleInventory` method, verify (a day). (5) Extract `initiateShipping` method, verify (a day). (6) Deploy with feature flag, shadow test for a week. (7) Full cutover. At each step, the system remains deployable and the old behavior is preserved as a fallback.

**Example:**
```java
// Shadow testing approach
OrderResult processOrder(Order order) {
    OrderResult oldResult = legacyProcess(order);  // old path
    OrderResult newResult = refactoredProcess(order); // new path

    if (!oldResult.equals(newResult)) {
        alertService.reportDiscrepancy(order.getId(), oldResult, newResult);
    }

    return featureFlag.isEnabled("new-process-order")
        ? newResult : oldResult;
}
```

## Q81: This design works today but will fail under new requirements: explain why

**A:** The system uses a single `NotificationService` that hard-codes email as the only notification channel. It works today because the only requirement is email notifications. However, upcoming requirements include SMS, push notifications, and in-app messages. The current design will fail because: (1) Adding each new channel requires modifying the `NotificationService` class (violates OCP). (2) The email-specific logic (SMTP configuration, HTML templating) is tangled with the general notification dispatch. (3) There is no abstraction for "notification channel" — the concept does not exist in the code.

The fix is to introduce a `NotificationChannel` interface with `send(Notification notification)` and implement it for each channel (`EmailChannel`, `SmsChannel`, `PushChannel`). A `NotificationService` then dispatches to the appropriate channels based on user preferences. This makes adding new channels a matter of adding a new class, not modifying existing code. The current design is a ticking time bomb because it conflates the notification mechanism with the notification dispatch, making the system rigid and fragile to requirement changes.

## Q82: Walk through your review of this cross-service API change

**A:** The PR changes the `UserService.getUser()` response format from flat to nested JSON. This is a breaking API change that affects all consumers (mobile app, web frontend, two partner services). My review: (1) **Versioning** — the change should be introduced as `/v2/users/` with the old endpoint preserved during a deprecation period. (2) **Consumer impact** — list all known consumers and verify they can handle the new format. (3) **Backward compatibility** — if the old format is removed, what happens to clients that have not upgraded?

(4) **Documentation** — the API documentation must be updated with the new schema and migration guide. (5) **Contract testing** — add or update contract tests (Pact, Spring Cloud Contract) that verify the new response format. (6) **Rollout plan** — deploy the new endpoint first, then migrate consumers one by one, then deprecate the old endpoint. (7) **Monitoring** — add metrics to track usage of old vs. new endpoint during the migration. The review should not approve this change until a migration strategy and rollback plan are documented.

## Q83: Debug this intermittent race condition in production

**A:** The issue: user balances occasionally go negative despite validation that should prevent it. The race condition: two concurrent requests check the balance simultaneously. Request A reads balance = $50, Request B reads balance = $50. Request A deducts $30, writes balance = $20. Request B deducts $40, writes balance = $10. Both passed validation (balance >= amount) because they read the same stale value. This is a classic Time-of-Check-to-Time-of-Use (TOCTOU) race condition.

The fix: use database-level atomic operations instead of read-check-write. `UPDATE accounts SET balance = balance - :amount WHERE id = :id AND balance >= :amount` is atomic — the database serializes the two requests, and the second one finds the balance insufficient and fails. Alternatively, use optimistic locking with a version column: read the version, attempt the update with `WHERE version = :oldVersion`, and retry if the version has changed. The key principle: never trust the application layer to enforce invariants on shared mutable state — use the database's ACID guarantees.

**Example:**
```sql
-- Atomic deduction: database enforces the invariant
UPDATE accounts
SET balance = balance - 40
WHERE id = 123 AND balance >= 40;
-- Returns 0 rows if balance < 40: validation and update are atomic
```

## Q84: This code is correct but unmaintainable: propose a senior-level redesign

**A:** The code is a single 2000-line file with 50 methods, no classes, no separation of concerns, and magic numbers throughout. It works correctly and has 100% test coverage, but any change requires understanding the entire file. The redesign: (1) **Decompose by responsibility** — identify cohesive groups of methods and extract them into classes (`OrderValidator`, `PriceCalculator`, `InventoryManager`, `ShipmentTracker`). (2) **Introduce domain types** — replace primitive parameters with value objects (`Money`, `OrderId`, `Address`). (3) **Define interfaces** — create abstractions for external dependencies (database, email, shipping API).

(4) **Layer the architecture** — establish clear layers: Controller (HTTP), Service (business logic), Repository (data access). (5) **Add configuration externalization** — extract hard-coded values to a configuration class. (6) **Establish coding conventions** — consistent naming, method length limits (20 lines), class responsibility limits. The key senior-level insight: correct code is the minimum bar. The code must also be readable, modifiable, testable, and align with the team's architectural standards. The redesign should be done incrementally over several PRs, not as a big-bang rewrite.

## Q85: Review this concurrent code for correctness issues

**A:** The `CacheManager` uses a `HashMap` accessed by multiple threads with no synchronization. This has three correctness issues: (1) **Data races** — concurrent `put()` calls can corrupt the map's internal structure (lost entries, infinite loops in bucket chains in Java 7). (2) **Visibility** — one thread's writes may not be visible to other threads due to CPU caching (no happens-before relationship). (3) **Iterator inconsistency** — iterating while another thread modifies throws `ConcurrentModificationException` or silently skips/duplicates entries.

The fix depends on the requirements: (1) `ConcurrentHashMap` for lock-free reads and fine-grained locking for writes. (2) Synchronized blocks for critical sections that require atomicity (check-then-act). (3) `Collections.synchronizedMap` for simple cases (but it still requires external synchronization for iteration). (4) Read-write locks (`ReentrantReadWriteLock`) when reads vastly outnumber writes. Additionally, the code should use `volatile` for the reference to the map itself if the map can be replaced entirely, ensuring that all threads see the new map after replacement.

**Example:**
```java
// Broken: unsynchronized HashMap
class CacheManager {
    Map<String, Object> cache = new HashMap<>();
    void put(String key, Object val) { cache.put(key, val); }
    Object get(String key) { return cache.get(key); }
}

// Fixed: ConcurrentHashMap
class CacheManager {
    ConcurrentHashMap<String, Object> cache = new ConcurrentHashMap<>();
    void put(String key, Object val) { cache.put(key, val); }
    Object get(String key) { return cache.get(key); }

    // Atomic check-then-act
    Object getOrCompute(String key, Function<String, Object> loader) {
        return cache.computeIfAbsent(key, loader);
    }
}
```

## Q86: You find this in code review right before a release: what do you do?

**A:** The code review reveals a SQL injection vulnerability in a user-facing search endpoint. The query is built with string concatenation: `"SELECT * FROM users WHERE name = '" + userInput + "'"`. This is a critical security issue that must not be released. Despite the release pressure, this must be fixed before deployment.

The action plan: (1) **Block the release** — inform the team lead and product owner that a critical security vulnerability has been found. This is non-negotiable. (2) **Fix immediately** — replace string concatenation with parameterized queries: `PreparedStatement` with bound parameters. The fix is a one-line change in the data access layer. (3) **Audit for similar patterns** — grep the codebase for other instances of string concatenation in SQL queries. (4) **Add a lint rule** — configure a static analysis rule (SpotBugs, SonarQube) that flags string concatenation in SQL contexts. (5) **Retrospective** — discuss how to prevent this in the future (code review checklists, security-focused PR templates, automated scanning in CI).

## Q87: Debug this memory leak that manifests only under high load

**A:** The leak appears in production monitoring as a steady increase in heap usage under load, not during normal operation. Under high load, more objects are created faster than they are garbage collected. The investigation: (1) Take heap dumps at intervals and compare — look for objects growing in count. (2) The dump reveals growing `byte[]` arrays tied to `HttpURLConnection` instances. (3) The code opens HTTP connections in a retry loop but does not close them on failure — `connection.disconnect()` is in a `finally` block, but the `finally` block is skipped when the `catch` block throws.

The fix: (1) Use try-with-resources for all `InputStream` and `OutputStream` objects associated with HTTP connections. (2) Set connection and read timeouts to prevent indefinite blocking. (3) Ensure the `finally` block does not throw — the catch block re-throws a wrapped exception, which prevents the finally block from completing. Under high load, many connections are opened and never closed, accumulating unreclaimable `byte[]` buffers. The fix is straightforward but requires understanding the interaction between exception handling and resource cleanup.

**Example:**
```java
// Broken: finally not reached if catch rethrows
try {
    conn = (HttpURLConnection) url.openConnection();
    stream = conn.getInputStream();
    // read data
} catch (Exception e) {
    throw new RuntimeException(e); // exits here, finally skipped?
} finally {
    if (stream != null) stream.close(); // never reached
}

// Fixed: try-with-resources
try (InputStream stream = url.openConnection().getInputStream()) {
    // read data
} // stream guaranteed closed
```

## Q88: This refactoring introduces a subtle behavioral change

**A:** The refactoring extracted a method `calculateDiscount(order)` from inline code in `processOrder`. However, the extracted method caches the discount value, while the original code recalculated it on every use. If the discount depends on mutable state (e.g., the customer's tier changes between calculations), the cached version returns a stale value while the original returned the current value. The refactoring changed the semantics from "always fresh" to "snapshot at calculation time."

This is a classic refactoring pitfall: extracting a method changes when the expression is evaluated. If the expression has side effects or depends on changing state, the extraction changes behavior. The fix: ensure the extracted method is called at the same point in the execution flow as the original code, or explicitly handle the caching semantics. Code reviews should verify that refactored code has identical behavior, not just identical structure. Property-based tests and characterization tests can catch such subtle changes.

## Q89: Review this code for design principle violations

**A:** The `ReportManager` class violates multiple SOLID principles: (1) **SRP** — it generates reports, caches results, formats output, and manages report schedules. (2) **OCP** — adding a new report type requires modifying the `generateReport` method. (3) **LSP** — `PdfReportGenerator` throws `UnsupportedOperationException` for `getHtml()`, breaking substitutability. (4) **ISP** — the `ReportGenerator` interface forces all implementations to implement all format methods. (5) **DIP** — the class depends directly on `Database`, `FileManager`, and `EmailService`.

The recommended redesign: extract interfaces for each concern (`DataSource`, `ReportFormatter`, `ReportCache`, `ReportScheduler`). Implement each as a separate class. Use Strategy for report formatting (PDF, HTML, CSV as interchangeable strategies). Use Template Method for the report generation algorithm. Use Observer for report delivery notifications. This decomposition follows all five SOLID principles, resulting in smaller, focused, testable classes.

## Q90: How would you approach refactoring this monolithic service?

**A:** The `MonolithService` class is 3000 lines handling user management, order processing, inventory, reporting, and notifications. The refactoring follows the Strangler Fig pattern: gradually extract functionality into separate services while the monolith continues to serve traffic. The approach: (1) **Identify seams** — find methods that can be extracted with minimal coupling to the rest. (2) **Extract internal modules** — first refactor within the monolith (extract classes, not services). (3) **Identify service boundaries** — determine which modules should become separate services based on team ownership, deployment frequency, and scaling needs.

(4) **Extract one service at a time** — start with the least coupled module (notifications), extract it as a microservice, and redirect traffic via an API gateway. (5) **Monitor and validate** — ensure the extracted service handles its traffic correctly. (6) **Repeat** — continue with the next module. The key principle: never rewrite from scratch. Incremental refactoring preserves the system's working behavior while gradually improving its architecture. Each extraction is a deployable, reversible change.

## Q91: This design has a hidden Liskov violation: identify it

**A:** The `ReadonlyList<T>` extends `ArrayList<T>` but throws `UnsupportedOperationException` for `add()`, `remove()`, and `set()`. The Liskov violation: client code that accepts `List<T>` (the supertype) may call `add()` or `remove()`, expecting the operation to succeed. When a `ReadonlyList` is substituted, these operations throw at runtime, breaking the contract of `List`.

The violation is hidden because the code compiles (the method signatures are valid), and tests using `ArrayList` directly pass. The bug manifests only when `ReadonlyList` is passed where `List` is expected and mutation is attempted. The fix: do not extend `ArrayList`. Instead, implement `List<T>` by delegating to a `List<T>` and only implementing the read methods, or better yet, use `Collections.unmodifiableList()` which returns a proper unmodifiable view. Alternatively, use `java.util.function.Unmodifiable` interfaces (Java 9+) that expose only read methods.

**Example:**
```java
// Hidden LSP violation
class ReadonlyList<T> extends ArrayList<T> {
    @Override public boolean add(T e) { throw new UnsupportedOperationException(); }
    @Override public T remove(int i) { throw new UnsupportedOperationException(); }
}

void processItems(List<String> items) {
    items.add("new"); // works for ArrayList, throws for ReadonlyList
}

// Fix: use unmodifiable view
List<String> items = List.of("a", "b", "c"); // truly immutable
```

## Q92: Review this API change for backward compatibility impacts

**A:** The change renames `getUserName()` to `getDisplayName()` in the public API. This breaks all existing callers — any code calling `getUserName()` will fail to compile after the upgrade. The impacts: (1) All consumer applications must update simultaneously or the build breaks. (2) Third-party integrations calling the old name will receive 404 errors. (3) Client libraries published with the old name become unusable. (4) API documentation and code samples become outdated.

The safe approach: (1) Add `getDisplayName()` as a new method alongside `getUserName()`. (2) Deprecate `getUserName()` with `@Deprecated` and a javadoc pointing to the new method. (3) Publish the change with a minor version bump (not major). (4) Monitor usage of the old method. (5) After a deprecation period (typically 2-3 release cycles), remove the old method in a major version bump. This gives consumers time to migrate and provides a clear upgrade path.

## Q93: Debug this issue where the system appears correct but produces wrong results

**A:** The financial calculations use `double` for monetary amounts, causing floating-point precision errors. For example, `0.1 + 0.2` in IEEE 754 floating-point equals `0.30000000000000004`, not `0.3`. Over millions of transactions, these tiny errors compound, producing incorrect totals. The system appears correct in unit tests (which use small numbers and loose tolerance) but produces wrong results in production with large volumes.

The fix: use `BigDecimal` for all monetary calculations. `BigDecimal` provides arbitrary precision arithmetic that eliminates floating-point rounding errors. The refactoring: (1) Change all monetary fields from `double` to `BigDecimal`. (2) Update all arithmetic operations to use `BigDecimal` methods (`add`, `multiply`, `divide` with explicit scale and rounding mode). (3) Update serialization/deserialization to handle `BigDecimal` correctly. (4) Add tests that verify precision over millions of operations. The lesson: never use `double` for money. The error is insidious because it only appears at scale.

**Example:**
```java
// Broken: floating-point precision
double total = 0.0;
for (int i = 0; i < 1000000; i++) {
    total += 0.01;
}
System.out.println(total); // 9999.999999999063, not 10000.00

// Fixed: BigDecimal
BigDecimal total = BigDecimal.ZERO;
BigDecimal penny = new BigDecimal("0.01");
for (int i = 0; i < 1000000; i++) {
    total = total.add(penny);
}
System.out.println(total); // 10000.00 exactly
```

## Q94: This violates Open-Closed Principle: how would you fix it?

**A:** The `ReportExporter` class has a method that uses `if (type.equals("pdf"))`, `else if (type.equals("csv"))`, etc. Adding a new export type requires modifying this method, violating OCP (open for extension, closed for modification). The class should be open for new export types without modification to existing code.

The fix: extract an `Exporter` interface with an `export(Data data)` method. Each export type becomes a separate class: `PdfExporter`, `CsvExporter`, `JsonExporter`. The original class becomes a registry that maps type strings to exporter instances (using a Map or dependency injection). New export types are added by creating a new class and registering it, without touching any existing code. This follows OCP: the system is extended by adding new classes, not modifying existing ones.

**Example:**
```java
// Before: violates OCP
void export(String type, Data data) {
    if (type.equals("pdf")) exportPdf(data);
    else if (type.equals("csv")) exportCsv(data);
    // adding "json" requires modifying this method
}

// After: follows OCP
interface Exporter { byte[] export(Data data); }

Map<String, Exporter> exporters = Map.of(
    "pdf", new PdfExporter(),
    "csv", new CsvExporter()
);

void export(String type, Data data) {
    exporters.get(type).export(data); // no modification needed
}
// To add "json": just add a new Exporter class and register it
```

## Q95: Review this cross-team dependency for design issues

**A:** Team A's `UserService` directly calls Team B's `InventoryService` via REST, creating a synchronous dependency. If `InventoryService` is slow or down, `UserService` is blocked. The design issues: (1) **Tight coupling** — Team A's service cannot be deployed independently of Team B's. (2) **Availability coupling** — Team B's downtime becomes Team A's downtime. (3) **No resilience** — no timeout, circuit breaker, or fallback for the dependency.

The recommended fix: replace the synchronous REST call with an asynchronous event-driven approach. `UserService` publishes a `UserCreated` event to a message queue. `InventoryService` consumes the event and initializes inventory independently. This decouples the services in time and availability. If `InventoryService` is down, the event is queued and processed when it recovers. The trade-off: eventual consistency instead of strong consistency, and increased complexity of event-driven architecture. For use cases where synchronous response is required, add circuit breakers, timeouts, and fallback behavior.

## Q96: Debug this race condition in production

**A:** Two concurrent HTTP requests for the same user both read the user's profile, modify different fields, and write back. Request A reads the profile, updates the email. Request B reads the profile (with the old email), updates the phone. Both write back — whichever writes last overwrites the other's change. This is the lost update problem, a classic race condition in concurrent systems.

The fix: use optimistic locking with a version field. Each profile read includes the current version number. Each update includes a `WHERE version = :expected_version` clause. If the version has changed (another request modified the record), the update affects zero rows, and the request can retry with fresh data. Alternatively, use field-level updates: `UPDATE users SET email = :email WHERE id = :id` instead of updating the entire record. This way, concurrent updates to different fields do not conflict. The key principle: make writes as granular as possible to minimize contention.

**Example:**
```sql
-- Optimistic locking
UPDATE users
SET email = :new_email, version = version + 1
WHERE id = :id AND version = :expected_version;
-- If 0 rows affected: conflict, retry with fresh data

-- Or field-level update: no conflict for different fields
UPDATE users SET email = :email WHERE id = :id;
-- Concurrent: UPDATE users SET phone = :phone WHERE id = :id; -- no conflict
```

## Q97: You're reviewing this critical-path code: comprehensive analysis

**A:** The critical-path code handles order checkout and payment. My comprehensive review covers: (1) **Correctness** — the payment calculation has no rounding error handling; `double` arithmetic should use `BigDecimal`. (2) **Error handling** — payment failures return null instead of throwing, making error detection unreliable. (3) **Security** — credit card numbers are logged in plaintext (PCI DSS violation). (4) **Concurrency** — the inventory check and reservation are not atomic, allowing overselling. (5) **Performance** — the method makes 5 sequential HTTP calls that could be parallelized. (6) **Resilience** — no circuit breaker for the payment gateway; if it is slow, the checkout thread blocks indefinitely. (7) **Observability** — no metrics or tracing for the critical path. (8) **Testability** — dependencies are created internally, preventing unit testing.

The recommended changes: (1) Use `BigDecimal` for all monetary values. (2) Throw typed exceptions for payment failures. (3) Remove all card number logging (mask: `****-****-****-1234`). (4) Use database transactions with row-level locking for inventory operations. (5) Parallelize independent HTTP calls with `CompletableFuture`. (6) Add Resilience4j circuit breaker for external calls. (7) Add Micrometer metrics for latency and error rates. (8) Refactor for dependency injection.

## Q98: How would you refactor for testability?

**A:** The current code creates dependencies internally, uses static methods, and has hidden side effects — making it untestable. The refactoring for testability: (1) **Constructor injection** — replace `new Database()` with `Database db` constructor parameter. (2) **Interface extraction** — depend on `IDatabase` interface, not concrete `MySQLDatabase`. (3) **Replace static calls** — wrap `UUID.randomUUID()` behind an injectable `IdProvider`. (4) **Clock injection** — replace `Instant.now()` with `Clock.now()` so tests can control time.

(5) **Output injection** — replace direct `System.out.println` calls with an injectable `Logger`. (6) **Extract pure functions** — separate pure logic (calculations, validations) from impure operations (I/O, network, database). Test pure functions directly; mock impure dependencies. (7) **Make side effects explicit** — methods that modify state should be clearly separated from methods that read state. The goal: every method can be tested in isolation by controlling its inputs and mocking its dependencies.

**Example:**
```java
// Before: untestable
class OrderService {
    OrderResult process(Order o) {
        String id = UUID.randomUUID().toString(); // static
        Instant now = Instant.now();              // static
        new Database().save(o);                   // internal creation
        System.out.println("Processed");          // side effect
        return new OrderResult(id, now);
    }
}

// After: testable
class OrderService {
    private final IdProvider ids;
    private final Clock clock;
    private final Database db;
    private final Logger log;

    OrderResult process(Order o) {
        String id = ids.generate();
        Instant now = clock.now();
        db.save(o);
        log.info("Processed order " + id);
        return new OrderResult(id, now);
    }
}
```

## Q99: This code has hidden coupling: expose and fix

**A:** The `NotificationService` appears independent but is tightly coupled to `UserService` (it queries user preferences), `TemplateService` (it renders email templates), `AnalyticsService` (it tracks notification opens), and `PaymentService` (it sends payment receipts). These dependencies are hidden inside method implementations, not expressed in the class's constructor or interface. The hidden coupling means: (1) Changes to any of these services can break `NotificationService` unexpectedly. (2) Testing `NotificationService` requires mocking four unrelated services. (3) The class is much harder to understand than its interface suggests.

The fix: make all dependencies explicit through constructor injection. If a dependency is only needed for one method, extract that method into a separate class that owns the dependency. For example, `PaymentReceiptSender` takes the `PaymentService` dependency, and `NotificationService` no longer needs it. This exposes the coupling and makes it possible to refactor each dependency independently. The general rule: if a class needs it, it should be in the constructor. Hidden dependencies are the number one cause of unexpected breakage in large codebases.

## Q100: Senior-level comprehensive analysis of this module's design

**A:** The module handles user registration, authentication, profile management, and notification preferences in a single `UserService` class with 800 lines. My senior-level analysis:

**Architecture**: The class mixes three bounded contexts (identity, profile, preferences) that should be separate services. Each has its own data model, business rules, and API surface. Splitting into `IdentityService`, `ProfileService`, and `PreferenceService` aligns with domain-driven design boundaries.

**Design Patterns**: The class should use Strategy for authentication (password, OAuth, SSO), Observer for registration events (welcome email, analytics, audit log), and Builder for user creation (complex object with many optional fields).

**SOLID Violations**: SRP — three reasons to change. OCP — adding auth methods requires modifying existing code. ISP — the `UserService` interface exposes methods for all three concerns. DIP — depends on concrete implementations.

**Testing**: The class has 15% code coverage because it is untestable (static calls, internal dependencies, no interfaces). After decomposition, each service should achieve 80%+ coverage.

**Operational Concerns**: No circuit breakers for external dependencies, no metrics for monitoring, no feature flags for gradual rollout. The class should use resilience patterns and observability from the start.

**Migration Plan**: Extract `IdentityService` first (least coupled), then `ProfileService`, then `PreferenceService`. Each extraction is a deployable PR with full test coverage and a feature flag for safe rollout.
