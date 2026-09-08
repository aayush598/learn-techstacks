# Spatial Reasoning - Concepts & Strategies

## ISRO Exam Context
- Part B Aptitude: 15 questions, 20 marks, NO negative marking
- Spatial reasoning accounts for 3-4 questions — critical for ISRO
- These test 3D visualization ability essential for engineering
- Time: ~2-3 minutes per question (slightly more for paper folding)

---

## 1. Paper Folding (Mentally Fold and Punch Holes)

### Concept
A paper is folded one or more times, holes are punched, then the paper is unfolded. Find the correct unfolded pattern.

### Step-by-Step Method
1. **Trace the fold lines** on the diagram
2. **Mentally fold** step by step, keeping track of layers
3. **Locate the hole position** relative to fold lines
4. **Unfold step by step**, reflecting holes across each fold line
5. **Count total holes** = (number of holes punched) × 2^(number of folds)

### Fold Line Rules
| Fold Type | Effect on Hole |
|-----------|---------------|
| Single fold (1 axis) | Hole appears 2× (original + mirror) |
| Two folds (perpendicular) | Hole appears 4× |
| Diagonal fold | Hole appears 2× along diagonal axis |
| Three folds | Hole appears 8× |

### Hole Position Rules
- Hole near folded edge → holes appear close together when unfolded
- Hole near open edge → holes appear far apart when unfolded
- Hole on fold line → single hole (not doubled) at that position

### Speed Tip
- Start from the LAST fold (innermost) and work outward
- Count holes to eliminate wrong options quickly

---

## 2. Cube Construction from Nets

### Concept
A 2D net (unfolded pattern) is given. Determine which 3D cube it forms.

### Valid Cube Net Rules
- A cube net always has exactly 6 squares
- Not all arrangements of 6 squares form valid nets
- There are exactly 11 valid cube nets

### Opposite Face Rule
- In a valid net, opposite faces are separated by exactly ONE square
- In the T-shaped net: the top and bottom of the T are opposite
- In the cross-shaped net: the four arms are adjacent, top and bottom are opposite

### Common Valid Nets
1. **Cross/Plus shape**: 4 in a row, 1 above, 1 below the middle
2. **T-shape**: 3 in a row, 1 below each end, 1 in the middle bottom
3. **Staircase**: Zigzag pattern of 6 squares
4. **L-shape with extensions**: Various configurations

### Approach
1. Identify opposite face pairs in the net
2. Check if the answer options have these pairs as opposite faces
3. Verify the relative position of adjacent faces

### Speed Tip
- In any net, if two squares share an edge, they are adjacent in 3D
- If two squares are separated by exactly one square in a straight line, they are opposite

---

## 3. Dice Problems

### Concept
Standard or custom dice with specific number arrangements. Find the rule governing the die.

### Standard Die Rule
- Opposite faces sum to 7: (1,6), (2,5), (3,4)
- When looking at a standard die, if you see 1, 2, and 3, they meet at a corner (no two are opposite)

### Custom Die Rules
- Given views of a die, determine which number is opposite which
- Use the "common face" technique: two views sharing a face reveal adjacent numbers

### Common Face Technique
If two views of a die show:
- View 1: Faces A, B, C
- View 2: Faces A, D, E
- Then A is adjacent to B, C, D, E → A is opposite to the remaining face F

### Approach
1. List all visible faces from given views
2. Identify the common face(s) between views
3. The common face is adjacent to all other visible faces
4. The remaining unseen face must be opposite the common face

### Speed Tip
- Maximum faces visible in one view: 3 (out of 6)
- Two views can reveal 5 faces (1 common + 4 unique) → the 6th is determined

---

## 4. Spatial Visualization

### Concept
Mentally manipulate 3D objects: rotate, flip, or combine shapes.

### Common Tasks
1. **3D rotation**: Given a 3D shape, find its rotated view
2. **Assembly**: Given component parts, determine the assembled 3D shape
3. **Cross-section**: Determine what a 3D shape looks like when cut by a plane

