# Load Factor & Resizing

## Key Concepts

**Load Factor** = `number of entries / number of buckets`

Default in Java HashMap: **0.75**

**Threshold** = `capacity * load factor` — when size exceeds this, resize happens.

## Why 0.75?

Trade-off between time and space:
- **Lower (0.5)**: fewer collisions, more memory, frequent resizes
- **Higher (0.9)**: more collisions, less memory, fewer resizes
- 0.75 is the empirical sweet spot

## Resizing (Rehashing) Process

1. Create new array: `newCap = oldCap * 2`
2. Recompute index for each entry: `hash & (newCap - 1)`
3. Transfer entries to new buckets

```java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;
    int newCap = oldCap * 2;
    int newThr = (int)(newCap * LOAD_FACTOR);
    
    Node<K,V>[] newTab = new Node[newCap];
    transfer(oldTab, newTab);
    table = newTab;
    threshold = newThr;
    return newTab;
}
```

## Amortized O(1) Analysis

- Each insert: O(1) average (usually)
- Resize costs O(n) but happens rarely
- After resize to capacity C, next C/2 inserts don't trigger resize
- Cost spread out: each insert "pays" a constant amount toward future resize

**Formal proof**:
- Total cost of resizing from capacity 1 to n: 1 + 2 + 4 + 8 + ... + n ≈ 2n
- Per insert: O(2n / n) = O(1) amortized

## Performance Impact

- Frequent resizes waste memory and CPU
- If you know size in advance: `new HashMap<>(expectedSize)`
- For large maps: `new HashMap<>(expectedSize / 0.75f + 1, 0.75f)`
- Resizing is the most expensive HashMap operation
- Worst case: each insert triggers resize → O(n²) total

## HashMap Initial Capacity Best Practices

```java
// Expected 1000 entries:
Map<K,V> map = new HashMap<>(1000);  // capacity 1000, threshold 750
// Better:
Map<K,V> map = new HashMap<>(1337);  // ~1000/0.75, avoids early resize
```
