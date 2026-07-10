# Parentheses Problems

Parentheses matching is a classic stack application. These problems range from easy validation to hard generation and removal — learn them in order.

---

## 1. Valid Parentheses

**Problem:** Given a string containing only `(){}[]`, determine if the input is valid.

**Key rules:** Open brackets must be closed by the same type, and in the correct order.

```java
public static boolean isValid(String s) {
    Map<Character, Character> closeToOpen = new HashMap<>();
    closeToOpen.put(')', '(');
    closeToOpen.put('}', '{');
    closeToOpen.put(']', '[');

    Deque<Character> stack = new ArrayDeque<>();

    for (char c : s.toCharArray()) {
        if (closeToOpen.containsKey(c)) {
            // It's a closing bracket — check top of stack
            if (stack.isEmpty() || stack.pop() != closeToOpen.get(c)) {
                return false;
            }
        } else {
            // It's an opening bracket — push to stack
            stack.push(c);
        }
    }

    return stack.isEmpty();
}
```

**Walkthrough: `"{[()]}"`**

| char | Action | Stack |
|------|--------|-------|
| `{` | push | `{` |
| `[` | push | `{[` |
| `(` | push | `{[(` |
| `)` | pop, match `(` | `{[` |
| `]` | pop, match `[` | `{` |
| `}` | pop, match `{` | empty |

Stack empty → valid!

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n)  | (worst case: all opening brackets) |

---

## 2. Generate Parentheses

**Problem:** Generate all combinations of `n` pairs of valid parentheses.

**Example:** n=2 → `["(())", "()()"]`

### Approach: Backtracking

```java
public static List<String> generateParenthesis(int n) {
    List<String> result = new ArrayList<>();
    backtrack(result, new StringBuilder(), 0, 0, n);
    return result;
}

private static void backtrack(List<String> result, StringBuilder sb,
                               int open, int close, int n) {
    // Base case: we've used all parentheses
    if (sb.length() == 2 * n) {
        result.add(sb.toString());
        return;
    }

    // Can add '(' if we haven't used all n open brackets
    if (open < n) {
        sb.append('(');
        backtrack(result, sb, open + 1, close, n);
        sb.deleteCharAt(sb.length() - 1); // undo
    }

    // Can add ')' if we have more opens than closes
    if (close < open) {
        sb.append(')');
        backtrack(result, sb, open, close + 1, n);
        sb.deleteCharAt(sb.length() - 1); // undo
    }
}
```

**Why the two conditions?**
1. `open < n` → we haven't placed all opening brackets yet
2. `close < open` → we have unmatched opening brackets to close

**This guarantees every generated string is valid.**

### Decision Tree for n=2

```
                ""
               /    \
              (      (   ← only '(' can start
             / \
           ((  ()
          /   \
        (((  (()    ← ((( has open=3 > n=2, blocked
         |
       ((()
      /    \
  ((())  (()())
```

Result: `["(())", "()()"]`

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(4ⁿ / √n) | (Catalan number) |
| Space  | O(n)  | (recursion depth) |

---

## 3. Longest Valid Parentheses

**Problem:** Find the length of the longest valid (well-formed) parentheses substring.

**Example:** `"(()"` → 2, `")()())"` → 4

### Approach 1: Stack with -1 Initialization

```java
public static int longestValidParentheses(String s) {
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(-1); // base index for valid substring length calculation
    int maxLen = 0;

    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == '(') {
            stack.push(i);
        } else {
            stack.pop();
            if (stack.isEmpty()) {
                stack.push(i); // current ')' becomes the new base
            } else {
                maxLen = Math.max(maxLen, i - stack.peek());
            }
        }
    }

    return maxLen;
}
```

**Why push -1 initially?** It serves as a sentinel index. When we pop and the stack isn't empty, `i - stack.peek()` gives the length of the valid substring from the index after the top of stack to the current index.

**Walkthrough: `")()())"`**

| i | char | Action | Stack | maxLen |
|---|------|--------|-------|--------|
| 0 | `)` | pop -1, stack empty, push 0 | [0] | 0 |
| 1 | `(` | push 1 | [0,1] | 0 |
| 2 | `)` | pop 1, peek 0 | [0] | 2-0=2 |
| 3 | `(` | push 3 | [0,3] | 2 |
| 4 | `)` | pop 3, peek 0 | [0] | 4-0=4 |
| 5 | `)` | pop 0, stack empty, push 5 | [5] | 4 |

Answer: 4

### Approach 2: DP

```java
public static int longestValidParenthesesDP(String s) {
    int n = s.length();
    int[] dp = new int[n]; // dp[i] = length of longest valid substring ending at i
    int maxLen = 0;

    for (int i = 1; i < n; i++) {
        if (s.charAt(i) == ')') {
            if (s.charAt(i - 1) == '(') {
                // Case 1: ...()
                dp[i] = (i >= 2 ? dp[i - 2] : 0) + 2;
            } else if (dp[i - 1] > 0) {
                // Case 2: ...))
                int matchIndex = i - dp[i - 1] - 1;
                if (matchIndex >= 0 && s.charAt(matchIndex) == '(') {
                    dp[i] = dp[i - 1] + 2 + (matchIndex >= 1 ? dp[matchIndex - 1] : 0);
                }
            }
            maxLen = Math.max(maxLen, dp[i]);
        }
    }

    return maxLen;
}
```

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| Stack | O(n) | O(n) |
| DP | O(n) | O(n) |

---

## 4. Remove Invalid Parentheses

**Problem:** Remove the minimum number of invalid parentheses to make the string valid. Return all possible results.

