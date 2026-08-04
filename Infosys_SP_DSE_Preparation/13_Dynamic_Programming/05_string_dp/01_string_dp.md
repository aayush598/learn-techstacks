# String DP Problems

String DP problems involve computing an optimal or counting result over one or two strings, where the state is defined by prefixes (or substrings). The classic shape is `dp[i][j]` = answer for `s1[:i]` and `s2[:j]`. Problems already covered elsewhere (LCS, Edit Distance, Distinct Subsequences, LPS, SCS, Wildcard, Regex) are omitted here.

---

## 1. Edit Distance — Operations Listed (LC #72 variant) — Medium

### Problem Explanation
Given two strings `word1` and `word2`, find the minimum number of operations to convert `word1` to `word2` AND return the actual sequence of operations (insert, delete, replace). This extends the standard Edit Distance by requiring the reconstruction of the optimal path through the DP table.

### State Definition
`dp[i][j]` = minimum operations to convert `word1[:i]` into `word2[:j]`. Same as standard edit distance.

### Recurrence Relation
```
if word1[i-1] == word2[j-1]:  dp[i][j] = dp[i-1][j-1]
else:  dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```
Operations: `dp[i-1][j]+1` = delete, `dp[i][j-1]+1` = insert, `dp[i-1][j-1]+1` = replace.

### Base Cases
- `dp[0][j] = j` (j inserts to build `word2[:j]` from empty).
- `dp[i][0] = i` (i deletes to empty `word1[:i]`).

### Intuition
After filling the table identically to standard edit distance, we trace back from `dp[m][n]` to `dp[0][0]`. At each cell, the value was produced by one of three operations; recording which one reconstructs the sequence.

### Step-by-Step Procedure
1. Build `(m+1)×(n+1)` dp table for edit distance.
2. Fill base row/col, then all cells with the standard recurrence.
3. Start at `i=m, j=n` with an empty operations list.
4. While `i > 0` or `j > 0`:
5. If `word1[i-1] == word2[j-1]`: record "match", move diagonal.
6. Else find which of the three neighbors gave the `min`; record the corresponding operation and move accordingly.
7. Reverse the operations list and return.

### Worked Example (Dry Run)
`word1 = "horse"`, `word2 = "ros"`. dp table is the same as standard edit distance (answer = 3).

Trace back from `dp[5][3]=3`:
- `(5,3)`: `e≠s`, `dp[4][3]=2` is min of neighbors → "delete e", move `(4,3)`.
- `(4,3)`: `d≠s`, `dp[3][2]=2` is min → "delete d", move `(3,2)`.
- `(3,2)`: `r≠o`, `dp[2][1]=2` → "replace r with o", move `(2,1)`.
- `(2,1)`: `o≠r`, `dp[1][0]=1` → "replace o with r", move `(1,0)`.
- `(1,0)`: "delete h", move `(0,0)`.

Reversed: `replace h→r, replace o→o(no), delete d, delete e`. Actual: replace h→r, no-op o, delete r, delete e → `["replace h by r", "delete r", "delete d", "delete e"]`. Answer: 3 operations.

### Code
```python
def edit_distance_with_ops(word1: str, word2: str) -> tuple:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    # Trace back to collect operations
    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}'")
            i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"Delete '{word1[i-1]}'")
            i -= 1
        else:
            ops.append(f"Insert '{word2[j-1]}'")
            j -= 1
    ops.reverse()
    return dp[m][n], ops
```

### Complexity
- Time: O(m×n) to fill table + O(m+n) to trace back.
- Space: O(m×n) for the dp table.

### Common Mistakes & Edge Cases
- Forgetting to reverse the operations list after trace-back.
- Choosing the wrong neighbor when two have equal values (any valid path is fine).
- Insert vs delete direction: inserting `word2[j-1]` advances `j`, deleting `word1[i-1]` advances `i`.
- Both strings empty → 0 operations, empty list.

---

## 2. Distinct Subsequences II (LC #940) — Hard

### Problem Explanation
Given a string `s`, count the number of distinct non-empty subsequences of `s`. Two subsequences are different if they differ in at least one character's selection. The answer can be very large, so return it modulo `10^9 + 7`. For example, `"abc"` has 7 distinct non-empty subsequences: `a, b, c, ab, ac, bc, abc`.

### State Definition
`dp[i]` = number of distinct non-empty subsequences of `s[:i]`. We track an auxiliary array `last[c]` = the index of the most recent occurrence of character `c`.

### Recurrence Relation
```
dp[i] = 2 * dp[i-1]                          (take or skip s[i-1])
if s[i-1] was seen before at position j:
    dp[i] -= dp[j-1]                          (subtract duplicates)
```
Each new character doubles the count (old subsequences + old subsequences with `s[i-1]` appended), but subsequences ending at the previous occurrence of the same character are counted twice.

### Base Cases
- `dp[0] = 1` (the empty subsequence, used as a multiplier).
- Answer is `dp[n] - 1` (subtract the empty subsequence).

### Intuition
When we add a new character `c`, every existing subsequence can either include or exclude it, doubling the count. But if `c` appeared before at index `j`, the subsequences that existed before `j` and had `c` appended are now counted twice (once from the old occurrence, once from the new). We subtract `dp[j-1]` to fix this.

### Step-by-Step Procedure
1. Let `n = len(s)`, `MOD = 10^9 + 7`.
2. Initialize `dp = [0] * (n + 1)`, `dp[0] = 1`.
3. Maintain `last = {}` mapping character to last index.
4. For `i` from 1 to `n`:
5. `dp[i] = 2 * dp[i-1] % MOD`.
6. If `s[i-1]` in `last`, subtract `dp[last[s[i-1]] - 1]`.
7. Update `last[s[i-1]] = i`.
8. Return `(dp[n] - 1) % MOD`.

### Worked Example (Dry Run)
`s = "aba"`, `MOD` large enough to ignore.

- `dp[0] = 1`, `last = {}`.
- `i=1`, `c='a'`: `dp[1] = 2*1 = 2`; `last` has no 'a' → `dp=[1,2]`, `last={'a':1}`.
- `i=2`, `c='b'`: `dp[2] = 2*2 = 4`; no 'b' in last → `dp=[1,2,4]`, `last={'a':1,'b':2}`.
- `i=3`, `c='a'`: `dp[3] = 2*4 = 8`; 'a' at index 1 → subtract `dp[0]=1` → `dp[3]=7`. `last={'a':3,'b':2}`.

Answer: `dp[3] - 1 = 6`. Non-empty subsequences: `a, b, ab, aa, ba, aba`.

### Code
```python
def distinct_subseq_ii(s: str) -> int:
    MOD = 10 ** 9 + 7
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1  # empty subsequence as multiplier
    last = {}  # last index (1-based) where each character appeared
    for i in range(1, n + 1):
        c = s[i - 1]
        dp[i] = (2 * dp[i - 1]) % MOD
        if c in last:
            # Subtract subsequences that were already counted at the previous 'c'
            dp[i] = (dp[i] - dp[last[c] - 1]) % MOD
        last[c] = i
    return (dp[n] - 1) % MOD  # subtract empty subsequence
```

### Complexity
- Time: O(n)
- Space: O(n) for dp (or O(1) if we only keep the last value and a dict).

