# TCS Digital / Ninja Interview Patterns

## Table of Contents
1. Hiring Process
2. TCS Digital vs Ninja
3. Most Asked Topics
4. Coding Round Details
5. Example Problems with Solutions
6. Preparation Strategy

---

## 1. Hiring Process

### TCS Ninja (Entry Level)
- **Registration** → **Online Test** → **Interview** (Technical + HR)

### TCS Digital (Higher Package)
- **Registration** → **Online Test** → **Technical Interview** → **Managerial/HR**

### Online Test Format

| Section | Duration | Content |
|---------|----------|---------|
| Aptitude | 40 min | Quantitative, Logical, Verbal |
| Programming | 60-90 min | 2-3 coding problems |
| (Digital only) Advanced Coding | 60 min | 1-2 harder problems |

### Key Difference
- **Ninja**: Coding problems are Easy-Medium, focus on basic DSA
- **Digital**: Problems are Medium, may include DP or Graph
- **Digital** also has a separate **Advanced Coding** round

---

## 2. Most Asked Topics

| Topic | Ninja | Digital | Why TCS Asks It |
|-------|-------|---------|-----------------|
| Arrays | Very High | Very High | Foundation, frequency |
| Strings | Very High | High | Text processing |
| Math / Number Theory | High | Medium | Basic logic testing |
| Matrix | High | Medium | 2D array manipulation |
| Sorting | Medium | Medium | Array operations |
| Pattern Printing | High | Low | Basic logic (Ninja) |
| HashMap | Medium | High | Frequency counting |
| Recursion | Low | Medium | Problem-solving |
| DP | Rare | Medium | Optimization (Digital) |
| Graphs | Rare | Low | Connectivity (Digital) |

### Topic Frequency Graph (Ninja)
```
Arrays:  ████████████████████
Strings: ████████████████████
Math:    ████████████████
Matrix:  ██████████████
Pattern: ██████████
```

### Topic Frequency Graph (Digital)
```
Arrays:  ████████████████████
Strings: ████████████████
HashMap: ██████████████
Matrix:  ██████████
DP:      ████████
Graphs:  ██████
```

---

## 3. Coding Round Details

### Ninja Coding (2 problems, 60 min)
- **Problem 1** (Easy): Basic array/string manipulation
- **Problem 2** (Medium): Requires simple algorithm
- Languages allowed: Java, C++, Python, C
- Focus: **CORRECT code above all else**

### Digital Advanced Coding (1-2 problems, 60 min)
- **Problem 1** (Medium): HashMap or sorting based
- **Problem 2** (Medium-Hard): DP or Graph
- Focus: Correctness + Efficiency

### Grading Criteria (in order)
1. **All test cases pass** (most important)
2. **Edge cases handled**
3. **Time complexity** (should be reasonable)
4. **Code readability** (variable names, structure)
5. **Comments** (optional but helpful)

---

## 4. Example Problems with Solutions

### Problem 1: Leaders in an Array (TCS Favorite)
**Problem:** Find all leaders in an array (element > all elements to its right).

**Approach:** Scan from right, track max.
```java
public List<Integer> findLeaders(int[] arr) {
    List<Integer> leaders = new ArrayList<>();
    int maxFromRight = Integer.MIN_VALUE;
    for (int i = arr.length - 1; i >= 0; i--) {
        if (arr[i] > maxFromRight) {
            leaders.add(arr[i]);
            maxFromRight = arr[i];
        }
    }
    Collections.reverse(leaders);
    return leaders;
}
```

### Problem 2: Array Rotation (Very Common)
**Problem:** Rotate array left by k positions.

**Approach:** Reverse parts.
```java
public void rotateLeft(int[] arr, int k) {
    int n = arr.length;
    k = k % n;
    reverse(arr, 0, k - 1);
    reverse(arr, k, n - 1);
    reverse(arr, 0, n - 1);
}
private void reverse(int[] arr, int left, int right) {
    while (left < right) {
        int temp = arr[left];
        arr[left] = arr[right];
        arr[right] = temp;
        left++; right--;
    }
}
```

### Problem 3: Pattern Printing (Ninja)
**Problem:** Print a diamond pattern with `*`.

