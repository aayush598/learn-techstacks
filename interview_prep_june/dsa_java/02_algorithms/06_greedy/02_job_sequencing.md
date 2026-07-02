# Job Sequencing with Deadlines

**Problem**: Each job has a deadline and profit. Each job takes 1 unit time. Schedule jobs to maximize profit. Only one job can be done at a time.

**Greedy**: Sort by profit descending. Schedule each job at the latest available slot before its deadline.

```java
public int jobScheduling(int[] deadlines, int[] profits) {
    int n = deadlines.length;
    int[][] jobs = new int[n][2];
    int maxDeadline = 0;

    for (int i = 0; i < n; i++) {
        jobs[i][0] = deadlines[i];
        jobs[i][1] = profits[i];
        maxDeadline = Math.max(maxDeadline, deadlines[i]);
    }

    Arrays.sort(jobs, (a, b) -> b[1] - a[1]); // sort by profit desc

    int[] slots = new int[maxDeadline + 1]; // 1-indexed
    int totalProfit = 0;

    for (int[] job : jobs) {
        // Find latest free slot before deadline
        for (int j = job[0]; j > 0; j--) {
            if (slots[j] == 0) {
                slots[j] = job[1];
                totalProfit += job[1];
                break;
            }
        }
    }

    return totalProfit;
}
```

## Optimization with Disjoint Set (O(n log n))

```java
public int jobScheduling(int[] deadlines, int[] profits) {
    int n = deadlines.length;
    int[][] jobs = new int[n][2];
    int maxDeadline = 0;

    for (int i = 0; i < n; i++) {
        jobs[i][0] = deadlines[i];
        jobs[i][1] = profits[i];
        maxDeadline = Math.max(maxDeadline, deadlines[i]);
    }

    Arrays.sort(jobs, (a, b) -> b[1] - a[1]);

    int[] parent = new int[maxDeadline + 2];
    for (int i = 0; i <= maxDeadline + 1; i++) parent[i] = i;

    int totalProfit = 0;

    for (int[] job : jobs) {
        int slot = find(parent, job[0]);
        if (slot > 0) {
            totalProfit += job[1];
            union(parent, slot, slot - 1); // mark slot as used
        }
    }

    return totalProfit;
}

int find(int[] parent, int x) {
    if (parent[x] != x) parent[x] = find(parent, parent[x]);
    return parent[x];
}

void union(int[] parent, int x, int y) {
    parent[x] = find(parent, y);
}
```

## Key Insight

> Schedule high-profit jobs first. Use union-find to quickly find the latest available slot.
