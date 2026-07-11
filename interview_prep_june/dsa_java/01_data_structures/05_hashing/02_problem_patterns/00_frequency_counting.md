# Frequency Counting Patterns

## The Master Pattern

```java
Map<KeyType, Integer> freq = new HashMap<>();
for (Element e : collection) {
    freq.put(e.key, freq.getOrDefault(e.key, 0) + 1);
}
```

Or with `merge`:
```java
freq.merge(e.key, 1, Integer::sum);
```

## Problem 1: Character Frequency

```java
// Count character occurrences in string
String s = "hello world";
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
}
```

## Problem 2: Word Frequency

```java
String[] words = "the quick brown fox jumps over the lazy dog".split(" ");
Map<String, Integer> freq = new HashMap<>();
for (String w : words) freq.merge(w.toLowerCase(), 1, Integer::sum);
```

## Problem 3: Most Frequent Element

```java
int mostFrequent(int[] arr) {
    Map<Integer, Integer> freq = new HashMap<>();
    int maxCount = 0, result = arr[0];
    for (int x : arr) {
        int count = freq.merge(x, 1, Integer::sum);
        if (count > maxCount) { maxCount = count; result = x; }
    }
    return result;
}
```

## Problem 4: Top K Frequent Elements

```java
List<Integer> topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.merge(n, 1, Integer::sum);
    
    // Min-heap of (frequency, element)
    PriorityQueue<Map.Entry<Integer, Integer>> pq = 
        new PriorityQueue<>(Map.Entry.comparingByValue());
    
    for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
        pq.offer(e);
        if (pq.size() > k) pq.poll();
    }
    
    return pq.stream().map(Map.Entry::getKey).collect(Collectors.toList());
}
```

## Problem 5: Frequency Sort (Sort by Frequency)

```java
String frequencySort(String s) {
    Map<Character, Integer> freq = new HashMap<>();
    for (char c : s.toCharArray()) freq.merge(c, 1, Integer::sum);
    
    PriorityQueue<Character> pq = new PriorityQueue<>(
        (a, b) -> freq.get(b) - freq.get(a)
    );
    pq.addAll(freq.keySet());
    
    StringBuilder sb = new StringBuilder();
    while (!pq.isEmpty()) {
        char c = pq.poll();
        sb.append(String.valueOf(c).repeat(freq.get(c)));
    }
    return sb.toString();
}
```

## Frequency Array (When Key Space is Small)

For characters (26 lowercase, 128 ASCII) or small integers:
```java
int[] freq = new int[26];
for (char c : s.toCharArray()) freq[c - 'a']++;
```
This is faster than HashMap for small key spaces.
