# 02 — Space Complexity

Time complexity gets all the attention, but space complexity — how much memory your algorithm uses — is equally important. In interviews, you'll often need to find a balance between time and space.

---

## 1. Input Space vs Auxiliary Space

### The Distinction

```java
public int sum(int[] arr) {
    int total = 0;              // auxiliary space
    for (int x : arr) {
        total += x;
    }
    return total;
}
```

- **Input space:** Memory taken by the input (`arr`). We usually don't count this.
- **Auxiliary space:** Extra memory your algorithm uses (`total` variable).
- **Total space:** Input space + Auxiliary space.

**When we say "O(1) space" or "in-place", we mean O(1) auxiliary space.**

### Why We Ignore Input Space

Because the input already exists before your algorithm runs. The question is: "How much *extra* memory do you need to solve this problem?"

---

## 2. How to Calculate Space Complexity

### Variables — O(1) per primitive, O(size) per reference

```java
// O(1) space — fixed number of variables
public int max(int[] arr) {
    int max = Integer.MIN_VALUE;   // O(1)
    for (int x : arr) {
        if (x > max) max = x;      // O(1)
    }
    return max;
}

// O(n) space — creating an array of size n
public int[] copyArray(int[] arr) {
    int[] copy = new int[arr.length];  // O(n)
    System.arraycopy(arr, 0, copy, 0, arr.length);
    return copy;
}

// O(n²) space — 2D matrix
public int[][] identityMatrix(int n) {
    int[][] mat = new int[n][n];  // O(n²)
    for (int i = 0; i < n; i++) mat[i][i] = 1;
    return mat;
}
```

### Recursion Stack Space

Every recursive call adds a **stack frame** — it contains local variables, return address, etc. The recursion depth determines space.

```java
// O(n) stack space — recursion depth = n
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// O(log n) stack space — recursion depth = log n
int binarySearch(int[] arr, int target, int low, int high) {
    if (low > high) return -1;
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) return binarySearch(arr, target, mid + 1, high);
    return binarySearch(arr, target, low, mid - 1);
}

// O(n) stack space — depth = n, even though only O(1) extra variables
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
// Wait — this is O(n) stack space (depth), but O(2ⁿ) time
```

**Key insight:** Recursion space = maximum recursion depth × size per frame.

---

## 3. Tail Recursion — Space Optimization

```java
// Non-tail recursive — O(n) stack space
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
    // After recursion returns, still needs to multiply by n
}

// Tail recursive — O(1) stack space with TCO
int factorialTail(int n, int accumulator) {
    if (n <= 1) return accumulator;
    return factorialTail(n - 1, n * accumulator);
    // No work after recursive call — result is returned directly
}
```

**Tail call optimization (TCO):** If the last thing a function does is call itself (and returns its result directly), the compiler can reuse the current stack frame instead of creating a new one.

**Java DOES NOT have TCO.** That's right — Java won't optimize tail recursion. Every recursive call creates a new stack frame regardless.

```java
// In Java, this will stack overflow for large n:
int factorialTail(int n, int acc) {
    if (n <= 1) return acc;
    return factorialTail(n - 1, n * acc);
}
// factorialTail(10000) → StackOverflowError!
```

**Implication:** In Java, prefer iteration over recursion when you care about space and n could be large.

---

## 4. In-Place Algorithms — O(1) Extra Space

An algorithm is **in-place** if it uses O(1) auxiliary space (excluding input and output).

```java
// In-place array reversal — O(1) space
void reverse(int[] arr) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int temp = arr[left];         // O(1) extra
        arr[left] = arr[right];
        arr[right] = temp;
        left++;
        right--;
    }
}
// Space: just 'left', 'right', 'temp' — O(1)

// NOT in-place — creates a new array
int[] reverseNewArray(int[] arr) {
    int[] result = new int[arr.length];  // O(n) extra!
    for (int i = 0; i < arr.length; i++) {
        result[i] = arr[arr.length - 1 - i];
    }
    return result;
}
```

### Examples of In-Place Algorithms

