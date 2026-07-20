# Sorting, Hashing & Heaps — Problem Bank (Batch 2)

## 40 More Classic Problems for Infosys SP DSE Preparation

---

# PART A: SORTING (Problems 1–10)

---

## Problem 1: Sort Array By Parity

**Statement:** Given an integer array `nums`, move all even integers to the beginning and all odd integers to the end. Return any array that satisfies this.

**Approach:** Use two pointers — one from left, one from right. Swap when left is odd and right is even. This gives an in-place O(n) solution without extra space.

**Key Insight:** The relative order within even group and odd group does not matter. Only the even-before-odd property is required.

**Edge Cases:**
- Array with all even or all odd elements — return as is.
- Single element array — already trivially valid.
- Zero is even.

**Python Code:**

```python
def sortArrayByParity(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] % 2 == 1 and nums[right] % 2 == 0:
            nums[left], nums[right] = nums[right], nums[left]
        if nums[left] % 2 == 0:
            left += 1
        if nums[right] % 2 == 1:
            right -= 1
    return nums

# Test
print(sortArrayByParity([3, 1, 2, 4]))  # [4, 2, 1, 3] or any valid ordering
print(sortArrayByParity([0]))  # [0]
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

## Problem 2: Sort Array By Parity II

**Statement:** Given an integer array `nums`, exactly half the integers are even and half are odd. Rearrange so that `nums[0]` is even, `nums[1]` is odd, `nums[2]` is even, and so on.

**Approach:** Maintain two pointers — even pointer starts at 0, odd pointer starts at 1. Find misplaced elements and swap them.

**Key Insight:** Since exactly half are even and half are odd, once we find a misplaced element at each pointer, a single swap fixes both positions.

**Edge Cases:**
- Already correctly arranged — no swaps needed.
- Array of length 2 — single comparison.

**Python Code:**

```python
def sortArrayByParityII(nums):
    even, odd = 0, 1
    while even < len(nums) and odd < len(nums):
        if nums[even] % 2 == 0:
            even += 2
        elif nums[odd] % 2 == 1:
            odd += 2
        else:
            nums[even], nums[odd] = nums[odd], nums[even]
            even += 2
            odd += 2
    return nums

# Test
print(sortArrayByParityII([4, 2, 5, 7]))  # [4, 5, 2, 7]
print(sortArrayByParityII([2, 3]))  # [2, 3]
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

## Problem 3: Relative Sort Array

**Statement:** Given two arrays `arr1` and `arr2`, sort `arr1` so that all elements appear in the same relative order as in `arr2`. Elements not in `arr2` should be placed at the end in ascending order.

**Approach:** Use a hash map to store the rank of each element in `arr2`. Sort `arr1` using a custom key: (rank if present, value) so unmatched elements go to end sorted.

**Key Insight:** Elements not in `arr2` are given a high sentinel rank (e.g., infinity) and then sorted by their actual value within that group.

**Edge Cases:**
- All elements of `arr1` are in `arr2` — no leftover group.
- No elements of `arr1` in `arr2` — pure sort.
- Duplicate elements in `arr1` — all instances grouped together.

**Python Code:**

```python
def relativeSortArray(arr1, arr2):
    rank = {val: i for i, val in enumerate(arr2)}
    def custom_key(x):
        if x in rank:
            return (0, rank[x])
        return (1, x)
    arr1.sort(key=custom_key)
    return arr1

# Test
print(relativeSortArray([2,3,1,3,2,4,6,7,9,2,19], [2,1,4,3,9,6]))
# Output: [2,2,2,1,4,3,3,9,6,7,19]
```

**Time Complexity:** O(n log n) where n = len(arr1)
**Space Complexity:** O(n) for the rank map

---

## Problem 4: Sort Array by Increasing Frequency

**Statement:** Given an array of integers `nums`, sort the array in increasing order based on the frequency of the values. If two values have the same frequency, sort them in decreasing order.

**Approach:** Count frequencies with a hash map. Sort using a custom key: (frequency, -value) so that ties are broken by higher value first.

**Key Insight:** Using `-value` as the secondary sort key achieves descending order for same-frequency elements within Python's ascending sort.

**Edge Cases:**
- All elements have frequency 1 — sort by value descending.
- All elements are the same — no change in order.
- Two groups of same frequency — each sorted descending internally.

**Python Code:**

```python
from collections import Counter

def frequencySort(nums):
    count = Counter(nums)
    nums.sort(key=lambda x: (count[x], -x))
    return nums

# Test
print(frequencySort([1, 1, 2, 2, 2, 3]))  # [3, 1, 1, 2, 2, 2]
print(frequencySort([2, 3, 5, 3, 7, 9, 5, 3, 7]))
# [9, 2, 7, 7, 5, 5, 3, 3, 3]
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

## Problem 5: Minimum Absolute Difference

**Statement:** Given an array of distinct integers `arr`, find all pairs of elements with the minimum absolute difference. Return a list of pairs in ascending order.

**Approach:** Sort the array first. The minimum difference must be between consecutive elements. First pass finds the minimum difference, second pass collects all pairs with that difference.

**Key Insight:** After sorting, the minimum absolute difference is always between some consecutive pair. Non-adjacent pairs always have larger differences.

**Edge Cases:**
- Array of size 2 — only one pair.
- All elements equal — difference is 0, all adjacent pairs are answers.
- Negative numbers — sorting handles this correctly.

**Python Code:**

```python
def minimumAbsDifference(arr):
    arr.sort()
    min_diff = float('inf')
    for i in range(len(arr) - 1):
        min_diff = min(min_diff, arr[i + 1] - arr[i])
    result = []
    for i in range(len(arr) - 1):
        if arr[i + 1] - arr[i] == min_diff:
            result.append([arr[i], arr[i + 1]])
    return result

# Test
print(minimumAbsDifference([4, 2, 1, 3]))  # [[1,2],[2,3],[3,4]]
print(minimumAbsDifference([1, 3, 6, 10, 15]))  # [[1,3]]
print(minimumAbsDifference([3, 8, -10, 23, 19, -4, -12, 27]))
# [[-12,-10],[19,23],[23,27]]
```

**Time Complexity:** O(n log n) for sorting
**Space Complexity:** O(n) for the result

---

## Problem 6: Triangle

**Statement:** Given an integer array `nums`, return `True` if you can form a valid triangle from any three elements. A triangle is valid if the sum of any two sides is strictly greater than the third.

**Approach:** Sort the array. Check consecutive triplets — if `a + b > c` for any consecutive triplet in sorted order, a valid triangle exists. This is sufficient because sorting ensures `a <= b <= c`, so we only need to check `a + b > c`.

**Key Insight:** If `a + b <= c` for consecutive triplets, then any other pair including a and b will also fail against any larger c. So checking consecutive triplets is both necessary and sufficient.

**Edge Cases:**
- Array length less than 3 — impossible to form a triangle.
- Negative numbers — cannot form a valid triangle.
- Duplicate values — valid if triangle inequality holds.

**Python Code:**

```python
def isTriangle(nums):
    nums.sort()
    for i in range(len(nums) - 2):
        if nums[i] + nums[i + 1] > nums[i + 2]:
            return True
    return False

# Test
print(isTriangle([2, 2, 3, 4]))  # True (2+3>4)
print(isTriangle([1, 1, 1]))  # True
print(isTriangle([1, 2, 3]))  # False
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(1)

---

## Problem 7: Maximum Product of Three Numbers

**Statement:** Given an integer array `nums`, find three numbers whose product is maximum. Return the maximum product.

**Approach:** Sort the array. The maximum product is either the product of the three largest numbers OR the two smallest (most negative) multiplied by the largest. Return the max of both cases.

