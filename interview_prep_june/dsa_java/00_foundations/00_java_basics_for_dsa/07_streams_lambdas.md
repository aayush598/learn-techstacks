# 07 — Streams & Lambdas in Java

Java 8 brought functional programming to the mainstream Java world. Lambdas and Streams let you write concise, expressive, and often more readable code. For DSA, they're especially useful for quick data transformations, filtering, and aggregation.

---

## 1. Lambda Syntax

### The Basics

```java
// Full syntax: (parameters) -> { body }
// Type inference: (a, b) -> a + b
// Single parameter (no parens): x -> x * 2
// Block body: (x, y) -> { return x + y; }

// Examples:
Runnable r = () -> System.out.println("Hello");
Consumer<String> c = s -> System.out.println(s);
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
Comparator<Integer> comp = (a, b) -> Integer.compare(a, b);
```

### Variable Capture — Effectively Final

```java
int threshold = 10;
List<Integer> nums = List.of(5, 15, 20, 3);

// Lambda can access 'threshold' — it must be effectively final
List<Integer> filtered = nums.stream()
    .filter(n -> n > threshold)   // captures threshold
    .collect(Collectors.toList());

// threshold = 20;  // ❌ can't reassign — not effectively final
```

**Rule:** A lambda can reference local variables that are `final` or **effectively final** (not reassigned after initialization).

---

## 2. Functional Interfaces

| Interface | Method | Signature | Example |
|-----------|--------|-----------|---------|
| `Predicate<T>` | `test` | `T → boolean` | `x -> x > 0` |
| `Function<T,R>` | `apply` | `T → R` | `s -> s.length()` |
| `Consumer<T>` | `accept` | `T → void` | `x -> System.out.println(x)` |
| `Supplier<T>` | `get` | `() → T` | `() -> new Random().nextInt()` |
| `UnaryOperator<T>` | `apply` | `T → T` | `x -> x * 2` |
| `BinaryOperator<T>` | `apply` | `(T,T) → T` | `(a,b) -> a + b` |
| `BiFunction<T,U,R>` | `apply` | `(T,U) → R` | `(a,b) -> a + "," + b` |

```java
// Predicate — test condition
Predicate<Integer> isEven = n -> n % 2 == 0;
Predicate<Integer> isPositive = n -> n > 0;
Predicate<Integer> isEvenAndPositive = isEven.and(isPositive);

// Function — transform
Function<String, Integer> lengthFn = String::length;
Function<Integer, String> intToString = Object::toString;
Function<String, String> upperCase = String::toUpperCase;

// Consumer — perform action
Consumer<String> printer = System.out::println;
Consumer<String> logger = s -> System.out.println("LOG: " + s);
Consumer<String> combined = printer.andThen(logger);

// Supplier — provide value
Supplier<Double> random = Math::random;
Supplier<Integer> zero = () -> 0;
```

---

## 3. Creating Streams

```java
// From collections
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream = list.stream();
Stream<String> parallelStream = list.parallelStream();

// From arrays
int[] arr = {1, 2, 3, 4, 5};
IntStream intStream = Arrays.stream(arr);           // IntStream (primitive)
Stream<Integer> boxed = Arrays.stream(arr).boxed(); // Stream<Integer>
Stream<String> strStream = Arrays.stream(new String[]{"a", "b"});

// Stream.of
Stream<Integer> stream = Stream.of(1, 2, 3, 4, 5);
Stream<String> empty = Stream.empty();
Stream<Integer> single = Stream.of(42);

// Stream.iterate (infinite, use limit)
Stream<Integer> evens = Stream.iterate(0, n -> n + 2).limit(10);

// Stream.generate (infinite, use limit)
Stream<Double> randoms = Stream.generate(Math::random).limit(5);

// From builder
Stream<String> built = Stream.<String>builder()
    .add("a").add("b").add("c")
    .build();

// Primitive streams
IntStream.range(0, 10);           // 0 to 9
IntStream.rangeClosed(1, 10);     // 1 to 10
IntStream.of(1, 2, 3, 4, 5);
LongStream.range(0, 100);
DoubleStream.of(1.5, 2.5, 3.5);
```

---

## 4. Intermediate Operations

These are **lazy** — they don't execute until a terminal operation is called.

