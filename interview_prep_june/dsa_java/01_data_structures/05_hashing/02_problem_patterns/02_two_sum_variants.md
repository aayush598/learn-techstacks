# Two Sum Variants

## Problem 1: Two Sum (Classic)

Given array, find indices of two numbers that sum to target:
```java
int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();  // value -> index
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```
O(n) time, O(n) space.

## Problem 2: Two Sum II (Sorted Array)

```java
int[] twoSumSorted(int[] numbers, int target) {
    int left = 0, right = numbers.length - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) return new int[]{left + 1, right + 1};
        else if (sum < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}
```
O(n) time, O(1) space.

## Problem 3: Two Sum III (Data Structure Design)

Design a class supporting add(num) and find(sum):
```java
class TwoSum {
    Map<Integer, Integer> map = new HashMap<>();  // num -> frequency
    
    void add(int num) { map.merge(num, 1, Integer::sum); }
    
    boolean find(int target) {
        for (int num : map.keySet()) {
            int complement = target - num;
            if (complement == num) {
                if (map.get(num) >= 2) return true;
            } else if (map.containsKey(complement)) {
                return true;
            }
        }
        return false;
    }
}
```

## Problem 4: Two Sum IV (BST Input)

```java
boolean findTarget(TreeNode root, int k) {
    Set<Integer> set = new HashSet<>();
    return dfs(root, k, set);
}
boolean dfs(TreeNode node, int k, Set<Integer> set) {
    if (node == null) return false;
    if (set.contains(k - node.val)) return true;
    set.add(node.val);
    return dfs(node.left, k, set) || dfs(node.right, k, set);
}
```

## Problem 5: Three Sum

```java
List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue;  // skip duplicates
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(List.of(nums[i], nums[left], nums[right]));
                while (left < right && nums[left] == nums[left+1]) left++;
                while (left < right && nums[right] == nums[right-1]) right--;
                left++; right--;
            } else if (sum < 0) left++;
            else right--;
        }
    }
    return result;
}
```
O(n²) time.

## Problem 6: Four Sum

```java
List<List<Integer>> fourSum(int[] nums, int target) {
    Arrays.sort(nums);
    return kSum(nums, target, 0, 4);
}
List<List<Integer>> kSum(int[] nums, long target, int start, int k) {
    List<List<Integer>> result = new ArrayList<>();
    if (start == nums.length) return result;
    if (k == 2) return twoSum(nums, target, start);
    for (int i = start; i < nums.length - k + 1; i++) {
        if (i > start && nums[i] == nums[i-1]) continue;
        List<List<Integer>> sub = kSum(nums, target - nums[i], i + 1, k - 1);
        for (List<Integer> list : sub) {
            List<Integer> cur = new ArrayList<>(list);
            cur.add(0, nums[i]);
            result.add(cur);
        }
    }
    return result;
}
```
