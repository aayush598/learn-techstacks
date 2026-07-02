# 03 — HashMap & HashSet in Java

If arrays are a hammer, HashMap is a Swiss Army knife. It's arguably the single most versatile data structure in DSA. Problems that would take O(n²) with brute force often become O(n) with a HashMap.

---

## 1. HashMap Basics

### What Is It?

A `HashMap<K, V>` stores key-value pairs. Keys are unique (no duplicates). Both keys and values can be any reference type.

```java
import java.util.*;

HashMap<String, Integer> map = new HashMap<>();

// Core operations — all O(1) average
map.put("Alice", 25);              // add or update
map.put("Bob", 30);
map.put("Charlie", 35);

System.out.println(map.get("Alice"));        // 25
System.out.println(map.get("NotHere"));      // null

// Getting with default
int age = map.getOrDefault("Dave", 0);       // 0 (not found)

// Check existence
System.out.println(map.containsKey("Alice"));   // true
System.out.println(map.containsValue(25));      // true — O(n), rarely used

// Remove
map.remove("Charlie");                  // removes entry, returns value (35)
map.remove("Alice", 25);               // removes only if key maps to that value

// Size & emptiness
System.out.println(map.size());         // 1 (Bob left)
System.out.println(map.isEmpty());      // false

// Clear all
map.clear();                            // removes all entries
```

### Iteration — 4 ways

```java
HashMap<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob", 87);
scores.put("Charlie", 92);

// 1. keySet() — iterate over keys
for (String name : scores.keySet()) {
    System.out.println(name + ": " + scores.get(name));
}

// 2. values() — iterate over values
for (int score : scores.values()) {
    System.out.println(score);
}

// 3. entrySet() — iterate over key-value pairs (most efficient)
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + " → " + entry.getValue());
    entry.setValue(entry.getValue() + 5);  // modify values during iteration
}

// 4. forEach (Java 8+)
scores.forEach((name, score) -> {
    System.out.println(name + " → " + score);
});
```

**Pro tip:** `entrySet()` is the most efficient for accessing both key and value simultaneously. `keySet()` + `get(key)` does an extra lookup per iteration.

---

## 2. Advanced HashMap Methods

### getOrDefault

```java
// Before Java 8 (verbose)
Integer val = map.get(key);
int count = (val == null) ? 0 : val;

// Java 8+ (clean)
int count = map.getOrDefault(key, 0);
```

### putIfAbsent

```java
// Only puts if key doesn't exist or value is null
map.putIfAbsent("Alice", 100);  // won't overwrite if "Alice" already exists

// Before: verbose
if (!map.containsKey(key)) {
    map.put(key, value);
}
```

### computeIfAbsent

```java
// Compute value only if key is absent — returns the value (new or existing)
List<Integer> list = map.computeIfAbsent("group1", k -> new ArrayList<>());
list.add(42);

// Classic use case: grouping
HashMap<String, List<Integer>> groups = new HashMap<>();
for (int num : numbers) {
    String key = getCategory(num);
    groups.computeIfAbsent(key, k -> new ArrayList<>()).add(num);
}
// Compare to old way:
// if (!groups.containsKey(key)) groups.put(key, new ArrayList<>());
// groups.get(key).add(num);
```

### merge — The Swiss Army Knife

```java
// merge(key, value, remappingFunction)
// If key absent: puts value. If key present: applies function(old, new)

HashMap<String, Integer> wordCount = new HashMap<>();

// Count frequencies — the cleanest pattern
for (String word : words) {
    wordCount.merge(word, 1, Integer::sum);
}
// Same as: wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
// But method reference is cleaner and potentially more efficient
```

### replace and replaceAll

```java
map.replace("Alice", 30);            // replace value for key (no-op if missing)
map.replace("Alice", 25, 30);        // replace only if currently 25
map.replaceAll((k, v) -> v * 2);     // transform all values
```

---

## 3. HashMap Internals — What's Under the Hood?

### Hashing

1. When you call `put(key, value)`, Java computes `hashCode()` of the key
2. The hash is used to find the **bucket index** (usually `hash & (n-1)` where n is array size, a power of 2)
3. If bucket is empty, the entry goes there
4. If bucket has entries (collision), it's stored as a **linked list** (or **tree** if many collisions)

```java
// Simplified view
// Internal array: Node<K,V>[] table
// Node structure: { int hash, K key, V value, Node<K,V> next }

// Bucket index calculation
int hash = key.hashCode();
int index = (n - 1) & hash;  // equivalent to hash % n, but faster
```

### Load Factor & Resizing

```java
HashMap<String, Integer> map = new HashMap<>(16, 0.75f);
// Default: capacity=16, loadFactor=0.75

// Threshold = capacity * loadFactor = 16 * 0.75 = 12
// When size exceeds 12 → resize (doubles capacity to 32)
// Rehash all entries → O(n) operation
// Happens rarely → O(1) amortized per insert
```

