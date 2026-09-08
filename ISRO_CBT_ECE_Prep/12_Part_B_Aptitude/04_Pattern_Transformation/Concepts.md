# Pattern Transformation - Concepts & Strategies

## ISRO Exam Context
- Part B Aptitude: 15 questions, 20 marks, NO negative marking
- Pattern transformation: 2-3 questions per exam
- Tests ability to identify and apply visual transformations
- Time: ~2 minutes per question

---

## 1. 90° Rotation (Clockwise & Counter-Clockwise)

### Clockwise Rotation (CW)
- Top → Right → Bottom → Left → Top
- An element at 12 o'clock moves to 3 o'clock

### Counter-Clockwise Rotation (CCW)
- Top → Left → Bottom → Right → Top
- An element at 12 o'clock moves to 9 o'clock

### Rotation Tracking Table
| Original Position | After 90° CW | After 90° CCW | After 180° |
|-------------------|-------------|---------------|------------|
| Top | Right | Left | Bottom |
| Right | Bottom | Top | Left |
| Bottom | Left | Right | Top |
| Left | Top | Bottom | Right |
| Top-Left | Top-Right | Bottom-Left | Bottom-Right |
| Top-Right | Bottom-Right | Top-Left | Bottom-Left |
| Bottom-Right | Bottom-Left | Top-Right | Top-Left |
| Bottom-Left | Top-Left | Bottom-Right | Top-Right |
| Center | Center | Center | Center |

### Speed Tip
- For 90° CW: move each element one position clockwise
- For 90° CCW: move each element one position counter-clockwise
- For 180°: flip top↔bottom and left↔right simultaneously

---

## 2. Size Scaling

### Concept
Elements change size in a pattern: small → medium → large, or increasing/decreasing.

### Common Patterns
- **Progressive scaling**: Each step increases size by a fixed factor
- **Alternating sizes**: Small, large, small, large...
- **Proportional scaling**: All elements scale proportionally
- **Selective scaling**: Only specific elements change size

### Speed Tip
- Track size changes of individual elements across the series
- Note if the scaling is uniform (all elements) or selective

---

## 3. Shape Morphing

### Concept
Shapes transform from one type to another across a series.

### Common Morphing Patterns
- Number of sides increases: triangle (3) → square (4) → pentagon (5) → hexagon (6)
- Curves become straight or vice versa
- Internal details change (e.g., solid fill → hatched → empty)
- Complex shapes simplify or vice versa

### Speed Tip
- Count sides/vertices as the primary discriminator
- Check if the shape family changes (e.g., polygon → circle)

---

## 4. Element Position Tracking in Matrices

### Concept
In a 3×3 grid, elements move according to a rule across rows or columns.

### Row-Based Movement
- Elements shift right by one position each row (cyclic)
- Elements shift left by one position each row (cyclic)
- Elements swap positions between consecutive rows

### Column-Based Movement
- Elements shift down by one position each column
- Elements shift up by one position each column

### Diagonal Movement
- Elements move diagonally across the matrix

### Speed Tip
- Track ONE element across all rows to find its movement rule
- Verify the rule holds for ALL elements before applying to find the missing one

---

## 5. Row/Column Pattern Identification

### Concept
Each row or column follows an independent pattern. Find the missing element.

### Row Pattern Types
1. **Cyclic shift**: Elements rotate within the row
2. **Element addition**: Elements from previous rows combine
3. **Element subtraction**: Elements cancel out
4. **Set completion**: Each row contains one of each element type

### Column Pattern Types
1. **Progressive change**: Size, count, or shading changes progressively
2. **Same elements**: All rows in a column share one element
3. **Alternating**: Odd and even rows have different patterns

### Speed Tip
- Check if each row has the same set of elements (just rearranged)
- If yes, it's a permutation/cyclic pattern
- If no, check for progressive changes

---

## 6. Combination Rules (for Matrices)

### Common Combination Rules
| Rule | Description | Example |
|------|-------------|---------|
| XOR (Exclusive OR) | Elements appearing in exactly one input appear in output | Row 1 + Row 2 = Row 3 |
| AND | Elements appearing in both inputs appear in output | Common elements only |
| OR | Elements appearing in either input appear in output | All elements combined |
| Subtraction | Remove elements of Row 1 from Row 2 | Row 2 - Row 1 = Row 3 |
| Superposition | Overlay Row 1 and Row 2 | All elements combined, overlapping preserved |

### Speed Tip
- For 3×3 matrices, check if Row 1 + Row 2 = Row 3 (most common rule)
- Also check Column 1 + Column 2 = Column 3

---

## 7. Color/Shading Transformation

### Concept
Shading patterns change across the series.

### Common Patterns
- White → Shaded → Black (progressive darkening)
- Alternating shading: white, black, white, black
- Shading rotates with the figure
- Number of shaded elements increases/decreases

### Speed Tip
- Track shading independently of position/rotation
- Note if shading is tied to specific elements or to positions

---

## 8. Arrow/Direction Changes

### Concept
Arrows or directional elements change direction in a pattern.

### Common Direction Patterns
- Rotate 90° CW each step
- Rotate 90° CCW each step
- Reverse direction each step
- Follow a path (e.g., clockwise around the figure)

### Speed Tip
- Assign directions as numbers (Up=0, Right=1, Down=2, Left=3)
- Check if the sequence has a pattern (e.g., +1, +1, +1 = CW rotation)

---

## Pattern Transformation Speed-Solving Framework

### Step 1: Identify the Transformation Type (10 seconds)
- Is it rotation, scaling, movement, or combination?

### Step 2: Find the Specific Rule (30 seconds)
- Compare consecutive figures to find what changed
- Write the rule: "Rotate 90° CW and add one dot"

### Step 3: Apply Rule to Last Figure (20 seconds)
- Apply the identified rule to get the answer

### Step 4: Verify with All Figures (20 seconds)
- Check if the rule works for ALL given transitions, not just the last one

---

## Common ISRO Pattern Transformation Questions

1. **90° rotation + element movement**: Most common combination
2. **Matrix with XOR rule**: Row 3 = Row 1 XOR Row 2
3. **Size progression**: Small → Medium → Large in each row
4. **Position cycling**: Elements cycle through positions in each row
5. **Shading rotation**: Shading pattern rotates with the figure

---

## Quick Reference: Position Mapping After Rotation

### 90° Clockwise
```
Before:  After:
1 2 3    7 4 1
4 5 6    8 5 2
7 8 9    9 6 3
```

### 90° Counter-Clockwise
```
Before:  After:
1 2 3    3 6 9
4 5 6    2 5 8
7 8 9    1 4 7
```

### 180° Rotation
```
Before:  After:
1 2 3    9 8 7
4 5 6    6 5 4
7 8 9    3 2 1
```

---

## Speed Tips Summary

| Technique | When to Use | Time Saved |
|-----------|-------------|------------|
| Track single element | Rotation/movement series | ~20 seconds |
| Count elements | Size/number progression | ~15 seconds |
| XOR/AND check | Matrix combination rules | ~25 seconds |
| Shading tracking | Color pattern changes | ~15 seconds |
| Direction numbering | Arrow rotation patterns | ~20 seconds |