### Common Mistakes & Edge Cases
- Forgetting to subtract the empty subsequence at the end (`dp[n] - 1`).
- Negative modulo: always use `% MOD` after subtraction.
- All same characters `"aaaa"`: each new `a` adds 0 new subsequences (all duplicates), answer = 1 (just `"a"`).
- Single character: answer = 1.
- Empty string: answer = 0.

---

## 3. Interleaving String (LC #97) — Medium

### Problem Explanation
Given three strings `s1`, `s2`, and `s3`, determine if `s3` is formed by interleaving `s1` and `s2`. An interleaving uses all characters of `s1` and `s2` in their original relative order to form `s3`. For example, `s1 = "aab"`, `s2 = "axy"`, `s3 = "aaxaby"` → True.

### State Definition
`dp[i][j]` = True if `s3[:i+j]` can be formed by interleaving `s1[:i]` and `s2[:j]`.

### Recurrence Relation
```
dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1])    (take from s1)
         or (dp[i][j-1] and s2[j-1] == s3[i+j-1])    (take from s2)
```
The last character of `s3[:i+j]` must come from either `s1[i-1]` or `s2[j-1]`, and the prefixes before that must also interleave.

### Base Cases
- `dp[0][0] = True` (two empty strings interleave to empty).
- `dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]` (only `s1` contributes).
- `dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]` (only `s2` contributes).

### Intuition
At each position in `s3`, we decide: did this character come from the next unused character in `s1` or `s2`? If we took from `s1`, the remaining problem is `s1[1:]` and `s2` forming `s3[1:]` — a smaller subproblem. The 2D table records all prefix-pair answers so we avoid re-exponential branching.

### Step-by-Step Procedure
1. If `len(s1) + len(s2) != len(s3)`, return False.
2. Create `(m+1)×(n+1)` boolean table.
3. Set `dp[0][0] = True`.
4. Fill column 0 (only `s1` contributing) and row 0 (only `s2` contributing).
5. For `i` from 1 to `m`, for `j` from 1 to `n`: compute `dp[i][j]` from the two predecessors.
6. Return `dp[m][n]`.

### Worked Example (Dry Run)
`s1 = "ab"`, `s2 = "cd"`, `s3 = "acbd"`.

```
     ""  c  d
""    T  F  F
a     T  F  F
b     F  F  F
```
- `dp[1][0]`: `s1[0]='a' == s3[0]='a'` → True.
- `dp[1][1]`: from `s1`: `dp[0][1]=F`; from `s2`: `dp[1][0]=T and s2[0]='c'==s3[1]='c'` → True.
- `dp[1][2]`: from `s1`: `dp[0][2]=F`; from `s2`: `dp[1][1]=T and s2[1]='d'==s3[2]='b'` → False.
- `dp[2][1]`: from `s1`: `dp[1][1]=T and s1[1]='b'==s3[2]='b'` → True.
- `dp[2][2]`: from `s2`: `dp[2][1]=T and s2[1]='d'==s3[3]='d'` → True.

Answer: True. `s3 = "acbd"` = interleave `"ab"` and `"cd"`.

### Code
```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            take_s1 = dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]
            take_s2 = dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]
            dp[i][j] = take_s1 or take_s2
    return dp[m][n]
```

### Complexity
- Time: O(m×n)
- Space: O(m×n) (can optimize to O(n) with a 1D array).

### Common Mistakes & Edge Cases
- Forgetting to check length mismatch upfront (`m + n != len(s3)`).
- Overlapping characters: `s1="aab"`, `s2="axy"`, `s3="aaxaby"` requires tracking both paths.
- Both `s1` and `s2` have the same next character as `s3` — both paths must be tried.
- Empty strings: `s1=""`, `s2=""`, `s3=""` → True.
- One string empty: reduces to checking if the other equals `s3`.

---

## 4. Is Subsequence (LC #392) — Easy

### Problem Explanation
Given two strings `s` and `t`, determine if `s` is a subsequence of `t`. A subsequence maintains relative order but skips characters. Input: two strings; output: a boolean. For example, `s = "abc"`, `t = "ahbgdc"` → True.

### State Definition
`dp[i][j]` = length of the longest common subsequence of `s[:i]` and `t[:j]`. Alternatively, a simpler greedy/two-pointer approach works.

### Recurrence Relation (DP version)
```
if s[i-1] == t[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
else:                 dp[i][j] = dp[i][j-1]
```
Note: we can only skip in `t` (not in `s`), so there is no `dp[i-1][j]` term.

### Base Cases
- `dp[0][j] = 0` for all j (empty `s` has LCS 0 with anything).
- `dp[i][0] = 0` for all i (empty `t` cannot match non-empty `s`).
- Answer is `dp[m][n] == m` (all characters of `s` matched).

### Intuition
This is a simplified LCS where we only care about matching `s` within `t` (one direction). The greedy approach works: scan `t` and greedily match the next needed character of `s`. DP formalizes this: `dp[i][j]` tracks how many characters of `s[:i]` are matched using `t[:j]`.

### Step-by-Step Procedure
1. Let `m = len(s)`, `n = len(t)`.
2. Create `(m+1)×(n+1)` table of zeros.
3. For `i` from 1 to `m`, for `j` from 1 to `n`:
4. If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`.
5. Else: `dp[i][j] = dp[i][j-1]`.
6. Return `dp[m][n] == m`.

### Worked Example (Dry Run)
`s = "abc"`, `t = "ahbgdc"`.

```
     ""  a  h  b  g  d  c
""    0  0  0  0  0  0  0
a     0  1  1  1  1  1  1
b     0  1  1  2  2  2  2
c     0  1  1  2  2  2  3
```
`dp[3][6] = 3 == len(s)` → True.

### Code
```python
def is_subsequence(s: str, t: str) -> bool:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = dp[i][j - 1]
    return dp[m][n] == m
```

### Complexity
- Time: O(m×n)
- Space: O(m×n) (greedy two-pointer is O(1) space and O(n) time).

### Common Mistakes & Edge Cases
- Empty `s` is a subsequence of any `t` (return True).
- `s` longer than `t` → always False.
- Repeated characters: greedy approach still works because we always match the earliest possible position.
- The DP is equivalent to "does `s` appear as a subsequence" — not the same as substring.

---

## 5. Longest Repeating Subsequence (LC #647 variant) — Medium

### Problem Explanation
Given a string `s`, find the length of the longest subsequence that appears at least twice in `s`, where the two occurrences use different character indices (but may have the same character value). For example, `s = "aab"` → answer is 1 (the two `a`s at different indices form `"a"`, and `"aa"` uses the same index twice which is not allowed in both subsequences).

### State Definition
`dp[i][j]` = length of the longest repeating subsequence using `s[:i]` and `s[:j]` where we require `i ≠ j`.

### Recurrence Relation
```
if s[i-1] == s[j-1] and i != j:  dp[i][j] = dp[i-1][j-1] + 1
else:                             dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
Same as LCS but comparing `s` with itself, with the constraint that matching positions must differ (`i ≠ j`).

### Base Cases
- `dp[0][j] = 0`, `dp[i][0] = 0` (empty prefix has no repeating subsequence).

### Intuition
This is LCS of `s` with itself, but we disallow using the same index twice. The `i ≠ j` check in the match condition ensures the two subsequences come from different positions. Since the string is the same, the recurrence is symmetric.

### Step-by-Step Procedure
1. Let `n = len(s)`.
2. Create `(n+1)×(n+1)` table of zeros.
3. For `i` from 1 to `n`, for `j` from 1 to `n`:
4. If `s[i-1] == s[j-1]` and `i != j`: `dp[i][j] = dp[i-1][j-1] + 1`.
5. Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
6. Return `dp[n][n]`.

