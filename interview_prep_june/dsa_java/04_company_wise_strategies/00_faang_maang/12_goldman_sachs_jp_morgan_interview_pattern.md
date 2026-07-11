# Goldman Sachs / JP Morgan Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Investment Bank Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Focus on analytical and quantitative skills
- Discussion of past projects involving data/finance

### Technical Phone Screen (45-60 min)
- 2-3 coding problems in 45 minutes (time-pressured)
- Problems tend to be easy-medium difficulty
- Focus on **correctness** over optimization
- May include SQL and database questions

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (2-3): Multiple problems per round
- **System Design** (1): Trading systems, risk management
- **Quantitative** (1): Mathematical problem-solving (sometimes)
- **Hiring Manager / Behavioral** (1): Team fit, cultural alignment

### Key Differences from Other FAANG
- **Structured process** — Investment banks follow strict interview protocols
- **2-3 problems per round** — More problems, less time per problem
- **Easy-medium difficulty** — They value correctness over complexity
- **Attention to detail** — Financial code must be precise
- **Clean OOP** — Financial systems need maintainable code
- **SQL knowledge** — Often asked for data-related roles

---

## 2. Most Asked Topics

### Priority Matrix

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 85% | Easy-medium, basic operations |
| 2 | Strings | 80% | Anagrams, palindromes, parsing |
| 3 | HashMaps | 75% | Frequency, grouping, two sum |
| 4 | DP Basics | 60% | Simple DP, not hard |
| 5 | OOP Design | 55% | Design patterns, clean code |
| 6 | Trees | 50% | Basic BST, traversals |
| 7 | SQL | 40% | Queries, joins, optimization |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Strings:    ██████████████████
HashMaps:   █████████████████
DP Basics:  ████████████
OOP:        ███████████
Trees:      ██████████
SQL:        ████████
```

### What Makes Investment Banks Different
- **Multiple problems per round** — They want breadth, not depth
- **Correctness over optimization** — Right answer is more important than fast
- **Attention to detail** — Financial code must be precise
- **Clean OOP** — Enterprise code needs to be maintainable
- **SQL knowledge** — Data is central to finance
- **Mathematical thinking** — Some quantitative problems

---

## 3. Investment Bank Culture

### Core Values

| Value | Meaning | Interview Impact |
|-------|---------|-----------------|
| **Excellence** | High standards in everything | Attention to detail |
| **Integrity** | Ethical behavior | Honest communication |
| **Client Service** | Client-first approach | User-centric thinking |
| **Partnership** | Collaborative culture | Team-oriented solutions |
| **Innovation** | Modernize financial systems | Creative problem-solving |

### What Investment Banks Look For
1. **Correct code** — Financial systems can't have bugs
2. **Clean OOP** — Enterprise-grade code quality
3. **Attention to detail** — Precision matters in finance
4. **SQL knowledge** — Data queries are daily work
5. **Quantitative skills** — Mathematical problem-solving

### Behavioral Questions
- "Tell me about a time you had to write very precise code"
- "How do you approach debugging critical financial systems?"
- "Describe a time you had to meet a tight deadline"
- "How do you handle working with large datasets?"

---

## 4. Types of Problems

### Array Problems
- Two sum variants
- Subarray problems
- Sorting and searching
- Merge intervals
- Kadane's algorithm

### String Problems
- Anagram detection
- Palindrome checking
- String parsing
- Pattern matching
- Substring problems

### HashMap Problems
- Frequency counting
- Group anagrams
- Two sum
- Subarray sum equals k
- Valid anagram

### DP Basics
- Climbing stairs
- Coin change
- Longest common subsequence
- House robber
- Maximum subarray

### Financial Problems
- Stock buy/sell (max profit)
- Currency conversion
- Transaction matching
- Risk calculation
- Portfolio optimization (basics)

---

## 5. Example Problems

### Problem 1: Two Sum
**Problem:** Find two numbers that add up to a target.

**Approach:** HashMap — store seen numbers, check complement.

```java
import java.util.*;

public class TwoSum {

