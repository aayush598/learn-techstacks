# Remove Duplicates and In-Place Modifications

In-place array modification is a superpower. It lets you "remove" elements without creating new arrays. The key is the **write pointer** technique — a same-direction two-pointer pattern.

## The Write Pointer Pattern

The idea is simple:
- **Read pointer (r)**: scans the array, examining each element
- **Write pointer (w)**: marks where to place the next "kept" element

By the end, elements before `w` are the kept elements, and elements from `w` onward are garbage (don't matter).

```
Before: [1, 1, 2, 2, 3, 3, 4]
               r          w=1
                   
After:  [1, 2, 3, 4, _, _, _]
               w=4
Length of kept portion: 4
```

## Remove Duplicates from Sorted Array I

Remove duplicates in-place such that each element appears **at most once**.

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;

    int write = 0; // Position of last unique element

    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[write]) {
            write++;
            nums[write] = nums[read];
        }
    }

    return write + 1; // Length is index + 1
}
```

### How It Works

1. `write` starts at 0 (first element is always kept)
2. For each element at `read`:
   - If it's different from the last unique element (`nums[write]`), advance `write` and copy
   - If it's the same, skip it (read moves, write stays)

### Dry Run

```
nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
w=0, r=1 → nums[1]=0 == nums[0]=0 → skip
w=0, r=2 → nums[2]=1 != nums[0]=0 → w=1, nums[1]=1
w=1, r=3 → nums[3]=1 == nums[1]=1 → skip
w=1, r=4 → nums[4]=1 == nums[1]=1 → skip
w=1, r=5 → nums[5]=2 != nums[1]=1 → w=2, nums[2]=2
w=2, r=6 → nums[6]=2 == nums[2]=2 → skip
w=2, r=7 → nums[7]=3 != nums[2]=2 → w=3, nums[3]=3
w=3, r=8 → nums[8]=3 == nums[3]=3 → skip
w=3, r=9 → nums[9]=4 != nums[3]=3 → w=4, nums[4]=4

Result: write+1 = 5 (unique elements: 0,1,2,3,4)
Array: [0, 1, 2, 3, 4, _, _, _, _, _]
```

## Remove Duplicates from Sorted Array II

Each element can appear **at most twice**.

```java
public int removeDuplicatesII(int[] nums) {
    if (nums.length <= 2) return nums.length;

    int write = 2; // First two elements are always kept

    for (int read = 2; read < nums.length; read++) {
        if (nums[read] != nums[write - 2]) {
            nums[write] = nums[read];
            write++;
        }
    }

    return write;
}
```

### The Trick

We compare `nums[read]` with `nums[write - 2]`, not `nums[write - 1]`. Why?

- `nums[write - 1]` is the *most recent* kept element
- `nums[write - 2]` is the element *two positions back*

If `nums[read]` equals `nums[write - 2]`, that means we'd have three copies if we kept it. So we skip.

### Generalization: At Most K Copies

```java
public int removeDuplicatesK(int[] nums, int k) {
    if (nums.length <= k) return nums.length;

    int write = k;

    for (int read = k; read < nums.length; read++) {
        if (nums[read] != nums[write - k]) {
            nums[write] = nums[read];
            write++;
        }
    }

    return write;
}
```

## Remove Element

Remove all occurrences of a specific value.

```java
public int removeElement(int[] nums, int val) {
    int write = 0;

    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != val) {
            nums[write] = nums[read];
            write++;
        }
    }

    return write;
}
```

### Dry Run

```
nums = [3, 2, 2, 3], val = 3
w=0, r=0 → nums[0]=3 == val → skip
w=0, r=1 → nums[1]=2 != val → nums[0]=2, w=1
w=1, r=2 → nums[2]=2 != val → nums[1]=2, w=2
w=2, r=3 → nums[3]=3 == val → skip

Result: write=2
Array: [2, 2, _, _]
```

## Move Zeros

Move all zeros to the end while maintaining the relative order of non-zero elements.

```java
public void moveZeroes(int[] nums) {
    int write = 0;

    // Move all non-zero elements to the front
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != 0) {
            nums[write] = nums[read];
            write++;
        }
    }

    // Fill the rest with zeros
    while (write < nums.length) {
        nums[write] = 0;
        write++;
    }
}
```

### Swap-Based Version

```java
public void moveZeroesSwap(int[] nums) {
    int write = 0;

    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != 0) {
            int temp = nums[write];
            nums[write] = nums[read];
            nums[read] = temp;
            write++;
        }
    }
}
```

The swap version avoids the second loop by swapping elements in-place. This is useful if you want to preserve the original elements better (no overwriting).

### Why Use Swap?

```
Original: [0, 1, 0, 3, 12]

Non-swap version:
  → [1, 3, 12, 0, 0] (zeros at end, good)

Swap version:
  → [1, 3, 12, 0, 0] (same result)
  
But with non-zero elements:
  Original: [2, 1] (no zeros)
  Non-swap: [2, 1] (unchanged? Actually copy happens)
  Swap:     [2, 1] (unchanged, no swap needed since nothing moves)
```

Both work. The swap version uses a bit more time (extra swaps) but maintains the invariant that the write area contains the original elements.

## Remove Duplicates from Unsorted Array

If the array isn't sorted, use a HashSet.

```java
public int removeDuplicatesUnsorted(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    int write = 0;

    for (int read = 0; read < nums.length; read++) {
        if (!seen.contains(nums[read])) {
            seen.add(nums[read]);
            nums[write] = nums[read];
            write++;
        }
    }

    return write;
}
```

This is O(n) time but O(n) space (for the HashSet).

## Remove All Occurrences of Value (Multiple)

Same as Remove Element. Already covered above.

## Remove Duplicates from Sorted Array Using Two Pointers (Alternate)

You can also use the same approach but with distinct read/write roles:

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;

    int i = 0; // Write pointer

    for (int j = 1; j < nums.length; j++) {
        if (nums[j] != nums[i]) {
            i++;
            nums[i] = nums[j];
        }
    }

    return i + 1;
}
```

This is essentially the same as our first version but using `i` and `j` instead of `write` and `read`.

## Pattern Summary

All these problems follow the same template:

```java
int write = <initial_value>;

for (int read = <start>; read < arr.length; read++) {
    if (<condition to keep element>) {
        arr[write] = arr[read];
        write++;
    }
}

return write; // or write + 1 depending on setup
```

| Problem | Condition | Write Start | Return |
|---------|-----------|-------------|--------|
| Remove Duplicates I | `arr[read] != arr[write]` | 0 | `write + 1` |
| Remove Duplicates II | `arr[read] != arr[write - 2]` | 2 | `write` |
| Remove Duplicates K | `arr[read] != arr[write - k]` | k | `write` |
| Remove Element | `arr[read] != val` | 0 | `write` |
| Move Zeros | `arr[read] != 0` | 0 | N/A (void) |

## Interview Tips

1. **Explain the write pointer** — "the read pointer discovers elements, the write pointer places them"
2. **Handle empty arrays** — always check `nums.length == 0`
3. **For Duplicates II**, explain why we compare with `write - 2` — "this ensures at most two copies"
4. **Move Zeros** — mention the trade-off between two-pass and swap versions
5. **All these are O(n) time, O(1) space** — that's the whole point

The write pointer is one of the most common patterns in coding interviews. Master it here, and you'll use it everywhere.
