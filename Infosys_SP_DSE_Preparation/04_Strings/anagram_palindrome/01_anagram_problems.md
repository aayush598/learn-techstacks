# Anagram Problems

## 1. Anagram Definition and Checking

```python
from collections import Counter, defaultdict

# Two strings are anagrams if they have same characters with same frequencies
def is_anagram_sort(s, t):
    """Check if t is anagram of s using sorting"""
    return sorted(s) == sorted(t)

# Time: O(n log n), Space: O(n)

def is_anagram_count(s, t):
    """Check if t is anagram of s using character counting"""
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

# Time: O(n), Space: O(k) where k is character set size

def is_anagram_counter(s, t):
    """Check using Counter"""
    return Counter(s) == Counter(t)

# Time: O(n), Space: O(k)

def is_anagram_array(s, t):
    """Check using fixed-size array (for lowercase letters)"""
    if len(s) != len(t):
        return False
    
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    for c in t:
        count[ord(c) - ord('a')] -= 1
        if count[ord(c) - ord('a')] < 0:
            return False
    return True

# Time: O(n), Space: O(1) (fixed 26)

# Test
print(is_anagram_sort("anagram", "nagaram"))    # True
print(is_anagram_count("rat", "car"))            # False
print(is_anagram_counter("listen", "silent"))    # True
print(is_anagram_array("hello", "olleh"))        # True
```

## 2. Group Anagrams (LeetCode 49)

```python
def group_anagrams(strs):
    """
    Group strings that are anagrams of each other
    Time: O(n * k log k) where k is max length
    Space: O(n * k)
    """
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Use sorted string as key
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    
    return list(anagram_map.values())

def group_anagrams_optimal(strs):
    """
    Optimal grouping using character count as key
    Time: O(n * k)
    Space: O(n * k)
    """
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Use character count as key (avoid sorting)
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        anagram_map[key].append(s)
    
    return list(anagram_map.values())

# Test
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

print(group_anagrams_optimal(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

## 3. Find All Anagram Substrings in a String

```python
def find_anagrams(s, p):
    """
    Find all start indices of p's anagrams in s
    Time: O(n) using sliding window
    Space: O(k) where k is character set size
    """
    n, m = len(s), len(p)
    if m > n:
        return []
    
    p_count = Counter(p)
    window_count = Counter()
    
    result = []
    
    for i in range(n):
        # Add character to window
        window_count[s[i]] += 1
        
        # Remove character from left if window too large
        if i >= m:
            left_char = s[i - m]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
        
        # Check if window matches
        if i >= m - 1 and window_count == p_count:
            result.append(i - m + 1)
    
    return result

def find_anagrams_optimized(s, p):
    """
    Optimized version using array comparison
    Time: O(n)
    Space: O(1)
    """
    n, m = len(s), len(p)
    if m > n:
        return []
    
    p_count = [0] * 26
    window_count = [0] * 26
    
    for c in p:
        p_count[ord(c) - ord('a')] += 1
    
    result = []
    
    for i in range(n):
        # Add right character
        window_count[ord(s[i]) - ord('a')] += 1
        
        # Remove left character
        if i >= m:
            window_count[ord(s[i - m]) - ord('a')] -= 1
        
        # Check match
        if i >= m - 1 and window_count == p_count:
            result.append(i - m + 1)
    
    return result

# Test
print(find_anagrams("cbaebabacd", "abc"))    # [0, 6]
print(find_anagrams_optimized("abab", "ab"))  # [0, 1, 2]
```

## 4. Minimum Number of Swaps to Make Anagram

```python
def min_swaps_to_make_anagram(s, t):
    """
    Find minimum swaps to make t an anagram of s
    Time: O(n)
    Space: O(k)
    """
    if len(s) != len(t):
        return -1
    
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        count[c] = count.get(c, 0) - 1
    
    # Count positive differences
    swaps = 0
    for v in count.values():
        if v > 0:
            swaps += v
    
    return swaps

def min_swaps_anagram_detailed(s, t):
    """Detailed version showing the swaps"""
    if len(s) != len(t):
        return -1, []
    
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        count[c] = count.get(c, 0) - 1
    
    # Separate excess and deficit
    excess = []
    deficit = []
    
    for c, v in count.items():
        if v > 0:
            excess.extend([c] * v)
        elif v < 0:
            deficit.extend([c] * (-v))
    
    swaps = []
    for i in range(len(excess)):
        swaps.append(f"Swap '{excess[i]}' with '{deficit[i]}'")
    
    return len(excess), swaps

# Test
print(min_swaps_to_make_anagram("abcd", "cbad"))  # 1
print(min_swaps_to_make_anagram("abc", "def"))     # 3
count, swaps = min_swaps_anagram_detailed("abcd", "cbad")
print(f"Swaps needed: {count}")
for swap in swaps:
    print(f"  {swap}")
```

## 5. Check if Strings Are Close (LeetCode 1657)

```python
def are_close(word1, word2):
    """
    Two strings are close if:
    1. They have same length
    2. Same characters with same frequencies
    3. Can transform by swapping characters (same multiset)
    """
    if len(word1) != len(word2):
        return False
    
    count1 = Counter(word1)
    count2 = Counter(word2)
    
    # Must have same characters
    if set(count1.keys()) != set(count2.keys()):
        return False
    
    # Must have same frequency distribution
    return sorted(count1.values()) == sorted(count2.values())

