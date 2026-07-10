# Infosys — HackWithInfy & Campus Recruitment

> "Infosys is where many Indian developers begin their careers. HackWithInfy is your golden ticket to skip the queue — use it wisely."

---

## 1. Infosys Hiring Paths

### HackWithInfy
- **What:** Annual coding competition for pre-final and final year students
- **Format:** 3 problems in 3 hours (online round)
- **Prizes:** Top performers get direct offers for **Power Programmer** role (₹6.5 LPA+)
- **Rounds:** Online → Interview (2 rounds: Technical + HR)
- **Difficulty:** Easy to Medium (LeetCode Easy-Medium level)
- **Key Insight:** Completing all 3 problems correctly matters more than speed

### DSE — Digital Specialist Engineer
- **What:** Campus hiring for specialized digital roles
- **Package:** ~₹5 LPA base + bonuses
- **Focus:** Stronger coding + domain knowledge
- **Process:** Online Assessment → Technical Interview → HR

### SES — Systems Engineer Specialist
- **What:** Premium campus role (higher package than regular SE)
- **Package:** ~₹4.5 LPA base
- **Process:** Similar to DSE but slightly easier coding round
- **Focus:** Clean code, good CS fundamentals

---

## 2. Most Asked Topics (Priority Order)

| Priority | Topic | Frequency | Difficulty |
|----------|-------|-----------|------------|
| 1 | Arrays | 90% | Easy-Medium |
| 2 | Strings | 85% | Easy |
| 3 | HashMap/HashSet | 70% | Easy |
| 4 | Basic DP | 50% | Easy-Medium |
| 5 | Greedy | 40% | Easy-Medium |
| 6 | Math/Number Theory | 35% | Easy |
| 7 | Sorting | 30% | Easy |

**Key Pattern:** Infosys rarely asks Trees/Graphs in coding rounds. Focus on arrays and strings.

---

## 3. Coding Round Format (HackWithInfy)

```
┌─────────────────────────────────────────────┐
│  Problem 1: Easy (50 points) — 30-45 min    │
│  Problem 2: Easy-Medium (100 points) — 45-60 min │
│  Problem 3: Medium (150 points) — 60-75 min │
│  Total Time: 180 minutes                     │
│  Language: Java preferred (school setting)   │
└─────────────────────────────────────────────┘
```

### Time Management Strategy
1. **Minutes 0-5:** Read all three problems
2. **Minutes 5-45:** Solve Problem 1 completely (easy warm-up)
3. **Minutes 45-110:** Solve Problem 2 (the medium one)
4. **Minutes 110-170:** Attempt Problem 3 (hardest, partial credit possible)
5. **Minutes 170-180:** Review and fix edge cases

> **Pro Tip:** Even partial solutions for Problem 3 can boost your rank. Don't leave it blank.

---

## 4. Core Problem Categories & Solutions

### Category 1: Subarray Problems (Most Frequent!)

#### Problem: Subarray Sum Equals K
**Pattern:** Prefix Sum + HashMap

```java
import java.util.*;

public class SubarraySumEqualsK {
    
    // APPROACH: Prefix sum with frequency counting
    // If prefixSum[j] - prefixSum[i] == k, then subarray (i, j] has sum k
    // We use HashMap to store frequency of prefix sums seen so far
    
    public static int subarraySum(int[] nums, int k) {
        // HashMap: prefix_sum → frequency of that prefix sum
        Map<Integer, Integer> prefixSumCount = new HashMap<>();
        prefixSumCount.put(0, 1); // Empty prefix has sum 0
        
        int currentSum = 0;
        int count = 0;
        
        for (int num : nums) {
            currentSum += num;
            
            // If (currentSum - k) was seen before, those subarrays sum to k
            if (prefixSumCount.containsKey(currentSum - k)) {
                count += prefixSumCount.get(currentSum - k);
            }
            
            // Record this prefix sum
            prefixSumCount.put(currentSum, prefixSumCount.getOrDefault(currentSum, 0) + 1);
        }
        
        return count;
    }
    
    public static void main(String[] args) {
        int[] nums = {1, 2, 3, -3, 2, 1, -1};
        int k = 3;
        System.out.println("Count of subarrays with sum " + k + ": " + subarraySum(nums, k));
        // Output: 4 (subarrays: [1,2], [1,2,3,-3], [3], [2,1])
        
        // Edge case: all zeros
        int[] zeros = {0, 0, 0};
        System.out.println("Count: " + subarraySum(zeros, 0));
        // Output: 6 (all possible subarrays)
    }
}
```

