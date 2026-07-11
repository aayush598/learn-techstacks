# Scheduling Problems with Heap

## Problem 1: Task Scheduler

CPU tasks with cooldown k, find minimum intervals:
```java
int leastInterval(char[] tasks, int n) {
    // Count frequencies
    Map<Character, Integer> freq = new HashMap<>();
    for (char c : tasks) freq.merge(c, 1, Integer::sum);
    
    // Max-heap of frequencies
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    maxHeap.addAll(freq.values());
    
    int time = 0;
    Queue<int[]> queue = new LinkedList<>();  // [count, readyTime]
    
    while (!maxHeap.isEmpty() || !queue.isEmpty()) {
        time++;
        
        if (!maxHeap.isEmpty()) {
            int count = maxHeap.poll() - 1;
            if (count > 0) queue.offer(new int[]{count, time + n});
        }
        
        if (!queue.isEmpty() && queue.peek()[1] == time) {
            maxHeap.offer(queue.poll()[0]);
        }
    }
    
    return time;
}
```

**Alternative formula** (O(n) without heap):
```java
int leastInterval(char[] tasks, int n) {
    int[] freq = new int[26];
    for (char c : tasks) freq[c - 'A']++;
    Arrays.sort(freq);
    
    int maxFreq = freq[25];
    int idleSlots = (maxFreq - 1) * n;
    
    for (int i = 24; i >= 0 && freq[i] > 0; i--) {
        idleSlots -= Math.min(freq[i], maxFreq - 1);
    }
    
    return tasks.length + Math.max(0, idleSlots);
}
```

## Problem 2: Meeting Rooms II

Minimum meeting rooms required:
```java
int minMeetingRooms(int[][] intervals) {
    if (intervals.length == 0) return 0;
    
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);  // sort by start time
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();  // end times
    
    minHeap.offer(intervals[0][1]);
    
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] >= minHeap.peek()) {
            minHeap.poll();  // reuse room
        }
        minHeap.offer(intervals[i][1]);
    }
    
    return minHeap.size();
}
```

## Problem 3: Course Schedule III

Max courses that can be taken (each has duration and deadline):
```java
int scheduleCourse(int[][] courses) {
    // Sort by deadline ascending
    Arrays.sort(courses, (a, b) -> a[1] - b[1]);
    
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    int totalTime = 0;
    
    for (int[] course : courses) {
        int duration = course[0], deadline = course[1];
        totalTime += duration;
        maxHeap.offer(duration);
        
        if (totalTime > deadline) {
            totalTime -= maxHeap.poll();  // drop the longest course
        }
    }
    
    return maxHeap.size();
}
```

## Problem 4: Rearrange String K Distance Apart

```java
String rearrangeString(String s, int k) {
    if (k == 0) return s;
    
    Map<Character, Integer> freq = new HashMap<>();
    for (char c : s.toCharArray()) freq.merge(c, 1, Integer::sum);
    
    PriorityQueue<Map.Entry<Character, Integer>> maxHeap = 
        new PriorityQueue<>((a, b) -> b.getValue() - a.getValue());
    maxHeap.addAll(freq.entrySet());
    
    Queue<Map.Entry<Character, Integer>> waitQ = new LinkedList<>();
    StringBuilder sb = new StringBuilder();
    
    while (!maxHeap.isEmpty()) {
        Map.Entry<Character, Integer> entry = maxHeap.poll();
        sb.append(entry.getKey());
        entry.setValue(entry.getValue() - 1);
        waitQ.offer(entry);
        
        if (waitQ.size() < k) continue;
        
        Map.Entry<Character, Integer> front = waitQ.poll();
        if (front.getValue() > 0) maxHeap.offer(front);
    }
    
    return sb.length() == s.length() ? sb.toString() : "";
}
```