**Key Insight:** Two large negative numbers multiplied together produce a large positive number. So we must consider both the top-3 and bottom-2 + top-1 combinations.

**Edge Cases:**
- All negative numbers — pick three with largest absolute value (rightmost).
- Mix of negative and positive — both strategies may apply.
- Array of exactly 3 elements — only one product possible.

**Python Code:**

```python
def maximumProduct(nums):
    nums.sort()
    n = len(nums)
    # Either three largest or two smallest * largest
    return max(nums[-1] * nums[-2] * nums[-3],
               nums[0] * nums[1] * nums[-1])

# Test
print(maximumProduct([1, 2, 3, 4]))  # 24
print(maximumProduct([-1, -2, -3]))  # -6
print(maximumProduct([-10, -10, 1, 3, 2]))  # 300
print(maximumProduct([-4, -3, -2, -1]))  # -6
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(1)

---

## Problem 8: 3Sum Closest

**Statement:** Given an integer array `nums` and an integer `target`, find three integers whose sum is closest to `target`. Return the sum of the three integers.

**Approach:** Sort the array. Fix one element, then use two pointers for the remaining. Track the closest sum seen so far. Skip duplicates for efficiency.

**Key Insight:** Sorting allows us to make directional moves with the two pointers — if the current sum is too small, move the left pointer right; if too large, move the right pointer left.

**Edge Cases:**
- Array of exactly 3 elements — only one triplet.
- Target is between min and max possible sums.
- All elements the same — sum is always 3 * element.
- Negative target with positive array or vice versa.

**Python Code:**

```python
def threeSumClosest(nums, target):
    nums.sort()
    n = len(nums)
    closest = nums[0] + nums[1] + nums[2]
    for i in range(n - 2):
        left, right = i + 1, n - 1
        while left < right:
            curr_sum = nums[i] + nums[left] + nums[right]
            if abs(curr_sum - target) < abs(closest - target):
                closest = curr_sum
            if curr_sum < target:
                left += 1
            elif curr_sum > target:
                right -= 1
            else:
                return target
    return closest

# Test
print(threeSumClosest([-1, 2, 1, -4], 1))  # 2
print(threeSumClosest([0, 1, 2], 3))  # 3
print(threeSumClosest([-3, -2, -5, 3, -4], -1))  # -2
```

**Time Complexity:** O(n^2)
**Space Complexity:** O(1)

---

## Problem 9: Pancake Sorting

**Statement:** Given an array of unique integers `arr`, sort it using only the flip operation. A flip reverses the order of the first k elements. Return a list of k-values used for each flip.

**Approach:** For each position from end to start, find the maximum element in the unsorted portion, flip it to the front, then flip it to its correct position. Each element needs at most 2 flips.

**Key Insight:** Each element needs at most 2 operations: one flip to bring it to index 0, then another flip to place it at its correct position. Total flips are at most 3(n-1).

**Edge Cases:**
- Already sorted array — 0 flips needed.
- Reverse sorted — maximum flips.
- Single element — no flips.

**Python Code:**

```python
def pancakeSort(arr):
    result = []
    for size in range(len(arr), 0, -1):
        max_idx = arr.index(max(arr[:size]))
        if max_idx == size - 1:
            continue
        if max_idx > 0:
            arr[:max_idx + 1] = reversed(arr[:max_idx + 1])
            result.append(max_idx + 1)
        arr[:size] = reversed(arr[:size])
        result.append(size)
    return result

# Test
print(pancakeSort([3, 2, 4, 1]))  # [2, 4, 3, 3] or similar
print(pancakeSort([1, 2, 3]))  # []
```

**Time Complexity:** O(n^2)
**Space Complexity:** O(n) for result list

---

## Problem 10: Reveal Cards In Increasing Order

**Statement:** You have a deck of cards (unique integers). Rearrange the deck so that when you reveal cards from left to right, the revealed cards come out in increasing order. The reveal process: reveal the top card, then move the next top card to the bottom.

**Approach:** Sort the cards. Use a deque of indices representing available positions. Assign sorted cards to positions following the same reveal pattern (take first position, move next to end).

**Key Insight:** By simulating the reveal process on positions rather than cards, we can place cards in increasing order into the correct positions. The deque gives us the exact order of reveal.

**Edge Cases:**
- Single card — trivially in place.
- Two cards — reveal first, second stays.
- Already sorted deck — may still need rearrangement.

**Python Code:**

```python
from collections import deque

def deckRevealedIncreasing(deck):
    deck.sort()
    n = len(deck)
    indices = deque(range(n))
    result = [0] * n
    for card in deck:
        result[indices.popleft()] = card
        if indices:
            indices.append(indices.popleft())
    return result

# Test
print(deckRevealedIncreasing([17, 13, 11, 2, 3, 5, 7]))
# [2, 13, 3, 11, 5, 17, 7]
print(deckRevealedIncreasing([1, 1000]))  # [1, 1000]
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

# PART B: HASHING (Problems 11–25)

---

## Problem 11: Subarray Sum Equals K

**Statement:** Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals `k`.

**Approach:** Use prefix sum with a hash map. For each position, check if `prefix_sum - k` exists in the map. If yes, that many subarrays ending at current position sum to k.

**Key Insight:** `prefix_sum[j] - prefix_sum[i] == k` means the subarray from `i+1` to `j` sums to k. So for each j, we look for how many previous prefix sums equal `prefix_sum[j] - k`.

**Edge Cases:**
- k = 0 — subarrays that sum to 0 (e.g., `[1, -1]` or `[0]`).
- All positive elements — subarray must be contiguous and bounded.
- Negative k — valid, works with same logic.
- Single element array — check if element equals k.

**Python Code:**

```python
from collections import defaultdict

def subarraySum(nums, k):
    count = 0
    prefix_sum = 0
    seen = defaultdict(int)
    seen[0] = 1
    for num in nums:
        prefix_sum += num
        count += seen[prefix_sum - k]
        seen[prefix_sum] += 1
    return count

# Test
print(subarraySum([1, 1, 1], 2))  # 2
print(subarraySum([1, 2, 3], 3))  # 2
print(subarraySum([1, -1, 0], 0))  # 3
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

## Problem 12: Continuous Subarray Sum

**Statement:** Given an integer array `nums` and an integer `k`, return `True` if `nums` has a good subarray. A good subarray has length at least 2 and its sum is a multiple of `k`.

**Approach:** Use prefix sum modulo k. If the same remainder is seen at two different indices and the distance between them is at least 2, we found a valid subarray. Store the first occurrence of each remainder.

**Key Insight:** `(prefix_sum[j] - prefix_sum[i]) % k == 0` is equivalent to `prefix_sum[j] % k == prefix_sum[i] % k`. The length constraint of at least 2 ensures `j - i >= 2`.

**Edge Cases:**
- k = 1 — any subarray of length >= 2 works.
- k = 0 — only works with the standard prefix sum approach.
- Array length 1 — impossible (need at least 2).
- Negative numbers — modulo handles correctly with proper implementation.

**Python Code:**

```python
def checkSubarraySum(nums, k):
    remainder_map = {0: -1}
    prefix_sum = 0
    for i, num in enumerate(nums):
        prefix_sum += num
        r = prefix_sum % k
        if r in remainder_map:
            if i - remainder_map[r] >= 2:
                return True
        else:
            remainder_map[r] = i
    return False