**Time:** O(n) | **Space:** O(n)
**Why Infosys loves this:** Tests HashMap usage + prefix sum concept — two birds, one stone.

---

#### Problem: Kadane's Algorithm — Maximum Subarray Sum
**Pattern:** Dynamic Programming / Greedy

```java
public class KadaneMaxSubarray {
    
    // CORE IDEA: At each position, decide:
    // Should I extend the current subarray, or start a new one?
    // dp[i] = max(nums[i], dp[i-1] + nums[i])
    
    public static int maxSubarraySum(int[] nums) {
        int currentMax = nums[0];
        int globalMax = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            // Either extend previous subarray or start fresh
            currentMax = Math.max(nums[i], currentMax + nums[i]);
            globalMax = Math.max(globalMax, currentMax);
        }
        
        return globalMax;
    }
    
    // VARIANT: Return the subarray indices too
    public static int[] maxSubarrayWithIndices(int[] nums) {
        int currentMax = nums[0];
        int globalMax = nums[0];
        int start = 0, end = 0, tempStart = 0;
        
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > currentMax + nums[i]) {
                currentMax = nums[i];
                tempStart = i; // New subarray starts here
            } else {
                currentMax += nums[i];
            }
            
            if (currentMax > globalMax) {
                globalMax = currentMax;
                start = tempStart;
                end = i;
            }
        }
        
        return new int[]{globalMax, start, end};
    }
    
    public static void main(String[] args) {
        int[] arr1 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Max Sum: " + maxSubarraySum(arr1)); // 6
        
        int[] arr2 = {-1, -2, -3, -4}; // All negative
        System.out.println("Max Sum: " + maxSubarraySum(arr2)); // -1
        
        int[] result = maxSubarrayWithIndices(arr1);
        System.out.println("Max Sum: " + result[0] + ", Indices: [" + result[1] + ", " + result[2] + "]");
        // Max Sum: 6, Indices: [3, 6]
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

#### Problem: Rotate Array by K Positions
**Pattern:** Three-Step Reversal

```java
public class RotateArray {
    
    // BRILLIANT TRICK: Rotate in three steps
    // Example: [1,2,3,4,5,6,7], k=3
    // Step 1: Reverse entire array → [7,6,5,4,3,2,1]
    // Step 2: Reverse first k=3 → [5,6,7,4,3,2,1]
    // Step 3: Reverse remaining → [5,6,7,1,2,3,4] ✓
    
    public static void rotate(int[] nums, int k) {
        int n = nums.length;
        k = k % n; // Handle k > n
        if (k == 0) return;
        
        reverse(nums, 0, n - 1);      // Full reverse
        reverse(nums, 0, k - 1);       // Reverse first k
        reverse(nums, k, n - 1);       // Reverse rest
    }
    
    private static void reverse(int[] nums, int start, int end) {
        while (start < end) {
            int temp = nums[start];
            nums[start] = nums[end];
            nums[end] = temp;
            start++;
            end--;
        }
    }
    
    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4, 5, 6, 7};
        rotate(nums, 3);
        System.out.println(java.util.Arrays.toString(nums)); // [5, 6, 7, 1, 2, 3, 4]
        
        int[] nums2 = {-1, -100, 3, 99};
        rotate(nums2, 2);
        System.out.println(java.util.Arrays.toString(nums2)); // [3, 99, -1, -100]
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Category 2: String Problems

#### Problem: Longest Common Prefix
**Pattern:** Vertical scanning / Sorting

```java
public class LongestCommonPrefix {
    
    // APPROACH: Sort strings, compare first and last (they'll be most different)
    public static String longestCommonPrefixSorting(String[] strs) {
        if (strs == null || strs.length == 0) return "";
        
        java.util.Arrays.sort(strs);
        String first = strs[0];
        String last = strs[strs.length - 1];
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < first.length(); i++) {
            if (i < last.length() && first.charAt(i) == last.charAt(i)) {
                sb.append(first.charAt(i));
            } else {
                break;
            }
        }
        return sb.toString();
    }
    
    // APPROACH: Vertical scanning (more intuitive)
    public static String longestCommonPrefixVertical(String[] strs) {
        if (strs == null || strs.length == 0) return "";
        
        // Use first string as reference
        for (int i = 0; i < strs[0].length(); i++) {
            char c = strs[0].charAt(i);
            for (int j = 1; j < strs.length; j++) {
                // If index out of bounds OR characters don't match
                if (i >= strs[j].length() || strs[j].charAt(i) != c) {
                    return strs[0].substring(0, i);
                }
            }
        }
        return strs[0]; // First string itself is the prefix
    }
    
    public static void main(String[] args) {
        String[] strs1 = {"flower", "flow", "flight"};
        System.out.println("LCP: " + longestCommonPrefixVertical(strs1)); // "fl"
        
        String[] strs2 = {"dog", "racecar", "car"};
        System.out.println("LCP: " + longestCommonPrefixVertical(strs2)); // ""
        
        String[] strs3 = {"a"};
        System.out.println("LCP: " + longestCommonPrefixVertical(strs3)); // "a"
    }
}
```

