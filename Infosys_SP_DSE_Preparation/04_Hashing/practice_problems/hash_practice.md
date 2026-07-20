# Hashing Practice Problems

## Easy Problems

### 1. Valid Anagram (LeetCode 242)

```python
from collections import Counter

def is_anagram(s, t):
    """
    Check if t is an anagram of s
    Time: O(n), Space: O(1)
    """
    if len(s) != len(t):
        return False
    
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        count[c] = count.get(c, 0) - 1
        if count[c] < 0:
            return False
    return True

# Test
print(is_anagram("anagram", "nagaram"))  # True
print(is_anagram("rat", "car"))          # False
```

### 2. Isomorphic Strings (LeetCode 205)

```python
def is_isomorphic(s, t):
    """
    Check if s and t are isomorphic
    Time: O(n), Space: O(k) where k is character set
    """
    if len(s) != len(t):
        return False
    
    s_to_t = {}
    t_to_s = {}
    
    for c1, c2 in zip(s, t):
        if c1 in s_to_t:
            if s_to_t[c1] != c2:
                return False
        else:
            s_to_t[c1] = c2
        
        if c2 in t_to_s:
            if t_to_s[c2] != c1:
                return False
        else:
            t_to_s[c2] = c1
    
    return True

# Test
print(is_isomorphic("egg", "add"))    # True
print(is_isomorphic("foo", "bar"))    # False
print(is_isomorphic("paper", "title"))  # True
```

### 3. Jewels and Stones (LeetCode 771)

```python
def num_jewels_in_stones(jewels, stones):
    """
    Count stones that are jewels
    Time: O(n + m), Space: O(m)
    """
    jewel_set = set(jewels)
    return sum(1 for stone in stones if stone in jewel_set)

# Test
print(num_jewels_in_stones("aA", "aAAbbbb"))  # 3
print(num_jewels_in_stones("z", "ZZ"))        # 0
```

### 4. Intersection of Two Arrays (LeetCode 349)

```python
def intersection(nums1, nums2):
    """
    Find intersection of two arrays
    Time: O(n + m), Space: O(min(n, m))
    """
    return list(set(nums1) & set(nums2))

def intersection_ii(nums1, nums2):
    """Find intersection with duplicates"""
    from collections import Counter
    count1 = Counter(nums1)
    result = []
    
    for num in nums2:
        if count1[num] > 0:
            result.append(num)
            count1[num] -= 1
    
    return result

# Test
print(intersection([1, 2, 2, 1], [2, 2]))      # [2]
print(intersection_ii([1, 2, 2, 1], [2, 2]))    # [2, 2]
```

### 5. Happy Number (LeetCode 202)

```python
def is_happy(n):
    """
    Check if n is a happy number
    Time: O(log n), Space: O(log n)
    """
    def get_next(num):
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total
    
    seen = set()
    
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)
    
    return n == 1

# Test
print(is_happy(19))  # True
print(is_happy(2))   # False
```

## Medium Problems

### 6. Group Anagrams (LeetCode 49)

```python
from collections import defaultdict

def group_anagrams(strs):
    """
    Group strings that are anagrams
    Time: O(n * k log k), Space: O(n * k)
    """
    anagram_map = defaultdict(list)
    
    for s in strs:
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    
    return list(anagram_map.values())

# Test
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

### 7. Longest Substring Without Repeating Characters (LeetCode 3)

```python
def length_of_longest_substring(s):
    """
    Find length of longest substring without repeating chars
    Time: O(n), Space: O(min(n, m))
    """
    char_index = {}
    max_len = 0
    left = 0
    
    for right, c in enumerate(s):
        if c in char_index and char_index[c] >= left:
            left = char_index[c] + 1
        char_index[c] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len

# Test
print(length_of_longest_substring("abcabcbb"))  # 3
print(length_of_longest_substring("bbbbb"))      # 1
print(length_of_longest_substring("pwwkew"))     # 3
```

### 8. Minimum Window Substring (LeetCode 76)

```python
from collections import Counter

def min_window(s, t):
    """
    Find minimum window containing all chars of t
    Time: O(n), Space: O(m)
    """
    if not s or not t:
        return ""
    
    dict_t = Counter(t)
    required = len(dict_t)
    
    filtered = [(c, i) for i, c in enumerate(s) if c in dict_t]
    l, r = 0, 0
    formed = 0
    window = {}
    
    ans = (float("inf"), 0, 0)
    
    while r < len(filtered):
        char = filtered[r][0]
        window[char] = window.get(char, 0) + 1
        
        if window[char] == dict_t[char]:
            formed += 1
        
        while l <= r and formed == required:
            char = filtered[l][0]
            end = filtered[r][1]
            start = filtered[l][1]
            
            if end - start + 1 < ans[0]:
                ans = (end - start + 1, start, end)
            
            window[char] -= 1
            if window[char] < dict_t[char]:
                formed -= 1
            l += 1
        
        r += 1
    
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]

