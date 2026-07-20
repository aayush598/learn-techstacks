# Advanced Sliding Window Tricks

## 1. Window with Hash Map for Character Counting

```python
from collections import Counter

def max_freq_in_window(s, k):
    """Max frequency of any character in any window of size k."""
    freq = Counter()
    max_f = 0
    
    for i in range(len(s)):
        freq[s[i]] += 1
        
        if i >= k:
            freq[s[i - k]] -= 1
        
        max_f = max(max_f, max(freq.values()))
    
    return max_f
# Time: O(n * 26) = O(n)
```

---

## 2. Two Pointer Variant of Sliding Window

```python
def max_distinct_subarray(arr, k):
    """Longest subarray with at most k distinct elements."""
    from collections import defaultdict
    freq = defaultdict(int)
    left = 0
    max_len = 0
    
    for right in range(len(arr)):
        freq[arr[right]] += 1
        
        while len(freq) > k:
            freq[arr[left]] -= 1
            if freq[arr[left]] == 0:
                del freq[arr[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
# The "two pointer" aspect: left and right both move forward
# but right explores while left only moves to restore validity
```

---

## 3. Sliding Window with Monotonic Deque

```python
from collections import deque

def max_in_sliding_window(nums, k):
    """Maximum of each window of size k - O(n)."""
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (they'll never be max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
# deque maintains indices of potential maximums in decreasing order
# dq[0] is always the max of current window
# Time: O(n), Space: O(k)

def min_in_sliding_window(nums, k):
    """Minimum of each window of size k."""
    dq = deque()
    result = []
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] > nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

## 4. Sliding Window Median (LeetCode 480)

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (invert values)
        self.hi = []  # min-heap
    
    def add(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    
    def remove(self, num):
        if num <= -self.lo[0]:
            self.lo.remove(-num)
            heapq.heapify(self.lo)
        else:
            self.hi.remove(num)
            heapq.heapify(self.hi)
        
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
        elif len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
    
    def median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0

def median_sliding_window(nums, k):
    finder = MedianFinder()
    result = []
    
    for i in range(len(nums)):
        finder.add(nums[i])
        
        if i >= k:
            finder.remove(nums[i - k])
        
        if i >= k - 1:
            result.append(finder.median())
    
    return result
# Time: O(n log k), Space: O(k)
```

---

## 5. Count Subarrays Matching Pattern

```python
def count_subarrays_with_condition(arr, k):
    """Count subarrays where max - min <= k."""
    from collections import deque
    
    max_dq = deque()  # decreasing - front is max
    min_dq = deque()  # increasing - front is min
    left = 0
    count = 0
    
    for right in range(len(arr)):
        # Maintain max deque
        while max_dq and arr[max_dq[-1]] <= arr[right]:
            max_dq.pop()
        max_dq.append(right)
        
        # Maintain min deque
        while min_dq and arr[min_dq[-1]] >= arr[right]:
            min_dq.pop()
        min_dq.append(right)
        
        # Shrink if condition violated
        while arr[max_dq[0]] - arr[min_dq[0]] > k:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()
        
        count += right - left + 1
    
    return count
# Time: O(n), Space: O(k)
```

---

## 6. Longest Subarray with Absolute Difference <= Limit (LeetCode 1438)

```python
from collections import deque

def longest_subarray(nums, limit):
    max_dq = deque()
    min_dq = deque()
    left = 0
    max_len = 0
    
    for right in range(len(nums)):
        while max_dq and nums[max_dq[-1]] < nums[right]:
            max_dq.pop()
        max_dq.append(right)
        
        while min_dq and nums[min_dq[-1]] > nums[right]:
            min_dq.pop()
        min_dq.append(right)
        
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
# Time: O(n), Space: O(n)
```

---

## 7. Subarrays with At Most K Odd Numbers

```python
def subarrays_with_at_most_k_odd(arr, k):
    """Count subarrays with at most k odd numbers."""
    left = 0
    count = 0
    odd_count = 0
    
    for right in range(len(arr)):
        if arr[right] % 2 == 1:
            odd_count += 1
        
        while odd_count > k:
            if arr[left] % 2 == 1:
                odd_count -= 1
            left += 1
        
        count += right - left + 1
    
    return count

# For exactly k odds:
def subarrays_with_exactly_k_odd(arr, k):
    return subarrays_with_at_most_k_odd(arr, k) - subarrays_with_at_most_k_odd(arr, k - 1)
# Time: O(n), Space: O(1)
```

---

## 8. Maximum Points from Cards (LeetCode 1423)

**Problem:** Pick k cards from either end of array, maximize sum.

```python
def max_score(card_points, k):
    n = len(card_points)
    # Pick from left + right = total - (window of n-k from middle)
    total = sum(card_points)
    
    if k == n:
        return total
    
    # Minimize the subarray of size n-k we DON'T pick
    window_size = n - k
    window_sum = sum(card_points[:window_size])
    min_window = window_sum
    
    for i in range(window_size, n):
        window_sum += card_points[i] - card_points[i - window_size]
        min_window = min(min_window, window_sum)
    
    return total - min_window
# Time: O(n), Space: O(1)
# Key insight: picking from ends = leaving a contiguous middle subarray
```

---

## Summary: Which Trick When

| Trick | Use When |
|-------|----------|
| Hash map counting | Character/element frequency in window |
| Monotonic deque | Min/max queries in sliding window |
| Two heaps | Median in sliding window |
| at_most(k) - at_most(k-1) | Exactly k condition |
| Total - min_subarray | Picking from both ends |
| Dual deques (max+min) | Range constraints (max-min <= limit) |
