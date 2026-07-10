# Two Pointers - The Basics

Hey there! Let's talk about one of the most elegant patterns in algorithms — the **Two Pointers** technique. If you've ever been in an interview and heard "can you do it in O(n) time and O(1) space?", two pointers is often the answer.

## What's the Big Idea?

Two pointers is exactly what it sounds like: we use two pointer variables (indices) to traverse an array, usually moving them strategically based on conditions. Instead of nested loops (O(n²)), we make a single pass (O(n)).

There are two main flavors:

### 1. Opposite Direction Pointers
One pointer starts at the **left** (index 0), the other at the **right** (index n-1). They move **towards each other** and typically meet somewhere in the middle.

```
Left →                      ← Right
 [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Use cases:**
- Finding pairs in a **sorted** array (Two Sum II)
- Checking if a string is a palindrome
- Reversing an array in-place
- Container with most water

### 2. Same Direction Pointers (Fast & Slow)
Both pointers start at the same end but move at **different speeds** or with different logic.

```
Fast →→→→→→→→→→
Slow →→→
 [1, 1, 2, 2, 3, 3, 4, 4, 5]
```

**Use cases:**
- Removing duplicates from a sorted array
- Partitioning arrays
- Linked list cycle detection
- Moving zeros to the end

## Complexity Analysis

| Aspect | Opposite Direction | Same Direction |
|--------|------------------|----------------|
| Time | O(n) | O(n) |
| Space | O(1) | O(1) |
| Requires sorted? | Usually yes | Usually no |

## Template: Opposite Direction

```java
public boolean twoSumSorted(int[] arr, int target) {
    int left = 0;
    int right = arr.length - 1;

    while (left < right) {
        int sum = arr[left] + arr[right];

        if (sum == target) {
            return true;
        } else if (sum < target) {
            left++;  // We need a bigger sum, move left forward
        } else {
            right--; // We need a smaller sum, move right backward
        }
    }
    return false;
}
```

## Template: Same Direction (Write Pointer)

```java
public int removeDuplicates(int[] arr) {
    if (arr.length == 0) return 0;

    int write = 0;  // Where to place the next unique element

    for (int read = 0; read < arr.length; read++) {
        if (arr[read] != arr[write]) {
            write++;
            arr[write] = arr[read];
        }
    }
    return write + 1; // Length of unique portion
}
```

## When Do You Use Two Pointers?

Here's your mental checklist:

1. **"Sorted array"** → probably opposite direction two pointers
2. **"In-place modification"** → probably same direction (write pointer)
3. **"Find a pair / triplet"** → sort first, then two pointers
4. **"Palindrome"** → opposite direction
5. **"Remove duplicates / partition"** → same direction
6. **"O(1) extra space"** → two pointers is calling your name

## Common Pitfalls

1. **Forgetting to sort** — opposite direction two pointers only works on *sorted* arrays. If your input isn't sorted, sort it first (or use a HashSet).
2. **Off-by-one on duplicates** — when removing duplicates, compare `arr[read]` with `arr[write]`, not `arr[write-1]`. Wait — actually in our template above, `arr[read]` is compared with `arr[write]` and we increment `write` afterward. Different variations exist; be careful!
3. **Infinite loops** — always make sure your pointers actually move. Every iteration should increment `left` or decrement `right`.
4. **Pointer collision condition** — most commonly `while (left < right)`. Using `<=` might double-count the middle element.

## The Mentality

Here's the mindset shift you need: when you see a brute force O(n²) solution (nested loops), ask yourself — can I replace one of those loops with a pointer that moves intelligently?

The nested loop checks *every* pair `(i, j)`. Two pointers eliminates pairs that can *never* work based on the sorted property and the current sum. That's the whole secret.

## More Patterns and Examples

### Opposite Direction: Palindrome Check

```java
public boolean isPalindrome(String s) {
    int left = 0;
    int right = s.length() - 1;

    while (left < right) {
        // Skip non-alphanumeric characters
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
            left++;
        }
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
            right--;
        }

        if (Character.toLowerCase(s.charAt(left)) !=
            Character.toLowerCase(s.charAt(right))) {
            return false;
        }

        left++;
        right--;
    }

    return true;
}
```

### Same Direction: Squaring a Sorted Array

Given a sorted array that may have negative numbers, return an array of squares in sorted order.

```java
public int[] sortedSquares(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    int left = 0;
    int right = n - 1;

    for (int i = n - 1; i >= 0; i--) {
        if (Math.abs(nums[left]) > Math.abs(nums[right])) {
            result[i] = nums[left] * nums[left];
            left++;
        } else {
            result[i] = nums[right] * nums[right];
            right--;
        }
    }

    return result;
}
```

This one's interesting — even though the array is sorted, the squares aren't (because negatives make larger squares). We use opposite-direction pointers to build the result from largest to smallest.

### Opposite Direction: Reverse an Array

```java
public void reverse(int[] arr) {
    int left = 0;
    int right = arr.length - 1;

    while (left < right) {
        int temp = arr[left];
        arr[left] = arr[right];
        arr[right] = temp;
        left++;
        right--;
    }
}
```

## Classification by Input Type

| Input | Pointer Type | Why |
|-------|-------------|-----|
| Sorted array | Opposite direction | Monotonic values let us decide which pointer to move |
| Unsorted array | Same direction (write ptr) | We're partitioning/filtering |
| LinkedList | Fast & slow | Can't go backward, need speed difference |
| String (palindrome) | Opposite direction | Symmetry check done from ends |

## Two Pointers vs Other Techniques

Sometimes a problem *looks* like two pointers but is better solved differently:

- **Two Sum (unsorted)** — use HashMap, not two pointers (sorting changes index requirements)
- **Longest substring without repeating** — sliding window (not exactly two pointers)
- **Find median of two sorted arrays** — binary search (not two pointers)

Two pointers is for when the *position* of the pointers and the *direction* of movement naturally lead to the solution. The trade-off is usually: sort (O(n log n)) + two pointers (O(n)) vs HashMap (O(n), more space).

## Common Edge Cases Checklist

```java
// Empty array
int[] empty = {};
// Single element
int[] single = {5};
// All same values
int[] allSame = {1, 1, 1, 1};
// Already sorted
int[] sorted = {1, 2, 3, 4, 5};
// Reverse sorted
int[] reverse = {5, 4, 3, 2, 1};
// With duplicates
int[] dupes = {1, 2, 2, 2, 3, 4, 4, 5};
```

Before writing code, think about these. Your interviewer will test edge cases.

## Practice Progression

1. **Two Sum II** (sorted) — simplest opposite-direction
2. **Remove duplicates** — simplest same-direction
3. **Container with most water** — opposite, maximization
4. **3Sum** — three pointers (two nested + one two-pointer)
5. **Trapping rain water** — opposite with tracking maxima
6. **Dutch National Flag** — three-way partitioning

Each builds on the previous. Get comfortable with the basics here, then crush the harder problems.

Let's get into the specific problems now and see this pattern in action! 🚀