```java
public void printDiamond(int n) {
    // Upper half
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i; j++) System.out.print(" ");
        for (int j = 1; j <= 2 * i - 1; j++) System.out.print("*");
        System.out.println();
    }
    // Lower half
    for (int i = n - 1; i >= 1; i--) {
        for (int j = 1; j <= n - i; j++) System.out.print(" ");
        for (int j = 1; j <= 2 * i - 1; j++) System.out.print("*");
        System.out.println();
    }
}
```

### Problem 4: Anagram Check (Digital)
**Problem:** Check if two strings are anagrams.

**Approach:** Frequency array.
```java
public boolean areAnagrams(String s1, String s2) {
    if (s1.length() != s2.length()) return false;
    int[] freq = new int[256];
    for (char c : s1.toCharArray()) freq[c]++;
    for (char c : s2.toCharArray()) {
        if (freq[c] == 0) return false;
        freq[c]--;
    }
    return true;
}
```

### Problem 5: Count Subarrays with Sum = K (Digital)
**Problem:** Count subarrays whose sum equals K.

**Approach:** Prefix sum + HashMap.
```java
public int countSubarrays(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1);
    int sum = 0, count = 0;
    for (int num : nums) {
        sum += num;
        count += prefixCount.getOrDefault(sum - k, 0);
        prefixCount.put(sum, prefixCount.getOrDefault(sum, 0) + 1);
    }
    return count;
}
```

### Problem 6: Fibonacci (Recursive vs Iterative)
**Problem:** Find nth Fibonacci number.

**Iterative (preferred):**
```java
public int fibonacci(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int next = a + b;
        a = b;
        b = next;
    }
    return b;
}
```

### Problem 7: Prime Number Check
**Problem:** Check if a number is prime.

```java
public boolean isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}
```

### Problem 8: Matrix Spiral (Digital)
**Problem:** Print matrix in spiral order.

**Approach:** Layer by layer (standard algorithm).
```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    int top = 0, bottom = matrix.length - 1;
    int left = 0, right = matrix[0].length - 1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) result.add(matrix[top][j]);
        top++;
        for (int i = top; i <= bottom; i++) result.add(matrix[i][right]);
        right--;
        if (top <= bottom) {
            for (int j = right; j >= left; j--) result.add(matrix[bottom][j]);
            bottom--;
        }
        if (left <= right) {
            for (int i = bottom; i >= top; i--) result.add(matrix[i][left]);
            left++;
        }
    }
    return result;
}
```

---

## 5. Preparation Strategy

### Phase 1: Basics (Week 1-2)
- **Arrays**: Sorting, rotation, leaders, subarray operations
- **Strings**: palindrome, anagram, frequency counting
- **Math**: Prime numbers, GCD, factorial, Fibonacci
- **Pattern printing**: All classic patterns (diamond, triangle, number pyramid)

### Phase 2: Core DSA (Week 3-4)
- **HashMap**: Frequency counting, two sum, subarray sum
- **Sorting**: All O(n log n) algorithms
- **Recursion**: Basic backtracking
- **Matrix operations**: Spiral, transpose, rotate, search

### Phase 3 (Digital Only): Advanced (Week 5-6)
- **DP**: Knapsack, LIS, subset sum basics
- **Graphs**: BFS/DFS, connected components
- **Trees**: Basic traversal
- **Sliding window**: Basic substring problems

### Must-Practice Problems

**For Ninja:**
- Array rotation (left/right)
- Leaders in an array
- Find duplicate in array
- Pattern printing (all types)
- Palindrome check
- Anagram check
- Prime number operations
- Array reversal
- Matrix addition/multiplication
- Character frequency counting

**Additional for Digital:**
- Subarray sum = K
- Longest substring without repeat
- Longest common subsequence
- 0/1 Knapsack
- BFS/DFS on grid
- Minimum path sum
- Validate BST
- Top K frequent elements

### TCS-Specific Tips
1. **Correctness is #1** — A working solution with O(n²) beats a non-working O(n)
2. **Handle all edge cases** — Empty input, single element, all same values
3. **Test mentally** — Trace through your code with examples
4. **Keep it simple** — Don't over-complicate; TCS tests fundamentals
5. **Time management** — If stuck on one problem, move to the next
6. **Know your language well** — Java/Python/C++ — be comfortable with syntax
7. **Practice without IDE** — The test environment may not have syntax highlighting
