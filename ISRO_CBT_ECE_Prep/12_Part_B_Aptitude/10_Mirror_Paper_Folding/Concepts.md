# Mirror & Paper Folding - Concepts & Strategies

## ISRO Exam Context
- Part B Aptitude: 15 questions, 20 marks, NO negative marking
- Mirror and paper folding: 2-3 questions per exam (high frequency)
- Tests spatial visualization — critical for ISRO
- Time: ~2 minutes per question

---

## 1. Mirror Image Identification

### Vertical Mirror (Most Common)
The mirror is placed vertically (left or right of the figure).

### Rules for Vertical Mirror
- Left and right are SWAPPED
- Top and bottom REMAIN THE SAME
- Distance from mirror is preserved
- Symmetric figures appear unchanged

### Key Characteristic Changes
| Feature | Vertical Mirror Effect |
|---------|----------------------|
| Horizontal lines | Reversed direction |
| Vertical lines | Unchanged |
| Circles | Unchanged |
| Letters (asymmetric) | Horizontally flipped |
| Numbers | Horizontally flipped |
| Arrows (horizontal) | Point in opposite direction |
| Arrows (vertical) | Unchanged |

### Mirror-Resistant Characters (appear same after vertical mirror)
A, H, I, M, O, T, U, V, W, X, Y

### Characters That Change
| Original | Vertical Mirror |
|----------|----------------|
| B | Reversed B |
| C | Reversed C |
| D | Reversed D |
| E | Reversed E |
| F | Reversed F |
| G | Reversed G |
| J | Reversed J |
| K | Reversed K |
| L | Reversed L |
| N | Reversed N |
| P | Reversed P |
| Q | Reversed Q |
| R | Reversed R |
| S | Reversed S |
| Z | Reversed Z |

### Speed Tip
- Check 3 distinctive features, not the whole image
- Focus on asymmetric elements (they change the most)

---

## 2. Horizontal Mirror (Water Image)

The mirror is placed horizontally (above or below the figure).

### Rules for Horizontal Mirror
- Top and bottom are SWAPPED
- Left and right REMAIN THE SAME
- Distance from mirror is preserved
- Figures are flipped upside down

### Key Characteristic Changes
| Feature | Horizontal Mirror Effect |
|---------|------------------------|
| Horizontal lines | Unchanged |
| Vertical lines | Reversed (top-bottom flip) |
| Letters | Flipped upside down |
| Arrows (vertical) | Point in opposite direction |
| Arrows (horizontal) | Unchanged |

### Characters That Change Under Horizontal Mirror
| Original | Horizontal Mirror |
|----------|------------------|
| A | Flipped A |
| B | B (if symmetric) |
| C | C (if symmetric) |
| D | D (if symmetric) |
| M | W |
| W | M |
| 3 | Reversed 3 |
| 2 | Reversed 2 |

### Characters That Stay Same Under Horizontal Mirror
H, I, O, X (horizontally symmetric characters)

### Speed Tip
- Horizontal mirror = flip upside down
- M becomes W, W becomes M (common ISRO trick)

---

## 3. Paper Folding and Cutting Patterns

### Concept
Paper is folded, a pattern is cut/punched, and you must identify the unfolded pattern.

### Fold Types
| Fold | Layers | Effect |
|------|--------|--------|
| 1 horizontal fold | 2 layers | Mirror across horizontal axis |
| 1 vertical fold | 2 layers | Mirror across vertical axis |
| 2 perpendicular folds | 4 layers | Mirror across both axes |
| 1 diagonal fold | 2 layers | Mirror across diagonal |
| 2 diagonal folds | 4 layers | Mirror across both diagonals |
| 3 folds | 8 layers | Mirror across 3 axes |

### Cut/Hole Rules
- **Through all layers**: Hole appears 2^n times (n = number of folds)
- **Partial cut**: Depends on which layers are cut
- **On fold line**: Single hole (not doubled) at that position
- **Near fold**: Holes appear close together when unfolded
- **Away from fold**: Holes appear far apart when unfolded

### Unfolding Sequence
1. Start with the LAST fold (innermost)
2. Reflect the cut/hole pattern across the fold line
3. Continue unfolding one fold at a time
4. After each unfold, double the number of cut impressions

---

## 4. Unfolded Paper Reconstruction