### Rotation Rules
- Rotating 90° about X-axis: Y becomes Z, Z becomes -Y
- Rotating 90° about Y-axis: X becomes Z, Z becomes -X
- Rotating 90° about Z-axis: X becomes Y, Y becomes -X

### Speed Tip
- For simple rotations, track ONE distinctive feature
- For cross-sections, think about which planes the cutting surface intersects

---

## 5. 3D Rotation

### Concept
Given a 3D figure in one orientation, find it after rotation.

### Step-by-Step Method
1. Identify a unique feature of the figure (e.g., a shaded face, marked corner)
2. Determine the axis and direction of rotation
3. Track where that feature moves
4. Eliminate options that don't match

### Common Rotation Axes
- **About vertical axis (Y)**: Left and right swap
- **About horizontal axis (X)**: Top and bottom swap
- **About depth axis (Z)**: Figure rotates in the viewing plane

### Speed Tip
- Track the position of ONE element (e.g., a dot or arrow)
- If the element moves to a position not in your answer, eliminate that option

---

## 6. Block Counting

### Concept
Count the number of cubes in a 3D structure shown in 2D perspective.

### Approach
1. Count cubes layer by layer (bottom to top)
2. For each layer, count visible cubes and estimate hidden ones
3. Hidden cubes exist ONLY if supported by cubes below
4. Total = sum of all layers

### Formula
- Bottom layer: count all positions (visible + hidden beneath upper layers)
- Middle layer: count only positions where cubes exist above
- Top layer: count only visible cubes

### Speed Tip
- Count by columns: each column has height equal to its number of stacked cubes
- Mark counted columns on the diagram to avoid double-counting

---

## Spatial Reasoning Quick Reference

### Cube Properties
- 6 faces, 12 edges, 8 vertices
- Each face has 4 edges
- Each vertex connects 3 edges
- Opposite faces never share an edge

### Paper Folding Quick Guide
| Folds | Punches | Unfolded Holes |
|-------|---------|----------------|
| 1 | 1 | 2 |
| 1 | 2 | 4 |
| 2 | 1 | 4 |
| 2 | 2 | 8 |
| 3 | 1 | 8 |

### Net Identification Cheat Sheet
- 4 squares in a row + 1 above + 1 below = valid (cross)
- 3 squares in a row + 3 attached = check arrangement
- Any arrangement where all 6 squares touch = likely valid
- If a square is "hanging" with no adjacent square on at least one side = check carefully

---

## Common ISRO Spatial Reasoning Patterns

1. **Paper folding with single fold**: Most common, test basic symmetry
2. **Standard die questions**: Opposite faces sum to 7
3. **Cube from net**: Check opposite face pairs
4. **3D rotation**: Track one feature through rotation
5. **Block counting**: Count column heights

---

## Speed-Solving Strategy

### For Paper Folding (30-45 seconds)
1. Note the number of folds → determines hole count
2. Find hole position relative to fold line
3. Unfold mentally: mirror the hole across fold lines
4. Count holes and match with options

### For Cube/Net (20-30 seconds)
1. Identify opposite face pairs in the net
2. Check if answer has same opposite pairs
3. Verify adjacent face orientations

### For Dice (20-30 seconds)
1. List faces visible in each view
2. Find common face
3. Remaining unseen face = opposite to common face

### For Block Counting (30-40 seconds)
1. Count by columns
2. Each column height = number of cubes stacked
3. Sum all column heights

---

## Visualization Exercises (Practice Without Paper)

1. **Mental rotation**: Hold a book in your hand, rotate it 90°, note which face is now on top
2. **Paper folding**: Fold a real paper, punch a hole, unfold, verify your mental prediction
3. **Dice**: Roll a die, cover one face, try to name the opposite face
4. **Block building**: Build a small cube structure, draw it from different angles
