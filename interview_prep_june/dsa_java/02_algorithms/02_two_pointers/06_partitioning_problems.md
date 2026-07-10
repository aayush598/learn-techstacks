# Partitioning Problems

Partitioning is about rearranging elements into groups based on some property. Two pointers (often three!) are perfect for this.

## Dutch National Flag (Sort Colors)

### Problem Statement
Given an array with three values (0, 1, 2), sort them in-place without a sorting algorithm.

This is called the Dutch National Flag problem (named after the Dutch flag having three colors).

### The Three-Pointer Approach

```java
public void sortColors(int[] nums) {
    int low = 0;    // Boundary for 0s
    int mid = 0;    // Current element
    int high = nums.length - 1; // Boundary for 2s

    while (mid <= high) {
        switch (nums[mid]) {
            case 0:
                swap(nums, low, mid);
                low++;
                mid++;
                break;
            case 1:
                mid++;
                break;
            case 2:
                swap(nums, mid, high);
                high--;
                break;
        }
    }
}

private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
}
```

### The Invariant

Throughout the algorithm, the array maintains these zones:

```
[0, 0, 0, 1, 1, 1, 2, 2, 2]
          |        |        |
         low      mid     high
```

- `[0, low)` — all 0s ✅
- `[low, mid)` — all 1s ✅
- `[mid, high]` — unsorted (the unknown zone)
- `(high, n-1]` — all 2s ✅

### Why Does This Work?

When we see a 0 at `mid`:
- `low` is where the next 0 should go
- Swap with `low`, advance both `low` and `mid`
- After swap, position `low` has 0 ✅, position `mid` has whatever was at `low` (which was 1, since all 1s are in `[low, mid)`)

When we see a 1 at `mid`:
- It's already in the right zone, just advance `mid`

When we see a 2 at `mid`:
- `high` is where the next 2 should go
- Swap with `high`, decrement `high`
- **Don't advance `mid`** — the swapped-in element from `high` needs processing!

### Dry Run

```
nums = [2, 0, 2, 1, 1, 0]
low=0, mid=0, high=5

mid=0, nums[0]=2 → swap(0,5) → [0,0,2,1,1,2], high=4
mid=0, nums[0]=0 → swap(0,0) → no change, low=1, mid=1
mid=1, nums[1]=0 → swap(1,1) → no change, low=2, mid=2
mid=2, nums[2]=2 → swap(2,4) → [0,0,1,1,2,2], high=3
mid=2, nums[2]=1 → mid=3
mid=3, nums[3]=1 → mid=4
mid=4 ≤ high=3? No → exit

Result: [0, 0, 1, 1, 2, 2] ✓
```

### Complexity
- **Time**: O(n) — one pass
- **Space**: O(1)

### Counting Sort Alternative

```java
public void sortColorsCounting(int[] nums) {
    int count0 = 0, count1 = 0, count2 = 0;

    for (int num : nums) {
        if (num == 0) count0++;
        else if (num == 1) count1++;
        else count2++;
    }

    int i = 0;
    while (count0-- > 0) nums[i++] = 0;
    while (count1-- > 0) nums[i++] = 1;
    while (count2-- > 0) nums[i++] = 2;
}
```

Two-pass approach. Simpler but not as elegant. The one-pass three-pointer is the intended solution.

### Generic Dutch Flag (For N Colors)

```java
public void dutchFlag(int[] nums, int pivot) {
    int low = 0, mid = 0;
    int high = nums.length - 1;

    while (mid <= high) {
        if (nums[mid] < pivot) {
            swap(nums, low, mid);
            low++;
            mid++;
        } else if (nums[mid] == pivot) {
            mid++;
        } else {
            swap(nums, mid, high);
            high--;
        }
    }
}
```

## Partition Labels

### Problem Statement
Partition a string into as many parts as possible so that each character appears in at most one part.

```
Input:  "ababcbacadefegdehijhklij"
Output: [9, 7, 8]

Explanation:
"ababcbaca" — a,b,c only appear here
"defegde"   — d,e,f only appear here  
"hijhklij"  — h,i,j,k,l only appear here
```

### Approach

```java
public List<Integer> partitionLabels(String s) {
    // Step 1: Store the last occurrence of each character
    Map<Character, Integer> lastIndex = new HashMap<>();
    for (int i = 0; i < s.length(); i++) {
        lastIndex.put(s.charAt(i), i);
    }

    // Step 2: Expand windows
    List<Integer> result = new ArrayList<>();
    int start = 0;
    int end = 0;

    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        end = Math.max(end, lastIndex.get(c));

        if (i == end) {
            // Found a partition
            result.add(end - start + 1);
            start = i + 1;
        }
    }

    return result;
}
```

### How It Works

