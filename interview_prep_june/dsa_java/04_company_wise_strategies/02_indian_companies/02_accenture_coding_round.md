# Accenture — Coding Assessment Strategy

> "Accenture's coding round is straightforward but unforgiving. They test correctness, not cleverness. Nail the basics, and you're through."

---

## 1. Accenture Assessment Format

### Structure (Total: ~3 hours)
```
┌──────────────────────────────────────────────────────────┐
│  Section 1: Cognitive Assessment (45 min)                 │
│  → Logical reasoning, pattern recognition, data analysis  │
│                                                           │
│  Section 2: Technical Assessment (60 min)                 │
│  → CS fundamentals, DBMS, OOP, Networking basics          │
│                                                           │
│  Section 3: Coding Assessment (60 min)                    │
│  → 2-3 coding problems (Easy difficulty)                  │
│  → Language: Java, C++, Python, or C                      │
└──────────────────────────────────────────────────────────┘
```

### Key Observations
- **Difficulty:** Easiest among all service companies
- **Pattern:** Very predictable — mostly array/string/math problems
- **Goal:** Complete correctness > optimization
- **Acceptance Rate:** High if you solve all problems correctly
- **Package:** ~₹4.5 LPA (ASE) to ₹6.5 LPA (SE)

---

## 2. Most Asked Topics (Priority Order)

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 80% | Basic operations, rotation, leaders |
| 2 | Strings | 70% | Anagram, palindrome, reversal |
| 3 | Math/Number Theory | 60% | Prime, GCD, factorial, Fibonacci |
| 4 | Pattern Printing | 50% | Star, number, alphabet patterns |
| 5 | Sorting | 40% | Bubble, selection, insertion |
| 6 | Searching | 30% | Binary search basics |
| 7 | Basic DP | 20% | Fibonacci, climbing stairs |

**Golden Rule:** If you can print patterns and do array manipulation, you're 70% prepared.

---

## 3. Core Problems with Java Solutions

### Problem 1: Leaders in an Array
**Concept:** An element is a leader if it's greater than all elements to its right.

```java
import java.util.*;

public class LeadersInArray {
    
    // APPROACH: Traverse from right to left
    // Keep track of max-so-far from right
    // If current element > max-so-far, it's a leader
    
    public static List<Integer> findLeaders(int[] arr) {
        List<Integer> leaders = new ArrayList<>();
        
        // Rightmost element is always a leader
        int maxFromRight = arr[arr.length - 1];
        leaders.add(maxFromRight);
        
        // Traverse from second-last to first
        for (int i = arr.length - 2; i >= 0; i--) {
            if (arr[i] > maxFromRight) {
                leaders.add(arr[i]);
                maxFromRight = arr[i];
            }
        }
        
        // Leaders were collected right to left, reverse if needed
        Collections.reverse(leaders);
        return leaders;
    }
    
    public static void main(String[] args) {
        int[] arr1 = {16, 17, 4, 3, 5, 2};
        System.out.println("Leaders: " + findLeaders(arr1)); // [17, 5, 2]
        
        int[] arr2 = {1, 2, 3, 4, 5};
        System.out.println("Leaders: " + findLeaders(arr2)); // [5]
        
        int[] arr3 = {5, 4, 3, 2, 1};
        System.out.println("Leaders: " + findLeaders(arr3)); // [5, 4, 3, 2, 1]
    }
}
```

**Time:** O(n) | **Space:** O(1) excluding output

---

### Problem 2: Find the Missing Number
**Concept:** Given array of n-1 numbers from 0 to n, find the missing one.

