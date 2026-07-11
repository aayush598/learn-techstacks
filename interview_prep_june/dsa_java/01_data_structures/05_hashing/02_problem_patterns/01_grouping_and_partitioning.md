# Grouping and Partitioning Patterns

## The Master Pattern: computeIfAbsent

```java
map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
```

## Problem 1: Group Anagrams

```java
List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```

**Alternative key** (faster, avoids sort):
```java
String getKey(String s) {
    int[] count = new int[26];
    for (char c : s.toCharArray()) count[c - 'a']++;
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < 26; i++) {
        sb.append('#').append(count[i]);
    }
    return sb.toString();
}
```

## Problem 2: Group by Property

```java
// Group numbers by their parity
Map<Boolean, List<Integer>> parityGroups = new HashMap<>();
for (int x : arr) {
    parityGroups.computeIfAbsent(x % 2 == 0, k -> new ArrayList<>()).add(x);
}
// parityGroups.get(true) = evens, parityGroups.get(false) = odds
```

## Problem 3: Partition Labels

Each character must appear in at most one partition:
```java
List<Integer> partitionLabels(String s) {
    Map<Character, Integer> last = new HashMap<>();
    for (int i = 0; i < s.length(); i++) {
        last.put(s.charAt(i), i);
    }
    
    List<Integer> result = new ArrayList<>();
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        end = Math.max(end, last.get(s.charAt(i)));
        if (i == end) {
            result.add(end - start + 1);
            start = i + 1;
        }
    }
    return result;
}
```
O(n) time, O(1) space (since alphabet is 26 chars).

## Problem 4: Group Shifted Strings

Group strings that can be shifted circularly:
```java
String getShiftKey(String s) {
    StringBuilder sb = new StringBuilder();
    for (int i = 1; i < s.length(); i++) {
        int diff = s.charAt(i) - s.charAt(i-1);
        if (diff < 0) diff += 26;
        sb.append(diff).append(',');
    }
    return sb.toString();
}
```

## Problem 5: Group Products by Price Range

```java
Map<String, List<Product>> groupByPriceRange(List<Product> products) {
    Map<String, List<Product>> groups = new HashMap<>();
    for (Product p : products) {
        String range;
        if (p.price < 100) range = "budget";
        else if (p.price < 500) range = "mid";
        else range = "premium";
        groups.computeIfAbsent(range, k -> new ArrayList<>()).add(p);
    }
    return groups;
}
```

## When to Use Grouping

- "Group by X" → HashMap<X, List<Y>>
- "Categorize items" → computeIfAbsent
- "Partition" → find boundary condition
- "Classify by property" → custom key function