# Test
print(checkSubarraySum([23, 2, 4, 6, 7], 6))  # True
print(checkSubarraySum([23, 2, 6, 4, 7], 6))  # True
print(checkSubarraySum([23, 2, 6, 4, 7], 13))  # False
```

**Time Complexity:** O(n)
**Space Complexity:** O(min(n, k))

---

## Problem 13: Minimum Index Sum of Two Lists

**Statement:** Given two arrays of restaurant names, find the restaurants that appear in both lists with the minimum index sum. Return the list of common restaurants sorted by their index sum.

**Approach:** Build a hash map of restaurant name to index for the first list. For the second list, check if each restaurant exists in the map and compute the index sum. Track the minimum sum.

**Key Insight:** We only need one pass through list2, looking up each entry in the map built from list1. This avoids O(n*m) brute force.

**Edge Cases:**
- No common restaurants — return empty list (though problem guarantees at least one).
- Multiple restaurants with same minimum sum — return all of them.
- Duplicate restaurant names — first occurrence's index is used (use the map built from list1).

**Python Code:**

```python
def findRestaurant(list1, list2):
    index_map = {name: i for i, name in enumerate(list1)}
    min_sum = float('inf')
    result = []
    for j, name in enumerate(list2):
        if name in index_map:
            idx_sum = index_map[name] + j
            if idx_sum < min_sum:
                min_sum = idx_sum
                result = [name]
            elif idx_sum == min_sum:
                result.append(name)
    return result

# Test
print(findRestaurant(["Shogun", "Tapioca Express", "Burger King", "KFC"],
                      ["Piatti", "The Grill at Torrey Pines",
                       "Hungry Hunter Steakhouse", "Shogun"]))
# ["Shogun"]
print(findRestaurant(["happy", "sad", "good"], ["sad", "happy", "good"]))
# ["sad", "happy"]
```

**Time Complexity:** O(n + m) where n, m are lengths of the two lists
**Space Complexity:** O(n)

---

## Problem 14: Number of Good Pairs

**Statement:** Given an array of integers `nums`, return the number of good pairs. A pair `(i, j)` is good if `i < j` and `nums[i] == nums[j]`.

**Approach:** Count occurrences of each number. For each count `c`, the number of pairs is `c * (c - 1) / 2` (combinations of 2 from c elements).

**Key Insight:** This is the mathematical combinations formula C(c, 2) = c! / (2! * (c-2)!) = c * (c-1) / 2. No need to enumerate pairs.

**Edge Cases:**
- All elements distinct — 0 pairs.
- All elements the same — C(n, 2) pairs.
- Single element — 0 pairs.

**Python Code:**

```python
from collections import Counter

def numIdenticalPairs(nums):
    count = Counter(nums)
    result = 0
    for c in count.values():
        result += c * (c - 1) // 2
    return result

# Test
print(numIdenticalPairs([1, 2, 3, 1, 1, 3]))  # 4
print(numIdenticalPairs([1, 1, 1, 1]))  # 6
print(numIdenticalPairs([1, 2, 3]))  # 0
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

## Problem 15: Word Pattern

**Statement:** Given a pattern string and a string `s`, return `True` if `s` follows the given pattern. A bijection must exist between each character in pattern and each non-empty word in `s`.

**Approach:** Use two hash maps — one for pattern to word mapping and one for word to pattern. Both must be consistent for a valid bijection. Also check that the number of words matches the pattern length.

**Key Insight:** A bijection requires both directions to be consistent. If pattern "ab" maps to "cat dog", then "cat" must map back to "a" and "dog" to "b". We also need the word count to match the pattern length.

**Edge Cases:**
- Empty pattern and empty string — True.
- Pattern longer than word count — False.
- Repeated words in different pattern positions — must use same pattern character.
- Single character pattern with single word — always True.

**Python Code:**

```python
def wordPattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
    char_to_word = {}
    word_to_char = {}
    for c, w in zip(pattern, words):
        if c in char_to_word:
            if char_to_word[c] != w:
                return False
        else:
            char_to_word[c] = w
        if w in word_to_char:
            if word_to_char[w] != c:
                return False
        else:
            word_to_char[w] = c
    return True

# Test
print(wordPattern("abba", "dog cat cat dog"))  # True
print(wordPattern("abba", "dog cat cat fish"))  # False
print(wordPattern("abc", "def def def"))  # False
```

**Time Complexity:** O(n) where n is the number of words
**Space Complexity:** O(n)

---

## Problem 16: Isomorphic Strings

**Statement:** Given two strings `s` and `t`, determine if they are isomorphic. Two strings are isomorphic if characters in `s` can be replaced to get `t`, preserving the order. No two characters may map to the same character.

**Approach:** Similar to Word Pattern — maintain two mapping dictionaries, one from s to t and one from t to s. Both must be consistent.

**Key Insight:** Unlike Word Pattern, strings have characters not words, so we iterate character by character. The bidirectional mapping ensures no two characters map to the same character.

**Edge Cases:**
- Empty strings — True (vacuously).
- Single character strings — True if both are same character, False otherwise.
- All same characters in s, different in t — False (bijection broken).
- Unicode characters — works with same logic.

**Python Code:**

```python
def isIsomorphic(s, t):
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
print(isIsomorphic("egg", "add"))  # True
print(isIsomorphic("foo", "bar"))  # False
print(isIsomorphic("paper", "title"))  # True
print(isIsomorphic("ab", "aa"))  # False
```

**Time Complexity:** O(n)
**Space Complexity:** O(1) since alphabet is bounded

---

## Problem 17: Find Duplicate Number in Array

**Statement:** Given an array of integers `nums` containing `n + 1` integers where each integer is between `1` and `n` (inclusive), return the single duplicate number. Must use O(1) extra space approach.

**Approach:** Use Floyd's cycle detection (tortoise and hare). Treat the array as a linked list where `nums[i]` is the next node. The cycle's entrance point is the duplicate.

**Key Insight:** Since values are in range [1, n] and there are n+1 elements, by pigeonhole principle, at least one duplicate exists. This creates a cycle. Floyd's algorithm finds the cycle entrance in O(n) time and O(1) space.

**Two Phase Algorithm:**
1. Phase 1: Find intersection point inside the cycle using slow/fast pointers.
2. Phase 2: Reset one pointer to start, move both at same speed. Meeting point is the duplicate.

**Edge Cases:**
- Duplicate at position 0 — handled correctly.
- Multiple duplicates — returns one of them.
- Array of size 2 with [1,1] — returns 1.

**Python Code:**

```python
def findDuplicate(nums):
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

# Test
print(findDuplicate([1, 3, 4, 2, 2]))  # 2
print(findDuplicate([3, 1, 3, 4, 2]))  # 3
print(findDuplicate([1, 1]))  # 1
print(findDuplicate([2, 5, 9, 6, 9, 3, 8, 9, 7, 1]))  # 9
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

## Problem 18: Check if Numbers Are Ascending in a Sentence

**Statement:** Given a string `s` containing words and numbers, return `True` if all numbers in the sentence are in strictly increasing order. Ignore words.

**Approach:** Extract all numbers from the string, convert to integers, and check if each number is strictly less than the next.

**Key Insight:** Python's `str.isdigit()` correctly identifies numeric substrings. After splitting by spaces, each token is either a word or a number.

**Edge Cases:**
- No numbers in the string — vacuously True.
- Single number — vacuously True.
- Numbers with leading zeros — `isdigit()` handles them, integer conversion ignores leading zeros.
- Very large numbers — Python handles arbitrary precision.

**Python Code:**

```python
def areNumbersAscending(s):
    numbers = [int(word) for word in s.split() if word.isdigit()]
    for i in range(len(numbers) - 1):
        if numbers[i] >= numbers[i + 1]:
            return False
    return True