```java
public class MissingNumberAccenture {
    
    // APPROACH 1: Sum formula
    public static int findMissingSum(int[] arr, int n) {
        int expectedSum = n * (n + 1) / 2;
        int actualSum = 0;
        for (int num : arr) actualSum += num;
        return expectedSum - actualSum;
    }
    
    // APPROACH 2: XOR (no overflow)
    public static int findMissingXOR(int[] arr, int n) {
        int xor = 0;
        for (int i = 0; i <= n; i++) xor ^= i;
        for (int num : arr) xor ^= num;
        return xor;
    }
    
    // APPROACH 3: Boolean array
    public static int findMissingBool(int[] arr, int n) {
        boolean[] present = new boolean[n + 1];
        for (int num : arr) present[num] = true;
        for (int i = 0; i <= n; i++) {
            if (!present[i]) return i;
        }
        return -1;
    }
    
    public static void main(String[] args) {
        int[] arr = {3, 0, 1, 5, 4, 6};
        int n = 6;
        System.out.println("Missing (Sum): " + findMissingSum(arr, n));   // 2
        System.out.println("Missing (XOR): " + findMissingXOR(arr, n));   // 2
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 3: Anagram Check
**Concept:** Two strings are anagrams if they have the same characters with same frequencies.

```java
public class AnagramAccenture {
    
    public static boolean isAnagram(String s1, String s2) {
        if (s1.length() != s2.length()) return false;
        
        int[] freq = new int[26];
        
        for (int i = 0; i < s1.length(); i++) {
            freq[s1.charAt(i) - 'a']++;
            freq[s2.charAt(i) - 'a']--;
        }
        
        for (int f : freq) {
            if (f != 0) return false;
        }
        return true;
    }
    
    // Group anagrams from array of strings
    public static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        
        for (String str : strs) {
            char[] chars = str.toCharArray();
            java.util.Arrays.sort(chars);
            String sorted = new String(chars);
            map.computeIfAbsent(sorted, k -> new ArrayList<>()).add(str);
        }
        
        return new ArrayList<>(map.values());
    }
    
    public static void main(String[] args) {
        System.out.println(isAnagram("listen", "silent"));  // true
        System.out.println(isAnagram("hello", "world"));    // false
        
        String[] words = {"eat", "tea", "tan", "ate", "nat", "bat"};
        System.out.println("Groups: " + groupAnagrams(words));
        // [[eat, tea, ate], [tan, nat], [bat]]
    }
}
```

---

### Problem 4: Remove Duplicates from Sorted Array
**Concept:** In-place removal using two pointers.

```java
public class RemoveDuplicates {
    
    // Two pointer approach: slow pointer marks unique elements
    public static int removeDuplicates(int[] nums) {
        if (nums.length == 0) return 0;
        
        int slow = 0; // Points to last unique element
        
        for (int fast = 1; fast < nums.length; fast++) {
            if (nums[fast] != nums[slow]) {
                slow++;
                nums[slow] = nums[fast];
            }
        }
        
        return slow + 1; // Number of unique elements
    }
    
