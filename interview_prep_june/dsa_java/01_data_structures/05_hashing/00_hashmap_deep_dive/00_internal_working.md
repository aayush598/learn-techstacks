# HashMap Internal Working

## The Big Picture

HashMap is the most used data structure in DSA interviews. Understanding its internals separates good candidates from great ones.

## Core Structure

HashMap stores key-value pairs in an **array of buckets**:
```java
Node<K,V>[] table;  // array of buckets
```

Each bucket is a linked list (or tree in Java 8+):
```java
static class Node<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
}
```

## How `put(key, value)` works

1. **Hash computation**: `key.hashCode()` → `h ^ (h >>> 16)` (spread high bits)
2. **Index calculation**: `hash & (table.length - 1)` (only works if length is power of 2)
3. **Bucket lookup**: If bucket empty → insert directly
4. **Collision handling**: If bucket occupied → traverse chain comparing hashes + equals
   - Same key (equals true) → replace value
   - Different key → add to end of chain
5. **Treeify**: If chain length > 8 → convert to Red-Black Tree (Java 8+)
6. **Resize check**: If `size > threshold (capacity * 0.75)` → resize

## How `get(key)` works

1. Hash the key
2. Find bucket index
3. Traverse chain: `e.hash == hash && (e.key == key || key.equals(e.key))`
4. Return value or null

## hashCode() and equals() contract

- If `a.equals(b)` is true → `a.hashCode() == b.hashCode()` MUST be true
- If `a.hashCode() == b.hashCode()` → `a.equals(b)` MAY be true (collision)
- Both must be consistent (same object → same values each call)
- Common equals implementation: check `==`, then `instanceof`, then field comparison

## Why length is always power of 2

- `hash % n == hash & (n-1)` when n is power of 2
- Bitwise AND is faster than modulo
- Good distribution of keys across buckets

## Java 8+ Optimization

- Threshold: `TREEIFY_THRESHOLD = 8` → convert linked list to Red-Black tree
- Untreeify: `UNTREEIFY_THRESHOLD = 6` → convert back during resize
- `MIN_TREEIFY_CAPACITY = 64` → treeify only if capacity >= 64
- Tree search: O(log n) vs Linked list: O(n) for collisions