    // APPROACH: One-pass HashMap
    // Store each number and its index
    // For each number, check if complement exists
    
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            
            map.put(nums[i], i);
        }
        
        return new int[]{-1, -1};
    }

    // VARIANT: Three Sum (find three numbers that add to zero)
    public static List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums);
        
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue; // Skip duplicates
            
            int left = i + 1, right = nums.length - 1;
            
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        
        return result;
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] result = twoSum(nums, 9);
        System.out.println("Indices: " + result[0] + ", " + result[1]); // 0, 1
        
        int[] nums2 = {-1, 0, 1, 2, -1, -4};
        System.out.println(threeSum(nums2)); // [[-1, -1, 2], [-1, 0, 1]]
    }
}
```

**Time:** O(n) for Two Sum, O(n²) for Three Sum | **Space:** O(n)

---

### Problem 2: Valid Anagram
**Problem:** Determine if two strings are anagrams of each other.

**Approach:** Character frequency count — compare counts of both strings.

```java
import java.util.*;

public class ValidAnagram {

    // APPROACH: Character count array
    // Count characters in first string, decrement for second
    // If all counts are zero, they're anagrams
    
    public static boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        
        int[] count = new int[26];
        
        for (char c : s.toCharArray()) {
            count[c - 'a']++;
        }
        
        for (char c : t.toCharArray()) {
            count[c - 'a']--;
            if (count[c - 'a'] < 0) return false;
        }
        
        return true;
    }
    
    // ALTERNATIVE: Sorting approach
    public static boolean isAnagramSort(String s, String t) {
        if (s.length() != t.length()) return false;
        
        char[] sChars = s.toCharArray();
        char[] tChars = t.toCharArray();
        Arrays.sort(sChars);
        Arrays.sort(tChars);
        
        return Arrays.equals(sChars, tChars);
    }

    // VARIANT: Group anagrams from a list
    public static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String sorted = new String(chars);
            
            map.computeIfAbsent(sorted, k -> new ArrayList<>()).add(s);
        }
        
        return new ArrayList<>(map.values());
    }

    public static void main(String[] args) {
        System.out.println(isAnagram("anagram", "nagaram")); // true
        System.out.println(isAnagram("rat", "car"));          // false
        
        String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        System.out.println(groupAnagrams(strs));
        // [[eat, tea, ate], [tan, nat], [bat]]
    }
}
```

**Time:** O(n) for count approach, O(n log n) for sort | **Space:** O(1)

---

### Problem 3: Best Time to Buy and Sell Stock
**Problem:** Find maximum profit from buying and selling once.

**Approach:** Track minimum price seen so far, calculate profit at each step.

```java
public class BuySellStock {

    // APPROACH: Track minimum price, calculate max profit
    // At each day, profit = current price - minimum price seen so far
    
    public static int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        
        for (int price : prices) {
            if (price < minPrice) {
                minPrice = price;
            } else if (price - minPrice > maxProfit) {
                maxProfit = price - minPrice;
            }
        }
        