### Worked Example (Dry Run)
`s = "aab"`.

```
     ""  a  a  b
""    0  0  0  0
a     0  0  1  1
a     0  1  0  1
b     0  1  1  1
```
- `dp[1][2]`: `s[0]='a'==s[1]='a'` and `1≠2` → `dp[0][1]+1 = 1`.
- `dp[2][1]`: `s[1]='a'==s[0]='a'` and `2≠1` → `dp[1][0]+1 = 1`.
- `dp[3][3]`: `s[2]='b'==s[2]='b'` but `3==3` → skip, `max(dp[2][3], dp[3][2]) = 1`.

Answer: 1. The longest repeating subsequence is `"a"` (using different indices).

### Code
```python
def longest_repeating_subsequence(s: str) -> int:
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i - 1] == s[j - 1] and i != j:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][n]
```

### Complexity
- Time: O(n²)
- Space: O(n²)

### Common Mistakes & Edge Cases
- Forgetting the `i != j` constraint — without it, LCS of a string with itself is just `n`.
- All same characters `"aaaa"`: answer is `n-1` (use all but one index twice).
- All unique characters: answer is 1 if any character repeats (wait — no repeats means answer is 0).
- Single character: answer is 0 (cannot pick the same index twice).

---

## 6. Longest Palindromic Substring (LC #5) — Medium

### Problem Explanation
Given a string `s`, find the longest substring that is a palindrome. Return the substring itself (or its length). Unlike Longest Palindromic *Subsequence*, this requires contiguous characters. For example, `s = "babad"` → `"bab"` or `"aba"`.

### State Definition
`dp[i][j]` = True if `s[i..j]` (inclusive) is a palindrome.

### Recurrence Relation
```
dp[i][j] = True  if  s[i] == s[j]  and  dp[i+1][j-1] is True
```
Base: single characters and two-character palindromes are handled directly.

### Base Cases
- `dp[i][i] = True` for all `i` (single character is a palindrome).
- `dp[i][i+1] = (s[i] == s[i+1])` (two-character palindromes).
- `dp[i][j] = False` for `j < i`.

### Intuition
A substring `s[i..j]` is a palindrome if its outer characters match and the inner substring `s[i+1..j-1]` is also a palindrome. We fill by increasing substring length: length 1 (all True), length 2 (check pairs), then length 3+ (outer match AND inner palindrome). The global answer tracks the longest True cell.

### Step-by-Step Procedure
1. If `s` is empty, return `""`.
2. Let `n = len(s)`, initialize `dp = [[False]*n for _ in range(n)]`.
3. Set `start = 0`, `max_len = 1`.
4. Fill all `dp[i][i] = True`.
5. For length 2: `dp[i][i+1] = (s[i] == s[i+1])`.
6. For length from 3 to `n`: for each `i`, set `j = i+length-1`, `dp[i][j] = (s[i]==s[j] and dp[i+1][j-1])`.
7. Update `start` and `max_len` whenever a longer palindrome is found.
8. Return `s[start:start+max_len]`.

### Worked Example (Dry Run)
`s = "babad"`, `n = 5`.

```
     b   a   b   a   d
b    T   F   T   F   F
a    -   T   F   T   F
b    -   -   T   F   F
a    -   -   -   T   F
d    -   -   -   -   T
```
- Length 1: all True.
- Length 2: `dp[0][1]='b'!='a'`=F, `dp[1][2]='a'!='b'`=F, `dp[2][3]='b'!='a'`=F, `dp[3][4]='a'!='d'`=F.
- Length 3: `dp[0][2]`: `b==b and dp[1][1]=T` → T (len 3, start 0). `dp[1][3]`: `a==a and dp[2][2]=T` → T (len 3, start 1).
- Length 4: all False.
- Length 5: `dp[0][4]`: `b!=d` → F.

Longest: `"bab"` (length 3, start 0).

### Code
```python
def longest_palindrome_substring(s: str) -> str:
    n = len(s)
    if n < 2:
        return s
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    for i in range(n):
        dp[i][i] = True  # single chars are palindromes
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, max_len = i, 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length
    return s[start:start + max_len]
```

### Complexity
- Time: O(n²)
- Space: O(n²)

### Common Mistakes & Edge Cases
- Off-by-one in the inner diagonal: `dp[i+1][j-1]` must already be computed; fill by increasing length.
- Single character input → return that character.
- All same characters → return the entire string.
- Two different characters → return either one (length 1).
- Empty string → return `""`.

---

## 7. Count of Palindromic Substrings (LC #647) — Medium

### Problem Explanation
Given a string `s`, count the number of substrings that are palindromes. Every single character is a palindrome. For example, `s = "aaa"` → 6 (`"a"`, `"a"`, `"a"`, `"aa"`, `"aa"`, `"aaa"`).

### State Definition
`dp[i][j]` = True if `s[i..j]` is a palindrome. Same table as Longest Palindromic Substring.

### Recurrence Relation
```
dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]
```
Count increments by 1 every time `dp[i][j]` becomes True.

### Base Cases
- `dp[i][i] = True` (n single-character palindromes).
- Two-character: `dp[i][i+1] = (s[i] == s[i+1])`.

### Intuition
Identical to the longest palindromic substring DP, but instead of tracking the maximum, we increment a counter each time a cell is set to True. Every True cell represents one palindromic substring.

### Step-by-Step Procedure
1. Let `n = len(s)`, `count = 0`.
2. Create `dp = [[False]*n for _ in range(n)]`.
3. For `i` from 0 to `n-1`: `dp[i][i] = True`; `count += 1`.
4. For `i` from 0 to `n-2`: if `s[i]==s[i+1]`, `dp[i][i+1]=True`; `count += 1`.
5. For length from 3 to `n`: for each `i`, `j=i+length-1`: if `s[i]==s[j] and dp[i+1][j-1]`: `dp[i][j]=True`; `count += 1`.
6. Return `count`.

### Worked Example (Dry Run)
`s = "aaa"`.

- Length 1: `dp[0][0]=T, dp[1][1]=T, dp[2][2]=T` → count = 3.
- Length 2: `dp[0][1]`: `a==a` → T (count=4); `dp[1][2]`: `a==a` → T (count=5).
- Length 3: `dp[0][2]`: `a==a and dp[1][1]=T` → T (count=6).

Answer: 6.

### Code
```python
def count_palindromic_substrings(s: str) -> int:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    count = 0
    for i in range(n):
        dp[i][i] = True
        count += 1
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            count += 1
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                count += 1
    return count
```

### Complexity
- Time: O(n²)
- Space: O(n²)

### Common Mistakes & Edge Cases
- Forgetting to count single characters (every one is a palindrome).
- `n = 1` → answer is 1.
- All same characters `"aaaa"` → answer is `n*(n+1)/2 = 10`.
- Two-character palindromes require `s[i] == s[i+1]` check before accessing diagonal.

---

## 8. Palindrome Partitioning (LC #131) — Medium

### Problem Explanation
Given a string `s`, partition it such that every substring of each partition is a palindrome. Return all possible palindrome partitionings. For example, `s = "aab"` → `[["a","a","b"], ["aa","b"]]`.

### State Definition
`is_pal[i][j]` = True if `s[i..j]` is a palindrome (precomputed). `dfs(start)` = list of all valid partitions of `s[start:]`.