```java
List<Integer> nums = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// filter — keep elements matching predicate
List<Integer> evens = nums.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());  // [2, 4, 6, 8, 10]

// map — transform each element
List<Integer> squares = nums.stream()
    .map(n -> n * n)
    .collect(Collectors.toList());  // [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

// flatMap — flatten nested structures
List<List<Integer>> nested = List.of(List.of(1,2), List.of(3,4), List.of(5,6));
List<Integer> flat = nested.stream()
    .flatMap(Collection::stream)
    .collect(Collectors.toList());  // [1, 2, 3, 4, 5, 6]

// flatMap with String
String[] words = {"hello", "world"};
List<String> letters = Arrays.stream(words)
    .flatMap(s -> Arrays.stream(s.split("")))
    .distinct()
    .collect(Collectors.toList());  // [h, e, l, o, w, r, d]

// distinct — remove duplicates
List<Integer> distinct = List.of(1, 2, 2, 3, 3, 3).stream()
    .distinct()
    .collect(Collectors.toList());  // [1, 2, 3]

// sorted — sort elements
List<Integer> sorted = List.of(5, 2, 8, 1, 9).stream()
    .sorted()
    .collect(Collectors.toList());  // [1, 2, 5, 8, 9]

List<Integer> desc = List.of(5, 2, 8, 1, 9).stream()
    .sorted(Comparator.reverseOrder())
    .collect(Collectors.toList());  // [9, 8, 5, 2, 1]

// peek — see each element (debugging only)
List<Integer> withLog = nums.stream()
    .peek(x -> System.out.println("Processing: " + x))
    .filter(x -> x > 5)
    .collect(Collectors.toList());

// limit — take first n elements
List<Integer> first3 = nums.stream()
    .limit(3)
    .collect(Collectors.toList());  // [1, 2, 3]

// skip — skip first n elements
List<Integer> after5 = nums.stream()
    .skip(5)
    .collect(Collectors.toList());  // [6, 7, 8, 9, 10]

// takeWhile (Java 9+) — take while condition is true
List<Integer> taken = nums.stream()
    .takeWhile(n -> n < 6)
    .collect(Collectors.toList());  // [1, 2, 3, 4, 5]

// dropWhile (Java 9+) — drop while condition is true
List<Integer> dropped = nums.stream()
    .dropWhile(n -> n < 6)
    .collect(Collectors.toList());  // [6, 7, 8, 9, 10]
```

### Chaining Intermediate Operations

```java
// Pipeline: source → multiple intermediates → terminal
List<String> result = words.stream()
    .filter(w -> w.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .distinct()
    .collect(Collectors.toList());
```

---

## 5. Terminal Operations

These trigger the pipeline and produce a result or side effect.

```java
List<Integer> nums = List.of(1, 2, 3, 4, 5);

// forEach — perform action on each element
nums.stream().forEach(System.out::println);
nums.forEach(System.out::println);  // same, for Collection

// collect — accumulate into a collection
List<Integer> list = nums.stream()
    .filter(n -> n > 2)
    .collect(Collectors.toList());

Set<Integer> set = nums.stream()
    .collect(Collectors.toSet());

// toList() — Java 16+ shortcut
List<Integer> list16 = nums.stream()
    .filter(n -> n > 2)
    .toList();  // immutable

// toArray
Integer[] arr = nums.stream()
    .filter(n -> n > 2)
    .toArray(Integer[]::new);

// count — count elements
long count = nums.stream()
    .filter(n -> n > 3)
    .count();  // 2

// anyMatch / allMatch / noneMatch — short-circuiting
boolean hasEven = nums.stream().anyMatch(n -> n % 2 == 0);     // true
boolean allPositive = nums.stream().allMatch(n -> n > 0);      // true
boolean noneNegative = nums.stream().noneMatch(n -> n < 0);    // true

// findFirst / findAny — return Optional (short-circuiting)
Optional<Integer> first = nums.stream()
    .filter(n -> n > 3)
    .findFirst();  // Optional[4]

Optional<Integer> any = nums.parallelStream()
    .filter(n -> n > 3)
    .findAny();  // non-deterministic for parallel streams

// min / max — need Comparator
Optional<Integer> min = nums.stream().min(Integer::compareTo);  // 1
Optional<Integer> max = nums.stream().max(Integer::compareTo);  // 5

// reduce — combine elements
int sum = nums.stream().reduce(0, Integer::sum);          // 15
int product = nums.stream().reduce(1, (a, b) -> a * b);  // 120
Optional<Integer> maxReduce = nums.stream()
    .reduce(Integer::max);  // Optional[5]
```

### Collectors in Depth