# Test
print(are_close("abc", "bca"))      # True
print(are_close("abc", "abd"))      # False
print(are_close("cabbba", "abbccc")) # False
print(are_close("aabbcc", "bbaacc")) # True
print(are_close("aabbcc", "aabbc"))  # False (different lengths)
```

## 6. Sort Characters by Frequency (LeetCode 451)

```python
def frequency_sort(s):
    """Sort characters by frequency in descending order"""
    count = Counter(s)
    
    # Sort by frequency (descending), then by character (descending for stability)
    sorted_chars = sorted(count.keys(), key=lambda c: (-count[c], -ord(c)))
    
    result = []
    for c in sorted_chars:
        result.append(c * count[c])
    
    return ''.join(result)

def frequency_sort_heap(s):
    """Using heap for frequency sort"""
    import heapq
    
    count = Counter(s)
    
    # Max heap (negate frequency for max heap)
    heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(heap)
    
    result = []
    while heap:
        freq, char = heapq.heappop(heap)
        result.append(char * (-freq))
    
    return ''.join(result)

# Test
print(frequency_sort("tree"))        # "eert" or "eetr"
print(frequency_sort("cccaaa"))      # "aaaccc" or "cccaaa"
print(frequency_sort("Aabb"))        # "bbAa" or "bbaA"
```

## 7. Custom Sort String (LeetCode 791)

```python
def custom_sort_string(order, s):
    """
    Sort s according to the order defined by order
    Characters not in order come at the end in any order
    """
    char_order = {}
    for i, c in enumerate(order):
        char_order[c] = i
    
    # Sort using custom key
    return ''.join(sorted(s, key=lambda c: char_order.get(c, 26)))

# Test
print(custom_sort_string("cba", "abcd"))    # "cbad" or "dcba"
print(custom_sort_string("bcafg", "abcd"))   # "bcad"
```

## 8. Anagram Substrings Count

```python
def count_anagram_substrings(s, pattern):
    """
    Count occurrences of pattern's anagrams in s
    Time: O(n)
    Space: O(k)
    """
    n, m = len(s), len(s)
    if m > len(pattern):
        return 0
    
    p_count = Counter(pattern)
    window_count = Counter()
    
    count = 0
    
    for i in range(n):
        window_count[s[i]] += 1
        
        if i >= len(pattern):
            left_char = s[i - len(pattern)]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
        
        if i >= len(pattern) - 1 and window_count == p_count:
            count += 1
    
    return count

def count_all_anagram_pairs(s):
    """Count pairs of anagram substrings"""
    n = len(s)
    anagram_count = defaultdict(int)
    total_pairs = 0
    
    # Check all substring lengths
    for length in range(1, n + 1):
        window_count = Counter()
        
        for i in range(n):
            window_count[s[i]] += 1
            
            if i >= length:
                left_char = s[i - length]
                window_count[left_char] -= 1
                if window_count[left_char] == 0:
                    del window_count[left_char]
            
            if i >= length - 1:
                key = tuple(sorted(window_count.items()))
                total_pairs += anagram_count[key]
                anagram_count[key] += 1
    
    return total_pairs

# Test
print(count_anagram_substrings("forxxorfxdofr", "for"))  # 3
print(count_all_anagram_pairs("abba"))  # 4 (anagram pairs)
```

## 9. Minimum Index Sum for Two Restaurant Lists

```python
def find_restaurant(list1, list2):
    """
    Find restaurants with minimum index sum
    Time: O(n + m)
    Space: O(n)
    """
    index_map = {name: i for i, name in enumerate(list1)}
    
    min_sum = float('inf')
    result = []
    
    for j, name in enumerate(list2):
        if name in index_map:
            index_sum = index_map[name] + j
            if index_sum < min_sum:
                min_sum = index_sum
                result = [name]
            elif index_sum == min_sum:
                result.append(name)
    
    return result

# Test
list1 = ["Shogun", "Tapioca Express", "Burger King", "KFC"]
list2 = ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"]
print(find_restaurant(list1, list2))  # ["Shogun"]
```

## 10. Find All Anagrams in a String (Streaming)

```python
def find_anagrams_streaming(s, p):
    """
    Find anagrams with early termination
    Useful for streaming data
    """
    from collections import Counter
    
    n, m = len(s), len(p)
    if m > n:
        return []
    
    p_count = Counter(p)
    window_count = Counter()
    
    result = []
    match_count = 0
    
    for i in range(n):
        # Add character
        char = s[i]
        if window_count[char] < p_count.get(char, 0):
            match_count += 1
        window_count[char] += 1
        
        # Remove character if window too large
        if i >= m:
            left_char = s[i - m]
            if window_count[left_char] <= p_count.get(left_char, 0):
                match_count -= 1
            window_count[left_char] -= 1
        
        # Check if all characters match
        if match_count == m:
            result.append(i - m + 1)
    
    return result

# Test
print(find_anagrams_streaming("cbaebabacd", "abc"))  # [0, 6]
```
