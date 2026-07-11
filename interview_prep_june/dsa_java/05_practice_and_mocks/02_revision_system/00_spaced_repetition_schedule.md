# Spaced Repetition Schedule

## The Principle

Review content at increasing intervals to move it from short-term to long-term memory.

```
Study → Review after 1 day → Review after 3 days → 7 days → 14 days → 30 days
```

## DSA Spaced Repetition Schedule

### Daily
- 30 min review of yesterday's problems (re-solve if you can't recall the pattern)
- 60 min learning new concepts/problems

### Weekly Review (2-3 hours every Sunday)
- Review all problems from the week
- Categorize: "Knew immediately" / "Had to think" / "Couldn't solve"
- Re-solve any in the "Couldn't solve" category

### Monthly Review (4 hours every month end)
- Pick 5 random problems from each topic covered
- Simulate interview conditions (timed, no distractions)
- Identify weak areas for next month's focus

## Review Intervals by Problem Difficulty

| After Solving | Review After |
|---------------|--------------|
| First time | 1 day |
| 2nd review (knew it) | 3 days |
| 3rd review (still knew it) | 7 days |
| 4th review | 14 days |
| 5th review | 30 days |

If you struggle at any review, reset to 1 day interval.

## Tracking Template

Create a simple spreadsheet:

```
Date     | Problem                  | Pattern       | Next Review | Status
2026-01-01| Two Sum                  | HashMap       | 2026-01-02  | Solved
2026-01-02| Two Sum (review)         | HashMap       | 2026-01-05  | Easy
2026-01-02| Longest Substring Without| Sliding Window| 2026-01-03  | Solved
```

## Tools

- **Anki**: Best for spaced repetition. Create cards with problem name on front, solution pattern on back.
- **Notion**: Spreadsheet view + calendar for review scheduling
- **Google Sheets**: Simple tracking with conditional formatting
- **LeetCode Lists**: Create "Review" list with scheduled dates
