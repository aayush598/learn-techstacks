# Array Basics & Operations

## Declaration and Initialization

Arrays in Java are **objects**, not primitives. They live on the heap. There are two ways to declare:

```java
int[] arr;           // preferred — the type is "int array"
int arr[];           // C-style, works but less readable
```

### Initialization flavors

```java
// 1. Declare + allocate (default values: 0 for int, null for objects, false for boolean)
int[] arr = new int[5];        // [0, 0, 0, 0, 0]

// 2. Declare + inline init
int[] arr = {10, 20, 30, 40, 50};

// 3. Anonymous array (no new variable name)
new int[]{1, 2, 3, 4, 5};

// 4. Using a loop
int[] arr = new int[5];
for (int i = 0; i < arr.length; i++) {
    arr[i] = i * 10;
}
```

The `length` field is a **final int** set at creation. It is NOT a method — this trips up beginners who type `arr.length()`.

## Memory Layout

```plaintext
Stack                           Heap
+-----------+                   +----------------------------+
| arr       | ----> [ref] ----> | [0] | [1] | [2] | [3] | [4] |
+-----------+                   +----------------------------+

- arr holds a 4-byte (or 8-byte on 64-bit JVM) reference
- The array object itself has: length field + contiguous block of elements
- Access time: O(1) — calculate offset = baseAddress + index * elementSize
```

Contiguous memory means **cache-friendly** iteration. When you read `arr[i]`, the CPU pulls a cache line (64 bytes) into L1 cache, so `arr[i+1]` is likely already there. That's why arrays are faster than linked lists for traversal.

## Traversal Patterns

### Forward traversal

```java
for (int i = 0; i < arr.length; i++) {
    System.out.print(arr[i] + " ");
}
```

### Enhanced for-each (read-only)

```java
for (int val : arr) {
    System.out.print(val + " ");
}
```

### Backward traversal

```java
for (int i = arr.length - 1; i >= 0; i--) {
    System.out.print(arr[i] + " ");
}
```

### Two-direction / meet-in-the-middle

```java
int left = 0, right = arr.length - 1;
while (left <= right) {
    // process arr[left] and arr[right]
    left++;
    right--;
}
```

## Insertion Operations — O(n) Shifts

Arrays have **fixed size**. Insertion means shifting elements right to create a hole. This is O(n).

### Insert at beginning

```java
public static int[] insertAtBeginning(int[] arr, int value) {
    int[] newArr = new int[arr.length + 1];
    newArr[0] = value;
    for (int i = 0; i < arr.length; i++) {
        newArr[i + 1] = arr[i];
    }
    return newArr;
}
```

### Insert at end

**Trivial if capacity exists.** Otherwise you need a new array (same as above but copy then add at end).

```java
public static int[] insertAtEnd(int[] arr, int value) {
    int[] newArr = Arrays.copyOf(arr, arr.length + 1);
    newArr[arr.length] = value;
    return newArr;
}
```

### Insert at position pos (0-indexed)

```java
public static int[] insertAtPosition(int[] arr, int pos, int value) {
    int[] newArr = new int[arr.length + 1];
    for (int i = 0; i < pos; i++) {
        newArr[i] = arr[i];
    }
    newArr[pos] = value;
    for (int i = pos; i < arr.length; i++) {
        newArr[i + 1] = arr[i];
    }
    return newArr;
}
```

**Key insight:** Shifting is the bottleneck. If you need frequent insertions at arbitrary positions, consider `ArrayList` (amortized O(1) add at end) or `LinkedList` (O(1) at head, O(n) for indexed insert).

## Deletion Operations — O(n) Shifts

### Delete at beginning

```java
public static int[] deleteAtBeginning(int[] arr) {
    if (arr.length == 0) return arr;
    int[] newArr = new int[arr.length - 1];
    for (int i = 1; i < arr.length; i++) {
        newArr[i - 1] = arr[i];
    }
    return newArr;
}
```

### Delete at end

```java
public static int[] deleteAtEnd(int[] arr) {
    if (arr.length == 0) return arr;
    return Arrays.copyOf(arr, arr.length - 1);
}
```

### Delete at position

```java
public static int[] deleteAtPosition(int[] arr, int pos) {
    if (pos < 0 || pos >= arr.length) return arr;
    int[] newArr = new int[arr.length - 1];
    for (int i = 0, j = 0; i < arr.length; i++) {
        if (i != pos) newArr[j++] = arr[i];
    }
    return newArr;
}
```

## Linear Search

