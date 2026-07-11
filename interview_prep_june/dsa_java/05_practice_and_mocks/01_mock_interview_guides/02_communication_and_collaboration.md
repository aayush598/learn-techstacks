# Communication & Collaboration

## The STAR Framework for Interviews

```
S - Situation: "The problem is asking us to..."
T - Task: "I need to find/implement..."
A - Approach: "I can solve this by..."
R - Result: "This gives us O(n) time and O(n) space"
```

## Effective Thought Process

**Bad**: "Hmm... I don't know... maybe... let me think..."

**Good**: 
- "Let me think about this..." [pause]
- "A brute force approach would be..."
- "But that's O(n²). Let me look for a better way."
- "I notice the array is sorted, so maybe two pointers?"

## Clarifying Questions to Ask

1. "What are the constraints on input size?"
2. "Can the input contain duplicates?"
3. "What should I return if no valid answer exists?"
4. "Is the array guaranteed to be sorted?"
5. "Can I modify the input?"
6. "What's more important — time or space?"

## Verbalizing Problem-Solving

```
"I'm thinking about using a HashMap because we need O(1) lookups."

"If I use two pointers, I can reduce O(n²) to O(n)."

"This is similar to the 'Maximum Subarray' problem — I can adapt Kadane's algorithm."

"The bottleneck is the nested loop. Let me try to eliminate it."
```

## Handling Hints

If interviewer says "Consider using a different data structure":
- "You're hinting that I should use something with faster lookups?"
- "Maybe a HashSet would help here?"
- "I could trade space for time by precomputing..."

## What Interviewers Evaluate

- **Clarity**: Can I follow your thinking?
- **Structure**: Do you work systematically?
- **Collaboration**: Can you take and respond to hints?
- **Depth**: Do you understand trade-offs?
- **Ownership**: Do you test and debug your own code?

## Phrases That Help

| Use | Avoid |
|-----|-------|
| "Let me walk through an example." | "That's it, I'm done." |
| "One approach would be..." | "This is the only way." |
| "The trade-off here is..." | "This is optimal, period." |
| "Let me check if this edge case works." | "I'll handle edge cases later." |
| "I'm considering X because Y." | "I'll just use X." |
