# 01 Graph Representations — Graphs

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a graph and its kinds.**
   - A graph is a set of vertices (V) and edges (E). It can be undirected or directed, weighted or unweighted, connected or disconnected, acyclic (trees/DAG) or cyclic.

2. **What are the common representations of a graph?**
   - Adjacency matrix (V×V, O(V^2) space, O(1) edge check), adjacency list (dict of lists, O(V+E) space), and edge list (list of (u,v,w)). For sparse graphs adjacency lists dominate.

3. **Why is an adjacency list preferred for competitive problems?**
   - Space O(V+E) not O(V^2); fast iteration over neighbours in BFS/DFS; simple dict/set of neighbours in Python.

4. **When would you use an adjacency matrix?**
   - Dense graphs (E ~ V^2), frequent O(1) edge-existence queries, and small V (≤ few thousand). Used in Floyd-Warshall style all-pairs.

5. **How do you store a weighted graph?**
   - Adjacency list of (neighbour, weight) tuples; matrix stores weights; edge list stores (u,v,w). Represent INF for absence in matrix form.

6. **What is the edge list and when is Kruskal used with it?**
   - Edge list is a flat list of edges — ideal for Kruskal's MST (sort by weight, union-find) and for algorithms needing sorted edges. O(E log E) sort.

7. **How does Python typically express an adjacency list?**
   - graph = defaultdict(list); graph[u].append(v) with weights as tuples graph[u].append((v,w)). Used with 'from collections import defaultdict'.

8. **What is an adjacency-set and its benefit?**
   - Set of neighbours per vertex gives O(1) membership (edge existence) at the cost of iteration order; useful when edge-existence queries dominate.

9. **Why is undirected representation duplicated?**
   - An undirected edge (u,v) is stored twice — once in u's list and once in v's list — so traversal can move both ways.

10. **What is a DAG? Give examples.**
   - A directed acyclic graph: directed with no cycles. Examples: dependency graphs, build pipelines, topological-order problems, SP/DSE scheduling questions.

11. **What is a strongly connected component (SCC)?**
   - Maximal set of vertices where each can reach every other via directed paths. Found by Tarjan or Kosaraju in O(V+E); condenses a graph into a DAG.

12. **How do you read graph constraints and choose representation?**
   - n≤10^5, m≤10^5 → adjacency list; n≤10^3 dense → matrix fine; verify memory before designing the algorithm.

13. **What is an implicit graph (grid as graph)?**
   - A grid where each cell is a node and up/right/down/left are neighbour edges; BFS/DFS over (r,c) with boundary checks is graph traversal without building lists.

14. **How do you detect that a traversal is correct on disconnected graphs?**
   - Iterate all vertices; run BFS/DFS from each unvisited; the outer loop guarantees every component processed even when the start is arbitrary.

15. **Explain complexity of building a graph from input.**
   - Reading E edges and storing in adjacency list costs O(E) time and O(V+E) space — typically dominated by the algorithm that follows.

16. **What is the intuition behind the 01 graph representations technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

17. **Write the brute-force approach for a typical 01 graph representations problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

18. **State the time and space complexity of the optimal solution for most 01 graph representations problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

19. **What common edge cases must be handled in 01 graph representations implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

20. **How would you dry-run your 01 graph representations code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

21. **Give a real-world analogy for 01 graph representations.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

22. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

23. **What is the role of a prefix/suffix precomputation in 01 graph representations?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

24. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

25. **How is 01 graph representations asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

26. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

27. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

28. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

29. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

30. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

31. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

32. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

33. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

34. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

35. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

36. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

37. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

38. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

39. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

40. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

41. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

42. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

43. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

44. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

45. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

46. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

47. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

48. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

49. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

50. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

51. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

52. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

53. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

54. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

55. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

56. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

57. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

58. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

59. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

60. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

61. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

62. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

63. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

64. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

65. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

66. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

67. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

68. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

69. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

70. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

71. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

72. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

73. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

74. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

75. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

76. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

77. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

78. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

79. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

80. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

81. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

82. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

83. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

84. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

85. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

86. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

87. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

88. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

89. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

90. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

91. **Give a real-world analogy for 01 graph representations. Extend your answer with a second example.**
   - Analogy: 01 graph representations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

92. **How do you decide between a hash map, sorting, or two pointers as tools for 01 graph representations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

93. **What is the role of a prefix/suffix precomputation in 01 graph representations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

94. **Explain the optimisation step you would mention after writing the naive version for 01 graph representations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

95. **How is 01 graph representations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

96. **What is the intuition behind the 01 graph representations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

97. **Write the brute-force approach for a typical 01 graph representations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

98. **State the time and space complexity of the optimal solution for most 01 graph representations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

99. **What common edge cases must be handled in 01 graph representations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

100. **How would you dry-run your 01 graph representations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

</details>