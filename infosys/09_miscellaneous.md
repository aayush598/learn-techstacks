# Miscellaneous Important Problems

## Problem 1: Largest Product of Set S (Wilson's Theorem)
**Difficulty: Medium | Marks: 30**

Asked in Infosys SP/DSE exam - Find largest set S from [1, N-1] whose product ≡ 1 (mod N).

```python
def largest_set_product_mod(N):
    # Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p
    # For prime N, all numbers 1..N-2 work -> answer = N-2
    # For N=4, answer = 1 (just {1})
    # For composite N, answer = max count where product ≡ 1 mod N
    if N == 1:
        return 0
    if N == 4:
        return 1

    # Check if N is prime
    def is_prime(n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    if is_prime(N):
        # For prime N, product of all 1..N-1 ≡ -1 mod N
        # Excluding N-1 gives product ≡ 1 mod N
        return N - 2
    else:
        # For composite N, count numbers coprime to N
        # Subtract numbers that have gcd != 1 with N
        count = 0
        for i in range(1, N):
            from math import gcd
            if gcd(i, N) == 1:
                count += 1
        if count % 2 == 0:
            return count
        else:
            # If totient(N) is odd, exclude one number
            return count - 1

print(largest_set_product_mod(7))
print(largest_set_product_mod(5))
print(largest_set_product_mod(4))
```

---

## Problem 2: Bucket Ball Probability
**Difficulty: Hard | Marks: 50**

Asked in Infosys SP/DSE exam - N buckets with K colored balls, transfer probability.

```python
def bucket_ball_probability(N, K, buckets):
    # buckets: list of lists, each with K counts
    totals = [sum(row) for row in buckets]
    dp = [0] * K
    for j in range(K):
        dp[j] = buckets[0][j] / totals[0]
    for i in range(1, N):
        new_dp = [0] * K
        for j in range(K):
            new_dp[j] = dp[j] * (buckets[i][j] + 1) / (totals[i] + 1) + \
                        (1 - dp[j]) * buckets[i][j] / (totals[i] + 1)
        dp = new_dp
    return dp

# Sample: 2 buckets, 2 colors
N, K = 2, 2
buckets = [
    [0, 1],  # bucket 0: 0 color1, 1 color2
    [1, 1]   # bucket 1: 1 color1, 1 color2
]
result = bucket_ball_probability(N, K, buckets)
print(' '.join(f'{p:.6f}' for p in result))
```

---

## Problem 3: Implement LRU Cache
**Difficulty: Medium | Marks: 30**

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))
cache.put(3, 3)
print(cache.get(2))
```

---

## Problem 4: Implement Min Stack
**Difficulty: Easy-Medium | Marks: 20**

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        if self.stack:
            val = self.stack.pop()
            if val == self.min_stack[-1]:
                self.min_stack.pop()

    def top(self):
        return self.stack[-1] if self.stack else None

    def get_min(self):
        return self.min_stack[-1] if self.min_stack else None
```

---

## Problem 5: Find Median from Data Stream
**Difficulty: Hard | Marks: 50**

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max heap (store negatives)
        self.large = []  # min heap

    def add_num(self, num):
        heapq.heappush(self.small, -num)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0

mf = MedianFinder()
mf.add_num(1)
mf.add_num(2)
print(mf.find_median())
mf.add_num(3)
print(mf.find_median())
```

---

## Problem 6: Largest Rectangle in Histogram
**Difficulty: Hard | Marks: 50**

```python
def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    heights.append(0)
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

heights = [2, 1, 5, 6, 2, 3]
print(largest_rectangle_area(heights))
```

---

## Problem 7: Sliding Window Maximum
**Difficulty: Hard | Marks: 50**

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    result = []
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(max_sliding_window(nums, k))
```

---

## Problem 8: Time Needed to Inform All Employees
**Difficulty: Medium | Marks: 30**

```python
from collections import defaultdict

def num_of_minutes(n, head_id, manager, inform_time):
    tree = defaultdict(list)
    for emp, mgr in enumerate(manager):
        if mgr != -1:
            tree[mgr].append(emp)

    def dfs(emp):
        if emp not in tree:
            return 0
        max_time = 0
        for sub in tree[emp]:
            max_time = max(max_time, dfs(sub))
        return max_time + inform_time[emp]

    return dfs(head_id)

n = 6
head_id = 2
manager = [2, 2, -1, 2, 2, 2]
inform_time = [0, 0, 1, 0, 0, 0]
print(num_of_minutes(n, head_id, manager, inform_time))
```

---

## Problem 9: Network Delay Time
**Difficulty: Medium | Marks: 30**

```python
import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, w in graph[node]:
            new_dist = d + w
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    max_dist = max(dist.values())
    return max_dist if max_dist != float('inf') else -1

times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
n = 4
k = 2
print(network_delay_time(times, n, k))
```

---

## Problem 10: Evaluate Division (Graph + Union-Find)
**Difficulty: Medium | Marks: 30**

```python
from collections import defaultdict

def calc_equation(equations, values, queries):
    graph = defaultdict(list)
    for (a, b), val in zip(equations, values):
        graph[a].append((b, val))
        graph[b].append((a, 1 / val))

    def dfs(start, end, visited):
        if start not in graph or end not in graph:
            return -1.0
        if start == end:
            return 1.0
        visited.add(start)
        for neighbor, val in graph[start]:
            if neighbor not in visited:
                result = dfs(neighbor, end, visited)
                if result != -1.0:
                    return val * result
        return -1.0

    results = []
    for a, b in queries:
        results.append(dfs(a, b, set()))
    return results

equations = [["a", "b"], ["b", "c"]]
values = [2.0, 3.0]
queries = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
print(calc_equation(equations, values, queries))
```