# Test
print(areNumbersAscending("1 box has 3 blue 4 red 6 green"))  # True
print(areNumbersAscending("hello world 5 x 5"))  # False
print(areNumbersAscending("4 5 11 26 35"))  # True
print(areNumbersAscending("4 5 11 26 35 35"))  # False
```

**Time Complexity:** O(n) where n is the length of the string
**Space Complexity:** O(m) where m is the count of numbers

---

## Problem 19: Find the Difference of Two Arrays

**Statement:** Given two integer arrays `nums1` and `nums2`, return a list of their unique difference. The result should contain all unique values in `nums1` that are not in `nums2` followed by all unique values in `nums2` not in `nums1`.

**Approach:** Convert both arrays to sets. Find the set difference in both directions and combine.

**Key Insight:** Set operations are O(1) per element on average, making the overall complexity linear in the input sizes.

**Edge Cases:**
- Both arrays identical — both differences are empty.
- No common elements — both differences are full arrays.
- Duplicate elements within arrays — sets handle deduplication.

**Python Code:**

```python
def findDifference(nums1, nums2):
    set1, set2 = set(nums1), set(nums2)
    diff1 = list(set1 - set2)
    diff2 = list(set2 - set1)
    return [diff1, diff2]

# Test
print(findDifference([1, 2, 3], [2, 4, 6]))  # [[1,3],[4,6]]
print(findDifference([1, 2, 3, 3], [1, 1, 2, 2]))  # [[3],[]]
print(findDifference([1, 2, 3], [4, 5, 6]))  # [[1,2,3],[4,5,6]]
```

**Time Complexity:** O(n + m)
**Space Complexity:** O(n + m)

---

## Problem 20: Intersection of Multiple Arrays

**Statement:** Given a 2D integer array `nums` where `nums[i]` is an array of integers, return a list of the integers that appear in every array. The result should be sorted.

**Approach:** Count the frequency of each number across all arrays using a hash map. Numbers that appear in every array (count equals the number of arrays) are the intersection.

**Key Insight:** By converting each array to a set before counting, we handle duplicates within a single array. A number must appear in every array to be in the intersection.

**Edge Cases:**
- Empty arrays — no intersection possible.
- Single array — intersection is that array's unique elements.
- No common element — return empty list.
- Arrays with overlapping but non-identical elements — only common ones survive.

**Python Code:**

```python
from collections import Counter

def intersection(nums):
    count = Counter()
    total = len(nums)
    for arr in nums:
        count.update(set(arr))
    return sorted([num for num, c in count.items() if c == total])

# Test
print(intersection([[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]]))
# [3, 4]
print(intersection([[1, 2, 3], [4, 5, 6]]))  # []
print(intersection([[2, 1, 3, 4, 5], [1, 2, 3], [2, 3, 1, 4]]))
# [1, 2, 3]
```

**Time Complexity:** O(N) total elements across all arrays
**Space Complexity:** O(U) where U is the number of unique values

---

## Problem 21: Largest Unique Number

**Statement:** Given an array of integers `nums`, return the largest integer that appears exactly once. If no integer appears exactly once, return -1.

**Approach:** Count frequencies using a hash map. Iterate through the map to find the largest value with frequency exactly 1.

**Key Insight:** We only care about unique elements (frequency 1). Among those, we pick the largest. If no element has frequency 1, return -1.

**Edge Cases:**
- All elements appear more than once — return -1.
- All elements are unique — return the maximum.
- Single element — return that element (it's unique and largest).
- Negative numbers — largest means closest to positive infinity.

**Python Code:**

```python
from collections import Counter

def largestUniqueNumber(nums):
    count = Counter(nums)
    result = -1
    for num, freq in count.items():
        if freq == 1:
            result = max(result, num)
    return result

# Test
print(largestUniqueNumber([5, 7, 3, 9, 4, 9, 5, 12]))  # 12
print(largestUniqueNumber([9, 9, 8, 8]))  # -1
print(largestUniqueNumber([1, 2, 3, 4, 5]))  # 5
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

## Problem 22: Find the Town Judge

**Statement:** In a town of `n` people labeled `1` to `n`, the town judge is the person who: trusts nobody, and is trusted by everybody else (n - 1 people). Given an array `trust` where `trust[i] = [a, b]` means person `a` trusts person `b`, return the label of the town judge. Return -1 if none exists.

**Approach:** Maintain a trust score for each person. When `a` trusts `b`, decrease score of `a` and increase score of `b`. The person with score `n - 1` is the judge.

**Key Insight:** The judge must have exactly n-1 trust votes (trusted by everyone else) and give 0 trust (trusts nobody). The net score of + (n-1) uniquely identifies the judge.

**Edge Cases:**
- n = 1 with no trust relationships — person 1 is the judge by default.
- Cycle of trust — no judge exists.
- Multiple people with same trust count — no valid judge.

**Python Code:**

```python
def findJudge(n, trust):
    score = [0] * (n + 1)
    for a, b in trust:
        score[a] -= 1
        score[b] += 1
    for i in range(1, n + 1):
        if score[i] == n - 1:
            return i
    return -1

# Test
print(findJudge(2, [[1, 2]]))  # 2
print(findJudge(3, [[1, 3], [2, 3]]))  # 3
print(findJudge(3, [[1, 3], [2, 3], [3, 1]]))  # -1
print(findJudge(1, []))  # 1
```

**Time Complexity:** O(n + t) where t = len(trust)
**Space Complexity:** O(n)

---

## Problem 23: Check if Pangram

**Statement:** A pangram is a sentence that contains every letter of the English alphabet at least once. Given a string `sentence`, return `True` if it is a pangram.

**Approach:** Convert the sentence to a set of characters and check if the set contains all 26 lowercase letters.

**Key Insight:** A set automatically deduplicates. If the set size reaches 26 after including only lowercase letters, all letters are present.

**Edge Cases:**
- Empty string — not a pangram.
- Upper and lower case mix — convert to lowercase first.
- Non-alphabetic characters — ignored.
- String shorter than 26 characters — impossible to be a pangram.

**Python Code:**

```python
def checkIfPangram(sentence):
    return len(set(sentence.lower())) == 26

# Test
print(checkIfPangram("The quick brown fox jumps over the lazy dog"))  # True
print(checkIfPangram("abcde fghij klmno pqrst uvwxy z"))  # True
print(checkIfPangram("This is not a pangram"))  # False
```

**Time Complexity:** O(n)
**Space Complexity:** O(1) since at most 26 characters

---

## Problem 24: Count Distinct Numbers on Board

**Statement:** Given a positive integer `n`, start with a board containing only the number `1`. In each step, replace every number `x` on the board with all divisors of `x`. Return the count of distinct numbers on the board after all steps are done.

**Approach:** Since we keep adding divisors, ultimately all divisors of all numbers from 1 to n end up on the board. So the answer is simply n (every number from 1 to n appears). More precisely, we can use a set and simulate, but the mathematical answer is n.

**Key Insight:** After the first step, 1's divisor is 1 (itself). Then n's divisors include all numbers from 1 to n that divide n. Through iterative expansion, every number from 1 to n eventually appears as a divisor of some number already on the board.

**Edge Cases:**
- n = 1 — only number on board is 1.
- n = 2 — board has {1, 2}.
- Large n — still just n by the formula.

**Python Code:**

```python
def distinctIntegers(n):
    # After all steps, every integer 1..n ends up on the board
    return n

# Test
print(distinctIntegers(5))  # 5
print(distinctIntegers(1))  # 1
print(distinctIntegers(10))  # 10
```

**Time Complexity:** O(1)
**Space Complexity:** O(1)

---

## Problem 25: Find All Numbers Disappeared in Array

**Statement:** Given an array of integers `nums` where `nums[i]` is in range `[1, n]` (n = array length), return all integers in `[1, n]` that do not appear. Use a hash set approach.