### Recurrence Relation
```
For each end in range(start, n):
    if is_pal[start][end]:
        for each partition in dfs(end + 1):
            result.append([s[start:end+1]] + partition)
```
At each position, try every possible palindromic prefix, then recursively partition the rest.

### Base Cases
- `dfs(n) = [[]]` (one way to partition the empty string: no substrings).
- `is_pal[i][i] = True` for all `i`.

### Intuition
This is a backtracking problem with a DP precomputation. We first compute which substrings are palindromes (O(n²)), then use DFS: at each position, try every palindromic substring starting there, and recurse on the remainder. The palindrome check prevents invalid splits.

### Step-by-Step Procedure
1. Precompute `is_pal[i][j]` for all substrings (same as Count of Palindromic Substrings).
2. Define `dfs(start)` that returns all partitions of `s[start:]`.
3. If `start == n`, return `[[]]`.
4. For `end` from `start` to `n-1`: if `is_pal[start][end]`, recurse on `end+1`.
5. Prepend `s[start:end+1]` to each returned partition.
6. Return all collected partitions.

### Worked Example (Dry Run)
`s = "aab"`.

`is_pal`: `dp[0][0]=T, dp[1][1]=T, dp[2][2]=T, dp[0][1]=(a==a)=T, dp[1][2]=(a!=b)=F, dp[0][2]=(a!=b)=F`.

DFS from index 0:
- Try `s[0:1]="a"` (pal): recurse from 1.
  - Try `s[1:2]="a"` (pal): recurse from 2.
    - Try `s[2:3]="b"` (pal): recurse from 3 → [[]]. Result: `[["a","a","b"]]`.
  - `s[1:3]="ab"` (not pal): skip.
  - Result from 1: `[["a","a","b"]]`. Total: `[["a","a","b"]]`.
- Try `s[0:2]="aa"` (pal): recurse from 2.
  - Try `s[2:3]="b"` (pal): recurse from 3 → [[]]. Result: `[["aa","b"]]`.
  - Total: `[["aa","b"]]`.
- `s[0:3]="aab"` (not pal): skip.

Final: `[["a","a","b"], ["aa","b"]]`.

### Code
```python
def partition(s: str) -> list:
    n = len(s)
    # Precompute palindrome table
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i + 1][j - 1])

    result = []
    def dfs(start: int):
        if start == n:
            result.append([]); return
        for end in range(start, n):
            if is_pal[start][end]:
                for rest in dfs(end + 1):
                    result.append([s[start:end + 1]] + rest)

    dfs(0)
    return result
```

### Complexity
- Time: O(n × 2^n) in the worst case (exponential partitions, each O(n) to copy).
- Space: O(n²) for `is_pal` + O(n) recursion depth.

### Common Mistakes & Edge Cases
- Forgetting the palindrome precomputation — checking palindromes on-the-fly is O(n) per check, making the DFS much slower.
- Base case: returning `[[]]` (one empty partition), not `[]` (zero partitions).
- Single character: `[["a"]]`.
- All same characters `"aaa"`: `[["a","a","a"],["a","aa"],["aa","a"],["aaa"]]`.

---

## 9. Palindrome Partitioning II (LC #132) — Hard

### Problem Explanation
Given a string `s`, find the minimum number of cuts needed to partition `s` so that every substring is a palindrome. For example, `s = "aab"` → 1 cut (split as `"aa" | "b"`).

### State Definition
`dp[i]` = minimum cuts to partition `s[:i]` into palindromes. `is_pal[i][j]` = True if `s[i..j]` is a palindrome.

### Recurrence Relation
```
dp[i] = min over j in [0, i-1]:  dp[j] + 1   if is_pal[j+1][i] is True
       or 0                        if s[0..i] itself is a palindrome
```
Try every possible last cut position; if the substring after the last cut is a palindrome, the cost is `dp[j] + 1`.

### Base Cases
- `dp[-1] = -1` (convention: zero cuts for an empty prefix, so `dp[j] + 1` starts at 0 for `j=-1`).
- `dp[i] = 0` if `s[0..i]` is a palindrome.

### Intuition
For each prefix ending at `i`, we try every possible "last palindrome" `s[j+1..i]`. If that substring is a palindrome, we need `dp[j]` cuts for `s[:j+1]` plus one more cut to separate it. We take the minimum over all valid `j`. Precomputing `is_pal` in O(n²) avoids redundant palindrome checks.

### Step-by-Step Procedure
1. Precompute `is_pal[i][j]` for all substrings.
2. Create `dp` of size `n`, initialize with `i` (worst case: cut between every character).
3. If `s[0..i]` is a palindrome, `dp[i] = 0`.
4. For `i` from 1 to `n-1`:
5. For `j` from 0 to `i-1`: if `is_pal[j+1][i]`, `dp[i] = min(dp[i], dp[j] + 1)`.
6. Return `dp[n-1]`.

### Worked Example (Dry Run)
`s = "aab"`. `is_pal[0][0]=T, [1][1]=T, [2][2]=T, [0][1]=T, [1][2]=F, [0][2]=F`.

- `dp = [0, 1, 2]` (initial worst case: 0, 1, 2 cuts).
- `dp[0] = 0` (s[0..0]="a" is pal).
- `i=1`: `s[0..1]="aa"` is pal → `dp[1] = 0`.
- `i=2`: `s[0..2]="aab"` is not pal. Try `j=0`: `is_pal[1][2]=F` → skip. Try `j=1`: `is_pal[2][2]=T` → `dp[2] = min(2, dp[1]+1) = min(2, 1) = 1`.

Answer: 1 cut.

### Code
```python
def min_cut(s: str) -> int:
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i + 1][j - 1])
    dp = list(range(n))  # worst case: cut between every char
    for i in range(1, n):
        if is_pal[0][i]:
            dp[i] = 0
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                dp[i] = min(dp[i], dp[j - 1] + 1)
    return dp[n - 1]
```

### Complexity
- Time: O(n²) for palindrome precomputation + O(n²) for dp = O(n²).
- Space: O(n²) for `is_pal` (can reduce to O(n) with expand-around-center).

### Common Mistakes & Edge Cases
- `n = 0` → 0 cuts (guard with `if n <= 1: return 0`).
- Already a palindrome → 0 cuts.
- All unique characters → `n-1` cuts.
- The `dp` initial value must be `i` (max cuts), not `inf`, since `dp[j]+1` must not overflow.

---

## 10. Palindrome Partitioning III (LC #1278) — Hard

### Problem Explanation
Given a string `s`, an integer `k`, you need to partition `s` into exactly `k` substrings. In one operation you can change any character to any other character. Find the minimum number of changes needed so that every substring in the partition is a palindrome.

### State Definition
`cost[i][j]` = minimum changes to make `s[i..j]` a palindrome. `dp[i][k]` = minimum changes to partition `s[:i]` into `k` palindromic substrings.

### Recurrence Relation
```
cost[i][j] = number of mismatched pairs in s[i..j]
dp[i][p] = min over j in [p-1, i-1]:  dp[j][p-1] + cost[j+1][i]
```
Try every split point for the p-th (last) substring; pay the cost to make it a palindrome plus the optimal cost for the remaining `p-1` partitions.

### Base Cases
- `dp[0][0] = 0` (empty string, zero partitions, zero cost).
- `dp[i][1] = cost[0][i-1]` (one partition = make the whole prefix a palindrome).
- `cost[i][j] = 0` when `i >= j` (single char or empty is already a palindrome).