        return maxProfit;
    }
    
    // VARIANT: Multiple transactions allowed (buy and sell multiple times)
    public static int maxProfitMultiple(int[] prices) {
        int profit = 0;
        
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] > prices[i - 1]) {
                profit += prices[i] - prices[i - 1];
            }
        }
        
        return profit;
    }

    public static void main(String[] args) {
        int[] prices1 = {7, 1, 5, 3, 6, 4};
        System.out.println(maxProfit(prices1)); // 5 (buy at 1, sell at 6)
        
        int[] prices2 = {7, 6, 4, 3, 1};
        System.out.println(maxProfit(prices2)); // 0 (no profit possible)
        
        int[] prices3 = {7, 1, 5, 3, 6, 4};
        System.out.println(maxProfitMultiple(prices3)); // 7 (1→5 + 3→6)
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 4: Longest Common Subsequence
**Problem:** Find the length of the longest common subsequence of two strings.

**Approach:** 2D DP — dp[i][j] = LCS length of first i chars and first j chars.

```java
public class LongestCommonSubsequence {

    // APPROACH: 2D DP
    // dp[i][j] = LCS length of text1[0..i-1] and text2[0..j-1]
    // If characters match: dp[i][j] = dp[i-1][j-1] + 1
    // Otherwise: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    public static int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }

    // VARIANT: Return the actual LCS string
    public static String lcsString(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        // Backtrack to find the actual subsequence
        StringBuilder sb = new StringBuilder();
        int i = m, j = n;
        
        while (i > 0 && j > 0) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                sb.append(text1.charAt(i - 1));
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        
        return sb.reverse().toString();
    }

    public static void main(String[] args) {
        System.out.println(longestCommonSubsequence("abcde", "ace")); // 3
        System.out.println(longestCommonSubsequence("abc", "abc"));   // 3
        System.out.println(longestCommonSubsequence("abc", "def"));   // 0
        
        System.out.println(lcsString("abcde", "ace")); // "ace"
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n)

---

### Problem 5: Reverse Integer
**Problem:** Reverse the digits of a 32-bit signed integer.

**Approach:** Mathematical — extract digits using modulo, build reversed number.

```java
public class ReverseInteger {

    // APPROACH: Extract digits from right, build reversed number
    // Handle overflow for 32-bit signed integer
    
    public static int reverse(int x) {
        int reversed = 0;
        
        while (x != 0) {
            int digit = x % 10;
            
            // Check for overflow before updating
            if (reversed > Integer.MAX_VALUE / 10 || 
                (reversed == Integer.MAX_VALUE / 10 && digit > 7)) {
                return 0;
            }
            if (reversed < Integer.MIN_VALUE / 10 || 
                (reversed == Integer.MIN_VALUE / 10 && digit < -8)) {
                return 0;
            }
            
            reversed = reversed * 10 + digit;
            x /= 10;
        }
        
        return reversed;
    }

    public static void main(String[] args) {
        System.out.println(reverse(123));    // 321
        System.out.println(reverse(-123));   // -321
        System.out.println(reverse(120));    // 21
        System.out.println(reverse(1534236469)); // 0 (overflow)
    }
}
```

**Time:** O(log n) | **Space:** O(1)

---

## 6. Preparation Strategy

### Focus Areas (3-Week Plan — Shorter, more focused)

#### Week 1: Easy-Medium Arrays and Strings
- [ ] Two sum variants (10 problems)
- [ ] Valid anagram, palindrome (10 problems)
- [ ] Kadane's algorithm and variants (5 problems)
- [ ] Buy/sell stock problems (5 problems)
- [ ] Practice: 25 problems

#### Week 2: HashMaps, Trees, and DP Basics
- [ ] HashMap patterns (10 problems)
- [ ] BST basics (10 problems)
- [ ] 1D DP (climbing stairs, house robber) (10 problems)
- [ ] SQL basics (5 queries)
- [ ] Practice: 25 problems

#### Week 3: OOP Design and Mocks
- [ ] Design patterns (Singleton, Factory, Observer)
- [ ] SOLID principles
- [ ] Financial problem variants (5 problems)
- [ ] Mock interviews (3-5 sessions, 2-3 problems per session)
- [ ] Review and consolidate

### Investment Bank-Specific Tips
1. **Correctness first** — Don't optimize until you have the right answer
2. **Multiple problems per round** — Practice solving 2-3 problems quickly
3. **Clean code** — Investment banks have massive codebases; readability matters
4. **Attention to detail** — Handle edge cases, overflow, empty inputs
5. **SQL basics** — Know JOINs, GROUP BY, subqueries
6. **OOP design** — Enterprise-grade code quality
7. **Mathematical thinking** — Some quantitative problems may appear
8. **Time management** — You have less time per problem; be efficient

### Common Follow-up Questions
- "Can you handle overflow cases?"
- "What if the input is empty?"
- "How would you make this thread-safe?"
- "Can you optimize for memory?"
- "What if the numbers are very large?"

### Resources
- LeetCode Easy-Medium problems (top 100)
- SQL practice on LeetCode/HackerRank
- "Clean Code" by Robert Martin
- OOP design patterns

---

> **Remember:** Investment banks value correctness and clean code over clever algorithms. They want you to solve multiple problems quickly and correctly. Practice easy-medium problems and focus on writing production-quality code.
