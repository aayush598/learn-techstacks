# Median in Data Stream

## Problem: Find Median from Data Stream

**Pattern: Two Heaps**
- **Max-heap** (left half): contains smaller numbers
- **Min-heap** (right half): contains larger numbers
- Invariant: maxHeap.size() >= minHeap.size() (by at most 1)
- Invariant: maxHeap.peek() <= minHeap.peek()

```java
class MedianFinder {
    private PriorityQueue<Integer> maxHeap;  // left half (smaller numbers)
    private PriorityQueue<Integer> minHeap;  // right half (larger numbers)
    
    MedianFinder() {
        maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        minHeap = new PriorityQueue<>();
    }
    
    void addNum(int num) {
        // Step 1: Add to maxHeap (left side)
        maxHeap.offer(num);
        
        // Step 2: Ensure maxHeap's max <= minHeap's min
        if (!minHeap.isEmpty() && maxHeap.peek() > minHeap.peek()) {
            minHeap.offer(maxHeap.poll());
        }
        
        // Step 3: Rebalance sizes (maxHeap can have 1 more at most)
        if (maxHeap.size() > minHeap.size() + 1) {
            minHeap.offer(maxHeap.poll());
        }
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.offer(minHeap.poll());
        }
    }
    
    double findMedian() {
        if (maxHeap.size() == minHeap.size()) {
            return (maxHeap.peek() + minHeap.peek()) / 2.0;
        }
        return maxHeap.peek();  // maxHeap has the extra element
    }
}
```

**Simpler version** (add to maxHeap, then fix):

```java
void addNum(int num) {
    maxHeap.offer(num);
    minHeap.offer(maxHeap.poll());
    
    if (maxHeap.size() < minHeap.size()) {
        maxHeap.offer(minHeap.poll());
    }
}
```

## Complexity

- addNum: O(log n)
- findMedian: O(1)
- Space: O(n)

## Follow-up: Sliding Window Median

Maintain median of current window as it slides:
- Use two TreeSets (or two heaps with lazy removal)
- Or use two heaps + a HashMap for lazy deletion

```java
// Simplified approach using two heaps with lazy deletion
class SlidingWindowMedian {
    private PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    private PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    private Map<Integer, Integer> pendingRemovals = new HashMap<>();
    
    double[] medianSlidingWindow(int[] nums, int k) {
        double[] result = new double[nums.length - k + 1];
        
        for (int i = 0; i < nums.length; i++) {
            addNum(nums[i]);
            if (i >= k - 1) {
                result[i - k + 1] = findMedian();
                removeNum(nums[i - k + 1]);
            }
        }
        return result;
    }
    
    private void addNum(int num) { /* same as MedianFinder */ }
    private void removeNum(int num) { /* lazy removal */ }
    private double findMedian() { /* same as MedianFinder */ }
}
```