### Intuition
First precompute the cost of making every substring a palindrome. Then DP over (prefix length, number of partitions): for each `(i, p)`, try every possible last partition boundary `j`, paying `cost[j+1][i]` to make the last substring a palindrome, plus `dp[j][p-1]` for the rest.

### Step-by-Step Procedure
1. Precompute `cost[i][j]` for all substrings: count mismatched pairs `(i,j)`, `(i+1,j-1)`, etc.
2. Create `dp[i][p]` for `i` in `0..n`, `p` in `0..k`, fill with `inf`.
3. Set `dp[0][0] = 0`.
4. For `p` from 1 to `k`:
5. For `i` from `p` to `n`:
6. For `j` from `p-1` to `i-1`: `dp[i][p] = min(dp[i][p], dp[j][p-1] + cost[j][i-1])`.
7. Return `dp[n][k]`.

### Worked Example (Dry Run)
`s = "abc"`, `k = 2`.

`cost[0][0]=0, cost[1][1]=0, cost[2][2]=0, cost[0][1]=1(a≠b), cost[1][2]=1(b≠c), cost[0][2]=2(a≠c)`.

`dp[0][0]=0`. For `p=1`: `dp[1][1]=cost[0][0]=0, dp[2][1]=cost[0][1]=1, dp[3][1]=cost[0][2]=2`.
For `p=2`:
- `dp[2][2]`: `j=1` → `dp[1][1]+cost[1][1]=0+0=0`. Answer so far: 0.
- `dp[3][2]`: `j=1` → `dp[1][1]+cost[1][2]=0+1=1`; `j=2` → `dp[2][1]+cost[2][2]=1+0=1`. Min = 1.

Answer: `dp[3][2] = 1` (change `b` to `a` → `"aa" | "c"`, or change `b` to `c` → `"a" | "cc"`).

### Code
```python
def palindrome_partition(s: str, k: int) -> int:
    n = len(s)
    # Precompute cost to make s[i..j] a palindrome
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = cost[i + 1][j - 1] + (0 if s[i] == s[j] else 1)
    INF = float('inf')
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for p in range(1, k + 1):
        for i in range(p, n + 1):
            for j in range(p - 1, i):
                dp[i][p] = min(dp[i][p], dp[j][p - 1] + cost[j][i - 1])
    return dp[n][k]
```

### Complexity
- Time: O(n²) for cost + O(k × n²) for dp.
- Space: O(n² + k×n).

### Common Mistakes & Edge Cases
- `k >= n` → 0 changes (each character is its own palindrome).
- `k = 1` → cost to make the whole string a palindrome.
- `s` already a palindrome and `k=1` → 0.
- `cost` precomputation: when length is 2, `cost[i][i+1] = (0 if s[i]==s[i+1] else 1)`.

---

## 11. Minimum Insertions to Make a String Palindrome (LC #1312) — Medium

### Problem Explanation
Given a string `s`, find the minimum number of insertions needed at any position to make `s` a palindrome. For example, `s = "zzazz"` → 0 (already a palindrome); `s = "mbadm"` → 2.

### State Definition
`dp[i][j]` = minimum insertions to make `s[i..j]` a palindrome.

### Recurrence Relation
```
if s[i] == s[j]:  dp[i][j] = dp[i+1][j-1]
else:             dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])
```
If outer characters match, no insertion needed; otherwise insert one character to match the other end.

### Base Cases
- `dp[i][i] = 0` (single character is already a palindrome).
- `dp[i][i+1] = 0 if s[i]==s[i+1] else 1`.

### Intuition
This is the complement of Longest Palindromic Subsequence: `min_insertions = n - LPS_length`. The intuition is that characters not in the LPS need to be paired by insertion. The interval DP formulation works by expanding from single characters outward.

### Step-by-Step Procedure
1. Let `n = len(s)`.
2. Create `n×n` table, fill with 0.
3. For `i` from `n-1` down to 0:
4. For `j` from `i+1` to `n-1`:
5. If `s[i]==s[j]`: `dp[i][j] = dp[i+1][j-1]`.
6. Else: `dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])`.
7. Return `dp[0][n-1]`.

### Worked Example (Dry Run)
`s = "mbadm"`, `n = 5`.

```
     m   b   a   d   m
m    0   1   2   2   0
b    -   0   1   1   2
a    -   -   0   1   2
d    -   -   -   0   1
m    -   -   -   -   0
```
- Diagonal: all 0.
- `dp[0][1]`: `m≠b` → `1+min(dp[1][1], dp[0][0]) = 1`.
- `dp[0][2]`: `m≠a` → `1+min(dp[1][2], dp[0][1]) = 1+1 = 2`.
- `dp[0][3]`: `m≠d` → `1+min(dp[1][3], dp[0][2]) = 1+1 = 2`.
- `dp[0][4]`: `m==m` → `dp[1][3] = 1`. Answer: 1? Let me recheck.
- `dp[1][4]`: `b≠m` → `1+min(dp[2][4], dp[1][3]) = 1+1 = 2`.
- `dp[0][4]`: `m==m` → `dp[1][3] = 1`.

Hmm, `"mbadm"` needs 2 insertions (`d` and `a` to make `"mdbadm"` → not quite). Let me recalculate: `"mbadm"` → insert `d` before `m` → `"dmbadm"`, insert `b` → `"dbmadm"` → no. Actually the answer should be 2: insert `a` after first `m` and `d` → `"madadm"` → wait. The correct answer is indeed 2 (`"mdbadm"` is not right). Let me trace more carefully.

`dp[1][3]`: `s[1]='b', s[3]='d'` → `1+min(dp[2][3], dp[1][2]) = 1+min(1,1) = 2`. Then `dp[0][4] = dp[1][3] = 2`. Answer: 2.

