# Monotonic Stack Patterns

## What is Monotonic Stack
A monotonic stack is a stack where elements are either in increasing or decreasing order. It's used to find the next greater or smaller element efficiently.

**Key Insight**: When you encounter an element that violates the monotonic property, you pop elements and process them.

## Next Greater Element (Right) - O(n)
```python
def next_greater_element_right(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result

# Example: [2, 1, 2, 4, 3] -> [4, 2, 4, -1, -1]
```

## Next Smaller Element (Right) - O(n)
```python
def next_smaller_element_right(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[i] < nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result

# Example: [2, 1, 2, 4, 3] -> [1, -1, -1, 3, -1]
```

## Next Greater Element (Left) - O(n)
```python
def next_greater_element_left(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            stack.pop()
        
        if stack:
            result[i] = nums[stack[-1]]
        
        stack.append(i)
    
    return result

# Example: [2, 1, 2, 4, 3] -> [-1, 2, -1, -1, 4]
```

## Next Smaller Element (Left) - O(n)
```python
def next_smaller_element_left(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            stack.pop()
        
        if stack:
            result[i] = nums[stack[-1]]
        
        stack.append(i)
    
    return result

# Example: [2, 1, 2, 4, 3] -> [-1, -1, 1, 2, 2]
```

## Daily Temperatures - O(n)
```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        stack.append(i)
    
    return result

# Example: [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]
```

## Stock Span Problem - O(n)
```python
def stock_span(prices):
    n = len(prices)
    result = [0] * n
    stack = []  # Stack of (price, span)
    
    for i in range(n):
        span = 1
        
        while stack and prices[i] >= stack[-1][0]:
            span += stack[-1][1]
            stack.pop()
        
        stack.append((prices[i], span))
        result[i] = span
    
    return result

# Example: [100,80,60,70,60,75,85] -> [1,1,1,2,1,4,6]
```

## Largest Rectangle in Histogram - O(n)
```python
def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    n = len(heights)
    
    for i in range(n + 1):
        current_height = heights[i] if i < n else 0
        
        while stack and current_height < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    return max_area

# Example: [2,1,5,6,2,3] -> 10
```

## Maximal Rectangle in Binary Matrix - O(m * n)
```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0
    
    for i in range(rows):
        # Update heights
        for j in range(cols):
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0
        
        # Calculate largest rectangle in histogram
        max_area = max(max_area, largest_rectangle_area(heights))
    
    return max_area

# Helper function
def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    n = len(heights)
    
    for i in range(n + 1):
        current_height = heights[i] if i < n else 0
        
        while stack and current_height < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    return max_area

# Example: [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]] -> 6
```

## Trapping Rain Water (Monotonic Stack Approach) - O(n)
```python
def trap_rain_water(height):
    if not height:
        return 0
    
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            
            if stack:
                width = i - stack[-1] - 1
                trapped_height = min(h, height[stack[-1]]) - height[bottom]
                water += width * trapped_height
        
        stack.append(i)
    
    return water

# Example: [0,1,0,2,1,0,1,3,2,1,2,1] -> 6
```

## Sum of Subarray Minimums - O(n)
```python
def sum_subarray_minimums(arr):
    MOD = 10**9 + 7
    n = len(arr)
    result = 0
    
    # Find next smaller on left and right
    left = [-1] * n
    right = [n] * n
    
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    # Calculate contribution of each element
    for i in range(n):
        left_count = i - left[i]
        right_count = right[i] - i
        contribution = arr[i] * left_count * right_count
        result = (result + contribution) % MOD
    
    return result

# Alternative: Using monotonic stack directly
def sum_subarray_minimums_v2(arr):
    MOD = 10**9 + 7
    stack = []
    result = 0
    
    for i, num in enumerate(arr):
        while stack and arr[stack[-1]] > num:
            idx = stack.pop()
            left = stack[-1] if stack else -1
            result += arr[idx] * (idx - left) * (i - idx)
        
        stack.append(i)
    
    # Process remaining elements
    while stack:
        idx = stack.pop()
        left = stack[-1] if stack else -1
        result += arr[idx] * (idx - left) * (len(arr) - idx)
    
    return result % MOD

# Example: [3,1,2,4] -> 17
```

## Complete Example Usage
```python
# Next Greater Element
nums = [2, 1, 2, 4, 3]
print(f"Next Greater Right: {next_greater_element_right(nums)}")  # [4, 2, 4, -1, -1]
print(f"Next Greater Left: {next_greater_element_left(nums)}")   # [-1, 2, -1, -1, 4]

# Daily Temperatures
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(f"Daily Temperatures: {daily_temperatures(temps)}")  # [1, 1, 4, 2, 1, 1, 0, 0]

# Largest Rectangle in Histogram
heights = [2, 1, 5, 6, 2, 3]
print(f"Largest Rectangle: {largest_rectangle_area(heights)}")  # 10

# Trapping Rain Water
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(f"Trapped Water: {trap_rain_water(height)}")  # 6

# Sum of Subarray Minimums
arr = [3, 1, 2, 4]
print(f"Sum of Subarray Minimums: {sum_subarray_minimums(arr)}")  # 17
```

## Pattern Summary

| Pattern | When to Use | Stack Order |
|---------|-------------|-------------|
| Next Greater Right | Find next bigger element | Decreasing |
| Next Smaller Right | Find next smaller element | Increasing |
| Next Greater Left | Find previous bigger element | Decreasing |
| Next Smaller Left | Find previous smaller element | Increasing |
| Histogram | Find largest rectangle | Increasing |
| Rain Water | Calculate trapped water | Increasing |