    public static void main(String[] args) {
        int[] nums = {1, 1, 2, 2, 3, 4, 4, 5};
        int uniqueCount = removeDuplicates(nums);
        System.out.println("Unique count: " + uniqueCount); // 5
        System.out.print("Array: ");
        for (int i = 0; i < uniqueCount; i++) {
            System.out.print(nums[i] + " "); // 1 2 3 4 5
        }
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

## 4. Pattern Printing (Accenture's Favorite!)

### Pattern 1: Right Triangle Stars
```
*
**
***
****
*****
```

```java
public class PatternStarRight {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
```

### Pattern 2: Inverted Right Triangle
```
*****
****
***
**
*
```

```java
public class PatternStarInverted {
    public static void main(String[] args) {
        int n = 5;
        for (int i = n; i >= 1; i--) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
```

### Pattern 3: Pyramid
```
    *
   ***
  *****
 *******
*********
```

```java
public class PatternPyramid {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            // Print spaces
            for (int j = 1; j <= n - i; j++) {
                System.out.print(" ");
            }
            // Print stars
            for (int j = 1; j <= 2 * i - 1; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
```

### Pattern 4: Diamond
```
    *
   ***
  *****
 *******
*********
 *******
  *****
   ***
    *
```

```java
public class PatternDiamond {
    public static void main(String[] args) {
        int n = 5;
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
}
```

### Pattern 5: Number Triangle
```
1
12
123
1234
12345
```

```java
public class PatternNumberTriangle {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(j);
            }
            System.out.println();
        }
    }
}
```

### Pattern 6: Floyd's Triangle
```
1
2 3
4 5 6
7 8 9 10
```

```java
public class PatternFloyds {
    public static void main(String[] args) {
        int n = 4;
        int num = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(num + " ");
                num++;
            }
            System.out.println();
        }
    }
}
```

### Pattern 7: Alphabet Pattern
```
A
AB
ABC
ABCD
ABCDE
```

```java
public class PatternAlphabet {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                System.out.print((char)('A' + j));
            }
            System.out.println();
        }
    }
}
```

### Pattern 8: Butterfly
```
*        *
**      **
***    ***
****  ****
**********
****  ****
***    ***
**      **
*        *
```

```java
public class PatternButterfly {
    public static void main(String[] args) {
        int n = 5;
        // Upper half
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) System.out.print("*");
            for (int j = 1; j <= 2 * (n - i); j++) System.out.print(" ");
            for (int j = 1; j <= i; j++) System.out.print("*");
            System.out.println();
        }
        // Lower half
        for (int i = n; i >= 1; i--) {
            for (int j = 1; j <= i; j++) System.out.print("*");
            for (int j = 1; j <= 2 * (n - i); j++) System.out.print(" ");
            for (int j = 1; j <= i; j++) System.out.print("*");
            System.out.println();
        }
    }
}
```

---

## 5. Mathematical Problems

### Problem: Check if Prime
```java
public class PrimeCheck {
    public static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        
        // Only check up to √n, skip even numbers
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }
    
    // Print all primes up to n (Sieve of Eratosthenes)
    public static void sieveOfEratosthenes(int n) {
        boolean[] isComposite = new boolean[n + 1];
        
        for (int i = 2; i * i <= n; i++) {
            if (!isComposite[i]) {
                for (int j = i * i; j <= n; j += i) {
                    isComposite[j] = true;
                }
            }
        }
        
        System.out.print("Primes up to " + n + ": ");
        for (int i = 2; i <= n; i++) {
            if (!isComposite[i]) System.out.print(i + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        System.out.println("Is 17 prime? " + isPrime(17));  // true
        System.out.println("Is 15 prime? " + isPrime(15));  // false
        sieveOfEratosthenes(30);
        // Primes up to 30: 2 3 5 7 11 13 17 19 23 29
    }
}
```

### Problem: GCD and LCM
```java
public class GCDCalculator {
    
    // Euclidean Algorithm: GCD(a, b) = GCD(b, a % b)
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
    
    public static int lcm(int a, int b) {
        return (a / gcd(a, b)) * b; // Divide first to avoid overflow
    }
    
    // GCD of array
    public static int gcdArray(int[] arr) {
        int result = arr[0];
        for (int i = 1; i < arr.length; i++) {
            result = gcd(result, arr[i]);
        }
        return result;
    }
    
    public static void main(String[] args) {
        System.out.println("GCD(12, 18): " + gcd(12, 18)); // 6
        System.out.println("LCM(12, 18): " + lcm(12, 18)); // 36
        System.out.println("GCD of [12, 18, 24]: " + gcdArray(new int[]{12, 18, 24})); // 6
    }
}
```

### Problem: Fibonacci Series
```java
public class FibonacciAccenture {
    
    // Print first n Fibonacci numbers
    public static void fibonacci(int n) {
        int a = 0, b = 1;
        System.out.print("Fibonacci: ");
        for (int i = 1; i <= n; i++) {
            System.out.print(a + " ");
            int next = a + b;
            a = b;
            b = next;
        }
        System.out.println();
    }
    
    // Check if a number is Fibonacci
    public static boolean isFibonacci(int n) {
        // A number is Fibonacci if and only if
        // 5n^2 + 4 or 5n^2 - 4 is a perfect square
        return isPerfectSquare(5 * n * n + 4) || isPerfectSquare(5 * n * n - 4);
    }
    
    private static boolean isPerfectSquare(int x) {
        int s = (int) Math.sqrt(x);
        return s * s == x;
    }
    
    public static void main(String[] args) {
        fibonacci(10); // 0 1 1 2 3 5 8 13 21 34
        System.out.println("Is 8 Fibonacci? " + isFibonacci(8)); // true
        System.out.println("Is 9 Fibonacci? " + isFibonacci(9)); // false
    }
}
```

### Problem: Sum of Digits
```java
public class SumOfDigits {
    
    public static int digitSum(int n) {
        int sum = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
        }
        return sum;
    }
    
    // Recursive version
    public static int digitSumRecursive(int n) {
        if (n == 0) return 0;
        return n % 10 + digitSumRecursive(n / 10);
    }
    
    // Digital root (keep summing until single digit)
    public static int digitalRoot(int n) {
        while (n >= 10) {
            n = digitSum(n);
        }
        return n;
    }
    
    public static void main(String[] args) {
        System.out.println("Sum of 12345: " + digitSum(12345)); // 15
        System.out.println("Digital root of 9999: " + digitalRoot(9999)); // 9
    }
}
```

---

## 6. String Manipulation Problems

### Problem: Reverse a String (without built-in)
```java
public class ReverseString {
    
    public static String reverse(String s) {
        char[] arr = s.toCharArray();
        int left = 0, right = arr.length - 1;
        
        while (left < right) {
            char temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
        return new String(arr);
    }
    
    // Reverse each word in a sentence
    public static String reverseWords(String s) {
        String[] words = s.split(" ");
        StringBuilder sb = new StringBuilder();
        
        for (String word : words) {
            sb.append(reverse(word)).append(" ");
        }
        
        return sb.toString().trim();
    }
    
    public static void main(String[] args) {
        System.out.println(reverse("hello")); // "olleh"
        System.out.println(reverseWords("Hello World")); // "olleH dlroW"
    }
}
```

### Problem: Count Vowels and Consonants
```java
public class VowelConsonant {
    public static void count(String s) {
        int vowels = 0, consonants = 0, digits = 0, spaces = 0;
        s = s.toLowerCase();
        
        for (char c : s.toCharArray()) {
            if ("aeiou".indexOf(c) != -1) {
                vowels++;
            } else if (Character.isLetter(c)) {
                consonants++;
            } else if (Character.isDigit(c)) {
                digits++;
            } else if (c == ' ') {
                spaces++;
            }
        }
        
        System.out.println("Vowels: " + vowels);
        System.out.println("Consonants: " + consonants);
        System.out.println("Digits: " + digits);
        System.out.println("Spaces: " + spaces);
    }
    
    public static void main(String[] args) {
        count("Hello World 123");
        // Vowels: 3
        // Consonants: 7
        // Digits: 3
        // Spaces: 2
    }
}
```

### Problem: Check Pangram
```java
public class PangramCheck {
    
    public static boolean isPangram(String s) {
        boolean[] letters = new boolean[26];
        s = s.toLowerCase();
        
        for (char c : s.toCharArray()) {
            if (c >= 'a' && c <= 'z') {
                letters[c - 'a'] = true;
            }
        }
        
        for (boolean found : letters) {
            if (!found) return false;
        }
        return true;
    }
    
    public static void main(String[] args) {
        System.out.println(isPangram("The quick brown fox jumps over the lazy dog")); // true
        System.out.println(isPangram("Hello World")); // false
    }
}
```

---

## 7. Complete Problem List for Accenture (50 Problems)

### Arrays (15)
1. Leaders in array ✓
2. Missing number ✓
3. Remove duplicates ✓
4. Rotate array
5. Array rotation (left by d)
6. Move zeroes to end
7. Second largest element
8. Merge two sorted arrays
9. Sort array of 0s, 1s, and 2s (Dutch National Flag)
10. Kadane's algorithm
11. Best time to buy and sell stock
12. Two sum
13. Find duplicate in array
14. Intersection of two arrays
15. Pair with given sum

### Strings (10)
16. Reverse string ✓
17. Reverse words ✓
18. Anagram check ✓
19. Pangram check ✓
20. Count vowels/consonants ✓
21. Palindrome check
22. First non-repeating character
23. String compression
24. Remove duplicates from string
25. Check if rotation

### Math (10)
26. Prime check ✓
27. GCD/LCM ✓
28. Fibonacci ✓
29. Sum of digits ✓
30. Digital root ✓
31. Factorial
32. Power of a number
33. Armstrong number
34. Strong number
35. Perfect number

### Pattern Printing (8)
36. Star triangle ✓
37. Inverted triangle ✓
38. Pyramid ✓
39. Diamond ✓
40. Number triangle ✓
41. Floyd's triangle ✓
42. Alphabet pattern ✓
43. Butterfly ✓

### Sorting/Searching (7)
44. Bubble sort
45. Selection sort
46. Insertion sort
47. Binary search
48. Linear search
49. Sort characters by frequency
50. Search in rotated sorted array

---

## 8. Mock Test Strategy

### Before the Test
- [ ] Practice all pattern printing problems (10 min each)
- [ ] Practice array/string manipulation (15 min each)
- [ ] Review math problems (5 min each)
- [ ] Time yourself: Easy = 10 min, Medium = 20 min

### During the Test
1. **Read ALL problems first** (5 min)
2. **Start with easiest** — complete it fully
3. **Don't optimize prematurely** — correct brute force > buggy optimal
4. **Test every solution** with at least 3 examples
5. **Handle edge cases** — empty arrays, single elements

### Common Mistakes to Avoid
```java
// ❌ Off-by-one errors
for (int i = 0; i <= n; i++) // Should be i < n

// ❌ Integer overflow
int sum = n * (n + 1) / 2; // Use long for large n

// ❌ Not handling empty input
if (arr == null || arr.length == 0) return;

// ❌ Forgetting to import
import java.util.*; // Always import at top

// ❌ Not closing Scanner
sc.close(); // Always close resources
```

---

## 9. Java Templates for Quick Coding

```java
// Template 1: Fast I/O
import java.util.*;
import java.io.*;

public class Solution {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt(); // Number of test cases
        
        while (t-- > 0) {
            int n = sc.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }
            // Your solution here
            System.out.println(solve(arr));
        }
        sc.close();
    }
    
    static int solve(int[] arr) {
        // Implementation
        return 0;
    }
}

// Template 2: HashMap for frequency counting
Map<Integer, Integer> freq = new HashMap<>();
for (int num : arr) {
    freq.merge(num, 1, Integer::sum);
}

// Template 3: Sort and use
Arrays.sort(arr);
int min = arr[0];
int max = arr[arr.length - 1];
```

---

## 10. Final Preparation Checklist

### Easy (Should solve in < 10 min each)
- [ ] Array rotation
- [ ] Reverse string
- [ ] Anagram check
- [ ] Palindrome check
- [ ] Missing number
- [ ] Leaders in array
- [ ] Pattern printing (all types)
- [ ] Factorial/Fibonacci
- [ ] Prime check
- [ ] GCD/LCM

### Medium (Should solve in < 20 min each)
- [ ] Two sum
- [ ] Kadane's algorithm
- [ ] Merge sorted arrays
- [ ] Binary search
- [ ] Sort 0s, 1s, 2s
- [ ] String compression
- [ ] Group anagrams

### Confidence Boosters
- [ ] Can solve any pattern in 2 minutes
- [ ] Can implement any sorting algorithm from memory
- [ ] Know all edge cases by heart
- [ ] Have practiced 50+ problems

---

> **Remember:** Accenture values completeness and correctness above all. A working brute force solution with all edge cases handled is worth more than an optimal solution with bugs. Focus on getting it RIGHT, not getting it FAST.
