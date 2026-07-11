# Top K Elements Patterns

## Master Pattern

For **Top K largest/smallest**, use a heap of size K:
- **Top K largest** → min-heap (keep K largest in heap, smallest among them at top)
- **Top K smallest** → max-heap (keep K smallest in heap, largest among them at top)
- **Top K frequent** → HashMap for frequency + min-heap of size K

## Pattern Template

```java
// Top K largest
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
for (int x : nums) {
    minHeap.offer(x);
    if (minHeap.size() > k) minHeap.poll();
}
// heap contains K largest elements
```

## Problem 1: Kth Largest Element in Array

```java
int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int n : nums) {
        minHeap.offer(n);
        if (minHeap.size() > k) minHeap.poll();
    }
    return minHeap.peek();
}
```

## Problem 2: Top K Frequent Elements

```java
List<Integer> topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.merge(n, 1, Integer::sum);
    
    // Min-heap by frequency
    PriorityQueue<Map.Entry<Integer, Integer>> pq = 
        new PriorityQueue<>(Map.Entry.comparingByValue());
    
    for (Map.Entry<Integer,Integer> e : freq.entrySet()) {
        pq.offer(e);
        if (pq.size() > k) pq.poll();
    }
    
    return pq.stream().map(Map.Entry::getKey).collect(Collectors.toList());
}
```

## Problem 3: Top K Frequent Words

```java
List<String> topKFrequent(String[] words, int k) {
    Map<String, Integer> freq = new HashMap<>();
    for (String w : words) freq.merge(w, 1, Integer::sum);
    
    // Tie-break: if same frequency, lexicographically larger first (for removal)
    PriorityQueue<Map.Entry<String, Integer>> pq = new PriorityQueue<>(
        (a, b) -> a.getValue().equals(b.getValue()) 
            ? b.getKey().compareTo(a.getKey()) 
            : a.getValue() - b.getValue()
    );
    
    for (Map.Entry<String, Integer> e : freq.entrySet()) {
        pq.offer(e);
        if (pq.size() > k) pq.poll();
    }
    
    List<String> result = new ArrayList<>();
    while (!pq.isEmpty()) result.add(pq.poll().getKey());
    Collections.reverse(result);
    return result;
}
```

## Problem 4: K Closest Points to Origin

```java
int[][] kClosest(int[][] points, int k) {
    // Max-heap: keep K closest, remove farthest
    PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1])
    );
    
    for (int[] p : points) {
        maxHeap.offer(p);
        if (maxHeap.size() > k) maxHeap.poll();
    }
    
    return maxHeap.toArray(new int[0][0]);
}
```

## Problem 5: Sort Characters by Frequency

```java
String frequencySort(String s) {
    Map<Character, Integer> freq = new HashMap<>();
    for (char c : s.toCharArray()) freq.merge(c, 1, Integer::sum);
    
    PriorityQueue<Character> maxHeap = new PriorityQueue<>(
        (a, b) -> freq.get(b) - freq.get(a)
    );
    maxHeap.addAll(freq.keySet());
    
    StringBuilder sb = new StringBuilder();
    while (!maxHeap.isEmpty()) {
        char c = maxHeap.poll();
        sb.append(String.valueOf(c).repeat(freq.get(c)));
    }
    return sb.toString();
}
```