**Time:** O(S) where S = sum of all characters | **Space:** O(1)

---

#### Problem: Check if Two Strings are Anagrams
**Pattern:** Frequency Counting

```java
public class AnagramCheck {
    
    // APPROACH 1: Frequency array (26 chars)
    public static boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        
        int[] freq = new int[26];
        
        for (int i = 0; i < s.length(); i++) {
            freq[s.charAt(i) - 'a']++;
            freq[t.charAt(i) - 'a']--;
        }
        
        // If all frequencies are 0, it's an anagram
        for (int f : freq) {
            if (f != 0) return false;
        }
        return true;
    }
    
    // APPROACH 2: HashMap (handles Unicode)
    public static boolean isAnagramHashMap(String s, String t) {
        if (s.length() != t.length()) return false;
        
        Map<Character, Integer> map = new HashMap<>();
        
        for (char c : s.toCharArray()) {
            map.merge(c, 1, Integer::sum);
        }
        
        for (char c : t.toCharArray()) {
            map.merge(c, -1, Integer::sum);
            if (map.get(c) == 0) map.remove(c);
        }
        
        return map.isEmpty();
    }
    
    public static void main(String[] args) {
        System.out.println(isAnagram("anagram", "nagaram"));  // true
        System.out.println(isAnagram("rat", "car"));           // false
        System.out.println(isAnagram("aacc", "ccac"));         // false
    }
}
```

**Time:** O(n) | **Space:** O(1) for array, O(k) for HashMap

---

#### Problem: Valid Palindrome (with skip)
**Pattern:** Two Pointers

```java
public class ValidPalindrome {
    
    // Skip non-alphanumeric and check palindrome
    public static boolean isPalindrome(String s) {
        int left = 0;
        int right = s.length() - 1;
        
        while (left < right) {
            // Move left pointer to next alphanumeric
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }
            // Move right pointer to previous alphanumeric
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }
            
            // Compare (case-insensitive)
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
    
    public static void main(String[] args) {
        System.out.println(isPalindrome("A man, a plan, a canal: Panama")); // true
        System.out.println(isPalindrome("race a car")); // false
        System.out.println(isPalindrome("")); // true
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Category 3: HashMap & Frequency Problems

#### Problem: Find the Duplicate Number
**Pattern:** Frequency / HashSet / Floyd's Cycle Detection

```java
public class FindDuplicate {
    
    // APPROACH 1: HashSet (O(n) time, O(n) space)
    public static int findDuplicateHashSet(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (!seen.add(num)) return num;
        }
        return -1;
    }
    
    // APPROACH 2: Floyd's Tortoise and Hare (O(n) time, O(1) space!)
    // Treat array as linked list where index = value
    // Duplicate means cycle exists
    public static int findDuplicateFloyd(int[] nums) {
        // Phase 1: Find intersection point in cycle
        int slow = nums[0];
        int fast = nums[0];
        
        do {
            slow = nums[slow];       // Move one step
            fast = nums[nums[fast]];  // Move two steps
        } while (slow != fast);
        
        // Phase 2: Find the entrance to the cycle
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        
        return slow;
    }
    
    public static void main(String[] args) {
        int[] nums1 = {1, 3, 4, 2, 2};
        System.out.println(findDuplicateFloyd(nums1)); // 2
        
        int[] nums2 = {3, 1, 3, 4, 2};
        System.out.println(findDuplicateFloyd(nums2)); // 3
    }
}
```

**Time:** O(n) | **Space:** O(1) for Floyd's approach

---

#### Problem: Missing Number (0 to n)
**Pattern:** Math / XOR

```java
public class MissingNumber {
    
