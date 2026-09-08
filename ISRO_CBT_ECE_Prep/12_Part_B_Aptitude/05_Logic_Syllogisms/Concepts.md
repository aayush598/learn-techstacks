# Logic Syllogisms - Concepts & Strategies

## ISRO Exam Context
- Part B Aptitude: 15 questions, 20 marks, NO negative marking
- Logic syllogisms: 1-2 questions per exam
- Tests logical deduction and reasoning ability
- Time: ~1.5 minutes per question (faster than visual types)

---

## 1. Categorical Syllogisms

### What is a Syllogism?
A syllogism is a form of logical reasoning where a conclusion is drawn from two given premises.

### Structure
```
Major Premise: All A are B
Minor Premise: All C are A
Conclusion: All C are B
```

### Standard Form
- **Major Premise**: Contains the major term (predicate of conclusion) and middle term
- **Minor Premise**: Contains the minor term (subject of conclusion) and middle term
- **Conclusion**: Links minor term to major term

### Example
```
Premise 1: All engineers are graduates
Premise 2: All ISRO scientists are engineers
Conclusion: All ISRO scientists are graduates ✓
```

---

## 2. Types of Categorical Propositions

| Type | Symbol | Example | Quantity | Quality |
|------|--------|---------|----------|---------|
| Universal Affirmative | A | All A are B | Universal | Affirmative |
| Universal Negative | E | No A are B | Universal | Negative |
| Particular Affirmative | I | Some A are B | Particular | Affirmative |
| Particular Negative | O | Some A are not B | Particular | Negative |

