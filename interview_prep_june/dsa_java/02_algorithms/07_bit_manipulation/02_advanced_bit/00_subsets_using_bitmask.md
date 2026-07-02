# Subsets Using Bitmask

## Generate All Subsets

```java
public List<List<Integer>> subsets(int[] nums) {
    int n = nums.length;
    List<List<Integer>> result = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.add(nums[i]);
            }
        }
        result.add(subset);
    }
    return result;
}
```

## Count Subsets with Sum Condition

```java
public int countSubsetsWithSum(int[] nums, int target) {
    int n = nums.length, count = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) sum += nums[i];
        }
        if (sum == target) count++;
    }
    return count;
}
```
