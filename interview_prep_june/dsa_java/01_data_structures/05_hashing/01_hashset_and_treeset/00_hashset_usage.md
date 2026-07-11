# HashSet Usage

## Internals

HashSet is literally a HashMap with dummy values:
```java
private static final Object PRESENT = new Object();
private transient HashMap<E,Object> map;

public boolean add(E e) { return map.put(e, PRESENT) == null; }
public boolean contains(Object o) { return map.containsKey(o); }
public boolean remove(Object o) { return map.remove(o) == PRESENT; }
```

## Key Characteristics

- **No duplicates**: add returns false if element exists
- **No order guarantee**: iteration order may appear random
- **O(1)** average for add, remove, contains
- **Allows one null** element

## Important Methods

```java
Set<String> set = new HashSet<>();

set.add("apple");              // true
set.add("apple");              // false (already exists)
set.contains("apple");         // true
set.remove("apple");           // true
set.size();                    // 0
set.isEmpty();                 // true
set.clear();                   // remove all
```

## Iteration

```java
// for-each (most common)
for (String s : set) { ... }

// forEach with lambda
set.forEach(s -> { ... });

// Iterator
Iterator<String> it = set.iterator();
while (it.hasNext()) { String s = it.next(); }
```

## Common DSA Use Cases

**1. Deduplication**: Remove duplicates from array/stream
```java
int[] arr = {1,2,2,3,4,4,5};
Set<Integer> unique = new HashSet<>();
for (int x : arr) unique.add(x);
```

**2. Check if element exists (fast lookup)**
```java
Set<Integer> visited = new HashSet<>();
if (visited.contains(node)) continue;
```

**3. Intersection / Union / Difference**
```java
Set<Integer> a = new HashSet<>(List.of(1,2,3));
Set<Integer> b = Set.of(3,4,5);

// Union
Set<Integer> union = new HashSet<>(a);
union.addAll(b);  // {1,2,3,4,5}

// Intersection
Set<Integer> intersection = new HashSet<>(a);
intersection.retainAll(b);  // {3}

// Difference
Set<Integer> diff = new HashSet<>(a);
diff.removeAll(b);  // {1,2}
```

## LinkedHashSet

Maintains **insertion order** (doubly linked list chain in backing HashMap):
```java
Set<String> ordered = new LinkedHashSet<>();
ordered.add("a"); ordered.add("b"); ordered.add("c");
// iteration always: a, b, c
```

## Performance Comparison

| Operation | HashSet | TreeSet | LinkedHashSet |
|-----------|---------|---------|---------------|
| add | O(1)* | O(log n) | O(1)* |
| contains | O(1)* | O(log n) | O(1)* |
| remove | O(1)* | O(log n) | O(1)* |
| iteration | O(n) unpredictable | O(n) sorted | O(n) insertion order |
| space | O(n) | O(n) | O(n + pointer) |

*amortized average case
