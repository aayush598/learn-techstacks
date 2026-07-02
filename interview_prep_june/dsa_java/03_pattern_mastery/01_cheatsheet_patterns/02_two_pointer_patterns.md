# Two Pointer Patterns

## Table of Contents
1. Overview
2. Opposite Ends (Pair Sum, Palindrome)
3. Same Direction (Remove Duplicates, Merge)
4. Fast and Slow (Cycle Detection, Middle)
5. Partitioning (Dutch Flag, Sort by Parity)
6. Sliding Window as Special Case
7. Pattern Recognition

---

## 1. Overview

Two pointers is a technique where two reference variables traverse the data structure, often converging, diverging, or moving in tandem.

**When to use:**
- Sorted array (or can be sorted)
- Need to find pairs/triplets that satisfy condition
- Need to process two parts of array simultaneously
- In-place modification required

**Why O(n):** Each pointer moves O(n) total steps, no nested loops.

### Complexity Classes
| Pattern | Time | Space | Typical Use |
|---------|------|-------|-------------|
| Opposite ends | O(n) | O(1) | Pair sum, palindrome |
| Same direction | O(n) | O(1) | Remove duplicates, merge |
| Fast & slow | O(n) | O(1) | Cycle detection, middle |
| Partitioning | O(n) | O(1) | Dutch flag, sort by parity |

---

## 2. Opposite Ends (Converging Pointers)

**When to use:** Sorted array, need to find pairs. Palindrome checking.

**Template: Pair Sum in Sorted Array**
```java
public int[] twoSumSorted(int[] numbers, int target) {
    int left = 0, right = numbers.length - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            return new int[]{left + 1, right + 1};
        } else if (sum < target) {
            left++; // Need larger sum
        } else {
            right--; // Need smaller sum
        }
    }
    return new int[]{-1, -1};
}
```

**Template: Valid Palindrome**
```java
public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        // Skip non-alphanumeric
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
        if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right)))
            return false;
        left++;
        right--;
    }
    return true;
}
```

### Common Problems

**3Sum (a + b + c = 0)**
```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue; // skip duplicates
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++; right--;
            } else if (sum < 0) left++;
            else right--;
        }
    }
    return result;
}
```

**Container with Most Water**
```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, max = 0;
    while (left < right) {
        int area = Math.min(height[left], height[right]) * (right - left);
        max = Math.max(max, area);
        if (height[left] < height[right]) left++;
        else right--;
    }
    return max;
}
```

**Trapping Rain Water**
```java
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0, water = 0;
    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= leftMax) leftMax = height[left];
            else water += leftMax - height[left];
            left++;
        } else {
            if (height[right] >= rightMax) rightMax = height[right];
            else water += rightMax - height[right];
            right--;
        }
    }
    return water;
}
```

### Problems List
| Problem | Pattern | Complexity |
|---------|---------|------------|
| Two Sum II | Opposite ends | O(n) |
| 3Sum | Fix one + opposite ends | O(n²) |
| 3Sum Closest | Fix one + opposite ends | O(n²) |
| 4Sum | Two nested + opposite ends | O(n³) |
| Container with most water | Opposite ends | O(n) |
| Trapping rain water | Opposite ends with max tracking | O(n) |
| Valid palindrome | Opposite ends skip non-alnum | O(n) |
| Valid palindrome II | Opposite ends, allow one delete | O(n) |

---

## 3. Same Direction (Parallel Pointers)

**When to use:** In-place modification, merging two sorted arrays, slow builds result, fast traverses.

### Template: Remove Duplicates from Sorted Array
```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.length; fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
```

### Template: Move Zeroes
```java
public void moveZeroes(int[] nums) {
    int slow = 0;
    for (int fast = 0; fast < nums.length; fast++) {
        if (nums[fast] != 0) {
            int temp = nums[slow];
            nums[slow] = nums[fast];
            nums[fast] = temp;
            slow++;
        }
    }
}
```

### Template: Merge Two Sorted Arrays
```java
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int p1 = m - 1, p2 = n - 1, p = m + n - 1;
    while (p2 >= 0) {
        if (p1 >= 0 && nums1[p1] > nums2[p2]) {
            nums1[p--] = nums1[p1--];
        } else {
            nums1[p--] = nums2[p2--];
        }
    }
}
```

### Template: Intersection of Two Sorted Arrays
```java
public int[] intersect(int[] nums1, int[] nums2) {
    Arrays.sort(nums1);
    Arrays.sort(nums2);
    int i = 0, j = 0;
    List<Integer> list = new ArrayList<>();
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] < nums2[j]) i++;
        else if (nums1[i] > nums2[j]) j++;
        else {
            list.add(nums1[i]);
            i++; j++;
        }
    }
    return list.stream().mapToInt(k -> k).toArray();
}
```

### Problems List
| Problem | Pattern | Complexity |
|---------|---------|------------|
| Remove duplicates from sorted array | Slow/fast | O(n) |
| Remove element | Slow/fast | O(n) |
| Move zeroes | Slow/fast swap | O(n) |
| Merge two sorted arrays | Two pointers from end | O(m+n) |
| Intersection of two arrays | Two sorted pointers | O(n log n) |
| Backspace string compare | Two pointers from end | O(n) |
| Compare version numbers | Two string pointers | O(n) |

---

## 4. Fast and Slow Pointers

**When to use:** Linked list cycle detection, finding middle, finding nth from end.

### Template: Linked List Cycle Detection
```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```

### Template: Find Cycle Start (Floyd's Algorithm)
```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            // Cycle detected, find start
            slow = head;
            while (slow != fast) {
                slow = slow.next;
                fast = fast.next;
            }
            return slow;
        }
    }
    return null;
}
```

