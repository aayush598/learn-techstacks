# 02 — Arrays & ArrayList in Java

Arrays and ArrayLists are the bread and butter of DSA. If you can't wield these confidently, you'll struggle with everything else. Let's fix that.

---

## 1. Arrays — The Foundation

### Declaration & Initialization

```java
// Declaration (no memory allocated yet)
int[] arr;          // preferred — reads as "int array"
int arr2[];         // valid but ugly — C-style

// Memory allocation
arr = new int[5];   // creates array of size 5, all elements = 0

// Combined declaration + allocation
int[] nums = new int[10];

// Literal initialization (size inferred)
int[] literal = {1, 2, 3, 4, 5};

// Anonymous array (for passing inline)
printArray(new int[]{10, 20, 30});

// Array of objects
String[] names = new String[3];  // all null
Integer[] numbers = {1, 2, 3};   // autoboxed
```

### The `length` Property

**Not** `length()` — that's for String. Arrays use `length` (no parentheses):

```java
int[] arr = {10, 20, 30, 40, 50};
System.out.println(arr.length);  // 5

for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}
```

### Iterating

```java
int[] arr = {10, 20, 30, 40, 50};

// Standard for loop — need index
for (int i = 0; i < arr.length; i++) {
    System.out.println("Index " + i + ": " + arr[i]);
}

// Enhanced for-each — don't need index
for (int num : arr) {
    System.out.println(num);
}

// Backwards iteration
for (int i = arr.length - 1; i >= 0; i--) {
    System.out.println(arr[i]);
}

// Two-pointer style
for (int i = 0, j = arr.length - 1; i < j; i++, j--) {
    // process both ends
}
```

### Filling & Copying

```java
import java.util.Arrays;

int[] arr = new int[10];

// Fill entire array with a value
Arrays.fill(arr, -1);          // arr = [-1, -1, ..., -1]

// Fill a range [from, to) — to is exclusive
Arrays.fill(arr, 2, 5, 42);    // indices 2,3,4 = 42

// Copy — new array, separate memory
int[] original = {1, 2, 3, 4, 5};
int[] copy = Arrays.copyOf(original, original.length);  // exact copy
int[] first3 = Arrays.copyOf(original, 3);               // [1, 2, 3]
int[] longer = Arrays.copyOf(original, 10);              // [1,2,3,4,5,0,0,...]

// Copy range [from, to)
int[] range = Arrays.copyOfRange(original, 1, 4);        // [2, 3, 4]

// clone() also works
int[] cloned = original.clone();
```

**Important:** `clone()` and `copyOf` create shallow copies. For primitives, this is fine. For objects, both arrays share the same object references.

### Sorting

```java
int[] arr = {5, 2, 8, 1, 9};

// Full sort — O(n log n), Dual-Pivot Quicksort
Arrays.sort(arr);  // [1, 2, 5, 8, 9]

// Sort a range [from, to)
Arrays.sort(arr, 1, 4);  // sorts indices 1,2,3 only

// Sort in reverse order (need Integer[], not int[])
Integer[] boxed = {5, 2, 8, 1, 9};
Arrays.sort(boxed, Collections.reverseOrder());

// Custom comparator on objects
Arrays.sort(boxed, (a, b) -> b - a);  // descending

// ⚠️ Careful: (a - b) can overflow! Safer:
Arrays.sort(boxed, (a, b) -> Integer.compare(b, a));
```

### Binary Search

```java
int[] arr = {1, 3, 5, 7, 9, 11, 13};

// Must be SORTED first!
int index = Arrays.binarySearch(arr, 7);   // returns 3

// If not found: returns -(insertion point) - 1
int notFound = Arrays.binarySearch(arr, 6);
// returns -4 → means insertion point is index 3 (at value 7)

// Range search
int index = Arrays.binarySearch(arr, 1, 5, 7);  // search in [1,5)
```

### 2D Arrays

```java
// Declaration & initialization
int[][] matrix = new int[3][4];        // 3 rows, 4 cols
int[][] literal = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Jagged arrays — each row can have different length
int[][] jagged = new int[3][];
jagged[0] = new int[2];
jagged[1] = new int[4];
jagged[2] = new int[3];

// Key property: length
System.out.println(matrix.length);      // 3 (number of rows)
System.out.println(matrix[0].length);   // 4 (number of columns)

// Row-wise traversal
for (int i = 0; i < matrix.length; i++) {
    for (int j = 0; j < matrix[i].length; j++) {
        System.out.print(matrix[i][j] + " ");
    }
    System.out.println();
}

// For-each on 2D
for (int[] row : matrix) {
    for (int val : row) {
        System.out.print(val + " ");
    }
}

// Deep toString
System.out.println(Arrays.deepToString(matrix));  // [[1,2,3],[4,5,6],[7,8,9]]
```

