# Abstract Reasoning - Concepts & Strategies

## ISRO Exam Context
- Part B Aptitude: 15 questions, 20 marks, NO negative marking
- Abstract reasoning typically accounts for 3-4 questions
- These test pattern recognition and logical thinking
- Time: ~2 minutes per question

---

## 1. Symbol Substitution (Coding-Decoding)

### Concept
A code language is defined where symbols/letters represent operations or other letters.

### Types
1. **Direct substitution**: A = +, B = -, C = ×, D = ÷ → Find value of expression
2. **Letter coding**: If WRITE = XVGHF, find how KNIFE is coded
3. **Conditional coding**: Coding depends on position or context

### Approach for Direct Substitution
- Read the code definition carefully
- Substitute each symbol in the expression
- Evaluate using BODMAS/BIDMAS
- Double-check the mapping before calculating

### Approach for Letter Coding
- Compare original and coded word letter by letter
- Find the shift pattern (e.g., +1, +2, +3...)
- Verify pattern with another given word
- Apply same pattern to target word

### Speed Tip
- Write down the complete substitution table before solving
- For letter shifts, check if it's a Caesar cipher or position-dependent

---

## 2. Coding-Decoding Patterns

### Common Patterns
| Pattern Type | Example | Rule |
|-------------|---------|------|
| Caesar shift | CAT → DBU | Each letter +1 |
| Reverse coding | CAT → TAC | Reversed string |
| Position coding | CAT → CZT | A→Z, T→T, C→C (symmetric) |
| Skipping | CAT → CVT | +0, +2, +0 |
| Word-based | CAT → FOX | A=1, B=2, ..., sum or product |

### Advanced Patterns
- **Interleaved coding**: Coded in pairs or alternating positions
- **Conditional coding**: Different rules for vowels and consonants
- **Matrix coding**: 2D grid-based encoding

### Speed Tip
- For short codes (2-3 letter change), list all possibilities
- For long codes, find the pattern from first few letters and verify

---

## 3. Letter Series

### Concept
A series of letters follows a pattern. Find the next letter(s).

### Common Patterns
1. **Skip pattern**: A(0) C(+2) E(+2) G(+2) → I
2. **Reverse direction**: A B C D C B → A
3. **Multiple series**: Interleaved patterns (1st, 3rd, 5th... and 2nd, 4th, 6th...)
4. **Alphabetical groups**: ABC, DEF, GHI → JKL
5. **Mirror pairs**: AZ, BY, CX → DW (A-Z=25, B-Y=25, C-X=25)

### Approach
- Write the alphabet with position numbers: A=1, B=2, ..., Z=26
- Find the gap between consecutive letters
- Check if gaps are constant, increasing, or following a pattern
- If alternating series, separate into odd-positioned and even-positioned

### Speed Tip
- Use the position numbers directly (A=1, Z=26)
- For mirror pairs: first + last = 27 (A+Z=27, B+Y=27, etc.)

---

## 4. Number Analogy

### Concept
Find the relationship between a pair of numbers and apply it to find the missing number.

### Common Relationships
| Type | Example | Rule |
|------|---------|------|
| Sum | 3,5 → 8 | a + b = c |
| Product | 3,5 → 15 | a × b = c |
| Difference | 5,3 → 2 | a - b = c |
| Square | 3 → 9 | a² = b |
| Position-based | 3,5 → 35 | Concatenate |
| Digit operation | 23 → 5 | 2+3=5 or 2×3=6 |

### Speed Tip
- Check arithmetic operations first (+, -, ×, ÷)
- Then check digit operations (sum of digits, product of digits)
- Then check squares and cubes

---

## 5. Figure Analogy

### Concept
Similar to visual analogy but with abstract figures (shapes, lines, dots).

### Approach
1. Identify the transformation rule from first pair
2. Common transformations:
   - Number of sides increases/decreases
   - Elements rotate
   - Shading inverts
   - Elements are added/removed
   - Size changes proportionally
3. Apply the SAME transformation to the third figure

### Speed Tip
- Count elements first (quickest check)
- Then verify rotation/orientation
- Then check shading/color

---

## 6. Matrix Completion

### Concept
A 3×3 or 2×2 grid of figures with one missing. Find the pattern across rows and columns.

### Approach
1. **Row analysis**: Check what changes across each row
2. **Column analysis**: Check what changes down each column
3. **Diagonal analysis**: Check diagonal patterns
4. **Global patterns**: Count total elements, check symmetry

### Common Row Patterns
- Elements rotate by fixed angle
- Elements are added/removed sequentially
- Elements shift position (move right/down)

### Common Column Patterns
- Progressive size change
- Progressive shading change
- Element count increases/decreases

### Speed Tip
- Check rows first (usually the primary pattern)
- If rows don't reveal the pattern, check columns
- For 3×3: the third row/column often combines elements from first two

---

## 7. Number Series

### Concept
Find the next number in a sequence.

### Common Patterns
| Pattern | Example | Rule |
|---------|---------|------|
| Arithmetic | 2,5,8,11,... | +3 each time |
| Geometric | 2,6,18,54,... | ×3 each time |
| Fibonacci | 1,1,2,3,5,... | Sum of previous two |
| Square | 1,4,9,16,... | n² |
| Cube | 1,8,27,64,... | n³ |
| Prime | 2,3,5,7,11,... | Prime numbers |
| Nested | 1,11,21,1211,... | Look and say |

### Speed Tip
- Calculate differences between consecutive terms
- If differences are constant: arithmetic progression
- If ratios are constant: geometric progression
- If differences have a pattern: check second differences

---

## 8. Symbol Pattern Recognition

### Concept
Find the pattern in a sequence of symbols and identify the next one.

### Approach
- Count the number of each symbol type
- Check for alternating patterns
- Look for movement/position changes
- Verify if the pattern is cyclic

---

## Speed-Solving Framework for Abstract Reasoning

### Step 1: Identify the Question Type (5 seconds)
- Is it coding/decoding, series, analogy, or matrix?

### Step 2: Find the Rule (30 seconds)
- Compare given pairs/groups systematically
- Write down the rule explicitly

### Step 3: Apply and Verify (30 seconds)
- Apply the rule to find the answer
- Verify with all given data points

### Step 4: Check Alternative Interpretations (20 seconds)
- Could there be another valid rule?
- If multiple rules fit, choose the simpler one (Occam's razor)

---

## Common ISRO Abstract Reasoning Patterns

1. **Alphabet position arithmetic**: A=1, B=2, etc. — operations on positions
2. **Cyclic patterns**: Elements that repeat in a cycle
3. **Interleaved series**: Two independent series woven together
4. **Conditional rules**: Different rules for different element types
5. **Matrix XOR**: Elements present in exactly one of the row/column inputs

---

## Speed-Solving Tips Summary

| Technique | When to Use | Time Saved |
|-----------|-------------|------------|
| Position numbering | Letter series, coding | ~30 seconds |
| Difference method | Number series | ~20 seconds |
| Element counting | Figure matrices | ~15 seconds |
| Rule extraction | Analogy questions | ~25 seconds |
| Elimination | All types | ~20 seconds |

---

## Quick Check: Common Letter-Number Mapping

| Letter | A | B | C | D | E | F | G | H | I | J | K | L | M |
|--------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Number | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |

| Letter | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
|--------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Number | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |

### Key Relationships
- A+Z = 27, B+Y = 27, C+X = 27 (mirror pairs sum to 27)
- A=1, E=5, I=9, O=15, U=21 (vowels at specific positions)
- Reverse alphabet: Z=1, Y=2, ..., A=26