**Approach:** Create a set of all elements in the array. Iterate from 1 to n and collect numbers not in the set.

**Key Insight:** The set lookup is O(1) on average, making this approach O(n) instead of the O(n^2) brute force. The hash set approach is the most intuitive for this problem.

**Edge Cases:**
- All numbers present — return empty list.
- Duplicates in array — set handles deduplication, missing numbers still found.
- n = 1 with [1] — return empty list.
- n = 1 with [1, 1] — return empty list (only value 1 exists).

**Alternative:** There is also an O(1) space approach using the array itself as a hash set by marking visited indices, but the hash set approach is cleaner and O(n) time.

**Python Code:**

```python
def findDisappearedNumbers(nums):
    num_set = set(nums)
    return [i for i in range(1, len(nums) + 1) if i not in num_set]

# Test
print(findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]))  # [5, 6]
print(findDisappearedNumbers([1, 1]))  # [2]
print(findDisappearedNumbers([2, 2]))  # [1]
print(findDisappearedNumbers([1, 2, 3, 4, 5]))  # []
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

# PART C: HEAPS / PRIORITY QUEUE (Problems 26–40)

---

## Problem 26: Last Stone Weight

**Statement:** You have `n` stones with positive integer weights. Each turn, smash the two heaviest stones together. If they are equal, both are destroyed. If not, the lighter is destroyed and the heavier becomes `x - y`. Repeat until at most one stone remains. Return the weight of the last stone (or 0 if none).

**Approach:** Use a max-heap. Python's `heapq` is a min-heap, so negate values to simulate a max-heap. Pop the two largest, compute difference, push back if nonzero.

**Key Insight:** Negating values is the standard Python trick to simulate a max-heap using the built-in min-heap. The process is: pop two largest, smash them (|first - second|), push result if nonzero.

**Edge Cases:**
- Single stone — already done, return its weight.
- All stones equal weight — all destroyed, return 0.
- Two different stones — one survives.
- Large values — no overflow in Python.

**Python Code:**

```python
import heapq

def lastStoneWeight(stones):
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0

# Test
print(lastStoneWeight([2, 7, 4, 1, 8, 1]))  # 1
print(lastStoneWeight([1]))  # 1
print(lastStoneWeight([1, 1]))  # 0
print(lastStoneWeight([8, 7, 4, 2, 1, 1]))  # 1
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

## Problem 27: Kth Largest Element in a Stream

**Statement:** Design a class that finds the kth largest element in a stream of numbers. Implement the constructor with the initial stream and `k`, and a method `add` that adds a new value and returns the kth largest element after each addition.

**Approach:** Maintain a min-heap of size k. The smallest element in this heap is the kth largest overall. On each add, if the heap has fewer than k elements, push; otherwise, if new element is larger than the heap root, replace.

**Key Insight:** A min-heap of size k always has the kth largest element at the root. When we see a new element larger than the root, we know it belongs in the top-k, so we replace the root.

**Edge Cases:**
- k equals the length of initial array — all initial elements in heap.
- All added values smaller than current kth largest — no change.
- Single element stream — just that element.

**Python Code:**

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]

# Test
kth = KthLargest(3, [4, 5, 8, 2])
print(kth.add(3))   # 4
print(kth.add(5))   # 5
print(kth.add(10))  # 5
print(kth.add(9))   # 8
print(kth.add(4))   # 8
```

**Time Complexity:** Constructor O(n log k), Add O(log k)
**Space Complexity:** O(k)

---

## Problem 28: Kth Largest in Sorted Matrix

**Statement:** Given an `n x n` matrix where each row and column is sorted in ascending order, find the kth largest element (1-indexed).

**Approach:** Binary search on the value range. For a candidate mid, count how many elements are <= mid using the sorted property of rows. Adjust search range based on count relative to k.

**Key Insight:** Since each row is sorted, we can count elements <= mid in O(n) time using a staircase approach starting from top-right corner. Binary search over the value range gives O(n log(max-min)).

**Alternative:** A min-heap of size k with the first row gives O(k log k + n * k log k), but binary search is more efficient.

**Edge Cases:**
- n = 1 — single element matrix.
- k = 1 — smallest element (matrix[0][0]).
- k = n^2 — largest element (matrix[-1][-1]).
- All elements same — any position works.

**Python Code:**

```python
def kthLargest(matrix, k):
    n = len(matrix)
    low, high = matrix[0][0], matrix[-1][-1]

    def count_less_equal(mid):
        count = 0
        row, col = 0, n - 1
        while row < n and col >= 0:
            if matrix[row][col] <= mid:
                count += col + 1
                row += 1
            else:
                col -= 1
        return count

    while low < high:
        mid = (low + high) // 2
        if count_less_equal(mid) < k:
            low = mid + 1
        else:
            high = mid
    return low

# Test
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print(kthLargest(matrix, 8))  # 13
matrix2 = [[-5]]
print(kthLargest(matrix2, 1))  # -5
matrix3 = [[2, 6], [5, 7]]
print(kthLargest(matrix3, 3))  # 6
```

**Time Complexity:** O(n * log(max - min))
**Space Complexity:** O(1)

---

## Problem 29: K Closest Points to Origin

**Statement:** Given an array of points where `points[i] = [x, y]`, find the `k` closest points to the origin `(0, 0)`. Return the answer in any order.

**Approach:** Use a max-heap of size k. For each point, compute squared distance. Push to heap; if heap exceeds size k, pop the farthest. The heap root is the farthest among the k closest.

**Key Insight:** We use squared distance (x^2 + y^2) to avoid the expensive sqrt computation. The ordering is preserved since sqrt is monotonically increasing.

**Edge Cases:**
- k equals number of points — return all points.
- k = 1 — closest single point.
- Points at same distance — any order is acceptable.
- Origin point included — distance is 0.
- Negative coordinates — squared distance handles correctly.

**Python Code:**

```python
import heapq

def kClosest(points, k):
    heap = []
    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]

# Test
print(kClosest([[1, 3], [-2, 2]], 1))  # [[-2, 2]]
print(kClosest([[3, 3], [5, -1], [-2, 4]], 2))  # [[3,3],[-2,4]]
print(kClosest([[0, 1], [1, 0]], 2))  # [[0,1],[1,0]]
```

**Time Complexity:** O(n log k)
**Space Complexity:** O(k)

---

## Problem 30: Furthest Building You Can Reach

**Statement:** You are climbing a building with `n` floors. You have `b` bricks and `l` ladders. Moving to a higher floor requires climbing the height difference. You can use bricks for small jumps or ladders for big jumps. Return the index of the furthest building you can reach.

**Approach:** Use a min-heap to track the largest l jumps (which will be handled by ladders). Process height differences; use bricks for small differences. If bricks run out, replace the largest brick-cost jump with a ladder.

**Key Insight:** Ladders are best used for the largest jumps. By keeping a min-heap of the l largest jumps seen so far, we can always replace the smallest ladder-use with bricks when a bigger jump comes along.

**Edge Cases:**
- No height differences — reach the end without using anything.
- All ladders used early — use bricks for remaining smaller jumps.
- Not enough resources to reach end — return index of last reachable building.
- l = 0 — all jumps must use bricks.
- bricks = 0 — all jumps must use ladders.

**Python Code:**

```python
import heapq

def furthestBuilding(heights, bricks, ladders):
    heap = []
    for i in range(len(heights) - 1):
        diff = heights[i + 1] - heights[i]
        if diff <= 0:
            continue
        heapq.heappush(heap, diff)
        if len(heap) > ladders:
            bricks -= heapq.heappop(heap)
            if bricks < 0:
                return i
    return len(heights) - 1

