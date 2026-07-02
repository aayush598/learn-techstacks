# 01 — Control Flow in Java for DSA

Control flow is the skeleton of every algorithm. Loops and conditionals are where your logic lives. Master these, and you've cleared half the battle.

---

## 1. Conditional Statements

### if-else

The workhorse. Straightforward.

```java
int score = 85;
if (score >= 90) {
    System.out.println("A");
} else if (score >= 80) {
    System.out.println("B");
} else if (score >= 70) {
    System.out.println("C");
} else {
    System.out.println("Fail");
}
```

**Nested if — use sparingly:**

```java
if (x > 0) {
    if (y > 0) {
        System.out.println("Quadrant I");
    } else {
        System.out.println("Quadrant IV");
    }
}
```

**Pro tip:** Flatten nested ifs when possible. Deep nesting = bug magnet.

```java
// 👎 Nested
if (user != null) {
    if (user.isActive()) {
        if (user.hasPermission()) {
            doSomething();
        }
    }
}

// 👍 Guard clauses
if (user == null) return;
if (!user.isActive()) return;
if (!user.hasPermission()) return;
doSomething();
```

### Ternary Operator — The Concise if-else

```java
int max = (a > b) ? a : b;
String result = (n % 2 == 0) ? "Even" : "Odd";

// Nested ternary (avoid — hurts readability)
int x = (a > b) ? ((a > c) ? a : c) : ((b > c) ? b : c);
```

**When to use:** Simple assignments. Never nest them.

### switch — Pre-Java 14 (The Old Way)

```java
int day = 3;
String dayName;

switch (day) {
    case 1:
        dayName = "Monday";
        break;          // Don't forget! Fall-through otherwise
    case 2:
        dayName = "Tuesday";
        break;
    case 3:
        dayName = "Wednesday";
        break;
    default:
        dayName = "Unknown";
        break;
}
```

**Fall-through pitfall:** If you omit `break`, execution falls through to the next case:

```java
switch (x) {
    case 1:
        System.out.println("One");
        // no break — falls through!
    case 2:
        System.out.println("Two");
        break;
}
// Input x=1 → prints "One" AND "Two"
```

**Intentional fall-through** (when you want it):

```java
switch (grade) {
    case 'A':
    case 'B':
    case 'C':
        System.out.println("Pass");
        break;
    case 'D':
    case 'F':
        System.out.println("Fail");
        break;
}
```

### switch — Java 14+ Arrow Syntax (The New Way)

```java
String result = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3 -> "Wednesday";
    case 4 -> "Thursday";
    case 5 -> "Friday";
    case 6, 7 -> "Weekend";    // Multiple labels
    default -> "Invalid";
};

// With code blocks — need 'yield' to return value
String result = switch (score / 10) {
    case 10, 9 -> "A";
    case 8 -> "B";
    case 7 -> {
        System.out.println("Close!");
        yield "C";
    }
    default -> "F";
};
```

**Arrow syntax advantages:** No fall-through, no `break`, can be used as expression. If you're on Java 14+, prefer this.

### Key Differences Summary

| Feature | Old switch | New switch (14+) |
|---------|-----------|------------------|
| Fall-through | Yes (without break) | No (arrow = implicit break) |
| Expression | No (use if-else chain) | Yes (returns value) |
| Multiple labels | case 6: case 7: | case 6, 7 -> |
| Statement vs Expression | Statement only | Both |

---

## 2. Loops

### for Loop — The Classic

```java
// Standard: init; condition; update
for (int i = 0; i < n; i++) {
    System.out.println(i);
}

// Multiple variables
for (int i = 0, j = n - 1; i < j; i++, j--) {
    // Two-pointer pattern
}

// Breaking early
for (int i = 0; i < n; i++) {
    if (arr[i] == target) {
        System.out.println("Found at " + i);
        break;
    }
}

// Continuing
for (int i = 0; i < n; i++) {
    if (arr[i] % 2 == 0) continue;  // skip evens
    System.out.println(arr[i]);      // prints odds only
}
```