1. First pass: record the **last index** of each character
2. Second pass: expand the right boundary of the current partition as we encounter characters
3. When `i == end`, all characters in the current window appear only within it → partition!

The key insight: if a character appears at position `i` and its last occurrence is at `j`, then the partition must extend at least to `j`.

### Dry Run

```
s = "ababcbacadefegdehijhklij"

Last index map:
a→8, b→5, c→7, d→14, e→15, f→11, g→13, h→19, i→22, j→23, k→20, l→21

Iteration:
i=0, c='a', end=max(0,8)=8,  i≠end
i=1, c='b', end=max(8,5)=8,  i≠end
i=2, c='a', end=max(8,8)=8,  i≠end
i=3, c='b', end=max(8,5)=8,  i≠end
i=4, c='c', end=max(8,7)=8,  i≠end
i=5, c='b', end=max(8,5)=8,  i≠end
i=6, c='a', end=max(8,8)=8,  i≠end
i=7, c='c', end=max(8,7)=8,  i≠end
i=8, c='a', end=max(8,8)=8,  i==end → add 9, start=9
i=9, c='d', end=max(0,14)=14, i≠end
i=10,c='e', end=max(14,15)=15, i≠end
...continue until i=15, add 7
...continue until i=23, add 8

Result: [9, 7, 8] ✓
```

## Sort Array by Parity

Move all even numbers to the front, odd numbers to the back.

### Two-Pointer (Opposite Direction)

```java
public int[] sortArrayByParity(int[] nums) {
    int left = 0;
    int right = nums.length - 1;

    while (left < right) {
        // Find odd on the left
        while (left < right && nums[left] % 2 == 0) left++;
        // Find even on the right
        while (left < right && nums[right] % 2 == 1) right--;

        if (left < right) {
            swap(nums, left, right);
            left++;
            right--;
        }
    }

    return nums;
}

private void swap(int[] arr, int i, int j) {
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}
```

### Write-Pointer (Same Direction)

```java
public int[] sortArrayByParityWrite(int[] nums) {
    int write = 0;

    for (int read = 0; read < nums.length; read++) {
        if (nums[read] % 2 == 0) {
            swap(nums, write, read);
            write++;
        }
    }

    return nums;
}
```

### Stable Parity Sort (Preserves Relative Order)

```java
public int[] sortArrayByParityStable(int[] nums) {
    int[] result = new int[nums.length];
    int write = 0;

    for (int num : nums) {
        if (num % 2 == 0) result[write++] = num;
    }
    for (int num : nums) {
        if (num % 2 == 1) result[write++] = num;
    }

    return result;
}
```

## Partition Array Into Three Parts

```java
public boolean canThreePartsEqualSum(int[] arr) {
    int total = 0;
    for (int num : arr) total += num;

    if (total % 3 != 0) return false;

    int target = total / 3;
    int sum = 0;
    int count = 0;

    for (int i = 0; i < arr.length - 1; i++) {
        sum += arr[i];
        if (sum == target) {
            sum = 0;
            count++;
            if (count == 2) return true;
        }
    }

    return false;
}
```

## Partition by Pivot (QuickSort Partition)

```java
public int partition(int[] nums, int low, int high) {
    int pivot = nums[high];
    int i = low - 1; // Index of smaller element

    for (int j = low; j < high; j++) {
        if (nums[j] <= pivot) {
            i++;
            swap(nums, i, j);
        }
    }

    swap(nums, i + 1, high);
    return i + 1;
}
```

## Segregate 0s and 1s

```java
public void segregate01(int[] nums) {
    int left = 0, right = nums.length - 1;

    while (left < right) {
        while (left < right && nums[left] == 0) left++;
        while (left < right && nums[right] == 1) right--;

        if (left < right) {
            swap(nums, left, right);
            left++;
            right--;
        }
    }
}
```

## Pattern Summary

| Problem | Pointers | Condition | Complexity |
|---------|----------|-----------|------------|
| Dutch Flag (3 colors) | low, mid, high | 3-way partition | O(n), O(1) |
| Sort Colors | low, mid, high | Values 0,1,2 | O(n), O(1) |
| Partition Labels | start, end | Character last index | O(n), O(1) |
| Sort by Parity | left, right or write | Even/odd | O(n), O(1) |
| Segregate 0/1 | left, right | Binary values | O(n), O(1) |

## Interview Tips

1. **Dutch Flag is the hardest** — practice the three-pointer invariant explanation
2. **Partition Labels** — think "expand the window as needed"
3. **Always explain invariants** — "before low is all 0s, between low and mid is all 1s..."
4. **Know your partition schemes** — Lomuto (one-pass) vs Hoare (two-pointer from ends)

The beauty of partitioning problems is that they look like they need sorting (O(n log n)), but with the right pointer arrangement, you can do it in O(n). That's the signal interviewers are looking for.
