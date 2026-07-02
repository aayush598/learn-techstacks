# Permutations of a String

**Problem**: Given a string, generate all possible permutations of its characters.

**Example**: `"abc"` → `["abc", "acb", "bac", "bca", "cab", "cba"]`

For n distinct characters, there are n! permutations.

---

## Approach 1: Swap-Based (Best for Strings)

Since strings are immutable in Java, we convert to a char array and swap in place.

```java
public List<String> permuteString(String s) {
    List<String> result = new ArrayList<>();
    char[] chars = s.toCharArray();
    permute(chars, 0, result);
    return result;
}

private void permute(char[] chars, int index, List<String> result) {
    if (index == chars.length - 1) {
        result.add(new String(chars));
        return;
    }

    for (int i = index; i < chars.length; i++) {
        swap(chars, index, i);
        permute(chars, index + 1, result);
        swap(chars, index, i); // backtrack
    }
}

private void swap(char[] chars, int i, int j) {
    char temp = chars[i];
    chars[i] = chars[j];
    chars[j] = temp;
}
```

### Visual Trace for "abc"

```
permute("abc", 0)
├── i=0: swap(0,0) → "abc"
│   └── permute("abc", 1)
│       ├── i=1: swap(1,1) → "abc"
│       │   └── permute("abc", 2) → add "abc"
│       └── i=2: swap(1,2) → "acb"
│           └── permute("acb", 2) → add "acb"
├── i=1: swap(0,1) → "bac"
│   └── permute("bac", 1)
│       ├── i=1: swap(1,1) → "bac"
│       │   └── permute("bac", 2) → add "bac"
│       └── i=2: swap(1,2) → "bca"
│           └── permute("bca", 2) → add "bca"
└── i=2: swap(0,2) → "cba"
    └── permute("cba", 1)
        ├── i=1: swap(1,1) → "cba"
        │   └── permute("cba", 2) → add "cba"
        └── i=2: swap(1,2) → "cab"
            └── permute("cab", 2) → add "cab"
```

---

## Approach 2: Used-Array with StringBuilder

```java
public List<String> permuteString(String s) {
    List<String> result = new ArrayList<>();
    boolean[] used = new boolean[s.length()];
    backtrack(s.toCharArray(), used, new StringBuilder(), result);
    return result;
}

private void backtrack(char[] chars, boolean[] used,
                       StringBuilder current, List<String> result) {
    if (current.length() == chars.length) {
        result.add(current.toString());
        return;
    }

    for (int i = 0; i < chars.length; i++) {
        if (used[i]) continue;

        used[i] = true;
        current.append(chars[i]);

        backtrack(chars, used, current, result);

        used[i] = false;
        current.deleteCharAt(current.length() - 1);
    }
}
```

---

## Handling Duplicates in String

**Example**: `"aab"` → `["aab", "aba", "baa"]` (not 6, but 3! / 2! = 3)

### With Sorting + Skip Condition

```java
public List<String> permuteUnique(String s) {
    List<String> result = new ArrayList<>();
    char[] chars = s.toCharArray();
    Arrays.sort(chars); // sort to bring duplicates together
    boolean[] used = new boolean[chars.length];
    backtrack(chars, used, new StringBuilder(), result);
    return result;
}

private void backtrack(char[] chars, boolean[] used,
                       StringBuilder current, List<String> result) {
    if (current.length() == chars.length) {
        result.add(current.toString());
        return;
    }

    for (int i = 0; i < chars.length; i++) {
        if (used[i]) continue;

        // KEY: skip duplicates — if same as previous and previous not used
        if (i > 0 && chars[i] == chars[i - 1] && !used[i - 1]) continue;

        used[i] = true;
        current.append(chars[i]);

        backtrack(chars, used, current, result);

        used[i] = false;
        current.deleteCharAt(current.length() - 1);
    }
}
```

### Why the Skip Condition Works

For `"aab"` (sorted = `['a', 'a', 'b']`):

Without skipping duplicates, we'd get:
```
aab, aab, aba, aba, baa, baa
```
Each permutation appears twice because the two 'a's are interchangeable.

With the skip condition `chars[i] == chars[i-1] && !used[i-1]`:
- At the root level, i=0 ('a') is used, i=1 ('a') is skipped (prev not used)
- At deeper levels, the second 'a' is only used if the first 'a' is already used

This ensures:
- `a a b` (both 'a's, in order) → valid
- `a b a` (first 'a', then 'b', then second 'a') → valid
- `b a a` ('b', then both 'a's in order) → valid
- But we never start a branch with the second 'a' when the first isn't used yet

---

## Print vs Store: Memory Considerations

### Printing (Memory Efficient)

```java
public void printPermutations(String s) {
    permuteAndPrint(s.toCharArray(), 0);
}

private void permuteAndPrint(char[] chars, int index) {
    if (index == chars.length - 1) {
        System.out.println(new String(chars));
        return;
    }
    for (int i = index; i < chars.length; i++) {
        swap(chars, index, i);
        permuteAndPrint(chars, index + 1);
        swap(chars, index, i);
    }
}
```