```java
// toList / toSet / toCollection
List<Integer> list = stream.collect(Collectors.toList());
Set<Integer> set = stream.collect(Collectors.toSet());
TreeSet<Integer> treeSet = stream.collect(Collectors.toCollection(TreeSet::new));

// toMap
Map<Integer, String> map = stream.collect(
    Collectors.toMap(
        Student::getId,          // key mapper
        Student::getName,        // value mapper
        (a, b) -> a + "," + b   // merge function for duplicate keys (optional)
    )
);

// joining — for strings
String joined = words.stream()
    .collect(Collectors.joining(", ", "[", "]"));  // "[apple, banana, cherry]"

// summarizing — statistics
IntSummaryStatistics stats = nums.stream()
    .collect(Collectors.summarizingInt(Integer::intValue));
stats.getSum(); stats.getAverage(); stats.getMin(); stats.getMax(); stats.getCount();

// counting
long count = stream.collect(Collectors.counting());

// summing / averaging
int total = stream.collect(Collectors.summingInt(Student::getGrade));
double avg = stream.collect(Collectors.averagingInt(Student::getAge));

// groupingBy — group by classifier (returns Map<K, List<V>>)
Map<String, List<Student>> byGrade = students.stream()
    .collect(Collectors.groupingBy(Student::getGradeLetter));

// groupingBy with downstream collector
Map<String, Long> countByGrade = students.stream()
    .collect(Collectors.groupingBy(
        Student::getGradeLetter,
        Collectors.counting()
    ));

Map<String, Double> avgAgeByGrade = students.stream()
    .collect(Collectors.groupingBy(
        Student::getGradeLetter,
        Collectors.averagingInt(Student::getAge)
    ));

Map<String, Set<String>> namesByGrade = students.stream()
    .collect(Collectors.groupingBy(
        Student::getGradeLetter,
        Collectors.mapping(Student::getName, Collectors.toSet())
    ));

// partitioningBy — split into two groups (true/false)
Map<Boolean, List<Integer>> partitioned = nums.stream()
    .collect(Collectors.partitioningBy(n -> n % 2 == 0));
// {false=[1,3,5], true=[2,4]}

Map<Boolean, Long> countPartition = nums.stream()
    .collect(Collectors.partitioningBy(
        n -> n % 2 == 0,
        Collectors.counting()
    ));
```

---

## 6. Primitive Streams — Avoiding Boxing Overhead

```java
int[] arr = {1, 2, 3, 4, 5};

// IntStream methods
IntStream stream = Arrays.stream(arr);
int sum = stream.sum();                           // 15
OptionalDouble avg = stream.average();            // 3.0
OptionalInt min = stream.min();                   // 1
OptionalInt max = stream.max();                   // 5
int range = IntStream.range(1, 10).sum();         // 45
int[] evens = IntStream.range(0, 20)
    .filter(n -> n % 2 == 0)
    .toArray();                                   // [0,2,4,...,18]

// Converting between streams
IntStream intStream = IntStream.range(0, 10);
Stream<Integer> boxed = intStream.boxed();
int[] back = boxed.mapToInt(Integer::intValue).toArray();

// Useful operations
IntSummaryStatistics stats = IntStream.range(1, 100).summaryStatistics();
```

---

## 7. Parallel Streams — With Caution

```java
// Easy parallelism — just call parallelStream() or .parallel()
int sum = list.parallelStream()
    .filter(n -> n > 0)
    .mapToInt(Integer::intValue)
    .sum();

// Or convert sequential → parallel
int sum = list.stream()
    .parallel()
    .filter(n -> n > 0)
    .mapToInt(Integer::intValue)
    .sum();
```

### Caveats of Parallel Streams

```java
// ⚠️ Shared mutable state — WRONG!
List<Integer> results = new ArrayList<>();  // not thread-safe!
IntStream.range(0, 1000).parallel()
    .forEach(results::add);  // race condition! missing elements, duplicates

// ✅ Use thread-safe collector
List<Integer> results = IntStream.range(0, 1000)
    .parallel()
    .boxed()
    .collect(Collectors.toList());

// ⚠️ Order-dependent operations
// findAny() gives different results
// forEachOrdered() guarantees order but kills parallelism
IntStream.range(0, 10).parallel()
    .forEachOrdered(System.out::print);  // 0123456789 (parallel but ordered)

// ⚠️ When NOT to parallelize
// - Small datasets (overhead > benefit)
// - Sequential operations (findFirst, limit)
// - Unordered sources with forEachOrdered
// - Operations with blocking IO

// ✅ Good candidates for parallel
// - Large datasets (10k+ elements)
// - Independent element processing
// - CPU-intensive computations
// - ArrayList, HashMap, HashSet (splittable)
// ❌ Bad: LinkedList, TreeSet (poor splitting)
```

---

## 8. Optional — Null Safety Made Functional

