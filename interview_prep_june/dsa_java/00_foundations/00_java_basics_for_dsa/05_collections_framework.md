# 05 — Java Collections Framework

The Java Collections Framework is a unified architecture for storing and manipulating groups of objects. It's one of the most powerful parts of the standard library, and you'll use it constantly in DSA.

---

## 1. Collection Interface Hierarchy

```
Iterable (interface)
  └── Collection (interface)
        ├── List (interface) — ordered, allows duplicates, indexed access
        │     ├── ArrayList
        │     ├── LinkedList
        │     ├── Vector (legacy, synchronized)
        │     └── Stack (legacy, extends Vector)
        │
        ├── Set (interface) — no duplicates, no guaranteed order
        │     ├── HashSet
        │     ├── LinkedHashSet
        │     └── SortedSet → TreeSet
        │
        └── Queue (interface) — FIFO, LIFO, priority order
              ├── PriorityQueue
              ├── LinkedList (also Queue)
              └── Deque (interface)
                    ├── ArrayDeque
                    └── LinkedList
```

### The Root Interfaces

```java
// Iterable — can be used in for-each
Iterable<String> iterable = List.of("a", "b", "c");
for (String s : iterable) { }

// Collection — basic operations
Collection<String> col = new ArrayList<>();
col.add("a");
col.remove("a");
col.contains("a");
col.size();
col.isEmpty();
col.clear();
col.addAll(other);
col.removeAll(other);
col.retainAll(other);  // intersection
col.containsAll(other);
col.toArray();
```

---

## 2. List Interface

### ArrayList — The King

```java
List<String> list = new ArrayList<>();

// Creation
List<String> fromElements = List.of("a", "b", "c");       // immutable, Java 9+
List<String> fromArray = Arrays.asList("a", "b", "c");    // fixed-size view

// Bulk operations
list.addAll(List.of("d", "e"));
list.removeAll(Set.of("a", "b"));   // remove all matching
list.retainAll(Set.of("a", "c"));   // keep only matching

// Sublist — view, not copy!
List<String> sub = list.subList(0, 2);
sub.set(0, "modified");     // modifies the original list!
// ⚠️ Structural changes to original list while sublist exists = ConcurrentModificationException

// Searching
list.sort(null);                  // natural order
list.sort(Comparator.reverseOrder());
Collections.sort(list);           // same as list.sort(null)
Collections.reverse(list);
Collections.rotate(list, 2);      // rotate right by 2
Collections.shuffle(list);        // random permutation
```

### LinkedList — When You Need Deque Operations

```java
LinkedList<String> list = new LinkedList<>();

// List operations
list.add("b");
list.add(0, "a");     // add at front — O(1)

// Deque operations
list.addFirst("z");   // O(1)
list.addLast("x");    // O(1)
list.getFirst();      // O(1)
list.getLast();       // O(1)
list.removeFirst();   // O(1)
list.removeLast();    // O(1)

// Stack operations
list.push("top");     // addFirst
list.pop();           // removeFirst
list.peek();          // getFirst

// Queue operations
list.offer("end");    // addLast
list.poll();          // removeFirst
list.element();       // getFirst
```

### Vector & Stack — Legacy, Avoid

```java
Vector<String> vector = new Vector<>();   // synchronized = slow
Stack<String> stack = new Stack<>();      // extends Vector, also slow

// If you need a stack:
Deque<String> betterStack = new ArrayDeque<>();
betterStack.push("a");
betterStack.pop();
betterStack.peek();
```

**Why ArrayDeque is better than Stack:** Stack extends Vector, which is synchronized (slow). ArrayDeque is unsynchronized, has no capacity restrictions, and is faster.

---

## 3. Set Interface

### HashSet — O(1) operations, no order

