# Next Permutation

**Problem**: Find the next lexicographically greater permutation of a sequence. If no greater permutation exists, return the smallest permutation (sorted ascending).

**Example**:
- `[1, 2, 3]` → `[1, 3, 2]`
- `[3, 2, 1]` → `[1, 2, 3]` (wrap around)
- `[1, 1, 5]` → `[1, 5, 1]`

---

## The Algorithm (O(n))

Next permutation in lexicographical order can be found in O(n) time with this 3-step process:

```
1. Find first decreasing element from right
2. Find next larger element to swap
3. Reverse the suffix
```

```java
public void nextPermutation(int[] nums) {
    int n = nums.length;
    if (n <= 1) return;

    // Step 1: Find first decreasing element from right
    // nums[i] < nums[i+1] → this is where we can make a bigger change
    int i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) {
        i--;
    }

    // Step 2: If such element exists, find next larger element to swap
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) {
            j--;
        }
        swap(nums, i, j);
    }

    // Step 3: Reverse the suffix (from i+1 to end)
    reverse(nums, i + 1, n - 1);
}

private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
}

private void reverse(int[] nums, int start, int end) {
    while (start < end) {
        swap(nums, start, end);
        start++;
        end--;
    }
}
```

---

## Visual Walkthrough

### Example: [1, 3, 5, 4, 2]

```
Step 1: Find first decreasing from right
  [1, 3, 5, 4, 2]
          ↑
    nums[2]=5, nums[3]=4 → 5 > 4, continue
  [1, 3, 5, 4, 2]
       ↑
    nums[1]=3, nums[2]=5 → 3 < 5 → i=1 ✓

Step 2: Find next larger than nums[1]=3 from right
  [1, 3, 5, 4, 2]
              ↑
    nums[4]=2 ≤ 3, continue
  [1, 3, 5, 4, 2]
           ↑
    nums[3]=4 > 3 → j=3 ✓, swap(1,3)

  After swap: [1, 4, 5, 3, 2]

Step 3: Reverse suffix from i+1=2 to end
  [1, 4, | 5, 3, 2] → reverse → [1, 4, | 2, 3, 5]
                    ↑                  ↑
                 suffix            reversed

Result: [1, 4, 2, 3, 5]
```

### Example: [3, 2, 1] (last permutation)

```
Step 1: Find first decreasing from right
  [3, 2, 1]
       ↑ nums[1]=2 > nums[2]=1, continue
  [3, 2, 1]
    ↑ nums[0]=3 > nums[1]=2, continue
  i = -1 (no decreasing element found)

Step 2: Skipped (i < 0)

Step 3: Reverse entire array
  reverse(0, 2): [3, 2, 1] → [1, 2, 3]

Result: [1, 2, 3] (wraps around to smallest)
```

---

## Why This Algorithm Works

### Understanding Lexicographic Order

Think of permutations as numbers. `[1, 3, 5, 4, 2]` is like the number 13542.

To find the next bigger number:
1. Find the rightmost position where we can increase the digit
2. Increase it by the smallest possible amount
3. Make the remaining digits as small as possible

### Step 1: Find the "Pivot"

We scan from right to left looking for `nums[i] < nums[i+1]`. This is the rightmost position where the sequence decreases. Everything after `i` is in descending order.

Why descending? Because if the suffix were ascending, there would be a bigger permutation possible with a later position — we'd need to look further right.

### Step 2: Find the "Successor"

From the right side, find the first element greater than `nums[i]`. Since the suffix is descending, this will be the smallest element in the suffix that's greater than `nums[i]`.

After swapping, the suffix remains in descending order (we swapped a smaller value into the suffix).

### Step 3: Reverse to Get Ascending

The suffix is now in descending order. To get the smallest possible arrangement of these elements, we reverse to make it ascending.

---

## Previous Permutation

The reverse operation: find the previous lexicographically smaller permutation.

```java
public void previousPermutation(int[] nums) {
    int n = nums.length;
    if (n <= 1) return;

    // Step 1: Find first increasing element from right
    int i = n - 2;
    while (i >= 0 && nums[i] <= nums[i + 1]) {
        i--;
    }

    // Step 2: If such element exists, find next smaller element from right
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] >= nums[i]) {
            j--;
        }
        swap(nums, i, j);
    }

    // Step 3: Reverse suffix
    reverse(nums, i + 1, n - 1);
}
```

**Differences from nextPermutation**:
- Find `nums[i] > nums[i+1]` (increasing) instead of `nums[i] < nums[i+1]`
- Find first element smaller than nums[i] instead of larger

---

## Generating All Permutations

Use `nextPermutation` repeatedly to generate all permutations in order:

```java
public List<List<Integer>> generateAllPermutations(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(nums);

    do {
        List<Integer> perm = new ArrayList<>();
        for (int num : nums) perm.add(num);
        result.add(perm);
    } while (nextPermutation(nums));

    return result;
}

// Modified to return boolean
public boolean nextPermutation(int[] nums) {
    int n = nums.length;
    int i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i < 0) {
        reverse(nums, 0, n - 1);
        return false; // no more permutations
    }
    int j = n - 1;
    while (nums[j] <= nums[i]) j--;
    swap(nums, i, j);
    reverse(nums, i + 1, n - 1);
    return true;
}
```

---

## Applications and Extensions

### Kth Permutation

Find the kth permutation in lexicographic order without generating all:

```java
public String getPermutation(int n, int k) {
    List<Integer> numbers = new ArrayList<>();
    int[] factorial = new int[n + 1];
    factorial[0] = 1;

    for (int i = 1; i <= n; i++) {
        numbers.add(i);
        factorial[i] = factorial[i - 1] * i;
    }

    k--; // convert to 0-indexed
    StringBuilder sb = new StringBuilder();

    for (int i = n; i >= 1; i--) {
        int index = k / factorial[i - 1];
        sb.append(numbers.get(index));
        numbers.remove(index);
        k %= factorial[i - 1];
    }

    return sb.toString();
}
```

### Next Greater Element III

Same as next permutation but for a number:

```java
public int nextGreaterElement(int n) {
    char[] digits = String.valueOf(n).toCharArray();
    int i = digits.length - 2;

    while (i >= 0 && digits[i] >= digits[i + 1]) i--;
    if (i < 0) return -1;

    int j = digits.length - 1;
    while (digits[j] <= digits[i]) j--;

    swap(digits, i, j);
    reverse(digits, i + 1, digits.length - 1);

    long result = Long.parseLong(new String(digits));
    return result > Integer.MAX_VALUE ? -1 : (int) result;
}
```

---

## Complexity

- **Time**: O(n) for next/previous permutation
- **Space**: O(1) (in-place modification)

## Key Interview Points

1. This is a **mathematical/combinatorial** algorithm, not a backtracking one
2. It's O(n) — very efficient compared to O(n * n!) for generating all
3. Often used as a subroutine to generate all permutations in order
4. The algorithm works with **duplicates** without modification
5. Key insight: finding the rightmost position where we can make a change

## Common Mistakes

| Mistake | Explanation |
|---|---|
| Using `>` instead of `>=` in step 1 | Using `>` would miss the correct pivot when there are equal elements |
| Not handling the wrap-around case | When i < 0, the array is the last permutation — need to reverse entirely |
| Swapping with wrong element in step 2 | Must find the RIGHTMOST element greater than nums[i] |
| Forgetting to reverse | The suffix after the pivot must be in ascending order for it to be the "next" arrangement |
