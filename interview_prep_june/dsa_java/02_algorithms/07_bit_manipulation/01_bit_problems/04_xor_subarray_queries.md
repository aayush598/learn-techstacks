# XOR Subarray Queries

## XOR from L to R

```java
public int xorRange(int[] nums, int L, int R) {
    int[] prefix = new int[nums.length + 1];
    for (int i = 0; i < nums.length; i++) {
        prefix[i + 1] = prefix[i] ^ nums[i];
    }
    return prefix[R + 1] ^ prefix[L];
}
```

## Count Subarrays with XOR = K

```java
public int countSubarraysWithXorK(int[] nums, int k) {
    Map<Integer, Integer> prefixXor = new HashMap<>();
    prefixXor.put(0, 1);
    int xor = 0, count = 0;
    for (int num : nums) {
        xor ^= num;
        count += prefixXor.getOrDefault(xor ^ k, 0);
        prefixXor.put(xor, prefixXor.getOrDefault(xor, 0) + 1);
    }
    return count;
}
```