| Algorithm | Space | Notes |
|-----------|-------|-------|
| Bubble sort | O(1) | Swaps in-place |
| Selection sort | O(1) | Swaps in-place |
| Insertion sort | O(1) | Shifts elements |
| Quick sort | O(log n) | Recursion stack (in-place partitioning) |
| Heap sort | O(1) | In-place heapify |
| Merge sort (iterative) | O(1) possible | Usually O(n) for merging |
| Matrix rotation | O(1) | Four-way swaps |

---

## 5. Common Space Complexities

### O(1) — Constant Space

```java
int findMax(int[] arr) {
    int max = Integer.MIN_VALUE;
    for (int x : arr) {
        if (x > max) max = x;
    }
    return max;
}
```

### O(log n) — Logarithmic Space

```java
// Recursive binary search — O(log n) stack depth
int binarySearch(int[] arr, int target, int l, int r) {
    if (l > r) return -1;
    int mid = l + (r - l) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target)
        return binarySearch(arr, target, mid + 1, r);
    return binarySearch(arr, target, l, mid - 1);
}

// Quick sort — O(log n) average stack depth
void quickSort(int[] arr, int low, int high) {
    if (low >= high) return;
    int pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
}
```

### O(n) — Linear Space

```java
// Creating a copy
int[] clone = arr.clone();

// Hash map for counting
Map<Integer, Integer> freq = new HashMap<>();
for (int x : arr) freq.put(x, freq.getOrDefault(x, 0) + 1);

// Recursion with linear depth (if n is reasonable)
void printReverse(int n, int[] arr) {
    if (n == 0) return;
    System.out.println(arr[n - 1]);
    printReverse(n - 1, arr);
}

// String builder
StringBuilder sb = new StringBuilder();
for (String s : strings) sb.append(s);
```

### O(n²) — Quadratic Space

```java
// 2D matrix
int[][] dp = new int[n][n];

// Adjacency matrix for graphs
int[][] adjacency = new int[n][n];
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        adjacency[i][j] = (hasEdge(i, j)) ? 1 : 0;
    }
}
```

---

## 6. The Time-Space Tradeoff

Almost every optimization problem in DSA involves trading time for space or vice versa.

### Example 1: Two Sum

```java
// O(n²) time, O(1) space — brute force
int[] twoSumBrute(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target)
                return new int[]{i, j};
        }
    }
    return new int[]{-1, -1};
}

// O(n) time, O(n) space — HashMap
int[] twoSumHashMap(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement))
            return new int[]{map.get(complement), i};
        map.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```

**Tradeoff:** Brute force uses no extra memory but is slow. HashMap uses O(n) memory but is fast.

### Example 2: Duplicate Detection

```java
// O(n²) time, O(1) space
boolean hasDuplicatesBrute(int[] arr) {
    for (int i = 0; i < arr.length; i++) {
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[i] == arr[j]) return true;
        }
    }
    return false;
}

// O(n log n) time, O(1) space (sort first)
boolean hasDuplicatesSorted(int[] arr) {
    Arrays.sort(arr);
    for (int i = 1; i < arr.length; i++) {
        if (arr[i] == arr[i - 1]) return true;
    }
    return false;
}

// O(n) time, O(n) space (HashSet)
boolean hasDuplicatesSet(int[] arr) {
    Set<Integer> set = new HashSet<>();
    for (int x : arr) {
        if (!set.add(x)) return true;
    }
    return false;
}
```

**Three solutions, three tradeoffs.** The right choice depends on constraints.

---

## 7. Space Complexity of Common Data Structures

### Arrays & Strings

| Structure | Space |
|-----------|-------|
| `int[n]` | O(n) |
| `int[n][m]` | O(n·m) |
| `String` of length n | O(n) |
| `StringBuilder` capacity c | O(c) |

### Collection Classes

| Structure | Space |
|-----------|-------|
| `ArrayList`, `Vector` | O(n) |
| `LinkedList` | O(n) — ~3× overhead (value + prev + next) |
| `HashMap`, `HashSet` | O(n + capacity) — capacity is power of 2 |
| `TreeMap`, `TreeSet` | O(n) — Red-Black tree nodes |
| `PriorityQueue` | O(n) |
| `ArrayDeque` | O(n) |