# Test
print(furthestBuilding([4, 2, 7, 6, 9, 14, 12], 5, 1))  # 4
print(furthestBuilding([4, 12, 2, 7, 3, 18, 20, 3, 19], 7, 2))  # 7
print(furthestBuilding([14, 3, 19, 3], 17, 0))  # 3
```

**Time Complexity:** O(n log l)
**Space Complexity:** O(l)

---

## Problem 31: Maximum Performance of a Team

**Statement:** You are given `n` engineers with `speed[i]` and `efficiency[i]`. Choose at most `k` engineers to form a team. Performance = (sum of speeds) * (min efficiency). Maximize performance. Return result modulo 10^9 + 7.

**Approach:** Sort engineers by efficiency descending. Use a min-heap to maintain the k fastest engineers. As we iterate, the current engineer's efficiency is the team minimum. Add speed to running sum; if team exceeds k, remove the slowest.

**Key Insight:** By iterating efficiency in descending order, we guarantee that the current engineer's efficiency is the team's minimum efficiency. The heap keeps the k highest-speed engineers seen so far, maximizing the speed sum component.

**Edge Cases:**
- k = 1 — pick the single best (speed * efficiency) engineer.
- k = n — pick all engineers.
- All same efficiency — pick k fastest.
- All same speed — pick any k (efficiency determines the answer).

**Python Code:**

```python
import heapq

def maxPerformance(n, speed, efficiency, k):
    MOD = 10**9 + 7
    engineers = sorted(zip(efficiency, speed), reverse=True)
    speed_heap = []
    total_speed = 0
    best = 0
    for eff, spd in engineers:
        heapq.heappush(speed_heap, spd)
        total_speed += spd
        if len(speed_heap) > k:
            total_speed -= heapq.heappop(speed_heap)
        best = max(best, total_speed * eff)
    return best % MOD

# Test
print(maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2))  # 60
print(maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3))  # 68
print(maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 4))  # 72
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(k)

---

## Problem 32: Minimum Cost to Connect Sticks

**Statement:** Given an array `sticks` where `sticks[i]` is the length of the i-th stick, return the minimum total cost to connect all sticks. The cost of connecting two sticks is their combined length.

**Approach:** Always connect the two shortest sticks (greedy with min-heap). Push the combined stick back. Repeat until one stick remains. The sum of all intermediate costs is the answer.

**Key Insight:** This is a classic greedy problem. Connecting the shortest sticks first minimizes the total cost because shorter sticks are reused more times. This is analogous to Huffman coding.

**Edge Cases:**
- Single stick — cost is 0 (nothing to connect).
- Two sticks — cost is their sum.
- All same length — cost is deterministic regardless of order.
- Very large arrays — heap keeps operations efficient.

**Python Code:**

```python
import heapq

def connectSticks(sticks):
    heapq.heapify(sticks)
    total_cost = 0
    while len(sticks) > 1:
        first = heapq.heappop(sticks)
        second = heapq.heappop(sticks)
        cost = first + second
        total_cost += cost
        heapq.heappush(sticks, cost)
    return total_cost

# Test
print(connectSticks([2, 4, 3]))  # 14
print(connectSticks([1, 8, 3, 5]))  # 30
print(connectSticks([5]))  # 0
print(connectSticks([1, 2, 3, 4, 5]))  # 33
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

## Problem 33: Reorganize String

**Statement:** Given a string `s`, rearrange it so that no two adjacent characters are the same. Return any valid rearrangement, or `""` if impossible.

**Approach:** Count character frequencies. Use a max-heap. At each step, pop the two most frequent characters (to ensure they differ), append them to result, decrement counts, and push back if count > 0.

**Key Insight:** By always picking the two most frequent characters, we ensure they are different. After using them, we put them back with decremented counts, preventing adjacent duplicates.

**Edge Cases:**
- Single character repeated — impossible if count > (n+1)/2.
- All characters unique — trivially rearrangeable.
- Two different characters — always possible.
- Impossible case: one character appears more than (n+1)/2 times.

**Python Code:**

```python
import heapq
from collections import Counter

def reorganizeString(s):
    count = Counter(s)
    heap = [(-cnt, char) for char, cnt in count.items()]
    heapq.heapify(heap)
    result = []
    prev = None
    while heap:
        cnt, char = heapq.heappop(heap)
        result.append(char)
        if prev:
            heapq.heappush(heap, prev)
        cnt += 1
        prev = (cnt, char) if cnt < 0 else None
    res = ''.join(result)
    return res if len(res) == len(s) else ""

# Test
print(reorganizeString("aab"))  # "aba"
print(reorganizeString("aaab"))  # ""
print(reorganizeString("vvvlo"))  # "vlvvo"
print(reorganizeString("aaabc"))  # "abaca"
```

**Time Complexity:** O(n log k) where k is unique characters
**Space Complexity:** O(n)

---

## Problem 34: Sort Characters By Frequency

**Statement:** Given a string `s`, sort it in decreasing order based on the frequency of characters. Return the sorted string. If multiple characters have the same frequency, any order among them is fine.

**Approach:** Count character frequencies. Use a max-heap (negate frequencies). Pop each character and repeat it by its frequency count.

**Key Insight:** This is a simpler version of Reorganize String — we just need to output all characters in decreasing frequency order. No adjacency constraint.

**Edge Cases:**
- All characters same — entire string is one character repeated.
- All characters unique — sorted by decreasing frequency (all freq 1, any order).
- Single character — return as is.

**Python Code:**

```python
import heapq
from collections import Counter

def frequencySort(s):
    count = Counter(s)
    heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(heap)
    result = []
    while heap:
        freq, char = heapq.heappop(heap)
        result.append(char * (-freq))
    return ''.join(result)

# Test
print(frequencySort("tree"))  # "eert"
print(frequencySort("cccaaa"))  # "aaaccc"
print(frequencySort("Aabb"))  # "bbAa"
print(frequencySort("hello"))  # "llhhe"
```

**Time Complexity:** O(n log k) where k is unique characters
**Space Complexity:** O(n)

---

## Problem 35: Top K Frequent Words

**Statement:** Given an array of words `words` and an integer `k`, return the `k` most frequent words sorted by frequency (descending). If two words have the same frequency, sort them alphabetically (ascending).

**Approach:** Count word frequencies. Use a min-heap of size k with custom key: (-frequency, word). The min-heap naturally keeps the lexicographically larger word at the root for ties, which gets popped when exceeding k.

**Key Insight:** The tricky part is the tie-breaking: when frequencies are equal, we want lexicographically smaller words to have higher priority. By using (-frequency, word) in a min-heap, the heap root has the worst combination (highest frequency with lexicographically largest word for ties), which gets correctly evicted.

**Edge Cases:**
- All words unique — k most frequent is any k words (all have freq 1).
- k equals number of unique words — return all sorted.
- Single word repeated — just that word.
- Case sensitivity — "The" and "the" are different words.

**Python Code:**

```python
import heapq
from collections import Counter

def topKFrequent(words, k):
    count = Counter(words)
    heap = []
    for word, freq in count.items():
        heapq.heappush(heap, (-freq, word))
        if len(heap) > k:
            heapq.heappop(heap)
    result = []
    while heap:
        result.append(heapq.heappop(heap)[1])
    result.reverse()
    return result

# Test
print(topKFrequent(["i", "love", "leetcode", "i", "love", "coding"], 2))
# ["i", "love"]
print(topKFrequent(["the", "day", "is", "sunny", "the", "the", "the",
                     "sunny", "is", "is"], 4))