```java
Set<Integer> set = new HashSet<>();

set.add(3); set.add(1); set.add(2);
set.add(3);  // returns false — already there

// Iteration order is NOT guaranteed (based on hash codes)
for (int x : set) { }  // could be any order

// Bulk set operations (modify the set)
Set<Integer> a = new HashSet<>(Set.of(1, 2, 3));
Set<Integer> b = new HashSet<>(Set.of(2, 3, 4));

Set<Integer> union = new HashSet<>(a);
union.addAll(b);              // {1, 2, 3, 4}

Set<Integer> intersection = new HashSet<>(a);
intersection.retainAll(b);    // {2, 3}

Set<Integer> difference = new HashSet<>(a);
difference.removeAll(b);      // {1}
```

### LinkedHashSet — Insertion order

```java
Set<Integer> set = new LinkedHashSet<>();
set.add(3); set.add(1); set.add(2);
// Iteration: 3 → 1 → 2 (insertion order preserved)
```

### TreeSet — Sorted, O(log n)

```java
TreeSet<Integer> set = new TreeSet<>();
set.add(5); set.add(1); set.add(9);

// Navigation
set.first();          // 1
set.last();           // 9
set.lower(5);         // 1 (strictly less)
set.higher(5);        // 9 (strictly greater)
set.floor(5);         // 5 (less or equal)
set.ceiling(5);       // 5 (greater or equal)

set.subSet(2, 8);     // elements in [2, 8)
set.headSet(5);       // elements < 5
set.tailSet(5);       // elements >= 5

// Custom comparator
TreeSet<String> byLength = new TreeSet<>(Comparator.comparingInt(String::length));
byLength.add("a"); byLength.add("bb"); byLength.add("ccc");
// ⚠️ TreeSet uses compareTo() for equality, not equals()!
// If comparator says two strings are equal (same length), only one is stored
```

---

## 4. Queue Interface

### PriorityQueue — Heap

```java
// Min-heap (default) — smallest element first
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5); minHeap.offer(1); minHeap.offer(9);
minHeap.peek();   // 1 (smallest)
minHeap.poll();   // 1, now heap has {5, 9}

// Max-heap — use reverse comparator
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

// Custom comparator
PriorityQueue<Map.Entry<String, Integer>> pq = new PriorityQueue<>(
    (a, b) -> b.getValue() - a.getValue()  // descending by value
);

// ⚠️ PriorityQueue iterator does NOT guarantee order!
for (int x : pq) { }  // not sorted!
// Only poll() gives elements in priority order

// Offer/poll = O(log n), peek = O(1), remove(Object) = O(n)
```

### LinkedList as Queue

```java
Queue<String> queue = new LinkedList<>();
queue.offer("a"); queue.offer("b"); queue.offer("c");
queue.peek();   // "a"
queue.poll();   // "a", queue now = [b, c]
queue.element(); // "b" (like peek but throws if empty)
queue.remove();  // "b" (like poll but throws if empty)
```

### ArrayDeque — Best All-Rounder

```java
ArrayDeque<String> deque = new ArrayDeque<>();

// As queue (FIFO)
deque.offer("a");   // add to tail
deque.offer("b");
deque.poll();       // remove from head → "a"

// As stack (LIFO)
deque.push("a");    // add to head
deque.push("b");
deque.pop();        // remove from head → "b"

// Full deque API
deque.addFirst("x");   // throws if full (it won't — no capacity limit)
deque.addLast("y");
deque.offerFirst("z"); // returns false if full
deque.offerLast("w");
deque.getFirst();      // throws if empty
deque.getLast();
deque.peekFirst();     // null if empty
deque.peekLast();
deque.removeFirst();
deque.removeLast();
deque.pollFirst();
deque.pollLast();
deque.removeFirstOccurrence("x");
deque.removeLastOccurrence("x");
```

**Why ArrayDeque rocks:**
- Faster than Stack (not synchronized)
- Faster than LinkedList (locality of reference)
- No capacity limits (resizable array)
- Implements both Queue and Deque

---

## 5. Collections Utility Class

