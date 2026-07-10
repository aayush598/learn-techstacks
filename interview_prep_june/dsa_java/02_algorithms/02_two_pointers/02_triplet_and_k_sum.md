# Triplets, K-Sum, and Generalizations

If you've mastered pair sum, you're ready to level up. Triplets and K-Sum problems are just **nested two-pointers** — we fix one or more elements, then use two pointers on the rest.

## 3Sum

### Problem Statement
Given an array, find all unique triplets that sum to zero.

### The Approach

1. **Sort** the array (required for two pointers)
2. **Fix** one element at index `i`
3. Use **two pointers** on `i+1..n-1` to find pairs that sum to `-arr[i]`
4. **Skip duplicates** to avoid duplicate triplets

```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    int n = nums.length;

    for (int i = 0; i < n - 2; i++) {
        // Skip duplicate values for the fixed element
        if (i > 0 && nums[i] == nums[i - 1]) continue;

        int left = i + 1;
        int right = n - 1;
        int target = -nums[i];

        while (left < right) {
            int sum = nums[left] + nums[right];

            if (sum == target) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));

                // Skip duplicates for left and right
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;

                left++;
                right--;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
    }

    return result;
}
```

### Complexity
- **Time**: O(n²) — sorting is O(n log n), the nested loop is O(n²)
- **Space**: O(1) not counting the output, or O(n) for sorting

### Dry Run

```
Array: [-1, 0, 1, 2, -1, -4]
Sorted: [-4, -1, -1, 0, 1, 2]

i=0, nums[i]=-4, target=4
  left=1(-1), right=5(2) → sum=-1+2=1 < 4 → left++
  left=2(-1), right=5(2) → sum=1 < 4 → left++
  left=3(0),  right=5(2) → sum=2 < 4 → left++
  left=4(1),  right=5(2) → sum=3 < 4 → left++
  left=5, left<right false → break

i=1, nums[i]=-1, target=1
  left=2(-1), right=5(2) → sum=1 == 1 → add [-1,-1,2]
  skip duplicates, left=3, right=4
  left=3(0), right=4(1) → sum=1 == 1 → add [-1,0,1]
  ...

Result: [[-1,-1,2], [-1,0,1]]
```

## 3Sum Closest

Find the triplet whose sum is closest to a given target.

```java
public int threeSumClosest(int[] nums, int target) {
    Arrays.sort(nums);
    int n = nums.length;
    int closest = nums[0] + nums[1] + nums[2];

    for (int i = 0; i < n - 2; i++) {
        int left = i + 1;
        int right = n - 1;

        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];

            if (sum == target) return target; // Perfect match

            if (Math.abs(sum - target) < Math.abs(closest - target)) {
                closest = sum;
            }

            if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
    }

    return closest;
}
```

### Pruning Optimization

```java
// After sorting, you can add this optimization inside the outer loop:
// Minimum possible sum with current i
int minSum = nums[i] + nums[i + 1] + nums[i + 2];
if (minSum > target) {
    // Even the smallest possible sum is too big
    if (Math.abs(minSum - target) < Math.abs(closest - target)) {
        closest = minSum;
    }
    break;
}

// Maximum possible sum with current i
int maxSum = nums[i] + nums[n - 2] + nums[n - 1];
if (maxSum < target) {
    if (Math.abs(maxSum - target) < Math.abs(closest - target)) {
        closest = maxSum;
    }
    continue;
}
```

## 3Sum Smaller

Count the number of triplets with sum less than a given target.

```java
public int threeSumSmaller(int[] nums, int target) {
    Arrays.sort(nums);
    int count = 0;
    int n = nums.length;

    for (int i = 0; i < n - 2; i++) {
        int left = i + 1;
        int right = n - 1;

        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];

            if (sum < target) {
                // All pairs between left and right work
                count += right - left;
                left++;
            } else {
                right--;
            }
        }
    }

    return count;
}
```

