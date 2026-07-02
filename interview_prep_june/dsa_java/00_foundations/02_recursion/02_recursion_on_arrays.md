# 02 — Recursion on Arrays

Recursion on arrays follows a natural pattern: process the first element (or a portion), then recurse on the rest. The index acts as the "size of the problem" that decreases toward the base case.

---

## 1. Check if Array is Sorted

```java
boolean isSorted(int[] arr, int index) {
    if (index == arr.length - 1 || arr.length == 0) {
        return true;
    }
    if (arr[index] > arr[index + 1]) {
        return false;
    }
    return isSorted(arr, index + 1);
}

// Usage
int[] arr1 = {1, 2, 3, 4, 5};
int[] arr2 = {1, 3, 2, 4, 5};
System.out.println(isSorted(arr1, 0));  // true
System.out.println(isSorted(arr2, 0));  // false
```

**Complexity:** O(n) time, O(n) stack space.

---

## 2. Linear Search with Recursion

### Find First Occurrence

```java
int firstOccurrence(int[] arr, int target, int index) {
    if (index == arr.length) return -1;
    if (arr[index] == target) return index;
    return firstOccurrence(arr, target, index + 1);
}
```

### Find Last Occurrence

```java
int lastOccurrence(int[] arr, int target, int index) {
    if (index < 0) return -1;
    if (arr[index] == target) return index;
    return lastOccurrence(arr, target, index - 1);
}
```

---

## 3. Find All Indices of Target

```java
List<Integer> findAllIndices(int[] arr, int target, int index) {
    List<Integer> result = new ArrayList<>();
    if (index == arr.length) return result;

    if (arr[index] == target) result.add(index);

    List<Integer> fromRest = findAllIndices(arr, target, index + 1);
    result.addAll(fromRest);
    return result;
}

// More efficient — pass the list (avoid creating many intermediate lists)
void findAllIndices(int[] arr, int target, int index, List<Integer> result) {
    if (index == arr.length) return;
    if (arr[index] == target) result.add(index);
    findAllIndices(arr, target, index + 1, result);
}

// Usage
int[] arr = {3, 2, 3, 5, 3, 7};
List<Integer> indices = new ArrayList<>();
findAllIndices(arr, 3, 0, indices);
System.out.println(indices);  // [0, 2, 4]
```

---

## 4. Reverse an Array with Recursion

```java
void reverse(int[] arr, int left, int right) {
    if (left >= right) return;
    int temp = arr[left];
    arr[left] = arr[right];
    arr[right] = temp;
    reverse(arr, left + 1, right - 1);
}

// Usage
int[] arr = {1, 2, 3, 4, 5};
reverse(arr, 0, arr.length - 1);
System.out.println(Arrays.toString(arr));  // [5, 4, 3, 2, 1]
```

---

## 5. Recursive Binary Search

```java
int binarySearch(int[] arr, int target, int left, int right) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target)
        return binarySearch(arr, target, mid + 1, right);
    return binarySearch(arr, target, left, mid - 1);
}

int binarySearch(int[] arr, int target) {
    return binarySearch(arr, target, 0, arr.length - 1);
}

// First occurrence in sorted array with duplicates
int firstOccurrence(int[] arr, int target, int left, int right) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) {
        if (mid == 0 || arr[mid - 1] != target) return mid;
        return firstOccurrence(arr, target, left, mid - 1);
    } else if (arr[mid] < target) {
        return firstOccurrence(arr, target, mid + 1, right);
    } else {
        return firstOccurrence(arr, target, left, mid - 1);
    }
}
```

---

## 6. Rotated Binary Search with Recursion

Search in a rotated sorted array like `[4, 5, 6, 7, 0, 1, 2]`.

```java
int rotatedBinarySearch(int[] arr, int target, int left, int right) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) return mid;

    if (arr[left] <= arr[mid]) {
        // Left half is sorted
        if (target >= arr[left] && target < arr[mid])
            return rotatedBinarySearch(arr, target, left, mid - 1);
        else
            return rotatedBinarySearch(arr, target, mid + 1, right);
    } else {
        // Right half is sorted
        if (target > arr[mid] && target <= arr[right])
            return rotatedBinarySearch(arr, target, mid + 1, right);
        else
            return rotatedBinarySearch(arr, target, left, mid - 1);
    }
}

// Usage
int[] rotated = {4, 5, 6, 7, 0, 1, 2};
System.out.println(rotatedBinarySearch(rotated, 0, 0, rotated.length - 1));  // 4
System.out.println(rotatedBinarySearch(rotated, 3, 0, rotated.length - 1));  // -1
```

**Key insight:** At least one half of any subarray is always sorted. Determine which, then check if the target lies there.

---

## 7. Complete Example: All Array Operations

```java
public class RecursiveArrayOps {

    static int sum(int[] arr, int n) {
        if (n <= 0) return 0;
        return sum(arr, n - 1) + arr[n - 1];
    }

    static int product(int[] arr, int n) {
        if (n <= 0) return 1;
        return product(arr, n - 1) * arr[n - 1];
    }

    static int max(int[] arr, int n) {
        if (n == 1) return arr[0];
        return Math.max(arr[n - 1], max(arr, n - 1));
    }

    static int min(int[] arr, int n) {
        if (n == 1) return arr[0];
        return Math.min(arr[n - 1], min(arr, n - 1));
    }

    static void reverse(int[] arr, int l, int r) {
        if (l >= r) return;
        int temp = arr[l]; arr[l] = arr[r]; arr[r] = temp;
        reverse(arr, l + 1, r - 1);
    }

    static boolean isPalindrome(int[] arr, int l, int r) {
        if (l >= r) return true;
        if (arr[l] != arr[r]) return false;
        return isPalindrome(arr, l + 1, r - 1);
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        System.out.println("Sum: " + sum(arr, arr.length));
        System.out.println("Max: " + max(arr, arr.length));
        reverse(arr, 0, arr.length - 1);
        System.out.println("Reversed: " + Arrays.toString(arr));

        int[] pal = {1, 2, 3, 2, 1};
        System.out.println("Is palindrome: " + isPalindrome(pal, 0, pal.length - 1));
    }
}
```

---

## 8. The "Trust the Recursion" Mindset

```java
boolean isSorted(int[] arr, int i) {
    // "I'll check just the first pair.
    //  You handle the rest, isSorted function."
    if (i == arr.length - 1) return true;
    if (arr[i] > arr[i + 1]) return false;
    return isSorted(arr, i + 1);
}
```

Each call does **one unit of work** and passes the rest to the next call.

---

## Cheat Sheet

```java
isSorted(arr, i)       -> check pair && recurse
linearSearch(arr, i)   -> arr[i]==target || recurse
binarySearch(arr,l,r)  -> T(n/2) pattern
rotatedSearch(arr,l,r) -> check sorted half, recurse
reverse(arr,l,r)       -> swap ends, recurse inward
```