### Key Relationships
- **Contradictory**: A↔O, E↔I (one true, other false, always)
- **Contrary**: A and E (both can't be true, both can be false)
- **Subcontrary**: I and O (both can be true, both can't be false)
- **Subalternation**: A→I, E→O (if universal true, particular true)

---

## 3. Venn Diagram Method for Syllogisms

### Three-Circle Method
Each category gets a circle. The three circles represent the three terms (A, B, C).

### Steps
1. Draw three overlapping circles labeled with the three terms
2. **Universal (All/No)**: Shade the area that is excluded
3. **Particular (Some)**: Place an X in the area that is included
4. **Check conclusion**: Does the diagram automatically show the conclusion?

### Shading Rules
| Premise | Shading |
|---------|---------|
| All A are B | Shade area of A that is NOT in B |
| No A are B | Shade area where A and B overlap |
| Some A are B | Place X in the overlap of A and B |
| Some A are not B | Place X in A but outside B |

### Speed Tip
- After drawing the diagram, the conclusion is valid if it's NECESSARILY true
- If the conclusion MIGHT be true but isn't guaranteed, it's INVALID

---

## 4. Premise-Conclusion Validity

### Valid Syllogistic Forms (Mnemonic: "Barbara" and "Celarent")
| Form | Major | Minor | Conclusion | Valid? |
|------|-------|-------|------------|--------|
| AAA-1 | All M are P | All S are M | All S are P | ✓ Valid |
| EAE-1 | No M are P | All S are M | No S are P | ✓ Valid |
| AII-1 | All M are P | Some S are M | Some S are P | ✓ Valid |
| EIO-1 | No M are P | Some S are M | Some S are not P | ✓ Valid |
| AEE-2 | All P are M | No S are M | No S are P | ✓ Valid |
| AOO-2 | All P are M | Some S are not M | Some S are not P | ✓ Valid |

### Invalid Forms (Common Traps)
| Form | Why Invalid |
|------|-------------|
| IIA-3 | Particular → Universal (can't conclude universal from particular) |
| AOO-1 | Undistributed middle |
| AAA-2 | Middle term not distributed |

---

## 5. Common Syllogistic Fallacies

### Fallacy 1: Undistributed Middle
```
All dogs are animals
All cats are animals
∴ All cats are dogs ← INVALID
```
The middle term "animals" is never distributed (never covers ALL animals).

### Fallacy 2: Illicit Major/Minor
```
All birds are animals
No cats are birds
∴ No cats are animals ← INVALID
```
The major term "animals" is distributed in conclusion but not in the premise.

### Fallacy 3: Exclusive Premises
```
No A are B
No B are C
∴ No A are C ← INVALID
```
Two negative premises cannot yield a valid conclusion.

### Fallacy 4: Affirmative from Negative
```
All A are B
No B are C
∴ Some A are C ← INVALID
```
A valid conclusion from one affirmative and one negative premise must be negative.

### Fallacy 5: Particular Conclusion from Universal Premises (can be valid)
Actually, universal premises CAN yield particular conclusions (valid).
The fallacy is: particular premises CANNOT yield universal conclusions.

---

## 6. Distribution Rules

### What is a Term "Distributed"?
A term is distributed if the proposition says something about ALL members of that class.

| Proposition | Subject Distributed? | Predicate Distributed? |
|-------------|---------------------|----------------------|
| All A are B | Yes | No |
| No A are B | Yes | Yes |
| Some A are B | No | No |
| Some A are not B | No | Yes |

### Rules for Valid Syllogism
1. The middle term must be distributed at least once
2. If a term is distributed in the conclusion, it must be distributed in the premise
3. Two negative premises yield no valid conclusion
4. If one premise is negative, the conclusion must be negative (and vice versa)
5. Two particular premises yield no valid conclusion

---

## 7. Quick Deduction Techniques

### Technique 1: Chain Rule
```
All A are B
All B are C
∴ All A are C (Chain)
```

### Technique 2: Some-Chain
```
All A are B
Some C are A
∴ Some C are B
```

### Technique 3: No-Chain
```
No A are B
All B are C
∴ No A are C
```

### Technique 4: Double Negative
```
No A are B
No B are C (but C has elements outside B)
Some C are not A (might be valid depending on overlap)
```

---

## 8. Syllogism with "Only" and "All"

### "Only" Statements
- "Only A are B" = "All B are A" (B is a subset of A)
- "Only graduates can apply" = "All who can apply are graduates"

### Common Confusion
- "All A are B" ≠ "All B are A"
- "Some A are B" = "Some B are A" (symmetric)
- "No A are B" = "No B are A" (symmetric)

---

## Speed-Solving Framework

### Step 1: Identify Terms (5 seconds)
- What are the three terms? (Subject, Predicate, Middle)

### Step 2: Draw Venn Diagram (20 seconds)
- Three circles, shade/Mark X based on premises

### Step 3: Check Conclusion (10 seconds)
- Does the conclusion follow from the diagram?

### Step 4: Alternative: Use Rules (15 seconds)
- Check distribution, check for fallacies

---

## Quick Reference Table

| Premise Combination | Valid Conclusion Type |
|--------------------|-----------------------|
| Two Universal (A+A, A+E, E+E) | Universal or Particular (check rules) |
| One Universal + One Particular | Particular only |
| Two Particular | NO valid conclusion |
| Two Affirmative | Affirmative only |
| One Affirmative + One Negative | Negative only |
| Two Negative | NO valid conclusion |

---

## Common ISRO Syllogism Patterns

1. **All A are B, All B are C → All A are C** (chain rule, most common)
2. **Some A are B, All B are C → Some A are C** (some + all)
3. **No A are B, All B are C → No A are C** (no + all)
4. **All A are B, No B are C → No A are C** (all + no)
5. **All A are B, Some C are B → Some C are A** (can't conclude — common trap!)

---

## Speed Tips Summary

| Technique | When to Use | Time Saved |
|-----------|-------------|------------|
| Venn diagram | Complex syllogisms | ~30 seconds |
| Chain rule | All-All-All patterns | ~20 seconds |
| Distribution check | Validity verification | ~15 seconds |
| Elimination | Multiple choice | ~20 seconds |
| "Only" conversion | "Only A are B" statements | ~10 seconds |