### Array to String

```java
int[] arr = {1, 2, 3, 4, 5};
System.out.println(arr);                    // [I@hashcode — useless!
System.out.println(Arrays.toString(arr));    // [1, 2, 3, 4, 5] — what you want
```

---

## 2. ArrayList — The Dynamic Array

### Why ArrayList?

Arrays are fixed-size. Once created, you can't add or remove elements. ArrayList wraps an internal array and handles resizing automatically. When it fills up, it creates a new array ~1.5x larger and copies elements over.

```java
import java.util.ArrayList;

// Declaration
ArrayList<Integer> list = new ArrayList<>();         // default capacity 10
ArrayList<String> names = new ArrayList<>(20);       // initial capacity 20
ArrayList<Integer> fromArray = new ArrayList<>(List.of(1, 2, 3));

// ⚠️ Generics — can't use primitives
// ArrayList<int> bad = new ArrayList<>();  // ❌ won't compile
```

### All CRUD Operations

```java
ArrayList<String> list = new ArrayList<>();

// CREATE — add elements
list.add("Java");           // appends to end — O(1) amortized
list.add("Python");         // ["Java", "Python"]
list.add(0, "C++");         // inserts at index — O(n), shifts rest
list.addAll(List.of("Go", "Rust"));  // bulk add

// READ — access elements
String s = list.get(0);                    // O(1) — like array index
int size = list.size();                    // NOT length!
boolean empty = list.isEmpty();
boolean contains = list.contains("Java");  // O(n) — linear search
int index = list.indexOf("Python");        // first occurrence, O(n)
int lastIdx = list.lastIndexOf("Java");    // last occurrence, O(n)

// UPDATE
list.set(1, "JavaScript");  // replaces element at index — O(1)

// DELETE
list.remove(0);             // remove by index — O(n), shifts
list.remove("Go");          // remove by value (first occurrence) — O(n)
list.clear();               // remove all — O(n)
String removed = list.remove(list.size() - 1);  // remove last

// Iteration
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}
for (String lang : list) {
    System.out.println(lang);
}
list.forEach(System.out::println);

// Convert to array
String[] arr = list.toArray(new String[0]);  // preferred
Object[] objArr = list.toArray();            // loses type info
```

### Important Capacity Methods

```java
ArrayList<Integer> list = new ArrayList<>();
System.out.println(list.size());     // 0
list.ensureCapacity(100);            // pre-allocate space (performance tip)
list.trimToSize();                   // shrink internal array to current size
```

**When to use `ensureCapacity`:** If you know you'll add 10,000 elements, pre-allocating saves ~log₂(10000) ≈ 14 resize operations.

### Sorting an ArrayList

```java
ArrayList<Integer> nums = new ArrayList<>(List.of(5, 2, 8, 1, 9));

// Natural order (ascending)
Collections.sort(nums);  // [1, 2, 5, 8, 9]

// Reverse order
Collections.sort(nums, Collections.reverseOrder());  // [9, 8, 5, 2, 1]

// Custom comparator
Collections.sort(nums, (a, b) -> b - a);  // descending

// Sort objects by a field
ArrayList<Student> students = getStudents();
Collections.sort(students, (s1, s2) -> s1.grade - s2.grade);

// Chained comparators
Collections.sort(students, Comparator
    .comparing(Student::getGrade)
    .thenComparing(Student::getName)
    .reversed());
```

### Common ArrayList Pitfalls

```java
// ⚠️ Removing elements while iterating (forward)
ArrayList<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4, 5));

// WRONG — concurrent modification
for (int i = 0; i < list.size(); i++) {
    if (list.get(i) % 2 == 0) list.remove(i);  // skip bug!
}
// After removing index 1 (value 2): list = [1,3,4,5]
// Next i=2: checks value 4, skips 3! Bug!

// RIGHT — iterate backwards
for (int i = list.size() - 1; i >= 0; i--) {
    if (list.get(i) % 2 == 0) list.remove(i);
}

// RIGHT — use iterator
Iterator<Integer> it = list.iterator();
while (it.hasNext()) {
    if (it.next() % 2 == 0) it.remove();
}

// RIGHT — removeIf (Java 8+)
list.removeIf(n -> n % 2 == 0);

// ⚠️ IndexOutOfBoundsException
list.get(list.size());  // ❌ index = size, max index = size-1
```

---

## 3. ArrayList vs LinkedList (Java Collections)

