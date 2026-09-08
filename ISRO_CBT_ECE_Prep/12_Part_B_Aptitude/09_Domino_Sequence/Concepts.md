# Domino Sequence - Concepts & Strategies

## ISRO Exam Context
- Part B Aptitude: 15 questions, 20 marks, NO negative marking
- Domino sequence: 1-2 questions per exam
- Tests pattern recognition in number sequences
- Time: ~1.5 minutes per question

---

## 1. Domino Pattern Recognition

### What Are Domino Sequences?
Numbers arranged in domino-style format (top and bottom values) following a specific pattern.

### Common Domino Formats
| Format | Description |
|--------|-------------|
| Single row | Numbers in a line with separators |
| Top-bottom pairs | Two rows of numbers |
| L-shape | Three positions (top-left, top-right, bottom) |
| T-shape | Four positions around a center |

### Basic Pattern Types
1. **Linear progression**: Numbers increase/decrease by a fixed amount
2. **Cyclic patterns**: Numbers repeat in a cycle
3. **Mirror/symmetry**: Numbers reflect around a center
4. **Sum/product relationships**: Relationships between pairs

---

## 2. Number Sequences in Domino Format

### Type 1: Separate Top and Bottom Sequences
Each row (top and bottom) follows its own independent pattern.

**Example:**
```
Top:    1  3  5  7  9
Bottom: 2  4  6  8  ?
```
- Top: Odd numbers (+2)
- Bottom: Even numbers (+2)
- Answer: 10

### Type 2: Top-Bottom Relationship
Each domino has a relationship between top and bottom values.

**Example:**
```
Top:    2  4  6  8
Bottom: 4  8 12 16
```
- Relationship: Bottom = 2 × Top
- Or: Bottom increases by 4 each time

### Type 3: Cross-Domino Pattern
The pattern spans across multiple dominoes.

**Example:**
```
Domino 1: 3/6
Domino 2: 5/10
Domino 3: 7/14
```
- Top: 3, 5, 7 (+2 each)
- Bottom: 6, 10, 14 (+4 each)
- Or: Bottom = 2 × Top for each domino

---

## 3. Arithmetic Progressions in Dominoes

### Concept
Numbers form an arithmetic sequence (constant difference).

### Finding the Pattern
1. Calculate differences between consecutive numbers
2. If constant → arithmetic progression
3. If differences form a pattern → check second differences

### Common Arithmetic Patterns in Dominoes
| Pattern | Example | Rule |
|---------|---------|------|
| Top +2, Bottom +3 | 1/2, 3/5, 5/8, 7/11 | Independent progressions |
| Top +1, Bottom ×2 | 1/1, 2/2, 3/4, 4/8 | Top linear, bottom geometric |
| Sum constant | 4/4, 3/5, 2/6, 1/7 | Top+Bottom = 8 |

### Speed Tip
- Check if top and bottom sequences are independent first
- If not, look for relationships between top and bottom values

---

## 4. Geometric Progressions in Dominoes

### Concept
Numbers form a geometric sequence (constant ratio).

### Finding the Pattern
1. Calculate ratios between consecutive numbers
2. If constant → geometric progression
3. Common ratios: 2, 3, 1/2, 1/3

### Example
```
Top:    1  2  4  8  16
Bottom: 2  4  8  16  32
```
- Top: ×2 each time (geometric)
- Bottom: ×2 each time (geometric)

---

## 5. Missing Element Identification

### Step-by-Step Approach
1. **Identify the structure**: What positions exist? (top, bottom, left, right)
2. **Separate the sequences**: Find the pattern for each position
3. **Check for relationships**: Between positions within each domino
4. **Apply the rule**: Use the identified pattern to find the missing value
5. **Verify**: Check if your answer fits with the overall pattern

### Common Missing Element Types
| Type | Approach |
|------|----------|
| Last element | Extend the sequence |
| Middle element | Find the gap in the progression |
| Top or bottom | Find the independent pattern for that row |
| Relationship value | Use the top-bottom relationship |

---

## 6. Complex Domino Patterns

### Fibonacci-like Patterns
```
Domino 1: 1/1
Domino 2: 1/2
Domino 3: 2/3
Domino 4: 3/5
```
- Top: 1, 1, 2, 3 → Fibonacci sequence
- Bottom: 1, 2, 3, 5 → Fibonacci sequence

### Alternating Patterns
```
Domino 1: 1/4
Domino 2: 3/2
Domino 3: 1/4
Domino 4: 3/2
```
- Pattern alternates between (1,4) and (3,2)

### Nested Patterns
```
Top:    1  2  3  4  5
Bottom: 5  4  3  2  ?
```
- Top: Increasing (+1)
- Bottom: Decreasing (-1)
- Bottom mirrors the top

---

## 7. Domino Addition/Subtraction Patterns

### Cross-Domino Operations
```
Domino 1: 2/3
Domino 2: 4/5
Domino 3: 6/7
```
- Top: 2, 4, 6 (+2)
- Bottom: 3, 5, 7 (+2)
- Top+Bottom: 5, 9, 13 (+4)

### Ratio Patterns
```
Domino 1: 2/4
Domino 2: 3/6
Domino 3: 4/8
```
- Bottom/Top = 2 for each domino
- Top: 2, 3, 4 (+1)
- Bottom: 4, 6, 8 (+2)

---

## 8. Symmetry in Domino Sequences

### Mirror Symmetry
```
1/4, 2/3, 3/2, 4/1
```
- The sequence mirrors around the center
- Top: 1, 2, 3, 4 (increasing)
- Bottom: 4, 3, 2, 1 (decreasing)

### Palindrome
```
1/2, 3/4, 5/6, 3/4, 1/2
```
- The sequence reads the same forwards and backwards

---

## Domino Sequence Speed-Solving Framework

### Step 1: Identify the Structure (10 seconds)
- How many dominoes? What positions are visible?
- Is it top-bottom, left-right, or a grid?

### Step 2: Separate Sequences (20 seconds)
- Find the pattern for the top row
- Find the pattern for the bottom row
- Check for relationships between top and bottom

### Step 3: Verify Pattern (15 seconds)
- Does the pattern hold for ALL given dominoes?
- If not, look for an alternative pattern

### Step 4: Find Missing Value (10 seconds)
- Apply the identified rule to get the answer

---

## Common ISRO Domino Sequence Patterns

1. **Independent top/bottom progressions**: Most common
2. **Bottom = k × Top**: Simple multiplication relationship
3. **Sum of top+bottom constant**: Cross-domino relationship
4. **Fibonacci sequences**: Top and/or bottom follow Fibonacci
5. **Alternating patterns**: Two values alternate

---

## Quick Reference: Sequence Types

| Type | Rule | Example |
|------|------|---------|
| Arithmetic | +k constant | 2,5,8,11,... |
| Geometric | ×k constant | 2,6,18,54,... |
| Fibonacci | Sum of previous two | 1,1,2,3,5,... |
| Alternating | Two values alternate | 1,3,1,3,... |
| Mirror | Symmetric about center | 1,2,3,2,1 |
| Square | n² | 1,4,9,16,... |

---

## Speed Tips Summary

| Technique | When to Use | Time Saved |
|-----------|-------------|------------|
| Check rows independently | Most domino problems | ~20 seconds |
| Calculate differences | Arithmetic sequences | ~15 seconds |
| Calculate ratios | Geometric sequences | ~15 seconds |
| Check sum/product | Relationship patterns | ~15 seconds |
| Verify with all data | Before finalizing answer | ~10 seconds |