**Memory**: O(n) for recursion stack + char array. No storage of results.

### Storing (Memory Intensive)

```java
public List<String> storePermutations(String s) {
    List<String> result = new ArrayList<>();
    // ... generate and store
    return result;
}
```

**Memory**: O(n * n!) for storing all permutations.
- n=10: 3.6 million permutations × 10 chars ≈ 36 MB
- n=11: 39.9 million × 11 ≈ 439 MB
- n=12: 479 million × 12 ≈ 5.7 GB (impractical)

### Practical Limits

| n | n! | Memory to Store | Print Only |
|---|---|---|---|
| 5 | 120 | Negligible | Fine |
| 8 | 40,320 | Fine | Fine |
| 10 | 3,628,800 | ~36 MB | Fine |
| 12 | 479,001,600 | ~5.7 GB | Slow but possible |
| 15 | 1.3 × 10¹² | Impossible | Impossible |

**Rule of thumb**: If n > 10, printing is slow and storing is impractical. For n > 12, even backtracking itself is too slow. Mention this in interviews when asked to consider large inputs.

### Lazy Evaluation with Iterator

```java
public Iterator<String> permutationIterator(String s) {
    char[] chars = s.toCharArray();
    Arrays.sort(chars);
    return new Iterator<String>() {
        char[] current = chars.clone();
        boolean hasNext = true;

        @Override
        public boolean hasNext() {
            return hasNext;
        }

        @Override
        public String next() {
            String result = new String(current);
            hasNext = nextPermutation(current);
            return result;
        }
    };
}
```

This generates permutations one at a time without storing all.

---

## Lexicographic Order Generation

The swap-based approach does NOT generate permutations in lexicographic order.
For "abc", swap-based gives: abc, acb, bac, bca, cba, cab (not sorted).

### Generate in Lexicographic Order

Use the next-permutation algorithm repeatedly:

```java
public List<String> permuteLexicographic(String s) {
    List<String> result = new ArrayList<>();
    char[] chars = s.toCharArray();
    Arrays.sort(chars);

    do {
        result.add(new String(chars));
    } while (nextPermutation(chars));

    return result;
}

private boolean nextPermutation(char[] chars) {
    // Find first decreasing element from right
    int i = chars.length - 2;
    while (i >= 0 && chars[i] >= chars[i + 1]) i--;
    if (i < 0) return false;

    // Find next larger element to swap
    int j = chars.length - 1;
    while (chars[j] <= chars[i]) j--;
    swap(chars, i, j);

    // Reverse suffix
    reverse(chars, i + 1);
    return true;
}

private void reverse(char[] chars, int start) {
    int end = chars.length - 1;
    while (start < end) {
        swap(chars, start, end);
        start++;
        end--;
    }
}
```

---

## Problem Variations

### Permutations of Subset of String (k-permutations)

Generate all permutations of length k from the string:

```java
public List<String> permuteK(String s, int k) {
    List<String> result = new ArrayList<>();
    boolean[] used = new boolean[s.length()];
    backtrack(s.toCharArray(), k, used, new StringBuilder(), result);
    return result;
}

private void backtrack(char[] chars, int k, boolean[] used,
                       StringBuilder current, List<String> result) {
    if (current.length() == k) {
        result.add(current.toString());
        return;
    }

    for (int i = 0; i < chars.length; i++) {
        if (used[i]) continue;
        used[i] = true;
        current.append(chars[i]);
        backtrack(chars, k, used, current, result);
        current.deleteCharAt(current.length() - 1);
        used[i] = false;
    }
}
```

P(n,k) = n! / (n-k)! permutations of size k from n elements.

### Anagram Check Using Permutations

```java
// Check if s2 contains any anagram of s1
public boolean containsAnagram(String s1, String s2) {
    // Better: sliding window approach (O(n))
    // But permutations work for small s1
    List<String> perms = permuteString(s1);
    for (String perm : perms) {
        if (s2.contains(perm)) return true;
    }
    return false;
}
```

---

## Complexity Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Swap-based | O(n * n!) | O(n) | Most memory efficient |
| Used-array | O(n * n!) | O(n) | Most intuitive |
| Lexicographic | O(n * n!) | O(1) extra | Sorted order output |
| Print only | O(n * n!) | O(n) | Best for large n |

## Key Interview Takeaways

1. **Swap-based is preferred for strings** — no extra data structures
2. **Sort + skip for duplicates** — the `chars[i]==chars[i-1] && !used[i-1]` pattern
3. **For large n (>10), print instead of store** — mention memory constraints
4. **Lexicographic order** — use next-permutation, not swap-based
5. **Time complexity is always O(n * n!)** — no way around that for permutations