**Example:** `"(a)())()"` → `["(a)()()", "(a())()"]`

### Approach: BFS

```java
public static List<String> removeInvalidParentheses(String s) {
    List<String> result = new ArrayList<>();
    Set<String> visited = new HashSet<>();
    Queue<String> queue = new LinkedList<>();

    queue.offer(s);
    visited.add(s);
    boolean found = false;

    while (!queue.isEmpty()) {
        String curr = queue.poll();

        if (isValid(curr)) {
            result.add(curr);
            found = true; // Don't go deeper — we want minimum removals
        }

        if (found) continue; // Skip generating more at this level

        // Try removing each parenthesis
        for (int i = 0; i < curr.length(); i++) {
            char c = curr.charAt(i);
            if (c != '(' && c != ')') continue;

            String next = curr.substring(0, i) + curr.substring(i + 1);

            if (!visited.contains(next)) {
                visited.add(next);
                queue.offer(next);
            }
        }
    }

    return result;
}

private static boolean isValid(String s) {
    int count = 0;
    for (char c : s.toCharArray()) {
        if (c == '(') count++;
        else if (c == ')') count--;
        if (count < 0) return false;
    }
    return count == 0;
}
```

**Why BFS?** BFS explores all strings with 1 removal, then 2 removals, etc. The first level where we find valid strings gives us the minimum removals.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(2ⁿ) worst case |
| Space  | O(2ⁿ) |

---

## 5. Minimum Add to Make Parentheses Valid

**Problem:** Given a string of parentheses, find the minimum number of additions (insertions) needed to make it valid.

**Example:** `"())"` → 1, `"((("` → 3

```java
public static int minAddToMakeValid(String s) {
    int unmatchedClose = 0; // ')' without a matching '('
    int unmatchedOpen = 0;  // '(' without a matching ')'

    for (char c : s.toCharArray()) {
        if (c == '(') {
            unmatchedOpen++;
        } else {
            if (unmatchedOpen > 0) {
                unmatchedOpen--; // matched with a previous '('
            } else {
                unmatchedClose++; // no matching '(' found
            }
        }
    }

    return unmatchedOpen + unmatchedClose;
}
```

**Why this works:** At the end:
- `unmatchedOpen` = number of '(' that need a ')' after them
- `unmatchedClose` = number of ')' that need a '(' before them
- Each unmatched bracket needs exactly one insertion

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 6. Minimum Insertions to Balance a Parentheses String

**Problem:** Given a string of only `(` and `)`, find the minimum number of insertions to balance it.

**Note:** This version considers `))` as a valid closing pair (double close).

```java
public static int minInsertions(String s) {
    int insertions = 0;
    int closeNeeded = 0; // how many ')' we still need

    for (char c : s.toCharArray()) {
        if (c == '(') {
            closeNeeded += 2; // each '(' needs '))'

            // If odd ')' needed, we insert one ')' to make it even
            if (closeNeeded % 2 != 0) {
                insertions++;
                closeNeeded--;
            }
        } else {
            closeNeeded--;

            if (closeNeeded < 0) {
                insertions++; // need a '(' before this ')'
                closeNeeded = 1; // this ')' counts as one of the needed '))'
            }
        }
    }

    return insertions + closeNeeded;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Valid Parentheses
    System.out.println(isValid("()"));       // true
    System.out.println(isValid("()[]{}"));   // true
    System.out.println(isValid("(]"));       // false
    System.out.println(isValid("([)]"));     // false
    System.out.println(isValid("{[]}"));     // true

    // Test 2: Generate Parentheses
    System.out.println(generateParenthesis(2)); // [(()), ()()]
    System.out.println(generateParenthesis(3));
    // [((())), (()()), (())(), ()(()), ()()()]

    // Test 3: Longest Valid Parentheses
    System.out.println(longestValidParentheses("(()"));      // 2
    System.out.println(longestValidParentheses(")()())"));   // 4
    System.out.println(longestValidParentheses(""));         // 0

    // Test 4: Remove Invalid Parentheses
    System.out.println(removeInvalidParentheses("(a)())()"));
    // [(a)()(), (a())()]
    System.out.println(removeInvalidParentheses(")("));  // [""]

    // Test 5: Min Add
    System.out.println(minAddToMakeValid("((("));  // 3
    System.out.println(minAddToMakeValid("())"));  // 1
    System.out.println(minAddToMakeValid(""));     // 0

    // Test 6: Min Insertions
    System.out.println(minInsertions("(()"));    // 2
    System.out.println(minInsertions("()))"));   // 0
    System.out.println(minInsertions("))())"));  // 3
}
```

---

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Valid Parentheses | Stack | O(n) | O(n) |
| Generate Parentheses | Backtracking | O(4ⁿ/√n) | O(n) |
| Longest Valid Parentheses | Stack or DP | O(n) | O(n) |
| Remove Invalid Parentheses | BFS | O(2ⁿ) | O(2ⁿ) |
| Min Add to Make Valid | Balance counter | O(n) | O(1) |
| Min Insertions to Balance | Balance counter | O(n) | O(1) |

---

## Common Mistakes

1. **Forgetting to check `stack.isEmpty()`** before `stack.pop()` in valid parentheses
2. **Not resetting the base index** in longest valid parentheses — the `-1` initialization is crucial
3. **Using DFS instead of BFS** for remove invalid parentheses — BFS guarantees minimum removals because we find valid strings at the earliest level
4. **Confusing min add with min insertions** — the second version uses `))` as a closing pair, not just `)`
5. **Off-by-one in generate parentheses** — the base case is `sb.length() == 2*n`, not `open == n && close == n`