### Hidden Space Costs

```java
// Autoboxing overhead
ArrayList<Integer> list = new ArrayList<>(1_000_000);
// int = 4 bytes, Integer = 16-24 bytes (header + value)
// 4 MB vs 16-24 MB!

// String overhead
String s = "hello";
// ≈ 40 bytes (header + char[] reference) + 5×2 bytes (char array) + header

// HashMap overhead per entry
// HashMap.Entry = ~32 bytes + key + value objects
// A HashMap<Integer, Integer> with 1M entries ≈ 40-50 MB
```

---

## 8. Analyzing Space: Step-by-Step

### Example: Merge Sort

```java
void mergeSort(int[] arr, int l, int r) {
    if (l >= r) return;
    int mid = l + (r - l) / 2;
    mergeSort(arr, l, mid);
    mergeSort(arr, mid + 1, r);
    merge(arr, l, mid, r);
}

void merge(int[] arr, int l, int mid, int r) {
    // Creates temporary arrays!
    int[] left = Arrays.copyOfRange(arr, l, mid + 1);  // O(n)
    int[] right = Arrays.copyOfRange(arr, mid + 1, r + 1);  // O(n)
    // ... merge back into arr
}
```

**Space analysis:**
- `mergeSort` recursion: O(log n) stack frames (depth)
- `merge` creates temporary arrays: O(n) total per level
- But at any point, only one merge is executing → O(n) auxiliary space
- **Total: O(n)** auxiliary

### Example: Recursive Fibonacci

```java
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
```

**Space analysis:**
- Maximum recursion depth = n (going down the leftmost branch)
- Each frame is O(1)
- **Total: O(n)** stack space

### Example: Quick Sort

```java
void quickSort(int[] arr, int low, int high) {
    if (low >= high) return;
    int pi = partition(arr, low, high);  // in-place — O(1) extra
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
}
```

**Space analysis:**
- Partition is in-place: O(1) auxiliary
- Recursion depth: O(log n) average, O(n) worst (if pivots are bad)
- **Total: O(log n)** average, **O(n)** worst

---

## 9. Space Optimization Techniques

### 1. Modify Input In-Place (If Allowed)

```java
// Instead of creating new arrays, write to the input
// (Only if problem allows modifying input!)
public int[] runningSum(int[] nums) {
    for (int i = 1; i < nums.length; i++) {
        nums[i] += nums[i - 1];  // in-place
    }
    return nums;
}
```

### 2. Use Primitives Instead of Objects

```java
// Instead of: ArrayList<Integer> list = new ArrayList<>();
// Use: int[] arr = new int[n];

// Instead of: Stack<Integer> stack = new Stack<>();
// Use: int[] stack = new int[n]; int top = -1;
```

### 3. Reuse Arrays

```java
// DP with space optimization
// Instead of: int[][] dp = new int[n][k];
// Use: int[] dp = new int[k];  // overwrite each row
```

### 4. Tail Recursion → Iteration

Since Java has no TCO, convert tail-recursive functions to loops:

```java
// Tail recursive: O(n) stack space (no TCO)
int factorial(int n, int acc) {
    if (n <= 1) return acc;
    return factorial(n - 1, n * acc);
}

// Iterative: O(1) space
int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}
```

---

## Space Complexity Cheat Sheet

```
Variables (primitives)        → O(1)
Arrays of size n              → O(n)
2D array of n×n               → O(n²)
Recursion stack (depth d)     → O(d)
HashMap with n entries        → O(n)
String of length n            → O(n)
StringBuilder capacity n      → O(n)

In-place                      → O(1) aux
Out-of-place copy             → O(n) aux (typically)

Tail recursion (w/ TCO)       → O(1)
Tail recursion (Java, no TCO) → O(n)
```

Remember: when an interviewer asks for "constant space", they mean O(1) auxiliary space. Input doesn't count.
