# 15 Must-Know DSA Patterns

## 1. Sliding Window

**When to use:** Problems involving contiguous subarrays/substrings, especially when asked for longest/shortest/optimal subarray that satisfies a condition.

**Template:**
```java
// Variable size window
int left = 0;
for (int right = 0; right < n; right++) {
    // Add arr[right] to window
    while (window is invalid) {
        // Remove arr[left] from window
        left++;
    }
    // Update answer (window [left, right] is valid)
}

// Fixed size window (size k)
for (int right = 0; right < n; right++) {
    // Add arr[right] to window
    if (right >= k - 1) {
        // Record answer for window [right-k+1, right]
        // Remove arr[right-k+1] from window
    }
}
```

**Example:** Longest substring without repeating characters
**Variations:** Min window substring, max sum subarray of size k, longest substring with at most k distinct chars, max consecutive ones III

---

## 2. Two Pointers / Iterators

**When to use:** Sorted arrays/pairs, palindrome checking, merging sorted arrays, removing duplicates.

**Template:**
```java
// Opposite ends (pair sum, palindrome)
int left = 0, right = n - 1;
while (left < right) {
    // Process arr[left] and arr[right]
    if (condition) left++;
    else right--;
}

// Same direction (remove duplicates)
int slow = 0;
for (int fast = 0; fast < n; fast++) {
    if (arr[fast] != arr[slow]) {
        slow++;
        arr[slow] = arr[fast];
    }
}
```

**Example:** Two Sum II (sorted array), Valid Palindrome
**Variations:** 3Sum, container with most water, remove duplicates, trapping rain water

---

## 3. Fast & Slow Pointers

**When to use:** Cycle detection in linked lists, finding middle of linked list, palindrome linked list.

**Template:**
```java
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow == fast) { // Cycle detected
        // Find cycle start if needed
    }
}
```

**Example:** Linked list cycle, find middle of linked list
**Variations:** Find duplicate number, happy number, palindrome linked list

---

## 4. Merge Intervals

**When to use:** Problems with intervals/ranges, meeting schedules, overlapping intervals.

**Template:**
```java
Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
List<int[]> merged = new ArrayList<>();
int[] current = intervals[0];
for (int[] next : intervals) {
    if (current[1] >= next[0]) { // Overlap
        current[1] = Math.max(current[1], next[1]);
    } else {
        merged.add(current);
        current = next;
    }
}
merged.add(current);
```

**Example:** Merge intervals, insert interval
**Variations:** Meeting rooms I/II, interval list intersections, non-overlapping intervals

---

## 5. Cyclic Sort

**When to use:** Problems with numbers in range [1, n] where you need to find missing/duplicate numbers.

**Template:**
```java
int i = 0;
while (i < n) {
    int correctIdx = arr[i] - 1; // For [1,n] range
    if (arr[i] != arr[correctIdx]) {
        swap(arr, i, correctIdx);
    } else {
        i++;
    }
}
// Now arr[i] should be at index i+1
// Find missing/duplicate by scanning
```

**Example:** Find missing number, find all duplicates
**Variations:** First missing positive, find all numbers disappeared, find duplicate number

---

## 6. In-place Reversal of Linked List

**When to use:** Reversing linked list, checking palindrome, reordering list.

**Template:**
```java
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode next = curr.next;
    curr.next = prev;
    prev = curr;
    curr = next;
}
return prev; // New head
```

**Example:** Reverse linked list, reverse nodes in k-group
**Variations:** Reverse between positions, palindrome linked list, reorder list

---

## 7. Tree BFS

**When to use:** Level-order traversal, shortest path in unweighted tree/graph, views of tree.

**Template:**
```java
Queue<TreeNode> queue = new LinkedList<>();
queue.offer(root);
while (!queue.isEmpty()) {
    int size = queue.size();
    for (int i = 0; i < size; i++) {
        TreeNode node = queue.poll();
        // Process node
        if (node.left != null) queue.offer(node.left);
        if (node.right != null) queue.offer(node.right);
    }
    // Level processing complete
}
```

**Example:** Binary tree level order traversal, right side view
**Variations:** Zigzag traversal, min depth, connect level order siblings, average of levels

---

## 8. Tree DFS

**When to use:** Path sum problems, tree property computation, tree serialization.

**Template:**
```java
// Recursive
void dfs(TreeNode node, List<Integer> result) {
    if (node == null) return;
    // Pre-order: process node, dfs(left), dfs(right)
    dfs(node.left, result);
    // In-order: dfs(left), process node, dfs(right)
    dfs(node.right, result);
    // Post-order: dfs(left), dfs(right), process node
}
```

**Example:** Binary tree inorder traversal, path sum, max depth
**Variations:** Validate BST, serialize/deserialize, diameter of tree, LCA

---

## 9. Two Heaps (Min/Max)

**When to use:** Finding median of stream, scheduling with priorities, sliding window median.

