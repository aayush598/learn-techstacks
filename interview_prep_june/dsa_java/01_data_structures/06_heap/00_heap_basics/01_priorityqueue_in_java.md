# PriorityQueue in Java

## Overview

```java
PriorityQueue<E> pq = new PriorityQueue<>();
```
- **Min-heap by default** (smallest element at front)
- Not thread-safe (use `PriorityBlockingQueue` for thread-safety)
- Iterator does NOT guarantee order (must use `poll()` for sorted order)

## Constructors

```java
new PriorityQueue<>();                        // initial capacity 11
new PriorityQueue<>(20);                      // custom capacity
new PriorityQueue<>(Comparator.reverseOrder()); // max-heap
new PriorityQueue<>(collection);              // from existing collection
new PriorityQueue<>(new MyComparator());      // custom comparator
```

## Key Methods

```java
pq.offer(e);      // insert element, returns false if capacity-restricted
pq.add(e);        // insert element, throws exception if fails
pq.poll();        // retrieve and remove head (null if empty)
pq.peek();        // retrieve without removing (null if empty)
pq.remove(obj);   // remove specific object O(n)
pq.contains(obj); // check existence O(n)
pq.size();
pq.isEmpty();
pq.clear();
pq.toArray();     // copy to array
```

## Max-Heap with Comparator

```java
// Method 1: reverseOrder
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

// Method 2: lambda
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);
```

## Custom Objects

```java
class Student {
    String name;
    int grade;
    Student(String n, int g) { name = n; grade = g; }
}

// Min-heap by grade
PriorityQueue<Student> pq = new PriorityQueue<>(
    (a, b) -> a.grade - b.grade
);

// Or using Comparator.comparing
PriorityQueue<Student> pq = new PriorityQueue<>(
    Comparator.comparingInt(s -> s.grade)
);

// Multiple fields
PriorityQueue<Student> pq = new PriorityQueue<>(
    Comparator.comparingInt(Student::getGrade)
        .thenComparing(Student::getName)
);
```

## Time Complexities

| Operation | Time |
|-----------|------|
| offer/add | O(log n) |
| poll | O(log n) |
| peek | O(1) |
| remove(Object) | O(n) |
| contains | O(n) |
| size | O(1) |
