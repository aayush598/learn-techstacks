# After Solution: Code Review and Follow-Up Guide

What happens after you solve the coding problem — code review, optimization discussion, and follow-up scenarios.

---

## 1. Code Review Checklist

Run through this before declaring "I'm done."

### Variable Names
```java
// BAD: unclear names
int d = arr[j] - arr[i];
int[] dp = new int[n];
boolean f = false;

// GOOD: descriptive names
int distance = arr[right] - arr[left];
int[] minCuts = new int[n];
boolean hasPath = false;
```

### Magic Numbers
```java
// BAD
if (arr.length < 3) return -1;
while (count < 26) { ... }

// GOOD
private static final int MIN_ELEMENTS = 3;
private static final int ALPHABET_SIZE = 26;
if (arr.length < MIN_ELEMENTS) return -1;
while (count < ALPHABET_SIZE) { ... }
```

### DRY Violations
```java
// BAD: duplicated logic
public int minInLeft(int[] arr, int mid) {
    int min = Integer.MAX_VALUE;
    for (int i = 0; i <= mid; i++) min = Math.min(min, arr[i]);
    return min;
}
public int minInRight(int[] arr, int mid) {
    int min = Integer.MAX_VALUE;
    for (int i = mid; i < arr.length; i++) min = Math.min(min, arr[i]);
    return min;
}

// GOOD: extract helper
public int minInRange(int[] arr, int start, int end) {
    int min = Integer.MAX_VALUE;
    for (int i = start; i <= end; i++) min = Math.min(min, arr[i]);
    return min;
}
```

### Error Handling
```java
// Check null inputs
public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
    if (l1 == null) return l2;
    if (l2 == null) return l1;
    // ... rest of solution
}

// Check boundary conditions
public int trap(int[] height) {
    if (height == null || height.length < 3) return 0;
    // ... rest of solution
}
```

### Code Completeness
- All imports present? (`java.util.*`)
- Method signature matches the problem?
- Return statement in all branches?
- No unclosed resources (Scanner, Stream)?

---

## 2. Optimization Discussion

### Time Complexity Optimization

| Current | Possible Optimization | Technique |
|---|---|---|
| O(n²) nested loops | O(n log n) sort + scan | Sorting |
| O(n²) DP table | O(n) rolling array | Space optimization |
| O(n) linear scan | O(log n) binary search | If input sorted |
| O(n) repeated work | O(n) cached results | Memoization |
| O(V²) graph | O(V + E) adjacency list | Better representation |

### Space Complexity Optimization

```java
// DP: O(n) space → O(1) space
// Climbing stairs
public int climbStairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// DP: 2D array → 1D rolling array
// Longest common subsequence (partial)
public int lcsOptimized(String s1, String s2) {
    int[] prev = new int[s2.length() + 1];
    for (int i = 1; i <= s1.length(); i++) {
        int[] curr = new int[s2.length() + 1];
        for (int j = 1; j <= s2.length(); j++) {
            if (s1.charAt(i-1) == s2.charAt(j-1))
                curr[j] = prev[j-1] + 1;
            else
                curr[j] = Math.max(prev[j], curr[j-1]);
        }
        prev = curr;
    }
    return prev[s2.length()];
}

// HashSet → boolean array for ASCII chars
public boolean isUnique(String s) {
    boolean[] seen = new boolean[128];  // O(1) space, O(n) time
    for (char c : s.toCharArray()) {
        if (seen[c]) return false;
        seen[c] = true;
    }
    return true;
}
```

---

## 3. Trade-Off Analysis

### When O(n²) is Better Than O(n log n)

```java
// Small input size: n < 100
// O(n²) has less overhead than sorting + scanning
// Example: finding max pair sum in small array
public int maxPairSum(int[] arr) {
    if (arr.length < 2) throw new IllegalArgumentException();
    int max = Integer.MIN_VALUE;
    for (int i = 0; i < arr.length; i++) {
        for (int j = i + 1; j < arr.length; j++) {
            max = Math.max(max, arr[i] + arr[j]);
        }
    }
    return max;
}
// For n=50, this is ~1250 ops vs ~300 ops for sort+scan
// The constant factor of sorting makes it comparable
```

### Trade-Off Matrix

| Factor | O(n²) | O(n log n) | O(n) |
|---|---|---|---|
| Implementation simplicity | Simple | Moderate | Varies |
| Constant factor | Low | Medium | Low-Medium |
| Cache performance | Good | Good | Good |
| Parallelizable | Sometimes | Yes | Sometimes |
| Small n (<100) | Preferred | Overkill | OK |
| Large n (>10⁶) | TLE | Preferred | Best |

### Space-Time Trade-Off
```java
// Use more space to save time
public boolean hasDuplicate(int[] arr) {
    HashSet<Integer> seen = new HashSet<>();  // O(n) space for O(n) time
    for (int num : arr) {
        if (!seen.add(num)) return true;
    }
    return false;
}

// Use more time to save space
public boolean hasDuplicateInPlace(int[] arr) {
    Arrays.sort(arr);  // O(1) extra space for O(n log n) time
    for (int i = 1; i < arr.length; i++) {
        if (arr[i] == arr[i-1]) return true;
    }
    return false;
}
```

