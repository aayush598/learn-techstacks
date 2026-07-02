# Minimum Platforms (Railway Station)

**Problem**: Given arrival and departure times of trains, find minimum number of platforms needed at a station to avoid waiting time.

**Greedy**: Sort arrivals and departures separately. Use two pointers to track concurrent trains.

```java
public int findPlatform(int[] arr, int[] dep) {
    int n = arr.length;
    Arrays.sort(arr);
    Arrays.sort(dep);

    int platforms = 0, maxPlatforms = 0;
    int i = 0, j = 0;

    while (i < n && j < n) {
        if (arr[i] <= dep[j]) {
            platforms++; // train arrives
            maxPlatforms = Math.max(maxPlatforms, platforms);
            i++;
        } else {
            platforms--; // train departs
            j++;
        }
    }

    return maxPlatforms;
}
```

## Key Insight

> Sort both arrays. When a train arrives before the earliest departure, we need another platform. Otherwise, a platform frees up. This is O(n log n) and much simpler than interval overlap checking.