    // APPROACH 1: Math formula — sum of 0..n minus actual sum
    public static int missingNumberMath(int[] nums) {
        int n = nums.length;
        int expectedSum = n * (n + 1) / 2;
        int actualSum = 0;
        for (int num : nums) actualSum += num;
        return expectedSum - actualSum;
    }
    
    // APPROACH 2: XOR — no overflow risk!
    public static int missingNumberXOR(int[] nums) {
        int xor = 0;
        // XOR all indices 0..n
        for (int i = 0; i <= nums.length; i++) {
            xor ^= i;
        }
        // XOR all elements
        for (int num : nums) {
            xor ^= num;
        }
        // Everything cancels except the missing number
        return xor;
    }
    
    public static void main(String[] args) {
        int[] nums = {3, 0, 1};
        System.out.println("Missing (Math): " + missingNumberMath(nums));   // 2
        System.out.println("Missing (XOR): " + missingNumberXOR(nums));     // 2
        
        int[] nums2 = {9, 6, 4, 2, 3, 5, 7, 0, 1};
        System.out.println("Missing: " + missingNumberXOR(nums2));          // 8
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Category 4: Basic DP

#### Problem: Climbing Stairs
**Pattern:** Fibonacci variant

```java
public class ClimbingStairs {
    
    // Like Fibonacci: ways(n) = ways(n-1) + ways(n-2)
    // You can reach step n from step (n-1) or (n-2)
    
    public static int climbStairs(int n) {
        if (n <= 2) return n;
        
        int prev2 = 1; // ways(1)
        int prev1 = 2; // ways(2)
        
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
    
    public static void main(String[] args) {
        System.out.println(climbStairs(2));  // 2
        System.out.println(climbStairs(3));  // 3
        System.out.println(climbStairs(5));  // 8
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

#### Problem: Coin Change (Minimum Coins)
**Pattern:** Unbounded Knapsack DP

```java
public class CoinChange {
    
    // dp[i] = minimum coins needed to make amount i
    // dp[i] = min(dp[i - coin] + 1) for each coin
    
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        java.util.Arrays.fill(dp, amount + 1); // Use amount+1 as "infinity"
        dp[0] = 0; // 0 coins needed for amount 0
        
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] > amount ? -1 : dp[amount];
    }
    
    public static void main(String[] args) {
        int[] coins1 = {1, 5, 10, 25};
        System.out.println(coinChange(coins1, 30)); // 2 (25 + 5)
        
        int[] coins2 = {2};
        System.out.println(coinChange(coins2, 3)); // -1 (impossible)
        
        int[] coins3 = {1};
        System.out.println(coinChange(coins3, 0)); // 0
    }
}
```

**Time:** O(amount × coins) | **Space:** O(amount)

---

#### Problem: Fibonacci (with Memoization)
**Pattern:** Top-Down DP

```java
public class Fibonacci {
    
    // Without memoization: O(2^n) — too slow for n > 35
    // With memoization: O(n)
    
    static Map<Integer, Long> memo = new HashMap<>();
    
    public static long fibMemo(int n) {
        if (n <= 1) return n;
        if (memo.containsKey(n)) return memo.get(n);
        
        long result = fibMemo(n - 1) + fibMemo(n - 2);
        memo.put(n, result);
        return result;
    }
    
    // Bottom-up iterative
    public static long fibIterative(int n) {
        if (n <= 1) return n;
        
        long prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++) {
            long current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
    
    public static void main(String[] args) {
        System.out.println(fibMemo(10));        // 55
        System.out.println(fibIterative(10));    // 55
        System.out.println(fibMemo(50));         // 12586269025
    }
}
```

---

### Category 5: Greedy Problems

#### Problem: Jump Game
**Pattern:** Greedy — track the farthest reachable index

```java
public class JumpGame {
    
    // At each position, track the farthest we can reach
    // If farthest >= last index, we can reach the end
    
    public static boolean canJump(int[] nums) {
        int farthest = 0;
        
        for (int i = 0; i < nums.length; i++) {
            // If we can't even reach this position, fail
            if (i > farthest) return false;
            
            // Update farthest reachable
            farthest = Math.max(farthest, i + nums[i]);
        }
        
        return true;
    }
    
