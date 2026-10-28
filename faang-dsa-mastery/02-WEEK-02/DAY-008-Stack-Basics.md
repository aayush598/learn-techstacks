# DAY-008 | PATTERN FOCUS: Stack Basics | TARGET: 1H + 2M + 3E

> **Objective:** Master LIFO, push/pop/peek, ArrayDeque as stack.

---

## 1) EASY-1 | Valid Parentheses | Leetcode 20

### Problem
Check valid parentheses string.

### Approach
Stack, push opening, pop on matching closing.

### Java Solution
```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if ((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) return false;
            }
        }
        return stack.isEmpty();
    }
}
```
**TC:** O(n) | **SC:** O(n)

### Similar
1. Leetcode 921 - Minimum Add to Make Parentheses Valid
2. Leetcode 1021 - Remove Outermost Parentheses
3. Leetcode 1249 - Minimum Remove to Make Valid Parentheses

---

## 2) EASY-2 | Implement Stack using Queues | Leetcode 225
Understand design.

### Java Solution
```java
import java.util.LinkedList;
import java.util.Queue;

class MyStack {
    Queue<Integer> q1 = new LinkedList<>();
    Queue<Integer> q2 = new LinkedList<>();
    public MyStack() {}
    public void push(int x) {
        q2.offer(x);
        while (!q1.isEmpty()) q2.offer(q1.poll());
        Queue<Integer> temp = q1; q1 = q2; q2 = temp;
    }
    public int pop() { return q1.poll(); }
    public int top() { return q1.peek(); }
    public boolean empty() { return q1.isEmpty(); }
}
```

---

## 3) EASY-3 | Next Greater Element I | Leetcode 496

### Problem
Find next greater element for each element in nums1 in terms of nums2.

### Approach
Stack from right to left on nums2, map value->next greater.

### Java Solution
```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> map = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = nums2.length - 1; i >= 0; i--) {
            while (!stack.isEmpty() && stack.peek() <= nums2[i]) stack.pop();
            if (stack.isEmpty()) map.put(nums2[i], -1);
            else map.put(nums2[i], stack.peek());
            stack.push(nums2[i]);
        }
        int[] res = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) res[i] = map.get(nums1[i]);
        return res;
    }
}
```
**TC:** O(m+n) | **SC:** O(m+n)

### Similar
1. Leetcode 503 - Next Greater Element II
2. Leetcode 739 - Daily Temperatures
3. Leetcode 42 context

---

## 4) MEDIUM-1 | Daily Temperatures | Leetcode 739

### Problem
Days to wait for warmer temperature.

### Approach
Monotonic stack decreasing.

### Java Solution
```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int[] res = new int[temperatures.length];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = temperatures.length - 1; i >= 0; i--) {
            while (!stack.isEmpty() && temperatures[stack.peek()] <= temperatures[i]) stack.pop();
            if (stack.isEmpty()) res[i] = 0;
            else res[i] = stack.peek() - i;
            stack.push(i);
        }
        return res;
    }
}
```
**TC:** O(n) | **SC:** O(n)

### Similar
1. Leetcode 496
2. Leetcode 503
3. Leetcode 901 - Online Stock Span

---

## 5) MEDIUM-2 | Remove All Adjacent Duplicates In String | Leetcode 1047

### Problem
Remove duplicates adjacent until no more.

### Approach
Stack, push if different else pop.

### Java Solution
```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public String removeDuplicates(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (!stack.isEmpty() && stack.peek() == c) stack.pop();
            else stack.push(c);
        }
        StringBuilder sb = new StringBuilder();
        while (!stack.isEmpty()) sb.append(stack.pollLast());
        return sb.toString();
    }
}
```
**TC:** O(n) | **SC:** O(n)

### Similar
1. Leetcode 1209 - Remove All Adjacent Duplicates in String II
2. Leetcode 1047
3. Leetcode 844 - Backspace String Compare

---

## 6) HARD-1 | Largest Rectangle in Histogram | Leetcode 84

### Problem
Largest rectangle area in histogram.

### Approach
Monotonic stack to find previous less and next less element.

### Java Solution
```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && heights[stack.peek()] >= heights[i]) stack.pop();
            if (stack.isEmpty()) left[i] = 0;
            else left[i] = stack.peek() + 1;
            stack.push(i);
        }
        stack.clear();
        for (int i = n - 1; i >= 0; i--) {
            while (!stack.isEmpty() && heights[stack.peek()] >= heights[i]) stack.pop();
            if (stack.isEmpty()) right[i] = n - 1;
            else right[i] = stack.peek() - 1;
            stack.push(i);
        }
        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            maxArea = Math.max(maxArea, heights[i] * (right[i] - left[i] + 1));
        }
        return maxArea;
    }
}
```
**TC:** O(n) | **SC:** O(n)

### Similar
1. Leetcode 85 - Maximal Rectangle
2. Leetcode 42
3. Leetcode 84

---

## END OF DAY REVIEW
- **Learned:** Stack patterns, monotonic stack
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