# Test
print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
print(min_window("a", "a"))                # "a"
```

### 9. Subarray Sum Equals K (LeetCode 560)

```python
def subarray_sum(nums, k):
    """
    Count subarrays with sum k
    Time: O(n), Space: O(n)
    """
    count = 0
    prefix_sum = 0
    seen = {0: 1}
    
    for num in nums:
        prefix_sum += num
        
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    
    return count

# Test
print(subarray_sum([1, 1, 1], 2))        # 2
print(subarray_sum([1, 2, 3], 3))        # 2
```

### 10. Encode and Decode Strings (LeetCode 271)

```python
class Codec:
    """Encode and decode strings to/from single string"""
    
    def encode(self, strs):
        """Encode list of strings to single string"""
        return '|'.join(s.replace('|', '||') for s in strs)
    
    def decode(self, s):
        """Decode single string to list of strings"""
        return [part.replace('||', '|') for part in s.split('|')]

# Test
codec = Codec()
encoded = codec.encode(["lint", "code", "love", "you"])
print(f"Encoded: {encoded}")
decoded = codec.decode(encoded)
print(f"Decoded: {decoded}")
```

## Hard Problems

### 11. Sliding Window Maximum (LeetCode 239)

```python
from collections import deque

def max_sliding_window(nums, k):
    """
    Find max in each sliding window of size k
    Time: O(n), Space: O(k)
    """
    result = []
    dq = deque()
    
    for i in range(len(nums)):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Test
print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
```

### 12. Count of Smaller Numbers After Self (LeetCode 315)

```python
def count_smaller(nums):
    """
    Count smaller elements after each element
    Time: O(n log n), Space: O(n)
    """
    def merge_sort(enum):
        half = len(enum) // 2
        if half > 1:
            left = merge_sort(enum[:half])
            right = merge_sort(enum[half:])
            merge(left, right, enum)
        return enum
    
    def merge(left, right, enum):
        i = j = 0
        while i < len(left) or j < len(right):
            if j == len(right) or (i < len(left) and left[i][1] <= right[j][1]):
                enum[i + j] = left[i]
                count[left[i][0]] += j
                i += 1
            else:
                enum[i + j] = right[j]
                j += 1
    
    count = [0] * len(nums)
    merge_sort(list(enumerate(nums)))
    return count

# Test
print(count_smaller([5, 2, 6, 1]))  # [2, 1, 1, 0]
print(count_smaller([-1]))           # [0]
```

### 13. Max Points on a Line (LeetCode 149)

```python
from collections import defaultdict
from math import gcd

