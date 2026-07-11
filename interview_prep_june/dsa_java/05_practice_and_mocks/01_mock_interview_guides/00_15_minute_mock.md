# 15-Minute Mock Interview Guide

## Format

Typically a phone screen or early-stage interview:
- 2 problems or 1 medium problem
- 15 minutes total

## Time Breakdown

| Phase | Time | Activity |
|-------|------|----------|
| Understand | 1-2 min | Read problem, ask clarifying questions |
| Approach | 2 min | State the solution, discuss trade-offs |
| Code | 6-7 min | Write clean, correct code |
| Test | 2 min | Dry run with example, check edge cases |
| Wrap | 1-2 min | Complexity analysis, follow-ups |

## Strategy

- **Skip brute force** (time is limited)
- Jump to optimal if you recognize the pattern
- Write code as you explain (don't explain first then code)
- Test with the given example at minimum
- Edge cases: empty input, single element, large values

## Best Topics for 15-minute

1. **Arrays**: Two Sum, Max Subarray, Product Except Self
2. **Strings**: Valid Anagram, Palindrome, Reverse Words
3. **Linked List**: Reverse, Cycle Detection, Merge Two Sorted
4. **Stacks**: Valid Parentheses, Min Stack
5. **Trees**: Max Depth, Invert Tree, Subtree Check

## Example Script

```
Interviewer: "Given an array of integers, return indices of two numbers that add up to target."

You: "Let me clarify: can I use the same element twice? Is the array sorted? 
      Can there be multiple answers? OK, I'll use a HashMap approach.

      I iterate once, storing each value with its index. For each element, 
      I check if (target - current) is in the map. If yes, return both indices.

      [Write code quickly, talking through each line]

      Let me trace with [2,7,11,15], target=9. At 2, map has {2:0}. At 7, 
      target-7=2 is in map, return [0,1]. Edge cases: empty array → return [-1,-1].

      Time: O(n), Space: O(n)."
```
