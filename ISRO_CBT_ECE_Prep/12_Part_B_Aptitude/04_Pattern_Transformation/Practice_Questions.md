# Pattern Transformation - Practice Questions (ISRO CBT ECE Style)

> **Exam Pattern**: 15 questions, 20 marks, NO negative marking
> **Time Target**: 2 minutes per question
> **Instructions**: Attempt ALL questions. Draw rough diagrams on paper where needed.

---

## Question 1: 90° Clockwise Rotation

A figure shows a square with an arrow pointing UP. The figure is rotated 90° clockwise. What is the result?

(A) Arrow pointing RIGHT
(B) Arrow pointing LEFT
(C) Arrow pointing DOWN
(D) Arrow pointing UP

**Solution:**
90° CW rotation:
- UP → RIGHT (top moves to right position)

**Answer: (A)** — Arrow pointing RIGHT.

---

## Question 2: Series — Progressive Rotation

Figure 1: Arrow pointing RIGHT
Figure 2: Arrow pointing DOWN
Figure 3: Arrow pointing LEFT
Figure 4: ?

(A) Arrow pointing UP
(B) Arrow pointing RIGHT
(C) Arrow pointing DOWN
(D) Arrow pointing LEFT

**Solution:**
- Figure 1→2: RIGHT to DOWN = 90° CW
- Figure 2→3: DOWN to LEFT = 90° CW
- Rule: 90° CW rotation each step
- Figure 4: LEFT rotated 90° CW = UP

**Answer: (A)** — Arrow pointing UP.

---

## Question 3: Size Scaling

Three circles in a row:
Figure 1: Small circle
Figure 2: Medium circle
Figure 3: Large circle

What comes next?

(A) Extra large circle
(B) Small circle
(C) Medium circle
(D) Disappear

**Solution:**
The pattern shows progressive size increase: Small → Medium → Large.
If the pattern cycles: Small → Medium → Large → Small → ...
Or if it continues: Small → Medium → Large → Extra Large

In most ISRO-style questions, the pattern cycles or reverses.
After reaching maximum size, it typically returns to the smallest.

**Answer: (B)** — Small circle (cycle restarts).

---

## Question 4: Element Position Tracking

A 3×3 grid has a black dot that moves:
- [1,1]: Dot at position (1,1) — top-left
- [1,2]: Dot at position (1,2) — top-center
- [1,3]: Dot at position (1,3) — top-right
- [2,1]: Dot at position (2,1) — middle-left
- [2,2]: Dot at position (2,2) — center

Where is the dot at [2,3]?

(A) Middle-right
(B) Top-right
(C) Bottom-right
(D) Center

**Solution:**
The dot moves one position to the right each step, going row by row:
Row 1: (1,1) → (1,2) → (1,3)
Row 2: (2,1) → (2,2) → (2,3)

Position [2,3] = middle-right.

**Answer: (A)** — Middle-right.

---

## Question 5: Matrix — XOR Rule

3×3 grid with shapes in each cell:
Row 1: △, □, △⊕□
Row 2: ○, △, ○⊕△
Row 3: □, ○, ?

Where ⊕ means the shapes are combined (superimposed).

(A) □⊕○
(B) □
(C) ○
(D) △

**Solution:**
Row 1: △ + □ = △⊕□ (combination)
Row 2: ○ + △ = ○⊕△ (combination)
Row 3: □ + ○ = □⊕○ (combination)

The rule is: Column 3 = Column 1 + Column 2 (superposition)

**Answer: (A)** — □⊕○

---

## Question 6: Shape Morphing — Sides

Figure 1: Triangle (3 sides)
Figure 2: Square (4 sides)
Figure 3: Pentagon (5 sides)
Figure 4: ?

(A) Hexagon (6 sides)
(B) Heptagon (7 sides)
(C) Circle
(D) Square

**Solution:**
3 → 4 → 5 → 6 (sides increasing by 1)

**Answer: (A)** — Hexagon (6 sides).

---

## Question 7: Row Pattern — Cyclic Shift

Row 1: A, B, C
Row 2: C, A, B
Row 3: B, C, ?