**Template:**
```java
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a,b)->b-a); // left half
PriorityQueue<Integer> minHeap = new PriorityQueue<>(); // right half

void addNum(int num) {
    if (maxHeap.isEmpty() || num <= maxHeap.peek()) {
        maxHeap.offer(num);
    } else {
        minHeap.offer(num);
    }
    // Balance: maxHeap size >= minHeap size
    if (maxHeap.size() < minHeap.size()) maxHeap.offer(minHeap.poll());
    if (maxHeap.size() - minHeap.size() > 1) minHeap.offer(maxHeap.poll());
}

double findMedian() {
    if (maxHeap.size() == minHeap.size())
        return (maxHeap.peek() + minHeap.peek()) / 2.0;
    return maxHeap.peek();
}
```

**Example:** Find median from data stream
**Variations:** Sliding window median, IPO (capital), schedule tasks

---

## 10. Subsets (Backtracking)

**When to use:** Generating all subsets/permutations/combinations, constraint satisfaction.

**Template:**
```java
List<List<Integer>> result = new ArrayList<>();
void backtrack(int[] nums, int start, List<Integer> current) {
    result.add(new ArrayList<>(current));
    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current);
        current.remove(current.size() - 1);
    }
}
```

**Example:** Subsets, permutations, combination sum
**Variations:** Generate parentheses, letter combinations of phone number, N-Queens, Sudoku solver

---

## 11. Modified Binary Search (Binary Search on Answer)

**When to use:** Search space [min, max] where monotonic condition exists. Finding minimized maximum or maximized minimum.

**Template:**
```java
boolean feasible(int mid, int[] arr, int target) { /* condition */ }

int left = min, right = max;
while (left < right) {
    int mid = left + (right - left) / 2;
    if (feasible(mid, arr, target)) {
        right = mid; // or left = mid + 1 depending on direction
    } else {
        left = mid + 1; // or right = mid
    }
}
return left;
```

**Example:** Koko eating bananas, split array largest sum
**Variations:** Aggressive cows, book allocation, smallest divisor, min time to repair

---

## 12. Top K Elements (Heap)

**When to use:** Finding K largest/smallest/frequent elements.

**Template:**
```java
// K smallest: use max heap
PriorityQueue<Integer> pq = new PriorityQueue<>((a,b)->b-a);
for (int num : nums) {
    pq.offer(num);
    if (pq.size() > k) pq.poll();
}
// pq now contains K smallest elements

// K largest: use min heap
PriorityQueue<Integer> pq = new PriorityQueue<>();
for (int num : nums) {
    pq.offer(num);
    if (pq.size() > k) pq.poll();
}
// pq now contains K largest elements
```

**Example:** Kth largest element, top K frequent elements
**Variations:** K closest points to origin, sort characters by frequency, top K frequent words

---

## 13. K-Way Merge

**When to use:** Merging K sorted lists/arrays.

**Template:**
```java
PriorityQueue<ListNode> pq = new PriorityQueue<>((a,b)->a.val-b.val);
for (ListNode list : lists) {
    if (list != null) pq.offer(list);
}
ListNode dummy = new ListNode(0), curr = dummy;
while (!pq.isEmpty()) {
    ListNode node = pq.poll();
    curr.next = node;
    curr = curr.next;
    if (node.next != null) pq.offer(node.next);
}
return dummy.next;
```

**Example:** Merge K sorted lists
**Variations:** Kth smallest in sorted matrix, smallest range covering K lists, merge K sorted arrays

---

## 14. 0/1 Knapsack (DP)

**When to use:** Subset choosing with capacity constraint, maximize/minimize some value.

**Template:**
```java
// 0/1 Knapsack: dp[i][w] = max value with first i items and capacity w
int[][] dp = new int[n + 1][capacity + 1];
for (int i = 1; i <= n; i++) {
    for (int w = 1; w <= capacity; w++) {
        if (weights[i-1] <= w) {
            dp[i][w] = Math.max(dp[i-1][w],
                values[i-1] + dp[i-1][w - weights[i-1]]);
        } else {
            dp[i][w] = dp[i-1][w];
        }
    }
}

// Optimized 1D space
int[] dp = new int[capacity + 1];
for (int i = 0; i < n; i++) {
    for (int w = capacity; w >= weights[i]; w--) {
        dp[w] = Math.max(dp[w], values[i] + dp[w - weights[i]]);
    }
}
```

**Example:** 0/1 Knapsack, subset sum, partition equal subset sum
**Variations:** Target sum, ones and zeros, last stone weight II, coin change II (unbounded)

---

## 15. Topological Sort (Graph)

**When to use:** Dependency resolution, ordering tasks with prerequisites, detecting cycles in directed graph.

**Template:**
```java
// Kahn's algorithm (BFS)
int[] inDegree = new int[n];
List<Integer>[] graph = new List[n];
for (int[] edge : edges) {
    graph[edge[0]].add(edge[1]);
    inDegree[edge[1]]++;
}
Queue<Integer> queue = new LinkedList<>();
for (int i = 0; i < n; i++)
    if (inDegree[i] == 0) queue.offer(i);

List<Integer> order = new ArrayList<>();
while (!queue.isEmpty()) {
    int u = queue.poll();
    order.add(u);
    for (int v : graph[u]) {
        if (--inDegree[v] == 0) queue.offer(v);
    }
}
// If order.size() != n -> cycle exists
```

**Example:** Course schedule, course schedule II
**Variations:** Alien dictionary, sequence reconstruction, parallel courses, minimum height trees