```java
// Creating Optionals
Optional<String> empty = Optional.empty();
Optional<String> present = Optional.of("hello");   // throws if null
Optional<String> nullable = Optional.ofNullable(null);  // empty if null

// Checking
if (present.isPresent()) { /* ... */ }
present.ifPresent(s -> System.out.println(s));
present.ifPresentOrElse(
    s -> System.out.println(s),
    () -> System.out.println("empty")
);

// Getting values
String val = present.get();               // throws if empty
String withDefault = nullable.orElse("default");
String withDefaultLazy = nullable.orElseGet(() -> computeDefault());
String orThrow = nullable.orElseThrow(() -> new NoSuchElementException());

// Transforming
Optional<Integer> length = present.map(String::length);
Optional<String> upper = present.filter(s -> s.length() > 3)
    .map(String::toUpperCase);

// Chaining
String result = Optional.ofNullable(getName())
    .filter(name -> name.length() > 0)
    .map(String::toUpperCase)
    .orElse("UNKNOWN");

// FlatMap — for nested Optionals
Optional<Optional<String>> nested = Optional.of(Optional.of("hello"));
Optional<String> flat = nested.flatMap(opt -> opt);  // Optional["hello"]

// Stream of Optionals (Java 9+)
List<Optional<String>> list = Arrays.asList(
    Optional.of("a"), Optional.empty(), Optional.of("b")
);
List<String> presentValues = list.stream()
    .flatMap(Optional::stream)
    .collect(Collectors.toList());  // [a, b]
```

---

## 9. Streams for DSA — Practical Patterns

### Pattern 1: Frequency Map

```java
Map<Character, Long> freq = s.chars()
    .mapToObj(c -> (char) c)
    .collect(Collectors.groupingBy(
        Function.identity(),
        Collectors.counting()
    ));
```

### Pattern 2: Filter and Transform

```java
// Get names of all students with grade > 80, sorted
List<String> result = students.stream()
    .filter(s -> s.getGrade() > 80)
    .map(Student::getName)
    .sorted()
    .collect(Collectors.toList());
```

### Pattern 3: Sum / Average / Statistics

```java
int totalAge = students.stream()
    .mapToInt(Student::getAge)
    .sum();

double avgGrade = students.stream()
    .collect(Collectors.averagingInt(Student::getGrade));
```

### Pattern 4: Check Conditions

```java
boolean allAdults = people.stream().allMatch(p -> p.getAge() >= 18);
boolean hasMinors = people.stream().anyMatch(p -> p.getAge() < 18);
```

### Pattern 5: Find Duplicates

```java
List<Integer> duplicates = list.stream()
    .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()))
    .entrySet().stream()
    .filter(e -> e.getValue() > 1)
    .map(Map.Entry::getKey)
    .collect(Collectors.toList());
```

### Pattern 6: Convert Primitives

```java
int[] arr = {1, 2, 3, 4, 5};
List<Integer> boxed = Arrays.stream(arr).boxed().collect(Collectors.toList());
int[] back = boxed.stream().mapToInt(Integer::intValue).toArray();
```

### Pattern 7: Group Anagrams

```java
Map<String, List<String>> groups = Arrays.stream(strs)
    .collect(Collectors.groupingBy(s -> {
        char[] c = s.toCharArray();
        Arrays.sort(c);
        return new String(c);
    }));
```

---

## Cheat Sheet

```java
// STREAM CREATION
list.stream(); Arrays.stream(arr); Stream.of(a,b,c);
IntStream.range(s,e); Stream.iterate(seed, fn).limit(n);

// INTERMEDIATE
.filter(pred).map(fn).flatMap(fn).distinct().sorted()
.limit(n).skip(n).takeWhile(pred).dropWhile(pred).peek(fn)

// TERMINAL
.collect(toList/toSet/toMap).toList().toArray()
.forEach(fn).count().reduce(id, op)
.anyMatch/allMatch/noneMatch(pred)
.findFirst().findAny().min(cmp).max(cmp)

// COLLECTORS
joining(","); groupingBy(fn); partitioningBy(pred);
counting(); summingInt(); averagingInt();
toCollection(TreeSet::new); mapping(fn, collector);

// OPTIONAL
Optional.of(v); Optional.ofNullable(v); Optional.empty()
opt.isPresent(); opt.ifPresent(fn);
opt.orElse(def); opt.orElseGet(supp); opt.orElseThrow(ex);
opt.map(fn); opt.filter(pred); opt.flatMap(fn);

// PRIMITIVE STREAMS
IntStream.range(0, n).sum(); .average(); .min(); .max();
```

Streams won't replace loops for everything, but they're invaluable for quick transformations, especially in coding interviews where you need to write concise, readable code.