(A) A
(B) B
(C) C
(D) D

**Solution:**
Row 1: A, B, C
Row 2: C, A, B (shifted right by 1, cyclic)
Row 3: B, C, A (shifted right by 1 again)

The pattern is cyclic right shift: each row shifts the elements one position to the right.

**Answer: (A)** — A

---

## Question 8: Shading Transformation

Figure 1: White square
Figure 2: Half-shaded square (left half shaded)
Figure 3: Fully shaded square
Figure 4: ?

(A) White square
(B) Half-shaded (right half)
(C) Fully shaded square
(D) Disappear

**Solution:**
Progressive shading: White → Half → Full → ?
The pattern could:
1. Cycle back to White
2. Reverse: Full → Half → White
3. Stay fully shaded

In ISRO-style questions, the most common pattern is cyclic or reversing.
After reaching full shading, it likely reverses: Full → Half → White

**Answer: (B)** — Half-shaded (right half, reversing the pattern).

---

## Question 9: Column Pattern — Addition

Column 1 elements: △, □, ○
Column 2 elements: □, ○, △
Column 3 elements: ○, △, ?

(A) □
(B) △
(C) ○
(D) ◇

**Solution:**
Each column is a cyclic permutation:
Column 1: △, □, ○
Column 2: □, ○, △ (shifted up by 1)
Column 3: ○, △, ? (shifted up by 1 again)

Row 1: △, □, ○
Row 2: □, ○, △
Row 3: ○, △, □

Each row and column has one of each shape (Latin square).

**Answer: (A)** — □

---

## Question 10: 90° CCW Rotation

Figure: A right-facing arrow (→)
After 90° counter-clockwise rotation:

(A) ↑ (up arrow)
(B) ↓ (down arrow)
(C) ← (left arrow)
(D) → (right arrow)

**Solution:**
90° CCW: RIGHT → UP

**Answer: (A)** — ↑ (up arrow).

---

## Question 11: Matrix — Superposition with Cancellation

Row 1: ● ○ ●
Row 2: ○ ● ○
Row 3: ? (Row 1 ⊕ Row 2, with like elements cancelling)

(A) ● ● ●
(B) ○ ○ ○
(C) ● ○ ●
(D) ○ ● ○

**Solution:**
XOR rule (like elements cancel):
Row 1: ● ○ ●
Row 2: ○ ● ○
XOR: Each position where they differ → ●, where same → ○

Position 1: ● vs ○ → different → ●
Position 2: ○ vs ● → different → ●
Position 3: ● vs ○ → different → ●

Result: ● ● ●

**Answer: (A)** — ● ● ●

---

## Question 12: Arrow Rotation in Grid

A 2×2 grid has arrows:
Top-left: ↑, Top-right: →
Bottom-left: ←, Bottom-right: ↓

All arrows rotate 90° CW. New configuration?

(A) TL:→, TR:↓, BL:↑, BR:←
(B) TL:←, TR:↑, BL:↓, BR:→
(C) TL:↓, TR:←, BL:→, BR:↑
(D) TL:↑, TR:→, BL:←, BR:↓

**Solution:**
Each arrow rotates 90° CW:
- ↑ → → (CW)
- → → ↓ (CW)
- ← → ↑ (CW)
- ↓ → ← (CW)

New: TL:→, TR:↓, BL:↑, BR:←

**Answer: (A)** — TL:→, TR:↓, BL:↑, BR:←

---

## Question 13: Shape Morphing — Complex

Figure 1: Circle with 1 dot
Figure 2: Circle with 2 dots
Figure 3: Circle with 3 dots
Figure 4: Square with 1 dot
Figure 5: Square with 2 dots
Figure 6: ?

(A) Square with 3 dots
(B) Circle with 3 dots
(C) Square with 4 dots
(D) Triangle with 1 dot

**Solution:**
The pattern has two components:
1. Shape: Circle, Circle, Circle, Square, Square, ? → Square (groups of 3)
2. Dots: 1, 2, 3, 1, 2, ? → 3 (cycle of 3)