### Treeify Threshold (Java 8+)

```java
// When a bucket has ≥ 8 entries AND capacity ≥ 64:
// linked list → Red-Black Tree (O(n) → O(log n) for lookups)
// When bucket shrinks to ≤ 6: tree → linked list
// Why 8? Poisson distribution: probability ≈ 0.00000006 with good hash codes
```

### Key Requirements

```java
// For HashMap to work correctly:
// 1. If a.equals(b) then a.hashCode() == b.hashCode()  (MUST)
// 2. If a.hashCode() == b.hashCode(), a.equals(b) is NOT required (collision)
// 3. hashCode() should be consistent (same object = same hash)

// Common hashCode implementations
// String: s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]
// Integer: just the int value itself

// For custom objects as keys:
public class Person {
    String name;
    int age;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Person p)) return false;
        return age == p.age && Objects.equals(name, p.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);  // standard, good enough
    }
}
```

### Null Handling

```java
HashMap<String, Integer> map = new HashMap<>();
map.put(null, 1);        // null key is allowed
map.put("hello", null);  // null values are allowed
map.put(null, 2);        // overwrites previous null key entry
// System.out.println(map.get(null));  // 2
```

---

## 4. HashMap Variants

### LinkedHashMap — Maintains Insertion Order (LRU)

```java
LinkedHashMap<String, Integer> insertionOrder = new LinkedHashMap<>();
insertionOrder.put("Z", 1);
insertionOrder.put("A", 2);
insertionOrder.put("M", 3);
// Iteration order: Z → A → M (insertion order preserved)

// Access-order (for LRU caches)
LinkedHashMap<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
// 'true' = access-order. Most recently accessed moves to end.

// Simple LRU Cache
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

### TreeMap — Sorted Order (Red-Black Tree)

```java
TreeMap<String, Integer> sorted = new TreeMap<>();
sorted.put("Charlie", 3);
sorted.put("Alice", 1);
sorted.put("Bob", 2);
// Iteration order: Alice → Bob → Charlie (alphabetical)

// Navigation methods
sorted.firstKey();              // "Alice"
sorted.lastKey();               // "Charlie"
sorted.lowerKey("Bob");         // "Alice" (strictly less)
sorted.higherKey("Bob");        // "Charlie"
sorted.floorKey("B");           // "Alice" (less or equal)
sorted.ceilingKey("B");         // "Bob" (greater or equal)
sorted.subMap("A", "C");        // {Alice=1, Bob=2}
sorted.headMap("C");            // {Alice=1, Bob=2}
sorted.tailMap("B");            // {Bob=2, Charlie=3}
```

### Comparison Table

| Feature | HashMap | LinkedHashMap | TreeMap |
|---------|---------|---------------|---------|
| Ordering | None | Insertion/Access | Sorted (Comparable/Comparator) |
| Get/Put | O(1) avg | O(1) avg | O(log n) |
| Implementation | Hash table | Hash table + DLL | Red-Black Tree |
| Null keys | Yes | Yes | No (comparator can't handle null) |
| Memory | Lowest | Moderate | Higher |
| When to use | General purpose | Need predictable iteration | Need sorted traversal |

---

## 5. HashSet — When You Only Care About Keys

`HashSet<E>` is a `HashMap` under the hood using a dummy value (`PRESENT` = new Object()).

```java
HashSet<Integer> set = new HashSet<>();

// Core operations
set.add(10);              // O(1) — returns true if added, false if exists
set.add(20);
set.add(30);
set.add(20);              // false — already there

set.remove(10);           // O(1) — returns true if removed
boolean has = set.contains(20);  // O(1)
int size = set.size();
boolean empty = set.isEmpty();
set.clear();

// Bulk operations
HashSet<Integer> a = new HashSet<>(Set.of(1, 2, 3));
HashSet<Integer> b = new HashSet<>(Set.of(2, 3, 4));

a.addAll(b);              // union: {1,2,3,4}
a.retainAll(b);           // intersection: {2,3}
a.removeAll(b);           // difference: {1}
a.containsAll(b);         // superset check?

// Iteration
for (int num : set) {
    System.out.println(num);
}
set.forEach(System.out::println);

// Convert to array
Integer[] arr = set.toArray(new Integer[0]);
```

### LinkedHashSet & TreeSet

```java
LinkedHashSet<Integer> insertionOrder = new LinkedHashSet<>();
// Insertion order preserved — useful for removing duplicates while keeping order

TreeSet<Integer> sorted = new TreeSet<>();
// Sorted order — O(log n) operations
sorted.first();   // smallest
sorted.last();    // largest
sorted.lower(10); // greatest < 10
sorted.higher(10);// smallest > 10
sorted.subSet(5, 15); // elements in [5, 15)
```

---

## 6. Practical Problem Patterns

### Pattern 1: Count Frequencies

```java
int[] arr = {1, 2, 2, 3, 3, 3, 4};