### Code
```python
def min_insertions(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

### Complexity
- Time: O(n²)
- Space: O(n²)

### Common Mistakes & Edge Cases
- Empty string → 0 insertions.
- Already a palindrome → 0.
- All different characters → `n-1` insertions.
- `dp[i+1][j-1]` when `j = i+1` reads `dp[i+1][i]` which is 0 (correct, base case).

---

## 12. Minimum Deletions to Make a String Palindrome — Medium

### Problem Explanation
Given a string `s`, find the minimum number of deletions needed to make `s` a palindrome. For example, `s = "aebcbda"` → 2 (delete `e` and `d`).

### State Definition
`dp[i][j]` = minimum deletions to make `s[i..j]` a palindrome.

### Recurrence Relation
```
if s[i] == s[j]:  dp[i][j] = dp[i+1][j-1]
else:             dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])
```
If outer characters match, no deletion needed; otherwise delete one character (whichever side gives the minimum).

### Base Cases
- `dp[i][i] = 0` (single character).
- `dp[i][i+1] = 0 if s[i]==s[i+1] else 1`.

### Intuition
Equivalent to `n - LPS_length`: keep the longest palindromic subsequence and delete everything else. The DP formulation is identical to Minimum Insertions, but conceptually we are deleting mismatched characters instead of inserting matching ones.

### Step-by-Step Procedure
1. Let `n = len(s)`.
2. Create `n×n` table, fill with 0.
3. For `i` from `n-1` down to 0:
4. For `j` from `i+1` to `n-1`:
5. If `s[i]==s[j]`: `dp[i][j] = dp[i+1][j-1]`.
6. Else: `dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])`.
7. Return `dp[0][n-1]`.

### Worked Example (Dry Run)
`s = "abcda"`, `n = 5`.

- `dp[0][4]`: `a==a` → `dp[1][3]`.
- `dp[1][3]`: `b≠d` → `1+min(dp[2][3], dp[1][2])`.
- `dp[2][3]`: `c≠d` → `1+min(0,0) = 1`. `dp[1][2]`: `b≠c` → `1`.
- `dp[1][3] = 1+1 = 2`. `dp[0][4] = 2`.

Answer: 2 deletions (delete `b` and `d` → `"aca"`). Or `5 - LPS("abcda") = 5 - 3 = 2`.

### Code
```python
def min_deletions(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

### Complexity
- Time: O(n²)
- Space: O(n²)

### Common Mistakes & Edge Cases
- Empty string → 0.
- Already a palindrome → 0.
- All unique characters → `n-1` deletions.
- Same recurrence as Minimum Insertions — the answer is `n - LPS` in both cases.

---

## 13. Minimum Deletions and Insertions to Transform One String into Another (LC #1546) — Medium

### Problem Explanation
Given two strings `s1` and `s2`, find the minimum number of deletions from `s1` and insertions into `s2` to make them equal. This is equivalent to finding the edit distance with only delete and insert operations (no replace). For example, `s1 = "heap"`, `s2 = "pea"` → 2 deletions (remove `h` and `p`) + 1 insertion (insert `p`) = 3.

### State Definition
`dp[i][j]` = minimum operations (deletes + inserts) to transform `s1[:i]` into `s2[:j]`.

### Recurrence Relation
```
if s1[i-1] == s2[j-1]:  dp[i][j] = dp[i-1][j-1]
else:                     dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1])
```
`dp[i-1][j]` = delete from `s1`, `dp[i][j-1]` = insert into `s1`.

### Base Cases
- `dp[0][j] = j` (j insertions to build `s2[:j]`).
- `dp[i][0] = i` (i deletions to empty `s1[:i]`).

### Intuition
Without the replace operation, the edit distance only has two choices per mismatch: delete a character from `s1` or insert a character matching `s2`. The LCS length connects everything: `deletes = len(s1) - LCS`, `inserts = len(s2) - LCS`.

### Step-by-Step Procedure
1. Build `(m+1)×(n+1)` table.
2. Fill base cases: row 0 with `0..n`, column 0 with `0..m`.
3. For each cell: if characters match, copy diagonal; else `1 + min(above, left)`.
4. Return `dp[m][n]`.

### Worked Example (Dry Run)
`s1 = "heap"`, `s2 = "pea"`.

```
     ""  p  e  a
""    0  1  2  3
h     1  2  3  4
e     2  3  2  3
a     3  4  3  2
p     4  3  4  3
```
- `dp[1][1]`: `h≠p` → `1+min(1,1) = 2`.
- `dp[2][2]`: `e==e` → `dp[1][1] = 2`. Hmm wait: `dp[1][1]=2`, but let me recheck.
- `dp[2][2]`: `s1[1]='e', s2[1]='e'` → `dp[1][1] = 2`.
- `dp[3][3]`: `s1[2]='a', s2[2]='a'` → `dp[2][2] = 2`.
- `dp[4][3]`: `s1[3]='p', s2[2]='a'` → `1+min(dp[3][3]=2, dp[4][2]=4) = 3`.

Answer: 3 (delete `h`, delete `e`, insert `a` — or equivalently, keep `ea` and transform `hp` → `p`).

### Code
```python
def min_operations(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

### Complexity
- Time: O(m×n)
- Space: O(m×n)

### Common Mistakes & Edge Cases
- Forgetting to handle the case when one string is empty (answer = length of the other).
- Confusing with full edit distance: no replace operation here.
- Equivalent to `len(s1) + len(s2) - 2 * LCS(s1, s2)`.
- Both strings empty → 0.

---

## 14. One Edit Distance (LC #161) — Medium

### Problem Explanation
Given two strings `s` and `t`, determine if they are exactly one edit distance apart. A single edit is an insert, delete, or replace operation. Return True if exactly one edit separates them, False otherwise. For example, `s = "ab"`, `t = "acb"` → True (one insert).

### State Definition
No full DP table needed. We scan both strings simultaneously and check for exactly one difference.

### Recurrence Relation
Scan linearly: if characters match, advance both pointers. On the first mismatch, try all three operations on the remainder and check if the rest matches exactly.

### Base Cases
- If lengths differ by more than 1 → False.
- If lengths are equal → check for exactly one character difference.
- If lengths differ by 1 → check if deleting one char from the longer makes them equal.

### Intuition
We do not need a full DP table because we only care about "exactly one" difference. After finding the first mismatch, we check if the remaining suffixes match exactly (for delete/insert, the longer string has one extra char; for replace, the lengths are equal and the rest must match).

### Step-by-Step Procedure
1. If `abs(len(s) - len(t)) > 1` → return False.
2. Ensure `s` is the shorter (or equal) string.
3. Scan for the first position `i` where `s[i] != t[i]`.
4. If no mismatch found, return `len(s) != len(t)` (exactly one edit = one is longer).
5. If lengths are equal: check if `s[i+1:] == t[i+1:]`.
6. If `t` is longer: check if `s[i:] == t[i+1:]`.

### Worked Example (Dry Run)
`s = "ab"`, `t = "acb"`. `len(s)=2, len(t)=3`, diff=1.

Scan: `s[0]='a'==t[0]='a'` → advance. `s[1]='b'!=t[1]='c'` → mismatch at `i=1`.
Check: `s[1:] = "b"`, `t[2:] = "b"` → equal → True.

Answer: True (insert `c` between `a` and `b`).

### Code
```python
def is_one_edit_distance(s: str, t: str) -> bool:
    m, n = len(s), len(t)
    if m > n:
        return is_one_edit_distance(t, s)  # ensure s is shorter
    if n - m > 1:
        return False
    for i in range(m):
        if s[i] != t[i]:
            if m == n:
                return s[i + 1:] == t[i + 1:]  # replace: rest must match
            else:
                return s[i:] == t[i + 1:]      # insert/delete: skip one in t
    return m != n  # all matched: exactly one edit only if lengths differ by 1
```

### Complexity
- Time: O(min(m,n))
- Space: O(1)

### Common Mistakes & Edge Cases
- Equal strings → False (zero edits, not one).
- Differ by more than 1 character → False.
- `s = ""`, `t = "a"` → True (one insert).
- `s = "a"`, `t = ""` → True (one delete).
- Multiple differences → False.

---

## 15. Longest Uncommon Subsequence I (LC #521) — Easy

### Problem Explanation
Given two strings `a` and `b`, find the length of the longest uncommon subsequence between them. An uncommon subsequence of `a` is a subsequence of `a` that is NOT a subsequence of `b`. If no such subsequence exists, return -1.

### State Definition
No DP needed. The answer is determined by a simple comparison.

### Recurrence Relation
If `a == b`: no uncommon subsequence exists → -1.
Otherwise: the longer of the two strings is itself an uncommon subsequence → `max(len(a), len(b))`.

### Base Cases
- Equal strings → -1.
- Different strings → `max(len(a), len(b))`.

### Intuition
If `a ≠ b`, then `a` (the full string) cannot be a subsequence of `b` (unless one is a subsequence of the other, but even then the longer string works). Specifically, if `a` is not a subsequence of `b`, then `a` itself is an uncommon subsequence of length `len(a)`. Otherwise `b` is not a subsequence of `a` and has length `len(b)`. The maximum is the answer.

### Step-by-Step Procedure
1. If `a == b` → return -1.
2. Return `max(len(a), len(b))`.

### Worked Example (Dry Run)
`a = "aaa"`, `b = "bbb"` → not equal → `max(3, 3) = 3`. The string `"aaa"` is not a subsequence of `"bbb"`.

`a = "abc"`, `b = "abc"` → equal → -1.

### Code
```python
def find_luas_length(a: str, b: str) -> int:
    if a == b:
        return -1
    return max(len(a), len(b))
```

### Complexity
- Time: O(n) for string comparison.
- Space: O(1).

### Common Mistakes & Edge Cases
- `a = ""`, `b = ""` → -1 (both empty and equal).
- `a = ""`, `b = "a"` → 1 (`"a"` is not a subsequence of `""`).
- `a = "abc"`, `b = "aebdc"` → -1 (`"abc"` IS a subsequence of `"aebdc"` and vice versa? No: `"aebdc"` is not a subsequence of `"abc"` because it's longer → answer is 5).

---

## 16. Longest Uncommon Subsequence II (LC #522) — Medium

### Problem Explanation
Given an array of strings `strs`, find the length of the longest uncommon subsequence. An uncommon subsequence of string `a` is a subsequence of `a` that is not a subsequence of any other string in the array. Return -1 if none exists. For example, `strs = ["aba","cdc","eae"]` → 3.

### State Definition
Sort strings by length descending. For each string (longest first), check if it is a subsequence of any other string in the array. The first string that is NOT a subsequence of any other is the answer.

### Recurrence Relation
Not a traditional DP recurrence. This is a sorting + subsequence-checking problem.

### Base Cases
- All strings equal → -1.
- Single string → its length.

### Intuition
The longest uncommon subsequence must be one of the input strings (if it exists as a subsequence of another, it's not uncommon). By checking from longest to shortest, the first string not a subsequence of any other is the answer.

### Step-by-Step Procedure
1. Sort `strs` by length descending.
2. For each string `strs[i]` (from longest):
3. Check if it is a subsequence of any `strs[j]` where `j ≠ i`.
4. If not a subsequence of any other, return `len(strs[i])`.
5. If no string qualifies, return -1.

### Worked Example (Dry Run)
`strs = ["aba", "cdc", "eae"]`. All length 3.
- `"aba"`: is it a subsequence of `"cdc"`? No (`a` not in `cdc`). → Answer: 3.

### Code
```python
def find_luas_length(strs: list) -> int:
    def is_subseq(a: str, b: str) -> bool:
        it = iter(b)
        return all(c in it for c in a)

    strs.sort(key=len, reverse=True)
    for i in range(len(strs)):
        is_uncommon = True
        for j in range(len(strs)):
            if i != j and is_subseq(strs[i], strs[j]):
                is_uncommon = False
                break
        if is_uncommon:
            return len(strs[i])
    return -1
```

### Complexity
- Time: O(n² × L) where n = number of strings, L = average length.
- Space: O(1).

### Common Mistakes & Edge Cases
- `["aaa","aaa","aa"]` → -1 (every string is a subsequence of `"aaa"`).
- `["a", "b", "c"]` → 1 (each is length 1 and not a subsequence of others? Actually `"a"` is not a subsequence of `"b"` → answer is 1).
- Single element array → return its length.

---

## 17. Valid Parentheses String (LC #678) — Medium

### Problem Explanation
Given a string `s` containing only `(`, `)`, and `*`, determine if the string is valid. The `*` can represent `(`, `)`, or an empty string. A valid string has every `(` matched by a later `)` and every `)` matched by an earlier `(`. For example, `s = "(*))"` → True.

### State Definition
`dp[i][j]` = True if `s[i..j]` can be a valid parentheses string. Alternatively, use two counters `lo` and `hi` (greedy).

### Recurrence Relation (DP)
```
if s[i] == '(' and s[j] == ')' and dp[i+1][j-1]:  dp[i][j] = True
if s[i] in ('(', '*') and s[j] in (')', '*') and dp[i+1][j-1]:  dp[i][j] = True
for k in range(i, j, 2): if dp[i][k] and dp[k+1][j]: dp[i][j] = True
```

### Base Cases
- `dp[i][i] = False` (single char can't be valid).
- `dp[i][j] = True` for `i > j`.
- Two chars: `dp[i][i+1] = True` if they form `()`, `(*`, `*)`, `**`, `*(`, etc.

### Intuition
The interval DP checks: can `s[i..j]` be split into two valid halves, or do the outer characters `s[i]` and `s[j]` form a matching pair (with `*` flexibility) around a valid interior? The two-counter greedy approach is O(n) but the DP is the classic formulation.

### Step-by-Step Procedure
1. Let `n = len(s)`.
2. Create `dp = [[False]*n for _ in range(n)]`.
3. For `i` from `n-1` down to 0:
4. For `j` from `i` to `n-1`:
5. Check all split points and outer-character matching.
6. Return `dp[0][n-1]`.

### Worked Example (Dry Run)
`s = "(*))"`. The DP would check:
- Length 2: `dp[0][1]`: `s[0]='('` and `s[1]='*'` → could be `()` → True.
- `dp[2][3]`: `s[2]=')'` and `s[3]=')'` → can't match → False.
- Length 3: `dp[0][2]`: split at 1 → `dp[0][1]=T and dp[2][2]=F` → F; `s[0]='('==s[2]=')'` and `dp[1][1]='*'` → True (`*` = empty).
- `dp[1][3]`: split at 2 → `dp[1][2]` (`"*)"` → True: `*`=`(`, `)`=`)`) and `dp[3][3]=F` → F; outer: `s[1]='*'` and `s[3]=')'` → `*`=`(`, `dp[2][2]=F` → F.
- Length 4: `dp[0][3]`: split at 1 → `dp[0][1]=T and dp[2][3]=F`; split at 2 → `dp[0][2]=T and dp[3][3]=F`. But outer: `s[0]='('` and `s[3]=')'` and `dp[1][2]`... `dp[1][2]` = `True` (`*` = `(`). So `dp[0][3] = True`.

Answer: True.

### Code
```python
def check_valid_string(s: str) -> bool:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = False  # single char never valid
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            length = j - i + 1
            if length == 2:
                dp[i][j] = (
                    (s[i] in '(*' and s[j] in '*)') or
                    (s[i] == '*' and s[j] == '*')
                )
            else:
                # outer chars could match
                if s[i] in '(*' and s[j] in '*)' and dp[i + 1][j - 1]:
                    dp[i][j] = True
                # split into two valid halves
                if not dp[i][j]:
                    for k in range(i, j, 2):
                        if dp[i][k] and dp[k + 1][j]:
                            dp[i][j] = True
                            break
    return dp[0][n - 1] if n > 0 else True
```

### Complexity
- Time: O(n³) for the interval DP.
- Space: O(n²).

### Common Mistakes & Edge Cases
- `s = ""` → True (empty string is valid).
- `s = "*"` → True (`*` = empty).
- `s = "("` → False.
- The greedy two-counter approach (`lo`, `hi`) runs in O(n) and is preferred for interviews.

---

## 18. Minimum Add to Make Parentheses Valid (LC #921) — Medium

### Problem Explanation
Given a string `s` of only `(` and `)`, find the minimum number of additions (insertions) needed to make the string valid. For example, `s = "(()("` → 2 (add one `)` and one `)`).

### State Definition
Two counters: `open_count` (unmatched `(`) and `close_count` (unmatched `)`). No DP table needed.

### Recurrence Relation
```
if c == '(':  open_count += 1
else:
    if open_count > 0:  open_count -= 1   (match with existing '(')
    else:               close_count += 1  (unmatched ')')
answer = open_count + close_count
```

### Base Cases
- Empty string → 0.
- Already valid → 0 (both counters end at 0).

### Intuition
Every unmatched `(` needs a `)` added, and every unmatched `)` needs a `(` added. The counters track how many of each remain after all possible matches. This is a classic stack/counting problem solvable in O(n) time, O(1) space.

### Step-by-Step Procedure
1. Initialize `open_count = 0`, `close_count = 0`.
2. For each character `c` in `s`:
3. If `c == '('`: increment `open_count`.
4. If `c == ')'`: if `open_count > 0`, decrement `open_count`; else increment `close_count`.
5. Return `open_count + close_count`.

### Worked Example (Dry Run)
`s = "(()("`.

- `c='('`: open=1, close=0.
- `c='('`: open=2, close=0.
- `c=')'`: open=1, close=0 (matched one `(`).
- `c='('`: open=2, close=0.

Answer: 2 (need 2 `)` to close the 2 unmatched `(`).

### Code
```python
def min_add_to_make_valid(s: str) -> int:
    open_count = 0
    close_count = 0
    for c in s:
        if c == '(':
            open_count += 1
        else:
            if open_count > 0:
                open_count -= 1
            else:
                close_count += 1
    return open_count + close_count
```

### Complexity
- Time: O(n)
- Space: O(1)

### Common Mistakes & Edge Cases
- Empty string → 0.
- All `(` → return count of `(`.
- All `)` → return count of `)`.
- Already valid `"()"` → 0.
- Mixed like `")("` → 2 (each needs its opposite).

---

## 19. Minimum Number of Swaps to Make String Balanced (LC #1249) — Medium

### Problem Explanation
Given a string `s` of only `(` and `)`, find the minimum number of swaps needed to make the string balanced. A swap exchanges any two characters. For example, `s = ")()()("` → 1 (swap first and last).

### State Definition
Track the balance (number of unmatched `(`). A negative balance means unmatched `)`.

### Recurrence Relation
```
balance += 1  if '('
balance -= 1  if ')'
max_depth = max(max_depth, -balance)  (when balance goes negative)
answer = (max_depth + 1) // 2
```

### Base Cases
- Already balanced → 0.
- The string is guaranteed to be balanceable (equal number of `(` and `)`).

### Intuition
Each swap can fix at most 2 unmatched `)` characters. The maximum depth of unmatched `)` (negative balance) tells us the worst point. The minimum swaps needed is `ceil(max_negative_depth / 2)`.

### Step-by-Step Procedure
1. Initialize `balance = 0`, `max_depth = 0`.
2. For each `c` in `s`:
3. Update balance: `+1` for `(`, `-1` for `)`.
4. If `balance < 0`, update `max_depth = max(max_depth, -balance)`.
5. Return `(max_depth + 1) // 2`.

