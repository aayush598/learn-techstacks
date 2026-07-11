# Anki Card Templates

## Template 1: Concept Card

**Front**: 
```
Kadane's Algorithm
```

**Back**:
```
Purpose: Find maximum subarray sum
Approach: Carry forward positive sum, reset at negative
Pattern: Prefix sum variant
Time: O(n) | Space: O(1)
Code:
  int maxSoFar = nums[0], maxEnding = nums[0];
  for (int i=1; i<n; i++) {
      maxEnding = Math.max(nums[i], maxEnding + nums[i]);
      maxSoFar = Math.max(maxSoFar, maxEnding);
  }
  return maxSoFar;
When to use: Maximum subarray, best time to buy stock (variants)
```

## Template 2: Problem Card

**Front**:
```
Longest Substring Without Repeating Characters
Given "abcabcbb", find length of longest substring without repeating chars.
```

**Back**:
```
Pattern: Sliding Window (variable size)
Data Structure: HashMap<Character, Integer> (char → last index)
Approach:
  1. left = 0, maxLen = 0
  2. For right = 0..n-1:
     - If char exists in map: left = max(left, map.get(char) + 1)
     - Update map: map.put(char, right)
     - maxLen = max(maxLen, right - left + 1)
  3. Return maxLen
Time: O(n) | Space: O(min(m,n)) where m = charset size
Edge cases: empty string, single char, all unique, all same
```

## 20 Example Cards

### Array Cards
1. **Two Sum**: HashMap, O(n), store complement
2. **Max Subarray**: Kadane's, O(n), carry forward
3. **Product Except Self**: Prefix+Suffix, O(n) without division
4. **Rotate Array**: Reverse whole → reverse parts

### String Cards
5. **Valid Anagram**: Frequency array int[26]
6. **Longest Palindrome**: Count pairs of chars
7. **String Compression**: Two pointers, count runs

### Linked List Cards
8. **Reverse Linked List**: Three pointers (prev, curr, next)
9. **Cycle Detection**: Fast/slow pointers (Floyd's)
10. **Merge Two Sorted**: Dummy node + pointers

### Tree Cards
11. **Max Depth**: DFS recursion or BFS level order
12. **Validate BST**: Range [min, max] per node
13. **Level Order**: Queue, process level by level

### DP Cards
14. **Climbing Stairs**: dp[n] = dp[n-1] + dp[n-2]
15. **House Robber**: dp[i] = max(dp[i-1], dp[i-2]+nums[i])
16. **Coin Change**: dp[i] = min(dp[i-coin]+1)

### Graph Cards
17. **Number of Islands**: DFS for each '1', mark visited
18. **Course Schedule**: Topological sort, detect cycle
19. **Clone Graph**: HashMap<Node, Node>, DFS

### Misc
20. **Binary Search**: while(l<=r), mid = l+(r-l)/2