### Concept
Given a cut pattern, determine where it was folded and how.

### Approach
1. Count the number of cut impressions → determines number of folds
2. Look for symmetry → fold lines are axes of symmetry
3. Find the simplest folding pattern that produces the given cut arrangement
4. Verify by mentally folding and checking

### Symmetry Analysis
| Cut Pattern Symmetry | Likely Fold Lines |
|---------------------|-------------------|
| 4-fold rotational | 2 perpendicular folds |
| Mirror (horizontal + vertical) | 2 perpendicular folds |
| Diagonal symmetry | Diagonal fold(s) |
| 2-fold symmetry | 1 fold |
| No symmetry | Complex folding |

---

## 5. Advanced Mirror Images

### Mirror at 45°
- The mirror image appears rotated and flipped
- Diagonal elements may become horizontal or vertical

### Mirror Combined with Rotation
- Some problems combine mirror image with rotation
- First find the mirror image, then apply rotation (or vice versa)

### Multiple Mirrors
- Two mirrors at 90°: creates 4 images (including original)
- The number of images = 360°/angle between mirrors - 1

---

## 6. Paper Folding with Multiple Cuts

### Concept
Multiple holes/cuts are made in the folded paper.

### Approach
1. Count total holes in folded state = m
2. Count number of folds = n
3. Total holes when unfolded = m × 2^n
4. Each hole mirrors across each fold line independently

### Example
- 3 folds → 8 layers
- 2 holes punched → 2 × 8 = 16 holes when unfolded
- Each hole creates 8 copies (mirror images)

---

## 7. Cutting Patterns (Not Just Holes)

### Types of Cuts
| Cut Type | Unfolded Result |
|----------|----------------|
| Circular hole | Symmetric circular pattern |
| Square hole | Symmetric square pattern |
| Triangular notch | Star-like pattern |
| Strip cut | Geometric pattern |
| Corner cut | Corner features in all quadrants |

### Speed Tip
- For circular holes: count the holes and check positions
- For geometric cuts: the unfolded pattern will be symmetric about fold lines
- Eliminate options that break symmetry

---

## Mirror & Paper Folding Speed-Solving Framework

### For Mirror Images (30-45 seconds)
1. Identify mirror type (vertical/horizontal/diagonal)
2. Check left-right or top-bottom reversal
3. Focus on 2-3 asymmetric features
4. Eliminate options that don't match

### For Paper Folding (60-90 seconds)
1. Count folds → determine hole count
2. Note hole position relative to fold lines
3. Unfold step by step mentally
4. Count total holes and verify positions
5. Eliminate options with wrong hole count first

---

## Common ISRO Mirror & Paper Folding Patterns

1. **Vertical mirror with letters**: Most common mirror question
2. **Single fold with one hole**: Simplest paper folding
3. **Double fold with two holes**: Moderate difficulty
4. **Diagonal fold**: Tests diagonal symmetry understanding
5. **Combined fold + cut**: Complex folding with geometric cuts

---

## Quick Reference: Mirror Image Checks

| Check | Vertical Mirror | Horizontal Mirror |
|-------|----------------|-------------------|
| Left-right swap | ✓ | ✗ |
| Top-bottom swap | ✗ | ✓ |
| Vertical lines | Same | Flipped |
| Horizontal lines | Flipped | Same |
| Circles | Same | Same |
| Letters | Flipped L-R | Flipped T-B |

---

## Quick Reference: Paper Fold Hole Count

| Folds | Layers | 1 hole → | 2 holes → | 3 holes → |
|-------|--------|----------|-----------|-----------|
| 1 | 2 | 2 | 4 | 6 |
| 2 | 4 | 4 | 8 | 12 |
| 3 | 8 | 8 | 16 | 24 |
| 4 | 16 | 16 | 32 | 48 |

---

## Speed Tips Summary

| Technique | When to Use | Time Saved |
|-----------|-------------|------------|
| Check asymmetric features | Mirror images | ~20 seconds |
| Count holes first | Paper folding | ~15 seconds |
| Symmetry analysis | Reconstruction | ~20 seconds |
| Unfold step by step | Complex folding | ~25 seconds |
| Eliminate wrong hole count | All paper folding | ~10 seconds |
| M↔W check | Horizontal mirror | ~5 seconds |