### Enhanced for-each — When Index Doesn't Matter

```java
int[] arr = {10, 20, 30, 40, 50};

for (int num : arr) {
    System.out.println(num);
}

// Works with all Iterables
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
for (String name : names) {
    System.out.println(name);
}

// ⚠️ for-each CANNOT:
// - Access index (use regular for)
// - Modify the array (you get a copy of the element)
// - Remove elements from collection (use iterator.remove())
for (int num : arr) {
    num = 0;  // ❌ doesn't modify original array
}
```

### Labeled Loops — Breaking Out of Nested Loops

```java
// Without label — breaks only inner loop
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (i == 1 && j == 1) break;
        System.out.println(i + " " + j);
    }
}
// Output: (0,0) (0,1) (0,2) (1,0) (1,1 was skipped... wait, breaks inner, so (1,0) only)

// With label — breaks out of outer loop
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (i == 1 && j == 1) break outer;
        System.out.println(i + " " + j);
    }
}
// Output: (0,0) (0,1) (0,2) (1,0)
```

**Pro tip:** Labeled breaks are a code smell if overused. Often, extracting to a method with `return` is cleaner.

```java
// Alternative: extract to method + return
public static boolean findInMatrix(int[][] mat, int target) {
    for (int i = 0; i < mat.length; i++) {
        for (int j = 0; j < mat[0].length; j++) {
            if (mat[i][j] == target) return true;
        }
    }
    return false;
}
```

### while Loop — When You Don't Know the Count

```java
// Classic: count digits
int n = 12345, count = 0;
while (n > 0) {
    n /= 10;
    count++;
}

// While with a condition variable
boolean found = false;
int i = 0;
while (!found && i < arr.length) {
    if (arr[i] == target) found = true;
    i++;
}

// Infinite loop (use with break)
while (true) {
    int x = sc.nextInt();
    if (x == -1) break;
    process(x);
}
```

### do-while — Execute At Least Once

```java
// Menu-driven program
int choice;
do {
    System.out.println("1. Add  2. Exit");
    choice = sc.nextInt();
    if (choice == 1) add();
} while (choice != 2);

// Palindrome check using reversal
int n = 12321;
int reversed = 0, original = n;
do {
    reversed = reversed * 10 + n % 10;
    n /= 10;
} while (n > 0);
System.out.println(original == reversed);  // true
```

---

## 3. break, continue, return

```java
// break — exits the loop entirely
for (int i = 0; i < 10; i++) {
    if (i == 5) break;
    System.out.print(i + " ");  // 0 1 2 3 4
}

// continue — skips to next iteration
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;
    System.out.print(i + " ");  // 1 3 5 7 9
}

// return — exits the entire method
public static int firstPositive(int[] arr) {
    for (int num : arr) {
        if (num > 0) return num;
    }
    return -1;  // or throw exception
}
```

---

## 4. Common DSA Loop Patterns

### Pattern 1: Two Pointers (Front and Back)

```java
int[] arr = {1, 2, 3, 4, 5, 6};
int left = 0, right = arr.length - 1;
while (left < right) {
    // swap or compare
    int temp = arr[left];
    arr[left] = arr[right];
    arr[right] = temp;
    left++;
    right--;
}
```

### Pattern 2: Sliding Window

```java
// Fixed window size k
int k = 3, windowSum = 0;
for (int i = 0; i < k; i++) windowSum += arr[i];  // first window
int maxSum = windowSum;

for (int i = k; i < arr.length; i++) {
    windowSum += arr[i] - arr[i - k];  // slide window
    maxSum = Math.max(maxSum, windowSum);
}
```

```java
// Variable window — smallest subarray with sum >= target
int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
for (int right = 0; right < arr.length; right++) {
    sum += arr[right];
    while (sum >= target) {
        minLen = Math.min(minLen, right - left + 1);
        sum -= arr[left++];
    }
}
```

### Pattern 3: Fast and Slow Pointers (Cycle Detection)