Walk through each element. O(n) time, O(1) space.

```java
public static int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}
```

**When to use:** unsorted data, small arrays, single search query.

## Reverse an Array

### Two-pointer swap (O(n), O(1) space)

```java
public static void reverse(int[] arr) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int temp = arr[left];
        arr[left] = arr[right];
        arr[right] = temp;
        left++;
        right--;
    }
}
```

### Using recursion

```java
public static void reverseRecursive(int[] arr, int left, int right) {
    if (left >= right) return;
    int temp = arr[left];
    arr[left] = arr[right];
    arr[right] = temp;
    reverseRecursive(arr, left + 1, right - 1);
}
```

## Rotate Array by K Positions

Rotate left by k positions: `[1,2,3,4,5]` with k=2 → `[3,4,5,1,2]`.

### Brute force: rotate one by one — O(n*k), O(1) space

### Using extra array — O(n), O(n) space

```java
public static void rotateLeft(int[] arr, int k) {
    int n = arr.length;
    k = k % n;
    int[] temp = new int[n];
    for (int i = 0; i < n; i++) {
        temp[i] = arr[(i + k) % n];
    }
    System.arraycopy(temp, 0, arr, 0, n);
}
```

### Reversal algorithm — O(n), O(1) space (THE BEST)

This is a classic. Reverse three segments:

```java
public static void rotateLeft(int[] arr, int k) {
    int n = arr.length;
    k = k % n;
    reverse(arr, 0, k - 1);   // reverse first k elements
    reverse(arr, k, n - 1);   // reverse remaining
    reverse(arr, 0, n - 1);   // reverse whole array
}
```

**Why this works:** Visualize it. Reversing segments isolates the block that wraps around, then the full reversal puts them in correct relative order.

For **right rotation** by k: reverse(arr, 0, n-1), reverse(arr, 0, k-1), reverse(arr, k, n-1).

## Leaders in an Array

**Problem:** An element is a "leader" if it is greater than ALL elements to its right. The rightmost element is always a leader.

### Naive: O(n²) — for each element, scan right

### Optimal: O(n) — scan from right, track max

```java
public static List<Integer> findLeaders(int[] arr) {
    List<Integer> leaders = new ArrayList<>();
    int maxFromRight = Integer.MIN_VALUE;
    for (int i = arr.length - 1; i >= 0; i--) {
        if (arr[i] > maxFromRight) {
            maxFromRight = arr[i];
            leaders.add(arr[i]);
        }
    }
    Collections.reverse(leaders);  // if you want original order
    return leaders;
}
```

**Key insight:** The naive approach double-counts work. By tracking the running maximum from the right, each element is examined once. You cannot solve this without at least O(n) because you must examine each element.

## Maximum Difference Problem (Buy/Sell Stock Basic)

**Problem:** Find max `arr[j] - arr[i]` where j > i. (Buy low, sell high — single transaction.)

### Naive: O(n²)

### Optimal: O(n) — track min so far

```java
public static int maxDifference(int[] arr) {
    int minSoFar = arr[0];
    int maxDiff = 0;
    for (int i = 1; i < arr.length; i++) {
        maxDiff = Math.max(maxDiff, arr[i] - minSoFar);
        minSoFar = Math.min(minSoFar, arr[i]);
    }
    return maxDiff;
}
```

**Variation:** Stock Buy and Sell II (multiple transactions) — just sum all positive gains: add up every `arr[i] - arr[i-1]` where the diff is positive.

## Common Pitfalls

1. **ArrayIndexOutOfBoundsException** — accessing arr[-1] or arr[length]. Always validate index.
2. **Null array** — declares but never initializes. `int[] arr = null; arr.length` → NPE.
3. **Confusing length vs length()** — arrays use `.length` (field), Strings use `.length()` (method).
4. **Reference aliasing** — `int[] b = a;` does NOT copy data. Both reference the same array. Use `clone()` or `System.arraycopy()` for actual copy.
5. **Enhanced for loop modification** — `for (int x : arr)` cannot modify the array elements. x is a copy.

## Quick Reference

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|-----------------|
| Access by index | O(1) | O(1) |
| Search (unsorted) | O(n) | O(1) |
| Insert at beginning | O(n) | O(n) if resize |
| Insert at end | O(1) amortized | O(1) |
| Insert at position | O(n) | O(1) |
| Delete at beginning | O(n) | O(1) |
| Delete at end | O(1) | O(1) |
| Reverse | O(n) | O(1) |
| Rotate (reversal) | O(n) | O(1) |