// Method 1: getOrDefault
HashMap<Integer, Integer> freq = new HashMap<>();
for (int num : arr) {
    freq.put(num, freq.getOrDefault(num, 0) + 1);
}

// Method 2: merge (clever)
HashMap<Integer, Integer> freq = new HashMap<>();
for (int num : arr) {
    freq.merge(num, 1, Integer::sum);
}

// Method 3: compute
HashMap<Integer, Integer> freq = new HashMap<>();
for (int num : arr) {
    freq.compute(num, (k, v) -> (v == null) ? 1 : v + 1);
}

// Result: {1=1, 2=2, 3=3, 4=1}
```

### Pattern 2: Find Duplicates

```java
public List<Integer> findDuplicates(int[] arr) {
    HashSet<Integer> seen = new HashSet<>();
    List<Integer> duplicates = new ArrayList<>();

    for (int num : arr) {
        if (!seen.add(num)) {  // add returns false if already present
            duplicates.add(num);
        }
    }
    return duplicates;
}
```

### Pattern 3: Two Sum

```java
public int[] twoSum(int[] nums, int target) {
    HashMap<Integer, Integer> map = new HashMap<>();  // value → index

    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```

### Pattern 4: Group Anagrams

```java
public List<List<String>> groupAnagrams(String[] strs) {
    HashMap<String, List<String>> map = new HashMap<>();

    for (String s : strs) {
        // Sorted string as key
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);

        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}
```

### Pattern 5: First Non-Repeating Character

```java
public char firstNonRepeating(String s) {
    HashMap<Character, Integer> freq = new HashMap<>();

    for (char c : s.toCharArray()) {
        freq.put(c, freq.getOrDefault(c, 0) + 1);
    }
    for (char c : s.toCharArray()) {
        if (freq.get(c) == 1) return c;
    }
    return '_';  // placeholder
}
```

### Pattern 6: Subarray Sum Equals K

```java
public int subarraySum(int[] nums, int k) {
    HashMap<Integer, Integer> prefixSumFreq = new HashMap<>();
    prefixSumFreq.put(0, 1);  // base case

    int sum = 0, count = 0;
    for (int num : nums) {
        sum += num;
        // If sum - k exists, subarray between those sums equals k
        count += prefixSumFreq.getOrDefault(sum - k, 0);
        prefixSumFreq.put(sum, prefixSumFreq.getOrDefault(sum, 0) + 1);
    }
    return count;
}
```

---

## 7. HashMap Performance Pitfalls

```java
// ⚠️ Iterating while modifying (structural change)
HashMap<String, Integer> map = new HashMap<>();
map.put("a", 1); map.put("b", 2); map.put("c", 3);

// ❌ ConcurrentModificationException
for (String key : map.keySet()) {
    if (key.equals("b")) map.remove(key);
}

// ✅ Use iterator
Iterator<String> it = map.keySet().iterator();
while (it.hasNext()) {
    if (it.next().equals("b")) it.remove();
}

// ✅ Or use removeIf (Java 8+)
map.keySet().removeIf(key -> key.equals("b"));

// ⚠️ Bad hashCode → O(n) performance
// If all keys hash to same bucket, HashMap degenerates to linked list
// This is a DoS attack vector (hash collision attack)

// ⚠️ Mutable keys
List<Integer> key = new ArrayList<>(List.of(1, 2));
map.put(key, "value");
key.add(3);  // ⚠️ hash changes! Can never find this entry again
// Never use mutable objects as HashMap keys
```

---

## Cheat Sheet

```java
// HASHMAP
HashMap<K,V> map = new HashMap<>();
map.put(k,v);  map.get(k);  map.getOrDefault(k, def);
map.containsKey(k);  map.containsValue(v);
map.remove(k);  map.remove(k,v);
map.size();  map.isEmpty();  map.clear();
map.keySet();  map.values();  map.entrySet();
map.forEach((k,v) -> {});
map.putIfAbsent(k,v);
map.computeIfAbsent(k, fn);
map.merge(k, v, Integer::sum);

// HASHSET
HashSet<E> set = new HashSet<>();
set.add(e);  set.remove(e);  set.contains(e);
set.size();  set.isEmpty();  set.clear();
for (E e : set) {}

// VARIANTS
LinkedHashMap<K,V> insOrder = new LinkedHashMap<>();
TreeMap<K,V> sorted = new TreeMap<>();
LinkedHashSet<E> insOrderSet = new LinkedHashSet<>();
TreeSet<E> sortedSet = new TreeSet<>();
```

HashMap and HashSet will appear in ~40% of medium-level interview problems. Master the patterns above and you'll have a massive head start.
