# Kahn's Algorithm (BFS-based Topological Sort)

## Overview

Topological sorting of a DAG in O(V+E) using in-degree tracking.

## Algorithm

```java
int[] topologicalSort(List<List<Integer>> graph, int V) {
    // 1. Compute in-degrees
    int[] inDegree = new int[V];
    for (int u = 0; u < V; u++) {
        for (int v : graph.get(u)) {
            inDegree[v]++;
        }
    }
    
    // 2. Queue vertices with 0 in-degree
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < V; i++) {
        if (inDegree[i] == 0) q.offer(i);
    }
    
    // 3. Process
    int[] topo = new int[V];
    int idx = 0;
    
    while (!q.isEmpty()) {
        int u = q.poll();
        topo[idx++] = u;
        
        for (int v : graph.get(u)) {
            inDegree[v]--;
            if (inDegree[v] == 0) q.offer(v);
        }
    }
    
    // 4. Check for cycle
    if (idx != V) throw new RuntimeException("Graph has a cycle");
    
    return topo;
}
```

## Problem: Course Schedule I (Can Finish?)

```java
boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    
    int[] inDegree = new int[numCourses];
    for (int[] pre : prerequisites) {
        graph.get(pre[1]).add(pre[0]);
        inDegree[pre[0]]++;
    }
    
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) q.offer(i);
    }
    
    int completed = 0;
    while (!q.isEmpty()) {
        int course = q.poll();
        completed++;
        for (int next : graph.get(course)) {
            if (--inDegree[next] == 0) q.offer(next);
        }
    }
    
    return completed == numCourses;
}
```

## Problem: Course Schedule II (Return Order)

```java
int[] findOrder(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    
    int[] inDegree = new int[numCourses];
    for (int[] pre : prerequisites) {
        graph.get(pre[1]).add(pre[0]);
        inDegree[pre[0]]++;
    }
    
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) q.offer(i);
    }
    
    int[] order = new int[numCourses];
    int idx = 0;
    
    while (!q.isEmpty()) {
        int course = q.poll();
        order[idx++] = course;
        for (int next : graph.get(course)) {
            if (--inDegree[next] == 0) q.offer(next);
        }
    }
    
    return idx == numCourses ? order : new int[0];
}
```