```java
import java.util.*;

List<Integer> list = new ArrayList<>(List.of(5, 2, 8, 1, 9, 2));

// Sorting & ordering
Collections.sort(list);                          // [1, 2, 2, 5, 8, 9]
Collections.sort(list, Comparator.reverseOrder()); // [9, 8, 5, 2, 2, 1]
Collections.reverse(list);                       // reverse current order
Collections.shuffle(list);                       // random permutation
Collections.rotate(list, 2);                     // rotate right: [2, 9, ...]

// Searching (must be sorted first!)
Collections.sort(list);
int idx = Collections.binarySearch(list, 5);     // 3 (index)
int notFound = Collections.binarySearch(list, 10); // -7

// Min/Max/Frequency
int min = Collections.min(list);
int max = Collections.max(list);
int freq = Collections.frequency(list, 2);       // 2

// Disjoint — check if two collections have no common elements
boolean noOverlap = Collections.disjoint(list1, list2);

// Swapping
Collections.swap(list, 0, 1);                     // swap elements at indices

// Filling
Collections.fill(list, 0);                        // replace all with 0

// Copying
List<Integer> dest = new ArrayList<>(Collections.nCopies(6, 0));
Collections.copy(dest, source);                   // dest must be same size or larger

// Factory methods (immutable)
List<Integer> singleton = Collections.singletonList(42);  // single element
List<Integer> nCopies = Collections.nCopies(5, "x");     // ["x","x","x","x","x"]

// Unmodifiable views (read-only)
List<Integer> readOnly = Collections.unmodifiableList(list);
// readOnly.add(1);  // ❌ UnsupportedOperationException
// Changes to underlying list are reflected in the view

// Synchronized wrappers (thread-safe)
List<Integer> syncList = Collections.synchronizedList(new ArrayList<>());
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
```

---

## 6. Arrays Utility Class

```java
int[] arr = {5, 2, 8, 1, 9};

// Converting to List
List<Integer> list = Arrays.asList(1, 2, 3);     // fixed-size!
// list.add(4);  // ❌ UnsupportedOperationException

// For primitives:
List<Integer> boxed = Arrays.stream(arr)
                            .boxed()
                            .collect(Collectors.toList());

// String representation
System.out.println(Arrays.toString(arr));          // [5, 2, 8, 1, 9]
int[][] mat = {{1,2}, {3,4}};
System.out.println(Arrays.deepToString(mat));      // [[1,2],[3,4]]

// Filling
Arrays.fill(arr, 0);
Arrays.fill(arr, 1, 4, 42);  // indices [1,4) = 42

// Sorting
Arrays.sort(arr);                      // full sort
Arrays.sort(arr, 1, 4);                // sort range [1,4)
Arrays.parallelSort(arr);              // multi-threaded for large arrays

// Searching (must be sorted)
int idx = Arrays.binarySearch(arr, 5);
int idxRange = Arrays.binarySearch(arr, 1, 4, 5);

// Copying
int[] copy = Arrays.copyOf(arr, arr.length);
int[] first3 = Arrays.copyOf(arr, 3);
int[] range = Arrays.copyOfRange(arr, 1, 4);  // [indices 1,4)

// Comparison
boolean eq = Arrays.equals(arr1, arr2);               // 1D
boolean deepEq = Arrays.deepEquals(mat1, mat2);       // multidimensional

// Hash
int hash = Arrays.hashCode(arr);
int deepHash = Arrays.deepHashCode(mat);

// Set all elements using generator function (Java 8+)
Arrays.setAll(arr, i -> i * i);   // arr = [0, 1, 4, 9, 16]
Arrays.parallelSetAll(arr, i -> i * i);

// Stream (Java 8+)
int sum = Arrays.stream(arr).sum();
double avg = Arrays.stream(arr).average().orElse(0);
long count = Arrays.stream(arr).filter(x -> x > 5).count();
```

---