def max_points(points):
    """
    Find maximum number of points on same line
    Time: O(n^2), Space: O(n)
    """
    if len(points) <= 2:
        return len(points)
    
    def slope_key(p1, p2):
        """Get normalized slope as key"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        if dx == 0:
            return (0, 1)
        if dy == 0:
            return (1, 0)
        
        g = gcd(dx, dy)
        dx //= g
        dy //= g
        
        if dx < 0:
            dx, dy = -dx, -dy
        
        return (dx, dy)
    
    result = 1
    
    for i in range(len(points)):
        slopes = defaultdict(int)
        
        for j in range(i + 1, len(points)):
            slope = slope_key(points[i], points[j])
            slopes[slope] += 1
        
        if slopes:
            result = max(result, max(slopes.values()) + 1)
    
    return result

# Test
print(max_points([[1,1],[2,2],[3,3]]))  # 3
print(max_points([[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]))  # 4
```

### 14. Word Ladder (LeetCode 127)

```python
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    """
    Find shortest transformation sequence
    Time: O(n * m^2), Space: O(n * m)
    """
    word_set = set(word_list)
    
    if end_word not in word_set:
        return 0
    
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    
    while queue:
        word, steps = queue.popleft()
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i + 1:]
                
                if new_word == end_word:
                    return steps + 1
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, steps + 1))
    
    return 0

# Test
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))  # 5
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))  # 0
```

### 15. Longest Duplicate Substring (LeetCode 1044)

```python
def longest_dup_substring(s):
    """
    Find longest substring that appears at least twice
    Time: O(n log n), Space: O(n)
    """
    def check(length):
        if length == 0:
            return ""
        
        base, mod = 31, 10**9 + 7
        
        hash_count = {}
        current_hash = 0
        power = pow(base, length - 1, mod)
        
        for i in range(length):
            current_hash = (current_hash * base + ord(s[i])) % mod
        
        hash_count[current_hash] = [0]
        
        for i in range(1, len(s) - length + 1):
            current_hash = (current_hash - ord(s[i - 1]) * power) % mod
            current_hash = (current_hash * base + ord(s[i + length - 1])) % mod
            current_hash = (current_hash + mod) % mod
            
            if current_hash in hash_count:
                for pos in hash_count[current_hash]:
                    if s[pos:pos + length] == s[i:i + length]:
                        return s[i:i + length]
                hash_count[current_hash].append(i)
            else:
                hash_count[current_hash] = [i]
        
        return ""
    
    left, right = 0, len(s) - 1
    result = ""
    
    while left <= right:
        mid = (left + right) // 2
        found = check(mid)
        if found:
            result = found
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Test
print(longest_dup_substring("abcabc"))    # "abc"
print(longest_dup_substring("abcdabcd"))  # "abcd"
```

## Bonus Problems

### 16. Group Shifted Strings (LeetCode 249)

```python
from collections import defaultdict

def group_strings(strings):
    """Group strings that are shifts of each other"""
    groups = defaultdict(list)
    
    for s in strings:
        if not s:
            groups[""].append(s)
            continue
        
        # Normalize by shifting first char to 'a'
        shift = ord(s[0]) - ord('a')
        key = tuple((ord(c) - ord('a') - shift) % 26 for c in s)
        groups[key].append(s)
    
    return list(groups.values())

# Test
print(group_strings(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]))
```

### 17. Continuous Subarray Sum (LeetCode 523)

```python
def check_subarray_sum(nums, k):
    """
    Check if subarray sum is divisible by k
    Time: O(n), Space: O(k)
    """
    seen = {0: -1}
    prefix_sum = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in seen:
            if i - seen[remainder] >= 2:
                return True
        else:
            seen[remainder] = i
    
    return False

# Test
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 6))  # True
```

### 18. Find Duplicate Number (LeetCode 287)

```python
def find_duplicate(nums):
    """
    Find duplicate number in array
    Time: O(n), Space: O(1)
    """
    slow = fast = nums[0]
    
    # Find intersection point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # Find entrance to cycle
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow

# Test
print(find_duplicate([1, 3, 4, 2, 2]))  # 2
print(find_duplicate([3, 1, 3, 4, 2]))  # 3
```

### 19. Subarray Product Less Than K (LeetCode 713)

```python
def num_subarray_product_less_than_k(nums, k):
    """
    Count subarrays with product less than k
    Time: O(n), Space: O(1)
    """
    if k <= 1:
        return 0
    
    count = 0
    product = 1
    left = 0
    
    for right in range(len(nums)):
        product *= nums[right]
        
        while product >= k:
            product //= nums[left]
            left += 1
        
        count += right - left + 1
    
    return count

# Test
print(num_subarray_product_less_than_k([10, 5, 2, 6], 100))  # 8
```

### 20. Unique Email Addresses (LeetCode 929)

```python
def num_unique_emails(emails):
    """
    Count unique email addresses
    Time: O(n * m), Space: O(n * m)
    """
    unique = set()
    
    for email in emails:
        local, domain = email.split('@')
        
        # Process local name
        if '+' in local:
            local = local[:local.index('+')]
        
        local = local.replace('.', '')
        
        unique.add(f"{local}@{domain}")
    
    return len(unique)

# Test
print(num_unique_emails([
    "test.email+alex@leetcode.com",
    "test.e.mail+bob@leetcode.com",
    "testemail+david@leetcode.com"
]))  # 2
```

## Summary

```python
"""
KEY PATTERNS FOR HASHING PROBLEMS:

1. TWO SUM PATTERN:
   - Use hash map to store complements
   - O(n) time for any two-sum variant

2. FREQUENCY COUNTING:
   - Use Counter or defaultdict(int)
   - Useful for anagrams, duplicates, counting

3. GROUPING:
   - Use defaultdict(list)
   - Group by sorted string, frequency, etc.

4. SLIDING WINDOW WITH HASH:
   - Use Counter or dict for window state
   - O(n) for substring problems

5. PREFIX SUM WITH HASH:
   - Store prefix sums in hash map
   - O(n) for subarray sum problems

6. ROLLING HASH:
   - Polynomial hash for string matching
   - O(n) preprocessing, O(1) per query

7. ANAGRAM CHECKING:
   - Use Counter for O(n) comparison
   - Use array[26] for lowercase letters

8. PALINDROME CHECKING:
   - Use hash for O(1) substring comparison
   - Combine with expand-around-center
"""
```