### Worked Example (Dry Run)
`s = ")()()("`.

- `c=')'`: balance=-1, max_depth=1.
- `c='('`: balance=0.
- `c=')'`: balance=-1, max_depth=1.
- `c='('`: balance=0.
- `c=')'`: balance=-1, max_depth=1.
- `c='('`: balance=0.

max_depth = 1. Answer: `(1+1)//2 = 1`.

### Code
```python
def min_swaps(s: str) -> int:
    balance = 0
    max_depth = 0
    for c in s:
        balance += 1 if c == '(' else -1
        max_depth = max(max_depth, -balance)
    return (max_depth + 1) // 2
```

### Complexity
- Time: O(n)
- Space: O(1)

### Common Mistakes & Edge Cases
- Using `balance < 0` instead of tracking the maximum negative excursion.
- `"()()"` → 0 (already balanced).
- `"))))(((("` → 2 swaps (max depth = 4, `(4+1)//2 = 2`).
- The string always has equal `(` and `)` (guaranteed by problem).

---

## 20. Generate Parentheses (LC #22) — Medium

### Problem Explanation
Given `n` pairs of parentheses, generate all combinations of well-formed parentheses. For example, `n = 3` → `["((()))", "(()())", "(())()", "()(())", "()()()"]`.

### State Definition
`dp[i]` = list of all valid parentheses strings with `i` pairs. Alternatively, use backtracking with counters `open_count` and `close_count`.