Figure 6: Square with 3 dots

**Answer: (A)** — Square with 3 dots.

---

## Question 14: Matrix — Movement Rule

3×3 grid, a star (★) moves:
Row 1: ★ at (1,1), empty, empty
Row 2: empty, ★ at (2,2), empty
Row 3: empty, empty, ★ at (3,3)

The star moves diagonally from top-left to bottom-right. Where would it be in Row 4 (hypothetically)?

(A) At (4,4) — continuing the diagonal
(B) At (4,1) — cycling back to start
(C) Disappears
(D) At (4,3)

**Solution:**
The star moves diagonally: (1,1) → (2,2) → (3,3)
This is a main diagonal movement.

If the grid were 4×4, the next position would be (4,4).
Since we only have a 3×3 grid, the star would cycle or bounce.

In ISRO-style questions, the diagonal movement continues to (4,4).

**Answer: (A)** — At (4,4), continuing the diagonal.

---

## Question 15: Size and Position Combined

Three figures in a series:
Figure 1: Large triangle at center
Figure 2: Medium triangle shifted right
Figure 3: Small triangle shifted further right

Figure 4 should be:

(A) Extra small triangle shifted even further right
(B) Large triangle at center (cycle restarts)
(C) Small triangle shifted left
(D) Medium triangle at center

**Solution:**
Trends:
1. Size: Large → Medium → Small (decreasing)
2. Position: Center → Right → Further right (moving right)

After reaching the extreme (smallest, furthest right), the pattern likely cycles:
- Size: Small → Large (restart)
- Position: Right → Center (restart)

**Answer: (B)** — Large triangle at center (cycle restarts).

---

## Question 16: Matrix — Row XOR

Grid:
Row 1: ●●○
Row 2: ●○●
Row 3: ○●?

Where ? is determined by XOR of Rows 1 and 2 (●=1, ○=0, XOR means different→●, same→○).

(A) ●
(B) ○
(C) ●●
(D) ○○

**Solution:**
Row 1: 1 1 0 (●●○)
Row 2: 1 0 1 (●○●)
XOR:    0 1 1 (○●●)

Position 3: 0 XOR 1 = 1 = ●

**Answer: (A)** — ●

---

## Question 17: Element Count Progression

Figure 1: 1 line segment
Figure 2: 2 line segments (angle)
Figure 3: 3 line segments (triangle)
Figure 4: 4 line segments (square)
Figure 5: ?

(A) Pentagon (5 lines)
(B) Hexagon (6 lines)
(C) Triangle (3 lines)
(D) Square with diagonal (5 lines)

**Solution:**
1 → 2 → 3 → 4 → 5 (element count increases by 1)
Figure 5 should have 5 line segments.

Option A (pentagon) has 5 sides = 5 line segments.
Option D (square + diagonal) has 4 + 1 = 5 line segments.

Both have 5 lines. But the pattern is building closed shapes: 1→2→3(triangle)→4(square)→5(pentagon).

**Answer: (A)** — Pentagon (5 sides, continues the shape-building pattern).

---

## Question 18: Pattern — Alternating

Figure 1: ● (black circle)
Figure 2: ○ (white circle)
Figure 3: ● (black circle)
Figure 4: ○ (white circle)
Figure 5: ?

(A) ● (black circle)
(B) ○ (white circle)
(C) ◐ (half circle)
(D) ●○ (both)

**Solution:**
Alternating pattern: Black, White, Black, White, ...
Next: Black

**Answer: (A)** — ● (black circle).

---

## Self-Assessment

| Metric | Target |
|--------|--------|
| Questions attempted | 18/18 |
| Correct answers | 14+/18 (80%+) |
| Average time per question | < 2 minutes |
| Questions needing review | Note them below |

**Questions I need to review**: _______________

**Key takeaways**:
1. 90° CW: Top→Right→Bottom→Left
2. Track ONE element across the series to find its movement rule
3. For matrices: check if Row 3 = Row 1 XOR Row 2 (common rule)
4. Shape morphing: count sides as primary discriminator
5. When patterns reach an extreme, they usually cycle back to the start
