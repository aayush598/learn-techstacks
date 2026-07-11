# TreeSet Usage

## Internals

TreeSet is backed by TreeMap (Red-Black Tree):
```java
private transient NavigableMap<E,Object> m;
public TreeSet() { this(new TreeMap<>()); }
```

## Key Characteristics

- **Sorted order**: natural ordering (Comparable) or custom Comparator
- **O(log n)** for add, remove, contains (tree operations)
- **No duplicates**
- **Does NOT allow null** (requires comparison)
- Provides navigation methods (floor, ceiling, higher, lower)

## Essential Methods

```java
TreeSet<Integer> set = new TreeSet<>();
set.addAll(List.of(3, 1, 4, 1, 5, 9, 2, 6));
// set = {1, 2, 3, 4, 5, 6, 9}

// Basic
set.first();          // 1 (smallest)
set.last();           // 9 (largest)

// Navigation
set.ceiling(4);       // 4 (smallest >= 4)
set.floor(4);         // 4 (largest <= 4)
set.higher(4);        // 5 (smallest > 4)
set.lower(4);         // 3 (largest < 4)

// Range views
set.headSet(4);       // {1, 2, 3} (< 4)
set.headSet(4, true); // {1, 2, 3, 4} (<= 4)
set.tailSet(4);       // {4, 5, 6, 9} (>= 4)
set.subSet(2, 6);     // {2, 3, 4, 5} ([2, 6))
set.subSet(2, true, 6, true); // {2, 3, 4, 5, 6}

// Poll (extract and remove)
set.pollFirst();      // 1 (now set = {2, 3, 4, 5, 6, 9})
set.pollLast();       // 9

// Reverse order
set.descendingSet();  // {6, 5, 4, 3, 2}
set.descendingIterator();
```

## Custom Comparator

```java
// Reverse order
TreeSet<Integer> rev = new TreeSet<>(Comparator.reverseOrder());

// By string length
TreeSet<String> byLen = new TreeSet<>(
    Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder())
);
byLen.add("a"); byLen.add("bb"); byLen.add("ccc");
// order: a, bb, ccc
```

## When to Use TreeSet vs HashSet

**Use TreeSet when**:
- You need sorted iteration
- You need range queries (headSet, subSet)
- You need floor/ceiling operations
- Maintaining order is more important than O(log n) speed

**Use HashSet when**:
- Only need uniqueness + lookup
- O(1) is more important
- Order doesn't matter

## Common DSA Problems Solved with TreeSet

1. **Count of Smaller Numbers After Self**: Use TreeSet with size tracking
2. **Range Sum Queries with Updates**: TreeMap for intervals
3. **My Calendar I/II**: TreeMap of start->end events
4. **Finding median in data stream**: Two TreeSets (balanced)
5. **Longest Consecutive Sequence**: O(n) better with HashSet, but TreeSet also works

```java
// Example: find closest element to target in sorted set
int closestTo(TreeSet<Integer> set, int target) {
    Integer floor = set.floor(target);
    Integer ceil = set.ceiling(target);
    if (floor == null) return ceil;
    if (ceil == null) return floor;
    return (target - floor <= ceil - target) ? floor : ceil;
}
```