## 7. Iterator, ListIterator, Fail-Fast vs Fail-Safe

### Iterator — Universal Traversal

```java
Collection<String> collection = new ArrayList<>(List.of("a", "b", "c"));

Iterator<String> it = collection.iterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.equals("b")) {
        it.remove();  // ✅ safe removal during iteration
    }
}
// ⚠️ collection.remove(s) during iteration = ConcurrentModificationException
```

### ListIterator — Bidirectional

```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));

ListIterator<String> it = list.listIterator();
// Forward
while (it.hasNext()) {
    int idx = it.nextIndex();
    String s = it.next();
    if (s.equals("b")) {
        it.set("modified");   // modify current element
        it.add("new");        // add after current
    }
}

// Backward
while (it.hasPrevious()) {
    int idx = it.previousIndex();
    String s = it.previous();
}
```

### Fail-Fast vs Fail-Safe

```java
// Fail-Fast (most collections): throws ConcurrentModificationException
// if collection is modified structurally during iteration

List<String> list = new ArrayList<>(List.of("a", "b", "c"));
for (String s : list) {      // uses iterator internally
    if (s.equals("b")) {
        // list.remove(s);   // ❌ ConcurrentModificationException
    }
}

// ✅ Safe removal: use iterator.remove()
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().equals("b")) it.remove();
}

// ✅ Safe removal using removeIf (Java 8+)
list.removeIf(s -> s.equals("b"));

// Fail-Safe (java.util.concurrent): creates a snapshot
// or uses a safe copy internally
CopyOnWriteArrayList<String> safeList = new CopyOnWriteArrayList<>(List.of("a", "b", "c"));
for (String s : safeList) {
    safeList.add("d");  // ✅ OK — iteration uses snapshot
}
// ⚠️ Fail-safe has memory overhead (copying)
```

---

## 8. Quick Decision Guide

```
Need a sequence?
  ├── Indexed access? → ArrayList
  ├── Queue/Stack/Deque? → ArrayDeque (1st choice) or LinkedList
  ├── Frequent insert/delete at middle? → ArrayList (still fine), consider LinkedList
  └── FIFO queue? → LinkedList or ArrayDeque

Need unique elements?
  ├── O(1) ops, no ordering? → HashSet
  ├── Insertion order? → LinkedHashSet
  └── Sorted? → TreeSet (O(log n))

Need key-value pairs?
  ├── O(1), no ordering? → HashMap
  ├── Insertion order? → LinkedHashMap
  └── Sorted keys? → TreeMap (O(log n))

Need priority ordering? → PriorityQueue (heap)

Need thread safety?
  ├── Collections.synchronizedXxx() wrapper
  └── java.util.concurrent: ConcurrentHashMap, CopyOnWriteArrayList
```

---

## Cheat Sheet

```java
// LISTS
new ArrayList<>();  new LinkedList<>();
list.get(i); list.set(i, e); list.add(e); list.remove(i);
Collections.sort(list); Collections.reverse(list);

// SETS
new HashSet<>(); new LinkedHashSet<>(); new TreeSet<>();
set.add(e); set.contains(e); set.remove(e);

// QUEUES - DEQUES
new ArrayDeque<>();  // stack: push/pop/peek; queue: offer/poll/peek
new PriorityQueue<>(); // minHeap: offer/poll/peek

// MAPS (in next file, but relevant)
new HashMap<>(); new LinkedHashMap<>(); new TreeMap<>();

// UTILITY CLASSES
Collections.sort(list); Collections.binarySearch(list, k);
Collections.min/max/frequency/swap/shuffle/reverse/fill/copy/nCopies
Arrays.sort(arr); Arrays.binarySearch(arr, k);
Arrays.toString/deepToString; Arrays.fill; Arrays.copyOf;
Arrays.equals/deepEquals; Arrays.stream(arr);
```

The Collections Framework is your toolkit. Know what's available so you don't reinvent the wheel.