| Operation | ArrayList | LinkedList |
|-----------|-----------|------------|
| get(i) | O(1) | O(n) — must traverse |
| add(e) (at end) | O(1) amortized | O(1) |
| add(i, e) (at index) | O(n) — shift | O(n) — traverse to index |
| remove(i) | O(n) — shift | O(n) — traverse to index |
| remove(e) | O(n) | O(n) |
| Memory | Less overhead | More (prev/next pointers) |

**Verdict:** Use ArrayList 95% of the time. LinkedList is only better when you frequently add/remove at the **beginning** or need a **double-ended queue** (but `ArrayDeque` is even better for that).

---

## 4. Converting Between Arrays and ArrayLists

```java
// Array → ArrayList
int[] arr = {1, 2, 3, 4, 5};

// Method 1: Stream (Java 8+) — works with primitives
List<Integer> list1 = Arrays.stream(arr)
                            .boxed()
                            .collect(Collectors.toList());

// Method 2: Loop (verbose but clear)
List<Integer> list2 = new ArrayList<>();
for (int num : arr) list2.add(num);

// Method 3: For String/Integer arrays (not primitives)
Integer[] boxed = {1, 2, 3, 4, 5};
List<Integer> list3 = Arrays.asList(boxed);   // fixed-size!
List<Integer> list4 = new ArrayList<>(Arrays.asList(boxed));  // mutable

// ⚠️ Arrays.asList caveats
List<Integer> fixed = Arrays.asList(1, 2, 3);
fixed.set(0, 99);       // ✅ allowed
// fixed.add(4);         // ❌ UnsupportedOperationException — fixed-size!
// fixed.remove(0);     // ❌ UnsupportedOperationException — fixed-size!

// ArrayList → Array
List<Integer> list = new ArrayList<>(List.of(10, 20, 30));

// To Object[]
Object[] objArr = list.toArray();

// To typed array
Integer[] intArr = list.toArray(new Integer[0]);  // preferred idiom
int[] primitive = list.stream().mapToInt(i -> i).toArray();  // Java 8+
```

---

## 5. Multi-dimensional ArrayList

```java
// 2D ArrayList — ArrayList of ArrayLists
ArrayList<ArrayList<Integer>> matrix = new ArrayList<>();

// Initialize rows
int rows = 3, cols = 4;
for (int i = 0; i < rows; i++) {
    matrix.add(new ArrayList<>());
    for (int j = 0; j < cols; j++) {
        matrix.get(i).add(i * cols + j);
    }
}

// Access
int val = matrix.get(1).get(2);  // row 1, col 2

// Iteration
for (ArrayList<Integer> row : matrix) {
    for (int num : row) {
        System.out.print(num + " ");
    }
    System.out.println();
}
```

---

## 6. The `List.of()` Factory (Java 9+)

```java
List<String> immutable = List.of("a", "b", "c");
// immutable.add("d");  // ❌ UnsupportedOperationException

// Multiple overloads (up to 10 args, then varargs)
List<Integer> nums = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
```

---

## 7. Performance Tips

```java
// 1. Pre-size ArrayLists when you know the size
ArrayList<Integer> list = new ArrayList<>(1_000_000);  // avoid resizing

// 2. Prefer arrays over ArrayLists for primitives (memory + speed)
int[] arr = new int[n];           // ~4n bytes + header
ArrayList<Integer> list = new ArrayList<>(n);  // ~16n+ bytes + autoboxing overhead

// 3. Use System.arraycopy for bulk array operations (fastest)
int[] src = {1, 2, 3, 4, 5};
int[] dest = new int[10];
System.arraycopy(src, 0, dest, 0, src.length);  // native, very fast

// 4. Use Arrays.parallelSort for very large arrays (multithreaded)
Arrays.parallelSort(hugeArray);  // uses ForkJoinPool

// 5. ArrayList iteration: for-each is fine (uses internal iterator)
// Manual indexed loop is slightly faster for ArrayList (no iterator object)
```

---

## Cheat Sheet

```java
// ARRAYS
int[] a = new int[10];
int[] b = {1,2,3};
int len = a.length;
Arrays.sort(a);
Arrays.fill(a, 0);
Arrays.copyOf(a, a.length);
Arrays.binarySearch(a, key);
Arrays.toString(a);
Arrays.deepToString(matrix);
System.arraycopy(src, srcPos, dest, destPos, length);

// ARRAYLIST
ArrayList<Integer> list = new ArrayList<>();
list.add(e);  list.add(i, e);  list.get(i);  list.set(i, e);
list.remove(i);  list.remove(e);  list.contains(e);
list.indexOf(e);  list.size();  list.isEmpty();  list.clear();
list.toArray(new Integer[0]);
Collections.sort(list);
Collections.sort(list, (a,b) -> a-b);
```

Arrays and ArrayLists are your daily drivers in DSA. Get comfortable with every method above — you'll use them in literally every problem.