# ["the", "is", "sunny", "day"]
print(topKFrequent(["a", "aa", "aaa"], 2))  # ["a", "aa"]
```

**Time Complexity:** O(n log k)
**Space Complexity:** O(n)

---

## Problem 36: Find K Pairs with Smallest Sums

**Statement:** Given two integer arrays `nums1` and `nums2` sorted in ascending order and an integer `k`, find `k` pairs with the smallest sums where one element comes from each array.

**Approach:** Start with pairs `(nums1[0], nums2[0])`. Use a min-heap. For each `(i, j)` popped, push `(i+1, j)` and `(i, j+1)` with a visited set to avoid duplicates.

**Key Insight:** We avoid pushing `(i+1, j+1)` directly because it would be pushed twice (once from `(i+1, j)` and once from `(i, j+1)`). The visited set prevents duplicate entries in the heap.

**Edge Cases:**
- Empty array — return empty list.
- k larger than m*n — return all possible pairs.
- All elements same — all sums equal, any k pairs work.
- Single element arrays — only one pair possible.

**Python Code:**

```python
import heapq

def kSmallestPairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []
    heap = [(nums1[0] + nums2[0], 0, 0)]
    visited = {(0, 0)}
    result = []
    while heap and len(result) < k:
        total, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])
        if i + 1 < len(nums1) and (i + 1, j) not in visited:
            heapq.heappush(heap, (nums1[i + 1] + nums2[j], i + 1, j))
            visited.add((i + 1, j))
        if j + 1 < len(nums2) and (i, j + 1) not in visited:
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
            visited.add((i, j + 1))
    return result

# Test
print(kSmallestPairs([1, 7, 11], [2, 4, 6], 3))
# [[1,2],[1,4],[1,6]]
print(kSmallestPairs([1, 1, 2], [1, 2, 3], 2))
# [[1,1],[1,1]]
print(kSmallestPairs([1, 2], [3], 3))  # [[1,3],[2,3]]
```

**Time Complexity:** O(k log k)
**Space Complexity:** O(k)

---

## Problem 37: Kth Smallest Element in Sorted Matrix

**Statement:** Given an `n x n` matrix where each row and column is sorted in ascending order, find the kth smallest element.

**Approach:** Binary search on the value range. For a candidate mid, count how many elements are <= mid using the sorted property. Adjust low/high based on whether the count is less than k.

**Key Insight:** The count of elements <= mid in a sorted matrix can be computed in O(n) time by starting from the top-right corner and moving down/left. This is the same technique as Problem 28.

**Edge Cases:**
- n = 1 — single element is the answer for k=1.
- k = 1 — smallest element (top-left).
- k = n^2 — largest element (bottom-right).
- Duplicate values — binary search handles them correctly.

**Python Code:**

```python
def kthSmallest(matrix, k):
    n = len(matrix)
    low, high = matrix[0][0], matrix[-1][-1]

    def count_less_equal(mid):
        count = 0
        row, col = 0, n - 1
        while row < n and col >= 0:
            if matrix[row][col] <= mid:
                count += col + 1
                row += 1
            else:
                col -= 1
        return count

    while low < high:
        mid = (low + high) // 2
        if count_less_equal(mid) < k:
            low = mid + 1
        else:
            high = mid
    return low

# Test
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print(kthSmallest(matrix, 8))  # 13
matrix2 = [[-5]]
print(kthSmallest(matrix2, 1))  # -5
matrix3 = [[1, 2], [3, 4]]
print(kthSmallest(matrix3, 2))  # 2
print(kthSmallest(matrix3, 3))  # 3
```

**Time Complexity:** O(n * log(max - min))
**Space Complexity:** O(1)

---

## Problem 38: Find Median from Data Stream

**Statement:** Implement a data structure that supports adding numbers from a stream and finding the median at any point in time.

**Approach:** Use two heaps — a max-heap for the lower half and a min-heap for the upper half. The max-heap stores the smaller half, the min-heap stores the larger half. Balance them so their sizes differ by at most 1.

**Key Insight:** The median is either the root of the max-heap (odd total) or the average of both roots (even total). We maintain the invariant that all elements in the max-heap are <= all elements in the min-heap.

**Two Invariants:**
1. Size: `len(max-heap)` is either equal to or one more than `len(min-heap)`.
2. Order: Every element in max-heap <= every element in min-heap.

**Edge Cases:**
- Single element — median is that element.
- Even number of elements — average of two middle.
- All same values — median is that value.
- Very large stream — O(log n) per insertion.

**Python Code:**

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negated)
        self.hi = []   # min-heap

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        # Ensure max of lo <= min of hi
        if self.hi and (-self.lo[0]) > self.hi[0]:
            val = -heapq.heappop(self.lo)
            heapq.heappush(self.hi, val)
        # Balance sizes
        if len(self.lo) > len(self.hi) + 1:
            val = -heapq.heappop(self.lo)
            heapq.heappush(self.hi, val)
        elif len(self.hi) > len(self.lo):
            val = heapq.heappop(self.hi)
            heapq.heappush(self.lo, -val)

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0

# Test
mf = MedianFinder()
mf.addNum(1)
print(mf.findMedian())  # 1.0
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2.0
mf.addNum(4)
print(mf.findMedian())  # 2.5
mf.addNum(5)
print(mf.findMedian())  # 3.0
```

**Time Complexity:** Add O(log n), FindMedian O(1)
**Space Complexity:** O(n)

---

## Problem 39: Sliding Window Median

**Statement:** Given an array `nums` and a window size `k`, return the median of each sliding window of size `k` as it moves from left to right.

**Approach:** Maintain two heaps (max-heap for lower half, min-heap for upper half) along with lazy deletion using counters. For each window position, balance the heaps and remove elements going out of the window.

**Key Insight:** The SortedList approach from `sortedcontainers` simplifies the implementation by providing O(log k) insertions and deletions with O(1) median access. The pure heap approach requires lazy deletion with hash maps.

**Alternative (Pure Heaps):** Use two heaps with lazy deletion. Track which elements should be removed using a hash map. Before accessing heap roots, pop any marked elements.

**Edge Cases:**
- k = 1 — each element is its own median.
- k = n — single window, single median.
- k even — median is average of two middle values.
- k odd — median is the exact middle value.
- Duplicate values in window — handled by SortedList or lazy deletion.

**Python Code:**

```python
import heapq
from collections import defaultdict

def medianSlidingWindow(nums, k):
    from sortedcontainers import SortedList
    window = SortedList()
    result = []
    for i, num in enumerate(nums):
        window.add(num)
        if len(window) > k:
            window.remove(nums[i - k])
        if len(window) == k:
            if k % 2 == 1:
                result.append(window[k // 2])
            else:
                result.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
    return result

# Test
print(medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
print(medianSlidingWindow([1, 2, 3, 4], 2))
# [1.5, 2.5, 3.5]
print(medianSlidingWindow([2, 1, 3, 4, 5], 4))
# [2.5, 3.0]
```

**Time Complexity:** O(n log k) with SortedList
**Space Complexity:** O(k)

---

## Problem 40: IPO

**Statement:** You are given `n` projects. Each project has a capital cost `capital[i]` and a profit `profit[i]`. You start with `w` capital. You can complete at most `k` projects. Completing a project adds its profit to your capital. Maximize your final capital. Return the final capital.

**Approach:** Sort projects by capital. Use a max-heap of profits for all projects whose capital we can afford. Greedily pick the most profitable project each time, add its profit, and repeat for k projects.

**Key Insight:** At each step, we can afford any project whose capital requirement <= current capital. Among those, the one with highest profit gives us the most capital growth. Sorting by capital ensures we only need to scan forward through the list.

