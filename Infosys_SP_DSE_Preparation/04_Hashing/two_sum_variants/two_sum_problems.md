# Two Sum Problems

## 1. Two Sum (LeetCode 1)

```python
def two_sum(nums, target):
    """
    Find two numbers that add up to target
    Return their indices
    Time: O(n), Space: O(n)
    """
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
print(two_sum([3, 3], 6))           # [0, 1]
```

## 2. Two Sum II - Sorted Array (LeetCode 167)

```python
def two_sum_ii(numbers, target):
    """
    Find two numbers in sorted array that add up to target
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []

# Test
print(two_sum_ii([2, 7, 11, 15], 9))  # [1, 2]
print(two_sum_ii([2, 3, 4], 6))        # [1, 3]
```

## 3. Three Sum (LeetCode 15)

```python
def three_sum(nums):
    """
    Find all unique triplets that sum to zero
    Time: O(n^2), Space: O(n)
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two pointers
        left, right = i + 1, n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result

# Test
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0]))               # [[0, 0, 0]]
```

## 4. Four Sum (LeetCode 18)

```python
def four_sum(nums, target):
    """
    Find all unique quadruplets that sum to target
    Time: O(n^3), Space: O(n)
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 3):
        # Skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        for j in range(i + 1, n - 2):
            # Skip duplicates
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            
            left, right = j + 1, n - 1
            
            while left < right:
                total = nums[i] + nums[j] + nums[left] + nums[right]
                
                if total == target:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
    
    return result

# Test
print(four_sum([1, 0, -1, 0, -2, 2], 0))
# [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
```

## 5. Two Sum III - Data Structure Design (LeetCode 170)

```python
class TwoSum:
    """
    Design a data structure that supports:
    - add(value): Add value to internal data structure
    - find(value): Return true if any two numbers sum to value
    """
    
    def __init__(self):
        self.num_count = {}
    
    def add(self, value):
        self.num_count[value] = self.num_count.get(value, 0) + 1
    
    def find(self, value):
        for num in self.num_count:
            complement = value - num
            
            if complement in self.num_count:
                # Check if same element is used twice
                if complement != num or self.num_count[num] > 1:
                    return True
        
        return False

# Test
ts = TwoSum()
ts.add(1)
ts.add(3)
ts.add(5)
print(ts.find(4))   # True (1 + 3)
print(ts.find(7))   # True (2 + 5)
print(ts.find(10))  # False
```

## 6. Two Sum IV - BST (LeetCode 653)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_target(root, k):
    """
    Find if two nodes in BST sum to k
    Time: O(n), Space: O(n)
    """
    seen = set()
    
    def dfs(node):
        if not node:
            return False
        
        if (k - node.val) in seen:
            return True
        
        seen.add(node.val)
        
        return dfs(node.left) or dfs(node.right)
    
    return dfs(root)

# Build BST
#       5
#      / \
#     3   6
#    / \   \
#   2   4   7
root = TreeNode(5)
root.left = TreeNode(3)
root.right = TreeNode(6)
root.left.left = TreeNode(2)
root.left.right = TreeNode(4)
root.right.right = TreeNode(7)

print(find_target(root, 9))   # True (2 + 7 or 4 + 5)
print(find_target(root, 28))  # False
```

## 7. Subarray Sum Equals K (LeetCode 560)

```python
def subarray_sum(nums, k):
    """
    Count subarrays with sum equal to k
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
print(subarray_sum([1, 1, 1], 2))          # 2
print(subarray_sum([1, 2, 3], 3))          # 2
print(subarray_sum([1, -1, 0], 0))         # 3
```

## 8. Continuous Subarray Sum (LeetCode 523)

```python
def check_subarray_sum(nums, k):
    """
    Check if there's a continuous subarray with sum divisible by k
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