```java
// On a linked list (array indices simulating next pointers)
int[] next = {1, 2, 3, 4, 5, 3};  // points to index 3 → cycle!
int slow = 0, fast = 0;
do {
    slow = next[slow];
    fast = next[next[fast]];
} while (slow != fast);
System.out.println("Cycle detected at index " + slow);
```

### Pattern 4: Loop with Half Increments (Logarithmic)

```java
// O(log n) — binary search, exponentiation
for (int i = n; i > 0; i /= 2) {
    System.out.println(i);
}
// n=16 → 16 8 4 2 1
```

```java
// Binary search template
int low = 0, high = n - 1;
while (low <= high) {
    int mid = low + (high - low) / 2;  // avoid overflow
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) low = mid + 1;
    else high = mid - 1;
}
```

### Pattern 5: Loop with sqrt Bounds

```java
// Check if prime — O(√n)
boolean isPrime = n > 1;
for (int i = 2; i * i <= n; i++) {
    if (n % i == 0) {
        isPrime = false;
        break;
    }
}
```

### Pattern 6: Running Maximum / Prefix Sum

```java
// Prefix sum — O(n) build, O(1) range sum query
int[] prefix = new int[n + 1];  // extra space for convenience
for (int i = 0; i < n; i++) {
    prefix[i + 1] = prefix[i] + arr[i];
}
// Range sum [l, r] (inclusive): prefix[r+1] - prefix[l]

// Running maximum (left to right, right to left)
int[] leftMax = new int[n];
int maxSoFar = Integer.MIN_VALUE;
for (int i = 0; i < n; i++) {
    maxSoFar = Math.max(maxSoFar, arr[i]);
    leftMax[i] = maxSoFar;
}
```

### Pattern 7: Nested Loop — Matrix Traversal

```java
int[][] mat = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

// Row-major order
for (int i = 0; i < mat.length; i++) {
    for (int j = 0; j < mat[0].length; j++) {
        System.out.print(mat[i][j] + " ");
    }
}

// Column-major order
for (int j = 0; j < mat[0].length; j++) {
    for (int i = 0; i < mat.length; i++) {
        System.out.print(mat[i][j] + " ");
    }
}

// Diagonal traversal
for (int i = 0; i < mat.length; i++) {
    System.out.print(mat[i][i] + " ");       // main diagonal
    System.out.print(mat[i][n-1-i] + " ");  // anti-diagonal
}
```

### Pattern 8: Reading Until EOF

```java
// Using Scanner
while (sc.hasNextInt()) {
    int n = sc.nextInt();
    process(n);
}

// Using BufferedReader
String line;
while ((line = br.readLine()) != null) {
    process(line);
}
```

---

## 5. Performance Notes

```java
// ❌ DON'T: calculate length each iteration (wasteful)
for (int i = 0; i < arr.length; i++) { ... }  // fine for arrays (O(1))
for (int i = 0; i < list.size(); i++) { ... } // fine, but...

// ✅ DO: cache when using LinkedList
int size = list.size();
for (int i = 0; i < size; i++) {
    list.get(i);  // O(n) per call for LinkedList!
}
// Actually, just don't use get() on LinkedList in loops
// Use for-each or iterator

// ❌ DON'T: string concatenation in loops
String s = "";
for (int i = 0; i < 1000; i++) {
    s += i;  // O(n²) — creates new String each iteration!
}

// ✅ DO: use StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String s = sb.toString();  // O(n)
```

---

## Control Flow Cheat Sheet

```java
// CONDITIONALS
if (condition) { } else if (condition) { } else { }
int x = (cond) ? val1 : val2;

// OLD SWITCH
switch(x) { case 1: break; default: }

// NEW SWITCH (14+)
String s = switch(x) { case 1 -> "one"; default -> "other"; };

// LOOPS
for (int i = 0; i < n; i++) { }
for (int x : arr) { }
while (condition) { }
do { } while (condition);

// JUMP
break; continue; return; label: for(...) { break label; }
```

Recap: Loops are where algorithms come alive. Understand every pattern above — you'll see them in at least 60% of all DSA problems.
