# Ordered Set & Multiset

## TreeMap as Multiset

Java doesn't have a built-in multiset. Use TreeMap<K, Integer>:

```java
class Multiset<T extends Comparable<T>> {
    private TreeMap<T, Integer> map = new TreeMap<>();
    
    void add(T element) { map.merge(element, 1, Integer::sum); }
    
    void remove(T element) {
        if (!map.containsKey(element)) return;
        map.merge(element, -1, Integer::sum);
        if (map.get(element) == 0) map.remove(element);
    }
    
    int count(T element) { return map.getOrDefault(element, 0); }
    
    T first() { return map.firstKey(); }
    T last() { return map.lastKey(); }
    
    T lower(T key) { return map.lowerKey(key); }
    T floor(T key) { return map.floorKey(key); }
    T ceiling(T key) { return map.ceilingKey(key); }
    T higher(T key) { return map.higherKey(key); }
    
    int size() { return map.values().stream().mapToInt(Integer::intValue).sum(); }
    
    List<T> toList() {
        List<T> list = new ArrayList<>();
        for (Map.Entry<T, Integer> e : map.entrySet()) {
            for (int i = 0; i < e.getValue(); i++) list.add(e.getKey());
        }
        return list;
    }
}
```

## Order Statistics with Fenwick Tree

When values are bounded (e.g., ≤ 10⁶), get Kth smallest:

```java
class OrderStatisticTree {
    int[] bit;
    int maxVal;
    
    OrderStatisticTree(int max) {
        maxVal = max;
        bit = new int[max + 2];
    }
    
    void add(int val, int delta) {
        for (int i = val; i <= maxVal; i += i & -i) bit[i] += delta;
    }
    
    int countLessThan(int val) {  // prefix sum
        int sum = 0;
        for (int i = val - 1; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
    
    int kthSmallest(int k) {  // 1-indexed
        int lo = 1, hi = maxVal;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (countLessThan(mid + 1) >= k) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
}
```
