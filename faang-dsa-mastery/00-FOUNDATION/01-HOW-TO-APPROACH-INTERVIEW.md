# How To Approach DSA In FAANG/MAANG Interviews

## The UMPIRE Method (Highly Recommended)
Use this on every question in the interview and while practicing.

| Step | Action | Goal |
| :-- | :-- | :-- |
| **U - Understand** | Clarify input, output, constraints, edge cases. Ask questions. | Remove ambiguity |
| **M - Match** | Map to known patterns (Sliding Window, Two Pointers, HashMap, Stack etc). | Find the right tool |
| **P - Plan** | Think brute force -> optimize. Write logic on paper/whiteboard. Discuss approach. | Show structured thinking |
| **I - Implement** | Code cleanly in Java with meaningful names. Handle edge cases. | Convert plan to code |
| **R - Review** | Dry run with examples + edge cases. Check for nulls, bounds. | Catch silly bugs |
| **E - Evaluate** | Give TC, SC, and possible follow-ups/optimizations. | Prove you're efficient |

## Complexity Mindset
- **Time Complexity**: Always think best/average/worst. Aim for optimal for given constraints.
- **Space Complexity**: Prefer O(1) extra excluding input. Count auxiliary space.
- **Constraints Clue**: n <= 10^3 -> O(n^2) acceptable, n <= 10^4-10^5 -> need O(n log n), n large with values -> think Hashing/DP/Graphs.

## Java Tips For Interviews
- Use Arrays, ArrayList, HashMap, HashSet, LinkedList, Stack, Queue, PriorityQueue, Deque.
- Write helper methods when needed (cleaner).
- Prefer iterative over heavy recursion only if stack depth is concern (Java stack limited).
- Use `int[]`, `StringBuilder` where efficient.
- Don't overuse built-ins unnecessarily but use them wisely.

## Daily Practice Discipline
- **First Pass (Learn)**: Understand, derive, code with help only if truly stuck after 20-25 min.
- **Second Pass (Recall)**: Next day/week revise without looking at solution.
- **Third Pass (Speed)**: Time-bound under pressure.
- **Explain Out Loud**: If you can't explain, you haven't mastered.

## Red Flags To Avoid
- Jumping to code without approach
- Ignoring constraints
- Not testing edge cases (empty, single element, duplicates, all same, sorted/reverse)
- Writing unreadable code
- Overcomplicating simple problems
