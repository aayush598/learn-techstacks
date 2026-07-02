# Beginner 30 — Easy Difficulty Problems

> Master these before moving to intermediate. Each problem reinforces one core data structure or pattern.

---

## How to Use This List

- Solve in any order, but **Arrays → Strings → Recursion → Linked List → Stacks** is recommended
- Time yourself using the estimated times
- After solving, review the **pattern** and **complexity** — don't just pass
- Re-solve after 24h, 7d, and 30d for spaced repetition

---

## Arrays (10 problems)

### 1. Two Sum

| Property | Value |
|---|---|
| **Topic** | Array, HashMap |
| **Pattern** | Complementation |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 1](https://leetcode.com/problems/two-sum/) |
| **Difficulty** | Easy |

**Description:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`.

**Approach Hint:** Use a HashMap to store `(value → index)`. For each element, check if `target - nums[i]` exists in the map.

**Time:** O(n) | **Space:** O(n)

**Java Solution Approach:**
```java
HashMap<Integer, Integer> map = new HashMap<>();
for (int i = 0; i < nums.length; i++) {
    int complement = target - nums[i];
    if (map.containsKey(complement))
        return new int[]{map.get(complement), i};
    map.put(nums[i], i);
}
```

---

### 2. Best Time to Buy and Sell Stock

| Property | Value |
|---|---|
| **Topic** | Array |
| **Pattern** | Sliding Window / Kadane |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) |
| **Difficulty** | Easy |

**Description:** Given prices array, find max profit from one buy + one sell.

**Approach Hint:** Track `minPriceSoFar` and `maxProfit`. At each price, compute potential profit.

**Time:** O(n) | **Space:** O(1)

**Java Solution Approach:**
```java
int minPrice = Integer.MAX_VALUE, maxProfit = 0;
for (int price : prices) {
    if (price < minPrice) minPrice = price;
    else if (price - minPrice > maxProfit) maxProfit = price - minPrice;
}
return maxProfit;
```

---

### 3. Contains Duplicate

| Property | Value |
|---|---|
| **Topic** | Array, HashSet |
| **Pattern** | Hashing |
| **Est. Time** | 5 min |
| **Platform** | [LeetCode 217](https://leetcode.com/problems/contains-duplicate/) |
| **Difficulty** | Easy |

**Description:** Return true if any value appears at least twice in the array.

**Approach Hint:** Use a HashSet. If add() returns false, a duplicate exists.

**Time:** O(n) | **Space:** O(n)

---

### 4. Move Zeroes

| Property | Value |
|---|---|
| **Topic** | Array, Two Pointer |
| **Pattern** | Partitioning |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 283](https://leetcode.com/problems/move-zeroes/) |
| **Difficulty** | Easy |

**Description:** Move all zeroes to the end while maintaining relative order of non-zero elements (in-place).

**Approach Hint:** Use a `nonZeroIndex` pointer. Iterate; when non-zero found, swap with `nonZeroIndex` and increment.

**Time:** O(n) | **Space:** O(1)

---

### 5. Remove Duplicates from Sorted Array

| Property | Value |
|---|---|
| **Topic** | Array, Two Pointer |
| **Pattern** | In-place modification |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) |
| **Difficulty** | Easy |

**Description:** Remove duplicates in-place from sorted array and return new length.

**Approach Hint:** Use two pointers — `i` (slow) and `j` (fast). When `nums[j] != nums[i]`, increment `i` and copy.

**Time:** O(n) | **Space:** O(1)

---

### 6. Find Missing Number

| Property | Value |
|---|---|
| **Topic** | Array, Math |
| **Pattern** | Summation / XOR |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 268](https://leetcode.com/problems/missing-number/) |
| **Difficulty** | Easy |

**Description:** Given `n` numbers from `0..n` with one missing, find the missing one.

**Approach Hint:** Use XOR (a ^ a = 0) or sum formula: `expected - actual`.

**Time:** O(n) | **Space:** O(1)

---

### 7. Intersection of Two Arrays II

| Property | Value |
|---|---|
| **Topic** | Array, HashMap |
| **Pattern** | Frequency counting |
| **Est. Time** | 12 min |
| **Platform** | [LeetCode 350](https://leetcode.com/problems/intersection-of-two-arrays-ii/) |
| **Difficulty** | Easy |

**Description:** Return intersection of two arrays (with duplicates).

**Approach Hint:** Count frequencies of smaller array in HashMap, then iterate second array decrementing counts.

**Time:** O(n + m) | **Space:** O(min(n, m))

---

### 8. Plus One

| Property | Value |
|---|---|
| **Topic** | Array, Math |
| **Pattern** | Digit manipulation |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 66](https://leetcode.com/problems/plus-one/) |
| **Difficulty** | Easy |

**Description:** Given a large integer as an array of digits, add one.

**Approach Hint:** Iterate from end. If digit < 9, increment and return. Else set to 0 and carry. Handle edge case of all 9s.

**Time:** O(n) | **Space:** O(1) or O(n) for carry overflow

---

### 9. Majority Element

| Property | Value |
|---|---|
| **Topic** | Array, Voting |
| **Pattern** | Boyer-Moore Majority Vote |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 169](https://leetcode.com/problems/majority-element/) |
| **Difficulty** | Easy |

**Description:** Find element that appears more than ⌊n/2⌋ times.

**Approach Hint:** Boyer-Moore: maintain a candidate and count. When count hits 0, pick new candidate.

**Time:** O(n) | **Space:** O(1)

---

### 10. Find Pivot Index

| Property | Value |
|---|---|
| **Topic** | Array, Prefix Sum |
| **Pattern** | Prefix sum |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 724](https://leetcode.com/problems/find-pivot-index/) |
| **Difficulty** | Easy |

**Description:** Find the index where left sum equals right sum.

**Approach Hint:** Compute total sum. Iterate maintaining left sum, check if `left == total - left - nums[i]`.

**Time:** O(n) | **Space:** O(1)

---

## Strings (5 problems)

### 11. Valid Anagram

| Property | Value |
|---|---|
| **Topic** | String, HashMap |
| **Pattern** | Frequency counting |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 242](https://leetcode.com/problems/valid-anagram/) |
| **Difficulty** | Easy |

**Description:** Given two strings, determine if they are anagrams.

**Approach Hint:** Count char frequencies in an array of size 26. Increment for s, decrement for t.

**Time:** O(n) | **Space:** O(1)

---

### 12. First Unique Character in a String

| Property | Value |
|---|---|
| **Topic** | String, HashMap |
| **Pattern** | Frequency counting |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 387](https://leetcode.com/problems/first-unique-character-in-a-string/) |
| **Difficulty** | Easy |

**Description:** Find the first non-repeating character and return its index.

**Approach Hint:** Two passes: first count frequencies, second find first char with count 1.

**Time:** O(n) | **Space:** O(1)

---

### 13. Reverse String

| Property | Value |
|---|---|
| **Topic** | String, Two Pointer |
| **Pattern** | In-place swap |
| **Est. Time** | 5 min |
| **Platform** | [LeetCode 344](https://leetcode.com/problems/reverse-string/) |
| **Difficulty** | Easy |

**Description:** Reverse a character array in-place.

**Approach Hint:** Two pointers — left and right — swap and move inward.

**Time:** O(n) | **Space:** O(1)

---

### 14. Valid Palindrome

| Property | Value |
|---|---|
| **Topic** | String, Two Pointer |
| **Pattern** | Palindrome check |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 125](https://leetcode.com/problems/valid-palindrome/) |
| **Difficulty** | Easy |

**Description:** Check if string is a palindrome considering only alphanumeric characters and ignoring case.

**Approach Hint:** Two pointers. Skip non-alphanumeric using `Character.isLetterOrDigit()`.

**Time:** O(n) | **Space:** O(1)

---

### 15. Longest Common Prefix

| Property | Value |
|---|---|
| **Topic** | String |
| **Pattern** | Horizontal scanning |
| **Est. Time** | 12 min |
| **Platform** | [LeetCode 14](https://leetcode.com/problems/longest-common-prefix/) |
| **Difficulty** | Easy |

**Description:** Find the longest common prefix string among an array of strings.

**Approach Hint:** Start with first string as prefix. Iterate rest, shrinking prefix until it matches.

**Time:** O(S) where S = sum of all characters | **Space:** O(1)

---

## Recursion (5 problems)

### 16. Fibonacci Number

| Property | Value |
|---|---|
| **Topic** | Recursion |
| **Pattern** | Tree recursion |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 509](https://leetcode.com/problems/fibonacci-number/) |
| **Difficulty** | Easy |

**Description:** Return the nth Fibonacci number.

**Approach Hint:** Base: `n <= 1` return n. Recurse: `fib(n-1) + fib(n-2)`. Note: use memoization or iterative for O(n).

**Time:** O(2^n) naive, O(n) memoized | **Space:** O(n)

---

### 17. Factorial

| Property | Value |
|---|---|
| **Topic** | Recursion |
| **Pattern** | Linear recursion |
| **Est. Time** | 5 min |
| **Platform** | [GeeksforGeeks](https://www.geeksforgeeks.org/program-for-factorial-of-a-number/) |
| **Difficulty** | Easy |

**Description:** Compute factorial of n.

**Approach Hint:** Base: `n <= 1` return 1. Recurse: `n * fact(n - 1)`.

**Time:** O(n) | **Space:** O(n) call stack

---

### 18. Sum of Digits

| Property | Value |
|---|---|
| **Topic** | Recursion |
| **Pattern** | Digit recursion |
| **Est. Time** | 5 min |
| **Platform** | [GeeksforGeeks](https://www.geeksforgeeks.org/sum-digit-number-using-recursion/) |
| **Difficulty** | Easy |

**Description:** Given a number, find sum of its digits using recursion.

**Approach Hint:** Base: `n == 0` return 0. Recurse: `n % 10 + sumDigits(n / 10)`.

**Time:** O(log n) | **Space:** O(log n)

---

### 19. Power of Two

| Property | Value |
|---|---|
| **Topic** | Recursion |
| **Pattern** | Divide and conquer |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 231](https://leetcode.com/problems/power-of-two/) |
| **Difficulty** | Easy |

**Description:** Given integer n, return true if it is a power of two.

**Approach Hint:** Base: `n == 1` return true. If `n % 2 != 0` return false. Recurse: `isPowerOfTwo(n / 2)`.

**Time:** O(log n) | **Space:** O(log n)

---

### 20. Print 1 to N Without Loops

| Property | Value |
|---|---|
| **Topic** | Recursion |
| **Pattern** | Tail recursion |
| **Est. Time** | 5 min |
| **Platform** | [GeeksforGeeks](https://www.geeksforgeeks.org/print-1-to-n-without-using-loops/) |
| **Difficulty** | Easy |

**Description:** Print numbers from 1 to N without using any loops.

**Approach Hint:** Base case: `n < 1` return. Recurse: `print(n - 1)`, then print `n`.

**Time:** O(n) | **Space:** O(n)

---

## Linked List (5 problems)

### 21. Reverse Linked List

| Property | Value |
|---|---|
| **Topic** | Linked List |
| **Pattern** | Iterative / Recursive reversal |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 206](https://leetcode.com/problems/reverse-linked-list/) |
| **Difficulty** | Easy |

**Description:** Reverse a singly linked list.

**Approach Hint:** Iterative: `prev = null, curr = head`. Save `next`, point `curr.next = prev`, advance. Recursive: `head.next.next = head; head.next = null`.

**Time:** O(n) | **Space:** O(1) iterative, O(n) recursive

---

### 22. Middle of the Linked List

| Property | Value |
|---|---|
| **Topic** | Linked List |
| **Pattern** | Slow & Fast Pointer |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 876](https://leetcode.com/problems/middle-of-the-linked-list/) |
| **Difficulty** | Easy |

**Description:** Return the middle node of a linked list.

**Approach Hint:** Slow pointer moves 1 step, fast pointer moves 2 steps. When fast reaches end, slow is at middle.

**Time:** O(n) | **Space:** O(1)

---

### 23. Merge Two Sorted Lists

| Property | Value |
|---|---|
| **Topic** | Linked List |
| **Pattern** | Two-pointer merge |
| **Est. Time** | 12 min |
| **Platform** | [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/) |
| **Difficulty** | Easy |

**Description:** Merge two sorted linked lists into one sorted list.

**Approach Hint:** Dummy head node. Compare `l1.val` and `l2.val`, attach the smaller, advance. Handle remaining.

**Time:** O(n + m) | **Space:** O(1)

---

### 24. Remove Duplicates from Sorted List

| Property | Value |
|---|---|
| **Topic** | Linked List |
| **Pattern** | Sequential traversal |
| **Est. Time** | 8 min |
| **Platform** | [LeetCode 83](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) |
| **Difficulty** | Easy |

**Description:** Remove duplicates from a sorted linked list.

**Approach Hint:** If `curr.val == curr.next.val`, skip `curr.next`. Else advance.

**Time:** O(n) | **Space:** O(1)

---

### 25. Linked List Cycle Detection

| Property | Value |
|---|---|
| **Topic** | Linked List |
| **Pattern** | Floyd's Cycle Detection |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/) |
| **Difficulty** | Easy |

**Description:** Determine if a linked list has a cycle.

**Approach Hint:** Fast and slow pointers. If they meet, there's a cycle.

**Time:** O(n) | **Space:** O(1)

---

## Stacks (5 problems)

### 26. Valid Parentheses

| Property | Value |
|---|---|
| **Topic** | Stack |
| **Pattern** | Matching parentheses |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 20](https://leetcode.com/problems/valid-parentheses/) |
| **Difficulty** | Easy |

**Description:** Given string of `(){}[]`, determine if valid.

**Approach Hint:** Push opening brackets onto stack. When closing bracket encountered, check if stack top matches.

**Time:** O(n) | **Space:** O(n)

---

### 27. Min Stack

| Property | Value |
|---|---|
| **Topic** | Stack, Design |
| **Pattern** | Auxiliary stack |
| **Est. Time** | 12 min |
| **Platform** | [LeetCode 155](https://leetcode.com/problems/min-stack/) |
| **Difficulty** | Easy |

**Description:** Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

**Approach Hint:** Use two stacks — main and minStack. Push: push value + push min(value, minStack.top()).

**Time:** O(1) per operation | **Space:** O(n)

---

### 28. Implement Queue using Stacks

| Property | Value |
|---|---|
| **Topic** | Stack, Queue |
| **Pattern** | Two-stack queue |
| **Est. Time** | 12 min |
| **Platform** | [LeetCode 232](https://leetcode.com/problems/implement-queue-using-stacks/) |
| **Difficulty** | Easy |

**Description:** Implement a FIFO queue using only two stacks.

**Approach Hint:** Use `pushStack` and `popStack`. When popping, if popStack is empty, transfer all from pushStack to popStack.

**Time:** O(1) amortized per operation | **Space:** O(n)

---

### 29. Next Greater Element I

| Property | Value |
|---|---|
| **Topic** | Stack, HashMap |
| **Pattern** | Monotonic stack |
| **Est. Time** | 12 min |
| **Platform** | [LeetCode 496](https://leetcode.com/problems/next-greater-element-i/) |
| **Difficulty** | Easy |

**Description:** For each element in `nums1`, find its next greater element in `nums2`.

**Approach Hint:** Use monotonic decreasing stack on `nums2`. For each popped element, the next greater is the current element. Store in map.

**Time:** O(n + m) | **Space:** O(n)

---

### 30. Baseball Game

| Property | Value |
|---|---|
| **Topic** | Stack |
| **Pattern** | Operation simulation |
| **Est. Time** | 10 min |
| **Platform** | [LeetCode 682](https://leetcode.com/problems/baseball-game/) |
| **Difficulty** | Easy |

**Description:** You are keeping score for a baseball game. Operations: integer (add), `+` (sum of last two), `D` (double last), `C` (remove last).

**Approach Hint:** Use a stack (or ArrayList as stack). Apply each operation.

**Time:** O(n) | **Space:** O(n)

---

## Quick Reference Table

| # | Problem | Topic | Pattern | Time | Space |
|---|---|---|---|---|---|
| 1 | Two Sum | Array | HashMap | O(n) | O(n) |
| 2 | Buy & Sell Stock | Array | Sliding Window | O(n) | O(1) |
| 3 | Contains Duplicate | Array | HashSet | O(n) | O(n) |
| 4 | Move Zeroes | Array | Two Pointer | O(n) | O(1) |
| 5 | Remove Duplicates | Array | Two Pointer | O(n) | O(1) |
| 6 | Missing Number | Array | XOR/Sum | O(n) | O(1) |
| 7 | Intersection II | Array | HashMap | O(n+m) | O(min) |
| 8 | Plus One | Array | Math | O(n) | O(1) |
| 9 | Majority Element | Array | Boyer-Moore | O(n) | O(1) |
| 10 | Pivot Index | Array | Prefix Sum | O(n) | O(1) |
| 11 | Valid Anagram | String | Freq Count | O(n) | O(1) |
| 12 | First Unique Char | String | Freq Count | O(n) | O(1) |
| 13 | Reverse String | String | Two Pointer | O(n) | O(1) |
| 14 | Valid Palindrome | String | Two Pointer | O(n) | O(1) |
| 15 | Longest Common Prefix | String | Scanning | O(S) | O(1) |
| 16 | Fibonacci | Recursion | Tree Rec | O(2^n) | O(n) |
| 17 | Factorial | Recursion | Linear | O(n) | O(n) |
| 18 | Sum of Digits | Recursion | Digit | O(log n) | O(log n) |
| 19 | Power of Two | Recursion | Divide | O(log n) | O(log n) |
| 20 | Print 1 to N | Recursion | Tail | O(n) | O(n) |
| 21 | Reverse LL | LinkedList | Reverse | O(n) | O(1) |
| 22 | Middle of LL | LinkedList | Fast/Slow | O(n) | O(1) |
| 23 | Merge Sorted Lists | LinkedList | Merge | O(n+m) | O(1) |
| 24 | Remove Duplicates LL | LinkedList | Traversal | O(n) | O(1) |
| 25 | Cycle Detection | LinkedList | Floyd | O(n) | O(1) |
| 26 | Valid Parentheses | Stack | Matching | O(n) | O(n) |
| 27 | Min Stack | Stack | Design | O(1) | O(n) |
| 28 | Queue using Stacks | Stack | Design | O(1)* | O(n) |
| 29 | Next Greater I | Stack | Monotonic | O(n+m) | O(n) |
| 30 | Baseball Game | Stack | Simulation | O(n) | O(n) |

*amortized

---

## Tips for Beginners

1. **Don't look at solutions immediately** — struggle for at least 20-30 minutes
2. **Draw it out** — use paper/whiteboard for every problem
3. **Start with brute force** — then optimize
4. **Write tests** — edge cases: empty, single element, negatives
5. **Review after solving** — read LeetCode discuss for alternative solutions
6. **Teach someone** — explaining solidifies understanding
7. **Use debugger** — step through your code to understand the flow
8. **Time yourself** — build awareness of pacing
9. **Solve variations** — e.g., after Two Sum, try Three Sum, Four Sum
10. **Track progress** — maintain a spreadsheet (see `03_performance_tracking/`)