The `count += right - left` trick again! When `sum < target` holds for `(i, left, right)`, it also holds for `(i, left, right-1)`, `(i, left, right-2)`, etc. because the array is sorted.

## 4Sum

Same idea as 3Sum but with an extra nested loop.

```java
public List<List<Integer>> fourSum(int[] nums, int target) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    int n = nums.length;

    for (int i = 0; i < n - 3; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;

        for (int j = i + 1; j < n - 2; j++) {
            if (j > i + 1 && nums[j] == nums[j - 1]) continue;

            int left = j + 1;
            int right = n - 1;

            while (left < right) {
                long sum = (long) nums[i] + nums[j] + nums[left] + nums[right];

                if (sum == target) {
                    result.add(Arrays.asList(nums[i], nums[j], nums[left], nums[right]));

                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;

                    left++;
                    right--;
                } else if (sum < target) {
                    left++;
                } else {
                    right--;
                }
            }
        }
    }

    return result;
}
```

**Watch out for overflow!** If `nums[i] + nums[j] + nums[left] + nums[right]` can overflow int, use `long`.

## General KSum

Here's the beautiful recursive generalization. You can solve 2Sum, 3Sum, 4Sum, ... KSum with the same function.

```java
public List<List<Integer>> kSum(int[] nums, int target, int start, int k) {
    List<List<Integer>> result = new ArrayList<>();

    // Base case: 2Sum using two pointers
    if (k == 2) {
        int left = start, right = nums.length - 1;
        while (left < right) {
            int sum = nums[left] + nums[right];
            if (sum == target) {
                result.add(new ArrayList<>(Arrays.asList(nums[left], nums[right])));
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
        return result;
    }

    // Recursive case: fix one element, recurse for (k-1)Sum
    for (int i = start; i < nums.length - k + 1; i++) {
        if (i > start && nums[i] == nums[i - 1]) continue;

        // Pruning: check if possible sums are within range
        int minSum = nums[i] + nums[i + 1] * (k - 1);
        if (minSum > target) break;

        int maxSum = nums[i] + nums[nums.length - 1] * (k - 1);
        if (maxSum < target) continue;

        List<List<Integer>> subResults = kSum(nums, target - nums[i], i + 1, k - 1);

        for (List<Integer> sub : subResults) {
            sub.add(0, nums[i]);
            result.add(sub);
        }
    }

    return result;
}

// Wrapper
public List<List<Integer>> fourSum(int[] nums, int target) {
    Arrays.sort(nums);
    return kSum(nums, target, 0, 4);
}
```

### How It Works

1. **Base case**: k=2 → use standard two-pointer pair sum
2. **Recursive step**: fix `nums[i]`, then solve `(k-1)Sum` with `target - nums[i]` starting from `i+1`
3. **Deduplication**: skip duplicate `nums[i]` values
4. **Pruning**: 
   - If the smallest possible sum > target, break (can't get smaller as i increases)
   - If the largest possible sum < target, continue to next i

### Complexity of KSum

- **Time**: O(n^(k-1)) — each level of recursion adds a nested loop
- **Space**: O(k) for the recursion stack

## Pattern Summary

| Problem | Type | Complexity |
|---------|------|------------|
| 2Sum (sorted) | Two pointers | O(n) |
| 3Sum | Fix one + two pointers | O(n²) |
| 3Sum Closest | Fix one + two pointers | O(n²) |
| 3Sum Smaller | Fix one + two pointers | O(n²) |
| 4Sum | Fix two + two pointers | O(n³) |
| KSum | Fix (k-2) + two pointers | O(n^(k-1)) |

## Interview Tips

1. **Always sort first** — 3Sum/4Sum/KSum all need sorting
2. **Duplicate handling is critical** — if you miss it, you'll have duplicate triplets
3. **Know the pruning tricks** — they show deep understanding
4. **For KSum, write the recursive version** — it's impressive and shows CS fundamentals
5. **Watch for overflow** with large targets and 4Sum

The pattern is simple: KSum is just K-2 nested loops around a two-pointer pair sum. Everything else is handling duplicates!
