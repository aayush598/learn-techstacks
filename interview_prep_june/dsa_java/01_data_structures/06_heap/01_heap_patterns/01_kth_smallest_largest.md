# Kth Smallest/Largest Patterns

## Quick Reference

| Problem | Data Structure | Heap Type | Size |
|---------|---------------|-----------|------|
| Kth Smallest | Max-Heap | Keep K smallest, largest at top | K |
| Kth Largest | Min-Heap | Keep K largest, smallest at top | K |

## Kth Smallest (Max-Heap)

```java
int findKthSmallest(int[] nums, int k) {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    for (int n : nums) {
        maxHeap.offer(n);
        if (maxHeap.size() > k) maxHeap.poll();  // remove largest
    }
    return maxHeap.peek();
}
```

## Kth Largest (Min-Heap)

```java
int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int n : nums) {
        minHeap.offer(n);
        if (minHeap.size() > k) minHeap.poll();  // remove smallest
    }
    return minHeap.peek();
}
```

## Kth Smallest in Sorted Matrix

```java
int kthSmallest(int[][] matrix, int k) {
    int n = matrix.length;
    PriorityQueue<int[]> minHeap = new PriorityQueue<>(
        (a, b) -> a[0] - b[0]
    );
    
    // Add first element of each row
    for (int i = 0; i < n; i++) minHeap.offer(new int[]{matrix[i][0], i, 0});
    
    while (k > 1) {
        int[] curr = minHeap.poll();
        int row = curr[1], col = curr[2];
        if (col + 1 < n) {
            minHeap.offer(new int[]{matrix[row][col+1], row, col+1});
        }
        k--;
    }
    return minHeap.poll()[0];
}
```

## QuickSelect (Alternative for Arrays)

```java
int quickSelect(int[] nums, int k) {
    // kth smallest (convert to 0-indexed)
    return select(nums, 0, nums.length - 1, k - 1);
}

int select(int[] nums, int left, int right, int k) {
    if (left == right) return nums[left];
    
    int pivotIndex = partition(nums, left, right);
    if (k == pivotIndex) return nums[k];
    else if (k < pivotIndex) return select(nums, left, pivotIndex - 1, k);
    else return select(nums, pivotIndex + 1, right, k);
}

int partition(int[] nums, int left, int right) {
    int pivot = nums[right];
    int i = left;
    for (int j = left; j < right; j++) {
        if (nums[j] <= pivot) { swap(nums, i, j); i++; }
    }
    swap(nums, i, right);
    return i;
}
```

| Approach | Time | Space | When to Use |
|----------|------|-------|-------------|
| Heap | O(n log k) | O(k) | Stream/online data |
| QuickSelect | O(n) avg, O(n²) worst | O(1) | In-place array |
| Sorting | O(n log n) | O(1) | Single query |
