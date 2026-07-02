# Activity Selection

**Problem**: Given start and end times of activities, select maximum number of non-overlapping activities.

**Greedy**: Sort by end time, pick the one that finishes earliest.

```java
public int activitySelection(int[] start, int[] end) {
    int n = start.length;
    int[][] activities = new int[n][2];
    for (int i = 0; i < n; i++) {
        activities[i][0] = start[i];
        activities[i][1] = end[i];
    }

    Arrays.sort(activities, (a, b) -> a[1] - b[1]);

    int count = 1;
    int lastEnd = activities[0][1];

    for (int i = 1; i < n; i++) {
        if (activities[i][0] >= lastEnd) {
            count++;
            lastEnd = activities[i][1];
        }
    }

    return count;
}
```

## N Meetings in One Room

Same problem, different name. Find max meetings that can be held in one room.

```java
public int maxMeetings(int[] start, int[] end) {
    return activitySelection(start, end);
}
```

## Key Insight

> Earliest finish time leaves maximum room for remaining activities. This is proven by exchange argument.
