# Pair Sum Problems

Pair sum problems are the gateway to two pointers. Once you nail these, triplet problems become straightforward.

## Two Sum II - Sorted Array

This is THE classic two-pointer problem. Given a **sorted** array, find two numbers that add up to a target.

### Problem Statement
Given a 1-indexed sorted array and a target, return the indices of the two numbers that sum to target.

### The Intuition

Imagine you're at the first and last element. Their sum is either:
- **Too small** → move left forward to get a bigger number
- **Too large** → move right backward to get a smaller number
- **Just right** → done!

This works because the array is sorted. Moving left always increases the sum; moving right always decreases it.

### Code

```java
public int[] twoSum(int[] numbers, int target) {
    int left = 0;
    int right = numbers.length - 1;

    while (left < right) {
        int sum = numbers[left] + numbers[right];

        if (sum == target) {
            return new int[]{left + 1, right + 1}; // 1-indexed
        } else if (sum < target) {
            left++;  // Need a larger sum
        } else {
            right--; // Need a smaller sum
        }
    }

    return new int[]{-1, -1};
}
```

### Dry Run

```
Array: [2, 7, 11, 15], Target = 9

left=0, right=3 → sum=2+15=17 > 9 → right--
left=0, right=2 → sum=2+11=13 > 9 → right--
left=0, right=1 → sum=2+7=9  == 9 → return [1, 2]
```

Only 3 iterations instead of checking all 6 possible pairs. That's O(n) vs O(n²)!

## Pair Sum with Difference K

Find all pairs that have a difference of K.

### Approach 1: Two Pointers (Sorted)

```java
public List<int[]> findPairsWithDifference(int[] arr, int k) {
    Arrays.sort(arr);
    List<int[]> result = new ArrayList<>();
    int left = 0, right = 1;

    while (right < arr.length) {
        int diff = arr[right] - arr[left];

        if (diff == k) {
            result.add(new int[]{arr[left], arr[right]});
            left++;
            right++;
        } else if (diff < k) {
            right++;  // Need a bigger difference
        } else {
            left++;   // Need a smaller difference
        }

        // Prevent left from passing right
        if (left == right) right++;
    }

    return result;
}
```

### Approach 2: HashMap (Unsorted)

```java
public List<int[]> findPairsWithDifferenceMap(int[] arr, int k) {
    Set<Integer> set = new HashSet<>();
    List<int[]> result = new ArrayList<>();

    for (int num : arr) {
        // Check both num - k and num + k
        if (set.contains(num - k)) {
            result.add(new int[]{num - k, num});
        }
        if (set.contains(num + k)) {
            result.add(new int[]{num, num + k});
        }
        set.add(num);
    }

    return result;
}
```

The HashMap approach is O(n) time and O(n) space. The two-pointer approach is O(n log n) time (due to sorting) but O(1) space.

## Count Pairs with Given Sum

Count how many pairs sum to a target. Elements can be repeated.

### With HashMap

```java
public int countPairs(int[] arr, int target) {
    Map<Integer, Integer> freq = new HashMap<>();
    int count = 0;

    for (int num : arr) {
        int complement = target - num;
        if (freq.containsKey(complement)) {
            count += freq.get(complement);
        }
        freq.put(num, freq.getOrDefault(num, 0) + 1);
    }

    return count;
}
```

### Dry Run

```
Array: [1, 5, 7, -1, 5], Target = 6

num=1:  comp=5, freq={}  → count=0, freq={1:1}
num=5:  comp=1, freq={1:1} → count=1, freq={1:1, 5:1}
num=7:  comp=-1, freq={...} → count=1, freq={1:1, 5:1, 7:1}
num=-1: comp=7, freq={...} → count=2, freq={1:1, 5:1, 7:1, -1:1}
num=5:  comp=1, freq={1:1} → count=3, freq={1:1, 5:2, ...}

Result: 3 pairs: (1,5), (1,5), (-1,7)
```

Note that `5` appears twice, so `(1,5)` is counted twice. If you need unique pairs, use a Set-based approach.

## Unique Pairs with Given Sum

```java
public int countUniquePairs(int[] arr, int target) {
    Set<Integer> seen = new HashSet<>();
    Set<Integer> used = new HashSet<>();
    int count = 0;

    for (int num : arr) {
        int complement = target - num;
        if (seen.contains(complement) && !used.contains(num)) {
            count++;
            used.add(num);
            used.add(complement);
        }
        seen.add(num);
    }

    return count;
}
```

## Common Variations

### Pair Sum Less Than Target
```java
public int countPairsLessThanTarget(int[] arr, int target) {
    Arrays.sort(arr);
    int left = 0, right = arr.length - 1;
    int count = 0;

    while (left < right) {
        if (arr[left] + arr[right] < target) {
            // All pairs (left, left+1...right) are valid
            count += right - left;
            left++;
        } else {
            right--;
        }
    }

    return count;
}
```

This is a neat trick — when `arr[left] + arr[right] < target`, then *all* pairs between `left` and `right` (with `right` fixed) also satisfy the condition because the array is sorted. So we add `right - left` pairs in one shot.

### Pair Sum Greater Than Target
```java
public int countPairsGreaterThanTarget(int[] arr, int target) {
    Arrays.sort(arr);
    int left = 0, right = arr.length - 1;
    int count = 0;

    while (left < right) {
        if (arr[left] + arr[right] > target) {
            count += right - left;
            right--;
        } else {
            left++;
        }
    }

    return count;
}
```

## Interview Tips

1. **Clarify if the array is sorted** — if it's not, ask if you can sort it.
2. **Clarify if you need indices or values** — makes a difference!
3. **Clarify about duplicates** — should pairs be unique? Count each occurrence?
4. **Start with the HashMap approach** for unsorted, then offer two pointers as the optimization if sorted.
5. **Edge cases**: empty array, single element, no valid pairs, all elements same.

## Pattern Recognition

When you hear:
- **"Find two numbers that..."** → think HashMap or Two Pointers
- **"Sorted array"** → Two Pointers is almost always the intended solution
- **"Count number of pairs"** → Two Pointers with the `right - left` trick or HashMap

Remember: nested loops give you O(n²). Two pointers give you O(n). That's a massive difference when n = 10⁵.