### Recurrence Relation (DP)
```
dp[i] = union over all j in [0, i-1]:
    "(" + dp[j] + ")" + dp[i-1-j]
```
Split the `i` pairs: one pair wraps `j` pairs inside, and `i-1-j` pairs come after.

### Base Cases
- `dp[0] = [""]` (empty string).
- `dp[1] = ["()"]`.

### Intuition
Any valid parentheses string with `i` pairs has the form `(A)B` where `A` uses `j` pairs and `B` uses `i-1-j` pairs, for some `j` in `0..i-1`. The `(` and `)` form one matched pair, and `A` and `B` are independently valid. This decomposition generates all strings without duplicates.

### Step-by-Step Procedure
1. Initialize `dp = [[""], ["()"]]`.
2. For `i` from 2 to `n`:
3. For `j` from 0 to `i-1`:
4. For each `a` in `dp[j]` and `b` in `dp[i-1-j]`:
5. Add `"(" + a + ")" + b` to `dp[i]`.
6. Return `dp[n]`.

### Worked Example (Dry Run)
`n = 3`.

- `dp[0] = [""], dp[1] = ["()"]`.
- `dp[2]`: `j=0`: `"(" + "" + ")" + "()" = "()()"`. `j=1`: `"(" + "()" + ")" + "" = "(())"`. → `["()()", "(())"]`.
- `dp[3]`: `j=0`: `"(" + "" + ")" + dp[2]` → `"()(())"`, `"()()()"`. `j=1`: `"(" + "()" + ")" + dp[1]` → `"(())()"`, `"(()())"`. `j=2`: `"(" + dp[2] + ")" + ""` → `"((()))"`, `"(()())"`.

After dedup: `["((()))", "(()())", "(())()", "()(())", "()()()"]`. Answer: 5 strings.

### Code
```python
def generate_parenthesis(n: int) -> list:
    dp = [[] for _ in range(n + 1)]
    dp[0] = [""]
    if n >= 1:
        dp[1] = ["()"]
    for i in range(2, n + 1):
        for j in range(i):
            for a in dp[j]:
                for b in dp[i - 1 - j]:
                    dp[i].append("(" + a + ")" + b)
    return dp[n]
```

### Complexity
- Time: O(4^n / √n) — the nth Catalan number of valid strings, each of length 2n.
- Space: O(4^n / √n) for storing all strings.

### Common Mistakes & Edge Cases**
- `n = 0` → `[""]` (empty string is valid).
- `n = 1` → `["()"]`.
- Backtracking approach: track `open_count` and `close_count`, only add `(` if `open < n`, only add `)` if `close < open`.
- The DP approach avoids duplicates naturally because each `(A)B` decomposition is unique.
