# Hashing Patterns Cheatsheet

---

## When to Use Hashing

- Need **O(1) average lookup** for keys
- Need to **group** elements by some property
- Need **frequency counting**
- Need to **detect duplicates**
- Need **complement tracking** (two-sum style)
- Need **prefix state caching**

---

## Pattern 1: Frequency Counting

```java
// Most Frequent Element
public int mostFrequent(int[] nums) {
    Map<Integer, Integer> freq = new HashMap<>();
    int maxCount = 0, result = nums[0];

    for (int num : nums) {
        int count = freq.merge(num, 1, Integer::sum);
        if (count > maxCount) {
            maxCount = count;
            result = num;
        }
    }
    return result;
}

// Top K Frequent Elements
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) freq.merge(num, 1, Integer::sum);

    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
        pq.offer(new int[]{e.getKey(), e.getValue()});
        if (pq.size() > k) pq.poll();
    }

    int[] result = new int[k];
    for (int i = 0; i < k; i++) result[i] = pq.poll()[0];
    return result;
}
```

---

## Pattern 2: Two-Sum / Complement Tracking

```java
// Two Sum — O(n)
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>(); // value → index

    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}

// Four Sum II — count tuples where A[i]+B[j]+C[k]+D[l]=0
public int fourSumCount(int[] A, int[] B, int[] C, int[] D) {
    Map<Integer, Integer> abSums = new HashMap<>();

    for (int a : A) {
        for (int b : B) {
            abSums.merge(a + b, 1, Integer::sum);
        }
    }

    int count = 0;
    for (int c : C) {
        for (int d : D) {
            count += abSums.getOrDefault(-(c + d), 0);
        }
    }
    return count;
}
```

---

## Pattern 3: Prefix Sum + Hashing

```java
// Subarray Sum Equals K (LeetCode 560)
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1);

    int prefixSum = 0, count = 0;
    for (int num : nums) {
        prefixSum += num;
        count += prefixCount.getOrDefault(prefixSum - k, 0);
        prefixCount.merge(prefixSum, 1, Integer::sum);
    }
    return count;
}

// Continuous Subarray Sum (divisible by k, LeetCode 523)
public boolean checkSubarraySum(int[] nums, int k) {
    Map<Integer, Integer> remainderIndex = new HashMap<>();
    remainderIndex.put(0, -1);

    int prefixSum = 0;
    for (int i = 0; i < nums.length; i++) {
        prefixSum += nums[i];
        int remainder = prefixSum % k;

        if (remainderIndex.containsKey(remainder)) {
            if (i - remainderIndex.get(remainder) >= 2) return true;
        } else {
            remainderIndex.put(remainder, i);
        }
    }
    return false;
}
```

---

## Pattern 4: Grouping by Property

```java
// Group Anagrams (LeetCode 49)
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();

    for (String s : strs) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);

        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}

// Group Shifted Strings
public List<List<String>> groupStrings(String[] strings) {
    Map<String, List<String>> groups = new HashMap<>();

    for (String s : strings) {
        StringBuilder key = new StringBuilder();
        int base = s.charAt(0) - 'a';

        for (char c : s.toCharArray()) {
            int shifted = (c - base + 26) % 26;
            key.append(shifted).append(',');
        }

        groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```

---

## Pattern 5: Caching / Memoization

```java
// LRU Cache
class LRUCache {
    private int capacity;
    private Map<Integer, Node> map;
    private Node head, tail; // doubly linked list

    private static class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) { key = k; value = v; }
    }

    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        removeNode(node);
        addToFront(node);
        return node.value;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            removeNode(node);
            addToFront(node);
        } else {
            if (map.size() >= capacity) {
                Node lru = tail.prev;
                removeNode(lru);
                map.remove(lru.key);
            }
            Node node = new Node(key, value);
            map.put(key, node);
            addToFront(node);
        }
    }

    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}
```

---

## Pattern 6: Sliding Window + Hashing

```java
// Minimum Window Substring (LeetCode 76)
public String minWindow(String s, String t) {
    Map<Character, Integer> need = new HashMap<>();
    Map<Character, Integer> have = new HashMap<>();

    for (char c : t.toCharArray()) {
        need.merge(c, 1, Integer::sum);
    }

    int required = need.size();
    int formed = 0;
    int left = 0, minLen = Integer.MAX_VALUE, minStart = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        have.merge(c, 1, Integer::sum);

        if (have.get(c).equals(need.get(c))) {
            formed++;
        }

        while (formed == required) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minStart = left;
            }
            char leftChar = s.charAt(left);
            have.merge(leftChar, -1, Integer::sum);
            if (need.containsKey(leftChar) && have.get(leftChar) < need.get(leftChar)) {
                formed--;
            }
            left++;
        }
    }

    return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
}
```

---

## Pattern 7: Cycle Detection with Hashing

```java
// Happy Number (LeetCode 202)
public boolean isHappy(int n) {
    Set<Integer> seen = new HashSet<>();
    while (n != 1 && !seen.contains(n)) {
        seen.add(n);
        n = sumOfSquares(n);
    }
    return n == 1;
}

private int sumOfSquares(int n) {
    int sum = 0;
    while (n > 0) {
        int d = n % 10;
        sum += d * d;
        n /= 10;
    }
    return sum;
}
```

---

## Pattern 8: String Hashing (Rabin-Karp)

```java
// Rabin-Karp substring search
public int strStr(String haystack, String needle) {
    if (needle.length() > haystack.length()) return -1;

    int base = 31, mod = 1_000_000_007;
    int needleHash = 0, windowHash = 0;
    int power = 1;

    for (int i = 0; i < needle.length(); i++) {
        needleHash = (int)((needleHash * base + needle.charAt(i)) % mod);
        windowHash = (int)((windowHash * base + haystack.charAt(i)) % mod);
        if (i > 0) power = (int)((long) power * base % mod);
    }

    for (int i = needle.length(); i <= haystack.length(); i++) {
        if (needleHash == windowHash) {
            if (haystack.substring(i - needle.length(), i).equals(needle)) {
                return i - needle.length();
            }
        }
        if (i < haystack.length()) {
            windowHash = (int)(((windowHash - haystack.charAt(i - needle.length()) * power) * base
                + haystack.charAt(i)) % mod);
            if (windowHash < 0) windowHash += mod;
        }
    }
    return -1;
}
```

---

## 10+ Hashing Problem Templates

| # | Problem | Hashing Pattern |
|---|---------|----------------|
| 1 | Two Sum | Complement tracking |
| 2 | Group Anagrams | Sort chars as key |
| 3 | Subarray Sum = K | Prefix sum + map |
| 4 | Top K Frequent | Frequency map + heap |
| 5 | LRU Cache | HashMap + doubly linked list |
| 6 | Valid Sudoku | HashSet per row/col/box |
| 7 | Happy Number | Cycle detection with set |
| 8 | Rabin-Karp | Rolling hash |
| 9 | Longest Consecutive | HashSet membership check |
| 10 | Randomized Set | HashMap + ArrayList |
| 11 | Encode/Decode Strings | Length prefix + delimiters |
| 12 | Minimum Window Substring | Sliding window + frequency map |