    public static void main(String[] args) {
        int[] nums1 = {2, 3, 1, 1, 4};
        System.out.println(canJump(nums1)); // true
        
        int[] nums2 = {3, 2, 1, 0, 4};
        System.out.println(canJump(nums2)); // false
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

## 5. Complete Problem List for Infosys Prep (40 Problems)

### Arrays (15 problems)
1. Two Sum ✓
2. Subarray Sum Equals K ✓
3. Maximum Subarray (Kadane) ✓
4. Rotate Array ✓
5. Find Duplicate Number ✓
6. Missing Number ✓
7. Merge Sorted Arrays
8. Best Time to Buy and Sell Stock
9. Contains Duplicate
10. Product of Array Except Self
11. Maximum Product Subarray
12. Move Zeroes
13. Intersection of Two Arrays
14. Next Permutation
15. Spiral Matrix

### Strings (10 problems)
16. Valid Palindrome ✓
17. Longest Common Prefix ✓
18. Anagram Check ✓
19. Reverse Words in a String
20. Count and Say
21. Longest Substring Without Repeating Characters
22. String to Integer (atoi)
23. Group Anagrams
24. Valid Parentheses
25. Longest Palindromic Substring

### HashMap & Basics (8 problems)
26. Two Sum using HashMap
27. Ransom Note (frequency check)
28. First Unique Character
29. Valid Anagram
30. Intersection of Two Arrays II
31. Single Number
32. Happy Number
33. Contains Duplicate II

### Basic DP & Greedy (7 problems)
34. Climbing Stairs ✓
35. Coin Change ✓
36. Jump Game ✓
37. House Robber
38. Best Time to Buy and Sell Stock II
39. Maximum Subarray Sum after Rotation
40. Min Cost Climbing Stairs

---

## 6. Edge Cases to Always Check

```
✅ Empty input (length 0 or 1)
✅ Single element arrays
✅ All same elements
✅ All negative numbers
✅ Negative numbers mixed with positive
✅ k = 0 or k > array length
✅ Integer overflow (use long for sums)
✅ Strings with spaces and special characters
✅ Very large inputs (test with maximum constraints)
```

---

## 7. Time Management During the Exam

| Phase | Duration | Action |
|-------|----------|--------|
| Reading | 5 min | Read ALL problems, identify easiest |
| Problem 1 | 35 min | Solve completely + test |
| Problem 2 | 55 min | Solve + optimize if time permits |
| Problem 3 | 70 min | Solve as much as possible |
| Review | 15 min | Check edge cases, fix bugs |

### Golden Rules
1. **Never leave a problem blank** — even a brute force solution gets partial credit
2. **Test with examples** — run through at least 3 examples manually
3. **Handle edge cases** — empty arrays, single elements, negative numbers
4. **Don't get stuck** — if stuck for 15 min, move to next problem
5. **Return to stuck problems** — fresh eyes help

---

## 8. Interview Tips (Post Online Round)

### Technical Interview (1-2 rounds)
- They'll ask 2-3 coding problems + CS fundamentals
- **Expect:** Basic SQL queries, OOP concepts, OS/Networking basics
- **Coding:** Similar difficulty to online round
- **Key:** Explain your approach before coding

### HR Interview
- Standard behavioral questions
- "Why Infosys?", "Where do you see yourself?"
- **Pro tip:** Show enthusiasm for learning and growing

### What Interviewers Look For
1. ✅ Problem-solving approach
2. ✅ Code clarity and structure
3. ✅ Edge case handling
4. ✅ Communication skills
5. ✅ Willingness to learn

---

## 9. Java-Specific Tips for Infosys

```java
// Always use Scanner for input (faster than BufferedReader for small inputs)
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();

// Use StringBuilder for string concatenation in loops
StringBuilder sb = new StringBuilder();
for (char c : arr) {
    sb.append(c);
}
String result = sb.toString();

// Use Arrays.sort() — it uses TimSort (O(n log n))
int[] arr = {5, 2, 8, 1};
Arrays.sort(arr);

// For HashMap iteration
for (Map.Entry<Integer, Integer> entry : map.entrySet()) {
    int key = entry.getKey();
    int value = entry.getValue();
}
```

---

## 10. Final Checklist Before Exam

- [ ] Practiced all 40 problems above
- [ ] Can solve Easy problems in under 10 minutes
- [ ] Can solve Medium problems in under 20 minutes
- [ ] Know common edge cases by heart
- [ ] Have Java templates ready (HashMap, PriorityQueue, etc.)
- [ ] Practiced time management with mock tests
- [ ] Rest well the night before

---

> **Remember:** Infosys values correctness over cleverness. A working brute force beats a buggy optimal solution every time. Focus on clean, correct code.