---

## 4. Follow-Up Scenarios

### "What if the input is a stream?"

```java
// Streaming data: maintain running state
// Running median
class RunningMedian {
    private PriorityQueue<Integer> maxHeap;  // lower half
    private PriorityQueue<Integer> minHeap;  // upper half

    public RunningMedian() {
        maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        minHeap = new PriorityQueue<>();
    }

    public void addNum(int num) {
        maxHeap.add(num);
        minHeap.add(maxHeap.poll());  // balance
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.add(minHeap.poll());
        }
    }

    public double findMedian() {
        if (maxHeap.size() > minHeap.size()) return maxHeap.peek();
        return (maxHeap.peek() + minHeap.peek()) / 2.0;
    }
}

// Streaming: sliding window maximum
class SlidingWindowMax {
    private Deque<Integer> deque = new ArrayDeque<>();

    public void add(int index, int val) {
        while (!deque.isEmpty() && index - deque.peekFirst() >= windowSize) {
            deque.pollFirst();
        }
        while (!deque.isEmpty() && nums[deque.peekLast()] <= val) {
            deque.pollLast();
        }
        deque.addLast(index);
    }
}
```

### "What if the data doesn't fit in memory?"

```java
// External sort: divide and conquer
// 1. Split file into chunks that fit in memory
// 2. Sort each chunk in memory, write to temp files
// 3. Merge sorted temp files

// MapReduce pattern for distributed processing
// For interviews: explain the approach, don't implement full solution

// Database approach
// "I would use a database with appropriate indexing"
// "For very large data, I'd use external sorting or MapReduce"

// For specific problems:
// - Two Sum on 1TB file: use hash-based partitioning
// - Sort 10GB file: external merge sort
// - Find median of billion numbers: reservoir sampling or k-th element on chunks
```

### "How would you handle concurrent access?"

```java
// Thread-safe version of a solution
public class ThreadSafeCounter {
    private final ConcurrentHashMap<String, AtomicInteger> map = new ConcurrentHashMap<>();

    public void increment(String key) {
        map.computeIfAbsent(key, k -> new AtomicInteger(0)).incrementAndGet();
    }

    public int get(String key) {
        return map.getOrDefault(key, new AtomicInteger(0)).get();
    }
}

// Read-write lock for read-heavy workloads
private final ReadWriteLock lock = new ReentrantReadWriteLock();

public int read(int key) {
    lock.readLock().lock();
    try {
        return cache.getOrDefault(key, -1);
    } finally {
        lock.readLock().unlock();
    }
}

public void write(int key, int value) {
    lock.writeLock().lock();
    try {
        cache.put(key, value);
    } finally {
        lock.writeLock().unlock();
    }
}

// For interview: "I'd use ConcurrentHashMap for thread safety,
// or a ReadWriteLock if reads vastly outnumber writes."
```

---

## 5. Scaling Discussion

### How Would This Work for 1 Billion Elements?

```
Input size: 1B integers = 4GB (fits in RAM on most machines)

If it doesn't fit in memory:
- Partition data across machines
- Process in parallel with MapReduce
- Use external memory algorithms

If time complexity matters:
- O(n) with n=10^9: ~10^9 operations = ~1 second on modern CPU
- O(n log n): ~30 × 10^9 operations = ~30 seconds
- O(n²): 10^18 operations = ~31 years — impossible
```

### Scaling Framework

```
1. Estimate data size
   - 1B integers = 4GB
   - 1B strings (avg 10 chars) = ~14GB
   - 1B objects = much larger

2. Choose algorithm complexity
   - O(n) or O(n log n) required for 10^9 elements
   - O(n²) only for n < 10^5

3. Choose data structures
   - Arrays: contiguous, cache-friendly
   - Lists: pointer overhead, bad cache locality
   - Trees: O(log n) operations
   - Hash maps: O(1) average, O(n) worst case

4. Choose processing model
   - Single machine, in-memory: simplest
   - Single machine, external memory: disk-based
   - Distributed: MapReduce, Spark, Flink
```

---

## 6. Refactoring

### Common Refactoring Opportunities

```java
// 1. Extract method
// BAD: 50-line method
public void solve(int[] arr) {
    // 30 lines of preprocessing
    // 20 lines of main logic
}

// GOOD: separate concerns
public void solve(int[] arr) {
    int[] processed = preprocess(arr);
    return coreLogic(processed);
}

// 2. Replace magic with named constants
// BAD
if (state == 0) { ... } else if (state == 1) { ... }

// GOOD
private static final int UNVISITED = 0;
private static final int IN_PROGRESS = 1;
private static final int DONE = 2;

if (state == UNVISITED) { ... } else if (state == IN_PROGRESS) { ... }

// 3. Replace nested conditionals
// BAD
if (a) {
    if (b) {
        if (c) { doSomething(); }
    }
}

// GOOD: guard clause
if (!a || !b || !c) return;
doSomething();

// 4. Use Java streams for readability
// BAD
List<Integer> result = new ArrayList<>();
for (int x : list) {
    if (x > 0) result.add(x * 2);
}

// GOOD
List<Integer> result = list.stream()
    .filter(x -> x > 0)
    .map(x -> x * 2)
    .collect(Collectors.toList());
```

