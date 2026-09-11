# Graphs — Bfs And Dfs Interview Questions and Answers

## Q1: Explain BFS and its data structure.
**A:** Breadth-first search visits level by level using a queue. Starting from a node, it discovers all neighbours, then their neighbours, guaranteeing shortest-path (fewest edges) in unweighted graphs.

## Q2: What is the time and space complexity of BFS?
**A:** O(V+E) time with adjacency lists; O(V) space for the visited set and queue (frontier can be O(V) at one level).

## Q3: Explain DFS with recursion and stack.
**A:** DFS follows one branch as far as possible before backtracking; recursive implementation uses the call stack, or an explicit stack, marking visited on entry. O(V+E).

## Q4: Distinguish BFS vs DFS use-cases.
**A:** BFS: shortest path in unweighted graphs, level-order, connectivity between two nodes at min hops. DFS: cycle detection, topological sort, connected components, path existence, backtracking.

## Q5: How do you detect a cycle in an undirected graph with DFS?
**A:** While DFS from u, if a neighbour v is visited and v != parent[u], a cycle exists. Parent distinction prevents treating the back-edge to origin as a cycle. O(V+E).

## Q6: How do you detect a cycle in a directed graph?
**A:** Use three-colour marking (unvisited/on-stack/done); encountering a grey (currently on recursion stack) node indicates a back-edge → cycle. O(V+E).

## Q7: How do you count connected components?
**A:** Outer loop over vertices; each unvisited start increments the count and its BFS/DFS marks that component. O(V+E).

## Q8: How do you find the shortest path in an unweighted graph?
**A:** BFS from source tracking parent array; distance = level. Reconstruct path by backtracking parents. This is the canonical Infosys 'shortest path BFS' answer.

## Q9: How do you check if a path exists between two vertices?
**A:** Run BFS/DFS from source; true iff the target is visited. If both in same component this is decided by component membership.

## Q10: What is a bipartite check and how is it done?
**A:** A graph is bipartite if its vertices can be coloured 2-colour so that edges always join different colours. BFS colouring: neighbours must be the opposite colour or the answer is False. O(V+E).

## Q11: What is 0-1 BFS and when is it used?
**A:** Edge weights in {0,1}; use a deque pushing 0-weights to the front and 1-weights to the back, achieving O(V+E) shortest paths instead of Dijkstra's O(E log V).

## Q12: What is topological ordering?
**A:** A linear ordering of a DAG where every edge u→v has u before v. Kahn's algorithm (indegree-0 queue) or DFS finishing-time reversal produce it in O(V+E).

## Q13: How does Kahn's algorithm detect a DAG?
**A:** Process indegree-0 nodes; decrement neighbours; if processed < V nodes, a cycle exists (remainder have nonzero indegree). O(V+E).

## Q14: How do you find the number of islands (grid BFS/DFS)?
**A:** Scan cells; on encountering an unvisited '1', increment count and flood-fill (BFS/DFS) over adjacent land marking visited. O(rows×cols). This was literally asked in SP/DSE.

## Q15: What are flood-fill variations used for?
**A:** Image fill, islands, largest island, regions bounded by water, and matrix-connectivity problems — all apply BFS/DFS over 4-direction neighbours.

## Q16: How do you get all paths from source to target?
**A:** DFS tracking current path and visited; when target reached, copy path. Reuse of vertices is forbidden inside a single path unless revisits allowed. Exponential worst case.

## Q17: What is multi-source BFS?
**A:** Seed the queue with all sources at distance 0 (e.g., all rotten oranges); the first BFS wave assigns minimal distance from ANY source — classic 'rotting oranges'.

## Q18: How do you find the shortest transformation (word ladder)?
**A:** BFS over word states; neighbours are words differing by one letter. Precompute wildcard patterns or neighbours to keep transitions cheap. BFS gives hops.

## Q19: What is the 'min steps to eat all cheese / nearest 0' style?
**A:** Multi-source BFS computes distance from all targets simultaneously; the cellular-automaton trick gives distances to nearest target in O(V+E).

## Q20: How do you detect if BFS results are level order for trees vs graphs?
**A:** In graphs, BFS level = shortest edge-hops only if unweighted; in weighted graphs you must use Dijkstra or 0-1 BFS — not plain BFS.

## Q21: What is the intuition behind the 02 bfs and dfs technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q22: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q23: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q24: What common edge cases must be handled in 02 bfs and dfs implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q25: How would you dry-run your 02 bfs and dfs code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q26: Give a real-world analogy for 02 bfs and dfs.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q27: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q28: What is the role of a prefix/suffix precomputation in 02 bfs and dfs?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q29: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q30: How is 02 bfs and dfs asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q31: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q32: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q33: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q34: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q35: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q36: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q37: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q38: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q39: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q40: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q41: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q42: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q43: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q44: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q45: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q46: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q47: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q48: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q49: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q50: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q51: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q52: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q53: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q54: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q55: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q56: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q57: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q58: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q59: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q60: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q61: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q62: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q63: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q64: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q65: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q66: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q67: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q68: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q69: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q70: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q71: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q72: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q73: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q74: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q75: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q76: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q77: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q78: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q79: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q80: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q81: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q82: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q83: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q84: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q85: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q86: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q87: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q88: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q89: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q90: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q91: What is the intuition behind the 02 bfs and dfs technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q92: Write the brute-force approach for a typical 02 bfs and dfs problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q93: State the time and space complexity of the optimal solution for most 02 bfs and dfs problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q94: What common edge cases must be handled in 02 bfs and dfs implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q95: How would you dry-run your 02 bfs and dfs code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q96: Give a real-world analogy for 02 bfs and dfs. Extend your answer with a second example.
**A:** Analogy: 02 bfs and dfs is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q97: How do you decide between a hash map, sorting, or two pointers as tools for 02 bfs and dfs? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q98: What is the role of a prefix/suffix precomputation in 02 bfs and dfs? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q99: Explain the optimisation step you would mention after writing the naive version for 02 bfs and dfs. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q100: How is 02 bfs and dfs asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.
