# Jump Game I & II

## Jump Game I — Can Reach End?

**Problem**: Each element is max jump length from that position. Can you reach the last index?

**Greedy**: Maintain `maxReach` — the furthest index reachable so far.

```java
public boolean canJump(int[] nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > maxReach) return false; // can't reach this position
        maxReach = Math.max(maxReach, i + nums[i]);
        if (maxReach >= nums.length - 1) return true;
    }
    return true;
}
```

## Jump Game II — Minimum Jumps

**Problem**: Find minimum jumps to reach the last index.

**Greedy/BFS**: Track the range reachable with current number of jumps.

```java
public int jump(int[] nums) {
    int jumps = 0, currentEnd = 0, farthest = 0;

    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);

        if (i == currentEnd) {
            jumps++;
            currentEnd = farthest;
        }
    }

    return jumps;
}
```

## Key Insight

> For Jump Game I: maintain the furthest reachable index. If at any point we can't reach i, return false.
> For Jump Game II: BFS on reachable ranges. Each jump extends the range.