def find_subarray_divisible_by_k(nums, k):
    """Find the subarray itself"""
    seen = {0: -1}
    prefix_sum = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in seen:
            if i - seen[remainder] >= 2:
                return nums[seen[remainder] + 1:i + 1]
        else:
            seen[remainder] = i
    
    return []

# Test
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 13)) # False
print(find_subarray_divisible_by_k([23, 2, 4, 6, 7], 6))  # [2, 4]
```

## 9. Count of Subarrays with Sum K

```python
def count_subarrays_with_sum_k(nums, k):
    """
    Count subarrays with sum exactly k
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

def subarrays_with_sum_k(nums, k):
    """Find all subarrays with sum k"""
    result = []
    prefix_sum = 0
    seen = {0: [-1]}
    
    for i, num in enumerate(nums):
        prefix_sum += num
        
        if prefix_sum - k in seen:
            for start in seen[prefix_sum - k]:
                result.append(nums[start + 1:i + 1])
        
        if prefix_sum not in seen:
            seen[prefix_sum] = []
        seen[prefix_sum].append(i)
    
    return result

# Test
print(count_subarrays_with_sum_k([1, 1, 1], 2))  # 2
print(subarrays_with_sum_k([1, 2, 3, 4, 5], 5))  # [[2, 3], [5]]
```

## 10. Minimum Size Subarray Sum (LeetCode 209)

```python
def min_subarray_len(target, nums):
    """
    Find minimal length of subarray with sum >= target
    Time: O(n), Space: O(1)
    """
    left = 0
    total = 0
    min_len = float('inf')
    
    for right in range(len(nums)):
        total += nums[right]
        
        while total >= target:
            min_len = min(min_len, right - left + 1)
            total -= nums[left]
            left += 1
    
    return min_len if min_len != float('inf') else 0

def min_subarray_len_binary_search(target, nums):
    """
    Binary search approach for sorted prefix sums
    Time: O(n log n), Space: O(n)
    """
    n = len(nums)
    prefix_sum = [0] * (n + 1)
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + nums[i]
    
    min_len = float('inf')
    
    for i in range(n):
        # Find smallest j such that prefix_sum[j] - prefix_sum[i] >= target
        target_sum = prefix_sum[i] + target
        
        # Binary search
        left, right = i + 1, n
        while left <= right:
            mid = (left + right) // 2
            if prefix_sum[mid] >= target_sum:
                min_len = min(min_len, mid - i)
                right = mid - 1
            else:
                left = mid + 1
    
    return min_len if min_len != float('inf') else 0

# Test
print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]))  # 2
print(min_subarray_len_binary_search(11, [1, 2, 3, 4, 5]))  # 3
```

## 11. Additional Two Sum Variants

```python
from collections import defaultdict

# Problem: Two Sum Less Than K (LeetCode 1099)
def two_sum_less_than_k(nums, k):
    """Find max sum of two elements less than k"""
    nums.sort()
    left, right = 0, len(nums) - 1
    max_sum = -1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum < k:
            max_sum = max(max_sum, current_sum)
            left += 1
        else:
            right -= 1
    
    return max_sum

# Problem: Max Number of K-Sum Pairs (LeetCode 1679)
def max_operations(nums, k):
    """Find max number of operations to make sum k"""
    count = Counter(nums)
    operations = 0
    
    for num in list(count.keys()):
        complement = k - num
        
        if complement in count:
            if num == complement:
                operations += count[num] // 2
                count[num] = 0
            else:
                pairs = min(count[num], count[complement])
                operations += pairs
                count[num] = 0
                count[complement] = 0
    
    return operations

# Problem: Subarray Product Less Than K (LeetCode 713)
def num_subarray_product_less_than_k(nums, k):
    """Count subarrays with product less than k"""
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
print(two_sum_less_than_k([34, 23, 1, 24, 75, 33, 54, 8], 60))  # 58
print(max_operations([1, 2, 3, 4], 5))  # 2
print(num_subarray_product_less_than_k([10, 5, 2, 6], 100))  # 8
```
