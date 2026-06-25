# Data Structures & Algorithms - 200+ Interview Q&A

## Arrays & Strings (Q1-Q40)

### Q1: Reverse a string in-place. (Two pointer approach)
**Answer:** Use two pointers, left=0, right=n-1. Swap s[left] and s[right]. Move left++, right--. O(n) time, O(1) space.

### Q2: Two Sum problem and variants?
**Answer:** Given array and target, find two numbers that sum to target. HashMap solution: for each num, check if target-num in map. O(n). Variants: Two Sum II (sorted - two pointer), Three Sum (sort + two pointer), Four Sum.

### Q3: Find maximum subarray sum (Kadane's algorithm)?
**Answer:** Keep current_sum = max(num, current_sum+num), max_sum = max(max_sum, current_sum). O(n). Handles all negatives.

## Linked Lists (Q41-Q70)

### Q4: Reverse a linked list?
**Answer:** Three pointers: prev=None, curr=head, next=curr.next. In loop: curr.next=prev, prev=curr, curr=next. O(n). Also recursive: reverse rest, point head.next.next=head, head.next=None.

### Q5: Detect cycle in linked list (Floyd's algorithm)?
**Answer:** Slow and fast pointer. Slow moves 1 step, fast moves 2 steps. If they meet, cycle exists. O(n). Find cycle start: reset one to head, move both 1 step until they meet.

## Trees (Q71-Q110)

### Q6: Binary tree traversals (recursive + iterative)?
**Answer:** Inorder (left, root, right), Preorder (root, left, right), Postorder (left, right, root), Level order (BFS). Iterative: use stack for DFS, queue for BFS.

### Q7: Lowest Common Ancestor of BST?
**Answer:** If root.val > p.val and > q.val, go left. If root.val < p.val and < q.val, go right. Else root is LCA. O(h). For binary tree (not BST): recursive search left/right.

## Dynamic Programming (Q111-Q150)

### Q8: Fibonacci - DP approaches?
**Answer:** Recursive O(2^n). Memoized top-down O(n). Bottom-up O(n). Space optimized O(1). Matrix exponentiation O(log n). Binet's formula O(1).

### Q9: Longest Common Subsequence?
**Answer:** DP[i][j] = LCS of text1[0:i] and text2[0:j]. If chars match: DP[i][j]=DP[i-1][j-1]+1, else DP[i][j]=max(DP[i-1][j], DP[i][j-1]). O(m*n).

## Graphs (Q151-Q180)

### Q10: BFS vs DFS - when to use?
**Answer:** BFS: shortest path in unweighted graph, level-order traversal. DFS: path finding, topological sort, cycle detection, connected components. BFS uses queue, DFS uses stack/recursion.

## Sorting & Searching (Q181-Q200)

### Q11: Quick Sort vs Merge Sort?
**Answer:** Quick Sort: O(n log n) average, O(n²) worst, in-place, unstable. Merge Sort: O(n log n) always, O(n) space, stable. Quick Sort faster in practice but Merge Sort has guaranteed performance.

### Q12: Binary search implementation?
**Answer:** left=0, right=n-1, while left<=right: mid=(left+right)//2. If arr[mid]==target return mid. If arr[mid]<target, left=mid+1, else right=mid-1. O(log n).