---

## 7. Testing Strategy

### Unit Tests to Write

```java
// Standard cases
@Test
void testNormalCase() {
    assertEquals(5, solution.maxSubarray(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}));
}

// Edge cases
@Test
void testEmptyInput() {
    assertThrows(IllegalArgumentException.class, () -> solution.maxSubarray(new int[]{}));
}

@Test
void testSingleElement() {
    assertEquals(3, solution.maxSubarray(new int[]{3}));
}

@Test
void testAllNegative() {
    assertEquals(-1, solution.maxSubarray(new int[]{-3, -4, -1, -2}));
}

@Test
void testAllPositive() {
    assertEquals(15, solution.maxSubarray(new int[]{1, 2, 3, 4, 5}));
}

@Test
void testLargeInput() {
    int[] arr = new int[100000];
    Arrays.fill(arr, 1);
    assertEquals(100000, solution.maxSubarray(arr));
}

// Boundary conditions
@Test
void testMinValue() {
    assertEquals(Integer.MIN_VALUE, solution.maxSubarray(new int[]{Integer.MIN_VALUE}));
}
```

### Stress Testing Pattern

```java
// For randomized testing to find bugs
public void stressTest() {
    Random rand = new Random(42);
    for (int test = 0; test < 10000; test++) {
        int n = rand.nextInt(100) + 1;
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = rand.nextInt(1000) - 500;
        }
        int result1 = bruteForce(arr);  // O(n²) correct solution
        int result2 = optimized(arr);   // Your solution
        assert result1 == result2 :
            "Failed on: " + Arrays.toString(arr) +
            " expected=" + result1 + " got=" + result2;
    }
}
```

---

## 8. Production Considerations

### Thread Safety
```java
// Not thread-safe
private Map<String, Integer> cache = new HashMap<>();

// Thread-safe options:
private Map<String, Integer> cache = new ConcurrentHashMap<>();
private Map<String, Integer> cache = Collections.synchronizedMap(new HashMap<>());
private volatile Map<String, Integer> cache = new HashMap<>();  // only for immutable maps
```

### Memory Limits
```java
// Estimate memory usage
// int: 4 bytes, long: 8 bytes, object: 16 bytes + fields
// HashMap entry: ~32 bytes + key + value
// ArrayList: 4 bytes per element (references)

// For 10^7 elements:
// int[]: 40MB
// Integer[]: 160MB + GC overhead
// ArrayList<Integer>: ~480MB
// HashMap<Integer, Integer>: ~960MB

// Use primitive arrays when possible
// Use arrays over collections for performance-critical code
```

### Garbage Collection
```java
// Avoid creating objects in tight loops
// BAD
for (int i = 0; i < n; i++) {
    String s = String.valueOf(i);  // new String each iteration
    process(s);
}

// BETTER
StringBuilder sb = new StringBuilder();
for (int i = 0; i < n; i++) {
    sb.setLength(0);  // reuse
    sb.append(i);
    process(sb.toString());
}

// Reuse collections
List<Integer> buffer = new ArrayList<>();
for (int i = 0; i < n; i++) {
    buffer.clear();  // reuse
    collectData(buffer);
    process(buffer);
}
```

---

## Template Responses for Common Follow-Ups

### "Can you optimize further?"
> "Yes, currently we're using O(n) time and O(n) space. We could reduce space to O(1) by [technique]. For example, instead of storing all intermediate results, we only need to track [specific values]."

### "What's the time complexity?"
> "The algorithm makes [one/two] passes through the data, so it's O(n). The [sorting/hashmap] step is O(n log n) / O(1) average. Overall, it's O(n) / O(n log n)."

### "How would you test this?"
> "I'd write unit tests covering: normal cases, empty input, single element, all same elements, already sorted input, and large inputs. I'd also add stress tests comparing against a brute-force implementation."

### "What if the input is very large?"
> "For inputs larger than memory, I'd use [external sort / streaming / pagination]. For truly massive datasets, I'd distribute across machines using [MapReduce / partitioning]. The time complexity stays the same, but we add I/O overhead."

### "How would this work in production?"
> "I'd add input validation, error handling, and logging. For thread safety, I'd use [ConcurrentHashMap / locks]. I'd also add metrics for monitoring and set up rate limiting if it's an API."

### "What are the trade-offs of your approach?"
> "My approach trades [space/time] for [time/space]. It's optimal for [typical case] but could be slower for [worst case]. An alternative would be [other approach], which is better when [specific condition] but worse when [other condition]."
