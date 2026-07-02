# Sorting Algorithms Overview

## When to Use Which Sorting Algorithm

| Scenario | Best Algorithm | Why |
|----------|---------------|-----|
| Small array (< 50 elements) | Insertion Sort | Fast on small data, adaptive |
| Mostly sorted data | Insertion Sort | O(n) for nearly sorted |
| Large data, need stability | Merge Sort | O(n log n) guaranteed, stable |
| Large data, in-place preferred | Quick Sort | O(n log n) average, O(1) space |
| Large data with worst-case concerns | Heap Sort | O(n log n) guaranteed, no extra space |
| Need to sort in parallel | Parallel Sort (Java 8+) | Uses ForkJoin |
| Sorting integers (small range) | Counting Sort | O(n + k), linear |
| Sorting integers (large range) | Radix Sort | O(d × (n + b)) |
| Uniformly distributed data | Bucket Sort | O(n) average |
| Need top K elements | Heap / Quick Select | O(n + k log n) or O(n) |

## Stability, In-Place, Adaptive Properties

**Stable:** Equal elements maintain their original relative order.
- Stable: Bubble, Insertion, Merge, Counting, Radix
- Unstable: Selection, Quick, Heap

**In-place:** Uses O(1) or O(log n) extra space.
- In-place: Bubble, Selection, Insertion, Quick (log n stack), Heap
- Not in-place: Merge (O(n)), Counting (O(k)), Radix (O(n+b))

**Adaptive:** Performance improves on partially sorted data.
- Adaptive: Bubble, Insertion, Merge (natural variant)
- Not adaptive: Selection, Quick, Heap

## Java's Arrays.sort vs Collections.sort Internals

### Arrays.sort (Primitives)

Uses **Dual-Pivot QuickSort** (since Java 7).

```java
int[] arr = {5, 2, 9, 1, 3};
Arrays.sort(arr); // Dual-Pivot QuickSort
```

- Picks two pivots instead of one
- Partitions into three sections: < pivot1, between pivots, > pivot2
- Average: O(n log n), Worst: O(n²) — rare due to random pivot selection
- Not stable (but irrelevant for primitives — equal values are indistinguishable)

### Arrays.sort (Objects)

Uses **TimSort** (since Java 7), a hybrid of Merge Sort and Insertion Sort.

```java
String[] arr = {"banana", "apple", "cherry"};
Arrays.sort(arr); // TimSort
```

- Identifies "runs" of already-sorted data
- Merges runs using a stack
- Stable
- O(n log n) worst, O(n) on nearly sorted data
- Uses O(n) temporary space

### Collections.sort (List of Objects)

Delegates to `Arrays.sort` (TimSort).

```java
List<Integer> list = new ArrayList<>();
Collections.sort(list); // also TimSort
```

### List.sort (default method)

```java
list.sort(Comparator.naturalOrder()); // same TimSort behind the scenes
```

## Dual-Pivot QuickSort vs TimSort

| Feature | Dual-Pivot QuickSort | TimSort |
|---------|---------------------|---------|
| Used for | Primitive arrays | Object arrays/Collections |
| Stable? | No | Yes |
| Best case | O(n log n) | O(n) |
| Average | O(n log n) | O(n log n) |
| Worst case | O(n²) (extremely rare) | O(n log n) |
| Space | O(log n) stack | O(n) |
| Adaptivity | No | Yes (exploits runs) |

**Why different algorithms for primitives vs objects?** Primitives don't need stability (two 5s are indistinguishable). QuickSort is faster and uses less memory. Objects need stability for multi-key sorting (sort by name, then by date). TimSort guarantees stability.

## Comparison of All Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable | In-place | Adaptive |
|-----------|------|---------|-------|-------|--------|----------|----------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✓ | ✓ | ✓ |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | ✗ | ✓ | ✗ |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | ✓ | ✓ | ✓ |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | ✓ | ✗ | ✓ |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | ✗ | ✓ | ✗ |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | ✗ | ✓ | ✗ |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | ✓ | ✗ | ✗ |
| Radix | O(d(n+b)) | O(d(n+b)) | O(d(n+b)) | O(n+b) | ✓ | ✗ | ✗ |
| Bucket | O(n+k) | O(n+k) | O(n²) | O(n) | ✓ | ✗ | ✗ |

## Java Parallel Sort

Java 8+ provides `Arrays.parallelSort()` which uses ForkJoinPool for parallel sorting.

```java
int[] arr = generateHugeArray(100_000_000);
Arrays.parallelSort(arr); // splits, sorts in parallel, merges
```

- Uses parallel merge sort for objects
- Uses parallel Dual-Pivot QuickSort for primitives
- On large arrays (> 8192 elements), splits into chunks
- Each chunk is sorted by a separate thread
- Results are merged

**When to use:** Large arrays (millions+ elements) on multi-core machines. For small arrays, overhead > benefit.

## Comparator Usage

```java
// Natural order
Arrays.sort(arr);

// Custom comparator (objects only — not for primitives)
Arrays.sort(strings, (a, b) -> b.compareTo(a)); // descending

// Multiple criteria
Arrays.sort(persons, Comparator
    .comparing(Person::getLastName)
    .thenComparing(Person::getFirstName));

// Null handling
Arrays.sort(persons, Comparator.comparing(Person::getName, 
    Comparator.nullsLast(String::compareTo)));
```

## Quick Decision Flowchart

```
Is it an array of primitives?
├── Yes → Use Arrays.sort() (Dual-Pivot QuickSort)
└── No  → Collections.sort() or list.sort() (TimSort)

Do you need stable sort?
├── Yes → TimSort, Merge Sort, Counting Sort, Radix Sort
└── No  → QuickSort, HeapSort

Is the array nearly sorted?
├── Yes → Insertion Sort, TimSort
└── No  → Any O(n log n) algorithm

Is memory tight?
├── Yes → QuickSort, HeapSort, Insertion Sort
└── No  → Merge Sort, TimSort

Integer data with small range?
├── Yes → Counting Sort
└── No  → Comparison-based sort

String or fixed-width keys?
├── Yes → Radix Sort
└── No  → Comparison-based sort
```