---

## Problem 11: Find the Celebrity
**Difficulty: Medium | Marks: 30**

```python
def find_celebrity(n, knows):
    candidate = 0
    for i in range(1, n):
        if knows(candidate, i):
            candidate = i
    for i in range(n):
        if i != candidate:
            if knows(candidate, i) or not knows(i, candidate):
                return -1
    return candidate

# knows(a, b) returns True if a knows b (API function)
```

---

## Problem 12: Race Car
**Difficulty: Hard | Marks: 50**

```python
from collections import deque

def race_car(target):
    queue = deque([(0, 1, 0)])  # position, speed, steps
    visited = {(0, 1)}
    while queue:
        pos, speed, steps = queue.popleft()
        if pos == target:
            return steps
        # accelerate
        a_pos, a_speed = pos + speed, speed * 2
        if (a_pos, a_speed) not in visited and abs(a_pos) < 2 * target:
            visited.add((a_pos, a_speed))
            queue.append((a_pos, a_speed, steps + 1))
        # reverse
        r_speed = -1 if speed > 0 else 1
        if (pos, r_speed) not in visited:
            visited.add((pos, r_speed))
            queue.append((pos, r_speed, steps + 1))
    return -1

print(race_car(3))
print(race_car(6))
```

---

## Problem 13: Basic Calculator II
**Difficulty: Medium | Marks: 30**

```python
def calculate(s):
    stack = []
    num = 0
    op = '+'
    s = s.replace(' ', '')
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if not ch.isdigit() or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            elif op == '/':
                stack.append(int(stack.pop() / num))
            op = ch
            num = 0
    return sum(stack)

print(calculate("3+2*2"))
print(calculate(" 3/2 "))
print(calculate(" 3+5 / 2 "))
```

---

## Problem 14: Top K Frequent Elements
**Difficulty: Medium | Marks: 30**

```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):
    counter = Counter(nums)
    return heapq.nlargest(k, counter.keys(), key=counter.get)

nums = [1, 1, 1, 2, 2, 3]
k = 2
print(top_k_frequent(nums, k))
```

---

## Problem 15: Task Scheduler
**Difficulty: Medium | Marks: 30**

```python
from collections import Counter

def least_interval(tasks, n):
    counter = Counter(tasks)
    max_freq = max(counter.values())
    max_count = sum(1 for v in counter.values() if v == max_freq)
    intervals = (max_freq - 1) * (n + 1) + max_count
    return max(intervals, len(tasks))

tasks = ["A", "A", "A", "B", "B", "B"]
n = 2
print(least_interval(tasks, n))
```

---

## Problem 16: Design Twitter (System Design Problem)
**Difficulty: Hard | Marks: 50**

```python
import heapq
from collections import defaultdict
from itertools import count

class Twitter:
    def __init__(self):
        self.tweets = defaultdict(list)
        self.following = defaultdict(set)
        self.timestamp = count(step=-1)

    def post_tweet(self, userId, tweetId):
        self.tweets[userId].append((next(self.timestamp), tweetId))

    def get_news_feed(self, userId):
        users = self.following[userId] | {userId}
        heap = []
        for user in users:
            for tweet in self.tweets[user][-10:]:
                heapq.heappush(heap, tweet)
                if len(heap) > 10:
                    heapq.heappop(heap)
        return [tid for _, tid in sorted(heap, key=lambda x: x[0])]

    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

---

## Problem 17: Number of Subarrays with Bounded Maximum
**Difficulty: Medium | Marks: 30**

```python
def num_subarray_bounded_max(nums, left, right):
    def count_subs_bound(limit):
        count = curr = 0
        for num in nums:
            if num <= limit:
                curr += 1
                count += curr
            else:
                curr = 0
        return count
    return count_subs_bound(right) - count_subs_bound(left - 1)

nums = [2, 1, 4, 3]
left, right = 2, 3
print(num_subarray_bounded_max(nums, left, right))
```

---

## Problem 18: Sum of Subarray Minimums
**Difficulty: Hard | Marks: 50**

```python
def sum_subarray_mins(arr):
    MOD = 10**9 + 7
    n = len(arr)
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    result = 0
    for i in range(n):
        result = (result + arr[i] * (i - left[i]) * (right[i] - i)) % MOD
    return result

arr = [3, 1, 2, 4]
print(sum_subarray_mins(arr))
```

---

## Problem 19: Design HashMap
**Difficulty: Easy-Medium | Marks: 20**

```python
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return key % self.size

    def put(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return -1

    def remove(self, key):
        idx = self._hash(key)
        self.buckets[idx] = [(k, v) for k, v in self.buckets[idx] if k != key]
```

---

## Problem 20: Maximum Frequency Stack
**Difficulty: Hard | Marks: 50**

```python
from collections import defaultdict

class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)
        self.group = defaultdict(list)
        self.max_freq = 0

    def push(self, val):
        self.freq[val] += 1
        f = self.freq[val]
        self.max_freq = max(self.max_freq, f)
        self.group[f].append(val)

    def pop(self):
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val

fs = FreqStack()
fs.push(5)
fs.push(7)
fs.push(5)
fs.push(7)
fs.push(4)
fs.push(5)
print(fs.pop())
print(fs.pop())
print(fs.pop())
print(fs.pop())
```
