# Collision Handling in HashMap

## What is a Collision?

When two different keys produce the same bucket index: collision.

## 1. Chaining (Separate Chaining) — Java's Approach

Each bucket stores a linked list of entries with the same hash.

**Pros**: Simple, handles high load factors, no limit on entries
**Cons**: Memory overhead for pointers, O(n) search in worst case

Java improves this by **treeifying** chains longer than 8 nodes (Red-Black Tree, O(log n) search).

## 2. Open Addressing

All entries stored directly in the table array. On collision, find another slot.

**Linear Probing**: `index = (hash + i) % tableSize`
- Easy but causes **primary clustering** (long runs of occupied slots)

**Quadratic Probing**: `index = (hash + c1*i + c2*i²) % tableSize`  
- Reduces clustering but may not probe all slots

**Double Hashing**: `index = (hash + i * hash2(key)) % tableSize`
- Best distribution but more computation

## Java's Choice: Chaining with Treeification

```
chain length ≤ 8 → LinkedList (traverse, compare equals)
chain length > 8 AND capacity ≥ 64 → Red-Black Tree
capacity < 64 → resize instead (double capacity)
```

## Implement Simple HashMap with Chaining

```java
class MyHashMap<K, V> {
    private static class Entry<K, V> {
        K key; V value; Entry<K,V> next;
        Entry(K k, V v) { key = k; value = v; }
    }
    
    private Entry<K,V>[] buckets;
    private int size = 0;
    private static final double LOAD_FACTOR = 0.75;
    
    MyHashMap() { buckets = new Entry[16]; }
    
    private int hash(K key) {
        return (key == null) ? 0 : key.hashCode() & (buckets.length - 1);
    }
    
    public void put(K key, V value) {
        int idx = hash(key);
        Entry<K,V> head = buckets[idx];
        // Search for existing key
        for (Entry<K,V> e = head; e != null; e = e.next) {
            if (e.key.equals(key)) { e.value = value; return; }
        }
        // Insert at front
        Entry<K,V> newEntry = new Entry<>(key, value);
        newEntry.next = head;
        buckets[idx] = newEntry;
        size++;
        if (size > buckets.length * LOAD_FACTOR) resize();
    }
    
    public V get(K key) {
        int idx = hash(key);
        for (Entry<K,V> e = buckets[idx]; e != null; e = e.next) {
            if (e.key.equals(key)) return e.value;
        }
        return null;
    }
    
    private void resize() {
        Entry<K,V>[] old = buckets;
        buckets = new Entry[old.length * 2];
        size = 0;
        for (Entry<K,V> head : old) {
            for (Entry<K,V> e = head; e != null; e = e.next) {
                put(e.key, e.value);
            }
        }
    }
}
```