### Template: Find Middle of Linked List
```java
public ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}
```

### Problems on Arrays (not just linked lists)
The **Find the Duplicate Number** problem uses Floyd's algorithm on an array interpreted as a linked list:
```java
public int findDuplicate(int[] nums) {
    int slow = nums[0], fast = nums[0];
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);
    slow = nums[0];
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}
```

**Happy Number:**
```java
public boolean isHappy(int n) {
    int slow = n, fast = n;
    do {
        slow = digitSquareSum(slow);
        fast = digitSquareSum(digitSquareSum(fast));
    } while (slow != fast);
    return slow == 1;
}
private int digitSquareSum(int n) {
    int sum = 0;
    while (n > 0) {
        int d = n % 10;
        sum += d * d;
        n /= 10;
    }
    return sum;
}
```

### Problems List
| Problem | Insight | Complexity |
|---------|---------|------------|
| Linked list cycle | Floyd's algorithm | O(n) |
| Find cycle start | Floyd's second phase | O(n) |
| Middle of linked list | Fast moves 2x | O(n) |
| Palindrome linked list | Middle + reverse second half | O(n) |
| Find duplicate number | Array as linked list | O(n) |
| Happy number | Detect 1 cycle vs non-1 cycle | O(log n) |
| Reorder list | Middle + reverse + merge | O(n) |

---

## 5. Partitioning (Dutch National Flag)

**When to use:** Need to partition array into 2 or 3 categories in-place.

### Template: Sort Colors (Dutch Flag)
```java
public void sortColors(int[] nums) {
    int left = 0, right = nums.length - 1, curr = 0;
    while (curr <= right) {
        if (nums[curr] == 0) {
            swap(nums, curr, left);
            left++; curr++;
        } else if (nums[curr] == 2) {
            swap(nums, curr, right);
            right--;
        } else {
            curr++;
        }
    }
}
private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
}
```

### Template: Partition Array (QuickSelect style)
```java
// Partition around pivot (last element)
int partition(int[] nums, int left, int right) {
    int pivot = nums[right];
    int i = left; // position to place next smaller element
    for (int j = left; j < right; j++) {
        if (nums[j] <= pivot) {
            swap(nums, i, j);
            i++;
        }
    }
    swap(nums, i, right);
    return i;
}
```

### Problems List
| Problem | Pattern | Complexity |
|---------|---------|------------|
| Sort colors (0s, 1s, 2s) | Dutch flag, 3 pointers | O(n) |
| Sort array by parity | Two pointers (even/odd) | O(n) |
| Partition labels | Two pointers + last index map | O(n) |
| Segregate 0s and 1s | Two pointers swap | O(n) |
| QuickSelect (Kth smallest) | Partition + binary search | O(n) avg |
| All elements at left ≤ pivot | Single partition | O(n) |

---

## 6. Sliding Window as Special Case

Two pointers and sliding window are closely related. The key difference:

| Aspect | Two Pointers | Sliding Window |
|--------|-------------|----------------|
| Direction | Opposite or same | Always same direction |
| Window | Not necessarily contiguous | Always contiguous |
| State | Just the values at pointers | Complex window state |
| Use case | Pairs, partitioning, merging | Subarrays, substrings |

Sliding window is essentially same-direction two pointers with a maintained window state. When `left <= right` always holds and you maintain a cumulative state of the range `[left, right]`, it's sliding window.

### Generalized Framework
```java
// Left pointer conditionally advances
// Right pointer always advances in outer loop
for (int right = 0; right < n; right++) {
    // Expand window (add arr[right])
    while (condition to shrink) {
        // Shrink window (remove arr[left])
        left++;
    }
}
```

This is different from the normal two-pointer approaches where both pointers may advance independently.

---

## 7. Pattern Recognition

### Decision Flowchart
```
Is the array/string sorted?
├── YES → Can you reduce it to a pair search?
│   ├── YES → Opposite ends (Two Sum II)
│   └── NO → Binary search may be better
└── NO → Can you sort it without losing answer?
    ├── YES → Sort + Opposite ends (3Sum)
    └── NO → Is it about in-place modification?
        ├── YES → Same direction slow/fast
        └── NO → Is it about cycle detection?
            ├── YES → Fast & slow pointers
            └── NO → Is it about partitioning?
                ├── YES → Dutch flag partition
                └── NO → Sliding window or other technique
```

### Quick Reference: Problem → Algorithm

| Problem statement keywords | Algorithm |
|---------------------------|-----------|
| "Find pair with sum = target" in sorted array | Opposite ends |
| "Find triple with sum = target" | Fix one + opposite ends |
| "Remove duplicates in-place" | Same direction slow/fast |
| "Check if palindrome" | Opposite ends converge |
| "Linked list has cycle" | Fast & slow |
| "Find middle of linked list" | Fast & slow |
| "Sort array of 0s, 1s, 2s" | Dutch flag (3 pointers) |
| "Move all X to the front/back" | Two pointers swap |
| "Find duplicate number" (array 1..n) | Fast & slow on index |
| "Merge two sorted arrays" | Two pointers (or from end) |
| "Container with most water" | Opposite ends |
| "Trapping rain water" | Opposite ends with max |

### Complexities at a Glance
- O(n) time, O(1) space: The beauty of two pointers — linear time with constant extra space
- Sorting adds O(n log n) if array is not sorted (e.g., 3Sum)
- Dutch flag is single pass O(n) with 3 pointers
- Fast & slow is always O(n) with O(1) space