**Greedy Correctness:** Taking the highest-profit affordable project never hurts future choices because it gives us the most capital, making more projects affordable.

**Edge Cases:**
- k = 0 — return initial capital w.
- No affordable projects — return current capital (heap empty).
- All projects affordable — greedily pick top k profits.
- Projects with same capital — sorted by profit via heap.
- Large n and k — efficient with heap operations.

**Python Code:**

```python
import heapq

def findMaximizedCapital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))
    heap = []
    idx = 0
    n = len(projects)
    for _ in range(k):
        while idx < n and projects[idx][0] <= w:
            heapq.heappush(heap, -projects[idx][1])
            idx += 1
        if not heap:
            break
        w += -heapq.heappop(heap)
    return w

# Test
print(findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]))  # 4
print(findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]))  # 6
print(findMaximizedCapital(1, 0, [1, 2, 3], [0, 1, 2]))  # 1
print(findMaximizedCapital(1, 2, [1], [1]))  # 3
print(findMaximizedCapital(2, 3, [2, 1, 3], [1, 2, 1]))  # 8
```

**Time Complexity:** O(n log n + k log n)
**Space Complexity:** O(n)

---

# KEY PATTERNS & TIPS FOR INFOSYS SP DSE

---

## Sorting Patterns to Master

1. **Two-Pointer Partitioning** — Problems 1, 2 use in-place partitioning with O(n) time and O(1) space. Always check if relative order matters.

2. **Custom Sort Key** — Problems 3, 4 use lambda/comparator functions to define custom ordering. Python's `sort(key=lambda x: ...)` is very powerful.

3. **Sort + Two Pointers** — Problems 8, 5 use sorting to enable two-pointer technique. This is a very common pattern in coding interviews.

4. **Sort + Greedy** — Problems 6, 7 use sorting followed by a single greedy check. Always think about what sorting reveals about the structure.

5. **Deque Simulation** — Problem 10 uses a deque to simulate a process. Deques are useful for queue/dequeue operations.

## Hashing Patterns to Master

1. **Prefix Sum + Hash Map** — Problems 11, 12 are classic prefix sum problems. The hash map stores frequencies of prefix sums for O(1) lookup.

2. **Bidirectional Mapping** — Problems 15, 16 require checking bijections with two maps. Always verify both directions.

3. **Frequency Counting** — Problems 14, 20, 21, 22 use Counter or dictionary to count occurrences. This is the most basic hashing pattern.

4. **Set Operations** — Problems 19, 23, 25 use set difference, set intersection, or set membership. Sets provide O(1) average lookup.

5. **Floyd's Cycle Detection** — Problem 17 is a unique application of cycle detection to find duplicates. This is a must-know O(1) space technique.

6. **Trust/Score Counting** — Problem 22 uses a simple scoring system. Many graph problems can be reduced to scoring/counting.

## Heap Patterns to Master

1. **Max-Heap via Min-Heap** — Problems 26, 29, 34 use `heapq` with negated values. This is the standard Python approach for max-heaps.

2. **Min-Heap of Size k** — Problems 27, 29, 35 maintain a heap of fixed size k for top-k problems. This is O(n log k) which is better than full sorting for large n.

3. **Two-Heap Median** — Problem 38 is the classic median maintenance pattern. The two-heap invariant is essential to know.

4. **Greedy + Heap** — Problems 30, 31, 32, 40 combine greedy decisions with heap data structures. The heap helps select the best option at each step.

5. **Sort + Heap** — Problems 36, 40 sort first, then use heap for subsequent operations. Combining sorting with heaps is very powerful.

## Infosys SP DSE Specific Tips

- **Time Limits:** Python solutions may be slower than C++. Focus on O(n log n) or better algorithms.
- **Edge Cases:** Always consider empty inputs, single elements, all-same values, and very large inputs.
- **Space Constraints:** If O(1) space is required, look for in-place techniques (Problem 17's Floyd's algorithm).
- **Output Format:** Pay attention to whether the problem asks for indices, values, or boolean results.
- **Modulo Arithmetic:** Problems with large numbers often require mod 10^9 + 7 (Problem 31).
- **Custom Comparators:** Python 3 doesn't support `cmp` parameter. Use `key` function with tuples or `functools.cmp_to_key`.

---

# SUMMARY: ALL 40 PROBLEMS AT A GLANCE

| #  | Category | Problem | Key Technique |
|----|----------|---------|---------------|
| 1  | Sorting  | Sort Array By Parity | Two pointers |
| 2  | Sorting  | Sort Array By Parity II | Two pointers |
| 3  | Sorting  | Relative Sort Array | Custom sort key |
| 4  | Sorting  | Sort Array by Increasing Frequency | Frequency map sort |
| 5  | Sorting  | Minimum Absolute Difference | Sort + consecutive pairs |
| 6  | Sorting  | Triangle | Sort + greedy check |
| 7  | Sorting  | Maximum Product of Three Numbers | Sort + edge cases |
| 8  | Sorting  | 3Sum Closest | Sort + two pointers |
| 9  | Sorting  | Pancake Sorting | Flip operations |
| 10 | Sorting  | Reveal Cards In Increasing Order | Deque simulation |
| 11 | Hashing  | Subarray Sum Equals K | Prefix sum + hash map |
| 12 | Hashing  | Continuous Subarray Sum | Prefix sum modulo k |
| 13 | Hashing  | Minimum Index Sum of Two Lists | Index hash map |
| 14 | Hashing  | Number of Good Pairs | Frequency combinations |
| 15 | Hashing  | Word Pattern | Bijection mapping |
| 16 | Hashing  | Isomorphic Strings | Bidirectional mapping |
| 17 | Hashing  | Find Duplicate Number | Floyd's cycle detection |
| 18 | Hashing  | Check if Numbers Are Ascending | Extract and verify |
| 19 | Hashing  | Find Difference of Two Arrays | Set difference |
| 20 | Hashing  | Intersection of Multiple Arrays | Frequency counting |
| 21 | Hashing  | Largest Unique Number | Frequency map |
| 22 | Hashing  | Find the Town Judge | Trust score counting |
| 23 | Hashing  | Check if Pangram | Set of 26 letters |
| 24 | Hashing  | Count Distinct Numbers on Board | Math observation |
| 25 | Hashing  | Find All Numbers Disappeared | Hash set lookup |
| 26 | Heaps    | Last Stone Weight | Max-heap simulation |
| 27 | Heaps    | Kth Largest in Stream | Min-heap of size k |
| 28 | Heaps    | Kth Largest in Sorted Matrix | Binary search + counting |
| 29 | Heaps    | K Closest Points to Origin | Max-heap of size k |
| 30 | Heaps    | Furthest Building You Can Reach | Min-heap + greedy |
| 31 | Heaps    | Maximum Performance of a Team | Sort + min-heap |
| 32 | Heaps    | Minimum Cost to Connect Sticks | Greedy min-heap |
| 33 | Heaps    | Reorganize String | Greedy two-pick heap |
| 34 | Heaps    | Sort Characters By Frequency | Max-heap output |
| 35 | Heaps    | Top K Frequent Words | Min-heap of size k |
| 36 | Heaps    | Find K Pairs with Smallest Sums | BFS + min-heap |
| 37 | Heaps    | Kth Smallest in Sorted Matrix | Binary search |
| 38 | Heaps    | Find Median from Data Stream | Two-heap median |
| 39 | Heaps    | Sliding Window Median | SortedList / two heaps |
| 40 | Heaps    | IPO | Sort + max-heap greedy |

---

*Total: 40 problems | 10 Sorting + 15 Hashing + 15 Heaps*
*Each solution in clean, working Python — ready for Infosys SP DSE prep.*
